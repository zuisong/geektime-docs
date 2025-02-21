你好，我是文强。

上节课讲完了RocketMQ，这节课我们再来看一下流消息领域的消息队列Kafka。

因为我们之前在[第16讲](https://time.geekbang.org/column/article/680879)已经详细描述了，基于ZooKeeper和KRaft来构建集群的两种方式，在这里就不再重复。这节课我们会详细分析 Kafka 副本之间的数据一致性、数据同步机制、Leader 切换、数据截断。

## 数据可靠性

我们知道，Kafka 集群维度的数据可靠性也是通过副本来实现的，而副本间数据一致性是通过Kafka ISR 协议来保证的。ISR 协议是现有一致性协议的变种，它是参考业界主流的一致性协议，设计出来的符合流消息场景的一致性协议。

**ISR协议的核心思想是：**通过副本拉取Leader数据、动态维护可用副本集合、控制Leader切换和数据截断3个方面，来提高性能和可用性。

![](https://static001.geekbang.org/resource/image/7e/ed/7e4cf5f54694b1624f91b31f2a2c7ced.jpg?wh=10666x6000)

参考图示，这是一个包含1个Leader、2个Follower的分区。如果是基于Raft协议或者多数原则实现的一致性算法，那么当Leader接收到数据后，就会直接分发给部分或全部副本。我们在前面两节课说到的 RabbitMQ的镜像队列、仲裁队列和 RocketMQ 的 Master/Slave、Dledger 都是这么实现的。

这种机制在流消息队列的大吞吐场景中主要有两个缺点：
<div><strong>精选留言（1）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/1a/f3/8d/402e0e0f.jpg" width="30px"><span>林龍</span> 👍（0） 💬（0）<div>当配置最终一致（ACK=1），Leader 接收到数据成功写入应该就会告诉客户端写入成功把？

这里是不是想表达的是LEO的概念.

强一致性是需要所有follewer都收到了这个LEO写入时高水位+1，才返回
最终一致性是只要把这个LEO信息同步到follewer，不等待同步成功就返回。</div>2023-08-17</li><br/>
</ul>