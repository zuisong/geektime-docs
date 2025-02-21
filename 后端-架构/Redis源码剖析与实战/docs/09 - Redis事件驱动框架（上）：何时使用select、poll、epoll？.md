你好，我是蒋德钧。

Redis作为一个Client-Server架构的数据库，其源码中少不了用来实现网络通信的部分。而你应该也清楚，通常系统实现网络通信的基本方法是**使用Socket编程模型**，包括创建Socket、监听端口、处理连接请求和读写请求。但是，由于基本的Socket编程模型一次只能处理一个客户端连接上的请求，所以当要处理高并发请求时，一种方案就是使用多线程，让每个线程负责处理一个客户端的请求。

而Redis负责客户端请求解析和处理的线程只有一个，那么如果直接采用基本Socket模型，就会影响Redis支持高并发的客户端访问。

因此，为了实现高并发的网络通信，我们常用的Linux操作系统，就提供了select、poll和epoll三种编程模型，而在Linux上运行的Redis，通常就会采用其中的**epoll模型**来进行网络通信。

这里你可能就要问了：**为啥Redis通常会选择epoll模型呢？这三种编程模型之间有什么区别？**如果我们自己要开发高并发的服务器处理程序时，应该如何选择使用呢？

今天这节课，我就来和你聊聊，Redis在高并发网络通信编程模型上的选择和设计思想。通过这节课的学习，你可以掌握select、poll和epoll三种模型的工作机制和使用方法。了解这些内容，一方面可以帮助你理解Redis整体网络通信框架的工作基础，另一方面，也可以让你学会如何进行高并发网络通信的开发。
<div><strong>精选留言（10）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/0f/90/8a/288f9f94.jpg" width="30px"><span>Kaito</span> 👍（65） 💬（2）<div>1、单线程服务器模型，面临的最大的问题就是，一个线程如何处理多个客户端请求？解决这种问题的办法就是「IO 多路复用」。它本质上是应用层不用维护多个客户端的连接状态，而是把它们「托管」给了操作系统，操作系统维护这些连接的状态变化，之后应用层只管问操作系统，哪些 socket 有数据可读&#47;可写就好了，大大简化了应用层的复杂度

2、IO 多路复用机制要想高效使用，一般还需要把 socket 设置成「非阻塞」模式，即 socket 没有数据可读&#47;可写时，应用层去 read&#47;write socket 也不会阻塞住（内核会返回指定错误，应用层可继续重试），这样应用层就可以去处理其它业务逻辑，不会阻塞影响性能

3、为什么 Redis 要使用「单线程」处理客户端请求？本质上是因为，Redis 操作的是内存，操作内存数据是极快的，所以 Redis 的瓶颈不在 CPU，优化的重点就在网络 IO 上，高效的 IO 多路复用机制，正好可以满足这种需求，模型简单，性能也极高

4、但成也萧何败也萧何，因为 Redis 处理请求是「单线程」，所以如果有任意请求在 Server 端发生耗时（例如操作 bigkey，或一次请求数据过多），就会导致后面的请求发生「排队」，业务端就会感知到延迟增大，性能下降

5、基于此，Redis 又做了很多优化：一些耗时的操作，不再放在主线程处理，而是丢到后台线程慢慢执行。例如，异步关闭 fd，异步释放内存、后台 AOF 刷盘这些操作。所以 Redis Server 其实是「多线程」的，只不过最核心的处理请求逻辑是单线程的，这点一定要区分开

课后题：在 Redis 事件驱动框架代码中，分别使用了 Linux 系统上的 select 和 epoll 两种机制，你知道为什么 Redis 没有使用 poll 这一机制吗？

首先要明确一点，select 并不是只有 Linux 才支持的，Windows 平台也支持。

而 Redis 针对不同操作系统，会选择不同的 IO 多路复用机制来封装事件驱动框架，具体代码见 ae.c。

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

仔细看上面的代码逻辑，先判断了 Solaris&#47;Linux&#47;MacOS 系统，选择对应的多路复用模型，最后剩下的系统都用 select 模型。

所以我理解，select 并不是为 Linux 服务的，而是在 Windows 下使用的。

因为 epoll 性能优于 select 和 poll，所以 Linux 平台下，Redis 直接会选择 epoll。而 Windows 不支持 epoll 和 poll，所以会用 select 模型。
</div>2021-08-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/26/38/ef063dc2.jpg" width="30px"><span>Darren</span> 👍（33） 💬（1）<div>epoll总结如下：
epoll是在2.6内核中提出的，是之前的select和poll的增强版本。相对于select和poll来说，epoll更加灵活，没有描述符限制。epoll使用一个文件描述符管理多个描述符，将用户关系的文件描述符的事件存放到内核的一个事件表中，这样在用户空间和内核空间的copy只需一次。

int epoll_create(int size)；&#47;&#47;创建一个epoll的句柄，
int epoll_ctl(int epfd, int op, int fd, struct epoll_event *event)；
int epoll_wait(int epfd, struct epoll_event * events, int maxevents, int timeout);


1. int epoll_create(int size);
创建一个epoll的句柄，size用来告诉内核这个监听的数目一共有多大，这个参数不同于select()中的第一个参数，给出最大监听的fd+1的值，参数size并不是限制了epoll所能监听的描述符最大个数，在2.6.8之后这个参数就没有实际价值了，因为内核维护一个动态的队列了。

当创建好epoll句柄后，它就会占用一个fd值，在linux下如果查看&#47;proc&#47;进程id&#47;fd&#47;，是能够看到这个fd的，所以在使用完epoll后，必须调用close()关闭，否则可能导致fd被耗尽。当某一进程调用epoll_create方法时，Linux内核会创建一个eventpoll结构体，这个结构体中有两个成员与epoll的使用方式密切相关。
eventpoll结构体如下所示：
struct eventpoll{
    &#47;&#47; 红黑树的根节点，这棵树中存储着所有添加到epoll中的需要监控的事件
    struct rb_root rbr;
    &#47;&#47; 双链表中则存放着将要通过epoll_wait返回给用户的满足条件的事件
    struct list_head rdlist;
    ...
}
每一个epoll对象都有一个独立的eventpoll结构体，用于存放通过epoll_ctl方法向epoll对象中添加进来的事件。这些事件都会挂载在红黑树中，如此，重复添加的事件就可以通过红黑树而高效的识别出来(红黑树的插入时间效率是lgn，其中n为树的高度)。

而所有添加到epoll中的事件都会与设备(网卡)驱动程序建立回调关系，也就是说，当相应的事件发生时会调用这个回调方法。这个回调方法在内核中叫ep_poll_callback,它会将发生的事件添加到rdlist双链表中。
2. int epoll_ctl(int epfd, int op, int fd, struct epoll_event *event)；

函数是对指定描述符fd执行op操作。

用于向内核注册新的描述符或者是改变某个文件描述符的状态。已注册的描述符在内核中会被维护在一棵红黑树上

epfd：是epoll_create()的返回值。
op：表示op操作，用三个宏来表示：添加EPOLL_CTL_ADD，删除EPOLL_CTL_DEL，修改EPOLL_CTL_MOD。分别添加、删除和修改对fd的监听事件。
fd：是需要监听的fd（文件描述符）
epoll_event：是告诉内核需要监听什么事。

当调用epoll_wait检查是否有事件发生时，只需要检查eventpoll对象中的rdlist双链表中是否有epitem元素即可。如果rdlist不为空，则把发生的事件复制到用户态，同时将事件数量返回给用户 。

3.int epoll_wait(int epfd, struct epoll_event * events, int maxevents, int timeout);

等待epfd上的io事件，最多返回maxevents个事件。
通过回调函数内核会将 I&#47;O 准备好的描述符添加到rdlist双链表管理，进程调用 epoll_wait() 便可以得到事件完成的描述符。
参数events用来从内核得到事件的集合，maxevents告之内核这个events有多大，参数timeout是超时时间（毫秒，正整数时间，0是非阻塞，-1永久阻塞直到事件发生）。该函数返回需要处理的事件数目，如返回0表示已超时。

当然epoll对文件描述符的操作有两种模式：LT (level trigger)（默认）和ET (edge trigger)。LT模式是默认模式。</div>2021-08-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/26/38/ef063dc2.jpg" width="30px"><span>Darren</span> 👍（7） 💬（0）<div>select、poll总结如下：

int select (int n, fd_set *readfds, fd_set *writefds, fd_set *exceptfds, struct timeval *timeout);
select 函数监视的文件描述符分3类，分别是readfds、writefds、和exceptfds。调用后select函数会阻塞，直到有描述符就绪（有数据 可读、可写、或者有except），或者超时（timeout指定等待时间，如果立即返回设为null即可），函数返回。当select函数返回后，可以 通过遍历fdset，来找到就绪的描述符。

优点：
        select目前几乎在所有的平台(POSIX)上支持，其良好跨平台支持也是它的一个优点。
缺点：
        1、单个进程能够监视的文件描述符的数量存在最大限制，它由FD_SETSIZE设置，默认值是1024。可以通过修改宏定义甚至重新编译内核的方式提升这一限制，但是这样也会造成效率的降低。一般来说这个数目和系统内存关系很大。32位机默认是1024个。64位机默认是2048.
        2、fd集合在内核被置位过，与传入的fd集合不同，不可重用。重复进行FD_ZERO(&amp;rset); FD_SET(fds[i],&amp;rset);操作
        3、每次调⽤用select，都需要把fd集合从用户态拷贝到内核态，这个开销在fd很多时会很大。
        4、每次调用select都需要在内核遍历传递进来的所有fd标志位，O(n)的时间复杂度，这个开销在fd很多时也很大。

int poll (struct pollfd *fds, unsigned int nfds, int timeout);
不同与select使用三个位图bitmap(bit数组)来表示三个fdset的方式，poll使用一个 pollfd的指针实现。
struct pollfd {
    int fd;             &#47;* file descriptor *&#47;
    &#47;&#47;读 POLLIN; 写POLLOUT;
    short events;   &#47;* requested events to watch 要监视的event*&#47;
    short revents;  &#47;* returned events witnessed 发生的event*&#47;
};
优点：
        1、poll用pollfd数组代替了bitmap，没有最大数量限制。（解决select缺点1）
        2、利用结构体pollfd，每次置位revents字段，每次只需恢复revents即可。pollfd可重用。（解决select缺点2）
缺点：
        1、每次调⽤用poll，都需要把pollfd数组从用户态拷贝到内核态，这个开销在fd很多时会很大。（同select缺点3）
        2、和select函数一样，poll返回后，需要轮询pollfd来获取就绪的描述符。事实上，同时连接的大量客户端在一时刻可能只有很少的处于就绪状态，因此随着监视的描述符数量的增长，其效率也会线性下降。（同select缺点4）</div>2021-08-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1d/6c/b5/32374f93.jpg" width="30px"><span>可怜大灰狼</span> 👍（7） 💬（0）<div>poll相比select性能上变化不大，反而select可以运行在更多的系统上，兼容性更好。但是我记得rewrite aof的时候会用到poll。所以特意翻了下代码。aof.c中rewriteAppendOnlyFile方法调用了aeWait，aeWait里通过poll来完成阻塞时间。</div>2021-08-15</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/25/7f/473d5a77.jpg" width="30px"><span>曾轼麟</span> 👍（5） 💬（0）<div>首先回答老师的问题：为什么Redis没有使用poll这种机制？
select 和 poll其实本质上没有太大的区别（二选一就好了，而select对windows较友好），poll的特点就是突破了select的最大套接字上限的问题，所以poll本身和select一样会存在，遍历所有套接字列表的情况，而如果Redis当前存在大量无效或者空闲的连接，这时候每次都遍历就会带来一定的开销了，而epoll可以直接返回已经触发事件（活跃）的套接字，避免了循环带来的开销。

总结：
今天老师主要和我们介绍了，Redis在IO多路复用的实现和设计思路。我回到源码阅读后大概整理了一下：
	1、redis为了满足各种系统实现了多套IO多路复用，分别有：epoll，select，evport，kqueue
	2、redis在IO多路复用的代码实现进行了抽象，通过同一实现了aeApiState，aeApiCreate，aeApiResize，aeApiFree等等方法（类比接口）实现了多套IO复用，方便在编译期间切换（文件：ae_epoll.c，ae_evport.c，ae_kqueue.c，ae_select.c）
	3、在前面的文章中提到Redis启动的时候，在initServer方法中注册了acceptTcpHandler方法，用于处理连接事件，创建完成连接后交给对应IO多路复用
	4、通过aeApiCreate方法创建对应的IO多路复用，在创建aeEventLoop中创建，然后开始接受处理对应的事件

此外Redis在整个IO多路复用上的实现，预留了很大的灵活空间，实现了类似java接口的效果，这点值得我们学习，能灵活的切换不同的IO复用的方式，并且也方便拓展新的IO复用方式。</div>2021-08-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1c/4e/88/791d0f5e.jpg" width="30px"><span>lei</span> 👍（2） 💬（0）<div>JDK 里也有 select() 方法，但是底层它是基于 epoll 实现。

select 函数将当前进程轮流加入每个 fd 对应设备的等待队列去询问该 fd 有无可读&#47;写事件。Linux 的开发者想到，找个“代理”的回调函数代替当前进程，去加入 fd 对应设备的等待队列，让这个代理的回调函数去等待设备就绪，当有设备就绪就将自己唤醒，然后该回调函数就把这个设备的 fd 放到一个就绪队列，同时通知可能在等待的轮询进程来这个就绪队列里取已经就绪的 fd。当前轮询的进程不需要遍历整个被侦听的 fd 集合。

简单说：
* epoll 将用户关心的 fd 放到了 Linux 内核里的一个事件表中，而不是像 select&#47;poll 函数那样，每次调用都需要复制 fd 到内核。内核将持久维护加入的 fd，减少了内核和用户空间复制数据的性能开销。
* 当一个 fd 的事件发生（比如说读事件），epoll 机制无须遍历整个被侦听的 fd 集，只要遍历那些被内核 I&#47;O 事件异步唤醒而加入就绪队列的 fd 集合，减少了无用功。
* epoll 机制支持的最大 fd 上限远远大于 1024，在1GB内存的机器上是 10 万左右，具体数目可以 cat&#47;proc&#47;sys&#47;fs&#47;file-max 查看。

epoll缺点：
epoll每次只遍历活跃的 fd (如果是 LT，也会遍历先前活跃的 fd)，在活跃fd较少的情况下就会很有优势，如果大部分fd都是活跃的，epoll的效率可能还不如 select&#47;poll。
</div>2021-11-16</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/17/8b/4b/15ab499a.jpg" width="30px"><span>风轻扬</span> 👍（1） 💬（0）<div>看了好几遍，终于看懂了select和epoll的主要区别。
select函数。函数中定义了几个描述符集合，然后内核会关注这些描述符集合中，哪些描述符就绪了，然后返回已就绪的描述符个数，业务程序需要遍历所有的描述符集合，来找到可处理的描述符集合，这个遍历操作，很明显是O(n)的时间复杂度
epoll函数。函数中定义了监听的描述符、就绪的描述符，并且很重要的是：就绪的描述符用一个专门的结构存储，业务程序可以直接遍历这个就绪描述符集合，这样就省了遍历整个集合，在描述符很多时，epoll相比select，性能有肉眼的增长</div>2023-10-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/96/a6/aac2a550.jpg" width="30px"><span>陌</span> 👍（1） 💬（0）<div>epoll 还有一个非常重要的一点就是会在 TCP&#47;IP 协议栈实现上注册一个回调函数，也就是 `ep_poll_callback`，其作用就是将 epoll 红黑树上的 epitem 对象添加到双向链表中，同时如果此时 `epoll_wait()` 如果被阻塞的话将会唤醒，获得调度机会后将双向链表的数据拷贝到 `evlist` 中，应用程序可直接对其中的 socket fd 进行读写。</div>2021-08-17</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/S2RCl03ejxSqsShDO7uExPvKfFQuoMlvTbicUqwYCzQYAZUtCC4HTBNhrjmLcOGA3fOkCkzjAKbJ74nJl6Ngicvw/132" width="30px"><span>Geek_613829</span> 👍（1） 💬（0）<div>天，我居然是第一Σ(￣ロ￣lll)</div>2021-08-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1a/46/42/eaa0cc92.jpg" width="30px"><span>无风</span> 👍（0） 💬（0）<div>ep_events为什么用malloc呢？我查了下很多demo用malloc，也有的demo直接定义数组。。</div>2021-08-18</li><br/>
</ul>