你好，我是李智慧。

Web应用防火墙（Web Application Firewall， WAF）通过对HTTP(S)请求进行检测，识别并阻断SQL注入、跨站脚本攻击、跨站请求伪造等攻击，保护Web服务安全稳定。

Web安全是所有互联网应用必须具备的功能，没有安全防护的应用犹如怀揣珠宝的儿童独自行走在盗贼环伺的黑夜里。我们准备开发一个Web应用防火墙，该防火墙可作为Web插件，部署在Web应用或者微服务网关等HTTP服务的入口，拦截恶意请求，保护系统安全。我们准备开发的Web应用防火墙名称为“Zhurong（祝融）”。

## 需求分析

HTTP请求发送到Web服务器时，请求首先到达Zhurong防火墙，防火墙判断请求中是否包含恶意攻击信息。如果包含，防火墙根据配置策略，可选择拒绝请求，返回418状态码；也可以将请求中的恶意数据进行消毒处理，也就是对恶意数据进行替换，或者插入某些字符，从而使请求数据不再具有攻击性，然后再调用应用程序处理。如下图：

![图片](https://static001.geekbang.org/resource/image/c6/27/c62b0c3517c9yy2ce9e556a75a44a427.jpg?wh=1920x588)

Zhurong需要处理的攻击和安全漏洞列表：

![图片](https://static001.geekbang.org/resource/image/ec/e2/ec061c371c83170cbdb4254332319ee2.jpg?wh=1920x884)

## 概要设计

Zhurong能够发现恶意攻击请求的主要手段，是对HTTP请求内容进行正则表达式匹配，将各种攻击类型可能包含的恶意内容构造成正则表达式，然后对HTTP请求头和请求体进行匹配。如果匹配成功，那么就触发相关的处理逻辑，直接拒绝请求；或者将请求中的恶意内容进行消毒，即进行字符替换，使攻击无法生效。
<div><strong>精选留言（5）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/0f/ec/13/49e98289.jpg" width="30px"><span>neohope</span> 👍（11） 💬（1）<div>
除了课程中提到的几种，Web方面的还有水平越权攻击，垂直越权攻击，渗透攻击，漏洞攻击，源码分析攻击，DDOS攻击，缓存攻击，随机数预测攻击，字典攻击，刷单攻击，钓鱼网站，钓鱼邮件，木马攻击，社会工程学攻击等等很多种。
大型商业机构，一般都会信息数据安全方面投入高额成本，包括但不限于防火墙、网闸、安全扫码、杀毒软件、入侵检测、操作系统、中间件、编码流水线、安全策略、安全咨询等等。
但这方面的攻防其实是很不对等的，黑客只需攻破一点，其余投入便都成了马奇诺防线。近年来，社会工程系攻击频频爆雷。从这个角度看，提升员工的安全意识，与上面的各类投入相比，反而更加重要一些。</div>2022-05-05</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/b9/32/84346d4a.jpg" width="30px"><span>雪碧心拔凉</span> 👍（2） 💬（1）<div>这种防火墙应用是要以一个应用的角色(类似网关？)挂在普通应用的前面，还是以sdk包的方式嵌入到应用中去？
如果是以网关的形式存在，那要解析body对性能是不是会有有很大的影响呢？一般我们网关都是响应式网关，不会去解析body流吧，解析body相当于要将数据从内核态拷贝到用户态，转发时在从用户态拷贝到内核态，性能是有影响吧？</div>2022-05-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/71/05/db554eba.jpg" width="30px"><span>👽</span> 👍（2） 💬（2）<div>请教一下，这种多层的安全校验会不会有性能问题？要过滤这么多层，每一层都有若干个正则。需要匹配的字符串比较长的话，感觉性能可能会受影响。
</div>2022-03-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/25/87/f3a69d1b.jpg" width="30px"><span>peter</span> 👍（0） 💬（2）<div>请教老师两个问题：
Q1：CSRF第一步怎么过渡到第二步？
CSRF的第一步是访问正常服务器，怎么第二步就访问攻击者服务器了？怎么过渡的？
Q2：假如应用服务器是Tomcat，Zhurong怎么才能先于tomcat处理请求？是将Zhurong注册到tomcat来作为一个前置filter吗？</div>2022-03-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/18/ee/a1ed60d1.jpg" width="30px"><span>ABC</span> 👍（0） 💬（0）<div>早年在一个通用评论类插件（类似Disqus）里面，发现了JS脚本注入。有人在评论里面写了一个alert，导致每次进入页面的时候浏览器会弹出一个弹窗。</div>2022-04-22</li><br/>
</ul>