你好，我是蒋德钧。

在[第2讲](https://time.geekbang.org/column/article/268253)中，我们学习了Redis的5大基本数据类型：String、List、Hash、Set和Sorted Set，它们可以满足大多数的数据存储需求，但是在面对海量数据统计时，它们的内存开销很大，而且对于一些特殊的场景，它们是无法支持的。所以，Redis还提供了3种扩展数据类型，分别是Bitmap、HyperLogLog和GEO。前两种我在上节课已经重点介绍过了，今天，我再具体讲一讲GEO。

另外，我还会给你介绍开发自定义的新数据类型的基本步骤。掌握了自定义数据类型的开发方法，当你面临一些复杂的场景时，就不用受基本数据类型的限制，可以直接在Redis中增加定制化的数据类型，来满足你的特殊需求。

接下来，我们就先来了解下扩展数据类型GEO的实现原理和使用方法。

## 面向LBS应用的GEO数据类型

在日常生活中，我们越来越依赖搜索“附近的餐馆”、在打车软件上叫车，这些都离不开基于位置信息服务（Location-Based Service，LBS）的应用。LBS应用访问的数据是和人或物关联的一组经纬度信息，而且要能查询相邻的经纬度范围，GEO就非常适合应用在LBS服务的场景中，我们来看一下它的底层结构。
<div><strong>精选留言（30）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/10/5f/e5/54325854.jpg" width="30px"><span>范闲</span> 👍（29） 💬（1）<div>BloomFilter用的比较多。缓存穿透可以用这个防止</div>2020-10-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/57/4f/6fb51ff1.jpg" width="30px"><span>奕</span> 👍（14） 💬（2）<div>Redis 键值对中的每一个值都是用 RedisObject 保存
-------------------------
那么 redis 的键用什么保存的呢？ 也是 RedisObject 吗？</div>2020-09-05</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/90/8a/288f9f94.jpg" width="30px"><span>Kaito</span> 👍（377） 💬（35）<div>Redis也可以使用List数据类型当做队列使用，一个客户端使用rpush生产数据到Redis中，另一个客户端使用lpop取出数据进行消费，非常方便。但要注意的是，使用List当做队列，缺点是没有ack机制和不支持多个消费者。没有ack机制会导致从Redis中取出的数据后，如果客户端处理失败了，取出的这个数据相当于丢失了，无法重新消费。所以使用List用作队列适合于对于丢失数据不敏感的业务场景，但它的优点是，因为都是内存操作，所以非常快和轻量。

而Redis提供的PubSub，可以支持多个消费者进行消费，生产者发布一条消息，多个消费者同时订阅消费。但是它的缺点是，如果任意一个消费者挂了，等恢复过来后，在这期间的生产者的数据就丢失了。PubSub只把数据发给在线的消费者，消费者一旦下线，就会丢弃数据。另一个缺点是，PubSub中的数据不支持数据持久化，当Redis宕机恢复后，其他类型的数据都可以从RDB和AOF中恢复回来，但PubSub不行，它就是简单的基于内存的多播机制。

之后Redis 5.0推出了Stream数据结构，它借鉴了Kafka的设计思想，弥补了List和PubSub的不足。Stream类型数据可以持久化、支持ack机制、支持多个消费者、支持回溯消费，基本上实现了队列中间件大部分功能，比List和PubSub更可靠。

另一个经常使用的是基于Redis实现的布隆过滤器，其底层实现利用的是String数据结构和位运算，可以解决业务层缓存穿透的问题，而且内存占用非常小，操作非常高效。</div>2020-09-04</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/fd/fd/326be9bb.jpg" width="30px"><span>注定非凡</span> 👍（69） 💬（2）<div>1，作者讲了什么？
    Redis的三种扩展数据类型之一：GEO，一种可以实现LBS服务的数据结构

2，作者是怎么把这事给讲明白的？
    1，提出一个真问题：打车软件是怎么基于位置提供服务的
    2，通过GEO原理讲解，说明GEO为什么可以

3，作者为了把这事给讲清楚，讲了那些要点？有哪些亮点？
    1，亮点1：GEO的原理，这个是我之前所不知道的，学完后对GEO有了一些认知
    2，亮点2：Redis居然支持自定义数据存储结构，这打开了我的眼界
    3，要点1：GEO的底层实现，是sortSet，元素是车辆信息，权重是车辆经纬度转换过来的float值
    4，要点2：GEOHash编码，基本原理“二分区间，区间编码”（二分法的应用，将一个值编码成N位的二进制值）
    5，要点3：GEO使用GEOHash编码后，将经纬度，按照纬奇经偶位分别填充组合，得到一个车辆的经纬度编码值
    6，要点4：GEOHash编码实现的效果是将一个空间分割成为一个个方块，可以实现LBS服务（但编码值相近，不一定位置相近）

4，对于作者所讲，我有哪些发散性思考？
   ①：这一篇讲了通过Redis的GEO数据类型可以实现LBS服务，让我体验到了算法的巧妙应用带来的巨大便利（这应是科技让生活更美好的实例）。
   ②：不过，我觉得最大的惊喜在于作者介绍了如何自定义一种新的数据类型，虽然我尚未掌握开发新数据类型的能力。
   ③：通过作者的讲解，拓宽了我了见识，这让我体验到了购买专栏的价值（如果都是搜索引擎能解决的事，何必买专栏）。
   ④：作者细致的讲解开发过程，也让我对Redis的数据结构，RedisObjecti有了进一步认识（面向对象等）

5，在未来的那些场景中，我能够使用它？
    redis采用的GEOHash算法，貌似可以协助我们处理分省的一些业务

6，留言区的收获</div>2020-09-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/83/af/1cb42cd3.jpg" width="30px"><span>马以</span> 👍（45） 💬（7）<div>现在很多公司如果没有特殊场景，都是一个String走天下～</div>2020-09-04</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/20/28/e2/fbf76ae6.jpg" width="30px"><span>迷迷徒</span> 👍（16） 💬（1）<div>geohash真是妙呀</div>2020-09-07</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1e/f5/9d/104bb8ea.jpg" width="30px"><span>Geek2014</span> 👍（12） 💬（10）<div>想问一个扩展的问题，还请老师解答。
因为车辆是不断移动的，那如何维护车辆位置的GEOHASH呢。</div>2020-09-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/26/cb/28/21a8a29e.jpg" width="30px"><span>夏天</span> 👍（11） 💬（0）<div>给大家补一个

ElasticSearch 的 geo_distance 也可以用来做距离计算

按性能而言，肯定是 Redis 好。

ElasticSearch 对于搜索，更灵活，支持功能更多。

设计方案可以考虑</div>2021-04-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/49/a5/e4c1c2d4.jpg" width="30px"><span>小文同学</span> 👍（7） 💬（2）<div>1、作者讲了什么？
GEO 的数据结构原理，及特点。还有编写 Redis 新数据结构和命令的步骤（此部分我没细看）。
2、作者是怎么把事情说明白的？
通过利用 LBS(Location-Based Service)  位置信息服务 来说引入 GEO 这个数据结构如何编码地理位置的经纬度信息，写成一个数值，再利用 Sorted Set 进行存储。
3、为了讲明白，作者讲了哪些要点？哪些是亮点？
举例子说明，Hash、Sorted Set 如何无法满足 LBS 服务；
讲述 Geo Hash 的过程（二分区间，区间编码）：
将一个数值通过二分拆解，形成一个二叉树结构，得到每层的 bool 值，从而通过N位 bit 对一个数值进行存储。N 越大，精度越高；
将经纬度，分别按照 step1 获得两个 N 位bit，在进行交叉组合，得到一个值，就是 Geo Hash 值。
这个 Geo Hash 值是连续的，但位置不一定是连续的。故需要计算多个经纬度所在的方格，在求得邻居节点的较低，已提高 LBS 准确率。
4、对于作者所讲，我有哪些发散性思考？
车辆的位置信息已经存储在 GEO 集合中了，投入一个 GEO 的值，如何获得它周围的范围值呢？
5、在未来哪些场景，我可以使用它？
LBS 服务可以考虑实现它，已和公司的一个上司沟通个，大家就这个问题有了共识。nice</div>2020-09-07</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/de/28/acb248d6.jpg" width="30px"><span>晖</span> 👍（5） 💬（1）<div>严格来说，根据Redis文档: &quot;There are limits to the coordinates that can be indexed: areas very near to the poles are not indexable. Valid latitudes are from -85.05112878 to 85.05112878 degrees.&quot; 所以纬度的极值应该不能到正负90度。</div>2020-09-07</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/d3/01/716d45b6.jpg" width="30px"><span>LQS  KF</span> 👍（3） 💬（0）<div>布隆过滤器RedisBloom和RedisCell提供的限流操作</div>2021-05-20</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/sPORo6cN3GSVxjHj9nqSAPn7KG4wtSTqNUommjNndpf8qd7bHKHquuldXZfxD5nF1ldy4LeoAQNwSsOgcmWG9w/132" width="30px"><span>守望者</span> 👍（3） 💬（0）<div>纬度越高(大)的地方，单位经度所对应的地面实际距离会越小，即经度与距离并不是恒定等比的。所以我想问的是，GEORADIUS命令中的参数，5km是如何在redis中使用的呢?</div>2021-03-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/68/da/b8d734bf.jpg" width="30px"><span>白日辰</span> 👍（2） 💬（1）<div>自定义数据类型那里，是怎么去部署和实现的呢？好像只是说到编码而已？</div>2022-01-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/ee/c6/bebcbcf0.jpg" width="30px"><span>俯瞰风景.</span> 👍（2） 💬（0）<div>对于“搜索附近的餐馆”和“搜索附近的车辆”等基于地理位置信息的业务需求，想要支持这种需求，首先想到的就是获取地理位置信息并进行编码，把“比较距离远近”的问题抽象为“比较数值的差值”的问题，因为地址信息是二维空间中的问题，数值编码是一维的，那么首先要做的事情就是“数据降维”，通过GeoHash编码方式把二维数据降维到一维，然后再进行比较。而范围比较需求就可以使用Sorteed Set类型来支持了。</div>2021-09-30</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/DYAIOgq83eo6waC1mF0VmQibDjnJLEgFnmEUSNJozibaUeYZkpQaqicVcXxGZ3kKtnY5XF0iblxT4oiam7ucuJ1bqgg/132" width="30px"><span>Geek_c37e49</span> 👍（2） 💬（2）<div>为什么geo经纬度编码之后，要使用奇数位和偶数位分别存放经纬度这种交错的方式呢？有点没想通</div>2021-08-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/24/b2/17/3161b49c.jpg" width="30px"><span>达叔灬</span> 👍（2） 💬（0）<div>了解下 有这么个东西  害</div>2021-03-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/09/42/1f762b72.jpg" width="30px"><span>Hurt</span> 👍（2） 💬（1）<div>老师   基于位置信息服实际用什么数据库来做呢？真是用redis吗 ？ 还是用postgresql还是其他的数据啊</div>2020-11-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/25/f1/f7a11901.jpg" width="30px"><span>杜兰特有丶小帅</span> 👍（1） 💬（0）<div>关于geohash有个点没明白，redis把经纬度转换为geohash作为score存储在sorted set中，那么是如何计算附近的人的，比如，我想计算距离当前位置5km内的人，使用GEORADIUS命令，那么redis是如何计算出5km内的点呢？可以直接通过score算出来长度吗？</div>2022-05-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/74/aa/178a6797.jpg" width="30px"><span>阿昕</span> 👍（1） 💬（0）<div>1.签到的场景，使用了BitMap结构；
2.排行榜场景，使用了SortSet结构；
3.购物车场景，使用了HashSet结构；</div>2022-04-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/19/4f/a2/694cde4c.jpg" width="30px"><span>　　　　　　　　</span> 👍（1） 💬（3）<div>还有一点不是太清楚，geohash是怎么计算距离的了</div>2021-10-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/92/6d/becd841a.jpg" width="30px"><span>escray</span> 👍（1） 💬（2）<div>位置信息服务现在已经成为了各种服务的标配，另外，用户的地理位置信息也是很有价值的，其实我倒是非常看好高德，这可能也是百度和其他一些大厂始终不放弃开发地图和导航应用的初衷。

一开始不理解 GeoHash 的编码，为什么要经纬度编码交叉组合，后来看到那个 4 分区图示，就只能说，第一个想到的人实在是天才。

GEOADD 和 GEOADIUS 已经有点类似于 DSL 了，简化了很多操作。

专栏中老师手把手的教了一遍如何自定义类型，虽然暂时用不到，但是看的还是比较过瘾的。不过因为已经看过了全部的加餐内容，老师提到后面会讲到持久化保存的代码，明显不在其中，也可能是在专栏的正式文章里面？

个人猜测，基于位置服务的应用不会只用 Redis 来查询，还会有持久化到数据库的部分，Redis 只是提供接近实时的查询应用，Elastic 似乎也有类似的功能。

另外，从老师回复中知道，Redis 的键和值都是用 RedisObject 保存的。稍有疑问，键直接用 String 或者 SDS 来存不好么？</div>2021-03-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/c2/cc/ca22bb7c.jpg" width="30px"><span>蓝士钦</span> 👍（1） 💬（2）<div>关于用GEO来实现LBS有个疑问，缓存大小是珍贵且有限的，一次性把所有位置信息都存在缓存中不现实吧。过期淘汰策略该怎么实现？是不是要在程序中定期的做业务检测和缓存数据批量落库。只保证热点区域在缓存中即可</div>2020-10-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/ae/0c/f39f847a.jpg" width="30px"><span>D</span> 👍（1） 💬（0）<div>老师，这块的代码改动能否给个fork url 看下？</div>2020-09-06</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/8f/cf/890f82d6.jpg" width="30px"><span>那时刻</span> 👍（1） 💬（3）<div>请问老师，redisobject里的 refcount：记录了对象的引用计数，这个对象引用计数在什么情况下发生呢？具体使用场景是什么？</div>2020-09-04</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/2e/f1/f3/6a2e6977.jpg" width="30px"><span>严光</span> 👍（0） 💬（0）<div>📌 问：Redis 的 GEO 扩展类型的原理是什么？
💡 答：GEO 底层基于 Sorted Set 数据结构，排序权重采用 GeoHash 编码的经纬度信息。

📌 问：GeoHash 编码的原理是什么？
💡 答：基本原理是把二维地理空间划分成网格，每个网格中的所有经纬度都对应 GeoHash 的同一个码值。
💡 步骤：首先对经度、纬度分别做二分编码，得到 2 个 N 位编码；然后将经度、纬度的编码值按「偶数位经度、奇数位纬度」的方式插值成 2*N 位编码。

📌 问：GeoHash 编码的优缺点是什么？
💡 优点：把「二维空间的经纬度排序」简化为「一维编码值的排序」。
💡 缺点：
1.  在从经纬度网格映射到编码值的过程中，存在一定误差；
2.  有些相近的编码值，在经纬度网格中的实际距离较远（如 0111 和 1000），所以通常需要同时查询给定经纬度所在网格周围的 4-8 个网格。</div>2024-10-25</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/18/4b/d7/f46c6dfd.jpg" width="30px"><span>William Ning</span> 👍（0） 💬（2）<div>看完了，觉得大家都很厉害哦～</div>2022-03-26</li><br/><li><img src="" width="30px"><span>Geek_275fa9</span> 👍（0） 💬（0）<div>真是干活满满</div>2022-03-23</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTJ4QCWqGgMN4kp615f0Dlb8Ty61iaeOfMia7dyOic5mcgiarxGv8pyra1dibiajXicDLibxqsyM6uNabia4ckw/132" width="30px"><span>南天</span> 👍（0） 💬（0）<div>经纬度(116.034579，39.030452)取区间 是否可以用sortedset来实现，其中权重值设置成11603457939030452
先精度范围取一些只，再维度范围取一些值，然后取交集</div>2021-11-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/19/d9/ff/b23018a6.jpg" width="30px"><span>Heaven</span> 👍（0） 💬（0）<div>用布隆过滤器做限流应该算是吧</div>2021-08-05</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1a/7f/0e/e3a8dbd9.jpg" width="30px"><span>Liujun</span> 👍（0） 💬（0）<div>GEO 用来处理 LBS 相关业务功能，底层是基于 Sorted Set 实现的，使用 GEOHASH 算法把经纬度转换成 Score 值。</div>2021-07-22</li><br/>
</ul>