你好，我是蒋德钧。

从这节课开始，我们又将进入一个新的模块：“Redis Cluster”模块。在这个模块中，我会带你了解Redis Cluster的关键功能实现，包括了Gossip协议通信、集群关键命令和数据迁移等机制的设计与实现。

通过这些课程的学习，一方面，你可以深入了解Redis是如何完成集群关系维护、请求转发和数据迁移的。当你遇到集群问题时，这些知识可以帮助你排查问题。另一方面，当你在开发分布式集群时，不可避免地会遇到节点信息维护、数据放置和迁移等设计问题，接下来的几节课可以让你掌握Gossip协议、数据迁移等分布式集群中关键机制的典型设计和实现，而这些实现方法对于你开发分布式集群是很有帮助的。

那么接下来，我就先带你来学习Redis Cluster中节点的通信机制，而这个通信机制的关键是Gossip协议。所以今天这节课，我们主要来了解下Gossip协议在Redis中是如何实现的。

## Gossip协议的基本工作机制

对于一个分布式集群来说，它的良好运行离不开集群节点信息和节点状态的正常维护。为了实现这一目标，通常我们可以选择**中心化**的方法，使用一个第三方系统，比如Zookeeper或etcd，来维护集群节点的信息、状态等。同时，我们也可以选择**去中心化**的方法，让每个节点都维护彼此的信息、状态，并且使用集群通信协议Gossip在节点间传播更新的信息，从而实现每个节点都能拥有一致的信息。
<div><strong>精选留言（6）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/0f/90/8a/288f9f94.jpg" width="30px"><span>Kaito</span> 👍（24） 💬（2）<div>1、多个节点组成一个分布式系统，它们之间需要交换数据，可以采用中心化的方式（依赖第三方系统，例如ZK），也可以采用非中心化（分布式协议，例如 Gossip）的方式

2、Redis Cluster 采用非中心化的方式 Gossip 协议，实现多个节点之间信息交换

3、集群中的每个实例，会按照固定频率，从集群中「随机」挑选部分实例，发送 PING 消息（自身实例状态、已知部分实例信息、slots 分布），用来交换彼此状态信息

4、收到 PING 的实例，会响应 PONG 消息，PONG 消息和 PING 消息格式一样，包含了自身实例状态、已知部分实例信息、slots 分布

5、这样经过几次交换后，集群中每个实例都能拿到其它实例的状态信息

6、即使有节点状态发生变化（新实例加入、节点故障、数据迁移），也可以通过 Gossip 协议的 PING-PONG 消息完成整个集群状态在每个实例上的同步

课后题：为什么 clusterSendPing 函数计算 wanted 值时，是用的集群节点个数的十分之一？

这个和 Redis Cluster 判定实例「故障」逻辑有关了。

Redis Cluster 实例在周期性向其它实例交换信息时，会先随机选出 5 个实例，然后从中找出最久没通信过的实例，发送 PING 消息。

但这里有个问题，随机选出的这 5 个实例，有可能并不是整个「集群」中最久没通信过的，为了避免拿不到这些实例的状态，导致集群误以为这些实例已过期，所以制定了一个策略：如果和实例最近通信时间超过了 cluster-node-timeout &#47; 2，那会立即向这个实例发送 PING 消息。

每次 PING 都会收到 PONG 响应，一来一回 2 次心跳包，来回都带有部分实例的状态信息，那在 cluster-node-timeout 时间内会收到 4 次心跳包。

又因为 Redis Cluster 计算故障转移超时时间是 cluster-node-timeout * 2，那这段时间内就能收到 8 个 PING + PONG 心跳包，每个心跳包中实例个数设置为集群的 1&#47;10，那在故障转移期间就能收到集群 80%（8 * 1&#47;10）节点发来的故障状态信息了，满足集群大部分节点发来的节点故障情况。</div>2021-10-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/59/12/49458cb3.jpg" width="30px"><span>🙄</span> 👍（2） 💬（0）<div>关于PING消息 用的集群节点个数的十分之一作为wanted值如课代表所说，但是在我阅读源码的时候发现，PING消息是先把wanted数量的实例放到消息体，然后再把所有当前nodes认为是PFAIL的实例放到消息体末尾，也就是说，新版的redis实例加速了 PFAIL-&gt;FAIL的判断，跟十分之一的关系已经不大了。

PS: 当时看这段代码的时候非常疑惑，看源码的注释也很疑惑...直到翻阅github上面的提交记录

https:&#47;&#47;github.com&#47;redis&#47;redis&#47;commit&#47;1e659a04cf19e4349c8dbba931d1606336970b8c#diff-55c2de0fa49d05f6ed8f0c13cacedc85fba5d5739c8360567743f9f740df3179


&#47;* If there are PFAIL nodes, add them at the end. *&#47;
    if (pfail_wanted) {
        dictIterator *di;
        dictEntry *de;

        di = dictGetSafeIterator(server.cluster-&gt;nodes);
        while((de = dictNext(di)) != NULL &amp;&amp; pfail_wanted &gt; 0) {
            clusterNode *node = dictGetVal(de);
            if (node-&gt;flags &amp; CLUSTER_NODE_HANDSHAKE) continue;
            if (node-&gt;flags &amp; CLUSTER_NODE_NOADDR) continue;
            if (!(node-&gt;flags &amp; CLUSTER_NODE_PFAIL)) continue;
            clusterSetGossipEntry(hdr,gossipcount,node);
            freshnodes--;
            gossipcount++;
            &#47;* We take the count of the slots we allocated, since the
             * PFAIL stats may not match perfectly with the current number
             * of PFAIL nodes. *&#47;
            pfail_wanted--;
        }
        dictReleaseIterator(di);
    }</div>2021-10-15</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/ec/13/49e98289.jpg" width="30px"><span>neohope</span> 👍（1） 💬（0）<div>为何选择了1&#47;10的节点，在源码注释里其实就有，分两部分解释一下：

一、在clusterCron函数中，有一个强制PING策略：
如果节点A和节点B最后通信时间超过了 cluster-node-timeout&#47;2，节点A会立即向节点B发送 PING 消息。所以，在在cluster-node-timeout时间内，节点A和节点B最少也会收发2来2回共4次心跳包。
Redis Cluster计算故障转移确认时间是cluster-node-timeout*2，那这段时间内节点A和节点B最少会收发4来4回共8个心跳包。

二、在一个100个全master节点的集群中，有一个正常节点A，一个被A判断为PFAIL节点C，在没有pfail_wanted的时候：
对于节点A，在cluster-node-timeout*2的故障转移确认时间内，最少也可以与他节点交换关于C节点到这么多个包：
PROB * GOSSIP_ENTRIES_PER_PACKET * TOTAL_PACKETS
(节点C被包含在一个entry中的几率，100选1，也就是1%)*(一个GOSSIP包中的entry数量，10分之1，100个节点网络中是10)*（其他节点与A交换的最小总包数，节点数*8）
1%*10*(100*8)=80
由于这些包都是随机选择entry的，节点A收发的这80个包含C节点信息的包，也就是与A交换过C节点信息的节点也差不多为80个，大概率覆盖了100个节点的多数节点，也就可以确实证明了C点有问题了。

为何不再高一些：现在这个比例已经够高了，如果再高一些，只会增加网络负担而已。而且，收发8个包已经是最差情况了，平时比8个包还会多一些。 
同时，在4.x的源码中，已经补充了pfail_wanted的代码，会让PFAIL节点更快的传播。

为何不再低一些：在正常的redis cluster集群中，有一些slave节点，不会参与投票，所以保持了这样一个比例。

此外，这里就是个估算，别纠结为何用100不用99或98什么的，不影响结论。也不用纠结这80个包，如果收发全部重叠，不就只有40个节点交换信息吗，估算时不要考虑小概率时间。</div>2022-03-25</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/29/39/be9d2e88.jpg" width="30px"><span>边际革命</span> 👍（0） 💬（0）<div>主从如何做故障切换的 不讲一下吗？</div>2022-04-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/d6/e8/50b58ed8.jpg" width="30px"><span>OAuth</span> 👍（0） 💬（0）<div>这个达到最终一致性是Gossip中的谣言传播吗</div>2022-02-16</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/4f/55/0a5fd84a.jpg" width="30px"><span>李艳伟</span> 👍（0） 💬（0）<div>老师我想问一下，我遇到一个问题，就是一个正常集群由于节点故障产生了一条fail信息，没有及时清理，这个ip又被别的集群使用了，请问这个是ping pong信息交换的，还是meet呢</div>2021-12-18</li><br/>
</ul>