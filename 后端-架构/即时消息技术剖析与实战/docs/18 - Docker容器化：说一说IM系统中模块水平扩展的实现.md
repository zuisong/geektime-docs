你好，我是袁武林。

在[第10讲“自动智能扩缩容：直播互动场景中峰值流量的应对”](https://time.geekbang.org/column/article/137000)中，我较为系统地讲解了直播场景中突发流量的应对策略。其中比较重要的一点就是：当有热点流量进来时，我们能够通过监控指标对服务进行快速扩缩容。

而快速扩缩容的一个重要前提，就是部署的服务和资源能够做到水平扩展。

那么，今天我们就来聊一聊服务和资源水平扩展的实现问题。

## 垂直扩展

首先从水平扩展(Scale out)的概念说起吧。

要解释水平扩展是什么，我们要先了解下与水平扩展相对应的另一个概念：垂直扩展（Scale up）。只有通过这两者可行性和实现层面的对比，我们才能更好地理解为什么水平扩展能力对于实现一个架构良好的系统如此重要。

当业务的用户量随着产品迭代不断增长时，相应的后端资源和服务器的压力也在逐渐加大。而解决资源和服务器瓶颈一个有效且较快的方式就是：提升资源服务器和应用服务器的单机处理能力，也就是对资源服务器和应用服务器进行“垂直扩展”。

### 提升单机硬件性能

要对资源和服务进行垂直扩展，一个简单粗暴但也比较有效的方式就是：增强单机服务器的性能。

比如：对CPU出现瓶颈的服务器进行升级，增加CPU核数和主频；对于网卡有瓶颈的服务器，升级到万兆网卡并接入到万兆交换机下；内存出现瓶颈导致系统吃Swap的情况，我们也可以将内存升级到更高配置来进行垂直扩展。一般情况下，通过对服务器硬件的升级，往往能快速解决短期的系统瓶颈问题。
<div><strong>精选留言（23）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/14/34/df/64e3d533.jpg" width="30px"><span>leslie</span> 👍（17） 💬（1）<div>    老师：目前有没有什么不错的开源IM项目可以学习和研究？</div>2019-10-07</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/6b/f8/b4da7936.jpg" width="30px"><span>大魔王汪汪</span> 👍（13） 💬（2）<div>老师的课程应该是最近半年极客时间最棒的啦！其他的竟是些概念理论的泛泛而谈😜</div>2019-10-07</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/3d/02/ecdb4e66.jpg" width="30px"><span>东东🎈</span> 👍（8） 💬（1）<div>老师，如果遇到ddos攻击，有啥处理方案吗？</div>2019-10-07</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/8d/6c/0c2a26c7.jpg" width="30px"><span>clip</span> 👍（6） 💬（1）<div>用分片来做水平扩展的话灵活性是低的吧，是不是不适合随着每天波峰、波谷来调整？感觉只能扩很难收。
如果某个时段有大量写入，用什么方式应对比较合适呢？</div>2019-10-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/7b/57/a9b04544.jpg" width="30px"><span>QQ怪</span> 👍（5） 💬（2）<div>可以分库分表来解决单表写入数据量大，查询时间过长，但实现其复杂性也增加了，需要实现分区键或者说以什么依据来进行分库分表</div>2019-10-07</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/18/b2/c9/b414a77c.jpg" width="30px"><span>HelloTalk</span> 👍（4） 💬（1）<div>要想解决资源层的写入瓶颈，除了分片机制外，还可以移步写 用队列来操作 </div>2019-10-07</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/jXbwicoDwia7ooDfwBTRyvNYQkefnVwF1CMicMS8FqKfuFAdvVZo2pqc4ic0R9kSdHTIxaE6YyqxwX8BdNGv5PqSIw/132" width="30px"><span>kamida</span> 👍（3） 💬（5）<div>老师 请问长链接请求是怎么从lvs转到网关的啊。  是接入服务先返回给用户一个网关地址 然后用户直接长链接到那个网关的吗</div>2020-03-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/92/9d/9fe6c5a9.jpg" width="30px"><span>面爸</span> 👍（3） 💬（1）<div>人数统计的话，应该用redis就可以实现，写入的话，可以队列，异步去写</div>2019-10-07</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/80/98/5591d99d.jpg" width="30px"><span>唯我天棋</span> 👍（2） 💬（1）<div>1.连接层和业务层之间增加一个业务代理，这样连接层可以更加专注于处理连接问题，让业务代理来完成服务发现，管理业务集群，这样会不会更好？
2.为什么在连接层直接rpc调用业务端。那业务端需要通过这条连接推送消息不是会很不方便吗？</div>2019-11-04</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/b4/c1/73df153f.jpg" width="30px"><span>Jun</span> 👍（2） 💬（1）<div>是否可以先在服务器端聚合一段时间的数据再写入</div>2019-10-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/55/e6/87197b10.jpg" width="30px"><span>GeekAmI</span> 👍（0） 💬（2）<div>请问老师：长连网关调用业务层为何是RPC，而不是通过消息队列调用呢？</div>2019-11-12</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/L8Hia5sfiafASmBa3eTLMH8C25gMCHLTXddMkIiaCb0ky48FowibUrLQ9WSeTxSIS3prFsSjiaarwbRp1kTXDbug9eQ/132" width="30px"><span>黄海</span> 👍（0） 💬（1）<div>请问老师，课程中的 tcp长连接网关机，可以用 openresty 开发吗？</div>2019-10-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/3d/02/ecdb4e66.jpg" width="30px"><span>东东🎈</span> 👍（0） 💬（3）<div>老师，线上netty经常抛java.io.Exception:Connection reset by peer异常，连接被重置，这个问题可以修复吗？</div>2019-10-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/0a/e3/9637bfdb.jpg" width="30px"><span>Ricky Fung</span> 👍（1） 💬（0）<div>提升写入能力：
1.分片（数据库、缓存分片）；
2.批量写入，例如点赞数统计 如果有N个用户对某条微博点赞可以直接incr N</div>2021-07-26</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/DYAIOgq83erq6X1NBCibSe2TheibLEykYPK9nb1NWicoU1xia0ibpjCZJxwqlA7830uZLj4jSDkwRT8viaFf3j9BZ3Tw/132" width="30px"><span>Vicky</span> 👍（1） 💬（2）<div>请教老师：
中央资源中（比如 Redis）记录当前用户在哪台网关机上线，如果其中一个网关机宕机，是如果及时的将redis中相关的记录删除？</div>2020-12-07</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/DYAIOgq83erZCyXaP2gbxwFHxvtnyaaF2Pyy5KkSMsk9kh7SJl8icp1CD6wicb6VJibiblGibbpDo6IuHrdST6AnWQg/132" width="30px"><span>Geek_1cc6d1</span> 👍（0） 💬（0）<div>业务层调用网关层rpc服务发送消息（客户端连接着具体的某台网关服务器）时应该是跟ip有关的，所以默认的路由策略应该是不行了。通常都有什么解决方法？</div>2021-04-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1f/75/15/8b2cf6d4.jpg" width="30px"><span>包子浣熊</span> 👍（0） 💬（0）<div>解决资源写入瓶颈的问题（比如直播间观看人数的计数资源）？ 能否在人数过多的账号后面加上一个不同的数字作为key，让它们布到不同的切片上。 写入的时候可以写到其中的任意一个。 读取的时候需要把它们的结果聚合起来。</div>2020-08-02</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/47/00/3202bdf0.jpg" width="30px"><span>piboye</span> 👍（0） 💬（0）<div>水平扩展接入层，还有一种特殊方式，接入层是带状态的，这种方式不需要全局状态，接入层容灾就是两个备份机器</div>2020-05-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/47/00/3202bdf0.jpg" width="30px"><span>piboye</span> 👍（0） 💬（0）<div>1 合并写，增加了延迟，同时使用directio
2 多机器写日志方式，因为没有sync，顺序写性能高
3 多机器，写内存，异步合并写磁盘，同时挂机可能会丢失部分数据。</div>2020-05-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/f6/ed/35186af6.jpg" width="30px"><span>康家沟偶像天团王大锤</span> 👍（0） 💬（0）<div>在连接的前端机对进出直播间事件做初步统计，定期将统计结果刷入缓存，多次进出可以变为一次更新</div>2020-01-16</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/60/71/895ee6cf.jpg" width="30px"><span>分清云淡</span> 👍（0） 💬（0）<div>分表 存贮 对于一些热点列 在cache里面增加特殊索引字段 也可以在内存中 直接存储计算结果 节省 查询 计算时间</div>2019-12-04</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/80/98/5591d99d.jpg" width="30px"><span>唯我天棋</span> 👍（0） 💬（0）<div>要想解决资源层的写入瓶颈，除了分片机制外，还有什么办法能解决资源写入瓶颈的问题呢（比如直播间观看人数的计数资源）？

1.使用高性能缓存。。
2.请求合并</div>2019-11-04</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/e1/08/3dc76043.jpg" width="30px"><span>钢</span> 👍（0） 💬（0）<div>老师问题:单位时间时间内如何提高写入速度
垂直方向:
1、sql语句优化，索引，事务写入
水平方向:
1、分库分表
2、读写分离
直播观看计数资源，不是要保存在关系数据库，可以考虑用nosql非关系数据库</div>2019-10-10</li><br/>
</ul>