你好，我是徐文浩。

在过去的几讲里，我们看到了大数据的流式处理系统是如何一步一步进化的。从最早出现的S4，到能够做到“至少一次”处理的Storm，最后是能够做到“正好一次”数据处理的MillWheel。你应该能发现，这些流式处理框架，每一个都很相似，它们都采用了有向无环图一样的设计。但是在实现和具体接口上又很不一样，每一个框架都定义了一个属于自己的逻辑。

S4是无中心的架构，一切都是PE；Storm是中心化的架构，定义了发送数据的Spout和处理数据的Bolt；而MillWheel则更加复杂，不仅有Computation、Stream、Key这些有向无环图里的逻辑概念，还引入了Timer、State这些为了持久化状态和处理时钟差异的概念。

和我们在大数据的批处理看到的不同，S4、Storm以及MillWheel其实是某一个数据处理系统，而不是MapReduce这样高度抽象的编程模型。每一个流式数据处理系统各自有各自对于问题的抽象和理解，**很多概念不是从模型角度的“该怎么样”抽象出来，而是从实际框架里具体实现的“是怎么样”的角度，抽象出来的**。

不过，我们也看到了这些系统有很多相似之处，它们都采用了有向无环图模型，也都把同一个Key的数据在逻辑上作为一个单元进行抽象。随着工业界对于流式数据处理系统的不断研发和运用，到了2015年，仍然是Google，发表了今天我们要解读的这一篇《The Dataflow Model》的论文。
<div><strong>精选留言（4）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/28/c0/fe/34a99a93.jpg" width="30px"><span>Gavin</span> 👍（3） 💬（0）<div>window merging 中结果有误(文中位置为：论文中的图5，如何通过AssignWindows和MergeWindows来进行数据计算，数据乱序也不影响计算结果) ，取的是window end, 而非window start，对应Google 论文应该是Figure 4
https:&#47;&#47;storage.googleapis.com&#47;pub-tools-public-publication-data&#47;pdf&#47;43864.pdf</div>2022-01-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/8f/cf/890f82d6.jpg" width="30px"><span>那时刻</span> 👍（2） 💬（1）<div>对于有边界的固定数据，我们当然可以通过重放日志把数据给到 Dataflow 系统， 我之前采用的是global window以及default trigger来处理的</div>2021-12-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/47/00/3202bdf0.jpg" width="30px"><span>piboye</span> 👍（1） 💬（0）<div>sql支持这些功能了吗？</div>2021-12-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/66/8f/02be926d.jpg" width="30px"><span>在路上</span> 👍（0） 💬（0）<div>徐老师好，DataFlow论文第3.2节Design Principles，提到Support robust analysis of data in the context in which they occurred，数据的健壮分析是指什么？</div>2021-12-24</li><br/>
</ul>