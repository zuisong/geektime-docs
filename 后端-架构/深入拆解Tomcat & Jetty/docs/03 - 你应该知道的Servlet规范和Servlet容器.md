通过专栏上一期的学习我们知道，浏览器发给服务端的是一个HTTP格式的请求，HTTP服务器收到这个请求后，需要调用服务端程序来处理，所谓的服务端程序就是你写的Java类，一般来说不同的请求需要由不同的Java类来处理。

那么问题来了，HTTP服务器怎么知道要调用哪个Java类的哪个方法呢。最直接的做法是在HTTP服务器代码里写一大堆if else逻辑判断：如果是A请求就调X类的M1方法，如果是B请求就调Y类的M2方法。但这样做明显有问题，因为HTTP服务器的代码跟业务逻辑耦合在一起了，如果新加一个业务方法还要改HTTP服务器的代码。

那该怎么解决这个问题呢？我们知道，面向接口编程是解决耦合问题的法宝，于是有一伙人就定义了一个接口，各种业务类都必须实现这个接口，这个接口就叫Servlet接口，有时我们也把实现了Servlet接口的业务类叫作Servlet。

但是这里还有一个问题，对于特定的请求，HTTP服务器如何知道由哪个Servlet来处理呢？Servlet又是由谁来实例化呢？显然HTTP服务器不适合做这个工作，否则又和业务类耦合了。

于是，还是那伙人又发明了Servlet容器，Servlet容器用来加载和管理业务类。HTTP服务器不直接跟业务类打交道，而是把请求交给Servlet容器去处理，Servlet容器会将请求转发到具体的Servlet，如果这个Servlet还没创建，就加载并实例化这个Servlet，然后调用这个Servlet的接口方法。因此Servlet接口其实是**Servlet容器跟具体业务类之间的接口**。下面我们通过一张图来加深理解。
<div><strong>精选留言（30）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/13/9d/f5/c74224dc.jpg" width="30px"><span>天琊</span> 👍（390） 💬（24）<div>文章中提到
1.SpringMVC 容器实在DispatcherServlet中init方法里创建的。
2.Spring 容器是通过Listener创建的
a、就是说SpringMVC容器和Spring容器还不一样，那么他们是什么关系？
b、他们和Servlet容器又是啥关系？</div>2019-05-16</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/16/5b/83a35681.jpg" width="30px"><span>Monday</span> 👍（51） 💬（2）<div>基于思考题，我在梦中醒来，觉得servlet容器管理的是servlet（把controller也理解成了servlet），spring容器则是管理service，DAO这类bean。这样理解的话springMVC不就是多余的了吗？但是我们项目中都有使用springMVC，存在即合理，所以我的理解是有误的。于是想老师帮忙给出以下三张图。非常感谢，
1，恳求老师能给出servlet，spring，springMVC三个容器的关系图。
2，恳求老师给出初始化三个容器的顺序图
3，恳求老师给出tomcat在响应客户端请求时，以上3个容器的分工以及各自是在什么时候产生作用的。类似于第2节http必知必会中，用户在浏览器输入url到最后浏览器返回展示的那样的11步的图，并做出每一步的解释。
PS：本文通读不少于3遍，收获颇丰。提这个问题是手机敲的字，和整理提问思路一起花了半小时。</div>2019-05-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/ec/13/49e98289.jpg" width="30px"><span>neohope</span> 👍（48） 💬（9）<div>Servlet容器，是用于管理Servlet生命周期的。
Spring容器，是用于管理Spring Bean生命周期的。
SpringMVC容器，适用于管理SpringMVC Bean生命周期的。

Tomcat&#47;Jetty启动，对于每个WebApp，依次进行初始化工作：
1、对每个WebApp，都有一个WebApp ClassLoader，和一个ServletContext
2、ServletContext启动时，会扫描web.xml配置文件，找到Filter、Listener和Servlet配置

3、如果Listener中配有spring的ContextLoaderListener
3.1、ContextLoaderListener就会收到webapp的各种状态信息。
3.3、在ServletContext初始化时，ContextLoaderListener也就会将Spring IOC容器进行初始化，管理Spring相关的Bean。
3.4、ContextLoaderListener会将Spring IOC容器存放到ServletContext中

4、如果Servlet中配有SpringMVC的DispatcherServlet
4.1、DispatcherServlet初始化时（其一次请求到达）。
4.2、其中，DispatcherServlet会初始化自己的SpringMVC容器，用来管理Spring MVC相关的Bean。
4.3、SpringMVC容器可以通过ServletContext获取Spring容器，并将Spring容器设置为自己的根容器。而子容器可以访问父容器，从而在Controller里可以访问Service对象，但是在Service里不可以访问Controller对象。
4.2、初始化完毕后，DispatcherServlet开始处理MVC中的请求映射关系。

有一个很坑问题，Servlet默认是单例模式的，Spring的Bean默认是单例模式的，那Spring MVC是如何处理并发请求的呢？</div>2019-05-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/97/1a/389eab84.jpg" width="30px"><span>而立斋</span> 👍（40） 💬（3）<div>spring容器中还包含许多的子容器，其中springmvc容器就是其中常用的一个，文中的DispatcherServlet就是springmvc容器中的servlet接口，也是springmvc容器的核心类。spring容器主要用于整个Web应用程序需要共享的一些组件，比如DAO、数据库的ConnectionFactory等,springmvc的容器主要用于和该Servlet相关的一些组件,比如Controller、ViewResovler等。至此就清楚了spring容器内部的关系，那servlet容器跟spring容器又有什么关系呢？有人说spring容器是servlet容器的子容器，但是这个servlet容器到底是tomcat实现的容器呢，还是jetty实现的容器呢？所以我觉得spring容器与servlet容器他们之间并没有直接的血缘关系，可以说spring容器依赖了servlet容器，spring容器的实现遵循了Servlet 规范。不知道这么理解是可以，还请老师给予指导？</div>2019-05-16</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/DYAIOgq83eoRiaKX0ulEibbbwM4xhjyMeza0Pyp7KO1mqvfJceiaM6ZNtGpXJibI6P2qHGwBP9GKwOt9LgHicHflBXw/132" width="30px"><span>Geek_ebda96</span> 👍（32） 💬（2）<div>老师，spring容器指的是spring本身的ioc容器吧，是用来管理所有的bean，servlet本身会把sping的容器设置到上下文中，而spring mvc的容器dispatch servlet相当于是一个具体的servlet的实现，然后会创建一个全局的上下文application context spring的ioc容器会注入到这个上下文中，后面通过上下文getbean，其实是先找到上下文中的ioc容器，然后再从这个容器拿到具体的bean，这是不是对的？</div>2019-05-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/70/9e/9337ca8e.jpg" width="30px"><span>jaryoung</span> 👍（31） 💬（3）<div>没有Spring boot以前，他们的关系为tomcat抱着Spring的关系，有了Spring boot之后他们关系刚好反过来。</div>2019-08-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/3b/5d/15c4817a.jpg" width="30px"><span>xxxxL</span> 👍（27） 💬（1）<div>请问service方法为什么把request和response都当作输入参数，而不是输入参数只有request，response放到返回值里呢？</div>2019-05-31</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/10/61/7ba48062.jpg" width="30px"><span>菜鸡小王子</span> 👍（17） 💬（1）<div>老师问一下  tomcat分为http服务器+sevlet服务器  这个http服务器怎么理解呢</div>2019-05-30</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/03/e2/5768d26e.jpg" width="30px"><span>inrtyx</span> 👍（16） 💬（1）<div>老题，问下。springmvc如何实现url到方法的映射</div>2019-05-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/c2/cc/ca22bb7c.jpg" width="30px"><span>蓝士钦</span> 👍（14） 💬（2）<div>课后思考：
Servlet容器与Spring容器的关系：
1.Servlet容器管理Servlet对象
2.Spring容器管理Spring 的Bean对象（Service和Dao）
3.SpringMVC容器管理 Controller的Bean对象，本质上也是Servlet对象。Servlet容器和SpringMVC容器通过web.xml配置文件产生交集。
Spring容器管理所有的Bean并且包括SpringMVC容器。

疑问：
为什么SpringMVC要实现自己的容器，并且和Spring容器为父子关系，直接用Spring容器不可以吗？Spring是如何区分Bean属于哪个容器的呢？
</div>2019-06-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/9f/98/b6f20c10.jpg" width="30px"><span>王皓月</span> 👍（12） 💬（1）<div>老师您好！请问您的置顶回复中“IoC容器初始化完毕后，Spring将其存储到ServletContext中，便于以后来获取”，对于这句话我不是很理解，想请老师解答一下IoC容器是如何被存储到ServletContext中的，以及为什么要这么做，相应的源码在哪里看。非常感谢老师~</div>2019-05-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/ee/67/d6d9499e.jpg" width="30px"><span>木木木</span> 👍（11） 💬（1）<div>老师能不能大概介绍下tomcat这种容器的具体调试方式，比如结合一个场景，加载实例化serverlet。</div>2019-05-30</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/0f/4f/c75c4889.jpg" width="30px"><span>石头狮子</span> 👍（11） 💬（1）<div>servlet 容器抽象了网络处理，请求封装等事情，同样提供了可以处理其他非 http 协议的能力。
spring 容器是依赖注入设计模式的体现，其主要抽象了类初始化，注入，依赖解决，动态代理等功能。
两者主要解决的问题不同。
</div>2019-05-16</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/d4/44/ec084136.jpg" width="30px"><span>LoveDlei</span> 👍（10） 💬（1）<div>请问老师：springboot 和tomcat 如何融合到一起的啊？</div>2019-05-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/79/4b/740f91ca.jpg" width="30px"><span>-W.LI-</span> 👍（10） 💬（3）<div>老师好!我看留言里有同学说，spring上下文负责创建service和dao的bean，MVC负责创建controller的bean。我们平时说的IOC容器是指哪个啊?还有就是controller注解是一个组合注解，我在controller上用service注解一样能注册成功，spring和MVC容器又是怎么区分这个bean是controller还是service,或者是dao，bean的?还是我完全理解错了。</div>2019-05-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/63/c5/a85ade71.jpg" width="30px"><span>刘冬</span> 👍（9） 💬（1）<div> 老师你好，请问在SpringBoot项目中，为什么没有web.xml了？
我的理解是：SpringBoot本身是个App，调用启动Tomcat，而这个Tomcat的Servlet Container中只有一个Servlet，所有的请求一定都是发给这个Servlet处理，所以不需要web.xml来匹配请求应该有哪个Servlet处理。所以web.xml不写也没有影响。
请问我的理解对吗？另外，如果没有web.xml了，Tomcat不报错吗？ </div>2019-05-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/65/84/5515dde0.jpg" width="30px"><span>李青</span> 👍（9） 💬（1）<div>老师给你个大大的赞，讲课方式是我很喜欢的风格，先抛出问题，再讲思路和解决方案。以后讲课希望一直用这个风格</div>2019-05-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/39/24/963178c4.jpg" width="30px"><span>rrbbt</span> 👍（8） 💬（1）<div>老师，tomcat是servlet容器，spring也是servlet容器，为什么两个都是servlet容器？这个有点搞不懂</div>2019-05-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/65/9c/5c94692c.jpg" width="30px"><span>_关旭_</span> 👍（7） 💬（2）<div>还是没能明白spring容器和spring mvc容器的区别,是说@service注解下的类由spring容器管理,@controller下的由spring mvc容器管理吗</div>2019-09-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/f8/76/3db69173.jpg" width="30px"><span>onepieceJT2018</span> 👍（7） 💬（1）<div>请教下 http请求怎么打到servlet上的 本质上是socket连接 拿到报文？</div>2019-05-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/15/87/d22d8c3e.jpg" width="30px"><span>_你说了不算</span> 👍（7） 💬（1）<div>老师好，请问下http服务器指的是什么？跟tomcat什么关系？</div>2019-05-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/64/86/f5a9403a.jpg" width="30px"><span>yang</span> 👍（7） 💬（2）<div>1. 一个应用中的多个Servlet共享唯一的一个ServletContext不会有问题嘛？ 
  老师，求告知这个源码的入口从哪里看啊？

2.我猜想Spring容器是管理Servlet容器的吧？ 一个Spring容器可以被多个Servlet容器共享吗，不会有问题吗？

李老师，我底子差，可能专栏的文字与音频篇幅有限，
恳请您也在极客邦的github下建一个仓库，这样后面接下来的章节中如果遇到源代码的讲解，或者类似这种tomcat容器源代码的讲解，或者Spring容器的讲解，可以以代码或者其他文件形式给大家看看嘛~！让我们通过您更多的分享可以理解的更透彻一点~！

3. 老师，tomcat容器的入口是ServletContext吗？  spring容器的入口是dispatcherServlet吗？

ps:一篇引人思考的技术类文章不应该它写完了，普及度就降低了。应该让后续的人读完之后在这篇文章的引导下能通过自己的努力弄明白它原来是什么样子的。 很多人在看与学的过程中苦于没有人讨论，交流而显得很闭塞。我就是其中之一。  这也可能能增加大家的讨论热度吧~！  

可能我说的太多了， 也可能不多，不过还是要谢谢老师的讲解~！</div>2019-05-16</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/39/c1/2f9bde7a.jpg" width="30px"><span>军哥</span> 👍（7） 💬（1）<div>或者说，单单一个servlet 容器有什么用？</div>2019-05-16</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/e8/f5/e758b7b6.jpg" width="30px"><span>karen</span> 👍（6） 💬（1）<div>第一张图，Servlet容器和下面业务类之间连接的部分，能说下具体都是什么嘛</div>2019-05-24</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/IgjIXs9jjpODTPaOLrms0XOhJ8pxMcaZgtgBrPG6deqsKXv1sPIqkg0faL6X0rtFicJn5Wf7QXTickjYWpmF0V8A/132" width="30px"><span>Geek_28b75e</span> 👍（6） 💬（1）<div>“Servlet 规范并不在乎通信协议是什么”，tomcat又包含http服务器的功能，那么tomcat是不是只能处理http协议类型的请求呢？</div>2019-05-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/79/4b/740f91ca.jpg" width="30px"><span>-W.LI-</span> 👍（6） 💬（1）<div>刚试了下在service对象中采用set注入和构造器注入controlle对象都成功了，项目是springboot项目。是sprringboot实例化对象方式和传统的spring不一样么导致的么?希望老师帮忙解惑!</div>2019-05-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/17/77/61/adf1c799.jpg" width="30px"><span>KL3</span> 👍（6） 💬（1）<div>请问老师，spring容器初始化后放在servletcontext的属性里，那springmvc创建后是不是也放在servletcontext的属性里</div>2019-05-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/17/64/da/5fb5817c.jpg" width="30px"><span>蔡伶</span> 👍（6） 💬（1）<div>打卡
给老师提个建议：介绍下servlet规范和spring的历史起源演变过程，这样大家对于技术的发展脉络就会有更准确的认识。
本课程理解：
http服务，处理hhttp协议网络连接的事情。
servlet容器，基于servlet规范实现网络协议与业务逻辑的解耦，常用实现有tomcat,jboss,weblogic等。
spring容器，servlet规范项下servlet实现，可以理解为一个大servlet。主要解决业务类的解耦和管理，也就是常说的IOC依赖注入；同时spring还集成了持久化、事务管理、MVC等众多功能，可以作为轻量级企业应用服务框架。</div>2019-05-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/02/c8/a6a2a182.jpg" width="30px"><span>许路路</span> 👍（6） 💬（1）<div>老师好，mvc中的lanjieqi跟servlet中的过滤器是什么关系</div>2019-05-16</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/e9/0b/1171ac71.jpg" width="30px"><span>WL</span> 👍（5） 💬（1）<div>关于Servlet容器的实现我有点晕， 请问一下老师Servlet容器对应的实现是哪个对象， 是ServletContext吗？ </div>2019-05-18</li><br/>
</ul>