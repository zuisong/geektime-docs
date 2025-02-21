你好，我是吴磊。

一提到Shuffle，你能想到什么？我想很多人的第一反应都是应用中最顽固、最难解决的性能瓶颈。

在之前的课程中，我们也不止一次地提到Shuffle，尤其是在开发原则那一讲，我还建议你遵循“能省则省、能拖则拖”的原则，在应用中尽量去避免Shuffle，如果受业务逻辑所限确实不能避免，就尽可能地把Shuffle往后拖。

那么，为什么我们一谈Shuffle就色变，提到它就避之唯恐不及呢？今天这一讲，我就通过实现一个仙女散花游戏的过程，来和你深入探讨Shuffle是如何工作的，说说它为什么是分布式应用一时无两的性能杀手。毕竟，只有了解Shuffle的工作原理，我们才能更好地避免它。

## 如何理解Shuffle？

假设，你的老板今天给你安排一个开发任务，让你用Spark去实现一个游戏需求。这个实现需求来自一个小故事：仙女散花。

很久以前，燕山脚下有个小村庄，村子里有所“七色光”小学，方圆百里的孩子都来这里上学。这一天，一年级2班的黄老师和班里的五个孩子正在做一个游戏，叫做“仙女散花”。

黄老师的背包里装满了五种不同颜色的花朵，五种颜色分别是红、橙、黄、紫、青。她把背包里的花朵随机地分发给五个小同学：小红、橙橙、黄小乙、阿紫和小青。花朵发完之后，每个同学分到的花朵数量差不多，颜色各有不同。
<div><strong>精选留言（30）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/26/b5/88/477e7812.jpg" width="30px"><span>RespectM</span> 👍（24） 💬（6）<div>老师，如何加快netty堆外内存的回收啊？snappy+parquet格式数据会导致，netty堆外内存增长太快，导致netty使用过多direct memory，然后报错。</div>2021-06-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/fe/a2/5252a278.jpg" width="30px"><span>对方正在输入。。。</span> 👍（14） 💬（3）<div>老师我补充一下，采用sortShuffle的方式时，只有满足在shuffleDependency里面aggeragator或者sort这两个字段有效时，才会根据partitionid和key排序，否则只根据partitionid排序。如不会按照key排序的算子有repartition</div>2021-04-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/17/df/e5/65e37812.jpg" width="30px"><span>快跑</span> 👍（13） 💬（1）<div>老师你好，针对参数配置有几个疑问，辛苦帮忙解答下疑问

SELECT
	userid, pvid
FROM table
GROUP BY user,pvid

没有额外设置配置的情况下，日志：Stage-0_0: 0(+1)&#47;1294 Stage-1_0: 0&#47;1099
Stage-0_0，就是读取文件的过程，Task数据根据数据块决定的。
疑问1：Stage-1_0，这个阶段的Task数量，默认是怎么计算出来的？

我想改变Stage-1_0阶段的Task并发数量。
通过设置spark.default.parallelism=2000和spark.sql.shuffle.partitions=3000都没有生效。倒是mapreduce.job.reduces=1500配置项生效了。
日志：Stage-0_0: 0(+1)&#47;1294 Stage-1_0: 0&#47;1500


疑问2：这种sql执行计划中的groupByKey，属于spark.sql.shuffle.partitions所描述的聚合类操作的场景么？
疑问3：spark.sql.shuffle.partitions 和 mapreduce.job.reduces 怎么理解这两个参数的使用场景</div>2021-05-21</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/IcDlyK6DaBrssVGlmosXnahdJ4bwCesjXa98iaapSDozBiagZTqSCok6iaktu2wOibvpNv9Pd6nfwMg7N7KTSTzYRw/132" width="30px"><span>慢慢卢</span> 👍（8） 💬（2）<div>建议老师以同样的思路弄一个flink的专栏</div>2021-06-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/28/36/7b/b06aad84.jpg" width="30px"><span>空</span> 👍（6） 💬（1）<div>老师，您好，学习了您的专栏受益匪浅，对于您评论里说的每个task处理的数据分片200M左右最佳，那如果我两个5Ｔ的大表做join，那我的shuffle reduce 的task数量岂不是要26215，那这个磁盘和网络开销不是大的惊人？</div>2021-06-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/19/a1/2d/599e9051.jpg" width="30px"><span>CycleGAN</span> 👍（6） 💬（2）<div>老师的这一节讲得真棒，我也看了一些博客和书，但总是乱糟糟的，专栏质量很高，兼顾了深度+清晰度+新，已推荐同事中，好好看一起跳槽。。
老师我有个两个问题，第一个是针对问题一，每一个分区的（分区 ID，Key）的枚举数目，在初始阶段就应该就确定了，partitionedAppendOnlyMap中很多时候key有时候也就几十几百，这里，是5种，而buffer只能放4种，差这么一种，就增加了很多次的落盘读盘，spark有针对buffer的动态调整吗？
第二个，是对所有临时文件和内存数据结构中剩余的数据记录做归并排序，是结合堆排序的吗，临时文件太多的时候，会不会不能同时打开这么多文件，还是用的类似优化版的两两归并呢？
</div>2021-05-15</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/25/f1/bb/547b580a.jpg" width="30px"><span>苏子浩</span> 👍（6） 💬（5）<div>老师我想确认一下，问题一所提到的reduceByKey 中 Map 阶段每一个临时文件中的内容是否和该对应数据分区中的数据记录的顺序有关呢？因为分区中数据记录的不同而导致Map 阶段每一个临时文件中的内容不同。根据在文中提到的GroupBuKey算子的计算步骤二：“PartitionedPairBuffer 填满后，如果分片中还有未处理的数据记录，就对 Buffer 中的数据记录按（目标分区 ID，Key）进行排序，将所有数据溢出到临时文件，同时清空缓存。”那么类比到ReduceByKey中，就可以得到“当PartitionedAppendOnlyMap填满后，如果分片中还有未处理的数据记录，就对 Buffer 中的数据记录按（目标分区 ID，Key）进行排序，将所有数据溢出到临时文件，同时清空缓存。”那么根据您文中所给出的“数据分区0”图片，所可看到的文件顺序是“红，菊，黄，紫，黄，红，紫，橙，紫，青，青，橙，橙，红，黄，黄”。那么根据上述算法，假设PartitionedAppendOnlyMap的size为4。那么在我们处理到第一个“青”的时候，触发第一次临时文件的排序与溢出，并清空数据结构。i.e.
溢写出的第一个文件为：
[(分区id, 红), 2]; [(分区id, 橙), 2]; [(分区id, 黄), 2]; [(分区id, 紫), 3]。继续扫描剩下的数据记录，直到遍历所有数据分区0中所有数据记录。此时partitionedAppendOnlyMap里的数据为：
[(分区id, 红), 1]; [(分区id, 橙), 2]; [(分区id, 黄), 2]; [(分区id, 蓝), 2].
此时我们对partitionedAppendOnlyMap里的数据排序后，与溢出的临时文件进行归并排序得到输出文件(数据文件):
[(分区id,红), 3]; [(分区id, 橙), 4]; [(分区id, 黄), 4]; [(分区id, 紫), 3]; [(分区id, 青), 2].
对应的索引文件为:
0,1,2,3,4.
和 groupByKey 生成的中间文件不一样，map端聚合，降低了数据量。
不好意思，打了这么多字，谢谢！</div>2021-04-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/17/df/e5/65e37812.jpg" width="30px"><span>快跑</span> 👍（5） 💬（4）<div>老师好，这节学习过后生成许多疑问，请老师帮忙解惑
想就“千女散花”的过程详细了解下spark.shuffle.sort.bypassMergeThreshold
1、“千女散花”过程中的groupByKey和reduceByKey是否都不需要引入排序操作？ 目前我觉得是不需要

2、如果满足spark.shuffle.sort.bypassMergeThreshold阈值情况下，由这个参数引入排序具体发生在哪阶段？ 
	map写临时文件阶段
	临时文件归并merge阶段
	reduce拉取数据merge
这些过程都会有影响么

3、spark.shuffle.sort.bypassMergeThreshold生效的场景会区分spark rdd， spark sql，还是hive on spark么
</div>2021-04-15</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/20/2b/86/318e6ff3.jpg" width="30px"><span>井先生</span> 👍（5） 💬（4）<div>答题1：
溢写出一个文件
[（分区id，红），3] ,[（分区id，橙），4] ,[（分区id，黄），4] ,[（分区id，紫），3]
partitionedAppendOnlyMap里面的数据
[（分区id，蓝），2] 
归并排序后的输出文件
[（分区id，红），3] ,[（分区id，橙），4] ,[（分区id，黄），4] ,[（分区id，紫），3]，[（分区id，蓝），2] 
比groupByKey生产的中间文件size小，因为做过map端的预聚合

疑问：
map端做归并排序再写文件的目的是为了每一个分区的数据连续，从而让reduce端在读文件的时候读连续的记录速度更快吗？</div>2021-04-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/25/78/a0/7a248ddc.jpg" width="30px"><span>福</span> 👍（3） 💬（1）<div>真的是希望老师出个flink的，写的好nice呀</div>2021-11-09</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/PNmB3mOQ4jTSoDMGPwp5j8a2NL1Mibu4iaebBNnuDQltb2yZ3sygJpxTHuLrG9ewCDLEialorSK3pzXBCQ3JFCZPA/132" width="30px"><span>果子</span> 👍（2） 💬（1）<div>索引文件正是用于帮助判定哪部分数据属于哪个 Reduce Task。老师，（1）每个Reduce Task怎么知道自己的要读哪个索引部分，这个信息谁提供给他的，（2）他知道了后怎么定位自己的索引，二分吗？（3）索引文件记录的是reduce阶段的起始索引，每个redcue task要读取分区数据的话，是从起始索引一直读到下一个起始索引吗？这样确定一个partition?</div>2021-10-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/26/c5/fd/bb7fd00b.jpg" width="30px"><span>黄宪坤</span> 👍（2） 💬（1）<div>老师您好，有个疑问， PartitionedPairBuffer、PartitionedAppendOnlyMap 这些内存数据结构，与缓冲区内存有什么关系？</div>2021-08-30</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1e/65/0f/7b9f27f2.jpg" width="30px"><span>猿鸽君</span> 👍（2） 💬（2）<div>老师好，请问下为什么需要计算partitionid，直接根据key来排序不行吗？相同key计算的partitionid不是一样的吗，为什么需要根据（partitionid， key）来排？不懂这里计算partitionid的用意</div>2021-08-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/1d/22/f04cea4c.jpg" width="30px"><span>Fendora范东_</span> 👍（2） 💬（3）<div>Map端配置
spark.shuffle.file.buffer  适当调大可以降低落盘次数，以及降低归并排序路数
reduce端配置
spark.reducer.maxSizeInFlight   可以适当调大减少网络io次数


spark.shuffle.sortBypassMergeThreshold  map端不进行排序的阈值。因为目前shuffle操作由sortshufflemanager管理，默认在map操作时会进行排序，例子中groupbykey，reducebykey并不需要排序

请问磊哥，缓存大小调整有啥技巧么，应该不是越大越好吧</div>2021-04-07</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1e/f2/f5/b82f410d.jpg" width="30px"><span>Unknown element</span> 👍（1） 💬（1）<div>第一题：
每个 map task 遍历本地分片中的数据，为每条数据计算目标分区，假设 PartitionedAppendOnlyMap 的容量还是4，那么第一次溢出前它的内容应该是：
[(课桌1，橙)，2]，[(课桌2，灰)，2]，[(课桌3，黄)，2]，[(课桌4，紫)，3]
溢出后继续刚才的步骤填充 PartitionedAppendOnlyMap:
[(课桌5，白)，2]，[(课桌2，灰)，2]，[(课桌1，橙)，1]，[(课桌3，黄)，2]
此时完成对所有数据的遍历，maptask接着对临时文件和内存中的数据做归并排序生成中间文件：
data文件：（橙，3）（灰，4）（黄，4）（紫，3）（白，2）
index文件：0 1 2 3 4
它和groupByKey的中间文件显然是不一样的，因为reduceByKey在map端做了聚合，所以溢出次数和文件体积都会更小
第二题：
map阶段：（1）map task数量：spark.default.parallelism
               （2）计算数据的目标分区：(spark.executor.memory-300)*spark.memory.fraction*(1-spark.memory.storageFraction)
               （3）是否排序：spark.shuffle.sort.bypassMergeThreshold
               （4）写入临时文件、中间文件的位置：spark.local.dir
               （5）map输出端写入缓冲区大小：spark.shuffle.file.buffer
reduce阶段：（1）reduce task数量：spark.sql.shuffle.partitions
                   （2）reduce输入端缓冲区大小：spark.reducer.maxSizeInFlight

另外我有几个问题，（1）map task 和 reduce task 用到的 executor 是在所有可用资源里根据配置项指定的数目随机选出来的吗？如果是的话那么他们有可能有交集（就是某个map task完成计算后接着变成reduce task开始执行reduce的计算）？
                             （2）reduce 阶段每个 executor 怎么知道自己的编号从而知道自己应该拉取哪个分区的数据呢？
                             （3）您在回答评论区的问题 “在使用partitionedAppendOnlyMap时，多个溢出的文件需要归并排序，归并排序的过程中是不是对同一个key也做了一次combine操作？” 时说 “并不会，归并排序这个说法，可能有些迷惑性。他实际上就是把多份临时文件“拼接”在一起，” ，这里我不太明白，假如 shuffle 是由 reduceByKey 引入的，而map阶段溢出的两份临时文件中都包含某个key的记录，那么在对溢出文件做归并排序时不是应该把这两条数据的value再加一次吗？如果归并排序阶段只是简单的拼接临时文件感觉计数会出问题？
                             （4）老师方便讲一下各个概念之间数量上的对应关系以及它们和物理实体的对应关系吗？比如节点和 executor 是一对多，executor 和 task 也是一对多，task 和 partition 是一对一？一个节点对应一台计算机，一个executor是若干CPU和存储资源的集合，一个task是独占一个cpu的任务？
字比较多，希望老师不要介意，谢谢老师~~~</div>2021-12-15</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/2a/39/68/56dfc8c0.jpg" width="30px"><span>子兮</span> 👍（1） 💬（1）<div>老师您好，之前在学习shuffle时看到的总结是：map端局部聚合，reduce 端全局聚合，所以我对combineByKey代替groupByKey 的优化方法不是很能接受，今天看了老师的课，我的理解是，每个shuffle 算在map 端的处理是不同的，比如reduceByKey是map端局部聚合，再reduce端全局聚合，但groupByKey 在map端只是进行排序，在reduce 端进行聚合。不知道我的理解对不对，麻烦老师啦，谢谢</div>2021-11-03</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/21/00/3f/a0f84788.jpg" width="30px"><span>Sean</span> 👍（1） 💬（1）<div>磊哥,二刷后又多了两个疑问,辛苦磊哥解答下,这样一条sql
create table if not exists tmp_a as
select a.id, age, name, sex
from (
         select id, age, name
         from app_info
         group by id, age, name
     ) a
         join

     (
         select a1.id, sex
         from (
                  select id, count(distinct uid) uid_cnt
                  from register_log
                  group by id
                  having uid_cnt &gt; 100
              ) a1
                  join
              (
                  select id, sex
                  from register_log
                  group by id,sex
              ) a2
              on a1.id = a2.id
     ) b
     on a.id = b.id;
运行结束后,产生了9个stage,发现ui上的每个成功的stage的total task个数不一,在shuffle read有数据的stage中(理解为这是shuffle reduce阶段,这里会生成5000个task),task个数并没有达到5000,9个stage的task累加依然没有达到5000个task,
问题1:想请教下磊哥这块这个task的划分规则是怎么定义的,自己没能定位到这块的源代码
问题2:想请教下磊哥这块这个stage的划分规则,我理解一个宽依赖一个stage,但依然无法还原这9个stage生成的规则</div>2021-10-01</li><br/><li><img src="" width="30px"><span>Geek_c17db5</span> 👍（1） 💬（1）<div>老师，reduce 阶段读取map阶段写的临时文件，是不是也是按大小分块，分成多个task去读的？</div>2021-09-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/17/11/20/9f31c4f4.jpg" width="30px"><span>wow_xiaodi</span> 👍（1） 💬（4）<div>结合本节课程和评论思考了下，有如下问题想请教下老师：
(1)对于使用partitionedAppendOnlyMap时，相当于作了一次map端的combine操作，请问这个combine操作在spark里是必须要做的吗？是否有开关去控制呢？
(2)在使用partitionedAppendOnlyMap时，多个溢出的文件需要归并排序，归并排序的过程中是不是对同一个key也做了一次combine操作？</div>2021-07-31</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/7DL88WEw0QsxHg4HicLyickqGT3C9NLeiaDmPFSENNs0yw2wp2rqLicZ3AY935PKd3WJbcJrn43O3JLYUbmOmfkTnA/132" width="30px"><span>Lon_coder</span> 👍（1） 💬（1）<div>老哥请问，partitionedpairbuffer在内存中不对某个key的结果进行聚合，但在文件merge过程🀄️会聚合么，因为那时候key已经有序了</div>2021-07-06</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/PNmB3mOQ4jTSoDMGPwp5j8a2NL1Mibu4iaebBNnuDQltb2yZ3sygJpxTHuLrG9ewCDLEialorSK3pzXBCQ3JFCZPA/132" width="30px"><span>果子</span> 👍（1） 💬（2）<div>老师能讲讲SPARK溢写的流程吗？</div>2021-07-01</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/PNmB3mOQ4jTSoDMGPwp5j8a2NL1Mibu4iaebBNnuDQltb2yZ3sygJpxTHuLrG9ewCDLEialorSK3pzXBCQ3JFCZPA/132" width="30px"><span>果子</span> 👍（0） 💬（1）<div>吴老师，spark map阶段进入内存的数据为啥要排序</div>2021-12-03</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/87/4b/16ea3997.jpg" width="30px"><span>tiankonghewo</span> 👍（0） 💬（1）<div>OOM容易发生在shuffle的哪个环节?</div>2021-11-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/19/1a/19/440b0c7e.jpg" width="30px"><span>学无止境</span> 👍（0） 💬（1）<div>老师，你好，面试经常问到MR shuffle 与 spark shuffle有什么区别，感觉他两好像都差不多的步骤，数据分区，写缓冲区，溢写磁盘归并排序，reduce端拉取。有什么比较好答的点吗</div>2021-11-03</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/17/11/20/9f31c4f4.jpg" width="30px"><span>wow_xiaodi</span> 👍（0） 💬（1）<div>到这里对bypass机制就有点懵了
(1)算子无需聚合或排序，还要reduce并行度低于bypass门限值，就不排序，可以省去排序开销，但是一定程度增加临时文件IO开销，那么人为如何去评估哪个收益大呢？
(2)ByPass溢出机制会为每个reduce task都建立一个临时文件，这样会增加磁盘IO，那么为何就不能按照SortShuffle默认机制去溢出，不排序就行了吗？</div>2021-07-31</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/26/b5/88/477e7812.jpg" width="30px"><span>RespectM</span> 👍（0） 💬（2）<div>接上一条，Caused by: io.netty.util.internal.OutOfDirectMemoryError: failed to allocate 16777216 byte(s) of direct memory (used: 7633633280, max: 7635730432)</div>2021-06-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/d4/78/66b3f2a2.jpg" width="30px"><span>斯盖丸</span> 👍（0） 💬（2）<div>老师，请问shuffle时spill到磁盘的中间文件的大小在哪看？
比如一个task 200多M，我一个shuffle write操作后，怎么看生成了几个spill文件，各自的大小是多少呢？哪些参数可以控制它们～?</div>2021-06-04</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/d4/78/66b3f2a2.jpg" width="30px"><span>斯盖丸</span> 👍（0） 💬（1）<div>请问一下老师，SortShuffle里，map阶段在合并中间文件之前，中间文件的数量也可能是很可观的吧(假如溢出次数不得不很多的情况下)…？我想问的是总有一个时间点，map需要同时维护那么多个中间文件，同时打开那么多的句柄，这样会出问题吗？</div>2021-06-03</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/17/df/e5/65e37812.jpg" width="30px"><span>快跑</span> 👍（0） 💬（1）<div>突然想到个问题，想请教下老师，会不会因为SET某个变量，导致执行计划的变化？Explain SQL的结果不一样？</div>2021-05-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/5c/d7/e4673fde.jpg" width="30px"><span>October</span> 👍（0） 💬（1）<div>Reduce极端的读缓存指的是什么？</div>2021-04-10</li><br/>
</ul>