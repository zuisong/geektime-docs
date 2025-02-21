你好，我是蒋德钧。

在Web和移动应用的业务场景中，我们经常需要保存这样一种信息：一个key对应了一个数据集合。我举几个例子。

- 手机App中的每天的用户登录信息：一天对应一系列用户ID或移动设备ID；
- 电商网站上商品的用户评论列表：一个商品对应了一系列的评论；
- 用户在手机App上的签到打卡信息：一天对应一系列用户的签到记录；
- 应用网站上的网页访问信息：一个网页对应一系列的访问点击。

我们知道，Redis集合类型的特点就是一个键对应一系列的数据，所以非常适合用来存取这些数据。但是，在这些场景中，除了记录信息，我们往往还需要对集合中的数据进行统计，例如：

- 在移动应用中，需要统计每天的新增用户数和第二天的留存用户数；
- 在电商网站的商品评论中，需要统计评论列表中的最新评论；
- 在签到打卡中，需要统计一个月内连续打卡的用户数；
- 在网页访问记录中，需要统计独立访客（Unique Visitor，UV）量。

通常情况下，我们面临的用户数量以及访问量都是巨大的，比如百万、千万级别的用户数量，或者千万级别、甚至亿级别的访问信息。所以，我们必须要选择能够非常高效地统计大量数据（例如亿级）的集合类型。

**要想选择合适的集合，我们就得了解常用的集合统计模式。**这节课，我就给你介绍集合类型常见的四种统计模式，包括聚合统计、排序统计、二值状态统计和基数统计。我会以刚刚提到的这四个场景为例，和你聊聊在这些统计模式下，什么集合类型能够更快速地完成统计，而且还节省内存空间。掌握了今天的内容，之后再遇到集合元素统计问题时，你就能很快地选出合适的集合类型了。
<div><strong>精选留言（30）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/0f/90/8a/288f9f94.jpg" width="30px"><span>Kaito</span> 👍（557） 💬（39）<div>使用Sorted Set可以实现统计一段时间内的在线用户数：用户上线时使用zadd online_users $timestamp $user_id把用户添加到Sorted Set中，使用zcount online_users $start_timestamp $end_timestamp就可以得出指定时间段内的在线用户数。

如果key是以天划分的，还可以执行zinterstore online_users_tmp 2 online_users_{date1} online_users_{date2} aggregate max，把结果存储到online_users_tmp中，然后通过zrange online_users_tmp 0 -1 withscores就可以得到这2天都在线过的用户，并且score就是这些用户最近一次的上线时间。

还有一个有意思的方式，使用Set记录数据，再使用zunionstore命令求并集。例如sadd user1 apple orange banana、sadd user2 apple banana peach记录2个用户喜欢的水果，使用zunionstore fruits_union 2 user1 user2把结果存储到fruits_union这个key中，zrange fruits_union 0 -1 withscores可以得出每种水果被喜欢的次数。

使用HyperLogLog计算UV时，补充一点，还可以使用pfcount page1:uv page2:uv page3:uv或pfmerge page_union:uv page1:uv page2:uv page3:uv得出3个页面的UV总和。

另外，需要指出老师文章描述不严谨的地方：“Set数据类型，使用SUNIONSTORE、SDIFFSTORE、SINTERSTORE做并集、差集、交集时，选择一个从库进行聚合计算”。这3个命令都会在Redis中生成一个新key，而从库默认是readonly不可写的，所以这些命令只能在主库使用。想在从库上操作，可以使用SUNION、SDIFF、SINTER，这些命令可以计算出结果，但不会生成新key。

最后需要提醒一下：

1、如果是在集群模式使用多个key聚合计算的命令，一定要注意，因为这些key可能分布在不同的实例上，多个实例之间是无法做聚合运算的，这样操作可能会直接报错或者得到的结果是错误的！

2、当数据量非常大时，使用这些统计命令，因为复杂度较高，可能会有阻塞Redis的风险，建议把这些统计数据与在线业务数据拆分开，实例单独部署，防止在做统计操作时影响到在线业务。</div>2020-09-02</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/fd/fd/326be9bb.jpg" width="30px"><span>注定非凡</span> 👍（69） 💬（0）<div>1，作者讲了什么？
    1，Redis有那些数据结构适合做统计

2，作者是怎么把这事给讲明白的？
    1，列举了常见的数据统计需求。从实际需求出发，推荐适合的数据类型，讲解了怎么用，并解答这种数据结构为什么可以
    2，将数据统计需求，分了四类，分类分别讲解

3，为了讲明白，作者讲了哪些要点，有哪些亮点？
    1，亮点1：BITMAP的特性和使用场景，方式
    2，亮点2：HyperLogLog的特性和使用场景，方式
    3，要点1：日常的统计需求可以分为四类：聚合，排序，二值状态，基数，选用适合的数据类型可以实现即快速又节省内存
    4，要点2：聚合统计，可以选用Set类型完成，但Set的差，并，交集操作复杂度高，在数据量大的时候会阻塞主进程
    5，要点3：排序统计，可以选用List和Sorted Set
    6，要点4：二值状态统计：Bitmap本身是用String类型作为底层数据结构实现，String类型会保存为二进制字节数组，所以可以看作是一个bit数组
    7，要点5：基数统计：HyperLogLog ,计算基数所需空间总是固定的，而且很小。但要注意，HyperLogLog是统计规则是基于概率完成的，不是非常准确

4，对于作者所讲，我有那些发散性思考？
    1，对于统计用户的打卡情况，我们项目组也做了这个需求，但遗憾的是我们没有采用bitmap这种方案，而是使用了 sortSet
    2，HyperLogLog可以考虑使用到，我们项目中的统计视频播放次数，现在这块，我们的方案是，每天产生一个key，单调递增。在通过定时任务，将缓存中的结果，每天一条数据记录，存入数据库

5，在将来的那些场景中，我能够使用它？

6，留言区的收获

1，主从库模式使用Set数据类型聚合命令(来自 @kaito 大神)
    ①：使用SUNIONSTORE，SDIFFSTORE，SINTERSTOR做并集，差集，交集时，这三个命令都会在Redis中生成一个新key,而从库默认是readOnly。所以这些命令只能在主库上使用
    ②：SUNION，SDIFF,SINTER，这些命令可以计算出结果，不产生新的key可以在从库使用
   </div>2020-09-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/fc/d4/743d3f02.jpg" width="30px"><span>Anthony</span> 👍（36） 💬（2）<div>感觉第一个聚合统计这种场景一般频率不会太高，一般都是用在运营统计上，可以直接在mysql的从库上去统计，而不需要在redis上维护复杂的数据结构</div>2020-09-02</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/20/47/d5/24e60497.jpg" width="30px"><span>波哥威武</span> 👍（25） 💬（0）<div>现在大数据情况下都是通过实时流方式统计pvuv，不太会基于redis，基于存在即合理，老师能分析下相关优劣吗，我个人的想法，一个是在大量pvuv对redis的后端读写压力，还有复杂的统计结果redis也需要复杂的数据结构设计去实现，最后是业务和分析任务解耦。</div>2020-09-02</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/ea/51/9132e9cc.jpg" width="30px"><span>土豆哪里挖</span> 👍（21） 💬（2）<div>在集群的情况下，聚合统计就没法用了吧，毕竟不是同一个实例了</div>2020-09-02</li><br/><li><img src="" width="30px"><span>Geek_960d5b</span> 👍（15） 💬（0）<div>老师只是提供了一种使用思路，
但做统计业界主流还是上数仓用hive等做报表</div>2020-11-02</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/23/5b/983408b9.jpg" width="30px"><span>悟空聊架构</span> 👍（12） 💬（4）<div>对于这个问题：假设越新的评论权重越大，目前最新评论的权重是 N，我们执行下面的命令时，就可以获得最新的 10 条评论。

理解如下：

假设当前的评论 List 是{A, B, C, D, E, F}（其中，A 是最新的评论，以此类推，F 是最早的评论，权重分别为 10，9，8，7，6，5）。

在展示第一页的 3 个评论时，按照权重排序，查出 ABC。

展示第二页的 3 个评论时，按照权重排序，查出 DEF。

如果在展示第二页前，又产生了一个新评论 G，权重为 11，排序为 {G, A, B, C, D, E, F}。

再次查询第二页数据时，权重还是会以 10 为准，逻辑上，第一页的权重还是 10，9，8。

查询第二页数据时，可以查询出权重等于 7，6，5 的数据，返回评论 DEF。

当想查询出最新评论时，需要以权重 11 为准，第一页数据的权重就是 11，10，9，返回评论 GAB。

再次查询第二页数据时，以权重 11 为准，查询出评论 CDE。</div>2021-05-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/5f/e5/54325854.jpg" width="30px"><span>范闲</span> 👍（12） 💬（3）<div>1.redis里不建议用聚合统计。原因有几点:
单实例会阻塞。cluster的时候key可能分布在不同的节点，需要调用方做聚合。
2.带排序的统计可以使用sorted set。cluster的时候可能一样需要做聚合
3.hyperlog是带误差的统计，可以用来统计总量。</div>2020-10-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/26/38/ef063dc2.jpg" width="30px"><span>Darren</span> 👍（10） 💬（4）<div>
老师说的大部分场景都没用到过。。。。。
我们有这么一种场景：
	在多实例下，定时任务就不能使用@Schedule使用，必须使用分布式定时调度，我们自研的分布式调度系统支持MQ和Http两种模式，同时支持一次性的调用和Cron表达是式形式的多次调用。
	在MQ模式下（暂时不支持Cron的调用），分布式调度系统作为MQ的消费者消费需要调度的任务，同时消息中会有所使用的资源，调度系统有对应的资源上线，也可以做资源限制，没有可用资源时，消息不调度（不投递）等待之前任务资源的释放，不投递时消息就在Zset中保存着，当然不同的类型在不同的Zset中，当有对用的资源类型释放后，会有专门的MQ确认消息，告诉任务调度系统，某种类型的资源已经释放，然后从对应type的Zset中获取排队中优先级最高的消息，进行资源匹配，如果可以匹配，则进行消息发送。
	当然http也是类似的，只是http不做资源管理，业务方自己掌控资源及调用频次，http请求的调用时调度系统自己发起的，引入quartz，在时间到达后，通过Http发送调用。
</div>2020-09-02</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/e8/e4/c9dd6058.jpg" width="30px"><span>阿基米德</span> 👍（9） 💬（2）<div>这里一亿个数据返回给客户端处理，这个场景是不是就会有大key问题</div>2021-05-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/1b/93/e3b44969.jpg" width="30px"><span>sgl</span> 👍（6） 💬（0）<div>12MB的bitmap是大key了，生产环境会有问题等我</div>2021-04-02</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTKib3vNM6TPT1umvR3TictnLurJPKuQq4iblH5upgBB3kHL9hoN3Pgh3MaR2rjz6fWgMiaDpicd8R5wsAQ/132" width="30px"><span>陈阳</span> 👍（4） 💬（4）<div>没懂， 文中说到的list由于插入的新的评论，第二页可能会读到原第一页的值， 我觉得这个本来不应该就是这样的吗？ 应该因为最新评论已经刷新了啊， 难道还要回去读原来的老数据吗 这块没太看懂</div>2021-08-07</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1d/fe/83/df562574.jpg" width="30px"><span>慎独明强</span> 👍（4） 💬（16）<div>有个疑问，统计亿级用户连续10天登录的场景，每天用一个bitmap的key，来存储每个用户的登录情况，将10个bitmap的key进行与运算来统计连续10天登录的用户，这个是怎么保证10个bitmap相同位是同一个用户的登录情况呢？</div>2020-09-02</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/0e/6c/1f3b1372.jpg" width="30px"><span>哈哈哈</span> 👍（2） 💬（0）<div>个人感觉redis不太适合做聚合统计，这种统计是通过埋点+大数据平台</div>2023-01-31</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/5a/34/4cbadca6.jpg" width="30px"><span>吃饭睡觉打酱油</span> 👍（2） 💬（3）<div>老师，我对bitmap统计1亿用户的有个疑问，缓存中的bitmap是怎么初始化或者怎么来的呢，怎么保证用户的顺序呢？</div>2021-04-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/ef/21/69c181b8.jpg" width="30px"><span>Rain</span> 👍（2） 💬（0）<div>redis真是应用开发利器啊</div>2020-09-16</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/00/69/3b1375ca.jpg" width="30px"><span>海拉鲁</span> 👍（2） 💬（9）<div>之前做过利用redis一个统计最近200个客户触达率的方案，借助list+lua
具体是用0代表触达，1代表未触达，不断丢入队列中。需要统计是lrang key 0 -1 取出全部元素，计算0的比例就是触达率了。
这样不需要每次都计算一次触达率，而是按需提供，也能保证最新。应该不是很有共性的需求，是我们对用户特定需求的一个尝试</div>2020-09-02</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/cc/de/e28c01e1.jpg" width="30px"><span>剑八</span> 👍（1） 💬（1）<div>redis还是适合缓存提速场景
像评论这样的，要实际看业务，是有一定业务逻辑的。比如评论还有几星，图片什么的，这种用redis就比较被动了。</div>2022-08-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/6c/a4/7f7c1955.jpg" width="30px"><span>死磕郎一世</span> 👍（1） 💬（1）<div>list新增元素如果插入到尾部，这样，前面的元素位置就不用改变了</div>2021-06-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/3e/8a/891b0e58.jpg" width="30px"><span>wnz27</span> 👍（1） 💬（2）<div>有个疑问，每个用户签到是横向情况，也就是一亿个十位bit，怎么转变为竖向的10个一亿位bit</div>2021-04-07</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/0a/a4/828a431f.jpg" width="30px"><span>张申傲</span> 👍（1） 💬（0）<div>使用 incr 统计一个网页的 PV，具体为 incr page:{page_id} 和 get page:{page_id} 。因为 PV 都是长整型，因此对于String类型来说，可以采用 int 编码方式，内存开销不大。</div>2020-12-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/5b/8f/4b0ab5db.jpg" width="30px"><span>Middleware</span> 👍（1） 💬（0）<div>昨天遇到一个近实时的排行榜，类似抖音排行榜那种，老师用有序集合来做是不是好？这是我昨天的方案</div>2020-09-04</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/7d/8e/bc1a990d.jpg" width="30px"><span>link</span> 👍（1） 💬（3）<div>不是很懂 key=user280680 value 是一个set  set里面又是用户id。 key不是已经是userId了么。为啥value里面还要存那么多userId干什么</div>2020-09-03</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/2e/f1/f3/6a2e6977.jpg" width="30px"><span>严光</span> 👍（0） 💬（0）<div>本章总结：
【聚合统计】采用 Set 类型，用 SUNIONSTORE 求并集、SDIFFSTORE 求差集、SINTERSTORE 求交集，但开销较高。
【排序统计】采用 Sorted Set 类型，用 ZRANGEBYSCORE 按权重排序。
【二值统计】采用 Bitmap 扩展类型，用 SETBIT 设置、GETBIT 查询、BITCOUNT 计数，或用 BITOP 对多个 Bitmap 做按位与&#47;异或操作。
【基数统计】采用 HyperLogLog 扩展类型，用 PFADD 设置、PFCOUNT 统计，它的优势在于需要的空间是固定的（只需 12KB 就可以统计接近 2^64 个元素），但缺点是统计存在一定误差。</div>2024-10-24</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTIrwJL5ic5iaZj2z6rbnIiaWZnMpJ3fJBBwFmSt7eFA00PgHoUPJ01awf4eGmfABPlz7PyvLfgu07EFg/132" width="30px"><span>rlzhao</span> 👍（0） 💬（0）<div>如果使用过程中redis服务重启，可能会造成数据丢失，这样统计的数据可能会不准确吧</div>2024-02-26</li><br/><li><img src="" width="30px"><span>Geek_fd9ad5</span> 👍（0） 💬（0）<div>redis是有这些数据结构，但实际的使用场景不是文章中讲的这些例子。真这么用要出大问题。</div>2023-09-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/2d/75/e7c29de4.jpg" width="30px"><span>wkq2786130</span> 👍（0） 💬（0）<div>分享一篇redis内存优化的文章  https:&#47;&#47;weikeqin.com&#47;2023&#47;06&#47;24&#47;redis-memory-optimization&#47;</div>2023-08-07</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/ae/8a/e67def95.jpg" width="30px"><span>念头通达</span> 👍（0） 💬（0）<div>slave-read-only 设置为no 就可以在从库进行写，并且这个写操作不会同步给别的实例(主-从-从)</div>2023-06-04</li><br/><li><img src="" width="30px"><span>wdg</span> 👍（0） 💬（0）<div>老师，统计uv 用bitmap是不是也可以呢</div>2022-08-27</li><br/><li><img src="" width="30px"><span>风之翼</span> 👍（0） 💬（0）<div>Redis 是将 Bitmap 以 String 类型的形式保存为二进制的字节数组吗？</div>2022-07-28</li><br/>
</ul>