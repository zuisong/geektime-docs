你好，我是倪朋飞。

上一节，我们学习了 NAT 的原理，明白了如何在 Linux 中管理 NAT 规则。先来简单复习一下。

NAT 技术能够重写 IP 数据包的源 IP 或目的 IP，所以普遍用来解决公网 IP 地址短缺的问题。它可以让网络中的多台主机，通过共享同一个公网 IP 地址，来访问外网资源。同时，由于 NAT 屏蔽了内网网络，也为局域网中机器起到安全隔离的作用。

Linux 中的NAT ，基于内核的连接跟踪模块实现。所以，它维护每个连接状态的同时，也对网络性能有一定影响。那么，碰到 NAT 性能问题时，我们又该怎么办呢？

接下来，我就通过一个案例，带你学习 NAT 性能问题的分析思路。

## 案例准备

下面的案例仍然基于 Ubuntu 18.04，同样适用于其他的 Linux 系统。我使用的案例环境是这样的：

- 机器配置：2 CPU，8GB 内存。
- 预先安装 docker、tcpdump、curl、ab、SystemTap 等工具，比如

```
  # Ubuntu
  $ apt-get install -y docker.io tcpdump curl apache2-utils
  
  # CentOS
  $ curl -fsSL https://get.docker.com | sh
  $ yum install -y tcpdump curl httpd-tools
```

大部分工具，你应该都比较熟悉，这里我简单介绍一下 SystemTap 。

[SystemTap](https://sourceware.org/systemtap/) 是 Linux 的一种动态追踪框架，它把用户提供的脚本，转换为内核模块来执行，用来监测和跟踪内核的行为。关于它的原理，你暂时不用深究，后面的内容还会介绍到。这里你只要知道怎么安装就可以了：
<div><strong>精选留言（30）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/13/60/71/895ee6cf.jpg" width="30px"><span>分清云淡</span> 👍（48） 💬（1）<div>https:&#47;&#47;mp.weixin.qq.com&#47;s&#47;VYBs8iqf0HsNg9WAxktzYQ：（多个容器snat时因为搜索本地可用端口（都从1025开始，到找到可用端口并插入到conntrack表是一个非事务并且有时延--第二个插入会失败，进而导致第一个syn包被扔掉的错误，扔掉后重传找到新的可用端口，表现就是时延偶尔为1秒或者3秒）

这篇文章是我见过诊断NAT问题最专业的，大家要多学习一下里面的思路和手段</div>2019-03-01</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTL9hlAIKQ1sGDu16oWLOHyCSicr18XibygQSMLMjuDvKk73deDlH9aMphFsj41WYJh121aniaqBLiaMNg/132" width="30px"><span>腾达</span> 👍（11） 💬（1）<div>这个案例，能不能讲讲怎么找到是NAT问题？这个很关键，但文章里直接点明说是NAT问题，这个就不好了，一般看cpu,看其他指标很难想到是nat问题，真实场景里，怎么会想到是nat问题呢？</div>2019-03-01</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/c8/74/a1bd2307.jpg" width="30px"><span>vvccoe</span> 👍（10） 💬（3）<div>‘# 连接跟踪对象大小为 376，链表项大小为 16
nf_conntrack_max* 连接跟踪对象大小 +nf_conntrack_buckets* 链表项大小 
= 1000*376+65536*16 B
= 1.4 MB’   
老师 上面的376和16 是固定值吗？
</div>2019-02-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/63/2e/e49116d1.jpg" width="30px"><span>Geek_007</span> 👍（7） 💬（2）<div>老师你好，有两个问题想请教一下。
第一点，了解到ip_conntrack模块既然会限制链接，且调大会导致占用内存，而且调大了也不一定能解决大流量服务器的网络性能问题，我理解是不是应该关掉ip_conntrack模块，因为业务服务器按理说是不需要状态追踪的。
第二点，如果我关掉ip_conntrack，会不会因为我执行iptables命令导致该模块被加载，或者执行conntrack命令导致模块被加载。。</div>2019-04-10</li><br/><li><img src="" width="30px"><span>无名老卒</span> 👍（6） 💬（2）<div>很惊讶，之前在线上环境中就出现了kernel: nf_conntrack: table full, dropping packet.的报错，当时就认为是conntrack_max导致的，后面调整了这个值之后就恢复了，但其实那次故障也不应该会加载nf_conntrack模块，因为iptables规则只是设置了几个IP允许登陆服务器，当时也不清楚为什么会去加载这个模块了。

同时，conntrack_max和conntrack_buckets有没有什么联系呢？从描述中，感觉conntrack_buckets应该要大于conntrack_max才对，但实际 上不是这样，请老师解惑下。</div>2019-05-01</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/64/05/6989dce6.jpg" width="30px"><span>我来也</span> 👍（4） 💬（1）<div>[D42打卡]
今天的内容只能围观了.
居然还用了内核动态追踪工具,统计丢包位置.
对于我这种完全不了解内核的人来说, 只当是开了眼界.

对于我来说,目前知道 NAT会带来性能损耗 就行了.🤦‍♀️
能避免就避免使用,不能避免了就在请求数较多的场景下调些参数.

`# 连接跟踪对象大小为 376，链表项大小为 16`
这应该是c结构体的大小吧.
</div>2019-02-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/93/1b/bf902c9d.jpg" width="30px"><span>aliuql</span> 👍（1） 💬（1）<div>老师你好，docker，是不是必然会用到dnat的端口映射？linux服务器内 nat本身应该也有流量限制吧！</div>2019-07-31</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/f1/84/7d21bd9e.jpg" width="30px"><span>Goal</span> 👍（1） 💬（1）<div>nf_conntrack_buckets 和 nf_conntrack_max  从文中的描述没有搞清楚，
我们只是调整了 nf_conntrack_max（最大连接跟踪数），那么，这个连接是记录在 nf_conntrack_buckets（连接跟踪表）中的吗？，那是否意味着，调整max的同时，也得调整buckets表的大小？</div>2019-06-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/93/43/0e84492d.jpg" width="30px"><span>Maxwell</span> 👍（1） 💬（3）<div>请问这个错误是什么原因导致的呢？
root@maxwell-virtual-machine:&#47;usr&#47;bin&#47;env# stap --all-modules dropwatch.stp
semantic error: while resolving probe point: identifier &#39;kernel&#39; at dropwatch.stp:18:7
        source: probe kernel.trace(&quot;kfree_skb&quot;) { locations[$location] &lt;&lt;&lt; 1 }
                      ^

semantic error: no match

Pass 2: analysis failed.  [man error::pass2]
Tip: &#47;usr&#47;share&#47;doc&#47;systemtap&#47;README.Debian should help you get started.
</div>2019-03-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/57/6e/b6795c44.jpg" width="30px"><span>夜空中最亮的星</span> 👍（1） 💬（1）<div>以前只是知道net性能不好，今天通过老师的讲解彻底明白了来龙去脉。
公司内部上网用的就是net 人一多就特别慢。
业务基本上没用过net。</div>2019-02-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/e6/ee/e3c4c9b3.jpg" width="30px"><span>Cranliu</span> 👍（1） 💬（4）<div>今天是跟不上了，没有网络基础，进入到网络模块就开始觉得吃力了😂</div>2019-02-27</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/RQdib68D7dsoFlYXOweiaPqLrcyn2jD6DCGnz8nc2VFmhmX0bpGTeSrVM5M9Qs7ibIInAmt5MeLcpcNja5YjyZCIg/132" width="30px"><span>bigzuo</span> 👍（0） 💬（1）<div>不太熟悉linux 网络底层超过，这节课看的很费力</div>2019-07-03</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/e2/d8/f0562ede.jpg" width="30px"><span>manatee</span> 👍（0） 💬（1）<div>另外安装centos 安装systemtap那边有个小小的笔误，最后那个stab-prep 应该是stap-prep</div>2019-05-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/e2/d8/f0562ede.jpg" width="30px"><span>manatee</span> 👍（0） 💬（1）<div>讲个不是很重要的点，ab命令在centos中没有-s参数</div>2019-05-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/11/4b/fa64f061.jpg" width="30px"><span>xfan</span> 👍（0） 💬（1）<div>讲的不错，让我懂了追踪过程，和我最想知道的东西</div>2019-02-28</li><br/><li><img src="https://wx.qlogo.cn/mmopen/vi_32/PiajxSqBRaEKQMM4m7NHuicr55aRiblTSEWIYe0QqbpyHweaoAbG7j2v7UUElqqeP3Ihrm3UfDPDRb1Hv8LvPwXqA/132" width="30px"><span>ninuxer</span> 👍（0） 💬（1）<div>打卡day44
很少用nat，没有发言权😂
不过对于lvs的nat模式，之后如果用到，可以用这里的contrack命令分析分析具体状态
然后计算链表占用内存大小的，链接对象376和链表大小16是固定数值？</div>2019-02-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1b/3d/3d/66512c23.jpg" width="30px"><span>ben</span> 👍（33） 💬（0）<div>其实遇到很多问题的时候多看看内核日志就知道了，linux很智能的，很多报错信息都在日志里面，越遇到系统优化层面，就多要看看内核日志，我一般是使用journalctl -k -f来查看，有报错信息就Google，线上遇到nf_conntrack: table full，就是这样排查出来的，查看内核日志真的很重要，特别应用日志没看出什么来的时候</div>2020-03-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/4d/49/28e73b9c.jpg" width="30px"><span>明翼</span> 👍（4） 💬（0）<div>systemtap这个真牛，还可以追踪内核模块执行，长见识咯！iptables需要学习下</div>2019-03-01</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/ec/18/bf7254d3.jpg" width="30px"><span>肥low</span> 👍（1） 💬（1）<div>这个基础知识应该去哪里学习才能不走弯路呢……</div>2022-08-05</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1b/5d/51/87fc7ef9.jpg" width="30px"><span>Issac慜</span> 👍（1） 💬（0）<div>在测试系统的并发和新建时，出现过指标上不去的问题。最终就是发现最大连接跟踪数设置的比较小，导致测试不通过</div>2021-12-05</li><br/><li><img src="" width="30px"><span>小刚</span> 👍（1） 💬（1）<div>这篇文章仔细看了几遍，也操作了文中的实际案例。期间遇到的问题及解决方法顺便记录一下：

1.带NAT的docker启动不起来，docker logs 提示权限不足，修改Dockerfile，进入docker发现实际是 &#47;proc&#47;sys&#47;net&#47;netfilter&#47;nf_conntrack_max文件无写权限
2.systemtap按文中步骤安装后，执行脚本报符号找不到，尝试从源码安装仍不可用

我用的ubuntu版本为最新下载的18.04.5，原因为ubuntu18.04.5的内核版本(5.4)过高导致的兼容性问题，安装18.04.1(内核4.15.0)即可解决这两问题，其中systemtap问题要注意下systemtap和内核版本兼容。</div>2021-09-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/4f/2d/7b5ed6c2.jpg" width="30px"><span>章星</span> 👍（1） 💬（3）<div>执行第二个8080的容器的时候提示：
&#47;bin&#47;sh: 1: cannot create &#47;proc&#47;sys&#47;net&#47;netfilter&#47;nf_conntrack_max: Permission denied  
不知道有没有人碰到，怎么解决呢
root@vm101:&#47;home&#47;zhang# docker logs nginx         
&#47;bin&#47;sh: 1: cannot create &#47;proc&#47;sys&#47;net&#47;netfilter&#47;nf_conntrack_max: Permission denied
root@vm101:&#47;home&#47;zhang# docker ps -a
CONTAINER ID   IMAGE              COMMAND                  CREATED          STATUS                      PORTS     NAMES
79b0ea8bb408   feisky&#47;nginx:nat   &quot;&#47;bin&#47;sh -c &#39;echo 10…&quot;   11 minutes ago   Exited (2) 11 minutes ago             nginx</div>2021-08-12</li><br/><li><img src="" width="30px"><span>noma</span> 👍（1） 💬（0）<div>systemtap 这个使用姿势好高级！</div>2019-02-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/b7/e9/5400cdf3.jpg" width="30px"><span>扬一场远远的风</span> 👍（0） 💬（0）<div>老师，在排查容器性能问题时碰到一个容器与主机网络端口映射问题。
有一个k8s环境，redis裸部署在172.20.46.20主机上，端口为6878 。 在另一台主机-172.20.49.45上使用k8s部署了一个java应用，其中java进程有连接到redis(172.20.46.20:6878)。

现象：1、查看redis的客户端连接列表（client list的结果）发现有从172.20.49.45主机上连接到redis(172.20.46.20:6878)的端口号；2、然而，从主机172.20.9.45上使用netstat -na查看却没有查到有端口连接到该redis；3、使用kubectl exec -it -n yonbip {java服务}  -- bash 进入到java 容器中，使用netstat -na却能发现有多个端口在与redis通信。

问：java容器中连接到redis端口如何与主机172.20.49.45进行映射的，映射到主机172.20.49.45的端口为多少？这些端口是否与从redis 中执行client list得到的端口是一样的？或者返过来说，我从redis 中执行client list得到了172.20.49.45主机的连接端口，如何确定这些连接和端口是否为从172.20.49.45 主机上的java容器中发出来的连接呢？</div>2024-10-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/91/b4/d5d9e4fb.jpg" width="30px"><span>爱学习的小学生</span> 👍（0） 💬（0）<div>客户端连服务器是长连接3分钟发一次心跳，conntract的time_wait时间是不是改大点更好?</div>2024-07-03</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/c3/d1/bdf895bf.jpg" width="30px"><span>penng</span> 👍（0） 💬（0）<div>Netfilter模块很多操作系统没有开启，不然无法看到conntrack的各个内核参数，如要开启需要执行以下命令：
modprobe nf_conntrack

备注：一般启动防火墙，安装docker这些服务，会自动加载Netfilter模块
Netfilter的主要功能包括：
1. 包过滤：就是linux的防火墙功能
2. 状态跟踪：可以跟踪tcp和udp连接，根据连接状态进行更精细的过滤和操作
3. 网络地址转换（NAT）：将源IP地址和目标IP地址修改为其他地址，docker服务也需要nat功能。


</div>2023-11-01</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/17/39/f8/b5a1b669.jpg" width="30px"><span>Brilliant</span> 👍（0） 💬（1）<div>$ docker run --name nginx --privileged -p 8080:8080 -itd feisky&#47;nginx:nat
执行后容器没有启动起来，日志显示
&#47;bin&#47;sh: 1: cannot create &#47;proc&#47;sys&#47;net&#47;netfilter&#47;nf_conntrack_max: Permission denied

需要为容器中的入口指令提权，如下：
$ docker run --name nginx --privileged=true -u=root -p 8080:8080 -itd feisky&#47;nginx:nat &#47;bin&#47;sh

附docker版本为：20.10.17</div>2022-09-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/c4/03/f753fda7.jpg" width="30px"><span>JianXu</span> 👍（0） 💬（0）<div>
# 连接跟踪对象大小为376，链表项大小为16
nf_conntrack_max*连接跟踪对象大小+nf_conntrack_buckets*链表项大小 
= 1000*376+65536*16 B
= 1.4 MB

在这样的设置下，每一个bucket 所对应的list 大小是 1000&#47;65536 ? 那就是不到1,  意思是大部门情况都不需要单向链表遍历了吗？</div>2022-01-02</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/75/3a/a7596c06.jpg" width="30px"><span>大大</span> 👍（0） 💬（0）<div>不知道老师现在还能回答问题么，我们线上出现一个问题，内核比较新5.4，ipvs模式下，只有一台物理机上出现问题，pod内通过service访问服务，当后端的pod在本机时百分之百超时失败，经抓包发现svc后面的pod返回tcp三次握手的第二个包时原ip没有改成service  ipvs 导致client  直接reset</div>2020-11-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/18/01/bb/7d15d44a.jpg" width="30px"><span>欧雄虎(Badguy）</span> 👍（0） 💬（0）<div>老师我那个脚本不能执行成功，辛苦帮看下，自己百度没解决
root@VM-0-5-ubuntu:~# stap --all-modules dropwatch.stp
semantic error: while resolving probe point: identifier &#39;kernel&#39; at dropwatch.stp:19:7
        source: probe kernel.trace(&quot;kfree_skb&quot;) { locations[$location] &lt;&lt;&lt; 1 }
                      ^

semantic error: no match (similar tracepoints: map, kfree, rdpmc, unmap, read_msr)

Pass 2: analysis failed.  [man error::pass2]
Tip: &#47;usr&#47;share&#47;doc&#47;systemtap&#47;README.Debian should help you get started.
root@VM-0-5-ubuntu:~# uname -r
4.15.0-54-generic
</div>2020-04-26</li><br/>
</ul>