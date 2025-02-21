你好，我是蒋德钧。今天，我们来聊聊Redis是如何实现Reactor模型的。

你在做Redis面试题的时候，或许经常会遇到这样一道经典的问题：Redis的网络框架是实现了Reactor模型吗？这看起来像是一道简单的“是/否”问答题，但是，如果你想给出一个让面试官满意的答案，这就非常考验你的**高性能网络编程基础和对Redis代码的掌握程度**了。

如果让我来作答这道题，我会把它分成两部分来回答：一是介绍Reactor模型是什么，二是说明Redis代码实现是如何与Reactor模型相对应的。这样一来，就既体现了我对网络编程的理解，还能体现对Redis源码的深入探究，进而面试官也就会对我刮目相看了。

实际上，Reactor模型是高性能网络系统实现高并发请求处理的一个重要技术方案。掌握Reactor模型的设计思想与实现方法，除了可以应对面试题，还可以指导你设计和实现自己的高并发系统。当你要处理成千上万的网络连接时，就不会一筹莫展了。

所以今天这节课，我会先带你了解下Reactor模型，然后一起来学习下如何实现Reactor模型。因为Redis的代码实现提供了很好的参考示例，所以我会通过Redis代码中的关键函数和流程，来给你展开介绍Reactor模型的实现。不过在学习Reactor模型前，你可以先回顾上节课我给你介绍的IO多路复用机制epoll，因为这也是学习今天这节课的基础。
<div><strong>精选留言（16）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/13/26/38/ef063dc2.jpg" width="30px"><span>Darren</span> 👍（76） 💬（2）<div>Reactor模型可以分为3种：
单线程Reactor模式
一个线程：
单线程：建立连接（Acceptor）、监听accept、read、write事件（Reactor）、处理事件（Handler）都只用一个单线程。

多线程Reactor模式
一个线程 + 一个线程池：
单线程：建立连接（Acceptor）和 监听accept、read、write事件（Reactor），复用一个线程。
工作线程池：处理事件（Handler），由一个工作线程池来执行业务逻辑，包括数据就绪后，用户态的数据读写。

主从Reactor模式
三个线程池：
主线程池：建立连接（Acceptor），并且将accept事件注册到从线程池。
从线程池：监听accept、read、write事件（Reactor），包括等待数据就绪时，内核态的数据I读写。
工作线程池：处理事件（Handler），由一个工作线程池来执行业务逻辑，包括数据就绪后，用户态的数据读写

具体的可以参考并发大神 doug lea 关于Reactor的文章。 http:&#47;&#47;gee.cs.oswego.edu&#47;dl&#47;cpjslides&#47;nio.pdf

再提一点，使用了多路复用，不一定是使用了Reacto模型，Mysql使用了select（为什么不使用epoll，因为Mysql的瓶颈不是网络，是磁盘IO），但是并不是Reactor模型

回到问题，那些也是reactor

nginx：nginx是多进程模型，master进程不处理网络IO，每个Wroker进程是一个独立的单Reacotr单线程模型。

netty：通信绝对的王者，默认是多Reactor，主Reacotr只负责建立连接，然后把建立好的连接给到从Reactor，从Reactor负责IO读写。当然可以专门调整为单Reactor。

kafka：kafka也是多Reactor，但是因为Kafka主要与磁盘IO交互，因此真正的读写数据不是从Reactor处理的，而是有一个worker线程池，专门处理磁盘IO，从Reactor负责网络IO，然后把任务交给worker线程池处理。</div>2021-08-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/90/8a/288f9f94.jpg" width="30px"><span>Kaito</span> 👍（26） 💬（2）<div>1、为了高效处理网络 IO 的「连接事件」、「读事件」、「写事件」，演化出了 Reactor 模型

2、Reactor 模型主要有 reactor、acceptor、handler 三类角色：

- reactor：分配事件
- acceptor：接收连接请求
- handler：处理业务逻辑

3、Reactor 模型又分为 3 类：

- 单 Reactor 单线程：accept -&gt; read -&gt; 处理业务逻辑 -&gt; write 都在一个线程
- 单 Reactor 多线程：accept&#47;read&#47;write 在一个线程，处理业务逻辑在另一个线程
- 多 Reactor 多线程 &#47; 进程：accept 在一个线程&#47;进程，read&#47;处理业务逻辑&#47;write 在另一个线程&#47;进程

4、Redis 6.0 以下版本，属于单 Reactor 单线程模型，监听请求、读取数据、处理请求、写回数据都在一个线程中执行，这样会有 3 个问题：

- 单线程无法利用多核
- 处理请求发生耗时，会阻塞整个线程，影响整体性能
- 并发请求过高，读取&#47;写回数据存在瓶颈

5、针对问题 3，Redis 6.0 进行了优化，引入了 IO 多线程，把读写请求数据的逻辑，用多线程处理，提升并发性能，但处理请求的逻辑依旧是单线程处理

课后题：除了 Redis，你还了解什么软件系统使用了 Reactor 模型吗？

Netty、Memcached 采用多 Reactor 多线程模型。

Nginx 采用多 Reactor 多进程模型，不过与标准的多 Reactor 多进程模型有些许差异。Nginx 的主进程只用来初始化 socket，不会 accept 连接，而是由子进程 accept 连接，之后这个连接的所有处理都在子进程中完成。</div>2021-08-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/22/bd/9b/366bb87b.jpg" width="30px"><span>飞龙</span> 👍（3） 💬（0）<div>main(server.c)-&gt;aeCreateEventLoop(aeApiCreate epoll_create)-&gt;aeCreateFileEvent(aeApiAddEvent epoll_ctl)-&gt;aeMain(server.c)-&gt;aeProcessEvents(aeApiPoll epoll_wait)</div>2022-09-15</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/26/cb/28/21a8a29e.jpg" width="30px"><span>夏天</span> 👍（2） 💬（1）<div>Redis 实现 ae 框架十分巧妙的一点是&quot;抽象&quot;。用面向过程的 C 写出了面向对象的感觉。

抽象出事件初始化、事件注册、事件接收。并通过 fd 和 mask 关联底层 API 对象和上层对象。

当底层 API 触发时，通过 fd 和 mask 找到上层对象，再调用对象中注册的 callback。

以 epoll 举例，aeApi 是抽象层，不同平台选用不通的 IO 复用 API。

aeCreateEventLoop &lt;---&gt; aeApiCreate   &lt;---&gt; epoll_create
aeCreateFileEvent &lt;---&gt; aeApiAddEvent &lt;---&gt; epoll_ctl    
aeProcessEvents   &lt;---&gt; aeApiPoll     &lt;---&gt; epoll_wait   </div>2022-02-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1f/5e/81/82709d6e.jpg" width="30px"><span>码小呆</span> 👍（2） 💬（0）<div>只知道netty用过Reactor模型，看了评论学到了</div>2021-08-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/c6/dc/37dac825.jpg" width="30px"><span>阿豪</span> 👍（1） 💬（5）<div>主循环这样不断执行，怎么保证不耗尽cpu ？理论上这个cpu 会一直处于忙碌状态。</div>2021-12-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/25/7f/473d5a77.jpg" width="30px"><span>曾轼麟</span> 👍（1） 💬（0）<div>上篇文章回答的时候自己提到的-Redis基于多种IO复用实现了同一方法但是多套代码文件的思路，没想到这期老师就提到了。回答老师的问题：还有什么软件系统使用了Reactor模型？
答：
    最典型的就是netty，java靠netty得以实现了高性能的服务

总结：
本篇文章老师主要介绍了Redis是如何实现Reactor模型，其本质上就是围绕三个事件的实现【连接请求，读事件，写事件】，而Redis为了方便实现，封装了事件驱动框架aeEventLoop，其本质上是一个不断处理事件的循环。能同时分发处理来自成百上千个客户端的读，写，连接等请求。
</div>2021-08-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/9b/69/b844df30.jpg" width="30px"><span>结冰的水滴</span> 👍（1） 💬（0）<div>kafka使用了Reactor编程模型，它使用一个Acceptor,多个Processor处理网络连接，读写请求，以及一个线程池处理消息读写</div>2021-08-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/ca/07/22dd76bf.jpg" width="30px"><span>kobe</span> 👍（0） 💬（0）<div>ae_epoll.c，对应 Linux 上的 IO 复用函数 epoll；
ae_evport.c，对应 Solaris 上的 IO 复用函数 evport；
ae_kqueue.c，对应 macOS 或 FreeBSD 上的 IO 复用函数 kqueue；
ae_select.c，对应 Linux（或 Windows）的 IO 复用函数 select。
你好 我想问下 这个不同操作系统是不是在编译的时候就确定了对应的是哪一个实现？</div>2023-08-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/ca/07/22dd76bf.jpg" width="30px"><span>kobe</span> 👍（0） 💬（0）<div>ae_epoll.c，对应 Linux 上的 IO 复用函数 epoll；ae_evport.c，对应 Solaris 上的 IO 复用函数 evport；ae_kqueue.c，对应 macOS 或 FreeBSD 上的 IO 复用函数 kqueue；ae_select.c，对应 Linux（或 Windows）的 IO 复用函数 select。</div>2023-08-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/ca/07/22dd76bf.jpg" width="30px"><span>kobe</span> 👍（0） 💬（0）<div>ae_epoll.c，对应 Linux 上的 IO 复用函数 epoll；
ae_evport.c，对应 Solaris 上的 IO 复用函数 evport；
ae_kqueue.c，对应 macOS 或 FreeBSD 上的 IO 复用函数 kqueue；
ae_select.c，对应 Linux（或 Windows）的 IO 复用函数 select。</div>2023-08-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1a/30/60/f6cd45e3.jpg" width="30px"><span>柯江胜</span> 👍（0） 💬（1）<div>对于写事件还不是很理解，连接事件是客户端发来连接请求，读事件是客户端发来命令请求需要读取，那么写事件对应的是什么触发的？</div>2022-09-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/29/2e/49/a04480a9.jpg" width="30px"><span>路遥知码力</span> 👍（0） 💬（0）<div>swoole使用的是主从Reactor模型</div>2021-10-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/88/d7/07f8bc6c.jpg" width="30px"><span>sljoai</span> 👍（0） 💬（0）<div>Netty也实现了Reactor模型</div>2021-08-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/ee/6c/246fa0d1.jpg" width="30px"><span>Mr.差不多</span> 👍（0） 💬（1）<div>老师 您好，while 循环里面的线程就算是 IO 线程吗</div>2021-08-24</li><br/><li><img src="https://wx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTLm8skz4F7FGGBTXWUMia6qVEc00BddeXapicv5FkAx62GmOnUNEcE4scSR60AmappQoNdIQhccKsBA/132" width="30px"><span>末日，成欢</span> 👍（0） 💬（6）<div>我一直不明白的一点， while循环里使用aeApiPoll得到一些事件后，要对这些事件进行处理， 每个处理函数不耗时吗， 假设每个函数处理耗时1ms， 有1000个事件， 那么下一次循环不得1s后了。 </div>2021-08-17</li><br/>
</ul>