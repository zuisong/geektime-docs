你好，我是蔡元楠。

今天我要与你分享的主题是“Beam数据转换操作的抽象方法”。

在上一讲中，我们一起学习了Beam中数据的抽象表达——PCollection。但是仅仅有数据的表达肯定是无法构建一个数据处理框架的。那么今天，我们就来看看Beam中数据处理的最基本单元——Transform。

下图就是单个Transform的图示。

![](https://static001.geekbang.org/resource/image/cc/66/cc1266a6749cdae13426dd9721f66e66.jpg?wh=1430%2A694)

之前我们已经讲过，Beam把数据转换抽象成了有向图。PCollection是有向图中的边，而Transform是有向图里的节点。

不少人在理解PCollection的时候都觉得这不那么符合他们的直觉。许多人都会自然地觉得PCollection才应该是节点，而Transform是边。因为数据给人的感觉是一个实体，应该用一个方框表达；而边是有方向的，更像是一种转换操作。事实上，这种想法很容易让人走入误区。

其实，区分节点和边的关键是看一个Transform是不是会有一个多余的输入和输出。

每个Transform都可能有大于一个的输入PCollection，它也可能输出大于一个的输出PCollection。所以，我们只能把Transform放在节点的位置。因为一个节点可以连接多条边，而同一条边却只能有头和尾两端。
<div><strong>精选留言（11）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/11/5f/e9/95ef44f3.jpg" width="30px"><span>常超</span> 👍（17） 💬（2）<div>1.ParDo支持数据输出到多个PCollection，而Spark和MapReduce的map可以说是单线的。
2.ParDo提供内建的状态存储机制，而Spark和MapReduce没有（Spark Streaming有mapWithState ）。</div>2019-06-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/48/f3/65c7e3ef.jpg" width="30px"><span>cricket1981</span> 👍（2） 💬（1）<div>ParDo能指定并行度吗？</div>2019-06-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/4c/6d/c20f2d5a.jpg" width="30px"><span>LJK</span> 👍（1） 💬（1）<div>ParDo是不是跟map一个意思？</div>2019-08-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/e3/72/afd1eef0.jpg" width="30px"><span>柳年思水</span> 👍（0） 💬（1）<div>ParDo 有点自定义 UDX 的意思，而 Spark 或 Flink 除了支持 UDX，还内置很多常用的算子</div>2019-07-20</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/yYzf0yonEqKny7dHlvLibc7OrQJ6HszX3VP1fciaMD3hITFySbayL9vULch5hvicoqGA2EBzcPicss2ciaB7ibodgQ6w/132" width="30px"><span>sxpujs</span> 👍（9） 💬（0）<div>Spark的算子和函数非常方便和灵活，这种通用的DoFn反而很别扭。</div>2019-06-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/93/57/3ffdfc8d.jpg" width="30px"><span>vigo</span> 👍（8） 💬（0）<div>推荐python,然而这章又几乎全是java事例</div>2019-10-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/53/3d/1189e48a.jpg" width="30px"><span>微思</span> 👍（2） 💬（0）<div>Statefullness、side input&#47;side output相关的例子可以再多一点。</div>2019-06-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1e/ef/1a/34ee87e6.jpg" width="30px"><span>老莫mac</span> 👍（1） 💬（0）<div>刚开始接触并行处理架构，之前看了FLINK，后来公司选型用SPARK，走回学习SPARK的路。看了SPARK 的BEAM，我只有一个感觉，和FLINK的理念何其相像，每个处理步骤或者概念FLINK都有对应的实现。BEAM要在FLINK上面加一层，会损失效率。所以我能想象到的好处只有一个，就是BEAM能同时在FLINK和SPARK上运行，汇聚两边的结果。为了将两种不同的架构当成一种来使用，把处理目标PCOLLECTION 当成流，当成KAFKA往两边分发，两边时独立的消息处理，把结果返回，在某个地方REDUCE 或者SHUFFLE，得到结果。感觉本质上就是这样。</div>2020-06-03</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/19/70/3d/93aa82b6.jpg" width="30px"><span>Junjie.M</span> 👍（1） 💬（0）<div>老师，当一个transform有多个输入pcollection时如何调用transform，是合并pcollection后调用还是各自调用。还有一个transform如何输出多个pcollection。可以给个代码示例吗</div>2020-04-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/be/3e/1de66fbc.jpg" width="30px"><span>阿里斯托芬</span> 👍（0） 💬（0）<div>ParDo应该可以理解为是一个flatmap操作，不过是一个操作更加丰富的flatmap</div>2022-05-17</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/qmdZbyxrRD5qQLKjWkmdp3PCVhwmWTcp0cs04s39pic2RcNw0nNKTDgKqedSQ54bAGWjAVSc9p4vWP8RJRKB6nA/132" width="30px"><span>冯杰</span> 👍（0） 💬（0）<div>感觉ParDo的本意是被设计用来满足这样的场景：数据的处理可以实现并行的操作，即数据集中任意一条数据的处理不依赖于其它的数据，在这种场景下可以满足不同分区数据的并行执行。  与spark相比的话，其实等价于spark中能被分割到单个stage内的操作算子(或者说是不产生shuffle的算子)，总结一下就是ParDo = {map、filter、flatmap...}。    与MR中的map相比的话，功能上类似，但是提供了状态的语义。 不知道理解的对不对，请老师点评。</div>2020-04-11</li><br/>
</ul>