你好，我是吴磊。

在数据分析领域，数据关联可以说是最常见的计算场景了。因为使用的频率很高，所以Spark为我们准备了非常丰富的关联形式，包括Inner Join、Left Join、Right Join、Anti Join、Semi Join等等。

搞懂不同关联形式的区别与作用，可以让我们快速地实现业务逻辑。不过，这只是基础，要想提高数据关联场景下Spark应用的执行性能，更为关键的是我们要能够深入理解Join的实现原理。

所以今天这一讲，我们先来说说，单机环境中Join都有哪几种实现方式，它们的优劣势分别是什么。理解了这些实现方式，我们再结合它们一起探讨，分布式计算环境中Spark都支持哪些Join策略。对于不同的Join策略，Spark是怎么做取舍的。

## Join的实现方式详解

到目前为止，数据关联总共有3种Join实现方式。按照出现的时间顺序，分别是嵌套循环连接（NLJ，Nested Loop Join ）、排序归并连接（SMJ，Shuffle Sort Merge Join）和哈希连接（HJ，Hash Join）。接下来，我们就借助一个数据关联的场景，来分别说一说这3种Join实现方式的工作原理。

假设，现在有事实表orders和维度表users。其中，users表存储用户属性信息，orders记录着用户的每一笔交易。两张表的Schema如下：
<div><strong>精选留言（18）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/17/6f/33/8a26a19a.jpg" width="30px"><span>louis</span> 👍（11） 💬（2）<div>SHJ的第二个条件，“内表数据分片的平均大小要小于广播变量阈值”。
这里为什么是广播变量阈值，这里不涉及广播啊？不应该是内表的每一个数据分片都恰好放入执行内存中。</div>2021-08-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/17/df/e5/65e37812.jpg" width="30px"><span>快跑</span> 👍（11） 💬（2）<div>老师你好，产生了几个疑问，请帮忙看看我理解的对么
1、从MapReduce阶段来看JOIN，带Shuffle的Join应该都发生在Reduce阶段？

2、经过Shuffle后的数据不就已经是排序的么，这样子使用SMJ是不是比SHJ少了Hash计算，也减少构建Hash的内存开销。

3、不等值连接的情况，BNLJ不生效的时候，采用CPJ策略时候，JOIN发生在Reduce阶段？ 这个时候数据不都分散在各个节点么。 其中一个节点的数据怎么跟其他节点的数据比较呢。
这个时候不仅仅是数据逻辑上要Nested Loop。就连数据也需要通过网络挨个节点传输一遍么</div>2021-05-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/20/d6/b9513db0.jpg" width="30px"><span>kingcall</span> 👍（7） 💬（1）<div>回答：
问题1：个人觉得SMJ 就是用在两张大表上的关联才有意思啊，也就是事实表 Join 事实表，但是这里要求是等值关联，如果是不等值关联就只能CPJ
问题2：可以分情况讨论一下，但是肯定是可以实现的
    1. != 这样的关联，Sort Merge Join 和 Hash Join 都是不划算的，但是是可以实现的。
    2. 大于等于、小于等于 、大于 、小于 Sort Merge Join 还是有可取之处的，但是还是考虑到了排序的成本，但是这个地方有一个问题那就是我们的shuffle输出的数据的本身就是有序的啊，所以我觉得 Sort Merge Join 是可以的，Hash Join 就算了，其实可以看出来hash 只适合等值，这是取决于hash 本身的特点的。</div>2021-05-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/98/4d/582d24f4.jpg" width="30px"><span>To_Drill</span> 👍（6） 💬（1）<div>老师您好，有个疑问想请教下，如果选择了SMJ，那么在map端shuffle的输出文件中是按partitionID和key排序的，但是map端不应该只是局部数据的排序嘛，当reduce端拉取各个输出文件的时候还是会做一次全局排序（粒度为partition）的吧？如果是这样的话那么map端的排序只是加快了后续reduce端全局排序的效率，而不是map端排序了之后reduce端就不需要排序了是吧？</div>2021-10-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/a2/4b/b72f724f.jpg" width="30px"><span>zxk</span> 👍（5） 💬（2）<div>1. 可以对 Sort Merge Join 做一个变种，例如一个表排序，一个表不排序，不排序的表作为驱动表，排序的表可以通过二分查找等方式快速定位驱动表的 Join Key。
2. 也可以强行实现，但 Sort Merge Join 方面的排序就会变得毫无意义，同时 Sort Merge Join、Hash Join 的时间复杂度也并未降低，反而带来了额外的排序开销与内存开销。</div>2021-05-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/d4/78/66b3f2a2.jpg" width="30px"><span>斯盖丸</span> 👍（2） 💬（6）<div>老师一般SQL的教程里都是join的优化方法之一是小表join大表，但我看Spark里你都是大表join小表，在大数据里谁join谁要紧吗，感觉好像无所谓？</div>2021-05-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/21/26/db/27724a6f.jpg" width="30px"><span>辰</span> 👍（1） 💬（1）<div>老师，斯盖丸同学的大表join小表，在spark中，大表作为驱动表放在左边，那和放在右边有效率影响吗？还是不成文的规范，第二点，在hive中，小表是放在左边的，如果足够小的话，hive会自动把小表放进内存中，相当于广播变量了</div>2021-05-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/25/0b/aa/09c1215f.jpg" width="30px"><span>Sansi</span> 👍（1） 💬（1）<div>1.两张事实表最好的等值连接方式就是smj，可以让map端输出的时候先进行排序，reduce拉取数据的时候就可以对两个表的多个数据流进行join操作
2可以强行使用smj和hj，但是这样并没有意义，因为最后join还是m*n的复杂度(当时如果是大于或者小于的连接方式，在进行连接的可以优化一下)，而smj会带来额外的排序开销，hj要求内存能够放得下并且需要构建hash表</div>2021-05-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/2b/54/d1/d548f376.jpg" width="30px"><span>七夏、</span> 👍（0） 💬（2）<div>老师您好，有个问题需要您答惑下：
关于spark sql 中的广播机制，spark是会将满足条件的原表广播还是过滤后的结果表呢？ 
比如 关联 A表 A的大小为210M 但是广播机制是以hdfs 200M大小为阈值的，这个时候是不会被广播的，那如果我在A表做了 where 条件后 过滤后的A表只有120M，这个时候会被广播么？</div>2021-11-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/25/87/f6/bc199560.jpg" width="30px"><span>天翼</span> 👍（0） 💬（2）<div>请教一个问题，主动扫描的作为外表，被动参与扫描的表叫做内表，主动与被动是怎么区分的呢？</div>2021-05-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/d4/78/66b3f2a2.jpg" width="30px"><span>斯盖丸</span> 👍（0） 💬（1）<div>老师，问个生产上的问题，我把autoBroadcastThreshold值调到了3g，然后就遇到了spark.driver.maxResultSize超出最大值的错误。该值默认1g，我调到了5g，已经大于autoBroadcastThreshold的3g了，可为什么还报错，请问生产上这两个参数的最佳实践该怎么互相指定呢？</div>2021-05-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/37/d0/26975fba.jpg" width="30px"><span>西南偏北</span> 👍（0） 💬（1）<div>第二题，如果使用SMJ实现不等值Join，比如在大于或小于的关联条件下，排序还是有些用处的，因为拿一个表的Join key去另一个表扫描的时候，遍历到不满足条件的记录时，就可以不用继续遍历了。但是如果不排序，每次都是无脑全部遍历，虽然在计算时间复杂度的时候可能还是一样的，但是，按概率来讲，多数时候，实际的遍历记录是不一样的，还是有性能提升的。</div>2021-05-16</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/1d/22/f04cea4c.jpg" width="30px"><span>Fendora范东_</span> 👍（0） 💬（1）<div>问题回答
1.等值条件时，内外表任意大小都可以用SMJ，只不过当内表比较小或者内表平均分片小于阈值时，有性能更好的BHJ与SHJ可以选择。特别是大表join大表时，不满足使用其他两个的条件，SMJ就是最优解。

大表join大表，我理解目前最好的方式就是Shuffle sort merge join

2.不等值条件可以强行用SMJ，那他的时间复杂度又变成了O(M*N)，两表前期排序也没有太大意义。</div>2021-05-12</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTJDgV2qia6eAL7Fb4egX3odViclRRwOlkfCBrjhU9lLeib90KGkIDjdddSibNVs47N90L36Brgnr6ppiag/132" width="30px"><span>ddww</span> 👍（1） 💬（0）<div>经过代码走读，发现文中有一个错误的地方，等值 Join 下，SHJ并不支持全连接（Full Outer Join），可以这样说只要是HJ都不支持全连接（Full Outer Join）。</div>2023-08-24</li><br/><li><img src="" width="30px"><span>chengshaoli</span> 👍（1） 💬（0）<div>SMJ中，如果基表有重复值，按照上述三个规则处理后，会有漏数据的情况哎</div>2023-05-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/b5/ea/e7d78a65.jpg" width="30px"><span>不犹豫～不后悔</span> 👍（0） 💬（0）<div>老师你好，我在spark3的生产中遇到一个问题，2个0行的DF进行等值join，默认开启广播，
在spark-cluster模式下运行报错: (Caused by: org.apache.spark.SparkException: Could not execute broadcast in 300 secs. You can increase the timeout for broadcasts via spark.sql.broadcastTimeout or disable broadcast join by setting spark.sql.autoBroadcastJoinThreshold to -1)
在spark3-shell yarn-client模式下中执行正常不报错, 打印结果依旧是0行。 
网上查阅2种部署模式的区别，但依旧一片茫然，能不能帮忙分析分析吗</div>2023-07-02</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/fe/01/dedbf09a.jpg" width="30px"><span>陈念念</span> 👍（0） 💬（0）<div>等值 join 的情况下，A, B 两个表根据  join key 进行分区，确保 A，B 两张表中 join key 相等的数据放到通一个分区，分区内有完整的数据进行join。 在不等值得情况下 Shuffle Nested Loop Join  分区规则是什么呀，B 表的全量数据分别拉倒 A 表的每个分区进行 Nested Loop Join 吗？</div>2022-11-04</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/21/c3/e9/8cb4e2e5.jpg" width="30px"><span>C2H4</span> 👍（0） 💬（3）<div>请教一个问题,为什么BHJ的连接类型不能是全连接呢</div>2022-05-10</li><br/>
</ul>