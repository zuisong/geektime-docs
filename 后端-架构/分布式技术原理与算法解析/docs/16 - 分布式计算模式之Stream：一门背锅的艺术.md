你好，我是聂鹏程。今天，我来继续带你打卡分布式核心技术。

在上一篇文章中，我与你介绍了分布式计算模式中的MapReduce模式。这种模式的核心思想是，将大任务拆分成多个小任务，针对这些小任务分别计算后，再合并各小任务的结果以得到大任务的计算结果。

这种模式下任务运行完成之后，整个任务进程就结束了，属于短任务模式。但，任务进程的启动和停止是一件很耗时的事儿，因此MapReduce对处理实时性的任务就不太合适了。

实时性任务主要是针对流数据的处理，对处理时延要求很高，通常需要有常驻服务进程，等待数据的随时到来随时处理，以保证低时延。处理流数据任务的计算模式，在分布式领域中叫作Stream。

今天，我将针对流数据的处理展开分享，和你一起打卡Stream这种计算模式。

## 什么是Stream？

近年来，由于网络监控、传感监测、AR/VR等实时性应用的兴起，一类需要处理流数据的业务发展了起来。比如各种直播平台中，我们需要处理直播产生的音视频数据流等。这种如流水般持续涌现，且需要实时处理的数据，我们称之为**流数据**。

总结来讲，流数据的特征主要包括以下4点：

- 数据如流水般持续、快速地到达；
- 海量数据规模，数据量可达到TB级甚至PB级；
- 对实时性要求高，随着时间流逝，数据的价值会大幅降低；
- 数据顺序无法保证，也就是说系统无法控制将要处理的数据元素的顺序。
<div><strong>精选留言（23）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/12/20/b7/bdb3bcf0.jpg" width="30px"><span>Eternal</span> 👍（14） 💬（1）<div>
老师课后思考题：“离线计算和批量计算，实时计算和流式计算是等价的吗？”

其实留言去已经有小伙伴总结得很好（自认为，如果有错望指正）：
离线计算、批量计算、实时计算、流式计算都是要计算的，这是它们的共同特点；

批量和流式是描述计算的时候计算资源的特点的，是描述计算数据的维度。
    批量计算
    	是等到计算数据积累到一定数量才开始计算
    流式计算
    	是数据量很小时候就可以开始计算，有了资源就可以开始，源源不断

离线和实时是描述计算的时效性，是描述计算的维度。
    离线计算
    	因为计算数据不能来了就计算，需要累计到一定阈值，所以按照时效性来说，计算是离线的
    实时计算
    	因为计算数据来了就开始计算，计算没得延迟，，所以按照时效性来说，计算是实时的

批量和流式是一个维度，离线和实时是另外一个维度，但是两个维度之间又有联系：
因为目前现有的技术发展，不能大批量计算做到实时的效果，所以只能少量资源做到实时计算，且通过流式计算来达到实时的效果；
但是如果一旦当前的硬件指标和技术能力突破后，能大批量计算做到实时的效果，这也是可能的。因此我认为，我们的演进目标是想能
做到批量实时的。两个维度之间由相关联的因素来驱动它们相互变化。
</div>2019-11-02</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/c0/6c/29be1864.jpg" width="30px"><span>随心而至</span> 👍（5） 💬（0）<div>In computer science, an online algorithm[1] is one that can process its input piece-by-piece in a serial fashion, i.e., in the order that the input is fed to the algorithm, without having the entire input available from the start.

In contrast, an offline algorithm is given the whole problem data from the beginning and is required to output an answer which solves the problem at hand.

In computer science, streaming algorithms are algorithms for processing data streams in which the input is presented as a sequence of items and can be examined in only a few passes (typically just one). In most models, these algorithms have access to limited memory (generally logarithmic in the size of and&#47;or the maximum value in the stream). They may also have limited processing time per item.

In computer science, real-time computing (RTC), or reactive computing describes hardware and software systems subject to a &quot;real-time constraint&quot;, for example from event to system response.[1] Real-time programs must guarantee response within specified time constraints, often referred to as &quot;deadlines&quot;. 


从维基百科的定义可以，他们侧重的点不同，个人总结如下：
1.online algorithm  只能看到数据的一部分，必须基于此做决定（可能不是最优的）
2.offline algorithm 可以看到解决问题的所有数据
3.streaming algorithms 处理序列流（内存有限，流大小有限，单个序列项处理时间有限）
4.real-time computing 强调响应时间,有时间限制。 

参考自https:&#47;&#47;en.wikipedia.org&#47;wiki&#47;Online_algorithm 及其See also:


</div>2019-10-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/3b/47/f6c772a1.jpg" width="30px"><span>Jackey</span> 👍（5） 💬（0）<div>不太好说是否等价，因为离线和实时是针对时延判断的，批量和流式是针对数据处理方式判断的。只能目前说离线和批量使用的框架、处理方法相同（实时和流式相同）。但如果以后发展出能批量进行实时数据计算的计算机就不能说批量=离线了吧</div>2019-10-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/90/db/02aa2247.jpg" width="30px"><span>林通</span> 👍（2） 💬（0）<div>storm都快被淘汰了吧，为啥不讲讲最流行的框架呢</div>2020-11-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/c0/6c/29be1864.jpg" width="30px"><span>随心而至</span> 👍（2） 💬（0）<div>聂老师从一般到具体，讲的真好。
我认为批量计算是离线计算的一种实现方式；流式计算是实习计算的一种实现方式。待会我查下他们的定义看看自己理解的对不对</div>2019-10-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/a1/e6/50da1b2d.jpg" width="30px"><span>旭东(Frank)</span> 👍（2） 💬（2）<div>如果历史数据回放进行就处理也算流量处理吧；个人认为注意区别点还是处理数据的时效性，如果对处理结果不要求那么及时，新鲜。

流处理就像喝豆浆，批量处理像吃豆腐。</div>2019-10-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/6b/6a/798232a8.jpg" width="30px"><span>信xin_n</span> 👍（1） 💬（0）<div>终于明白了 Nimbus 和 Supervisor 的关系了</div>2019-11-16</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/fe/b4/295338e7.jpg" width="30px"><span>Allan</span> 👍（0） 💬（0）<div>1、离线计算和批量计算，实时计算和流式计算是等价的吗？你能和我说说你做出判断的原因吗？

离线计算数据已经过去的数据了，基于这些数据进行某时段统计。批量技术可以是离线计算任务也可以实时任务，实时任务的时候就是根据时间窗口进行时间窗口内的批量数据进行计算；实时计算就是实时数据的计算，流式计算只是计算的模式采用流式的架构进去的。</div>2024-08-22</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/3Mf5ickZ4gwXXM0kO04EtWY6icTswVNSg1H8bhy72b5ErNjbmKkawcneovickGfmK1OkfhfIZ2Fib77e2uLIsiaH4aw/132" width="30px"><span>lcken</span> 👍（0） 💬（0）<div>flink也应该纳入流式计算框架。它是以流计算批数据的</div>2020-04-03</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/17/c1/66/e8dfeef4.jpg" width="30px"><span>王涛</span> 👍（0） 💬（0）<div>MR 针对静态数据，Stream 针对动态数据。并实时性较高。</div>2020-03-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/17/c1/66/e8dfeef4.jpg" width="30px"><span>王涛</span> 👍（0） 💬（0）<div>继续打卡</div>2020-03-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/67/f4/9a1feb59.jpg" width="30px"><span>钱</span> 👍（0） 💬（0）<div>阅过留痕
知识盲区地带，流式计算没接触过，概念大概能明白。
流数据的价值会随时间的流逝而降低，“时间就是金钱”在流计算中体现得淋漓尽致。这就要求流计算框架必须是低延迟、可扩展、高可靠的。
不过流计算框架具体怎么实现低延迟、可扩展、高可靠的没领会到。</div>2020-02-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/5b/70/6411282d.jpg" width="30px"><span>陈</span> 👍（0） 💬（0）<div>老师请问流计算怎么做增量计算？</div>2019-11-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/1f/9c/6e37e32b.jpg" width="30px"><span>simon</span> 👍（0） 💬（0）<div>流计算看上去，这些框架跟普通的分布式微服务框架是不是一样，都是可以并发处理实时数据，并且可以横向扩展？</div>2019-11-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/c1/3a/2ce09963.jpg" width="30px"><span>张先生</span> 👍（0） 💬（0）<div>实习的时候做过写过mapreduce和storm的代码，一直不是特别清楚两者的区别，看了这篇文章豁然开朗</div>2019-11-04</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/20/b7/bdb3bcf0.jpg" width="30px"><span>Eternal</span> 👍（0） 💬（0）<div>继续打卡

分布式计算了解的很少，这几节引起我的兴趣和思考，很受益。
老师将流式计算的一个节点定义成一个拓扑节点，这个让我想到了一个点:
计算机CPU由计算单元，控制单元，内存组成。CPU的计算由很多与门、非门等控制电路组成。
计算机的发展从单机单核，到单机多核，到分布式多核，这是不断的最求性能提升的发展趋势。
如果我们想要用分布式集群来模拟单机单核的计算怎么做呢？也就是通过一个进程来模拟一个CPU最底层的门电路计算。
由上面的推演让我想到了，流式计算将一个CPU的计算能力抽象成了一个进程，也就是老师讲的一个计算拓扑节点，这样我们
就可以获取更加超大规模的分布式计算能力了。

老师总结的流式计算特点：持续产生，易逝，实时。CUP的计算也有类似的特点。
流式计算的节点计算规则可以自定义，CPU的计算逻辑不能很轻易的更新。


再想到一个点：华为将原来通过软件处理的很多能力通过Soc集成到芯片中，这样来提高芯片的处理能力，但是Soc制作成本（俗称流片）很昂贵。
而分布式计算将本来硬件处理的能力抽象到软件层面来实现，这样可以更加灵活，也突破了传统计算机计算的边界。
两者走的是不同的方向，虽然它们的场景可能不经相同，但是都是为了提升计算性能而做的努力。

以上纯属自己的相互思考和联系，望大牛们看到到错误后能给与指正，谢谢！
</div>2019-11-02</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/4b/d4/b7719327.jpg" width="30px"><span>波波安</span> 👍（0） 💬（0）<div>spark streaming就是使用的批处理方式实现的实时计算</div>2019-11-01</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/4b/d4/b7719327.jpg" width="30px"><span>波波安</span> 👍（0） 💬（0）<div>离线和实时是指数据处理的时延。批量和流式是指数据处理的方式。</div>2019-11-01</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/e9/1a/6ba207a3.jpg" width="30px"><span>天天向善</span> 👍（0） 💬（0）<div>实时天气预报，直播音视频处理，在流式计算中是计算什么，没有概念，能介绍下吗</div>2019-10-31</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/34/df/64e3d533.jpg" width="30px"><span>leslie</span> 👍（0） 💬（0）<div>    离线计算和批量计算不是等价的：批量计算不一定离线，需要使用在线资源；离线计算则是使用闲置资源，时间和线上压力还是不同的。离线计算是批量计算的一种形式，但是离线计算不一定是批量计算。    
    实时计算和流式计算不是等价的：实时计算是当下-个体，流式计算可能是处理一组实时计算。流式计算是有1个或者多个实时计算通过分布式处理之后处理完再发送出去的结果；实时计算则是拿到就处理，处理完了就把结果发送出去。
    这是我个人对于老师课程的理解：期待老师答案的公布以及后面的继续分享。通过老师对分布式计算的讲解，解释明白了分布式技术的核心。</div>2019-10-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/ef/0e/618689da.jpg" width="30px"><span>有人@我</span> 👍（0） 💬（0）<div>分布式跟流水计算好像没多大的关系</div>2019-10-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/29/c6/7fd7efa3.jpg" width="30px"><span>xingoo</span> 👍（0） 💬（0）<div>有一些区别，离线指数据混入是延时获取，存在一定的时间差，比如今天读取昨天的数据；批量处理形容的是处理数据的模式，分差成多个子任务，同时处理；实时形容的是读取数据尽量贴近业务时间；流式计算描述的也是一种计算方式，每个子任务并行或穿行，行成数据的</div>2019-10-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/44/a7/171c1e86.jpg" width="30px"><span>啦啦啦</span> 👍（0） 💬（0）<div>打卡</div>2019-10-28</li><br/>
</ul>