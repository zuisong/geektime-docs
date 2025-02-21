你好，我是文强。

上节课我们分析了RabbitMQ在通信协议、网络模块、存储模块、生产者、消费者这五个模块的设计思路。这节课我们用同一个思路来讲讲 RocketMQ。

有一个蛮有意思的现象，从我们的统计数据来看，RabbitMQ的用户数是最多的。但是在程序员的口碑中，RocketMQ无论是从性能还是稳定性上都是优于RabbitMQ的。从我个人来看，RocketMQ 可以当作RabbitMQ的替代品，因为RocketMQ在功能、稳定性、性能层面都比RabbitMQ的表现更好。所以我们一起来看看为什么吧。

## **RocketMQ 系统架构**

在正式讲解之前，我们先来看一下RocketMQ的架构图。

如下图所示，RocketMQ由 **Producer**、**NameServer**、**Broker**、**Consumer** 四大模块组成。其中，NameServer是RocketMQ的元数据存储组件。另外，在RocketMQ 5.0后，还增加了Proxy模块，用来支持gRPC协议，并为后续的计算存储分离架构做准备。

![](https://static001.geekbang.org/resource/image/6a/38/6af4ab5debc9535849ab7da3e5022f38.jpg?wh=10666x4161)

RocketMQ有Topic、MessageQueue、Group的概念，一个Topic可以包含一个或多个MessageQueue，一个Group 可以订阅一个或多个Topic。MessageQueue是具体消息数据的存储单元，订阅的时候通过Group来管理消费订阅关系。
<div><strong>精选留言（10）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/12/0a/a4/828a431f.jpg" width="30px"><span>张申傲</span> 👍（3） 💬（1）<div>小建议：架构图中的Partition是不是换成MessageQueue好一点？虽然概念上是一致的～</div>2023-07-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/17/5f/73/a9346146.jpg" width="30px"><span>陈</span> 👍（1） 💬（1）<div>pop模式优点
1.每个消费者都可以消费到所有queue的消息，消费者不用再关心重平衡。
2.消费者不与某个queue强绑定，不会因为某个消费者hang住导致某个queue堆积。
但是按照 &quot;消息粒度负载均衡&quot; 来消费数据不是也是同样的效果吗？为什么还要实现这个pop模式？</div>2023-07-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/1d/de/62bfa83f.jpg" width="30px"><span>aoe</span> 👍（0） 💬（1）<div>原来支持 gRPC 是为了简化多语言 SDK 的开发</div>2023-07-16</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/aa/0c/6a65f487.jpg" width="30px"><span>cykuo</span> 👍（3） 💬（0）<div>首先在生产者开始生产消息，包括根据remoting协议序列化消息内容，然后尝试访问namesrv获取所有broker信息，然后根据自己发送消息topic消息决定将数据投递到具体哪个broker上。投递动作根据投递方式的不同分为同步发送，异步等发送方式的不同略有差异。消息在投递到broker之后，如果是发送到topic中，则需要在broker上完成生产分发的工作，决定消息最后投递到哪个queue上。如果是投递到queue则可以省略这一步。（这里不管是topic还是queue应该都是逻辑概念，通过索引所描述的在commitLog中的逻辑关系所决定的）。最后在consumer侧，则默认是使用pull模式来拉取消息，首先从namesrv中获取所有broker的信息，进而确定自己需要的数据坐标信息，在拉取消息之后还有提交消费位点等动作，另外在消费侧还有其他的消费模式POP&#47;PUSH（这里问作者一个问题，POP模式是否可以避免因为消费者的rebalance？当然broker自身导致的rebalance是无法避免的。。。）</div>2023-07-14</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTLFAw6al5teduStTwsALr6OVCbWEOviaHq1xrsqn9pgGibRxtJur4FndDzibCkic0Sk8Tv02ANXm9GdFA/132" width="30px"><span>赵海升</span> 👍（2） 💬（1）<div>许老师 这个消息粒度负载均衡 的配图有点小疑惑 , R3 和 R5 的 不被消费吗 ？R2 R4  别同一个消费组的cosume1 消费两次？这图是不是有问题</div>2023-07-17</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/DYAIOgq83ersGSic8ib7OguJv6CJiaXY0s4n9C7Z51sWxTTljklFpq3ZAIWXoFTPV5oLo0GMTkqW5sYJRRnibNqOJQ/132" width="30px"><span>walle斌</span> 👍（0） 💬（0）<div>补充rocketmq 一个特性，对比kafka  对于业务开发有个巨大的优势就是并发，kafka的并发等于partition数目，提升涉及到的改动比较大，而rocketmq的并发等于readQueueNum* client的多线程，并且rocketmq通过客户端与broker 配合实现了，并发消费与消息重试得兼容功能，这点对于大部分都是IO操作的业务而言提升巨大。</div>2024-12-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/f0/85/6dfb8ac5.jpg" width="30px"><span>开发很忙</span> 👍（0） 💬（0）<div>Pull模型和Pop模型的区别是消费重平衡的工作在客户端完成和在服务端完成吗？</div>2023-09-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/28/43/5062a59b.jpg" width="30px"><span>shan</span> 👍（0） 💬（0）<div>总结
协议网络模块
RocketMQ 5.0以前使用的是自定义的Remoting协议，5.0以后增加了gRPC协议的支持，Remoting基于四层的TCP协议通信，gRPC基于七层的HTTP2协议通信，不过底层也是基于TCP。
Remoting是私有协议，在多语言SDK开发时，一些基础的工作都需要重新开发，而且与第三方服务集成不便捷。
gRPC是公有协议，底层已经实现了网络通信、编解码等基础框架，提供了各个语言的开发库，非常轻便，并且有天然的生态集成能力，比如Service Mesh、Kubernetes等。

元数据存储
Broker中存储了元数据信息，在启动的时候会向所有NameServer上报自己负责的Topic有哪些，消息队列有哪些，之后生产者和消费者就可以通过NameServer获取Topic的路由信息。
NameServer一般是多节点部署，每个节点之间是对等的，没有主从之分。

消息数据存储
RocketMQ一般会将Topic划分为多个MessageQueue，不过在底层文件存储方面，所有MessageQueue都对应一个CommitLog，消息会被顺序写入CommitLog文件。单个CommitLog大小为1G，超出限定之后会新起一个文件。

ConsumeQueue是逻辑消息队列，因为CommitLog中存储的是所有消息，为了根据Topic进行检索，所以创建了ConsumeQueue，每个Topic都会有一个对应的ConsumeQueue目录，里面是该Topic下所有消息队列对应的ConsumeQueue文件，文件中记录了该消息队列里面每条消息在CommitLog中的偏移量。
消费者就是通过这个ConsumeQueue进行消息消费的。

IndexFile是为了便于根据Key对消息进行检索设计的。

ConsumeQueue和IndexFile存储的是索引数据，数据量一般不大，所以不需要分段存储。

生产者
生产者发送消息的时候，需要知道往哪个Topic上发，Topic信息可以从NameServer获取，之后会根据算法（轮询算法或者最小投递延迟算法）选取其中一个MessageQueue进行发送。

消费者
消费者支持Pull、Push、Pop 三种消费模型。
Pull模式：需要消费者主动调用poll方法获取消息，从表面上看消费者需要不断主动进行消息拉取，所以叫做拉模式。

Push模式：从名字上看起来是消息到达Broker后推送给消费者，实际上还是需要消费者向Broker发送拉取请求获取消息内容，获取之后触发回调函数进行消费，从表面上看就像是Broker主动推送给消费者一样，所以叫做推模式。

Pop模式：RocketMQ 5.0以后新增了Pop模式，它主要是将消费分区、分区分配关系、重平衡都移到了Broker端。</div>2023-09-19</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/DYAIOgq83ersGSic8ib7OguJv6CJiaXY0s4n9C7Z51sWxTTljklFpq3ZAIWXoFTPV5oLo0GMTkqW5sYJRRnibNqOJQ/132" width="30px"><span>walle斌</span> 👍（0） 💬（1）<div>rocketmq是支持批量发送，详细查看MessageBatch 这个类</div>2023-09-05</li><br/><li><img src="" width="30px"><span>Geek_8562b2</span> 👍（0） 💬（1）<div>老师，消费端和生产端消费生产时是连接到整个NameServer集群吗，还是连接到某一个NameServer节点，如果只是连接到某一个NameServer节点，那么这个节点挂掉，生产端和消费端怎么获取其他NameServer节点信息。</div>2023-08-07</li><br/>
</ul>