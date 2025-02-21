你好，我是蒋德钧。

通过上节课的学习，我们知道Redis server启动后的进程会以单线程的方式，执行客户端请求解析和处理工作。但是，Redis server也会通过bioInit函数启动三个后台线程，来处理后台任务。也就是说，Redis不再让主线程执行一些耗时操作，比如同步写、删除等，而是交给后台线程异步完成，从而避免了对主线程的阻塞。

实际上，在2020年5月推出的Redis 6.0版本中，Redis在执行模型中还进一步使用了多线程来处理IO任务，这样设计的目的，就是为了充分利用当前服务器的多核特性，使用多核运行多线程，让多线程帮助加速数据读取、命令解析以及数据写回的速度，提升Redis整体性能。

**那么，这些多线程具体是在什么时候启动，又是通过什么方式来处理IO请求的呢？**

今天这节课，我就来给你介绍下Redis 6.0实现的多IO线程机制。通过这部分内容的学习，你可以充分了解到Redis 6.0是如何通过多线程来提升IO请求处理效率的。这样你也就可以结合实际业务来评估，自己是否需要使用Redis 6.0了。

好，接下来，我们先来看下多IO线程的初始化。注意，因为我们之前课程中阅读的是Redis 5.0.8版本的代码，所以在开始学习今天的课程之前，你还需要下载[Redis 6.0.15](https://github.com/redis/redis/tree/6.0)的源码，以便能查看到和多IO线程机制相关的代码。
<div><strong>精选留言（15）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/0f/90/8a/288f9f94.jpg" width="30px"><span>Kaito</span> 👍（37） 💬（0）<div>1、Redis 6.0 之前，处理客户端请求是单线程，这种模型的缺点是，只能用到「单核」CPU。如果并发量很高，那么在读写客户端数据时，容易引发性能瓶颈，所以 Redis 6.0 引入了多 IO 线程解决这个问题

2、配置文件开启 io-threads N 后，Redis Server 启动时，会启动 N - 1 个 IO 线程（主线程也算一个 IO 线程），这些 IO 线程执行的逻辑是 networking.c 的 IOThreadMain 函数。但默认只开启多线程「写」client socket，如果要开启多线程「读」，还需配置 io-threads-do-reads = yes

3、Redis 在读取客户端请求时，判断如果开启了 IO 多线程，则把这个 client 放到 clients_pending_read 链表中（postponeClientRead 函数），之后主线程在处理每次事件循环之前，把链表数据轮询放到 IO 线程的链表（io_threads_list）中

4、同样地，在写回响应时，是把 client 放到 clients_pending_write 中（prepareClientToWrite 函数），执行事件循环之前把数据轮询放到 IO 线程的链表（io_threads_list）中

5、主线程把 client 分发到 IO 线程时，自己也会读写客户端 socket（主线程也要分担一部分读写操作），之后「等待」所有 IO 线程完成读写，再由主线程「串行」执行后续逻辑

6、每个 IO 线程，不停地从 io_threads_list 链表中取出 client，并根据指定类型读、写 client socket

7、IO 线程在处理读、写 client 时有些许差异，如果 write_client_pedding &lt; io_threads * 2，则直接由「主线程」负责写，不再交给 IO 线程处理，从而节省 CPU 消耗

8、Redis 官方建议，服务器最少 4 核 CPU 才建议开启 IO 多线程，4 核 CPU 建议开 2-3 个 IO 线程，8 核 CPU 开 6 个 IO 线程，超过 8 个线程性能提升不大

9、Redis 官方表示，开启多 IO 线程后，性能可提升 1 倍。当然，如果 Redis 性能足够用，没必要开 IO 线程

课后题：为什么 startThreadedIO &#47; stopThreadedIO 要执行加解锁？

既然涉及到加锁操作，必然是为了「互斥」从而控制某些逻辑。可以在代码中检索这个锁变量，看存在哪些逻辑对 io_threads_mutex 操作了加解锁。

跟踪代码可以看到，在 networking.c 的 IOThreadMain 函数，也对这个变量进行了加解锁操作，那就说明 startThreadedIO &#47; stopThreadedIO 函数，可以控制 IOThreadMain 里逻辑的执行，IOThreadMain 代码如下。

void *IOThreadMain(void *myid) {
    ...
    while(1) {
        ...
        &#47;* Give the main thread a chance to stop this thread. *&#47;
        if (io_threads_pending[id] == 0) {
            pthread_mutex_lock(&amp;io_threads_mutex[id]);
            pthread_mutex_unlock(&amp;io_threads_mutex[id]);
            continue;
        }
        &#47;&#47; 读写 client socket 
        &#47;&#47; ...
    }


这个函数正是 IO 多线程的主逻辑。

从注释可以看到，这是为了给主线程停止 IO 线程的的机会。也就是说，这里的目的是为了让主线程可以控制 IO 线程的开启 &#47; 暂停。

因为每次 IO 线程在执行时必须先拿到锁，才能执行后面的逻辑，如果主线程执行了 stopThreadedIO，就会先拿到锁，那么 IOThreadMain 函数在执行时就会因为拿不到锁阻塞「等待」，这就达到了 stop IO 线程的目的。

同样地，调用 startThreadedIO 函数后，会释放锁，IO 线程就可以拿到锁，继续「恢复」执行。
</div>2021-08-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/25/7f/473d5a77.jpg" width="30px"><span>曾轼麟</span> 👍（8） 💬（1）<div>一样首先回答老师的问题，你知道为什么这两个函数要执行解锁和加锁操作么？

答案：是为了方便主线程动态，灵活调整IO线程而设计的，当clients数量较少的时候可以方便直接停止IO线程。停止IO线程的阈值是，当等待写的client客户端数量小于IO线程数量的两倍，就会停止IO线程避免多线程带来不必要的开销

回归代码：
1、stopThreadedIO，startThreadedIO 和 stopThreadedIOIfNeeded这三个函数中有体现，其中在stopThreadedIOIfNeeded中会判断当前待写出客户端数量是否大于2倍IO线程数量，如果不是则会调用stopThreadedIO函数通过io_threads_mutex的方式停止所有IO线程（主线程除外，因为index是从1开始的）并且将io_threads_active设置为0，并且后续调用stopThreadedIOIfNeeded函数会返回0，在handleClientsWithPendingWritesUsingThreads函数中会直接调用handleClientsWithPendingWrites来使用单线程进行写出。

    流程如下：
        第一次：handleClientsWithPendingWritesUsingThreads -&gt; stopThreadedIOIfNeeded -&gt; stopThreadedIO -&gt; 设置io_threads_active为0并lock住IO线程
        第二次: handleClientsWithPendingWritesUsingThreads -&gt; stopThreadedIOIfNeeded -&gt; 直接返回1 -&gt; handleClientsWithPendingWrites进行单线程处理

2、当待写出client的数量上来的时候，stopThreadedIOIfNeeded函数中判断，待写出client数量大于2倍IO线程数量，返回0，然后调用startThreadedIO激活IO线程
    
    流程如下：
        handleClientsWithPendingWritesUsingThreads -&gt; stopThreadedIOIfNeeded(发现不满足需要IO线程，返回0) -&gt; startThreadedIO(激活IO线程) -&gt; 设置io_threads_active为1

此外注意：IO线程一定是处理完了所有client之后，才会倍lock，在IOThreadMain有一个条件 if (getIOPendingCount(id) == 0) 

总结：
    本篇文章，老师带我们了解了IO线程的设计原理和多IO给Redis带了了性能上的提升，从代码中可以看出，IO线程的数量并不是随心所欲的设置的，应当结合Redis client的数量而定的，并且上限是128，此外IO线程，是和主线程共同协调运行的，最典型的就是主线程通过控制io_threads_op来协调IO线程是同步读取还是写入

建议:
    IO线程这块其实还涉及一个比较大的内容，就是RESP的协议编解码，IO线程虽然不涉及命令执行，但是会协助主线程进行协议编解码，而RESP协议的设计很巧妙，对粘包拆包等处理也是其一大亮点</div>2021-08-31</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/29/7d/fe/2220c6cf.jpg" width="30px"><span>土豆种南城</span> 👍（3） 💬（0）<div>回答课后题：为什么 startThreadedIO &#47; stopThreadedIO 要执行加解锁？
几个评论都提到这部分代码：

&#47;* Give the main thread a chance to stop this thread. *&#47;
if (io_threads_pending[id] == 0) {
    pthread_mutex_lock(&amp;io_threads_mutex[id]);
    pthread_mutex_unlock(&amp;io_threads_mutex[id]);
    continue;
}
我觉得光看这里还不够，还应该结合这部分代码的前面一段来看：

&#47;* Wait for start *&#47;
for (int j = 0; j &lt; 1000000; j++) {
    if (getIOPendingCount(id) != 0) break;
}
&#47;* Give the main thread a chance to stop this thread. *&#47;
if (io_threads_pending[id] == 0) {
    pthread_mutex_lock(&amp;io_threads_mutex[id]);
    pthread_mutex_unlock(&amp;io_threads_mutex[id]);
    continue;
}
总体逻辑是这样的，io子线程启动后直接一入一段“狂热”时间，子线程会积极响应主线程设置的任务。但是如果一段时间（一百万次循环）之后任务数量还是0会发生两种情况：

1. 主线程没打开多线程模式（没有调用过startThreadedIO），这情况可能是主线程本身就没收到任何请求，也可能是主线程觉得不需要子线程来处理（stopThreadedIOIfNeeded）
2. 主线程打开了多线程模式，但是还没来得及调用setIOPendingCount设置任务
1情况下pthread_mutex_lock会阻塞子线程，相当于子线程进入沉睡状态了
2情况下不会阻塞子线程，子线程进入下次循环，依然处于“狂热”状态，只要主线程调用setIOPendingCount就可以立即工作
综上，startThreadedIO的解锁操作相当于是“唤醒”了子线程在“狂热”状态未满足下进入的沉睡。stopThreadedIO能让子线程在一个阶段的“狂热”结束后进入沉睡</div>2021-09-05</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/af/62/5eeb9041.jpg" width="30px"><span>里咯破</span> 👍（1） 💬（0）<div>redis6刚出时用redis-benchmark 测试过,的确会有提升,get能有将近一倍,set根据数据量不同有20%~40%的提升.但是只是单机测试,没有考虑网络环境.</div>2021-09-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1d/6c/b5/32374f93.jpg" width="30px"><span>可怜大灰狼</span> 👍（1） 💬（0）<div>networking.c中IOThreadMain方法有如下一小段代码：
&#47;* Give the main thread a chance to stop this thread. *&#47;
if (getIOPendingCount(id) == 0) {
       pthread_mutex_lock(&amp;io_threads_mutex[id]);
       pthread_mutex_unlock(&amp;io_threads_mutex[id]);
       continue;
 }
就像代码里说的，给主线程暂停子线程的机会。
如果主线程没有在startThreadedIO做unlock和在stopThreadedIO做lock，主线程也无法暂停和开始子线程，进而会导致cpu资源浪费。</div>2021-08-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/5c/f6/443808f8.jpg" width="30px"><span>孤独患者</span> 👍（0） 💬（1）<div>假设按顺序先后收到a、b、c三个命令，分别被线程1、2、3成功解析，redis是怎么保证主线程执行命令也是按a、b、c这个顺序的呢？</div>2024-01-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/5c/f6/443808f8.jpg" width="30px"><span>孤独患者</span> 👍（0） 💬（1）<div>多线程的话，能保证先到的命令先执行吗？虽然说执行命令还是在一个线程顺序进行，但是命令解析是在不同的线程，有没有可能后收到的命令，被先执行了？</div>2024-01-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/2c/35/18/2adbbba6.jpg" width="30px"><span>Hubery</span> 👍（0） 💬（0）<div>老师，最近遇到个问题。压测的时候，本地机子是16核的，然后redis只会把一个核打满，其他核都是空闲的，花费的时间主要是在软中断上面。不知道啥原因</div>2023-09-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/ca/07/22dd76bf.jpg" width="30px"><span>kobe</span> 👍（0） 💬（0）<div>你好，关于handleClientsWithPendingReadsUsingThreads和handleClientsWithPendingWritesUsingThreads两个方法的第四步，为什么前者是直接由主线程处理new buffers，包括解析和执行命令，而后者是注册个新的可写事件，交由事件驱动框架去处理？</div>2023-08-31</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/4b/2f/2f73fd52.jpg" width="30px"><span>水滴s</span> 👍（0） 💬（1）<div>判断所有多线程是否处理完读，这里不会造成CPU忙等待吗，为啥不使用锁条件变量实现呢？
 while(1) {
        unsigned long pending = 0;
        for (int j = 1; j &lt; server.io_threads_num; j++)
            pending += io_threads_pending[j];
        if (pending == 0) break;
    }</div>2022-06-25</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/17/5d/35/b1eb964a.jpg" width="30px"><span>🐟🐙🐬🐆🦌🦍🐑🦃</span> 👍（0） 💬（1）<div>handleClientsWithPendingReadsUsingThreads 在把clients_pending_read 放到io_threads_list 时，为啥不加锁，主线程放，消费线程读取时，不会有问题么，加入时，有指针的变更</div>2022-03-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1b/2e/ee/3457154b.jpg" width="30px"><span>YFW</span> 👍（0） 💬（0）<div>老师看了文章还有一个疑问？ 还望解答， 主线程在调用 函数initThreadedIO 的时候，会给 io_threads_mutex[i]进行加锁， 
这个时候IO子线程就无法获取到锁，只有在主线程调用 startThreadedIO 中才会把这些锁释放，
此时IO子线程才能够继续运行， 查看了源码发现startThreadedIO只会在函数handleClientsWithPendingWritesUsingThreads中被调用，
那如果只有可读事件， IO子线程不就一直pending 在 io_threads_mutex[i] 上？</div>2022-01-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/65/6a/be36c108.jpg" width="30px"><span>ikel</span> 👍（0） 💬（0）<div>你知道为什么这两个函数要执行解锁和加锁操作么？
让多线程模式下的部分子线程休眠以释放cpu资源
在networking,c文件中_Atomic unsigned long io_threads_pending[IO_THREADS_MAX_NUM]中_Atomic用法是类似于多线程中锁的作用么？这个用法没查到相关资料</div>2021-11-10</li><br/><li><img src="" width="30px"><span>Geek_3930c2</span> 👍（0） 💬（2）<div>io_threads_op为啥不用volatile修改</div>2021-09-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/f3/cf/851dab01.jpg" width="30px"><span>Milittle</span> 👍（0） 💬（0）<div>课后题我的猜测：就是对于一个线程完整的释放和触发，启动线程，将线程的mutex释放，意味着你在这个线程中，去访问一些共享资源，那么你可以使用这个mutex。关闭线程，将线程的mutex获取，让线程中其他获取mutex的能力失效。一点猜测，不知道对不对。</div>2021-08-24</li><br/>
</ul>