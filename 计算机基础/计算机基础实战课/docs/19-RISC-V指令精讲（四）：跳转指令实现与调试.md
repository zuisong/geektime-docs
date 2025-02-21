你好，我是LMOS。

前面我们学习了无条件跳转指令，但是在一些代码实现里，我们必须根据条件的判断状态进行跳转。比如高级语言中的if-else 语句，这是一个典型程序流程控制语句，它能根据条件状态执行不同的代码。这种语句落到指令集层，就需要有根据条件状态进行跳转的指令来支持，这类指令我们称为有条件跳转指令。

这节课，我们就来学习这些有条件跳转指令。在RISC-V指令集中，一共有6条有条件跳转指令，分别是beq、bne、blt、bltu、bge、bgeu。

这节课的配套代码，你可以从[这里](https://gitee.com/lmos/Geek-time-computer-foundation/tree/master/lesson18~19)下载。

## 比较数据是否相等：beq和bne指令

我们首先来看看条件相等跳转和条件不等跳转指令，即beq指令和bne指令，它们的汇编代码书写形式如下所示：

```plain
beq rs1，rs2，imm
#beq 条件相等跳转指令
#rs1 源寄存器1
#rs2 源寄存器2
#imm 立即数
bne rs1，rs2，imm
#bne 条件不等跳转指令
#rs1 源寄存器1
#rs2 源寄存器2
#imm 立即数
```

上述代码中，rs1、rs2可以是任何通用寄存器，imm是立即数（也可称为偏移量），占用13位二进制编码。请注意，**beq指令和bne指令没有目标寄存器，就不会回写结果。**

我们用伪代码描述一下beq指令和bne指令完成的操作。
<div><strong>精选留言（5）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/2c/c7/89/16437396.jpg" width="30px"><span>极客酱酱</span> 👍（2） 💬（1）<div>终于了解了高级语言是怎么实现函数返回和调用的了</div>2022-09-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/29/a6/ad/e65aec4c.jpg" width="30px"><span>苏流郁宓</span> 👍（1） 💬（1）<div>俺更好奇，RIScv基本指令中怎么实现接口的功能（比如不同厂家在基本指令上扩展，为了实现不同riscv+指令，能够实现互联互通，需要基本指令怎么实现接口功能，避免碎片化（不同指令集互通不了））</div>2022-09-07</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/29/a6/ad/e65aec4c.jpg" width="30px"><span>苏流郁宓</span> 👍（1） 💬（1）<div>答：不需要再增加多余比较指令，上面的跳转指令混合使用就能实现相同的功能的，riscv类似软件功能的模块化设计，不需要搞那么多比较指令的，只要无符号比较和有符号比较上基本扩展就行的 啊</div>2022-09-07</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/PiaDmjdWicz1PM4F6XCjQwoTwZueqFyjoF9ATPFBvhoxwsuW4v55ppg38iao2pMMgpPIH7svWa3WfvxGsiaiaRE4SCw/132" width="30px"><span>Geek_5ed498</span> 👍（0） 💬（0）<div>这节课程的标题是不是应当修改为“跳转指令的应用与调试”更合适一些</div>2023-12-01</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/f7/f8/3c0a6854.jpg" width="30px"><span>xavier</span> 👍（0） 💬（0）<div>小于等于可以使用 小于和相等跳转指令组合，那就需要多一条判断指令。比如这样一条语句： a ≤ 3，那么写成 a &lt; 4, 就少了相等判断，执行效率更高。</div>2023-06-28</li><br/>
</ul>