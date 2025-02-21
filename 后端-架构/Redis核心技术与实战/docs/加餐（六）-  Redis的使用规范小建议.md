你好，我是蒋德钧。

今天的加餐，我们来聊一个轻松点儿的话题，我来给你介绍一下Redis的使用规范，包括键值对使用、业务数据保存和命令使用规范。

毕竟，高性能和节省内存，是我们的两个目标，只有规范地使用Redis，才能真正实现这两个目标。如果说之前的内容教会了你怎么用，那么今天的内容，就是帮助你用好Redis，尽量不出错。

好了，话不多说，我们来看下键值对的使用规范。

## 键值对使用规范

关于键值对的使用规范，我主要想和你说两个方面：

1. key的命名规范，只有命名规范，才能提供可读性强、可维护性好的key，方便日常管理；
2. value的设计规范，包括避免bigkey、选择高效序列化方法和压缩方法、使用整数对象共享池、数据类型选择。

### 规范一：key的命名规范

一个Redis实例默认可以支持16个数据库，我们可以把不同的业务数据分散保存到不同的数据库中。

但是，在使用不同数据库时，客户端需要使用SELECT命令进行数据库切换，相当于增加了一个额外的操作。

其实，我们可以通过合理命名key，减少这个操作。具体的做法是，把业务名作为前缀，然后用冒号分隔，再加上具体的业务数据名。这样一来，我们可以通过key的前缀区分不同的业务数据，就不用在多个数据库间来回切换了。
<div><strong>精选留言（13）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/0f/90/8a/288f9f94.jpg" width="30px"><span>Kaito</span> 👍（266） 💬（19）<div>我总结的 Redis 使用规范分为两大方面，主要包括业务层面和运维层面。

业务层面主要面向的业务开发人员：

1、key 的长度尽量短，节省内存空间
2、避免 bigkey，防止阻塞主线程
3、4.0+版本建议开启 lazy-free
4、把 Redis 当作缓存使用，设置过期时间
5、不使用复杂度过高的命令，例如SORT、SINTER、SINTERSTORE、ZUNIONSTORE、ZINTERSTORE
6、查询数据尽量不一次性查询全量，写入大量数据建议分多批写入
7、批量操作建议 MGET&#47;MSET 替代 GET&#47;SET，HMGET&#47;HMSET 替代 HGET&#47;HSET
8、禁止使用 KEYS&#47;FLUSHALL&#47;FLUSHDB 命令
9、避免集中过期 key
10、根据业务场景选择合适的淘汰策略
11、使用连接池操作 Redis，并设置合理的参数，避免短连接
12、只使用 db0，减少 SELECT 命令的消耗
13、读请求量很大时，建议读写分离，写请求量很大，建议使用切片集群

运维层面主要面向的是 DBA 运维人员：

1、按业务线部署实例，避免多个业务线混合部署，出问题影响其他业务
2、保证机器有足够的 CPU、内存、带宽、磁盘资源
3、建议部署主从集群，并分布在不同机器上，slave 设置为 readonly
4、主从节点所部署的机器各自独立，尽量避免交叉部署，对从节点做维护时，不会影响到主节点
5、推荐部署哨兵集群实现故障自动切换，哨兵节点分布在不同机器上
6、提前做好容量规划，防止主从全量同步时，实例使用内存突增导致内存不足
7、做好机器 CPU、内存、带宽、磁盘监控，资源不足时及时报警，任意资源不足都会影响 Redis 性能
8、实例设置最大连接数，防止过多客户端连接导致实例负载过高，影响性能
9、单个实例内存建议控制在 10G 以下，大实例在主从全量同步、备份时有阻塞风险
10、设置合理的 slowlog 阈值，并对其进行监控，slowlog 过多需及时报警
11、设置合理的 repl-backlog，降低主从全量同步的概率
12、设置合理的 slave client-output-buffer-limit，避免主从复制中断情况发生
13、推荐在从节点上备份，不影响主节点性能
14、不开启 AOF 或开启 AOF 配置为每秒刷盘，避免磁盘 IO 拖慢 Redis 性能
15、调整 maxmemory 时，注意主从节点的调整顺序，顺序错误会导致主从数据不一致
16、对实例部署监控，采集 INFO 信息时采用长连接，避免频繁的短连接
17、做好实例运行时监控，重点关注 expired_keys、evicted_keys、latest_fork_usec，这些指标短时突增可能会有阻塞风险
18、扫描线上实例时，记得设置休眠时间，避免过高 OPS 产生性能抖动</div>2020-11-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/41/5e/9d2953a3.jpg" width="30px"><span>zhou</span> 👍（28） 💬（4）<div>还有一个规范：不要把 Redis 当数据库使用</div>2020-11-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/8d/55/1345dff3.jpg" width="30px"><span>独自等待</span> 👍（4） 💬（2）<div>【在集合元素个数小于一定的阈值时，会使用内存紧凑型的底层数据结构进行保存，从而节省内存。例如，假设 Hash 集合的 hash-max-ziplist-entries 配置项是 1000，如果 Hash 集合元素个数不超过 1000，就会使用 ziplist 保存数据。紧凑型数据结构虽然可以节省内存，但是会在一定程度上导致数据的读写性能下降】
请问这个怎么理解，内存连续读写性能不应该更好吗？</div>2020-11-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/92/6d/becd841a.jpg" width="30px"><span>escray</span> 👍（3） 💬（0）<div>好像没怎么看到过 bigkey 的标准定义，之前误以为真的是&quot;key&quot;太大，后来才发现是 value 太大。

键值对使用规范

- key 命名规范：业务名作前缀，冒号分隔，加业务数据名，尽量避免数据库切换。key 的长度最好不超过 31（SDS结构元数据大小 1 字节）

- 避免使用 bigkey：String 类型的数据控制在 10KB 一下，集合类型的元素个数控制在 1 万以内。

- 使用高效的序列化和压缩方法：protostuff 和 kryo 优于 Java 内置的 java-build-in-serializer；如果使用 XML 或者 JSON 可以考虑压缩，snappy 或 gzip

- 使用整数对象共享池：在满足业务数据需求的前提下，尽量用整数

数据保存规范

- 使用 Redis 保存热数据
- 不同的业务数据分实例存储
- 保存数据时，设置过期时间
- 控制 Redis 实例的容量，2~6 GB

命令使用规范

- 线上禁用部分命令：KEYS、FLUSHALL、FLUSHDB
- 慎用 MONITOR
- 慎用全量操作命令

课代表 @Kaito 大神的 Redis 使用规范值得收藏。</div>2021-03-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/0d/5a/e60f4125.jpg" width="30px"><span>camel</span> 👍（1） 💬（1）<div>请问为什么特别强调sds元数据的大小？key超过32，元数据才从1到3，相对于本身key大小而言元数据不是才占很小比例吗？</div>2021-09-15</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/1d/de/62bfa83f.jpg" width="30px"><span>aoe</span> 👍（1） 💬（0）<div>非常实用，感谢老师</div>2021-04-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/41/6c/687c5dfb.jpg" width="30px"><span>叶子。</span> 👍（1） 💬（2）<div>从 Redis 3.2 版本开始，当 key 字符串的长度增加时，SDS 中的元数据也会占用更多内存空间
请问这句话怎么理解，之前讲SDS的时候说的好像是 长度和实际分配长度分别占用4B？</div>2020-11-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/22/bd/9b/366bb87b.jpg" width="30px"><span>飞龙</span> 👍（0） 💬（2）<div>实际业务中遇到过一个困扰，就是项目起初只是记录每个用户的一个标识，用了HASH，但是随便项目的飞速发展，用户数量到了5000W，导致 这个HASH里的元素上千万级别了，单这一个就占了1个多G的内存，后面也不太好根据业务分散</div>2022-08-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/0d/5a/e60f4125.jpg" width="30px"><span>camel</span> 👍（0） 💬（1）<div>请问老师，如果一个hash非常大，比如超过10w个记录，避免了hgetall也会导致阻塞很久吗？ 也就是说hget操作的性能与hash.size有没有关系，是什么复杂度的关系？（算法层面上能理解的是应该没关系，因为hash的查询操作是O(1)复杂度）</div>2021-09-15</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/23/5b/983408b9.jpg" width="30px"><span>悟空聊架构</span> 👍（0） 💬（1）<div>总结得很棒，还需要在实践中不断地总结。谢谢老师！</div>2021-05-14</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTIIMRcKFGZTZCZCmm6ibb8KrjFaXxAm90R1Uic6lpBTN0HKKGQnzto6hnyQBfTNcYEoXAnJxhRQnUEg/132" width="30px"><span>Geek_4d3b66</span> 👍（0） 💬（3）<div>就文中hash集合过大，我不明白的是hash不是key  field value吗，一个key怎么可能过大呢，是存储了上万字段吗</div>2021-04-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/7d/41/3c5b770b.jpg" width="30px"><span>喵喵喵</span> 👍（0） 💬（0）<div>打卡</div>2020-12-30</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/d4/d6/1d4543ac.jpg" width="30px"><span>云海</span> 👍（0） 💬（3）<div>建议里的Redis实例容量控制在2~6GB，这个数据是如何而来的呢，现在很多大型集群动辄几十上百G。</div>2020-11-22</li><br/>
</ul>