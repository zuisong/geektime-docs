你好，我是宋一玮，欢迎回到React应用开发的学习。

这是专栏的第一次加餐。我和专栏编辑从已上线课程的留言区中，选择了一些具有代表性的问题。这次加餐我们先来讲讲“真·子组件”，以及JSX这一语法糖在React 17版本以后发生的变化。在心愿单里呼声同样比较高的，还有Fiber协调引擎，会放到下节加餐中。

好的，接下来开始我们的加餐内容。

## 真·子组件

在第5节课中，我曾提到过：

> React还流行过一波真·子组件（Sub-components）的设计模式，代表性的组件库有[Semantic UI React](https://react.semantic-ui.com/#sub-components)、[Recharts](https://recharts.org/zh-CN/guide/getting-started)……如果你感兴趣的话，在靠后面的课程中我会讲解一下这种模式的具体实现。

在React领域，一般提到中文“子组件”，指的是Child Component，用于描述在React运行时（Runtime）构建的组件树（元素树）中，组件与组件之间的父子关系。

而这里提到的Sub-components，主要还是在**描述设计时**（Design-time）**组件与组件间的强包含关系**（Containment），而在运行时这些组件之间却不一定是父子关系。所以，把Sub-components直译成“子组件”就不太合适，我就改用了“真·子组件”这种中二的翻译，意在与Child Component区别开。事实上，“附属组件”、“次级组件”、“副组件”也都是可行的名字。
<div><strong>精选留言（3）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/12/96/87/bbdeb4ee.jpg" width="30px"><span>杨永安</span> 👍（1） 💬（1）<div>夜宵支持</div>2022-09-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/17/a8/1e/4ec85e24.jpg" width="30px"><span>joel</span> 👍（0） 💬（1）<div>老师你好，我希望以下心愿单：
1、react 更新机制原理等比较进阶的东西
2、react 自定义hooks 比较经典的案例场景，以及hooks 实现原理
3、对比vue 的原理机制，比如 vue 没有fiber, react 的设计的原理貌似跟vue 不一样，虽然都是有xxx等特点</div>2022-09-23</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/dCfVz7wIUT4fM7zQO3gIwXo3BGodP5FJuCdMxobZ5dXpzBeTXiaB3icoFqj22EbIGCu1xxd1FLo9xic0a2pGnunibg/132" width="30px"><span>风太大太大</span> 👍（0） 💬（1）<div>想听听react的高阶级用法，例如使用高阶组件。
怎么利用react-hooks 进行项目工程化改造，
怎么自己封装合理且好用的自定义hooks</div>2022-09-20</li><br/>
</ul>