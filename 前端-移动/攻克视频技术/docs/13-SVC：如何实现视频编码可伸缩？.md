你好，我是李江。

前面我们用了4节课的时间分别讲述了如何将视频编码码流打包成H264，如何预测网络带宽，如何做好码控来控制视频发送的速率，如何分析视频的花屏和卡顿等问题。基本上循序渐进地将视频传输中最重要的一些知识点都讲解了一遍，并对里面几个重要的算法进行了深入的研究。

今天，我们再讲述一个视频会议场景中经常会使用的视频编码传输相关的技术——SVC编码，也叫做可伸缩视频编码。它的作用是可以实现在一个码流里面包含多个可解码的子码流，服务器可以根据接收端的网络状况，下发对应码率的码流，从而实现可伸缩性。

## 为什么需要SVC

2020年全球爆发新冠疫情，很多公司为了员工的安全，实行在家办公的政策。视频会议一时成为了工作中必不可少的日常工作活动。很多大型公司可能会出现一次几十、上百个人参加视频会议的情况。对于视频会议技术商来说，如何提供几十、上百个人的高质量视频通话技术是一个难题。为什么呢？

比如说，我和你两个人进行视频通话，我是发送端，网络非常好，你是接收端，网络比较差。发送端和接收端之间的视频通路如下图所示：

![图片](https://static001.geekbang.org/resource/image/bb/d2/bb477d3a740c1b5a4a9c41e33c1043d2.jpeg?wh=1920x620)

在[带宽预测](https://time.geekbang.org/column/article/467073)这节课里面我们讲过，由于服务器到接收端的网络比较差，那么最后会引起：

- 一组视频RTP包的接收时长很长，而一组视频RTP包的发送时长比较小；
- 或者发送端的视频RTP包发送给接收端之后，网络中丢包率很高。
<div><strong>精选留言（8）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/23/ec/8a/4de35fb7.jpg" width="30px"><span>paradise</span> 👍（1） 💬（1）<div>江哥，问一下，就是svc 编码采用rtp 包封装的形式，实际编码器出来的是普通码流，那这个码流是如何进行rtp svc 封装呢？ 是编码器提前设置好svc 的参考关系，然后从收到第一个I帧开始后就自动更新rtp 包里关于封装svc 编码的相关字段信息吗？</div>2021-12-24</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/Ikib5hH6AA9v1kJWp14ImL99HSv9XRmURK0IiaLAjm51dYbjicsgyXWwud3KjdweGtyd1SelMNb2HIsj9nzcAS0Sw/132" width="30px"><span>Geek_7de4c5</span> 👍（1） 💬（1）<div>如果是发送端网络不好，时域svc就失效了，有什么好的手段吗？</div>2021-12-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/54/20/abb7bfe3.jpg" width="30px"><span>Geek_wad2tx</span> 👍（1） 💬（2）<div>SVC开始是否有前提，当接收端的方差达到某个阈值时在开启，或者发送端本身发送的帧率或者码率对网络要求很低，例如500k就可以，这时不启用SVC，可以更进一步增加压缩率。</div>2021-12-20</li><br/><li><img src="https://wx.qlogo.cn/mmopen/vi_32/ywSuwVNMKNjRLPMjZmpQOQHWW2usAu8RwRIOlBHaVVU6J3xHdtibgO6FVzYkRIkV50vCr62ia4OwJp07giabiazUGA/132" width="30px"><span>ripple</span> 👍（0） 💬（1）<div>你好，请问下如果是硬编码，svc有相关的处理方式不？</div>2022-03-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/2b/8a/7a/df91459b.jpg" width="30px"><span>Leo-J</span> 👍（0） 💬（2）<div>老师，这是不是直播推流原理？直播端高质量，观众段可选质量？</div>2022-03-02</li><br/><li><img src="https://wx.qlogo.cn/mmopen/vi_32/ywSuwVNMKNjRLPMjZmpQOQHWW2usAu8RwRIOlBHaVVU6J3xHdtibgO6FVzYkRIkV50vCr62ia4OwJp07giabiazUGA/132" width="30px"><span>ripple</span> 👍（0） 💬（1）<div>simulcast是不是更常用些？</div>2021-12-20</li><br/><li><img src="" width="30px"><span>龚长华</span> 👍（0） 💬（0）<div>FEC, Transport-CC, 丢包重传， 关键帧重传， SVC</div>2022-06-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/43/61/eeefa369.jpg" width="30px"><span>tony</span> 👍（0） 💬（1）<div>如果使用x264实现时域svc,设置参考帧的大概思路是怎样的？谢谢。</div>2022-01-09</li><br/>
</ul>