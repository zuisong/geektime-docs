你好，我是LMOS。

上一节课，我们完成了CPU流水线的指令译码模块设计。我们一起探讨了RISC-V指令是如何翻译的，还学会了提取不同类型指令中的信息。最后根据流水线的需要，我们设计出了译码控制模块和数据通路模块。

接下来，我们利用译码后的这些信息继续设计流水线的下一级——执行单元。指令执行算是CPU流水线中最复杂的一个阶段了，不过别担心，经过前面课程的准备，我们一定可以搞定它。

## CPU的执行概述

回顾前面我们已经设计完成的CPU流水线步骤：

1.取指模块根据程序计数器（PC）寻址到指令所在的存储单元，并从中取出指令。  
2.译码模块对取出的指令进行翻译，得到功能码、立即数、寄存器索引等字段，然后根据某些字段读取一个或两个通用寄存器的值。

经过流水线的这两个步骤之后，下一步就需要把这些指令信息发送给执行单元去执行相关操作。根据译码之后的指令信息，我们可以把指令分为三类，分别是算术逻辑指令、分支跳转指令、存储器访问指令。

[上节课](https://time.geekbang.org/column/article/548002)我们已经详细解读了RISC-V指令集的指令格式，正是因为格式上比较简单而且规整，所以不同类别的指令执行过程也是类似的。这样，RISC执行单元的电路结构相比CISC就得到了简化。

所以在指令执行阶段，上述的这三类指令都能通过ALU进行相关操作。比如，存储访问指令用ALU进行地址计算，条件分支跳转指令用ALU进行条件比较，算术逻辑指令用ALU进行逻辑运算。
<div><strong>精选留言（7）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/1b/6b/2c/b27eefc5.jpg" width="30px"><span>Abcd</span> 👍（3） 💬（1）<div>左移运算复用右移运算的电路，也体现了RISC－V精简的哲学：能够用基本的组合出来，就不创造新的电路</div>2022-08-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/25/87/f3a69d1b.jpg" width="30px"><span>peter</span> 👍（1） 💬（2）<div>请教老师几个问题：
Q1：[31:0]，什么意思？
input  [31:0] regWData,   是说regWData占31位，每一位是0吗？
Q2：reg [31:0] regs[31:0];： 这条语句什么意思？
Q3：regs[ii] &lt;= 32&#39;b0;   是把32&#39;b0写到regs[ii]吗？
32&#39;b0;，是说有32位，每一位是0吗？</div>2022-08-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/27/f4/48/2242bed9.jpg" width="30px"><span>吴建平</span> 👍（1） 💬（3）<div>“如果它们的最高位不相等，则根据 ALU 运算控制码 aluOp 的最低位判断。如果 aluOp 最低位为“1”，表示是无符号数比较，直接取操作数 2 的最高位作为比较结果。如果 aluOp 最低位为“0”，表示是有符号数比较，直接取操作数 1 的最高位作为比较结果。”
这句话什么意思，比如，为什么无符号数比较，直接取操作数2的最高位为比较结果，这个最高位和大小没关系吧</div>2022-08-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/2e/d1/f0/0eafdb8e.jpg" width="30px"><span>😇</span> 👍（0） 💬（1）<div>always @(posedge clk or posedge reset) begin if(reset) begin for(ii=0; ii&lt;32; ii=ii+1) regs[ii] &lt;= 32&#39;b0; end else if(wen &amp; (|regWAddr)) regs[regWAddr] &lt;= regWData; end
请问这里为什么|regWAddr，没太看懂</div>2022-08-27</li><br/><li><img src="" width="30px"><span>+1</span> 👍（0） 💬（1）<div>还是没懂$signed() 函数将符号位扩位后的作用是什么</div>2022-08-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/2f/85/d1/bfe4d1b2.jpg" width="30px"><span>小博(微信/手机号1849登录)</span> 👍（0） 💬（1）<div>itype我咋没找到在哪里</div>2022-08-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/29/a6/ad/e65aec4c.jpg" width="30px"><span>苏流郁宓</span> 👍（0） 💬（2）<div>在 ALU 模块代码中，为什么要把左移操作转换为右移进行处理？
这和cpu小端模式有关？</div>2022-08-12</li><br/>
</ul>