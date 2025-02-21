上一讲，我们看到，要能够实现一个完整的CPU功能，除了加法器这样的电路之外，我们还需要实现其他功能的电路。其中有一些电路，和我们实现过的加法器一样，只需要给定输入，就能得到固定的输出。这样的电路，我们称之为**组合逻辑电路**（Combinational Logic Circuit）。

但是，光有组合逻辑电路是不够的。你可以想一下，如果只有组合逻辑电路，我们的CPU会是什么样的？电路输入是确定的，对应的输出自然也就确定了。那么，我们要进行不同的计算，就要去手动拨动各种开关，来改变电路的开闭状态。这样的计算机，不像我们现在每天用的功能强大的电子计算机，反倒更像古老的计算尺或者机械计算机，干不了太复杂的工作，只能协助我们完成一些计算工作。

这样，我们就需要引入第二类的电路，也就是**时序逻辑电路**（Sequential Logic Circuit）。时序逻辑电路可以帮我们解决这样几个问题。

第一个就是**自动运行**的问题。时序电路接通之后可以不停地开启和关闭开关，进入一个自动运行的状态。这个使得我们上一讲说的，控制器不停地让PC寄存器自增读取下一条指令成为可能。

第二个是**存储**的问题。通过时序电路实现的触发器，能把计算结果存储在特定的电路里面，而不是像组合逻辑电路那样，一旦输入有任何改变，对应的输出也会改变。
<div><strong>精选留言（30）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/16/8b/3a/e1625b86.jpg" width="30px"><span>LeeLink</span> 👍（17） 💬（4）<div>这一部分真一点没看懂，好头疼。</div>2020-01-05</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/DYAIOgq83erTlRJ6skf7iawAeqNfIT1PPgjD7swUdRIRkX1iczjj97GNrxnsnn3QuOhkVbCLgFYAm7sMZficNTSbA/132" width="30px"><span>senekis</span> 👍（15） 💬（2）<div>老师的课程很精彩，以前都没有好好学，看了受益匪浅，《编码：隐匿在计算机软硬件背后的语言》
和《数字逻辑应用与设计》这两本书都买了，一定要坚持看完啊！！！
</div>2019-06-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/ba/01/5ce8ce0b.jpg" width="30px"><span>Leoorz</span> 👍（5） 💬（1）<div>今天用一天的时间读了《编码：隐匿在计算机软硬件背后的语言》关于触发器的章节，仔仔细细地每个图都自己分析并画了好几遍，终于把level-triggered&#47;edge-triggered D-type flip-flop搞清楚了
分频书中有讲，采用多个 edge-triggered 触发器级联的方式，~Q作为反馈信号输入至D，并将上一级触发器的~Q作为当前触发器的CLK信号输入，Q输出即为降频的时钟信号
倍频这个暂时不清楚，待继续学习</div>2020-01-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/be/02/43202976.jpg" width="30px"><span>w 🍍</span> 👍（3） 💬（2）<div>“如果这个时候，我们让 R 和 S 的开关，也用一个反相器连起来” 这有什么用，不是很明白</div>2019-09-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/76/23/31e5e984.jpg" width="30px"><span>空知</span> 👍（28） 💬（4）<div>接通R 断开S  结果是 1 RS触发器的真值表 是不是写反了呀</div>2019-06-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1a/bc/6d/e6e2329f.jpg" width="30px"><span>linxi</span> 👍（19） 💬（3）<div>“打开”、“关闭”、“合上”这些词语有时候真的会产生歧义，建议用“闭合”、“断开”这样的词</div>2021-10-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/17/95/af/b7f8dc43.jpg" width="30px"><span>拓山</span> 👍（12） 💬（1）<div>编码一书看完了 这段内容理解的比较容易</div>2019-10-04</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/ca/e3/447aff89.jpg" width="30px"><span>记事本</span> 👍（7） 💬（3）<div>上大学的时候就学习过触发器，那会儿压根就不知道触发器是做什么用的…谢谢老师！</div>2019-10-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1d/9a/89/babe8b52.jpg" width="30px"><span>A君</span> 👍（6） 💬（0）<div>时钟信号用个非门就可以构建，反馈电路还可以用于两两组合做成记忆电路，所谓记忆电路，就是电路会持续输出上次电路改动时的输出结果。</div>2020-06-25</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/23/66/413c0bb5.jpg" width="30px"><span>LDxy</span> 👍（6） 💬（0）<div>n分之一分频器可以使用n进制计数器实现，n进制计数器的进位输出端的频率即为输入时钟信号频率的n分之一。
n倍频器可以由锁相环加n分之一分频器实现。锁相环是一个反馈环路，这个环路里面有一个叫鉴相器的部件，外部输入信号f0会进入鉴相器，同时锁相环输出端的信号f1也会反馈到鉴相器的另一个输入端，鉴相器会比较f0与f1的相位差，输出一个变化的电压信号去控制锁相环的其他部件，从而调整输出信号f1的频率。总的来说，锁相环的基本功能就是使得输出端的信号f1与输入端信号f0的相位差维持恒定，所以名为「锁相环」。如上所述，如果f1直接反馈回到鉴相器，为了维持相位差恒定，会有输出信号f1=f0。如果将f1经过n分之一分频器得到信号f2再反馈回到鉴相器，即将f2=f1&#47;n与f0输入鉴相器比较相位。此时，为了维持f2与f0的相位差恒定，鉴相器会输出一个电压信号控制锁相环的其他部件，调整输出信号f1，使得f0=f2。此时，锁相环的输出信号f1=n*f2=n*f0。从而实现n倍频。</div>2019-06-05</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/16/5b/83a35681.jpg" width="30px"><span>Monday</span> 👍（3） 💬（3）<div>1、或非门的真值表图，表示看不懂，不应该如下吗？
   输入1  输入2  结果 
   0      0       1
   0      1        0
   1       0       0
   1       1        0
2、RS触发器真值表，也有问题吧，正确的我理解如下：
   S     R     Q 
   0      0     Q
   0      1      1
   1       0     0
   1       1      0</div>2020-05-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/17/42/50/4914d4fa.jpg" width="30px"><span>浮夸，</span> 👍（3） 💬（0）<div>D触发器实战😄</div>2020-01-04</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/79/0b/4346a253.jpg" width="30px"><span>Ant</span> 👍（3） 💬（0）<div>囫囵吞枣的看了，晶体振荡器的实现原理</div>2019-06-05</li><br/><li><img src="https://wx.qlogo.cn/mmopen/vi_32/DYAIOgq83eqLcWH3mSPmhjrs1aGL4b3TqI7xDqWWibM4nYFrRlp0z7FNSWaJz0mqovrgIA7ibmrPt8zRScSfRaqQ/132" width="30px"><span>易儿易</span> 👍（3） 💬（2）<div>老师，最后一张图，加入反向器之后，不太明白如何用信号D同时控制R-S两个开关……看了之前反向器的介绍，还是没理解……是D输入0之后，R收到1，S收到0，D输入1，R收到0，S收到1吗？</div>2019-06-05</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTKkzrezV2dOBAgickt9DLzabz3dNFYyDEVXENMQ5ibrWhFbFqXIOia3ZaR21pozvB7UfoxJx4Ar688sA/132" width="30px"><span>开心</span> 👍（2） 💬（1）<div>没有时钟信号也可以存储了呀，时钟信号在这里的作用是什么呢~</div>2019-06-19</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/IPdZZXuHVMibwfZWmm7NiawzeEFGsaRoWjhuN99iaoj5amcRkiaOePo6rH1KJ3jictmNlic4OibkF4I20vOGfwDqcBxfA/132" width="30px"><span>鱼向北游</span> 👍（2） 💬（0）<div>分频用计数器就可以吧 从0开始计数模n 归零就来个输入 应该根据此原理用d触发器+计数器有优化的方法
倍频数学的方法叫时域信号傅里叶级数展开到频域 然后滤波器滤专门那个频滤
电路的方法我编不下去了。。。
老师解答吧</div>2019-06-05</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/ef/19/ba159b8c.jpg" width="30px"><span>🗿顾晓峰🈹🈳🈴🈷🎏</span> 👍（1） 💬（1）<div>买一本CSAPP就可以了，其他上网查一下。</div>2019-10-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/87/62/f99b5b05.jpg" width="30px"><span>曙光</span> 👍（1） 💬（1）<div>老师： 1 SR真值表貌似反了；2 S和R都为1时，Q分析结果是0吧，为什么是NA</div>2019-10-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/79/4b/740f91ca.jpg" width="30px"><span>-W.LI-</span> 👍（1） 💬（0）<div>老师好!我虽然是计算机专业的，就是那种计组，操作系统这些课大几学的都不知道那种。现在回头学从哪本开始看好啊。不过你的课能看懂就是有点费力，理解不深脱了课件自己想回忆就费力。</div>2019-06-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/2b/96/a7/a9bfe8d3.jpg" width="30px"><span>漂泊者</span> 👍（0） 💬（0）<div>读了两天，每天一小时，看懂了</div>2024-01-20</li><br/><li><img src="" width="30px"><span>Geek_88604f</span> 👍（0） 💬（0）<div>组合逻辑电路:根据输入计算输出；时序逻辑电路:不停地切换01信号。</div>2023-10-31</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/30/a7/bd/791d0f5e.jpg" width="30px"><span>齐sir</span> 👍（0） 💬（0）<div>晶振就是指的电路层面的自动开关吗？我一直以为真的是有个晶体在振动🤪😅</div>2023-02-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/2d/a8/0a/791d0f5e.jpg" width="30px"><span>Nolan</span> 👍（0） 💬（0）<div>第一个时钟周期，
当D=1、CLK高电平时，与门输出取决于各自输入，此时S=1、R=0，输出Q被设置为1；
当D=1、CLK低电平时，与门输出必为0，此时S=0、R=0，输出Q保持上个状态1；

第二个时钟周期，
当D=0、CLK高电平时，与门输出取决于各自输入，此时S=0、R=1，输出Q被重置为0；
当D=0、CLK低电平时，与门输出必为0，此时S=0、R=0，输出Q保持上个状态0；

也就是说，在一个时钟周期内，输入一个信号D，就能存储信号D。
换个存储的地址，在下一个时钟周期就能保存下一组

（作者的真值表写错了，Set为1、设置Q=1；Reset为1，重置Q=0）</div>2023-02-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/78/4c/61018b26.jpg" width="30px"><span>Suwian</span> 👍（0） 💬（0）<div>RS触发器的，R跟S应该是搞反了，R：Reset，S：Set，R用来做复位操作，所以R输入高电平，Q应该为0的</div>2022-12-16</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/EIxfye0noElD6CgfvHgByRN9ics8hGENNBRuibSmXqeMNakF0BpN8RWpXUWcd8v2Wp8N7bqd9mDia5n8PH2qeUySA/132" width="30px"><span>云龙</span> 👍（0） 💬（0）<div>时钟信号在这里有什么用处</div>2022-09-16</li><br/><li><img src="" width="30px"><span>Geek3340</span> 👍（0） 💬（0）<div>刚开始把反相器看成二极管了哈哈 我寻思这不是一直导通吗</div>2022-07-28</li><br/><li><img src="" width="30px"><span>Geek_964a1d</span> 👍（0） 💬（0）<div>谢谢老师。大学就学过，但是一直不知道应用在哪里。通过这门课，把操作系统，体系结构，甚至硬件都串起来了，太感谢了</div>2022-07-04</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/23/be/eb/d5ef9cb3.jpg" width="30px"><span>LY</span> 👍（0） 💬（0）<div>RS触发器真值表画错了</div>2022-04-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/28/97/dc/8eacc8f1.jpg" width="30px"><span>漠博嵩</span> 👍（0） 💬（0）<div>数电 模电 你们都学过吗?</div>2022-02-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/d5/a4/5dd93357.jpg" width="30px"><span>Passion</span> 👍（0） 💬（0）<div>大学数电的知识，还好都理解了</div>2021-12-23</li><br/>
</ul>