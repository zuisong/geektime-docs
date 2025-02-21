首先我来问出这个问题：“你觉得HTTP是什么呢？”

你可能会不假思索、脱口而出：“HTTP就是超文本传输协议，也就是**H**yper**T**ext **T**ransfer **P**rotocol。”

回答非常正确！我必须由衷地恭喜你：能给出这个答案，就表明你具有至少50%HTTP相关的知识储备，应该算得上是“半个专家”了。

不过让我们换个对话场景，假设不是我，而是由一位面试官问出刚才的问题呢？

![unpreview](https://static001.geekbang.org/resource/image/b4/bf/b4de4be0f7dfd4185464bb5a1d6df0bf.png?wh=1142%2A640)

显然，这个答案有点过于简单了，不能让他满意，他肯定会再追问你一些问题：

- 你是怎么理解HTTP字面上的“超文本”和“传输协议”的？
- 能否谈一下你对HTTP的认识？越多越好。
- HTTP有什么特点？有什么优点和缺点？
- HTTP下层都有哪些协议？是如何工作的？
- ……

几乎所有面试时问到的HTTP相关问题，都可以从这个最简单的“HTTP是什么？”引出来。

所以，今天的话题就从这里开始，深度地解答一下“**HTTP是什么？**”，以及延伸出来的第二个问题“**HTTP不是什么？**”

## HTTP是什么

咱们中国有个成语“人如其名”，意思是一个人的性格和特点是与他的名字相符的。

先看一下HTTP的名字：“**超文本传输协议**”，它可以拆成三个部分，分别是：“**超文本**”“**传输**”和“**协议**”。我们从后往前来逐个解析，理解了这三个词，我们也就明白了什么是HTTP。
<div><strong>精选留言（30）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/10/ab/e1/079ee6e3.jpg" width="30px"><span>壹笙☞漂泊</span> 👍（130） 💬（9）<div>问题一：
我觉得这种说法是错误的。
    理由：HTTP是在计算机世界里，用于两点之间之间传输超文本的协议。这两点并不限定于是服务器还是浏览器。可以是从浏览器到服务器，也可以从服务器到服务器，也可以是浏览器到浏览器。并不能描述成从服务器到浏览器。
问题二：
HTTP不是软件、不是网址（暂时想到的比较少）
总结：
协议：HTTP是一个用在计算机世界里的协议。它使用计算机能够理解的语言确立了一种计算机之间交流通信的规范，以及相关的各种控制和错误处理方式
 传输：HTTP是一个在计算机世界里专门用来在两点之间传输数据的约定和规范
        1、HTTP协议是一个“双向协议”
        2、不限定两个角色，允许有中转或接力A&lt;=&gt;X&lt;=&gt;Y&lt;=&gt;Z&lt;=&gt;B    
文本：完整的有意义的数据，可以被上层应用程序处理
        包括但不限于 文字、图片、音频、压缩包
超文本：超越了普通文本的文本。是文字、图片、音频和视频等的混合体。最关键的是含有超链接。能从一个超文本跳跃到另一个超文本。形成复杂的非线性、网状的结构关系。

HTTP是一个在计算机世界里专门在两点之间传输文字、图片、音频、视频等超文本数据的约定和规范。

HTTP不是互联网、不是编程语言、不是HTML，不是一个孤立的协议
    HTTP通常跑在TCP&#47;IP协议栈之上，依靠IP实现寻址和路由、TCP协议实现可靠数据传输、DNS协议实现域名查找、SSL&#47;TLS协议实现安全通信。此外，还有一些协议依赖于HTTP，例如WebSocket、HTTPDNS等。这些协议相互交织，构成了一个协议网，而HTTP则处于中心地位。

</div>2019-05-31</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/e0/0c/c6151e22.jpg" width="30px"><span>团结屯儿王二狗</span> 👍（62） 💬（1）<div>所谓的专家是用大家能听懂的语言，把复杂的知识讲明白。看的出来峰哥简单的背后是巨大的知识储备，感觉很用心，不错。期待后面文章能够让大家循序渐进、由浅入深，已关注，哈哈哈</div>2019-06-04</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/23/74/e0b9807f.jpg" width="30px"><span>小米</span> 👍（44） 💬（1）<div>这是我看过的讲HTTP最通俗易懂的文章，忍不住要点赞！</div>2019-05-31</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/48/d2/eb4c3649.jpg" width="30px"><span>A-Lang</span> 👍（31） 💬（1）<div>这个课程感觉很适合基础的同学学习!不知道后面老师会不会逐渐深入讲解一些深层次的东西</div>2019-05-31</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/f7/72/2d35f80c.jpg" width="30px"><span>xing.org1^</span> 👍（23） 💬（6）<div>老师您好，请问小结第二条，说http是在两点之间进行传输数据。我的疑惑是：http不是协议吗？我就按照老师的比喻把他理解为“协议”、“合同”了，如果就是纸上的约定，只是一个规范的话，http怎么做传输数据的事情呢？另外http又是怎么做到的呢？

我的网络知识真的是小白，问的很幼稚还请见谅:)</div>2019-06-07</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/17/07/fa/62186c97.jpg" width="30px"><span>恩佐</span> 👍（20） 💬（2）<div>老师你的知识导图里有错误
错误在HHTTP&#47;2里的gRPC
您写的是gRFC</div>2019-06-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/7f/a2/8ccf5c85.jpg" width="30px"><span>XThundering</span> 👍（10） 💬（2）<div>有个小问题，为什么文章说HTTP通常跑在 TCP&#47;IP协议栈之上，请问还有其它协议栈吗？</div>2019-05-31</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/76/a7/374e86a7.jpg" width="30px"><span>欢乐的小马驹</span> 👍（9） 💬（1）<div>我定了快二十个专栏。这是唯一一个对所有人回复的专栏 👍</div>2020-02-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/b7/cb/18f12eae.jpg" width="30px"><span>不靠谱～</span> 👍（9） 💬（1）<div>1 错误的说法，Http可以在任意两点间进行传输。只是从服务器传输到浏览器这种形式比较常见。
2 http不是一种服务，不是一种语言，不是一种网络。只是一种协议，一种约定。

感谢老师分享</div>2019-05-31</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/fb/2d/e6548e48.jpg" width="30px"><span>tokamak</span> 👍（8） 💬（1）<div>老师你好，我想用Linux C++写一个HTTP Client，但有个问题：当我用socket套接字接收HTTP 响应报文时，会调用recv(int sockfd, void *buf, size_t len, int flags);，这里的len填多少合适呢？开源代码里有填1个字节的，也有填4096个字节的，你怎么看这个问题？</div>2019-05-31</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/30/8a/b5ca7286.jpg" width="30px"><span>业余草</span> 👍（6） 💬（1）<div>作者写的很用心！点赞👍
HTTP 协议是双向的。服务器 -&gt; 客户端，客户端 -&gt; 服务器。
期待后面的内容</div>2019-05-31</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/09/da/9b2f84d9.jpg" width="30px"><span>毕竟养猪能致富</span> 👍（5） 💬（1）<div>罗老师，我今年7月毕业，我也是软件工程专业的。感觉看了你的课程真的懂了很多，讲得非常详细，越看越想看，本来都准备睡觉了，结果没睡着，起来又看了遍。😂希望在后面的课程能学到更多知识。嘻嘻</div>2019-06-01</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/07/8c/0d886dcc.jpg" width="30px"><span>蚂蚁内推+v</span> 👍（4） 💬（1）<div>1. 「用于从互联网服务器传输超文本到本地浏览器」的说法太过片面，HTTP 是在两点之间，即服务端与客户端，而客户端不仅包括本地浏览器，服务器也可以作为客户端，其他的 App、小程序等应用程序也属于客户端。
2. HTTP 不是软件：HTTP 是没有实体的协议，而软件是一种具体实现。</div>2019-06-04</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/7e/bb/019c18fc.jpg" width="30px"><span>徐云天</span> 👍（4） 💬（1）<div>总而言之，http是一个通信协议，它有它的规范。不会限制在某个平台。任何计算机，都可以使用它。计算机程序之间的通信可以使用它。</div>2019-05-31</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/8b/6c/004026f4.jpg" width="30px"><span>个人学习</span> 👍（3） 💬（1）<div>罗老师，您好，有个疑问，HTTP 是在两点之间传输数据，这个「两点」是理解为两个终端设备之间吗？但是，我们学习网络协议，知道数据是一层一层传输，从 A 终端的网络层-&gt;....-&gt;物理层，然后到 B 终端的物理层-&gt;...-&gt; 网络层。而  HTTP 协议在这个过程仅仅能接触到的只是「客户端」以及「传输层协议」呀。所以，这个两点是否能够理解为只是「客户端」和「传输层协议」之间的数据传输？</div>2019-05-31</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/2a/d5/62dfbc11.jpg" width="30px"><span>patsun</span> 👍（3） 💬（3）<div>
HTTP可应用的个体是两个或者两个以上，对象可以是服务器与服务器、服务器与本地浏览器，本地浏览器与本地浏览器。

http不是网址</div>2019-05-31</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/26/eb/d7/90391376.jpg" width="30px"><span>ifelse</span> 👍（1） 💬（1）<div>编程语言是人与计算机沟通交流所使用的语言，而 HTTP 是计算机与计算机沟通交流的语言。--记下来</div>2023-01-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/d2/17/b52417a6.jpg" width="30px"><span>迷途</span> 👍（1） 💬（1）<div>打卡</div>2022-10-30</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/8d/0e/5e97bbef.jpg" width="30px"><span>半橙汁</span> 👍（1） 💬（1）<div>问题1:
    对错各参一点，狭隘的理解http的部分功能确实是从互联网服务器传输超文本到本地浏览器的协议；结合本章学到的内容，不正确的理解在于太过片面，HTTP可以被定义为：‘与 HTTP 协议相关的所有应用层技术的总和’
问题2：
    http不是静止存在的，不是单独的存在的，不是一门单独的语言。</div>2022-07-04</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/8SdpYbicwXVXt0fIN7L0f2TSGIScQIhWXT7vTze9GHBsjTvDyyQW9KEPsKBpRNs4anV61oF59BZqHf586b3o4ibw/132" width="30px"><span>Leolee</span> 👍（1） 💬（1）<div>半路出家的小白程序员报道，这个课程说得非常明白，连我这种基础不这么好的都听懂了而且入脑了。
HTTP（HyperText Transfer Protocol：超文本 传输 协议 （超媒体传输协议）；
超文本（HyperText）：超越了普通文本的文本，可以包含图片、视频、音频、文字，还包含了超链接，可以在当前超文本跳转到其他超文本（这个也是普通文本做不到的，与超文本的根本区别。
传输（Transfer）：在两点之间传输数据，这两点之间可以有多个支点节点，但不能用来寻址、广播、路由。
协议（Protocol）：双向协议，协议两方分别为请求方以及响应方（应答方）。浏览器A发送一些数据给网站B，网站再把一些数据传输给浏览器，呈现在电脑浏览器上的就是我们看到的各种内容了。</div>2021-04-02</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/94/82/d0a417ba.jpg" width="30px"><span>蓝配鸡</span> 👍（1） 💬（1）<div>有一种流行的说法：“HTTP 是用于从互联网服务器传输超文本到本地浏览器的协议”。
对在哪里?
    http确实是一种传输协议

又错在哪里？
    1. HTTP的client不仅仅是浏览器。
    2. 传输的内容不仅限于文本，可以是图片， 音频， 视频等。

你能再说出几个“HTTP 不是什么”吗？
    这个多了：）HTTP不是电饭煲，不能烧水， 不能吃 。。。。。。</div>2019-10-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/f7/72/2d35f80c.jpg" width="30px"><span>xing.org1^</span> 👍（1） 💬（1）<div>哇，好喜欢这个专栏。收获满满。谢谢老师</div>2019-06-07</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/81/51/4999f121.jpg" width="30px"><span>qzmone</span> 👍（1） 💬（1）<div>1，不准确，http传输的实际上是多媒体资源，HTML只是多媒体资源的一种标识语言。
2. http是传输协议，不是寻址、隧道、广播等协议。也不是应用程序，编程语音，操作系统等</div>2019-06-05</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/ee/e2/23e44221.jpg" width="30px"><span>余熙</span> 👍（1） 💬（1）<div>讲的很有趣！
一、课后题
问题一： 我觉得这种说法，协议和超文本的描述是对的。从服务器传输超文本到浏览器是不对的。超文本除了从服务器传输到浏览器、还可以浏览器到服务器（比如上传图片、视频，输入用户信息等）、还可以从服务器到服务器传输。
问题二：HTTP 不是算法、不是数据结构、不是数据库、不是机房

二、我的疑问
问题1  A&lt;===&gt;B  这个表示看起来浏览器既可以是请求方，也可以是响应方。如果浏览器可以作为响应方，什么时候会出现，会有错误标识返回服务器吗
问题2 websocket 的设计是依赖于 HTTP 的，它是 tcp 上包了壳，那为何要依赖于 HTTP (希望后面有机会得到解答哈)
</div>2019-06-02</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/1c/2e/93812642.jpg" width="30px"><span>Amark</span> 👍（1） 💬（2）<div>老师，WebSocket协议跟http协议有啥关系?</div>2019-05-31</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/27/d5/0fd21753.jpg" width="30px"><span>一粟</span> 👍（1） 💬（1）<div>超媒体传输协议更形象，但“超”字含义不明，不好理解，改成“富媒体”或“多媒体”可否?</div>2019-05-31</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/1b/6e/cd8fea9f.jpg" width="30px"><span>RecordLiu</span> 👍（0） 💬（1）<div>问题 1：
说的也对，但不完全对。

因为 HTTP 不仅可以作为 web 服务器和浏览器之间进行超文本数据传输的协议，它还可以作为服务器与服务器之间传输协议，比如 api（接口）之间的 curl 请求场景。

问题 2:
1.http 不是开源项目，它在 github 上没有源码
2.http 不是具体的软件技术，不属于哪家公司的技术专利</div>2024-08-30</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/27/1f/06/a154381b.jpg" width="30px"><span>翟浩</span> 👍（0） 💬（1）<div>http是双向的而非作业中描述的单向</div>2023-04-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/35/7e/5a/6073d5a0.jpg" width="30px"><span>Ethan</span> 👍（0） 💬（2）<div>老师，这些课件都有嘛</div>2023-02-16</li><br/><li><img src="" width="30px"><span>Geek_21da11</span> 👍（0） 💬（1）<div>问题1:
忽略了客户端同样也能上传数据
问题2</div>2023-02-02</li><br/>
</ul>