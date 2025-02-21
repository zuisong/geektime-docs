你好，我是文强。

到了这节课，我们的课程已经讲完三分之一了。前面我们讲了消息队列各个模块的设计、权衡、思考、选型，基本覆盖了基础核心架构中的所有细节了。

我一直认为，架构设计选型和编码是两个事情，魔鬼在细节，不管多牛逼的架构，都需要细致的工程化实现，才能达到我们预期的效果。这节课我们将用很零散的方式讲一下用 Java 来开发存储系统时会用到的一些技巧及其背后的原理。其中的每个知识点都是独立的，你可以挑自己感兴趣的部分学习。

## PageCache 调优和 Direct IO

我们一直会听到PageCache，简单理解它就是内存。写内存性能肯定是最高的。但是PageCache 并不是万能的，在某些情况下会存在命中率低，导致读写性能不高的情况。遇到这种情况，就需要在业务上进行处理。我们先来看下面这张图：

![](https://static001.geekbang.org/resource/image/58/80/586ac52baff5c8c9e6644da62d962f80.jpg?wh=10666x4844)

如上图所示，应用程序读取文件，会经过应用缓存、PageCache、DISK（硬盘）三层。即应用程序读取文件时，Linux 内核会把从硬盘中读取的文件页面缓存在内存一段时间，这个文件缓存被称为 PageCache。

**缓存的核心逻辑是：**比如应用层要读1KB文件，那么内核的预读算法则会以它认为更合适的大小进行预读 I/O，比如 16-128KB。当应用程序下次读数据的时候，会先尝试读PageCache，如果数据在PageCache中，就会直接返回；如果数据不在PageCache中，就会触发从硬盘读取数据，效率就会变低。
<div><strong>精选留言（3）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/2a/29/ab/59a6e437.jpg" width="30px"><span>Kevin</span> 👍（1） 💬（0）<div>干货总结，点赞six six six</div>2023-08-07</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/c9/ea/08c2cc5b.jpg" width="30px"><span>如果可以改变</span> 👍（1） 💬（2）<div>在某些场景下，比如数据的集合长度是固定的时候，可以考虑数组替代或者重写 Map，用来降低 HashMap 的 overheap。
上述 HashMap 的 overheap 应该是 overhead 吧！老师，如何降低 map 的 overhead ？</div>2023-07-31</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/tJxR1fwzvhmL3CVmpfC37zibAwDlEiaLDF0M834E3op7ULuTK2U7B8OEMbHUibPxHiasCayzicC5ian02jpPV1ibjSrCw/132" width="30px"><span>Geek_db7484</span> 👍（0） 💬（0）<div>Unsafe JDK 9 没有被禁用</div>2024-06-17</li><br/>
</ul>