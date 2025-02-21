你好，我是吴咏炜。

在前几讲，我已经介绍了不少 Vim 的常用命令，我想你已经略有心得了吧。今天我们转换一下视角，来讲一下 Vim 这个软件本身。

作为一个 Vim 的使用者，光熟悉命令是不够的，你还需要定制 Vim。因为每个人的习惯和需求都是不一样的，一个高度定制化的 Vim 环境能大大提高你的工作效率。

今天，我会先带你了解一下 Vim 的运行支持文件目录结构，然后我们再一起探索 Vim 8 带来的新功能，及如何对 Vim 进行初步配置来使得 Vim 更加好用。

## Vim 的目录结构

Vim 的工作环境是由运行支持文件来设定的。如果你想要定制 Vim，就要熟知 Vim 有哪些不同类型的运行支持文件，分别存放在哪里，怎样能快捷地找到它们。Vim 比较有意思的一点的是，虽然运行支持文件是在 Vim 的安装目录下，但用户自己是可以“克隆”这个目录结构的。也就是说，你自己目录下的用户配置，到你深度定制的时候，也有相似的目录结构。所以，我就先从这些文件的目录结构开始讲起。

### 安装目录下的运行支持文件

Vim 的运行支持文件在不同的平台上有着相似的目录结构。以 Vim 8.2 为例，它们的标准安装位置分别在：

- 大部分 Unix 下面：/usr/share/vim/vim82
- macOS Homebrew 下：/usr/local/opt/macvim/MacVim.app/Contents/Resources/vim/runtime
- Windows 下：C:\\Program Files (x86)\\Vim\\vim82
<div><strong>精选留言（28）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/19/1c/47/53c48284.jpg" width="30px"><span>吴咏炜</span> 👍（7） 💬（6）<div>由于 minpac 本身的修改，文中给出的需要加到 .vimrc 中的代码目前应改成：

if exists(&#39;g:loaded_minpac&#39;)
  &quot; Minpac is loaded.
  call minpac#init()
  call minpac#add(&#39;k-takata&#47;minpac&#39;, {&#39;type&#39;: &#39;opt&#39;})

  &quot; Other plugins
endif

if has(&#39;eval&#39;)
  &quot; Minpac commands
  command! PackUpdate packadd minpac | source $MYVIMRC | call minpac#update()
  command! PackClean  packadd minpac | source $MYVIMRC | call minpac#clean()
  command! PackStatus packadd minpac | source $MYVIMRC | call minpac#status()
endif

请大家注意一下。

示例的 Git 库里的指定标签上仍然是老的代码。最新的代码则已经调整过。</div>2020-10-25</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/ibZVAmmdAibBeVpUjzwId8ibgRzNk7fkuR5pgVicB5mFSjjmt2eNadlykVLKCyGA0GxGffbhqLsHnhDRgyzxcKUhjg/132" width="30px"><span>pyhhou</span> 👍（5） 💬（1）<div>赞，理清了 vim 的文件和配置架构，以及 .vim 文件的由来。

另外请教老师一个问题，在 Mac 下，我看到 vim 是有两个安装位置的：

&#47;usr&#47;share&#47;vim&#47;vim82
&#47;usr&#47;local&#47;opt&#47;macvim&#47;MacVim.app&#47;Contents&#47;Resources&#47;vim&#47;runtime

我在想，之前的配置都是基于 Homebrew 下安装的 macvim，那么是否可以考虑将 &#47;usr&#47;share&#47;vim&#47; 直接 rm -rf 删除掉？避免两个版本的 vim 造成混淆？
</div>2020-08-04</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/60/71/895ee6cf.jpg" width="30px"><span>分清云淡</span> 👍（4） 💬（1）<div>求问老师，文章中的 gif 动图有什么工具制作的，特别是动图中 大大的按键提示。多谢</div>2020-08-02</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/57/4f/6fb51ff1.jpg" width="30px"><span>奕</span> 👍（3） 💬（2）<div>怎么查看 runtimepath 这个环境变量的？直接 echo 出来是空的</div>2020-08-02</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1f/7a/6b/1b021705.jpg" width="30px"><span>大狗爱吃鱼</span> 👍（2） 💬（1）<div>PackUpdate命令后等很久很久，也没有安装好，请问下这是怎么回事啊？</div>2020-10-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/db/d8/e090658c.jpg" width="30px"><span>JRTx</span> 👍（1） 💬（1）<div>每次执行PackUpdate，GVIM下方就会提示&quot;Minpac has not been initialized. Use the default val Press ENTER or type command to continue&quot;
系统环境：Windows 7 旗舰版
VIM版本：8.2.1845
配置文件采用的tag是l4-windows。经查阅GitHub上的Minpac源码发现与此段源码有关
function! s:ensure_initialization() abort
  if !exists(&#39;g:minpac#opt&#39;)
    echohl WarningMsg
    echom &#39;Minpac has not been initialized. Use the default values.&#39;
    echohl None
    call minpac#init()
  endif
endfunction
对Vimscript不熟悉，希望老师能够指正。</div>2020-10-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1f/ea/95/3f2539cc.jpg" width="30px"><span>__@948CSheLL</span> 👍（1） 💬（1）<div>老师您好，请问vim中的菜单是什么，我该如何在vim中显示出菜单？</div>2020-08-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/2c/c7/89/16437396.jpg" width="30px"><span>极客酱酱</span> 👍（0） 💬（1）<div>eunuch.vim插件很实用
:Remove: Delete a file on disk without E211: File no longer available.
:Delete: Delete a file on disk and the buffer too.
:Move: Rename a buffer and the file on disk simultaneously. See also :Rename, :Copy, and :Duplicate.
:Chmod: Change the permissions of the current file.
:Mkdir: Create a directory, defaulting to the parent of the current file.
:Cfind: Run find and load the results into the quickfix list.
:Clocate: Run locate and load the results into the quickfix list.
:Lfind&#47;:Llocate: Like above, but use the location list.
:Wall: Write every open window. Handy for kicking off tools like guard.
:SudoWrite: Write a privileged file with sudo.
:SudoEdit: Edit a privileged file with sudo.</div>2023-02-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/28/86/cf/3764011f.jpg" width="30px"><span>bianf</span> 👍（0） 💬（2）<div>我在将留言第一条的语句配置到.vimrc文件中后，执行命令:PackUpdate,提示E117, 未定义的函数，minpac#update,请问是什么原因，要如何解决</div>2022-02-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/cd/e0/c85bb948.jpg" width="30px"><span>朱雯</span> 👍（0） 💬（2）<div>centos7 vim8.0 minpac root用戶可以安裝插件，但是普通用戶不能安裝，一直報錯minpac error(129) :
老師給的兩個配置偶讀沒有用。。。</div>2020-12-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/10/3d/b3991de7.jpg" width="30px"><span>dulp</span> 👍（0） 💬（1）<div>mac里面设置唤醒菜单那块代码没用</div>2020-12-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/4f/3f/6f62f982.jpg" width="30px"><span>wangkx</span> 👍（0） 💬（1）<div>老师，安装完minpac后，添加其他插件，在命令模式下显示
Minpac has not been initialized. Use the default values.

这个问题怎么处理呀，上网没找到解决方案</div>2020-10-28</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTKdzXiawss5gGiax48CJGAJpha4pJksPia7J7HsiatYwjBA9w1bkrDicXfQz1SthaG3w1KJ2ibOxpia5wfbQ/132" width="30px"><span>chris</span> 👍（0） 💬（1）<div>安装完 yegappan&#47;mru 包启动gvim发生报如下错误, 不影响mru功能的使用, 但好多其他菜单不见了, 请问老师知道是什么问题吗?
处理 &#47;usr&#47;share&#47;vim&#47;vim81&#47;menu.vim 时发生错误:
第  129 行:
E329: 没有菜单 &quot;&amp;Print&quot;</div>2020-09-15</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/18/0b/6a/90ca5930.jpg" width="30px"><span>裕</span> 👍（0） 💬（2）<div>使用 :PackUpdate 命令 会报下面错误，请问是什么问题阿

Error detected while processing function minpac#update:
line    2:
E117: Unknown function: minpac#impl#update
Press ENTER or type command to continue
</div>2020-08-31</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/20/c3/ca/9ffef865.jpg" width="30px"><span>老王</span> 👍（0） 💬（3）<div>Vim的安装目录是什么？用户目录又是什么呢？</div>2020-08-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/20/c3/ca/9ffef865.jpg" width="30px"><span>老王</span> 👍（0） 💬（1）<div>我用的是16.04 unbuntu，是否支持vim8?</div>2020-08-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/64/33/f5f5c407.jpg" width="30px"><span>韩德田Tivens</span> 👍（0） 💬（2）<div>我的mac笔记本，得这样let do_syntax_sel_menu = 1|runtime!synmenu.vim设置后vim -g打开后才是默认显示菜单的，如果let do_syntax_sel_menu = 1，则不可以。
</div>2020-08-25</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1f/ea/95/3f2539cc.jpg" width="30px"><span>__@948CSheLL</span> 👍（0） 💬（1）<div>老师您好，我想请问一下我在ubuntu上下载的vim-gtk3，8.1的版本，命令行模式打开vim，可是没有显示菜单栏，请问我该怎么调出来呢？</div>2020-08-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/19/01/6d/d29a4ad7.jpg" width="30px"><span>Dev</span> 👍（0） 💬（1）<div>Valloric&#47;YouCompleteMe这个插件无法安装</div>2020-08-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/a1/cd/2c513481.jpg" width="30px"><span>瀚海星尘</span> 👍（0） 💬（1）<div>用的vim-pug加1，它的结构是简单了，但是就不容易和vim的默认目录结构对上~所以也一直以为vim是按照关联放置的相关文件，今天才知道，原来是按unix style的类型放置的啊！等后面学深了研究看看vim-plug是咋工作的~</div>2020-08-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1f/ea/95/3f2539cc.jpg" width="30px"><span>__@948CSheLL</span> 👍（0） 💬（1）<div>老师您好，请问let do_syntax_sel_menu = 1的功能是在菜单中显示文件类型，我该怎么才能看出加上他和不加上他的效果呢</div>2020-08-06</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1f/ea/95/3f2539cc.jpg" width="30px"><span>__@948CSheLL</span> 👍（0） 💬（1）<div>老师您好，我想请问一下let do_syntax_sel_menu = 1设置了之后，我该如何在vim菜单中显示文件内容呢？</div>2020-08-06</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/a3/d2/69356194.jpg" width="30px"><span>Woong</span> 👍（0） 💬（1）<div>怎么让文件直接在终端打开，而不另启MacVim。
但是配置使用MacVim的配置。</div>2020-08-04</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/5d/30/a9d12bdb.jpg" width="30px"><span>ChamPly</span> 👍（0） 💬（1）<div>现在的包管理应该是vim-plug用的比较多了吧</div>2020-08-04</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/57/4f/6fb51ff1.jpg" width="30px"><span>奕</span> 👍（0） 💬（1）<div>使用的是 vim-plug 包管理工具，但是在自己的 vim 目录生成的是 plugged 目录，没有使用 plugin 文件夹，这应该是 plug 工具自己进行处理了</div>2020-08-02</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/31/5e/d7cdc1d6.jpg" width="30px"><span>江厚宏</span> 👍（0） 💬（3）<div>老师你好，我是mac电脑，下了minpac之后，总会出现如：Invalid expression: exists(&#39;loaded_mru&#39;)^M 这种报错，我只能一个文件一个文件执行：:set fileformat=unix。
很麻烦，有没有一劳永逸的办法？</div>2020-08-02</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/53/a8/abc96f70.jpg" width="30px"><span>return</span> 👍（0） 💬（2）<div>git clone https:&#47;&#47;github.com&#47;k-takata&#47;minpac.git \ ~&#47;.vim&#47;pack&#47;minpac&#47;opt&#47;minpac
请教老师， 中间 的 反斜杠 \  有啥讲究吗， 因为我感觉 加不加 都行吧。
</div>2020-08-02</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/88/07/7804f4cc.jpg" width="30px"><span>逗逼师父</span> 👍（3） 💬（0）<div>迫不及待要学后面的内容了</div>2020-07-31</li><br/>
</ul>