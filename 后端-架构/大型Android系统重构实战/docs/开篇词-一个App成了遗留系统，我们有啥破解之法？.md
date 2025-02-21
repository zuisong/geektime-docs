你好，我是黄俊彬，很高兴在极客时间和你相遇。

作为一个在移动开发领域历练了十年的老兵，我曾参与过多个国内大型手机OS研发团队整机组件化、架构解耦的项目，在移动开发领域的架构设计、自动化测试、性能优化、DevOps等方面有丰富的经验。

近几年，我经历了多个大型Android遗留系统的重构项目，很多系统的代码达到百万行的量级。这个过程里，我收获了很多经验，也希望能够帮助更多朋友，在遗留系统重构方面少走弯路。

## 你的产品是遗留系统吗？

说起遗留系统，我们通常会有后面这几种认识。

- Bug很多的系统就是遗留系统。
- 代码很难维护的就是遗留系统。
- 没有自动化测试的代码就是遗留系统。
- ……

在这些认识里，已经提到了遗留系统的一些症状。其实对于遗留系统，我更认为它是一种“综合症”，指的是技术上已过时，但仍然在企业中使用的计算机系统或应用程序，**有许多负面的症状**。

这么说你可能还是觉得有点抽象，可以对号入座，看看下面这9个问题是否在你的项目中也曾经遇到过。

![](https://static001.geekbang.org/resource/image/3f/cd/3f5bfb00067df2022d06de8ca9d312cd.jpg?wh=3413x2178)

如果你的产品也有类似的一些问题，那么不管你是团队中的任何角色，希望你能引起足够的重视，因为符合的“症状”越多，你的产品就越趋近于一个遗留系统。当遗留系统这个泥球越滚越大时，我们对它投入的改造成本就会越来越高。遗留系统就像一辆老破旧的小汽车，不知道啥时候会出问题，维修成本也越来越高，想快也快不起来。
<div><strong>精选留言（13）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/14/5a/8a/dd06563f.jpg" width="30px"><span>Justin</span> 👍（3） 💬（1）<div>没经历大厂的流程，希望可以学到不一样的东西。</div>2023-02-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/93/ed/9cc44242.jpg" width="30px"><span>JakePrim</span> 👍（2） 💬（1）<div>赞</div>2023-02-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/c0/15/02fe27bf.jpg" width="30px"><span>戴益波</span> 👍（0） 💬（1）<div>怎么界定大型Android系统？
大厂到底是什么大厂？
这么多年的工作经验到底是什么工作经验？

看了下博主的 github 和 简书，基本都是一些简单的Android入门知识？ 标题是不是起的太大了些。

- https:&#47;&#47;github.com&#47;junbin1011&#47;
- https:&#47;&#47;www.jianshu.com&#47;u&#47;466f8b75f81c</div>2023-10-02</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/10/3d/b3991de7.jpg" width="30px"><span>dulp</span> 👍（0） 💬（1）<div>做ios开发刚满三年，希望通过这门课也能够对移动端架构有所收获</div>2023-03-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/57/ce/01df95aa.jpg" width="30px"><span>木头人</span> 👍（0） 💬（1）<div>没经历大厂的流程，希望可以学到不一样的东西。</div>2023-03-01</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1e/67/0d/ffa5cd9b.jpg" width="30px"><span>oldjii</span> 👍（0） 💬（1）<div>目前正着手于一个遗留模块的重构，给我感受最大难度是保证重构后的业务逻辑与线上保持一致，所以很期待自动化分析、自动化重构的内容。</div>2023-02-17</li><br/><li><img src="" width="30px"><span>Geek_90e087</span> 👍（0） 💬（1）<div>打卡开始</div>2023-02-16</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/d6/7d/4b09b0bf.jpg" width="30px"><span>李鑫鑫</span> 👍（0） 💬（1）<div>学习了</div>2023-02-15</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/a3/33/8680446c.jpg" width="30px"><span>拭心</span> 👍（0） 💬（1）<div>课程名称容易让人迷惑，我一开始以为是针对 Android 操作系统的重构，看完发现是「大型 Android 应用的系统重构」。</div>2023-02-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/7e/95/56224a2f.jpg" width="30px"><span>耿森</span> 👍（0） 💬（1）<div>开篇看的很有感觉，希望学有所成。赞一个</div>2023-02-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/ce/6d/530df0dd.jpg" width="30px"><span>徐石头</span> 👍（0） 💬（1）<div>服务端开发人员能从课程学到哪些？</div>2023-02-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/c1/bf/494d0895.jpg" width="30px"><span>、时光偷走当初คิดถึง</span> 👍（0） 💬（1）<div>好久没有看到Android知识了，过来取个经</div>2023-02-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/3b/f8/54/791d0f5e.jpg" width="30px"><span>Geek群接龙</span> 👍（0） 💬（0）<div>老师你好， 我们公司也遇到了历史系统的问题， 公司想邀请老师过来指导， skfier 可以加 v 联系</div>2024-09-26</li><br/>
</ul>