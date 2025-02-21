你好，我是唐聪。

通过前面课程的学习，我相信你已经对etcd基本架构、核心特性有了一定理解。如果让你基于Raft协议，实现一个简易的类etcd、支持多存储引擎的分布式KV服务，并能满足读多写少、读少写多的不同业务场景诉求，你知道该怎么动手吗？

纸上得来终觉浅，绝知此事要躬行。

今天我就和你聊聊如何实现一个类etcd、支持多存储引擎的KV服务，我们将基于etcd自带的[raftexample](https://github.com/etcd-io/etcd/tree/v3.4.9/contrib/raftexample)项目快速构建它。

为了方便后面描述，我把它命名为metcd（表示微型的etcd），它是raftexample的加强版。希望通过metcd这个小小的实战项目，能够帮助你进一步理解etcd乃至分布式存储服务的核心架构、原理、典型问题解决方案。

同时在这个过程中，我将详细为你介绍etcd的Raft算法工程实现库、不同类型存储引擎的优缺点，拓宽你的知识视野，为你独立分析etcd源码，夯实基础。

## 整体架构设计

在和你深入聊代码细节之前，首先我和你从整体上介绍下系统架构。

下面是我给你画的metcd整体架构设计，它由API层、Raft层的共识模块、逻辑层及存储层组成的状态机组成。

接下来，我分别和你简要分析下API设计及复制状态机。
<div><strong>精选留言（5）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/22/3a/de/e5c30589.jpg" width="30px"><span>云原生工程师</span> 👍（12） 💬（2）<div>设计上存储引擎的介绍，获益匪浅，具体实现上的解读，也搞清了之前几个疑问，etcd足够轻量级，简直就是学习分布式系统的最佳案例，后面抽空自己基于raft搞个小小项目，进一步加深下，老师在这块有什么分布式书籍推荐没</div>2021-03-02</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/2a/b9/2bf8cc89.jpg" width="30px"><span>无名氏</span> 👍（6） 💬（0）<div>大佬 有完整demo可以分享吗😀</div>2022-02-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/29/36/7d/eab0d26a.jpg" width="30px"><span>丹尼尔-雪碧</span> 👍（0） 💬（0）<div>请问大佬，raft模块返回的快照信息，快照是从哪里来的？我理解快照就是从kvStorage来的？所以是当需要生成快照的时候，raft模块调用kvStorage的接口生成快照？</div>2022-07-31</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/49/fc/5627215c.jpg" width="30px"><span>小何</span> 👍（0） 💬（0）<div>这个实现的代码在哪里可以下载？</div>2022-05-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/bc/fc/cf98963a.jpg" width="30px"><span>lixg</span> 👍（0） 💬（1）<div>文中提到“Messages，持久化 Entries 后，发送给其他节点的消息”

这里的消息是指什么消息，包含什么内容？</div>2022-03-14</li><br/>
</ul>