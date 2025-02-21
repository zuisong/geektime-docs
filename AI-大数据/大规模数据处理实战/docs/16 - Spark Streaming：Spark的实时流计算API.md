你好，我是蔡元楠。

今天我要与你分享的内容是“Spark Streaming”。

通过上一讲的内容，我们深入了解了Spark SQL API。通过它，我们可以像查询关系型数据库一样查询Spark的数据，并且对原生数据做相应的转换和动作。

但是，无论是DataFrame API还是DataSet API，都是基于批处理模式对静态数据进行处理的。比如，在每天某个特定的时间对一天的日志进行处理分析。

在第二章中你已经知道了，批处理和流处理是大数据处理最常见的两个场景。那么作为当下最流行的大数据处理平台之一，Spark是否支持流处理呢？

答案是肯定的。

早在2013年，Spark的流处理组件Spark Streaming就发布了。之后经过好几年的迭代与改进，现在的Spark Streaming已经非常成熟，在业界应用十分广泛。

今天就让我们一起揭开Spark Streaming的神秘面纱，让它成为我们手中的利器。

## Spark Streaming的原理

Spark Streaming的原理与微积分的思想很类似。

在大学的微积分课上，你的老师一定说过，微分就是无限细分，积分就是对无限细分的每一段进行求和。它本质上把一个连续的问题转换成了无限个离散的问题。
<div><strong>精选留言（11）</strong></div><ul>
<li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/DYAIOgq83eqTwSGXttkspRF37CTYQvVsibWicKJDtseiaE3DibfsSAHiaFM2Iwb04hg3O0Bq9JfG358A7Tlhia6vAhDw/132" width="30px"><span>Hobbin</span> 👍（32） 💬（6）<div>老师，Spark团队对Spark streaming更新越来越少，Spark streaming存在使用Processing time 而非 Event time，批流代码不统一等问题，而Structured streaming对这些都有一定改进。所以Structure streaming 会替代Spark streaming或者Flink，成为主流的流计算引擎吗？</div>2019-05-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/57/bd/acf40fa0.jpg" width="30px"><span>lwenbin</span> 👍（9） 💬（2）<div>没用过spark streaming, 用storm比较多。
觉得流处理关键在于要在窗口内尽快地把到来的数据处理完，不要造成数据堆积，内存溢出。
其中牵涉到了如何高效地接受数据，如何并行尽快地处理数据。
觉得优化可以从：接受输入，处理算法，处理单元数量，GC调优等方面入手吧。
有个问题，对于RDD如果transform链很长，感觉是否会对性能造成一定影响，特别是流式或者图形计算？老师能否解答一下。
谢谢！</div>2019-05-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/41/27/3ff1a1d6.jpg" width="30px"><span>hua168</span> 👍（17） 💬（2）<div>批处理可以选择spark；流处理：spark stream，storm，Flink；还有现在大统一的beam
请问：这些技术都要学一遍吗？精力放在哪个技术上？
如果我是初学者，我能直接学beam其它都不学吗？</div>2019-05-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/ac/a7/4d41966a.jpg" width="30px"><span>邱从贤※klion26</span> 👍（14） 💬（0）<div>上一条留言没有说完。
spark streaming 需要设置 batch time 是多少，这决定时效性，以及调度的 overhead，另外要看自己需要的吞吐多大，并发是不是有特殊需求。
spark streaming 有几个点不太喜欢，修改业务逻辑后，需要删除 checkpoint 才行，这会导致从头计算；慢节点没法解决，当一个 batch 里面有一个节点很难的时候，整个 batch 都无法完成。
一个反常识的点：实时 etl 同样吞吐下，flink 比 spark streaming 更节省资源。
另外官方已经放弃 spark streaming，转向structured streaming，但是从邮件列表看又没有 commiter 在管，导致 pr 没人 review，或许这和 spark 整体的重心或者方向有关吧</div>2019-05-26</li><br/><li><img src="" width="30px"><span>Fiery</span> 👍（7） 💬（0）<div>既然DStream底层还是RDD，那我认为针对RDD的一些优化策略对DStream也有效。比如平衡RDD分区减少数据倾斜，在tranformation链中优先使用filter&#47;select&#47;first减少数据量，尽量串接窄依赖函数方便实现节点间并行计算和单节点链式计算优化，join时优化分区或使用broadcast减少stage间shuffle。

另外专门针对流数据的处理，个人经验上主要是要根据业务需求微调window length和sliding interval以达到吞吐量和延时之间的一个最优平衡，时间窗口越大，一个RDD可以一次批处理的数据就越多，Spark的优势就可以发挥出来，吞吐量就上去了。而滑动间隔越大，windowed DStream在固定时间内的RDD就越少，系统的任务队列里同时需要处理的计算当然就越少，不过这两个调整都会加大数据更新延迟和牺牲数据实时性，所以说要根据业务真实需求谨慎调整。

不过个人理解RDD里面用来避免重复计算的cache和persist无法用来减少窗口滑动产生的重复计算，因为窗口每滑动一次，都产生一个新的RDD，而persist只针对其中某个RDD进行缓存，在RDD这种low level api里面，应该是无法知道下个窗口中的RDD和现在的RDD到底有多少数据是重叠的。对于这点理解是否正确望老师解答！</div>2020-03-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/17/21/eb/bb2e7a3b.jpg" width="30px"><span>Ming</span> 👍（3） 💬（1）<div>优化的定义很广，不知道在这个领域大家提到这个词主要指的是什么？望解答

不过，对具体实现细节不了解的情况下有几个猜测：
我会改变时间粒度，来减少RDD本身带来的开销，上文的例子里时间粒度如果设置成10秒应该逻辑上也是可行的。
另外，我大概会考虑多使用persist来减少因为窗口滑动产生的重复计算。</div>2019-05-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/f5/b9/888fe350.jpg" width="30px"><span>不记年</span> 👍（1） 💬（0）<div>在满足需求的情况下尽可能的使用更宽的窗口长度，减少rdd的处理链</div>2020-03-30</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/93/b8/6510592e.jpg" width="30px"><span>渡码</span> 👍（1） 💬（0）<div>稳定性：对于7*24小时的流式任务至关重要
低延迟高吞吐量</div>2019-05-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/8b/4b/503eaecc.jpg" width="30px"><span>skybird</span> 👍（0） 💬（0）<div>嗨，有人吗？第三行代码应该是ssc：
lines = ssc.socketTextStream(&quot;localhost&quot;, 9999)
？？</div>2023-05-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/f9/45/eaa8beb0.jpg" width="30px"><span>王翔宇🍼</span> 👍（0） 💬（0）<div>sc和ssc的区别是什么？我理解ssc才是那个streamingContext吧，如果是这样，那么又出现错误了。</div>2019-07-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/ac/a7/4d41966a.jpg" width="30px"><span>邱从贤※klion26</span> 👍（0） 💬（0）<div>spark streaming 批次的大小设置多少合适，从官方宣传来看已经被 structure steeaming 替代。</div>2019-05-26</li><br/>
</ul>