你好，我是Barry。

前端实战篇即将步入尾声。之前的课程中，整体的前端项目开发已经告一段落，在本地即可访问项目的完整功能，但是，如果想让更多的人在浏览器直接访问我们的平台，又该如何实现呢？

为了让更多的用户访问视频平台界面。这节课我们就一起来学习一下，如何将我们的前端代码打包上线。

想要高效地打包代码，我们需要用到模块管理工具Webpack。这款工具你应该不陌生，因为我们在最初构建项目的时候就用过它。

只有全面了解Webpack，你才能在后续项目部署的时候轻车熟路，快速实现项目管理和项目打包。而且，Webpack也是在技术面试中也是个高频考点，难度系数也比较高。不过不要有心理负担，耐心学完这节课，你就能找到掌握Webpack的诀窍了。

## Webpack初识

Webpack 是一种模块打包工具，它可以将多个 JavaScript 模块打包成一个或多个 JavaScript 文件，从而减少网页加载时的体积。Webpack 主要用于构建大型的、复杂的应用程序，比如游戏、后端服务等。

Webpack 的工作原理是将源代码分割成一个个模块，然后使用 loader 将这些模块打包成一个或多个 JavaScript 文件。每个模块都可以看作一个独立的文件，它们之间通过依赖关系相互联系。
<div><strong>精选留言（2）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/10/da/d9/f051962f.jpg" width="30px"><span>浩仔是程序员</span> 👍（0） 💬（1）<div>老师可以加餐讲一下怎么部署到服务器吗？</div>2023-06-15</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/25/87/f3a69d1b.jpg" width="30px"><span>peter</span> 👍（0） 💬（1）<div>请教老师几个问题：
Q1：VSCode中编辑vue文件，而vue文件是node解析的，这个关系应该是在VSCode中指定的吧。请问，是在VSCode的什么地方指定的？
Q2：webpack能打包Java后端吗？
Q3：output的path和public有什么区别啊？
Q4：不允许打包的标志是什么？
文中提到“Webpack 会从入口起点开始打包，直到遇到第一个不允许打包的模块或文件为止”，怎么判断不运行打包？
Q5：loader部分，vue会被babel-loader和vue-loader处理。对于一个vue文件，是被两个loader都处理吗？还是选一个处理？
Q6：打包后vue文件还存在吗？
我的理解：vue文件在开发的时候存在，打包后并不存在vue文件；vue会被转换为js文件。</div>2023-05-31</li><br/>
</ul>