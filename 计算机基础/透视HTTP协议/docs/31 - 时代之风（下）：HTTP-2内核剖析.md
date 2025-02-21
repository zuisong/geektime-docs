今天我们继续上一讲的话题，深入HTTP/2协议的内部，看看它的实现细节。

![](https://static001.geekbang.org/resource/image/89/17/8903a45c632b64c220299d5bc64ef717.png?wh=1142%2A586)

这次实验环境的URI是“/31-1”，我用Wireshark把请求响应的过程抓包存了下来，文件放在GitHub的“wireshark”目录。今天我们就对照着抓包来实地讲解HTTP/2的头部压缩、二进制帧等特性。

## 连接前言

由于HTTP/2“事实上”是基于TLS，所以在正式收发数据之前，会有TCP握手和TLS握手，这两个步骤相信你一定已经很熟悉了，所以这里就略过去不再细说。

TLS握手成功之后，客户端必须要发送一个“**连接前言**”（connection preface），用来确认建立HTTP/2连接。

这个“连接前言”是标准的HTTP/1请求报文，使用纯文本的ASCII码格式，请求方法是特别注册的一个关键字“PRI”，全文只有24个字节：

```
PRI * HTTP/2.0\r\n\r\nSM\r\n\r\n
```

在Wireshark里，HTTP/2的“连接前言”被称为“**Magic**”，意思就是“不可知的魔法”。

所以，就不要问“为什么会是这样”了，只要服务器收到这个“有魔力的字符串”，就知道客户端在TLS上想要的是HTTP/2协议，而不是其他别的协议，后面就会都使用HTTP/2的数据格式。
<div><strong>精选留言（30）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/12/79/4b/740f91ca.jpg" width="30px"><span>-W.LI-</span> 👍（47） 💬（2）<div>1.还是无状态,流状态只是表示流是否建立，单次请求响应的状态。并非会话级的状态保持
2.小帧好，少量多次，万一拥堵重复的的少。假设大帧好，只要分流不用分帧了。
3.每一个请求响应都是一个流，流和流之间可以并行，流内的帧还是有序串行。</div>2019-08-07</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/a5/98/a65ff31a.jpg" width="30px"><span>djfhchdh</span> 👍（19） 💬（1）<div>3、首先要明确造成“队头阻塞”的原因，因为http1里的请求和应答是没有序号标识的，导致了无法将乱序的请求和应答关联起来，也就是必须等待起始请求的应答先返回，则后续请求的应答都会延迟，这就是“队头阻塞”，而http2采用了虚拟的“流”，每次的请求应答都会分配同一个流id，而同一个流id里的帧又都是有序的，这样根据流id就可以标识出同一次的请求应答，不用再等待起始请求的应答先返回了，解决了“队头阻塞”</div>2019-08-07</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/04/71/0b949a4c.jpg" width="30px"><span>何用</span> 👍（15） 💬（1）<div>服务端是不是要为每一个客户端都单独维护一份索引表？连接的客户端多了的话内存不就OOM了嘛</div>2019-08-07</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/17/9a/67/73f384f9.jpg" width="30px"><span>好好好</span> 👍（14） 💬（5）<div>老师，我还是无法理解HTTP1.X无法实现多路复用的具体原因。如果我在HTTP1.X版本的一个TCP连接下同时发送多个请求，会发生什么情况呢？造成这个情况的具体原因又是什么呢？</div>2020-06-30</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/04/71/0b949a4c.jpg" width="30px"><span>何用</span> 👍（13） 💬（3）<div>HTTP&#47;2 底层还是依赖 TCP 传输，没有解决队头阻塞的问题啊，这就是为何 HTTP&#47;3 要基于 UDP 来传输</div>2019-08-07</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/c4/8b/a9fbaea6.jpg" width="30px"><span>想个昵称好难</span> 👍（10） 💬（1）<div>还有一个问题想请教下老师,您之前在《HTTP的前世今生》上有一段回复是说,只要是HTTP&#47;1.1，就都是文本格式，虽然里面的数据可能是二进制，但分隔符还是文本，这些都会 在“进阶篇”里讲, 不过我看到现在还是有点迷惑,所二进制协议和文本协议的区别是什么呢?可以按照stackoverflow中https:&#47;&#47;stackoverflow.com&#47;questions&#47;2645009&#47;binary-protocols-v-text-protocols  的回答来理解吗?</div>2019-08-07</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/c4/8b/a9fbaea6.jpg" width="30px"><span>想个昵称好难</span> 👍（9） 💬（2）<div>老师您好,打扰您实在是抱歉,想请教您一个问题,您在文中说HTTP&#47;2会在两端维护“Key-Value”的索引表,静态表应该是一摸一样的,那动态表俩边一样吗?如果一样的话,同步是比较难做的事情吧,我看RFC文档中是这么写的,”When used for bidirectional communication, such as in HTTP, the encoding and decoding dynamic tables maintained by an endpoint are completely independent, i.e., the request and response dynamic tables are separate.“, 所以我的理解是,动态表在客户端和服务器各自都有俩个表,一个是用来保存客户端发送的message的header,另外一个是保存服务器发送的header, 我看stackoverflow中也是这么写的,https:&#47;&#47;stackoverflow.com&#47;questions&#47;53003333&#47;how-does-headers-keep-sync-in-both-client-and-server-side-in-http-2, 如果我有哪个地方理解错了,麻烦下老师指点一下

</div>2019-08-07</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/a5/98/a65ff31a.jpg" width="30px"><span>djfhchdh</span> 👍（8） 💬（1）<div>1、http的“无状态”是指对事务处理没有记忆，每个请求之间都是独立的，这与HPACK算法里的动态表、流状态转换是两回事。HPACK算法里维护动态表是用于头部压缩，而流状态转换只是表示一次请求应答里流的状态，都不会记录之前事务的信息</div>2019-08-07</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/4e/94/0b22b6a2.jpg" width="30px"><span>Luke</span> 👍（7） 💬（2）<div>1、一个流中的多个帧是有序的，但是在二进制帧协议中，并没有看到这个序号，请问下老师，这个序号是在哪里？或者一个流中的多个帧是如何保证有序的？
2、如果出现丢帧的情况是如何重传的？</div>2019-09-02</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/4d/fd/0aa0e39f.jpg" width="30px"><span>许童童</span> 👍（6） 💬（4）<div>HTTP&#47;2 的动态表维护、流状态转换很复杂，你认为 HTTP&#47;2 还是“无状态”的吗？
还是无状态的，对上层应用来说，动态表维护、流状态转换这些操作对它不可见。

HTTP&#47;2 的帧最大可以达到 16M，你觉得大帧好还是小帧好？
大帧好，应该小帧需要很多额外的头信息，有数据冗余。小帧可以当出差错时，只转输出错的帧，细粒度控制。

结合这两讲，谈谈 HTTP&#47;2 是如何解决“队头阻塞”问题的。
因为流可以并发，一个流被阻塞了，并不影响其它的流。</div>2019-08-07</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/19/e4/4f/df6d810d.jpg" width="30px"><span>Maske</span> 👍（5） 💬（3）<div>1.还是无状态，http2虽然实现了多路复用，但是本质没有变，因为服务端永远不会自动记录上次请求的相关数据，客户端的每一次请求都需要表明其身份。
2.小帧好。因为http2的一个一个请求都分解为了一个一个帧，在同一个tcp&#47;ip连接层面上表现为无序收发的，小帧有利于提高并行请求或响应。
3.通过分解一个一个请求或响应报文数据为多个帧，将同一个请求或响应的帧贴上相同的streamid来作为标识，使得在连接层面上变为无序收发，而且这些帧是并行的，因此不需要等待前一个请求响应结束才能进行下一个请求，实现了多路复用。</div>2020-06-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/17/9e/c0/69ae8a58.jpg" width="30px"><span>sunxu</span> 👍（5） 💬（1）<div>想问一下，nginx前端采用http2, 反向代理到应用服务使用的http1.1, 这种方式对请求响应有提升吗？</div>2019-08-07</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/75/aa/21275b9d.jpg" width="30px"><span>闫飞</span> 👍（4） 💬（1）<div>哈夫曼编码的使用是HTTP2协议里面一个不容忽视的要素，该编码方式很好地保证了所有信息的平均码长最短而互相不构成前缀关系，易于解码。</div>2019-08-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/79/4b/740f91ca.jpg" width="30px"><span>-W.LI-</span> 👍（4） 💬（1）<div>老师好!TCP网络不好的时候会降速，http2的话是一个帧没收到就会导致TCP降速么?</div>2019-08-07</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTIuTjCibv0afd7SSdLicfNk0f7KO5ga9VMleD1hc2DtQfianK20ht06SekClKV7M8UXLRHqQLm9hJ3ow/132" width="30px"><span>Jasmine</span> 👍（3） 💬（1）<div>老师，同一个流内部，相同类型的帧，比如DATA[3]和DATA[3]怎么区分先后顺序呢？</div>2021-10-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/25/5e/40/dee7906c.jpg" width="30px"><span>张欣</span> 👍（3） 💬（2）<div>老师，您好：
1，http2也是依赖于tcp来保证他自己帧数据的完整性么？他自己有检测数据完整性的功能么
2，http2的帧的排序序号也是保存在帧头部里面的么？</div>2021-04-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/67/f4/9a1feb59.jpg" width="30px"><span>钱</span> 👍（3） 💬（1）<div>1：HTTP&#47;2 的动态表维护、流状态转换很复杂，你认为 HTTP&#47;2 还是“无状态”的吗？
还是无状态的，因为第二次交互并不需要保留或者知道是否在之前已经有过一次交互了，假设后面的服务是个集群第一次请求和第二次请求负载打到的机器不同也没关系，另外动态表应该可以重新创建吧！
另外，用代号表示语义是不是也是一种空间换时间的运用，虽然只是减少了传输空间增加了两头的存储空间。

2：HTTP&#47;2 的帧最大可以达到 16M，你觉得大帧好还是小帧好？
大帧好还是小帧好，我觉得应该看场景，如果网络不稳定小帧好因为丢失重传的成本低，也可以传输更多的数据帧提高并行度。不过如果网络稳定，帧小必然帧头多对于而数据是放在帧体区的是不是针对大文件下载之类的需求就有些浪费了呢？

3：结合这两讲，谈谈 HTTP&#47;2 是如何解决“队头阻塞”问题的。
HTTP&#47;2的连接好似一座桥，桥上可以过许多的车辆（数据帧），他们可以并发来走，而车队中的车辆是有顺序的她们组成一个车队（一次请求或响应报文），所以，先出发的车队不一定先到，因为车队之间是并行互不阻塞的。</div>2020-04-04</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/11/e7/044a9a6c.jpg" width="30px"><span>book尾汁</span> 👍（3） 💬（1）<div>1 http的无状态是针对应用层的吧，多个请求之前不会有影响，http2虽然有维护一些状态的信息，但这是针对流的信息，所以我认为http2也还是无状态的
2 不知道大小帧哪个好，大帧头部占比会少一点，但在TCP层会需要拆分成小帧，可能会多耗点时间，太大的帧TCP发送缓存区也要设的大一点吧
3  http2相比http1.1有了流ID来标识请求响应，因此同一个连接就可以同时进行多个流的传输，但由于TCP的收发窗口的确认机制，并发性还是会受到限制。

总结：
http2连接的建立
建立完成TLS连接之后，发送连接前言PRI * HTTP&#47;2.0\r\n\r\nSM\r\n\r\n，这样后面的报文就会使用http2的格式
报文格式：
帧长度  3byte    默认上限为16k 最大为2^24
帧类型  1byte   大致分为数据帧和控制帧，最高可表示256种，可自己扩展
标志位   1byte   携带简单的控制信息
流ID    4byte  其中最高位为0，客户端发起的流id为奇数，服务器发起的流id为偶数，0号流为控制流

请求头字段采用HPACK的方式来进行压缩，有静态表来存储二元组（字段 ，value）和index之间的关系，静态表里找不到的key value，可以放在动态表里。
</div>2019-11-04</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/17/9a/67/73f384f9.jpg" width="30px"><span>好好好</span> 👍（2） 💬（1）<div>想请问下老师，我在别的地方看到http1.1有管道机制可以同时发送请求，服务端会根据请求顺序返回内容。那为什么还说http1.x如果同时发送请求，服务端无法区分数据是哪个请求所以实现不了多路复用呢？希望老师解答下。</div>2020-06-30</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/29/55/03/1092fb6a.jpg" width="30px"><span>假于物</span> 👍（1） 💬（1）<div>老师，帧头和数据帧对应关系是怎么样的？
1对1还是1对多？</div>2021-08-04</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTIpF5euTNx3GOkmf515HFh1ahAzogerLfIyLia2AspTIR9fkU6icGbo2ungo23cdM5s9dUjZGMno7ZA/132" width="30px"><span>dawn</span> 👍（1） 💬（1）<div>老师，一个流处理完一次请求响应后可以用于下一次请求吗，就是客户端不用新起一个流，复用这个流</div>2021-07-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1e/44/c0/cd2cd082.jpg" width="30px"><span>BoyiKia</span> 👍（1） 💬（2）<div>老师您好，我有一个疑问。
 http:是将整个请求的报文传递给 传输层，传输层又将上层的报文 分成多个报文段，然后 发给 IP层。

 http2:是 每个请求报文 先分成不同的帧，然后 乱序 发到传输层。
        那么传输层是等一个完整流到达才开始分段，还是说接受到混合内容(多个请求的混合帧对应内容)，就开始分段，走下面的流程呢？</div>2021-03-03</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1d/12/13/e103a6e3.jpg" width="30px"><span>扩散性百万咸面包</span> 👍（1） 💬（2）<div>还有一个问题。本来HTTP&#47;1 也是用二进制在 网络上传输（底层的frame），那和HTTP&#47;2的这个二进制帧有何不同呢？</div>2020-07-31</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1d/12/13/e103a6e3.jpg" width="30px"><span>扩散性百万咸面包</span> 👍（1） 💬（1）<div>HTTP2 通过流ID来实现乱序frame的分组。那么对于同一个流的frame，又是如何组装的呢？很有可能同一个流的不同帧到达的时间点不同，接收方要怎么辩识正确的顺序呢？</div>2020-07-31</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/85/49/585c69c4.jpg" width="30px"><span>皮特尔</span> 👍（1） 💬（1）<div>用了HTTP2以后，HTTP时代的一些前端优化手段，比如雪碧图，是不是就不需要了？因为多路复用，已经不存在重复建立连接的问题了？</div>2020-06-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/19/95/c2/afbb3f61.jpg" width="30px"><span>- shadow -</span> 👍（1） 💬（1）<div>老师你好，http2的头字段都是要求小写的，那服务端要升级到支持http2岂不是很难？因为很多头字段都是定义在程序里，我记得首字母是大写</div>2019-10-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/4d/fd/0aa0e39f.jpg" width="30px"><span>许童童</span> 👍（1） 💬（1）<div>老师你好，nginx反向代理与服务端应用间有必要使用HTTP2吗？对性能提升大吗？</div>2019-08-07</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/a5/98/a65ff31a.jpg" width="30px"><span>djfhchdh</span> 👍（1） 💬（1）<div>2、小帧好，如果多个流的帧可以在同一个tcp数据段发送的话，就可以提高网络利用率</div>2019-08-07</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/19/8b/06/fb3be14a.jpg" width="30px"><span>TableBear</span> 👍（0） 💬（1）<div>HTTP2 帧结构里面没有给帧标号的字段。那么 HTTP2 是依赖TCP的按序到达功能来保证同个流的帧有序的吗？</div>2023-07-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/66/b1/40a25f84.jpg" width="30px"><span>不利于团结的话不要说</span> 👍（0） 💬（2）<div>一个http2的连接，同时能并行跑几个流</div>2023-05-23</li><br/>
</ul>