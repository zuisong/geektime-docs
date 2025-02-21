你好，我是宫文学。

经过了上一节课的学习，你已经对物理机的运行期机制有了一定的了解。其中最重要的知识点就是，为了让一个程序运行起来，硬件架构、操作系统和计算机语言分别起到了什么作用？对这些知识的深入理解，是让你进入高手行列的关键。

接下来，就让我们把程序编译成汇编代码，从而生成在物理机上运行的可执行程序吧！

慢着，不要太着急。为了让你打下更好的基础，我决定再拿出一节课来，带你了解一下CPU架构和指令集，特别是ARM和X86这两种使用最广泛的CPU架构，为你学习汇编语言打下良好的基础。

首先，我们讨论一下什么是CPU架构，以及它对学习汇编语言的作用。

## 掌握汇编语言的关键，是了解CPU架构

提到汇编语言，很多同学都会觉得很高深、很难学。其实这是个误解，汇编语言并不难掌握。

为什么这么说呢？其实前面在实现虚拟机的时候，我们已经接触了栈机的字节码。你觉得它难吗？JVM的字节码理论上不会超过128条，而我们通过前面几节课已经了解了其中的好几十条指令，并且已经让他们顺利地运转起来了。

而且，汇编代码作为物理机的指令，也不可能有多么复杂。因为CPU的设计，就是要去快速地执行一条条简单的指令，所以这些指令不可能像高级语言那样充满复杂的语义。
<div><strong>精选留言（4）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/12/21/7e/fb725950.jpg" width="30px"><span>罗 乾 林</span> 👍（4） 💬（1）<div>Linux: cat &#47;proc&#47;cpuinfo
Windows:https:&#47;&#47;docs.microsoft.com&#47;en-us&#47;sysinternals&#47;downloads&#47;coreinfo
手上的ARM开发板Features：
fp asimd evtstrm aes pmull sha1 sha2 crc32

fp：浮点运算指令集
asimd：单指令流多数据流,处理RGB，YUV，即小碎数据的并行操作，armv7上有个NEON指令完成功能差不多
aes、sha1、sha2：看上去像是跟加密相关的指令集

其他几个就不太清楚了</div>2021-09-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/23/7f/24/ceab0e7b.jpg" width="30px"><span>奋斗的蜗牛</span> 👍（2） 💬（1）<div>汇编一直是弱项，看来还是要多学</div>2021-09-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/19/70/67/0c1359c2.jpg" width="30px"><span>qinsi</span> 👍（0） 💬（1）<div>A64更接近x86_64。相比之下A32更有趣一些，比如每条指令都自带4bit标志位来实现条件执行；又比如指令中的立即数只有12bit，却能用来表示一些32bit的整数。</div>2021-09-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/26/eb/d7/90391376.jpg" width="30px"><span>ifelse</span> 👍（0） 💬（0）<div>学习打卡</div>2022-09-16</li><br/>
</ul>