你好，我是刘超。专栏上线已经有20多天的时间了，首先要感谢各位同学的积极留言，交流的过程使我也收获良好。

综合查看完近期的留言以后，我的第一篇答疑课堂就顺势诞生了。我将继续讲解I/O优化，对大家在08讲中提到的内容做重点补充，并延伸一些有关I/O的知识点，更多结合实际场景进行分享。话不多说，我们马上切入正题。

Tomcat中经常被提到的一个调优就是修改线程的I/O模型。Tomcat 8.5版本之前，默认情况下使用的是BIO线程模型，如果在高负载、高并发的场景下，可以通过设置NIO线程模型，来提高系统的网络通信性能。

我们可以通过一个性能对比测试来看看在高负载或高并发的情况下，BIO和NIO通信性能（这里用页面请求模拟多I/O读写操作的请求）：

![](https://static001.geekbang.org/resource/image/3e/4a/3e66a63ce9f0d9722005f78fa960244a.png?wh=934%2A518)

![](https://static001.geekbang.org/resource/image/3e/74/3e1d942b7e5e09ad6e4757b8d5cbe274.png?wh=935%2A521)

**测试结果：Tomcat在I/O读写操作比较多的情况下，使用NIO线程模型有明显的优势。**

Tomcat中看似一个简单的配置，其中却包含了大量的优化升级知识点。下面我们就从底层的网络I/O模型优化出发，再到内存拷贝优化和线程模型优化，深入分析下Tomcat、Netty等通信框架是如何通过优化I/O来提高系统性能的。

## 网络I/O模型优化

网络通信中，最底层的就是内核中的网络I/O模型了。随着技术的发展，操作系统内核的网络模型衍生出了五种I/O模型，《UNIX网络编程》一书将这五种I/O模型分为阻塞式I/O、非阻塞式I/O、I/O复用、信号驱动式I/O和异步I/O。每一种I/O模型的出现，都是基于前一种I/O模型的优化升级。
<div><strong>精选留言（30）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/12/79/4b/740f91ca.jpg" width="30px"><span>-W.LI-</span> 👍（29） 💬（1）<div>老师好!万分感觉，写的非常非常好谢谢。不过开心的同时，好多没看懂:-(先讲下我的理解吧。
阻塞IO:调用read()线程阻塞了
非阻塞IO:调用read()马上拿到一个数据未就绪，或者就绪。
I&#47;O多路复用:selector线程阻塞，channel非阻塞，用阻塞一个selector线程换了多个channel了非阻塞。select()函数基于数组，fd个数限制1024，poll()函数也是基于数组但是fd数目无限制。都会负责所有的fd(未就绪的开销浪了)，
epll()基于红黑数实现，fd无大小限制，平衡二叉数插入删除效率高。
信号驱动模式IO:对IO多路复用进一步优化，selector也非阻塞了。但是sign信号无法区分多信号源。所以socket未使用这种，只有在单一信号模型上才能应用。
异步IO模型:真正的非阻塞IO，其实前面的四种IO都不是真正的非阻塞IO，他们的非阻塞只是，从网络或者内存磁盘到内核空间的非阻塞，调用read()后还需要从内核拷贝到用户空间。异步IO基于回调，这一步也非阻塞了，从内核拷贝到用户空间后才通知用户进程。
能我是这么理解的前半断，有理解错的请老师指正谢谢。后半断没看完。</div>2019-06-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/54/9a/76c0af70.jpg" width="30px"><span>每天晒白牙</span> 👍（16） 💬（1）<div>老师您在介绍Reactor线程模型的时候，关于多线程Reactor线程模型和主从Reactor线程模型，我有不同的理解。您画的多线程模型，其中读写交给了线程池，我在看Doug Lea的 《Scalable in java》中画的图和代码示例，读写事件还是由Reactor线程处理，只把业务处理交给了线程池。主从模型也是同样的，Reactor主线程处理连接，Reactor从线程池处理读写事件，业务交给单独的线程池处理。
还望老师指点</div>2019-06-15</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/79/4b/740f91ca.jpg" width="30px"><span>-W.LI-</span> 👍（15） 💬（3）<div>老师好对Reacktor的三种模式还是理解不太好。帮忙看看哪里有问题
单线程模型:一个selector同时监听accept,事件和read事件。检测到就在一个线程处理。
多线程模型:一个线程监听accept事件，创建channel注册到selector上，检听到Read等事件从线程池中获取线程处理。
主从模式:没看懂:-(，一个端口只能被一个serverSocketChannel监听，第二个好像会报错?这边的主从怎么理解啊</div>2019-06-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/9c/35/9dc79371.jpg" width="30px"><span>你好旅行者</span> 👍（8） 💬（2）<div>I&#47;O多路复用其实就相当于用了一个专门的线程来监听多个注册的事件，而之前的IO模型中，每一个事件都需要一个线程来监听，不知道我这样理解的是否正确？老师我还有一个问题，就是当select监听到一个事件到来时，它是另起一个线程把数据从内核态拷贝到用户态，还是自己就把这个事儿给干了？</div>2019-06-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/3b/36/2d61e080.jpg" width="30px"><span>行者</span> 👍（7） 💬（1）<div>感谢老师分享，联想到Redis的单线程模式，Redis使用同一个线程来做selector，以及处理handler，这样的优点是减少上下文切换，不需要考虑并发问题；但是缺点也很明显，在IO数据量大的情况下，会导致QPS下降；这是由Redis选择IO模型决定的。</div>2019-07-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/05/7f/a7df049a.jpg" width="30px"><span>Standly</span> 👍（6） 💬（5）<div>老师，隔壁李号双老师的《深入拆解Tomcat &amp; Jetty》中关于DirectByteBuffer的解释和您不一样，他的文章中DirectByteBuffer的作用是：DirectByteBuffer 避免了 JVM 堆与本地内存直接的拷贝，而并没有避免内存从内核空间到用户空间的拷贝。而sendfile 特性才是避免了内核与应用之间的内存拷贝。请问哪种才是对的？</div>2019-06-16</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/f0/2e/b3c880b8.jpg" width="30px"><span>余冲</span> 👍（4） 💬（2）<div>老师能对reactor的几种模型，给一个简单版的代码例子看看吗。感觉通过代码应该能更好的理解理论。</div>2019-06-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/c2/fe/038a076e.jpg" width="30px"><span>阿卧</span> 👍（3） 💬（1）<div>老师，redis的io多路复用模型，用的是单线程reactor线程模型嘛？</div>2020-02-25</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/f9/5f/b0a125a9.jpg" width="30px"><span>chp</span> 👍（2） 💬（1）<div>老师，为什么说NIO是同步非阻塞呀？同步我知道原因，那个非阻塞搞不懂，select函数不是已经阻塞了吗，这块要怎么理解呢</div>2020-04-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/17/48/3ab39c86.jpg" width="30px"><span>insist</span> 👍（2） 💬（1）<div>感谢老师的讲解，很细致，从底层原理解释了5中IO模型。在netty，或者其他课程中，都有接触到这类知识，但是一直没有总结，总是看了感觉自己知道了，但是过段时间遇到这类问题，又不知道是为什么。</div>2020-01-04</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/a4/9c/b32ed9e9.jpg" width="30px"><span>陆离</span> 👍（2） 💬（1）<div>我所使用的Tomcat版本是9，默认的就是NIO，是不是版本不同默认模型也不同？
directbuffer如果满了会阻塞还是会报错？这一块的大小设置是不是也可以优化？
因为Linux的aio这一块不成熟所以nio现在是主流？还是有其他原因？</div>2019-06-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/d6/df/1e4ecd94.jpg" width="30px"><span>AA</span> 👍（1） 💬（1）<div>acceptCount是Acceptor主线程数？</div>2020-01-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/2d/11/0ecbe9ea.jpg" width="30px"><span>烈冬冰夏</span> 👍（0） 💬（1）<div>Tomcat 中，BIO、NIO 是基于主从 Reactor主从，那2则的区别是什么呢</div>2019-09-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/5d/57/82f1a3d4.jpg" width="30px"><span>吾爱有三</span> 👍（0） 💬（1）<div>文章多次提到挂起会进入阻塞状态，然到挂起等价阻塞？不是吧</div>2019-06-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/79/4b/740f91ca.jpg" width="30px"><span>-W.LI-</span> 👍（0） 💬（1）<div>老师好!又看了一遍总结了下
epoll()方式的优点如下
1.无需用户空间到内核空间的fd拷贝过程。
2.通过事件表，只返回就绪事件无需轮训遍历
3.基于红黑树增删快。
4.事件发生后内核主动回调，用户进程wait状态(此时算阻塞还是非阻塞啊?)
内核也像观察者，(事件驱动的都像观察者)
还有别的优点么?</div>2019-06-15</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/0b/34/f41d73a4.jpg" width="30px"><span>王盛武</span> 👍（0） 💬（2）<div>刘老师，请问poller线程池 poller队列和文末提的acceptCount队列是不是一个队列？
</div>2019-06-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/7b/57/a9b04544.jpg" width="30px"><span>QQ怪</span> 👍（21） 💬（1）<div>老师这篇可以配合隔壁专栏tomcat的13，14章一起看，会更加有味道。😃</div>2019-06-13</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/PiajxSqBRaELZPnUAiajaR5C25EDLWeJURggyiaOP5GGPe2qlwpQcm5e3ybib8OsP4tvddFDLVRSNNGL5I3SFPJHsA/132" width="30px"><span>null</span> 👍（1） 💬（0）<div>第 8 课原文：
DirectBuffer 只优化了用户空间内部的拷贝，而之前我们是说优化用户空间和内核空间的拷贝，那 Java 的 NIO 中是否能做到减少用户空间和内核空间的拷贝优化呢？

第 11 课原文：
在 Java 的 NIO 编程中，则是使用到了 Direct Buffer 来实现内存的零拷贝。Java 直接在 JVM 内存空间之外开辟了一个物理内存空间，这样内核和用户进程都能共享一份缓存数据。

老师，您好！
第 8 课说：DirectBuffer 只优化了用户空间内部的拷贝，并非优化用户空间和内核空间的。第 8 课提到的是 MappedByteBuffer 调用 mmap 文件内存映射，直接从硬盘读取数据到用户空间，没有经过内核空间。

第 11 课对 DirectBuffer 描述为：内核和用户进程都能共享一份缓存数据。

问题：
第 8 课讲只能优化用户空间。第 11 课讲优化内核空间和用户空间。这 2 节课的描述是否有出入吖？

谢谢老师！</div>2021-04-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/f5/d1/cc6f82eb.jpg" width="30px"><span>kaixiao7</span> 👍（1） 💬（2）<div>老师，有两个疑惑还望您解答，谢谢
1. ulimit -n 显示单个进程的文件句柄数为1024，但是启动一个socket服务(bio实现)后, cat &#47;proc&#47;&lt;pid&gt;&#47;limits 中显示的open files为4096, 实际测试当socket连接数达到4000左右时就无法再连接了.   还请老师解答一下4096怎么来的, 为什么1024不生效呢?
2. 您在文中提到epoll不受fd的限制. 但是我用NIO实现的服务端也是在连接到4000左右时无法再接收新的连接, 环境为Centos7(虚拟机, 内核3.10, 除了系统之外, 没有跑其他程序), jdk1.8, ulimit -n 结果为1024, cat &#47;proc&#47;sys&#47;fs&#47;file-max 结果为382293. 按理说socket连接数最大可以达到38000左右, 代码如下：
public static void main(String[] args) throws IOException {
        ServerSocketChannel channel = ServerSocketChannel.open();
        Selector selector = Selector.open();
        
        channel.configureBlocking(false);
        channel.socket().bind(new InetSocketAddress(10301));
        channel.register(selector, SelectionKey.OP_ACCEPT);

        int size = 0;
        
        while (true) {
            if (selector.select() == 0) {
                continue;
            }

            Iterator&lt;SelectionKey&gt; iterator = selector.selectedKeys().iterator();
            while (iterator.hasNext()) {
                SelectionKey key = iterator.next();
                iterator.remove();
                
                if (key.isAcceptable()) {
                    size++;
                    ServerSocketChannel server = (ServerSocketChannel) key.channel();
                    SocketChannel client = server.accept();

                    System.out.println(&quot;当前客户端连接数: &quot; + size + &quot;, &quot; + client.getRemoteAddress());
                }
            }
        }
        
    }</div>2019-07-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/19/3d/43/72ace06e.jpg" width="30px"><span>accpan</span> 👍（0） 💬（0）<div>总结的很到位</div>2022-08-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/28/91/91/428a27a3.jpg" width="30px"><span>平民人之助</span> 👍（0） 💬（0）<div>其实大部分的公司都用undertow了，这个是默认开启nio吗</div>2021-07-04</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/15/6b/4e472ff9.jpg" width="30px"><span>Mars</span> 👍（0） 💬（0）<div>Tomcat 中，BIO、NIO 是基于主从 Reactor 线程模型实现的。这句话不是很清楚，Reactor 的核心思想是将 I&#47;O 事件注册到多路复用器上，一旦有 I&#47;O 事件触发，多路复用器就会将事件分发到事件处理器中，执行就绪的 I&#47;O 事件操作。那BIO没有所有的I&#47;O事件注册，那怎么套用Reator模型呢？</div>2021-07-03</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/pM3u1b8RtXpsjH8wHzwKnmnsDiba2SfeRbj8ltNnbBNN59FD3ZOOvYDx42kFdBLvu3FuWDQnDba2sop1iaGqBq8A/132" width="30px"><span>Geek_f67f40</span> 👍（0） 💬（1）<div>不知道老师用的是哪个版本，似乎没有mmap的源码显示，或者说，epoll底层根本没使用mmap？</div>2021-04-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/18/5f/10/ed332d5a.jpg" width="30px"><span>warriorSL</span> 👍（0） 💬（0）<div>这篇文章对于理解服务器处理网络请求线程模型真是太优秀了</div>2021-03-07</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/2b/cf/bfb4d21f.jpg" width="30px"><span>星期一</span> 👍（0） 💬（0）<div>sun.nio.ch.ServerSocketChannelImpl#accept()
public SocketChannel accept() throws IOException {
        Object var1 = this.lock;
        synchronized(this.lock) {
            ......
        }
}  和文中Acceptor 线程池有冲突吗？</div>2021-03-06</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/07/d2/0d7ee298.jpg" width="30px"><span>惘 闻</span> 👍（0） 💬（0）<div>BIO通过fork一个子进程处理一个对应连接,NIO一个进程对应多个连接,再通过多个线程处理对应的连接上的io.</div>2020-12-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/07/d2/0d7ee298.jpg" width="30px"><span>惘 闻</span> 👍（0） 💬（0）<div>程序会通过 Selector 来轮询注册在其上的 Channel，当发现一个或多个 Channel 处于就绪状态时.
老师的这句话不太明白,epoll实现了阻塞时的监听回调,为什么selector还是使用轮循呢?轮循不是非常消耗性能嘛?</div>2020-12-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/07/d2/0d7ee298.jpg" width="30px"><span>惘 闻</span> 👍（0） 💬（0）<div>select 通过阻塞后被唤醒的遍历读取fd数组来操作io,poll在select之上去除了对管理的fd数组中fd元素数量的限制,epoll采用红黑树存放fd提高了删写查性能,采用事件监听回调来操作io.</div>2020-12-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/64/9b/d1ab239e.jpg" width="30px"><span>J.Smile</span> 👍（0） 💬（0）<div>&quot;连接在 accept 队列中等待超时。如果 accept 队列过大，就容易浪费连接。&quot;
-----------------------
这里感觉没很看得很清楚，说下我的理解：
浪费连接是因为从accept中取出来之后放入worker线程池，但worker线程池由于并发量太大已经达到最大的线程数，所以只能在队列排队，而如果线程池的队列也占满，那就只能拒绝了。所以accept队列就算设置的很大，worker线程池处理不过来导致线程无法释放，那还是无济于事。老师，我理解的对吗？</div>2020-12-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/a5/ff/6201122c.jpg" width="30px"><span>Geek_89bbab</span> 👍（0） 💬（1）<div>老师，问一下epoll中哪里使用了mmap,我看了linux源码没有看到epoll中使用mmap。
“I&#47;O 复用中的 epoll 函数中就是使用了 mmap 减少了内存拷贝。”这个结论的出处是哪里？</div>2020-09-18</li><br/>
</ul>