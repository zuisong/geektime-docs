在之前讲TCP/IP协议栈的时候，我说过有“TCP Socket”，它实际上是一种功能接口，通过这些接口就可以使用TCP/IP协议栈在传输层收发数据。

那么，你知道还有一种东西叫“WebSocket”吗？

单从名字上看，“Web”指的是HTTP，“Socket”是套接字调用，那么这两个连起来又是什么意思呢？

所谓“望文生义”，大概你也能猜出来，“WebSocket”就是运行在“Web”，也就是HTTP上的Socket通信规范，提供与“TCP Socket”类似的功能，使用它就可以像“TCP Socket”一样调用下层协议栈，任意地收发数据。

![](https://static001.geekbang.org/resource/image/ee/28/ee6685c7d3c673b95e46d582828eee28.png?wh=1142%2A502)

更准确地说，“WebSocket”是一种基于TCP的轻量级网络通信协议，在地位上是与HTTP“平级”的。

## 为什么要有WebSocket

不过，已经有了被广泛应用的HTTP协议，为什么要再出一个WebSocket呢？它有哪些好处呢？

其实WebSocket与HTTP/2一样，都是为了解决HTTP某方面的缺陷而诞生的。HTTP/2针对的是“队头阻塞”，而WebSocket针对的是“请求-应答”通信模式。

那么，“请求-应答”有什么不好的地方呢？

“请求-应答”是一种“**半双工**”的通信模式，虽然可以双向收发数据，但同一时刻只能一个方向上有动作，传输效率低。更关键的一点，它是一种“被动”通信模式，服务器只能“被动”响应客户端的请求，无法主动向客户端发送数据。
<div><strong>精选留言（30）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/0f/4d/fd/0aa0e39f.jpg" width="30px"><span>许童童</span> 👍（32） 💬（2）<div>思考题：
1.WebSocket 和 HTTP&#47;2 都是用来弥补HTTP协议的一些缺陷和不足，WebSocket 主要解决双向通信、全双工问题，HTTP&#47;2 主要解决传输效率的问题，两者在二进制帧的格式上也不太一样，HTTP&#47;2 有多路复用、优先级和流的概念。

2.试着自己解释一下 WebSocket 里的”Web“和”Socket“的含义。
Web就是HTTP的意思，Socket就是网络编程里的套接字，也就是HTTP协议上的网络套接字，可以任意双向通信。

3.结合自己的实际工作，你觉得 WebSocket 适合用在哪些场景里？
IM通信，实时互动，回调响应，数据实时同步。</div>2019-08-23</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTI3F4IdQuDZrhN8ThibP85eCiaSWTYpTrcC6QB9EoAkw3IIj6otMibb1CgrS1uzITAnJmGLXQ2tgIkAQ/132" width="30px"><span>cugphoenix</span> 👍（22） 💬（1）<div>是不是可以这样理解：HTTP是基于TCP的，通过TCP收发的消息用HTTP的应用层协议解析。WebSocket是首先通过HTTP协议把TCP链接建好，然后通过Upgrade字段进行协议转换，在收到服务器的101 Switching Protocols应答之后，后续的TCP消息就通过WebSocket协议解析。</div>2020-02-07</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/9b/a8/6a391c66.jpg" width="30px"><span>geraltlaush</span> 👍（13） 💬（3）<div>工作场景遇到过用户订阅股票的股价，股价波动时实时推送给海量订阅的用户，面试场景被问到两次，一 千万粉丝的明星发布动态如何推送给粉丝 二 海量用户的主播直播如何推送弹幕 当时回答消息队列，其实web socket才是比较好的方案</div>2019-08-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/1d/64/52a5863b.jpg" width="30px"><span>大土豆</span> 👍（9） 💬（1）<div>WebSocket定义为tcp over web，我个人感觉是不妥的，应该是&quot;可靠有序的传输层 + 实现组包协议的应用层的长连接方案 over web&quot;。WebSocket和HTTP已经有包的结构了,业务直接可以用了，浏览器A发一个websocket包，比如说数据是1234，给服务器，服务器可以获取这个包，数据是1234，和http一样了。而tcp还是原始的没头没尾的字节流，想要通讯，还得再自定义一个应用层的协议。</div>2020-02-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/81/4e/d71092f4.jpg" width="30px"><span>夏目</span> 👍（5） 💬（1）<div>两年前我实习的时候公司项目用过，到现在我才搞清楚和http的区别，惭愧…</div>2019-12-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/e8/91/e05a03a0.jpg" width="30px"><span>ccx</span> 👍（4） 💬（1）<div>在 FINTECH 领域工作了几年了，自研发的外汇&#47;数字货币交易系统的行情模块基本都是 websocket 实现的；另外还遇到一个有意思的场景，就是 discord 的机器人 Slash Commands 的实现也是基于 websocket  的。</div>2021-09-30</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/ba/bf/e9a44c63.jpg" width="30px"><span>chao</span> 👍（4） 💬（1）<div>1、第二个字节后 7 位是“Payload len”，表示帧内容的长度。它是另一种变长编码，最少 7 位，最多是 7+64 位，也就是额外增加 8 个字节，所以一个 WebSocket 帧最大是 2^64。
2、如果数据的长度小于等于125个字节，则用默认的7个bit来标示数据的长度；
如果数据的长度为126个字节，则用后面相邻的2个字节来保存一个16bit位的无符号整数作为数据的长度；
如果数据的长度大于等于127个字节，则用后面相邻的8个字节来保存一个64bit位的无符号整数作为数据的长度；
老师，2是其它地方看到的，Payload len 这样设计的原因是什么，以及没明白为啥126个字节的长度要用16bit来表示</div>2019-09-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/23/40/c8/17af3598.jpg" width="30px"><span>Evan Xia</span> 👍（2） 💬（1）<div>我们的业务场景是在下黑白棋的过程双方都能实时收到对方的落子， 用的是一个封装好的Centrifugo库，期间遇到最多的就是网络不好重连的问题</div>2022-05-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/60/4f/db0e62b3.jpg" width="30px"><span>Daiver</span> 👍（2） 💬（2）<div>还有socket.io，算是websocket的超集了。</div>2020-01-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/fa/5d/735fdc76.jpg" width="30px"><span>╭(╯ε╰)╮</span> 👍（1） 💬（3）<div>有个问题 30课介绍http2的时候不能重复使用443端口，所以重新用了8443端口。这节课websocket为什么就能跟http一起复用443端口呢？</div>2023-01-20</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTIuTjCibv0afd7SSdLicfNk0f7KO5ga9VMleD1hc2DtQfianK20ht06SekClKV7M8UXLRHqQLm9hJ3ow/132" width="30px"><span>Jasmine</span> 👍（1） 💬（1）<div>第二个字节后 7 位是“Payload len”，表示帧内容的长度。它是另一种变长编码，最少 7 位，最多是 7+64 位，也就是额外增加 8 个字节，所以一个 WebSocket 帧最大是 2^64。——这里最大的帧为什么不说是2^71呢？</div>2021-11-22</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/WtHCCMoLJ2DvzqQwPYZyj2RlN7eibTLMHDMTSO4xIKjfKR1Eh9L98AMkkZY7FmegWyGLahRQJ5ibPzeeFtfpeSow/132" width="30px"><span>脱缰的野马__</span> 👍（1） 💬（1）<div>老师你好，请问服务端在使用websocket主动推送信息给客户端的时候，是如何知道客户端的呢？另外服务端要主动推送的客户端有成千上万个，哪又如何推送？不像客户端请求服务端，客户端请求服务端是使用http，有ip和端口。</div>2021-03-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/18/ed/a9/662318ab.jpg" width="30px"><span>我母鸡啊！</span> 👍（1） 💬（1）<div>3.结合自己的实际工作，你觉得 WebSocket 适合用在哪些场景里？
最近在做直播功能的项目，就用到了websovket的去做用户评论的推送，观看人数等的功能。</div>2020-05-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/67/f4/9a1feb59.jpg" width="30px"><span>钱</span> 👍（1） 💬（1）<div>1：WebSocket 与 HTTP&#47;2 有很多相似点，比如都可以从 HTTP&#47;1 升级，都采用二进制帧结构，你能比较一下这两个协议吗？
初心不一样，WebSocket核心是实现全双工通信，可以重分的利用网络的通信能力，实现全双工后服务器就不总是被动的响应了，也可以主动邀请浏览器喝咖啡。HTTP&#47;2核心是提高数据的传输效率，通过多路复用的方式来实现。

2：试着自己解释一下 WebSocket 里的”Web“和”Socket“的含义。
Web主要强调浏览器或者网页相关的应用吧！
Socket主要强调他是在TCP上的一层薄薄的封装，实现通信方式比较简单考向底层。

3：结合自己的实际工作，你觉得 WebSocket 适合用在哪些场景里？
目前还没用到，他核心解决的是全双工通信问题，HTTP早就就解决了浏览器侧的主动请求，那他的出现主要方便了想发起主动请求的服务器这一侧。只有是服务器想主动推送数据的场景也许都合适，比如：数据变动主动推送，不用客户端不断轮询。</div>2020-04-05</li><br/><li><img src="" width="30px"><span>Geek_5b0e47</span> 👍（1） 💬（1）<div>向客户端监控屏推送时实更新数据，可以使用websocket</div>2020-03-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/7b/f0/ccc11dec.jpg" width="30px"><span>Cris</span> 👍（1） 💬（1）<div>老师，我想问下，uri里的端口号，有什么用？为什么它是和协议对应的（http默认80，https默认443），却又写在域名的后面？</div>2019-08-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/75/00/618b20da.jpg" width="30px"><span>徐海浪</span> 👍（1） 💬（2）<div>1. WebSocket 与 HTTP&#47;2 有很多相似点，比如都可以从 HTTP&#47;1 升级，都采用二进制帧结构，你能比较一下这两个协议吗？
差别：HTTP&#47;2是请求与响应的模式，而WebSocket是双向的，服务器也可以主动向客户端发起请求。
2. 试着自己解释一下 WebSocket 里的”Web“和”Socket“的含义。
是基于web服务器，类似于tcp的socket方式来使用的协议。
3. 结合自己的实际工作，你觉得 WebSocket 适合用在哪些场景里？
我在实际工作中还没有用到WebSocket，觉得适合服务器主动推送的客户端的场景，比如站内信或者站内聊天，或者在线页游？</div>2019-08-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/79/4b/740f91ca.jpg" width="30px"><span>-W.LI-</span> 👍（1） 💬（1）<div>老师好!websocket单机服务器能支持多少链接啊?之前没用过websocket。看帖子好像是通过key-value形式存储所有链接。需要用得时候通过key拿到链接往外写数据。希望老师科普下web socket的简单应用和实现，性能分析。
需要服务器主动推的感觉都可以用websocket做。
聊天工具:用户A，用户B，
A-&gt;服务器(保存聊天记录)-&gt;B;B-&gt;服务器(保存聊天记录)-&gt;A;是这样么?</div>2019-08-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/23/6c/785d9cd3.jpg" width="30px"><span>Snooker</span> 👍（0） 💬（1）<div>1.除了双向推送消息外，websocket创建链接后的消息收发，相比http是可以省去头部等字段信息？
3.工作场景：主要是直播场景下的一些信息交互，例如：消息的主动推送，像直播间主播推送的商品信息、全频道的消息广播：榜一大哥刷🚀、状态维护：上下麦状态、音视频开关状态等
</div>2024-07-01</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/c0/6c/29be1864.jpg" width="30px"><span>随心而至</span> 👍（0） 💬（1）<div>如果是想用 web socket 做大模型的流式输出，就不要设置 fin 为 0，否则 web socket client 会默认等拿到 fin 为 1 的 fragement 并且合并好，再给应用。
</div>2024-06-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/fa/5d/735fdc76.jpg" width="30px"><span>╭(╯ε╰)╮</span> 👍（0） 💬（1）<div>websocket包装成http协议不应该就是按照http协议的“请求-应答”模式收发数据了嘛，还是没理解怎么实现的全双工？服务器向客户端推消息先封装成websocket帧，帧再模拟成fttp协议，然后http协议不支持推送，这不是没办法进行下去了嘛？</div>2023-01-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/98/1c/d7a1439e.jpg" width="30px"><span>KaKaKa</span> 👍（0） 💬（1）<div>请问下老师，握手的请求只能用 GET 吗？能用POST吗？如果不能是因为什么？</div>2023-01-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1e/f2/f5/b82f410d.jpg" width="30px"><span>Unknown element</span> 👍（0） 💬（2）<div>老师问下
1.Web socket既然没有流的概念那具体是怎么实现全双工的呢  两边都同时收发那包的顺序就乱了吧
2.Web socket帧里帧长度最大是7+64位那最长不应该是2^71位吗  为什么课程里说最长是2^64？</div>2021-06-04</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/c0/5c/10111544.jpg" width="30px"><span>张峰</span> 👍（0） 💬（1）<div>服务器发送事件（Server-sent Events）是基于 WebSocket 协议的一种服务器向客户端发送事件和数据的单向通讯。
HTML5 服务器发送事件（server-sent event）允许网页获得来自服务器的更新。

老师能讲解一下 Server-sent Events 和 websocket的相同和不同。</div>2021-04-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1b/b8/79/a4dbe9ee.jpg" width="30px"><span>blueBean</span> 👍（0） 💬（1）<div>帧那里，第一个字节的第一位应该就是一个bit吧，为啥能放下FIN这个字段呢？想不通</div>2021-04-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/24/b9/b9/9e4d7aa4.jpg" width="30px"><span>乘风破浪</span> 👍（0） 💬（4）<div>罗大师，所有WS的页面都无法打开，错误提示如下，
无法访问此网站网址为 ws:&#47;&#47;www.chrono.com:8080&#47;srv 的网页可能暂时无法连接，或者它已永久性地移动到了新网址。
ERR_DISALLOWED_URL_SCHEME

无法访问此网站网址为 ws:&#47;&#47;127.0.0.1&#47;38-0 的网页可能暂时无法连接，或者它已永久性地移动到了新网址。
ERR_DISALLOWED_URL_SCHEME

wireshark也抓不到任何包
</div>2021-01-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/12/4e/ff0702fc.jpg" width="30px"><span>火锅小王子</span> 👍（0） 💬（1）<div>老师您好，可以解释一下其中的帧是如何具体划分的吗 比如发送一个大的内容 ，分割帧有什么依据，还是说依赖mss或者滑动窗口这些内容？</div>2020-09-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/19/e4/4f/df6d810d.jpg" width="30px"><span>Maske</span> 👍（0） 💬（2）<div>1.都是建立在tcp&#47;ip之上，默认端口和http(s)一样。不同点：http2专注于解决http1.1的性能问题。websocket是一种全双工通信协议，解决的是能够让服务器端主动推送数据给客户端的问题，使得web应用不再局限于‘请求——应答’模式。
2.‘web’表示是基于web浏览器层面的，在前端通过js动态控制网络的连接与断开、数据收发操作。socket是一种应用进程与网络通信协议之间的连接机制。
3.实时聊天应用，金融领域的股价股指等走势图的绘制也需要实时获取最新的数据，导航应用也需要获取实时路况。</div>2020-06-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/18/ed/a9/662318ab.jpg" width="30px"><span>我母鸡啊！</span> 👍（0） 💬（1）<div>1.WebSocket 与 HTTP&#47;2 有很多相似点，比如都可以从 HTTP&#47;1 升级，都采用二进制帧结构，你能比较一下这两个协议吗？

websocket里面有帧的概念，却没有http2.0里的虚拟流的概念，也不存在优先级，多路复用。websocket的出现本质上还是为了解决http的半双工的问题，变成全双工，服务器和客户端可以随意通行的问题</div>2020-05-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1b/58/b0/417b4117.jpg" width="30px"><span>哎呦歪</span> 👍（0） 💬（1）<div>老师，你好。我想问一下既然 http&#47;2 也可以 Server push，那么是不是也可以理解是 全双工，websocket和 http&#47;2 在 Server push 上有什么区别？ </div>2020-05-03</li><br/>
</ul>