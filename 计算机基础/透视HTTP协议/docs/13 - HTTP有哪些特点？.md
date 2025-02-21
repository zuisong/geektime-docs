通过“基础篇”前几讲的学习，你应该已经知道了HTTP协议的基本知识，了解它的报文结构，请求头、响应头以及内部的请求方法、URI和状态码等细节。

你会不会有种疑惑：“HTTP协议好像也挺简单的啊，凭什么它就能统治互联网这么多年呢？”

所以接下来的这两讲，我会跟你聊聊HTTP协议的特点、优点和缺点。既要看到它好的一面，也要正视它不好的一面，只有全方位、多角度了解HTTP，才能实现“扬长避短”，更好地利用HTTP。

今天这节课主要说的是HTTP协议的特点，但不会讲它们的好坏，这些特点即有可能是优点，也有可能是缺点，你可以边听边思考。

![](https://static001.geekbang.org/resource/image/78/4a/7808b195c921e0685958c20509855d4a.png?wh=1717%2A1165)

## 灵活可扩展

首先， HTTP协议是一个“灵活可扩展”的传输协议。

HTTP协议最初诞生的时候就比较简单，本着开放的精神只规定了报文的基本格式，比如用空格分隔单词，用换行分隔字段，“header+body”等，报文里的各个组成部分都没有做严格的语法语义限制，可以由开发者任意定制。

所以，HTTP协议就随着互联网的发展一同成长起来了。在这个过程中，HTTP协议逐渐增加了请求方法、版本号、状态码、头字段等特性。而body也不再限于文本形式的TXT或HTML，而是能够传输图片、音频视频等任意数据，这些都是源于它的“灵活可扩展”的特点。
<div><strong>精选留言（30）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/10/ab/e1/079ee6e3.jpg" width="30px"><span>壹笙☞漂泊</span> 👍（63） 💬（1）<div>课后题：
1、我觉得所谓的优点和缺点都是要区别场景来看待的，比如，在一些长连接场景中，需要保存上下文状态，那么无状态这一点就成为缺点甚至是致命缺点了。但是在客户端-服务端通信中，如果场景不需要保存上下文信息，那么无状态就可以减少一些网络资源消耗，也就是优点了。
2、可靠传输对我比较重要，减少很多查错的工作。。。
总结：
http特点：
灵活可扩展
    可以扩展头字段实现功能
可靠传输
    HTTP并不能100%保证数据一定能够发送到另一端，在网络繁忙、连接差等恶劣环境时，也有可能收发失败，可靠只是向使用者提供了一个承诺，会在下层用多种手段尽量保证数据的完整送达
应用层协议

请求-应答通信模式
    客户端主动请求，服务端被动响应
无状态协议
    状态：客户端或者服务器里保存的一些数据或者标志，记录了通信过程中的一些变化信息
    每个请求都是互相独立，毫无关联的，两端都不会记录请求相关的信息</div>2019-06-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/2e/53/bf62683f.jpg" width="30px"><span>狼的诱惑</span> 👍（44） 💬（1）<div>老师好，有两点疑问
1、为什么说MQ的比HTTP是高可靠的
2、个人觉得http的无状态，完全符合可扩展，轻量级、易维护现代设计，属于优点，不算是缺点，为什么大家认为不支持有状态就算是缺点，如果http做成有状态，估计复杂度会非常高吧？
个人想法，还请老师指正</div>2019-07-31</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/DYAIOgq83erwIgbTd3oy4GzkdCUBmz8lHGIIWBwoSIfibgQzwDlQuvTrLlqwTh7p99NBJIsu98ziaYoroQCSENwA/132" width="30px"><span>Celine</span> 👍（23） 💬（1）<div>Http的缺点，无状态，在需要身份信息验证的时候就显示为缺点，用户登陆后每次请求都需要阐释一下身份，不能保存登陆成功的状态，不过现在可以在头字段里加入cookie或者token来解决这个问题;请求应答模式，导致服务器端只能被动的接收而不能主动推送，如果服务器资源状态变化的时候想要主动推送到客户端就需要借助其他协议来完成，比如we socket</div>2020-03-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/67/f4/9a1feb59.jpg" width="30px"><span>钱</span> 👍（19） 💬（1）<div>1：就如同开头我讲的那样，你能说一下今天列出的这些 HTTP 的特点中哪些是优点，哪些是缺点吗？
灵活可扩展是优点，没有这一点，她不可能一统江湖，这也是她敢说“在坐的各位都是垃圾”的底气。
灵活可扩展是缺点，她引入了一定的复杂度，增加了一定的学习成本。
可靠传输协议是优点，保证了数据的可靠性。
可靠传输协议是缺点，必须先建连才行，效率估计不如UDP。
应用层协议是优点，靠近用户，对用户优化，方便使用。
应用层协议是缺点，越往上处理的事情会越多，通信效率会差一些。
请求应答模式是优点，符合人类的对话方式容易理解，一个请求得到响应在发生另外一个。
请求应答模式是缺点，我请求一个资源，发现不够再请求一次，你一次回给我俩，不用回两次这么简单的事就做不到。
无状态是优点，无状态意味着易扩展，也不需要保持状态信息，节省空间。
无状态是缺点，我想保持回话状态还必须自己去想办法。

好吧！😅我编不下去了，不过我觉得HTTP最大的优点就是灵活可扩展，我们自己设计程序也希望做到这样，不过真要如此，复杂度会马上上去，不过HTTP确做到了灵活可扩展但是复杂度却没有增加太多。这一点太厉害了。

2：不同的应用场合有不同的侧重方面，你觉得哪个特点对你来说是最重要的呢？
看应用场景吧！目前，可靠传输对我而言至关重要，效率可以放一放，安全稳定第一。</div>2020-03-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/5d/48/03abbbd1.jpg" width="30px"><span>瑞</span> 👍（19） 💬（2）<div>http无状态不是特别理解，状态的意思就是一个事物因为外界因素导致这个事物的形态，使用等发生改变，这个就是有状态的吧，http作为一个协议，本质不承载任何东西，只是一个数据的传输通道，即使传输通道里的数据有状态改变，也不能称为是http状态改变，因为理解为无状态，可以这样理解吗？</div>2019-06-29</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/6LaITPQ4Lk5fZn8ib1tfsPW8vI9icTuSwAddiajVfibPDiaDvMU2br6ZT7K0LWCKibSQuicT7sIEVmY4K7ibXY0T7UQEiag/132" width="30px"><span>尔东橙</span> 👍（15） 💬（3）<div>HTTP的长连接和无状态不矛盾么</div>2019-12-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/55/cb/1efe460a.jpg" width="30px"><span>渴望做梦</span> 👍（11） 💬（2）<div>老师，这个顺序发包和顺序收包不是很理解，是是指第一个发送的请求一定会排在第一位处理吗？</div>2019-08-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/08/17/e63e50f3.jpg" width="30px"><span>彩色的沙漠</span> 👍（7） 💬（4）<div>请求应答模式也就注定了HTTP不适合用于IM场景？</div>2019-06-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/55/f2/ba68d931.jpg" width="30px"><span>有米</span> 👍（6） 💬（1）<div> 即使是当红MQ也没人敢打包票100%不丢</div>2020-05-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/18/fa/dd/f640711f.jpg" width="30px"><span>哈德韦</span> 👍（5） 💬（1）<div>尽量送达不是UDP的特征吗？只送出去不确认的，而TCP是保证送达，收不到确认会重试的，如果实在不行就会报错。HTTP基于它，应该也是保证送达吧？</div>2020-10-07</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/18/65/35361f02.jpg" width="30px"><span>潇潇雨歇</span> 👍（3） 💬（2）<div>1、无状态是把双刃剑，设计成无状态能够减少资源的使用。但是如果需要保存用户身份，那么无状态就是缺点了。
2、可靠传输和请求应答吧，能确定成功发起请求和收到响应很重要。这也是平常开发的基础</div>2020-06-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/42/1a/de91a790.jpg" width="30px"><span>ddq432</span> 👍（3） 💬（3）<div>我有个问题，http 用 tcp 来尽量保持可靠请求，客户端发送一次请求服务，服务端会发送一个tcp的ack，告诉客户端我收到消息了，假如说这次发送的tcp下的ack信息，客户端没收到，会怎么办</div>2019-12-05</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/18/22/89/73397ccb.jpg" width="30px"><span>响雨</span> 👍（3） 💬（1）<div>优点：灵活拓展性强
缺点：明文传输
因时而异：无状态</div>2019-07-04</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/27/d5/0fd21753.jpg" width="30px"><span>一粟</span> 👍（3） 💬（2）<div>终于明白为何是HTTP一统天下了，扬长避短灵活使用才是王道。</div>2019-06-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/c7/0c/8e7f1a85.jpg" width="30px"><span>Tintin</span> 👍（2） 💬（2）<div>1. 优点：可扩展（更能适应不确定的环境）、可靠（在可靠比时效性重要的场景下）；缺点：可靠（在时效性比可靠更重要的场景下）、请求应答模式（服务器无法主动推送数据给浏览器）、无状态</div>2020-06-02</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/19/51/29/24739c58.jpg" width="30px"><span>凉人。</span> 👍（2） 💬（2）<div>cookie应该算是一种上下文么？
 这里有点想不通</div>2020-03-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/7b/f0/ccc11dec.jpg" width="30px"><span>Cris</span> 👍（2） 💬（1）<div>HTTP 完全可以用开玩笑的口吻说：“不要误会，我不是针对 FTP，我是说在座的应用层各位，都是垃圾。”  websocket表示不服</div>2019-08-16</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/64/9b/d1ab239e.jpg" width="30px"><span>J.Smile</span> 👍（1） 💬（2）<div>老师好，看了下边的留言发现也没人问过这个问题。
问题：http是明文的文本报文，TCP是二进制报文，这中间是由谁来决定序列化的呢？序列化的规则是固定的，还是由谁来决定的呢？希望老师解答，感谢。</div>2020-10-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/cf/2f/4f89f22a.jpg" width="30px"><span>李鑫磊</span> 👍（1） 💬（1）<div>老师，特别困惑的是：HTTP、WebService、RPC、RESTful、gRPC、WebSocket 这几个概念之间的联系和区别，纠结...</div>2019-11-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/a3/fc/379387a4.jpg" width="30px"><span>ly</span> 👍（1） 💬（1）<div>一些个人的见解：
正如文章所说，由于http只规定了报文的基本格式，并没有严格的语法规则，例如header我们可以随便自定义、body可以随便传输什么数据，以后只要时代需要，就会存在无穷的可能（只要以后这些web服务器和客户端进行事先的约定就能实现）。
http的可靠性完全由下层的TCP协议承担，http无力承担可靠性。
http对数据的封装，其实就是在数据body的上面加了一个请求行和若干个header（CRLF分隔）。
http的万能，http可以传输任意的内容，比如文件内容（将FTP秒杀）；发送邮件（SMTP秒杀），其根本原因还是HTTP没有严格的要求必须传输什么样的数据，基本上没有限制其应用场景。
</div>2019-08-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/9b/a7/440aff07.jpg" width="30px"><span>风翱</span> 👍（1） 💬（1）<div>1、灵活可扩展是优点，促进其发展。 2和3也是优点。 4、是优点也是缺点，缺点是应答方不能做到主动反馈。 5、即是优点也是缺点，主要是看适用的场景，无状态，请求时需要携带更多的数据。</div>2019-06-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/23/6c/785d9cd3.jpg" width="30px"><span>Snooker</span> 👍（0） 💬（1）<div>确实，像是优点和缺点，要看具体的场景，像是面试时常随口会问的一句“你有什么缺点”。
像是可靠传输，可靠传输必然要有额外的网络开销，在不追求数据可靠的场景这个就是缺点；
像是请求-应答模式，缺点不能主动接受服务端的推送。
类似这样一体两面吧</div>2024-04-16</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1e/a3/4a/d3867ca2.jpg" width="30px"><span>徐小虾</span> 👍（0） 💬（3）<div>TCP会出现粘包和分包的问题。
之前的项目中, 我们一般都是采用发送定长数据的方法, 就是把&quot;长度&quot;放在包头里, recv到数据时, 先解析出包头里存储的&quot;长度&quot;, 然后根据这个进行校验。
HTTP请求头里面并没有数据的长度，问下老师HTTP会出现这个问题吗</div>2023-01-31</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/26/eb/d7/90391376.jpg" width="30px"><span>ifelse</span> 👍（0） 💬（1）<div>“不要误会，我不是针对 FTP，我是说在座的应用层各位，都是垃圾。”--记下来</div>2023-01-23</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/u8g8UoUaBZTGpDgAQKDwLxS2ibE0GfAPED5r0Dnm4RsT22HcWRNE79RFeF9bUP3xQfKa9jiaGUzw0icxK836NvicQQ/132" width="30px"><span>阳树</span> 👍（0） 💬（1）<div>优点与缺点并不绝对，比如我不需要缓存时，无状态就是一个优点，而当我需要缓存时，无状态就是一个缺点。还有的应该算是优点，比如说灵活可扩展，可以添加一些方法，还有HTTP是可靠传输协议，会努力保证数据传输的“可靠”，以及运用了请求应答模式，一接一收。以及HTTP是应用层的协议，能够暴打其他应用层协议，因为它几乎可以传输所有数据类型。</div>2022-03-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/29/b0/d3/200e82ff.jpg" width="30px"><span>功夫熊猫</span> 👍（0） 💬（1）<div>其实http目前我最大的问题，我需要持续的后端里获取数据，所有就必须写个用promise和axios写个轮训函数，这个对我来说很麻烦，所以我最后选择了websocket的协议。</div>2021-10-21</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTKiboeh23vhCNruZ7odUjROiac6N9fx0VWAE6zBNRxJIJFZspSUTQdgu9ajg4F0fAZgdk1vBsicnib3QQ/132" width="30px"><span>在水一方</span> 👍（0） 💬（1）<div>老师，课程中的插图用什么软件画的？</div>2021-06-15</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/DYAIOgq83er6OV33jHia3U9LYlZEx2HrpsELeh3KMlqFiaKpSAaaZeBttXRAVvDXUgcufpqJ60bJWGYGNpT7752w/132" width="30px"><span>dog_brother</span> 👍（0） 💬（1）<div>老师好，在隔壁课程看到这么一个知识点“HTTP 协议属于无状态协议，客户端无法对请求和响应进行关联，每次请求都需要重新建立连接，响应完成后再关闭连接“ 老师您对这句话怎么理解啊？
我还有个疑问是，http长连接下，如何将每次请求和响应对应起来的呢？</div>2021-04-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/20/ae/b6/fc1c61f8.jpg" width="30px"><span>huanshui@smile</span> 👍（0） 💬（1）<div>这些特点是缺点还是优点都要带入到合适的场景下去分析，抛开场景单独去讨论就是耍流氓，比如http的无状态，如果放在一个需要登录的网站，这就是一个致命的缺点，服务器不能记录当前用户登录的信息，每次请求都需要用户重新登录，用户体验极差。反之则亦然，有无状态影响不大。</div>2021-04-24</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/8SdpYbicwXVXt0fIN7L0f2TSGIScQIhWXT7vTze9GHBsjTvDyyQW9KEPsKBpRNs4anV61oF59BZqHf586b3o4ibw/132" width="30px"><span>Leolee</span> 👍（0） 💬（2）<div>作业:
1、HTTP最大的优点应该是灵活可扩展，需要用到的时候可以自己制定，即使标准里没有的也可以改。所以优缺点是看使用场景的，没有绝对的优劣；
2、还是个小白，没有任何项目经验，也没应用过HTTP，所以这题真不知道怎么回答。

再次感谢老师每次的鼓励！谢谢！


HTTP特点：

灵活可扩展
只规定了报文的基本格式，却没对报文的各个组成部分作严格的语法语义先知，可以由开发者任意定制。这也是HTTP协议三十多年来屹立不倒的根基。

可靠传输
基于TCP&#47;IP的HTTP协议也继承了TCP&#47;IP“可靠”的特性，能够在请求方和应答方之间“可靠”地传输数据；它的具体做法与TCP&#47;UDP差不多，都是对传输的数据（entity）做一层包装加一个头，然后调用Socket API，通过TCP&#47;IP协议栈发送或者接收。
可靠的正确含义就是：“承诺”会在下层动用多种手段“尽量”保证数据的完整送达。但遇上光纤段了的极端情况，神仙也不能发送成功。可靠不代表保证100%传输成功。

应用层协议
HTTP可以传输几乎任何数据，只要不苛求性能。它能凭借可携带任意头字段和实体数据的报文结构，以及连接控制、缓存代理等方便一用的特性，技压群雄。比如FTP只能传输文件、SMTP只能发送邮件、SSH只能远程登录，做不到传输通用数据！而HTTP却可以！

请求-应答模式
请求应答模式是HTTP协议最根本的通信模型，也即一发一收、有来有去。这个模式明确了通信双方的定位，请求方先主动发起连接和请求，应答方被动回复，如果没有请求就没有应答动作。
虽然服务器经常作为应答方存在，但如果它勇作代理连接后端服务器，那么它就同时兼具请求方和应答方了。
该模式也契合传统的C&#47;S（Client&#47;Server）系统架构，请求方是Client，应答方是Server。由于客户端笨重，慢慢互联网就发展了B&#47;S（Browser&#47;Server）架构，就是以轻量级的浏览器替换掉客户端。

无状态
TCP是有状态，TCP一开始处于CLOSER状态，连接成功后是ESTABLISHED状态，断开连接后是FIN-WAIT状态，最后又是CLOSED状态。维持这些状态需要TCP在内部用一些数据结构去维护。
无状态形象地说就是“没有记忆能力”，每次收发的报文都是互相独立的，没有任何联系，收发后也不要求保存任何信息，也就不会对客户端和服务器端产生任何影响。
虽然标准没有规定状态，也即无状态存在，但是可以灵活可扩展的HTTP完全可以打个补丁，增加状态。无状态很容易变成有状态，反过来就难了，这也是HTTP灵活性的体现。
这个无状态与响应头里的状态码是两个概念，不能混淆了。</div>2021-04-21</li><br/>
</ul>