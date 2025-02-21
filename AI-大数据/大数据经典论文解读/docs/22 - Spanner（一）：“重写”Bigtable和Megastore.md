你好，我是徐文浩。

经过两个月的旅程，我们终于来到了Spanner面前。在这个课程的一开始，我们一起看过GFS这样的分布式文件存储系统，然后基于GFS的分布式存储，我们看到了Bigtable这样的分布式KV数据库是如何搭建的。接着在过去的三讲里，我们又看到了Megastore是如何基于Bigtable搭建出来的。相信你现在也发现了，通过不断利用已经搭建好的成熟系统，分布式数据库的功能越来越强大，架构也越来越复杂。

不过，即使是Megastore，它也仍然有各种各样的缺点。比如想要跨实体组实现事务，我们就需要使用昂贵的两阶段事务。而由于所有的跨数据中心的数据写入，都是通过Paxos算法来实现的，这就使得单个实体组也只能支持每秒几次的事务。

所以，最终Google还是选择了另起炉灶，实现了一个全新的数据库系统Spanner。Spanner的论文一发表，就获得了很大的反响，成为了新一代数据库的标杆。而论文的标题也很简单明确，就叫做“Google’s Globally-Distributed Database”。

那么，在接下来的两讲里，我们就一起来学习一下Spanner的这篇论文的内容。**Spanner不同于Megastore，它是一个全新设计的新系统，而不是在Megastore或者Bigtable上修修补补。**不过，Spanner从Bigtable和Megastore的设计和应用中，都汲取了非常多的养分，你会在它的论文里看到大量Bigtable和Megastore的影子。
<div><strong>精选留言（9）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/14/18/3e/f8632713.jpg" width="30px"><span>EveryDayIsNew</span> 👍（22） 💬（5）<div>越往后越难懂，貌似留言也少了，老师也不回答了</div>2021-11-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/66/8f/02be926d.jpg" width="30px"><span>在路上</span> 👍（4） 💬（0）<div>徐老师好，读完spanner论文，我想megastore写操作慢，spanner替换bigtable有六个原因：
1.megastore第4.5节提到Replication Server的一个作用是最小化bigtable写操作带来的广域网通信次数，这说bigtable的一次写操作需要和客户端的通信多次。
2.Replication Server是无状态服务，它和bigtable在一个数据中心，但是和具体的tabletServer很可能不在一台服务器上，比起spanner这增加了写操作需要的中转和通信。
3.megastore写每个数据中心都要通过chubby查找tabletServer的位置，spanner确定写哪个tablet是发生在写每个数据中心之前，只需要查一次。
4.megastore为了提供本地读的特性，要求写操作必须通知到所有的副本，而不仅仅是多数副本，这让写操作变得更慢。
5.megastore paxos在并发提议的时候，后一个提议会退回到两阶段请求，spanner paxos采用有租期的Leader，并发提议会排队，不用退回两阶段请求，这在高延时的网络中很有用。
6.spanner需要提供全局事务，bigtable内部实现的锁，比如保证单行原子性修改的逻辑，是多余的。
不知道徐老师的答案是什么样的？</div>2021-12-02</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/66/8f/02be926d.jpg" width="30px"><span>在路上</span> 👍（3） 💬（0）<div>徐老师好，这节课对比Megastore和Spanner的部分我不太理解。在 Megastore 里，每个数据中心，都是一个 Paxos 集群里的一个副本，而且是一个完全副本。这样，在每一次的数据写入时，我们都需要有网络请求到所有的数据中心。

第一、Megastore论文第2.2.3节提到一个EntityGroup写入部分地区，一个地区有3个或5个副本，原文这样描述，To minimize latency, applications try to keep data near users and replicas near each other. They assign each entity group to the region or continent from which it is accessed most. Within that region they assign a triplet or quintuplet of replicas to datacenters with isolated failure domains.

第二、Magastore论文第4.4.3节提到副本有三种，full replica, witness replica, read-only replica。为什么所有副本一定是完全副本呢，可以用其他两种啊。</div>2021-12-01</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/66/8f/02be926d.jpg" width="30px"><span>在路上</span> 👍（2） 💬（0）<div>徐老师好，读完论文的第1-2部分，我有两个问题。第一、Figure 2把tablet和replica画在了不同层级，这两个不是一个东西吗？

第二、single paxos state machine和pipelined paxos是怎么样的paxos？我自己的理解是single paxos是指一个提议完成后，才能开始下一个提议，single paxos对应mutiple paxos，它允许多个提议并发，并且使用单调递增的编号，megastore写操作看起来就是用了mutiple paxos。pipelined paxos是在上一个提议还没有完成的情况下，下一个提议在Leader上排队，而不是像megastore一样退回到两阶段。</div>2021-12-02</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/f6/e3/e4bcd69e.jpg" width="30px"><span>沉淀的梦想</span> 👍（0） 💬（2）<div>Spanner 是如何采用 B 树存储数据的呢？是像 MySQL 一样先找到根节点的 Tablet，然后不断地向下查找，直到找到叶子节点访问数据？感觉分布式环境下，这样效率是不是会有点低？
还是说采用了某种 B 树变种？</div>2023-01-02</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/22/f4/9fd6f8f0.jpg" width="30px"><span>核桃</span> 👍（0） 💬（0）<div>spanner架构的出现，首先就是提出了一个更高维度的类似全局管理者的概念，论文里面叫zone，也有一些架构设计实现叫resource manger,这个架构的出现，其实就类似分公司和集团总部的关系那样。

然后就是优化了抽象了调度模块出来，spanner的调度模块实现，和k8s的调度机制其实很类似的了，云原生领域，k8s集群调度服务到某个节点前，有两次选择，第一次是排除不适合的节点，第二次是在适合的节点挑选相对适合的。这里应该两者的思想和实现是类似的了。同时因为这些调度的策略不会经常太频繁改变，也不太会很多并发，因此可以考虑类似静态缓存数据那样保存起来。

当然除了调度以外，这里关于数据迁移的模块，这里涉及到的rebalance的概念，也就是数据重平衡，在glusterfs的实现里面，数据调度有两种，一种是数据移走，一种是数据不挪走，但是元数据改变。新节点下的更新指向原数据节点的信息，这样也算一种rebalance策略。因此在迁移调度过程中，这里为了保证数据读写平稳过渡，就可以借鉴这种思想去过渡了。</div>2022-02-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/47/00/3202bdf0.jpg" width="30px"><span>piboye</span> 👍（0） 💬（3）<div>有对标spanner 的开源实现了吗？</div>2022-01-17</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTKJrOl63enWXCRxN0SoucliclBme0qrRb19ATrWIOIvibKIz8UAuVgicBMibIVUznerHnjotI4dm6ibODA/132" width="30px"><span>Helios</span> 👍（0） 💬（1）<div>如果广州、新加坡、西雅图的三副本，用户在西雅图写入master，是不是要等到复制到广州新加坡才算结束呢。
</div>2022-01-05</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTKJrOl63enWXCRxN0SoucliclBme0qrRb19ATrWIOIvibKIz8UAuVgicBMibIVUznerHnjotI4dm6ibODA/132" width="30px"><span>Helios</span> 👍（0） 💬（0）<div>zone和数据中心的关系有点不理解，按照解释应该是一个数据中心可以有多个zone，一个zone中包含多个Spanserver，Spanserver有包含多个tablet。
但是“论文里的图2”确是按照数据中心维度的，也就意味着不同的zone之间也要进行数据同步么</div>2021-12-29</li><br/>
</ul>