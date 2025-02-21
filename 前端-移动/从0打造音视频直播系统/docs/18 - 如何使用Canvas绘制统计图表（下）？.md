Google 的 Chrome 浏览器已经默认支持 WebRTC 库了，因此 Chrome浏览器之间已经可以进行音视频实时通信了。更让人欣喜的是Google还开源了 WebRTC 源码，此举不仅惊艳，而且非常伟大。WebRTC源码的开放，为音视频实时通信领域从业者、爱好者提供了非常好的研究和学习的机会。

虽然“浏览器 + WebRTC”为广大用户提供了诸多便利，但当你开发产品时会发现，在浏览器上调试**媒体流**还是非常困难的。因为媒体通信涉及到了多个层面的知识，而浏览器更擅长的是处理 HTML 页面和 JavaScript 脚本，所以如果用它来分析媒体流的收发情况或者网络情况，就显得很困难了。

为了解决这个问题，Google在它的 Chrome 浏览器中支持了 WebRTC 的统计分析功能，只要**在 Chrome 浏览器的地址栏输入 “chrome://webrtc-internals/ ”**，你就可以看到浏览器中正在使用的 WebRTC 的各种统计分析数据了，而且这些数据都是以可视化统计图表的方式展现在你面前的，从而大大方便了你分析媒体流的效率。

实际上，关于WebRTC统计方面的内容我在前面《WebRTC中的数据统计原来这么强大》的两篇文章中已经做了详细的介绍。而今天我们要讲的主要内容是**如何使用 Canvas 进行图表的绘制**。
<div><strong>精选留言（3）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/0f/4d/fd/0aa0e39f.jpg" width="30px"><span>许童童</span> 👍（0） 💬（1）<div>可以手动开启抗锯齿：
canvas.getContext(&#39;2d&#39;).imageSmoothingEnabled = true;</div>2019-08-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/e5/39/951f89c8.jpg" width="30px"><span>信信</span> 👍（0） 💬（0）<div>https:&#47;&#47;learningrtc.cn&#47;getstats&#47;index.html 打不开了。。。</div>2023-01-16</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/28/75/28/b4f403d3.jpg" width="30px"><span>出逃的晴天小兔纸</span> 👍（0） 💬（0）<div>quadraticCurveTo，绘制二次贝塞尔曲线</div>2021-06-14</li><br/>
</ul>