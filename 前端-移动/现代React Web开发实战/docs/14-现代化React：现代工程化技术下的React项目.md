你好，我是宋一玮，欢迎回到React应用开发的学习。

在第[12](https://time.geekbang.org/column/article/571276)、[13](https://time.geekbang.org/column/article/574161)节课，我们学习了React的单向数据流，以及怎么用面向接口编程的思想指导组件设计开发。同时我们一起为oh-my-kanban做了一次大重构，实践了刚学到的概念和方法。可以说，我们在学习写React应用代码方面，已经获得了阶段性进展。

但也需要知道，写出来的源码毕竟还不能用来上线，还得经过 `npm run build` 打包构建出生产环境代码，然后才能上线。你可能会好奇，这个命令都做了什么？这个命令是CRA，由Create React App脚手架工具提供，它的内部**对开发者而言是个黑盒**。要想了解它，我们得先把黑盒打开，或者，用更好的方式：**自己搭一个白盒**出来。

还记得在上节课末尾的预告吗？这节课我会带着你，不依赖CRA，**用现代的工程化技术重新搭建一个React项目，然后把oh-my-kanban的代码迁移过来**，让它真正成为你自己的项目。

好的，现在开始这节课的内容。

## CRA为我们做了什么？

在[第3节课](https://time.geekbang.org/column/article/553817)，我们用FB官方提供的CRA脚手架工具创建了oh-my-kanban项目，在这之后我们就一直专注于代码开发，再也没有关注过项目配置了。现在oh-my-kanban项目开发已经步入正轨，是时候回过头来看看CRA为我们做了哪些事情。
<div><strong>精选留言（6）</strong></div><ul>
<li><img src="" width="30px"><span>Geek_82fd2f</span> 👍（1） 💬（1）<div>在添加ESLint的时候，如果选择Yes也就是使用TS， Does your project use TypeScript? · No &#47; Yes，规则里就不会出现Airbnb代码风格了，请问是不是Airbnb还不支持</div>2022-11-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/18/bc/3e/82b7deca.jpg" width="30px"><span>huangshan</span> 👍（1） 💬（2）<div>可以补充一下关于turbopack相关的工程化吗？</div>2022-10-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/30/61/98/0d6b499d.jpg" width="30px"><span>船长</span> 👍（1） 💬（1）<div>记得想要 Eslint 生效要启动 vscode 中的 eslint 插件。。</div>2022-09-30</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/9d/c4/13376c14.jpg" width="30px"><span>DullSword</span> 👍（1） 💬（1）<div>增加NPM 命令lint出错的小伙伴可以试试：

```
&quot;lint&quot;: &quot;eslint \&quot;.&#47;src&#47;**&#47;*.{js,jsx}\&quot;&quot;,
```</div>2022-09-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/30/61/98/0d6b499d.jpg" width="30px"><span>船长</span> 👍（1） 💬（3）<div>3-13 痛点：
没有报错提醒
没有智能提示，比如在引入 useEffect，浏览器直接报错，原因是没有在顶部 import，这时候还需要手写去引入</div>2022-09-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1b/6b/c6/4cc776a7.jpg" width="30px"><span>百里</span> 👍（0） 💬（0）<div>最近独立负责一个项目，这个课程像及时雨一样，助我成长</div>2023-01-24</li><br/>
</ul>