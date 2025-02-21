你好，我是大明。今天我们学习 Elasticsearch 的另外一个关键主题——高性能。

如果你经常和 Elasticsearch 打交道，你十有八九遇到过 Elasticsearch 的性能问题。这也就是为什么在面试中我们经常会遇到 Elasticsearch 性能优化相关的问题。 那么今天我就带你看看怎么优化 Elasticsearch 的性能，在面试中赢得竞争优势。

我们先来看 Elasticsearch 的索引机制，它是我们理解 Elasticsearch 原理的关键。

## Elasticsearch 的索引机制

Elasticsearch 的索引和之前你已经学习过的数据库索引比起来，还是有很大不同的，它使用的是倒排索引。所谓的倒排索引是相对于“正排”索引而言的。在一般的文件系统中，索引是文档映射到关键字，而倒排索引正相反，是从关键字映射到了文档。

![图片](https://static001.geekbang.org/resource/image/db/cd/db5821d3c177ba83963442c6c8fd56cd.png?wh=1920x659)

所以你可以想到，假如说没有倒排索引，你想要找到包含关键字“Elasticsearch”的文档，那么你需要遍历所有的文档，然后筛选出包含了“Elasticsearch”关键字的文档。而有了倒排索引，你就可以直接从关键字出发，找到“Elasticsearch”关键字对应的文档。

Elasticsearch 依赖于 Lucene 来维护索引，它的基本原理也很简单。
<div><strong>精选留言（7）</strong></div><ul>
<li><img src="" width="30px"><span>Geek_035c60</span> 👍（0） 💬（1）<div>解释索引机制，posting list 其中的 Hello 单词在文档0、文档1都出现，为什么posting list 中只记录了文档0的信息，没有文档1的信息的呢？</div>2023-11-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/25/87/f3a69d1b.jpg" width="30px"><span>peter</span> 👍（0） 💬（1）<div>请教老师两个问题：
Q1：对于一个网站，ES主要用于日志处理吗？
Q2：ES的源码是否值得研究？复杂吗？</div>2023-09-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/28/44/cf/791d0f5e.jpg" width="30px"><span>ZhiguoXue_IT</span> 👍（0） 💬（1）<div>1）优化那个间隔时间，需要根据业务场景来选择，有些场景太慢确实影响用户
2）作者提到的冷热分离优化偏机器配置上，机器配置决定性能的大小
冷热分离，也可以根据索引数的个数来区分，比如冷索引数据比较多可以多一些索引数
也可以通过将冷索引的段数强制合并成1，提高搜索性能</div>2023-09-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/fc/d1/57ba44a1.jpg" width="30px"><span>果娞</span> 👍（1） 💬（0）<div>标题不是优化es的查询性能吗怎么后面都变成优化写入性能了，优化查询性能就那两种情况吗</div>2024-11-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/26/b4/73/48f6361b.jpg" width="30px"><span>牧鱼羊</span> 👍（1） 💬（0）<div>先回答在冷热分离中，一般冷数据我们的都是用机械硬盘，而热数据就是用固态硬盘，你知道这是为什么吗？理由主要是两点：从成本上考虑一般都会考虑机械硬盘，并且机械硬盘更适合存储；但由于是热数据所以考虑速度，使用更快的固态硬盘以支持更频繁的读写
2. 在实践中我们利用了ES进行向量数据处理，但是由于成本问题，最终还是优化掉了，使用插件在postgreSQL上支持向量数据查询</div>2024-06-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/bf/22/26530e66.jpg" width="30px"><span>趁早</span> 👍（0） 💬（0）<div>文件描述符那个根本不算Bug</div>2025-02-16</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/36/f3/d4/86a99ae0.jpg" width="30px"><span>哆啦a喵</span> 👍（0） 💬（0）<div>老师，想问一下，优化es那里，批量处理那块的第二个策略，什么是调整批次呀？</div>2024-05-21</li><br/>
</ul>