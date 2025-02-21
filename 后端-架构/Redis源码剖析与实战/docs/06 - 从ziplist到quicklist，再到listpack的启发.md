你好，我是蒋德钧。

在前面的[第4讲](https://time.geekbang.org/column/article/402223)，我介绍Redis优化设计数据结构来提升内存利用率的时候，提到可以使用压缩列表（ziplist）来保存数据。所以现在你应该也知道，ziplist的最大特点，就是它被设计成一种内存紧凑型的数据结构，占用一块连续的内存空间，以达到节省内存的目的。

但是，**在计算机系统中，任何一个设计都是有利有弊的**。对于ziplist来说，这个道理同样成立。

虽然ziplist节省了内存开销，可它也存在两个设计代价：一是不能保存过多的元素，否则访问性能会降低；二是不能保存过大的元素，否则容易导致内存重新分配，甚至可能引发连锁更新的问题。所谓的连锁更新，简单来说，就是ziplist中的每一项都要被重新分配内存空间，造成ziplist的性能降低。

因此，针对ziplist在设计上的不足，Redis代码在开发演进的过程中，新增设计了两种数据结构：**quicklist和listpack**。这两种数据结构的设计目标，就是尽可能地保持ziplist节省内存的优势，同时避免ziplist潜在的性能下降问题。

今天这节课，我就来给你详细介绍下quicklist和listpack的设计思想和实现思路，不过在具体讲解这两种数据结构之前，我想先带你来了解下为什么ziplist的设计会存在缺陷。这样一来，你在学习quicklist和listpack时，可以和ziplist的设计进行对比，进一步就能更加容易地掌握quicklist和listpack的设计考虑了。
<div><strong>精选留言（22）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/0f/90/8a/288f9f94.jpg" width="30px"><span>Kaito</span> 👍（49） 💬（6）<div>1、ziplist 设计的初衷就是「节省内存」，在存储数据时，把内存利用率发挥到了极致：

- 数字按「整型」编码存储，比直接当字符串存内存占用少
- 数据「长度」字段，会根据内容的大小选择最小的长度编码
- 甚至对于极小的数据，干脆把内容直接放到了「长度」字段中（前几个位表示长度，后几个位存数据）

2、但 ziplist 的劣势也很明显：

- 寻找元素只能挨个遍历，存储过长数据，查询性能很低
- 每个元素中保存了「上一个」元素的长度（为了方便反向遍历），这会导致上一个元素内容发生修改，长度超过了原来的编码长度，下一个元素的内容也要跟着变，重新分配内存，进而就有可能再次引起下一级的变化，一级级更新下去，频繁申请内存

3、想要缓解 ziplist 的问题，比较简单直接的方案就是，多个数据项，不再用一个 ziplist 来存，而是分拆到多个 ziplist 中，每个 ziplist 用指针串起来，这样修改其中一个数据项，即便发生级联更新，也只会影响这一个 ziplist，其它 ziplist 不受影响，这种方案就是 quicklist：

qucklist: ziplist1(也叫quicklistNode) &lt;-&gt; ziplist2 &lt;-&gt; ziplist3 &lt;-&gt; ...

4、List 数据类型底层实现，就是用的 quicklist，因为它是一个链表，所以 LPUSH&#47;LPOP&#47;RPUSH&#47;RPOP 的复杂度是 O(1)

5、List 中每个 ziplist 节点可以存的元素个数&#47;总大小，可以通过 list-max-ziplist-size 配置：

- 正数：ziplist 最多包含几个数据项
- 负数：取值 -1 ~ -5，表示每个 ziplist 存储最大的字节数，默认 -2，每个ziplist 8KB

ziplist 超过上述任一配置，添加新元素就会新建 ziplist 插入到链表中。

6、List 因为更多是两头操作，为了节省内存，还可以把中间的 ziplist「压缩」，具体可看 list-compress-depth 配置项，默认配置不压缩

7、要想彻底解决 ziplist 级联更新问题，本质上要修改 ziplist 的存储结构，也就是不要让每个元素保存「上一个」元素的长度即可，所以才有了 listpack

8、listpack 每个元素项不再保存上一个元素的长度，而是优化元素内字段的顺序，来保证既可以从前也可以向后遍历

9、listpack 是为了替代 ziplist 为设计的，但因为 List&#47;Hash&#47;Set&#47;ZSet 都严重依赖 ziplist，所以这个替换之路很漫长，目前只有 Stream 数据类型用到了 listpack</div>2021-08-07</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/44/cf/a0315a85.jpg" width="30px"><span>lzh2nix</span> 👍（15） 💬（0）<div>从ziplist---&gt;quickList这在计算机里也是一个常见的设计模式。

为了防止单个数据表太大，我们将其拆分成多个数据表，也叫 [分桶设计]，数据库中的sharding，以及将一个大粒度的锁拆分成多个小粒度的锁都是类似的思想。</div>2021-08-15</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/57/4f/6fb51ff1.jpg" width="30px"><span>奕</span> 👍（6） 💬（0）<div>listpack 解决了 ziplist 连锁更新的问题，但是还是没有解决元素多的时候，查询复杂度高的问题</div>2021-08-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/25/7f/473d5a77.jpg" width="30px"><span>曾轼麟</span> 👍（3） 💬（2）<div>回答老师的提问，ziplist 能支持的最大整数是多大？

分析步骤：
1、按照问题范围，首先我去查看了zipTryEncoding的实现（ziplist.c），其中在给encoding赋值的时候划分了：极小值，int8，int16，int24，int32和int64
2、此外发现当value大于int32最大值的时候，会统一使用ZIP_INT_64B去编码
3、但是在zipTryEncoding开头处发现了一个判断，entrylen &gt;= 32的时候是不允许编码，意思就是传入的数据如果entrylen大于32直接跳过不编码为int
4、最后调用string2ll尝试将string value编码为long long(转换成功为1失败为0)
5、若转换成功，编码类型放到encoding中，值放到v中


根据第三步个人判断，传入的int值大小不会超过32位，那么最大值应该就是int32的最大值
</div>2021-08-08</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTLR2YXdT0AticVATPbtpd1LLOAA0FE1uRJstglZeBs1bAiaPB2PkEnlibIFtUPg1gsseribTib5Oiaw0BBA/132" width="30px"><span>Geek_0cfc2d</span> 👍（1） 💬（1）<div>老师，有个问题想请教一下：
listpack 中如果不考虑逆序查询，entry 其实使用 encoding+data 就可以，那 entry 中最后一个 len 其实是为了逆序遍历而加入的，这样理解对吗？ </div>2022-02-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/18/ae/cf/6186d936.jpg" width="30px"><span>辉度</span> 👍（1） 💬（0）<div>课后题：
1. 函数中先判断entrylen，达到32编码则返回0,编码失败。if (entrylen &gt;= 32 || entrylen == 0) return 0;
2. 其次*encoding 最大为 #define ZIP_INT_64B (0xc0 | 2&lt;&lt;4)，即11000000 | 00100000 == 11100000 == 224
3. value 类型为 long long，8个字节数，一共64位。

第2个式子我还不是很明白，没有搞懂编码encoding的单位，是位还是什么？

三者取最小，应该就是最多只能保存31位，则整数最大值2*31 - 1
</div>2021-08-07</li><br/><li><img src="https://wx.qlogo.cn/mmopen/vi_32/PiajxSqBRaEI9Fb9tYoBrjUa8zpvOTGibnKYI9fz1QnfXO1Dy5rp5DPJ7nQOHIIXzKOXet3DMqHNYIHJHyz6bm3g/132" width="30px"><span>胡玲玲</span> 👍（1） 💬（0）<div>请问ziplist、quicklist、listpack 这三者是如何协助redis的数据类型的呢</div>2021-08-07</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/c6/bf/52b3f71d.jpg" width="30px"><span>dawn</span> 👍（0） 💬（0）<div>如果数据存在连续内存里，针对插入和删除操作，只要不是最后一个节点，不都需要给后续的节点重新分配内存地址嘛，listpack并没有解决这个问题啊？而quicklist解决这个问题是方式，实际上是用了链表而非连续空间，牺牲了空间来解决这个事的，那还不如直接全上链表，根据类型归类也挺麻烦的</div>2022-08-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1b/89/52/b96c272d.jpg" width="30px"><span>🤐</span> 👍（0） 💬（0）<div>作为一个写JAVA的，有点理解不了这里</div>2022-07-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/5c/f6/443808f8.jpg" width="30px"><span>孤独患者</span> 👍（0） 💬（2）<div>quicklist，如果更新某个节点数据，导致节点内存变大了，那是不是当前节点的后续节点都要往后移动呢？因为内存是连续的</div>2022-06-15</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/18/7b/74/9b88e040.jpg" width="30px"><span>柏油</span> 👍（0） 💬（1）<div>在连锁更新代码块中，只看到调用了一次ziplistResize进行内存重分配；在这之前会将所有连锁更新影响的entry找出来，并重新计算len，这样就可以一次性计算得到所有需要的内存大小，也就是只有一次ziplistResize内存重新分配。不过，可能会调用多次memmove来调整元素的位置。

文章中：
“ziplist 新增某个元素或修改某个元素时，可能会导致后续元素的 prevlen 占用空间都发生变化，从而引起连锁更新问题，导致每个元素的空间都要重新分配”

每个元素都会进行内存重分配是不是有问题？还望解答</div>2022-01-05</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/29/2e/49/a04480a9.jpg" width="30px"><span>路遥知码力</span> 👍（0） 💬（1）<div>quicklist里的quicklistnode存储ziplist，每个quicklistnode里的ziplist是怎么拆分进入不同的node里的？</div>2021-09-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/43/79/18073134.jpg" width="30px"><span>test</span> 👍（0） 💬（0）<div>entey-encoding算是哈夫曼编码？</div>2021-09-04</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/1c/6f/3ea2a599.jpg" width="30px"><span>嘉木</span> 👍（0） 💬（1）<div>unsigned long lpEncodeBacklen(unsigned char *buf, uint64_t l) { 
	&#47;&#47;编码类型和实际数据的总长度小于等于127，entry-len长度为1字节 
	if (l &lt;= 127) { ... return 1; } 
	else if (l &lt; 16383) { &#47;&#47;编码类型和实际数据的总长度大于127但小于16383，entry-len长度为2字节 ... return 2; } 
	else if (l &lt; 2097151) {&#47;&#47;编码类型和实际数据的总长度大于16383但小于2097151，entry-len长度为3字节 ... return 3; } 
	else if (l &lt; 268435455) { &#47;&#47;编码类型和实际数据的总长度大于2097151但小于268435455，entry-len长度为4字节 ... return 4; } 
	else { &#47;&#47;否则，entry-len长度为5字节 ... return 5; }
}

老师您好，
对于backlen的编码计算这段代码有点疑惑：
除了第一个if判断是&lt;=之外，后面的if判断为什么是&lt;，而不是&lt;=了呢？ 
比如16383，按照&lt;=判断，编码为7f ff，最高位为0，表示下个字节不属于backlen，这样backlen只使用2个字节；
但是按照源码逻辑的话，16383编码为00 ff ff了，backlen使用了3个字节，这样的话不是浪费了一个字节吗？
</div>2021-09-04</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/4d/79/803537db.jpg" width="30px"><span>慢动作</span> 👍（0） 💬（1）<div>listpack有对应的quicklist吗？数组类型存储有最优大小吧，过大以后中间插入代价会很大？</div>2021-08-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/25/fa/51/5da91010.jpg" width="30px"><span>Miroticwillbeforever</span> 👍（0） 💬（0）<div>在有关 listpack 的正向查询图中，第二步 2.lpFirst 调用 lpSkip 是否是错误呢？第一步调用 lpNext,此时已经进入 lpNext 函数了，而 lpFirst 是将指针指到第一个列表项就返回。所以我觉得这里可以做个修正。。。</div>2021-08-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/18/4b/a8/14b8a860.jpg" width="30px"><span>赵小洛</span> 👍（0） 💬（0）<div>老师还是有点听不太懂，有没有辅助的书</div>2021-08-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1f/f7/4d/09554c96.jpg" width="30px"><span>iron bo</span> 👍（0） 💬（0）<div>在zipTryEncoding中，第一个判断是：
 if (entrylen &gt;= 32 || entrylen == 0) return 0;
这个判断中entrylen 是指的整数的长度，不是二进制的长度，所以这里判断的是这个整数的长度是否超过32位，如果超过了就用str的形式编码
第二个判断是：
if (string2ll((char*)entry,entrylen,&amp;value))
查询string2ll函数所能表示的最大值是ULLONG_MAX，如果超过了就用str的形式编码
此时*encoding = ZIP_INT_64B 也就是8个字节，和long long类型的字节数一致
两个判断取较小值，即ULLONG_MAX，但是由于value是有符号的，即为LLONG_MAX 0x7fffffffffffffffLL

我有一个疑问，当value的值在LLONG_MAX和ULLONG_MAX之间，string2ll函数会返回true，如果用ZIP_INT_64B表示，那符号位就没有了，这会不会有问题？
</div>2021-08-10</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTIiatbibYU9p7aVpq1o47X83VbJtsnP9Dkribian9bArLleibUVMDfD9S0JF9uZzfjo6AX5eR6asTiaYkvA/132" width="30px"><span>倪大人</span> 👍（0） 💬（0）<div>看了下zipTryEncoding的实现
 if (entrylen &gt;= 32 || entrylen == 0) return 0;
这行代码的意思应该是传入的字符串长度≥32或为0，就不认为是数字，直接按字符串处理
又看了一下__ziplistInsert，调用zipTryEncoding之后会调用zipIntSize算需要多少字节存数字，最大8个字节，所以课后题能支持的最大整数应该是2^64</div>2021-08-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/d4/d6/1d4543ac.jpg" width="30px"><span>云海</span> 👍（0） 💬（0）<div>ziplist
优点：
1. 【节省内存】内存紧凑型的数据结构，不存储前后节点的指针，占用一块连续的内存空间；
缺点：
1. 【查找复杂度高】ziplist 元素过多时，访问性能会降低；
2. 【潜在的连锁更新风险】不能保存过大的元素，否则新增或修改数据时，容易导致内存重新分配，甚至可能引发连锁更新的问题。

quicklist
优点：
1. 结合了链表和 ziplist 各自的优势；
2. 一个 quicklist 就是一个链表，而链表中的每个元素又是一个 ziplist；
3. quicklist 通过控制每个 quicklistNode 中 ziplist 的大小或是元素个数，就有效减少了在 ziplist 中新增或修改元素后，发生连锁更新的情况，从而提供了更好的访问性能。
缺点：
1. 【潜在的连锁更新风险】有效减少但未完全避免；
2. 【内存开销大】quicklist 使用 quicklistNode 结构指向每个 ziplist；

listpack
优点：
1. 【节省内存】用一块连续的内存空间来紧凑地保存数据；
2. 为了【进一步节省内存空间】，listpack 元素会对不同长度的整数和字符串进行不同的编码；
3. 【避免连锁更新】；</div>2021-08-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/18/ae/cf/6186d936.jpg" width="30px"><span>辉度</span> 👍（0） 💬（0）<div>- ziplist 连续、紧凑，选用最小的长度编码保存上一个元素的长度，这是节约内存的重点，同样也是因为这个“保存上一个元素长度”的prevlen，在更新时需要做到更新，导致的级联更新。
- quicklist 为了解决zipilist级联更新的影响，相当于多一点内存开销，分割多段ziplist，用quicklistNode来记录节点，使得一个节点内的ziplist即使发生级联更新，影响范围也会有限。
- listpack 的数据结构发生的变化就相对更大了，其不记录上一个节点的长度，从根本上解决了级联更新的问题。同时，其遍历的方法也发生了变化。</div>2021-08-07</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1f/7e/5a/da39f489.jpg" width="30px"><span>Ethan New</span> 👍（0） 💬（0）<div>这个专栏太值了，干货满满</div>2021-08-07</li><br/>
</ul>