你好，我是彭旭。

上节课我们介绍了ClickHouse应该怎么配置集群，以及怎么用分布式表和集群的能力，并行处理数据的写入与查询。

通过利用分布式并行计算，ClickHouse的性能与扩展性得到了进一步提升，之前我们也用CDP场景测试过了StarRocks的性能。

所以这节课，我们在相同的集群机器配置中，先来对比一下ClickHouse与StarRocks的性能。然后再给你介绍一个能够加速标签AND、OR计算的数据结构bitmap。

## CDP在ClickHouse下的性能表现

首先，我们在一个与前面StarRocks相同配置的集群中，使用分布式表，将之前的2千万用户与1亿行为事件导入，看看在CDP的几个场景中，ClickHouse的性能表现如何。

### 数据准备

我给你准备好了几个[建表脚本](https://github.com/ZHAMoonlight/referencebook/blob/master/script/ls19_cdp.sql)，是在ClickHouse中使用分布式表引擎，创建CDP相关的几个表。

至于数据，你仍然可以复用之前在StarRocks中的[测试数据集](https://pan.baidu.com/s/1Es3ffXjVKpZ73RJNPWWcsw?pwd=abw3)。

ClickHouse客户端工具clickhouse-client可以快速地将csv格式的数据导入表，下面这个命令就将文件cdp\_user\_data.csv的数据导入到了cdp.cdp\_user\_all表中。
<div><strong>精选留言（1）</strong></div><ul>
<li><img src="" width="30px"><span>Geek_5e1c70</span> 👍（0） 💬（1）<div>cdp_user_local 表的建表sql，分区键是不是应该使用toYYYYMM(register_date)，不然分区粒度太细，ck会报错</div>2024-09-19</li><br/>
</ul>