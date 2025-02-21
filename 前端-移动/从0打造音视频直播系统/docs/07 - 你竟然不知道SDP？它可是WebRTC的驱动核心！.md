在前面[《01 | 原来通过浏览器访问摄像头这么容易》](https://time.geekbang.org/column/article/107948)[《04 | 可以把采集到的音视频数据录制下来吗？》](https://time.geekbang.org/column/article/109105)等文章中，我向你讲解了 WebRTC 如何采集音视频数据，以及如何将它们录制成文件等相关内容。但那些知识不过是个“**开胃菜**”，WebRTC 真正核心的知识将从本文开始陆续向你展开。不过从本文开始，知识的难度会越来越高，你一定要做好心理准备。

说到 WebRTC 运转的核心，不同的人可能有不同的理解：有的人认为 WebRTC 的核心是音视频引擎，有的人认为是网络传输，而我则认为WebRTC之所以能很好地运转起来，完全是由SDP驱动的，因此**SDP才是WebRTC的核心**。

掌握了这个核心，你就知道WebRTC都支持哪些编解码器、每次通话时都有哪些媒体（通话时有几路音频/视频）以及底层网络使用的是什么协议，也就是说你就相当于拿到了打开 WebRTC 大门的一把钥匙。

由此可见，SDP 在 WebRTC 中是何等重要。下面就让我们正式进入正题吧！

## SDP 是什么

在正式讲解 SDP 之前，你首先要弄清楚SDP是什么？SDP（Session Description Protocal）说直白点就是用文本描述的各端（PC端、Mac端、Android端、iOS端等）的**能力**。这里的**能力**指的是各端所支持的音频编解码器是什么，这些编解码器设定的参数是什么，使用的传输协议是什么，以及包括的音视频媒体是什么等等。
<div><strong>精选留言（21）</strong></div><ul>
<li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTLOMFSAg7ZEt9UvpyfMgTpZLRY22wGLhAdpU619cpWicBZbsRIWnf6iakFNT1H2iarreqzKAha9VlfPQ/132" width="30px"><span>诸葛亮了</span> 👍（7） 💬（2）<div>浏览器和ios app之间用webrtc建立视频直播，ios app退出到后台，再次进入时浏览器的直播会卡住是什么原因呢？</div>2019-07-31</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/24/e8/a4/18b34a6f.jpg" width="30px"><span>_(:з」∠)_</span> 👍（4） 💬（1）<div>果然饭要一口一口吃  以前找的案例都是能跑通  但是想改点什么 不知道原理真没法下手_(:з」∠)_</div>2021-03-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/b5/3c/967d7291.jpg" width="30px"><span>艺超(鲁鸣)</span> 👍（3） 💬（2）<div>老师好，请问一下，一直不是很明白，这个里面交换SDP的时候，是通过信令服务器做的交换是吗？即使是P2P里面，也是需要信令服务器的吗？</div>2021-05-25</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/d3/ba/75f3b73b.jpg" width="30px"><span>Benjamin</span> 👍（3） 💬（1）<div>李老师你好。
SDP 这篇内容不错，让我梳理清楚了很多 SDP 细节和后续需要进一步补充更多细节的方向。

但是我这里一直有个 SDP 信息报文两端相互交换的时间点疑问。

假设是 1 to 1 的场景，一次连接时相互会交换一次 SDP 信息，连接正常音视频通信正常中的时候。
后续两端还会相互交换 SDP 信息嘛？还是说在一段主动发起再次协商时，才会触发一次两边交换一次新的 SDP 信息。并且 o= 下的 version 会递增一次。</div>2020-02-11</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTL7h9x6VXY9DmPnRWVKELfbfeJ9e9ricn12ia5icXB8u1cBhjlSE74lHiaYFAatosmjAxCdNIsyV23ByQ/132" width="30px"><span>Geek_ualcx9</span> 👍（3） 💬（1）<div>这节课开始加深了，找了一段资料，不知道对不对。

课后题：
   In SDP [1] there exists a bandwidth attribute, which has a modifier
   used to specify what type of bit-rate the value refers to.  The
   attribute has the following form:

      b=&lt;modifier&gt;:&lt;value&gt;

   Today there are four defined modifiers used for different purposes.</div>2019-12-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/19/06/39/ab72ab58.jpg" width="30px"><span>just so so</span> 👍（1） 💬（1）<div>当用户发送数据量太大超过评估的带宽时，要及时减少数据包的发送：这是不是代表着视频的质量就下降了，或者会出现马赛克的情况？</div>2019-08-26</li><br/><li><img src="" width="30px"><span>Geek_1ae6d0</span> 👍（1） 💬（2）<div>看了sdp   但是sdp是怎么用呢    web端要我们自己去打出来吗   还是调用api
</div>2019-08-14</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/HHryCCVzcAkYibxZ6B5jNRVd26NjzRZRVWff6gR9ibbmHx8JN2A6icPA48NgtLkIg1kFtiaI1ZzV1RT9UrYywLTicvw/132" width="30px"><span>Geek_855fe4</span> 👍（1） 💬（1）<div>可以使用b=AS:xxx来限制传输码率，应该是这样子的吧；
另外，老师是否可以增加些candidate、ssrc-group、ice-ufrag、ice-pwd、fingerprint、setup等属性的深入讲解呢，以及这些属性在哪些地方会被用到。有些属性一直没能很清楚的理解，没能很好的通RTP包关联起来，谢谢老师。</div>2019-08-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/18/a4/97/bc269801.jpg" width="30px"><span>良师益友</span> 👍（1） 💬（1）<div>多个用户加入一个房间，需要sdp关于编解码部分必须一样吗？</div>2019-07-30</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/ee/04/81d19d82.jpg" width="30px"><span>佛学渣</span> 👍（1） 💬（1）<div>l传输协议好像还有RTP&#47;SAVP吧...</div>2019-07-30</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/18/a8/54/06da255b.jpg" width="30px"><span>Beast-Of-Prey</span> 👍（1） 💬（1）<div>打卡 一遍过去记不住 明天再读一遍</div>2019-07-30</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/39/14/5df8e173.jpg" width="30px"><span>David</span> 👍（0） 💬（2）<div>在流媒体描述中改变码率吧，a=rtpmap:96 VP8&#47;90000，不过我好奇怎么更改SDP</div>2019-08-15</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/4d/fd/0aa0e39f.jpg" width="30px"><span>许童童</span> 👍（0） 💬（1）<div>短期记忆已经记住了SDP，晚上再回顾一下。</div>2019-07-30</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/ee/04/81d19d82.jpg" width="30px"><span>佛学渣</span> 👍（0） 💬（2）<div>是在fmtp下设置传输码率吗?</div>2019-07-30</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/2e/6b/d5870164.jpg" width="30px"><span>Berklee</span> 👍（2） 💬（0）<div>最近遇到的问题：safari 下有音频数据过来，但是没视频画面（chrome，火狐一切正常）。经排查是 safari 生成的 sdp，没有携带 video 相关信息。添加 addTransceiver 之后，可以正常产生带有 video 的 sdp。问题解决👌</div>2023-03-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/22/a6/9b/00e68014.jpg" width="30px"><span>Rian</span> 👍（1） 💬（0）<div>请教一个问题：在 janus 中，pub 的 offer 中描述推流的媒体信息，pub 的 answer中描述的也是推流的媒体信息，sub 的 offer 中描述拉流的媒体信息，sub 的 offer 中描述的也是拉流的媒体信息；那在 P2P 中一个PC即有 pub ，又有 sub ，但实际好像又没有pub和sub这个概念，pub和sub应该是信令定义的，那实际上一次sdp交换中的 offer 和 answer 的 sdp 描述的是谁的媒体信息？在webrtc中一个1v1的通话，会交换多少次sdp？</div>2022-04-29</li><br/><li><img src="" width="30px"><span>Geek_f66b13</span> 👍（0） 💬（0）<div>不太清楚webrtc通信的流程，请问是先通过sdp交换信息，然后双方再建立连接吗?建立连接的时候传输数据也是用sdp 吗？</div>2022-11-02</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/18/df/9f/6db75dff.jpg" width="30px"><span>Random</span> 👍（0） 💬（0）<div>设置码率，在SDP里设置是在媒体描述里设置b=AS:1710这种(chrome)，firefox不是AS是另外一个，这个在webrtc官网的samples目录里有。</div>2021-04-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/8c/a5/e0d96e36.jpg" width="30px"><span>helloa</span> 👍（0） 💬（0）<div>这一节的标题太网红了</div>2019-08-30</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/DYAIOgq83eos0PEkRcfViczmTPgjJ7iaAziaxswFPaqmZTEiayhXrhicmsiaOk9DDcPro0MhK3tcQlROQibe6ncH7Oj4A/132" width="30px"><span>Geek_om9fl3</span> 👍（0） 💬（0）<div>这里边设置传输码率 a=rtcp-fb:100 后边

</div>2019-08-02</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/12/ce/a8c8b5e8.jpg" width="30px"><span>Jason</span> 👍（0） 💬（1）<div>a=fmtp:122 profile-level-id=008016;max-mbps=42000;max-fs=3600;max-smbps=323500
--max-mbps=42000</div>2019-07-31</li><br/>
</ul>