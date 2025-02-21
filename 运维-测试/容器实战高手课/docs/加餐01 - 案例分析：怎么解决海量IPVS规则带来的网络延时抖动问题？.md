你好，我是程远。

今天，我们进入到了加餐专题部分。我在结束语的彩蛋里就和你说过，在这个加餐案例中，我们会用到perf、ftrace、bcc/ebpf这几个Linux调试工具，了解它们的原理，熟悉它们在调试问题的不同阶段所发挥的作用。

加餐内容我是这样安排的，专题的第1讲我先完整交代这个案例的背景，带你回顾我们当时整个的调试过程和思路，然后用5讲内容，对这个案例中用到的调试工具依次进行详细讲解。

好了，话不多说。这一讲，我们先来整体看一下这个容器网络延时的案例。

## 问题的背景

在2020年初的时候，我们的一个用户把他们的应用从虚拟机迁移到了Kubernetes平台上。迁移之后，用户发现他们的应用在容器中的出错率很高，相比在之前虚拟机上的出错率要高出一个数量级。

那为什么会有这么大的差别呢？我们首先分析了应用程序的出错日志，发现在Kubernetes平台上，几乎所有的出错都是因为网络超时导致的。

经过网络环境排查和比对测试，我们排除了网络设备上的问题，那么这个超时就只能是容器和宿主机上的问题了。

这里要先和你说明的是，尽管应用程序的出错率在容器中比在虚拟机里高出一个数量级，不过这个出错比例仍然是非常低的，在虚拟机中的出错率是0.001%，而在容器中的出错率是0.01%~0.04%。
<div><strong>精选留言（10）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/14/e3/9e/b26da70d.jpg" width="30px"><span>closer</span> 👍（9） 💬（3）<div>看了老师的文章涨见识了。深深的知道了自己的不足了，请问一下老师，作为一个运维工程师，怎么学习这种底层的内核开发细节？谢谢老师指导</div>2021-01-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/64/05/6989dce6.jpg" width="30px"><span>我来也</span> 👍（8） 💬（2）<div>大集群就容易遇到IPVS规则过多的问题吧。

有点好奇
1. 集群中的其他节点应该也会存在类似的问题吧。
2.每次都是固定在这一个核上做这个事情么？</div>2021-02-06</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/5e/96/a03175bc.jpg" width="30px"><span>莫名</span> 👍（5） 💬（2）<div>很赞的排查思路。

softirq 通常是节点内网络延迟的重要线索。不借助 eBPF 工具时，可以先采用传统工具 top、mpstat 重点观测下 softirq CPU 使用率是否存在波动或者持续走高的情况。如果存在，进一步使用 perf 进行热点函数分析。

不过使用现有的 eBPF softirq 相关工具更方便。</div>2021-01-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/0f/70/cdef7a3d.jpg" width="30px"><span>Joe Black</span> 👍（4） 💬（1）<div>“把 IPVS 规则的状态统计从 TIMER softirq 中转移到 kernel thread 中处理”，这个事情是通过什么配置就可以实现的吗？总不能改内核模块吧？</div>2021-02-04</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/8f/cf/890f82d6.jpg" width="30px"><span>那时刻</span> 👍（4） 💬（1）<div>请问老师，IPVS过多是由于service导致的么？还是旧service遗留导致的呢？
另外，不知可否分享下您实现的ebpf工具呢？</div>2021-01-29</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/Um0fKCDsGBRStZBF1M4HLPSq8jiancnNoYKiaYyYldFX0NObkyUFmnVKTgjm6Y7wUiaCQ3Vm9Ic213l65kJfUzq4w/132" width="30px"><span>Geek_c92584</span> 👍（0） 💬（1）<div>干货满满，赞</div>2021-07-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/0c/30/d4737cd5.jpg" width="30px"><span>lyonger</span> 👍（5） 💬（0）<div>整体排查思路：
查看系统整体负载情况 -&gt; 缩小问题的请求链路和排查范围 -&gt; 采用ebpf给请求链路上的内核关键函数加上时间戳，分析时间差较长的环节，定位到cpu si高 -&gt; perf针对高cpu使用率进行热点函数分析，找出调用次数最频繁的函数 -&gt; 是调用次数频繁导致 or 本身执行一次该热点函数执行时间长导致？ -&gt; 使用ftrace分析热点参数在每个CPU上的执行时间 -&gt; 根据内核源码，分析该热点函数的执行逻辑 -&gt; 操作系统原理 -&gt; 破案。
</div>2021-09-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/38/34/e2/21859878.jpg" width="30px"><span>yell</span> 👍（1） 💬（0）<div>采样10秒，怎么抓到0.01概率的超时的。</div>2023-07-28</li><br/><li><img src="" width="30px"><span>Geek_9234b0</span> 👍（1） 💬（0）<div>给跪了</div>2021-10-23</li><br/><li><img src="" width="30px"><span>从远方过来</span> 👍（0） 💬（0）<div>老师，分享下下分析脚本吧</div>2021-06-30</li><br/>
</ul>