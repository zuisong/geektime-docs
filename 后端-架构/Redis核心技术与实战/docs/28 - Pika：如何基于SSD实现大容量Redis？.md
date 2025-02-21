你好，我是蒋德钧。

我们在应用Redis时，随着业务数据的增加（比如说电商业务中，随着用户规模和商品数量的增加），就需要Redis能保存更多的数据。你可能会想到使用Redis切片集群，把数据分散保存到多个实例上。但是这样做的话，会有一个问题，如果要保存的数据总量很大，但是每个实例保存的数据量较小的话，就会导致集群的实例规模增加，这会让集群的运维管理变得复杂，增加开销。

你可能又会说，我们可以通过增加Redis单实例的内存容量，形成大内存实例，每个实例可以保存更多的数据，这样一来，在保存相同的数据总量时，所需要的大内存实例的个数就会减少，就可以节省开销。

这是一个好主意，但这也并不是完美的方案：基于大内存的大容量实例在实例恢复、主从同步过程中会引起一系列潜在问题，例如恢复时间增长、主从切换开销大、缓冲区易溢出。

那怎么办呢？我推荐你使用固态硬盘（Solid State Drive，SSD）。它的成本很低（每GB的成本约是内存的十分之一），而且容量大，读写速度快，我们可以基于SSD来实现大容量的Redis实例。360公司DBA和基础架构组联合开发的Pika[键值数据库](https://github.com/Qihoo360/pika)，正好实现了这一需求。

Pika在刚开始设计的时候，就有两个目标：一是，单实例可以保存大容量数据，同时避免了实例恢复和主从同步时的潜在问题；二是，和Redis数据类型保持兼容，可以支持使用Redis的应用平滑地迁移到Pika上。所以，如果你一直在使用Redis，并且想使用SSD来扩展单实例容量，Pika就是一个很好的选择。
<div><strong>精选留言（30）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/10/c4/92/338b5609.jpg" width="30px"><span>Roy Liang</span> 👍（31） 💬（4）<div>SSD使用寿命和擦写次数相关，我们有的业务数据量和访问量特别大，使用SSD一年就得换了，这样实际成本降不下来。所以，请问有没有可能开发一套混合存储系统，热数据存储而不是缓存在Redis，冷数据存储在Pika，Redis中的热数据淘汰时，自动写入Pika，Pika的冷数据加载时，自动写入Redis，这样业务代码几乎就不用做数据一致性维护相关的内容。不知道这个系统是否存在可行性？其中的技术风险可能在哪里？</div>2020-10-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/cf/81/96f656ef.jpg" width="30px"><span>杨逸林</span> 👍（5） 💬（4）<div>Redis 服务器有没有必要上 ECC 内存？
还有如果那个  Memtable 有没有极端情况，Memtable1 还在写入 SSD，Memtable2 已经满了，这怎么办？虽然写入 SSD 很快，我是说如果。

binlog 机制在 MySQL 那已经玩烂了。。。</div>2020-10-25</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/71/3d/da8dc880.jpg" width="30px"><span>游弋云端</span> 👍（3） 💬（1）<div>可以考虑内存、SSD、HDD做分级存储，当前这对系统要求就更高了，需要识别数据的冷温热，再做不同介质间的动态迁移，甚至可以做一些访问预测来做预加载和调级。</div>2020-10-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/cb/f9/75d08ccf.jpg" width="30px"><span>Mr.蜜</span> 👍（0） 💬（1）<div>只要能区分出冷热数据，启用机械硬盘作为一部分存储介质也是一个可取的方案。</div>2020-11-13</li><br/><li><img src="" width="30px"><span>dfuru</span> 👍（0） 💬（1）<div>使用机械硬盘作为实例容量扩展：
1. 在pika的解决方案中，当写满一个memtable时，切换memtable,将写满的memtable中的数据已文件的形式持久化到硬盘上。
   硬盘具体是SSD、机械硬盘还是NVME，都可以。
2. 使用机械硬盘，容量更大，价格更便宜，读写性能更低。大量数据访问机械盘时，磁盘IO是主要瓶颈。</div>2020-10-31</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/90/8a/288f9f94.jpg" width="30px"><span>Kaito</span> 👍（113） 💬（6）<div>是否可以使用机械硬盘作为Redis的内存容量的扩展？

我觉得也是可以的。机械硬盘相较于固态硬盘的优点是，成本更低、容量更大、寿命更长。

1、成本：机械硬盘是电磁存储，固态硬盘是半导体电容颗粒组成，相同容量下机械硬盘成本是固态硬盘的1&#47;3。
2、容量：相同成本下，机械硬盘可使用的容量更大。
3、寿命：固态硬盘的电容颗粒擦写次数有限，超过一定次数后会不可用。相同ops情况下，机械硬盘的寿命要比固态硬盘的寿命更长。

但机械硬盘相较于固态硬盘的缺点也很明显，就是速度慢。

机械硬盘在读写数据时，需要通过转动磁盘和磁头等机械方式完成，而固态硬盘是直接通过电信号保存和控制数据的读写，速度非常快。

如果对于访问延迟要求不高，对容量和成本比较关注的场景，可以把Pika部署在机械硬盘上使用。

另外，关于Pika的使用场景，它并不能代替Redis，而是作为Redis的补充，在需要大容量存储（50G数据量以上）、访问延迟要求不苛刻的业务场景下使用。在使用之前，最好是根据自己的业务情况，先做好调研和性能测试，评估后决定是否使用。</div>2020-10-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/ec/13/49e98289.jpg" width="30px"><span>neohope</span> 👍（23） 💬（2）<div>用机械硬盘阵列来做缓存，其实没有必要，速度太慢了：
1、用redis来做缓存，就是因为mysql慢，所以加了一层
2、redis比mysql快的最根本原因，不是redis技术强悍，而是内存比磁盘快
3、mysql本身就是把热数据放到内存里，冷数据存到磁盘阵列上，并且做了很多数据查找的优化
4、pika利用的是SSD比磁盘快，比内存便宜，才找到了自己的生存空间，其根本原因也不是RocksDB技术先进；
5、Pika的用磁盘做缓存，从磁盘上查找记录，比mysql也快不了太多，解决不了什么问题，而且还引入了新的故障点，没有太多价值
</div>2021-02-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/a0/c4/4ab49f4e.jpg" width="30px"><span>孔祥鑫</span> 👍（8） 💬（4）<div>有个地方没搞明白，读ssd上的数据文件，和redis读rdb文件相比，两者都是文件，为什么会比redis快呢</div>2020-11-16</li><br/><li><img src="" width="30px"><span>Geek_9a0c9f</span> 👍（6） 💬（0）<div>pika从性能上比当然不然redis,但是它你补了redis几个不足，那么pika在真是项目中都应用在什么场景呢？，与ssd的mysql比优势在哪里？除了o(1)的操作。</div>2020-10-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/24/05/a6/098dfae1.jpg" width="30px"><span>Q, Q</span> 👍（5） 💬（4）<div>pika实际是使用ssd提高性能，那还不如把redis层去掉，mysql直接上ssd岂不是更加方便？</div>2021-08-01</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/49/a5/e4c1c2d4.jpg" width="30px"><span>小文同学</span> 👍（5） 💬（0）<div>机械硬盘和 SSD 在性能上最大的区别是因为机械硬盘的随机访问涉及到机器臂的移动和寻址，所以非常慢。但我在了解 Pika 对文件的使用上，其实有考虑过这方面的问题，通过 A、B两块内存交换使用，以一块内存为单位进行磁盘写，在这个情况下。我认为机械硬盘的写性能并不一定比 SSD 差很多。

在读数据的情况下，假如没有热点数据，和存在大量的随机读，则机械硬盘的读性能会显得很差，反之，由于有一大块的内存做缓冲，读性能或许并不会太差，这取决于业务场景。

剩余机械硬盘的某些优势还是比较明显，Kaito 班长的留言已经非常明白，顾不复述。</div>2020-11-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/c1/c6/1456274a.jpg" width="30px"><span>麦呆小石头</span> 👍（4） 💬（0）<div>pika 的存储机制，集合类型的性能会低很多啊，hash 和跳表的特性都没了吧</div>2020-12-02</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/19/b3/49/79024ed2.jpg" width="30px"><span>Tr丶Zoey</span> 👍（2） 💬（2）<div>有没有人用ssdb的啊？😂
老大让我们用这个代替redis，说没问题，结果用下来坑真的多。。。</div>2021-02-02</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/23/f8/24fcccea.jpg" width="30px"><span>💢 星星💢</span> 👍（1） 💬（1）<div>Pika 的多线程模型，可以同时使用多个线程进行数据读写，这在一定程度上弥补了从 SSD 存取数据造成的性能损失，多线程读写，会涉及到数据竞争吧，pika这一块是否有优雅的处理呢？</div>2021-01-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/9a/ab/fd201314.jpg" width="30px"><span>小耿</span> 👍（0） 💬（0）<div>优势：机械硬盘的优势是成本更低，在对性能要求不高时，可以用更少的成本保存更多的数据。
劣势：机械硬盘相对固态来说读写速度更慢，必然会影像pika的读写、重启、同步的性能。 pika 主要为了解决 redis 大内存实例主从同步、恢复慢，缓存溢出的问题，使用机械硬盘在读写速度降低的情况下，是否能有效改进同步、恢复慢的问题，需要验证。而对于缓存溢出，机械硬盘应该可以有效解决。</div>2023-09-04</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/29/cd/58/06a8ce36.jpg" width="30px"><span>Jackson</span> 👍（0） 💬（0）<div>这里如果用持久化内存的话读写性能如何？redis6.0在多线程和这个优劣是啥</div>2022-08-09</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/WxLKJlXCibwqO92vB8XTicLQiahrhuUEqP7yT9dearZxLzbia7oMdsLmon5J4LJyTfIWchHY3bKfibm1lS1aZarZs4Q/132" width="30px"><span>jie</span> 👍（0） 💬（0）<div>mysql上ssd 比rocksdb 上 ssd 收益更大吧 毕竟一个随机写,一个顺序写.</div>2022-06-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/74/aa/178a6797.jpg" width="30px"><span>阿昕</span> 👍（0） 💬（0）<div>好处：便宜，成本低；不足：速度慢；</div>2022-04-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/b2/e0/d856f5a4.jpg" width="30px"><span>余松</span> 👍（0） 💬（0）<div>由于是文件连续读写，Pika最大的问题并不是数据写入的时候吧。而是读取key的时候要去RocketsDB的SSTable里面挨个读文件。文章没有提及。相比之下，写入的性能降低和读取的性能降低比较不值一提啊。</div>2021-09-07</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/8oQ7n5tkeHs3FMzhpMqB7Q3WJspzicGG9GpQ0LzC4VZ3Bsht1LOWicHoYDiafZW6ibfgNibLx2ZicYbbzt9icaVroNvYg/132" width="30px"><span>Geek_blmxvc</span> 👍（0） 💬（0）<div>这让我想起来前几年的混合硬盘，机械+NAND</div>2021-03-22</li><br/><li><img src="" width="30px"><span>Geek_5b378d</span> 👍（0） 💬（3）<div>有一点不理解:RDB 文件生成时的 fork 时长就会增加
不是用另外一个进程去生成 RDB 文件嘛,咋会阻塞 redis 实例呢</div>2021-03-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/2a/6e/fb980b6b.jpg" width="30px"><span>沈寅</span> 👍（0） 💬（1）<div>redis操作都是原子的，pika内部使用多线程，还能保证原子性吗？ </div>2021-02-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/33/74/d9d143fa.jpg" width="30px"><span>silentyears</span> 👍（0） 💬（0）<div>老师，pika这样存储集合类型的方式不太明白，拿Hash来说，field存储在键中，value存储在值中，怎么快速定位呢？难道是hash后计算出来位置m，在键中“数组”位置m上找field，同样在值中“数组”位置m上找value？</div>2021-02-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/be/d4/ff1c1319.jpg" width="30px"><span>金龟</span> 👍（0） 💬（0）<div>刚才说错了，可以用mongodb</div>2021-01-31</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/5f/e5/54325854.jpg" width="30px"><span>范闲</span> 👍（0） 💬（0）<div>Pika就是支持多种数据结构的分布式kv。
数据访问的性能一定会下降:
memtable有大小限制，如果不在这里一定是从磁盘读，一定比从内存读慢。</div>2020-12-03</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/c4/f3/92f654f1.jpg" width="30px"><span>Bug? Feature!</span> 👍（0） 💬（0）<div>如果钱多，优先选择SSD，哈哈</div>2020-10-25</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/ff/51/9d5cfadd.jpg" width="30px"><span>好运来</span> 👍（0） 💬（0）<div>如果能够识别高频热数据和低频冷数据，对于低频冷数据放在机械硬盘存储都是可以的</div>2020-10-23</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTITcwicqBDYzXtLibUtian172tPs7rJpqG1Vab4oGjnguA9ziaYjDCILSGaS6qRiakvRdUEhdmSG0BGPKw/132" width="30px"><span>大饶Raysir</span> 👍（0） 💬（0）<div>使用机械硬盘最大的好处就是成本更低、存储容量更大，缺点就是访问极慢，适合对访问速度要求很不敏感的场景</div>2020-10-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/20/99/5e/33481a74.jpg" width="30px"><span>Lemon</span> 👍（0） 💬（0）<div>同容量下，机械硬盘对比固态硬盘
优点：
1、价格便宜
2、使用寿命长
缺点：
速度慢，使用缓存（redis ）是为了加速数据的访问速度，本身pika数据操作不在内存中直接执行，需要使用其他存储介质。使用机械硬盘怕是会使用户体验打骨折……</div>2020-10-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/92/d5/699384a0.jpg" width="30px"><span>yeek</span> 👍（0） 💬（0）<div>感觉pika在给redis不足的地方提供了补充：

比如使用binlog机制进行增量同步，避免内存中进行rdb同步，直接先使用磁盘的rdb恢复，再使用binlog增量，再使用内存增量缓冲区追上最后的一点，最终实时同步</div>2020-10-21</li><br/>
</ul>