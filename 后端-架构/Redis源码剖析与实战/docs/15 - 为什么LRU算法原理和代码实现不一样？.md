你好，我是蒋德钧。

从这节课开始，我们就进入了课程的第三个模块：缓存模块。在接下来的三节课当中，我会给你详细介绍LRU、LFU算法在Redis源码中的实现，以及Redis惰性删除对缓存的影响。

学习这部分内容，一方面可以让你掌握这些经典缓存算法在一个实际系统中该如何设计和实现；另一方面，你也可以学习到在计算机系统设计实现中的一个重要原则，也就是在进行系统设计开发的过程中，需要均衡算法复杂度和实现复杂度。另外，你还可以学习到缓存替换、惰性删除是如何释放Redis内存的。内存资源对Redis来说是非常宝贵的，所以掌握了这一点，你就可以有效减少Redis的内存使用问题了。

好，那么今天这节课呢，我们就先来学习下LRU算法在Redis中的实现。

## LRU算法的基本原理

首先，我们需要理解LRU算法的基本原理。LRU算法就是指**最近最少使用**（Least Recently Used，LRU）算法，这是一个经典的缓存算法。

从基本原理上来说，LRU算法会使用一个链表来维护缓存中每一个数据的访问情况，并根据数据的实时访问，调整数据在链表中的位置，然后通过数据在链表中的位置，来表示数据是最近刚访问的，还是已经有一段时间没有访问了。
<div><strong>精选留言（12）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/0f/90/8a/288f9f94.jpg" width="30px"><span>Kaito</span> 👍（35） 💬（6）<div>1、实现一个严格的 LRU 算法，需要额外的内存构建 LRU 链表，同时维护链表也存在性能开销，Redis 对于内存资源和性能要求极高，所以没有采用严格 LRU 算法，而是采用「近似」LRU 算法实现数据淘汰策略

2、触发数据淘汰的时机，是每次处理「请求」时判断的。也就是说，执行一个命令之前，首先要判断实例内存是否达到 maxmemory，是的话则先执行数据淘汰，再执行具体的命令

3、淘汰数据时，会「持续」判断 Redis 内存是否下降到了 maxmemory 以下，不满足的话会继续淘汰数据，直到内存下降到 maxmemory 之下才会停止

4、可见，如果发生大量淘汰的情况，那么处理客户端请求就会发生「延迟」，影响性能

5、Redis 计算实例内存时，不会把「主从复制」的缓冲区计算在内，也就是说不管一个实例后面挂了多少个从库，主库不会把主从复制所需的「缓冲区」内存，计算到实例内存中，即这部分内存增加，不会对数据淘汰产生影响

6、但如果 Redis 内存已达到 maxmemory，要谨慎执行 MONITOR 命令，因为 Redis Server 会向执行 MONITOR 的 client 缓冲区填充数据，这会导致缓冲区内存增长，进而引发数据淘汰

课后题：为什么键值对的 LRU 时钟值，不是直接通过调用 getLRUClock 函数来获取？

本质上是为了性能。

Redis 这种对性能要求极高的数据库，在系统调用上的优化也做到了极致。

获取机器时钟本质上也是一个「系统调用」，对于 Redis 这种动不动每秒上万的 QPS，如果每次都触发一次系统调用，这么频繁的操作也是一笔不小的开销。

所以，Redis 用一个定时任务（serverCron 函数），以固定频率触发系统调用获取机器时钟，然后把机器时钟挂到 server 的全局变量下，这相当于维护了一个「本地缓存」，当需要获取时钟时，直接从全局变量获取即可，节省了大量的系统调用开销。</div>2021-08-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/26/38/ef063dc2.jpg" width="30px"><span>Darren</span> 👍（9） 💬（0）<div>6.2的版本中，增加了maxmemory-eviction-tenacity配置，目的是控制大量淘汰内存空间阻塞客户端的时间。
6.2的版本中没有了freeMemoryIfNeeded 和 freeMemoryIfNeededAndSafe函数，而是被performEvictions替代
然后在执行内存释放期间，耗时统计，超过限制时间，新增时间事件，然后结束循环，流程继续往下执行。

&#47;&#47; 如果执行释放空间超过限制时间，则添加一个时间事件，时间事件中继续释放内存
if (elapsedUs(evictionTimer) &gt; eviction_time_limit_us) {
    &#47;&#47; We still need to free memory - start eviction timer proc
    if (!isEvictionProcRunning) {
        isEvictionProcRunning = 1;
        &#47;&#47; 新增时间时间
        aeCreateTimeEvent(server.el, 0,
                evictionTimeProc, NULL, NULL);
    }
    break;
}

如果一次时间事件没结束，则该时间事件不结束，等待一段时间，继续执行
&#47;&#47; 如果返回值不是AE_NOMORE，则继续把当前事件间隔retval毫秒后继续执行
if (retval != AE_NOMORE) {
    te-&gt;when = now + retval * 1000;
} else {
    te-&gt;id = AE_DELETED_EVENT_ID;
}</div>2021-09-06</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/25/7f/473d5a77.jpg" width="30px"><span>曾轼麟</span> 👍（4） 💬（0）<div>首先回答老师的问题：

是为了均衡性能和精度才这样设计的，如果server.hz设置的值小，精度要求小于LRU_CLOCK_RESOLUTION全局的频率精度，那么直接获预先计算的值对性能友好。如果server.hz设置的值较大，精度要求高于LRU_CLOCK_RESOLUTION的精度，那么就会在每次通过getLRUClock函数计算出结果。此外atomicGet的方法证明server.lruclock这个值是可能并发修改。此外在getLRUClock方法中，其本身是调用gettimeofday这个操作系统级别的API获取的。

本篇文章老师介绍了Redis-LRU的实现：
    1、为了妥协性能和资源，Redis使用的是，近似LRU算法，并且通过全局时钟去预计算LRU时钟的值。
    2、通过每次调用命令都访问freeMemoryIfNeeded函数，判断是否需要释放内存，从而保证Redis能及时通过淘汰算法进行数据驱逐，而保证服务正常运行。
    3、serverCron时间事件，会定期执行全局LRU时钟的更新，而在后续的运行中如果精度设置的要求不高基本上都会使用预先计算好的值。</div>2021-09-06</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1f/7e/5a/da39f489.jpg" width="30px"><span>Ethan New</span> 👍（4） 💬（0）<div>server.lruclock相当于是一个缓存值，serverCron每100ms更新一次server.lruclock，避免了频繁进行系统调用获取系统时钟</div>2021-08-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/17/8b/4b/15ab499a.jpg" width="30px"><span>风轻扬</span> 👍（1） 💬（0）<div>回答课后问题：
redis全局时钟，计算公式为：
unsigned int getLRUClock(void) {
     return (mstime()&#47;LRU_CLOCK_RESOLUTION) &amp; LRU_CLOCK_MAX;
}
就像老师文章中所说，redis的全局时钟，精度是1秒。
unsigned int LRU_CLOCK(void) {
    unsigned int lruclock;
    &#47;&#47;hz的值没有配置为1或者比1更大的值,此时说明redis服务端需要的全局时钟精度是秒,直接获取全局变量的时钟即可
    if (1000&#47;server.hz &lt;= LRU_CLOCK_RESOLUTION) {
        atomicGet(server.lruclock,lruclock);
    } else {
        &#47;&#47;如果hz的值配置为1或者比1更小的值,此时说明redis服务端需要的全局时钟精度是毫秒,需要实时计算全局时钟
        lruclock = getLRUClock();
    }
    return lruclock;
}</div>2023-11-13</li><br/><li><img src="" width="30px"><span>Geek_3b4ae8</span> 👍（1） 💬（1）<div>假设第一次执行lru。数组里面没有元素。随机采样5个，那此时这5个都能插入数组，也就都会被淘汰。但是这5个不一定是最近最少使用的啊，甚至可能是最近最常使用的啊。这里不太明白。感觉就是随机的，并不是lru</div>2022-04-22</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/VSylTssVXGVH10P32wfThTploZBuG9meyufz7wyVNUvmsFgMoEZlQl5lx7Ge5hhR5wSPloRy8GZAhEc4yD9fbA/132" width="30px"><span>JJPeng</span> 👍（1） 💬（1）<div>老师，您好。我认为您原文中”如果一个数据前后两次访问的时间间隔小于 1 秒，那么这两次访问的时间戳就是一样的。“这句话的描述是有误的。
因为一秒钟表示一个时间跨度，如果对一个数据的访问分别是在前一秒的结束和后一秒的开始，这样的话，虽然两次操作的时间间隔小于1秒，但LRU时间戳的值应该是不一样的。
反之，如果您的描述正确的话，那在每次时间间隔小于1秒的情况下连续对某个键进行访问，那该键的LRU时间戳就始终与第一次访问时的时间戳保持一致，这样应该是有问题的。</div>2022-04-03</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1d/6c/b5/32374f93.jpg" width="30px"><span>可怜大灰狼</span> 👍（1） 💬（0）<div>getLRUClock内部是通过gettimeofday系统调用来获取时间。redis的QPS每秒近10w，如果始终通过系统调用，会导致用户态和内核态来回切换，会造成很大的性能损失。</div>2021-08-31</li><br/><li><img src="https://wx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTLm8skz4F7FGGBTXWUMia6qVEc00BddeXapicv5FkAx62GmOnUNEcE4scSR60AmappQoNdIQhccKsBA/132" width="30px"><span>末日，成欢</span> 👍（0） 💬（1）<div>while (k &lt; EVPOOL_SIZE &amp;&amp;
	       pool[k].key &amp;&amp;
	       pool[k].idle &lt; idle) k++;
如果在当前集合中找到一个空闲时间小于采用数据的空闲时间，不应该k++,不是不会增加吗？ 应该是大于把？</div>2022-03-12</li><br/><li><img src="https://wx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTLm8skz4F7FGGBTXWUMia6qVEc00BddeXapicv5FkAx62GmOnUNEcE4scSR60AmappQoNdIQhccKsBA/132" width="30px"><span>末日，成欢</span> 👍（0） 💬（1）<div>如果配置的时候没有配置maxmemory会怎么样？是不是redis使用内存就无上限了吗？</div>2022-03-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/65/6a/be36c108.jpg" width="30px"><span>ikel</span> 👍（0） 💬（0）<div>这篇开始源码版本又回到5.xx了么</div>2021-11-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/57/4f/6fb51ff1.jpg" width="30px"><span>奕</span> 👍（0） 💬（4）<div>随机取  maxmemory_samples 配置的 5个 key 保存到待淘汰数组里面，然后淘汰最后一个时间空闲最长的 key，这样很大的可能淘汰不是最近最少使用的啊</div>2021-08-29</li><br/>
</ul>