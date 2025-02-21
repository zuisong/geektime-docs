在专栏[第1讲](https://time.geekbang.org/column/article/97837)时我曾经说过，为了实现在互联网上构建超链接文档系统的设想，蒂姆·伯纳斯-李发明了万维网，使用HTTP协议传输“超文本”，让全世界的人都能够自由地共享信息。

“超文本”里含有“超链接”，可以从一个“超文本”跳跃到另一个“超文本”，对线性结构的传统文档是一个根本性的变革。

能够使用“超链接”在网络上任意地跳转也是万维网的一个关键特性。它把分散在世界各地的文档连接在一起，形成了复杂的网状结构，用户可以在查看时随意点击链接、转换页面。再加上浏览器又提供了“前进”“后退”“书签”等辅助功能，让用户在文档间跳转时更加方便，有了更多的主动性和交互性。

那么，点击页面“链接”时的跳转是怎样的呢？具体一点，比如在Nginx的主页上点了一下“download”链接，会发生什么呢？

结合之前的课程，稍微思考一下你就能得到答案：浏览器首先要解析链接文字里的URI。

```
http://nginx.org/en/download.html
```

再用这个URI发起一个新的HTTP请求，获取响应报文后就会切换显示内容，渲染出新URI指向的页面。

这样的跳转动作是由浏览器的使用者主动发起的，可以称为“**主动跳转**”，但还有一类跳转是由服务器来发起的，浏览器使用者无法控制，相对地就可以称为“**被动跳转**”，这在HTTP协议里有个专门的名词，叫做“**重定向**”（Redirection）。
<div><strong>精选留言（30）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/0f/67/f4/9a1feb59.jpg" width="30px"><span>钱</span> 👍（48） 💬（8）<div>之前面试官好像比较喜欢问外部重定向和内部重定向的区别？
外部重定向，服务器会把重定向的地址给浏览器，然后浏览器再次的发起请求，地址栏的地址变化了。
内部重定向，服务器会直接把重定向的资源返给浏览器，不需要再次在浏览器发起请求，地址栏的地址不变。
重定向我的经验，主要用在未登录或者权限不足的场景，跳转到对应的登录或提升页面之中。
当然，通用的SSO也是这样做的。</div>2020-03-29</li><br/><li><img src="" width="30px"><span>Geek_5b0e47</span> 👍（17） 💬（1）<div>笔记：
主动跳转：跳转动作是由浏览器的使用者主动发起的;
被动跳转：跳转动作是由服务器发起的，浏览器使用者无法控制。

1、重定向状态码

301：俗称“永久重定向”，原URI已经“永久”性地不存在了，今后的所有请求都必须改用新的URI.
302: 俗称“临时重定向”，原URI处于“临时维护”状态，新的URI是起“顶包”作用的临时工。
303 See Other: 类似302，但要求重定向后的请求改为GET方法，访问一个结果页面，避免POST&#47;PUT重复操作；
307 Temporary Redirect: 类似302，但重定向后请求里的方法和实体不允许变动，含义比302更明确；
308 Permanent Redirect: 类似307，不允许重定向后的请求变动，但它是301“永久重定向”的含义

2、重定向的应用场景
一个最常见的原因就是“资源不可用”，需要用另一个新的URI来代替。
不可用的原因：如域名变更、服务器变更、网站改版、系统维护。
另一个原因就是“避免重复”，让多个网址都跳转到一个URI，增加访问入口的同时还不会增加额外的工作量。如：有的网站会申请多个名称类似的域名，然后把它们重定向到主站上。

3、重定向的相关问题
第一个问题是“性能损耗”。重定向的机制决定了一个跳转会有两次请求-应答，比正常的访问多了一次。
第二个问题是“循环跳转”。如果重定向的策略设置欠考虑，可能会出现“A=&gt;B=&gt;C=&gt;A”的无限循环。</div>2020-03-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/07/8c/0d886dcc.jpg" width="30px"><span>蚂蚁内推+v</span> 👍（14） 💬（1）<div>老师，使用301会比302有较大的性能提升么</div>2019-08-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/57/4f/6fb51ff1.jpg" width="30px"><span>奕</span> 👍（12） 💬（2）<div>老师，这个301，302, 303重定向要求前后协议一致吗？http不能调转https?</div>2019-07-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/93/ff/87d8de89.jpg" width="30px"><span>snake</span> 👍（9） 💬（1）<div>站外重定向就要开两个连接，如果网络连接质量差，那成本可就高多了，会严重影响用户的体验。
------------》
老师这个我不理解，站外重定向，比如重定向到其他网站，那客户端的连接跟自己的服务端应该就没有什么关系了吧？为什么还有两个连接呢？不是客户端应该跟其他网站的服务器连接吗？</div>2020-06-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/81/4e/d71092f4.jpg" width="30px"><span>夏目</span> 👍（9） 💬（1）<div>1、301用于废弃原地址跳转新地址，302用于暂时无法访问原地址跳转新地址，两者都需要浏览器重新发起一次请求
2、最开始接触重定向的时候就是用于未登录跳转登录页了</div>2019-12-03</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/20/e9/fe/bc38c919.jpg" width="30px"><span>lll</span> 👍（7） 💬（2）<div>“另一个原因就是“避免重复”，让多个网址都跳转到一个 URI，增加访问入口的同时还不会增加额外的工作量。”这句话怎么理解呢？</div>2020-09-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/11/a2/33be69a6.jpg" width="30px"><span>毛毛</span> 👍（6） 💬（4）<div>重定向和转发的区别和用途，以后章节会讲吗？</div>2019-07-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/c9/fd/5ac43929.jpg" width="30px"><span>天方夜</span> 👍（4） 💬（1）<div>从短域名跳长域名（z.cn - www.amazon.cn），从 http 跳 https，分别应当用哪种重定向，有没有最佳实践呢？</div>2021-02-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/86/e3/a31f6869.jpg" width="30px"><span> 尿布</span> 👍（4） 💬（1）<div>重定向报文里还可以用Refresh字段，实现延时重定向，例如”Refresh: 5; url=xxx“告诉浏览器5秒钟后再跳转

与跳转有关的还有一个”Referer“和”Refereer-Policy“（注意前者是个拼写错误，但已经”将错就错“），表示浏览器跳转的来源（即引用地址），可用于统计分析和防盗链</div>2020-09-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/19/e4/4f/df6d810d.jpg" width="30px"><span>Maske</span> 👍（4） 💬（1）<div>1.好比去寄快递，我去到常去的寄送点，发现寄送店有一块告示栏，被告知当前地点近期处于维修状态，需要前往另一个临时寄送点办理（302状态码），临时地址即为location字段值。或者被告知当前寄送店已永久搬迁至新地址（301状态码），临时地址为location字段值。两者都表示当前访问地址已失效，区别在于一个为临时的，短期的，另一个为永久性的。
2.比如商城类的页面，需要浏览个人中心或者订单列表等页面时需要进行登录态校验，如果没有登录或者登录态失效了，需要重定向到登录页。某个页面进行了重构，且url发生了变化，由于老url遍布站点的很多页面，不好直接修改跳转url，此时将老url重定向到新url是比较合适的。
有个疑问请教一下老师：
内部重定向和外部重定向一般在使用场合上有什么区别？
查了一下 资料说内部重定向不会造成浏览器地址栏url的变化，实际对客户端是无感知的，只是代理转发到另一个url。个人感觉又不太对，因为资料上又说nginx的重定向是属于内部，但是实际客户端url确实变了，比较矛盾</div>2020-06-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/26/ba/a9/7432b796.jpg" width="30px"><span>coral</span> 👍（3） 💬（1）<div>一个问题：
打开qq.com的时候，浏览器进行了两次跳转：
http:&#47;&#47;qq.com =&gt; https:&#47;&#47;qq.com =&gt;https:&#47;&#47;www.qq.com 
访问google.ca的时候也有类似的现象
http:&#47;&#47;google.ca&#47; =&gt; http:&#47;&#47;www.google.ca&#47; =&gt; https:&#47;&#47;www.google.ca&#47;?gws_rd=ssl

为什么要设计中间的那一层呢？从第一步直接redirect到最后一个url不行吗？

作业
1. 301 和 302 非常相似，试着结合第 12 讲，用自己的理解再描述一下两者的异同点。
同：两者都会让访问者知道，当前url不可用，并且会在location字段里回复你要去的的url。
异：
301: “永久重定向”（Moved Permanently），表示原来的页面永久不可用，所有优化的程序都可以更新了，如浏览器可以更新bookmark，爬虫更新搜索库。
302: “临时重定向”（“Moved Temporarily”），要访问的页面临时不可用了，优化程序不需更新，临时跳转一下即可。

2. 你能结合自己的实际情况，再列出几个应当使用重定向的场景吗？
需要更换域名&#47;页面url的时候，可以给旧的url设置一个重定向，导到新的url去，这样曾经bookmark旧url的用户也可以访问到新的内容而不会看到报错页面。
还有把http页面重定向到https、把不带www的页面重定向到www.开头的页面也是很常见的操作。</div>2021-04-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/c9/fd/5ac43929.jpg" width="30px"><span>天方夜</span> 👍（3） 💬（1）<div>有同学提到 ajax 中的重定向，这是个有点复杂的问题。简单说，xhr 方式，存在 Location 的情况下只能看到重定向后的最终结果；fetch 方式，可以看到 Location，而且对于重定向有不同的处理模式，可以设置。</div>2021-02-21</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTI8mFt5wSkia31qc8paRg2uPSB6AuEBDricrSxvFBuTpP3NnnflekpJ7wqvN0nRrJyu7zVbzd7Lwjxw/132" width="30px"><span>Geek_steven_wang</span> 👍（3） 💬（2）<div>Sso就会用重定向引导用户登录。
但如果location中没有地址，那浏览器也不知跳转到那，会出错。</div>2019-08-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/26/eb/d7/90391376.jpg" width="30px"><span>ifelse</span> 👍（2） 💬（2）<div>“Location”字段属于响应字段，必须出现在响应报文里。但只有配合 301&#47;302 状态码才有意义，它标记了服务器要求重定向的 URI。--记下来</div>2023-01-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/18/07/53/05aa9573.jpg" width="30px"><span>keep it simple</span> 👍（2） 💬（1）<div>老师你好，提交几个问题：
1.在自己的测试中，保存了一个https:&#47;&#47;bing.com的书签，访问后得到301，location为cn.bing.com，但书签中的地址并没有改变，还是https:&#47;&#47;bing.com。是否意味着我使用的浏览器没有遵循301的规范？
2.关于303的使用场景是什么？如果原请求方式就是POST，用于上传一组数据，然后服务器返回303，浏览器端只能用GET，那需要上传的数据就无法被上传了吧？
3.关于307的描述，言外之意是302可以改变请求里的方法和实体，但服务端只返回location的情况下，浏览器也不会改变请求方法和实体吧？
</div>2020-01-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/e5/39/951f89c8.jpg" width="30px"><span>信信</span> 👍（2） 💬（2）<div>文中提到的所有链接都返回200，和访问http:&#47;&#47;www.chrono.com&#47;一个效果。。。。。。</div>2019-07-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/18/22/89/73397ccb.jpg" width="30px"><span>响雨</span> 👍（2） 💬（3）<div>我这边要做一个web升级，在升级过程中要展示升级进度，就打算301重定向到另一个服务来展示升级的进度</div>2019-07-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/92/e4/abb7bfe3.jpg" width="30px"><span>TerryGoForIt</span> 👍（2） 💬（1）<div>重定向可以应用于实现负载均衡。</div>2019-07-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/7a/ee/257a22fb.jpg" width="30px"><span>饭饭</span> 👍（2） 💬（1）<div>老师您好，
重定向，我一般使用在移动PC互切的情况下会使用，因为使用到了域名会不一样。还有一种情况会在判断浏览器的时候会使用到重定向，比如IE。。。

但是有一个问题，302是临时重定向，想问一下浏览器在每次访问的时候，都会直接访问原先URI吗？还是会有什么过期时间呢？</div>2019-07-08</li><br/><li><img src="" width="30px"><span>刘同青</span> 👍（1） 💬（1）<div>OAuth2授权是302典型的使用场景，浏览器发起授权请求，授权服务器会将浏览器重定向到用户确认页面，用户确认后，会再次被302到应用的回调地址，如果是授权登录，那么应用收到回调地址完成登录后，会再次将浏览器重定向到指定页面（比如首页）等；

在这个过程中，每一次重定向都是有作用的，这种不能用301，否者浏览器记录了最后的URI，就不能授权了</div>2023-09-07</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/2e/53/bf62683f.jpg" width="30px"><span>狼的诱惑</span> 👍（1） 💬（1）<div>老师好，又来请教问题了
1.状态码301，302是有些客户端遵循http规范默认支持吗？比如浏览器，是不是浏览器解析了返回状态码，解析到301或302然后解析出地响应头&#47;15-1地址然后又发起了一次http请求？能举例那些客户端不支持重定向吗？
2.我觉得看文章的同时，我们是不是结合着老师提供的实验源码，来了解整个来龙去脉，这样会更容易理解？虽然老师用的lua，但还是可以勉强看懂的</div>2019-08-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/57/4f/6fb51ff1.jpg" width="30px"><span>奕</span> 👍（1） 💬（4）<div>对于ajax请求，网上好多资料说不能处理重定向的请求比如321,302,303等，不能进行跳转，这个是为什么呢？</div>2019-07-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/30/8a/b5ca7286.jpg" width="30px"><span>业余草</span> 👍（1） 💬（1）<div>每周1、3、5等着老师更新！</div>2019-07-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/23/6c/785d9cd3.jpg" width="30px"><span>Snooker</span> 👍（0） 💬（1）<div>问题1，在用户体验上对301和302基本无感知，刚开始学的时候感觉基本没区别，都是一个location然后跳一下，再深入了解，应用场景不同，301永久跳 http升级https，v2接口升级v3接口等，302的临时跳，实际中好像是有遇到过，针对风险性比较高的活动，设置静态页面，当到达某个阈值后，给用户显示静态页面；不过更多感觉像运维是否遵循开发规范，技术层面问题：文中提到的搜索优化和评论区提到的浏览器针对301的优化
问题2，除留言区提到的未登录状态下的跳转，像是常见的诱导分享链接，是否也是用了重定向来规避风控</div>2024-04-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/28/40/5b/29e00f0b.jpg" width="30px"><span>小雨</span> 👍（0） 💬（1）<div>1.网站改版，用301来把原url的权重转移到新url
2.把http 301到https，把一级域名301到www域名</div>2023-11-19</li><br/><li><img src="" width="30px"><span>Geek_da4d45</span> 👍（0） 💬（1）<div>罗老师，您好！
我对于 307 的描述比较感兴趣：
`307 Temporary Redirect：类似 302，但重定向后请求里的方法和实体不允许变动，含义比 302 更明确；`
但是我查阅了 [rfc](https:&#47;&#47;datatracker.ietf.org&#47;doc&#47;html&#47;rfc7231#section-6.4.7) 文档，文档中只说了适用于 POST 请求，没有对其他方法有描述，我想进一步了解一下您说的这个知识是从哪里获取到的？</div>2022-08-02</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/23/6c/785d9cd3.jpg" width="30px"><span>Snooker</span> 👍（0） 💬（1）<div>301 和 302 实际应该中好像没有怎么区分，公司域名升级从http到https，访问http还是返回了302 . </div>2022-06-16</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/29/b0/d3/200e82ff.jpg" width="30px"><span>功夫熊猫</span> 👍（0） 💬（1）<div>vue-router里所谓的跳转也算跳转，它们跟所谓的服务器跳转有什么区别</div>2021-10-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/1c/a5/226ce8a7.jpg" width="30px"><span>Noir</span> 👍（0） 💬（1）<div>使用重定向的场景：
用电脑访问知乎主页（www.zhihu.com），会用 302 强制转跳到登录页</div>2021-08-07</li><br/>
</ul>