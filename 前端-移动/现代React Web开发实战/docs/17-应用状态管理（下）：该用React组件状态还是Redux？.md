你好，我是宋一玮，欢迎回到React应用开发的学习。

上节课我们学习了应用状态对于JS前端应用的重要意义，也学习了以Redux为代表的应用状态管理框架，介绍了Redux的核心概念 `action` 、 `reducer` 、 `store` ，以及它单向数据流的本质。从使用角度，我们介绍了Redux封装库Redux Toolkit的用法，强调了它对Redux开发的简化。

不知你发现没有，上节课除了作为扩展内容的MobX和XState，我们完全没有用到React。请你放心，当然不是我忘了这个专栏的主题，而是我希望你能以更纯粹的视角，去了解应用状态管理这个领域知识，不会因为React的概念导致先入为主。

这节课，我们会把Redux与React结合起来使用，看看它能为React的状态管理带来什么好处，同时也要探讨什么时候该用Redux，什么时候用React内建的state，更或者，是否可以混用两种状态管理。

## React应用中有哪些状态？

我们在开发React应用时，会用到各种状态，大致可以分类成三种：业务状态、交互状态以及外部状态。

**业务状态是指与业务直接相关的状态，这些状态理论上剥离UI也可以使用**，比如在单元测试中、Node.js环境中等等。
<div><strong>精选留言（4）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/21/69/79/b4132042.jpg" width="30px"><span>🐑</span> 👍（10） 💬（1）<div>老师提到了路径依赖这个概念，说明老师平时的知识储备是不局限于技术领域的。学习了，向老师看齐～</div>2022-10-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/72/89/1a83120a.jpg" width="30px"><span>yihang</span> 👍（1） 💬（2）<div>还有个问题我想提前问一下老师：最近使用了react router browserrouter模式，同时用懒加载实现动态路由，但页面跳转之间会有明显的闪烁。换成hashrouter能好一些，但同样有肉眼可见的闪烁，不知这个问题有没有较好的解决方案？</div>2022-10-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/72/89/1a83120a.jpg" width="30px"><span>yihang</span> 👍（4） 💬（0）<div>希望讲讲redux异步数据的处理。为什么它的api设计的如此复杂，感觉mobx就简单直白很多</div>2022-10-25</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/c9/f9/39492855.jpg" width="30px"><span>阿阳</span> 👍（1） 💬（0）<div>老师，对于外部状态，感觉还不太懂，能多举几个例子吗</div>2023-02-02</li><br/>
</ul>