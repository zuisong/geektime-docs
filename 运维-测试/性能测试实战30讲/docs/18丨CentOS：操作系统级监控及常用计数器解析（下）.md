在上一篇文章中，我们已经讲了监控系统层面的分析思路以及CPU分析，今天我们分析一下操作系统中其他的层面。

首先是I/O。

## I/O

I/O其实是挺复杂的一个逻辑，但我们今天只说在做性能分析的时候，应该如何定位问题。

对性能优化比较有经验的人（或者说见过世面比较多的人）都会知道，当一个系统调到非常精致的程度时，基本上会卡在两个环节上，对计算密集型的应用来说，会卡在CPU上；对I/O密集型的应用来说，瓶颈会卡在I/O上。

我们对I/O的判断逻辑关系是什么呢？

我们先画一个I/O基本的逻辑过程。我们很多人嘴上说I/O，其实脑子里想的都是Disk I/O，但实际上一个数据要想写到磁盘当中，没那么容易，步骤并不简单。

![](https://static001.geekbang.org/resource/image/0b/0c/0b8dd1fa8ddda518e666546205d9170c.jpg?wh=1632%2A1729)

这个简化的图是思虑再三的结果。

I/O有很多原理细节，那我们如何能快速地做出相应的判断呢？首先要祭出的一个工具就是`iostat`。

![](https://static001.geekbang.org/resource/image/b8/31/b8de645585fa5804e26929c88c579031.png?wh=720%2A405)

在这张图中，我们取出一条数据来做详细看下：

```
Device:   rrqm/s   wrqm/s     r/s     w/s    rkB/s    wkB/s  avgrq-sz 
vda        0.00     0.67   18.33  114.33   540.00 54073.33   823.32
avgqu-sz   await r_await w_await  svctm  %util
127.01  776.75    1.76  901.01   7.54 100.00 
```

我解释一下其中几个关键计数器的含义。

`svctm`代表I/O平均响应时间。请注意，这个计数器，有很多人还把它当个宝一样，实际上在man手册中已经明确说了：“Warning! Do not trust this field any more. This field will be removed in a future sysstat version.” 也就是说，这个数据你爱看就爱，不一定准。
<div><strong>精选留言（24）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/14/20/1d/0c1a184c.jpg" width="30px"><span>罗辑思维</span> 👍（21） 💬（2）<div>当操作系统中配置了vm.swappiness是 30%，那么当内存用到1-30%=70%的时候，就会发生 Swap。

高老师，文中对swappiness参数设置值描述跟倪鹏飞老师在专栏讲解有不一样的地方。个人还是认同swappiness不是内存的百分比。下面这段是摘自是倪鹏飞老师《Linux性能分析实战》第19讲。
---------------------------
&#47;proc&#47;sys&#47;vm&#47;swappiness 选项，用来调整使用 Swap 的积极程度。
swappiness 的范围是 0-100，数值越大，越积极使用 Swap，也就是更倾向于回收匿名页；数值越小，越消极使用 Swap，也就是更倾向于回收文件页。
虽然 swappiness 的范围是 0-100，不过要注意，这并不是内存的百分比，而是调整 Swap 积极程度的权重，即使你把它设置成 0，当剩余内存 + 文件页小于页高阈值时，还是会发生 Swap。</div>2020-04-05</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/22/58/eb/963ea7fe.jpg" width="30px"><span>木剑温华</span> 👍（9） 💬（1）<div>一个 TCP 连接大概占 3KB，创建 10 万个连接，才100000x3KB≈300M左右，何况最多才 65535 呢？服务器有那么穷吗？
这里感觉老师说的有一点问题，一个tcp链接由四元组组成：sip：sport---cip：cport，单机最多65535个端口，但是可以根据公式可以看到只影响了sport的数量，但是cip和cport的组合是无穷尽的，所以单机理论最大连接数远大于65535，我之前在iot项目和消息推送项目做过相关的压测，成功地把单机最大长连接数提高到100w以上。</div>2021-08-31</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/7e/3e/82202cc8.jpg" width="30px"><span>月亮和六便士</span> 👍（4） 💬（1）<div>高老师，看完您的课程，有一些思路了，但是我发现思路和实战之间有一道鸿沟，我已经掉到沟里了，比如 分析的起点拆分响应时间，但是不知道怎么拆分，开发更是一头雾水。应用又是部署在docker里面，好不容易配置了个Tomcat监控，结果重启了一下配置又没了，运维说docker里没法暴露监控端口，真是寸步难行啊</div>2020-03-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/44/b0/c196c056.jpg" width="30px"><span>SeaYang</span> 👍（3） 💬（1）<div>使用Linux服务器作为压力机，TPS达到比较高的时候压力机会大量报无法分配请求地址的错误，从而导致TPS直接降为0，命令看了下TIME_WAIT的数量很多，调整了一下几个内核参数，就解决了</div>2020-10-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/1d/de/62bfa83f.jpg" width="30px"><span>aoe</span> 👍（3） 💬（1）<div>老师硬核调优！测试、开发、运维后期在操作系统、网络上都这么强了！</div>2020-10-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/e3/b3/d8bdddad.jpg" width="30px"><span>黑脸龙猫酱</span> 👍（3） 💬（1）<div>老师可否说下对于云服务器，io有些时间段不稳定的情况应该如何处理？</div>2020-03-16</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/2f/f4/2dede51a.jpg" width="30px"><span>小老鼠</span> 👍（3） 💬（1）<div>由于上下文切换过多引起性能降低的情形多吗？</div>2020-02-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1b/41/44/00ea2279.jpg" width="30px"><span>悦霖</span> 👍（2） 💬（1）<div>高老师问一下，每次性能测试看io较高基本都是jbd2这个进程占用大量的IO，怎么进一步分析，而且这个jdb2是个啥？</div>2020-02-18</li><br/><li><img src="" width="30px"><span>Geek_6add55</span> 👍（1） 💬（1）<div>老师你好，netstat命令Recv_Q和Send_Q的值显示的是环形缓冲区的队列还是套接字缓冲区的队列</div>2023-06-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1d/4b/1e/107db99f.jpg" width="30px"><span>闲鱼超人</span> 👍（1） 💬（1）<div>监控平台为什么不重要呢？
监控平台的主要用途是为了提供运行时状态数据给我们的，利用这些数据，我们分析性能情况。所以关键是数据、是证据链，是这些数据反馈出来的问题，这是核心。所以从这个角度来说，监控平台是不重要的，因为只要能提供这些你需要的数据，哪个平台都可以。</div>2021-02-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/de/d4/b83c4185.jpg" width="30px"><span>David.cui</span> 👍（1） 💬（1）<div>高老师讲的还是很透彻的，能分析到非常细微的差别。
高手！</div>2020-12-03</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTJJ6G2xZvNRmhyXBjmGbI5G8icGCCMPupr6yxZ1IcURwp7GTRHcpWGWpg9A0fLlyicmVdDwzqZqwiaOQ/132" width="30px"><span>jy</span> 👍（0） 💬（1）<div>老师，请教一个问题，
文中：&quot;在我们做性能分析的过程中，基本上，基于上面这个表格就够通过接收和发送判断瓶颈点发生在谁身上了&quot;

感觉这里没说完整呢

比如发送端Send_Q有值，接收端Recv_Q也有值，说明瓶颈点在接收端，那下一步如何分析接收端呢？
比如发送端Send_Q有值，接收端Recv_Q没有值，说明瓶颈点在发送端或者网络设备，这种情况，那下一步又该如何分析发送端呢？

谢谢老师指导。</div>2022-10-21</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTKfbvRdpx6zMkyHc6t5BdP2TN6sZic29MHmt5TwHHt1ksvPAiaSqVgRVwljBchH1lcX4iaxeXzaTP8fw/132" width="30px"><span>Fzz</span> 👍（0） 💬（2）<div>老师你好，想问下系统tps到顶，系统CPU只有20%，系统相响应时间1秒以下，感觉压力发起端也没有瓶颈，想问下这个瓶颈在哪？看了资源的使用也不高，不知道是不是jvm或者应用的的问题？</div>2022-06-13</li><br/><li><img src="" width="30px"><span>学员141</span> 👍（0） 💬（2）<div>在测试环境压测，发现服务器端口占满了，服务器的端口配置是否需要修改？网上说过大又容易被攻击（我们是docker，一个节点上部署了18个应用，节点主机16C16G，有些应用CPU和内存都分配很小，导致都到一个节点上来）</div>2021-07-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1e/0b/c9/b53037df.jpg" width="30px"><span>0909</span> 👍（0） 💬（1）<div>因为数据来源都是一样的，重要的还是要根据数据去找到瓶颈和优化方案</div>2021-06-21</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTJlkFFx4N8ice8UcQRu3AMP0QAXdib17lyFI8G6QLje9iaumOXhsNq50PyLowAwg0umho89o1amN2UGQ/132" width="30px"><span>Geek_7cf52a</span> 👍（0） 💬（1）<div>老师我之前说的端口不够用的问题我知道了，听了音频知道老师说的客户端的端口了，不是服务端的，刚开始还以为是服务端的端口</div>2020-07-10</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTJlkFFx4N8ice8UcQRu3AMP0QAXdib17lyFI8G6QLje9iaumOXhsNq50PyLowAwg0umho89o1amN2UGQ/132" width="30px"><span>Geek_7cf52a</span> 👍（0） 💬（1）<div>至于为什么要处理TIME_WAIT，却没几个人能回答得上来。在我的性能工作经验中，只有一种情况要处理TIME_WAIT，那就是端口不够用的时候。TCP&#47;IPv4的标准中，端口最大是 65535，还有一些被用了的，所以当我们做压力测试的时候，有些应用由于响应时间非常快，端口就会不够用，这时我们去处理TIME_WAIT的端口，让它复用或尽快释放掉，以支持更多的压力。所以处理TIME_WAIT的端口要先判断清楚，如果是其他原因导致的，即使你处理了TIME_WAIT，也没有提升性能的希望。如果还有人说，还有一种情况，就是内存不够用。我必须得说，那是我没见过世面了，我至今没见过因为TIME_WAIT的连接数把内存耗光了的。一个 TCP 连接大概占 3KB，创建 10 万个连接，才100000x3KB≈300M左右，何况最多才 65535 呢？服务器有那么穷吗？
-----来自原文
老师你好，你上面说的端口不够用的时候处理time_wait是不是有问题？应该是连接不够用才对吧？一个应用在一开始就指定了具体的tcp端口，端口是不会变的，只有连接数才会不断的增多</div>2020-07-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/3f/39/a4c2154b.jpg" width="30px"><span>小昭</span> 👍（0） 💬（1）<div>今日思考题
为什么说用什么监控平台并不重要呢？
监控平台再花哨，都只是提供数据来给性能测试人员分析的。作为性能测试人员，重点是要知道数据的来源、原理、含义。

知易行难，信息量好大。一节课够学一个月系列……</div>2020-04-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/7e/3e/82202cc8.jpg" width="30px"><span>月亮和六便士</span> 👍（0） 💬（1）<div>老师，怎么查看端口够用不够用，或者说端口用了多少？Linux系统的命令是什么，window系统的命令是什么？</div>2020-04-07</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1a/9f/c2/3d1c2f88.jpg" width="30px"><span>蔡森冉</span> 👍（0） 💬（1）<div>平台就像是每个人用着不同品牌手机都用着差不多的功能。老师现在使用着云平台，平台上就会有一个监控模块，公司应用都是在云服务器上，那是否我只用在服务器提供商上的这个监控模块看就可以了？</div>2020-03-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/2f/f4/2dede51a.jpg" width="30px"><span>小老鼠</span> 👍（0） 💬（1）<div>在固态硬盘中还存在扇区与磁道吗？</div>2020-02-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1b/42/84/e0a6fc1c.jpg" width="30px"><span>wjh</span> 👍（0） 💬（1）<div>测试某场景的时候，发现该场景的network出入都非常少，但其他场景又都正常（同一服务器），请问高老师，这种情况的分析思路是怎么样的？明显不是带宽不够，那还有设么其他原因呢？</div>2020-02-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/d4/84/7f584cb2.jpg" width="30px"><span>杜艳</span> 👍（0） 💬（1）<div>对于基础差的人，这一块就看不懂了，对于这些命令需要去哪里输入都不知道，请问怎么入手补习这块知识</div>2020-02-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/bc/25/1c92a90c.jpg" width="30px"><span>tt</span> 👍（0） 💬（2）<div>我们用的是REDHAT，WAS挂过几次，IBM的人说要给他们的实验室分析以下，下次我用dmesg命令看看。</div>2020-02-04</li><br/>
</ul>