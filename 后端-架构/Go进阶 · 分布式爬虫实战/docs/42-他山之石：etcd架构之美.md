你好，我是郑建勋。

这节课，我们来聊一聊我们将在分布式项目中使用的重要中间件：etcd。

etcd这个名字是 etc distributed 的缩写。我们知道，在Linux中etc目录存储了系统的配置文件，所以etcd代表了分布式的配置中心系统。然而，它能够实现的功能远不是同步配置文件这么简单。etcd可以作为分布式协调的组件帮助我们实现分布式系统。

使用etcd的重要项目包括了CoreOS与Kubernetes。etcd使用 Go 书写，底层使用了 Raft 协议，它的架构本身非常优美。这节课就让我们来看一看etcd的架构、核心特性和实现机制，这样我们才能利用etcd更好地完成分布式协调工作，领会这个优秀的开源组件的设计哲学。同时，掌握etcd也有助于我们更深入地了解Kubernetes的运行机制。

## etcd全局架构

etcd的第一个版本 v0.1 于2013年发布，现在已经更新到了v3，在这个过程中，etcd 的稳定性、扩展性、性能都在不断提升。我们这节课主要讨论的是当前最新的v3版本。话不多说，我们先来从整体上看一看etcd的架构。

![](https://static001.geekbang.org/resource/image/b3/11/b37975657d35abfca244f2884d840c11.jpg?wh=1920x736)

etcd从大的方面可以分为几个部分，让我们结合图片从右往左说起。

**首先etcd抽象出了raft-http模块，由于etcd通常为分布式集群部署方式，该层用于处理和其他etcd节点的网络通信。**etcd内部使用了HTTP协议来进行通信，由于etcd中的消息类型很多，心跳探活的数据量较小，快照信息较大（可达GB级别），所以etcd有两种处理消息的通道，分别是Pipeline消息通道与Stream消息通道。
<div><strong>精选留言（1）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/10/7f/d3/b5896293.jpg" width="30px"><span>Realm</span> 👍（4） 💬（0）<div>思考题：
1. MVCC（Multi-Version Concurrency Control），即多版本并发控制。MVCC 是一种并发控制的方法，可以实现对数据库的并发访问。

2. MySQL的MVCC工作在RC(读提交)和RR(重复读)的隔离级别。 
表的行记录逻辑上是一个链表，既保留业务数据本身，还有两个隐藏字段：
- trx_id（最近修改的事务ID）
- roll_ptr(指向上一个版本数据的指针,通过undo log可以实现从高版本到低版本的迁跃)

3. ETCD的MVCC同样可以维护一个数据(key对应的值)的多个历史版本，且使得读写操作没有冲突,不使用锁，增加系统吞吐。

4. 窥探etcd对同一个key进行修改，内部版本的变化
```
&gt; docker exec etcd-gcr-v3.5.5 &#47;bin&#47;sh -c &quot;&#47;usr&#47;local&#47;bin&#47;etcdctl put a 1 &quot;
OK

&gt; docker exec etcd-gcr-v3.5.5 &#47;bin&#47;sh -c &quot;&#47;usr&#47;local&#47;bin&#47;etcdctl get a -w=json&quot;
{&quot;header&quot;:{&quot;cluster_id&quot;:18011104697467366872,&quot;member_id&quot;:6460912315094810421,&quot;revision&quot;:22,&quot;raft_term&quot;:3},&quot;kvs&quot;:[{&quot;key&quot;:&quot;YQ==&quot;,&quot;create_revision&quot;:22,&quot;mod_revision&quot;:22,&quot;version&quot;:1,&quot;value&quot;:&quot;MQ==&quot;}],&quot;count&quot;:1}

&gt; docker exec etcd-gcr-v3.5.5 &#47;bin&#47;sh -c &quot;&#47;usr&#47;local&#47;bin&#47;etcdctl put a 2 &quot;
OK

&gt; docker exec etcd-gcr-v3.5.5 &#47;bin&#47;sh -c &quot;&#47;usr&#47;local&#47;bin&#47;etcdctl get a -w=json&quot;
{&quot;header&quot;:{&quot;cluster_id&quot;:18011104697467366872,&quot;member_id&quot;:6460912315094810421,&quot;revision&quot;:23,&quot;raft_term&quot;:3},&quot;kvs&quot;:[{&quot;key&quot;:&quot;YQ==&quot;,&quot;create_revision&quot;:22,&quot;mod_revision&quot;:23,&quot;version&quot;:2,&quot;value&quot;:&quot;Mg==&quot;}],&quot;count&quot;:1}


&gt; docker exec etcd-gcr-v3.5.5 &#47;bin&#47;sh -c &quot;&#47;usr&#47;local&#47;bin&#47;etcdctl put a 3 &quot;
OK

&gt; docker exec etcd-gcr-v3.5.5 &#47;bin&#47;sh -c &quot;&#47;usr&#47;local&#47;bin&#47;etcdctl get a -w=json&quot;
{&quot;header&quot;:{&quot;cluster_id&quot;:18011104697467366872,&quot;member_id&quot;:6460912315094810421,&quot;revision&quot;:24,&quot;raft_term&quot;:3},&quot;kvs&quot;:[{&quot;key&quot;:&quot;YQ==&quot;,&quot;create_revision&quot;:22,&quot;mod_revision&quot;:24,&quot;version&quot;:3,&quot;value&quot;:&quot;Mw==&quot;}],&quot;count&quot;:1}
```</div>2023-01-14</li><br/>
</ul>