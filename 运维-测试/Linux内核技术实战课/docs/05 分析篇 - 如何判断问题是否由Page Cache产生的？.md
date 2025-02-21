你好，我是邵亚方。

在前面几节课里，我们讲了Page Cache的一些基础知识，以及如何去处理Page Cache引发的一些问题。这节课我们来讲讲，如何判断问题是不是由Page Cache引起的。

我们知道，一个问题往往牵扯到操作系统的很多模块，比如说，当系统出现load飙高的问题时，可能是Page Cache引起的；也可能是锁冲突太厉害，物理资源（CPU、内存、磁盘I/O、网络I/O）有争抢导致的；也可能是内核特性设计缺陷导致的，等等。

如果我们没有判断清楚问题是如何引起的而贸然采取措施，非但无法解决问题，反而会引起其他负面影响，比如说，load飙高本来是Page Cache引起的，如果你没有查清楚原因，而误以为是网络引起的，然后对网络进行限流，看起来把问题解决了，但是系统运行久了还是会出现load飙高，而且限流这种行为还降低了系统负载能力。

那么当问题发生时，我们如何判断它是不是由Page Cache引起的呢？

## Linux问题的典型分析手段

Linux上有一些典型的问题分析手段，从这些基本的分析方法入手，你可以一步步判断出问题根因。这些分析手段，可以简单地归纳为下图：

![](https://static001.geekbang.org/resource/image/ee/c1/ee08329fc5eb7fb8ddff14dba9ebf0c1.jpg?wh=2200%2A1184 "Linux的典型分析手段")

从这张图中我们可以看到，Linux内核主要是通过/proc和/sys把系统信息导出给用户，当你不清楚问题发生的原因时，你就可以试着去这几个目录下读取一下系统信息，看看哪些指标异常。比如当你不清楚问题是否由Page Cache引起时，你可以试着去把/proc/vmstat里面的信息给读取出来，看看哪些指标单位时间内变化较大。如果pgscan相关指标变化较大，那就可能是Page Cache引起的，因为pgscan代表了Page Cache的内存回收行为，它变化较大往往意味着系统内存压力很紧张。
<div><strong>精选留言（13）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/1e/3b/d7/9d942870.jpg" width="30px"><span>邵亚方</span> 👍（18） 💬（0）<div>课后作业答案：
- 假设现在内存紧张， 有很多进程都在进行直接内存回收，如何统计出来都是哪些进程在进行直接内存回收呢？
评论区里有人已经很好的回答了这个问题，使用tracepoint是最简单的方法。
“已经得知是直接内存回收引起的问题，一次执行
echo 1 &gt;&#47;sys&#47;kernel&#47;debug&#47;tracing&#47;events&#47;vmscan&#47;mm_vmscan_direct_reclaim_begin
echo 1 &gt;&#47;sys&#47;kernel&#47;debug&#47;tracing&#47;events&#47;vmscan&#47;mm_vmscan_direct_reclaim_end
打开直接内存回收相关的tracepoint，然后
cat &#47;sys&#47;kernel&#47;debug&#47;tracing&#47;trace_pipe
查看跟踪输出，得到进程号“</div>2020-10-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/64/05/6989dce6.jpg" width="30px"><span>我来也</span> 👍（12） 💬（1）<div>邵老师，看了文中的一句话，正好有个困扰很久的疑问请教一下：
我们什么时候会真的遇到需要申请连续物理内存的情况？

&gt; “单位时间内 compact_fail 变化很大时，那往往意味着系统内存碎片很严重，已经很难申请到连续物理内存了”
这里提到了“连续物理内存”。
平常也经常会看到这个描述。

我们知道，每个用户进程都有自己独立的虚拟内存地址空间。
自己申请到的内存地址其实只是进程虚拟内存中的一个地址，并不是实际的物理内存地址。
只有自己在用到了对应的虚拟地址时才会，系统才会通过缺页异常来分配具体的物理地址。

而系统的内存一般都是4k一个页表。
很有可能在进程中连续的虚拟内存地址，在实际的物理内存中并不是连续的。
现在几乎都只有内核有权限直接操作物理内存了。

所以我就有了开头的那个疑问。</div>2020-08-30</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/64/9b/d1ab239e.jpg" width="30px"><span>J.Smile</span> 👍（9） 💬（2）<div>sar 里面记录的 PSI（Pressure-Stall Information）具体怎么用啊？</div>2020-08-29</li><br/><li><img src="https://wx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTIt0nAFvqib3fpf9AIKUrEJMdbiaPjnKqCryevwjRdqrbzAIxdOn3P5wCz28MNb5Bgb2PwEdCezLEWg/132" width="30px"><span>KennyQ</span> 👍（6） 💬（1）<div>很多生产问题都是要对秒级甚至毫秒级的行为进行分析，而业务一旦向运维部门反馈了问题以后，一般都是要做事后分析， 那么一般如何应对这样的问题分析场景？
是针对一些重要指标在事前就进行秒级监控？分钟级监控？还是等待事后部署秒级的监控脚本进行信息抓取？</div>2020-09-05</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1e/e8/ec/faed0b4f.jpg" width="30px"><span>Eria</span> 👍（6） 💬（1）<div>请教老师一个问题：我们两个机器上一样的系统和硬件配置和服务，运行相同的测试：

    1. 系统 A 的磁盘 util 很小（3%-10%），但是可以看到 80G 左右的 buffer&#47;cache，系统 A 的服务延迟非常小
    2. 系统 B 的磁盘 util 很高（大于 30%)，buffer&#47;cache 10G 左右，系统 B 的服务延迟是 A 的好几倍

系统 B 是否可能由于太小的 buffer&#47;cache 导致 disk util 飙高进而导致延迟上升？两个系统的 cahce 参数配置是一样的，所以为什么系统 B 的 buffer&#47;cache 会比系统 A 小那么多？</div>2020-09-02</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/DYAIOgq83epUBQibdMCca340MFZOe5I1GwZ0PosPIzA0TPCNzibgH00w45Zmv4jmL0mFRHMUM9FuKiclKOCBjSmsw/132" width="30px"><span>Geek_circle</span> 👍（5） 💬（1）<div>老师好，想确认下页面的换出是否依赖系统开启的swap分区（一般linux系统为了避免影响性能，都是关闭不启用swap的），如果不依赖，这个换出的页面是放置在物理硬盘的哪里呢？
.这个sar统计的pgpgin和pgpgout 如何解读呢</div>2020-09-13</li><br/><li><img src="" width="30px"><span>ray</span> 👍（5） 💬（2）<div>老师您好，请问
==&gt; &#47;proc&#47;pressure&#47;cpu &lt;==
some avg10=0.00 avg60=0.00 avg300=0.00 total=10078249

==&gt; &#47;proc&#47;pressure&#47;io &lt;==
some avg10=18.04 avg60=17.66 avg300=19.08 total=1334977849
full avg10=17.54 avg60=16.98 avg300=18.49 total=1294527367

==&gt; &#47;proc&#47;pressure&#47;memory &lt;==
some avg10=0.00 avg60=0.00 avg300=0.00 total=0
full avg10=0.00 avg60=0.00 avg300=0.00 total=0

1. 上述cpu, io, memory指标的avg的计算方式是，单位 &#47; 秒数，我的疑问是这3个指标是用什么单位除以秒数计算出平均值？（以memory为例，可能是page &#47; s，但我不是很清楚单位是否是page）

2. total代表的意思是什么？

谢谢老师的解答^^</div>2020-08-30</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/9b/ba/333b59e5.jpg" width="30px"><span>Linuxer</span> 👍（3） 💬（1）<div>请问一下邵老师，如何确定负载高是锁冲突导致的呢？还有就是象 resource temporarily unavailable这种报错我想知道具体是哪一种资源，是不是可以通过系统快照找到呢？</div>2020-10-22</li><br/><li><img src="https://wx.qlogo.cn/mmopen/vi_32/DYAIOgq83eqtXSgThiaEiaEqqic5YIJ7v469nCM3VXiccOJ4SxbYjW91ciczuYYEzcTVtYWaWXaokZqShuLdKsXjnFA/132" width="30px"><span>Geek_b85295</span> 👍（2） 💬（1）<div>关于课后作业，我来依葫芦画瓢，还望老师指教。
已经得知是直接内存回收引起的问题，一次执行
echo 1 &gt;&#47;sys&#47;kernel&#47;debug&#47;tracing&#47;events&#47;vmscan&#47;mm_vmscan_direct_reclaim_begin
echo 1 &gt;&#47;sys&#47;kernel&#47;debug&#47;tracing&#47;events&#47;vmscan&#47;mm_vmscan_direct_reclaim_end
打开直接内存回收相关的tracepoint，然后
cat &#47;sys&#47;kernel&#47;debug&#47;tracing&#47;trace_pipe
查看跟踪输出，得到进程号</div>2020-09-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/5a/56/115c6433.jpg" width="30px"><span>jssfy</span> 👍（2） 💬（1）<div>请问老师你们生产环境是否用4.18+内核多? 还是定制迁移相关特性到自维护版本内核?</div>2020-08-30</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/e3/8b/27f875ba.jpg" width="30px"><span>Bryant.C</span> 👍（0） 💬（1）<div>老师好，在老版本(2.6.32)里面有没有比较好的方式检测机器整体page cache的命中率呢？page cache命中这个指标对于我们的服务还是相当重要的，如果使用systemtap监控函数调用的话会不会有很高的开销呢？</div>2020-10-15</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1f/73/66/a71aa8c1.jpg" width="30px"><span>Arcoo</span> 👍（1） 💬（0）<div>【你需要重点关注 avg10 这一列，它表示最近 10s 内存的平均压力情况，如果它很大（比如大于 40）那 load 飙高大概率是由于内存压力，尤其是 Page Cache 的压力引起的。】
压力的大小该如何界定，40代表压力很大，那 10、20 就表示压力不大？
我该如何评估系统的压力是否大？</div>2022-06-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/38/5e/f0394817.jpg" width="30px"><span>费曼先生</span> 👍（0） 💬（0）<div>邵老师，目前我这边操作系统版本是 CentOS Linux release 7.9.2009 (Core) 为什么我在主机上无法找到&#47;sys&#47;kernel&#47;debug&#47;tracing&#47;events&#47;compaction&#47;mm_compaction_begin&#47;enable这个文件呐？是因为操作系统不同引起的嘛？</div>2022-10-09</li><br/>
</ul>