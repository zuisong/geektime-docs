你好，我是蒋德钧。

从今天这节课开始，我们又将进入一个新的模块，也就是可靠性保证模块。在这个模块中，我会先带你了解Redis数据持久化的实现，其中包括Redis内存快照RDB文件的生成方法，以及AOF日志的记录与重写。了解了这部分内容，可以让你掌握RDB文件的格式，学习到如何制作数据库镜像，并且你也会进一步掌握AOF日志重写对Redis性能的影响。

然后，我还会围绕Redis主从集群的复制过程、哨兵工作机制和故障切换这三个方面，来给你介绍它们的代码实现。因为我们知道，主从复制是分布式数据系统保证可靠性的一个重要机制，而Redis就给我们提供了非常经典的实现，所以通过学习这部分内容，你就可以掌握到在数据同步实现过程中的一些关键操作和注意事项，以免踩坑。

好，那么今天这节课，我们就先从RDB文件的生成开始学起。下面呢，我先带你来了解下RDB创建的入口函数，以及调用这些函数的地方。

## RDB创建的入口函数和触发时机

Redis源码中用来创建RDB文件的函数有三个，它们都是在[rdb.c](http://github.com/redis/redis/tree/5.0/src/rdb.c)文件中实现的，接下来我就带你具体了解下。

- **rdbSave函数**

这是Redis server在本地磁盘创建RDB文件的入口函数。它对应了Redis的save命令，会在save命令的实现函数saveCommand（在rdb.c文件中）中被调用。而rdbSave函数最终会调用rdbSaveRio函数（在rdb.c文件中）来实际创建RDB文件。rdbSaveRio函数的执行逻辑就体现了RDB文件的格式和生成过程，我稍后向你介绍。
<div><strong>精选留言（3）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/16/25/7f/473d5a77.jpg" width="30px"><span>曾轼麟</span> 👍（21） 💬（0）<div>先回答老师的问题：serverCron函数中，查找到 rdbSaveBackground 函数一共会被调用执行几次？

    答：包含直接或者间接，一共调用了4次（不知道还有没有漏的）

    1、【直接调用】：server.c(1296行)
        如果达到了更改量阈值，等待秒数阈值，延时失败重试达到时间，会进行一次调用。

    2、【直接调用】：server.c(1369行)
        bgsave因为AOF重写的原有被迫推迟，所以在最后需要重新调用。

    3、【间接调用】：replicationCron(1340行) -&gt; startBgsaveForReplication -&gt; rdbSaveBackground
        主从复制定时任务，通过startBgsaveForReplication，触发的RDB文件保存。

    4、【间接调用】：backgroundSaveDoneHandler(1261行) -&gt; backgroundSaveDoneHandlerDisk&#47;backgroundSaveDoneHandlerSocket -&gt; updateSlavesWaitingBgsave -&gt; startBgsaveForReplication -&gt; rdbSaveBackground
        如果当前的进程角度是rdb_child_pid子进程，在结束bgsave后可能有机器在等待RDB文件，那么会调用 updateSlavesWaitingBgsave，从而间接的可能调用startBgsaveForReplication函数


补充总结：
    本期老师主要介绍了Redis的持久化做法和RDB文件的编码方式，包括文件头部的编码方式，文件的键值对写入的编码方式，还有写入的触发时机等等，也方便我们日后自行解析RDB文件。

    此外在本次源码中多次出现了RIO的标识，这里解释一下，RIO其实是unix下的一款IO包，起本质是封装了操作系统I&#47;O，能通过缓冲区的方式调用操作系统I&#47;O去对文件进行读写，此外Redis在保存RDB文件也使用了一些技巧，例如在rdbSave函数中，文件是先写入tmpfile（临时文件）的，最后通过rename的方式修改文件名字来替换掉整个文件，这是安全的文件写入方式，如果在写入期间掉电也并不会导致旧RDB文件损坏，但是也证明在磁盘预留上是需要双倍空间的。</div>2021-09-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/90/8a/288f9f94.jpg" width="30px"><span>Kaito</span> 👍（9） 💬（1）<div>1、RDB 文件是 Redis 的数据快照，以「二进制」格式存储，相比 AOF 文件更小，写盘和加载时间更短

2、RDB 在执行 SAVE &#47; BGSAVE 命令、定时 BGSAVE、主从复制时产生

3、RDB 文件包含文件头、数据部分、文件尾

4、文件头主要包括 Redis 的魔数、RDB 版本、Redis 版本、RDB 创建时间、键值对占用的内存大小等信息

5、文件数据部分包括整个 Redis 数据库中存储的所有键值对信息

- 数据库信息：db 编号、db 中 key 的数量、过期 key 的数量、键值数据
- 键值数据：过期标识、时间戳（绝对时间）、键值对类型、key 长度、key、value 长度、value

6、文件尾保存了 RDB 的结束标记、文件校验值

7、RDB 存储的数据，为了压缩体积，还做了很多优化:

- 变长编码存储键值对数据
- 用操作码标识不同的内容
- 可整数编码的内容使用整数类型紧凑编码

课后题：在 serverCron 函数中，rdbSaveBackground 函数一共会被调用执行几次？这又分别对应了什么场景？

在 serverCron 函数中 rdbSaveBackground 会被调用 2 次。

一次是满足配置的定时 RDB 条件后（save &lt;seconds&gt; &lt;changes），触发子进程生成 RDB。

另一次是客户端执行了 BGSAVE 命令，Redis 会先设置 server.rdb_bgsave_scheduled = 1，之后 serverCron 函数判断这个变量为 1，也会触发子进程生成 RDB。</div>2021-09-07</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTKrAnvnf7bm30wuzkns2eLt15libqTv5ardAAQZNx67NuHPzib0kVXaFHGHE7IE19IiargjtWJgC9D9g/132" width="30px"><span>Geek_6580e3</span> 👍（0） 💬（0）<div>老师好，能咨询个问题，redis321版本是有unknown RDB format version：7 #3353的bug吗，使用中遇到这个问题，但不知道什么情况下会触发，谢谢</div>2022-02-10</li><br/>
</ul>