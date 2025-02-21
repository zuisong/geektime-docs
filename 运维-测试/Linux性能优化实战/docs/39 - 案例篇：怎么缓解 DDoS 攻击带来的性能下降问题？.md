你好，我是倪朋飞。

上一节，我带你学习了tcpdump 和 Wireshark 的使用方法，并通过几个案例，带你用这两个工具实际分析了网络的收发过程。碰到网络性能问题，不要忘记可以用 tcpdump 和 Wireshark 这两个大杀器，抓取实际传输的网络包，排查潜在的性能问题。

今天，我们一起来看另外一个问题，怎么缓解 DDoS（Distributed Denial of Service）带来的性能下降问题。

## DDoS 简介

DDoS 的前身是 DoS（Denail of Service），即拒绝服务攻击，指利用大量的合理请求，来占用过多的目标资源，从而使目标服务无法响应正常请求。

DDoS（Distributed Denial of Service） 则是在 DoS 的基础上，采用了分布式架构，利用多台主机同时攻击目标主机。这样，即使目标服务部署了网络防御设备，面对大量网络请求时，还是无力应对。

比如，目前已知的最大流量攻击，正是去年 Github 遭受的 [DDoS 攻击](https://githubengineering.com/ddos-incident-report/)，其峰值流量已经达到了 1.35Tbps，PPS 更是超过了 1.2 亿（126.9 million）。

从攻击的原理上来看，DDoS 可以分为下面几种类型。

第一种，耗尽带宽。无论是服务器还是路由器、交换机等网络设备，带宽都有固定的上限。带宽耗尽后，就会发生网络拥堵，从而无法传输其他正常的网络报文。
<div><strong>精选留言（30）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/10/5c/cb/3ebdcc49.jpg" width="30px"><span>怀特</span> 👍（29） 💬（3）<div>这个专栏太超值，我跟追剧一样的追到现在，收获已经巨大！
谢谢倪工的分享。
更谢谢倪工对留言一丝不苟的回复---这份对听众的耐心，其他专栏的作者没有一个能比得上的。
继续追剧！</div>2019-02-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/92/e3/1be13204.jpg" width="30px"><span>ichiro</span> 👍（15） 💬（2）<div>最近服务会出现干核现象，一个单进程程序发现把一个cpu耗尽，用top发现一个cpu的，软中断很高，通过watch -d cat &#47;proc&#47;softireq，发现网络中断很高，然后配置多网卡队列，把中断分散到是他cpu，缓解了进程cpu的压力，但同时带来担忧，配置多网卡队列绑定，会不会带来cpu切换，缓存失效等负面影响？另外，老师还有别的建议吗？</div>2019-02-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/cb/88/f9ae7bc9.jpg" width="30px"><span>李燕平</span> 👍（13） 💬（1）<div>服务器插上网线就像开车上路。

DDoS攻击可以理解为撞车，提升汽车本身的安全系数会有用。
大量DDoS攻击可以理解为撞上大货车，需要护卫车队来保护主车。
</div>2019-02-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/4d/49/28e73b9c.jpg" width="30px"><span>明翼</span> 👍（11） 💬（1）<div>检测DDOS攻击，我没有什么这方面经验想了下：
1、既然攻击，肯定不是正常业务，所以在sar -n DEV 4 命令看运行包的时候，不光要注意收到的包的大小，还要注意平时在监控业务的时候观察正常的业务的收包量，做一个横向比较，确定异常流量；还有一点特别重要，我觉得tcp连接交互基本都是双向的，那么回包数量和发包的数量不能相差太大，如果太大了可能有问题。

2、至于查看源IP，除了tcpdump外，是不是可以通过netstat 结合wc 统计下各类状态的连接数，如果连接数超过平时的连接数就要注意，关注状态一致的连接数，这里面也有ip信息，当然也可以判断来源。
</div>2019-02-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/8c/9c/d48473ab.jpg" width="30px"><span>dancer</span> 👍（8） 💬（1）<div>重新开追，前两天着重看了cpu调优，正好线上压测发现了cpu.user飙高的问题，通过perf和pprof查明了是一个复杂json结构解析导致的，学以致用下来印象更深了！这两天开始看网络，后面再看io和内存相关，感谢！</div>2019-03-06</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/60/05/3797d774.jpg" width="30px"><span>forever</span> 👍（7） 💬（1）<div>我之前在生产环境中遇到过多次ddos攻击，最好的被打到55G.最初的时候遇到攻击束手无策，还被人勒索过，说给钱就不攻击！哈哈😄因为没经验，后来就打游击战，那时候攻击的是我们负载均衡的ip，当攻击发生时我就换ip这样能暂时缓解，当然提前要把ip给准备好，比如白名单添加等！后来业务壮大，换ip的时间成本比网站不能访问的成本要高，最后我们用了阿里云的高防，就这样攻击就告一段落了！虽然高防很贵，但是比起被攻击的损失，还是值得的！</div>2019-02-25</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/05/7f/a7df049a.jpg" width="30px"><span>Standly</span> 👍（6） 💬（1）<div>请问老师今天讲的三个tcp内核参数调优能否作为通用的提高服务器抗并发能力的优化手段？</div>2019-04-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/8c/2b/3ab96998.jpg" width="30px"><span>青石</span> 👍（6） 💬（1）<div>REJECT攻击IP所有报文，接口响应没什么变化，还是127秒，DROP报文后响应时间才恢复正常，查了REJECT和DROP的区别，REJECT会返回个ICMP包给源IP，有点不太理解为什么一个ICMP包导致这么大的差异。

# hping3命令, u10效果不明显，所以改成了u1测试
$ hping3 -S -p 80  172.30.81.136 -I eno1 -i u1

# 调整内核参数测试结果，接口响应时间为127秒
$ curl -s -w &#39;Http code: %{http_code}\nTotal time:%{time_total}s\n&#39; -o &#47;dev&#47;null http:&#47;&#47;172.30.81.136&#47; 
Http code: 000
Total time:127.109s

# 调整内核参数、iptables限制syn并发的测试结果，接口响应时间为127秒
$ curl -s -w &#39;Http code: %{http_code}\nTotal time:%{time_total}s\n&#39; -o &#47;dev&#47;null http:&#47;&#47;172.30.81.136&#47; 
Http code: 000
Total time:127.106s

# 调整内核参数、iptables限制syn并发、单IP连接数的测试结果，接口响应时间为127秒
$ curl -s -w &#39;Http code: %{http_code}\nTotal time:%{time_total}s\n&#39; -o &#47;dev&#47;null http:&#47;&#47;172.30.81.136&#47; 
Http code: 000
Total time:127.097s

# 调整内核参数、iptables限制syn并发、单IP连接数、DROP攻击IP所有报文的测试结果，接口响应时间为127秒
$ curl -s -w &#39;Http code: %{http_code}\nTotal time:%{time_total}s\n&#39; -o &#47;dev&#47;null http:&#47;&#47;172.30.81.136&#47; 
Http code: 200
Total time:0.001s</div>2019-03-17</li><br/><li><img src="https://wx.qlogo.cn/mmopen/vi_32/PiajxSqBRaEKQMM4m7NHuicr55aRiblTSEWIYe0QqbpyHweaoAbG7j2v7UUElqqeP3Ihrm3UfDPDRb1Hv8LvPwXqA/132" width="30px"><span>ninuxer</span> 👍（4） 💬（1）<div>打卡day42
真正的ddos要靠运营商的流量清洗之类的了</div>2019-02-25</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/a0/2d/2fee2d83.jpg" width="30px"><span>且听风吟</span> 👍（3） 💬（1）<div>net.ipv4.tcp_max_tw_buckets 
net.ipv4.tcp_tw_reuse 
net.ipv4.tcp_tw_recycle
net.ipv4.tcp_keepalive_time 
net.ipv4.tcp_timestamps
期待结合生产环境对这几个内核参数的讲解。目前生产环境下php服务器time_wait特别多，网络包的流程：  NGINX代理&lt;——&gt;PHP服务器——&gt;redis&#47;mysql.. 
高峰时期php服务器一共50k+的连接。49k+的time_wait.， 主要来源是php作为客户端的角色时连接redis、mysql、给代理NGINX回包、php服务器内部调用。希望老师能给解决问题的思路。
</div>2019-02-20</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/oCx7GX9P4w5cml1cpbFD1x21Biad3MLCTOhTPJvicRW3xp9C8xTgdiaOSdpFyvibKSfcD1LL4miaT7VtqqKms6rgujg/132" width="30px"><span>zshanjun</span> 👍（2） 💬（2）<div>我这里dos攻击没有什么效果，我查看了一下被攻击主机的tcp连接状态发现根本就没有多少SYN_REC的状态。
然后通过抓包发现，是攻击主机主动发了【R】，导致被攻击主机的tcp的SYN_REC没有堆积起来：
06:38:15.452913 IP 192.168.38.4.15651 &gt; 192.168.38.5.80: Flags [S], seq 1206198085, win 512, length 0
06:38:15.452930 IP 192.168.38.5.80 &gt; 192.168.38.4.15651: Flags [S.], seq 1729577211, ack 1206198086, win 29200, options [mss 1460], length 0
06:38:15.453009 IP 192.168.38.4.15652 &gt; 192.168.38.5.80: Flags [S], seq 1185838297, win 512, length 0
06:38:15.453033 IP 192.168.38.5.80 &gt; 192.168.38.4.15652: Flags [S.], seq 1389286866, ack 1185838298, win 29200, options [mss 1460], length 0
06:38:15.453132 IP 192.168.38.4.15651 &gt; 192.168.38.5.80: Flags [R], seq 1206198086, win 0, length 0
06:38:15.453141 IP 192.168.38.4.15652 &gt; 192.168.38.5.80: Flags [R], seq 1185838298, win 0, length 0
06:38:15.453384 IP 192.168.38.4.15653 &gt; 192.168.38.5.80: Flags [S], seq 1851454908, win 512, length 0
06:38:15.453406 IP 192.168.38.5.80 &gt; 192.168.38.4.15653: Flags [S.], seq 128486955, ack 1851454909, win 29200, options [mss 1460], length 0
06:38:15.453479 IP 192.168.38.4.15653 &gt; 192.168.38.5.80: Flags [R], seq 1851454909, win 0, length 0
06:38:15.453719 IP 192.168.38.4.15654 &gt; 192.168.38.5.80: Flags [S], seq 700664781, win 512, length 0
06:38:15.453743 IP 192.168.38.5.80 &gt; 192.168.38.4.15654: Flags [S.], seq 3877145682, ack 700664782, win 29200, options [mss 1460], length 0
06:38:15.454017 IP 192.168.38.4.15654 &gt; 192.168.38.5.80: Flags [R], seq 700664782, win 0, length 0
06:38:15.454961 IP 192.168.38.4.15655 &gt; 192.168.38.5.80: Flags [S], seq 1751493720, win 512, length 0
06:38:15.454993 IP 192.168.38.5.80 &gt; 192.168.38.4.15655: Flags [S.], seq 1257904630, ack 1751493721, win 29200, options [mss 1460], length 0

请问这种情况是hping3工具的问题吗？</div>2019-04-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/9a/64/ad837224.jpg" width="30px"><span>Christmas</span> 👍（2） 💬（1）<div>Sysc backlog并不是在配置了sync cookie之后就失效了吧，netstat -s 看到的listen状态的recv 和send不是分别表示连接队列配置和当前活跃队列长度吗，比如监听某个端口的进程不响应了，那么这里的recv队列就会慢慢变长然后溢出。溢出之后，linux可以选择drop掉什么也不做，或者返回connection reset通知客户端</div>2019-03-01</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/cf/5c/d4e19eb6.jpg" width="30px"><span>安小依</span> 👍（2） 💬（1）<div>随机化源 IP 和 多台机器分布式攻击 有什么区别，为什么限制 syn 包速率的方式不适用于多台机器分布式的</div>2019-02-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/57/6e/b6795c44.jpg" width="30px"><span>夜空中最亮的星</span> 👍（2） 💬（1）<div>谷歌的QUIC 协议对 DDoS 有好的应对办法了吗，对QUIC 协议理解的不是很透彻，请老师赐教</div>2019-02-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/93/43/0e84492d.jpg" width="30px"><span>Maxwell</span> 👍（1） 💬（1）<div>压测过程中，使用多线程向服务器施压，也算是DDOS攻击吧？</div>2019-03-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/f7/b1/982ea185.jpg" width="30px"><span>美妙的代码</span> 👍（1） 💬（1）<div>老师，如果把tcp 改为sctp 协议，是不是就不会再发生DDos 攻击了？</div>2019-03-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/12/04/5837b21c.jpg" width="30px"><span>Brown羊羊</span> 👍（0） 💬（1）<div>net.ipv4.tcp_max_syn_backlog = 256 改成1024 这个对DDoS攻击无效吧，也不差这几百个连接</div>2019-03-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/0f/85/0fa6f80f.jpg" width="30px"><span>wj</span> 👍（0） 💬（1）<div>我也按上面的情况去模拟了，但是没有达到能够把服务器刷死的那种效果，请求时间没什么变化</div>2019-03-06</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTL9hlAIKQ1sGDu16oWLOHyCSicr18XibygQSMLMjuDvKk73deDlH9aMphFsj41WYJh121aniaqBLiaMNg/132" width="30px"><span>腾达</span> 👍（0） 💬（1）<div>使用iptables过滤包，并不能使的ksoftirq&#47;0,还有softirq里的Net_Rx降低，是这样吗？</div>2019-02-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/64/05/6989dce6.jpg" width="30px"><span>我来也</span> 👍（0） 💬（3）<div>[D39打卡]
老师留的课后思考题,回答不上来.😂

目前因为都是云服务器,云服务商一般都会主动推送这些被攻击的风险信息.
之前工作中确实遇到过Ddos攻击.基本上都是云服务器把云主机的ip加入黑名单,封禁30分钟.
由于攻击流量很大,一个云主机IP在很短的时间里(一分钟左右吧),就被封禁了.
后来虽然购买了高防IP,据说一天防护能力几百G,但是也不经用.

如果不是局域网中有其他入口,连机器都登不上去.
等发现时,机器的公网已经被切断,也看不到有用的信息了.</div>2019-02-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/4a/15/106eaaa8.jpg" width="30px"><span>stackWarn</span> 👍（22） 💬（2）<div>讲的很不错。补充一点，半连接状态不只这一个参数net.ipv4.tcp_max_syn_backlog 控制，实际是 这个，还有系统somaxcon，以及应用程序的backlog，三个一起控制的。具体可以看下相关的源码</div>2020-05-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1d/3f/0d/1e8dbb2c.jpg" width="30px"><span>怀揣梦想的学渣</span> 👍（10） 💬（5）<div>我观摩过我所在城市的部分学校以及部分教育部门网站的DDOS防护，他们的方案是单个IP发来访问请求，会自动跳转到一个检测的界面，如果这个IP无正常互动响应，直接拉黑1个月，如果想解封，需要自己实名认证发邮件到教育部门的咨询邮箱申请。这个办法是真的挺神奇的。有些好奇，逻辑上外层加了一些防火墙或者防护设备，那内部的服务器还需要配置网络防护的策略吗。</div>2020-04-06</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/dd/5b/5461afad.jpg" width="30px"><span>Wen</span> 👍（4） 💬（0）<div>DDoS简介
DDoS（Distributied）的前身是DoS（Denail of Service），即拒绝服务攻击，指利用大量的合理请求，来占用过多的目标资源，从而使目标服务无法响应正常的请求。
DDos在Dos的基础上，采用了分布式架构，利用多台主机同时攻击目标主机。
DDoS有以下三种类型：
a、耗尽宽带。
b、消耗操作系统的资源。
c、消耗应用程序的运行资源。

DoS实验模拟：
VM1终端一：开启web服务
 docker run -itd --name=nginx --network=host nginx
VM2终端一：对比被攻击前后的web访问时间：
curl -s -w &#39;Http code: %{http_code}\nTotal time:%{time_total}s\n&#39; -o &#47;dev&#47;null http:&#47;&#47;10.10.10.2&#47;
VM2终端二：模拟Dos攻击
hping3 -S -p 80 -i U10 --flood 10.10.10.2
VM1终端二：查看网络接收包情况
sar -n DEV 1
VM1终端三：tcpdump抓包
tcpdump -i eth0 -n tcp port 80
VM1终端4：统计SYN_REC连接数
netstat -n -p | grep SYN_REC | wc -l


解决Dos攻击：
防火墙方法1：拒绝源ip访问
iptables -I INPUT -s 10.10.10.4 -p tcp -j REJECT
防火墙方法2：限制 syn 包的速率
# 限制syn并发数为每秒1次
$ iptables -A INPUT -p tcp --syn -m limit --limit 1&#47;s -j ACCEPT
# 限制单个IP在60秒新建立的连接数为10
$ iptables -I INPUT -p tcp --dport 80 --syn -m recent --name SYN_FLOOD --update --seconds 60 --hitcount 10 -j REJECT
优化系统内核TCP参数
方法1：增大syn连接数
$ sysctl net.ipv4.tcp_max_syn_backlog
net.ipv4.tcp_max_syn_backlog = 256
$ sysctl -w net.ipv4.tcp_max_syn_backlog=1024
net.ipv4.tcp_max_syn_backlog = 1024
方法2：减少SYN_REVC重试次数为1，默认是5
$ sysctl -w net.ipv4.tcp_synack_retries=1
net.ipv4.tcp_synack_retries = 1
方法3：开启TCP SYN Cookies
注意：开启 TCP syncookies 后，内核选项 net.ipv4.tcp_max_syn_backlog 也就无效了。
$ sysctl -w net.ipv4.tcp_syncookies=1
net.ipv4.tcp_syncookies = 1

永久生效方式：写入 &#47;etc&#47;sysctl.conf 文件中：
$ cat &#47;etc&#47;sysctl.conf
net.ipv4.tcp_syncookies = 1
net.ipv4.tcp_synack_retries = 1
net.ipv4.tcp_max_syn_backlog = 1024
 sysctl -p




</div>2020-10-02</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/18/de/ab/e87f0e5e.jpg" width="30px"><span>spike</span> 👍（3） 💬（0）<div>用了hping3 -S -p 80 -i u1 192.168.0.30把公司内网打炸了。。。感谢老师。。认识到了syn泛洪的威力。。</div>2022-07-01</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/3a/6e/e39e90ca.jpg" width="30px"><span>大坏狐狸</span> 👍（2） 💬（0）<div>1 增大队列SYN最大半连接数sysctl -w et.ipv4.tcp_max_syn_backlog=3000
2 减少超时值：通过减少超时重传次数，sysctl -w net.ipv4.tcp_synack_retries=1
3 SYN_COOKIE : 开启cookie echo &quot;1&quot; &gt; &#47; proc&#47;sys&#47;net&#47;ipv4&#47;tcp_syncookies （原本对cookie有误解，看了本文才清楚，谢谢老师）
4 过滤可疑IP地址:  iptables -I INPUT -s 192.168.0.2 -p tcp -j REJECT  禁止 0.2访问
</div>2019-04-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/19/11/0e/23d6a88f.jpg" width="30px"><span>Shuai</span> 👍（1） 💬（0）<div>到服务器的网络如果比喻成车道的话，感觉dos攻击像是恶意阻塞车道的车辆，耗尽带宽、耗尽操作系统的资源、消耗应用程序的运行资源分别相当于主车道被阻塞、服务器家附近的路被阻塞、服务器家门口的停车场被阻塞，导致真正属于服务器的车开不到家门口；
于是防治策略一个是 家门口的停车场加上管控，家门口附近的路加上管控，在主干道之前加上WAF、CDN等流量管控，让恶意的车辆进入主干道之前就被过滤掉。</div>2022-05-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/c3/d1/bdf895bf.jpg" width="30px"><span>penng</span> 👍（0） 💬（0）<div>老师好，配置了sync cookie之后，Sys backlog就失掉了？之前有看到backlog还是有效的，在backlog队列以内，还是会正常的响应，超过backlog之后，内核才使用sync cookie的特性，希望老师解读一下，当然，开启sync cookie后，可以理解为半队列无限大。</div>2023-10-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/21/5f/f8/1d16434b.jpg" width="30px"><span>陈麒文</span> 👍（0） 💬（0）<div>坚持看到这，脑袋瓜有个映像，多个思考的方向</div>2021-08-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/f6/24/547439f1.jpg" width="30px"><span>ghostwritten</span> 👍（0） 💬（0）<div>1. DDoS 类型:耗尽带宽、耗尽操作系统的资源、消耗应用程序的运行资源
2. curl -s -w &#39;Http code: %{http_code}\nTotal time:%{time_total}s\n&#39; -o &#47;dev&#47;null http:&#47;&#47;192.168.0.30&#47;
curl -w &#39;Http code: %{http_code}\nTotal time:%{time_total}s\n&#39; -o &#47;dev&#47;null --connect-timeout 10 http:&#47;&#47;192.168.0.30
3. hping3 -S -p 80 -i u10 192.168.0.30
4. sar -n DEV 1
5. tcpdump -i eth0 -n tcp port 80
6. netstat -n -p | grep SYN_REC
7. iptables -I INPUT -s 192.168.0.2 -p tcp -j REJECT
8. iptables -A INPUT -p tcp --syn -m limit --limit 1&#47;s -j ACCEPT
9. iptables -I INPUT -p tcp --dport 80 --syn -m recent --name SYN_FLOOD --update --seconds 60 --hitcount 10 -j REJECT
10. sysctl net.ipv4.tcp_max_syn_backlog
sysctl -w net.ipv4.tcp_max_syn_backlog=1024
sysctl -w net.ipv4.tcp_synack_retries=1
sysctl -w net.ipv4.tcp_syncookies=1</div>2021-08-03</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/20/34/fe/e5429b02.jpg" width="30px"><span>glimmer</span> 👍（0） 💬（0）<div>nginx backlog默认为512</div>2021-04-12</li><br/>
</ul>