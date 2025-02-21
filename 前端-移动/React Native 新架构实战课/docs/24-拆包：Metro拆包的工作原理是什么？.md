你好，我是蒋宏伟。

在上一讲我们聊了热更新，今天这一讲我们聊聊热更新中的拆包环节。

热更新和拆包都是大家聊得比较多的话题，通常一个聊得比较多的技术话题都会有一套成熟的技术方案，比如热更新平台就有 CodePush 这样的成熟方案，但拆包却没有一套大家都公认成熟的方案，这也是很奇怪。

业内没有方案，换作以前大家就只能自己“造轮子”了，但去年我们开源了 58RN 的拆包工具 [metro-code-split](https://github.com/wuba/metro-code-split)，你可以直接拿去用。

metro-code-split 是我们团队的赵琦同学写的一个基于 Metro 的拆包工具，它能帮你实现 React Native 的拆包工作。

要知道，无论我们是运行 npm start 启动本地调试，还是运行 npm run-ios 构建应用，底层都会用到 Metro 打包工具。

然而，Facebook 开源的 Metro 打包工具，本身并没有拆包功能。它只能将 JavaScript 代码，打包成一个 Bundle 文件，而且 Metro 也不支持第三方插件，所以社区也没有第三方拆包插件。但当初，我们在阅读 Metro 源码的时候，发现了一个可配置的函数 [customSerializer](https://github.com/facebook/metro/blob/779e724885ec439a317edd7eb4356d01fe8d55a2/packages/metro/src/Server.js#L218-L224)，从而找到了不入侵 Metro 源码，通过[配置的方式](https://github.com/wuba/metro-code-split/blob/fce8183629d07bf34978c0f246c0a91a842ec4e9/src/config/craeteMustConfig.js#L33-L47)给 Metro 写第三方插件的方法。
<div><strong>精选留言（5）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/11/d7/bd/50d98f9e.jpg" width="30px"><span>黑马有点白986</span> 👍（4） 💬（0）<div>先讲讲metro如何配置分包吧，不要一上来就讲原理呀，先run起来。</div>2023-02-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/61/c1/93031a2a.jpg" width="30px"><span>Aaaaaaaaaaayou</span> 👍（4） 💬（0）<div>关于拆包，分享一下我写过的文章 https:&#47;&#47;juejin.cn&#47;post&#47;7056402608298131469?share_token=127d466c-9e55-45f8-9eec-4946389a3ec7

https:&#47;&#47;juejin.cn&#47;post&#47;7067895964794617892?share_token=1a0d8603-a165-4e3e-8445-58d584664897</div>2022-06-20</li><br/><li><img src="" width="30px"><span>Geek_e8d04f</span> 👍（0） 💬（0）<div>把demo下下来，build出来的公共包是0k，出现如下警告，是什么问题？

D:\software\metro-code-split-master\Example&gt;yarn build:dll
yarn run v1.22.21
$ mcs-scripts build -t dll -od public&#47;dll
                    Welcome to Metro!
              Fast - Scalable - Integrated


warning: failed to load the preRefPath correctly! are you setting the &quot;dll.referenceDir&quot; correctly?
warning: failed to load the dllRefPath correctly! are you setting the &quot;dll.referenceDir&quot; correctly?
info Writing bundle output to:, public\dll\_dll.ios.bundle
info Done writing bundle output
warn Assets destination folder is not set, skipping...
                    Welcome to Metro!
              Fast - Scalable - Integrated


warning: failed to load the preRefPath correctly! are you setting the &quot;dll.referenceDir&quot; correctly?
warning: failed to load the dllRefPath correctly! are you setting the &quot;dll.referenceDir&quot; correctly?
info Writing bundle output to:, public\dll\_dll.android.bundle
info Done writing bundle output
warn Assets destination folder is not set, skipping...
Done in 22.03s.</div>2024-01-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/8c/18/7cbc34eb.jpg" width="30px"><span>davidzhou</span> 👍（0） 💬（0）<div>拆包能理解为 webpack4 的 dllplugin 技术吗</div>2023-04-25</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/e1/71/f0b1f069.jpg" width="30px"><span>郭智强</span> 👍（0） 💬（1）<div>老师您好，我用 metro 拆包后，也导出了 sourcemap 文件，想做 RN 里的 js 异常反解，异常的调用堆里是一些数字，具体应该解析呢？我是 iOS开发</div>2022-05-30</li><br/>
</ul>