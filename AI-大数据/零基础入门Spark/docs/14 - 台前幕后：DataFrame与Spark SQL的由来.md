你好，我是吴磊。

在上一讲，结合“小汽车倍率分析”的例子，我们学习了在Spark SQL子框架下做应用开发的一般模式。我们先是使用SparkSession的read API来创建DataFrame，然后，以DataFrame为入口，通过调用各式各样的算子来完成不同DataFrame之间的转换，从而进行数据分析。

尽管我们说过，你可以把DataFrame看作是一种特殊的RDD，但你可能仍然困惑DataFrame到底跟RDD有什么本质区别。Spark已经有了RDD这个开发入口，为什么还要重复造轮子，整出个DataFrame来呢？

相信学完了上一讲，这些问题一定萦绕在你的脑海里，挥之不去。别着急，今天我们就来高屋建瓴地梳理一下DataFrame的来龙去脉，然后再追本溯源，看看帮助DataFrame崭露头角的幕后大佬Spark SQL又是怎么回事儿。

## RDD之殇：优化空间受限

在RDD算子那一讲（[第3讲](https://time.geekbang.org/column/article/418079)），我们曾经留过一道思考题，像map、mapPartitions、filter、flatMap这些算子，它们之间都有哪些共性？

今天，我们从一个全新的视角，来重新审视这个问题。先说结论，它们都是高阶函数（Higher-order Functions）。
<div><strong>精选留言（5）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/12/07/8a/4bef6202.jpg" width="30px"><span>大叮当</span> 👍（15） 💬（1）<div>老师您好，请教您两个问题：
1、除了dataframe，还有个dataset，那dataframe和dataset两种格式，在执行的时候有没有效率、性能这方面差异呢？您更推荐哪种呢
2、Dataset&lt;Row&gt;和Dataset&lt;具体类型&gt;比如Dataset&lt;Person&gt;，这两种是不是性能上也有差异呢？
谢谢</div>2021-10-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/41/76/d5cfd0f7.jpg" width="30px"><span>米哈游牛浚亲</span> 👍（3） 💬（1）<div>想请问下，DataFrame API 最终是都会转化成codegen的生成代码吗？还是可选生成RDD或codegen呢</div>2021-10-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/2a/39/68/56dfc8c0.jpg" width="30px"><span>子兮</span> 👍（1） 💬（1）<div>老师， spark graphX 也是会把一个stage 的算子合成一个函数执行，但是grapX 是没有用到Tungsten的，所以这种优化方式不应该是spark core 在做的吗？</div>2021-11-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/0c/9e/56767592.jpg" width="30px"><span>legend</span> 👍（2） 💬（1）<div>下面这段话中不再是透明的是不是说反了？应该是“不再是不透明的”吧？

这些计算逻辑对 Spark 来说，不再是透明的，因此，Spark 可以基于启发式的规则或策略，甚至是动态的运行时信息，去优化 DataFrame 的计算过程。</div>2023-03-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/29/3f/0f/5fdf1241.jpg" width="30px"><span>Nicky</span> 👍（0） 💬（0）<div>请问RDD比Dataframe有什么样的优势吗？课程中有提到RDD 算子多采用高阶函数，表达能力强，能灵活地设计并实现业务逻辑。老师可以详细讲一下RDD的价值吗？</div>2022-12-18</li><br/>
</ul>