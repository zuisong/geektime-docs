在上一篇[《08 | 有话好商量，论媒体协商》](https://time.geekbang.org/column/article/111675)文章中，我向你介绍了WebRTC进行通信时，是如何进行媒体协商的，以及媒体协商的目的是什么。

在媒体协商过程中，如果双方能达成一致，也就是商量好了使用什么编解码器，确认了使用什么传输协议，那么接下来，WebRTC就要建立连接，开始传输音视频数据了。

WebRTC之间建立连接的过程是非常复杂的。之所以复杂，主要的原因在于它既要考虑传输的**高效性**，又要保证端与端之间的**连通率**。

换句话说，当同时存在多个有效连接时，它首先选择传输质量最好的线路，如能用内网连通就不用公网。另外，如果尝试了很多线路都连通不了，那么它还会使用服务端中继的方式让双方连通，总之，是“想尽办法，用尽手段”让双方连通。

对于**传输的效率与连通率**这一点，既是WebRTC的目标，也是 WebRTC 建立连接的基本策略。下面我们就来具体看一下 WebRTC 是如何达到这个目标的吧！

## 在WebRTC 处理过程中的位置

下面这张图清晰地表达了本文所讲的内容在整个WebRTC处理过程中的位置。

![](https://static001.geekbang.org/resource/image/fb/ff/fbce1bba75073ab721cca628b0a61cff.png?wh=1142%2A606)

WebRTC处理过程图

图中的红色部分——连接的创建、STUN/TURN以及 NAT 穿越，就是我们本文要讲的主要内容。

## 连接建立的基本原则
<div><strong>精选留言（17）</strong></div><ul>
<li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/DYAIOgq83eoicwtj6x3l7NEcODqsXHjUTjzbl99pesNbydQUSfR6IywcKKyyaY9AIhBS0bCz3R8icMRIploDdUQA/132" width="30px"><span>花果山の酸梅汤</span> 👍（14） 💬（1）<div>srflx candidate是通过信令方式向STUN服务器发送binding request，通过该请求找到NAT映射后的地址（server视角）；prflx candidate用于链接检查，当A按照优先级向目标peer B发送binding request，B收到peer A的连通性成功时获得的地址（peer视角）。不知道是否是这样。</div>2019-08-05</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/12/a2/d18e6394.jpg" width="30px"><span>山石尹口</span> 👍（5） 💬（1）<div>连通性检测时的超时设置比较重要，设置短了，会把可以连通的判断为不能连通，设置长了，就会在不能连通的配对上浪费时间</div>2019-08-03</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/9EU2n1Rc4FEr2QicklnU0GQUhPMssibCpTSoxvd779pialoSRraibbiakCHgibA3LIMxWPrWMccjaWvWIJZIztqKXTkA/132" width="30px"><span>Hengstar</span> 👍（3） 💬（1）<div>李老师你好。非常喜欢你的课，讲解很详细。我正好工作中有遇到很多麻烦的问题。比如有很多人家里会安装Wifi的扩展器（extender）设备，这样在家里的时候这些人在不同的位置可能会自动连接到不同的wifi设备（可能是路由器或者是扩展器之间来回切换）。对于这种情况，我们移动端用WebRTC实现的app在通过Host local网络连接上以后，切换wifi的时候是不是会断开WebRTC连接呢？我们如何能够判断这种情况？有没有办法可以很好的实现这种无缝的重连呢？</div>2021-02-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/d3/ba/75f3b73b.jpg" width="30px"><span>Benjamin</span> 👍（3） 💬（1）<div>这篇总算把 STUN 和 TURN 差别搞清楚了

理论上来说 relay 的 TURN 保证一定可以连接上，但是被中转了一次后，后续音视频 UDP 包效率会受到影响。</div>2020-02-11</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTILsdfVI9jlvql6iaLMyButxZS3PztEMBn4GpUTAM9vsEyWk6GxjqjtU894A3npELIs3uxe6AoP7icg/132" width="30px"><span>Geek_fc668a</span> 👍（2） 💬（2）<div>老师，有个问题一直很不解，很希望获得您的解答：在一般的C&#47;S架构中，服务器可以很轻松地获取客户端的ip地址，拿为什么不能由信令服务器获取一方的ip交给另一方发起连接，而需要STUN&#47;TURN呢？</div>2020-12-01</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTJLAxia7JictXmRQ02VwuibKOpib5bMcWbQHZeeQhsV17KeGh5u7ySyibgMVLwcoqCA3ZiayI3dLaVOjibRg/132" width="30px"><span>Geek_82d1fd</span> 👍（2） 💬（4）<div>老师，我又几个问题
1. candidate是不是可以直接设置到SDP里面？
2. 跟媒体服务器通信的时候为什么要发Stun包？</div>2020-04-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/82/42/8b04d489.jpg" width="30px"><span>刘丹</span> 👍（2） 💬（3）<div>请问ICE是哪3个英文单词的缩写？是Internet Communication Engine吗？能否创建一个术语表章节？</div>2019-08-04</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/47/00/3202bdf0.jpg" width="30px"><span>piboye</span> 👍（1） 💬（2）<div>老师， 我一直纳闷 turn 服务器为什么一定要分配 relay port 出来， 这样分配后服务器很难部署了。 不分配端口也是可以做转发啊？</div>2021-03-03</li><br/><li><img src="https://wx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTJoNVHqRL5iatEoMgfFAaGFZxD8ic6CicxKI9Facp4bzAkNMAfaduSENlPOafs6dOGawibhNv3V9lVowQ/132" width="30px"><span>SherwinFeng</span> 👍（1） 💬（2）<div>prflx和srflx都是为了获取内网主机IP映射的公网IP，只是srflx是通过STUN协议，prflx是直接向目的主机发起连接并请求响应的方式。</div>2019-11-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/12/ce/a8c8b5e8.jpg" width="30px"><span>Jason</span> 👍（1） 💬（1）<div>是不是这样的？srflx：内网地址被NAT映射后的地址，对称型 NAT 与对称型 NAT 、对称型 NAT 与端口限制型 NAT是无法进行 P2P 穿越的；prflx：TUN Server上为客户端分配的中继地址，与各种NAT类型地址都可以进行P2P连接；</div>2019-08-05</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTKcwxhdFicBaG4zozbxwNa1K5slcRP7ia3iacjWf5odJO4WtvFDJlztDRFKRddAAVHwlIS5CatQMD5wA/132" width="30px"><span>Geek_7afbfc</span> 👍（0） 💬（3）<div>老师，无互联网环境，如果是同一网段内网，且未搭建内网的turn服务器，那咱们的Webrtc就不可用吗？</div>2020-08-03</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1a/ab/6f/58ca88b8.jpg" width="30px"><span>微~凉</span> 👍（0） 💬（2）<div>请问老师：我在iOS设备上再若望情况下，相互视频的过程中经常会收到ice断开连接的信息，网络通畅的情况下就没问题，请问是什么原因啊？</div>2020-01-15</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1a/0e/96/eca820c7.jpg" width="30px"><span>李新</span> 👍（0） 💬（2）<div>候选者类型还有一种：prflx，可以提供P2P的打洞成功率。</div>2019-11-03</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/4d/fd/0aa0e39f.jpg" width="30px"><span>许童童</span> 👍（0） 💬（1）<div>prflx candidate (prflx候选者）：是一个候选地址，通过从主机候者选地址发 送一个STUN请求到运行在Peer候选地址上的STUN服务器而获取的候选地址。</div>2019-08-03</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/4d/fd/0aa0e39f.jpg" width="30px"><span>许童童</span> 👍（0） 💬（3）<div>老师你好，可以解释一下为什么需要 NAT 穿越吗？</div>2019-08-03</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/ae/a7/6d3a5d44.jpg" width="30px"><span>Dump</span> 👍（0） 💬（0）<div>WebRTC看似是用于及时视频通话的，里面涉及的技术如老师所说可以应用到很多方面，真是一个大宝藏，学习了。</div>2019-08-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/18/a8/54/06da255b.jpg" width="30px"><span>Beast-Of-Prey</span> 👍（0） 💬（0）<div>打卡</div>2019-08-03</li><br/>
</ul>