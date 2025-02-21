你好，我是王昊天。

如今，我们开发一个Web应用需要用到前端和后端两部分。其中前端主要用于数据的渲染，将信息更好地展示给我们；后端则需要获取数据，将合适的信息展示给我们。只有前端和后端一起合作，才能构建出一个优秀的Web应用。

在之前的课程中，我们学习了SQL注入、命令注入这两种注入攻击，它们都是针对Web后端的攻击。那么注入攻击可以针对前端执行吗？答案是肯定的，今天我们要学习的XSS即跨站脚本攻击就是针对前端的攻击方式，下面让我们开始对它的学习吧。

## XSS介绍

XSS即跨站脚本攻击，是OWASP TOP10之一。它的全称为Cross-site scripting，之所以缩写为XSS是因为CSS这个简称已经被占用了。这就是XSS名称的由来。

XSS攻击的原理为，**浏览器将用户输入的恶意内容当做脚本去执行**，从而导致了恶意功能的执行，这种针对用户浏览器的攻击即跨站脚本攻击。它的攻击方式可以分为三种类型，我在下图将它们列举出来了。

![图片](https://static001.geekbang.org/resource/image/71/04/7172a54a6f8ffdc207a8c28e3e474304.png?wh=937x481)

下面让我们进一步来学习它的攻击方式吧。

## 反射型XSS

当应用程序将收到的用户输入，直接作为HTML输出的一部分时，并且未经验证或转义，攻击者就可以输入一些JavaScript脚本，使得受害者的浏览器执行任意的JavaScript代码。这就是反射型XSS攻击，之所以称之为反射型XSS，是因为这种攻击需要用户提供一个恶意输入，然后页面据此进行反射，执行攻击的命令。
<div><strong>精选留言（3）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/24/7e/73/a5d76036.jpg" width="30px"><span>DoHer4S</span> 👍（3） 💬（0）<div>防范XSS的方法有：(1) 严格的输入检测以及对恶意字符的过滤，在接收从用户端输入的进行验证和限制，对非法的字符进行过滤；(2) 对后端传输到前端的输出进行编码，防止其被解析成为动态内容；(3) 使用HTTP Content_Type &#47; X-Content-Type-Options 的字段对非引用HTML和JavaScript的HTTP响应进行限制；(4) 使用 HTTP 协议中的 Content-Security-Policy 来对引用外部的JavaScript资源进行限制；</div>2022-02-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/25/87/f3a69d1b.jpg" width="30px"><span>peter</span> 👍（1） 💬（1）<div>请教老师一个问题啊：
DOM型XSS攻击，只是修改页面，能造成什么危害吗？</div>2022-02-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/26/eb/d7/90391376.jpg" width="30px"><span>ifelse</span> 👍（0） 💬（0）<div>学习打卡</div>2023-03-20</li><br/>
</ul>