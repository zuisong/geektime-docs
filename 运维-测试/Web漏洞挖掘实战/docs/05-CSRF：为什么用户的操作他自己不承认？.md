你好，我是王昊天。

想象你是个青春阳光的精神小伙，和女神小美青梅竹马，培养了十几年的感情。眼看着就要抱得美人归时，半路杀出了个男二号，成了你的竞争对手。有一天你们恰好在一起聚会，男二号趁你上厕所，用你的手机给小美发了微信。

“小美，你闺蜜真好看，可以介绍给我吗？”

你回来时，小美大骂了你一通，然后生气地摔门而去。

在这个故事里，男二就通过他的行为完成了一次CSRF。

## CSRF

CSRF的全名是Cross-Site Request Forgery，中文名称是跨站点请求伪造，简单来说，**就是让Web应用程序不能有效地分辨一个外部的请求，是否真正来自发起请求的用户**，虽然这个请求可能是构造完整、并且输入合法的。

和前几节课程中学习过的漏洞相比，CSRF有自己的漏洞名称，明显是一个更为细分的漏洞类型，而非一个漏洞类别。它作为一个独立的细分漏洞类型，值得我们单独进行探讨，说明影响力是足够大的。

扩展开讲一讲，当一个Web应用在设计过程中没有充分考虑来自客户端请求的验证机制时，就可能会遇到CSRF问题。站在攻击者的视角来看，他可以通过一个URL、图片加载或者XMLHttpRequest等方式，让用户触发一个自动化请求发送行为，这个请求在Web Server接受时会被认为是合法的。
<div><strong>精选留言（7）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/24/7e/73/a5d76036.jpg" width="30px"><span>DoHer4S</span> 👍（5） 💬（1）<div>Samesite Cookie 是一种JavaScript技术，因此需要在启用JavaScript的浏览器才可以使用该技术；

“双重Cookie” 和 “Samesite Cookie” 都需要在HTTPS应用协议下使用；

Samesite Cookie 是 HTTP 响应头 Set-Cookie 的属性之一，用于声明该Cookie是否仅限于第一方(首次发起请求的客户端)或者同一网站的后端上下文(后端设置该Cookie的失效时间，在这个失效时间内任意客户端进行通信使用该Cookie是合法的)。

Samesite 支持三种参数形式，因为该参数是一个配置项，事实上是对 “Cookie&#47;Set-Cookie”  中的Cookie信息的使用进行规范，这种规范是对浏览器的功能进行规范的：

- “Lax” ： Cookies允许和顶级导航一起发送，这种方式就是跨域请求，即支持第三方搜索引擎的GET请求，支支持三种情况：链接、预加载请求、GET表单；

- “Strict”： Cookies只会在第一方的上下文发送，不会与第三方的网站发起的请求一起发送，只有当前网页的URL 与 请求目标一致才会带上Cookie；

  举一个例子，在一个网站上假设有两条外链，第一条外链是QQ的链接，允许携带Cookie(Samesite=Lax)，一条 Github 不允许携带Cookie(Samesite=Strict)；则在这个网站单击链接进行跳转之后，如果你之前已经同时登录了QQ和Github，Github网站会要求你重新输入信息登录；

- “None”： 不对 Cookies 进行任何限制 - 非常地不安全，无法防范CSRF攻击；

Samesite Cookie 和 双重Cookie 两者技术的区别：

- 根本区别： 
  + Samesite Cookie 技术限制的是使用Cookie的范围，即其作用是：可以阻止第三方滥用Cookie，即上述所述对URL发送请求能否携带Cookie；
  + 双重Cookie 的技术是：用户访问页面（拥有特定的域名），注入一个Cookie，该Cookie不是由后端决定的，是由前端随机生成的，提交给后端进行存储；当前端重新进行请求时，重新发送Cookie通过URL参数，后端进行验证是否与第一次访问相同，相同允许，不相同拒绝；
- Samesite 缺点：
  - 如果一个网站有多个子域，那么主域的Cookie无法被携带到子域；
  - Lax 下还有存在CSRF攻击的可能性的，如果设置为 Strict，那么用户体验不好；
- 双重 Cookie 缺点：
  - 占用 Cookie的额外空间，URL额外空间；
  - XSS 如果获取到客户端的Cookie那么就会失效；
  - 无法做到子域隔离

</div>2021-12-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/89/5b/d8f78c1e.jpg" width="30px"><span>孜孜</span> 👍（2） 💬（2）<div>下面是我的理解，理论上，在现代浏览器下，cors完全可以防止csrf，因为永远可以校验origin。。但是如果使用img tag浏览器就不会发送origin header(这是html 设计的失误)，这样服务器就没办法知道这是跨域请求，然后在恶意网站在监听img onload事件就可以知道资源是否加载成功。虽然无法拿到非img的数据，但是这样就可以判断用户是否登陆某些网站或者判断用户是否在企业内网etc。。更严重甚至可以利用img标签请求json数据并通过cpu的bug，拿到这个json数据。 这就是为什么在破坏web兼容性的前提下，新加samesite cookies的原因，让跨域请求无法默认带cookies，这样就避免了csrf。</div>2021-12-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/26/eb/d7/90391376.jpg" width="30px"><span>ifelse</span> 👍（1） 💬（0）<div>学习了，将校验进行到底。</div>2023-03-06</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/de/9a/bf7634a3.jpg" width="30px"><span>E-N</span> 👍（1） 💬（1）<div>老师在 MiTuan 里放的靶机似乎没有安装 nc，无法最终复现漏洞，不过自己搭建一下环境也不麻烦。</div>2022-01-15</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/26/eb/d7/90391376.jpg" width="30px"><span>ifelse</span> 👍（0） 💬（0）<div>&lt;script&gt;
    function attack()
    {
        form.email = &quot;attacker@example.com&quot;
        form.submit();
    }
&lt;script&gt;

&lt;body onload = &quot;attack()&quot;&gt;
    &#47;&#47; ...
&lt;&#47;body&gt;

这段攻击代码不是很理解，页面加载函数里form.submit()；
提交到哪里去?表单在哪里?提交地址在哪里？</div>2023-03-06</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/be/29/4302f98b.jpg" width="30px"><span>人类幼仔</span> 👍（0） 💬（0）<div>请教老师，本域是怎么发生csrf攻击的呢</div>2022-11-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/50/70/6856fd0f.jpg" width="30px"><span>孤雁独鸣</span> 👍（0） 💬（0）<div>老师有没有h5静态代码扫描疑似漏洞的开源工具呢，要不然漏洞挖掘也不应该一直人肉找</div>2022-02-28</li><br/>
</ul>