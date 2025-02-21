你好，我是海纳。

在前面的几节课程中，我们学习了 CMS 、G1 等垃圾回收算法，这两类GC算法虽然一直在想办法降低GC时延，但它们仍然存在相当可观的停顿时间。

如何进一步降低GC的停顿时间，是当前垃圾回收算法领域研究的最热点话题之一。今天我们就来学习这类旨在减少GC停顿的垃圾回收算法，也就是**无暂停GC**（Pauseless GC）。由于Hotspot的巨大影响力和普及程度，以及它的代码最容易获得，我们这节课就以ZGC为例来深入讲解无暂停GC。

而且，ZGC对Java程序员的意义和G1是同样重要的。如果说CMS代表的是过去式，而G1是一种过渡（尽管这个过渡期会很长），那么ZGC无疑就是JVM自动内存管理器的未来。

通过这节课的学习，你就能了解到无暂停GC的基本思想和可以使用的条件，从而为未来正确地使用无暂停GC做好充分的准备。

无暂停GC这个词你可能比较陌生，让你觉得这个算法很难，我们不妨先来了解一下它的前世今生，你就能知其然，经过后面对它原理的讲解，你就能知其所以然了。

## 无暂停GC简介

JVM的核心开发者Cliff Click供职于Azul Systems公司期间，撰写了一篇很重要的论文，也就是[Pauseless GC](https://www.usenix.org/legacy/events/vee05/full_papers/p46-click.pdf)，提出了无暂停GC的想法和架构设计。同时，Azul公司也在他们的JVM产品Zing中实现了一个无暂停GC，将GC的停顿时间大大减少，这就是[C4垃圾回收器](https://www.azul.com/products/components/pgc)。
<div><strong>精选留言（4）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/10/cd/ed/825d84ee.jpg" width="30px"><span>费城的二鹏</span> 👍（10） 💬（1）<div>使用 forwarding table 的好处是，在remap前就可以释放已经被迁移的 page，只要保留 forwarding 即可，减少内存占用。
而如果使用 forwarding point 则需要一直保留这个page 直到重映射完成。

另一方面是性能考虑，提升了吞吐量</div>2021-12-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/50/b3/084e2dde.jpg" width="30px"><span>Danta</span> 👍（0） 💬（0）<div>复制对象过程中是不是要禁止修改对象啊</div>2022-02-25</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/d4/f3/129d6dfe.jpg" width="30px"><span>李二木</span> 👍（0） 💬（1）<div>由于remap 会等待下一次mark，这里的下一次mark是下一次垃圾回收吗？如果是那假如很久不触发回收，那之前标记的对象都还是通过forwarding table获取了哦？</div>2021-12-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/cd/ed/825d84ee.jpg" width="30px"><span>费城的二鹏</span> 👍（0） 💬（2）<div>我想问一个关于染色指针的问题。

假如有 a，b，c 三个对象。a 和 b均引用c，在扫描过程中，对指针做标记，是在 a 和 b对象存储的引用上加标记吗？还是一个公共空间加标记？如何确保修改了a引用c的地址后，b也可以做修改？

看了内容，感觉这个指针标记的修改有点像公共空间，改一次就行了。</div>2021-12-20</li><br/>
</ul>