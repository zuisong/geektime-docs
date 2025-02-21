你好，我是陈东。

LevelDB是由Google开源的存储系统的代表，在工业界中被广泛地使用。它的性能非常突出，官方公布的LevelDB的随机读性能可以达到6万条记录/秒。那这是怎么做到的呢？这就和LevelDB的具体设计和实现有关了。

LevelDB是基于LSM树优化而来的存储系统。都做了哪些优化呢？我们知道，LSM树会将索引分为内存和磁盘两部分，并在内存达到阈值时启动树合并。但是，这里面存在着大量的细节问题。比如说，数据在内存中如何高效检索？数据是如何高效地从内存转移到磁盘的？以及我们如何在磁盘中对数据进行组织管理？还有数据是如何从磁盘中高效地检索出来的？

其实，这些问题也是很有代表性的工业级系统的实现问题。LevelDB针对这些问题，使用了大量的检索技术进行优化设计。今天，我们就一起来看看，LevelDB究竟是怎么优化检索系统，提高效率的。

## 如何利用读写分离设计将内存数据高效存储到磁盘？

首先，对内存中索引的高效检索，我们可以用很多检索技术，如红黑树、跳表等，这些数据结构会比B+树更高效。因此，LevelDB对于LSM树的第一个改进，就是使用跳表代替B+树来实现内存中的C0树。

好，解决了第一个问题。那接下来的问题就是，内存数据要如何高效存储到磁盘。在第7讲中我们说过，我们是将内存中的C0树和磁盘上的C1树归并来存储的。但如果内存中的数据一边被写入修改，一边被写入磁盘，我们在归并的时候就会遇到数据的一致性管理问题。一般来说，这种情况是需要进行“加锁”处理的，但“加锁”处理又会大幅度降低检索效率。
<div><strong>精选留言（30）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/0f/57/4f/6fb51ff1.jpg" width="30px"><span>奕</span> 👍（27） 💬（2）<div>当 MemTable 的存储数据达到上限时，我们直接将它切换为只读的 Immutable MemTable，然后重新生成一个新的 MemTable
------------------
这样的一个机制，内存中会出现多个Immutable MemTable 吗？ 上一个Immutable MemTable 没有及时写入到磁盘</div>2020-05-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/57/4f/6fb51ff1.jpg" width="30px"><span>奕</span> 👍（21） 💬（2）<div>LevelDB 分层的逻辑没有理解
当 Level0 层 有四个 SSTable 的时候，这时候把这个四个进行归并，然后放到 Level1 层，这时候 Level0 层清空，这个有个问题是 当进行归并后 后生成几个 SSTable ,这里是有什么规则吗？

接下来，然后 Level0 层在满了之后，是Level0 层的每个 SSTable 分别与 Level1 所有的 SSTable 进行多路归并吗？

再然后 Level1 层满了之后，是按照顺序取 Level1 层的一个 SSTable 与 Level2所有的 SSTable 进行多路归并吗？

这样会有大量的 磁盘 IO,老师说利用判断重合度进行解决的？ 这个重合度是怎么计算计算判断的呢？

==============================
老师的文中的这句话没有看明白：
在多路归并生成第 n 层的 SSTable 文件时，LevelDB 会判断生成的 SSTable 和第 n+1 层的重合覆盖度，如果重合覆盖度超过了 10 个文件，就结束这个 SSTable 的生成，继续生成下一个 SSTable 文件
</div>2020-05-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/00/4e/be2b206b.jpg" width="30px"><span>吴小智</span> 👍（19） 💬（3）<div>之前看过基于 lsm 的存储系统的代码，能很好理解这篇文章。不过，还是不太理解基于 B+ 树与基于 lsm 的存储系统，两者的优缺点和使用场景有何不同，老师有时间可以解答一下。</div>2020-05-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/4f/3f/6f62f982.jpg" width="30px"><span>wangkx</span> 👍（9） 💬（1）<div>1. 既然要查找的数据在某一层查到了，按照LevelDB的分层管理的设计，即使下一层数据也存在，数据也是一样的，没有必要再去查找下一层的数据了。

2. “在多路归并生成第 n 层的 SSTable 文件时，LevelDB 会判断生成的 SSTable 和第 n+1 层的重合覆盖度，如果重合覆盖度超过了 10 个文件，就结束这个 SSTable 的生成，继续生成下一个 SSTable 文件。”———如果通过控制sstable文件数量来限制每层容量的话，有可能每个sstable会比较小，很快就达到数量限制，可能分层作用就不明显了。</div>2020-05-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/f7/5b/d2e7c2c4.jpg" width="30px"><span>时隐时现</span> 👍（7） 💬（2）<div>老师好，有2个问题：
1、内存中的C0树，采用跳表替换掉B+树，检索效率会有提升吗？我一直觉得两者是差不多的吧，什么场景下跳表会比B+树性能高很多？
2、滚动合并应该是后台操作，在合并的过程中，相应的sstable应该是被写锁锁定的吧？此时如果有应用执行读，会不会被阻塞？如果不阻塞，如何保证读写一致性？</div>2020-05-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1c/af/6e/30fb83f1.jpg" width="30px"><span>xaviers</span> 👍（7） 💬（1）<div>老师，不好意思哈，再追问一下😬那为啥用change buffer + WAL优化后的MySQL的写性能还是不如LSM类的存储系统啊？原因是啥啊</div>2020-05-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/57/4f/6fb51ff1.jpg" width="30px"><span>奕</span> 👍（6） 💬（2）<div>在评论下回复老师看不到啊，那就在评论问一下

第一问还有点疑问:level0层的每个sstable可能会有范围重叠，需要把重叠的部分提取到合并列表，这个这个合并列表是什么？还有就是提取之后呢，还是要遍及level0层的每个sstable与level1层的sstable进行归并吗？

还有个问题就是:当某层的sstable向下层转移的时候，碰巧下层的空间也满了，这时候的处理方案是向下层递归吗？一直往下找，然后在向上处理</div>2020-05-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/8f/cf/890f82d6.jpg" width="30px"><span>那时刻</span> 👍（4） 💬（1）<div>有两个问题，请教下老师。
1。在多路归并生成第 n 层的 SSTable 文件时，如何控制当前层最大容量呢？如果超过当前层的容量是停止计算还是把多余的量挪到下一层？
2。数据索引区里meta index block，当存在多个过滤器时，对过滤器进行索引。这是涉及到filter block过滤么？</div>2020-05-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/cd/db/7467ad23.jpg" width="30px"><span>Bachue Zhou</span> 👍（3） 💬（2）<div>这个数据库在海量数据的情况下真的很快吗，我总感觉一般般的样子啊。
1. 层次没有上限 单层文件总容量却有上限，因此极端情况下需要搜索的文件依然很多，虽然每个文件有布隆过滤器预搜索，所以单个文件检索性能还不错，但需要一层层打开文件解析文件然后开始搜索，文件数量如果很多，则性能不佳
2. 如果是范围检索，则注定所有层次都必须被查询，性能不佳
3. 每个文件尺寸有上限，而且很小，意味着文件数量很多，文件打开数就会很多，当达到通常的 65536 的上限时（如果每个文件 2m 大小，那么也就存了 128g，实际上由于进程自身也有文件打开数开销，实际上能提供给 leveldb 的文件打开数配额会远远小于这个值），就只能被迫使用 lru 来关闭一些不常用的小文件了，如果频繁打开解析关闭小文件时，性能不佳
4. 多路归并多个文件的数据，意味着磁盘在多个文件中来回寻道，哪怕只有最多十个文件，性能也不佳
5. 无法理解为何只选一个文件参与和下一层的归并，选一个文件和选两个文件的区别在哪里？
</div>2021-01-06</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/47/00/3202bdf0.jpg" width="30px"><span>piboye</span> 👍（3） 💬（1）<div>如果把sstable换成B+树，也有bloomfilter，是不是可以不用限制文件为2m的大小？</div>2020-09-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/47/00/3202bdf0.jpg" width="30px"><span>piboye</span> 👍（3） 💬（2）<div>为什么要限制sstable为2m，感觉很小啊，如果是个很大的数据集，文件不是会很多？</div>2020-09-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/4e/1b/f4b786b9.jpg" width="30px"><span>飞翔</span> 👍（2） 💬（2）<div>老师 level db 的应用场景是什么呀</div>2020-06-25</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/18/3d/ad/819a731a.jpg" width="30px"><span>Geek_863b69</span> 👍（2） 💬（1）<div>老师，请教下，levelDB中，data block存的是sstable的数据，如果sstable跟上一层数据合并了，那么查找的时候如果直接从缓存找，数据不就不一致了？还是说合并的时候会顺带删除缓存？</div>2020-06-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1c/af/6e/30fb83f1.jpg" width="30px"><span>xaviers</span> 👍（2） 💬（4）<div>老师晚上好，请教个问题哈。

MySQL在写数据的时候，是先写到change buffer内存中的，不会立刻写磁盘的，达到一定量再将change buffer落盘。这个和Memtable的设计理念类似，按理说，速度也不会太慢吧？</div>2020-05-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/8f/cf/890f82d6.jpg" width="30px"><span>那时刻</span> 👍（2） 💬（1）<div>讨论问题1：在某一层找到了key，不需要再去下一层查找的原因是，这一层是最新的数据。即使下一层有的话，是旧数据。这引申出另外一个问题，数据删除的时候是怎么处理的呢？是另外一个删除列表来保存删除的key吗？
问题2：如老师提示的这样，SSTable 的生成过程会受到约束，SSTable在归并的过程中，可能由于数据倾斜，导致某个分区里的数据量比较大，所以没有办法保证每个SSTable的大小。</div>2020-05-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/17/df/e5/65e37812.jpg" width="30px"><span>快跑</span> 👍（1） 💬（2）<div>“LevelDB 会判断生成的 SSTable 和第 n+1 层的重合覆盖度”，
判断第N层的SSTable跟N+1层的覆盖重合度，这块逻辑是怎么实现的，需要将第N层的数据加载到内存每条记录都判断，还是有额外的索引记录着第N层的数据范围？</div>2021-04-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/3a/82/1ff83a38.jpg" width="30px"><span>牛牛</span> 👍（1） 💬（2）<div>老师、我想请教下、levelDB是怎么处理`脏缓存`(eg. 有用户突然访问了别人很久不访问的数据(假设还比较大)、导致本来应该在缓存中的数据被驱逐, Data Block的优化效果就会打折扣)的 ?

------
我是想到了Mysql 处理Buffer Poll的机制(分为Old 和 Young区)、类似的思想在jvm的gc管理中也有用到

</div>2020-05-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/57/4f/6fb51ff1.jpg" width="30px"><span>奕</span> 👍（1） 💬（1）<div>课后思考：
1: 因为 LevelDB 天然的具有缓存的特性，最经常使用的最新的数据离用户最近，所有在上层找到数据就不会在向下找了
2: 如果规定生成文件的个数，那么有可能当前层和下一层的存储大小相近了，起不到分层的作用了</div>2020-05-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/1d/13/31ea1b0b.jpg" width="30px"><span>峰</span> 👍（1） 💬（1）<div>问题1： 因为只是get(key), 所以上层的sstabe的数据是最新的，所以没必要再往下面查，但如果有hbase这样的scan(startkey,endkey) 那还是得全局的多路归并（当然可以通过文件元数据迅速排除掉一些hfile）
问题2：SSTable 的生成过程会受到约束，无法保证每一个 SSTable 文件的大小。哈哈哈，我在抄答案，我其实有疑问，就算限定文件数量，那么在层次合并的时候，假设我是先合成一个整个sstable再切，面临的对这一整个sstable怎么切成文件的问题，那就顺序的2m一个算会不会文件数量超标，决定是否要滚动下一层，不过我这样想法过于理想显然假设那块就不成立，应该是多路归并式的动态生成，否则对内存压力太大，但是如果按整个层的文件大小分，就不用考虑文件量的问题，只要key连续性大点，文件大小不超过2m就生成就好了。</div>2020-05-08</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTKJrOl63enWXCRxN0SoucliclBme0qrRb19ATrWIOIvibKIz8UAuVgicBMibIVUznerHnjotI4dm6ibODA/132" width="30px"><span>Helios</span> 👍（0） 💬（1）<div>请教老师一个问题:
将内存可读写的table切换为 Immutable MemTable的时候会不会有阻塞操作，类似于gc中的stw，如果发生频繁是不是对性能也有影响。</div>2021-09-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/17/df/e5/65e37812.jpg" width="30px"><span>快跑</span> 👍（0） 💬（1）<div>请教老师，levelDB中实现LSM的C0树是用跳表，这个是通过源码看的么？如果我想了解下其他使用LSM实现的系统，比如doris，druid之类，我怎么判断其他开源系统的C0树是用的什么结构实现？老师可以给个思路嘛</div>2021-03-07</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1b/be/af/93e14e9d.jpg" width="30px"><span>扁舟</span> 👍（0） 💬（1）<div>哈哈，这么多优质评论与老师一个一个问题的细心回答。看评论时，都会思考，我为什么没有进行这样的联想与对比，看来还是思考能力不强，以后看到知识点多想几个为什么。这样的文章真是看到就是赚到</div>2020-06-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1c/af/6e/30fb83f1.jpg" width="30px"><span>xaviers</span> 👍（0） 💬（1）<div>老师辛苦了，经常都是凌晨更新，终于等到这篇文章了😁</div>2020-05-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/4e/29/1be3dd40.jpg" width="30px"><span>ykkk88</span> 👍（0） 💬（2）<div>老师，如果是memtable有删除key的情况下，skiplist是不是设置墓碑标志，刷level 0的时候 sstable也还是有这个删除标记，只有在最下层的sstable合并时候再真的物理删除key啊，感觉不这么做，可能get时候会读出来已经被删除的key</div>2020-05-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/55/a9/5282a560.jpg" width="30px"><span>yic</span> 👍（0） 💬（0）<div>&quot;而从 Level 1 开始，每一层的 SSTable 都做过了处理，这能保证覆盖范围不重合的。因此，对于同一层中的 SSTable，我们可以使用二分查找算法快速定位唯一的一个 SSTable 文件&quot;  -- 老师，关于这个点我有疑问还请帮忙解答：
这句话描述的是一个终态吧？ 我理解一条比较大的数据A（预期应该放在L6层）写入了Level0层后，要到达L6层是需要一定的时间的。

如果我上面的理解没有错误，那么当数据A到达了L3层时，用户过来查询，会是怎样的处理过程呢？</div>2023-09-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/26/eb/d7/90391376.jpg" width="30px"><span>ifelse</span> 👍（0） 💬（0）<div>学习打卡</div>2023-04-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/18/29/7a/3c0fbf9c.jpg" width="30px"><span>berkin</span> 👍（0） 💬（0）<div>老师，这里有一段话不太理解，
“在多路归并生成第 n 层的 SSTable 文件时，LevelDB 会判断生成的 SSTable 和第 n+1 层的重合覆盖度，如果重合覆盖度超过了 10 个文件，就结束这个 SSTable 的生成，继续生成下一个 SSTable 文件。”
意思是说 第 n 层 新生成的 SSTable 与 n+1 层覆盖度超过 10 个文件 就会结束第 n层的 SSTable，意思是第 n 层的 SSTable 在生成的时候一直会和第 n+1 层的文件 key range 进行比较，如果覆盖超过 n+1 层
就会开启另外一个 SSTable 写入n -1 层归并过来的数据吗？</div>2022-03-04</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/99/79/74d4f24f.jpg" width="30px"><span>anker</span> 👍（0） 💬（0）<div>想问一下Compaction过程中需要加锁吗？</div>2021-08-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/de/5d/3a75c20b.jpg" width="30px"><span>Geek_bd6gy9</span> 👍（0） 💬（1）<div>老师，请教一下，“使用LSM树，对于大量的随机读，它无法在内存中命中，因此会去读磁盘，并且是一层一层地多次读磁盘，会带来很严重的读放大效应”，这里的读放大效应如何理解呢？</div>2021-07-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/bf/22/26530e66.jpg" width="30px"><span>趁早</span> 👍（0） 💬（0）<div>你好，不理解为啥写入的时候sst会出现重叠？批量写入一般都是有序的吧，为啥会范围会重叠呢，那重叠之后多个sstable 在归并的时候是怎么判断哪个sst里面的数据是最新的需要被留下的</div>2021-07-09</li><br/>
</ul>