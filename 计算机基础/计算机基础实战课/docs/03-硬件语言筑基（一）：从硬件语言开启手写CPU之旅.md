你好，我是LMOS。

我们都知道，自己国家的芯片行业被美国“吊打”这件事了吧？尤其是像高端CPU这样的芯片。看到相关的报道，真有一种恨铁不成钢的感觉。你是否也有过想亲自动手设计一个CPU的冲动呢？

万丈高楼从地起，欲盖高楼先打地基，芯片是万世之基，这是所有软件基础的开始，这个模块我会带你一起设计一个迷你RISC-V处理器（为了简单起见，我选择了最火热的RISCV芯片）。哪怕未来你不从事芯片设计工作，了解芯片的工作机制，也对写出优秀的应用软件非常重要。

这个处理器大致是什么样子呢？我们将使用Verilog硬件描述语言，基于RV32I指令集，设计一个32位五级流水线的处理器核。该处理器核包括指令提取单元、指令译码单元、整型执行单元、访问存储器和写回结果等单元模块，支持运行大多数RV32I的基础指令。最后，我们还会编写一些简单汇编代码，放在设计出来的处理器上运行。

我会通过两节课的篇幅，带你快速入门Verilog，为后续设计迷你CPU做好准备。这节课我们先来学习硬件描述语言基础，芯片内部的数字电路设计正是由硬件语言完成的。

## 一个芯片的内部电路是怎么样的？

作为开发，你日常最常用的编程语言是什么？也许是C语言、Java、Go、PHP……这些高级编译语言吧。而硬件设计领域里，也有专门的硬件描述语言。为什么会出现专门的硬件描述语言呢？这还要先从芯片的内部结构说起。
<div><strong>精选留言（30）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/27/f8/2c/92969c48.jpg" width="30px"><span>青玉白露</span> 👍（17） 💬（1）<div>感觉大家很吃力，做了一个关于Verilog的初学者笔记，里面包含在线学习网站https:&#47;&#47;zhuanlan.zhihu.com&#47;p&#47;550710744</div>2022-08-06</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/Q3auHgzwzM7mF1Zdh16zKFDsIjV6movCe1vArG6icbr9Bd537NDg7dA6y24LhdC3ypvzqJBW18oGcDeC2yTwDsw/132" width="30px"><span>肖水平</span> 👍（14） 💬（1）<div>思考题：
根本原因就是专用芯片运算速度比GPU快，GPU运算速度比CPU快，而软件实现的算法是运行在CPU上的。
具体原因如下：
1、指令数多：软件实现的算法最终要编译成CPU可执行的机器指令，中间还会有很多控制指令；
2、CPU指令执行步骤多：CPU执行一条指令需要经过取指、译码、执行、访存、写回步骤；
3、多位运算需要拆分：比如128位的运算在32&#47;64位CPU上执行编译后会拆分成多条指令；
4、将算法硬件化后可以直接执行运算，不需要通过指令来控制，多位运算也可以实现多位运算模块来直接运算；
总之软件实现的算法在CPU消耗的时钟数要多很多，而CPU也只擅长控制，不擅长运算。</div>2022-08-03</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/2e/fa/37/3b151ca3.jpg" width="30px"><span>爱酱大胜利</span> 👍（8） 💬（1）<div>思考题：
1.设计的目的 CPU属于“通用性”设计 一个CPU能运行这个算法也能运行那个算法 改改代码就可以 代价就是翻译过程因为通用性所带来的迁就 而硬件化的算法属于“专用性”设计 也就是说它只能做着一件事所以怎么设计方便怎么来 反正以后不用为了实现其他算法再改电路了 这也是软硬件实现的区别之一
2.运行效率 还是由于上一条的设计理念 导致软件的运行依赖于CPU实现的特定指令集 原本算法中一个硬件周期的动作可能被转化为多条指令 而每条指令可能会依赖多个运行周期 即使运行会得到优化 也远远比不上一个周期来的快 而且CPU为了通用性很可能不会将这种特殊性动作添加到一个不常用CISC里</div>2022-08-04</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/25/87/f3a69d1b.jpg" width="30px"><span>peter</span> 👍（8） 💬（3）<div>请教老师几个问题：
Q1：代码转化后的逻辑电路，只是电子版的“设计电路”，并不是实际的电路，对吗？
文中有这样一句：“把一份电路用代码的形式表示出来，然后由计算机把代码转换为所对应的逻辑电路。”，此处，“转换后的逻辑电路”并不是实际的电路，应该只是“设计电路”。
Q2：“cnt_r &lt;=4&#39;b000;”？ 此处应该是四个0吧，为什么写成三个0？笔误吗？
Q3：芯片中的模拟电路是用什么设计的？
Q4：芯片前端设计的代码，就是用verilog写的代码，对于一个芯片来说，一般规模多大？比如十万行代码？</div>2022-08-01</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/71/4f/bce0d5bc.jpg" width="30px"><span>哈哈</span> 👍（5） 💬（1）<div>思考题我认为，软件实现要在通用的硬件上执行就势必要执行一些逻辑上的模拟或者转换。而专用的硬件则没有这些转换过程，并且可以针对性的优化执行路径，所以要快许多。</div>2022-08-01</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/19/ae/c3/d930693b.jpg" width="30px"><span>LockedX</span> 👍（3） 💬（2）<div>老师，有个问题一直没有想明白
reg 	[3:0]         cnt_r;    
wire	[1:0]		cout_w;
reg和wire的声明，冒号前面是数字代表位宽，冒号后面的0含义是什么？</div>2022-08-01</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/27/73/63/791d0f5e.jpg" width="30px"><span>青蓝</span> 👍（2） 💬（1）<div>FPGA编程和今天讲得编程有什么区别吗？</div>2022-08-01</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/2a/af/28/9ffc55a2.jpg" width="30px"><span>可爱因子1/n</span> 👍（1） 💬（1）<div>针对我自己的理解，打个比喻：在性能和单位时间以及油门相同的情况下，我开着一辆车的发动机的转速和一个直接裸的发动机的转速比较，裸的发动机的转速按常理来说应该会更快一点，不知道我的比喻是否准确？</div>2022-08-06</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/f4/8d/4ea7aeef.jpg" width="30px"><span>111</span> 👍（1） 💬（1）<div>关于思考题：
我的理解是 Verilog更多面向的是硬件，通过它设计完成之后，可以直接参照其代码流程组合相关硬件，在针对特定算法的设计后，组合出来的就是该算法最“合身”的底层电路模型。

而对于一些软件语言的实现，更多的是业务层面的实现，业务实现之后还要面临“翻译”，翻译成计算机能够执行的指令集，这一步就已经开始出现了效率损耗，同时因为“翻译”动作，也就可能出现为了实现某一功能，底层指令可能要绕一些“弯路”才能实现，毕竟不能像Verilog那样，做到“完美贴切”的电路设计</div>2022-08-02</li><br/><li><img src="" width="30px"><span>nmg</span> 👍（1） 💬（1）<div>是因为用硬件实现是算法最优化电路设计，而软件实现可能是芯片现有资源的组合，不是最优电路，所以会慢吗？</div>2022-08-01</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/kddcgrkQHsuwH72o54jljmTnibicYfZFPnoTkphqCUCHv2U8h7UuHtKRBlZdcWQeUSNfUbbNhMfYLiccsHq27d7Tg/132" width="30px"><span>Geek_785f19</span> 👍（1） 💬（2）<div>请教老师：
平时做的是业务系统，对底层不熟悉，有兴趣多了解底层知识，学习本课程需要什么前置知识吗</div>2022-08-01</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/29/a6/ad/e65aec4c.jpg" width="30px"><span>苏流郁宓</span> 👍（1） 💬（1）<div>用 Verilog 设计并且硬件化之后，要比用软件实现的运算速度快很多？
俺觉得软件需要译码，消耗时间。还有软件功能化设计，需要用到硬件的不同模块，光是沟通自然也消耗时间的。更不用说分支预测失败，重来也消耗时间的
但硬件有个难度，就是越复杂的东西，用软件高级语言开发更容易，比如高级语言开发浏览器比光靠汇编等低级语言开发难度容易得多！
软件与硬件取平衡，开发看那个性价比高，更贴近实用的啊</div>2022-08-01</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/2e/0a/46/cde22711.jpg" width="30px"><span>IgoZhang</span> 👍（0） 💬（1）<div>老师，我发现一个重要问题没讲，导致没法连贯：
Verilog  是啥，我的意思是它干啥用，它的输出是啥？

他是一个硬件描述语言，但是的干啥用呢？  是否可以举例说明什么时候使用Verilog写了啥，然后写出来的结果用于做啥？    我还以为是汇编呢？  有点理解不好</div>2023-03-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/30/45/bf/1f36539b.jpg" width="30px"><span>南总无敌</span> 👍（0） 💬（1）<div>思考题：为什么很多特定算法，用 Verilog 设计并且硬件化之后，要比用软件实现的运算速度快很多？
答：因为用verilog设计硬件化之后，算法能够用更少的指令和SIMD（单指令多数据）的方式执行，例如NPU执行卷积运算时候只要配置好卷积参数就能一条指令执行，并且数据能够实现部分复用。但CPU需要拆解成为多条指令，每条指令都必须完整走完5个执行步骤，这样花费的cycles数就会成倍上涨</div>2022-10-07</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/30/89/00/0b3e720b.jpg" width="30px"><span>xhh</span> 👍（0） 💬（1）<div>请问老师在Linux中的Verilog编辑器是VSCode吗还是什么</div>2022-09-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/29/f5/e1/5ea38f5b.jpg" width="30px"><span>BiuBiuBiu～</span> 👍（0） 💬（1）<div>题外问题：能不能帮忙简略聊一下芯片复位和解复位这个点</div>2022-09-01</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/18/b1/68/35e0729f.jpg" width="30px"><span>Frank611</span> 👍（0） 💬（1）<div>cnt clk这些名字是固定的吗？还是跟变量一样，可以任意定义，但是又没有定义这些信号的类型</div>2022-08-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/2b/89/50/aee9fdab.jpg" width="30px"><span>小杰</span> 👍（0） 💬（1）<div>自己的理解。特定的算法，应该是依赖特定的实现，高级语言虽然能在数学上，看着像是一步一步在执行，实际最后的执行经过了编译器，这里其实已经不是一条语句对应cpu一条指令，然后不同cpu的执行可能也会有区别。专门的语言配合专门的cpu，来运行专门的算法，效率肯定是要高于上面使用，高级语言加商业化的通用cpu</div>2022-08-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/21/10/5e/42f4faf7.jpg" width="30px"><span>天择</span> 👍（0） 💬（1）<div>对于一些特殊的算法，可以在硬件电路级别进行优化，充分利用不同电路的特点，而软件算法即使被编译器优化过，也被限制在写死的硬件电路上了。</div>2022-08-05</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/2e/f6/ef/9d19893f.jpg" width="30px"><span>skyline</span> 👍（0） 💬（1）<div>“它从 0 时刻开始执行，且内部逻辑语句只按顺序执行一次，多个 initial 块之间是相互独立的“
问：如果内部是非阻塞赋值的话，岂不是内部也可以并行执行么？</div>2022-08-04</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/27/73/63/791d0f5e.jpg" width="30px"><span>青蓝</span> 👍（0） 💬（1）<div>特定的算法需要大量特定的处理器的能力，通过硬件设计可以增加大量的算法所需的能力单元，如GPU就是CPU砍掉大量功能留下大量运算单元，所以GPU特别适合做图形渲染、深度学习模型运算</div>2022-08-02</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/24/a5/8a/27602e90.jpg" width="30px"><span>墨橦的猪</span> 👍（0） 💬（1）<div>硬件设计是特定电路实现更符合项目，并且是真正的并行结构，软件是在特定的处理器下进行项目实现，顺序结构。效率远低于直接硬件设计实现。</div>2022-08-02</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/2e/d0/40/5de7e64d.jpg" width="30px"><span>Leo</span> 👍（0） 💬（1）<div>软件执行，数据流和指令流需要在内存——cache——cpu之间流动，需要执行取指，译码，执行，回写等过程，并且还会出现cache miss的情况，增加时间开销。将算法定点化之后不涉及到以上的过程，所以效率大大提升！！</div>2022-08-02</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/d3/98/60d13550.jpg" width="30px"><span>Bryan</span> 👍（0） 💬（1）<div>思考题：盲猜因为软件需要经过操作系统管理的内存，会涉及到虚拟内存寻址等，而硬件则可以省掉这些开销</div>2022-08-02</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/b4/9c/e034537f.jpg" width="30px"><span>wudishi</span> 👍（0） 💬（1）<div>目测因为硬件化之后可以利用到电路是天生并行的特性，而不像cpu需要一条条指令往下执行</div>2022-08-02</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/83/06/9d88395e.jpg" width="30px"><span>暂命名</span> 👍（0） 💬（1）<div>软件运行在硬件之上，硬件上直接运行跟通过软件转换之后再给硬件运行两者的效率是不一样的。</div>2022-08-01</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/2a/39/93/f0247cf8.jpg" width="30px"><span>一本书</span> 👍（0） 💬（1）<div>思考题，我觉得硬件的优化要比软件的优化快的多的原因是，软件是用CPU来读取的，如果CPU性能很差，你程序写的再好，也发挥不了太大的作用，就像华为的麒麟芯片一样，一样的软件，但是在不同的CPU上运行的效率是不一样的，好的自然就快一点。不知道对不对</div>2022-08-01</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/f7/f8/3c0a6854.jpg" width="30px"><span>xavier</span> 👍（0） 💬（0）<div>我觉得初学者首先要认识到的一点是：硬件语言代码是并行执行的，这有别于软件代码的顺序执行。</div>2023-05-30</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/Q3auHgzwzM7mF1Zdh16zKFDsIjV6movCe1vArG6icbr9Bd537NDg7dA6y24LhdC3ypvzqJBW18oGcDeC2yTwDsw/132" width="30px"><span>肖水平</span> 👍（0） 💬（0）<div>&#47;&#47;可配置位宽和计数周期数的计数器
module counter #(
        parameter               WIDTH = 4,  &#47;&#47;计数器位宽
        parameter               COUNT = 10  &#47;&#47;计数多少次输出周期位
    )
    (
        input                   clk,        &#47;&#47;输入时钟
        input                   rstn,       &#47;&#47;复位端，低有效
        output    [WIDTH-1:0]   cnt,        &#47;&#47;计数输出
        output                  cout        &#47;&#47;输出周期位
    );

    reg [WIDTH-1:0]             cnt_r;      &#47;&#47;计数器寄存器

    always @ (posedge clk or negedge rstn) begin
        if (!rstn) begin                    &#47;&#47;复位时，计时归0
            cnt_r        &lt;= 4&#39;d0;
        end
        else if (cnt_r == (COUNT - 1)) begin &#47;&#47;计时10个cycle时，计时归0
            cnt_r        &lt;= 4&#39;d0;
        end
        else begin
            cnt_r        &lt;= cnt_r + 4&#39;d1;   &#47;&#47;计时加1
        end
    end

    assign  cout = (cnt_r == (COUNT - 1));  &#47;&#47;输出周期位
    assign  cnt  = cnt_r;                   &#47;&#47;输出实时计时器

endmodule
</div>2022-08-03</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/18/8b/c3/bf036d99.jpg" width="30px"><span>砥砺奋进</span> 👍（0） 💬（0）<div>思考题是 类似于 FGPA和ASIC的区别吗 ASIC可以根据算法的逻辑采用最少的电路完成</div>2022-08-02</li><br/>
</ul>