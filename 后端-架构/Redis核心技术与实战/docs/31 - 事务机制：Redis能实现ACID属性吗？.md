你好，我是蒋德钧。

事务是数据库的一个重要功能。所谓的事务，就是指对数据进行读写的一系列操作。事务在执行时，会提供专门的属性保证，包括原子性（Atomicity）、一致性（Consistency）、隔离性（Isolation）和持久性（Durability），也就是ACID属性。这些属性既包括了对事务执行结果的要求，也有对数据库在事务执行前后的数据状态变化的要求。

那么，Redis可以完全保证ACID属性吗？毕竟，如果有些属性在一些场景下不能保证的话，很可能会导致数据出错，所以，我们必须要掌握Redis对这些属性的支持情况，并且提前准备应对策略。

接下来，我们就先了解ACID属性对事务执行的具体要求，有了这个知识基础后，我们才能准确地判断Redis的事务机制能否保证ACID属性。

## 事务ACID属性的要求

首先来看原子性。原子性的要求很明确，就是一个事务中的多个操作必须都完成，或者都不完成。业务应用使用事务时，原子性也是最被看重的一个属性。

我给你举个例子。假如用户在一个订单中购买了两个商品A和B，那么，数据库就需要把这两个商品的库存都进行扣减。如果只扣减了一个商品的库存，那么，这个订单完成后，另一个商品的库存肯定就错了。
<div><strong>精选留言（30）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/12/0a/a4/828a431f.jpg" width="30px"><span>张申傲</span> 👍（13） 💬（4）<div>Redis 为什么不支持事务的回滚？可以参考下官网的解释：https:&#47;&#47;redis.io&#47;topics&#47;transactions </div>2020-12-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/20/5c/af/2215f3b6.jpg" width="30px"><span>徐小熊</span> 👍（3） 💬（7）<div>我想问一下redis能否做到替代mysql作为数据来使用呢？因为redis可以使用aof日志记录命令，开启everysecond的话最多只会让一秒钟的数据丢失。如果可以接受这一秒钟丢失的数据情况的话，是不是完全可以替代mysql作为数据库啊？
</div>2020-11-02</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/90/8a/288f9f94.jpg" width="30px"><span>Kaito</span> 👍（257） 💬（36）<div>在执行事务时，如果 Redis 实例发生故障，而 Redis 使用的 RDB 机制，事务的原子性还能否得到保证？

我觉得是可以保证原子性的。

如果一个事务只执行了一半，然后 Redis 实例故障宕机了，由于 RDB 不会在事务执行时执行，所以 RDB 文件中不会记录只执行了一部分的结果数据。之后用 RDB 恢复实例数据，恢复的还是事务之前的数据。但 RDB 本身是快照持久化，所以会存在数据丢失，丢失的是距离上一次 RDB 之间的所有更改操作。

关于 Redis 事务的使用，有几个细节我觉得有必要补充下，关于 Pipeline 和 WATCH 命令的使用。

1、在使用事务时，建议配合 Pipeline 使用。

a) 如果不使用 Pipeline，客户端是先发一个 MULTI 命令到服务端，客户端收到 OK，然后客户端再发送一个个操作命令，客户端依次收到 QUEUED，最后客户端发送 EXEC 执行整个事务（文章例子就是这样演示的），这样消息每次都是一来一回，效率比较低，而且在这多次操作之间，别的客户端可能就把原本准备修改的值给修改了，所以无法保证隔离性。

b) 而使用 Pipeline 是一次性把所有命令打包好全部发送到服务端，服务端全部处理完成后返回。这么做好的好处，一是减少了来回网络 IO 次数，提高操作性能。二是一次性发送所有命令到服务端，服务端在处理过程中，是不会被别的请求打断的（Redis单线程特性，此时别的请求进不来），这本身就保证了隔离性。我们平时使用的 Redis SDK 在使用开启事务时，一般都会默认开启 Pipeline 的，可以留意观察一下。

2、关于 WATCH 命令的使用场景。

a) 在上面 1-a 场景中，也就是使用了事务命令，但没有配合 Pipeline 使用，如果想要保证隔离性，需要使用 WATCH 命令保证，也就是文章中讲 WATCH 的例子。但如果是 1-b 场景，使用了 Pipeline 一次发送所有命令到服务端，那么就不需要使用 WATCH 了，因为服务端本身就保证了隔离性。

b) 如果事务 + Pipeline 就可以保证隔离性，那 WATCH 还有没有使用的必要？答案是有的。对于一个资源操作为读取、修改、写回这种场景，如果需要保证事物的原子性，此时就需要用到 WATCH 了。例如想要修改某个资源，但需要事先读取它的值，再基于这个值进行计算后写回，如果在这期间担心这个资源被其他客户端修改了，那么可以先 WATCH 这个资源，再读取、修改、写回，如果写回成功，说明其他客户端在这期间没有修改这个资源。如果其他客户端修改了这个资源，那么这个事务操作会返回失败，不会执行，从而保证了原子性。

细节比较多，如果不太好理解，最好亲自动手试一下。</div>2020-10-30</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/bc/25/1c92a90c.jpg" width="30px"><span>tt</span> 👍（35） 💬（12）<div>	• 原子性就是一批操作，要不全部完成，要不一个也不执行。
	• 原子性的结果就是中间结果对外不可见，如果中间结果对外可见，则一致性就不会得到满足（比如操作）。
	• 而隔离性，指一个事务内部的操作及使用的数据对正在进行的其他事务是隔离的，并发执行的各个事务之间不能互相干扰，正是它保证了原子操作的过程中，中间结果对其它事务不可见。

本文在讨论一致性的时候，说到“ 命令入队时没报错，实际执行时报错在这种情况下，有错误的命令不会被执行，正确的命令可以正常执行，也不会改变数据库的一致性。”，我觉得这一点是存疑的，不保证原子性就保证不了一致性。比如转账操作，扣减转出账户的操作成功，增加转入账户的操作失败，则原子性和一致性都被破坏。
</div>2020-11-02</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/43/79/18073134.jpg" width="30px"><span>test</span> 👍（17） 💬（0）<div>redis开启RDB，因为RDB不会在事务执行的时候执行，所以是可以保证原子性的</div>2020-10-30</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/49/a5/e4c1c2d4.jpg" width="30px"><span>小文同学</span> 👍（10） 💬（1）<div>1、作者讲了什么？
作者通过本文讨论，Redis 是否可以保证 ACID 的事务功能。事务是对数据进行一系列操作。
2、作者是怎么把事情说明白的？
作者先讨论 事务ACID 属性的要求：然后作者说明了 Redis 的 API ：MULTI 和 EXEC 是如何完成事务的；完成说明后，作者开始针对事务的每个特性，讨论 Redis 是否已经完成达成。
2.1 原子性。原子性的保证分三种情况
2.1.1 队列中有命令存在错误，队列清空；（可保证原子）
2.1.2 队列中命令到执行的时候才被发现有错误，不会滚，执行多少算多少；（不保证原子）
2.1.3 EXEC 时， Redis 实例发生故障。这个涉及到日志，AOF 的 redis-check-aof 可以发现没执行完成的操作，进而清除；（可以保证原子）
2.2 一致性。作者分三种情况说明，并且确认都可以提供一致性。
2.3 隔离性。WATCH 机制提供事务隔离性。
2.4 持久性。Redis 任何时候都无法提供持久性保障。

3、为了讲明白，作者讲了哪些要点？哪些是亮点？
在 Redis 的事务上，作者通过 三种情况 ，分别说明了 Redis 是否满足 ACID 特性，这个划分方法是一个亮点；

4、对于作者所讲，我有哪些发散性思考？
Redis 始终坚持是一个高性能的内存数据库，并没有因为事务的重要性而放弃这一个宗旨，故在内存中实现了隔离性，一致性，有条件原子性，不实现持久性。这个也可以放映出 Redis 的定位和一般数据库 MySQL 是不一样的；

5、在未来哪些场景，我可以使用它？
在高并发，竞争环境下，需要保证数据正确时，可以考虑 Redis 的事务性实现。</div>2020-12-04</li><br/><li><img src="" width="30px"><span>与君共勉</span> 👍（6） 💬（5）<div>AOF如果开启always模式不是可以保证数据不丢失吗？为啥也保证不了持久性呢？</div>2020-10-30</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/19/29/a1/41607383.jpg" width="30px"><span>hello</span> 👍（5） 💬（4）<div>“错误的命令不会被执行，正确的命令可以正常执行，也不会改变数据库的一致性”这个怎么就没有改变数据库的一致性了呢？我是菜鸟一枚，有大神指点一二吗？</div>2020-11-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/20/99/5e/33481a74.jpg" width="30px"><span>Lemon</span> 👍（5） 💬（4）<div>老师，我对Redis能保证一致性这点表示困惑：在命令入队时没有报错，实际执行时报错的情况下，如果A给B转账，A的账户被扣钱了，此时命令出错，B账户并没有增加转账金额，这不就导致了事务前后的数据不一致了吗？</div>2020-11-02</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/c9/5e/b79e6d5d.jpg" width="30px"><span>꧁子华宝宝萌萌哒꧂</span> 👍（4） 💬（6）<div>老师，在上一节中，分布式锁重要的就是保证操作的原子性，既然事物能保证原子性，为啥上一节中没有提到用事物来做呢？</div>2020-10-30</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTJF1c2h1dCWAkdvs049lb3y7vzIicvv2kZOZwEFpUyhxmmehdpVicWGBaSsGv2TPkuastTW0MgxoLxg/132" width="30px"><span>吕宁博</span> 👍（3） 💬（1）<div>显然大家对关系型数据库ACID的C没理解透彻。C是通过用户自定义的一系列“数据类型、约束、触发器”等保证的。就拿银行取钱来说，如果用户没设置check(balance&gt;=0)，即使最终因为各种原因导致balance&lt;0，那也没违反C。数据库是在一定的系统+用户规则下运行的，只要没违反规则，就是保证了C。

数据库只是个软件，理解C的时候不要把现实世界的规则强加给它，除非你明确告诉它规则（数据类型、约束、触发器），否则它就是一个满足前后一致性状态规则的C。

这样理解C比较简单：我（数据库）管你balance是不是小于0，你又没告诉我（设置check），那我小于0违法了吗？</div>2021-07-22</li><br/><li><img src="" width="30px"><span>JohnReese</span> 👍（3） 💬（6）<div>那请问老师，Multi 命令 和 Lua脚本 的功能上有什么区别嘛？（似乎都是保证‘原子性’地执行多命令？）</div>2020-10-30</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/60/a1/45ffdca3.jpg" width="30px"><span>静心</span> 👍（3） 💬（3）<div>老师，在集群模式下，ACID是个什么情况？</div>2020-10-30</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/3a/a2/7c/be30e54c.jpg" width="30px"><span>不动</span> 👍（1） 💬（0）<div>这里的一致性到底是什么含义，没搞懂</div>2024-04-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/9c/53/ade0afb0.jpg" width="30px"><span>ub8</span> 👍（1） 💬（0）<div>老师redis的pipline 可以保证执行命令结果集按顺序返回么：具体操作如下：
Pipeline pipeline = jedis.pipelined();
            Map&lt;Integer,PrizeConfig&gt; day2PrizeConfigMap = new HashMap&lt;&gt;();
            Map&lt;Integer,redis.clients.jedis.Response&lt;Set&lt;Tuple&gt;&gt;&gt; day2PrizeCache = new HashMap&lt;&gt;();
            for (Integer dayIndex : days) {
                String cacheKey = String.format(SignInConstants.PRIZE_VERSION_KEY,
                        dayIndex);
                redis.clients.jedis.Response&lt;Set&lt;Tuple&gt;&gt; prizeConfigsResponse  =
                        pipeline.zrevrangeByScoreWithScores(cacheKey, version, 0);
                day2PrizeCache.put(dayIndex, prizeConfigsResponse);
            }
            pipeline.sync();
&#47;&#47; 我的问题是 day2PrizeCache 这个map中的 dayIndex 和 返回值prizeConfigsResponse 可以对应关系有可能发生错位吗？</div>2021-08-26</li><br/><li><img src="" width="30px"><span>Geek_da8c85</span> 👍（0） 💬（0）<div>一致性：
中途失败了，无法回滚，其实是无法保证一致性的</div>2024-10-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/9a/ab/fd201314.jpg" width="30px"><span>小耿</span> 👍（0） 💬（0）<div>事务的原子性是指所有命令要么都完成，要么都不执行。事务执行到中间 redis 实例故障，分两种情况：一是如果事务执行期间开始 RDB 备份，当redis实例发生故障时，无法保证原子性，因为此时会将执行到一半的命令备份到 RDB 文件；如果事务执行期间未开始 RDB 备份，那么可以保证原子性，因为使用 RDB 文件恢复时不会恢复执行的部分命令。</div>2023-09-27</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/DYAIOgq83erZCyXaP2gbxwFHxvtnyaaF2Pyy5KkSMsk9kh7SJl8icp1CD6wicb6VJibiblGibbpDo6IuHrdST6AnWQg/132" width="30px"><span>Geek_1cc6d1</span> 👍（0） 💬（0）<div>隔离性即便是数据库也是分多种级别，redis一个watch怎么能解决呢。就像插入操作，watch的时候都还没key呢</div>2023-09-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/26/be/e9/9d597e04.jpg" width="30px"><span>豆豆酱</span> 👍（0） 💬（0）<div>我感觉可以从两个方面来看：单机版本的一致性和分布式版本的一致性。
分布式的话主要依赖主从同步，这块是能有一个最终一致的。
单机的话，主要看事务里边的操作，是不是客户端执行完成后，他能一直看到提交成功后的结果（或者是提交前的，因为是个内存数据库，重启的话会丢数据）。
只要能保证看到的一定是提交前，或者提交后的，那他就是一致的。</div>2023-06-02</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/Z8t0JKFjnmdx4s4wuRePZXRL2L9awEpicp0rjT9rfXmZKOBIleZuOC86OzZE0tSdkfy3LWWa7YU67MicWeiaFd3jA/132" width="30px"><span>小白</span> 👍（0） 💬（0）<div>文中的例子 DISCARD ，这个起到的效果不是和回滚的效果是一样的嘛，为什么不能算回滚？</div>2022-09-20</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/MOuCWWOnoQjOr8KjicQ84R7xu6DRcfDv3VAuHseGJ1gxXicKJboA24vOcrcJickTJPwFAU38VuwCGGkGq7f8WkTIg/132" width="30px"><span>Geek_b14c55</span> 👍（0） 💬（2）<div>如果使用了rdb机制，事务的原子性没办法保证，因为已经有部分数据落盘了，所以没办法保证原子性</div>2022-09-07</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/22/bd/9b/366bb87b.jpg" width="30px"><span>飞龙</span> 👍（0） 💬（0）<div>我测试的结果貌似和有些例子不太一样，开启multi lpop a:stock;decr b:stock  exec   因为a:stock类型对不上报错，b:stock并没有执行。</div>2022-08-09</li><br/><li><img src="" width="30px"><span>风之翼</span> 👍（0） 💬（0）<div>在使用 watch 机制后，若存在并发写多个变量的情况，在 watch 到变量发生变化后，停止事务执行前，已经做的修改会回滚吗</div>2022-08-05</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTKq0oQVibKcmYJqmpqaNNQibVgia7EsEgW65LZJIpDZBMc7FyMcs7J1JmFCtp06pY8ibbcpW4ibRtG7Frg/132" width="30px"><span>zhoufeng</span> 👍（0） 💬（1）<div>既然redis能实现事务的隔离性，为什么在应对多客户端并发访问时，还需要争抢分布式锁呢？</div>2022-07-25</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/9c/53/ade0afb0.jpg" width="30px"><span>ub8</span> 👍（0） 💬（0）<div>越看评论越蒙</div>2022-04-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/24/27/77/8493aa4a.jpg" width="30px"><span>伟</span> 👍（0） 💬（0）<div>可以</div>2022-02-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/cc/de/e28c01e1.jpg" width="30px"><span>剑八</span> 👍（0） 💬（0）<div>能保证一致性隔离性
不能保证原子性，持久性</div>2022-02-05</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/DYAIOgq83eqOn7k48KXia5rf0eXpzv2EGtqGibz3eNb8QnL8X72uia0g1rBwzXef4dV2JEdz3r4bu9GC1FLIeic4UA/132" width="30px"><span>Lee</span> 👍（0） 💬（1）<div>watch机制也不一定能完全保证隔离性吧！例如，watch也是离散时间内的监控，执行EXEC 命令过程中最后一刻，其他写请求对队列中的值做了修改，也是有问题的</div>2022-01-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/19/d9/ff/b23018a6.jpg" width="30px"><span>Heaven</span> 👍（0） 💬（0）<div>只是原子性的话是可以保证的,因为Redis并不会在执行事务期间进行快照,所以RDB只会在完成事务之后进行,对于原子性可以保证,持久性不会保证
</div>2021-08-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/28/c3/13/d1519146.jpg" width="30px"><span>大脸驴</span> 👍（0） 💬（0）<div>关于一致性的说明，有点没理解，“情况二，命令入队时没报错，实际执行时报错”，这种情况下，如果有部分命令失败，另外一部分命令成功了，有两个问题，1.为什么这个不影响数据库的一致性；2.此时一致性，和原子性有什么差异；我理解的是此时，数据和预期不一致了，数据库一致性应该受到影响才对</div>2021-08-11</li><br/>
</ul>