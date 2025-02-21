你好，我是李玥。

在这个系列课程中，我们讲的都是如何解决生产系统中面临的一些存储系统相关的问题。在最后两节课里面，我们来说点儿新东西，看一下存储这个技术领域，可能会有哪些值得关注的新技术。当然，技术圈每天都有很多新的技术出现，也会经常发很多论文，出现很多的开源项目，这些大多数都不太靠谱儿。

今天我给你要说的这个New SQL，它是我个人认为非常靠谱，甚至在未来可能会取代MySQL这样的关系型数据库的一个技术。MySQL是几乎每一个后端开发人员必须要精通的数据库，既然New SQL非常有可能在将来替代MySQL，那我们就非常有必要提前去了解一下了。

## 什么是New SQL？

什么是New SQL？这个说来话长了，还要从存储技术发展的历史来解读。我们知道，早期只有像MySQL这样的关系数据库，这种关系型数据库因为支持SQL语言，后来被叫做SQL或者Old SQL。

然后，出现了Redis和很多KV存储系统，性能上各种吊打MySQL，而且因为存储结构简单，所以比较容易组成分布式集群，并且能够做到水平扩展、高可靠、高可用。因为这些KV存储不支持SQL，为了以示区分，被统称为No SQL。

No SQL本来希望能凭借高性能和集群的优势，替代掉Old SQL。但用户是用脚投票的，这么多年实践证明，你牺牲了SQL这种强大的查询能力和ACID事务支持，用户根本不买账，直到今天，Old SQL还是生产系统中最主流的数据库。
<div><strong>精选留言（13）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/16/e7/76/79c1f23a.jpg" width="30px"><span>李玥</span> 👍（29） 💬（0）<div>
Hi，我是李玥。

这里回顾一下上节课的思考题：

我们要做一个日志系统，收集全公司所有系统的全量程序日志，给开发和运维人员提供日志的查询和分析服务，你会选择用什么存储系统来存储这些日志？原因是什么？

对于这个问题，仍然需要根据业务对数据的查询方式，反推数据应该使用什么存储系统。对于日志的查询，最常用的二种方式就是按照关键字去查询或者指定一个时间和IP去浏览。

如果说，日志的量级不超过TB级别，直接放到ES里面最省事，对于二种查询方式都可以获得还不错的查询性能。如果规模太大了，ES也扛不住的情况下，可以考虑把日志放到HDFS中，对于浏览的查询需求，直接定位的具体的日志文件返回是比较快的。对于关键字查询的需求，也可以通过实现Map-Reduce任务，并行查询然后聚合的方式来实现。</div>2020-04-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/57/4f/6fb51ff1.jpg" width="30px"><span>奕</span> 👍（9） 💬（1）<div>New SQL 数据库是不是都是这样设计的？ 执行器支持 SQL，然后底层的存储系统是分布式存储系统？ 区别在与底层的分布式存储系统实现的原理不一样？</div>2020-04-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/ea/32/1fd102ec.jpg" width="30px"><span>真名不叫黄金</span> 👍（4） 💬（2）<div>老师讲得非常好~
不过我有一个小问题想请教一下老师，文中说到MySQL的RR级别是没有Write Skew的，但是RR使用的是MVCC读，也是快照读，理论上也会有Write Skew问题，我刚刚测试了一下，RR的事务中进行读取，是快照读不加锁，如果将老师文中的子查询拆分出来，向上提，先进行子查询的余额检查，再进行更新，开启2个事务分别更新父子账户，父账户先读取检查余额，人为没问题，然后子账户读取检查余额，也认为没问题，然后子账户更新余额并提交，父账户更新余额再提交，两个事务都可以成功，但余额不满足业务约束了，也就是Write Skew了，所以说我的理解是，RR是可能会出现Write Skew的，不知道理解有没有问题</div>2020-04-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/98/af/3945cea4.jpg" width="30px"><span>一剑</span> 👍（0） 💬（1）<div>例子中，主卡更新和副卡更新同时在两个事务里执行，容易导致死锁吧？</div>2020-04-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/34/df/64e3d533.jpg" width="30px"><span>leslie</span> 👍（9） 💬（2）<div>不知道老师是否有发现一点，现在大量的Analyze DB在对之前的MYSQL或PG SQL做补充；首当其冲的应当是阿里最近推出的此类DB；tidb做为国产数据库-目前几乎聚集了国内大多所有的RMDB方面的神人，应当是继OceanBase之后又一个国内真正汇聚顶级DB相关人才打造的数据库。老师如何去看待tidb?
谢谢老师的分享，期待后续的继续分享。</div>2020-04-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/9c/c6/05a6798f.jpg" width="30px"><span>苗</span> 👍（8） 💬（0）<div>mongodb 4.2.6也支持rc和rr级别的事务了；老师似乎很少提到mongodb。</div>2020-05-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/e0/1c/aa50dc27.jpg" width="30px"><span>icyricky</span> 👍（5） 💬（6）<div>公司有用TiDB…感觉架构很像…还是leader任期之后的续租还是选举，多数票同意选出leader，follower从leader复制数据…检测心跳…在leader宕机之后发起新一轮选举；leader对外提供读写服务，避免数据不一致</div>2020-04-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/7b/57/a9b04544.jpg" width="30px"><span>QQ怪</span> 👍（4） 💬（0）<div>我项目用的就是小强db，的确是有写性能比不上mysql，也出现了相关的锁竞争导致事务回滚的问题，解决了事务问题往往带来了其他新的问题，所以说newSQL并不是什么技术银弹:-D</div>2020-05-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/b2/5a/574f5bb0.jpg" width="30px"><span>Lukia</span> 👍（2） 💬（1）<div>不知道cockroach的两种隔离级别是不是借鉴了postgres的做法</div>2020-04-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/19/ab/88/60da22d7.jpg" width="30px"><span>健行</span> 👍（1） 💬（0）<div>老师有个点说错了。 从维基百科上可以查到，NoSQL的意思是Not only SQL。像mongoDB，支持了SQL也提供的更多方便的功能。</div>2023-09-12</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTJUw1l8kgofKxSGdtRcqYKtCzKh3gYb35sTiaj2SSgLY55sFGItBCuZSAia46ib2xRk2hEq3EudEjSDA/132" width="30px"><span>anthony</span> 👍（0） 💬（0）<div>老师 mysql 的分区表技术现在在企业里面用的多吗 oracle 的分区技术在业务系统中使用的非常多</div>2022-03-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1c/c8/7b/153181d7.jpg" width="30px"><span>夜辉</span> 👍（0） 💬（0）<div>冲突检测机制是新技术吧</div>2021-04-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/a5/98/a65ff31a.jpg" width="30px"><span>djfhchdh</span> 👍（0） 💬（0）<div>raft协议，要求全系统的节点全连接。按照投票数最多的原则选举主节点。主节点去主动同步从节点的数据，保持数据的一致性。如果主节点fail（超时或stop）则重新选举主节点。选举时，候选节点会广播RequestVote请求。</div>2020-09-22</li><br/>
</ul>