你好，我是徐文浩。

从GFS这样的分布式文件系统，到MapReduce这样的数据批处理系统；从Bigtable这样的分布式KV数据库，到Spanner这样全球部署的强一致性关系数据库；从Storm这样只能做到“至少一次”的流式系统，到Dataflow这样真正做到“流批一体”的统一数据处理系统。在过去的30多讲里，我和你一起看过了各式各样的大数据系统。

在研究这些大数据系统的时候，我们其实有一个假设。这个假设，就是其中的每一个系统，都需要占用一组独立的服务器。而在一个完整的大数据体系中，我们既需要有GFS这样的文件系统，也需要MapReduce/Spark这样的批处理系统，还需要Bigtable这样的KV数据库、Hive这样的数据仓库、Kafka这样的消息队列，以及Flink这样的流式系统。这样一算，我们需要的服务器可真不算少。

## 成本-混合编排的需求起源

但是，当我们采购了很多服务器，搭建起了一系列的大数据系统，我们又会发现这些服务器在很多时候负载不高，显得非常浪费。因为我们在采购服务器的时候，需要根据平时的峰值流量来确定服务器数量。比如，像Kafka这样的消息队列，肯定是在早晚高峰，和中午用户比较多的时候，流量比较大，到了半夜流量就比较小。如果我们高峰时间的CPU占用要有60%，那么在低谷时刻，可能只有10%。
<div><strong>精选留言（4）</strong></div><ul>
<li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/zgricoGj6fbGXLESjTA0cX7g994ibpe70YLunwJy1hVQCnfwpqxuNrgZ6VM3aicAwYbTNasnuG8BLcy6VfbgWO71Q/132" width="30px"><span>张耒</span> 👍（1） 💬（0）<div>为啥说是电力成本呢 文章是在讨论资源合理利用，避免闲置的情况  这种应该耗电量更大吧 ？ 辛苦老师解答</div>2023-06-09</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTJGMphabeneYXs9otkAtr67RvxJClDa7jPe7w8yExg4YaS2FGJruDKMj5yN1E90o6MFibnicH8gM0ibg/132" width="30px"><span>hadoop_admin</span> 👍（0） 💬（0）<div>服务器多的话，监控、心跳都是问题</div>2022-02-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/4d/bb/abb7bfe3.jpg" width="30px"><span>csyangchsh</span> 👍（0） 💬（1）<div>1 万台服务器的额外挑战能想到的有两个：网络和机器故障。</div>2022-01-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/8f/cf/890f82d6.jpg" width="30px"><span>那时刻</span> 👍（0） 💬（3）<div>请问老师，CGroup进行资源的限制和权限的隔离，而namespace也有权限的隔离，它们的区别是什么呢？</div>2022-01-07</li><br/>
</ul>