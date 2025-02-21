你好，我是LMOS。

上节课，我带你见证了两种计算机指令集的设计结构——CISC与RISC。而今天我们的“主角”就是RISC中的一个代表性特例，它就是RISC-V。

作为未来芯片指令集的主流，RISC-V是今后芯片设计的最佳方案，甚至可以说它就是硬件行业里的Linux。

为什么这么说呢？这节课，我会从RISC-V发展历史、原理与技术特性几个方面入手，带你弄明白为什么RISC-V在半导体行业中发展得如此迅猛。

### RISC-V从何而来

让我们“穿越时空”，把时间线拉回到2010年。在加州伯克利分校的校园中，Krste Asanovic教授正为了学生们学习计算机架构而发愁。由于现存芯片指令集冗余且专利许可费用昂贵，还有很多IP法律问题，没有一款合适的CPU用于学习。

于是他想要带领一个研究团队，来设计一款用于学生学习的CPU。研究团队在选择架构的时候，对比了传统已经存在的ARM、MIPS、SPARC以及x86架构等，发现这些架构指令集要么极其复杂，要么极其昂贵。所以，他们的研究团队最终决定设计一套全新的指令集。

这个研究团队最开始只有4个人，却在三个月之内完成了指令集原型开发，其能力可见一斑。后来，这个项目被计算机体系结构方面的泰斗 David Patterson 发现，并且得到了他的大力支持。
<div><strong>精选留言（30）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/16/e8/c9/59bcd490.jpg" width="30px"><span>听水的湖</span> 👍（22） 💬（1）<div>又见面啦，我是这门课的编辑小新。

以下是下节课的预告和“预习作业”：

下个模块开始手写CPU啦（8月1日更新），我们这次用Verilog语言写。老师正奋战中，把配套代码等等都为大家准备上，大伙儿可以趁等待更新这周吸收消化下前两节课。

还可以看看下面的“预习”作业：

1.第一季也有一篇内容稍微涉及了一点Verilog语言，代码也不多，会带你实现一个可以计算任意 N 位二进制数的 ALU。迫不及待的同学可以先行去瞅瞅，找个感觉：https:&#47;&#47;time.geekbang.org&#47;column&#47;article&#47;409790

2.也许你之前并没接触过硬件语言，但对比学习大法还是很不错的。可以先自行思考一下Verilog语言和我们熟悉的软件编程所用语言有哪些不同，带着疑问学习，效果加倍哦。答案我们将在后面揭晓！</div>2022-07-25</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/52/40/e57a736e.jpg" width="30px"><span>pedro</span> 👍（45） 💬（8）<div>为什么riscv需要定义不同的特权级？

这并不是riscv独有的，让我们把注意力回到老朋友intel上。

事实上，cpu刚出现的那段时间里，压根就没有特权级这个概念，任何人都是实打实土皇帝，但是这样怎么管理？应用程序之间经常打架斗殴，搞不好还把机器搞垮了。

然后inter的那帮人就搞出了一个特权级的概念，你虽然想打架，但我不准你打，你出手，我就红牌，然后大家都老实了，系统运行就很稳定了。

说了这么多，特权级无非是让大家守规矩，讲安全，和谐共生。</div>2022-07-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/28/02/88/df790e16.jpg" width="30px"><span>lifetime</span> 👍（4） 💬（1）<div>问个小白才会问到的问题？
硬件CPU的“源代码”指的是什么？
对于ARM是售卖“源代码”存活的，那么它的“源代码”是指指令集的定义，寄存器的定义，特权级的定义吗，以及如何实现特权级的转换，寄存器如何使用等的规范？
我觉得是不是除了这些规范，还会包含CPU的内部结构，那些晶体管的摆放和连接设计图纸呀？</div>2022-10-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/88/9c/cbc463e6.jpg" width="30px"><span>仰望星空</span> 👍（3） 💬（1）<div>为什么RISC-V要定义特权级？主要是为了系统能稳定和安全的运行，设想一下如果没有特权级，任何应用都能任意访问所有硬件，这必将会是一场灾难</div>2022-07-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/2a/af/28/9ffc55a2.jpg" width="30px"><span>可爱因子1/n</span> 👍（3） 💬（1）<div>就像老师上课讲到的，设置特权级就是给指令加上了权力，这样的话应用程序所执行的指令就只能做自己权利范围以内的事情，避免对其他的应用程序产生不必要的干扰和破坏，维持这个生态的稳定和平衡
</div>2022-07-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/27/f8/2c/92969c48.jpg" width="30px"><span>青玉白露</span> 👍（3） 💬（1）<div>特权级是为了能够实现资源隔离、权限管理所设置的。之后实现的操作系统就需要用到他</div>2022-07-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/29/a6/ad/e65aec4c.jpg" width="30px"><span>苏流郁宓</span> 👍（2） 💬（1）<div>俺觉得特权级区分用户软件与操作系统功能，在操作系统那边讲过，亮点应该是硬件线程，任意时刻只能运行在一个特权级上。这算不算是在安全与好用上做平衡？算不算是RISCv指令集对cpu发展的贡献？</div>2022-07-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/4c/b3/931dcd9e.jpg" width="30px"><span>J</span> 👍（2） 💬（1）<div>RISC-V定义特权级，有助于保护系统资源不被滥用和破坏，不会因为低特权程序的bug或恶意代码破坏环境。</div>2022-07-20</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTJ5WmAmuxTzKoln814dKIAia1KTUcgSSYzYgDIphlbv5dQpCuxrfRqodtXGMh7QtVUexCZE3CfYAgg/132" width="30px"><span>尹小白</span> 👍（1） 💬（1）<div>开放，简单，模块化</div>2022-12-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/25/31/d2/40338b73.jpg" width="30px"><span>揭晓林</span> 👍（1） 💬（1）<div>老师和同学们好，我这边想补充两个点：

1. 在RSIC-V因何流行那里，老师写的是“之前硬件和软件一样，都是小心地保护自己的 “源代码” ”这里是否将“硬件”和“软件”互换位置更顺畅一点？因为后面讲的是“直到后来，软件界出现了开源的 Linux”

2. 评论区有人评论特权级是如何切换的：我在B站看哈工大的操作系统课程时，第5讲里说到是用段寄存器来实现的，CPL（Current Privilege Level    当前的特权级） 和 DPL （Descriptor Privilege Level，目标段）。在操作系统启动的时候会初始化好。当用户程序执行的时候，会判断两个寄存器的值。</div>2022-10-15</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/55/df/6dfd3cde.jpg" width="30px"><span>杨景胜</span> 👍（1） 💬（2）<div>催更催更催更</div>2022-07-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/68/83/ecd4e4d6.jpg" width="30px"><span>WGJ</span> 👍（0） 💬（1）<div>这个特权级是怎么切换的呢，如果是通过控制和状态寄存器控制，那是不是不同应用的寄存器的特权标志是有区别的，像操作系统的特权级是0，其他应用就是3，是这么区分的吗</div>2022-08-30</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1b/6b/2c/b27eefc5.jpg" width="30px"><span>Abcd</span> 👍（0） 💬（1）<div>关于 CPU 通用寄存器的保存问题，有的寄存器需要caller保存，有的需要callee保存，能举个例子吗？</div>2022-08-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/2b/89/50/aee9fdab.jpg" width="30px"><span>小杰</span> 👍（0） 💬（1）<div>每个模块，每个指令，做自己应该要做的事，不然就乱套了。</div>2022-08-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/88/57/0526d6c8.jpg" width="30px"><span>Lpc-Win32</span> 👍（0） 💬（1）<div>实模式、保护模式</div>2022-08-01</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/17/f3/2d/1a5f7542.jpg" width="30px"><span>0ver10@d</span> 👍（0） 💬（1）<div>排除虚拟化的应用场景,对于多核处理器理论上有没有可能一个核运行在高特权级,一个核运行在低特权级?</div>2022-07-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/2a/ec/06/4494ecde.jpg" width="30px"><span>jk001</span> 👍（0） 💬（1）<div>这几天怎么没更新？</div>2022-07-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/7a/21/a33cc944.jpg" width="30px"><span>熊出没</span> 👍（0） 💬（1）<div>权级设置是为了从杂乱中设置秩序 否则硬件资源就会被无序使用 导致机器崩溃</div>2022-07-25</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/18/8b/c3/bf036d99.jpg" width="30px"><span>砥砺奋进</span> 👍（0） 💬（1）<div>不得不说 彭老师这思维导图真心到位</div>2022-07-25</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/e5/56/3bee284c.jpg" width="30px"><span>落叶🍂建良</span> 👍（0） 💬（1）<div>为什么设置特权级？
从业务角度来理解，应该就是权限管理，特权级就是管理员，其他的属于不同的角色，拥有不同的权限，目的是为了系统的安全和稳定</div>2022-07-25</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTJIGLdWEhYTSa6ibdibOpUISmXqSmBIoPEKaEQPrafA2jvNiaWkuEhWvyAzr3icrN8NuGUViaRIsfpO76A/132" width="30px"><span>Geek_53914b</span> 👍（0） 💬（1）<div>同一时间只能运行在一个特权级，那不就不会冲突了吗？不同时间特权级来回切换不更乱？</div>2022-07-24</li><br/><li><img src="" width="30px"><span>nmg</span> 👍（0） 💬（1）<div>今天没有更新吗，今天是周五啊</div>2022-07-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/17/37/2b/b32f1d66.jpg" width="30px"><span>Ball</span> 👍（0） 💬（1）<div>设定特权级别主要为了适应分时操作系统的全局调度操作，部分系统资源的访问权限收敛到一个地方，方便解决冲突和提高资源利用率</div>2022-07-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/67/49/da88c745.jpg" width="30px"><span>小虞</span> 👍（0） 💬（1）<div>老师怎么看基于RISC-V的XiangShan (香山)开源处理器</div>2022-07-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/20/5b/d7/d88c1850.jpg" width="30px"><span>和某欢</span> 👍（0） 💬（1）<div>设置特权级是为了保护操作系统资源，不被上层应用程序滥用资源导致系统崩溃</div>2022-07-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/24/c2/791d0f5e.jpg" width="30px"><span>jeigiye</span> 👍（0） 💬（1）<div>”特权”就相对“一般”，他们都为程序服务，应用、服务、驱动、操作系统都程序，但程序也有分层，地层服务上层，比如操作系统为应用服务，这样操作系统就要稳定，一些危险操作或是控制就只能操作系统运行，即“特权”</div>2022-07-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/25/87/f3a69d1b.jpg" width="30px"><span>peter</span> 👍（0） 💬（2）<div>请教老师几个问题：
Q1：CPU为什么不多造一些寄存器？
CPU的寄存器好像数量不多，为什么不多造几个寄存器呢，比如造一百个，
这样不就速度快了吗？寄存器数量少，是因为制造难度大？还是因为成本高？
或者是没有必要造那么多？
Q2：“需要保存的寄存器”，什么意思？
Q3：RV特权级，0是最高特权、3是最低特权吗？</div>2022-07-21</li><br/><li><img src="" width="30px"><span>nmg</span> 👍（0） 💬（1）<div>虽然理解特权级别是为了资源合理分配，不被滥用，但是还是想不到这种特权级，在硬件上是如何实现的</div>2022-07-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/56/60/17bbbcf3.jpg" width="30px"><span>softbaddog</span> 👍（0） 💬（1）<div>特权设计肯定就是为了安全，但所谓合久必分，分久必合。说不定哪天又冒出一个新架构，打破了现有权限等级，将权限放到OS中，自身追求极致精简。</div>2022-07-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1e/99/b9/96261f86.jpg" width="30px"><span>沙里飞</span> 👍（0） 💬（1）<div>开源软件, 和开源硬件内容不同, 本质上有相似的理念. 成本&#47;利润是商业的重要出发点
1. 开源
2. 可定制, 可控; 适用领域广泛, 避免捆绑销售, 节省成本
3. 需要的行业规范, 业界标准. RISC-V基于&quot;前人&quot;的基础, 没有过多的历史包袱
4. 行业发展趋势本身; 去中心化, 去耦合, 软件定义; 感觉都是信息从一个量级到另外一个量级变化过程中的必然结果</div>2022-07-20</li><br/>
</ul>