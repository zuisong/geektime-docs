专栏上一期我们学完了连接器的设计，今天我们一起来看一下Tomcat的容器设计。先复习一下，上期我讲到了Tomcat有两个核心组件：连接器和容器，其中连接器负责外部交流，容器负责内部处理。具体来说就是，连接器处理Socket通信和应用层协议的解析，得到Servlet请求；而容器则负责处理Servlet请求。我们通过下面这张图来回忆一下。

![](https://static001.geekbang.org/resource/image/ee/d6/ee880033c5ae38125fa91fb3c4f8cad6.jpg?wh=1580%2A836)

容器，顾名思义就是用来装载东西的器具，在Tomcat里，容器就是用来装载Servlet的。那Tomcat的Servlet容器是如何设计的呢？

## 容器的层次结构

Tomcat设计了4种容器，分别是Engine、Host、Context和Wrapper。这4种容器不是平行关系，而是父子关系。下面我画了一张图帮你理解它们的关系。

![](https://static001.geekbang.org/resource/image/cc/ed/cc968a11925591df558da0e7393f06ed.jpg?wh=1172%2A718)

你可能会问，为什么要设计成这么多层次的容器，这不是增加了复杂度吗？其实这背后的考虑是，**Tomcat通过一种分层的架构，使得Servlet容器具有很好的灵活性。**

Context表示一个Web应用程序；Wrapper表示一个Servlet，一个Web应用程序中可能会有多个Servlet；Host代表的是一个虚拟主机，或者说一个站点，可以给Tomcat配置多个虚拟主机地址，而一个虚拟主机下可以部署多个Web应用程序；Engine表示引擎，用来管理多个虚拟站点，一个Service最多只能有一个Engine。
<div><strong>精选留言（30）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/12/93/ee/101f0356.jpg" width="30px"><span>一路远行</span> 👍（229） 💬（9）<div>1）Servlet规范中ServletContext表示web应用的上下文环境，而web应用对应tomcat的概念是Context，所以从设计上，ServletContext自然会成为tomcat的Context具体实现的一个成员变量。

2）tomcat内部实现也是这样完成的，ServletContext对应tomcat实现是org.apache.catalina.core.ApplicationContext，Context容器对应tomcat实现是org.apache.catalina.core.StandardContext。ApplicationContext是StandardContext的一个成员变量。

3）Spring的ApplicationContext之前已经介绍过，tomcat启动过程中ContextLoaderListener会监听到容器初始化事件，它的contextInitialized方法中，Spring会初始化全局的Spring根容器ApplicationContext，初始化完毕后，Spring将其存储到ServletContext中。

总而言之，Servlet规范中ServletContext是tomcat的Context实现的一个成员变量，而Spring的ApplicationContext是Servlet规范中ServletContext的一个属性。</div>2019-05-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/17/70/0c/c923c776.jpg" width="30px"><span>阿旺</span> 👍（75） 💬（4）<div>你好 请问到业务的controller是从哪部分进去的呢 谢谢</div>2019-05-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/36/d2/c7357723.jpg" width="30px"><span>发条橙子 。</span> 👍（70） 💬（4）<div>老师 ， 我之前一直误以为一个 server表示我们一个应用(实际上只是代表一个tomcat实例)，所以一直不理解为什么 server 下通过 host 可以配置多个应用 ，学了这节，发现是一个context对应一个应用， 自己百度了一下，原来可以通过 host 或者 service 来让 tomcat 访问不同的目录来访问多个应用 。

1. 但是我看生产环境中， 配的都是一个 tomcat 对应一个应用, 多个应用就用多个tomcat 。  那么他和一个 tomcat 加载多个应用有什么区别么 。难道用一个tomcat是为了节约内存么， 用一个tomcat加载多个应用都有什么弊端呢 ？？ 比如应用的上限 ，希望老师指点一下 。 而且一个tomcat里多个应用的话， 我们就无法用 ps -ef | grep tomcat 来定位到我们的真实应用了。
2. 老师后面讲的， 通过责任链模式， 一步一步解析到 wrapper 的 servlet ， 那不是应该调用servlet 的 doGet()／doPost() 方法了么 ，老师说的创建一个 filter 链，并调用Servlet 的 service 方法， 这句话我不是很理解 </div>2019-05-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/74/c9/d3439ca4.jpg" width="30px"><span>why</span> 👍（60） 💬（4）<div>- 容器的层次结构
    - Engine, Host, Context, Wrapper, 是嵌套关系
    - 一个 Tomcat 实例包含一个 Engine, 一个 Engine 包含多个 Host, 以此类推
    - 容器采用组合模式, 所有容器组件都实现 Container 接口, 保证使用一致性
- 定位 Servlet 的过程
    - 由 Mapper 组件完成, Mapper 组件保存了容器组件与访问路径的映射关系, 根据请求的 URL 进行定位
        - 端口号定位出 Service 和 Engine
        - 域名定位出 Host
        - URL 路径定位出 Context Web 应用
        - URL 路径定位出 Wrapper ( Servlet )
        - 在各个层次定位过程中, 都会对请求做一些处理
    - 通过 Pipeline-Valve 实现容器间的互相调用 ( 责任链模式 )
        - valve 表示一个处理点 ( 如权限认证, 日志等), 处理请求; valve 通过链表串联, 并由 pipeline 维护
        - valve 会通过 getNext().invoke() 调用下一个 valve, 最后一个 valve ( Basic ) 调用下一层容器的 pipeline 的第一个 valve
        - Adapter 调用 Engine pipeline 的第一个 valve
        - Wrapper 最后一个 valve 会创建一个 Filter 链, 并最终调用 Servlet 的 service 方法
    - valve 与 filter 对比
        - valve 是 Tomcat 的私有机制, Filter 是 Servlet API 公有标准
        - valve 工作在容器级别, 拦截所有应用; Servlet Filter 工作在应用级别, 只能拦截某个应用的请求
- 留言

    &gt; Tomcat 的 Context 是一个 Web 应用; Servlet 的 ServletContext 是 Web 应用上下文, 是 Context 的一个成员变量; Spring 的 ApplicationContext 是 spring 容器, 是 Servlet 的一个属性.</div>2019-05-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/dc/ce/a144dea1.jpg" width="30px"><span>yhh</span> 👍（47） 💬（3）<div>Basic value 有些疑惑。比如engine容器下有多个host容器，那engine容器的basic value是怎么知道要指向哪个host容器的value呢？</div>2019-05-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/d3/6e/281b85aa.jpg" width="30px"><span>永光</span> 👍（27） 💬（3）<div>老师您好，
你看这样理解对吗？，一个Engine可以对应多个Host，一个Host下面可以放多个应用。
问题：
1、如果我有两个应用需要部署，现在就可以有很多种方案了。
     部署在同一个service下（同一个Engine）的同一个Host目录下
     部署在同一个service下（同一个Engine）的不同Host目录下
     部署在不同Service下（不同Engine）的各自Host目录下
这几种部署方式有什么差异以及优缺点？以及分别适用于什么场合呀？
谢谢
</div>2019-06-04</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/97/1a/389eab84.jpg" width="30px"><span>而立斋</span> 👍（24） 💬（3）<div>老师，能提供一份tomcat多host的配置吗？</div>2019-05-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/bb/c9/37924ad4.jpg" width="30px"><span>天天向上</span> 👍（18） 💬（1）<div>Connector和Engine是平级的，并且 Connector可以有多个 容器结构图 xml结构表示的有问题吧</div>2019-05-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/93/ee/101f0356.jpg" width="30px"><span>一路远行</span> 👍（17） 💬（1）<div>这段话的描述有些不准确：
“首先，根据协议和端口号选定 Service 和 Engine。”

我的理解是，connector配置中只要有端口号就可以确定service和engine，协议的配置只是为了解析，对请求的路由决策没有起到作用。</div>2019-05-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/64/86/f5a9403a.jpg" width="30px"><span>yang</span> 👍（15） 💬（0）<div>老师，  关于 MapperHost的构造方法  

        public MappedHost(String name, Host host) {
            super(name, host);
            realHost = this;
            contextList = new ContextList();
            aliases = new CopyOnWriteArrayList&lt;&gt;();
        }

不会存在  this泄露吗？

 public volatile ContextList contextList;

contextList 尽管使用volatile修饰的，可以防止编译指令重拍序，并保证可见性。  

但是，它没办法保证 还没构造完，这个new出来的对象，就不被其他线程使用啊？  求老师解答~！</div>2019-06-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/1a/7c/e1d33f7c.jpg" width="30px"><span>robert_z_zhang</span> 👍（15） 💬（0）<div>老师，filter中没有办法直接使用@autowired的方式注入bean，是因为filter是tomcat管理，bean是spring容器管理，filter先于spring bean初始化，但是为什么在filter的init方法中使用applicationContext.getBean的方式就可以获取了呢，是因为init方法调用的时候，spring容器已经完全初始化了吗？ init方法调用的时机是什么？</div>2019-06-01</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/16/5b/83a35681.jpg" width="30px"><span>Monday</span> 👍（14） 💬（1）<div>老师，tomcat容器的四层架构是一步一步演化过来的还是一步到位的？如果是演化过来的，是哪些故事推动他们如此演化的？谢谢</div>2019-05-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/79/4b/740f91ca.jpg" width="30px"><span>-W.LI-</span> 👍（14） 💬（1）<div>老师好!Tomcat，server.xml还是搞不太清楚。最外层是server，一个server对应一个Tomcat实例，server下面可以由很多service组件，service组件是区分协议和端口号(问题1:域名访问的话请求到达这里是已经被解析成port了吗？如果已经解析了后面为啥还能拿到二级域名)。每个service对应多个连接器和一个engine。(问题2:为啥要设置多个连接器对应一个engine，是为了提高连接器接受请求的并发吗？)。engine下面对应host，host区分域名(问题3:不同的二级域名对应多个host?)，host下面就是context对应应用通过服务名(webapps下文件夹名区分)（问题4：域名相同路径不同指向不同的服务，是在这配置的么?之前运维同事搞过，原理不太理解），wrapper就是应用程序web.xml中配置的servlet。默认只有一个dispatchservlet。支持对url进行ant风格配置多个。</div>2019-05-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/0b/4e/fd946cb2.jpg" width="30px"><span>allean</span> 👍（8） 💬（1）<div>原文：“所有容器都实现了Container接口，因此组合模式可以使得用户对单容器和组合容器的对象使用具有一致性”
问题：这段话不太理解，这里说的一致性是指什么，麻烦老师指明😁
</div>2019-05-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/d3/6e/281b85aa.jpg" width="30px"><span>永光</span> 👍（7） 💬（1）<div>老师你好，你在回答中Pipeline-value这个机制的详细流程是怎样时提到：“在Tomcat启动的时候，这些Valve都已经设置好了。通过addValve方法向Pipeline中添加Valve，最新添加的总是成为’first‘。“
问题：当engine容器下有多个host容器，那engine容器的basic value，在Tomcat启动时是怎么设置Value的？

谢谢
</div>2019-06-05</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/4e/1b/f4b786b9.jpg" width="30px"><span>飞翔</span> 👍（6） 💬（1）<div>老师 现在都用微服务 每个机器上部署一个应用 是不是engine host 就没用了 是吧</div>2019-06-05</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTKb5BzdGZbSYHxq88kicdDtBh0yBtJpDAD81wruIsTsLdBysDZztrm8tYb4mBYvAI1ZE4lorKuvmgw/132" width="30px"><span>java_lunsong</span> 👍（5） 💬（2）<div>老师 你好，按照组合的定义，不同的host其实也可以有相同的context。也就是把appbase配置成全部一样的，也是正确的，对吧？
&lt;server port=“8005” shutdown=“SHUTDOWN”&gt;
&lt;service name=“Catalina”&gt;
&lt;engine defaulthost=“localhost” name=“Catalina”&gt;
&lt;host appbase=“webapps” autodeploy=“true” name=“localhost” unpackwars=“true”&gt;&lt;&#47;host&gt;
&lt;host appbase=“webapps” autodeploy=“true” name=“www.domain1.com” unpackwars=“true”&gt;&lt;&#47;host&gt;
&lt;host appbase=“webapps” autodeploy=“true” name=“www.domain2.com” unpackwars=“true”&gt;&lt;&#47;host&gt;
&lt;host appbase=“webapps” autodeploy=“true” name=“www.domain3.com” unpackwars=“true”&gt;&lt;&#47;host&gt;
&lt;&#47;engine&gt;
&lt;&#47;service&gt;
&lt;&#47;server&gt;</div>2019-07-05</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/68/d5/567bf8ad.jpg" width="30px"><span>非想</span> 👍（5） 💬（1）<div>老师您好，一个server对应的是一个tomcat实例，那service怎么理解呢？它代表的是什么呢？</div>2019-06-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/ea/05/c0d8014d.jpg" width="30px"><span>一道阳光</span> 👍（5） 💬（1）<div>老师，Pipeline中的getBasic方法没用被用到，Host要调用Host的valve，直接调用request.getHost().getPipeline()().getFirst().invoke()方法。</div>2019-06-02</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/0b/4e/fd946cb2.jpg" width="30px"><span>allean</span> 👍（5） 💬（1）<div>收获很多，谢谢老师。有几个问题：
1.Wrapper容器里有且只有一个Servlet，Context里可以有多个Servlet即可以有多个Wrapper，这样理解对吗 ？
2.PepeLine负责维护链式Vavle，具体Vavle负责处理具体请求？</div>2019-05-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/fa/4e/03864cbc.jpg" width="30px"><span>、</span> 👍（4） 💬（1）<div>李老师，不知道还能不能看到我的问题了。我在看完这篇文章，在自己做demo的时候，遇到一个问题。在web.xml中配置如下
 &lt;servlet&gt;
  &lt;servlet-name&gt;servletA&lt;&#47;servlet-name&gt;
  &lt;servlet-class&gt;servlet2.MyServlet&lt;&#47;servlet-class&gt;
  &lt;&#47;servlet&gt;
  &lt;servlet-mapping&gt;
  	&lt;servlet-name&gt;servletA&lt;&#47;servlet-name&gt;
  	&lt;url-pattern&gt;&#47;firstURL&lt;&#47;url-pattern&gt;
  &lt;&#47;servlet-mapping&gt;
    &lt;servlet&gt;
  &lt;servlet-name&gt;servletB&lt;&#47;servlet-name&gt;
  &lt;servlet-class&gt;servlet2.MyServlet&lt;&#47;servlet-class&gt;
  &lt;&#47;servlet&gt;
  &lt;servlet-mapping&gt;
  	&lt;servlet-name&gt;servletB&lt;&#47;servlet-name&gt;
  	&lt;url-pattern&gt;&#47;secondURL&lt;&#47;url-pattern&gt;
  &lt;&#47;servlet-mapping&gt;
同时在servlet2.MyServlet类中的构造方法打印hashcode()方法。

然后在浏览器中输入不同的URL，访问这个servlet，在控制台打印的却是两个hashcode。
疑问如下：
1)  Servlet不是单例的吗？为何还会创建两个servlet对象
2)  多次看这篇文章之后，自己的想法是：在最后一步，Mapper组件根据URL路径找到的servlet，我们肉眼能明显看出来是同一个servlet，但是组件并不识别(可能是没有像ID这样的唯一标识)，所有才导致创建了两个servlet对象。
不知道正确的解释是什么？希望李老师能看到帮我解决一下。万分感谢！！！</div>2019-08-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/3f/2f/8513c4d3.jpg" width="30px"><span>a(๑≖ิټ≖ิ)✌</span> 👍（4） 💬（1）<div>老师请问像tomcat这种开源项目想要像你这样分析它的源代码的话应该从哪读起呢？有时候想看一些开源项目，不知道该怎么入手研究，打开文件目录从A开头的类翻到Z开头的，也不知道该看哪个</div>2019-07-03</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/IgjIXs9jjpODTPaOLrms0XOhJ8pxMcaZgtgBrPG6deqsKXv1sPIqkg0faL6X0rtFicJn5Wf7QXTickjYWpmF0V8A/132" width="30px"><span>Geek_28b75e</span> 👍（4） 💬（1）<div>老师,不同的连接器监听的端口不同，那么tomcat启动时，应该会有多个进程启动吧？我理解的是，外部请求进来，操作系统是根据端口号来找到具体的进程的。</div>2019-06-04</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/07/41/2d477385.jpg" width="30px"><span>柠檬C</span> 👍（4） 💬（1）<div>Tomcat的Context组件应该是对ServletContext的一种实现吧，Spring的ApplicationContext是spring容器，包含于Tomcat的Context组件内</div>2019-05-25</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/d6/64/75f772dc.jpg" width="30px"><span>SlamDunk</span> 👍（4） 💬（1）<div>不知道后面会不会详细讲一下内嵌式tomcat，例如springboot内置的tomcat?</div>2019-05-24</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTKhD6Zib0sPIL1ia8obYgICUCjhE3MKib647IVKibC1Qq7gFp31sagtLJ3OjdicibKw9DZMltG4Lj30icKlg/132" width="30px"><span>Geek_a7fd0f</span> 👍（3） 💬（1）<div>老师您好:
文中提到Tomcat的每个连接器都会监听不同的端口，存在多个Tomcat的多个连接器监听同一个端口或者一个Tomcat的多个连接器监听
同一个端口的情况吗?如8080端口如果存在大量的并发请求的话Tomcat会怎么处理?
文中有提到Engine容器确定后根据请求的域名找到Host容器，请问域名和Host的映射关系是配置在server.xml文件中Host标签上的属性值吗?
另外，例子中将用户管理、商品管理...定义为了一个web应用，请问老师，这里的web应用应该如何理解?也是配置在server.xml中context标签上的值理解为一个web应用吗?
多谢老师!</div>2019-07-03</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/e8/c8/0dc100ad.jpg" width="30px"><span>李白</span> 👍（3） 💬（1）<div>老师我没太理解配置多个host，域名不是会被解析为IP地址吗，连接器只能监听一个IP地址，这里怎么跟容器的host关联起来的？</div>2019-06-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/d3/6e/281b85aa.jpg" width="30px"><span>永光</span> 👍（3） 💬（1）<div>老师你好，
&quot;Tomcat 如何将这个 URL 定位到一个 Servlet
首先，根据协议和端口号选定 Service 和 Engine.&quot;
问题：不是很明白，为什么是根据协议和端口选定Service 和 Engine？我自己理解应该是根据ip+端口来确定Service 和 Engine。
ps：每次看文章都会产生新的疑惑，谢谢老师的耐心回答。


</div>2019-06-05</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/DYAIOgq83eoRiaKX0ulEibbbwM4xhjyMeza0Pyp7KO1mqvfJceiaM6ZNtGpXJibI6P2qHGwBP9GKwOt9LgHicHflBXw/132" width="30px"><span>Geek_ebda96</span> 👍（3） 💬（1）<div>李老师，Pipeline-value这个机制的详细流程是怎样的，比如first这个节点是怎么加入到pipeline的fisrt，什么时候设置pipeline的basic，执行value的invoke之后，还是之前呢？</div>2019-05-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/36/d2/c7357723.jpg" width="30px"><span>发条橙子 。</span> 👍（3） 💬（1）<div>另外老师， 我看到默认的server.xml配置文件里在 &lt;host&gt; 的下面有配 &lt;valve&gt; ， 这个按照老师所讲的， 是不是实际上在 &lt;engine&gt; 或者 &lt;context&gt; 甚至 &lt;wrapper&gt; 里面都可以配置这个 &lt;valve&gt; ， 当作filer来使用，扩展我们的功能点</div>2019-05-26</li><br/>
</ul>