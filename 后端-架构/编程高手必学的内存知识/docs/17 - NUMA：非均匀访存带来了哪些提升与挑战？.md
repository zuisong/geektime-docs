你好，我是海纳。

在硬件篇的最后一节课，我们来看两个比较重要的物理内存问题。在[第1节课](https://time.geekbang.org/column/article/430073)，我们讲到物理内存就是指主存，这句话是不太精确的，其实大型服务器的物理内存是由很多部分组成的，主要包含**外设所使用的内存和主存**。

这节课，我们先会对计算机是如何组织外设所使用的内存进行分析，因为这是你了解设备驱动开发的基础；接下来，我们将分析主存，不过在展开之前，你还是需要了解一下它的内部结构，才能更好的理解。

如果你从CPU的角度去看，就会发现物理内存并不是平坦的，而是坑坑洼洼的。正是因为这样的特点，也就导致CPU对物理内存的访问速度也不一样。同时，有些内存可以使用CPU Cache，有些则不可以。我们把这种组织方式称为**异质（Heterogeneity）式**的结构。

再往深入拆解，在异质式结构中，CPU不仅仅对外设内存和主存的访问速度不一样，它访问主存不同区间的速度也不一样。换句话说，**不同的CPU访问不同地址主存的速度各不相同**，我们把采用这种设计的内存叫做非一致性访存（Non-uniform memory access，NUMA）。

通常，在进行应用程序内存管理时，正确使用NUMA可以极大地提升应用程序的吞吐量；相应地，如果NUMA的配置不合理，也有可能带来比较大的负面影响。而且，在多核体系结构的服务器上，合理地通过控制NUMA的绑定，来提升应用程序的性能，对于服务端程序员至关重要。为了帮助你合理运用NUMA，今天这节课，我们就来详细分析NUMA会为应用程序带来哪些提升与挑战。
<div><strong>精选留言（5）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/12/23/66/413c0bb5.jpg" width="30px"><span>LDxy</span> 👍（3） 💬（1）<div>NUMA架构是用于多个CPU的架构而不是多核单CPU的架构吧？Linux的终端模式是不是就是字符模式，而桌面模式就是图形模式？</div>2021-12-07</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/18/39/d2/845c0e39.jpg" width="30px"><span>送过快递的码农</span> 👍（2） 💬（1）<div>老师，nginx采用多进程的模型通过绑定核心的方式，是不是也是巧妙运用NUMA架构？</div>2021-12-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/18/39/d2/845c0e39.jpg" width="30px"><span>送过快递的码农</span> 👍（0） 💬（1）<div>是不是有段内存是留给bios的？老师我在mac上面通过gcc把一个简单的c变异最终得到a.out 和老师专栏里面多次提到的a.out是一回事儿么？表示类unix下的课执行文件么？</div>2021-12-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/19/00/1b/eee13196.jpg" width="30px"><span>李圣悦</span> 👍（0） 💬（0）<div>最近dpdk上做开发，还一直在想这个问题，数据包从一个网卡收包处理完转发到另外一个网卡，网卡1绑定到node0，网卡2绑定到node1；从网卡1到网卡2，业务内存在node0上分配；从网卡2到网卡2，业务内存应该在node1上分配；但业务内存没法拆成两个方向，请教老师，这个该怎么处理比较好？</div>2022-04-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/25/3c/92/81fa306d.jpg" width="30px"><span>张Dave</span> 👍（0） 💬（0）<div>swap替换，哪一章节有详细介绍啊？</div>2022-02-10</li><br/>
</ul>