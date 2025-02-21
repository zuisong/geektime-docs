通过前面的学习，相信你对Tomcat的架构已经有所了解，知道了Tomcat都有哪些组件，组件之间是什么样的关系，以及Tomcat是怎么处理一个HTTP请求的。下面我们通过一张简化的类图来回顾一下，从图上你可以看到各种组件的层次关系，图中的虚线表示一个请求在Tomcat中流转的过程。

![](https://static001.geekbang.org/resource/image/12/9b/12ad9ddc3ff73e0aacf2276bcfafae9b.png?wh=1041%2A635)

上面这张图描述了组件之间的静态关系，如果想让一个系统能够对外提供服务，我们需要创建、组装并启动这些组件；在服务停止的时候，我们还需要释放资源，销毁这些组件，因此这是一个动态的过程。也就是说，Tomcat需要动态地管理这些组件的生命周期。

在我们实际的工作中，如果你需要设计一个比较大的系统或者框架时，你同样也需要考虑这几个问题：如何统一管理组件的创建、初始化、启动、停止和销毁？如何做到代码逻辑清晰？如何方便地添加或者删除组件？如何做到组件启动和停止不遗漏、不重复？

今天我们就来解决上面的问题，在这之前，先来看看组件之间的关系。如果你仔细分析过这些组件，可以发现它们具有两层关系。

- 第一层关系是组件有大有小，大组件管理小组件，比如Server管理Service，Service又管理连接器和容器。
- 第二层关系是组件有外有内，外层组件控制内层组件，比如连接器是外层组件，负责对外交流，外层组件调用内层组件完成业务功能。也就是说，**请求的处理过程是由外层组件来驱动的。**
<div><strong>精选留言（30）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/12/93/ee/101f0356.jpg" width="30px"><span>一路远行</span> 👍（104） 💬（2）<div>ContainerBase提供了针对Container接口的通用实现，所以最重要的职责包含两个:
1) 维护容器通用的状态数据
2) 提供管理状态数据的通用方法

容器的关键状态信息和方法有:
1) 父容器, 子容器列表
getParent, setParent, getParentClassLoader, setParentClassLoader;
getStartChildren, setStartChildren, addChild, findChild, findChildren, removeChild.

2) 容器事件和属性监听者列表
findContainerListeners, addContainerListener, removeContainerListener, fireContainerEvent;
addPropertyChangeListener, removePropertyChangeListener.

3) 当前容器对应的pipeline
getPipeline, addValve.

除了以上三类状态数据和对应的接口，ContainerBase还提供了两类通用功能:
1) 容器的生命周期实现，从LifecycleBase继承而来，完成状态数据的初始化和销毁
startInternal, stopInternal, destroyInternal

2) 后台任务线程管理，比如容器周期性reload任务
threadStart, threadStop，backgroundProcess.

想了解更多技术细节，可以参考源码org.apache.catalina.core.ContainerBase，有源码有真相。</div>2019-05-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/0b/4e/fd946cb2.jpg" width="30px"><span>allean</span> 👍（51） 💬（5）<div>原理理解之后特别想看看源码是怎么写的，不看源码总感觉不踏实🤣，老师在介绍组件原理之后可不可以指明怎么启动Tomcat源码，并debug啊，多谢</div>2019-05-25</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/74/c9/d3439ca4.jpg" width="30px"><span>why</span> 👍（20） 💬（1）<div>- 系统启动时会创建，组装，启动组件，服务停止时释放资源销毁组件。
- 组件间由两层关系
    - 组件有大有小, 大组件管理小组件( Server 管 Service )
    - 组件有内有外, 外层控制内层( 连接器控制容器 )
- 关系决定创建应有的顺序
    - 先创建子组件, 再创建父组件, 子组件注入父组件
    - 先创建内层组件, 再创建外层, 内层注入外层组件
- 以上方法存在的问题: 代码混乱&#47;组件遗漏&#47;不利扩展
- 解决方法: 通用, 统一的组件管理
- LifeCycle 接口 ( 通用性 → 组合模式 )
    - 不变: 组件创建, 初始化, 启动等状态
    - 变化: 具体启动方法
    - 将不变抽象为接口 LifeCycle, 包括四个方法 init start stop destroy; 以下为组合模式:
        - 父组件 init 方法创建子组件并调用其 init 方法
        - 父组件 start 调用 子组件 start 方法
        - 只要调用最顶层 init start 就可以启动应用
- LifeCycle 事件 ( 扩展性 → 观察者模式 )
    - 系统可扩展性, 应遵循开闭原则: 不能修改已有的类, 可以定义新的类
    - 上层 init 等方法触发下层 init 等方法, 把状态当做事件, 事件有对应Listener; Listener可方便添加和删除, 此为观察者模式
    - 在 LifeCycle 中加入两个方法: 添加&#47;删除Listener, 并用 Enum 定义状态及其对应触发事件
- LifeCycleBase 抽象基类 ( 重用性 → 模板设计模式 )
    - 接口实现类有一些相同的逻辑, 定义一个基类实现共同的逻辑
    - 基类会定义一些抽象方法, 调用这些方法实现子类逻辑
    - LifeCycleBase 实现 LifeCycle 接口, 实现通用逻辑: 状态转变&#47;维护, 事件触发, 监控器添加&#47;删除, 调用子类逻辑
    - LifeCycleBase 抽象基类抽象方法改名, initInternal 等, 避免与 init 重名; initInternal 会调用子组件的 init 方法
- Listener注册, 分为两种情况
    - Tomcat 自定义的Listener, 父组件创建子组件是注册到子组件中
    - 可在 server.xml 中定义自己的Listener, 由 Tomcat 解析, 创建Listener并注册到组件中
- 容器类生命周期管理接口与功能接口分开 → 接口分离原则</div>2019-05-30</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/6LaITPQ4Lk5fZn8ib1tfsPW8vI9icTuSwAddiajVfibPDiaDvMU2br6ZT7K0LWCKibSQuicT7sIEVmY4K7ibXY0T7UQEiag/132" width="30px"><span>尔东橙</span> 👍（16） 💬（2）<div>老师，会不会考虑出一门课：深入拆解spring?我特别想听老师讲Spring架构的的设计，和里面用到的设计模式</div>2019-06-02</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/e9/0b/1171ac71.jpg" width="30px"><span>WL</span> 👍（15） 💬（2）<div>请问一下老师Tomcat为什么要在LifeCycleBase中定义一系列的***internal()让子类取调用,  为什么不是子类实现接口的init()方法呢, 这一点我不是很理解, 希望老师指点一下.</div>2019-05-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/e5/84/4a01e18d.jpg" width="30px"><span>nsn_huang</span> 👍（11） 💬（1）<div>这是Tomcat8.5版本的源码，基于Maven和IDEA，希望大家一起学习，一起进步。https:&#47;&#47;blog.csdn.net&#47;sougou_1323&#47;article&#47;details&#47;90597079</div>2019-05-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/16/5b/83a35681.jpg" width="30px"><span>Monday</span> 👍（10） 💬（2）<div>思考题
1，容器的创建&#47;初始化&#47;销毁
2，容器添加&#47;删除子容器
3，如果还要监听容器状态变化的话还需要有添加&#47;移除事件的方法。
请指正。

本节收获，干货干货。
多种设计模式还带Tomcat设计的应用场景，面试设计模式绝对加分项（我还没消化）

问题：进入架构篇，就处于下面这种学习状态。
1，觉得老师讲得很有道理
2，被动的吸收着知识点，没有自己的思路
3，一看文档就感觉自己似乎是懂了，因为提不出好问题，一合上文档就感觉本节我没来过
老师有没有好的建议，谢谢！</div>2019-05-25</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/4e/1b/f4b786b9.jpg" width="30px"><span>飞翔</span> 👍（8） 💬（1）<div>老师 我从 tomcat class 里边的main方法找，跟踪到 catalina里边的load方法，在这个方法里边有digester.parse(inputSource);  我觉得这个应该是具体读serverxml的，但是在往下跟踪始终找不到哪里读server.xml 实例化server等，求指导</div>2019-07-15</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/79/4b/740f91ca.jpg" width="30px"><span>-W.LI-</span> 👍（8） 💬（1）<div>老师好!之前设计模式看过好几遍，总感觉用不上，虽然知道是自己对设计思想的理解不够深入导致的。又苦于找不到方法，看了老师的分析对设计模式，和设计原则又有了进一步的了解。问题1:对于变于不变的界定标准，哪些方法需要抽象为接口。老师有啥好的建议么。问题2:spring的event，发布一个事件时会把事件放入map.然后轮训所有的所有的观察者。观察者和event很多的时候，内存等开销，会成为性能瓶颈么?比如处理事件的逻辑比较复杂或者需要IO操作。会有处理速度跟不上事件发生的速度这样的情况导致OOM的么?</div>2019-05-25</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/DYAIOgq83eoRiaKX0ulEibbbwM4xhjyMeza0Pyp7KO1mqvfJceiaM6ZNtGpXJibI6P2qHGwBP9GKwOt9LgHicHflBXw/132" width="30px"><span>Geek_ebda96</span> 👍（7） 💬（1）<div>老师，你的意思是配置在server.xml里的connector的线程池是tomcat对于一个应用的全局线程池，用于接受请求的socketprocessor会放到这个线程池里，假如这个应用里面有后台一些定时job或或其他需要异步线程处理的业务，也会从这个大的线程池里取线程处理，不会再单独做新建线程？</div>2019-06-06</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/63/c5/a85ade71.jpg" width="30px"><span>刘冬</span> 👍（7） 💬（2）<div>强烈呼吁老师能够讲解一下，怎么启动Tomcat的源码、调试。怎么读源码。
另外，有些Interface的实现是在单独的Jar中，用Intellij无法直接看到Implementation，请问有什么好的办法看到这部分的源码吗？</div>2019-05-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/5d/91/a9365c01.jpg" width="30px"><span>锟铻</span> 👍（6） 💬（1）<div>弱弱的问题问题，
上面有提到：
如果想让一个系统能够对外提供服务，我们需要创建、组装并启动这些组件；在服务停止的时候，我们还需要释放资源，销毁这些组件
服务已经停止了，进程以及不在了，为什么还需要释放资源，销毁这些组件，不释放资源，不销毁这些组件，有什么影响？</div>2019-06-21</li><br/><li><img src="" width="30px"><span>dingdongfm</span> 👍（6） 💬（1）<div>请问tomcat什么时候会reload?</div>2019-06-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/7b/57/a9b04544.jpg" width="30px"><span>QQ怪</span> 👍（4） 💬（1）<div>还好订阅老师专栏之前看完大话设计模式，正好根据tomcat原理来体会设计模式的精髓，不然都会看不懂啊，哈哈哈</div>2019-05-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/76/23/31e5e984.jpg" width="30px"><span>空知</span> 👍（4） 💬（1）<div>老师，请教下 
两层关系决定了 组件由内到外 有小到大的加载顺序，这个地方为啥不是先外再内 先大再小，上层加载好了之后根据配置去加载子(内)组件？</div>2019-05-25</li><br/><li><img src="https://wx.qlogo.cn/mmopen/vi_32/DYAIOgq83eqLcWH3mSPmhjrs1aGL4b3TqI7xDqWWibM4nYFrRlp0z7FNSWaJz0mqovrgIA7ibmrPt8zRScSfRaqQ/132" width="30px"><span>易儿易</span> 👍（3） 💬（3）<div>李老师，扣一个小细节，为什么在描述LifeCycleBase 与LifeCycleState关系时类图使用“依赖”而不是“关联”呢？</div>2019-06-30</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/4e/1b/f4b786b9.jpg" width="30px"><span>飞翔</span> 👍（2） 💬（1）<div>老师 求教  为啥呀用lifcycle呀，还是不是很理解。每次 例如 standardserver调用init还是都到lifecyclebase中的init中去，然后在调用standardserver的initinternal函数， 在这个函数里调用standardservice.init() 为啥不在standardserver.init 里边调用standardservice.init() ，在在里边调用connect.init 这样不更简单嘛</div>2019-08-16</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/e9/0b/1171ac71.jpg" width="30px"><span>WL</span> 👍（2） 💬（1）<div>请问一下老师我看LifecycleMBeanBase中的initInternal()方法想问下这个方法里面的Registry是起到什么作用, 我不太理解?</div>2019-05-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/ee/6c/246fa0d1.jpg" width="30px"><span>Mr.差不多</span> 👍（2） 💬（1）<div>您好，老师，我想问一下Tomcat是如何通过start.sh 来启动项目的，换句话说就是怎么找到了Bootstrop.java类进行启动的。</div>2019-05-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/ee/67/d6d9499e.jpg" width="30px"><span>木木木</span> 👍（0） 💬（1）<div>目前找到的debug资料都是tomcat8的，老师提供的例子也是tomcat8的，有没有基于新代码的呢，目前也是github上拉了最新的代码，试着构建了下。一个是debug tomcat本身，还有就是部署的应用的，两个应用不一样的吧。</div>2019-06-02</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/d2/ac/aeb9f156.jpg" width="30px"><span>吖蒲</span> 👍（0） 💬（1）<div>Tomcat生命周期的三种设计模式运用
①.基于LifeCycleBase抽象骨架类实现的子类，使用组合模式管理起来，只需要调用一个顶层组件，即可对所有子类进行管理。
②.使用观察者模式可跟踪顶层组件的状态改变，通知子类更新生命周期的状态。
③.继承LifecycleBase的子类实现的initInternal()、startInternal()等方法，根据步骤②获取的状态，以模板方法模式执行顺序分别在LifecycleBase类中的init、start、stop和destroy方法中执行。
期待老师下一章节，每节课我都能学到很多。</div>2019-05-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/1f/48/4bf434ef.jpg" width="30px"><span>非洲铜</span> 👍（0） 💬（2）<div>为了避免跟基类中的方法同名，我们把具体子类的实现方法改个名字，在后面加上 Internal，叫 initInternal()、startInternal() 等。
李老师，感觉这段话有点问题，是基类为了避免接口重名才这样命名的。</div>2019-05-25</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/46/85/0a5f1b5b.jpg" width="30px"><span>yi_jun</span> 👍（33） 💬（3）<div>看了这篇文章对tomcat中用到的设计模式又有了新的理解. 
看到评论里有问tomcat启动的同学, 和大家分享一篇介绍Tomcat启动的文章, 从startup.bat的源码开始分析的.
https:&#47;&#47;www.cnblogs.com&#47;tanshaoshenghao&#47;p&#47;10932306.html</div>2019-05-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/63/c5/a85ade71.jpg" width="30px"><span>刘冬</span> 👍（5） 💬（2）<div>老师太拼了，周末凌晨发新的课程。太感动了😹 </div>2019-05-25</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/d5/3e/7f3a9c2b.jpg" width="30px"><span>Jaising</span> 👍（1） 💬（0）<div>总体类图少了一个关系：Container也继承了Lifecycle</div>2021-05-25</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/66/e9/814d057a.jpg" width="30px"><span>小陈</span> 👍（1） 💬（0）<div>讲的真好</div>2020-03-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/53/e3/39dcfb11.jpg" width="30px"><span>来碗绿豆汤</span> 👍（1） 💬（0）<div>老师啥时候出一个spring的课程啊，好喜欢你的讲课风格</div>2019-10-03</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/4e/1b/f4b786b9.jpg" width="30px"><span>飞翔</span> 👍（1） 💬（0）<div>老师 读完 init start 之后发现 除了catalina里边init的时候调用digester 创造了几乎所有的实例和他们之间的关系和属性， 别的部分 比如connect还有host engineer的init和start基本上就没做啥重要的事情 感觉

老师要是能讲解下digester 创建对象和关系 就更完整了。</div>2019-08-15</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/8f/d5/bab4332a.jpg" width="30px"><span>K.Zhou</span> 👍（1） 💬（0）<div>这篇干货十足，几种设计模式的经典实际运用！</div>2019-05-25</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/pVYBnckSuRLhnYsSUiaibLS1xs2PlciaQoOQCyic83OSibksmWm4HKB0OQWCo2ChBl7bCiaaia7IMdtOH4Pq3GZ2AUglw/132" width="30px"><span>HHH90</span> 👍（0） 💬（0）<div>老师，可以详细说下omcat生命周期中的destroy吗，他的意义是什么呢？优雅停机是怎么做到接收到shutdown信号的时候，一个个卸载组件，只完成接收的请求，不在接收新请求了呢？类似的优雅停机代码要怎么组织其卸载先后顺序的代码结构？</div>2022-09-15</li><br/>
</ul>