你好，我是倪朋飞。

上一节，我们探究了网络延迟增大问题的分析方法，并通过一个案例，掌握了如何用 hping3、tcpdump、Wireshark、strace 等工具，来排查和定位问题的根源。

简单回顾一下，网络延迟是最核心的网络性能指标。由于网络传输、网络包处理等各种因素的影响，网络延迟不可避免。但过大的网络延迟，会直接影响用户的体验。

所以，在发现网络延迟增大的情况后，你可以先从路由、网络包的收发、网络包的处理，再到应用程序等，从各个层级分析网络延迟，等到找出网络延迟的来源层级后，再深入定位瓶颈所在。

今天，我再带你来看看，另一个可能导致网络延迟的因素，即网络地址转换（Network Address Translation），缩写为 NAT。

接下来，我们先来学习 NAT 的工作原理，并弄清楚如何优化 NAT 带来的潜在性能问题。

## NAT原理

NAT 技术可以重写 IP 数据包的源 IP 或者目的 IP，被普遍地用来解决公网 IP 地址短缺的问题。它的主要原理就是，网络中的多台主机，通过共享同一个公网 IP 地址，来访问外网资源。同时，由于 NAT 屏蔽了内网网络，自然也就为局域网中的机器提供了安全隔离。

你既可以在支持网络地址转换的路由器（称为 NAT 网关）中配置 NAT，也可以在 Linux 服务器中配置 NAT。如果采用第二种方式，Linux 服务器实际上充当的是“软”路由器的角色。
<div><strong>精选留言（28）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/12/64/05/6989dce6.jpg" width="30px"><span>我来也</span> 👍（13） 💬（3）<div>[D41打卡]
在已有的项目经验中,还未涉及到过NAT.
倒是本地的虚拟机环境下,或者路由器上,会看到nat相关选项.

问题一:当多个内网 IP 地址的端口号相同时，MASQUERADE 还可以正常工作吗？
我觉得是可以正常工作的,要不然就不会允许设置ip地址段了.😁[纯属猜测哈]
在路由器上做端口映射时,一个外网端口只能对应一个内网的IP.
但是反方向,nat在转换源地址时,应该会记录原来的连接信息吧.要不然收到包该给谁发呢.

问题二:如果内网 IP 地址数量或请求数比较多，这种方式有没有什么隐患呢？
根据之前的经验,在请求数过多时,会导致CPU软中断上升.
再谷歌了下,有看到说:
iptables的conntrack表满了导致访问网站很慢.[https:&#47;&#47;my.oschina.net&#47;jean&#47;blog&#47;189935]
    ```kernel 用 ip_conntrack 模块来记录 iptables 网络包的状态，并保存到 table 里（这个 table 在内存里），如果网络状况繁忙，比如高连接，高并发连接等会导致逐步占用这个 table 可用空间。```

优化Linux NAT网关[https:&#47;&#47;tech.youzan.com&#47;linux_nat&#47;]
    ```net.netfilter.nfconntrackbuckets 这个参数，默认有点小，连接数多了以后，势必造成“哈希冲突”增加，“哈希处理”性能下降。（ 是这样吗？）```

</div>2019-02-25</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTL9hlAIKQ1sGDu16oWLOHyCSicr18XibygQSMLMjuDvKk73deDlH9aMphFsj41WYJh121aniaqBLiaMNg/132" width="30px"><span>腾达</span> 👍（6） 💬（1）<div>大伙儿都掉队了吗？有深度的问题留言越来越少，有价值的问题回答也少了。</div>2019-02-25</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTLzvaL724GwtzZ5mcldUnlicicSlI8BXL9icRZbUOB10qjRMlmog7UTvwxSBHXagnPGGR1BYdjWcGGSg/132" width="30px"><span>wwj</span> 👍（3） 💬（1）<div>nat的三种类型有什么本质的区别、和链接追踪的联系有是什么</div>2019-02-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/a8/8b/c5c234b6.jpg" width="30px"><span>小庄.Jerry</span> 👍（3） 💬（1）<div>最近我们的一个客户，遇到问题2的问题了。该公司很多用户同时加入我们的会议系统，一般来说，客户会访问我们部署在当地数据中心的服务器，结果很多用户访问到我们数据美国数据中心的服务器了，导致糟糕的体验。
我们的网络team给的解决方案:禁用了我们服务器的tcp_tw_recycle。
看了man tcp的介绍，对于NAT网络中，要求禁掉tcp_tw_recycle。但是对于个中的原理还不是很明白，希望老师可以帮忙解释下</div>2019-02-27</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/xzHDjCSFicNY3MUMECtNz6sM8yDJhBoyGk5IRoOtUat6ZIkGzxjqEqwqKYWMD3GjehScKvMjicGOGDog5FF18oyg/132" width="30px"><span>李逍遥</span> 👍（3） 💬（1）<div>有个疑问， 看了访问baidu.com的例子，发包和收报都是需要NAT的，那是不是只配置SNAT或DNAT，就不能正常访问外网或被访问了呢？</div>2019-02-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/c0/ce/fc41ad5e.jpg" width="30px"><span>陳先森</span> 👍（2） 💬（1）<div>第一个问题是可以的，外网端口映射内网端口是一对多。就跟之前老师留言的一样，服务端对端口没有65535个端口限制但是客户端有。
第二个问题会有隐患，请求数量多的时候会导致软路由服务器的资源和性能下降，甚至延时和超时都有可能以至于达到系统资源的瓶颈系统的软连接数达到瓶颈或者无法正常工作</div>2019-04-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/aa/30/acc91f01.jpg" width="30px"><span>honnkyou</span> 👍（2） 💬（1）<div>&quot;再来看 DNAT，显然，DNAT 需要在 nat 表的 PREROUTING 或者 OUTPUT 链中配置，其中， PREROUTING 链更常用一些（因为它还可以用于转发的包）。&quot;
DNAT不是转换到达包的目的地址吗？也可以在OUTPUT链中配置吗？</div>2019-03-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/88/17/68aa48cb.jpg" width="30px"><span>曾经的十字镐</span> 👍（1） 💬（1）<div>我们有部分业务需要向外同步数据，但又必须保证内网服务器的安全，所以我就使用了nat网络，单纯知道外网ip是无法攻击的</div>2019-03-01</li><br/><li><img src="https://wx.qlogo.cn/mmopen/vi_32/PiajxSqBRaEKQMM4m7NHuicr55aRiblTSEWIYe0QqbpyHweaoAbG7j2v7UUElqqeP3Ihrm3UfDPDRb1Hv8LvPwXqA/132" width="30px"><span>ninuxer</span> 👍（1） 💬（1）<div>打卡day43
工作场景没用到nat，基本都是基于4层或7层的反代
针对第一个问题，是可以的，第二个问题不可以，我认为是有连接追踪表，文件数量，端口数量的限制</div>2019-02-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/57/6e/b6795c44.jpg" width="30px"><span>夜空中最亮的星</span> 👍（1） 💬（1）<div>第一个问题：是可以正常工作的，是由（源地址：源端口   目的地址：目的端口 ）来标记的
第二个问题：会把这台linux主机撑爆了</div>2019-02-25</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/93/43/0e84492d.jpg" width="30px"><span>Maxwell</span> 👍（1） 💬（1）<div>vmware中虚拟机网络选择NAT模式后，IP地址经常变动，有什么方法解决么？</div>2019-02-25</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/11/4b/fa64f061.jpg" width="30px"><span>xfan</span> 👍（0） 💬（1）<div>终于搞明白了iptables原理和写法</div>2019-02-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/8c/2b/3ab96998.jpg" width="30px"><span>青石</span> 👍（72） 💬（5）<div>问题1：Linux的NAT时给予内核的连接跟踪模块实现，保留了源IP、源端口、目的IP、目的端口之间的关系，多个内网IP地址的端口相同，但是IP不同，再nf_conntrack中对应不同的记录，所以MASQUERADE可以正常工作。

问题2：NAT方式所有流量都要经过NAT服务器，所以NAT服务器本身的软中断导致CPU负载、网络流量、文件句柄、端口号上限、nf_conntrack table full都可能是性能瓶颈。</div>2019-03-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/f8/4b/5ae62b10.jpg" width="30px"><span>Geek_b04b12</span> 👍（6） 💬（0）<div>1）iptalbes的三个表

filter 这个表主要用于过滤包的，是系统预设的表，这个表也是阿铭用的最多的。内建三个链INPUT、OUTPUT以及FORWARD。INPUT作用于进入本机的包；OUTPUT作用于本机送出的包；FORWARD作用于那些跟本机无关的包。

nat 主要用处是网络地址转换，也有三个链。PREROUTING 链的作用是在包刚刚到达防火墙时改变它的目的地址，如果需要的话。OUTPUT链改变本地产生的包的目的地址。POSTROUTING链在包就要离开防火墙之前改变其源地址。该表阿铭用的不多，但有时候会用到。

mangle 这个表主要是用于给数据包打标记，然后根据标记去操作哪些包。这个表几乎不怎么用。除非你想成为一个高级网络工程师，否则你就没有必要花费很多心思在它上面。</div>2019-09-06</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/f8/4b/5ae62b10.jpg" width="30px"><span>Geek_b04b12</span> 👍（5） 💬（1）<div>http:&#47;&#47;www.apelearn.com&#47;study_v2&#47;chapter16.html#id3  这个链接是我初次接触linux的时候学习的课程，对小白蛮友好</div>2019-09-06</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/f6/24/547439f1.jpg" width="30px"><span>ghostwritten</span> 👍（1） 💬（0）<div>1. NAT 可以分为三类：
静态 NAT，即内网 IP 与公网 IP 是一对一的永久映射关系；
动态 NAT，即内网 IP 从公网 IP 池中，动态选择一个进行映射；
网络地址端口转换 NAPT（Network Address and Port Translation），即把内网 IP 映射到公网 IP 的不同端口上，让多个内网 IP 可以共享同一个公网 IP 地址。

2.  NAPT 分为三类：
第一类是源地址转换 SNAT，即目的地址不变，只替换源 IP 或源端口。SNAT 主要用于，多个内网 IP 共享同一个公网 IP来访问外网资源的场景。
第二类是目的地址转换 DNAT，即源 IP 保持不变，只替换目的 IP 或者目的端口。DNAT 主要通过公网 IP 的不同端口号，来访问内网的多种服务，同时会隐藏后端服务器的真实 IP 地址。
第三类是双向地址转换，即同时使用 SNAT 和 DNAT。当接收到网络包时，执行 DNAT，把目的 IP 转换为内网 IP；而在发送网络包时，执行 SNAT，把源 IP 替换为外部 IP。

3. nat 表内置了三个链
PREROUTING`，用于路由判断前所执行的规则，比如，对接收到的数据包进行 DNAT；
`POSTROUTING`，用于路由判断后所执行的规则，比如，对发送或转发的数据包进行 SNAT 或 MASQUERADE。
 `OUTPUT`，类似于 PREROUTING，但只处理从本机发送出去的包。

4. SNAT
iptables -t nat -A POSTROUTING -s 192.168.0.0&#47;16 -j MASQUERADE
iptables -t nat -A POSTROUTING -s 192.168.0.2 -j SNAT --to-source 100.100.100.100

5. DNAT
iptables -t nat -A PREROUTING -d 100.100.100.100 -j DNAT --to-destination 192.168.0.2

6. 双向地址转换
$ iptables -t nat -A POSTROUTING -s 192.168.0.2 -j SNAT --to-source 100.100.100.100
$ iptables -t nat -A PREROUTING -d 100.100.100.100 -j DNAT --to-destination 192.168.0.2

</div>2021-08-05</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/19/c4/35/2cc10d43.jpg" width="30px"><span>Wade_阿伟</span> 👍（1） 💬（0）<div>对于第一个问题：当多个内网 IP 地址的端口号相同时，MASQUERADE 还可以正常工作吗？答案是肯定可以工作的。因为netfilter_conntrack中记录的是五元组信息，包括源端口、源Ip、目的端口、目的ip等信息。即便源端口相等，也能组成不同的连接记录。
第二个问题：如果内网 IP 地址数量或请求数比较多，会导致服务器整体的性能下降，包括导致cpu的软中断过多，nf_conntrack连接跟踪表中记录过多，导致跟踪表溢出。导致服务器table over full，从而导致服务器出现响应延时并丢包等问题。</div>2021-01-03</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/65/3a/bc801fb2.jpg" width="30px"><span>mqray</span> 👍（0） 💬（0）<div>还是没搞懂为什么 nat 里面snat要 对应 prerouting这条链，而dnat则写在 postrouting 和output中</div>2023-09-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/19/b2/91/714c0f07.jpg" width="30px"><span>zero</span> 👍（0） 💬（0）<div>以前看iptables，一脸懵逼，现在知道了一丢丢</div>2023-03-02</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/79/d5/4a7971fc.jpg" width="30px"><span>Ethan</span> 👍（0） 💬（2）<div>老师有两个问题，感觉需要重新讨论下：

第一个关于 SNAT 和 DNAT 的解释：

原文中说：

SNAT 主要用于，多个内网 IP 共享同一个公网 IP ，来访问外网资源的场景。
DNAT 主要通过公网 IP 的不同端口号，来访问内网的多种服务，同时会隐藏后端服务器的真实 IP 地址。

这里给人的感觉好像是 SNAT 和 DNAT 是两个不同的应用场景。但我理解，并不是这样。
首先内网的服务器想和外网通信，不可能是单方向的通信，必定涉及到一来一回。

如果单单做 SNAT，这里仅仅解决的是发送数据包时，把源地址进行替换和外网通信。
但外网想和内网的服务器通信，还涉及到回包的过程，将外网的目的地址（也就是发送的源地址）进行转换，也就是 DNAT。

所以通过 SNAT 和 DNAT 结合起来才能实现内网访问外网，以及隐藏后端服务器地址的作用。


第二个是关于一个同学的提问：

提问如下：
有个疑问， 看了访问baidu.com的例子，发包和收报都是需要NAT的，那是不是只配置SNAT或DNAT，就不能正常访问外网或被访问了呢？
老师回答：
作者回复: 不是的，内核有连接跟踪，知道每个请求的来源和目的

我和老师的看法不一样，我认为这个同学说的是对的，如果仅仅配置 SNAT 或者 DNAT 是无法通信的，原因就在于上面的解释，通信是一来一回的过程。
除非，我们隐含 SNAT 包含了 DNAT 的步骤，或者 DNAT 包含了 SNAT 的步骤。

并且这里做了实验验证：
使用 docker 以 run 的形式起了一个 nginx 容易，并暴露 80 端口给到外网。
这时外面是可以和 nginx 正常交互的。

并且查看 iptables 中 nat 表的，PREROUTING 和 POSTROUTING 链。
可以找到 PREROUTING 做了 DNAT。
POSTROUTING 做了MASQUERADE，就是动态的 snat.

当我手动把 DNAT 删除，光留下 snat 时，这时是无法正常通信的。
在容器内抓包后发现，流量根本进入不到容器内。</div>2022-07-06</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1f/90/f1/7f2b5e16.jpg" width="30px"><span>CHN-Lee-玉米</span> 👍（0） 💬（0）<div>曾经遇过内网大量机器通过一个公网IP地址访问另一个公网IP，导致端口号用满的情况</div>2021-06-06</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/16/f0/3051cc84.jpg" width="30px"><span>兵临城下</span> 👍（0） 💬（0）<div>老师，我想问一下。系统使用的，阿里云SLB（负载）+ECS，ECS上设置 iptables 禁用某个IP，如何能启作用？默认是内网的SLB的IP</div>2020-11-30</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/7d/d8/d7c77764.jpg" width="30px"><span>HunterYuan</span> 👍（0） 💬（0）<div>对于问题1：可以工作，因为NAT转换是通过状态连接表的，状态连接表中会记录正向数据的状态的五元组和返现数据的五元组，通过查找此状态连接进行逆向转换（例如SNAT的反向转换），建立一一对应的关系。有了这些表示就可以进行完全转换，对于不同内网IP的相同端口数据包，进行MASQUERADE时，会随机选择一个出接口的IP，若此时不同内网IP访问的目的IP通过路由，都是从MASQUERADE设备的同一个口出去，那么他们做SNAT时会使用相同的IP，为了达到一一对应区别不同的内网IP，此时选择一个未被使用的端口进行SAPT，这样反向的数据访问相同的外网IP，通过不同目的端口，找到相应内网IP。
对于问题2，若是请求数量比较多，对于问题一中需要进行SAPT的被占用端口数将是其瓶颈，还需要考虑状态连接的总数最大值，是否为瓶颈。
对于两个问题，这是我的理解，若有错误，希望老师指正，不要因为我的错误回答，误导队友的理解。谢谢老师，不吝赐教。</div>2020-02-03</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/f8/4b/5ae62b10.jpg" width="30px"><span>Geek_b04b12</span> 👍（0） 💬（0）<div>以前在学习linux的时候，自己搭建过linux的下的nginx的负载均衡， 内网的处理后的结果转发，记得好想负载均衡和高可用，具体哪一个忘记了，工作的时候用过一次，将内网服务器处理请求后转发给那个可以上外网的服务器，然后返回给外网。。。本节有有好几个陌生的名词。。</div>2019-09-06</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/mnBC29lF1RibHdwkZdPdGM9QRAl7Y7Aicad8vpmIEialjia93IEVSAHibkKdwHwfZr6qedVHiafKUD8Yk1v2eiaibj8l0w/132" width="30px"><span>xierongfei</span> 👍（0） 💬（0）<div>问题1：
可以, MASQUERADE 主要用内部多个IP公用一个公网访问访问外部地址，发起连接的是本机的一个随机端口，并且是用在公网IP不固定情况下，比如拨号场景；
问题2：
 会有性能问题，比如访问缓慢。客户端过多，并且连接过多，iptables conntrack表会满，并发生空间溢出</div>2019-04-13</li><br/><li><img src="" width="30px"><span>如果</span> 👍（0） 💬（0）<div>DAY41，打卡</div>2019-04-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/47/46/61f16147.jpg" width="30px"><span>唯美</span> 👍（0） 💬（0）<div>项目中还没有用到，学习中</div>2019-02-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/42/76/256bbd43.jpg" width="30px"><span>松花皮蛋me</span> 👍（0） 💬（0）<div>iptables性能还是有问题的</div>2019-02-26</li><br/>
</ul>