你好，我是LMOS。

在之前的学习中，我们了解到了很多计算机基础相关的知识，也学过了iostat等观察系统运行状态的命令。但在我们的实际工程中，排查分析一些具体的性能优化问题或者定位一些故障时，可能需要在不同的命令间来回切换、反复排查。

那么有没有一款工具可以贯穿操作系统的各个模块，帮我们准确分析运行的程序、系统的运行细节呢？当然有，答案就是eBPF。

## 从BPF到eBPF

eBPF是怎么来的，还要从1992年说起。当年伯克利实验室的Steven McCanne和Van Jacobso为了解决高性能的抓包、分析网络数据包的问题，在BSD操作系统上设计出了一种叫做伯克利数据包过滤器（BSD Packet Filter）的机制，并发表了《The BSD Packet Filter:A New Architecture for User-level Packet Capture》这篇论文（论文链接在[这里](https://www.tcpdump.org/papers/bpf-usenix93.pdf)）。

为了让内核态能够高效率地处理数据包，这套机制引入了一套只有2个32位寄存器、16个内存位和32个指令集的轻量级虚拟机，包过滤技术的性能因此提升了20多倍。

因为这套方案设计的太好用了，后来在1997年的时候，Linux操作系统从Linux2.1.75版本开始，就把BPF合并到了内核中了。
<div><strong>精选留言（5）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/19/ae/c3/d930693b.jpg" width="30px"><span>LockedX</span> 👍（2） 💬（2）<div>eBPF有访问内核的权限，如果被误用，后果不堪设想，所以要谨慎合理的使用eBPF。</div>2022-11-07</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1d/80/93/dde3d5f0.jpg" width="30px"><span>熊悟空的凶</span> 👍（1） 💬（1）<div>eBPF 对系统有侵入性吗，是类似于Agent技术么</div>2022-11-07</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/M3iaJULcXSjCNya7UibVzgF0fq1H2fobO1ic7ibDzfGbic6DR6CbkUnfJo8ibbPjQRMHRbE1L8c2bTh2PhiczpE5SbPibw/132" width="30px"><span>童谣</span> 👍（0） 💬（1）<div>这个怎么用？比如我要做一些性能分析，类似io、cpu突刺较高，ebpf有帮助吗？</div>2023-11-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/29/a6/ad/e65aec4c.jpg" width="30px"><span>苏流郁宓</span> 👍（0） 💬（1）<div>eBPF通过安全认证等尽可能排除无用的干扰，但问题是也增加了复杂度。
也就是eBPF应该在关键时候用，而不是频繁的滥用。滥用容易增加系统的复杂度！技术是中性的，有时解决一个问题也容易增加新的问题！越复杂就越容易出错，普通电脑大不了关机重启，但是对数据库电脑，应该是能减则减。性能和稳定兼顾（就比如双11数据库电脑哪怕停几分钟就是大损失）</div>2022-11-07</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/25/87/f3a69d1b.jpg" width="30px"><span>peter</span> 👍（0） 💬（1）<div>请教老师两个问题：
Q1：BPF比协议栈还优先获取数据报吗？
文中有“当数据报文从设备驱动上传输过来之后，首先会被分流到 BPF”，从这句话看，数据先到
BPF，然后到协议栈，是这样吗？（我感觉应该是先到协议栈，协议栈优先级最高）

Q2：协议栈会不处理数据吗？
文中有“如果某些设备驱动发过来的数据, 找不到对应的 BPF 处理逻辑的话，则会由正常的协议栈来处理。”，
从这句话看，如果BPF处理，则协议栈就不处理，是这样吗？（我的理解是：协议栈肯定要处理，BPF是
辅助处理的</div>2022-11-07</li><br/>
</ul>