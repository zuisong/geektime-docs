使用过Tomcat的同学都知道，我们可以通过Tomcat的`/bin`目录下的脚本`startup.sh`来启动Tomcat，那你是否知道我们执行了这个脚本后发生了什么呢？你可以通过下面这张流程图来了解一下。

![](https://static001.geekbang.org/resource/image/57/4d/578edfe9c06856324084ee193243694d.png?wh=994%2A346)

1.Tomcat本质上是一个Java程序，因此`startup.sh`脚本会启动一个JVM来运行Tomcat的启动类Bootstrap。

2.Bootstrap的主要任务是初始化Tomcat的类加载器，并且创建Catalina。关于Tomcat为什么需要自己的类加载器，我会在专栏后面详细介绍。

3.Catalina是一个启动类，它通过解析`server.xml`、创建相应的组件，并调用Server的start方法。

4.Server组件的职责就是管理Service组件，它会负责调用Service的start方法。

5.Service组件的职责就是管理连接器和顶层容器Engine，因此它会调用连接器和Engine的start方法。

这样Tomcat的启动就算完成了。下面我来详细介绍一下上面这个启动过程中提到的几个非常关键的启动类和组件。

你可以把Bootstrap看作是上帝，它初始化了类加载器，也就是创造万物的工具。
<div><strong>精选留言（30）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/0f/8c/f7/a4de6f64.jpg" width="30px"><span>大卫</span> 👍（37） 💬（2）<div>老师好，tomcat一般生产环境线程数大小建议怎么设置呢</div>2019-06-05</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/DYAIOgq83eoRiaKX0ulEibbbwM4xhjyMeza0Pyp7KO1mqvfJceiaM6ZNtGpXJibI6P2qHGwBP9GKwOt9LgHicHflBXw/132" width="30px"><span>Geek_ebda96</span> 👍（34） 💬（5）<div>老师最近遇到一个问题，刚到新公司，看他们把一个tomact的connector的线程池设置成800，这个太夸张了吧，connector的线程池只是用来处理接收的http请求，线程池不会用来处理其他业务本身的事情，设置再大也只能提高请求的并发，并不能提高系统的响应，让这个线程池干其他的事情，而且线程数太高，线程上下文切换时间也高，反而会降低系统的响应速度吧？我理解是不是对的，老师？还有一个问题就是设置的connector线程数，是tomcat启动的时候就会初始化这么多固定的线程还是这只是一个上限，还有就是如果线程处于空闲状态，会不会进行上下文切换呢？</div>2019-06-05</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/64/86/f5a9403a.jpg" width="30px"><span>yang</span> 👍（21） 💬（2）<div>老师，我看的慢。  

一个子容器只有一个父容器， 如 a的父容器是容器b；
那此时，只有父容器会调用子容器的start()方法吧？
如果用synchronized同步互斥的方法保护调用子容器的start()方法，会不会有些多余？</div>2019-06-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/be/a4/5051fec4.jpg" width="30px"><span>识度℃</span> 👍（20） 💬（2）<div>有个常见问题请教一下，在实际应用场景中，tomcat在shutdown的时候，无法杀死java进程，还得kill，这是为何呢？</div>2019-05-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/0b/4e/fd946cb2.jpg" width="30px"><span>allean</span> 👍（20） 💬（1）<div>如果映射关系不变，而是某个具体的Servlet的方法处理逻辑变了，热部署也可以解决重启tomcat的尴尬吗</div>2019-05-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/f7/ee/6eeb58a3.jpg" width="30px"><span>calljson</span> 👍（18） 💬（1）<div>热部署和热加载原理帮忙讲解下，还有强制停止比如杀进程等，怎么通过钩子处理的？</div>2019-05-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/ea/05/c0d8014d.jpg" width="30px"><span>一道阳光</span> 👍（9） 💬（1）<div>老师，1.catalina创建组件，是把所有的对象都new出来了吧，只是各个组件之间没有相互注入吧。
2.为什么catalina直接调用server的start方法？不是先init吗？
3.容器之间是什么时候注入进去的？还有listener是什么时候注入到组件中去的？</div>2019-06-04</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/fd/82/b048d00b.jpg" width="30px"><span>wwm</span> 👍（9） 💬（1）<div>老师，请教一个问题：
在Bootstrap中，基于什么原因用反射的方式创建Catalina实例，之后继续基于反射方式调用load、init、start这些方法？为什么不是直接new Catalina实例后通过实例直接调用这些方法？</div>2019-05-28</li><br/><li><img src="https://wx.qlogo.cn/mmopen/vi_32/DYAIOgq83eqLcWH3mSPmhjrs1aGL4b3TqI7xDqWWibM4nYFrRlp0z7FNSWaJz0mqovrgIA7ibmrPt8zRScSfRaqQ/132" width="30px"><span>易儿易</span> 👍（7） 💬（1）<div>李老师，您在给Geek_ebda96同学回复问题的时候指出“Connector中的线程池就是用来处理业务的”，这个业务指的是什么呢？从第05节讲ProtocolHandler组件的图中可以看出，这个线程池位于EndPoint与Processor之间用于处理接收到的Socket请求并调用Proessor,并没有直接处理业务呀……</div>2019-06-30</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/36/d2/c7357723.jpg" width="30px"><span>发条橙子 。</span> 👍（6） 💬（2）<div>老师，对于你的问题，实际上我也不理解为何要加锁 。
首先，按理说server对每一个service开一个线程去初始化 。 应该不会多个线程对一个service同时初始化吧。
再者，这块同步如果是要防止重复初始化，那应该在start()方法中做，否则等释放锁后，下一个线程获得锁还是会执行start()方法。

所以这块加锁具体的作用我也看不懂，难道是起到多线程同步阻塞的作用？？</div>2019-05-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/23/ed/a4a774a8.jpg" width="30px"><span>What for</span> 👍（5） 💬（1）<div>老师您好，问个问题：
文中提到用动态数组节省内存，据我所知对象数组里放的是引用而不是对象本身，所以理论上建一个稍微大一点的数组（比如说常见的 16）似乎并不会占用太多空间，请问我的理解有没有问题？</div>2019-07-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/79/4b/740f91ca.jpg" width="30px"><span>-W.LI-</span> 👍（5） 💬（1）<div>老师好!catalina的start()方法末尾那部分不太理解能帮忙讲解下么。
&#47;&#47; 用 await 方法监听停止请求
    if (await) {
        await();
        stop();
    }
if里面那个await我理解是一个属性值是否启用await。然后进入await()方法，出了await()就直接stop()了。下文老师说await()是调用了Server的await()方法，然后Server的await()方法会死循环监听8005端口。读取到停止命令就会退出死循环。回到catalina执行stop方法。我这边的问题是。调用catalina.start方法的线程一直阻塞着，处理监听事件么，监听到关闭事件就去stop()?。感觉好怪啊!请老师看下哪里理解错了。
课后问题:文中说部分通过线程池实现并发加载，加同步方法就是为了保证线程安全。</div>2019-05-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/16/5b/83a35681.jpg" width="30px"><span>Monday</span> 👍（5） 💬（3）<div>根据老师的给出的Github上Tomcat源码调试Tomcat的启动过程，遇到以下这个问题。
经debug发现，运行完Catalina.load()方法的第566行digester.parse(inputSource)初始化了Server对象。但是我单步进入第566行，各种操作都没有跟踪到具体是哪一行初始化了Server对象。莫非有Listener？</div>2019-05-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/53/3d/1189e48a.jpg" width="30px"><span>微思</span> 👍（4） 💬（2）<div>老师，以上源码是基于tomcat的哪个版本？</div>2019-05-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/79/69/5960a2af.jpg" width="30px"><span>王智</span> 👍（2） 💬（1）<div>老师,具体的注入是个什么样的概念,上节课说的子组件注入到父组件,内层组件注入到外层组件,这是个什么样的操作,在上面的代码中并没有看到具体的操作呢?</div>2019-05-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/17/87/be/7466bf26.jpg" width="30px"><span>清风</span> 👍（1） 💬（1）<div>调试源码，会遇到在执行不到对应的断点的情况，看调用栈是被之前的断点拦住了，这个有什么好的断点调试方法吗，这样调试太费劲了</div>2019-05-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/4e/1b/f4b786b9.jpg" width="30px"><span>飞翔</span> 👍（1） 💬（2）<div>老师能讲一下startup.sh里边的code 都啥意思不？</div>2019-05-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/b5/d4/e58e39f0.jpg" width="30px"><span>Geek_0quh3e</span> 👍（0） 💬（1）<div>Mapping和MapperListener会重点讲嘛？</div>2019-06-04</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/6d/8f/81e282e2.jpg" width="30px"><span>802.11</span> 👍（0） 💬（1）<div>abel614: {
                            label613: {
                                try {
老师，在tomcat出现的，这是什么语法呀</div>2019-06-02</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/74/c9/d3439ca4.jpg" width="30px"><span>why</span> 👍（57） 💬（0）<div>- Tomcat 本质是 Java 程序, [startup.sh](http:&#47;&#47;startup.sh) 启动 JVM 运行 Tomcat 启动类 bootstrap
- Bootstrap 初始化类加载器, 创建 Catalina
- Catalina 解析 server.xml, 创建相应组件, 调用 Server start 方法
- Server 组件管理 Service 组件并调用其 start 方法
- Service 负责管理连接器和顶层容器 Engine, 其会调用 Engine start 方法
- 这些类不处理具体请求, 主要管理下层组件, 并分配请求
- Catalina 完成两个功能
    - 解析 server.xml, 创建定义的各组件, 调用 server init 和 start 方法
    - 处理异常情况, 例如 ctrl + c 关闭 Tomcat. 其会在 JVM 中注册&quot;关闭钩子&quot;
        - 关闭钩子, 在关闭 JVM 时做清理工作, 例如刷新缓存到磁盘
        - 关闭钩子是一个线程, JVM 停止前会执行器 run 方法, 该 run 方法调用 server stop 方法
- Server 组件, 实现类 StandServer
    - 继承了 LifeCycleBase
    - 子组件是 Service, 需要管理其生命周期(调用其 LifeCycle 的方法), 用数组保存多个 Service 组件, 动态扩容数组来添加组件
    - 启动一个 socket Listen停止端口, Catalina 启动时, 调用 Server await 方法, 其创建 socket Listen 8005 端口, 并在死循环中等连接, 检查到 shutdown 命令, 调用 stop 方法
- Service 组件, 实现类 StandService
    - 包含 Server, Connector, Engine 和 Mapper 组件的成员变量
    - 还包含 MapperListener 成员变量, 以支持热部署, 其Listen容器变化, 并更新 Mapper, 是观察者模式
    - 需注意各组件启动顺序, 根据其依赖关系确定
        - 先启动 Engine, 再启动 Mapper Listener, 最后启动连接器, 而停止顺序相反.
- Engine 组件, 实现类 StandEngine 继承 ContainerBase
    - ContainerBase 实现了维护子组件的逻辑, 用 HaspMap 保存子组件, 因此各层容器可重用逻辑
    - ContainerBase 用专门线程池启动子容器, 并负责子组件启动&#47;停止, &quot;增删改查&quot;
    - 请求到达 Engine 之前, Mapper 通过 URL 定位了容器, 并存入 Request 中. Engine 从 Request 取出 Host 子容器, 并调用其 pipeline 的第一个 valve</div>2019-06-02</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/93/ee/101f0356.jpg" width="30px"><span>一路远行</span> 👍（32） 💬（1）<div>加锁通常的场景是存在多个线程并发操作不安全的数据结构。

不安全的数据结构:
Server本身包含多个Service，内部实现上用数组来存储services，数组的并发操作(包含缩容，扩容)是不安全的。所以，在并发操作(添加&#47;修改&#47;删除&#47;遍历等)services数组时，需要进行加锁处理。

可能存在并发操作的场景:
Tomcat提供MBean的机制对管理的对象进行并发操作，如添加&#47;删除某个service。</div>2019-05-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/0b/4e/fd946cb2.jpg" width="30px"><span>allean</span> 👍（14） 💬（0）<div>老师的专栏思路清晰，讲解的深入但又通俗易懂，感谢大佬带我飞😁</div>2019-05-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/16/5b/83a35681.jpg" width="30px"><span>Monday</span> 👍（7） 💬（2）<div>listener对应的中文（三个字）竟然是敏感词。。。</div>2019-05-29</li><br/><li><img src="" width="30px"><span>Mongo</span> 👍（2） 💬（0）<div>因为 tomcat 支持热部署，故需要加锁来确定服务正确的加载。</div>2020-03-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/24/5d/65e61dcb.jpg" width="30px"><span>学无涯</span> 👍（1） 💬（0）<div>一个Server可以有多个Service，这样设计的意义是什么呢，为什么不使用一个Service</div>2021-08-02</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/ca/bd/a51ae4b2.jpg" width="30px"><span>吃饭饭</span> 👍（1） 💬（0）<div>老师，真正启动容器和组件是在 StandardService 中吧？每个 Service 都有自己的组件和容器，这里没有产生竞态条件，为什么需要加锁，没想明白，希望老师能解答一下，谢谢：）</div>2019-10-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/10/61/7ba48062.jpg" width="30px"><span>菜鸡小王子</span> 👍（1） 💬（1）<div>老师你好  我看catalina这个类里面start方法，最后有个await监听关闭socket，里面的判断是这样的：if（await）｛await（）；stop（）；｝  我疑惑的是，await变量设置值为false  这份代码一直进不去呀  我没找到哪块代码会将这个await设置为true  谢谢老师</div>2019-07-15</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1a/0d/81/ed4957e8.jpg" width="30px"><span>walzzz</span> 👍（0） 💬（0）<div>加锁的原因，搜索了源码中其他加锁的地方，譬如stop中也会对engine加锁，这里是为了避免start的过程中同时stop所造成的异常，因此猜测竞态主要来自对同一组件的不同操作。</div>2023-11-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1b/5d/c3/69019d24.jpg" width="30px"><span>江东</span> 👍（0） 💬（0）<div>Server 组件的在启动连接器和容器时，都分别加了锁，这是因为JMX的原因吗</div>2021-07-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/51/0d/fc1652fe.jpg" width="30px"><span>James</span> 👍（0） 💬（0）<div>请问问答题：Server 组件的在启动连接器和容器时，都分别加了锁，这是为什么
什么情况下才会导致线程安全问题。</div>2021-03-05</li><br/>
</ul>