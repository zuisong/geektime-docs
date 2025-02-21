你好，我是吴磊。

在上一讲，我们拜访了斯巴克国际建筑集团总公司，结识了Spark调度系统的三巨头：DAGScheduler、TaskScheduler和SchedulerBackend。相信你已经感受到，调度系统组件众多且运作流程精密而又复杂。

任务调度的首要环节，是DAGScheduler以Shuffle为边界，把计算图DAG切割为多个执行阶段Stages。显然，**Shuffle是这个环节的关键**。那么，我们不禁要问：“Shuffle是什么？为什么任务执行需要Shuffle操作？Shuffle是怎样一个过程？”

今天这一讲，我们转而去“拜访”斯巴克国际建筑集团的分公司，用“工地搬砖的任务”来理解Shuffle及其工作原理。由于Shuffle的计算几乎需要消耗所有类型的硬件资源，比如CPU、内存、磁盘与网络，在绝大多数的Spark作业中，Shuffle往往是作业执行性能的瓶颈，因此，我们必须要掌握Shuffle的工作原理，从而为Shuffle环节的优化打下坚实基础。

## 什么是Shuffle

我们先不急着给Shuffle下正式的定义，为了帮你迅速地理解Shuffle的含义，从而达到事半功倍的效果，我们不妨先去拜访斯巴克集团的分公司，去看看“工地搬砖”是怎么一回事。
<div><strong>精选留言（29）</strong></div><ul>
<li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/DYAIOgq83epGTSTvn7r4ibk1PuaUrSvvLdviaLcne50jbvvfiaxKkM5SLibeP6jibA2bCCQBqETibvIvcsOhAZlwS8kQ/132" width="30px"><span>Geek_2dfa9a</span> 👍（39） 💬（7）<div>官网配置文档 https:&#47;&#47;spark.apache.org&#47;docs&#47;3.1.2&#47;configuration.html
Directory to use for &quot;scratch&quot; space in Spark, including map output files and RDDs that get stored on disk. This should be on a fast, local disk in your system. It can also be a comma-separated list of multiple directories on different disks.
Note: This will be overridden by SPARK_LOCAL_DIRS (Standalone), MESOS_SANDBOX (Mesos) or LOCAL_DIRS (YARN) environment variables set by the cluster manager.
临时目录，用来存map output文件（shuffle产生）和save RDD到磁盘的时候会用到。应该配置成快速的本地磁盘。支持‘,’分隔的多个目录。
注意：这个配置会被SPARK_LOCAL_DIRS（Standalone部署），MESOS_SANDBOX（Mesos），LOCAL_DIRS (YARN)替换。
既然shuffle会带来很高的开销，除了优化driver程序也可以考虑优化系统配置。
首先&#47;tmp是会被系统清理的（取决于不同linux分发版的清理策略），如果作业运行时&#47;tmp中的文件被清除了，那就要重新shuffle或
重新缓存RDD（这块没有仔细研究，简单猜测下缓存失效策略是重新缓存），因此，不适合将配置spark.local.dir设置为默认的&#47;tmp
其次，部署文档有提该配置项支持多个目录，那可以考虑配置多块硬盘（或者SSD），再把挂载不同硬盘的目录配置到spark.local.dir，
这样可以显著提升shuffle和RDD缓存的性能。请大家指教。</div>2021-09-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/19/70/67/0c1359c2.jpg" width="30px"><span>qinsi</span> 👍（13） 💬（2）<div>看到哈希那边有个问题，就是遇到不均匀的数据会怎么样？比如对这篇论文执行word count：https:&#47;&#47;isotropic.org&#47;papers&#47;chicken.pdf

原本可能指望所有工人一起搬砖，结果发现只有一个工人在搬砖？

另外前几讲说过大数据的精髓在于数据不动代码动，但这讲说还是无法避免shuffle搬运数据，这个要怎么理解？</div>2021-09-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1e/f2/f5/b82f410d.jpg" width="30px"><span>Unknown element</span> 👍（10） 💬（1）<div>老师您在shuffle read部分说“不同的 Reduce Task 正是根据 index 文件中的起始索引来确定哪些数据内容是属于自己的”，这一步具体是怎么实现的呢？以文中的index文件举例，文中的index文件是0,3,7，那么不同的reduce task是各自有一个编号，然后按编号大小顺序确定自己应该拉取哪一部分数据吗？比如编号为0的reduce task拉取index文件的第一个索引到第二个索引之间的数据，也就是index为0,1,2的数据；编号为1的reduce task拉取index文件的第二个索引到第三个索引之间的数据，也就是index为3,4,5,6的数据；编号为2的reduce task拉取index文件的第三个索引到最后的数据，也就是index为7,8,9的数据？这样的话如果map task计算出来没有数据应该被发到第二个reduce task那index文件是0,3,3吗？</div>2021-10-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1e/f2/f5/b82f410d.jpg" width="30px"><span>Unknown element</span> 👍（8） 💬（3）<div>老师您好  我有两个问题想问下：
1. 对于所有 Map Task 生成的中间文件，Reduce Task 需要通过网络从不同节点的硬盘中下载并拉取属于自己的数据内容  那不同的reduce task是怎么知道哪些内容是属于自己的呢？比如对于文中的例子，reduce阶段的3个任务怎么知道自己应该拉取中间文件的哪些记录？
2. 对于评论区AIK的问题，您说shuffle过程不是数据交换，而是数据流转，那意思是在map阶段 所有将要执行reduce task的节点都是空闲的吗（等待map task生成shuffle中间文件）？那他们是不是在这个stage的整个计算过程中都是空闲的？这样的话岂不是没有发挥出集群的最大算力？</div>2021-09-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/25/55/a4/a06abd2d.jpg" width="30px"><span>钟强</span> 👍（3） 💬（1）<div>如果集群中只有一个executor, 但是executor上面有多个map task, 这样的环境是不是不需要shuffle?</div>2022-03-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1a/49/fe/48846a6d.jpg" width="30px"><span>Ebdaoli</span> 👍（3） 💬（1）<div>磊哥，关于 spark shuffle write 阶段有个问题不太理解，①：Maptask的 任务数的并行度由什么来决定的？根据文件大小来切分划分的吗？ ②：为什么最终数据需要进行 sort？合并的方式选择的是 归并排序？</div>2022-03-06</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/29/57/61/369a609c.jpg" width="30px"><span>A</span> 👍（3） 💬（2）<div>因rdd得依赖属性shuffle划分了两个stage0和1
运行stage0的executor产生的数据称作建材，结束后driver继续提交stage1，运行stage1的executor全集群得去拉去各自所需的建材，可以这样理解嘛老师？
那stage0产生的临时data、index是记录在哪里？如何返回给driver的呢？以及stage1提交时是如何获取的呢？
目前想到的是重新封装但是又说不过去
还望老师给条路，自己再去研究一下！
感谢老师！</div>2022-01-15</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/17/76/51/96291466.jpg" width="30px"><span>猫太太</span> 👍（3） 💬（1）<div>您好，讲的很清楚，看完都有点想去去自己看源码了。这句有点不太理解，可以解释一下么：“Reduce 阶段不同于 Reduce Task 拉取数据的过程，往往也被叫做 Shuffle Read。” 请问shuffle read属于reduce阶段么？reduce task拉取数据的过程不包括在reduce阶段么？reduce task拉取数据的过程不是shuffle read么？reduce阶段有什么事情发生呢？谢谢～</div>2021-12-05</li><br/><li><img src="" width="30px"><span>阿狸弟弟的包子店</span> 👍（2） 💬（1）<div>Shuffle算法感觉需要补一补，看评论有hash得，还有sort-base的，还有其他的吗？</div>2022-01-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/28/3f/9d/c59c12ad.jpg" width="30px"><span>实数</span> 👍（2） 💬（1）<div>这个讲的是hashshuffle是吗，那么第二代的sortshuffle相比较如何呢。是不是两代的shuffle都不能保证全局有序啊</div>2021-11-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/25/d4/04/49dfb810.jpg" width="30px"><span>啊秋秋秋秋</span> 👍（2） 💬（2）<div>老师您好！请问为什么是reducer从mapper那里拉取数据，而不是mapper把数据push到reducer端呢？我自己的理解是，如果是mapper push的话，传递数据这部分工作主要在mapper端，比如需要存储各个reducer的地址，会给mapper增加workload？但是感觉两种方式都可以，不太清楚为什么MR Spark这种分布式计算模型里都是采用reducer pull，请指点一下！谢谢！！</div>2021-11-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1d/5e/b2/aceb3e41.jpg" width="30px"><span>Neo-dqy</span> 👍（2） 💬（3）<div>老师好，学完这节课我主要有三个问题：
1. Shuffle Write 过程中，对所有临时文件和内存数据结构中剩余的数据记录做归并排序，这里是按照目标分区的ID进行排序，还是按照value（词频）进行排序的啊？
2. 除了reduce类型的算子会触发shuffle操作，还有什么别的算子能触发呢？
3. 既然shuffle操作是不可避免的，那我们又要怎么优化这个操作呢？</div>2021-09-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/23/bb/a1a61f7c.jpg" width="30px"><span>GAC·DU</span> 👍（1） 💬（2）<div>中间存储文件，我理解它是一个不用永久存储的临时文件，理论上放到任何位置都可以。但是如果在生成文件这个临界点Executor宕机，存放在&#47;tmp目录下的文件就会丢失，如果存放在正常的目录下就会避免这种问题。还有shuffle write如果是顺序写，选SSD或者HDD硬盘也没什么区别。

有两个问题想请教老师

第一，您说Reduce Task 通过 index 文件来“定位”属于自己的数据内容和index 文件，是用来标记目标分区所属数据记录的起始索引。那么Reduce Task如何知道从起始索引读取多少个数据为止，是Reduce Task内部还有算法吗？

第二，您说Map 阶段与 Reduce 阶段，通过生产与消费 Shuffle 中间文件的方式，来完成集群范围内的数据交换，我对此处的交换不是很理解，交换不应该是相互的吗，我理解的交换是双方拿出自己的交给对方，比如我在篮子里放一个苹果，您在篮子里放一个梨，我拿到了梨而您拿到了苹果。但是Map和Reduce两者之间Reduce更像是白拿。这里的数据交换能不能理解成数据传递或者数据流转？</div>2021-09-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/2b/f5/9c/4bdff9f2.jpg" width="30px"><span>Tianchen</span> 👍（0） 💬（1）<div>老师好，想问下公式1的哈希值P，在后续流程中是对应的Map 结构中Reduce Task Partition ID（P0,P1 ,P2）还是index（0,3,7）</div>2022-03-03</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/d9/36/05eda19f.jpg" width="30px"><span>小西门</span> 👍（0） 💬（1）<div>老师好，我的问题是：
如果计算记录所属那个Reduce Task的算法是一致的话，会不会出现某些exectors中只有单个(k,v)，但是通过算法计算出来的reduce task partition ID是另外一个executor？这样就产生了不必要的网络IO。

我个人猜想是，会不会计算reduce task partition ID是在各map task做完之后，通知到driver，dirver获得了全局信息后，再通知到reduce task不用去shuffle read只有单个(k,v)的executor的shuffle中间文件。</div>2022-02-16</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/3c/c4/4ee2968a.jpg" width="30px"><span>艾利特-G</span> 👍（0） 💬（1）<div>&gt; 假设 Reduce 阶段有 N 个 Task，这 N 个 Task 对应着 N 个数据分区，那么在 Map 阶段，每条记录应该分发到哪个 Reduce Task，是由下面的公式来决定的。
&gt; ...
&gt; 首先，我们需要注意的是，对于每一个 Map Task 生成的中间文件，其中的目标分区数量是由 Reduce 阶段的任务数量（又叫并行度）决定的。

所以我是不是可以这么理解: 第一段里说的&quot;N&quot;和第二段里说的任务并行度是同一个事物，也就是Executor的core数？</div>2022-02-08</li><br/><li><img src="" width="30px"><span>Geek_a3a122</span> 👍（0） 💬（2）<div>`Reduce 阶段不同于 Reduce Task 拉取数据的过程，往往也被叫做 Shuffle Read。`
这句话没太理解，Reduce Task拉取数据的过程不就是Shuffle Read吗，为什么叫Reduce阶段不同于Reduce Task拉取数据的过程呢？</div>2021-11-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/4c/6d/c20f2d5a.jpg" width="30px"><span>LJK</span> 👍（0） 💬（1）<div>老师的课真的是很好，非常感谢！对于Shuffle有个疑问，之前看到过对于几种特殊情况窄依赖的操作，譬如coalesce(shuffle=false)和cartesian，虽然child rdd依赖多个parent rdd，但是是不会生成新的stage的，不明白这几个操作会不会产生网络IO。毕竟如果下一个task需要合并多个分区的话，如果这些分区不在同一物理节点，那么如何进行合并呢？还是说由于懒加载其实是不进行合并的？</div>2021-10-03</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/26/6f/4f/3cf1e9c4.jpg" width="30px"><span>钱鹏 Allen</span> 👍（0） 💬（2）<div>tmp缓存文件可以临时生成
shuflle阶段：溢出临时文件和合并merge中间文件
transform和action算子之间需要shuffle，之前自己只了解宽窄依赖，现在对shuffle的运行机制更深一部了解。</div>2021-09-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/21/ec/05/ce889d6c.jpg" width="30px"><span>般度五子</span> 👍（0） 💬（3）<div>大佬，看完觉得spark的shuffle跟mapreduce的shuffle像是一样的，两者有区别吗？两者主要区别是什么？
另外，如果一个MR job只有一个阶段的map和reduce而没有级联，处理效率应该和spark差不多吧？</div>2021-09-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/63/a2/abb7bfe3.jpg" width="30px"><span>星潼</span> 👍（1） 💬（2）<div>感谢老师的精彩讲解，我有一个问题请教老师^_^。
听了老师的讲解，我发现Spark也是将Shuffle过程的中间结果保存在磁盘，感觉这个流程跟MapReduce的Shuffle过程很类似。
MapReduce性能差的一个原因就是Map Task将中间结果数据写在磁盘，之前听说Spark性能好的原因是由于内存计算，可既然Spark的shuffle过程也是将中间结果写到磁盘，那为什么spark的性能就会比MR高出很多呢？请老师指教，感谢。</div>2022-05-05</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/04/0d/3dc5683a.jpg" width="30px"><span>柯察金</span> 👍（0） 💬（0）<div>老师，map task 的并行度跟读取文件分片有关系，那么 reduce task 的并行度呢？是跟 map task 保持一致，还是由什么决定，还是可以手动指定的呢？</div>2024-02-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/17/f8/90/9179380d.jpg" width="30px"><span>杨曦</span> 👍（0） 💬（0）<div>map阶段的临时文件,以及内存中的剩余数据. 在归并排序生成data文件的时候,这些临时文件是都打进内存的么?如果是的话,是如何保证不出现内存溢出的呢?</div>2023-10-09</li><br/><li><img src="" width="30px"><span>Geek_7caf52</span> 👍（0） 💬（1）<div>在 Shuffle Write 一节中提到 “当 Map 结构被灌满之后”，请问 Map 结构什么情况下会被 “灌满” 呢</div>2023-08-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/0f/70/f59db672.jpg" width="30px"><span>槑·先生</span> 👍（0） 💬（0）<div>有个疑惑，为什么一定要先生成文件了再让reduce来拉，直接在map端算好了目标reduce节点，从内存里发过去不是更快么。生成文件是为了任务恢复考虑的吗？</div>2023-03-22</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/iaQgtbE98VGIVIyribdo6dgLOnaNoe7ZdUuPr60ibsduibscrzQCTzdW2AfL9nxwe8YlSK75gOnK3YbAJKTaFPxibdg/132" width="30px"><span>小李</span> 👍（0） 💬（2）<div>老师，在业务场景中，shuffle write阶段是怎么知道shuffle read阶段的分区数的？</div>2022-10-23</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/ugib9sF9icd9dhibQoAA025hibbD5zgZTiaddLoeEH457hrkBBhtQK6qknTWt270rHCtBZqeqsbibtHghgjdkPx3DyIw/132" width="30px"><span>唐方刚</span> 👍（0） 💬（0）<div>怎么感觉和hadoop mr的过程一样的</div>2022-08-10</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTIw0Nnvrrt9fV1wHVfBlPzrZmxNCRTbWPfNEbCEMtuoj6gw0LlMbbS3gtRLgLMfCoAV3TXsk5giavw/132" width="30px"><span>Geek_b2839b</span> 👍（0） 💬（0）<div>4. 对所有临时文件和内存数据结构中剩余的数据记录做归并排序，生成数据文件和索引文件。
-----------------------
老师，如果临时文件和内存数据文件非常大，无法单节点加载进入内存里，那怎么去归并排序呢</div>2022-05-16</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/13/9d/0ff43179.jpg" width="30px"><span>Andy</span> 👍（0） 💬（0）<div>我在当前项目中，安装了spark2.3.3 手动设置了 SPARK_LOCAL_DIRS 目录。因为我运行程序时没指定cluster模式，默认是master local ，程序会把所有数据（1T数据）拉到提交任务的机器，把tmp写爆了，程序就死了。提交任务时显示指定了 client 或 cluster模式就解决了这个写爆本地磁盘问题（数据都是各各datanode上运行了）。平时程序如果不报没有硬盘空间，我根本不关注spark.local.dir参数。</div>2021-11-12</li><br/>
</ul>