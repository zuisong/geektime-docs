你好，我是蒋德钧。

我们现在做互联网产品的时候，都有这么一个需求：记录用户在网站或者App上的点击行为数据，来分析用户行为。这里的数据一般包括用户ID、行为类型（例如浏览、登录、下单等）、行为发生的时间戳：

```
UserID, Type, TimeStamp
```

我之前做过的一个物联网项目的数据存取需求，和这个很相似。我们需要周期性地统计近万台设备的实时状态，包括设备ID、压力、温度、湿度，以及对应的时间戳：

```
DeviceID, Pressure, Temperature, Humidity, TimeStamp
```

这些与发生时间相关的一组数据，就是时间序列数据。**这些数据的特点是没有严格的关系模型，记录的信息可以表示成键和值的关系**（例如，一个设备ID对应一条记录），所以，并不需要专门用关系型数据库（例如MySQL）来保存。而Redis的键值数据模型，正好可以满足这里的数据存取需求。Redis基于自身数据结构以及扩展模块，提供了两种解决方案。

这节课，我就以物联网场景中统计设备状态指标值为例，和你聊聊不同解决方案的做法和优缺点。

俗话说，“知己知彼，百战百胜”，我们就先从时间序列数据的读写特点开始，看看到底应该采用什么样的数据类型来保存吧。

## 时间序列数据的读写特点

在实际应用中，时间序列数据通常是持续高并发写入的，例如，需要连续记录数万个设备的实时状态值。同时，时间序列数据的写入主要就是插入新数据，而不是更新一个已存在的数据，也就是说，一个时间序列数据被记录后通常就不会变了，因为它就代表了一个设备在某个时刻的状态值（例如，一个设备在某个时刻的温度测量值，一旦记录下来，这个值本身就不会再变了）。
<div><strong>精选留言（30）</strong></div><ul>
<li><img src="" width="30px"><span>Geek_1e8830</span> 👍（31） 💬（4）<div>老师，你好，问个问题，基于redis的单线程原理lua脚本到底可不可以保证原子性？</div>2021-01-31</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/90/8a/288f9f94.jpg" width="30px"><span>Kaito</span> 👍（433） 💬（45）<div>使用Sorted Set保存时序数据，把时间戳作为score，把实际的数据作为member，有什么潜在的风险？

我目前能想到的风险是，如果对某一个对象的时序数据记录很频繁的话，那么这个key很容易变成一个bigkey，在key过期释放内存时可能引发阻塞风险。所以不能把这个对象的所有时序数据存储在一个key上，而是需要拆分存储，例如可以按天&#47;周&#47;月拆分（根据具体查询需求来定）。当然，拆分key的缺点是，在查询时，可能需要客户端查询多个key后再做聚合才能得到结果。

如果你是Redis的开发维护者，你会把聚合计算也设计为Sorted Set的内在功能吗？

不会。因为聚合计算是CPU密集型任务，Redis在处理请求时是单线程的，也就是它在做聚合计算时无法利用到多核CPU来提升计算速度，如果计算量太大，这也会导致Redis的响应延迟变长，影响Redis的性能。Redis的定位就是高性能的内存数据库，要求访问速度极快。所以对于时序数据的存储和聚合计算，我觉得更好的方式是交给时序数据库去做，时序数据库会针对这些存储和计算的场景做针对性优化。

另外，在使用MULTI和EXEC命令时，建议客户端使用pipeline，当使用pipeline时，客户端会把命令一次性批量发送给服务端，然后让服务端执行，这样可以减少客户端和服务端的来回网络IO次数，提升访问性能。</div>2020-09-07</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/10/92/760f0964.jpg" width="30px"><span>阳明</span> 👍（76） 💬（6）<div>存在member重复的问题，会对member覆盖</div>2020-09-07</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/52/40/e57a736e.jpg" width="30px"><span>pedro</span> 👍（35） 💬（0）<div>Hash 和 Sorted Set 的结合让我想到了 LRU 中的 HashMap 和 LinkedList 的结合，二者均取长处碰撞出了不一样的火花，看看毫不沾边的事物，往往具有相同的内涵。</div>2020-09-07</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/fd/fd/326be9bb.jpg" width="30px"><span>注定非凡</span> 👍（24） 💬（0）<div>1，作者讲了什么？
根据时间序列数据的特点，选择合适的存储方案

2，作者是怎么把这事给讲明白的？
结合具体场景，探讨解决方案
    1，介绍需求背景，用户行为，设备监控数据分析
    2，介绍数据特点，时间线连续，没有逻辑关系，数据量大
    3，介绍操作场景，插入多且快，常单点查询，分组统计聚合
 
3，作者为了把这事给讲清楚，讲了那些要点？有哪些亮点？
1，亮点1：先讲清楚需求背景，从实际问题出发，推演出存储时间序列数据适合使用sort set 和hash解决点查询和范围查询的需求
2，要点1：同时写入sort set和hash 两种数据类型的存储，需要使用原子操作，可以借助MULTI和 EXEC命令
3，要点2：大数据量的聚合统计，会非常消耗网络带宽，所以可以使用RedisTimeSeries模块处理

4，对于作者所讲，我有哪些发散性思考？

5，在未来的那些场景中，我能够使用它？

6，留言区的收获</div>2020-10-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/43/79/18073134.jpg" width="30px"><span>test</span> 👍（20） 💬（4）<div>redis的事务不是完整的事务，当有一个命令失败时还是会继续往下执行，这是个问题。时序数据还是交给时序数据库来保存比较专业</div>2020-09-07</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/cb/f9/75d08ccf.jpg" width="30px"><span>Mr.蜜</span> 👍（17） 💬（0）<div>Sorted Set还是基于Set集合的，所以如果member值相同，那么ZADD只会更新score，存在数据丢失的风险。我有个问题：既然每三分钟聚合一次计算，为何不直接按时间统计值呢？比方说hincrby，把指定一段时间的温度聚合在一起，可以用lua脚本，实现此类计算，这样既实现了原子性，又不会特别消耗内存，还能实现数据统计。</div>2020-09-19</li><br/><li><img src="" width="30px"><span>dfuru</span> 👍（12） 💬（6）<div>hash和sorted set类型的key不能相同，文件是相同的。
127.0.0.1:6379&gt; MULTI
OK
127.0.0.1:6379&gt; ZADD dev:temp4 2020092201 26.8
QUEUED
127.0.0.1:6379&gt; HSET dev:temp4 2020092201 26.8
QUEUED
127.0.0.1:6379&gt; EXEC
1) (integer) 1
2) (error) WRONGTYPE Operation against a key holding the wrong kind of value
127.0.0.1:6379&gt; MULTI
OK
127.0.0.1:6379&gt; HSET dev:temp5 2020092201 26.8
QUEUED
127.0.0.1:6379&gt; ZADD dev:temp6 2020092201 26.8
QUEUED
127.0.0.1:6379&gt; EXEC
1) (integer) 1
2) (integer) 1
</div>2020-09-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/17/28/6002bfd7.jpg" width="30px"><span>Eric.Lee</span> 👍（11） 💬（5）<div>有个问题：市面上有成熟的时间序列数据库如：influxdb、Prometheus等。这一讲，我理解是介绍了Redis支持通过加载模块的形式也能支持这种数据类型的存储。单从时间序列管理、功能方面上个人感觉不如专业数据库成熟？还是作者做过这些数据库的比较专门选用的Redis做数据存储？</div>2020-10-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1e/37/29/b3af57a7.jpg" width="30px"><span>凯文小猪</span> 👍（10） 💬（3）<div>虽然有点泼冷水 但实际上点击流数据 通常是用kafka 作为日志来中转的。这里面涉及几个问题：
1。数据的维度并不总是固定的。比方说今天要聚合统计 明天可能要最值或基数统计。那这时候用redis存储显然不是第一选择。
2. 数据清洗问题。不是所有的数据都是我们期望的 但我们不能要求埋点方来做数据清洗 我们只能要求埋点方尽可能多的上报 才能保证数据是正确的 偏差值 最小。
3. 数据量存储问题。比方说亿级流量 每秒点击流是1W qps ，以一个上送数据1KB估算：那么一天数据量有1KB * 10000 * 3600 * 24 = 864GB 实际上无论是用切片 还是集群都存不下</div>2021-05-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/24/ee/46/7d65ae37.jpg" width="30px"><span>木几丶</span> 👍（8） 💬（0）<div>实际上multi只是redis提供的一个简易的事务操作，如果入队列时就能检测出命令错误的情况，事务会被回滚，而对于在执行时才能检测出错误的情况（如评论中提到的类型错误），前后命令正常执行，事务将不会被回滚，这点跟数据库很不一样 需要特别注意</div>2021-06-04</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1e/2c/82/98e2b82a.jpg" width="30px"><span>Reborn 2.0</span> 👍（7） 💬（4）<div>我想问, 使用sorted set存储, zset不是本身就维护了一个dict么? 为什么还要用hash再存一遍呢?</div>2020-10-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/f8/ba/d28174a9.jpg" width="30px"><span>Geek_zbvt62</span> 👍（6） 💬（0）<div>以前是做物联网的，看完之后有几点思考：
1. 为什么查询指定时间的数据不直接用sorted set的查询操作，虽然是log(N）的时间，比o(1)要慢很多，但这种场景毕竟占比很小。而一般专业时序数据库也确实是这么做的。
2. 时序数据库一个常见场景跨时间线的聚合运算，第一个方案的例子都是在解决单条时间线的问题，场景非常单一。在这点上RedisTimeSeries是否可以实现？是否能更好的利用多核并行？
3. 比起原子性问题，我觉得redis丢数据的问题更严重。</div>2021-01-30</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/66/1a/9e9f7d58.jpg" width="30px"><span>少年</span> 👍（5） 💬（0）<div>TS.ADD device:temperature:1 1596416700 25.1
key指定device id做demo感觉会更清晰些</div>2021-01-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/46/a0/aa6d4ecd.jpg" width="30px"><span>张潇赟</span> 👍（4） 💬（0）<div>这一节中老师的例子有点没说明白：
1.hash 和sorted set 不能用同样的key
2.mutli exec 并不能保证全部成功，redis对事物的支持只是保证两条命令全部被执行，不保证执行成功。如果有保存hash成功了，保存sorted set失败。redis会维持现状，不会对hash回滚</div>2022-03-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/7e/1f/b1d458a9.jpg" width="30px"><span>iamjohnnyzhuang</span> 👍（4） 💬（2）<div>课后题：使用 sorted set 时间戳作为score，温度作为 member 的问题应该主要还是 温度大概率会出现相同的，这个时候 zadd 后会覆盖掉原有的数据，个人觉得的一个解决方法就是value使用时间戳_温度 这样存储。

关于 sorted set + hash 存储时许的方案有个点想的不是很懂，希望有同学或者老师帮忙下：之前看过 zset 的实现，实际上也是 hash + skiplist 实现，skiplist 负责遍历，hash 负责和本文说的一样 依据 score 找到对应的 member（zscore 命令）。 所以感觉多弄了一个hash来存储是不是多此一举呢？

</div>2020-10-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/bb/56/05459f43.jpg" width="30px"><span>Geek_h6mwnx</span> 👍（3） 💬（0）<div>个人认为 redis中的stream类型也可以用于保存时间类型数据，stream XADD会自动保存时间戳参数，使用XRANGE也可以添加时间戳用于范围查询，只是无法像timeseries一样做聚合计算，个人认为做聚合计算这种大量消耗CPU的操作，不适合直接放在redis中进行，更适合放在单独的客户端，加上云服务本身默认不支持time series而默认支持stream.综上所述，如果使用redis存储时间类型数据，建议使用stream</div>2021-03-04</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/92/6d/becd841a.jpg" width="30px"><span>escray</span> 👍（2） 💬（0）<div>记录用户的行为以及物联网设备实时状态，这两种用法都把 Redis 当做“数据库”来用，似乎有悖于 Redis 的初衷。

时间序列数据要求“写”的时候插入快，“读”的时候查询模式多，似乎对于读的快并没有太高的要求，我怎么觉得 Elastic 似乎也挺合适。

读完专栏，感觉上似乎针对查询需求，点查询使用 Hash，范围查询使用 Sorted Set，聚合计算使用 RedisTimeSeries。

如果想要保证插入事务的原子性，那么使用 MUTLI 和 EXEC 关键字。

专栏里面没说，如何编译 RedisTimeSeries，在哪里加载 loadmodule，暂时只能是不明觉厉了。

```
git clone --recursive https:&#47;&#47;github.com&#47;RedisTimeSeries&#47;RedisTimeSeries.git
cd RedisTimeSeries
make setup
...
$ redis-server --loadmodule &#47;path&#47;to&#47;module&#47;redistimeseries.so
loadmodule bin&#47;redistimeseries.so
```

课后题，使用 Sorted Set 保存时间序列数据，时间戳作为 score，实际数据作为 member，潜在的风险可能是时间戳作为 score 有点太长了，或者说太大了，并不方便比较，而且在存储上有些浪费。

看了课代表 @Kaito 的回答，发现我忽略了潜在的 bigkey 风险。另外，可能更大的风险来自于留言中多位同学指出的，当温度作为 member 相同的时候，zadd 会覆盖掉原有的 score，也就是 时间戳，然后就没法查询了。

如果我是 Redis 的开发维护者，不会把 聚合计算 作为 Sorted Set 的内在功能，因为 Redis 本来就不是用作聚合计算或者说是统计的，Redis 的初心应该是“缓存”，或者说是提供高性能的数据读取。

同样来自课代表，聚合计算是 CPU 密集型任务，而 Redis 是单线程的……

在 @Eric.Lee 的留言里面看到时间序列数据库：influxdb 和 Prometheus，后者不是一个监控框架么？

还有同学问到了如何在云 Redis 上加载 RedisTimeSeries 的问题，同问。</div>2021-03-25</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/e8/72/e44c69ef.jpg" width="30px"><span>夏虫井蛙</span> 👍（2） 💬（1）<div>现在很多服务都上云了，用的redis也是供应商提供的服务，一般不自己搭建。RedisTimeSeries以及上一讲的自定义数据类型需要编译加载，一般云供应商不提供这些吧？这时候是不是只能用基础数据类型，没办法用RedisTimeSeries以及自定义数据类型了？</div>2020-09-09</li><br/><li><img src="" width="30px"><span>Geek_LV</span> 👍（2） 💬（2）<div>127.0.0.1:6379&gt; multi
OK
127.0.0.1:6379&gt; HSET device:temperature 202008030911 26.8
QUEUED
127.0.0.1:6379&gt; ZADD device:temperature 202008030911 26.8
QUEUED
127.0.0.1:6379&gt; exec
1) (integer) 1
2) (error) WRONGTYPE Operation against a key holding the wrong kind of value</div>2020-09-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/61/44/10d7ce5a.jpg" width="30px"><span>Sue</span> 👍（2） 💬（1）<div>老师，为什么那个存温度的value🀄️也有key？难道这个value类型是hash类型吗</div>2020-09-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/fd/94/0247f945.jpg" width="30px"><span>咸鱼</span> 👍（2） 💬（5）<div>使用sorted set时间戳作为score，可能会出现时间戳相同导致被覆盖的可能吧</div>2020-09-07</li><br/><li><img src="" width="30px"><span>Geek_da6c20</span> 👍（1） 💬（1）<div>那为什么RedisTimeSeries没有bigKey问题？</div>2022-10-25</li><br/><li><img src="" width="30px"><span>Geek_0bba55</span> 👍（1） 💬（0）<div>数据量大的情况下，2种方案都有问题，用来玩玩就行。
第一个方案：会造成大key，热key，影响系统性能。
第二个方案：在redis完成聚合操作，会导致redis阻塞。
</div>2022-04-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/46/a0/aa6d4ecd.jpg" width="30px"><span>张潇赟</span> 👍（1） 💬（0）<div>老师这一节举的例子，hash 和 sorted set用的是同一个key啊。感觉有明显的漏洞！！！</div>2022-03-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/e8/61/47293afd.jpg" width="30px"><span>levi</span> 👍（1） 💬（0）<div>我觉得时间序列的计算存储这块，有更多更好的方式去做。
比如专门的时间序列数据库influxDB，做存储，回放，各种粒度的聚合都非常合适。
再比如用flink做基于3分钟窗口的计算，简直是flink天然的场景。
但是老师在这边讲的内容，对我来说最大的好处在于，提供了多种不同方式去解决同一个问题，同时能够让你从底层去思考解决问题的方式。比如说flink基于状态存储去做聚合，如果状态过大不适合，是否可以改为redis去存储，如果基于redis存储又该如何去做。
另外，聚合的本质是什么？为什么说用hash和sortedSet会占用空间存不下，如果题目是不考虑窗口是不是可以将简单聚合存储为sum和count值到redis中从而降低空间占用；而如果是按照题目考虑窗口，又是否可以将窗口聚合切分为一个一个粒度合适的unit，本质上是先做一次小聚合，再根据需要用到的数据做一次大聚合。
总之，老师讲得蛮好，从某个场景带我见识了redis的能力和用法。</div>2021-10-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1f/26/34/891dd45b.jpg" width="30px"><span>宙斯</span> 👍（1） 💬（0）<div>问题： 使用Sorted Set保存时序数据，把时间戳作为score，把实际的数据作为member，有什么潜在的风险？
回答：存在相同的member值时会覆盖以前的member值（尽管score不同）
问题：如果你是Redis的开发维护者，你会把聚合计算也设计为Sorted Set的内在功能吗？
回答：不会。聚合计算比较消耗CPU，对于单线程redis来说这不是它的强项。
</div>2021-08-13</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/UWDBUEsDLIKpeIujPLsrRG9l0cFhWlXB9CcaOpNKrOdhDAia6PialmJZ4MQgYtBpDdu58leIDDlsOxaZsRvknZZA/132" width="30px"><span>Geek_cc0645</span> 👍（1） 💬（0）<div>第一种方案中，自己有两个问题：1.如果是多台设备应该怎么存储这些数据，是一个集合，一个时间戳，里面存储的所有设备的温度还是多个集合，每个集合表示一个设备 2.如何查询某时间区间内所有设备的数据。希望有想法的同学可以给答疑一下。</div>2021-06-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/2c/99/2a5b782f.jpg" width="30px"><span>风云一度</span> 👍（0） 💬（0）<div>这里说的返回客户端聚合，客户端是指什么
</div>2024-05-16</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/61/ef/ac5e914d.jpg" width="30px"><span>麦耀锋</span> 👍（0） 💬（0）<div>基于sorted set来做温度这种数值记录会有一个问题，因为sorted set本质上还是set，同一个member只能出现一次。在本节的例子里面，不同时刻出现相同温度的可能性太大了，因此相同温度的记录最多只能保留一条，很多信息就丢了。文中例子“指定时间范围查温度”就很有可能查不出来了，其他一些用例也会因此而导致一些问题（如平均温度等）。</div>2023-11-06</li><br/>
</ul>