你好，我是蒋宏伟。

对核心渲染流程的持续迭代和优化，是 React Native 能够广受欢迎的重要原因之一。

Fabric 是 React Native 新架构渲染器的名字。今天，这一讲我不仅要给你介绍 Fabric 渲染器的核心技术原理，更想让你通过渲染器的演变升级过程，了解该过程中 React Native 技术团队每次大升级背后的思考过程。希望这些优秀框架背后的升级思考，以及对技术极致追求的精神，能够给你带去启发。

为了便于你理解 Fabric 新渲染器是如何演变而来的，我会先和你介绍一个假想的简化版渲染器，接着再带你回顾 React Native 老架构渲染器的工作原理，最后再告诉你 Fabric 新架构渲染器是如何设计的。

## 简版渲染器

时至今日，在 React Native 开源之初的宏大愿景依旧打动着我：将现代 Web 技术引入移动端（Bringing modern web techniques to mobile）。

Web 开发历史悠久，沉淀了诸多优秀实践和基础设施。随着 React Web 框架的出现，将现代 Web 中积累的开发理念，以及语言、框架、规范和生态等引入移动端，统一各端基础设施，必然能够整体降低移动端学习和开发成本。这是该理念如此打动我的原因。
<div><strong>精选留言（7）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/10/61/c1/93031a2a.jpg" width="30px"><span>Aaaaaaaaaaayou</span> 👍（2） 💬（2）<div>为什么 Fiber Tree diff 完后还要再Diff Shadow Tree?</div>2023-02-08</li><br/><li><img src="" width="30px"><span>Geek_1de763</span> 👍（1） 💬（0）<div>所以新架构应用6讲没了？
</div>2023-05-02</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/37/2e/02/7f151e08.jpg" width="30px"><span>听说昵称太长了躲在树后面会被别人看见的</span> 👍（0） 💬（1）<div>老师你好，有个新架构的问题想请教下，TurboModule 和 Fabric 怎么向 JS 端发送消息？我把公司应用升级到 0.71.8 并开启新构架后折腾了三天最终无奈退回到老架构了，TextInput 不可用、触摸事件也乱了，这些都通过 ref 操作和自定义封装触摸组件解决，但是最困惑我的问题是 TurboModule 和 Fabric 怎么发送消息给 RN 端？官方文档翻遍了没看到相关介绍，还有原生代码在新构架只能解耦出来做成单独的 NPM 包吗，我们大量老构架的原生组件都是直接在 Android&#47;IOS 工程下写的，没办法解耦出来成单独 NPM 包。</div>2023-05-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/48/c3/04de5d84.jpg" width="30px"><span>jing</span> 👍（0） 💬（0）<div>+催更</div>2023-05-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/48/c3/04de5d84.jpg" width="30px"><span>jing</span> 👍（0） 💬（0）<div>催更</div>2023-05-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/21/3c/55/74844d08.jpg" width="30px"><span>大大小小</span> 👍（0） 💬（0）<div>怎么不更新了？</div>2023-05-09</li><br/><li><img src="" width="30px"><span>Geek_781ef0</span> 👍（0） 💬（0）<div>老师，还剩3讲，剩下的题目会是什么？催更！</div>2023-02-26</li><br/>
</ul>