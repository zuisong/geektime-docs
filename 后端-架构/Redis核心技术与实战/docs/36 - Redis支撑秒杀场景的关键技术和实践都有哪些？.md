你好，我是蒋德钧。

秒杀是一个非常典型的活动场景，比如，在双11、618等电商促销活动中，都会有秒杀场景。秒杀场景的业务特点是**限时限量**，业务系统要处理瞬时的大量高并发请求，而Redis就经常被用来支撑秒杀活动。

不过，秒杀场景包含了多个环节，可以分成秒杀前、秒杀中和秒杀后三个阶段，每个阶段的请求处理需求并不相同，Redis并不能支撑秒杀场景的每一个环节。

那么，Redis具体是在秒杀场景的哪个环节起到支撑作用的呢？又是如何支持的呢？清楚了这个问题，我们才能知道在秒杀场景中，如何使用Redis来支撑高并发压力，并且做好秒杀场景的应对方案。

接下来，我们先来了解下秒杀场景的负载特征。

## 秒杀场景的负载特征对支撑系统的要求

秒杀活动售卖的商品通常价格非常优惠，会吸引大量用户进行抢购。但是，商品库存量却远远小于购买该商品的用户数，而且会限定用户只能在一定的时间段内购买。这就给秒杀系统带来两个明显的负载特征，相应的，也对支撑系统提出了要求，我们来分析下。

**第一个特征是瞬时并发访问量非常高**。

一般数据库每秒只能支撑千级别的并发请求，而Redis的并发处理能力（每秒处理请求数）能达到万级别，甚至更高。所以，**当有大量并发请求涌入秒杀系统时，我们就需要使用Redis先拦截大部分请求，避免大量请求直接发送给数据库，把数据库压垮**。
<div><strong>精选留言（30）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/10/78/c7/083a3a0b.jpg" width="30px"><span>新世界</span> 👍（29） 💬（4）<div>一般秒杀场景 用redis 扣减库存，不去保证原子性，扣减后有可能超卖，再用数据库去保证最终不超卖，因为超卖的不会多，能够打到mysql的操作就是超卖+实际库存，所以mysql压力也会比较少

课后习题：  redis的 800个库存，分布到4个server上，打到哪个server上，取决于key，如果key分布不均匀，会导致 一定的不公平，就像高考一样，有的地方考生多，有的地方考生少，虽然在每个省中录取名额一样，但是也不公平</div>2020-12-07</li><br/><li><img src="" width="30px"><span>Geek_f6a7c7</span> 👍（18） 💬（2）<div>不是一个好方案，一个商品库存数切片不同实例存储的确可以减少单个实例的压力，但是在业务上可行性有待商榷，如果当前切片实例没有库存，是不是要再请求别的切片实例？特别是库存数都被抢购完成后，后面的请求是不是都要请求4个切片节点做库存数的聚合才知道又没人退货，做库存数的聚合？</div>2020-12-04</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/f0/9f/46d8f49a.jpg" width="30px"><span>华伦</span> 👍（9） 💬（2）<div>设计上是可行的，将秒杀请求也进行分片，库存的校验可以按照分库顺序扣。</div>2020-11-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/25/7f/473d5a77.jpg" width="30px"><span>曾轼麟</span> 👍（5） 💬（1）<div>我个人认为这个方式不是很好，因为单个sku分开后，需要对用户的请求做路由判断，假如一个用户请求本身就发出了两条，按照随机路由的方式，他有可能在两个切片中抢到商品。假如路由规则是固定的，那么会出现sku还有库存，但是用户就是抢不到的情况</div>2020-11-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/5f/e5/54325854.jpg" width="30px"><span>范闲</span> 👍（3） 💬（2）<div>如果秒杀请求能够比较均匀的分别打到4个实例上是没有问题的。
这个时候不返回剩余库存，不做聚合，能大幅度提高速度。</div>2020-12-03</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/dd/9b/0bc44a78.jpg" width="30px"><span>yyl</span> 👍（0） 💬（1）<div>将800个商品均分至4个实例，并不能保证客户端请求被均分至不同的实例；毕竟用户的行为是无法预测的，有可能出现某个实例的请求量比较大</div>2020-11-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/13/45/16c60da2.jpg" width="30px"><span>蔫巴的小白菜</span> 👍（0） 💬（1）<div>我觉得，是可行的，主要要考虑最后的余量怎么处理，0～2个分片上有余量，而3号分片上有余量，这样怎么处理，还有，就是最后的用余量足够，而每个分片的余量不够，这个又怎么去处理，我觉得这些处理好了，分片存储可以考虑使用。</div>2020-11-16</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/bc/25/1c92a90c.jpg" width="30px"><span>tt</span> 👍（0） 💬（1）<div>每个实例200个库存，当某个请求在某个实例上查询不到库存时，并不是库存真的为0了，还需要去其它实例查询，这个是一个缺点。

好处时可以承受更大的流量。</div>2020-11-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/90/8a/288f9f94.jpg" width="30px"><span>Kaito</span> 👍（216） 💬（22）<div>使用多个实例的切片集群来分担秒杀请求，是否是一个好方法？

使用切片集群分担秒杀请求，可以降低每个实例的请求压力，前提是秒杀请求可以平均打到每个实例上，否则会出现秒杀请求倾斜的情况，反而会增加某个实例的压力，而且会导致商品没有全部卖出的情况。

但用切片集群分别存储库存信息，缺点是如果需要向用户展示剩余库存，要分别查询多个切片，最后聚合结果后返回给客户端。这种情况下，建议不展示剩余库存信息，直接针对秒杀请求返回是否秒杀成功即可。

秒杀系统最重要的是，把大部分请求拦截在最前面，只让很少请求能够真正进入到后端系统，降低后端服务的压力，常见的方案包括：页面静态化（推送到CDN）、网关恶意请求拦截、请求分段放行、缓存校验和扣减库存、消息队列处理订单。

另外，为了不影响其他业务系统，秒杀系统最好和业务系统隔离，主要包括应用隔离、部署隔离、数据存储隔离。</div>2020-11-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/20/08/bc06bc69.jpg" width="30px"><span>Dovelol</span> 👍（22） 💬（37）<div>老师好，想问下，用redis扣库存直接用HINCRBY已秒杀库存量，判断返回值&gt;=总库存就是没库存，小于总库存就是扣减库存成功可以购买，这样判断有什么问题么？为什么要引入lua脚本来增加复杂度呢？</div>2020-11-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/d2/74/7861f504.jpg" width="30px"><span>马听</span> 👍（7） 💬（1）<div>为啥库存扣减不能再数据库执行呢？
除了文中提到的额外开销和可能导致超售，另外如果数据库是 MySQL，则可能导致 MySQL 的死锁检测，导致消耗大量的 CPU 资源。具体可以参考《MySQL实战45 讲》07 节 ：行锁功过</div>2021-02-02</li><br/><li><img src="" width="30px"><span>Geek_0879b1</span> 👍（7） 💬（6）<div>老师，秒杀过程中，如果不论Redis采用RDB还是AOF的方式来持久化，都有可能导致库存数据的丢失。而如果不采用持久化的方式，数据丢失的风险更大。此时如果redis中的库存数据丢失，并且库存数据没有同步到关系型数据库，这种丢失的风险该如何应对？</div>2020-12-14</li><br/><li><img src="" width="30px"><span>Geek_9a0c9f</span> 👍（4） 💬（1）<div>老师问下，最后的订单处理是如何处理的，库存扣完成功操作，接着进行下单操作，下单操作是直接对数据库进行操作么？还是将行为打入kafka之类的消息队列，然后慢慢的去消费处理订单</div>2020-11-15</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/KFgDEHIEpnTUibfcckj33D1LVj9VapfrK3Yq2Gj00wnLt4nkWS7HvYy5NxvmnQcQpaysuBHVrB9MILWZ9hibUNasicPNtueYoNM/132" width="30px"><span>JAVA初级开发工程师</span> 👍（3） 💬（2）<div>关于秒杀场景有几个问题
1、redis并不保证数据的一致性 发生主备切换有可能会造成超卖这种情况怎么处理
2、秒杀如何处理大库存场景 如果一个商品库存对应redis一个key  这个key可能同时承受数十万的qps 这种情况redis也是扛不住的</div>2021-05-20</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/DYAIOgq83eoSMRiaMtAcqQz7oNzcNg0M2vEic2sByibGib0l9z2g5Niafo7caLhqJtACRfCCT1sdAKQQM40BHEWsdOg/132" width="30px"><span>王云星</span> 👍（3） 💬（0）<div>使用多个实例的切片集群来分担秒杀请求，是否是一个好方法？
不太行，难度很大，第一个是流量需要均衡分配到每个实例，第二个是如果说一个订单需要扣减多个库存，而单个实例库存剩余不够，导致扣减库存失败，但其实总库存是够的。比如每个实例还剩1件库存，一个订单同时秒杀4件，这下就会扣减失败，实际上库存是够的</div>2021-01-08</li><br/><li><img src="" width="30px"><span>Geek_f00f74</span> 👍（2） 💬（5）<div>实际生产中能用Redis做库存校验和扣减吗？如果Redis宕机如何保证Redis库存和数据库库存一致？如果发生主从切换导致库存更新丢失呢？
使用分布式锁的话就是串行化了，这个性能太差了吧。</div>2020-11-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/2d/35/d3/8de43dd5.jpg" width="30px"><span>Breeze</span> 👍（1） 💬（0）<div>使用多个实例的切片集群来分担秒杀请求，是否是一个好方法?
如果并发量不大，或者提前做了限流策略，那么使用多个实例切片来分担压力就没有太大必要性了，主从集群就足够应对了。
如果并发量非常大，比如10w+请求，那么此时通过多实例来分担秒杀请求是合理的，因为并发量足够大，800库存理论上在极短的时间内会出现库存不均匀的现象，但是很快整个库存就都被消化掉，所以这个影响是可以忽略的。
所以整个方案取决秒杀的并发量和秒杀整个过程时长，如果并发量很大，秒杀过程很短（库存不大），那么这个方案是可行的。</div>2022-04-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/23/5b/983408b9.jpg" width="30px"><span>悟空聊架构</span> 👍（1） 💬（0）<div>客户端的秒杀请求可以分发到不同的实例上进行处理，你觉得这是一个好方法吗？

使用切片集群会将问题复杂化：
1.如果分片的处理能力不是均衡的，可能出现某个分片的商品在秒杀活动结束后未卖完。
2.前端查询总库存时，后端需要查多个分片的库存，然后进行合并，增加了网络交互。
3.当出现一个订单购买多件商品时，商品库存被分摊到多个分片，需要用锁占用分片资源，多个分片扣减库存成功后，才会释放分片资源，影响性能。</div>2021-05-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/77/a5/c5ae871d.jpg" width="30px"><span>zenk</span> 👍（1） 💬（0）<div>多个实例，需要客户段做负载均衡，这是额外的复杂度

查询

查询的时候需要查询每个结点，因此集群并没减少每个节点的请求量

扣库存

扣库存的时候，考虑到高并发的时候很容易给每个实例分配到200个并发请求，因此只有这些请求会分散在各个节点

如果不命中，需要请求其他每个节点，而这些请求量更大，因此整体而言扣库存也没有降低节点的压力

单机情况下，假设一次扣库存操作是10us（量级不确定），800次就是8ms，200次是2ms

可靠性
集群高，一个挂了其他节点还能处理

结论
集群在命中第一个节点的时候可缓解节点压力，但是增加客户端复杂度

可靠性，秒杀集中在很短时间，减少故障概率

扣库存差6ms可以接受

所以，集群好处不明显</div>2020-12-03</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/cf/81/96f656ef.jpg" width="30px"><span>杨逸林</span> 👍（1） 💬（9）<div>有秒杀场景，那老师，在 Redis 中，当一个 Key 的 QPS 达到 100万时，应该如何处理呢？</div>2020-11-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/9a/ab/fd201314.jpg" width="30px"><span>小耿</span> 👍（0） 💬（0）<div>如果用lua脚本的方式应对秒杀，这个方法确实可以减轻单个实例的访问压力。但如果用分布式锁的方式来应对秒杀，访问压力集中在锁在的实例，库存量所在的实例访问压力并不大，无需做分片处理。</div>2023-09-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/cf/c2/fe1fb863.jpg" width="30px"><span>ss柚子</span> 👍（0） 💬（0）<div>这边采用redis支撑秒杀场景业务，那数据库和redis如何保证数据的一致性？这里没有涉及到什么时候去更新数据库中的数据</div>2023-03-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/ca/07/22dd76bf.jpg" width="30px"><span>kobe</span> 👍（0） 💬（0）<div>那怎么在 Lua 脚本中实现这两个操作呢？我给你提供一段 Lua 脚本写的伪代码，它显示了这两个操作的实现。#获取商品库存信息            local counts = redis.call(&quot;HMGET&quot;, KEYS[1], &quot;total&quot;, &quot;ordered&quot;);#将总库存转换为数值local total = tonumber(counts[1])#将已被秒杀的库存转换为数值local ordered = tonumber(counts[2])  #如果当前请求的库存量加上已被秒杀的库存量仍然小于总库存量，就可以更新库存         if ordered + k &lt;= total then    #更新已秒杀的库存量    redis.call(&quot;HINCRBY&quot;,KEYS[1],&quot;ordered&quot;,k)                              return k;  end               return 0有了 Lua 脚本后，我们就可以在 Redis 客户端，使用 EVAL 命令来执行这个脚本了。最后，客户端会根据脚本的返回值，来确定秒杀是成功还是失败了。如果返回值是 k，就是成功了；如果是 0，就是失败。
这里hincrby命令的返回值应该是ordered的新值，而不是这个增量k吧</div>2022-06-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/25/86/2b/7f9b94d8.jpg" width="30px"><span>Seajunnn</span> 👍（0） 💬（0）<div>基于Redis原子操作和 基于分布式锁 这两种方案 各有什么优劣呢？</div>2022-05-05</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/74/aa/178a6797.jpg" width="30px"><span>阿昕</span> 👍（0） 💬（0）<div>切片的目的是分隔数据，所以没必要</div>2022-04-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/1e/8c/d9330d2b.jpg" width="30px"><span>花儿少年</span> 👍（0） 💬（0）<div>使用多个实例的切片集群来分担秒杀请求，是否是一个好方法？

我觉得是一个可行的方式，减少单台实例的压力；
举个例子：京东在下单的时候会显示区域是否有货，而不是全国的库存情况，此时区域可认为是库存的一部分，区域无货也可以下单，然后从别的区域扣减，如果能扣减成功，则下单成功，否则认为下单失败。</div>2021-09-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/19/d9/ff/b23018a6.jpg" width="30px"><span>Heaven</span> 👍（0） 💬（0）<div>这会造成一些意外的操作,比如长连接导致的请求的都是一个实例,不建议这么做</div>2021-09-02</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/18/90/ea/67f2ef29.jpg" width="30px"><span>乐事不乐</span> 👍（0） 💬（0）<div>能否把库存直接存储在redis中，直接在redis 完成库存信息的变动？</div>2021-07-30</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/23/20/b2/32eef1b6.jpg" width="30px"><span>Forever♏️</span> 👍（0） 💬（0）<div>请问秒杀场景，客户端在点击秒杀按钮后，如何接收到服务器端已经秒杀成功的响应呢</div>2021-06-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1d/20/be/bf6a570f.jpg" width="30px"><span>Tom</span> 👍（0） 💬（0）<div>老师，您好，请问采用分布式锁的方式，那如何解决秒杀场景下的用户等待问题，造成用户体验不好的现状？</div>2021-05-06</li><br/>
</ul>