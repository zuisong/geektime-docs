你好，我是于航。

作为“应用篇”的最后一节课，我们来一起看看自 Wasm MVP 标准发布之后（2017年3月）的这三年时间里，Wasm 还有哪些行进中的后续标准正在被设计和实现？这些标准将会分别影响整个 Wasm 生态的哪些组成部分？借助于这些新的标准，现有的 Wasm 应用能否被进一步得到优化？Wasm 这项技术能否被应用到更多、更广的领域中呢？相信在学习完这节课后，对于上面这些问题，你会有着进一步的感悟。

实际上，在我们之前课程里所讲到的那些 Wasm 案例，均是在现有 MVP 标准所提供能力的基础上进行构建的。但 MVP 标准并不代表着 Wasm 的最终版本，相反，它正是标志着 Wasm 从枯燥的技术理论走向生产实践的一个起点。

## MVP

MVP（Minimum Viable Product）的全称为“最小可行产品”，这个我们之前也提到过。既然是“最小可行产品”，那就意味着在这个版本中，包含有能够支持该产品正常使用的最少，同时也是最重要的组成部分。对于 Wasm 来说，便是我们之前在“核心原理”篇中介绍的那些内容。

那在这里，让我先来总结一下，Wasm 在 MVP 标准中都定义了哪些“功能”？

### 可编译目标

在本课程的第 [03](https://time.geekbang.org/column/article/283436) 讲中，我们曾介绍过，Wasm 实际上是一种新的 V-ISA 标准。“ISA” 我们都知道，翻译过来即“指令集架构”。同 X86、ARM 等其他常见的物理指令集架构类似，这意味着我们可以将诸如 C/C++ 等高级静态编程语言的代码，编译为对应这些 (V)ISA 的机器代码。
<div><strong>精选留言（4）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/21/25/23/9acf29cc.jpg" width="30px"><span>慌慌张张</span> 👍（2） 💬（1）<div>您好老师，请问一下mvp是最小稳定版，post-mvp是什么呢？还有就是这些新特性要是可以使用了，我们是不是要更新一下编译工具emscripten呀</div>2020-11-02</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1b/99/f0/280891d5.jpg" width="30px"><span>黄东</span> 👍（0） 💬（1）<div>显卡这一块好像没有讲到</div>2022-04-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/57/4f/6fb51ff1.jpg" width="30px"><span>奕</span> 👍（11） 💬（0）<div>wasm 所有的提案可以在这里看到 https:&#47;&#47;github.com&#47;WebAssembly&#47;proposals，然后浏览器的支持情况或者 node 的支持情况 可以使用这个 npm 库进行判断： https:&#47;&#47;github.com&#47;GoogleChromeLabs&#47;wasm-feature-detect</div>2020-10-07</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/26/83/a0/84e00635.jpg" width="30px"><span>ROME</span> 👍（0） 💬（0）<div>要走的路还很长。</div>2021-07-18</li><br/>
</ul>