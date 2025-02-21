你好，我是蒋德钧。

我们知道，Redis除了使用内存快照RDB来保证数据可靠性之外，还可以使用AOF日志。不过，RDB文件是将某一时刻的内存数据保存成一个文件，而AOF日志则会记录接收到的所有写操作。如果Redis server的写请求很多，那么AOF日志中记录的操作也会越来越多，进而就导致AOF日志文件越来越大。

所以，为了避免产生过大的AOF日志文件，Redis会对AOF文件进行重写，也就是针对当前数据库中每个键值对的最新内容，记录它的插入操作，而不再记录它的历史写操作了。这样一来，重写后的AOF日志文件就能变小了。

**那么，AOF重写在哪些时候会被触发呢？以及AOF重写需要写文件，这个过程会阻塞Redis的主线程，进而影响Redis的性能吗？**

今天这节课，我就来给你介绍下AOF重写的代码实现过程，通过了解它的代码实现，我们就可以清楚地了解到AOF重写过程的表现，以及它对Redis server的影响。这样，当你再遇到Redis server性能变慢的问题时，你就可以排查是否是AOF重写导致的了。

好，接下来，我们先来看下AOF重写函数以及它的触发时机。

## AOF重写函数与触发时机

首先，实现AOF重写的函数是**rewriteAppendOnlyFileBackground**，它是在[aof.c](https://github.com/redis/redis/tree/5.0/src/aof.c)文件中实现的。在这个函数中，会调用fork函数创建一个AOF重写子进程，来实际执行重写操作。关于这个函数的具体实现，我稍后会给你详细介绍。这里呢，我们先来看看，这个函数会被哪些函数调用，这样我们就可以了解AOF重写的触发时机了。
<div><strong>精选留言（5）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/0f/90/8a/288f9f94.jpg" width="30px"><span>Kaito</span> 👍（19） 💬（5）<div>1、AOF 记录的是每个命令的「操作历史」，随着时间增长，AOF 文件会越来越大，所以需要 AOF 重写来「瘦身」，减小文件体积

2、AOF 重写时，会扫描整个实例中的数据，把数据以「命令 + 键值对」的格式，写到 AOF 文件中

3、触发 AOF 重写的时机有 4 个：

- 执行 bgrewriteaof 命令
- 手动打开 AOF 开关（config set appendonly yes）
- 从库加载完主库 RDB 后（AOF 被启动的前提下）
- 定时触发：AOF 文件大小比例超出阈值、AOF 文件大小绝对值超出阈值（AOF 被启动的前提下）

这 4 个时机，都不能有 RDB 子进程，否则 AOF 重写会延迟执行。

4、AOF 重写期间会禁用 rehash，不让父进程调整哈希表大小，目的是父进程「写时复制」拷贝大量内存页面

课后题：为什么 Redis 源码中在有 RDB 子进程运行时，不会启动 AOF 重写子进程？

无论是生成 RDB 还是 AOF 重写，都需要创建子进程，然后把实例中的所有数据写到磁盘上，这个过程中涉及到两块：

- CPU：写盘之前需要先迭代实例中的所有数据，在这期间会耗费比较多的 CPU 资源，两者同时进行，CPU 资源消耗大
- 磁盘：同样地，RDB 和 AOF 重写，都是把内存数据落盘，在这期间 Redis 会持续写磁盘，如果同时进行，磁盘 IO 压力也会较大

整体来说都是为了资源考虑，所以不会让它们同时进行。</div>2021-09-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/25/7f/473d5a77.jpg" width="30px"><span>曾轼麟</span> 👍（7） 💬（0）<div>先回答老师的问题：RDB和AOF进程为什么不能同时运行？
答：有多方的原因
    1、AOF-RDB混合持久化
        现在Redis官方主推的是AOF-RDB混合持久化方案，同时运行AOF进程重写和RDB进程保存必然会带来不必要的冲突。

    2、两个都是fork出来的
        由于AOF重写进程和RDB保存进程都是通过fork出来的，AOF在重写期间还会继续保存来自主进程的命令操作，那么同时运行必然带来风险也需要考虑更多问题。

    3、更高的资源消耗 
        AOF和RDB都是高IO的操作，而且业务场景也非必须同时进行，同时进行对资源是较大的浪费。

总结：
    本次老师介绍了AOF重写是如何进行的，和上一篇文章一样AOF重写是高IO操作，并且是一个异步缓慢的过程为了避免阻塞主进程Redis是通过fork子进程进行的，但是与RDB不同的是AOF重写期间还需要同步重写期间来自主进程的命令，并在重写完成后同步到文件中，在这里老师也引出了管道技术，为AOF进程同步主进程命令买下伏笔（期待老师的下篇文章）

    其次值得注意的是updateDictResizePolicy函数，文章中提到updateDictResizePolicy是在AOF进行中调用，目的是为了阻止渐进式Rehash从而减少【写时复制】带来的大量内存开销，除了AOF意外其实bgsave 异步保存RDB文件也会调用这个方法来避免同样的问题。</div>2021-09-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/8a/a7/674c1864.jpg" width="30px"><span>William</span> 👍（0） 💬（3）<div>这里有疑问，“在父进程中，这个 rewriteAppendOnlyFileBackground 函数会把 aof_rewrite_scheduled 变量设置为 0，同时记录 AOF 重写开始的时间，以及记录 AOF 子进程的进程号。”

我看这是if..else 结构呀？ 进来的时候 是 if ((childpid = fork()) == 0) { ....} , 怎么会既有fork子进程重写AOF, 又有父进程，对这个标记调整为0 ？ 

查到的资料： fock函数调用一次却返回两次；向父进程返回子进程的ID，向子进程中返回0；

所以父子进程的业务逻辑都会执行。

请老师解惑是不是这样？ </div>2021-09-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/60/a1/45ffdca3.jpg" width="30px"><span>静心</span> 👍（0） 💬（1）<div>我有一个疑问没搞明白：
在AOF重写的时候，是新创建一个文件来写，写完之后再替换旧的AOF文件呢？还是重写先在内存中进行，然后再覆盖旧的AOF文件？</div>2021-09-15</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/f3/cf/851dab01.jpg" width="30px"><span>Milittle</span> 👍（0） 💬（1）<div>问答题：我的考虑是为了并发安全</div>2021-09-09</li><br/>
</ul>