你好，我是邵亚方。

我们在基础篇和案例篇里讲了很多问题，比如说RT抖动问题、丢包问题、无法建连问题等等。这些问题通常都会伴随着TCP重传，所以我们往往也会抓取TCP重传信息来辅助我们分析这些问题。

而且TCP重传也是一个信号，我们通常会利用这个信号来判断系统是否稳定。比如说，如果一台服务器的TCP重传率很高，那这个服务器肯定是存在问题的，需要我们及时采取措施，否则可能会产生更加严重的故障。

但是，TCP重传率分析并不是一件很容易的事，比如说现在某台服务器的TCP重传率很高，那究竟是什么业务在进行TCP重传呢？对此，很多人并不懂得如何来分析。所以，在这节课中，我会带你来认识TCP重传是怎么回事，以及如何来高效地分析它。

## 什么是TCP重传 ？

我在“[开篇词](https://time.geekbang.org/column/article/273544)”中举过一个TCP重传率的例子，如下图所示：

![](https://static001.geekbang.org/resource/image/ab/f6/ab358c52ede21f0983fe7dfb032dc3f6.jpg?wh=896%2A488)

这是互联网企业普遍都有的TCP重传率监控，它是服务器稳定性的一个指标，如果它太高，就像上图中的那些毛刺一样，往往就意味着服务器不稳定了。那TCP重传率究竟表示什么呢？

其实TCP重传率是通过解析/proc/net/snmp这个文件里的指标计算出来的，这个文件里面和TCP有关的关键指标如下：

![](https://static001.geekbang.org/resource/image/d5/e7/d5be65df068c3a2c4d181f492791efe7.jpg?wh=2460%2A1592)

TCP重传率的计算公式如下：
<div><strong>精选留言（7）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/1e/3b/d7/9d942870.jpg" width="30px"><span>邵亚方</span> 👍（12） 💬（0）<div>
课后作业答案：
- 请问我们提到的 tracepoint 观察方式，或者 tcpretrans 这个工具，可以追踪收到的 TCP 重传包吗？为什么？
不可以，因为tracepoint是在发送的地方进行打点来追踪的重传包，所以无法追踪收到的重传包。</div>2020-10-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/4c/49/125f5adc.jpg" width="30px"><span>mazhen</span> 👍（10） 💬（1）<div>从本文了解到的ftrace简直打开了新天地。
学习后写了篇ftrace的介绍文章 https:&#47;&#47;github.com&#47;mz1999&#47;blog&#47;blob&#47;master&#47;docs&#47;ftrace.md</div>2021-06-30</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/4a/2c/f8451d77.jpg" width="30px"><span>石维康</span> 👍（2） 💬（0）<div>『如果你觉得实现内核模块比较麻烦，可以借助 ftrace 框架来使用 Kprobe。Brendan Gregg 实现的tcpretrans采用的就是这种方式，你也可以直接使用它这个工具来追踪 TCP 重传。』

『。它通过解析该 Tracepoint 实现了对 TCP 重传事件的追踪，而不再使用之前的 Kprobe 方式，』</div>2020-09-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/17/d9/9a098646.jpg" width="30px"><span>lxwCoding</span> 👍（0） 💬（0）<div>弱网情况下如何保证网络数据传输</div>2024-08-15</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/4d/49/28e73b9c.jpg" width="30px"><span>明翼</span> 👍（0） 💬（0）<div>有个问题请教，一次重传，总发包数也会增加，那么重传率为什么可以超过百分之百？</div>2023-05-02</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/5c/bd/f5d0a2c8.jpg" width="30px"><span>逗比</span> 👍（0） 💬（0）<div>最近遇到一个情况，关掉接收方的网卡GRO就没有重传，乱序，重复ack现象，但是不知道为什么

场景：A（虚拟机ip） -&gt; B(虚拟机ip:port)， ipvs转发到某一台pod ip，其实就是一个普通的k8s service</div>2022-08-30</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/3a/a5/217df1c5.jpg" width="30px"><span>尼克</span> 👍（0） 💬（2）<div>请问老师，路由变化为什么会导致发送包乱序呢？这段时间生产有个问题，ospf刷新的时候会有很多的重传，但是我不理解为什么路由变化会导致乱序，我理解的seq 不应该是同一个包是一直不变的吗，谢谢</div>2021-01-28</li><br/>
</ul>