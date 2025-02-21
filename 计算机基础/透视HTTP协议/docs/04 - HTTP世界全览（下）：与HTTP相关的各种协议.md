在上一讲中，我介绍了与HTTP相关的浏览器、服务器、CDN、网络爬虫等应用技术。

今天要讲的则是比较偏向于理论的各种HTTP相关协议，重点是TCP/IP、DNS、URI、HTTPS等，希望能够帮你理清楚它们与HTTP的关系。

同样的，我还是画了一张详细的思维导图，你可以点击后仔细查看。

![](https://static001.geekbang.org/resource/image/1e/81/1e7533f765d2ede0abfab73cf6b57781.png?wh=1863%2A2271)

## TCP/IP

TCP/IP协议是目前网络世界“事实上”的标准通信协议，即使你没有用过也一定听说过，因为它太著名了。

TCP/IP协议实际上是一系列网络通信协议的统称，其中最核心的两个协议是**TCP**和**IP**，其他的还有UDP、ICMP、ARP等等，共同构成了一个复杂但有层次的协议栈。

这个协议栈有四层，最上层是“应用层”，最下层是“链接层”，TCP和IP则在中间：**TCP属于“传输层”，IP属于“网际层”**。协议的层级关系模型非常重要，我会在下一讲中再专门讲解，这里先暂时放一放。

**IP协议**是“**I**nternet **P**rotocol”的缩写，主要目的是解决寻址和路由问题，以及如何在两点间传送数据包。IP协议使用“**IP地址**”的概念来定位互联网上的每一台计算机。可以对比一下现实中的电话系统，你拿着的手机相当于互联网上的计算机，而要打电话就必须接入电话网，由通信公司给你分配一个号码，这个号码就相当于IP地址。
<div><strong>精选留言（30）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/10/ab/e1/079ee6e3.jpg" width="30px"><span>壹笙☞漂泊</span> 👍（175） 💬（1）<div>课后题：
1、URI DNS
DNS 是将域名解析出真实IP地址的系统
URI 是统一资源标识符，标定了客户端需要访问的资源所处的位置，如果URI中的主机名使用域名，则需要使用DNS来讲域名解析为IP。
2、打电话给小明，请小明找小王拿一下客户资料。小明处于代理角色。
内容笔记
1、四层模型：应用层、传输层、网际层、链接层
2、IP协议主要解决寻址和路由问题
3、ipv4，地址是四个用“.”分隔的数字，总数有2^32个，大约42亿个可以分配的地址
4、ipv6，地址是八个用“:”分隔的数字，总数有2^128个。
5、TCP协议位于IP协议之上，基于IP协议提供可靠的(数据不丢失)、字节流(数据完整)形式的通信，是HTTP协议得以实现的基础
6、域名系统：为了更好的标记不同国家或组织的主机，域名被设计成了一个有层次的结构
7、域名用“.”分隔成多个单词，级别从左到右逐级升高。
8、域名解析：将域名做一个转换，映射到它的真实IP
9、URI：统一资源标识符；URL：统一资源定位符
10、URI主要有三个基本部分构成：协议名、主机名、路径
11、HTTPS：运行在SSL&#47;TLS协议上的HTTP
12 、SSL&#47;TLS：建立在TCP&#47;IP之上的负责加密通信的安全协议，是可靠的传输协议，可以被用作HTTP的下层
13、代理(Proxy)：是HTTP协议中请求方和应答方中间的一个环节。既可以转发客户端的请求，也可以转发服务器的应答。
14、代理常见种类：匿名台历、透明代理、正向代理、反向代理
15、代理可以做的事：负载均衡、内容缓存、安全防护、数据处理。</div>2019-06-05</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/67/f4/9a1feb59.jpg" width="30px"><span>钱</span> 👍（71） 💬（4）<div>1：DNS 与 URI 有什么关系？
       DNS专门用于域名解析，作用是简化人类记忆数据的复杂度。
        URI专门用于标识互联网世界中的资源，作用是帮助找到对应的互联网中资源。
         互联网中的电脑通过IP地址来表示，DNS可以把一个域名变成一个IP地址，IP地址是标识资源的一部分，仅定位了具体的电脑，还有继续定位在电脑上的具体位置。

2：在讲代理时我特意没有举例说明，你能够用引入一个“小强”的角色，通过打电话来比喻一下吗？
小强给小明打电话要小红的照片——小明是正向代理
小强要小红的照片小明负责处理——小明是反向代理

网络通信是分布式系统的底座，也是信息交互的法宝
TCP——负责数据传输
IP——负责标识传输对象
DNS——负责简化人类的记忆
URI&#47;L——负责标识传输的资源
SSL——负责数据传输的安全
Proxy——负责信息的中转
像极了走标，
需要搞清楚从哪到哪——IP
需要搞定怎么传输——TCP
需要保障货物的安全——SSL
需要送货的具体位置——URI
需要把目的地的经纬度换成地址名——DNS
需要中间中转一下——Proxy
HTTP——我不那么多，我向你要什么你就给什么</div>2020-03-24</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTIjTlXUOibjFdIicwDas890lM4Jrsdag4c0t0XLBtopQRvwG8Vj4agbtpPkKGNPH96bDWyibmMiceEibaA/132" width="30px"><span>Atomic</span> 👍（41） 💬（8）<div>打个比方：我让老婆帮我去楼下超市买瓶水，DNS可以帮她找到楼下超市，URI可以帮她找到水放在超市的具体位置</div>2019-06-06</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/5d/e2/3331ad9e.jpg" width="30px"><span>Shine Sunner</span> 👍（24） 💬（1）<div>1.假如去某个小区找人，DNS可以帮我定位到是哪栋大楼，URI可以帮我定位到是哪个房间。
2.
正向代理:
   假如我【客户端】想找小强【服务端】借钱，但是我不好意思。我去找小李【代理】，然后让小李找小强借。对于小强来说他以为是小李找他借钱，而不是我。
   
反向代理:
  同样是借钱，这回我【客户端】找小李【代理】借钱，小李没钱了，他去找小强【服务端】借钱，然后再把钱借给我，对我来说我认为是小李借钱给我，而不是小强。

  总结:
   正向代理的代理服务器是部署在客户端，而对服务端来说，它以为对它发起请求的是代理服务器，而真正请求的客户端对服务端来说是不可见的。
   反向代理的代理服务器是部署在服务端，而对客户端来说，它以为对它做出响应的是代理服务器，而真正响应的服务端对客户端来说是不可见的。</div>2020-01-01</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/27/d5/0fd21753.jpg" width="30px"><span>一粟</span> 👍（19） 💬（3）<div>小强家钥匙丢了，需要找一家开锁公司开门。于是小强打电话给114，114给小强提供一家有资质的开锁公司，并将电话转接过去。这里的114就是代理。</div>2019-06-05</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/07/8c/0d886dcc.jpg" width="30px"><span>蚂蚁内推+v</span> 👍（13） 💬（3）<div>1. URL 包含了协议+主机名+路径，DNS 会将其中的主机名解析为 IP，进而方便根据 IP 协议进行寻址、路由；
2. 我们为了更安全的和小明交流，选择通过和小强交流，让其再告诉小明，这是匿名代理，也是正向代理，而如果让小明知道我们的存在则不是匿名代理，是透明代理；小明由于某些原因不能直接响应我们，找了小强来代为响应我们，这是反向代理；
3. 另外回答一下楼下同学关于 URI 和 URL 区别的疑惑，URI 是 Identifier，即标识符，URL 是 Location，即定位，所以定位只是标识符的一种，打个比方，我们找到小明可以通过其家庭地址（Location）也可以通过名字（比如上课点名）来找到他，所以后者也可以成为 URN。因此 URL 和 URN 都是 URI 的子集。</div>2019-06-06</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/52/56/5abb4d94.jpg" width="30px"><span>不知道该叫什么</span> 👍（9） 💬（3）<div>但是我还是没明白URI跟RUL的区别</div>2019-10-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/57/4f/6fb51ff1.jpg" width="30px"><span>奕</span> 👍（7） 💬（2）<div>Http协议不是依赖tcp&#47;ip的拆包和封包吗？Unix domain socket可以做到吗？</div>2019-06-05</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/27/d3/0a/92640aae.jpg" width="30px"><span>我爱夜来香</span> 👍（5） 💬（3）<div>老师，我有个问题，就是URL由三部分组成，前面的协议名和主机名能理解,后面的路径指的是应用在服务器上的真实路径吗？或者说是由真实路径经过一层封装而形成的?</div>2021-05-02</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/57/4f/6fb51ff1.jpg" width="30px"><span>奕</span> 👍（4） 💬（1）<div>看到老师后面小帖士说的，在unix系统上http可以依赖一种进程间传输的机制Unix domain socket进行传输，这是因为满足了底层的可靠的传输。这句话意思是说，http不一定在tcp&#47;ip之上进行传输？只要底层满足可靠传输的都可以？

</div>2019-06-05</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/cd/94/0d44361e.jpg" width="30px"><span>Jerryz</span> 👍（3） 💬（1）<div>1. DNS 可以定位到一台主机，URI 则可以定位到主机上的资源。
2. 正向代理：我通过查找小强的电话薄，转话到小明。反向代理：我通过查找小明的电话薄，但是和我通话的实际是小强。</div>2021-01-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/17/07/97/980d36e2.jpg" width="30px"><span>Tio Kang</span> 👍（3） 💬（1）<div>老师，我有一个疑问，一个代理即可以是反向代理也可以正向代理吗？</div>2019-09-02</li><br/><li><img src="" width="30px"><span>dingdongfm</span> 👍（3） 💬（1）<div>不做本地证书校验时，https可以被抓包工具抓到明文包，原因是什么？https不能防止中间人攻击么</div>2019-06-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/b0/b0/30b29949.jpg" width="30px"><span>愚人</span> 👍（3） 💬（1）<div>域名可以对应多个IP，IP也可以通过端口映射对应多个域名。能讲一讲这方面实例么？</div>2019-06-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/cb/9d/2bc85843.jpg" width="30px"><span>　　　　　　　鸟人</span> 👍（3） 💬（1）<div>a要向b发送消息，实际是先发到代理，由代理发给b。反向由b返回给代理，代理返回给a。
那么我向cdn发送评论  此时为正向，然后刷新页面  看到自己写的评论  此时为反向 
可以这样理解么？</div>2019-06-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/36/d2/c7357723.jpg" width="30px"><span>发条橙子 。</span> 👍（3） 💬（1）<div>老师，我这里有个疑问 。 一个请求由DNS解析到指定的IP ，然后通过URI确定要访问哪些资源。最后通过 TCP&#47;IP 进行路由寻址以及数据的传输。
但是一台机子上有多个应用 ， 可能两个相同的应用运行在同一个主机上 ，有着两个不同的进程。 那么根据URI是指定从哪个进程里获取数据呢 。 
这时候是不是根据端口号来判定 ， 但是URI上并没有显式的让我们看出是哪个端口号 ？？</div>2019-06-09</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/gPNQV6n5ibib3qaWEuiaUY77TpxM4dkvr44PA3xJHc14AZbdl0kvRQhmpwpaQ4I0qZobtZlYbY5ZXuVrGfWyuk3JQ/132" width="30px"><span>小伙儿爱裸睡</span> 👍（3） 💬（1）<div>老师，TCP协议作用中的数据不丢失和数据完整有什么区别呢？可能我刚入门，有点抠字眼，还望老师不吝赐教哈。</div>2019-06-07</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/a3/f1/4af11863.jpg" width="30px"><span>herseus</span> 👍（3） 💬（1）<div>负载均衡应该算作反向代理，因为是为服务器端服务的。另外，字节流应该是数据传输格式，不是</div>2019-06-07</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/6LaITPQ4Lk5fZn8ib1tfsPW8vI9icTuSwAddiajVfibPDiaDvMU2br6ZT7K0LWCKibSQuicT7sIEVmY4K7ibXY0T7UQEiag/132" width="30px"><span>尔东橙</span> 👍（3） 💬（1）<div>老师会后面会展开来讲么，比如域名解析过程，CDN调度过程等。现在面试官都问的太深了，如果只了解表面的概念很难以应对。希望老师能挖深一点</div>2019-06-07</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/79/4b/740f91ca.jpg" width="30px"><span>-W.LI-</span> 👍（3） 💬（1）<div>URI为了方便拥有记忆可以采用域名代替IP。
当用户使用域名访问时，就需要DNS技术找到对应的IP地址。然后找到对应的服务器或者代理。DNS域名解析发生在客户端。服务端接受到的还是用户输入的域名，或者IP。服务器(代理)可开启限制，只采用域名访问。
小刚替小明找小张，小刚就是正向代理。
小刚说我就是小张(私下问小张)。反向代理</div>2019-06-05</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/8f/9d/abb7bfe3.jpg" width="30px"><span>Carson</span> 👍（3） 💬（1）<div>Dns负责解析uri中主机名为ip地址，这样才能使用ip协议来完成通信

在早起电话时代，小强给朋友打电话，要先拨通总机，让总机转接，总机就是代理。</div>2019-06-05</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/f3/2d/4b7f12b6.jpg" width="30px"><span>死后的天空</span> 👍（3） 💬（1）<div>我印象中https的加密，只是对报文头进行加密，在三成和四层之间，如果消息被篡改，将会改变头信息，这样报文到对端的时候会被丢弃，这样的效果就是实现了，文件传输不被篡改，但是还是会被截获。如果记忆没错的话，“火星文”这个比喻，会不会有一点歧义，让不知道同学理解为，https将消息本身也加密了</div>2019-06-05</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/0e/d9/e61ce097.jpg" width="30px"><span>郭纯</span> 👍（3） 💬（1）<div>DNS域名解析 是为了将域名解析成IP地址.IP地址为了标记服务器在万维网的位置.
URI 是为了标记网络资源在服务器的位置.

代理：比如小明喜欢校花但是不好意思去表达. 小明就打电话给好朋友小刚委托他给校花打电话传输自己的心意. 小刚就充当了代理的角色.</div>2019-06-05</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/20/37/b2/4dd0add9.jpg" width="30px"><span>九涯</span> 👍（2） 💬（1）<div>正向代理：其实可以叫做【请求代理】
反向代理：其实可以叫做【响应代理】</div>2022-09-02</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/8SdpYbicwXVXt0fIN7L0f2TSGIScQIhWXT7vTze9GHBsjTvDyyQW9KEPsKBpRNs4anV61oF59BZqHf586b3o4ibw/132" width="30px"><span>Leolee</span> 👍（2） 💬（1）<div>URI中的主机使用域名，就需要DNS来将域名解析成IP地址。
我让小红电话给小明，通知他将文案快递过来。小红就是我的代理。
协议栈分四层 从低到高：链接层、网际层（IP层）、传输层（TCP层）、应用层（HTTP层）。
TCP&#47;IP协议 网络世界最常用的协议，HTTP通常运行在TCP&#47;IP提供的可靠传输基础上。
IP（Internet Protocol 互联网协议）主要是解决寻址和路有问题，以及如何在两点间传送数据包。IP协议使用&quot;IP地址&quot;的概念来定位互联网上的每一台计算机。可以类比为现实中的电话系统，手机相当于计算机，电话号码就相当于IP地址。
TCP（Transmission Control Protocol 传输控制协议）它位于IP协议之上，给予IP协议提供可靠的、字节流形式的通信，是HTTP协议得以实现的基础。
“可靠”是指保证数据不丢失，“字节流”是指保证数据完整，所以在TCP协议的两端可以入到操作文件一样访问传输的数据，就像是读写在一个密闭的管道里“流动”的字节。

DNS（Domain Name System 域名系统）  是将域名解析出真实IP地址的系统
在DNS中，域名（Domain Name）又称为主机名（Host），为了更好地标记不同国家或组织的主机，让名字更好记，所以被设计成了一个有层次的结构。
要使用TCP&#47;IP协议来通信仍然要使用IP地址，所以需要把域名做一个转换，“映射”到它的真实IP地址，这就是所谓的“域名解析”。
举个例子：你想要打电话给小明，但不记得电话号码，就得在通讯录找到“小明“，然后才能查到号码，”小明“就相当于域名，电话号码相当于IP地址，在通讯录查找的过程就相当于域名解析。
HTTP协议中并没有明确要求必须使用DNS，但实际上为了方便访问互联网的WEB服务器，通常都会使用DNS来定位或标记主机名，间接地把DNS与HTTP绑在了一起。

URI&#47;URL  URI是用来标记互联网上资源的一个名字，由“协议名+主机名+路径构成”，俗称URL。
URI（Uniform Resource Identifier 统一资源标识符）有了TCP&#47;IP和DNS，只能让浏览器找到主机；主机上那么多文本、图片、超链接，就需要用到URI了。使用它就能够唯一地标记互联网上的资源。
URL（Uniform Resource Locator 统一资源定位符）也即俗称的”网址“，它实际上是URI的一个子集，不过两者几乎是相同的，差异不大，所以通常不会做严格的区分。URL相对URI来讲更加常见。
举例：你通过通讯录电联了小明，让他把昨天做好的宣传文案快递过来。这个过程里面你就完成了一次URI资源访问，”小明“就是”主机名“，”宣传文案“就是”路径”，而“快递”就是你要访问这个资源的“协议名”。

HTTPS （HTTP over SSL&#47;TLS）也即运行在SSL&#47;TLS协议上的HTTP。相当于“HTTP+SSL&#47;TLS+TCP&#47;IP”，即未HTTP套上一个安全的外壳。
SSL&#47;TLS
SSL（Secure Socket Layer 安全套接字协议）它是由网景公司发明，当发展到3.0时被标准化，改名为TLS（Transport Layer Security 安全传输层协议），但由于历史的原因还是有很多人称之为SSL&#47;TLS，或者直接简称为SSL。
SSL使用了许多密码学最先进的研究成果，综合了对称加密，非对称加密，摘要算法，数字签名，数字证书等技术，能够在不安全的环境中为通信的双方创建出一个秘密的，安全的传输通道，为HTTP套上一副坚固的盔甲。

代理（Proxy）它是HTTP协议中请求方和应答方中间的一个环节，作为“中转站”，即可以转发客户端的请求，也可以转发服务器的应答。
代理有很多的种类，常见的有：
1.匿名代理：完全“隐匿”了被代理的机器，外界看到的只是代理服务器；
2.透明代理：顾名思义，它在传输过程中是“透明开放”的，外界既知道带了，也知道客户端；
3.正向代理：靠近客户端，代表客户端向服务器发送请求；
4.反向代理：靠近服务器端，代替服务器响应客户端的请求；
5.CDN，实际上也是一种代理，它代替源站服务器响应客户端的请求，通常扮演者透明代理和反向代理的角色。
由于代理在传输过程中插入了一个“中间层”,所以可以在这个环境左很多有意思的事情，比如：
1.负载均衡：把访问请求均匀分散到多台机器，实现访问集群化；
2.内容缓存：暂存上下行的数据，减轻后端的压力；
3.安全防护：隐匿IP，使用WAF等工具抵御网络攻击，保护被代理的极其；
4.数据处理：提供压缩，加密等额外功能。
关于HTTP的代理还有一个特殊的“代理协议（proxy protocol）”，它由知名的代理软件HAProxy制订，但并不是RFC标准。</div>2021-04-02</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/5e/4e/85502e98.jpg" width="30px"><span>balance</span> 👍（2） 💬（1）<div>“数据不丢失”和“数据完整”不是一个意思吗？</div>2020-01-31</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/ea/25/75be8cdf.jpg" width="30px"><span>Halohoop</span> 👍（2） 💬（3）<div>所以，“著名的”酸酸乳，可以认为是正向代理不？</div>2019-06-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/ae/bd/d12f8907.jpg" width="30px"><span>梓航(﹏)</span> 👍（2） 💬（1）<div>老师，数据是通过什么方式从七层传到一层的呢，是有相关的系统接口来发这些数据吗？网卡又是怎么知道数据是要往外发的呢？</div>2019-06-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/17/0d/b2/8c876d07.jpg" width="30px"><span>sakila</span> 👍（2） 💬（1）<div>老师我想问一下，同一个域名下的不同文件可以指定不同的ip吗？比如test.com&#47;a.html指向1.1.1.1，test.com&#47;b.html指向2.2.2.2</div>2019-06-05</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTKuLsA1AAjUSO7oPHIqbA8f8slVIUw7nhdiaOI4nBYH6RxlyxXyFNe2Bc0g7yMoMHxnlh2mf43aVXw/132" width="30px"><span>zjajxzg</span> 👍（2） 💬（1）<div>1、dns是用来解析uri中的域名部分，将人能够记住的域名解析为计算机能够认识的ip地址，才能让</div>2019-06-05</li><br/>
</ul>