你好，我是倪朋飞。

前几节，我们一起学习了文件系统和磁盘 I/O 的工作原理，以及相应的性能分析和优化方法。接下来，我们将进入下一个重要模块—— Linux 的网络子系统。

由于网络处理的流程最复杂，跟我们前面讲到的进程调度、中断处理、内存管理以及 I/O 等都密不可分，所以，我把网络模块作为最后一个资源模块来讲解。

同 CPU、内存以及 I/O 一样，网络也是 Linux 系统最核心的功能。网络是一种把不同计算机或网络设备连接到一起的技术，它本质上是一种进程间通信方式，特别是跨系统的进程间通信，必须要通过网络才能进行。随着高并发、分布式、云计算、微服务等技术的普及，网络的性能也变得越来越重要。

那么，Linux 网络又是怎么工作的呢？又有哪些指标衡量网络的性能呢？接下来的两篇文章，我将带你一起学习 Linux 网络的工作原理和性能指标。

## 网络模型

说到网络，我想你肯定经常提起七层负载均衡、四层负载均衡，或者三层设备、二层设备等等。那么，这里说的二层、三层、四层、七层又都是什么意思呢？

实际上，这些层都来自国际标准化组织制定的**开放式系统互联通信参考模型**（Open System Interconnection Reference Model），简称为 OSI 网络模型。
<div><strong>精选留言（30）</strong></div><ul>
<li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/DYAIOgq83ernR4NKI5tejJAV3HMTF3gszBBUAjkjLO2QYic2gx5dMGelFv4LWibib7CUGexmMcMp5HiaaibmOH3dyHg/132" width="30px"><span>渡渡鸟_linux</span> 👍（97） 💬（9）<div>我结合网络上查阅的资料和文章中的内容，总结了下网卡收发报文的过程，不知道是否正确：
1. 内核分配一个主内存地址段（DMA缓冲区)，网卡设备可以在DMA缓冲区中读写数据
2. 当来了一个网络包，网卡将网络包写入DMA缓冲区，写完后通知CPU产生硬中断
3. 硬中断处理程序锁定当前DMA缓冲区，然后将网络包拷贝到另一块内存区，清空并解锁当前DMA缓冲区，然后通知软中断去处理网络包。
-----
当发送数据包时，与上述相反。链路层将数据包封装完毕后，放入网卡的DMA缓冲区，并调用系统硬中断，通知网卡从缓冲区读取并发送数据。
</div>2019-03-07</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/39/fa/a7edbc72.jpg" width="30px"><span>安排</span> 👍（31） 💬（1）<div>当一个网络帧到达网卡后，网卡会通过 DMA 方式，把这个网络包放到收包队列中；然后通过硬中断，告诉中断处理程序已经收到了网络包。

接着，网卡中断处理程序会为网络帧分配内核数据结构（sk_buff），并将其拷贝到 sk_buff 缓冲区中；然后再通过软中断，通知内核收到了新的网络帧。

接下来，内核协议栈从缓冲区中取出网络帧，并通过网络协议栈，从下到上逐层处理这个网络帧。



老师你好，上面的一段话有些疑问想请教一下。

收包队列是属于哪里的存储空间，是属于物理内存吗，还是网卡中的存储空间，通过dma方式把数据放到收包队列，我猜这个收包队列是物理内存中的空间。这个收包队列是由内核管理的吧，也就是跟某一个进程的用户空间地址没关系？   

那sk_buf缓冲区又是哪里的存储空间，为什么还要把收包队列拷贝到这个缓冲区呢，这个缓冲区是协议栈维护的吗？也属于内核，跟进程的用户空间地址有关系吗？


socket的接收发送缓冲区是映射到进程的用户空间地址的吗？还是由协议栈为每个socket在内核中维护的缓冲区？

还有上面说到的这些缓冲区跟cache和buf有什么关系？会被回收吗？


内核协议栈的运行是通过一个内核线程的方式来运行的吗？是否可以看到这个线程的名字？</div>2019-02-26</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/AkO5s3tJhibth9nelCNdU5qD4J3aEn8OpBhOHluicWgEj1SbcGC6e9rccK8DrfJtRibJT5g6iamfIibt5xX7ketDF6w/132" width="30px"><span>Penn</span> 👍（12） 💬（7）<div>中断不均，连接跟踪打满</div>2019-02-06</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTKq0oQVibKcmYJqmpqaNNQibVgia7EsEgW65LZJIpDZBMc7FyMcs7J1JmFCtp06pY8ibbcpW4ibRtG7Frg/132" width="30px"><span>zhoufeng</span> 👍（8） 💬（2）<div>老师好，一直不太明白skb_buff和sk_buff的区别，这两者有关系吗</div>2019-04-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/92/01/c723d180.jpg" width="30px"><span>饼子</span> 👍（6） 💬（1）<div>遇到了程序分配大量链接，占用完程序最大打开文件数量，使用lsof 查看分析的</div>2019-02-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/4d/fe/882eaf0f.jpg" width="30px"><span>威</span> 👍（4） 💬（2）<div>老师您好，请问最后一张图下方的两个大圈圈代表的是什么意思，是代表loop吗</div>2019-02-06</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/3d/77/45e5e06d.jpg" width="30px"><span>胡鹏</span> 👍（3） 💬（2）<div>我所知道的网络问题，就是服务器被ddos攻击，小规模，可以防，，，大规模防不了</div>2019-03-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/5b/ae/3d639ea4.jpg" width="30px"><span>佳</span> 👍（3） 💬（1）<div>使用InfiniBand网卡和InfiniBand交换机的时候， mtu如果配置65520的时候，通过http下载对象存储小文件比较慢，但是配置9000的时候大小文件都比较快。https:&#47;&#47;github.com&#47;antirez&#47;redis&#47;issues&#47;2385 Redis works very slow with MTU higher than packet size. 请问老师是什么原因
</div>2019-02-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/61/14/2f9fec68.jpg" width="30px"><span>空空</span> 👍（3） 💬（2）<div>老师过年好！
曾经在Linux3.10测试netlink收发包效率，发现一个问题，正常情况下每收一个包大概需要10us，但是每隔8秒会出现一次收包时间30-50ms，就是因为固定间隔8秒会出现一次收包时间过长，导致收包效率降低。请教一下老师每隔8秒系统会做什么？或者是因为什么系统配置？希望老师解答一下疑惑，谢谢！</div>2019-02-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/0c/d2/381c75f5.jpg" width="30px"><span>道无涯</span> 👍（3） 💬（1）<div>本机有两张网卡，如果路由配成第二张网卡也走第一张网卡，会不会导致第二张网络收不到数据？</div>2019-02-06</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/fa/b4/6892eabe.jpg" width="30px"><span>Geek_33409b</span> 👍（3） 💬（1）<div>系统出口带宽被打满，导致大量请求超时</div>2019-02-06</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/83/69/77256c74.jpg" width="30px"><span>空白</span> 👍（2） 💬（1）<div>一直不太理解，网络包是如何具体交付给对应的线程的？</div>2019-07-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/89/46/ff27e90f.jpg" width="30px"><span>Geek_gthxw2</span> 👍（2） 💬（1）<div>请问老师环回接口的收发包也是和正常网卡接口一样的吗？</div>2019-03-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/64/05/6989dce6.jpg" width="30px"><span>我来也</span> 👍（2） 💬（2）<div>[D33打卡]
可能是公司业务规模不大，峰值带宽未超过100m。以前遇到的网络性能问题不太多，现在都是云服务器了，理论上出口带宽可以动态调整，遇到的问题就更少了。
但自从阿里云切到腾讯云后，还真遇到了一个对我来说无解的网络问题。
云服务器控制台经常提示带宽已达峰值，但上控制台观察，只能查到最小粒度10s的流量图，而服务器上只能看到内网ip，并未有单独的外网ip，就是说在服务器上用工具观察到的流量是内外+外网的流量总和。而内网流量又不能砍掉，也无法预估流量大小。
最后就很尴尬了，以我用iftop的分析结果来看，流量应该是未超，但控制台说超了被限制了，也无法核对数据。</div>2019-02-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/5f/28/17ed19bc.jpg" width="30px"><span>J</span> 👍（2） 💬（1）<div>先拜年，再问问题:)。好多时候性能问题是由于网络造成的，后续应该有些相关案例分析吧。
从centos7.4升级到7.5之后，网卡busy-poll: off 被设置成off了。如果用tuned-profile network-latency,
就会有很大的性能下降。必须把里面的net.core.busy_read net.core.busy_poll 设置为0关闭。不太明白这个内核变化的原因以及性能下降的原因。</div>2019-02-07</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/04/8a/ff94bd60.jpg" width="30px"><span>涛涛</span> 👍（1） 💬（2）<div>接受网络包的时候，数据拷贝了好几次，所以后来有了零拷贝？</div>2019-04-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/86/fa/4bcd7365.jpg" width="30px"><span>玉剑冰锋</span> 👍（1） 💬（1）<div>您好老师，IP包分片，一个IP包分成多个分片，是如何保证接收方收一个完整的数据包的？</div>2019-02-15</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/57/6e/b6795c44.jpg" width="30px"><span>夜空中最亮的星</span> 👍（1） 💬（1）<div>新年好，给老师拜个晚年，过年的课都落下了，抓紧时间赶上来。</div>2019-02-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/c8/74/a1bd2307.jpg" width="30px"><span>vvccoe</span> 👍（1） 💬（4）<div>老师，新年快乐。
之前忘了在哪里读的，关于分片的说法，和你在文章中的说法，有一点差异，如果是TCP连接，在三次握手中的前两次会带一个MSS值，MSS值来表示接收单包最大量，MSS值根据MTU计算出来。以避免在IP层分片，IP层分片的缺点在于如果丢失一个包，会导致所有分片包重传。
如果在中间路由出现MTU过小的情况，会重新协商MSS值，总之TCP的连接不会用IP层来分片，不知道对否？</div>2019-02-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/61/5b/9ad27865.jpg" width="30px"><span>sTone</span> 👍（0） 💬（1）<div>互联网是按ip寻址还是mac?</div>2019-05-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/69/88/528442b0.jpg" width="30px"><span>Dale</span> 👍（20） 💬（7）<div>网络报文传需要在用户态和内核态来回切换，导致性能下降。业界使用零拷贝或intel的dpdk来提高性能。</div>2019-02-12</li><br/><li><img src="https://wx.qlogo.cn/mmopen/vi_32/PiajxSqBRaEKQMM4m7NHuicr55aRiblTSEWIYe0QqbpyHweaoAbG7j2v7UUElqqeP3Ihrm3UfDPDRb1Hv8LvPwXqA/132" width="30px"><span>ninuxer</span> 👍（11） 💬（1）<div>打卡day35
有一次业务反馈有些请求无法正常响应，后来花了两天时间才发现ifconfig看网卡的drop的包不断增长，后来发现是跟开启了内核的timestamp参数有关</div>2019-02-13</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTJUP6ibuQssqJBNtQdSaFNhzzibdf7I3nyVGCeJPoDYqfsRndqRY19GpOJCOibMXQmOv2EchtHh0SXow/132" width="30px"><span>Geek_00d753</span> 👍（5） 💬（5）<div>收数据的时候，从网卡到应用层socket。需要一次硬中断+一次软中断。
发数据的时候只需要一次软中断。
是这样吗？老师</div>2019-03-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1d/63/a9/abed781e.jpg" width="30px"><span>李維道</span> 👍（2） 💬（0）<div>专有名词请附上英文原文，实在没办法看懂中文名词在描述什么</div>2022-10-16</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/4d/fe/abb7bfe3.jpg" width="30px"><span>bd7xzz</span> 👍（1） 💬（1）<div>1.有大量的zerowindow返回，拥塞控制了
2.抖动重传，重传的耗时很高，因为keepalive时间长
3.端口耗尽，导致内核建链循环遍历可用端口时很慢
4.ringbuff满丢弃，ifconfig可以看到
5.irqbalance关闭，且进程绑核，导致处理包慢</div>2023-04-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/12/f9/7e6e3ac6.jpg" width="30px"><span>Geek_04e22a</span> 👍（1） 💬（0）<div>网关机器带宽被打满，查看发送机器有TCP重传</div>2020-08-24</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/CV9kk5M26pdIuAxwdXvj90ewKECzdSmzO4ibP6iaLXY50hICibefmib4qGvu1wCSfXuRobFC86z7W3OcfncpV8Uevw/132" width="30px"><span>Geek_25565b</span> 👍（1） 💬（1）<div>老师好，netstat 执行一次 Recv-Q 和Send-Q 有值就说明堆积吗？还是用watch 看变化情况确定堆积？</div>2019-08-02</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/da/6a/91bd13de.jpg" width="30px"><span>张挺</span> 👍（1） 💬（0）<div>您好，请问，数据从网卡到应用程序或者应用程序到网卡，都会同时触发硬中断和软中断吗？</div>2019-03-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/26/af/73/6bc60f7a.jpg" width="30px"><span>爱丽包°</span> 👍（0） 💬（0）<div>老师，不太明白网络协议栈和内核协议栈有什么关联和区别</div>2022-04-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/18/dc/49/43ae1627.jpg" width="30px"><span>Ansyear</span> 👍（0） 💬（0）<div>学过网络的就会觉得这张比较简单了</div>2021-10-17</li><br/>
</ul>