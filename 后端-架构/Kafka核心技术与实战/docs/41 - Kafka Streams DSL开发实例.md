你好，我是胡夕。今天我要和你分享的主题是：Kafka Streams DSL开发实例。

DSL，也就是Domain Specific Language，意思是领域特定语言。它提供了一组便捷的API帮助我们实现流式数据处理逻辑。今天，我就来分享一些Kafka Streams中的DSL开发方法以及具体实例。

## Kafka Streams背景介绍

在上一讲中，我们提到流处理平台是专门处理无限数据集的引擎。就Kafka Streams而言，它仅仅是一个客户端库。所谓的Kafka Streams应用，就是调用了Streams API的普通Java应用程序。只不过在Kafka Streams中，流处理逻辑是用**拓扑**来表征的。

一个拓扑结构本质上是一个有向无环图（DAG），它由多个处理节点（Node）和连接节点的多条边组成，如下图所示：

![](https://static001.geekbang.org/resource/image/da/22/da3db610f959e0952a76d6b06d249c22.jpg?wh=1334%2A1674)

图中的节点也称为处理单元或Processor，它封装了具体的事件处理逻辑。Processor在其他流处理平台也被称为操作算子。常见的操作算子包括转换（map）、过滤（filter）、连接（join）和聚合（aggregation）等。后面我会详细介绍几种常见的操作算子。

大体上，Kafka Streams开放了两大类API供你定义Processor逻辑。
<div><strong>精选留言（10）</strong></div><ul>
<li><img src="" width="30px"><span>leige</span> 👍（5） 💬（1）<div>stream和table都会有对应的topic吧，老师？他们的本质区别是什么？</div>2019-12-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/4d/49/28e73b9c.jpg" width="30px"><span>明翼</span> 👍（4） 💬（1）<div>单词计数里面的groupBy算子里面的key和value不太明白，不太明确那，为什么最后还要count计数</div>2019-09-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/23/ed/a4a774a8.jpg" width="30px"><span>What for</span> 👍（2） 💬（1）<div>有几个疑惑详情老师赐教：
1、demo 是一个可以单机跑的 Java 进程，运行时会有几个线程工作？
2、如果输入 topic 有 3 个分区，在计算过程中 consumer 会在 3 个不同的线程里分别起 1 个消费 1 个分区还是说有其他的配置项可以调整？
3、遇到 shuffle 时下游的计算计算分区还是就统一汇总计算？如果 shuffle 下游有分区怎么确定分区策略以及写入输出 topic 的时候会有几个 producer？</div>2020-02-04</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/4d/5e/c5c62933.jpg" width="30px"><span>lmtoo</span> 👍（2） 💬（2）<div>第一个例子没有时间窗口的情况下，统计的是什么？最终单词的计数，还是某个时间段的计数</div>2019-09-07</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/52/bb/225e70a6.jpg" width="30px"><span>hunterlodge</span> 👍（1） 💬（1）<div>老师，我们领导提出了这样一些需求：1. 可以根据消息中的字段查询消息内容，这样可以用来诊断消息确实写入了kafka；2. 可以对某些消息重放；3. 可以对某些消息打标记从而控制消息的消费。我调研了一圈，第一点貌似可以用confluent的ksql做到，但是需要引入ksql server等复杂性，第二点也可以基于ksql来复制消息到重放队列（这样每一个topic都会存在一个重放topic）。第三点暂时还没有很好的思路。求助老师更好的方案，谢谢！</div>2019-11-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/52/bb/225e70a6.jpg" width="30px"><span>hunterlodge</span> 👍（1） 💬（1）<div>老师，我有几个疑问：
1. 如果客户端应用重启了，KTable及写入的KStream在重启前的状态就都清楚了对吗？如果是的话，重启后，单词计数要重新对队列中的所有数据从头到尾再次计算，对吗？
2. 在没有指定时间窗口的情况下，应用读取队列消息的周期是什么呢？Stream API也是通过poll方式读取队列数据吗？
3. “所以，事件的 Key 也必须要携带时间窗口的信息。”，这里携带时间窗口信息是指什么呢？能举个例子吗？

谢谢！</div>2019-11-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/25/7f/473d5a77.jpg" width="30px"><span>曾轼麟</span> 👍（1） 💬（1）<div>老师有个疑问，如果按照这个事例，我使用kafka普通client的batch方式消费，搭载JAVA8的lambda不是实现更快捷吗？而且我中间还能自己通过代码写入各种数据库或者其它持久化方式？lambda本身也支持map—reduce的方式计算，而且consumer group本身也是一种负载均衡的思路</div>2019-09-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/8d/56/2a04dd88.jpg" width="30px"><span>icejoywoo</span> 👍（1） 💬（2）<div>count之前加上.windowedBy(TimeWindows.of(Duration.ofMinutes(5)))，应该就可以了吧</div>2019-09-07</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/c0/8b/0371baee.jpg" width="30px"><span>张丽娜</span> 👍（0） 💬（1）<div>这个章节，老师讲的东西，我竟然听懂了，感谢老师耐心的讲解啊。</div>2020-03-05</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/58/28/c86340ca.jpg" width="30px"><span>达文西</span> 👍（0） 💬（0）<div>感觉打开了新世界的大门,虽然暂时在业务上用不上</div>2019-11-27</li><br/>
</ul>