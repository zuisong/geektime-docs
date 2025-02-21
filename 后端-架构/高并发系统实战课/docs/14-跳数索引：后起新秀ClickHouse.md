你好，我是徐长龙。

通过前面的学习，我们见识到了Elasticsearch的强大功能。不过在技术选型的时候，价格也是重要影响因素。Elasticsearch虽然用起来方便，但却有大量的硬件资源损耗，再富有的公司，看到每月服务器账单的时候也会心疼一下。

而ClickHouse是新生代的OLAP，尝试使用了很多有趣的实现，虽然仍旧有很多不足，比如不支持数据更新、动态索引较差、查询优化难度高、分布式需要手动设计等问题。但由于它架构简单，整体相对廉价，逐渐得到很多团队的认同，很多互联网企业加入社区，不断改进ClickHouse。

ClickHouse属于列式存储数据库，多用于写多读少的场景，它提供了灵活的分布式存储引擎，还有分片、集群等多种模式，供我们搭建的时候按需选择。

这节课我会从写入、分片、索引、查询的实现这几个方面带你重新认识ClickHouse。在学习过程中建议你对比一下Elasticsearch、MySQL、RocksDB的具体实现，想想它们各有什么优缺点，适合什么样的场景。相信通过对比，你会有更多收获。

## 并行能力CPU吞吐和性能

我先说说真正使用ClickHouse的时候，最让我意料不到的地方。
<div><strong>精选留言（12）</strong></div><ul>
<li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/YbUxEV3741vKZAiasOXggWucQbmicJwIjg3HDE58oyibYXbSop9QQFqZ7X6OhynDoo6rDHwzK8njSeJjN9hx3pJXg/132" width="30px"><span>黄堃健</span> 👍（1） 💬（1）<div>好，我们回头来整体看看 ClickHouse 的查询工作流程：
1. 根据查询条件，查询过滤出需要读取的 data part 文件夹范围；
2. 根据 data part 内数据的主键索引、过滤出要查询的 granule；
3. 使用 skip index 跳过不符合的 granule；

-- 老师， 前面的3个步骤都涉及到过滤，不明白有什么区别，能举例说明一下吗？</div>2024-03-09</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/YbUxEV3741vKZAiasOXggWucQbmicJwIjg3HDE58oyibYXbSop9QQFqZ7X6OhynDoo6rDHwzK8njSeJjN9hx3pJXg/132" width="30px"><span>黄堃健</span> 👍（0） 💬（1）<div>在实际用上 ClickHouse 之后，你会发现很难对它做索引查询优化，动不动就扫全表，这是为什么呢？
主要是我们大部分数据的特征不是很明显、建立的索引区分度不够高

--老师，索引区分度不够高。 这个索引区分度 指的是 主键索引，还是跳表索引。  

谢谢老师的评论。</div>2024-03-09</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/YbUxEV3741vKZAiasOXggWucQbmicJwIjg3HDE58oyibYXbSop9QQFqZ7X6OhynDoo6rDHwzK8njSeJjN9hx3pJXg/132" width="30px"><span>黄堃健</span> 👍（0） 💬（1）<div>老师，新年好， 大部分数据的特征不是很明显、建立的索引区分度不够？ 这句话怎么理解？是主键的区分度不高吗？ 因为只有主键才有索引。如果是主键，怎么可能区分度不高呢？ 如果不是？究竟是怎么意思？</div>2024-02-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/4c/b5/fcede1a9.jpg" width="30px"><span>IT小村</span> 👍（0） 💬（1）<div>elasticsearch的写性能并不高</div>2023-12-02</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/97/0b/a943bcb3.jpg" width="30px"><span>zhou</span> 👍（0） 💬（1）<div>clickhourse存储有leve0,leve1,leve2，用datapart的文件的方式存储，那多节点的情况下是如何做到同步的。</div>2023-02-07</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1a/f3/8d/402e0e0f.jpg" width="30px"><span>林龍</span> 👍（0） 💬（1）<div>读吞吐跟QPS有什么区别？一直以为是同个东西</div>2023-01-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1a/f3/8d/402e0e0f.jpg" width="30px"><span>林龍</span> 👍（0） 💬（1）<div>感觉用clickhouse就是为了解决MySQL慢的问题，但是却没有es那么好用，还要考虑的问题反而加大了</div>2023-01-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/60/71/895ee6cf.jpg" width="30px"><span>分清云淡</span> 👍（0） 💬（2）<div>mysql写性能不差吧？</div>2022-12-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/94/fe/5fbf1bdc.jpg" width="30px"><span>Layne</span> 👍（0） 💬（1）<div>看到了几个通性：
1.利用分片提高写性能
2.通过后期合并来提高查询性能
3.利用布隆过滤器快速检验数据存在标志位
4.利用顺序性特性，磁盘顺序写，存储文件顺序性，天生降低数据的杂乱</div>2022-12-05</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/20/04/5e/5d2e6254.jpg" width="30px"><span>Elvis Lee</span> 👍（0） 💬（3）<div>ClickHouse 是不能轻易修改删除数据的，那我们要如何做历史数据的清理呢？
1.设置TTL
2.表使用ReplaceMergetree</div>2022-11-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/31/0d/fb/a5fef3f7.jpg" width="30px"><span>移横为固</span> 👍（0） 💬（1）<div>有简单使用clickhouse，考虑到clickhouse的特性，对需要修改的数据是不放入clickhouse存储。在历史数据清理上，使用过两个方法：
1.clickhouse支持过期删除策略，可以根据表中的时间字段设置过期时间，让clickhouse帮忙自动删除过期数据。
2.clickhouse存储数据会对数据进行分区存储，建表时就可以设置好分区字段，类似平常所说的水平分表。在删除数据时可以查找到表的分区信息，按分区删除数据。</div>2022-11-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/be/52/568e8c06.jpg" width="30px"><span>lvvp</span> 👍（0） 💬（0）<div>为什么是写多于读？olap场景，读多写少（强调大批量一次性写入增加吞吐量）</div>2024-09-04</li><br/>
</ul>