近年来，随着智能手机的普及以及移动互联网的飞速发展，音视频技术在各个行业得到了广泛的应用。尤其是娱乐直播在前几年着实火了一把，像映客、斗鱼这类以展示才艺为主的直播产品非常受大家的欢迎。

从技术角度来讲，映客、斗鱼这类娱乐直播与在线教育、音视频会议直播有着非常大的区别。在线教育、音视频会议这类直播属于**实时互动直播**，主要考虑**传输的实时性**，因此一般使用 **UDP** 作为底层传输协议；而娱乐直播对实时性要求不高，更多关注的是画面的质量、音视频是否卡顿等问题，所以一般采用 **TCP** 作为传输协议。我们称前者为实时互动直播，后者为传统直播。

本专栏的前两个模块都是介绍实时互动直播的，而从今天开始我们会讲解传统直播技术。

**传统直播技术使用的传输协议是 RTMP 和 HLS**。其中，RTMP是由 Adobe 公司开发的，虽然不是国际标准，但也算是工业标准，在 PC 占有很大的市场；而HLS是由苹果公司开发的，主要用在它的 iOS 平台，不过Android 3 以后的平台也是默认支持 HLS 协议的。

接下来，我们先看一下传统音视频直播系统的基本架构，让你对传统直播架构的“内幕”有一个初步的了解。

## 传统直播基本架构

商业级直播系统的规模、结构是非常复杂的，除了最核心的音视频直播外，还包括用户管理、认证系统、直播间管理、打赏、红包、私信等很多功能，不过这些更多的是一些业务逻辑，在本文中我们不会对它们进行讲解，而是聚焦在**最核心的音视频直播技术**上。
<div><strong>精选留言（13）</strong></div><ul>
<li><img src="" width="30px"><span>Geek_701918</span> 👍（15） 💬（1）<div>还有一个RTMP不支持h265</div>2019-09-26</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/WgRsoJMxcTMcDkRlR59jCDLux2JDdtz1G8Ophe3a7EnhP8lqOdFw8F7sURXkRTYXibzVicozrQ8HFYj578myJ0CA/132" width="30px"><span>行所当行</span> 👍（7） 💬（4）<div>老师你好，RTMP 协议没有使用标准的 HTTP 接口传输数据，这个劣势为啥不能把端口改成80&#47;443?   另外，RTMP 协议也是基于TCP协议，也要三次握手四次挥手，那这部分机制造成的延迟是不是也和HLS一样长？</div>2020-05-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/3c/8a/900ca88a.jpg" width="30px"><span>神经旷野舞者</span> 👍（4） 💬（1）<div>rtmp使用tcp为了不丢数据，保证视频的不失真，因为对实时性要求不高，所以就优先保证不失真。
最近在研究ffmpeg怎么保证rtsp的稳定性和提高hls视频首开速度，考虑使用srs流媒体服务器，所以直接看了这节的视频，想问老师，要解决速度问题这会涉及到什么关键帧之类的底层视频编码知识吗？
</div>2019-12-16</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/TFV3al9EvFeoCrJnQQAXBTqGtg2Ev42eJXlTnX4aAP8alUt1vVD8GkqudkhBdWNqcvELzq2oXmrppD9dWcKgsw/132" width="30px"><span>大只广</span> 👍（4） 💬（1）<div>老师能讲讲rtsp和rtmp的区别和使用场景吗？</div>2019-10-03</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/93/bd/f3977ebb.jpg" width="30px"><span>John</span> 👍（3） 💬（3）<div>一直想不明白很多电脑上的Chrome是怎么播放m3u8的 老师能不能讲解一下</div>2019-09-24</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/DYAIOgq83epHNuOTMIO9AmibXQ8ibsbAhYMiaYtBX7yI88zZHiakwc829S6iaerDFlqPvsySleQnm7yPCHCPyTZ1NAA/132" width="30px"><span>Geek_fe19fe</span> 👍（1） 💬（1）<div>老师，我有几个问题请教，希望能得到您的帮助：
（1）前面文章有提到NAT类型检测需要用到两台服务器，但这里却是一台，是否会出现判断不准确的情况？
（2）如果打洞失败，靠TURN服务器中转，延迟大概多少呢，假如是2M、720P。
（3）中国PC端和移动端打洞成功率大概多少呢，校园环境会不会特殊？
（4）生日悖论下的预测端口方法，真的可以将打洞成功率提升到80%以上吗？</div>2021-01-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/47/00/3202bdf0.jpg" width="30px"><span>piboye</span> 👍（1） 💬（1）<div>http2.0普及，http3.0的到来，rtmp的延迟优势会消失吧</div>2020-12-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/0b/a7/6ef32187.jpg" width="30px"><span>Keep-Moving</span> 👍（1） 💬（1）<div>#### RTMP协议
* 优势：
    1. 底层依赖于TCP
    2. 使用简单，技术成熟
    3. 市场占有率高
    4. 相较于HLS协议，实时性要高很多
* 劣势：
    1. iOS不支持RTMP，认为其在安全方面有缺陷
    2. Adobe已停止对其的更新

#### HLS：本质就是通过HTTP下载文件，然后将下载的切片缓存起来。由于切片文件很小，所以可以实现边下载边播放的效果
* 优势：
    1. RTMP没有使用标准的HTTP接口传输数据，在一些有访问限制的网络环境下，没法访问外网。而HLS是基于HTTP的，天然就解决了这个问题
    2. HLS协议本身实现了码率自适应，不同带宽的设备可以自动切换到最适合自己码率的视频进行播放
    3. 浏览器天然支持HLS，而RTMP协议需要安装Flash插件才能播放RTMP流
* 不足：
    1. 实时性差</div>2019-09-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/20/25/b7/43901643.jpg" width="30px"><span>陈陳</span> 👍（0） 💬（1）<div>flash 貌似2020 12月份不支持了，rtmp是不是就不行了</div>2020-11-04</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/69/ad/608188c2.jpg" width="30px"><span>4thirteen2one</span> 👍（0） 💬（1）<div>从图中可以看出，传输直播架构由直播客户端、信令服务器和 CDN 网络这三部分组成。

“传输”应该是“传统”，文中这里打错了。</div>2019-10-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/82/42/8b04d489.jpg" width="30px"><span>刘丹</span> 👍（0） 💬（3）<div>看这门课的目录，好像WebRTC只支持几个人、几十个人的视频会议，不支持上万人在线的直播？</div>2019-09-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/1a/e2/f88bf28f.jpg" width="30px"><span>frank</span> 👍（0） 💬（2）<div>技术解决的问题域决定其实现，rtmp主要的应用场景是单向直播，并不是双向互动（虽然现在小程序也可以rtmp做双向视频通讯，毕竟做了大量优化的），所以使用TCP带来的一秒左右的延时完全可以接收，而且可以简化协议设计、实现和大规模商用</div>2019-09-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/94/d7/bd4ffe8c.jpg" width="30px"><span>么么直播</span> 👍（16） 💬（0）<div>现在的直播公司都往webrtc迁移了。特别是类似连麦互动场景增多后。。。我们就是☺️</div>2019-11-30</li><br/>
</ul>