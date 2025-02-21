你好，我是LMOS。

上节课，我们学习了算术指令中的加减指令和比较指令。不过一个CPU只能实现这两类指令还不够。如果你学过C语言，应该对“&lt;&lt;、&gt;&gt;、&amp;、|、!”这些运算符并不陌生，这些运算符都需要CPU提供逻辑和移位指令才可以实现。

今天我们就继续学习逻辑指令（and、or、xor）和移位指令 （sll、srl、sra）。代码你可以从[这里](https://gitee.com/lmos/Geek-time-computer-foundation/tree/master/lesson16~17)下载。话不多说，我们开始吧。

## 逻辑指令

从CPU芯片电路角度来看，其实CPU更擅长执行逻辑操作，如与、或、异或。至于为什么，你可以看看CPU的基础门电路。

RISC-V指令集中包含了三种逻辑指令，这些指令又分为立即数版本和寄存器版本，分别是andi、and、ori、or、xori、xor这六条指令。我们学习这些指令的方法和上节课类似，也涉及到写代码验证调试的部分。

### 按位与操作：andi、and指令

首先我们来学习一下andi、and指令，它们的形式如下所示：

```plain
andi rd，rs1，imm
#andi 立即数按位与指令
#rd 目标寄存器
#rs1 源寄存器1
#imm 立即数
and rd，rs1，rs2
#and 寄存器按位与指令
#rd 目标寄存器
#rs1 源寄存器1
#rs2 源寄存器2
```

上述代码中rd、rs1、rs2可以是任何通用寄存器，imm是立即数。
<div><strong>精选留言（4）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/29/a6/ad/e65aec4c.jpg" width="30px"><span>苏流郁宓</span> 👍（1） 💬（1）<div>逻辑运算有时效率高于加减乘除法，就好比十进制运算，有九九乘法表等加持，20个3直接等于60它的效率优于累计加20个3算出，但cpu的算力是软硬件共同的努力，软件方面通过优化算法结构能够直接提升效率，甚至在浮点运算中，好的算法结构能起事半功倍的效果！</div>2022-09-02</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/29/a6/ad/e65aec4c.jpg" width="30px"><span>苏流郁宓</span> 👍（1） 💬（1）<div>答案简单，RISCV寄存器一共32个的啊</div>2022-09-02</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/41/62/33520c3e.jpg" width="30px"><span>贾献华</span> 👍（1） 💬（2）<div>寄存器共 32 位。
2^5 = 32。</div>2022-09-02</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/26/e1/30/56151c95.jpg" width="30px"><span>徐大雷</span> 👍（0） 💬（0）<div>CPU更擅长计算逻辑操作  -   老师能大致讲解一下为啥么？谢谢</div>2023-12-22</li><br/>
</ul>