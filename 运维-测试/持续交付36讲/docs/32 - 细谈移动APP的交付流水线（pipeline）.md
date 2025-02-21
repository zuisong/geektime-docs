你好，我是王潇俊。今天我和你分享的主题是：细谈移动APP的交付流水线（pipeline）。

在上一篇文章[《了解移动App的持续交付生命周期》](https://time.geekbang.org/column/article/23611)中，我和你分享了移动App的整个交付生命周期，并把移动客户端的交付与后端服务的交付方式进行了对比。从中，我们发现移动App自身的特点，使得其持续交付流程与后端服务存在一定的差异。

所以，今天我会在上一篇文章的基础上，和你分享移动App持续交付中的个性化内容。这些个性化的内容，主要表现在流水线的三个重要环节上：

1. 采用与发布快车（Release Train）模式匹配的代码分支管理策略；
2. 支持多项目、多组件并行的全新构建通道；
3. 自动化发布，完全托管的打包、发布、分发流程。

接下来，我就从这三个角度，和你详细聊聊移动App的持续交付吧。

## 发布快车模式

首先，我先和你说说什么是发布快车。

顾名思义，发布快车，就像一列由多节车厢组成的火车，每一节车厢代表一个发布版本，整个火车以一节节车厢或者说一个个版本的节奏，定期向前发车。而工程师们，则会把自己开发完成的功能集成到一节节的车厢上，这样集成在一节车厢的功能代码，就形成了一个新的版本。

如图1所示，就很好地展示了发布快车的含义。

![](https://static001.geekbang.org/resource/image/c8/d2/c802a0f8f0cf4e57e4854b4e227918d2.png?wh=624%2A388)

图1 发布快车详解图
<div><strong>精选留言（5）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/14/0c/30/d4737cd5.jpg" width="30px"><span>lyonger</span> 👍（0） 💬（0）<div>老师，移动APP的自动构建和持续集成工具有什么区别呢？不知我下面这么理解有无问题。

1）自动构建比如gradle&#47;maven是解决工程类的打包编译，包依赖问题，实际上是一个包管理器是么？
2）而持续集成工具是一个可以自定义流水线的平台？</div>2021-03-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/1c/4b/2e5df06f.jpg" width="30px"><span>三件事</span> 👍（0） 💬（0）<div>老师还有一个问题

3.如果我们的实际开发比线上版本领先一到两个版本的话，采用 git flow 这种方式，分支管理就比较麻烦。对于这一点老师有没有什么好的办法？</div>2019-10-15</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/1c/4b/2e5df06f.jpg" width="30px"><span>三件事</span> 👍（0） 💬（0）<div>老师你好，受益匪浅，想请教两个问题：

1.如何最大程度的提高构建速度？在打包设备一定的情况下。
2.从 master merge 回 dev 的时候有没有什么好的实践方式？</div>2019-10-15</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/6a/a2/f9efd9dc.jpg" width="30px"><span>春和景明</span> 👍（0） 💬（1）<div>老师，我们知道
stages有如下特点 :

所有 stages 会按照顺序运行，即当一个 stage 完成后，下一个 stage 才会开始

只有当所有 stages 成功完成后，该构建任务 (Pipeline) 才算成功

如果任何一个 stage 失败，那么后面的 stages 不会执行，该构建任务 (Pipeline) 失败

针对第三个特点，我们有没有办法，让所有stage都能够执行呢？


另外经常遇到的
Stage &quot;xxx&quot; skipped due to earlier failure(s)

是什么意思？该如何避免呢？
</div>2019-05-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/48/9e/99cb0a7a.jpg" width="30px"><span>心在飞</span> 👍（0） 💬（0）<div>我们分支模型为 master -&gt; integration-&gt;feature, 叫法不同，但使用方式上一样。master 打tag发布，每次feature合并到integration都要做DoD(definition of done)检查，包括sonar，coverity等。但我们是嵌入式设备（医疗行业），没有持续交付，只有持续部署。</div>2019-02-27</li><br/>
</ul>