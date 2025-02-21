你好，我是LMOS。

通过前面的学习，我们已经了解了在C语言编译器的“视角”下，C语言的各种表达式是如何转换成各种机器汇编指令的。从这节课开始，我会带你进一步深入学习各种汇编指令的细节。

只要你耐心跟我学完这节课，对RISC-V的各种指令，你就能了如指掌了。这里我们将从RV32I的算术指令开始，先学习加减指令（add、sub），接着了解一下数值比较指令（slt）。这些指令都有两个版本，一个是立即数版本，一个是寄存器的版本。话不多说，我们开始吧。

课程配套代码从[这里](https://gitee.com/lmos/Geek-time-computer-foundation/tree/master/lesson16~17)下载。

## 加减指令

上小学时我们都学过四则运算，最基础的是加减法，即一个数加上或者减去一个数，对应到CPU中就是一条加法指令和一条减法指令。

一个CPU要执行基本的数据处理计算，加减指令是少不了的，否则基础的数学计算和内存寻址操作都完成不了，用这样的CPU做出来的计算机将毫无用处。

不过想让CPU实现加减法，我们需要用到它能“理解”的语言格式，这样才能顺畅交流。所以，在研究指令之前，我们先来看看RISC-V指令的格式。

### RISC-V指令的格式

RISC-V机器指令是一种三操作数指令，其对应的汇编语句格式如下：

```plain
指令助记符 目标寄存器，源操作数1，源操作数2
```
<div><strong>精选留言（6）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/2b/d4/4b/ec621442.jpg" width="30px"><span>范廷东</span> 👍（0） 💬（1）<div>用手机看不清文章中的图片</div>2023-08-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/ee/31/8a5cd41d.jpg" width="30px"><span>James Deng</span> 👍（0） 💬（1）<div>想问一下，浮点及不同数据类型转换，也是有对应的指令吧</div>2022-09-15</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/19/ae/c3/d930693b.jpg" width="30px"><span>LockedX</span> 👍（0） 💬（1）<div>0x00000033解析为0000 0000 0011 0011
由操作码011 0011和功能码都是0推出指令add(寄存器加法)
再由第5课查表得知0表示寄存是zero，所以指令是add zero,zero,zero
这个就是所谓的占位指令啦</div>2022-09-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/25/87/f3a69d1b.jpg" width="30px"><span>peter</span> 👍（0） 💬（1）<div>请教老师几个问题：
Q1：立即数最小只能是-2048，如果要减去更大的数，怎么办？
同理，如果要加上比2048大的数，怎么办？
Q2：功能位有什么用？addi指令的功能位是3位，都是0，好像没有区别。
Q3：jr ra，这里的 ra 表示什么？</div>2022-09-01</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/29/a6/ad/e65aec4c.jpg" width="30px"><span>苏流郁宓</span> 👍（0） 💬（1）<div>操作符add，……，a1？中间的00不懂指向那个寄存器的啊</div>2022-08-31</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/Q3auHgzwzM7mF1Zdh16zKFDsIjV6movCe1vArG6icbr9Bd537NDg7dA6y24LhdC3ypvzqJBW18oGcDeC2yTwDsw/132" width="30px"><span>肖水平</span> 👍（0） 💬（1）<div>汇编语言中.globl是什么意思？为什么addi_ins没有加它？</div>2022-08-31</li><br/>
</ul>