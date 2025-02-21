你好，我是陈东。

B+树作为检索引擎中的核心技术得到了广泛的使用，尤其是在关系型数据库中。

但是，在关系型数据库之外，还有许多常见的大数据应用场景，比如，日志系统、监控系统。这些应用场景有一个共同的特点，那就是数据会持续地大量生成，而且相比于检索操作，它们的写入操作会非常频繁。另外，即使是检索操作，往往也不是全范围的随机检索，更多的是针对近期数据的检索。

那对于这些应用场景来说，使用关系型数据库中的B+树是否合适呢？

我们知道，B+树的数据都存储在叶子节点中，而叶子节点一般都存储在磁盘中。因此，每次插入的新数据都需要随机写入磁盘，而随机写入的性能非常慢。如果是一个日志系统，每秒钟要写入上千条甚至上万条数据，这样的磁盘操作代价会使得系统性能急剧下降，甚至无法使用。

那么，针对这种频繁写入的场景，是否有更合适的存储结构和检索技术呢？今天，我们就来聊一聊另一种常见的设计思路和检索技术：**LSM树**（Log Structured Merge Trees）。LSM树也是近年来许多火热的NoSQL数据库中使用的检索技术。

## 如何利用批量写入代替多次随机写入？

刚才我们提到B+树随机写入慢的问题，对于这个问题，我们现在来思考一下优化想法。操作系统对磁盘的读写是以块为单位的，我们能否以块为单位写入，而不是每次插入一个数据都要随机写入磁盘呢？这样是不是就可以大幅度减少写入操作了呢？
<div><strong>精选留言（30）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/10/83/14/099742ae.jpg" width="30px"><span>xzy</span> 👍（25） 💬（2）<div>请问，如果wal所在的盘和数据在同一个盘，那怎么保证wal落盘是顺序写呢，我理解也得寻道寻址</div>2020-04-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/40/1e/910aef6a.jpg" width="30px"><span>兰柯一梦</span> 👍（22） 💬（1）<div>感觉取决于系统需要提供什么样的功能，如果系统需要提供高效的查询不需要范围scan那么C0用hashmap都可以，如果需要scan那么平衡树或者skiplist比较合适。leveldb是使用skiplist来实现的，这里的checkpoint主要目的是定期将数据落盘后用来对log文件进行清理的，使得系统重启时不需要重放过多的log影响性能</div>2020-04-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/0f/70/cdef7a3d.jpg" width="30px"><span>Joe Black</span> 👍（12） 💬（1）<div>请问WAL文件有什么特殊之处吗？还是说就是一个以append only方式打开的文件？写入日志后，是否每次都要同步到磁盘呢？如果不同步，那可能只在操作系统页面缓存吧？一断电不就也没了？另外老师说可以提前给日志文件分配空间，这个是具体怎么分配呢？seek过去写一下再seek回去吗？</div>2020-05-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/45/8f/a56b2214.jpg" width="30px"><span>innocent</span> 👍（10） 💬（2）<div>为了性能内存中的树至少有两棵吧</div>2020-04-11</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTIvMlvSXsYgJibgutQdyFT6LsrXuvbjWVh0UpcF4esLzlWzBRlsFHA9MyBY38ibngKAN8mDn6DdHnMQ/132" width="30px"><span>taotaowang</span> 👍（9） 💬（1）<div>有个疑问想请教老师 Lsm树读写性能都优于B+树，那关系型数据库为什么不采取这种数据结构存储呢？</div>2020-04-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/17/df/e5/65e37812.jpg" width="30px"><span>快跑</span> 👍（8） 💬（1）<div>随着越来越理解B+树和LSM树，
B+树是写入的时候就找好key的位置，读取的时候直接根据索引查找key的值
LSM是写入是可能一个key存在不同层的树上，读取的时候，需要合并key不同树上的值。
相当于B+树是写入时merge，LSM是读取时候merge</div>2021-02-25</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/83/14/099742ae.jpg" width="30px"><span>xzy</span> 👍（8） 💬（1）<div>你好，这里还有个问题：如果是ssd，顺序写和随机写的差异不大，那么是否还有必要写wal， 毕竟写wal相当于double写了数据，那直接就写数据是否性能还会更好呢</div>2020-04-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/57/4f/6fb51ff1.jpg" width="30px"><span>奕</span> 👍（7） 💬（2）<div>当内存的C0 树满时， 都要 把磁盘的 C1 树的全部数据 加载到内存中合并生成新树吗？ 我感觉这样性能不高啊。

还有就是 类型日志系统，都是天然按照时间排序；这样的话 ，就可以直接把 C0 树的叶子节点直接放到 C1 树的叶子节点后面啊，没有必要在进行合并生成新树了</div>2020-04-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/57/4f/6fb51ff1.jpg" width="30px"><span>奕</span> 👍（6） 💬（1）<div>填充块写满了，我们就要将填充块作为新的叶节点集合顺序写入磁盘，

这个时候 填充快写的磁盘位置会是之前C1 叶子节点 清空块的位置吗？ 还是另外开辟有个新的空间，当新的树生成后，在把旧的C1树 磁盘数据空间在标记为删除？</div>2020-04-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/1d/13/31ea1b0b.jpg" width="30px"><span>峰</span> 👍（4） 💬（1）<div>考虑的点
1 随机和顺序存取差距不大
2 什么样的有序结构适合高并发的写入
对于2，必须插入的时候只影响局部，这样上锁这样开销就只在局部细粒度上，如果是树可能存在需要调整树高的各种旋转或者分裂合并操作。对于1，在说不用像b树那样降低树高，底层数据节点搞比较大的块，可以充分利用指针这种随机读取的力量，当然块太小有内存碎片之类的问题，以及jvm老年代跨代引用新生代之类问题，所以hbase中跳表的实现是基于chunk的。
感觉自己好像逻辑不是很通，自己还想的不够透彻，其实也在思考全内存的数据库和基于b树这样的数据库在它的缓存可以容纳全部块，不用换入换出，这两种情况下全内存数据库的优势在哪里。</div>2020-04-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/52/40/e57a736e.jpg" width="30px"><span>pedro</span> 👍（3） 💬（1）<div>不知道为什么我昨天发布成功的评论没有被通过，可能 bug了，那我重说一次😭。

问题，前面的文章提到 B 树是为了解决磁盘 io 的问题而引入的，所以 B 树自然不适合做内存索引，适合的是红黑球和跳表。

当然也有例外，如小而美的 Bitcask 就选择了哈希表作为内存索引，是学习 Log-structure 的最佳入门数据库。</div>2020-04-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1f/0b/c8/15f055d3.jpg" width="30px"><span>图灵机</span> 👍（2） 💬（1）<div>每天回家最享受的时间就是看这个课程，越看越爽</div>2020-07-01</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/33/54/595be268.jpg" width="30px"><span>fengyi</span> 👍（1） 💬（3）<div>想请问一下。C0 和 C1 里面有包含所有的数据吗？如果搜寻一个比较老旧的数据。会需要建立一个新的C0吗？</div>2020-05-05</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/1d/de/62bfa83f.jpg" width="30px"><span>aoe</span> 👍（1） 💬（1）<div>评论很精彩，又学到了很多</div>2020-04-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/64/86/f5a9403a.jpg" width="30px"><span>yang</span> 👍（1） 💬（2）<div>老师我问个面试题啊：

现在爬了100亿条URL ，每条url 64字节，我该怎么存在？

然后问如何快速检索某条url在不在其中？

每条64B，100亿条就是640G，这个好大。
想了一下编号，实在太大了，100亿条。
可以打标签吗？
或者针对域名的开始的字母按顺序建立B+树的索引？ 
完整数据按块存储在叶子结点上？ 这样可以加快查询吧</div>2020-04-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/8f/cf/890f82d6.jpg" width="30px"><span>那时刻</span> 👍（1） 💬（1）<div>请问两个关于检查点check point的问题。
1.检查点也是要落盘，和WAL一样的位置么？
2.在数据删除和同步到硬盘之后会生成检查点，还有其它情况会生成检查点么？</div>2020-04-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/54/9a/76c0af70.jpg" width="30px"><span>每天晒白牙</span> 👍（1） 💬（2）<div>思考题
对于c0树因为是存放在内存中的，可以用平衡二叉树或跳表来代替 B+ 树</div>2020-04-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/2a/c5/af/174261ab.jpg" width="30px"><span>armatrix</span> 👍（0） 💬（1）<div>c0树和c1树flag的使用，同样也可以应用在一些业务上状态在cache和持久化存储之间吧？</div>2021-10-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/9d/f9/b98d9c40.jpg" width="30px"><span>森林木</span> 👍（0） 💬（1）<div>老师，问一下如果在归并的过程中又有写入该怎么处理?</div>2021-05-14</li><br/><li><img src="" width="30px"><span>entropy</span> 👍（0） 💬（1）<div>为什么C0小而C1大呢，如果C0和C1一样大，每次内存到达阈值（这时候应该是多个块大小吧），直接刷到硬盘呢？</div>2021-04-02</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/51/7b/191a2112.jpg" width="30px"><span>愤怒的虾干</span> 👍（0） 💬（1）<div>您好，当与内存中的最新数据合并完成后写入磁盘，此时写入的也只是b+树的数据节点（叶子节点），其索引节点创建过程是什么样的？（我的理解是这样合并的b+树类似满二叉树，可以自底向上快速建立索引，不知道对不对？）</div>2021-02-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/cd/db/7467ad23.jpg" width="30px"><span>Bachue Zhou</span> 👍（0） 💬（1）<div>感觉 LSM Tree 还存在一个问题，对于范围查询的场景，c0 无论查到多少数据，都依然需要再查一次 c1，然后合并结果，这样 c0 相当于无法起到优化的效果。</div>2020-12-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/cd/db/7467ad23.jpg" width="30px"><span>Bachue Zhou</span> 👍（0） 💬（2）<div>这是我见过对 LSM Tree 最清晰的教程了，以前就一直没搞懂为何放着这么好的 B+ Tree 不用要用一个分层的数据结构，现在才知道他只是 B+ Tree 的加强版本，更好的利用内存充当磁盘缓冲区的做法而已，它也并没有必要是 NoSQL only 的，一样可以给传统 SQL 数据库服务。但我依然有一件事不明白，请老师指点，“数据采取类似日志追加写的方式写入磁盘，以顺序写的方式提高写入效率。”一般来说，一条日志尺寸并不会太大，至少不可能一个盘块这么大，而且一旦用户发起操作，数据库必须等待日志写入磁盘才能告知用户操作成功，日志永远不可能延迟写入，因此，如果每次操作都必须高频率地向磁盘的同一个盘块追加日志，由于磁盘写入必须是以块为单位，存在写放大，即使是SSD都不能幸免，那么写日志和写整个盘块没有区别，因此这个盘块就相当于被高频的反复重写，这样的操作为什么会被认为高效呢？</div>2020-12-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/e5/5d/b6378027.jpg" width="30px"><span>小山猫</span> 👍（0） 💬（2）<div>请问老师，有没有好的开源实现呢？ 现在有一些业务数据就是树形的，存储检索都是通过mysql做的。一直考虑找一种更好的方案。</div>2020-11-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1b/96/47/93838ff7.jpg" width="30px"><span>青鸟飞鱼</span> 👍（0） 💬（1）<div>老师，你好，有个疑问，为什么从c0查不到数据，从c1查到的数据，要删除标记呢？是因为c1已经存在了，合并时不需要再合并了，是这么理解吗？</div>2020-09-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1b/96/47/93838ff7.jpg" width="30px"><span>青鸟飞鱼</span> 👍（0） 💬（1）<div>老师，你好，每次刷都有新的收获和问题。在c0和c1合并后，c0树就没有数据，最新的数据就查不到，是这么理解的吗？</div>2020-06-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1b/96/47/93838ff7.jpg" width="30px"><span>青鸟飞鱼</span> 👍（0） 💬（1）<div>老师你好，之前看到一种树，类似于B+树，所有的数据不是有序的，但是每页的数据的有序的，这样子可以提高写的效率，降低读效率，不知道这种树应用于NoSQL吗？</div>2020-06-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1c/af/6e/30fb83f1.jpg" width="30px"><span>xaviers</span> 👍（0） 💬（1）<div>东哥晚上好，请问下“工业界具体怎么实现一个高性能的lsm树”这一节在哪啊，没找到。是还没出吗？</div>2020-04-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/fa/f7/91ac44c5.jpg" width="30px"><span>Mq</span> 👍（0） 💬（3）<div>B+树数据存储是以块为单位的，读到内存也是以块为单位，一个块里面如果数据多了顺序查找也不是太快。
内存存储我觉得应该选择跳表，他的查找、插入、删除都跟树一样，只是空间上会多一些消耗，他对范围查找的支持是其他内存数据结构一大优势。
另外，我感觉文章中有把c0写成c1的地方，不知道我理解对不‘和普通的 B+ 树相比，C1 树有一个特点’
</div>2020-04-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/57/4f/6fb51ff1.jpg" width="30px"><span>奕</span> 👍（2） 💬（0）<div>对于 对数据敏感的数据库，基本上都会采用 WAL 技术，来防止数据在内存中丢失， 比如 MySQL 的 redo log </div>2020-04-10</li><br/>
</ul>