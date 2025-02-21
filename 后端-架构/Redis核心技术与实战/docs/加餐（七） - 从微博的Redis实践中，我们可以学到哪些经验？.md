你好，我是蒋德钧。

我们知道，微博内部的业务场景中广泛使用了Redis，积累了大量的应用和优化经验。微博有位专家曾有过一个[分享](https://mp.weixin.qq.com/s?__biz=MzI4NTA1MDEwNg%3D%3D&mid=2650782429&idx=1&sn=7f2df520a7295a002c4a59f6aea9e7f3&chksm=f3f90f48c48e865e478d936d76c5303663c98da506f221ede85f0f9250e5f897f24896147cfb&scene=27#wechat_redirect)，介绍了Redis在微博的优化之路，其中有很多的优秀经验。

俗话说“他山之石，可以攻玉”，学习掌握这些经验，可以帮助我们在自己的业务场景中更好地应用Redis。今天这节课，我就结合微博技术专家的分享，以及我和他们内部专家的交流，和你聊聊微博对Redis的优化以及我总结的经验。

首先，我们来看下微博业务场景对Redis的需求。这些业务需求也就是微博优化和改进Redis的出发点。

微博的业务有很多，例如让红包飞活动，粉丝数、用户数、阅读数统计，信息流聚合，音乐榜单等，同时，这些业务面临的用户体量非常大，业务使用Redis存取的数据量经常会达到TB级别。

作为直接面向终端用户的应用，微博用户的业务体验至关重要，这些都需要技术的支持。我们来总结下微博对Redis的技术需求：

- 能够提供高性能、高并发的读写访问，保证读写延迟低；
- 能够支持大容量存储；
- 可以灵活扩展，对于不同业务能进行快速扩容。

为了满足这些需求，微博对Redis做了大量的改进优化，概括来说，既有对Redis本身数据结构、工作机制的改进，也基于Redis自行研发了新功能组件，包括支持大容量存储的RedRock和实现服务化的RedisService。
<div><strong>精选留言（11）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/0f/90/8a/288f9f94.jpg" width="30px"><span>Kaito</span> 👍（105） 💬（6）<div>在实际应用 Redis 时，你有哪些优化和二次开发的经验？

分享一下我们对 Redis 的二次开发经验。

由于我们采用的 Redis 集群方案是 Codis，我们主要对 Codis 下的 Redis Server 进行了二次开发。

我们在做服务跨机房容灾和多活时，需要在两个机房各自部署 Codis&#47;Redis 实例，并且两个机房的实例数据需要实时同步，以支持任意机房故障时，可随时切换应用流量到另一个机房继续提供服务。

但由于两个机房之间的网络是通过专线连通的，而专线的质量和稳定性是不如同机房内的，如果使用原生 的 Redis 主从复制方案，当专线长时间故障再恢复时，原生 Redis 主从复制会进行全量的数据同步。全量同步不仅对 master 节点有阻塞风险，同时也会对机房之间的专线的带宽产生巨大的压力，还会影响应用的机房流量切换。

所以我们对 Codis 下的 Redis 做了二次开发，对其增加了类似于 MySQL 的 binlog 模块，把实时的写命令通过异步线程写入到 binlog 文件中，然后开发了数据同步中间件去读取 Redis 的 binlog，向另一个机房实时同步数据，并且支持增量同步、断点续传，这样就可以兼容专线任意时间的故障，故障恢复后我们的同步中间件会从断点处继续增量同步 Redis 数据到另一个机房，避免了全量复制的风险。

同时，我们还对 Codis 进行了二次开发，在集成数据同步中间件时，兼容了 Codis 的日常运维和故障容错，例如集群内节点主从切换、故障转移、数据迁移等操作，保证了机房之间数据同步的最终一致性。

最后，我想说的是，对 Redis 进行改造，优点是可以更加适配自己的业务场景，但缺点是维护和升级成本较高，改造 Redis 相当于自己开辟了一个新的分支，公司内部需要投入人力去持续维护，需要平衡投入产出比。如果没有特别复杂的需求，一般使用官方版本即可，好处是可以第一时间使用最新版本的特性。</div>2020-11-30</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/dd/9b/0bc44a78.jpg" width="30px"><span>yyl</span> 👍（2） 💬（1）<div>问题：微博采用的集群部署方案，不是Redis cluster？是自研的吗？</div>2020-11-30</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/92/6d/becd841a.jpg" width="30px"><span>escray</span> 👍（8） 💬（5）<div>顺着专栏给的链接，先去看了《万亿级日访问量下，Redis在微博的9年优化历程 》，虽然没有机会面对类似微博这样的体量（2019年 100T+ 存储、1000+ 台物理机、10000+ Redis实例、万亿级读写、响应时间 20 毫秒），但是也算是大开眼界。

其实原文中的那个缓存、存储、队列技术选型流程图，就很有价值。

分享的很多内容不明觉厉，结合专栏的解析来看，可以感觉到微博团队在 Redis 运维方面做的比较深入。有一点疑问就是，基于 Redis 的早期版本做了很多二次开发，那么是否能够和 Redis 的新版本兼容？或者说是否反馈回了开源社区？

老师最后总结的业务纵切、平台横切很有高屋建瓴的味道，当然，最终还是要靠代码实践。

有一点好奇，一般分享都是大厂如何在高性能、大容量和可扩展方面应用 Redis，有没有人分享过“小厂”是如何使用 Redis，直接拿开源版本上生产环境么？可能也够用。

希望以后有机会能回答课后题中关于 Redis 的优化和二次开发的问题。</div>2021-03-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/8f/cf/890f82d6.jpg" width="30px"><span>那时刻</span> 👍（4） 💬（0）<div>请问老师，在冷热数据处理的图例中，异步读取冷数据，是直接从IO队列读取，这是异步处理线程发送读取命令后，然后从IO队列读取么？
另外，如果需要读冷数据，是把冷数据再放回redis变成热数据么？</div>2020-11-30</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/23/5b/983408b9.jpg" width="30px"><span>悟空聊架构</span> 👍（2） 💬（1）<div>微博的 Redis 分享很棒，一直都觉得微博是个很厉害的平台。
另外老师总结得也很到位，更容易理解。</div>2021-05-30</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/dd/9b/0bc44a78.jpg" width="30px"><span>yyl</span> 👍（2） 💬（0）<div>问题：冷热数据的迁移，是怎么操作的？由后台根据访问量自行迁移吗？</div>2020-11-30</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/16/6c/26fc96c4.jpg" width="30px"><span>cloud</span> 👍（0） 💬（1）<div>老师能展开说下longset是如何实现的吗？
用数组的话，hash冲突后是怎么解决的</div>2023-12-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/89/dc/756ca2b5.jpg" width="30px"><span>学习</span> 👍（0） 💬（0）<div>用户关注列表定制了longest这块，为什么不直接使用set结构？</div>2023-03-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/22/bd/9b/366bb87b.jpg" width="30px"><span>飞龙</span> 👍（0） 💬（0）<div>对redis还没有二次开发过，感觉官方提供的能够完全使用都可以满足一般公司的业务需求</div>2022-08-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/33/74/d9d143fa.jpg" width="30px"><span>silentyears</span> 👍（0） 💬（1）<div>请问，“在 AOF 日志写入刷盘时，用额外的 BIO 线程负责实际的刷盘工作”这句话，额外的BIO线程是什么意思？</div>2021-02-16</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/dd/9b/0bc44a78.jpg" width="30px"><span>yyl</span> 👍（0） 💬（0）<div>一个机房作为另一个机房的热备？</div>2020-11-30</li><br/>
</ul>