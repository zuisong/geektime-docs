你好，我是LMOS。

在今天，Andriod+ARM已经成了移动领域的霸主，这与当年的Windows+Intel何其相似。之前我们已经在Intel的x86 CPU上实现了Cosmos，今天我会给你讲讲ARM的AArch64体系结构，带你扩展一下视野。

首先，我们来看看什么是AArch64体系，然后分析一下AArch64体系有什么特点，最后了解一下AArch64体系下运行程序的基础，包括AArch64体系下的寄存器、运行模式、异常与中断处理，以及AArch64体系的地址空间与内存模型。

话不多说，下面我们进入正题。

## 什么是AArch64体系

ARM架构在不断发展，现在它在各个领域都得到了非常广泛地应用。

自从Acorn公司于1983年开始发布第一个版本，到目前为止，有九个主要版本，版本号由1到9表示。2011年，Acorn公司发布了ARMv8版本。

ARMv8是首款支持64位指令集的ARM处理器架构，它兼容了ARMv7与之前处理器的技术基础，同样它也兼容现有的A32（ARM 32bit）指令集，还扩充了基于64bit的AArch64架构。

下面我们一起来看看ARMv8一共定义了哪几种架构，一共有三种。

1.**ARMv8-A（Application）架构**，支持基于内存管理的虚拟内存系统体系结构（VMSA），支持A64、A32和T32指令集，主打高性能，在我们的移动智能设备中广泛应用。
<div><strong>精选留言（10）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/0f/ec/13/49e98289.jpg" width="30px"><span>neohope</span> 👍（7） 💬（1）<div>非特权状态EL0：运行用户应用程序，无论安全状态还是非安全状态；
特权El1：安全状态下运行操作系统OS；非安全状态下运行虚拟机GuestOS；
特权EL2：安全状态下没有这一级别；非安全状态下运行Hypervisor，为GuestOS提供支持；
特权EL3：运行Secure monitor，管理安全状态与非安全状态的切换；
</div>2021-08-25</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/52/40/e57a736e.jpg" width="30px"><span>pedro</span> 👍（5） 💬（1）<div>2个特级权，分别是用户态和特权态，但却有7种工作模式，除了用户模式，其它均在特权态，特权态拥有全部权限，可访问一切资源。

信息量太大了，真就南孚聚能环，一节更比六节强！</div>2021-08-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/28/04/44/1fac2c1e.jpg" width="30px"><span>无凉</span> 👍（0） 💬（1）<div>通篇粗读下来学到了很多 </div>2023-04-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/2f/d7/77/0bbdc9af.jpg" width="30px"><span>VMNode</span> 👍（0） 💬（2）<div>流程图中的 开中断 关中断 最好改为 进入中断处理，结束中断处理函数</div>2022-08-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/2c/b2/58/e842dbd9.jpg" width="30px"><span>白雲城主</span> 👍（0） 💬（1）<div>用户态EL0 只能切换到EL1 内核态，其通过调用svc 指令实现，调用后的寄存器变化如下
1. 将当前EL0等级的PC 指针存储在 ELR_EL1寄存器中，硬件自动完成.
2. 将当前EL0等级的PSATE 赋值给 SPSR_EL1 寄存器，硬件自动完成.
3. 根据当前处理器的状态将PSTATE 值更新，硬件自动完成.
4. 根据SPSEL 寄存器选择使用的栈指针 0: 使用SP_EL0  1: 使用SP_EL1 .

Exception Handler 执行完后需要软件上主动调用 ERET  指令来返回，执行后寄存器变化如下
1. 自动将 ELR_EL1 寄存器值加载到PC，硬件自动完成
2. 自动将SPSR_EL1 寄存器值加载到PSTATE，硬件自动完成</div>2022-03-04</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/29/a6/ad/e65aec4c.jpg" width="30px"><span>苏流郁宓</span> 👍（0） 💬（1）<div>知识量过大，二刷课程还是有很多看不懂（不是本节，不能理解透）的啊！
有个不懂的问题，既然cpu用到分支预测，那么优化指令集是不是也会对预测有帮助呀？（不只是cisc与Risc对比，不同的risc指令集也可以比的），俺认为是可以的！</div>2022-02-04</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/29/a6/ad/e65aec4c.jpg" width="30px"><span>苏流郁宓</span> 👍（0） 💬（1）<div>有了 MMU 硬件转换机制，操作系统只需要控制页表就能控制内存的映射和隔离了。
可以理解成ARM处理器对内存利用权限的限制更严格，非特定的特权模式，仅在系统模式下，运行在ARm上的系统不能直接修改内存地址，从而进行内存保护。而是通过mmu页表的变动来影响内存数据（内存地址）的变动吗？</div>2021-08-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/29/a6/ad/e65aec4c.jpg" width="30px"><span>苏流郁宓</span> 👍（0） 💬（1）<div>3个特权级，6个特权模式？</div>2021-08-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1b/2c/3d/0bd58aa4.jpg" width="30px"><span>Em</span> 👍（0） 💬（0）<div>check in</div>2024-10-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/a6/f0/50d0931d.jpg" width="30px"><span>木易杨</span> 👍（0） 💬（0）<div>arm的指令集没有实模式，保护模式这个说法吧</div>2023-12-12</li><br/>
</ul>