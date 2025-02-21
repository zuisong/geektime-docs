你好，我是李玥。

从这节课开始，我们课程将进入最后一部分“海量数据篇”，这节课也是我们最后一节主要讲MySQL的课程。解决海量数据的问题，必须要用到分布式的存储集群，因为MySQL本质上是一个单机数据库，所以很多场景下不是太适合存TB级别以上的数据。

但是，绝大部分的电商大厂，它的在线交易这部分的业务，比如说，订单、支付相关的系统，还是舍弃不了MySQL，原因是，**只有MySQL这类关系型数据库，才能提供金融级的事务保证**。我们之前也讲过分布式事务，那些新的分布式数据库提供的所谓的分布式事务，多少都有点儿残血，目前还达不到这些交易类系统对数据一致性的要求。

那既然MySQL支持不了这么大的数据量，这么高的并发，还必须要用它，怎么解决这个问题呢？还是按照我上节课跟你说的思想，**分片**，也就是拆分数据。1TB的数据，一个库撑不住，我把它拆成100个库，每个库就只有10GB的数据了，这不就可以了么？这种拆分就是所谓的MySQL分库分表。

不过，思路是这样没错，分库分表实践起来是非常不容易的，有很多问题需要去思考和解决。

## 如何规划分库分表？

还是拿咱们的“老熟人”订单表来举例子。首先需要思考的问题是，分库还是分表？分库呢，就是把数据拆分到不同的MySQL库中去，分表就是把数据拆分到同一个库的多张表里面。
<div><strong>精选留言（30）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/16/e7/76/79c1f23a.jpg" width="30px"><span>李玥</span> 👍（25） 💬（0）<div>Hi，我是李玥。

这里回顾一下上节课的思考题：

在数据持续增长的过程中，今天介绍的这种“归档历史订单”的数据拆分方法，和直接进行分库分表相比，比如说按照订单创建时间，自动拆分成每个月一张表，两种方法各有什么优点和缺点？欢迎你在留言区与我讨论。

这个问题我在本节课中也提到了，简单的总结一下。按月自动拆分订单的好处是，不需要做数据搬运，相对实现比较简单，数据分得更碎，缺点是跨月查询比较麻烦，但好处是容量也更大（因为分片更多）。归档历史订单的方法，实现起来更复杂，容量要小一些，但是对查询更加友好。</div>2020-04-01</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/34/df/64e3d533.jpg" width="30px"><span>leslie</span> 👍（37） 💬（2）<div>是不是漏了另外一种拆分方式：纵向拆分？分表应当还有一个原因，早期数据量小可以几十个字段都没有关系；后期数据量大了，多列查询导致了一些性能问题。我自己在生产中就碰到了设计的不合理性，做了纵向分表-效果还不错，精度只能靠实战、学习、反思去提升。
课程中提及的分表所引发的外键问题其实应当和DML有关：查询并无影响。个人觉得影响不大，细看是多张表，但是设计时其实还是一张；查询时对应的判断补进去就好。</div>2020-04-02</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/66/9b/59776420.jpg" width="30px"><span>百威</span> 👍（28） 💬（7）<div>接“发条橙子”“用完整用户id分片还是后四位分片”对话：为什么是一样的啊，没懂……比如300个分片，用取模法，用户id分别为12000和22000，后四位相同但查找的表不同呀……我感觉这块没说清楚，我听完之后也有这个疑惑</div>2020-04-13</li><br/><li><img src="https://wx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTJkwbyTYtSCx6Qc7cQPnnRWv38Jybh3etziaPmuP8gHcgS6FMxcdftrKgWiamH6fc2iciaicDKDVEwcEibQ/132" width="30px"><span>sami</span> 👍（24） 💬（1）<div>感觉Redis Cluster的分片规则有点像查表法</div>2020-03-31</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/fa/f7/91ac44c5.jpg" width="30px"><span>Mq</span> 👍（16） 💬（3）<div>关联表可以冗余用户ID字段，跟订单表的都在一个库里吗，这样用户维度的交易都在一个库事物里面，大部分的关联查询也是在一个库里。
老师查找法有具体例子吗，我们之前也有过表按hash分后数据极度不均</div>2020-03-31</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/28/29/162e2795.jpg" width="30px"><span>Loren</span> 👍（13） 💬（6）<div>老师，请教一个问题，分库分表以后，数据量大的情况下，分页一般该怎么处理？我暂时没这方面的经验，想了解一下</div>2020-04-04</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/f3/83/e2612d81.jpg" width="30px"><span>锐</span> 👍（11） 💬（1）<div>请问老师，假设现在是24个分片，使用取模算法，后续发现分片后数据量还是太大，要改成扩大分片数，需要重新迁移数据吧？工作量大且复杂，该怎么设计比较方便扩容呢</div>2020-04-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/81/4d/5f892de2.jpg" width="30px"><span>Echo</span> 👍（8） 💬（1）<div>老师您好：您文中说“范围分片特别适合那种数据量非常大，但并发访问量不大的 ToB 系统”，如果是这样的话 并发量不大的ToB 系统就没必要分库了吧？因为分库要解决的是高并发的问题。可以用分表或者归档的方式解决？</div>2020-05-16</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/DYAIOgq83erbY9UsqHZhhVoI69yXNibBBg0TRdUVsKLMg2UZ1R3NJxXdMicqceI5yhdKZ5Ad6CJYO0XpFHlJzIYQ/132" width="30px"><span>饭团</span> 👍（8） 💬（17）<div>老师您好，您提到的把用户id放到订单id中，是说如果用订单id去做查询，就把第10-14位取出来，之后再用这部分去查询是吗？</div>2020-03-31</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/87/62/f99b5b05.jpg" width="30px"><span>曙光</span> 👍（7） 💬（6）<div>老师，我有个生产问题，内部管理系统，使用的是Oracle数据库，按月分表，该表每天新增近6W的数据，目前共有1亿的数据量。现在的问题是，业务每天都需要查这个表进行对账，查询速度很慢，每次慢的适合，我们就重建索引速度就快一点，过一段时间又会变慢。最要命的事，这些数据有一个归属人的字段，如果某个人换部门或离职，这部分历史数据都要归宿新人，涉及历史数据的修改。 之前通过归档历史表，处理查询慢的问题，发现还没重建索引收益高，就没修改了。但是交易归属人就比较麻烦，一次变更需要2～3分钟，体验很差。我目前想的解决方案是：重构历史功能，将交易表拆分成两张表，账户表，交易余额对账表和人员归属表，虽然每天6w笔数据，但大部分账户是一样的只是余额不一样。这样查询的话，每次需要关联3张表。如果真的这样实施，需要修改很多中间表的洗数流程。面对目前的数据量，我这种方案可行么？还有更好的修改方案么？ 怕自己盲目修改后，和之前的查询修改性能差不多，就白忙活了</div>2020-04-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/81/e6/6cafed37.jpg" width="30px"><span>旅途</span> 👍（6） 💬（3）<div>老师 问几个问题
1.用户Id的根据性别的0,1,这样分表为什么会造成热点问题,只看到了分表数据可能不均匀?
2.使用分表映射表,这种如果要修改映射是怎么做的呢?是直接修改表记录还是修改代码,在生成的时候让他改变?</div>2020-05-04</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTJIocn8OMjfSGqyeSJEV3ID2rquLR0S6xo0ibdNYQgzicib6L6VlqWjhgxOqD2iaicX1KhbWXWCsmBTskA/132" width="30px"><span>虚竹</span> 👍（6） 💬（7）<div>老师好，订单id总共18位，10-14位放用户id的后几位，当用户要查询自己的所有订单时怎么查呢？这里没太明白</div>2020-03-31</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/c6/00/683bb4f0.jpg" width="30px"><span>正在减肥的胖籽。</span> 👍（6） 💬（1）<div>老师您好，有几个问题需要请教你下：
1.运营后台查询数据，肯定就是查询很多数据，不止是单个用户的数据。京东怎么去处理运营后台的数据呢?是把数据同步到ES中还是？</div>2020-03-31</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1d/3f/5c/ed0f0836.jpg" width="30px"><span>gfgf</span> 👍（4） 💬（1）<div>用户id和订单id关联这块，订单中取用户id的几位来做分区分表的依据，这个做法是否会造成数据量的不均衡；
看到个人淘宝订单是嵌入了用户id的后几位，但是京东订单没有发现规律，这块能否请老师以淘宝和京东订单为例，做一个更深入的介绍</div>2020-04-01</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/b8/78/2828195b.jpg" width="30px"><span>隰有荷</span> 👍（3） 💬（1）<div>是否可以采用mycat中间件的方式去实现分表，让代码使用过程中不感知分表带来的变化呢？</div>2020-05-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/7c/45/416fe519.jpg" width="30px"><span>Cha</span> 👍（2） 💬（3）<div>老师，请教一个问题。我看网上分库分表，有的说要2的N次方，没想明白是怎么个缘故。</div>2020-06-24</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTJbh5FQajwKhNlMrkoSklPpOXBtEYXCLvuWibhfWIS9QxHWDqzhEHJzEdmtUiaiaqFjfpsr2LwgNGpbQ/132" width="30px"><span>Geek_q29f6t</span> 👍（1） 💬（1）<div>如果用户ID使用的是guid的话，是否就不能用哈希分片算法了呢？</div>2020-05-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/5e/f0/fab69114.jpg" width="30px"><span>StopLiu</span> 👍（1） 💬（1）<div>按时间范围分片后，例如每月一个分片，但如果用户查询时想要3月15-4月15这种，就会跨月查询，这种怎么解决？</div>2020-04-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/9d/a4/e481ae48.jpg" width="30px"><span>lesserror</span> 👍（0） 💬（1）<div>老师，您说的这句话：“选择 Sharding Key 的时候，一定要能兼容业务最常用的查询条件，让查询尽量落在一个分片中。”，查询都落在一个分片中了，那不是访问压力更大了嘛？</div>2020-05-30</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/56/65/22a37a8e.jpg" width="30px"><span>Yezhiwei</span> 👍（0） 💬（1）<div>TiDB是否可以代替 MySQL 解决大数据量的问题，同时又能满足金融级别的事物问题哈？</div>2020-04-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/36/d2/c7357723.jpg" width="30px"><span>发条橙子 。</span> 👍（0） 💬（1）<div>老师 是直接用完整的用户id做哈希分片 还是那四位做哈希分片</div>2020-04-03</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/54/9a/76c0af70.jpg" width="30px"><span>每天晒白牙</span> 👍（35） 💬（1）<div>分库分表的原则
能不拆就不拆，能少拆就少拆

分库分表的目的
1.数据量大查询慢的问题
解决查询慢就是减少每次查询的数据量，即分表可以解决该问题
2.应对高并发的问题
一个数据库实例撑不住就分散到多个实例中去，即分库可以解决

概括就是数据量大就分表，高并发就分库

如何选择 sharding key?
这是分表的依据，选择要考虑的因素取决于业务如何访问数据，让查询尽量落到一个分片中。如果分片无法兼容查询，可以把数据同步到其他存储中，供查询

常见的分片算法
1.范围分片
对查询友好，适合并发量不大的场景。但容易产生热点数据
2.哈希分片
比较均匀
3.查表法
灵活，性能差因为多了一次查表

实例案例
订单表分库分表
一般按用户id分，采用哈希分片算法。为了支持按订单号查询，可以把用户id的后几位放到订单号中</div>2020-04-01</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/ee/bb/7afd6824.jpg" width="30px"><span>闫冬</span> 👍（5） 💬（3）<div>分表分库的原则，能通过其他方式优化的就不去分库分表，一来容易出错二来增加了系统的复杂度
根据不同的场景原则分库还是分表
如果是数据量大则分表 如果并发量大则分库
分表又分水平分表和垂直分表
垂直分表主要应用于当表的字段过多时，讲常用的字段分到一个表 不常用的分到一个表

水平分表比较复杂
可以按时间划分 也可以哈希 取模
时间划分比较适用于 经常按时段 热度没那么高的场景 因为如果有热点数据会造成分布不均衡
哈希 取模主要应用于按某个字段分表 分布比较均匀 但是范围查找又会有问题 可以通过冗余表来实现

异构表 相当于索引表 可以人为的调整 灵活 但是性能没有 哈希或取模快

有一个小技巧 就是订单号可以隐藏一些信息 这样避免一些场景的局限性</div>2020-04-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/51/86/b5fd8dd8.jpg" width="30px"><span>建强</span> 👍（1） 💬（0）<div>思考题，和订单有外键关联的表也可以采用查表法来处理，单独搞一张表，里面存储外键ID和对应的分片信息，这样查询时，有外键的表在关联订单表时，需要多关联这张中间表。</div>2022-01-02</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1c/c8/7b/153181d7.jpg" width="30px"><span>夜辉</span> 👍（1） 💬（0）<div>老师讲了数据分片
并没有讲集群方案，例如MySQL Cluster
能详细介绍下嘛？</div>2021-04-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/16/5b/83a35681.jpg" width="30px"><span>Monday</span> 👍（1） 💬（0）<div>老师的题目，正中下怀啊。</div>2020-08-01</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/57/4f/6fb51ff1.jpg" width="30px"><span>奕</span> 👍（1） 💬（0）<div>分库分表使用的场景是不一样的，分表是因为数据量比较大查询较慢才进行的，分库是因为单库的性能无法满足要求才进行的</div>2020-03-31</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/21/1d/d4c1cd2c.jpg" width="30px"><span>V</span> 👍（0） 💬（0）<div>看到后面越来越感觉方案已经落伍了，像这种海景数据的存储不说Ocenbase这种分布式数据库，Polardb这种自带分布式文件存储的数据库也是更好的选择，干嘛还分库分表呢？还不能线性扩容</div>2023-05-08</li><br/><li><img src="" width="30px"><span>勿更改任何信息</span> 👍（0） 💬（0）<div>分多少个库需要用并发量来预估，分多少表需要用数据量来预估
我们预估的时候一般单库并发和单表数据量的经验值是多大了</div>2022-12-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/2c/a9/cc/1183d71f.jpg" width="30px"><span>无</span> 👍（0） 💬（0）<div>您好！李老师。
请问用什么中间件去实现分片呐？</div>2022-12-21</li><br/>
</ul>