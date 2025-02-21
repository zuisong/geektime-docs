你好，我是宋一玮，欢迎回到React应用开发的学习。

之前提到过，我们会在专栏的留言区选取一些具有代表性的问题，放到加餐里统一讲解。

上次的加餐01我们介绍了“真·子组件”，以及JSX语法糖在React 17版本以后发生的变化。这节加餐我们有且只有一个主题，就是目前留言区呼声最高的，Fiber协调引擎。

首先还是要说明一下，在React 18.2.0中，Fiber的源代码有3万多行（以 `wc -l packages/react-reconciler/src/*[^new].js` 命令统计），要想搞清它的每一行代码都是干什么的，一节加餐是远远不够的。

这节加餐会从原理入手，介绍Fiber内的部分重要模型和一些关键流程，并尽量跟前面课程中学到的React各种概念串联起来，这包括React元素、渲染过程、虚拟DOM、生命周期、Hooks。不求面面俱到，为的是帮助你加深对React框架的理解。

另外请注意，Fiber协调引擎是React的内部实现，无论是否学习它，都不会影响你对React框架的使用。

## 什么是Fiber协调引擎？

正如第6节课讲到的：

> React组件会渲染出一棵元素树……每次有props、state等数据变动时，组件会渲染出新的元素树，React框架会与之前的树做Diffing对比，将元素的变动最终体现在浏览器页面的DOM中。这一过程就称为**协调（Reconciliation）**。
> 
> > 在React的早期版本，协调是一个**同步过程**，这意味着当虚拟DOM足够复杂，或者元素渲染时产生的各种计算足够重，协调过程本身就可能超过16ms，严重的会导致页面卡顿。而从React v16开始，协调从之前的同步改成了**异步过程**，这主要得益于新的**Fiber协调引擎**。
<div><strong>精选留言（6）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/14/4f/39/791d0f5e.jpg" width="30px"><span>学习前端-react</span> 👍（2） 💬（1）<div>感谢宋老师的精彩加餐。目前看下来一餐可能不太够，有点囫囵吞枣的感觉。
</div>2022-09-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/17/a8/1e/4ec85e24.jpg" width="30px"><span>joel</span> 👍（2） 💬（1）<div>要是有视频就更好，老师辛苦了</div>2022-09-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/bc/e3/6267bf06.jpg" width="30px"><span>乐雨</span> 👍（1） 💬（2）<div>没有讲到任务优先级和饥饿问题的处理</div>2022-09-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/4f/39/791d0f5e.jpg" width="30px"><span>学习前端-react</span> 👍（0） 💬（1）<div>请问：修改state 是生成fiber 并 diffing的过程？</div>2022-09-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/81/eb/04c16c3e.jpg" width="30px"><span>silence_wh</span> 👍（0） 💬（0）<div>推荐一篇帮助理解 React 工作流程的文章：https:&#47;&#47;pomb.us&#47;build-your-own-react&#47;</div>2024-04-01</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/e7/20/70a95f94.jpg" width="30px"><span>潮汐</span> 👍（0） 💬（0）<div>这篇加餐结合正文课程第6、8节和文中的图，对渲染、协调有更深的理解。与6、8节正文的图形成互相诠释说明，值得反复对比理解！</div>2023-02-19</li><br/>
</ul>