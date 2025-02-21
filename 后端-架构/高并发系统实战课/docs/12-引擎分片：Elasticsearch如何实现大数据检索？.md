你好，我是徐长龙。

上节课我们看到了ELK对日志系统的强大支撑，如果没有它的帮助，我们自己实现分布式链路跟踪其实是十分困难的。

为什么ELK功能这么强大？这需要我们了解ELK中储存、索引等关键技术点的架构实现才能想清楚。相信你学完今天的内容，你对大数据分布式的核心实现以及大数据分布式统计服务，都会有更深入的理解。

## Elasticsearch架构

那么ELK是如何运作的？它为什么能够承接如此大的日志量？

我们先分析分析ELK的架构长什么样，事实上，它和OLAP及OLTP的实现区别很大，我们一起来看看。Elasticsearch架构如下图：

![图片](https://static001.geekbang.org/resource/image/0d/cc/0d954e660d80ae00854f29955c6168cc.jpg?wh=1920x1357 "整体的数据流向图")

我们对照架构图，梳理一下整体的数据流向，可以看到，我们项目产生的日志，会通过Filebeat或Rsyslog收集将日志推送到Kafka内。然后由LogStash消费Kafka内的日志、对日志进行整理，并推送到Elasticsearch集群内。

接着，日志会被分词，然后计算出在文档的权重后放入索引中供查询检索，Elasticsearch会将这些信息推送到不同的分片。**每个分片都会有多个副本，数据写入时，只有大部分副本写入成功了，主分片才会对索引进行落地（需要你回忆下分布式写一致知识）**。
<div><strong>精选留言（5）</strong></div><ul>
<li><img src="" width="30px"><span>Geek4892</span> 👍（0） 💬（1）<div>老师好，答疑课堂后续还会更新吗</div>2023-10-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/4e/cf/21bea6bb.jpg" width="30px"><span>衣舞晨风</span> 👍（0） 💬（1）<div>es是先获取到shardid集合然后再去请求这些shard来获取数据(https:&#47;&#47;jiankunking.com&#47;elasticsearch-search-source-code-analysis.html)；
文中说的，请求所有data节点是指到shardid集合获取数据？</div>2023-05-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1d/e7/8e/318cfde0.jpg" width="30px"><span>Spoon</span> 👍（0） 💬（1）<div>文章：Elasticsearch 每次查询都是请求所有索引所在的 Data 节点，查询请求时协调节点会在相同数据分片多个副本中，随机选出一个节点发送查询请求，从而实现负载均衡
问题：
1.请求所有索引所在的 Data 节点，这个Data节点是什么？和普通数据节点有什么区别？
2.如果所有索引放在一个Data节点，是不是会有容量限制？
3.如果将索引分片，放在多个节点，是不是又陷入了数据定位的问题？
</div>2023-04-02</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/ce/6d/530df0dd.jpg" width="30px"><span>徐石头</span> 👍（0） 💬（1）<div>来公司做的第一件事就是把搜索从mysql迁移到Elasticsearch，然后用CQRS架构解析binlog写入，Elasticsearch，用Elasticsearch做app内的内容搜索功能，我猜测极客时间的搜索功能也是用的Elasticsearch。
在做搜索相关的业务首选的便是Elasticsearch，所以如果我来实现Elasticsearch最先解决的功能便是分词和倒排索引设计，至于链路追踪和日志采集相关的组件，从业务角度我觉得地位没有搜索重要，优先级没有那么高。</div>2022-12-16</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/d0/b4/a6c27fd0.jpg" width="30px"><span>John</span> 👍（0） 💬（1）<div>老师能否列一下相关的扩展阅读资料，比如词频统计，search_type 详解之类的，不胜感激</div>2022-11-20</li><br/>
</ul>