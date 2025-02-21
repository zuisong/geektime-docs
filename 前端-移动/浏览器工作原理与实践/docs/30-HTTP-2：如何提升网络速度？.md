[上一篇文章](https://time.geekbang.org/column/article/147501)我们聊了HTTP/1.1的发展史，虽然HTTP/1.1已经做了大量的优化，但是依然存在很多性能瓶颈，依然不能满足我们日益变化的新需求，所以就有了我们今天要聊的HTTP/2。

本文我们依然从需求的层面来谈，先分析HTTP/1.1存在哪些问题，然后再来分析HTTP/2是如何解决这些问题的。

我们知道HTTP/1.1为网络效率做了大量的优化，最核心的有如下三种方式：

1. 增加了持久连接；
2. 浏览器为每个域名最多同时维护6个TCP持久连接；
3. 使用CDN的实现域名分片机制。

通过这些方式就大大提高了页面的下载速度，你可以通过下图来直观感受下：

![](https://static001.geekbang.org/resource/image/91/c5/91c3e0a8f13ebc4d81f08d8604f770c5.png?wh=1142%2A849)

HTTP/1.1的资源下载方式

在该图中，引入了CDN，并同时为每个域名维护6个连接，这样就大大减轻了整个资源的下载时间。这里我们可以简单计算下：如果使用单个TCP的持久连接，下载100个资源所花费的时间为100 * n * RTT；若通过上面的技术，就可以把整个时间缩短为100 * n * RTT/(6 * CDN个数)。从这个计算结果来看，我们的页面加载速度变快了不少。

## HTTP/1.1的主要问题

虽然HTTP/1.1采取了很多优化资源加载速度的策略，也取得了一定的效果，但是HTTP/1.1**对带宽的利用率却并不理想**，这也是HTTP/1.1的一个核心问题。
<div><strong>精选留言（30）</strong></div><ul>
<li><img src="" width="30px"><span>moss</span> 👍（21） 💬（6）<div>老师好，采用了HTTP&#47;2之后，雪碧图是不是彻底不需要了呢？而且多张图片变成雪碧图后，多张图片大小加和都没有一张雪碧图大，那是不是雪碧图反而让传输更慢了呢？</div>2019-10-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/8f/c9/833d5060.jpg" width="30px"><span>玉皇大亮</span> 👍（4） 💬（5）<div>有个疑问想请教老师，既然HTTP1.1为了并行下载资源为每个域名提供了6个TCP连接，那这6个TCP连接是并行传输数据的么？如果是为什么还会有队头阻塞的问题呢？这里没搞明白，或者其他同学明白的帮忙回答一下呗，感谢感谢</div>2019-12-05</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/44/0e/ce14b7d3.jpg" width="30px"><span>-_-|||</span> 👍（3） 💬（1）<div>HTTP&#47;2 下浏览器获取的所有请求数据都会经过 &quot;二进制分帧层&quot; 吗?</div>2019-12-16</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1a/e9/7b/b844f3a4.jpg" width="30px"><span>匡晨辉</span> 👍（1） 💬（4）<div>老师，还是没有理解http2怎么就能解决队头阻塞问题呢？http2 还是基于tcp连接的，经过二进制分帧层了以后不还是需要以数据包的形式通过tcp传输吗？tcp的数据包队头阻塞发生了不还是会影响后面的请求数据包的发送吗？</div>2019-12-18</li><br/><li><img src="" width="30px"><span>vianem</span> 👍（0） 💬（1）<div>带宽那有点问题吧？一般我们说的100M带宽，是指100Mbps，转换成MBps得除以8</div>2019-12-05</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/a1/8e/03aeb9df.jpg" width="30px"><span>Rocky</span> 👍（0） 💬（1）<div>tcp的队头阻塞虽然是缺点，但也从另一个方面保证了数据传输的可靠性，前一个没有完成或者出错，可以重传。改用udp后可能会丢帧，不可靠</div>2019-11-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/84/ee/3a364ccd.jpg" width="30px"><span>滇西之王</span> 👍（66） 💬（1）<div>在tcp层 Tls层以上的数据都是tcp层的数据，tcp层对每个数据包都有编号，分为1，2，3 .... tcp保证双向稳定可靠的传输，如果2包数据丢失，1号包和3号包来了，那么在超时重传时间还没有收到2编号数据包，服务端会发送2号数据包，客服端收到之后，发出确认，服务端才会继续发送其他数据，客服端数据才会呈现给上层应用层，这样tcp层的阻塞就发生了</div>2019-10-12</li><br/><li><img src="" width="30px"><span>Geek_1e6198</span> 👍（30） 💬（6）<div>刚出去面试就被问到了,而且很多都是老师这个专栏下的问题 让我怀疑是不是面试官刚看过这个</div>2020-08-06</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/1e/71/54ff7b4e.jpg" width="30px"><span>3Spiders</span> 👍（16） 💬（1）<div>TCP的队头阻塞，TCP传输过程中也是把一份数据分为多个数据包的。当其中一个数据包没有按照顺序返回，接收端会一直保持连接等待数据包返回，这时候就会阻塞后续请求。</div>2019-10-12</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTJxhkqxtWKQeYrYlVYphlicHXW5KmHAvibx6hmice4NTvmn60ZEfTpLp3480umVEquqPdMfwOnecj6Aw/132" width="30px"><span>焦糖大瓜子</span> 👍（10） 💬（4）<div>HTTP&#47;2请求是如何设置请求的优先级？</div>2020-06-02</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/DYAIOgq83eo3yW0arVaSoQiccftUPYo0LZqRHicMEbqjoBVkEVNw405S7OL5dlFDqVibdyudpPaVQkbxwcywJ1bNg/132" width="30px"><span>小智</span> 👍（7） 💬（3）<div>浏览器是如何判断选择http1，http1.1，http2的。对应的部署是不是也要有回退机制，比如检测到浏览器不支持http2，就返回http1的模式？</div>2019-10-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/18/3c/e3/aee9692f.jpg" width="30px"><span>CMS</span> 👍（4） 💬（3）<div>能不能再详细讲一下：使用 CDN 的实现域名分片机制。</div>2020-01-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/11/5d/0d955f19.jpg" width="30px"><span>安思科</span> 👍（4） 💬（1）<div>前几天，http3已经在chrome和curl试用，使用UDP试图解决对头阻塞问题。</div>2019-10-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/eb/09/ba5f0135.jpg" width="30px"><span>Chao</span> 👍（4） 💬（1）<div>由于多路复用，反而产生队头阻塞时， 影响比http1.1更为巨大。 
在目前TCP下解决这个问题还是很困难的</div>2019-10-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/6a/22/527904b2.jpg" width="30px"><span>hao-kuai</span> 👍（3） 💬（0）<div>1. HTTP 0.9 到 HTTP 1.0 是功能增强
2. HTTP 1.0 到 HTTP 1.1 是性能优化
3. HTTP 1.1 到 HTTP 2.1 是性能优化及顺带功能增强
4. 再次遇到可暂停可恢复增量任务调度，相信以后还会遇到：V8的垃圾回收老生代区域算法、HTTP&#47;2多路复用技术、React的Fiber调度算法</div>2021-12-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/ef/a2/6ea5bb9e.jpg" width="30px"><span>LEON</span> 👍（3） 💬（1）<div>老师http2 是不是必须要使用https? 如果不用https可以吗？</div>2019-12-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/55/28/66bf4bc4.jpg" width="30px"><span>荷兰小猪8813</span> 👍（2） 💬（0）<div>TCP 队头阻塞

TCP 是面向连接的、可靠的流协议，其为上层应用提供了可靠的传输，保证将数据有序并且准确地发送至接收端。为了做到这一点，TCP 采用了 “顺序控制” 和 “重发控制” 机制，另外还使用 “流量控制” 和 “拥塞控制” 来提高网络利用率。

应用层（如 HTTP）发送的数据会先传递给传输层（TCP），TCP 收到数据后并不会直接发送，而是先把数据切割成 MSS 大小的包，再按窗口大小将多个包丢给网络层（IP 协议）处理。

IP 层的作用是 “实现终端节点之间的通信”，并不保证数据的可靠性和有序性，所以接收端可能会先收到窗口末端的数据，这个时候 TCP 是不会向上层应用交付数据的，它得等到前面的数据都接收到了才向上交付，所以这就出现了队头阻塞，即队头的包如果发生延迟或者丢失，队尾必须等待发送端重新发送并接收到数据后才会一起向上交付。

当然 TCP 有快重传和快恢复机制，一旦收到失序的报文段就立即发出重复确认，并且接收端在连续收到三个重复确认时，就会把慢开始门限减半，然后执行拥塞避免算法，以快速重发丢失的报文。</div>2023-04-02</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/b4/94/2796de72.jpg" width="30px"><span>追风筝的人</span> 👍（1） 💬（0）<div>Http2 优点  多路复用  ，二进制流传输数据，  Hpack算法头部字段压缩，服务器主动推送，请求优先级的设置，部分解决了队头阻塞，原因是基于TCP协议传输，Http3 基于QUIC协议下的UDP协议，解决了队头阻塞。</div>2020-02-25</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/a4/eb/c092f833.jpg" width="30px"><span>晓东</span> 👍（1） 💬（4）<div>同一个域名用一个tcp解决了慢启动的问题，并且tcp带宽的竞争也少了6倍。但是本来可以6个tcp同时下载同一个域名的资源，现在只能用一个tcp了，我这个理解对么？</div>2020-01-15</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/26/eb/d7/90391376.jpg" width="30px"><span>ifelse</span> 👍（0） 💬（0）<div>学习打卡</div>2024-05-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/66/b1/40a25f84.jpg" width="30px"><span>不利于团结的话不要说</span> 👍（0） 💬（2）<div>http2相同域名建立一个tcp连接是以页面维度，还是浏览器维度。
譬如打开京东的两个不同的页面，两个页面都调用了京东相同域名的oss图片服务，那么浏览器是建立了一个连接，还是两个连接呢</div>2023-05-25</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/4a/b1/e2b9e94f.jpg" width="30px"><span>六个周</span> 👍（0） 💬（1）<div>Chrome有个机制，同一个域名同时最多只能建立6个TCP连接，若此刻同时有10个请求发生。则4个会进入TCP队列进行排队。 
然后在HTTP&#47;1.1中增加了持久性连接方法，一个TCP上可以传输多个HTTP请求。

结合这两句话，有点懵逼了，一个TCP上可以传输多个HTTP请求这句话该怎么理解呢？
意思是不是说，在访问一个网站的时候，浏览器提供了6个TCP管道，然后你这个网站同时有十个请求发生，那么六个进入了这个TCP管道，还有四个在排队，当六个中有一个结束之后，然后四个排队中的出来一个，然后又用这个管道，但是这个时候，这个管道就不用在此建立TCP连接了，也就是说一个TCP上可以传输多个HTTP请求，是这个意思吗？求老师，大神们指点啊，在这里的理解上有点出不来了。</div>2022-04-12</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/DYAIOgq83eqLlZ7ibJqRocm0EM4YF8iaJJFeicGI9U0gh5ZLeWTjXeicOFlT4tjKtIz8SpGqBPXAspLMbWD5GnrdhQ/132" width="30px"><span>痴人指路</span> 👍（0） 💬（0）<div>http2中，浏览器短时间内发送多个请求是 一起被二进制分帧层处理吗？还是一个个的被处理发送？然后服务器收到诸多请求后再返回？这里我理解的不是很明白。
看老师文中内容，感觉是多个请求会一起被分帧层处理然后都发送到服务器，服务器收到了分帧层发过来的全部内容，再组合拆分成不同请求</div>2022-01-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/24/13/26/8dfc7011.jpg" width="30px"><span>唯唯喏</span> 👍（0） 💬（0）<div>如果只有一个TCP连接，它会占满带宽，滑动窗口最大化，但是包本身有序，tcp层面也会出现队头阻塞，是这样吧。</div>2022-01-15</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/0a/db/84f40545.jpg" width="30px"><span>Du小强🍪</span> 👍（0） 💬（0）<div>我不理解这里所说的并行发送是可以同时发送还是可以不用等待发送，但发送时还是以顺序发送</div>2021-09-02</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1f/07/69/43cf2251.jpg" width="30px"><span>Alan He</span> 👍（0） 💬（0）<div>HTTP2的多路复用解决了同一个TCP连接下可以并发请求，浏览器本身单域名的TCP连接数是有限制的，比如6个，那么每一个TCP连接又可以并发多个请求，这个并发的请求数量有限制吗？</div>2021-03-05</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/18/26/f7/03134808.jpg" width="30px"><span>lerman</span> 👍（0） 💬（0）<div>请教一下，如果用了两个web server，前一个web server做负载均衡，支持HTTP&#47;2，后一个web server是实际执行任务的服务器，支持HTTP&#47;1.1，这种情况下，请求在客户端和服务器端是使用什么协议呢？谢谢！</div>2021-01-15</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1e/f8/8a/f7e7fd54.jpg" width="30px"><span>君自兰芳</span> 👍（0） 💬（3）<div>“HTTP&#47;2 提供了请求优先级，可以在发送请求时，标上该请求的优先级”

有个疑问，具体是怎么操作的，在请求头里面加上什么字段吗😂</div>2020-11-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1f/9d/15/dd819dd4.jpg" width="30px"><span>小朋友</span> 👍（0） 💬（0）<div>https:&#47;&#47;developers.google.com&#47;web&#47;fundamentals&#47;performance&#47;http2</div>2020-09-24</li><br/><li><img src="https://wx.qlogo.cn/mmopen/vi_32/6bCYR5TvPPNxBic9xBicXuyiaF0waeE71TTLRH0lM8OPnR0ibo40JlMplfmsuPuJevfxgbhDhFUqqp469lM3lGRqmg/0" width="30px"><span>kevinInsight</span> 👍（0） 💬（2）<div>这些数据经过二进制分帧层处理之后，会被转换为一个个带有请求 ID 编号的帧，通过协议栈将这些帧发送给服务器。服务器接收到所有帧之后，会将所有相同 ID 的帧合并为一条完整的请求信息

----

老师，这里不太明白；什么情况下帧的ID会相同？二进制分针层按照什么原则把请求数据分配成同一个帧ID？</div>2020-09-02</li><br/>
</ul>