你好，我是黄俊彬。上一节我给你介绍了两个遗留系统常用的分析工具：ArchUnit和Dependencies依赖分析工具。

虽然我们了解了它们的基本使用方法，但是实际落地到项目中，我们经常会遇到一些问题，比如：

1.代码散落各处，约束规则不好写？  
2.结合架构设计，怎么来设计约束规则？  
3.约束规则怎么应用到自动化分析工具上？

这节课我们就一起用ArchUnit和Dependencies对Sharing项目进行一次整体分析。

这个分析由五部分组成。

- 第一部分，将代码结构按新的架构设计进行调整。
- 第二部分，根据代码结构以及新架构设计定义出依赖规则。
- 第三部分，将依赖规则转化成Dependencies的Rule规则，然后进行扫描分析。
- 第四部分，将依赖规则转化成ArchUnit的用例，进行扫描分析。
- 最后，总结出从现有的代码结构按未来架构设计需要重构的问题清单，作为下一阶段代码重构的输入。

通过这节课的分析，你可以学会在实际项目中如何结合工具来落地架构分析工作，上面的问题也能得到解答。

## 以新架构设计来组织代码

首先，我们一起回顾一下Sharing项目目前代码的方式。如下图所示，所有的代码是以技术维度来组织。例如把所有页面都放在ui的包下，或者把所有的模型都放在model下。
<div><strong>精选留言（6）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/10/25/87/f3a69d1b.jpg" width="30px"><span>peter</span> 👍（1） 💬（2）<div>请教老师两个问题：
Q1：用Dependencies时怎么增加scope？
我用AS4.1，操作顺序：菜单Analyze  Dependencies。点击后AS开始执行Dependencies扫描，然后出现扫描结果的界面；此界面分为左右两个部分。我在此界面尝试多次，没有找到在哪里可以添加scope。（注：我的界面和文中的界面相同。）

Q2：“热更新”、“热修复”的理解是否对？
A“热更新”：用户安装了版本1，现在出了版本2，用户不需要先卸载版本1然后重新安装版本2，而是在版本1的基础上直接更新为版本2。   B“热修复”：与版本无关，用户安装了某一个版本，该版本有bug，在线直接打补丁来修复。  我的理解对吗？</div>2023-02-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/22/59/97/9b7a412c.jpg" width="30px"><span>Aā 阳～</span> 👍（0） 💬（1）<div>如果模块之间存在页面复用怎么办呢，这种怎么做到不横向依赖？</div>2023-09-05</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/2e/6e/05230eb6.jpg" width="30px"><span>稻草人的忧桑</span> 👍（0） 💬（1）<div>这里按照包结构的写完约束，之后按照组件重构，约束规则是不是还得调整</div>2023-03-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/2e/6e/05230eb6.jpg" width="30px"><span>稻草人的忧桑</span> 👍（0） 💬（1）<div>示例项目的archutil依赖版本，能否做一下更新</div>2023-03-06</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/1d/ae/f78ce0d7.jpg" width="30px"><span>中世纪的knight</span> 👍（0） 💬（1）<div>github 上Sharing项目希望老师可以保留一份重构前分支，每次重构切一次分支。</div>2023-02-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/19/08/f7/2c3238bd.jpg" width="30px"><span>Lihyper</span> 👍（1） 💬（0）<div>模型数据以及消息事件可以详细解说一下吗？</div>2024-11-20</li><br/>
</ul>