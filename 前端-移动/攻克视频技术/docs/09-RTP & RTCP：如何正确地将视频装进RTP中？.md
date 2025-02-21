你好，我是李江。

在前面的课程中，我们详细地讲述了视频编码的原理以及预测编码和变换编码的知识。通过这些我们了解了视频编码的基本原理和步骤。同时，我们还用了一节课的时间深入探讨了H264的码流结构，相信你已经清楚了H264码流是什么样的，以及如何从码流中分离出一帧帧图像数据，并学会了如何判断这些帧的类型。

那么从这节课开始呢，我们就要进入视频传输和网络对抗部分了。我们会在视频编码码流的基础上，讲讲如何将码流打包成一个个数据包发送到网络上，并进一步讨论如何避免在发送的过程中引起网络拥塞，从而保证视频的流畅性。同时，我们会进一步在后面的课程中讲解如何在网络不断变化的时候做好视频码控算法，如何防止视频出现花屏，以及如何尽量减少视频卡顿等非常有难度的实际工程问题。

这些问题是视频开发过程中经常会遇到且迫切需要解决的重要问题。而解决这些问题的基础就是需要熟悉RTP和RTCP协议，也就是我们这节课的重点。

接下来我们会分别从RTP协议、RTCP协议和H264的RTP打包方法这三个方面来展开这节课。首先让我们一起来认识一下RTP协议。

## RTP协议

RTP（Real-time Transport Protocol）协议，全称是实时传输协议。它主要用于音视频数据的传输。那它的作用是什么呢？
<div><strong>精选留言（14）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/10/3a/56/96aa5869.jpg" width="30px"><span>狂奔的带刀蜗牛</span> 👍（11） 💬（5）<div>
不超过1500主要是因为Udp协议的MTU为1500，超过了会导致Udp分片传输，而分片的缺点是丢了一个片，整包数据就废弃了</div>2021-12-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/20/b4/7d/9455f31a.jpg" width="30px"><span>我有一条鱼</span> 👍（3） 💬（2）<div>想问一下RTCP协议如果也是基于UDP协议的话，怎么保证统计信息是正确的呢？所以RTCP是不是应该具体TCP协议？</div>2022-01-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1d/ef/3c/673826c1.jpg" width="30px"><span>木希</span> 👍（3） 💬（6）<div>江哥，您这课程介绍的视频技术原理性都很详细，可以很好的理解视频原理性的东西，后面是否会带上部分代码逻辑的实现，原理跟实现还是有很长的路。</div>2021-12-10</li><br/><li><img src="" width="30px"><span>Geek_b8aa7b</span> 👍（2） 💬（1）<div>rtp和rtcp是基于udp的，上面也提到实时场景一般用udp，但为什么rtmp是基于tcp的，我看很多音视频传输是基于rtmp的，不是说tcp会延时嘛？</div>2021-12-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/31/a3/15/6d99cf21.jpg" width="30px"><span>louie</span> 👍（0） 💬（1）<div>rtp 打包音频数据是怎么打包的呢，rtp 协议中如何和视频区分，两者一起传输的时候是怎么传输呢</div>2023-07-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/2b/8a/8a/2aa0e992.jpg" width="30px"><span>weekend</span> 👍（0） 💬（1）<div>好像没有讲RTMP相关的，RTMP的区别是什么</div>2022-03-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1c/f2/bc/ffc7ad67.jpg" width="30px"><span>Chris Zou</span> 👍（0） 💬（1）<div>老师，结合jitterbuffer那章来看，对于FU-A封包，一个NALU单元对应一个slice，一帧数据是有可能对应多个slice，也就是NALUT单元，每个slice都会有一次S起始位和E终止位？</div>2022-01-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/f1/f4/707b7877.jpg" width="30px"><span>王夏望</span> 👍（0） 💬（2）<div>请问对于不同帧，rtp包中的timestamp的差值是固定的还是变化的？</div>2021-12-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/54/20/abb7bfe3.jpg" width="30px"><span>Geek_wad2tx</span> 👍（3） 💬（0）<div>记录下从视频从编码到传输分别经历了哪些格式：

一段视频 -&gt;由多个Frame组成（I，B，P）
一个Frame -&gt; 分为多个Slice
一个Slice -&gt; 由多个MB组成

编码：
Slice编码 -&gt; MB分析 -&gt; 熵编码 -&gt;封装NALU

传输：
NALU -&gt; 由一个或多个RTP包组装传输
</div>2022-02-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/35/5e/7a584fed.jpg" width="30px"><span>accessory</span> 👍（1） 💬（1）<div>请问，RTP 头中的 16 位 sequence number 起始值为什么是随机的？ 2 字节的能表示的范围是 [0, 2^16-1],超出这个范围后 sequence number 怎么处理，是从 0 重新开始，还是换一个随机数？</div>2022-04-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1d/9a/89/babe8b52.jpg" width="30px"><span>A君</span> 👍（1） 💬（0）<div>预测帧经过编码后需要封装进RTP包才能发送，因为接收方要知道码流是使用哪种编码以及播放速度是多少等信息。RTP包没有丢包重传和拥塞控制，RTCP通过发送RTP记录来统计已接受包信息，用户可以根据这些信息来自己实现丢包重传。RTP也会根据码流大小采用单包或分片的格式来封装包。</div>2022-04-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1f/05/63/dd59ad18.jpg" width="30px"><span>加油加油</span> 👍（0） 💬（0）<div>老师能补充讲讲     rtp&#47;rtsp    在tcp中的组织实现方式吗？</div>2022-07-06</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1f/05/63/dd59ad18.jpg" width="30px"><span>加油加油</span> 👍（0） 💬（0）<div>rtsp header中的mark是不是也是表示当前帧数据的结束？</div>2022-07-05</li><br/><li><img src="" width="30px"><span>龚长华</span> 👍（0） 💬（0）<div>如果一个NALU的大小大于MTU （1500字节），那么这个NALU必须通过分片方式来封装其rtp包。</div>2022-06-06</li><br/>
</ul>