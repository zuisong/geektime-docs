你好，我是蒋德钧。今天，我们来聊聊Redis中的Hash。

我们知道，Hash表是一种非常关键的数据结构，在计算机系统中发挥着重要作用。比如在Memcached中，Hash表被用来索引数据；在数据库系统中，Hash表被用来辅助SQL查询。而对于Redis键值数据库来说，Hash表既是键值对中的一种值类型，同时，Redis也使用一个全局Hash表来保存所有的键值对，从而既满足应用存取Hash结构数据需求，又能提供快速查询功能。

那么，Hash表应用如此广泛的一个重要原因，就是从理论上来说，它能以O(1)的复杂度快速查询数据。Hash表通过Hash函数的计算，就能定位数据在表中的位置，紧接着可以对数据进行操作，这就使得数据操作非常快速。

Hash表这个结构也并不难理解，但是在实际应用Hash表时，当数据量不断增加，它的性能就经常会受到**哈希冲突**和**rehash开销**的影响。而这两个问题的核心，其实都来自于Hash表要保存的数据量，超过了当前Hash表能容纳的数据量。

那么要如何应对这两个问题呢？事实上，这也是在大厂面试中，面试官经常会考核的问题。所以你现在可以先想想，如果你在面试中遇到了这两个问题，你会怎么回答呢？
<div><strong>精选留言（30）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/11/23/5b/983408b9.jpg" width="30px"><span>悟空聊架构</span> 👍（31） 💬（4）<div>说下我是怎么找到这个 Hash 函数的吧。有点艰辛...

（1）文中也提到了 rehash 的主要函数就是 dictRehash 函数，所以我们可以直接在这个函数里面找： 

h = dictHashKey(d, de-&gt;key) &amp; d-&gt;ht[1].sizemask;

代码含义：根据扩容后的哈希表ht[1]大小，计算当前哈希项在扩容后哈希表中的bucket位置。

（2）点进这个方法里面，发现如下：

\#define dictHashKey(d, key) (d)-&gt;type-&gt;hashFunction(key)

最后调用的是一个 hashFunction，但是你会发现，不能跳转到这个方法里面。这样来看似乎线索断了。

（3）我们可以 hashFunction 是被 type 调用的，那么这个 type 其实 dict 的一个属性。那我们就直接去看下 dict 结构体，再 dict.h 中定义了 struct dict。里面可以找到 type 属性：

  dictType *type;

那这个 dictType 又是什么呢？

（4）我们点进去看下，发现 dictType 也是一个结构体，定义了 hash 函数的指针：

uint64_t (*hashFunction)(const void *key);

但是这里还是没有看到指针指向哪个 hash 函数，线索似乎又断了。

（5）这个时候，只能到 dict.c 中看下有没有线索。发现有一个 dictCreate 函数，里面指定了 type：

dict *dictCreate(dictType *type, void *privDataPtr)

所以我们只要找到调用 dictCreate 的地方，看下传的什么 type 就知道调用的是哪个 hash 函数了。

（6）全局搜 dictCreate 函数。发现有 53 个地方调用了，第一个文件时 deps\hiredis\async.c，到这里，其实再点进去没有意义了，因为 deps 文件夹属于第三方依赖库，和 redis 的核心源码没有关系，那就继续找。

（7）把 deps 排除掉，剩余 49 个结果，第一个是 cluster.c 中调用的，cluster 是 Redis 集群初始化相关的

  server.cluster-&gt;nodes = dictCreate(&amp;clusterNodesDictType,NULL);

这里用到的 clusterNodesDictType 中指定了 Hash 函数：dictSdsHash

（8）dictSdsHash 点进去，发现还是回到了 dict.c 文件中，调用了 dictGenHashFunction 函数，如下所示：

uint64_t dictGenHashFunction(const void *key, int len) {

  return siphash(key,len,dict_hash_function_seed);

}

调用的就是 siphash 函数，这就是我们要找的 hash 函数。

（9）siphash 点进去，跳转到了 siphash.c 文件，定义了 siphash 函数。

（10）第 7 步中，搜索结果我是看的 cluster.c 文件，如果想看下 Redis 服务端初始化相关的代码，就在 server.c 中找。搜索结果中有一条相关的，初始化 Redis 数据库：

server.db[j].dict = dictCreate(&amp;dbDictType,NULL);

dbDictType 点进去，发现用到了 dictSdsHash 函数：

再从 dictSdsHash 函数点进去，发现还是用到了 dict.c 中的 dictGenHashFunction 函数，和第十步找到的一样，同一个 dictGenHashFunction 函数，顿时感觉神清气爽。

------

总结：

1. 其实可以直接从 server.c 中来找创建 dict 的地方，会省很多步，这是一个正向的思维，但往往排查问题时，我们用的是逆向思维，虽然逆向思维苦了点，但是会有一种柳暗花明又一村的感觉。

2. 寻找的过程比较艰辛，但是对源码理解更深了。

3. 可以看 Redis 5 设计与源码实现作为本专栏的补充。比如缩容时也会触发渐见式 hash。当使用量不到总空间 10% 时，则进行缩容。缩容时空间大小则为能恰好包含 d-&gt;ht[0].used 个节点的 2^N 次方幂整数，并把字典中字段 rehashidx 标识为 0。在 server.h 文件中有定义：#define HASHTABLE_MIN_FILL    10。</div>2021-08-01</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/25/8c/a7/3a696385.jpg" width="30px"><span>.</span> 👍（2） 💬（3）<div>老师，您好！我有个疑问，dictRehash 进行迁移n个桶 ，这个n是固定吗？如果不是固定怎么确定呢？</div>2021-08-01</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/b7/15/6a2b6b83.jpg" width="30px"><span>董宗磊</span> 👍（1） 💬（3）<div>老师，当负载因子 &gt; 5 的时候，是不是就不再考虑有没有 RDB 或者 AOF 进程在运行？？</div>2021-07-31</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/90/8a/288f9f94.jpg" width="30px"><span>Kaito</span> 👍（114） 💬（13）<div>1、Redis 中的 dict 数据结构，采用「链式哈希」的方式存储，当哈希冲突严重时，会开辟一个新的哈希表，翻倍扩容，并采用「渐进式 rehash」的方式迁移数据

2、所谓「渐进式 rehash」是指，把很大块迁移数据的开销，平摊到多次小的操作中，目的是降低主线程的性能影响

3、Redis 中凡是需要 O(1) 时间获取 k-v 数据的场景，都使用了 dict 这个数据结构，也就是说 dict 是 Redis 中重中之重的「底层数据结构」

4、dict 封装好了友好的「增删改查」API，并在适当时机「自动扩容、缩容」，这给上层数据类型（Hash&#47;Set&#47;Sorted Set）、全局哈希表的实现提供了非常大的便利

5、例如，Redis 中每个 DB 存放数据的「全局哈希表、过期key」都用到了 dict：

&#47;&#47; server.h
typedef struct redisDb {
    dict *dict;     &#47;&#47; 全局哈希表，数据键值对存在这
    dict *expires;  &#47;&#47; 过期 key + 过期时间 存在这
    ...
}

6、「全局哈希表」在触发渐进式 rehash 的情况有 2 个：

- 增删改查哈希表时：每次迁移 1 个哈希桶（文章提到的 dict.c 中的 _dictRehashStep 函数）
- 定时 rehash：如果 dict 一直没有操作，无法渐进式迁移数据，那主线程会默认每间隔 100ms 执行一次迁移操作。这里一次会以 100 个桶为基本单位迁移数据，并限制如果一次操作耗时超时 1ms 就结束本次任务，待下次再次触发迁移（文章没提到这个，详见 dict.c 的 dictRehashMilliseconds 函数）

（注意：定时 rehash 只会迁移全局哈希表中的数据，不会定时迁移 Hash&#47;Set&#47;Sorted Set 下的哈希表的数据，这些哈希表只会在操作数据时做实时的渐进式 rehash）

7、dict 在负载因子超过 1 时（used: bucket size &gt;= 1），会触发 rehash。但如果 Redis 正在 RDB 或 AOF rewrite，为避免父进程大量写时复制，会暂时关闭触发 rehash。但这里有个例外，如果负载因子超过了 5（哈希冲突已非常严重），依旧会强制做 rehash（重点）

8、dict 在 rehash 期间，查询旧哈希表找不到结果，还需要在新哈希表查询一次

课后题：Hash 函数会影响 Hash 表的查询效率及哈希冲突情况，那么，你能从 Redis 的源码中，找到 Hash 表使用的是哪一种 Hash 函数吗？

找到 dict.c 的 dictFind 函数，可以看到查询一个 key 在哈希表的位置时，调用了 dictHashKey 计算 key 的哈希值：

dictEntry *dictFind(dict *d, const void *key) {
    &#47;&#47; 计算 key 的哈希值
    h = dictHashKey(d, key);
    ...
}

继续跟代码可以看到 dictHashKey 调用了 struct dict 下 dictType 的 hashFunction 函数：

&#47;&#47; dict.h
dictHashKey(d, key) (d)-&gt;type-&gt;hashFunction(key)

而这个 hashFunction 是在初始化一个 dict 时，才会指定使用哪个哈希函数的。

当 Redis Server 在启动时会创建「全局哈希表」：

&#47;&#47; 初始化 db 下的全局哈希表
for (j = 0; j &lt; server.dbnum; j++) {
    &#47;&#47; dbDictType 中指定了哈希函数
    server.db[j].dict = dictCreate(&amp;dbDictType,NULL);
    ...
}

这个 dbDictType struct 指定了具体的哈希函数，跟代码进去能看到，使用了 SipHash 算法，具体实现逻辑在 siphash.c。

（SipHash 哈希算法是在 Redis 4.0 才开始使用的，3.0-4.0 使用的是 MurmurHash2 哈希算法，3.0 之前是 DJBX33A 哈希算法）</div>2021-07-31</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/25/7f/473d5a77.jpg" width="30px"><span>曾轼麟</span> 👍（21） 💬（3）<div>首先回答老师的提问：Redis使用的hash函数算法是siphash，其代码位于siphash.c的siphash函数中，上层函数是dictGenHashFunction 【注意】：在查找dictGenHashFunction的时候如果发现算法是time33，其实你找到的是C的redis客户端框架hiredis实现的hash函数，并不是redis本身的hash函数


此外阅读完文章我产生了三个问题并且自己给出自己的理解：

问题一：

    redis的dict结构核心就是链式hash，其原理其实和JDK的HashMap类似（JDK1.7之前的版本，1.8开始是红黑树或链表），这里就有一个问题为什么Redis要使用链式而不引入红黑树呢，或者直接使用红黑树？

答：
    1、hash冲突不使用红黑树：redis需要高性能，如果hash冲突使用红黑树，红黑树和链表的转换会引起不必要的开销（hash冲突不大的情况下红黑树其实比链表沉重，还会浪多余的空间）
    2、dict不采用红黑树：在负载因子较低，hash冲突较低的情况下，hash表的效率O(1)远远高于红黑树
    3、当采用渐进式rehash的时候，以上问题都可以解决


问题二：

    何为渐进式rehash？本质原理是什么？当内存使用变小会缩容吗？

答：
    1、渐进式rehash的本质是分治思想，通过把大任务划分成一个个小任务，每个小任务只执行一小部分数据，最终完成整个大任务的过程
    2、渐进式rehash可以在不影响运行中的redis使用来完成整改hash表的扩容（每次可以控制只执行1ms）
    3、初步判定会，因为dictResize中用于计算hash表大小的minimal就是来源于实际使用的大小，并且htNeedsResize方法中（used*100&#47;size &lt; HASHTABLE_MIN_FILL）来判断是否触发缩容来节约内存，而缩容也是渐进式rehash


问题三：

    渐进式rehash怎么去执行？

答：
    在了解渐进式rehash之前，我们需要了解一个事情，就是正在运行执行任务的redis，其实本身就是一个单线程的死循环（不考虑异步以及其他fork的场景），其循环的方法为aeMain(),位于ae.c文件中，在这个循环中每次执行都会去尝试执行已经触发的时间事件和文件事件，而渐进式rehash的每个小任务就是位于redis，serverCron时间事件中，redis每次循环的时候其实都会经过如下所示的调用流程：

    1、serverCron -&gt; updateDictResizePolicy (先判断是否能执行rehash，当AOF重写等高压力操作时候不执行)
    2、serverCron -&gt; databasesCron -&gt; incrementallyRehash -&gt; dictRehashMilliseconds -&gt; dictRehash (dictRehashMilliseconds默认要求每次rehash最多只能执行1ms)

    通过这种方式最终完成整改hash表的扩容</div>2021-07-31</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/fc/f7/457c14b2.jpg" width="30px"><span>叶坚</span> 👍（7） 💬（7）<div>咨询个问题，当部分bucket 执行 rehash，部分bucket还没有执行rehash，这时增删查请求操作是对ht[1]操作，还是ht[0]，谢谢
</div>2021-08-01</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/a2/d6/97370dfc.jpg" width="30px"><span>onno</span> 👍（5） 💬（6）<div>为啥说dictht里的**table是一个二维数组啊，不是一个二级指针的一位数组吗？</div>2021-12-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1f/d6/b2/449b4ae3.jpg" width="30px"><span>shp</span> 👍（4） 💬（0）<div>需要注意的是在渐进式rehash的过程，如果有增删改查操作时，如果index大于rehashindex，访问ht[0]，否则访问ht[1]</div>2022-01-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/96/a6/aac2a550.jpg" width="30px"><span>陌</span> 👍（3） 💬（0）<div>Hash 表使用的是哪一种 Hash 函数?

各个类型的 dictType 在 server.c 中被初始化，常用的包括 setDictType、zsetDictType 以及 16 个 database 所使用的 dbDictType。
此时就可以找到 hashFunction 的实现为 dictSdsHash()，最终的底层实现为 siphash()。

dict 对象的使用除了理解最基本的拉链法处理哈希冲突、使用渐进式 rehash 的方式进行扩容以外，我认为还需要从全局的角度来考虑。也就是 Redis Server 在运行时
使用了哪些功能的 dict。这部分内容可以在 server.c&#47;initServer() 方法中找到答案:

```
for (j = 0; j &lt; server.dbnum; j++) {
    &#47;&#47; 创建基础 hashmap，也就是 set key value 所使用的 hashmap
    server.db[j].dict = dictCreate(&amp;dbDictType,NULL);

    &#47;&#47; 创建 expires hashmap，用于实现 TTL，调用可见 dbAsyncDelete()
    server.db[j].expires = dictCreate(&amp;dbExpiresDictType,NULL);

    &#47;&#47; 创建 blocking_keys hashmap，用于记录阻塞信息，调用可见 serveClientsBlockedOnListKey()
    server.db[j].blocking_keys = dictCreate(&amp;keylistDictType,NULL);

    &#47;&#47; 创建 ready_keys hashmap，调用可见 handleClientsBlockedOnKeys()
    server.db[j].ready_keys = dictCreate(&amp;objectKeyPointerValueDictType,NULL);

    &#47;&#47; 创建 watched_keys hashmap，调用可见 watchForKey()
    server.db[j].watched_keys = dictCreate(&amp;keylistDictType,NULL);

    ......
}
```

也就是说，Redis 在启动时将会创建 16 * 5 个功能性的 dict，这些 dcit 是实现 TTL、BLPOP&#47;BRPOP 等功能的关键组件。</div>2021-08-01</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/56/e0/d34f57b3.jpg" width="30px"><span>日落黄昏下</span> 👍（2） 💬（1）<div>我看源码好像扩容并不是双倍的used大小，在_dictNextPower中要计算出来的新容量是2的n次幂。</div>2021-08-25</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/24/ee/46/7d65ae37.jpg" width="30px"><span>木几丶</span> 👍（2） 💬（8）<div>老师你好，有几个问题想请教下：
1、判断是否扩容并rehash的条件是d-&gt;ht[0].used &gt;= d-&gt;ht[0].size &amp;&amp;(dict_can_resize || d-&gt;ht[0].used&#47;d-&gt;ht[0].size &gt; dict_force_resize_ratio)，这句逻辑好像不对？应该写成d-&gt;ht[0].used &gt;= d-&gt;ht[0].size &amp;&amp; dict_can_resize || d-&gt;ht[0].used&#47;d-&gt;ht[0].size &gt; dict_force_resize_ratio？
2、在函数dictRehash中有一段代码是  assert(d-&gt;ht[0].size &gt; (unsigned long)d-&gt;rehashidx)，这是断言rehashidx是否越界，rehashidx为什么会有越界的情况？
3、另外问个代码上的问题（有可能钻牛角尖了），作为性能抠的很细的redis来说，在计算新哈希表大小的时候需要从初始大小4频繁*2得到最终size，这里为什么不直接用移位操作提升效率？</div>2021-07-31</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1d/6c/b5/32374f93.jpg" width="30px"><span>可怜大灰狼</span> 👍（2） 💬（0）<div>dict.c中dictGenHashFunction调用的是siphash.c中siphash方法。我想从MurmurHash2到siphash，也是看重哈希洪水攻击。不过java的HashMap还是通过平衡树来处理同一位置超过8个元素的哈希碰撞。</div>2021-07-31</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/83/c9/5d03981a.jpg" width="30px"><span>thomas</span> 👍（1） 💬（2）<div>&#47;&#47;将当前哈希项添加到扩容后的哈希表ht[1]中        
de-&gt;next = d-&gt;ht[1].table[h];       第一步
d-&gt;ht[1].table[h] = de;
---------------------------------------&gt;
没想明白，为什么需要第一步的操作？</div>2021-09-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/d4/d6/1d4543ac.jpg" width="30px"><span>云海</span> 👍（1） 💬（1）<div>如果当前表的已用空间大小为 size，那么就将表扩容到 size*2 的大小。
这里应该笔误了。
从_dictNextPower 可以看出，这里的描述有点歧义，size 应该是 hash 表的容量，而不是 hash 表已使用的空间。 
扩容是从 4开始一直乘以2，直到大于 当前已使用空间+1（下面代码里的size 实际是 used+1）
static unsigned long _dictNextPower(unsigned long size)
{
    unsigned long i = DICT_HT_INITIAL_SIZE;

    if (size &gt;= LONG_MAX) return LONG_MAX + 1LU;
    while(1) {
        if (i &gt;= size)
            return i;
        i *= 2;
    }
}</div>2021-08-15</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/f3/cf/851dab01.jpg" width="30px"><span>Milittle</span> 👍（1） 💬（0）<div>使用的hash函数是siphash</div>2021-07-31</li><br/><li><img src="" width="30px"><span>Geek1278</span> 👍（0） 💬（1）<div>老师，我有个疑问，为什么 redis 的哈希表用的是数组+链表形式，而 java  1.8里的 hashmap 用的是 数组+链表+红黑树。redis 后面是不是也会朝红黑树演进？</div>2024-02-16</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1a/8a/7e/bfe37c46.jpg" width="30px"><span>飞鱼</span> 👍（0） 💬（0）<div>终于理解为什么是二维数组了，dictEntry **table 写法是个二维数组

在C语言中，一维数组是一个线性数据结构，它由一组连续的内存单元组成，每个内存单元都有一个地址，并且可以按照数组索引进行访问。

而二维数组是由多个一维数组组成的，它可以看作是一个表格，其中的每个元素都有两个索引来确定其位置。二维数组在内存中也是连续存储的，但是在访问元素时需要使用两个索引来确定具体的位置。

所以，dictEntry **table 是一个二维数组，其中每个元素是一个指向 dictEntry 结构体指针的指针。

在 Redis 中，决定键值对应该落在二维数组的哪个行和列，涉及两个步骤：计算哈希值和确定数组索引。

计算哈希值：首先，根据键的内容计算出一个哈希值。在 Redis 中，通常使用 MurmurHash 算法或者其他哈希算法来生成哈希值。哈希值的生成是根据键的内容来计算的，因此相同的键生成的哈希值是固定的。

确定数组索引：根据哈希值，通过取模运算将其映射到二维数组的行和列。具体的取模运算可以根据数组的大小进行计算。例如，如果二维数组的大小是4x4，可以使用哈希值对4取模来得到行索引，再使用哈希值对4进行取模来得到列索引。

行索引 = 哈希值 % 数组行数
列索引 = 哈希值 % 数组列数

例如，如果哈希值是9，且数组大小为4x4，则行索引为9 % 4 = 1，列索引为9 % 4 = 1。这意味着该键值对将被存储在 table[1][1] 的位置。

通过计算哈希值和确定数组索引，可以将键值对均匀地分布到二维数组中的不同位置，实现了键值对的快速访问和高效存储。同时，数组的大小和结构可以根据实际需求进行调整，以适应不同的数据量和性能要求。</div>2023-11-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1a/8a/7e/bfe37c46.jpg" width="30px"><span>飞鱼</span> 👍（0） 💬（0）<div>redis 渐进式哈希扩容，如果 h[0] 的 第1桶迁移完毕，后续写操作又往h[0]  的第1个桶写数据，怎么处理？

ChatGPT3.5：当使用渐进式哈希扩容时，如果已经完成了哈希槽的迁移，但之后再往被迁移的哈希槽中写入数据时，Redis会根据当前的情况来处理。

在这种情况下，如果写操作仍然指向哈希扩容前的哈希槽（例如h[0]的第1个桶），Redis会按照以下方式处理：

1. 如果哈希槽已被迁移完毕，但新的写操作仍旧指向旧的哈希槽，Redis会将数据写入旧的哈希槽中，即h[0]的第1个桶。这是因为迁移过程中，Redis为了保证数据的一致性，会在新的哈希槽和旧的哈希槽之间进行同步复制，直到迁移完成。

2. 如果哈希槽尚未迁移完毕，写操作指向的是即将被迁移的旧的哈希槽，Redis会将数据写入旧的哈希槽中，也就是h[0]的第1个桶。

无论是哪种情况，写操作都会被成功处理，并将数据写入适当的位置。然而，建议在进行哈希扩容时，尽量避免在迁移过程中对旧的哈希槽进行写操作，以避免可能的数据不一致或性能问题。一旦哈希扩容完成，所有的写操作都应该指向新的哈希槽，以确保数据的一致性和性能的最大化。
</div>2023-11-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/ef/64/5b71bb14.jpg" width="30px"><span>David</span> 👍（0） 💬（0）<div>dictGetSomeKeys，该函数返回一定数量的随机键，如果当前在rehash，函数内部似乎会尝试执行与 count 成正比的 rehashing 步骤</div>2023-09-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1a/36/fb/b480f2ac.jpg" width="30px"><span>人间理想</span> 👍（0） 💬（0）<div>老师写的很好，给老师点赞！</div>2023-05-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/2d/f1/1b/0957d4c5.jpg" width="30px"><span>王飞</span> 👍（0） 💬（0）<div>触发refresh条件：
	① 负载因子(load factor)大于5
	② 负载因子(load factor)大于等于1，且当前没有RDB子进程、也没有AOF子进程 (dict_can_resize = 1)</div>2022-08-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/23/4a/8f/ca11d7ad.jpg" width="30px"><span>问月</span> 👍（0） 💬（0）<div>dictGetIterator dictGetSafeIterator 这两个有课代表总结么？ 看代码感觉safeIterator也不会safe， 
1、定时任务会更新全局的dict
2、什么时候决定该用哪个，如果对于单线程来说，不是一般都是执行完这个线程就释放了么</div>2022-07-26</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTL3xax4aG4h59x50C7LQ5K7BicvIEicakyfE0lV4Pyib6OsYc1jC7Qa37g2v8qhib5BQiaB2DfB4DMG5Cw/132" width="30px"><span>花花世界小人物</span> 👍（0） 💬（0）<div>老师有一点不明白
rehash 是两个数组之前的数据拷贝。在执行rehash但是未执行完成,有新增或者删除操作相当于更新了原本的h[0]数组，rehashidx是递增的，redis是怎么保证这个新增和删除的数据同步到h[1]的
我是做java,也试着去代码中找了，找的迷迷糊糊的也没搞清楚，老师见笑了</div>2022-07-04</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/74/3d/54bbc1df.jpg" width="30px"><span>Jaime</span> 👍（0） 💬（0）<div>使用了siphash算法，
uint64_t siphash(const uint8_t *in, const size_t inlen, const uint8_t *k) {
.....
}
</div>2022-05-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/03/2f/0a5e0751.jpg" width="30px"><span>再见理想</span> 👍（0） 💬（0）<div>Redis主要的一种数据类型 和数据结构hash.
Hash表在使用中会面对两个问题 hash冲突和rehash
Redis使用hash链表的方式存储hash冲突的键值。
当hash的负载因子越来越大时，冲突会越来越多，导致hash的查询性能降低，这个时候就需要扩大hash的桶数量，redis使用渐进式rehash的方式，创建一个新的size*2的hash表，将现有hash表的数据迁移到新的表中，再将hash的指针引用到新的hash表，清空旧表，完成rehash操作。
Rehash的时机
负载因子大于1并且(可以扩容或者负载因子大于5)</div>2022-04-16</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/23/c0/ae/e5e62510.jpg" width="30px"><span>徐志超-Klaus</span> 👍（0） 💬（0）<div>Redis 的 Hashes是有存储顺序的吗？就像java的LinkedHashMap那样？hkeys 是按存储顺序返回的？</div>2022-02-24</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/dr34H3hOMVsibL0XV1iaBWFiaTnYssX8sNjmJDpiaBUVv2X39nFzDjNpe288cKkZfH3P9sVRxZ1lzYZEcRR3vJNYtA/132" width="30px"><span>Benson_Geek</span> 👍（0） 💬（2）<div>有个点始终想不明白。
看到源码dictFind函数，
dictEntry *dictFind(dict *d, const void *key)
{
    dictEntry *he;
    uint64_t h, idx, table;

    if (d-&gt;ht[0].used + d-&gt;ht[1].used == 0) return NULL; &#47;* dict is empty *&#47;
    if (dictIsRehashing(d)) _dictRehashStep(d);
    h = dictHashKey(d, key);
    for (table = 0; table &lt;= 1; table++) {
        idx = h &amp; d-&gt;ht[table].sizemask;
        he = d-&gt;ht[table].table[idx];
        while(he) {
            if (key==he-&gt;key || dictCompareKeys(d, key, he-&gt;key))
                return he;
            he = he-&gt;next;
        }
        if (!dictIsRehashing(d)) return NULL;
    }
    return NULL;
}
----

确实在查找的时候，rehash期间需要查找两个表，
我问题是，不是可以计算出当前要查询的key的index，然后跟ht[0]中的rehashidx对比一下，
要是index &lt; rehashidx，不就说明了这个key所在的bucket已经是搬迁完毕到ht[1]中了？
那么这时候就直接去读ht[1]，而不用读一遍ht[0]，再读一遍ht[1]这样两次读操作。
求大佬们谁能解答一下我这个疑问，是否有啥原因而不能这么做？？？
我都能想到这种方式减少一次读没理由官方想不到？跪求解！！！</div>2021-11-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/29/2e/49/a04480a9.jpg" width="30px"><span>路遥知码力</span> 👍（0） 💬（1）<div>有一个疑问，如果rehash的过程中，因为数据量的暴增（默认扩容是size*2n次方），新设置的rehashht[1]在可以预见完全迁移数据的未来，也不够了（预见性发生hash冲突），甚至超过了强制rehash值dict_force_resize_ratio，咋办？</div>2021-09-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/db/fe/90446b61.jpg" width="30px"><span>lhgdy</span> 👍（0） 💬（0）<div>int dictExpand(dict *d, unsigned long size)
{
    &#47;* the size is invalid if it is smaller than the number of
     * elements already inside the hash table *&#47;
    if (dictIsRehashing(d) || d-&gt;ht[0].used &gt; size)
        return DICT_ERR;

    dictht n; &#47;* the new hash table *&#47;                                      这个地方是局部变量吧？ 局部变量被赋值给别的变量后还是会产生内存问题的吧？  请大佬解读下
    unsigned long realsize = _dictNextPower(size);

    &#47;* Rehashing to the same table size is not useful. *&#47;
    if (realsize == d-&gt;ht[0].size) return DICT_ERR;

    &#47;* Allocate the new hash table and initialize all pointers to NULL *&#47;
    n.size = realsize;
    n.sizemask = realsize-1;
    n.table = zcalloc(realsize*sizeof(dictEntry*));
    n.used = 0;

    &#47;* Is this the first initialization? If so it&#39;s not really a rehashing
     * we just set the first hash table so that it can accept keys. *&#47;
    if (d-&gt;ht[0].table == NULL) {
        d-&gt;ht[0] = n;
        return DICT_OK;
    }

    &#47;* Prepare a second hash table for incremental rehashing *&#47;
    d-&gt;ht[1] = n;
    d-&gt;rehashidx = 0;
    return DICT_OK;
}
</div>2021-09-04</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/47/65/5534850b.jpg" width="30px"><span>请叫我猿叔叔</span> 👍（0） 💬（1）<div>想问一下渐进式是根据bucket来操作的，  一个hash里面bucket的数量是怎么决定的</div>2021-09-02</li><br/>
</ul>