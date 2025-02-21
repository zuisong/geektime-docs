WebRTC不但可以让你进行音视频通话，而且还可以用它传输普通的二进制数据，比如说可以利用它实现文本聊天、文件的传输等等。

WebRTC的**数据通道（RTCDataChannel）**是专门用来传输除了音视频数据之外的任何数据，所以它的应用非常广泛，如实时文字聊天、文件传输、远程桌面、游戏控制、P2P加速等都是它的应用场景。

像文本聊天、文件传输这类应用，大多数人能想到的通常是通过服务器中转数据的方案，但 WebRTC 则优先使用的是**P2P方案，即两端之间直接传输数据**，这样就大大减轻了服务器的压力。当然WebRTC也可以采用中继的方案，这就需要你根据自己的业务需要进行选择，非常灵活。

## RTCDataChannel 介绍

RTCDataChannel 就是 WebRTC 中专门用来传输非音视频数据的类，它的设计模仿了WebSocket 的实现，使用起来非常方便，关于这一点我将在下面的“RTCDataChannel 的事件” 部分向你做更详细的介绍。

另外，RTCDataChannel 支持的数据类型也非常多，包括：字符串、Blob、ArrayBuffer 以及 ArrayBufferView。

实际上，关于这几种类型的联系与区别我在前面[《04 | 可以把采集到的音视频数据录制下来吗？》](https://time.geekbang.org/column/article/109105)一文中已经向你做过详细的介绍，如果你现在记不清了，可以再去回顾一下。
<div><strong>精选留言（12）</strong></div><ul>
<li><img src="" width="30px"><span>Geek_c1c44a</span> 👍（7） 💬（1）<div>老师您好，请问zoom和直播技术相关吗？zoom可能使用什么协议呢？</div>2019-08-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/4d/fd/0aa0e39f.jpg" width="30px"><span>许童童</span> 👍（6） 💬（1）<div>SCTP 协议基于UDP，自行实现TCP相关的功能。</div>2019-08-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/93/bd/f3977ebb.jpg" width="30px"><span>John</span> 👍（5） 💬（2）<div>这个问题好像应该问在这个章节: 如果做百人群聊的功能 不用中间服务器 只用webrtc技术和peerconnection 大家觉得普通带宽和手机能够承载么</div>2019-11-16</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/a8/7e/c9201b20.jpg" width="30px"><span>三角形小于零</span> 👍（3） 💬（1）<div>&quot;文本通过 RTCDataChannel 发送出去后，最终是经过 RTCPeerConnection 传送出去的&quot; 
之前提到过 RTCPeerConnection 可以理解为是一个功能超强的 socket，那么 DataChannel 的 SCTP 也是使用这个超强的 socket 来实现的吗？ 

如果需要 relay，那么 turn server 也会负责帮忙 relay 通信双方往 DataChannel 里发的数据吗？ </div>2020-11-22</li><br/><li><img src="" width="30px"><span>宇宙之王</span> 👍（1） 💬（1）<div>看到您GitHub例子里面19_chat用了var pcConfig = {
  &#39;iceServers&#39;: [{
    &#39;urls&#39;: &#39;turn:stun.al.learningrtc.cn:3478&#39;,
    &#39;credential&#39;: &quot;mypasswd&quot;,
    &#39;username&#39;: &quot;garrylea&quot;
  }]
};
这段是不是没用，好像是您自己的服务器，我把它赋值空var pcConfig=null;也能正常运行。另外当开两个窗口的时候，有时会掉线一个，再连接服务器能连上，但是发送框就老是灰的了，就要两个都断掉重新再联了，这一般是什么原因，谢谢老师！
</div>2020-09-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/d2/8a/57dcd0c7.jpg" width="30px"><span>峰</span> 👍（1） 💬（1）<div>老师，一个题外话，这么多可作后端的语言，c++、python、go、java、c#该如何选择了？</div>2019-08-28</li><br/><li><img src="" width="30px"><span>木木</span> 👍（1） 💬（1）<div>SCTP是运行在UDP上的，本质上是对UDP的封装，在应用层实现了有序性与可靠性的配置。</div>2019-08-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1d/7e/57/588337e9.jpg" width="30px"><span>Bubbly</span> 👍（0） 💬（1）<div>var options = {
	key : fs.readFileSync(&#39;.&#47;cert&#47;1557605_www.learningrtc.cn.key&#39;),
	cert: fs.readFileSync(&#39;.&#47;cert&#47;1557605_www.learningrtc.cn.pem&#39;)
}
老师，这里的key和pem都没有呀</div>2020-10-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1d/cd/56/988460da.jpg" width="30px"><span>cheese</span> 👍（0） 💬（1）<div>在create和join后，双方成功连接后，能否用Datachannel来传输信令呢？比如：关闭麦克风之类的</div>2020-04-09</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTIQYc8seCHrRfJicqCWDfUap4jdHWnJ39ezlpvIY5sbwZP8ze9lFE572hzeNEY07nHWVjaR0QLjgyw/132" width="30px"><span>Geek_5a0689</span> 👍（0） 💬（1）<div>老师，我的server.js在我部署的腾讯云服务器上跑起来了，但是在我本机的html页面请求的时候，没有任何反应，看服务器上的日志也是没有任何的打印，是什么原因呢？我直接跑的git上面的代码都不可以</div>2020-03-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/fa/6d/d8ba854c.jpg" width="30px"><span>希望改名字不被发现的俊wen</span> 👍（0） 💬（2）<div>同一个peerconnection，datachannel发送的文字能和视频stream保持同步吗</div>2019-08-29</li><br/><li><img src="" width="30px"><span>Geek_c9206f</span> 👍（0） 💬（0）<div>如果同时有多个会话呢DataChannel还能对上嘛</div>2024-10-11</li><br/>
</ul>