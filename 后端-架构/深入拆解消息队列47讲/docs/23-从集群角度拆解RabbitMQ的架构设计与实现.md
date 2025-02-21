你好，我是文强。

到了这节课，我们就讲完了进阶篇所有的知识点了。在进阶篇，我们首先分析了消息队列集群中哪些地方可能存在性能瓶颈和可靠性风险，然后依次讲解了集群构建、数据一致性、数据安全、集群可观测性四大模块的设计和选型思路。同时也分享了一些Java在开发存储系统过程中的编码技巧。

接下来，我们围绕着进阶篇的内容，用四节课分别讲一下消息方向的RabbitMQ 、RocketMQ 以及流方向的Kafka、Pulsar 在这几个方面的实现。另外，你也可以先复习下第10～13讲，有助于你更好、更完整地理解内容。

那么这节课我们就先来讲一下RabbitMQ，从集群构建的设计思路开始。

## 集群构建

我们前面讲过，集群构建由**节点发现**和**元数据存储**两部分组成。RabbitMQ 也是一样的实现思路。

在节点发现方面，RabbitMQ 通过插件化的方式支持了多种发现方式，用来满足不同场景下的集群构建需求。如下图所示，主要分为**固定配置发现**、**类广播机制发现**、**第三方组件发现**、**手动管理**等4种类型，以及固定配置、DNS、AWS（EC2）、Kubernetes、Consule、etcd、手动管理等7种发现方式。

![](https://static001.geekbang.org/resource/image/78/da/78ceyy4c08aaf07bea5494ebcb42afda.jpg?wh=10666x6000)

- **固定配置发现：**是指通过在RabbitMQ的配置文件中配置集群中所有节点的信息，从而发现集群所有节点的方式。和ZooKeeper的节点发现机制是一个思路。
- **类广播机制发现：**是指通过DNS本身的机制解析出所有可用IP列表，从而发现集群中的所有节点。和 Elasticsearch 通过多播来动态发现集群节点是类似的思路。
- **第三方组件发现：**是指通过多种第三方组件发现集群中的所有节点信息，比如 AWS（EC2）、Kubernetes、Consul、etcd 等。和Kafka、Pulsar依赖ZooKeeper，RocketMQ依赖NameServer是一个思路。
- **手动管理：**是RabbitMQ比较特殊的实现方式，是指通过命令 rabbitmqctlctl 工具往集群中手动添加或移除节点。即依赖人工来管理集群，这种方式使用起来不太方便，其他消息队列很少采用这个方案。
<div><strong>精选留言（1）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/15/ac/23/8eb08fdf.jpg" width="30px"><span>小手冰凉*^O^*</span> 👍（0） 💬（0）<div>RabbitMQ 没有 Topic，只有 Queue 的概念?这个怎么理解呢。RabbitMQ不是有六种工作模式，其中一种不就是Topic模式吗？</div>2024-05-20</li><br/>
</ul>