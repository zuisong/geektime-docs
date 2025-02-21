你好，我是庄振运。

从这一讲开始，我们探讨分析几个最容易发生性能问题的领域：CPU、内存、存储和网络。

这一讲先来讨论关于CPU的常见性能问题。首先我们从硬件的角度，来看看CPU的性能取决于哪些因素，然后分析一下CPU的内部结构。接着我们探讨和CPU性能相关的软件系统，看看CPU运行时侯的调度和切换。

## CPU的性能决定因素

宏观来讲，一台服务器里面的CPU性能取决于好几个因素，包括有多少处理器、多少个核、时钟主频是多少、有没有Turbo模式、处理器内部的运算架构以及和CPU紧密交互的其他部件的性能。

CPU的更新换代很频繁，基本上每两年就会更新一代。比如Intel的CPU，最近10年已经经历了5代左右。每一代都有主频的变化，而且有好几个变种。

下面的表格描述了从十年前（也就是2009年）的SandyBridge，到后来的IvyBridge、Haswell、Broadwell，直到Skylake。注意，对后面的三代，我分别列出了其中的两种变化——单处理器（1P）和双处理器（2P）。

![](https://static001.geekbang.org/resource/image/0c/09/0ccfee296bbd3ab792b41ee0feb26209.png?wh=1290%2A280)

大体上我们可以看出，虽然CPU更新换代，但是处理器的时钟主频基本不再提高，甚至变得更低了。这样的目的是降低CPU的功耗。比如SandyBridge的时钟频率是2.6GHz，但是到了Skylake，反而降低到了2GHz。
<div><strong>精选留言（12）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/11/9b/ba/333b59e5.jpg" width="30px"><span>Linuxer</span> 👍（6） 💬（1）<div>请问老师后续有与实验结合的讲解吗？我觉得大多数人都知道概念和监测的方法，但是都不知道如何分析出具体的深层次的原因？比如NUMA里面跨节点内存访问对性能到底有多大影响呢？比如流水线停顿对性能的影响又是如何表现的等等</div>2019-12-30</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/03/41/ba59e1ee.jpg" width="30px"><span>Ethan</span> 👍（4） 💬（1）<div>概念清楚了，需要实战才好</div>2020-01-01</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/0c/ad/d1ab1995.jpg" width="30px"><span>Di Yu</span> 👍（4） 💬（3）<div>请问老师，用什么工具才能测出来CPU几个核负载不均衡呢？</div>2019-12-30</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/67/f4/9a1feb59.jpg" width="30px"><span>钱</span> 👍（2） 💬（1）<div>站在程序员的角度，如何让CPU的运行不受阻碍哪？</div>2020-03-04</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/f7/b1/982ea185.jpg" width="30px"><span>美妙的代码</span> 👍（0） 💬（1）<div>老师。cpu 指令是存在哪儿的？ 还是说程序代码，经过翻译后就会变成 cpu 指令？</div>2020-04-01</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/58/78/fe19274b.jpg" width="30px"><span>睡在床板下</span> 👍（0） 💬（1）<div>老师问一个问题，有一个c++四个线程程序都执行while死循环，任务管理器查看时cpu显示25%，说明是4核处理器某一个核100%了吗？ 一个进程默认是不能跨处理器吗？</div>2020-02-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/6e/55/8c2c83f4.jpg" width="30px"><span>Wang</span> 👍（0） 💬（1）<div>CPU利用率在72%，负载却到了8以上，四核CPU，请问这种情况正常吗？是不是需要深入研究CPU空闲原因？
非常感谢！</div>2020-01-05</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/4b/46/717d5cb9.jpg" width="30px"><span>惜心（伟祺）</span> 👍（1） 💬（0）<div>西瓜哥的《大话计算机》里面对硬件介绍比较清晰</div>2020-12-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1d/9a/89/babe8b52.jpg" width="30px"><span>A君</span> 👍（0） 💬（0）<div>衡量处理器性能🉐指标是每秒指令数，这和gpu的每秒浮点运算数类似。MIPS＝ipc*clk。计算时间长，可能是多处理器、多核负债不均衡导致的，这可能跟线程调度有关，单核的性能只能是提高代码质量。</div>2021-03-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/2b/fa/1cde88d4.jpg" width="30px"><span>大俊stan</span> 👍（0） 💬（0）<div>把这篇文章看下来，只能佩服老师的总结能力。老师这篇文章中的很多概念大家可以结合LInux性能优化实战以及深入操作系统组成原理一起学习。很多小的概念点另外两门课程都有讲到。感兴趣的同学可以看看去。</div>2020-11-01</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/50/20/47729092.jpg" width="30px"><span>谢煜锋</span> 👍（0） 💬（0）<div>如果能结合具体case来分析，就比较好。我们在实际业务中对于计算型密集型程序设置超频，确实带来了意想不到的收益。老师讲的这种，使用场景也能举几个例子就比较好</div>2020-10-09</li><br/><li><img src="" width="30px"><span>Scott</span> 👍（0） 💬（3）<div>我遇到过一个sys cpu高的问题，现象就是sys cpu至少10%，一重启就好了，最后发现是cgroup泄漏的问题，这个问题排查过程真是非常艰难。</div>2019-12-30</li><br/>
</ul>