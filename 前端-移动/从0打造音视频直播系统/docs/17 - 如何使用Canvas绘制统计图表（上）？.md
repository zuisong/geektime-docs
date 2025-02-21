**Canvas** 是 HTML5 标准中的一个新元素，你可以把它想像成一块“画布”，有了它你就可以在网页上绘制图像和动画了。在HTML5页面中可像使用其他元素一样使用Canvas，如Video标签。为了能够在 Canvas 上绘图，浏览器为此提供了一整套 JavaScript API ，我们将在后面的代码中看到如何使用它们。

实际上，早期要想在浏览器的网页上实现动画效果，需要用到 Flash 技术。但通过Flash实现动画非常繁琐，你必须专门去学习Flash相关的知识。而 Canvas 则完全不用，它就是一个简单的标签，通过几行 JavaScript 代码你就可以很容易地控制它。

Canvas 最早由苹果公司开发的，用在 Mac OS X 的 WebKit 组件中。之后，各大主流的浏览器都对 Canvas 进行了支持，所以它也被纳入到了 HTML5的规范中。

Canvas 支持 2D 和 3D 图像的绘制，并且应用领域非常广泛，基本上涵盖了 Web 图形/图像、视频、动画等领域。我们在网页中经常见到的统计图表、视频应用、网页游戏等等，都是由它来实现的。

## 基本概念和原理

在深入讲解 Canvas 之前，我们先来了解一些基础概念和原理。对于这些基础概念的理解，将会为你学习后面的知识点打下坚实的基础。
<div><strong>精选留言（4）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/0f/fb/2d/e6548e48.jpg" width="30px"><span>tokamak</span> 👍（16） 💬（1）<div>思考题回答：（1）H.264视频解码后通常是YUV420P格式，可以把YUV转成RGBA，调用Canvas的2D上下文接口来逐帧显示视频。（2）或者调用Canvas的webgl上下问，直接渲染YUV数据，也可显示视频。参考案例：https:&#47;&#47;github.com&#47;v354412101&#47;wsPlayer</div>2019-08-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/17/69/65/7622ac40.jpg" width="30px"><span>flying LP</span> 👍（2） 💬（2）<div>有关于渲染的疑惑请老师指导下：
1.理解下来感觉渲染的输出就是非矢量图，类似yuv&#47;rgb格式的像素位图，从而可以让显示器可以直接显示；而音视频通话中播放端解码后都是如yuv的一帧帧图像，应该可以直接显示；那解码后还有渲染的环节吗，作用又是什么？
2.了解到如云游戏这种实时视频传输是通过传送图形指令实现的，如果传送的是纯图形指令，就不需要编解码的环节，而是这样的流程吗：发端视频采集--发端绘图指令--收端解指令--渲染--显示？
新手接触，烦请不吝指导！</div>2020-06-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/4d/fd/0aa0e39f.jpg" width="30px"><span>许童童</span> 👍（4） 💬（0）<div>思考题：
可以通过canvas来解析渲染二进制流，根据视频的编码方式，选择相应的解码方式即可。
这一节讲的内容还是挺基础的，不过正好复习一下。</div>2019-08-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/42/4b/fa2dc54c.jpg" width="30px"><span>LWP</span> 👍（0） 💬（0）<div>纯干货，清晰易懂，点赞 </div>2020-02-25</li><br/>
</ul>