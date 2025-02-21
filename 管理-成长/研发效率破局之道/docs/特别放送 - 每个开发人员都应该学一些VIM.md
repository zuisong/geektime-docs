你好，我是葛俊。

在“研发流程”和“工程方法”模块中，我主要是从团队的角度和你分享如何提高研发效能，所以很多同学希望我能分享一些工具的使用，来提高自己的效能。所以今天，我准备了一篇关于VIM的文章。在这篇文章中，我会着重带你深入了解VIM的两个特点。因为正是基于这两个特点，VIM可以很好地提高我们的工作效率。至于更多的、具体的VIM使用方法和技巧，我会在接下来的“个人效能”模块中，用另一篇文章专门详细与你介绍。

如果你已经是一个VIM的使用者了，那我希望文中关于VIM原理的讨论，可以帮助你更深入地理解它，进而可以更高效地使用它。而如果你还不是VIM的使用者，那我推荐你学习它的基本方法，并寻找适当的场景去使用它。

其实，向开发者们推荐编辑器，尤其是像VIM这样一个比较容易引起争议的编辑器，是一件有风险的事儿。但，基于我对VIM的了解和它能给开发者带来的巨大好处，我认为这个风险是值得的，相信你也能从中有所收获。

我们下来看看什么是VIM。

## 什么是VIM？

VIM是一个老牌的编辑器，前身是VI，第1个版本发行于1978年，距离今天已经有41年的历史了。

VIM是VI Improved，是提高版的VI，相对来说比较新，但实际上它的第1个版本也早在1991年就发布，也已经有28年的历史了。
<div><strong>精选留言（14）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/13/17/27/ec30d30a.jpg" width="30px"><span>Jxin</span> 👍（8） 💬（1）<div>1.严格要求自己代码的规范，深入学习并运用重构手法。坚持两三个月后，突然有一天，就发现自己写代码打开了一片新天地，一切都变得整洁，明确。
2.对于vim用得很烂，严重依赖idea和鼠标。但我愿意相信，如果能脱离鼠标，熟练命令行的开发模式，很可能这也会是一片新天地，一个关于高效的新天地。
3.期待老师的个人效能篇。前面的章节写得很棒，很多干货和知识延伸，极客的专栏买了大半读了大半，您的这个专栏，个人觉得跟宝玉老师的软件工程之美带来的感受相似，虽非纯技术文章，但对实际工作和国内软件开发的帮助都极大。对国内，非专科的程序员都是很宝贵的财富，谢谢您。</div>2019-10-07</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/75/9b/611e74ab.jpg" width="30px"><span>技术修行者</span> 👍（6） 💬（1）<div>编译器有点儿像编程语言，不同的人有不同的爱好，比较容易引起争吵。

最近一年多一直在用VS Code，对于vim，更多的是到服务器上的维护工作时会用到，例如检查服务器或者应用配置，这种情况下，不是深度使用vim，知道基本的命令操作就好了。

曾几何时，我看到别人基本不用鼠标，直接通过键盘可以完成大部分日常工作，非常羡慕，也背过很多快捷键，但后来基本忘的差不多了。这种事情如果没有形成“肌肉记忆”，基本没啥意义。

我现在的理解，软件开发的工作更多是脑力工作，工具可以提高我们的效率，维护一套适合自己的工具箱很有必要，但是过度关注这些，可能会舍本逐末。当然，我的理解可能会很片面。</div>2019-10-04</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/88/c8/6af6d27e.jpg" width="30px"><span>Y024</span> 👍（4） 💬（1）<div>既然都说了 what 和 why，怎么能少了 how 呢？
狗尾续貂，补充下 vim 攻略链接：
http:&#47;&#47;yannesposito.com&#47;Scratch&#47;en&#47;blog&#47;Learn-Vim-Progressively&#47;

左耳朵耗子翻译中文版：https:&#47;&#47;coolshell.cn&#47;articles&#47;5426.html</div>2020-01-06</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/64/05/6989dce6.jpg" width="30px"><span>我来也</span> 👍（2） 💬（5）<div>行内查找命令F&#47;f T&#47;t 可以了解一下。

&#47;&#47; This is mkaing sure that userTotalScore is not

从行尾移到mkaing的k只需要在普通模式下依次按下Fk，两个按键，光标就到k上了。</div>2019-10-04</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/79/4b/740f91ca.jpg" width="30px"><span>-W.LI-</span> 👍（2） 💬（1）<div>vim命令确实很cool，可惜掌握的不好。</div>2019-10-04</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/b1/4d/10c75b34.jpg" width="30px"><span>Johnson</span> 👍（1） 💬（1）<div>vim的多模式特点，让它确实是应用范围最广的编辑器，啥都能搞个vim插件，这一点上emacs真是没法比。不过emacs高人尝尝开发出神级插件(magit，evil)，各有千秋。Spacemacs绝对是值得一番折腾的，其实是将vim的leader key发挥到了极致，再结合evil和emacs丰富的插件，真叫一个酸爽，感兴趣的可以参考我的github的spacemacs 配置https:&#47;&#47;github.com&#47;Johnson9009&#47;dotfiles&#47;blob&#47;master&#47;editor&#47;spacemacs.d&#47;init.el, 高频率用上一个月，别的不敢说，以后在服务器上纯字符界面的开发环境，不会再想用其他的编辑器了。就像项目中说的最好的编辑器既不是VIM也不是Emacs，而是Emacs+Vim。</div>2019-10-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/6e/4c/494b2907.jpg" width="30px"><span>ck</span> 👍（0） 💬（3）<div>在&quot;非vim按键 vim按键&quot; 比较重到达当前单词的结尾的vim 按键应该是e 不是c.</div>2020-05-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/1a/66/2d9db9ed.jpg" width="30px"><span>苦行僧</span> 👍（0） 💬（1）<div>当你发现 vim vim浏览器插件 idea-vim插件 相互配合的时候, 你就能感受到各种快捷键的便捷了</div>2019-11-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/19/09/f2/6ed195f4.jpg" width="30px"><span>于小咸</span> 👍（0） 💬（1）<div>有个小问题，在vs code中使用vim插件的时候，怎样使用命令行打开其他的文件呢？</div>2019-10-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/ee/4f/b9ebc543.jpg" width="30px"><span>Miletos</span> 👍（0） 💬（1）<div>VIM重度使用者，中毒太深，戒不掉了</div>2019-10-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/fd/83/b432b125.jpg" width="30px"><span>鱼_XueTr</span> 👍（0） 💬（1）<div>近几年一直在用Emacs&amp;Vim的Spacemacs</div>2019-10-07</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/51/4d/0aceadde.jpg" width="30px"><span>腾挪</span> 👍（1） 💬（0）<div>原来也是 emacs 大佬啊，膜拜。</div>2021-01-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/9f/fc/0232f005.jpg" width="30px"><span>我要收购腾讯</span> 👍（0） 💬（0）<div>换上机械键盘，使用手掌按压 Ctrl， 小拇指从来没酸过 &gt;_&lt;</div>2022-02-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/19/47/e4/17cb3df1.jpg" width="30px"><span>BBQ</span> 👍（0） 💬（0）<div>之前也认真背过VIM 命令，好久几年没有用过了。最近再打开，发现基本的命令 j, k, w ，&#47; 搜索，i 进入编辑模式, c+w 修改单词， o 添加新行 还记得，感觉已经是在潜意识里面了。
</div>2021-05-07</li><br/>
</ul>