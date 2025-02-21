你好，我是王昊天。

不知道你是否听说过木桶效应？我们可以看下图这个木桶，假设它的底面为一整块木板，桶身由15块木板组成。现在，我们需要用这个木桶装尽可能多的水，显而易见，它能装水的数量仅与木板中高度最低的相关。

![图片](https://static001.geekbang.org/resource/image/2f/15/2ff52ecc09928964f2c10b997d71f015.jpg?wh=499x325)

其实对于Web应用的安全性来说，木桶效应同样有效。假设我们的Web应用运用了多个组件，例如Struts、Apache，那么**它的安全强度也是由这些组件中最脆弱的一个所决定**。所以在我们开发一个Web应用时，需要确保每一个组件都不存在已知的安全问题。

那么这节课，就让我们一起学习下Web应用中组件的安全问题吧。

## 易受攻击和过时的组件

首先，我们需要了解Web应用中具有哪些组件。

通常来讲，Web应用一般都包含三个基础组件，**Web应用服务组件、Web数据库组件以及Web客户端浏览器组件**。其中，我们很容易知道Web应用服务器是用于运行Web应用的，Web数据库服务器是用于给Web应用提供需要的数据，而Web客户端浏览器则可以用来展示Web应用返回的内容，同时决定用户与Web应用的交互方式。

其实上述三个基础组件本身，也是由多个组件所构成的，例如Web应用服务器可能会包含Struts、Apache应用等多个组件，而Struts、Apache内部也会包含很多组件。所以组件是一个很灵活的说法，**你可以将它简单地理解为是一个独立功能单元**。
<div><strong>精选留言（3）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/14/34/df/64e3d533.jpg" width="30px"><span>leslie</span> 👍（1） 💬（0）<div>Sec处于Dev和Ops的全生命周期</div>2022-03-07</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/26/eb/d7/90391376.jpg" width="30px"><span>ifelse</span> 👍（0） 💬（0）<div>学习打卡</div>2023-03-31</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/24/7e/73/a5d76036.jpg" width="30px"><span>DoHer4S</span> 👍（0） 💬（0）<div>安全组件比如比较著名的： Apache Shiro - 关于Apache的Web安全组件(CVE-2020-17523) 
漏洞大户： IIS， 基本上一搜一大堆。</div>2022-03-08</li><br/>
</ul>