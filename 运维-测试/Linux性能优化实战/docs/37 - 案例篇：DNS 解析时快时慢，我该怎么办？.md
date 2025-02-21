你好，我是倪朋飞。

上一节，我带你一起学习了网络性能的评估方法。简单回顾一下，Linux 网络基于 TCP/IP 协议栈构建，而在协议栈的不同层，我们所关注的网络性能也不尽相同。

在应用层，我们关注的是应用程序的并发连接数、每秒请求数、处理延迟、错误数等，可以使用 wrk、JMeter 等工具，模拟用户的负载，得到想要的测试结果。

而在传输层，我们关注的是 TCP、UDP 等传输层协议的工作状况，比如 TCP 连接数、 TCP 重传、TCP 错误数等。此时，你可以使用 iperf、netperf 等，来测试 TCP 或 UDP 的性能。

再向下到网络层，我们关注的则是网络包的处理能力，即 PPS。Linux 内核自带的 pktgen，就可以帮你测试这个指标。

由于低层协议是高层协议的基础，所以一般情况下，我们所说的网络优化，实际上包含了整个网络协议栈的所有层的优化。当然，性能要求不同，具体需要优化的位置和目标并不完全相同。

前面在评估网络性能（比如 HTTP 性能）时，我们在测试工具中指定了网络服务的 IP 地址。IP 地址是 TCP/IP 协议中，用来确定通信双方的一个重要标识。每个 IP 地址又包括了主机号和网络号两部分。相同网络号的主机组成一个子网；不同子网再通过路由器连接，组成一个庞大的网络。
<div><strong>精选留言（30）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/13/60/71/895ee6cf.jpg" width="30px"><span>分清云淡</span> 👍（43） 💬（9）<div>nslookup 域名结果正确，但是 ping 域名 返回 unknown host, 让我挖出一大把相关的基础知识，一下子就把dns这块通关了：https:&#47;&#47;plantegg.github.io&#47;2019&#47;01&#47;09&#47;nslookup-OK-but-ping-fail&#47;</div>2019-03-01</li><br/><li><img src="https://wx.qlogo.cn/mmopen/vi_32/PiajxSqBRaEKQMM4m7NHuicr55aRiblTSEWIYe0QqbpyHweaoAbG7j2v7UUElqqeP3Ihrm3UfDPDRb1Hv8LvPwXqA/132" width="30px"><span>ninuxer</span> 👍（21） 💬（1）<div>打卡day39
碰到dns问题最多的就是劫持，现在公网都是强制https，内部用powerdns，性能刚刚的～</div>2019-02-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/e0/99/5d603697.jpg" width="30px"><span>MJ</span> 👍（14） 💬（1）<div>centos 7  dnsmasq如下操作：

cat &#47;etc&#47;resolv.conf
nameserver 114.114.114.114

yum -y install dnsmasq
systemctl start dnsmasq

测试dns缓存，要测试查询速度，请访问一个 dnsmasq 启动后没有访问过的网站，执行：
[root@node ~]# dig archlinux.org | grep &quot;Query time&quot;
;; Query time: 212 msec
[root@node ~]# dig archlinux.org | grep &quot;Query time&quot;
;; Query time: 2 msec
再次运行命令，因为使用了缓存，查询时间应该大大缩短。

老师，这种情况也是可以的吧。（针对上一个问题的解释）
</div>2019-03-06</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/58/c7/a65f5080.jpg" width="30px"><span>Lucky  Guy</span> 👍（8） 💬（2）<div>老师关于 DNS污染 有什么好的解决方案么?</div>2019-07-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/41/af/4307867a.jpg" width="30px"><span>JJj</span> 👍（7） 💬（1）<div>你好，请问下dns缓存dnsmasq的配置里面是否还要设置DNS服务器地址，比如8.8.8.8或114.114.114.114

</div>2019-07-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/93/89/f3b28216.jpg" width="30px"><span>慢热怪友</span> 👍（5） 💬（2）<div>既然域名以分层的结构进行管理，相对应的，域名解析其实也是用递归的方式（从顶级开始，以此类推），发送给每个层级的域名服务器，直到得到解析结果。
这里描述不恰当，老师漏讲了递归查询和迭代查询：
（1）递归查询
递归查询是一种DNS 服务器的查询模式，在该模式下DNS 服务器接收到客户机请求，必须使用一个准确的查询结果回复客户机。如果DNS 服务器本地没有存储查询DNS 信息，那么该服务器会询问其他服务器，并将返回的查询结果提交给客户机。所以，一般情况下服务器跟内网DNS 或直接 dns 之间都采用递归查询。
（2）迭代查询
DNS 服务器另外一种查询方式为迭代查询，DNS 服务器会向客户机提供其他能够解析查询请求的DNS 服务器地址，当客户机发送查询请求时，DNS 服务器并不直接回复查询结果，而是告诉客户机另一台DNS 服务器地址，客户机再向这台DNS 服务器提交请求，依次循环直到返回查询的结果。所以一般内网 dns 和外网 dns 之间的都采用迭代查询。
</div>2020-08-05</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/57/6e/b6795c44.jpg" width="30px"><span>夜空中最亮的星</span> 👍（4） 💬（1）<div>会有DNS域名劫持的内容吗？</div>2019-02-15</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/a0/39/ddcf26ac.jpg" width="30px"><span>bruceding</span> 👍（3） 💬（1）<div>遇到过 GO client 解析 dns 的问题，也是做了折中，配置 &#47;etc&#47;resolv.conf  多个 name server 解决，GO DNS 解析流程可以参考： http:&#47;&#47;blog.bruceding.com&#47;516.html</div>2019-02-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/25/66/4835d92e.jpg" width="30px"><span>潘政宇</span> 👍（2） 💬（1）<div>ping一个IP的时候，140ms就算延迟很大了，一般多少毫秒算正常？</div>2019-02-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/5b/ae/3d639ea4.jpg" width="30px"><span>佳</span> 👍（2） 💬（1）<div>还需要故意，linux,ping过程域名解析，还有一个方向解析过程，内网解析器，目前使用coredns做内网的域名解析器的时候，使用etcd插件时候需要配置方向解析配置，否则ping时候，会把反向解析发送外网上游dns,出现超时，</div>2019-02-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/58/42/abb7bfe3.jpg" width="30px"><span>eric-xin</span> 👍（1） 💬（1）<div>之前我配置内部DNS时候发现解析腾讯的地址有问题，后来把请求腾讯接口的zone换成了 119.29.29.29dns 超时就好了，默认dns 超时时间是30秒，简直要命</div>2019-07-04</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/e9/e9/1f95e422.jpg" width="30px"><span>杨陆伟</span> 👍（1） 💬（1）<div>请教下，为什么多次nslookup的时延没有提升？dns服务器本身不是可以缓存吗？</div>2019-06-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/e0/99/5d603697.jpg" width="30px"><span>MJ</span> 👍（1） 💬（1）<div>echo nameserver 127.0.0.1 &gt; &#47;etc&#47;resolv.conf

老师，这个需要配置吗？配置后就解析不了吧
dnsmasq默认会从&#47;etc&#47;resolv.conf读取文件，读取114.114.114.114.</div>2019-03-06</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/2f/f4/2dede51a.jpg" width="30px"><span>小老鼠</span> 👍（1） 💬（1）<div>1）
root@ubuntu:&#47;usr&#47;sbin# dig +trace +nodnssec time.geekbang.org

; &lt;&lt;&gt;&gt; DiG 9.11.3-1ubuntu1.2-Ubuntu &lt;&lt;&gt;&gt; +trace +nodnssec time.geekbang.org
;; global options: +cmd
;; Received 28 bytes from 127.0.0.53#53(127.0.0.53) in 0 ms
为什么只显示这些信息

2）
root@ubuntu:&#47;usr&#47;sbin# whereis  dnsmasq 
dnsmasq: &#47;usr&#47;sbin&#47;dnsmasq &#47;usr&#47;share&#47;man&#47;man8&#47;dnsmasq.8.gz
root@ubuntu:&#47;usr&#47;sbin# &#47;usr&#47;sbin&#47;dnsmasq start

dnsmasq: junk found in command line
如何解决</div>2019-02-16</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/53/af/0e3ddb1d.jpg" width="30px"><span>SunnyBird</span> 👍（1） 💬（1）<div>请教一下 如果在使用 http 的时候 直接使用 IP 地址 而不是 域名 是不是可以减少 dns 查询时间？</div>2019-02-16</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/1b/ca/9afb89a2.jpg" width="30px"><span>Days</span> 👍（1） 💬（1）<div>总结：对DNS工作流程做了总结，感觉比较基础，后期是否可以深度讲解？</div>2019-02-15</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/9a/64/ad837224.jpg" width="30px"><span>Christmas</span> 👍（0） 💬（1）<div>配置了缓存的情况下，dig和nslookup有一个是可以不走缓存的。</div>2019-02-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/2e/72/145c10db.jpg" width="30px"><span>每日都想上班</span> 👍（0） 💬（1）<div>nslookup 前面加time 可以出现耗时是用nslooktime 本身的机制吗？我想在windows中time nslookup查看发现不行？</div>2019-02-17</li><br/><li><img src="" width="30px"><span>fran712</span> 👍（0） 💬（1）<div>使用nscd做客户端缓存也可以吧？</div>2019-02-16</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/64/05/6989dce6.jpg" width="30px"><span>我来也</span> 👍（0） 💬（1）<div>[D37打卡]
做移动端开发时,确实会经常遇到域名劫持的情况.
不过当时的做法都是替换http为https. ws替换为wss.
今天算是见识了,还可以用 HTTPDNS.

平常服务器端的dns解析问题好排查和处理,客户端的就麻烦多了.只能让客户端绕过一些已知的坑,或者提供备选方案.</div>2019-02-15</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/20/1d/0c1a184c.jpg" width="30px"><span>罗辑思维</span> 👍（13） 💬（0）<div>今天课程比较熟悉，但是收获非常大。
1. 两个命令的使用场景：nslookup -debug、time nslookup。
2. 理解性能分析的思路：性能分析和优化要做到可视化，可量化。比如DNS查询慢，多少延迟算慢？有什么命令可以观察指标？又有什么命令可以观察DNS解析的过程？
现在开始明白老师给我们灌输的性能分析思路。
以前个人DNS排查顺序都是这三把斧：
1. 检查本地hosts：cat &#47;etc&#47;hosts
2.检查resolv.conf文件：cat &#47;etc&#47;resolv.conf。在redhat7&#47;centos7上修改resolv.conf里的DNS地址后，重启启网络服务发现DNS地址消失了，那么检查下网卡配置文件。
3. 检查网卡配置文件： cat &#47;etc&#47;sysconfig&#47;network-scripts&#47;ifcfg-&lt;网卡名称&gt;，看下里头有没DNS配置信息，没有的话补上去。</div>2020-03-05</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/65/30/74fcbb4b.jpg" width="30px"><span>单行道</span> 👍（6） 💬（0）<div>大牛啥时候把这个系列出版纸质书，收藏</div>2019-04-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/12/f9/7e6e3ac6.jpg" width="30px"><span>Geek_04e22a</span> 👍（4） 💬（0）<div>DNS解析分为两部分，服务器到本地DNS服务器是递归，本地服务器到域名解析服务器是迭代的方式</div>2020-09-01</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/2b/7b/9c/5d1dcda5.jpg" width="30px"><span>Runner91</span> 👍（2） 💬（0）<div>曾经排查一个api接口时快时慢的问题使用了这个python脚本https:&#47;&#47;github.com&#47;reorx&#47;httpstat，能够清晰显示http各阶段的耗时，锁定到了dns问题后，对比&#47;etc&#47;resolv.conf发现某些dns ip过期了，修改后，又可以愉快的摸鱼了</div>2021-12-05</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/c0/ce/fc41ad5e.jpg" width="30px"><span>陳先森</span> 👍（2） 💬（0）<div>很有收获，感谢作者···这个专栏还是很让我涨知识~~~修炼不能一口吃成一个大胖子得自己慢慢去消化，专栏知识点有点多。有点基础，看起来虽然不太费力，但是要完全掌握还是要多学几遍温故而知新才行，还多敲，多练，多记（基础知识）才能消化知识点。</div>2019-04-27</li><br/><li><img src="" width="30px"><span>如果</span> 👍（2） 💬（0）<div>DAY37,打卡</div>2019-04-01</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/dd/5b/5461afad.jpg" width="30px"><span>Wen</span> 👍（1） 💬（0）<div>1、 两个命令的使用场景：nslookup --debug、time nslookup。安装：yum install -y bind-utils

2、DNS查询顺序：
1）检查本地hosts：cat &#47;etc&#47;hosts
2）检查 &#47;etc&#47;resolv.conf，临时生效，永久生效需配置网卡。

3、DNS优化思路：
1）更换延迟更小的DNS服务器，比如电信的dns：114.114.114.114
2）开启DNS缓存，比如dnsmasq，安装和开启：yum install -y dnsmasq;systemctl enable dnsmasq

</div>2020-09-30</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/Q3auHgzwzM78picDmK4b2roBGAqoLicqc5EPPbsPQWkb3xbMk6kDpft19DgeLEfBeekPlvFg2O5lrEXa0XdYhhng/132" width="30px"><span>Geek_e2b7bc</span> 👍（0） 💬（0）<div>docker镜像站全挂时代。拉不到学习镜像了
</div>2025-01-04</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1e/d1/49/791d0f5e.jpg" width="30px"><span>aake</span> 👍（0） 💬（0）<div>为啥 man nslookup 没有看到 -debug 这个选项 ？</div>2023-12-07</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/7a/62/9b248708.jpg" width="30px"><span>阿硕</span> 👍（0） 💬（0）<div>win环境， 客户端配置2个dns服务器，一个dns仅提供内部解析，一个公网dns提供外部，不同系统表现不同，win解析有时候出现内部不能解析，需要的多次刷新，mac上正常，关于dns解析地址的逻辑关系是什么呢？</div>2023-04-12</li><br/>
</ul>