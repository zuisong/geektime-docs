你好，我是邵亚方。这节课我来跟大家分享TCP拥塞控制与业务性能抖动之间的关系。

TCP拥塞控制是TCP协议的核心，而且是一个非常复杂的过程。如果你不了解TCP拥塞控制的话，那么就相当于不理解TCP协议。这节课的目的是通过一些案例，介绍在TCP拥塞控制中我们要避免踩的一些坑，以及针对TCP性能调优时需要注意的一些点。

因为在TCP传输过程中引起问题的案例有很多，所以我不会把这些案例拿过来具体去一步步分析，而是希望能够对这些案例做一层抽象，把这些案例和具体的知识点结合起来，这样会更有系统性。并且，在你明白了这些知识点后，案例的分析过程就相对简单了。

我们在前两节课（[第11讲](https://time.geekbang.org/column/article/284912)和[第12讲](https://time.geekbang.org/column/article/285816)）中讲述了单机维度可能需要注意的问题点。但是，网络传输是一个更加复杂的过程，这中间涉及的问题会更多，而且更加不好分析。相信很多人都有过这样的经历：

- 等电梯时和别人聊着微信，进入电梯后微信消息就发不出去了；
- 和室友共享同一个网络，当玩网络游戏玩得正开心时，游戏忽然卡得很厉害，原来是室友在下载电影；
- 使用ftp上传一个文件到服务器上，没想到要上传很久；
- ……

在这些问题中，TCP的拥塞控制就在发挥着作用。

## TCP拥塞控制是如何对业务网络性能产生影响的 ？
<div><strong>精选留言（14）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/1e/3b/d7/9d942870.jpg" width="30px"><span>邵亚方</span> 👍（24） 💬（0）<div>课后作业答案：
- 通过 ssh 登录到服务器上，然后把网络关掉，过几秒后再打开，请问这个 ssh 连接还正常吗？为什么？
ssh使用的TCP协议，也就是它是有连接的，这个连接对内核而言就是tcp_sock这个结构体，这个结构体会记录该TCP连接的状态，包括四元组(src_ip:src_port - dst_ip:dst_port)，该连接的路由信息也被保存着。关闭网络后，该TCP连接的这些信息都还在，如果两边没有数据交互的话，这些信息就不会被更新，也就你一直存在着，当你再次打开网络，该连接还可以正常使用；假如关闭网络后，该TCP连接有数据交互，此时就会检查到异常，同样的也会去更新TCP连接状态信息，就有可能会断开这个连接。除此之外，TCP还有keepalive机制，如果该连接长时间没有数据，keepalive机制也会把该连接给关闭掉。
</div>2020-10-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/17/96/a10524f5.jpg" width="30px"><span>蓬蒿</span> 👍（8） 💬（1）<div>我们金融交易平台的生产环境出现过一个案例，每天早上9点开盘会有用户集中登录的情况，其中登录链路中有两个服务，部署在两台服务器上，事故当天就出现了很多用户无法登陆的情况，开发人员排查日志发现这两个服务之间的通信有非常大的延时，A服务发的消息，B服务过了很久才收到，时间5分钟到20分钟不等，我们运维小伙伴监控服务器的负载非常低，CPU，内存，io都很正常，甚至我们还有专门的程序每秒探测内网机器的存活，ping包每秒一次，延时也都在毫秒级别。所以当时判断可能是两个服务之间的tcp链接出了问题，我比较怀疑是接收方窗口变为0了，但苦于没有抓包无法验证猜想，并且此类事件再也没有出现，但是心里一直存在疑惑，所以想问问老师，在您看来这种情况比较可能原因有哪些？</div>2020-11-07</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/64/05/6989dce6.jpg" width="30px"><span>我来也</span> 👍（8） 💬（2）<div>课后思考题：
这个应该是不确定的。

以前也测试过，只要在网络断开期间不主动发送数据，就会晚一点探测到连接已断开。
如果不主动发数据，可能网络恢复时，连接就自动恢复了。</div>2020-09-18</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/dwehJHP4ycAfDb9MoudXb4QSt7YgmISqwwsa928XZ6aTWqwWh0kx0iatjocSibLa7iajXmbGlJ5svegY3P6LfKJ0w/132" width="30px"><span>solar</span> 👍（6） 💬（3）<div>cwnd和rwnd使用的单位是什么呢？</div>2020-10-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/f9/e6/47742988.jpg" width="30px"><span>webmin</span> 👍（5） 💬（2）<div>要分情况：
1. 如果关闭网络是发生在Client端或Server端的机器上，那么网络恢复后连接不会正常；
2. 如果关闭网络是发生在Client端与Server端之间链路中的某个路由节点上；
    2.1 Client端到Server端之间有多条路可用，只要不是和CS直连这个设备有问题，那么设备可以选择其它路走，这时连接还是正常的；
    2.2 Client端与Server端之间链路有NAT，且网络关闭发生与NAT端相关的设备上，那么连接就不正常； 
    2.3 Client端与Server端之间只有一条路，只要不是和CS直连这个设备有问题，那么如果网络在发生tcp_keepalive之前恢复，那么连接还是正常的； 
 3. 以上讨论的都是在TCP&#47;IP协议情况下，网上查了一下SSH有居于UDP的方案（http:&#47;&#47;publications.lib.chalmers.se&#47;records&#47;fulltext&#47;123799.pdf），如果走UDP的话这个要看SSH应用层的保活或SESSION有效期是否超过网络关闭时间，大小则可以连接，小于则关闭。</div>2020-09-18</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/a8PMLmCTCBa40j7JIy3d8LsdbW5hne7lkk9KOGQuiaeVk4cn06KWwlP3ic69BsQLpNFtRTjRdUM2ySDBAv1MOFfA/132" width="30px"><span>Ilovek8s</span> 👍（4） 💬（1）<div>keepalive心跳的时间里如果不发送ssh命令操作，断开网络之后再重新打开，由于TCP有重试机制，是可以恢复的，但如果keepalive开始检查了，服务端发现客户端是死的之后就会关闭连接</div>2021-03-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/5a/56/115c6433.jpg" width="30px"><span>jssfy</span> 👍（3） 💬（1）<div>引用：对此，我们使用 tcpdump 在 server 上抓包后发现，Client 响应的 ack 里经常出现 win 为 0 的情况，也就是 Client 的接收窗口为 0。于是我们就去 Client 上排查，最终发现是 Client 代码存在 bug，从而导致无法及时读取收到的数据包。

请问这里的前一句的接收窗口为0和后一句的代码bug是有什么逻辑关系吗？这里没太看懂</div>2020-09-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/ed/91/1d332031.jpg" width="30px"><span>我能走多远</span> 👍（2） 💬（2）<div>感谢老师分享，学习了拥塞控制的原理，慢启动，拥塞避免，快速重传和快速恢复。cwnd和rwnd使用的单位是什么呢？ TCP segment个数。每个segment的长度就是mss的大小吗？</div>2020-11-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/00/8e/ebe3c8ea.jpg" width="30px"><span>董泽润</span> 👍（2） 💬（1）<div>连接是否正常，要看是否开启了 tcp_keepalive, 并且探测持续失败，连接才失效</div>2020-09-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/48/5e/36d96d40.jpg" width="30px"><span>redseed</span> 👍（5） 💬（1）<div>老师你好，去年公司接入了跨境专线，使用默认对 CUBIC 算法时 TCP 的流量极不稳定，根据网上的优化建议增大了 TCP 的 sendbuf 适应这类高延迟网络，但是 TCP 的传输带宽反而下降了，想请教一下可能的原因出现在哪里？（PS. 后面我们使用了 BBR 算法并增大 sendbuf，这个对长肥管道有奇效...）</div>2020-10-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/b5/1d/f2f66e8d.jpg" width="30px"><span>团团-BB</span> 👍（1） 💬（0）<div>老师我遇到一个有一系列pod运行的应用，其中有1-2个pod的响应时间抖动比其他pod严重很多，流量相对是均衡的，抖动的pod我们看有出现丢包的情况。
出现这种情况的pod所在的宿主机节点网卡的流量比较高，节点网卡eth0有drop包，和应用的延时徒增时间大致吻合，查看网卡rx有drop包的情况。因为是使用的公有云的基础设施，这种情况下，怎么能排除是否是基础设施网络存在的问题呢</div>2022-04-02</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/17/37/a0/032d0828.jpg" width="30px"><span>上杉夏香</span> 👍（0） 💬（0）<div>老师，有个问题。「我们再回到上面这张图，因为接收端没有接收到第 2 个 segment，因此接收端每次收到一个新的 segment 后都会去 ack 第 2 个 segment，即 ack 17。紧接着，发送端就会接收到三个相同的 ack（ack 17）。连续出现了 3 个响应的 ack 后，发送端会据此判断数据包出现了丢失，于是就进入了下一个阶段：快速重传。」我的理解，应该是连续出现 3 个 Dup Ack 才会导致快速重传，进而进入快速恢复阶段吧。</div>2023-04-03</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/17/37/a0/032d0828.jpg" width="30px"><span>上杉夏香</span> 👍（0） 💬（0）<div>老师，有个问题。原文为「我们再回到上面这张图，因为接收端没有接收到第 2 个 segment，因此接收端每次收到一个新的 segment 后都会去 ack 第 2 个 segment，即 ack 17。紧接着，发送端就会接收到三个相同的 ack（ack 17）。连续出现了 3 个响应的 ack 后，发送端会据此判断数据包出现了丢失，于是就进入了下一个阶段：快速重传。」</div>2023-04-03</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/4d/49/28e73b9c.jpg" width="30px"><span>明翼</span> 👍（0） 💬（0）<div>&quot;如上图所示，接收方在收到数据包后，会给发送方回一个 ack，然后把自己的 rwnd 大小写入到 TCP 头部的 win 这个字段，这样发送方就能根据这个字段来知道接收方的 rwnd 了。接下来，发送方在发送下一个 TCP segment 的时候，会先对比发送方的 cwnd 和接收方的 rwnd，得出这二者之间的较小值，然后控制发送的 TCP segment 个数不能超过这个较小值。&quot;

老师你好，这段话说发送的tcp报文个数不能超过拥塞控制窗口和接受窗口的最小值，怎么我在其他资料上看到接受窗口单位是字节数，我哪里理解错了，谢谢</div>2022-02-18</li><br/>
</ul>