你好，我是宋一玮。

上节课我们从相当于React门面的JSX语法入手，了解了JSX是React核心API之一`React.createElement()` 的语法糖，是一种声明式的前端模版技术，然后深入学习了JSX的写法，也捎带提了一下JSX与React组件的关系。

那么这节课我们就来进一步讲讲React组件。

组件化开发已经成为前端开发的主流趋势，市面上大部分前端框架都包含组件概念，有些框架里叫Component，有些叫Widget。**React更是把组件作为前端应用的核心**。

不过无论是哪种框架，几乎每一位学习前端组件的开发者都会遇到下面这些问题：

- 开发应用时是不是一定要拆分组件？一个应用我只用一个组件开发行不行？
- 如果一定要拆分组件，面对需求文档我该怎么下手？
- 组件拆分的粒度是应该大些还是小些？有没有可以参照的标准？

其实**组件拆分并无唯一标准**。拆分时需要你理解业务和交互，设计组件层次结构（Hierarchy），以关注点分离（Separation Of Concern）原则检验每次拆分。另外也要避免一个误区：组件确实是代码复用的手段之一，但并不是每个组件都需要复用。

这节课我们就从实践入手，学习如何拆分React组件，同时也介绍一些最佳实践。相信这节课结束时，你对上面的问题已经有自己的答案了。
<div><strong>精选留言（10）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/21/69/79/b4132042.jpg" width="30px"><span>🐑</span> 👍（1） 💬（0）<div>大家好，咱们课程的代码地址在这里哦👇

对应的Pull Request是： https:&#47;&#47;gitee.com&#47;evisong&#47;geektime-column-oh-my-kanban&#47;pulls&#47;3
打了一个v0.5.0版本标签： https:&#47;&#47;gitee.com&#47;evisong&#47;geektime-column-oh-my-kanban&#47;releases&#47;tag&#47;v0.5.0</div>2022-09-01</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/96/87/bbdeb4ee.jpg" width="30px"><span>杨永安</span> 👍（3） 💬（1）<div>哇，周四的凌晨更新</div>2022-09-01</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/96/87/bbdeb4ee.jpg" width="30px"><span>杨永安</span> 👍（1） 💬（2）<div>好奇真子组件模式</div>2022-09-01</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/18/5d/74/2762a847.jpg" width="30px"><span>流乔</span> 👍（0） 💬（1）<div>唉，现在写开源项目就特别容易决策疲劳</div>2022-09-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/18/ca/f5/3f95bf91.jpg" width="30px"><span>tron</span> 👍（0） 💬（1）<div>对 React 子组件概念的澄清这一小节
对于组件树和元素树的不同之处，有点不是太理解
不知道是不是可以理解为，组件树是代码运行前的结构，代码运行后，组件return出元素，就成了元素树呢</div>2022-09-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/5b/25/d78cc1fe.jpg" width="30px"><span>都市夜归人</span> 👍（0） 💬（1）<div>const KanbanBoard = ({ children }) =&gt; (  &lt;main className=&quot;kanban-board&quot;&gt;{children}&lt;&#47;main&gt;);
缺少 return</div>2022-09-01</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/dc/bd/ea9c16b8.jpg" width="30px"><span>莫比斯</span> 👍（0） 💬（0）<div>pc存储空间
|——本地磁盘
|        |——文件夹
|        |——文件
|——其他存储设备</div>2023-07-03</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/ea/c1/d9cb2299.jpg" width="30px"><span>Lucas Lin</span> 👍（0） 💬（0）<div>不理解为什么老师会说「就拆分方向而言，一般面对中小型应用，更倾向于从上到下拆分，先定义最大粒度的组件，然后逐渐缩小粒度；面对大型应用，则更倾向于从下往上拆分，先从较小粒度的组件开始。」，有例子或是不同拆分方向带来的优缺点吗？</div>2022-12-09</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTJnRUibp7LV1l6RA5E8BcLjwLIaOoQxyicM3iaZXcPrJPdMkGmvFHWxBV6sbib7FQK6YMaOdKo6oiaBRaA/132" width="30px"><span>InfoQ_3906e8b6c95f</span> 👍（0） 💬（0）<div>React 的Component和Element是不是类似于Flutter的Widget和Element? Component&#47;Widget 只是轻量级的UI逻辑封装，也就是文章中说的POJO，真正参与渲染的其实是Element或更加底层的RenderObject(Flutter)</div>2022-10-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/c9/f9/39492855.jpg" width="30px"><span>阿阳</span> 👍（0） 💬（0）<div>周四，继续追</div>2022-09-01</li><br/>
</ul>