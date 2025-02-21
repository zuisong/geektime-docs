你好，我是微扰君。

上一节我们学习了数据库中非常常用的索引数据结构——B+树，在过去很多年里它都是数据库索引的首选实现方式，但是这种数据结构也并不是很完美。

因为，每次修改数据都很有可能破坏B+树的约束，我们需要对整棵树进行递归的合并、分裂等调整操作，而不同节点在磁盘上的位置很可能并不是连续的，这就导致我们需要不断地做随机写入的操作。

众所周知，随机写入的性能是比较差的。这个问题在写多读少的场景下会更加明显，而且现在很多非关系型数据库就是为了适用写多读少的场景而设计的，比如时序数据库常常面对的IOT也就是物联网场景，数据会大量的产生。所以，如果用B+树作为索引的实现方式，就会产生大量的随机读写，这会成为系统吞吐量的瓶颈。

但是考虑到非关系型数据库的检索，往往都是针对近期的数据进行的。不知道你会不会又一次想到Kafka的线性索引呢？不过很可惜，非关系型数据库的workload也不是完全append only的，我们仍然需要面对索引结构变动的需求。

那在写多读少的场景下，如何降低IO的开销呢？

LSM Tree（Log Structure Merge Tree）就是这样比B+树更适合写多读少场景的索引结构，也广泛应用在各大NoSQL中。比如基于LSM树实现底层索引结构的RocksDB，就是Facebook用C++对LevelDB的实现，RocksDB本身是一个KV存储引擎，现在被很多分布式数据库拿来做单机存储引擎，其中LSM树对性能的贡献功不可没。
<div><strong>精选留言（6）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/11/8f/cf/890f82d6.jpg" width="30px"><span>那时刻</span> 👍（4） 💬（2）<div>我想最小的segment应该与内存叶相适应，一般是4k。如果是内存大叶，可能是16k吧</div>2022-02-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/da/dd/c9735ee8.jpg" width="30px"><span>泛岁月的涟漪</span> 👍（0） 💬（1）<div>rocksdb主要是cpp吧</div>2022-04-21</li><br/><li><img src="" width="30px"><span>Paul Shan</span> 👍（0） 💬（1）<div>Segment是从内存到磁盘的读写单位，最小要设置成虚拟内存的页的大小。个人觉得设置成虚拟内存页的大小的整数倍都可以，太大会影响内存调度。
</div>2022-02-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/18/b3/15/30822e33.jpg" width="30px"><span>小麦</span> 👍（3） 💬（0）<div>MySQL InnoDB 存储引擎也提供了 MRR 优化，将批量随机写入转换成顺序写入。
此外，MySQL InnoDB 在删除行数据时也采用的标记删除，磁盘空间并不会立即回收</div>2022-06-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/21/f4/15/0542b1e6.jpg" width="30px"><span>蒋某人尚需顿悟</span> 👍（0） 💬（0）<div>es的存储应该也是lsm吧，还有个fsm是什么关系呢</div>2023-05-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/83/4a/3e08427e.jpg" width="30px"><span>药师</span> 👍（0） 💬（0）<div>每层遍历segment时也应该从最新加入的segment开始遍历吧？一层是有可能出现相同的key出现在不同的segment的情况的，那么越晚加入的到这层的segment的数据越新
如果上面成立，那是不是要维护每层segment的顺序
</div>2022-03-16</li><br/>
</ul>