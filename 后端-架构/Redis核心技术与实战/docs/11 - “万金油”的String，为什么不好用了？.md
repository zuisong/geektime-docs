你好，我是蒋德钧。

从今天开始，我们就要进入“实践篇”了。接下来，我们会用5节课的时间学习“数据结构”。我会介绍节省内存开销以及保存和统计海量数据的数据类型及其底层数据结构，还会围绕典型的应用场景（例如地址位置查询、时间序列数据库读写和消息队列存取），跟你分享使用Redis的数据类型和module扩展功能来满足需求的具体方案。

今天，我们先了解下String类型的内存空间消耗问题，以及选择节省内存开销的数据类型的解决方案。

先跟你分享一个我曾经遇到的需求。

当时，我们要开发一个图片存储系统，要求这个系统能快速地记录图片ID和图片在存储系统中保存时的ID（可以直接叫作图片存储对象ID）。同时，还要能够根据图片ID快速查找到图片存储对象ID。

因为图片数量巨大，所以我们就用10位数来表示图片ID和图片存储对象ID，例如，图片ID为1101000051，它在存储系统中对应的ID号是3301000051。

```
photo_id: 1101000051
photo_obj_id: 3301000051
```

可以看到，图片ID和图片存储对象ID正好一一对应，是典型的“键-单值”模式。所谓的“单值”，就是指键值对中的值就是一个值，而不是一个集合，这和String类型提供的“一个键对应一个值的数据”的保存形式刚好契合。
<div><strong>精选留言（30）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/12/7d/8e/bc1a990d.jpg" width="30px"><span>link</span> 👍（195） 💬（12）<div>实测老师的例子，长度7位数，共100万条数据。使用string占用70mb，使用hash ziplist只占用9mb。效果非常明显。redis版本6.0.6</div>2020-08-31</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1f/08/22/ac1b8a34.jpg" width="30px"><span>super BB💨🐷</span> 👍（72） 💬（4）<div>老师，我之前看到《redis设计与实现》中提出SDS 的结构体的中没有alloc字段，书中的提到的是free,用来表示buf数组未使用的字节长度</div>2020-09-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/7a/0a/0ce5c232.jpg" width="30px"><span>吕</span> 👍（54） 💬（5）<div>我有一个疑惑，老师，文中的案例，这么大的数据量，为什么采用redis这种内存数据库来存储数据么呢，感觉它的业务场景还是不很清楚？直接采用mysql存储会有什么问题么？</div>2020-09-01</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/28/8f/f4d14c03.jpg" width="30px"><span>Hm_</span> 👍（14） 💬（5）<div>老师有个地方不是很理解，文中讲到String需要dictEntry来保存键值关系，那么hash结构最外层的那个key没有dictEntry来维护吗？因为我记得之前讲得Redis是用一个大的hash来维护所有的键值对的，所以感觉这和dictEntry所占用的内存是一样的吧</div>2020-12-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/36/2c/8bd4be3a.jpg" width="30px"><span>小喵喵</span> 👍（14） 💬（11）<div>老师，请教下，这样拆分的话，如何重复了咋办呢？
以图片 ID 1101000060 和图片存储对象 ID 3302000080 为例，我们可以把图片 ID 的前 7 位（1101000）作为 Hash 类型的键，把图片 ID 的最后 3 位（060）和图片存储对象 ID 分别作为 Hash 类型值中的 key 和 value。
比如：两张图片分别为：图片 ID 1101000060 图片存储对象 ID 3302000080；
                                     图片 ID 1101001060 图片存储对象 ID 3302000081
这个时候最后 3 位（060）的key是冲突的的，但是它的图片存储对象 ID不同。</div>2020-09-01</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/dd/9b/0bc44a78.jpg" width="30px"><span>yyl</span> 👍（13） 💬（3）<div>“在节省内存空间方面，哈希表就没有压缩列表那么高效了”
在内存空间的开销上，也许哈希表没有压缩列表高效
但是哈希表的查询效率，要比压缩列表高。
在对查询效率高的场景中，可以考虑空间换时间

</div>2020-09-03</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/17/e2/d4/ef86ea64.jpg" width="30px"><span>Front</span> 👍（4） 💬（1）<div>如果你刚好读过Database System Implemenation, 这篇正解释了NoSQL Database越来越像RDBMS</div>2020-12-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/d7/3d/a076faf1.jpg" width="30px"><span>蜗牛</span> 👍（3） 💬（3）<div>有大佬能解释下 “prev_len 有两种取值情况：1 字节或 5 字节” 这一句吗？取值的话不应该是具体的某一个值吗？这里取值为1字节或5字节 是啥意思呢？小菜鸟想不太明白。</div>2020-11-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/90/8a/288f9f94.jpg" width="30px"><span>Kaito</span> 👍（551） 💬（52）<div>保存图片的例子，除了用String和Hash存储之外，还可以用Sorted Set存储（勉强）。

Sorted Set与Hash类似，当元素数量少于zset-max-ziplist-entries，并且每个元素内存占用小于zset-max-ziplist-value时，默认也采用ziplist结构存储。我们可以把zset-max-ziplist-entries参数设置为1000，这样Sorted Set默认就会使用ziplist存储了，member和score也会紧凑排列存储，可以节省内存空间。

使用zadd 1101000 3302000080 060命令存储图片ID和对象ID的映射关系，查询时使用zscore 1101000 060获取结果。

但是Sorted Set使用ziplist存储时的缺点是，这个ziplist是需要按照score排序的（为了方便zrange和zrevrange命令的使用），所以在插入一个元素时，需要先根据score找到对应的位置，然后把member和score插入进去，这也意味着Sorted Set插入元素的性能没有Hash高（这也是前面说勉强能用Sorte Set存储的原因）。而Hash在插入元素时，只需要将新的元素插入到ziplist的尾部即可，不需要定位到指定位置。

不管是使用Hash还是Sorted Set，当采用ziplist方式存储时，虽然可以节省内存空间，但是在查询指定元素时，都要遍历整个ziplist，找到指定的元素。所以使用ziplist方式存储时，虽然可以利用CPU高速缓存，但也不适合存储过多的数据（hash-max-ziplist-entries和zset-max-ziplist-entries不宜设置过大），否则查询性能就会下降比较厉害。整体来说，这样的方案就是时间换空间，我们需要权衡使用。

当使用ziplist存储时，我们尽量存储int数据，ziplist在设计时每个entry都进行了优化，针对要存储的数据，会尽量选择占用内存小的方式存储（整数比字符串在存储时占用内存更小），这也有利于我们节省Redis的内存。还有，因为ziplist是每个元素紧凑排列，而且每个元素存储了上一个元素的长度，所以当修改其中一个元素超过一定大小时，会引发多个元素的级联调整（前面一个元素发生大的变动，后面的元素都要重新排列位置，重新分配内存），这也会引发性能问题，需要注意。

另外，使用Hash和Sorted Set存储时，虽然节省了内存空间，但是设置过期变得困难（无法控制每个元素的过期，只能整个key设置过期，或者业务层单独维护每个元素过期删除的逻辑，但比较复杂）。而使用String虽然占用内存多，但是每个key都可以单独设置过期时间，还可以设置maxmemory和淘汰策略，以这种方式控制整个实例的内存上限。

所以在选用Hash和Sorted Set存储时，意味着把Redis当做数据库使用，这样就需要务必保证Redis的可靠性（做好备份、主从副本），防止实例宕机引发数据丢失的风险。而采用String存储时，可以把Redis当做缓存使用，每个key设置过期时间，同时设置maxmemory和淘汰策略，控制整个实例的内存上限，这种方案需要在数据库层（例如MySQL）也存储一份映射关系，当Redis中的缓存过期或被淘汰时，需要从数据库中重新查询重建缓存，同时需要保证数据库和缓存的一致性，这些逻辑也需要编写业务代码实现。

总之，各有利弊，我们需要根据实际场景进行选择。</div>2020-08-31</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/fd/fd/326be9bb.jpg" width="30px"><span>注定非凡</span> 👍（105） 💬（5）<div>一，作者讲了什么？
    Redis的String类型数据结构，及其底层实现
二，作者是怎么把这事给说明白的？
    1，通过一个图片存储的案例，讲通过合理利用Redis的数据结构，降低资源消耗

三，为了讲明白，作者讲了哪些要点？有哪些亮点？
1，亮点1：String类型的数据占用内存，分别是被谁占用了
2，亮点2：可以巧妙的利用Redis的底层数据结构特性，降低资源消耗
3，要点1： Simple Dynamic String结构体（
                  buf：字节数组，为了表示字节结束，会在结尾增加“\0”
                  len： 占4个字节，表示buf的已用长度
                  alloc：占4个字节，表示buf实际分配的长度，一般大于len）

4，要点2： RedisObject 结构体（
                   元数据：8字节（用于记录最后一次访问时间，被引用次数。。。）
                   指针：8字节，指向具体数据类型的实际数据所在 ）

5，要点3：dicEntry 结构体（    
                  key：8个字节指针，指向key
                  value：8个字节指针，指向value
                  next：指向下一个dicEntry）
6，要点4：ziplist(压缩列表)（
                 zlbytes：在表头，表示列表长度
                 zltail：在表头，表示列尾偏移量
                 zllen：在表头，表示列表中
                 entry：保存数据对象模型
                 zlend：在表尾，表示列表结束）
entry：（
              prev_len：表示一个entry的长度，有两种取值方式：1字节或5字节。
                     1字节表示一个entry小于254字节，255是zlend的默认值，所以不使用。
              len：表示自身长度，4字节
              encodeing：表示编码方式，1字节
              content：保存实际数据）

5，要点4：String类型的内存空间消耗
①，保存Long类型时，指针直接保存整数数据值，可以节省空间开销（被称为：int编码）
②，保存字符串，且不大于44字节时，RedisObject的元数据，指针和SDS是连续的，可以避免内存碎片（被称为：embstr编码）
③，当保存的字符串大于44字节时，SDS的数据量变多，Redis会给SDS分配独立的空间，并用指针指向SDS结构（被称为：raw编码）
④，Redis使用一个全局哈希表保存所以键值对，哈希表的每一项都是一个dicEntry，每个dicEntry占用32字节空间
⑤，dicEntry自身24字节，但会占用32字节空间，是因为Redis使用了内存分配库jemalloc。
                    jemalloc在分配内存时，会根据申请的字节数N，找一个比N大，但最接近N的2的幂次数作为分配空间，这样可以减少频繁分配内存的次数

4，要点5：使用什么数据结构可以节省内存？
①， 压缩列表，是一种非常节省内存的数据结构，因为他使用连续的内存空间保存数据，不需要额外的指针进行连接
②，Redis基于压缩列表实现List，Hash，Sorted Set集合类型，最大的好处是节省了dicEntry开销

5，要点6：如何使用集合类型保存键值对？
①，Hash类型设置了用压缩列表保存数据时的两个阀值，一旦超过就会将压缩列表转为哈希表，且不可回退
②，hash-max-ziplist-entries：表示用压缩列表保存哈希集合中的最大元素个数 
③，hash-max-ziplist-value：表示用压缩列表保存时，哈希集合中单个元素的最大长度

四，对于作者所讲，我有哪些发散性思考？
    看了老师讲解，做了笔记，又看了黄建宏写的《Redis 设计与实现》
有这样的讲解： 
        当哈希对象可以同时满足以下两个条件时， 哈希对象使用 ziplist 编码：
	1. 哈希对象保存的所有键值对的键和值的字符串长度都小于 64 字节；
	2. 哈希对象保存的键值对数量小于 512 个；

五，在将来的哪些场景中，我能够使用它？
    这次学习Redis数据结构特性有了更多了解，在以后可以更加有信心根据业务需要，选取特定的数据结构
</div>2020-09-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/d8/17/367943f4.jpg" width="30px"><span>永祺</span> 👍（28） 💬（11）<div>hset 1101000 060 3302000080 操作为何只占用16字节？哈希键（060）、值（3302000080）两者各占用一个entry，按文中介绍，应该至少占用28字节。

其中原因，我认为很可能是文中对ziplist entry的介绍有误，参考下面GitHub文章，entry中并没有len字段，entry长度由encoding表示。所以例子中虽然创建两个entry，但总长度是小于16的。

参考：https:&#47;&#47;github.com&#47;zpoint&#47;Redis-Internals&#47;blob&#47;5.0&#47;Object&#47;hash&#47;hash_cn.md</div>2020-10-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/41/5e/9d2953a3.jpg" width="30px"><span>zhou</span> 👍（20） 💬（39）<div>hset 1101000 060 3302000080
这条记录只消耗 16 字节没明白，压缩列表保存一个对象需要 14 字节，060、3302000080 都需要保存，那应该至少大于 28 字节</div>2020-09-01</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1c/f1/e5/c8f4e000.jpg" width="30px"><span>aworker</span> 👍（15） 💬（3）<div>看好多小伙伴里面对embstr的临界点是44字节的算法有疑问，给大家解释下：

首先说下redisObject的数据结构包含如下字段：
type：表明redisobjct的类型如果string，hash，set等，占4字节。
encoding：编码类型，占4字节。
lru:记录此object最近被访问的时间数据和过期逻辑有关，4字节。
refcount:记录指向此object的指针数量，用来表示不同指针相同数据的情况，4个字节。
ptr：真正指向具体数据的指针，8字节。

在3.2版本以前的sds结构如下：
len：表示sds中buf已经使用的长度，4个字节。
free：表示sds中buf没有使用的长度，4个字节。
buf：数组，真正存储数据的地方，会有1字节的‘\0’，表示数据的结尾。

如果想让string类型用embstr编码那么需要满足如下条件：

64-16（redisObjct除去ptr后最小使用的内存）-（4+4+1）（sds最小内存需求）=39 。

redis 3.2及其以后的版本sds会根据实际使用的buf长度，采用不同的sds对象表示，这里只说下小于等64字节的sds对象结构：
len：表示buf的使用长度，1字节。
alloc：表示分配给buf的总长度，1字节。
flag：表示具体的sds类型，1个字节。
buf：真正存储数据的地方，肯定有1字节的‘\0’表示结束符。

如果想让redis3.2以后的版本使用embstr编码的string需要buf满足的最大值为：
64-16（redisObject最小值）-（1+1+1+1）（sds最小用的内存）= 44字节。

这里需要澄清一点：相较于raw编码，当redis采用 embstr编码的时候，redis会吧redisObjct的元数据和sds连续存在，这就节约了ptr指针的内存使用，这也是redis要分embstr和raw的原因。老师的图中embstr编码也有8字节的指针，这个应该是不准确的。

随着版本升级也能看出redis开发者对高效数据结构的极致追求：在3.2版本以前的sds中用4个字节表示buf的已用长度和未使用长度，但对于embstr编码的sds是有些浪费的，因为buf最大值是39字节，1字节就可以表示255的长度了，所以3.2以后的embstr编码的sds的 len和alloc都是一个字节。



</div>2021-05-06</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/9b/6e/edd2da0c.jpg" width="30px"><span>蓝魔丶</span> 👍（14） 💬（6）<div>老师，测试环境：redis5.0.4
1.实践采用String方案：set 1101000052 3301000051，查看内存增加的72，而不是64，是为什么？
2.实践采用Hash方案：hset 1101000 060 3302000080 查看内存增加88，再次添加key-value，才是满足增加16</div>2020-09-02</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/2c/6b/6c/3e80afaf.jpg" width="30px"><span>HappyHasson</span> 👍（11） 💬（1）<div>hset 1101000 060 3302000080  为什么这条语句执行之后内存增加了16B？

老师的前提是执行命令之前已经有了hash key 1101000。然后插入fieldkey:060   fieldvalue:3302000080
fieldkey和fieldvalue各分配一个ziplist entry，hset时，会调用ziplistPush函数先把fieldkey放到ziplist表尾，然后再放fieldvalue。之所以是16字节，是老师讲解的有点问题。ziplist entry包含三个字段previous_entry_length、encoding、content。没有老师说的len这个固定4字节的字段
previous_entry_length取值规则：https:&#47;&#47;github.com&#47;zpoint&#47;Redis-Internals&#47;blob&#47;5.0&#47;Object&#47;hash&#47;prevlen.png
encoding取值规则：https:&#47;&#47;github.com&#47;zpoint&#47;Redis-Internals&#47;blob&#47;5.0&#47;Object&#47;hash&#47;encoding.png
所以这个命令的fieldkey占用字节：1+1+1=3、fieldvalue占用字节：1+1+8(64位整数表示3302000080)</div>2022-03-03</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/43/79/18073134.jpg" width="30px"><span>test</span> 👍（9） 💬（3）<div>虽然压缩列表可以节约内存，但是set和get的时间复杂度为O(N)，一个时间换空间的方法。</div>2020-09-02</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/57/4f/6fb51ff1.jpg" width="30px"><span>奕</span> 👍（9） 💬（0）<div>使用 http:&#47;&#47;www.redis.cn&#47;redis_memory&#47; 这个网站来计算 文章中 一亿张图片ID消耗的内存， 为什么得出来 9269.71M,  9点多个 G呢？ 1亿个 string , string 的 key 和 value 分别是 8个 字节
</div>2020-09-01</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTLzvaL724GwtzZ5mcldUnlicicSlI8BXL9icRZbUOB10qjRMlmog7UTvwxSBHXagnPGGR1BYdjWcGGSg/132" width="30px"><span>wwj</span> 👍（6） 💬（3）<div>这样是不是有点本位倒置了，缓存本来就是以空间换时间的，这样节省了空间，但是时间复杂度也上去了</div>2020-09-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/e8/55/63189817.jpg" width="30px"><span>MClink</span> 👍（6） 💬（0）<div>老师，底层数据结构的转换是怎么实现的呢？是单纯的开一个新的数据结构再把数据复制过去吗？再释放之前的数据结构的内存，复制过程中有修改值的话要怎么处理，复制过程中不就两倍内存消耗了</div>2020-08-31</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1d/fe/83/df562574.jpg" width="30px"><span>慎独明强</span> 👍（6） 💬（0）<div>看了Redis设计与实现，有讲SDS这一块，对于老师分析的内容，自己心里有印象，再结合老师今天的实践案例，前面的知识还没有吃透
😂😂</div>2020-08-31</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/45/ab/7dec2448.jpg" width="30px"><span>我不用网名</span> 👍（5） 💬（1）<div>看了很久, 一直没有静下心来仔细品味, 今天又重新将课程内容梳理了一遍,有几个问题, 希望老师能解答一下:
1.  redis把sds使用raw编码还是embstr编码的临界值是44, 这个44是如何计算出来的呢? 按文档中sds len(4) + alloc(4) + 1(\0)  + redisObject(元素数据8+指针8) = 25, jemalloc 将超过64字节的使用raw编码, 这样的话, buff 的最大值 64-25=39.    这也是我看网上其它资料时写的reids.3.2版本之前使用的值. 3.2及以后使用44.  老师文档中sds各字段的大小是不是标错了?
2.  hash类型使用ziplist存储数据时, key&#47;value的映射关系是发何保持的呢?
     我自己有如下猜想,存储结构是不是这样?
     zlbytes zltail zllen key1 value1 key2 value2 ...  zlend
     如果是这样存储的话, 又有以下两个问题困绕着我:
     在hash中通过某个key获取对应value时,需要遍历整个压缩列表吧. 这会不会有性能影响?
     key与value都紧挨着存储, entry里面并没有字段用于标记该entry是key还是value, 假如 key与value是相同的字段串时, 即有两个相同的entry, reids如何识别哪个是key,哪个是value呢?
     对于后面一个问题,我自己可以猜想一下的, 就是key与value是成对出现的, key 永远是在寄数位 value永远是在偶数位. 这样也可以分辨, 如果是我来实现的话,可能会这样. 但我不懂c,没看过源码, 请老师专业解答我才放心.
    感谢!
     </div>2020-09-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/28/4a/a7/ab7998b1.jpg" width="30px"><span>zachary</span> 👍（4） 💬（2）<div>通过查看redis的源码，sds数据结构这块老师讲的不是很对。可能跟redis的版本有关吧。redis在高版本对sds做了优化，sds将不再直接使用结构体。sds底层通过sdshdr_5, sdshdr_8, sdshdr_16, sdshdr_32, sdshdr_64来实现。这么做的目的明显是为了更加节省空间。以下是源码，版本4.0.9， 文件sds.h。

typedef char *sds;

&#47;* Note: sdshdr5 is never used, we just access the flags byte directly.
 * However is here to document the layout of type 5 SDS strings. *&#47;
struct __attribute__ ((__packed__)) sdshdr5 {
    unsigned char flags; &#47;* 3 lsb of type, and 5 msb of string length *&#47;
    char buf[];
};
struct __attribute__ ((__packed__)) sdshdr8 {
    uint8_t len; &#47;* used *&#47;
    uint8_t alloc; &#47;* excluding the header and null terminator *&#47;
    unsigned char flags; &#47;* 3 lsb of type, 5 unused bits *&#47;
    char buf[];
};
struct __attribute__ ((__packed__)) sdshdr16 {
    uint16_t len; &#47;* used *&#47;
    uint16_t alloc; &#47;* excluding the header and null terminator *&#47;
    unsigned char flags; &#47;* 3 lsb of type, 5 unused bits *&#47;
    char buf[];
};
struct __attribute__ ((__packed__)) sdshdr32 {
    uint32_t len; &#47;* used *&#47;
    uint32_t alloc; &#47;* excluding the header and null terminator *&#47;
    unsigned char flags; &#47;* 3 lsb of type, 5 unused bits *&#47;
    char buf[];
};
struct __attribute__ ((__packed__)) sdshdr64 {
    uint64_t len; &#47;* used *&#47;
    uint64_t alloc; &#47;* excluding the header and null terminator *&#47;
    unsigned char flags; &#47;* 3 lsb of type, 5 unused bits *&#47;
    char buf[];
};
</div>2021-06-25</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/34/67/06a7f9be.jpg" width="30px"><span>while (1)等;</span> 👍（4） 💬（2）<div>老师，压缩列表里的prev_len有什么作用，记录上一个的长度意义在哪？</div>2021-02-18</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/FQQA0icGXUvJZicd7jX1r85MmH2XgpQUlkXNpB2u9OibCc1k3ITJwaqbZm7WQiaT93hWYDRBCJMsThuL62PLTaP5hQ/132" width="30px"><span>ytyee</span> 👍（4） 💬（5）<div>老师，这里真不太理解。

所以，在刚才的二级编码中，我们只用图片 ID 最后 3 位作为 Hash 集合的 key，也就保证了 Hash 集合的元素个数不超过 1000，同时，我们把 hash-max-ziplist-entries 设置为 1000，这样一来，Hash 集合就可以一直使用压缩列表来节省内存空间了。

这里我不太理解，entries不是指元素的个数吗？跟元数的值的长度有什么关系呢，我用后3位，后4位不都是1个元素吗？</div>2021-02-03</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTJkeOAC8k7aPMfQZ4ickiavpfR9mTQs1wGhGtIicotzAoszE5qkLfFTabkDU2E39ovSgoibJ1IiaLXtGicg/132" width="30px"><span>bigben</span> 👍（2） 💬（2）<div>感觉ziplist这里讲的不对啊，二级索引的key也占空间啊</div>2021-08-02</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/Etr1TYTsMiazWFoGnReIVP9ic9Na38BFkTOKbdgiaicwBLgHBnS980Xn03FJ1UPWAyiaONEMtyiaU7vNw2RlhSkUsYDQ/132" width="30px"><span>gen</span> 👍（2） 💬（0）<div>hash用ziplist实现时，插入键值对的时候，不是应该插入两个entry吗？如果键为三位数，那占用8个字节；值为16个字节，还是需要24个字节的单位。为什么每次插入只增加16个字节呢？</div>2021-02-04</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/8e/41/709e9677.jpg" width="30px"><span>袁帅</span> 👍（2） 💬（0）<div>hset 1101000 060 3302000080

增加一条，key(060)  value(3302000080) 都要存储在ziplist中吧

value(3302000080)  这个entry 占用 14个字节， 
key(060) 也需要占用8个字节呀 （1+4+1+4）= 10
事实上我实践有的时候也有占用24个字节的情况， 但是大部分增加一条占用 16个字节
请老师同学们解惑一下呀</div>2020-11-21</li><br/><li><img src="" width="30px"><span>13761642169</span> 👍（2） 💬（4）<div>有个疑问：（测试redis版本6.0.7）
执行命令：hset 1101000 060 3302000080，执行之前，通过info memory得到used_memory：353968，第1次执行后，同样得到used_memory：354056，这里增加了88，再一次执行并存储不同的hash key（hset 1101000 061 3302000081），就是老师所分析的16个字节了，那88个字节我分析了下，但始终分析不出来：
（1）全局hash的key为8个字节的指针，指向一个dictEntry结构
（2）dictEntry占用32个字节
（2.1）dictEntry-key指向一个RedisObject结构，占用16个字节（8位元数据+8为long型1101000）
（2.2）dictEntry-value指向一个RedisObject结构，占用16个字节（8为元数据+8为指向压缩列表的指针）
（3）压缩列表：zlbytes、zltail、zllen、zlend占用4+4+2+1=11个字节；数据entry项：prev_len、len、encoding、content（3302000081）为1+4+1+8=14字节，共计25个字节，而根据jemalloc的分配策略，实际会分配32个字节

综上，新增加一个只有一个元素的hash表，共计增加：8+32+16+16+32=104，和实际增加的88个字节不等？？？？？</div>2020-09-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/c6/18/2a9c0ff6.jpg" width="30px"><span>子非鱼</span> 👍（2） 💬（0）<div>为啥只增了16字节，图片 ID 的前 7 位作为 Hash 类型的键这个不是也要占用空间么</div>2020-09-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/20/27/8e/9f1edfc5.jpg" width="30px"><span>拥有两个端点是线段</span> 👍（2） 💬（1）<div>老师，在字符串长度不超过44字节时是使用embstr编码，那为何规定是44字节呢？</div>2020-08-31</li><br/>
</ul>