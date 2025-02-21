你好，我是三桥。

这节课，我将为你介绍实现前端全链路指标数据的第一步，把Web Vitals集成到你的项目。

我们先了解一下前端项目的现状。

近年来，前端开发者从0到1开发新项目，技术选型这方面基本上会将Vue和React作为前端开发首选框架之一，因为它们的模块化开发模式能让我们方便、快速地引入第三方框架或库，为开发更复杂的功能提供强大的后盾。

实际上，前端工程师需要负责的项目并不仅仅局限于Vue和React这两种框架，有些公司还在维护着最传统的旧前端系统，他们仍然使用着古老的技术栈，例如JSP、ASP、PHP以及jQuery等。

那在这种环境下，前端同学应该如何把Web Vital的网页指标应用到不同架构的前端项目上，并实现全链路的分析和体验优化呢？这是一个很有趣的题目。

## 使用Web Vitals的第一步

Web Vitals网页指标是由Google提出的。Google还开发了一套前端SDK，方便前端同学直接通过函数获取网页指标数据。

通常，想要前端项目中使用第三方库可以通过NPM安装依赖或者script链接引入的方式实现。而Web Vitals库正好可以支持这两种方式。

如果前端项目是通过NPM安装依赖，比如Vue或React项目，就可以直接使用npm、yarn或pnpm安装命令来安装Web Vitals。
<div><strong>精选留言（4）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/2b/86/73/5190bbde.jpg" width="30px"><span>苏果果</span> 👍（0） 💬（0）<div>完整源码入口：
https:&#47;&#47;github.com&#47;sankyutang&#47;fontend-trace-geekbang-course</div>2024-07-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/15/7c/cfaaf421.jpg" width="30px"><span>blue</span> 👍（2） 💬（1）<div>三桥老师，这些性能指标，只有在页面刷新的时候才能调用web-vitals回调，那么单页应用的切换怎么监听每个页面的性能指标？</div>2024-05-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/18/ea/05/9976b871.jpg" width="30px"><span>westfall</span> 👍（1） 💬（1）<div>Hello，三桥老师，我感觉开发者更关心的应该是如何通过 web-vitals 的数据分析和解决性能问题，后面会详细讲解吗？</div>2024-05-07</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/18/87/d7/7202a499.jpg" width="30px"><span>小尤</span> 👍（0） 💬（1）<div>老师，
web-vitals Safari 只支持 FCP和TTFB，对于移动端来说，衡量页面首屏渲染是否足够？</div>2024-07-03</li><br/>
</ul>