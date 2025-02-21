你好，我是于航。

在 [23 讲](https://time.geekbang.org/column/article/486342) 中，我对本次实战项目将要构建的程序 FibServ 的功能做了基本介绍，并从理论的角度，带你对它的基本实现方案有了一个初步认识。而这一讲，我们将通过实际编码，来应用这些理论知识。

为了便于你理解这一讲的内容，我已经将本项目的完整代码实现放到了 GitHub 上，你可以点击[这个链接](https://github.com/Becavalier/tiny-http-echo-server/tree/geektime)，先大致浏览一下每个源文件的内容。而在后续讲解到相关代码时，我也会在整段代码的第一行，通过注释的方式将这些代码的所在源文件标注出来。比如注释 “libs/structs.h#L9-L11”，便表示当前所示的代码段对应于项目 libs 目录下，structs.h 文件内的第 9 到 11 行。其他注释的含义你可以此类推。

接下来，我会带你从基本的项目目录创建，到模块功能编写，再到代码编译和程序运行，一步步地完成整个项目的开发过程。

## 项目基本结构

首先，我们来看应该如何组织整个项目的目录结构。根据预估的项目体量，我使用了如下图所示的目录结构：

![图片](https://static001.geekbang.org/resource/image/f9/8c/f9fcf00722c6b785052f1yyd8d27aa8c.png?wh=760x616)

这里，整个项目包含有三个目录：build、libs 以及 src。其中，build 目录用于存放程序在 CMake 下的临时编译结果。如果你对这个目录还不太熟悉，可以参考我在 [22 讲](https://time.geekbang.org/column/article/485191) 中为你介绍的例子。libs 目录中主要存放可以模块化的独立功能实现，这些功能会以头文件的形式来提供外部可用接口，以供不同的应用程序使用。而最后的 src 目录则存放有与应用程序 FibServ 实现相关的源代码。
<div><strong>精选留言（5）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/11/2f/5c/e6e27476.jpg" width="30px"><span>fee1in</span> 👍（3） 💬（1）<div>花了两个小时 终于将示例跑通 后面的同学doxygen问题 可以参考老师在uriparser的issue https:&#47;&#47;github.com&#47;uriparser&#47;uriparser&#47;issues&#47;137</div>2022-02-16</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/18/fa/46/ef3b85a6.jpg" width="30px"><span>叶兰</span> 👍（2） 💬（1）<div>于老师讲的太好了，受益匪浅</div>2022-02-16</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1f/59/d3/696b1702.jpg" width="30px"><span>校歌</span> 👍（0） 💬（1）<div>老师你好，我没写过C项目，包管理感觉还是go的项目爽😁；运行报错如下
# cmake ..  
...
Could not find a package configuration file provided by &quot;uriparser&quot;
... 

为了跑老师的项目，本地安装了libgtest-dev和源码编译安装 uriparser，项目才跑起来。不知有没有简单的办法，类似go mod tidy 或者go get xxx 获取go项目的依赖呢？</div>2022-06-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/0b/6f/68cd0614.jpg" width="30px"><span>brian</span> 👍（0） 💬（0）<div>老师啊，epoll和异步io都没有用上，不能算高性能吧</div>2023-04-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/43/cf/118c4ef5.jpg" width="30px"><span>lunar</span> 👍（0） 💬（0）<div>第一次跑C项目 还要自己装一下第三方库,学习的路上又踏出了一步 -DURIPARSER_BUILD_DOCS=OFF</div>2022-03-20</li><br/>
</ul>