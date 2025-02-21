你好，我是黄金。今天我们来复习Chubby这篇论文。

## **Chubby介绍**

Chubby是一种粗粒度的分布式锁服务，允许多个客户端通过分布式锁，就某项提议达成共识。它的**首要设计目标是可靠性、可用性和易用性**，而吞吐量和存储能力是次要的。

Chubby的客户端接口类似Unix文件系统，可以方便地读写文件，在此之上它还提供了锁操作，以及诸如文件内容变化之类的事件变更通知机制。合理地使用Chubby，我们甚至可以让它同时服务几万个客户端。

在GFS中，Chubby用于选举Master；在Bigtable中，Chubby不仅用于选举Master，还能够让Master方便地发现Tablet Server服务，也能让客户端轻松地找到Master地址。

## **课程内容梳理**

徐老师通过3节课给我们讲透了Chubby论文，其内容的广度和深度远超论文本身。让我们先来回顾下课程内容。

[第1讲](https://time.geekbang.org/column/article/426865)首先提出了两个问题：GFS如何保证集群中只有一个Master？以及Master怎么把数据同步复制到Backup Master，由此引出了**分布式共识问题**。接着讨论了分布式系统中同步复制数据的解决方案，也就是两阶段提交和三阶段提交，而不管是哪一种方式，我们都面临着协调者单点故障的问题。如果协调者需要自动选举，如何保证系统中只有一个协调者，问题又再次指向了分布式共识。
<div><strong>精选留言（2）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/16/0f/70/f59db672.jpg" width="30px"><span>槑·先生</span> 👍（0） 💬（0）<div>关于paxos总结得不错👍</div>2022-06-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1b/a9/12/e041e7b2.jpg" width="30px"><span>Ping</span> 👍（0） 💬（1）<div>chubby脱离Bigtable单独用的时候多吗？</div>2021-12-31</li><br/>
</ul>