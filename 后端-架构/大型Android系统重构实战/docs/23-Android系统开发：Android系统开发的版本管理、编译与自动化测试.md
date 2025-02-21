你好，我是黄俊彬。

这节课起，我们进入到扩展篇的学习。扩展篇我们将从系统角度，学习定制Android系统的一些常见问题和解决思路。一起了解定制Android系统中常见的一些开发方式、架构问题以及解耦思路。

从应用到系统开发，代码量从几十万行增长到几千万行，开发框架以及编译环境等与应用开发也不一样。所以如果要学习Android系统开发，我们需要先了解对应的开发框架及工具链。

今天，我们就来聊聊Android系统开发的版本管理、编译调试以及相关的自动化测试等实践，了解引入这些工具及实践的目的。在实践过程中用好这些工具，会大大提升开发效率。

## Repo &amp; Gerrit 代码管理

我们先来看看代码的管理。由于Android源码的代码量庞大，采用的是多个Git仓库来管理代码。你可以通过 [GoogleSource](https://android.googlesource.com/?format=HTML) 查看对应的仓库，大约有3000个仓库。

那么，假如有一个需求开发涉及到跨多个仓库的修改，我们怎么来维护代码提交以及同步工作呢？

为了解决这个问题，**官方提供了一个多Git仓代码管理的工具——** [Repo](https://gerrit.googlesource.com/git-repo/+/refs/heads/master/README.md)。根据官网的介绍，Repo 不会取代 Git，目的是帮助我们在 Android 环境中更轻松地使用 Git。

Repo 将多个 Git 项目汇总到一个Manifest文件中，使用Repo命令来并发操作多个Git仓库的代码提交与代码同步很方便。我用表格梳理了一些Repo常用的命令，供你参考。
<div><strong>精选留言（1）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/10/25/87/f3a69d1b.jpg" width="30px"><span>peter</span> 👍（0） 💬（1）<div>请教老师几个问题：
Q1：构建系统Bazel怎么体现？是在AS的新版本中吗？或者在AS的老版本中可以设置Bazel?
Q2：从求职的角度，安卓系统开发要重点关注哪些方面？对某一个方面，怎么学习更好？
Q3：安卓APP开发完成后，怎么发布该APP？
--- 在哪些应用市场发布？
--- 可以自己放在一个地方，让用户通过二维码扫码来下载吗？</div>2023-04-03</li><br/>
</ul>