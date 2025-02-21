你好，我是LMOS。

前面我们实现了Cosmos的内存管理组件，相信你对计算机内存管理已经有了相当深刻的认识和见解。那么，像Linux这样的成熟操作系统，又是怎样实现内存管理的呢？

这就要说到Linux系统中，用来管理物理内存页面的**伙伴系统**，以及负责分配比页更小的内存对象的**SLAB分配器**了。

我会通过两节课给你理清这两种内存管理技术，这节课我们先来说说伙伴系统，下节课再讲SLAB。只要你紧跟我的思路，再加上前面的学习，真正理解这两种技术也并不难。

## 伙伴系统

伙伴系统源于Sun公司的Solaris操作系统，是Solaris操作系统上极为优秀的物理内存页面管理算法。

但是，好东西总是容易被别人窃取或者效仿，伙伴系统也成了Linux的物理内存管理算法。由于Linux的开放和非赢利，这自然无可厚非，这不得不让我们想起了鲁迅《孔乙己》中的：“窃书不算偷”。

那Linux上伙伴系统算法是怎样实现的呢？我们不妨从一些重要的数据结构开始入手。

### 怎样表示一个页

Linux也是使用分页机制管理物理内存的，即Linux把物理内存分成4KB大小的页面进行管理。那Linux用了一个什么样的数据结构，表示一个页呢？

早期Linux使用了位图，后来使用了字节数组，但是现在Linux定义了一个page结构体来表示一个页，代码如下所示。
<div><strong>精选留言（11）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/0f/ec/13/49e98289.jpg" width="30px"><span>neohope</span> 👍（33） 💬（1）<div>一、整理一下思路
NUMA体系下，每个CPU都有自己直接管理的一部分内存，叫做内存节点【node】，CPU访问自己的内存节点速度，快于访问其他CPU的内存节点；
每个内存节点，按内存的迁移类型，被划分为多个内存区域【zone】；迁移类型包括ZONE_DMA、ZONE_DMA32、ZONE_NORMAL 、ZONE_HIGHMEM、ZONE_MOVABLE、ZONE_DEVICE等；
每个内存区域中，是一段逻辑上的连续内存，包括多个可用页面；但在这个连续内存中，同样有不能使用的地方，叫做内存空洞；在处理内存操作时，要避免掉到洞里；

二、整理一下结构
每个内存节点由一个pg_data_t结构来描述其内存布局；
每个pg_data_t有一个zone数组，包括了内存节点下的全部内存区域zone；
每个zone里有一个free_area数组【0-10】，其序号n的元素下面，挂载了全部的连续2^n页面【page】，也就是free_area【0-10】分别挂载了【1个页面，2个页面，直到1024个页面】
每个free_area，都有一个链表数组，按不同迁移类型，对所属页面【page】再次进行了划分

三、分配内存【只能按2^n页面申请】
alloc_pages-&gt;alloc_pages_current-&gt;__alloc_pages_nodemask
-&gt;get_page_from_freelist，快速分配路径，尝试直接分配内存
-&gt;__alloc_pages_slowpath，慢速分配路径，尝试回收、压缩后，再分配内存，如果有OOM风险则杀死进程-&gt;实际分配时仍会调用get_page_from_freelist
-&gt;-&gt;所以无论快慢路径，都会到rmqueue
-&gt;-&gt;-&gt;如果申请一个页面rmqueue_pcplist-&gt;__rmqueue_pcplist
1、如果pcplist不为空，则返回一个页面
2、如果pcplist为空，则申请一块内存后，再返回一个页面
-&gt;-&gt;-&gt;如果申请多个页面__rmqueue_smallest
1、首先要取得 current_order【指定页面长度】 对应的 free_area 区中 page
2、若没有，就继续增加 current_order【去找一个更大的页面】，直到最大的 MAX_ORDER
3、要是得到一组连续 page 的首地址，就对其脱链，然后调用expand函数对内存进行分割
-&gt;-&gt;-&gt;-&gt;expand 函数分割内存
1、expand分割内存时，也是从大到小的顺序去分割的
2、每一次都对半分割，挂载到对应的free_area，也就加入了伙伴系统
3、直到得到所需大小的页面，就是我们申请到的页面了

四、此外
1、在整个过程中，有一个水位_watermark的概念，其实就是用于控制内存区是否需要进行内存回收
2、申请内存时，会先按请求的 migratetype 从对应类型的page结构块中寻找，如果不成功，才会从其他 migratetype 的 page 结构块中分配， 降低内存碎片【rmqueue-&gt;__rmqueue-&gt;__rmqueue_fallback】
3、申请内存时，一般先在CPU所属内存节点申请；如果失败，再去其他内存节点申请；具体顺序，和NUMA memory policy有关；</div>2021-06-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/52/40/e57a736e.jpg" width="30px"><span>pedro</span> 👍（8） 💬（2）<div>迟到了，迟到了！每节都评论是我一直坚持的事，我以此为傲。

问题答案已经在文中了，最大1024页，每页4kb，答案也就呼之欲出了。

之前我一直在内心吐槽东哥写代码的函数名太难伺候了，现在来看linux的命名，不说优雅与否，就连基本的表意都办不到啊，东哥简直就是内核届的一股清流啊。</div>2021-06-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/3e/e7/261711a5.jpg" width="30px"><span>blentle</span> 👍（4） 💬（1）<div>最大order是11. 一个块是4k大小所以最大能分配
2的10次方乘以4 也就是4MB的的物理内存吧</div>2021-06-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1d/68/36/478194f3.jpg" width="30px"><span>Shawn Duan</span> 👍（2） 💬（1）<div>请问内存空洞是如何形成的呢？</div>2021-11-02</li><br/><li><img src="" width="30px"><span>springXu</span> 👍（2） 💬（1）<div>还是按照阅读理解题解答问的问题。
free_area 结构的数组，这个数组就是用于实现伙伴系统的。其中 MAX_ORDER 的值默认为 11，分别表示挂载地址连续的 page 结构数目为 1，2，4，8，16，32……最大为 1024。

所以是1024个pages，如果每个page是4k大小的话，那1024x4k=4m。 所以按MAX_ORDER默认值11，连续内存是4M</div>2021-06-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/25/9f/be/14b2ad2e.jpg" width="30px"><span>卖薪沽酒</span> 👍（0） 💬（1）<div>打卡打卡</div>2022-07-03</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/2d/06/30/c26ea06a.jpg" width="30px"><span>艾恩凝</span> 👍（0） 💬（1）<div>先打卡这个吧，轻松一下，啃完之前的，这个理解起来轻车熟路</div>2022-04-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/26/eb/d7/90391376.jpg" width="30px"><span>ifelse</span> 👍（0） 💬（1）<div>膜拜评论区各位大神</div>2022-02-16</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/2a/58/a7/51cb2340.jpg" width="30px"><span>lzd</span> 👍（0） 💬（1）<div>最大连续内存 = MAX_ORDER_NR_PAGES * PAGE_SIZE
MAX_ORDER_NR_PAGES : (1 &lt;&lt; (MAX_ORDER-1))
MAX_ORDER : (11)
PAGE_SIZE : 4k&#47;16k&#47;64k</div>2021-10-14</li><br/><li><img src="" width="30px"><span>Geek2808</span> 👍（0） 💬（1）<div>老师好，请教一个问题，当内核分配内存时，__alloc_pages_slowpath找不到也没法回收或者整理出空闲页，在开启swap的情况下，其中slab&#47;slub部分的匿名页会调用shrink_inactive_list 函数会扫描inactive list，将不活跃的page置换到swap分区。但是swap有的时候几M、几百M甚至几个G，这个内核置换的机制或算法逻辑是啥？为啥一次性会swap out这么多内存数据？(我理解这个时间点本身应用程序或内核不会一次性申请几个G的内存)</div>2021-07-31</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/65/89/9308706d.jpg" width="30px"><span>Jesus</span> 👍（0） 💬（1）<div>老师，这个课程什么时候更新完呀？想攒一些章节连续看。</div>2021-06-28</li><br/>
</ul>