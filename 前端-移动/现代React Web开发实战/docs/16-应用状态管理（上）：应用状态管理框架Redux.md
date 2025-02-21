你好，我是宋一玮，欢迎回到React应用开发的学习。

上节课我们学习了不可变数据，了解了不可变数据对React的重要意义，然后学习了用 `React.memo` 创建具有更佳性能的纯组件。最后介绍了在JS中实现不可变数据的几种方式，除了我们在`oh-my-kanban` 中的手工实现，还有Immutable.js和Immer这些开源框架。

接下来我们会用两节课的时间，学习React的应用状态管理。你也许已经胸有成竹了：“应用状态，不就是 `useState` 吗？已经很熟悉啦。”

很高兴你有这份自信，不过我们上面提到的应用状态管理的学习，是一个概念到框架再到具体案例的过程。首先应用状态管理是一个前端领域的概念，这节课我们会先来看看它是解决什么问题的，然后来学习目前仍然最流行的应用状态管理框架Redux，了解它的用法和设计思想。

这里也提前做个小预告，在下节课我们会进一步讨论什么情况下使用React的state，什么情况下使用Redux，并举一些实际的例子。

下面开始这节课的内容。

## 什么是应用状态管理？

我们先看**应用状态（Application State）**。理论上，一个应用在运行的时候内存里所有跟它有关的数据都可以称作是应用状态，但实际上，这远远超出了应用开发者需要关注的范围。
<div><strong>精选留言（5）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/14/4f/39/791d0f5e.jpg" width="30px"><span>学习前端-react</span> 👍（0） 💬（1）<div>请问：“React.memo 创建具有更佳性能的纯组件”。对于目前创建的组件来说是不是都可以包上memo。收益是大于成本。</div>2022-10-25</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/09/c2/4e086a4b.jpg" width="30px"><span>demo123567</span> 👍（3） 💬（0）<div>redux的作用有点像redis ，发布订阅模式，缓存各类状态。难道开发者是后端转的前端吗</div>2022-10-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/13/8b/a161ae71.jpg" width="30px"><span>Gn</span> 👍（1） 💬（0）<div>1.useReducer+Context可以复制Redux流程，更加轻量；Redux对频繁state更新做了优化；
2.redux devTools，state改变很清晰，使用很方便；
让望补充
</div>2022-10-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/96/87/bbdeb4ee.jpg" width="30px"><span>杨永安</span> 👍（0） 💬（0）<div>新手学习，遇到跨组件状态管理问题。context 似乎只能传递一个对象，多个数据，需要在根节点上添加多层 Provider，不太方便。

看到了 redux，恍然大悟。但是写到后来模板代码太多了，还好有 redux-toolkit。

另外，Recoil 感觉更加简洁。老师怎么看这个库？
https:&#47;&#47;recoiljs.org&#47;zh-hans&#47;docs&#47;introduction&#47;getting-started&#47;</div>2023-03-16</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/13/8b/a161ae71.jpg" width="30px"><span>Gn</span> 👍（0） 💬（0）<div>1.useReducer + Context 可以复制Redux状态流程，更轻量；Redux在多次状态更新有优化</div>2022-10-28</li><br/>
</ul>