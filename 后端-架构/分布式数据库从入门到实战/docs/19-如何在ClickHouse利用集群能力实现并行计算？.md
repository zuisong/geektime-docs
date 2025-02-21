你好，我是彭旭。

上节课我们介绍了ClickHouse的MergeTree表引擎系列，但是还只涉及单节点。

这节课我们就来看看，既然ClickHouse是分布式数据库，那么它是如何利用集群多节点、数据分片、数据多副本的能力，来实现并行计算，加速查询的呢？

## 集群概览

HBase、StarRocks一般是配置一个大集群，所有服务器节点，数据都存储在大集群中，像HBase也可以配置多机房多集群，然后集群间配置数据实时复制。

ClickHouse的集群配置则非常灵活，你可以将所有的物理服务器配置成一个大的集群，也可以根据业务、部门等隔离，划分多个小的逻辑集群。每个小集群都可以配置自己的节点、副本、分片，甚至一个节点可以被多个逻辑集群包含。

你也可以每个机房配置成一个逻辑集群，然后配置一个包含了所有机房所有服务器的大的逻辑集群，用来汇总统计所有数据。不过这时候要注意，统计数据就可能涉及多机房之间大量的数据传输了。

举个例子，比如我们南沙与无锡数据中心分属不同的业务，各有3台服务器，平时业务能够在本数据中心机房完成闭环。假设总部需要统计所有的业务数据，这时候你可以分别统计两个数据中心的数据，然后汇总。但是如果数据中心较多，统计内容与查询也较多，这样就会很麻烦。
<div><strong>精选留言（5）</strong></div><ul>
<li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTIKa0PdjFnEpvGFBcED2P28ugPmwwRoCbeUfulpGEye8964F4nwChQyVfgVUia74TyDISvXTYJfQpA/132" width="30px"><span>Nick</span> 👍（0） 💬（1）<div>跨数据中心部署，距离较远的情况下，zk节点部署怎么分布，是否影响同步效率？</div>2024-09-10</li><br/><li><img src="" width="30px"><span>Geek_0d1fb8</span> 👍（0） 💬（1）<div>希望可以结合一些例子来讲解一下，这样能更好的理解</div>2024-07-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/55/bf/d442b55e.jpg" width="30px"><span>mikewt</span> 👍（0） 💬（2）<div>本地表，分布式表in本地表，天然分布式查询</div>2024-07-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/13/71/3762b089.jpg" width="30px"><span>stevensafin</span> 👍（1） 💬（0）<div>更多的是使用层面的东西，还是希望有原理层面的讲解</div>2024-07-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1b/2c/3d/0bd58aa4.jpg" width="30px"><span>Em</span> 👍（0） 💬（0）<div>分布式表和本地表有啥区别啊</div>2025-01-17</li><br/>
</ul>