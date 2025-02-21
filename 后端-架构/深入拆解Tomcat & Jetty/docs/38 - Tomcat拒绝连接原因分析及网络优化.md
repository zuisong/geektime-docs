专栏上一期我们分析各种JVM OutOfMemory错误的原因和解决办法，今天我们来看看网络通信中可能会碰到的各种错误。网络通信方面的错误和异常也是我们在实际工作中经常碰到的，需要理解异常背后的原理，才能更快更精准地定位问题，从而找到解决办法。

下面我会先讲讲Java Socket网络编程常见的异常有哪些，然后通过一个实验来重现其中的Connection reset异常，并且通过配置Tomcat的参数来解决这个问题。

## 常见异常

**java.net.SocketTimeoutException**

指超时错误。超时分为**连接超时**和**读取超时**，连接超时是指在调用Socket.connect方法的时候超时，而读取超时是调用Socket.read方法时超时。请你注意的是，连接超时往往是由于网络不稳定造成的，但是读取超时不一定是网络延迟造成的，很有可能是下游服务的响应时间过长。

**java.net.BindException: Address already in use: JVM\_Bind**

指端口被占用。当服务器端调用new ServerSocket(port)或者Socket.bind函数时，如果端口已经被占用，就会抛出这个异常。我们可以用`netstat –an`命令来查看端口被谁占用了，换一个没有被占用的端口就能解决。
<div><strong>精选留言（18）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/13/ee/23/b92b0811.jpg" width="30px"><span>读书看报</span> 👍（7） 💬（1）<div>老师可以讲下：Jconsole 线程信息里 总阻止数和总等待数的含义吗？还有线程已启动的总数(这个数字很大)是什么意思？</div>2019-08-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/ee/23/b92b0811.jpg" width="30px"><span>读书看报</span> 👍（3） 💬（5）<div>老师能讲下 maxConnections 与 maxThreads 的区别和联系吗？</div>2019-08-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/79/4b/740f91ca.jpg" width="30px"><span>-W.LI-</span> 👍（0） 💬（1）<div>老师好!TCP链接time_wait我和线程状态搞混了。。。我哭</div>2019-08-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/55/45/e4314bc6.jpg" width="30px"><span>magicnum</span> 👍（46） 💬（0）<div>增大accept队列长度使得tomcat并发短连接数暴增，必然导致服务器处理完请求后需要主动断开连的连接数增加；断开连接时四次挥手的最后一个阶段，客户端要等待2mls时间来保证服务端收到了客户端的ack（如果服务端没有收到最后一次挥手ack会重试，这时客户端需要重新发送ack），这时会导致大量time_wait；一旦达到上限将导致服务器拒绝服务</div>2019-08-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/4d/fd/0aa0e39f.jpg" width="30px"><span>许童童</span> 👍（16） 💬（2）<div>TCP 连接处在 TIME_WAIT 状态，这个是TCP协议规定的，四次挥手时主动关闭方所处的一个状态，会等待2个MSL，所以在这个时间段内不会释放端口，如果并发量大的话，会导致端口不够用，从而影响新的TCP连接。</div>2019-08-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/64/86/f5a9403a.jpg" width="30px"><span>yang</span> 👍（9） 💬（1）<div>老师 这个问题我查了一下别处的答案 https:&#47;&#47;mp.weixin.qq.com&#47;s&#47;KtcDxcY-pZBsvwJhwuKJmw

说是tcp连接关闭的最后一步 time_wait 需要2MLS

文中说到:
请求方过多time_wait会导致“Cannot assign requested address”异常。

     服务方过多time_wait会导致”Too Many Open Files”异常。


</div>2019-08-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/7b/57/a9b04544.jpg" width="30px"><span>QQ怪</span> 👍（3） 💬（0）<div>保留timewait是为了是高效复用tcp连接，避免重复创建连接造成资源浪费，但过多的也会造成服务端文件打开数过多造成资源浪费</div>2019-08-08</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/WtHCCMoLJ2DvzqQwPYZyj2RlN7eibTLMHDMTSO4xIKjfKR1Eh9L98AMkkZY7FmegWyGLahRQJ5ibPzeeFtfpeSow/132" width="30px"><span>脱缰的野马__</span> 👍（2） 💬（0）<div>首先有几点需要明确：
1.连接关闭的发起方是请求端，四次挥手中的TIME_WAIT状态存在于请求端（发起方）；
2.请求端每次进行HTTP请求的时候，会使用一个临时的端口号，而机器的端口号是有限的，接收端是固定监听某个端口的；
3.建立连接时，机器是要打开一个文件句柄（这里我不太确定请求端要不要打开，接收端是肯定要打开一个文件句柄的，有肯定的同学可以赐教）。
然后我们来看如果存在大量TIME_WAIT状态的链接可能存在的问题：
如果在高并发场景下，可能会有如下问题
1.请求端的端口耗尽，因为处于TIME_WAIT状态不能释放连接所占用的相关资源，临时端口就是。如果端口耗尽的话请求端就无法再向外部进行HTTP请求，导致服务不可用等问题；
2.由于一直TIME_WAIT状态，最直接的原因是接收端一直没有接收到请求端最后一次挥手中的ACK，所以会重试发送FIN和ACK，所以导致的问题是接收端的相关资源无法释放，文件句柄就是，那极端情况下会导致服务端报Too many open files错误，致使接收端服务不可用
</div>2021-01-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/64/86/f5a9403a.jpg" width="30px"><span>yang</span> 👍（1） 💬（0）<div>哇 老师， 您这里讲的 和 网络编程 那一专栏里讲的部分内容一致诶 难怪我读起那篇文章来没有一点违和感，原来在这里已经阅读过一遍了啊。 
</div>2019-08-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/21/7e/fb725950.jpg" width="30px"><span>罗 乾 林</span> 👍（1） 💬（0）<div>连接在TIME_WAIT状态停留的时间为2倍的MSL。在2MSL等待期间，该端口不能再被使用。</div>2019-08-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/54/cf/fddcf843.jpg" width="30px"><span>芋头</span> 👍（0） 💬（0）<div>不知道老师还看不看这里的评论，最近两家公司都是频繁遇到connection reset &#47; connection reset peer的问题，看了老师的解释，明白了原因，但是找不到解决方案，服务也没有问题，线上远程调用频繁出现这样的问题，服务很不稳定，排查不出来原因，有看到评论的大神，能一起讨论一下解决方案不</div>2023-04-04</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTJJ6G2xZvNRmhyXBjmGbI5G8icGCCMPupr6yxZ1IcURwp7GTRHcpWGWpg9A0fLlyicmVdDwzqZqwiaOQ/132" width="30px"><span>jy</span> 👍（0） 💬（0）<div>请问：

java.net.SocketException: Socket is closed

和
java.net.SocketException: Broken pipe


如何分析解决呢？谢谢老师</div>2022-06-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/3b/ad/31193b83.jpg" width="30px"><span>孙志强</span> 👍（0） 💬（0）<div>建立的tcp连接数超过maxConnection,服务就不是很健康了吧？我有一次出现一个情况是websocket占用了大量的tcp连接，导致http请求非常慢</div>2020-04-01</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/5f/27/a6873bc9.jpg" width="30px"><span>我知道了嗯</span> 👍（0） 💬（0）<div>老师，目前我们线上环境在高峰会出现一种报错（与一个远程主机断开连接），然后用户页面就无法支付，没有响应。这是什么原因，我用工具发现线程都是阻塞状态，是不是因为gc了？</div>2020-01-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/b3/c5/7fc124e2.jpg" width="30px"><span>Liam</span> 👍（0） 💬（0）<div>time_waited过多会占用大量内存资源mbufs, 导致其他活跃连接无资源可用，拖慢了其他连接</div>2019-08-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/b3/c5/7fc124e2.jpg" width="30px"><span>Liam</span> 👍（0） 💬（0）<div>time_waited过多会占有大量内存资源mbufs),;&#47;</div>2019-08-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/64/86/f5a9403a.jpg" width="30px"><span>yang</span> 👍（0） 💬（1）<div>老师 我问一个和今天讲的不相关的问题

分布式系统里面可以使用多种不同的队列应用于不同的业务场景吗？

分布式系统里面可以使用不用属性的分布式锁应用于不同的业务场景吗？ </div>2019-08-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/1e/3a/5b21c01c.jpg" width="30px"><span>nightmare</span> 👍（0） 💬（1）<div>timewait是由于什么原因引起的，tcp四次挥手的哪一个阶段？</div>2019-08-08</li><br/>
</ul>