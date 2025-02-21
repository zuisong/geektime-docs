上一讲我介绍了HTTP的五个基本特点，这一讲要说的则是它的优点和缺点。其实这些也应该算是HTTP的特点，但这一讲会更侧重于评价它们的优劣和好坏。

上一讲我也留了两道课下作业，不知道你有没有认真思考过，今天可以一起来看看你的答案与我的观点想法是否相符，共同探讨。

不过在正式开讲之前我还要提醒你一下，今天的讨论范围仅限于HTTP/1.1，所说的优点和缺点也仅针对HTTP/1.1。实际上，专栏后续要讲的HTTPS和HTTP/2都是对HTTP/1.1优点的发挥和缺点的完善。

## 简单、灵活、易于扩展

首先，HTTP最重要也是最突出的优点是“**简单、灵活、易于扩展**”。

初次接触HTTP的人都会认为，HTTP协议是很“**简单**”的，基本的报文格式就是“header+body”，头部信息也是简单的文本格式，用的也都是常见的英文单词，即使不去看RFC文档，只靠猜也能猜出个“八九不离十”。

可不要小看了“简单”这个优点，它不仅降低了学习和使用的门槛，能够让更多的人研究和开发HTTP应用，而且我在[第1讲](https://time.geekbang.org/column/article/97837)时就说过，“简单”蕴含了进化和扩展的可能性，所谓“少即是多”，“把简单的系统变复杂”，要比“把复杂的系统变简单”容易得多**。**

所以，在“简单”这个最基本的设计理念之下，HTTP协议又多出了“**灵活和易于扩展**”的优点。
<div><strong>精选留言（30）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/11/fe/4c/46eb517a.jpg" width="30px"><span>Xiao</span> 👍（48） 💬（1）<div>老师说的对，以前的时候觉得看书或者文章，人家说什么就是什么，而且很绝对。后来慢慢发现，很多东西都是需要结合业务场景来分析的，在这种业务场景是优点，在另外的业务场景就可能是致命的缺点！那句话：脱离业务场景谈技术就是耍流氓！哈哈哈，谢谢老师！</div>2019-06-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/67/f4/9a1feb59.jpg" width="30px"><span>钱</span> 👍（15） 💬（2）<div>1：你最喜欢的 HTTP 优点是哪个？最不喜欢的缺点又是哪个？为什么？
最喜欢她的简单，因为简单所以美好，简简单单容易上手，易于理解。
最不喜欢她的不安全和低性能，如果她能做到安全高效，那就不用再去学习别的乱七八糟的协议了，编写RPC接口也就没有其他框架什么事情了，搞微服务应该门槛更低效率更高，当然，她目前做不到，由于考上层以后估计也悬，不过如果基建OK，也许网络带宽不再是瓶颈，她能做到天然的高效传输吧！

2：你能够再进一步扩展或补充论述今天提到这些优点或缺点吗？
简单和易扩展，我认为是矛盾的，很少系统能做到即易扩展又简单，毕竟以后需要什么谁也不能未卜先知，留下扩展的余地毕竟会增加复杂度吧！如果设计的不好，复杂度也许会急剧上升，不过HTTP做的很好貌似没有出现这种情况。不知是为什么？是公共的预定义基本OK吗？其实扩展的不是很多吗？还请老师分享一下。

3：你能试着针对这些缺点提出一些自己的解决方案吗？
有无状态已有方案，可以自由选择
安全性后面也会采用加密的方式来解决
低效这个是相对的，靠上必然会低效，如果基建进一步加强，也许能进一步解决，不过这个看需求和增加的带宽那个更大吧！
明文最早的初心就是分享信息，明文我觉得太正常了，现在多了安全性的需求，所以，才渴望更安全的，此时的HTTP用于分享信息已是一部分功能，她还可以实现各种各样的诉求。
如果协议里设置的有类似开关的东西就好了，可以选择是否有状态、可以选择是否明文、可以选择是否加密，使用者仅需要控制开关就能实现相关的功能，不需自己实现，那就更好了。</div>2020-03-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/9d/5d/3fdead91.jpg" width="30px"><span>レイン小雨</span> 👍（13） 💬（5）<div>老师，我想问一下关于“队头阻塞”的概念，正好上周团队有人分享这方面的知识，当时是说浏览器针对一个域名最多同时建立6个连接通道，也就是支持6个http并发，当一个页面中有100个资源文件需要加载的时候，就只能6个6个的串行加载，第七个请求要等到第一个请求结果返回来之后才能发出。这么理解队头阻塞的概念对吗？</div>2019-06-29</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/DYAIOgq83eoTQdEVIg38BZJzTskicylttPwoiaWNwFxE8QXibrze3no9HiaGNvUibTou9zY1HMq2HrEQ1PZfDUFicBBw/132" width="30px"><span>Geek_d59aa7</span> 👍（9） 💬（2）<div>老师，问个沙雕问题，什么叫明文传输，难道http里的信息不是转成二进制传输的吗，看网上的意思好像明文传输是直接传输字母和数字？？不是二进制？</div>2020-07-02</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/30/8a/b5ca7286.jpg" width="30px"><span>业余草</span> 👍（9） 💬（3）<div>老师不仅技术好，文章写的也很好。比较喜欢看这种风格的文章，可以加个微信好友吗？我微信：xttblog</div>2019-06-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/76/a7/374e86a7.jpg" width="30px"><span>欢乐的小马驹</span> 👍（6） 💬（1）<div>老师好，小贴士里面提到了：绝大多数的网站都封禁了80&#47;8080以外的端口号，只允许HTTP进行穿透。
1、最初为什么要封禁其他端口只留80&#47;8080呢？ 2、穿透是什么意思？</div>2020-03-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/08/35/3367b66b.jpg" width="30px"><span>我的朋友叫垃圾呆</span> 👍（5） 💬（2）<div>老师，我查了资料之后还是不太理解 文本协议和二进制协议，我看之前的文章有说，从http2 开始，变成了二进制协议，这篇文章说 tcp是二进制协议，而http是文本协议，不太能理解两者的区别，在传输信息的时候不都是转换成二进制的字节流进行传输的吗</div>2021-01-03</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/79/4b/740f91ca.jpg" width="30px"><span>-W.LI-</span> 👍（4） 💬（3）<div>老师好!传输的时候序列化方式属于HTTP范畴么?现在大多用的json形式可是cloud和dubbo在高并发情况下dubbo性能比cloud好。网上说是序列化方式不一样。也不晓得是不是</div>2019-06-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/17/dc/97/4930a9f0.jpg" width="30px"><span>小丽</span> 👍（3） 💬（1）<div>老师讲的非常透彻，有些话看似简单，却值得琢磨，希望老师多讲一点关于身份认证和安全的东西</div>2019-07-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/fe/4c/46eb517a.jpg" width="30px"><span>Xiao</span> 👍（3） 💬（1）<div>不觉得明文是缺点，因为http本身就是一套标准规范，而且前面也说它是非常灵活的，所以个人觉得明文也是一种场景，用户也可以选择密文传输！</div>2019-06-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1e/44/c0/cd2cd082.jpg" width="30px"><span>BoyiKia</span> 👍（2） 💬（1）<div>老师，我想问下。你刚刚说的明文传输具体指headr,但是  body也是明文吗？</div>2020-04-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/19/51/29/24739c58.jpg" width="30px"><span>凉人。</span> 👍（2） 💬（1）<div>大概最喜欢应用广泛的特点。这点太适用了。</div>2020-03-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/08/17/e63e50f3.jpg" width="30px"><span>彩色的沙漠</span> 👍（2） 💬（1）<div>虽然使用了HTTPS金融领域还是需要对数据加密和完整性检验，加密对body数据好加密对于header部分不好加密，需要对KV一个一个加密有点麻烦，不过在传输的时候一般把字段都用body传输，header里面不使用自定义字段。</div>2019-06-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1e/01/c5/b48d25da.jpg" width="30px"><span>cake</span> 👍（1） 💬（1）<div>“无状态”服务器是不知道这些请求是相互关联的，每次都得问一遍身份信息，不仅麻烦，而且还增加了不必要的数据传输量 老师请问下，&quot;每次都得问一遍身份信息&quot; 这个在没有cookie时是怎么实现的呢</div>2021-11-01</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/67/2c/ee3c2d36.jpg" width="30px"><span>飞翔的葱油饼</span> 👍（1） 💬（3）<div>有个问题啊。老师在上节课中有提到HTTP有可靠传输的特点，这是由于HTTP基于TCP协议，而TCP提供了可靠传输，而这节中提到HTTP的灵活性，其下层使用的传输层协议是可以变的，甚至可以使用UDP，那这样的情况下，HTTP是否就不具有可靠传输性了呢？</div>2021-04-06</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/23/6c/785d9cd3.jpg" width="30px"><span>Snooker</span> 👍（1） 💬（1）<div>HTTP. 身份认证，可以通过加入通信双方约定的密钥做摘要算法，完成身份认证。</div>2021-03-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/01/01/8890d0d1.jpg" width="30px"><span>i</span> 👍（1） 💬（1）<div>

这里有一点小疑问 就是头字段的灵活性 可以任意的添加字段 为什么不用get put方式传递呢 非要写在头里面呢 什么时候必须在header里面加自己的字段 https会对body 和header都加密 感觉也可以不用添加头字段 直接put传递就好了 安全性没什么区别。还是没有所谓的硬性要求 全靠个人爱好 </div>2019-09-02</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/23/6c/785d9cd3.jpg" width="30px"><span>Snooker</span> 👍（0） 💬（1）<div>1.最喜欢的优点：简单易学，容易上手；最不喜欢的，业务侧的可能更关注安全，技术侧的可能更关注性能，比如队头阻塞和头信息压缩不完全
2.-
3.安全方面，已有解决方案 加入一层 tls&#47;ssl ；性能方面：头阻塞，多加队列；头压缩，客户端和服务端约定新的解压缩格式，http后续版本也有相关解决方案</div>2024-04-16</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/68/1d/682eaee0.jpg" width="30px"><span>Map</span> 👍（0） 💬（1）<div>问个问题HTTP2解决了应用层的队头阻塞问题，实现了单个链接上的多路复用，那么用了HTTP2，客户端还会并发多个TCP链接吗，比如在HTTP1.1浏览器通常会并发6个TCP链接。</div>2024-03-19</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/8SdpYbicwXVXt0fIN7L0f2TSGIScQIhWXT7vTze9GHBsjTvDyyQW9KEPsKBpRNs4anV61oF59BZqHf586b3o4ibw/132" width="30px"><span>Leolee</span> 👍（0） 💬（1）<div>作业：
1、我最喜欢HTTP的应用广泛，学会了就可以受用很久；我不喜欢HTTP的不安全，因为不安全已经是致命的缺陷了，不然也不会出现HTTPS和HTTP2了；
2、PASS（python的pass，留待以后再写）；
3、PASS（python的pass，留待以后再写）。

HTTP优点：
简单、灵活、易于扩展，应用广泛、软硬件环境成熟、无状态
HTTP缺点：
明文传输、不安全、性能不算差但也不够好
HTTP优缺点并存：
明文传输、无状态

简单、灵活、可扩展
HTTP协议很简单，报文格式就是header+body，头部信息也是简单的文本格式，用的也是常见的英文单词。学习使用的门槛很低。正是基于简单这个最基本的设计理念，才有了HTTP最锋利的剑：灵活可扩展！简单相当于一张白纸，你想怎么写都行。
HTTP里的请求方法、URI、状态码、原因短语、头字段等每一个核心组件都没有被写死，允许任意定制、扩充和解释，缺什么功能自己写就可以了。
HTTP不限制具体的下层协议，下层协议可以随意变化，上层的语义却可以始终保持稳定。

应用广泛、软硬件环境成熟
HTTP已经遍布互联网世界，很能找到一个没有使用HTTP的地方。无论应用领域还是开发领域都得到了广泛支持。HTTP天然具有跨语言、跨平台的特性，几乎所有编程语言都有HTTP调用库和外围的开发测试工具。
很多互联网和传统行业公司都购买服务器开办网站、建设数据中心、CDN和高速光纤，持续优化上网体验。

无状态
无状态令服务器不需要额外的资源来记录状态信息，负担轻一些。
无状态令服务器没有状态的差异，很容易组成集群，让负载均衡把请求转发到任意一台服务器，不会因为昨天不一致导致处理出错，直接买多几台服务器就可以轻松实现高并发高可用。
无状态的缺点就是没有记忆能力，也就无法支持需要连续多个步骤的事务操作，每一次都要问一次身份信息，不仅麻烦，也增加了不必要的数据传输量。但这个问题可以通过Cookies解决。

明文
是优点也是缺点；
明文的意思就是协议里的报文header部分，不使用二进制数据，而使用简单可阅读的文本形式。优点就是不需要借助任何外部工具，抓包后直接就可以查看或者修改，开发调试起来很便利。
缺点就是毫无隐私可言，只需要侵入了这个链路里的某个设备，简单地旁路一下浏览，就可以实现对通信的窥视。

不安全
HTTP没有提供有效的手段来确认通信双方的真实身份，虽然有基本的认证机制，但在明文传输面前几乎等同无效。
HTTP也不支持完整性校验，数据在传输过程中很容易被篡改而无法验证真伪。
正是因为这个缺陷，所以出现了HTTPS。

性能
不算差、不够好
因为请求-应答模式决定了按顺序发送的请求序列中有一个请求因为某种原因被阻塞时，后面一长串的请求也会被阻塞，会导致客户端迟迟收不到数据。

其他
出于安全原因，绝大多数网站都封禁了80&#47;8080意外的端口号，只允许HTTP进行穿透，这也是导致HTTP流行的客观原因之一。80&#47;8080是HTTP端口。</div>2021-04-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/26/ba/a9/7432b796.jpg" width="30px"><span>coral</span> 👍（0） 💬（1）<div>1. 你最喜欢的 HTTP 优点是哪个？最不喜欢的缺点又是哪个？为什么？
最喜欢明文的传输，一目了然，上手几乎没有门槛，拿来就能用。最不喜欢的是明文可能会被截获带来安全性的问题。当然现在已经有了https（还没有搞清楚它是怎么加密的）很好奇为什么在一开始http设计的时候没有把这个考虑进去。是因为早期的互联网，比较着重在公开的信息，没有这么多隐私的需求吗？

2. 你能够再进一步扩展或补充论述今天提到这些优点或缺点吗？
通讯方式必须一来一回，且需要由客户端发起。服务器无法主动发送信息。这个特点减小了服务器的工作量，但增加了状态变化的监听、即时推送的难度。（但这个需求已经随着网络带宽的增加越来越普遍了）

3. 你能试着针对这些缺点提出一些自己的解决方案吗？
监听的问题，有没有办法增加一条监听通道，认证过身份的客户端就可以接收服务器推送，这个认证需要定时刷新确保客户端alive</div>2021-04-06</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/18/8f/ec/c30b45d4.jpg" width="30px"><span>Geek_Maggie</span> 👍（0） 💬（1）<div>自己看书总觉得像是学会了但是浮于表面。听了老师课程，结合实际去理解，感觉加深了不少印象</div>2021-03-15</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/25/8c/80/7310baac.jpg" width="30px"><span>刘杰</span> 👍（0） 💬（1）<div>1、我最喜欢HTTP简单、灵活易于扩展的优点，易于扩展就意味着有无限的可能。最不喜欢不安全的缺点，不安全意味着无法知道真实身份是我想要连接的，容易被有心人利用
2、HTTP的另外一个优点应用广泛，可以使我们轻易的将开发的应用部署在服务器上，让大家可以轻易访问
3、关于不安全的，可以使用HTTPS。关于明文问题，可以考虑客户端和服务端自定义一套自己能看懂的编码。</div>2021-03-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1b/96/47/93838ff7.jpg" width="30px"><span>青鸟飞鱼</span> 👍（0） 💬（1）<div>老师，HTTP1.1和HTTP2分别适合什么场景呢？不可能1.1跟2相比，一点优点都没有吧</div>2021-02-16</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/18/65/35361f02.jpg" width="30px"><span>潇潇雨歇</span> 👍（0） 💬（1）<div>1、最喜欢http简单，灵活的特点，最不喜欢不安全
</div>2020-06-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/19/e4/4f/df6d810d.jpg" width="30px"><span>Maske</span> 👍（0） 💬（1）<div>1.最喜欢的优点：简单灵活易于扩展，这样对于应用层开发人员来说只需重点关心当前请求相关信息，无需过多的关心底层传输机制，且易于扩展的特性使得在实际场景中更方便解决遇到问题。最不喜欢的缺点：协议本身缺乏完整的安全性校验，可能导致CSRF。
2.可能也不算缺点吧，仅为个人理解，对于那些冷门的几乎不怎么用到的请求方法比如delete,put,options, connect等,这些应该属于历史遗留产物,最好在协议中剔除，质量越高的东西应该越简洁</div>2020-06-11</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/6LaITPQ4Lk5fZn8ib1tfsPW8vI9icTuSwAddiajVfibPDiaDvMU2br6ZT7K0LWCKibSQuicT7sIEVmY4K7ibXY0T7UQEiag/132" width="30px"><span>尔东橙</span> 👍（0） 💬（1）<div>像浏览器-服务器这种，应用层是http协议，那IM消息系统这种CS架构，应用层是什么协议呢，总感觉不是http协议，是自定义的么</div>2020-02-16</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1a/26/7e/823c083e.jpg" width="30px"><span>Wr</span> 👍（0） 💬（1）<div>作为一个测试，只有将特性融合到某个测试场景，问题处理中才印象深刻。。至于解决方案，希望未来可以达到的深度。</div>2020-01-04</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTL7h9x6VXY9DmPnRWVKELfbfeJ9e9ricn12ia5icXB8u1cBhjlSE74lHiaYFAatosmjAxCdNIsyV23ByQ/132" width="30px"><span>Geek_ualcx9</span> 👍（0） 💬（1）<div>1、最喜欢的优点当然是简单可扩展；最不喜欢的是不安全，性能也一般。原因的话，自然是简单可扩展让我们更多的关注业务，但不安全，性能一般使得我们不得不更多的了解底层。这也是程序员的使命吧，哈哈。
2、HTTP支持缓存；HTTP目前还是请求-应答为主。
3、难，还是先学好底层思想。</div>2019-09-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/30/e8/6898e576.jpg" width="30px"><span>季末灬离殇</span> 👍（0） 💬（2）<div>1、最喜欢的优点是灵活、可扩展，感觉这个是 HTTP 纵横江湖几十年而屹立不倒的根基，能够随时拥抱变化，解决与时俱进中产生的问题。
最不喜欢的缺点是不安全，在这个物欲纵横，互联网高速发展的时代，很容易被窃取信息，数据劫持，数据篡改，中间人攻击等，因此诞生了基于 TLS&#47;SSL 的 HTTPS。
2、最近在做客户端网络优化，感触比较深的就是基于“请求 - 问答”模式，C&#47;S每一次的交互都需要经历握手建立连接，比较耗时，但是感觉keep-alive也只是假的长连接，不知道有没有终极处理方案。
3、关于队头阻塞在网上找了下资料
1&gt; 数据分帧：多个请求复用一个TCP连接，然后每个request-response都被拆分为若干个frame发送，这样即使一个请求被阻塞了，也不会影响其他请求
2&gt; 修改底层协议，也即是QUIC诞生的原因，使 HTTP 协议基于 UDP 实现
老师能帮忙解析下问题3吗？</div>2019-08-10</li><br/>
</ul>