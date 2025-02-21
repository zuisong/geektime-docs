你好，我是轩脉刃。

上一节课我们增加了自动化创建服务工具、命令行工具，以及中间件迁移工具。你会发现，这些工具实现起来并不复杂，但是在实际工作中却非常有用。今天我们继续思考还能做点什么。

我们的框架是定义了业务的目录结构的，每次创建一个新的应用，都需要将AppService中定义的目录结构创建好，如果这个行为能自动化，实现**一个命令就能创建一个定义好所有目录结构，甚至有demo示例的新应用**呢？是不是有点心动，这就是我们今天要实现的工具了，听起来功能有点庞大，所以我们还是慢慢来，先设计再实现。

## 初始化脚手架设计

这个功能倒不是什么新想法，有用过Vue的同学就知道，Vue官网有介绍一个 `vue create` [命令](https://cli.vuejs.org/zh/guide/creating-a-project.html)，可以从零开始创建一个包含基本Vue结构的目录，这个目录可以直接编译运行。

在初始化一个Vue项目的时候，大多数刚接触Vue的同学对框架的若干文件还不熟悉，很容易建立错误vue的目录结构，而这个工具能帮Vue新手们有效规避这种错误。

同理，我们的框架也有基本的hade结构的目录，初学者在创建hade应用的时候，也大概率容易建立错误目录。所以参考这一点，让自己的框架也有这么一个命令，能直接创建一个新的包含hade框架业务脚手架目录的命令。这样，能很大程度方便使用者就在这个脚手架目录上不断开发，完成所需的业务功能。
<div><strong>精选留言（6）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/18/6b/23/ddad5282.jpg" width="30px"><span>Aaron</span> 👍（0） 💬（1）<div>直接go get 好像会更方便啊</div>2021-11-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/3b/fc/04a75cd0.jpg" width="30px"><span>taoist</span> 👍（0） 💬（0）<div>这里生成的新项目需要先 go mod tidy 更新依赖</div>2024-01-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/ce/6d/530df0dd.jpg" width="30px"><span>徐石头</span> 👍（0） 💬（0）<div>默认最小版本号是0.1.0吧，不是0.0.1</div>2022-11-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/23/50/1f5154fe.jpg" width="30px"><span>无笔秀才</span> 👍（0） 💬（0）<div>那么正确的使用方法是 先git clone hade框架，
再进行 hade new?
那么新项目的目录 在hade 框架下？</div>2022-01-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/cb/07/482b7155.jpg" width="30px"><span>牛玉富</span> 👍（0） 💬（0）<div>咦，go install不就能一步安装的吗？</div>2022-01-13</li><br/><li><img src="" width="30px"><span>2345</span> 👍（0） 💬（1）<div>这个利用脚手架创建新的项目，还需要先下载hade的示例代码吧，不然哪里有hade new命令呢？</div>2021-11-14</li><br/>
</ul>