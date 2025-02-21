你好，我是陈天。

随着我们的实战项目 KV server 接近尾声，课程也到了收官阶段。掌握一门语言的特性，能写出应用这些特性解决一些小问题的代码，算是初窥门径，就像在游泳池里练习冲浪；真正想把语言融会贯通，还要靠大风大浪中的磨练。所以接下来的三篇文章，我们会偏重了解真实的 Rust 应用环境，看看如何用 Rust 构建复杂的软件系统。

今天，我们首先来学习真实世界下的一个 Rust 项目，应该包含哪些要素。主要介绍和开发阶段相关的内容，包括：代码仓库的管理、测试和持续集成、文档、特性管理、编译期处理、日志和监控，最后会顺便介绍一下如何控制 Rust 代码编译出的可执行文件的大小。

![图片](https://static001.geekbang.org/resource/image/5c/69/5ca01caa4c92ae2b595927b32f5cba69.jpg?wh=1920x1145)

## 代码仓库的管理

我们先从一个代码仓库的结构和管理入手。之前介绍过，Rust 支持 workspace，可以在一个 workspace 下放置很多 crates。不知道你有没有发现，这门课程在GitHub 上的 repo，就把每节课的代码组织成一个个 crate，放在同一个 workspace 中。

![图片](https://static001.geekbang.org/resource/image/2b/62/2bf542e266197e04ededc5c4a6e6cf62.jpg?wh=1920x1134)

在构建应用程序或者服务的时候，我们要尽量把各个模块划分清楚，然后用不同的 crate 实现它们。这样，一来增量编译的效率更高（没有改动的 crate 无需重编），二来可以通过 crate 强制为模块划分边界，明确公开的接口和私有接口。
<div><strong>精选留言（4）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/1e/da/b8/3f80b8a5.jpg" width="30px"><span>交流会</span> 👍（3） 💬（1）<div>没想到rust几行代码的小项目会占这么大空间，哈哈
2.4G	.&#47;queryer
797M .&#47;scrape_url
1.7G	.&#47;httpie
1.9G	.&#47;thumbor</div>2021-12-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/25/02/22/19585900.jpg" width="30px"><span>彭亚伦</span> 👍（1） 💬（2）<div>弱弱地问一句, &quot;加餐|开悟之坡 业界都在用rust干什么&quot;这节课木有了么?</div>2021-12-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/4c/12/f0c145d4.jpg" width="30px"><span>Rayjun</span> 👍（0） 💬（1）<div>很赞，不仅仅是 rust 项目可以参考这个流程，对于其他语言的项目，同样适用</div>2021-12-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/17/ec/f7/d33de1ce.jpg" width="30px"><span>柱子</span> 👍（0） 💬（0）<div>老师，看到您这章提到了：min-sized-rust，并且您在27讲中有提到一些Rust开发前端应用、以Wasm的方式在浏览器里运行的框架，如Yew、Seed；
请问这类Wasm的方案是否有方法编译 Wasm的代码分包，并且以懒加载的方式在用到部分代码的时候再动态加载？</div>2022-05-21</li><br/>
</ul>