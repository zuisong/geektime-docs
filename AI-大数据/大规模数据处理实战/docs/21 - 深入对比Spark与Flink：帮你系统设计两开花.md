你好，我是蔡元楠。

今天我要与你分享的主题是“深入对比Spark与Flink”。

相信通过这一模块前9讲的学习，你对Spark已经有了基本的认识。现在，我们先来回顾整个模块，理清一下思路。

首先，从MapReduce框架存在的问题入手，我们知道了Spark的主要优点，比如用内存运算来提高性能；提供很多High-level API；开发者无需用map和reduce两个操作实现复杂逻辑；支持流处理等等。

接下来，我们学习了Spark的数据抽象——RDD。RDD是整个Spark的核心概念，所有的新API在底层都是基于RDD实现的。但是RDD是否就是完美无缺的呢？显然不是，它还是很底层，不方便开发者使用，而且用RDD API写的应用程序需要大量的人工调优来提高性能。

Spark SQL提供的DataFrame/DataSet API就解决了这个问题，它提供类似SQL的查询接口，把数据看成关系型数据库的表，提升了熟悉关系型数据库的开发者的工作效率。这部分内容都是专注于数据的批处理，那么我们很自然地就过渡到下一个问题：Spark是怎样支持流处理的呢？

那就讲到了Spark Streaming和新的Structured Streaming，这是Spark的流处理组件，其中Structured Streaming也可以使用DataSet/DataFrame API，这就实现了Spark批流处理的统一。
<div><strong>精选留言（8）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/10/37/d0/26975fba.jpg" width="30px"><span>西南偏北</span> 👍（27） 💬（2）<div>老师能详细解释一下这句话吗？
“由于相同的原因，Spark 只支持基于时间的窗口操作（处理时间或者事件时间），而 Flink 支持的窗口操作则非常灵活，不仅支持时间窗口，还支持基于数据本身的窗口，开发者可以自由定义想要的窗口操作。”</div>2019-06-05</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/4c/6d/c20f2d5a.jpg" width="30px"><span>LJK</span> 👍（8） 💬（1）<div>老师好，请问大多数机器学习算法是有环数据这是啥意思啊？是说每个优化迭代之间是环的么？</div>2019-08-16</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/48/f3/65c7e3ef.jpg" width="30px"><span>cricket1981</span> 👍（15） 💬（1）<div>spark根据算子依赖类型将计算过程划分成多个stage，只有上一个stage全部完成才能进入下一个stage，而flink无此限制。</div>2019-06-05</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/b6/2e/096790e1.jpg" width="30px"><span>淹死的大虾</span> 👍（4） 💬（0）<div>Spark多数据源的join实时处理不如Flink；Spark处理多数据源时，如果有数据源时间间隔超过watermark就没法inner-join了</div>2019-06-26</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/DYAIOgq83eqDDqOsV3gmETQPicqR4hIeOTzEI8DPV1xIXygQgRXxOHnSTibicMMGT9zGMst5QWDiaicUGx1X2NlMWyg/132" width="30px"><span>Geek_88b596</span> 👍（2） 💬（0）<div>我们知道flink的特点是支持在计算流做到exactly once，想问下老师spark支持这样特性吗？不支持的话是不是代表特殊场景下的结果是不准确的也就是说不确定的</div>2019-06-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/f2/ff/2a27214e.jpg" width="30px"><span>se7en</span> 👍（2） 💬（0）<div>Flink有环数据流和用流思想做到批的思想，这两个地方我没懂，老师，你能详细说说么</div>2019-06-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/4c/1b/b1953a5e.jpg" width="30px"><span>江中芦苇</span> 👍（1） 💬（0）<div>本文例子加了时间窗口，不是对一段时间的数据进行计算吗？应该算批处理的例子吧</div>2019-07-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/29/d8/f8/a775cde7.jpg" width="30px"><span>太阳与冰</span> 👍（0） 💬（0）<div>老师，能解释一下从最底层算子的粒度，两边算子的差异么？以及为什么spark的算子只能处理微批，而Flink的算子能够处理基于事件的一条条数据呢？</div>2022-03-16</li><br/>
</ul>