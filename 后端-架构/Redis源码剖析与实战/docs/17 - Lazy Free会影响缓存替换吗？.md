你好，我是蒋德钧。

Redis缓存淘汰算法的目的，其实是为了在Redis server内存使用量超过上限值的时候，筛选一些冷数据出来，把它们从Redis server中删除，以保证server的内存使用量不超出上限。我们在前两节课，已经分别学习了Redis源码对LRU算法和LFU算法的实现，这两种算法在最后淘汰数据的时候，都会删除被淘汰的数据。

不过，无论是LRU算法还是LFU算法，它们在删除淘汰数据时，实际上都会根据Redis server的**lazyfree-lazy-eviction配置项**，来决定是否使用Lazy Free，也就是惰性删除。

惰性删除是Redis 4.0版本后提供的功能，它会使用后台线程来执行删除数据的任务，从而避免了删除操作对主线程的阻塞。但是，**后台线程异步删除数据能及时释放内存吗？它会影响到Redis缓存的正常使用吗？**

今天这节课，我就来给你介绍下惰性删除在缓存淘汰时的应用。了解这部分内容，你就可以掌握惰性删除启用后，会给Redis缓存淘汰和内存释放带来的可能影响。这样，当你在实际应用中，遇到Redis缓存内存容量的问题时，你就多了一条排查思路了。

好，那么接下来，我们就先来看下缓存淘汰时的数据删除的基本过程。不过在了解这个删除过程之前，我们需要先了解下Redis server启动惰性删除的配置。因为在Redis源码中，有不少地方都会根据server是否启动惰性删除，来执行不同的分支操作。
<div><strong>精选留言（6）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/1b/89/52/b96c272d.jpg" width="30px"><span>🤐</span> 👍（3） 💬（0）<div>从源码可以体会到redis作者的精益求精</div>2022-07-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/90/8a/288f9f94.jpg" width="30px"><span>Kaito</span> 👍（26） 💬（10）<div>1、lazy-free 是 4.0 新增的功能，默认是关闭的，需要手动开启

2、开启 lazy-free 时，有多个「子选项」可以控制，分别对应不同场景下，是否开启异步释放内存：

a) lazyfree-lazy-expire：key 在过期删除时尝试异步释放内存
b) lazyfree-lazy-eviction：内存达到 maxmemory 并设置了淘汰策略时尝试异步释放内存
c) lazyfree-lazy-server-del：执行 RENAME&#47;MOVE 等命令或需要覆盖一个 key 时，Redis 内部删除旧 key 尝试异步释放内存
d) replica-lazy-flush：主从全量同步，从库清空数据库时异步释放内存

3、即使开启了 lazy-free，但如果执行的是 DEL 命令，则还是会同步释放 key 内存，只有使用 UNLINK 命令才「可能」异步释放内存

4、Redis 6.0 版本新增了一个新的选项 lazyfree-lazy-user-del，打开后执行 DEL 就与 UNLINK 效果一样了

5、最关键的一点，开启 lazy-free 后，除 replica-lazy-flush 之外，其它选项都只是「可能」异步释放 key 的内存，并不是说每次释放 key 内存都是丢到后台线程的

6、开启 lazy-free 后，Redis 在释放一个 key 内存时，首先会评估「代价」，如果代价很小，那么就直接在「主线程」操作了，「没必要」放到后台线程中执行（不同线程传递数据也会有性能消耗）

7、什么情况才会真正异步释放内存？这和 key 的类型、编码方式、元素数量都有关系（详见 lazyfreeGetFreeEffort 函数）：

a) 当 Hash&#47;Set 底层采用哈希表存储（非 ziplist&#47;int 编码存储）时，并且元素数量超过 64 个
b) 当 ZSet 底层采用跳表存储（非 ziplist 编码存储）时，并且元素数量超过 64 个
c) 当 List 链表节点数量超过 64 个（注意，不是元素数量，而是链表节点的数量，List 底层实现是一个链表，链表每个节点是一个 ziplist，一个 ziplist 可能有多个元素数据）

只有满足以上条件，在释放 key 内存时，才会真正放到「后台线程」中执行，其它情况一律还是在主线程操作。

也就是说 String（不管内存占用多大）、List（少量元素）、Set（int 编码存储）、Hash&#47;ZSet（ziplist 编码存储）这些情况下的 key，在释放内存时，依旧在「主线程」中操作。

8、可见，即使打开了 lazy-free，String 类型的 bigkey，在删除时依旧有「阻塞」主线程的风险。所以，即便 Redis 提供了 lazy-free，还是不建议在 Redis 存储 bigkey

9、Redis 在释放内存「评估」代价时，不是看 key 的内存大小，而是关注释放内存时的「工作量」有多大。从上面分析可以看出，如果 key 内存是连续的，释放内存的代价就比较低，则依旧放在「主线程」处理。如果 key 内存不连续（包含大量指针），这个代价就比较高，这才会放在「后台线程」中执行

课后题：freeMemoryIfNeeded 函数在使用后台线程，删除被淘汰数据的过程中，主线程是否仍然可以处理外部请求？

肯定是可以继续处理请求的。

主线程决定淘汰这个 key 之后，会先把这个 key 从「全局哈希表」中剔除，然后评估释放内存的代价，如果符合条件，则丢到「后台线程」中执行「释放内存」操作。

之后就可以继续处理客户端请求，尽管后台线程还未完成释放内存，但因为 key 已被全局哈希表剔除，所以主线程已查询不到这个 key 了，对客户端来说无影响。</div>2021-09-02</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/OAykKXiaicxfx5Mx5VvF5vf9Sfqz30qW06hSNsUky5BB4HiaTYibpluIn1SH9VpYftgBLZe5O0HhsMP0lCN5p8kWpw/132" width="30px"><span>Geek_轻风</span> 👍（1） 💬（0）<div>异步删除后，一直要等到检查满足已释放足够内存的条件才会停止删除。所以，最开始的几次异步删除后不会立刻结束这个函数。后面还有异步删除的话，说不定之前的异步删除已经释放了足够的内存，所以退出了删除循环。这个函数退出后，Redis才能接着处理网络请求</div>2023-03-06</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/17/8b/4b/15ab499a.jpg" width="30px"><span>风轻扬</span> 👍（0） 💬（0）<div>回答一下课后题。
后台线程是将任务放进了队列中，在放的这个过程中，是主线程的同步操作，在这一瞬间，redis是不能对外处理请求的，但是一旦将任务放进了队列中，后面的释放工作就是由后台任务执行，主线程就可以处理客户端的请求了</div>2023-11-15</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/d4/d6/1d4543ac.jpg" width="30px"><span>云海</span> 👍（0） 💬（2）<div>惰性删除，每删除16个key后会计算一次内存。那么问题来了，计算内存的操作是否会消耗很多资源？</div>2021-10-25</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/57/4f/6fb51ff1.jpg" width="30px"><span>奕</span> 👍（0） 💬（4）<div>现在有个问题，如果配置的 后台线程删除，在删除前后计算 内存使用量的时候 (long long)zmalloc_used_memory(); 是不是就不准了？这时候 key 和 value 的内存还没有得到释放的，只是把全局和失效 哈希表里面的删除了</div>2021-09-03</li><br/>
</ul>