你好，我是LMOS。

上节课我们学习了伙伴系统，了解了它是怎样管理物理内存页面的。那么你自然会想到这个问题：Linux系统中，比页更小的内存对象要怎样分配呢？

带着这个问题，我们来一起看看**SLAB分配器的原理和实现。**在学习过程中，你也可以对照一下我们Cosmos的内存管理组件，看看两者的内存管理有哪些异同。

## SLAB

与Cosmos物理内存页面管理器一样，Linux中的伙伴系统是以页面为最小单位分配的，现实更多要以内核对象为单位分配内存，其实更具体一点说，就是根据内核对象的实例变量大小来申请和释放内存空间，这些数据结构实例变量的大小通常从几十字节到几百字节不等，远远小于一个页面的大小。

如果一个几十字节大小的数据结构实例变量，就要为此分配一个页面，这无疑是对宝贵物理内存的一种巨大浪费，因此一个更好的技术方案应运而生，就是**Slab分配器**（由Sun公司的雇员Jeff Bonwick在Solaris 2.4中设计并实现）。

由于作者公开了实现方法，后来被Linux所借鉴，用于实现内核中更小粒度的内存分配。看看吧，你以为Linux很强大，真的强大吗？不过是站在巨人的肩膀上飞翔的。

### 走进SLAB对象

何为SLAB对象？在SLAB分配器中，它把一个内存页面或者一组连续的内存页面，划分成大小相同的块，其中这一个小的内存块就是SLAB对象，但是这一组连续的内存页面中不只是SLAB对象，还有SLAB管理头和着色区。
<div><strong>精选留言（19）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/0f/bb/85/191eea69.jpg" width="30px"><span>搬铁少年ai</span> 👍（5） 💬（2）<div>回答有的同学关于为什么是196大小的问题

这里196大小的对象，应该是专门针对256B以下小内存进行的优化，正常情况支持的对象大小都是2的n次方，2的七次方是128，8次方就是256了。所以这里在不违反缓存对其的前提下，单独支持了196大小的对象。

如果cache line 是32的话，192&#47;32=6，也是缓存对其的，那么如果申请的内存在129到192之间时，就不必去分配256大小的对象，而是可以分配192大小的对象，可以在满足缓存对齐的前提下节省空间。

除了192，另外在2的6次方和7次方之间，也特殊支持了96b大小的对象，同样是类似的原理。

理论上能够背cache line大小整除的都可以特殊支持，只不过256以上的对象可能不常见，slab申请了特殊大小的对象却没有人用，反倒是一种浪费</div>2021-11-05</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/ec/13/49e98289.jpg" width="30px"><span>neohope</span> 👍（15） 💬（2）<div>一、数据结构
系统有一个全局kmem_cache_node数组，每一个kmem_cache_node结构，对应一个内存节点

kmem_cache_node结构，用三个链表管理内存节点的全部kmem_cache【slab管理结构】，包括：
slabs_partial，对象部分已分配的kmem_cache结构；
slabs_full，对象全部已分配的kmem_cache结构；
slabs_free ，对象全部空闲kmem_cache结构；

kmem_cache结构，slab管理头，包括：
array_cache，每个CPU一个，用于管理空闲对象。 array_cache的entry数组，用于管理这些空闲对象，出入遵循LIFO原则；
num，表示对象个数；
gfporder，表示页面的大小 (2^n)；
colour，表示着色区大小。着色区，主要利用SLAB划分对象剩余的空间，让SLAB前面的几个对象，根据cache line大小进行偏移，以缓解缓存过热的问题，防止Cache地址争用，防止引起Cache抖动；

此外，全局有一个slab_caches链表中，记录了系统中全部的slab

二、初始化
全局有一个kmem_cache结构，kmem_cache_boot，用于初始化
全局有一个kmem_cache_node数组结构init_kmem_cache_node，用于初始化

x86_64_start_kernel-&gt;x86_64_start_reservations-&gt;start_kernel-&gt;mm_init -&gt; kmem_cache_init
1、将变量kmem_cache指向静态变量kmem_cache_boot
2、初始化全局的init_kmem_cache_node结构
3、调用create_boot_cache，初始化kmem_cache_boot结构
4、将kmem_cache_boot其加入全局slab_caches链表中
5、调用create_kmalloc_cache，建立第一个kmem_cache，供kmalloc函数使用
6、调用init_list函数，将静态init_kmem_cache_node，替换为用kmalloc生成的kmem_cache_node
7、 调用create_kmalloc_caches，创建并初始化了全部 kmalloc_caches中的kmem_cache
路径为：kmem_cache_init-&gt;create_kmalloc_caches-&gt; new_kmalloc_cache-&gt; create_kmalloc_cache

三、对象分配
kmalloc-&gt;__kmalloc-&gt;__do_kmalloc
-&gt;kmalloc_slab
从kmalloc_caches中，根据类型和大小，找到对应的 kmem_cache
-&gt;slab_alloc-&gt;__do_cache_alloc-&gt;____cache_alloc
1、第一级分配，如果array_cache.entry中有空闲对象，直接分配
2、如果一级分配失败，调用cache_alloc_refill，进行第二级分配
-&gt;-&gt;cache_alloc_refill从全局的slab中进行refill
1、如果没有空闲对象，而且shared arry没有共享对象可用，需要扩容
2、如果shared arry有空闲对象，直接分配，否则继续
3、尝试从kmem_cache_node结构中其它kmem_cache获取slab页面
4、如果都失败了就扩容

如果一、二级分配都失败了，那就扩容，并进行第三级分配：
1、再次尝试在不扩容情况下，分配新的kmem_cache并初始化，如果成功就返回
2、调用cache_grow_begin 函数，找伙伴系统分配新的内存页面，找第一个 kmem_cache 分配新的对象，来存放 kmem_cache 结构的实例变量，并进行必要的初始化
3、调用 cache_grow_end 函数，把这页面挂载到 kmem_cache_node 结构的空闲链表中
4、返回一个空闲对象

四、对象回收
kfree-&gt;__cache_free-&gt;___cache_free-&gt;__free_one
将对象清空后，还给了CPU的对应的array_cache
</div>2021-07-07</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/43/61/eeefa369.jpg" width="30px"><span>tony</span> 👍（2） 💬（1）<div>既然已经有了slab分配机制，为什么在用户态还有ptmalloc以及tcmalloc？它们侧重点有什么不一样</div>2022-11-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/17/06/7e/735968e2.jpg" width="30px"><span>西门吹牛</span> 👍（2） 💬（1）<div>之前学 netty，netty 中用到了伙伴算法实现内存分配与释放，说下 netty 中的实现吧：
首先会预申请一大块内存 PoolArena，内部由 6 个 PoolChunkList，和俩个 PoolSubpage[]
● 6 个 PoolChunkList：分别是 qInit、q000、q025、q050、q075、q100
  ○ Netty 根据 PoolChunk 的使用率，将他们分别放入对应的 PoolChunkList 中，目的减少内存碎片
  ○ 每个 PoolChunk 默认 16MB，每个 PoolChunk 有划分为 2048 个 Subpage，每个 Subpage 8KB，16MB&#47;2048 = 8KB
  ○ PoolChunk 划分的 2048 个 8KB 的 Subpage 构成满二叉树
● PoolSubpage[]：用于分配小于 8KB 的内存
  ○ PoolSubpage[] 中的元素是指向 8KB 大小的 Subpage 地址，同时又把 8KB 的 subpage 分割成大小相等的段，比如 32B，64B......

分配大于 8 KB 的内存，直接走 PoolChunk 对应满二叉树，这样们更好的避免内存碎片，比如：
  ○ 先分配 8KB：需要一个 Page ，满二叉树最下一层满足要求，故分配这层的第一个节点page0
  ○ 在分配 16KB：需要两个Page ，满二叉树倒数第二层满足要求，因为这层的下一层的第一个节点page0已被分配，所以选这层第二个节点，就是相当分配 page2和page3
  ○ 在分配 8KB：需要一个 Page ，满二叉树最下一层满足要求，page0 以占用，往后page1可用，直接分配
经过这样分配，最终分配的是page0、page1、page2、page3 刚好这四个页是连续的。

对于小于 8KB 的分配：比如32B：
  ○ 定位到 PoolSubpage[] 中的元素，看有没有值，没有代表之前没有分配过，执行分配，有值代表之前分配过 32B 的空间
  ○ 如果没有分配过，那么先取一个 8KB的page，将数组中对应的元素指向该page
  ○ 在将 8KB 的page  按 32B 划分成相等的段，然后取划分好的第一个 32B 的段拿出使用，并把该段标记为占用
  ○ 等下次在分配 32B 的时候，先定位到数组对应的元素，有值代表之前分配过 32B 的空间，那么该元素指向的 page 已经是被按 32B 划分好的相同的小段
  ○ 那么就可以直接从划分好的小段中，依次遍历，取出没有使用的那个 32B 的段来分配
也就是说，第一次分配小于 8KB (比如32B)的内存的时候，已经在内存中分配好了若干相同的32B 的段了，后续可以直接取用第一次分配好的

当然，其中还有很多细节，比如是否池化，内存释放之后，是直接归还，还是先缓存起来，下次在用，多线程申请的时候，怎么避免竞争等问题

</div>2022-07-06</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/da/b5/9d1f2f55.jpg" width="30px"><span>朱熙</span> 👍（2） 💬（1）<div>linux内核包括三种小对象管理方式，slab，slub和slob，其中slob效率较低用于嵌入式等，linux默认使用slub</div>2021-07-03</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/2d/06/30/c26ea06a.jpg" width="30px"><span>艾恩凝</span> 👍（1） 💬（1）<div>打卡，看了记，记了忘，忘了看，内存的相关学习，我在路上</div>2022-04-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/bb/85/191eea69.jpg" width="30px"><span>搬铁少年ai</span> 👍（1） 💬（1）<div>请教老师，为什么有的资料说struct page就是slab，您这里说kmem_cache是描述slab，有点糊涂。</div>2021-11-03</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/bb/85/191eea69.jpg" width="30px"><span>搬铁少年ai</span> 👍（1） 💬（1）<div>请教老师，我看kmem_cache源码里的node是一个指向kmem_cache_node的指针数组，您这里给的是一个指针，如果是指针我是理解的，但是如果是指针数组，我不明白为什么需要多个node管理kmem_cache(slab头)</div>2021-11-02</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/26/82/0c/cc106ab1.jpg" width="30px"><span>Samaritan.</span> 👍（1） 💬（1）<div>“在 Linux 中，SLAB 管理头用 kmem_cache 结构来表示，代码如下”，请问一下，作者引用的是linux的哪个内核版本的代码呀？</div>2021-09-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/27/f8/2c/92969c48.jpg" width="30px"><span>青玉白露</span> 👍（1） 💬（1）<div>其实在 kmalloc_slab 函数已经写明了，最大是192，单位应该是B吧？</div>2021-07-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/52/40/e57a736e.jpg" width="30px"><span>pedro</span> 👍（1） 💬（1）<div>Cosmos YYDS！！！
问题答案看代码注释，最大192</div>2021-06-30</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/3b/d7/42/d37aaa5b.jpg" width="30px"><span>小灰象</span> 👍（0） 💬（1）<div>翻过内存管理的大山啦！可喜可贺！！！</div>2024-08-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/fa/b0/f70ec8a0.jpg" width="30px"><span>弘文要努力</span> 👍（0） 💬（1）<div>请问老师的源码从哪里获取呢？</div>2022-04-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/27/f8/2c/92969c48.jpg" width="30px"><span>青玉白露</span> 👍（0） 💬（1）<div>思考题有点像脑筋急转弯······
几处的注释都表明了最大值是192
不过这个值是怎么定的呢？</div>2021-06-30</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/3e/e7/261711a5.jpg" width="30px"><span>blentle</span> 👍（0） 💬（1）<div>最多192吧，

&#47;&#47;计算出index
    if (size &lt;= 192) {
        if (!size)
            return ZERO_SIZE_PTR;
        index = size_index[size_index_elem(size)];
    } else {
        if (WARN_ON_ONCE(size &gt; KMALLOC_MAX_CACHE_SIZE))
            return NULL;
        index = fls(size - 1);
    }</div>2021-06-30</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/3b/e0/9b/6a227f73.jpg" width="30px"><span>建涛</span> 👍（0） 💬（0）<div>老师您好，我看您给出的源码，在发现没有空闲内存对象的时候，会新建kmem_cache实例。但我看具体代码，好像是将新增的page挂载到原先的kmem_cache上面来扩展slab，求解惑。</div>2025-02-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/3b/e0/9b/6a227f73.jpg" width="30px"><span>建涛</span> 👍（0） 💬（0）<div>if (unlikely(!ac-&gt;avail)) { &#47;&#47;分配新的kmem_cache并初始化 page = cache_grow_begin(cachep, gfp_exact_node(flags), node); ac = cpu_cache_get(cachep); if (!ac-&gt;avail &amp;&amp; page) alloc_block(cachep, ac, page, batchcount); &#47;&#47;让page挂载到kmem_cache_node结构的slabs_list链表上 cache_grow_end(cachep, page); if (!ac-&gt;avail) return NULL; }           &#39;
老师您好,这段代码好像没有分配新的kmem_cache实例呀，而是将新的page挂载到原先的cachep上诶，求老师解答，疑惑很久了。呜呜呜</div>2025-02-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/37/4f/ef/4d4b1260.jpg" width="30px"><span>庄重</span> 👍（0） 💬（0）<div>我有个疑惑，slab分配器和伙伴算法管理的是虚拟内存还是物理内存？
因为我目前认知是最底层的物理内存管理，在这之上是mmu和分页(10-10-12分页等)开启了虚拟内存的映射，上面就是虚拟内存的管理算法，我困惑的点是这两种算法在linux中属于管理物理内存还是虚拟内存。</div>2024-03-05</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/bb/85/191eea69.jpg" width="30px"><span>搬铁少年ai</span> 👍（0） 💬（0）<div>SLAB 支持的最大 size 不是 2 的 25 次方 32MB 吗？大家说的 192B 是为什么呢？</div>2021-11-05</li><br/>
</ul>