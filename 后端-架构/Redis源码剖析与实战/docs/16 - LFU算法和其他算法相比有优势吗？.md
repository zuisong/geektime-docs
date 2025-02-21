你好，我是蒋德钧。

上节课我给你介绍了Redis对缓存淘汰策略LRU算法的近似实现。其实，Redis在4.0版本后，还引入了LFU算法，也就是**最不频繁使用**（Least Frequently Used，LFU）算法。LFU算法在进行数据淘汰时，会把最不频繁访问的数据淘汰掉。而LRU算法是把最近最少使用的数据淘汰掉，看起来也是淘汰不频繁访问的数据。那么，**LFU算法和LRU算法的区别到底有哪些呢？我们在实际场景中，需要使用LFU算法吗？**

其实，如果只是从基本定义来看的话，我们是不太容易区分出这两个算法的。所以，今天这节课，我就带你从源码层面来学习了解下LFU算法的设计与实现。这样，你就能更好地掌握LFU算法的优势和适用场景，当你要为Redis缓存设置淘汰策略时，就可以作出合适的选择了。

好，那么在开始学习LFU算法的实现代码之前，我们还是先来看下LFU算法的基本原理，以此更好地支撑我们掌握代码的执行逻辑。

## LFU算法的基本原理

因为LFU算法是根据**数据访问的频率**来选择被淘汰数据的，所以LFU算法会记录每个数据的访问次数。当一个数据被再次访问时，就会增加该数据的访问次数。

不过，访问次数和访问频率还不能完全等同。**访问频率是指在一定时间内的访问次数**，也就是说，在计算访问频率时，我们不仅需要记录访问次数，还要记录这些访问是在多长时间内执行的。否则，如果只记录访问次数的话，就缺少了时间维度的信息，进而就无法按照频率来淘汰数据了。
<div><strong>精选留言（8）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/0f/90/8a/288f9f94.jpg" width="30px"><span>Kaito</span> 👍（39） 💬（0）<div>1、LFU 是在 Redis 4.0 新增的淘汰策略，它涉及的巧妙之处在于，其复用了 redisObject 结构的 lru 字段，把这个字段「一分为二」，保存最后访问时间和访问次数

2、key 的访问次数不能只增不减，它需要根据时间间隔来做衰减，才能达到 LFU 的目的

3、每次在访问一个 key 时，会「懒惰」更新这个 key 的访问次数：先衰减访问次数，再更新访问次数

3、衰减访问次数，会根据时间间隔计算，间隔时间越久，衰减越厉害

4、因为 redisObject lru 字段宽度限制，这个访问次数是有上限的（8 bit 最大值 255），所以递增访问次数时，会根据「当前」访问次数和「概率」的方式做递增，访问次数越大，递增因子越大，递增概率越低

5、Redis 实现的 LFU 算法也是「近似」LFU，是在性能和内存方面平衡的结果

课后题：LFU 算法在初始化键值对的访问次数时，会将访问次数设置为 LFU_INIT_VAL，默认值是 5 次。如果 LFU_INIT_VAL 设置为 1，会发生什么情况？

如果开启了 LFU，那在写入一个新 key 时，需要初始化访问时间、访问次数（createObject 函数），如果访问次数初始值太小，那这些新 key 的访问次数，很有可能在短时间内就被「衰减」为 0，那就会面临马上被淘汰的风险。

新 key 初始访问次数 LFU_INIT_VAL = 5，就是为了避免一个 key 在创建后，不会面临被立即淘汰的情况发生。</div>2021-08-31</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/25/7f/473d5a77.jpg" width="30px"><span>曾轼麟</span> 👍（11） 💬（0）<div>回答老师的问题：
LFU_INIT_VAL的初始值为5主要是避免，刚刚创建的对象被立马淘汰，而需要经历一个衰减的过程后才会被淘汰。

LFU算法和LRU算法的不同就是，存粹的LFU算法会累计历史的访问次数，然而在高QPS的情况下可能会出现以下几个问题：
    1、运行横跨高峰期和低峰期，不同时期存储的数据不一致，可能会导致部分高峰期产生的数据不容易被淘汰，甚至可能永远淘汰不掉（因为在高峰获得一个较高的count值，在计算淘汰的时候仍然存在）
    2、需要long乃至更大的值去存储count。对于高频访问的数据如果需要统计每一次的调用，可能需要使用更大的空间去存储，还需要考虑溢出的问题。
    3、 可能存在，每次淘汰掉的几乎是刚刚创建的新数据。

为了解决这些问题，Redis实现了一个近似LFU算法，并做出了以下改进：
    1、count有上限值255。（避免高频数据获得一个较大的count值，还能节省空间）
    2、count值是会随着时间衰减。(不再访问的数据更加容易被淘汰，高16位记录上一次访问时间戳-分钟，低8位记录count)
    3、刚刚创建的数据count值不为0。（避免刚刚创建的数据被淘汰） 
    4、count值累加是概率随机的。（避免高峰期数据都能一下就能累加到255，其中概率能人为调整）</div>2021-09-07</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1d/6c/b5/32374f93.jpg" width="30px"><span>可怜大灰狼</span> 👍（7） 💬（0）<div>uint8_t LFULogIncr(uint8_t counter) {
    if (counter == 255) return 255;
    double r = (double)rand()&#47;RAND_MAX;
    double baseval = counter - LFU_INIT_VAL;
    if (baseval &lt; 0) baseval = 0;
    double p = 1.0&#47;(baseval*server.lfu_log_factor+1);
    if (r &lt; p) counter++;
    return counter;
}
通过源码可以发现：如果LFU_INIT_VAL太小，会导致baseval变大，从而导致p变小，导致counter加1比较困难。结果就是很容易导致刚set进去的数据，很快就会被淘汰。</div>2021-08-31</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/17/8b/4b/15ab499a.jpg" width="30px"><span>风轻扬</span> 👍（0） 💬（0）<div>回答一下课后问题。如果LFU_INIT_VAL设置为1。会有两方面影响
1、数据访问次数的增加概率会变大，导致很多数据都会达到255这个值，最终导致不容易淘汰数据
2、新创建出来的数据，访问频率过小。很容易刚刚创建就被淘汰</div>2023-11-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1a/8a/7e/bfe37c46.jpg" width="30px"><span>飞鱼</span> 👍（0） 💬（0）<div>提问：上一节中，哪里有说在实际淘汰数据的时候更新 redisObject对象中的 lru变量的值，只看到了 创建 和 访问更新 这2种情况会更新 lru变量值。</div>2022-09-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/20/df/ac/b1e58982.jpg" width="30px"><span>leetcode</span> 👍（0） 💬（1）<div>redis6.0以后server.c文件中都没有lookupKey函数了呀</div>2022-01-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/24/0b/8690964e.jpg" width="30px"><span>或许</span> 👍（0） 💬（0）<div>第一张图里面，lookupKey函数是在db.c里面，老师这里是不是有问题啊？</div>2021-11-30</li><br/><li><img src="" width="30px"><span>Geek_197c21</span> 👍（0） 💬（2）<div>如果 LFU_INIT_VAL 设置为 1，那么容易一个key刚刚被set进去就被删除。
麻烦问下老师，如果lfu算法要替换成lru算法的话，那么怎么处理呢？将key都对 255-次数呢？或者啥都不管，继续运行呢</div>2021-08-31</li><br/>
</ul>