你好，我是戴铭。

在专栏的第2篇文章[《App 启动速度怎么做优化与监控？》](https://time.geekbang.org/column/article/85331)更新完之后，我看到很多同学对启动加载 App 的底层原理表示出了浓厚兴趣。所谓工欲善其事，必先利其器，相信有着好奇心的你，一定也会对支撑着 App 运行的操作系统有着各种各样的疑问。

我曾在专栏的第5篇文章[《链接器：符号是怎么绑定到地址上的？》](https://time.geekbang.org/column/article/86840)中，和你分享了链接器在编译时和程序启动时会做的事情。而今天这篇文章，我会重点与你说说加载动态链接器之前，系统是怎么加载 App 的。

所以，今天我会先跟你说说iOS系统的架构是怎样的，各部分的作用是什么，帮助你理解iOS系统的原理，进而更全面地理解它在 App 加载时做了哪些事情？

接下来，我就先跟你聊聊 iOS 的系统架构是怎样的。在理解iOS系统架构之前，你最好掌握一些操作系统原理的基础知识。

## iOS 系统架构

iOS 系统是基于 ARM 架构的，大致可以分为四层：

- 最上层是用户体验层，主要是提供用户界面。这一层包含了 SpringBoard、Spotlight、Accessibility。
- 第二层是应用框架层，是开发者会用到的。这一层包含了开发框架 Cocoa Touch。
- 第三层是核心框架层，是系统核心功能的框架层。这一层包含了各种图形和媒体核心框架、Metal 等。
- 第四层是 Darwin层，是操作系统的核心，属于操作系统的内核态。这一层包含了系统内核 XNU、驱动等。
<div><strong>精选留言（14）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/11/cb/c8/ff9f3ffb.jpg" width="30px"><span>赵国辉</span> 👍（4） 💬（1）<div>老师，有没有计划讲解一下dyld的工作过程和原理，非常想学习一下</div>2019-05-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/6c/cb/8a41f8ce.jpg" width="30px"><span>Bill</span> 👍（1） 💬（1）<div>多从提到了BSD BSD全称到底是啥</div>2019-10-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/7a/7c/7bde009a.jpg" width="30px"><span>烩面</span> 👍（1） 💬（1）<div>老师，是先 fork 出新进程，还是先分配内存呢？ 小结和上面对 __mac_execve 函数的分析上好像有点出入 。。。</div>2019-05-26</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/DYAIOgq83eoGRhUIWgJcgLOkpH6p4EfxVGvF0daA9r91CoEcJ0lRIAiad8FJFzf4WVHgJRh0OdicX5PZ2MpWCV0Q/132" width="30px"><span>bart</span> 👍（29） 💬（0）<div>推荐大家回顾一下大学的《操作系统》，然后看一下《 深入解析Mac OSX &amp; IOS 操作系统》，这样听起来会畅快很多。</div>2019-05-30</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/44/59/b607b8c0.jpg" width="30px"><span>毛成方</span> 👍（9） 💬（0）<div>Mike Ash文章最后总结说道大部分工程师不会去在意这些细节 但是当你在遇到动态链接等报错的时候 你讲更好去分析和解决它们。换句话说 我们要走出自己的舒适区 去研究新的技术 碰壁 总结 才能有更好的成长 去挑战更大的平台。</div>2019-06-03</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/3b/05/b2776d73.jpg" width="30px"><span>Geek</span> 👍（2） 💬（4）<div>读后感: 真的看不懂，iOS开发需要这么深入吗？</div>2019-05-30</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTJVegfjqa0gM4hcRrBhZkIf7Uc5oeTMYsg6o5pd76IQlUoIIh2ic6P22xVEFtRnAzjyLtiaPVstkKug/132" width="30px"><span>xilie</span> 👍（1） 💬（1）<div>读后感: 真的看不懂，iOS开发需要这么深入吗？</div>2019-05-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/28/ea/36/7d088c63.jpg" width="30px"><span>D</span> 👍（0） 💬（1）<div>所以App的Mach-O 文件到底是由XNU加载到内存的还是由dyld加载到内存的？以前一直认为是dyld 加载App的Mac-o 并解析加载load commands。现在越来越看不懂了...</div>2021-08-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/21/63/a6/5b5879e7.jpg" width="30px"><span>Wim</span> 👍（0） 💬（0）<div>大神能讲一下“点击appIcon到app启动”或者“被别的应用拉起的启动”具体的底层过程吗？</div>2020-12-08</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/rWMGIQG1z13nekorr9I4PY1w7rlskssf949IQ24SvIewpM7mmZoH2QEZ2aKHu5tkmicGQ7KTGrN9vFYhrDsdp9w/132" width="30px"><span>Geek_9dbcb4</span> 👍（0） 💬（0）<div>文中“加载 Mach-O 文件，内核会 fork 进程，并对进程进行一些基本设置，比如为进程分配虚拟内存、为进程创建主线程、代码签名等”。
问题，这个地方的代码签名，不同于我们证书的私钥对APP的签名吧？也不同于苹果的私钥对APP的再次签名吧？</div>2020-04-18</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/rWMGIQG1z13nekorr9I4PY1w7rlskssf949IQ24SvIewpM7mmZoH2QEZ2aKHu5tkmicGQ7KTGrN9vFYhrDsdp9w/132" width="30px"><span>Geek_9dbcb4</span> 👍（0） 💬（0）<div>文中“XNU 加载就是为 Mach-O 创建一个新进程，建立虚拟内存空间，解析 Mach-O 文件，最后映射到内存空间。”，最后这个虚拟内存空间就没有了吧？例如进程内所有的地址访问，都是真实内存地址了，是吧</div>2020-04-18</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/DYAIOgq83eryWeGhypWhPlxbnPgx5o7iadtgBU9YkNFJfJfBu5dvosdTns8JELibOciaZx89MajzCRLOrrqwqgcPw/132" width="30px"><span>yujian</span> 👍（0） 💬（1）<div>请问：app被拒后，申诉仅解释一下，但是代码不动还用原来的ipa，想问是否还需要重新提交审核么</div>2019-05-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/73/b9/c4b5b7c6.jpg" width="30px"><span>凛冬一壶酒</span> 👍（0） 💬（0）<div>这个可以有 哈哈哈</div>2019-05-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/35/19/4f9dc4b5.jpg" width="30px"><span>帅气潇洒的豆子</span> 👍（0） 💬（0）<div>帅！看来得多听几遍了</div>2019-05-25</li><br/>
</ul>