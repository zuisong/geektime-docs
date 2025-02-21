你好，我是何小锋。在上一讲我讲解了RPC框架中的序列化，通过上一讲，我们知道由于网络传输的数据都是二进制数据，所以我们要传递对象，就必须将对象进行序列化，而RPC框架在序列化的选择上，我们更关注序列化协议的安全性、通用性、兼容性，其次才关注序列化协议的性能、效率、空间开销。承接上一讲，这一讲，我要专门讲解下RPC框架中的网络通信，这也是我们在开篇词中就强调过的重要内容。

那么网络通信在RPC调用中起到什么作用呢？

我在[\[第 01 讲\]](https://time.geekbang.org/column/article/199650) 中讲过，RPC是解决进程间通信的一种方式。一次RPC调用，本质就是服务消费者与服务提供者间的一次网络信息交换的过程。服务调用者通过网络IO发送一条请求消息，服务提供者接收并解析，处理完相关的业务逻辑之后，再发送一条响应消息给服务调用者，服务调用者接收并解析响应消息，处理完相关的响应逻辑，一次RPC调用便结束了。可以说，网络通信是整个RPC调用流程的基础。

## 常见的网络IO模型

那说到网络通信，就不得不提一下网络IO模型。为什么要讲网络IO模型呢？因为所谓的两台PC机之间的网络通信，实际上就是两台PC机对网络IO的操作。

常见的网络IO模型分为四种：同步阻塞IO（BIO）、同步非阻塞IO（NIO）、IO多路复用和异步非阻塞IO（AIO）。在这四种IO模型中，只有AIO为异步IO，其他都是同步IO。
<div><strong>精选留言（30）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/10/0f/bf/ee93c4cf.jpg" width="30px"><span>雨霖铃声声慢</span> 👍（66） 💬（8）<div>IO多路复用分为select，poll和epoll，文中描述的应该是select的过程，nigix，redis等使用的是epoll，所以光只看这个文章的话会比较迷惑，文中写的太粗了。
对于课后思考，目前很多的主流的需要通信的中间件都差不多都实现了零拷贝，如Kfaka，RocketMQ等。kafka的零拷贝是通过java.nio.channels.FileChannel中的transferTo方法来实现的，transferTo方法底层是基于操作系统的sendfile这个system call来实现的。</div>2020-03-01</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/51/b4/0d402ae8.jpg" width="30px"><span>南桥畂翊</span> 👍（30） 💬（1）<div>所谓的零拷贝，就是取消用户空间与内核空间之间的数据拷贝操作，应用进程每一次的读写操作，可以通过一种方式，直接将数据写入内核或从内核中读取数据，再通过 DMA 将内核中的数据拷贝到网卡，或将网卡中的数据 copy 到内核。


老师，上述说直接将数据写入内核或从内核中读取数据，这部分内存不是属于内核态空间的吧？应该说只是一块物理内存，用户态虚拟地址和内核态虚拟地址都作了页表映射</div>2020-03-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1d/79/04/748ee8c9.jpg" width="30px"><span>想出家的小和尚</span> 👍（4） 💬（1）<div>老师，直接内存给我的概念很模糊，他指的到底是什么？和jvm中的堆内内存，堆外内存，用户空间，内核空间有什么关系？</div>2020-03-31</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/c2/fe/038a076e.jpg" width="30px"><span>阿卧</span> 👍（3） 💬（2）<div>阻塞IO：
1. 阻塞等待：多线程进行IO读取，需要阻塞等待
2. 内存两次拷贝：从设备（磁盘或者网络）拷贝到用户空间，再从用户空间拷贝到内核空间
IO多路复用
1. 一个复用器（selector）监听有多个通道（channel）。实现非阻塞式IO读取、写入
2. 内存直接拷贝（derict buffers），直接从用户空间拷贝到内核空间</div>2020-03-01</li><br/><li><img src="" width="30px"><span>嘻嘻</span> 👍（2） 💬（2）<div>老师，个人理解netty 堆在内存还是在用户态的，还是要拷贝到内核态啊，为啥零拷贝了？</div>2020-04-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/19/ca/82/85f6a1a2.jpg" width="30px"><span>番茄炒西红柿</span> 👍（2） 💬（3）<div>问一下nio和io多路复用的区别（我认为没区别吧），io多路复用不就是为了实现同步非阻塞？</div>2020-04-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/01/37/12e4c9c9.jpg" width="30px"><span>高源</span> 👍（2） 💬（1）<div>老师你讲的netty零拷贝不光做到在用户级别的，还有操作系统级别的，那老师如果我想理解它的怎么做的，因为它源代码看的迷糊，怎样把他实现的高技巧和方法运用到自己这块,灵活运用</div>2020-02-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/75/b0/17f46582.jpg" width="30px"><span>Mike</span> 👍（1） 💬（1）<div>RocketMq中对消息的读取也用到了零拷贝</div>2020-03-31</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/c1/3a/2ce09963.jpg" width="30px"><span>张先生</span> 👍（1） 💬（1）<div>1.我的理解netty对应用层的零拷贝优化就是把做个tcp包做合并来减少频繁的cpu内核交互，但是cpu内核应该也有个大小限制吧？
2.零拷贝只是优化了服务器的开销，对于传输层并没有什么优化吧，因为传输层传输的包大小会受链路上路由可接收的包大小决定拆多少个包</div>2020-02-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/78/d3/1dc40aa2.jpg" width="30px"><span>Jonah</span> 👍（0） 💬（1）<div>典型的Kafka，Rocketmq等</div>2020-04-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/b7/00/12149f4e.jpg" width="30px"><span>郭刚</span> 👍（0） 💬（1）<div>请问一下，RPC调用本地和远程机器之间的带宽是不是千兆起？</div>2020-03-25</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/DYAIOgq83epY2JtiahsBz4LK1k00DbYoR2Zk56wnYaoBfP63v5X3Xu1kuH1ethAnMOMu6vT9eKQSqHqn3HrTK9Q/132" width="30px"><span>Geek_7d1d6d</span> 👍（0） 💬（1）<div>老师请教一个问题呗：“对数据包的分割和合并”跟咱们说的在传输层说的分组是一个东西吗</div>2020-03-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/81/e6/6cafed37.jpg" width="30px"><span>旅途</span> 👍（0） 💬（2）<div>老师 用户空间指的是jvm吗？
</div>2020-03-07</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/39/fa/a7edbc72.jpg" width="30px"><span>安排</span> 👍（0） 💬（2）<div>select监视一批socket文件描述符，当某个socket可读或者可写了，那么调用select的线程会被从阻塞中唤醒。这个过程的底层细节是啥啊？比如网卡中断收包，然后中断调用协议栈处理，一直到传输层，然后到socket，发现这个socket是被select监视的，然后将调用select的进程从阻塞队列放到可运行队列，最后在调度点被调度运行。这样理解对吗？</div>2020-03-01</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTKCGgico4wOAghiaVXDAhGZr8EYpJOk3AdrePWaHLsWzPNk0tMzax5ibaeztcmysNnxS53ibuAlPjHvxg/132" width="30px"><span>小脚丫</span> 👍（0） 💬（5）<div>何老师您好，我是京东员工，看到您这章关于零拷贝的介绍，突然想起来个之前使用jmq的问题想请教您下，Jmq抛出了ERROR com.jd.jmq.common.network.netty.NettyTransport - netty channel exception 10.194.143.76:50088
io.netty.handler.codec.DecoderException: java.lang.IndexOutOfBoundsException这个异常，导致我们应用的堆内存里都是heapbytebuffer这个对象，占用了几个G，之后导致不停的full gc。我们的jmq没有使用直接内存吗？ 从现象看，感觉数据都被拷贝到了堆内存中。</div>2020-02-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/4c/83/7788fc66.jpg" width="30px"><span>Simon</span> 👍（0） 💬（1）<div>课后思考: RocketMQ使用mmap实现零拷贝</div>2020-02-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/18/7e/0e/b828909c.jpg" width="30px"><span>益</span> 👍（0） 💬（4）<div>请问.NET Core上有与Netty框架类似的网络通信框架吗？
请教老师，如果选择用gRPC开发接口服务，从底层原理角度，Java和.NET Core哪个更好呢？</div>2020-02-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/17/9e/42/ab4f65c8.jpg" width="30px"><span>པག་ཏོན་།</span> 👍（20） 💬（0）<div>写的非常粗，可见作者对网络知识了解并不深入，买这个课是真的交了智商税</div>2021-10-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/57/4f/6fb51ff1.jpg" width="30px"><span>奕</span> 👍（14） 💬（11）<div>老师，我理解的IO多路复用，是应用线程一直再调用select，读取内核准备好数据的socket，所以应用线程是阻塞的，但是老师你文章中举的那个例子，不用应用(用户)打电话去询问的，而是内核(餐馆)打电话通知的，在这期间你还可以去干其他的事情，我感觉你这个案例是异步IO非阻塞的</div>2020-02-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/67/0e/c77ad9b1.jpg" width="30px"><span>eason2017</span> 👍（13） 💬（3）<div>Nginx  sendfile方式
Kafka  应该是mmap方式，适合小文件</div>2020-03-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/07/d2/0d7ee298.jpg" width="30px"><span>惘 闻</span> 👍（9） 💬（0）<div>感觉在零拷贝这块讲的不细致,没有图来展示到底是那块做的优化,单单文字描述让人有点误解,而且对比另外几个课程讲解零拷贝的感觉这块老师似乎还讲错了,用户态到内核态的零拷贝.看完这节课疑问更多了....难受</div>2021-02-01</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/36/e7/c9eda4e7.jpg" width="30px"><span>stonyliu</span> 👍（9） 💬（1）<div>零拷贝这块对于一个非JAVA程序员来说就等于没说啥，给给题目自己查吧</div>2020-03-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/c7/e6/11f21cb4.jpg" width="30px"><span>川杰</span> 👍（5） 💬（2）<div>老师好，有句话不大理解：但它最大的优势在于，用户可以在一个线程内同时处理多个socket的IO请求；
1、这个线程指的是维护select的线程吗？
2、为什么用户可以在一个线程内处理多个socket的IO请求？我理解，这里的用户，应该指的是客户端调用方，那么多个socket，应该是指，其他客户端调用方发送过来的、且IO还未准备好的socket，都被放在了这个select里，然后因为这个用户的select调用，某个IO完成的socket被返回了。如果我理解的没错，那应该还是，只处理了一个请求啊？（那个IO完成的socket）

3、Reactor模式是为了应对高并发场景的，假设一个极端情况：请求A过来，处理IO稍微花了点时间，后面就没有任何请求过来了，那么请求A是不是永远得不到响应了？因为Reactor是时间驱动的，请求A的socket被放在select里了，没有新的事件触发它去返回；
还是说内核会监视，处理完之后就主动返回给客户端？
如果内核会主动返回给客户端，那么为什么说：当用户发起了select调用，进程会被阻塞，当发现该select负责的socket有准备好的数据时才返回，之后才发起一次read。
麻烦解答下，谢谢！</div>2020-02-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/21/2f/37c96c64.jpg" width="30px"><span>陈掌门</span> 👍（4） 💬（0）<div>讲的真好，全是干货</div>2020-05-15</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/19/06/7e/daa187da.jpg" width="30px"><span>Q.E.D</span> 👍（4） 💬（4）<div>tcp不是流协议吗，为什么会有粘包这种说法。</div>2020-03-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/07/d2/0d7ee298.jpg" width="30px"><span>惘 闻</span> 👍（3） 💬（0）<div>缓冲区也是属于用户空间的啊,从缓冲区到内核空间还是需要一次拷贝的啊.为什么这里就说是取消了.只有sendfile可以做到取消用户空间到内核空间的数据拷贝吧?啊啊啊啊,能不能再精致严谨一点呀.</div>2021-02-01</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/67/f4/9a1feb59.jpg" width="30px"><span>钱</span> 👍（3） 💬（0）<div>网络IO通信模型和零拷贝，这两个知识点在不同的课程上都有讲解，重要性不言而喻，虽然讲解的都算是高手吧！每个人的讲解方式都不一样，理解起来也是有的容易有的费劲。有此推测完全把这块都系统的弄明白，也能讲出来让他人弄明白是比较困难的。不知道别人什么感受，个人觉得何老师讲解的不是很细致和全面，我不太容量理解 之前觉得这块自己理解了，现在发现并没有。我需要找本书，在好好学习一下。

不过快的原理还是比较容易理解的，不同的网络IO通信模型之所以，有快慢且相差很大，主要是因为，一个是否消除或减少了线程阻塞等待的过程，另一个是否实现了一个链接供多个线程通信复用。零拷贝之所以快是因为它在做减法，省去一次拷贝的动作，少做事尤其是少做费时间的事情速度自然就快起来了。不过具体到每一步，他们是怎么做到的还有待继续学习，计算机是比较复杂的，光理解信息是怎么表示？怎么存储？怎么传输？怎么运算？都比较烧脑了。</div>2020-05-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/f8/ba/37c24a08.jpg" width="30px"><span>学习学习学习学习学习学习学习</span> 👍（2） 💬（1）<div>**网络io中的零拷贝**

系统内核处理 IO 操作分为两个阶段——等待数据和拷贝数据。

- 等待数据，就是系统内核在等待网卡接收到数据后，把数据写到内核中
- 拷贝数据，就是系统内核在获取到数据后，将数据拷贝到用户进程的空间中。

应用进程的每一次写操作，都会把数据写到用户空间的缓冲区中，再由 CPU 将数据拷贝到系统内核的缓冲区中，之后再由 DMA 将这份数据拷贝到网卡中，最后由网卡发送出去。一次写操作数据要拷贝两次才能通过网卡发送出去

- 零拷贝技术
    - 零拷贝，就是取消用户空间与内核空间之间的数据拷贝操作，应用进程每一次的读写操作，都可以通过一种方式，让应用进程向用户空间写入或者读取数据，就如同直接向内核空间写入或者读取数据一样，再通过 DMA 将内核中的数据拷贝到网卡，或将网卡中的数据 copy 到内核。
- 零拷贝实现
    - mmap+write 方式，核心原理是通过虚拟内存来解决的
    - sendfile 方式
- Netty零拷贝实现：
    - 用户空间数据操作零拷贝优化
        - 收到数据包后，在对数据包进行处理时，需要根据协议，处理数据包，在进行处理时，免不了需要进行在用户空间内部内存中进行拷贝处理，Netty就是在用户空间中对数据操作进行优化
        - Netty 提供了 CompositeByteBuf 类，它可以将多个 ByteBuf 合并为一个逻辑上的  ByteBuf，避免了各个 ByteBuf 之间的拷贝。
        - ByteBuf 支持 slice 操作，因此可以将 ByteBuf 分解为多个共享同一个存储区域的 ByteBuf，避免了内存的拷贝。
        - 通过 wrap 操作，我们可以将 byte[] 数组、ByteBuf、ByteBuffer  等包装成一个 Netty ByteBuf 对象, 进而避免拷贝操作。
    - 用户空间与内核空间之间零拷贝优化
        - Netty  的  ByteBuffer 可以采用 Direct Buffers，使用堆外直接内存进行 Socket 的读写操作，效果和虚拟内存所实现的效果是一样的。
        - Netty  还提供  FileRegion  中包装  NIO  的  FileChannel.transferTo()  方法实现了零拷贝，这与 Linux  中的  sendfile  方式在原理上也是一样的。</div>2021-05-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/e1/5a/d2081f1c.jpg" width="30px"><span>徐敏</span> 👍（1） 💬（0）<div>看这个课程，其实是来看一些思路的，没点基础真不行。</div>2022-06-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/ec/e0/d072d6f0.jpg" width="30px"><span>bigdudo</span> 👍（1） 💬（0）<div>前面的BIO，是一个连接一个线程的处理方式，每条线程自己去监听自己的连接，自己去阻塞并accpet。在这里多路复用，可以理解为是一种批量处理的方式，在一条线程里批量处理多个连接，哪个连接有连接上来了，就向用户进程返回有效的连接。这就是一开始说的多路复用的概念，一个线程处理多个连接。多路复用后面的优化迭代也主要是在批量处理这块的数据模型选型和fd有连接上来的回调的不断优化，从纯遍历方式的select（bitmap承载，最大1024）和poll（数组承载，相对于select，解决了1024有限连接弊端），到cpu终端信号回调的epoll（红黑树管理，有效连接获取放到双向链表并返回个用户进程） 至于用户进程这边怎么处理，是单线程一个一个处理recv&#47;send 还是多线程一个线程一个连接的处理recv&#47;send，这是用户进程的处理方式，也是属于我们常知道的netty这些io中间件的范畴（当然最重要的也是包括基础IO类型的选型也是属于此）。</div>2021-12-03</li><br/>
</ul>