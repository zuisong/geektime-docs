你好，我是文强。

上节课我们分析了 Kafka 在协议、网络、存储、生产者、消费者这五个模块的设计实现。这节课我们用同样的思路来分析一下 Pulsar。

近几年，作为消息队列后起之秀的Pulsar，因为其存算分离、多租户、多协议、丰富的产品特性、支持百万Topic等特点，逐渐为大家所熟知。从定位来看，Pulsar 希望同时满足消息和流的场景。从技术上来看，它当前主要对标的是Kafka，解决 Kafka 在流场景中的一些技术缺陷，比如计算层弹性、超大分区支持等等。

接下来我们就围绕着基础篇的知识点来拆解一下 Pulsar。

## Pulsar 系统架构

我们先来看一下Pulsar的架构图。

![](https://static001.geekbang.org/resource/image/90/71/904fd20b6ced9af51ae9c25e1c196171.jpg?wh=10666x6000)

如上图所示，Pulsar的架构就复杂很多了，它和其他消息队列最大的区别在于 Pulsar 是基于计算存储分离的思想设计的架构，所以 Pulsar 整体架构要分为计算层和存储层两层。我们通常说的 Pulsar 是指计算层的 Broker 集群和存储层的 BookKeeper 集群两部分。

计算层包含 Producer、Broker、ZooKeeper、Consumer 四个组件，用来完成MQ相关的功能。存储层是独立的一个组件BookKeeper，是一个专门用来存储日志数据的开源项目，它由Bookies（Node）和ZooKeeper组成。
<div><strong>精选留言（4）</strong></div><ul>
<li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTJIocn8OMjfSGqyeSJEV3ID2rquLR0S6xo0ibdNYQgzicib6L6VlqWjhgxOqD2iaicX1KhbWXWCsmBTskA/132" width="30px"><span>虚竹</span> 👍（1） 💬（3）<div>老师好，作为新一代的mq，为何pulsar会在明知zk会成为瓶颈的情况下，依然选择zk呢？另外，pulsar的明显优势是哪些呢？</div>2023-10-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/0a/a4/828a431f.jpg" width="30px"><span>张申傲</span> 👍（1） 💬（2）<div>请教下强哥：像Pulsar这类存算分离架构，存储性能不会存在瓶颈吗？像RocketMQ、Kafka消息都是存本地文件，最多就是一次磁盘IO，而Pulsar要存远程BookKeeper，相当于是网络IO+磁盘IO，虽然会有PageCache、WAL顺序写等优化机制，但是理论上性能还是不如本地存储吧？
还是说存算分离架构就是要牺牲存储性能来换取架构的弹性？</div>2023-07-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/17/5f/73/a9346146.jpg" width="30px"><span>陈</span> 👍（0） 💬（1）<div>Pulsar底层也是一个分区数据一个文件存放的，为什么能支持百万topic？不会产生随机IO带来的性能影响吗？</div>2023-07-31</li><br/><li><img src="" width="30px"><span>Geek_ec80d2</span> 👍（0） 💬（0）<div>&quot;，TTL 仅用于 ACK 掉在 TTL 范围内应被 ACK 的消息，不执行删除操作。真正删除的操作是依靠 Retention 策略来执行的&quot;  这个帮忙代码上确定一下，看日志，5分钟周期ack消息后，马上把满足条件的ledger删除，而不是走retention的删除周期，多谢。</div>2023-07-20</li><br/>
</ul>