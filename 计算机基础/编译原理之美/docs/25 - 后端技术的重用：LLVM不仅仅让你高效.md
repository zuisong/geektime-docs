在编译器后端，做代码优化和为每个目标平台生成汇编代码，工作量是很大的。那么，有什么办法能降低这方面的工作量，提高我们的工作效率呢？**答案就是利用现成的工具。**

在前端部分，我就带你使用Antlr生成了词法分析器和语法分析器。那么在后端部分，我们也可以获得类似的帮助，比如利用LLVM和GCC这两个后端框架。

相比前端的编译器工具，如Lex（Flex）、Yacc（Bison）和Antlr等，对于后端工具，了解的人比较少，资料也更稀缺，如果你是初学者，那么上手的确有一些难度。不过我们已经用20～24讲，铺垫了必要的基础知识，也尝试了手写汇编代码，这些知识足够你学习和掌握后端工具了。

本节课，我想先让你了解一些背景信息，所以会先概要地介绍一下LLVM和GCC这两个有代表性的框架的情况，这样，当我再更加详细地讲解LLVM，带你实际使用一下它的时候，你接受起来就会更加容易了。

## 两个编译器后端框架：LLVM和GCC

LLVM是一个开源的编译器基础设施项目，主要聚焦于编译器的后端功能（代码生成、代码优化、JIT……）。它最早是美国伊利诺伊大学的一个研究性项目，核心主持人员是Chris Lattner（克里斯·拉特纳）。
<div><strong>精选留言（14）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/0f/87/8a/3631f06f.jpg" width="30px"><span>无嗔</span> 👍（18） 💬（0）<div>Mozilla 还真的是一家非营利性的科技公司</div>2019-12-02</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/e8/ca/2a7cc193.jpg" width="30px"><span>阿鼎</span> 👍（10） 💬（1）<div>老师未提到visual studio的后端，请老师也介绍一下？</div>2019-10-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/69/4d/81c44f45.jpg" width="30px"><span>拉欧</span> 👍（8） 💬（1）<div>老师的技术深度真心让人敬佩</div>2019-12-05</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/39/fa/a7edbc72.jpg" width="30px"><span>安排</span> 👍（3） 💬（1）<div>老师请问下，LLVM 版本的 C++ 标准类库，这个是什么意思啊？ 是说libc++是用llvm后端编译出来的吗？区别于gun项目的libstdc++吗？
libc++这个c++标准类库是苹果弄出来的吗？</div>2019-10-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/0a/83/f916f903.jpg" width="30px"><span>风</span> 👍（2） 💬（2）<div>在Windows上安装好llvm后，只能用clang命令，llvm-as和llc命令用不了，这是为什么呢?</div>2019-11-05</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/25/f8/4a6062b1.jpg" width="30px"><span>疯二中</span> 👍（0） 💬（1）<div>老师你好，我在window上使用clang，看输出好像是用了visual studio的c++标准库。llvm没有提供window版本的c++标准库吗？</div>2019-11-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/c5/a2/4ece341b.jpg" width="30px"><span>Ivan.Qi</span> 👍（2） 💬（0）<div>增加一些LLVM的中文资料

LLVM后端开发书籍或文章整理
https:&#47;&#47;zhuanlan.zhihu.com&#47;p&#47;645857966

毕昇编译--llvm编译入门
https:&#47;&#47;mp.weixin.qq.com&#47;mp&#47;appmsgalbum?action=getalbum&amp;__biz=MzkyNTMwMjI2Mw==&amp;scene=2&amp;album_id=2974971429714837504&amp;count=3#wechat_redirect
</div>2023-09-02</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/21/16/f7/cce336a2.jpg" width="30px"><span>涛</span> 👍（0） 💬（0）<div>请问示例代码在哪里下载？
</div>2024-02-07</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/17/e0/76/ffaf5f49.jpg" width="30px"><span>allen</span> 👍（0） 💬（0）<div>老师，你提供的示例代码，我在运行的时候，报以下错误，能回答一下吗:
Could not find a package configuration file provided by &quot;LLVM&quot; with any of
  the following names:

    LLVMConfig.cmake
    llvm-config.cmake</div>2023-04-26</li><br/><li><img src="" width="30px"><span>Geek_a0b00e</span> 👍（0） 💬（0）<div>老师，您好，能详细讲讲llvm中的memory SSA吗</div>2022-06-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/04/60/64d166b6.jpg" width="30px"><span>Fan</span> 👍（0） 💬（0）<div>老师，C++的示例程序没有找到的呢？

建立 C++ 开发环境来使用 LLVM
整个开发环境的搭建我在课程里就不多写了，你可以参见示例代码所附带的文档。文档里有比较清晰的说明，可以帮助你把环境搭建起来，并运行示例程序。</div>2021-08-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/9e/50/21e0beca.jpg" width="30px"><span>kylin</span> 👍（0） 💬（0）<div>老师，请问这个项目用C++如何搭建起来呢？没有找到资料呢</div>2021-07-03</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1f/68/12/031a05c3.jpg" width="30px"><span>A免帅叫哥</span> 👍（0） 💬（0）<div>问句课程外的问题，老师的clion是正版购买的吗？
做技术，如果全部使用正版，一年也是一笔不小的开销，老师对于使用正版这个问题，有什么看法吗？</div>2021-06-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/64/99/c22d82a1.jpg" width="30px"><span>陈高健</span> 👍（0） 💬（0）<div>给老师点赞👍</div>2020-03-26</li><br/>
</ul>