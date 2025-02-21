你好，我是蒋德钧。从今天这节课开始，我们将开启“Redis代码之旅”，一起来掌握Redis的核心设计思想。

不过，在正式开始我们的旅程之前，还需要先做个“攻略”，也就是要了解和掌握Redis代码的整体架构。

这是因为，一旦掌握了Redis代码的整体架构，就相当于给Redis代码画了张全景图。有了这张图，我们再去学习Redis不同功能模块的设计与实现时，就可以从图上快速查找和定位这些功能模块对应的代码文件。而且，有了代码的全景图之后，我们还可以对Redis各方面的功能特性有个全面了解，这样也便于更加全面地掌握Redis的功能，而不会遗漏某一特性。

那么，我们究竟该如何学习Redis的代码架构呢？我的建议是要掌握以下两方面内容：

- **代码的目录结构和作用划分**，目的是理解Redis代码的整体架构，以及所包含的代码功能类别；
- **系统功能模块与对应代码文件**，目的是了解Redis实例提供的各项功能及其相应的实现文件，以便后续深入学习。

实际上，当你掌握了以上两方面的内容之后，即使你要去了解和学习其他软件系统的代码架构，你都可以按照“先面后点”的方法来推进。也就是说，先了解目录结构与作用类别，再对应功能模块与实现文件，这样可以帮助你快速地掌握一个软件系统的代码全景。
<div><strong>精选留言（22）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/12/b1/50/678a529b.jpg" width="30px"><span>lison</span> 👍（1） 💬（1）<div>老师，有幸听了您的集训班，想咨询下 后续章节是否有具体版本和编译工具的介绍，后续好和您保持同步</div>2021-07-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/19/f7/60/31c5873e.jpg" width="30px"><span>Leven</span> 👍（0） 💬（1）<div>请问老师，没有c语言基础适合吗</div>2021-07-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/90/8a/288f9f94.jpg" width="30px"><span>Kaito</span> 👍（158） 💬（11）<div>重新看了一下源码目录，结合这篇文章的内容，整理了一下代码分类（忽略.h头文件），这也更清晰一些：

数据类型：
- String（t_string.c、sds.c、bitops.c）
- List（t_list.c、ziplist.c）
- Hash（t_hash.c、ziplist.c、dict.c）
- Set（t_set.c、intset.c）
- Sorted Set（t_zset.c、ziplist.c、dict.c）
- HyperLogLog（hyperloglog.c）
- Geo（geo.c、geohash.c、geohash_helper.c）
- Stream（t_stream.c、rax.c、listpack.c）

全局：
- Server（server.c、anet.c）
- Object（object.c）
- 键值对（db.c）
- 事件驱动（ae.c、ae_epoll.c、ae_kqueue.c、ae_evport.c、ae_select.c、networking.c）
- 内存回收（expire.c、lazyfree.c）
- 数据替换（evict.c）
- 后台线程（bio.c）
- 事务（multi.c）
- PubSub（pubsub.c）
- 内存分配（zmalloc.c）
- 双向链表（adlist.c）

高可用&amp;集群：
- 持久化：RDB（rdb.c、redis-check-rdb.c)、AOF（aof.c、redis-check-aof.c）
- 主从复制（replication.c）
- 哨兵（sentinel.c）
- 集群（cluster.c）

辅助功能：
- 延迟统计（latency.c）
- 慢日志（slowlog.c）
- 通知（notify.c）
- 基准性能（redis-benchmark.c）

下面解答课后问题：

Redis 从 4.0 版本开始，能够支持后台异步执行任务，比如异步删除数据，你能在 Redis 功能源码中，找到实现后台任务的代码文件么？

后台任务的代码在 bio.c 中。

Redis Server 在启动时，会在 server.c 中调用 bioInit 函数，这个函数会创建 3 类后台任务（类型定义在 bio.h 中）：

#define BIO_CLOSE_FILE    0 &#47;&#47; 后台线程关闭 fd
#define BIO_AOF_FSYNC     1 &#47;&#47; AOF 配置为 everysec，后台线程刷盘
#define BIO_LAZY_FREE     2 &#47;&#47; 后台线程释放 key 内存

这 3 类后台任务，已经注册好了执行固定的函数（消费者）：

- BIO_CLOSE_FILE 对应执行 close(fd)
- BIO_AOF_FSYNC 对应执行 fsync(fd)
- BIO_LAZY_FREE 根据参数不同，对应 3 个函数（freeObject&#47;freeDatabase&#47;freeSlowsMap）

之后，主线程凡是需要把一个任务交给后台线程处理时，就会调用 bio.c 的 bioCreateBackgroundJob 函数（相当于发布异步任务的函数），并指定该任务是上面 3 个的哪一类，把任务挂到对应类型的「链表」下（bio_jobs[type]），任务即发布成功（生产者任务完成）。

消费者从链表中拿到生产者发过来的「任务类型 + 参数」，执行上面任务对应的方法即可。当然，由于是「多线程」读写链表数据，这个过程是需要「加锁」操作的。

如果要找「异步删除数据」的逻辑，可以从 server.c 的 unlink 命令为起点，一路跟代码进去，就会看到调用了 lazyfree.c 的 dbAsyncDelete 函数，这个函数最终会调到上面提到的发布异步任务函数 bioCreateBackgroundJob，整个链条就串起来了。</div>2021-07-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/23/5b/983408b9.jpg" width="30px"><span>悟空聊架构</span> 👍（14） 💬（6）<div>回答每课一问：
Redis 从 4.0 版本开始，能够支持后台异步执行任务，比如异步删除数据，你能在 Redis 功能源码中，找到实现后台任务的代码文件么？

我翻看了 3.0 的源码，发现 3.0 就支持后台任务了。在文件 src\bio.c 里面有一个后台任务的函数：
bioProcessBackgroundJobs，支持两种后台任务：关闭文件和 AOF 文件的 fsync 也是放到后台执行的。

（fsync 就是执行命令后将命令写到日志中，提供了三种策略：Always，同步写回，Everysec，每秒写回，No，操作系统控制的写回。）

疑问：根据 3.0 源码，Redis 3.0 其实就已经有后台任务了，老师在文中说的 4.0 才开始支持后台任务，我没理解。

然后我又去翻了下 4.0 的源码，增加一种后台任务：BIO_LAZY_FREE。

当任务类型等于 BIO_LAZY_FREE 时，针对不同的传参，可以释放对象、数据库、跳跃表。

对于释放可以稍微说一下，释放的源码在这个文件里面：\src\lazyfree.c，相对 3.0 来说，这个文件是新增加的。

关于对象的释放，我们可以联想到 Java 的垃圾回收算法：可达性分析算法，但是 Redis 的垃圾回收算法用的是引用计数算法，另外 PHP 的垃圾回收算法用的也是引用计数（扩展下：用了多色标记的方式，来识别垃圾，详细参考这里：https:&#47;&#47;mp.weixin.qq.com&#47;s&#47;n6PGIgfZ8vXUZ1rkU5Otog），所以别再说引用计数不能用做垃圾回收了哦。

而对于 Redis 释放对象来说，会减少引用的次数，调用的是这个函数：decrRefCount(o); 根据函数的名字也容易理解。

吐槽下：Github 上下载源码总是下载失败，为了其他同学们方便下载，我整理了多套源码的下载地址，都是国内的网盘链接，只有几MB 大小，下载比较快的。

http:&#47;&#47;www.passjava.cn&#47;#&#47;12.Redis&#47;00.DownloadRedis</div>2021-07-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1f/7e/5a/da39f489.jpg" width="30px"><span>Ethan New</span> 👍（10） 💬（0）<div>评论区也太强了吧，瑟瑟发抖</div>2021-07-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/96/a6/aac2a550.jpg" width="30px"><span>陌</span> 👍（9） 💬（1）<div>关于作业，如果一开始对 Redis 源码不熟悉的话，我们可以借用 GDB 工具来回答 Redis 有哪些后台任务:

1) 添加 -g 的编码参数，向编译文件中添加调试信息，以便使用 GDB：

make CFLAGS=&quot;-g -O0&quot;

2) cd src &amp;&amp; gdb redis-server

3) 在 aeMain 函数处打一个断点，然后再使得程序运行至此处:
break aeMain
run

4) 查看线程信息:
info threads

这时候我们就能够看到 4 个线程的相关信息，分别是 redis-server、bio_close_file、bio_aof_fsync、bio_lazy_free，然后就可以按线程名称再去源码中查找了。</div>2021-07-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1d/6c/b5/32374f93.jpg" width="30px"><span>可怜大灰狼</span> 👍（5） 💬（0）<div>我的第一反应应该是从unlink命令入手查找。首先肯定是server.c中redisCommandTable[]中的unlinkCommand，找到了lazyfree.c中dbAsyncDelete方法，然后找到了bio.c中bioCreateBackgroundJob方法，很显然bio.h中加了一种后台IO任务类型：BIO_LAZY_FREE=2。我记得我看3.0代码还只有BIO_CLOSE_FILE和BIO_AOF_FSYNC</div>2021-07-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/26/38/ef063dc2.jpg" width="30px"><span>Darren</span> 👍（5） 💬（0）<div>bio.c
在5.x的源码中，后台异步执行又3个子线程
#define BIO_NUM_OPS       3
#define BIO_CLOSE_FILE    0 &#47;* Deferred close(2) syscall. *&#47;
#define BIO_AOF_FSYNC     1 &#47;* Deferred AOF fsync. *&#47;
#define BIO_LAZY_FREE     2 &#47;* Deferred objects freeing. *&#47;

bioInit方法中通过pthread_create创建BIO_NUM_OPS子线程，不同线程的任务在static list *bio_jobs[BIO_NUM_OPS]中存储。</div>2021-07-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/89/5b/b014ce14.jpg" width="30px"><span>小五</span> 👍（3） 💬（0）<div>1 Redis 支持 3 大类型的后台任务，它们定义在 bio.h 文件中：
&#47;* Background job opcodes 后台作业操作码
 * 1 处理关闭文件
 * 2 AOF 异步刷盘
 * 3 lazyfree
 *&#47;
#define BIO_CLOSE_FILE    0 &#47;* Deferred close(2) syscall. *&#47;
#define BIO_AOF_FSYNC     1 &#47;* Deferred AOF fsync. *&#47;
#define BIO_LAZY_FREE     2 &#47;* Deferred objects freeing. *&#47;

在 Redis 服务器启动时，会创建以上三类后台线程，然后阻塞等待任务的到来。处理关闭文件和 AOF 异步刷盘异步任务比较好理解，lazyfree 类型的异步任务场景就比较多了，比如下面几种情况：
1）删除数据：配置 lazyfree_lazy_user_del ，使用 unlink , 都可能将删除封装成任务放到 bio_jobs 任务队列中
2) 定期删除时，如果配置 lazyfree_lazy_expire ，那么可能将删除封装成任务放到 bio_jobs 任务队列中

2 后台创建的以上三种 bio 后台线程会不断轮询 bio_jobs 任务队列中的任务，并分门别类的处理对应的任务。逻辑操作定义在 bio.c 文件中

3 在 Redis 6.0 中增加了 io 多线程，在 networking.c 中定义了 io 线程的任务队列，以及创建 io_threads_num 个 io 线程，这些 io 线程会不断轮询 IO 读写任务。</div>2021-07-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/e2/97/dfadcc92.jpg" width="30px"><span>Kang</span> 👍（3） 💬（1）<div>请问下老师，各个源码目录的作用是从那里获取到的，mysql的话也会有相应解释吗</div>2021-07-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/17/bc/6d/f6f0a442.jpg" width="30px"><span>汤小高</span> 👍（1） 💬（0）<div>老师，能不能提供完整调试的搭建环境方案呀，看源码应该需要调试的</div>2022-06-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/44/cf/a0315a85.jpg" width="30px"><span>lzh2nix</span> 👍（1） 💬（0）<div>另外你还需要知道的是，Redis 的主从集群在进行恢复时，主要是依赖于哨兵机制，而这部分功能则直接实现在了 sentinel.c 文件中。

老师这里的描述是不是有问题，redis的高可用有两种方式sentinel模式和cluster模式，这里在cluster模式下的主从复制不依赖哨兵机制吧？</div>2021-08-01</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/CV9kk5M26pdIuAxwdXvj90ewKECzdSmzO4ibP6iaLXY50hICibefmib4qGvu1wCSfXuRobFC86z7W3OcfncpV8Uevw/132" width="30px"><span>Geek_25565b</span> 👍（0） 💬（1）<div>用什么工具看源码？</div>2022-05-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/2a/03/08/eacfce6a.jpg" width="30px"><span>z</span> 👍（0） 💬（0）<div>bioCreateBackgroundJob 这个就是异步执行逻辑吗？</div>2021-08-31</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/e0/4a/c0a3cb3f.jpg" width="30px"><span>肖鹏</span> 👍（0） 💬（1）<div>希望了解一下redis 外部数据结构到内部数据结构中间是怎么转换的</div>2021-08-06</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/9b/69/b844df30.jpg" width="30px"><span>结冰的水滴</span> 👍（0） 💬（3）<div>看redis源码，有好用的IDE么，老师能给推荐一个么</div>2021-08-04</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/44/cf/a0315a85.jpg" width="30px"><span>lzh2nix</span> 👍（0） 💬（0）<div>redis模块化做的特别好，如果想看一个模块我都先看下对应模块.h文件， 在.h中可以看到外提供里那些能力，再去看具体的实现。最后回答以下每日一问里的问题，后台异步相关的的都是再bio.h&#47;bio.c中，我们可以看下bio.h中提供了个那些能力。

void bioInit(void);
void bioCreateBackgroundJob(int type, void *arg1, void *arg2, void *arg3);
unsigned long long bioPendingJobsOfType(int type);
unsigned long long bioWaitStepOfType(int type);
time_t bioOlderJobOfType(int type);
void bioKillThreads(void);

&#47;* Background job opcodes *&#47;
#define BIO_CLOSE_FILE    0 &#47;* Deferred close(2) syscall. *&#47;
#define BIO_AOF_FSYNC     1 &#47;* Deferred AOF fsync. *&#47;
#define BIO_LAZY_FREE     2 &#47;* Deferred objects freeing. *&#47;
#define BIO_NUM_OPS       3

在种类定义对外的API(管理BIO相关的任务)， 已经有三种backgroup jop，然后再去看这个三种job的具体实现。在bio.c中我们可以看到pthread的经典用法。</div>2021-08-01</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/44/cf/a0315a85.jpg" width="30px"><span>lzh2nix</span> 👍（0） 💬（1）<div>&quot;包括 glibc 库提供的默认分配器 tcmalloc&quot;

老师这里描述是不是有问题， glibc使用的是ptmalloc(参考 https:&#47;&#47;www.gnu.org&#47;software&#47;libc&#47;manual&#47;html_node&#47;The-GNU-Allocator.html)，tcmalloc是google搞出来的，golang默认采用的是tcmalloc。</div>2021-07-31</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1c/4e/88/791d0f5e.jpg" width="30px"><span>lei</span> 👍（0） 💬（0）<div>等我复习下c语言，马上回来！</div>2021-07-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/25/7f/473d5a77.jpg" width="30px"><span>曾轼麟</span> 👍（0） 💬（0）<div>以unlink为例子，其实是有几个步骤的：
    1、首先在redis启动的时候会调用bioInit初始化异步执行的线程，等待注册任务执行（截至到6.x版本目前只初始化三个线程，对应三种异步类型，每个线程只处理指定类型的任务，概念上和线程池不一样）
    2、当执行unlink的时候，先删除key在字典上的指针，如果不需要异步直接使用dictFreeUnlinkedEntry释放内存，如果需要直接跳过释放步骤
    3、通过lazyfreeGetFreeEffort函数计算删除key的代价，如果代价超过阈值则注册一个bioCreateLazyFreeJob 并标记类型为BIO_LAZY_FREE等待异步执行
    4、异步线程执行job释放内存



实际代码流程如下所示：
    1、unlink主流程（允许异步）：unlinkCommand -&gt; delGenericCommand -&gt; dbAsyncDelete -&gt; dictUnlink -&gt; 注册bioCreateBackgroundJob
    2、unlink主流程（不用异步）：unlinkCommand -&gt; delGenericCommand -&gt; dbAsyncDelete -&gt; dictUnlink -&gt; dictFreeUnlinkedEntry(直接释放内存)

对应的代码在lazyfree.c和bio.c文件中，此外异步执行一共支持三种类型 BIO_CLOSE_FILE（异步关闭文件）BIO_AOF_FSYNC（AOF异步同步） BIO_LAZY_FREE（懒删除）</div>2021-07-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/88/d7/07f8bc6c.jpg" width="30px"><span>sljoai</span> 👍（0） 💬（4）<div>没什么C语言开发经验，请问一下大家都是采用哪种开发工具来查看及调试Redis源码的?</div>2021-07-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/57/6e/b6795c44.jpg" width="30px"><span>夜空中最亮的星</span> 👍（0） 💬（0）<div>一讲这么长，必须买</div>2021-07-26</li><br/>
</ul>