你好，我是蒋德钧。

在上节课，我们了解了哨兵实例的初始化过程。哨兵实例一旦运行后，会周期性地检查它所监测的主节点的运行状态。当发现主节点出现客观下线时，哨兵实例就要开始执行故障切换流程了。

不过，我们在部署哨兵实例时，通常会部署多个哨兵来进行共同决策，这样就避免了单个哨兵对主节点状态的误判。但是这同时也给我们带来了一个问题，即**当有多个哨兵判断出主节点故障后，究竟由谁来执行故障切换？**

实际上，这就和**哨兵Leader选举**有关了。而哨兵Leader选举，又涉及到分布式系统中经典的共识协议：Raft协议。学习和掌握Raft协议的实现，对于我们在分布式系统开发中实现分布式共识有着非常重要的指导作用。

所以接下来的两节课，我会带你了解Raft协议以及Redis源码中，基于Raft协议实现Leader选举的具体设计思路。今天我们先来学习下Raft协议的基本流程、它和哨兵Leader选举的关系，以及哨兵工作的整体执行流程，这部分内容也是我们学习哨兵Leader选举的必备知识。

## 哨兵Leader选举和Raft协议

当哨兵发现主节点有故障时，它们就会选举一个Leader出来，由这个Leader负责执行具体的故障切换流程。但因为哨兵本身会有多个实例，所以，在选举Leader的过程中，就需要按照一定的协议，让多个哨兵就“Leader是哪个实例”达成一致的意见，这也就是**分布式共识**。
<div><strong>精选留言（5）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/0f/90/8a/288f9f94.jpg" width="30px"><span>Kaito</span> 👍（35） 💬（3）<div>1、Redis 为了实现故障自动切换，引入了一个外部「观察者」检测实例的状态，这个观察者就是「哨兵」

2、但一个哨兵检测实例，有可能因为网络原因导致「误判」，所以需要「多个」哨兵共同判定

3、多个哨兵共同判定出实例故障后（主观下线、客观下线），会进入故障切换流程，切换时需要「选举」出一个哨兵「领导者」进行操作

4、这个选举的过程，就是「分布式共识」，即多个哨兵通过「投票」选举出一个都认可的实例当领导者，由这个领导者发起切换，这个选举使用的算法是 Raft 算法

5、严格来说，Raft 算法的核心流程是这样的：

1) 集群正常情况下，Leader 会持续给 Follower 发心跳消息，维护 Leader 地位
2) 如果 Follower 一段时间内收不到 Leader 心跳消息，则变为 Candidate 发起选举
3) Candidate 先给自己投一票，然后向其它节点发送投票请求
4) Candidate 收到超过半数确认票，则提升为新的 Leader，新 Leader 给其它 Follower 发心跳消息，维护新的 Leader 地位
5) Candidate 投票期间，收到了 Leader 心跳消息，则自动变为 Follower
6) 投票结束后，没有超过半数确认票的实例，选举失败，会再次发起选举

6、但哨兵的选举没有按照严格按照 Raft 实现，因为多个哨兵之间是「对等」关系，没有 Leader 和 Follower 角色，只有当 Redis 实例发生故障时，哨兵才选举领导者进行切换，选举 Leader 的过程是按照 Raft 算法步骤 3-6 实现的

课后题：哨兵实例执行的周期性函数 sentinelTimer 的最后，修改 server.hz 的目的是什么？

server.hz 表示执行定时任务函数 serverCron 的频率，哨兵在最后修改 server.hz 增加一个随机值，是为了避免多个哨兵以「相同频率」执行，引发每个哨兵同时发起选举，进而导致没有一个哨兵能拿到多数投票，领导者选举失败的问题。适当打散执行频率，可以有效降低选举失败的概率。</div>2021-09-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/25/7f/473d5a77.jpg" width="30px"><span>曾轼麟</span> 👍（5） 💬（0）<div>首先回答老师的问题：调整 server.hz 的目的是什么？
答：为了使每个哨兵与其他哨兵不同步，通过这种方式避免由于几个哨兵同时启动，导致无法投出leader的情况，类似脑裂，因为每个独立的哨兵都在启动同一时刻开始发起投票，然后一轮一轮下去都没法投出leader。

总结：
本篇文章老师主要介绍了，redis在Raft协议上的实现，Redis本身不是完全按照Raft协议实现的，其中最主要的原因就是每个哨兵节点都是对等的，而Raft协议逻辑主要如下：
        1、在稳定系统中只有 Leader 和 Follower 两种节点，并且 Leader 会向 Follower 发送心跳消息。
        2、如果某个Follower 在一定时间没收到Leader的心跳，那么他会变成Candidate 并且可以发起选举。
        3、Candidate 会先投自己一票，然后等待其他follower的投票。
        4、如果投票结果能选出Leader则新的Leader上位，否则再进行一轮选举。

而Redis是哨兵是对等的，所以每个哨兵都会监听当前Redis的Leader的心跳，当前Redis的Leader如果发生异常，哨兵会开始发起选举直到第一个Leader被选举出来并通知每个哨兵。

TILT模式：
由于哨兵模式是对等的，那么必然会出现一情况导致哨兵节点不可信任，比如：当前系统时间被修改，当前哨兵节点硬件资源繁忙，当前网络稳定状态差等等。当这些情况发生的时候哨兵就有可能进入TILT模式，在这种模式下哨兵是正常运行工作，但是它的投票是不被信任的。

拓展：
其实本篇文章主要的核心就是分布式共识问题，针对分布式共识有一个很经典的问题就是【拜占庭将军问题】 ，而大多数分布式共识最终目的都是处理这个问题的场景，由此衍生出了各种共识算法如：Raft算法，Paxos算法，ZAB算法，PBFT算法等等。

而ZAB算法就是Zookeeper核心指导算法，ZAB与Raft不同的是，ZAB是通过竞争手里资源，比如leader底下有几个ack，最多ack的那个竞选成功，所以相比Raft可以改造为平等模型的互相投票再出leader，ZAB中leader的概念稍微重要一点（我个人理解ZAB应该比较容易脑裂，不知道理解是否到位）。</div>2021-09-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/17/8b/4b/15ab499a.jpg" width="30px"><span>风轻扬</span> 👍（0） 💬（0）<div>回答一下老师的思考题。
redis的源码中，关于这一段有注释server.hz = CONFIG_DEFAULT_HZ + rand() % CONFIG_DEFAULT_HZ;
是为了让哨兵实例错开执行，以避免出现选主失败的情况。因为redis选主用的是RAFT协议，如果哨兵同时发起投票，得到相同票数的几率要高。</div>2023-12-05</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/28/74/e0/6be55bc4.jpg" width="30px"><span>Petrichor</span> 👍（0） 💬（1）<div>&quot;Redis 哨兵实例在正常运行的过程中，不同实例间并不是 Leader 和 Follower 的关系，而是对等的关系&quot;
在主备模式应该必须有一个leader吧，在去中心化的redis切片集群确实没有 Leader 和 Follower区分</div>2023-10-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1d/6c/b5/32374f93.jpg" width="30px"><span>可怜大灰狼</span> 👍（0） 💬（0）<div>回答问题：为了防止哨兵们总是按照一个频率来竞选leader，从而导致重复多轮选举</div>2021-09-26</li><br/>
</ul>