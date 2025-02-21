你好，我是蒋德钧。

在上节课，我给你介绍了AOF重写过程，其中我带你重点了解了AOF重写的触发时机，以及AOF重写的基本执行流程。现在你已经知道，AOF重写是通过重写子进程来完成的。

但是在上节课的最后，我也提到了在AOF重写时，主进程仍然在接收客户端写操作，**那么这些新写操作会记录到AOF重写日志中吗？如果需要记录的话，重写子进程又是通过什么方式向主进程获取这些写操作的呢？**

今天这节课，我就来带你了解下AOF重写过程中所使用的管道机制，以及主进程和重写子进程的交互过程。这样一方面，你就可以了解AOF重写日志包含的写操作的完整程度，当你要使用AOF日志恢复Redis数据库时，就知道AOF能恢复到的程度是怎样的。另一方面，因为AOF重写子进程就是通过操作系统提供的管道机制，来和Redis主进程交互的，所以学完这节课之后，你还可以掌握管道技术，从而用来实现进程间的通信。

好了，接下来，我们就先来了解下管道机制。

## 如何使用管道进行父子进程间通信？

首先我们要知道，当进程A通过调用fork函数创建一个子进程B，然后进程A和B要进行通信时，我们通常都需要依赖操作系统提供的通信机制，而**管道**（pipe）就是一种用于父子进程间通信的常用机制。
<div><strong>精选留言（7）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/29/7d/fe/2220c6cf.jpg" width="30px"><span>土豆种南城</span> 👍（19） 💬（0）<div>一些补充：
1. 重写子进程写入多少从父进程传来的操作后发出ack？
  答：子进程在正常的重写完成后至多再等一秒，在这一秒内如果有连续20ms没有可读事件发生，那么直接发送ack

2. 子进程收到父进程回复的ack时管道内还有数据怎么处理？
 答：父进程收到子进程ack后设置server.aof_stop_sending_diff为1，然后回复ack
子进程收到ack时会再次调用aofReadDiffFromParent尝试把管道里可能存在的数据都读出来
最后一步将aof_child_diff的内容写入文件，并将文件名rename为temp-rewriteaof-bg-pid.aof
父进程在serverCron中调用wait3来确认重写子进程执行结果，读取子进程重写的aof文件，在文件末尾再次写入子进程执行结束后父进程积累的数据，最后将文件名重命名成最终文件</div>2021-09-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/90/8a/288f9f94.jpg" width="30px"><span>Kaito</span> 👍（17） 💬（4）<div>1、AOF 重写是在子进程中执行，但在此期间父进程还会接收写操作，为了保证新的 AOF 文件数据更完整，所以父进程需要把在这期间的写操作缓存下来，然后发给子进程，让子进程追加到 AOF 文件中

2、因为需要父子进程传输数据，所以需要用到操作系统提供的进程间通信机制，这里 Redis 用的是「管道」，管道只能是一个进程写，另一个进程读，特点是单向传输

3、AOF 重写时，父子进程用了 3 个管道，分别传输不同类别的数据：

- 父进程传输数据给子进程的管道：发送 AOF 重写期间新的写操作
- 子进程完成重写后通知父进程的管道：让父进程停止发送新的写操作
- 父进程确认收到子进程通知的管道：父进程通知子进程已收到通知

4、AOF 重写的完整流程是：父进程 fork 出子进程，子进程迭代实例所有数据，写到一个临时 AOF 文件，在写文件期间，父进程收到新的写操作，会先缓存到 buf 中，之后父进程把 buf 中的数据，通过管道发给子进程，子进程写完 AOF 文件后，会从管道中读取这些命令，再追加到 AOF 文件中，最后 rename 这个临时 AOF 文件为新文件，替换旧的 AOF 文件，重写结束

课后题：Redis 中其它使用管道的地方还有哪些？

在源码中搜索 pipe 函数，能看到 server.child_info_pipe 和 server.module_blocked_pipe 也使用了管道。

其中 child_info_pipe 管道如下：

 &#47;* Pipe and data structures for child -&gt; parent info sharing. *&#47;
    int child_info_pipe[2];  &#47;* Pipe used to write the child_info_data. *&#47;
    struct {
        int process_type;           &#47;* AOF or RDB child? *&#47;
        size_t cow_size;            &#47;* Copy on write size. *&#47;
        unsigned long long magic;   &#47;* Magic value to make sure data is valid. *&#47;
    } child_info_data;


从注释能看出，子进程在生成 RDB 或 AOF 重写完成后，子进程通知父进程在这期间，父进程「写时复制」了多少内存，父进程把这个数据记录到 server 的 stat_rdb_cow_bytes &#47; stat_aof_cow_bytes 下（childinfo.c 的 receiveChildInfo 函数），以便客户端可以查询到最后一次 RDB 和 AOF 重写期间写时复制时，新申请的内存大小。

而 module_blocked_pipe 管道主要服务于 Redis module。

&#47;* Pipe used to awake the event loop if a client blocked on a module command needs to be processed. *&#47;
int module_blocked_pipe[2]; 

看注释是指，如果被 module 命令阻塞的客户端需要处理，则会唤醒事件循环开始处理。
</div>2021-09-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/2e/e5/a0/8b3e4acc.jpg" width="30px"><span>鱼鱼</span> 👍（4） 💬（0）<div>7.0之后的redis使用Multipart AOF的方式，用manifest结构管理AOF文件。
有三种类型的AOF文件
base incr和history
AOF rewrite的时候，会生成一个新的incr型的aof用于追加
写完之后把以前的base和incr改为history
保留写完后的base和写时创建的incr

这样做好处是节约内存，不需要aof_rewrite_buf，而是直接写在server.aof_buf中，通过server.aof_fd判断往哪个里面写。
当然同时也节约了CPU
减少了写入管道这种交互过程

重新根据aof恢复数据的时候是base+incrs的方式构建数据库的</div>2022-08-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/25/7f/473d5a77.jpg" width="30px"><span>曾轼麟</span> 👍（3） 💬（0）<div>首先回答老师问题：
	1、slave同步RDB文件中返回状态和错误
		通过rdb_pipe_write_result_to_parent和rdb_pipe_read_result_from_child。在进行fork之前，创建一个管道，用于将成功接收到所有写操作的slave服务器的id发送回父服务器。一般是slave在等待bgsave的情况下主库完成bgsave后进行的处理。在rdbSaveToSlavesSockets函数中调用。

	2、用于传输子进程info给父进程
		child_info_pipe，用于将RDB &#47; AOF保存进程的信息从子进程传输给父进程。（例如同步期间产生写时复制的量等信息）。

	3、唤醒由于处理module命令而阻塞的event loop
		module_blocked_pipe（具体细节还没看完）。

	4、自检函数linuxMadvFreeForkBugCheck
		针对arm64 Linux内核的一个bug（太旧的内核可能会导致数据损坏），自检时候会fork出一个子进程来进行判断是否发现bug，如果发现则响应主进程并输出日志提示升级内核。

总结：
	老师本期介绍了，在AOF重写期间，主进程产生的增量写命令是如何通过管道技术同步给子进程，（管道技术是基于内核进行的跨进程同步方案）。为此Redis实现了三种管道来完成AOF重写期间，主子进程的命令同步。三种管道分别为：
		1、父进程传输给子进程的命令管道。
		2、子进程响应父进程的ack管道。
		3、父进程确认收到子进程ack的管道。
	（这里会发现设计上多少有点和tcp握手类似）

	此外需要主意的是，在管道交互期间，读取管道的数据是通过aeCreateFileEvent创建文件事件进行的。那么结合前面的文章内容-IO多线程可以得知：在主子进程同步命令和处理ack信号是有IO线程参与的。</div>2021-09-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/17/8b/4b/15ab499a.jpg" width="30px"><span>风轻扬</span> 👍（0） 💬（0）<div>除了AOF重写时，用到了管道。我搜索了一下，源码中还有另外3个地方也用到了管道。
1、主从复制时，主向从发送RDB文件后，从会使用管道回复主，已收到RDB文件
2、server.c的main方法中，在初始化module的时候，也会调用管道。这个管道的目的是：如果客户端处理module命令阻塞时，使用该管道可以唤醒事件驱动框架
3、当进行RDB写入或者AOF写入时，子进程通过这个管道向父进程传递一些信息。比如：copyOnWrite机制使用了多少内存</div>2023-11-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1b/89/52/b96c272d.jpg" width="30px"><span>🤐</span> 👍（0） 💬（0）<div>以前不清楚 redis的qps那么多，什么时候才会写结束？原来是有一个通知回复机制。</div>2022-07-25</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1d/6c/b5/32374f93.jpg" width="30px"><span>可怜大灰狼</span> 👍（0） 💬（0）<div>回答问题。
1.rdbSaveBackground。2.rdbSaveToSlavesSockets，diskless模式下直接把rdb通过socket发送给slave。3.moduleInitModulesSystem，和第三方子模块通信。4.linuxMadvFreeForkBugCheck，检查MADV_FREE在arm64 Linux内核上bug，具体见https:&#47;&#47;github.com&#47;redis&#47;redis&#47;commit&#47;b02780c41dbc5b28d265b5cf141c03c1a7383ef9。</div>2021-09-11</li><br/>
</ul>