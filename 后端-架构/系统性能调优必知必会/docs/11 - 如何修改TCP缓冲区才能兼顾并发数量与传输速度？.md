你好，我是陶辉。

我们在[\[第8课\]](https://time.geekbang.org/column/article/236921) 中讲了如何从C10K进一步到C10M，不过，这也意味着TCP占用的内存翻了一千倍，服务器的内存资源会非常紧张。

如果你在Linux系统中用free命令查看内存占用情况，会发现一栏叫做buff/cache，它是系统内存，似乎与应用进程无关。但每当进程新建一个TCP连接，buff/cache中的内存都会上升4K左右。而且，当连接传输数据时，就远不止增加4K内存了。这样，几十万并发连接，就在进程内存外又增加了GB级别的系统内存消耗。

这是因为TCP连接是由内核维护的，内核为每个连接建立的内存缓冲区，既要为网络传输服务，也要充当进程与网络间的缓冲桥梁。如果连接的内存配置过小，就无法充分使用网络带宽，TCP传输速度就会很慢；如果连接的内存配置过大，那么服务器内存会很快用尽，新连接就无法建立成功。因此，只有深入理解Linux下TCP内存的用途，才能正确地配置内存大小。

这一讲，我们就来看看，Linux下的TCP缓冲区该如何修改，才能在高并发下维持TCP的高速传输。

## 滑动窗口是怎样影响传输速度的？

我们知道，TCP必须保证每一个报文都能够到达对方，它采用的机制就是：报文发出后，必须收到接收方返回的ACK确认报文（Acknowledge确认的意思）。如果在一段时间内（称为RTO，retransmission timeout）没有收到，这个报文还得重新发送，直到收到ACK为止。
<div><strong>精选留言（20）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/14/64/9b/d1ab239e.jpg" width="30px"><span>J.Smile</span> 👍（18） 💬（1）<div>总结：
----------缓冲区动态调节功能-----------
①发送缓冲区自动调整（自动开启）：
net.ipv4.tcp_wmem = 4096(动态范围下限)        16384(初始默认值)   4194304(动态范围上限)
一旦发送出的数据被确认，而且没有新的数据要发送，就可以把发送缓冲区的内存释放掉


②接收缓冲区自动调整（通过设置net.ipv4.tcp_moderate_rcvbuf = 1开启）：
net.ipv4.tcp_rmem = 4096(动态范围下限)          87380(初始默认值)    6291456(动态范围上限)
可以依据空闲系统内存的数量来调节接收窗口。如果系统的空闲内存很多，就可以把缓冲区增大一些，这样传给对方的接收窗口也会变大，因而对方的发送速度就会通过增加飞行报文来提升。反之，内存紧张时就会缩小缓冲区，这虽然会减慢速度，但可以保证更多的并发连接正常工作。


③接收缓冲区判断内存空闲的方式：
net.ipv4.tcp_mem = 88560        118080  177120
当 TCP 内存小于第 1 个值时，不需要进行自动调节；
在第 1 和第 2 个值之间时，内核开始调节接收缓冲区的大小；
大于第 3 个值时，内核不再为 TCP 分配新内存，此时新连接是无法建立的。

④带宽时延积的衡量方式：对网络时延多次取样计算平均值，再乘以带宽。</div>2020-07-16</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1b/95/dc/07195a63.jpg" width="30px"><span>锋</span> 👍（9） 💬（3）<div>老师好，我有一个疑问想请教老师，在使用tcp来传输大数据包时，比如2M。这样的数据包在业务中很频繁出现，这样的数据包我们需要在我们的业务代码层面来实现拆包后发送，还是将拆包的工作交给网络设备来处理？为什么？谢谢</div>2020-06-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/8a/92/73a571ea.jpg" width="30px"><span>代后建</span> 👍（6） 💬（2）<div>老师，你好，我项目上用了nginx做代理，但偶尔会出现请求响应特别忙慢的情况(20s左右)，目前系统暂未上线，不存在并发影响性能的问题。我也用命令看了请求已到达网卡，却不知道nginx为何不响应，日志问题看不到什么问题，请教下排查问题的思路，谢谢！</div>2020-06-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/b1/1f/c2793540.jpg" width="30px"><span>Thinking</span> 👍（4） 💬（1）<div>请问一条TCP连接的带宽时延积中的带宽大小内核如何计算出来的？</div>2020-09-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/b5/8e/d91f87a2.jpg" width="30px"><span>kimileonis</span> 👍（3） 💬（1）<div>老师，当 net.ipv4.tcp_rmem 的当前值超过 net.ipv4.tcp_mem 的第三个值，就不会接受发送端新的TCP请求，直到 net.ipv4.tcp_rmem 的当前值小于 net.ipv4.tcp_mem 的第三个值后，才会接收新的连接请求，请问这么理解对吗？</div>2020-10-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/3e/d2/624a3d59.jpg" width="30px"><span>张华中-Blackc</span> 👍（3） 💬（1）<div>比如，发送一个 100MB 的文件，如果 MSS 值为 1KB，那么需要发送约 10 万个报文。发送方大可以同时发送这 10 万个报文，再等待它们的 ACK 确认。这样，发送速度瞬间就达到 100MB&#47;10ms=10GB&#47;s。

这里发送方同时发送10万个报文是需要应用层做，还是说操作系统默认就是这么做的？</div>2020-07-31</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/22/52/0b/50bf0f05.jpg" width="30px"><span>橙子橙</span> 👍（2） 💬（2）<div>老师 目前请求1000qps, client每次发送2MB数据, 服务器返回20MB数据, 要求每个请求client端rtt 50ms内, 不知道有没有可能?
还有老师对dpdk是什么看法, 针对这个场景有没有可能使用dpdk优化?</div>2020-12-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/d8/ee/6e7c2264.jpg" width="30px"><span>Only now</span> 👍（2） 💬（1）<div>这里设置的带宽时延积是从哪里来的？
我有一私有网络PriNet， 其内部带宽1G bit&#47;s，但是出口带宽5M&#47;s，那么网络内的服务器调整参数是，带宽时延积计算，这个带宽和时延分别取哪一段？？？</div>2020-11-18</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/l4nngwyggBGqeMXC0micwO8bM1hSttgQXa1Y5frJSqWa8NibDhia5icwPcHM5wOpV3hfsf0UicDY0ypFqnQ3iarG0T1w/132" width="30px"><span>Trident</span> 👍（1） 💬（1）<div>带宽时延积如何衡量呢，网络时延不是固定的，是要多次取样计算平均网络时延？然后估算出这个时延积</div>2020-05-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/b5/8e/d91f87a2.jpg" width="30px"><span>kimileonis</span> 👍（0） 💬（1）<div>老师，当 net.ipv4.tcp_rmem 的当前值超过 net.ipv4.tcp_mem 的第三个值，就不会接受发送端新的TCP请求，直到 net.ipv4.tcp_rmem 的当前值小于 net.ipv4.tcp_mem 的第三个值后，才会接收新的连接请求，请问这么理解对吗？</div>2020-10-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/60/71/895ee6cf.jpg" width="30px"><span>分清云淡</span> 👍（25） 💬（7）<div>TCP性能和发送接收窗口、Buffer的关系, 定量分析和图形展示, 正好看看wireshark分析这类问题的魅力： https:&#47;&#47;plantegg.github.io&#47;2019&#47;09&#47;28&#47;%E5%B0%B1%E6%98%AF%E8%A6%81%E4%BD%A0%E6%87%82TCP--%E6%80%A7%E8%83%BD%E5%92%8C%E5%8F%91%E9%80%81%E6%8E%A5%E6%94%B6Buffer%E7%9A%84%E5%85%B3%E7%B3%BB&#47;</div>2020-05-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/39/fa/a7edbc72.jpg" width="30px"><span>安排</span> 👍（6） 💬（1）<div>tcp的缓冲区占用的buffer&#47;cache不算在进程的内存中吗？那如果系统开了swap，这些缓冲区是否会在内存紧张时被回收呢？</div>2020-05-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/02/43/1c2fb7b3.jpg" width="30px"><span>Bourne</span> 👍（2） 💬（1）<div>老师您好，我有两个疑问：
1、一个TCP连接在客户端和服务端是都会有两个内存缓冲区吗，一个接收缓冲区，一个发送缓冲区？还是说各只有一个缓冲区，接收和发送共用？
2、文章说的带宽时延积是用带宽乘以时延，这里的带宽是指客户端的还是服务端的？因为客户端和服务端的带宽不可能都一样，所以算出来的时延积是不同的。</div>2020-06-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/4a/15/106eaaa8.jpg" width="30px"><span>stackWarn</span> 👍（2） 💬（0）<div>相关的内存配置在nginx调优中使用过，这次终于从前到后理解了意义</div>2020-06-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/34/df/64e3d533.jpg" width="30px"><span>leslie</span> 👍（1） 💬（0）<div>建立和释放以及为了连接数而滑动合适设置值，这个只能通过不断的观察去调整适应主要时间段的业务；均衡的设计考虑确实不易。</div>2020-05-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/27/4b/f7/114e2b48.jpg" width="30px"><span>九月不再朦胧</span> 👍（0） 💬（0）<div>有三个问题想请教老师
接收缓冲区判断内存空闲的方式：
net.ipv4.tcp_mem = 88560        118080  177120
在第 1 和第 2 个值之间时，内核开始调节接收缓冲区的大小；
Q1：这里认为内存紧张还是充足呢？
Q2：是调大还是调小呢？
Q3：在第2个值和第3个值之间时又会怎样呢？
</div>2023-11-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/29/88/8a/9008b284.jpg" width="30px"><span>Henry</span> 👍（0） 💬（0）<div>老师，MTU值与文中说到的“由于发送缓冲区决定了发送窗口的上限”有关联吗？</div>2023-06-07</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/d4/d9/c3296187.jpg" width="30px"><span>airmy丶</span> 👍（0） 💬（0）<div>“提速的方式很简单，并行地批量发送报文，再批量确认报文即可“ 这种处理方式，如果加上滑动窗口。ACK返回的窗口大小是不是出入很大(ACK返回期间服务器又接受了其他的报文)？</div>2021-04-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/11/78/4f0cd172.jpg" width="30px"><span>妥协</span> 👍（0） 💬（0）<div>请教老师，net.ipv4.tcp_wmem，net.ipv4.tcp_rmem这两个设置是针对单个TCP连接的发送缓冲区和接收缓冲区吧？net.ipv4.tcp_mem是指所有TCP内存吧？</div>2020-07-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/64/9b/d1ab239e.jpg" width="30px"><span>J.Smile</span> 👍（0） 💬（0）<div>看了两遍，才总体有了感觉</div>2020-06-30</li><br/>
</ul>