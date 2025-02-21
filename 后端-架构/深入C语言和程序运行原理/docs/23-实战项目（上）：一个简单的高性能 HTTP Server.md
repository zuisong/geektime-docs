你好，我是于航。

在“C 核心语法实现篇”中，通过观察 C 代码被编译后的产物，我们了解了 C 基本语法在机器指令层面的多种具体实现细节。进入“C 工程实战篇”后，通过探索 C 标准库，我们发现了 C 语言为我们提供的更多优秀能力，并同时深入分析了它们的内部实现原理。在此基础之上，通过探讨 C 项目编码规范、代码优化技巧、自动化测试与结构化编译等话题，我们对 C 语言在实际工程中的应用方式又有了更深刻的理解。

但“光说不练假把式”，在本模块最后，就让我们通过实现一个完整的 C 语言项目，来整体回顾之前的学习内容，并尝试在实战过程中体会 C 这门语言的独特魅力。

## 这是一个怎样的实战项目？

俗话说得好，“有趣是第一生产力”。但似乎是从大学时代第一次接触 C 语言开始，我们就对使用这门语言开发的项目有了刻板印象，感觉它们不是枯燥的用户后台管理系统，就是各类晦涩的、与操作系统或硬件深入“绑定”的底层应用。但现实情况却并非如此。正如我在开篇词中介绍的那样，C 语言可以被广泛使用在应用软件、系统软件、编程语言、嵌入式开发等各类场景中。而今天我们要做的项目，便是应用软件类目下服务器应用中的一种，“HTTP Server”。

Server 翻译过来即“服务器”，它在整个互联网世界中，主要用于接收由客户端发来的请求，并在处理之后返回相应结果。而 HTTP 服务器则将可处理的请求类型限定为了 “HTTP 请求”。这类服务器的稳定运行，支撑了我们日常生活中需要与互联网打交道的大多数事务。比如，每一次打开网页，都伴随着浏览器发出 HTTP 请求，服务器返回 HTTP 响应的过程。而这些返回的内容在经过浏览器渲染后被呈现在了你的面前。
<div><strong>精选留言（4）</strong></div><ul>
<li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/DYAIOgq83er5SNsSoiaZw4Qzd2ctH4vtibHQordcLrYsX43oFZFloRTId0op617mcGlrvGx33U8ic2LTgdicoEFPvQ/132" width="30px"><span>Frankey</span> 👍（2） 💬（3）<div>使用epoll？</div>2022-02-16</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/20/3e/e2f1b2af.jpg" width="30px"><span>I WANN BE THAT GUY</span> 👍（0） 💬（1）<div>c语言有尾递归优化吗？</div>2022-02-16</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/23/66/413c0bb5.jpg" width="30px"><span>LDxy</span> 👍（0） 💬（1）<div>使用缓存，把已经计算过的数据缓存起来</div>2022-02-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/a2/4b/b72f724f.jpg" width="30px"><span>zxk</span> 👍（0） 💬（0）<div>使用 reactor 模型</div>2022-04-05</li><br/>
</ul>