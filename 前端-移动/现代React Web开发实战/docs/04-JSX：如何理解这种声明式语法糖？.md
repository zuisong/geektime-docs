你好，我是宋一玮。上节课我们利用Create React App（CRA）脚手架工具创建了一个React项目，并在项目中部分实现了一个简单的看板应用。在接下来的课程里，我们会把看板应用抽丝剥茧，逐一认识学习项目里涉及到的React概念和API。很自然地，我们这节课会讲到JSX语法和React组件。

有不少初学者对React的第一印象就是JSX语法，以至于会有这样的误解：

- JSX就是React？
- JSX就是React组件？
- JSX就是另一种HTML？
- JSX既能声明视图，又能混入JS表达式，那是不是可以把所有逻辑都写在JSX里？

这些误解常会导致开发时遇到各种问题：

- 写出连续超百行、甚至近千行的JSX代码，既冗长又难维护；
- 在JSX的标签上添加了HTML属性却不生效；
- JSX混入JS表达式后，页面一直报错。

其实只要**理清了JSX和React组件的关系**，这些问题自然不在话下。

总的来说，React是一套声明式的、组件化的前端框架。顾名思义，**声明（动词）组件**是React前端开发工作最重要的组成部分。在声明组件的代码中使用了JSX语法，JSX不是HTML，也不是组件的全部。

接下来，我们就详细展开介绍JSX和React组件。
<div><strong>精选留言（19）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/20/48/9e/9bbaa97d.jpg" width="30px"><span>Geek_fcdf7b</span> 👍（16） 💬（1）<div>首先，感谢老师对于评论区的每个问题几乎都在回复，从评论中也学到了很多东西。然后，请教一下，V17之后，JSX好像不一定是编译成React.createElement了吧，好像有个react&#47;jsx-runtime</div>2022-09-03</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/58/9d/91d795cf.jpg" width="30px"><span>ZENG</span> 👍（8） 💬（1）<div>1. JSX 是函数的语法糖，那 JS 相关框架函数都能实现 JSX
2. 函数的原理就是输入什么会得到一个确定的结果返回，理论上就可以输出成其他需要的结果
</div>2022-08-31</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1a/0e/80/f8f91bae.jpg" width="30px"><span>null</span> 👍（4） 💬（1）<div>这一节课下来干货好多哇</div>2022-08-30</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/4f/39/791d0f5e.jpg" width="30px"><span>学习前端-react</span> 👍（3） 💬（1）<div>请问：如上我们理解的声明式在编程上便是函数式编程，在jsx上便是 三目运算符 和 Function map，所有在vue的模板里，v-if v-for 是不是不太声明式？</div>2022-09-01</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/ac/62/37912d51.jpg" width="30px"><span>东方奇骥</span> 👍（3） 💬（1）<div>1. JSX 一定得是 React 吗？React 以外的技术能不能使用 JSX？
答：不一定。JSX 并不是一个新的模板语言，可以认为是一个语法糖。比如Vue也有JSX。

2. JSX 一定得生成 HTML 吗？可以用 JSX 生成其他模版吗？
答：课程中讲到，本质上来说，JSX可以认为是一个语法糖，最终还是调用React.createElement. 所以理解重写一个createElement也可能生成别的，不一定是HTML。</div>2022-08-31</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1e/b0/d8/1425514b.jpg" width="30px"><span>心叶</span> 👍（3） 💬（1）<div>讲到jsx，为什么不直接拿出官方文档呢？

https:&#47;&#47;facebook.github.io&#47;jsx&#47;

从文档你可以知道：
jsx不是react的api，虽然是react团队搞出来的
他的灵感是es4里面的e4x，但原本的e4x因为涉及到语法和语义的定义，实现过于复杂所以被弃用。
jsx的目标是供预处理器使用，将其转换成es</div>2022-08-31</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/4f/39/791d0f5e.jpg" width="30px"><span>学习前端-react</span> 👍（1） 💬（1）<div>JSX 一定得是 React 吗？React 以外的技术能不能使用 JSX？
 不是 这是一个dsl ，其他语言只要实现其底层，便可使用其上层的jsx
JSX 一定得生成 HTML 吗？可以用 JSX 生成其他模版吗？
如上。</div>2022-09-01</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/c9/f9/39492855.jpg" width="30px"><span>阿阳</span> 👍（1） 💬（1）<div>最近在vue项目中引入了jsx，在自定义组件的时候，恰好踩到了这节课说的几个坑。帮助很大。
jsx应该不是react独有的，它只是个语法糖，它可以被编译为任意的其他渲染函数。</div>2022-09-01</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/96/87/bbdeb4ee.jpg" width="30px"><span>杨永安</span> 👍（1） 💬（4）<div>jsx本质是一个返回格式为json的node节点描述信息。可以用在跨端跨平台的用途，比如拿到json作为render蓝本的时候，最后的render会根据宿主环境对应调用相应API。


话说这课没有了吗？</div>2022-08-31</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/a0/59/86073794.jpg" width="30px"><span>Hello,Tomrrow</span> 👍（1） 💬（1）<div>JSX 不是在 React 中发明的，二者的关系更像是相互成就。

</div>2022-08-30</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/2b/01/f7/75eb754f.jpg" width="30px"><span>即将暴富的木杉</span> 👍（1） 💬（1）<div>vue  的  template 的实现就是基于jsx的吧</div>2022-08-30</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/5c/31/d7b92b6b.jpg" width="30px"><span>癡癡的等你歸</span> 👍（0） 💬（2）<div>老师，这段话是否有问题？

其中 type 参数是必须的，props 可选，当参数数量大于等于 3 时，可以有一个或多个 children。

参数数量和children有什么必然联系吗？🤔️</div>2022-11-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/c9/d5/b08a27ed.jpg" width="30px"><span>灵感_idea</span> 👍（0） 💬（1）<div>讲解确实系统又全面，也可以看出作者的经历和经验都比较丰富，只是暂时还未进入比较深入的部分，希望加油做成一个精品课！</div>2022-11-06</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/28/d8/2b/21bbdcc4.jpg" width="30px"><span>狗蛋。</span> 👍（0） 💬（1）<div>如果todoList中有一个空对象，还会遍历出KanbanCard吗？如果遍历出来只是title和status没有值 是一个空的dom？</div>2022-10-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/20/88/a1/a78990c4.jpg" width="30px"><span>永不放弃</span> 👍（0） 💬（1）<div>老师 这篇适合0基础开发吗？ 了解html css  flutter，js部分</div>2022-10-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/19/64/6f2b7b86.jpg" width="30px"><span>01</span> 👍（0） 💬（1）<div>jsx 并不直接生成html。 </div>2022-09-15</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/30/5d/f7/936e32e3.jpg" width="30px"><span>雨猫</span> 👍（1） 💬（0）<div>怎么大家收货这么多呀</div>2022-09-02</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/dc/bd/ea9c16b8.jpg" width="30px"><span>莫比斯</span> 👍（0） 💬（0）<div>1. JSX 一定得是 React 吗？React 以外的技术能不能使用 JSX？
jsx=js+xml，用模板语句的地方都用它。所以vue中可以用

2. JSX 一定得生成 HTML 吗？可以用 JSX 生成其他模版吗？
可以的，比如说xml。只要是标记语言，jsx都可以拿生成模板</div>2023-07-03</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/e7/20/70a95f94.jpg" width="30px"><span>潮汐</span> 👍（0） 💬（0）<div>将Ract很重要的基础知识讲的很详细，好多点都是需要大脉络层面熟记反复思考的</div>2022-11-25</li><br/>
</ul>