你好，我是宋一玮，欢迎回到React应用开发的学习。

上节课我们学习了React的事件处理，理解了React事件是标准化封装过的合成事件。在这基础之上，还学习了受控组件和事件冒泡/捕获的概念，并为 `oh-my-kanban` 项目加入了实用的卡片拖拽功能。其间我们也不忘与浏览器原生DOM事件作对比。

到目前为止，包括生命周期、Hooks、事件处理，你已经基本了解了可以在哪些位置编写组件逻辑代码。那么当你在React应用中写了多段逻辑代码后，代码之间是怎么串联起来的？反过来说，怎样才能把每段代码写在它合适的地方，让它们各司其职，支撑应用跑起来呢？

接下来我们会用两节课的时间，把视野从单个React组件中拓展开来，看看**组件与组件之间的分工和交互，**从而帮助你解决刚才提出的问题。

我把这两节课分别称为组件的“面子”和“里子”。这节课的重点，是React的**单向数据流**。当你理解了在React的设计哲学中数据应该如何流转，就会对如何设计props和state了然于心。

在学习概念的基础上，也请你跟随我，从数据流的视角重新梳理早在第5节课就基本定型的 `oh-my-kanban` 各组件，进行一次**大重构：对组件文件进行拆分，并根据需要调整各组件的props和state**。同时我们也会学习React另一个与数据流相关的概念——context。
<div><strong>精选留言（9）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/21/69/79/b4132042.jpg" width="30px"><span>🐑</span> 👍（1） 💬（3）<div>你好，我是《现代React Web开发实战》的编辑辰洋，这是👇项目的源代码链接，供你学习与参考：https:&#47;&#47;gitee.com&#47;evisong&#47;geektime-column-oh-my-kanban&#47;releases&#47;tag&#47;v0.12.0</div>2022-09-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/b9/d8/92c2b3ab.jpg" width="30px"><span>海华呀</span> 👍（4） 💬（1）<div>1、因为一个父组件可能有多个子组件，如果任意子组件都可以修改父组件数据，可能会导致其他子组件受到影响，这样以来会加大开发和debug难度，单向数据流就没这个影响。</div>2022-10-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/30/61/98/0d6b499d.jpg" width="30px"><span>船长</span> 👍（1） 💬（1）<div>有一个细节疑问：在重构 css 时，vscode 中有 4 个选项，宋老师用的是“抽取为模块范围的常量”, 实际效果是将这块代码放到了根目录下。我试了下另一个选项（第一个选项）“抽取为封闭范围的常量”，发现 vsc 将其放到了 KanbanBoard 这个函数的大括号下。
想问下这 2 块有什么区别吗？</div>2022-09-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/19/64/6f2b7b86.jpg" width="30px"><span>01</span> 👍（0） 💬（1）<div>state 其实应该可变可不变的。 变是因为实打实的值变了， 不变是UI在当下不变</div>2022-09-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/9d/c4/13376c14.jpg" width="30px"><span>DullSword</span> 👍（0） 💬（1）<div>1.使数据流向简单清晰，多向可能会带来复杂和混乱。
2.我理解的重构是改进代码，可能是改进代码的结构，也可能是改进代码的运行效率。</div>2022-09-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/30/61/98/0d6b499d.jpg" width="30px"><span>船长</span> 👍（0） 💬（1）<div>所谓重构（refactoring）是这样一个过程：在不改变代码外在行为的前提下，对代码做出修改，以改进程序的内部结构。重构是一种经千锤百炼形成的有条不紊的程序整理方法，可以最大限度地减小整理过程中引入错误的概率。本质上说，重构就是在代码写好之后改进它的设计。
Ref: 《重构》 马丁 福勒</div>2022-09-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/4f/39/791d0f5e.jpg" width="30px"><span>学习前端-react</span> 👍（0） 💬（5）<div>请问：类似于redux 这样的状态管理器也都是基于 context 去实现的吧。</div>2022-09-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/e7/20/70a95f94.jpg" width="30px"><span>潮汐</span> 👍（1） 💬（1）<div>Context.Provider 的 value 值也可以传一个对象进去，但要注意写法，避免在组件重新渲染时反复创建新的对象，比如利用 state 或 useMemo ：
--------------------------------------------------
问下老师，这里说的要避免的写法，是为了单纯避免value值的对象的重复创建，还是说避免重复创建对象防止多余重复渲染啊。试验了一下，文中value值的对象形式，不管哪种形式，对象字面了，state对象值，useMemo值，在状态更新时，子孙组件都会重新渲染。所以我觉得老师这里的意思是 避免每次组件更新渲染时重新创建value值的对象。然而这里，不管是否重新创建value值的对象，子孙组件都会更新渲染。</div>2023-01-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/30/61/98/0d6b499d.jpg" width="30px"><span>船长</span> 👍（1） 💬（0）<div>思考题2: 个人理解重构是为了降低代码耦合度，减少系统的熵，方便后续增补或阅读</div>2022-09-20</li><br/>
</ul>