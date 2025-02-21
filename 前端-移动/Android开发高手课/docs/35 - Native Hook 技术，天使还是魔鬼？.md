相信一直坚持学习专栏的同学对Hook一定不会陌生，在前面很多期里我无数次提到Hook。可能有不少同学对于Hook还是“懵懵懂懂”，那今天我们从来头了解一下什么是Hook。

Hook直译过来就是“钩子”的意思，是指截获进程对某个API函数的调用，使得API的执行流程转向我们实现的代码片段，从而实现我们所需要得功能，这里的功能可以是监控、修复系统漏洞，也可以是劫持或者其他恶意行为。

相信许多新手第一次接触Hook时会觉得这项技术十分神秘，只能被少数高手、黑客所掌握，那Hook是不是真的难以掌握？希望今天的文章可以打消你的顾虑。

## Native Hook的不同流派

对于Native Hook技术，我们比较熟悉的有GOT/PLT Hook、Trap Hook以及Inline Hook，下面我来逐个讲解这些Hook技术的实现原理和优劣比较。

**1. GOT/PLT Hook**

在[Chapter06-plus](https://github.com/AndroidAdvanceWithGeektime/Chapter06-plus)中，我们使用了PLT Hook技术来获取线程创建的堆栈。先来回顾一下它的整个流程，我们将libart.so中的外部函数pthread\_create替换成自己的方法pthread\_create\_hook。

![](https://static001.geekbang.org/resource/image/71/f5/715e03d40d7c5f185959e284c23e9df5.png?wh=1772%2A1042)

你可以发现，GOT/PLT Hook主要是用于替换某个SO的外部调用，通过将外部函数调用跳转成我们的目标函数。GOT/PLT Hook可以说是一个非常经典的Hook方法，它非常稳定，可以达到部署到生产环境的标准。
<div><strong>精选留言（14）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/14/17/b7/b229a627.jpg" width="30px"><span>LEi</span> 👍（2） 💬（1）<div>大佬请教下，就是插件化和热修复不会冲突吗，都在hook，一直很疑问，大家都在争夺下层的控制权，微信这种级别的应用是否两个都在用，谢谢</div>2019-10-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/6e/fe/79955244.jpg" width="30px"><span>公众号：程序员大兵</span> 👍（0） 💬（1）<div>请问老师有没有什么技术把安卓应用跑在Linux服务器端？</div>2019-07-10</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTJqMIsh1qiau2v08V2oSEYGic8KAQjfZSlR1syuXhUt6UwriaDGMetkBbrYF4HYw2o3OZIoMFoSF69vQ/132" width="30px"><span>bluevalley</span> 👍（0） 💬（1）<div>请教一下老师，我们现在想做本地io hook加解密，io-canary能覆盖所有的io读写场景么？  另Java层有没有办法做类似hook</div>2019-03-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/0b/73/4f1c9676.jpg" width="30px"><span>舒大飞</span> 👍（0） 💬（1）<div>绍文老师，问一下前面的asm插桩的Demo里为什么使用反射注入自定义的transform，而不是利用register注册transform的方式，有什么讲究吗?</div>2019-03-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/53/a0/8c26f345.jpg" width="30px"><span>红色物质长方体固体转移</span> 👍（1） 💬（0）<div>我没想到 我25年 又回过头来学习这个课程 </div>2025-01-25</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/N0NACGUr8dNAbN6BdiagPHBaB0EnyDsI9zWpwJteqTY38apOEnTOA7JkBAQnzYKJBgxu3Q8YMUILwLAB6camn4w/132" width="30px"><span>Swing</span> 👍（1） 💬（1）<div>看完一脸懵。。。没有搞过c&#47;c++的估计都是这样的看法。。
cpu指令这种名词，看的太猛了。
plt hook还能稍微理解，trap hook 是什么鬼，不适用ptrace，只使用了 signal句柄处理机制？
那怎么 定位和修改指令。。
还有下面的 inline hook。。。

还有就是 “但是需要注意，无论是哪一种 Hook 都只能 Hook 到应用自身的进程，我们无法替换系统或其他应用进程的函数执行”

ptrace 可以实现修改 其他进程？但是 由于trap hook 舍弃了 ptrace ，所以 不行？</div>2020-04-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/5e/96/a03175bc.jpg" width="30px"><span>莫名</span> 👍（1） 💬（0）<div>👍</div>2019-12-25</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/54/c1/1d852e91.jpg" width="30px"><span>hs</span> 👍（0） 💬（1）<div>老师，您好，想问一下动态链接中的，虚拟地址、绝对地址、实际地址的关系是什么？</div>2020-11-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/e7/c0/71f69d77.jpg" width="30px"><span>aspiration🍭</span> 👍（0） 💬（0）<div>邵老师，想请教下，这个hook，可以用来hook，so中的非对外调用方法吗？因为想要用来测试so的逻辑。</div>2020-11-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/20/fc/ac/d236de41.jpg" width="30px"><span>null</span> 👍（0） 💬（0）<div>大佬，关于Art Hook，我不太了解arm64下 x0-x30 ART是怎么调用的。能推荐几个博客文档吗。</div>2020-09-28</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/MzQVZhFALRPibYvtKgUpp0vpMaxKibKwDibdo4fTJpdr2E5nx12Bq7hbRAdf8UTyHj07t7vAcXVnuXfBh5E6hZh5A/132" width="30px"><span>Geek_cccb56</span> 👍（0） 💬（0）<div>绍文老师，我运行了Trap hook的demo，我看里面只能做方法替换，没有inline hook那种origin_method的指针可以回去执行原来的方法，比如我只想hook后打印下参数，还想执行原来的方法，这种trap hook怎么实现</div>2020-05-05</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/N0NACGUr8dNAbN6BdiagPHBaB0EnyDsI9zWpwJteqTY38apOEnTOA7JkBAQnzYKJBgxu3Q8YMUILwLAB6camn4w/132" width="30px"><span>Swing</span> 👍（0） 💬（1）<div>这些都是 编译期 修改的，还是 运行时修改的？</div>2020-04-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/80/2b/ef1581b5.jpg" width="30px"><span>米兰的小铁匠</span> 👍（0） 💬（0）<div>看了java和native两篇hook了，可以讲下xposed的吗？逆向现在也挺热门的</div>2020-04-02</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/7e/bb/947c329a.jpg" width="30px"><span>程序员小跃</span> 👍（0） 💬（0）<div>想当初，项目组因为libhwui.so崩溃，想了很多办法，因为没有了解过Hook，始终在其他方向努力。当时的深度和广度还远远不够，感谢老师的课程，让我对当初的经历有了一个新的看法。</div>2019-07-24</li><br/>
</ul>