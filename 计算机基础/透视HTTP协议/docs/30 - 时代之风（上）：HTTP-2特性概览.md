在[第14讲](https://time.geekbang.org/column/article/103746)里，我们看到HTTP有两个主要的缺点：安全不足和性能不高。

刚结束的“安全篇”里的HTTPS，通过引入SSL/TLS在安全上达到了“极致”，但在性能提升方面却是乏善可陈，只优化了握手加密的环节，对于整体的数据传输没有提出更好的改进方案，还只能依赖于“长连接”这种“落后”的技术（参见[第17讲](https://time.geekbang.org/column/article/104949)）。

所以，在HTTPS逐渐成熟之后，HTTP就向着性能方面开始“发力”，走出了另一条进化的道路。

在[第1讲](https://time.geekbang.org/column/article/97837)的HTTP历史中你也看到了，“秦失其鹿，天下共逐之”，Google率先发明了SPDY协议，并应用于自家的浏览器Chrome，打响了HTTP性能优化的“第一枪”。

随后互联网标准化组织IETF以SPDY为基础，综合其他多方的意见，终于推出了HTTP/1的继任者，也就是今天的主角“HTTP/2”，在性能方面有了一个大的飞跃。

## 为什么不是HTTP/2.0

你一定很想知道，为什么HTTP/2不像之前的“1.0”“1.1”那样叫“2.0”呢？

这个也是很多初次接触HTTP/2的人问的最多的一个问题，对此HTTP/2工作组特别给出了解释。

他们认为以前的“1.0”“1.1”造成了很多的混乱和误解，让人在实际的使用中难以区分差异，所以就决定HTTP协议不再使用小版本号（minor version），只使用大版本号（major version），从今往后HTTP协议不会出现HTTP/2.0、2.1，只会有“HTTP/2”“HTTP/3”……
<div><strong>精选留言（30）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/10/f4/87/644c0c5d.jpg" width="30px"><span>俊伟</span> 👍（49） 💬（2）<div>1.h2c使用明文传输，速度更快，不需要TLS握手。
2.客户端将多个请求分成不同的流，然后每个流里面在切成一个个帧，发送的时候是按帧发送的。每个帧存着一个流ID来表示它属于的流。服务端收到请求的时候将帧按流ID进行拼接。从传输的角度来看流是不存在的，只是看到了一个个帧，所以说流是虚拟的。
3.相同点：都是基于TCP和TLS的，url格式都是相同的。都是基于header+body的形式。都是请求-应答模型。
4.不同点： 1.使用了HPACK进行头部压缩。
                2.使用的是二进制的方式进行传输。
                3.将多个请求切分成帧发送，实现了多路复用。这个感觉上利用了多道程序设计的思想。
                4.服务器可以主动向客户端推送消息。充分利用了TCP的全功双通道。</div>2020-01-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/55/45/e4314bc6.jpg" width="30px"><span>magicnum</span> 👍（26） 💬（3）<div>h2c优点是性能，不需要TLS握手以及加解密。可以通过curl工具构造h2c请求；
h2的流是虚拟的因为它是使用帧传输数据的，相同streamid的帧组成了虚拟消息以及流；
相同点：都是基于tcp或TLS，并且是基于请求-响应模型，schema还是http或https不会有http2。
不同点：h2使用二进制传输消息并且通过HPACK压缩请求头，实现流多路复用、服务器推送
</div>2019-08-05</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/35/51/c616f95a.jpg" width="30px"><span>阿锋</span> 👍（14） 💬（3）<div>突然想起了一个问题，get和post请求其中一个区别是，post请求会把请求的数据放入请求体（body）中，而get请求是拼接到url后面。get请求是不是一定不能往请求体（body）中放入数据。还是这些都只是客户端和服务端的约定，可以灵活的自定义，没有强制的要求。</div>2019-08-05</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/5a/13/3160996d.jpg" width="30px"><span>nb Ack</span> 👍（14） 💬（1）<div>老师好。我想问一下，http2的多路复用和http的长连接效果不是一样吗？</div>2019-08-05</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/81/4e/d71092f4.jpg" width="30px"><span>夏目</span> 👍（12） 💬（1）<div>流就是逻辑上将数据帧按id分组了，同组有序，组间无序，本质就是id相同的几个数据帧所以流是虚拟的。在tcp层面还是队首阻塞的吧？需要等待ack</div>2019-12-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/19/e4/4f/df6d810d.jpg" width="30px"><span>Maske</span> 👍（9） 💬（1）<div>1.明文传输时不需要进行加密解密动作，不需要TLS握手，能节约性能。适用于对数据传输安全性要求不高的场景。
2.http2改变了http1.1的“请求-应答”模式，将head+body的请求报文在传输过程中改为 head帧 + data帧，在同一个TCP&#47;IP中，可以将多个请求分解为多个帧，从连接层面来看，这些帧是无序的，为了让接受端准确的将这些帧还原为一个一个独立的请求或响应，就给了每一个帧分配了streamid，streamid相同的即为同一个请求或响应的数据。因此，此处的流并不是真实有序的二进制字节，所以叫‘虚拟流’。
3.http1.1解决的是在万维网中，计算机之间的信息通信的一套规范，包括定义其属于应用层协议，建立在tcp&#47;ip之上，请求响应的报文结构等。https不改变http1.1的原有属性，是在其之上新增了对数据安全性和有效性的特性，解决的是数据安全的问题，通过使用加密解密，数字证书，TLS握手等过程保证了这一点。http2解决的是性能问题，通过头部压缩，使用二进制传输，多路复用，服务器推送等策略使得http的性能更好。http2和https本质上都是对http1.1的扩展和延伸。</div>2020-06-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/79/4b/740f91ca.jpg" width="30px"><span>-W.LI-</span> 👍（7） 💬（3）<div>课后习题出的很好。可惜我不会坐等答案
1.内网用h2c会比https快么?
2.感觉回答虚拟流之前给先回答啥是真真的流。我对流的理解是有序，切只能读一次。http2支持乱序发，我猜也支持，部分帧重发，所以就是虚拟的了。
3.共同，都是应用层协议，传输成都用的TCP。
不同:https=TLS+HTTP&#47;HTTP2，安全。
http2:二进制传输，对header压缩，通过二进制分帧解决了队头阻塞，传输效率更高，服务端可推数据
http:明文，队头阻塞，半双工。
问题1:一个TCP链接可以打开很多channel是吧，每一个channel都可以传输数据。底层具体怎么实现的啊，是怎么区分channel里的数据谁是谁的?
问题2:我之前看见TPC好像是通过服务端IP,服务端端口号,客户端端IP,客户端端口号。来唯一标识一个链接的。http1的时候队头阻塞，继续要多建http链接。每建立一个链接客户端就用一个不同的端口号么?
</div>2019-08-05</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/55/cb/1efe460a.jpg" width="30px"><span>渴望做梦</span> 👍（6） 💬（1）<div>老师，我有个疑问，既然http2是二进制的格式，那我们还能用chrome自带的工具调试吗？</div>2019-08-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/18/65/35361f02.jpg" width="30px"><span>潇潇雨歇</span> 👍（5） 💬（1）<div>1、明文传输性能更好，省去了加密相关操作
2、流和请求&#47;应答一样，但是流是相同流id的帧组合，不同流可以无序，相同流有序。整个看起来是无序的，请求之间不受影响。这也解决了http1.1的队头阻塞。
3、三者都是基于tcp的，基本语义是一样的。http2在性能上做了提升，比如二进制帧，流，服务器推送，HPACK算法等；https在安全上做了提升，下层多了TLS&#47;SSL，要多做一些握手加密证书验证等操作。</div>2020-11-30</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1e/44/c0/cd2cd082.jpg" width="30px"><span>BoyiKia</span> 👍（4） 💬（1）<div>http2  优点
1.兼容性
   兼容以前的http1.1 ，https等。

2.性能提升
   报文变成了 二进制数据帧，提高传输效率，和减少歧义。
    ①header 采用了头部压缩，来减小传输体积。
    ②body数据 放到了 data帧。
   a.同一请求或响应的数据帧具有相同的帧标识(流ID)，两端接受到的帧数据可以通过同一帧标识，重新组装成请求或响应数据。
 b.不同请求&#47;响应的数据帧可以乱序发，避免生成请求队列造成的队头阻塞。
c.同一个TCP连接上，可以并行发送多种流的数据帧(多路复用，PS： http1的 多路复用是分母效应，同一连接串行增加http通信 )。
d.强化了请求响应模式，服务器可以主动发送信息-服务器推送。
3.安全性
①.要求下层必须是 TlS1.2以上，支持前向安全，废除安全性比较低的密码套件。


   
 </div>2020-05-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1e/f5/0b/73628618.jpg" width="30px"><span>兔嘟嘟</span> 👍（3） 💬（3）<div>老师好，我不太理解为什么二进制帧可以提高解析效率，我的理解是这样的：
在HTTP&#47;1.1中，请求方的字符串在TCP层被解码为Unicode二进制，然后应答方在HTTP层编码为utf-8字符串。
而在HTTP&#47;2中，请求方的字符串在HTTP层被解码为二进制，然后应答方在浏览器处编码为字符串。所以好像没有省去时间或者资源。请老师赐教</div>2021-07-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/19/e4/4f/df6d810d.jpg" width="30px"><span>Maske</span> 👍（3） 💬（1）<div>老师我又回来了，按之前的理解是，http2是对同一域名使用单一的TCP连接进行数据传输，多个请求同时进行，既然如此，为什么在chrome调试面板中还能看到资源还是是有请求排队时间的呢？</div>2020-11-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/66/51/052c7b30.jpg" width="30px"><span>谢一</span> 👍（3） 💬（3）<div>老师，既然在连接层，是无序的，那在http&#47;2中是怎么保证frame的有序性的呢？</div>2019-09-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/c6/73/abb7bfe3.jpg" width="30px"><span>疯琴</span> 👍（2） 💬（2）<div>请问老师，同一个流里面不同序号的帧可以乱序到达统一组装么？</div>2021-07-16</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1e/01/c5/b48d25da.jpg" width="30px"><span>cake</span> 👍（1） 💬（1）<div>老师请问下，而在“连接”的层面上看，消息却是乱序收发的“帧”，为什么HTTP3 Over UDP 连接层面是包，这个HTTP2连接层面为啥是帧呢？不应该叫报文段么</div>2022-06-24</li><br/><li><img src="" width="30px"><span>思维决定未来</span> 👍（1） 💬（4）<div>http2的事实标准就是加密传输的，那是不是跟https重复了？</div>2020-09-07</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/a5/f0/8648c464.jpg" width="30px"><span>Joker</span> 👍（1） 💬（1）<div>老师，使用二进制的传输，是节省了从字符转二进制，以及从二进制转字符类型的时间吗</div>2020-05-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1f/64/8a/bc8cb43c.jpg" width="30px"><span>路边的猪</span> 👍（0） 💬（1）<div>想知道对于 HTTP&#47;2 这种大的版本，以及包括之前的http&#47;1.1 
是怎么一步步在全世界范围内被广泛应用的？协议颁发出来，是会有一些大头企业领头去实现基于HTTP&#47;2的协议吗？</div>2023-02-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/98/1c/d7a1439e.jpg" width="30px"><span>KaKaKa</span> 👍（0） 💬（2）<div>老师，重新复习的时候，我突然有点疑惑：
1.同一个TCP连接中，多个流是怎么并发请求的？再怎么并发，不都是需要这个TCP连接去一个个数据包进行传输吗？那为什么还需要有多个流？
2.多个TCP连接，每个连接都能单独去发送数据包，这种形式不是更快吗？
本来我以为我了解这章了，现在重新复习的时候，有些点还是不太了解</div>2023-01-10</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/DYAIOgq83eqf54z1ZmqQY1kmJ6t1HAnrqMM3j6WKf0oDeVLhtnA2ZUKY6AX9MK6RjvcO8SiczXy3uU0IzBQ3tpw/132" width="30px"><span>Geek_68d3d2</span> 👍（0） 💬（1）<div>请问同一个流可以在一个tcp连接里面发送吗</div>2021-09-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/83/98/fab9bd2a.jpg" width="30px"><span>Mingyan</span> 👍（0） 💬（1）<div>我有疑问，http2.0如果遇到服务器主动关闭tcp链接会理会回ack，再发fin等ack去关闭tcp链接还是不理会继续使用被关闭的tcp链接了？</div>2021-06-04</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/24/22/4e/2e081d9c.jpg" width="30px"><span>hao</span> 👍（0） 💬（1）<div>为何新增了流的概念，就可以实现服务器主动推送呢？那HTTP2可以像websocket那样实现即使通信（服务器主动推送） ？</div>2021-06-04</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/rQOn22bNV0kHpoPWRLRicjQCOkiaYmcVABiaIJxIDWIibSdqWXYTxjcdjiadibIxFsGVp5UE4DBd6Nx2DxjhAdlMIZeQ/132" width="30px"><span>ThinkerWalker</span> 👍（0） 💬（1）<div>老师，http2使用一个tcp连接传输多个流（多个请求），http1.1用的是多个tcp连接多个请求，会不会因为连接少而导致整体吞吐量降低？</div>2020-12-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/84/19/7ed2ffa6.jpg" width="30px"><span>风</span> 👍（0） 💬（1）<div>老师,请教一个关于多路复用的问题
由于http2将数据分割为帧进行无须发送,那接收方是怎么正确处理请求的呢？
通过什么判断该请求的数据都已经发送完毕</div>2020-07-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/52/3c/d6fcb93a.jpg" width="30px"><span>张三</span> 👍（0） 💬（1）<div>学习了，在小贴士里看到端口的重定向，有个疑问，我们一般在web 服务器配置不同的http端口和https端口都是用重定向吗？</div>2020-04-15</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/67/f4/9a1feb59.jpg" width="30px"><span>钱</span> 👍（0） 💬（1）<div>1：你觉得明文形式的 HTTP&#47;2（h2c）有什么好处，应该如何使用呢？
明文就是没加密，没加密就不会有加密的开销，性能会好一些，针对就是用于信息分享的场景加不加密其实无所谓啦！之所以，挖空心思要安全要加密主要是为了钱，为了不让别人轻易知道。

2：你觉得应该怎样理解 HTTP&#47;2 里的“流”，为什么它是“虚拟”的？
流就是具有方向性的二进制字节数据，为啥说她是虚拟的？是因为这里的流实际是一些有序的数据帧组成的，并且流动的方向是双向的嘛？不太清楚为啥这么说？另外，数据帧是将字节封装了一下是吗？具有一定的格式，也会更大一些。

3：你能对比一下 HTTP&#47;2 与 HTTP&#47;1、HTTPS 的相同点和不同点吗？
首先，他们的核心关注点不同，HTTP&#47;1主要就是分享信息之用，HTTPS主要是安全的分享信息，HTTP&#47;2是想又快又安全的解决信息分享。后一个协议的出现为了解决前一个的缺陷，后面的也是类似。
然后就是解决问题的具体方案有所不同了，老师文章给的那个对比图就非常的形象。
相同点本质都是HTTP协议的家庭成员，初心一样，底层基因一样，后面的成员为了适应环境进行了适当的变异，变得更安全更快更强。</div>2020-04-04</li><br/><li><img src="" width="30px"><span>Geek_5b0e47</span> 👍（0） 💬（1）<div>流是二进制帧的双向传输序列。是双方通信吗？服务器，再没有请求时，可以推送更新数据吗？</div>2020-03-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/63/2e/e49116d1.jpg" width="30px"><span>Geek_007</span> 👍（0） 💬（1）<div>老师，新版nginx已经支持同端口，不同域名根据配置开启h2了。另外h2不支持CBC吗？CBC只是加解密效率低，没有安全性问题吧，况且的确CBC还是很常见的加密模式呢。</div>2019-10-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/0e/9c/cb9da823.jpg" width="30px"><span>猫王者</span> 👍（0） 💬（1）<div>http1中消息的内容不也通过一定的编码比如utf8，将文本转成二进制，然后在网络上传输吗？http2和它又能有什么区别呢</div>2019-08-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/79/4b/740f91ca.jpg" width="30px"><span>-W.LI-</span> 👍（0） 💬（2）<div>老师好。之前用MQ的时候，AMPT协议说是只打开一个长链接TCP链接。然后AMPT协议每次都是在这个链接里打开信道进行传输。队列和client(服务器)IP和端口基本固定，如果以TCP链接形式会占用很多端口号，还影响性能，所以就采用了信道。可是信道和信道之间如何实现数据隔离和马上要讲的http2的channel原理差不多么?</div>2019-08-06</li><br/>
</ul>