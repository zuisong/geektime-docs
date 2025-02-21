到今天为止，专栏已经过半了。过去的20多讲里，我给你讲的内容，很多都是围绕着怎么提升CPU的性能这个问题展开的。

我们先回顾一下[第4讲](https://time.geekbang.org/column/article/93246)，不知道你是否还记得这个公式：

程序的CPU执行时间 = 指令数 × CPI × Clock Cycle Time

这个公式里，有一个叫CPI的指标。我们知道，CPI的倒数，又叫作IPC（Instruction Per Clock），也就是一个时钟周期里面能够执行的指令数，代表了CPU的吞吐率。那么，这个指标，放在我们前面几节反复优化流水线架构的CPU里，能达到多少呢？

答案是，最佳情况下，IPC也只能到1。因为无论做了哪些流水线层面的优化，即使做到了指令执行层面的乱序执行，CPU仍然只能在一个时钟周期里面，取一条指令。

![](https://static001.geekbang.org/resource/image/dd/13/dd88d0dbf3a88b09d5e8fb6d9e3aea13.jpeg?wh=2173%2A1018)

这说明，无论指令后续能优化得多好，一个时钟周期也只能执行完这样一条指令，CPI只能是1。但是，我们现在用的Intel CPU或者ARM的CPU，一般的CPI都能做到2以上，这是怎么做到的呢？

今天，我们就一起来看看，现代CPU都使用了什么“黑科技”。

## 多发射与超标量：同一时间执行的两条指令

之前讲CPU的硬件组成的时候，我们把所有算术和逻辑运算都抽象出来，变成了一个ALU这样的“黑盒子”。你应该还记得第13讲到第16讲，关于加法器、乘法器、乃至浮点数计算的部分，其实整数的计算和浮点数的计算过程差异还是不小的。实际上，整数和浮点数计算的电路，在CPU层面也是分开的。
<div><strong>精选留言（30）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/12/fa/fd/ec24cba7.jpg" width="30px"><span>fcb的鱼</span> 👍（7） 💬（1）<div>想知道在cpu里边是怎么并行执行的？一直觉得cpu是一个单线程的工作模式。</div>2020-02-05</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/e7/2e/1522a7d6.jpg" width="30px"><span>活的潇洒</span> 👍（6） 💬（2）<div>“安腾失败的原因有很多，其中有一个重要的原因就是“向前兼容”。”现在终于明白安腾为什么失败了

day26 笔记：https:&#47;&#47;www.cnblogs.com&#47;luoahong&#47;p&#47;11441329.html</div>2019-09-01</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/55/45/e4314bc6.jpg" width="30px"><span>magicnum</span> 👍（24） 💬（0）<div>个人感觉VLIW架构下处理器乱序执行应该不需要了，因为编译器已经将可以并行执行的指令打包成了指令包；操作数前推和分支预测应该可以用吧？</div>2019-06-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/9b/ba/333b59e5.jpg" width="30px"><span>Linuxer</span> 👍（24） 💬（6）<div>一个时钟周期也只能执行完这样一条指令，CPI 只能是 1。但是，我们现在用的 Intel CPU 或者 ARM 的 CPU，一般的 CPI 都能做到 2 以上，这是怎么做到的呢？这里不是ipc？</div>2019-06-24</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTLzSRrK59sydlOmgvqIFm1pjHA55RcM5ttWvHdOZyibZhFCr7picy4Xf5Bf9dLOW8d2DGUwA1zormzw/132" width="30px"><span>钱勇</span> 👍（7） 💬（1）<div>不能叫VLIW的失败，只能说是EPIC的失败。
VLIW在配套专用编译器的专用芯片上，应用应该是有前途的。
只是不适合用在涉及到前后兼容的通用芯片上。</div>2020-05-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/ec/3e/885ec1d2.jpg" width="30px"><span>宋不肥</span> 👍（6） 💬（0）<div>这个本身就已经编译器是打乱顺序执行了吧。分支预测的话，相对于指令包的更多指令来讲，预测出错的话，清理缓存的开销应该会更大，但只要出错率*出错时的开销够小的话就应该依旧可行吧。操作数前推应该依旧可以用</div>2019-06-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1b/86/b4/51b7f79c.jpg" width="30px"><span>QianLu</span> 👍（4） 💬（0）<div>在《计算机组成与设计：硬件、软件接口（第三版中文）》中，“指令级并行”和“多发射”应是属于章节6.9。</div>2020-02-25</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/DYAIOgq83eqXNhbTULKiakib8lYXrvGF2zPwfedooBzC2EtSv1nt1MwV1KUvTkcJrvCBFvcdwJicnr3OEXnk9GUCg/132" width="30px"><span>WENMURAN</span> 👍（2） 💬（0）<div>如何让CPU的吞吐率超过1？
经过前面对于各种冒险的操作，每个周期可以处理的指令只有1条，那么如何让这个数超过1？
解决:多发射，与超标量
一次从内存里取出多条指令，然后交给多个并行的指令译码器，然后交给对应的功能单元去处理。多发射，就是一次取多条指令进行译码执行，超标量，就是一个周期内同时有多条流水线并行工作。
</div>2020-04-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/e0/6b/f61d7466.jpg" width="30px"><span>prader26</span> 👍（2） 💬（0）<div>1 程序的执行时间= 指令数*CPI* 其中周期
2  为了进一步提升cpu的效率，引入了多发射和超标量(同时取多条指令，让多条流水线并行)。</div>2019-09-22</li><br/><li><img src="" width="30px"><span>范海良</span> 👍（1） 💬（2）<div>硬件层面是怎么检测依赖关系的？</div>2022-03-06</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/17/e3/01/a254f22d.jpg" width="30px"><span>童言</span> 👍（1） 💬（0）<div>多发射、超标量通过一次读取多条指令、并行进行指令译码来实现 IPC 的提升。但问题在于，有相互依赖的指令并不适合这个策略。如何解决这个问题？期待后续内容。</div>2021-05-05</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/68/ef/6264ca3d.jpg" width="30px"><span>Magic</span> 👍（1） 💬（0）<div>应该是可以的。超长指令字只是在编译器层面对指令数据依赖关系进行分析，并且找到没有依赖关系的n条指令打包成指令包，cpu取到指令包后，会将每条指令分发到不同的流水线执行，这个过程都是一样的</div>2020-10-06</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/6e/8e/5d309a85.jpg" width="30px"><span>拯救地球好累</span> 👍（1） 💬（0）<div>---总结---
为了让IPC大于1，除了指令执行阶段，取指和译码阶段也需要并行化。
多发射：同一个时间，多条指令会被发射到不同的译码器或后续的流水线中。
超标量：一个时钟周期内执行多个标量的运算。
无论是乱序执行技术还是超标量技术，冒险问题都是不可忽视的。
超长指令字：利用编译器在编译阶段便完成指令乱序、插入NOP指令等工作，并将可并行的打包组成一个指令包，在指令执行阶段并行执行指令包中所有指令。
VLIW失败的原因：将指令乱序等工作放在了编译阶段做，导致硬件的提升也需要软件层面的重编译工作

---问题---
请问下老师，硬件是如何检测到数据依赖的呢？</div>2019-10-27</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTKw77qmuyx5tL2IKrNicAibIEvprPHg2CibZCKUicXZBSlS7Tib1hINYtVVXCKVdGqwteTx9yUsO9w5P5Q/132" width="30px"><span>Geek_53dfd0</span> 👍（1） 💬（0）<div>非计算机的专业的我已经听起来比较吃力了</div>2019-10-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/81/e9/d131dd81.jpg" width="30px"><span>Mamba</span> 👍（0） 💬（0）<div>安腾CPU在VLIW架构下采用了分支预测和操作数前推等技术来优化性能，但由于其架构的特点，乱序执行的应用与传统超标量处理器有所不同。</div>2024-08-27</li><br/><li><img src="" width="30px"><span>！巴甫洛夫的狗</span> 👍（0） 💬（0）<div>现代CPU设计中的超标量和VLIW架构技术为提高CPU吞吐率带来了新的可能性。超标量技术通过并行取指令和指令译码，以及增加多个功能单元并行处理指令，实现了超过1的吞吐率。而VLIW架构则通过编译器在软件层面优化指令执行顺序，实现指令包并行执行。然后，Intel的安腾处理器由于指令集不兼容和扩展困难等问题，最终未能获得市场认可。这表明技术思路上的先进想法在实际应用中会遇到更多具体的实践考验。</div>2024-03-22</li><br/><li><img src="" width="30px"><span>Geek_88604f</span> 👍（0） 💬（0）<div>1.个人认为乱序执行、操作数前推、分支预测应该都会用到（把一个指令包当成一条指令就可以理解了；编译器是否分析很准也存疑；乱序执行的电路设计已经摆在那里了）
    2.由于兼容性问题导致的失败在软件领域比比皆是</div>2023-11-05</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1e/f1/12/c40d07bc.jpg" width="30px"><span>pearl刘东洋</span> 👍（0） 💬（0）<div>我是觉得power服务器和aix的成功和现有阶段的难以替代的很一个重要因素可能就是它的编译器，我猜测可能用了和vliw想通的理念设计的</div>2021-03-01</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/3a/6d/8b417c84.jpg" width="30px"><span>Wheat Liu</span> 👍（0） 💬（0）<div>安腾为什么要把乱序指令打成指令包，在编译器重排序完了直接执行不行吗？重排时编译器知道数据依赖关系，执行的结果又不会变</div>2021-01-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/49/3c/5d54c510.jpg" width="30px"><span>skull</span> 👍（0） 💬（0）<div>&quot;这说明，无论指令后续能优化得多好，一个时钟周期也只能执行完这样一条指令，CPI 只能是 1。但是，我们现在用的 Intel CPU 或者 ARM 的 CPU，一般的 CPI 都能做到 2 以上&quot;，老师，纠个错，这里是IPC吧</div>2020-10-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/2f/7a/ab6c811c.jpg" width="30px"><span>相逢是缘</span> 👍（0） 💬（0）<div>徐老师，请教一个问题
内存的主频是很低的，怎能在一个时钟周期里面取多个指令呢？
（内存外接32位地址线和32位数据线，每次内存的一个时钟周期，只能取一个32位数据啊）</div>2020-10-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/03/79/08daec09.jpg" width="30px"><span>Mr_Ben</span> 👍（0） 💬（0）<div>老师，你好。请教下:安腾cpu架构下，将多个指令打包后一次执行。是否是cpu从指令段取出多条指令，一次执行？还是编译器编译时，就将指令打包了。这样的话，是否在这个cpu上运行的编译器版本有特殊要求？</div>2020-09-10</li><br/><li><img src="" width="30px"><span>Paul Shan</span> 👍（0） 💬（0）<div>个人以为超长指令字架构设计的一个问题是指令包的内部依赖会变得很复杂，这里的复杂度不是线性的而是平方级，指令包每扩大一倍，复杂度就是原来的四倍，这让摩尔定理如何玩得下去呀。
而且把处理这些复杂度都推给编译器，编译器又没法和硬件升级同步，除非是从应用软件到硬件通吃的公司才能处理，像英特尔这种主打开放架构的公司，现实中的操作性就大打折扣。</div>2020-08-15</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1d/9a/89/babe8b52.jpg" width="30px"><span>A君</span> 👍（0） 💬（0）<div>请问nvidia和amd的gpu是不是也是vliw的设计？</div>2020-07-03</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1d/9a/89/babe8b52.jpg" width="30px"><span>A君</span> 👍（0） 💬（0）<div>超标量技术也和乱序指令发射器一样让指令译码可以并行执行。vliw设计将指令乱序、操作数前推、加nop等工作交给了编译器，编译后的指令不再以一条条呈现，而是以一个指令包的形式出现，指令包和指令包之间应该也能应用乱序、操作数前推等操作。</div>2020-07-03</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/18/fe/2d/e23fc6ee.jpg" width="30px"><span>深水蓝</span> 👍（0） 💬（0）<div>虽然虽然VLIW失败了，但是有编译器优化的乱序指令这个做法应该一致沿用到现在吧。由编译器将没有依赖的指令放到一起执行，可以降低CPU硬件处理冲突的机会，也可以降低CPU乱序执行对指令预读长度的要求吧？</div>2020-02-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/6e/8e/5d309a85.jpg" width="30px"><span>拯救地球好累</span> 👍（0） 💬（0）<div>---总结---
为了让IPC大于1，除了指令执行阶段，取指和译码阶段也需要并行化。
多发射：同一个时间，多条指令会被发射到不同的译码器或后续的流水线中。
超标量：一个时钟周期内执行多个标量的运算。
无论是乱序执行技术还是超标量技术，冒险问题都是不可忽视的。
超长指令字：利用编译器在编译阶段便完成指令乱序、插入NOP指令等工作，并将可并行的打包组成一个指令包，在指令执行阶段并行执行指令包中所有指令。
VLIW失败的原因：将指令乱序等工作放在了编译阶段做，导致硬件的提升也需要软件层面的重编译工作

---问题---
请问下老师，硬件是如何检测到数据依赖的呢？</div>2019-10-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/17/64/4c/791d0f5e.jpg" width="30px"><span>Donatello</span> 👍（0） 💬（1）<div>认真思考发现了一个问题，取指不是依赖于pc寄存器吗 那是如何完成多发射的
</div>2019-08-02</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/5d/01/9cd84003.jpg" width="30px"><span>栋能</span> 👍（0） 💬（1）<div>有句话没太理解：“于是，我们可以让编译器把没有依赖关系的代码位置进行交换。然后，再把多条连续的指令打包成一个指令包。安腾的 CPU 就是把 3 条指令变成一个指令包。” 这里连续指令是指无依赖的指令，还是有依赖关系的指令？</div>2019-07-06</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/f8/23/937a1bb7.jpg" width="30px"><span>周</span> 👍（0） 💬（0）<div>多发射，超标量，， 执行顺序怎么控制呢？  
a=3;
b=a+1;
c=b+a;
像这种有顺序的会怎么处理呢？</div>2019-07-03</li><br/>
</ul>