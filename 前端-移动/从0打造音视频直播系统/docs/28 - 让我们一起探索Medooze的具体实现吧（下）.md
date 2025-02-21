在[上一篇文章](https://time.geekbang.org/column/article/136000)中，我向你介绍了 Medooze 的 SFU 模型、录制回放模型以及推流模型，并且还向你展示了Medooze的架构，以及Medooze核心组件的基本功能等相关方面的知识。通过这些内容，你现在应该已经对Medooze有了一个初步了解了。

不过，那些知识我们是从静态的角度讲解的 Medooze ，而本文我们再从动态的角度来分析一下它。讲解的主要内容包括：WebRTC 终端是如何与 Meooze 建立连接的、数据流是如何流转的，以及Medooze是如何进行异步I/O事件处理的。

## 异步I/O事件模型

异步I/O事件是什么概念呢？你可以把它理解为一个引擎或动力源，这里你可以类比汽车系统来更好地理解这个概念。

汽车的动力源是发动机，发动机供油后会产生动力，然后通过传动系统带动行车系统。同时，发动机会驱动发电机产生电能给蓄电池充电。汽车启动的时候，蓄电池会驱动起动机进行点火。

这里的汽车系统就是一种事件驱动模型，发动机是事件源，驱动整车运行。实际上，Medooze的异步I/O事件模型与汽车系统的模型是很类似的。那接下来，我们就看一下 Medooze 中的异步I/O事件驱动机制：

![](https://static001.geekbang.org/resource/image/7f/6d/7f431dc7ae34e5aa635952b461ec726d.png?wh=540%2A268)

Medooze事件驱动机制图

上面这张图就是Modooze异步 I/O 事件处理机制的整体模型图，通过这张图你可以发现 **poll 就是整个系统的核心**。如果说 EventLoop 是 Medooze 的发动机，那么 EventLoop 中的 poll 就是汽缸，是动力的发源地。
<div><strong>精选留言（6）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/0f/e4/39/a06ade33.jpg" width="30px"><span>极客雷</span> 👍（0） 💬（1）<div>为什么都不用epoll，Janus也是</div>2021-03-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/d2/39/a7edf2b9.jpg" width="30px"><span>Joseph</span> 👍（0） 💬（1）<div>老师介绍的非常仔细，谢谢老师！</div>2019-09-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/1a/e2/f88bf28f.jpg" width="30px"><span>frank</span> 👍（0） 💬（2）<div>重点是介绍libmediaserver.a？mcu不介绍吗？</div>2019-09-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/54/21/8c13a2b4.jpg" width="30px"><span>周龙亭</span> 👍（0） 💬（1）<div>DTLS连接建立过程中，WebRTC客户端是怎么参与的？</div>2019-09-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/18/a4/97/bc269801.jpg" width="30px"><span>良师益友</span> 👍（0） 💬（1）<div>为什么不用epoll呢？</div>2019-09-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/48/0f/6d6cc6c3.jpg" width="30px"><span>正平</span> 👍（1） 💬（0）<div>异步IO触发写时间的时机：

当本端收到对方发送的ACK确认包后 删除了本端的一些数据，或者 socket 的写缓冲区也就是writebuffer 可用空间大于设置的低水位（默认是1B），就会标记fd的 POLLOUT标记，下次epoll或者poll轮询的时候，会返回用户可写事件。</div>2020-05-19</li><br/>
</ul>