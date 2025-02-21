你好，我是宋一玮，欢迎回到React应用开发的学习。

上节课我们不再依赖CRA，从零开始用 Vite 搭建了一个新的React项目，并把 oh-my-kanban 的代码迁移了过来，熟悉了与 React 应用代码直接相关的工程化概念和工具。其中，我们也重点介绍了代码静态检查工具的用法和部分规则。结合从第3节课以来学到的知识，到现在你已经基本可以独立开发小型React项目了。

从这节课开始，我们将进入新的模块，学习一些大中型React项目中会用到的技术和最佳实践，尤其会重点讲解当你融入一个前端开发团队时，需要的开发工作思路和方式的转变，这会帮你更从容应对团队协作。

这节课的主要内容是不可变数据。

没能以正确方式变更数据，是React开发中产生Bug的重要原因之一。请你回忆一下在[第3节课](https://time.geekbang.org/column/article/553817)末尾，在更新 `todoList` state时留下的伏笔： `setTodoList(currentTodoList => [newCard, ...currentTodoList])` 为什么不能写成 `todoList.unshift(newCard)` 呢？当学习了不可变数据的原理和实现，你将对React的渲染与数据之间的关系更有把握。

下面开始这节课的内容。
<div><strong>精选留言（3）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/13/1f/08/14642f9e.jpg" width="30px"><span>相望于江湖</span> 👍（1） 💬（1）<div>我有个疑问，不可变其实就是把对象、数组深度克隆一遍。
深度克隆这个操作应该比深度比较更耗时吧，而且对象克隆来克隆去，难道不会造成内存暴涨，甚至泄露吗？</div>2023-09-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/19/64/6f2b7b86.jpg" width="30px"><span>01</span> 👍（0） 💬（3）<div>可能需要deepFreeze。 本身存在冻结不应该冻结对象的风险
preact给自己乃至react 提供了 signals。 用到了proxy</div>2022-10-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/83/c9/5d03981a.jpg" width="30px"><span>thomas</span> 👍（0） 💬（0）<div>保存一份数据的多个版本变得可行。
--------------------------------&gt;
没理解这句话，即使是可变的数据，也能实现一份数据多个版本。麻烦老师具体解释下</div>2023-12-29</li><br/>
</ul>