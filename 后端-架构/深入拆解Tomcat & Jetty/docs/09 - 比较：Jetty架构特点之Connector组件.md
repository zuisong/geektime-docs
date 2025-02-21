经过专栏前面几期的学习，相信你对Tomcat的整体架构和工作原理有了基本了解。但是Servlet容器并非只有Tomcat一家，还有别的架构设计思路吗？今天我们就来看看Jetty的设计特点。

Jetty是Eclipse基金会的一个开源项目，和Tomcat一样，Jetty也是一个“HTTP服务器 + Servlet容器”，并且Jetty和Tomcat在架构设计上有不少相似的地方。但同时Jetty也有自己的特点，主要是更加小巧，更易于定制化。Jetty作为一名后起之秀，应用范围也越来越广，比如Google App Engine就采用了Jetty来作为Web容器。Jetty和Tomcat各有特点，所以今天我会和你重点聊聊Jetty在哪些地方跟Tomcat不同。通过比较它们的差异，一方面希望可以继续加深你对Web容器架构设计的理解，另一方面也让你更清楚它们的设计区别，并根据它们的特点来选用这两款Web容器。

## 鸟瞰Jetty整体架构

简单来说，Jetty Server就是由多个Connector（连接器）、多个Handler（处理器），以及一个线程池组成。整体结构请看下面这张图。

![](https://static001.geekbang.org/resource/image/95/b6/95b908af86695af107fd3877a02190b6.jpg?wh=1368%2A728)

跟Tomcat一样，Jetty也有HTTP服务器和Servlet容器的功能，因此Jetty中的Connector组件和Handler组件分别来实现这两个功能，而这两个组件工作时所需要的线程资源都直接从一个全局线程池ThreadPool中获取。
<div><strong>精选留言（30）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/12/a8/e2/f8e51df2.jpg" width="30px"><span>Li Shunduo</span> 👍（47） 💬（2）<div>有两个问题请教老师：
问题一：根据文章看，Jetty中有多个Acceptor组件，请问这些Acceptor背后是共享同一个ServerSocketChannel？还是每个Acceptor有自己的ServerSocketChannel? 如果有多个ServerSocketChannel的话，这些ServerSocketChannel如何做到监听同一个端口？连接到来时如何决定分配到哪一个ServerSocketChannel?
问题二：Acceptor组件是直接使用ServerSocketChannel.accept()方法来接受连接的，为什么不使用向Selector注册OP_ACCEPT事件的方式来接受连接？直接调用.accept()方法有什么考虑？
问题三：Jetty中有多个ManagedSelector，这些ManagedSelector背后是共享同一个Selector吗？还是每个ManagedSelector有自己的Selector？如果是多个Selector有什么好处，注册IO事件时如何选择合适的Selector？
</div>2019-06-01</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/74/c9/d3439ca4.jpg" width="30px"><span>why</span> 👍（22） 💬（1）<div>- Jetty 也是 Http 服务器 + Servlet 容器, 更小巧, 更易于定制
- Jetty 架构: 多个 Connector + 多个 Handler + 一个全局线程池(Connector 和 Handler 共享)
- 多个 Connector 在不同端口监听请求, 可以根据应用场景选择 Handler : ServletHandler 和 SessionHandler
- Jetty 用 Server 启动和协调上述组件
- Jetty 与 Tomcat 的区别
    - Jetty 没有 Service 的概念, Jetty 的 Connector 被 Handler 共享
    - Tomcat 连接器有自己的线程池, Jetty Connector 使用全局线程池
- Connector 组件, 完成 I&#47;O 模型 + 协议封装
    - 只支持 NIO 模型, 通过 Connection 组件封装协议
    - Java NIO 核心组件为: Channel, Buffer, Selector
        - Channel 即一个 socket 连接
        - Channel 通过 Buffer 间接读写数据
        - Selector 检测 Channel 的 I&#47;O 事件, 可以处理多个 Channel, 减少线程切换开销
    - NIO 完成三个功能: 监听连接, I&#47;O 事件查询, 数据读写, 对应的 Jetty 封装为 Acceptor, SelectorManager, Connection
    - Acceptor 接受请求
        - Jetty 有独立 Acceptor 线程组处理连接请求
        - Connector 的实现类 ServerConnector 中有 _acceptors 数组, 保存固定数目的 Acceptor.
        - Acceptor 是 Connector 内部类, 是 Runnable 的. 通过 getExecutor 得到线程以执行
        - Acceptor 通过阻塞接受连接, 接受连接后, 调用 accepted, 其将 SocketChannel 设为非阻塞, 交给 Selector 处理
    - SelectorManager 管理 Selector
        - 被管理的 Selector 叫 ManagedSelector, 保存于 SelectorManager 的一个数组中
        - SelectorManager 选择一个 Selector, 并创建一个任务 Accept 给 ManagedSelector, ManagerSelector 实现:
            - 调用 register 将 Channel 注册到 Selector, 拿到 SelectionKey
            - 创建 EndPoint 和 Connection, 并与 SelectionKey(Channel) 绑定
        - 当有 I&#47;O 事件时, ManagedSelector 调用 EndPoint 返回一个 Runnable 对象, 并扔给线程池执行
    - Connection
        - 上述 Runnable 对象会调用 Connection 处理请求, 得到 Request 并调用 Handler 容器处理
        - 具体实现类 HttpConnection
            - 请求处理: 在 EndPoint 中注册一系列回调函数, 数据到达时调用. ( 用回调函数模拟异步 I&#47;O ). 在回调方法中读数据, 解析请求并存到 Request
            - 相应处理: Handler 返回 Response, HttpConnection 通过 EndPoint 写到 Channel
- 留言
    - 每次请求跟一个 Hanlder 线程是一对一的关系, 下一次再来请求，会分配一个新的 Hanlder 线程。
    - 多个 Acceptor 共享同一个 ServerSocketChannel 。多个 Acceptor 线程调用同一个 ServerSocketChannel 的 accept 方法，由操作系统保证线程安全</div>2019-06-02</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/67/8a/babd74dc.jpg" width="30px"><span>锦</span> 👍（16） 💬（1）<div>使用不同的线程是为了合理的使用全局线程池。
我有两个问题请教老师：
问题一：负责读写的socket与handle线程是什么对应关系呢？多对1，还是1对1？
问题二：如果有很多tcp建立连接后迟迟没有写入数据导致连接请求堵塞，或者如果有很多handle在处理耗时io操作时，
同样可能拖慢整个线程池，进而影响到accepters和selectors，那么可能会拖慢整个线程池，jetty是如何考虑的呢？</div>2019-05-30</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/5d/0d/9a7e588c.jpg" width="30px"><span>focus</span> 👍（13） 💬（1）<div>源码都是怎么导入，怎么编译，怎么看呢</div>2019-05-30</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/79/4b/740f91ca.jpg" width="30px"><span>-W.LI-</span> 👍（10） 💬（1）<div>老师好!在线程模型设计上 Tomcat 的 NioEndpoint 跟 Jetty 的 Connector 是相似的，都是用一个 Acceptor 数组监听连接，用一个 Selector 数组侦测 I&#47;O 事件。这句话怎么理解啊?
问题1:Acceptor 数组监听连接,监听的是一次TCP链接么?

问题2:Selector 数组侦测 I&#47;O 事件，具体监听的是啥?

问题3:长链接下，每次http请求会新打开一个channel的，还是复用原有的channel，channel是阻塞还是非阻塞的。

说的有点乱不晓得老师看的懂不😂。我就是想知道，一次TCP链接，多次http具体是和connector怎么绑定的。</div>2019-06-01</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/aa/e6/cc3f3853.jpg" width="30px"><span>gameboy120</span> 👍（9） 💬（1）<div>请问注册一堆回调函数的用意是什么？</div>2019-07-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/79/4b/740f91ca.jpg" width="30px"><span>-W.LI-</span> 👍（9） 💬（1）<div>老师好，跑在不同的线程里是为了解耦么?实在想不出，告诉答案吧</div>2019-06-02</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/69/c6/513df085.jpg" width="30px"><span>强哥</span> 👍（9） 💬（1）<div>说了各自的特点。但是感觉缺少关键性的对比，以及背后设计的理念，建议再深入探讨各自的主要差异及场景</div>2019-05-30</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTKPjJg1rdQ0D0l6EbdrXsKhmCAVLBJmc7QNFHS19LMdjk1ibVOVlicuZlWTrEWUsYuoftdhJvBWcTGw/132" width="30px"><span>kxkq2000</span> 👍（7） 💬（1）<div>分在不同的线程里我认为是这样分工明确好比工厂流水线最大化提升处理能力。
我有个疑问是用全局线程池真的好吗，不是应该根据任务类型分配线程池的吗？用全局的不会互相干扰吗？</div>2019-06-01</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/03/57/31595f22.jpg" width="30px"><span>Lrwin</span> 👍（7） 💬（2）<div>感觉jetty就是一个netty模型</div>2019-05-30</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/17/6e/89/be79c8a5.jpg" width="30px"><span>Lc</span> 👍（4） 💬（1）<div>Jetty作为后起之秀，跟tomcat相比，它的优势在哪儿？他们的设计思路不同，我们自己在设计的时候应该依据什么来确定使用哪种呢？</div>2019-05-30</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/IgjIXs9jjpODTPaOLrms0XOhJ8pxMcaZgtgBrPG6deqsKXv1sPIqkg0faL6X0rtFicJn5Wf7QXTickjYWpmF0V8A/132" width="30px"><span>Geek_28b75e</span> 👍（3） 💬（1）<div>老师，麻烦您给说说bio和nio的区别，表面上的差别我看过了，能不能从操作系统角度给讲解一下呢？麻烦您了，实在有点难理解</div>2019-06-04</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/6d/8f/81e282e2.jpg" width="30px"><span>802.11</span> 👍（3） 💬（1）<div>老师，在一个类里再写接口或者类，一般是基于什么样的设计思想呢</div>2019-06-02</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTKDfO7wKibzpwxZzSMDtkPlnD2nqtkBEX2g71uibJZY1Ly2dNulEICGqkMWUicOicLGIibTib7fPEBU8lPQ/132" width="30px"><span>毕延文</span> 👍（2） 💬（1）<div>前面几章还好，到这里就有些看不懂了，我还是太菜了。</div>2019-06-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/16/5b/83a35681.jpg" width="30px"><span>Monday</span> 👍（2） 💬（1）<div>tomcat还没学透，就学jetty，两者还相互比较，生怕自己混淆了</div>2019-05-30</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/cf/14/384258ba.jpg" width="30px"><span>Wiggle Wiggle</span> 👍（1） 💬（1）<div>请教一下，在 SelectorManager 在 accept 方法里，向selector中注册channel的事件为什么还是on_accept呢？在上一步的serverchannel不是已经建立连接了吗？</div>2019-08-03</li><br/><li><img src="https://wx.qlogo.cn/mmopen/vi_32/DYAIOgq83eqLcWH3mSPmhjrs1aGL4b3TqI7xDqWWibM4nYFrRlp0z7FNSWaJz0mqovrgIA7ibmrPt8zRScSfRaqQ/132" width="30px"><span>易儿易</span> 👍（1） 💬（1）<div>Jetty这个共享线程池的设计，在另一篇专讲并发的专栏里是明确提出严禁使用的……比如A调用B，线程池容量2，2个A同时开始执行，这个时候B无法创建，A无法释放……Jetty有特别设计可以避免这种情况吗？</div>2019-07-01</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/5c/c5/1231d633.jpg" width="30px"><span>梁中华</span> 👍（1） 💬（1）<div>jetty内部是用epoll的吗？还是只是传统的select?</div>2019-06-21</li><br/><li><img src="" width="30px"><span>田程杯166</span> 👍（1） 💬（1）<div>java处理网络请求的底层都是socket，传统bio是将每个网络连接的socket封装完成后，交给单独的线程去处理，那nio是怎么处理？将每个网络连接封装成的socket，用一个线程去接受 ，然后放到一个数组里面，再用一个线程去轮询这个socket数组？那么实际处理业务的代码是在什么线程呢？业务线程是在哪里创建的呢？</div>2019-06-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/d1/fd/1cdfef42.jpg" width="30px"><span>刘为红</span> 👍（1） 💬（1）<div>李老师，您好！看源码tomcat9好像把阻塞IO去掉了，也不支持阻塞IO，tomcat支持NIO和NIO2（异步IO），jetty不支持NIO2吗？</div>2019-06-06</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/ee/67/d6d9499e.jpg" width="30px"><span>木木木</span> 👍（1） 💬（1）<div>从理论上，Accept接受请求，SelectorManager处理客户端socket组的轮询，Connection负责数据的收发，三者关系是异步的，可以分成不同的线程。特别是jetty的Accept是阻塞的更没办法。
有几点疑问，按我的理解，虽然是全局线程池，这三者应该有独立的线程最大数量配置吧，这样应该更可控点，否则相互抢占，会不会有问题。
第二点，我觉得Jetty的多个Accept本身可以设成非阻塞的，然后挂到一个selector下面，现在这种设计就是bio了。不知道它是偷懒呢（既然已经有selector了），还是有其他的考虑呢。
第三点，SelectorManager里的多个ManagedSelector本身其实可以合成一个，所有channel挂在一个selector下面，有多个selector是不是基于性能考虑，利用多核多线程能力</div>2019-06-04</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/b3/c5/7fc124e2.jpg" width="30px"><span>Liam</span> 👍（1） 💬（1）<div>文中的事例里面，acceptor拿到连接后创建SocketChannel， 为什么又重新去注册Accept事件呢，socketChannel不应该只关心读写事件吗</div>2019-05-30</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTLNRjRHibgf1ia8RrhPJSZBiawk5OOb5VsVva5cmwickaV58WsaOkljD5rVeibWnlic62c2ZqcPsapOqCdw/132" width="30px"><span>east</span> 👍（1） 💬（1）<div>共享的线程池的大小就是一个应用的最大并发量吗</div>2019-05-30</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/8d/a6/22c37c91.jpg" width="30px"><span>楊_宵夜</span> 👍（0） 💬（1）<div>李老师好, 请问, spring-boot的jetty9, Acceptor第667-&gt;670行, 是
CountDownLatch stopping = _stopping;   &#47;&#47; 此处_stopping是AbstractConnector的成员变量
然后就stopping.countDown()了;

我就想问, 为何要创建一个局部引用? 直接使用 _stopping.countDown()不行吗?
</div>2019-07-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/03/57/31595f22.jpg" width="30px"><span>Lrwin</span> 👍（0） 💬（1）<div>创建多个Acceptor 真的有必要吗？一个线程一个selector就可以用于监听所有的连接呀、。

netty中bossgroup也就只有一个eventloop来监听所有连接。</div>2019-06-03</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/79/4b/740f91ca.jpg" width="30px"><span>-W.LI-</span> 👍（0） 💬（1）<div>老师好!源码里面有些全局变量希望给下注释解释下。都搞不清楚acceptor怎么拿到selectormanager对象的。然后_manager.accept(channel)调用的是一个入参，下面是两个入参的重载方法。基础比较差希望老师照顾下。</div>2019-06-02</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/bb/c9/37924ad4.jpg" width="30px"><span>天天向上</span> 👍（2） 💬（0）<div>为了分工协作，IO工作，业务处理工作分成两大流程环节，互不干扰，分工明确，
高效复用IO线程</div>2019-05-30</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/1f/48/4bf434ef.jpg" width="30px"><span>非洲铜</span> 👍（1） 💬（0）<div>一直没用过jetty当web容器，看的有点懵逼</div>2019-05-31</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/87/62/f99b5b05.jpg" width="30px"><span>曙光</span> 👍（0） 💬（0）<div>老师，有个疑问：
1 SocketChannel channel = serverChannel.accept();
2 _key = _channel.register(selector, SelectionKey.OP_ACCEPT, this);
既然已经监听到接收事件，为什么后面继续监听OP_ACCEPT，而不是OP_READ?</div>2022-09-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/87/62/f99b5b05.jpg" width="30px"><span>曙光</span> 👍（0） 💬（0）<div>老师，有个疑问：
1 SocketChannel channel = serverChannel.accept();
2 _key = _channel.register(selector, SelectionKey.OP_ACCEPT, this); </div>2022-09-18</li><br/>
</ul>