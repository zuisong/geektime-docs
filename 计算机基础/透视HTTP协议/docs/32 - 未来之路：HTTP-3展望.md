在前面的两讲里，我们一起学习了HTTP/2，你也应该看到了HTTP/2做出的许多努力，比如头部压缩、二进制分帧、虚拟的“流”与多路复用，性能方面比HTTP/1有了很大的提升，“基本上”解决了“队头阻塞”这个“老大难”问题。

## HTTP/2的“队头阻塞”

等等，你可能要发出疑问了：为什么说是“基本上”，而不是“完全”解决了呢？

这是因为HTTP/2虽然使用“帧”“流”“多路复用”，没有了“队头阻塞”，但这些手段都是在应用层里，而在下层，也就是TCP协议里，还是会发生“队头阻塞”。

这是怎么回事呢？

让我们从协议栈的角度来仔细看一下。在HTTP/2把多个“请求-响应”分解成流，交给TCP后，TCP会再拆成更小的包依次发送（其实在TCP里应该叫segment，也就是“段”）。

在网络良好的情况下，包可以很快送达目的地。但如果网络质量比较差，像手机上网的时候，就有可能会丢包。而TCP为了保证可靠传输，有个特别的“丢包重传”机制，丢失的包必须要等待重新传输确认，其他的包即使已经收到了，也只能放在缓冲区里，上层的应用拿不出来，只能“干着急”。

我举个简单的例子：

客户端用TCP发送了三个包，但服务器所在的操作系统只收到了后两个包，第一个包丢了。那么内核里的TCP协议栈就只能把已经收到的包暂存起来，“停下”等着客户端重传那个丢失的包，这样就又出现了“队头阻塞”。
<div><strong>精选留言（30）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/0f/4d/fd/0aa0e39f.jpg" width="30px"><span>许童童</span> 👍（27） 💬（3）<div>IP 协议要比 UDP 协议省去 8 个字节的成本，也更通用，QUIC 为什么不构建在 IP 协议之上呢？
直接利用UDP，兼容性好。
说一说你理解的 QUIC、HTTP&#47;3 的好处。
彻底解决队头阻塞，用户态定义流量控制、拥塞避免等算法，优化慢启动、弱网、重建连接等问题。
对比一下 HTTP&#47;3 和 HTTP&#47;2 各自的流、帧，有什么相同点和不同点。
HTTP&#47;3在QUIC层定义流、帧，真正解决队头阻塞，HTTP&#47;2流、帧是在TCP层上抽象出的逻辑概念。
相同点是在逻辑理解上是基本一致的，流由帧组成，多个流可以并发传输互不影响。</div>2019-08-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/9d/a4/e481ae48.jpg" width="30px"><span>lesserror</span> 👍（12） 💬（1）<div>老师，以下问题，麻烦回答一下，谢谢：

1.它使用自己的帧“接管”了 TLS 里的“记录”，握手消息、警报消息都不使用 TLS 记录，直接封装成 QUIC 的帧发送，省掉了一次开销。省掉的一次开销是什么？

2.解决了 HPACK 的“队头阻塞”问题。 没明白这句话。</div>2019-12-25</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/35/51/c616f95a.jpg" width="30px"><span>阿锋</span> 👍（7） 💬（1）<div>（1）http的队头阻塞，和tcp的队头阻塞，怎么理解 ？是由于tcp队头阻塞导致http对头阻塞，还是http本身的实现就会造成队头阻塞，还是都有。感觉有点模糊？
（2）看完了QUIC，其流内部还是会产生队头阻塞，感觉没啥区别，QUIC内部还不是要实现tcp的重传那一套东西。QUIC没看出来比tcp好在哪里。
（3）队头阻塞在http，tcp，流等这几个概念中是怎么理解和区分的，很迷惑。</div>2019-08-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/79/4b/740f91ca.jpg" width="30px"><span>-W.LI-</span> 👍（6） 💬（1）<div>1.传输层TCP和UDP就够了，在多加会提高复杂度，基于UDP向前兼容会好一些。
2.在传输层解决了队首阻塞，基于UDP协议，在网络拥堵的情况下，提高传输效率
3.http3在传输层基于UDP真正解决了队头阻塞。http2只是部分解决。</div>2019-08-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/62/dc/8876c73b.jpg" width="30px"><span>moooofly</span> 👍（3） 💬（3）<div>我是不是可以这样理解，QUIC 之所以解决了队头阻塞，是基于UDP的乱序，无连接，以包为单位进行传出的特性，即当发生丢包时，当前流中对应的请求或应答就彻底“丢失”了，之后只需要通过在UDP基础实现的“可靠传输”功能，重传就好了，这样就避免了接收端死等尚未接收到的数据的“干着急”状态；</div>2019-08-31</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/29/b0/d3/200e82ff.jpg" width="30px"><span>功夫熊猫</span> 👍（2） 💬（1）<div>udp虽然可以节省时间和速度比tcp快，但是如果传输的是那种很机密的东西的时候，但是如何保证udp传输的数据是没有丢失的，（所以udp一般是传输视频，图片之类的东西吧）是换tcp还是对udp进行改装，还是http&#47;3有什么特殊的方法</div>2021-10-31</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/ee/c2/873cc8d9.jpg" width="30px"><span>Rick</span> 👍（2） 💬（1）<div>请问连接迁移是如何做到的?毕竟它依赖于udp，而udp使用了ip&#47;port。当一个连接的一端从一个ip&#47;port转移到另外一个ip&#47;port上的时候，怎么通知对端呢？需要使用QUIC的控制帧来完成吗？</div>2021-03-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1e/01/c5/b48d25da.jpg" width="30px"><span>cake</span> 👍（1） 💬（1）<div>老师 请问下这句话怎么理解呢  HTTP&#47;2 那样再去定义流</div>2021-10-05</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1e/f2/f5/b82f410d.jpg" width="30px"><span>Unknown element</span> 👍（1） 💬（1）<div>gQUIC 混合了 UDP、TLS、HTTP，是一个应用层的协议。而 IETF 则对 gQUIC 做了“清理”，把应用部分分离出来，形成了 HTTP&#47;3，原来的 UDP 部分“下放”到了传输层，所以 iQUIC 有时候也叫“QUIC-transport”。接下来要说的 QUIC 都是指 iQUIC，要记住，它与早期的 gQUIC 不同，是一个传输层的协议，和 TCP 是平级的

老师问下这一段最后为什么说iQUIC是传输层协议？本来gQUIC是应用层协议，去掉传输层部分后反而变成了传输层协议吗？</div>2021-06-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1a/e8/43/f9c0faed.jpg" width="30px"><span>小童</span> 👍（1） 💬（1）<div>老师这个QUIC 是如何保证UDP的 可靠传输？还是没看明白。</div>2021-04-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/18/80/f4/564209ea.jpg" width="30px"><span>纳兰容若</span> 👍（1） 💬（1）<div>老师您好，想向老师请教一下学习方法的问题
学习HTTP协议一直学习到这里，发现老师学识太渊博了，这得需要好多年的积累吧
像我这样初学网络、HTTP协议的，老师有什么好的建议么
感谢老师的回复</div>2020-11-16</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/67/f4/9a1feb59.jpg" width="30px"><span>钱</span> 👍（1） 💬（1）<div>浏览器需要先用 HTTP&#47;2 协议连接服务器，然后服务器可以在启动 HTTP&#47;2 连接后发送一个“Alt-Svc”帧，包含一个“h3=host:port”的字符串，告诉浏览器在另一个端点上提供等价的 HTTP&#47;3 服务。
老师，这里的意思是指HTTP&#47;3包含了HTTP&#47;2的这部分功能，还是HTTP&#47;3的使用必须依赖HTTP&#47;2？
另外，QUIC中的包是一个完整的请求或响应报文？否则多个包的内容才能组成一个完整的请求或响应报文，必然也需要等待所有包都到齐了，组装一下吧？假如你一个包，这个包得多大？</div>2020-04-04</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/42/44/d3d67640.jpg" width="30px"><span>Hills录</span> 👍（1） 💬（1）<div>课后1：QUIC 不基于 IP 协议，是因为没有设备认识它
课后2：HTTP&#47;3 端口不固定、内容天然加密、连接迁移等特性，让互联网回归自由</div>2020-02-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/ba/bf/e9a44c63.jpg" width="30px"><span>chao</span> 👍（1） 💬（1）<div>老师，文中有一张包的结构图，Quic Package Payload 里面说『实际传输的数据是多个帧构成的流』，这里怎么理解呢？
是这样吗，Quic里面有帧、流、包的概念，流上传输的是帧，Quic是把多个流结合为包然后传递给UDP吗，因为每个流是一个消息，丢包的时候会一次丢多个消息吗</div>2019-10-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/62/dc/8876c73b.jpg" width="30px"><span>moooofly</span> 👍（1） 💬（1）<div>“下班回家，手机会自动由 4G 切换到 WiFi。这时 IP 地址会发生变化，TCP 就必须重新建立连接。而 QUIC 连接里的两端连接 ID 不会变，所以连接在“逻辑上”没有中断，它就可以在新的 IP 地址上继续使用之前的连接，消除重连的成本，实现连接的无缝迁移”，我觉得这里是不是应该强调一下，QUIC 是基于无连接概念的 UDP 协议，因此也就没有所谓的“中断”和“重连”概念，进而才能实现在新的 ip 地址上的无缝迁移；</div>2019-08-31</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/62/dc/8876c73b.jpg" width="30px"><span>moooofly</span> 👍（1） 💬（1）<div>一个小建议：既然 TLS1.3 是被“包含”在 QUIC 协议中的，那么文章中给出的 HTTP&#47;3 协议栈图，就有点容易让人产生误会，图示给人的感觉是 QUIC 和 TLS1.3 是一个级别的对等存在，让人感觉 QPack 是基于 QUIC 的，而 Stream 是基于 TLS1.3 实现的</div>2019-08-31</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/79/4b/740f91ca.jpg" width="30px"><span>-W.LI-</span> 👍（1） 💬（1）<div>老师好!
协议处在哪一次有什么划分标准么?
mac层和ip成感觉一般不怎么会变
传输层和应用层搞不太清楚</div>2019-08-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/7b/57/a9b04544.jpg" width="30px"><span>QQ怪</span> 👍（1） 💬（1）<div>老师能否分享下要更新换代http3，其上层的服务协议是否也要更新还是都能够兼容？</div>2019-08-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/c0/f0/1aabc056.jpg" width="30px"><span>Jiantao</span> 👍（0） 💬（1）<div>老师，文中提到h3&#47;quic是包含tls的，意思是要使用h3&#47;quic 必须要求域名是https吗

</div>2022-11-07</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/Q3auHgzwzM74658w9PQeTM4TcM14BzfpJnVLrsciaS26ibRwRbCE09ydI6UlZhFrJh7iaVLp2xxhBppVDKLyRRg9Q/132" width="30px"><span>Geek_21a73c</span> 👍（0） 💬（2）<div>老师，基于UDP的QUIC如何保证数据一定抵达目的地呢</div>2022-06-20</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTIuTjCibv0afd7SSdLicfNk0f7KO5ga9VMleD1hc2DtQfianK20ht06SekClKV7M8UXLRHqQLm9hJ3ow/132" width="30px"><span>Jasmine</span> 👍（0） 💬（1）<div>老师，文中QUIC Packet Header的目标连接\源连接ID的长度为什么单独拎出来画？是ID长度单独花8bit来表示，具体ID再是ID，还是连接ID就是各4位来表示？</div>2021-10-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1e/01/c5/b48d25da.jpg" width="30px"><span>cake</span> 👍（0） 💬（1）<div> HTTP&#47;2 那样再去定义流   这句话中的 &quot;定义&quot; 如何理解呢</div>2021-10-05</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1e/f2/f5/b82f410d.jpg" width="30px"><span>Unknown element</span> 👍（0） 💬（1）<div>老师再问下课外小贴士里说QUIC和HTTP3的变长编码使用第一个字节的高两位决定整数的长度，这里的“整数”是指哪个整数呢</div>2021-06-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1e/f2/f5/b82f410d.jpg" width="30px"><span>Unknown element</span> 👍（0） 💬（1）<div>老师问下既然gQUIC 混合了 UDP、TLS、HTTP那可不可以说gQUIC就是构建在ip协议之上呢</div>2021-05-30</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/21/eb/ea/7a0d0843.jpg" width="30px"><span>迷途羔羊</span> 👍（0） 💬（1）<div>老师你好，请教个问题。
在 HTTP2 中，是通过“流”来实现多路复用，而 TCP 可以保证流中的帧是顺序收发的，而如果在 TCP 层上如果某个包丢失了，就需要 TCP 等待重连，这样理解不知道有没有问题？
假设多个流中同时通过 TCP 收发的话，其中某个流的包需要多次重传，会影响其他流的帧收发吗？
还有一个问题，TCP 是在什么时机将缓冲的数据交给 HTTP 呢？</div>2021-02-07</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/84/19/7ed2ffa6.jpg" width="30px"><span>风</span> 👍（0） 💬（1）<div>老师,请问
在 HTTP&#47;2 把多个“请求 - 响应”分解成流，交给  TCP 后，TCP 会再拆成更小的包依次发送（其实在 TCP 里应该叫  segment，也就是“段”）

TCP是收集到一个完整的流之后再发送数据包(段)还是说收到HTTP的一个帧就会通过HTTP传输一个帧？</div>2020-07-22</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/AxgtX8ic6C7A4L1noficibBkwmJ22bUicOrRsm7zFYBoLhibpPlvERX8AGaiawHDd1apawhqFvt3PIfuC1WXIibAbtumw/132" width="30px"><span>Mingo</span> 👍（0） 💬（1）<div>值得深思</div>2020-03-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/17/0e/55/a94dee57.jpg" width="30px"><span>YK_861</span> 👍（0） 💬（1）<div>跟不上节奏了呀。</div>2019-10-31</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/79/4b/740f91ca.jpg" width="30px"><span>-W.LI-</span> 👍（0） 💬（1）<div>老师好!能问个关于nginx的问题么?
nginx配置gzip on;
后还需要在http头里加
accept encoding :gzip么?
然后还需要再header头里添加，Accept-Encoding :gzip么?
</div>2019-08-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/17/e5/4939b0c6.jpg" width="30px"><span>sunözil</span> 👍（0） 💬（1）<div>老师，针对HTTPS章节，如何查看非实验环境的密码套件呢？</div>2019-08-09</li><br/>
</ul>