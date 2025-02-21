HTTP协议在我们的生活中随处可见，打开手机或者电脑，只要你上网，不论是用iPhone、Android、Windows还是Mac，不论是用浏览器还是App，不论是看新闻、短视频还是听音乐、玩游戏，后面总会有HTTP在默默为你服务。

据NetCraft公司统计，目前全球至少有16亿个网站、2亿多个独立域名，而这个庞大网络世界的底层运转机制就是HTTP。

那么，在享受如此便捷舒适的网络生活时，你有没有想过，HTTP协议是怎么来的？它最开始是什么样子的？又是如何一步一步发展到今天，几乎“统治”了整个互联网世界的呢？

常言道：“**时势造英雄，英雄亦造时势**”。

今天我就和你来聊一聊HTTP的发展历程，看看它的成长轨迹，看看历史上有哪些事件推动了它的前进，它又促进了哪些技术的产生，一起来见证“英雄之旅”。

在这个过程中，你也能够顺便了解一下HTTP的“历史局限性”，明白HTTP为什么会设计成现在这个样子。

## 史前时期

20世纪60年代，美国国防部高等研究计划署（ARPA）建立了ARPA网，它有四个分布在各地的节点，被认为是如今互联网的“始祖”。

然后在70年代，基于对ARPA网的实践和思考，研究人员发明出了著名的TCP/IP协议。由于具有良好的分层结构和稳定的性能，TCP/IP协议迅速战胜其他竞争对手流行起来，并在80年代中期进入了UNIX系统内核，促使更多的计算机接入了互联网。
<div><strong>精选留言（30）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/11/b7/cb/18f12eae.jpg" width="30px"><span>不靠谱～</span> 👍（94） 💬（1）<div>用户需求推动技术发展</div>2019-05-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/54/f3/2216f04f.jpg" width="30px"><span>我叫不知道</span> 👍（62） 💬（2）<div>1.协议标准不同于原理，原理是相对稳定的，而标准则需要与时俱进，随着业务和技术发展中出现的新问题一起变化。在实际商业应用、竞争和实践中反复打磨，让协议标准适应不断发展变化的实际业务问题，而不是让日渐庞大复杂的业务去适应受限于特定时空因素的标准。
标准的诞生和发展一方面是基于具体业务需要和技术发展，另一方面是为了统一游戏规则，让各厂商的软硬件产品可以方便地“互联”，降低“沟通”和“翻译”的成本，提高网络互联的开放性。
2.http对厂商和技术人员来说，某种意义上，是一种技术语言，便于通过软硬件相互沟通；对用户来说……编不下去了
个人的一点拙见，还请大佬点评指正～</div>2019-05-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/17/bc/6d/f6f0a442.jpg" width="30px"><span>汤小高</span> 👍（47） 💬（12）<div>超文本和文本有什么区别吗</div>2019-05-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/78/51/4790e13e.jpg" width="30px"><span>Smallfly</span> 👍（44） 💬（2）<div>老师文中说，HTTP2.0 的新特点：“二进制协议，不再是纯文本”。

那像 HTTP&#47;1.1 中的 application&#47;octet-stream 和 multipart&#47;form-data 也属于本文格式吗？</div>2019-05-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/2f/fd/dead7549.jpg" width="30px"><span>codewu</span> 👍（32） 💬（1）<div>老师提的问题很好，我之前都没考虑过～

比如，
ftp、telnet使用前必须输入用户名和密码，更偏向于一对一的使用，对用户来说不够开放。

而http设计之初就是对所有用户开放，而且还统一了访问方式，使用门槛很低，就会有很多人用。至于后续各种优化和功能的添加，那都是顺其自然的事了。

所以总的来说，是http对用户的开放性，使得用户推动其蓬勃发展。</div>2019-05-30</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/a5/f0/8648c464.jpg" width="30px"><span>Joker</span> 👍（26） 💬（1）<div>从历史的进程来看，就是互联网的用户推动协议的发展的。刚刚开始只有文本，都只是文字；后来有了超文本，不仅仅是文字；后来嫌弃速度慢，有了持久连接，缓存机制；后来为了安全，有了加密通信。一切都是以用户的需求为导向的，用户的需要越来越高，协议就越来越高级，越来越完善。</div>2019-05-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/67/f4/9a1feb59.jpg" width="30px"><span>钱</span> 👍（22） 💬（1）<div>1：你认为推动 HTTP 发展的原动力是什么？
       我觉得推动HTTP协议发展的原动力是人类的好奇心＋逐利，那为啥其他协议没有一统互联网江湖呢？HTTP简单、开放、顺应潮流，初心满足了人类天生好奇的需求，顺势满足了大家都能从中获利的需求，由于这两点支持的力量就变得强大无比，进一步反而增加了她一统互联网天下的能力。

2：你是怎么理解 HTTP（超文本传输协议）的？
超文本传输协议＝超文本＋传输＋协议，协议即约定，HTTP就是约定超文本怎么传输的。初心就是分享信息，所以，简单、开放、有求有应，只针对文本，后来出现了音频、视频、动画、图片、超链接这些玩意，比纯文本复杂了一些，不过初心不改，所以，原则未变，只是需要调整一下适应这些正当其时的需求而已。
</div>2020-03-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/24/b9/b9/9e4d7aa4.jpg" width="30px"><span>乘风破浪</span> 👍（14） 💬（1）<div>关于host头和主机托管的关系，尝试自己理解了一下，请老师指正
一个主机&#47;IP地址可以运行多个网站，即虚拟主机
		www.a.com
		www.b.com
		…
它们在浏览器地址栏无论输入www.a.com或www.b.com都将解析到同一个IP地址
但不同网站的浏览器发起的访问请求，host填的URI不一样
如www.a.com请求host里填的是www.a.com, www.b.com填的www.b.com
这样就把同一个IP的不同网站（虚拟主机）区分开了</div>2021-01-25</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/cd/c1/19531313.jpg" width="30px"><span>innovationmech</span> 👍（11） 💬（1）<div>希望破冰篇和基础篇能更新快点</div>2019-05-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/27/3b/fd/2e2feec3.jpg" width="30px"><span>💍</span> 👍（8） 💬（1）<div>课后总结：
  http 0.9 ： 功能较为简单， 且传输格式只能是纯文本格式 ， 只支持get请求 ， 请求完毕立即关闭请求
  http 1.0： 1. 增加了head， post 等请求
                  2. 增加返回状态码
                  3. 引入版本号概念
                  4. 增加了http头部的概念， 提高灵活度
                  5. 传输的文本不再限制纯文本格式， 增加了音视频等格式
    http1.1： 1. 增加了put， delete请求 
                   2. 增加缓存管理
                   3. 明确链接管理， 推动持久链接 
                   4. 允许响应数据分块
                   5. 强制要求host头
   http 2.0 ： 1. 二进制协议
                    2. 支持同时发送多个请求
                    3. 压缩头部， 减少数据传输量
                    4.  允许服务端主动推送数据
                    5. 增加安全性， 增加加密通信

http不同版本特点：
    http 0.9：  版本功能单一简单， 因前期设计简单， 后期版本更新就会比较容易
    http 1.0：  功能相对0.9 更加丰富， 但并不是统一标准 只是一份文档， 不具约束力
    http 1.1 ： 相对1.0 添加了小规模更新， 但是它算是一份http统一的标准， 所有的http请求都需严格按照这个标准
   http 2.0 ： 相对1.1 提升了http请求的性能和安全性 

               </div>2022-10-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/07/8c/0d886dcc.jpg" width="30px"><span>蚂蚁内推+v</span> 👍（8） 💬（1）<div>1. HTTP 发展的原动力我认为还是人们对信息获取的需求升级，从单一的文本到静态图片，再到动态视频、音乐，更到未来的 AR&#47;VR，以及与日俱增的风险，因此对于安全性、隐私的保护，为了满足更高层级的需要，HTTP 协议本身也要与时俱进；
2. HTTP 的本质是 P（Protocol），即一个协议，定义了服务端与客户端数据交互的标准。</div>2019-06-02</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/f8/e5/7c06cd59.jpg" width="30px"><span>二楞子</span> 👍（8） 💬（4）<div>1.用户需求
2.我理解的http 类似河里的船 传输东西用的工具</div>2019-05-30</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/5f/30/4ae82e16.jpg" width="30px"><span>wordMan</span> 👍（6） 💬（1）<div>请问老师，HTTP&#47;2： “二进制协议，不再是纯文本” 这个怎么理解的，如果是指传输的话应该都是二进制啊</div>2020-04-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/5c/de/16695891.jpg" width="30px"><span>SBB</span> 👍（6） 💬（1）<div>大家都说源动力来自用户需求，但是没说清楚是什么需求。
我觉得源动力是知识共享和工作协同的需要，也是因为这个原因在研究所里有了万维网，在万维网的基础上又想要利用这个网络来分享知识、同步信息。</div>2019-11-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/7d/3c/fdab3611.jpg" width="30px"><span>灰</span> 👍（6） 💬（2）<div>HTTP 1.1 的 强制要求 Host 头，让互联网主机托管成为可能。

难道不是总是要经过DNS解析吗，如果都要经过DNS解析的话，Host的设计和主机托管有什么关系。</div>2019-05-30</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/8d/0e/5e97bbef.jpg" width="30px"><span>半橙汁</span> 👍（5） 💬（1）<div>1，原动力:
     时代思想环境的日渐成熟;
     与之匹配的相关技术的达标;
     求知欲，好奇心等因素催生出的相关技术工种人才;
     各个行业的用户对信息流通速率提升的高度关注与需求;(占比较大的因素)
2，http
    超文本传输协议，可以拆解着来理解(个人拙见):
    超(over):  更多，更快，更加便捷等等;
    文本(information): 信息，资源等等;
   传输(translate): 交互，响应;
   协议(role): 规则;

最后，附上个人的一点疑惑(希望得到各位的响应):
http0.9---http1.0---http1.1---http2.0---http3.0
对应的相关RFC编号，从无到已知的具体编号，之间有各种联系？
RFC7230对应1.1，随意定义的还是通过审核收集意见制定的？
     </div>2020-01-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/36/d2/c7357723.jpg" width="30px"><span>发条橙子 。</span> 👍（5） 💬（4）<div>突然想到一个点 ，是不是因为2.0之前数据都是以文本形式传输 ，所以才命名为 超文本传输协议 。 那后来2.0可以支持二进制形式传输了 ， 实际上HTTP这个命名也不太准确了</div>2019-05-30</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/5f/73/bb3dc468.jpg" width="30px"><span>拒绝</span> 👍（5） 💬（1）<div>开发至今，只使用到了http的get、post的请求方式，至于put、delete的方式，它们的存在肯定是有原因，至于是什么原因，应用在怎样的场景下，请老师解答下</div>2019-05-29</li><br/><li><img src="" width="30px"><span>Dang</span> 👍（4） 💬（2）<div>HTTP 1.1应该已经支持了多连接，但是每个连接都需要遵循request-response然后再req-resp的模式。
HTTP 2支持不需要等待resp就可以继续发送多个req。

这是文章中提到的HTTP 2的特点：2、可发起多个请求，废弃了 1.1 里的管道；的意思么？</div>2021-01-11</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTIjUDIRQ0gRiciax3Wo78c5rVjuWDiaw4ibcCiby8xiaMXJh5ibjU5242vfCGOK4ehibe1IKyxex2A4IX4XSA/132" width="30px"><span>追风者</span> 👍（4） 💬（1）<div>业务驱动技术发展，技术反哺成就业务。</div>2019-08-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/30/8a/b5ca7286.jpg" width="30px"><span>业余草</span> 👍（4） 💬（1）<div>老师：后面有没有一些 http 安全知识方面的内容？比如：host 头攻击、缓速攻击等。</div>2019-05-31</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/05/0b/9a877a15.jpg" width="30px"><span>恒`∞`真理</span> 👍（3） 💬（2）<div>对于哪些软件功能使用了 HTTP 协议，个人最直观感受到的场景是在内网中通过 HTTP 代理服务器连接互联网的时候。比如淘宝、京东、iCloud 等都可以正常工作，但支付宝、微信、QQ 只有部分功能可用，而大部分网络游戏则完全不使用 HTTP。
其中，QQ、支付宝这些 app 是为了安全性还是为了其他原因抛弃了 HTTP 呢？如果是前者的话，为什么京东金融等部分金融 app 也完全使用 HTTP？期待老师的解答。</div>2019-05-30</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/5d/48/03abbbd1.jpg" width="30px"><span>瑞</span> 👍（3） 💬（1）<div>http最初就是来传输超文本内容的？</div>2019-05-29</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTIuUYcwKWUuib5mpdIbTwQzTGNWBmk0ktZSwm2vteUXf4TxWF2aVCv7Hvshcq0OaG7JRLj6rJyPLicA/132" width="30px"><span>godliness</span> 👍（2） 💬（1）<div>社会发展&#47;进步：人们日益增长的物质文化需求，同落后的生产关系之间的矛盾。</div>2019-12-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/7b/57/a9b04544.jpg" width="30px"><span>QQ怪</span> 👍（2） 💬（1）<div>用户需求推动技术革命。
我理解的http就是表示传递数据是用什么格式</div>2019-05-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/b0/e1/3aeb2d2d.jpg" width="30px"><span>笑忘日月星辰</span> 👍（2） 💬（1）<div>峰哥，
我们有个web应用，需要配置它的访问ip:port, 如果在它的配置里填127.0.0.1:8080，那么用localhost:8080或者172.168.5.36:8080访问就登录不了应用,只能通过127.0.0.1:8080才能登录，反之亦然。

请问127.0.0.1与localhost、172.168.5.36三者之间有什么关系与区别？http是怎么识别它们的？</div>2019-05-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/26/eb/d7/90391376.jpg" width="30px"><span>ifelse</span> 👍（1） 💬（1）<div>有趣</div>2023-01-16</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/2c/92/95/b15fd434.jpg" width="30px"><span>香港晚安</span> 👍（1） 💬（1）<div>互联网上一切工具的原动力都是推动人与人之间的连接，后面的发展优化不过是在此基础上的缝缝补补</div>2022-02-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/e8/55/63189817.jpg" width="30px"><span>MClink</span> 👍（1） 💬（1）<div>一门技术的升级和迭代，必然是不满足当前需求而被迫升级</div>2020-03-17</li><br/><li><img src="" width="30px"><span>Geek_ab7818</span> 👍（1） 💬（1）<div>你认为推动 HTTP 发展的原动力是什么？ 
答：互联网的发展越来越厉害，人们上网获得的知识推动http协议的发展。

你是怎么理解 HTTP（超文本传输协议）的？
答：定义了一套规则，约束服务器和客户端还有网站必须按照此规则约束。大家都按照统一规则来发展。</div>2019-09-04</li><br/>
</ul>