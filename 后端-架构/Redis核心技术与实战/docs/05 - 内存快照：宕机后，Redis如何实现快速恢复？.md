你好，我是蒋德钧。

上节课，我们学习了Redis避免数据丢失的AOF方法。这个方法的好处，是每次执行只需要记录操作命令，需要持久化的数据量不大。一般而言，只要你采用的不是always的持久化策略，就不会对性能造成太大影响。

但是，也正因为记录的是操作命令，而不是实际的数据，所以，用AOF方法进行故障恢复的时候，需要逐一把操作日志都执行一遍。如果操作日志非常多，Redis就会恢复得很缓慢，影响到正常使用。这当然不是理想的结果。那么，还有没有既可以保证可靠性，还能在宕机时实现快速恢复的其他方法呢？

当然有了，这就是我们今天要一起学习的另一种持久化方法：**内存快照**。所谓内存快照，就是指内存中的数据在某一个时刻的状态记录。这就类似于照片，当你给朋友拍照时，一张照片就能把朋友一瞬间的形象完全记下来。

对Redis来说，它实现类似照片记录效果的方式，就是把某一时刻的状态以文件的形式写到磁盘上，也就是快照。这样一来，即使宕机，快照文件也不会丢失，数据的可靠性也就得到了保证。这个快照文件就称为RDB文件，其中，RDB就是Redis DataBase的缩写。

和AOF相比，RDB记录的是某一时刻的数据，并不是操作，所以，在做数据恢复时，我们可以直接把RDB文件读入内存，很快地完成恢复。听起来好像很不错，但内存快照也并不是最优选项。为什么这么说呢？
<div><strong>精选留言（30）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/0f/a4/2b/3ba9f64b.jpg" width="30px"><span>Devin</span> 👍（130） 💬（8）<div>老师全文中都是使用的“主线程”而不是“主进程”，评论中大家有的用的是“主线程”有的是“主进程”。请问下老师为啥不是用的“主进程”？</div>2020-08-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/90/8a/288f9f94.jpg" width="30px"><span>Kaito</span> 👍（1065） 💬（119）<div>2核CPU、4GB内存、500G磁盘，Redis实例占用2GB，写读比例为8:2，此时做RDB持久化，产生的风险主要在于 CPU资源 和 内存资源 这2方面：

	a、内存资源风险：Redis fork子进程做RDB持久化，由于写的比例为80%，那么在持久化过程中，“写实复制”会重新分配整个实例80%的内存副本，大约需要重新分配1.6GB内存空间，这样整个系统的内存使用接近饱和，如果此时父进程又有大量新key写入，很快机器内存就会被吃光，如果机器开启了Swap机制，那么Redis会有一部分数据被换到磁盘上，当Redis访问这部分在磁盘上的数据时，性能会急剧下降，已经达不到高性能的标准（可以理解为武功被废）。如果机器没有开启Swap，会直接触发OOM，父子进程会面临被系统kill掉的风险。

	b、CPU资源风险：虽然子进程在做RDB持久化，但生成RDB快照过程会消耗大量的CPU资源，虽然Redis处理处理请求是单线程的，但Redis Server还有其他线程在后台工作，例如AOF每秒刷盘、异步关闭文件描述符这些操作。由于机器只有2核CPU，这也就意味着父进程占用了超过一半的CPU资源，此时子进程做RDB持久化，可能会产生CPU竞争，导致的结果就是父进程处理请求延迟增大，子进程生成RDB快照的时间也会变长，整个Redis Server性能下降。

	c、另外，可以再延伸一下，老师的问题没有提到Redis进程是否绑定了CPU，如果绑定了CPU，那么子进程会继承父进程的CPU亲和性属性，子进程必然会与父进程争夺同一个CPU资源，整个Redis Server的性能必然会受到影响！所以如果Redis需要开启定时RDB和AOF重写，进程一定不要绑定CPU。</div>2020-08-14</li><br/><li><img src="" width="30px"><span>Geek_Lin</span> 👍（91） 💬（14）<div>文章中写时复制那里，复制的是主线程修改之前的数据还是主线程修改之后的呢？</div>2020-08-16</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1d/12/13/e103a6e3.jpg" width="30px"><span>扩散性百万咸面包</span> 👍（41） 💬（5）<div>感觉老师这里是不是说的有点问题？
１．fork()本身应该是比较快的吧？因为COW的存在，只需要部分数据（局部变量）的复制。真正阻塞的是bgsave在持久化过程中写RDB的时候，因为同时要服务写请求，所以主线程要复制对应内存。
２．这个复制为什么不能让fork()出来的子线程去做呢？这样不就不阻塞主线程了吗？
</div>2020-08-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/dd/9b/0bc44a78.jpg" width="30px"><span>yyl</span> 👍（24） 💬（2）<div>解答：
系统的QPS未知，两种情况吧：
1. QPS较低，不会有什么问题
2. QPS较高，首先由于写多读少，造成更多的写时拷贝，导致更多的内存占用。如果采用增量快照，需要增加额外的内存开销；再则，写RDB文件，OS会分配一些Cache用于磁盘写，进一步加剧内存资源的消耗。
由于频繁的写RDB文件，造成较大的磁盘IO开销，消耗CPU</div>2020-08-15</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/DYAIOgq83eppZl39m2knwLH6PIia5YQTOWSOTGhy8ZZAutUIrxKOYFCtLLLYb1OZvIVVLzL7Y8eglKFe4Sib9D7g/132" width="30px"><span>漫步oo0云端</span> 👍（18） 💬（19）<div>我想提一个傻问题，我作为初学者想问，如果redis服务挂了，备份有什么用？能恢复的前提不是服务还存活吗？难道服务挂了会自动拉起服务？自动还原吗？</div>2020-08-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/7a/0a/0ce5c232.jpg" width="30px"><span>吕</span> 👍（9） 💬（1）<div>老师，请教一下，bgsave命令只能是手动执行么？没配置中只看到了save,没有bgsave的配置</div>2020-08-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/24/d7/146f484b.jpg" width="30px"><span>小宇子2B</span> 👍（8） 💬（4）<div>做RDB期间是写时复制的 2GB的数据 80%都是写请求 也就是大概要复制出来1.6GB数据，加上本身数据2GB ，已经达到3.6GB，去掉操作系统本身的内存占用 机器所剩内存已经不多了 容易发生OOM</div>2020-08-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/18/8e/49/10ef002d.jpg" width="30px"><span>周翔在山麓（Xiang Zhou）</span> 👍（7） 💬（5）<div>这一讲真的很好, aof 相当于数据库的 binlog, rdb 相当于redo log. 知识互相映射, 加强了学习. 我又看了一遍mysql 的数据恢复机制. 同学们还记得吗?</div>2021-01-01</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTKiauonyMORA2s43W7mogGDH4WYjW0gBJtYmUa9icTB6aMPGqibicEKlLoQmLKLWEctwHzthbTZkKR20w/132" width="30px"><span>Spring4J</span> 👍（2） 💬（2）<div>由于修改操作占大部分比例，为了尽可能保证宕机时数据的完整性，快照的间隔就不能太长，而间隔太短又会带来很多的性能开销，所以对于这种特点的数据，不适合使用RDB的持久化方式</div>2020-08-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/ce/d7/5315f6ce.jpg" width="30px"><span>不负青春不负己🤘</span> 👍（0） 💬（1）<div>打卡 第二遍 </div>2020-08-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/19/7c/66/73eabdd2.jpg" width="30px"><span>无名十三</span> 👍（0） 💬（1）<div>简单来说，bgsave 子进程是由主线程 fork 生成的，可以共享主线程的所有内存数据。bgsave 子进程运行后，开始读取主线程的内存数据，并把它们写入 RDB 文件。


老师，这里是主线程还是主进程？</div>2020-08-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/fd/fd/326be9bb.jpg" width="30px"><span>注定非凡</span> 👍（117） 💬（6）<div>1，作者讲了什么？
作者在本章讲了redis两种持久化方式中的RDB方式
2，作者是怎么把这事给讲明白的？
为了让大家明白RDB的快照的概念，作者举了拍照片，照合影的例子
3，为了讲明白，作者讲了哪些要点，有哪些亮点？
（1）亮点1：作者解释快照使用了拍合影的例子，让我很好的理解快照的概念，以及内存数据大小对快照产生的影响
（2）要点1：RDB快照，将此时内存中的所有的数据写入磁盘
（3）要点2：生成快照有两种方式：sava和bgsava，save是主进程执行，生成时会阻塞redis，只能执行查找。bgsave是由主进程fork出子进程执行，
（4）要点3：子进程在被fork处理时，与主进程共享同一份内存，但在生成快照时采取COW机制，确保不会阻塞主进程的数据读写
（5）要点4：RDB的执行频率很重要，这会影响到数据的完整性和Redis的性能稳定性。所以4.0后有了aof和rdb混合的数据持久化机制
4，对于作者所讲，我有哪些发散性思考？
作者开篇提到的两个问题：快照什么数据，快照有何影响，具体的场景，才能讨论出具体的技术方案，我个人认为，脱离场景谈方案是在自嗨

5，将来有哪些场景，我能够使用到它？
我们项目的redis持久化使用的方式就是aof和rdb混合，前一段时间，做过集群升级扩容。把每台8c,30G内存,5主5从，升级改造成为8c,15G内存,15主15从。这样搞主要是因为之前的集群内存占用太高，导致数据持久化失败
6，读者评论的收获：
定这个专栏，真是觉得捡到宝了，大神@Kaito写的评论实在漂亮，每次都要读好几遍，读完都有赏心悦目的愉悦感，期望自己有一天也可像他那样出色
</div>2020-08-15</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/26/38/ef063dc2.jpg" width="30px"><span>Darren</span> 👍（51） 💬（18）<div>Kaito的回答为啥老让我觉得自己那么菜呢������

我稍微补充下老师对于 ”混合使用 AOF 日志和内存快照“这块的东西：
在redis4.0以前，redis AOF的重写机制是指令整合（老师上一节课已经说过），但是在redis4.0以后，redis的 AOF 重写的时候就直接把 RDB 的内容写到 AOF 文件开头，将增量的以指令的方式Append到AOF，这样做的好处是可以结合 RDB 和 AOF 的优点, 快速加载同时避免丢失过多的数据。当然缺点也是有的， AOF 里面的 RDB 部分就是压缩格式不再是 AOF 格式，可读性较差。Redis服务在读取AOF文件的怎么判断是否AOF文件中是否包含RDB，它会查看是否以 REDIS 开头；人为的看的话，也可以看到以REDIS开头，RDB的文件也打开也是乱码。

可以通过aof-use-rdb-preamble 配置去设置改功能。

# When rewriting the AOF file, Redis is able to use an RDB preamble in the
# AOF file for faster rewrites and recoveries. When this option is turned
# on the rewritten AOF file is composed of two different stanzas:
#
#   [RDB file][AOF tail]
#
# When loading Redis recognizes that the AOF file starts with the &quot;REDIS&quot;
# string and loads the prefixed RDB file, and continues loading the AOF
# tail.
aof-use-rdb-preamble yes
</div>2020-08-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/25/7f/473d5a77.jpg" width="30px"><span>曾轼麟</span> 👍（19） 💬（7）<div> 【内存风险】：2 核 CPU、4GB 内存、500GB 磁盘， 2GB数据，在操作系统虚拟内存的支持下，fork出一个子进程会贡献主进程的虚拟内存映射的物理空间，这个是MMU实现的不属于Redis的产物，但是当发生数据修改的时候，MMU会将子进程的物理内存复制独立出来（写时拷贝技术）。在 8:2的独写比例中实际需要的物理内存可能会达到 1.6 +1.6 = 3.2 。假设开启swap的情况下，在物理内存不能满足程序运行的时候，虚拟内存技术会将内存中的数据保存在磁盘上，这样会导致Redis性能下降。

对于绑核问题，我认同Kaito同学的说法。不过我认为的问题是因为云主机的原因：一般大型服务器是使用QPI总线，NMUA架构。NUMA中，虽然内存直接绑定在CPU上，但是由于内存被平均分配在了各个组上。只有当CPU访问自身直接绑定的内存对应的物理地址时，才会有较短的响应时间。而如果需要访问其他CPU 绑定的内存的数据时，就需要通过特殊的通道访问，响应时间就相比之前变慢了（甚至有些服务器宁愿使用swap也不走特殊通道），假如当前云主机比较繁忙的情况下，这样就会导致性能下降。（大部分互联网公司都使用了服务器虚拟化技术）</div>2020-08-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/54/9a/76c0af70.jpg" width="30px"><span>每天晒白牙</span> 👍（10） 💬（1）<div>Redis持久化
AOF
AOF是一种通过记录操作命令的的方式来达到持久化的目的，正是因为记录操作命令而不是数据，所以在恢复数据的时候需要 redo 这些操作命令(当然 AOF 也有重写机制从而使命令减少)，如果操作日志太多，恢复过程就会很慢，可能会影响 Redis 的正常使用

RDB
RDB 是一种内存快照，把内存的数据在某一时刻的状态记录下来，所以通过 RDB 恢复数据只需要把 RDB 文件读入内存就可以恢复数据(具体实现细节还没去了解)

但这里有两个需要注意的问题
1.对哪些数据做快照，关系到快照的执行顺序
2.做快照时，还能对数据做增删改吗？这会关系到 Redis 是否阻塞，因为如果在做快照时，还能对数据做修改，说明 Redis 还能处理写请求，如果不能对数据做修改，就不能处理写请求，要等执行完快照才能处理写请求，这样会影响性能

来看第一个问题
RDB 是对全量数据需要快照，全量数据会使 RDB 文件大，发文件写到磁盘就会耗时，因为 Redis 是单线程，会不会阻塞主线程？(这一点始终都要考虑的点)
Redis 实现 RDB 的方式有两种
①save:在主线程中执行，会导致阻塞
②bgsave:创建子线程来执行，不会阻塞，这是默认的
所以可以使用 bgsave 来对全量内存做快照，不影响主进程

来看第二个问题
在做快照时，我们是不希望数据被修改的，但是如果在做快照过程中，Redis 不能处理写操作，这对业务是会造成影响的，但上面刚说完 bgsave 进行快照是非阻塞的呀，这是一个常见的误区：避免阻塞和正常的处理写操作不是一回事。用 bgsave 时，主线程是没有被阻塞，可以正常处理请求，但为了保证快照的完整性，只能处理读请求，因为不能修改正在执行快照的数据。显然为了快照而暂停写是不能被接受的。Redis 采用操作系统提供的写时复制技术（Copy-On-Write 即 COW），在执行快照的同时，可以正常的处理写操作
bgsave 子线程是由主线程 fork 生成，可以共享主线程的所有内存数据，所以 bgsave 子线程是读取主线程的内存数据并把他们写入 RDB 文件的
如果主线程对这些数据只执行读操作，两个线程是互不影响的。如果主线程要执行写造作，那么这个数据就会被复制一份，生成一个副本，然后 bgsave 子线程会把这个副本数据写入 RDB 文件，这样主线程就可以修改原来的数据了。这样既保证了快照的完整性，也保证了正常的业务进行

那如何更好的使用 RDB 呢？
RDB 的频率不好把握，如果频率太低，两次快照间一旦有宕机，就可能会丢失很多数据。如果频率太高，又会产生额外开销，主要体现在两个方面
①频繁将全量数据写入磁盘，会给磁盘带来压力，多个快照竞争有效的磁盘带宽
②bgsave 子线程是通过 fork 主线程得来，前面也说了，bgsave 子线程是不会阻塞主线程的，但 fork 这个创建过程是会阻塞主线程的，而且主线程内存越大，阻塞时间越长

最好的方法是全量快照+增量快照，即进行一次 RDB 后，后面的增量修改用 AOF 记录两次全量快照之间的写操作，这样可以避免频繁 fork 对主线程的影响。同时避免 AOF 文件过大，重写的开销</div>2020-08-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1d/12/13/e103a6e3.jpg" width="30px"><span>扩散性百万咸面包</span> 👍（10） 💬（7）<div>很奇怪，对于RDB和AOF混合搭配的策略，为什么不把AOF应用于RDB生成增量快照呢？而非要再次生成全量快照？</div>2020-08-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/43/79/18073134.jpg" width="30px"><span>test</span> 👍（9） 💬（0）<div>1.写太多，COW需要复制的东西太多，内存占用问题；
2.CPU太少，redis后台还有很多线程在后台工作，会产生CPU竞争。</div>2020-08-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/20/21/aa/66d71e6b.jpg" width="30px"><span>benzhang</span> 👍（4） 💬（1）<div>你好，关于这一点我有点疑问
“另一方面，bgsave 子进程需要通过 fork 操作从主线程创建出来。虽然，子进程在创建后不会再阻塞主线程，但是，fork 这个创建过程本身会阻塞主线程，而且主线程的内存越大，阻塞时间越长。如果频繁 fork 出 bgsave 子进程，这就会频繁阻塞主线程了。那么，有什么其他好方法吗？”
我一直以为bgsave这个子进程只需要创建一次而已。从上面这段话的意思看，也就是说每写一次快照就需要fork一个bgsave子进程吗？如果是的话，哪如何解决写入冲突呢？</div>2020-09-07</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTJnugUNWBtcszhJg3Q0hqEMSHftKco2TqCG78blZ3ibjncjZ64NbibGia5l4NB0DUibIq0BCZ03JvkoNA/132" width="30px"><span>Geek__e15575f5b6ec</span> 👍（3） 💬（0）<div>最近遇到个问题，docker安装的redis，运行一段时间之后，日志显示会出现几十次的DB saved on disk
时间间隔几百毫秒到几秒之间 然后会出现redis部分数据丢失  完全不知道怎么排查 有没有大佬能够解惑</div>2021-04-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/3b/6a/80d9c545.jpg" width="30px"><span>RD</span> 👍（2） 💬（0）<div>我感觉混合模式那里说的有问题。AOF 日志和 RDB 日志就是两个东西。重启恢复逻辑应该是这样的，如果 AOF 没开，RDB 开着，则走 RDB 恢复。如果 AOF 开着，则只会走 AOF ，因为 AOF 本身的定义就是全量数据，所以只要 AOF 开启，不管是否混用，都只需要 AOF 文件就能完全恢复数据。这里的混用不是指，混用两种日志逻辑去恢复数据，而是综合两种日志的优势给 AOF 增强。AOF 的缺点是，记录的命令行而不是数据本身，所以在恢复的时候只能挨条重放，redis 又是单线程，所以很慢。RDB 的缺点是，每隔很短的时间就做快照，会频繁做 fork 操作，并且频繁地进行写时复制耗费内存。所以，所谓的混合模式，还是单独使用 AOF 日志模式，用重写机制不频繁的优点代替 RDB 频繁快照的缺点，用 RDB 记录数据二进制格式的优点，弥补 AOF 记录命令重放的缺点。所以，最终逻辑应该是，在服务启动时，做快照生成二进制内容写到 AOF 文件，然后正常增量写，等到了重写的时候，再重新生成二进制内容写到新的 AOF 文件，然后继续增量写。从头到尾都是 AOF 的逻辑，唯一的就是重写的时候，结合 RDB 的优点，写入的是二进制格式日志。</div>2022-09-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/2c/53/12/ed39ec11.jpg" width="30px"><span>go big</span> 👍（1） 💬（0）<div>哈哈</div>2022-04-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/2b/54/a8/3b334406.jpg" width="30px"><span>冷山</span> 👍（1） 💬（1）<div>哎呀，总结一下：
不管是RDB还是AOF。他们都需要fork出一个子进程进行日志的操作。
而两者使用子进程来操作日志时、都存在两个阻塞点：
1. fork的过程中、如果实例数据比较多，主线程的页表就比较大、复制主线程的页表给子进程这个操作就比较耗时（这里可以理解为主线程把自己的内存空间中的数据遗传给子进程使用），会阻塞主线程。

2. RDB在生成日志和AOF在重写时，为了支持主线程同时可以对原有数据进行写操作：两者都借助了操作系统的：写时复制机制。 写时复制机制就是主线程在修改原有数据时，它会动用遗传给子进程的数据，而是拷贝一份数据副本（以页为单位拷贝），然后对这个副本进行操作。  假设主线程在子进程使用的原有数据A上做修改，如果此时数据A还没有被AOF重写或者被生成RDB快照，那么就会导致子进程重写&#47;生成RDB快照的过程失败，或者说是脏数据嘛。</div>2021-12-30</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/18/41/13/bf8e85cc.jpg" width="30px"><span>树心</span> 👍（1） 💬（0）<div>bgsave是子进程，为什么能共享主线程（主进程）的数据，不是子线程才能共享父进程的数据吗？子进程fork的时候是要复制一份的</div>2021-12-06</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/33/14/78104f1f.jpg" width="30px"><span>Just Do IT</span> 👍（1） 💬（2）<div>感觉老师说的Redis4.0AOF和RDB混用那个地方有点问题？

Redis恢复数据是以AOF优先的，如果采用AOF只记录中间的数据，那么恢复的时候肯定是数据缺失的。</div>2021-07-01</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/33/14/78104f1f.jpg" width="30px"><span>Just Do IT</span> 👍（1） 💬（3）<div>我认为这句话是有问题的，不是使用了混合持久化就不丢失数据了   如果在全量快照的过程中宕机，丢失的数据反而比只使用AOF的策略更多，它丢失的是整个内存的数据，如果在生成全量快照之后宕机，那么它丢失数据的情况和AOF相同。



“数据不能丢失时，内存快照和 AOF 的混合使用是一个很好的选择；”</div>2021-02-26</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/PiajxSqBRaELZPnUAiajaR5C25EDLWeJURggyiaOP5GGPe2qlwpQcm5e3ybib8OsP4tvddFDLVRSNNGL5I3SFPJHsA/132" width="30px"><span>null</span> 👍（1） 💬（0）<div>「混合使用 AOF 日志和内存快照」
这节课的aof文件，和上一节课的aof 文件，不是同一份吧？因为重新执行快照，这节课的aof 文件会被清空。
比如我开启了aof 和rdb 两种持久化策略，在更新数据时，要写两份aof 文件是么？
那我能关闭上节课的aof 持久化策略，只启用本节课的混合aof 和rdb 策略，是不是也能做到数据的不丢失？（丢失多少数据，则由混合的aof 文件刷盘间隔决定）
谢谢老师！</div>2021-01-15</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/4f/7d/dd852b04.jpg" width="30px"><span>chon</span> 👍（1） 💬（3）<div>写读比这么高有必要用redis吗？</div>2020-12-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/38/fe/04f56d1e.jpg" width="30px"><span>learn more</span> 👍（1） 💬（0）<div>因为redis是单线程的，所以双核够用，一个执行命令，一个用来bgsave，不会阻塞主线程；内存4g，实际占用2g左右，因此内存是一个临界点，比如 fork 子进城的时候很有可能耗尽所有的内存，加上读写比例是写多读少，那么根据 save 的配置很有可能出现频繁的 bgsave，此时内存将成为瓶颈；磁盘空间足够，所以不会影响。
不知道有没有分析正确😂</div>2020-08-14</li><br/><li><img src="" width="30px"><span>Geek_fe58be</span> 👍（0） 💬（0）<div>这块数据就会被复制一份，生成该数据的副本（键值对 C’

老师，这个副本是怎么处理的？没有看到</div>2024-06-13</li><br/>
</ul>