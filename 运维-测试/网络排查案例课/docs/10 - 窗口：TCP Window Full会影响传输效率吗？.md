你好，我是胜辉。

有时候，不少知识点在过段时间重新回看的时候，又会有新的体会和发现。比如在[第8讲](https://time.geekbang.org/column/article/484667)里，我们回顾了一个MTU造成传输失败的案例，虽然整个排查过程的步骤不算很多，但也算是TCP传输问题的一个缩影了。尤其是其中那个失败的TCP流中的一些现象，比如客户端发出的重复确认（DupAck），还有服务端启动的超时重传，都值得我们继续深挖，所以我会在后续的课程里继续这个话题。

然后在上节课里，我们还探讨了传输速度的相关知识，也初步学习了窗口的概念。最后，我们终于推导出了TCP传输的核心公式：速度=窗口/往返时间。这个公式，对于我们理解传输本质和排查传输问题，都有很强的指导意义。

然而，如果你足够细心的话，其实可能会对上节课里的细节有一些疑问，比如：既然接收窗口满了，那为什么当时没有看到TCP Window Full这种提示呢？

其实，我这边也有不少内容按住没有展开，包括核心公式的理解，我们在这节课里将有一个新的认识。另外，我也将带你继续挖掘窗口这个细分领域，这样你以后遇到跟窗口相关的问题，就知道如何破解了。

## 案例：TCP Window Full是导致异地拷贝速度低的原因吗？

也是在公有云服务的时候，有个客户有这么一个需求，就是要把文件从北京机房拷贝到上海机房。但是他们发现传输速度比较慢，就做了抓包。在查看抓包文件的时候，发现Wireshark有很多**TCP Window Full**这样的提示，不明白这些是否跟速度慢有关系，于是找我们来协助分析。
<div><strong>精选留言（17）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/12/21/b8/aca814dd.jpg" width="30px"><span>江山如画</span> 👍（17） 💬（1）<div>问题1:
序列号和确认号都占用 32bit，空间范围从 [0, 2**32-1], 最大是 2**32-1

问题2:
感觉接收端确认的这部分数据，就是用户进程从内核接收缓冲区中读取的数据。出现数据滞留，说明写接收缓冲区的速度大于读接收缓冲区的速度，基于此，可以从接收缓冲区的大小(接收窗口的大小)，写接收缓冲区的速度，读接收缓冲区的速度三方面考虑。

从接收缓冲区的自身的大小考虑，出现数据滞留，可能是接收窗口太小了，比如 &#47;proc&#47;sys&#47;net&#47;ipv4&#47;tcp_window_scaling 设置为了0，导致窗口上限就是 65535。

从读接收缓冲区的角度考虑，出现数据滞留，可能是用户进程读取速度太慢了，用户进程读取的时候也可能一次也读区不完，需要读取多次，这里取决于用户进程的代码逻辑，极端情况下，比如每调用一次 recv，就 sleep 一段时间。

写接收缓冲区的速度由tcp协议栈维护，取决于接收窗口大小和读接收缓冲区的速度。
</div>2022-02-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/1f/51/5e2c484e.jpg" width="30px"><span>静静同学</span> 👍（10） 💬（1）<div>老师，我们工作中有同事遇到了tcp window zero，我当时没参与这个任务，没去看具体的抓包数据，但好像也是接收端窗口满了的原因。请问window zero 和window full的区别是什么呢？是视角不同吗？zero是接收端视角，full是发送端视角？</div>2022-03-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/18/81/83b6ade2.jpg" width="30px"><span>好吃不贵</span> 👍（2） 💬（4）<div>老师好，请教下，如果是长连接，没法抓到TCP之前的SYN报文了，在抓到的报文里，window size scaling factor字段显示为-1(unknown)，有什么办法解决吗？多谢。</div>2022-02-19</li><br/><li><img src="" width="30px"><span>Geek_4661de</span> 👍（1） 💬（1）<div>这里理解起来还是有点复杂的，
1. 首先v = 窗口 &#47; rtt，这里的窗口是指发送窗口，又知道发送窗口 = Math.min(对端接收窗口，自身拥塞窗口)，在自身拥塞窗口不是瓶颈的情况下，窗口就是指接收窗口；
2. 发送的data其实等于发送窗口值（也就是接收窗口），如果这些数据全部被ack了，那么套上正确公式```v = acked_data &#47; rtt```也就等价于```v = 窗口 &#47; rtt ```
</div>2023-09-25</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/29/88/8a/9008b284.jpg" width="30px"><span>Henry</span> 👍（1） 💬（1）<div>文件从北京机房拷贝到上海机房。但是他们发现传输速度比较慢
接收端只确认部分数据，导致了“数据滞留”现象，这个现象背后的原因可能是什么呢？
1、确认接收端 TCP接收缓冲区大小
2、已到达tcp缓冲区的字节，为什么没有快速的被取走，属于知识盲区</div>2023-06-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/17/48/8f/b728f820.jpg" width="30px"><span>AlohaJack</span> 👍（1） 💬（4）<div>&quot;不知道你有没有考虑到这个问题：Bytes in flight 是指真的一直在网络上两头不着吗？一般来说，数据到了接收端，接收端就发送 ACK 确认这部分数据，然后 TCP Window 就往下降了。比如 ACK 300 字节，那么 TCP Window 就又空出来 300 字节，也就是发送端又可以新发送 300 字节了。&quot;

老师，这里对应的图里面，t3时刻回的ack包里面，窗口应该是从0变成了300吧，图里面ack的window=1000，这里不是很直观。
t3时刻ack的包里window是300
t4时刻A收到了这个ack，才可以继续发送300B
图里面改成300可能要直观点，还是我理解有偏差</div>2022-08-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/8f/cf/890f82d6.jpg" width="30px"><span>那时刻</span> 👍（1） 💬（1）<div>第一题：tcp头的序列号是32位，所以最大值是2^32。 如果短时间内发送大量数据，会有序列号回绕的问题。
第二题，接收端只确认了部分数据，可能接收程序处理慢，没有及时响应网卡缓冲区的irq，接收了部分数据。抑或网卡多队列导致接收不及时。</div>2022-02-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/c4/03/f753fda7.jpg" width="30px"><span>JianXu</span> 👍（0） 💬（1）<div>如果把老师这个课程里的案例都实际操作一遍，相信一定对于网络抓包分析问题达到实操水平的。对于我们部门的分布式防火墙和分布式负载均衡系统的问题排查我也相信用同样的方法可以批量的培训人。

更难或者更重要的是：怎么才能让更多的人有像老师这样的心和动力去 准备这样的培训呢？人性的善需要被激发，而激发的方法是多样的。</div>2022-10-15</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/4f/ca/3ac60658.jpg" width="30px"><span>orange</span> 👍（0） 💬（1）<div>我们公司之前遇到一个问题，访问特别慢，排查到最后，ss命令发现是 被攻击了，8081端口的 接收队列满了，默认是128</div>2022-03-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/18/7c/25/70134099.jpg" width="30px"><span>许凯</span> 👍（0） 💬（1）<div>如果高速公路的路更宽、车速更快，那么就相当于接收窗口变得更大，车辆就能进更多，也就相当于 Bytes in flight 更大了。      

老师这句话是否不妥哈？</div>2022-02-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/76/f5/e3f5bd8d.jpg" width="30px"><span>宝仔</span> 👍（0） 💬（1）<div>老师我想问下，你这个案例里用scp从北京机房拷贝到上海机房，为什么服务端数据确认这么慢，这个你们后来查到是为啥吗</div>2022-02-15</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTJnugUNWBtcszhJg3Q0hqEMSHftKco2TqCG78blZ3ibjncjZ64NbibGia5l4NB0DUibIq0BCZ03JvkoNA/132" width="30px"><span>Geek__e15575f5b6ec</span> 👍（0） 💬（1）<div>(2) 有时候发送的时候拆包了 接收端接收的时候  需要完整数据  所以只能等到后续的数据
</div>2022-02-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/7f/d3/b5896293.jpg" width="30px"><span>Realm</span> 👍（0） 💬（1）<div>1. 默认最大2的32次方，好像也有一些机制，比如使用timestaps，用来防止序列号环绕，是不是一定程度上也突破了这个最大限制？
2 接收端，用户程序处理速度过慢，或者网卡出现故障。

</div>2022-02-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/eb/09/ba5f0135.jpg" width="30px"><span>Chao</span> 👍（0） 💬（1）<div>2 ** 32 -1</div>2022-02-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/64/05/6989dce6.jpg" width="30px"><span>我来也</span> 👍（0） 💬（1）<div>从老师的文章中学了不少工具的使用方法，以前只会傻傻的看每个报文。马上就把它给用起来，😄</div>2022-02-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/23/5b/983408b9.jpg" width="30px"><span>悟空聊架构</span> 👍（0） 💬（0）<div>有个疑问：
原文：Wireshark 报告 TCP Window Full 是因为，一端的在途数据跟另一端的接收窗口相等。

疑问：在途字节数为 863800 字节，远远大于接收窗口的 112000，并不是相等呢？</div>2024-11-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/36/8b/7a/ec36ff82.jpg" width="30px"><span>原则</span> 👍（0） 💬（0）<div>老师这里是不是说错了？

「中期这里的 Calculated Window Size 明显增大了，到了 445312 字节。再看看后半程」

从抓包来开，Calculated Window Size 还是 19200 字节，这里说的是不是在途字节数？在途字节数是 443800 字节</div>2023-06-04</li><br/>
</ul>