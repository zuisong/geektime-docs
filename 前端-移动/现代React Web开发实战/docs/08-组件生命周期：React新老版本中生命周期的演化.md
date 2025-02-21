你好，我是宋一玮，欢迎回到React组件的学习。

上节课我们暂时跳出React的核心概念，了解了如何利用 `CSS-in-JS` 技术将React组件的CSS样式也组件化，并以 `emotion` 框架为例，一起改写了 `oh-my-kanban` 项目的部分CSS。

到这里，对于组件的结构和样式，我们已经给予了足够充分的学习和关注。那么接下来我们将用六节课的时间，来学习如何为组件编写逻辑。

组件的逻辑代码应该写在哪里呢？不妨参考一下开源项目React组件库AntD。根据在AntD的v3.26.20版本源代码中统计函数个数，至少有**35%的函数是React生命周期方法**。这就引出了这节课的主题，组件生命周期。

可以说，生命周期一直都是前端技术中的核心概念，React也不例外。在React这里，尤其需要注意的是，**组件生命周期并不等同于类组件的生命周期方法**。

组件生命周期首先是一组抽象概念，类组件生命周期方法和Hooks API都可以看作是这组概念的对外接口。因此，无论是选择函数组件加Hooks，还是在类组件上一条路走到黑，都要学习组件生命周期。

那么这节课我们就先从类组件入手，通过介绍类组件的生命周期方法，带你了解背后的React组件生命周期，然后再从实际出发，讲解对应的Hooks用法。
<div><strong>精选留言（12）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/21/69/79/b4132042.jpg" width="30px"><span>🐑</span> 👍（1） 💬（0）<div>你好，我是《现代React Web开发实战》的编辑辰洋，这是👇项目的源代码链接，供你学习与参考： https:&#47;&#47;gitee.com&#47;evisong&#47;geektime-column-oh-my-kanban&#47;releases&#47;tag&#47;v0.8.0</div>2022-09-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/4f/39/791d0f5e.jpg" width="30px"><span>学习前端-react</span> 👍（5） 💬（1）<div>你好，&quot;进入提交阶段，React 会先执行 Effect 的清理函数，然后再次执行 Effect。&quot;
没理解这里为啥要effect 的清理函数，然后执行Effect，很反直觉。是为了执行后产生符合预期的值吗？</div>2022-09-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/4f/39/791d0f5e.jpg" width="30px"><span>学习前端-react</span> 👍（4） 💬（3）<div>附和！之前常见在vue2中经常会去理解父子组件的生命周期函数执行顺序。如created（父） - created（子）- mounted（子）- created（父）。对于react  created 代表render前，mounted 代表render后。所以react 生命周期的执行顺序为。

class 组件：
constructor（父） - render (父) - constructor（子） - render(子) - componentdidmounted（子）- ComponentDidMounted（父）。
hooks 组件：生命周期不显。</div>2022-09-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/fb/4e/6762d56f.jpg" width="30px"><span>林十二XII</span> 👍（2） 💬（1）<div>https:&#47;&#47;react.dev&#47;learn&#47;render-and-commit
结合react新版文档, 可以更容易理解函数组件的生命周期</div>2023-03-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/17/52/0e/c5ff46d2.jpg" width="30px"><span>CondorHero</span> 👍（2） 💬（1）<div>antd 写法说明，来自官网

How to spell Ant Design correctly?#
✅ Ant Design: Capitalized with space, for the design language.

✅ antd: all lowercase, for the React UI library.

✅ ant.design：For ant.design website url.

Here are some typical wrong examples:

❌ AntD

❌ antD

❌ Antd

❌ ant design

❌ AntDesign

❌ antdesign

❌ Antdesign</div>2022-11-06</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/19/64/6f2b7b86.jpg" width="30px"><span>01</span> 👍（0） 💬（1）<div>父组件和子组件的生命周期是交叉进行的， useLayoutEffect 和 useEffect 其实不太一样， useEffect其实是异步的</div>2022-09-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/30/61/98/0d6b499d.jpg" width="30px"><span>船长</span> 👍（0） 💬（2）<div>思考题：有点朦胧的感觉，感觉是像递归那样，父组件遇到子组件，先执行子组件，等子组件执行完了再去执行父组件</div>2022-09-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/39/d2/88/7ea5d21b.jpg" width="30px"><span>momo</span> 👍（0） 💬（1）<div>老师能讲下什么是副作用（Side-effect）吗？包含哪些？</div>2023-12-05</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/fb/4e/6762d56f.jpg" width="30px"><span>林十二XII</span> 👍（0） 💬（0）<div>https:&#47;&#47;react.dev&#47;learn&#47;render-and-commit</div>2023-03-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/e7/20/70a95f94.jpg" width="30px"><span>潮汐</span> 👍（0） 💬（0）<div>组件函数的返回值通常会使用 JSX 语法，React 在渲染阶段根据返回值创建 FiberNode 树。在提交阶段，React 更新真实 DOM 之前会依次执行前面定义的 Effect。

请问老师，这句话最后说在React更新真是DOM之前依次执行前面定义的Effect，不是应该在更新DOM之后吗（按照图中所示）</div>2023-02-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/29/f2/bb/28727280.jpg" width="30px"><span>斩尽满院桃花</span> 👍（0） 💬（0）<div>老师，有点不太理解文稿中“其中useLayoutEffect 的 Effect 是在更新真实 DOM 之后同步执行的，与类组件的 componentDidMount、componentDidUpdate 更相似一些；而 useEffect 的 Effect 是异步执行的，一般晚于 useLayoutEffect 。”这句话里提到的useLayoutEffect是在真实dom之后同步执行，useEffect是异步的是什么意思</div>2023-01-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/17/52/0e/c5ff46d2.jpg" width="30px"><span>CondorHero</span> 👍（0） 💬（0）<div>antd 应该全部小写，参考其官网。</div>2022-11-06</li><br/>
</ul>