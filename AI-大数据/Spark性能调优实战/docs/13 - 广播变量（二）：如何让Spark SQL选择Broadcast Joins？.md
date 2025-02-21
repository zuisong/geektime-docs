你好，我是吴磊。

上一讲我们说到，在数据关联场景中，广播变量是克制Shuffle的杀手锏，用Broadcast Joins取代Shuffle Joins可以大幅提升执行性能。但是，很多同学只会使用默认的广播变量，不会去调优。那么，我们该怎么保证Spark在运行时优先选择Broadcast Joins策略呢？

今天这一讲，我就围绕着数据关联场景，从配置项和开发API两个方面，帮你梳理出两类调优手段，让你能够游刃有余地运用广播变量。

## 利用配置项强制广播

我们先来从配置项的角度说一说，有哪些办法可以让Spark优先选择Broadcast Joins。在Spark SQL配置项那一讲，我们提到过spark.sql.autoBroadcastJoinThreshold这个配置项。它的设置值是存储大小，默认是10MB。它的含义是，**对于参与Join的两张表来说，任意一张表的尺寸小于10MB，Spark就在运行时采用Broadcast Joins的实现方式去做数据关联。**另外，AQE在运行时尝试动态调整Join策略时，也是基于这个参数来判定过滤后的数据表是否足够小，从而把原本的Shuffle Joins调整为Broadcast Joins。
<div><strong>精选留言（18）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/10/20/d6/b9513db0.jpg" width="30px"><span>kingcall</span> 👍（25） 💬（3）<div>第一题：可以参考JoinStrategyHint.scala 
    BROADCAST,
    SHUFFLE_MERGE,
    SHUFFLE_HASH,
    SHUFFLE_REPLICATE_NL
第二题:本质上是一样的，sql 的broadcast返回值是一个Dataset[T]，而sparkContext.broadcast的返回值是一个Broadcast[T] 类型值，需要调用value方法，才能返回被广播出去的变量,所以二者在使用的使用的体现形式上，sparkContext.broadcast 需要你调用一次value 方法才能和其他DF 进行join,下面提供一个demo 进行说明

    import org.apache.spark.sql.functions.broadcast

    val transactionsDF: DataFrame = sparksession.range(100).toDF(&quot;userID&quot;)
    val userDF: DataFrame = sparksession.range(10, 20).toDF(&quot;userID&quot;)

    val bcUserDF = broadcast(userDF)
    val bcUserDF2 = sparkContext.broadcast(userDF)
    val dataFrame = transactionsDF.join(bcUserDF, Seq(&quot;userID&quot;), &quot;inner&quot;)
    dataFrame.show()
    val dataFrame2 = transactionsDF.join(bcUserDF2.value, Seq(&quot;userID&quot;), &quot;inner&quot;)
    dataFrame2.show()
</div>2021-04-12</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTIiaeebUYxl7e4jicPshDRKMbiculHUjKgZZ2ygDibn2S7bbsjeqYIdsEUdVyoryKNa43ZGnDQmWjv3ibQ/132" width="30px"><span>Geek_d794f8</span> 👍（19） 💬（5）<div>老师我做了一个测试，我的表数据是parquet存储，snappy压缩的，磁盘的存储大小为133.4M。我将广播变量的阈值调到了134M，它却可以自动广播；当我将阈值调到132M，则不会自动广播。
我用老师的方法做了一个数据在内存展开的预估，大概1000M左右，那么为什么我按照磁盘的大小设定广播阈值，它能够广播呢？</div>2021-05-18</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/PiajxSqBRaELOB7pvNfq404zOrBt7OfibficJmfaTHbd14w0Om7VRUakQWnEzmbbpJHGTmRYp0ibA31oJAZUVruatA/132" width="30px"><span>YJ</span> 👍（16） 💬（3）<div>老师，我有一个问题。 
bigTableA.Join(broadcast(smallTable), ...);
bigTableB.Join(broadsast(smallTable), ...);
bigTableA.Join(bigTableB, ...);
这里 广播了的smallTable 会被第二个join重用吗？ 还是说会被广播两次？</div>2021-04-16</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1e/f5/9a/63dc81a2.jpg" width="30px"><span>Geek1185</span> 👍（12） 💬（3）<div>为什么left join的时候不能广播左边的小表呢？几百行的表左连接几亿行的表（业务上要求即便没关联上也要保留左表的记录）。
就像为什么left join时，左表在on的谓词不能下推？
我不太明白，希望老师解答</div>2021-08-30</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/29/90/99/24cccca5.jpg" width="30px"><span>周俊</span> 👍（5） 💬（1）<div>老师，假设我有16张表需要连接，其余15张都是小表，如果我将15张小表都做成广播变量，假设他们的总数据量超过了8G，是不是会直接OOM呀，还是说只要每一个广播变量不超过8g,就不会有问题。</div>2021-08-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/ea/23/508f71e3.jpg" width="30px"><span>Jefitar</span> 👍（3） 💬（1）<div>老师，有个问题，字符串“abcd”只需要消耗 4 个字节，为什么JVM 在堆内存储这 4 个字符串总共需要消耗 48 个字节？</div>2021-04-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1e/f2/f5/b82f410d.jpg" width="30px"><span>Unknown element</span> 👍（2） 💬（1）<div>老师您好 请问
val plan = df.queryExecution.logicalval estimated: BigInt = spark.sessionState.executePlan(plan).optimizedPlan.stats.sizeInBytes
这个查看内存占用的方法是在哪里看到的呢？我在官方文档 
https:&#47;&#47;spark.apache.org&#47;docs&#47;2.4.0&#47;api&#47;scala&#47;index.html#org.apache.spark.sql.DataFrameNaFunctions 里把这些方法都搜了一遍没有搜到QAQ</div>2022-01-06</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1b/76/62/74e6d2d1.jpg" width="30px"><span>笨小孩</span> 👍（2） 💬（1）<div>老师你好  在SparkSql中使用类似with  as  这样的语法  会自动广播这张表嘛</div>2021-05-25</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/25/35/cf/aa4f9c65.jpg" width="30px"><span>魏海霞</span> 👍（1） 💬（2）<div>老师您好，用sparksql开发，遇到一个写了hint也不走broadcast的情况。具体情况是这样的，A表是个大表,有20多亿条记录，b,c,d都是小表，表就几个字段，数据最多也就3000多条，select &#47;*+ broadcast(b,c,d) from a join b jion c left join d
执行计划里b c都用的是BroadcastHashJOIN,d表是SortMergeJoin。d表不走bhj的原因大概是什么？能给个思路吗？</div>2021-09-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/a3/f2/ab8c5183.jpg" width="30px"><span>Sampson</span> 👍（0） 💬（1）<div>磊哥你好 ，请教一下，我在我的任务中设置的如下的参数提交Spark任务，
--master yarn --deploy-mode cluster --num-executors 20 --executor-cores 1 --executor-memory 5G --driver-memory 2G  --conf spark.yarn.executor.memoryOverhead=2048M --conf spark.sql.shuffle.partitions=30 --conf spark.default.parallelism=30 --conf spark.sql.autoBroadcastJoinThreshold=1024 

按照上文中讲到的我设置了广播变量的阀值是 1024 = 1G ，但是看任务运行中的日志 

storage.BlockManagerInfo: Added broadcast_4_piece0 in memory on miai7:38123 (size: 14.5 KB, free: 2.5 GB)
storage.BlockManagerInfo: Added broadcast_4_piece0 in memory on miai9:38938 (size: 14.5 KB, free: 2.5 GB)
storage.BlockManagerInfo: Added broadcast_4_piece0 in memory on miai5:39487 (size: 14.5 KB, free: 2.5 GB)
storage.BlockManagerInfo: Added broadcast_4_piece0 in memory on miai7:46429 (size: 14.5 KB, free: 2.5 GB)
storage.BlockManagerInfo: Added broadcast_4_piece0 in memory on miai5:41456 (size: 14.5 KB, free: 2.5 GB)
storage.BlockManagerInfo: Added broadcast_4_piece0 in memory on miai7:40246 (size: 14.5 KB, free: 2.5 GB)
storage.BlockManagerInfo: Added broadcast_4_piece0 in memory on miai5:45320 (size: 14.5 KB, free: 2.5 GB)
storage.BlockManagerInfo: Added broadcast_4_piece0 in memory on miai4:41769 (size: 14.5 KB, free: 2.5 GB)
storage.BlockManagerInfo: Added broadcast_4_piece0 in memory on miai4:38896 (size: 14.5 KB, free: 2.5 GB)
storage.BlockManagerInfo: Added broadcast_4_piece0 in memory on miai4:35351 (size: 14.5 KB, free: 2.5 GB)

并不是我设置的1G呀 ，这是为什么呢 ？

</div>2022-01-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1e/65/0f/7b9f27f2.jpg" width="30px"><span>猿鸽君</span> 👍（0） 💬（1）<div>老师好。我们spark是2.2.0，sparksql是2.11。我想模拟读取 Spark SQL 执行计划的统计数据时。在调用stats时却需要传一个SQLConf类型的参数。请问这是版本的问题吗？有什么替代的方法？感谢</div>2021-08-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/97/62/1a2d7825.jpg" width="30px"><span>臻果爸爸</span> 👍（0） 💬（1）<div>spark sql执行时，有一个task一直running，但是执行耗时等sparkui参数都为0，只有gc时间一直在增加，想问下这个怎么排查？</div>2021-07-06</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/DYAIOgq83errHypG6kuO0V0bRwp74rm8srjoQ4zXUBNNLMcY19uNdz8Ea3rOFuBJibXMHWePMwBYpGsyyxiav0ibw/132" width="30px"><span>闯闯</span> 👍（0） 💬（1）<div>老师有个疑问，看了您的文章后，动手试了下：
df.queryExecution.optimizedPlan.stats.sizeInBytes
这段代码也是能够获取统计信息的。这说明是不是可以简化呢。看了源码发现，这个例子跟您的例子调用 optimizedPlan 是同一段代码</div>2021-06-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/18/fb/78/dc5a1035.jpg" width="30px"><span>Geek_01eb83</span> 👍（0） 💬（3）<div>老师，您好！请教一个问题，最近用DataFrame编写spark程序，程序中通过sqlContext.sql()的方式处理Hive上的数据，发现速度很慢（整个程序很长，用了很多次sqlContext.sql()，并且注册了临时表）。最后在每一步的sqlContext.sql()语句后面加上了count（也即是action算子），其他没有改动，这样整个程序快了很多。想麻烦问下这是什么原因？</div>2021-05-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/51/8b/29ed1c41.jpg" width="30px"><span>耳东</span> 👍（0） 💬（2）<div>在左连接（Left Outer Join）中，我们只能广播右表；在右连接（Right Outer Join）中，我们只能广播左表。  这段的意思是指在 left outer join时 大表放左边 ，小表放右边吗 ？为什么？</div>2021-04-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/21/26/db/27724a6f.jpg" width="30px"><span>辰</span> 👍（0） 💬（1）<div>Hint好像是spark2.4版本之后才会有的吧，我公司版本是2.2，但是我之前使用broadcast不管用，然后试了一下hint,居然生效了</div>2021-04-16</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/27/7b/2d/6ba4a75a.jpg" width="30px"><span>🦅⃒⃘⃤ Shean</span> 👍（2） 💬（0）<div>老师，你好，请问optimizedPlan.stats.sizeInBytes展示的内存时数据集大小跟webui的storage里显示的RDD大小是一回事吗，我用sizeInBytes算出的数据集大小约是3.7G，webui显示这个RDD是2.8G</div>2023-02-14</li><br/><li><img src="" width="30px"><span>Horse_Lion</span> 👍（0） 💬（0）<div>老师，请问一下，在调整autobroadcast的阈值大小时，分配给driver的内存也要同步调整才可以吧？分布式数据集需要收集到driver端才继续分发操作</div>2023-01-31</li><br/>
</ul>