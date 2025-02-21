你好，我是蒋德钧。

在[第9讲](https://time.geekbang.org/column/article/407901)中，我给你介绍了Linux提供的三种IO多路复用机制，分别是select、poll和epoll，这是Redis实现事件驱动框架的操作系统层支撑技术。

紧接着在上节课，我带你学习了Redis事件驱动框架的基本工作机制，其中介绍了事件驱动框架基于的Reactor模型，并以IO事件中的客户端连接事件为例，给你介绍了**框架运行的基本流程**：从server初始化时调用aeCreateFileEvent函数注册监听事件，到server初始化完成后调用aeMain函数，而aeMain函数循环执行aeProceeEvent函数，来捕获和处理客户端请求触发的事件。

但是在上节课当中，我们主要关注的是框架基本流程，所以到这里，你或许仍然存有一些疑问，比如说：

- Redis事件驱动框架监听的IO事件，除了上节课介绍的客户端连接以外，还有没有其他事件？而除了IO事件以外，框架还会监听其他事件么？
- 这些事件的创建和处理又分别对应了Redis源码中的哪些具体操作？

今天这节课，我就来给你介绍下Redis事件驱动框架中的两大类事件类型：**IO事件和时间事件，以及它们相应的处理机制。**

事实上，了解和学习这部分内容，一方面可以帮助我们更加全面地掌握，Redis事件驱动框架是如何以事件形式，处理server运行过程中面临的请求操作和多种任务的。比如，正常的客户端读写请求是以什么事件、由哪个函数进行处理，以及后台快照任务又是如何及时启动的。
<div><strong>精选留言（12）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/0f/90/8a/288f9f94.jpg" width="30px"><span>Kaito</span> 👍（35） 💬（0）<div>1、Redis 事件循环主要处理两类事件：文件事件、时间事件

- 文件事件包括：client 发起新连接、client 向 server 写数据、server 向 client 响应数据
- 时间事件：Redis 的各种定时任务（主线程中执行）

2、Redis 在启动时，会创建 aeEventLoop，初始化 epoll 对象，监听端口，之后会注册文件事件、时间事件：

- 文件事件：把 listen socket fd 注册到 epoll 中，回调函数是 acceptTcpHandler（新连接事件）
- 时间事件：把 serverCron 函数注册到 aeEventLoop 中，并指定执行频率

3、Redis Server 启动后，会启动一个死循环，持续处理事件（ae.c 的 aeProcessEvents 函数）

4、有文件事件（网络 IO)，则优先处理。例如，client 到 server 的新连接，会调用 acceptTcpHandler 函数，之后会注册读事件 readQueryFromClient 函数，client 发给 server 的数据，都会在这个函数处理，这个函数会解析 client 的数据，找到对应的 cmd 函数执行

5、cmd 逻辑执行完成后，server 需要写回数据给 client，会先把响应数据写到对应 client 的 内存 buffer 中，在下一次处理 IO 事件之前，Redis 会把每个 client 的 buffer 数据写到 client 的 socket 中，给 client 响应

6、如果响应给 client 的数据过多，则会分多次发送，待发送的数据会暂存到 buffer，然后会向 epoll 注册回调函数 sendReplyToClient，待 socket 可写时，继续调用回调函数向 client 写回剩余数据

7、在这个死循环中处理每次事件时，都会先检查一下，时间事件是否需要执行，因为之前已经注册好了时间事件的回调函数 + 执行频率，所以在执行 aeApiPoll 时，timeout 就是定时任务的周期，这样即使没有 IO 事件，epoll_wait 也可以正常返回，此时就可以执行一次定时任务 serverCron 函数，这样就可以在一个线程中就完成 IO 事件 + 定时任务的处理

课后题：Redis 在调用 aeApiCreate、aeApiAddEvent 这些函数时，是根据什么条件来决定，具体调用哪个文件中的 IO 多路复用函数的？

在 ae.c 中，根据不同平台，首先定义好了要导入的封装好的 IO 多路复用函数，每个平台对应的文件中都定义了 aeApiCreate、aeApiAddEvent 这类函数，在执行时就会执行对应平台的函数逻辑。

&#47;&#47; ae.c
#ifdef HAVE_EVPORT
#include &quot;ae_evport.c&quot;  &#47;&#47; Solaris
#else
    #ifdef HAVE_EPOLL
    #include &quot;ae_epoll.c&quot;   &#47;&#47; Linux
    #else
        #ifdef HAVE_KQUEUE
        #include &quot;ae_kqueue.c&quot;  &#47;&#47; MacOS
        #else
        #include &quot;ae_select.c&quot;  &#47;&#47; Windows
        #endif
    #endif
#endif
</div>2021-08-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/f3/cf/851dab01.jpg" width="30px"><span>Milittle</span> 👍（11） 💬（0）<div>总结一下ae处理框架：
处理IO事件的一些感悟：
1. 创建eventloop（这个地方还没有建立socket服务器监听）(initServer-&gt;aeCreateEventLoop)
2. 然后接着使用listenToPort将所有需要监听的端口进行socket建立以及bind，然后listen。（initServer-&gt;listenToPort-&gt;anetTcpServer-&gt;_anetTcpServer-&gt;anetListen）将普通的监听fd放在server.ipfd，将tls的监听fd放在server.tlsfd
2. 有了这个监听的fd，就得注册到IO多路复用的事件集合中，让后续client可以连接，（initServer-&gt;createSocketAcceptHandler(记住这个地方传入了回调函数acceptTcpHandler，当有客户端连接以后，调的就是它)-&gt;aeCreateFileEvent-&gt;aeApiAddEvent(底层添加事件的调用)）。
3. 把这个监听的scoket放进去，我们就等着连接事件的到来，main函数已经启动的时候调用了aeMain函数，一直在循环监听（main-&gt;aeMain-&gt;aeProcessEvents-&gt;aeApiPoll-&gt;(这里如果有事件，就会调用事件回调，rfileProc or wfileProc， 这两个函数是FilteEvent的回调函数注册，刚才的acceptTcpHandler就注册在这个上面了)）当我们收到客户端监听事件以后，开始在accpetTcpHandler处理任务了。
4. （acceptTcpHandler-&gt;anetTcpAccept(这个函数玩命把这个监听的socket accept一下，然后就返回了我们想要的conn fd叫cfd)-&gt;acceptCommonHandler）。
5. 第四步，最后一个函数就开始处理我们这个链接的cfd的事件注册，重点在调用这个函数createClient，从这函数瞅了半天，发现没有createFileEvent，原来在connSetReadHandler这里，老牛逼了，这些读写事件都被提前注册在conn这个实例里面了，叫type的这个变量。到了connSetReadHandler这个函数里面，那就是该注册连接的cfd了，然后你看到，这个函数传入了readQueryFromClient（这个回调，意思是说，如果这个fd被触发了，那么我们就调它么？显然你从conn中得知，不是的，很遗憾，那么是啥呢，你得乖乖看CT_Socket这个变量，这个玩意就是初始化给了conn的type，然后connSetReadHandler这个函数调用的就是connSocketSetReadHandler它，隐藏在CT_Socket这里面，妈呀，挺绕的。），那么接下来我们看看connSocketSetReadHandler这个函数里面到底干了个啥，不就是注册个fd的事件么，至于这么麻烦么，进去一看，发现真有aeCreateFileEvent，果然，不负真心，上面说的传入的readQueryFromClient，不是fd被触发以后的回调，是因为aeCreateFileEvent这个里面传入的是connSocketEventHandler这个回调，也就是说，我们在后续创建conn以后的读写事件都是在connSocketEventHandler这个函数调用的。
6. 那么我们假设现在已经有了一个连接的事件，客户端发来一条消息，那么就会触发这个cfd，进而回调在这个函数上，进去探探，搞了半天，里面就调了一个conn的读事件，和写事件（还有那个屏障，写法也是牛逼，这个函数可以理解为proxy，触发的是上层注册进来的读事件或者写事件，就是第五步，注册在conn里面的read_handler or write_handler），还得看函数readQueryFromClient，将数据读取，然后放在client里面，然后processInputBuffer处理实际的命令请求，processCommandAndResetClient-&gt;processCommand(各种reject不符合条件的命令)-&gt;call(核心了)。
7. 重点来了，c-&gt;cmd-&gt;proc(c); call的一行调用，看struct redisCommand的定义，注册在server.c的redisCommandTable（查找命令：c-&gt;cmd = c-&gt;lastcmd = lookupCommand(c-&gt;argv[0]-&gt;ptr); 在processCommand这个函数的某一行）。
8. 我们把它串起来了。
备注：本人走读的代码都是最新版本，望知。细节慢慢在补充吧。</div>2021-08-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/25/7f/473d5a77.jpg" width="30px"><span>曾轼麟</span> 👍（6） 💬（0）<div>感谢老师的文章，一样首先回答老师的问题：Redis事件驱动框架是如何区分文件的？
答：
    首先，观察可以发现这几份文件都是命名了相同的代码名字和结构体，例如都有aeApiState结构体，都有aeApiCreate，aeApiResize，aeApiAddEvent，aeApiPoll等方法，那么这里就可以发现其实无论我们使用那一份文件，都不会对调用方造成影响，其次我们观察发现在ae.c文件头部中有这样一段代码：

    #ifdef HAVE_EVPORT
    #include &quot;ae_evport.c&quot;
    #else
        #ifdef HAVE_EPOLL
        #include &quot;ae_epoll.c&quot;
        #else
            #ifdef HAVE_KQUEUE
            #include &quot;ae_kqueue.c&quot;
            #else
            #include &quot;ae_select.c&quot;
            #endif
        #endif
    #endif

    这段代码大致就是根据当前操作系统类型来决定使用那一份头文件，而对操作系统识别在config.h这份文件中，主要划分了（HAVE_EVPORT，HAVE_EPOLL，HAVE_KQUEUE，和默认ae_select.c）这四种类型，所以大致逻辑如下：
        1、config.h中确定当前操作系统类型并打上标记
        2、通过标记选择对应的IO复用文件ae_xxxx.c
        3、编译期间使用对应的文件进行编译
        4、通过统一实现的方法调用例如：aeApiPoll

    所以从这里也能看出，如果我们想强行选择select这种方式进行IO多路复用，可以直接修改ae.c上面的这段宏定义


最后顺便拓展一下本篇文章外的内容，本篇文章除了老师提到的事件驱动框架的核心方法外，老师还提到了几个方法，我个人觉得也比较重要可以深度阅读一下其在Redis项目中出现的位置和实现：
    1、readQueryFromClient
    2、beforeSleep
    3、handleClientsWithPendingWrites
    4、writeToClient

原因：
    1、readQueryFromClient主要是和querybuf打交道（对应读事件），里面涉及到RESP编解码可以深度阅读一下（个人发现Redis处理粘包拆包的方式很独特）。
    2、beforeSleep和afterSleep是搭配的（在aeMain的大循环中每次都被调用），通过这两个钩子函数Redis实现了很多主干路的功能，和一些分治思想的功能。
    3、handleClientsWithPendingWrites可以关注一下其调用方handleClientsWithPendingWritesUsingThreads函数，在这两个方法中都要调用writeToClient方法（对应写事件），而在他们中通过一种巧妙的方式实现了Redis6 IO多线程的方案（可以先预习），handleClientsWithPendingWrites是在只有一个线程或者禁用IO线程的时候使用的。
</div>2021-08-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/26/38/ef063dc2.jpg" width="30px"><span>Darren</span> 👍（3） 💬（0）<div>通过不同的操作系统，include不同的头文件。
在ae.c中
&#47;* Include the best multiplexing layer supported by this system.
 * The following should be ordered by performances, descending. *&#47;
#ifdef HAVE_EVPORT
#include &quot;ae_evport.c&quot;
#else
    #ifdef HAVE_EPOLL
    #include &quot;ae_epoll.c&quot;
    #else
        #ifdef HAVE_KQUEUE
        #include &quot;ae_kqueue.c&quot;
        #else
        #include &quot;ae_select.c&quot;
        #endif
    #endif
#endif

在config.h中，根据操作系统，设置相关的值

&#47;* Test for polling API *&#47;
#ifdef __linux__
#define HAVE_EPOLL 1
#endif

#if (defined(__APPLE__) &amp;&amp; defined(MAC_OS_X_VERSION_10_6)) || defined(__FreeBSD__) || defined(__OpenBSD__) || defined (__NetBSD__)
#define HAVE_KQUEUE 1
#endif

#ifdef __sun
#include &lt;sys&#47;feature_tests.h&gt;
#ifdef _DTRACE_VERSION
#define HAVE_EVPORT 1
#endif
#endif</div>2021-08-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/67/84/50ca0f42.jpg" width="30px"><span>桃僧</span> 👍（2） 💬（1）<div>感觉redis的定时器存储用个链表十分偷懒 当然也和目前只有1个serverCron有关, 按理来说应该弄1个最小堆或者红黑树之类的</div>2021-12-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/2d/f1/1b/0957d4c5.jpg" width="30px"><span>王飞</span> 👍（0） 💬（0）<div>评论区都是大佬呀</div>2022-08-29</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/pftx8PrTibZqu39dxkicUdrXbaMe6v4rcoTzOoF9Z04OibIIDgbpRIrDS9lYBYc97QAscGp77vU6nN5uxRiceRER3Q/132" width="30px"><span>Leon廖</span> 👍（0） 💬（0）<div>按照作者答复，AE_BARRIER好像并没有起作用。
https:&#47;&#47;github.com&#47;redis&#47;redis&#47;issues&#47;7098#issuecomment-614435928
</div>2022-04-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/ee/6c/246fa0d1.jpg" width="30px"><span>Mr.差不多</span> 👍（0） 💬（2）<div>您好，老师如果这时候在epoll_wait 发现可读事件发生（比如对于redis 有一个特别耗时的操作）那么这时候不是会阻塞住while循环吗？</div>2021-08-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/23/c0/ae/e5e62510.jpg" width="30px"><span>徐志超-Klaus</span> 👍（0） 💬（0）<div>请问这个课程能开个微信讨论群吗？这样不仅能大大提高学习氛围和学习效率，还能提高宣传力度。不过还是先问问老师意见？</div>2021-08-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/57/4f/6fb51ff1.jpg" width="30px"><span>奕</span> 👍（0） 💬（1）<div>事件循环结构体中的  aeEventLoop 的 io 事件 aeFileEvent *events 中的 文件描述符 是怎么和外面传入的对应上的？ 

我看 创建监听连接事件的时候 ，直接就把文件描述符传入进入了 server.ipfd[j] 这样怎么保证一定能找到对应的上？</div>2021-08-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/23/c0/ae/e5e62510.jpg" width="30px"><span>徐志超-Klaus</span> 👍（0） 💬（3）<div>刚买课程我就来这里评论了，希望被作者翻牌。我在C语言这块迷路了，我自学看完了《C语言程序设计现代方法第2版》，然后我发现看别人的代码还是有很多不懂的，比如有些关键字书本里没提到，比如我还有些疑问C语言的并发编程怎么写，也不知道接下来该上哪里查资料，因为又要学其他东西，导致我又放弃了一个月的C语言。我现在该怎么办</div>2021-08-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/f3/cf/851dab01.jpg" width="30px"><span>Milittle</span> 👍（0） 💬（0）<div>由宏定义去确定的 ecport-&gt;epoll-&gt;kqueue-&gt;select 

性能逐级递减。这个包含在ae.c头部包含c文件的</div>2021-08-19</li><br/>
</ul>