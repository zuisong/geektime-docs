上次我们谈到了HTTP报文里的body，知道了HTTP可以传输很多种类的数据，不仅是文本，也能传输图片、音频和视频。

早期互联网上传输的基本上都是只有几K大小的文本和小图片，现在的情况则大有不同。网页里包含的信息实在是太多了，随随便便一个主页HTML就有可能上百K，高质量的图片都以M论，更不要说那些电影、电视剧了，几G、几十G都有可能。

相比之下，100M的光纤固网或者4G移动网络在这些大文件的压力下都变成了“小水管”，无论是上传还是下载，都会把网络传输链路挤的“满满当当”。

所以，如何在有限的带宽下高效快捷地传输这些大文件就成了一个重要的课题。这就好比是已经打开了冰箱门（建立连接），该怎么把大象（文件）塞进去再关上门（完成传输）呢？

今天我们就一起看看HTTP协议里有哪些手段能解决这个问题。

## 数据压缩

还记得上一讲中说到的“数据类型与编码”吗？如果你还有印象的话，肯定能够想到一个最基本的解决方案，那就是“**数据压缩**”，把大象变成小猪佩奇，再放进冰箱。

通常浏览器在发送请求时都会带着“**Accept-Encoding**”头字段，里面是浏览器支持的压缩格式列表，例如gzip、deflate、br等，这样服务器就可以从中选择一种压缩算法，放进“**Content-Encoding**”响应头里，再把原数据压缩后发给浏览器。
<div><strong>精选留言（30）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/10/61/c1/93031a2a.jpg" width="30px"><span>Aaaaaaaaaaayou</span> 👍（86） 💬（16）<div>老师，有个问题：http交给tcp进行传输的时候本来就会分块，那http分块的意义是什么呢？</div>2019-07-03</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/59/f6/ed66d1c1.jpg" width="30px"><span>chengzise</span> 👍（78） 💬（3）<div>1. 分块传输中数据里含有回车换行（\r\n）不影响分块处理，因为分块前有数据长度说明
2. 范围是应用于压缩后的文件</div>2019-07-03</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/3a/d6/485590bd.jpg" width="30px"><span>赵健</span> 👍（60） 💬（4）<div>“Transfer-Encoding: chunked”和“Content-Length”这两个字段是互斥的，也就是说响应报文里这两个字段不能同时出现，一个响应报文的传输要么是长度已知，要么是长度未知（chunked），这一点你一定要记住。老师请问下，为啥分块意味着长度未知，后面不是提到块里面有个长度头嘛？而且单个块应该是一次http传输的内容，既然块里有长度头，那这次传输的内容长度也就能算出来，这次http的Content-Length 也就知道啊！是我理解错了吗</div>2019-07-04</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/17/c9/9e/ce7c8522.jpg" width="30px"><span>秋水共长天一色🌄</span> 👍（55） 💬（2）<div>老师，我有些问题需要问问您。
1.比如我在视频网上看电影，我们经常能看到进度条里面有一条灰色的缓存进度，我是否能理解成这个进度就是分块传输的一个进度显示吗？
2.刚刚我有看到评论说过一个问题就是分块传输的时候是由一个请求和一个响应完成的，如果我们在抓一个需要10分钟才能完成分块传输的请求时，我是不是就会看到这个请求在这10分钟内都是一个正在响应的状态吗？
3.为什么我们在对一些视频网站看视频抓包的时候却无法捕抓到这个请求呢？
4.如果我们在看完视频后在浏览器缓存里发现一些片段式的视频文件，能否就说明这个是用分块传输呢？
5.如果我们在看视频拖动进度条到10分30秒，到最后视频会从10分20秒开始播放，能否说明10分30秒的这个分块的头是在10分20秒呢？
6.请问多段数据能理解成一次性获取分块传输里多个连续的分块的数据的意思吗？
还有就是非常感谢老师把这些知识点讲的那么细，我近期多个面试里都有被问到相关的知识，多亏老师的讲解我才能顺利应付，谢谢老师！！！</div>2019-07-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/11/b9/abb7bfe3.jpg" width="30px"><span>小桶</span> 👍（44） 💬（12）<div>分块传输，客户端只需要发一次请求，还是发多次请求呢？使用分块传输时，客户端与服务器是怎样工作的呢</div>2019-07-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/57/4f/6fb51ff1.jpg" width="30px"><span>奕</span> 👍（24） 💬（1）<div>对于问题2,range是针对原文的还是压缩后的，可以想象一下看视频的时候，我们拖拽进度条请求的range范围是针对原视频长度的，如果针对压缩后的，那么我们实际拖拽的范围和响应的数据范围就不一致了</div>2019-07-04</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/93/5d/91f1d849.jpg" width="30px"><span>darren</span> 👍（20） 💬（1）<div>不分块：http把客户端需要的东西整个交给tcp，由tcp切块后发送给客户端，客户端接受后在tcp层组装完整发给浏览器使用。
分块：http把客户端需要的东西切分成1、2、3到n块，然后将1块发给tcp，tcp将块1再次切分后发给客户端，客户端接受后在tcp组装成块1发给http层。然后服务器与客户端用同样的方式发送块2、块3到块n。客户端的http在接收完所有块后组装成一个完整的响应。整个过程使用同一个tcp连接，块1到块n如上是挨个发送的。如果是http2，则基于多路复用技术块1到块n可以同时发送。所以分块抓包http只能抓到一个包，如果抓tcp的包，分不分块，都会抓到很多包。
分段：分段就是对某个资源的一部分进行请求（类似于把一个大文件切分成很多小文件，类似压缩中的分卷功能，然后客户端只对这些小文件中的一部分进行请求）
分段是对需要哪些资源进行一种说明，分块是一种传输机制，完全不同的两个东西，只是名字比较像。
请老师指教理解不正确的地方，另外想问一下老师分块的时候每个块都会复制一次响应头吗，还是只有块1带有请求头。</div>2021-04-07</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/79/4b/740f91ca.jpg" width="30px"><span>-W.LI-</span> 👍（15） 💬（1）<div>老师好!在带宽固定的情况下，范围请求没发提高下载速度。如果服务器对客户端每个累链接限速的情况下，可通过多线程并发下载，提高下载速度是么?还有几个问题
分块传输:顺序传一次一小块
范围请求:支持跳跃式传输，还可以并发获取不同的range最后合并。
多段数据:一次请求多个范围，范围可以不连续是么?如果必须联系的话和请求一个大范围没差别了。
这几个拒的例子都是服务端这么返回的。
客户端上传的时候怎么使用呢?老师后面会讲么。
只读到了这么点，希望老师补充下每个的作用，和解决的问题，谢谢老师。</div>2019-07-03</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/6b/b4/47c548fd.jpg" width="30px"><span>一只鱼</span> 👍（11） 💬（1）<div>针对课下作业2：
情况一：如果服务器上只有 gzip 之后的文件，没有原文件，那范围请求针对的就是 gizp 之后的文件；
情况二：如果服务器上有原文件(未压缩)，只是在传输过程中被 gizp , 那范围请求针对的就是未压缩的原文件。
这里拓展一下，假如在服务器和客户端之间有一个 cdn , 那么 cdn 缓存的是文件的某个范围吗？cdn 会根据请求头判断缓存里面有没有这个范围的结果，如果有就直接返回，并没有再根据bytes进行计算?</div>2020-04-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/96/b1/141bf83e.jpg" width="30px"><span>wheat7</span> 👍（8） 💬（6）<div>chunk的核心问题并不是所谓把大象装进冰箱，是为了解决应用层在没有content-length的时候知道数据在哪里结束，chunk和普通传输方式都是在一个http报文里传输的，只是在body里相当于又加了一层协议或者是编码，数据无论如何是在一头大象里，在一个http报文中传输，大的数据传输使用chunk和不使用传输方式并没有什么区别。 </div>2019-07-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/9d/a4/e481ae48.jpg" width="30px"><span>lesserror</span> 👍（6） 💬（1）<div>老师，请问一下：“分块传输也可以用于“流式数据””。该怎么理解这个“流式数据”这句话呢？</div>2019-12-04</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/a3/fc/379387a4.jpg" width="30px"><span>ly</span> 👍（6） 💬（2）<div>有几个小疑问：
分块传输：
对于一个500Mb的数据，客户端应该是发送N次http请求，每次http请求只传输其中一部分，每次都是采用了分块传输的body格式，那么每次都会重新建立TCP连接吗（三次握手）？

另外文章提到分块传输中的“流式数据”，这个流式数据怎么理解呢？

对于多段数据:
服务端在响应body里面的每一段都会指定Content-Type和Content-Range，总感觉其中的Content-Type字段是多余的，难道body里面的不同分段，Content-Type可能不一样？
</div>2019-08-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/51/cd/d6fe851f.jpg" width="30px"><span>Gopher</span> 👍（6） 💬（1）<div>这个专栏质量很棒，老师很负责，知识讲解很通透，很容易就get、解惑了。

哈哈哈，特此留言就是想说，老师，你认真做事的样子真帅(*•̀ᴗ•́*)و ̑̑</div>2019-07-03</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/a6/84/92cb4db4.jpg" width="30px"><span>四月长安</span> 👍（4） 💬（1）<div>http数据包封装好交给下层tcp协议的时候，应该是作为tcp数据部分所要传输的内容吧，ip协议数据报最大传输65535字节的数据，这65535的数据减去tcp的首部，应该就是tcp所能容纳的负载极限了吧，所以如果是这样的话http数据的分块应该粒度更小才是吧，或许一个tcp负载里边就有好多http分块？请老师指正，感谢🙏</div>2019-08-16</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/a5/98/a65ff31a.jpg" width="30px"><span>djfhchdh</span> 👍（4） 💬（1）<div>1、因为分块数据是明文传输，如果数据里有\r\n，是会影响分块处理的
2、个人感觉应该是应用于原文件</div>2019-07-03</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/1f/04/1cddf65b.jpg" width="30px"><span>不二</span> 👍（3） 💬（4）<div>老师，问一个问题，这篇文章主要讲的是服务器端如何分块传输给客户端数据，或者客户端如何获取部分服务器端的数据， 那web客户端可以分批上传一个大文件的功能吗？类似于云盘中的上传功能</div>2020-12-16</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1f/04/c8/3c7af100.jpg" width="30px"><span>Javatar</span> 👍（3） 💬（2）<div>老师你好，看完本节内容后，找了一个网络上的pdf，用telnet发了下请求，结果在响应报文中并没有看到chunked头，pdf也是大文件，但是并没有分块传输，该怎么理解？还是说大文件也可以不用分段传输？

Trying 202.38.64.11...
Connected to staff.ustc.edu.cn.
Escape character is &#39;^]&#39;.


GET &#47;~bhua&#47;Kurose_Labs_v7.0&#47;Wireshark_HTTP_v7.0.pdf HTTP&#47;1.1
Host: staff.ustc.edu.cn

HTTP&#47;1.1 200 OK
Date: Sun, 30 Aug 2020 05:54:44 GMT
Server: Apache&#47;2.0.52 (Red Hat)
Last-Modified: Thu, 19 Sep 2019 09:00:14 GMT
ETag: &quot;40d8086-2392cc-2e81a380&quot;
Accept-Ranges: bytes
Content-Length: 2331340
Connection: close
Content-Type: application&#47;pdf

%PDF-1.3
%?????????
4 0 obj
&lt;&lt; &#47;Length 5 0 R &#47;Filter &#47;FlateDecode &gt;&gt;
stream
....省略body</div>2020-08-30</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/67/f4/9a1feb59.jpg" width="30px"><span>钱</span> 👍（3） 💬（1）<div>压缩和分而治之的思路是解决各种大问题的通用思路，思路容易理解，大东西放入小容器，要么把大东西变小也就是压缩，实在变小不了就弄多个容器把大东西分块放入多个容器之中，如果仅是传输之用那就一次传一点，有点类似愚公移山的动作。
比较关心大东西怎么拆？传输到对应的地方每一小块又怎么组合起来？比如：内存只有1G要传输10G的大文件，具体怎么拆分呢？是按照大小吗？比如：拆成20个0.5G的文件，如果这样传输到的内容也是需要保持一定的顺序的吧？否则组装也是一个问题，我能想到的最简单的方式就是表上号放置的时候按照序号一个个码放，不过我觉得应该不会这么简单，希望老师能分享一下，这块的具体实现逻辑。
目前在做的一个项目就涉及大文件上传、下载、解析的事情，量变引起质变感觉文件的体积大到一定程度，就不是一个简单的文件上传、下载、解析的事情了，需要各种考虑怎么提高性能减短处理时间的问题，还要考虑中间网络断了或者解析数据时遇到不OK的数据怎么处理的问题。</div>2020-03-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/18/22/89/73397ccb.jpg" width="30px"><span>响雨</span> 👍（3） 💬（1）<div>响应报文返回的数据太大，所以采用了chunk分块传输的话，那响应报文在传输完成前是什么样子，响应行和头过来了，响应体还在流式传递，那响应体内的数据该怎么展示?</div>2019-07-05</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/93/ff/87d8de89.jpg" width="30px"><span>snake</span> 👍（2） 💬（1）<div>1、使用chunk分段后还能压缩吗？或者说chunk分段分的是压缩后还是压缩前的文件呢？2、使用了chunk，为什么内存、带宽会节省呢？总的数据大小不变吧？内存的话，分段后，前面的数据到达浏览器客户端后，是存在内存还是磁盘呢？如何节省内存呢?</div>2020-06-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/b8/11/26838646.jpg" width="30px"><span>彧豪</span> 👍（2） 💬（3）<div>老师我有几个疑问：
1. 比如总共是1314的数据, 响应头会这么写`Content-Range: bytes 0-1313&#47;1314`, 为何会少1?
2. 浏览器如何开N个线程下载数据?多个ajax请求?</div>2019-07-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/1a/66/2d9db9ed.jpg" width="30px"><span>苦行僧</span> 👍（2） 💬（1）<div>老师 我们的业务就是视频处理 经常涉及的就是视频下载本地处理 使用的是ftp协议 如果使用http会更快？</div>2019-07-04</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/11/9c/4fd6ebe0.jpg" width="30px"><span>白了少年头</span> 👍（2） 💬（2）<div>1.数据里有回车换行，会影响分块的处理
2.范围应用于压缩后文件
不知道对不对，辛苦老师解答一下，谢谢！</div>2019-07-03</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/27/d5/0fd21753.jpg" width="30px"><span>一粟</span> 👍（2） 💬（1）<div>迅雷下载或者在线视频播放器是不是在使用分块或者任意请求功能?</div>2019-07-03</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/26/eb/d7/90391376.jpg" width="30px"><span>ifelse</span> 👍（1） 💬（2）<div>1.应该不影响
2.应该是压缩后的数据</div>2023-01-25</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/DYAIOgq83erXRaa98A3zjLDkOibUJV1254aQ4EYFTbSLJuEvD0nXicMNA8pLoxOfHf5kPTbGLXNicg8CPFH3Tn0mA/132" width="30px"><span>Geek_115bc8</span> 👍（1） 💬（1）<div>想跳过片头，直接看正片，或者有段剧情很无聊，想拖动进度条快进几分钟，这实际上是想获取一个大文件其中的片段数据，而分块传输并没有这个能力。

这个为什么分块传输没有能力呢？他不是也将数据传输过来，然后拼接展示吗。快进也可以有数据的啊</div>2022-04-30</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/6c/d4/85ef1463.jpg" width="30px"><span>路漫漫</span> 👍（1） 💬（1）<div>老师，多段数据的请求方式是应用在什么业务场景下呢</div>2021-11-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/20/b9/f5/cfeb1094.jpg" width="30px"><span>墨中白</span> 👍（1） 💬（2）<div>https:&#47;&#47;www.chrono.com&#47;域名是被回收重新分配了吗？</div>2021-08-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1e/f5/0b/73628618.jpg" width="30px"><span>兔嘟嘟</span> 👍（1） 💬（1）<div>我觉得HTTP分块和TCP分块的核心区别还是：”HTTP分块是在应用层层面的工作，它不关心TCP的分块”，因为HTTP没有认定TCP作为底层协议，所以不去考虑底层协议是否也做了分块。至于性能上的区别，我做了测试没有体现出来，不管大文件分不分段，在HTTP层面都是多个continuation包</div>2021-07-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/c9/fd/5ac43929.jpg" width="30px"><span>天方夜</span> 👍（1） 💬（1）<div>本篇有个小问题。偏移量指的是相对于第一个元素，偏移多少个单位。bytes=x-y 里面的 x 和 y 是从 0 开始的索引值（index），而不是偏移量。0-9 表示索引 0 到 9 的数据。关于偏移量，最典型的例子是 SQL 里面的 offset 与 limit，offset 10 limit 5 表示相对第一个元素偏移 10 个单位然后获取 5 个元素。不过也有一种理解是 index 就是指偏移量，但我觉得这样理解容易产生混乱。TUS 是一个支持续传的上传协议，它用的就是 offset，我觉得比 range 更清晰。</div>2021-02-18</li><br/>
</ul>