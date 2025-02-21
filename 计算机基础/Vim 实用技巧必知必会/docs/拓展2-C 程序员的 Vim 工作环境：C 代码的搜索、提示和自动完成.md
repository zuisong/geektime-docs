你好，我是吴咏炜。

从今天开始，我们会用连续 3 讲，深入讨论怎么为编程定制环境。如果你是 C 程序员，那么今天这一讲对你来说毫无疑问是必修课。如果你用的是类 C 语言，也能从这一讲中学到很多有用的内容，尤其是在语法加亮精调、tags 和 Clang-Format 部分。

## 语法加亮精调

在[第 4 讲](https://time.geekbang.org/column/article/267765)中我们已经学到了，Vim 能根据文件类型对代码进行加亮。在[第 12 讲](https://time.geekbang.org/column/article/275752)里，我们还进一步讨论了 Vim 实现语法加亮的细节，知道这些是如何通过代码来进行控制的。对于 C（含其他基于 C 的语言如 C++），语法加亮文件有一些精调选项，还挺有意思，能应对一些特殊场景的需求。我一般会设置以下几项：

```vim
let g:c_space_errors = 1
let g:c_gnu = 1
let g:c_no_cformat = 1
let g:c_no_curly_error = 1
if exists('g:c_comment_strings')
  unlet g:c_comment_strings
endif
```

第一项 `c_space_errors` 用来标记空格错误，包括了 tab 字符前的空格和行尾空格，这样设置之后 Vim 会把这样的空格加亮出来。

第二项 `c_gnu` 激活 GNU 扩展，这在 Unix 下一般是必要的。
<div><strong>精选留言（10）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/25/2b/ca/71ff1fd7.jpg" width="30px"><span>谁家内存泄露了</span> 👍（2） 💬（3）<div>吴老师，你好，我有两个问题：
1 cscope有时候找不到一些c++文件的函数（我执行的命令为：cscope -Rbq）？
2 我有一部分的工作场景是需要用yocto去构建整个Linux的镜像，而且大部分的语言会用的是c++，基于问题1，可能cscope不是万能的，再考虑ycm又需要导出cmake的compile_commands.json文件，这个不清楚怎么在yocto下导出来。。。
基于以上描述，吴老师有什么建议吗？</div>2022-09-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/64/05/6989dce6.jpg" width="30px"><span>我来也</span> 👍（2） 💬（1）<div>如果能早几年看到这系列文章,我正式切换到vim开发的时间也许会提前几年了.

我的vim定制始于这篇文章
[手把手教你把Vim改装成一个IDE编程环境(图文)](https:&#47;&#47;blog.csdn.net&#47;wooin&#47;article&#47;details&#47;1858917)

虽然这篇文章写于2007年,但我看到时应该也是12年了.
当时即使是照着文章把插件都装好了,也花了不少功夫.
搞完后,我对vim真是有了新的认识.原来还可以这么用.

当时有些配置我并没有调通.
不知是自己配置错误,还是文章中插件的配置发生了变化.
但周边也没有可以交流的人.
导致真正完全用vim做开发并不是很顺手.

我就用vim做c代码的查看器,用它去跳转,搜索,对比,
偶尔用它完成小的bug修复.
</div>2020-08-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1f/e0/9b/fc1e6047.jpg" width="30px"><span>大敏</span> 👍（0） 💬（1）<div>请教一下大神，如果工程代码是，C&#47;C++ 混合代码，ctags参数该如何选择呢？</div>2023-08-15</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/a8/bf/ec6de2ad.jpg" width="30px"><span>Alex</span> 👍（0） 💬（1）<div>学到目前阶段，感觉吴老师真是实打实的布道者，我也是守旧之人，只喜欢Linux、vim、c,其余的真心不想碰</div>2021-09-25</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/ee/12/77ddaeb8.jpg" width="30px"><span>Yabo</span> 👍（0） 💬（1）<div>插件 ludovicchabant&#47;vim-gutentags，跳转链接不对，应该是 https:&#47;&#47;github.com&#47;ludovicchabant&#47;vim-gutentags</div>2020-11-18</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTKdzXiawss5gGiax48CJGAJpha4pJksPia7J7HsiatYwjBA9w1bkrDicXfQz1SthaG3w1KJ2ibOxpia5wfbQ/132" width="30px"><span>chris</span> 👍（0） 💬（1）<div>cscope不支持c++的话, 请问如何用vim打造一个c++开发环境呢?</div>2020-11-02</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTKdzXiawss5gGiax48CJGAJpha4pJksPia7J7HsiatYwjBA9w1bkrDicXfQz1SthaG3w1KJ2ibOxpia5wfbQ/132" width="30px"><span>chris</span> 👍（0） 💬（1）<div>老师能否讲解一下ctags的-D和-I参数阿?
另外Cscope好像也能支持c++的是吗?</div>2020-11-01</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/37/d2/945fa276.jpg" width="30px"><span>AirY</span> 👍（0） 💬（3）<div>感觉对rust需要不友好，没有提示，python的话也得.出来而且还有很小的延迟才出来，</div>2020-08-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/20/5b/1f/2f4b7cca.jpg" width="30px"><span>Albert</span> 👍（0） 💬（1）<div>老师，您好。想买一本关于vim的书。看了一下有精通vim、vim8文本处理实战、vim实用技巧 2版。能推荐一下选哪本吗？或者有其他推荐吗？</div>2020-08-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/19/70/67/0c1359c2.jpg" width="30px"><span>qinsi</span> 👍（0） 💬（1）<div>查了下Vim8的话应该可以通过LSP实现跳转自动完成和格式化等功能 https:&#47;&#47;microsoft.github.io&#47;language-server-protocol&#47;implementors&#47;tools&#47;</div>2020-08-24</li><br/>
</ul>