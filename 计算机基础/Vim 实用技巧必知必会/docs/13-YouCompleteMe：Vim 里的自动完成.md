你好，我是吴咏炜。

在集成开发环境里，自动完成是一个非常重要的功能。可是 Vim 并不能真正理解你输入的代码，因此它自身无法提供自动完成的功能。不过，Vim 仍然提供了一些接口，允许第三方的软件实现这样的功能，并和 Vim 自身进行集成。[YouCompleteMe](https://github.com/ycm-core/YouCompleteMe)（简称YCM）就是这样的一个第三方软件，今天，我就为你详细介绍一下它。

YCM 对 C++ 程序员最为适合，它可以提供其他工具实现不了的功能。而且，它也适用于很多其他语言，包括 C 家族的各种语言和其他常用的语言，如 Python、Java 和 Go 等。即使在 YCM 不直接支持你使用的语言的时候，它仍然能通过标识符完成功能提供比没有 YCM（和其他语言支持插件）时更好的编辑体验。因此，我推荐你使用这个插件。

## YouCompleteMe

### 功能简介

首先我来介绍一下 YCM 的基本功能吧。根据它的主页（我的翻译）：

> YouCompleteMe 是一个快速、即输即查、模糊搜索的 Vim 代码完成引擎。它实际上有好几个完成引擎：  
>  
> 
> - 一个基于标识符的引擎，可以在任何编程语言中工作
> - 一个强大的基于 clangd 的引擎，可以为 C/C++/Objective-C/Objective-C++/CUDA（C 家族语言）提供原生的语义代码完成
> - 一个基于 Jedi 的完成引擎，可以支持 Python 2 和 3
> - 一个基于 OmniSharp-Roslyn 的完成引擎，用来支持 C#
> - 一个基于 Gopls 的完成引擎，支持 Go
> - 一个基于 TSServer 的完成引擎，支持 JavaScript 和 TypeScript
> - 一个基于 rls 的完成引擎，支持 Rust
> - 一个基于 jdt.ls 的完成引擎，支持 Java
> - 一个通用的语言服务器协议（LSP）实现，用来支持任何其他有 LSP 服务器的语言
> - 还有一个基于 omnifunc 的完成器，使用 Vim 的全能补全（omnicomplete）系统提供的数据来为很多其他语言提供语义完成
<div><strong>精选留言（16）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/18/4f/a3/0e56b4e5.jpg" width="30px"><span>doge</span> 👍（2） 💬（1）<div>说一下用后感吧，跳转的速度和精度上比vscode和clion要迅速很多，就是快捷键比较多，得多用熟能生巧才行。
另一个就是得ctags+cscope+YCM+rtags一起用才能得到最好的跳转体验。
基本就是C-] \gt \rj \rT轮番上阵，哈哈！
整体感觉还是非常良好的，不过如果CLion没那么卡和吃内存就好了，CLion的类继承关系这一块的体验很好，不知道vim这一块有没有类似的操作，另外CLion的调试也很适合小白使用。但Clion经常用着用着就卡死了，尴尬。
当然如果vim实在玩不转，vscode和CLion还是可以作为替代的，哈哈。
最后一点就是高亮配色方案的事，老师好像比较喜欢朴素的色调，但我看多色调习惯了，最后用了octol&#47;vim-cpp-enhanced-highlight这个插件，但感觉还是挺一般的。不知道有没有大神有啥推荐的配置。
</div>2020-09-03</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTKdzXiawss5gGiax48CJGAJpha4pJksPia7J7HsiatYwjBA9w1bkrDicXfQz1SthaG3w1KJ2ibOxpia5wfbQ/132" width="30px"><span>chris</span> 👍（1） 💬（1）<div>请问老师，我想给ycm的GoToSymbol命令也定义一个快捷键，但发现这个命令不是默认取当前光标下的符号，而是要自己输入带查找的symbol，这样的快捷键应该如何定义？</div>2020-11-07</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/19/51/29/24739c58.jpg" width="30px"><span>凉人。</span> 👍（0） 💬（1）<div>&#47;usr&#47;bin&#47;ld: &#47;home&#47;work&#47;.vim&#47;my&#47;start&#47;YouCompleteMe&#47;third_party&#47;ycmd&#47;third_party&#47;regex-build&#47;3&#47;temp.linux-x86_64-3.6&#47;regex_3&#47;_regex.o(.text+0x112c): unresolvable H��@�&gt;H��FH��H��H��@�~�F�H��@�~H��8�H��H��0�FH��H��(�FH��H�� �FH��H���FH��H���FH��H��F�fD relocation against symbol `_Py_NoneStruct&#39; 安装过程一直失败。看起来是mrab-regex有bug，这个可以跳过吗</div>2022-12-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/25/2b/ca/71ff1fd7.jpg" width="30px"><span>谁家内存泄露了</span> 👍（0） 💬（2）<div>请问老师，我安装了ycm，采用的是在ubuntu上直接用apt安装的方式；
在c++的工程中添加了对应的json文件；
现在的现象是函数&#47;符号能够跳转了，但是无法查找相关的引用即没有这个命令：YcmCompleter GoToReferences，这个问题您有什么思路吗？</div>2022-09-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/5f/09/2ec44412.jpg" width="30px"><span>Qfeng</span> 👍（0） 💬（1）<div>公司内网无法访问网络，只能通过外网电脑下载好后拷贝的方式传输文件进入。这种情况下试过，无法安装YCM，它会在安装的时候访问github，请问老师这种问题可以如何绕过？</div>2022-09-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1a/7f/5f/1d82812f.jpg" width="30px"><span>軟件賺硬幣</span> 👍（0） 💬（1）<div>老师好，我是Linux初学者。我的Ubuntu20.04下面运行了
sudo apt install vim-youcompleteme，
vim-addon-manager install youcompleteme两行代码之后，然后用vim打开新文件，还是用不了ycm。显示NoExtraConfDetected: No .ycm_extra_conf.py file detected, so no compile flags are available…（后面字体看不到了，笔记本屏幕限制）</div>2021-05-29</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/gKnIR8mga02s9xdQoxyJBibmuxHGhfQ8WZicia3Ie4wBQKg4Zc1oVoS03mvaCD46je9xCza25qXc3w6KMckpS0BqQ/132" width="30px"><span>supakito</span> 👍（0） 💬（2）<div>老师，感觉最近tabnine好像很火的样子，不知道和ycm相比，哪个更好用一些？</div>2020-11-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/18/1f/29/c7a69190.jpg" width="30px"><span>浩浩</span> 👍（0） 💬（1）<div>brew list. 安装了一下软件
=============================
autoconf	cmake		fzf		gettext		icu4c		lua		node		pkg-config	python@3.9	ruby		universal-ctags
automake	cscope		gdbm		go		libyaml		macvim		openssl@1.1	python@3.8	readline	sqlite		xz

ycm 只加 clangd  选项以下报错 【我需要自己安装 clangd 吗，请问？】
=======================

Downloading Clangd from https:&#47;&#47;dl.bintray.com&#47;ycm-core&#47;clangd&#47;clangd-10.0.0-x86_64-apple-darwin.tar.bz2...
ERROR: downloaded Clangd archive does not match checksum.
</div>2020-10-25</li><br/><li><img src="" width="30px"><span>gigglesun</span> 👍（0） 💬（1）<div>YouCompleteMe可以通过离线的方式安装吗？ 公司的服务器不能连接外网，我可以在自己的电脑通过

git clone --recurse-submodules \
          --shallow-submodules \
    https:&#47;&#47;github.com&#47;ycm-core&#47;YouCompleteMe.git
装好后，把这个YouCompleteMe文件夹拷贝到公司服务器，然后我再额外的安装对应的语言引擎这样安装吗？</div>2020-10-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/a1/cd/2c513481.jpg" width="30px"><span>瀚海星尘</span> 👍（0） 💬（3）<div>老师我这里 ubuntu 使用 apt install vim-youcompleteme 后，提示找不到引擎，估计是还需要单独安装，最后还是用了编译安装的方式。我也安装了 vim-autopairs，确实带来了很多困扰，最头痛的就是需要只输入一对的第一个符号的情况，每次输入都会自动输出两个，然后删除第二个又会自动把第一个给删除...看了老师的留言，果断把它删除了。������</div>2020-10-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/18/4f/a3/0e56b4e5.jpg" width="30px"><span>doge</span> 👍（0） 💬（1）<div>ubuntu环境按照老师的命令安装rtags失败，报错
rtags&#47;src&#47;rct&#47;rct&#47;Apply.h:46:10: error: unknown
      type name &#39;size_t&#39;; did you mean &#39;std::size_t&#39;?
最后直接下载release 2.3.8的tarball编译成功。。</div>2020-08-31</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/ibZVAmmdAibBeVpUjzwId8ibgRzNk7fkuR5pgVicB5mFSjjmt2eNadlykVLKCyGA0GxGffbhqLsHnhDRgyzxcKUhjg/132" width="30px"><span>pyhhou</span> 👍（0） 💬（1）<div>安老师给的步骤安装了 YCM，试着编辑了 javascript 文件，感觉有几个地方不是太清楚：

1. YCM 中的跳转(GoTo)貌似只能在单个文件中跳转，不能跳转到其它的文件中去？有些时候，如果需要跳转到函数，只能跳转到前面的定义和声明，无法跳转到后面的定义和声明。当无法跳转的时候，右下方会出现 `KeyError: &#39;file&#39;` 的错误，或者是提示你使用命令不恰当的错误

2. YCM 支持回跳吗？就是跳转到一个定义或者声明处，然后再回到跳转前的地方，感觉这个对浏览代码时特别有用

是不是除了安装 YCM，还得相应安装配套的其它插件（比如 C++ 的话就需要 rtags）。感觉好难������</div>2020-08-31</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/cf/db/9693d08f.jpg" width="30px"><span>YouCompleteMe</span> 👍（0） 💬（1）<div>老师，我有两个疑问：
1.截图里是否使用了statusline的插件，我的用了老师的配置，没有显示 [+] &#47; utf-8 &#47; 当前行百分比。
2.老师平时写代码会使用括号自动补全吗～</div>2020-08-26</li><br/><li><img src="" width="30px"><span>know-one</span> 👍（0） 💬（1）<div>请问python有没有哪个插件能显示继承关系？</div>2020-08-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/64/05/6989dce6.jpg" width="30px"><span>我来也</span> 👍（0） 💬（2）<div>有些功能确实很吸引人。
比如自动补全时自动用正则过滤候选词。

曾经我也折腾过ycm，但由于有些东西不会用，自己没调通，最终也放弃了。
要是能早些看到这篇文章，应该会少走不少弯路。

对于老师说的这个重构变量名需要手敲的问题，
:YcmCompleter RefactorRename bar
在golang中有个小插件解决了这个问题，
它是用快捷键在命令行触发一个提示框，告知你想把当前光标下的变量重命名为啥，等你输入完毕按回车后再替换。

这个功能实现起来应该也不复杂。
如果这个重构功能还蛮常用的话，可以折腾一下。</div>2020-08-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/53/a8/abc96f70.jpg" width="30px"><span>return</span> 👍（0） 💬（0）<div>ycm确实难装，以前总想着通过插件方式来装， 今天才知道 其中的原理。 </div>2020-08-26</li><br/>
</ul>