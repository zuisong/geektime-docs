你好，我是葛俊。今天，我来跟你聊聊研发过程中的Git代码分支管理和发布策略。

在前面两篇文章中，我们讨论了持续开发、持续集成和持续部署的整个上线流程。这条流水线针对的是分支，因此代码的分支管理便是基础。能否找到适合自己团队的分支管理策略，就是决定代码质量，以及发布顺畅的一个重要因素。

Facebook有几千名开发人员同时工作在一个大代码仓，每天会有一两千个代码提交入仓 ，但仍能顺利地进行开发，并发布高质量的产品。平心而论，Facebook的工程水平的确很高，与他们的分支管理息息相关。

所以在今天这篇文章中，我会先与你详细介绍Facebook的分支管理策略，以及背后的原因；然后，与你介绍其他的常见分支管理策略；最后，向你推荐如何选择适合自己的分支策略。

## Facebook的分支管理和发布策略

Facebook的分支管理策略，是一种基于主干的开发方式，也叫作Trunk-based。在这种方式中，用于开发的长期分支只有一个，而用于发布的分支可以有多个。

首先，我们先看看这个长期存在的开发分支。

### 开发分支

这个长期存在的开发分支，一般被叫作trunk或者master。为方便讨论，我们统一称它为master。也就是说，所有的开发人员基于master分支进行开发，提交也直接push到这个分支上。
<div><strong>精选留言（24）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/0f/75/9b/611e74ab.jpg" width="30px"><span>技术修行者</span> 👍（15） 💬（2）<div>看完这篇后，最大的感受就是Git是个宝库，之前对它的使用还停留在表面，我要去找本书系统学习一下。</div>2019-09-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/a1/e6/50da1b2d.jpg" width="30px"><span>旭东(Frank)</span> 👍（11） 💬（3）<div>想问一下老师，Facebook的开关是配置系统统一管理的吧？那么多功能分支，都靠开关管理，如何做好多个配置开关有效快速管理？</div>2019-09-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/5f/ad/9c310977.jpg" width="30px"><span>phobal</span> 👍（6） 💬（1）<div>像 Facebook 这种主干（master）开发模式，每个人的代码每天都会合入到 master，实际中经常会有这样的情况：A、B 两个 feature 同时在进行，但上线时间不同，A 先上，那基于这种模式，A 上的话就会带入 B 的代码，难道 A 上的时候再基于上一个稳定版本 tag 再 cheery-pick A 的所有功能代码到测试分支？</div>2019-09-07</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/b1/4d/10c75b34.jpg" width="30px"><span>Johnson</span> 👍（5） 💬（4）<div>听起来trunk-base这种方式基本和集中式的svn和perforce是一个思路，那疑问就是为啥不直接用perforce,收费？学习成本？需要额外的运维投入？
trunk-base针对pull request的方式还有一个疑问，怎么做pre checkin的code review来控制入库代码的质量？
我能想到的好像还是集中式的那种checkin必须使用固定的工具，这个工具会去自动获取这个提交的code review，如果没有就不允许checkin.</div>2019-09-06</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/17/e9/a8/8fc92fcc.jpg" width="30px"><span>菜头</span> 👍（3） 💬（1）<div>facebook 的原子化提交这块，开发是以什么标准拆分，确保原子性的。老师能否帮忙介绍下。谢谢</div>2019-12-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/75/9b/611e74ab.jpg" width="30px"><span>技术修行者</span> 👍（3） 💬（1）<div>全栈是趋势，这是不可避免的。
全栈不意味着所有事情都亲力亲为，从个人发展的角度来说，肯定还是需要先在某个方向上做专做精，然后对项目涉及的其他方面由浅入深的逐渐熟悉。在读圣贤书的同时，也要知窗外事。</div>2019-09-13</li><br/><li><img src="" width="30px"><span>GeekJ</span> 👍（2） 💬（2）<div>从上面文章中获取，您的cherry-pick 策略都是在master上进行修复，然后cherry-pick 至周部署分支或热修复分支。
针对这个场景，我有以下几个问题
1. master分支每天有很多提交，其分支代码与周部署分支&amp;热修复分支很大可能已经不一致了，如何保证cherry-pick质量？为什么不是从待发布分支 cherry-pick 至 master 分支呢？
2. cherry-pick 操作是自动化，还是手动的？</div>2020-02-02</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/38/cf/f2c7d021.jpg" width="30px"><span>李双</span> 👍（2） 💬（1）<div>各种分支管理策略，学习！问下，基于base开发的这种方式，是不是根据时间线，截止某一时间点（或者某个版本号之前的），代码验证过了，就可以上线了，而不是根据业务功能的先后紧急！</div>2019-09-06</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/f9/86/272fc86f.jpg" width="30px"><span>小齐</span> 👍（1） 💬（1）<div>rebase 的时候冲突为啥是 git add &amp; git commit 而不是 git add &amp; git rebase --continue</div>2020-09-15</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/64/05/6989dce6.jpg" width="30px"><span>我来也</span> 👍（1） 💬（1）<div>学习了。

以前就我一个人用git时，只能在官网（https:&#47;&#47;git-scm.com&#47;book&#47;zh&#47;v2）看看文档。
很多命令都不知道在什么场景下使用。
之前看耗子书关于分支管理的文章，也是云里雾里，很多命令不知道为什么那么用。

现在新工作环境中，由于需要跟别人协作，用的git命令也是越来越多了。
现在再来看老师的这篇文章，就不再吃力了。

我现在很喜欢git rebase 和 git cherry-pick。
我也很努力的保持分支线性，看上去好看。😄
之前很小的提交都是用git merge -no-ff来合并的。

总之，这个东西是熟来生巧。</div>2019-11-01</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1c/f9/36/f44b633e.jpg" width="30px"><span>bidinggong</span> 👍（0） 💬（1）<div>Facebook一直使用这种主干分支开发方式。它强迫我们把代码进行原子化，尽量确保每一个提交都尽快合入 master，并保证代码质量。实际应用后才会发现它的确很棒。</div>2020-10-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/92/8a/e86a8db7.jpg" width="30px"><span>文中</span> 👍（0） 💬（1）<div>文中提到的 FB 的实践，对提交的新代码质量、新代码的测试覆盖、已有的测试覆盖率的要求都很高。对于大型的项目，还需要上下游统一写集成测试用例才能完成。怎么能保证不同业务系统的业务代码和测试代码能同时或在很短的间隔内都完成提交呢？</div>2020-04-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/8a/62/1ce50dc3.jpg" width="30px"><span>Ian</span> 👍（0） 💬（1）<div>老师你好，请问一下Git-flow工作流，你提到不方便持续集成，这个点能展开说明一下吗？不太明白为什么不方便持续集成呢？谢谢。</div>2020-03-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/82/a4/a92c6eca.jpg" width="30px"><span>墨灵</span> 👍（0） 💬（1）<div>看了大厂的最佳实践，不得不感叹我司的产品管理这块的确是做得太粗糙了，可以完善的点还有很多，自己以前对git的了解也不够深入。</div>2020-03-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/e0/37/a78abe7e.jpg" width="30px"><span>Hacken</span> 👍（0） 💬（1）<div>有没有toB的分支模型建议，多客户，核心功能相同，但是多个客户可能有不同的功能集合或者定制</div>2019-11-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/c9/db/b7b3acf3.jpg" width="30px"><span>Robin</span> 👍（0） 💬（1）<div>facebook 的 Trunk-based 模式感觉没有 code review 流程介入呀，开发者直接push到master就测试上线了吗？</div>2019-11-15</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/13/68/859713ae.jpg" width="30px"><span>无名路人</span> 👍（0） 💬（1）<div>老师，为什么用的是rebase而不是merge</div>2019-09-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/ca/8d/4ebf66a6.jpg" width="30px"><span>高倩</span> 👍（0） 💬（1）<div>主干开发模式，对于开发的拆分能力要求很高，同时从测试的角度，又怎么确保整个项目和产品功能的完整性呢？</div>2019-09-16</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/ae/a7/6d3a5d44.jpg" width="30px"><span>Dump</span> 👍（0） 💬（2）<div>老师能不能讲讲移动端的开发管理，看了几篇都是后端的集成和发布流程</div>2019-09-07</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/89/dc/3c4bc06b.jpg" width="30px"><span>囧囧冰淇淋</span> 👍（0） 💬（1）<div>看到今天，感觉研发和代码越来越有趣了XD</div>2019-09-07</li><br/><li><img src="" width="30px"><span>果粒橙</span> 👍（1） 💬（0）<div>Git-flow 工作流，功能或者修复合并时，容易出现忘记合并到某个分支的情况。不过可以使用脚本自动化来解决。请教一下怎么自动化解决？有具体方法么？</div>2022-05-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/2c/fe/86/61bc225d.jpg" width="30px"><span>K先生</span> 👍（1） 💬（0）<div>请教老师，模式一：主干分支，无功能分支，几千人的开发团队，如何做好，万一有人一提交，功能就不可用的问题，是在提交的时候就做质量门禁么？感觉此方法对人的要求非常高</div>2022-03-20</li><br/><li><img src="https://wx.qlogo.cn/mmopen/vi_32/ibXbRJ3yOT48IHc6mayIRxibutDz2bWHxBdicNoeJBG9EG6AXpuRMhtBRmjpFvmGPBIAYNrnq6nP9okwk5oU36GSA/132" width="30px"><span>静水潜流，润物无声</span> 👍（0） 💬（0）<div>请教老师两个问题：
1、feature 分支与本地分支是只是叫法上的区别吗？实际在git里面是指一个意思？

2、分支让实际上就是为了方便分布全球不同local的team渐进式集成不同功能到同一代码文件，不知道这种理解是否正确。</div>2021-12-07</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1a/3b/d0/a6da72a7.jpg" width="30px"><span>小慧</span> 👍（0） 💬（0）<div>主仓库以master为主，建立功能分支。功能分支开发完成合并到测试分支，比如sit  uat  ，有bug直接在功能分支修改，再合并到测试分支验证。测试通过把功能分支合并到master分支，进行生产发布。这是哪个模式呢？</div>2021-04-14</li><br/>
</ul>