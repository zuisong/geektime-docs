你好，我是吴磊。

上一讲我们说了，Catalyst优化器的逻辑优化过程包含两个环节：逻辑计划解析和逻辑计划优化。逻辑优化的最终目的就是要把Unresolved Logical Plan从次优的Analyzed Logical Plan最终变身为执行高效的Optimized Logical Plan。

但是，逻辑优化的每一步仅仅是从逻辑上表明Spark SQL需要“做什么”，并没有从执行层面说明具体该“怎么做”。因此，为了把逻辑计划交付执行，Catalyst还需要把Optimized Logical Plan转换为物理计划。物理计划比逻辑计划更具体，它明确交代了Spark SQL的每一步具体该怎么执行。

![](https://static001.geekbang.org/resource/image/53/fd/534dd788609386c14d9e977866301dfd.jpg?wh=4629%2A1104%3Fwh%3D4629%2A1104 "物理计划阶段")

今天这一讲，我们继续追随小Q的脚步，看看它经过Catalyst的物理优化阶段之后，还会发生哪些变化。

## 优化Spark Plan

物理阶段的优化是从逻辑优化阶段输出的Optimized Logical Plan开始的，因此我们先来回顾一下小Q的原始查询和Optimized Logical Plan。

```

val userFile: String = _
val usersDf = spark.read.parquet(userFile)
usersDf.printSchema
/**
root
|-- userId: integer (nullable = true)
|-- name: string (nullable = true)
|-- age: integer (nullable = true)
|-- gender: string (nullable = true)
|-- email: string (nullable = true)
*/
val users = usersDf
.select("name", "age", "userId")
.filter($"age" < 30)
.filter($"gender".isin("M"))

val txFile: String = _
val txDf = spark.read.parquet(txFile)
txDf.printSchema
/**
root
|-- txId: integer (nullable = true)
|-- userId: integer (nullable = true)
|-- price: float (nullable = true)
|-- volume: integer (nullable = true)
*/

val result = txDF.select("price", "volume", "userId")
.join(users, Seq("userId"), "inner")
.groupBy(col("name"), col("age")).agg(sum(col("price") * col("volume")).alias("revenue"))

result.write.parquet("_")

```

两表关联的查询语句经过转换之后，得到的Optimized Logical Plan如下图所示。注意，在逻辑计划的根节点，出现了“Join Inner”字样，Catalyst优化器明确了这一步需要做内关联。但是，怎么做内关联，使用哪种Join策略来进行关联，Catalyst并没有交代清楚。因此，逻辑计划本身不具备可操作性。
<div><strong>精选留言（17）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/11/d4/78/66b3f2a2.jpg" width="30px"><span>斯盖丸</span> 👍（43） 💬（2）<div>老师看到您的回复说一个action对应一个job，可是我看Spark UI里，经常一个action被拆分成了两三个相同的job(task数量可能会有不同)，并且有时候好多job还是可以skip的。这又涉及了Spark的哪些优化机制呢？</div>2021-06-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/20/d6/b9513db0.jpg" width="30px"><span>kingcall</span> 👍（10） 💬（4）<div>回答问题：
个人认为没有必要：因为被广播出去的数据集合都很小，可以通过Hash 或者 Nested Loop 来实现，而这二者之间的区别在于
1. Hash 主要适用于等值关联
2. Nested Loop 就可以用来实现笛卡尔积或者是不等值关联
提问：
Sort Merge 个人认为是在大数据量下催生出来的一个解决方案，但是想不通为什么在大数量的情况下，&gt; 或者是&lt; 的这种关联为什么会退化成CartesianProduct，而不是SortMergeJoin
因为我觉得这个时候使用SortMergeJoin还是比CartesianProduct好的，除非是!= 这样的关联使用CartesianProduct，当然spark 可能是考虑到了排序的成本
</div>2021-05-03</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/1d/22/f04cea4c.jpg" width="30px"><span>Fendora范东_</span> 👍（5） 💬（1）<div>一、从原理和复杂度看(假设单节点大表规模m,小表规模n)
1、数据分发:
      broadcast把整个小表发送到大表数据所在节点;
      shuffle大小表按照同样的分区方式、数进行数据重新          划分。
2、join实现
    hash join小表建立hash表，大表遍历;(时间复杂度为构建hash表时间O(n)+大小表比较时间O(m)*O(1)，空间复杂依赖hash map)
    sort merge join 先排序，然后采用MergeSort中合并操作进行比较;(时间复杂度为 排序时间max{O(m*lgm),O(n*lgn)} + 大小表比较时间O(m+n)，其实时空复杂度依赖具体排序算法。。。)
    nested loop join大小表双层for循环依次比较。O(mn)

二、BSMJ分析(小表总规模N)
1.实现
   1.1小表先broadcast，所有节点再分别进行排序、合并。
   1.2小表先排序再broadcast，最后两表进行合并。
2.原因
   2.1先broadcast，再排序，最坏时相比BNLJ多了每个节点的O(N*lgN)小表排序耗时;最好时max{O(N*lgN)，O(m*lgm)}+O(M+N)不见得就一定比O(Mn)效果好。
   2.2如果先排序，那driver端就需要排序耗时O(N*lgN)，driver极有可能是整个集群的瓶颈。

磊哥看看哪里有问题没</div>2021-05-03</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/37/6f/b3337e6d.jpg" width="30px"><span>金角大王</span> 👍（3） 💬（1）<div>老师您好，请问Physical Plan 中节点前的&quot;+-&quot;号有啥特殊含义吗？</div>2021-07-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/d9/e7/45d9e964.jpg" width="30px"><span>Hiway</span> 👍（2） 💬（3）<div>老师，我觉得优化Spark Join这一步叫成优化不太好，实际上这一步是根据逻辑计划中的关系操作符一一映射成物理操作符，生成 Spark Plan。我读了源码发现其实spark plan就是physical plan。这两步理解为根据策略Strategies生成spark plan，和根据Rules优化spark plan更形象一点。</div>2021-11-07</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/37/d0/26975fba.jpg" width="30px"><span>西南偏北</span> 👍（2） 💬（1）<div>broadcast广播模式下，排序没啥必要吧，因为本身被广播的数据集就比较小，hash join和NLJ完全够用了。而且SMJ本身就是针对大表关联大表设计的join算法</div>2021-05-05</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/d9/e7/45d9e964.jpg" width="30px"><span>Hiway</span> 👍（1） 💬（4）<div>老师你好，在2.4.3中使用ShuffledHashJoin的前置条件有一个canBuildLocalHashMap，其要求就是数据大小要小于spark.sql.autoBroadcastJoinThreshold*spark.sql.shuffle.partitions，我想请教一下这里为什么需要小于Broadcast的大小*sqlshuffle的分区数呢？从ShuffledHashJoin的逻辑来看，应该不涉及到Broadcast呀</div>2021-09-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/21/63/6e/6b971571.jpg" width="30px"><span>Z宇锤锤</span> 👍（1） 💬（3）<div>Broadcast Sort Merger Join中Broadcast指的是数据分发的方式，SMB指的是Join实现机制。
Sort Merge Join的原理是将两张表的数据按照相同的分区算法，分发到各个Executor上。如果使用Broadcast传输，被广播的表会先在Executor端进行数据的拆分，拆分完成以后，所有的分区会被Collect到Driver端，再向每一个Executor分发完整数据。这使被广播的表数据即便拆分了，还是被聚合分发，浪费时间。</div>2021-05-03</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1e/f2/f5/b82f410d.jpg" width="30px"><span>Unknown element</span> 👍（0） 💬（1）<div>老师您好 想问一下我有个 hive sql 只是执行了一个 insert overwrite select a join b 的操作，spark 日志却有6个job，点进二级链接后在dag visualization中可以看到：
job0：WSCG然后sort; 
job1：WSCG然后exchange；
job2：exchange =&gt; WSCG =&gt; exchange
job3：exchange =&gt; hash aggregate =&gt;sort
job4：parallelize
job5:  parallelize
我想请教一下为什么有这么多job呢？另外在sql页面显示的是completed queries，这个query又是什么概念呢？和job是一个东西吗？谢谢老师~</div>2022-01-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/22/8e/67/afb412fb.jpg" width="30px"><span>Sam</span> 👍（0） 💬（2）<div>老师，早上好！~

本文中出现一句：“括号中数字相同的操”，这里的“操”，是值的意思吗？</div>2021-07-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/cd/90/af47197b.jpg" width="30px"><span>小人物</span> 👍（0） 💬（5）<div>老师您好，我有两个问题想请教：
1，能否通过查看物理执行计划判断哪些stage可以并行执行，并行执行是否有对应的触发前置条件？
2，能否通过查看物理执行计划判断该sql会生成的job数，如果可以该如何去阅读得到应该有几个job？</div>2021-06-06</li><br/><li><img src="" width="30px"><span>kris37</span> 👍（0） 💬（2）<div>shuffle hash join 条件并不支持 full outer join （不知道Spark3是否有支持 full outer join 的hash join 实现，FB提供的PR？），这块老师要修改下表格。</div>2021-05-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/a2/4b/b72f724f.jpg" width="30px"><span>zxk</span> 👍（0） 💬（1）<div>没必要实现 BSMJ， Shuffle 排序的目的是为了将同个 partition 的数据汇集到一起发送，而 Broadcast 本身就是对数据的全量发送，并不需要区分数据归属于哪个 partition。

提问：老师说 Tungsten 的 WSCG 会将同个 stage 内的操作捏合成一个手写代码，意思是指你合成一个函数操作么？如果是，那么跟 DAGScheduler 中的函数合并有什么区别不，毕竟 Spark SQL 最后也是转化为 Spark Core 执行的？</div>2021-05-04</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/DYAIOgq83eo2GMhevabZrjINs2TKvIeGC7TJkicNlLvqTticuM5KL8ZN80OC2CnrsUyzPcZXO4uptj4Q1S4jT2lQ/132" width="30px"><span>jerry guo</span> 👍（0） 💬（1）<div>Sort Merger Join适用于大表，大表无法broadcast，所以没有broadcast sort merge join。
</div>2021-05-04</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/oltLEqTrmHm2aJP99BK6tH56hSYps7LicOBSt518gbUKGSrpNfpuCA8snDFt3whqF7FsPPc1MKQX0bE96eTt7jA/132" width="30px"><span>KiloMeter</span> 👍（0） 💬（0）<div>我理解SMJ是用于大表跟大表之间的关联，SHJ是大表和小表之间的关联，为什么SMJ优先级会高于SHJ呢，理论上来说，shuffle完之后，如果一个节点上的这两个表中的小表足以构建hash表，那么直接用SHJ会比SMJ快吧，因为少了排序的时间</div>2023-05-04</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/74/5a/b6934700.jpg" width="30px"><span>travi</span> 👍（0） 💬（0）<div>请问：df.explain()展示的是Physical Plan, 文中的Spark Plan是通过什么工具展示出来的呢</div>2022-09-30</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/a3/f2/ab8c5183.jpg" width="30px"><span>Sampson</span> 👍（0） 💬（0）<div>磊哥，这里有个疑问请教下，在上一张Catalyst逻辑计划中逻辑计划优化阶段主要依赖AQE 等3项，那么AQE 中的join策略调整和这里的物理计划中生成Spark plan 中join策略的选择有什么异同吗 ？还是说针对的点不同 ？</div>2022-07-29</li><br/>
</ul>