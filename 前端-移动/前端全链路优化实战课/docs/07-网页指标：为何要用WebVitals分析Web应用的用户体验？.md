你好，我是三桥。

对于网页来说，用户行为是一种输入，那什么样的网页“输出”才会更好呢？想象一下，如果你在打开一个页面时，加载过程需要等待很久才出现画面，你还愿意等下去吗？你还会继续想用这样的产品吗？

我想表达的是，网页的反馈速度，对于用户体验至关重要，这也是我们在前端全链路监控中最核心的指标。这节课，我们就一起来学习通过网页指标衡量Web页面用户体验的方法。

我们先从前端最常用的分析方法开始。

## 使用 Performance 指标分析用户体验的局限性

对于大部分Web开发者来说，需要做Web性能分析时，第一时间肯定会想到用window.performance接口获取一个Web页面的性能基础数据，然后再分析，就完事了。

但是不是真的能解决问题呢？不能。

你可以看下下面这张图，Performance接口记录了一次网页加载全过程中每个生命周期的指标。这些指标，都是以时间戳来表达每个生命周期的时间位置的。

![图片](https://static001.geekbang.org/resource/image/5b/f7/5bb743e499e273e3183d786a0c8341f7.png?wh=1152x420 "图来源自W3C：https://www.w3.org/TR/navigation-timing-2/")

假设，即使我们获取到了这些时间戳，它们真的能帮助我们判断Web应用存在哪些性能问题吗？

首先，performance.timing获取每个周期阶段的时间戳，都只是网页加载过程中每个生命周期的时间节点，对于我们分析Web应用性能帮助还是有限的，毕竟我们还要通过这些时间戳去计算真正需要的指标值。
<div><strong>精选留言（5）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/2b/86/73/5190bbde.jpg" width="30px"><span>苏果果</span> 👍（0） 💬（0）<div>完整源码入口：
https:&#47;&#47;github.com&#47;sankyutang&#47;fontend-trace-geekbang-course</div>2024-07-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/2b/86/73/5190bbde.jpg" width="30px"><span>苏果果</span> 👍（1） 💬（1）<div>各位同学大家好～我是这门课程的编辑同学。

课程将于五一假期暂停更新，在5月6日（周一）00:00恢复更新。

假期归来之后欢迎继续追更～预祝大家五一假期快乐！</div>2024-04-30</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/38/49/2f/590142fb.jpg" width="30px"><span>JuneRain</span> 👍（0） 💬（1）<div>利用 performance API获取到的生命周期时间戳，从而计算出来的TCP链接时间，DNS解析时间数值很大，是因为你没给要统计的资源的响应头加上 Timing-Allow-Origin 字段，导致 connectStart ，transferSize 等字段值一直为0

https:&#47;&#47;developer.mozilla.org&#47;en-US&#47;docs&#47;Web&#47;HTTP&#47;Headers&#47;Timing-Allow-Origin</div>2024-05-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/44/5e/a882dc64.jpg" width="30px"><span>北国风光</span> 👍（0） 💬（0）<div>请教个问题，页面上使用了大量的异步组件，根据条件渲染不同的异步组件，每次FCP的时间都不同，是不是针对异步加载组件的场景，FCP无法衡量加载性能？</div>2024-09-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/61/c1/93031a2a.jpg" width="30px"><span>Aaaaaaaaaaayou</span> 👍（0） 💬（0）<div>https:&#47;&#47;web.dev&#47;articles&#47;tti 从这里的定义来看 TTI 应该比 FCP 更靠后呀</div>2024-09-14</li><br/>
</ul>