你好，我是徐逸。

通过上节课的学习，我们知道了提升服务吞吐的数据库架构方案。

不过在实践中，除了在数据库层面做优化之外，我们还可以通过搭配缓存的方式，来减轻数据库的访问压力，避免数据库成为性能瓶颈点。例如电商大促的商品详情页，由于商品的名称、图片链接、价格等数据会被频繁访问，因此一般会被缓存，以便提升系统的性能。

今天我们就来聊聊，在大促抢购期间，有些商品访问QPS突然大幅度增高时，我们如何才能保障Redis访问的性能不受影响呢？

## 什么是热 Key 问题

在讨论具体方案之前，你不妨先想一想：要是Redis中某个Key的访问QPS突然变得很高，会给我们的系统带来怎样的影响？

就像下面的图展示的一样，当从 Redis 读取数据时，Redis 代理服务会基于 Key 进行 Hash 计算，以此定位到 Redis 中实际存放数据的后端 Redis Server。所以，要是某个 Key 的访问 QPS 突然大幅攀升，那么这个 Key 所在的 Redis Server 就会有部分请求被迫排队，进而导致延迟升高，严重时还会出现超时失败的状况。这便是我们平常所说的热 Key 问题，而那些**被高频率访问的 Key 就是热 Key**。

![](https://static001.geekbang.org/resource/image/71/36/71fb5bb42c689ce7c4725732bfd2b336.jpg?wh=3400x2630 "图1 Redis 分片架构")

在应对突发热 Key 所引发的性能难题时，各个公司所采用的解决方案可谓是各有千秋。不过，它们的核心思路却殊途同归，那便是**借助更多的机器资源，来分担热 Key 的访问流量**。这些方案大致能够归为以下两类。
<div><strong>精选留言（6）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/1e/e9/58/7bb2c561.jpg" width="30px"><span>请务必优秀</span> 👍（1） 💬（1）<div>学到了go的golang.org&#47;x&#47;sync&#47;singleflight库，之前没有用过！老师，那么什么场景会在Redis集群和关系型数据库中间再加一层KV持久化存储（有些公司会用rocksdb+raft仿照Redis再搞一层）呢？或者什么时候会直接不用redis，直接用rocksdb+raft的那一套kv呢？这个目前业界运用的很普遍吗？是否会取代redis还是说只是各家在造无用的轮子（有一些公司号称取代redis，用rocksdb+raft造出来各种xxedis）？</div>2025-01-06</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/17/e9/26/472e16e4.jpg" width="30px"><span>Amosヾ</span> 👍（1） 💬（1）<div>数据量大的时候，本地业务缓存是否可以考虑实现类似redis集群的分布式缓存？目前业界go生态是否有一些成熟的工具可以借鉴？</div>2025-01-03</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/58/30/c8dfbe5f.jpg" width="30px"><span>cjs</span> 👍（0） 💬（1）<div>老师 。比如用了bigcache， 设置本地占用最大内存3G,  最大元素 500字节，那最多元素 3 * 1024 * 1024  * 1024 &#47; 500  约等于 6000w 数据，在存储量这么大情况下，热key 被替换的概率感觉会比较低，所以热key发现还有必要么</div>2025-01-07</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/27/19/fe/d31344db.jpg" width="30px"><span>lJ</span> 👍（0） 💬（1）<div>1. 业务层解决方案=&gt;本地缓存部分数据中，采用本地缓存的 LRU策略或过期策略来管理缓存是否可行呢
2. Proxy 热 Key 承载方案 =&gt;同一个客户端会被同一个proxy处理吗
3. 这些方案对旧数据的容忍度是怎么样的呢，在数据一致性方面，各个方案适用的业务场景有哪些注意点呢
4. 思考题：https:&#47;&#47;pkg.go.dev&#47;golang.org&#47;x&#47;sync&#47;singleflight，大并发请求的场景，而且这些请求都是读请求时，可以把这些请求合并为一个请求
</div>2025-01-03</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/17/11/a0/085f8747.jpg" width="30px"><span>『WJ』</span> 👍（0） 💬（1）<div>识别出来热key以后呢</div>2025-01-03</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/7f/d3/b5896293.jpg" width="30px"><span>Realm</span> 👍（0） 💬（1）<div>带缓冲区的通道.</div>2025-01-03</li><br/>
</ul>