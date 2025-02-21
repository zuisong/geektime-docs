你好，我是韩健。

学完[上一讲](https://time.geekbang.org/column/article/217049)后，相信你已经了解了分布式KV系统的架构设计，同时应该也很好奇，架构背后的细节代码是怎么实现的呢？

别着急，今天这节课，我会带你弄明白这个问题。我会具体讲解[分布式KV系统](https://github.com/hanj4096/raftdb)核心功能点的实现细节。比如，如何实现读操作对应的3种一致性模型。而我希望你能在课下反复运行程序，多阅读源码，掌握所有的细节实现。

话不多说，我们开始今天的学习。

在上一讲中，咱们将系统划分为三大功能块（接入协议、KV操作、分布式集群），那么今天我会按顺序具体说一说每块功能的实现，帮助你掌握架构背后的细节代码。首先，先来了解一下，如何实现接入协议。

## 如何实现接入协议？

在19讲提到，我们选择了HTTP协议作为通讯协议，并设计了"/key"和"/join"2个HTTP RESTful API，分别用于支持KV操作和增加节点的操作，那么，它们是如何实现的呢？

接入协议的核心实现，就是下面的样子。

![](https://static001.geekbang.org/resource/image/b7/56/b72754232480fadd7d8eeb9bfdd15e56.jpg?wh=1142%2A369 "图1")

我带你走一遍这三个步骤，便于你加深印象。

1. 在ServeHTTP()中，会根据URL路径设置相关的路由信息。比如，会在handlerKeyRequest()中处理URL路径前缀为"/key"的请求，会在handleJoin()中处理URL路径为"/join"的请求。
2. 在handleKeyRequest()中，处理来自客户端的KV操作请求，也就是基于HTTP POST请求的赋值操作、基于HTTP GET请求的查询操作、基于HTTP DELETE请求的删除操作。
3. 在handleJoin()中，处理增加节点的请求，最终调用raft.AddVoter()函数，将新节点加入到集群中。
<div><strong>精选留言（18）</strong></div><ul>
<li><img src="https://wx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTIC2Ww3swYiaMalnpA1f87xgzV8Hs1Y27M2CbNQqgR27Il72hibXn5FvhU7mbr3XKsxYDZdjY4GMDbg/132" width="30px"><span>wjh_all_in</span> 👍（10） 💬（1）<div>这里实现一致性，没有采用Quorum NWR，而是把所有读请求都转移到主节点，这在实际的生产系统会成为瓶颈吧？</div>2020-03-30</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/65/89/e2ceca70.jpg" width="30px"><span>方块睡衣</span> 👍（7） 💬（1）<div>老师请留意下项目地址</div>2020-04-01</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/47/31/f35367c8.jpg" width="30px"><span>小晏子</span> 👍（5） 💬（2）<div>如果移除节点，那要考虑是移除主节点还是非主节点吧，如果是主节点那么需要重新发起选主流程，并将主节点数据同步到其他节点，如果是非主节点，那么要通知主节点该节点移除不需要在发送日志给它了。</div>2020-03-30</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/c7/97/e88b94da.jpg" width="30px"><span>还有这种操作</span> 👍（3） 💬（2）<div>老师有没有代码示例，或者项目示例</div>2020-03-30</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/3e/d2/5f9d3fa7.jpg" width="30px"><span>羽翼1982</span> 👍（1） 💬（1）<div>一路过来追老师的课，收获还是蛮多的；不过比起实现的细节，我还是想更多了解设计和架构上的知识，特别是这些理论在成熟的开源分布式系统上应用（Kafka，TiDB，ETCD，Cassandra等等），希望老师能够同通过加餐的形式补充这些内容</div>2020-03-31</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/23/30/5f/69e63a33.jpg" width="30px"><span>🤔 2⃣ 0⃣ 1⃣ 9⃣🙄 🤥</span> 👍（0） 💬（1）<div>$GOPATH&#47;bin&#47;raftdb -id node02 -haddr raft-cluster-host02:8091 -raddr raft-cluster-host02:8089 -join raft-cluster-host01:8091 ~&#47;.raftdb

$GOPATH&#47;bin&#47;raftdb -id node02 -haddr raft-cluster-host02:8091 -raddr raft-cluster-host02:8089  ~&#47;.raftdb
老师，添加第二个节点，这两条命令都要执行一遍吗？我执行第一条就被阻塞了</div>2020-11-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/19/d9/ff/b23018a6.jpg" width="30px"><span>Heaven</span> 👍（0） 💬（1）<div>那么整体流程还是按照写操作的流程
获取到store中进行执行
如果不报错,就说进行了RemoveServer()
报错了,查看报错信息,如果是因为不是领导者节点,那么直接返回客户端领导者的地址,让其进行重定向
如果是因为删除节点是领导者节点,无法删除导致的,那么直接返回客户端错误信息
(我这里认为是无法删除领导者节点的,应该由管理人员直接杀死领导者节点的进程)</div>2020-08-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/19/d9/ff/b23018a6.jpg" width="30px"><span>Heaven</span> 👍（0） 💬（1）<div>那么整体流程还是按照写操作的流程
获取到store中进行执行
如果不报错,就说进行了RemoveServer()
报错了,查看报错信息,如果是因为不是领导者节点,那么直接返回客户端领导者的地址,让其进行重定向
如果是因为删除节点是领导者节点,无法删除导致的,那么直接返回客户端错误信息
(我这里认为是无法删除领导者节点的,应该由管理人员直接杀死领导者节点的进程)</div>2020-08-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/dd/21/382ec2bf.jpg" width="30px"><span>向永俊</span> 👍（0） 💬（4）<div>基于Hashicorp，如果在分布式kv系统中，需要实现cas功能，应该怎么实现</div>2020-08-05</li><br/><li><img src="" width="30px"><span>Geek_5735ca</span> 👍（0） 💬（1）<div>1.hddr和rddr代表什么含义?
2.单机上怎么模拟多个ip地址?</div>2020-04-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/f6/e3/e4bcd69e.jpg" width="30px"><span>沉淀的梦想</span> 👍（0） 💬（2）<div>项目地址在哪里？自己实现 Raft 的话，正确性要如何测试呢？</div>2020-03-31</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/c3/5d/ced9b5c2.jpg" width="30px"><span>Michael Tesla</span> 👍（0） 💬（2）<div>老师能不能推荐一些课外的相关资料呢？</div>2020-03-31</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/0d/83/9f4bc7eb.jpg" width="30px"><span>杜享平</span> 👍（1） 💬（2）<div>可以再丰富一下，如果数据量比较大，单机存不下，必须对数据做分片处理，这个时候应该怎么设计</div>2021-04-02</li><br/><li><img src="" width="30px"><span>Geek_ae855f</span> 👍（0） 💬（0）<div>谢谢老师的课程，几个月前就看了理论篇和开篇词，但一直没进行实战篇，因为自己基础不行，现在重新补了实战篇感觉收获很大。raft算法的一致性的强弱是基于上层业务确定的嘛</div>2023-01-27</li><br/><li><img src="" width="30px"><span>public</span> 👍（0） 💬（1）<div>读写都在主节点上面，那性能和单件差不多了</div>2022-04-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/63/85/1dc41622.jpg" width="30px"><span>姑射仙人</span> 👍（0） 💬（0）<div>老师，Store中的m就代表实现的存储系统实际的数据载体，为什么要在内存中用map表示。实际场景中此处是否可以替换成自己需要的，比如基于数据库的存储？如果可以的话，那么Snapshot为什么还要Restore到内存中的map中去，如果数据量特别大，Restore到存中的map会特别耗时，而且还会和底层存储产生一致性问题。</div>2021-10-05</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1e/f5/97/9a7ee7b3.jpg" width="30px"><span>Geek4329</span> 👍（0） 💬（0）<div>当raft将指令应用到状态机后，将执行applySet功能，创建key和value到内存中。这一点没看明白，我理解Raft主要管理复制日志，但是日志如何应用到状态机这个需要应用自己实现fsm的几个接口。状态机存储这个也是应用自己决定，可以选择内存，文件等。这个地方应用到状态机完成后内存中已经有了kv，后面为什么还要执行其他操作呢？</div>2021-01-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/23/30/5f/69e63a33.jpg" width="30px"><span>🤔 2⃣ 0⃣ 1⃣ 9⃣🙄 🤥</span> 👍（0） 💬（0）<div>$GOPATH&#47;bin&#47;raftdb -id node02 -haddr raft-cluster-host02:8091 -raddr raft-cluster-host02:8089 -join raft-cluster-host01:8091 ~&#47;.raftdb</div>2020-11-12</li><br/>
</ul>