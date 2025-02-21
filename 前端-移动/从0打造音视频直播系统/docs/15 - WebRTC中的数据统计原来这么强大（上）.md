当你使用WebRTC实现1对1通话后，还有一个非常重要的工作需要做，那就是**实现数据监控**。数据监控对于 WebRTC 来讲，就像是人的眼睛，有了它，你就可以随时了解WebRTC客户端的运转情况。

在WebRTC中可以监控很多方面的数据，比如收了多少包、发了多少包、丢了多少包，以及每路流的流量是多少，这几个是我们平常最关心的。除此之外，WebRTC还能监控目前收到几路流、发送了几路流、视频的宽/高、帧率等这些信息。

有了这些信息，你就可以**评估出目前用户使用的音视频产品的服务质量是好还是坏了**。当发现用户的音视频服务质量比较差时，尤其是网络带宽不足时，可以通过降低视频分辨率、减少视频帧率、关闭视频等策略来调整你的网络状况。

当然，还可以给用户一些友好的提示信息，以增强用户更好的体验。比如说，当发现丢包率较高时，可以给用户一个提示信息，如 “你目前的网络质量较差，建议…”。

如果确实是网络质量较差时，还可以在底层做切换网络链路的尝试，从而使服务质量能有所改善！

## WebRTC都能统计哪些数据

鉴于这些统计信息的重要性，那接下来我们来看一下，在 WebRTC 中都能监控到哪些统计信息。

在WebRTC中可以统计到的信息特别多，按类型大体分为以下几种：
<div><strong>精选留言（7）</strong></div><ul>
<li><img src="https://wx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTJoNVHqRL5iatEoMgfFAaGFZxD8ic6CicxKI9Facp4bzAkNMAfaduSENlPOafs6dOGawibhNv3V9lVowQ/132" width="30px"><span>SherwinFeng</span> 👍（7） 💬（1）<div>具体地说就是，A从B那里获得SR报文，获得其中Report block部分中SSRC（数据源）是自己（A）的接收包（B接收A）情况，可以查看fraction lost&#47;丢包比例字段 也可以查看cumulative number of packet lost字段&#47;总丢包数。</div>2019-11-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/35/0e/88d055d2.jpg" width="30px"><span>李宁</span> 👍（0） 💬（1）<div>老师，STCP数据包是通过信令服务器转发的吗？如果在服务端获取到所有客户端的RR&#47;SR数据包并解析存储下来？</div>2020-01-25</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/4d/fd/0aa0e39f.jpg" width="30px"><span>许童童</span> 👍（0） 💬（1）<div>思考题：两者都有统计数据，通过中间服务器一对比，就知道有没有丢包了。A还可以通过自己重发的包数，大致知道网络情况。</div>2019-08-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/12/ce/a8c8b5e8.jpg" width="30px"><span>Jason</span> 👍（6） 💬（0）<div>思考题：我想老师前面已经给出了答案，RTCP 有两个最重要的报文，RR（Reciever Report）和 SR(Sender Report)。通过这两个报文的交换，各端就知道自己的网络质量到底如何了。</div>2019-08-17</li><br/><li><img src="" width="30px"><span>Geek_530e85</span> 👍（0） 💬（0）<div>老师  请问如何显示传输过程的传输延迟</div>2022-03-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/04/60/20c6a3f2.jpg" width="30px"><span>expecting</span> 👍（0） 💬（0）<div>思考题：
对于接收端，对比inbound-rtp中接收的包总数和remote-outbound-rtp中发送的包总数就可以计算出来
发送端同理。</div>2022-02-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/17/5d/03/ccd169b8.jpg" width="30px"><span>boom shakalaka</span> 👍（0） 💬（0）<div>老师，如何通过getStats()中的bytesReceived去计算bandwidth（带宽）</div>2021-11-18</li><br/>
</ul>