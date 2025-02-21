你好，我是LMOS。

通过前面几节课的学习，我们已经完成了MiniCPU五级流水线的模块设计，现在距离实现一个完整的MiniCPU也就一步之遥。

还差哪些工作没完成呢？还记得我们在第六节课设计的MiniCPU架构图吗？回想一下，我们已经设计完成的五级流水线，都包含下图的哪些模块？

![图片](https://static001.geekbang.org/resource/image/31/dd/31b586c344cd7d0127775e7ff63711dd.jpg?wh=1920x1289)

上图的CPU核心模块，也就是CPU Core包含的模块的设计，这些我们已经在前面几节课里完成了。除了五级流水线的模块，我们还设计了用于保存操作数和运算结果的通用寄存器组，设计了解决数据冒险问题的forwarding模块，以及解决控制冒险问题的hazard模块。

接下来，我们还需要搞定一些外围组件，也就是图里虚线框外的系统总线、ROM、RAM、输入输出端口GPIO（GPIO比较简单，课程里没专门讲）和UART模块。

学完这节课，我们就可以把这个CPU运行起来了，最终我还会带你在这个CPU上跑一个RISC-V版本的Hello World程序（课程代码从[这里](https://gitee.com/lmos/Geek-time-computer-foundation)下载），是不是很期待？话不多说，我们这就开始！

## 系统总线设计

首先，让我们看看CPU的系统总线。

总线是连接多个部件的信息传输线，它是各部件共享的传输介质。在某一时刻，只允许有一个部件向总线发送信息，而多个部件可以同时从总线上接收相同的信息。MiniCPU的系统总线用来连接CPU内核与外设，完成信息传输的功能。
<div><strong>精选留言（12）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/15/32/fe/c2179924.jpg" width="30px"><span>mantra</span> 👍（1） 💬（1）<div>询问小编一个小问题：学到此处 mini_cpu 小结了，还有后续的扩展吗？后续 “RISC-V 指令精讲（X）” 系列是在 GCC + QEMU 环境实现吗？会和 min_cpu 有关联吗？谢谢！</div>2022-08-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/2f/03/8f/38038fb5.jpg" width="30px"><span>Liu Zheng</span> 👍（3） 💬（1）<div>需要指出一下，如果同学用13讲里的方法安装toolchain的话，需要作以下修改才能跑出hello world来：
1. 在`sim&#47;asm&#47;Makefile`中，需要把所有的`riscv32`都替换成`riscv64`。详情见12讲里面的multilib部分。
2. 如果你和我一样用的是ubuntu 20.04，那么需要`mini_cpu&#47;Makefile`里面，把`python`换成`python3`。因为默认ubuntu20.04开始已经没有`python`了。</div>2022-08-24</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTKy9XSxDLRibViazIs1wzhEmIQqMlhcoKhTXNvxXkaPGIveib8B9ibvpdkZxABKFIc4iaSMrkTh7EfWjtg/132" width="30px"><span>likejjj</span> 👍（1） 💬（3）<div>可以在fpga上面跑这个cpu不？</div>2022-08-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/27/f8/2c/92969c48.jpg" width="30px"><span>青玉白露</span> 👍（1） 💬（1）<div>打算写个汇编搞一下！</div>2022-08-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/2e/d1/f0/0eafdb8e.jpg" width="30px"><span>😇</span> 👍（0） 💬（1）<div>总线你的cpu--&gt;imem的imem是啥意思啊</div>2022-09-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/2e/d1/f0/0eafdb8e.jpg" width="30px"><span>😇</span> 👍（0） 💬（2）<div>老师你好，我的运行make asm后显示
make -C .&#47;sim&#47;asm 
make[1]: 进入目录“&#47;home&#47;qianq&#47;mini_cpu&#47;sim&#47;asm”
+ AS src&#47;miniCPU_sim.asm build&#47;miniCPU_sim.o
make[1]: riscv32-unknown-elf-as: Command not found
Makefile:27: recipe for target &#39;build&#47;miniCPU_sim.o&#39; failed
make[1]: *** [build&#47;miniCPU_sim.o] Error 127
make[1]: 离开目录“&#47;home&#47;qianq&#47;mini_cpu&#47;sim&#47;asm”
Makefile:11: recipe for target &#39;asm&#39; failed
make: *** [asm] Error 2
请问这个出错是什么原因呢</div>2022-08-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/2f/03/8f/38038fb5.jpg" width="30px"><span>Liu Zheng</span> 👍（0） 💬（2）<div>老师，想问一下，这里汇编代码里面没发送一个字符延时1ms是为了匹配uart的波特率吗？请问这个mini cpu的串口的波特率是在哪里指明的啊？是固定在uart的verilog代码的某个地方了吗？</div>2022-08-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/2d/ff/22/dadbadb2.jpg" width="30px"><span>云海</span> 👍（0） 💬（1）<div>为什么我运行 make asm 的时候出现这样的error？谢谢

make -C .&#47;sim&#47;asm 
make[1]: Entering directory &#39;&#47;home&#47;yh&#47;ws&#47;riscv&#47;Geek-time-computer-foundation&#47;lesson06~11&#47;mini_cpu&#47;sim&#47;asm&#39;
+ AS src&#47;miniCPU_sim.asm build&#47;miniCPU_sim.o
make[1]: riscv32-unknown-elf-as: Command not found
Makefile:27: recipe for target &#39;build&#47;miniCPU_sim.o&#39; failed
make[1]: *** [build&#47;miniCPU_sim.o] Error 127
make[1]: Leaving directory &#39;&#47;home&#47;yh&#47;ws&#47;riscv&#47;Geek-time-computer-foundation&#47;lesson06~11&#47;mini_cpu&#47;sim&#47;asm&#39;
Makefile:11: recipe for target &#39;asm&#39; failed
make: *** [asm] Error 2
</div>2022-08-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/19/8b/06/fb3be14a.jpg" width="30px"><span>TableBear</span> 👍（0） 💬（1）<div>好难o(╥﹏╥)o</div>2022-08-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/29/a6/ad/e65aec4c.jpg" width="30px"><span>苏流郁宓</span> 👍（0） 💬（1）<div>哈佛结构？</div>2022-08-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/2b/d4/4b/ec621442.jpg" width="30px"><span>范廷东</span> 👍（0） 💬（0）<div>跑通这个案例，需要用ubuntu或centos的虚拟机？需要安装什么工具？

这些能不能补充说一下；</div>2024-02-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/d4/0c/4decd1aa.jpg" width="30px"><span>氢原子</span> 👍（0） 💬（0）<div>计算机两大体系结构分别是冯诺依曼体系结构和哈弗体系结构，可以自己设计第三个体系结构吗？</div>2023-09-13</li><br/>
</ul>