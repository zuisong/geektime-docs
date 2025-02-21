你好，我是文强。

在基础篇开篇的时候，我们说过最基础的消息队列应该具备**通信协议**、**网络模块**、**存储模块**、**生产者**、**消费者**五个模块。在之前的课程中，我们详细分析了这五个模块的选型、设计和实现思路，接下来我们从消息和流的角度，用四节课的篇幅分别讲一下消息方向的消息队列RabbitMQ、RocketMQ，流方向的消息队列Kafka、Pulsar，在这五个模块的实现思路和设计思想。这节课我们先讲 RabbitMQ。

![](https://static001.geekbang.org/resource/image/9b/f1/9b8b5a5fe12b677377a3497c863373f1.jpg?wh=3228x1488)

## RabbitMQ 系统架构

在正式讲解之前，我们先来看一下RabbitMQ的系统架构。

![](https://static001.geekbang.org/resource/image/f8/8d/f87175e8b0e42c14bf648dfa8f18608d.jpg?wh=10666x5157)

如上图所示，RabbitMQ由Producer、Broker、Consumer三个大模块组成。生产者将数据发送到Broker，Broker 接收到数据后，将数据存储到对应的Queue里面，消费者从不同的Queue消费数据。

那么除了Producer、Broker、Queue、Consumer、ACK 这几个消息队列的基本概念外，它还有 Exchange、Bind、Route 这几个独有的概念。下面我来简单解释下。

Exchange 称为交换器，它是一个逻辑上的概念，用来做分发，本身不存储数据。流程上生产者先将消息发送到Exchange，而不是发送到数据的实际存储单元Queue里面。然后 Exchange 会根据一定的规则将数据分发到实际的Queue里面存储。这个分发过程就是Route（路由），设置路由规则的过程就是Bind（绑定）。即 Exchange 会接收客户端发送过来的 route\_key，然后根据不同的路由规则，将数据发送到不同的Queue里面。
<div><strong>精选留言（7）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/11/1d/de/62bfa83f.jpg" width="30px"><span>aoe</span> 👍（1） 💬（1）<div>老师在文中用「邮局」举例非常好！
才发现「邮局」这个模式应用及其广泛：小到个人网购，大到国之重器「东风快递」
联想到「漂流瓶」可能是「邮局」的前身</div>2023-07-16</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/aa/0c/6a65f487.jpg" width="30px"><span>cykuo</span> 👍（0） 💬（4）<div>channel为何可以降低实际TCP的数量？</div>2023-07-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/56/f4/8ca92aa0.jpg" width="30px"><span>奔腾ing</span> 👍（3） 💬（1）<div>请问老师，针对Mnesia数据损坏的问题，有修复的方法吗？我们项目上经常遇到因服务器断电导致的rmq（目前是3.8.19版本，单机部署）启动不了的情况。目前处理方案都是备份然后删除Mnesia。研究了下rmq官方的文档以及git上issue上问题，没看到明确的修复方案，目前倾向于升级到3.11.20版本，来看看有没有解决此问题。</div>2023-08-11</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/DYAIOgq83ersGSic8ib7OguJv6CJiaXY0s4n9C7Z51sWxTTljklFpq3ZAIWXoFTPV5oLo0GMTkqW5sYJRRnibNqOJQ/132" width="30px"><span>walle斌</span> 👍（0） 💬（0）<div>开发某个消息队列客户端的消费模块，这部分补充一下
1）、是否支持多线程消费，尤其是会牵扯到ack，需要看这个mq的定位问题
2）、开了多线程，那么pull 得拉取 得流速限制，尤其是第一步开了多线程以后可能存在占用较多内存的问题
3）、考虑到异常消费，可以额外指定 过期时间、重复消费次数控制、堆积数据转移等option 功能</div>2024-12-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/24/54/cb/3be06a7d.jpg" width="30px"><span>JooKS</span> 👍（0） 💬（0）<div>客户端跟broker建连后就不会变了吗，如果某个broker的消费者阻塞了或者负载很高，其他broker的消费者负载很低，这种情况下是不是没办法解决这个broker的慢消费问题了。这时候选择扩容收益也比较低。</div>2024-05-30</li><br/><li><img src="" width="30px"><span>TKF</span> 👍（0） 💬（0）<div>老师，既然rabbitmq的数据存储是顺序写到一个文件中的，那发送到queue的意义是不是仅仅构建一下相应的索引？</div>2023-08-16</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/cb/92/cfc1cfd3.jpg" width="30px"><span>贝氏倭狐猴</span> 👍（0） 💬（0）<div>老师，有个问题：“在 AMQP 协议中，是没有定义 Topic 和消费分组的概念的，所以在消费端没有消费分区分配、消费分组 Rebalance 等操作，消费者是直接消费 Queue 数据的。”那消费模式是类似pulsar的shared么？</div>2023-07-12</li><br/>
</ul>