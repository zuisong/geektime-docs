你好，我是吴磊。

目前，距离Spark 3.0版本的发布已经将近一年的时间了，这次版本升级添加了自适应查询执行（AQE）、动态分区剪裁（DPP）和扩展的 Join Hints 等新特性。利用好这些新特性，可以让我们的性能调优如虎添翼。因此，我会用三讲的时间和你聊聊它们。今天，我们先来说说AQE。

我发现，同学们在使用AQE的时候总会抱怨说：“AQE的开关打开了，相关的配置项也设了，可应用性能还是没有提升。”这往往是因为我们对于AQE的理解不够透彻，调优总是照葫芦画瓢，所以这一讲，我们就先从AQE的设计初衷说起，然后说说它的工作原理，最后再去探讨怎样才能用好AQE。

## Spark为什么需要AQE？

在2.0版本之前，Spark SQL仅仅支持启发式、静态的优化过程，就像我们在第21、22、23三讲介绍的一样。

启发式的优化又叫RBO（Rule Based Optimization，基于规则的优化），它往往基于一些规则和策略实现，如谓词下推、列剪枝，这些规则和策略来源于数据库领域已有的应用经验。也就是说，**启发式的优化实际上算是一种经验主义**。

经验主义的弊端就是不分青红皂白、胡子眉毛一把抓，对待相似的问题和场景都使用同一类套路。Spark社区正是因为意识到了RBO的局限性，因此在2.2版本中推出了CBO（Cost Based Optimization，基于成本的优化）。
<div><strong>精选留言（19）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/29/90/99/24cccca5.jpg" width="30px"><span>周俊</span> 👍（15） 💬（1）<div>老师，

&#47;&#47;订单表与用户表关联
select sum(order.price * order.volume), user.id
from order inner join user
on order.userId = user.id
where user.type = ‘Head Users’
group by user.id
这段代码中，catalyst会做谓词下推处理，将过滤条件放到贴近数据源扫描的地方，这里过滤之后user表的大小已经属于小表变成广播变量的阈值了吧，为什么还会有AQE呢</div>2021-08-16</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/1d/22/f04cea4c.jpg" width="30px"><span>Fendora范东_</span> 👍（8） 💬（3）<div>磊哥，请教下
Join策略调整里面，为啥只有SMJ能降级，而其他Join比如SHJ不能降级</div>2021-05-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/42/f3/e945e4ac.jpg" width="30px"><span>sparkjoy</span> 👍（5） 💬（1）<div>老师，为什么不在join之前统计两个表的大小，从而决定是否用BHJ，而是map结束之后才根据shuffle文件总大小去判断呢？</div>2021-08-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/a2/4b/b72f724f.jpg" width="30px"><span>zxk</span> 👍（4） 💬（1）<div>问题一：个人认为 AQE 可以在加载读取文件的时候获取一些运行时信息，或者做 cache 的时候。这里也有个疑问，就是 AQE 会不会根据这些信息也进行一些优化？
问题二想到两种方法，不知道是否可行：
1.  Spark 有一个动态分配调整 executor 的功能，在 Shuffle Map 阶段由 Driver 端汇聚信息决定好倾斜数据的切割方式，之后部分数据发送到原有的 executor 上，切割出来的数据发送到新的 executor 上，同时也需要注意对应做关联的数据也需要复制一份传输到新的 executor 上，但这样会带来 driver 端决策的开销、新的 executor 调度开销以及关联数据额外复制并通过网络传输的开销。
2. 仍按照原来的方式进行，但在 Reduce 阶段切割数据后，起一个新的 executor 来分担切割后的数据，并通知 driver 端。如果能够在同节点上新起 executor，还可以消除网络之间的传输，只做进程间的数据传输即可。

这里想向老师请教一个关于 Join 策略调整的问题，如果 a、b 为事实表，c 为维度表，a、c 做关联后 c 从原来的 SMJ 被 AQE 优化为了 BHJ 后，如果紧接着 b 又跟 c 做关联，那么 Spark 是否会直接使用 
 BHJ，还是仍需要将 b、c 做 SHuffle Map 之后才能优化为 BHJ？</div>2021-05-07</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/42/f3/e945e4ac.jpg" width="30px"><span>sparkjoy</span> 👍（2） 💬（1）<div>老师，cbo的信息是存在表的元信息里吗？</div>2021-08-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/29/57/61/369a609c.jpg" width="30px"><span>A</span> 👍（2） 💬（2）<div>spark.sql.adaptive.advisoryPartitionSizeInBytes，由开发者指定分区合并后的推荐尺寸。分区合并的最终尺寸这个配置应该是个建议值吧？min(maxTargetSize,advisoryTargetSize)会通过这行代码来取advisoryTargetSize</div>2021-07-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1b/a5/65/898bc6c5.jpg" width="30px"><span>wayne</span> 👍（1） 💬（1）<div>老师，请问 aqe可以强制指定输出文件的大小吗？比如强制设置 设置分区文件大小为128m</div>2021-12-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/98/4d/582d24f4.jpg" width="30px"><span>To_Drill</span> 👍（1） 💬（1）<div>老师您好，关于文章中的图-两边倾斜中的关联箭头指向有点疑问，如果两张表的关联分区都发生了倾斜，然后都进行了拆分，那么拆分之后的子分区中的是局部数据，应该和对方的全量数据都关联下才能保证原来的关联逻辑，这样的话各个子分区的关联箭头指向是不是应该如下图所示呢？
拆分-01-拷贝   -&gt;    拆分-01
拆分-01        -&gt;    拆分-02 
拆分-02        -&gt;    拆分-01-拷贝
拆分-02-拷贝   -&gt;     拆分-02-拷贝
</div>2021-11-30</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/17/11/20/9f31c4f4.jpg" width="30px"><span>wow_xiaodi</span> 👍（1） 💬（1）<div>老师，请教下：
(1)尽管两个大分区被拆分，但横向来看，整个作业的主要负载还是落在了 Executor 0 的身上。Executor 0 的计算能力依然是整个作业的瓶颈，这一点并没有因为分区拆分而得到实质性的缓解。这里不是很明白为何分区拆分后都落到一个executor上呢？
(2)aqe的分区拆分底层也是走两阶段shuffle聚合吗？</div>2021-08-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/37/d0/26975fba.jpg" width="30px"><span>西南偏北</span> 👍（1） 💬（1）<div>1. 如果不用Map阶段的输出文件的话，那应该就是实时统计了吧，比如&quot;ANALYZE TABLE COMPUTE STATISTICS&quot;
2. 为了防止倾斜分区都出现在同一个Executor的情况，可以考虑对倾斜数据的key进行加前缀，然后再将这些数据进行一下重分区repartition()，分区数指定为executor的个数。但是，由于使用了repartition()，也就引入了shuffle开销，这个也是一个要平衡的问题</div>2021-05-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/31/9d/daad92d2.jpg" width="30px"><span>Stony.修行僧</span> 👍（1） 💬（2）<div>老师请教一个问题，一个10g的csv 文件，里面有4个字段，其中三个字段需要做匿名化。在匿名化三个字段里过程中，可以partition第四个字段来提高性能吗？求老师的意见和建议</div>2021-05-07</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/04/30/7f2cb8e3.jpg" width="30px"><span>CRT</span> 👍（0） 💬（1）<div>老师，既然分区合并是要等shuffle map阶段结束之后才可以适用，那么shuffle map阶段原本会生成多少个task，应该怎么决定呢？</div>2022-01-18</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/DYAIOgq83eoTl88qjhxrFFdPSJbcCt3CGib90KAvoqzvibZpc4ZaInk2x4gGEABbXgIic1KkhQxNABXYAD1Pic3jjQ/132" width="30px"><span>Geek_c8148b</span> 👍（0） 💬（1）<div>想问一下文中提到“每个 data 文件的大小、空文件数量与占比、每个 Reduce Task 对应的分区大小，所有这些基于中间文件的统计值构成了 AQE 进行优化的信息来源”，这里为啥会出现“每个 Reduce Task 对应的分区大小” ？有点不理解~ 希望解答一下</div>2022-01-15</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/17/55/41/b68df312.jpg" width="30px"><span>农夫三拳</span> 👍（0） 💬（1）<div>问题2: 可否采用自动分区合并的思路。  判断发送到某个executor的数据量过大。 预判会发生倾斜。  不是join情况下 ：就让其他的executor拉取一部分数据做计算。 join情况下： 依然是一部分数据拉取到其他executor 同时关联的数据做复制 也拉取过去。  不知道是否可行？</div>2021-11-05</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/42/f3/e945e4ac.jpg" width="30px"><span>sparkjoy</span> 👍（0） 💬（1）<div>老师，DemoteBroadcastHashJoin 策略在本文中的表格中说是对于逻辑计划部分的优化，我理解join策略应该属于物理计划，这个为什么是对逻辑计划的优化呢？</div>2021-08-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/28/0e/60/9b9e28f8.jpg" width="30px"><span>really_z</span> 👍（0） 💬（0）<div>生产情况遇到这样的问题，有张表是标签表，大量的1和0 ，发现aqe自动优化成了broadcast join，就发生了oom。再隐式转化成sort merge join 就没有oom。想问一下aqe是怎么评估的呢，难道中间文件是会被压缩后评估的么</div>2024-10-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1e/f5/9a/63dc81a2.jpg" width="30px"><span>Geek1185</span> 👍（0） 💬（0）<div>老师这里该如何理解呢？“除此之外，我们还要注意，在 Shuffle Map 阶段完成之后，AQE 优化机制被触发，CoalesceShufflePartitions 策略“无条件”地被添加到新的物理计划中。”是指只要有shuffle，那么就会在exchange节点下增加customshuffleread coalesce节点吗</div>2023-03-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/0a/ab/4d0cd508.jpg" width="30px"><span>你挺淘啊</span> 👍（0） 💬（1）<div>问下老师，自动分区合并那里的两个参数，spark.sql.adaptive.advisoryPartitionSizeInBytes，由开发者指定分区合并后的推荐尺寸。
spark.sql.adaptive.coalescePartitions.minPartitionNum，分区合并后，分区数不能低于该值。
为什么有了推荐尺寸后，还要一个分区数的参数呢？这两个参数在实际中要如何一起使用呢？能举个例子说明吗，多谢老师</div>2022-07-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/27/d3/0a/92640aae.jpg" width="30px"><span>我爱夜来香</span> 👍（0） 💬（1）<div>老师,有一点不大理解,一般都是把相同的key放到一个reducer执行,倾斜分区打散后最终还是会发到同一个reducer吗</div>2022-05-01</li><br/>
</ul>