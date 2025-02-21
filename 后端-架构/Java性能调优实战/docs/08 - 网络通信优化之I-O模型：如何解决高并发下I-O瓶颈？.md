你好，我是刘超。

提到Java I/O，相信你一定不陌生。你可能使用I/O操作读写文件，也可能使用它实现Socket的信息传输…这些都是我们在系统中最常遇到的和I/O有关的操作。

我们都知道，I/O的速度要比内存速度慢，尤其是在现在这个大数据时代背景下，I/O的性能问题更是尤为突出，I/O读写已经成为很多应用场景下的系统性能瓶颈，不容我们忽视。

今天，我们就来深入了解下Java I/O在高并发、大数据业务场景下暴露出的性能问题，从源头入手，学习优化方法。

## 什么是I/O

I/O是机器获取和交换信息的主要渠道，而流是完成I/O操作的主要方式。

在计算机中，流是一种信息的转换。流是有序的，因此相对于某一机器或者应用程序而言，我们通常把机器或者应用程序接收外界的信息称为输入流（InputStream），从机器或者应用程序向外输出的信息称为输出流（OutputStream），合称为输入/输出流（I/O Streams）。

机器间或程序间在进行信息交换或者数据交换时，总是先将对象或数据转换为某种形式的流，再通过流的传输，到达指定机器或程序后，再将流转换为对象数据。因此，流就可以被看作是一种数据的载体，通过它可以实现数据交换和传输。
<div><strong>精选留言（30）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/0f/b4/3b/a1f7e3a4.jpg" width="30px"><span>ZOU志伟</span> 👍（74） 💬（4）<div>老师，为什么要字符流还是没懂</div>2019-06-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/d8/ee/6e7c2264.jpg" width="30px"><span>Only now</span> 👍（53） 💬（3）<div>老师能不能讲讲DMA和Channel的区别, DMA需要占用总线, 那么Channel是如何跳过总线向内存传输数据的?</div>2019-06-06</li><br/><li><img src="https://wx.qlogo.cn/mmopen/vi_32/DYAIOgq83eotSSnZic41tGkbflx0ogIg3ia6g2muFY1hCgosL2t3icZm7I8Ax1hcv1jNgr6vrZ53dpBuGhaoc6DKg/132" width="30px"><span>张学磊</span> 👍（50） 💬（1）<div>在Linux中，AIO并未真正使用操作系统所提供的异步I&#47;O，它仍然使用poll或epoll，并将API封装为异步I&#47;O的样子，但是其本质仍然是同步非阻塞I&#47;O，加上第三方产品的出现，Java网络编程明显落后，所以没有成为主流</div>2019-06-06</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/a6/10/3ff2e1a5.jpg" width="30px"><span>皮皮</span> 👍（28） 💬（1）<div>老师，个人觉得本期的内容讲的稍微浅了一点，关于IO的几种常见模型可以配图讲一下的，另外就是linux下的select，poll，epoll的对比应用场景。最重要的目前用的最多的IO多路复用可以深入讲一下的。</div>2019-06-06</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/1b/a3/64a37f40.jpg" width="30px"><span>小兵</span> 👍（14） 💬（1）<div>很多知识linux 网络 I&#47;O模型底层原理，零拷贝技术等深入讲一下，毕竟学Java性能调优的学员都是有几年工作经验的， 希望老师后面能专门针对这次io 出个补充，这一讲比较不够深入。</div>2019-06-07</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/79/4b/740f91ca.jpg" width="30px"><span>-W.LI-</span> 👍（13） 💬（6）<div>老师好!隔壁的李好双老师说一次普通IO需要要进过六次拷贝。
网卡-&gt;内核-&gt;临时本地内存-&gt;堆内存-&gt;临时本地内存-&gt;内核-&gt;网卡。
directbfuffer下
网卡-&gt;内核-&gt;本地内存-&gt;内核-&gt;网卡
ARP下C直接调用
文件-&gt;内核-&gt;网卡。
李老师说的对么?
本地内存和堆内存都是在用户空间的是么?</div>2019-06-20</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/SM4fwn9uFicXU8cQ1rNF2LQdKNbZI1FX1jmdwaE2MTrBawbugj4TQKjMKWG0sGbmqQickyARXZFS8NZtobvoWTHA/132" width="30px"><span>td901105</span> 👍（10） 💬（3）<div>在少量连接请求的情况下，使用这种方式没有问题，响应速度也很高。但在发生大量连接请求时，就需要创建大量监听线程，这时如果线程没有数据就绪就会被挂起，然后进入阻塞状态。一旦发生线程阻塞，这些线程将会不断地抢夺 CPU 资源，从而导致大量的 CPU 上下文切换，增加系统的性能开销。

后面一句一旦发生线程阻塞，这些线程会不断的抢夺CPU资源，从而导致大量的CPU进行上下文切换，增加系统开销，这一句不是太明白，能解释一下吗？阻塞线程不是不会占用CPU资源吗？</div>2019-12-04</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/67/f4/9a1feb59.jpg" width="30px"><span>钱</span> 👍（10） 💬（2）<div>课后思考及问题
1本文核心观点
1-1：JAVA IO操作为啥分为字节流和字符流？我们知道字符到字节必须经过转码，这个过程非常耗时，如果我们不知道编码类型就很容易出现乱码问题。所以 I&#47;O 流提供了一个直接操作字符的接口，方便我们平时对字符进行流操作。
有个疑问，字符流虽然在不知道其编码类型的情况下可以操作，不过一旦需要进行网络传输了，还是必须要知道的？
1-2：一次读取数据的操作流程，如下
用户空间—请求数据—内核空间—请求数据—数据存储设备—响应数据—内核空间—响应数据—用户空间，应用程序从用户空间的数据缓存区中读取数据，数据以字节流的形式流转。这种方式数据经过了两次复制过程，比较耗性能。
1-3：传统IO耗性能的地方主要有两点，一是数据从从存储设备到应用程序中经历了两次复制，二是数据的处理方式是阻塞式的
1-4：NIO快就快在解决了传统IO的两个耗性能的问题，一是减少复制次数，二是数据处理线程不再阻塞，为此增加了缓存区+通道+多路复用选择器+操作系统数据缓存区
对比来看，感觉老师讲的有点凌乱，IO网络通信模型，我在很多的课程上都学过，这个几乎讲到高性能这一块是必讲的，极客时间里有好几个专栏里也都有讲，大概原理还行，不过体系和细致成度一般，可能是篇幅有限吧!
我见过最通俗易懂的讲解就是netty权威指南的李林峰，用了好几章来讲解这一块的内容。
他从IO的历史演进来讲，一个个IO通信模型是怎么来的？前一个有什么问题？后一个基本是为了解决前一个的问题而来的，以及具体是怎么解决的？
磁盘或网络IO由于其内部结构决定和内存、各级缓存、CUP的速度有巨大的鸿沟，写操作系统的大神们和JDK的大神都清楚，所以，他们也都在绞尽脑汁来通过其他方式来尽量的解决这些问题。
希望他们的脑汁没没白绞，真心能明白他们绞尽脑汁后都产生了什么牛逼的方案。
非阻塞、零拷贝、多路复用选择器、Reactor、Preactor、DMA、epoll、通道这些概念有些理解啦有些还没，不过性能优化的原则没变还是那一套。
</div>2019-09-07</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/b7/ba/ae4cabd8.jpg" width="30px"><span>仙道</span> 👍（8） 💬（1）<div>有两个地方理解不了，请老师指点一下。
1.传统io请求数据没有的话就会挂起进入阻塞状态，既然进入了阻塞状态文中为什么还会说会继续强悍cpu。
2，传统io对文件边读边处理，NIO一次性将文件读到缓冲区，就这样的话问什么说NIO要快？我觉得单是读取的时间花费的是一样的</div>2019-08-16</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/18/3a/c8/7e75d165.jpg" width="30px"><span>Haies</span> 👍（6） 💬（2）<div>讲的很精炼，不过有三个问题没明白
1.图2的directbuffer是不是临时直接内存，和文中提到的DirectBuffer应该不是一回事吧。
2.Chanel有自己的处理器，这个何解？
3.传统I&#47;O使用buffer后，是不是处理单位也变成块了，怎么可以优化阻塞的问题呢，不太明白？</div>2019-11-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/2c/87/9a3d80dc.jpg" width="30px"><span>昨夜的柠檬</span> 👍（4） 💬（2）<div>文中说，多线程阻塞时，会占用大量CPU资源。线程阻塞应该会让出CPU吧？</div>2020-03-08</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTJYEdMwBDUC6lDsNOFlRxdOXkUheMKUTWpYtK1KRuGGicS2dwyrKiasicvk1A1A8dExlRXkx5iaX4Xdjw/132" width="30px"><span>天星之主</span> 👍（3） 💬（3）<div>“DirectBuffe直接将步骤简化为从内核空间复制到外部设备，减少了数据拷贝”，direct buffer申请的非堆内存，只是不受JVM管控，不应该还是用户态的内存吗</div>2019-11-07</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/a0/cb/aab3b3e7.jpg" width="30px"><span>张三丰</span> 👍（2） 💬（1）<div>如果单纯使用 Java 堆内存进行数据拷贝，当拷贝的数据量比较大的情况下，Java 堆的 GC 压力会比较大，而使用非堆内存可以减低 GC 的压力。




为何GC压力会比较大呢？只能说是没法回收导致内存泄漏吧。</div>2020-04-07</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/61/78/e7aa4e04.jpg" width="30px"><span>al-byte</span> 👍（2） 💬（1）<div>我们可以在注册 Channel 时设置该通道为非阻塞，当 Channel 上没有 I&#47;O 操作时，该线程就不会一直等待了，而是会不断轮询所有 Channel，从而避免发生阻塞。
如果一个Channel上I&#47;O耗时很长是不是后续的Channel就被阻塞了？</div>2019-06-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/41/87/46d7e1c2.jpg" width="30px"><span>Better me</span> 👍（1） 💬（1）<div>老师在评论中的下面这段话
阻塞线程在阻塞状态是不会占用CPU资源的，但是会被唤醒争夺CPU资源。操作系统将CPU轮流分配给线程任务，当线程数量越多的时候，当某个线程在规定的时间片运行完之后，会被其他线程抢夺CPU资源，此时会导致上下文切换。抢夺越激烈，上下文切换就越频繁。

这里抢夺越激烈，上下文切换越频繁有点不太理解，如果只是单次抢夺操作，最后不都只有一个线程抢夺到CPU从而进行一次上下文切换吗？还是这里是以抢夺资源的这整段时间维度去衡量理解的</div>2020-05-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1c/af/6e/30fb83f1.jpg" width="30px"><span>xaviers</span> 👍（1） 💬（2）<div>老师，有个疑问。
Buffer 可以将文件一次性读入内存再做后续处理，而传统的方式是边读文件边处理数据。
按说边读文件边处理应该更快呀</div>2020-04-25</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/e0/a1/d1c6f0a7.jpg" width="30px"><span>袁林</span> 👍（1） 💬（1）<div>根据 ‘使用 DirectBuffer 减少内存复制’ 这段描述 DirectBuffer 申请的应该是内核的内存，这是如何实现的？unix使用的是哪些系统调用？
还请解答</div>2019-08-07</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/09/d6/5f366427.jpg" width="30px"><span>码农Kevin亮</span> 👍（1） 💬（1）<div>
请问老师，我理解传统bio之所以慢是因为它要等待数据从磁盘到内核空间再到用户空间，由于经过两次复制数据所以慢。
我没太理解nio是快在哪？只有用户空间直接到磁盘一次的复制？具体是怎么实现的呢？</div>2019-08-05</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTJwQvLGE4dMsF4JU0svW3DtGbodpjskbY65FdwF13JdtBYZfgL2IXHlHrdejWzHdjT0RibEIfib4QYA/132" width="30px"><span>知行合一</span> 👍（1） 💬（1）<div>思考题：是因为会很耗费cpu吗？</div>2019-06-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/96/4e/2acbc3a8.jpg" width="30px"><span>vvsuperman</span> 👍（1） 💬（1）<div>建议加写例子，比如tomcat用的io造成阻塞之类，实例分析等</div>2019-06-06</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/79/4b/740f91ca.jpg" width="30px"><span>-W.LI-</span> 👍（1） 💬（1）<div>老师好!能说下哪些操作需要在用户态下完成么?正常的代码运行用户态就可以了是吗?
1.创建selector
2.创建serverSockekChannel
3.OP_ACCEPT事件注册到selector中
4.监听到OP_ACCEPT事件
5.创建channel
6.OP_READ事件注册到selector中
7.监听到READ事件
8.从channel中读数据
读的时候需要先切换到内核模式，复制在内核空间，然后从内核空间复制到用户空间。
9.处理数据 
10.write:用户模式切换到内核模式，从用户空间复制到内核空间，再从内核空间发送到IO网络上。
1-7步里面有哪些操作需要在内核模式下执行的么?

第8和10我是不是理解错了?
DMA啥时候起作用啊?

JVM的内存属于用户空间是吧，directBuffer直接申请的物理内存，是属于特殊的用户空间么。内核模式直接往那里写。kafka的0拷贝和directbuffer一个意思么?╯﹏╰都不知道
</div>2019-06-06</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/a0/cb/aab3b3e7.jpg" width="30px"><span>张三丰</span> 👍（0） 💬（1）<div>传统的 I&#47;O 即使使用了缓冲块，依然存在阻塞问题。由于线程池线程数量有限，一旦发生大量并发请求，超过最大数量的线程就只能等待


奇怪了 传统的IO和线程池有什么关系？？</div>2020-04-07</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTKibjS2ia1BldGnI6gGcy89W5y3009dMXpsibpkWMIWK9Tks1omwT1HQjibuKWibcmegrpXztvB1BbrOaA/132" width="30px"><span>greekw</span> 👍（0） 💬（1）<div>老师，NIO模型里面的多路复用的线程机制能否讲下？还有零拷贝是怎么实现的？</div>2019-10-20</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/DYAIOgq83eqOn7k48KXia5nvt5VO0x0Fh7SN5MHrbglBAEUVicdRBFpFU3icvNmpjVXDaUVjY0vvic9OrTV5mBRqVQ/132" width="30px"><span>没有小名的曲儿</span> 👍（0） 💬（4）<div>老师，我想请教一个问题，对于向服务器上传多张图片，服务器接收到后进行压缩或者合成pdf等类似的io操作，会占用很大的资源，我试着用线程池来规避数量可服务器还是承受不住这种压力，对于这种耗时比较长的操作您有什么建议吗</div>2019-08-19</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTLXibzeMXGoTbe4me8gUjMYYMMdrz8XLJvqadmic3AQqbNvKn8Q1udpPuV83zt20ibSlSiciaqKnH02aDg/132" width="30px"><span>Geek_94aebf</span> 👍（0） 💬（2）<div>Java后台需求要返回几百上千条数据，数据是实时变化的，每次返回数据有几百k到几m不等，非常耗费网络带宽，现在单机带宽30m，该从哪些方面优化?</div>2019-08-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/a0/da/4f50f1b2.jpg" width="30px"><span>Knight²º¹⁸</span> 👍（0） 💬（1）<div>Java的IO模型和操作系统的关系是啥？</div>2019-08-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/8f/b1/7b697ed4.jpg" width="30px"><span>晓晨同学</span> 👍（0） 💬（1）<div>请问老师，传统io中的buffer和nio中的buffer同样都在用户内存缓冲区，那么有什么区别呢</div>2019-08-06</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/d4/70/f093eaf0.jpg" width="30px"><span>飞鱼</span> 👍（0） 💬（1）<div>老师，请教个问题，如果是长连接下，高并发应该怎么样设计方案更合理呢，谢谢</div>2019-07-02</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/DYAIOgq83eqWJ2sP28ZpDp6uTCXOzpd1RYK4Lkf8ZspaNNwnqzVAN7we2rk7YPia3VDjCR0b3CAc3vVhGL8kEZg/132" width="30px"><span>Geek_37bdff</span> 👍（0） 💬（1）<div>老师，您好，能通俗解释一下什么是同步阻塞，异步阻塞，同步非阻塞，异步非阻塞这些概念不，还有就是nio是属于同步非阻塞还是异步非阻塞，为什么</div>2019-06-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/05/7f/a7df049a.jpg" width="30px"><span>Standly</span> 👍（0） 💬（1）<div>从文章的描述我猜测DirectBuffer属于内核空间的内存，但java作为用户进城是如何操作内核空间内存的呢？</div>2019-06-09</li><br/>
</ul>