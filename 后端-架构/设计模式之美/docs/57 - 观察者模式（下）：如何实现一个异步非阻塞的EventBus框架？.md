上一节课中，我们学习了观察者模式的原理、实现、应用场景，重点介绍了不同应用场景下，几种不同的实现方式，包括：同步阻塞、异步非阻塞、进程内、进程间的实现方式。

同步阻塞是最经典的实现方式，主要是为了代码解耦；异步非阻塞除了能实现代码解耦之外，还能提高代码的执行效率；进程间的观察者模式解耦更加彻底，一般是基于消息队列来实现，用来实现不同进程间的被观察者和观察者之间的交互。

今天，我们聚焦于异步非阻塞的观察者模式，带你实现一个类似Google Guava EventBus的通用框架。等你学完本节课之后，你会发现，实现一个框架也并非一件难事。

话不多说，让我们正式开始今天的学习吧！

## 异步非阻塞观察者模式的简易实现

上一节课中，我们讲到，对于异步非阻塞观察者模式，如果只是实现一个简易版本，不考虑任何通用性、复用性，实际上是非常容易的。

我们有两种实现方式。其中一种是：在每个handleRegSuccess()函数中创建一个新的线程执行代码逻辑；另一种是：在UserController的register()函数中使用线程池来执行每个观察者的handleRegSuccess()函数。两种实现方式的具体代码如下所示：
<div><strong>精选留言（30）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/13/76/66/cbd6013c.jpg" width="30px"><span>Lambor</span> 👍（2） 💬（1）<div>使用异步非阻塞观察者模式，事务怎么控制呢？毕竟最后都是扔到线程池里执行。</div>2020-04-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/07/8c/0d886dcc.jpg" width="30px"><span>蚂蚁内推+v</span> 👍（0） 💬（1）<div>老师，例子跑不通，应该把long 类型参数改为封装类型Long ,不然找不到对应的订阅者</div>2020-04-15</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/49/a5/e4c1c2d4.jpg" width="30px"><span>小文同学</span> 👍（220） 💬（1）<div>Guava EventBus 对我来说简直是一份大礼。里面解耦功能使本来的旧项目又不可维护逐渐转化为可维护。

EventBus作为一个总线，还考虑了递归传送事件的问题，可以选择广度优先传播和深度优先传播，遇到事件死循环的时候还会报错。Guava的项目对这个模块的封装非常值得我们去阅读，复杂的都在里头，外面极为易用，我拷贝了一份EventBus的代码进行修改以适配自己的项目，发觉里面的构造都极为精密巧妙，像一个机械钟表一样，自己都下不了手，觉得不小心就是弄坏了。

跟随真正优秀的工程师，并阅读其写出来的代码让人受益匪浅。</div>2020-03-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/62/bb/323a3133.jpg" width="30px"><span>下雨天</span> 👍（84） 💬（4）<div>课后题：
代理模式，使用一个代理类专门来处理EventBus相关逻辑。作用：
1.将业务与非业务逻辑分离
2.后续替换EventBus实现方式直接改写代理类，满足拓展需求</div>2020-03-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/17/86/25/25ded6c3.jpg" width="30px"><span>zhengyu.nie</span> 👍（72） 💬（2）<div>一开始在携程工作的时候因为早期Spring Event驱动强制要求事件继承抽象事件，而转到Guava EventBus，在Event实体上更加灵活。后面来阿里后发现一些项目里，Spring新版本也可以支持非继承的事件类型了，也有很多MetaQ消息直接分发到内存Event的写法。

关于EventBus源码也看了几遍了，总体来说提供了几种dispatcher，有广度和深度优先原则，像PerThread中两层while也有对嵌套事件的处理，像Google工程师致敬。

EventBus现在来对我个人说主要有以下几点可能存在的问题：
1.在比较高需求的场景上，Event持久化机制也是需要的，不管是为了高可用（内存队列宕机就丢），做成最终一致性软事务，或者是CQRS中事件溯源等需求。

2.现在的异步处理，是直接丢在同一个线程池处理，那么存在忙死的event导致event饿死的情况，所以这一块会有很大局限性，对比akka之类的话。

3.现在的Event在没打的@AllowConcurrentEvents时候，也就是需要线程安全的时候，是invoke method过程是加了synchronized关键字控制的，那么最好方法粒度不要太大，性能上考虑的话。

其实现在也蛮纠结的，到底用EventBus还是Spring Event，按道理讲，现在项目基本都是SpringBoot体系，那么其实Spring事件隔绝依赖更多，也更容易和Spring Async等集成，所以我现在基本是用Spring事件驱动替代EventBus。</div>2020-04-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/0b/32/c2eff01b.jpg" width="30px"><span>鱼Shiyao</span> 👍（48） 💬（9）<div>把老师的EventBus的代码实现了一下，发现有两个地方有问题。
1：
XMsg xMsg = new XMsg();
YMsg yMsg = new YMsg();
如果XMsg是YMsg的父类的话，应该是
post(xMsg); =&gt; AObserver接收到消息
post(yMsg); =&gt; AObserver,BObserver接收到消息
2. 和刚才的问题一样，对应着ObserverRegistry的代码。
在getMatchedObserverAction函数中
if (postedEventType.isAssignableFrom(eventType)) 
应该改成
if (eventType.isAssignableFrom(postedEventType)) </div>2020-03-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/50/d7/f82ed283.jpg" width="30px"><span>辣么大</span> 👍（12） 💬（4）<div>重构使用代理模式，将非业务代码放到代理类中。
另外试了争哥讲的EventBut类，在定义观察者的入参要修改成*Long*类型，如果使用long，这个方法是无法注册的，代码执行收不到通知。应该是ObserverRegistry类需要完善一下。
  @Subscribe
  public void handleRegSuccess(Long userId) {
    System.out.println(&quot;handleRegSuccess...&quot;);
    promotionService.issueNewUserExperienceCash(userId);
  }
代码见：https:&#47;&#47;github.com&#47;gdhucoder&#47;Algorithms4&#47;tree&#47;master&#47;designpattern&#47;u57</div>2020-03-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/47/31/f35367c8.jpg" width="30px"><span>小晏子</span> 👍（9） 💬（1）<div>我的想法比较直接，将UserController中的业务代码提出来放在接口的实现类中，这个UserController可以改名为EventController，然后这个接口实现类注入到这个EventController中，这样业务逻辑和控制逻辑就分离了，示例如下：
interface iController {
    object register()
}

public class UserControllerService implement iController {
    private string telphone;
    private string password;

    public Long register() {
        long userId = userService.register(telephone, password);
        return userId;
  }
}

public class EventController {
    private iController iService;

    private EventBus eventBus;
    private static final int DEFAULT_EVENTBUS_THREAD_POOL_SIZE = 20; 

    public EventController() {
        eventBus = new AsyncEventBus(Executors.newFixedThreadPool(DEFAULT_EVENTBUS_THREAD_POOL_SIZE)); &#47;&#47; 异步非阻塞模式 
    }

    public void setRegObservers(List&lt;Object&gt; observers) {
        for (Object observer : observers) {
            eventBus.register(observer);
        }
    }

    public void SendMessage() {
        object msg = iService.register()
        eventBus.post(msg)
    }

}</div>2020-03-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/c2/2e/c4a527d9.jpg" width="30px"><span>blacknhole</span> 👍（7） 💬（2）<div>提个问题：

文中“所谓可匹配指的是，能接收的消息类型是发送消息（post 函数定义中的 event）类型的子类”这话似乎有问题，应该是父类吧？</div>2020-03-15</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/19/d9/ff/b23018a6.jpg" width="30px"><span>Heaven</span> 👍（7） 💬（1）<div>对于这个问题,在UserCntroller中,我们应该只保留post函数() 发送的相关逻辑,而将注册Observer,初始化EventBus相关逻辑剔除,如果非要使用EventBus来实现的话,我们需要有人帮我们去进行注册和初始化,这时候就可以立马想到之前讲的工厂模式的DI框架,我们可以让所有观察者都被DI框架所管理,并且对EventBus创建一个装饰器类,在这个装饰器类中,由开发者选择注入线程池实现异步发送还是直接使用同步发送的,并且在init函数中 从DI框架管理的对象池中拿出所有标有@Subscribe注解的类,保存到ObserverRegistry中,对于所有需要使用EventBus的类,注入这个装饰器类即可,设计的好,甚至可以做到其他依赖代码都不用改一点</div>2020-03-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/fe/36/df26de4a.jpg" width="30px"><span>依然亦晨</span> 👍（5） 💬（0）<div>debug的时候发现一个小问题，ObserverRegistry类的getMatchedObserverActions()方法中调用了isAssignableFrom()方法，由于postedEventType是java.lang.Long，而eventType是long，导致postedEventType.isAssignableFrom(eventType)始终为false，因而无法获取到匹配的观察者。从网上查阅相关资料的得知，Java反射获取方法不支持自动装箱或拆箱；</div>2020-04-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/98/3b/5af90c80.jpg" width="30px"><span>右耳听海</span> 👍（5） 💬（0）<div>给老师点赞，虽然很早就接触了eventbus，但一直没明白这个的设计思想，现在有种醍醐灌顶的感觉</div>2020-03-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1c/d2/0d/f10048ce.jpg" width="30px"><span>Mogeko</span> 👍（4） 💬（1）<div>ObserverRegistry类的getMatchedObserverActions方法，postedEventType.isAssignableFrom(eventType)是不是反了？
不是应该eventType.isAssignableFrom(postedEventType)吗？</div>2020-03-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/48/f3/65c7e3ef.jpg" width="30px"><span>cricket1981</span> 👍（4） 💬（0）<div>public void handleRegSuccess(long userId) 方法签名中的long类型应该改成Long类型，不然SubscriberRegistry.getSubscribers(Object event)会匹配不上类型</div>2020-03-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/4e/60/0d5aa340.jpg" width="30px"><span>gogo</span> 👍（4） 💬（0）<div>看了下google EventBus源码，是标注了@Beta的，能用于生产环境吗？</div>2020-03-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1e/40/f7/e62bbc62.jpg" width="30px"><span>zh</span> 👍（3） 💬（1）<div>作为cpp选手，这节有点不太友好了，反射语法、注解都不太懂...前面的讲得很好，特别是设计原则与思想部分，但后面涉及的一些技术点用C++翻译还是比较吃力啊，比如IOC、反射、动态代理...</div>2021-02-04</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/9a/e6/e8439f9a.jpg" width="30px"><span>ttxser</span> 👍（3） 💬（0）<div>异步+注解的，后期比较难维护吧，运行时生效，没有办法看到全局的注册信息</div>2020-04-15</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/49/a5/e4c1c2d4.jpg" width="30px"><span>小文同学</span> 👍（3） 💬（0）<div>感谢大家点赞，收到了37个赞，今天重新读了一下 EventBus 的源码，发现这个留言存在问题。&quot;遇到事件死循环的时候还会报错。&quot; Event Bus 是允许循环提交事件的，假如采用深度优先，则会导致线程栈溢出报错，假如使用广度优先，则会导致死循环。

前面误解了，递归报错是源自于 LoadingCache 在执行加载缓存A的时候，方法栈一直又重复递归加载A，则会导致报错：
java.lang.IllegalStateException: Recursive load of: 1000020000000066
 at com.google.common.base.Preconditions.checkState(Preconditions.java:197)
at com.google.common.cache.LocalCache$Segment.waitForLoadingValue(LocalCache.java:2299)

因为我使用的EventBus 去驱动 LoadingCache 加载缓存的，所以误以为是 EventBus 报的错。

另外我自己针对 EventBus 做了一次比较具体的源码分析，并且使用了王争老师设计模式专栏中P15-22讲的设计模式思想对 EventBus 代码进行了分析，这里分享给大家，同时为我没经考据的留言表示歉意：
https:&#47;&#47;juejin.im&#47;post&#47;5e925c75f265da47b844fd83</div>2020-04-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/a4/b7/e0d88365.jpg" width="30px"><span>佐西玛</span> 👍（3） 💬（2）<div>争哥，在EventBus 框架功能需求介绍里面，如果XMsg 是 YMsg 的父类，则post(xMsg); =&gt; AObserver、BObserver接收到消息，这个地方应该是如果XMsg 是 YMsg 的子类。</div>2020-03-14</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTJKj3GbvevFibxwJibTqm16NaE8MXibwDUlnt5tt73KF9WS2uypha2m1Myxic6Q47Zaj2DZOwia3AgicO7Q/132" width="30px"><span>饭</span> 👍（3） 💬（5）<div>老师，我们主要做物流方面的业务系统，类似仓储，港口这样的，流程繁杂。平时主要就是写增删改查，然后通过一个状态字段变化控制流程，所有业务代码流程中每一步操作都写满了各种状态验证，判断。后期稍微需求变动一点点，涉及到状态改动，要调整流程的话，都是一场灾难。针对我们这种系统，有办法将流程状态解耦出来吗？今天看到这篇事件总线的文章，好像看到希望，但是没想清具体怎么操作。不知道老师怎么看</div>2020-03-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1a/86/56/509535da.jpg" width="30px"><span>守拙</span> 👍（3） 💬（0）<div>课堂讨论: 

在今天内容的第二个模块“EventBus 框架功能需求介绍”中，我们用 Guava EventBus 重新实现了 UserController，实际上，代码还是不够解耦。UserController 还是耦合了很多跟观察者模式相关的非业务代码，比如创建线程池、注册 Observer。为了让 UserController 更加聚焦在业务功能上，你有什么重构的建议吗？



使用EventBus后, setRegObservers()方法无需在UserController中调用了, 每个Observer的构造器中EventBus.register(this)就可以了. EventBus的意义就在于将Observable与Observer彻底解耦.



EventBus作为系统中唯一的组件, 可以设计成单例模式. Observable可以直接通过EventBus.getDefault().post(XXEvent())的方式使用, Observable无需依赖注入.



线程池的创建可以使用Builder模式为EventBus配置. 在Application进程初始化时, 即配置EventBus的线程池. 如此Observable就可以无需考虑线程池的配置.


EventBus可以提供unregister()以便observer生命周期管理.</div>2020-03-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/1e/f2/453d5f88.jpg" width="30px"><span>seker</span> 👍（2） 💬（0）<div>class1.isAssignableFrom(class2)
从class1的角度看，是判断class1是否为class2的父类。从class2的角度看，是判断class2是否为class1的子类。
  
所谓可匹配指的是，能接收的消息类型是发送消息（post 函数定义中的 event）类型的父类。
  
public List&lt;ObserverAction&gt; getMatchedObserverActions(Object event)
入参event是method方法的参数，通过Class&lt;?&gt; postedEventType = event.getClass()可以拿到入参的类型，而这个类型就是发送消息的类型。
能接收的消息类型通过Class&lt;?&gt; eventType = entry.getKey()拿到。
  
综上所述，是要判断postedEventType是否为eventType的子类，或者说是要判断eventType是否为postedEventType的父类。
故代码应该写成eventType.isAssignableFrom(postedEventType)</div>2020-10-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/17/0c/5f/4cbcbfb9.jpg" width="30px"><span>hello</span> 👍（2） 💬（0）<div>看不懂java的我，用c++模仿文中的内容实现了一个c++版本的EventBus：
https:&#47;&#47;github.com&#47;chenhongjun&#47;event?files=1&amp;from=timeline
支持多类型msg，支持同步和异步，使用线程池</div>2020-06-14</li><br/><li><img src="" width="30px"><span>Geek_76616d</span> 👍（2） 💬（2）<div>对Guava EventBus相见恨晚啊</div>2020-03-16</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/19/89/20488013.jpg" width="30px"><span>hanazawakana</span> 👍（2） 💬（0）<div>单独用一个工具类来处理eventbus相关的注册和post操作。然后通过依赖注入传给usercontroller</div>2020-03-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/64/9b/d1ab239e.jpg" width="30px"><span>J.Smile</span> 👍（2） 💬（4）<div>在例子中当eventbus调用post传递的参数中是long userId,而两个observer被subcriber注解的方法参数都一样，此时这两个方法都会被调用到吗？</div>2020-03-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/37/3f/a9127a73.jpg" width="30px"><span>KK</span> 👍（1） 💬（1）<div>这是一节 java 课。</div>2022-05-08</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/N6yjnrLnMW4XVSkBr3f0N3F962l35b5j0kib9VSlAqqbf6iaoCPicL1WnJ9KjgT4egQ7A2G0Zx3OayaK4yuoZrUVA/132" width="30px"><span>worthto</span> 👍（1） 💬（0）<div>为何要使用@Subscribe所注解的方法的参数作为事件类型，Guava也是这样做的吗？
个人觉得这样做有几个问题，1、这种约定有点不平易近人；2、这样做限定了@Subscribe方法的参数的个数；3、如果同一个Observer里面有多个@Subscribe方法的参数相同，但是他们所需要关注的事件不同，这样做就必须在@Subscribe方法内部去做逻辑判断了。4、是否可以设计成这样，在@Subscribe注解内部设定事件类型，而不直接通过@Subscribe方法的参数判定事件类型。</div>2020-05-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/8a/02/828938c9.jpg" width="30px"><span>Frank</span> 👍（1） 💬（0）<div>为了让 UserController 更加聚焦在业务功能上，我的想法是将耦合的EventBus代码抽取出来形成一个单独的服务类，通过注入的方式注入到UserController类中使用。这样使其两者的职责单一，而新抽取出来的服务类可被其他业务场景复用。
今天也加深了对Guava Eventbus的认识，虽然之前专栏也介绍过这个类库的使用。结合Jdk提供的java.util.Observable&amp;Observer观察者模式API，与EventBus进行比对，如果要实现进程内的观察者使用EventBus最为方便。从JDK9之后，java.util.Observable&amp;Observer已被标记为废弃，建议使用Java Beans规范中的事件模式和java.util.concurrent.Flow API。</div>2020-03-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/e5/69/719ec5d0.jpg" width="30px"><span>Jian</span> 👍（1） 💬（0）<div> 最近公司做了个业务系统架构重构，套用了其它公司的业务架构，架构与业务耦合的太紧，做起来非常痛苦，越来越觉得跟争哥写的专栏相违背。</div>2020-03-14</li><br/>
</ul>