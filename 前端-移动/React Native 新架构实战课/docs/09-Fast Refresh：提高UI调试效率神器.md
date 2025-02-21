你好，我是蒋宏伟。今天我们来讲一讲提高 UI 调试效率的方法。

在开发 UI 时，大家一般都是一边看设计稿，一边写代码，一边调试，三种行为交替进行的。谁的大脑都不是一台编译机，也不能安装真正的 React Native 环境。即使已经思考得很完备了，我们也不能保写完的一段代码里面没有任何 Bug，每次写完的代码都能完美符合我们预期的设计。所以，我们离不开 UI 调试。

那UI 调试效率重要吗？非常重要。你可以回想一下，是不是我们大部分的业务开发都会涉及到 UI 的开发。而在 UI 开发的过程中，你是不是会花费很多时间在调试代码上，甚至调试时间可能比真正写代码的时间还要多？正是如此，我们才更应该花点时间学一下调试技巧，把 UI 开发整体效率给提上去。

今天这节课，我会先从 React Native 快速刷新的使用讲起，然后再深入核心原理，帮你理解如何更好地使用快速刷新，提高你的 UI 开发效率。

## 使用快速刷新

React Native [快速刷新（Fast Refresh）](https://reactnative.dev/blog/2019/09/18/version-0.61#fast-refresh)是默认开启的，你不用做任何额外的配置，就能立刻体验到。

快速刷新提效的本质是**及时反馈**。也就是说，你写下代码后就能看到 UI，没有其他任何多余步骤。代码完成了，UI 就更新了，这就是及时反馈。
<div><strong>精选留言（10）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/0f/fc/e7/646bd9f1.jpg" width="30px"><span>worm</span> 👍（0） 💬（1）<div>老师您好，文中介绍使用 allFamiliesByID[id] 作为代理组件，allFamiliesByID[id] 实际上只是一个对象：{current: componentType}。那意思是 RN 里用这个对象从一些逻辑上代替了之前的组件？比如做视图更新时对比新旧组件是否浅相等，改为了只要对比这个 allFamiliesByID[id] 对象就行？

另外，“通过‘代理’组件的方式，就可以实现在同一个组件模块的上下文中，执行不同的函数组件。”，不太理解 不同函数组件的上下文是如何保留在‘代理’组件中的？是使用变量在‘代理’组件中保存了？

最后，“原生视图不会重新创建，从而实现了原生视图的复用”，但是视图是要更新为代码修改后的样子的，所以这里说的是不会将组件整体重新创建，但是会做内部更新的意思？</div>2022-04-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/01/7c/855a7f20.jpg" width="30px"><span>袁德圣</span> 👍（0） 💬（1）<div>请教一下老师用的什么模拟器？</div>2022-04-16</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/ca/71/b5ac045e.jpg" width="30px"><span>Gavin 峰</span> 👍（2） 💬（0）<div>即使反馈 -&gt; 即时反馈</div>2023-05-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/60/a1/45ffdca3.jpg" width="30px"><span>静心</span> 👍（1） 💬（0）<div>老师讲的一如既往的好</div>2022-06-03</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/1a/47/b4cb7fe5.jpg" width="30px"><span>潇元奕</span> 👍（0） 💬（0）<div>老师，我是初学者，那个置顶模拟器怎么个置顶法呢？还有那个类似网页的 dom 元素调试界面对于 react native 怎么调出来呢？</div>2024-02-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/2b/af/c406a173.jpg" width="30px"><span>BennyTian</span> 👍（0） 💬（0）<div>模块：如果你修改的模块导出的东西不只是 React 组件，快速刷新将重新执行该模块以及所有依赖它的模块；
React Native 应用：如果你修改的文件被 React 组件树之外的模块引用了，快速刷新将重新渲染整个 React Native 应用。
-----
这两个可以帮忙举个例子吗？ 确实有时候遇到 更改代码后 莫名其妙刷新了整个App，很费解，感觉答案在这里，但不太理解，希望您帮忙提供例子~ 感谢~</div>2023-11-02</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/33/8c/1cb64815.jpg" width="30px"><span>CLC</span> 👍（0） 💬（0）<div>状态复用还是花了一点时间消化，后来突然想明白：

“状态“是存在不变“代理”上的，代码变化保存后，“代理”会将“状态”数据给到新的函数组件进行渲染

是这样吗</div>2023-08-19</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/lYyZCOD8Cn0Tb2BXtic01fHc6Pl8c4X3lyRRX0xd7iblFbYvrk7Jm9ibbfrqg5KuaWxDrso0eicPW9wem8cd8pSoQA/132" width="30px"><span>Geek_2158bf</span> 👍（0） 💬（0）<div>牛啊，还以为直接讲下用法就行了，想不到还把原理也讲到</div>2023-02-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/19/0f/35bf848b.jpg" width="30px"><span>昼短夜长</span> 👍（0） 💬（0）<div>很好, 这一章可以反复琢磨</div>2022-08-16</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/21/56/8a/16545faf.jpg" width="30px"><span>胡少伟</span> 👍（0） 💬（1）<div>有没有什么办法能够js打断点</div>2022-06-28</li><br/>
</ul>