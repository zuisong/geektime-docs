你好，我是宋一玮。欢迎回到React组件的学习。

上节课我们从前端组件化这个概念开始，学习了React组件的层次结构，并用第三节课的React项目演练了组件拆分，引出了React拆分组件的基本原则，也顺带着提出React组件树的本质是元素树。

上节课的内容是比较多的。如果你有做过上节课的思考题，我仍然有些好奇，课上学到的内容是不是足够你完成题目。如果你顺利交卷那你真是很棒！当然，做题时遇到些难题也没关系，在这节课我会延续上节课的思路，继续讲React组件，重点会落在React组件的渲染机制上。

这节课会涉及一些React的底层原理，可以为你解答如下问题：

- 为什么我需要关心React组件的渲染机制？
- 为什么数据变了，但组件没重新渲染？
- 为什么数据没变，但组件也重新渲染了？

后两个问题本身都可以作为第一个问题的答案。至于后两个问题，掌握React组件重新渲染的时机，避免无效的重新渲染都需要学习React组件的渲染机制。

我们现在开始这节课的内容。

## 虚拟DOM

虚拟DOM（Virtual DOM）是前端领域近几年比较出圈的一个概念，是相对于HTML DOM（Document Object Model，文档对象模型）更轻量的JS模型。在React、Vue.js、[Elm](https://elm-lang.org/) 这样的声明式前端框架中，都包含了虚拟DOM。
<div><strong>精选留言（14）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/11/d1/27/1e0e30cf.jpg" width="30px"><span>Dearest</span> 👍（21） 💬（1）<div>想多了解 React Fiber， 想了解React18对实际开发的影响</div>2022-09-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/4f/39/791d0f5e.jpg" width="30px"><span>学习前端-react</span> 👍（5） 💬（1）<div>思考题一：也是猜测。对于相同的标签元素，可能变化的就是children 和 attr。那attr来说，因为到最后都会生成一个对象去描述jsx，所以这些attrs可以做对比 简单类型可以直接做对比，引用类型可以比较是否同一个引用。类似浅拷贝。
判断数据类型目前比较常规的是通过object prototype to string call 去判断。
这时同样有一个问题如果父组件的属性发生变化 那么子组建会重新渲染吗？</div>2022-09-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/b9/d8/92c2b3ab.jpg" width="30px"><span>海华呀</span> 👍（3） 💬（1）<div>1、相同tag，属性修改的实现 应该新旧属性都遍历一遍，遍历旧的因为要移除一些可能存在的事件监听，遍历新的是为了查看属性新增更新情况。
2、尽量不要在JSX中写大量JS语句，对事件的处理，要另外写在函数中，不要直接在JSX中写</div>2022-10-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/17/a8/1e/4ec85e24.jpg" width="30px"><span>joel</span> 👍（2） 💬（1）<div>老师咨询一个问题：
比如一个函数组件：
function A （）{
 return (&lt;span&gt;我是组件A&lt;&#47;span&gt;)
}
是不是只要这个函数执行了，就会生成一个虚拟节点，然后通过diff 算法对比是否需要在真实的dom 结构中更新这个节点。</div>2022-09-15</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1a/b7/d2/2cab8598.jpg" width="30px"><span>里脊</span> 👍（1） 💬（2）<div>当一个组件的状态发生变化，会触发整个虚拟dom的比对吗？</div>2022-10-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/4f/39/791d0f5e.jpg" width="30px"><span>学习前端-react</span> 👍（1） 💬（1）<div>小结一下：
我们讲述了 react的分层。我们在上层使用了jsx ，中间抽象了一层中间层，中间层用来操作底层dom，同时接收上层的UI 。
中间层的操作被称为协调 reconcilation 。react使用了fiber来做这个事。渲染方式是对比两颗fiber树，在对比的过程中寻找最优解，例如我们需要在list中加上key就是如此。
一般协调会有两种方式 推或者拉。轮训造成的开销过大，一般会选择push的方式。
fiber的特点是一个链表的形式所以是可以更好的启动停止渲染过程，降低对于主进程的占用。</div>2022-09-05</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/Q3auHgzwzM7D1LViadpKva62AYrvTy0tHFVaiaUUHFhw3Cqgrvj6kufayoOSJ9IcgL5viamlhhbIwhFtL0vMu35aA/132" width="30px"><span>Geek_0c843c</span> 👍（1） 💬（2）<div>想多了解下react fiber</div>2022-09-05</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/4f/39/791d0f5e.jpg" width="30px"><span>学习前端-react</span> 👍（0） 💬（1）<div>fiber 的理解：
首先不是普遍意义上的 parent-children 结构 而是 parent-child的结构，他是一个链表结构。
Parent-child - child - sibling，即父子关系是单向的，通过sibling完成兄弟之前的链接。
”这棵树可以随时暂停并恢复渲染，

触发组件生命周期等副作用（Side-effect），

并将中间结果分散保存在每一个节点上，

不会 block 浏览器中的其他工作。“
这里引用了文档中描述fiber 简要做了四件事情，但是好像都不太理解他是怎么操作的。</div>2022-09-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/19/64/6f2b7b86.jpg" width="30px"><span>01</span> 👍（0） 💬（1）<div>html元素 主要是判断 props 是否相等， 简单粗暴</div>2022-09-16</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/41/00/ede1aa05.jpg" width="30px"><span>Pioneer</span> 👍（0） 💬（1）<div>想学习下react fiber</div>2022-09-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/30/61/98/0d6b499d.jpg" width="30px"><span>船长</span> 👍（0） 💬（1）<div>思考题 1：以我目前后端的水平我能想到的是：React 先判断属性的类型变没变，如果变了，则直接触发渲染。否则再进行值的对比</div>2022-09-07</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/96/87/bbdeb4ee.jpg" width="30px"><span>杨永安</span> 👍（0） 💬（2）<div>开销一般会在DOM操作和大数据数组等操作上发生吧</div>2022-09-03</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/ztfX2Sjr6Hk3Rtzxhhoib7rKVoSbl53IicJ0awelZdiaIa1A8t7EMbic9ibVY1W72szgNKdYial6JsE2GKChn0Wzt2zg/132" width="30px"><span>阳宝</span> 👍（1） 💬（0）<div>打卡</div>2022-09-04</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTLRCFV3dRy76k26FZXialtnB3UEdgJ8alq0SFlxrGka6j8icsjGgjKnfYxzPeGjG42oumVibibJl31aRg/132" width="30px"><span>Geek_24d08b</span> 👍（0） 💬（0）<div>思考题1：使用Object.is()判断属性是否修改
思考题2：如果render开销很大可能会造成页面卡顿情况，会在造成大开销的代码场景： 1）多余的setState，引起页面重复渲染  2）文章中提到的直接对DOM元素进行操作  </div>2024-03-06</li><br/>
</ul>