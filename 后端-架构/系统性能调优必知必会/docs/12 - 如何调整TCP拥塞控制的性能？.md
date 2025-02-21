你好，我是陶辉。

上一讲我们谈到接收主机的处理能力不足时，是通过滑动窗口来减缓对方的发送速度。这一讲我们来看看，当网络处理能力不足时又该如何优化TCP的性能。

如果你阅读过TCP协议相关的书籍，一定看到过慢启动、拥塞控制等名词。这些概念似乎离应用开发者很远，然而，如果没有拥塞控制，整个网络将会锁死，所有消息都无法传输。

而且，如果你在开发分布式集群中的高并发服务，理解拥塞控制的工作原理，就可以在内核的TCP层，提升所有进程的网络性能。比如，你可能听过，2013年谷歌把初始拥塞窗口从3个MSS（最大报文长度）左右提升到10个MSS，将Web站点的网络性能提升了10%以上，而有些高速CDN站点，甚至把初始拥塞窗口提升到70个MSS。

特别是，近年来谷歌提出的BBR拥塞控制算法已经应用在高版本的Linux内核中，从它在YouTube上的应用可以看到，在高性能站点上网络时延有20%以上的降低，传输带宽也有提高。

Linux允许我们调整拥塞控制算法，但是，正确地设置参数，还需要深入理解拥塞控制对TCP连接的影响。这一讲我们将沿着网络如何影响发送速度这条线，看看如何调整Linux下的拥塞控制参数。

## 慢启动阶段如何调整初始拥塞窗口？
<div><strong>精选留言（14）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/13/11/78/4f0cd172.jpg" width="30px"><span>妥协</span> 👍（14） 💬（5）<div>为什么报文5之后的ack都是ack6呀</div>2020-05-25</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/64/9b/d1ab239e.jpg" width="30px"><span>J.Smile</span> 👍（9） 💬（3）<div>总结一：
1 接收主机的处理能力不足时，是通过滑动窗口来减缓对方的发送速度。
2 接收主机的处理能力很强时，也无法通过增加发送方的发送窗口来提升发送速度，因为网络的传输速度是有限的，它会直接丢弃超过其处理能力的报文。
发送方只有在重传RTO时间超时后才会发现报文被丢弃然后重传报文。 解决这个问题办法是拥塞控制。
3 TCP慢启动
  TCP连接传输中会穿越多层网络并不清楚网络传输能力，所以一开始TCP会调低发送窗口大小，避免发送超过网络传输负载大小的报文。这样以来TCP发送报文速度就
  会变慢，这就是慢启动。TCP调低发送窗口(swnd)的大小是通过”拥塞窗口“---congestion window(cwnd)实现的。
4 如果不考虑网络拥塞，发送窗口就等于对方的接收窗口，而考虑了网络拥塞后，发送窗口则应当是拥塞窗口(cwnd)与对方接收窗口(rwnd)的最小值.
swnd = min(cwnd, rwnd),即发送速度就综合考虑了接收方和网络的处理能力。
5 通常用 MSS 作为描述窗口大小的单位，其中 MSS 是 TCP 报文的最大长度。虽然窗口的计量单位是字节。
6 拥塞窗口增长原理：
假如：初始拥塞窗口只有 1 个 MSS，MSS为1KB，RTT时延为100ms。发送速度=1KB&#47;100ms=10KB&#47;s
6.1 当没有发生拥塞时，拥塞窗口必须快速扩大，才能提高互联网的传输速度.
6.2 启动阶段会以指数级扩大拥塞窗口,发送方每收到一个 ACK 确认报文，拥塞窗口就增加 1 倍 MSS,比如最初的初始拥塞窗口（也称为 initcwnd）是 1 个 MSS，经过 4 个 RTT 就会变成 16 个 MSS。
6.3 互联网中的很多资源体积并不大， 2010 年 Google 对 Web 对象大小的 CDF 累积分布统计，大多数对象在 10KB 左右。
==》当 MSS 是 1KB 时，则多数 HTTP 请求至少包含 10 个报文才能下载完一个文件。以指数级增加拥塞窗口，经过4个RTT之后，才能收到大于10个MSS。
6.4 2013 年 TCP 的初始拥塞窗口调整到了 10 个 MSS，这样下载一个10KB的文件，只需要一个RTT就可以传输10KB的请求。
如果你需要传输的对象体积更大，BDP 带宽时延积很大时，完全可以继续提高初始拥塞窗口的大小
6.5 根据网络状况和传输对象的大小，调整初始拥塞窗口的大小
    ①ss 命令查看当前拥塞窗口：
    	ss -nli|fgrep cwnd
    ②ip route change 命令修改初始拥塞窗口：

		# ip route | while read r; do
		           ip route change $r initcwnd 10;
		       done</div>2020-07-16</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/64/9b/d1ab239e.jpg" width="30px"><span>J.Smile</span> 👍（3） 💬（1）<div>总结2：
7 慢启动结束的三个场景
①慢启动阶段结束场景一（通过定时器明确探测到了丢包）：
发送数据后发送方在timeout时间内没有收到ack报文，说明报文丢失，网络拥塞。降低发送速度，即调小拥塞窗口大小，cubic可以将拥塞窗口降低为原先的0.8倍。同时记得设置慢启动阈值为发生网络拥塞之前的拥塞窗口的大小。
②慢启动阶段结束场景二（拥塞窗口的增长到达了慢启动阈值 ssthresh）：
慢启动阶段，拥塞窗口大小达到了慢启动阈值，很可能出现网络拥塞，为了避免拥塞，拥塞窗口增长速度应当更加保守的使用线性增长，而不是开始的指数增长。线性增长方式时每个RTT增加一个MSS，指数增长方式时每个ACK增加一倍MSS。
③慢启动阶段结束场景三（接收到重复的 ACK 报文，可能存在丢包）：
	如果发送方连续发送多个报文，在慢启动阶段第6个报文丢失。那么接收方就会接下来直接收到发送的第七个报文。接收方收到失序的第7个报文会触发快速重传算法，
立刻返回ACK6。以后收到的第8个、第9个报文都会返回ACK6，接收方直接反复的传递ACK6，这样发送方就能明白，报文6丢了，他可以提前重发报文6. 这叫做快速重传！
而不是等待发送方在RTO时间内没收到报文6的ACK响应才重传，那样就太慢了！
在触发快速重传之后，发送方会把慢启动阈值和拥塞窗口都降到之前的一半，进入”快速恢复阶段“。
此时发送方的拥塞窗口会由于接收到重复的ACK6，而增加相应个数的MSS。
发送方明白了报文6丢失之后，立即发送报文6给接收方，接收方这次收到了并给出了正常的响应。
后续不会再重复ACK6的响应了。然后才进入”拥塞避免阶段“（也就是从指数变线程增长）。


8 拥塞控制算法
慢启动、拥塞避免、快速重传、快速恢复，共同构成了拥塞控制算法
内核支持的拥塞控制算法列表：
net.ipv4.tcp_available_congestion_control = cubic reno
内核选择的拥塞控制算法：
net.ipv4.tcp_congestion_control = cubic
Linux 4.9 版本之后都支持 BBR 算法，是基于测量的拥塞控制算法，开启 BBR 算法仍然使用 tcp_congestion_control 配置：
net.ipv4.tcp_congestion_control=bbr</div>2020-07-16</li><br/><li><img src="" width="30px"><span>李新龙</span> 👍（1） 💬（1）<div>收到重复的ACK后，报文是不是暂停发送了</div>2020-09-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/64/9b/d1ab239e.jpg" width="30px"><span>J.Smile</span> 👍（1） 💬（1）<div>”慢启动阶段会以指数级扩大拥塞窗口（扩大规则是这样的：发送方每收到一个 ACK 确认报文，拥塞窗口就增加 1 个 MSS）“
---------------------------------
老师，这一句是不是有问题，发送方收掉一个ack，是增加1倍的吧MSS，这样才跟后面一致。4个RTT就是4个ACK，那也就增加了4个MSS，就不是16了。。。
”比如最初的初始拥塞窗口（也称为 initcwnd）是 1 个 MSS，经过 4 个 RTT 就会变成 16 个 MSS“</div>2020-07-16</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/82/3d/356fc3d6.jpg" width="30px"><span>忆水寒</span> 👍（19） 💬（3）<div>1、关于课后思考题，快速恢复阶段的拥塞窗口，在报文变得有序后反而会缩小？
我想原因可能是 TCP觉得此时网络轻度拥塞，然后拥塞阈值ssthresh降低为cwnd 的一半，并设置cwnd为ssthresh，然后拥塞窗口再线性增长。

2、本文的一些思考与总结
首先由于慢启动拥塞窗口肯定不能无止境的指数级增长下去，否则拥塞控制就会失控。
这个时候，ssthresh 就是一道刹车，让拥塞窗口别涨那么快。
  当 cwnd&lt;ssthresh 时，拥塞窗口按指数级增长（慢启动）
  当 cwnd&gt;ssthresh 时，拥塞窗口按线性增长（拥塞避免）

  拥塞控制的几种算法：
慢启动：拥塞窗口一开始是一个很小的值，然后每 RTT 时间翻倍
拥塞避免：当拥塞窗口达到拥塞阈值（ssthresh）时，拥塞窗口从指数增长变为线性增长。
快速重传：发送端接收到 3 个重复 ACK 时立即进行重传。
快速恢复：当收到三次重复 ACK 时，进入快速恢复阶段，此时拥塞阈值降为之前的一半，然后进入线性增长阶段。</div>2020-05-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/39/fa/a7edbc72.jpg" width="30px"><span>安排</span> 👍（5） 💬（0）<div>毕竟还是发生了丢包或者延迟，所以快速恢复后重新进去拥塞避免。</div>2020-05-25</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/60/71/895ee6cf.jpg" width="30px"><span>分清云淡</span> 👍（2） 💬（1）<div>bbr比较适合高rt场景，对机房内网性能反而更差，慎用</div>2020-05-25</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/17/47/12/2c47bf36.jpg" width="30px"><span>Geek_2b3614</span> 👍（1） 💬（0）<div>扩大规则是这样的：发送方每收到一个 ACK 确认报文，拥塞窗口就增加 1 个 MSS---&gt; 貌似是增加一倍个mss？</div>2020-06-05</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/7f/91/962eba1a.jpg" width="30px"><span>唐朝首都</span> 👍（1） 💬（0）<div>我理解：快速重传是窗口虽然是8，但是在网络中传输的数据包数量是&lt;=4的，因为另外几个被“8，9，10，11”占了，所以进入拥塞避免阶段之后，继续保持8实际上是可能造成拥塞，不如恢复的已经被证明能够支撑的cwnd，然后再线性增长。</div>2020-05-25</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/64/05/6989dce6.jpg" width="30px"><span>我来也</span> 👍（1） 💬（0）<div>第一次见BBR还是在搭建梯子的过程中.
那时ubuntu默认内核还不支持,需要手动开启.</div>2020-05-25</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/2c/a9/cc/1183d71f.jpg" width="30px"><span>无</span> 👍（0） 💬（0）<div>您好陶辉老师，请问初始ssthresh如何设置哈？查了网上好多资料都找不到</div>2023-08-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/d4/44/ec084136.jpg" width="30px"><span>LoveDlei</span> 👍（0） 💬（0）<div>如果初始拥塞窗口只有 1 个 MSS，当 MSS 是 1KB，而 RTT 时延是 100ms 时，发送速度只有 10KB&#47;s。所以，当没有发生拥塞时，拥塞窗口必须快速扩大，才能提高互联网的传输速度。因此，慢启动阶段会以指数级扩大拥塞窗口（扩大规则是这样的：发送方每收到一个 ACK 确认报文，拥塞窗口就增加 1 个 MSS），比如最初的初始拥塞窗口（也称为 initcwnd）是 1 个 MSS，经过 4 个 RTT 就会变成 16 个 MSS。

这段没有整明白？</div>2021-10-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/57/4f/6fb51ff1.jpg" width="30px"><span>奕</span> 👍（0） 💬（0）<div>linux 可以控制 TCP 拥塞窗口 Cwnd 的大小 和 拥塞控制算法 net.ipv4.tcp_congestion_control 这个有两个值： bbr 基于带宽时延的   cubic 基于丢包的</div>2020-07-17</li><br/>
</ul>