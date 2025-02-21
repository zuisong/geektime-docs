你好，我是陶辉。

这是课程的第一讲，我们先从主机最重要的部件CPU开始，聊聊如何通过提升CPU缓存的命中率来优化程序的性能。

任何代码的执行都依赖CPU，通常，使用好CPU是操作系统内核的工作。然而，当我们编写计算密集型的程序时，CPU的执行效率就开始变得至关重要。由于CPU缓存由更快的SRAM构成（内存是由DRAM构成的），而且离CPU核心更近，如果运算时需要的输入数据是从CPU缓存，而不是内存中读取时，运算速度就会快很多。所以，了解CPU缓存对性能的影响，便能够更有效地编写我们的代码，优化程序性能。

然而，很多同学并不清楚CPU缓存的运行规则，不知道如何写代码才能够配合CPU缓存的工作方式，这样，便放弃了可以大幅提升核心计算代码执行速度的机会。而且，越是底层的优化，适用范围越广，CPU缓存便是如此，它的运行规则对分布式集群里各种操作系统、编程语言都有效。所以，一旦你能掌握它，集群中巨大的主机数量便能够放大优化效果。

接下来，我们就看看，CPU缓存结构到底是什么样的，又该如何优化它？

## CPU的多级缓存

刚刚我们提到，CPU缓存离CPU核心更近，由于电子信号传输是需要时间的，所以离CPU核心越近，缓存的读写速度就越快。但CPU的空间很狭小，离CPU越近缓存大小受到的限制也越大。所以，综合硬件布局、性能等因素，CPU缓存通常分为大小不等的三级缓存。
<div><strong>精选留言（30）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/11/82/3d/356fc3d6.jpg" width="30px"><span>忆水寒</span> 👍（91） 💬（4）<div>因为在多核CPU时代，CPU有“缓存一致性”原则，也就是说每个处理器（核）都会通过嗅探在总线上传播的数据来检查自己的缓存值是不是过期了。如果过期了，则失效。比如声明volitate，当变量被修改，则会立即要求写入系统内存。</div>2020-04-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/f6/00/2a248fd8.jpg" width="30px"><span>二星球</span> 👍（76） 💬（12）<div>一片连续的内存被加载到不同cpu核心中（就是同一个cache line在不同的cpu核心），其中一个cpu核心中修改cache line,其它核心都失效，加锁也是加在cache  line上，其它核心线程也被锁住，降低了性能。解决办法是填充无用字节数，使分开</div>2020-04-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/57/4f/6fb51ff1.jpg" width="30px"><span>奕</span> 👍（43） 💬（1）<div>配置 nginx server_names_bucket_siz 的大小
而桶大小为 50 字节，会导致最坏 2 次访问内存，而 70 字节最坏会有 3 次访问内存。
----------------------------------------------------
为什么 50字节会访问2次内存呢？ 不是可以加载 64k数据到缓存，包含了 50个字节，一次不就够了吗？
70k 也是同样的问题，为什么是3次啊</div>2020-04-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/82/3d/356fc3d6.jpg" width="30px"><span>忆水寒</span> 👍（28） 💬（3）<div>这个文章其实讲解的很细致，来龙去脉都说清楚了。不错！
其实每篇文章能讲到这个地步，作为读者（也可以称为学生）每篇能够学到一个哪怕很小的知识点，那也是值得的。</div>2020-04-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/4a/6f/e36b3908.jpg" width="30px"><span>xzy</span> 👍（25） 💬（8）<div>思考题：
数据从内存加载到高速缓存中，以块为基本单元（一个块64字节），相邻的两个变量很可能在同一块中，当这个数据块分别加载到两颗cpu的高速缓存中时，只要一个cpu对该块（高速缓存中缓存的块）进行写操作，那么另一cpu缓存的该块将失效。
可以通过将两个变量放到不同的缓存块中，来解决这个问题</div>2020-04-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/0c/52/f25c3636.jpg" width="30px"><span>长脖子树</span> 👍（21） 💬（5）<div>多线程并行访问不同的变量,  cpu 缓存的失效需要基于其中有一个 core 将 L1&#47;L2 cache 写回主存, 但这个时间是不固定的. 除非你使用  lock 等强制刷新到 主存 , 而其他 core 上的缓存行会置为 Invalid , 这就要提到 缓存一致性 MESIF 协议 
如果这些变量在内存布局中相邻的, 很有可能在同一个 cache line 中,  要避免竞争, 就要避免在同一个 缓存行中, 比如 java 中的方法:  手动在这个变量前后 padding 间隔开一定字节(一般 64 字节) 或者 @Contended 标记这个变量 </div>2020-04-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/c8/34/fb871b2c.jpg" width="30px"><span>海罗沃德</span> 👍（21） 💬（1）<div>第一篇就进入知识盲区了</div>2020-04-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/18/81/83b6ade2.jpg" width="30px"><span>好吃不贵</span> 👍（14） 💬（1）<div>思考题猜测是False sharing导致的，非常热的数据最好cache line对齐。</div>2020-04-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/63/0b/ad56aeb4.jpg" width="30px"><span>AI</span> 👍（12） 💬（1）<div>CPU性能优化的4个点：
1.按顺序访问数据（操作连续内存）：利用数据缓存，提高读数据缓存的命中率。
2.有规律的条件分支（如数据集先排序再处理）：利用指令缓存，提高读指令缓存的命中率。
3.数据按缓存行大小填充&#47;对齐（通常为64字节）：防止伪共享，提高并发处理能力和缓存命中率。
4.对于多核处理器，如果缓存命中率很高，可以考虑进行CPU绑定。</div>2020-05-25</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/30/6e/581b0307.jpg" width="30px"><span>鲤鲤鱼</span> 👍（9） 💬（3）<div>陶老师我们集群有一个问题，某一台物理机的CPU会被Hadoop yarn的查询任务打满，并且占用最多的pid在不停的变化，我查看了TIME_WAIT的个数好像也不是很多，在顶峰的时候还没达到一万，能够持续一两个小时。这个问题您有没有什么思路呢？</div>2020-04-27</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTICBNZjA9hW65x6g9b2iaicKUJW5gxFxtgPXH9Cqp6eyFfY1sD2hVY4dZrY5pmoK2r1KZEiaaIKocdZQ/132" width="30px"><span>赖阿甘</span> 👍（7） 💬（2）<div>此时内存是跳跃访问的，如果 N 的数值很大，那么操作 array[j][i]时，是没有办法把 array[j][i+1]也读入缓存的。
---------------------------------------------------------------------------------------------
老师是不是写错了，应该是”那么操作 array[j][i]时，是没有办法把 array[j+1][i]（而不是array[j][i+1]）也读入缓存的。”</div>2020-04-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/64/05/6989dce6.jpg" width="30px"><span>我来也</span> 👍（7） 💬（1）<div>老师代码准备的真多！

思考题有同学已经回答的非常准确了。
虽然已经看过了 linux性能优化 计算机组成原理 和 性能工程高手课 ，但看起老师的文章还是很有意思。
一些知识也加深了印象。

perf工具看来是要找个时间好好看看了。
最早是在linux性能优化专栏看到用到，今天在一篇公众号上看别人用这个快速定位了线上有问题的死循环函数，今天老师又提到了用它看命中率。

工具用好了真的是方便，lsof之前也没用过，后来用了几次觉得非常好用，现在就经常用了。</div>2020-04-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/67/dd/55aa6e07.jpg" width="30px"><span>罗帮奎</span> 👍（6） 💬（1）<div>多线程并发，如果一个core上的线程改变了变量，而其他core正好映射到相同的cacheLine上，则底层硬件会宣布所有其他core的缓存行失效。其它core下次需要重新去从主存中读取数据，来获取新的cacheLine。在多核系统上，这样会有严重的性能问题</div>2020-04-30</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/4f/3f/6f62f982.jpg" width="30px"><span>wangkx</span> 👍（6） 💬（2）<div>前几天学习了一下计算机组成原理。大部分都能听懂，开心~~~

本节讲到的性能优化实际上是涉及到了计算机组成原理中的【内存的局部性原理】以及【cpu的分支预测】。

对于课后的问题，因为多线程操作某些共享变量，涉及到变量的有效性问题（是否过期），如果变量在一个线程被修改，其他核心中的缓存失效啦。其他线程调用该变量的时候会从内存中重新加载到缓存。

所谓的如何解决，应该是解决缓存失效和保持数据一致性的问题，应该满足两点：
1. 写传播，即通知其他核心，某个缓存失效，需要从内存读取一下
2. 保证事务串行化，事务请求的顺序不能变化
我看资料了解到解决方案是基于总线嗅探机制的MESI协议来解决数据一致性问题。

在Java中，volatile 会确保我们对于这个变量的读取和写入，都一定会同步到主内存里，而不是从 Cache 里面读取，保证了数据一致性问题。 

这是我最近学习计算机组成原理后见解，不知道自己理解的有没有问题。有问题希望陶辉老师指正一下。</div>2020-04-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/39/fa/a7edbc72.jpg" width="30px"><span>安排</span> 👍（4） 💬（1）<div>内存伪共享问题，可以通过填充无效数据解决。
伪共享：假设cache line是64字节，我们在一个64字节的并且和cache line 对齐后的内存中放入两个4字节的整数A和B，然后线程a和b分别访问A和B，在内存层面的语义是这两个线程分别独享一块内存区域，操作时互不干扰，但是在缓存cache line层面他们是共享一个cache line的，是一个&quot;原子的数&quot;，这就是伪共享。
         缓存层面的伪共享的一致性由硬件保证，对程序员透明，也就是对这个&quot;原子数&quot;的操作不用显式加锁，但是伪共享降低程序效率。</div>2020-04-30</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/d0/6c/2e7dd298.jpg" width="30px"><span>卓明</span> 👍（3） 💬（1）<div>在jdk1.7以下的版本中，linkedTransferQueue有这方面的优化，使用追加字节的方式，来避免缓存行的竞争导致入队和出队的效率低下的问题，应该是同一个原因</div>2020-05-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/99/36/80d3f12b.jpg" width="30px"><span>Oliver</span> 👍（3） 💬（1）<div>对比开篇树图，numa架构貌似还没说，后续会提到吗？</div>2020-04-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/cf/96/251c0cee.jpg" width="30px"><span>xindoo</span> 👍（3） 💬（1）<div>https:&#47;&#47;zxs.io&#47;s&#47;o 我之前写过一篇博客详细介绍了cpu分支预测和性能差异，有兴趣可以参考下。 </div>2020-04-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/21/20/1299e137.jpg" width="30px"><span>秋天</span> 👍（2） 💬（1）<div>因为cache-line的大小是64kb，由于单个变量站的大小占用的缓存大小达不到64kb。所以存在多个内存变量共享一个缓存行。导致多线程访问不同变量的时候 缓存行失效。解决方法是采用缓存行填充的方式，让每个线程的不同变量，占用不同的缓存行，提高命中率。</div>2020-08-03</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/5f/83/bb728e53.jpg" width="30px"><span>Douglas</span> 👍（1） 💬（2）<div> a[i][j]   和    a[j][i]  孰优孰劣 需要看情况， 是 行 优先 还是列 优先？这一块老师是不是漏掉了？   </div>2021-01-16</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/57/af/0b39cab7.jpg" width="30px"><span>卒迹</span> 👍（1） 💬（1）<div>要学的课程太多了，一入IT深似海。</div>2020-04-28</li><br/><li><img src="" width="30px"><span>Geek_309f42</span> 👍（0） 💬（1）<div>补充一个知识，多核cpu下每个核都有自己的l1 l2</div>2023-11-25</li><br/><li><img src="" width="30px"><span>林腾</span> 👍（0） 💬（2）<div>请教两个java层面运用cpu缓存的场景： 1. java api如何指定线程绑定一颗cpu运行？ 2.如果采用string对象有什么方式可以减少由cpu缓存一致性带来的缓存失效的问题？</div>2020-12-15</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1f/13/e1/6939ae4f.jpg" width="30px"><span>knight劉先生</span> 👍（0） 💬（1）<div>列表遍历的区别，Python几乎没差别，思考了下，这个应该跟Python是通过引用指向对象有关</div>2020-12-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/d8/ee/6e7c2264.jpg" width="30px"><span>Only now</span> 👍（0） 💬（1）<div>这个失效，应该是在有读情况下才会吧。只读的情况下应该不会失效。</div>2020-11-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1a/e8/43/f9c0faed.jpg" width="30px"><span>小童</span> 👍（0） 💬（1）<div>我查看了我自己的 

hw.l1icachesize:32768;
hw.l1dcachesize:32768;

为什么l1有两个？
</div>2020-09-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/1f/66/59e0647a.jpg" width="30px"><span>万历十五年</span> 👍（0） 💬（1）<div>打卡第1天：
1.cpu一级缓存分数据缓存和指令缓存
2.顺序访问连续的内存可提高数据缓存命中率,
有规律的条件分支可以提高指令缓存命中率
3.对于计算密集型任务，可以绑定cpu以提高缓存命中率</div>2020-08-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/fc/16/293da3e8.jpg" width="30px"><span>麻将胡了2pg</span> 👍（0） 💬（1）<div>结合老师讲的，再加上评论区同学们的分享，感觉把自己的视野一下打开了。点赞了</div>2020-08-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/a9/cb/a431bde5.jpg" width="30px"><span>木头发芽</span> 👍（0） 💬（1）<div>这一篇边学边思考再加看C++&#47;java的代码花了1小时,看评论后引申出的缓存一致性,volitate用法等去查资料学习又花了1小时. 满满的收货</div>2020-08-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1b/77/c0/22872965.jpg" width="30px"><span>LindaWang</span> 👍（0） 💬（2）<div>请问老师，这是跟系统内核版本有关吗？我的当前系统X86 Ubuntu 16.04 内核 4.4.0-21-generic， 不支持L1-dcache-load-misses、L1-dcache-loads这些events
perf stat -e cache-references,cache-misses,instructions,cycles,L1-dcache-load-misses,L1-dcache-loads .&#47;branch_predict -
 1127

 Performance counter stats for &#39;.&#47;branch_predict -&#39;:

         5,205,676      cache-references
         4,595,532      cache-misses              #   88.279 % of all cache refs
     1,631,836,685      instructions              #    0.50  insns per cycle
     3,268,533,223      cycles
   &lt;not supported&gt;      L1-dcache-load-misses
   &lt;not supported&gt;      L1-dcache-loads

       1.201545784 seconds time elapsed
</div>2020-07-17</li><br/>
</ul>