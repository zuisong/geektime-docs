你好，我是胜辉。

在[第1讲](https://time.geekbang.org/column/article/477510)里，我给你介绍过TCP segment（TCP段）作为“部分”，是从“整体”里面切分出来的。这种切分机制在网络设计里面很常见，但同时也容易引起问题。更麻烦的是，这些概念因为看起来都很像，特别容易引起混淆。比如，你可能也听说过下面这些概念：

- TCP分段（segmentation）
- IP分片（fragmentation）
- MTU（最大传输单元）
- MSS（最大分段大小）
- TSO（TCP分段卸载）
- ……

所以这节课，我就通过一个案例，来帮助你彻底搞清楚这些概念的联系和区别，这样你以后遇到跟MTU、MSS、分片、分段等相关的问题的时候，就不会再茫然失措，也不会再张冠李戴了，而是能清晰地知道问题在哪里，并能针对性地搞定它。

## 案例：重传失败导致应用压测报错

我先来给你介绍下案例背景。

在公有云服务的时候，一个客户对我们公有云的软件负载均衡（LB）进行压力测试，结果遇到了大量报错。要知道，这是一个比较大的客户，这样的压测失败，意味着可能这个大客户要流失，所以我们打起十二分的精神，投入了排查工作。

首先，我们看一下这个客户的压测环境拓扑图：

![](https://static001.geekbang.org/resource/image/9a/e0/9ae5998eb5922295ebbdab9147eff0e0.jpg?wh=1821x692)

这里的香港和北京，都是指客户在我们平台上租赁的云计算资源。从香港的客户端机器，发起对北京LB上的VIP的压力测试，也就是短时间内有成千上万的请求会发送过来，北京LB就分发这些请求到后端的那些同时在北京的服务器上。照理说，我们的云LB的性能十分出色，承受数十万的连接没有问题。不夸张地说，就算客户端垮了，LB都能正常工作。
<div><strong>精选留言（28）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/12/21/b8/aca814dd.jpg" width="30px"><span>江山如画</span> 👍（21） 💬（4）<div>问题1:
从可用性角度分析，通过 iptables 修改 mss 只对 tcp 报文生效，对 udp 报文不生效。由于udp 报文传输时没有协商 mss 的过程，如果发现 udp 负载长度比 mtu 大，会交给网络层分片处理，分片传输途中只要有一个分片丢了，由于 udp 没有反馈给发送端具体是哪个分片丢了的能力，只能重新传整个包，传输效率会变低。

从运维角度分析，由于修改中间环节某个服务器的 iptables ，对于其它侧是透明的，可能会对定位问题带来困扰。

问题2:
遇到过 mtu 引发的问题。之前手动创建了虚拟网卡，和物理网卡之间做了流量的桥接，发现有些报文在二者之间转发时会被丢掉，分析发现虚拟网卡的 mtu 设置过大，并且报文 DF 位设置为了 1，通过 ifconfig 命令把虚拟网卡的 mtu 改小，报文就可以正常转发了。</div>2022-02-07</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/vM2NmFZQYmb4kkk8Cba1fGP4bhK9diaeXb2LXFWXJWfOPuibK3aib24qujweqciaxt43btqicSz9gDDlJkUQ12RDfJQ/132" width="30px"><span>Geek_955506</span> 👍（11） 💬（1）<div>Flow Graph 展示页的左下角有一个复选框 &quot;limt to display filter&quot;，勾上之后就只展示过滤的内容了，不需要再单独保存展示</div>2022-06-05</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/50/33/9dcd30c4.jpg" width="30px"><span>斯蒂芬.赵</span> 👍（5） 💬（1）<div>不明白，如果传入的tcp载荷超过了mtu值，不应该根据mss值自动的分段么</div>2023-01-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/28/73/9a/5197bbbd.jpg" width="30px"><span>张靳</span> 👍（5） 💬（1）<div>开始对[为什么有重复确认（DupAck）]这个小节标志位Dup ACK的两个报文是载荷为688和57的两个报文的确认报文不是很理解，在杨老师指导下豁然开朗，做一下我的理解记录：
最开始我对wirshark的符号有误解，我选中Dup ACK报文发现是7号报文（三次握手的ack报文）的重复确认（有两个对勾），我就以为是7号报文的确认报文，这个理解本身有问题，因为ack本身没有ack了，不然就没完没了了。查阅了Dup ACK的定义，当发现丢包或者乱序的时候接收方会收到一些Seq序列号比期望值大的包，每收到这种包就会ack一次期望的Seq值。
所以我们知道可能有丢包才会有重复确认，且确认得是对端发过来得报文。那么结合整个tcp流来看，发生重传得报文是没收到的，然后确认了688和57载荷得报文。</div>2022-02-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/47/00/3202bdf0.jpg" width="30px"><span>piboye</span> 👍（3） 💬（1）<div>包的收发路径不一致的时候,  MSS 协商是不是就失效了?  运营商网络, 如果出现链路调整, 之前协商的MSS 是不是也会可能失效了?  特别是长链接场景, 这种情况, 是不是要预先设置一个比较保守的值?</div>2022-08-03</li><br/><li><img src="" width="30px"><span>Geek3340</span> 👍（3） 💬（5）<div>老师，有一点不是很理解：
由于 Tunnel 1 比 Tunnel 2 的封装更大一些，所以服务端选择了不同的传输尺寸，一个是 1388，一个是 1348。
为啥会有这种选择呢，按照理解，MSS会自动从MTU-40来计算，不太理解为啥中间的IPIP隧道会影响到MSS的分段


经过LB的，1388 + 40(TCPIP) + IP(20) + IP(20) = 1468
不经过LB的，1348 + 40(TCPIP) + IP(20) = 1408 

在本次案例中，以下命令能解决问题，应该如何理解呢？我理解1400应该是调整小了MSS到1400，但是之前的1388也没有超限呀，不理解：
iptables -A FORWARD -p tcp --tcp-flags SYN SYN -j TCPMSS --set-mss 1400


</div>2022-02-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/6b/20/004af747.jpg" width="30px"><span>志强</span> 👍（2） 💬（3）<div>老师有几个疑问请教：
问题1.&quot;我们选中 575 号报文&quot;下边的图中Dup ACK报文是31号，&quot;为什么是两个重复确认报文呢？我们把视线从 2 个 DupAck 报文往上挪&quot;下边的图中dup ack 就变成了3号，是人为修改的还是怎么回事？
问题2.有两次31号报文的dup ack，是因为收到了额外两次17号报文吧，有人肯能会问那为啥看不到17号报文的重传呢，这个我也不太清楚，可能是处理重传的位置在捕获抓包之后吧，要是在客户端抓包就能看到17号报文的重传，请老师指正
问题3.无论是握手的ack 还是数据的ack，这个ack是谁给回的，知道是内核给回复，具体哪一层的什么函数处理过后给回复的ack；kcp老师了解吗，是应用层在再给回复还是也是内核给的恢复
谢谢老师，期待您的详细解答</div>2022-02-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/25/66/4835d92e.jpg" width="30px"><span>潘政宇</span> 👍（2） 💬（2）<div>杨老师，中间设备不是只是转发作用吗，协商mss也参与吗</div>2022-02-07</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/18/b7/24/17f6c240.jpg" width="30px"><span>janey</span> 👍（1） 💬（1）<div>MTU我看有的文章说是二层的，不知道到底算那层的？</div>2023-02-07</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/17/a8/60/7abaaa62.jpg" width="30px"><span>夜、</span> 👍（1） 💬（1）<div>好像没有直接说明第一个包为啥没发送成功？  就算超过MTU了不是还会IP分片么</div>2022-02-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/27/ce/58/71ed845f.jpg" width="30px"><span>Dexter</span> 👍（1） 💬（1）<div>TCP分段的计算公司，那个IP header length和TCP header length是如何的得知的？难道都是按照默认的IP HDR =20, TCP HDR =20吗？这不是很可靠吧。 还有TCP segmentation probe功能开启是不是能够解决案例中的问题？
[root@master03 ipv4]# cat tcp_mtu_probing
0
[root@master03 ipv4]#


问题2：如果启用了TSO或者GRO，为什么经常在抓包中看到TCP segment还是1460?

问题3： LRO是什么？老师能帮忙解答下吗？</div>2022-02-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/27/ce/58/71ed845f.jpg" width="30px"><span>Dexter</span> 👍（1） 💬（1）<div>iptables -A FORWARD -p tcp --tcp-flags SYN SYN -j TCPMSS --set-mss 1400   --- 文中说是在nat表，不过这个command没有指定nat表，而且nat表中应该没有forward chain</div>2022-02-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/f1/d7/a52e390d.jpg" width="30px"><span>Pantheon</span> 👍（1） 💬（1）<div>每一个字都值得分析,老师的课写的很棒,实战派</div>2022-02-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1d/97/ad/cdb3c420.jpg" width="30px"><span>kakashi</span> 👍（0） 💬（2）<div>关于怎么看包是在服务器抓的还是在客户端抓的，还有一个方法，就是看端口号，服务器端都是固定的公认端口，客户端都是随机的高端口。

另外，请教下老师，TCP MSS有没有类似PMTUD的路径发现机制？</div>2022-05-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/16/2a/68913d36.jpg" width="30px"><span>杨震</span> 👍（0） 💬（1）<div>每节课都要看几遍消化消化，老师写的非常好，图文清晰。期待后续老师更多栏目</div>2022-03-03</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1b/e4/79/0f0114ba.jpg" width="30px"><span>taochao_zs</span> 👍（0） 💬（1）<div>老师，你的wireshark是什么版本的，为啥3.4.6版本没法再显示列这里添加ttl的字段。</div>2022-02-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/8f/cf/890f82d6.jpg" width="30px"><span>那时刻</span> 👍（0） 💬（1）<div>老师的思考题：在 LB 或者网关上修改 MSS，虽然可以减小 MSS。 我想的问题是减少mss，会加大传输层segment机会，从而丢包可能性也会增加</div>2022-02-07</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/eb/09/ba5f0135.jpg" width="30px"><span>Chao</span> 👍（0） 💬（2）<div>就在老师这篇文章前遇到同样问题，client 和 rs 之间有Lvs。 Lvs与RS走IPIP。 运维将LVS和RS的MTU设置为同样大小，client与rs 握手协商后的mss。 client发送大量重传。 由于Lvs封装后的tcp包大于MTU，TCP默认不作IP封片，所以直接被丢弃了。 但这种情况只发生个别客户上。 其他多数用户反而没有问题。 唯一能解释过去的是多数用户能收到PMTUD。进行二次分片。 但PMTUD不应该更容易被中间设备丢弃吗？ 目前做法增大lvs 的mtu</div>2022-02-07</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1b/96/47/93838ff7.jpg" width="30px"><span>青鸟飞鱼</span> 👍（3） 💬（1）<div>TCP，三次握手时，会相互沟通MSS，MSS是怎么来的呢？经过网络各种设备后，不能保证MSS比MTU小，是不是随时得关注MTU、MSS吗</div>2022-04-03</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/DYAIOgq83ep8bWkhQUsZRYaoWhWpTKsoSSx7avG2GlvGXYGrfiaiaur9LkTFWeHnuTvyqQN1W1ibJ5pnamB2a92lQ/132" width="30px"><span>Geek_cf2028</span> 👍（1） 💬（0）<div>这个案例确实经典，我也遇到过，中间过了ipsec设备加了一层封装导致报文变长，通过修改mss解决了，通过这个案例才明白icmp不是只有ping才有。</div>2022-07-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/38/34/e2/21859878.jpg" width="30px"><span>yell</span> 👍（0） 💬（0）<div>不仅是老师的课很好，留言也必须看一遍</div>2024-01-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/37/9c/28/9a7dd23f.jpg" width="30px"><span>一宁兮</span> 👍（0） 💬（0）<div>老师i好，请问针对连续发送的三个数据包的后两个数据的确认ack数据包在哪里呀</div>2023-08-15</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/36/8b/7a/ec36ff82.jpg" width="30px"><span>原则</span> 👍（0） 💬（0）<div>还有 Packet size limited during capture 是什么意思呢</div>2023-06-02</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/36/8b/7a/ec36ff82.jpg" width="30px"><span>原则</span> 👍（0） 💬（0）<div>为什么第33号报文的序列号是1，第38号报文的序列号也是1</div>2023-06-02</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/db/17/aee5d35a.jpg" width="30px"><span>远天</span> 👍（0） 💬（0）<div>老师，您好，最近遇到一个问题，一个http请求的请求参数比较大2M左右，服务端接收到http请求后，发现请求体丢失了，在服务端抓包发现，tcp分段传输到一半的时候，服务端就已经返回http请求的响应了，然后tcp数据还是在继续传输，过一会儿后，客户端发起Fin,这种现象是为什么呢？</div>2023-04-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/69/21/7db9faf1.jpg" width="30px"><span>简迷离</span> 👍（0） 💬（0）<div>经过 LB 的时候，报文需要做 2 次封装（Tunnel 1 和 Tunnel 2），而绕过 LB 就只要做 1 次封装
（只有 Tunnel 1）。另外，由于 Tunnel 1 比 Tunnel 2 的封装更大一些，所以服务端选择了不同的传
输尺寸，一个是 1388，一个是 1348。

杨老师，请教个问题，“由于 Tunnel 1 比 Tunnel 2 的封装更大一些，所以服务端选择了不同的传
输尺寸，一个是 1388，一个是 1348。”这句话不理解，还望老师解答</div>2022-04-05</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/c4/03/f753fda7.jpg" width="30px"><span>JianXu</span> 👍（0） 💬（0）<div>杨老师，我看了前面Geek3340 这位同学的问题，我也有类似的问题：

1. 广州到LB 之间应该会商量一个MTU1然后LB 和后端Server 之间也会商量一个MTU2,  造成这个问题的原因是广州到LB 之间的包设置了DF 标记导致LB 在转发到后端server 时候直接丢弃超出MTU2的包吗？

2. 现在的情况是我们有LB 的权限，所以可以在LB 上用iptables来“暗箱操作”, 但是如果客户端到服务端之间经过的网络设备因为MTU 导致问题，而我们又没有权限那是不是就只剩下在客户端直接降低MTU 了呢？如果答案是Yes , 这又导致一个问题，在现在应用和基础架构分离的趋势下，应用开发人员越来越不关心基础架构，那基础架构维护OS 的人就必须保证提供的vm 或者docker image 提供合适的MTU 配置？写到这里还是觉得不设置DF 让网络协议自己商量MTU 似乎更好一些？但是这样会碰到你说的防火墙不认拆分后的后续包的问题，我这样理解对吗？</div>2022-03-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/8f/cf/890f82d6.jpg" width="30px"><span>那时刻</span> 👍（0） 💬（1）<div>请问老师，暗箱操作的图例里，中间节点给客户端回复syn+ack的mss是1460，为什么客户端认为mss是1400呢？</div>2022-02-07</li><br/>
</ul>