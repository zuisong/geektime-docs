你好，我是宋一玮，欢迎回到React应用开发的学习。

上节课我们学习了React组件的生命周期，包括组件层面的挂载、更新、卸载、错误处理四个阶段，以及框架层面的渲染和提交这两个阶段。

在这些阶段中，我们列举了类组件的 `render`、`componentDidMount`、`componentWillUnmount` 等生命周期方法，以及这些方法执行的先后顺序，也对比了函数组件中的Hooks是如何参与组件生命周期的。最后，我们利用 `useEffect` Hooks函数，为 `oh-my-kanban` 项目新加了一个定时更新卡片显示时间的功能。

敏锐的你可能发现了，上节课中你只为函数组件写了Hooks代码，而类组件的生命周期方法仅是介绍而已。还有就是截止目前，`oh-my-kanban`项目里只有函数组件，一个类组件都没有——同样是组件，类组件怎么就被区别对待了呢？其实不是类组件掉了链子，只是函数组件加Hooks这对黄金搭档后来居上，抢了类组件的风头。

接下来你可能还会有疑问：

- Hooks到底是什么？怎么用？
- 函数组件加Hooks可以完全替代类组件吗？
- 还有必要学习类组件吗？

这节课和下节课，我们将学习React自v16.8.0版本加入的Hooks API。当你完成这两节课的学习，相信在掌握Hooks使用的同时，也会对函数组件和类组件在今后React应用开发中的地位，拥有自己的独立判断。
<div><strong>精选留言（9）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/21/69/79/b4132042.jpg" width="30px"><span>🐑</span> 👍（1） 💬（1）<div>你好，我是《现代React Web开发实战》的编辑辰洋，这是👇项目的源代码链接，供你学习与参考： https:&#47;&#47;gitee.com&#47;evisong&#47;geektime-column-oh-my-kanban&#47;releases&#47;tag&#47;v0.9.0</div>2022-09-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/c8/04/fed4c1ad.jpg" width="30px"><span>若川</span> 👍（17） 💬（7）<div>1. React官方文档：Hook 规则
https:&#47;&#47;zh-hans.reactjs.org&#47;docs&#47;hooks-rules.html
1.1 只在最顶层使用 Hook。不要在循环，条件或嵌套函数中调用 Hook。
1.2 只在 React 函数中调用 Hook。不要在普通的 JavaScript 函数中调用 Hook。

因为本质是链表。在各种判断中写 Hook 会导致节点错乱。

2. useRef 中值变化是不会触发重新渲染。useState 中则是会触发渲染。</div>2022-09-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/17/a8/1e/4ec85e24.jpg" width="30px"><span>joel</span> 👍（2） 💬（1）<div>useRef 来代替 useState 吗?
不能，这两个是不同的使用场景，usestate 是可以出发react 的协调过程，useref 不能</div>2022-09-15</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/19/64/6f2b7b86.jpg" width="30px"><span>01</span> 👍（1） 💬（1）<div>18 批处理依托的 它的调度器。 可中断。  进入commit 阶段 则不可中断。  是否只渲染一次 这个不一定吧</div>2022-09-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/23/93/23/6b6feb42.jpg" width="30px"><span>__Initial</span> 👍（1） 💬（1）<div>我想问一下：在state自动批处理时，为什么使用函数参数就可以保证更新函数使用最新的state</div>2022-09-19</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/dCfVz7wIUT4fM7zQO3gIwXo3BGodP5FJuCdMxobZ5dXpzBeTXiaB3icoFqj22EbIGCu1xxd1FLo9xic0a2pGnunibg/132" width="30px"><span>风太大太大</span> 👍（1） 💬（1）<div>1. 函数组件之外的一个普通函数中调用 useState 不会生效
2. 函数组件内部加一个 if 条件语句，在满足条件时才去调用 useState 不会生效。
3. 在这个函数内部调用 useState，再在函数组件内调用这个函数。  useState 不会生效
</div>2022-09-16</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/4f/39/791d0f5e.jpg" width="30px"><span>学习前端-react</span> 👍（0） 💬（1）<div>隔了好久，回答第二个问题。
useRef 的使用方式是用用会存放一个最新的值即 current，每次修改也不会触发当前组件的render，这个应该就区别于 useState 了，因为setState 会触发当前组件的render。</div>2022-09-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/2d/ca/7c/98193e9e.jpg" width="30px"><span>奕晨</span> 👍（1） 💬（0）<div>Hook 在使用中都会有哪些限制：
1. 在函数组件之外的一个普通函数中调用 useState；
    在函数组件之外的普通函数不能调用 useState；
2. 在函数组件内部加一个 if 条件语句，在满足条件时才去调用 useState；
   不能
3. 在函数组件内部定义一个函数，在这个函数内部调用 useState，再在函数组件内调用这个函数。
    不能
只能在React函数中调用Hook。


可以用 useRef 来代替 useState 吗？
不可以，useState会重新渲染，useRef 值发生变化，不会重新渲染。</div>2023-01-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/3b/71/8c/0ee14f99.jpg" width="30px"><span>huangnan0709</span> 👍（0） 💬（0）<div>useState的set函数，无论是使用表达式，还是函数返回值更新状态，都能在下一次重新渲染之前，在set函数的回调函数参数获取最新值</div>2024-05-27</li><br/>
</ul>