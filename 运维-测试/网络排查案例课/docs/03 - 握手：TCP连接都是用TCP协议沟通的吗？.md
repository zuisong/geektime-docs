你好，我是胜辉。

在前面预习篇的两节课里，我们一起回顾和学习了网络分层模型与排查工具，也初步学习了一下抓包分析技术。相信现在的你，已经比刚开始的时候多了不少底气了。那么从今天开始，我们就要正式进入TCP这本大部头，而首先要攻破的，就是握手和挥手。

TCP的三次握手非常有名，我们工作中也时常能用到，所以这块知识的实用性是很强的。更不用说，技术面试里面，无论是什么岗位，似乎只要是技术岗，都可能会问到TCP握手。可见，它跟操作系统基础、编程基础等类似，同属于计算机技术的底座之一。

握手，说简单也简单，不就是三次握手嘛。说复杂也复杂，别看只是三次握手，中间还是有不少学问的，有些看似复杂的问题，也能用握手的技术来解决。不信你就跟我看这几个案例。

## TCP连接都是用TCP协议沟通的吗？

看到这个小标题，可能你都觉得奇怪了：TCP连接不用TCP协议沟通还用什么呢？

确实，一般来说TCP连接是标准的TCP三次握手完成的：

1. 客户端发送SYN；
2. 服务端收到SYN后，回复SYN+ACK；
3. 客户端收到SYN+ACK后，回复ACK。

这里面SYN会在两端各发送一次，表示“我准备好了，可以开始连接了”。ACK也是两端各发送了一次，表示“我知道你准备好了，我们开始通信吧”。
<div><strong>精选留言（30）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/14/d3/cc/bc01a9ef.jpg" width="30px"><span>某人</span> 👍（26） 💬（5）<div>数退避原则本身就不建议在精确的整秒做重试，为什么？</div>2022-01-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/24/b7/08/a6493073.jpg" width="30px"><span>MeowTvづ</span> 👍（20） 💬（1）<div>对于服务器端最多65535确实是个误区，其实这个跟很多都有关系的，比如服务器端的CPU、内存、fd数以及连接的情况，fd数是前提。一个连接会牵扯到服务端的接收缓冲区(net.ipv4.tcp_rmem)以及发送缓冲区(net.ipv4.tcp_wmem)，一个空的TCP连接会消耗3.3KB左右的内存，如果发数据的话，一个连接占用的内存会更大。所以理论上4GB的机器理论上支持的空TCP连接可以达到100W个。此外数据经过内核协议栈的处理需要CPU，所以CPU的好坏也会影响连接数。</div>2022-02-09</li><br/><li><img src="" width="30px"><span>Geek_cad238</span> 👍（11） 💬（3）<div>其实Window Scale是常识，并不是冷门，😂，关于这个，在林沛满大佬的《wireshark网络分析就这么简单》一书里有详细说明，大家可以一看。</div>2022-01-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/a1/bc/ef0f26fa.jpg" width="30px"><span>首富手记</span> 👍（8） 💬（1）<div>一个客户端（假设只有一个出口 IP）和一个服务端（假设也只有一个 IP 和一个服务端口），那么确实只能最多发起 6 万多个连接。针对这句话，在centos 和ubuntu系统默认的情况下，tcp是没有办法建立起6万多个链接的，因为 net.ipv4.ip_local_port_range 这个参数固定了机器当做client 发起请求的时候使用的端口范围，所以默认的情况下，单向智能建立28231 个链接，这个是我们真实生产服务器上发生过的问题；
因为程序释放tcp有问题，所以机器上的timewite 过多，然后把这两万多个端口用完了，导致了服务之间链接异常；</div>2022-01-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/17/d0/2b/c571c59f.jpg" width="30px"><span>steven</span> 👍（6） 💬（1）<div>在握手期间window是不会被scale放大的，但是我发现在传输过程中的window有260000+，但是握手的时候我客户端最大只有65535，服务端只有8000+，和我理解的有点不太一样呀</div>2022-03-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1d/5b/96/57d4970d.jpg" width="30px"><span>魏玉会 Gabby</span> 👍（6） 💬（1）<div>老师讲的真好，我一个前端人员也能看的懂</div>2022-01-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/18/c3/eb/528a1d68.jpg" width="30px"><span>beanSeedling</span> 👍（6） 💬（1）<div>
1.
第二次握手最大重传次数
tcp_synack_retries (integer; default: 5; since Linux 2.2)
              The maximum number of times a SYN&#47;ACK segment for a
              passive TCP connection will be retransmitted.  This number
              should not be higher than 255.
2.
This option is an offer, not a promise; both sides must send Window Scale options in their SYN segments to enable window scaling in either direction.
This option may be sent in an initial &lt;SYN&gt; segment (i.e., a segment with the SYN bit on and the ACK bit off).  It may also be sent in a &lt;SYN,ACK&gt; segment, but only if a Window Scale option was received in the initial &lt;SYN&gt; segment. 
不会，从上诉RFC原文可以看出是必须双方都支持Window Scale，才会启用
</div>2022-01-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1d/97/ad/cdb3c420.jpg" width="30px"><span>kakashi</span> 👍（2） 💬（1）<div>“一台机器最多65535个TCP连接”，确实让我懵逼了下，差点就着了你的道了哈哈，确实，一台机器有65535个端口，但不表示最多有65535个连接，连接数是按五元组定义的，一个五元组表示一个连接。不知道我理解的对不对(✿◡‿◡)</div>2022-05-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/57/4f/6fb51ff1.jpg" width="30px"><span>奕</span> 👍（2） 💬（2）<div>CentOS Linux release 7.6 , net.ipv4.tcp_syn_retries = 6  设置静默丢包，客户端重试的时候，发现尝试了 11次，前5次是每隔1s 后面几次就根据指数退避原则了，我这个环境为什么会多了 4次呢？</div>2022-01-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/21/b8/aca814dd.jpg" width="30px"><span>江山如画</span> 👍（2） 💬（2）<div>问题1:
因为 net.ipv4.tcp_syn_retries 是三次握手的 SYN 包的重试次数，猜测 net.ipv4.tcp_synack_retries 是 SYN+ACK 包的重试次数，在 centos 上看了下，这个值默认是2.

问题2:
在RFC1332的2.2节 Window Scale Option中有一段 &quot;Upon receiving a SYN segment with a Window Scale option containing shift.cnt = S, a TCP sets Snd.Wind.Scale to S and sets Rcv.Wind.Scale to R; otherwise, it sets both Snd.Wind.Scale and Rcv.Wind.Scale to zero.&quot;

所以当通信双方一方支持 windows scale, 另一方不支持时，再之后的通信中，发送窗口和接口窗口的缩放比例都是0，相当于双方的 Shift Count 的值都是0.</div>2022-01-17</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/PiajxSqBRaELTaqicWVpIsOpha9icy6LLJrrd24lGlwsBYhBTkBUdGHIGFXRbyZicNbSafvhMATDBjX6NSGLam9bag/132" width="30px"><span>懵懂的Java</span> 👍（1） 💬（1）<div>老师请教一下，我遇到 telnet，被瞬间远程服务器 close 的情况，是因为啥呢</div>2024-02-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/29/b4/a1/befed081.jpg" width="30px"><span>86</span> 👍（1） 💬（2）<div>老师，请教个问题，在服务器抓包，收到的SYN包TTL值是113，之后收到的客户端传过来的数据包的TTL值都是114。请问，为什么首次的TTL值会小。哪个TTL值是准确的。谢谢！</div>2023-12-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/4d/49/28e73b9c.jpg" width="30px"><span>明翼</span> 👍（1） 💬（1）<div>发送窗口大小扩展信息只能握手包发，那后面的发送窗口的变化只能改发送窗口的值而不是倍数对吗？</div>2023-09-22</li><br/><li><img src="" width="30px"><span>Geek_0d1ecd</span> 👍（1） 💬（2）<div>对我们7年运维，5年TAM静下心看还是收获满满，已经强推荐给伙伴，不介意加个微信，讨论下一个10年</div>2022-06-05</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/9f/a1/d75219ee.jpg" width="30px"><span>po</span> 👍（1） 💬（2）<div>对于redis的案例有几个疑问，1.原始的窗口65535字节不是已经满足308字节大小了吗？还需要用到Windows scale？2.为什么服务端是通知190字节呢？为什么不是240或者其他字节大小呢？</div>2022-03-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/38/5e/f0394817.jpg" width="30px"><span>费曼先生</span> 👍（1） 💬（1）<div>看的出来，老师写的专栏真的很用心，内容真的很充实，收获很多！！！</div>2022-02-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/b4/94/2796de72.jpg" width="30px"><span>追风筝的人</span> 👍（1） 💬（1）<div>1.第二次握手最大重传次数
tcp_synack_retries (integer; default: 5; since Linux 2.2)
              The maximum number of times a SYN&#47;ACK segment for a
              passive TCP connection will be retransmitted. This number
              should not be higher than 255.

2. 不会     both sides must support window Scale</div>2022-02-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/22/0f/f9/95d1537d.jpg" width="30px"><span>氢气球</span> 👍（1） 💬（1）<div>老师讲的真好，收益匪浅！</div>2022-01-18</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/PiajxSqBRaEKb69vx0T0Aaf1sc0rOqtHk3Zlk7A4RQG77v5EJ78xMiajTsgCyAnNHr0XhQ892eCnl29a0IcqyXbEVcWShR0S1TBibdG0utVgb072V6148ms1A/132" width="30px"><span>Geek_971427</span> 👍（0） 💬（1）<div>         This option is an offer, not a promise; both sides must send Window Scale options in their SYN segments to enable window scaling in either direction.  </div>2024-08-08</li><br/><li><img src="" width="30px"><span>Geek_c1ddab</span> 👍（0） 💬（1）<div>文中“sudo tcpdump -i any -w telnet-80-reject.pcap host 47.94.129.219 and port 80 ”这个过滤条件为什么没有抓到icmp包，icmp走的不是这个端口吗？</div>2024-07-26</li><br/><li><img src="" width="30px"><span>Geek_85d326</span> 👍（0） 💬（1）<div>老师  在实践中，发现Window Scale还是不太明白 例如:在客户端发送的握手SYN报文中 WS=256，也就是默认窗口值翻256倍，在接下来服务端回复的SYN,ACK报文中WS=1   那这个TCP流在后面的数据传输中窗口值最大为多少呢？是256倍还是原值？</div>2023-05-16</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/be/f5/e98a2199.jpg" width="30px"><span>稻香</span> 👍（0） 💬（1）<div>老师，你好。这里有点不太明白。根据四元祖，这句话是不是有点问题呢？
在限定场景下，一个客户端（假设只有一个出口 IP）和一个服务端（假设也只有一个 IP 和一个服务端口），那么确实只能最多发起 6 万多个连接。
这种情况，源端端口不是可以变化吗？端口变化后不就是一个新的连接吗？
</div>2023-02-06</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/17/18/e4382a8e.jpg" width="30px"><span>有识之士</span> 👍（0） 💬（1）<div>打开学习，迟到的学习，不晚。</div>2022-07-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/2a/29/ab/59a6e437.jpg" width="30px"><span>Kevin</span> 👍（0） 💬（1）<div>厉害了，瞬间感觉自己的网络底层知识翻倍了。谢谢老师的倾囊相授。</div>2022-05-06</li><br/><li><img src="" width="30px"><span>web</span> 👍（0） 💬（1）<div>感觉大佬对nc有很多误会，大佬可以用下centos下的nc，这样就可以避免很多误会了。：-）</div>2022-04-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/11/e5/ebd56b05.jpg" width="30px"><span>晓波</span> 👍（0） 💬（2）<div>iptables 限制80端口 reject 【-A INPUT -p tcp -m tcp --dport 80 -j REJECT --reject-with icmp-port-unreachable】
没生效
服务端是按照drop方式处理的
默认不加iptables规则，是按照REJECT --reject-with tcp-reset 方式处理的

是不是还有其他什么地方的规则起作用了</div>2022-03-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1f/52/5c/d4a9accb.jpg" width="30px"><span>仄言</span> 👍（0） 💬（1）<div>静默丢包 可能还会涉及到 应用层面的队列打满</div>2022-03-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/c4/03/f753fda7.jpg" width="30px"><span>JianXu</span> 👍（0） 💬（1）<div>杨老师，那个Redis 的例子没有理解，实际上并没有问题对吗？只是Tcpdump 是在链接建立以后发起的，所以看不到一开始的window scale 导致显示有问题？而后面给的SYNC 里面看到window scale 是另一个链接？</div>2022-03-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/27/59/f0/09b50521.jpg" width="30px"><span>1000AP大德玛</span> 👍（0） 💬（3）<div>一台机器最多 65535 个 TCP 连接
所以如果是作为客户端（单个IP）理论上最大连接数就是65535 个，比如Nginx作为客户端（反向代理），理论上的反向代理的最大连接数65535 个？</div>2022-03-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/26/b1/cc902a24.jpg" width="30px"><span>三三</span> 👍（0） 💬（1）<div>思考题依回不知道，同志还需努力</div>2022-03-01</li><br/>
</ul>