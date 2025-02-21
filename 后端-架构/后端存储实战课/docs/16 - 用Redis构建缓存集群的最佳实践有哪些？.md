你好，我是李玥。

之前连续几节课，我们都在以MySQL为例子，讲如何应对海量数据，如何应对高并发，如何实现高可用，我先带你简单复习一下。

- 数据量太大查询慢怎么办？存档历史数据或者分库分表，这是数据分片。
- 并发太高扛不住怎么办？读写分离，这是增加实例数。
- 数据库宕机怎么办？增加从节点，主节点宕机的时候用从节点顶上，这是主从复制。但是这里面要特别注意数据一致性的问题。

我在之前课程中，也多次提到过，**这些方法不仅仅是MySQL特有的，对于几乎所有的存储系统，都是适用的。**

今天这节课，我们来聊一聊，如何构建一个生产系统可用的Redis缓存集群。你将会看到，几种集群解决方案用到的思想，基本和我们上面讲的都是一样的。

## Redis Cluster如何解决数据量大、高可用和高并发问题？

Redis从3.0版本开始，提供了官方的集群支持，也就是Redis Cluser。**Redis Cluster相比于单个节点的Redis，能保存更多的数据，支持更多的并发，并且可以做到高可用，在单个节点故障的情况下，继续提供服务。**

为了能够保存更多的数据，和MySQL分库分表的方式类似，Redis Cluster也是通过分片的方式，把数据分布到集群的多个节点上。
<div><strong>精选留言（24）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/16/e7/76/79c1f23a.jpg" width="30px"><span>李玥</span> 👍（49） 💬（4）<div>Hi，我是李玥。

这里回顾一下上节课的思考题：

课后请你想一下，把订单表拆分之后，那些和订单有外键关联的表，该怎么处理？

对于这些表，我的建议是，和订单表一起拆分，让相同订单ID的订单和关联表的数据分布到相同的分片上，这样便于查询。</div>2020-04-03</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/dc/b8/31c7e110.jpg" width="30px"><span>LVM_23</span> 👍（54） 💬（1）<div>老师你好，想问个问题。redis的list内元素的单独过期怎么做，而不是整个list过期。 网上都是用时间戳存，然后用定时任务来清除。有其他的方案吗? 写入频繁的，谢谢老师解答了</div>2020-05-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/36/d2/c7357723.jpg" width="30px"><span>发条橙子 。</span> 👍（19） 💬（3）<div>老师 有两个疑问点

1.  大厂自建集群 是不是就是常说的使用一致性哈希来做槽的映射

2. 既然自带集群包含了哨兵， 代理也包含 ，是不是哨兵的功能也是在自建中使用 ，还是大厂自建的也不用哨兵 是自己做的高可用</div>2020-04-03</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/0e/39/174741d1.jpg" width="30px"><span>特种流氓</span> 👍（14） 💬（1）<div>redis cluster集群 是不是就没有哨兵的概念了</div>2020-04-02</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/c6/00/683bb4f0.jpg" width="30px"><span>正在减肥的胖籽。</span> 👍（11） 💬（1）<div>请教老师一个问题：
 1.redis集群新增分片后，线上怎么实现好的平滑迁移？这个一直没有想到好的解决方法</div>2020-04-02</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1a/af/0e/ac955022.jpg" width="30px"><span>申学晋</span> 👍（7） 💬（1）<div>redis6.0的官方集群代理和客户端缓存是不是可以把您讲的两种方案结合使用？</div>2020-05-15</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/ce/db/9dba29ea.jpg" width="30px"><span>暴君•熊</span> 👍（6） 💬（1）<div>老师，最后介绍的定制客户端模式来保存分片表。那redis的服务端不需要动嘛？当有新增或者删除节点的时候，服务端内部不还是需要使用流言来传播一次嘛？</div>2020-04-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/c7/52/c5adf218.jpg" width="30px"><span>喜欢地球的阿培同学</span> 👍（3） 💬（1）<div>老师，您好，问一个问题。最后介绍的定制客户端模式。是不是这些redis是一个一个节点，并没有一起组成一个集群。如果这些redis组成一个集群的话，那岂不是每次新增和删除redis节点时，也会流言传播一次吗？</div>2020-05-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/bb/61/2c2f5024.jpg" width="30px"><span>haijian.yang</span> 👍（8） 💬（0）<div>阿里云有个 redis 方案，冷数据存磁盘，热数据放在内存。</div>2020-04-02</li><br/><li><img src="https://wx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTJkwbyTYtSCx6Qc7cQPnnRWv38Jybh3etziaPmuP8gHcgS6FMxcdftrKgWiamH6fc2iciaicDKDVEwcEibQ/132" width="30px"><span>sami</span> 👍（3） 💬（0）<div>cluster命令是受限的，跟mysql的分库分表一样，有一些场景也是无法支持</div>2020-04-02</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1a/9d/81/d748b7eb.jpg" width="30px"><span>千锤百炼领悟之极限</span> 👍（1） 💬（0）<div>小规模集群适合使用Redis Cluster，适合几个到几十个节点的规模。

为什么不适合大规模的集群? 因为Redis Cluster使用了一种去中心化设计的Gossip（流言）协议，用于节点之间更新映射表。

如果集群的节点数量多，更新映射表速度较慢，导致数据同步等问题。</div>2022-03-03</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/df/bf/f90caa79.jpg" width="30px"><span>椿</span> 👍（1） 💬（0）<div>最后一种集群方案，感觉有点类似于sharding sphere这样的中间件，客户端读取元数据然后路由到具体的redis实例请求</div>2020-05-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/34/df/64e3d533.jpg" width="30px"><span>leslie</span> 👍（1） 💬（1）<div>其实这也反向提出了另一个问题mysql cluster的问题：其自身同样有cluster,可是真实环境下很少企业会去用mysql cluster；都是各自运用自己的方案去做集群，方案之前的课程中都有提及就不提了。
自身的cluster在实际生产中极少被某些数据库使用这大概算是一大特点，尤其像我们所常见的mysql、redis、以及后面新出来的、、、</div>2020-04-02</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/26/eb/d7/90391376.jpg" width="30px"><span>ifelse</span> 👍（0） 💬（0）<div>还有一个小问题需要注意的是，这几种集群方案对一些类似于“KEYS”这类的多 KEY 命令，都没法做到百分百支持。--记下来</div>2022-12-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/26/eb/d7/90391376.jpg" width="30px"><span>ifelse</span> 👍（0） 💬（0）<div>学习打卡</div>2022-12-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/f3/83/e2612d81.jpg" width="30px"><span>锐</span> 👍（0） 💬（0）<div>定制客户端这个方案，客户端缓存元数据，当集群中机器发生变化时，是通过zookeeper通知客户端更新元数据吗</div>2021-03-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/21/0a/78/5ac3666f.jpg" width="30px"><span>Lynn</span> 👍（0） 💬（1）<div>老师你好，假如两个key计算出来的槽是同一个，那是以链表的方式保存到槽里面吗？</div>2020-09-05</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/75/6b/fd685164.jpg" width="30px"><span>lcf枫</span> 👍（0） 💬（0）<div>老师 redis cluster 的高可用应该是有两方面来保证的吧？中从库 + 哨兵帮助监控切换</div>2020-08-16</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/18/fa/dd/f640711f.jpg" width="30px"><span>哈德韦</span> 👍（0） 💬（0）<div>请问下老师，跨数据中心的 Redis 数据同步有没有最佳实践？比如用户的登录信息Session数据缓存在Redis，那么国内集群和海外集群怎么同步呢？</div>2020-07-31</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1f/4c/3f/5a343ddd.jpg" width="30px"><span>远航</span> 👍（0） 💬（0）<div>老师您好，如果系统部署在两个机房，1:1部署业务，redis采用何种部署方式？两个机房需要保证redis的数据一致性</div>2020-07-03</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/10/bb/f1061601.jpg" width="30px"><span>Demon.Lee</span> 👍（0） 💬（0）<div>老师，请教一下：
我们现在做redis小规模的高可用，只有3台机器，部署的就是redis cluster集群，一共部署了6个实例，3个master，3个slave（错开部署，A机器上master1, slave3; B 机器上 master2, slave1; C 机器上master 3, slave2 这样）。
我测试时，把A机器上的两个实例停掉，java jedis客户端连接报错一会后，就正常了；然后我把A恢复，再把B机器上的两个实例停掉，java jedis客户端连接报错就无法恢复正常了（错误：throw new JedisClusterMaxRedirectionsException(&quot;Too many Cluster redirections?&quot;)），重启java服务也无效。然后我通过CLUSTER NODES命令看到B机器上的两个实例都是master （fail， disconnectd状态）。

我理解是第一次停止A机器上实例的时候，master漂到B机器上了，然后停止B机器上实例的时候，master没有漂到其他机器上，不清楚为什么？
同事建议换哨兵模式，我自己想了一下，觉得哨兵好像更靠谱些，但我看老师说哨兵已经慢慢过时了，且redis cluster已经有哨兵的功能了，请老师针对我这种场景，给点意见，谢谢。</div>2020-07-02</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1b/73/43/ae139b1f.jpg" width="30px"><span>博</span> 👍（0） 💬（0）<div>老师，redis的key 有什么统一的设计规范吗，看到好多都是与数据库表相对应的方式</div>2020-06-05</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/81/e6/6cafed37.jpg" width="30px"><span>旅途</span> 👍（0） 💬（1）<div>老师,为什么redis没有事务同步就不需要binlog了?</div>2020-05-04</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/0c/0f/93d1c8eb.jpg" width="30px"><span>mickey</span> 👍（0） 💬（0）<div>HDFS分片、复制和高可用原理基本一样，机架感知是独创。</div>2020-04-20</li><br/>
</ul>