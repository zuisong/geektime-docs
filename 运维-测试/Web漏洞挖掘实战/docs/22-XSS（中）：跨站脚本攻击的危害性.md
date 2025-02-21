你好，我是王昊天。

在上一节课程中，我们学习了什么是XSS攻击，并且介绍了XSS攻击的不同种类。在攻击示例的代码中，我们仅仅是让网页弹出一个警告框，看上去XSS攻击并没有什么作用，但实际上，它的危害性是比较大的。你会好奇XSS攻击会造成哪些危害吗？

这节课，让我们一起来深入了解一下。

## XSS攻击的危害

XSS攻击的危害主要包括四种类型，我已经将它们整理在下图中，它们分别是盗取cookie、按键记录和钓鱼、广告植入以及欺骗跳转。

![图片](https://static001.geekbang.org/resource/image/79/28/7947771b79fb81ebdd8309d45e58a028.jpg?wh=856x412)

首先我们来学习具有代表性的XSS攻击利用，盗取cookie，看看攻击者是如何用XSS攻击实现对cookie的窃取。

### 盗取cookie

cookie在英文中的意思为甜品、饼干，不过这里盗取cookie可不是偷饼干的意思哦。在HTTP请求中，cookie代表着登录信息，我们在Web应用登录成功后，服务器端会生成一个cookie。然后服务器端会将这个生成的cookie发送给我们，供我们之后访问的时候使用。

如果攻击者拿到cookie信息了，那他就可以实现登录我们的账号，这是非常危险的，所以我们平时需要保护好我们的cookie信息。

在了解完cookie是什么之后，让我们用一个示例，一起看看XSS攻击是如何获得cookie信息的。
<div><strong>精选留言（3）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/26/eb/d7/90391376.jpg" width="30px"><span>ifelse</span> 👍（0） 💬（0）<div>阔怕，打卡</div>2023-03-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/25/87/f3a69d1b.jpg" width="30px"><span>peter</span> 👍（0） 💬（0）<div>请教老师三个问题啊：
Q1：拿到cookie以后，可以直接访问，并不需要使用“用户名+密码”登录，
        相当于绕过了登录，对吗？
       文中这句话“如果攻击者拿到 cookie 信息了，那他就可以实现登录我们的账号”，
       从这句话来看，好像还需要用“用户名+密码”登录。

Q2：BeEF的Hooked Browsers界面上，192.168.3.102前面的几个“？”是什么意思？
        乱码吗？ 还是有其他含义？
Q3：本专栏所用的软件、脚本等内容，放在一个公共地方了吗？</div>2022-02-15</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/24/7e/73/a5d76036.jpg" width="30px"><span>DoHer4S</span> 👍（0） 💬（0）<div>XSS攻击还可以盗取CSRF TOKEN来进行CSRF攻击；</div>2022-02-14</li><br/>
</ul>