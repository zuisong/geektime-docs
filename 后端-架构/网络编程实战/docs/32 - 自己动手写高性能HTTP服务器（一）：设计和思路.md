你好，我是盛延敏，这里是网络编程实战第32讲，欢迎回来。

从这一讲开始，我们进入实战篇，开启一个高性能HTTP服务器的编写之旅。

在开始编写高性能HTTP服务器之前，我们先要构建一个支持TCP的高性能网络编程框架，完成这个TCP高性能网络框架之后，再增加HTTP特性的支持就比较容易了，这样就可以很快开发出一个高性能的HTTP服务器程序。

## 设计需求

在第三个模块性能篇中，我们已经使用这个网络编程框架完成了多个应用程序的开发，这也等于对网络编程框架提出了编程接口方面的需求。综合之前的使用经验，TCP高性能网络框架需要满足的需求有以下三点。

第一，采用reactor模型，可以灵活使用poll/epoll作为事件分发实现。

第二，必须支持多线程，从而可以支持单线程单reactor模式，也可以支持多线程主-从reactor模式。可以将套接字上的I/O事件分离到多个线程上。

第三，封装读写操作到Buffer对象中。

按照这三个需求，正好可以把整体设计思路分成三块来讲解，分别包括反应堆模式设计、I/O模型和多线程模型设计、数据读写封装和buffer。今天我们主要讲一下主要的设计思路和数据结构，以及反应堆模式设计。
<div><strong>精选留言（30）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/14/00/4e/be2b206b.jpg" width="30px"><span>吴小智</span> 👍（7） 💬（2）<div>map_make_space() 函数里 realloc() 和 memset() 两个函数用的很巧妙啊，realloc() 用来扩容，且把旧的内容搬过去，memset() 用来给新申请的内存赋 0 值。赞，C 语言太强大了。</div>2019-10-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/23/66/413c0bb5.jpg" width="30px"><span>LDxy</span> 👍（7） 💬（1）<div>event_loop_handle_pending_add函数中，
map-&gt;entries[fd] = calloc(1, sizeof(struct channel *));
map-&gt;entries[fd] = channel;
这两行都给map-&gt;entries[fd] 赋值，后一行不是覆盖上一行的赋值了么？有何用意？</div>2019-10-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/9c/62/f625b2bb.jpg" width="30px"><span>酸葡萄</span> 👍（3） 💬（2）<div>老师你好，问个基础的问题：
epoll_dispatcher和poll_dispatcher都有，在添加，删除，更新事件时都有如下的逻辑，其中if条件中的判断怎么理解啊？
if (channel1-&gt;events &amp; EVENT_READ) {
        events = events | POLLRDNORM;
    }

    if (channel1-&gt;events &amp; EVENT_WRITE) {
        events = events | POLLWRNORM;
    }</div>2019-12-01</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/f6/e3/e4bcd69e.jpg" width="30px"><span>沉淀的梦想</span> 👍（2） 💬（3）<div>看到map_make_space里面的realloc函数，突然有个疑问，既然操作系统底层支持直接在原数组上扩充内存，为什么Java不支持直接在原数组上扩容呢，ArrayList每次扩容都要重新拷贝一份原来的数据。</div>2019-10-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/fa/20/0f06b080.jpg" width="30px"><span>凌空飞起的剪刀腿</span> 👍（1） 💬（1）<div>int map_make_space(struct channel_map *map, int slot, int msize) {
    if (map-&gt;nentries &lt;= slot) {
        int nentries = map-&gt;nentries ? map-&gt;nentries : 32;
        void **tmp;

        while (nentries &lt;= slot)
            nentries &lt;&lt;= 1;

        tmp = (void **) realloc(map-&gt;entries, nentries * msize);
        if (tmp == NULL)
            return (-1);

        memset(&amp;tmp[map-&gt;nentries], 0,
               (nentries - map-&gt;nentries) * msize);

        map-&gt;nentries = nentries;
        map-&gt;entries = tmp;
    }

    return (0);
}
老师，fd不一定是连续的吧，这样会浪费内存存储空间吧？</div>2021-06-07</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/25/2b/ca/71ff1fd7.jpg" width="30px"><span>谁家内存泄露了</span> 👍（1） 💬（1）<div>老师好，请问您的代码中关于锁的使用，我想知道您关于每个loop都设计了一个锁，可是这几个mutex都是局部变量吧？他们的作用范围是什么样的呢？这里想不清楚，请指点一下！</div>2021-04-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/18/c1/39/11904266.jpg" width="30px"><span>Steiner</span> 👍（1） 💬（1）<div>如果Channel是一个管道，他连接着哪两个对象？</div>2021-02-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/28/97/dc/8eacc8f1.jpg" width="30px"><span>漠博嵩</span> 👍（0） 💬（1）<div>感觉就是仿照netty框架做的</div>2022-05-24</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTLmWgscKlnjXiaBugNJ2ozMmZibAEKichZv7OfGwQX9voDicVy2qnKtlm5kWQAKZ414vFohR8FV5N9ZhA/132" width="30px"><span>菜鸡</span> 👍（0） 💬（1）<div>第二个问题有点疑问。channel_map中元素的空间大小是与fd的值正相关的，而不是跟当前在线的连接数量正相关，这样做是不是有点浪费内存？比如经历了很多次连接、断开之后，fd返回的值比较大，而此时只有几个未断开的连接，那么channel_map有必要申请那么大的内存空间嘛？</div>2022-05-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/ed/6c/6fb35017.jpg" width="30px"><span>群书</span> 👍（0） 💬（1）<div>用sock对通知 唤醒会不会增加逻辑线程或主线程的系统调用次数 限制了吞吐量呢</div>2021-11-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/18/c1/39/11904266.jpg" width="30px"><span>Steiner</span> 👍（0） 💬（1）<div>我看了下定义，channel_element就像是个链表节点，为什么不用C++来做这块呢？</div>2021-02-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/20/dd/6e/8f6f79d2.jpg" width="30px"><span>YUAN</span> 👍（0） 💬（1）<div>老师请问这个channel就相当于libevent中的event结构体吧？</div>2020-11-05</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/49/96/7523cdb6.jpg" width="30px"><span>spark</span> 👍（0） 💬（2）<div>盛老师好: 为什么要在下面这个函数中lock和unlock? 不是每个线程都对应一个自己的event_loop吗?
这样的话event_loop就不是shared resource。
int event_loop_handle_pending_channel(struct event_loop *eventLoop) {
    &#47;&#47;get the lock
    pthread_mutex_lock(&amp;eventLoop-&gt;mutex);
    eventLoop-&gt;is_handle_pending = 1;

    struct channel_element *channelElement = eventLoop-&gt;pending_head;
    while (channelElement != NULL) {
        &#47;&#47;save into event_map
        struct channel *channel = channelElement-&gt;channel;
        int fd = channel-&gt;fd;
        if (channelElement-&gt;type == 1) {
            event_loop_handle_pending_add(eventLoop, fd, channel);
        } else if (channelElement-&gt;type == 2) {
            event_loop_handle_pending_remove(eventLoop, fd, channel);
        } else if (channelElement-&gt;type == 3) {
            event_loop_handle_pending_update(eventLoop, fd, channel);
        }
        channelElement = channelElement-&gt;next;
    }

    eventLoop-&gt;pending_head = eventLoop-&gt;pending_tail = NULL;
    eventLoop-&gt;is_handle_pending = 0;

    &#47;&#47;release the lock
    pthread_mutex_unlock(&amp;eventLoop-&gt;mutex);

    return 0;
}</div>2020-09-25</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTKVUskibDnhMt5MCIJ8227HWkeg2wEEyewps8GuWhWaY5fy7Ya56bu2ktMlxdla3K29Wqia9efCkWaQ/132" width="30px"><span>衬衫的价格是19美元</span> 👍（0） 💬（2）<div>channel_map这里map-&gt;entries是一个数组，数组的下标是fd,数组的元素是channel的地址，如果新增的fd跳变很大的话比如从3变成了100，会不会浪费了很多的空间</div>2020-07-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/ab/cb/55eddaf1.jpg" width="30px"><span>胤</span> 👍（0） 💬（1）<div>问个c语言的问题，比如event_loop_handle_pending_channel这个函数，返回值是int类型，但是除了函数最后是个return 0，其他地方没有错误处理，为什么要返回0？还是就是一种习惯？</div>2020-05-04</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/18/b3/17/19ea024f.jpg" width="30px"><span>chs</span> 👍（0） 💬（1）<div>老师，您为了支持poll和epoll，抽象出了struct event_dispatcher结构体，然后在epoll_dispatcher.c 和poll_dispatcher.c中分别实现struct event_dispatcher中定义的接口。请问epoll_dispatcher.c中的 const struct event_dispatcher epoll_dispatcher变量 和poll_dispatcher.c中的const struct event_dispatcher poll_dispatcher变量怎样让其他文件知道其定义的。我自己写的提示上边两个变量未定义。</div>2019-12-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/18/c1/39/11904266.jpg" width="30px"><span>Steiner</span> 👍（0） 💬（1）<div>请问channel里的fd也需要设置为非阻塞吗</div>2019-10-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/df/1e/cea897e8.jpg" width="30px"><span>传说中的成大大</span> 👍（0） 💬（1）<div>老师 你好 问你一个和课程沾点点边的关系的问题哈，虽然我晓得什么这样模式那样模式 但是还是不会设计 比如像老师为课程设计的框架 回调都是两层 为什么要这样设计我却不明白 有没有什么规范啥的可以指导一下 可能真的是没好好学过设计模式,既然现在都涉及到要自己动手一个服务器框架了  我也想解决设计这方面的问题，希望老师点播一下</div>2019-10-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/df/1e/cea897e8.jpg" width="30px"><span>传说中的成大大</span> 👍（0） 💬（1）<div>而且新连接,创建的channel对象上的回调也应该是tcp_connection上的回调</div>2019-10-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/df/1e/cea897e8.jpg" width="30px"><span>传说中的成大大</span> 👍（0） 💬（1）<div>lib&#47;tcp_connection.c最终是在lib&#47;tcp_connection.c 第22行执行了应用层的readcallback函数执行 epoll-server-multithreads.c onMessage为什么要封装两次呢？ 封装一个tcp_connection是为了隐藏读取字节流的实现吗,主要是套接字层？ tcp_server层主要就是引用层的这样理解可以吗？</div>2019-10-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/df/1e/cea897e8.jpg" width="30px"><span>传说中的成大大</span> 👍（0） 💬（1）<div>今天仔细研读了老师的代码突然发现有两层回调
1. epoll-server-multithreads.c里面写的有回调 并且赋给了tcp_server
2. tcp_connection.c 实现了 handle_read handle_write 等等事件的回调 为什么要封装两层回调呢 我设计模式没怎么学过 希望老师指点哈</div>2019-10-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/df/1e/cea897e8.jpg" width="30px"><span>传说中的成大大</span> 👍（0） 💬（1）<div>epollDispatcherData-&gt;events = calloc(MAXEVENTS, sizeof(struct acceptor));
这一行不太明白为什么要分配MAXEVENTS* sizeof( struct acceptor )这么多内存？我的关注点在sizeof( 
struct acceptor ),为什么取它的大小？</div>2019-10-21</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/IPdZZXuHVMibwfZWmm7NiawzeEFGsaRoWjhuN99iaoj5amcRkiaOePo6rH1KJ3jictmNlic4OibkF4I20vOGfwDqcBxfA/132" width="30px"><span>鱼向北游</span> 👍（0） 💬（1）<div>老师的程序读了一遍，c版的netty，果然高手们的思路都是相通的</div>2019-10-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/df/1e/cea897e8.jpg" width="30px"><span>传说中的成大大</span> 👍（3） 💬（0）<div>第二道题 就是一个扩容啊 类似std的vector自动扩容 而且每次成倍的增长</div>2019-10-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/37/e6/48/c8ca3db6.jpg" width="30px"><span>Y.X</span> 👍（0） 💬（0）<div>老师你好，请问event_loop里为什么有pending head和pending tail呢？请问每个channel是重复使用吗？</div>2023-07-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/37/e6/48/c8ca3db6.jpg" width="30px"><span>Y.X</span> 👍（0） 💬（0）<div>while (!eventLoop-&gt;quit)

老师，请问什么情况下quit会被修改呢？我没有看到相关修改quit的函数。</div>2023-07-07</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/37/e6/48/c8ca3db6.jpg" width="30px"><span>Y.X</span> 👍（0） 💬（0）<div>void *(*init)(struct event_loop * eventLoop);

老师，请问*init的“*”是什么意思呢？</div>2023-07-07</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/29/b0/d3/200e82ff.jpg" width="30px"><span>功夫熊猫</span> 👍（0） 💬（0）<div>老师，套接字不是用于进城通信的嘛，线程也能用？</div>2022-09-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/2a/31/17/ab2c27a6.jpg" width="30px"><span>菜鸡互啄</span> 👍（0） 💬（0）<div>再来看看 重温重温。感谢老师 这个教程 是我入门网络编程的领路人。我是做iOS开发的 因为一些原因转到网络这边 一开始一头懵逼 学习了老师的教程就清晰了很多。后面接触到的知识 老师的教程都能引申到 真的很赞。</div>2022-07-26</li><br/><li><img src="" width="30px"><span>刘系</span> 👍（0） 💬（2）<div>第二课后题：当描述字大于channel_map的容量时，map_make_space会被调用。在map初始化时，容量为0，往map里写描述字时先给容量为32，如果描述字仍然大于等于32将会使容量右移一位，也就是描述字容量增加两倍再与要写入的描述字进行比较，直至容量大于要写入的描述字。然后使用realloc进行空间开辟，保留原有空间，扩展新空间。将新空间内存置0。最后更新map</div>2019-10-21</li><br/>
</ul>