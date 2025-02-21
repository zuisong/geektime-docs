你好，我是盛延敏，今天是网络编程实战性能篇的答疑模块，欢迎回来。

在性能篇中，我主要围绕C10K问题进行了深入剖析，最后引出了事件分发机制和多线程。可以说，基于epoll的事件分发能力，是Linux下高性能网络编程的不二之选。如果你觉得还不过瘾，期望有更深刻的认识和理解，那么在性能篇的答疑中，我就带你一起梳理一下epoll的源代码，从中我们一定可以有更多的发现和领悟。

今天的代码有些多，建议你配合文稿收听音频。

## 基本数据结构

在开始研究源代码之前，我们先看一下epoll中使用的数据结构，分别是eventpoll、epitem和eppoll\_entry。

我们先看一下eventpoll这个数据结构，这个数据结构是我们在调用epoll\_create之后内核侧创建的一个句柄，表示了一个epoll实例。后续如果我们再调用epoll\_ctl和epoll\_wait等，都是对这个eventpoll数据进行操作，这部分数据会被保存在epoll\_create创建的匿名文件file的private\_data字段中。

```
/*
 * This structure is stored inside the "private_data" member of the file
 * structure and represents the main data structure for the eventpoll
 * interface.
 */
struct eventpoll {
    /* Protect the access to this structure */
    spinlock_t lock;

    /*
     * This mutex is used to ensure that files are not removed
     * while epoll is using them. This is held during the event
     * collection loop, the file cleanup path, the epoll file exit
     * code and the ctl operations.
     */
    struct mutex mtx;

    /* Wait queue used by sys_epoll_wait() */
    //这个队列里存放的是执行epoll_wait从而等待的进程队列
    wait_queue_head_t wq;

    /* Wait queue used by file->poll() */
    //这个队列里存放的是该eventloop作为poll对象的一个实例，加入到等待的队列
    //这是因为eventpoll本身也是一个file, 所以也会有poll操作
    wait_queue_head_t poll_wait;

    /* List of ready file descriptors */
    //这里存放的是事件就绪的fd列表，链表的每个元素是下面的epitem
    struct list_head rdllist;

    /* RB tree root used to store monitored fd structs */
    //这是用来快速查找fd的红黑树
    struct rb_root_cached rbr;

    /*
     * This is a single linked list that chains all the "struct epitem" that
     * happened while transferring ready events to userspace w/out
     * holding ->lock.
     */
    struct epitem *ovflist;

    /* wakeup_source used when ep_scan_ready_list is running */
    struct wakeup_source *ws;

    /* The user that created the eventpoll descriptor */
    struct user_struct *user;

    //这是eventloop对应的匿名文件，充分体现了Linux下一切皆文件的思想
    struct file *file;

    /* used to optimize loop detection check */
    int visited;
    struct list_head visited_list_link;

#ifdef CONFIG_NET_RX_BUSY_POLL
    /* used to track busy poll napi_id */
    unsigned int napi_id;
#endif
};
```

你能看到在代码中我提到了epitem，这个epitem结构是干什么用的呢？

每当我们调用epoll\_ctl增加一个fd时，内核就会为我们创建出一个epitem实例，并且把这个实例作为红黑树的一个子节点，增加到eventpoll结构体中的红黑树中，对应的字段是rbr。这之后，查找每一个fd上是否有事件发生都是通过红黑树上的epitem来操作。
<div><strong>精选留言（18）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/11/9b/88/34c171f1.jpg" width="30px"><span>herongwei</span> 👍（24） 💬（2）<div>这篇文章写得非常棒！之前学 epoll，只会流于表面，也很少去深度剖析底层的数据结构，多读几遍!
另外分享一个大佬同学 epoll 内核源码详解发的帖子：https:&#47;&#47;www.nowcoder.com&#47;discuss&#47;26226</div>2019-10-26</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/IPdZZXuHVMibwfZWmm7NiawzeEFGsaRoWjhuN99iaoj5amcRkiaOePo6rH1KJ3jictmNlic4OibkF4I20vOGfwDqcBxfA/132" width="30px"><span>鱼向北游</span> 👍（20） 💬（1）<div>select这种是把等待队列和就绪队列混在一起，epoll根据这两种队列的特性用两种数据结构把这两个队列分开，果然在程序世界没有解决不了的事情，如果有，就加一个中间层</div>2019-10-18</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/86QEF74Mhc6ECbBBMr62hVz0ezOicI2Kbv8QBA7qR7KepeoDib9W6KLxxMPuQ24JGusvjC03NNr8uj8GyK0DxKiaw/132" width="30px"><span>HerofH</span> 👍（9） 💬（1）<div>首先感谢老师的精彩分析。

然后说下我的个人理解：epoll之所以效率比select高，原因在于select要做的事情太多，每次调用select不仅需要将描述符集添加到监听队列中，还要负责监听事件发生后的处理，以及select最后的清理工作等等...
而epoll则把这么多事情分到了epoll_ctl和epoll_wait去处理，调用epoll_ctl可以开启事件的监听工作，epoll_wait则可以完成对已激活的事件的处理工作，最后close(epfd)完成epoll的清理工作。
而select和epoll_wait是循环中反复调用的，epoll_wait做的事情比select少多了，因此从这个角度来说epoll效率会比select效率高。
除此之外，个人感觉epoll还有一个妙处就是就绪链表，当监听的事件发生后，相应的epitem会自动在监听回调中将其添加到就绪链表中，而对于select来说，则需要不停对所有监听的描述符进行遍历，来检查它们的状态。

不知道理解是否正确，敬请指正。
</div>2020-01-15</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/19/51/29/24739c58.jpg" width="30px"><span>凉人。</span> 👍（8） 💬（1）<div>感觉这一章是最难以理解，如果多一些结构图，流程图，会好很多。</div>2020-02-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/85/d3/abb7bfe3.jpg" width="30px"><span>fackgc17</span> 👍（4） 💬（1）<div>可以提供一下分析用的 kernel 版本吗</div>2019-10-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/e9/86/d34800a4.jpg" width="30px"><span>heyman</span> 👍（3） 💬（4）<div>请问一下，为什么要用红黑树？是因为要排序吗？排序的意义又在哪里？确保查找、插入和删除的高效还不够吗？</div>2020-04-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/22/b1/54/6d663b95.jpg" width="30px"><span>瓜牛</span> 👍（2） 💬（1）<div>还是没明白为啥epoll有红黑树之后就不用在用户空间和内核空间之间拷贝了，或者说poll&#47;select为啥要在用户空间和内核空间之间拷贝？</div>2021-11-05</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/67/f4/9a1feb59.jpg" width="30px"><span>钱</span> 👍（2） 💬（1）<div>功力不够，读起来有些费劲，好似拿到了九阴真经，不过需要黄姑娘翻译一下！
如果能来个图，就好了😁</div>2019-12-01</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/DYAIOgq83errIIarFicghpKamvkUaJmGdIV488iaOUyUqcTwbQ6IeRS40ZFfIOfb369fgleydAT8pkucHuj2x45A/132" width="30px"><span>xupeng1644</span> 👍（1） 💬（1）<div>老师 在Level-triggered VS Edge-triggered小节中给出了Level-triggered的实现机制，可以再给下Edge-triggered的吗</div>2020-02-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/4f/a5/71358d7b.jpg" width="30px"><span>J.M.Liu</span> 👍（1） 💬（1）<div>老师，我请教两个问题：
1.ep_send_events_proc这个函数在把events列表拷贝到用户空间前会调用ep_item_poll函数，已确定对应的fd上的事件依旧有效。那ep_item_poll是根据什么来确定事件的有效性呢？
2.在ep_send_events_proc处理level-triggered的时候，有这么一段话“At this point, no one can insert into ep-&gt;rdllist besides us. The epoll_ctl()  callers are locked out by ep_scan_ready_list() holding &quot;mtx&quot; and the  poll callback will queue them in ep-&gt;ovflist.”意思是说epoll_ctl（）的调用者也被锁在外面了。这个锁是说在ep_send_events_proc还没处理完的时候，epoll_ctl()无法操纵rdllist，但是之后是可以的，以实现再次注册感兴趣的时间。是这样吗？</div>2019-10-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/f6/e3/e4bcd69e.jpg" width="30px"><span>沉淀的梦想</span> 👍（1） 💬（1）<div>缺乏C语言和linux内核基础的人读起这些源码来相当吃力，虽然老师讲得很好</div>2019-10-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/17/06/7e/735968e2.jpg" width="30px"><span>西门吹牛</span> 👍（0） 💬（1）<div>当内核监测到有就绪事件后，将对应的fd 加入就绪 队列，这里其实还会涉及到将有事件的fd拷贝到用户空间，可不可以让用户空间和内核空间采用共享内存的方式，避免拷贝呢</div>2022-01-27</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/DYAIOgq83eqf54z1ZmqQY1kmJ6t1HAnrqMM3j6WKf0oDeVLhtnA2ZUKY6AX9MK6RjvcO8SiczXy3uU0IzBQ3tpw/132" width="30px"><span>Geek_68d3d2</span> 👍（0） 💬（3）<div> epi&gt;nwait &gt;= 0请问这行代码什么意思</div>2020-01-08</li><br/><li><img src="" width="30px"><span>haozhang</span> 👍（0） 💬（1）<div>老师   进程阻塞的形式是什么呢   是for死循环吗     还是加入到等待队列呢，我看for循环前面不是加入到等待队列了吗？</div>2019-11-06</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/ce/5d/5297717a.jpg" width="30px"><span>初见</span> 👍（0） 💬（5）<div>老师，我之前面试被问到过说，epoll 更适合连接很多，但活跃的连接较少的情况

那么，连接很多，活跃连接也很多的情况下，用什么方案呢？  堆机器嘛</div>2019-10-25</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/d7/49/c2426b51.jpg" width="30px"><span>影帝</span> 👍（0） 💬（1）<div>我发现看留言学到的更多。🤓</div>2019-10-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/19/ce/4e/17fd7195.jpg" width="30px"><span>TM</span> 👍（0） 💬（1）<div>hi 老师您好，有个问题想咨询下。把 redis 的 backlog 设置为 1，然后在 redis 里 debug sleep 50，然后发起两个请求，一个成功连接，另一个会出 『opration timeout』 ，而不是 connect timeout，然后大概是 26 s ，反复试了几次、都是26s左右的时间。很奇怪这个报错是内核爆出来的吗？为什么是26s这个时间呢？扩展是 phpredis，php 底层 socket 超时是 60s。</div>2019-10-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/2c/2b/8e/4d24c872.jpg" width="30px"><span>season</span> 👍（0） 💬（0）<div>&#47;&#47;这是eventloop对应的匿名文件，充分体现了Linux下一切皆文件的思想 struct file *file;

&#47;&#47;这个队列里存放的是该eventloop作为poll对象的一个实例，加入到等待的队列 &#47;&#47;这是因为eventpoll本身也是一个file, 所以也会有poll操作 wait_queue_head_t poll_wait;

这两段注释中提到的 eventloop 是什么？  还是 typo，应该是 eventpoll ?</div>2023-05-22</li><br/>
</ul>