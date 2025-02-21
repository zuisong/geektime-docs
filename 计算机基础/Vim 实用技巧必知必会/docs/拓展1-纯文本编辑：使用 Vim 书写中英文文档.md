你好，我是吴咏炜。

今天是拓展篇的第 1 讲，我想带你对 Vim 的纯文本编辑技巧做一个专项突破。由于 Vim 是在欧美世界诞生的工具，贡献者中也是说英语的人居多，因而它对英文的支持要远远超出其他语言。所以今天，我们就深入讨论一下，如何使用 Vim 来进行纯文本编辑，特别是英文的文本编辑。

熟练掌握这一讲的内容，可以让你使用 Vim 书写中英文文档时都感到游刃有余。如果你有这个需求，一定要亲自动手尝试我提到的这些功能，加深自己的记忆。如果你觉得还需要多花一点时间，消化吸收前几讲的基础知识，也可以先阅读全文，把握要点，之后再回过头来深入学习。

## 为什么不使用字处理器？

你可能已经开始怀疑了，我为什么要使用 Vim 来进行文字编辑？用 Word 不香么？如果嫌 Word 贵，还有免费的 WPS 啊……

嗯，首先，Word 和 WPS 这些字处理器不是用来生成纯文本文件的。在处理纯文本文件上，它们反而会有诸多劣势，如：

- 只能本地使用，既不能在远程 Linux 服务器上运行，也不能用 SSH/SCP 的方式打开远程的文件（除非在服务器上启用 Samba 服务，但体验真的不好）
- 分段和分行一般没有很好的区分
- 如果存成纯文本的话，格式会全部丢失

最后一句话似乎是废话？还真不是，纯文本文件里面是可以存储格式的，但 Word 和其他字处理软件对于文本类型一般只能支持纯文本或富文本（Rich Text），而富文本虽然包含了格式信息，但却对直接阅读不友好。我想，没有人会去手写富文本文件吧。仍有一些带格式的文本文件比较适合手写，下面这些是其中较为流行的格式：
<div><strong>精选留言（6）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/10/dd/09/feca820a.jpg" width="30px"><span>helloworld</span> 👍（2） 💬（1）<div>拼写检查这个，老师是开启的吗，开启后，代码中很多原生关键字都会显式下划线提示错误，造成干扰，这个问题是怎么解决的呢，因为这个原因所以一直没开启这个。</div>2021-07-05</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTKdzXiawss5gGiax48CJGAJpha4pJksPia7J7HsiatYwjBA9w1bkrDicXfQz1SthaG3w1KJ2ibOxpia5wfbQ/132" width="30px"><span>chris</span> 👍（0） 💬（3）<div>请问老师, 插入模式下输中文, 退出后又要切回因为模式, 很麻烦, 有什么自动且输入法的标准方法吗?</div>2020-10-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/a1/cd/2c513481.jpg" width="30px"><span>瀚海星尘</span> 👍（0） 💬（2）<div>原以为就写写文档，应该会很简单，没想到有这么多配置。之前也好奇72是怎么来的，今天算是知道了。另外，那个分行的问题我之前也有困惑，原来是 l 选项默认设置的。</div>2020-09-22</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/ibZVAmmdAibBeVpUjzwId8ibgRzNk7fkuR5pgVicB5mFSjjmt2eNadlykVLKCyGA0GxGffbhqLsHnhDRgyzxcKUhjg/132" width="30px"><span>pyhhou</span> 👍（0） 💬（9）<div>感觉 markdown 还是很实用的。看了两遍，跟着老师的描述操作了一遍，有些地方还是不是特别清楚

按我的理解，在 .vimrc 中设置了 textwidth，当一行的文字超过了 textwidth 的设定值就会自动回转到新的一行？但是调了好久，一行的长度都是vim窗口的长度。

formatoptions 那里，上节课，我记得老师用的是 m 选项而不是 n ？想要有 markdown 下的列表的换行自动缩进功能，需要在老师的配置基础上更改吗？我试了一下，好像这个功能也出不来

看网上一些帖子， markdown 还可以和 tagbar 配合着来使用，不知道效果有没有提升。

平时 markdown 用的比较多，但都是用像 macdown 那种图形编辑器。很想尝试下用 vim，但鉴于自己对 vim 的熟悉程度，还需要多多尝试😂</div>2020-08-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/cf/db/9693d08f.jpg" width="30px"><span>YouCompleteMe</span> 👍（0） 💬（1）<div>模式行有什么常用的组合吗，比如示例README里的 ”：
&lt;!--
vim:autoindent:expandtab:formatoptions=tcqlmn:textwidth=72:
--&gt;</div>2020-08-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/64/05/6989dce6.jpg" width="30px"><span>我来也</span> 👍（0） 💬（1）<div>学习了.

虽然平常也在用vim写markdown,但是没这么讲究过,都是自己手动处理一些边界情况.
之前也从没有想过在这个方向上折腾.
等有时间了,我再参考本文把我的配置调整一下.

说起vim写markdown,我用的是插件[markdown-preview.nvim](https:&#47;&#47;github.com&#47;iamcco&#47;markdown-preview.nvim)来实时预览.
不知道其他小伙伴有没有更好的推荐.
</div>2020-08-19</li><br/>
</ul>