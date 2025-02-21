你好，我是文强。

上节课我们讲完了RabbitMQ，今天继续来看看同样是消息方向的 RocketMQ 在集群构建、部署形态、数据可靠性、安全控制、可观测性等五个方面的设计实现。

## 集群构建

首先，我们还是从元数据存储和节点发现两个方面来分析一下RocketMQ的集群构建。

在前面的课程中，我们知道RocketMQ的元数据是存储在NameServer中。严格意义上来说，这个说法是不对的。**RocketMQ的元数据实际是存储在Broker上，不是直接存储在 NameServer中。**NameServer本身只是一个缓存服务，没有持久化存储的能力，先来看一张图示。

![](https://static001.geekbang.org/resource/image/f1/87/f1488df73a06ac0735e5b927b233df87.jpg?wh=10666x6000)

如上图所示，元数据信息实际存储在每台Broker上，每台Broker 会在本节点维护持久化文件来存储元数据信息。这些元数据信息主要包括节点信息、节点上的Topic、分区信息等等。在Broker启动时，会先连接NameServer注册节点信息，并将保存的元数据上报到所有NameServer节点中。此时所有NameServer节点就有全量的元数据信息了，从而完成了节点之间的发现。

从原理来看，RocketMQ 是基于第三方组件NameServer来完成节点发现的。即通过上报节点信息到一个中央存储，从而发现集群中的其他节点。
<div><strong>精选留言（2）</strong></div><ul>
<li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/LBOHwXq4wliccC1HUPEghTOkWsnVR5zOmSQsias4O6obKJb2tOEpqoiaPE9mGibTlrrnGeMC5m4fp1fY234k4p9PgA/132" width="30px"><span>Geek_4c6cb8</span> 👍（1） 💬（0）<div>有一些疑问请教：
1.Dledger模式是多个独立的Master注册到NameServer，每个Master背后各自一个raft集群吗？
2.Controller模式，文中提到Controller之间选主节点，这是通过选择完整性最高的Controller，在某个Master不可用之后，由Controller选择新的Master吗？</div>2024-01-01</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/28/43/5062a59b.jpg" width="30px"><span>shan</span> 👍（1） 💬（0）<div>RocketMQ的三种部署模式

1. Master&#47;Slave模式
分为Master、Slave两个角色，集群中可以有多个Master节点，一个Master节点可以有多个Slave节点。Master节点负责接收生产者发送的写入请求，将消息写入CommitLog文件，Slave节点会与Master节点建立连接，从Master节点同步消息数据（有同步复制和异步复制两种方式）。
消费者可以从Master节点拉取消息，也可以从Slave节点拉取消息。在RocketMQ 4.5版本之前，如果Master宕机，不支持自动将Slave切换为Master，需要人工介入。

优点
负载过高时，可以快速通过横向添加节点来扩容。

缺点
（1）Master节点宕机之后，不能自动将Slave节点切换为Master节点；
（2）每个节点上都需要创建全量的Topic，存在性能瓶颈；

2. Dledger模式
为了解决主从架构下Slave不能自动切换为Master的问题，4.5版本之后提供了DLedger模式，使用Raft算法，如果Master节点出现故障，可以自动从Slave节点中选举出新的Master进行切换。

存在问题
（1）根据Raft算法的多数原则，集群至少有三个节点以上，在消息写入时，也需要大多数的Follower节点响应成功才能认为消息写入成功；
（2）存在两套HA复制流程（个人认为是主从模式下一套、Dledger模式下一套），Dledger模无法利用RocketMQ原生的存储和复制能力。

3. DLedger Controller模式
RocketMQ 5.0以后推出了DLedger Controller模式，支持独立部署，也可以嵌入在NameServer中，Broker通过与Controller交互完成Master的选举。
在DLedger Controller模式中，数据的一致性可以通过参数inSyncReplicas配置来配置，不用向Dledger模式一样，需要要过半的Follower节点响应才算写入成功。

关于DLedger Controller模式详细信息可以参考
https:&#47;&#47;github.com&#47;apache&#47;rocketmq&#47;blob&#47;develop&#47;docs&#47;cn&#47;controller&#47;design.md</div>2023-09-22</li><br/>
</ul>