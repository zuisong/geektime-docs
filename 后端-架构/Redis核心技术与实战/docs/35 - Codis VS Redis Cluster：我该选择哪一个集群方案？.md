你好，我是蒋德钧。

Redis的切片集群使用多个实例保存数据，能够很好地应对大数据量的场景。在[第8讲](https://time.geekbang.org/column/article/275337)中，我们学习了Redis官方提供的切片集群方案Redis Cluster，这为你掌握切片集群打下了基础。今天，我再来带你进阶一下，我们来学习下Redis Cluster方案正式发布前，业界已经广泛使用的Codis。

我会具体讲解Codis的关键技术实现原理，同时将Codis和Redis Cluster进行对比，帮你选出最佳的集群方案。

好了，话不多说，我们先来学习下Codis的整体架构和流程。

## Codis的整体架构和基本流程

Codis集群中包含了4类关键组件。

- codis server：这是进行了二次开发的Redis实例，其中增加了额外的数据结构，支持数据迁移操作，主要负责处理具体的数据读写请求。
- codis proxy：接收客户端请求，并把请求转发给codis server。
- Zookeeper集群：保存集群元数据，例如数据位置信息和codis proxy信息。
- codis dashboard和codis fe：共同组成了集群管理工具。其中，codis dashboard负责执行集群管理工作，包括增删codis server、codis proxy和进行数据迁移。而codis fe负责提供dashboard的Web操作界面，便于我们直接在Web界面上进行集群管理。
<div><strong>精选留言（30）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/0f/90/8a/288f9f94.jpg" width="30px"><span>Kaito</span> 👍（183） 💬（20）<div>假设 Codis 集群中保存的 80% 的键值对都是 Hash 类型，每个 Hash 集合的元素数量在 10 万 ～ 20 万个，每个集合元素的大小是 2KB。迁移一个这样的 Hash 集合数据，是否会对 Codis 的性能造成影响？

不会有性能影响。

Codis 在迁移数据时，设计的方案可以保证迁移性能不受影响。

1、异步迁移：源节点把迁移的数据发送给目标节点后就返回，之后接着处理客户端请求，这个阶段不会长时间阻塞源节点。目标节点加载迁移的数据成功后，向源节点发送 ACK 命令，告知其迁移成功。

2、源节点异步释放 key：源节点收到目标节点 ACK 后，在源实例删除这个 key，释放 key 内存的操作，会放到后台线程中执行，不会阻塞源实例。（没错，Codis 比 Redis 更早地支持了 lazy-free，只不过只用在了数据迁移中）。

3、小对象序列化传输：小对象依旧采用序列化方式迁移，节省网络流量。

4、bigkey 分批迁移：bigkey 拆分成一条条命令，打包分批迁移（利用了 Pipeline 的优势），提升迁移速度。

5、一次迁移多个 key：一次发送多个 key 进行迁移，提升迁移效率。

6、迁移流量控制：迁移时会控制缓冲区大小，避免占满网络带宽。

7、bigkey 迁移原子性保证（兼容迁移失败情况）：迁移前先发一个 DEL 命令到目标节点（重试可保证幂等性），然后把 bigkey 拆分成一条条命令，并设置一个临时过期时间（防止迁移失败在目标节点遗留垃圾数据），迁移成功后在目标节点设置真实的过期时间。

Codis 在数据迁移方面要比 Redis Cluster 做得更优秀，而且 Codis 还带了一个非常友好的运维界面，方便 DBA 执行增删节点、主从切换、数据迁移等操作。

我当时在对 Codis 开发新的组件时，被 Codis 的优秀设计深深折服。当然，它的缺点也很明显，组件比较多，部署略复杂。另外，因为是基于 Redis 3.2.8 做的二次开发，所以升级 Redis Server 比较困难，新特性也就自然无法使用。

现在 Codis 已经不再维护，但是作为国人开发的 Redis 集群解决方案，其设计思想还是非常值得学习的。也推荐 Go 开发者，读一读 Codis 源码，质量非常高，对于 Go 语言的进阶也会有很大收获！</div>2020-11-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/cf/81/96f656ef.jpg" width="30px"><span>杨逸林</span> 👍（16） 💬（1）<div>我简单用 Google 搜了下，主流的 Redis 集群方案大概分为三种：
1. Redis Cluster
2. 大厂&#47;小项目组 开源的解决方案—— Twitter 开源的 Twemproxy、Codis
3. 买专有的 Redis 服务器—— Aliyun AparaCache（这个开源的没有 slot 的实现）、AWS ElasticCache

第二种的话，我看了下他们的 Github 对应的 Repository，上一次更新是两年前。现在要好用（能用 Redis 的新特性，并且能轻松扩容）的集群方案，只能自研或者买云厂商的吗？

主要参考了这三个
https:&#47;&#47;cloud.tencent.com&#47;developer&#47;article&#47;1701574
https:&#47;&#47;www.cnblogs.com&#47;me115&#47;p&#47;9043420.html
https:&#47;&#47;www.zhihu.com&#47;question&#47;21419897

第一个页面是转载自 Kaito 的个人博客网站，我是想不到的，对应的页面上有人说方案太老了。
顺便提一下，我的也是用的 Hexo，也是基于 Next 主题改的������。</div>2020-11-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/b4/76/5ca1718e.jpg" width="30px"><span>天气</span> 👍（11） 💬（1）<div>redis cluster怎么使用都没介绍啊</div>2020-12-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/11/a3/7a2405ca.jpg" width="30px"><span>rfyiamcool</span> 👍（7） 💬（1）<div>不建议使用codis，redis的版本太老，在很多特性和性能上都有体现，codis在大流量下性能衰减很厉害，另外codis的管道有性能和兼容问题。</div>2021-05-17</li><br/><li><img src="" width="30px"><span>Geek_f00f74</span> 👍（6） 💬（0）<div>迁移的数据会被设置为只读，如果迁移过程中，有对迁移数据的写操作，会导致redis读写线程阻塞吗？</div>2020-11-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/92/6d/becd841a.jpg" width="30px"><span>escray</span> 👍（5） 💬（0）<div>在阅读本文之前，我的想法是，如果条件允许，主要是 Redis 的版本，另外还有业务需要，当然是选择 Redis Cluster 官方的集群方案。

Codis 有 1024 个逻辑槽 Slot，客户端读取时，使用 CRC32 算法计算 key 的哈希值，并且对 1024 取模，余数对应 slot 编号，再通过 Slot 和 server 的对应关系，找到数据所在服务器。

数据路由表由 Codis dashboard 配置，保存在 codis proxy 上，同时也保存在 Zookeeper 中。

Redis Cluster 有 16384 个哈希槽 Hash Slot，采用 CRC16 算法计算哈希值，对 16384 取模。数据路由表通过实例间相同通信传递，每个实例上保存一份。

从老师的推荐来看，是比较偏爱 Codis 的，但是 Codis 似乎不再更新了。

对于课后题，20 万个 2KB 元素的 Hash 类型数据，应该已经算是 bigkey 了，迁移这样的 Hash 集合数据，如果采用 Codis 的异步迁移，感觉似乎问题不大。如果是读多写少的缓存应用，应该就更没有问题了。

看了课代表的提醒，才知道 Codis 是 Go 语言开发的，最近正准备入坑 Let&#39;s Go</div>2021-04-03</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/0a/a4/828a431f.jpg" width="30px"><span>张申傲</span> 👍（5） 💬（0）<div>老师好~ 目前公司在用twemproxy维护Redis集群，能简单对比下codis和twemproxy的优劣吗？</div>2020-11-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/77/a5/c5ae871d.jpg" width="30px"><span>zenk</span> 👍（3） 💬（1）<div>只读时间会不会太长导致key不可写</div>2020-12-02</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/92/d5/699384a0.jpg" width="30px"><span>yeek</span> 👍（3） 💬（0）<div>有几个疑问：
1、对于迁移过程中，codis的只读特性，对于集合类型，是整个key只读，还是已迁移的部分是只读的；
2、codis分批迁移的过期时间是怎么设置的，太长会长期驻留，太短会在迁移过程中失效么？
3、codis使用zk保存多proxy信息，那么客户端本地会缓存多proxy信息吗？从而选择不同proxy进行连接</div>2020-11-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/fb/86/a380cbad.jpg" width="30px"><span>柳磊</span> 👍（2） 💬（1）<div>关于“集群客户端需要重新开发吗?”有点疑问，虽然codis proxy 是和单实例客户端兼容的，但应该不支持codis proxy的HA吧？我看codis官方文档中提到，需要使用Jodis 客户端（在Jedis增加了codis proxy HA），所以我理解生产级的使用还是需要换客户端的吧？
</div>2021-01-25</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/29/42/43d4b1a8.jpg" width="30px"><span>烫烫烫</span> 👍（2） 💬（2）<div>我觉得会有影响。每个Hash集合元素数量以15万来算，则大小为 15w * 2KB = 300MB，如果是千兆网，耗时约300 &#47; (1000 &#47; 8) ≈ 2.4s。尽管迁移时bigkey会被拆分传输，但传输过程中数据是只读的，写操作还是会被阻塞，所以会有影响。</div>2020-11-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/2d/f6/9f/d7485d6a.jpg" width="30px"><span>Furious</span> 👍（0） 💬（0）<div>其实目前来讲，codis相对redis cluster的优势也没了，codis年代太久远了，上一次更新已经是2018年，到现在2024年都已经6年了，应用上redis cluster更加成熟了，而且官方推出的稳定性更可靠，至于说客户端，目前太多客户端都支持集群命令了，并不需要重新开发了，而数据迁移，redis基本上都是用作缓存的，不会有太多的数据迁移。所以目前cluster就是最优解了</div>2024-07-05</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/43/ce/a3734a6c.jpg" width="30px"><span>杨过</span> 👍（0） 💬（0）<div>sss</div>2023-01-06</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1b/65/b7/058276dc.jpg" width="30px"><span>i_chase</span> 👍（0） 💬（0）<div>迁移过程中，一个slot的数据会分布在两个节点，查询key的时候，codis怎么知道去哪里查？不是和redis 官方cluster一样得查询两次吗？</div>2022-11-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/22/bd/9b/366bb87b.jpg" width="30px"><span>飞龙</span> 👍（0） 💬（0）<div>还没有用过redis cluster</div>2022-08-16</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/5c/3f/a263f551.jpg" width="30px"><span>倚天照海</span> 👍（0） 💬（0）<div>redis按slot进行数据迁移时，如何知道哪些key是属于该slot的呢？</div>2022-02-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/47/00/3202bdf0.jpg" width="30px"><span>piboye</span> 👍（0） 💬（0）<div>总感觉redis 的 cluster 不靠谱</div>2022-02-18</li><br/><li><img src="" width="30px"><span>Geek_064e72</span> 👍（0） 💬（0）<div>redis客户不直接连接redis cluster，而是连接redis cluster proxy， 由redis cluster proxy真正请求后台的redis cluster server，并且处理MOVED请求，这样又是一种集群方案，而且还不用zookeeper了。</div>2022-02-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/28/6e/e4/9901994d.jpg" width="30px"><span>Geek_9bd7ef</span> 👍（0） 💬（1）<div>请问下 老师  关于 ”在 Redis Cluster 中，数据路由表是通过每个实例相互间的通信传递的，最后会在每个实例上保存一份“这里的 路由表信息在各个实例之间的一致性是怎么保证的呢~？</div>2022-01-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/19/d9/ff/b23018a6.jpg" width="30px"><span>Heaven</span> 👍（0） 💬（0）<div>我觉着不会造成影响,因为在Codis中,对于bigkey的迁移,是异步且拆分的,将集合对象拆分为更为细粒度的单个对象进行传输,避免了传输过程中的阻塞问题</div>2021-09-01</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/PiajxSqBRaELZPnUAiajaR5C25EDLWeJURggyiaOP5GGPe2qlwpQcm5e3ybib8OsP4tvddFDLVRSNNGL5I3SFPJHsA/132" width="30px"><span>null</span> 👍（0） 💬（0）<div>原文：
我给你举个例子，假如我们要迁移一个有 1 万个元素的 List 类型数据，当使用异步迁移时，源 server 就会给目的 server 传输 1 万条 RPUSH 命令，每条命令对应了 List 中一个元素的插入。在目的 server 上，这 1 万条命令再被依次执行，就可以完成数据迁移。

有2个疑问：
1. 源 server 如何确认 bigkey 迁移完成，然后删除 bigkey？
文章提到，在迁移完成之前，在目标 server 的中间状态的数据，是有过期时间的，因此不可能迁移 bigkey 一个元素，就在源 server 删除 bigkey 对应的元素。
就上述例子，应该是源 server 在自行维护一万条命令的 ack，判断 ack 的数量和迁移命令数量一致，则认为 bigkey 迁移完成。是这样么？

2. 这一万条 RPUSH 命令，如何保证顺序吖，即迁移之后，List 链表元素的顺序和迁移之前是一致的？
这一万条命令对应一万次 request，比如其中一个 request 网络延迟，后面的 request 先到达目的 server。
还是说必须要等前面命令的 request ack 后，才发送下一条 RPUSH 命令的 request 请求？

谢谢老师！！</div>2021-06-05</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/2a/ff/a9d72102.jpg" width="30px"><span>BertGeek</span> 👍（0） 💬（0）<div>请问老师，codies数据迁移，将binkey拆分以元素迁移，是整个binkey迁移完就可以读写，还是说，迁移一部分就可以再目标server访问，返回ack，删除binkey 迁移过的元素信息</div>2021-06-02</li><br/><li><img src="" width="30px"><span>Geek_7bb784</span> 👍（0） 💬（1）<div>redis cluster有16384个slot，codis有1024个。相同数据量的情况下，cluster中每个slot中的数据量更小，在数据迁移的时候难道不比codis更有效率嘛？

作者是否可以提供相同数据量情况下，codis扩容和cluster扩容的性能对比数据呢？</div>2021-05-30</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/db/79/9426c6ce.jpg" width="30px"><span>Super~琪琪</span> 👍（0） 💬（1）<div>老师我看这个codis 现在最新的版本也是在2018年，这个项目是不是已经被放弃了？</div>2021-05-07</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTLn1rhQ7nlmQgyEZhgfgH0s9BicusXhTG7J6Tcxib2oDVoKVTbia9CcNIkicj2L2a2xqQRicF4FhPepjqA/132" width="30px"><span>Geek_8cf0a3</span> 👍（0） 💬（0）<div>数据迁移的过程中，一个slot中的一部分数据在新server，另一部分在旧server，proxy如果接到对这个slot中的数据的读取请求，怎么知道数据在哪个server里？</div>2021-02-04</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/81/e6/6cafed37.jpg" width="30px"><span>旅途</span> 👍（0） 💬（1）<div>老师 我像问一下codis集群的入口网关在哪？proxy不是可以有多个,配置哪个?</div>2020-12-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/dd/9b/0bc44a78.jpg" width="30px"><span>yyl</span> 👍（0） 💬（0）<div>采用异步迁移影响不大，采用同步迁移会有影响</div>2020-11-22</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTIiatbibYU9p7aVpq1o47X83VbJtsnP9Dkribian9bArLleibUVMDfD9S0JF9uZzfjo6AX5eR6asTiaYkvA/132" width="30px"><span>倪大人</span> 👍（0） 💬（0）<div>“第二个特点是，对于 bigkey，异步迁移采用了拆分指令的方式进行迁移。具体来说就是，对 bigkey 中每个元素，用一条指令进行迁移，而不是把整个 bigkey 进行序列化后再整体传输。”

求问老师，拆分迁移bigKey的时候，源server上的这个key是不是也是只读，不允许修改？
如果是的话，那迁移的过程中这个key的修改请求会被阻塞，性能会受到影响？
如果不是的话，怎么保证数据一致性呢？</div>2020-11-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/ec/a7/7d44c655.jpg" width="30px"><span>snailshen</span> 👍（0） 💬（1）<div>老师，codis的key和slot的映射是crc16,并且zookeeper保存的元数据信息，只是proxy的信息，并不存储slot信息吧</div>2020-11-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/54/9a/76c0af70.jpg" width="30px"><span>每天晒白牙</span> 👍（0） 💬（2）<div>通过学完这篇文章，个人感觉集群更倾向于 Codis</div>2020-11-11</li><br/>
</ul>