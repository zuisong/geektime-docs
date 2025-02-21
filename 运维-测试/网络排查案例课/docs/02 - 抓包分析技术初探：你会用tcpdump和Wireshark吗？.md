你好，我是胜辉。

咱们这门课最核心的内容，恐怕就是抓包分析了。在众多的排查技术中，抓包分析可以说是“皇冠上的明珠”，也是包括我自己在内的很多人一直努力的方向。所以，tcpdump和Wireshark这两个工具在工程师心目中的位置，自然不用我多提了。相信你能来上这门课，也很大程度上是想把这两个工具好好学一下的。

不过，你了解这两个工具的过去吗？它们最初是怎么出现的，又是什么样的机制使得它们如此强大呢？

这节课，我就带你走进抓包分析技术大家庭。你会从中了解到抓包分析技术的光荣历史和渊源，以及通过实际的例子，感受到它的精妙设计和强大能力。当你理解了tcpdump和Wireshark的初步用法之后，你对常见的抓包需求场景也就能心里有数，知道大概从哪里下手了。

## 这些抓包技术名词，你分清楚了吗？

首先，我帮你捋一下这些技术的来龙去脉甚至“八卦”，这样你在进入后面课程的具体技术学习时，就会多几分亲近感，也多几分底气了。

- **tcpdump**

我们先来认识大名鼎鼎的tcpdump。1988年，劳伦斯伯克利国家实验室的四位工程师编写出了tcpdump这个殿堂级的工具。这个实验室呢，也很值得我们尊敬。这里涌现过[13位](https://www.lbl.gov/nobelists)诺贝尔奖获得者，其中包括1997年获得物理学奖的华人巨匠朱棣文，可见这是多么耀眼的一块科学圣地。
<div><strong>精选留言（30）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/12/21/b8/aca814dd.jpg" width="30px"><span>江山如画</span> 👍（33） 💬（4）<div>问题1:
通过偏移量方法抓取 SYN 包：tcpdump -i any &#39;tcp[13]&amp;2 !=0&#39;
通过标志位方法抓取 SYN 包：tcpdump -i any &#39;tcp[tcpflags]&amp;tcp-syn !=0&#39;

问题2:
tcpdump -i eth0 -s 34

老师对于问题2有个疑问，我最开始用的命令是&quot;tcpdump -i any -s 34&quot;，发现 -s 写成 34 抓不到网络层的目的地址字段，用 wireshark 分析发现帧头(不知道还叫不叫这个，wireshark 显示为 Linux cooked capture v1)占了 16 个字节，写成 36 就能把信息抓全了，但是写成&quot;tcpdump -i eth0 -s 34&quot; 就可以抓全</div>2022-01-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/7f/d3/b5896293.jpg" width="30px"><span>Realm</span> 👍（13） 💬（1）<div>补充一点基础知识，tcp的标志位在第13字节（具体可以看tcp header报文）

当我们只想过滤仅有SYN标志的包时，第14个字节的二进制是00000010,十进制是2
# tcpdump -i eth1 &#39;tcp[13] = 2&#39; 

匹配SYN+ACK包时(二进制是00010010或是十进制18)
# tcpdump -i eth1 &#39;tcp[13] = 18&#39;

匹配SYN或是SYN+ACK的数据时
# tcpdump -i eth1 &#39;tcp[13] &amp; 2 = 2&#39;</div>2022-01-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/18/a5/34/6e3e962f.jpg" width="30px"><span>yayiyaya</span> 👍（10） 💬（1）<div>1. 抓取 TCP SYN 包：  tcpdump  &#39;tcp[13] = 2&#39;  -w file.pcap
2. tcpdump -s 34  -w file.pcap
</div>2022-01-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/27/ce/58/71ed845f.jpg" width="30px"><span>Dexter</span> 👍（5） 💬（1）<div> tcpdump -i any -n &#39;tcp[tcpflags]&amp;(tcp-rst) !=0&#39; 。 请问一下tcp[tcpflags]&amp;(tcp-rst)  这中间的&amp;表示的是按位与吗？</div>2022-02-05</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/DYAIOgq83eovXluTbBvyjZQ5zY8e3AZLONj6Qx5mcF4G7ZWYVbeicDzOlakFj4dKh6jCFHfqXvrLccuiaxYicmTxg/132" width="30px"><span>远方的风</span> 👍（3） 💬（6）<div>请教个问题，我们用java写了一个展示图片的http接口，通过nginx转发，但是偶现图片展示不了nginx发送0字节的情况，请问这种如何排查？</div>2022-01-14</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/egApicxPAjbmdviavYc8Tc5HelLicQTicW9KgwRl9U2mCEibLTA3rCZ6PVlxRFZTddY7ZGC2DmRe8DJ8EKCZ6mLhkzg/132" width="30px"><span>谦逊的禾苗</span> 👍（2） 💬（1）<div>太难了 我以为我有基础，发觉我这是0</div>2022-06-27</li><br/><li><img src="" width="30px"><span>Geek_4996c9</span> 👍（2） 💬（1）<div>tcp[tcpflags] 这个tcpflags是指啥 固定语法格式吗？
</div>2022-04-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/2c/26/02/a2c6d49b.jpg" width="30px"><span>D⃰a⃰b⃰i⃰n⃰g⃰</span> 👍（2） 💬（5）<div>tcpdump这个软件百度下载吗，不会操作</div>2022-01-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/23/52/66/3e4d4846.jpg" width="30px"><span>includestdio.h</span> 👍（2） 💬（2）<div>问题已经有人回答了，那我就问个小问题吧哈哈，想问下老师文章里的libcap和bpf 关系图老师是用什么做的</div>2022-01-16</li><br/><li><img src="" width="30px"><span>Geek_601e15</span> 👍（1） 💬（1）<div>老师哪里有说明报文中哪个字段是0x.....  就代表syn，或者tls吗？</div>2023-08-05</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/ef/a2/6ea5bb9e.jpg" width="30px"><span>LEON</span> 👍（1） 💬（1）<div> 老师，请教下，wireshark 页面最下方，最左侧0x000这列是什么意思？
还有最右面这列，为啥有的能显示HTTP报文内容，有的是乱码和点？
谢谢
0x0000:  4500 0038 282d 0000 4006 3a83 0a00 0202  E..8(-..@.:.....
  0x0010:  0a00 020f cc5d 0050 0502 3a02 3ed1 3771  .....].P..:.&gt;.7q
  0x0020:  5018 ffff 4421 0000 4745 5420 2f20 4854  P...D!..GET.&#47;.HT
  0x0030:  5450 2f31 2e31 0d0a                      TP&#47;1.1..</div>2023-01-09</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/DYAIOgq83eqRISt77TSBaRuC5DdzmuiaeydT4nGVsI2NI62jvx8sMBNkzZPIEhkLTFBCWGY4piam32y3v9DV2qjQ/132" width="30px"><span>张太</span> 👍（1） 💬（1）<div>1、抓取client hello数据包：
wireshark的过滤条件可以为：tls.handshake.type == 1 
但是实际上tcpdump抓包时，需要使用tcp偏移量，
有点类似wireshark的过滤命令和嗅探命令
</div>2022-05-30</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/2c/47/1a/a5673d03.jpg" width="30px"><span>pathfinder</span> 👍（0） 💬（1）<div>问题：tcpdump -w file.pcap &#39;tcp[13]&amp;4 != 0&#39;  这个4是十进制还是十六进制呢？</div>2024-07-30</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/36/8b/7a/ec36ff82.jpg" width="30px"><span>原则</span> 👍（0） 💬（1）<div>这门课被名字给耽误了，价值太大了，很多人以为自己抓过包，就会了，其实不然啊，很多细节都值得推敲！</div>2023-05-25</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/36/8b/7a/ec36ff82.jpg" width="30px"><span>原则</span> 👍（0） 💬（1）<div>老师该如何统计乱序包的占比？</div>2023-05-25</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/d4/37/aa152ddb.jpg" width="30px"><span>AshinInfo</span> 👍（0） 💬（1）<div>老师，您最后一个视频，介绍wireshark的软件，说frame 是二层，是不是说错了，这个是物理层把，二层是Ehternet II吧</div>2022-08-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/47/00/3202bdf0.jpg" width="30px"><span>piboye</span> 👍（0） 💬（2）<div>老师, linux 有办法 像windows 那样捕获特定程序的包吗?
我看stackoverflow 上有人建议是用  namespace 隔离程序的 network 来抓取.
android 手机的 App 是每个app 一个uid,   这个可以通过 iptable 打标记来标识App 的出流量.
有其它更简单的方法吗?</div>2022-07-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/47/00/3202bdf0.jpg" width="30px"><span>piboye</span> 👍（0） 💬（1）<div>老师讲的太好了</div>2022-07-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/ce/d7/5315f6ce.jpg" width="30px"><span>不负青春不负己🤘</span> 👍（0） 💬（1）<div>有点看不懂了,主要是不了解TCP报文每个位置的含义啊
</div>2022-06-15</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/AkcVibvqux0qrKFbV7skQvQfHsl96tu9HTSaromQyzf7OOSacoorSDreBNbwOdlBeOrKr3Alc1zle66wKkibrL5g/132" width="30px"><span>学生监狱</span> 👍（0） 💬（2）<div>大家有没有在centos 7上把tcptrace给安装部署起来？现在网上的包都不是这个版本。有找到对应的版本的话，帮忙甩个链接。</div>2022-04-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1b/96/47/93838ff7.jpg" width="30px"><span>青鸟飞鱼</span> 👍（0） 💬（1）<div>老师，我想提一个建议，我最近在整理wireshark中具体某个报文中，展开后，网络层和传输层各个字段代表什么意思？网上资料需要查的同时，答案各不相同，对于小白来说，完全不知道对错。老师，在课程中介绍某些字段时，都是需要哪里介绍哪些，有点分散，而且不是很全。比如DF字段，如果不知道的话，可能都不知道在哪里找？</div>2022-03-30</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/28/2e/0c/b6180a5f.jpg" width="30px"><span>风铃</span> 👍（0） 💬（2）<div>这两个工具之前就没有怎么用过，完全听不懂</div>2022-03-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1e/0d/bf/aa2d6ba8.jpg" width="30px"><span>葫芦娃</span> 👍（0） 💬（2）<div>在实际生产环境中，我想抓生产环境的包，是不是最好使用tcpdump通过命令抓到包，生成文件，然后在下载下来使用本地的Wireshark来分析？其实我是想问在生产环境能不能直接使用Wireshark工具？</div>2022-03-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/f6/58/7458ac2e.jpg" width="30px"><span>Blue</span> 👍（0） 💬（1）<div>tcpdump &#39;tcp[13]&amp;2!=0&#39; -w file.pcap
tcpdump -s 34 -w file.pcap</div>2022-02-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/d4/37/aa152ddb.jpg" width="30px"><span>AshinInfo</span> 👍（0） 💬（1）<div>要搞清楚这一点也很简单，我们可以利用 IP 的 TTL 属性。显然，无论是哪一端，它的报文在发出时，其 TTL 就是原始值，也就是 64、128、255 中的某一个。而对端报文的 TTL，因为会经过若干个网络跳数，所以一般都会比 64、128、255 这几个数值要小一些。


这个并不能作为依据吧，我在自己的电脑打开wireshark，抓取本地网卡，有64、128、255的报文，也有小于他们的报文，这不就矛盾了吗</div>2022-02-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1b/96/47/93838ff7.jpg" width="30px"><span>青鸟飞鱼</span> 👍（0） 💬（2）<div>问个很傻的问题，老师是在mac上装的虚拟机做服务端吧？我用docker一直没弄出来</div>2022-01-31</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/18/c3/eb/528a1d68.jpg" width="30px"><span>beanSeedling</span> 👍（0） 💬（2）<div>1.
偏移量:tcpdump &#39;tcp[tcpflags]&amp;(tcp-syn) != 0&#39;
预定义过滤器:tcpdump &#39;tcp[13]&amp;2 != 0&#39;
2.tcpdump -s 34 #14位帧头+20位IP头</div>2022-01-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/8a/1d/abb7bfe3.jpg" width="30px"><span>熹</span> 👍（0） 💬（1）<div>1. tcpdump host xxxx and &#39;tcp[tcpflags] == tcp-syn&#39;
2. tcpdump -s 34 </div>2022-01-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/23/5b/983408b9.jpg" width="30px"><span>悟空聊架构</span> 👍（1） 💬（0）<div>第二题：如果确定问题是在 IP 层，tcpdump 命令如何写，可以做到既找到 IP 层的问题，又节约抓包文件大小呢？
答：tcpdump -s 34  -w file.pcap
-s 长度，可以只抓取每个报文的一定长度。
帧头 14 字节。
IP头 20 字节。
TCP 头 32 字节。
所有只需要抓取帧头（14字节）和 IP 头（20字节）的数据，后面的 TCP 头和后面的报文就不需要抓取了。</div>2024-10-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/23/5b/983408b9.jpg" width="30px"><span>悟空聊架构</span> 👍（1） 💬（0）<div>总结下评论区的留言，以及查阅资料的内容。

第一题：请你用偏移量方法，写一个 tcpdump 抓取 TCP SYN 包的过滤表达式。

答：
来自 @Realm 同学：
匹配SYN+ACK包时(二进制是00010010或是十进制18)
# tcpdump -i eth1 &#39;tcp[13] = 18&#39;
匹配SYN或是SYN+ACK的数据时
# tcpdump -i eth1 &#39;tcp[13] &amp; 2 = 2&#39;
-------
参考这篇 rfc793 文章： https:&#47;&#47;datatracker.ietf.org&#47;doc&#47;html&#47;rfc793#section-3.1
从第 13 字节开始，是 TCP 的控制标志位，这些标志位依次为 URG、ACK、PSH、RST、SYN、FIN等。

SYN 为倒数第二位 00000010
ACK 为倒数第五位 00010000

在 TCP 协议中，控制标志位位于 TCP 头部，这些标志位用于控制 TCP 连接的状态和行为。TCP 头部的最小长度是 20 字节，其中前 12 字节包含了源端口、目的端口、序列号和确认号等信息。从第 13 字节开始，是 TCP 的控制标志位，这些标志位包括 SYN、ACK、FIN、RST、PSH、URG 等。
TCP 头部的结构如下：
源端口（Source Port）和目的端口（Destination Port）：各占 2 字节，共 4 字节。
序列号（Sequence Number）：4 字节。
确认号（Acknowledgment Number）：4 字节。
数据偏移（Data Offset）：1 字节，指示 TCP 头部的长度。
保留位（Reserved）：1 字节，目前必须置为 0。
控制标志位（Control Flags）：1 字节，包含 SYN、ACK、FIN、RST、PSH、URG 等标志位。
窗口大小（Window Size）：2 字节。
校验和（Checksum）：2 字节。
紧急指针（Urgent Pointer）：2 字节（如果 URG 标志位为 1 时使用）。
控制标志位的具体含义如下：
SYN（Synchronize Sequence Numbers）：同步序列编号，用于建立连接时同步序列编号。在 TCP 三次握手过程中，SYN 标志位被设置为 1，以发起一个新的连接请求 
ACK（Acknowledgment）：确认标志位，用于确认收到的数据。当 ACK 标志位为 1 时，确认号字段有效，表示对已成功接收的数据段的确认
FIN（Finish）：结束标志位，用于释放连接。当 FIN 标志位为 1 时，表示发送方已经没有数据要发送了，希望终止连接 
RST（Reset）：重置连接。当 RST 标志位为 1 时，表示连接需要被重置或拒绝一个非法的段
PSH（Push）：推送标志位，用于提示接收方应尽快将数据推送给应用层 
URG（Urgent）：紧急标志位，用于指示数据包中有紧急数据，需要优先处理 </div>2024-10-28</li><br/>
</ul>