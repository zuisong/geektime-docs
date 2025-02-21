你好，我是何为舟。“Web安全”模块已经结束了，今天我会通过一篇串讲，带你回顾这一模块的知识，帮你复习巩固，更好地掌握和应用这些内容。

有同学留言说：“老师，讲了这么多漏洞的防护知识，有没有什么好的记忆方法呀？”首先，我们要明确一点，不管学什么知识，想要学好，在前期，一定需要时常复习来加深记忆。在此基础上，我们才能深刻理解和熟练应用这些知识。

那你可能要说了，怎么才能“记住”这些知识呢？我这里有一个我自己非常常用的、好的记忆方法，那就是“体系化的记忆”。怎么个体系化呢？说白了，就是每学完一块内容，通过自己的理解把相关的内容串联在一起。这也就是我们常说的，把知识变成自己的东西，长久下来，你就可以形成自己的知识体系了。

那放到我们这个“Web安全”模块中，我说过，安全落地的第一步是进行[威胁评估](https://time.geekbang.org/column/article/178528)，而威胁评估又可以分为：识别数据、识别攻击和识别漏洞。所以，今天我就基于比较常见的两种应用场景，通过威胁评估的方式，带你系统地复习我们学过的Web安全知识。

## 用户数据的威胁评估

假设，你正在为公司设计安全体系，首先要对用户数据进行威胁评估。以微博的用户数据为例，这些数据就包括：个人信息、博文信息以及关注互动信息等等。正常情况下，用户需要登录之后才能获取并修改自己的用户数据。那为了获取这些用户数据，黑客常常会通过盗取用户身份来进行未授权的操作。
<div><strong>精选留言（8）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/11/61/b1/1261c177.jpg" width="30px"><span>胖胖虎</span> 👍（1） 💬（1）<div>老师，我想问一下，为什么通过访问mysql的3306端口能知道内网的网络结构？</div>2020-01-28</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTKhuGLVRYZibOTfMumk53Wn8Q0Rkg0o6DzTicbibCq42lWQoZ8lFeQvicaXuZa7dYsr9URMrtpXMVDDww/132" width="30px"><span>hello</span> 👍（1） 💬（1）<div>老师：您好！请教您两个问题？烦请解惑？
问题1：内网服务器能访问互联网而且没有采用白名单的限制会存在什么样的漏洞？如果通过白名单限制，那服务器需要访问外网拉个镜像呀，某些软件升个级呀，这种情况下有什么好的可借鉴的处理方案没？
问题2：对存储数据（如：MySQL的数据）的加密有什么好的借鉴方案没？如部分字段数据加密？部分表数据加密？或是全库数据加密？同时给存储数据加密时，密钥该如何存储？我目前处理方案只支持指定的部分字段数据加密存储，同时数据加解密的密钥是密文存储在数据库中随应用服务启动解密放至在内存中给数据加解密用，但总觉得这种数据存储方式不灵活，而且密码明文长期放至内存中也不安全？老师是否有什么好的可借鉴的处理方案？谢谢！
</div>2020-01-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/46/79/01650d98.jpg" width="30px"><span>Y</span> 👍（0） 💬（1）<div>网络劫持，dns劫持这些会在后续章节讲么？</div>2020-01-07</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/2f/f4/2dede51a.jpg" width="30px"><span>小老鼠</span> 👍（13） 💬（0）<div>案例太少，知识不能落地</div>2020-01-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1d/3f/0d/1e8dbb2c.jpg" width="30px"><span>怀揣梦想的学渣</span> 👍（0） 💬（0）<div>思维导图做的很清晰</div>2023-06-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/19/92/92/0baba417.jpg" width="30px"><span>zdaiot</span> 👍（0） 💬（0）<div>请问作者，这种体系化的记忆，需要完全凭空回忆并梳理出来么？还是说，看着之前的内容，能梳理一遍即可</div>2023-03-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/92/6d/becd841a.jpg" width="30px"><span>escray</span> 👍（0） 💬（0）<div>安全落地的第一步是进行威胁评估，识别数据、识别攻击和识别漏洞

盗取用户身份的安全漏洞，主要有用户自身的密码保管不当和 Web 应用的漏洞（XSS、SQL 注入和CSRF）。

黑客利用 Web 安全漏洞（SSRF、反序列化漏洞和插件漏洞）和服务器“后门”，控制内网服务器的方式发动攻击

针对认证和授权的防护，主要是检测和过滤、加强认证（一次性 Token 和二次认证）、补丁管理。

在授权和审计阶段加入检测，识别异常的身份认证，最小权限原则、WAF Web Application Firewall 网站应用级入侵防御系统、IDS Intrusion Detection System 入侵检测系统。</div>2023-03-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/d0/78/a11a999d.jpg" width="30px"><span>COOK</span> 👍（0） 💬（0）<div>渗透性测试感觉是不完整的，还需要像老师讲的这样全面的评估</div>2020-03-29</li><br/>
</ul>