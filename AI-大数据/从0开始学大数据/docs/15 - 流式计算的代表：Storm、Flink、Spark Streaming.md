我前面介绍的大数据技术主要是处理、计算存储介质上的大规模数据，这类计算也叫大数据批处理计算。顾名思义，数据是以批为单位进行计算，比如一天的访问日志、历史上所有的订单数据等。这些数据通常通过HDFS存储在磁盘上，使用MapReduce或者Spark这样的批处理大数据计算框架进行计算，一般完成一次计算需要花费几分钟到几小时的时间。

此外，还有一种大数据技术，针对实时产生的大规模数据进行即时计算处理，我们比较熟悉的有摄像头采集的实时视频数据、淘宝实时产生的订单数据等。像上海这样的一线城市，公共场所的摄像头规模在数百万级，即使只有重要场所的视频数据需要即时处理，可能也会涉及几十万个摄像头，如果想实时发现视频中出现的通缉犯或者违章车辆，就需要对这些摄像头产生的数据进行实时处理。实时处理最大的不同就是这类数据跟存储在HDFS上的数据不同，是实时传输过来的，或者形象地说是流过来的，所以针对这类大数据的实时处理系统也叫大数据流计算系统。

目前业内比较知名的大数据流计算框架有Storm、Spark Streaming、Flink，接下来，我们逐一看看它们的架构原理与使用方法。

## Storm

其实大数据实时处理的需求早已有之，最早的时候，我们用消息队列实现大数据实时处理，如果处理起来比较复杂，那么就需要很多个消息队列，将实现不同业务逻辑的生产者和消费者串起来。这个处理过程类似下面图里的样子。
<div><strong>精选留言（30）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/10/4a/de/1289a35d.jpg" width="30px"><span>李鼎(哲良)</span> 👍（163） 💬（5）<div>数据流是久经考验的典型思路，在网络协议（如TCP）、数据平台这样场景，早就应用多年习以为常了。淘宝业务的应用架构升级可以认为是把这样思路应用到了业务系统开发中，把『流』作为业务表达上的一等概念和手段，并在业务架构&#47;系统能力优化提升。

简单地说，因为业务面向数据流来编写，一方面业务逻辑表达可以自然接近业务流程；另一方面逻辑运行可以是全异步有很好的性能提升，一核心后端应用在双11线上，单机QPS提升30%，RT下降40%。流程的表达与异步&#47;同步执行方式是分离的（如果了解过像RxJava，这句会容易理解：）。

另外，『流』也为业务系统的保护提供新的一些方法，在思路上其实和流计算平台是一样的，这对业务大型系统的稳定性来非常重要。

当然，业务的流式架构，在业务编写上有些FP风格（简单地说比如充分使用了Lambda），平时我们大家业务上主要是用命令式顺序平铺方式来表达，会有要个熟悉过程，虽然不见得有多难 :)</div>2018-12-06</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/00/f4/cc5f0896.jpg" width="30px"><span>Jowin</span> 👍（12） 💬（1）<div>智慧老师，我是从事金融实时数据处理的，有一类典型需求是从原始实时数据计算出各种衍生数据，但是有状态积累。比如，当前状态是S0，收到数据A0，此时要根据(S0,A0)生成数据A1，同时要更新当前状态S1，后续的新数据再基于S1处理。团队考虑过使用Stream作为计算平台，有两个问题没想清楚怎么处理：
1）如果计算任务故障挂掉，会不会导致这期间的数据丢失？
2）另外，由于数据量也不小，差不多在每秒4~5万条消息，状态S的更新特别频繁，常规的存储在性能上没有办法满足，所以我们是采用内存+日志文件保存。如果重启的任务被分配套新的服务节点上，我们是否就还得考虑这部分数据也要迁移过去？
盼复，谢谢。</div>2018-12-01</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/d7/d5/b9e3332e.jpg" width="30px"><span>星凡</span> 👍（11） 💬（1）<div>文中有这么一段话：“回到流计算，固然我们可以用各种分布式技术实现大规模数据的实时流处理，但是我们更希望只针对小数据量进行业务开发，然后丢到一个大规模服务器集群上，就可以对大规模实时数据进行流计算处理。”，在下愚昧，没有get到，不用分布式技术实现大规模数据实时流处理的真正原因是？</div>2019-10-06</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/04/1c/b0c6c009.jpg" width="30px"><span>zhj</span> 👍（7） 💬（1）<div>1面向数据流的编程在java里逐渐展露头角，之前rxjava更多的是用于android，直到hystrix才算是后端一个大规模应用的案例(也和场景有关吧，后端的大多业务都是短事物处理去构建一条数据流水线反倒显得累赘)，reactor是响应式编程的另一个实现，直到spring5全面拥抱以后，才完全进入人们视野(所以技术落地离不开大厂的支持)，单纯的业务层处理构造一条很短的数据流意义不大(因为数据源可能还是需要返回所有数据),spring webflux结合springdata从持久层到业务层构建了自下而上的数据流(前提是持久层驱动是非阻塞的),并利用reactor-netty(支持网络背压)，理想情况下将构建一个全链路的按需处理数据流
2 数据流编程，有点类似当年面向函数-&gt;面向对象，更多的是思考方式的改变，异步和数据流都是为了正确的构建数据流间的关系而存在，不过目前貌似不支持对数据流分片并行处理</div>2019-01-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/8b/e0/9a79ddac.jpg" width="30px"><span>🐱您的好友William🐱</span> 👍（5） 💬（1）<div>主攻人工智能，机器学习和算法实现的应该学习哪种呢？Storm，Spark还是Flink呢？</div>2018-12-04</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/d4/f3/129d6dfe.jpg" width="30px"><span>李二木</span> 👍（3） 💬（1）<div>和老师探讨一个问题，对于架构设计，目前流行的是微服务，我个人觉得微服务还是有好些缺点。架构从开始的合走到现在的分，未来会不会从分又到和呢？</div>2018-12-01</li><br/><li><img src="" width="30px"><span>Geek_ea2bf8</span> 👍（0） 💬（1）<div>智慧老师，通常的场景是，已经有大量的存量数据，在离线的Hadoop中，又有实时需求，依赖于历史存量数据，和当日的实时数据。这种典型场景，架构应该如何设计啊？</div>2023-07-25</li><br/><li><img src="" width="30px"><span>Geek_8593e5</span> 👍（0） 💬（1）<div>Flink 处理实时数据流的方式跟 Spark Streaming 也很相似，也是将流数据分段后，一小批一小批地处理。（？这没听懂）   Flink是分批的吗？</div>2022-03-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/6b/4c/c15c0fdf.jpg" width="30px"><span>万～～</span> 👍（27） 💬（2）<div>你好 storm spark flink 都是优秀的框架 那我们应该学习哪个呢？ 都学肯定精力不够 而且难以精通</div>2018-12-01</li><br/><li><img src="" width="30px"><span>laurencezl</span> 👍（18） 💬（3）<div>智慧老师你好，这节对storm.spark.flink的介绍感觉过于概述了！后面是否会有详细的文章介绍，比如分析对比一下他们三者各自优缺点在哪里？各自试用与不适用的业务场景有哪些之类的呢？</div>2018-12-04</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/40/10/b6bf3c3c.jpg" width="30px"><span>纯洁的憎恶</span> 👍（13） 💬（0）<div>批计算是对历史数据的一次性处理，流计算是对实时流入的数据实时响应。

storm模仿消息队列（什么是消息队列？卡夫卡？），把消息队列中与业务逻辑无关的过程部分抽象出来形成标准框架，实现复用。开发者不用纠结四面八方涌入的实时数据如何流转，消息如何处理和消费，只用考虑业务流程、数据源、处理逻辑。 

spark streaming以spark为基础，将同一时间段的数据分片聚合在一起做为一批数据处理（以批模拟流）。

flink则是以流模拟批，它的底层计算逻辑只有流，通过时间窗口把流入数据按时间间隔分为若干批（与spark streaming类似），通过数据源的不同，完成在流与批的切换。

计算机软件的发展史就是一部业务与技术分离的历史，通过把业务不相关部分高度抽象并标准化，开发者能够越来越多的专注于业务流程，而越来越少的考虑机器、程序等技术细节的因素。

不知这么理解对不对。

需要进一步明确的知识点：消息队列。</div>2018-12-01</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/d6/dd/94994606.jpg" width="30px"><span>常平</span> 👍（9） 💬（0）<div>流式架构本质上是事件驱动（event-Driven）架构，流由段（segment）组成，段由事件（event）组成，事件由字节（bytes）组成，事件大小有限，而字节流大小无限</div>2018-12-11</li><br/><li><img src="" width="30px"><span>尼糯米</span> 👍（4） 💬（0）<div>问题一
Strom算是比较早期的大数据流计算框架
	》》定义处理流程
	》》流程的每个环节上的处理逻辑
数据流转是计算框架按处理流程进行流转吗？
从作者的陈述，实在看不出这和实时数据有啥关系，把它的计算框架套在批数据上也不伪和，
至少文中不指明是为了流计算，实在看不出来

问题二
Spark Streaming实现的流计算
是通过把流数据切分迷你批数据且每个迷你批数据的处理非常迅速，
而这个迷你批数据是怎么做容错呢，切分出来的数据总要做容错吧

问题三
Flink不管是批数据还是实时数据流，对它只是数据源不同，这点从源码上切实看出来了，
它确实要构建一个数据源出来，在数据源上做各种数据处理。
但是我从作者描述中理解到的东西：数据处理终究还是避免不了对数据的分段，
所以，不管是怎样的流计算框架，把数据处理总是以数据分片的基础上进行呢

如果是这样，流计算喊出来还是响当当，蛮吓人的
希望看到的各位老师批评下

PS，该篇小结太多了，小结之上倒是不多</div>2019-01-10</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/THkFNC52F0lbGLm8VOU9xRjhAvZ8H4xl97Qaq38MgsFyJj0zMzlbiab4usvVyFDKawh3EMfvOM1hL8AWFY7Seog/132" width="30px"><span>qiaoer</span> 👍（3） 💬（0）<div>老师讲了Storm，Flink，Spark Streaming，感觉他们几个很相似，都是Master&#47;slave 结构，一个Master节点进行 任务划分管理，然后下发到Slave节点，Slave负责具体的执行。 但是他们的区别是什么？还有Flink和Spark Streaming他们都是Micro Streaming的思路？那么适用的场景又是什么呢？</div>2019-10-30</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/cb/50/66d0bd7f.jpg" width="30px"><span>杰之7</span> 👍（3） 💬（0）<div>通过本小节的学习，了解了常用的流计算及它们的计算框架，其中Spark Streaming巧妙了运用Spark计算速度的优势，将Spark批计算通过时间间隔装置成流计算。在我们的生活中，股票交易的价格传输应该就是运用了流计算，要求在极短的时间内完成对价格的改变。当然，淘宝，一线城市的摄像头在后台处理上也应用了流计算技术。相比批计算技术，流计算在重要的数据上会用的越来越广。</div>2018-12-01</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/e8/52/97f59d07.jpg" width="30px"><span>。。。。</span> 👍（1） 💬（1）<div>完全没有看出来flink在流处理的流程上和spark streaming有啥区别，老师后面的文章有没详细解读呢</div>2019-06-04</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/26/bc/df/30cdd506.jpg" width="30px"><span>云端团队</span> 👍（0） 💬（0）<div>现在还是这些东西：微服务、容器、服务编排、Serverless  马上2025年了</div>2024-12-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/47/00/3202bdf0.jpg" width="30px"><span>piboye</span> 👍（0） 💬（0）<div>大数据计算 目前 接口抽象都是往sql 方向， 那业务流化之后，是否也会往sql 或者 graphql 这样的方式呢？</div>2022-01-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/25/09/cf/7e3a43ee.jpg" width="30px"><span>薛猫</span> 👍（0） 💬（0）<div>老师，可不可以说一下tez计算框架</div>2021-09-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/26/6f/4f/3cf1e9c4.jpg" width="30px"><span>钱鹏 Allen</span> 👍（0） 💬（0）<div>Storm,Spark Streaming,Flink 有相似的架构，Flink再原先Spark Streaming的基础上升级流式窗口计算，在学习时，需要把握技术演变的主线。</div>2021-09-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/8c/5c/3f164f66.jpg" width="30px"><span>亚林</span> 👍（0） 💬（0）<div>重点是在讲编程技术发展史</div>2021-07-30</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/22/22/8a/7cfb84ca.jpg" width="30px"><span>张翠娟</span> 👍（0） 💬（0）<div>Storm和Spark Streaming 哪个更优秀</div>2021-03-16</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/67/f4/9a1feb59.jpg" width="30px"><span>钱</span> 👍（0） 💬（0）<div>纵观计算机软件发展史，发现这部历史堪称一部技术和业务不断分离的历史。人们不断将业务逻辑从技术实现上分离出来，各种技术和架构方案的出现，也基本都是为这一目标服务——这个很认同，所有工具的发展，人类都会趋于这种改进方式来处理。

流式计算，特点是否就是对实时数据的计算，数据像流水一样无穷无尽？</div>2019-09-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/d7/7e/6b6384e9.jpg" width="30px"><span>不贰过先生</span> 👍（0） 💬（0）<div>老师说flink也是将实时的数据流分成一小段一小段处理，这样的话和spark streaming本质上没有区别了？</div>2019-06-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/c1/60/f5439f04.jpg" width="30px"><span>Geek_dn82ci</span> 👍（0） 💬（0）<div>想了解storm与flink以及spark streaming 相比有什么区别？感觉后两者都是将数据源做很细粒度的切分，最终看上去“像”是连续的流，那么storm的处理方式呢？</div>2019-02-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/91/bb/481c5b62.jpg" width="30px"><span>Geek_4d3c4b</span> 👍（0） 💬（0）<div>好</div>2018-12-25</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/95/8a/caa2fea7.jpg" width="30px"><span>洪喜</span> 👍（0） 💬（0）<div>感谢老师的讲解，不过也印证了师傅领进门修行在个人这句话，个人需要针对没深入讲解的知识点再次深入自学了。</div>2018-12-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/1a/e2/9e59dd38.jpg" width="30px"><span>修行者</span> 👍（0） 💬（1）<div>想要了解这三种流式计算框架 Strom、Flink、Spark Streaming，各种的优缺点及适用的业务场景，智慧哥在下面的专栏会详细介绍吗 ？</div>2018-12-07</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/94/7d/7d056e1f.jpg" width="30px"><span>提米XXVII🌻</span> 👍（0） 💬（0）<div>老师好，我现在场景是针对一次请求单纯的并行计算后结果合并（单机内存限制和速度考虑），无存hdfs要求，spark合适吗？</div>2018-12-07</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/pEsmmPPRZictCKpQM8ZzzWRVdC3OMHJjUvXeBuD7mibPrrwRJp8nYqAibWfSpEAJFWuL18b6Uek1PA0XOGYcvItjw/132" width="30px"><span>WesleyWong</span> 👍（0） 💬（0）<div>使用spark 进行计算， 用Java 还是 scala 呢？现在项目组用的JAVA，后面想用scala. 如何取舍呢</div>2018-12-05</li><br/>
</ul>