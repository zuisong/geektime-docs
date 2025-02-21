你好，我是胜辉。今天这节课，我们要通过实际的案例，来学习下TCP挥手的知识，在实战中加深对这些知识的理解。

我们在做一些应用排查的时候，时常会在日志里看到跟TCP有关的报错。比如在Nginx的日志里面，可能就有connection reset by peer这种报错。“连接被对端reset（重置）”，这个字面上的意思是看明白了。但是，心里不免发毛：

- 这个reset会影响我们的业务吗，这次事务到底有没有成功呢?
- 这个reset发生在具体什么阶段，属于TCP的正常断连吗？
- 我们要怎么做才能避免这种reset呢？

要回答这类追问，Nginx日志可能就不够用了。

事实上，网络分层的好处是在于每一层都专心做好自己的事情就行了。而坏处也不是没有，这种情况就是如此：应用层只知道操作系统告诉它，“喂，你的连接被reset了”。但是为什么会被reset呢？应用层无法知道，只有操作系统知道，但是操作系统只是把事情处理掉，往内部reset计数器里加1，但也不记录这次reset的前后上下文。

所以，为了搞清楚connection reset by peer时具体发生了什么，我们需要**突破应用层这口井，跳出来看到更大的网络世界**。

## 在应用层和网络层之间搭建桥梁
<div><strong>精选留言（30）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/12/f5/d1/cc6f82eb.jpg" width="30px"><span>kaixiao7</span> 👍（15） 💬（1）<div>老师，在客户端握手的第三个RST+ACK报文中，为什么会出现RST呢？有哪些情况会出现呢？</div>2022-05-03</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/8f/cf/890f82d6.jpg" width="30px"><span>那时刻</span> 👍（15） 💬（5）<div>请问老师，客户端用 RST 来断开连接并不妥当，需要从代码上找原因。比如客户端在 Receive Buffer 里还有数据未被读取的情况下，就调用了 close()。调用close，是不是应该发fin包呢？什么时候会发rst包？</div>2022-01-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/2c/45/c6/28dfdbc9.jpg" width="30px"><span>*</span> 👍（9） 💬（4）<div>老师，tcp.ack和tcp.flags.ack有什么不同，为什么问题1的答案是tcp.ack==1 and tcp.flags.reset == 1</div>2022-01-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/57/4f/6fb51ff1.jpg" width="30px"><span>奕</span> 👍（5） 💬（3）<div>最后一个图 有个疑问的， 为什么客户端在初始化关闭的时候 除了发送一个 FIN ，还有个 ACK呢，是为了回复上一个服务端发送的数据吗？</div>2022-01-25</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/c1/23/fa377732.jpg" width="30px"><span>乌龟爱上金鱼</span> 👍（4） 💬（2）<div>老师您好，对端向我发了fin，我这边ack后没有close，进入closewait，对端现在应该是finwait2，按理来说对端现在只是不向我发送数据了，但是能接受数据，但是我继续向对端发送数据后，对端回复的是reset，这是为什么呀？</div>2022-09-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/17/37/a0/032d0828.jpg" width="30px"><span>上杉夏香</span> 👍（4） 💬（1）<div>这篇文章的最后一张图，是不是有些瑕疵？进入半连接状态后，服务端继续发送数据，当服务器发送FIN报文的时候，它的seq应该不再是L？</div>2022-06-27</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/BQaJmDRTUXyNIzH6SwM27kXQibyDUlJ3vibiaIUmRe9j1I4K5fLDnOf6Uicibj2gBsSeWA4zKoUMN803oFD4gAHuiblA/132" width="30px"><span>lxj</span> 👍（3） 💬（1）<div>有一点点小提议，分析一个问题能把如何抓包，在哪端抓包，抓包时间点，过滤条件再交代详细点嘛，感觉分析的粒度太粗了，上下文没有交代清楚</div>2022-04-04</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/22/73/76/a08f9af2.jpg" width="30px"><span>sysho</span> 👍（2） 💬（1）<div>这两个月刚好排查了几个抓包问题，觉得老师这节课讲得真好，看得很爽。</div>2022-04-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/18/b7/24/17f6c240.jpg" width="30px"><span>janey</span> 👍（1） 💬（1）<div>这里有疑问，上一句说“Nginx 都不知道还存在过这么一次失败的握手”下一句又说“在客户端日志里，是可以记录到这次握手失败的。” 那怎么知道“这个虽然也是 RST，但并不是我们要找的那种“在连接建立后发生的 RST””的？</div>2022-12-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1f/b3/e3/a66c8c75.jpg" width="30px"><span>邓坤坤</span> 👍（1） 💬（1）<div>老师，请问应用层如何编码才能在发送数据时带上fin flag？从来没见过这种</div>2022-08-01</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/69/21/7db9faf1.jpg" width="30px"><span>简迷离</span> 👍（1） 💬（1）<div>老师，案例中的抓包文件能提供下吗？这样单独的看文章分析效果还是有限，能提供下案例抓包文件边看边分析数据包效果更佳，还请老师提供下，谢谢您！</div>2022-03-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/9f/a1/d75219ee.jpg" width="30px"><span>po</span> 👍（1） 💬（2）<div>你看，这次客户端在握手中的第三个包不是 ACK，而是 RST（或者 RST+ACK），握手不是失败了吗？那么自然地，这次失败的握手，也不会转化为一次有效的连接了，所以 Nginx 都不知道还存在过这么一次失败的握手。

Nginx为什么会不知道握手失败呢？</div>2022-03-12</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/DYAIOgq83eoSffTqghG7YNWv5b4mEibbQh0ARr5Ar5U9qIE2BSCOjlmbfflhLDjQKsok9TvhCcV4PrVc1SsAD9w/132" width="30px"><span>仲晶晶</span> 👍（1） 💬（1）<div>老师您好，我这边做openresty测试的时候遇到个现象：
jemter通过F5压测到openresty网关的时候（TPS 5k-6k）左右，这个时候用的都是短链接，我就看到很多TW，这说明断链都是在网关这边断链的，我比较疑惑什么情况下服务端（网关）会发生断链呢（发FIN）？</div>2022-01-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/98/b1/f89a84d0.jpg" width="30px"><span>wu526</span> 👍（1） 💬（4）<div>老师请问一下，TIME_WAIT 需要等待2个MSL, 如果不等待2个MSL，此时直接使用该端口连接服务器，在建立连接的过程中，如果收到了服务端重发的FIN+ACK,此时客户端会做什么处理呢？</div>2022-01-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/23/52/66/3e4d4846.jpg" width="30px"><span>includestdio.h</span> 👍（1） 💬（1）<div>1.不太了解挥手阶段的RST特征，不确定对不对。tcp.flags.reset eq 1 and tcp.fin eq 1，感觉差点啥

2.实际工作中对抓包一知半解，基本只会通过RST分析问题大致在哪端，后续就不会了，希望通过专栏能得到提升</div>2022-01-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/b3/c5/7fc124e2.jpg" width="30px"><span>Liam</span> 👍（1） 💬（1）<div>前面提到的挥手时搭便车，指的是第二次和第三次挥手合并在一起吗，总共减少了一次挥手</div>2022-01-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/23/5b/983408b9.jpg" width="30px"><span>悟空聊架构</span> 👍（0） 💬（2）<div>一、对文章内容有点疑问：

 1.1、TCP 挥手阶段，我抓包看到的都是 

(1)发起端 FIN,ACK  

(2) 接收端 ACk

(3) 发起端  FIN,ACK

(4) 接收端ACK

而文中的（1）（4）都是 FIN，不带 ACK。

1. 2、最后一张 Stevens 的图，第四次挥手应该是 ACK， SEQ=K+1，ACK+1，这个是我抓包看到的结果。

二、对课后习题有点疑问

 2.1 第一题答案为啥是 tcp.flags.ack == 1 and tcp.flags.reset == 1 ？

tcp.flags.ack = 1 很多阶段都会出现，比如三次握手的最后一次握手，怎么判断当 tcp.flags.ack = 1 一定就是挥手阶段。

2.2 遇到的案例，通过抓包分析到客户端发送的两个数据包被服务端处理时，到1024 字节就截断了， 然后其中有个字节被丢弃了，导致程序判断时出现问题。

具体的排查总结在这里：

标题：真·卡了一个1024的 Bug，TCP 的数据包看吐了！

链接地址：https:&#47;&#47;mp.weixin.qq.com&#47;s&#47;ZfANeLutMkFMvH__apO5MQ  

半知半解的排查，很多地方不懂，还有好多知识要啃。</div>2024-10-30</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/2c/a7/7f702c49.jpg" width="30px"><span>liy</span> 👍（0） 💬（1）<div>请问老师，用curl库发post，结果返回一长串的SOAP-ENV链接，这种是什么错误啊</div>2023-06-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/47/00/3202bdf0.jpg" width="30px"><span>piboye</span> 👍（0） 💬（1）<div>sync 包的 seq 我想的是 ISN 现在已经随机化了,  怎么会是1呢? 仔细看 Wireshark的detail 部分, 才发现wireshark 帮我们计算成相对seq了,  棒</div>2022-07-25</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/f0/6d/3e570bb8.jpg" width="30px"><span>一打七</span> 👍（0） 💬（1）<div>如果线上请求量很大，而异常关闭可能一个小时才发生一次，为了定位问题，得一直开着tcpdump，那么.pcap文件岂不是非常大，这个怎么处理？还望老师能解答</div>2022-04-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/c4/03/f753fda7.jpg" width="30px"><span>JianXu</span> 👍（0） 💬（3）<div>第一个案例 第一次filter 掉的 握手时候客户端发往服务端的RST SEQ=1, ACK=1为什么会出现呢？ 没有办法理解为什么客户端刚发SYN,  收到服务端ACK 后立即RST 

第二次filter 掉的挥手那张图，看上去也是客户端给服务端的443 端口直接先发一个FIN , 然后接着就是 RST SEQ=2, ACK=1,  那这个对应客户端应用代码大概会是什么样呢？</div>2022-03-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/26/b1/cc902a24.jpg" width="30px"><span>三三</span> 👍（0） 💬（3）<div>我目前遇到的问题是：前台看见nginx connection timeout报错，然而后台数据已经处理了。偶发问题</div>2022-03-05</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/38/5e/f0394817.jpg" width="30px"><span>费曼先生</span> 👍（0） 💬（3）<div>老师你好，过滤条件tcp.stream eq 1098是从哪里来的？</div>2022-02-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/19/5a/5f/8a76aa8b.jpg" width="30px"><span>Lordran</span> 👍（0） 💬（1）<div>&quot;但是有意思的是，这个 POST 还是成功了，已经被正常处理完了，要不然 Nginx 也不会回复 HTTP 200。&quot;这里的表述有点怪怪的，既然已经返回了200，排除接口异步处理的话，是已经成功了啊，为什么说&quot;有意思的是，要不然&quot;呢？有点不解。</div>2022-01-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/44/6d/6cfc4d8b.jpg" width="30px"><span>松鼠</span> 👍（0） 💬（3）<div>tcp.seq eq 1 and tcp.ack eq 1  这个取反 不是 ! (tcp.seq eq 1 and tcp.ack eq 1) 么， 怎么是or</div>2022-01-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/1f/08/bc66fc56.jpg" width="30px"><span>追风少年</span> 👍（0） 💬（2）<div>老师好，碰到一个问题，一个java应用假死，使用命令lsof -n| grep java进程号 | grep CLOSE_WAIT ，发现存在在大量的CLOSE_WAIT状态的TCP信息，重启服务器端应用恢复正常，应该从哪方面入手排查好一些
http-nio-  14922  IPv6         2415378463       0t0        TCP 本机ip:radan-http-&gt;ip1:55250 (CLOSE_WAIT)
http-nio-  14922  IPv6         2416104072       0t0        TCP 本机ip:radan-http-&gt;ip2:32900 (CLOSE_WAIT)
http-nio-  14922  IPv6         2416104073       0t0        TCP 本机ip:radan-http-&gt;ip3:32934 (CLOSE_WAIT)
</div>2022-01-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/57/4f/6fb51ff1.jpg" width="30px"><span>奕</span> 👍（0） 💬（1）<div>tcpdump -w 文件名 抓包完成后发现文件的大小为0， 内容没有写入进去，这是什么原因的？
2265 packets captured
2352 packets received by filter
0 packets dropped by kernel

环境：linux Centos7</div>2022-01-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/9f/a1/d75219ee.jpg" width="30px"><span>po</span> 👍（0） 💬（3）<div>老师我最近一个网络超时的问题，nginx在某段时间去连接upstream都超时了，最后这个请求失败我做了以下尝试，1、我在nginx去用curl循环并且设置了超时是100毫秒，确实有时候会复现网络超时。2、我们ping去请求ip，没有发现丢包。3、找了网络组的同事让他们看看vpn有没有丢包，看了监控也是ok正常的。4、在upstream的几台机器互相curl请求都是正常不超时，这样看又和服务没关系。这下没太大思路，麻烦老师指点一下思路</div>2022-01-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/f7/b1/982ea185.jpg" width="30px"><span>美妙的代码</span> 👍（0） 💬（4）<div>老师，我一个场景是上传ipa包至AppStore。但是经常出错，上传失败。 我抓包看见，客服端端口指向服务端端口方向，tcp flags为reset。 不知道为什么会被重置，而且是客服端 发给服务端的。请问你老师有什么抓取建议么？</div>2022-01-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/4d/97/82e652a4.jpg" width="30px"><span>加了盐海盗</span> 👍（0） 💬（1）<div>还有知识拓展这两种形式
我们系统作为客户端就有这两种形式
我们请求发给服务端，服务端发送完响应信息后，服务端发起挥手。
也有我们请求发给服务端然后就发起挥手，等服务端响应完后然后开始挥手。这里有个说法就是关闭发送通道，不关闭接受通道。</div>2022-01-19</li><br/>
</ul>