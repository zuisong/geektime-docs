你好，我是LMOS。

这个专栏我会带你学习计算机基础。什么是基础？

基础就是根，从哪里来，到哪里去。而学习计算机基础，首先就要把握它的历史，这样才能了解计算机是怎么一步步发展到今天这个样子的，再根据今天的状况推导出未来的发展方向。

正所谓读历史方知进退，明兴衰。人类比其它动物高级的原因，就是人类能使用和发现工具。**从石器时代到青铜器时代，再到铁器时代，都是工具种类和材料的发展，推动了文明升级。**

让我们先从最古老的算盘开始聊起，接着了解一下机械计算机、图灵机和电子计算机。最后我会带你一起看看芯片的发展，尤其是它的两种设计结构——CISC与RISC。

### 从算盘到机械计算机

算盘就是一种辅助计算的工具，由中国古代劳动人民发明，迄今已有两千多年的历史，一直沿用至今。我准备了算盘的平面草图，你可以感受一下：

![图片](https://static001.geekbang.org/resource/image/c7/d9/c7c942f024b13ce96e9443efa2c93bd9.jpg?wh=1920x795)

上图中周围一圈蓝色的是框架，一串一串的是算椽和算珠，一根算椽上有七颗算珠，可以上下拨动，从右至左有个、十、百……亿等计数位。有了算盘，计算的准确性和速度得到提高，我们从中可以感受到先辈的智慧。

与其说算盘是计算机，还不如说它是个数据寄存器。“程序”的执行需要人工实现，按口诀拨动算珠。过了两千多年，人们开始思考，能不能有一种机器，不需要人实时操作就能自动完成一些计算呢？
<div><strong>精选留言（30）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/11/07/ff/b3fe9903.jpg" width="30px"><span>lisimmy</span> 👍（12） 💬（3）<div>小两口包饺子：夫擀饺子皮，妻包饺子
RISC-夫妻用的时间一致，完美流水线作业，并行（回答文中的问题）
CISC-夫擀饺子皮，1分钟一个，妻包饺子，10s一个，就算流水线，虽能并行，也有时间的浪费
因此流水线，会有加速比、效率等概念！</div>2022-08-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/ec/13/49e98289.jpg" width="30px"><span>neohope</span> 👍（9） 💬（3）<div>意犹未尽的话，可以延申阅读：
1、从MCU到SOC
2、从冯诺依曼结构到存算一体
3、Chiplet如何支撑后摩尔时代
4、碳基芯片
5、量子计算</div>2022-07-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/52/40/e57a736e.jpg" width="30px"><span>pedro</span> 👍（32） 💬（3）<div>谈到指令并行，就不得不谈CPU里面最核心的流水线了。

现代处理器都是流水线结构，由多个流水级组成，多个流水线同时干活，比如5级流水线由取指，译码，执行，访存和写回组成。

那么，理想情况下在同一个时钟周期内将会有5条处于不同流水阶段的指令，这就是指令并行。

而这样的CPU就能同时执行多条指令。</div>2022-07-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/17/06/7e/735968e2.jpg" width="30px"><span>西门吹牛</span> 👍（11） 💬（1）<div>指令流水线作业：取指令，指令译码，指令执行等都是独立的组合逻辑电路，每个阶段电路在完成对应任务之后，也不需要等待整个指令执行完成，而是可以直接执行下一条指令的对应阶段。就和工厂流水线一个道理。指令并行其实指的是，多个指令的不同阶段，可以在流水线上，并行的执行。
CPU 指令乱序执行：在执行过程中，还会有指令重排序，有依赖的指令不会重排，但是不依赖的会重排，比如后面的指令不依赖前面的指令，那就不用等待前面的指令执行，它完全可以先执行，充分利用流水线上的空闲位置。</div>2022-07-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/88/9c/cbc463e6.jpg" width="30px"><span>仰望星空</span> 👍（7） 💬（1）<div>为什么RISC的CPU能同时执行多条指令？其实就是CPU中的流水线在发挥作用，CPU执行指令的四个步骤：取指、译指、执行和回写，在执行A指令时也可以同时执行B指令</div>2022-07-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/85/ac/10d68f01.jpg" width="30px"><span>江同学</span> 👍（6） 💬（1）<div>CPU执行指令使用了流水线技术。以三级流水线为例。一个指令可拆分成“取指令 - 指令译码 - 执行指令”三个部分，因为三个部分资源依赖不一样，例如取指令依赖一个译码器把数据从内存取出写入寄存器，指令译码依赖另一个译码器，而执行依赖完成计算工作的ALU，那么第一个指令在译码阶段，第二个指令可以执行取指令了。所以在一定的拆分数量限制下，如果指令拆分得更多，增加更多的流水线，那么就可以同时执行更多的指令了。就好像我们做需求一样，产品经理除了需求后，开发进入开发阶段，产品经理可以继续准备新的需求。</div>2022-07-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/41/62/33520c3e.jpg" width="30px"><span>贾献华</span> 👍（6） 💬（1）<div>hart  硬 件 线 程 （hardware thread）</div>2022-07-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/2b/89/50/aee9fdab.jpg" width="30px"><span>小杰</span> 👍（4） 💬（1）<div>说一下我的理解，不知道是不是对的哈。RISC用的是精简指令，那cpu在执行是所需要的时间更少，一般来说，为了加快执行的速度，会采用多个指令流水线。所以我自己理解的CISC，也能同时执行多条指令，只是相对来说RISC会多一点。</div>2022-08-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/4b/46/717d5cb9.jpg" width="30px"><span>惜心（伟祺）</span> 👍（4） 💬（1）<div>电阻、电容、晶体管，感觉是从器的层面做总结，不能很好的把握计算机的本质状态控制
用电阻、电容、电感，感觉会更好传递计算机理论层分层思想，这三个东西实现了、状态变化、状态存储、控制跳转，才有了后面的更复杂的各种计算、应用
Risc和cisc的差异，感觉是对控制元素的抽象、模块化认识的问题
Cisc感觉有点异性封装，强调更强的包容性
risc抽象更本质，把控制抽象成几个严格的模块，模块之间外在的格式形式也是固定的
所以导致它更容易模块化和乐高化的扩展出更多高层应用</div>2022-07-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/a6/a7/86c32422.jpg" width="30px"><span>飞鹤Plus</span> 👍（4） 💬（1）<div>老师讲的真好。请问老师最后“计算机历史大事记”的图是用什么软件画的，感觉很简洁。</div>2022-07-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/2a/2c/69/6d1a0c98.jpg" width="30px"><span>vampire</span> 👍（2） 💬（1）<div>通过流水线排布可以实现虚拟的并行，还只是在一个程序内部的指令级并行
通过多发射可以实现多个程序的并行，也就是程序级并行
通过多核可以实现多个处理器内核的并行执行，也就是业务级并行</div>2022-08-03</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/0f/d7/31d07471.jpg" width="30px"><span>牛年榴莲</span> 👍（2） 💬（1）<div>想起了被计算机系统结构支配的恐惧</div>2022-07-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/ff/7b/cbe07b5c.jpg" width="30px"><span>顾琪瑶</span> 👍（2） 💬（1）<div>看了下面的回答, 发现还要补充下流水线的基础知识才能回答和思考本篇的提问</div>2022-07-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/18/8b/c3/bf036d99.jpg" width="30px"><span>砥砺奋进</span> 👍（2） 💬（1）<div>指令流水线技术: 将指令拆分为多个流水线部分,有多少层级就可以有多少指令并行(但不是流水线级越多越多, 涉及流水线停顿等优化手段), 而指令的时钟周期由最复杂的流水线级操作决定, 所以RISC的精简指令可以最大化发挥cpu性能</div>2022-07-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1a/11/7c/bf5049b3.jpg" width="30px"><span>Freddy</span> 👍（2） 💬（1）<div>CISC, RISC, 以及x86现在的外CISC内RISC，都是时代场景的最优选择；</div>2022-07-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/29/a6/ad/e65aec4c.jpg" width="30px"><span>苏流郁宓</span> 👍（2） 💬（2）<div>RISC指令长度一致，有利于提高分支预测的能力而且也方便cpu计算单元与寄存器，缓存等进行数据交流</div>2022-07-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/21/36/e7/87812eb1.jpg" width="30px"><span>sun</span> 👍（1） 💬（1）<div>本来还以为是RISC指令更精简，粒度更小，可以更好的并行，所以更快。
看了评论区才明白，原来是因为RISC架构的指令时间一致，并行执行时所有指令没有空闲，形成完美的流水线，所以才比较快。</div>2022-10-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/36/bf/9ac3271c.jpg" width="30px"><span>夏学方</span> 👍（1） 💬（1）<div>其实各行业 在发展到不得不面对复杂任务时 都发展出自己的逻辑机械 比如看风水的罗盘 纺织工业的提花机</div>2022-08-15</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/18/84/0d/4e289b94.jpg" width="30px"><span>三生</span> 👍（1） 💬（1）<div>1.指令流水线，2.指令可以乱序执行，粒度小那就可以分割的更多，可以在多个流水线上执行</div>2022-07-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/27/a7/43/2ac6a876.jpg" width="30px"><span>学校资产已登记在册</span> 👍（1） 💬（1）<div>LMOS老师的课里cpu要实现乱序吗</div>2022-07-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/2c/c7/89/16437396.jpg" width="30px"><span>极客酱酱</span> 👍（1） 💬（1）<div>写的真好，言简意赅</div>2022-07-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/27/f8/2c/92969c48.jpg" width="30px"><span>青玉白露</span> 👍（1） 💬（1）<div>拓展阅读，了解代码运行的原理，https:&#47;&#47;zhuanlan.zhihu.com&#47;p&#47;362950660</div>2022-07-20</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTJ5WmAmuxTzKoln814dKIAia1KTUcgSSYzYgDIphlbv5dQpCuxrfRqodtXGMh7QtVUexCZE3CfYAgg/132" width="30px"><span>尹小白</span> 👍（0） 💬（1）<div>RISC-V</div>2022-12-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/61/b8/7b23f8cb.jpg" width="30px"><span>本来是亚</span> 👍（0） 💬（1）<div>流水线设计，将一条指令的运行拆分成多个阶段，从而使得同一时间内可以存在不同生命周期的指令</div>2022-11-06</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/8d/c6/e648d118.jpg" width="30px"><span>嗣树</span> 👍（0） 💬（1）<div>来晚啦，打个卡😀</div>2022-09-06</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/2a/36/c5d1a120.jpg" width="30px"><span>CLMOOK🐾</span> 👍（0） 💬（1）<div>我的理解是，在某个特定的cpu时钟周期内，cpu只能执行某个指令在其流水线里的某个阶段，并不能在这个时钟周期内同时执行另一个指令的某个阶段。同时执行或者只是&quot;假象&quot;，因为时钟周期变小了cpu的吞吐率变大了</div>2022-07-25</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1b/93/b6/a7c9facf.jpg" width="30px"><span>一路向前</span> 👍（0） 💬（1）<div>重拾计算机基础，加油！</div>2022-07-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/24/c2/791d0f5e.jpg" width="30px"><span>jeigiye</span> 👍（0） 💬（1）<div>dpu这种是什么芯片呢？是正在记录的历史吗？</div>2022-07-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1a/1e/de/cdee1780.jpg" width="30px"><span>我是内存</span> 👍（0） 💬（2）<div>冥冥之中感觉流水线越多越好，但是是如何确定具体的数量的呢，多少条线算好呢，还是不太理解</div>2022-07-22</li><br/><li><img src="" width="30px"><span>nmg</span> 👍（0） 💬（1）<div>是只有risc-v cpu才能并行执行指令吗？</div>2022-07-21</li><br/>
</ul>