虽然苹果拒绝使用 RTMP 协议并推出了自己的 HLS 技术，但大多数用户仍然还是使用 RTMP 协议作为传统直播系统的传输协议。在 Adobe 宣布不再对 RTMP技术进行支持的情况下，仍然还有这么多用户在使用它，说明 RTMP 协议具有其他协议不可比拟的优势。

这里我们做个对比，你就知道 RTMP 协议的优势在哪里了。

- 首先，与 HLS 技术相比，RTMP协议在传输时延上要比 HLS 小得多。主要原因在于 HLS 是基于切片（几秒钟视频的小文件）、然后缓存的技术，这种技术从原理上就比直接进行数据传输慢很多，事实也证明了这一点。
- 其次，相对于 RTP 协议，RTMP底层是基于 TCP 协议的，所以它不用考虑数据丢包、乱序、网络抖动等问题，极大地减少了开发人员的工作量；而使用 RTP 协议，网络质量的保障都需要自己来完成。
- 最后，与现在越来越火的 WebRTC 技术相比，RTMP也有它自己的优势。虽然在实时传输方面 WebRTC 甩 RTMP 技术几条街，但对于实时性要求并没有那么高的传统直播来说，RTMP协议在音视频的服务质量上普遍要好于 WebRTC 的音视频服务质量。

这下你知道RTMP协议为什么会存活这么久了吧。那说了这么多，RTMP协议与 FLV 又有什么关系呢？实际上，FLV文件与 RTMP 之间是“近亲”关系，甚至比“近亲”还要近，亲得就好像是“一个人”似的。
<div><strong>精选留言（10）</strong></div><ul>
<li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/15WXictKcv02AGs8PPBGvytRZ2KwzsCQx3nWTWP9iasTvXiaUonAv2iawhAiaAwDDpZjKJtCaiaiaEQEmnwicnyJ7nbyicg/132" width="30px"><span>redbg</span> 👍（7） 💬（1）<div>bilibili 的 flv.js，可以用 h5 播放 flv</div>2019-09-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/82/42/8b04d489.jpg" width="30px"><span>刘丹</span> 👍（3） 💬（2）<div>FLV Body里为什么把TagSize放在Tag后面呢？如果TagSize在Tag前面，解析时就知道需要读入多少字节了。</div>2019-09-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/82/42/8b04d489.jpg" width="30px"><span>刘丹</span> 👍（2） 💬（1）<div>请问合并2个FLV文件的时候，是否要把第2个FLV文件的FLV头这几个字节删除掉？</div>2019-09-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/29/0a/0ba09c68.jpg" width="30px"><span>一颗大白菜</span> 👍（0） 💬（2）<div>有两个疑问：
（1）在尾部追加Tag时是否需要更新Metadata中filesize和duration吗？
（2）在尾部追加Tag时是否会引起Metadata大小变化呢？如果大小变化，那么是不是需要将重新生成文件？</div>2020-08-06</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/3c/8a/900ca88a.jpg" width="30px"><span>神经旷野舞者</span> 👍（0） 💬（1）<div>既然flv和rtmp等于没有区别，为什么后来者还要自立门户呢？</div>2019-12-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1a/0e/96/eca820c7.jpg" width="30px"><span>李新</span> 👍（0） 💬（1）<div>对于CDN厂商来说，观看端都是使用HTTP-FLV吧？</div>2019-11-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/12/ce/a8c8b5e8.jpg" width="30px"><span>Jason</span> 👍（0） 💬（1）<div>potplayer</div>2019-09-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/12/ce/a8c8b5e8.jpg" width="30px"><span>Jason</span> 👍（0） 💬（1）<div>讲的很清楚，赞</div>2019-09-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/75/38/973fa3e7.jpg" width="30px"><span>潇湘落木</span> 👍（6） 💬（0）<div>FLV封装格式详解，作为补充！
https:&#47;&#47;mp.weixin.qq.com&#47;s&#47;cMM2wbh1-DGWEMUB02mK8g
https:&#47;&#47;mp.weixin.qq.com&#47;s&#47;teQ7FoNj5FIE-3PICBIvlA</div>2019-11-05</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/4f/ab/dd9ab224.jpg" width="30px"><span>EdwdChen</span> 👍（1） 💬（0）<div>请问一下像 flv 没有一个结构化的头，seek 的时候应该怎么样快速找到对应的位置呢？</div>2022-06-28</li><br/>
</ul>