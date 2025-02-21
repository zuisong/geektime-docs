你好，我是唐聪。

在软件开发过程中，当我们需要解决配置、服务发现、分布式锁等业务痛点，在面对[etcd](https://github.com/etcd-io/etcd)、[ZooKeeper](https://github.com/apache/zookeeper)、[Consul](https://github.com/hashicorp/consul)、[Nacos](https://github.com/alibaba/nacos)等一系列候选开源项目时，我们应该如何结合自己的业务场景，选择合适的分布式协调服务呢？

今天，我就和你聊聊主要分布式协调服务的对比。我将从基本架构、共识算法、数据模型、重点特性、容灾能力等维度出发，带你了解主要分布式协调服务的基本原理和彼此之间的差异性。

希望通过这节课，让你对etcd、ZooKeeper、Consul原理和特性有一定的理解，帮助你选型适合业务场景的配置系统、服务发现组件。

## 基本架构及原理

在详细和你介绍对比etcd、ZooKeeper、Consul特性之前，我们先从整体架构上来了解一下各开源项目的核心架构及原理。

### etcd架构及原理

首先是etcd，etcd我们知道它是基于复制状态机实现的分布式协调服务。如下图所示，由Raft共识模块、日志模块、基于boltdb持久化存储的状态机组成。

![](https://static001.geekbang.org/resource/image/5c/4f/5c7a3079032f90120a6b309ee401fc4f.png?wh=605%2A319)

以下是etcd基于复制状态机模型的写请求流程：

- client发起一个写请求（put x = 3）；
- etcdserver模块向Raft共识模块提交请求，共识模块生成一个写提案日志条目。若server是Leader，则把日志条目广播给其他节点，并持久化日志条目到WAL中；
- 当一半以上节点持久化日志条目后，Leader的共识模块将此日志条目标记为已提交（committed），并通知其他节点提交；
- etcdserver模块从Raft共识模块获取已经提交的日志条目，异步应用到boltdb状态机存储中，然后返回给client。
<div><strong>精选留言（8）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/11/18/ac/4d68ba46.jpg" width="30px"><span>金时</span> 👍（2） 💬（1）<div>线性读和强一致读有什么区别？</div>2021-09-01</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/b2/e0/bf56878a.jpg" width="30px"><span>kkxue</span> 👍（10） 💬（0）<div>我觉得pingcap的这个方案可行：
https:&#47;&#47;github.com&#47;etcd-io&#47;etcd&#47;issues&#47;11357
https:&#47;&#47;pingcap.com&#47;blog-cn&#47;geographic-data-distribution-traffic-and-latency-halved&#47;
&quot;这里我们引入了一个新概念 Group，每一个 Raft 节点都有一个对应的 Group ID，拥有相同 Group ID 的节点即在同一个数据中心中。既然有了每个 Raft 节点的 Group 信息，Leader 就可以在广播消息时在每一个 Group 中选择一个代理人节点（我们称为 Follower  Delegate），将整个 Group 成员所需要的信息发给这个代理人，代理人负责将数据同步给 Group 内的其他成员&quot;</div>2021-03-15</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/66/2e/527b73c9.jpg" width="30px"><span>骑着🚀看银河</span> 👍（5） 💬（1）<div>按照这个比较ETCD并没有胜出啊，反而Consul是最佳选择，哈哈哈
</div>2022-03-17</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/q2HwchogzNiavKhIB4GfAxH6B88NhSoC7B7keVEUqiaP6JPokDUNJLYehocOyqYqrhA3iaxywyRXLYkYJjDUQESZw/132" width="30px"><span>残天噬魂</span> 👍（3） 💬（0）<div>额，老师这么一比较，我感觉除了语言契合度之外，consul就应该是第一选择啊，哈哈</div>2021-12-31</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/b2/e0/bf56878a.jpg" width="30px"><span>kkxue</span> 👍（2） 💬（2）<div>还有这个方案就是直接将不同数据中心的延时降低！如同local datacenter,传闻google做到了</div>2021-03-15</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/e9/91/4219d305.jpg" width="30px"><span>初学者</span> 👍（1） 💬（0）<div>关于同城双az高可用，有一些问题想和老师探讨一下: 
如果我想采用2+2部署方案，也就一个集群4个节点平均部署到两个机房，这样的好处是一个az跪了，能保证另一个az肯定有节点上的数据是完整的，坏处是任何一个az挂了，服务就立即不可用，要有一个手动恢复的流程，我这里想请教一下老师，当前etcd只发现一种通过force-new-cluster的参数也通过某一个节点的数据恢复集群，有什么优雅的方式知道正常的az中两个节点中哪个节点数据最新？
像zk这种，我完全可以在正常az中新扩容一个新节点，修改集群member配置信息，然后在正常的az中恢复出一个3节点的集群，而且也只能新扩容的节点需要复制集群数据，etcd好像不支持这种玩法。
</div>2021-12-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1a/1f/17/f2a69e62.jpg" width="30px"><span>Fis.</span> 👍（0） 💬（0）<div>3AZ的或者3地域的直接跨区域部署就行了，就是时延需要考虑及优化，双AZ的比较复杂。
方案1：etcd集群2+1部署，引入全局仲裁服务，自己做一个agent，根据仲裁服务的信息，管理etcd节点升主或降备，破坏了原有raft协议
方案2：两个etcd集群，开发专门的数据同步工具或者开源make mirror，主备集群模式。两个集群revision无法一致
方案3：区域1主集群，区域2部署3个learner，故障时区域2升主。
上面几种方案那种更好呢？还有其他好的方案吗？</div>2021-12-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/46/0f/f6cfc659.jpg" width="30px"><span>mckee</span> 👍（0） 💬（0）<div>etcd一般可以采用同一个region下跨可用区部署，最好每个可用区部署一台</div>2021-11-17</li><br/>
</ul>