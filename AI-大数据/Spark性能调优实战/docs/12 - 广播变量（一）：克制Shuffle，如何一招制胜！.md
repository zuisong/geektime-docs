你好，我是吴磊。

在数据分析领域，数据关联（Joins）是Shuffle操作的高发区，二者如影随从。可以说，有Joins的地方，就有Shuffle。

我们说过，面对Shuffle，开发者应当“能省则省、能拖则拖”。我们已经讲过了怎么拖，拖指的就是，把应用中会引入Shuffle的操作尽可能地往后面的计算步骤去拖。那具体该怎么省呢？

在数据关联场景中，广播变量就可以轻而易举地省去Shuffle。所以今天这一讲，我们就先说一说广播变量的含义和作用，再说一说它是如何帮助开发者省去Shuffle操作的。

## 如何理解广播变量？

接下来，咱们借助一个小例子，来讲一讲广播变量的含义与作用。这个例子和Word Count有关，它可以说是分布式编程里的Hello world了，Word Count就是用来统计文件中全部单词的，你肯定已经非常熟悉了，所以，我们例子中的需求增加了一点难度，我们要对指定列表中给定的单词计数。

```
val dict = List(“spark”, “tune”)
val words = spark.sparkContext.textFile(“~/words.csv”)
val keywords = words.filter(word => dict.contains(word))
keywords.map((_, 1)).reduceByKey(_ + _).collect
```

按照这个需求，同学小A实现了如上的代码，一共有4行，我们逐一来看。第1行在Driver端给定待查单词列表dict；第2行以textFile API读取分布式文件，内容包含一列，存储的是常见的单词；第3行用列表dict中的单词过滤分布式文件内容，只保留dict中给定的单词；第4行调用reduceByKey对单词进行累加计数。
<div><strong>精选留言（25）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/25/0b/aa/09c1215f.jpg" width="30px"><span>Sansi</span> 👍（22） 💬（4）<div>1. 改成由driver获取到数据分布，然后通知各个executor之间进行拉取，这样可以利用多个executor网络，避免只有driver组装以后再一个一个发送效率过低

2.当两个需要join的数据集都很大时，使用broadcast join需要将一个很大的数据集进行网络分发多次，已经远超出了shuffle join需要传输的数据</div>2021-04-09</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTIiaeebUYxl7e4jicPshDRKMbiculHUjKgZZ2ygDibn2S7bbsjeqYIdsEUdVyoryKNa43ZGnDQmWjv3ibQ/132" width="30px"><span>Geek_d794f8</span> 👍（21） 💬（3）<div>磊哥，为什么我测试了广播rdd不行：
我写了个demo，广播rdd是报错的，代码如下：
    val userFile: String =&quot;spark-basic&#47;File&#47;csv_data.csv&quot;
    val df: DataFrame = spark.read.csv(userFile)
    val rdd = spark.sparkContext.textFile(&quot;userFile&quot;)
    val bc_df: Broadcast[RDD[String]] = spark.sparkContext.broadcast(rdd)
    bc_df.value.collect().foreach(println)

报错如下：Exception in thread &quot;main&quot; java.lang.IllegalArgumentException: requirement failed: Can not directly broadcast RDDs; instead, call collect() and broadcast the result.

然后看了一下源码：SparkContext中的broadcast方法：

def broadcast[T: ClassTag](value: T): Broadcast[T] = {
    assertNotStopped()
    require(!classOf[RDD[_]].isAssignableFrom(classTag[T].runtimeClass),
      &quot;Can not directly broadcast RDDs; instead, call collect() and broadcast the result.&quot;)
    val bc = env.broadcastManager.newBroadcast[T](value, isLocal)
    val callSite = getCallSite
    logInfo(&quot;Created broadcast &quot; + bc.id + &quot; from &quot; + callSite.shortForm)
    cleaner.foreach(_.registerBroadcastForCleanup(bc))
    bc
  }

第4行的代码显示的Can not directly broadcast RDDs
是不是我哪里不太对？</div>2021-05-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/ca/d8/b109ed85.jpg" width="30px"><span>Jack</span> 👍（6） 💬（8）<div>老师，对于第1题，看了下spark的源码，目前Broadcast只有一个实现类TorrentBroadcast，看代码的注释，这个类通过使用类似Bit-torrent协议的方法解决了Driver成为瓶颈的问题。目前Spark还会存在广播变量的数据太大造成Driver成为瓶颈的问题吗？

&#47;**
 * A BitTorrent-like implementation of [[org.apache.spark.broadcast.Broadcast]].
 *
 * The mechanism is as follows:
 *
 * The driver divides the serialized object into small chunks and
 * stores those chunks in the BlockManager of the driver.
 *
 * On each executor, the executor first attempts to fetch the object from its BlockManager. If
 * it does not exist, it then uses remote fetches to fetch the small chunks from the driver and&#47;or
 * other executors if available. Once it gets the chunks, it puts the chunks in its own
 * BlockManager, ready for other executors to fetch from.
 *
 * This prevents the driver from being the bottleneck in sending out multiple copies of the
 * broadcast data (one per executor).
 *
 * When initialized, TorrentBroadcast objects read SparkEnv.get.conf.
 *
 * @param obj object to broadcast
 * @param id A unique identifier for the broadcast variable.
 *&#47;
private[spark] class TorrentBroadcast[T: ClassTag](obj: T, id: Long)
  extends Broadcast[T](id) with Logging with Serializable {
</div>2021-04-09</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/qmdZbyxrRD5qQLKjWkmdp3PCVhwmWTcp0cs04s39pic2RcNw0nNKTDgKqedSQ54bAGWjAVSc9p4vWP8RJRKB6nA/132" width="30px"><span>冯杰</span> 👍（5） 💬（1）<div>老师你好，关于broacast join，遇到了一个特别的问题请教一下。
1、Fact(订单) 和 DIM(门店) 关联。  其中门店表量级为 3w(条数) * 10个(字段)，采用Parquet存储在Hive上，大小1M左右。
2、运行参数，并行度 = 200，Executor = 50，CPU核数 = 2，内存&#47;Executor = 6G，Drvier内存=2G。 PS：没有特别配置Broadcast 相关参数
3、执行时，有两个疑问点，不得其解
    a）Spark UI 显示，并没有执行BHJ，反而执行了 hash sort merge join。   照理，如此小的数据，应该走前者
    b）Spark UI 显示，走hash sort merge join后，shuffle阶段的内存计算大小为4MB，sort阶段的内存计算大小为6G。    为何sort完后，为膨胀的如此厉害。

</div>2021-06-10</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTIiaeebUYxl7e4jicPshDRKMbiculHUjKgZZ2ygDibn2S7bbsjeqYIdsEUdVyoryKNa43ZGnDQmWjv3ibQ/132" width="30px"><span>Geek_d794f8</span> 👍（5） 💬（1）<div>老师有两个问题请教一下：
1.文中提到两个表join，两个表数据量相差很大呀，为什么他们的的分区数是一致的，而且分区数不是根据hadoop的切片规则去划分的吗？
2.广播join不是默认开启的吗，好像小表默认10M；还需像文中代码val bcUserDF = broadcast(userDF)这样声明吗？
希望得到您的指导，多谢！</div>2021-04-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/d4/78/66b3f2a2.jpg" width="30px"><span>斯盖丸</span> 👍（4） 💬（5）<div>老师我生产中为啥从没有遇到过10000并行度那么大的stage，可能我公司比较小吧，集群最多才100多个核，多数时才几百个任务，最多时也才2000多个任务。这健康吗？</div>2021-05-05</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/d4/78/66b3f2a2.jpg" width="30px"><span>斯盖丸</span> 👍（2） 💬（1）<div>原来小表和大表join是节省了大表的shuffle，不然大表只能根据join的列在所有机器上重新分布一遍，现在懂了</div>2021-04-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/29/96/17/200c21f0.jpg" width="30px"><span>狗哭</span> 👍（1） 💬（3）<div>select * from
(select id from table1) a -- 结果很大
left join
(select id from table2) b -- 结果很小
on t1.id = t2.id;
老师请教下，这种情况b表会广播吗？如果不会怎么处理能让其广播出去呢</div>2021-10-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/2b/2d/aa/e33e9edd.jpg" width="30px"><span>陌生的心酸</span> 👍（0） 💬（2）<div>1&gt;.当数据量比较大，对数据进行广播后，同时还要接受各个Executor的中间结果上报，状态管理，导致网络繁忙，继而会发生分发任务到Executor产生失败

2&gt; 两个大表【超过广播变量的阈值参数设置】进行join，数据需要分发多次，效率不佳</div>2022-02-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/2a/39/68/56dfc8c0.jpg" width="30px"><span>子兮</span> 👍（0） 💬（1）<div>老师您好，在整个应用资源较为紧张，数据量较大的情况下：spark core计算过程中，生成一个较大的RDD , 它被引用一次，但我还是对它persist(disk)，我在用完并且动作算子后，立刻对它进行了释放unpersist，这样操作是否能加快spark 对这个rdd 的清理，加快内存的释放，缓解内存压力？如果是persist(memory and disk)，用完并且在动作算子后立即释放unpersist，是否能缓解内存压力？如果不persist，用完并且在动作算子后立即释放unpersist，是否能缓解内存压力？ 文字有些长，希望没给老师造成困扰，谢谢老师</div>2021-11-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/2a/39/68/56dfc8c0.jpg" width="30px"><span>子兮</span> 👍（0） 💬（1）<div>1 老师，您好，spark core计算过程中，需要频繁的使用broadCast 操作， 这样累计几次后driver 端内存会很有压力，怎样设置参数或者手动清除之前用来broadCast 的数据？谢谢老师
2 老师这个课程的微信交流群怎么添加呢？期待加入学习

</div>2021-11-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/2a/39/68/56dfc8c0.jpg" width="30px"><span>子兮</span> 👍（0） 💬（1）<div>老师, 课程里您讲了内连接左右左右两表的连接过程，您能否再讲一下左外连接leftoutjoin 的呢？对shuffle过程不太清晰，谢谢老师</div>2021-11-02</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/4f/d5/1666b7d0.jpg" width="30px"><span>zhongmin</span> 👍（0） 💬（1）<div>吴老师，问个问题，在广播分布式变量的时候，如果变量的内容发生改变，是怎么去做变量的同步和更新呢？</div>2021-09-06</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/17/11/20/9f31c4f4.jpg" width="30px"><span>wow_xiaodi</span> 👍（0） 💬（1）<div>老师对于这节有一些问题：
(1)executor对于待回传driver端的广播数据集是先存在内存还是落地硬盘呢？
(2)由executor来处理分片再回传，可能分片需要进行一定的计算再由driver汇总广播，那么如果是无需计算的原始分片呢，driver可否亲自操刀读取所有原始分片直接汇总再分发呢，感觉这样可以节省网络开销？</div>2021-08-01</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1d/d3/82/c3e57eb3.jpg" width="30px"><span>xuchuan</span> 👍（0） 💬（1）<div>2.多个大表join应该就没法用广播解决，这个延伸一个问题，以电商为例，即席查询应该还要有数仓吧，这不是spark的主要覆盖范畴。</div>2021-05-18</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTIiaeebUYxl7e4jicPshDRKMbiculHUjKgZZ2ygDibn2S7bbsjeqYIdsEUdVyoryKNa43ZGnDQmWjv3ibQ/132" width="30px"><span>Geek_d794f8</span> 👍（0） 💬（3）<div>磊哥，为什么dataframe可以广播，而rdd不能广播。dataframe也不存数据呀，它只是比rdd 多了schema信息。这块不太理解。</div>2021-05-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/95/46/1cd5ab5f.jpg" width="30px"><span>弦断觅知音</span> 👍（0） 💬（4）<div>请教老师第一个问题： 用什么方式 改为由driver获取到数据分布，然后通知各个executor之间进行拉取？</div>2021-05-07</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1f/9b/3b/dc3f819f.jpg" width="30px"><span>小灵芝</span> 👍（0） 💬（0）<div>“第一步就是对参与关联的左右表分别进行 Shuffle，Shuffle 的分区规则是先对 Join keys 计算哈希值，再把哈希值对分区数取模。由于左右表的分区数是一致的，因此 Shuffle 过后，一定能够保证 userID 相同的交易记录和用户数据坐落在同一个 Executors 内。”

老师请问什么叫吧哈希值对分区取模？取模是什么意思？

提前感谢~</div>2021-04-30</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/76/5a/4393d800.jpg" width="30px"><span>七</span> 👍（0） 💬（1）<div>老师，问一下 从hdfs加载parquet文件时，例如spark.read.parquet(&quot;xx&quot;)，是怎么确定分区数的呢？阅读源码DataFrameReader没有找到相关配置，希望老师给指条路，解答一下。</div>2021-04-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/21/26/db/27724a6f.jpg" width="30px"><span>辰</span> 👍（0） 💬（2）<div>老师，您好，问题一和问题二有没有一种矛盾在里面，问题一是数据量大，如何使用广播，问题二我知道的是，当join的表数据量都很大时就不适合广播了，一是因为网络开销，二是因为executor内存不够大不足以存储大数据量，还有老师，能不能说一下广播的阈值多少合适，这个和其他的参数也有关系，比如整体的参数如何设置，能不能讲一下，executor数量，core的数量，分区大小以及内存大小设置</div>2021-04-15</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/ca/d8/b109ed85.jpg" width="30px"><span>Jack</span> 👍（0） 💬（4）<div>老师，第2题@Bennan的回答有疑惑。为什么当两个需要join的数据集都很大时，broadcast join会超出shuffle join需要传输的数据。
假设有A，B两表，各自大小都是100G，有4个executor，每个executor有4个task对应4个分区，总共16个task。，把shuffle的过程用二分图刻画，两边都各自有16个顶点，边有16*16条。
对于shuffle join，假设shuffle前后分区个数不变，每个task需要去其他12个task（有3个task和自己在同一个executor上）拉取数据，把shuffle的过程看做是二分图，两边都各自有16个顶点，边有16*16条（task到task）。
对于broadcast join，driver从各个分区获取数据，有16条从分区到driver的边（相当于16条task到task的边），然后driver广播给各个executor，总共有4条driver到executor的边。
broadcast join的粒度是executor，shuffle的粒度是task，感觉还是broadcast join的数据少一点。因为同一份数据，即使两个task在同一个executor，对于shuffle，还是会在同一个executor上有两份相同的数据，而broadcast，在一个executor上只有一份数据。</div>2021-04-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/48/ef/4750cb14.jpg" width="30px"><span>🚤</span> 👍（0） 💬（1）<div>Executor端的Broadcast这个功能，目前的spark版本是不是没有这个功能呀？</div>2021-04-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/29/c0/69/12966ad5.jpg" width="30px"><span>一只菜🐶</span> 👍（0） 💬（0）<div>老师，想问下生产中会碰到广播变量超过阈值然后导致driver oom但实际被广播的表很小 比如1mb driver内存一般设置在5g-10g之间 解决方案就是将spark.sql.autoBroadcastJoinThreshold=-1就可以避免oom 不太清楚原因 麻烦老师解答</div>2024-07-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/ce/53/d6a1f585.jpg" width="30px"><span>光羽隼</span> 👍（0） 💬（0）<div>如果通过Driver获取小表的数据分布信息，然后选取其中一个Executor收集所有的数据，然后再通过这个Executor将数据分发到所有的Executor。这样网络开销会小很多吧。。。。
这种让其中一个Executor收集分发的方式和Driver收集再分发的方式没区别，只是Driver收集小表全部数据可能会有内存的压力，但是Executor最后反正是需要小表全部的数据，那么提前让Executor来承担这个收集的工作，应该不会造成内存压力。</div>2024-06-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/20/f3/3d/7b37ce97.jpg" width="30px"><span>有风的夏天</span> 👍（0） 💬（0）<div>请问下，executor数 还有核数，与并行度设置的关系，您在实际应用中是怎么设置的</div>2022-11-01</li><br/>
</ul>