你好，我是尹会生。

咱们这个课程是用Python解决办公低效问题，但是**即使你从来没有用过Python，甚至没有任何的编程语言基础，也完全可以学会这门课**。

为了解决你的语言问题，我特意准备了这节课。我会给你讲解 Python的五个最基础的语法知识，包括运行环境配置、变量、数据类型、控制语句和使用函数库的方法。

这节课的内容也不需要你马上掌握，其中提到的一些关键知识，我会在后面的课程中详细讲解，包括它们的使用场景和具体用处。**学完这节课，你只要能对Python有一个初步的了解，可以看懂基本的Python代码就行了**。

当然，如果你有一定的Python语言基础，那么这节课就相当于给你巩固复习了，帮你查漏补缺。

## 运行环境配置

我们先从Python的运行环境配置开始说起。初学者面对的最大难题，就是如何让自己的Python程序运行起来。

一般情况下，运行的Python代码会被保存到一个以.py作为扩展名的文件中，也就是Python脚本文件。要想让Python程序运行，我们需要打开终端应用程序（在Windows中开始-运行-cmd.exe）：

```
python3 /py文件所在的路径/xxx.py
或
cd /py文件所在的路径
python3 xxx.py
```

这段代码中，xxx.py就是我们编写好的Python脚本文件，Python3 是Python脚本文件的解释器，它会把我们编写好的代码翻译给计算机，让计算机去执行。
<div><strong>精选留言（30）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/21/69/79/b4132042.jpg" width="30px"><span>🐑</span> 👍（0） 💬（0）<div>编辑小提示：专栏的完整代码位置是https:&#47;&#47;github.com&#47;wilsonyin123&#47;python_productivity，可点击链接下载查看。

或者通过网盘链接提取后下载，链接是: https:&#47;&#47;pan.baidu.com&#47;s&#47;1UvEKDCGnU6yb0a7gHLSE4Q?pwd=5wf1，提取码: 5wf1。</div>2022-03-30</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/04/60/64d166b6.jpg" width="30px"><span>Fan</span> 👍（29） 💬（2）<div>重要的事情说三遍，多看官方文档，多看官方文档，多看官方文档。会让你少走很多弯路。</div>2021-02-03</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/b8/24/039f84a2.jpg" width="30px"><span>咱是吓大的</span> 👍（12） 💬（1）<div>个人经验，技能类的学习应该先模仿后理解再创新</div>2021-02-25</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/78/a9/d0209735.jpg" width="30px"><span>海的对岸</span> 👍（7） 💬（1）<div>边看便敲，碰到问题，排查问题，上网查
编程的学习过程，在我看来，就是一条缓慢的学习曲线，很长一段时间，成效看起来比较低，但是你学着学着，之前学的，慢慢就都理解了，然后就会了</div>2021-02-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/18/a0/8c/801048d1.jpg" width="30px"><span>王波</span> 👍（4） 💬（1）<div>这节课相当于整个课程的基石，需要反复琢磨、反复学习。</div>2021-03-16</li><br/><li><img src="" width="30px"><span>建明</span> 👍（4） 💬（1）<div>分支结构代码的最后一句，print(&quot;程序执行结束&quot;)，总是出错，我试了好多遍，最后发现可能是最后这段代码前面那个符号的问题，怎么把‘...’换成‘&gt;&gt;&gt;’呢？</div>2021-02-20</li><br/><li><img src="" width="30px"><span>建明</span> 👍（3） 💬（1）<div>x = 20if x &gt; 10: # 注意结尾的冒号: print(&quot;if的判断结果为True&quot;) print(&quot;x的值大于10&quot;)else: print(&quot;if的判断结果为False&quot;) print(&quot;x的值小于10&quot;)print(&quot;程序执行结束&quot;)
以上这段代码在pycharm中运行可得到正确的结果，但是在Python中运行就会出错，如下：
&gt;&gt;&gt; x = 20
&gt;&gt;&gt; if x &gt; 10:  # 注意结尾的冒号:
...     print(&quot;if的判断结果为True&quot;)
...     print(&quot;x的值大于10&quot;)
... else:
...     print(&quot;if的判断结果为False&quot;)
...     print(&quot;x的值小于10&quot;)
... print(&quot;程序执行结束&quot;)
  File &quot;&lt;stdin&gt;&quot;, line 7
    print(&quot;程序执行结束&quot;)
    ^
SyntaxError: invalid syntax
</div>2021-03-11</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/l4QiaERRErVOK3pAp783YvQwHfKTNTibXicWOicOO4LnlPibkEX8uYW99BRvIdVkH3kUQa8aMNfGapsSFuTR6UgkkXA/132" width="30px"><span>Geek_bc5d2d</span> 👍（3） 💬（3）<div>pip3 install python-docx
提示SyntaxError: invalid syntax
这个是扩展库没有下载成功吗</div>2021-02-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/a8/df/a206a1a2.jpg" width="30px"><span>小伟</span> 👍（3） 💬（1）<div>基础入门，我喜欢搜索&quot;xxx the right way&quot;的入门指南文档，跟着入门指南熟悉基础知识和进阶路径，后面实战敲代码做demo，遇到问题查阅官方文档，当然还有stackoverflow</div>2021-02-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/25/68/bd/00ffcb80.jpg" width="30px"><span>炫丽生活</span> 👍（2） 💬（2）<div>cmd怎么运行pycharm文件</div>2021-02-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/77/b3/991f3f9b.jpg" width="30px"><span>公号-技术夜未眠</span> 👍（2） 💬（1）<div>一门新语言的快速入门指北:
鸟瞰全貌
对比之前已经掌握过语言间的差异
写一个简单的demo，先运行，后一步步调试
写一个小的项目，比如爬虫程序
多看官方文档，多看优秀的开源项目</div>2021-02-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/81/df/066ffab3.jpg" width="30px"><span>落曦</span> 👍（2） 💬（1）<div>基础入门，这一篇就够了，开心，复习了！
学编程 知行合一 多写代码就可以啦</div>2021-02-07</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1b/83/fb/621adceb.jpg" width="30px"><span>linker</span> 👍（2） 💬（2）<div>学c语言，先照着书上敲代码。</div>2021-02-04</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/92/5d/1bb9ca4b.jpg" width="30px"><span>👊</span> 👍（2） 💬（1）<div>刚好学到了老师零基础入门python课程的while 和 for循环语句，看这一节就比较容易理解。
两门课可以同时进行。</div>2021-02-04</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1f/84/82/c8d70c75.jpg" width="30px"><span>sunlight_r</span> 👍（1） 💬（2）<div>老师，这句没能理解为啥是1-10
list(range(1,11)) # 定义一个1-10 的列表</div>2023-01-04</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/21/87/cc/8380ee81.jpg" width="30px"><span>老吴</span> 👍（1） 💬（1）<div>python3 -V，python3 &#47;py文件所在的路径&#47;xxx.py，这里为什么python后要带3？</div>2021-12-14</li><br/><li><img src="" width="30px"><span>Chq</span> 👍（1） 💬（1）<div>学习，主要靠练习和实践。</div>2021-10-15</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/22/95/fa/bc723edd.jpg" width="30px"><span>阳光小孩</span> 👍（1） 💬（1）<div>学习python一段时间，在面向对象模块遇到瓶颈，原因自然就是思维方式还没有完全转变为程序思维，虽然Python语言简洁易懂但极为灵活，我希望自己能独立做出一些简单的Python项目包括GUI，数据处理，办公自动化，之前一直在学基础，今天开始跟着老师的脚步，希望自己得到蜕变！</div>2021-05-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/25/3a/03/459a8b55.jpg" width="30px"><span>嘉</span> 👍（1） 💬（1）<div>学过r语言，不知道有python和r语句的对照材料吗？</div>2021-03-03</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/25/45/29/53719533.jpg" width="30px"><span>Cherilyn</span> 👍（1） 💬（1）<div>请问有视频和课件吗？谢谢</div>2021-02-15</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1f/17/01/1c5309a3.jpg" width="30px"><span>McKee Chen</span> 👍（1） 💬（1）<div>一开始我是看书学习最基础的python语法，等基础语法掌握了，再跟着课程进行深入学习和实战，学习新知识的同时也能复习以往学过的知识。
最大的感悟还是多上手，多思考，多交流，把自己学到的跟朋友或一起学习的人进行交流与探讨，不仅加深自己的印象与理解，还能提高编程熟练度。
相信跟着尹老师学习会有很大的进步，给自己加油，也给同时在学习本课程的同学加油~</div>2021-02-07</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/1d/44/debb5ca0.jpg" width="30px"><span>燚，咁啱嘅😉</span> 👍（0） 💬（1）<div>请问怎么加学习群</div>2024-02-04</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/ac/28/50474240.jpg" width="30px"><span>黑猫警长</span> 👍（0） 💬（1）<div>windows 输入 python3 -V我没输出呀，输入py -v却可以</div>2022-01-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/2b/7c/01/f1b8ba78.jpg" width="30px"><span>巩会杰</span> 👍（0） 💬（2）<div>pip3 install python-docx 报错了需要更新？更新命令是啥？

WARNING: You are using pip version 21.2.3; however, version 21.3.1 is available.
You should consider upgrading via the &#39;D:\Program Files\Python310\python.exe -m pip install --upgrade pip&#39; command.


</div>2021-11-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/2a/08/5e/191013be.jpg" width="30px"><span>吴杨</span> 👍（0） 💬（1）<div>python基础很重要，需要做笔记扎实掌握。同时可以介绍一下办公自动化主要会用到哪些拓展库，比如python-docx、xlwings等，数据分析又会用到哪些拓展库，可以让学员提前了解和下载。</div>2021-09-02</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/85/49/585c69c4.jpg" width="30px"><span>皮特尔</span> 👍（0） 💬（1）<div>macOS自带的有python2 的解释器吧？</div>2021-07-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/3f/39/a4c2154b.jpg" width="30px"><span>小昭</span> 👍（0） 💬（1）<div>打卡~~~
评论区刷完，也学到很多~~</div>2021-04-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/27/5e/31/a6c2515c.jpg" width="30px"><span>        </span> 👍（0） 💬（1）<div>虽然现在可以中文当变量名了，不过貌似没啥人用，哈哈</div>2021-04-21</li><br/><li><img src="" width="30px"><span>Geek_a73070</span> 👍（0） 💬（2）<div>老师，有学习群吗？</div>2021-04-15</li><br/><li><img src="" width="30px"><span>一朵蔷薇花</span> 👍（0） 💬（1）<div>为什么我把代码复制到notepad++上面，运行的时候什么都没有？</div>2021-03-29</li><br/>
</ul>