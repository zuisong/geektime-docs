你好，我是文强。

上节课我们讲完了 Kafka ，这节课我们再来看一下消息队列领域最新的成员 Pulsar。在开始学习本节课之前，你可以先复习一下[第13讲](https://time.geekbang.org/column/article/676532)，这样的话你对本节内容吸收得会更好。

我们在基础篇讲过，从设计定位上来看，Pulsar 是作为 Kafka 的升级替代品出现的，它主要解决了 Kafka 在集群层面的弹性和规模限制问题。那么现在我们就从集群的角度来拆解一下 Pulsar 的架构设计和实现，先来看一下集群构建。

## 集群构建

在当前版本，Pulsar 集群构建和元数据存储的核心依旧是 ZooKeeper，同时社区也支持了弱ZooKeeper化改造。如下图所示，Pulsar Broker 集群的构建思路和 Kafka 是一致的，都是通过 ZooKeeper 来完成节点发现和集群的元数据管理。

![](https://static001.geekbang.org/resource/image/d4/62/d4090c7722effb453b5c965753736d62.jpg?wh=10666x6000)

从实现角度来看，Broker 启动时会在 ZooKeeper 上的对应目录创建名称为 BrokerIP + Port 的子节点，并在这个子节点上存储Broker相关信息，从而完成节点注册。Pulsar Broker 的节点信息是存储在 ZooKeeper 上的 /loadbalance/brokers 节点上，目录结构如下所示：

```plain
[zk: 9.164.54.17:2181(CONNECTED) 67] ls /loadbalance/brokers
[30.13.4.1:8080, 30.13.8.2:8080, 30.13.4.3:8080]
```
<div><strong>精选留言（1）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/10/d0/91/89123507.jpg" width="30px"><span>Johar</span> 👍（0） 💬（0）<div>为什么在去 ZooKeeper 的路上选择了可插拔的元数据存储框架，而不是去掉第三方存储引擎？
1.优秀分布式存储实现不易，需要技术积累，和成本
2.目前技术日新月异，每个中间件都自己的优点缺点，</div>2023-08-19</li><br/>
</ul>