你好，我是大明。今天开始我们要学习一个新的主题——NoSQL。在这个主题里面，我们先从 Elasticsearch 开始学起。

Elasticsearch 从面试的热度上来说，肯定是比不过数据库、缓存和消息队列。但是 Elasticsearch 在中大型公司里面又非常常用，这意味着如果你希望跳槽到一些比较大型的公司，那么 Elasticsearch 还是有比较大的概率考到的。

就像我之前说的，目前互联网行业面试中间件的话，就是高可用和高性能。而具体到每一个点，又可以拆成两个方向。

1. 中间件是如何做到高可用/高性能的？
2. 你在实践中怎么做到高可用/高性能？

那么这一节课我们就先来看高可用这一个点，并给出几个有亮点的提高可用性的方案，让你在面试的时候赢得竞争优势。在这里我就不严格区分 Elasticsearch 还是 Lucene，统一使用 Elasticsearch。我们先来看看 Elasticsearch 中的节点角色。

## Elasticsearch 节点角色

Elasticsearch 的节点可以分成很多种角色，并且一个节点可以扮演多种角色。这里我列举几种主要的。

- 候选主节点（Master-eligible Node)：可以被选举为主节点的节点。主节点主要负责集群本身的管理，比如说创建索引。类似的还有仅投票节点（Voting-only Node），这类节点只参与主从选举，但是自身并不会被选举为主节点。
- 协调节点（Coordinating Node）：协调节点负责协调请求的处理过程。一个查询请求会被发送到协调节点上，协调节点确定数据节点，然后让数据节点执行查询，最后协调节点合并数据节点返回的结果集。大多数节点都会兼任这个角色。
- 数据节点（Data Node）：存储数据的节点。当协调节点发来查询请求的时候，也会执行查询并且把结果返回给协调节点。类似的还有热数据节点（Hot Data Node）、暖数据节点（Warm Data Node）、冷数据节点（Cold Data Node），你从名字就可以看出来，它们只是用于存储不同热度的数据。
<div><strong>精选留言（4）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/11/10/60/146594a2.jpg" width="30px"><span>头号玩家</span> 👍（5） 💬（1）<div>系统刚刚启动的时候，选取id最小的备选master为master节点。
系统运行起来之后，master和非master节点间是存在一个类似心跳检测的ping机制的，当master ping不到其他节点，或者其他节点ping不到master的时候，他们之间就会互相判断，是否大多数都连不到主节点上了，如果大多数都连不上，那么就开始重新进行master选举。</div>2023-09-20</li><br/><li><img src="" width="30px"><span>Geek_035c60</span> 👍（0） 💬（2）<div>请问一下：但是没有被合并的段，就相当于告知了查询使用新的段。这是什么意思呀？</div>2023-11-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/28/44/cf/791d0f5e.jpg" width="30px"><span>ZhiguoXue_IT</span> 👍（0） 💬（1）<div>Es的高可用，在实际使用中，我们比较关注的一个点是refresh_interval的大小，这个值太小对es会造成压力，太大会搜索延时比较高</div>2023-09-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/25/87/f3a69d1b.jpg" width="30px"><span>peter</span> 👍（0） 💬（1）<div>请教老师几个问题：
Q1：投票节点只用来投票岂不是极大的浪费？
Q2：ES角色的划分，是逻辑划分吗？还是操作层面上的划分？比如在ES上进行某个设置就可以确定角色。
Q3：“分片”是指对数据的分片，不是针对节点（机器），对吗？
Q4：ES能够控制Page Cache吗？ 文中提到ES将数据写到Page Cache，数据写到Page Cache，这个是可以控制的吗？如果Linux下可以控制，Windows下是否也可以控制？</div>2023-09-20</li><br/>
</ul>