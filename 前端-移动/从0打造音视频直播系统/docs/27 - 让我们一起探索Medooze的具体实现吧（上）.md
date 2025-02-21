在咱们专栏的第一模块，我向你介绍了如何使用 WebRTC 进行实现音视频互动。随着 Google 对 WebRTC 的大力推广，目前主流的浏览器都支持了 WebRTC。WebRTC 最主要的功能就是提供端对端的音视频通信，其可以借助 STUN/TURN 服务器完成 NAT 穿越，实现两个端点之间的直接通信。

1对1的实时通信无疑是 WebRTC 最主要的应用场景，但你是否想过 WebRTC 可以通过浏览器实现多人音视频会议呢？更进一步，你是否想过 WebRTC 可以实现一些直播平台中上万人甚至几十万人同时在线的场景呢？

如果你对上面的问题感兴趣，那本文将让你对上面问题有个全面的了解，接下来就让我们一起开启本次神秘之旅吧！

## 流媒体服务器Medooze

正如我们在[《25 | 那些常见的流媒体服务器，你该选择谁？》](https://time.geekbang.org/column/article/134284)一文中介绍的，要实现多个浏览器之间的实时音视频通信（比如音视频会议），那么就一定需要一个支持 WebRTC 协议的流媒体服务器。目前，有很多开源的项目支持 WebRTC 协议， Medooze 就是其中之一。

Medooze的功能十分强大，通过它你既可以实现 SFU 类型的流媒体服务器，也可以实现MCU类型的流媒体服务器。而且，它还支持多种媒体流接入，也就是说，你除了可以通过浏览器（WebRTC）向Medooze分享音视频流之外，还可以使用 FFmpeg/VLC 等工具将 RTMP 协议的音视频流推送给 Meoodze。更加神奇的是，无论是 WebRTC 分享的音视频流还是 RTMP 格式的音视频流通过Medooze转发后，浏览器就可以将 FFmpeg/VLC推的流显示出来，而VLC也可以将 WebRTC 分享的音视频显示出来，这就是 Medooze 的强大之处。
<div><strong>精选留言（6）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/10/47/00/3202bdf0.jpg" width="30px"><span>piboye</span> 👍（0） 💬（2）<div>media-server-node 编译好像要 node v10 的版本， 高版本的node 编译不过去了，medooze 看来的确不怎么维护了</div>2020-12-31</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/WUqZcTgiaD7nLDWJV7vzIicHuNv4PqLEl2ZgAU6g2ez9OsGA9cF0fENpQialBp1XDTNQF7BM8qticNf87bTZTxacNg/132" width="30px"><span>江枫</span> 👍（0） 💬（1）<div>老师：Medooze支持MCU模式，请问有对应的资料推荐吗</div>2019-11-26</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/HHryCCVzcAkYibxZ6B5jNRVd26NjzRZRVWff6gR9ibbmHx8JN2A6icPA48NgtLkIg1kFtiaI1ZzV1RT9UrYywLTicvw/132" width="30px"><span>Geek_855fe4</span> 👍（0） 💬（1）<div>用了一年多的medooze-media-server，最近在看源码，看的一头雾水，感觉都快走火入魔了，感谢老师清晰的组件关系图。另外有点好奇怎么使用vlc向media-server推送RTP，老师可以详细说下吗？谢谢</div>2019-09-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/18/a8/54/06da255b.jpg" width="30px"><span>Beast-Of-Prey</span> 👍（0） 💬（1）<div>感觉好难 一遍过去 五分钟 忘的一干二净</div>2019-09-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/54/21/8c13a2b4.jpg" width="30px"><span>周龙亭</span> 👍（0） 💬（1）<div>浏览器怎么和媒体服务器建立起连接的呢？</div>2019-09-15</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/f7/a6/79a835ac.jpg" width="30px"><span>Leeing</span> 👍（0） 💬（0）<div>思考题：我理解 nodejs 的性能影响应该只影响 media-server-node 库吧，media-server 是调用的 c&#47;c++，nodejs 应该影响不到它。不知道我理解的对不对</div>2022-04-06</li><br/>
</ul>