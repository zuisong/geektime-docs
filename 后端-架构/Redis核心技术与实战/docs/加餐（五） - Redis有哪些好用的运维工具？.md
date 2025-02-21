你好，我是蒋德钧。

今天的加餐，我来给你分享一些好用的Redis运维工具。

我们在应用Redis时，经常会面临的运维工作，包括Redis的运行状态监控，数据迁移，主从集群、切片集群的部署和运维。接下来，我就从这三个方面，给你介绍一些工具。我们先来学习下监控Redis实时运行状态的工具，这些工具都用到了Redis提供的一个监控命令：INFO。

## 最基本的监控命令：INFO命令

**Redis本身提供的INFO命令会返回丰富的实例运行监控信息，这个命令是Redis监控工具的基础**。

INFO命令在使用时，可以带一个参数section，这个参数的取值有好几种，相应的，INFO命令也会返回不同类型的监控信息。我把INFO命令的返回信息分成5大类，其中，有的类别当中又包含了不同的监控内容，如下表所示：

![](https://static001.geekbang.org/resource/image/8f/a8/8fb2ef487fd9b7073fd062d480b220a8.jpg?wh=2753%2A1576)

在监控Redis运行状态时，INFO命令返回的结果非常有用。如果你想了解INFO命令的所有参数返回结果的详细含义，可以查看Redis[官网](https://redis.io/commands/info)的介绍。这里，我给你提几个运维时需要重点关注的参数以及它们的重要返回结果。

首先，**无论你是运行单实例或是集群，我建议你重点关注一下stat、commandstat、cpu和memory这四个参数的返回结果**，这里面包含了命令的执行情况（比如命令的执行次数和执行时间、命令使用的CPU资源），内存资源的使用情况（比如内存已使用量、内存碎片率），CPU资源使用情况等，这可以帮助我们判断实例的运行状态和资源消耗情况。
<div><strong>精选留言（16）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/0f/90/8a/288f9f94.jpg" width="30px"><span>Kaito</span> 👍（122） 💬（10）<div>老师这节课讲的工具很实用。

平时我们遇到的 Redis 变慢问题，有时觉得很难定位原因，其实是因为我们没有做好完善的监控。

Redis INFO 信息看似简单，但是这些信息记录着 Redis 运行时的各种状态数据，如果我们把这些数据采集到并监控到位，80% 的异常情况能在第一时间发现。

机器的 CPU、内存、网络、磁盘，都影响着 Redis 的性能。

监控时我们最好重点关注以下指标：

1、客户端相关：当前连接数、总连接数、输入缓冲大小、OPS

2、CPU相关：主进程 CPU 使用率、子进程 CPU 使用率

3、内存相关：当前内存、峰值内存、内存碎片率

4、网络相关：输入、输出网络流量

5、持久化相关：最后一次 RDB 时间、RDB fork 耗时、最后一次 AOF rewrite 时间、AOF rewrite 耗时

6、key 相关：过期 key 数量、淘汰 key 数量、key 命中率

7、复制相关：主从节点复制偏移量、主库复制缓冲区

能够查询这些指标的当前状态是最基本的，更好的方案是，能够计算出这些指标的波动情况，然后生成动态的图表展示出来，这样当某一刻指标突增时，监控能帮我们快速捕捉到，降低问题定位的难度。

目前业界比较主流的监控系统，都会使用 Prometheus 来做，插件也很丰富，监控报警也方便集成，推荐用起来。</div>2020-11-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/d2/74/7861f504.jpg" width="30px"><span>马听</span> 👍（14） 💬（0）<div>Redis 工具其他用过热 key 查找工具：redis-faina，还不错；Github地址：https:&#47;&#47;github.com&#47;facebookarchive&#47;redis-faina</div>2021-01-30</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/23/5b/983408b9.jpg" width="30px"><span>悟空聊架构</span> 👍（5） 💬（0）<div>Prometheus监控工具确实不错，界面美观，功能强大！</div>2021-05-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/99/87/5066026c.jpg" width="30px"><span>dao</span> 👍（4） 💬（0）<div>我们生产应用中使用 elastic metrcibeat 做 redis 统计监控，同时结合 zabbix 做机器监控，opserver 集合多种数据库的监控。也给开发人员准备了redis gui 工具 redisinsight。</div>2021-04-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/92/6d/becd841a.jpg" width="30px"><span>escray</span> 👍（3） 💬（0）<div>作为没有实战经验的小白，只能把本节内容暗自记下，以后需要的时候再回来查询。

运维的时候仅有 info 的信息是明显不够的，否则即使单项指标有问题，也只能依赖于经验值，如果有运维工具的话，就可以看到一段时间内的平均值、正常值、波动情况等等。

Prometheus 之前听说过，现在看来应该是开源系统监控报警框架里面比较成熟的一个了，有机会的话可以学习一下。

如果只运维 Redis 的话，CacheCloud 似乎也是一个不错的选择，不知道除了搜狐之外，有没有其他大厂采用。另外，CacheCloud 团队还写了一本《Redis开发与运维》。

有一点好奇，为什么中国团队似乎比较喜欢 Redis ？之前介绍的图书也大部分的都是国内原创的，这次介绍的运维工具也大多是国内的。</div>2021-03-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/d5/3e/7f3a9c2b.jpg" width="30px"><span>Jaising</span> 👍（1） 💬（0）<div>2023 年，可以推荐 Redis 官方出品的 RedisInsight，可视化与运维监控有颠覆 Prometheus 的趋势</div>2023-09-15</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/b4/94/2796de72.jpg" width="30px"><span>追风筝的人</span> 👍（1） 💬（0）<div>老师 加餐讲讲 Redis benchmark 性能测试的关注点？</div>2022-04-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/23/9e/d5/24fbf7c1.jpg" width="30px"><span>孙宏彬2</span> 👍（1） 💬（0）<div>老师，我直接做个从实例，然后程序更换ip这样的迁移方式，这样怎么样</div>2020-12-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/22/bd/9b/366bb87b.jpg" width="30px"><span>飞龙</span> 👍（0） 💬（0）<div>redis-shake可以满足从阿里云迁到AWS吗</div>2022-08-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/2b/60/3b/d12cd56b.jpg" width="30px"><span>Tangzen</span> 👍（0） 💬（0）<div>info states </div>2022-06-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/26/27/eba94899.jpg" width="30px"><span>罗杰</span> 👍（0） 💬（0）<div>Redis cli 🙈</div>2022-05-25</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/ce/d7/5315f6ce.jpg" width="30px"><span>不负青春不负己🤘</span> 👍（0） 💬（0）<div>Mark</div>2022-02-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/18/41/13/bf8e85cc.jpg" width="30px"><span>树心</span> 👍（0） 💬（0）<div>最基本的监控命令：INFO 命令
面向 Prometheus 的 Redis-exporter 监控
数据迁移工具 Redis-shake（数据一致性比对的工具Redis-full-check）
集群管理工具 CacheCloud</div>2022-01-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/73/a3/2b077607.jpg" width="30px"><span>Michael</span> 👍（0） 💬（0）<div>老师，你好，我有这么一个需求，两个k8s集群，分别是深圳和武汉，k8s集群中都部署了redis主从+哨兵集群，想要把深圳的redis数据迁移到武汉的redis集群环境中，因为redis实例都在pod中，redis-shake可以做到这个嘛?</div>2021-04-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/7d/41/3c5b770b.jpg" width="30px"><span>喵喵喵</span> 👍（0） 💬（0）<div>打卡</div>2020-12-30</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/75/dd/9ead6e69.jpg" width="30px"><span>黄海峰</span> 👍（0） 💬（4）<div>redis—shake解决的痛点在哪里，为何不直接同步到目的redis还要搞个中间的</div>2020-12-10</li><br/>
</ul>