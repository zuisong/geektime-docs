你好，我是吴磊。

在上一讲，我们从原理的角度出发，学习了Structured Streaming的计算模型与容错机制。深入理解这些基本原理，会帮我们开发流处理应用打下坚实的基础。

在“流动的Word Count”[那一讲](https://time.geekbang.org/column/article/446691)，我们演示了在Structured Streaming框架下，如何做流处理开发的一般流程。基于readStream API与writeStream API，我们可以像读写DataFrame那样，轻松地从Source获取数据流，并把处理过的数据写入Sink。

今天这一讲，咱们从功能的视角出发，继续来聊一聊Structured Streaming流处理引擎都为开发者都提供了哪些特性与能力，让你更灵活地设计并实现流处理应用。

## Structured Streaming怎样坐享其成？

学习过计算模型之后，我们知道，不管是Batch mode的多个Micro-batch、多个作业的执行方式，还是Continuous mode下的一个Long running job，这些作业的执行计划，最终都会交付给Spark SQL与Spark Core付诸优化与执行。

![图片](https://static001.geekbang.org/resource/image/96/74/963a1639328ae80997bf3f1ce90c9b74.jpg?wh=1920x526 "两种计算模型的执行方式")

而这，会带来两个方面的收益。一方面，凡是Spark SQL支持的开发能力，不论是丰富的DataFrame算子，还是灵活的SQL查询，Structured Streaming引擎都可以拿来即用。基于之前学过的内容，我们可以像处理普通的DataFrame那样，对基于流数据构建的DataFrame做各式各样的转换与聚合。
<div><strong>精选留言（4）</strong></div><ul>
<li><img src="" width="30px"><span>姚礼垚</span> 👍（4） 💬（2）<div>老师，我想问下Sliding Window的应用场景是啥，如果按照时间聚合的话，Tumbling Window界限好像更清晰一些</div>2022-01-06</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTJNAiaXKMKRVRvE0QwSS2icHmhKLCkhLHnwYxnBPR0WdOm6JNJFb0QolzC91YrZD6aib3o0zVXa2ibjdQ/132" width="30px"><span>Geek_63fe1e</span> 👍（1） 💬（5）<div>怎么觉得消息8也被丢弃，最大的watermark 是9：44，能容忍的最晚的消息不应该是9：34，而消息8已经早于这个时间了</div>2022-02-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1f/36/42/70d01532.jpg" width="30px"><span>苏文进</span> 👍（8） 💬（0）<div>   event time                                               水印        水位线       上沿      下沿
2021-10-01 09:30:00, Apache Spark           09:30:00    09:20:00  09:25:00    09:20:00  ok
2021-10-01 09:36:00, Structured Streaming   09:36:00    09:26:00  09:30:00    09:25:00  ok
2021-10-01 09:39:00, Spark Streaming        09:39:00    09:29:00  09:30:00    09:25:00  ok
2021-10-01 09:41:00, AMP Lab                09:41:00    09:31:00  09:35:00    09:30:00  ok
2021-10-01 09:44:00, Spark SQL              09:44:00    09:34:00  09:35:00    09:30:00  ok
2021-10-01 09:29:00, Test Test              09:44:00    09:34:00  09:35:00    09:30:00  no
2021-10-01 09:33:00, Spark is cool          09:44:00    09:33:00  09:35:00    09:30:00  ok</div>2022-05-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/24/57/c8/dd26d0de.jpg" width="30px"><span>PCZ</span> 👍（0） 💬（1）<div>为什么 scala下的spark element_at这个函数找不到，需要什么依赖吗</div>2023-04-16</li><br/>
</ul>