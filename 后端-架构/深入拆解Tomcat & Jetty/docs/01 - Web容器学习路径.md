你好，我是李号双。在开篇词里我提到要成长为一名高级程序员或者架构师，我们需要提高自己知识的广度和深度。你可以先突破深度，再以点带面拓展广度，因此我建议通过深入学习一些优秀的开源系统来达到突破深度的目的。

我会跟你一起在这个专栏里深入学习Web容器Tomcat和Jetty，而作为专栏更新的第1篇文章，我想和你谈谈什么是Web容器，以及怎么学习Web容器。根据我的经验，在学习一门技术之前，想一想这两个问题，往往可以达到事半功倍的效果。

## Web容器是什么？

让我们先来简单回顾一下Web技术的发展历史，可以帮助你理解Web容器的由来。

早期的Web应用主要用于浏览新闻等静态页面，HTTP服务器（比如Apache、Nginx）向浏览器返回静态HTML，浏览器负责解析HTML，将结果呈现给用户。

随着互联网的发展，我们已经不满足于仅仅浏览静态页面，还希望通过一些交互操作，来获取动态结果，因此也就需要一些扩展机制能够让HTTP服务器调用服务端程序。

于是Sun公司推出了Servlet技术。你可以把Servlet简单理解为运行在服务端的Java小程序，但是Servlet没有main方法，不能独立运行，因此必须把它部署到Servlet容器中，由容器来实例化并调用Servlet。
<div><strong>精选留言（30）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/17/64/da/5fb5817c.jpg" width="30px"><span>蔡伶</span> 👍（66） 💬（1）<div>打卡

先说下听完老师课程的感受：经典不会随着时间而消逝。java和servlet规范已经发布20多年、操作系统和网络协议以及html更是经过了几十年的洗礼，现在依然是业内最核心的技术基础，毫不动摇。

课程的理解：当前web技术涉及的知识包括这样几层，
第一层：核心规范相当于宪法，主要包括servlet规范、网络协议等；
第二层：主流技术支撑相当于各类法律，包括java语言、各类中间件等；
第三层：基于各行业的业务应用和框架，相当于行政法规地方法规。
规范是基础，具体实现可以用java也可以用python等等，行业应用和框架更是可以百花齐放。
那我们的学习一定是从具体技术入手，从规范和体系结构统筹安排，最后再落实到实现。是一个自底向上再由上向下的一个过程，也是一个由薄到厚再由厚到薄的过程。</div>2019-05-15</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/e1/d2/42ad2c87.jpg" width="30px"><span>今夜秋风和</span> 👍（43） 💬（3）<div>应用程序的上下文，这个概念总是感觉理解不透彻</div>2019-05-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/6a/59/ba3cad16.jpg" width="30px"><span>G</span> 👍（35） 💬（1）<div>你说的所有spring. 都应该说springMVC</div>2019-05-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/f6/66/991b7e3a.jpg" width="30px"><span>贤蛋蛋</span> 👍（30） 💬（2）<div>请问为什么说http是超文本传输协议，文本两字的含义是什么？http2.0所说的二进制帧，为什么说是二进制，和1.1格式上的本质区别是什么？再往下一层到TCP能否都看成二进制帧？</div>2019-05-15</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/e7/4a/4dfb565a.jpg" width="30px"><span>凌霄</span> 👍（25） 💬（1）<div>遇到过一个偶发的tomcat8问题，请求到tomcat后，nio长连接，到了20秒后超时后才自动断开连接，返回结果内容正常，抓包发现和正常的比少了最后的回车换行。</div>2019-05-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/7b/41/85796e32.jpg" width="30px"><span>飞向云端</span> 👍（12） 💬（1）<div>什么叫内嵌方式运行servlet容器，老师有时间普及一下。</div>2019-05-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/17/83/72/e37bbc52.jpg" width="30px"><span>yy_java</span> 👍（6） 💬（1）<div>请问老师，操作系统基础 除了您推荐的那本书以外还有其他薄点的书籍推荐吗？</div>2019-05-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/5f/73/bb3dc468.jpg" width="30px"><span>拒绝</span> 👍（6） 💬（2）<div>还停留在使用容器的阶段，并不清楚其原理，例如：一个请求到一个响应返回，其涉及到的设计模式，以及为什么这样做，这样做的好处是什么；我能在容器的基础上做一些自定义的扩展吗？希望在专栏收获到这些。</div>2019-05-13</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/BDqfaEhaYiaRLj92HaU4P8QmdPsNYGPaelpcMmUaM4ZVB2CRKErqWqnVibVMIKHjrV4Kg9g87VLSickPOqmeNvACA/132" width="30px"><span>chibohe</span> 👍（4） 💬（1）<div>如果我的服务全都是rpc调用，不涉及http调用，可以不部署在tomcat或者jetty容器中吗？还有你说的Spring都应该指的是SpringMVC吧？</div>2019-05-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/16/5b/83a35681.jpg" width="30px"><span>Monday</span> 👍（4） 💬（1）<div>操作系统还是我的痛，但也不是一两天就能补充得了的。只好边学本专栏边学操作系统了。希望不要因为操作系统的缘故拖了学习本专栏的后腿😃😃</div>2019-05-16</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/f8/ea/98738420.jpg" width="30px"><span>Jaswine</span> 👍（4） 💬（1）<div>带着问题学知识，学习的时候问自己几个为什么，为什么这么设计？为什么不那么设计？在自己解答这些为什么的时候，最后发现都是计算机基础知识决定的，操作系统，网络，数据结构和算法</div>2019-05-15</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/55/06/a495741c.jpg" width="30px"><span>刘三通</span> 👍（3） 💬（1）<div>Spring应用本身就是一个Servlet容器</div>2019-05-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/e1/0e/2912db26.jpg" width="30px"><span>小可爱(๑• . •๑)</span> 👍（3） 💬（1）<div>期待不断更新，希望老师能够讲清楚，让大家都理解</div>2019-05-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/e5/33/ff5c52ad.jpg" width="30px"><span>不负</span> 👍（2） 💬（1）<div>Web容器通常具备 HTTP 服务器和 Servlet 容器的功能，Tomcat 和 Jetty 是其经典代表。
Servlet 容器：部署和启动 Web 应用的环境。

1）文中提到的“嵌入式Web容器”，是已经不依赖外部容器，项目本身（具备Servlet功能）部署到一个HTTP服务器即可启动？
2）web服务器就是一个HTTP服务器？</div>2019-05-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/c9/cb/7b6802cc.jpg" width="30px"><span>贾智文</span> 👍（1） 💬（1）<div>想问下为什么内嵌的web容器会更加简单？</div>2019-06-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/c2/cc/ca22bb7c.jpg" width="30px"><span>蓝士钦</span> 👍（1） 💬（1）<div>想请问一下老师，我们平时的业务很简单的增删改查，从Controller到Service再到Dao层都是一个链式调用，这种简单的业务需要遵循面向接口设计的原则吗？</div>2019-06-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/56/90/be01bb8d.jpg" width="30px"><span>Asanz</span> 👍（1） 💬（1）<div>上来就搞 UNIX环境高级编程 这个大块头吗？？？</div>2019-05-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/56/05/152830ea.jpg" width="30px"><span>空亦非空</span> 👍（0） 💬（1）<div>是不是有些路线可以并行？</div>2019-08-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/cd/e0/c85bb948.jpg" width="30px"><span>朱雯</span> 👍（0） 💬（1）<div>我是一名运维工程师 工作经验不长 也断断续续 现在公司的系统是一个用java写的系统  其中tomcat也在其中使用 我本想抱着学习如何配置 如何使用 部署的来学这个tomcat容器 看到您推荐的这些书 我感受到了自己的操作系统基础以及java基础不够 存在担心自己跟不上的担心....这种担心正常吗 我是该去补完您说的那些课程 还是直接跟课呢</div>2019-06-25</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/17/2f/bb/f663ac5a.jpg" width="30px"><span>itschenxiang</span> 👍（0） 💬（1）<div>请问 &quot;由应用本身来启动一个嵌入式web容器，而不是通过web容器来部署和启动应用，这样可以降低应用的复杂度&quot; 这句话怎么理解，是指传统的使用Tomcat作为web容器和SpingBoot这种方式吗？</div>2019-06-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/d0/69/5dbdc245.jpg" width="30px"><span>张德</span> 👍（0） 💬（1）<div>老师后期能不能说一下tomcat和weblogic的区别  以前在某知名股份制银行工作的时候  开发用jetty 但是线上却用weblogic  完全不懂为什么。。。</div>2019-05-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/e5/84/4a01e18d.jpg" width="30px"><span>nsn_huang</span> 👍（0） 💬（1）<div>老师您好,您在文章中说到要从操作系统学起,并建议读一读《UNIX环境高级编程》,我也深知操作系统的重要性,但是作为一名大学生,想读完本科就工作,从事Java方向,总感觉自己的时间不够用,感觉可能操作系统学不到太深,您有什么好的建议么?</div>2019-05-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/a0/a4/b060c723.jpg" width="30px"><span>阿斯蒂芬</span> 👍（0） 💬（1）<div>老师在讲servlet和tomcat有没有推荐书单🙏
</div>2019-05-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/00/01/5c28c66c.jpg" width="30px"><span>快跑吧小姑娘，快跑</span> 👍（0） 💬（1）<div>现在都用spring boot，很想压榨单应用http的并发请求处理，还有单应用启动速度，以及怎么优化容器</div>2019-05-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/df/7d/d5bc03a4.jpg" width="30px"><span>落幕</span> 👍（30） 💬（2）<div>和一群优秀的人共同进步，这种感觉很好。</div>2019-05-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/a8/e8/bc84c47d.jpg" width="30px"><span>熊斌</span> 👍（9） 💬（0）<div>工作几年之后才明白 万变不离其宗，所以一直努力往技术的最底层走。跟着大佬探寻常用技术的本质。双11刚买的课，每天看一两节</div>2019-11-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/c3/3d/abb7bfe3.jpg" width="30px"><span>林炳强</span> 👍（7） 💬（0）<div>Spring 框架就是对 Servlet 的封装。。。
这句话我感觉容易造成误解。Spring MVC只是Spring的一部分，只有Spring MVC是Servlet的实现，其他的并没有。</div>2019-06-23</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTKMMsbPLKSkKJ5rEvoDE3T5aUgyicTXS2TyicIDPVDcsBStQfWQicuTNeFicBuEWibJepLQgEQOogpAcnQ/132" width="30px"><span>balsamspear</span> 👍（4） 💬（0）<div>**思考题**

请你分享一下你对 Web 容器的理解，或者你在学习、使用 Web 容器时遇到了哪些问题？

Web 容器是 HTTP 服务器 + Servlet 容器

1. HTTP 服务器负责处理 HTTP 请求（接收请求、返回请求结果）
2. Servlet 容器负责把 HTTP 请求分派给对应的 servlet 程序处理，并把结果返回给 HTTP 服务器

问题

1. 如何解析请求？
2. HTTP 服务器线程、Servlet 容器线程和 servlet 程序线程的关系？
3. Web 容器能支持什么量级的并发，由哪一块决定？HTTP 服务器、Servlet 容器还是 servlet 程序？</div>2020-09-15</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1d/0f/91/5e03fe38.jpg" width="30px"><span>Mr.tt</span> 👍（3） 💬（0）<div>说说对Web容器的理解:所谓容器就是一个装东西的东西，比如水容器，就是装水的，而我们的web容器就是装web的，从这里就可以看出，tomcat等这类容器是可以部署多个web项目的。在深入一点点，一个能作为水容器的要求是什么？不能有漏洞对不对，那么作为一个web容器它的要求是什么呢？一.能够处理网络请求，二.能返回数据。首先能够处理网络请求(作为http服务器)，这个意味着它能够监听端口，能够操作操作系统里的网络请求，并把这些请求和我们的web项目关联起来，交给我们的web项目处理这些请求，我们项目要怎么处理这些请求呢？什么样的程序能够处理这些请求呢？有没有什么规范呢？答案是有的，就是servlet规范。这个规范和tomat有啥关系？tomcat就是一个servlet容器。所以tomcat其实是一个http服务器+servlet服务器的集合</div>2020-08-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/c9/cb/467065d0.jpg" width="30px"><span>Rumble</span> 👍（2） 💬（0）<div>我天，1楼的大佬也太6了，没去从政真的是浪费人才</div>2020-01-15</li><br/>
</ul>