你好，我是王昊天。

我有次在访问某个页面时，为了下载一些东西，按照页面要求进行了复杂的登录操作。之后我不小心关闭了当前页面，然后再一次点开这个页面，麻木的准备再来一遍复杂的登录操作时，我神奇地发现，面前的Web应用竟然是登录成功的状态，你知道这是怎么一回事吗？

事实上，这个现象是**由Web账户体系的安全设计所导致的**。在这一讲中，我们将会对它进行学习，这样你就能清楚地知道问题的答案啦。下面我们就正式开始今天的学习。

现在几乎每个大型Web应用都会存在账户体系，当我们需要获取Web应用中的某些服务时，Web应用会首先对我们的身份进行认证。所以接下来，我们会从身份认证的相关基础知识入手。

## 身份认证

身份认证的方式有多种，我们可以用最典型的账号密码进行认证，除此之外，我们还可以用cookie（session）、Token、数字证书以及手机验证码来验证。这里你可能对于cookie以及Token会比较陌生，不过不用担心，我们会在后面对它们进行详细的讲解。

![图片](https://static001.geekbang.org/resource/image/23/32/2335013cf74e33de8a633f9e19ed9432.jpg?wh=1530x562)

在这些认证过程中，可以分为两种类型，即**登录过程的认证以及保持登录的认证**。

为了让你更好地理解它们二者之间的区别，我们一起来看一个示例。

![图片](https://static001.geekbang.org/resource/image/36/57/3687aa08f5f4b0d079a5c65101e45757.png?wh=1514x1558)

这是谜团（mituan.zone）的登录页面，我们需要输入正确的用户名、密码以及验证码才能通过身份认证，很明显这是登录过程的认证。
<div><strong>精选留言（7）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/10/25/87/f3a69d1b.jpg" width="30px"><span>peter</span> 👍（2） 💬（0）<div>请教老师几个问题啊：
Q1：session有哪几个方面决定？
同一个用户，用同一个浏览器，用两个tab登录，是一个session吗？
同一个用户，用不同浏览器登录，是一个session吗？
    我的理解：session由这三项决定： 电脑 + 浏览器 + 用户
        这里的“用户”是指用户账号。
        一个用户在多个电脑上登录，算是不同的session。
        一个用户在一台电脑上用不同浏览器登录是不同session。
        同一浏览器但不同tab，是同一个session.
        我的理解是否对？
Q2：session认证的第三步，&quot;auth req&quot;是浏览器发送、但用户无感知的吗？对于用户来说，是直接访问网站资源，不会再去做登录、鉴权一类的操作，对吗？
Q3：现在cookie还被大量使用吗？
    如果各个主流网站还依赖cookie，如果浏览器禁止cookie怎么办？另外，cookie容易被黑客破解吗？
Q4：会话固定攻击图中，第一步login，网站为什么返回sessionid？
    既然攻击者没有用户名和密码，他也没法login啊。
    login失败，网站怎么会返回sessionid？</div>2022-03-03</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/17/27/2a/a914cd3f.jpg" width="30px"><span>若镜</span> 👍（1） 💬（0）<div>请问 sessionid存在cookie中  这个很容易copy走   感觉这个设计很不安全呀？ 为啥目前这是普遍的登陆认证方式呀？多谢</div>2022-03-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/38/ac/0d/791d0f5e.jpg" width="30px"><span>Klaus7</span> 👍（0） 💬（0）<div>为什么将 session 信息放置在 cookie 中会更加安全吗？
1.默认情况下，浏览器会强制同源策略，这意味着一个网站的JS代码不能访问其他域的 Cookie。
2.Cookie 可以具有不同的过期时间，允许应用程序精确控制会话的持久性。</div>2023-09-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/38/ac/0d/791d0f5e.jpg" width="30px"><span>Klaus7</span> 👍（0） 💬（0）<div>会话固定攻击举例，感觉不严谨，受攻击网站通常会返回一个set-cookie（新的jsessionId）给受害者，攻击者此时使用原先的sessionId是无法保持登录的认证的</div>2023-09-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/26/eb/d7/90391376.jpg" width="30px"><span>ifelse</span> 👍（0） 💬（0）<div>学习打卡</div>2023-03-30</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/25/87/f3a69d1b.jpg" width="30px"><span>peter</span> 👍（0） 💬（0）<div>补充一个问题：
Q5：token部分，两个header是什么关系？
    token部分，JSW需要保存在header中；JWT的构成图中，也有一个header。我的理解：前一个header，是指http消息的请求头。后一个header，是JWT内容的构成部分。我的理解对吗？</div>2022-03-03</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/4e/fd/4e8c9743.jpg" width="30px"><span>clay</span> 👍（0） 💬（0）<div>在基于 session 的认证一节的攻击案例中，为什么攻击者没有登录的情况下服务器就会返回一个sessionid？而且这个sessionid还是需要用户登录后才可以通过验证？现实业务真的有这种设计逻辑吗？</div>2022-03-03</li><br/>
</ul>