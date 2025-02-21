你好，我是黄金。今天这期复习课，咱们来回顾和总结思考下Spanner这篇论文的内容。

## Spanner介绍

Spanner，是第一个同时支持外部一致性分布式事务和全球部署的分布式数据库，它能够伸缩至百万台服务器、横跨数百个数据中心、存储万亿条记录。那么，在这么大规模的分布式系统中，**如何高效地支持外部一致性事务**，就是我们需要关注的重点。

## 课程内容回顾

我们先来回顾下徐老师所讲的课程内容。

[第一讲](https://time.geekbang.org/column/article/446551)谈了Spanner的架构与实现。在架构上，Spanner由多个Zone构成，所有的Zone由一个Universe管理。Zone负责读写数据，它的结构类似Bigtable，由Zonemaster、Spanserver和Location Proxy构成；Universe负责管理Zone的状态，在Zone与Zone之间调度数据。

在实现上，数据是通过(key:string, timestamp:int64) -&gt; value:string这样的映射关系来表示的，TimeStamp，也就是版本是在整行数据上，而不是像Bigtable那样在列上。数据的组织顺序像Megastore的EntityGroup，关联在一起的数据在Spanner中被称为目录。