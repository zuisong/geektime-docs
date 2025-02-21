在上一篇[《12 | RTCPeerConnection：音视频实时通讯的核心》](https://time.geekbang.org/column/article/116324)一文中，我向你介绍了RTCPeerConnection 对象是如何在端与端之间建立连接的，以及音视频数据又是如何通过它进行传输的。而本文则更进一步，向你介绍如何使用 RTCPeerConnection 来控制音视频数据的传输速率。

通过 RTCPeerConnection 进行传输速率的控制实际上还是蛮简单的一件事儿，但在学习相关知识的时候，你不仅要能知其然，还要知其所以然。对于本文来讲，就是你不但要学习如何控制传输速率，同时还应该清楚为什么要对传输速率进行控制。

其实，之所以要进行传输速率的控制，是因为它会对**音视频服务质量**产生比较大的影响，对于音视频服务质量这部分知识，接下来我就与你一起做详细探讨。

## 在WebRTC处理过程中的位置

在此之前，我们依旧先来看看本文的内容在整个 WebRTC 处理过程中的位置。

![](https://static001.geekbang.org/resource/image/0b/c5/0b56e03ae1ba9bf71da6511e8ffe9bc5.png?wh=1142%2A481)

WebRTC 处理过程图

通过上图你可以知道，本文所讲的内容仍然属于**传输**的范畴。

## 音视频服务质量

像上面所说的，虽然通过 RTCPeerConnection 在端与端之间建立连接后，音视频数据可以互通了，但你还应对传输速率有所控制。之所以要对传输速率进行控制，主要是为了提高音视频服务质量。
<div><strong>精选留言（27）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/11/83/4f/8ea62482.jpg" width="30px"><span>笨小孩</span> 👍（9） 💬（1）<div>因为在传输数据之前是要将原始音视频数据进行压缩的，在同一个 GOP（Group Of Picture）中，除了 I&#47;IDR 帧外，B 帧和 P 帧的数据量是非常小的。
--
是说压缩后会变成gop一个单位吗？这个gop没看懂</div>2020-05-14</li><br/><li><img src="https://wx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTJoNVHqRL5iatEoMgfFAaGFZxD8ic6CicxKI9Facp4bzAkNMAfaduSENlPOafs6dOGawibhNv3V9lVowQ/132" width="30px"><span>SherwinFeng</span> 👍（6） 💬（1）<div>这样理解是不是对的呢？
①码率分为音视频压缩码率和传输控制码率；
②由于网络质量条件是不可控的（物理链路的质量、带宽的大小、传输速率的控制），所以webRTC只能通过对数据进行控制，让单位时间内发送的数据量降下来，那么可以增加音视频压缩码率或降低传输控制码率
增加音视频压缩码率，可以直接对SDP中的sample rate&#47;采样率（就是帧率吗）进行控制以减少数据大小，还可以降低分辨度（这些都是有损压缩，即压缩过程不可逆），这些我们可以主动控制的。
降低传输控制码率，指的是不对源数据进行任何处理，而是强行降低发包速度，这可能会造成严重延迟，因此这个是webRTC自己控制的。

而对于用户来说，我们只要知道通过maxBitrate来控制码率即可</div>2019-11-25</li><br/><li><img src="" width="30px"><span>Geek_91a5bd</span> 👍（2） 💬（1）<div>通过媒体描述字段进行控制，如a=rtpmap:103 ISAC&#47;16000，即是控制音频的采样率=16000</div>2020-11-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/82/42/8b04d489.jpg" width="30px"><span>刘丹</span> 👍（1） 💬（1）<div>senders.forEach( sender =&gt; {
  if(sender &amp;&amp; sender.track.kind === &#39;video&#39;){ &#47;&#47; 找到视频的 sender
      vsender = sender; 
  }
});
如果有多个sender符合 sender.track.kind === &#39;video&#39; ，那么只有最后一个sender被处理？</div>2019-08-13</li><br/><li><img src="" width="30px"><span>Geek_066e6b</span> 👍（0） 💬（1）<div>老师，通过getUserMedia设置的是采集的分辨率，还是编码后的分辨率呢？如果不是编码后分辨率，怎么设置呢？最后，还想咨询下，如果想同时支持上行多条不同分辨率的视频流，我们该怎么去控制呢？</div>2020-06-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/bb/fb/17dc9e8f.jpg" width="30px"><span>Desmond</span> 👍（0） 💬（1）<div>如果涉及到无线传输的话，物理传输带宽变化很快，请问WebRTC有办法测量到当前的物理带宽吗？</div>2020-03-30</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/d3/ba/75f3b73b.jpg" width="30px"><span>Benjamin</span> 👍（0） 💬（1）<div>还是一直好奇 SDP 控制的问题，SDP 协商控制连接完成前就做好了。

在音视频通信中，如何再次使用 SDP 控制呢？断开一次，重新相互投递 offer ？</div>2020-03-25</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/35/0e/88d055d2.jpg" width="30px"><span>李宁</span> 👍（0） 💬（1）<div>老师，请教两个问题：
1、怎么得到当前物理链路质量的信息（丢包率、延迟、抖动）
2、帧率和延迟有没有关系，如果没有关系，是否需要根据当前延迟状况动态调节帧率</div>2020-01-25</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/9c/75/950f00d7.jpg" width="30px"><span>蔡林</span> 👍（0） 💬（1）<div>一对一场景中，二者是通过点到点的方式连接的，中间没有经过服务器的中转对音视频流进行中转，流的质量完全依赖于发送端和接收端本地出口的网络质量，请问老师我的理解对吗？</div>2019-12-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/cf/8b/2b4ef30f.jpg" width="30px"><span>天天</span> 👍（0） 💬（1）<div>码率和压缩码率是同一个概念吗？</div>2019-12-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/2b/6a/3cbf37dc.jpg" width="30px"><span>天一</span> 👍（0） 💬（1）<div>老师，你好 ，代码中的 
	key  : fs.readFileSync(&#39;.&#47;cert&#47;1557605_www.learningrtc.cn.key&#39;),
	cert : fs.readFileSync(&#39;.&#47;cert&#47;1557605_www.learningrtc.cn.pem&#39;) 
这些 key 和 pem 哪里得到？</div>2019-11-06</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/9a/38/f7c979e1.jpg" width="30px"><span>Derek</span> 👍（0） 💬（1）<div>传输信道的充分利用是由webrtc内部控制。但webrtc是否会反馈给应用层，来让应用层调整编码码率，以适应当前的信道状况？如果是，是否就是通过这个maxbitrate参数调节？</div>2019-09-15</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTLOMFSAg7ZEt9UvpyfMgTpZLRY22wGLhAdpU619cpWicBZbsRIWnf6iakFNT1H2iarreqzKAha9VlfPQ/132" width="30px"><span>诸葛亮了</span> 👍（0） 💬（1）<div>怎么样设置能保证接收端的视频分辨率为720p呢？</div>2019-08-20</li><br/><li><img src="" width="30px"><span>tommy_zhang</span> 👍（0） 💬（1）<div>m=video 9 UDP&#47;TLS&#47;RTP&#47;SAVPF 96 97 98 99 100 101 127
c=IN IP4 0.0.0.0
b=AS:500
老师好，在android端我修改SDP,添加了b=AS:500，带宽没有限制住。是什么原因？</div>2019-08-16</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTLOMFSAg7ZEt9UvpyfMgTpZLRY22wGLhAdpU619cpWicBZbsRIWnf6iakFNT1H2iarreqzKAha9VlfPQ/132" width="30px"><span>诸葛亮了</span> 👍（0） 💬（1）<div>怎样能保证分辨率保持不变呢</div>2019-08-16</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/3f/1b/40293181.jpg" width="30px"><span>鼠辈</span> 👍（0） 💬（1）<div>也就是说 1M 带宽实际每秒钟只能传输 128K 个 Byte。应该是125吧</div>2019-08-15</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTLOMFSAg7ZEt9UvpyfMgTpZLRY22wGLhAdpU619cpWicBZbsRIWnf6iakFNT1H2iarreqzKAha9VlfPQ/132" width="30px"><span>诸葛亮了</span> 👍（0） 💬（2）<div>在 3.传输速率 下有这么一句话“当然，如果你的压缩码率本来就很小，比如每秒钟只有 500kb...”。当中的“如果你的压缩码率本来就很小”是不是应该是“如果你的传输码率本来就跟小”啊？</div>2019-08-14</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/sIfDHQxDV6iaanrd8PcdVWZnke6nJmqBOLMx0iazR1yNN3FI6ib7PtXCfzicWcuEwSIqzfqiaFMf7PMYNPiaRibiaFHgcw/132" width="30px"><span>hao11111205</span> 👍（0） 💬（1）<div>通过 SDP 来控制传输速率，是否可以通过修改SDP里的采样率来实现？
</div>2019-08-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/4d/fd/0aa0e39f.jpg" width="30px"><span>许童童</span> 👍（0） 💬（3）<div>能否这样理解，码率越大，视频越清晰。</div>2019-08-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/c7/64/340b60c1.jpg" width="30px"><span>崧阳</span> 👍（0） 💬（0）<div>我们业务上的要求是无论如何也不能降低分辨率，但是允许丢包，请问有办法做到吗？很多时候我能看到qualityLimitationReason 里面有cpu和bandwidth，但是不知道如何禁止自动降低分辨率。</div>2023-08-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/2e/38/4c/d20f8abf.jpg" width="30px"><span>颜</span> 👍（0） 💬（0）<div>【通过上述的方式只能对每一路音视频流进行码率的控制，而不能进行整体的统一控制。所以，如果你的应用同时存在多路音视频流，而你又想控制一个总的码率，就只能一路一路地控制了。】一对一音视频通信时，音频流和视频流是不是独立的，属于两路流？那么通过 sender 的 maxBitrate 控制码率，是同时设置的这两路流吗？
</div>2022-07-02</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/7f/15/b662e9a1.jpg" width="30px"><span>yoli</span> 👍（0） 💬（0）<div>老师您好， 我在使用webrtc的DataChannel 在局域网传输数据时， 最高只可以20M&#47;s.  但是在查看webRtc的相关文档时。即可以实现135M&#47;s.   关于DataChannel 的数据传输， 有哪些方面可以提高数据的传输速率 ？ </div>2022-03-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/04/60/20c6a3f2.jpg" width="30px"><span>expecting</span> 👍（0） 💬（0）<div>音视频压缩码率指的是单位时间内音视频被压缩后的数据大小，或者你可以简单地理解为压缩后每秒的采样率。它与视频的清晰度是成反比的，也就是压缩码率越高，清晰度越低。
这句话有点不理解，既然是压缩后的数据大小，不应该是数据越大视频越清晰吗？那应该是正比关系。</div>2022-02-17</li><br/><li><img src="" width="30px"><span>Geek_6a972c</span> 👍（0） 💬（0）<div>请问下初始码率怎么设置呢，webRtc开始那几秒较为模糊</div>2021-11-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/f2/cd/a2ddcd33.jpg" width="30px"><span>dybai</span> 👍（0） 💬（0）<div>老师你好，我跟一楼的问题类似。降帧率是把整个GOP作为一个整体来降低的，还是只是按照帧的数量来降低的(不区分帧类型)？</div>2021-06-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/d3/ba/75f3b73b.jpg" width="30px"><span>Benjamin</span> 👍（0） 💬（0）<div>其实，可以直观理解一下 WebRTC 的这个机制。

就是你看到视频画面变模糊或者马赛克，就是在控制 sender 端的 压缩码率 被设置高了，质量就降低了。

这个是 WebRTC 本质上去决定的，优先保证实时性。</div>2020-03-25</li><br/><li><img src="" width="30px"><span>tommy_zhang</span> 👍（0） 💬（0）<div>我在android端，在SDP中添加b=AS:500，带宽没有限制住。m=video 9 UDP&#47;TLS&#47;RTP&#47;SAVPF 96 97 98 99 100 101 127
c=IN IP4 0.0.0.0
b=AS:500</div>2019-08-16</li><br/>
</ul>