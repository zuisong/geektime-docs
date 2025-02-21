在[第14讲](https://time.geekbang.org/column/article/103746)里，我曾经提到过HTTP的性能问题，用了六个字来概括：“**不算差，不够好**”。同时，我也谈到了“队头阻塞”，但由于时间的限制没有展开来细讲，这次就来好好地看看HTTP在连接这方面的表现。

HTTP的连接管理也算得上是个“老生常谈”的话题了，你一定曾经听说过“短连接”“长连接”之类的名词，今天让我们一起来把它们弄清楚。

## 短连接

HTTP协议最初（0.9/1.0）是个非常简单的协议，通信过程也采用了简单的“请求-应答”方式。

它底层的数据传输基于TCP/IP，每次发送请求前需要先与服务器建立连接，收到响应报文后会立即关闭连接。

因为客户端与服务器的整个连接过程很短暂，不会与服务器保持长时间的连接状态，所以就被称为“**短连接**”（short-lived connections）。早期的HTTP协议也被称为是“**无连接**”的协议。

短连接的缺点相当严重，因为在TCP协议里，建立连接和关闭连接都是非常“昂贵”的操作。TCP建立连接要有“三次握手”，发送3个数据包，需要1个RTT；关闭连接是“四次挥手”，4个数据包需要2个RTT。

而HTTP的一次简单“请求-响应”通常只需要4个包，如果不算服务器内部的处理时间，最多是2个RTT。这么算下来，浪费的时间就是“3÷5=60%”，有三分之二的时间被浪费掉了，传输效率低得惊人。
<div><strong>精选留言（30）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/0f/92/e4/abb7bfe3.jpg" width="30px"><span>TerryGoForIt</span> 👍（79） 💬（3）<div>老师您好，我想对于 队首阻塞 的问题，应该从 TCP 层面去解释会比较好一点吧。
&gt; 以下引用自《Web 性能权威指南》
每个 TCP 分组都会带着一个唯一的序列号被发出，而所有分组必须按顺序传送到接收端。如果中途有一个分组没能到达接收端，那么后续分组必须保存到接收端的 TCP 缓冲区，等待丢失的分组重发并到达接收端。这一切都发生在 TCP 层，应用程序对 TCP 重发和缓冲区中排队的分组一无所知，必须等待分组全部到达才能访问数据。在此之前，应用程序只能在通过套接字读数据时感觉到延迟交互。这种效应称为 TCP 的队首阻塞。</div>2019-07-05</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/81/51/4999f121.jpg" width="30px"><span>qzmone</span> 👍（58） 💬（2）<div>＂多开几个域名，比如 shard1.chrono.com、shard2.chrono.com，而这些域名都指向同一台服务器 www.chrono.com＂老师，多开几个域名，最终都是指向一个服务器，那跟都直接连一个服务器的效果一样吧，我感觉对服务器的性能要求一样呀，没有减少后端的压力</div>2019-08-05</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/e5/39/951f89c8.jpg" width="30px"><span>信信</span> 👍（57） 💬（1）<div>老师能解释下，为什么tcp握手1个rtt，挥手2个rtt吗？</div>2019-07-06</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/67/8a/babd74dc.jpg" width="30px"><span>锦</span> 👍（38） 💬（1）<div>一般使用长连接，除非明确知道只会发送一个请求，比如游戏内连接兑换码服务进行礼包兑换。
1，服务器端设置keepalive＿timeout表示多长时间没有数据则关闭连接。
2，服务器端设置keepalive_requests，表示该连接上处理多少个请求后关闭连接。
3，服务器端设置最大连接数，当连接达到上限之后拒绝连接，也可以采用限流措施等。
4，客户端设置keepalive_requests，表示该连接上发送多少个连接后关闭连接。
5，客户端设置keepalive_timeout，表示多长时间没有数据发送则关闭连接。
6，客户端设置响应超时后重试次数，当次数达到上限后关闭连接。</div>2019-07-05</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/3f/dd/4a8b6e27.jpg" width="30px"><span>披荆斩棘KK</span> 👍（29） 💬（2）<div>老师，请问高并发请求和并发连接有什么关系吗？
负载均衡解决高并发问题是并发连接吗？</div>2019-07-05</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/b4/ee/c3ff8615.jpg" width="30px"><span>恒</span> 👍（23） 💬（2）<div>老师看下我总结的对不对，谢谢！
短连接：每次“请求-响应”都先建立tcp连接，完后关闭连接。这样三次握手1.5个rtt，“请求-响应”2个rtt(里面有两个ack)，四次挥手2个rtt，效率极低。适用于少次请求，例如客户端只会对某个服务器发送几次请求后就不再发送。
	
长连接：建立tcp连接后不立即关闭，后续http请求复用这个tcp连接。http&#47;1.1默认开启。如果有大量的空闲长连接只连不发占用资源，可能导致耗尽资源“拒绝服务”即DDoS。因此服务器常会设置超时时间或最大请求数。

这里的“连接”其实是对某个域名的，而不是某个ip或主机。而浏览器对单个域名的并发连接数量有限制，一般为6~8个，所以为了进一步提高连接数就有了“域名分片”技术，即将原来一个域名分成多个域名，但最后指向的服务器还是原来那一台。
例如把www.chrono.com分成shard1.chrono.com, 和 shard2.chrono.com，但还是指向原来那台服务器。这虽然提高了客户端的并发数，但反而增加了服务器端的压力。

连接相关头字段
Connection: keep-alive
在请求头里表明要求使用长连接，在响应头里表明支持使用长连接。
Connection: close
在请求头里表明告诉服务器这次通信后关闭长连接，在响应头里表明服务器将关闭长连接。
[Connection: Upgrade，配合101状态码表示协议升级，例如从http切换到WebSocket]</div>2019-10-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/5e/27/a871073d.jpg" width="30px"><span>小M</span> 👍（20） 💬（2）<div>个人理解，不能把http的队首阻塞归结于请求-响应机制。
tcp是全双工的，完全可以在一个tcp连接上双端同时进行收发。http只是在tcp连接上流动的一堆数据而已，应用层的数据不存在队首阻塞。问题在于http协议自身：它无法明确的标识出某个rsp是哪个req的。如果服务端不等待上一个req-rsp结束就发出另一个rsp，那么客户端无法区分收到的数据。
单连接上的多路复用也是基于请求-响应机制的，虽然一个连接上同时流动着多个req-rsp的数据，但是应用层协议有序号可以区分出rsp是哪个req的。</div>2021-03-07</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/cb/9d/2bc85843.jpg" width="30px"><span>　　　　　　　鸟人</span> 👍（17） 💬（1）<div>拒绝服务应该是dos  ddos是分布式dos</div>2019-07-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/ee/28/c04a0c83.jpg" width="30px"><span>小炭</span> 👍（13） 💬（4）<div>浪费的时间就是“3÷5=60%” 这个算法不是很理解，分子&#47;分母是怎么来的</div>2019-11-15</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/79/4b/740f91ca.jpg" width="30px"><span>-W.LI-</span> 👍（12） 💬（1）<div>谢谢老师!讲的很形象，有个问题，长链接。课后小贴士写了区分请求和应答。一个长链接，同一时间只能发送一个请求是么?等到收到服务器响应以后才能被别的请求复用?假如有一个视频的请求一直占着。在分段传输的间隙能发送别的请求么?
“域名分片”（domain sharding）技术，具体怎么实现啊后面仔细会讲么?那个域名的比喻没看太懂。是一个浏览器持有同一个服务的，多个负载的链接的意思么(一台服务器8个最多)服务器有集群浏览器创建了8*n个链接。每台负载最多只让一个浏览器连了8个。
域名解析不是DNS服务器做的么，不是直接解析成IP的么还能域名指向域名么?完全不懂</div>2019-07-05</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/18/cd/4b/36396a18.jpg" width="30px"><span>独钓寒江雪</span> 👍（10） 💬（1）<div>其实感觉本节用地铁站做例子更好：

地铁站相当于服务器；
地铁站有多个出入口，对应域名分片；
每个口有多条道，每条道对应一个连接；
每条道有开和关，对应握手和挥手；
人刷卡通过就传递了数据信息。</div>2020-02-01</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTKVUskibDnhMt5MCIJ8227HWkeg2wEEyewps8GuWhWaY5fy7Ya56bu2ktMlxdla3K29Wqia9efCkWaQ/132" width="30px"><span>衬衫的价格是19美元</span> 👍（9） 💬（2）<div>服务器或者客户端是怎么是判断一个连接的呢？是不是有一个id来对应一个连接？一个连接具体是什么东西呢？是双方在内存中开辟的空间吗？
</div>2019-07-05</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/e8/55/63189817.jpg" width="30px"><span>MClink</span> 👍（7） 💬（3）<div>老师，我们都知道tcp要三次握手来保证连接成功，但是老是有人问为什么是三次，不是四次，不是五次，如果面试官这么问的话，我们应该怎么回答才能是较为准确呢？我也只能说两次无法确认，三次足够确认，四次就多余了，每三次就是一个有效的循环</div>2020-04-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/9c/28/87421d8f.jpg" width="30px"><span>Happy-Coming</span> 👍（6） 💬（1）<div>打卡机器比喻非常棒</div>2019-12-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/ff/a4/55520286.jpg" width="30px"><span>answer宫</span> 👍（6） 💬（4）<div>老师 ,请问为什么此请求是两个RTT啊,我理解一个就够了啊,一次请求,一次响应,一来一回就ok了吧,没有想通为什么是2个RTT</div>2019-11-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/3d/03/b2d9a084.jpg" width="30px"><span>Hale</span> 👍（5） 💬（1）<div>对头阻塞 是http协议层实现的，还是tcp 中listen(blocklog) 实现的？二者有关系吗？</div>2020-04-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/75/00/618b20da.jpg" width="30px"><span>徐海浪</span> 👍（4） 💬（1）<div>1. 在开发基于 HTTP 协议的客户端时应该如何选择使用的连接模式呢？短连接还是长连接？
根据请求的频繁程度来选择连接模式。一次性的请求用短链接，频繁与服务端交互的用长连接。
2. 应当如何降低长连接对服务器的负面影响呢？
长连接会长期占用服务器资源，根据服务器性能设置连接数和长连接超时时间，保证服务器TCP资源使用处于正常范围。</div>2019-07-07</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/67/f4/9a1feb59.jpg" width="30px"><span>钱</span> 👍（3） 💬（1）<div>1：在开发基于 HTTP 协议的客户端时应该如何选择使用的连接模式呢？短连接还是长连接？
这个视业务场景而定，只要一次交互就行了，也就是只有一次来回就OK，那就短链接，否则就长连接。
罗老师，请教一下短链接和长链接，表面上的长短是指连接存活的长短，不过如果使用短链接的请求和响应时间比较长时，短链接的存活时间也可能比长链接长的吧？连接的长短核心在于关闭连接的机制而非实际存活长短是吧？当然，一般而言长链接的存活时间是比短链接长的。另外，长链接和回话的存活时间是两个不同的概念吧？他们有什么联系嘛？

2：应当如何降低长连接对服务器的负面影响呢？
使用一定的保护措施，比如：文中讲的按超时时间或请求次数来关闭连接，也可以搞一个连接池来防护服务器。

老师的例子很棒，生动形象跃然于脑，另外，浏览器建立多个连接看评论服务器端口是一个浏览器是随机的，换言之多个连接在浏览器侧是多个端口在服务器侧是一个端口，这是为什么？感觉有些疑惑，另外请教一下一个端口能建立多少个连接？长链接的超时时间一般设置为多少，怎么考虑的？
</div>2020-03-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/17/b0/9f/ea75aa8e.jpg" width="30px"><span>李扬翼</span> 👍（3） 💬（2）<div>老师，http2在应用层解决了队头阻塞，那TCP传输层的队头阻塞如何解决呢？</div>2019-09-30</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/4d/fd/0aa0e39f.jpg" width="30px"><span>许童童</span> 👍（3） 💬（1）<div>老师：请教一个问题。为什么我看很多网站HTTP请求都没有返回头里都没有Connection: Keep-Alive。有的网站却有。那些没有返回的是没有使用长连接吗？</div>2019-07-05</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTIuTjCibv0afd7SSdLicfNk0f7KO5ga9VMleD1hc2DtQfianK20ht06SekClKV7M8UXLRHqQLm9hJ3ow/132" width="30px"><span>Jasmine</span> 👍（2） 💬（2）<div>一次请求响应为什么是4个数据包呢？</div>2021-04-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/93/ff/87d8de89.jpg" width="30px"><span>snake</span> 👍（2） 💬（1）<div>这里的HTTP并发连接指的是TCP连接吗？</div>2020-06-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/9b/c8/665100a3.jpg" width="30px"><span>周曙光爱学习</span> 👍（2） 💬（1）<div>老师请教一个问题: 长连接肯定是客户端(ip:port)和某个服务器(ip:port)建立的，比如我们访问某个域名，但是这个域名背后可能有多个服务器，应该怎么理解这个这个长连接建立的双方呢？</div>2019-12-07</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/e9/0b/1171ac71.jpg" width="30px"><span>WL</span> 👍（2） 💬（1）<div>请问一下老师域名分片技术是不是让一个浏览器跟不同的域名都建立长连接, 而这些域名都指向同一个服务器集群?</div>2019-07-05</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/26/eb/d7/90391376.jpg" width="30px"><span>ifelse</span> 👍（1） 💬（1）<div>可以学习java的Tomcat服务器，采用连接池技术</div>2023-01-25</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/18/80/f4/564209ea.jpg" width="30px"><span>纳兰容若</span> 👍（1） 💬（2）<div>老师您好 17-1 我连续F5好多次 connection一直是keep-alive，是不是我哪里操作错了 
感谢老师的答复</div>2021-04-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/68/fd/3b65f3b2.jpg" width="30px"><span>陈文东</span> 👍（1） 💬（1）<div>作为 HTTP&#47;1.x 的连接，请求是序列化的，哪怕本来是无序的，在没有足够庞大可用的带宽时，也无从优化。一个解决方案是，浏览器为每个域名建立多个连接，以实现并发请求。曾经默认的连接数量为 2 到 3 个，现在比较常用的并发连接数已经增加到 6 条。如果尝试大于这个数字，就有触发服务器 DoS 保护的风险。

如果服务器端想要更快速的响应网站或应用程序的应答，它可以迫使客户端建立更多的连接。例如，不要在同一个域名下获取所有资源，假设有个域名是 www.example.com，我们可以把它拆分成好几个域名：www1.example.com、www2.example.com、www3.example.com。所有这些域名都指向同一台服务器，浏览器会同时为每个域名建立 6 条连接(在我们这个例子中，连接数会达到 18 条)。这一技术被称作域名分片。

----
以上内容应用的Mozilla 开发文档这段解释就比较清楚，对域名分片。</div>2021-02-25</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/DYAIOgq83eqjbwXwF3YUcSw7A8v6f0sAYzQMloOWg62aciaGfzZWibRw2jjTja1Vwh5CLVGZdseM6gSBnC1hRzEQ/132" width="30px"><span>firstblood</span> 👍（1） 💬（2）<div>老师好，有个疑问，对于一个域名最多6-8个链接是指，无论我开多少个页面，只要是同一个域名，就是最多6-8个，还是一个页面最多6-8个？</div>2020-05-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/1e/3f/5fc064d4.jpg" width="30px"><span>Edward_Elric</span> 👍（1） 💬（1）<div>用3÷5=60%来理解 3÷9≈33% 有点解释不通，分子3个RTT是长连接的握手和挥手的损耗,分母9个RTT是假如此次是短连接会浪费9个，3&#47;9 说是长连接的浪费率不对吧、(浪费&#47;总的=浪费率）.不明白3÷9≈33% ，求老师解释，谢谢！</div>2019-12-02</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/cf/2f/4f89f22a.jpg" width="30px"><span>李鑫磊</span> 👍（1） 💬（1）<div>请问老师“开发基于 HTTP 协议的客户端”是什么意思？</div>2019-11-30</li><br/>
</ul>