关于通过WebRTC实现多人音视频实时互动的实战，其实我们在[上一篇文章](https://time.geekbang.org/column/article/137836)中已经向你做过详细介绍了，其中包括如何编译Medooze源码、如何将编译出的Medooze SFU进行布署，以及如何去使用等相关的内容。

那么今天我们再从另外一个角度来总结一下 Medooze 是如何实现多人音视频互动的。

下面我们就从以下三个方面向你做一下介绍：

- 首先是多人音视频会议整体结构的讲解，这会让你从整体上了解利用Medooze搭建的流媒体服务器与WebRTC客户端是如何结合到一起运转的；
- 其次再对WebRTC客户端进行说明，你将知道无论是Medooze还是使用其他的流媒体服务器，对于客户端来讲它的处理流程基本是不变的；
- 最后是Medooze服务器的总结，让你了解Medooze各模块是如何协调工作的，实际上这部分知识我们在之前的文章中已经做过介绍了，但为了让你对它有更深刻的认识，这里我们还会从另外一个角度再重新剖析。

## Medooze整体架构

文中接下来这张图清晰地展示了Medooze是如何实现多方通信的，你可以先参考下：

![](https://static001.geekbang.org/resource/image/07/c3/07198d161bdd52309a6aabcb507c99c3.png?wh=1142%2A776)

Medooze多方通信整体结构图

从这张图你可以看到，它主要分成两大部分：**服务端**和**客户端**。下面我们就从这两个方面向你详细描述一下 Medooze 实现多方通信的过程。
<div><strong>精选留言（12）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/12/cb/d5/fab32cf7.jpg" width="30px"><span>卖藥郎</span> 👍（5） 💬（3）<div>老师JAVA系应该挑选哪个框架呀</div>2019-11-16</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1f/13/9a/c9125668.jpg" width="30px"><span>gonbcs</span> 👍（1） 💬（1）<div>老师，多路视频如何区分的？比如在多人视频中，每个人有一个摄像头、一个桌面共享，该如何区分从远端传过来的流是摄像头还是桌面共享？</div>2020-09-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/b4/ea/b3dca4dd.jpg" width="30px"><span>王乐</span> 👍（1） 💬（1）<div>多看几遍，实际操作一下，再结合平时实践才有了深刻理解，老师的总结很不错</div>2019-10-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1f/05/94/e55abef3.jpg" width="30px"><span>Her later</span> 👍（0） 💬（1）<div>那如何解决这个问题呢？解决的办法就是每当有新的用户进来之后，就通过 update 信令通知已经在房间内的所有用户，让它们重新与服务器进行媒体协商。重新协商后，所有老用户就可以收到了新用户的视频流了。

也就是每次重新媒体协商 ，都需要将房间里所有的音视频流和rtcpeerconnection 进行绑定 ？
能不能单独绑定新进来的一个呢 ？ </div>2021-05-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/32/1c/3e3cdad2.jpg" width="30px"><span>Jackson</span> 👍（0） 💬（1）<div>STUN可以不用，DTLS是为了传输安全，通常必须用。</div>2019-12-09</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/DYAIOgq83er5tJHYf1ica9LdMM5Q9BCfwBL7dPibTPwicbHpuGbicAS3MquenIs7x3VNW5ZbuJhYZBwA84ianfedprA/132" width="30px"><span>Geek_bang</span> 👍（0） 💬（2）<div>请问有native的demo嘛？想学习下native是怎么调用的</div>2019-10-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/9f/52/e5e8e80b.jpg" width="30px"><span>阿蒙</span> 👍（0） 💬（1）<div>老师，请问流媒体服务器怎么做压力测试，计算一台服务器支持多少用户，有没有什么方便的工具？</div>2019-10-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/13/8a/40459013.jpg" width="30px"><span>相见恨晚</span> 👍（0） 💬（1）<div>这个多人视频提供可运行代码吗</div>2019-09-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/9a/38/f7c979e1.jpg" width="30px"><span>Derek</span> 👍（0） 💬（1）<div>实现p2p和媒体数据加密传输不是都得用吗？</div>2019-09-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1f/05/94/e55abef3.jpg" width="30px"><span>Her later</span> 👍（1） 💬（0）<div>数据采集到之后，要与之前创建好的 RTCPeerConnection 进行绑定，然后才能通过 RTCPeerConnection 实例创建 Offer&#47;Answer 消息，并与服务器端进行媒体协商；

媒体协商的时候 不一定需要采集音视频数据吧 ，如果某个人进来只是看 ，而不推流 。
或者可以先进行媒体协商 ，将采集到的数据和RTCPeerConnection 进行绑定也是可以的吗 。 
还是采集到数据之后，还需要重新进行媒体协商 。 </div>2021-04-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/2e/38/4c/d20f8abf.jpg" width="30px"><span>颜</span> 👍（0） 💬（0）<div>STUN协议是为了进行身份验证，DTLS是为了实现加密传输，都是实现音视频安全传输的手段，不能少</div>2022-07-03</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/21/10/5e/42f4faf7.jpg" width="30px"><span>天择</span> 👍（0） 💬（0）<div>这篇文章需要反复回顾，总结了从客户端到服务端所有涉及的技术，把零散的知识点串起来了，可以按图索骥，对照之前的文章查缺补漏。</div>2022-01-21</li><br/>
</ul>