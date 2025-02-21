你好，我是蒋宏伟。

作为一名程序员，你是否有过看底层源码深入学习 React Native 新架构冲动？但冲动过后，你是否又因为源码太多、太难，而放弃了呢？

的确，React Native 从 2015 年开始开源，至今已经 8 年了，经历了 70 个版本的迭代，最新的新架构源码，代码量极大、功能模块极多、模块之间的关系也极其复杂。但其实只要我们掌握正确的方法，读源码远没有你想象的那么难。

今天，我就给你介绍我常用的读源码的三个方法，分别是“时光机”、“找线头”和“鸟瞰图”，并以第一版React Native源码为例，教你如何通过读源码，一步一步理解React Native新架构。

## 时光机

我的第一招叫做“时光机”。“时光机”是什么意思呢？

React Native 官方的每篇博客都有发表时间，每行代码都有 git 的版本记录，我把阅读过去某个时间节点的文章和代码的方式，叫做坐着“时光机”去学习。

React Native 项目，经历了 8 年的开源和发展，从0.1.0版本迭代到0.70.0，已经从一棵只有主干的小树苗，长成了有多根树枝的大树了。现在的新架构就包括了 JSI、Fabric、TurboModule、CodeGen、Herems、Metro、Yago 等模块。
<div><strong>精选留言（3）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/16/ce/24/bfd04641.jpg" width="30px"><span>ZouLe</span> 👍（0） 💬（1）<div>捉一个typo: &quot;现在的新架构就包括了 JSI、Fabric、TurboModule、CodeGen、Herems、Metro、Yago 等模块。&quot;</div>2022-09-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/ce/24/bfd04641.jpg" width="30px"><span>ZouLe</span> 👍（6） 💬（0）<div>捉一个type: &quot;现在的新架构就包括了 JSI、Fabric、TurboModule、CodeGen、Herems、Metro、Yago 等模块。&quot; 这里 Yago 应该是 Yoga， Herems 应该是 Hermes。</div>2022-09-09</li><br/><li><img src="" width="30px"><span>Geek4471</span> 👍（3） 💬（1）<div>React Native最初选择使用Bridge消息队列的形式实现JavaScript和Native的双向通信，而不是直接使用JSI（JavaScript Interface）的主要原因是为了提供跨平台的兼容性和可扩展性。以下是一些原因：
1. 跨平台兼容性：React Native的目标是实现跨平台开发，使开发人员能够在多个平台上共享代码。通过使用Bridge消息队列，React Native可以在不同的平台上实现JavaScript和Native之间的通信，而不需要依赖特定平台的底层接口。
2. 可扩展性：Bridge消息队列提供了一种灵活的机制，可以轻松地添加新的Native模块或功能。开发人员可以通过编写Native模块并注册到Bridge中，然后在JavaScript中调用这些模块来扩展应用程序的功能。
3. 性能优化：使用Bridge消息队列可以实现异步通信，避免阻塞JavaScript线程。这对于处理复杂的UI操作或大量数据传输非常重要，可以提高应用程序的性能和响应速度。
4. 社区支持：在React Native刚开始发展时，JSI还没有成熟和广泛采用。使用Bridge消息队列作为通信机制更符合当时React Native社区的技术栈和开发习惯。
尽管Bridge消息队列在一些方面存在一定的性能开销和限制，但它为React Native提供了一种可靠且跨平台的通信机制。随着React Native的发展和JSI的成熟，开发人员现在可以选择使用JSI来直接与Native进行交互，以获得更高的性能和更多的灵活性。</div>2023-07-28</li><br/>
</ul>