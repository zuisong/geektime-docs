你好，我是倪朋飞。

上一节，我给你讲了CPU上下文切换的工作原理。简单回顾一下，CPU 上下文切换是保证 Linux 系统正常工作的一个核心功能，按照不同场景，可以分为进程上下文切换、线程上下文切换和中断上下文切换。具体的概念和区别，你也要在脑海中过一遍，忘了的话及时查看上一篇。

今天我们就接着来看，究竟怎么分析CPU上下文切换的问题。

## 怎么查看系统的上下文切换情况

通过前面学习我们知道，过多的上下文切换，会把CPU 时间消耗在寄存器、内核栈以及虚拟内存等数据的保存和恢复上，缩短进程真正运行的时间，成了系统性能大幅下降的一个元凶。

既然上下文切换对系统性能影响那么大，你肯定迫不及待想知道，到底要怎么查看上下文切换呢？在这里，我们可以使用 vmstat 这个工具，来查询系统的上下文切换情况。

vmstat 是一个常用的系统性能分析工具，主要用来分析系统的内存使用情况，也常用来分析 CPU 上下文切换和中断的次数。

比如，下面就是一个 vmstat 的使用示例：

```
# 每隔5秒输出1组数据
$ vmstat 5
procs -----------memory---------- ---swap-- -----io---- -system-- ------cpu-----
 r  b   swpd   free   buff  cache   si   so    bi    bo   in   cs us sy id wa st
 0  0      0 7005360  91564 818900    0    0     0     0   25   33  0  0 100  0  0
```

我们一起来看这个结果，你可以先试着自己解读每列的含义。在这里，我重点强调下，需要特别关注的四列内容：

- cs（context switch）是每秒上下文切换的次数。
- in（interrupt）则是每秒中断的次数。
- r（Running or Runnable）是就绪队列的长度，也就是正在运行和等待CPU的进程数。
- b（Blocked）则是处于不可中断睡眠状态的进程数。
<div><strong>精选留言（30）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/10/3b/36/2d61e080.jpg" width="30px"><span>行者</span> 👍（226） 💬（1）<div>结合前两节，首先通过uptime查看系统负载，然后使用mpstat结合pidstat来初步判断到底是cpu计算量大还是进程争抢过大或者是io过多，接着使用vmstat分析切换次数，以及切换类型，来进一步判断到底是io过多导致问题还是进程争抢激烈导致问题。</div>2018-11-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/36/d2/c7357723.jpg" width="30px"><span>发条橙子 。</span> 👍（95） 💬（4）<div>案例分析 ：

登录到服务器，现在系统负载怎么样 。 高的话有三种情况，首先是cpu使用率 ，其次是io使用率 ，之后就是两者都高 。 

cpu 使用率高，可能确实是使用率高， 也的可能实际处理不高而是进程太多切换上下文频繁 ， 也可能是进程内线程的上下文切换频繁

io 使用率高 ， 说明 io 请求比较大， 可能是 文件io 、 网络io 。  

工具 ：
系统负载 ：  uptime   （ watch -d uptime）看三个阶段平均负载
系统整体情况 ：  mpstat （mpstat -p ALL 3） 查看 每个cpu当前的整体状况，可以重点看用户态、内核态、以及io等待三个参数
系统整体的平均上下文切换情况 ： vmstat   (vmstat 3) 可以重点看 r （进行或等待进行的进程）、b （不可中断进程&#47;io进程） 、in （中断次数） 、cs（上下文切换次数）  
查看详细的上下文切换情况 ： pidstat （pidstat -w(进程切换指标)&#47;-u（cpu使用指标）&#47;-wt(线程上下文切换指标)） 注意看是自愿上下文切换、还是被动上下文切换
io使用情况 ： iostat

模拟场景工具 ：
stress ： 模拟进程 、 io
sysbench ： 模拟线程数</div>2018-12-02</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/51/0f/17bdfdaf.jpg" width="30px"><span>酱油侠</span> 👍（68） 💬（10）<div>我用的centos，yum装的sysbench。执行后很快完事了的可以设置下max-requests，默认max-requests是1w所以很快就结束了。
sysbench --num-threads=10 --max-time=300 --max-requests=10000000 --test=threads run
有的朋友&#47;proc&#47;interrupts时看不见RES是因为窗口开太小了RES在最下面。</div>2018-11-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/5b/e0/d27145c8.jpg" width="30px"><span>discoverer-tab</span> 👍（35） 💬（1）<div>过多上下文切换会缩短进程运行时间vmstat 1 1：分析内存使用情况、cpu上下文切换和中断的次数。cs每秒上下文切换的次数，in每秒中断的次数，r运行或等待cpu的进程数，b中断睡眠状态的进程数。pidstat -w 5：查看每个进程详细情况。cswch（每秒自愿）上下文切换次数，如系统资源不足导致，nvcswch每秒非自愿上下文切换次数，如cpu时间片用完或高优先级线程案例分析：sysbench：多线程的基准测试工具，模拟context switch终端1：sysbench --threads=10 --max-time=300 threads run终端2：vmstat 1：sys列占用84%说明主要被内核占用，ur占用16%；r就绪队列8；in中断处理1w，cs切换139w==&gt;等待进程过多，频繁上下文切换，内核cpu占用率升高终端3：pidstat -w -u 1：sysbench的cpu占用100%（-wt发现子线程切换过多），其他进程导致上下文切换watch -d cat &#47;proc&#47;interupts ：查看另一个指标中断次数，在&#47;proc&#47;interupts中读取，发现重调度中断res变化速度最快总结：cswch过多说明资源IO问题，nvcswch过多说明调度争抢cpu过多，中断次数变多说明cpu被中断程序调用</div>2018-11-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/f6/4e/0066303c.jpg" width="30px"><span>cuikt</span> 👍（14） 💬（4）<div>可以通过以下指令进行排序，观察RES。
watch -d &#39;cat &#47;proc&#47;interrupts | sort -nr -k 2 &#39;</div>2019-04-30</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/78/e9/9d807269.jpg" width="30px"><span>miracle</span> 👍（12） 💬（10）<div>发现一个不太严谨的地方，即使没有开sysbench，用watch -d &#47;proc&#47;interrupts的时候 RES的变化也是最大的，这个时候in跟cs都不高</div>2018-11-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/1a/82/ca3ef12c.jpg" width="30px"><span>Haku</span> 👍（11） 💬（1）<div>Ubuntu16.04LTS下:
# 以 10 个线程运行 5 分钟的基准测试，模拟多线程切换的问题
$ sysbench --num-threads=10 --max-time=300 --test=threads run</div>2018-11-28</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/PiajxSqBRaEIHvQHWCJ6cjAjFthVAADNWx0uaZicm4UDJCbVbvcian6gFI1gqWWX2tG3lEB2nVNtaVXtwibGOYiauCA/132" width="30px"><span>echo</span> 👍（9） 💬（1）<div>老师你好，有个难题希望能指导一下排查
我有个系统，跑的是32核48G的云主机，load经常超过CPU核数，峰值时load5可达到CPU核数的3倍， 但是CPU利用率不超过50%左右。
其他关键数据：I&#47;O wait 不超过0.1， 网络流量没超出网卡QOS，R状态的进程数也就一两个，没有D状态的进程。系统只要跑一个CPU密集型的Java进程，线程数2-3k。另外load、CPU、网卡流量的曲线是一致的。

通读了你的第二篇文章，按文章指导能排查的都排查了，接下来应该从哪方面着手定位load高的根因呢？</div>2018-11-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/15/0f/954be2db.jpg" width="30px"><span>茴香根</span> 👍（8） 💬（1）<div>打卡本节课程，在使用Linux一些监控命令行时候常常碰到列宽和下面的的数据错位的情况，比如数据过大，占了两列，导致数据错位，不方便观察，不知老师可有好的工具或方法解决。</div>2018-11-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/9b/ba/333b59e5.jpg" width="30px"><span>Linuxer</span> 👍（8） 💬（1）<div>我们之前是如果系统CPU不高根本不会去关注上下文切换，但是这种情况下以前也观测到cs有几十万的情况，所以我想请教一个问题，什么情况下需要关注上下文切换呢？</div>2018-11-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/18/3e/22/f91219a8.jpg" width="30px"><span>wanlinwang</span> 👍（7） 💬（2）<div>进程状态说明

R (task_running) : 可执行状态

S (task_interruptible): 可中断的睡眠状态

D (task_uninterruptible): 不可中断的睡眠状态

T(task_stopped or task_traced)：暂停状态或跟踪状态

Z (task_dead - exit_zombie)：退出状态，进程成为僵尸进程

X (task_dead - exit_dead)：退出状态，进程即将被销毁

文章中写的是b状态是不可中断的睡眠状态，哪个是正确的？</div>2019-07-16</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/1b/82/69581d8a.jpg" width="30px"><span>姜小鱼</span> 👍（6） 💬（2）<div>老师 为什么我执行sysbench之后很快就结束了？sysbench --num-threads=10 --max-time=600 --test=threads run 我用的是ubuntu16</div>2018-11-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/42/f7/06cd1560.jpg" width="30px"><span>X</span> 👍（5） 💬（1）<div>『D5打卡』

不用root权限的Linux用户，不是好的用户😂
这几天访问&#47;proc 只读文件的次数，比以前几个月都多，老实说，学会pidstat、vmstat这些工具的靠谱使用方法，就值了。不过还是要记住，工具不是全部
乌班图真的稳，跟着老师操作，基本没啥问题</div>2018-11-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/e9/b2/6a9203b5.jpg" width="30px"><span>小苏</span> 👍（4） 💬（2）<div>老师我有个关于cpu 时间片的问题:
        进程是拥有资源的基本单位,很多书上说cpu分配时间片给进程,但是又说线程是cpu调度的基本单位更甚者有的说进程是抢占cpu的基本单位,现在我对这个概念比较乱,那么cpu分配时间片的到底是给进程还是直接给到线程如果是给到进程那么进程中的线程是不是共享进程的时间片,那么进程中的线程是由进程本身去调度的吗?(进程选中一个优先级交搞的线程吧时间片交给这个线程执行) 例如jvm,还是由操作系统去调度?个人理解是线程共享进程的时间片多线程情况下进程选择优先级高(或按照一定的规则)选择一个线程让改线程消耗进程的时间片,但是看了好多资料越看越懵,请老师和同学们帮忙释义下.到底是怎样调度的.</div>2019-08-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/2c/31/aa/e16254e2.jpg" width="30px"><span>正能量</span> 👍（3） 💬（1）<div>由于虚拟机和真实Linux环境搭建比较麻烦。 可以考虑使用 docker镜像 这也符合当下 云服务的实际情况。 win10装上 docker后，拉取Ubuntu镜像，即可。而且docker配置的灵活性更高。 只是建议</div>2022-01-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/fb/7f/746a6f5e.jpg" width="30px"><span>Q</span> 👍（3） 💬（1）<div>
	* 如何查看CPU上下文切换情况？
vmstat，指标参数(cs 每秒上下文切换次数、in 每秒中断次数、r 进程就绪队列、b 不可中断睡眠的进程数)，注意该工具只显示进程切换总体状态，不显示具体进程的切换状态
pidstat，指标参数(cswch 自愿上下文切换，一般是资源不足导致、nvcswch 非自愿上下文切换，时间片花完，被强制切换)，该工具可以显示具体进程的切换状态，加上 -t 参数之后显示具体的线程切换状态
	* 上下文切换次数多少才算正常？综合分析自愿、非自愿上下文切换次数、中断次数(中断会导致上下文切换)，结合系统正常、平稳运行状态下的基线状态来判断

	* 如何查看中断情况？ cat &#47;proc&#47;interrupts

注意，我在实验过程中由于虚拟机只配了一个核心CPU，所以RES值为0，因为该中断类型表示，唤醒空闲状态的 CPU 来调度新的任务运行，由于只配置了一个CPU，就没有空闲的CPU可用。当把CPU核数增加到2个之后，该RES值才体现出来。</div>2018-12-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/0d/4d/f692ba8b.jpg" width="30px"><span>wmmmeng</span> 👍（3） 💬（1）<div>老师您好，很感谢您的分享，让我了解了Linux的一些基础运行原理。有2句话，我没有太明白“观察一段时间，你可以发现，变化速度最快的是重调度中断（RES），这个中断类型表示，唤醒空闲状态的 CPU 来调度新的任务运行”。1. 变化速度这个怎么理解呢，是指每个cpu的每秒增长值吗，如果是，在有多个interrupts在变动的时候，有什么好的办法方便看变化么（我的是8核的，看到的结果是Local timer interrupts，Performance monitoring interrupts在8个cpu中的高亮也很快，不知道具体有没有什么好的方法看多个cpu多个interripts的变化值）？2. 在老师的配置中，vmstat状态里面r和b状态的进程数远超cpu核数，为啥还会有出现唤醒空闲状态的cpu这一说法呢？望老师不要嫌弃我小白用户，谢谢老师
</div>2018-12-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/64/9b/d1ab239e.jpg" width="30px"><span>J.Smile</span> 👍（2） 💬（1）<div>我的中断速度最快的是这个，这个啥意思嘞？
LOC: 1533644095 4160359531   Local timer interrupts
</div>2020-07-22</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/7UJwSjHWKYOwnAYjjiaNBob396XaIqmttnHKuM7ahBu19QCn1mNicrg24nKgzA2kttP8tpV466anzMjMxq8Sx3Lw/132" width="30px"><span>Solokat</span> 👍（2） 💬（1）<div>贡献一个曾经踩过的坑。

cswch数目在这个机器低load的情况下，总的cswch数目比高load的情况下，多出一个数量级。例如
系统高load：186,616
系统低load：1,067,542
在这种情况下，低load总的执行时间只是高load下的60%。

其原因是（我的认识），但cswch发生的时候，必然是两个原因之一：1）等待资源，例如内存，IO。2）高优先级的任务抢断。在我所用到系统中，基本上来自于等待资源，查询数据库的等待。

cswch只是反映了上下文切换的次数，并没有反映每次切换所~等~待~的~时~间。

不过也有疑问，为啥在低Load的情况下，上下文切换的次数增加那么多？对此，我也有疑问。

期待你的赐教！</div>2020-07-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/d9/31/e58f2fb0.jpg" width="30px"><span>ranger2</span> 👍（2） 💬（2）<div>运行这个命令时：watch -d cat &#47;proc&#47;interrupts
在终端中，显示的数据行数有限，刚好RES没有显示出来，这个有什么参数可以解决吗？</div>2019-07-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/3e/19/873abe8a.jpg" width="30px"><span>董尚斌</span> 👍（2） 💬（1）<div>所谓自愿上下文切换，是指进程无法获取所需资源，导致的上下文切换。比如说， I&#47;O、内存等系统资源不足时，就会发生自愿上下文切换。

而非自愿上下文切换，则是指进程由于时间片已到等原因，被系统强制调度，进而发生的上下文切换。比如说，大量进程都在争抢 CPU 时，就容易发生非自愿上下文切换。

所以在压测的情况下，不应该是非自愿上下文升高吗？表明很多线程和进程争抢CPU。而不是由于资源不足导致的切换。

老师这里不是很懂。</div>2019-06-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/93/43/0e84492d.jpg" width="30px"><span>Maxwell</span> 👍（2） 💬（1）<div>额，这个好像很难理解，实际工作中上下文切换导致性能问题的多么？</div>2018-12-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/ec/8f/8299495a.jpg" width="30px"><span>少盐</span> 👍（1） 💬（2）<div>刚开始使用的yum install sysbench,但是提升不能够从阿里源获取，改用以下命令，完成安装
$ curl -s https:&#47;&#47;packagecloud.io&#47;install&#47;repositories&#47;akopytov&#47;sysbench&#47;script.rpm.sh | sudo bash

$ sudo yum -y install sysbench
vmstat  pidstat  sysbench 都是第一次接触，慢慢熟悉下</div>2019-07-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/17/7d/0d/c753174e.jpg" width="30px"><span>筱の简單</span> 👍（1） 💬（1）<div>centos7系统，执行sysbetch后，watch -d cat &#47;proc&#47;interrupts并没有发现文中描述的RES(重调度中断指标)，直接使用cat &#47;proc&#47;interrupts 查看 是有RES的</div>2019-05-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/ec/2a/b11d5ad8.jpg" width="30px"><span>曾经瘦过</span> 👍（1） 💬（1）<div>mark  长见识了 &#47;proc下面其实有很多文件都是很有用出的 还有内核态 用户态  系统调用导致的cpu切换  还有中断  让我更加清晰产生native崩溃的时候 android的的运行，对捕获native那部分内容有了更好的认识，同时 以后也对 android  cpu 部分的优化 更加深入了解 PS：曾经纠结了半天 为啥CPU要多任务同时执行。。后来想了一下linux是多用户系统，需要多任务同事执行 额.</div>2019-01-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/7e/32/e569f729.jpg" width="30px"><span>Lost In The Echo。</span> 👍（1） 💬（1）<div>top里面好像都有这些数据吧</div>2018-12-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/c2/1f/343f2dec.jpg" width="30px"><span>9527</span> 👍（1） 💬（2）<div>老师好，我有些问题
您在试验中，最后中断是因为RES 导致的
我自己试验发现是是LOC Local timer interrupts 这个值变化比较大，RES没变化
我用的是阿里云单CPU的机器，是否是机器原因导致的试验差别呢

另外您提到了上下文切换数量是 几百--一万以内
因为公司线上机器有台机器正在做数据传输，读一个A服务器的数据再写入到B服务器
我用dstat看，每秒的中断高达10W了，上下文切换也是7-8W，机器的idl大概是80，网络读400M+，写200M+
机器配置是 2.2G*40核，128G内存，万M网卡，因为只是从网络读，再通过网络写，所以磁盘无压力
但这个中断和上下文切换数量比老师说的高了很多，这种算是正常吗？

我用 watch -d cat &#47;proc&#47;interrupts  看这个机器，因为是40核的，CPU太多了
显示都完全乱了，根本看不出来了，对于CPU核太多的，显示上有什么更好的方式吗？

最后再问下平均负载的问题
我看线上机器，1m，5m，15m 平均负载看都是1.2到1.3的样子
因为这个机器是40核的，所以每个CPU都满负荷运作的话，平均负载应该是 40.0 吗？
现在我看到的负载是1.2，1.3的样子，就表示其实负载还是比较低的？</div>2018-12-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/56/2d/dd3b12b8.jpg" width="30px"><span>汤🐠🥣昱</span> 👍（1） 💬（1）<div>procs -----------memory---------- ---swap-- -----io---- -system-- ------cpu-----
 r  b   swpd   free   buff  cache   si   so    bi    bo   in   cs us sy id wa st
 1  0    520 3831600    116 7871856    0    0     0    11    0    0  0  0 99  0  0
 0  0    520 3831264    116 7871868    0    0     0     0 2285 2400  0  0 100  0  0
 0  0    520 3830956    116 7871924    0    0     0    11 2591 2818  2  0 98  0  0
 0  0    520 3830268    116 7871972    0    0     0    64 2440 2673  1  0 99  0  0
在使用vmstat 5 查看系统性能的时候，第一行cs，us小，之后数值都很大，这是为什么？
</div>2018-12-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/13/56/6a062937.jpg" width="30px"><span>gentleman♥️</span> 👍（1） 💬（1）<div>老师问个问题 像我们一般的应用什么的 就可以说是进程吧
它的进程的切换，最后还是要通过内部的线程来体现，也就说实际上一般应用的进程上下文切换，最后反应的都是线程的上下文切换，是吗，
那是不是也有只有线程级别内核上下文切换呢，比如一个进程只有一个线程这个是吧
但是有其他操作系统内核层面也有这样的上下文切换嘛，就是没有进程附加的内核切换，如果有，老师能举几个例子嘛</div>2018-12-01</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/57/ed/d50de13c.jpg" width="30px"><span>mj4ever</span> 👍（1） 💬（1）<div>本周外出培训了，不过还是需要坚持跟上，所以，周六先补习下CPU上下文切换的知识。
通过两篇知识的学习，掌握了以下内容：
1、理解了什么是CPU的上下文切换，以及上下文切换发生的场景有哪些
2、理解了系统调用的概念，用户态到内核态的转变，属于特权模式切换
3、实操模拟上下文切换的分析：
（1）首先，观察上下文切换和中断次数总体情况，可使用 vmstat 命令
（2）如果是，上下文切换次数过多，可进一步观察每个进程的详细情况，可使用 pidstat 命令；还要区分出是自愿（cswch）还是非自愿（nvcswch）
（3）如果是，中断次数过多，进一步观察系统中断使用情况，可以查看 &#47;proc&#47;interrupts

有一点小疑问：我模拟的场景下（测试用例和老师给的相同），中断次数并不算高，维持在2000左右，这个时候查看&#47;proc&#47;interrupts，发现LOC（Local timer interrupts）变化率要比RES（Rescheduling interrupts）的高；然后去查了LOC（https:&#47;&#47;stackoverflow.com&#47;questions&#47;10567214&#47;what-are-linux-local-timer-interrupts），发现没有看懂，或许也不是很重要：）

</div>2018-12-01</li><br/>
</ul>