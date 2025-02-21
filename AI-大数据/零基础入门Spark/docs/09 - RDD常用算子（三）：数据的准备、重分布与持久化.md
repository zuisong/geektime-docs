你好，我是吴磊。

在RDD常用算子的前两讲中，我们分别介绍了用于RDD内部转换与聚合的诸多算子，今天这一讲，我们继续来介绍表格中剩余部分的算子。

按照惯例，表格中的算子我们不会全都介绍，而是只挑选其中最常用、最具代表性的进行讲解。今天要讲的算子，我用加粗字体进行了高亮显示，你不妨先扫一眼，做到心中有数。

![图片](https://static001.geekbang.org/resource/image/4e/d3/4ebaf6b9762b2d7ba64d21d8664080d3.jpg?wh=1920x1506 "RDD算子分类表")

你可能会觉得，这些高亮显示的算子乍一看也没什么关联啊？但如果我们从数据生命周期的角度入手，给它们归归类，很容易就会发现这些算子分别隶属于生命周期的某个阶段。

![图片](https://static001.geekbang.org/resource/image/8f/cb/8fc62a1795606466f1fe391d098731cb.jpg?wh=1920x737 "数据生命周期")

结合上图，我们分别来看看每个算子所在的生命周期和它们实现的功能。

首先，在数据准备阶段，union与sample用于对不同来源的数据进行合并与拆分。

我们从左往右接着看，接下来是数据预处理环节。较为均衡的数据分布，对后面数据处理阶段提升CPU利用率更有帮助，可以整体提升执行效率。那这种均衡要怎么实现呢？没错，这时就要coalesce与repartition登场了，它们的作用就是重新调整RDD数据分布。

在数据处理完毕、计算完成之后，我们自然要对计算结果进行收集。Spark提供了两类结果收集算子，一类是像take、first、collect这样，把结果直接收集到Driver端；另一类则是直接将计算结果持久化到（分布式）文件系统，比如咱们这一讲会提到的saveAsTextFile。
<div><strong>精选留言（15）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/15/23/bb/a1a61f7c.jpg" width="30px"><span>GAC·DU</span> 👍（16） 💬（1）<div>#合并RDD
测试了三种方法，分别是union、reduce、++，并且通过调用toDebugString方法查看，显示结果是一致的，下面的代码是在spark-shell上测试的
```scala
scala&gt; val rdd1 = spark.sparkContext.parallelize(1 to 10)

scala&gt; val rdd2 = spark.sparkContext.parallelize(20 to 30)
scala&gt; val unionRDD = rdd1 union rdd2

scala&gt; unionRDD.collect
res3: Array[Int] = Array(1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30)
scala&gt; unionRDD.toDebugString
res4: String =
(16) UnionRDD[2] at union at &lt;console&gt;:27 []
 |   ParallelCollectionRDD[0] at parallelize at &lt;console&gt;:23 []
 |   ParallelCollectionRDD[1] at parallelize at &lt;console&gt;:23 []

scala&gt; val data = Seq(rdd1, rdd2)
scala&gt; data.foreach(println)
ParallelCollectionRDD[0] at parallelize at &lt;console&gt;:23
ParallelCollectionRDD[1] at parallelize at &lt;console&gt;:23
scala&gt; val reduceRDD = data.reduce(_ union _)
scala&gt; reduceRDD.collect
res6: Array[Int] = Array(1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30)
scala&gt; reduceRDD.toDebugString
res7: String =
(16) UnionRDD[3] at union at &lt;console&gt;:25 []
 |   ParallelCollectionRDD[0] at parallelize at &lt;console&gt;:23 []
 |   ParallelCollectionRDD[1] at parallelize at &lt;console&gt;:23 []

scala&gt; val addRDD = rdd1 ++ rdd2
scala&gt; addRDD.collect
res15: Array[Int] = Array(1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30)
scala&gt; addRDD.toDebugString
res16: String =
(16) UnionRDD[7] at $plus$plus at &lt;console&gt;:27 []
 |   ParallelCollectionRDD[0] at parallelize at &lt;console&gt;:23 []
 |   ParallelCollectionRDD[1] at parallelize at &lt;console&gt;:23 []
```
# coalesce 潜在隐患
repartition和coalesce相比较，repartition由于引入了shuffle机制，对数据进行打散，混洗，重新平均分配，所以repartition操作较重，但是数据分配均匀。而coalesce只是粗力度移动数据，没有平均分配的过程，会导致数据分布不均匀，在计算时出现数据倾斜。
</div>2021-09-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/2a/3a/83/74e3fabd.jpg" width="30px"><span>火炎焱燚</span> 👍（13） 💬（1）<div>老师，我这儿遇到了一个问题，不太明白，一共有100个数字，每次sample（False，0.1）理论上应该会获取10个数字，但运行几次得到的数字个数都不同，有的是8个，有的11个，这是为啥？spark中sample的原理不会精确控制个数吗？
运行代码：
&gt;&gt;&gt; rdd.sample(False,0.1).collect()
[1, 18, 23, 25, 31, 52, 59, 73, 95, 96, 97]
&gt;&gt;&gt; rdd.sample(False,0.1).collect()
[11, 12, 13, 36, 40, 50, 51, 77, 90]
&gt;&gt;&gt; rdd.sample(False,0.1).collect()
[2, 13, 21, 33, 51, 59, 73, 80, 84, 88]
&gt;&gt;&gt; rdd.sample(False,0.1).collect()
[3, 18, 41, 44, 67, 87, 89, 91]
&gt;&gt;&gt; rdd.sample(False,0.1).collect()
[35, 41, 69, 75, 87, 92, 99]
</div>2021-10-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/19/70/67/0c1359c2.jpg" width="30px"><span>qinsi</span> 👍（10） 💬（1）<div>从文中的描述来看，coalesce似乎并不能避免shuffle？极端的例子，coalesce(1)必然会把数据都放入同一个Executor里？</div>2021-09-29</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/DYAIOgq83epGTSTvn7r4ibk1PuaUrSvvLdviaLcne50jbvvfiaxKkM5SLibeP6jibA2bCCQBqETibvIvcsOhAZlwS8kQ/132" width="30px"><span>Geek_2dfa9a</span> 👍（8） 💬（3）<div>第一题
没明白考点是啥，考的是scala的语法么？
val rdd1 = sc.textFile(&quot;&quot;)
val rdd2 = sc.textFile(&quot;&quot;)
val rdd3 = sc.textFile(&quot;&quot;)
val unionRdd = rdd1.union(rdd2).union(rdd3)
val unionRdd2 = Seq(rdd1, rdd2, rdd3).reduce(_.union(_))

第二题
repartition也是通过colesce实现的，只不过repartition默认是要shuffle的，也就是说，repartition肯定是会通过哈希重分区的，
不管分区前数据分布是否均匀，分区后数据分布会比较均匀，但是colesce就未必了，colesce默认是不shuffle的，会尽量在local合并分区，
  如果colesce之前数据是分布不均匀的，那colesce之后数据分布还是不均匀的，这种情况下指定方法入参shuffle=true就解决了。
</div>2021-09-30</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTIjUDIRQ0gRictgQpjWia38qjN3pYicfzahAwbntWq93CorhjiaIOVh7j2Fj6a9WxUW85icMxF3r2Ymblg/132" width="30px"><span>Geek_038655</span> 👍（6） 💬（1）<div>collect对于大数据分析结果过大导致的OOM问题，用saveAsTextFile解决是不是过于迁就？
为什么不用foreashPartition?</div>2021-09-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/17/1f/6e/7a6788f3.jpg" width="30px"><span>爱吃猫的鱼</span> 👍（2） 💬（4）<div>coalesce 会降低同一个 stage 计算的并行度，导致 cpu 利用率不高，任务执行时间变长。我们目前有一个实现是需要将最终的结果写成单个 avro 文件，前面的转换过程可能是各种各样的，我们在最后阶段加上 repartition(1).write().format(&#39;avro&#39;).mode(&#39;overwrite&#39;).save(&#39;path&#39;)。最近发现有时前面的转换过程中有排序时，使用 repartition(1) 有时写得单文件顺序不对，使用 coalesce(1) 顺序是对的，但 coalesce(1) 有性能问题。目前想到可以 collect 到 driver 自己写 avro 文件，但可能存在以上提到的内存问题，不知道有没有更好的方案？ </div>2021-09-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1e/f2/f5/b82f410d.jpg" width="30px"><span>Unknown element</span> 👍（1） 💬（3）<div>老师我看了评论区那个关于coalesce(1，shuffle = false)的问题，您说这个时候coalesce不会引入Shuffle，但是所有操作并行度都是1，都在一个executor计算；这里我不太明白，既然数据是分布在多个节点上，又不能用shuffle，那数据是怎么被汇集到一个节点的？</div>2021-10-04</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/26/6f/4f/3cf1e9c4.jpg" width="30px"><span>钱鹏 Allen</span> 👍（1） 💬（2）<div>1. 方法一：Seq(rdd1,rdd2).reduce(_ union _) 方法二： rdd1  ++  rdd2   (高赞精简版本)
2.大数据量的情况下，相比 repartition，coalesce没有shuffle，可能会导致数据倾斜，即一个分区上有着大量的数据，而另外一个可能没有多少数据。</div>2021-10-03</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/28/3f/9d/c59c12ad.jpg" width="30px"><span>实数</span> 👍（0） 💬（1）<div>sortshuufle是不是能保证全局有序呢  第一代的hashshuffle好像是不是废弃了 ，老师有空能不能讲下bypass mergesort、unsafe、sort shuffle ，这三个确实不懂</div>2021-11-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/13/9d/0ff43179.jpg" width="30px"><span>Andy</span> 👍（0） 💬（1）<div>如前一章内存，我看过一些博客文章也没看明白，老师一讲我就理解了。本章老师和同学的评论，进一步加强了对coalesce解释(shuffle和非shuffle的区别)，如coalesce(1) shuffle是多个executer输出数据到一个executer不保证数据顺序，但运行速度快。本章第一题没达出来，看官网文档和百度也没达上来。应该是我对scala语法不熟。第二题我的答案是可能会导致分区数据不均，严重的会导致数据倾斜计算慢或内存溢出。</div>2021-11-14</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/qmdZbyxrRD5qQLKjWkmdp3PCVhwmWTcp0cs04s39pic2RcNw0nNKTDgKqedSQ54bAGWjAVSc9p4vWP8RJRKB6nA/132" width="30px"><span>冯杰</span> 👍（0） 💬（1）<div>关于coalesce，有个疑问。 按照老师的说法，coalesce会引入两种操作，一种在stage开头将数据集放在一个executor运算；一种是按数据集的存储位置参与运算，并在最后将exectuor内的分区合并。  具体选用哪种方式，好像也只能根据coalesce的参数n来判断了，但具体的逻辑是什么呢？</div>2021-10-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/04/0d/3dc5683a.jpg" width="30px"><span>柯察金</span> 👍（0） 💬（0）<div>老师，比如源头读取有 200 个并行度

是不是说 coalesce(1) 为了不 shuffle ，从一开始的源头就把并行度缩减为 1 了啊？而 repartition(1) 的时候，是有 shuffle 的过程的，所以，在 repartition 之前还是 200 个并行度，只是在 repartition 的时候，在进行 shuffle 把分区缩小

这有点能解释我之前遇到的一个问题：

就是我从数据库里面读取的数据之后，dataframe 经过一系列处理，再输出之前，count 了一把，发现过滤得只有很少的数据了，于是我 coalesce(1) 缩到一个分区了，然后就直接内存爆了。我当时百思不得其解，为啥只有很少的数据还装不到一个分区里面去，现在看起来，是不是用了 coalesce(1) 就把源头的分区也改成了 1 的缘故啊？？？</div>2024-03-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/17/3f/2e/bdeb7a0b.jpg" width="30px"><span>岁月神偷</span> 👍（0） 💬（0）<div>对于 union这个算子，如果被合并的两个RDD分区数不一致，会出现什么情况</div>2023-08-06</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/37/e2/fd/c9a48b78.jpg" width="30px"><span>北森</span> 👍（0） 💬（0）<div>老师请教下，saveAsTextFile如果全量数据都存储到磁盘文件里，不是效率处理的更慢嘛？</div>2023-07-02</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/27/f1/e4fc57a3.jpg" width="30px"><span>无隅</span> 👍（0） 💬（0）<div>老师说的太棒了</div>2022-09-11</li><br/>
</ul>