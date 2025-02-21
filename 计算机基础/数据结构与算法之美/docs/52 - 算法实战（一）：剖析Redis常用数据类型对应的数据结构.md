到此为止，专栏前三部分我们全部讲完了。从今天开始，我们就正式进入实战篇的部分。这部分我主要通过一些开源项目、经典系统，真枪实弹地教你，如何将数据结构和算法应用到项目中。所以这部分的内容，更多的是知识点的回顾，相对于基础篇、高级篇的内容，其实这部分会更加容易看懂。

不过，我希望你不要只是看懂就完了。你要多举一反三地思考，自己接触过的开源项目、基础框架、中间件中，都用过哪些数据结构和算法。你也可以想一想，在自己做的项目中，有哪些可以用学过的数据结构和算法进一步优化。这样的学习效果才会更好。

好了，今天我就带你一块儿看下，**经典数据库Redis中的常用数据类型，底层都是用哪种数据结构实现的？**

## Redis数据库介绍

Redis是一种键值（Key-Value）数据库。相对于关系型数据库（比如MySQL），Redis也被叫作**非关系型数据库**。

像MySQL这样的关系型数据库，表的结构比较复杂，会包含很多字段，可以通过SQL语句，来实现非常复杂的查询需求。而Redis中只包含“键”和“值”两部分，只能通过“键”来查询“值”。正是因为这样简单的存储结构，也让Redis的读写效率非常高。

除此之外，Redis主要是作为内存数据库来使用，也就是说，数据是存储在内存中的。尽管它经常被用作内存数据库，但是，它也支持将数据存储在硬盘中。这一点，我们后面会介绍。
<div><strong>精选留言（30）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/14/37/8e/cf0b4575.jpg" width="30px"><span>郑晨Cc</span> 👍（114） 💬（14）<div>老师 关于redis的压缩列表有个地方不太明白
虽然压缩列表看起来想数组 但他能像数组一样支持按照下标进行直接随机访问吗？比如我要访问下标为n的数据我启不是需要知道之前从0到n-1的所有数据的长度才能找到n，那这跟链表的时间复杂读没啥区别啊，而且还占用了连续的内存空间？ 还是说压缩列表中的每个元素的长度都记录在它的头部可以一次性的获取？</div>2019-01-25</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/53/e3/39dcfb11.jpg" width="30px"><span>来碗绿豆汤</span> 👍（39） 💬（2）<div>压缩列表每个元素所占用的空间大小是不一定的，所以当想要随机访问某个元素的时候还是要像列表那样从头开始遍历，所以不能太大。理解对吗？</div>2019-04-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/f7/9d/c7295d17.jpg" width="30px"><span>青铜5 周群力</span> 👍（39） 💬（7）<div>我猜压缩列表的好处是能利用l2缓存?</div>2019-02-06</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/63/14/06eff9a4.jpg" width="30px"><span>Jerry银银</span> 👍（15） 💬（3）<div>发现一个功能：左滑进入上一篇，右滑进入下一篇</div>2019-01-25</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/cd/1e/692c3313.jpg" width="30px"><span>复兴</span> 👍（10） 💬（2）<div>值是字符串类型，老师一笔带过了，其实我想知道的是，值为字符串的键值对，是不是通过hash实现的，将键转换成index存储在hash表中。</div>2019-09-30</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/9b/35/79e42357.jpg" width="30px"><span>铁匠</span> 👍（7） 💬（4）<div>跳表和B+数既然大部分场景下可以互换，为什么redis没有使用B+树而选择跳表？</div>2019-08-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/06/52/3ad97645.jpg" width="30px"><span>Twogou27</span> 👍（7） 💬（3）<div>老师，Redis字典数据类型中散列表的装载因子最大不就是1么，大于1是什么情况？</div>2019-02-26</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTKYfReHXMbPaxO890ib9GvY9iciclPIUvaAYMYON4scP7ElXCPVzicghF0SH5HN2LqibYOrdrppC7DuSpw/132" width="30px"><span>static</span> 👍（4） 💬（4）<div>想问老师一个困扰我很久的redis问题。

redis中字典（hash）在数据量少时会采用ziplist数据结构，由于数据量少，并且可以利用CPU缓存，即不失查询速度的情况下又能大幅减少内存占用。但是同为散列表的集合（set）为什么没有采用同样的策略，在数据量少时使用ziplist？而是使用了intset这种有序整数数组？

感谢老师回答！</div>2019-09-16</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/07/8c/0d886dcc.jpg" width="30px"><span>蚂蚁内推+v</span> 👍（3） 💬（3）<div>王老师两种数据结构持久化：
redius用“清除格式，持久化数据再组织数据结构” 这么看来是很消耗性能，为什么不用“保留数据结构”的方式。我理解后者只牺牲部分空间换取了更多性能 。
麻烦王老师解释下？</div>2019-01-25</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/7b/9e/37d69ff0.jpg" width="30px"><span>balancer</span> 👍（2） 💬（1）<div>老师说的压缩列表，是整个数据 hash 或者set 实现是 压缩列表实现的，还是指 hash 或list 里面的具体一个元素是压缩列表实现的？ 压缩列表的结构不太清楚</div>2019-04-16</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/67/8a/babd74dc.jpg" width="30px"><span>锦</span> 👍（1） 💬（3）<div>常常听人说可以使用Redis作为消息队列，这是为什么呢？</div>2019-06-13</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTKnoSoric6IJjI9icQdhaL3IKRwbeic4IoLYAFricOzm0LnGbALtY6VQCYZ1AOiaux2foHok3OpRY94oxw/132" width="30px"><span>红红股海</span> 👍（1） 💬（1）<div>&quot;字典中保存的键和值的大小都要小于 64 字节&quot;
老师，请问这句话的意思是 size(键+值)&lt;64   还是 size(键) &lt;64  &amp;&amp; size(值)&lt;64</div>2019-03-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/1c/2e/93812642.jpg" width="30px"><span>Amark</span> 👍（0） 💬（1）<div>请教一个问题，redis hash 能存储多级字典吗?，比如:{‘a’: {&#39;b&#39;: {&#39;c&#39;: 9}}}</div>2019-09-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/d0/d7/a09ef784.jpg" width="30px"><span>Tattoo</span> 👍（0） 💬（1）<div>压缩列表是不是用变长数组实现的呐？
char  str[0[]</div>2019-02-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/e9/0b/1171ac71.jpg" width="30px"><span>WL</span> 👍（0） 💬（1）<div>想问老师两个问题: 
1.在列表的双向链表数据结构中, 使用额外的list来存储首位节点和长度等信息后使用起来就会方便呢?
2.redis的持久化策略中, 清除原有的存储结构只将数据存在磁盘中, 那这些数据具体在磁盘中是怎么存储的? 是采用压缩列表的方式吗?</div>2019-01-25</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/65/d0/b5b00bc2.jpg" width="30px"><span>在路上</span> 👍（157） 💬（4）<div>思考题1：redis的数据结构由多种数据结构来实现，主要是出于时间和空间的考虑，当数据量小的时候通过数组下标访问最快、占用内存最小，而压缩列表只是数组的升级版；
因为数组需要占用连续的内存空间，所以当数据量大的时候，就需要使用链表了，同时为了保证速度又需要和数组结合，也就有了散列表。
对于数据的大小和多少采用哪种数据结构，相信redis团队一定是根据大多数的开发场景而定的。

思考题2：二叉查找树的存储，我倾向于存储方式一，通过填充叶子节点形成完全二叉树，然后以数组的形式存储到硬盘，数据还原过程也是非常高效的。如果用存储方式二就比较复杂了。</div>2019-01-25</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/62/2f/6fe8ee9e.jpg" width="30px"><span>李靖峰</span> 👍（51） 💬（2）<div>数据量小时采用连续内存的数据结构是为了CPU缓存读取连续内存来提高命中率，而限制数据数量和数据大小应该是考虑到CPU缓存的大小</div>2019-02-02</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/fd/fd/326be9bb.jpg" width="30px"><span>注定非凡</span> 👍（28） 💬（0）<div>Redis 数据库介绍
	 Redis 中，键的数据类型是字符串，但是值的数据类型有很多，常用的数据类型是：字符串、列表、字典、集合、有序集合

列表（list）
1，列表这种数据类型支持存储一组数据
2，两种实现方法：（1）压缩列表（ziplist）（2）双向循环链表
	* 当列表中存储的数据量比较小时，可以采用压缩列表的方式实现。
	* 具体需要同时满足下面两个条件：
（1）列表中保存的单个数据（可能是字符串类型的）小于 64 字节；
（2）列表中数据个数少于 512 个

3，关于压缩列表
	* 它并不是基础数据结构，而是 Redis 自己设计的一种数据存储结构
	* 类似数组，通过一片连续的内存空间来存储数据
	* 跟数组不同的是它允许存储的数据大小不同

4，压缩列表中的“压缩”如何理解？
	* “压缩”：就是节省内存，之所以说节省内存，是相较于数组的存储思路而言的。数组要求每个元素的大小相同，如果要存储不同长度的字符串，就需要用最大长度的字符串大小作为元素的大小。但压缩数组允许不同的存储空间。

	* 压缩列表这种存储结构，另一方面可以支持不同类型数据的存储
	* 数据存储在一片连续的内存空间，通过键来获取值为列表类型的数据，读取的效率也非常高。

5，不能同时满足压缩列表的两个条件时，列表就要通过双向循环链表来实现

字典（hash）
1，字典类型用来存储一组数据对。
2，每个数据对又包含键值两部分，也有两种实现方式：（1）压缩列表（2）散列表
3，同样，只有当存储的数据量比较小的情况下，Redis 才使用压缩列表来实现字典类型。具体需要满足两个条件：

（1）字典中保存的键和值的大小都要小于 64 字节
（2）字典中键值对的个数要小于 512 个

4，当不能同时满足上面两个条件的时候，Redis 就使用散列表来实现字典类型
	* Redis 使用MurmurHash2这种运行速度快、随机性好的哈希算法作为哈希函数
	* 对于哈希冲突问题，Redis 使用链表法来解决
	* 除此之外，Redis 还支持散列表的动态扩容、缩容。

当数据动态增加，装载因子会不停地变大。为了避免散列表性能的下降，当装载因子大于 1 的时候，Redis 会触发扩容，将散列表扩大为原来大小的 2 倍左右（具体值需要计算才能得到）。

当数据动态减少之后，为了节省内存，当装载因子小于 0.1 的时候，Redis 就会触发缩容，缩小为字典中数据个数的大约 2 倍大小（这个值也是计算得到的）

扩容缩容要做大量的数据搬移和哈希值的重新计算，比较耗时。针对这个问题，Redis 使用渐进式扩容缩容策略：将数据的搬移分批进行，避免了大量数据一次性搬移导致的服务停顿。

集合（set）
1，集合这种数据类型用来存储一组不重复的数据
2，这种数据类型也有两种实现方法：（1）有序数组（2）散列表
3，Redis 若采用有序数组，要同时满足下面这样两个条件：

（1）存储的数据都是整数；
（2）存储的数据元素个数不超过 512 个。
当不能同时满足这两个条件的时候，Redis 就使用散列表来存储集合中的数据。
有序集合（sortedset）
1，它用来存储一组数据，并且每个数据会附带一个得分。通过得分的大小，将数据组织成跳表这样的数据结构，以支持快速地按照得分值、得分区间获取数据。
2，当数据量比较小的时候，Redis 可用压缩列表来实现有序集合。使用的前提有两个：

（1）所有数据的大小都要小于 64 字节；
（2）元素个数要小于 128 个
数据结构持久化
1，尽管 Redis 经常会被用作内存数据库，但它也支持将内存中的数据存储到硬盘中。当机器断电的时，存储在 Redis 中的数据不会丢失

Redis 的数据格式由“键”和“值”两部分组成。而“值”又支持很多数据类型，像字典、集合等类型，底层用到了散列表，散列表中有指针的概念，而指针指向的是内存中的存储地址。

Redis 是如何将一个跟具体内存地址有关的数据结构存储到磁盘中的？
1，Redis 遇到的这个问题被称为数据结构的持久化问题，或者对象的持久化问题
2，将数据结构持久化到硬盘主要有两种解决思路：
	* 第一种是清除原有的存储结构，只将数据存储到磁盘中。
		（1）当需要从磁盘还原数据到内存时，再重新将数据组织成原来的数据结构。Redis 采用的就是这种持久化思路。
		（2） 这种方式有一定的弊端：数据从硬盘还原到内存的过程，会耗用比较多的时间
		
	* 第二种方式是保留原来的存储格式，将数据按照原有的格式存储在磁盘中</div>2020-02-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/8b/ad/6325c4c4.jpg" width="30px"><span>田伟 คิดถึง</span> 👍（15） 💬（0）<div>看完前边的课程，当知识点连成线和面之后，才发现原来是这么回事，再来看redis确认是豁然开朗。知识成体系之后记忆会更深刻，不过也带来了更多的思考和发现-----知识边界扩大了</div>2019-01-25</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/d6/f3/601f5f29.jpg" width="30px"><span>目</span> 👍（10） 💬（0）<div>问题1:            压缩列表优点：访问存取快速，节省内存。但是受到操作系统空闲内存限制。越大的连续内存空间越不容易申请到。所以用了其他数据结构比如链表替代。</div>2019-01-26</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/Ryl35QN5UMAtDW4akGRyMzXEOzjXzTaXD9Tvf0M8mEvf7Kds5u8b9RvFul8oItBib8icrhyOy1xWXVDqDbicWu3nQ/132" width="30px"><span>Geek_d142f6</span> 👍（5） 💬（1）<div>程序员这行越干越焦虑，看到好多岗位都有年龄限制，好焦虑。
争哥，可以给点建议吗？</div>2020-03-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/a5/98/a65ff31a.jpg" width="30px"><span>djfhchdh</span> 👍（5） 💬（3）<div>思考题2：对二叉搜索树进行前序遍历，得到的结果以数组的形式存储到磁盘，还原的过程就是顺序遍历数组，构建二叉搜索树</div>2019-06-01</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/ee/85/59e39469.jpg" width="30px"><span>Xianping</span> 👍（4） 💬（0）<div>比高级篇，没那么烧脑了
</div>2019-01-25</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/38/c8/dfc7a25b.jpg" width="30px"><span>read</span> 👍（3） 💬（0）<div>老师您好，有这样一个场景，A关注了B,这样的操作会同时写两个链表一个是A的关注列表，另一个是B的粉丝列表，比如用redis 的sortset来存储。现在要检查所有不一致的情况(比如，A的关注列表有B，但是B的粉丝列表没有A，或者A的关注列表没有B，但是B的粉丝列表有A)。这种情况有什么好的方法吗?</div>2019-01-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/d4/f3/129d6dfe.jpg" width="30px"><span>李二木</span> 👍（3） 💬（3）<div>有个疑问，比如对于有序集合，这个数据量可能会逐步增加，那么数据量达到阈值时就会切换成跳表吗？是数据全部移动到跳表，然后删除列表吗？</div>2019-01-25</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/c5/a2/4ece341b.jpg" width="30px"><span>Ivan.Qi</span> 👍（2） 💬（0）<div>Redis2 和 Redis5数据结构
https:&#47;&#47;github.com&#47;Ivanqi&#47;RedisDataStructure</div>2020-07-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/61/91/9e30b3fe.jpg" width="30px"><span>package coder.wjx;</span> 👍（2） 💬（0）<div>关于思考题二，我想可以有两种方法。
1）平衡的树的保存
那么说明其高度是接近logn的，也就是接近完全二叉树的状态，那么使用数组就能够高效的保存这棵树，即便有些地方会是空的，但是这是以空间换时间，加上数组对缓存友好，保存读取应该都会很快。
保存的时候，首先查看最大的高度，申请一个足够大的数组。然后，从根节点开始，进行遍历，顺序无所谓。重要的是，我们要确定每个节点在数组中的下标，不过很简单，节点i的两个子节点的下标分别是2i+1和2i+2，画个图便清楚了。
还原的时候，首先获取数组第一个节点，构建节点，放入队列中，再使用类似广度遍历的方式，节点出对，在数组中查找其两个子节点，构建并连接两个子节点，子节点入队，直至队列空，构建就完成了。
保存与还原的时间复杂度与空间复杂度都是Ｏ(n)。
2）非平衡的树的保存
情况复杂一点，但是仍然能够使用下标。
保存的时候，为了方便后面的查找和读取，我们访问节点的顺序，是按下标升序的顺序走的，也就是广度遍历的顺序（加入子节点的时候注意先加左节点后右节点（好像本来就是这样的:-D）），这样一来，就能保存一条升序的列表，因而能够使用二分查找的方法寻找子节点的下标。
还原的时候，构建根节点，入队。进入循环，节点出队，使用二分查找的方法找到其两个子节点，构建连接并入队，直至队列为空。
空间复杂度为Ｏ(n)，时间复杂度，保存的是O(n)。还原时，n个节点的遍历需要O(n)，而遍历单个节点需要查找两次数组，因此是O(logn)，总体就是O(nlogn)。
不知有没有更快的方法，大家可以一起讨论下</div>2019-09-18</li><br/><li><img src="" width="30px"><span>wei</span> 👍（2） 💬（1）<div>老师，如果字典保存的键和值的大小都小于 64 字节，并且键值对的个数小于 512 个，Redis 用压缩列表实现。从 [源码](https:&#47;&#47;github.com&#47;antirez&#47;redis&#47;blob&#47;unstable&#47;src&#47;ziplist.c) （ziplist.c ziplistFind） 来看压缩列表根据键查找值的方式，就是一个个遍历。如果有几百个键值对，这么查找比散列表快吗？</div>2019-01-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/9d/ec/235b74c0.jpg" width="30px"><span>ppyh</span> 👍（1） 💬（0）<div>争哥，前面章节说到的跳跃表的排名问题留下的疑问怎么解决啊？
前两天看jdk和protobuf的序列化，总想不出怎么描述区分他两的优缺点，争哥说的对象持久化的两种解决思路真是太棒了，解决了我的疑问</div>2021-08-18</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/DYAIOgq83ersGSic8ib7OguJv6CJiaXY0s4n9C7Z51sWxTTljklFpq3ZAIWXoFTPV5oLo0GMTkqW5sYJRRnibNqOJQ/132" width="30px"><span>walle斌</span> 👍（1） 💬（0）<div>其实 老师应该讲一下redis的基本数据结构 sds  简单动态字符串的，redis的string使用这个结构，由此引申出，对于int 以及 embstr结构下速度比raw的更快。同时 引申出redis的预分配问题，一般的string 尽量不要append等操作，同时可以再引申出内存碎片率问题，与另外一款经典的内存数据库 memcache的作对比，毕竟后者的数据钙化问题还是蛮严重的一个问题。</div>2020-10-09</li><br/>
</ul>