你好，我是LMOS。

上节课，我们了解了什么是CPU的流水线，并决定采用经典的五级流水线来设计我们的MiniCPU，之后梳理了我们将要设计的MiniCPU架构长什么样，最后完成了流水线的第一步——取指。

取指阶段把存储器里的指令读出以后，就会传递给后续的译码模块进行处理。那之后指令是如何译码的呢？这就要说到流水线的第二步——译码（代码从[这里](https://gitee.com/lmos/Geek-time-computer-foundation)下载）。

## 指令是如何翻译的？

[第五节课](https://time.geekbang.org/column/article/546957)我们已经讲过了RISC-V指令架构，明确了我们的MiniCPU选用的是RV32I指令集。其中每条指令都是32位，且分为6种指令格式，不同格式的指令中包含了不一样的指令信息。

![](https://static001.geekbang.org/resource/image/7b/c8/7b035797137a9e42cc1f6544d6d4dac8.jpg?wh=4005x2200)

如上图所示的6种指令格式，其中R型指令包含了操作码opcode、目标寄存器索引rd、功能码funct3和funct7以及源寄存器索引rs1和rs2。而I型指令则是包含操作码opcode、目标寄存器索引rd、功能码funct3、源寄存器索引rs1以及立即数imm。

与此类似，后面的S型指令、B型指令、U型指令和J型指令也有特定的操作码、功能码、源寄存器索引、目标寄存器索引和立即数。

不过指令格式不同，指令译码模块翻译指令的工作机制却是统一的。首先译码电路会翻译出指令中携带的寄存器索引、立即数大小等执行信息。接着，在解决数据可能存在的数据冒险（这个概念后面第九节课会讲）之后，由译码数据通路负责把译码后的指令信息，发送给对应的执行单元去执行。
<div><strong>精选留言（11）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/27/f8/2c/92969c48.jpg" width="30px"><span>青玉白露</span> 👍（12） 💬（1）<div>我觉得之所以将立即数设置为不连续，主要还是为了让rs1 rs2 rd 寄存器的位置保持固定，从而提高指令流水线的效率。至于不连续的立即数，只要在译码的时候拼接就可以了。</div>2022-08-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/2e/d6/9f/4894fbc4.jpg" width="30px"><span>阿狸狸狸狸，</span> 👍（1） 💬（1）<div>我想请问一下，id_ex_ctrl这个译码控制模块的输入信号从哪里来？输出信号又送去哪里？</div>2022-10-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/27/ac/bf/f549183e.jpg" width="30px"><span>=</span> 👍（1） 💬（2）<div>localparam DEC_JALR    = {1&#39;b0,  2&#39;b11, 1&#39;b0,    1&#39;b0,     1&#39;b1,     1&#39;b0,  2&#39;b10,     1&#39;b1,   1&#39;b0,  7&#39;b0100000, 2&#39;b00,     1&#39;b1};
请问这里的7&#39;b0100000不应该是7&#39;b0000010吗</div>2022-08-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/29/a6/ad/e65aec4c.jpg" width="30px"><span>苏流郁宓</span> 👍（1） 💬（1）<div>B型是有条件跳转指令，J型是无条件跳转指令。俺的理解是既然是跳转指令，允许不连续的
S型是和内存交流，俺的理解是可以为指令，也可以部分为数据，没有严格的要求导致可以允许不连续的！</div>2022-08-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/27/eb/bf/8acfeaa6.jpg" width="30px"><span>小傅</span> 👍（0） 💬（1）<div>decode signals这段代码是怎么得出来的</div>2022-11-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/2f/85/d1/bfe4d1b2.jpg" width="30px"><span>小博(微信/手机号1849登录)</span> 👍（0） 💬（3）<div>还是有一个地方没看懂，那个立即数的拼接规则是什么呀？</div>2022-08-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/a6/f0/50d0931d.jpg" width="30px"><span>木易杨</span> 👍（0） 💬（1）<div>老师，这个写的代码有上传到git上嘛？</div>2022-08-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/19/ae/c3/d930693b.jpg" width="30px"><span>LockedX</span> 👍（0） 💬（3）<div>wire [31:0] Iimm = {{21{instr[31]}}, instr[30:20]};
wire [31:0] Simm = {{21{instr[31]}}, instr[30:25], instr[11:7]};
wire [31:0] Bimm = {{20{instr[31]}}, instr[7], instr[30:25], instr[11:8], 1&#39;b0};
wire [31:0] Uimm = {instr[31:12], 12&#39;b0};
wire [31:0] Jimm = {{12{instr[31]}}, instr[19:12], instr[20], instr[30:21], 1&#39;b0};  

老师，这个立即数的截取一直没看懂，{21{instr[31]}}的含义是什么呢</div>2022-08-16</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/2f/89/38/441bb99b.jpg" width="30px"><span>你要有个信念</span> 👍（0） 💬（2）<div>请问为什么要把立即数扩成32位的呢？</div>2022-08-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1b/9c/ac/4a488a4e.jpg" width="30px"><span>伊宝峰</span> 👍（0） 💬（1）<div>立即数不连续是为了让不同指令源和目的寄存器位置固定，方便寄存器地址的译码。</div>2022-08-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1d/9a/89/babe8b52.jpg" width="30px"><span>A君</span> 👍（0） 💬（0）<div>提取立即数的那段代码为什么是所有类型的立即数的集合？为什么不像前面那样根据opcode走不通分支来赋值?</div>2023-11-27</li><br/>
</ul>