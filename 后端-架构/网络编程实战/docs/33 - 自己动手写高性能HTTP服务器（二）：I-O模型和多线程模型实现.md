你好，我是盛延敏，这里是网络编程实战第33讲，欢迎回来。

这一讲，我们延续第32讲的话题，继续解析高性能网络编程框架的I/O模型和多线程模型设计部分。

## 多线程设计的几个考虑

在我们的设计中，main reactor线程是一个acceptor线程，这个线程一旦创建，会以event\_loop形式阻塞在event\_dispatcher的dispatch方法上，实际上，它在等待监听套接字上的事件发生，也就是已完成的连接，一旦有连接完成，就会创建出连接对象tcp\_connection，以及channel对象等。

当用户期望使用多个sub-reactor子线程时，主线程会创建多个子线程，每个子线程在创建之后，按照主线程指定的启动函数立即运行，并进行初始化。随之而来的问题是，**主线程如何判断子线程已经完成初始化并启动，继续执行下去呢？这是一个需要解决的重点问题。**

在设置了多个线程的情况下，需要将新创建的已连接套接字对应的读写事件交给一个sub-reactor线程处理。所以，这里从thread\_pool中取出一个线程，**通知这个线程有新的事件加入。而这个线程很可能是处于事件分发的阻塞调用之中，如何协调主线程数据写入给子线程，这是另一个需要解决的重点问题。**
<div><strong>精选留言（26）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/11/9c/62/f625b2bb.jpg" width="30px"><span>酸葡萄</span> 👍（6） 💬（1）<div>老师,你好,有个地方不是很明白,
为什么event_loop_channel_buffer_nolock(eventLoop, fd, channel1, type);是往子线程的数据中增加需要处理的 channel event 对象呢?

void event_loop_channel_buffer_nolock(struct event_loop *eventLoop, int fd, struct channel *channel1, int type) {
    &#47;&#47;add channel into the pending list
    struct channel_element *channelElement = malloc(sizeof(struct channel_element));
    channelElement-&gt;channel = channel1;
    channelElement-&gt;type = type;&#47;&#47;1 add  (1: add  2: delete)
    channelElement-&gt;next = NULL;
    &#47;&#47;第一个元素  channel_element是channel的链表，
    &#47;&#47; eventLoop pending_head和pending_tail维护的是channelElement的链表
    &#47;&#47;这样的话最终还是event_loop包含了channel(event_loop-&gt;channelElement-&gt;channel)
    if (eventLoop-&gt;pending_head == NULL) {
        eventLoop-&gt;pending_head = eventLoop-&gt;pending_tail = channelElement;
    } else {
        eventLoop-&gt;pending_tail-&gt;next = channelElement;
        eventLoop-&gt;pending_tail = channelElement;
    }
}


void *event_loop_thread_run(void *arg) {
    struct event_loop_thread *eventLoopThread = (struct event_loop_thread *) arg;

    pthread_mutex_lock(&amp;eventLoopThread-&gt;mutex);

    &#47;&#47; 初始化化event loop，之后通知主线程
    eventLoopThread-&gt;eventLoop = event_loop_init_with_name(eventLoopThread-&gt;thread_name);
    yolanda_msgx(&quot;event loop thread init and signal, %s&quot;, eventLoopThread-&gt;thread_name);
    pthread_cond_signal(&amp;eventLoopThread-&gt;cond);

    pthread_mutex_unlock(&amp;eventLoopThread-&gt;mutex);

    &#47;&#47;子线程event loop run
    event_loop_run(eventLoopThread-&gt;eventLoop);
}
struct event_loop_thread {
    struct event_loop *eventLoop;&#47;&#47;主线程和子线程共享
    pthread_t thread_tid;        &#47;* thread ID *&#47;
    pthread_mutex_t mutex;
    pthread_cond_t cond;
    char * thread_name;
    long thread_count;    &#47;* # connections handled *&#47;
};


event_loop_channel_buffer_nolock这个函数中是往eventLoop的链表中注册事件,可是这里的eventLoop是和子线程处理函数
event_loop_thread_run中eventLoopThread-&gt;eventLoop不是一个eventLoop啊,这个eventLoopThread-&gt;eventLoop不才是主子线程共享的吗?</div>2019-12-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1b/d0/48/0a865673.jpg" width="30px"><span>时间</span> 👍（5） 💬（4）<div>线程池个数有限，如何处理成千上万的链接？假如线程池共四个线程，正在处理四个链接。再来一个链接如何处理呢？</div>2020-09-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/20/dd/6e/8f6f79d2.jpg" width="30px"><span>YUAN</span> 👍（4） 💬（1）<div>为什么不直接让子线程自己调用accept而要主线程调用呢？</div>2020-12-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/6c/a8/1922a0f5.jpg" width="30px"><span>郑祖煌</span> 👍（2） 💬（1）<div>第一道， 可以直接在应用层上将输入的线程个数*2 。  第二道，(1)可以判断已经创建好的线程 那个线程的事件个数最少，挂在事件最少的那个线程上。 </div>2020-07-15</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/25/85/34/ad4cbfe4.jpg" width="30px"><span>消失的时光</span> 👍（1） 💬（4）<div>老师你好，不是很理解为什么要socketpair唤醒，直接把新连接的socket加到epoll里面，有发送就的数据过来，这个线程自己不会醒吗？</div>2022-01-07</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/73/9b/67a38926.jpg" width="30px"><span>keepgoing</span> 👍（1） 💬（2）<div>想问问老师关于基础语法的问题，代码里很多地方对象都是相互引用的，比如tcp_connection里引用了channel指针, channel 对象里引用了tcp_connection指针, dispatcher里引用了event_loop指针, event_loop里也引用了dispatcher指针。这样代码编译的时候为什么不会引起报错。。</div>2020-08-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/23/c1/54ef6885.jpg" width="30px"><span>MoonGod</span> 👍（1） 💬（2）<div>老师关于加锁这里有个疑问，如果加锁的目的是让主线程等待子线程初始化event loop。那不加锁不是也可以达到这个目的吗？主线程while 循环里面不断判断子线程的event loop是否不为null不就可以了？为啥一定要加一把锁呢？</div>2019-10-23</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/IPdZZXuHVMibwfZWmm7NiawzeEFGsaRoWjhuN99iaoj5amcRkiaOePo6rH1KJ3jictmNlic4OibkF4I20vOGfwDqcBxfA/132" width="30px"><span>鱼向北游</span> 👍（1） 💬（3）<div>netty选子线程是两种算法，都是有个原子自增计数，如果线程数不是2的幂用取模，如果是就是按位与线程数减一</div>2019-10-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/28/d2/c7/b7f52df2.jpg" width="30px"><span>雨里</span> 👍（0） 💬（2）<div>没有看明白主从reactor这个主线程是如何唤醒子线程的？？？
1、就单reactor而言，主线程创建管道fd，正常来说应该是在epoll_wait上注册0端读事件，往管道1端写数据的方式来唤醒epoll。
2、而主从reactor代码来看，主线程和子线程都创建了一对pairfd，主线程的管道1端注册在主线程的epoll上，这样即使往管道中写数据，也只是唤醒主线程，怎么会唤醒子线程呢？？，代码中好像没有将主线程的管道fd一端注册在子线程的epoll上。是不是下面的这行代码导致的
eventLoop-&gt;eventDispatcher = &amp;poll_dispatcher;
主线程和子线程共用一个同一个poll_dispatcher对象，还是没有看出在哪个地方传递的fd??</div>2022-02-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/6b/aa/ec09c4b4.jpg" width="30px"><span>zssdhr</span> 👍（0） 💬（1）<div>老师，关于 event_loop_thread 有两个问题。

1. 为什么主线程要等待子线程初始化完成？是担心 tcp_server_init 后、但子线程还未初始化完成时，thread_pool_get_loop 无法找到子线程来处理新来的连接吗？

2. 文中提到”你可能会问，主线程是循环在等待每个子线程完成初始化，如果进入第二个循环，等待第二个子线程完成初始化，而此时第二个子线程已经初始化完成了，该怎么办？“
主线程不是等第一个子线程初始化完成后才会进入下一个循环启动第二个子线程吗？怎么会出现”而此时第二个子线程已经初始化完成了“？</div>2022-02-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/28/b4/3c/e4a08d98.jpg" width="30px"><span>Janus Pen</span> 👍（0） 💬（1）<div>老师：event_loop_do_channel_event函数中的event_loop_handle_pending_channel函数调用与event_loop_run函数中的event_loop_handle_pending_channel函数调用是否重复?</div>2022-01-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/2a/31/17/ab2c27a6.jpg" width="30px"><span>菜鸡互啄</span> 👍（0） 💬（1）<div>老师你好 关于第二点 是不是相当于没有需要遍历的描述符 导致一直卡在poll或者select上。所以手动构造socketpair作为初始描述符。再添加真正新的描述符时 用socketpair把程序从poll或者select阻塞上解放出来 以获取达到添加描述符的时机？我的理解对吗？</div>2022-01-05</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/ed/6c/6fb35017.jpg" width="30px"><span>群书</span> 👍（0） 💬（1）<div>老师你好，逻辑线程写数据到发送队列，同时通知唤醒io线程，这个通知方式目前比较常规的做法是套接字对或者事件fd 实际测试下来 都会增加主线程的系统调用 有什么优化办法呢</div>2021-11-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/20/dd/6e/8f6f79d2.jpg" width="30px"><span>YUAN</span> 👍（0） 💬（1）<div>主线程和丛线程不是共享内存吗？为什么还要socketpair唤醒呢？</div>2020-12-04</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/82/3d/356fc3d6.jpg" width="30px"><span>忆水寒</span> 👍（0） 💬（4）<div>老师，main-EventLoop和sub-EventLoop里面的eventLoop-&gt;eventDispatcher = &amp;epoll_dispatcher;都是指向一个epoll_dispatcher。其中main-EventLoop用于accept新连接，获得新连接封装channel交给某一个sub-EventLoop去处理。假如dispatch有事件，是不是子线程也会从dispatch处惊醒，这是不是有“惊群效应”吗？</div>2020-09-06</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1e/d5/70/93a34aa5.jpg" width="30px"><span>Geek_76f04f</span> 👍（0） 💬（1）<div>老师您好，我有个问题想咨询一下，我看资料说线程或者进程需要绑定内核，减少上下文切换，像这种reactor模型中，如果开辟corenum个线程，一般需要绑定内核吗？</div>2020-06-02</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/db/64/06d54a80.jpg" width="30px"><span>中年男子</span> 👍（0） 💬（2）<div>event_loop_init中，代码片段：
event_loop_add_channel_event(eventLoop, eventLoop-&gt;socketPair[0], channel);
其中传入的应该是socketPair[1]
文稿中的代码还未修正，另外我认为这个fd作为参数实际上没有意义，event_loop_add_channel_event 往后调用的几个函数里实际上都用不到这个fd，只需要channel 就可以了，因为channel里已有这个fd。</div>2020-04-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/18/2a/9c18a3c4.jpg" width="30px"><span>wzp</span> 👍（0） 💬（1）<div>干货满满，有收获</div>2020-02-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/19/51/29/24739c58.jpg" width="30px"><span>凉人。</span> 👍（0） 💬（1）<div>比较难。但多看几遍还是有收获</div>2020-02-13</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/DYAIOgq83errIIarFicghpKamvkUaJmGdIV488iaOUyUqcTwbQ6IeRS40ZFfIOfb369fgleydAT8pkucHuj2x45A/132" width="30px"><span>xupeng1644</span> 👍（0） 💬（2）<div>event_loop_init中，代码片段：
event_loop_add_channel_event(eventLoop, eventLoop-&gt;socketPair[0], channel);
其中传入的应该是socketPair[1]吧。</div>2020-02-10</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/IPdZZXuHVMibwfZWmm7NiawzeEFGsaRoWjhuN99iaoj5amcRkiaOePo6rH1KJ3jictmNlic4OibkF4I20vOGfwDqcBxfA/132" width="30px"><span>鱼向北游</span> 👍（0） 💬（2）<div>回老师上一条 把代码netty贴过来了
     private static final class PowerOfTwoEventExecutorChooser implements EventExecutorChooser {
        private final AtomicInteger idx = new AtomicInteger();
        private final EventExecutor[] executors;

        PowerOfTwoEventExecutorChooser(EventExecutor[] executors) {
            this.executors = executors;
        }

        @Override
        public EventExecutor next() {
            return executors[idx.getAndIncrement() &amp; executors.length - 1];
        }
    }

    private static final class GenericEventExecutorChooser implements EventExecutorChooser {
        private final AtomicInteger idx = new AtomicInteger();
        private final EventExecutor[] executors;

        GenericEventExecutorChooser(EventExecutor[] executors) {
            this.executors = executors;
        }

        @Override
        public EventExecutor next() {
            return executors[Math.abs(idx.getAndIncrement() % executors.length)];
        }
    }</div>2019-10-29</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/DYAIOgq83eqyicZYyW7ahaXgXUD8ZAS8x0t8jx5rYLhwbUCJiawRepKIZfsLdkxdQ9XQMo99c1UDibmNVfFnAqwPg/132" width="30px"><span>程序水果宝</span> 👍（0） 💬（2）<div>求完整的代码链接</div>2019-10-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1f/a9/ce/23f2e185.jpg" width="30px"><span>Running man</span> 👍（1） 💬（0）<div>老师您好，子线程channel以及channel_element对象都是动态分配的内存，但在连接close后并未看到释放，是否是内存泄露了？</div>2022-09-01</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/37/e6/48/c8ca3db6.jpg" width="30px"><span>Y.X</span> 👍（0） 💬（0）<div>老师，请问怎么从概念上区分event和channel?</div>2023-07-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/8d/d2/498cd2d1.jpg" width="30px"><span>程序员班吉</span> 👍（0） 💬（0）<div>这篇也卡了好久，其实核心要解决的问题就是主线程要等当前子线程初始化完并跑起来之后才能再去初始化下一个线程。
这里如果把cond_wait改成一个while(event_loop == null)会好理解点，这里的even_loop是判断子线程是否就绪的依据。

但是我们知道while循环会造成非常大的cpu开销。最理想的情况是，event_loop为null的时候，我们等在这里，当event_loop不为空的时候通知一下我，这期间不消耗任何cpu资源。这个理想情况就是cond条件变量。

我们看第一种情况，假如父线程先获取到锁，由于event_loop还没有初始化好，所以进入到cond_wait，同时会释放锁进入到睡眠状态。此时子线程获取到锁，初始化完之后调用cond_signal。此时父线程从cond_wait唤醒，并在此持有锁，进入到下一次循环，此时event_loop一定是不等于null的，所以跳出循环，释放锁继续执行后面的代码。

第二种情况，子线程先拿到锁，此时父线程阻塞在mutex_lock，当子线程释放锁之后event_loop已经初始化好，然后父进程拿到锁，进入while(event
_loo)循环，event_loop不等于null，跳出循环，释放锁。

所以老师说cond_wait有必要持有锁吗？答案是要的。

理解这部分内容需要有一些前置知识，比如如果不知道cond的运行机制就很难理解cond_wait这行的意义，这又是整个实现的关键。</div>2023-07-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/2a/31/17/ab2c27a6.jpg" width="30px"><span>菜鸡互啄</span> 👍（0） 💬（0）<div>老师你好 最近在用C++重写示例代码。我发现个问题。在C代码中 不同线程同时在poll同一份event_set。如果poll函数时间参数写成-1。多启几个终端执行nc指令。经常会出现没有callback的现象。如果poll不是同一份event_set 就没有这个问题。网上也有别人的一些讨论。对此老师怎么看。望回复。https:&#47;&#47;stackoverflow.com&#47;questions&#47;18891500&#47;multiple-threads-doing-poll-or-select-on-a-single-socket-or-pipe</div>2022-09-07</li><br/>
</ul>