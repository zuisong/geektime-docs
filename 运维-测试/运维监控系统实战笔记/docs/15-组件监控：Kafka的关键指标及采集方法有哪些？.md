你好，我是秦晓辉。

前面两讲我们介绍了 MySQL 和 Redis 的监控，核心原理就是连到实例上执行特定语句命令拉取数据，类似的还有 MongoDB，这算是一类监控场景。这一讲我们介绍现代分布式系统中非常常用的组件——Kafka，同时引出 JMX 监控场景，丰富你的数据采集工具箱。

要做好 Kafka 的监控，首先要了解 Kafka 的[基础概念](https://time.geekbang.org/column/article/99318)，比如 Topic（主题）、Partition（分区）、Replica（副本）、AR（Assigned Replicas）、ISR（In-Sync Replicas）、OSR（Out-of-Sync Replicas）、HW（High Watermark）、LEO（Log End Offset）等等。其次是要了解 Kafka 的架构，通过架构才能知道要重点监控哪些组件，下面我们就先来看一下 Kafka 的架构图。

## Kafka 架构

![](https://static001.geekbang.org/resource/image/d6/84/d691yye35395bb878227c002dfcc7a84.png?wh=2306x1303 "图片来自网络")

上面绿色部分 PRODUCER（生产者）和下面紫色部分 CONSUMER（消费者）是业务程序，通常由研发人员埋点解决监控问题，如果是 Java 客户端也会暴露 JMX 指标。组件运维监控层面着重关注蓝色部分的 BROKER（Kafka 节点）和红色部分的 ZOOKEEPER。

ZooKeeper 也是 Java 语言写的，监控相对简单，可以复用下面介绍的 JMX 监控方式，另外 ZooKeeper 支持 mntr 四字命令，可以获取 ZooKeeper 内部健康状况。新版 ZooKeeper 连四字命令都不需要了，直接内置暴露了 Prometheus 协议的 metrics 接口，直接抓取即可。
<div><strong>精选留言（5）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/0f/46/76/67e111da.jpg" width="30px"><span>巴辉特</span> 👍（0） 💬（0）<div>关于 jmx_exporter 的描述有误，特做勘误，具体测试过程如下：https:&#47;&#47;mp.weixin.qq.com&#47;s&#47;_RLYGuGdz-gvuqZfg1_rFg 供各位小伙伴参考</div>2023-02-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/25/87/f3a69d1b.jpg" width="30px"><span>peter</span> 👍（1） 💬（1）<div>请教老师几个问题：
Q1：流程理解是否对？
A categraf部署在kafka上，采集指标数据，然后发送给jolokia，jolokia将数据转换为HTTP协议后发送到监控系统。B categraf和jolokia都位于kafka端，监控系统类似于server端。 这样理解对吗？
Q2：怎么知道消费流量？
BytesOutPerSec除了包含普通消费者的消费流量，也包含了副本同步流量，那么怎么知道普通消费者的消费流量？
Q3：关键指标的仪表盘是Prometheus的吗？</div>2023-02-10</li><br/><li><img src="" width="30px"><span>Geek_f31e99</span> 👍（0） 💬（1）<div>请问老师！ kafka_consumer_lag_millis这个报警值，设置多大比较合适！</div>2023-02-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/32/4b/20/8a289101.jpg" width="30px"><span>冷如冰</span> 👍（0） 💬（1）<div>为什么全是语音。。。没视频？</div>2023-02-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/7c/25/19cbcd56.jpg" width="30px"><span>StackOverflow</span> 👍（0） 💬（0）<div>如果是k8s集群部署的 kafka，是不是使能 metrics，然后监控相应指标？</div>2023-02-16</li><br/>
</ul>