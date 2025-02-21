你好，我是徐文浩。

过去的两讲，我们分别了解了Megastore的整体架构设计，以及它对应的数据模型是怎么样的。Megastore在这两点的设计上都非常注重实用性。

**在架构设计上**，它把一个大数据库分区，拆分成了很多小数据库，互相之间相互独立。这样可以并行通过多组Paxos来复制每一个分区的事务日志，来解决单个Paxos集群的性能瓶颈问题。

**在数据模型里**，Megastore更是进一步地引入了“实体组”这个概念，Megastore的一阶段事务，只发生在单个实体组这样一个“迷你”数据库里。这些设计，都大大缓解了大型分布式数据库可能会遇到的各种单个节点的极限压力。

不过，在Megastore里我们还有一个非常重要的问题需要解决，那就是**跨数据中心的延时问题**。我们在解读[Chubby的论文](https://time.geekbang.org/column/article/428116)里已经了解过Paxos算法了，任何一个共识的达成，都需要一个Prepare阶段和一个Accept阶段。如果我们每一个事务都要这样两个往返的网络请求，我们的数据库性能一定好不到哪里去。所以，Megastore专门在原始的Paxos算法上做了改造和优化。

那么，今天我们就一起来看看Megastore具体是怎么做的。通过这一讲的学习，你可以了解这样两点：
<div><strong>精选留言（7）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/15/66/8f/02be926d.jpg" width="30px"><span>在路上</span> 👍（2） 💬（1）<div>徐老师好，学完Megastore我还是没想明白为什么它的写入吞吐量只有每秒几次。论文第2.2.3节Physical Layout提到，为了降低延迟，提高吞吐量，Megastore允许应用把数据放在靠近用户的地方，让数据的多个副本处于临近的数据中心，同时让一个EntityGroup的数据连续存储，尽量由一个TabletServer提供服务。唯一看起来有影响的是，写操作需要同步给所有副本，相关副本要么写入数据，要么标记自己的数据不是最新。

不过我在Spanner论文第6节Related Work中找到了答案，Megastore does not achieve high performance. It is layered on top of Bigtable, which imposes high communication costs. It also does not support long-lived leaders: multiple replicas may initiate writes. All writes from different replicas necessarily conflict in the Paxos protocol, even if they do not logically conflict: throughput collapses on a Paxos group at several writes per second. 主要原因有两个，一个是Bigtable带来高昂的通信成本，另一个是没有租期的Paxos Leader导致没有必要的写冲突。</div>2021-11-30</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/66/8f/02be926d.jpg" width="30px"><span>在路上</span> 👍（1） 💬（1）<div>徐老师好，学完Megastore这三讲，我觉得Megastore的性能提升在于将数据拆分打包成很小的实体组，在实体组内实现事务，在实体组间允许并发。读和写都尽可能在离用户最近的数据中心完成，读的时候采用只要没收到invalidate，数据中心就认为自己的数据是最新的，其实分布式环境下自己无法确认自己的数据是不是最新的，必须要通过集群中的其他多数节点确认，但是这种假装自己是最新的模式，加快了读操作的速度，写的时候要严格一些，先在集群中确认最新的事务日志位置。

Megastore 的写入的吞吐量慢就慢在向集群确认最新的事务日志位置。这是一种悲观的写入方式，认为对同一个实体组的写入会发生冲突，所以先确认别的数据中心中有没有新的写入。要提升吞吐量，可以采用乐观的写入方式，认为写入冲突是小概率事件，先写入，有冲突再回滚，或者解决冲突。</div>2021-11-15</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/30/c1/2dde6700.jpg" width="30px"><span>密码123456</span> 👍（0） 💬（0）<div>有个问题，就是副本的追赶。这里只说了查询会同步一次。如果长期没有查询。突然来了一次查询，那岂不是要同步很久？</div>2023-05-23</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTIVR2wY9icec2CGzZ4VKPdwK2icytM5k1tHm08qSEysFOgl1y7lk2ccDqSCvzibHufo2Cb9c2hjr0LIg/132" width="30px"><span>dahai</span> 👍（0） 💬（0）<div>徐老师，关于这句：第一步，是查询本地的协同服务器，看看想要查询的实体组是否是最新的。
中的最新是怎么判断的？这点一直没弄明白。</div>2022-01-18</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTIVR2wY9icec2CGzZ4VKPdwK2icytM5k1tHm08qSEysFOgl1y7lk2ccDqSCvzibHufo2Cb9c2hjr0LIg/132" width="30px"><span>dahai</span> 👍（0） 💬（1）<div>还有一点不明白，Leader 是一个实体组的leader，如果一个用户ID可以看作一个实体组，那么整个数据库中会有千万上亿的实体组，也会对应上亿个Leader映射关系，我这样理解对么？如果对的话，请问这些关系是在哪儿维护的？</div>2021-12-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/66/8f/02be926d.jpg" width="30px"><span>在路上</span> 👍（0） 💬（0）<div>徐老师好，bigtable论文在figure 6中说，单个tabletserver随机读取1000-byte数据，每秒大概1200次，magestore论文在第4.10节说读操作的延迟是几十毫秒，两者差距怎么这么大？如果能够命中第4.4.1节所说的Fast Reads，相比bigtable，magestore的读操作只是多了coordinator的查询，查询性能不至于差这么大啊。</div>2021-11-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/17/4f/28/7beb5271.jpg" width="30px"><span>p</span> 👍（0） 💬（1）<div>在读数据时，如果本地数据不是最新的，直接找有最新数据的副本拿不可以吗，为什么需要等待本地的数据更新完成再去响应？这块设计是因为其他副本的数据也不一定是最新有效的么，是因为存在空洞吗？</div>2021-11-21</li><br/>
</ul>