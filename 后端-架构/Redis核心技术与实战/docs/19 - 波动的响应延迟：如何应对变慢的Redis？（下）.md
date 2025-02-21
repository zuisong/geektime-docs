你好，我是蒋德钧。

上节课，我介绍了判断Redis变慢的两种方法，分别是响应延迟和基线性能。除此之外，我还给你分享了从Redis的自身命令操作层面排查和解决问题的两种方案。

但是，如果在排查时，你发现Redis没有执行大量的慢查询命令，也没有同时删除大量过期keys，那么，我们是不是就束手无策了呢？

当然不是！我还有很多“锦囊妙计”，准备在这节课分享给你呢！

如果上节课的方法不管用，那就说明，你要关注影响性能的其他机制了，也就是文件系统和操作系统。

Redis会持久化保存数据到磁盘，这个过程要依赖文件系统来完成，所以，文件系统将数据写回磁盘的机制，会直接影响到Redis持久化的效率。而且，在持久化的过程中，Redis也还在接收其他请求，持久化的效率高低又会影响到Redis处理请求的性能。

另一方面，Redis是内存数据库，内存操作非常频繁，所以，操作系统的内存机制会直接影响到Redis的处理效率。比如说，如果Redis的内存不够用了，操作系统会启动swap机制，这就会直接拖慢Redis。

那么，接下来，我再从这两个层面，继续给你介绍，如何进一步解决Redis变慢的问题。

![](https://static001.geekbang.org/resource/image/cd/06/cd026801924e197f5c79828c368cd706.jpg?wh=4242%2A3039)

## 文件系统：AOF模式

你可能会问，Redis是个内存数据库，为什么它的性能还和文件系统有关呢？
<div><strong>精选留言（30）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/0f/90/8a/288f9f94.jpg" width="30px"><span>Kaito</span> 👍（525） 💬（37）<div>关于如何分析、排查、解决Redis变慢问题，我总结的checklist如下：

1、使用复杂度过高的命令（例如SORT&#47;SUION&#47;ZUNIONSTORE&#47;KEYS），或一次查询全量数据（例如LRANGE key 0 N，但N很大）

分析：a) 查看slowlog是否存在这些命令 b) Redis进程CPU使用率是否飙升（聚合运算命令导致）

解决：a) 不使用复杂度过高的命令，或用其他方式代替实现（放在客户端做） b) 数据尽量分批查询（LRANGE key 0 N，建议N&lt;=100，查询全量数据建议使用HSCAN&#47;SSCAN&#47;ZSCAN）

2、操作bigkey

分析：a) slowlog出现很多SET&#47;DELETE变慢命令（bigkey分配内存和释放内存变慢） b) 使用redis-cli -h $host -p $port --bigkeys扫描出很多bigkey

解决：a) 优化业务，避免存储bigkey b) Redis 4.0+可开启lazy-free机制

3、大量key集中过期

分析：a) 业务使用EXPIREAT&#47;PEXPIREAT命令 b) Redis info中的expired_keys指标短期突增

解决：a) 优化业务，过期增加随机时间，把时间打散，减轻删除过期key的压力 b) 运维层面，监控expired_keys指标，有短期突增及时报警排查

4、Redis内存达到maxmemory

分析：a) 实例内存达到maxmemory，且写入量大，淘汰key压力变大 b) Redis info中的evicted_keys指标短期突增

解决：a) 业务层面，根据情况调整淘汰策略（随机比LRU快） b) 运维层面，监控evicted_keys指标，有短期突增及时报警 c) 集群扩容，多个实例减轻淘汰key的压力

5、大量短连接请求

分析：Redis处理大量短连接请求，TCP三次握手和四次挥手也会增加耗时

解决：使用长连接操作Redis

6、生成RDB和AOF重写fork耗时严重

分析：a) Redis变慢只发生在生成RDB和AOF重写期间 b) 实例占用内存越大，fork拷贝内存页表越久 c) Redis info中latest_fork_usec耗时变长

解决：a) 实例尽量小 b) Redis尽量部署在物理机上 c) 优化备份策略（例如低峰期备份） d) 合理配置repl-backlog和slave client-output-buffer-limit，避免主从全量同步 e) 视情况考虑关闭AOF f) 监控latest_fork_usec耗时是否变长

7、AOF使用awalys机制

分析：磁盘IO负载变高

解决：a) 使用everysec机制 b) 丢失数据不敏感的业务不开启AOF

8、使用Swap

分析：a) 所有请求全部开始变慢 b) slowlog大量慢日志 c) 查看Redis进程是否使用到了Swap

解决：a) 增加机器内存 b) 集群扩容 c) Swap使用时监控报警

9、进程绑定CPU不合理

分析：a) Redis进程只绑定一个CPU逻辑核 b) NUMA架构下，网络中断处理程序和Redis进程没有绑定在同一个Socket下

解决：a) Redis进程绑定多个CPU逻辑核 b) 网络中断处理程序和Redis进程绑定在同一个Socket下

10、开启透明大页机制

分析：生成RDB和AOF重写期间，主线程处理写请求耗时变长（拷贝内存副本耗时变长）

解决：关闭透明大页机制

11、网卡负载过高

分析：a) TCP&#47;IP层延迟变大，丢包重传变多 b) 是否存在流量过大的实例占满带宽

解决：a) 机器网络资源监控，负载过高及时报警 b) 提前规划部署策略，访问量大的实例隔离部署

总之，Redis的性能与CPU、内存、网络、磁盘都息息相关，任何一处发生问题，都会影响到Redis的性能。

主要涉及到的包括业务使用层面和运维层面：业务人员需要了解Redis基本的运行原理，使用合理的命令、规避bigke问题和集中过期问题。运维层面需要DBA提前规划好部署策略，预留足够的资源，同时做好监控，这样当发生问题时，能够及时发现并尽快处理。</div>2020-09-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/c9/5e/b79e6d5d.jpg" width="30px"><span>꧁子华宝宝萌萌哒꧂</span> 👍（22） 💬（3）<div>
echo never &#47;sys&#47;kernel&#47;mm&#47;transparent_hugepage&#47;enabled 
这个是不是得改成
echo never &gt; &#47;sys&#47;kernel&#47;mm&#47;transparent_hugepage&#47;enabled
这样？</div>2020-09-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1c/fb/ab/c0c29cda.jpg" width="30px"><span>王世艺</span> 👍（19） 💬（5）<div>看了下，貌似是这样
redis 有一个aof_buf缓存,用来缓存新的aof操作信息。
正常情况下主线程每次循环都是先将aof_buff write，然后aof_buf是清空，
主线程会用去fsync，已经write的内容。
刷盘当时aways的情况下，主线程去直接调用redis_fsync。
但是当策略是EVERYSEC时，主线程会用aof_background_fsync中的bioCreateBackgroundJob(BIO_AOF_FSYNC,(void*)(long)fd,NULL,NULL);创建子线程去完成。

但是当io压力大的时候，也就是aof_buf有积压是。主线程在EVERYSEC模式下回去判断。是否有aofwrite在执行，并超过2s
如果超过2s主线程不会return，继续将aof_buf write
代码：nwritten = aofWrite(server.aof_fd,server.aof_buf,sdslen(server.aof_buf));
但是因为子线程在aof_fd上fsync，所以write aof_fd的请求会被堵塞,这里write全是主线程在操作，堵塞直到fsync完成，能改变文件描述符（aof_fd）,主线程才可以继续响应请求</div>2020-09-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/92/d5/699384a0.jpg" width="30px"><span>yeek</span> 👍（10） 💬（4）<div>如果redis是独立部署，那么当内存不足时，淘汰策略和操作系统的swap机制 哪个会优先执行？

曾遇到过线上触发内存淘汰的场景，并未观察当时的swap情况，感谢老师的建议</div>2020-09-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/5c/8f/551b5624.jpg" width="30px"><span>小可</span> 👍（9） 💬（0）<div>redis变慢问题优化自我总结：
1.cpu：redis实例绑定同一个cpu物理核；网络中断和redis实例绑定同一个cpu socket
2.内存：关闭大内存页，观察swap，增加物理内存
3.磁盘：数据丢失容忍度aof策略选择；AOF使用SDD
4.操作：集合操作，bigkey删除，返回集合改为SCAN多次操作
5.过期：过期时间加随机数
6.监控：基线性能--intrinsic-latency; monitor; ;latency</div>2021-02-04</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/1e/8c/d9330d2b.jpg" width="30px"><span>花儿少年</span> 👍（8） 💬（1）<div>之前出现过redis变慢的问题，导致系统整体变慢，系统大概几小时内30%的请求都很慢，基本到不可用的情况了。
具体情况是某同学(我)在新业务的时候添加了一个新的key，由于符合hash的特性于是直接使用了redission 的map，上线后由于逻辑问题并没有执行到，但是由于仅仅是缓存嘛，业务也没问题，后来由于另外的项目中覆盖到这个case发现有问题，然后就把逻辑修复了。
上线后redis集群的proxy节点的一两个节点cpu使用率飙高，但是没想明白为啥，所以也没回滚，然后第二天中午流量变大了，就会有更多的proxy节点cpu使用率100%，这个时候业务就开始大量报警了，因为接口开始部分超时，然后紧急把那块缓存的代码删除发布上线，然后系统就恢复了。
过程讲完了，接下来说原因，先说下redis集群的架构，流量经过proxy节点分发给redis，业务仅感知到一个vip节点，那么这种情况下，proxy节点就需要对客户端的请求进行保序的操作，这也就是说先到的请求没返回时，后来的请求也不能返回；redisson的map实现是加入了lua脚本的，同时代码里对单个key设置了过期时间，导致整个脚本很复杂很消耗性能，那么redis本身就会变慢，但是不是很明显，同时加上proxy节点，返回到客户端就很慢了，同时加上proxy保序的特点，更加剧了耗时。redis是分片的，所以量小的时只有少部分节点受影响，但是量大时所有的分片上都有这种慢请求，拖慢了整体的性能。。
血泪教训，使用不熟悉的类库时，一定要多看看源码，对公司的产品的特性要熟悉，对隐患要及时止损，想着问题不大也没回滚，简直天真。
不过redisson真的好用。yyds</div>2021-07-31</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/1d/de/62bfa83f.jpg" width="30px"><span>aoe</span> 👍（4） 💬（0）<div>Redis 变慢？按（老师 + Kaito）一波操作下来不快也得快！</div>2021-04-02</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/92/d5/699384a0.jpg" width="30px"><span>yeek</span> 👍（4） 💬（5）<div>当主线程使用后台子线程执行了一次 fsync，需要再次把新接收的操作记录写回磁盘时，如果主线程发现上一次的 fsync 还没有执行完，那么它就会阻塞。所以，如果后台子线程执行的 fsync 频繁阻塞的话（比如 AOF 重写占用了大量的磁盘 IO 带宽），主线程也会阻塞，导致 Redis 性能变慢。


这段没懂，redis主线程和后台子线程之间有状态通信吗？主线程调用fsync对子线程而言是任务队列的方式还是同步调用的方式？ 我去看看源码吧……</div>2020-09-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/ed/eb/88cac7a5.jpg" width="30px"><span>东</span> 👍（3） 💬（1）<div>“8. 是否运行了 Redis 主从集群？如果是的话，把主库实例的数据量大小控制在 2~4GB，以免主从复制时，从库因加载大的 RDB 文件而阻塞。” 这个2~4G的经验值和主库的内存大小无关吗？比如主从库内存都是64G， 这个主库数据量依然是2~4G？</div>2020-09-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/56/e0/d34f57b3.jpg" width="30px"><span>日落黄昏下</span> 👍（2） 💬（0）<div>除了aof重写可能造成堵塞，在aof everysec时，如果发现此时正在进行fsync，并且超过2s时，会堵塞主线程等待。可监控aof-pending-bio-fsync和aof-delay-fsync信息，并且会有aof fsync is taking too long 的日志。</div>2021-10-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/2c/0f/95/275d534e.jpg" width="30px"><span>卡尔</span> 👍（1） 💬（0）<div>aof的everysec策略下，子线程会导致主线程阻塞我说下个人观点。
作者的意思是在 ererysec下，子线程每秒去fsync，但是主线程会监测该子线程的fsync的执行情况。有个策略就是，若是主线程发现已过2s（也就是上次没执行完）了，子线程的上一次的fsync还没有执行完成，主线程就会阻塞，直到子线程当前的fsync完成，才返回。
当然影响 子线程的fsync，导致其变慢的因素是磁盘io的效率较低，当然影响磁盘io效率的有很多，其中aof重写占据大量的磁盘io资源就是其中之一。</div>2022-07-04</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/19/d9/ff/b23018a6.jpg" width="30px"><span>Heaven</span> 👍（1） 💬（0）<div>对于Swap机制,关闭应该是最方便的解决方案,包括在Kubernetes集群中,对于部署的节点也是要求关闭swap的,关闭方式如下swapoff -a</div>2021-08-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/29/9b/36/b639b67e.jpg" width="30px"><span>打怪升级小菜鸟</span> 👍（0） 💬（0）<div>评论区的各位大佬，我想请教一个问题，在写时复制内存大页拷贝时，是子线程bgsave拷贝了主线程的内存页，为什么还会影响到主线程的访存操作呢？</div>2023-09-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/22/26/81/036e6579.jpg" width="30px"><span>这一行，30年</span> 👍（0） 💬（0）<div>为什么主线程 fsync 要等子线程 fsync，主线程操作旧AOF文件，重写子线程操作新AOF文件，操作的是不同的文件，为什么不可以并发进行呢？</div>2023-06-19</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/MOuCWWOnoQjOr8KjicQ84R7xu6DRcfDv3VAuHseGJ1gxXicKJboA24vOcrcJickTJPwFAU38VuwCGGkGq7f8WkTIg/132" width="30px"><span>Geek_b14c55</span> 👍（0） 💬（1）<div>不使用复杂度过高的命令，或用其他方式代替实现（放在客户端做） ，麻烦请问一下大家，这个客户端指的是应用程序吗</div>2022-08-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/2d/7c/45/949ec41d.jpg" width="30px"><span>开学！</span> 👍（0） 💬（1）<div>主从同步期间，从节点能接受客户端请求吗</div>2022-05-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1b/48/b3/fdefc913.jpg" width="30px"><span>毛薛强</span> 👍（0） 💬（0）<div>no-appendfsync-on-rewrite no 的时候不调用fsync，但是会调用write吧，如果调用了write，那么实例宕机是不会丢数据的，只有服务器宕机才会丢数据，应该是这样的吧</div>2022-04-15</li><br/><li><img src="" width="30px"><span>Geek_0bba55</span> 👍（0） 💬（1）<div>大内存那里有个点不明白:Redis是单线程操作，不存在并发问题，为什么还要用写时复制的？</div>2022-01-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/18/41/13/bf8e85cc.jpg" width="30px"><span>树心</span> 👍（0） 💬（0）<div>透明大页和标准大页的区别是什么？</div>2021-12-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1f/ae/7b/47200692.jpg" width="30px"><span>贺子</span> 👍（0） 💬（0）<div>老师说的关闭大叶的命令是关闭透明大叶的命令吧</div>2021-09-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/e2/d8/f0562ede.jpg" width="30px"><span>manatee</span> 👍（0） 💬（0）<div>请问老师如何判断是否有bigkey存在？当前库中有约4000万个key</div>2021-06-04</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/04/16/91e82e9e.jpg" width="30px"><span>Architect</span> 👍（0） 💬（2）<div>多大的key算bigkey？</div>2021-06-03</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1e/37/29/b3af57a7.jpg" width="30px"><span>凯文小猪</span> 👍（0） 💬（0）<div>其实这里的问题可以扩展到很多点 因为本质上redis是部署在linux上的。那么作为一个内存数据库必然受制于两个因素 一是内存分配 二是数据持久化。

我们先来看 内存分配。之前老师解释过内存分配redis用的jmalloc 这种特性会造成一定的数据碎片 另外与free结合使用时 实际上是内存标记回收所以内存碎片是天然存在的。

再来看数据持久化 此处用的是fork &amp;&amp; fsync &amp;&amp; write。fsync毫无疑问是write through的 而write显然是write back。 这两种模式自身的问题就不做讨论了 毕竟不是linux课程。所以因为文件系统自身机制如ext3 ext4等之类的问题依然会限制redis子进程落盘 导致主进程监控时期卡顿</div>2021-06-01</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/23/5b/983408b9.jpg" width="30px"><span>悟空聊架构</span> 👍（0） 💬（0）<div>老师的总结太棒了</div>2021-05-28</li><br/><li><img src="" width="30px"><span>Geek_e0c185</span> 👍（0） 💬（0）<div>内存页表写时复制技术主线程只需要复制改动的数据即可，老师说内存大页在写实复制时会复制内存大页的所有数据，会不会有矛盾？还是说内存页表和内存大页的写时复制需要复制的数据不一样？</div>2021-04-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/92/6d/becd841a.jpg" width="30px"><span>escray</span> 👍（0） 💬（0）<div>没有发现慢查询，也没有同时删除大量的 keys，那么接下来呢？

作为 Redis 菜鸟，我觉得大多数情况下，AOF 写回策略不需要 always 的配置。

高速固态硬盘 SSD 已经成为性能优化的“杀手锏”，如果不差钱……

操作系统内存 swap 被触发之后，会影响 Redis 主 IO 线程，那么延续上面 SSD 的思路，加大内存应该可以解决部分问题。

对于关闭内存大页机制的办法，我在 macOS 上没有找到 &#47;sys&#47;kernel 目录。

小结中的 9 个检查点 Checklist，让我觉得专栏物超所值。课代表 @kaito 令人发指的给出了 11 个检查点，让我有了秘籍在手，天下我有的感觉。

对于课后题，没有遇到过 Redis 变慢的情况，如果以后遇到了，就回到这篇专栏文章，应该能找到线索。

虽然暂时没有接触或者运维业务中的 Redis ，但是这个专栏同时也讲了很多操作系统、底层架构方面的内容，学海无涯。</div>2021-03-26</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/Q3auHgzwzM7MkIibc8UBwDt7dNeeNmx9IMqmI98Do8icxZcmfsMk99ibeXUo9ficwR1dxF5CrDHJ55603icCpKF7cxw/132" width="30px"><span>Geek_mysql45</span> 👍（0） 💬（0）<div>这一节老师总结的定位思路很清晰明了，学习了。果然还是要对redis各方面机制都了解后，才能遇到问题不抓耳挠腮，心中有redis系统架构，再去看问题就有了方向。</div>2021-03-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/99/c3/e4f408d4.jpg" width="30px"><span>陌兮</span> 👍（0） 💬（0）<div>&quot;如果既需要高性能又需要高可靠性，最好使用高速固态盘作为 AOF 日志的写入盘。&quot;
老师，这一段有点疑惑，既然redis会存在频繁的aof文件重写，那么使用ssd盘作为aof的写入盘就会频繁的刷新磁盘数据。对于ssd这种有刷盘次数限制的存储硬盘来说，那不是很快就报废了？还有一个问题想要请教下：关于aof写盘是否为磁盘顺写？感觉如果是顺序写和顺序读，使用普通的机械硬盘也是可以用的吧？</div>2021-03-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/be/30/1154657e.jpg" width="30px"><span>风含叶</span> 👍（0） 💬（0）<div>看完这篇有一种 醍醐灌顶的 感觉</div>2021-03-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/60/c5/69286d58.jpg" width="30px"><span>樱小路依然</span> 👍（0） 💬（1）<div>虽然没遇到过redis变慢的问题,但是我之前工作中遇到过 rocketmq 由于过多使用swap导致卡死的问题,当时经过排查问题后,由于内存充足,没有其他应用同机部署,所以当时的处理方式是将 swap 关闭了,没有深究问题原因</div>2021-01-27</li><br/>
</ul>