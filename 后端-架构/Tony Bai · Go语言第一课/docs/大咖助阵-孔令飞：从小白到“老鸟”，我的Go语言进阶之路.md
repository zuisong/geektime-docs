你好，我是孔令飞，是极客时间 [《Go 语言项目开发实战》](https://time.geekbang.org/column/intro/100079601) 专栏和《从零构建企业级Go项目》图书的作者，目前在腾讯云从事分布式云方向的研发工作。

很高兴，也很感谢能够借助Tony Bai老师的专栏《**Tony Bai ·Go 语言第一课** 》给你分享我的Go语言进阶之路。今天这一讲没有Go语法知识的学习，没有高大上的理论，更多的是我个人在Go语言进阶过程中的一些经验、心得的分享。希望通过这些分享，能帮助到渴望在Go研发之路上走的更远的你。

为了方便说明如何提升Go研发能力，我需要先给你介绍下我认为的Go语言能力级别的划分依据。

## Go语言能力级别划分

下面这些能力级别是根据我自己的理解划分的。这些Go语言能力级别没有标准的定义，各级别之间也没有明确的界限，级别之间也可能有重叠的部分。但这不妨碍我们参考这些级别大概判断自己当前所处的阶段，思考如何提升自己的Go研发能力。

我将Go语言能力由低到高划分为以下5个级别。

- **初级**：已经学习完Go基础语法课程，能够编写一些简单Go代码段，或者借助于Google/Baidu能够编写相对复杂的Go代码段；这个阶段的你基本具备阅读Go项目代码的能力；
- **中级**：能够独立编写完整的Go程序，例如功能简单的Go工具等等，或者借助于Google/Baidu能够开发一个完整、简单的Go项目。此外，对于项目中涉及到的其他组件，我们也要知道怎么使用Go语言进行交互。在这个阶段，开发者也能够二次开发一个相对复杂的Go项目；
- **高级**：不仅能够熟练掌握Go基础语法，还能使用Go语言高级特性，例如channel、interface、并发编程等，也能使用面向对象的编程思想去开发一个相对复杂的Go项目；
- **资深**：熟练掌握Go语言编程技能与编程哲学，能够独立编写符合Go编程哲学的复杂项目。同时，你需要对Go语言生态也有比较好的掌握，具备较好的软件架构能力；
- **专家**：精通Go语言及其生态，能够独立开发大型、高质量的Go项目，编程过程中较少依赖Google/百度等搜索工具，且对Go语言编程有自己的理解和方法论。除此之外，还要具有优秀的软件架构能力，能够设计、并部署一套高可用、可伸缩的Go应用。这个级别的开发者应该是团队的技术领军人物，能够把控技术方向、攻克技术难点，解决各种疑难杂症。
<div><strong>精选留言（10）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/13/7b/bd/ccb37425.jpg" width="30px"><span>进化菌</span> 👍（3） 💬（2）<div>输出倒逼输入，还是得多练习，才能不断进阶golang</div>2021-12-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/17/85/92/9f7c43ef.jpg" width="30px"><span>乌云下的风</span> 👍（0） 💬（1）<div>22年的专栏24年才看到，加油吧 祝自己早日 go中级巅峰</div>2024-02-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/92/4f/ff04156a.jpg" width="30px"><span>天天向上</span> 👍（0） 💬（1）<div>以教促学！学习路线分享太实用了，等我1年之后再回复！</div>2022-08-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/9d/a4/e481ae48.jpg" width="30px"><span>lesserror</span> 👍（8） 💬（0）<div>学吧，太深了......</div>2021-12-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/cb/38/4c9cfdf4.jpg" width="30px"><span>谢小路</span> 👍（4） 💬（3）<div>大厂还是锻炼人的。6 年就专家了。学这个专栏的同学们六年时间，绝大多数达不到这高度。将将够混口饭吃，包括写留言的我。</div>2022-04-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/19/2e/ca/469f7266.jpg" width="30px"><span>菠萝吹雪—Code</span> 👍（2） 💬（0）<div>老师分享的太棒了，一年之后来报告学习效果</div>2022-09-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/1d/de/62bfa83f.jpg" width="30px"><span>aoe</span> 👍（1） 💬（0）<div>感谢大咖分享，待我初级毕业就学习《Go 语言项目开发实战》
看到文中的各种学习资源很激动，大部分都可以用来实战，提升工作效率</div>2022-01-01</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/3c/81/5b/fe82b3c2.jpg" width="30px"><span>Superdandan</span> 👍（0） 💬（0）<div>感谢老师分享，阅读iam专栏很有启发</div>2024-11-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/1d/3a/cdf9c55f.jpg" width="30px"><span>未来已来</span> 👍（0） 💬（0）<div>个人理解：自己动手整个 k8s 集群，非常非常非常重要</div>2022-12-02</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/27/ff/e4/927547a9.jpg" width="30px"><span>无名无姓</span> 👍（0） 💬（0）<div>老师讲的真好</div>2021-12-21</li><br/>
</ul>