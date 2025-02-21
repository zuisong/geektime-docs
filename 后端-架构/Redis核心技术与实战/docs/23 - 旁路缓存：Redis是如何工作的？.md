你好，我是蒋德钧。

我们知道，Redis提供了高性能的数据存取功能，所以广泛应用在缓存场景中，既能有效地提升业务应用的响应速度，还可以避免把高并发大压力的请求发送到数据库层。

但是，如果Redis做缓存时出现了问题，比如说缓存失效，那么，大量请求就会直接积压到数据库层，必然会给数据库带来巨大的压力，很可能会导致数据库宕机或是故障，那么，业务应用就没有办法存取数据、响应用户请求了。这种生产事故，肯定不是我们希望看到的。

正因为Redis用作缓存的普遍性以及它在业务应用中的重要作用，所以，我们需要系统地掌握缓存的一系列内容，包括工作原理、替换策略、异常处理和扩展机制。具体来说，我们需要解决四个关键问题：

- Redis缓存具体是怎么工作的？
- Redis缓存如果满了，该怎么办？
- 为什么会有缓存一致性、缓存穿透、缓存雪崩、缓存击穿等异常，该如何应对？
- Redis的内存毕竟有限，如果用快速的固态硬盘来保存数据，可以增加缓存的数据量，那么，Redis缓存可以使用快速固态硬盘吗？

这节课，我们来了解下缓存的特征和Redis适用于缓存的天然优势，以及Redis缓存的具体工作机制。

## 缓存的特征

要想弄明白Redis为什么适合用作缓存，我们得清楚缓存都有什么特征。
<div><strong>精选留言（30）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/0f/90/8a/288f9f94.jpg" width="30px"><span>Kaito</span> 👍（316） 💬（63）<div>Redis只读缓存和使用直写策略的读写缓存，这两种缓存都会把数据同步写到后端数据库中，它们的区别在于：

1、使用只读缓存时，是先把修改写到后端数据库中，再把缓存中的数据删除。当下次访问这个数据时，会以后端数据库中的值为准，重新加载到缓存中。这样做的优点是，数据库和缓存可以保证完全一致，并且缓存中永远保留的是经常访问的热点数据。缺点是每次修改操作都会把缓存中的数据删除，之后访问时都会先触发一次缓存缺失，然后从后端数据库加载数据到缓存中，这个过程访问延迟会变大。

2、使用读写缓存时，是同时修改数据库和缓存中的值。这样做的优点是，被修改后的数据永远在缓存中存在，下次访问时，能够直接命中缓存，不用再从后端数据库中查询，这个过程拥有比较好的性能，比较适合先修改又立即访问的业务场景。但缺点是在高并发场景下，如果存在多个操作同时修改同一个值的情况，可能会导致缓存和数据库的不一致。

3、当使用只读缓存时，如果修改数据库失败了，那么缓存中的数据也不会被删除，此时数据库和缓存中的数据依旧保持一致。而使用读写缓存时，如果是先修改缓存，后修改数据库，如果缓存修改成功，而数据库修改失败了，那么此时数据库和缓存数据就不一致了。如果先修改数据库，再修改缓存，也会产生上面所说的并发场景下的不一致。

我个人总结，只读缓存是牺牲了一定的性能，优先保证数据库和缓存的一致性，它更适合对于一致性要求比较要高的业务场景。而如果对于数据库和缓存一致性要求不高，或者不存在并发修改同一个值的情况，那么使用读写缓存就比较合适，它可以保证更好的访问性能。</div>2020-10-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1d/6c/b5/32374f93.jpg" width="30px"><span>可怜大灰狼</span> 👍（29） 💬（25）<div>对只读缓存方式的操作，先删redis，再修改db，最后删redis。用双删保证数据一致性。</div>2020-10-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1e/37/29/b3af57a7.jpg" width="30px"><span>凯文小猪</span> 👍（16） 💬（1）<div>这里有两点问题 老师没有说清楚：
1. 缓存更新模式 常见的就是cache aside 就是老师介绍的只读缓存
2. 读写缓存 有点类似write through 但从老师的叙述中只是特征部分吻合 所以这里要明确指出
 因为这并不是主流的四种更新缓存套路，分别是：cahce aside , write through, read through, write behind.

读写一般是和只读缓存共用的 用于分担热点压力 比如说eureka</div>2021-06-02</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/ec/a7/7d44c655.jpg" width="30px"><span>snailshen</span> 👍（11） 💬（0）<div>区别在于：只读缓存，是以数据库的数据为基准同步缓存的方案，读写缓存是同时修改数据库和缓存中的数据，这两种方案都存在数据一致性的问题。比如只读缓存在写回数据库删除缓存时这个时间段的读请求交易，读写缓存缓存的并发访问问题。
数据一致性问题：1.最终一致性方案，优先修改缓存数据，通过队列解耦修改请求到数据库，后台单独处理队列数据保证数据库数据最终一致性。
2.通过分布式事务，把缓存操作和数据库操作通过一个事务完成。这种情况数据能够强一致性
这两种情况都没办法保证，数据脏读的情况，只能保缓存和数据库的数据一致性，如何在保证缓存和数据的数据一致性的情况下，避免脏读的问题，还请大家讨论！</div>2020-10-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/d5/61/8ad99e09.jpg" width="30px"><span>刘百万</span> 👍（6） 💬（8）<div>我觉得解决所有问题的办法就是给机房配双电源</div>2021-04-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/5c/8f/551b5624.jpg" width="30px"><span>小可</span> 👍（5） 💬（1）<div>只读缓存：
①写时写db，删redis key，写性能好；
②读时读到redis无此key需从db load，只影响修改后首次读性能；
③redis+db数据一致
④适合读多写少场景
直写策略的读写缓存：
①写时同时写redis+db，首先保证同时成功，db写慢会阻塞redis，整体写性能有影响；
②读数据直接读redis，读性能好；
③如果写db成功，写缓存失败，造成数据不一致，但数据可靠性好
④适合读多写少场景，感觉还不如用只读缓存，不知道对不对？</div>2021-02-05</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/49/a5/e4c1c2d4.jpg" width="30px"><span>小文同学</span> 👍（5） 💬（4）<div>分享一个自己在使用缓存的时候遇到的坑：
1、Redis 的缓存数据来自数据库
2、在业务系统上快速对数据进行处理，Redis 是一个热点更新对象
生产环境会遇到这样一个问题：缓存数据从数据库拉取上来的时候，会和任务数据更新Redis冲突，这时候需要分布式锁救场。</div>2020-10-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/49/a5/e4c1c2d4.jpg" width="30px"><span>小文同学</span> 👍（4） 💬（1）<div>针对 Redis 和异步写回策略，等待 Redis 淘汰数据再写回数据库，那 Redis 处理缓存，一定程度上还承担着队列的任务，即向上接受业务的数据，向下把数据写到数据库。

这个情况下，考虑到 Redis 的掉电带来数据丢失的风险，我觉得可以把 Redis 任务方面的需求转移到专业的消息队列中去使用。

这样就需要这样处理：
1、Obj 写 Redis；
2、Obj 入队 Kafka；

由于 Kafka 可以做到数据不丢失，所以这样数据可以更加安全一点，还可以扩展吞吐量。缺点是：引入一个新的中间件，意味着更多更复杂的业务代码结构。</div>2020-10-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/3a/97/c4493e91.jpg" width="30px"><span>一缕阳光</span> 👍（2） 💬（0）<div>一般业务场景下，先写 DB ，后删缓存 + 删除重试已经可以满足大部分一致性要求了。
如果还要说的话，那就是延迟双删，但是具有一定复杂度，至少我们是没有在产线应用的。

或者是，对于某些场景，也可以在单用户维度做一个简单的分布式锁来限制一下并发，这样也可以降低出现不一致的概率。 

另外，就是和数据库事务一起的一些思考🤔：由于快照读的存在，事务内不对缓存做写操作，也可以根据业务场景来看事务结束后是否需要额外做一次删除缓存。
</div>2021-08-22</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTKo5jCPQW87sFySwXiaLxibak0qQYuFRTyy8RlNsO9JDyxBk1AYDrsphRskxzXPLPOW8ibWicWlRAnzwg/132" width="30px"><span>Kevin</span> 👍（2） 💬（0）<div>只读就是宏观上的mysql；读写就是微观的mysql操作，数据变更的终点在内存，数据落盘由日志操作</div>2020-11-16</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/bc/25/1c92a90c.jpg" width="30px"><span>tt</span> 👍（2） 💬（2）<div>对于只读缓存这个名字来说，感觉很奇怪，今天学完25讲记笔记的时候，回过头来又看了今天的内容，又想了想这个问题，有了下面的想法，不知道正确不正确？

这里的只读不是说缓存中的数据不会改变，而是说对于只读缓存来讲，没有更新操作，只有读取和删除操作。在数据更新时，只会写数据库，然后对于缓存来讲，更新操作分解为删除和插入操作，即

只读缓存的更新 = 删除 + 插入。
</div>2020-10-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/ac/96/46b13896.jpg" width="30px"><span>williamcai</span> 👍（2） 💬（3）<div>老师，您好，读写缓存无论是先写数据库还是缓存，都有可能出现其中一个失败的情况，造成数据不一致的情况，这个问题你有什么好的方案吗
</div>2020-10-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/01/c4/21c2cde4.jpg" width="30px"><span>窗外</span> 👍（2） 💬（2）<div>老师好，同步直写时，怎么保障 redis mysql 的操作具有原子性呢?不具有原子性的话两者数据可能就不一致了</div>2020-10-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/23/3b/35/e1f0e060.jpg" width="30px"><span>3-</span> 👍（1） 💬（0）<div>只读缓存-更新数据库，然后删除缓存，问题来了，你都删除缓存了，为什么不把这一步改成更新缓存呢？不然下次请求还要查数据库</div>2023-04-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/28/94/ec/8db3f04a.jpg" width="30px"><span>喰</span> 👍（1） 💬（0）<div>个人觉得只读缓存和读写缓存都会存在一致性问题，只读缓存的优点是强调数据可靠性，而读写缓存的优点是强调响应时间。  一致性问题都会存在。</div>2021-07-01</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/ee/ce/c024a857.jpg" width="30px"><span>藏锋</span> 👍（1） 💬（0）<div>只读缓存，实际上就是由数据库来驱动缓存的更新，从理论上讲，缓存的数据始终和数据库保持一致，不过如果修改数据库成功，删除缓存失败，那么缓存中的数据在缓存未过期之前就是脏数据；</div>2021-04-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/ed/eb/88cac7a5.jpg" width="30px"><span>东</span> 👍（1） 💬（0）<div>关于cache的写策略，就是write through和write back，维基百科上有完整的介绍。
https:&#47;&#47;en.wikipedia.org&#47;wiki&#47;Cache_(computing)#&#47;media&#47;File:Write-through_with_no-write-allocation.svg
https:&#47;&#47;en.wikipedia.org&#47;wiki&#47;Cache_(computing)#&#47;media&#47;File:Write-back_with_write-allocation.svg
</div>2020-10-10</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTJ5Wh2AdV0pAEOFU7uFJxqjpViaeZayicRBg6fNFShmszP2nqQLJh22HytnBHYXG9gAnYXJmzeF11kA/132" width="30px"><span>Geek_a8489f</span> 👍（1） 💬（3）<div>读写模式+同步直写策略，感觉意义不大吧？写操作仍然需要更新DB，无法实现写操作的加速。</div>2020-10-09</li><br/><li><img src="" width="30px"><span>Geek_fef55b</span> 👍（0） 💬（0）<div>“缓存中的数据需要按一定规则淘汰出去，写回后端系统”，这里的“缓存淘汰了，为什么要写回后端系统呢”，老师，这个没有理解。</div>2023-11-23</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/tKvmZ3Vs4t6RZ3X7cAliaW47Zatxhn1aV5PcCYT9NZ9k9WWqRrEBGHicGtRWvsG6yQqHnaWw6cGNSbicNLjZebcHA/132" width="30px"><span>柳十三</span> 👍（0） 💬（0）<div>只读缓存，删改的时候，删除缓存;读写缓存，修改的时候会修改缓存，删除的时候会删除缓存</div>2023-08-01</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/74/aa/178a6797.jpg" width="30px"><span>阿昕</span> 👍（0） 💬（0）<div>区别在于，直写策略的读写缓存是同步进行的，会阻塞处理过程</div>2022-04-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/28/6c/bc/f751786b.jpg" width="30px"><span>Ming</span> 👍（0） 💬（0）<div>1. 只读缓存，用的比较多，保证数据库和缓存一致性使用延迟双删策略；
 2. 读写缓存，缓存后数据库的修改是分开的，保证最终一致性较难，如果业务中对最终一致性要求不高建议使用；</div>2022-04-01</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/46/a0/aa6d4ecd.jpg" width="30px"><span>张潇赟</span> 👍（0） 💬（2）<div>只读缓存和读写缓存，这两种从一致性的角度考虑应该是只读缓存更可靠一点。从性能的角度考虑感觉没啥区别，不管是同步写还是异步写都可以用代码的形式搞定。
在生产环境中除了考虑一致性和性能两个因素外还需要考虑一个就是维护成本，感觉如果采用读写缓存的方案会给redis集群带来更高的复杂度，也会对后期的扩展带来不变。</div>2022-03-28</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTK0G3cibDykvgIkomb5QrjBGuiaf5rJG2317JN1sePZ589IjUcMTOF4ZMrKVYU4ywfq1qfREqCW9Zww/132" width="30px"><span>1634LM</span> 👍（0） 💬（1）<div>老师 您好 ，我是小白 对于只读缓存  我有点疑惑：“当应用再次读取这些数据时，会发生缓存缺失，应用会把这些数据从数据库中读出来，并写到缓存中” 并把数据写到缓存中，缓存不是只读的吗  怎么可以把数据写到缓存中呢 ？ 我理解的只读 是 只能读不能更新，删除 和插入啊？ </div>2022-01-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/3d/6c/935bdc7d.jpg" width="30px"><span>‭‭</span> 👍（0） 💬（0）<div>读写缓存路径更短一些，少了从数据库加载，会出现并发问题。原子性问题都有</div>2021-12-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/27/3c/1b/07c453a7.jpg" width="30px"><span>Sean</span> 👍（0） 💬（0）<div>请问老师，读写缓存为什么会影响redis的性能？感觉也只是响应请求会慢一些啊</div>2021-12-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/18/41/13/bf8e85cc.jpg" width="30px"><span>树心</span> 👍（0） 💬（0）<div>这节课老师讲的比较简单，继续下一节～</div>2021-12-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/19/d9/ff/b23018a6.jpg" width="30px"><span>Heaven</span> 👍（0） 💬（0）<div>只读缓存就好比mysql的缓存层，而MySQL缓存层已经被MySQL抛弃了。</div>2021-08-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/cc/de/e28c01e1.jpg" width="30px"><span>剑八</span> 👍（0） 💬（0）<div>还是从场景上去看：
只读缓存用于读性能提高的场景，比如常量数据。
读写缓存则是用于提升读写性能。
读缓存的数据库更新由应用去做，另外一个业务模块去做，同时删除读缓存。
读写缓存更新数据库则是直接由当前写操作直接做掉了，同时进行数据库操作及缓存删除。
读写缓存实际上是用于存储了，这个在不是同步刷盘的情况可能会丢失数据。</div>2021-07-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/27/05/a2/3fa5a070.jpg" width="30px"><span>吃橘子的汤圆🐳</span> 👍（0） 💬（0）<div>只读缓存观点：
1：:高并发场景下
2：T1 更新数据库 更新缓存
3：T2 更新数据库 更新缓存 T1由于某些原因比T2晚更新缓存
4：最终缓存保存T1数据 出现脏数据</div>2021-06-09</li><br/>
</ul>