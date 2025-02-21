前面几讲里，我从两个不同的部分为你讲解了CPU的功能。

在“**指令**”部分，我为你讲解了计算机的“指令”是怎么运行的，也就是我们撰写的代码，是怎么变成一条条的机器能够理解的指令的，以及是按照什么样的顺序运行的。

在“**计算**”部分，我为你讲解了计算机的“计算”部分是怎么执行的，数据的二进制表示是怎么样的，我们执行的加法和乘法又是通过什么样的电路来实现的。

然而，光知道这两部分还不能算是真正揭开了CPU的秘密，只有把“指令”和“计算”这两部分功能连通起来，我们才能构成一个真正完整的CPU。这一讲，我们就在前面知识的基础上，来看一个完整的CPU是怎么运转起来的。

## 指令周期（Instruction Cycle）

前面讲计算机机器码的时候，我向你介绍过PC寄存器、指令寄存器，还介绍过MIPS体系结构的计算机所用到的R、I、J类指令。如果我们仔细看一看，可以发现，计算机每执行一条指令的过程，可以分解成这样几个步骤。

1.**Fetch**（**取得指令**），也就是从PC寄存器里找到对应的指令地址，根据指令地址从内存里把具体的指令，加载到指令寄存器中，然后把PC寄存器自增，好在未来执行下一条指令。

2.**Decode**（**指令译码**），也就是根据指令寄存器里面的指令，解析成要进行什么样的操作，是R、I、J中的哪一种指令，具体要操作哪些寄存器、数据或者内存地址。
<div><strong>精选留言（30）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/0f/50/4a/04fef27f.jpg" width="30px"><span>kdb_reboot</span> 👍（11） 💬（1）<div>很喜欢这几章；大二时学数电，期末考了93分，但是仍然不知道它能做什么用，内心有困惑，但是也没更多的坚持这个问题；感谢你</div>2019-06-06</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/23/66/413c0bb5.jpg" width="30px"><span>LDxy</span> 👍（165） 💬（6）<div>CPU在空闲状态就会停止执行，具体来说就是切断时钟信号，CPU的主频就会瞬间降低为0，功耗也会瞬间降低为0。由于这个空闲状态是十分短暂的，所以你在任务管理器里面也只会看到CPU频率下降，不会看到降低为0。当CPU从空闲状态中恢复时，就会接通时钟信号，这样CPU频率就会上升。所以你会在任务管理器里面看到CPU的频率起伏变化。这个知识也是我找工作面试时才学到的。</div>2019-06-04</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTJEbZZ65d5ibzjadyKq6Odjs5eeSJGwxnfBAv7gKjp6vG5GUdz9YrXq54KZeAEsS1OfahWVZurXODg/132" width="30px"><span>Akizuki</span> 👍（61） 💬（0）<div>操作系统内核有 idle 进程，优先级最低，仅当其他进程都阻塞时被调度器选中。idle 进程循环执行 HLT 指令，关闭 CPU 大部分功能以降低功耗，收到中断信号时 CPU 恢复正常状态。</div>2019-06-05</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/8e/72/63c94eee.jpg" width="30px"><span>黄马</span> 👍（45） 💬（0）<div>uptime 命令查看平均负载
满载运行就是平均负载为1.0(一个一核心CPU)
定义为特定时间间隔内运行队列中的平均线程数。load average 表示机器一段时间内的平均load。
这个值越低越好。负载过高会导致机器无法处理其他请求及操作，甚至导致死机

当CUP执行完当前系统分配的任务，为了省电，系统将执行空闲任务（idle task），这个任务循环执行HLT指令，CPU就会停止指令的执行，并且让CPU处于HALT状态,CPU虽然停止指令执行，并且CPU的部分功能模块将会被关闭（达到降低功耗的目的），但是CPU的LAPIC（Local Advanced Programmable Interrupt Controller）并不会停止工作，即CPU将会继续接收外部中断、异常等外部事件（事实上，CPU HALT状态的退出将由外部事件触发）.当CPU接收到这些外部事件的时候，将会从HALT状态恢复回来，执行中断服务函数，并且当中断服务函数执行完毕后，指令寄存器（CS:EIP）将会指向HLT指令的下一条指令，即CPU继续执行HLT指令之后的程序</div>2019-10-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/e7/2e/1522a7d6.jpg" width="30px"><span>活的潇洒</span> 👍（26） 💬（2）<div>要想成功三个动作很重要
1、做出来
2、写出来
3、讲出来
三个非常重要，缺一不可

day17 笔记：https:&#47;&#47;www.cnblogs.com&#47;luoahong&#47;p&#47;11330406.html
</div>2019-08-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/17/0a/5f/5ee0221d.jpg" width="30px"><span>roger</span> 👍（19） 💬（0）<div>程序计数器一直在变化，就是满载吧，持续不变就是idle。CPU密集型任务需要CPU大量计算的任务，这个时候CPU负载就很高，IO密集型任务，CPU一直在等待IO，就会有idle。</div>2019-08-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/85/bf/5c5e86bb.jpg" width="30px"><span>旺旺</span> 👍（15） 💬（1）<div>cpu执行速度非常快，消耗性能资源也比较快。但实际上，电脑并不是时刻都需要进行大量运算。

所以，CPU需要一种“闲置”状态，来平衡这种矛盾（需要忙时，可以全速奔跑；暂无事务时，又可节能地随时待命。）

“Idle 闲置”是一种低功耗的状态，cpu在执行最低功耗的循环指令。实际上并非啥都没干，而是一直在干最最轻松的事儿。
</div>2019-06-04</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1d/9a/89/babe8b52.jpg" width="30px"><span>A君</span> 👍（9） 💬（0）<div>所谓构建数据通路，就是把各种组建通过线路组合起来，让他们可以完成数据存储、处理和传输的操作。数据处理部分自然是交给ALU组合逻辑计算元件，它是由大量运算器组合而成；数据存储自然是交给各种寄存器，存储的数据除了有计算数据外，还有各种状态，以及指令的地址；负责读取指令，将指令转换成电信号的就是译码器；为了让fetch-decode-execute这个循环体运作下去，还需要一个自动设备。</div>2020-06-25</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/dd/a8/fc96fb89.jpg" width="30px"><span>九云</span> 👍（7） 💬（3）<div>指令周期、时钟周期2个概念就够了。引入CPU周期这个概念，要解释什么问题呢？</div>2019-11-15</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/a5/98/a65ff31a.jpg" width="30px"><span>djfhchdh</span> 👍（6） 💬（0）<div>cpu满载和空闲的分别主要是操作系统调度任务导致的，如果操作系统调度了一个高优先级的任务，那么cpu就优先执行这个任务即满载，如果操作系统调度了一个低优先级的idle任务，那么cpu就执行这个idle任务，显示为空闲状态，空闲即假装“没事做”，其实当有其他更高优先级的任务调度时，就可以抢占它，去执行更高优先级的任务</div>2019-06-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/97/46/fe1f21d8.jpg" width="30px"><span>北风一叶</span> 👍（3） 💬（2）<div>指令周期由：取得指令，指令译码，执行指令三个步骤的不断循环组成，其中取指令和指令译码由控制器负责，执行指令由运算器负责。一个指令周期由多个CPU周期构成，而一个CPU周期又由多个时钟周期构成，这一部分感觉说的有点混乱。</div>2020-03-03</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/ce/cd/3753de4d.jpg" width="30px"><span>爱与自由</span> 👍（2） 💬（0）<div>看了一下评论，都没讲到重点，很多还偏题了，讲到操作系统，线程撒的，注意了：这节课的重点是cpu 是这样几个组件组成的。ALU运算器，寄存器，PC计数器，译码器这几个物理组件(生产线上的4 个工人)共同完成一个工厂流水线产品（一条指令的完整执行，也就是拿到计算后的结果，且是按时间有序地源源不断的生产产品，因为指令是一条一条执行的，比如产品 A（指令A:包含4个步骤），产品 B（包含4个步骤），且4个步骤花的时间不等，ALU 执行命令的时间远小于取指令时间），比如A指令取指令的时候，ALU 空闲，A指令执行的时候，译码器空闲。。。那么这几个组件工作就不饱满，老板不会满意的，狠不得每个工人每时每刻都不能休息，榨干你才是老板愿意看到的事情。要达到这点，就需要A，B指令从同步串行改为并行，也就是A指令在执行的时候，译码器空闲，那么译码器可以读取B指令进行译嘛，把B指令的前工序提前准备好，一旦A指令执行完成，释放占有的资源ALU，那么B指令可以马上执行，不必等到取指令，译码的过程(因为提前完成了)，几个工人工作饱和了，每时每刻都没闲着，节约了时间</div>2023-06-16</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/83/c9/5d03981a.jpg" width="30px"><span>thomas</span> 👍（2） 💬（0）<div>每一条指令都需要从内存里面加载而来，所以我们一般把从内存里面读取一条指令的最短时间，称为 CPU 周期
------------------------------------&gt;
为什么要加上最短？</div>2021-07-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1d/9a/89/babe8b52.jpg" width="30px"><span>A君</span> 👍（2） 💬（0）<div>因为cpu访问寄存器、cache、内存、硬盘的速度不同，为了不让宝贵的cpu资源浪费在数据传输过程中，因此引入中断，当cpu在访问硬盘等低速设备时可以将任务切换去，执行其他任务。如果不考虑进程调度策略、进程优先级等因素，如果几乎所有任务都是在做计算，那么cpu就会处在满载状态，如果当下没有任务在进行，操作系统就会切换ideal进程，该进程会主动挂起自己，所以说，虽然cpu当前在处理ideal任务，但并不会真正在读取处理传输数据。</div>2020-06-25</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/b5/98/ffaf2aca.jpg" width="30px"><span>Ronnyz</span> 👍（2） 💬（0）<div>满载就是执行高优先级任务，不会被中断；空闲就是执行的任务优先级较低，可以被中断</div>2019-11-25</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/59/f6/ed66d1c1.jpg" width="30px"><span>chengzise</span> 👍（2） 💬（0）<div>CPU 还会有满载运行和 Idle 闲置的状态, 指的系统层面的状态。即使是idle空闲状态，cpu也在执行循环指令
</div>2019-06-03</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/20/0c/4d/90ab20d8.jpg" width="30px"><span>Nuvole Bianche</span> 👍（1） 💬（0）<div>又一个疑问，原文：“我们通过数据总线的方式，把它们连接起来，就可以完成数据的存储、处理和传输了“，请问其中“数据总线的方式”具体是什么方式或者怎么理解吗？</div>2022-10-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/2c/83/f85ba9cd.jpg" width="30px"><span>once</span> 👍（1） 💬（2）<div>老师 前面你说了 访问内存很慢 从内存中取出指令至少需要一个cpu周期 但是执行指令相对于从内存中取出指令应该会快很多吧 为什么也要至少一个cpu周期呢</div>2019-11-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/9a/e3/0a094b50.jpg" width="30px"><span>Wales</span> 👍（0） 💬（0）<div>IDLE应该是在循环里空转，也就是不断地跳转到某个地址，往下走两步非ALU指令，然后再跳回起点无限循环，这没什么价值。

BUSY应该是让ALU进行运算获得结果，指导下一步的指令执行。</div>2023-11-04</li><br/><li><img src="" width="30px"><span>Geek_88604f</span> 👍（0） 💬（1）<div>CPU的架构牛逼啊。ALU和存储器是不同的独立电路，这和当前大数据存算分离架构如出一辙。CPU里面的自动执行电路就是大数据里面的任务编排和调度。原来现在看起来牛逼的架构都是以前玩剩下的。</div>2023-10-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/07/2b/d111e75d.jpg" width="30px"><span>Lion</span> 👍（0） 💬（0）<div>cpu密集型和io密集型</div>2022-12-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/50/2b/2344cdaa.jpg" width="30px"><span>第一装甲集群司令克莱斯特</span> 👍（0） 💬（0）<div>学起来！</div>2022-12-20</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTKylFSbosgp8gP4HtYdsFg27BeUkYnsQS3ShbibCk0mrVuOVeicqIL6MZ6r42I6nuWLtDwtIPvkzC0A/132" width="30px"><span>Geek_b0d83e</span> 👍（0） 💬（0）<div>指令周期（取指令+执行）&gt;=2*CPU周期&gt;时钟周期</div>2022-10-20</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/DYAIOgq83ert8WynVde6etxoVLry5cKiaiaV5TkNv3fE9Xe33AvwULZJsIoZFzica2LiccfDB4ic4vfibWax14wfB7lA/132" width="30px"><span>woodie</span> 👍（0） 💬（0）<div>总结：
1、掌握指令周期、CPU周期(机器周期)、时钟周期、CPI、CPU主频的联系和区别
指令周期：包括获取指令=&gt;指令解码=&gt;指令执行
CPU周期(机器周期)：一个指令周期包括多个CPU周期
时钟周期时间：主频的倒数
CPI：每条指令的平均CPU时钟周期数
2、CPU包括四类基础电路：ALU(根据输入计算输出)、锁存器和D触发器(进行状态读写)、&quot;自动&quot;电路、“译码”器</div>2022-09-26</li><br/><li><img src="" width="30px"><span>Geek_964a1d</span> 👍（0） 💬（0）<div>指令缓存可以预热吗？就是提前把内存中的一段 指令 都放在 缓存中，这样，就不用每次都去内存中取指？ </div>2022-07-04</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/28/3d/8b/47bcc851.jpg" width="30px"><span>何同一</span> 👍（0） 💬（0）<div>所有进程都阻塞时 cpu 执行 idle 指令</div>2022-02-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/8a/b0/6ab66f1b.jpg" width="30px"><span>牛金霖</span> 👍（0） 💬（0）<div>Cpu-Cycle的大小是否也和内存的频率有关呢</div>2021-11-04</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/GbZRicqbu1QJmlcOlfLyW48OPaMmcKSO6zeZaKkc2uFiaLYOysibTKMtrOvOpHvlSHulHUatKX7lVcrENibqCmGhwQ/132" width="30px"><span>18736297414</span> 👍（0） 💬（0）<div>计算机执行的基本流程是Fetch,Decode,Excute。
4 种基本电路。它们分别是，ALU 这样的组合逻辑电路、用来存储数据的锁存器和 D 触发器电路、用来实现 PC 寄存器的计数器电路，以及用来解码和寻址的译码器电路。</div>2021-08-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/d4/f3/129d6dfe.jpg" width="30px"><span>李二木</span> 👍（0） 💬（0）<div>CPU 需要的 4 种基本电路:
1) ALU 这样的组合逻辑电路、
2) 用来存储数据的锁存器和 D 触发器电路
3) 用来实现 PC 寄存器的计数器电路，
4) 解码和寻址的译码器电路</div>2021-04-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/f9/88/cdda9e6f.jpg" width="30px"><span>阳仔</span> 👍（0） 💬（1）<div>PC寄存器会自动取指令，即会自动自增，那它会溢出么？</div>2021-02-05</li><br/>
</ul>