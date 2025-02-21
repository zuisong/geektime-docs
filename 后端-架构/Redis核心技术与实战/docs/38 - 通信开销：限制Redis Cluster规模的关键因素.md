你好，我是蒋德钧。

Redis Cluster能保存的数据量以及支撑的吞吐量，跟集群的实例规模密切相关。Redis官方给出了Redis Cluster的规模上限，就是一个集群运行1000个实例。

那么，你可能会问，为什么要限定集群规模呢？其实，这里的一个关键因素就是，**实例间的通信开销会随着实例规模增加而增大**，在集群超过一定规模时（比如800节点），集群吞吐量反而会下降。所以，集群的实际规模会受到限制。

今天这节课，我们就来聊聊，集群实例间的通信开销是如何影响Redis Cluster规模的，以及如何降低实例间的通信开销。掌握了今天的内容，你就可以通过合理的配置来扩大Redis Cluster的规模，同时保持高吞吐量。

## 实例通信方法和对集群规模的影响

Redis Cluster在运行时，每个实例上都会保存Slot和实例的对应关系（也就是Slot映射表），以及自身的状态信息。

为了让集群中的每个实例都知道其它所有实例的状态信息，实例之间会按照一定的规则进行通信。这个规则就是Gossip协议。

Gossip协议的工作原理可以概括成两点。

一是，每个实例之间会按照一定的频率，从集群中随机挑选一些实例，把PING消息发送给挑选出来的实例，用来检测这些实例是否在线，并交换彼此的状态信息。PING消息中封装了发送消息的实例自身的状态信息、部分其它实例的状态信息，以及Slot映射表。
<div><strong>精选留言（26）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/12/0a/a4/828a431f.jpg" width="30px"><span>张申傲</span> 👍（54） 💬（5）<div>看到 Gossip 协议，第一时间想到了《人类简史》中说的：八卦是人类进步的动力，但是集群超过一定规模时，八卦的作用就十分有限了。</div>2020-12-22</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTI2icbib62icXtibTkThtyRksbuJLoTLMts7zook2S30MiaBtbz0f5JskwYicwqXkhpYfvCpuYkcvPTibEaQ/132" width="30px"><span>xuanyuan</span> 👍（17） 💬（1）<div>可以划分管理面和数据面，集群通信走单独的网络</div>2020-12-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/90/8a/288f9f94.jpg" width="30px"><span>Kaito</span> 👍（157） 💬（11）<div>如果采用类似 Codis 保存 Slot 信息的方法，把集群实例状态信息和 Slot 分配信息保存在第三方的存储系统上（例如Zookeeper），这种方法会对集群规模产生什么影响？

由于 Redis Cluster 每个实例需要保存集群完整的路由信息，所以每增加一个实例，都需要多一次与其他实例的通信开销，如果有 N 个实例，集群就要存储 N 份完整的路由信息。而如果像 Codis 那样，把 Slot 信息存储在第三方存储上，那么无论集群实例有多少，这些信息在第三方存储上只会存储一份，也就是说，集群内的通信开销，不会随着实例的增加而增长。当集群需要用到这些信息时，直接从第三方存储上获取即可。

Redis Cluster 把所有功能都集成在了 Redis 实例上，包括路由表的交换、实例健康检查、故障自动切换等等，这么做的好处是，部署和使用非常简单，只需要部署实例，然后让多个实例组成切片集群即可提供服务。但缺点也很明显，每个实例负责的工作比较重，如果看源码实现，也不太容易理解，而且如果其中一个功能出现 bug，只能升级整个 Redis Server 来解决。

而 Codis 把这些功能拆分成多个组件，每个组件负责的工作都非常纯粹，codis-proxy 负责转发请求，codis-dashboard 负责路由表的分发、数据迁移控制，codis-server 负责数据存储和数据迁移，哨兵负责故障自动切换，codis-fe 负责提供友好的运维界面，每个组件都可以单独升级，这些组件相互配合，完成整个集群的对外服务。但其缺点是组件比较多，部署和维护比较复杂。

在实际的业务场景下，我觉得应该尽量避免非常大的分片集群，太大的分片集群一方面存在通信开销大的问题，另一方面也会导致集群变得越来越难以维护。而且当集群出问题时，对业务的影响也比较集中。建议针对不同的业务线、业务模块，单独部署不同的分片集群，这样方便运维和管理的同时，出现问题也只会影响某一个业务模块。</div>2020-11-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/7f/91/962eba1a.jpg" width="30px"><span>唐朝首都</span> 👍（6） 💬（0）<div>集群的规模应该是可以进一步扩大的。因为集群的信息保存在了第三方存储系统上，意味着redis cluster内部不用再沟通了，这将节省下大量的集群内部的沟通成本。当然就整个集群而言部署、维护也会更加复杂，毕竟引入了一个第三方组件来管理集群。</div>2020-11-25</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/19/bf/415023b5.jpg" width="30px"><span>璩雷</span> 👍（5） 💬（2）<div>约到后面，评论的人越少，看来坚持到最后的人不多啊~~</div>2021-07-30</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/28/6c/bc/f751786b.jpg" width="30px"><span>Ming</span> 👍（2） 💬（0）<div>其实集群不要大，大了通讯是个问题同样后期维护也是个很大的麻烦；不同业务的redis集群区分开来，这样每个集群不至于太大，也不至于一个集群出问题影响到别的业务；</div>2022-04-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/23/5b/983408b9.jpg" width="30px"><span>悟空聊架构</span> 👍（2） 💬（0）<div>Gossip 协议还有很多有意思的东西，可以参照这篇：
病毒传播：全靠 Gossip 协议：
http:&#47;&#47;www.passjava.cn&#47;#&#47;92.%E5%88%86%E5%B8%83%E5%BC%8F&#47;08.Gossip%E5%8D%8F%E8%AE%AE</div>2021-06-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/ec/13/49e98289.jpg" width="30px"><span>neohope</span> 👍（2） 💬（0）<div>用Gossip协议管理配置和Zookeeper统一存储配置信息各有利弊。
Gossip协议在节点间传递配置让系统简单，而且发生网络故障时自行恢复能力更强一些，但通讯效率随着网络节点的增加而降低；
Zookeeper统一管理配置，通讯效率无论节点多少都比较高，但让系统架构更复杂故障点增多，对抗网络故障时自行恢复能力差一些。
但其实无论哪种方式，节点太多了都会更加难以管理维护，出现问题影响面也更难以控制，不推荐。
但其实另一个极端，就是单个实例性能特别高，存储特别多数据也不推荐，同样也是更容易出问题，出现问题影响面太大，不推荐。</div>2021-02-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/92/6d/becd841a.jpg" width="30px"><span>escray</span> 👍（1） 💬（0）<div>今天这个话题应该有点类似屠龙之技，菜鸟如我，什么时候才能有机会运维 100 个以上实例的 Redis Cluster。

Gossip 协议还挺有意思，名字也比较形象。如果翻译成中文，是叫“八卦协议”么？好像容易引起误解。“流言蜚语协议”、“风闻协议”？

一个 ping 消息大概是 104 字节，1000 个实例的 Redis 集群一个 Gossip 消息大概是 12KB，ping-pong 往返，24KB。再加上实例间的通信，那么集群中用于服务正常请求的带宽就会被占用。在这种情况下，是不是采用类似于 Codis 的集中式管理更合适？

将 cluster-node-timeout 从 15 秒调整到 20 或 25 秒，大概能减少 1&#47;3 到 2&#47;3 的实例间通信流量（不知道这个计算是否正确）

PING 消息发送数量 = 1 + 10 * 实例数（最近一次接收 PONG 消息的时间超出 cluster-node-timeout&#47;2）

估计最后还是要靠 tcpdump 来分析实例间的网络带宽变化情况，然后再找出合适的 cluster-node-timeout。但是业务流量经常会有变化，增加了调优的难度。

对于课后题，如果是 Codis 模式，将集群实例状态信息和 Slot 分配信息保存在 Zookeeper 上，那么实例太多之后，查询分配信息的时间也会比较长，另外实时保存实例状态信息也比较难。</div>2021-04-04</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/9a/ab/fd201314.jpg" width="30px"><span>小耿</span> 👍（0） 💬（0）<div>这种方法会将所有实例之间的两两通信，转换成实例和第三方服务器之间的单一通信，能大幅减少通信次数，从而减少集群运行所占用的网络带宽，实现更大规模的集群。</div>2023-10-07</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/17/8b/4b/15ab499a.jpg" width="30px"><span>风轻扬</span> 👍（0） 💬（0）<div>tcpdump命令，执行之后会报错：syntax error，在host和port之间加一个and就可以了。如下：

tcpdump host 192.168.10.3 and port 16379 -i 网卡名 -w &#47;tmp&#47;r1.cap</div>2023-04-06</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/2a/ff/a9d72102.jpg" width="30px"><span>BertGeek</span> 👍（0） 💬（0）<div>请问老师一个问题：
环境：阿里云ack k8s集群，阿里云redis，rds等
问题：应用访问突然报错：nested exception is io.lettuce.core.RedisConnectionException

1. 检查redis 连接ok，健康状态ok
2. 应用监控也正常
3. 最后java 一个服务pod 删除，自动重建，问题消失

针对这个不定时的问题，对于生产环境还是需要排查分析，希望老师给点建议，非常感谢</div>2023-02-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/28/a1/d8/42252c48.jpg" width="30px"><span>123</span> 👍（0） 💬（0）<div>差不多看到最后了，还是坚持快看完了，学习还是需要持之以恒</div>2022-11-30</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/28/ac/37a2a265.jpg" width="30px"><span>弱水穿云天</span> 👍（0） 💬（0）<div>冒个泡，还在坚持。善始者众善终者寡</div>2022-08-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/22/bd/9b/366bb87b.jpg" width="30px"><span>飞龙</span> 👍（0） 💬（1）<div>没搞明白，如果一定数量的redis实例都部署在同一内网网络环境之内，实例之前通过内网相互PING Pong,怎么会占网络通信带宽呢</div>2022-08-17</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTJN6ZnE6ECdJ2aW1WicDVyGwWjQgBWad8WNqHicajKaE4hkmVBJU8vuVEab2MicC4bdknMndjRspo4Hw/132" width="30px"><span>没想法的岁月</span> 👍（0） 💬（0）<div>每个实例在发送一个 Gossip 消息时，除了会传递自身的状态信息，默认还会传递集群十分之一实例的状态信息。---------ping的时候为什么要发送其他实例的信息</div>2022-04-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/47/00/3202bdf0.jpg" width="30px"><span>piboye</span> 👍（0） 💬（1）<div>master 故障的时候， 需要整个集群 master 参与选择 一个 slave 重新成为 master,  如果是 100 节点， 50 个master， 需要 49 个 master 参与这个类似raft 的算法， 效率也太低下了吧？</div>2022-02-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/57/fe/beab006d.jpg" width="30px"><span>Jasper</span> 👍（0） 💬（0）<div>打卡</div>2022-01-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/19/d9/ff/b23018a6.jpg" width="30px"><span>Heaven</span> 👍（0） 💬（0）<div>好处在于,这样减少了每个实例的负担,保证了元信息的一致性
坏处是集群系统中需要额外维护第三方系统,增加了系统复杂度</div>2021-09-06</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1e/01/c5/b48d25da.jpg" width="30px"><span>cake</span> 👍（0） 💬（1）<div>我们也不要把 cluster-node-timeout 调得太大，否则，如果实例真的发生了故障，我们就需要等待 cluster-node-timeout 时长后，才能检测出这个故障，这又会导致实际的故障恢复时间被延长，会影响到集群服务的正常使用。 老师请问下这句话 不是因该是 发生故障 cluster-node-timeout &#47;2 就能检测出故障吗? 因为 pong 超过 cluster-node-timeout &#47;2 就会发送ping，为什么是cluster-node-timeout 之后才能检测出故障呢</div>2021-08-21</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTJ8ic8eLTo5rnqIMJicUfpkVBrOUJAW4fANicKIbHdC54O9SOdwSoeK6o8icibaUbh7ZUXAkGF9zwHqo0Q/132" width="30px"><span>ivhong</span> 👍（0） 💬（2）<div>我一直想问个问题，是每个redis实例配置到一台计算机上？还是每个计算机的物理核上绑定一个redis实例？</div>2021-06-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1b/96/47/93838ff7.jpg" width="30px"><span>青鸟飞鱼</span> 👍（0） 💬（0）<div>老师你好，有个疑惑，选择一个节点Ping，这个节点是主节点还是主从节点都可以？</div>2021-03-31</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/81/e6/6cafed37.jpg" width="30px"><span>旅途</span> 👍（0） 💬（1）<div>找到了 PONG 消息接收超过 cluster-node-timeout&#47;2的节点之后,是其他所有的实例给它发消息?</div>2020-12-15</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/5f/e5/54325854.jpg" width="30px"><span>范闲</span> 👍（0） 💬（0）<div>集群的规模可以进一步扩大。
相当于前面套了一层proxy，proxy从zookeeper获取相关slot信息，然后做请求转发即可？</div>2020-12-03</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1f/3c/10/61efe672.jpg" width="30px"><span>向东是大海</span> 👍（0） 💬（0）<div>请教老师一个问题：Redis 哨兵模式中，默认情况下从实例是否接受读请求？哨兵模式中从实例的规模有没有限制？假设单个实例每秒能支撑 8 万 QPS，使用“一主二从三哨兵”方式部署，“一主二从”能支撑 8 万  QPS * 3 = 24 万 QPS 吗？</div>2020-11-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/ed/eb/88cac7a5.jpg" width="30px"><span>东</span> 👍（0） 💬（1）<div>“PING 消息中封装了发送消息的实例自身的状态信息、部分其它实例的状态信息，以及 Slot 映射表。” 如果两个实例中包含的“其他实例的状态信息” 不一致，实例2如何处理呢？是比较时间戳吗？</div>2020-11-20</li><br/>
</ul>