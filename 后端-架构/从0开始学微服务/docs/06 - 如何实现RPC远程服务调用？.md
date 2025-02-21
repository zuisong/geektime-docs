专栏上一期我讲过，要完成一次服务调用，首先要解决的问题是服务消费者如何得到服务提供者的地址，其中注册中心扮演了关键角色，服务提供者把自己的地址登记到注册中心，服务消费者就可以查询注册中心得到服务提供者的地址，可以说注册中心犹如海上的一座灯塔，为服务消费者指引了前行的方向。

有了服务提供者的地址后，服务消费者就可以向这个地址发起请求了，但这时候也产生了一个新的问题。你知道，在单体应用时，一次服务调用发生在同一台机器上的同一个进程内部，也就是说调用发生在本机内部，因此也被叫作本地方法调用。在进行服务化拆分之后，服务提供者和服务消费者运行在两台不同物理机上的不同进程内，它们之间的调用相比于本地方法调用，可称之为远程方法调用，简称RPC（Remote Procedure Call），那么RPC调用是如何实现的呢？

在介绍RPC调用的原理之前，先来想象一下一次电话通话的过程。首先，呼叫者A通过查询号码簿找到被呼叫者B的电话号码，然后拨打B的电话。B接到来电提示时，如果方便接听的话就会接听；如果不方便接听的话，A就得一直等待。当等待超过一段时间后，电话会因超时被挂断，这个时候A需要再次拨打电话，一直等到B空闲的时候，才能接听。
<div><strong>精选留言（30）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/0f/aa/21/6c3ba9af.jpg" width="30px"><span>lfn</span> 👍（83） 💬（1）<div>我觉得压缩只是序列化的一个原因，但却不是最本质的原因。序列化是为了解决内存中数据结构到字节序列的映射过程中，如何保留各个结构和字段间的关系而生的技术。</div>2018-09-04</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/a5/c9/eb389183.jpg" width="30px"><span>Hungry</span> 👍（6） 💬（1）<div>老师，我觉得序列化最大的目的是解决异构系统的数据传输，比如大小端、远端的持久存储；至于不同语言的代码结构上的变量映射，TLV压缩，这些应该是其次的</div>2018-09-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/06/81/28418795.jpg" width="30px"><span>衣申人</span> 👍（5） 💬（1）<div>原来不只是我觉得序列化不是为了压缩的，嘻嘻。我认为序列化和反序列化是解决内存数据到字节流的相互转换的。而压缩不压缩，其实不是必要的。当然序列化后的大小是评估一种序列化方式的优劣因素之一。</div>2018-09-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/ed/1a/269eb3d6.jpg" width="30px"><span>cfanbo</span> 👍（5） 💬（1）<div>（1）同步阻塞IO（Blocking IO）：即传统的IO模型。
（2）同步非阻塞IO（Non-blocking IO）：默认创建的socket都是阻塞的，非阻塞IO要求socket被设置为NONBLOCK。
（3）IO多路复用（IO Multiplexing）：即经典的Reactor设计模式，有时也称为异步阻塞IO，Java中的Selector和Linux中的epoll都是这种模型。高性能并发服务程序使用IO多路复用模型+多线程任务处理的架构。
（4）异步IO（Asynchronous IO）：即经典的Proactor设计模式，也称为异步非阻塞IO。

上面提到的“同步非阻塞“方式怎么不一样？</div>2018-09-04</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/7a/5d/b2e68df2.jpg" width="30px"><span>九斤鱼</span> 👍（4） 💬（1）<div>感觉这几篇还是在入门，实战什么时候开始呢？，老师，我更关心的实际操作层面，比如技术栈选型方面，是spring cloud呢还是dubbo还是其他什么，
系统划分后的工程如何管理，如何部署，如何测试，多容器环境下需要注意什么等等问题，望老师可以在接下来的课程里可以用实际项目解答一下🙏</div>2018-09-06</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/85/a5/471ce926.jpg" width="30px"><span>靖远小和尚</span> 👍（4） 💬（1）<div>老师你好aio是异步阻塞是不是写错了！他应该是异步非阻塞吧！</div>2018-09-04</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/ac/a1/43d83698.jpg" width="30px"><span>云学</span> 👍（3） 💬（1）<div>这篇文章感觉有些地方不太严谨，序列化是和异构系统有关</div>2018-09-05</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/7e/c6/83684988.jpg" width="30px"><span>齐家</span> 👍（2） 💬（1）<div>NIO,AIO描述有问题。
NIO （New I&#47;O）：同时支持阻塞与非阻塞模式，但主要是使用同步非阻塞IO。

AIO （Asynchronous I&#47;O）：异步非阻塞I&#47;O模型。</div>2018-09-04</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/ce/b2/1f914527.jpg" width="30px"><span>海盗船长</span> 👍（0） 💬（2）<div>老师你好，感觉你讲的重点都是rpc，对于restful，还需要注册中心吗</div>2020-01-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/07/8c/0d886dcc.jpg" width="30px"><span>蚂蚁内推+v</span> 👍（0） 💬（2）<div>老师 nioq这块方便详细说下嘛</div>2018-12-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/45/f7/0f9bcf1f.jpg" width="30px"><span>ServerCoder</span> 👍（0） 💬（1）<div>图配错了吧，那可是断链的四次挥手过程</div>2018-09-04</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/67/f4/9a1feb59.jpg" width="30px"><span>钱</span> 👍（23） 💬（1）<div>这节原理讲的好，所有的RPC框架应该都是一样的，那为啥还会存在那么多的RPC框架呢？重复造轮子显然会花费人力物力，益处是啥呢？相信老师后面会讲的

正如许多同学都发现了一样，本节讲的也存在一点点瑕疵。

我觉得RPC最核心，少了就是不行那部分内容如下：
1：网络链接，没有这个谈不上R
2：序列化和反序列化，没有这个服务之间无法交流
3：本地业务处理，没有这个谈不上PC，当然这个是涉及业务的部分，是独特的，不是框架开发者关心的部分是业务开发关心的部分

其他：
1：网络通信协议用什么，是场景而定，不过现在HTTP&#47;TCP已是业界的标准
2：序列化和反序列化的框架用什么，也是视情况而定，当然功能强、性能好、易使用、易扩展的谁都爱的
3：压缩和解压缩，这个我认为也是视情况而定的，对性能要求不高完全不用考虑，不过一般都是非常在乎性能的，估计也是有选择的至于选哪一种也是一个视情况而定的权衡问题
4：就连注册中心，也是个附加的功能，是为了解决提供者和消费者较多且变化频繁，如何发现和路由的问题</div>2019-05-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/f5/72/ee4c3df7.jpg" width="30px"><span>萨洪志</span> 👍（18） 💬（1）<div>沙发，珍惜在车上的时间，😂</div>2018-09-04</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/32/c5/38a59795.jpg" width="30px"><span>逍遥子</span> 👍（17） 💬（8）<div>搞不懂为什么区分长http与socket两种通信，个人理解这两者不是一种概念呀，一个是协议一个是通信基石，http协议访问不也是基于套接字么</div>2018-09-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/4b/d4/b7719327.jpg" width="30px"><span>波波安</span> 👍（15） 💬（0）<div>
一、gRPC数据传输采用的http2通信协议。连接管理的方式有
1.GOAWAY帧
服务端发出这种帧给客户端表示服务端在相关的连接上不再接受任何新流
2.PING帧
客户端和服务端均可以发送一个ping帧，对方必须精确回显它们所接收的消息。这可以用来确认连接任然是活动的。
3.连接失败
  客户端检测到连接失败，所有的调用都会以不可用状态关闭。服务端侧所有已经打开的调用都会被以取消状态关闭。
二、在多数语言里，gRPC编程接口同时支持同步和异步。
三、默认使用Protocol buffers协议对数据进行序列化和反序列化</div>2018-10-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/4d/fe/abb7bfe3.jpg" width="30px"><span>bd7xzz</span> 👍（7） 💬（0）<div>我认为序列化主要解决三点:
1.大小端虚，异构系统网络通信时候的大小端序问题，这点由通信底层库实现
2.一种协议，在异构语言中进行数据翻译
3.压缩优化，提高网络通信能力</div>2018-10-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/d7/df/fc0a6709.jpg" width="30px"><span>WolvesLeader</span> 👍（4） 💬（5）<div>服务A调用B，B调用C，假如B响应较慢，会造成整个调用链挂掉吗？有啥好办法防止这种问题吗？</div>2018-09-06</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/d4/7b/7c92c86f.jpg" width="30px"><span>Wayne</span> 👍（2） 💬（0）<div>压缩跟序列化是两回事啊</div>2019-04-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/4e/21/700586eb.jpg" width="30px"><span>王鸿运</span> 👍（2） 💬（0）<div>现在服务端最主流的处理方式应该是nio方式，因为Linux上并没有提供aio接口，epoll也是nio方式</div>2019-01-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/5f/83/bb728e53.jpg" width="30px"><span>Douglas</span> 👍（2） 💬（0）<div>老师，  nio  多路复用io 解决并发连接数问题，  但是，io密集型的应用，业务还是应该 放到单独的线程里面处理的吧，可以创建一个线程池， nio 事件监听连接建立之后， 直接从 业务线程池中获取一个线程来处理业务？</div>2018-10-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/68/da/b8d734bf.jpg" width="30px"><span>白日辰</span> 👍（1） 💬（0）<div>TCP可以看下这个https:&#47;&#47;blog.csdn.net&#47;striveb&#47;article&#47;details&#47;84063712</div>2019-09-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/19/fd/58/1af629c7.jpg" width="30px"><span>6点无痛早起学习的和尚</span> 👍（0） 💬（0）<div>研究了一下，所以 SpringBoot 用的是 NIO，SpringBoot 用的 Tomcat，Tomcat 默认 NIO</div>2024-05-06</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/26/be/e9/9d597e04.jpg" width="30px"><span>豆豆酱</span> 👍（0） 💬（0）<div>socket通信指的是websocket么？
WebSocket是一种在单个TCP连接上进行全双工通信的协议。WebSocket通信协议于2011年被IETF定为标准RFC 6455，并由RFC7936补充规范。WebSocket API也被W3C定为标准。
WebSocket使得客户端和服务器之间的数据交换变得更加简单，允许服务端主动向客户端推送数据。在WebSocket API中，浏览器和服务器只需要完成一次握手，两者之间就直接可以创建持久性的连接，并进行双向数据传输。</div>2022-10-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/ee/c6/bebcbcf0.jpg" width="30px"><span>俯瞰风景.</span> 👍（0） 💬（0）<div>在分布式微服务系统中，服务之间的调用需要通过rpc远程调用的方式。远程调用的过程中会涉及到建立网络链接(http、socket)、进行网络通信(开放协议、私有协议)、进行数据传输（序列化和反序列化）。

通信框架解决客户端和服务端如何建立连接、管理连接以及服务端如何处理请求的问题。
通信协议解决客户端和服务端采用哪种数据传输协议的问题。
序列化和反序列化解决客户端和服务端采用哪种数据编解码的问题。</div>2021-10-07</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/7a/d2/4ba67c0c.jpg" width="30px"><span>Sch0ng</span> 👍（0） 💬（0）<div>实现一个rpc服务，需要考虑：通信协议（HTTP、socket）、通信模型（NIO、BIO、AIO）、数据编码解码（json、XML、PB）、服务端实现、客户端实现。</div>2021-08-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/58/2c/92c7ce3b.jpg" width="30px"><span>易轻尘</span> 👍（0） 💬（0）<div>gRPC调用实现原理简单总结：
服务定义：使用protobuf进行服务定义
序列化与反序列化：使用protobuf定义message，protoc自动生成相应的类以及序列化反序列化代码
请求处理模式：以C++为例，同时提供了BIO和AIO两种方式
服务连接：支持HTTP连接或者socket连接
注：自己实现简单的rpc：Netty管理服务的连接+请求处理+protobuf进行序列化和反序列化</div>2020-05-04</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/4e/21/700586eb.jpg" width="30px"><span>王鸿运</span> 👍（0） 💬（0）<div>序列化的根本原因应该是以一种双方都可以解析方式对数据进行格式化，比如二进制方式和字符串方式。其中c语言的结构体（当然因为不同机器对齐方式不同，需要设置成按1字节填充）和protobuf都是二进制格式，而json和xml都是字符串方式进行序列化。
因为序列化的主要目的不是压缩，虽然为了节省带宽，提高传输速率的原因，大部分序列化方式都会涉及自己的编码方式对数据进行压缩，如protobuf。
但这种压缩编码和压缩算法本质上是不同的，protobuf对字符串字段就没办法压缩，还会因为扩展兼容性需要增加字段标签。而压缩主要是通过分析字符串出线频率，通过变长的编码方式对数据重新编码达到压缩目的</div>2019-01-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/0b/34/f41d73a4.jpg" width="30px"><span>王盛武</span> 👍（0） 💬（0）<div>忠老师总结的4点很到到位，赞</div>2019-01-06</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTJman25D8JlricJVaeweYqr70vyp2acetStqbtaDnCnroGXvuJfgr1As9q47iacTCUUMK1eRUt4KImg/132" width="30px"><span>进阶的小孔</span> 👍（0） 💬（0）<div>原来RPC是这样的</div>2018-12-27</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/IIkdC2gohpcibib0AJvSdnJQefAuQYGlLySQOticThpF7Ck9WuDUQLJlgZ7ic13LIFnGBXXbMsSP3nZsbibBN98ZjGA/132" width="30px"><span>batman</span> 👍（0） 💬（0）<div>TCP三次握手的英文，有没中文对照呀</div>2018-10-23</li><br/>
</ul>