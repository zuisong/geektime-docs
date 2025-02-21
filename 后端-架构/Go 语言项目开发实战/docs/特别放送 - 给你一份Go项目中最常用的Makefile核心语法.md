你好，我是孔令飞。今天，我们更新一期特别放送作为“加餐”，希望日常催更的朋友们食用愉快。

在第 [**14讲**](https://time.geekbang.org/column/article/388920) 里**，**我强调了熟练掌握Makefile语法的重要性，还推荐你去学习陈皓老师编写的[《跟我一起写 Makefile》 (PDF 重制版)](https://github.com/seisman/how-to-write-makefile)。也许你已经点开了链接，看到那么多Makefile语法，是不是有点被“劝退”的感觉？

其实在我看来，虽然Makefile有很多语法，但不是所有的语法都需要你熟练掌握，有些语法在Go项目中是很少用到的。要编写一个高质量的Makefile，首先应该掌握一些核心的、最常用的语法知识。这一讲我就来具体介绍下Go项目中常用的Makefile语法和规则，帮助你快速打好最重要的基础。

Makefile文件由三个部分组成，分别是Makefile规则、Makefile语法和Makefile命令（这些命令可以是Linux命令，也可以是可执行的脚本文件）。在这一讲里，我会介绍下Makefile规则和Makefile语法里的一些核心语法知识。在介绍这些语法知识之前，我们先来看下如何使用Makefile脚本。

## Makefile的使用方法

在实际使用过程中，我们一般是先编写一个Makefile文件，指定整个项目的编译规则，然后通过Linux make命令来解析该Makefile文件，实现项目编译、管理的自动化。
<div><strong>精选留言（10）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/10/dd/09/feca820a.jpg" width="30px"><span>helloworld</span> 👍（17） 💬（2）<div>我觉得变量用${}, 函数用$(),这样能很好区分，对熟悉shell的人也更友好</div>2021-06-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/52/40/e57a736e.jpg" width="30px"><span>pedro</span> 👍（7） 💬（1）<div>周一就更新，值😂</div>2021-06-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/6b/90/ca3bf377.jpg" width="30px"><span>haha</span> 👍（2） 💬（1）<div>有学员群吗？可以加入下吗？方便交流和提升，谢谢。</div>2021-07-16</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/01/8c/41adb537.jpg" width="30px"><span>Tiandh</span> 👍（2） 💬（4）<div>老师，这两句话不理解
因为伪目标不是文件，make 无法生成它的依赖关系，也无法决定是否要执行它。
因为伪目标总是会被执行，所以其依赖总是会被决议。</div>2021-06-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/9d/a4/e481ae48.jpg" width="30px"><span>lesserror</span> 👍（1） 💬（1）<div>大家有什么不懂的，可以结合：陈皓老师编写的《跟我一起写 Makefile》 (PDF 重制版) 来看，本文受限于篇幅，有些概念可能不能花很大的篇幅去讲解。</div>2021-09-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/04/60/64d166b6.jpg" width="30px"><span>Fan</span> 👍（1） 💬（3）<div>多行变量 的例子没明白


define USAGE_OPTIONS

Options:
  DEBUG        Whether to generate debug symbols. Default is 0.
  BINS         The binaries to build. Default is all of cmd.
  ...
  V            Set to 1 enable verbose build. Default is 0.
endef</div>2021-08-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/7b/c5/35f92dad.jpg" width="30px"><span>Jone_乔泓恺</span> 👍（0） 💬（1）<div>老师，有问格式问题想问下：ifeq 语句中的内容建议要用 tab，还是顶格呢？</div>2022-07-01</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/7b/c5/35f92dad.jpg" width="30px"><span>Jone_乔泓恺</span> 👍（0） 💬（1）<div>ifeq ($(origin ROOT_DIR),undefined)
ROOT_DIR := $(abspath $(shell cd $(COMMON_SELF_DIR)&#47;..&#47;.. &amp;&amp; pwd -P))
endif
和 
ROOT_DIR ?= $(abspath $(shell cd $(COMMON_SELF_DIR)&#47;..&#47;.. &amp;&amp; pwd -P))

请问：这两种方式的效果是否相同？
</div>2022-06-30</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/6b/90/ca3bf377.jpg" width="30px"><span>haha</span> 👍（0） 💬（2）<div>由于缺少云上开发资源，本地虚拟机的环境配置能否给些建议，可以创建一个群方便交流吗？</div>2021-07-16</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/7f/d3/b5896293.jpg" width="30px"><span>Realm</span> 👍（0） 💬（3）<div>老师，函数dir ，nodir注释好像有笔误.</div>2021-07-10</li><br/>
</ul>