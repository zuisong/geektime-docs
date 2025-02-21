你好，我是倪朋飞。

上一期我给你讲了软中断的基本原理，我们先来简单复习下。

中断是一种异步的事件处理机制，用来提高系统的并发处理能力。中断事件发生，会触发执行中断处理程序，而中断处理程序被分为上半部和下半部这两个部分。

- 上半部对应硬中断，用来快速处理中断；
- 下半部对应软中断，用来异步处理上半部未完成的工作。

Linux 中的软中断包括网络收发、定时、调度、RCU锁等各种类型，我们可以查看 proc 文件系统中的 /proc/softirqs ，观察软中断的运行情况。

在 Linux 中，每个 CPU 都对应一个软中断内核线程，名字是 ksoftirqd/CPU编号。当软中断事件的频率过高时，内核线程也会因为CPU 使用率过高而导致软中断处理不及时，进而引发网络收发延迟、调度缓慢等性能问题。

软中断 CPU 使用率过高也是一种最常见的性能问题。今天，我就用最常见的反向代理服务器 Nginx 的案例，教你学会分析这种情况。

## 案例

### 你的准备

接下来的案例基于 Ubuntu 18.04，也同样适用于其他的 Linux 系统。我使用的案例环境是这样的：

- 机器配置：2 CPU、8 GB 内存。
- 预先安装 docker、sysstat、sar 、hping3、tcpdump 等工具，比如 apt-get install [docker.io](http://docker.io) sysstat hping3 tcpdump。
<div><strong>精选留言（30）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/0f/47/42/5b55bd1a.jpg" width="30px"><span>倪朋飞</span> 👍（62） 💬（5）<div>统一回复一下终端卡顿的问题，这个是由于网络延迟增大（甚至是丢包）导致的。比如你可以再拿另外一台机器（也就是第三台）在 hping3 运行的前后 ping 一下案例机器，ping -c3 &lt;ip&gt;

hping3 运行前，你可能看到最长的也不超过 1 ms：

3 packets transmitted, 3 received, 0% packet loss, time 2028ms
rtt min&#47;avg&#47;max&#47;mdev = 0.815&#47;0.914&#47;0.989&#47;0.081 ms

而 hping3 运行时，不仅平均延迟增长到了 245 ms，而且还会有丢包的发生：

3 packets transmitted, 2 received, 33% packet loss, time 2026ms
rtt min&#47;avg&#47;max&#47;mdev = 240.637&#47;245.758&#47;250.880&#47;5.145 ms

网络问题的排查方法在后面的文章中还会讲，这儿只是从 CPU 利用率的角度出发，你可以发现也有可能是网络导致的问题。</div>2018-12-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/1b/ca/9afb89a2.jpg" width="30px"><span>Days</span> 👍（112） 💬（6）<div>软终端不高导致系统卡顿，我的理解是这样的，其实不是系统卡顿，而是由于老师用的ssh远程登录，在这期间hping3大量发包，导致其他网络连接延迟，ssh通过网络连接，使ssh客户端感觉卡顿现象。</div>2018-12-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/de/70/52b1d5ab.jpg" width="30px"><span>不去会死</span> 👍（41） 💬（1）<div>搞运维好些年了。一些底层性能的东西，感觉自己始终是一知半解，通过这个专栏了解的更深入了，确实学到了很多。而且老师也一直在积极回复同学们的问题，相比某些专栏的老师发出来就不管的状态好太多。给老师点赞。
</div>2018-12-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/5c/2b/25c1c14c.jpg" width="30px"><span>卿卿子衿</span> 👍（36） 💬（5）<div>有同学说在查看软中断数据时会显示128个核的数据，我的也是，虽然只有一个核，但是会显示128个核的信息，用下面的命令可以提取有数据的核，我的1核，所以这个命令只能显示1核，多核需要做下修改

watch -d &quot;&#47;bin&#47;cat &#47;proc&#47;softirqs | &#47;usr&#47;bin&#47;awk &#39;NR == 1{printf  \&quot;%13s %s\n\&quot;,\&quot; \&quot;,\$1}; NR &gt; 1{printf \&quot;%13s %s\n\&quot;,\$1,\$2}&#39;&quot;</div>2018-12-12</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTKsz8j0bAayjSne9iakvjzUmvUdxWEbsM9iasQ74spGFayIgbSE232sH2LOWmaKtx1WqAFDiaYgVPwIQ/132" width="30px"><span>2xshu</span> 👍（14） 💬（1）<div>老师，网络软中断明明只占了百分之四左右。为什么终端会感觉那么卡呢？不是很理解这点呢</div>2018-12-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/64/05/6989dce6.jpg" width="30px"><span>我来也</span> 👍（9） 💬（2）<div>[D10打卡]
 &quot;hping3 -S -p 80 -i u100 192.168.0.30&quot; 这里的u100改为了1 也没觉得终端卡,top的软中断%si倒是从4%上升了不少,吃满了一个cpu.
可能是我直接在宿主机上开终端的原因,本身两个虚拟机都在这个宿主机上,都是走的本地网络.
本地网卡可能还处理的过来.
-----------
在工作中,倒是没有遇到小包导致的性能问题.
也许是用户数太少,流量不够.[才二三十兆带宽], 也许是之前发生了,自己并不知道.
在工作中遇到的软中间导致的性能问题就是上期说的usleep(1)了.
-----------
本期又学到新东西了:
1.sar 原来可以这么方便的看各网卡流量,甚至是网络帧数.
到目前为止,我都是用的最原始的方法:在网上找的一个脚本,分析ifconfig中的数据,来统计某个网卡的流量.一来需要指定某个网卡(默认eth0),二来显示的数据不太准确且不友好(sleep 1做差值).
2.nping3 居然可以用来模拟SYN FLOOD. (不要用来做坏事哦)
3.tcpdump 之前有所耳闻. 用的不多. 平常有解包需求,都是在windows下用wireshark,毕竟是图形界面.
-----------
有同学说&quot;仅凭tcpdump发现一个syn包就断定是SYN FLOOD，感觉有些草断&quot;
我是这样认为的:
你tcpdump 截取一段时间的日志, 除去正常的流量, 着重分析异常的,再根据ip来统计出现的次数, 还是可以合理推理出来老师结论的.
毕竟平常不会有哪个ip每秒产生这么多的syn,且持续这么长时间.</div>2018-12-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/75/dd/9ead6e69.jpg" width="30px"><span>黄海峰</span> 👍（8） 💬（1）<div>这真是非常干货和务实的一个专栏，这么便宜，太值了。。。</div>2018-12-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/54/98/52ca7053.jpg" width="30px"><span>Vicky🐣🐣🐣</span> 👍（6） 💬（2）<div>1. 网络收发软中断过多导致命令行比较卡，是因为键盘敲击命令行属于硬中断，内核也需要去处理的原因吗？
2. 观察&#47;proc&#47;softirqs，发现变化的值是TIMER、NET_RX、BLOCK、RCU，奇怪的是SCHED一直为0，求老师解答</div>2018-12-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/11/4b/fa64f061.jpg" width="30px"><span>xfan</span> 👍（5） 💬（1）<div>ssh的tty其实也是通过网络传输的，既然是经过网卡，当然会卡，这就是攻击所带来的结果</div>2018-12-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/14/3a/94e25d0c.jpg" width="30px"><span>男人十八一枝花</span> 👍（4） 💬（4）<div>cat &#47;proc&#47;softirqs时我有4个cpu，可用
watch -d &quot;&#47;bin&#47;cat &#47;proc&#47;softirqs | &#47;usr&#47;bin&#47;awk &#39;NR == 1{printf \&quot;%-15s %-15s %-15s %-15s %-15s\n\&quot;,\&quot; \&quot;,\$1,\$2,\$3,\$4}; NR &gt; 1{printf \&quot;%-15s %-15s %-15s %-15s %-15s\n\&quot;,\$1,\$2,\$3,\$4,\$5}&#39;&quot;
查看</div>2018-12-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/a7/fa/1dca9fd5.jpg" width="30px"><span>王星旗</span> 👍（3） 💬（2）<div>hping3 -S --flood  -p 80 ip，这样压力更大，哈哈</div>2019-06-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/26/08/a59f930b.jpg" width="30px"><span>LT</span> 👍（3） 💬（2）<div>如果设备cpu核数比较多，比如，40核的设备，cat &#47;proc&#47;softirqs每行在屏幕换行了，几乎没法看。有没有其他合适的查看工具

</div>2018-12-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/c1/2a/e7102065.jpg" width="30px"><span>wking</span> 👍（2） 💬（2）<div>老师，你经常使用tcpdump，但是真正在线上环境是不能随便使用的。比如我们线上环境，如果使用tcpdump一分钟左右就产生1G的文档，有些问题也不是经常出现，如果一直使用tcpdump，系统受不了。老师，有什么好办法吗？</div>2019-08-15</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/7a/8e/934cbcbc.jpg" width="30px"><span>几叶星辰</span> 👍（2） 💬（1）<div>怎么让网卡中断平衡呢，可以请教下linux 2.6.40。中断平衡问题吗，以及内核版本更高的版本？</div>2019-01-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/54/98/52ca7053.jpg" width="30px"><span>Vicky🐣🐣🐣</span> 👍（2） 💬（1）<div>执行了一下hping3，机器直接卡死了，登录不上去了，哈哈</div>2018-12-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/f4/50/3b604b3b.jpg" width="30px"><span>chenjt</span> 👍（2） 💬（1）<div>同问，这种情况下cpu使用率这么低，为什么会感到卡顿呢</div>2018-12-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/58/25/2088864b.jpg" width="30px"><span>林贻民</span> 👍（1） 💬（1）<div>老师您好，有个问题，既然中断分上部分（硬中断，快速处理）和下部分（软中断，消耗一定时间）， 那为什么， SYC FLOOD时只有软中断的CPU利用率升高而硬件中断的CPU使用率没有升高呢？</div>2019-05-28</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTIkkg9icSGleYMAnwlb7A9MMJYOdovl8kOCA0asMkDe6grPNF74ib0prQMicicJTNa1WsdpMJ4p1CWkUQ/132" width="30px"><span>shawn</span> 👍（1） 💬（1）<div>既然卡顿是由于网络攻击造成的，并且cpu的使用率没有提高，那么标题可否换一下呢？</div>2019-05-06</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/c4/4a/c02c597b.jpg" width="30px"><span>Joe</span> 👍（1） 💬（1）<div>从网络统计中看到很大的流量，有没有办法知道流量到底是访问哪个端口呢？</div>2019-04-06</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/65/ae/9727318e.jpg" width="30px"><span>Boy-struggle</span> 👍（1） 💬（1）<div>此问题的关键一部是如何判断因为中断导致的性能问题，中断指标不像其他那么直白，还是需要进行监控</div>2019-03-08</li><br/><li><img src="" width="30px"><span>元天夫</span> 👍（1） 💬（1）<div>有个问题，网络收到的数据。平均每帧多少算是小包呢，文中是50字节，如果是200或者300字节算是小包吗</div>2019-02-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/93/43/0e84492d.jpg" width="30px"><span>Maxwell</span> 👍（1） 💬（2）<div>我用的是vmware虚拟机，网络连接是NAT,CPU是 I7 8750U 4C8T,运行案例场景时，并没有任何卡顿?
还有，我这边使用 sar命令查看的结果和你的差别很大是什么原因呢？
18时23分07秒     ens33   4462.00   2237.00    261.45    127.87      0.00      0.00      0.00     31.89</div>2019-02-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/71/ec/bfecf21b.jpg" width="30px"><span>keyboard_chen_-</span> 👍（1） 💬（1）<div>这个案例刚好是其他进程cpu利用率低，假如其他进程利用率比较高时，是不是比较难定位是软中断的问题了？</div>2019-02-08</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTL9hlAIKQ1sGDu16oWLOHyCSicr18XibygQSMLMjuDvKk73deDlH9aMphFsj41WYJh121aniaqBLiaMNg/132" width="30px"><span>腾达</span> 👍（1） 💬（1）<div>除了网络，如果是其他类型的si，该如何判断是由何种程序引起的si? 先找到引起si的类型，再怎么找呢？本文里是通过&#47;proc&#47;softirqs找到类型，再通过sar找到网络问题，如果是其他类型的softirq，该如何办？</div>2018-12-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/7d/17/179b24f4.jpg" width="30px"><span>燕羽阳</span> 👍（1） 💬（1）<div>
请教一下：
1.卡的核心原因是因为pps比较高么？
2.pps的上限一般是由网卡确定么？</div>2018-12-13</li><br/><li><img src="" width="30px"><span>bluefantasy1</span> 👍（1） 💬（2）<div>老师，既然软中断并没有占用太多cpu资源，为啥会影响其他任务的性能？</div>2018-12-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/e2/ab/430c24df.jpg" width="30px"><span>zqing</span> 👍（1） 💬（1）<div>同问:老师，网络软中断明明只占了百分之四左右。为什么终端会感觉那么卡呢？不是很理解这点呢</div>2018-12-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/4d/49/28e73b9c.jpg" width="30px"><span>明翼</span> 👍（0） 💬（1）<div>不知道老师还看留言不，遇到一个问题请教，我用tcpreplay对另外一台机器的直连网卡p1p2去打流量，如果用我程序抓这个p1p2的包发现网卡lo的流量很大，对端发送的速度就上不去，如果不抓流量则流量上的去都体现在p1p2上了请问是什么原因，用sar看的流量情况</div>2019-06-30</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/55/86/ca7c94ce.jpg" width="30px"><span>羁绊12221</span> 👍（0） 💬（1）<div>老师好，我是从网络部分跳回来的，按照网络部分的说法，包达到网卡后通过DMA方式进入收包队列，然后通过硬中断将包拷贝到sk_buffer中，再通知软中断处理。。。在syn flood的场景中，应该硬中断和软中断次数都非常多才对，为什么只有软中断比较多，%softirq比较高？希望老师能解惑，非常感谢！！！</div>2019-05-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/9b/a8/6a391c66.jpg" width="30px"><span>geraltlaush</span> 👍（0） 💬（1）<div>老师，我有个疑惑，cpu使用率和用户cpu和系统cpu，iowait还有软硬中断有关，我们这几篇讲iowait和软中断，都是软中断和iowait很高，但是cpu的使用率却并没有上升，如果没有直接关联性，那iowait和软硬中断怎么算影响cpu使用率的影响因子呢</div>2019-05-01</li><br/>
</ul>