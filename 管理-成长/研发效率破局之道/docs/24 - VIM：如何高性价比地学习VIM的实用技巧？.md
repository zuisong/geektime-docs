你好，我是葛俊。今天，我来和你聊聊VIM的使用技巧。

在“[特别放送 | 每个开发人员都应该学一些VIM](https://time.geekbang.org/column/article/144470)”这篇文章中，我和你详细介绍了VIM提高研发效能背后的原因。我推荐每个开发者都应该学一些VIM的原因，主要有两个：

- 独特的命令模式，可以大量减少按键次数，使得编辑更高效；
- 支持跨平台，同时可以在很多其他IDE、编辑器中作为插件使用，真正做到一次学习，处处使用。

VIM确实可以帮助我们提高效率，但面对这样一个学习曲线长而且陡的编辑器，我们很容易因为上手太难而放弃。所以，如何性价比高地学习VIM的使用技巧非常重要。

我推荐你按照以下三步，来高效地学习如何使用VIM：

1. 学习VIM的命令模式和命令组合方式；
2. 学习VIM最常用的命令；
3. 在自己的工作环境中使用VIM，比如与命令行环境的集成使用。

接下来，我们分别看看这三步吧。

## VIM的模式机制

VIM的基本模式是命令模式，在命令模式中，敲击主体键的效果不是直接插入字符，而是执行命令实现对文本的修改。

### 使用VIM的最佳工作流

在我看来，在命令模式下工作，效率高、按键少，所以我推荐你**尽量让VIM处于命令模式，使用各种命令进行工作。进入编辑模式完成编辑工作之后也立即返回命令模式。**

事实上，我们从命令模式进入编辑模式修改文件，之后再返回命令模式的全过程，就是一个编辑命令。它跟其他的命令，比如使用dd删除一行，并没有本质区别。接下来，我们一起看个具体的例子吧。
<div><strong>精选留言（11）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/0f/4b/4a/a142542a.jpg" width="30px"><span>吴新星</span> 👍（4） 💬（2）<div>老师你好 在使用vim的过程中 一直被中文输入法困扰着：

在Insert模式下录入中文，然后进入Normal模式进行一些操作，这时候一定要把输入法切换成英文，否则录入的命令会被输入法拦截，当操作完成后又需要进入到Insert模式录入中文，这时候又需要切换输入法，多出来的两次输入法切换，比较影响效率

请问老师有好的解决方案吗（我在Mac环境下使用vim）
</div>2019-12-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/ba/bd/6f2f078c.jpg" width="30px"><span>Marvin</span> 👍（4） 💬（1）<div>gg到文档头，o插入行，yy复制行，p粘贴，s删除并进入编辑，a光标移动到当前字之后进入编辑，v&#47;ctrl+v视图选择，ctrl+i移动到行首进入编辑…喜欢vim，服务器无障碍，nice。</div>2019-10-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/64/05/6989dce6.jpg" width="30px"><span>我来也</span> 👍（3） 💬（2）<div>我常用的几个小命令：
普通模式下的 zt zz zb
用于把当前行移动到窗口顶部&#47;中间&#47;底部。

再就是插入模式下的Ctrl+o，再结合zz。
从编辑模式临时切回普通模式，执行了一个命令后继续回到编辑模式。
避免按esc退出编辑模式。</div>2019-10-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/fc/80/21d67b9b.jpg" width="30px"><span>二狗</span> 👍（1） 💬（3）<div>在Windows下用gvim学vim。d的组合键怎么用
我按d的组合键容易触发长按效果dd
比如我按dw 结果把整个文本全删了
按d（  结果触发d+shift 把光标后面都删了</div>2019-11-01</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/19/09/f2/6ed195f4.jpg" width="30px"><span>于小咸</span> 👍（1） 💬（1）<div>发现了葛俊老师的个人博客！</div>2019-10-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/17/27/ec30d30a.jpg" width="30px"><span>Jxin</span> 👍（1） 💬（1）<div>刚好明天周末，开始照着练手。</div>2019-10-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/c7/5f/2028aae5.jpg" width="30px"><span>搏未来</span> 👍（1） 💬（1）<div>看完发现我是小白，去学习了</div>2019-10-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/1c/4b/2e5df06f.jpg" width="30px"><span>三件事</span> 👍（0） 💬（2）<div>老师 在一个1000多行文件里 我需要在三个不同的方法里改代码，要来回切换这三个方法。有没有啥好的办法？我现在是用 m 进行标记，但感觉还是不方便。</div>2020-03-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/18/75/ec/c60b29f5.jpg" width="30px"><span>Alvin-L</span> 👍（0） 💬（1）<div>我在其他通用编辑器里有这么个功能，ctrl+d是向下复制一行当前行内容。vim里的操作就要yyp，如何设置成ctrl+d同样功能呢，这个习惯了</div>2019-11-13</li><br/><li><img src="" width="30px"><span>Geek_a03aa5</span> 👍（1） 💬（0）<div>推荐两个高性价比插件

1. vim-surround 方便快捷地编辑成对的符号
2. easymotion 搜索并移动光标到指定位置</div>2021-12-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/cc/7e/0d050964.jpg" width="30px"><span>Rootrl</span> 👍（0） 💬（0）<div>关于那个可是模式多行编辑，老师演示的是VS 编辑器，其他终端中使用（比如MobaXterm)好像不行，选中多行后，按c想编辑，但只能编辑第一行</div>2022-05-25</li><br/>
</ul>