你好，我是何小锋。在上一讲中，我讲了“怎么设计一个灵活的RPC框架”，总结起来，就是怎么在RPC框架中应用插件，用插件方式构造一个基于微内核的RPC框架，其关键点就是“插件化”。

今天，我要和你聊聊RPC里面的“服务发现”在超大规模集群的场景下所面临的挑战。

## 为什么需要服务发现？

先举个例子，假如你要给一位以前从未合作过的同事发邮件请求帮助，但你却没有他的邮箱地址。这个时候你会怎么办呢？如果是我，我会选择去看公司的企业“通信录”。

同理，为了高可用，在生产环境中服务提供方都是以集群的方式对外提供服务，集群里面的这些IP随时可能变化，我们也需要用一本“通信录”及时获取到对应的服务节点，这个获取的过程我们一般叫作“服务发现”。

对于服务调用方和服务提供方来说，其契约就是接口，相当于“通信录”中的姓名，服务节点就是提供该契约的一个具体实例。服务IP集合作为“通信录”中的地址，从而可以通过接口获取服务IP的集合来完成服务的发现。这就是我要说的RPC框架的服务发现机制，如下图所示：

![](https://static001.geekbang.org/resource/image/51/5d/514dc04df2b8b2f3130b7d44776a825d.jpg?wh=2746%2A1445 "RPC服务发现原理图")

1. 服务注册：在服务提供方启动的时候，将对外暴露的接口注册到注册中心之中，注册中心将这个服务节点的IP和接口保存下来。
2. 服务订阅：在服务调用方启动的时候，去注册中心查找并订阅服务提供方的IP，然后缓存到本地，并用于后续的远程调用。
<div><strong>精选留言（30）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/10/c3/08/28c327d0.jpg" width="30px"><span>冰河时代</span> 👍（18） 💬（4）<div>记得之前在京东的时候，服务挂了，在注册中心上还得要手动删除下死亡节点，如果zk的话，服务没了，就代表会话也没了，临时节点的特性，应该会被通知到呀？为什么还要手动删除呢</div>2020-03-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/0f/bf/ee93c4cf.jpg" width="30px"><span>雨霖铃声声慢</span> 👍（14） 💬（1）<div>如果要能切换流量，那么要服务端配置有权重负载均衡策略，这样服务器端可以通过调整权重来安排流量</div>2020-03-07</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/69/cc/747c7629.jpg" width="30px"><span>🌀Pick Monster 🌀</span> 👍（12） 💬（3）<div>消息总栈类似一个队列，队列表示是递增的数字，注册中心集群的任何一个节点接收到注册请求，都会把服务提供者信息发给消息总栈，消息总栈会像队列以先进先出的原则推送消息给所有注册中心集群节点，集群节点接收到消息后会比较自己内存中的当前版本，保存版本大的，这种方式有很强的实效性，注册中心集群也可以从消息总栈拉取消息，确保数据AP，个人理解这是为了防止消息未接收到导致个别节点数据不准确，因为服务提供者可以向任意一个节点发送注册请求，从而降低了单个注册中心的压力，而注册和注册中心同步是异步的，也解决了集中注册的压力，在Zookeeper中，因为Zookeeper注册集群的强一致性，导致必须所有节点执行完一次同步，才能执行新的同步，这样导致注册处理性能降低，从而高I&#47;O操作宕机。
以上是我的个人理解，老师给看一下是否正确。

还有一个问题：当集中注册时，消息总栈下发通知给注册中心集群节点，对于单个节点也会不停的收到更新通知，这里也存在高I&#47;O问题，会不会有宕机？</div>2020-03-07</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/7b/98/8f1aecf4.jpg" width="30px"><span>楼下小黑哥</span> 👍（11） 💬（1）<div>服务消费者都是从注册中心拉取服务提供者的地址信息，所以我们要切走某些服务提供者数据，只需要将注册中心这些实例的地址信息删除（其实下线应用实例，实际也是去删除注册中心地址信息），然后注册中心反向通知消费者，消费者受到拉取最新提供者地址信息就没有这些实例了。
老师，提问一个问题：现有开源注册中心是不是还没有消息总线这种实现方式？消息总线有没有开源实现？
</div>2020-03-06</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/42/76/256bbd43.jpg" width="30px"><span>松花皮蛋me</span> 👍（10） 💬（1）<div>路由负载</div>2020-03-06</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/51/b4/0d402ae8.jpg" width="30px"><span>南桥畂翊</span> 👍（8） 💬（1）<div>消息总线策略是啥，老师能指点下么，怎么保证消息总线全局版本递增</div>2020-03-30</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTJD8FqEJwgFLR345UPmwKibMribfD8rEHrtweQTsKPpkfLiaUCesXrW9Iib0niaibib0th6WcKbsKFoicFS2Q/132" width="30px"><span>君言</span> 👍（8） 💬（1）<div>老师，在AP实现中“两级缓存，注册中心和消费者的内存缓存，通过异步推拉模式来确保最终一致性”能展开讲一下具体实现吗？另外请教下CP可以基于zk实现，AP在业内的实现方式有哪些呢？</div>2020-03-06</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/67/f4/9a1feb59.jpg" width="30px"><span>钱</span> 👍（5） 💬（1）<div>小结一下
1：注册中心的核心作用？
完成服务消费者和服务调用者，两者的路径匹配

2：注册中心的核心指标？
高效、稳定、高可用，使服务消费者及时感知节点的变化

3：路径匹配需要的信息？
服务提供者IP、端口、接口、方法＋服务分组别名
服务消费者IP、端口
路径匹配可以把分组别名利用上，即使提供者实例上线，不过由于设置的别名和服务消费者需要的不一致流量也不会打过去，什么时候打过去可以通过配置中心来自由的控制。分组内也是有多个服务提供者的，这里可以再利用相关的负载均衡策略来具体分发流量。</div>2020-05-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/c2/fe/038a076e.jpg" width="30px"><span>阿卧</span> 👍（4） 💬（1）<div>zookeeper注册中心实现原理
1. 服务平台向zookeeper创建服务目录
2. 服务提供者向zookeeper创建临时节点
3. 服务调用者订阅zookeeper，创建临时节点，拉取服务全量数据，watch服务全部节点数据
4. zookeeper节点发生变化会通知服务调用者

切掉服务流量，只需要将注册中心的配置节点下掉就好了</div>2020-03-06</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/23/be/81bd6a7b.jpg" width="30px"><span>knife</span> 👍（3） 💬（1）<div>稍微做点压测作为参考，我说的未必是对的，zookeeper写要是zab协议的，
提交要大多数成功才能提交，所以越多节点效率可能越慢，
</div>2020-05-14</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTJiaiaQYkUHByDARl4ULduH8Y4hicOpMxGjzPZmJkXK9RYd1oVMICd0icCfarxI4Yvmiap2a8t3Eae3LMg/132" width="30px"><span>etdick</span> 👍（3） 💬（1）<div>EURAKA就是AP模型</div>2020-03-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/e3/64/871dd03e.jpg" width="30px"><span>成熟中的猪</span> 👍（3） 💬（1）<div>如文中描述： ZooKeeper 的节点数量特别多，对 ZooKeeper 读写特别频繁，且 ZooKeeper 存储的目录达到一定数量的时候，ZooKeeper 将不再稳定，CPU 持续升高，最终宕机。
这里有点笼统，是否有量化的压测数据或者实际经验值可以分享？</div>2020-03-09</li><br/><li><img src="" width="30px"><span>嘻嘻</span> 👍（2） 💬（1）<div>老师，消息总线构建ap 型注册中心，不是很理解。是多个注册中心独立提供读写，他们之间通过消息队列做数据同步？那么一致性感觉不好保证，比如服务a 先注册，再反注册，但是分别发到两个注册中心节点，最终同步可能是乱序的哇</div>2020-04-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/fb/98/6f238b8e.jpg" width="30px"><span>半个柚子</span> 👍（1） 💬（1）<div>文中说的使用AP来代替CP，直接用Eureka来代替Zookeeper就行了吧</div>2020-04-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/d3/8d/f4ab1eab.jpg" width="30px"><span>zero</span> 👍（1） 💬（1）<div>老师，有一种场景zk可能无法发现，如有台服务发生了gc，这时过来的请求大部分人都会失败，但是还是会把请求路由到此实例上来，这个有什么好的方案吗？</div>2020-03-31</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/f3/a0/a693e561.jpg" width="30px"><span>魔曦</span> 👍（1） 💬（1）<div>注册中心的选型可以采用现有的nacos；或者基于gossip协议来搞</div>2020-03-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/07/8c/0d886dcc.jpg" width="30px"><span>蚂蚁内推+v</span> 👍（1） 💬（2）<div>请问老师，dubbo的服务发现也是用zk实现的，在大规模时有这个问题呢？</div>2020-03-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/f0/61/fedca2e9.jpg" width="30px"><span>(Kelen)</span> 👍（1） 💬（1）<div>终于看到这个消息总线的另一个应用，我们的配置中心也利用了这个原理</div>2020-03-07</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/8d/76/994a9929.jpg" width="30px"><span>OlafOO</span> 👍（0） 💬（1）<div>服务上线没有及时同步不会影响业务，但是服务下线了，单靠重试机制来避免问题么，要是掉用方配置的重试次数是0那这次请求就失败了</div>2020-04-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/67/0e/c77ad9b1.jpg" width="30px"><span>eason2017</span> 👍（0） 💬（2）<div>老师好，会存在一个服务多机房注册到不同的注册中心的情况吧？这样版本号的粒度是按照服务下的机器来做？请指点，谢谢</div>2020-04-15</li><br/><li><img src="https://wx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTK2sqFM20XhgC5xjEfDhbB1lk6rIe7LnqnxEicDdEcRSJ20YCTeBEcYFE84lvHFrJDq9n4WW7P9Zkg/132" width="30px"><span>nothing</span> 👍（0） 💬（2）<div>老师，怎么理解zk的强一致性呢？</div>2020-04-07</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/21/20/1299e137.jpg" width="30px"><span>秋天</span> 👍（0） 💬（1）<div>那个消息总线模式还是搭配原来的zookeeper吗？还是单独使用消息总线？</div>2020-04-07</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/a6/6e/0ffa1ff6.jpg" width="30px"><span>XxxxxxxMr</span> 👍（0） 💬（1）<div>文档当中所提到的Hazelcast。
问题一：这个到底是个啥？
问题二：什么样的业务场景才能用上它？并且发挥出它巨大的优势。</div>2020-04-01</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/05/1b/fc1aa0ac.jpg" width="30px"><span>王大伟</span> 👍（0） 💬（1）<div>看了隔壁的分布式协议算法与实战，感觉可以基于gossip协议实现多节点分布式服务注册中心：
1. 注册中心与服务消费&#47;服务提供节点用netty tcp长连接
2. 注册中心之间的消息通过gossip协议传播
3. 注册中心接到消息，看是否需要投递到服务发现&#47;服务提供节点，有需要就投递

老师，目前有没有较为成熟的gossip开源实现呢？</div>2020-03-25</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/4c/58/25152fa9.jpg" width="30px"><span>kevin</span> 👍（0） 💬（1）<div>注册中心作为rpc框架的核心依赖，如果有问题整体的功能会收到影响，其可用性是一个非常重要的指标，所以更加关注AP，那么在进行技术选型时考虑一些支持AP模式的中间件，例如Redis</div>2020-03-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/4c/58/25152fa9.jpg" width="30px"><span>kevin</span> 👍（0） 💬（1）<div>切流方案是控制流量进行路由，可以通过路由控制或者是给服务提供方设置权重达到目的</div>2020-03-16</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/ef/c3/ecf4c7fb.jpg" width="30px"><span>Sean</span> 👍（0） 💬（1）<div>可以给每个节点加一个weight 有服务发现方控制修改 这个weight还可以用来帮助做负载测试和normalize不同的硬件SKU

老师 请问用AP的方法 怎样可以最快的发现节点消失 比如说crash或长GC</div>2020-03-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/66/9b/59776420.jpg" width="30px"><span>百威</span> 👍（0） 💬（1）<div>老师，求解答……我看到这个思考题，第一反应是负载均衡，我看评论很多也是，也得到了老师的肯定，由此我有几个问题
1.在这种rpc框架中，是不是客户端和注册中心都会有负载均衡？（如果是的话，那这道题答案应该是客户端的吧）如果都有，那他们各自职责怎么明确呢，感觉总会有一些交集？
2.如果客户端有负载均衡，那这些配置也是存在注册中心上么？如果是的话，比如像题中的摘掉流量，应该是也会有一些延时才退给客户端，对么？

谢谢老师～</div>2020-03-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/da/36/ac0ff6a7.jpg" width="30px"><span>wusiration</span> 👍（0） 💬（1）<div>负载均衡，将对应节点的流量切为0</div>2020-03-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1c/ab/72/91c9853e.jpg" width="30px"><span>Reason</span> 👍（0） 💬（1）<div>要把服务流量切走还可以采用客户端服务负载均衡和服务路由的方式。服务路由则采取面向标签的路由方式，根据标签值确定选择访问的服务端实例</div>2020-03-08</li><br/>
</ul>