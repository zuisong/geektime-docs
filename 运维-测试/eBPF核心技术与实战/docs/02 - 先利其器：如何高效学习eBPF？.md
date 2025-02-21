你好，我是倪朋飞。

上一讲，我们一起了解了 eBPF 的发展历程、基本原理和主要应用场景。eBPF 来源于 Linux 内核子系统 Berkeley Packet Filter (BPF)，最早用于提升网络包过滤的性能。后来，随着 BPF 技术的逐步完善，它的应用范围从内核空间扩展到了用户空间，并逐步在网络、可观测以及安全等方面获得了大量的应用。

了解过这些的你，很可能遇到了我曾经有过的疑惑：作为 Linux 内核的一部分，eBPF 这么底层的技术，到底该如何学习才能更高效地掌握它？

这是初学者经常遇到的问题：在学习 eBPF 的知识和原理时，找不到正确的方法，只是照着网络上并不全面的片段文章操作，或者直接去啃内核的源码，这样往往事倍功半。甚至，还可能被海量的信息淹没，失去了持续学习的信心，“从入门到放弃” 。那么今天，我们就一起来看看，怎么才能高效且深入地学习 eBPF。

## 学习这门课需要什么基础？

首先，在学习 eBPF 之前你要明白，eBPF 是 Linux 的一部分，它所有的应用都需要在 Linux 系统中完成（虽然 Windows 也已经支持了 eBPF，但暂时不够成熟）。所以，我希望你**至少熟练掌握一种 Linux 系统（比如 Ubuntu、RHEL）的基本使用方法**，包括：
<div><strong>精选留言（5）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/0f/5e/96/a03175bc.jpg" width="30px"><span>莫名</span> 👍（36） 💬（11）<div>曾基于 BPF 做过一个容器平台的链路追踪系统，分解出单个请求在服务端经过的节点、网络设备、耗时等信息，便于快速定位网络抖动时主要延迟的具体发生点。

遇到最多的是内核版本差异引起的各类编译问题，要么跑不起来，要么运行结果不符合预期。尤其 4.9 内核问题很多，5.x 版本的内核自己在测试环境用一用还行，线上的内核版本相对会保守，几年前 3.10  的占比很高。不过好消息是，新机器的内核一般都直接使用 4.x，甚至 5.x。BPF 落地生产环境的环境阻力小了很多。

如果公司的环境暂时还不能应用 BPF 技术，不妨碍先进行知识储备，自己先玩起来，等到真正被需要的时候就可以发挥作用了。</div>2022-01-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/e7/8b/7baca523.jpg" width="30px"><span>吃苹果的考拉</span> 👍（13） 💬（5）<div>从倪老师的linux性能篇，了解到了ebpf，就买了《bpf之巅》自学了一阵，现在居然倪老师也出了ebpf的课程，果断入手，希望认识能更上一个台阶</div>2022-01-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/43/32/3eeac151.jpg" width="30px"><span>ranger</span> 👍（7） 💬（1）<div>正在接触混沌工程和其中一款开源产品chaos-mesh，一个基于bpf实现的内核故障注入的模块bpfki</div>2022-01-30</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/23/52/66/3e4d4846.jpg" width="30px"><span>includestdio.h</span> 👍（2） 💬（2）<div>第一次接触bpf是通过老师的 linux性能优化专栏，然后看到老师有推荐性能之巅这本书，果断入手并断断续续看完了，目前实际工作中还没有接触过ebpf，因此也无从入手，希望通过专栏能收获更多</div>2022-01-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/27/f6/78/84513df0.jpg" width="30px"><span>秋名山犬神</span> 👍（1） 💬（2）<div>想知道下k8s中的哪些功能是老师贡献的</div>2022-01-24</li><br/>
</ul>