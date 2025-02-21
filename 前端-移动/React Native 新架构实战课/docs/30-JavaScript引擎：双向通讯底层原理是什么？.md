你好，我是蒋宏伟。

在上一讲中，我们介绍了 React Native 使用 Bridge、Turbo Modules、Fabric Components 实现了 JavaScript 和 Native 之间的双向通讯，而双向通讯离不开我今天要和你介绍的 JavaScript 引擎。

常见的 JavaScript 引擎有V8 和 JavaScriptCore。V8 引擎是 Google 出品的，Chrome 浏览器用的就是它。而 JavaScriptCore 引擎是苹果主导的，它是 Safari 浏览器的引擎。在浏览器下载完成 JavaScript 脚本后，引擎开始执行这些字符串形式的脚本，这些字符串脚本最终会转换机械码，并在硬件上执行。这就是浏览器中页面能够跑起来的原因。

而在 React Native 新架构中，它用的引擎是 Facebook 团队自己研制的 Hermes 引擎。Hermes 引擎和常见的 V8 或 JavaScriptCore 的功能几乎一样，不同的是 Hermes 是为移动端定制的，在启动性能上有不少优势。类似浏览器中的页面，React Native 要跑起来，也离不开 JavaScript 引擎的支持。不仅如此，引擎还是 JavaScript 和 Native 双向通讯的秘密所在。
<div><strong>精选留言（6）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/12/35/f6/fc3881e7.jpg" width="30px"><span>稀饭</span> 👍（0） 💬（0）<div>这跟JSI有什么关系吗？</div>2024-10-03</li><br/><li><img src="" width="30px"><span>极客CEO</span> 👍（0） 💬（0）<div>通过context实现双向通信，那还需要 bridge 么</div>2024-01-17</li><br/><li><img src="" width="30px"><span>Geek_63fd40</span> 👍（0） 💬（3）<div>文中讲的是新架构下的通讯还是旧架构的通讯呢？有点懵。</div>2023-09-04</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/2d/73/417544ee.jpg" width="30px"><span>骑鹤下江南</span> 👍（0） 💬（0）<div>应该是 evaluateScript 不是 evaruateScript 吧</div>2023-08-01</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/96/87/bbdeb4ee.jpg" width="30px"><span>杨永安</span> 👍（0） 💬（1）<div>在原来的v8&#47;jscore引擎中，是不是共享系统本身的引擎？似乎需要将js代码转化为es5等安全的级别。

想知道 Hermes 对ES的版本支持是否依赖手机系统本身？还是独立的一个运行环境。</div>2023-03-08</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTKmR5MWEFXdicmO0S784v3lTqH4BzoKk4YiaDqA9icTFtxL49nR2mFRl5FibQNgWF5bD6mFe30K6zAcCw/132" width="30px"><span>小疯子一头</span> 👍（0） 💬（0）<div>jscontext 不等同于this</div>2023-01-29</li><br/>
</ul>