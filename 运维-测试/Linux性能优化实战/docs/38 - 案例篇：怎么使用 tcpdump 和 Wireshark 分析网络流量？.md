你好，我是倪朋飞。

上一节，我们学习了 DNS 性能问题的分析和优化方法。简单回顾一下，DNS 可以提供域名和 IP 地址的映射关系，也是一种常用的全局负载均衡（GSLB）实现方法。

通常，需要暴露到公网的服务，都会绑定一个域名，既方便了人们记忆，也避免了后台服务 IP 地址的变更影响到用户。

不过要注意，DNS 解析受到各种网络状况的影响，性能可能不稳定。比如公网延迟增大，缓存过期导致要重新去上游服务器请求，或者流量高峰时 DNS 服务器性能不足等，都会导致 DNS 响应的延迟增大。

此时，可以借助 nslookup 或者 dig 的调试功能，分析 DNS 的解析过程，再配合 ping 等工具调试 DNS 服务器的延迟，从而定位出性能瓶颈。通常，你可以用缓存、预取、HTTPDNS 等方法，优化 DNS 的性能。

上一节我们用到的ping，是一个最常用的测试服务延迟的工具。很多情况下，ping 可以帮我们定位出延迟问题，不过有时候， ping 本身也会出现意想不到的问题。这时，就需要我们抓取ping 命令执行时收发的网络包，然后分析这些网络包，进而找出问题根源。

tcpdump 和 Wireshark 就是最常用的网络抓包和分析工具，更是分析网络性能必不可少的利器。
<div><strong>精选留言（30）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/12/f4/5c/e0a56bbf.jpg" width="30px"><span>1+1</span> 👍（69） 💬（3）<div>wireshark的使用推荐阅读林沛满的《Wireshark网络分析就这么简单》和《Wireshark网络分析的艺术》</div>2019-02-18</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/mnBC29lF1RibHdwkZdPdGM9QRAl7Y7Aicad8vpmIEialjia93IEVSAHibkKdwHwfZr6qedVHiafKUD8Yk1v2eiaibj8l0w/132" width="30px"><span>xierongfei</span> 👍（37） 💬（3）<div>之前公司一个内部应用出现页面卡顿，而且每次都是1-2用户反馈（随机），排出了应用本身，服务器，客户端网络问题后，然后让it在用户端抓包传给我，然后用Wireshark分析后，发现有大量虚假重传，后面分析后发现，是用户都在一个Nat网络后面，部分用户时间不一致，同时我们服务器开启了tcp快速回收，导致连接被回收了。后面关闭tcp快速回收后解决。也是第一次用工具分析这种比较复杂的问题。</div>2019-04-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/f5/a0/c342c50e.jpg" width="30px"><span>bzadhere</span> 👍（20） 💬（2）<div>&quot;如果看了这个你还是不会用Wireshark，那就来找我吧&quot; ----这是在网上可以找到最牛逼的资料

https:&#47;&#47;www.dell.com&#47;community&#47;%E6%95%B0%E6%8D%AE%E5%AD%98%E5%82%A8%E8%AE%A8%E8%AE%BA%E5%8C%BA&#47;%E5%A6%82%E6%9E%9C%E7%9C%8B%E4%BA%86%E8%BF%99%E4%B8%AA%E4%BD%A0%E8%BF%98%E6%98%AF%E4%B8%8D%E4%BC%9A%E7%94%A8Wireshark-%E9%82%A3%E5%B0%B1%E6%9D%A5%E6%89%BE%E6%88%91%E5%90%A7-8%E6%9C%886%E6%97%A5%E5%AE%8C%E7%BB%93&#47;td-p&#47;7007033</div>2019-03-06</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/20/b0/0a1551c4.jpg" width="30px"><span>日拱一卒</span> 👍（20） 💬（1）<div>林沛满的书都看过，确实写的相当好，都是案例驱动。
把协议讲的生动有趣就数他。</div>2019-02-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/7c/59/26b1e65a.jpg" width="30px"><span>科学Jia</span> 👍（13） 💬（2）<div>老师，这个案例写的极其生动:D, 就是问一句，现在我们的项目都是https，那么如果抓包https，tcpdump或者wireshark是否可以解密？因为我看到wireshark解密需要private key，但是private key涉及安全问题，肯定都拿不到，那么你们遇到抓包https后解析是怎么做的呢？</div>2019-03-05</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/44/f8/6fdb50ab.jpg" width="30px"><span>肖飞码字</span> 👍（12） 💬（1）<div>tcpdump抓包可以用来处理一些疑难问题的。 如受到了什么类型的攻击，执行了mysql的什么命令，接收以及发送出去了什么数据包通通都可以。像入侵检测如snort工具之类的应该也是对数据包进行抓包分析的，很实用，很强大。</div>2019-02-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/25/66/4835d92e.jpg" width="30px"><span>潘政宇</span> 👍（9） 💬（2）<div>老师好，为什么ping命令使用PTR信息，ping一个域名的时候，直接dns查询得到A记录ip地址，然后ping这个ip就行啊，为什么使用反向解析？</div>2019-02-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/4d/49/28e73b9c.jpg" width="30px"><span>明翼</span> 👍（7） 💬（3）<div>老师wireshark有个命令行版本tshark，wireshark是通过一个叫dump的进程抓包管道方式发送给tshark解析的，不过tshark的命令项有点多，不是太好用</div>2019-02-18</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTKzqiaZnBw2myRWY802u48Rw3W2zDtKoFQ6vN63m4FdyjibM21FfaOYe8MbMpemUdxXJeQH6fRdVbZA/132" width="30px"><span>kissingers</span> 👍（6） 💬（1）<div>林沛满的书不错，EMC 大牛值得推荐。
Fiddler，工具也了解过，微软的人写的，支持https （man in middle），能修改请求和响应数据包。
另外老师能讲讲：linux 主机上怎么提高数据转发性能吗？</div>2019-03-07</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/97/61/34a0da09.jpg" width="30px"><span>Griffin</span> 👍（3） 💬（1）<div>Web的问题推荐 MITM啊</div>2019-03-24</li><br/><li><img src="https://wx.qlogo.cn/mmopen/vi_32/PiajxSqBRaEKQMM4m7NHuicr55aRiblTSEWIYe0QqbpyHweaoAbG7j2v7UUElqqeP3Ihrm3UfDPDRb1Hv8LvPwXqA/132" width="30px"><span>ninuxer</span> 👍（3） 💬（1）<div>打卡day40
使用姿势跟老师的一样，都是tcpdump抓包后，拿到图形界面分析，如果是web问题，还会用下fiddler来分析</div>2019-02-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/64/05/6989dce6.jpg" width="30px"><span>我来也</span> 👍（2） 💬（1）<div>[D38打卡]
以前都是在windows上用Wireshark,想不到linux下也有Wireshark.
不过平常维护的linux只能用终端登录,在终端中还是用tcpdump.

今天看了专栏,才发现,可以用tcpdump抓包,然后用Wireshark来展示.这个厉害了.
</div>2019-02-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/65/ae/9727318e.jpg" width="30px"><span>Boy-struggle</span> 👍（1） 💬（1）<div>老师，最近我们遇到了一个关于vsftp问题，客户端返回错误码为28，官方解释是数据连接超时，到不清楚到底是从客户端分析还是服务端分析，我们用的是被动模式vsftp</div>2019-04-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/97/61/34a0da09.jpg" width="30px"><span>Griffin</span> 👍（1） 💬（1）<div>老师问个问题，我man tcpdump搜索-nn没找到结果，只有-n的介绍。我搜索了下发现在linuxquestions.org上有人问，并且回答者也是用的man，结果有-n和-nn的介绍。是我的man版本不对么？系统版本是18.04.1</div>2019-03-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/93/43/0e84492d.jpg" width="30px"><span>Maxwell</span> 👍（1） 💬（1）<div>ubantu下用tcpdump抓包后，下载到本地，windows版的wireshark打开抓包文件，一直未响应，是咋回事呢？</div>2019-03-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/3a/6e/e39e90ca.jpg" width="30px"><span>大坏狐狸</span> 👍（0） 💬（1）<div>由于TCP连接是全双工的，因此每个方向都必须单独进行关闭。这原则是当一方完成它的数据发送任务后就能发送一个FIN来终止这个方向的连接。收到一个 FIN只意味着这一方向上没有数据流动，一个TCP连接在收到一个FIN后仍能发送数据。首先进行关闭的一方将执行主动关闭，而另一方执行被动关闭。
（1） TCP客户端发送一个FIN，用来关闭客户到服务器的数据传送。
（2） 服务器收到这个FIN，它发回一个ACK，确认序号为收到的序号加1。和SYN一样，一个FIN将占用一个序号。
（3） 服务器关闭客户端的连接，发送一个FIN给客户端。
（4） 客户端发回ACK报文确认，并将确认序号设置为收到序号加1。


老师这个是百度百科的。请问第一个抓包的时候有FIN 没说有ACK ，但是上图中ACK=y+1; 而你的（Wireshark TCP 4-times close 示例 这句话的连接的图片，也是没有ACK的 。但是平常抓包确实会看到ACK。。。那老师 到底带不带ACK，第一次FIN的时候?）</div>2019-04-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/19/a0/b7/1327ae60.jpg" width="30px"><span>hellojd_gk</span> 👍（3） 💬（1）<div>如果换一个 DNS 服务器，就可以用 PTR 反查到 35.190.27.188 所对应的域名，到最后也没讲到为什么是googleaccount域名。</div>2020-03-30</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/83/4b/0e96fcae.jpg" width="30px"><span>sky</span> 👍（2） 💬（1）<div>实践的时候出现了以下错误，也没找到解决方案，有朋友遇到过吗

配置：
腾讯云 OS：ubuntu18.04 
CPU：2 
Mem：4G
Bandwidth：8Mbps

resolv.conf
nameserver 114.114.114.114
options edns0

root@VM-4-13-ubuntu:&#47;home&#47;ubuntu# nslookup -type=PTR 39.106.233.176 8.8.8.8
Server:         8.8.8.8
Address:        8.8.8.8#53

** server can&#39;t find 176.233.106.39.in-addr.arpa: NXDOMAIN</div>2022-02-16</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/82/3d/356fc3d6.jpg" width="30px"><span>忆水寒</span> 👍（1） 💬（0）<div>分析过很多问题，比如高峰期的时候，网络断连。

https:&#47;&#47;mp.weixin.qq.com&#47;s&#47;XS3Jnn3Xl4_12gzg0zrSTA</div>2021-08-01</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/18/5e/abb7bfe3.jpg" width="30px"><span>哈哈哈哈哈哈哈哈</span> 👍（1） 💬（1）<div>老师 对线上服务进行tcpdump会影响性能吗</div>2019-09-15</li><br/><li><img src="" width="30px"><span>Geek_abc043</span> 👍（0） 💬（0）<div>之前公司里用的也是Linux版本的wireshark抓包工具，挺好用的</div>2024-08-15</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/19/93/ce/092acd6a.jpg" width="30px"><span>孙同学</span> 👍（0） 💬（0）<div>在Mac M1环境下 执行ping timebang.org 抓包时 没有ptr请求 有人知道为啥么</div>2024-04-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/65/3a/bc801fb2.jpg" width="30px"><span>mqray</span> 👍（0） 💬（0）<div>之前有遇到过ping能通 curl也行(实际不行)后来tcpdump抓包发现tls握手过程没有完成导致失败，实际上是客户的ac做了限制</div>2023-09-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/de/00/c646dc88.jpg" width="30px"><span>丫头</span> 👍（0） 💬（0）<div>怎么安装tcpdump</div>2022-04-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/c4/03/f753fda7.jpg" width="30px"><span>JianXu</span> 👍（0） 💬（0）<div>我们部门现在使用iPvS 和 envoy 作分布式负载均衡，有人说这种情况用log 分析就可以了，没有必要使用tcpdump, 也有人说需要使用tcpdump,  为什么支持类似Netscalar nstrace 的能力，需要改动envoy 源代码，加载自定义的kernel module , 还要暂存key … 不知道兄弟公司有这样的需求吗？</div>2021-12-30</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/f6/24/547439f1.jpg" width="30px"><span>ghostwritten</span> 👍（0） 💬（0）<div>ping -c3 geektime.org
ping -n -c3 geektime.org
iptables -I INPUT -p udp --sport 53 -m string --string googleusercontent --algo bm -j DROP
iptables -D INPUT -p udp --sport 53 -m string --string googleusercontent --algo bm -j DROP
time nslookup geektime.org
 nslookup -type=PTR 35.190.27.188 8.8.8.8
tcpdump -nn udp port 53 or host 35.190.27.188
tcpdump -nn udp port 53 or host 35.190.27.188 -w ping.pcap
dig +short example.com
tcpdump -nn host 93.184.216.34 -w web.pcap</div>2021-07-30</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/02/75/2839c0bb.jpg" width="30px"><span>谨兮谨兮</span> 👍（0） 💬（0）<div>为什么ping域名出现ptr呢</div>2021-04-15</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/71/48/44df7f4e.jpg" width="30px"><span>凯</span> 👍（0） 💬（0）<div>每节课都受益匪浅</div>2020-11-05</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTKT9Tk01eiaQ9aAhszthzGm6lwruRWPXia1YYFozctrdRvKg0Usp8NbwuKBApwD0D6Fty2tib3RdtFJg/132" width="30px"><span>欧阳洲</span> 👍（0） 💬（0）<div>老师好，请教一下：
抓包并没看到 googleusercontent 的字样，这个字符串在哪里呢？
PTR的包倒是看到了in-addr.arpa的字样，iptables命令用in-addr.arpa代替googleusercontent应该也可以吧
</div>2020-09-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/de/65/51147fb6.jpg" width="30px"><span>北纬8℃</span> 👍（0） 💬（0）<div>老师，讲http改成https 是我们文章中提到的加了域名么。 我们http改成了https流量就崩了，第一次链接要15s，</div>2020-07-28</li><br/>
</ul>