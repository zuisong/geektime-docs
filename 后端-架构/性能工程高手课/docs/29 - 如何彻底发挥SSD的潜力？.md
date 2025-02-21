你好，我是庄振运。

今天是“性能工程实践”这个模块的最后一讲，我们来讨论一种“软硬件结合”的性能工程优化实践，与SSD（硬件）有关。现在SSD用的越来越普遍的情况你一定非常清楚，但是你设计的应用程序（软件）真的充分利用了SSD的特点，并发挥SSD的潜力了吗？

要知道，SSD可不仅仅是“更快的HDD”。

SSD的好处显而易见，它作为存储时，应用程序可以获得更好的I/O性能。但是这些收益，主要归因于SSD提供的更高的IOPS和带宽。如果你因此只将SSD视为一种“更快的HDD”，那就真是浪费了SSD的潜力。

如果你在设计软件时，能够充分考虑SSD的工作特点，把应用程序和文件系统设计为“对SSD友好”，会使服务性能有个质的飞跃。

今天我们就来看看，**如何在软件层进行一系列SSD友好的设计更改**。

## 为什么要设计SSD友好的软件？

设计对SSD友好的软件有什么好处呢？简单来说，你可以获得三种好处：

1. 提升应用程序等软件的性能；
2. 提高SSD的 I/O效率；
3. 延长SSD的寿命。

先看第一种好处——**更好的应用程序性能**。在不更改应用程序设计的情况下，简单地采用SSD可以获得性能提升，但无法获得最佳性能。

我为你举个例子来说明。我们曾经有一个应用程序，它需要不断写入文件以保存数据，主要性能瓶颈就是硬盘I/O。使用HDD时，最大应用程序吞吐量为142个查询/秒（QPS）。无论我们对应用程序设计进行什么样的更改或调优，这就是使用HDD可以获得的最好性能了。
<div><strong>精选留言（7）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/13/39/fa/a7edbc72.jpg" width="30px"><span>安排</span> 👍（0） 💬（1）<div>应用层多线程写入数据，那不是写到了操作系统的缓存里了吗，内核线程刷盘的时候还会用多线程写入ssd吗？应用层多线程写入的好处感觉没讲清楚，应用层多线程写入应该利用文件系统层或者通用快层提供的能力来体现出优势，而不是直接对接ssd内部的并行写入机制，除非你的应用绕过这两层直接操作裸盘。</div>2020-04-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/64/05/6989dce6.jpg" width="30px"><span>我来也</span> 👍（0） 💬（1）<div>对于个人的电脑，考虑到ssd硬盘寿命，会适当确保磁盘空闲比例。

但对于云服务器，还是先保证性能吧，有精力了再考虑放大系数。😄</div>2020-02-06</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/eb/73/4352d691.jpg" width="30px"><span>木行</span> 👍（0） 💬（2）<div>老师您好，Cassandra升级memcached缓存到本地ssd这部分有参考链接吗，想进一步了解下，但网上没有搜索到</div>2020-02-02</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/2c/45/c6/28dfdbc9.jpg" width="30px"><span>*</span> 👍（0） 💬（0）<div>ssd内部并行度要怎么看是多少的</div>2023-05-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/d0/4d/2116c1a4.jpg" width="30px"><span>Bravery168</span> 👍（0） 💬（0）<div>对SSD友好的软件设计，似乎更多的在于系统软件层面的设计，从上层应用来说，可直接优化的应该不多。不过理解了SSD的原理，确实有助于思考怎么用好。</div>2021-04-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/85/49/585c69c4.jpg" width="30px"><span>皮特尔</span> 👍（0） 💬（0）<div>软件工程师也需要懂硬件才行呀。

关于SSD，隔壁专栏《深入浅出计算机组成原理》也有讲到，大家有兴趣的可以去看看。</div>2020-06-01</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/67/f4/9a1feb59.jpg" width="30px"><span>钱</span> 👍（0） 💬（0）<div>受教了，公司有用SSD存储的，不过也确实没意识到从代码层面来写出对SSD友好的程序。</div>2020-03-14</li><br/>
</ul>