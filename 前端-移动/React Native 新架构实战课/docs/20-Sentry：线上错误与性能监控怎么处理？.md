你好，我是蒋宏伟。

今天这一讲是我们社区生态篇的最后一讲，我们来聊聊 App 上线之后，如果遇到线上异常，或者是线上性能问题应该怎么处理。

这是我们每个人都会遇到的问题。即便我们的代码在本地测试时没有问题，也有各种上线流程的保障，但由于线上环境的复杂性，也难免遇到各种奇奇怪怪的线上 Bug。我们既然不能完全避免线上 Bug，那么就需要尽可能地减少线上 Bug 对用户的影响，这就要用到线上监控系统了。

我曾经遇到过好几次老板甩来的 Bug，那时候我开发的 React Native 应用也没有接入线上监控，遇到问题只能绞尽脑汁在本地复现和解决。经历过那几次痛苦的 Debug 后，我就打算搞个 React Native 监控系统，从 2020 年开始至今，我一直在参与 58 大前端监控系统的设计和研发，其中 React Native 的监控也是由我负责的。

但是，从头搭建和迭代一个监控系统的成本非常高。如果你有线上错误和性能的监控需求，但公司内部没有现成的监控系统，那我的建议是直接用 Sentry。Sentry 提供了一个[演示 Demo](https://try.sentry-demo.com/organizations/massive-stallion/projects/)，你可以直接打开看看它具体都有哪些功能。

而且 Sentry 的代码是开源的，它既支持你自己搭建，也支持付费直接使用。

如果想自己搭建的话，Sentry 后端服务是基于 Python 和 ClickHouse 创建的，需要自己使用物理机进行搭建，我们的兄弟团队，[转转团队](https://juejin.cn/post/6844904088866390024)就是这么做的。如果想付费使用的话，可以参考 [Sentry 官方文档](https://docs.sentry.io/)先试用一下，如果老板也觉得不错，愿意付费使用，那就省去了自己搭建和维护 Python 服务的麻烦事了。
<div><strong>精选留言（8）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/0f/9d/5f/06671a0d.jpg" width="30px"><span>python4</span> 👍（1） 💬（2）<div>实例代码中用同步的log来简单代替上报, 真实上报是个异步过程, 能讲一下异步上报需要注意的点么? 比如会不会阻塞业务代码运行, 需不需要空闲时间集中上报</div>2022-05-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/e1/71/f0b1f069.jpg" width="30px"><span>郭智强</span> 👍（0） 💬（2）<div>老师您好 ，您上面提到的那一段设置 ErrorUtils.setGlobalHandler 的代码我放到一个tsx 文件后，那这个文件应该在哪个地方 import 进去？我想在初始化的时候，就把这个 handler 设置好</div>2022-05-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/ec/38/409b35f0.jpg" width="30px"><span>魑魅魍魉👽</span> 👍（0） 💬（3）<div>老师您好,
我们也在使用Sentry 的 performance 来监控产线应用的性能, 项目中使用的是React Navigation V5. 同时也是直接使用Sentry提供的 ReactNavigationInstrumentation 作为routingInstrumentation. 但是在Sentry 的 Dashboard上会有很多的Route Change的Transaction. 这是什么原因?</div>2022-05-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/99/87/5066026c.jpg" width="30px"><span>dao</span> 👍（2） 💬（0）<div>写了个简易的基于 sentry 监控的 sdk ，代码 https:&#47;&#47;bit.ly&#47;3xKe1If ，应用 https:&#47;&#47;bit.ly&#47;3NPUHQj。</div>2022-06-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/99/87/5066026c.jpg" width="30px"><span>dao</span> 👍（2） 💬（0）<div>sentry event 本身有很多信息，比如 tags 里有用户ID、设备号、部署环境、发布版号等； contexts 里有 详细应用信息、详细设备信息、操作系统信息 等；在 breadcrumbs 里有很多种类的路径信息。真的很丰富，sentry event 对象示例 https:&#47;&#47;bit.ly&#47;3x84RVp 。（老师的 SDK 里的用户和设备信息对 sentry 上报系统来说，显得有点多余了。 ）
作业二，
- 考虑上传每次正式发布版的 sourcemap ；
- 在需要的时候，使用 Sentry.captureMessage 上报些特别调试信息；
- 在需要的时候，使用 Sentry.setExtras 和 Sentry.addBreadcrumb 增加更多的信息到 sentry event 。</div>2022-06-04</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1e/ed/f1/1ee1d707.jpg" width="30px"><span>三好大兄弟</span> 👍（0） 💬（0）<div>代码11行应该是userId = storage.getString(&#39;userId&#39;)</div>2024-09-02</li><br/><li><img src="" width="30px"><span>Geek_e3ffce</span> 👍（0） 💬（0）<div>老师您好，如何统计页面加载时长，类似web中的onload事件，rn能直接收集到这个时长吗</div>2022-07-04</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/3c/fa/f6e143e4.jpg" width="30px"><span>ad</span> 👍（0） 💬（0）<div>老师你好，Promise异常捕获，通过设置require(&#39;promise&#47;setimmediate&#47;rejection-tracking&#39;).enable(cusotomtRejectionTrackingOptions) 后，发生promise异常时，onUnhandled收不到回调，是什么原因呢？</div>2022-06-24</li><br/>
</ul>