你好，我是吴磊。

在上一讲，我们说了应对“大表Join大表”的第一种调优思路是分而治之，也就是把一个庞大而又复杂的Shuffle Join转化为多个轻量的Broadcast Joins。这一讲，我们接着来讲第二种调优思路：负隅顽抗。

负隅顽抗指的是，当内表没法做到均匀拆分，或是外表压根就没有分区键，不能利用DPP，只能依赖Shuffle Join，去完成大表与大表的情况下，我们可以采用的调优方法和手段。这类方法比较庞杂，适用的场景各不相同。从数据分布的角度出发，我们可以把它们分两种常见的情况来讨论，分别是数据分布均匀和数据倾斜。

我们先来说说，在数据分布均匀的情况下，如何应对“大表Join大表”的计算场景。

## 数据分布均匀

在第27讲的最后，我们说过，当参与关联的大表与小表满足如下条件的时候，Shuffle Hash Join的执行效率，往往比Spark SQL默认的Shuffle Sort Merge Join更好。

- 两张表数据分布均匀。
- 内表所有数据分片，能够完全放入内存。

实际上，这个调优技巧同样适用于“大表Join大表”的场景，原因其实很简单，这两个条件与数据表本身的尺寸无关，只与其是否分布均匀有关。不过，为了确保Shuffle Hash Join计算的稳定性，我们需要特别注意上面列出的第二个条件，也就是内表所有的数据分片都能够放入内存。
<div><strong>精选留言（13）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/11/fe/a2/5252a278.jpg" width="30px"><span>对方正在输入。。。</span> 👍（5） 💬（3）<div>第一题：可以先统计每个key的条目数，然后根据条目数从小到大排序，后取其序列之中位数，然后找出比中位数大n倍，同时条目数大于一定阈值的key

第二题：老师，我觉得加盐的操作好像根本没啥用，加盐的场景适合聚合操作，但是吧，一旦有了aggregator，sortShuffule的时候已经在map端提前聚合了，也不会发生倾斜了。比如，本文的例子，解决这个倾斜的问题，我理解是不是可以事先对交易表作group然后求其sum值等，这个阶段因为会在map阶段事先聚合，所以并不会倾斜，然后再将聚合的结果和orders做join</div>2021-05-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/17/4f/db/3d589d18.jpg" width="30px"><span>ulysses</span> 👍（3） 💬（2）<div>老师想问下面一段代码，怎么能够筛选去哪些是skew的数据，哪些是even的 数据，对scala语法不太熟悉。
val skewOrderIds: Array[Int] = _
val evenOrderIds: Array[Int] = _ 
val skewTx: DataFrame = transactions.filter(array_contains(lit(skewOrderIds),$&quot;orderId&quot;))
val evenTx: DataFrame = transactions.filter(array_contains(lit(evenOrderIds),$&quot;orderId&quot;))</div>2021-08-03</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/2a/39/68/56dfc8c0.jpg" width="30px"><span>子兮</span> 👍（2） 💬（1）<div>老师，“两阶段 Shuffle”指的是，通过“加盐、Shuffle、关联、聚合”与“去盐化、Shuffle、聚合”这两个阶段的计算过程，第二阶段去盐后进行shuffle，不是仍然会把一个key 的所有值拉到一起吗？这和直接join最后的结果一样的呀？应该是去盐后不再进行shuffle类的操作这种加盐的操作才有意义，如理解有误，还请老师解答，谢谢</div>2021-11-25</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/37/d0/26975fba.jpg" width="30px"><span>西南偏北</span> 👍（1） 💬（5）<div>第一题：一般来讲，我们不会在代码一出现Join的地方就进行Key数量的统计，一般是执行任务的过程中，结合Spark WebUI上查看某个Stage中的Tasks的耗时排行，比如某个Task或某些Task的耗时是其他Task耗时的两倍以上，那我们就知道出现了数据倾斜，然后我们可以根据stage对应的代码位置来排查是哪些key出现了倾斜
第二题：如果是对数据进行分组排序这种情况，某个Key对应组的数据比较多，如果进行加盐的话，是无法保证整个组内的数据是有序的。加盐之后一组分为N组，每个组是有序的，但是最后去盐合并的时候，需要进行归并排序。</div>2021-05-22</li><br/><li><img src="" width="30px"><span>王天雨</span> 👍（1） 💬（2）<div>2、比如聚合操作是取平均数 ，就不适合二次聚合了吧</div>2021-05-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1e/f2/f5/b82f410d.jpg" width="30px"><span>Unknown element</span> 👍（0） 💬（1）<div>老师您好 这两讲介绍的优化方法好像只适用于用spark原生API开发的情况？如果是hive SQL是不是就只能通过调参来优化了？谢谢老师~</div>2022-01-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1d/0f/85/e2944235.jpg" width="30px"><span>Monster</span> 👍（0） 💬（1）<div>&#47;&#47;内表复制加盐
var saltedskewOrders = skewOrders.withColumn(“joinKey”, concat($“orderId”, lit(“_”), lit(1)))for (i &lt;- 2 to numExecutors) {saltedskewOrders = saltedskewOrders union skewOrders.withColumn(“joinKey”, concat($“orderId”, lit(“_”), lit(i)))}

对内表复制加盐这块的代码还是没太理解，老师可否再指导下？
举个例子说下，我理解的这个部分的代码实现目的：
例如order_id=12345，在外表加盐后变成：12345_1，那么内表复制加盐后也应该是：12345_1，否则join时候关联条件会关联不到。但还是没看懂这个内表复制加盐的代码逻辑是怎么实现的。求老师解答，非常感谢！</div>2022-01-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/98/4d/582d24f4.jpg" width="30px"><span>To_Drill</span> 👍（0） 💬（1）<div>老师您好，想请教下，像以排序为前提的聚合类操作（一般都会进行全局排序）如果发生数据倾斜了，在资源固定的前提下有啥有效的方法优化呢？</div>2021-11-01</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTJHUiaEqkvVd7ByrjHznN9mPqPskLUtUHdliaxq7MVDicEoWQqOB9f8w2BIdhn5AP5QGiaAhXcRdrIZ7w/132" width="30px"><span>毛聪</span> 👍（0） 💬（3）<div>1.可以将Join Keys先group by统计一下各个不同的组合的数据量，可以取出前几个数据量特别大的作为倾斜组，剩余的作为非倾斜组。
2.“两阶段Shuffle”要对内表进行“复制加盐”，这样可能会导致内表的大小变得太大，如果内表原来的大小就超过单个Executor的大小，“复制加盐”后应该会导致OOM。</div>2021-05-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/09/72/7293dd69.jpg" width="30px"><span>abuff</span> 👍（0） 💬（3）<div>加盐不应该是加在前缀吗？文章怎么写是后缀呢</div>2021-05-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/2d/1f/a2/0ac2dc38.jpg" width="30px"><span>组织灵魂 王子健</span> 👍（1） 💬（0）<div>如果还是Spark 2那么只能选择清洗数据+加盐。。。</div>2023-07-25</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1a/49/fe/48846a6d.jpg" width="30px"><span>Ebdaoli</span> 👍（0） 💬（0）<div>对于分而治之这里，我有点困惑，假设两张表都是TB级别的，表tableA的数据为（1,2,3,4,4,4,4...），表tableB的数据为（1,1,1,1,2,3,4...），sql为：select a.key, a.value from tableA inner join tableB on a.key=b.key；根据均匀的tableA和均匀的tableB进行关联，这时候，tableA的均匀key部分就是(1,2,3...) 去与tableB的均匀key部分(2,3,4...)进行关联，倾斜部分是tableA的（4,4,4,4）与tableB的（1,1,1,1)进行关联，即使是加盐也关联不上，最后再进行union 两部分结果，这时候的实际是倾斜部分无法关联上，结果为NULL，均匀部分tableA的4和tableB的1也关联不上，最终的union 这两部分的结果实际上并不是符合原始sql的结果，请磊哥帮忙解答下这种情况，谢谢！</div>2022-10-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/0a/ab/4d0cd508.jpg" width="30px"><span>你挺淘啊</span> 👍（0） 💬（0）<div>加盐的倍数是通过executor数来确认，executor数怎么确认呢？这个不是动态变化的吗？比如设置minexecutor和max值？</div>2022-07-24</li><br/>
</ul>