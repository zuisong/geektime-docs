你好，我是盛延敏，这里是网络编程实战第28讲，欢迎回来。

在前面的第27讲中，我们引入了reactor反应堆模式，并且让reactor反应堆同时分发Acceptor上的连接建立事件和已建立连接的I/O事件。

我们仔细想想这种模式，在发起连接请求的客户端非常多的情况下，有一个地方是有问题的，那就是单reactor线程既分发连接建立，又分发已建立连接的I/O，有点忙不过来，在实战中的表现可能就是客户端连接成功率偏低。

再者，新的硬件技术不断发展，多核多路CPU已经得到极大的应用，单reactor反应堆模式看着大把的CPU资源却不用，有点可惜。

这一讲我们就将acceptor上的连接建立事件和已建立连接的I/O事件分离，形成所谓的主-从reactor模式。

## 主-从reactor模式

下面的这张图描述了主-从reactor模式是如何工作的。

主-从这个模式的核心思想是，主反应堆线程只负责分发Acceptor连接建立，已连接套接字上的I/O事件交给sub-reactor负责分发。其中sub-reactor的数量，可以根据CPU的核数来灵活设置。

比如一个四核CPU，我们可以设置sub-reactor为4。相当于有4个身手不凡的反应堆线程同时在工作，这大大增强了I/O分发处理的效率。而且，同一个套接字事件分发只会出现在一个反应堆线程中，这会大大减少并发处理的锁开销。
<div><strong>精选留言（27）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/0f/67/f4/9a1feb59.jpg" width="30px"><span>钱</span> 👍（81） 💬（1）<div>1：阻塞IO+多进程——实现简单，性能一般

2：阻塞IO+多线程——相比于阻塞IO+多进程，减少了上下文切换所带来的开销，性能有所提高。

3：阻塞IO+线程池——相比于阻塞IO+多线程，减少了线程频繁创建和销毁的开销，性能有了进一步的提高。

4：Reactor+线程池——相比于阻塞IO+线程池，采用了更加先进的事件驱动设计思想，资源占用少、效率高、扩展性强，是支持高性能高并发场景的利器。

5：主从Reactor+线程池——相比于Reactor+线程池，将连接建立事件和已建立连接的各种IO事件分离，主Reactor只负责处理连接事件，从Reactor只负责处理各种IO事件，这样能增加客户端连接的成功率，并且可以充分利用现在多CPU的资源特性进一步的提高IO事件的处理效率。


6：主 - 从Reactor模式的核心思想是，主Reactor线程只负责分发 Acceptor 连接建立，已连接套接字上的 I&#47;O 事件交给 从Reactor 负责分发。其中 sub-reactor 的数量，可以根据 CPU 的核数来灵活设置。</div>2019-11-24</li><br/><li><img src="" width="30px"><span>ray</span> 👍（12） 💬（2）<div>老师您好，
如果在worker thread pool里面的thread在执行工作时，又遇到了I&#47;O。是不是也可以在worker thread pool里面加入epoll来轮询？但通常在worker thread里面遇到的I&#47;O应该都已经不是network I&#47;O了，而是sql、读写file、或是向第三方发起api，我不是很确定能否用epoll来处理。

有在google上查到，worker thread或worker process若遇到I&#47;O，似乎会用一种叫作coroutine的方式来切换cpu的使用权。此种切换方式，不涉及kernel，全是在应用程序做切换。

这边想请教老师，对在worker thread里面遇到I&#47;O问题时的处理方式或是心得是什么？

谢谢老师的分享！</div>2020-04-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/18/b8/c8/950fb2c9.jpg" width="30px"><span>马不停蹄</span> 👍（7） 💬（1）<div>学习 netty 的时候了解到 reactor 模式，netty 的 （单 、主从）reactor 可以灵活配置，老师讲的模式真的是和 netty 设计一样 ，这次学习算是真正搞明白了哈哈</div>2019-11-12</li><br/><li><img src="" width="30px"><span>刘系</span> 👍（5） 💬（2）<div>老师，我试验了程序，发现有一个问题。
服务器程序启动后输出结果与文章中的不一样。
 .&#47;poll-server-multithreads 
[msg] set poll as dispatcher, main thread
[msg] add channel fd == 4, main thread
[msg] poll added channel fd==4, main thread
[msg] set poll as dispatcher, Thread-1
[msg] add channel fd == 8, Thread-1
[msg] poll added channel fd==8, Thread-1
[msg] event loop thread init and signal, Thread-1
[msg] event loop run, Thread-1
[msg] event loop thread started, Thread-1
[msg] set poll as dispatcher, Thread-2
[msg] add channel fd == 10, Thread-2
[msg] poll added channel fd==10, Thread-2
[msg] event loop thread init and signal, Thread-2
[msg] event loop run, Thread-2
[msg] event loop thread started, Thread-2
[msg] set poll as dispatcher, Thread-3
[msg] add channel fd == 19, Thread-3
[msg] poll added channel fd==19, Thread-3
[msg] event loop thread init and signal, Thread-3
[msg] event loop run, Thread-3
[msg] event loop thread started, Thread-3
[msg] set poll as dispatcher, Thread-4
[msg] add channel fd == 21, Thread-4
[msg] poll added channel fd==21, Thread-4
[msg] event loop thread init and signal, Thread-4
[msg] event loop run, Thread-4
[msg] event loop thread started, Thread-4
[msg] add channel fd == 6, main thread
[msg] poll added channel fd==6, main thread
[msg] event loop run, main thread
各个子线程启动后创建的套接字对是添加在子线程的eventloop上的，而不是像文章中的全是添加在主线程中。
从我阅读代码来看，确实也是添加在子线程中。不知道哪里不对？
主线程给子线程下发连接套接字是通过主线程调用event_loop_add_channel_event完成的，当主线程中发现eventloop和自己不是同一个线程，就通过给这个evenloop的套接字对发送一个“a”产生事件唤醒，然后子线程处理pending_channel，实现在子线程中添加连接套接字。
</div>2019-10-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/17/fa/84/f01d203a.jpg" width="30px"><span>Simple life</span> 👍（4） 💬（1）<div>我觉得老师这里onMessage回调中使用线程池方式有误，这里解码，处理，编码是串行操作的，多线程并不能带来性能的提升，主线程还是会阻塞不释放的，我觉得最佳的做法是，解码交给线程池去做，然后返回，解码完成后注册进sub-reactor中再交由下一个业务处理，业务处理，编码同上，实现解耦充分利用多线程</div>2020-08-03</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/cf/10/9fa2e5ba.jpg" width="30px"><span>进击的巨人</span> 👍（3） 💬（2）<div>Netty的主从reactor分别对应bossGroup和workerGroup，workerGroup处理非accept的io事件，至于业务逻辑是否交给另外的线程池处理，可以理解为netty并没有支持，原因是因为业务逻辑都需要开发者自己自定义提供，但在这点上，netty通过ChannelHandler+pipline提供了io事件和业务逻辑分离的能力，需要开发者添加自定义ChannelHandler，实现io事件到业务逻辑处理的线程分离。</div>2020-11-15</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1a/ea/3c/24cb4bde.jpg" width="30px"><span>疯狂的石头</span> 👍（2） 💬（1）<div>看老师源码，channel，buffer各种对象，调来调去的，给我调懵了。</div>2020-05-06</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/17/52/d8/123a4981.jpg" width="30px"><span>绿箭侠</span> 👍（1） 💬（1）<div>event_loop.c --- struct event_loop *event_loop_init_with_name(char *thread_name)：

#ifdef EPOLL_ENABLE
    yolanda_msgx(&quot;set epoll as dispatcher, %s&quot;, eventLoop-&gt;thread_name);
    eventLoop-&gt;eventDispatcher = &amp;epoll_dispatcher;
#else
    yolanda_msgx(&quot;set poll as dispatcher, %s&quot;, eventLoop-&gt;thread_name);
    eventLoop-&gt;eventDispatcher = &amp;poll_dispatcher;
#endif
    eventLoop-&gt;event_dispatcher_data = eventLoop-&gt;eventDispatcher-&gt;init(eventLoop);

没找到 EPOLL_ENABLE 的定义，老师怎么考虑的！！这里的话是否只能在event_loop.h 所包含的头文件中去找定义？</div>2020-03-06</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/97/b7/d5a83264.jpg" width="30px"><span>李朝辉</span> 👍（1） 💬（1）<div>fd为7的套接字应该是socketpair()调用创建的主-从reactor套接字对中，从reactor线程写，主reactor线程读的套接字，作用的话，个人推测应该是从reactor线程中的连接套接字关闭了（即连接断开了），将这样的事件反馈给主reactor，以通知主reactor线程，我已经准备好接收下一个连接套接字？</div>2020-01-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/97/b7/d5a83264.jpg" width="30px"><span>李朝辉</span> 👍（1） 💬（1）<div>4核cpu，主reactor要占掉一个，只有3个可以分配给从核心。
按照老师的说法，是因为主reactor的工作相对比较简单，所以占用内核的时间很少，所以将从reactor分配满，然后最大化对连接套接字的处理能力吗？</div>2020-01-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/4f/1e/e2b7a9ba.jpg" width="30px"><span>川云</span> 👍（1） 💬（1）<div>可不可以把调用poll代码的位置展示一下</div>2019-10-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/25/62/78/6e7642a3.jpg" width="30px"><span>王蓬勃</span> 👍（0） 💬（1）<div>老师 请问那个event_loop_do_channel_event函数什么时候才进入不是同一个线程的判断中去？看不明白了</div>2021-12-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/22/26/81/036e6579.jpg" width="30px"><span>这一行，30年</span> 👍（0） 💬（1）<div>
   
#include &lt;lib&#47;acceptor.h&gt;
#include &quot;lib&#47;common.h&quot;
#include &quot;lib&#47;event_loop.h&quot;
#include &quot;lib&#47;tcp_server.h&quot;

把老师的代码copy过去，这些类库都报错，不用老师引用的宏用什么宏？</div>2021-11-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/dd/01/803f3750.jpg" width="30px"><span>企鹅</span> 👍（0） 💬（1）<div>老师，主reactor只分发acceptor上建立连接的事件，不应该是client-&gt;acceptor -&gt; master reactor么，图上是client-&gt;master reactor-&gt;acceptor这里看晕了</div>2021-09-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/17/90/e6/5eb07352.jpg" width="30px"><span>Morton</span> 👍（0） 💬（1）<div>老师，Reactor线程池占用了一部分cpu核，然后worker线程如果用线程池又会占用一部分cpu核，假设8核机器应该怎么分配线程池？reactor占4个worker线程占4个？
</div>2021-01-25</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTJUzv6S9wroyXaoFIwvC1mdDiav4BVS4BbPTuwtvWibthL5PyMuxFNicY06QJMZicVpib7E88S19nH4I9Q/132" width="30px"><span>木子皿</span> 👍（0） 💬（1）<div>终于把整个代码流程走通了，太不容易了，不过还只是看得懂，写出来还是很难！</div>2020-10-19</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTJUzv6S9wroyXaoFIwvC1mdDiav4BVS4BbPTuwtvWibthL5PyMuxFNicY06QJMZicVpib7E88S19nH4I9Q/132" width="30px"><span>木子皿</span> 👍（0） 💬（1）<div>坚持坚持，无数次想放弃！快要结束了！</div>2020-10-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/17/68/1592a02d.jpg" width="30px"><span>我的名字不叫1988</span> 👍（0） 💬（1）<div>老师，github上面的源码，lib&#47;poll_dispacher.c文件里面的poll_add、poll_del、poll_update等函数里面的“if (i &gt; INIT_POLL_SIZE)” 判断有问题，因为 for 循环结束之后，i 的可能的最大值为INIT_POLL_SIZE，所以永远不可能大于INIT_POLL_SIZE</div>2020-07-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/18/5e/3b/845fb641.jpg" width="30px"><span>jhren</span> 👍（0） 💬（1）<div>请问老师，我看见有人在发送端使用httpcomponents I&#47;O reactor，请问合理吗？

https:&#47;&#47;hc.apache.org&#47;httpcomponents-core-ga&#47;tutorial&#47;html&#47;nio.html#d5e477</div>2020-05-30</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/2b/84/07f0c0d6.jpg" width="30px"><span>supermouse</span> 👍（0） 💬（1）<div>老师，请问能不能说一下上一讲和这一讲的代码中的channel是干什么用的？一直没看明白</div>2020-02-25</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/18/9d/ab/6589d91a.jpg" width="30px"><span>林林</span> 👍（0） 💬（1）<div>请问老师，这里的主从reactor，是否可以是两个不同的进程(非子进程) 并通过消息队列把新连接socket的描述符发给从reactor进程？ 用这种方法，close socket的时候是否需要主从reactor进程都close一次？</div>2019-11-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/dd/60/eae432c6.jpg" width="30px"><span>yusuf</span> 👍（0） 💬（1）<div>老师，请问是每个从反应堆都有自己的worker线程池么？</div>2019-10-31</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/df/1e/cea897e8.jpg" width="30px"><span>传说中的成大大</span> 👍（0） 💬（1）<div>第一问我研究了代码 lib&#47;event_loop.c 231和232行 创建了一个channel并且event_loop_add_channel_event事件
然后又在lib&#47;tcp_server.c  169和171给listenfd创建了一个channel并且执行了event_loop_add_channel_event
所以是两次,上面那个是对socketpair创建描述符进行了添加作用还不太明白</div>2019-10-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/3d/03/b2d9a084.jpg" width="30px"><span>Hale</span> 👍（0） 💬（1）<div>主 reactor 通过什么样的算法把连接套接字分发给从reactor？</div>2019-10-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/7c/16/4d1e5cc1.jpg" width="30px"><span>mgxian</span> 👍（0） 💬（2）<div>7这个套接字应该是用来传递新建连接的套接字的 </div>2019-10-11</li><br/><li><img src="" width="30px"><span>Geek_d89079</span> 👍（0） 💬（0）<div>我理解的第一个问题是。主线程在接受到一个新连接套接字后，需要把新连接套接字传递给子线程。
主线程通过挑选子线程，子线程会添加新连接套接字到pending-channel-queue中。此时子线程可能处于阻塞状态，无法立即将pending-channel-queue中的新连接套接字加入到监听状态。通过主线程线子线程的管道读端写入，子线程会激活，从而立即处理pending-channel-queue。 </div>2024-04-28</li><br/><li><img src="" width="30px"><span>Geek_d89079</span> 👍（0） 💬（0）<div>我理解的第一个问题是。主线程在接受到一个新连接套接字后，需要把新连接套接字传递给子线程。
主线程通过挑选子线程，子线程会添加新连接套接字到pending-channel-queue中。此时子线程可能处于阻塞状态，无法立即将pending-channel-queue中的新连接套接字加入到监听状态。通过主线程线子线程的管道读端写入，子线程会激活，从而立即处理pending-channel-queue。 </div>2024-04-28</li><br/>
</ul>