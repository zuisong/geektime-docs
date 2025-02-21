你好，我是倪朋飞。

前几节里，我通过几个案例，带你分析了各种常见的 CPU 性能问题。通过这些，我相信你对 CPU 的性能分析已经不再陌生和恐惧，起码有了基本的思路，也了解了不少 CPU 性能的分析工具。

不过，我猜你可能也碰到了一个我曾有过的困惑： CPU 的性能指标那么多，CPU 性能分析工具也是一抓一大把，如果离开专栏，换成实际的工作场景，我又该观察什么指标、选择哪个性能工具呢？

不要担心，今天我就以多年的性能优化经验，给你总结出一个“又快又准”的瓶颈定位套路，告诉你在不同场景下，指标工具怎么选，性能瓶颈怎么找。

## CPU 性能指标

我们先来回顾下，描述 CPU 的性能指标都有哪些。你可以自己先找张纸，凭着记忆写一写；或者打开前面的文章，自己总结一下。

首先，**最容易想到的应该是 CPU 使用率**，这也是实际环境中最常见的一个性能指标。

CPU 使用率描述了非空闲时间占总 CPU 时间的百分比，根据 CPU 上运行任务的不同，又被分为用户CPU、系统CPU、等待I/O CPU、软中断和硬中断等。

- 用户 CPU 使用率，包括用户态 CPU 使用率（user）和低优先级用户态 CPU 使用率（nice），表示 CPU 在用户态运行的时间百分比。用户 CPU 使用率高，通常说明有应用程序比较繁忙。
- 系统 CPU 使用率，表示 CPU 在内核态运行的时间百分比（不包括中断）。系统 CPU 使用率高，说明内核比较繁忙。
- 等待 I/O 的CPU使用率，通常也称为iowait，表示等待 I/O 的时间百分比。iowait 高，通常说明系统与硬件设备的 I/O 交互时间比较长。
- 软中断和硬中断的 CPU 使用率，分别表示内核调用软中断处理程序、硬中断处理程序的时间百分比。它们的使用率高，通常说明系统发生了大量的中断。
- 除了上面这些，还有在虚拟化环境中会用到的窃取 CPU 使用率（steal）和客户 CPU 使用率（guest），分别表示被其他虚拟机占用的 CPU 时间百分比，和运行客户虚拟机的 CPU 时间百分比。
<div><strong>精选留言（30）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/12/64/05/6989dce6.jpg" width="30px"><span>我来也</span> 👍（84） 💬（1）<div>[D11打卡]
这简直就是小抄😁
好像在我的场景中,使用老师提到的这些工具就够用了.
先把这些性价比高的工具琢磨好了,以后有精力了再去学些小众的.
感谢老师帮我们挑出了重点,哈哈!
时间就是金钱啊,感谢老师帮我们节约时间,更高效的学习.👍</div>2018-12-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/61/90/de8c61a0.jpg" width="30px"><span>dongge</span> 👍（70） 💬（3）<div>这个专栏的这篇文章值一个亿</div>2018-12-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/27/66/afa629d6.jpg" width="30px"><span>Kino</span> 👍（60） 💬（2）<div>这图可以抵掉无数加班夜。极客时间最贴心讲师！鉴定完毕。</div>2019-05-16</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/af/b8/e910f6ef.jpg" width="30px"><span>童年的记忆🌾</span> 👍（42） 💬（2）<div>哎妈呀，本科4年，研究生2年，工作3年，这是我遇到的最优秀的老师了，没有之一。</div>2019-05-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/97/61/34a0da09.jpg" width="30px"><span>Griffin</span> 👍（23） 💬（2）<div>哈哈哈，只有从一年级开始就当课代表才能总结的这么好。</div>2018-12-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/fb/72/3fe64bc5.jpg" width="30px"><span>LA</span> 👍（7） 💬（5）<div>老师，看了您的文章，有个问题一直在困扰这我。文章所说进程不可中断状态有可能是因为等待io响应，那这里的等待io响应包括等待从套接字读取数据么？如果是包括的话对于阻塞io来讲岂不是只要有阻塞进程就一直处在不可中断状态，从而无法被kill信号杀掉？</div>2019-06-01</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/54/9a/76c0af70.jpg" width="30px"><span>每天晒白牙</span> 👍（7） 💬（1）<div>【D11打卡】
总结篇文章，可以多看，多操作，遇到问题可以按照思路分析，慢慢内化成自己的思路</div>2018-12-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/93/43/0e84492d.jpg" width="30px"><span>Maxwell</span> 👍（6） 💬（2）<div>CPU缓存命中率如何查看呢？</div>2019-02-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/c2/e0/7188aa0a.jpg" width="30px"><span>blackpiglet</span> 👍（5） 💬（1）<div>请问 CPU 缓存命中率应该如何统计呢？perf 吗？网上看到一些例子，但缓存是否命中似乎不像其他指标那么直观。</div>2019-01-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/18/97/e1/0f4d90ff.jpg" width="30px"><span>乖，摸摸头</span> 👍（4） 💬（4）<div>我一个开发人员，居然也买了</div>2019-07-28</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTKq0oQVibKcmYJqmpqaNNQibVgia7EsEgW65LZJIpDZBMc7FyMcs7J1JmFCtp06pY8ibbcpW4ibRtG7Frg/132" width="30px"><span>zhoufeng</span> 👍（4） 💬（1）<div>老师好，
没太理解strace和perf的使用场景，文中说使用strace 分析系统调用情况，以及使用 perf 分析调用链中各级函数的执行情况。
是否可以理解为当用户态cpu使用率高时，使用perf进行分析，而当内核态cpu使用率高时，使用strace分析系统调用呢？
谢谢。</div>2019-05-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/9b/a8/6a391c66.jpg" width="30px"><span>geraltlaush</span> 👍（4） 💬（1）<div>老师，我看了下可中断睡眠和不可中断睡眠的区别
可中断的睡眠状态的进程会睡眠直到某个条件变为真，如产生一个硬件中断、释放进程正在等待的系统资源或是传递一个信号都可以是唤醒进程的条件。
不可中断睡眠状态与可中断睡眠状态类似，但是它有一个例外，那就是把信号传递到这种睡眠状态的进程不能改变它的状态，也就是说它不响应信号的唤醒。
是不是就是对应的可中断进程(软中断)和不可中断进程(硬中断)，这块有点疑惑</div>2018-12-14</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/2o1Izf2YyJSnnI0ErZ51pYRlnrmibqUTaia3tCU1PjMxuwyXSKOLUYiac2TQ5pd5gNGvS81fVqKWGvDsZLTM8zhWg/132" width="30px"><span>划时代</span> 👍（4） 💬（1）<div>整体回顾复习了实践案例，实践练习消化，CPU性能指标关系详解图很赞。</div>2018-12-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/14/3a/94e25d0c.jpg" width="30px"><span>男人十八一枝花</span> 👍（2） 💬（1）<div>top - 22:08:46 up 86 days, 16:05,  2 users,  load average: 0.00, 0.00, 0.00
Tasks:  89 total,   1 running,  53 sleeping,   0 stopped,   0 zombie


老师，请问一下，我在搬瓦工上买的云主机上执行top命令，Task那一行running（1）+sleeping（53）+stopped+zombie的总数并不等于total（89）.请问这是为什么？</div>2018-12-18</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTKsz8j0bAayjSne9iakvjzUmvUdxWEbsM9iasQ74spGFayIgbSE232sH2LOWmaKtx1WqAFDiaYgVPwIQ/132" width="30px"><span>2xshu</span> 👍（2） 💬（2）<div>老师你好，非常感谢你能回答之前我提出的问题。我现在有个问题想请教下。
机器情况如下：
[root@10.xx.xx.xxx ~]# numactl -H
available: 2 nodes (0-1)
node 0 cpus: 0 2 4 6 8 10 12 14 16 18 20 22 24 26 28 30
node 0 size: 130978 MB
node 0 free: 9566 MB
node 1 cpus: 1 3 5 7 9 11 13 15 17 19 21 23 25 27 29 31
node 1 size: 131072 MB
node 1 free: 119623 MB
node distances:
node   0   1 
  0:  10  21 
  1:  21  10 

服务器任务情况：
在这台服务器上运行了两百个进程，每个进程任务是平级的，每个进程基本是下载文件任务。

直观现象：
1：根据zabbix监控，该服务器每隔6个小时左右会有一次内存大量回收。也就是已用内存从250g掉到了20g左右。
2：在掉内存的时候，服务器性能是出现问题了。最直观的表现就是网络连接建立不了。

我的解决办法：
根据上面numa的输出，我就发现两个node可用内存相差太大了。然后我果断把zone_reclaim_mode从1改成了0.然后问题得到解决了。（实属运气型解bug。哈哈）

其他现象：
1：查看&#47;proc&#47;stat发现很多 user时钟都集中在node0对应的cpu上。
2：zone_reclaim_mode=1时，kswap0线程，始终处于sleep状态,sar -B看pgscank对应值始终为0。改成0之后，kswap0就能得到调用。sar -B看pgscank也确实有被值了。

虽然问题解决了，但是还是疑问重重。
疑问如下：
1：我认为导致内存突然回收的根源在于cpu调度不均匀导致。不知道我的猜测是不是正确？（有没有相关资料推荐下哇，感激涕零啊。）
2：从现象来看，确实是有cpu调度不均的情况出现。那么为什么会出现cpu调度不均呢？我这200个进程都拥有相同的父进程supervisord。
3：zone_reclaim_mode 到底是什么作用呢？查看各方资料，在内存对应zone的水位不充足时，如果zone_reclaim_mode=0时，不会调用zone_reclaim函数，并把自己标记为zone_full。
4：继问题3，如果当前zone被标记为 zone_full，是不是就代表了zone的vmark_low分配失败了呢？

大概现象和问题差不多就是这些。非常希望老师能帮忙分析下。有相关资料推荐也行。特此感谢。

</div>2018-12-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/22/9a/989a3d8e.jpg" width="30px"><span>JJ</span> 👍（2） 💬（2）<div>为什么等待io也算进CPU使用率。。</div>2018-12-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1f/19/f3/f015a5ea.jpg" width="30px"><span>runzexia</span> 👍（1） 💬（1）<div>老师老师我有一个问题，现在很多时候应用是跑在容器里。用perf追踪的时候会显示16进制的名称，而不是系统库里的函数名。
在这种情况下我们怎么做会更方便的看系统调用是什么呢？</div>2020-06-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/cb/38/388560d1.jpg" width="30px"><span>地主</span> 👍（1） 💬（1）<div>非常非常好的专栏，感谢倪老师。</div>2019-07-01</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/cf/96/251c0cee.jpg" width="30px"><span>xindoo</span> 👍（1） 💬（1）<div>网络相关命令有个iftop</div>2019-06-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/42/8d/5e5d6bd7.jpg" width="30px"><span>三明</span> 👍（1） 💬（1）<div>老师你好，我问下用jprofiler统计的一个操作的某一个方法的cpu时间和该方法在整个操作中的耗时有什么区别</div>2019-03-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/93/43/0e84492d.jpg" width="30px"><span>Maxwell</span> 👍（1） 💬（2）<div>中断和上下文切换过多会导致系统CPU使用率(%sys)升高，对么？</div>2019-02-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/7c/59/26b1e65a.jpg" width="30px"><span>科学Jia</span> 👍（1） 💬（1）<div>老师，女同学继续举手发言：你画图的工具是什么？做的很精致！</div>2018-12-25</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/ac/a4/e51a1fd0.jpg" width="30px"><span>JasperHsu</span> 👍（1） 💬（1）<div>打卡。刚换了公司，这几天抽时间追上来</div>2018-12-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/17/07/83f030c9.jpg" width="30px"><span>kakasir</span> 👍（1） 💬（1）<div>这个总结太棒了，后面应该每一个阶段都有总结，新手看前面的课程基本消化不了，总结帮助很大</div>2018-12-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/11/fe/de00d8d8.jpg" width="30px"><span>王涛</span> 👍（1） 💬（1）<div>D11打卡。图片非常有用，感谢分享</div>2018-12-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/5c/b1/9e70e7aa.jpg" width="30px"><span>石壹笑</span> 👍（1） 💬（2）<div>我试了试我的机器 perf report 90%以上都是 swapper 😂</div>2018-12-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/75/54/73cc7f73.jpg" width="30px"><span>王旧业</span> 👍（1） 💬（1）<div>请问有pdf格式或者其他能够打印的讲义吗？想打印出来</div>2018-12-16</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/57/6e/b6795c44.jpg" width="30px"><span>夜空中最亮的星</span> 👍（1） 💬（1）<div>图已经拖拖的保存了，是不是就翻出来看看，在公司服务器上练练手。</div>2018-12-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/5b/52/fea5ec99.jpg" width="30px"><span>俊飞</span> 👍（1） 💬（1）<div>倪老师，后面的课程有关于内存使用情况的分析案例吗？我们这边大部分都是内存消耗严重，cpu使用都正常，找到了占用内存的应用进程，但又找不出这个应用进程具体哪里占用了大量内存，希望老师能指点迷津。</div>2018-12-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/af/11/aa5a4815.jpg" width="30px"><span>留意</span> 👍（1） 💬（1）<div>在看这篇文章之前，我还在考虑之前那么多各种工具到底怎么下手，今天看完，真是惊喜</div>2018-12-14</li><br/>
</ul>