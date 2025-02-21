UNIX系统下的I/O模型有5种：同步阻塞I/O、同步非阻塞I/O、I/O多路复用、信号驱动I/O和异步I/O。这些名词我们好像都似曾相识，但这些I/O通信模型有什么区别？同步和阻塞似乎是一回事，到底有什么不同？等一下，在这之前你是不是应该问自己一个终极问题：什么是I/O？为什么需要这些I/O模型？

所谓的**I/O就是计算机内存与外部设备之间拷贝数据的过程**。我们知道CPU访问内存的速度远远高于外部设备，因此CPU是先把外部设备的数据读到内存里，然后再进行处理。请考虑一下这个场景，当你的程序通过CPU向外部设备发出一个读指令时，数据从外部设备拷贝到内存往往需要一段时间，这个时候CPU没事干了，你的程序是主动把CPU让给别人？还是让CPU不停地查：数据到了吗，数据到了吗……

这就是I/O模型要解决的问题。今天我会先说说各种I/O模型的区别，然后重点分析Tomcat的NioEndpoint组件是如何实现非阻塞I/O模型的。

## Java I/O模型

对于一个网络I/O通信过程，比如网络数据读取，会涉及两个对象，一个是调用这个I/O操作的用户线程，另外一个就是操作系统内核。一个进程的地址空间分为用户空间和内核空间，用户线程不能直接访问内核空间。
<div><strong>精选留言（30）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/11/54/d7/7ab8f58a.jpg" width="30px"><span>🐛</span> 👍（79） 💬（1）<div>老师，操作系统级的连接指的是什么啊？</div>2019-06-11</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/IgjIXs9jjpODTPaOLrms0XOhJ8pxMcaZgtgBrPG6deqsKXv1sPIqkg0faL6X0rtFicJn5Wf7QXTickjYWpmF0V8A/132" width="30px"><span>Geek_28b75e</span> 👍（42） 💬（1）<div>问一个基础问题，线程的同步，和本节所讲的同步，意义上的不同</div>2019-06-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/7b/57/a9b04544.jpg" width="30px"><span>QQ怪</span> 👍（38） 💬（1）<div>老师，信号驱动式 I&#47;O与其他io模型的有啥不一样？</div>2019-06-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/ce/ce/53392e44.jpg" width="30px"><span>BingoJ</span> 👍（27） 💬（2）<div>老师，那我们常说Java中自身的NIO到底是同步非阻塞，还是IO多路复用呢？</div>2019-06-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/9c/35/9dc79371.jpg" width="30px"><span>你好旅行者</span> 👍（26） 💬（5）<div>对于【同步与异步指的是应用程序在与内核通信时，数据从内核空间到应用空间的拷贝内核主动发起还是应用程序触发。】我有一个问题，以同步非阻塞为例，当网卡接收到数据，要将数据送到用户进程时，此时是由用户进程主动向操作系统请求拷贝网卡的数据吗？老师能不能详细介绍一下这个过程？</div>2019-06-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/20/08/bc06bc69.jpg" width="30px"><span>Dovelol</span> 👍（22） 💬（2）<div>老师，请教下，”当客户端发起一个http请求时，首先由Acceptor线程run方法中的socket = endpoint.serverSocketAccept();接收连接，然后传递给名称为Poller的线程去侦测I&#47;O事件，Poller线程会一直select，选出内核将数据从网卡拷贝到内核空间的 channel（也就是内核已经准备好数据）然后交给名称为Catalina-exec的线程去处理，这个过程也包括内核将数据从内核空间拷贝到用户空间这么一个过程，所以对于exec线程是阻塞的，此时用户空间（也就是exec线程）就接收到了数据，可以解析然后做业务处理了。
1.想问下老师我对这个流程的理解对吗，如果不对，哪个地方有问题呢？
2.老师讲的2个步骤是融合在这里面的吗？
3.老师说的“当用户线程发起 I&#47;O 操作后，xxx”，这里面应该是哪一步去发起的I&#47;O操作呢？</div>2019-06-12</li><br/><li><img src="" width="30px"><span>zyz</span> 👍（18） 💬（1）<div>老师！Tomcat为什么不用Semaphore而是自己实现LimitLatch来限流呢？出于什么考虑？性能？不想强依赖Semaphore？</div>2019-06-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/16/5b/83a35681.jpg" width="30px"><span>Monday</span> 👍（17） 💬（1）<div>阻塞与同异步的区别
本节的总结有如下的2句话，1）阻塞与非阻塞指的是应用程序发起i&#47;o操作后是等待还是立即返回。2）同步与异步指的是应用程序在与内核通信时，数据从内核空间到应用空间的拷贝内核主动发起还是应用程序触发。
1，阻塞对应的是等待，非阻塞对应的是立即返回。这句应该好理解。
2，同步对应的是哪个？
3，我的理解是js中ajax请求的有个属性，async为true异步false同步。这个对应了网络IO。好理解
4，我的理解阻塞非阻塞是java的jcu包下ArrayBlockingQueue队列中的offer和put方法的区别。其中前者是非阻塞的，队列满了就直接返回入队失败；后者是阻塞的，如果队列满了就阻塞入队的线程，直到队列有空闲并插入成功后返回true。这里面会牵涉到内核吗？
5，反正学完本节发现不知道的更多了，原来自己一直没分清楚过同&#47;异步和是否阻塞。。。疼疼疼</div>2019-06-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/8c/f7/a4de6f64.jpg" width="30px"><span>大卫</span> 👍（13） 💬（2）<div>李老师您好，
我来结合实际问题提3个问题吧。
结合这篇文章请教下线上的遇到的故障，接口响应慢最终导致无法正常响应。

jstack打印了堆栈信息，其中一台台机器，总线程数一共4700多，有3500多个Runnable状态的线程，有WAITING状态的1200多。
另外一台机器总线程数一共1200多，大部分都是WAITING状态。
部署方式是物理机（高配置，一般是24CPU 128G内存）+docker（一个docker）
springboot-tomcat参数设置如下：
server.tomcat.accept-count=1000
server.tomcat.max-threads=1000
server.tomcat.max-connections=1000

其中3500多个Runnable状态的线程栈信息如下所示：
&quot;I&#47;O dispatcher 1098713&quot; #1202019 prio=5 os_prio=0 tid=0x00007fdd24071000 nid=0x221f runnable [0x00007fdd28709000]
   java.lang.Thread.State: RUNNABLE
        at sun.nio.ch.EPollArrayWrapper.epollWait(Native Method)
        at sun.nio.ch.EPollArrayWrapper.poll(EPollArrayWrapper.java:269)
        at sun.nio.ch.EPollSelectorImpl.doSelect(EPollSelectorImpl.java:93)
        at sun.nio.ch.SelectorImpl.lockAndDoSelect(SelectorImpl.java:86)
        - locked &lt;0x00000007504d4020&gt; (a sun.nio.ch.Util$2)
        - locked &lt;0x00000007504d4008&gt; (a java.util.Collections$UnmodifiableSet)
        - locked &lt;0x0000000754258eb8&gt; (a sun.nio.ch.EPollSelectorImpl)
        at sun.nio.ch.SelectorImpl.select(SelectorImpl.java:97)
        at org.apache.http.impl.nio.reactor.AbstractIOReactor.execute(AbstractIOReactor.java:255)
        at org.apache.http.impl.nio.reactor.BaseIOReactor.execute(BaseIOReactor.java:104)
        at org.apache.http.impl.nio.reactor.AbstractMultiworkerIOReactor$Worker.run(AbstractMultiworkerIOReactor.java:588)
        at java.lang.Thread.run(Thread.java:745)

问题1：引起上述大量Runnable线程的原因，是因为tomcat最大连接数默认10000导致，放进来这么多待运行的线程吗？有疑惑，头一次遇到呢。
问题2：有1000多个WAITING状态的，目前分析是因为使用了HttpClient连接池，httpclient版本是4.5.5，其中可能没有合理设置超时参数导致，需要增加connectionRequestTimeout，减少retry重试次数，包括defaultMaxPerRoute参数的合理设置。这里的HttpClient线程池的大小和路由池大小怎么设置更合理呢？（可能跟tomcat没有太直接关系，如果老师有这方面经验不吝赐教）
问题3：上面提到部署方式是docker，其中一台docker压测接口比如qps是100，该接口就是调用了第三方接口聚合下返回结果，但是再在同一台物理机上部署一个docker，nginx负载到这两台docker上，qps还是100，并没有什么提升，这个应该从哪方面分析下原因呢？

问题有点多哦，麻烦老师了~</div>2019-06-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/4e/1b/f4b786b9.jpg" width="30px"><span>飞翔</span> 👍（12） 💬（1）<div>，当你的程序通过 CPU 向外部设备发出一个读指令时，数据从...


李老师想问一个问题， cpu发出读指令， 那么是什么东西负责读数据从硬盘到内存这个过程呢？ 不是cpu嘛？</div>2019-06-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/e7/b2/334bc992.jpg" width="30px"><span>AlfredLover</span> 👍（11） 💬（2）<div>有个疑问：内核数据从内核空间拷贝到用户空间？
这个过程是从内核内存拷贝到用户内存吗？
假如是这样会不会有点浪费？
毕竟实际上只有一块内存，能否直接把内存地址指向用户空间可以读取？</div>2019-10-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/ad/27/5556ae50.jpg" width="30px"><span>Demter</span> 👍（11） 💬（2）<div>对比同步阻塞和非阻塞，感觉就是多了个read方法循环调用，既然等数据到达用户空间后都会主动把线程唤醒，为什么还需要非阻塞方式中不断的read调用呢？不是多此一举吗？调不调用不是都一样的嘛</div>2019-08-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/85/91/9edff63f.jpg" width="30px"><span>星火燎原</span> 👍（8） 💬（1）<div>阻塞 用户线程会一直在那里等待数据，
非阻塞 用户线程不会等待，而是在轮询数据有没有到。
老师我这样理解有问题吗？
</div>2019-06-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/17/5d/35/b1eb964a.jpg" width="30px"><span>🐟🐙🐬🐆🦌🦍🐑🦃</span> 👍（8） 💬（1）<div>老师，我想问下NioEndpoint类中为什么把serverSock 的阻塞模式设置为true. 代码上是serceSock.configBlocking（true）.一般我们在选择NIo的时候都是设置为false的</div>2019-06-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/f7/03/8670ff5b.jpg" width="30px"><span>兔子临死前</span> 👍（6） 💬（1）<div>多路复用是指异步阻塞么？异步就是不需要用户线程主动去问，而是内核完成数据操作的时候返回的；而阻塞是发起read调用后要等待内核返回数据，不知道这样理解对不对。。</div>2019-06-16</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/a0/da/4f50f1b2.jpg" width="30px"><span>Knight²º¹⁸</span> 👍（5） 💬（1）<div>老师 ， linux IO模型和Java的IO模型关系是啥？</div>2019-08-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/ea/05/c0d8014d.jpg" width="30px"><span>一道阳光</span> 👍（5） 💬（6）<div>ServerSocketChannel 被设置成阻塞模式，也就是说它是以阻塞的方式接收连接的。
老师:为什么是阻塞的方式？阻塞和非阻塞的区别是什么？这个和多个acceptor有关系吗？阻塞是为了避免共同消费同一个channel吗?</div>2019-06-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/05/7f/a7df049a.jpg" width="30px"><span>Standly</span> 👍（5） 💬（2）<div>serverSock = ServerSocketChannel.open();
serverSock.socket().bind(addr,getAcceptCount());
serverSock.configureBlocking(true);
请假下，这里为什么设置成true了？设置成true和false的区别是什么？
</div>2019-06-15</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/ea/05/c0d8014d.jpg" width="30px"><span>一道阳光</span> 👍（5） 💬（1）<div>同时有多个 Poller 线程在运行，每个 Poller 线程都有自己的 Queue。每个 Poller 线程可能同时被多个 Acceptor 线程调用来注册 PollerEvent。
老师:按照这个意思，有可能一个channel被多个seletor监听，这样的话，重复监听的channel,造成资源浪费。</div>2019-06-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/e9/0b/1171ac71.jpg" width="30px"><span>WL</span> 👍（5） 💬（1）<div>老师有三个问题请教一下
1. tomcat的线程模型是但进程多线程, 还是多进程多线程, 怎样从源码中看到Tomcat是不是多进程的?
2. 对于同步阻塞式的IO模型, 当这个线程阻塞的时候是这个线程让出CPU还是Tomcat进程让出CPU, 如果是线程让出CPU的话, 那tomcat的其他线程是不是还可以用CPU处理它那部分的业务逻辑, 那为什么说非阻塞式IO模型的效率高呢? 
3. 在LimitLatch这个类中Sync类的tryAcquireShared方法中有两行代码是这样的
long newCount = count.incrementAndGet();
if (!released &amp;&amp; newCount &gt; limit)
想请教一下老师为啥单独创建一个newCount变量而不是if (!released &amp;&amp; (count.incrementAndGet()) &gt; limit) 是为可读性更强吗, 还是有啥别的原因?</div>2019-06-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/fa/c9/c75664e9.jpg" width="30px"><span>二两豆腐</span> 👍（5） 💬（1）<div>老师，在“准备数据”阶段，这个阶段数据到底在准备的是什么，“数据就绪”，指的是一种什么样的状态，什么样的数据才算是就绪了啊。</div>2019-06-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/64/86/f5a9403a.jpg" width="30px"><span>yang</span> 👍（4） 💬（1）<div>老师，那我们常说Java中自身的NIO到底是同步非阻塞，还是IO多路复用呢？

作者回复: NIO API可以不用Selector，就是同步非阻塞。使用了Selector就是IO多路复用

老师， 同步非阻塞，不是IO多路复用 不是用Selector实现的吗？</div>2019-08-09</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/6LaITPQ4Lk5fZn8ib1tfsPW8vI9icTuSwAddiajVfibPDiaDvMU2br6ZT7K0LWCKibSQuicT7sIEVmY4K7ibXY0T7UQEiag/132" width="30px"><span>尔东橙</span> 👍（4） 💬（2）<div>老师，操作系统层面的io模型如何和java中的io模型对应</div>2019-07-20</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/DYAIOgq83eoRiaKX0ulEibbbwM4xhjyMeza0Pyp7KO1mqvfJceiaM6ZNtGpXJibI6P2qHGwBP9GKwOt9LgHicHflBXw/132" width="30px"><span>Geek_ebda96</span> 👍（4） 💬（1）<div>老师，你好，请问几个问题
1.limitltach是用来限制应用接收连接的数量，acceptor用来限制系统层面的连接数量，这个限制的先后顺序有关系吗？
2.sreverscoketchannel设置为阻塞模式是指同时只能处理一个客户端连接请求。即同时只能有一个acceptor调用axcept()方法。把客户端的scoketchannel放入poller的队列里面吗？
3.内核空间的接收连接是不是对每个连接都产生一个channel，这个channel就是acceptor里接收方法得到的scoketchanmel，后面的poller在用selector的select方法监听内核是否准备就绪才知道监听内核哪个通道？</div>2019-06-18</li><br/><li><img src="" width="30px"><span>giantbroom</span> 👍（4） 💬（1）<div>从语义上说，Tomcat实现的LimitLatch，跟Semaphore是类似的吧，抛开效率不说，是不是可以简单粗暴的替换为Semaphore，也是工作的吧？</div>2019-06-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/02/96/7505099c.jpg" width="30px"><span>李同学爱学习</span> 👍（3） 💬（3）<div>老师问个问题：countUpOrAwait()获取连接许可的时候，如果超过了限制连接数后会将当前线程添加到aqs等待队列中，这样的话并发请求的连接数上来这个队列会不会被塞爆了（而且是一个线程请求连接许可）？countUpOrAwait的请求是不是线程池控制的？</div>2019-06-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/0b/34/f41d73a4.jpg" width="30px"><span>王盛武</span> 👍（3） 💬（3）<div>请问poller线程数是sever xml那个参数配置？ 暂时想到的是acceptorThreadCount对应acceptor线程数和acceptCount是待连接队列，那poller线程数对应哪个参数？</div>2019-06-15</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/IgjIXs9jjpODTPaOLrms0XOhJ8pxMcaZgtgBrPG6deqsKXv1sPIqkg0faL6X0rtFicJn5Wf7QXTickjYWpmF0V8A/132" width="30px"><span>Geek_28b75e</span> 👍（3） 💬（1）<div>老师，springboot应用程序之所以启动之后没有立即结束，本质原因就在于tomcat启动后，socket的accept（）方法阻塞监听吧？再加上此方法在死循环内部，用户线程不死</div>2019-06-14</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/IgjIXs9jjpODTPaOLrms0XOhJ8pxMcaZgtgBrPG6deqsKXv1sPIqkg0faL6X0rtFicJn5Wf7QXTickjYWpmF0V8A/132" width="30px"><span>Geek_28b75e</span> 👍（3） 💬（2）<div>老师，对于一个客户端来说就发起一次请求（附带了请求参数），1.那么对于客户端和服务端首先需要完成三次握手，才能处理具体请求吗？
2.三次握手和sellctor有交互吗？还是说处理具体请求时才和sellector有联系？

希望老师能用一个具体的请求讲解一下</div>2019-06-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/67/8a/babd74dc.jpg" width="30px"><span>锦</span> 👍（3） 💬（2）<div>NioEndpoint是同步非阻塞模型，只不过使用io多路复用技术实现的。优点是能有效减少线程的使用。那么问题来了，selector是使用哪种技术实现的呢？select,poll,epoll,iocp?
LimitLatch使用AQS实现最大连接数限制，问题是AQS如何使线程阻塞在线程队列的呢？
为什么要设计poller呢？连接建立后把新建的读写Socket扔到线程池不行么？这种可能比较适合异步io模型吧？
Socket与线程是稳定的多对一的关系么？


</div>2019-06-12</li><br/>
</ul>