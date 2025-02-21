你好，我是蒋德钧。

一提到Redis，我们的脑子里马上就会出现一个词：“快。”但是你有没有想过，Redis的快，到底是快在哪里呢？实际上，这里有一个重要的表现：它接收到一个键值对操作后，能以**微秒级别**的速度找到数据，并快速完成操作。

数据库这么多，为啥Redis能有这么突出的表现呢？一方面，这是因为它是内存数据库，所有操作都在内存上完成，内存的访问速度本身就很快。另一方面，这要归功于它的数据结构。这是因为，键值对是按一定的数据结构来组织的，操作键值对最终就是对数据结构进行增删改查操作，所以高效的数据结构是Redis快速处理数据的基础。这节课，我就来和你聊聊数据结构。

说到这儿，你肯定会说：“这个我知道，不就是String（字符串）、List（列表）、Hash（哈希）、Set（集合）和Sorted Set（有序集合）吗？”其实，这些只是Redis键值对中值的数据类型，也就是数据的保存形式。而这里，我们说的数据结构，是要去看看它们的底层实现。

简单来说，底层数据结构一共有6种，分别是简单动态字符串、双向链表、压缩列表、哈希表、跳表和整数数组。它们和数据类型的对应关系如下图所示：

![](https://static001.geekbang.org/resource/image/82/01/8219f7yy651e566d47cc9f661b399f01.jpg?wh=4000%2A1188)

可以看到，String类型的底层实现只有一种数据结构，也就是简单动态字符串。而List、Hash、Set和Sorted Set这四种数据类型，都有两种底层实现结构。通常情况下，我们会把这四种类型称为集合类型，它们的特点是**一个键对应了一个集合的数据**。
<div><strong>精选留言（30）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/0f/90/8a/288f9f94.jpg" width="30px"><span>Kaito</span> 👍（578） 💬（47）<div>两方面原因：

1、内存利用率，数组和压缩列表都是非常紧凑的数据结构，它比链表占用的内存要更少。Redis是内存数据库，大量数据存到内存中，此时需要做尽可能的优化，提高内存的利用率。

2、数组对CPU高速缓存支持更友好，所以Redis在设计时，集合数据元素较少情况下，默认采用内存紧凑排列的方式存储，同时利用CPU高速缓存不会降低访问速度。当数据元素超过设定阈值后，避免查询时间复杂度太高，转为哈希和跳表数据结构存储，保证查询效率。</div>2020-08-04</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/d0/69/5dbdc245.jpg" width="30px"><span>张德</span> 👍（110） 💬（9）<div>同问  老师  如果渐进式哈希操作  如果有一个value操作很长时间段都没被查到  那渐进式哈希会持续非常长的时间吗   还是会在空闲的时候  也给挪到扩容的hash表里面</div>2020-08-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/f6/9c/b457a937.jpg" width="30px"><span>不能扮演天使</span> 👍（78） 💬（5）<div>Redis的List底层使用压缩列表本质上是将所有元素紧挨着存储，所以分配的是一块连续的内存空间，虽然数据结构本身没有时间复杂度的优势，但是这样节省空间而且也能避免一些内存碎片；</div>2020-08-03</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/8f/cf/890f82d6.jpg" width="30px"><span>那时刻</span> 👍（65） 💬（5）<div>请问老师关于zset的问题，您在文中提到Sorted Set内部实现数据结构是跳表和压缩列表。但是我从zset代码看到这样的注释
The elements are added to a hash table mapping Redis objects to scores. At the same time the elements are added to a skip list mapping scores to Redis objects 
按照注释应该还有hash table来额外存储数据吧，这样在zset里查找单个元素，可以从O(logN)降低为O(1)。不知道我理解的是否正确？</div>2020-08-06</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1f/26/34/891dd45b.jpg" width="30px"><span>宙斯</span> 👍（33） 💬（1）<div>老师你好，hash表是全局的，这里的全局怎样理解？是‘存放key的数组全局只有一个‘是这样理解吗？</div>2020-12-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/1b/4d/2cc44d9a.jpg" width="30px"><span>刘忽悠</span> 👍（21） 💬（2）<div>redis底层的数据压缩搞的很细致，像sds，根据字节长度划分的很细致，另外采用的c99特性的动态数组，对短字符串进行一次性的内存分配；跳表设计的也很秀，简单明了，进行范围查询很方便；dict的扩容没细看，但是看了一下数据结构，应该是为了避免发生扩容的时候出现整体copy；
个人觉得老师应该把sds，dict等具体数据结构的源码也贴上</div>2020-08-03</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/5f/bf/4bd3eb4b.jpg" width="30px"><span>米 虫</span> 👍（20） 💬（1）<div>要是加餐中来一偏，一个redis指令的执行过程，那大局观就更深刻了。</div>2020-08-04</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/1b/4d/2cc44d9a.jpg" width="30px"><span>刘忽悠</span> 👍（10） 💬（1）<div>至于问题答案，采用压缩列表或者是整数集合，都是数据量比较小的情况，所以一次能够分配到足够大的内存，而压缩列表和整数集合本身的数据结构也是线性的，对cpu的缓存更友好一些，所以真正的执行的时间因为高速缓存的关系，速度更快</div>2020-08-03</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/ce/d7/074920d5.jpg" width="30px"><span>小飞同学</span> 👍（9） 💬（1）<div>小问题:
1.rehash的时候为啥存储位置会发生变化？一个对象的hashCode始终是一样的。  还是说rehash是对槽进行取模 
2.跳表找元素没太看明白，是二分查找么？怎么感觉找33那个元素不止3次
课后一问:
因为数组占用内存连续，不需要随机读取。同时碎片化问题也不需要考虑。

希望得到老师的解答，谢谢</div>2020-08-04</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/12/70/10faf04b.jpg" width="30px"><span>Lywane</span> 👍（7） 💬（1）<div>rehash不仅全局有，单独的值为HASH类型的数据也会有吧</div>2020-08-17</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/DYAIOgq83erPMtAfnQdpx1yOZQ2ic7icqUs3tvibEjUXQMUXKiaakyuIho6k6vmdl46nrdWjXIjPIRg9Pmco00tR5w/132" width="30px"><span>小氘</span> 👍（6） 💬（2）<div>我是没有用过redis的小白，尝试回答课后思考题。
数组这种基本数据结构的两个特点：1 连续的内存空间分布，符合程序的局部性原理，可以利用cpu高速缓存；2 根据数组下标随机访问元素的时间复杂度是O(1)。如果实现上可以利用这两个特点，那还是有它的存在价值。</div>2020-08-03</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/83/af/1cb42cd3.jpg" width="30px"><span>马以</span> 👍（5） 💬（1）<div>有个问题，在渐进式rehash的时候，如果有一个hash桶的位置一直没有被访问到，是不是这个rehash动作就永远完成不了了？那么也就意味着系统永远要保留两份全局hash表？</div>2021-01-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/d6/16/43b4814c.jpg" width="30px"><span>x</span> 👍（5） 💬（2）<div>redis的hash扩容跟golang中的map其实扩容机制竟然都是&quot;渐进式扩容&quot;！</div>2020-08-16</li><br/><li><img src="" width="30px"><span>zhuhaow</span> 👍（3） 💬（1）<div>老师，弱弱的请教下，list 的实现出了 quicklist 还有 ziplist 的吗？
我在 t_list.c 的 pushGenericCommand 方法中，只看到了 createQuicklistObject() 没看到 ziplist 的创建呢</div>2020-11-11</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTJIocn8OMjfSGqyeSJEV3ID2rquLR0S6xo0ibdNYQgzicib6L6VlqWjhgxOqD2iaicX1KhbWXWCsmBTskA/132" width="30px"><span>虚竹</span> 👍（3） 💬（1）<div>老师好，请教下，渐进式rehash过程中，接到客户端写入数据请求，是2个全局哈希表都会写入数据吗？</div>2020-11-01</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/58/45/721545cc.jpg" width="30px"><span>Q</span> 👍（3） 💬（2）<div> hash桶不是已经避免的一定程度上的hash冲突吗？hash冲突链难道是用来解决，hash桶中还有hash碰撞的情况？那假如hash桶冲突了，为啥不在hash桶末尾添加元素，这样操作的复杂度也是O（1）</div>2020-08-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/7a/0a/0ce5c232.jpg" width="30px"><span>吕</span> 👍（2） 💬（2）<div>文中说双向链表和整数数组都记录了元素的总个数，但就我平时接触的双向链表和数组，里面并没有记录元素(数组中实际存在的，不是说初始定义时指定的个数)的总个数，redis是对这两个数据结构做了改进了么？</div>2020-08-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/dd/9b/0bc44a78.jpg" width="30px"><span>yyl</span> 👍（2） 💬（2）<div>老师，您好，以查找33为例的“跳表的快速查找过程”，需要元素有序吧？
看着类似二分查找</div>2020-08-04</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/4b/0a/4bb137d9.jpg" width="30px"><span>hz</span> 👍（1） 💬（2）<div>老师，渐进式rehash的过程会不会出现hash[0]中的某个键一直不被访问到，导致rehash很久不完成。如果此时hash[1]中的负载因子又已经超过5了，会出现什么情况。</div>2020-12-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/97/18/a5218104.jpg" width="30px"><span>🐾</span> 👍（1） 💬（1）<div>读完这篇文章，才发现用了这么多久的Redis，从来都没有真正去关注和学习它的底层东西，醍醐灌顶～
专栏后面还会讲到 bitmap、hyperloglog、streams 这三个值类型的使用吗？不知道实际使用场景是怎么样的
</div>2020-08-06</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/23/46/db5212bc.jpg" width="30px"><span>努力努力再努力</span> 👍（1） 💬（1）<div>老师好，redis中的所有数据结构都是用redisObject存放的吧？</div>2020-08-05</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/22/f2/c3/5345b358.jpg" width="30px"><span>星夜</span> 👍（0） 💬（1）<div>List的底层数据结构，新版本的redis应该只有ziplist一种了吧？</div>2020-11-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/c4/f3/92f654f1.jpg" width="30px"><span>Bug? Feature!</span> 👍（0） 💬（1）<div>给老师点个赞，Redis 数据类型丰富，每个类型的操作繁多，我们通常无法一下子记住所有操作的复杂度。所以，最好的办法就是掌握原理，以不变应万变。一旦掌握了数据结构基本原理，我们就可以从原理上推断不同操作的复杂度，即使这个操作我们不一定熟悉。这样一来，我们不用死记硬背，也能快速合理地做出选择了。</div>2020-11-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/19/63/12/5a22fcc7.jpg" width="30px"><span>第四范式</span> 👍（0） 💬（2）<div>最近在撸redis源码。看了之后。再看老师的博客。和下面的讨论区。真的是受启发很大。感谢老师。</div>2020-08-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/cf/81/96f656ef.jpg" width="30px"><span>杨逸林</span> 👍（0） 💬（1）<div>我以为是 keys 这种，慢操作，原来是针对底层数据结构讲解的“慢”操作。</div>2020-08-03</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/fd/fd/326be9bb.jpg" width="30px"><span>注定非凡</span> 👍（493） 💬（23）<div>一，作者讲了什么？
    1，Redis的底层数据结构

二，作者是怎么把这事给讲明白的？
    1，讲了Redis的数据结构：数据的保存形式与底层数据结构
    2，由数据结构的异同点，引出数据操作的快慢原因
    
三，为了讲明白，作者讲了哪些要点？有哪些亮点？
    1，亮点1：string，list，set，hast,sortset都只是数据的保存形式，底层的数据结构是：简单动态字符串，双向链表，压缩列表，哈希表，跳表，整数数组
    2，亮点2：Redis使用了一个哈希表保存所有的键值对
    3，要点1：五种数据形式的底层实现
            a，string：简单动态字符串
            b，list：双向链表，压缩列表
            c，hash：压缩列表，哈希表
            d，Sorted Set：压缩列表，跳表
            e，set：哈希表，整数数组
    4，要点2：List ,hash，set ,sorted set被统称为集合类型，一个键对应了一个集合的数据
    5，要点3：集合类型的键和值之间的结构组织
            a：Redis使用一个哈希表保存所有键值对，一个哈希表实则是一个数组，数组的每个元素称为哈希桶。
            b：哈希桶中的元素保存的不是值的本身，而是指向具体值的指针
    6，要点4：哈希冲突解决
            a：Redis的hash表是全局的，所以当写入大量的key时，将会带来哈希冲突，已经rehash可能带来的操作阻塞
            b：Redis解决hash冲突的方式，是链式哈希：同一个哈希桶中的多个元素用一个链表来保存
            c：当哈希冲突链过长时，Redis会对hash表进行rehash操作。rehash就是增加现有的hash桶数量，分散entry元素。
    7，要点5：rehash机制
            a：为了使rehash操作更高效，Redis默认使用了两个全局哈希表：哈希表1和哈希表2，起始时hash2没有分配空间
            b：随着数据增多，Redis执行分三步执行rehash;
                1，给hash2分配更大的内存空间，如是hash1的两倍
                2，把hash1中的数据重新映射并拷贝到哈希表2中
                3，释放hash1的空间
    8，要点6：渐进式rehash
            a：由于步骤2重新映射非常耗时，会阻塞redis
            b：讲集中迁移数据，改成每处理一个请求时，就从hash1中的第一个索引位置，顺带将这个索引位置上的所有entries拷贝到hash2中。
    9，要点7 ：压缩列表，跳表的特点
            a：压缩列表类似于一个数组，不同的是:压缩列表在表头有三个字段zlbytes,zltail和zllen分别表示长度，列表尾的偏移量和列表中的entry的个数，压缩列表尾部还有一个zlend，表示列表结束
                所以压缩列表定位第一个和最后一个是O(1),但其他就是O(n)
            b：跳表：是在链表的基础上增加了多级索引，通过索引的几次跳转，实现数据快速定位

四，对于作者所讲，我有哪些发散性思考？

五，在将来的哪些场景中，我能够用到它？

六，评论区收获
    1，数组和压缩列表可以提升内存利用率，因为他们的数据结构紧凑
    2，数组对CPU高速缓存支持友好，当数据元素超过阈值时，会转为hash和跳表，保证查询效率</div>2020-08-25</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/34/b6/0feb574b.jpg" width="30px"><span>我的黄金时代</span> 👍（114） 💬（7）<div>来自互联网 ：因为在进行渐进式 rehash 的过程中， 字典会同时使用 ht[0] 和 ht[1] 两个哈希表， 所以在渐进式 rehash 进行期间， 字典的删除（delete）、查找（find）、更新（update）等操作会在两个哈希表上进行： 比如说， 要在字典里面查找一个键的话， 程序会先在 ht[0] 里面进行查找， 如果没找到的话， 就会继续到 ht[1] 里面进行查找， 诸如此类。
另外， 在渐进式 rehash 执行期间， 新添加到字典的键值对一律会被保存到 ht[1] 里面， 而 ht[0] 则不再进行任何添加操作： 这一措施保证了 ht[0] 包含的键值对数量会只减不增， 并随着 rehash 操作的执行而最终变成空表。</div>2020-08-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/3a/82/1ff83a38.jpg" width="30px"><span>牛牛</span> 👍（14） 💬（11）<div>老师、早安, 
今天的问题 @Kaito 同学回答的很好、尝试回答下: 数组上随机访问是否对cpu缓存友好 ?

数组对cpu缓存友好的原因是: cpu预读取一个cache line大小的数据, 数组数据排列紧凑、相同大小空间保存的元素更多, 访问下一个元素时、恰好已经在cpu缓存了. 如果是随机访问、就不能充分利用cpu缓存了, 拿int元素举例: 一个元素4byte, CacheLine 假设64byte, 可以预读取 16个挨着的元素, 如果下次随机访问的元素不在这16个元素里、就需要重新从内存读取了.


想请教几个问题:

1. rehash是将访问元素所在索引位置上的所有entries都 copy 到 hash表2 ?
   如果有索引位置一直没访问到、它会一直留着 hash表1 中 ？
   如果是, 再次rehash时这部分没被挪走的索引位置怎么处理 ?
   如果不是、那什么时候(时机)触发这部分位置的rehash呢 ?

2. rehash过程中、内存占用会多于原所占内存的2倍 ?
   (ht2的内存是ht1的2倍, 原ht1的空间还未释放)
   我记得redis设计实现上说 ht2的内存会与ht1实际使用的键值对的数量有关, 扩容好像是 &gt;= ht1.used * 2 的第一个 2^n; 缩容好像是 &gt;= ht1.used 的第一个 2^n
   
3. rehash完成之后, hash表1 留作下次rehash备用、但会把占用的内存释放掉, 这么理解对不 ？

4. rehash时 为什么是 `复制`, 而不是 `移动`, 这个是有什么考虑吗 ？
   我的理解: 移动需要释放原空间, 每个元素都单独释放会导致大量的碎片内存、多次释放也比一次释放效率更低. 不知道是不是考虑错了~~~
   </div>2020-08-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/aa/a5/194613c1.jpg" width="30px"><span>dingjiayi</span> 👍（13） 💬（6）<div>老师好，请问 rehash 期间，新的 操作请求（增删改查）到达，redis 是如何处理的？</div>2020-08-05</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/25/7f/473d5a77.jpg" width="30px"><span>曾轼麟</span> 👍（9） 💬（0）<div>intset 和 ziplist 如果直接使用确实是时间复杂度上不是很高效，但是结合Redis的使用场景，大部分Redis的数据都是零散碎片化的，通过这两种数据结构可以提高内存利用率，但是为了防止过度使用这两种数据结构Redis其实都设有阈值或者搭配使用的，例如：ziplist是和quicklist一起使用的，在quicklist中ziplist是一个个节点，而且quicklist为每个节点的大小都设置有阈值避免单个节点过大，从而导致性能下降</div>2020-08-03</li><br/>
</ul>