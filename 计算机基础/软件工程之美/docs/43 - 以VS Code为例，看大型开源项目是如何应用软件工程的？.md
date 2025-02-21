你好，我是宝玉。如果你所在的团队在日常的软件项目开发中，能科学地应用软件工程的知识，让你的项目能持续取得进展，最终交付的产品也有很好的质量，那么是一件非常幸运的事情。

然而现实中，很多人并没有机会去参与或观察一个好的项目是什么样子的，也没机会去分析一个好的项目是如何科学应用软件工程的。

好在现在有很多优秀的开源项目，不仅代码是公开的，它们整个项目的开发过程都是公开的。通过研究这些开源项目的开发，你能从中学习到一个优秀项目对软件工程的应用，加深你对软件工程知识的理解，进而应用到你自己的项目实践中。

我想你对VS Code应该不陌生，它是一个非常优秀的编辑器，很多程序员包括我非常喜欢它。VS Code也是一个大型的开源项目，整个开发过程非常透明，所以今天我将带你一起看一下VS Code是如何应用软件工程的，为什么它能构建出这么高质量的软件。

## 如何从VS Code的开发中学习软件工程？

也许你会很好奇，平时也去看过VS Code的网站，但并没有提到软件工程的呀？

是的，VS Code的网站并没有特别突出这些信息，但是如果你有心，可以找到很多有价值的信息，它的整个开发过程都是公开透明的。

比如通过它项目的[WIKI](http://github.com/microsoft/vscode/wiki)和[博客栏目](http://code.visualstudio.com/blogs)，可以看到项目的计划、项目开发流程、测试流程、发布流程等信息。通过它的[GitHub](http://github.com/microsoft/vscode)网站，你可以看到团队是如何基于分支开发，开发完成后提交Pull Request，团队成员如何对代码进行审核，合并代码后如何通过持续集成运行自动化测试。
<div><strong>精选留言（11）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/11/a8/37/00ed15af.jpg" width="30px"><span>胡浩🐸</span> 👍（11） 💬（1）<div>赞，有好多值的学习和借鉴的地方，打开 VS Code 经常看到更新提示，感觉被后就有一个非常高效的敏捷团队，今天终于学习到了。

VS Code 每 4 周发布一个迭代节奏非常棒，每周做的事情都很科学合理，而且把 Github Issue 的功能用的淋漓尽致，打的各种 Label 很值的学习。</div>2019-06-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/ec/4f/84415aa2.jpg" width="30px"><span>一文字</span> 👍（8） 💬（1）<div>棒，感觉像打开了新世界的大门，赶紧把这种学习方法消化下🧘‍♂️</div>2019-06-11</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/rNbzpa6VTaXYII5W2vrvq8j8DlNEYeFlWIDTFpCo4XMHARBHW8IqIMSfzX0XJH8R5YX2jtmLpsTtnicu2uibpCbw/132" width="30px"><span>露娜</span> 👍（5） 💬（1）<div>老师：现在遇到一个特别尴尬的事情，每次发测试前，都会预留时间每个人自测自己的代码，但是总有些人根本就不测，直接扔给测试。测试一测一大堆问题。请问这种情况有么有好的方法可以避免？</div>2020-05-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/88/c8/6af6d27e.jpg" width="30px"><span>Y024</span> 👍（5） 💬（1）<div>怎么学习开源项目？除了眼前的代码，还有诗和远方……</div>2019-06-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/53/5d/46d369e5.jpg" width="30px"><span>yellowcloud</span> 👍（4） 💬（1）<div>宝玉老师，我们目前项目使用的管理工具是TFS，它好像也自带CI和CD功能，我想请问一下，它和文中介绍的Azure DevOps，那个好用呢？

</div>2019-06-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/3c/8a/900ca88a.jpg" width="30px"><span>神经旷野舞者</span> 👍（3） 💬（1）<div>看了vscode感觉项目管理也不复杂，关键是一群靠谱的人有动力有方法有共识，项目管理失败基本都是人的因素，说难就难说不难也不难。</div>2020-01-01</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/c1/60/f5439f04.jpg" width="30px"><span>Geek_dn82ci</span> 👍（3） 💬（1）<div>感觉vscode的日常开发管理工作非常饱和，这里有个问题想请教，以vscode为例，4周的一个迭代周期如何确保效率，特别实在第一周里，包含了历史遗留问题的处理，还要做本次迭代的规划安排，更何况开源项目如果不是全职铺在上面怎么办？如果在某一个迭代周期内因为不可抗力因素导致延期了怎么办？</div>2019-06-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/b2/27/c9ab10ae.jpg" width="30px"><span>freda</span> 👍（1） 💬（2）<div>你好，我想请教下，我领导想用禅道软件做项目管理，可是我觉得禅道更适合做软件开发，想听听你的看法</div>2019-10-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/93/fa/5f8d06fc.jpg" width="30px"><span>远征</span> 👍（1） 💬（1）<div>师傅领进门：）不仅知道如何入手开源项目，而且在项目管理上也有新借鉴！谢谢老师</div>2019-06-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/26/eb/d7/90391376.jpg" width="30px"><span>ifelse</span> 👍（0） 💬（0）<div>当你日常在看一个开源项目的时候，不仅可以去看它的代码，还可以去观察它是怎么应用软件工程的，不仅可以加深你对软件工程知识的理解，还能从中学习到好的实践。--经记下来</div>2022-07-10</li><br/><li><img src="" width="30px"><span>清心草色</span> 👍（0） 💬（0）<div>window客户端使用WPF开发，是一个好的方向吗？</div>2021-11-18</li><br/>
</ul>