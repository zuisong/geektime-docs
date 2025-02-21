你好，我是邵亚方。我们这节课来讲一下，TCP数据在传输过程中会受到哪些因素干扰。

TCP收包和发包的过程也是容易引起问题的地方。收包是指数据到达网卡再到被应用程序开始处理的过程。发包则是应用程序调用发包函数到数据包从网卡发出的过程。你应该对TCP收包和发包过程中容易引发的一些问题不会陌生，比如说：

- 网卡中断太多，占用太多CPU，导致业务频繁被打断；
- 应用程序调用write()或者send()发包，怎么会发不出去呢；
- 数据包明明已经被网卡收到了，可是应用程序为什么没收到呢；
- 我想要调整缓冲区的大小，可是为什么不生效呢；
- 是不是内核缓冲区满了从而引起丢包，我该怎么观察呢；
- …

想要解决这些问题呢，你就需要去了解TCP的收发包过程容易受到哪些因素的影响。这个过程中涉及到很多的配置项，很多问题都是这些配置项跟业务场景不匹配导致的。

我们先来看下数据包的发送过程，这个过程会受到哪些配置项的影响呢？

## TCP数据包的发送过程会受什么影响？

![](https://static001.geekbang.org/resource/image/5c/5e/5ce5d202b7a179829f4c9b3863b0b15e.jpg?wh=4500%2A3274 "TCP数据包发送过程")

上图就是一个简略的TCP数据包的发送过程。应用程序调用write(2)或者send(2)系列系统调用开始往外发包时，这些系统调用会把数据包从用户缓冲区拷贝到TCP发送缓冲区（TCP Send Buffer），这个TCP发送缓冲区的大小是受限制的，这里也是容易引起问题的地方。
<div><strong>精选留言（13）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/1e/3b/d7/9d942870.jpg" width="30px"><span>邵亚方</span> 👍（19） 💬（0）<div>课后作业答案：
- 在 TCP 发送过程中使用到了 qdisc，但是在接收过程中没有使用它，请问是为什么？我们可以在接收过程中也使用 qdisc 吗？
qdisc的主要目的是流控，流控一般都是在发送端进行控制；对于接收端而言，它已经收到这个包了，再进行流控的话，也就只有选择性的丢包。如果在接收端也使用qdisc之类的流控机制，也需要将它模拟为发送端，也就是增加一个中间设备来做。</div>2020-10-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/64/05/6989dce6.jpg" width="30px"><span>我来也</span> 👍（11） 💬（3）<div>终于到TCP篇了.

看了文中的`TCP数据包发送过程`图,有几个疑问:
1. 如果用tcpdump抓包,它是在哪一层抓的包呢?(IP Layer &#47; Link Layer)
   最近遇到的问题,就是调用write函数有返回值.但是tcpdump抓包来看,并没有迹象.
   只知道在此期间有地方把包给丢了,并不知道具体是哪一层丢的.后来发现是内核把包丢了.
2. `TCP Send Buffer`默认是动态调整的.
   这个是按需分配的意思么?如果我调整了内核参数,对之前建立的连接产生影响么?
3. 如果`TCP Send Buffer`满了,调用`write`时是阻塞还是返回错误码呢?(是不是跟TCP的阻塞&#47;非阻塞模式有关?)

-------------------
最近在CentOS 7.6上遇到了一个TCP内核方面的问题.
它的内核版本太低了,还是linux-3.10.0-957.21.3.el7.

具体的分析和解决过程参考了这篇博文:
[TCP SACK 补丁导致的发送队列报文积压](https:&#47;&#47;runsisi.com&#47;2019-12-19&#47;tcp-sack-hang)
</div>2020-09-15</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTJpJXWFP3dNle88WnTkRTsEQkPJmOhepibiaTfhEtMRrbdg5EAWm4EzurA61oKxvCK2ZjMmy1QvmChw/132" width="30px"><span>唐江</span> 👍（1） 💬（2）<div>发送和接收端的缓冲区都是针对单个连接的吗</div>2021-05-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/ed/91/1d332031.jpg" width="30px"><span>我能走多远</span> 👍（4） 💬（1）<div>又一个问题需要帮忙解答一下，就是网络收包一共会又几次内存拷贝的流程。
看到一篇文章中说DMA也算一次的化，会又三次？（https:&#47;&#47;blog.csdn.net&#47;gengzhikui1992&#47;article&#47;details&#47;103142848）
对1，2 步中内存拷贝没有理解透。
1、DMA操作，网卡寄存器-&gt;内核为网卡分配的缓冲区ring buffer
  ring buffer存储的描述符的索引，索引对应存储存储报文的物理地址吧&#47;
2、驱动软件从ring buffer中读取，填充内核skbuff结构（第2次拷贝：内核网卡缓冲区ring buffer-&gt;内核专用数据结构skbuff）
 它是把填充skbuff头部也当作了一次内存拷贝吗？
3、socket系统调用将数据从内核搬移到用户态。(第3次拷贝：内核空间-&gt;用户空间)
这个是系统调用，比较好理解。

</div>2020-11-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/19/c4/35/2cc10d43.jpg" width="30px"><span>Wade_阿伟</span> 👍（1） 💬（0）<div>从tcp的发送过程和接受过程，讲解过程中可能影响的配置选项。让我既能很好的理解发送和接受过程，又学习了如何结合生产环境业务场景进行性能优化，真是收货满满。</div>2021-09-05</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/18/fb/c1334976.jpg" width="30px"><span>王崧霁</span> 👍（1） 💬（1）<div>流控应该在上游发送端控制，接收端有个开关net.core.devbudget也是控制发端行为</div>2020-09-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/17/37/a0/032d0828.jpg" width="30px"><span>上杉夏香</span> 👍（0） 💬（0）<div>捉个虫，课堂总结第一行中关于 tcp_wmem 的说明，应该是「如果通过SO_SNDBUF来设置发送发送缓冲区」而是不「SO_RECVBUF」</div>2023-04-03</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/20/81/02/59f5f168.jpg" width="30px"><span>小白debug</span> 👍（0） 💬（0）<div>有个疑惑，老师提到qdisc是在ip层里实现的，但在看代码的时候发现，qdisc是在 __dev_queue_xmit （数据链路层）中被使用到，那qdisc是属于哪一层的呢？</div>2022-11-04</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/b5/1d/f2f66e8d.jpg" width="30px"><span>团团-BB</span> 👍（0） 💬（0）<div>老师这种情况从何处入手：
eth0: flags=4163&lt;UP,BROADCAST,RUNNING,MULTICAST&gt;  mtu 9001
        inet 10.201.80.130  netmask 255.255.224.0  broadcast 10.201.95.255
        ether 02:c6:7a:df:c2:09  txqueuelen 1000  (Ethernet)
        RX packets 55403028044  bytes 88466263876451 (80.4 TiB)
        RX errors 0  dropped 1432413  overruns 0  frame 0
        TX packets 111313645859  bytes 182202219572067 (165.7 TiB)
        TX errors 0  dropped 0 overruns 0  carrier 0  collisions 0</div>2022-04-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/4d/fe/882eaf0f.jpg" width="30px"><span>威</span> 👍（0） 💬（1）<div>如果用 sysctl -p 来使得tcp缓冲区配置立刻生效，这样做之后，已建立了的tcp链接缓冲区大小会改变吗</div>2022-02-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/53/b5/d914f2c2.jpg" width="30px"><span>晴天</span> 👍（0） 💬（0）<div>老师，还有个内核参数netdev_max_backlog也值得讲讲</div>2022-01-02</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1f/68/12/031a05c3.jpg" width="30px"><span>A免帅叫哥</span> 👍（0） 💬（0）<div>19年1月份的commit，合并到5.8的内核，merge也挺慢的。</div>2021-09-06</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/dwehJHP4ycAfDb9MoudXb4QSt7YgmISqwwsa928XZ6aTWqwWh0kx0iatjocSibLa7iajXmbGlJ5svegY3P6LfKJ0w/132" width="30px"><span>solar</span> 👍（0） 💬（1）<div>用户通过openvpn连接服务器，然后使用的udp报文，然后测速发现连接VPN后的速度比连接VPN前要慢的多，但是服务器的入口带宽其实还剩余很多，这个是由于udp的缓存设置导致的吗？老师能解答下吗？</div>2020-09-28</li><br/>
</ul>