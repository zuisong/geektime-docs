你好，我是蒋德钧。

在Redis的实际部署应用中，有一个非常严重的问题，那就是Redis突然变慢了。一旦出现这个问题，不仅会直接影响用户的使用体验，还可能会影响到“旁人”，也就是和Redis在同一个业务系统中的其他系统，比如说数据库。

举个小例子，在秒杀场景下，一旦Redis变慢了，大量的用户下单请求就会被拖慢，也就是说，用户提交了下单申请，却没有收到任何响应，这会给用户带来非常糟糕的使用体验，甚至可能会导致用户流失。

而且，在实际生产环境中，Redis往往是业务系统中的一个环节（例如作为缓存或是作为数据库）。一旦Redis上的请求延迟增加，就可能引起业务系统中的一串儿“连锁反应”。

我借助一个包含了Redis的业务逻辑的小例子，简单地给你解释一下。

应用服务器（App Server）要完成一个事务性操作，包括在MySQL上执行一个写事务，在Redis上插入一个标记位，并通过一个第三方服务给用户发送一条完成消息。

这三个操作都需要保证事务原子性，所以，如果此时Redis的延迟增加，就会拖累App Server端整个事务的执行。这个事务一直完成不了，又会导致MySQL上写事务占用的资源无法释放，进而导致访问MySQL的其他请求被阻塞。很明显，Redis变慢会带来严重的连锁反应。
<div><strong>精选留言（30）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/19/aa/ff/e2c331e0.jpg" width="30px"><span>bbbi</span> 👍（29） 💬（3）<div>针对redis-cluster还可以使用scan命令么？</div>2020-10-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/90/8a/288f9f94.jpg" width="30px"><span>Kaito</span> 👍（386） 💬（28）<div>在 Redis 中，还有哪些其他命令可以代替 KEYS 命令，实现同样的功能呢？这些命令的复杂度会导致 Redis 变慢吗？

如果想要获取整个实例的所有key，建议使用SCAN命令代替。客户端通过执行SCAN $cursor COUNT $count可以得到一批key以及下一个游标$cursor，然后把这个$cursor当作SCAN的参数，再次执行，以此往复，直到返回的$cursor为0时，就把整个实例中的所有key遍历出来了。

关于SCAN讨论最多的问题就是，Redis在做Rehash时，会不会漏key或返回重复的key。

在使用SCAN命令时，不会漏key，但可能会得到重复的key，这主要和Redis的Rehash机制有关。Redis的所有key存在一个全局的哈希表中，如果存入的key慢慢变多，在达到一定阈值后，为了避免哈希冲突导致查询效率降低，这个哈希表会进行扩容。与之对应的，key数量逐渐变少时，这个哈希表会缩容以节省空间。

1、为什么不会漏key？Redis在SCAN遍历全局哈希表时，采用*高位进位法*的方式遍历哈希桶（可网上查询图例，一看就明白），当哈希表扩容后，通过这种算法遍历，旧哈希表中的数据映射到新哈希表，依旧会保留原来的先后顺序，这样就可以保证遍历时不会遗漏也不会重复。

2、为什么SCAN会得到重复的key？这个情况主要发生在哈希表缩容。已经遍历过的哈希桶在缩容时，会映射到新哈希表没有遍历到的位置，所以继续遍历就会对同一个key返回多次。

SCAN是遍历整个实例的所有key，另外Redis针对Hash&#47;Set&#47;Sorted Set也提供了HSCAN&#47;SSCAN&#47;ZSCAN命令，用于遍历一个key中的所有元素，建议在获取一个bigkey的所有数据时使用，避免发生阻塞风险。

但是使用HSCAN&#47;SSCAN&#47;ZSCAN命令，返回的元素数量与执行SCAN逻辑可能不同。执行SCAN $cursor COUNT $count时一次最多返回count个数的key，数量不会超过count。

但Hash&#47;Set&#47;Sorted Set元素数量比较少时，底层会采用intset&#47;ziplist方式存储，如果以这种方式存储，在执行HSCAN&#47;SSCAN&#47;ZSCAN命令时，会无视count参数，直接把所有元素一次性返回，也就是说，得到的元素数量是会大于count参数的。当底层转为哈希表或跳表存储时，才会真正使用发count参数，最多返回count个元素。</div>2020-09-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/f1/96/9571fa3d.jpg" width="30px"><span>青青子衿</span> 👍（75） 💬（10）<div>当你发现 Redis 性能变慢时，可以通过 Redis 日志，或者是 latency monitor 工具，查询变慢的请求，根据请求对应的具体命令以及官方文档，确认下是否采用了复杂度高的慢查询命令。
其实这个排除过程才是我们最想学习的，却被作者一带而过了。。。。</div>2020-09-18</li><br/><li><img src="" width="30px"><span>Geek_9b08a5</span> 👍（20） 💬（3）<div>第十八课：
1.作者讲了什么？
	当redis查询变慢了怎么办，如何排查，如何进行处理？
2.作者是怎么把这件事将明白的？
	1、通过分析redis各组件及硬件，找出问题所在
3.为了讲明白，作者讲了哪些要点，哪些亮点？
	1、亮点：通过redis-cli --intrinsic-latency 120可以得知redis的基准线。后续可以根据基准线的响应速度进行判断是否查询慢，这是我之前所不知道的判断方法
	2、要点：基于自己对 Redis 本身的工作原理的理解，并且结合和它交互的操作系统、存储以及网络等外部系统关键机制，再借助一些辅助工具来定位原因，并制定行之有效的解决方案
	3、要点：Redis 自身操作特性的影响
		1. 慢查询命令：命令操作的复杂度有关
			排查方法：通过 Redis 日志，或者是 latency monitor 工具，查询变慢的请求
			解决方法：1.用其他高效命令代替。如不要使用keys查询所有key，可以使用scan进行查询，不会阻塞线程
					  2.当你需要执行排序、交集、并集操作时，可以在客户端完成，而不要用 SORT、SUNION、SINTER 这些命令，以免拖慢 Redis 实例。
		2.过期 key 操作：redis本身的内存回收机制会造成redis操作阻塞，导致性能变慢（Redis 4.0 后可以用异步线程机制来减少阻塞影响）
		    导致原因：大批量的key同时间内过期，导致删除过期key的机制一直触发，引起redis操作阻塞
			解决方法：对key设定过期时间时，添加一个删除的时间随机数，能避免key存在同一时间过期
	4、要点：redis删除过期key的机制，每100毫秒对一些key进行删除。算法如下
		1.采样 ACTIVE_EXPIRE_CYCLE_LOOKUPS_PER_LOOP 个数的 key，并将其中过期的 key 全部删除；
		2.如果超过 25% 的 key 过期了，则重复删除的过程，直到过期 key 的比例降至 25% 以下。

4.对于作者所讲的，我有哪些发散性思考？

5.将来在哪些场景里，我能够使用它？

6.留言区收获
	1.在生产环境中，可以使用scan替代keys命令（答案来自@kaito 大佬）
		当scan在Redis在做Rehash时，会不会漏key或返回重复的key？
			1.不漏keys：Redis在SCAN遍历全局哈希表时，采用*高位进位法*的方式遍历哈希桶（可网上查询图例，一看就明白），当哈希表扩容后，通过这种算法遍历，旧哈希表中的数据映射到新哈希表，依旧会保留原来的先后顺序，这样就可以保证遍历时不会遗漏也不会重复。
			2.key重复：这个情况主要发生在哈希表缩容。已经遍历过的哈希桶在缩容时，会映射到新哈希表没有遍历到的位置，所以继续遍历就会对同一个key返回多次。处理方法是在客户端直接做重复过滤
	2.在redis-cluster中，不能使用一次scan在整个集群中获取所有的key，只能通过在每个实例上单独执行scan才可以，再到客户端进行合并	</div>2020-12-30</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/1e/8c/d9330d2b.jpg" width="30px"><span>花儿少年</span> 👍（8） 💬（2）<div>好像说了什么，好像又什么都没说
生产系统中出问题哪有时间整这些，赶紧恢复老板都在后面站着呢
同时这些命令，keys、集合操作基本都是被禁用的；所以正常情况下，生产系统中Redis变慢一般都是bigkey，同时过期，热点数据等等</div>2021-07-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/43/79/18073134.jpg" width="30px"><span>test</span> 👍（7） 💬（0）<div>通常线上是不能使用keys的，标准替代方案就是scan。scan不会导致redis变慢，只是如果在scan过程中kv表扩容的话可能会遇到重复key。
PS：sort的时间复杂度是O(N+M*log(M)) 是因为需要创建一个新的数字，并且用快排去排序。</div>2020-09-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/5f/e5/54325854.jpg" width="30px"><span>范闲</span> 👍（5） 💬（0）<div>可以利用scan命令。但是scan可能会返回重复key，使用方做个去重即可。</div>2020-12-03</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/04/18/d5cb509f.jpg" width="30px"><span>王益新</span> 👍（4） 💬（5）<div>&quot;默认情况下，Redis 每 100 毫秒会删除一些过期 key，具体的算法如下：采样 ACTIVE_EXPIRE_CYCLE_LOOKUPS_PER_LOOP 个数的 key，并将其中过期的 key 全部删除，ACTIVE_EXPIRE_CYCLE_LOOKUPS_PER_LOOP默认是 20，那么，一秒内基本有 200 个过期 key 会被删除。&quot;

这里的采样是什么意思？获取ACTIVE_EXPIRE_CYCLE_LOOKUPS_PER_LOOP个过期的key吗？那为什么说是其中过期的key？

如果采样得到的不全是过期的key，一秒内怎么还会有 200 个过期 key 会被删除？</div>2020-10-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/8f/cf/890f82d6.jpg" width="30px"><span>那时刻</span> 👍（3） 💬（0）<div>前段时间时间刚好看了redis里sort的实现，说说的我的理解。sort是基于Bentley &amp; McIlroy&#39;s Engineering a Sort Function。可以认为是partial qsort，只保证指定返回的数据（函数参数里的lrange和rrange）有序即可。在元素个数小于7的时候，采用插入排序，因为元素个数小的时候，快速排序并不高效。元素个数大大于7的时候，采用快速排序，经过这些优化之后，SORT操作复杂度为 O(N+M*log(M))。</div>2020-09-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/18/4b/d7/f46c6dfd.jpg" width="30px"><span>William Ning</span> 👍（2） 💬（0）<div>本机【Mac M1】运行情况如下：
➜  bin .&#47;redis-cli --intrinsic-latency 120
Max latency so far: 1 microseconds.
Max latency so far: 3 microseconds.
Max latency so far: 5 microseconds.
Max latency so far: 7 microseconds.
Max latency so far: 17 microseconds.
Max latency so far: 33 microseconds.
Max latency so far: 34 microseconds.
Max latency so far: 35 microseconds.
Max latency so far: 39 microseconds.
Max latency so far: 46 microseconds.
Max latency so far: 48 microseconds.
Max latency so far: 59 microseconds.
Max latency so far: 75 microseconds.
Max latency so far: 109 microseconds.
Max latency so far: 155 microseconds.
Max latency so far: 583 microseconds.
Max latency so far: 1073 microseconds.
Max latency so far: 1127 microseconds.
Max latency so far: 7119 microseconds.
Max latency so far: 9128 microseconds.

2686736240 total runs (avg latency: 0.0447 microseconds &#47; 44.66 nanoseconds per run).
Worst run took 204371x longer than the average latency.
➜  bin </div>2022-04-01</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/7f/91/962eba1a.jpg" width="30px"><span>唐朝首都</span> 👍（2） 💬（8）<div>定时删除是个异步流程吧？为啥会是一个阻塞操作？是要删除的key特别多会导致cpu被大量占用，影响了主线程调用？</div>2020-10-21</li><br/><li><img src="" width="30px"><span>勿更改任何信息</span> 👍（1） 💬（0）<div>Redis过期删除是在主线程里吗</div>2022-10-31</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/92/6d/becd841a.jpg" width="30px"><span>escray</span> 👍（1） 💬（0）<div>执行了一下 redis-cli --intrinsic-latency 120 命令，发现结果比较有意思，两次的结果差不多，从一开始 1 ms 的延迟，一直到后来的 8000+ ms。我访问的是 aliyun 上的 Redis。

```
&gt; redis-cli --intrinsic-latency 120

Max latency so far: 1 microseconds.
Max latency so far: 9 microseconds.
Max latency so far: 11 microseconds.
Max latency so far: 15 microseconds.
Max latency so far: 18 microseconds.
Max latency so far: 96 microseconds.
Max latency so far: 118 microseconds.
Max latency so far: 122 microseconds.
Max latency so far: 221 microseconds.
Max latency so far: 1047 microseconds.
Max latency so far: 1677 microseconds.
Max latency so far: 3378 microseconds.
Max latency so far: 4173 microseconds.
Max latency so far: 8509 microseconds.
2085259894 total runs (avg latency: 0.0575 microseconds &#47; 57.55 nanoseconds per run).
Worst run took 147862x longer than the average latency.
```

Redis 性能诊断的三个关键点：Redis 自身特性、操作系统、文件系统

Value 类型为 String 时，操作复杂度 O(1)，这个也解释了为什么有一些公司用 Redis 的时候，String 到底。

Value 类型为 Set 时，Sort、SUNION&#47;SMEMBERS 操作复杂度分别为 O(N+M*log(M)) 和 O(N)，后一个好理解，前面的那个估计得琢磨一下。

用 SSCAN 多次迭代返回代替 SMEMBERS 返回集合中所有成员。
KEYS 命令一般不用于生产环境。
不要让一批 key 的过期时间相同，可以加一个随机数

对于课后题，在生产环境中代替 KEYS 命令，返回与输入模式匹配的 keys，可以使用 SSCAN 分批次返回。

执行了一下 @泠小墨 留言中的例子，结果稍微有点意外

```
&gt; keys *
 1) &quot;1101001&quot;
 2) &quot;page1:uv&quot;
 3) &quot;aa&quot;
 4) &quot;comments&quot;
 5) &quot;aaa&quot;
 6) &quot;1101000&quot;
 7) &quot;zr&quot;
 8) &quot;testzset&quot;
 9) &quot;mqback&quot;
10) &quot;mylist&quot;
11) &quot;testkey&quot;
12) &quot;mqstream&quot;
13) &quot;a&quot;
14) &quot;testhash&quot;
15) &quot;hell&quot;
16) &quot;hello&quot;
&gt; scan 0 count 1
1) &quot;8&quot;
2) 1) &quot;1101001&quot;
&gt; scan 0 count 2
1) &quot;12&quot;
2) 1) &quot;1101001&quot;
   2) &quot;comments&quot;
```

在 课代表 @kaito 的提示下，看了一下 Redis 在 SCAN 时采用的 高位进位法，确实浅显易懂。</div>2021-03-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/7d/41/3c5b770b.jpg" width="30px"><span>喵喵喵</span> 👍（1） 💬（0）<div>打卡</div>2020-10-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/30/95/76/3965ac00.jpg" width="30px"><span>Jessie</span> 👍（0） 💬（0）<div>有一个小问题，这种采样+检测过期率的删除策略是不是不太合理呀，如果是均匀采样的话，那理论上采样中的过期率和剩余数据的过期率应该是一致且不变的，会不会有一直无法跳出循环的情况？</div>2024-08-25</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/d6/47/30132a10.jpg" width="30px"><span>朱</span> 👍（0） 💬（0）<div>老师您好，我们在生产上遇到两次延迟突然翻倍的问题，第一次碰到这个问题一个小时后自动恢复了，第二次是强行切换了主节点恢复了。我们的用的是主从+哨兵模式，每个虚拟机16G物理内存8核CPU，redis配置maxmemory为10G，只开了RDB，未开启AOF。平常运行时redis内存用量一直在10G左右，一直存在有key被淘汰的情况，单个CPU使用率90%-100%，有一些慢查询（hgetall 9M大小），查询响应翻倍前和后，以上情况都是一样的。不知道为什么会突然延迟变高…查询量也没有明显变多。我有两个猜测，1:内存用量一直在maxmemory附近，触发key淘汰，但淘汰key是后台线程处理，这个是否会影响主线程性能？2:maxmemory设置高于服务器实际内存45%，进行快照时是否有可能触发主线程swap？ 麻烦老师指点迷津</div>2024-04-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/19/5b/08/b0b0db05.jpg" width="30px"><span>丁丁历险记</span> 👍（0） 💬（0）<div>别的不知道，反正我们只准setex</div>2024-02-12</li><br/><li><img src="" width="30px"><span>Geek_c5eb91</span> 👍（0） 💬（0）<div>老师，RedisTemplate 渐进式scan 元素兼容redis集群吗</div>2022-10-17</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/MOuCWWOnoQjOr8KjicQ84R7xu6DRcfDv3VAuHseGJ1gxXicKJboA24vOcrcJickTJPwFAU38VuwCGGkGq7f8WkTIg/132" width="30px"><span>Geek_b14c55</span> 👍（0） 💬（0）<div>可以使用SCAN来代替keys 命令，SCAN是全表扫</div>2022-08-13</li><br/><li><img src="" width="30px"><span>林雪杉</span> 👍（0） 💬（0）<div>`---ts=2022-08-12 14:39:45;thread_name=DubboServerHandler-10.11.113.168:18001-thread-32;id=2fc;is_daemon=true;priority=5;TCCL=org.springframework.boot.loader.LaunchedURLClassLoader@6aaa5eb0
        +---[0.00187ms] io.lettuce.core.internal.AbstractInvocationHandler$MethodTranslator:get() #62

    `---[16.727451ms] io.lettuce.core.FutureSyncInvocationHandler:handleInvocation()        +---[0.002098ms] io.lettuce.core.FutureSyncInvocationHandler:isTxControlMethod() #69

        +---[0.00123ms] io.lettuce.core.FutureSyncInvocationHandler:isTransactionActive() #69        +---[0.002434ms] io.lettuce.core.internal.AbstractInvocationHandler$MethodTranslator:get() #62

        +---[0.002282ms] io.lettuce.core.FutureSyncInvocationHandler:getTimeoutNs() #73        +---[0.007581ms] io.lettuce.core.FutureSyncInvocationHandler:isTxControlMethod() #69

        `---[15.280161ms] io.lettuce.core.internal.Futures:awaitOrCancel() #75        +---[0.005613ms] io.lettuce.core.FutureSyncInvocationHandler:isTransactionActive() #69


        +---[0.006147ms] io.lettuce.core.FutureSyncInvocationHandler:getTimeoutNs() #73
        `---[16.541098ms] io.lettuce.core.internal.Futures:awaitOrCancel() 
投产前压测，操作redis耗时特别久，老师有什么排查思路吗？</div>2022-08-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/44/47/3ddb94d0.jpg" width="30px"><span>javaadu</span> 👍（0） 💬（2）<div>看完开透的那篇万字长文再来看这篇，感觉不那么累了😂</div>2022-03-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/39/34/10fe2b93.jpg" width="30px"><span>wedde</span> 👍（0） 💬（0）<div>scan可以代替keys命令。但是scan使用不当，依然会拖慢整体redis的响应时间。
scan每次返回不大于count的key数量，包括0个key。如果命令后面带了模糊匹配的话，可能会连续多次scan都获取到0个元素。而spring使用迭代器封装了scan的实现，当调用hasNext()判断时，就有可能触发连续多次scan调用。</div>2022-01-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/18/41/13/bf8e85cc.jpg" width="30px"><span>树心</span> 👍（0） 💬（0）<div>针对课后习题都说用scan解决，还提到如果使用scan时扩容会返回重复key，mark一下待研究。</div>2021-12-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1e/01/c5/b48d25da.jpg" width="30px"><span>cake</span> 👍（0） 💬（0）<div>老师 我有个问题，按到你整个课程的设计，这上下两篇应该在讲Redis 关键系统配置对Redis的影响，为什么会加个Redis 自身操作特性的影响呢？ </div>2021-10-16</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/b5/0d/0e65dee6.jpg" width="30px"><span>FelixFly</span> 👍（0） 💬（0）<div>如何能看到key的过期时间分布？响应慢了怎么判断是由于删除key导致的阻塞？</div>2021-10-15</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/19/d9/ff/b23018a6.jpg" width="30px"><span>Heaven</span> 👍（0） 💬（0）<div>可以利用SCAN来进行命令,对于其中存在的重复key,上层利用set这种天然去重的数据结构来进行接收</div>2021-08-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1a/7f/0e/e3a8dbd9.jpg" width="30px"><span>Liujun</span> 👍（0） 💬（0）<div>监控客户端评论响应时间</div>2021-07-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/cc/de/e28c01e1.jpg" width="30px"><span>剑八</span> 👍（0） 💬（0）<div>删除操作异步化是合适的
查询方面的优化是：
避免使用集合类操作，避免bigkey，避免使用keys这种遍历全部key的操作</div>2021-07-05</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/8b/54/db56a871.jpg" width="30px"><span>李明轩</span> 👍（0） 💬（0）<div>请问  redis插入标记位  是什么意思？</div>2021-06-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/8b/54/db56a871.jpg" width="30px"><span>李明轩</span> 👍（0） 💬（0）<div>redis插入标记位</div>2021-06-29</li><br/>
</ul>