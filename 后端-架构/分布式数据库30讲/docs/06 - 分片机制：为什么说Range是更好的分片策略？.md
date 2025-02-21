你好，我是王磊，你也可以叫我Ivan。

在这一讲的开头，我想请你思考一个问题，你觉得在大规模的业务应用下，单体数据库遇到的主要问题是什么？对，首先就是写入性能不足，这个我们在[第4讲](https://time.geekbang.org/column/article/274200)也说过，另外还有存储方面的限制。而分片就是解决性能和存储这两个问题的关键设计，甚至不仅是分布式数据库，在所有分布式存储系统中，分片这种设计都是广泛存在的。

所以今天，就让我们好好了解一下，分片到底是怎么回事儿。

## 什么是分片

分片在不同系统中有各自的别名，Spanner和YugabyteDB中被称为Tablet，在HBase和TiDB中被称为Region，在CockraochDB中被称为Range。无论叫什么，概念都是一样的，分片是一种水平切分数据表的方式，它是数据记录的集合，也是数据表的组成单位。

分布式数据库的分片与单体数据库的分区非常相似，区别在于：分区虽然可以将数据表按照策略切分成多个数据文件，但这些文件仍然存储在单节点上；而分片则可以进一步根据特定规则将切分好的文件分布到多个节点上，从而实现更强大的存储和计算能力。

分片机制通常有两点值得关注：

1. 分片策略

主要有Hash（哈希）和Range（范围）两种。你可能还听到过Key和List，其实Key和List可以看作是Hash和Range的特殊情况，因为机制类似，我们这里就不再细分了。
<div><strong>精选留言（19）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/1d/12/13/e103a6e3.jpg" width="30px"><span>扩散性百万咸面包</span> 👍（20） 💬（2）<div>思考题：
大部分分布式系统都有这么一个存储元数据的东西，比如TiDB的PD，HBase里的ZK，k8s的etcd。也可以把他们看成存储小数据的KV存储系统，一般通过Raft或者Paxos来维持共识，就跟普通分布式系统一样</div>2020-09-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/ea/32/1fd102ec.jpg" width="30px"><span>真名不叫黄金</span> 👍（9） 💬（4）<div>猜测一下，如果是TiDB的话，将元数据存在PD，而PD本身又可部署为多节点高可用的，不过数据最终是落在etcd的，PD只是交互节点。
Spanner如何做的就不太好猜测，但是Spanner也有PD这个角色，也许是差不多的。</div>2020-08-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1d/12/13/e103a6e3.jpg" width="30px"><span>扩散性百万咸面包</span> 👍（9） 💬（2）<div>Hash 分片写性能出众，但查询性能差，Range 则相反。

没懂这一句话，文章中哪里有详细阐释为什么Hash分片的写性能更好呢？为什么Range的写性能就不行呢？</div>2020-08-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/81/e6/6cafed37.jpg" width="30px"><span>旅途</span> 👍（4） 💬（1）<div>多数采用半同步复制，平衡可靠性和性能。这意味着，所有分片的主副本必须运行在 Set 的主节点上。

老师,这句话没懂,为什么使用半同步复制,所有分片的主福本都运行在set主节点呢</div>2020-09-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1a/05/fc/bceb3f2b.jpg" width="30px"><span>开心哥</span> 👍（4） 💬（1）<div>元数据搞个etcd存起来如何？</div>2020-08-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/71/3d/da8dc880.jpg" width="30px"><span>游弋云端</span> 👍（1） 💬（1）<div>元数据集中存储，特别是能用全内存性能最好，但可靠性不足，一般做HA;或者元数据可以做一致性Hash来分片打散，个人认为Range不适合元数据，变化了数据位置不好计算。</div>2020-08-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/ed/3e/c1725237.jpg" width="30px"><span>楚翔style</span> 👍（0） 💬（1）<div>hash环那里,A(0-3)表示只能放3个hash值吗?这个区间可以随意设置吗?</div>2020-10-16</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1d/12/13/e103a6e3.jpg" width="30px"><span>扩散性百万咸面包</span> 👍（4） 💬（1）<div>老师，PGXC的这种模式，如果按Set来分片的话，那么为什么不能像Multi Raft Group一样，主Set副本分布在不同节点呢？这样就可以把读写压力分摊在不同节点上了。</div>2020-09-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1c/f2/66/b16f9ca9.jpg" width="30px"><span>南国</span> 👍（4） 💬（0）<div>分片数据存在分布式文件系统里，元数据像bigtable一样用一个高可靠的协调中心存，比如Zookeeper，在合并和分裂的时候修改元数据，客户端缓存需要的元数据，修改的时候通知即可</div>2020-08-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/bb/ca/86d58e40.jpg" width="30px"><span>yang</span> 👍（3） 💬（0）<div>hash--分片，基于hash槽的设计几乎没讲--，比如redis-cluster--事实上这种在大规模应用中反而会更多。</div>2021-04-25</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/DYAIOgq83eqZCrVvIxvzSrvmoJAa3pTNGDabbq2ssvc8Z8jfGKKJiaNlNEm67BfTdfN0Bq2ypNvByHiboibpOyQBA/132" width="30px"><span>Geek_4e4b8b</span> 👍（2） 💬（0）<div>作者可以研究下mongodb的hash分片，还是挺巧妙的，他的算法依赖的应该不是节点数，而是跟数据的chunk数相关，这样增减节点，只是涉及chunk的移动，不会大面积做全部数据的重平衡。当然算法如果仅仅只是chunk数相关，那chunk数变化就会触发算法变化，所以应该是做了优化的，保证chunk的分裂只会影响分裂chunk的数据移动。</div>2020-08-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/2b/4a/72/e39f3bc7.jpg" width="30px"><span>Dancer</span> 👍（1） 💬（0）<div>尝试回答一下思考题，在分布式存储系统中一般都会有一个专门管理元数据的节点，这个节点可以用来存储动态变化的Range分片以及其他的元数据。这个管理元数据的节点在不同的分布式存储系统中使用的中间件都是不同的，有的是自己实现一套简单的强一致性kv系统（一般是通过Raft或者Paxos来保证数据的一致性），有的是直接复用已有的分布式协调系统（zookeeper，etcd等等）</div>2022-01-11</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTIKoEicqUZTJly55qoUXRmK4wia7YbnibsMncJaO6tKgKAQNJRfpMsibvfeiaukIibsCsuaic8QjQ3gOoTGA/132" width="30px"><span>张可夫斯基</span> 👍（0） 💬（0）<div>---原文
从架构设计角度看，Group 比 Set 更具优势，原因主要有两个方面。首先，Group 的高可靠单元更小，出现故障时影响的范围就更小，系统整体的可靠性就更高。其次，在主机房范围内，Group 的主副本可以在所有节点上运行，资源可以得到最大化使用，而 Set 模式下，占大多数的备节点是不提供有效服务的，资源白白浪费掉。

--问题

（这里可以斟酌一下，我们将海量数据划为不同的分片，每个分片使用Set来存储还是使用Group来存储在资源的使用上看是没有多大区别的，区别的是Set使用半同步来保证数据一致性，Group基于Raft保证数据一致性。 如果PGXC的所有分片主副本必须运行在Set的主节点上，那么它的写性能就是单机性能了。）</div>2022-03-04</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/20/d4/37/3c179df6.jpg" width="30px"><span>阿白</span> 👍（0） 💬（0）<div>总结一下hash分片, 其实有两类分片:
1.根据数据节点个数进行分片，node_id = hash(key) % 节点个数 ，上面介绍了.
2.在node上增加一层 chunk(redis-cluster叫slot)，这种典型的是redis-cluster，slot里的数据可以移动到不同的node上.</div>2022-02-25</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/bb/cc/fac12364.jpg" width="30px"><span>xxx</span> 👍（0） 💬（0）<div>这个问题很重要，老师是高手。</div>2022-02-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/2b/b8/81/a0afe928.jpg" width="30px"><span>杜思奇</span> 👍（0） 💬（0）<div>Teradata利用主索引求hash值，将数据分布到不同的AMP上。而GaussDB(DWS)是对主键求hash</div>2021-12-14</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTJMsZRXU5AAdOQCpPZmowTqyBcibQWjEKssEL3LNq97JNaqHAceCsiadmMgRl8d9PZg3OsOk9bibAlew/132" width="30px"><span>Geek_c39fbe</span> 👍（0） 💬（1）<div>本章的range分片是不是比较适合number类型的，例子中的按照北京、上海这种地区进行分片，怎么进行range分片？</div>2021-07-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/00/ac/614b8eb2.jpg" width="30px"><span>余学文</span> 👍（0） 💬（0）<div>请教老师一个问题，newsql的复制组如果将多副本存储在不同的机房，理论上是否可以实现数据库的异地多活，这会存在什么问题？</div>2020-09-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/1a/9c/082cf625.jpg" width="30px"><span>权</span> 👍（0） 💬（2）<div>es的，ceph的分片机制也是类似，ceph有自动rebalance,es貌似要手动</div>2020-08-21</li><br/>
</ul>