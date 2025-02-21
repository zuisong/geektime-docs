“性能”这个词，不管是在日常生活还是写程序的时候，都经常被提到。比方说，买新电脑的时候，我们会说“原来的电脑性能跟不上了”；写程序的时候，我们会说，“这个程序性能需要优化一下”。那么，你有没有想过，我们常常挂在嘴边的“性能”到底指的是什么呢？我们能不能给性能下一个明确的定义，然后来进行准确的比较呢？

在计算机组成原理乃至体系结构中，“性能”都是最重要的一个主题。我在前面说过，学习和研究计算机组成原理，就是在理解计算机是怎么运作的，以及为什么要这么运作。“为什么”所要解决的事情，很多时候就是提升“性能”。

## 什么是性能？时间的倒数

计算机的性能，其实和我们干体力劳动很像，好比是我们要搬东西。对于计算机的性能，我们需要有个标准来衡量。这个标准中主要有两个指标。

第一个是**响应时间**（Response time）或者叫执行时间（Execution time）。想要提升响应时间这个性能指标，你可以理解为让计算机“跑得更快”。

![](https://static001.geekbang.org/resource/image/4c/96/4c87a1851aeb6857a323064859da6396.png?wh=1142%2A537 "图中是我们实际系统里性能监测工具NewRelic中的响应时间，代表了每个外部的Web请求的执行时间")

第二个是**吞吐率**（Throughput）或者带宽（Bandwidth），想要提升这个指标，你可以理解为让计算机“搬得更多”。

![](https://static001.geekbang.org/resource/image/27/27/27cab77c0eec95ec29792e6c3d093d27.png?wh=1142%2A300)

服务器使用的网络带宽，通常就是一个吞吐率性能指标

所以说，响应时间指的就是，我们执行一个程序，到底需要花多少时间。花的时间越少，自然性能就越好。
<div><strong>精选留言（30）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/12/e7/2e/1522a7d6.jpg" width="30px"><span>活的潇洒</span> 👍（304） 💬（5）<div>运行的代码是：
[root@nfs ~]# time seq 1000000 | wc -l
1000000

real	0m0.058s
user	0m0.047s
sys	0m0.044s
为什么user + sys 运行出来会比real time 多呢</div>2019-04-30</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/bf/22/26530e66.jpg" width="30px"><span>趁早</span> 👍（75） 💬（6）<div>time seq 100000 | wc -l
100000

real	0m0.006s
user	0m0.003s
sys	0m0.004s

我也是类似的问题，操作系统centos7.4，物理环境阿里云ecs 
cpu 信息
Intel(R) Xeon(R) Platinum 8163 CPU @ 2.50GHz</div>2019-04-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/e4/39/a06ade33.jpg" width="30px"><span>极客雷</span> 👍（200） 💬（2）<div>搞明白这个事实就好了，一个程序对应多条语句，一条编程语句可能对应多条指令，一条CPU指令可能需要多个CPU周期才能完成。</div>2019-05-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/d8/ee/6e7c2264.jpg" width="30px"><span>Only now</span> 👍（102） 💬（2）<div>猜测，跑分程序载入后，停止操作系统的线程调度或者给最高优先级和响应中断，全力跑跑分。暂时提高时钟频率，停止温度检测和低级中断，这样CPU就全力在跑测试程序了吧。

没做过弊，猜测</div>2019-04-30</li><br/><li><img src="https://wx.qlogo.cn/mmopen/vi_32/DYAIOgq83eqLcWH3mSPmhjrs1aGL4b3TqI7xDqWWibM4nYFrRlp0z7FNSWaJz0mqovrgIA7ibmrPt8zRScSfRaqQ/132" width="30px"><span>易儿易</span> 👍（62） 💬（4）<div>老师，针对“主频越高，意味着这个表走得越快，我们的 CPU 也就“被逼”着走得越快。”这句话我有一点儿疑惑：
时钟周期时间为1&#47;2.8G 秒，代表CPU最细粒度时间，即一次晶振的时间
这个周期时间和指令执行的耗时有直接关系吗？我说的直接关系指的是比如“一次晶振时间可以固定完成n个CPU（最简单的）指令”这种，如果有关系的话，那可以很明确的得出这个表走的快，CPU执行就快，毕竟单位时间内执行的指令数固定，通过降低单位时间就可以提升效率。
但是文中好像并没有提到这个直接关系，所有我可不可以这么去理解，晶振时间变短后，CPU调度指令的周期变短频次变高，使得上一个指令执行完毕到下一个指令被调动期间的等待时间变短，从而提升了CPU的利用率。好比一个监工增加了抬头看监控视频的频率，一旦有员工手停下来能立马给安排任务，主频低的话，可能员工休息半天才会被发现。另外，这种情况下，似乎主频提升的倍率并不能与性能提升带来1:1的效益。
1.晶振时间与CPU执行固定指令耗时成正比
2.晶振时间降低使CPU调度指令的周期变短频次变高
这两种哪一种对呢？还是都错？请指点~
——————————
又看了一遍，感觉刚刚对CPI的概念误读了，其实晶振时间是固定处理一个cpu简单指令的，CPI的平均时间是用来描述复杂指令的，指令数同样也是，其实整个公式如果用用简单指令来描述可能更容易理解一些</div>2019-05-01</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/DYAIOgq83eqvlyYKtm9AAJSoe296Ya9licicias0oicgmHSdKZIvIbPBDIRpRxqHxYCgPIC2UoRKGWiby3TJcjfHRpA/132" width="30px"><span>霹雳</span> 👍（50） 💬（1）<div>用户态运行和系统内核运行这两个什么区别呢</div>2019-05-02</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/08/ab/caec7bca.jpg" width="30px"><span>humor</span> 👍（42） 💬（2）<div>对于文中的CPU钟表时间间隔和时钟周期还是没有理解很清楚，时间间隔和时钟周期是互为倒数的关系吗？就是CPU主频是一个单位时间，而时钟周期就是这个单位时间被分成主频(2.8G)等份的一份吗?</div>2019-04-30</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/fd/b2/6a7cab4c.jpg" width="30px"><span>changing</span> 👍（37） 💬（1）<div>运行的代码是 time seq 100000 | wc -l
real	0m0.033s
user	0m0.030s
sys	0m0.005s
为什么user + sys 运行出来会比real time 多呢 </div>2019-04-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/17/09/9a/6e7b4442.jpg" width="30px"><span>KR®</span> 👍（29） 💬（1）<div>又重刷了一遍前四讲, 徐老师讲得又清惜又易懂，老师备课花了不少心血吧…
现在等待更新的心情就像追了一部超高分剧等更一样!!辛苦徐老师备课喇^^</div>2019-04-30</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/17/25/fc/548c9c14.jpg" width="30px"><span>安之若素，岁月静好</span> 👍（26） 💬（3）<div>跑分作弊个人猜测：当检测到跑分程序运行的时候，降低系统调用，提高跑分程序优先级。关闭热管理系统(防止过热关核降频)，手机CPU核心全开，超频到最高等。不顾一切，全心全意为跑分程序服务</div>2019-05-02</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/4e/d1/ded6b849.jpg" width="30px"><span>大飞守角</span> 👍（19） 💬（1）<div>看到cpu指令这一块，我想起了精简指令和复杂指令，执行同样的任务，精简指令需要的条数少，复杂指令需要的多，是不是说同样的任务，放在同样频率的精简指令cpu和复杂指令cpu上执行，精简指令cpu的执行效率高？</div>2019-05-12</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTKUrryic1mC5jVSRPyYtibXSUjFstBxIlHrZF4yc8NrZHiclxRZQMAYf7h4G5qrzpFyynsz6jHRsFgOQ/132" width="30px"><span>ruanxw</span> 👍（18） 💬（1）<div>老师，CPU 8核 16核代表啥意思我还是没怎么理解。</div>2019-08-21</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/DYAIOgq83erWv8WHAwWNgQgvdfRaibickVtpxZtg5N90bicQ2ohWuBQqWpJez1sylZgOqMxJzP2SRDoWKZtK49NhQ/132" width="30px"><span>imicode</span> 👍（16） 💬（8）<div>1. 打卡总结:
性能的CPU有两个重要的指标，响应时间和吞吐率。在这两个重要指标下，要提升性能，核心是优化CPU的执行时间，而CPU执行时间公式如下:

程序的 CPU 执行时间 = 指令数×CPI×Clock Cycle Time

2. 关于作弊
要提高跑分，无非是优化CPU的执行时间，可以从两个方面入手，一是提高CPI，可以采取超频运行的模式；二是优化指令数，单独针对特定的CPU进行代码优化。
</div>2019-05-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/2f/cf/fb214a2c.jpg" width="30px"><span>Guarantee</span> 👍（11） 💬（1）<div>老师，单个CPU的主频是有上限的，所以出现了多核CPU进行计算，为了提高更多的计算，是不是就要运用分布式计算这个技术。</div>2019-05-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/30/8b/3334f23e.jpg" width="30px"><span>潜默闻雨</span> 👍（11） 💬（1）<div>徐老师，程序的cpu执行时间是不是由很多cpu时间片组成，而cpu并不知道自己在执行哪个程序的指令，只是按时间片去按顺序执行指令，不知道这样理解对不对？非科班的转行人士，正在努力补基础😅。。。</div>2019-04-29</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/ib3Rzem884S7icAGXsBzGKyricapL0sfax7wL7T4n1W1ZPZ0h7XNtGd5aqLlZQgZ3bZTPBmC4xa7ia8iaR0XBKMAuIQ/132" width="30px"><span>Geek_63ad86</span> 👍（10） 💬（1）<div>老师我尝试了用自己的话理解一下您讲授的内容：
度量一个程序运行的时间T需要知道该程序有几条指令(n)，每一个指令平均需要几个基本操作才能执行完毕(k)，cpu执行一个基本操作的耗时(t)，从而T = n*k*t，t作为SE一般是无法提升的，除非改进硬件，所以缩短运行时间可能主要还是从n、k入手。不知道这样理解是否正确？
此外，跑分“作弊”我猜测是利用软件暂时提升手机性能，但是性能只是衡量手机的一个维度，在不同使用场景下手机的流畅性和稳定性也是需要考虑的，“作弊”跑分的参考价值不大，对于十分注重跑分的用户作弊的跑分可能会对他们产生很强的欺骗性。</div>2019-05-15</li><br/><li><img src="" width="30px"><span>txhh</span> 👍（6） 💬（1）<div>time seq 100000 | wc -l
100000

real    0m0.003s
user    0m0.003s
sys     0m0.003s
虚拟机上的CentOS 7.5    i7 6700HQ</div>2019-04-30</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/57/4f/6fb51ff1.jpg" width="30px"><span>奕</span> 👍（6） 💬（1）<div>有个疑问，现在CPU的时钟周期是不是都是一定的，CPU的频率是根据CPU的处理能力计算出来的。 但是现在说的超频是缩短的CPU时钟周期，让在一个更短的周期内处理相同的指令数，但是这个缩短的范围怎么定义的？会不会超过CPU的处理极限，如果每个CPU的时钟周期不一致，那怎么相互比较CPU的性能差异

希望老师解答</div>2019-04-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/08/17/e63e50f3.jpg" width="30px"><span>彩色的沙漠</span> 👍（5） 💬（1）<div>老师您好，原文中有关于主频的描述如下：
这里的 2.8GHz 就是电脑的主频（Frequency&#47;Clock Rate）。这个 2.8GHz，我们可以先粗浅地认为，CPU 在 1 秒时间内，可以执行的简单指令的数量是 2.8G 条。

如果想要更准确一点描述，这个 2.8GHz 就代表，我们 CPU 的一个“钟表”能够识别出来的最小的时间间隔。
问题是&quot;这个 2.8GHz 就代表，我们 CPU 的一个“钟表”能够识别出来的最小的时间间隔。&quot;不应该是主频的倒数是最小的时间间隔吗？</div>2019-05-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/79/0b/4346a253.jpg" width="30px"><span>Ant</span> 👍（5） 💬（1）<div>时钟周期是啥意思</div>2019-05-06</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/df/c4/77b8828e.jpg" width="30px"><span>victory0943</span> 👍（4） 💬（1）<div>老师按你说的程序CPU执行时间=时钟周期数*指令数*每条指令的平均时钟周期数，
因为一个程序里会有不同的指令，且不同指令需要cycle也不同，这样在计算cpu总和的话，是不是要区分不同的指令来计算？如果是的话那怎么区分呢？</div>2019-05-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/03/c9/9a9d82ab.jpg" width="30px"><span>Aaron_涛</span> 👍（3） 💬（2）<div>老师，Clock Cycle Time代表CPU运行原子时间，同比与现实世界的秒，CPI代表一个指令所要的运行的时间周期次数。意思就是需要多少个秒的单位做完这条指令
例如 
乘法 对应一条指令， CPI = 2  Clock Cycle Time = 1&#47;2.8G   代表，完成乘法指令，需要2个Clock Cycle Time的时间
加法 对应一条指令 ，CPI = 1   Clock Cycle Time = 1&#47;2.8G   代表，完成加法指令，需要1个Clock Cycle Time的时间

这么理解不知道对不对

</div>2019-04-30</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/ad/a6/791d0f5e.jpg" width="30px"><span>Dsir9527</span> 👍（3） 💬（1）<div>changing 同学的问题在stackoverflow 上的解释是这样的：
The rule of thumb is:

real &lt; user: The process is CPU bound and takes advantage of parallel execution on multiple cores&#47;CPUs.
real ≈ user: The process is CPU bound and takes no advantage of parallel exeuction.
real &gt; user: The process is I&#47;O bound. Execution on multiple cores would be of little to no advantage.

https:&#47;&#47;unix.stackexchange.com&#47;questions&#47;40694&#47;why-real-time-can-be-lower-than-user-time</div>2019-04-30</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/17/14/c5/87631334.jpg" width="30px"><span>静静的拼搏</span> 👍（3） 💬（1）<div>觉得可以作弊，主要在cpu频率进行超频和通过编译减少程序执行的指令和执行时间，这样的分数比较片面，有一定的参考价值，但不能作为日常使用的性能参考</div>2019-04-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/9b/ba/333b59e5.jpg" width="30px"><span>Linuxer</span> 👍（3） 💬（3）<div>作弊应该也离不开三要素，超频、降低CPI、或者减少指令数</div>2019-04-29</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/3ibaWJTaDUfwRZib0TmxQYKJh7gEQicGzeh63t3llicqfJpYUZgofaib743G0JBdpIsppA3zCHvelVqGEfO0tBYW2pA/132" width="30px"><span>jql</span> 👍（2） 💬（1）<div>老师用那个脚本，要用什么编译器（我刚刚接触计算机）</div>2020-02-02</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/2a/c6/8646048e.jpg" width="30px"><span>ginger</span> 👍（2） 💬（1）<div>我觉得手机跑分的&quot;作弊&quot;,应该是公式中的指令数和Clock Cycle Time两个方面来做,前者可以通过关闭很多服务或者停止部分监控程序或者其他一些方式来实现,(这个想法不成熟,因为关闭指令也需要cpu资源.)后者就是通过超频来实现,一单检测到跑分程序,直接开启超频,不去在意cpu散热,毕竟跑分软件不会很长时间运行.
再有方式,那应该是一些别的途径了,既然cpu有超频概念,那么磁盘读写应该也有超读写概念.
希望作者或者看专栏的大佬们,可以指正下,补充下.手动嘻嘻.</div>2019-05-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/f0/19/9d754804.jpg" width="30px"><span>牧野</span> 👍（2） 💬（1）<div>老师文中给到的wall clock time示例图，结束程序逻辑应该是p1才对。</div>2019-05-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/40/35/6ebb8278.jpg" width="30px"><span>诺哲</span> 👍（2） 💬（1）<div>写的通俗易懂，因为跨考计算机研究生，之前看计组书很枯燥，看不懂，希望能通过老师的专栏顺路入个门。希望之后的课程也能这样通俗易懂，照顾我们这些新手。谢谢老师</div>2019-05-09</li><br/><li><img src="" width="30px"><span>庄小P</span> 👍（2） 💬（1）<div>提高性能的话从老师讲的三个方面
1. 时间周期，可通过超频技术，不过估计每个厂商都有把，看谁比较无赖而已哈哈？
2.指令CPI     特意改造硬件来使用程序的需求。FPGA好像就是能够来专门定制硬件的，可以把频繁使用的指令放在上面跑。
3.指令数 这个应该是本身测试有多少条指令就已经确定好了，所以这个应该没办法修改把
请老师指正哈~~~</div>2019-05-02</li><br/>
</ul>