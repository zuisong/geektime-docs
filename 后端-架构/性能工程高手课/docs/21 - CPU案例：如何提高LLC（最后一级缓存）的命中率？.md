你好，我是庄振运。

前面两讲中，我介绍了性能优化的六大原则和十大策略。从今天开始，我们来通过具体案例的解决方案讲解，了解这些原则和策略是如何应用的。

首先，我们要来探讨的是一个CPU相关的性能优化案例。

这个性能案例，是关于CPU的最后一级缓存的。你应该知道，最后一级缓存（一般也就是L3），如果命中率不高的话，对系统性能会有极坏的影响（相关基础知识建议回顾[第15讲](https://time.geekbang.org/column/article/183357)）。所以对这一问题，我们要及时准确地监测、暴露出来。

至于具体解决方案，我这里建议采取三种性能优化策略，来提高最后一级缓存的命中率。分别是：**紧凑化数据结构**、**软件预取数据**和**去除伪共享缓存**。它们分别适用于不同的情况。

## 性能问题：最后一级缓存（LLC）不命中率太高

一切问题的解决都要从性能问题开始入手，我们首先来看看**最后一级缓存不命中率太高**这个性能问题本身。

缓存的命中率，是CPU性能的一个关键性能指标。我们知道，CPU里面有好几级缓存（Cache），每一级缓存都比后面一级缓存访问速度快。最后一级缓存叫LLC（Last Level Cache）；LLC的后面就是内存。

当CPU需要访问一块数据或者指令时，它会首先查看最靠近的一级缓存（L1）；如果数据存在，那么就是缓存命中（Cache Hit），否则就是不命中（Cache Miss），需要继续查询下一级缓存。
<div><strong>精选留言（10）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/10/1c/4b/2e5df06f.jpg" width="30px"><span>三件事</span> 👍（2） 💬（1）<div>硬件指令预取是利用局部性原理 Locality。局部性原理在处理连续内存时是非常有效的，但是在实际情况下内存是不一定连续的，所以会预取到一些无效的 item，以至于会进一步导致有效缓存失效。最终造成性能问题。

有效的话，最典型的例子应该就是 loop 循环访问 data array 了吧。
无效的话，比如说两个矩阵按列相乘。

不知道这个例子对不对，感觉自己现在是刚懂了一些概念，但还做不到举一反三的地步。</div>2020-03-31</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1b/77/c0/22872965.jpg" width="30px"><span>LindaWang</span> 👍（1） 💬（2）<div>庄老师，您了解的业界有没有用AI做性能调优的工具呢？</div>2020-03-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/22/e3/510b69f9.jpg" width="30px"><span>benny</span> 👍（1） 💬（1）<div>去除伪共享缓存  这个如何发现有这样的问题呢？</div>2020-03-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1a/ec/50/fc9b338e.jpg" width="30px"><span>海华(海菜)</span> 👍（1） 💬（1）<div>采集了下我们的大数据类型机器的cache miss率，采样3台机器，10分钟均在25% ~ 30%左右，请教老师：
一个是25% ~ 30%这个值算比较高了吧？
二是都是hadoop类应用，应该从哪里着手排查问题呢？</div>2020-02-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1b/77/c0/22872965.jpg" width="30px"><span>LindaWang</span> 👍（0） 💬（1）<div>请教下，庄老师。您了解有没有流程级（函数级）Cache行为诊断机制呢？perf测的是进程级别的，粒度太大了</div>2020-07-07</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/07/8c/0d886dcc.jpg" width="30px"><span>蚂蚁内推+v</span> 👍（0） 💬（1）<div>老师您好，我有两个问题：
1.怎么判断什么时候该使用cpu? 缓存优化呢？cache的miss率达到多少就认为应该优化了？
2.CPU从内存中加载数据，会影响CPU使用率吗？比如CPU cache的miss率是10%，是不是一定比miss率是40%的cpu使用率更高？(假设都是cpu密集型的，都没有额外的io操作)。</div>2020-04-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/67/f4/9a1feb59.jpg" width="30px"><span>钱</span> 👍（0） 💬（1）<div>LLC命中率低导致的性能问题？
这个对我有些高级，基本没处理过这种问题，另外，请教一下，LLC命中率低导致的性能问题表现是怎么样的？可能刚开始不会意识到去查LLC的命中率？再者LLC的命中率多大算是OK，这个问题不同的组件标准估计也上是不同的，具体怎么判断呢？

能否认为CPU使用率较高但性能一般，可能就是LLC命中率较低造成的？</div>2020-03-05</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/39/fa/a7edbc72.jpg" width="30px"><span>安排</span> 👍（1） 💬（0）<div>原本我们想让不同线程各自访问不同的数据，也就是不让他们共享，可以并发操作。但是每个cache line长度并对齐的内存是核间共享的，对他们的访问需要原子进行，从而导致了伪共享。</div>2020-04-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/30/c1/df/d86883db.jpg" width="30px"><span>森屿时光</span> 👍（0） 💬（0）<div>作者，您好，按照您的分析，最后一级缓存的未命中数=(LLC-load-miss+LLC-store-miss)&#47;(LLC-load+LLC-store)[我也这么认为的]，但是还有一个指标LLC-miss，这个指标测出的数据又代表什么呢？
通过实验我发现：
当执行命令：perf stat -e LLC-miss,LLC-load-miss时，二者数值上相等（不知道为什么会相等）
当执行命令：perf stat -e LLC-miss,LLC-load-miss,LLC-load,LLC-store时，四者数值上均不相等，添加后两个指标后，LLC-miss 和 LLC-load-miss 就不等了【不知道为什么】
还有为什么 LLC-miss != LLC-load-miss+LLC-store-miss 【我也没看到有相关的解释】
另外，是否LLC-load-miss,LLC-store-miss就分别代表对内存的读-写次数
谢谢回复!</div>2022-10-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1a/f2/fc/3cc784be.jpg" width="30px"><span>外套</span> 👍（0） 💬（0）<div>好</div>2020-01-14</li><br/>
</ul>