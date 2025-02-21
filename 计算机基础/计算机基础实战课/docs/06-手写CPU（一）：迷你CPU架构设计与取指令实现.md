你好，我是LMOS。

经过上一节课的学习，我们已经知道了一个基于RISC-V指令集设计的CPU，必须要实现哪些指令。从这节课开始，我们就可以着手设计和实现MiniCPU了。

我会先跟你讲讲什么是流水线，在CPU中使用流水线的好处是什么？然后，我们再以经典的五级流水线为例，讲解CPU流水线的五个阶段。接着设计出我们MiniCPU的总体结构，并根据规划的五级流水线，完成流水线的第一步——取指模块的设计。课程的配套代码可以从[这里](https://gitee.com/lmos/Geek-time-computer-foundation.git)下载。

话不多说，让我们正式开始今天的学习吧。

## 什么是CPU流水线？

说到流水线，你是否会马上想到我们打工人的工厂流水线？没错，高大上的CPU流水线其实和我们打工人的流水线是一样的。

假如我们在冰墩墩工厂上班，生产流水线分为五个步骤，如下图所示：

![图片](https://static001.geekbang.org/resource/image/4e/e0/4e68e7b1f59cedb8723b32141ac12fe0.jpg?wh=1920x852)

在冰墩墩生产线上需要至少五个工人，各自负责模具制作、模具清洗、模具抛光、硅胶塑形和融入图案这五个环节中的一个。最简单的方法自然是：同一时刻只有一个冰墩墩在制作。但是冬奥会的热度让市场上的冰墩墩供应不足，为了早日实现“人手一墩”的目标，有什么提升生产效率的办法呢？

稍微想想就知道，生产线上一个人在制作冰墩墩的时候，另外四个工人都处于空闲状态，显然这是对人力资源的极大浪费。想要提高效率，我们不妨在第一个冰墩墩模具制作出来进入清洗阶段的时候，马上开始进行第二个冰墩墩模具的制作，而不是等到第一个冰墩墩全部步骤做完后，才开始制作下一个。
<div><strong>精选留言（22）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/29/a6/ad/e65aec4c.jpg" width="30px"><span>苏流郁宓</span> 👍（13） 💬（1）<div>预读取指令的好处是加强分支预测能力，减少无用功，但不仅仅于此，比如某些软件代码转汇编，为了对齐会增加一些无用的指令，比如x86的nop（它有时会夹在几个其它指令中），还有 复杂的指令可以通过微码进行转换为几个简单的指令，总之，cpu不是也不应该所有的指令全部都执行
预读取指令，有利于提高cpu效率，在一开始不执行浪费的时间好过cpu做到一半，才发现是无用的指令强的啊，还有部分条件指令，可以跳过不执行（比如c语言提高if的权重，降低else if的权重就是代码优化的方法），所以提高cpu效率在软硬件结合一起努力的啊
可以直接取指然后译码再执行，但那样效率会低很多！分支预测是配合cpu流水线工作的，主要是看应用场景，电脑手机等肯定用到分支预测等，但那些老旧或简单的计算器压根分支预测用不到呀
一句话：看应用场景再决定造什么样的cpu？</div>2022-08-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/27/ac/bf/f549183e.jpg" width="30px"><span>=</span> 👍（4） 💬（4）<div>wire [31:0] adder = is_jal ? jimm : (is_bxx &amp; bimm[31]) ? bimm : 4;  assign pre_pc = pc + adder;
在计算指令地址偏移量的时候，为什么写is_bxx &amp; bimm[31]，而不是直接写is_bxx呢？</div>2022-08-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1b/9c/ac/4a488a4e.jpg" width="30px"><span>伊宝峰</span> 👍（2） 💬（1）<div>对指令预读取，方便形成流水线，加快执行速度，因为从存储器中直接取指令会比较慢。</div>2022-08-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/31/22/52/49be0b7e.jpg" width="30px"><span>一笑千古</span> 👍（0） 💬（1）<div>老师，我想问一下为什么要将立即数的最高位复制以满足32位寄存器的长度要求</div>2022-12-07</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/2c/b9/32/c6177eb3.jpg" width="30px"><span>一个要强的男人</span> 👍（0） 💬（3）<div>老师，请问：对于单核cpu的流水线来说，如果在译码阶段占满了这个时钟周期，那么如何在对下一个任务进行取指呢？还是说在设计之初已经确定这个时钟周期肯定能执行完4个操作。这是我的疑问，对于单核来说，并没有像工人的流水线（有五个人在工作），这种怎么理解呀，搜索了很多资料都在拿工厂的流水线打比喻，没搞明白。</div>2022-12-01</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/28/28/a9/4cf153a3.jpg" width="30px"><span>雨巷</span> 👍（0） 💬（1）<div>请问老师，jalr指令没有进行分支预测是吧？</div>2022-11-25</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/27/eb/bf/8acfeaa6.jpg" width="30px"><span>小傅</span> 👍（0） 💬（1）<div>wire [31:0] bimm = {{20{instr[31]}}, instr[7], instr[30:25], instr[11:8], 1&#39;b0}; 这句怎么理解呢，{20{instr[31]}}这又是什么意思呢？</div>2022-11-15</li><br/><li><img src="" width="30px"><span>Geek_489363</span> 👍（0） 💬（1）<div>根据b型指令的格式，为什么会有得到{{20{instr[31]}}, instr[7], instr[30:25], instr[11:8], 1&#39;b0}？不是很理解</div>2022-11-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/27/f4/48/2242bed9.jpg" width="30px"><span>吴建平</span> 👍（0） 💬（1）<div>确实少了一段代码，下面这部分，gitee也没有。而且输入in_pc_next也没有在模块定义里看到。我的理解是，pre_id是if_id的伴生电路，他们俩其实都属于取指阶段，逻辑上属于同一个时钟周期。正常情况下（流水线正常运作），每次时钟跳变，根据next读取新的指令，pre_id就算出下一条指令地址，此时if_id就用此输出作为in_pc_next输入。所以pre_id比if_id要快半个周期。
  &#47;&#47;下一条指令的PC
  always @(posedge clock) begin
    if (reset) begin 
      reg_pc_next &lt;= 32&#39;h0; 
    end else if (flush) begin 
      reg_pc_next &lt;= 32&#39;h0; 
    end else if (valid) begin 
      reg_pc_next &lt;= in_pc_next; 
    end
  end</div>2022-08-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/27/f4/48/2242bed9.jpg" width="30px"><span>吴建平</span> 👍（0） 💬（1）<div>确实是少了一段代码，gitee下载的代码也没有。是reg_pc_next这部分，其输入不是out_pc_next</div>2022-08-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/2f/85/d1/bfe4d1b2.jpg" width="30px"><span>小博(微信/手机号1849登录)</span> 👍（0） 💬（1）<div>老师讲的很棒呀，文档学习比视频省时间。</div>2022-08-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1b/6b/2c/b27eefc5.jpg" width="30px"><span>Abcd</span> 👍（0） 💬（3）<div>if_id的代码不全啊老师，out_pc_next的那段是不是漏了？另外课程中的代码有Github仓库吗？</div>2022-08-16</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTIOMGF5KoLP5t64epdsVAYBBSu5hZFMvl7vqDkDMt7rwIfTur8HYBqLozZxZC78QUI3vVTxENDycA/132" width="30px"><span>Geek_e0e3b8</span> 👍（0） 💬（6）<div>&#47;&#47;B型指令的立即数拼接    
wire [31:0] bimm  = {{20{instr[31]}}, instr[7], instr[30:25], instr[11:8], 1&#39;b0};
&#47;&#47;J型指令的立即数拼接 
wire [31:0] jimm  = {{12{instr[31]}}, instr[19:12], instr[20], instr[30:21], 1&#39;b0};
请问两种指令的立即数拼接中{20{instr[31]}} 和 {12{instr[31]}} 该如何理解？有没有可能是写错了？希望能够给个具体指令范例详细说明下，谢谢~</div>2022-08-15</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/2f/89/38/441bb99b.jpg" width="30px"><span>你要有个信念</span> 👍（0） 💬（2）<div>老师您好，我不太理解立即数为什么要以那样的格式拼接？ </div>2022-08-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/2e/f6/ef/9d19893f.jpg" width="30px"><span>skyline</span> 👍（0） 💬（3）<div>wire [31:0] adder = is_jal ? jimm : (is_bxx &amp; bimm[31]) ? bimm : 4;
有小伙伴知道为啥要与上bimm的符号位么？</div>2022-08-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/1c/94/bf891bb0.jpg" width="30px"><span>陈-特-别</span> 👍（0） 💬（1）<div>请问老师 上面说的如果跳转指令不成立的话 需要冲刷指令 那请问cpu是如何实现执行正确的指令的（跳转条件成立的指令）？</div>2022-08-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/27/eb/bf/8acfeaa6.jpg" width="30px"><span>小傅</span> 👍（1） 💬（0）<div>请问MiniCPU 的整体框架是怎么设计出来的呢？</div>2022-11-15</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/21/20/1299e137.jpg" width="30px"><span>秋天</span> 👍（1） 💬（2）<div>wire [31:0] bimm  = {{20{instr[31]}}, instr[7], instr[30:25], instr[11:8], 1&#39;b0};  这是 verilog 预发的规则吗 这么取值 还有这个取值 跟老师的那个图怎么对应看啊？？？</div>2022-09-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/29/56/82/d965a0f5.jpg" width="30px"><span>嗨！探索者</span> 👍（0） 💬（0）<div>“访存阶段（Memory Access）：访存是指存储器访问指令将数据从存储器中读出，或写入存储器的过程。”
是指令访问存储器呢还是存储器访问指令？</div>2024-11-01</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/b8/dd/37726c34.jpg" width="30px"><span>小马哥</span> 👍（0） 💬（0）<div>指令预读取可以减少流水线中的气泡（stalls），保持流水线的连续流动，从而提高处理器的整体性能。</div>2024-01-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1d/9a/89/babe8b52.jpg" width="30px"><span>A君</span> 👍（0） 💬（0）<div>给取指模块增加预取功能，取指才能和其他组成流水线，否则就是同步操作了</div>2023-11-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1d/9a/89/babe8b52.jpg" width="30px"><span>A君</span> 👍（0） 💬（0）<div>预取的概念有点不清，它是指取了一条指令发给译码器后再提前下N条指令？还是说，反正它会持续取指，如果遇到跳转就推定它一定沿着某个分支执行因此就沿着那个分支取指？</div>2023-01-10</li><br/>
</ul>