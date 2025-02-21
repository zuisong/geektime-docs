你好，我是程远。

今天是我们专题加餐的最后一讲，明天就是春节了，我想给还在学习的你点个赞。这里我先给你拜个早年，祝愿你牛年工作顺利，健康如意！

上一讲，我们学习了eBPF的基本概念，以及eBPF编程的一个基本模型。在理解了这些概念之后，从理论上来说，你就能自己写出eBPF的程序，对Linux系统上的一些问题做跟踪和调试了。

不过，从上一讲的例子里估计你也发现了，eBPF的程序从编译到运行还是有些复杂。

为了方便我们用eBPF的程序跟踪和调试系统，社区有很多eBPF的前端工具。在这些前端工具中，BCC提供了最完整的工具集，以及用于eBPF工具开发的Python/Lua/C++的接口。那么今天我们就一起来看看，怎么使用BCC这个eBPF的前端工具。

## 如何使用BCC工具

[BCC](https://github.com/iovisor/bcc)（BPF Compiler Collection）这个社区项目开始于2015年，差不多在内核中支持了eBPF的特性之后，BCC这个项目就开始了。

BCC的目标就是提供一个工具链，用于编写、编译还有内核加载eBPF程序，同时BCC也提供了大量的eBPF的工具程序，这些程序能够帮我们做Linux的性能分析和跟踪调试。

这里我们可以先尝试用几个BCC的工具，通过实际操作来了解一下BCC。
<div><strong>精选留言（7）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/0f/5e/96/a03175bc.jpg" width="30px"><span>莫名</span> 👍（9） 💬（1）<div>老师提到过一个比较好用的网络包追踪工具：https:&#47;&#47;github.com&#47;yadutaf&#47;tracepkt。

不过这个是基于 BCC 编写的，阅读起来有些晦涩。假期抽空编写了一个简单的 bpftrace 版本（修复了 network ns 为 0、interface 为空的问题，不过没有根据 pid 过滤），供大家参考下：https:&#47;&#47;github.com&#47;xingfeng2510&#47;mybpf&#47;blob&#47;main&#47;tracepkt.bt

bpftrace 作为更高级的 eBPF 语言，写起来简单很多，而且容易看懂。</div>2021-02-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/4f/7d/dd852b04.jpg" width="30px"><span>chon</span> 👍（5） 💬（1）<div>看完了，谢谢老师，收获很多，后面还要刷2次并动手实验才能掌握好。</div>2021-02-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/c4/03/f753fda7.jpg" width="30px"><span>JianXu</span> 👍（3） 💬（0）<div>不禁想起以前志腾说 很多事情都是从论文开始的，一篇论文然后演化出一门技术，接着围绕这门技术演化出一个产品，逐步演化出一家公司。我总觉得这背后有一些规律，只是自己还没有掌握这门规律。</div>2022-08-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/2c/45/44/8df79d3c.jpg" width="30px"><span>事已至此开始撤退</span> 👍（2） 💬（0）<div>为什么没有评分呀，这门课，满分无疑了，全部干货，没有虚的东西。</div>2023-03-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/64/05/6989dce6.jpg" width="30px"><span>我来也</span> 👍（1） 💬（0）<div>祝老师新年快乐！</div>2021-02-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/0f/70/cdef7a3d.jpg" width="30px"><span>Joe Black</span> 👍（1） 💬（0）<div>春节快乐！学完课程后，感觉终究还是有必要认认真真看看内核的数据，还是需要系统化的学习下。</div>2021-02-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/46/3f/7825378a.jpg" width="30px"><span>无名氏</span> 👍（1） 💬（0）<div>春节快乐</div>2021-02-10</li><br/>
</ul>