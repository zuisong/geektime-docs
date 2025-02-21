你好，我是李玥。

之前的课程，我们大部分时间都在以RocketMQ、Kafka和RabbitMQ为例，通过分析源码的方式，来讲解消息队列的实现原理。原因是，这三种消息队列在国内的受众群体非常庞大，大家在工作中会经常用到。这节课，我给你介绍一个不太一样的开源消息队列产品：Apache Pulsar。

Pulsar也是一个开源的分布式消息队列产品，最早是由Yahoo开发，现在是Apache基金会旗下的开源项目。你可能会觉得好奇，我们的课程中为什么要花一节课来讲Pulsar这个产品呢？原因是，Pulsar在架构设计上，和其他的消息队列产品有非常显著的区别。我个人的观点是，Pulsar的这种全新的架构设计，很可能是消息队列这类中间件产品未来架构的发展方向。

接下来我们一起看一下，Pulsar到底有什么不同？

## Pulsar的架构和其他消息队列有什么不同？

我们知道，无论是RocketMQ、RabbitMQ还是Kafka，消息都是存储在Broker的磁盘或者内存中。客户端在访问某个主题分区之前，必须先找到这个分区所在Broker，然后连接到这个Broker上进行生产和消费。

在集群模式下，为了避免单点故障导致丢消息，Broker在保存消息的时候，必须也把消息复制到其他的Broker上。当某个Broker节点故障的时候，并不是集群中任意一个节点都能替代这个故障的节点，只有那些“和这个故障节点拥有相同数据的节点”才能替代这个故障的节点。原因就是，每一个Broker存储的消息数据是不一样的，或者说，每个节点上都存储了状态（数据）。这种节点称为“有状态的节点（Stateful Node）”。
<div><strong>精选留言（18）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/12/d1/29/1b1234ed.jpg" width="30px"><span>DFighting</span> 👍（46） 💬（3）<div>其实存储计算分离在数据的相关性不大的情况下优势会很明显，我理解这种是对数据和计算进行了一种操作和对象的切分，在大多数情况下，操作和对象的耦合度不高，可以使用，因为无状态、单一功能这就是微服务架构的优势。但是这里有个天然的缺陷就是牺牲了大量的磁盘读写和网络IO的性能，如果计算和对象耦合度过大，也就是计算需要频繁读写多数据源的数据，那这种就不如传统的MQ了。不过随着数据量的增大，读写计算分离应该是趋势，如果数据和计算耦合度过高，优先思路应该是重新划分业务模块和整合数据源，把耦合相关的劣势转换为优势，不过这一点很难，需要业务专家、技术专家、架构专家和数据专家等的一起努力。</div>2019-10-25</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/8b/ec/dc03f5ad.jpg" width="30px"><span>张天屹</span> 👍（0） 💬（3）<div>老师你好，请教一个本章的题外问题，对于严格的局部顺序性要求场景，比如十个分区，十个消费者线程，一一对应是可以保证的。但是绝不能一对多&#47;批量预取，这个不设置多线程消费就可以了，但是在进程角度的话，为了保证顺序性，一个分区也只能被一个进程消费，那就没办法做消费者集群了吗，只有一个单体的消费者服务的话，可靠性是不是不太好，如果宕机了下游就完全挂了，这种情况怎么办呢？</div>2019-09-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/04/bd/d1b7e47e.jpg" width="30px"><span>好好写代码</span> 👍（22） 💬（1）<div>消息队列大部分应用的场景还是需要快速去消费数据，吞吐量比持久化优先级高。</div>2019-09-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/05/06/f5979d65.jpg" width="30px"><span>亚洲舞王.尼古拉斯赵四</span> 👍（13） 💬（1）<div>我有一下的几点想法：
1.性能方面的考虑：像文中说的，使用计算存储分离的设计方式，原本broker只需要在本地进行消息查找，但是现在却需要连接到另一个集群中进行查找消息，增加了网络耗时，一旦并发大，带宽占满了，性能就会明显下降。
2.成本原因：
这里的成本包括两方面：一方面是部署成本，本来只需要一个集群部署，现在我还好增加一个存储集群，增加了使用者的钱方面的成本；另一方面是使用者的学习成本，新引入一个集群，无论使用的是什么存储系统，如果想要更好的解决可能出现的问题，使用者都要去学习这个新的存储系统，增加了使用者的学习成本。
</div>2019-10-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/1d/13/31ea1b0b.jpg" width="30px"><span>峰</span> 👍（7） 💬（0）<div>本来就是数据管道结果管道还要套层管道，计算本来就很轻，分离出去一种浪费的感觉。</div>2019-12-25</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/d1/29/1b1234ed.jpg" width="30px"><span>DFighting</span> 👍（6） 💬（2）<div>读了文章才发现，我们使用Flink做ETL真的很不适合，因为Flink适合计算，存储应该另外设计，系统设计存在明显的缺陷</div>2019-10-25</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/17/27/ec30d30a.jpg" width="30px"><span>Jxin</span> 👍（4） 💬（0）<div>回答问题：
1.mq这一侧的计算复杂度和存储管理难度都未到做更细拆分的程度。
2.在这些mq出来前，k8s这种容器编排的方案还没有。做结构拆分势必会增加复杂度，导致入门门槛提高，进而就不易于推广。而开源项目，亲和易推广也是很重要的指标。



自己的想法：
存储层在引入k8s的pv，pvc管理后，存储的管理复杂度就可以跟业务开发说再见了。毕竟上云后，这块东西就由云服务商承接走了。这样有利于更轻量的开发，亲和拥抱变化的市场环境。所以老师说是趋势。</div>2019-11-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/89/e6/ab403ccb.jpg" width="30px"><span>boyxie</span> 👍（2） 💬（0）<div>可以用在对实时性要求不高的应用，比如定时任务类型的，可以存储海量数据</div>2019-10-30</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/71/3d/da8dc880.jpg" width="30px"><span>游弋云端</span> 👍（2） 💬（0）<div>个人觉得从微服务的思想来讲，专业的人干专业的事，进行服务的细粒度拆分，不做大而全的系统，这样架构清晰，可扩展性强。其他消息队列适合快速部署，可以做到对外依赖少的精简配置，例如kafka要去ZK，要支持单节点配置等，这与Pulsar是不同的。在后续的微服务、容器等演进的趋势下，个人认为Pulsar会更具有竞争力。目前来看，只能说各有千秋，各有不同的应用场景。</div>2019-09-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/34/df/64e3d533.jpg" width="30px"><span>leslie</span> 👍（2） 💬（0）<div>      不一样的思路：非常喜欢老师这种方式，不仅仅是基于当下，而是持久；让我觉得不仅仅是一个User，而是在User中去扩展。
      就像之前学计算机组成原理是徐老师曾经提过基于CPU的MQ：当时问徐老师为什么有了CPU还需要有GPU？老师让我去看David Patterson老爷爷的文章，包括现在阿里做的GPU减负的是内存，应当是差不多的不一样的思路吧。
     感谢老师分享不一样的新东西：让我们不仅仅基于当下、研究当下，甚至可以在MQ的方向上扩展研究下去。期待老师后面的继续分享。</div>2019-09-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/46/ea/498dc41f.jpg" width="30px"><span>thecode</span> 👍（1） 💬（0）<div>这里有一篇 Pulsar 和 Kafka 性能测试对比的文章

https:&#47;&#47;www.infoq.cn&#47;article&#47;xeyeeenny5cg0pgyxevd
https:&#47;&#47;github.com&#47;streamnative&#47;openmessaging-benchmark&#47;blob&#47;master&#47;blog&#47;benchmarking-pulsar-kafka-a-more-accurate-perspective-on-pulsar-performance.pdf</div>2021-11-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/52/ba/440c0157.jpg" width="30px"><span>小红帽</span> 👍（0） 💬（0）<div>一方面，计算与存储分离这种思想并没有提高生产和消费性能，
另一方面，从业务上来说也很少有需要像iot这种千万级客户端通信的场景，这10年都是电子商务的各种变形的应用为主！
基于这种计算和存储的特点和业务场景，决定了市场上用得较多的还是这种成熟的计算与存储一体的架构。</div>2023-03-15</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/28/42/f7/8b57263a.jpg" width="30px"><span>wuhang202</span> 👍（0） 💬（0）<div>首先消息队列需要满足高并发下的低延时，hdfs为离线大数据批量计算而生，无法满足，mysql无法直接支持海量数据，因此需要消息队列定制化自己的存储。
此外，增加依赖，也增加了中间件入门、维护及使用的复杂度，作为中间件要尽可能保证最小依赖，例如rocketmq自带服务注册发现的nameserver，kafka将要移除zookeeper。</div>2021-12-07</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/19/d9/ff/b23018a6.jpg" width="30px"><span>Heaven</span> 👍（0） 💬（0）<div>好处是,读写分离,专注传输,集群状态变更速度快,利用现成的存储系统开发效率高
坏处是,增加网络传输,降低性能,读写性能低
从上面来看,好处的确不少,但是我们现阶段对于MQ的要求主要就是性能,在性能提升不上去的情况下,好处多也没啥用,就好比是容器界的gVisor,虽然代表着一种发展方向,但是由于性能问题,应用面仍然上不去</div>2021-02-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/f2/c3/f18e4507.jpg" width="30px"><span>远鹏</span> 👍（0） 💬（0）<div>计算存储分离加大了可控性，无论是对于开发还是运维来说都是一件好事</div>2020-03-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/41/87/46d7e1c2.jpg" width="30px"><span>Better me</span> 👍（0） 💬（0）<div>消息队列本身作为中间层应该以提升更好的性能为导向，但目前Pulsar的存储计算分离架构等于在中间层在分层，在架构上可以做到服务化单一职责，以及无状态的broker节点，但却有少许的性能损耗，如果以后能解决性能损耗的问题，那么存储计算分离架构必然是未来的趋势</div>2019-09-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/12/1b/f62722ca.jpg" width="30px"><span>A9</span> 👍（0） 💬（0）<div>是否使用存储计算分离也是一种trade off的体现。采用分离的架构，整个架构上模块更加清晰，能够降低开发成本，提升开发效率。不采用存储计算分离的架构，可能开发难度较大，不过整体效率更高。对于开发消息中间件来说，尤其是之前消息队列诞生时，计算机性能普遍性能交叉，可能牺牲一点开发的效率，获取更高的性能才是更重要的。
另外，最近流计算的流行，同样的存储计算分离架构可能有能直接进行配合（并不太了解流计算）
总结来说，算是诞生的时代背景占了相当大的原因吧</div>2019-09-26</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/3XbCueYYVWTiclv8T5tFpwiblOxLphvSZxL4ujMdqVMibZnOiaFK2C5nKRGv407iaAsrI0CDICYVQJtiaITzkjfjbvrQ/132" width="30px"><span>有铭</span> 👍（0） 💬（0）<div>消息队列的性能是个很重要的需求，既然存储计算分离了也就等于加了中间层。我们都知道加了中间层那是会损失性能的</div>2019-09-26</li><br/>
</ul>