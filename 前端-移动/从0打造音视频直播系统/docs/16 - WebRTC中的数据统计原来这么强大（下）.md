在[上一篇文章](https://time.geekbang.org/column/article/118885)中我向你介绍了 WebRTC 可以获得哪些统计信息，以及如何使用 RTCPeerConntction 对象的 getStats 方法获取想要的统计信息。

那本文我们在[上一篇文章](https://time.geekbang.org/column/article/118885)的基础之上，继续对 WebRTC 中的统计信息做进一步的讨论，了解它更为详细的内容。

## 再论 getStats

现在你已经非常清楚，通过 RTCPeerConnection 对象的 getStats 方法可以很轻松地获取到各种统计信息，比如发了多少包、收了多少包、丢了多少包，等等。但实际上对于收发包这块儿的统计还可以从其他方法获取到，即通过 **RTCRtpSender 的 getStats 方法和 RTCRtpReceiver 的 getStats 方法也能获取收发包的统计信息**。

也就是说，除了 RTCPeerConnection 对象有 getStats 方法外，RTCRtpSender 和 RTCRtpReceiver 对象也有 getStats 方法，只不过它们只能获取到与传输相关的统计信息，而RTCPeerConnection还可以获取到其他更多的统计信息。

下面我们就来看一下它们三者之间的区别：

- RTCPeerConnection 对象的 getStats 方法获取的是**所有的统计信息**，除了收发包的统计信息外，还有候选者、证书、编解码器等其他类型的统计信息。
- RTCRtpSender对象的 getStats 方法只统计**与发送相关**的统计信息。
- RTCRtpReceiver对象的 getStats 方法则只统计**与接收相关**的统计信息。
<div><strong>精选留言（7）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/0f/4d/fd/0aa0e39f.jpg" width="30px"><span>许童童</span> 👍（8） 💬（1）<div>思考题：
不会影响准确性，因为每一次传输都是全量的，丢失只会丢失这一次的值，在下一次又会全量带过来。</div>2019-08-20</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTKOCkbWo7KTAUYkTk5sqgOSAdjS51ZH8bTxiaBNLVnIFUOMsicBHRJBoXSOX6sZp5uORE2waGyz3ysw/132" width="30px"><span>npersonal</span> 👍（0） 💬（1）<div>老师，我想获取声音等级，目前web端是从webrtc提供的标准中获取，其他端是根据流去算出来的，我觉得这块性能开销很大。但是从webrtc标准api中获取，发现不同端取到的音量等级精度不一致，pc那边给过来的正常声音大概是0.7这种精度，但是android端给过来的是0.00…这种，这种是什么原因导致</div>2021-05-29</li><br/><li><img src="https://wx.qlogo.cn/mmopen/vi_32/ywSuwVNMKNjRLPMjZmpQOQHWW2usAu8RwRIOlBHaVVU6J3xHdtibgO6FVzYkRIkV50vCr62ia4OwJp07giabiazUGA/132" width="30px"><span>ripple</span> 👍（0） 💬（1）<div>一直对sr和rr不太理解，SR 是发送方发的，记录的是 RTP 流从发送到现在一共发了多少包、发送了多少字节数据，以及丢包率是多少。RR 是接收方发的，记录的是 RTP 流从接收到现在一共收了多少包、多少字节的数据等，实际中，发送方也是接收方的哇，譬如A，B，C三个user，A能收到BC的，B能收到AC的，C能收到AB的，然后拿C举例，收到A和B的RR后，然后和自己的SR对比，发现谁丢包严重，就限制谁？发现假如丢包严重，降低码率应该降低A还是B还是C呢？</div>2020-08-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/d3/ba/75f3b73b.jpg" width="30px"><span>Benjamin</span> 👍（0） 💬（1）<div>李老师，SR 和 RR 这些统计信息，会反馈影响 WebRTC 的通信质量上嘛？</div>2020-03-25</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/d2/8a/57dcd0c7.jpg" width="30px"><span>峰</span> 👍（0） 💬（1）<div>老师还是昨天问题，在Frefix，IE浏览器上是可以播放的，只是Google Chrome上播放一点就报错，提示视频问题或浏览器某些特征不支持，如果真的是视频问题，这种性象，暂时无法理解！</div>2019-08-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/d2/8a/57dcd0c7.jpg" width="30px"><span>峰</span> 👍（0） 💬（1）<div>老师，这个问题你遇到吗，能否帮帮我
Input #0, mov,mp4,m4a,3gp,3g2,mj2, from &#39;F:&#47;mp4&#47;convert&#47;041.mp4&#39;:  Metadata:    major_brand     : isom    minor_version   : 512    compatible_brands: isomiso2avc1mp41    encoder         : Lavf57.76.100  Duration: 00:00:21.04, start: 0.033008, bitrate: 3656 kb&#47;s    Stream #0:0(und): Video: h264 (Main) (avc1 &#47; 0x31637661), yuv420p(tv, bt709), 1920x1080, 3653 kb&#47;s, 29.99 fps, 50 tbr, 15360 tbn, 60 tbc (default)    Metadata:      handler_name    : VideoHandler[h264 @ 00000000028a4d80] Invalid NAL unit 8, skipping.    Last message repeated 3 times[h264 @ 00000000028a4d80] concealing 7569 DC, 7569 AC, 7569 MV errors in P frame[h264 @ 00000000028a4d80] illegal short term buffer state detected[h264 @ 00000000028a4d80] mmco: unref short failure</div>2019-08-21</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTKOCkbWo7KTAUYkTk5sqgOSAdjS51ZH8bTxiaBNLVnIFUOMsicBHRJBoXSOX6sZp5uORE2waGyz3ysw/132" width="30px"><span>npersonal</span> 👍（1） 💬（0）<div>老师，实现语音激励功能webrtc有提供一些支持吗，还是说都是要自己实现（大致思路是不是这样：使用AudioContext去做分析，识别出人声部分，然后去计算人声部分的音量等级去做比较）</div>2021-07-08</li><br/>
</ul>