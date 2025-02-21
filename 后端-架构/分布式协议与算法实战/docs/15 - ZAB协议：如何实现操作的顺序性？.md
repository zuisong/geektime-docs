你好，我是韩健。

很多同学应该使用过ZooKeeper，它是一个开源的分布式协调服务，比如你可以用它进行配置管理、名字服务等等。在ZooKeeper中，数据是以节点的形式存储的。如果你要用ZooKeeper做配置管理，那么就需要在里面创建指定配置，假设创建节点"/geekbang"和"/geekbang/time"，步骤如下：

```
[zk: 192.168.0.10:2181(CONNECTED) 0] create /geekbang 123
Created /geekbang
[zk: 192.168.0.10:2181(CONNECTED) 1] create /geekbang/time 456
Created /geekbang/time
```

我们分别创建了配置"/geekbang"和"/geekbang/time"，对应的值分别为123和456。那么在这里我提个问题：你觉得在ZooKeeper中，能用兰伯特的Multi-Paxos实现各节点数据的共识和一致吗？

当然不行。因为兰伯特的Multi-Paxos，虽然能保证达成共识后的值不再改变，但它不关心达成共识的值是什么，也无法保证各值（也就是操作）的顺序性。而这就是Zookeeper没有采用Multi-Paxos的原因，又是ZAB协议着力解决的，也是你理解ZAB协议的关键。

那么为了帮你更好地理解这个协议，接下来，我将分别以如何实现操作的顺序性、领导者选举、故障恢复、处理读写请求为例，具体讲解一下。希望你能在全面理解ZAB协议的同时，加深对Paxos算法的理解。
<div><strong>精选留言（30）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/10/fb/7b/2d4b38fb.jpg" width="30px"><span>Jialin</span> 👍（34） 💬（5）<div>如果 ZAB 采用的是 UDP 协议，无法保证消息接收的顺序性，主要是因为 TCP 协议本身支持按序确认，而 UCP 只能支持尽最大可能交付</div>2020-04-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/83/39/f9623363.jpg" width="30px"><span>竹马彦四郎的好朋友影法師</span> 👍（10） 💬（1）<div>本质上讲，zab和raft都是通过强领导者模型实现就多值达成共识的</div>2020-05-06</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/PiajxSqBRaEKB0h2nibEbQKcZ6eHkgkmtwMunlibSibT3YAJ8IbDa834HnTAYiajMd8YCdpyDrfhWibCicfpmDCjJzwlA/132" width="30px"><span>z</span> 👍（8） 💬（5）<div>&quot;首先，需要你注意的是，在 ZAB 中，写操作必须在主节点（比如节点 A）上执行。如果客户端访问的节点是备份节点（比如节点 B），它会将写请求转发给主节点&quot;
 关于这一点写请求会转发到主节点， 如果客户端把X，Y发往了两个不同的备份节点，这时候主节点拿到X，Y的顺序是不是没办法保证？ 那最终执行的顺序还是没法保证呀</div>2020-06-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/83/39/f9623363.jpg" width="30px"><span>竹马彦四郎的好朋友影法師</span> 👍（6） 💬（2）<div>怎么感觉zab和raft如果刨去leader选举之外就一模一样了，希望老师解惑，谢谢！</div>2020-05-06</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/5e/32/1ccb2b7c.jpg" width="30px"><span>海连天</span> 👍（4） 💬（1）<div>感觉过程像极了两阶段提交</div>2020-05-03</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/ae/8b/43ce01ca.jpg" width="30px"><span>ezekiel</span> 👍（3） 💬（1）<div>老师您好
我有两个疑问
图 2、3、4中尚无提案准备，是Mutli-paxos中的步骤吗？我理解领导者直接进入第二阶段赋值，是否正确？
图2中接受者已经赋值，后来领导者C执行Basic Paxos中准备阶段，将其修改。不是一旦赋值后就不能修改了吗？</div>2020-10-31</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/47/00/3202bdf0.jpg" width="30px"><span>piboye</span> 👍（2） 💬（1）<div>multipaxos假设就是不相关的吧，相关的数据，应该用paxos来决议log，这样就一致了。fast paxos也可以一次rpc一个提交，不过效率应该不如raft流模式。 zab比raft和paxos没有优势了吧？</div>2020-09-17</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/2UXuSevhia94o9Eky4OfMuSictaldxcqpjGuvRCOcvjIIoVBAENLEZbv2lgwmwC8icK1ZrUcneNtiaeFBV8MT3uzNg/132" width="30px"><span>Gavin</span> 👍（2） 💬（1）<div>在创建完提案之后，主节点会基于 TCP 协议，并按照顺序将提案广播到其他节点。这样就能保证先发送的消息，会先被收到，保证了消息接收的顺序性。

请问下，tcp协议有可能先发的消息后收到吧？</div>2020-08-07</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/ea/8b/613c162e.jpg" width="30px"><span>nomoshen</span> 👍（2） 💬（2）<div>第一个阶段提议ok之后，第二个committed阶段主节点挂了，那么在选举的时候这写未提交的提议咋处理？主节点反馈给客户端是否要直到comitted绝大多数才算OK</div>2020-06-04</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/4d/49/28e73b9c.jpg" width="30px"><span>明翼</span> 👍（0） 💬（2）<div>我看很多朋友回复是通过tcp来控制顺序，我不认为这样，tcp发送如果中间过程路由发生了变化，仍然会导致后发的消息先到；udp当然更不行了。。后来我看一篇文章说leader为每个flow生成一个先进先出的队列，如果flow去主动取数据的话这个顺序是可以保障的</div>2020-09-25</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/47/00/3202bdf0.jpg" width="30px"><span>piboye</span> 👍（0） 💬（1）<div>这里还是有误解？paxos是为了决议一个不变值，不变的值可以是log item吧？paxos有问题的地方是可能把原先没有成功的值也决议进去了，但如果这个值是个幂等也没关系吧，客户端看到的失败，不代表服务端就一定没写成功，所以只要是一致的日志，跟raft也一样了吧？</div>2020-09-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/47/00/3202bdf0.jpg" width="30px"><span>piboye</span> 👍（0） 💬（1）<div>multi-paxos中没有形成多数派的值y，为什么要被c选定呢？c应该忽略不是多数派的y吧。还有x和y的顺序性，完全可以在客户端解决啊，等x成功后再提新y啊。</div>2020-05-02</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/13/35/45391914.jpg" width="30px"><span>冷笑的花猫</span> 👍（0） 💬（2）<div>请教老师一个问题。zk用啥标准剔除follower？比如因网络抖动，zk一段时间内发送给follower的事务信息都是失败。</div>2020-04-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1c/48/c6/3c8d9a0c.jpg" width="30px"><span>爱德华</span> 👍（11） 💬（1）<div>老韩，课讲的很好，我有不懂的地方，想请教下。

zab是如何保证proposal提交的顺序型的？单纯的用zxid保证提交到FIFO队列依次广播是实现不了proposal提交的顺序性的。

zxid只能保证提交到队列顺序性，以及消息广播的顺序性。但是保证不了网络中消息先后到达follower的顺序，这是第一个问题。第二个问题就是，就算按照zxid的顺序依次到达了follower，但是follower处理每个proposal的时间是不一致的，也就是说后到达的proposal有可能先处理完，先给leader返回ack响应。这里除非zab处理是单线程的，才不会有这个问题。

我觉得zab中应该针对zxid做了特殊判断。
比如真正去提交的时候（第二阶段），先判断在此zxid之前proposal有没有提交，有的话等上一个提交了再提交。
或者另一个想法，当发现当前的需要提交的zxid之前的还有proposal没有提交，则拒绝提交，进去崩溃恢复模式。但是这样的话，leader很容易失去过半的follower。

不知道zab是怎么做的呢？</div>2020-08-17</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/DYAIOgq83epRK5v3IkvSfjicKNKlRLE2nTQUowhMvQkwWWWUSESat8EBbcPvMk4aAjZHGcsE5DCibES9WicHcC9Qw/132" width="30px"><span>充值一万</span> 👍（10） 💬（2）<div>这一节看得我一脸懵逼。。按照文中描述，Multi-Paxos 无法保证操作顺序性的原因是各节点可能先后宕机，然后最终恢复时，最终达成一致的提案可能不是预期的（X, Y 变成 Z, Y）。而ZAB 协议能保证顺序，是因为提案提交有序，TCP保证可靠通讯。
？？？？？？？？？？？？？？？？？？？？？？？？
Multi-Paxos领导节点也可以顺序提案啊，也可以用TCP；
ZAB 协议的节点也可能各种宕机啊？！</div>2021-04-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/ad/da/31a2eb50.jpg" width="30px"><span>andrewguo</span> 👍（5） 💬（1）<div>使用tcp协议来保证顺序的原因是
1. tcp协议栈能保证包的先后顺序
2. 虽然提案本身有递增的逻辑时钟，但zab里zxid要求不是严格连续，允许空洞。如果传输协议不能保证顺序，从节点获取提案N时无法判断是否还有比N小的提案未收到，从而无法执行。</div>2020-06-06</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/12/c7/a7a5df8b.jpg" width="30px"><span>达子不一般</span> 👍（4） 💬（2）<div>对文中举出的Multi Basic Paxos的实例的几个疑问：

- 针对不同的key(X)、key(Z)，为何要使用相同的编号101？不同的key之间使用共识判断，有意义吗？

- 因为网络故障，指令只成功复制到了节点A

指令只成功复制到了节点A，那么返回给客户端是成功还是失败？如果是失败，那么被占据多数101的Z覆盖似乎也没啥问题

- A恢复后，102对应的Y涉及的节点不占有多数，为啥学习者C会学到102呢</div>2021-10-05</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/11/2e/ebb53d59.jpg" width="30px"><span>熙成</span> 👍（2） 💬（0）<div>为什么 Multi-Paxos 无法保证操作顺序性？
讲述疑惑：
提案编号既然是1，那序号101、102是表示什么？是提案内容吗？不应该看提案编号递增+1吗，为什么又搞出来个序号？</div>2021-09-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/19/d9/ff/b23018a6.jpg" width="30px"><span>Heaven</span> 👍（2） 💬（0）<div>1.首先消息的前后性不能保证,因为TCP本质上是在接收和发送的两端都维护了一个栈的机制,模拟出了一条数据流,从而做到了顺序的传输,而UDP是无序的,可以在网上到处开车,可能导致消息前后错乱
2.但是消息的前后性我感觉可以从别的地方保证,可以从几点来分析下,对于失败重传,这个可以由发收双方进行手段性质的保证
而且在主节点不故障的情况下,是可以知道发送的消息,那么X不会的时候,Y也不会先提交
而且对于跟随者,只收到了Y的提交,估计也要等X的提交消息才能生效吧,不然即使是两个消息有依赖性,但是两个消息也不一定在一个TCP里面提交啊
最后,即使故障了,任期编号自然会更新,不会出现编号错乱的问题</div>2020-08-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/ae/8b/43ce01ca.jpg" width="30px"><span>ezekiel</span> 👍（1） 💬（0）<div>老师您好！

你可以看到，原本预期的指令是 X、Y，最后变成了 Z、Y。讲到这儿，你应该可以知道，为什么用 Multi-Paxos 不能达到我们想要的结果了吧？
========================================
x、y并没有复制到大多数节点，在客户端角度来说应该是失败的。从服务端角度来说，C当选后为什么会接受A节点的y值呢？没有达成共识呀</div>2021-10-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/67/df/8b85d0d9.jpg" width="30px"><span>--</span> 👍（1） 💬（0）<div>能否使用UDP得看zxid是不是连续递增的，本质上来说每个节点提案的偏序关系是一样的就能保证顺序。但是主节点故障之后，新主需要能够判断当前要提交的提案是不是第一个未提交的提案，即提案是否存在空洞。如果zxid是连续的，通过对比最后一个已提交的提案的zxid就能判断出是否有空洞，如果不是连续的，那么就无法判断了。</div>2021-05-10</li><br/><li><img src="" width="30px"><span>zyz</span> 👍（1） 💬（0）<div>老师！“Zookeeper 提供的是最终一致性，也就是读操作可以在任何节点上执行，客户端会读到旧数据”，这句话是不是这样理解，根据zk的单一视图保证客户端不会连接到数据版本比自己之前看到的旧的服务器上。
如果这个客户端，指的是当前刚刚发起操作修改数据的客户端，断开连上还没有更新到最新事务的非领导者节点，非领导者节点会拒绝当前连接，因为客户端zxid事务Id，大于当前节点事务Id lastProcessedZxid，因此客户端需要连接其他节点。
如果这个客户端，指的是新客户端，不是刚才操作的客户端，连接上非领导者节点，看的的数据可能不是最新的。</div>2021-02-06</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/cd/db/7467ad23.jpg" width="30px"><span>Bachue Zhou</span> 👍（1） 💬（0）<div>采用 udp 协议也可以保证消息的顺序性啊，只需要在上层再加一个保证消息顺序性的协议即可，比如 quic</div>2021-01-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1b/65/b7/058276dc.jpg" width="30px"><span>i_chase</span> 👍（0） 💬（0）<div>这里Multi paxos顺序性讲的是真的看不明白。。感觉保证顺序性的唯一办法就是让每个zxid提案顺序执行？</div>2022-11-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/21/03/c5/600fd645.jpg" width="30px"><span>tianbingJ</span> 👍（0） 💬（0）<div>不应该强调TCP协议啊，完全没有必要；像Raft那样有index也行啊，比如&lt;1,1&gt; &lt;1,2&gt;这样的序列，&lt;1,2&gt;先到也没关系，&lt;1,1&gt;不到不commit、不apply状态机就是了。
即使节点之间有连接也不一定是就一个TCP连接...

感觉不是一个层面的事情</div>2022-03-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/21/63/6e/6b971571.jpg" width="30px"><span>Z宇锤锤</span> 👍（0） 💬（0）<div>不可以。因为UDP不可以保证数据顺序。</div>2022-01-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/83/22/c3dae274.jpg" width="30px"><span>阿kai(aeo</span> 👍（0） 💬（0）<div>&quot;当主节点接收到指定提案的“大多数”的确认响应后，该提案将处于提交状态（Committed），主节点会通知备份节点提交该提案。&quot;
我有一个疑问，备份节点各自Commit提案以后 还会告诉主节点吗？
</div>2022-01-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/22/f4/9fd6f8f0.jpg" width="30px"><span>核桃</span> 👍（0） 💬（0）<div>其实结合工程实现来看,不管是基于Raft还是Paxos的实现,其实已经非常类似了,也就是在读写级别,是否从节点可写等方面有一些取舍罢了,但是本质思想是相同的.</div>2022-01-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/12/c7/a7a5df8b.jpg" width="30px"><span>达子不一般</span> 👍（0） 💬（0）<div>如果 ZAB 采用的是 UDP 协议，能保证消息接收的顺序性吗？

UDP不能保证消息接收的顺序性，但一定要保证消息接收的顺序性吗？是否只要保证leader上commit的顺序性即可</div>2021-10-05</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1a/a4/0c/be3ac2ca.jpg" width="30px"><span>乘修</span> 👍（0） 💬（0）<div>如果说x没有被选定，那么y也没有被选定啊，不可能出现后续z代替x，将结果从[x,y]变成[z,y]吧？</div>2021-08-30</li><br/>
</ul>