你好，我是徐文浩。

大数据技术一开始，更像一个专有系统。但是随着时间的推移，工程师们越来越多地让这些大数据系统支持上了SQL的特性。于是我们看到了Hive让大家可以用SQL来执行MapReduce任务，Dremel这样的系统更是一开始就支持了SQL。对于OLAP的分析类系统来说，支持Schema定义、支持字段类型、支持直接用类SQL的语言进行数据分析，很快就成为了新一代大数据分析系统的标准。

所以，Google想要在Bigtable这样的OLTP数据库上支持SQL，也不会让我们意外了。那么接下来，我们就一起来看一看《Megastore: Providing scalable, highly available storage for interactive services》这篇论文，为我们带来了一个什么样的分布式系统。

Megastore是一个雄心勃勃的系统，支持SQL这样的接口只是它想要做到的所有事情中的一小项。如果列出Megastore支持的所有特性，相信也是一个让人两眼放光的系统，好像是分布式数据库的终极答案：

- 跨数据中心的多副本同步数据复制；
- 支持为数据表的字段建立Schema，并且可以通过SQL接口来访问；
- 支持数据库的二级索引；
- 支持数据库的事务。
<div><strong>精选留言（11）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/11/30/c1/2dde6700.jpg" width="30px"><span>密码123456</span> 👍（1） 💬（1）<div>用paxos，来同步数据。虽然一致性，可以保障。但是更新数据那么频繁，每次同步数据都要2轮通信。而且还是跨数据中心，天然就是慢。那基于什么样的考虑，使用的呢？</div>2023-05-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/66/8f/02be926d.jpg" width="30px"><span>在路上</span> 👍（20） 💬（0）<div>徐老师好，Megastore通过对实体组分区，让数据库日志能并行复制，很像在编程的时候，用线程池来处理用户请求，通过对用户id取模的方法，将请求分发给不同的线程，使得用户请求可以被并行处理。用户请求一般只操作自身数据，如果需要操作其他用户的数据，要么加锁，要么丢给对应的线程处理。

在APRG游戏开发中，玩家的数据一般以文档的形式存储，类似于实体组的概念，这份数据包括玩家等级、属性、技能、装备、背包等各种信息。玩家的很多行为都不涉及其他玩家，比如在游戏中签到并领取奖励，只会改变自己的数据。不过如果他需要和其他玩家交易物品，就涉及到“同时”改变自己和对方的数据，要么加锁，要么丢到其他线程或进程处理。如果玩过“奇迹”这款游戏的同学都知道，两个人需要去到同一场景才能完成交易，去同一场景这个行为其实就是让两个人处于同一个线程或进程内，因为一个场景的所有请求会被顺序处理，工程师们通过这个方法简化了交易逻辑的实现难度。</div>2021-11-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/0f/70/f59db672.jpg" width="30px"><span>槑·先生</span> 👍（2） 💬（1）<div>先前了解过 TiDB 这种 NewSQL，再看 MegaStore 似乎非常好理解。 </div>2022-06-07</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTKJrOl63enWXCRxN0SoucliclBme0qrRb19ATrWIOIvibKIz8UAuVgicBMibIVUznerHnjotI4dm6ibODA/132" width="30px"><span>Helios</span> 👍（2） 💬（0）<div>Megastore号称多数据中心的同步，但是是有前提的，是针对同一个分区即实体组。和很多kv数据库舍弃了数据库事务一样，megastore也只能保证实体组内的事务，做做个人的文章集合还可以。就想发微博这种貌似在一个实体组，但是最终涉及到多个，业务越发展并不能保证实体没有关联</div>2021-12-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/22/f4/9fd6f8f0.jpg" width="30px"><span>核桃</span> 👍（1） 💬（0）<div>再次理解了一下实体组的概念，这个概念的出现，和传统的数据库中的表级锁，行级锁甚至全局锁是否有关系呢？对于传统的数据库来说，行级锁已经是很细粒度的锁了。但是往往一个用户的操作，是涉及到多个不同的表的数据，而Megastore的实体组概念，其实就是把本该属于一个用户对象下所有涉及的表的数据及对象结构包装成一个整体的概念，然后这样的数据进行操作，就和以前的行级锁思想有点类似了，但是更加适合大数据及分布式环境下。

同时对于跨越实体组的事务，使用异步复制这个方案，这里其实也有一个缺陷的。当队列中如果数据满了，或者前面有一个事务很久都没搞定出现问题，那么队列就可能会出现各种问题了，所以这里可以出现二级队列。 做法就是一级队列是接受到跨越实体组的事务请求，但是如果事务执行失败或者有问题了，那么尝试一定次数之后，直接扔到二级队列去处理，不要影响到后续的处理，同时也可以引入优先队列等尝试，这样就更加完善了。</div>2022-02-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/00/4e/be2b206b.jpg" width="30px"><span>吴小智</span> 👍（1） 💬（0）<div>实体组的多少需要提前定义嘛？实体组的扩缩容怎么办？</div>2021-11-16</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/8f/60/be0a8805.jpg" width="30px"><span>陈迪</span> 👍（1） 💬（0）<div>你下单，我下单，但都要扣共同的、全局的商品</div>2021-11-16</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1a/2e/c5/231114ed.jpg" width="30px"><span>Hadesu</span> 👍（0） 💬（0）<div>1. 异步消息队列是不是分布式的？
2. 实例组请求到异步消息队列失败怎么处理？
3. 异步消息队列请求到实例组失败怎么处理？</div>2024-12-03</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/22/f4/9fd6f8f0.jpg" width="30px"><span>核桃</span> 👍（0） 💬（2）<div>这里有个难题，对于同一个实体组里面写入的时候，怎么知道先后顺序呢？例如还是三副本机制下，往A节点的实体组1 写入的数据，然后中断了，再考虑往B中写入的话，怎么知道两次写入的先后呢？

这里的隐藏条件就是实体组之间是否需要分主次副本机制，如果分了，那么还是先找主来写入的话，当用户距离切换了，导致写入主的时候延迟比较大该怎么办？ 

如果不分的话，我想到的一种解决策略就是写入之前，先注销掉当前写入的批次的id，这里需要使用到全局唯一的id的方式来解决，再配合上各种修复逻辑才能完善实体组的概念吧。噢，把其他的内容串联起来了。</div>2022-02-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/04/30/7f2cb8e3.jpg" width="30px"><span>CRT</span> 👍（0） 💬（0）<div>不同数据中心之间的数据分区，这里的分区应该理解为数据副本更加合适？</div>2021-11-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1d/15/86/15b942d6.jpg" width="30px"><span>扭高达💨🌪</span> 👍（0） 💬（0）<div>Megastore有点像hdfs同步元数据，通过journal node或者bookkeeper写入元数据 其他的namenode异步消费同步元数据</div>2021-11-11</li><br/>
</ul>