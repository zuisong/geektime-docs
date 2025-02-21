在衡量Web页面性能的时候有一个重要的指标叫“**FP（First Paint）**”，是**指从页面加载到首次开始绘制的时长**。这个指标直接影响了用户的跳出率，更快的页面响应意味着更多的PV、更高的参与度，以及更高的转化率。那什么影响FP指标呢？其中一个重要的因素是**网络加载速度**。

要想优化Web页面的加载速度，你需要对网络有充分的了解。而理解网络的关键是要对网络协议有深刻的认识，不管你是使用HTTP，还是使用WebSocket，它们都是基于TCP/IP的，如果你对这些原理有足够了解，也就清楚如何去优化Web性能，或者能更轻松地定位Web问题了。此外，TCP/IP的设计思想还有助于拓宽你的知识边界，从而在整体上提升你对项目的理解和解决问题的能力。

因此，在这篇文章中，我会给你**重点介绍在Web世界中的TCP/IP是如何工作的**。当然，协议并不是本专栏的重点，这篇文章我会从我的角度结合HTTP来分析网络请求的核心路径，如果你想对网络协议有更深入的理解，那我推荐你学习刘超老师的《趣谈网络协议》专栏，以及陶辉老师的《Web协议详解与抓包实战》视频课程。

好，接下来我们回到正题，开始今天的内容。在网络中，一个文件通常会被拆分为很多数据包来进行传输，而数据包在传输过程中又有很大概率丢失或者出错。**那么如何保证页面文件能被完整地送达浏览器呢？**
<div><strong>精选留言（30）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/13/c0/17/033a9287.jpg" width="30px"><span>Dongz</span> 👍（242） 💬（4）<div>HTTP协议和TCP协议都是TCP&#47;IP协议簇的子集。

HTTP协议属于应用层，TCP协议属于传输层，HTTP协议位于TCP协议的上层。

请求方要发送的数据包，在应用层加上HTTP头以后会交给传输层的TCP协议处理，应答方接收到的数据包，在传输层拆掉TCP头以后交给应用层的HTTP协议处理。建立 TCP 连接后会顺序收发数据，请求方和应答方都必须依据 HTTP 规范构建和解析HTTP报文。</div>2019-08-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/57/8e/67990114.jpg" width="30px"><span>sheldon</span> 👍（100） 💬（19）<div>现在的浏览器可以同时打开多个页签，他们端口一样吗？如果一样，数据怎么知道去哪个页签？</div>2019-08-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/7b/f0/ccc11dec.jpg" width="30px"><span>Cris</span> 👍（56） 💬（1）<div>http 和 websocket都是属于应用层的协议吗？</div>2019-08-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/86/06/72b01bb7.jpg" width="30px"><span>美美</span> 👍（50） 💬（3）<div>tcp传送数据时 浏览器端就做渲染处理了么？如果前面数据包丢了 后面数据包先来是要等么？类似的那种实时渲染怎么处理？针对数据包的顺序性？</div>2019-08-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/d5/7e/5ce202d6.jpg" width="30px"><span>高斯定律</span> 👍（36） 💬（3）<div>这个tcp讲的非常清晰  一次就听明白了、tcp是个梯子，http就是利用梯子来搬运货物</div>2019-08-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/17/a8/41/b263223b.jpg" width="30px"><span>黄紫茜</span> 👍（30） 💬（4）<div>我想问下，输入url回车后理论上是不是生成http请求报文，然后传给TCP，加上TCP首部，然后进行三次握手，将http请求报文数据传递，四次挥手，请求报文到达服务端，然后服务端在返回响应报文，返回到过程也是要三次握手，传递数据，四次挥手？因为网上看到不少文章都说先三次握手，然后发起http请求。</div>2019-08-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/f7/a1/f2792182.jpg" width="30px"><span>orionis</span> 👍（24） 💬（2）<div>我记得在网络工程里有一句话,下层为上层提供服务,TCP为HTTP提供差错校验,超时重传的机制吧.</div>2019-08-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/e8/f3/01ce824b.jpg" width="30px"><span>我是辣妈</span> 👍（19） 💬（3）<div>1、IP 负责把数据包送达目的主机。
2、UDP 负责把数据包送达具体应用。
3、而 TCP 保证了数据完整地传输，它的连接可分为三个阶段：建立连接、传输数据和断开连接。

老师，这里面第二条，UDP和TCP都是把数据包送达具体应用应用的吧？</div>2019-08-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/7b/f0/ccc11dec.jpg" width="30px"><span>Cris</span> 👍（15） 💬（2）<div>老师，tcp和udp都是传输层协议，这两个是同时存在还是只能选其一，我看了这期感觉是选其一？</div>2019-09-02</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/6LaITPQ4Lk5fZn8ib1tfsPW8vI9icTuSwAddiajVfibPDiaDvMU2br6ZT7K0LWCKibSQuicT7sIEVmY4K7ibXY0T7UQEiag/132" width="30px"><span>尔东橙</span> 👍（14） 💬（3）<div>老师，那我打开谷歌浏览器里面开了10个页面，那就是至少有40个进程？windows下我控制面板里能看到40个google.exe？插件进程页面间能公用么</div>2019-08-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/a1/fe/8e29ffc0.jpg" width="30px"><span>sam</span> 👍（11） 💬（3）<div>这篇文章可以当作平时购物的流程就很清晰的理解：
数据包： 我们可以理解为我们买的东西；
TCP&#47;UDP头：买卖人电话、姓名等；
IP头：买卖双方地址；

TCP和UDP不同点在于，TCP会把购买的物品直接送到购买人手中，而UDP可能只是送到蜂巢如此之类的。

不过我有个疑问，三次握手的过程当中是否也是需要走三次传输流程？</div>2019-08-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/b3/e7/227ee616.jpg" width="30px"><span>阿桐</span> 👍（9） 💬（1）<div>文章前面从网络层引到传输层，再从 udp 过渡到 tcp，语言通俗易懂，图示也很清晰，看的意犹未尽。相比之下，后面的 【一个 tcp 连接的生命周期】老师用的笔墨就少了点，其实还是蛮期待老师能对这块有更为细致的讲解。</div>2019-08-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/9d/5d/3fdead91.jpg" width="30px"><span>レイン小雨</span> 👍（6） 💬（6）<div>想问一下老师，关于 &quot;数据在传输的过程中有可能会丢失或者出错&quot;，丢失的数据包去哪里了？凭空消失了吗？出错的数据包又变成啥了？ 为什么会出错？</div>2019-08-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/7b/f0/ccc11dec.jpg" width="30px"><span>Cris</span> 👍（3） 💬（4）<div>Tcp&#47;udp通过端口号把数据包发送给指定的程序，这里的端口号和http协议默认端口号80(Https默认端口号443)是一个意思吗？</div>2019-09-02</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/f9/90/5cd5d680.jpg" width="30px"><span>成</span> 👍（3） 💬（1）<div>可不可以形象地把TCP理解为一个传送带，而HTTP是一种具体类型的货物，TCP负责运送这种货物并且保证不会弄丢？</div>2019-08-16</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/39/1b/bcabd223.jpg" width="30px"><span>Snow同學</span> 👍（2） 💬（1）<div>好希望更新刚快一些 哈哈</div>2019-08-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/f4/4f/6be9c5d7.jpg" width="30px"><span>°半月含雪雨</span> 👍（1） 💬（1）<div>在TCP&#47;IP五层结构中，http协议属于应用层，应用层主要是来为操作系统和应用程序提供网络服务。而TCP属于传输层，传输层用来处理全部信息和提供可靠的数据传输服务。</div>2019-08-13</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/ibZVAmmdAibBeVpUjzwId8ibgRzNk7fkuR5pgVicB5mFSjjmt2eNadlykVLKCyGA0GxGffbhqLsHnhDRgyzxcKUhjg/132" width="30px"><span>pyhhou</span> 👍（1） 💬（1）<div>请教老师一下，TCP&#47;IP 建立连接和断开连接要经历三次握手和四次挥手，那么 TCP 和 HTTP 建立连接和断开连接是不是也要经历这么一个过程，还是说另有别的考虑？</div>2019-08-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/8c/d5/398b31fe.jpg" width="30px"><span>木棉</span> 👍（1） 💬（1）<div>http协议是超文本协议，浏览器发出http请求，TCP会把请求向底层传递知道web服务器，然后web服务器返回http请求的response，浏览器渲染数据</div>2019-08-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/14/2e/400913b1.jpg" width="30px"><span>金波</span> 👍（1） 💬（2）<div>只是简单罗列了下</div>2019-08-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/7b/f0/ccc11dec.jpg" width="30px"><span>Cris</span> 👍（0） 💬（1）<div>老师，ip地址中的ip是internet protocol网际协议的缩写？</div>2019-09-02</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/18/eb/f0/c687d678.jpg" width="30px"><span>433590</span> 👍（0） 💬（1）<div>个人认为总结中的第二条应该是，TCＰ协议和UDP协议都是会把数据包送达某一应用（端口号）</div>2019-08-21</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/ExHHyMiauDKhjmy4n8rgA1e3IVRd8vegMAnOFC7u6p9aiaefEJEZKa2Pu5rARLbeNicuz9NFicpF5YXEFf35gNn2vQ/132" width="30px"><span>阿段</span> 👍（0） 💬（2）<div>每个数据包的大小是固定的么？还是变化的？</div>2019-08-15</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/97/1a/389eab84.jpg" width="30px"><span>而立斋</span> 👍（0） 💬（1）<div>在同一个请求过程中，tcp跟udp是二选一吧？他们会都用吗？</div>2019-08-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/18/5f/02/f8a80843.jpg" width="30px"><span>XWL</span> 👍（0） 💬（1）<div>那丢包一般是什么原因</div>2019-08-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1c/d9/f8/290ef739.jpg" width="30px"><span>白糖炒栗子~</span> 👍（173） 💬（7）<div>在评论区也学到了很多，小总结：
1. 浏览器可以同时打开多个页签，他们端口一样吗？如果一样，数据怎么知道去哪个页签？
   端口一样的，网络进程知道每个tcp链接所对应的标签是那个，所以接收到数据后，会把数据分发给对应的渲染进程。

2. TCP传送数据时 浏览器端就做渲染处理了么？如果前面数据包丢了 后面数据包先来是要等么？类似的那种实时渲染怎么处理？针对数据包的顺序性？
    接收到http响应头中的content-type类型时就开始准备渲染进程了，响应体数据一旦接受到便开始做DOM解析了！基于http不用担心数据包丢失的问题，因为丢包和重传都是在tcp层解决的。http能保证数据按照顺序接收的（也就是说，从tcp到http的数据就已经是完整的了，即便是实时渲染，如果发生丢包也得在重传后才能开始渲染）

3. http 和 websocket都是属于应用层的协议吗？
都是应用层协议，而且websocket名字取的比较有迷惑性，其实和socket完全不一样，可以把websocket看出是http的改造版本，增加了服务器向客户端主动发送消息的能力。

4. 关于 &quot;数据在传输的过程中有可能会丢失或者出错&quot;，丢失的数据包去哪里了？凭空消失了吗？出错的数据包又变成啥了？ 为什么会出错？
比如网络波动，物理线路故障，设备故障，恶意程序拦截，网络阻塞等等</div>2020-04-06</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTLHOZjqhVkWgUrUibLnXkiaFkhJdfWT2BZP3LldE3tArIoHASlhTSp8tiatiamLbQOjKeMcYHkAexoyCg/132" width="30px"><span>江霖</span> 👍（53） 💬（3）<div>谢谢李冰老师，断断续续的花了很长时间终于要学完了，回顾完整个学习过程，感触颇多也和老师一样来做个总结和同学们分享：
1. 首先知识方面的收获：
学习完整个课程之后我对浏览器的整体架构和如何运作的有了一个宏观的理解，明白了浏览器是由哪些部分构成，这些部分是怎么配合来完成任务以及浏览器是如何与服务器交互的。
这让我的前端后端散装知识能够联系到一起，形成了一张知识网，感觉更容易记忆了

在一些比较重要的知识点上如页面的渲染，javascript的运行机制和网络安全等方面跟随老师的文章进行深度的挖掘，对这些知识有了更深层次的理解，掌握程度更高，工作中遇到的比较难解决的问题时也能很快的有一个清晰的思路

2. 如何学习一门知识的思路
以前我的学习方式是贪多而且杂，分不清主次，所有的东西搅在一起，学了不少但始终感觉没法融汇贯通和更深入的理解，多数知识只是停留到如何应用这一层
学习了老师的课程中知识的同时也学习如何学习一门知识的思路：
1) 搭建整个知识的框架（体），化繁为简对这门知识有个宏观整体的理解
2) 对于框架的每个部分进行拆分相关的知识点拆分成一个系列（面）
3) 之后再深入挖掘每个系列中的每个知识点（线）
4) 在每个知识点中分析其原因，解决的问题，历史，定义等（点），并使用简练有逻辑的语言配合图表将每个点讲清楚
5) 每章总结，化繁为简，梳理出关键的知识点形成记忆的主干，配合框架让知识形成树状结构。知识体系是根-&gt;每章总结是主干-&gt;讲解的知识点原因，历史等是叶子
6) 每章后的思考，学而不思则罔，思而不学则殆。对知识进行更进一步的思考，能够加深对知识的理解并且检查是否有欠缺的地方，计划下一步的学习方案等

3. 如何将知识写成文章
首先对整个知识需要有深度的了解
文章的思路就是学习的思路
考虑受众进行整体设计，确定文章的定位和目标，懂得舍弃，杂项影响主干完成的知识点作为加餐补充
使用总分的形式拆分章节
使用写作技巧多用图表，转折链接各个章节，简练的语言

说实话我是个喜欢白嫖的程序员，对于知识付费一向不以为然，这门课程是我的第一个网课，完全改变了我对知识付费的看法。
课程真的性价比超高很多东西真的不是靠自己短时间学习能够掌握的，跟着网课系统学习是一种很高效的学习方式，跟着老司机不翻车，之后感兴趣的话可以深度学习也成为一名合格的老司机

希望学习到的东西能够应用到工作中，学习知识和记录笔记等方面
感谢老师，祝老师越写越好，给我们带来更多更精彩的课程


</div>2020-07-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/a3/ea/53333dd5.jpg" width="30px"><span>HoSalt</span> 👍（4） 💬（2）<div>老师你好，有些问题想问下
『TCP（Transmission Control Protocol，传输控制协议）是一种面向连接的、可靠的、基于字节流的传输层通信协议』
1. 基于字节流是什么意思？
2. UDP不是基于字节流吗，那UDP是基于什么？
3. TCP性能没有UDP好，消耗的性能更多是不是用在了消息确认这套机制上，而非三次握手和四次挥手上，难道建立链接和断开链接很费时吗？平时应用中都是说通过减少http的连接数来提升性能</div>2020-04-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1d/fd/5b/0c821fbc.jpg" width="30px"><span>Cshine🌸🌸</span> 👍（2） 💬（0）<div>感觉很清晰，层层递减，打call！！</div>2020-05-06</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/26/f3/5c6f125b.jpg" width="30px"><span>学习</span> 👍（2） 💬（2）<div>IP协议是高速公路，TCP协议是货车，HTTP协议是货物。</div>2020-01-12</li><br/>
</ul>