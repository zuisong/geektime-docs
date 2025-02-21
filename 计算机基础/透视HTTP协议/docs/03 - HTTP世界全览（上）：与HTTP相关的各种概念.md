在上一讲的末尾，我画了一张图，里面是与HTTP关联的各种技术和知识点，也可以说是这个专栏的总索引，不知道你有没有认真看过呢？

那张图左边的部分是与HTTP有关系的各种协议，比较偏向于理论；而右边的部分是与HTTP有关系的各种应用技术，偏向于实际应用。

我希望借助这张图帮你澄清与HTTP相关的各种概念和角色，让你在实际工作中清楚它们在链路中的位置和作用，知道发起一个HTTP请求会有哪些角色参与，会如何影响请求的处理，做到“手中有粮，心中不慌”。

因为那张图比较大，所以我会把左右两部分拆开来分别讲，今天先讲右边的部分，也就是与HTTP相关的各种应用，着重介绍互联网、浏览器、Web服务器等常见且重要的概念。

![](https://static001.geekbang.org/resource/image/51/64/5102fc33d04b59b36971a5e487779864.png?wh=1142%2A1081)

为了方便你查看，我又把这部分重新画了一下，比那张大图小了一些，更容易地阅读，你可以点击查看。

暖场词就到这里，让我们正式开始吧。

## 网络世界

你一定已经习惯了现在的网络生活，甚至可能会下意识地认为网络世界就应该是这个样子的：“一张平坦而且一望无际的巨大网络，每一台电脑就是网络上的一个节点，均匀地点缀在这张网上”。

这样的理解既对，又不对。从抽象的、虚拟的层面来看，网络世界确实是这样的，我们可以从一个节点毫无障碍地访问到另一个节点。
<div><strong>精选留言（30）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/10/07/8c/0d886dcc.jpg" width="30px"><span>蚂蚁内推+v</span> 👍（83） 💬（1）<div>1. CDN 应当是不区分的，因为爬虫本身也是对 Web 资源的访问，且对于爬虫识别并不是 100% 准确的，因此 CDN 只会去计算实际使用了多少资源而不管其中多少来自爬虫；
2. 个人理解，Web Service 是网络服务实体，而 Web Server 是网络服务器，后者的存在是为了承载前者。</div>2019-06-05</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/1c/2e/93812642.jpg" width="30px"><span>Amark</span> 👍（37） 💬（3）<div>老师，能不能通俗地讲讲RPC, SOAP,  restful，之间的区别</div>2019-06-03</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/cf/18/16ec075e.jpg" width="30px"><span>飒～</span> 👍（33） 💬（6）<div>老师 ，暗网是如何规避搜索引擎的爬虫的，它又是怎么被人访问的呢</div>2019-06-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/17/2a/34/3308ef2d.jpg" width="30px"><span>Vickey Cheung</span> 👍（27） 💬（1）<div>老师，web服务器和web容器区别是什么呢？</div>2019-09-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/67/f4/9a1feb59.jpg" width="30px"><span>钱</span> 👍（22） 💬（1）<div>首先，非常喜欢这种评论多，互动多的专栏，好像买一赠一，感觉赚啦！有时有些疑惑看完评论就想明白了，这也是我判断一个专栏优质与否的标准之一，老师的专栏很棒，点赞！

1：你觉得 CDN 在对待浏览器和爬虫时会有差异吗？为什么？
刚开始觉得应该有区分的，不然反爬虫技术是干什么吃的，后来想想如果不用反爬虫技术的话应该是没差异的，因为CDN的核心工作是把网络的静态资源放的离用户更近一些，加速网络信息的获取速度，那区分是人要的信息还是机器人要的信息意义也不大，关键是我觉得爬虫如果做的好模仿真人来获取信息，那CND也是很难区分的，再者静态资源本来也是公开透明让用户代理来访问的嘛！

2：你怎么理解 WebService 与 Web Server 这两个非常相似的词？
首先，Web Server比较容易理解，就是web服务器，有软的也有硬的，软的特指有程序代码实现，硬的特指有实实在在的硬件机器组成，比如：Apache、nginx、tomcat、jetty等。
web service 直译是web服务，不过这么讲还是比较抽象不知道她是什么玩意？只好找一下，她的定义了。
Web  Service 是一种由 W3C 定义的应用服务开发规范，使用 client-server 主从架构，通常使用 WSDL 定义服务接口，使用 HTTP 协议传输 XML 或 SOAP 消息，也就是说，它是一个基于 Web（HTTP）的服务架构技术，既可以运行在内网，也可以在适当保护后运行在外网。
OK，直白来说，web service 是一种开发规范，规范即约定稍微有些强制执行的意味。她和 web Server 完全不是一种类型的东西，她比较虚是一个组织对某些行为的约束，告诉特定的人群，啥事能做？啥事不能做？啥事应该咋做？</div>2020-03-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/ba/a5/9f5ab366.jpg" width="30px"><span>redrain</span> 👍（21） 💬（1）<div>有些网站全新上线的，没有外链，也没特意提交过，为什么也会有爬虫经过呢，入口在哪里</div>2019-06-03</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/aa/21/6c3ba9af.jpg" width="30px"><span>lfn</span> 👍（19） 💬（1）<div>不是很理解web server和web service的区别。难道我们的服务不用nginx就不能用了么？我自己写个tcp server, 根据用户请求调用特定的handler返回数据，那我自己就是个server啊，也是service.老师能不能更清晰地定义下server.习惯了tcp编程的概念，这里的server就显得怪怪的，给人一种router的感觉.</div>2019-06-04</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/e2/54/f836054a.jpg" width="30px"><span>耿斌</span> 👍（13） 💬（4）<div>1. CDN可以根据User-Agent来判断发起请求的一端是浏览器还是爬虫，对待爬虫可以特殊处理返回特定内容
2. WebService是基于Web（HTTP）的服务器架构技术，基于HTTP协议传输xml或soap数据。WebServer分硬件和软件，硬件指服务器、云之类，软件如Nginx、Apache等</div>2019-06-06</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/21/63/f47576e1.jpg" width="30px"><span>永钱</span> 👍（10） 💬（1）<div>老师把tomcat放在web服务器中比较，说速度慢，不公平呀</div>2019-06-03</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/ff/c6/8b5cbe97.jpg" width="30px"><span>刘志兵</span> 👍（9） 💬（1）<div>老师，服务器只有这么少的几个吗，有一些grpc 服务算服务器吗，finagle, grpc等，还有spring不是也可以提供服务吗</div>2019-08-02</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/2a/d5/62dfbc11.jpg" width="30px"><span>patsun</span> 👍（8） 💬（1）<div>1.CDN在对待浏览器和爬虫时没有差异，因为如果没有验证码或者其他验证方式区分的话，浏览器和爬虫都被视为User Agent（客户代理）
2.Webservice是服务，Web Server是服务器</div>2019-06-03</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/76/a7/374e86a7.jpg" width="30px"><span>欢乐的小马驹</span> 👍（5） 💬（2）<div>老师，你说可以通过User-Agent来区分爬虫，那他们能假装成浏览器吗？怎么假装成浏览器呢？</div>2020-02-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1a/c9/d2/da213e18.jpg" width="30px"><span>朤..</span> 👍（4） 💬（1）<div>爬虫作为机器人，承载他的物理容器是什么？那为啥这个就不能作为一个真实的用户去访问数据？</div>2020-03-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/f4/b6/019bbb4d.jpg" width="30px"><span>少即是多</span> 👍（3） 💬（2）<div>1.	你觉得 CDN 在对待浏览器和爬虫时会有差异吗？为什么？你怎么理解?
CDN不会管是谁访问自己，本质上它只是一种提供资源加速服务的方式。
如果需要针对爬虫做搜索引擎优化，服务端可以根据User-Agent来判断发起请求的一端是浏览器还是爬虫，对待爬虫可以专门的服务端渲染等。

2.	WebService 与 Web Server 这两个非常相似的词？
一个是服务，一个是服务运行环境
</div>2020-11-02</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/ab/e1/079ee6e3.jpg" width="30px"><span>壹笙☞漂泊</span> 👍（3） 💬（1）<div>1、应该不会有差异，因为爬虫主要就是无限模仿浏览器行为
2、Web Server 是服务器，Web Service 是一种应用服务开发规范</div>2019-06-03</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/b7/cb/18f12eae.jpg" width="30px"><span>不靠谱～</span> 👍（3） 💬（1）<div>1.不是太清楚，个人认为不会区别对待，因为在正常程序应用来说，看不出是谁发起的请求。
2.web server是软件服务器，承载应用。
web service是一种服务方式。</div>2019-06-03</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/23/52/66/3e4d4846.jpg" width="30px"><span>includestdio.h</span> 👍（2） 💬（1）<div>1.CDN可以根据UA IP 访问频率等多个维度识别是否爬虫，但是否会区别对待，主要是看业务是否有区别对待的必要，或CDN是否有反爬虫策略

2.Web Server 是实实在在的硬件 软件相结合，且可以提供 Web Service 的平台，后者更像是一个定义，前者更像是一个实体</div>2021-06-15</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/a3/fc/379387a4.jpg" width="30px"><span>ly</span> 👍（2） 💬（2）<div>老师，我看了您对某位童鞋的评论说tomcat、netty只是http的“副业”，但是我对这2个中间件的了解，它们两个就是用来处理客户端的http请求的呀，我不是很明白您这里的“副业”是什么含义呢？难道这2个中间件有其他除http额外的协议吗？  请老师解答疑惑！！！</div>2019-08-03</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/79/4b/740f91ca.jpg" width="30px"><span>-W.LI-</span> 👍（2） 💬（3）<div>第一个有差别，因为有烦爬虫技术
第二个:web server 。web服务提供者，web服务器。web应用程序。 web service。。。。不知道了</div>2019-06-03</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/55/27/44c33cb1.jpg" width="30px"><span>Berry He</span> 👍（2） 💬（1）<div>第一个不太清楚，不敢妄加评论。
第二个:web server和web service是两个概念，前者是web服务器，像iis apache nginx这种。web service他只是一个或多个提供web请求响应的api，用来获取或提交更新web server资源的</div>2019-06-03</li><br/><li><img src="" width="30px"><span>张烨</span> 👍（1） 💬（1）<div>1、CDN应该不会去区分用户和爬虫，但对于过度消耗资源的用户（疑似爬虫）可能会有别的方式例如WAF对它进行拦截和限制。
2、Web Service是服务，Web Server是服务器，并不是完全相等的概念，但是它们之间的关联很紧密，因为服务器为用户提供服务，服务器是现实载体、服务是虚拟功能。</div>2022-05-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/44/db/689eaf1c.jpg" width="30px"><span>请叫我大萌萌</span> 👍（1） 💬（1）<div>关于 Web Server 和 Web Service 的理解。

客户端（Chrome）和服务器（Nginx）之所以可以通讯，是因为二者皆遵循了 HTTP 协议进行开发的。

而用 Perl、Java 类的编程语言实现的 web service。也可以不通过 Nginx 来进行通讯，那是否可以理解从这个层面上来讲此时去掉中间层的 Nginx、那我们自己实现的 web service 也是 webserver。

而为什么至今网络上大部分的架构并没有去掉 Nginx 的原因是不是可以理解为，Nginx 性能强劲，而且有成熟的负载均衡等解决方案；普通的 Django、Tomcat 性能无法比之。

因为 HTTP 是允许多节点双向通讯的，我理解的是 Tomcat 和 Nginx 都是 Web server。之所以要加上 Nginx 而不直接用 Tomcat 的原因上面已经说过了。其实就是 Chrome、Nginx、Tomcat 大家都遵循了 HTTP 协议。

Chrome 只能做客户端所以它是客户端；
Nginx、Tomcat 既可以做客户端也可以做服务端，所以他们都是服务端。

Chrome &lt;==&gt; Nginx &lt;==&gt; Tomcat。

仅此而已，请问下罗老师我的想法是否正确。确实难以理解 web server 和软件硬件有什么关系。</div>2020-01-16</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/JbLNnnttWxykBVPnCHrpWLqgxiaVlcE1eUOA8LWFQjLJ3gmZ8SZD0vdFR5ticQZxfWXu9NddNW7tUWEqK6ibFQw6w/132" width="30px"><span>Inner peace</span> 👍（1） 💬（1）<div>1. 不会区别对待，当爬虫的浏览器都使用一样的useragent时，cdn并不能识别
2. Web server是web服务器，web service是一种web服务协议</div>2019-06-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/cb/9d/2bc85843.jpg" width="30px"><span>　　　　　　　鸟人</span> 👍（1） 💬（1）<div>你觉得 CDN 在对待浏览器和爬虫时会有差异吗？为什么？
不管是否反爬虫 应该都没区别  爬虫本质不就是模拟浏览器么</div>2019-06-04</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/d6/53/21da9e2b.jpg" width="30px"><span>磊爷</span> 👍（1） 💬（1）<div>1.正常情况下没有差异，客户端访问服务器，cdn加速缓存。
2.websevice是一种服务，提供相应的内容。
Web sever是服务器，可获得内容不受限。</div>2019-06-03</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/78/ac/e5e6e7f3.jpg" width="30px"><span>古夜</span> 👍（1） 💬（1）<div>tomcat不也是阿帕奇的吗？啥时候变成JAVA的了</div>2019-06-03</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/1b/6e/cd8fea9f.jpg" width="30px"><span>RecordLiu</span> 👍（0） 💬（1）<div>问题 1：
我认为 CDN 在对待浏览器和爬虫是没有差异的。
本质上，浏览器和爬虫都属于 HTTP 客户端，而且爬虫可以通过设置一些特定参数，可以做到跟人工用浏览器访问网页一样。
对于 CDN 来说，两者都是客户端请求，并没有差异。

问题 2：
说一下我个人的理解，可能有理解错误的地方，望老师和大家指正。

Web Server 是用于接收和处理 HTTP 请求的服务器，可以认为它是一个 「软件」和「硬件」的集合体。

举个例子来理解：比如将 nginx 部署到腾讯云服务器。

这里的软件指的就是 Nginx,而腾讯云服务器本质是 「硬件」(硬件可以理解成是含高配置、大功率的计算机)。

这是比较狭义下的理解，作为完整的 web Server，可能还包含很多服务。

比如基于 PHP 实现的网站,nginx 并不能解释和直接运行 PHP 代码，而会把带有 PHP 代码的网页请求转发到 PHP 服务，由 PHP 服务负责解释和运行代码，然后再将运行结果返回给 nginx。

而 PHP 服务也是部署在「硬件服务器」上的，也可以把 PHP 服务理解成一种软件。再者，如果这段 PHP 代码，还包含数据查询的操作，那么还会涉及 PHP 服务跟数据库服务(比如 MySQL )的交互。

PS: 「硬件服务器」上需要安装相应的操作系统(比如 Linux 操作系统)，才能部署 Nginx、PHP、Mysql 等这些「软件」服务。


而 Web Service 可以认为是一种 「技术解决方案」，而这种技术也使用 HTTP 进行传输数据。
两者的相同之处都在于使用 HTTP 作为应用层的传输协议。</div>2024-09-02</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1a/80/10/2406a662.jpg" width="30px"><span>希言自然</span> 👍（0） 💬（1）<div>看到老师回复各位同学的信息，受益匪浅。谢谢大家！我弱弱的提个问题，就是前后端分离的实现原理是什么？是不是通过 WEB Server 获取 HTTP 请求后再转发到 WEB 容器中去进行业务处理，最终再返回 WEB Server 然后去响应UA的请求？（* 这里的 WEB Server 可以直接就是 WEB 容器，因为容器也有 WEB Server 的功能）老师或者同学有没有帮忙浅显易懂的解释下，谢谢啦~~</div>2023-08-24</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTJ313aXGKeQm1edMtWHs9ibmG8l1VbemO1gfPlzbrntFpwa5xTecv7v5q1iazCroV2f8xvJSSIQsOuw/132" width="30px"><span>Geek_3wtncp</span> 👍（0） 💬（1）<div>使用任意编程语言，实现了 web service 规范的 http协议上的服务接口的软件，就是可以算是 Web Server 的软件了。能这么理解么？</div>2023-01-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/2d/ca/7c/98193e9e.jpg" width="30px"><span>奕晨</span> 👍（0） 💬（1）<div>1. 你觉得 CDN 在对待浏览器和爬虫时会有差异吗？为什么？
    不会，因为CDN是利用了http缓存和代理机制，代替源点响应客户端的请求，可以快速的项羽请求，是不会区分的。
2. 你怎么理解 WebService 与 Web Server 这两个非常相似的词？
    WebService 是网络服务的实体，web Server 是网络服务器</div>2022-07-24</li><br/>
</ul>