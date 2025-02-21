你好，我是徐文浩。

在 [Storm的论文](https://time.geekbang.org/column/article/462384)里，我们看到Storm巧妙地利用了异或操作，能够追踪消息是否在整个Topology中被处理完了，做到了“至少一次（At Least Once）”的消息处理机制。然后，在 [Kafka的论文](https://time.geekbang.org/column/article/465972)里，我们又看到了，Kafka通过将消息处理进度的偏移量记录在ZooKeeper中的方法，使得整个消息队列非常容易重放。Kafka的消息重放机制和Storm组合，就使得At Least Once的消息处理机制不再是纸上谈兵。

然而，我们并不会满足于“至少一次”的消息处理机制，而是希望能够做到“**正好一次（Exactly Once）**”的消息处理机制。因为只有“正好一次”的消息处理机制，才能使得我们计算出来的数据结果是真正正确的。而一旦需要真的实现“正好一次”的消息处理机制，系统的“**容错能力**”就会变得非常重要。Storm的容错能力虽然比起S4已经有了一定的进步，但是实际上仍然非常薄弱。

所有的这些问题，伴随着Kappa架构设想的出现，为我们带来了新一代的流式数据处理系统。那么，接下来的几节课里，让我们步入现代流式数据处理系统，一起看看从Google的MillWheel、Dataflow，到开源的Apache Flink的系统是怎么回事儿。
<div><strong>精选留言（5）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/15/66/8f/02be926d.jpg" width="30px"><span>在路上</span> 👍（20） 💬（0）<div>读完streaming 101和streaming 102，我得说这两篇比专栏文章长多了，streaming 101啃完英文版，后来发现知乎上有翻译版，幸福的读完了streaming 102的中文版。这两篇文章很重要，它解释了流式数据处理系统能干嘛？能做和批处理系统一样多的事，甚至超过批处理系统的能力。尤其是第二篇，非常值得一读。它探索了四个问题：
1.【What】流式数据处理系统计算出什么结果？结果由pipeline的转换器决定。转换器好比MapReduce中的Mapper、Reducer函数，Spark中的transform算子。
2.【where】流式数据的结果在哪里计算？流式数据由事件构成，根据事件时间，流式数据可以切分成一个个窗口，把无界数据变成有界数据，计算在窗口中完成。
3.【when】计算结果何时输出？水位线或触发器触发输出。水位线表示属于某个窗口时间范围的事件全部到达，如果需要在水位线之前输出结果，或者水位线之后，还有迟到的事件需要计算，需要触发器的帮助。
4.【How】如果修正计算结果？一个窗口的结果会被计算多次。每次计算结果可以独立地发送到下游，也可以更新之前计算的结果，还可以把之前的结果丢弃，再发送新的结果。</div>2021-12-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/66/8f/02be926d.jpg" width="30px"><span>在路上</span> 👍（5） 💬（0）<div>徐老师好，Wikipedia Bloom filter在Probability of false positives一节，给出了漏算日志率的经典估算公式，p=(1 - (1 - 1&#47;m)^kn)^k，其中n为布隆过滤器要处理的日志条数，m为布隆过滤器的bit位数，k为日志映射到布隆过滤器的hash函数个数。
论文《ON THE FALSE-POSITIVE RATE OF BLOOM FILTERS》(2008年)讨论了经典公式在什么情况下有效，m的值要足够大，同时k的值要足够小。论文《A New Analysis of the False-Positive Rate of a Bloom Filter》(2010年)给出了新的估算公式，并讨论了m，以及m&#47;n在不同取值的情况下，经典公式的相对误差。选择合适的n、m、k，才能降低布隆过滤器的假正率。
</div>2021-12-16</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/8f/cf/890f82d6.jpg" width="30px"><span>那时刻</span> 👍（2） 💬（0）<div>估算一下 BloomFilter 可能会导致我们漏掉计算多少日志吗。我觉得需要日志总数据 以及 BloomFilter的 false positive的概率。而计算false positive概率需要 BloomFilter 中bit的总数，储存元素的个数，hash函数的个数</div>2021-12-15</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/b8/b5/52bc6223.jpg" width="30px"><span>shijiezhiai</span> 👍（0） 💬（0）<div>其实挺好奇论文里提到的unique ID是使用什么算法生成的。因为一个computation可能会被调度到其它的节点上运行。在这个前提下，怎么保证同一条数据生成的ID是相同的呢？</div>2023-02-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/fa/c3/7246eb05.jpg" width="30px"><span>小明</span> 👍（0） 💬（0）<div>我仿佛看到了 我在360三年的时光走马灯</div>2021-12-15</li><br/>
</ul>