你好，我是 LMOS。

前面两节课，我们一起学习了虚拟机和容器的原理，这些知识属于向上延展。而这节课我们要向下深挖，看看操作系统下面的硬件层面，重点研究一下CPU的原理和它的加速套路。

有了这些知识的加持，我还会给你说说，为什么去年底发布的苹果M1芯片可以实现高性能、低功耗。你会发现，掌握了硬件的知识，很多“黑科技”就不再那么神秘了。

好，让我们正式开始今天的学习！

## CPU的原理初探

经过前面的学习，我们已经对操作系统原理建立了一定认知。从操作系统的位置来看，它除了能够向上封装，为软件调用提供API（也就是系统调用），向下又对硬件资源进行了调度和抽象。我们通常更为关注系统调用，但为了更好地设计实现一个OS，我们当然也要对硬件足够了解。

接下来，我们一起看一看硬件中最重要的一个硬件——CPU是怎么工作的。让我们拆开CPU这个黑盒子，看一看一个最小的CPU应该包含哪些部分。不同架构的CPU，具体设计还是有很大差异的。为了方便你理解，我这里保留了CPU里的共性部分，给你抽象出了CPU的最小组成架构。

![](https://static001.geekbang.org/resource/image/c2/d1/c2d0b75dffcfbdb5e72011013a6cd2d1.jpg?wh=2323x1528 "CPU架构图")  
对照上图描绘的基本模块，我们可以把CPU运行过程抽象成这样6步。

1.众所周知，CPU的指令是以二进制形式存储在存储器中的（这里把寄存器、RAM统一抽象成了存储器），所以当CPU执行指令的时候，第一步就要先从存储器中取出（fetch）指令。
<div><strong>精选留言（7）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/0f/ec/13/49e98289.jpg" width="30px"><span>neohope</span> 👍（4） 💬（1）<div>老师设计芯片太豪放了哦，输入输出位数针脚太多了。30位就十分奢侈啦：
ena，1位；clk，1位；opcode，2位
data1，8位；data2，8位；y，10位；
Icarus Verilog：http:&#47;&#47;iverilog.icarus.com&#47;home
Icarus Verilog for Windows：http:&#47;&#47;bleyer.org&#47;icarus&#47;</div>2021-08-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/52/40/e57a736e.jpg" width="30px"><span>pedro</span> 👍（6） 💬（2）<div>risc-v最近太火了，没有历史包袱，设计又足够精妙，谁能不爱呢。</div>2021-08-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/04/60/64d166b6.jpg" width="30px"><span>Fan</span> 👍（5） 💬（1）<div>哈哈哈，再来几篇Verilog。🐂🍺</div>2021-08-20</li><br/><li><img src="" width="30px"><span>springXu</span> 👍（2） 💬（1）<div>请教东哥，intel那款20年前的IA64(安腾)处理器，也是CISC的指令集么？  目前主流RISC指令集就ARM了，mips已经被市场淘汰。RISC-V是开源的指令集，被众多公司所追捧了。还有IBM的PowerPC指令集。</div>2021-08-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/ce/c6/958212b5.jpg" width="30px"><span>sugar</span> 👍（1） 💬（1）<div>所以是不是可以得出这么个结论：苹果M1的macbook之所以快，不在于他从x86切了arm有多大提升（指令集本身我一直理解为arm只是性能&#47;功耗的比值胜过x86，不计功耗只看perf还是x86有优势才对），而在于arm的开放性 赋予了苹果在硬件层面 拿arm这套架构做了大量魔改。 intel封闭性注定苹果不会拿x86这样深度魔改的。这么理解对吗？东哥</div>2022-01-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/29/a6/ad/e65aec4c.jpg" width="30px"><span>苏流郁宓</span> 👍（1） 💬（1）<div>mips？risc-v？不过，risc指令集实际实现某些功能的步骤比cisc多，苹果的cpu优秀离不开先进的工艺，假如intel的cpu也用5nm工艺，就台式机的cpu的价格估计会翻不少价，当然性能也会好到爆。问题是市场需要吗，认可吗？如同作者所言，这也是商业模式有关，不同的模式决定不同的选择？</div>2021-08-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/28/e7/52/8302bf6c.jpg" width="30px"><span>-.-</span> 👍（0） 💬（0）<div>&#47;&#47;定义alu位宽 
parameter N = 32; &#47;&#47;输入范围[-128, 127]
如果需要输入范围是[-128,127]那么位宽不应该是N=8吗？</div>2022-12-29</li><br/>
</ul>