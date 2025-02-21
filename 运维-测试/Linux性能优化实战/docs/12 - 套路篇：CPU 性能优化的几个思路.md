你好，我是倪朋飞。

上一节我们一起回顾了常见的 CPU 性能指标，梳理了核心的 CPU 性能观测工具，最后还总结了快速分析 CPU 性能问题的思路。虽然 CPU 的性能指标很多，相应的性能分析工具也很多，但理解了各种指标的含义后，你就会发现它们其实都有一定的关联。

顺着这些关系往下理解，你就会发现，掌握这些常用的瓶颈分析套路，其实并不难。

在找到 CPU 的性能瓶颈后，下一步要做的就是优化了，也就是找出充分利用CPU的方法，以便完成更多的工作。

今天，我就来说说，优化 CPU 性能问题的思路和注意事项。

## 性能优化方法论

在我们历经千辛万苦，通过各种性能分析方法，终于找到引发性能问题的瓶颈后，是不是立刻就要开始优化了呢？别急，动手之前，你可以先看看下面这三个问题。

- 首先，既然要做性能优化，那要怎么判断它是不是有效呢？特别是优化后，到底能提升多少性能呢？
- 第二，性能问题通常不是独立的，如果有多个性能问题同时发生，你应该先优化哪一个呢？
- 第三，提升性能的方法并不是唯一的，当有多种方法可以选择时，你会选用哪一种呢？是不是总选那个最大程度提升性能的方法就行了呢？

如果你可以轻松回答这三个问题，那么二话不说就可以开始优化。

比如，在前面的不可中断进程案例中，通过性能分析，我们发现是因为一个进程的**直接 I/O** ，导致了 iowait 高达 90%。那是不是用“**直接 I/O 换成缓存 I/O**”的方法，就可以立即优化了呢？
<div><strong>精选留言（30）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/0f/54/9a/76c0af70.jpg" width="30px"><span>每天晒白牙</span> 👍（47） 💬（3）<div>【D12打卡】
CPU性能优化思路
方法论
1.性能优化的效果判断
三步走理论
(1)确定性能的量化指标－一般从应用程序纬度和系统资源纬度分析
(2)测试优化前的性能指标
(3)测试性能优化后的性能指标
2.当性能问题有多个时，优先级问题
先优化最重要的且最大程度提升性能的问题开始优化
3.优化方法有多个时，该如何选
综合多方面因素
CPU优化
应用程序优化:排除不必要工作，只留核心逻辑
1.减少循环次数  减少递归  减少动态没错分配
2.编译器优化
3.算法优化
4.异步处理
5.多线程代替多进程
6.缓存
系统优化:利用CPU缓存本地性，加速缓存访问;控制进程的cpu使用情况，减少程序的处理速度
1.CPU绑定
2.CPU独占
3.优先级调整
4.为进程设置资源限制
5.NUMA优化
6.中断负载均衡
很重要的一点:切记过早优化

</div>2018-12-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/42/f7/06cd1560.jpg" width="30px"><span>X</span> 👍（16） 💬（1）<div>又一篇精华满满的惊喜！
看到有人说，这些东西应该自己总结。是的，没错，很赞同。我也把用到的所有工具、指标、思路总结了一遍，但是看到老师给出了更全面系统的总结，仍然很受用。因为老师能从原理、关联多个角度给出更全面的知识网，也会指出一些易错的地方，是我们通学一遍、自己总结一遍以后的升华。起码，有些地方，因为原理知道的不多，我想错了或者漏了，看到这篇后，豁然开朗
老师给总结了，不等于你就会了，该学还得学，该记还得记，就像是满满的金子堆你面前，要不要弯腰去捡😊</div>2018-12-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/64/05/6989dce6.jpg" width="30px"><span>我来也</span> 👍（12） 💬（4）<div>[D12打卡]
这些常见的性能优化方法,之前都了解的不全面,待其他大神给我们开开眼界.
我以前优化大多都是感性的,就是凭感觉或经验,并没有些实际的指标来观测.
一方面自己只是做开发,管好自己的程序即可,其他方便(比如系统环境)可能是有心无力.
-------------------------
&quot;过早优化是万恶之源&quot;
我也是很赞同的,用户没几个,花那么多精力做过度优化没必要,还不如拿那些时间来学学专栏.等真的有一定规模和趋势了,再用&quot;二八原则&quot;有针对性的优化.
我个人一般在写代码时,会在可以进一步优化的地方加个注释,暂时先在够用的情况下,怎么简单怎么来,后期如果有必要了,再来找这些注释,看什么地方值得优化.
-------------------------
应用程序优化方面,可以谈谈我的经历:
编译器优化: 刚参加工作时,培训期间练习一些算法,会对比每个人程序的性能. 我当时还是用的VC6.0++. 而有的同学用dev-c++编译器, 结果成绩经常被吊打. 即使是同一份源码,编译出来的程序也是有很大的差距.
算法优化: 正在学算法专栏. 也是要根据实际情况来优化, 利用二八原则,有针对性的优化,不要什么都优化,一天才执行一次的程序, 耗时1s 和0.001s的差距并不大. 虽然数字上相差了很多倍.
异步优化: 比如lua的协程,epoll代替原来的select和poll.
多线程代替多进程: 线程的切换理论上是比进程切换的成本低. 但有时候考虑到扩展性,还会从单进程改为多进程模型.
善用缓存:也可利用二八原则, 看值不值得. 是用空间换时间,还是时间换空间.
------------------
做优化,真的是要见机行事,像老师说的,[不要只会“拿来主义”]</div>2018-12-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/cb/b3/4325ffc4.jpg" width="30px"><span>xcz</span> 👍（5） 💬（1）<div>买了几个课程里觉得最好的一门课，有条理，干货满满！</div>2018-12-19</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTJVwuRvAuze6NsLGr4qwVa7IJcib3YdQVqlicuEicP8FmGR2qo8Wia1BXtnnbVeDxH41EkLmOmNiac5nQQ/132" width="30px"><span>南宫轩诺</span> 👍（4） 💬（2）<div>倪老师，请教您一个问题：最近在开发服务端，遇到一个问题,客户端开启单线程批量向不断服务端导入数据（服务端是多线程接收），并且存在加锁、日志异步打印和耗时统计操作，在这种情况下，客户端导入数据比较慢，服务端的cpu利用率只能维持在50%~60%左右，通过iostat和pidstat工具观测系统io和进程上下文切换等指标也没发现导致该现象的原因。
       如果关闭日志打印和耗时统计操作，cpu利用率会得到很大的提升，接近100%，客户端数据导入速度得到很大提升。因此我判断是日志打印和统计导致cpu利用率过低。针对这种情况，从哪些指标上能辅助发现是日志打印和耗时操作导致cpu不能高效利用呢？期待您的答疑，谢谢！</div>2019-01-15</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/0e/f5/c4a26e84.jpg" width="30px"><span>Im Robin</span> 👍（3） 💬（1）<div>打开，谢谢老师干货满满的教学
--------------------------------------------------------------
这里有一个问题， 我们线上的nginx两个实例之间QPS差2倍，nginx前面是四层SLB，两者唯一的区别就是centos6.5跟centos7.3，QPS高的机器load也高，推论就是centos6.5的那台压力上不去，在&#47;proc&#47;interrupts看到centos6.5的只有cpu0在处理虚拟网卡中断，而另一台四个cpu都在工作，不知道是不是这里的原因，看到这篇里老师有提到中断负载均衡，在想跟这里有没有关系，想向老师请教下</div>2018-12-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/24/d7/146f484b.jpg" width="30px"><span>小宇子2B</span> 👍（2） 💬（1）<div>老师好，近期遇到一个问题，6核机器，负载在20-100之间徘徊，查看了cpu使用率、io、上下文切换都是很正常，业务是java的一个应用主要是接收监控agent上报的数据的，业务不受影响，其他一切正常，还有什么可能会导致负载高吗？</div>2019-06-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/d9/d0/baffc852.jpg" width="30px"><span>JuCY</span> 👍（2） 💬（1）<div>谢谢，不好意思再追问几句。
负载高CPU使用率低【也就是%idle高】，老师的结论是IO高，但我下面这么分析不知道对不对？
负载高CPU使用率低，说明CPU空闲的时候，等待队列里都是D状态进程，但是根据%iowait的定义和D状态的定义，CPU空闲时有D进程在等待的这段时间，应该算在iowait里，而不算在idle里，所以应该是%iowait高，%idle低才是啊，怎么会是%idle高呢？</div>2019-02-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/93/43/0e84492d.jpg" width="30px"><span>Maxwell</span> 👍（2） 💬（1）<div>请问CPU优化，cpu使用率和队列长度多少比较合适呢？</div>2019-01-25</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/dd/c8/3f100905.jpg" width="30px"><span>walt</span> 👍（2） 💬（2）<div>倪老师好，4核8G Centos7,cpu load 超过15，单核任务数接近4了，但是 cpu idle还有20～30%，这个情况下如何评价CPU资源呢？</div>2018-12-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/5f/28/17ed19bc.jpg" width="30px"><span>J</span> 👍（1） 💬（1）<div>有没有可能讲一讲cpufreq  Intel的E系列CPU影响很大啊 升级内核之后 谢谢</div>2018-12-17</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/DYAIOgq83erJFlHhylrbLANtehiaX50wgVa2Z1ibQAdLpgyW4gCpEyOKEI9bPNZZBiabrP2oCleZWc2KKyKADz8tg/132" width="30px"><span>阿丽</span> 👍（0） 💬（1）<div>老师，昨天的性能问题，今天还可以分析出来吗？用什么工具？</div>2019-06-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/d9/d0/baffc852.jpg" width="30px"><span>JuCY</span> 👍（0） 💬（1）<div>请教一下倪老师，有一种比较常见的情况是负载很高，但CPU使用率很低，可能是什么原因呢？怎么模拟这种现象？这个问题想了很久一直得不到答案</div>2019-02-25</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/d9/d0/baffc852.jpg" width="30px"><span>JuCY</span> 👍（0） 💬（1）<div>针对上面一个学员的问题，为什么负载高但是还有空闲CPU就判断是进程切换呢？</div>2019-02-25</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/bb/7d/1f4b4697.jpg" width="30px"><span>BR</span> 👍（0） 💬（1）<div>听了这几期，估计倪兄也是五分钟课的粉丝～</div>2019-01-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/0c/30/a2e7728a.jpg" width="30px"><span>Allen</span> 👍（0） 💬（1）<div>文章干货满满，如果当前cpu有DMA控制器，通过DMA进行数据搬移，也能很好的提高系统性能</div>2019-01-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/e3/9e/b26da70d.jpg" width="30px"><span>closer</span> 👍（0） 💬（1）<div>redis每次都把cpu打到100%。已经检查过netstat 和数据库只有6个连接，怎么排错</div>2019-01-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/93/43/0e84492d.jpg" width="30px"><span>Maxwell</span> 👍（0） 💬（1）<div>CPU利用率多少算是比较合适的呢，CPU优化需要优化到多少比较合适？</div>2019-01-10</li><br/><li><img src="" width="30px"><span>shibo</span> 👍（0） 💬（1）<div>之前做过服务器上的数据库性能优化，也是运用了这些套路，要是早点这篇文章，就能少走点弯路</div>2019-01-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/a9/90/0c5ed3d9.jpg" width="30px"><span>颇忒妥</span> 👍（0） 💬（1）<div>“分析完所有问题后，再按照因果等关系，排除掉有因果关联的性能问题。最后，再对剩下的性能问题进行优化。”
这句话不是太理解，为何要排除掉有因果关联的性能问题？
</div>2019-01-04</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/5c/cb/3ebdcc49.jpg" width="30px"><span>怀特</span> 👍（0） 💬（1）<div>不知道咋回事，每次都是mysql的cpu占满，注意是mysql，不是mysqld。当时没有看老师的专栏，酥手无策，业务也着急，所以后来重装了系统好了。
如果当时看过了老师的专栏，就可以立刻分析分析了，是一个很好的实际操练提高自己的机会，可惜了。</div>2018-12-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/92/c5/a2946220.jpg" width="30px"><span>陈启永</span> 👍（0） 💬（1）<div>倪老师您好，你讲的知识很有条理，跟着您的思路来走是能够很好的理解的。自己在工作用也会尝试使用这里学到的知识来解决实际问题，感觉不会有以前那样碰到问题没头绪的尴尬处境了。
但是使用起来还没那么顺手，有可能是接触不够多的原因，但我觉得更多的原因是对知识的理解不够深入导致的。
所以在这里想请教下您，有哪些书籍可以帮助我们更加深入地系统的理解您讲的知识呢？</div>2018-12-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/12/d8/12879eb7.jpg" width="30px"><span>善良的男人</span> 👍（0） 💬（1）<div>top  中的  %mem   总和  超过 百分之百  不是很明白   还有就是  res  时所占用的物理内存   可是 想加之后也远超 与 实际内存  其中有 共享内存的占用吗 ？</div>2018-12-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/34/bb/0b971fca.jpg" width="30px"><span>walker</span> 👍（0） 💬（2）<div>吞吐量一般怎么计算呢，有没有什么好的工具专门计算吞吐量的</div>2018-12-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/55/35/09e7dfde.jpg" width="30px"><span>Geek_101627</span> 👍（0） 💬（1）<div>打卡</div>2018-12-17</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/2o1Izf2YyJSnnI0ErZ51pYRlnrmibqUTaia3tCU1PjMxuwyXSKOLUYiac2TQ5pd5gNGvS81fVqKWGvDsZLTM8zhWg/132" width="30px"><span>划时代</span> 👍（0） 💬（1）<div>很多性能指标也是在做性能压力测试时使用的</div>2018-12-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/70/23/972dcd30.jpg" width="30px"><span>allan</span> 👍（0） 💬（1）<div>干货很多~</div>2018-12-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/34/bb/0b971fca.jpg" width="30px"><span>walker</span> 👍（0） 💬（1）<div>想做一个全面的性能调优测试，不知道需要从哪些点入手，然后需要注意哪些问题？</div>2018-12-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/11/fe/de00d8d8.jpg" width="30px"><span>王涛</span> 👍（0） 💬（1）<div>D12打卡。系统性优化是个大项目，要好好研究研究</div>2018-12-17</li><br/><li><img src="https://wx.qlogo.cn/mmopen/vi_32/PiajxSqBRaEKQMM4m7NHuicr55aRiblTSEWIYe0QqbpyHweaoAbG7j2v7UUElqqeP3Ihrm3UfDPDRb1Hv8LvPwXqA/132" width="30px"><span>ninuxer</span> 👍（0） 💬（1）<div>打卡，day13
cpu优化套路：
      程序级别：编译器优化，算法优化，异步处理，多进程转多线程，善用缓存
      系统级别：cpu绑定(优化上下文切换)，cpu独占（亲和性），nice值调整(得到更多的时钟周期)，cgroups设置资源限定，irqbalance负载中断，numa让cpu缓存命中率提升</div>2018-12-17</li><br/>
</ul>