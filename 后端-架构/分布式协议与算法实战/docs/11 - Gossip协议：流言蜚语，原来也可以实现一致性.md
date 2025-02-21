你好，我是韩健。

有一部分同学的业务在可用性上比较敏感，比如监控主机和业务运行的告警系统。这个时候，相信你希望自己的系统能在极端情况下（比如集群中只有一个节点在运行）也能运行。回忆了二阶段提交协议和Raft算法之后，你发现它们都需要全部节点或者大多数节点正常运行，才能稳定运行，那么它们就不适合了。而根据Base理论，你需要实现最终一致性，怎么样才能实现最终一致性呢？

在我看来，你可以通过Gossip协议实现这个目标。

Gossip协议，顾名思义，就像流言蜚语一样，利用一种随机、带有传染性的方式，将信息传播到整个网络中，并在一定时间内，使得系统内的所有节点数据一致。对你来说，掌握这个协议不仅能很好地理解这种最常用的，实现最终一致性的算法，也能在后续工作中得心应手地实现数据的最终一致性。

为了帮你彻底吃透Gossip协议，掌握实现最终一致性的实战能力，我会先带你了解Gossip三板斧，因为这是Gossip协议的核心内容，也是实现最终一致性的常用三种方法。然后以实际系统为例，带你了解在实际系统中是如何实现反熵的。接下来，就让我们开始今天的内容吧。

## Gossip的三板斧

Gossip的三板斧分别是：直接邮寄（Direct Mail）、反熵（Anti-entropy）和谣言传播（Rumor mongering）。
<div><strong>精选留言（30）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/10/fb/7b/2d4b38fb.jpg" width="30px"><span>Jialin</span> 👍（50） 💬（7）<div>课堂笔记（综合第四讲和第十一讲内容）
1.Gossip 协议存在的原因？
为了实现 BASE 理论中的“最终一致性原则”。两阶段提交协议和 Raft 算法需要满足“大多数服务节点正常运行”原则，如果希望系统在少数服务节点正常运行的情况下，仍能对外提供稳定服务，这时就需要实现最终一致性。
最终一致性是指系统中所有的数据副本在经过一段时间的同步后，最终能够达到一个一致的状态。
2.最终一致性原则中的一致性标准（实际工程实践）
• 以最新写入的数据为准，比如 AP 模型的 KV 存储采用的就是这种方式
• 以第一次写入的数据为准，如果不希望存储的数据被更改，可以以它为准
3.实现最终一致性的具体方式
• 读时修复：在读取数据时，检测数据的不一致，进行修复。比如 Cassandra 的 Read Repair 实现，具体来说，在向 Cassandra 系统查询数据的时候，如果检测到不同节点的副本数据不一致，系统就自动修复数据
• 写时修复：在写入数据，检测数据的不一致时，进行修复。比如 Cassandra 的 Hinted Handoff 实现。具体来说，Cassandra 集群的节点之间远程写数据的时候，如果写失败就将数据缓存下来，然后定时重传，修复数据的不一致性
• 异步修复：这个是最常用的方式，通过定时对账检测副本数据的一致性，并修复
4.Gossip 协议实现最终一致性
• 直接邮寄，即写时修复，直接发送更新数据，当数据发送失败时，将数据缓存在失败重试队列，然后重传。这种方式虽然存在丢数据问题，但是实现简单、数据同步及时，不需要校验数据一致性对比，性能消耗低
• 反熵，即异步修复，集群中的节点，每隔段时间就随机选择某个其他节点，然后通过互相交换自己的所有数据来消除两者之间的差异，实现数据的最终一致性。主要有推、拉、推拉三种实现方式。适合集群节点数已知、少量、稳定的场景，主要由于反熵需要节点两两交换和比对自己所有的数据，执行反熵时通讯成本会很高，性能消耗高。需要注意的是实现反熵时一般设计一个闭环的流程，一次修复所有节点的副本数据不一致，因为我们希望能在一个确定的时间范围内实现数据副本的最终一致性，而不是基于随机性的概率，在一个不确定的时间范围内实现数据副本的最终一致性
• 谣言传播，指的是当一个节点有了新数据后，这个节点变成活跃状态，并周期性地联系其他节点向其发送新数据，直到所有的节点都存储了该新数据。由于谣言传播非常具有传染性，它适合动态变化的分布式系统
5.思考题：既然使用反熵实现最终一致性时，需要通过一致性检测发现数据副本的差异，如果每次做一致性检测时都做数据对比的话，肯定是比较消耗性能的，那有什么办法降低一致性检测时的性能消耗呢？
除了老师在文章中提到的通过校验和进行数据一致性检测，可以借鉴通信原理中数据校验方法，如奇偶校验、CRC校验和格雷码校验等方式，但是这些方式只能检测出错误，但是无法纠错，可以通过重传的方式进行纠错。</div>2020-03-06</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/47/31/f35367c8.jpg" width="30px"><span>小晏子</span> 👍（26） 💬（1）<div>一致性检测是对比两个节点上的数据是否一致，如果每次都是全量比对，那么肯定性能不是很高，那为了提升性能，那么最好是不比对或增量数据比对，这里抛个砖，
1. 假设从某一时刻开始，所有节点数据都是一致的，每个节点都记录从这个时刻开始的数据变化，
2. 当反墒放生时，先看相关的两个节点上数据变化是否为空，如果为空就证明两个节点此时数据一致，不需要数据同步。
3. 如果相关的两个节点上数据有变化，则只比较变化的数据，然后只同步变化的差集，同时也要更新数据变化状态记录，
4. 在某个时间段内数据的变化只增不减，某个时刻所有节点做全量比对，然后重置数据变化记录。
5. 为了快速比较，可以同时计算数据变化记录的hash值用于比较，hash值一样就说明数据变化是相同的，两节点数据一致，否则就需要一致性查询并同步。</div>2020-03-06</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/82/3d/356fc3d6.jpg" width="30px"><span>忆水寒</span> 👍（23） 💬（4）<div>老师，有个疑惑。文章中说直接邮寄肯定要实现的，在固定节点的系统中可以实现反墒修复一致性。那么两者如何兼容呢？是不是每次有新数据写入，先执行直接邮寄。然后周期性的执行反墒修复数据一致性呢？</div>2020-03-06</li><br/><li><img src="" width="30px"><span>myrfy</span> 👍（17） 💬（4）<div>老师，gossip中，遇到数据冲突，以谁为准呢？</div>2020-03-06</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/e6/62/ee1c96e8.jpg" width="30px"><span>老辉</span> 👍（15） 💬（2）<div>老师，如果反熵过程中，组成的环上的一个节点挂了，怎么同步数据一致。</div>2020-03-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/4d/54/9c214885.jpg" width="30px"><span>kylexy_0817</span> 👍（11） 💬（1）<div>韩老师好，我觉得其实就目的而言，Gossip的三板斧都是为了反熵，即都是为了降低系统因为数据不一致引起的混乱程度，只是实现方法不一样，第一种用到消息队列，就是消息订阅发布模式；第二种不经消息队列，直接推拉消息到随机节点；第三种就是散播谣言，这里方法是推，还应该会涉及一个散播算法，避免消息重复下发，避免消息风暴。不知我的理解到不到位？</div>2020-04-26</li><br/><li><img src="" width="30px"><span>Scott</span> 👍（10） 💬（1）<div>merkle tree可以用来减少比较差异负担的开销吗</div>2020-03-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/16/bd/e14ba493.jpg" width="30px"><span>翠羽香凝</span> 👍（6） 💬（3）<div>老师，感觉谣言传播有很多细节值得讨论，比如：谣言何时停止？什么时候算是网络里都达到了一致性？而不是无止境的传下去？又比如：谣言传播可能会有很多消息被反复重传，会不会造成网络性能的下降？</div>2020-03-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/99/f4/e0484cac.jpg" width="30px"><span>崔伟协</span> 👍（6） 💬（1）<div>直接邮寄，反熵，谣言传播三者的区别是什么</div>2020-03-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/54/9a/76c0af70.jpg" width="30px"><span>每天晒白牙</span> 👍（4） 💬（2）<div>今日得到
出于可用性考虑(即使一个节点也照常运行)，而二阶段提交和 raft 协议都是需要保证大多数几点正常运行才能保证稳定运行。根据 base 理论要实现最终一致性，所以 gossip 协议就出来了。

gossip 协议是一种利用随机，带有传染性的方式，将数据传播到整个网络中，在一定时间内，使网络内的所有节点达到最终一致性

gossip 协议有三种方法
1.直接邮寄【必须要实现的】
直接发送更新数据给其他节点，如果失败缓存起来，然后后续进行重传。这种方式相对比较简单，但有个缺点是如果缓存满了会存在丢数据的风险

2.反熵
反熵是指消除节点之间的数据差异，它是一种异步修复数据从而达到最终一致性的方案
主要是指集群中的节点每隔断时间就随机选择集群中其他节点进行数据交换，达到数据同步的目的，这里有推、拉、推拉三种模式。
因为反熵需要对比数据，所以挺耗性能的，老师提到可以通过校验和的方式解决，这块我下去需要在查查相关资料
反熵有个局限性就是要求几点已经，且节点数量不能太多

3.谣言传播
当一个节点有了新数据后，这个节点变成活跃状态，并周期性的向其他节点发送数据，直到所有节点都存储了这个新数据
这种方式适合动态变化的分布式系统

思考题
反熵在做数据差异检查时是通过对比数据来进行的，比较耗性能，有啥好方式解决？
老师在专栏中提到了使用校验和的方式，但还不太懂这种方式，老师可以简单介绍下吗？</div>2020-03-06</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/43/79/18073134.jpg" width="30px"><span>test</span> 👍（3） 💬（1）<div>这三种方式，是不是主要的区别就是在过程中充当发起者的是单一个节点、轮询节点、多个节点？</div>2020-06-03</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/25/00/3afbab43.jpg" width="30px"><span>88591</span> 👍（3） 💬（1）<div>直接对比内容签名</div>2020-04-02</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/60/4f/db0e62b3.jpg" width="30px"><span>Daiver</span> 👍（2） 💬（1）<div>Fabric目前1.4.1版本以上实现了raft共识，不过用的是etcd的组件；Hyperledger Fabric 中组织内部的peer节点之间为了同步账本数据使用了gossip协议。</div>2020-03-07</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTLIBabuBHlohpGYRDt4mwWghVDztHyRnC9SfyYnENUZNbCe8m05qQn0cHdiazU4eKmMtSQ0bHicwLLQ/132" width="30px"><span>vi</span> 👍（2） 💬（2）<div>老师，对于数据复制，只有新增或减少的两处情况，有没有相同的数据不同版本的情况出现，比如数据库中相同ID的数据，某个字段不一致，要不要利用记录的时间擢来制定一个规则，以最后更新的数据为准确数据来做更新复制</div>2020-03-06</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/7c/25/7d9a2538.jpg" width="30px"><span>蚂蚁</span> 👍（1） 💬（1）<div>老师好 有一个疑问 课程中以数据丢失为例 如果两个节点所有数据的key一致 仅仅是value不同 那怎么确定谁的数据是对的呢？按照课程里的理论会不会导致新数据更新成功了但是集群最终的数据又变成旧数据了</div>2020-10-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/9d/ec/235b74c0.jpg" width="30px"><span>ppyh</span> 👍（1） 💬（1）<div>shard的各个节点有主副之分吗，读取的时候是不是允许读到的数据不是最新的？</div>2020-06-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/82/3d/356fc3d6.jpg" width="30px"><span>忆水寒</span> 👍（1） 💬（1）<div>2020年4月23日，这是第二遍阅读。感觉基本上能理解了，比之前的理解要深一些。加油！</div>2020-04-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/b7/ae/a25fcb73.jpg" width="30px"><span>colin</span> 👍（1） 💬（1）<div>反熵有点像路由算法啊</div>2020-04-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/42/62/536aef06.jpg" width="30px"><span>tim</span> 👍（1） 💬（1）<div>时序数据库存储的数据都是压缩的，而且一般都是分block的，如果反熵发现其中一个时间段的数据丢了，是整个block copy吗？这样会不会效率低？
数据写入会记录唯一ID吗？</div>2020-03-31</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/81/e6/6cafed37.jpg" width="30px"><span>旅途</span> 👍（1） 💬（1）<div>把数据生成一个hash值 每次比较这个hash值  我之前看过微服务中拉取注册中心的配置时,不是拉取所有的配置和本地比较 而是通过生成的hash值比较的 和这个应该是一个道理</div>2020-03-10</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTKfNticCvATj7dqwXfABo03DicMvEXmgwuPgff6KcLyU3wdxedJVDPWsqPIERmosAau7ClIlsibhRTpA/132" width="30px"><span>InfoQ_b4b7ff0241e5</span> 👍（1） 💬（1）<div>从网上搜了搜相关资料，发现大部分资料将谣言传播等同于gossip协议，也有把反熵等同于gossip协议的，感到很迷惑。</div>2020-03-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/0d/86/84984798.jpg" width="30px"><span>唐明</span> 👍（1） 💬（1）<div>请问老师，数据可以从任意一个副本节点写入吗？</div>2020-03-06</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/f4/e2/dbc4a5f2.jpg" width="30px"><span>朱东旭</span> 👍（1） 💬（1）<div>分片应该区分主分片和副本分片吧，只有主分片能更新。</div>2020-03-06</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/13/81/4dcb0f55.jpg" width="30px"><span>Geek_8af153</span> 👍（1） 💬（1）<div>同问因为分区错误导致数据不一致时，合并冲突怎么解决？</div>2020-03-06</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/f8/ba/d28174a9.jpg" width="30px"><span>Geek_zbvt62</span> 👍（1） 💬（1）<div>内容挺重要但疑问挺多，求翻牌：
Influxdb的例子讲解了修复数据，但没讲数据一开始是怎样产生的。结合最后总结中提到“直接邮寄必须实现”，能不能这样猜测：
一个请求到达某实例，实例写入本机shard，然后通过类似“直接邮寄”，发送给其他shard副本。修复工作是在在后台异步进行的。
另一个问题，即使以上猜测不是您的实现的方式，如果我做一个分布式中间件，采用这种方式冗余数据是否可行？
第三个问题，有哪个gossip实现的源码可以看一看，希望是用于大量用户数据交换的，我了解到有一些实现比如HashiCorp的，是用来维护集群成员管理的，我不知道这种在数据量猛增的场景下是否还适用

思考题，也许可以基于时间戳或者版本号机制来减小传输和比对的数据量。主分片同一时刻只有一个，所以版本号由主分片负责的节点来递增就好。</div>2020-03-06</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/fb/1a/57480c9c.jpg" width="30px"><span>AnonymousUser</span> 👍（0） 💬（1）<div>图10中ABC节点循环时要是B宕机了，整个过程就进行不下去了？是不是应该有个协商机制来做配置的更新啊？如何维护节点之间的前后关系啊？</div>2020-10-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1a/9e/d4/95f6fb65.jpg" width="30px"><span>仲夏夜空星星多</span> 👍（0） 💬（1）<div>感觉实现细节是不是没有提到，比如两个节点怎么做diff,怎么有效把diff 数据传过去</div>2020-08-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/19/d9/ff/b23018a6.jpg" width="30px"><span>Heaven</span> 👍（0） 💬（1）<div>看了大佬们的留言后,我这里提议中,就是先利用序号或者哈希等方式,计算一个总体的值,利用这个值来判断反熵的是否启动.</div>2020-08-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/67/d5/1b26b725.jpg" width="30px"><span>Gopher</span> 👍（0） 💬（1）<div>思考题：

本来想说用一个单调递增的消息id ，节点之间通过最大的消息id对比进行校验，但是好像在动态的节点中做不到单调递增。
只能想到通过摘要来校验了</div>2020-07-15</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/c5/00/37ef050e.jpg" width="30px"><span>superfq</span> 👍（0） 💬（1）<div>有个问题请老师解惑下：
对于集群中删除数据的不一致如何处理？不如A节点删除了一个key，B节点没有删除，在进行反熵对比的时候，A发送给B的差异数据中没有这个key，B如何达到有一致？</div>2020-06-13</li><br/>
</ul>