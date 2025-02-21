你好，我是吴磊。

DPP（Dynamic Partition Pruning，动态分区剪裁）是Spark 3.0版本中第二个引人注目的特性，它指的是在星型数仓的数据关联场景中，可以充分利用过滤之后的维度表，大幅削减事实表的数据扫描量，从整体上提升关联计算的执行性能。

今天这一讲，我们就通过一个电商场景下的例子，来说说什么是分区剪裁，什么是动态分区剪裁，它的作用、用法和注意事项，让你一次就学会怎么用好DPP。

## 分区剪裁

我们先来看这个例子。在星型（Start Schema）数仓中，我们有两张表，一张是订单表orders，另一张是用户表users。显然，订单表是事实表（Fact），而用户表是维度表（Dimension）。业务需求是统计所有头部用户贡献的营业额，并按照营业额倒序排序。那这个需求该怎么实现呢？

首先，我们来了解一下两张表的关键字段，看看查询语句应该怎么写。

```
// 订单表orders关键字段
userId, Int
itemId, Int
price, Float
quantity, Int
 
// 用户表users关键字段
id, Int
name, String
type, String //枚举值，分为头部用户和长尾用户

```

给定上述数据表，我们只需把两张表做内关联，然后分组、聚合、排序，就可以实现业务逻辑，具体的查询语句如下。

```
select (orders.price * order.quantity) as income, users.name
from orders inner join users on orders.userId = users.id
where users.type = ‘Head User’
group by users.name
order by income desc
```

看到这样的查询语句，再结合Spark SQL那几讲学到的知识，我们很快就能画出它的逻辑执行计划。
<div><strong>精选留言（17）</strong></div><ul>
<li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/DYAIOgq83eqF7eNOuMdLqsAIkvfCicD4CqrjzRhiaDGyZKCqzduC3iaogPu5wOiaDnpeUwQXC1X4RTfe6ceKO8pKhg/132" width="30px"><span>little_fly</span> 👍（12） 💬（3）<div>老师，能不能对Spark应用程序中经常遇到的一些报错，写篇分析文章？比如，类似如下的报错信息：
1. org.apache.spark.memory.SparkOutOfMemoryError: Unable to acquire 172 bytes of memory, got 0
2. ERROR cluster.YarnScheduler: Lost executor 4 on node-3: Container killed by YARN for exceeding memory limits.  5.0 GB of 5 GB physical memory used.
3. java.lang.OutOfMemoryError: No enough memory for aggregation
4. org.apache.spark.shuffle.FetchFailedException: java.lang.RuntimeException: Executor is not registered
5. ERROR shuffle.RetryingBlockFetcher: Exception while beginning fetch of 1 outstanding blocks
java.io.IOException: Failed to connect to node-2&#47;192.168.10.1:41977

等等诸如此类的报错，很多也都不是说增加资源就能解决的。希望老师能分享一下有哪些比较好的分析排错思路</div>2021-05-15</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/21/26/db/27724a6f.jpg" width="30px"><span>辰</span> 👍（8） 💬（1）<div>这个dpp限制其实蛮多的，就比如拿课件中的例子，通过user.id关联，而且这个关联应该也是大部分场景都用到的，但是的事实表居然要按userid进行分区，不管是电商项目还是其他项目，userid肯定是比较多的，比如10万个user就对应10万userid,也就对应了10万个分区，这怕不是要玩爆系统哦，不知道理解的对不对</div>2021-05-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/1d/22/f04cea4c.jpg" width="30px"><span>Fendora范东_</span> 👍（7） 💬（2）<div>有几个疑问，麻烦磊哥指点下
1.文中所写SQL，最终有3个stage,读数据的两个stage按理说是没有依赖关系的，资源足够情况下是可以并发运行的，这就和DPP运行逻辑相违背了，这块spark是怎么做的呢？
2.有没有这样一种可能:DPP生效，即维度表做了过滤查询，事实表基于维度表广播过来的hashtable再做过滤查询，这个过程比DPP不生效，即两张表并发进行过滤查询，过程还慢？
3.DPP感觉包含了AQE join策略调整。假如本来是SMJ，运行过程中维度表经过过滤小于广播阈值，变成了BHJ。</div>2021-05-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/a2/4b/b72f724f.jpg" width="30px"><span>zxk</span> 👍（4） 💬（1）<div>问题一：放弃使用 BHJ 的话，其中一个表经过裁剪过滤后，使用广播变量只广播 Join Key 而非整个表的数据，仍可以实现 DPP，但个人仍为仍需要针对广播的 Join Key 加上一个 Threshold，否则可能将 Driver 撑爆。
问题二：如果维度表的过滤条件正好是 Join key，同时也是事实表的分区目录，也可以考虑先将这个过滤条件直接推到事实表作为一个靠近数据源的 filter 条件。

有个疑问请教下老师：
1DPP 的机制就是将经过过滤后的维度表广播到事实表进行裁剪，减少扫描数据，但 Spark 怎么才知道哪个是维度表哪个是事实表？因为 Spark 一上来是不清楚表信息的，如果一开始就把事实表先扫描了，那感觉 DPP 就失去意义了，是否需要开发者共一些额外的信息？</div>2021-05-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/20/d6/b9513db0.jpg" width="30px"><span>kingcall</span> 👍（4） 💬（1）<div>回答：
问题1 Broadcast Hash Join 本身也是依赖Broadcast 来完成的，所以Broadcast 肯定是可以完成这个需求的，但是有一个问题  Broadcast Hash Join 有spark.sql.autoBroadcastJoinThreshold 这个限制条件，但是这个条件也仅仅是限制了是否自动发生Broadcast Join，所以手动Broadcast话就没这个限制了或者使用hints，所以想怎么玩就怎么玩了，不知道对不对? 但是这里依然有一个问题那就是Broadcast出去的变量过大，这也就是 Broadcast Join 为啥有一个阈值了，要是这里能有一个这样的机制就好了，首先判断能否发生PDD 优化，然后让每个executor 去主动拉去自己所需的数据就好了(满足条件的 Join Key 的key 和 value)，而不是整个Broadcast 变量。
问题2 缓存、外部存储主要是saprk 没有类似flink 的 Async IO ，但是也可以自己在map 函数中实现
</div>2021-05-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/98/4d/582d24f4.jpg" width="30px"><span>To_Drill</span> 👍（1） 💬（3）<div>老师，按照DPP的机制来看，DPP只支持内连接(inner join)不支持外连接(left&#47;right join)吧？如果是的，那就有多了个限制条件，适用场景更少了。</div>2021-12-02</li><br/><li><img src="" width="30px"><span>张守一</span> 👍（1） 💬（1）<div>老师 如果以userid作为分区字段 相比于日期等分区字段 分区过多 但id等字段又常常作为join key 这个怎么解决呢</div>2021-05-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/37/d0/26975fba.jpg" width="30px"><span>西南偏北</span> 👍（1） 💬（1）<div>可以在逻辑计划优化的时候，就直接将维表的过滤条件通过join条件传导到事实表，减少数据的扫描</div>2021-05-16</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1e/f2/f5/b82f410d.jpg" width="30px"><span>Unknown element</span> 👍（0） 💬（1）<div>老师您好，问下如果关联是left join那DPP还能生效吗？此时左表并不需要过滤，因为结果集应该保留左表所有数据
谢谢老师~</div>2022-01-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/23/85/e19f8833.jpg" width="30px"><span>tony</span> 👍（0） 💬（1）<div>其实，spark有定义rule的机制，在逻辑计划阶段自己实现query rewrite，通过一些前置的检验条件，把维表的非分区字段条件转为filter推到事实表的logical plan上。不过只能满足小数据量的场景。</div>2021-09-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/42/f3/e945e4ac.jpg" width="30px"><span>sparkjoy</span> 👍（0） 💬（1）<div>老师，DPP对于bucket有效果吗？</div>2021-08-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/1d/22/f04cea4c.jpg" width="30px"><span>Fendora范东_</span> 👍（0） 💬（1）<div>问题回答
1.只广播join key的key set，这个数据量应该是比较小的。
2.可以把join key的key set缓存到内存中。</div>2021-05-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/d4/78/66b3f2a2.jpg" width="30px"><span>斯盖丸</span> 👍（0） 💬（1）<div>老师，如果事实表的join字段有好几个，其中只有一个是分区字段，那还能享受到DPP吗？</div>2021-05-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/b4/20/c9058450.jpg" width="30px"><span>DarrenChan陈驰</span> 👍（0） 💬（0）<div>我有个疑问哈，在spark DPP机制下，可以利用维度表过滤来削减事实表的数据量，但是需要满足3个条件：1.join key必须是分区 2.必须是等值join 3.过滤后的维度表能被广播，2和3我能理解，1的条件太苛刻了，一般我们用id做join，总不能用id做分区吧？那么为什么不满足2和3就开启该机制呢，我理解把维表过滤后的join key广播出去，让事实表先过滤，哪怕不是分区裁剪，普通的谓词下推过滤后也会减少数据量啊，为什么不这么做呢？</div>2024-11-01</li><br/><li><img src="" width="30px"><span>Geek_0a679d</span> 👍（0） 💬（1）<div>我觉得这个DPP完全没有任何意义，首先用户表就不可能用user_id来分区，第二我都分区了，只要在SQL的过滤条件里增加这个分区的过滤条件为什么还要他来帮我分区剪裁</div>2024-02-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/18/47/b0/cf5529a0.jpg" width="30px"><span>ThomasG</span> 👍（0） 💬（0）<div>dpp使用条件上不局限在是否能够进行broadcastjoin 。
在参数spark.sql.optimizer.dynamicPartitionPruning.reuseBroadcastOnly=false时，如果此时判定在分区表中加入一个过滤子查询是有收益的仍然会走dpp,这里会按照过滤key对数据聚合，插入一个子查询到分区表中，另外对于join 类型上的限制是：
INNER, LEFT SEMI,LEFT OUTER (partitioned on right), or RIGHT OUTER (partitioned on left)
即对于inner ,left semi 没有限制，left outer join 分区表必须是右表  ，right out 分布表必须是左表
</div>2022-09-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/29/d8/f8/a775cde7.jpg" width="30px"><span>太阳与冰</span> 👍（0） 💬（0）<div>这个dpp我看很多数据库里面也都做了类似实现啊，比如华为的高斯db等等~</div>2022-04-20</li><br/>
</ul>