你好，我是徐文浩。

过去的两节课里，我给你介绍了S4和Storm这两个流式计算框架相关的论文。不过，在讲解这两篇论文的时候，我们其实没有去搞清楚对应的流式数据是从哪里来的。虽然S4里有Keyless PE，Storm里也有Spout，它们都是框架自己提供的发送流式数据的机制，这些框架本身并不能产生数据。我们各种应用服务器产生的数据，必须要想一个办法，能够给这些流式数据处理系统。

其实，不只是流式数据处理系统有这个需求，我们之前讲解过的GFS/MapReduce这些分布式文件系统，以及大数据批处理系统，一样面临这个“**数据从哪里来**”的问题。

这个问题，也就是我们今天要探讨的主题，就是我们应该通过一个什么样的系统，来传输数据。这个系统需要满足哪些需求，整个系统架构应该怎么设计。而对于这个问题的解答，就是开源的Kafka系统。

同样在2011年，来自LinkedIn的三位工程师，一起发表了《Kafka: a Distributed Messaging System for Log Processing》这样一篇论文，并且把论文里描述的这个系统Kafka开源。这篇论文，可以说帮我们圆上了整个大数据系统的最后一个环节，就是**高性能、高可用的数据传输**。
<div><strong>精选留言（5）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/15/66/8f/02be926d.jpg" width="30px"><span>在路上</span> 👍（15） 💬（1）<div>《Realtime Data Processing at Facebook》这篇论文帮助我建立了对流式处理系统的认识。业务系统允许秒级延迟，而不是毫秒级延迟，使得系统之间可以通过Kafka连接。使用Kafka传输数据带来了额外的好处：
1. 容错：流式处理节点的故障变得独立。
2. 容错：恢复故障变得更快，只需要在其他地方启动一个相同的节点。
3. 容错：自动化的多路复用允许下游运行相同功能的节点，处理相同的输入。
4. 性能：运行上游和下游以不同的速度处理消息，不像背压的一样使得下游会影响上游的执行。
5. 易用：debug更容易，只要启动一个新节点重新消费一遍数据，就能复现错误。
6. 易用：监控和告警变得简单，只要监控流式处理系统的消费Lag。
7. 易用：可以更灵活的编写流式处理系统，因为它们已经通过消息系统解耦了。</div>2021-12-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/66/8f/02be926d.jpg" width="30px"><span>在路上</span> 👍（14） 💬（2）<div>徐老师好，读完2011年的Kakfa论文，我惊讶的发现那时候的分区数据居然没有副本，充分体现了Kafka对业务需求的假设，可以容忍丢失部分日志。Kafka在未来工作中提到，第一、会增加同步和异步的副本模式，并由用户根据业务场景来选择需要的副本模式，第二、会增加流式处理的能力。从最新的Kafka版本来看，Kafka已经实现了这个目标，其中灵活的副本模式就是ISR机制。

Kafka怎么做到高可用呢？第一、Kafka由多个broker构成，通过zookeeper完成分布式协调，当broker宕机时，它负责的主题和分区会分配给其他broker；第二、一个消费者组由多个消费者构成，消费者失联时，它负责的主题和分区会分配给组内其他消费者。第三、一个主题有多个分区，每个分区有多个副本，可以通过ISR机制配置需要多少个同步副本，Leader副本失效时，会从其他副本中选举Leader。第四、消费者位移通过主题来保存，主题的高可用保证了消费者位移的高可用。</div>2021-12-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/fb/7b/2d4b38fb.jpg" width="30px"><span>Jialin</span> 👍（2） 💬（0）<div>备份机制：同一个 partition 存在多个数据副本：leader &amp; follower
ISR 机制：在指定容错时间内，与 leader 保持数据同步的副本机制
ACK 机制：生产者发送消息后，消费者收到消息后的确认机制
故障恢复机制：leader 选举及失败恢复
</div>2021-12-06</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/19/aa/ff/e2c331e0.jpg" width="30px"><span>bbbi</span> 👍（0） 💬（0）<div>老师你好，小文件上传到HDFS 上占用的物理空间应该是文件实际大小吧？不是block size 64M</div>2023-05-30</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/19/76/7c/e1d9a256.jpg" width="30px"><span>Psyduck</span> 👍（0） 💬（0）<div>干货满满</div>2022-07-10</li><br/>
</ul>