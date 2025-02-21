你好，我是胜辉。

在上一讲里，我们排查了一个跟操作系统紧密相关的性能问题。我们结合top和strace这两个工具，抓住了关键点，从而解决了问题。性能问题，确实也是我们日常技术工作中的一个重要话题。在出现性能问题以后，我们要有能力搞定它；而在出现性能问题之前，最好能提前预见到它。而要“预见”性能瓶颈，最好的方法就是做**压力测试**。

但是，我们在做压力测试的过程中也时常出现预料不到的情况。比如在离预期的瓶颈值还很远的时候，系统就出现了各种意外，影响到压力测试的继续进行。

那么在这节课里，我们会回顾几个典型的压力测试场景中的网络问题，一起来学习其中的关键要点。同时，我们还会学习一系列跟网络性能相关的压测工具和检测工具，这样以后你遇到类似的问题时，就有所准备了。

## 压测要做什么？

压力测试的诉求实际上多种多样，不过大体上可以分为这几种。

**应用的承受能力**：这主要在第七层应用层，比如发起了压测，把服务端的CPU打到95%甚至100%，观察这时候的请求的TPS、请求耗时、并发量等等。而这些对于不同的业务场景，又会有不同的侧重点。比如：

- 对于时间敏感型业务来说，请求耗时（Latency）这个指标就是关键了。
- 对于经常做秒杀的电商来说，并发处理量TPS（Transaction Per Second）就是一个核心关注点了。
<div><strong>精选留言（11）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/11/8f/cf/890f82d6.jpg" width="30px"><span>那时刻</span> 👍（6） 💬（3）<div>请问老师，文中提到：对于网络处理来说，主要的开销在包的头部的处理上，而载荷本身的处理是很快的。指的是内核需要处理头部信息所消耗的开销么？而载荷是由应用程序处理，不计入网络处理？</div>2022-03-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/c4/03/f753fda7.jpg" width="30px"><span>JianXu</span> 👍（5） 💬（1）<div>当年蒋公领导Cms 项目，压测必须见到cpu , mem 或者IO 之一见顶，不然不算过。客户端压测必须有多机并发避免受限单机性能。需要做大小包测试，对应到cms 就是小的文档和大的文档压测。目标机也需要多机集群，因为牵涉到服务端同步。</div>2022-03-12</li><br/><li><img src="" width="30px"><span>holiday</span> 👍（2） 💬（6）<div>案例一的5万pck&#47;s达到这台云主机的上限，这个老师能否详细解释一下？</div>2022-04-02</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/7f/d3/b5896293.jpg" width="30px"><span>Realm</span> 👍（2） 💬（2）<div>
1 iperf 和 netperf 都是最常用的网络性能测试工具；

2 也可以通过修改内核参数，优化tw的问题
#启用 timewait 快速回收。
net.ipv4.tcp_tw_recycle = 1

#开启重用。允许将 TIME-WAIT sockets 重新用于新的 TCP 连接。
net.ipv4.tcp_tw_reuse = 1</div>2022-03-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/31/d8/18a2de6d.jpg" width="30px"><span>朱林浩</span> 👍（0） 💬（1）<div>net.ipv4.tcp_max_tw_buckets参数默认值不应该是16384吧！超过这个值被清理，那怎么来的28231个TIME_WAIT呢？</div>2024-09-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/2a/14/76/304fb890.jpg" width="30px"><span>陈海松</span> 👍（0） 💬（1）<div>请问老师，最近我们这边遇到一个问题，2个系统建立tCP连接总是在1500个左右，超不过1600.遇到业务高峰期，就会出现连运维中心维护终端SSH都连接不上或者需要多次尝试才能登录系统。系统允许打开文件数、文件句柄数调整了，没有效果。系统负荷、内存占用率都不高，网络带宽也足够，麻烦老师协助帮忙分析分项，盼复，谢谢！</div>2022-05-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/4e/bd/7fc7c14f.jpg" width="30px"><span>汤玉民</span> 👍（0） 💬（1）<div>包量的上限是算的还是测试得到的</div>2022-03-30</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/8f/cf/890f82d6.jpg" width="30px"><span>那时刻</span> 👍（0） 💬（1）<div>1.测试带宽，可以使用iPerf工具 
2.Linux的TIME_WAIT貌似是hard code为60秒。而阿里云的机器可以通过 sysctl -w &quot;net.ipv4.tcp_tw_timeout=[$TIME_VALUE] 来修改TIME_WAIT。
window下可以通过修改注册表 HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Services\TCPIP\Parameters] &quot;TcpTimedWaitDelay&quot;=dword:0000001E </div>2022-03-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/eb/09/ba5f0135.jpg" width="30px"><span>Chao</span> 👍（0） 💬（2）<div>Idle timeout  导致连接被rest。 遇到一个相同案例， 浏览器做法是遇到这种情况 进行了重试。 虽然有http headers 里可以申明 keepalive 超时时间 。 但好像没有客户端实现其读取并主动断开。</div>2022-03-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/b3/c5/7fc124e2.jpg" width="30px"><span>Liam</span> 👍（0） 💬（3）<div>带宽测试：iperf, pktgen
修改timewait的时间： 修改TCP_TIME_WAIT, 重新编译内核。默认2MSL是60s
</div>2022-03-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/00/6d/335fc40d.jpg" width="30px"><span>我想静静</span> 👍（0） 💬（0）<div>案列3中，我们的 LB 上的 VIP 有一个 idle timeout 的设置，如果客户端在一定时限内不发任何报文，那么这条连接将被回收。这个时限是 180 秒，而且回收时不向客户端发送 FIN 或者 RST 报文。

请问LB为什么不向客户端发送FIN呢？</div>2023-10-15</li><br/>
</ul>