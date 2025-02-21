你好，我是于航。

相信现在你已经知道，“WebAssembly” 是由 “Web” 与 “Assembly” 两个单词组成的。前面的 “Web” 代指 Web 平台；后面的 “Assembly” 在我们所熟悉的编程语言体系中，可以理解为“汇编”。

通常来说，汇编语言给人的第一感觉便是“底层，外加高性能”。而这，也正是第一次听说 Wasm 这门技术的开发者们的第一感受。

说到 Web 开发，那我们不得不提到层出不穷的 Web 前端开发框架。以 React、Vue.js 及 Angular 为代表的三大框架的出现，使得 Web 前端应用的开发模式，自 2013 年后便开始逐渐从“旧时代”的 jQuery、Prototype.js 走向了以 “MVVM” 框架为主的“新时代”。

既然我们说 Wasm 起源于 Web，并且它的出现会给未来的 Web 应用开发模式，带来一系列变化。那么，对于这些现阶段在我们日常工作中承担“主力”角色的 Web 前端框架来说，Wasm 会给它们带来怎样的变化呢？未来的 Web 前端开发框架会以怎样的方式与 Wasm 紧密融合呢？

相信这些问题，是每一个 Web 前端开发同学在接触 Wasm 这项技术之后，都会存在的疑问。今天，我们就来看一看，在如今的 Wasm MVP 标准下，对于这些基于 JavaScript 编写的现代 Web 前端框架我们能够做些什么。
<div><strong>精选留言（6）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/17/df/7a/1176bc21.jpg" width="30px"><span>Yarco</span> 👍（4） 💬（1）<div>纯计算的话 貌似也许AI&#47;机器学习可用Wasm? 有这块的内容吗?</div>2020-09-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/57/4f/6fb51ff1.jpg" width="30px"><span>奕</span> 👍（2） 💬（1）<div>目前  wasm 落地情况是怎么样的呢？ 能不能使用与生产环境中的？ 还是只能学习学习，为未来做个知识储备</div>2020-09-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/53/47/3e7618b7.jpg" width="30px"><span>不过落魄</span> 👍（2） 💬（1）<div>恰巧在目前 Wasm 的 MVP 标准中，我们也同样无法直接在 Wasm 字节码中操作 HTML 页面上的 DOM 元素。
是要表达：恰巧在目前 Web 的 MVP 标准中，我们也同样无法直接在 Wasm 字节码中操作 HTML 页面上的 DOM 元素。这一意思吗？</div>2020-09-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1b/5f/1d/20921a78.jpg" width="30px"><span>Yixeu</span> 👍（1） 💬（1）<div>不好意思，我跨国前几章直接看的这一章。请问js glue code 具体是指什么？是要理解为js 开放给wasm 的api么？如果是的话，请问是wasm独有的，还是js统一开放出来的api。如果不是，请问怎么理解或者查阅这个glue code具体有些什么内容</div>2021-01-07</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/2c/c7/89/16437396.jpg" width="30px"><span>极客酱酱</span> 👍（1） 💬（0）<div>尤大的说法：
Not really. At this stage WebAssembly based solutions leads to questionable performance gain (wasm can&#39;t directly touch the DOM), large binary size (which actually reduces load performance), difficulty of debugging during development (can&#39;t just read the stack trace and the source code), significantly larger surface of maintenance (keeping both versions in sync), etc. It&#39;s simply not a reasonable trade-off for existing JavaScript frameworks.
没有。在这个阶段，基于 WebAssembly 的解决方案会导致可疑的性能提升（wasm 不能直接接触 DOM）、大二进制大小（这实际上降低了负载性能）、开发过程中的调试困难（不能只读取堆栈跟踪和源代码）、明显更大的维护表面（保持两个版本同步）等。对于现有的JavaScript框架来说，这根本不是一个合理的权衡。

The only case where a WASM-based frontend framework makes sense is to use a language other than JavaScript (e.g. people who prefer to write UI in Rust or C#).
基于 WASM 的前端框架有意义的唯一情况是使用 JavaScript 以外的语言（例如，喜欢用 Rust 或 C# 编写 UI 的人）。</div>2023-09-04</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/2a/49/62/db480ab6.jpg" width="30px"><span>跳跳</span> 👍（0） 💬（0）<div>一枚使用 Blazor WebAssembly 的同学飘过。</div>2022-01-19</li><br/>
</ul>