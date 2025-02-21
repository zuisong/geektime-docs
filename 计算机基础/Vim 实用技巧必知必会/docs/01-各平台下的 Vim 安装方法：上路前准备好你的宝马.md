你好，我是吴咏炜。

今天第一讲，我们先来讨论一下 Vim 在 Linux、macOS、Windows 系统下的安装和配置问题。

Vim 在 Linux 和 macOS 上一般是默认安装的，在 Windows 上不是。不过 Vim 的网站上提供了 Windows 下的安装包，自己安装也很容易。所以，今天的课程我不会手把手、一步步地讲，而是挑选一些重点。对于默认安装的情况，主要讨论的是版本老旧或功能不全的问题。对于其他情况，我则会给出一个基本指引，减少你走弯路的可能性。

好了，下面我们就分各个不同的平台，一一来看。

## Linux 下的安装

### Red Hat 和 CentOS 系列

在 Red Hat Linux 和 CentOS Linux 上，默认安装的 Vim 可能是一个最小功能的版本。虽然这个版本启动速度很快，但它缺少了很多对开发有用的功能，如语法加亮、Python 集成和图形界面。一般情况下，应至少安装更全功能版本的 Vim；如果能使用 X Window 的话，则应安装图形界面版本。

你可以通过下面的命令来查看已经安装的 Vim 版本：

```bash
yum list installed | grep vim
```

如果输出只有下面这样的内容的话，就说明安装的 Vim 版本只有基本功能：

> `vim-minimal.x86_64 2:8.0.1763-13.el8 @System`
<div><strong>精选留言（30）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/0f/57/4f/6fb51ff1.jpg" width="30px"><span>奕</span> 👍（5） 💬（3）<div> vim 的配置文件放到 用户目录下 .vimrc 和 放到 .vim 文件夹下的 有什么区别的？</div>2020-07-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/64/05/6989dce6.jpg" width="30px"><span>我来也</span> 👍（4） 💬（2）<div>前天看老师的直播,发现可以用airline在顶部展示buffer信息.
今天特意花了点时间,弄了一下,发现几乎可以替换之前的`minibufexpl.vim`了.
(minibufexpl.vim 已经有大几年没人维护了,😭)

由于我经常开很多buffer,需要在不同的buffer间跳转,所以我都配置了快捷键.
配置很简单:
```
let g:airline#extensions#tabline#enabled = 1            &quot; 展示顶部的状态栏
let g:airline#extensions#tabline#buffer_nr_show = 1     &quot; 展示:buffers中的序号 便于通过:buffer number 跳转
let g:airline#extensions#tabline#buffer_idx_mode = 3    &quot; 展示buffer的序列号&lt;连续递增&gt; 可以通过快捷键快速切换到指定buffer

&quot; 定义快捷键 空格+数字 跳转到指定序号的buffer
for i in range(1, 99)
  exe printf(&#39;nmap &lt;silent&gt; &lt;Space&gt;%d &lt;Plug&gt;AirlineSelectTab%02d&#39;, i, i)
endfor
```
</div>2020-07-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1b/a7/08/a7e03564.jpg" width="30px"><span>冰糕🍦</span> 👍（3） 💬（2）<div>内网环境，有没有离线装插件的好方法？</div>2020-07-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1e/a4/6d/7da41e79.jpg" width="30px"><span>oaeen</span> 👍（3） 💬（4）<div>请问在 VS Code 下使用 Vim 插件 和直接使用 Vim 比起来怎么样？推荐这种方式吗</div>2020-07-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1f/b9/59/ac75a02a.jpg" width="30px"><span>吴 谦</span> 👍（2） 💬（2）<div>请问老师，我手动安装的vim，在家目录里没找到.vim文件夹</div>2021-12-25</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/22/e1/7a/b206cded.jpg" width="30px"><span>人在江湖龙在江湖</span> 👍（2） 💬（2）<div>看了这篇文章，觉得只需要安装linux就行了，现在有docker,不论在mac或者Windows上，装个docker,搞个linux,就像在本地机上一样快，不像vmware虚拟机，占用资源太多，开了个vmware,本地机器其他软件都用不了</div>2020-11-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/db/64/06d54a80.jpg" width="30px"><span>中年男子</span> 👍（2） 💬（1）<div>再一次被吴老师折服了，每个问题都耐心的回答了，读吴老师的专栏总是能收获比专栏价值更大东西。</div>2020-07-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/64/05/6989dce6.jpg" width="30px"><span>我来也</span> 👍（2） 💬（4）<div>我习惯了hhkb的键位后，在别人的电脑上确实会相当不习惯。

大小写锁定键不推荐更换为ESC，因为Ctrl+[就是ESC键的效果。
在自定义的组合键中，Ctrl和Leader健是使用非常频繁的。

也有神人把连按两次大小写锁定键替换为Esc，理论上是可行的，但我没这么干。</div>2020-07-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/d4/78/66b3f2a2.jpg" width="30px"><span>斯盖丸</span> 👍（1） 💬（1）<div>老师有个问题百思不得其解。我新买的Mac notebook，现在Esc在touchpad上。问题是我每次按Esc和其他Fn的功能键时都会出现个圆形顺时针的进度条，只有进度条转了一圈后Esc才会生效。这样一来我的Esc就比正常情况下慢很多。怎么取消这个进度条，好让我每次按一下Esc就可以呢？谷歌了一圈没有找到方法…我也想尽量不改键，因为我还是新手。谢谢老师请指导一下。</div>2021-02-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/74/a9/5eb3ebc6.jpg" width="30px"><span>唐龙</span> 👍（1） 💬（2）<div>感谢老师的中文帮助文档，对我帮助很大，英文文档真的看不进去。
之前学习正则有些功能不知道在vim里怎么用，也在文档里找到了，甚至有一些和Perl正则的语法对比。
今天也重新试着安装了一下YCM，终于成功了，以前试过两次都失败了。
感觉最近比较顺，期待后续课程。</div>2020-07-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1f/b4/ad/94c0ae00.jpg" width="30px"><span>Nlife</span> 👍（1） 💬（1）<div>工作中，服务器通常是没有装window图形界面的，开发环境也是securityCRT或xshell等方式连接后进行。vim通过源码安装gui支持选项配的是auto，安装后查看版本结果是Huge version without GUI。

请问老师这个结果是对的吗？

再请问支持图形界面和不支持图形界面，主要差别在哪些重要的功能呢？能先简单举例一下吗？</div>2020-07-22</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTKU8b6w5Y9WYjOrpnqI4UcLLjpMuFfZBshrCHmK556syicvyiaoqDvPjr5rzI7pESsEoSHJ88ywnv7Q/132" width="30px"><span>剑米</span> 👍（1） 💬（3）<div>通过putty这类工具ssh到服务器，然后通过vim打开文件，使用的vim都是服务器配置的vim，但是由于无法获取sudo权限，导致在home目录下定制自己的vim遇到好多困难，依赖太多的库，最终放弃。老师是否可以提供一个教程，针对无sudo权限在用户目录下安装自己的vim，</div>2020-07-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/57/4f/6fb51ff1.jpg" width="30px"><span>奕</span> 👍（1） 💬（1）<div>Mac 执行 vim --version 会列出 vim 支持的功能 有的前面有 + 有的是 -, 现在想安装某个缺失的功能应该怎么去做的？ 比如 要支持 python3（Mac 自带的 vim）</div>2020-07-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1f/a5/f7/45d83f77.jpg" width="30px"><span>一条大老蛇</span> 👍（1） 💬（8）<div>将一个窗口vim内的内容复制到另外一个窗口给我造成了很大的困扰。看了各种回答我也没搞懂+寄存器到底怎么用。希望老师能给个解决，让系统剪切板脱离鼠标！</div>2020-07-20</li><br/><li><img src="" width="30px"><span>闲来</span> 👍（1） 💬（5）<div>请问，我的macvim配置和neovim配置光标游走都会出现卡顿现象，如何诊断原因和解决问题？</div>2020-07-20</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/PiajxSqBRaELIXTAcO8unnrCT0C0JqIOLfXnBvsXFRanBcl4vKR82AsEPnUaibEiaJcBmwICn2HjskfKaaxeWN9iab0evwBoLwofMh9b3bbh4Ezn27FfgwwSIQ/132" width="30px"><span>Geek_3dbca6</span> 👍（0） 💬（1）<div>想问一下老师，按这个教程在win下填写配置项的时候显示只可读要怎么处理呢？</div>2023-05-24</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/PiajxSqBRaEJsAzWfG8S3R53U8b2MJtLm5RxVnOjaUoLplicXp2KK7OicOf0GMV8MqPW7AfcqWzicZgficZ14Elcumw/132" width="30px"><span>fakefish</span> 👍（0） 💬（1）<div>老师，请教一下，我在vscode上安装vim，daw命令是删除一个word，但是在vscode里面因为a是插入模式，就直接进入了插入模式，而不是删除，我应该怎么办呢，或者是说在vscode里面使用vim有些命令不生效</div>2021-12-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/32/c3/3ca99b1e.jpg" width="30px"><span>Allen Lei</span> 👍（0） 💬（1）<div>老师您好，如何设置Macvim为默认打开方式，在应用程序上面选不到macvim.app，创建了链接也不行，求告知</div>2021-12-01</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/cd/e0/c85bb948.jpg" width="30px"><span>朱雯</span> 👍（0） 💬（1）<div>学习vimtutor的时候有一个问题一直困扰我，上下左右时hjkl，但是当你切换到插入模式的时候，你要移动你的光标，就又是上下左右，或者esc，这种时候，就让我频繁的切换到键盘的左上角和右下角，反而对我的使用极其不利，这样下来，降低了我对vim的感官，屡屡放弃。</div>2020-12-06</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/d8/45/a74136fc.jpg" width="30px"><span>Isaac Zhou</span> 👍（0） 💬（1）<div>请问在树莓派RaspberryOS上推荐哪个版本呢？按理说应该是和Debian一样，但是资源更有限，自带的vim 8.1能用吗？</div>2020-08-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/49/f2/25cfa472.jpg" width="30px"><span>寒溪</span> 👍（0） 💬（2）<div>mac 执行”LANG=zh_CN.UTF-8 vimtutor“ 打开的一直是英文版教程，请问是我的系统设置问题吗？
</div>2020-08-18</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/aFAYPyw7ywC1xE9h1qibnTBwtWn2ClJqlicy5cMomhZVaruMyqSq76wMkS279mUaGhrLGwWo9ZnW0WCWfmMovlXw/132" width="30px"><span>木瓜777</span> 👍（0） 💬（1）<div>老师，ubuntu自带的vim 需要卸载，再重新装吗？</div>2020-08-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/dd/7d/1c70c805.jpg" width="30px"><span>...</span> 👍（0） 💬（1）<div>请问ce和cw命令有什么区别？
</div>2020-08-04</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/5b/de/152f1c2c.jpg" width="30px"><span>Warn</span> 👍（0） 💬（2）<div>吴老师，你好 安装中文文档时，使用`cd ~&#47;.vim`目录不存在，macOS环境下，配置文件路径`~&#47;.zshrc`,使用brew安装的macvim.
只找到了`&#47;usr&#47;local&#47;bin&#47;`目录下有vim和mvim两个文件。这个正确路径应该怎么找呢</div>2020-08-03</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/53/a8/abc96f70.jpg" width="30px"><span>return</span> 👍（0） 💬（2）<div>先给老师点个赞，市面上讲的最好的vim教程，没有之一。
刚开始 apt install vim
发现  &quot;+   死后粘贴不料系统的剪切版
按照老师的方法， 重新装了  apt install vim-gtk3  又可以了。
请教老师一下， 个人觉得  &quot;+ 这个功能是一个vim的基础功能，这个也和 vim 安葬的 功能集大小有关系吗。</div>2020-08-02</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/8d/ed/ea2cbf3a.jpg" width="30px"><span>Sinclairs</span> 👍（0） 💬（1）<div>工作中经常要在不同的 windows 机器上切换, 每换个环境都要重新安装 vim 还是比较麻烦的.
于是想弄一个 portalbe 的版本, 但是还不清楚如何设置这个版本的配置文件,
不知道老师有没好的建议, 谢谢.</div>2020-08-01</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1b/96/47/93838ff7.jpg" width="30px"><span>青鸟飞鱼</span> 👍（0） 💬（1）<div>老师你好，我是windows的，可是我下载了好多次都不成功，每次都是几k的速率，一分钟不到就断了，怎么办？</div>2020-07-30</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/9b/00/8c1b9631.jpg" width="30px"><span>王建</span> 👍（0） 💬（5）<div>putty远程服务器，无桌面环境，如何设置 esc  为 大写锁定键

</div>2020-07-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/25/b2/abb7bfe3.jpg" width="30px"><span>三千世界3039</span> 👍（0） 💬（2）<div>老师，manjaro中有没有带图形界面的vim啊 ， 一直都是用命令行，</div>2020-07-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1f/43/2a/bfc4472e.jpg" width="30px"><span>Geeker-new</span> 👍（0） 💬（1）<div>老师，Mac环境下使用homebrew安装Macvim出现了问题。输入官网安装代码后，发生如下报错：curl: (7) Failed to connect to raw.githubusercontent.com port 443: Connection refused；不知道有没有简便的解决方法。</div>2020-07-28</li><br/>
</ul>