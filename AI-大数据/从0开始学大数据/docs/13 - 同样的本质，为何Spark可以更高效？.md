上一期我们讨论了Spark的编程模型，这期我们聊聊Spark的架构原理。和MapReduce一样，**Spark也遵循移动计算比移动数据更划算这一大数据计算基本原则**。但是和MapReduce僵化的Map与Reduce分阶段计算相比，Spark的计算框架更加富有弹性和灵活性，进而有更好的运行性能。

## Spark的计算阶段

我们可以对比来看。首先和MapReduce一个应用一次只运行一个map和一个reduce不同，Spark可以根据应用的复杂程度，分割成更多的计算阶段（stage），这些计算阶段组成一个有向无环图DAG，Spark任务调度器可以根据DAG的依赖关系执行计算阶段。

还记得在上一期，我举了一个比较逻辑回归机器学习性能的例子，发现Spark比MapReduce快100多倍。因为某些机器学习算法可能需要进行大量的迭代计算，产生数万个计算阶段，这些计算阶段在一个应用中处理完成，而不是像MapReduce那样需要启动数万个应用，因此极大地提高了运行效率。

所谓DAG也就是有向无环图，就是说不同阶段的依赖关系是有向的，计算过程只能沿着依赖关系方向执行，被依赖的阶段执行完成之前，依赖的阶段不能开始执行，同时，这个依赖关系不能有环形依赖，否则就成为死循环了。下面这张图描述了一个典型的Spark运行DAG的不同阶段。
<div><strong>精选留言（30）</strong></div><ul>
<li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/oNyD409Hg3iaSaMpF3ibn35FstWN3AHnQaJf7LaIqkrsvHZcd8lYbOicDiaU1NcicoERz5kC3YKM4iaYsXpHBYEVW6yw/132" width="30px"><span>vivi</span> 👍（71） 💬（1）<div>懂了原理，实战其实很简单，不用急着学部署啊，操作，原理懂了，才能用好，我觉得讲得很好</div>2018-12-25</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/40/10/b6bf3c3c.jpg" width="30px"><span>纯洁的憎恶</span> 👍（12） 💬（4）<div>这两天的内容对我来说有些复杂，很多知识点没有理解透。针对“而 Spark 更细腻一点，将前一个的 Reduce 和后一个的 Map 连接起来，当作一个阶段持续计算，形成一个更加优雅、高效地计算模型”。这句话中“将前一个的 Reduce 和后一个的 Map 连接起来”在细节上该如何理解，这也是明显的串行过程，感觉不会比传统的MapReduce快？是因为不同阶段之间有可能并行么？</div>2018-11-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/16/85/e4d53282.jpg" width="30px"><span>ming</span> 👍（9） 💬（1）<div>老师，有一句话我不太理解，请老师指导。“DAGScheduler 根据代码和数据分布生成 DAG 图”。根据代码生产DAG图我理解，但是为什么生成DAG图还要根据数据分布生成，数据分布不同，生成的DAG图也会不同吗？</div>2018-12-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/72/9e/69606254.jpg" width="30px"><span>张飞</span> 👍（7） 💬（1）<div>1.“而 Spark 更细腻一点，将前一个的 Reduce 和后一个的 Map 连接起来，当作一个阶段持续计算，形成一个更加优雅、高效地计算模型”，stage之间是串行的，即便前一个的reduce和后一个的map连接起来，也是要从前一个stage的计算节点的磁盘上拉取数据的，这跟mapreduce的计算是一样的，老师所说的高效在这里是怎么提现的呢？
2. spark的内存计算主要体现在shuffle过程，下一个stage拉取上一个stage的数据的时候更多的使用内存，在这里区分出与mapreduce计算的不同，别的还有什么阶段比mapreduce更依赖内存的吗？ 
3.我是不是可以这样理解，如果只有map阶段的话，即便计算量很大，mapreduce与spark的计算速度上也没有太大的区别？
可能问题问的不够清晰，希望老师解答一下。</div>2019-03-01</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/Ng7NIuMhg8E3U6DjwJlTKFcEYsTtFJkiag22G13JXSiaobpibfI6MicKg93VNqQnG7Rkvl2OfCsAaSksCAVbNDp8zw/132" width="30px"><span>weiruan85</span> 👍（5） 💬（1）<div>1.完备的技术说明文档是必须的，比如使用场景，常见问题，环境搭建，核心技术的原理等。
2.输出真实等使用案例，以及给解决实际问题带来等好处，比如如果没有我们的开源方案是怎么实现的，有了这个方案是怎么实现的，差异是什么
3.商业推广，找业界有名的公司站台，或者有名的技术大牛做宣传（头羊效应）
4.归根结底，还是得有开创性的技术，能解决现实中的某一类问题。</div>2019-07-31</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/09/70/6b6382ca.jpg" width="30px"><span>白鸽</span> 👍（5） 💬（1）<div>Executor 从 Diver 下载执行代码，是整个程序 jar包?还是仅 Executor 计算任务对应的一段计算程序（经SparkSession初始化后的）?</div>2018-11-30</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/cc/f3/5e4b0315.jpg" width="30px"><span>追梦小乐</span> 👍（5） 💬（2）<div>老师，我想请教几个问题：
1、“根据每个阶段要处理的数据量生成相应的任务集合（TaskSet），每个任务都分配一个任务进程去处理”，是一个任务集合TaskSet启动一个进程，taskSet里面的任务是用线程计算吗？还是每个TaskSet里面的任务启动一个进程？

2、task-time 图中红色密集的表示什么？

3、Spark 的执行过程 的图中 Executor 中的 Cache 是表示内存吗？task和Executor不是在内存中的吗？</div>2018-11-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/64/86/f5a9403a.jpg" width="30px"><span>yang</span> 👍（4） 💬（1）<div>啊、老师现在的提问都好大，我现在是老虎吃天无从下爪啊 ^_^</div>2018-11-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/56/65/22a37a8e.jpg" width="30px"><span>Yezhiwei</span> 👍（3） 💬（1）<div>这里是学习过程中做的一些总结

https:&#47;&#47;mp.weixin.qq.com&#47;s&#47;OyPRXAu9hR1KWIbvc20y1g</div>2019-01-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/17/96/a10524f5.jpg" width="30px"><span>蓬蒿</span> 👍（3） 💬（1）<div>“DAGScheduler 根据程序代码生成 DAG，然后将程序分发到分布式计算集群，按计算阶段的先后关系调度执行。Worker 收到任务后，启动 Executor 进程开始执行任务。Executor 先检查自己是否有 Driver 的执行代码，如果没有，从 Driver 下载执行代码，通过 Java 反射加载后开始执行。” 针对这一段话，我想多请教老师一些，我理解的DAGScheduler 根据程序代码生成 DAG，类似于关系型数据库优化器根据SQL生成执行计划，然后spark计算引擎根据这些计划去做计算，我的疑惑的是：DAG已经是根据代码生成的了，那Worker 还要从 Driver 下载执行代码去执行，我无法想象worker是如何执行代码的，能否帮忙解疑一下？</div>2018-12-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/d7/d5/b9e3332e.jpg" width="30px"><span>星凡</span> 👍（2） 💬（1）<div>老师您好，请问一下，对于复杂的多阶段计算，Hadoop MapReduce是需要进行多次map reduce 过程吗，而且每次map和reduce之间一定会进行shuffle（主要使用磁盘进行存储），所以相比Spark才更加低效，不知道我理解的正确嘛，请指教</div>2019-10-06</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/37/7c/b6bc6024.jpg" width="30px"><span>冰ྂ镇ྂ可ྂ乐ྂ</span> 👍（2） 💬（1）<div>之前讲mr时候也有提到生成dag，spark这里也是dag，二者的差异是mr中，map reduce为一组操作(可能没有reduce)的一个job job之间是依赖关系，而spark并非简单依照m r划分而是针对数据的处理情况，如果r后到下一个m是窄依赖，则属于同一个stage，属于一个流程，这样理解对吗？</div>2019-04-30</li><br/><li><img src="" width="30px"><span>尼糯米</span> 👍（2） 💬（1）<div>1、DAGScheduler根据应用构造执行的DAG：是不是一个应用便构造一个DAG
2、DAG划分出计算阶段
3、每个计算阶段，根据要处理的数据量，为每个数据分片生成一个对应的任务，这些任务组成一个任务集合
4、每个任务分配一个进程
5、分布式计算：某个计算阶段，其某个任务的进程在集群某处执行计算
6、执行action函数便生成作业：依据DAG计算，是不是便可以生成多个作业

我这么理解可以吗？</div>2019-01-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/df/73/4a4ce2b5.jpg" width="30px"><span>足迹</span> 👍（2） 💬（1）<div>老师，根据大数据技术，程序移动，数据不动的原理。是不是应该在每个DataNode节点上面安装Spark呢？</div>2018-12-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/32/3f/fa4ac035.jpg" width="30px"><span>sunlight001</span> 👍（2） 💬（1）<div>老师，多出几本书吧，我保证全买☺，这个专栏真值！</div>2018-11-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/6e/35/11008e02.jpg" width="30px"><span>forever</span> 👍（1） 💬（2）<div>老师spark是内存计算，是把数据都拿到内存算吗，shuffle的时候，如果两个父rdd不在同一个work节点，是不是需要把不同节点的数据移动到其中一个节点内存里，做聚合。这是不是也是移动数据</div>2019-02-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/64/14/c980c239.jpg" width="30px"><span>chenssy</span> 👍（1） 💬（1）<div>老师你好，是否可以过滤掉MapReduce，直接学习 spark</div>2019-02-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/e4/f4/96fa9deb.jpg" width="30px"><span>李勇</span> 👍（0） 💬（1）<div>老师，有个问题想咨询一下，在rddB和RDDF join的过程中，RDDB是窄依赖，RDDF是宽依赖。也就是说RDDB直接平移到下一个RDD中，而RDDF会对RDDB存在的分片做数据交叉。这里我有个问题，为什么是RDDF做数据平移而不是RDDB呢？有什么规则可遵循的么？</div>2022-04-06</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/47/00/3202bdf0.jpg" width="30px"><span>piboye</span> 👍（0） 💬（2）<div>感觉Spark 这个Driver 跟之前的东西都不一样了， 这个Driver 是在Cluster 之外的感觉， Cluster Mannger 是 资源的 提供者。 Job 的管理和执行完全是在集群外的Driver 自己处理，不知道这里理解对不？</div>2022-01-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/47/00/3202bdf0.jpg" width="30px"><span>piboye</span> 👍（0） 💬（1）<div>老师driver也是运行在spark集群中吗？还是只是客户端的机器上？</div>2022-01-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/2c/56/ff7a9730.jpg" width="30px"><span>许灵</span> 👍（0） 💬（2）<div>老师，这里有一个疑问: 如果spark用k8s部署，spark是怎么与hdfs协作的呢？如何做到移动计算而不是移动数据，hadoop也要用k8s部署吗？</div>2021-08-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/3c/c4/4ee2968a.jpg" width="30px"><span>艾利特-G</span> 👍（0） 💬（1）<div>我入职了Cloudera，虽然股票让人感觉沮丧，我觉得产品和技术还是挺好的。
关于开源产品如何提升影响力，我觉得要和公有云搞好关系以及当前最火的行业开源软件合作。当然，这也是现在看到k8s这么火之后的马后炮啦～</div>2020-11-02</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/e8/81/6692218b.jpg" width="30px"><span>李凯</span> 👍（0） 💬（1）<div>之后再根据每个阶段要处理的数据量生成相应的任务集合（TaskSet），每个任务都分配一个任务进程去处理，Spark 就实现了大数据的分布式计算。
我有点不明白，每个任务不应该是一个线程处理吗？难道你这个任务是指任务集合，所以要启动一个进城？</div>2019-10-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/d7/d5/b9e3332e.jpg" width="30px"><span>星凡</span> 👍（0） 💬（1）<div>老师您好，请教一下，上面关于作业、计算阶段、任务的依赖和时间关系图中，说到，两条粗黑线之间是一个作业，两条细线直接是一个计算阶段，那两个细线之间夹了一条粗黑线这个怎么算。。我的理解是分属两个作业的各一个计算阶段，不知道我的理解正确嘛</div>2019-10-06</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1a/10/3a/053852ee.jpg" width="30px"><span>张小喵</span> 👍（43） 💬（1）<div>把12|13反复读了4、5遍，以下是我的感悟
Spark再次理解：
	1：Spark计算框架编程和运行速度比MapReduce更加的简单和快
	编程更简单：Spark编程关注的数据是RDD，RDD是个抽象的，比较不好理解，我的理解RDD是一次计算阶段中 要操作的所有的数据的抽象，虽然它们是分片的，并且分布在HDFS的任意节点上，但是概念上，我们是针对这个抽象的RDD编程的。使用Scala编程，wordcount只需要三行代码，很简单是吧，但是背后的整体的计算过程是相当的复杂的。这样看我们在MapReduce中的编程要是关注所有的数据的，默认为map的数据输入的数据是整个要处理的数据，并不是说，其他的应用就不知道了，毕竟我们也可以在代码中感知到在文件中的偏移量这种东西。
	速度更快：MapReduce暴力的把计算阶段分为两个阶段，Map和Reduce阶段， 如果一个应用的计算实现只有两个阶段，那么MapReduce计算框架的速度不会比Spark慢多少，慢的地方只是在于Spark是不经过落盘的操作的，直接在内存中存储，但是如果一个应用的计算阶段变得很多的话，比如机器学习中的迭代计算，那么使用MapReduce的就非常慢了，如果这个应用的计算分为10000个计算阶段，如果用MapReduce实现，就需要启动5000次相关的应用，速度很慢，并且编码会很麻烦，如果 是Spark，那么在一次应用就可以解决该问题。

Spark的多个计算阶段的理解：
	相比于MapReduce只有两个计算阶段， Spark理论上可以有无限个计算阶段， 这也是Spark的速度的优势
	Spark的计算阶段的表示中，DAG（有向无环图）是Spark的关键，DAG可以很好的表示每个计算阶段的关系，或者说依赖书序
	那么DAG是谁生成的呢，是根据什么生成的呢？
		DAG是有Spark计算框架根据用于所写的代码生成的，那怎么依据代码的什么生成的呢？
			类比MapReduce的两个计算阶段，两个阶段之间的过度是什么？是shuffle，Spark也是根据Spark中的代码中的转换函数是否是有shuffle操作进行划分阶段的！
	我的理解，Spark的每个计算阶段可以类比MapReduce中的Map阶段或者Reduce阶段。不同的是，Spark计算阶段关注的是RDD，但是又有相同的点，RDD中的数据组成也是一片一片的，Spark中的最小的任务也就是对于片的计算，原理和MapReduce一样，Spark中的片和MapReduce中的片是通一个东西，每个片都是分布于HDFS上的，对于每个片的计算大概率也是在片所在的计算节点的。所以Spark的计算也是分布式，并且原理和MapReduce是一样的。

Spark中RDD上的操作函数：RDD上的操作函数分为两种类型，一种是转换函数，另一种是action函数
	转换函数：Spark编程中对于RDD的操作基本是用转换函数来完成的，转换函数是计算RDD，转换函数又分为两种
		只是改变RDD内容的转换函数：类似map，filter函数，RDD本身物理上没有变化，所有的操作都是针对于当前的分片
		会新生成RDD转换函数：类似于reduceByKey这种函数，会组合key生成新的RDD（所有的会生成新的RDD的函数都可以作为 计算阶段的分割函数吗？）
	action函数：aciton函数对于RDD的操作没有返回值，或者说不会改变RDD的内容，比如rdd.saveToPath等等

Spark中一些关于应用的生命周期中的过程的名词、概念：
	Spark中的RDD函数主要有两种，一是转换函数，调用转换函数可以返回一个RDD（产生新的RDD？&#47;会shuffle的函数分割计算阶段），RDD的计算逻辑主要是由转换函数完成

	另一种是action函数，调用这种函数不返回RDD，DAGScheduler在遇到shuffle的时候生成一个新的计算阶段，在遇到action函数的时候，产生一个作业。（我理解可以类似于，一次MapReduce程序对应Spark中的一个作业）
	在每个计算阶段都是针对RDD（包含很多片）的计算，每个分片Spark都会创建一个计算任务去处理，所以每个计算阶段会包含很多个计算任务</div>2019-12-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/f7/9d/be04b331.jpg" width="30px"><span>落叶飞逝的恋</span> 👍（38） 💬（0）<div>总结：Spark的优点就是能够动态根据计算逻辑的复杂度进行不断的拆分子任务，而实现在一个应用中处理所有的逻辑，而不像MapReduce需要启动多个应用进行计算。</div>2018-11-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/bd/fd/87b5d5d7.jpg" width="30px"><span>scorpiozj</span> 👍（23） 💬（0）<div>移动计算比移动数据划算 总结的真好 很多设计仔细想一想都是围绕这个中心

关于开源
1 准备好详细的使用 api文档并提供示例
2 撰写设计思路 和竞品比较的优势 以及创新点
3 提前联系若干团队使用产品 并请他们提供真实的提高效率的数据报告
4 联系公关团队在知名技术论坛推广
5 成立团队 及时响应开发者疑问 需求和pr等</div>2018-11-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/71/e5/bcdc382a.jpg" width="30px"><span>My dream</span> 👍（22） 💬（7）<div>老师，你讲的理论看的我头晕脑胀的，能不能讲点实战操作，搭建spark环境，通过案例来讲的话，对于我们这些初学学生来说是最直观，最容易弄明白它为什么会那么快，像你这样一味的讲理论，不讲实战，我们实在是吸收不了，理解不了你讲的这些知识点</div>2018-11-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/1c/51/dc21bb08.jpg" width="30px"><span>周洋舟</span> 👍（7） 💬（0）<div>每一篇文章都认真的读了，有些东西还没真正的去在实际工作中体会到，但这种思维的启发还是受益匪浅。</div>2018-11-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/97/b4/2ec7a386.jpg" width="30px"><span>海</span> 👍（5） 💬（0）<div>对于hbase和高速发展的es，不知道您怎么看，他们的优缺点是什么？</div>2019-03-07</li><br/>
</ul>