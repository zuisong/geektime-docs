你好，我是大圣。

上一讲我们讲完了组件库的核心知识点，这一讲我们来学习一个叫Vue 3的进阶知识点：自定义渲染器，这个功能可以自定义Vue渲染的逻辑。

在给你讲清楚原理之后，我还会带你一起实现一个Canvas的渲染器实际上手体验一下。

## 什么是渲染器

我们都知道，Vue内部的组件是以虚拟dom形式存在的。下面的代码就是一个很常见的虚拟Dom，用对象的方式去描述一个项目。相比dom标签相比，这种形式可以让整个Vue项目脱离浏览器的限制，更方便地实现Vuejs的跨端。

```javascript
{
  tag: 'div',
  props: {
    id: 'app'
  },
  chidren: [
    {
      tag: Container,
      props: {
        className: 'el-container'
      },
      chidren: [
        '哈喽小老弟!!!'
      ]
    }
  ]
}
```

渲染器是围绕虚拟Dom存在的。在浏览器中，我们把虚拟Dom渲染成真实的Dom对象，Vue源码内部把一个框架里所有和平台相关的操作，抽离成了独立的方法。所以，我们只需要实现下面这些方法，就可以实现Vue 3在一个平台的渲染。

首先用createElement创建标签，还有用createText创建文本。创建之后就需要用insert新增元素，通过remove删除元素，通过setText更新文本和patchProps修改属性。然后再实现parentNode、nextSibling等方法实现节点的查找关系。完成这些工作，理论上就可以在一个平台内实现一个应用了。
<div><strong>精选留言（14）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/12/e6/e5/b6980a7a.jpg" width="30px"><span>无双</span> 👍（3） 💬（1）<div>想深入了解一下three.js和vue的结合，有没有这方面的资料，或者最佳实践？</div>2021-12-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/3f/a8/8da58e53.jpg" width="30px"><span>海阔天空</span> 👍（1） 💬（1）<div>有很多都不是很懂。。。</div>2021-12-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/c8/4a/3a322856.jpg" width="30px"><span>ll</span> 👍（13） 💬（2）<div>开眼界的一课。平时工作中涉及相关内容较少，所以这部分的内容还需课下多练几遍。
结合之前所学，写几点感想，首先有以下几种“过程”;
1. html --&gt; dom --&gt; 浏览器
2. html --&gt; v-dom --&gt; dom --&gt; 浏览器
3. svg, canvas, webgl --&gt; v-dom --&gt; dom --&gt; 浏览器
4. html等 --&gt; v-dom --&gt; dom --&gt; &quot;web内核&quot; --&gt; 其他平台
5. html等 --&gt; v-dom --&gt; &quot;xxx object model&quot; --&gt; 其他平台
然后，
vue 的角色是提供了操作 v-dom 的“方式”，并且在 v-dom --&gt; dom 这个过程中，非常&quot;高效&quot;且&quot;专业&quot;,

今天的内容聚焦过程 4. 的前半段，即 html等 --&gt; v-dom.

为什么？或者解决了什么问题？ 答: 我们操作 v-dom 的方式不会因需要”适配“不同的&quot;标准&quot;而发生”任何“改变。

怎么实现的？svg，canvas 等怎么变成“统一”的 v-dom，需要什么？vue 也给你提供了 createRenderer。

“适配器&quot;出场了，在代码抽象实现上来说就是“适配器模式”。我开始看文章时猜的是“策略模式”，当然我学艺不精，这也是个复习“设计模式”的好机会。

至于思考题，Vue 在 在 node 环境中渲染我能想到的应用场景，是前后端同构，SSR，SSG，产生这个问题的根本原因就是，node 它不懂 “dom&quot;, 不懂怎么办？配个翻译？要不你翻译成它能懂的再给它？

已上，就是我的一些大致想法，谬误之处还望大家不吝赐教。</div>2021-12-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/3c/1c/47e5b7aa.jpg" width="30px"><span>Johnson</span> 👍（5） 💬（0）<div>这一讲的跨端原理讲解太实用啦！😁</div>2021-12-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/94/69/4937e1e4.jpg" width="30px"><span>Sean</span> 👍（1） 💬（0）<div>源码地址：https:&#47;&#47;github.com&#47;shengxinjing&#47;vue3-vs-vue2.git</div>2022-04-15</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/94/69/4937e1e4.jpg" width="30px"><span>Sean</span> 👍（1） 💬（0）<div>老师 这没有代码 可以运行一下吗</div>2022-04-15</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/17/d9/0b/d842b71a.jpg" width="30px"><span>乐多</span> 👍（1） 💬（0）<div>老师，这一讲的源码哪里有？</div>2022-04-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/29/9c/7a/39578e4e.jpg" width="30px"><span>老鼠砍猫</span> 👍（0） 💬（0）<div>仓库丢失</div>2024-08-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/29/d2/7f/44fbd96b.jpg" width="30px"><span>迷路森林</span> 👍（0） 💬（0）<div>我的renderer.js文件一直渲染不出来，请问是要安装什么依赖包吗</div>2022-09-04</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/19/92/a7/00fefed5.jpg" width="30px"><span>Chaos浩</span> 👍（0） 💬（0）<div>还是这种内容更吸引人</div>2022-09-01</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/ac/62/37912d51.jpg" width="30px"><span>东方奇骥</span> 👍（0） 💬（0）<div>好文！最近工作中正要自定义stater，没想道就找到了。</div>2022-07-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/18/66/b2/cf691f56.jpg" width="30px"><span>江无花</span> 👍（0） 💬（0）<div>Vue 如何在 node 环境中渲染，这个其实没太明白。是指在node环境中，使用命令行输出？</div>2022-06-25</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/18/9f/ea/b587985a.jpg" width="30px"><span>李文华</span> 👍（0） 💬（0）<div>第一个例子累加器值并不会增加</div>2022-03-10</li><br/><li><img src="" width="30px"><span>Geek_15264a</span> 👍（0） 💬（0）<div>最终找到了，感觉还是需要把本节涉及的源码，在显眼的位置贴出来，找到本章中提的一个链接，打开有问题，结果直接去你的github仓库下找到对应的代码</div>2022-01-07</li><br/>
</ul>