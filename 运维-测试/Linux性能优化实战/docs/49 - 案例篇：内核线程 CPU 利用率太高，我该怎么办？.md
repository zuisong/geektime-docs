你好，我是倪朋飞。

上一期，我们一起梳理了，网络时不时丢包的分析定位和优化方法。先简单回顾一下。

网络丢包，通常会带来严重的性能下降，特别是对 TCP 来说，丢包通常意味着网络拥塞和重传，进而会导致网络延迟增大以及吞吐量降低。

而分析丢包问题，还是用我们的老套路，从 Linux 网络收发的流程入手，结合 TCP/IP 协议栈的原理来逐层分析。

其实，在排查网络问题时，我们还经常碰到的一个问题，就是内核线程的 CPU 使用率很高。比如，在高并发的场景中，内核线程 ksoftirqd 的 CPU 使用率通常就会比较高。回顾一下前面学过的 CPU 和网络模块，你应该知道，这是网络收发的软中断导致的。

而要分析 ksoftirqd 这类 CPU 使用率比较高的内核线程，如果用我前面介绍过的那些分析方法，你一般需要借助于其他性能工具，进行辅助分析。

比如，还是以 ksoftirqd 为例，如果你怀疑是网络问题，就可以用 sar、tcpdump 等分析网络流量，进一步确认网络问题的根源。

不过，显然，这种方法在实际操作中需要步骤比较多，可能并不算快捷。你肯定也很想知道，有没有其他更简单的方法，可以直接观察内核线程的行为，更快定位瓶颈呢？

今天，我就继续以 ksoftirqd 为例，带你一起看看，如何分析内核线程的性能问题。
<div><strong>精选留言（20）</strong></div><ul>
<li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/xzHDjCSFicNY3MUMECtNz6sM8yDJhBoyGk5IRoOtUat6ZIkGzxjqEqwqKYWMD3GjehScKvMjicGOGDog5FF18oyg/132" width="30px"><span>李逍遥</span> 👍（9） 💬（1）<div>老师，能讲讲内存火焰图生成perf.data数据时,perf record加哪些选项吗？</div>2019-04-03</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/xzHDjCSFicNY3MUMECtNz6sM8yDJhBoyGk5IRoOtUat6ZIkGzxjqEqwqKYWMD3GjehScKvMjicGOGDog5FF18oyg/132" width="30px"><span>李逍遥</span> 👍（9） 💬（1）<div>cpu火焰图和内存火焰图，在生成数据时有什么不同？</div>2019-04-01</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/8c/2b/3ab96998.jpg" width="30px"><span>青石</span> 👍（3） 💬（1）<div>两周时间，终于追上来了。

请问老师，有哪些书有助于通过内核函数来定位故障，Linux用了9年，看到这还是感觉有些吃力。

内核线程问题，我的环境和老师的有些区别，没有br_nf_pre_routing函数调用，但是从ip_forward推测与消息转发有关，sar发现有大量小包接收，conntrack -L看到大量本机到docker地址的SYN_SENT状态的连接、hping3服务器到测试服务器的SYN_RECV状态连接。初步定位到具体的docker。

上面思考的过程，有点因为知道问题点，所以朝这个方向走的感觉。</div>2019-03-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/80/6e/7f78292e.jpg" width="30px"><span>无</span> 👍（1） 💬（1）<div>请问有没有可以表示调用顺序的火焰图? 或者类似的其它图??? 感觉这样更有用阿</div>2022-02-05</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTKsz8j0bAayjSne9iakvjzUmvUdxWEbsM9iasQ74spGFayIgbSE232sH2LOWmaKtx1WqAFDiaYgVPwIQ/132" width="30px"><span>2xshu</span> 👍（1） 💬（1）<div>老师，这是最后一节课程吗？</div>2019-03-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/64/05/6989dce6.jpg" width="30px"><span>我来也</span> 👍（1） 💬（1）<div>[D49打卡]
之前用火焰图分析过golang程序的内存分配及cpu使用率情况.感觉非常直观.能快速找到瓶颈.</div>2019-03-18</li><br/><li><img src="https://wx.qlogo.cn/mmopen/vi_32/PiajxSqBRaEKQMM4m7NHuicr55aRiblTSEWIYe0QqbpyHweaoAbG7j2v7UUElqqeP3Ihrm3UfDPDRb1Hv8LvPwXqA/132" width="30px"><span>ninuxer</span> 👍（0） 💬（1）<div>打卡day52
有碰到一个内核问题，docker宿主机上kworker&#47;u80进程的cpu占用率一直100%，其他的kworker进程都正常，每隔几个月就会碰到一次，为了快速恢复业务，就直接重启了，主要是没办法在线下实验的时候复现问题，所以就没有深入的分析，后面碰到后，可以用老师的方法，把perf record采集一段时间的调用信息，然后拿出去分析下👍</div>2019-03-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/39/fa/a7edbc72.jpg" width="30px"><span>安排</span> 👍（5） 💬（0）<div>横轴的长短代表执行时间长短，一个函数被调用多次那横轴很长，一个函数执行一次但是在里面休眠了，这算执行时间很长吗？on-cpu火焰图是不是只记录真正的在cpu上的执行时间而不把睡眠时间算在内？</div>2020-01-27</li><br/><li><img src="" width="30px"><span>opdozz</span> 👍（1） 💬（0）<div>老师，最近碰到一个kworker内核进程问题，48C的服务器，docker宿主机， 某个kworker会占满两个CPU，一个sys跑满，另外一个iowait跑满，剩下的CPU都很空闲，但是业务处理很慢，重启之后就好了，但是过段时间又复发， 不规律。
perf收集了信息，__rpc_execute 这个调用占了很多，下层nfs4_xdr_enc_open调用也占了很多，和挂的nas存储有关系吗，但是存储那边排查没有任何问题。</div>2021-07-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/3b/36/2d61e080.jpg" width="30px"><span>行者</span> 👍（1） 💬（0）<div>很赞，准备回去用火焰图分析下我们后端服务。^ _ ^</div>2019-03-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/60/b1/0cd5929d.jpg" width="30px"><span>Calvin</span> 👍（0） 💬（0）<div>请教老师个问题，driver可以用perf分析吗？强制中断线程化后，硬中断和软中断都在irq内核线程执行 但perf只能采样到软中断处理栈 没有任何硬中断栈 google了下有人提到硬中断处理会关中断，导致perf的硬件中断不能触发 希望老师帮忙详细解释下</div>2023-09-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/fa/03/eba78e43.jpg" width="30px"><span>风清扬</span> 👍（0） 💬（0）<div>$ ps -ef | grep &quot;\[.*\]&quot;
与ps -ef | grep &quot;\[*\]&quot; 有啥区别，为啥要加.?


</div>2023-01-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/62/dc/8876c73b.jpg" width="30px"><span>moooofly</span> 👍（0） 💬（0）<div>“到这里，我们就找出了内核线程 ksoftirqd 执行最频繁的函数调用堆栈，而这个堆栈中的各层级函数，就是潜在的性能瓶颈来源。这样，后面想要进一步分析、优化时，也就有了根据。” -- 然后呢，我还是不知道要如何解决，在高并发的场景中，内核线程 ksoftirqd 的 CPU 使用率高的问题……</div>2022-11-11</li><br/><li><img src="" width="30px"><span>Geek_1b7d36</span> 👍（0） 💬（1）<div>top发现load average : 2270.00  ,2270.26,  2270.26,
但是cpu使用率不超过10% ，32C64G的机器，其他的进程的CPU很低，就是这个负载很高，这个怎么排查呢，老师</div>2022-05-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/99/7a/558666a5.jpg" width="30px"><span>AceslupK</span> 👍（0） 💬（1）<div>此处火焰图，吃力了。依旧还是没看明白该怎么找出未知问题，还是觉得这次是有着方向的解决问题</div>2021-10-15</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/4Lprf2mIWpJOPibgibbFCicMtp5bpIibyLFOnyOhnBGbusrLZC0frG0FGWqdcdCkcKunKxqiaOHvXbCFE7zKJ8TmvIA/132" width="30px"><span>Geek_c2089d</span> 👍（0） 💬（1）<div>执行  
perf script -i &#47;root&#47;perf.data | .&#47;stackcollapse-perf.pl --all |  .&#47;flamegraph.pl &gt; ksoftirqd.svg
会报ERROR: No stack counts found错误，但是权限是都777的</div>2020-12-18</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTJGMphabeneYRlxs1biaO9oKic6Dwgbe312561lE56V93uUHgXXAsGmK1pH18mvpElygoJh8SUtQPUA/132" width="30px"><span>董皋</span> 👍（0） 💬（0）<div>打卡</div>2020-03-20</li><br/><li><img src="" width="30px"><span>Littlesoup</span> 👍（0） 💬（1）<div>&quot;一个函数占用的横轴越宽，就代表它的执行时间越长。&quot;
&quot;另外，整个火焰图不包含任何时间的因素，所以并不能看出横向各个函数的执行次序。&quot;
原文这两句话读起来有点困惑，第二句的意思是不是不包含任何时序的因素？</div>2019-11-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/18/97/e1/0f4d90ff.jpg" width="30px"><span>乖，摸摸头</span> 👍（0） 💬（1）<div>为啥我的一值都是显示的16进制而不是函数名</div>2019-10-15</li><br/><li><img src="" width="30px"><span>如果</span> 👍（0） 💬（0）<div>DAY49，打卡
</div>2019-04-17</li><br/>
</ul>