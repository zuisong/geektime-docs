你好，我是唐聪。

在软件开发过程中，我们经常会遇到需要批量执行多个key操作的业务场景，比如转账案例中，Alice给Bob转账100元，Alice账号减少100，Bob账号增加100，这涉及到多个key的原子更新。

无论发生任何故障，我们应用层期望的结果是，要么两个操作一起成功，要么两个一起失败。我们无法容忍出现一个成功，一个失败的情况。那么etcd是如何解决多key原子更新问题呢？

这正是我今天要和你分享的主题——事务，它就是为了**简化应用层的编程模型**而诞生的。我将通过转账案例为你剖析etcd事务实现，让你了解etcd如何实现事务ACID特性的，以及MVCC版本号在事务中的重要作用。希望通过本节课，帮助你在业务开发中正确使用事务，保证软件代码的正确性。

## 事务特性初体验及API

如何使用etcd实现Alice向Bob转账功能呢？

在etcd v2的时候， etcd提供了CAS（Compare and swap），然而其只支持单key，不支持多key，因此无法满足类似转账场景的需求。严格意义上说CAS称不上事务，无法实现事务的各个隔离级别。

etcd v3为了解决多key的原子操作问题，提供了全新迷你事务API，同时基于MVCC版本号，它可以实现各种隔离级别的事务。它的基本结构如下：
<div><strong>精选留言（20）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/22/3a/de/e5c30589.jpg" width="30px"><span>云原生工程师</span> 👍（5） 💬（1）<div>老师分析得透彻，学习了，原来自己平时使用的事务过程中，无意间已经使用了串行化快照隔离级别，还请问一下事务性能相比put接口差异大吗</div>2021-02-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/68/83/ecd4e4d6.jpg" width="30px"><span>WGJ</span> 👍（0） 💬（2）<div>老师，有个问题就是 在原子性和持久性介绍当中，假如在WAF日志已经提交成功了，执行事务的时候发生了crash，这时候我理解的返回给client是失败的，那么当执行WAF重放日志的时候，该事务又成功了；换句话说，事务操作 返回给client 结果 的时机是什么时候呢，是写 WAF日志成功就返回呢，还是等待事务提交之后才返回呢</div>2021-02-19</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/ib3Rzem884S5MOS96THy0gQXcF26PNsnRBpyr3pM5rVibZdYvAibpVvAGfibF1ddpgrteg9fQUsq4vce9EM95Jj97Q/132" width="30px"><span>Geek_604077</span> 👍（12） 💬（1）<div>在数据库事务中，有各种各样的概念，比如脏读、脏写、不可重复读与读倾斜、幻读与写倾斜、更新丢失、快照隔离、可串行化快照隔离? 你知道它们的含义吗？
脏读、脏写：

在读未提交的隔离级别的情况下，事务A执行过程中，事务A对数据资源进行了修改，事务B读取了事务A修改后且未提交的数据。A因为某些原因回滚了操作，B却使用了A对资源修改后的数据，进行了读写等操作。

不可重复读：

在读未提交、读提交的隔离级别情况下，事务B读取了两次数据资源，在这两次读取的过程中事务A修改了数据，导致事务B在这两次读取出来的数据不一致。这种在同一个事务中，前后两次读取的数据不一致的现象就是不可重复读。

幻读：

在可重复读得隔离级别情况下，事务B前后两次读取同一个范围的数据，在事务B两次读取的过程中事务A新增了数据，导致事务B后一次读取到前一次查询没有看到的行。

读倾斜、写倾斜：

读写倾斜是在数据分表不合理的情况下，对某个表的数据存在大量的读取写入的需求，分表不均衡不合理导致的。

更新丢失：

第一类丢失，在读未提交的隔离级别情况下，事务A和事务B都对数据进行更新，但是事务A由于某种原因事务回滚了，把已经提交的事务B的更新数据给覆盖了。这种现象就是第一类更新丢失。

第二类丢失，在可重复读的隔离级别情况下，跟第一类更新丢失有点类似，也是两个事务同时对数据进行更新，但是事务A的更新把已提交的事务B的更新数据给覆盖了。这种现象就是第二类更新丢失。

快照隔离：

每个事务都从一个数据库的快照中读数据，如果有些数据在当前事务开始之后，被其他事务改变了值，快照隔离能够保证当前事务无法看到这个新值。

可串行化快照隔离：

可串行化快照隔离是在快照隔离级别之上，支持串行化。
（讲得特别好，肯定花了特别多的心思跟时间，肯定掉了好多头发🐶，给老师点赞）</div>2022-02-15</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/31/4f/45/507464b6.jpg" width="30px"><span>warm</span> 👍（1） 💬（1）<div>觉得可串行快照读讲的不是很详细还是我理解不到位。是每次执行事务都要先拿到读写锁还是在检测冲突重试才加读写锁？如果是前者根本没必要做冲突检测</div>2023-08-21</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTLDUJyeq54fiaXAgF62tNeocO3lHsKT4mygEcNoZLnibg6ONKicMgCgUHSfgW8hrMUXlwpNSzR8MHZwg/132" width="30px"><span>types</span> 👍（1） 💬（0）<div>关于事务txn，请问事务都是在leader执行的嘛？还是根据request中的动作决定？</div>2021-09-25</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/YbUxEV3741vKZAiasOXggWucQbmicJwIjg3HDE58oyibYXbSop9QQFqZ7X6OhynDoo6rDHwzK8njSeJjN9hx3pJXg/132" width="30px"><span>黄堃健</span> 👍（0） 💬（0）<div>老师，在etcd看来，写事件时，先获取数据，然后获取mvcc的读写锁，获取锁之后，再次读取数据，比较符合预期，最后更新数据。 看上去不像是乐观锁。 更像悲观锁</div>2024-03-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/29/bc/c4/791d0f5e.jpg" width="30px"><span>akiqiu</span> 👍（0） 💬（0）<div>感觉可串行化的SSI有点牵强呢？看上去是用户手工来实现了SSi，而不是etcd自己实现了SSI。而且通过读代码，发现所有写操作在获取batchTx后都会LockInsideApply，是一个独占锁，所以看上去写操作是串行的，所以写事务应该也是串行的？我感觉是严格的串行执行写操作实现了可串行化。correct me if i&#39;m wrong</div>2024-02-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/29/bc/c4/791d0f5e.jpg" width="30px"><span>akiqiu</span> 👍（0） 💬（0）<div>请问etcd存在写-写并发冲突吗？因为并发写请求经过raft后，应该已经被整理成顺序执行的一个个条目，交给状态机串行地去apply了。这样在存储层还存在写-写并发冲突吗？</div>2024-02-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/22/e1/6b/74a8b7d8.jpg" width="30px"><span>Hugh</span> 👍（0） 💬（0）<div>在快照串行化隔离的案例里面，有个问题想请教一下，首先冲突检测机制是在提交前进行检测的，那么意味着无论提交是否成功，大部分的节点都已经写入了raft log或者WAL，假设这次检测的结果是失败的（比如已经没有足够的钱进行转账），那么就不会提交了（给客户端的反馈也是此次转账失败）。
这个时候leader节点突然宕机，其他节点重新开始了选举，那些已经写入此次转账log的节点是有可能成为新的leader，在新的任期中，仍然会尝试提交这次事务，假设这次提交时已经有了足够的金额，则会导致提交成功。但是这次的提交成功对于客户端来说完全不感知，这样子就会导致用户发现自己的金额突然变少了，这个肯定是不符合预期的，老师可以解释一下这中间是不是有哪部分我的理解有问题呢</div>2022-06-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/19/96/a2/c1596dd8.jpg" width="30px"><span>🤔</span> 👍（0） 💬（1）<div>etcd事务可用在分布式事务吗？</div>2022-02-15</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTLDRPejHodutia9Ud8UZLY8g5lTkKXgf3J104c0jM9aFfAGNoUdxkRLnnWRc5Kd3jIeN3EqXxKFT0g/132" width="30px"><span>蓝莓侠</span> 👍（0） 💬（0）<div>串行化快照隔离中的冲突检测，感觉和CAS一样啊，有什么区别吗？</div>2022-02-14</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/jA97yib7VetXc4iclOg2gGfZu1fO7efyib2mKeqvIxDdmgLqukusyFzPrbIQeZYR0WDJUicRakgVGroaYC7aWGFrEw/132" width="30px"><span>Turing</span> 👍（0） 💬（0）<div>这篇文章含金量很高, 分布式中的acid和数据库中的acid是不一样的概念. 其实事务提交的时候还是走了读写锁, 读写锁的目的应该是为了回写buffer吧. etcd事务提交, 并不一定立马持久化到磁盘中. </div>2021-11-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/11/3e/925aa996.jpg" width="30px"><span>HelloBug</span> 👍（0） 💬（0）<div>&gt;Apply 模块首先执行 If 的比较规则，为真则执行 Then 语句，否则执行 Else 语句
这里执行Then里的命令的时候，为什么不可能发生状态的变更呢？例如向Bob转账100，put bob 300时，bob的账户已经是300了，就是说判断的时候还没问题，执行Then的时候就有问题了。</div>2021-11-05</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/11/3e/925aa996.jpg" width="30px"><span>HelloBug</span> 👍（0） 💬（0）<div>极端一点考虑，冲突检测的时候可能会发生很多次的冲突，这样应用程序如果只进行了一次的冲突检测，是可能出现事务提交失败的情况的，对吗？</div>2021-11-05</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/11/3e/925aa996.jpg" width="30px"><span>HelloBug</span> 👍（0） 💬（0）<div>&gt;&gt;为了解决并发事务冲突问题，事务 A 中增加了冲突检测，期望的 Alice 版本号应为 2，Bob 为 3。结果事务 B 的修改导致 Bob 版本号变成了 5
这里Bob的版本号应该是变成了4吧？</div>2021-11-05</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/11/3e/925aa996.jpg" width="30px"><span>HelloBug</span> 👍（0） 💬（0）<div>已提交读和可重复读本身就是互相冲突的，如果每次都能读取已经提交的数据，那重复读的时候，前后两次的数据就可能是不一样的，可重复读无法保证。如果利用文中说的第一次读的时候，将读到的数据放在一个缓存里，然后下一次读的时候，读取到的数据就和上一次一样，这样读取到的数据就不是已提交的。这两个特性不可能同时满足吧？</div>2021-11-05</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTIAfpw5Mm3UNgMdju8V3WSbQiaHp4RxaG3JTz9Zx3dtL32Rib7zTVn6v7a1OF6KQcmQYnnILrSmee8g/132" width="30px"><span>降措</span> 👍（0） 💬（0）<div>多次执行stm事务时，偶尔会提示etcdserver: mvcc: required revision is a future revision，一直没有发现是什么原因</div>2021-07-16</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTLDUJyeq54fiaXAgF62tNeocO3lHsKT4mygEcNoZLnibg6ONKicMgCgUHSfgW8hrMUXlwpNSzR8MHZwg/132" width="30px"><span>types</span> 👍（0） 💬（1）<div>etcd事务默认的隔离级别是什么？ 可重复读？</div>2021-03-03</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1b/30/85/14c2f16c.jpg" width="30px"><span>石小</span> 👍（0） 💬（1）<div>“由于 etcd 是批量提交写事务的，而读事务又是快照读，因此当 MVCC 写事务完成时，它需要更新 buffer，这样下一个读请求到达时，才能从 buffer 中获取到最新数据。”  会不会出站事务完成后更新buffer失败的情况？</div>2021-03-01</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/57/4f/6fb51ff1.jpg" width="30px"><span>奕</span> 👍（0） 💬（0）<div>可串行化的快照隔离: 是每个事物都会生成一个新的快照吗？</div>2021-02-24</li><br/>
</ul>