你好，我是葛俊。今天，我来跟你聊一聊DevOps和SRE。

DevOps和SRE，尤其是DevOps，是最近几年软件研发方法的重要趋势。因为它们都跟打通开发和运维流程相关，所以常常被混淆。比如，SRE等同于Google的DevOps、SRE是升级版的DevOps，就是两个常见的误区。

事实上，DevOps和SRE虽然关系紧密，但差别还是蛮大的。所以今天，我首先会通过DevOps和SRE的对比，引出它们背后的Why、How和What（也就是它们的目标、原则和具体实践）。然后，我会结合自己在一个创业公司的经验，向你推荐如何在团队落地DevOps。

## DevOps和SRE的定义和异同

因为DevOps和SRE都是比较新的概念，而且在不断地发展变化，所以学术界和工业界对它们的定义并未达成一致。

接下来，我参考已有定义，并加入自己的理解，对DevOps和SRE的大致定义如下：

**DevOps**，Development和Operations的组合词，是一种重视“软件开发人员（Dev）”和“IT运维技术人员（Ops）”之间沟通合作的文化、活动或惯例。 通过自动化“软件交付”和“架构变更”的流程，使得软件的构建、测试、发布更加快捷、频繁和可靠。
<div><strong>精选留言（15）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/10/82/42/8b04d489.jpg" width="30px"><span>刘丹</span> 👍（15） 💬（1）<div>全栈工程师不一定全领域，准确的说法应该是多领域，掌握大部分领域，精通少数领域。</div>2019-09-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/6e/8d/e07c8b7c.jpg" width="30px"><span>刘晓光</span> 👍（11） 💬（1）<div>全栈!=全干 
全栈的支撑基础是服务化和技术封装。其实还是底层支撑越来越牛逼了。如果一个组织没有很好的底层技术支撑，</div>2019-09-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/da/24/afa9214a.jpg" width="30px"><span>兴国</span> 👍（6） 💬（1）<div>成为全栈工程师也是分阶段，分领域的。比如平常主要做java的开发人员，基于工作需要，也需要写前端，会golang&#47;php等语言；也需要对运维服务器进行部署&#47;使用，使用运维工具进行发布等。刚开始可能对前端等只是会写，并不能搭建框架，不了解其原理；对服务器部署原理，网络搭建原理也不了解。但是能够满足日常的开发，运维需要。随着时间的推移，业务的发展以及问题的不断出现和解决。慢慢的能够更深入了解除java开发之外的东西，慢慢加强巩固自己的技术栈。当然也不是说什么都要会，更多的还是工作中，业务中用到的，主要还是要服务于业务发展。所以是分时间段，分领域的。</div>2019-09-09</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTJOBwR7MCVqwZbPA5RQ2mjUjd571jUXUcBCE7lY5vSMibWn8D5S4PzDZMaAhRPdnRBqYbVOBTJibhJg/132" width="30px"><span>ヾ(◍°∇°◍)ﾉﾞ</span> 👍（4） 💬（1）<div>其实早起在土鳖公司都是全栈的，全栈的好处很明显减少扯皮，对功能聚焦。刚开始可能觉得有难度，其实刚开始比如可以有一个资深的前端搭建框架，后面更改和填充功能就容易多了</div>2019-09-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/c3/ab/c2ca35e6.jpg" width="30px"><span>名贤集</span> 👍（3） 💬（3）<div>这位大佬，你也没说使用devops遇到什么问题，如何解决的。
devops跟9999没有直接关系，用devops不一定能达到9999，不用也不一定达不到。
全栈开发跟devops有关系吗？前端和后端都是写代码-单元测试-签入-集成测试，所用的devops也是一样的。怎么感觉你的文章都飘在天上呢？</div>2019-09-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/fe/85/9ab352a7.jpg" width="30px"><span>iMARS</span> 👍（2） 💬（1）<div>全栈=全开发流程和生命周期</div>2020-10-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1f/50/dc/e8270e4f.jpg" width="30px"><span>xiaozhi239</span> 👍（2） 💬（1）<div>Team Topologies这本书里介绍里四种开发团队类型，其中最多的一种叫Stream-Aligned teams，负责业务的输出，在我的理解里就是一种DevOps的团队。其它团队类型就是用来服务Stream-Aligned团队的，比如封装复杂的系统调用、提供工具、提供技术支持等。我觉得大中台、小前台也是一个类似的理念。通过对全栈的支持，减少全栈团队所需要掌握的知识，让他们可以更专注focus在业务迭代上。

关于Team Topologies我也写了两篇文章介绍：
https:&#47;&#47;blog.csdn.net&#47;xiaozhi239&#47;article&#47;details&#47;108163138
https:&#47;&#47;blog.csdn.net&#47;xiaozhi239&#47;article&#47;details&#47;108326635</div>2020-09-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/0a/c8/dae4a360.jpg" width="30px"><span>Do</span> 👍（2） 💬（1）<div>Facebook是没有测试团队的吗？所有功能都是对应的开发自测？</div>2019-10-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/dd/30/9d36ccaf.jpg" width="30px"><span>桃源小盼</span> 👍（2） 💬（1）<div>全栈工程师，在面对一些非常见问题时，会更快的定位问题，而不是以前那样，大家都觉得跟自己没关系，就等着别人去解决。</div>2019-09-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/19/35/be8372be.jpg" width="30px"><span>quietwater</span> 👍（1） 💬（1）<div>全栈是趋势，意味着独立地交付客户价值，所以通过平台和各种工具的支撑，可以直接承接客户的需求是更高的全栈。最后甚至可能包括市场洞察等更多的东西。</div>2020-01-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/18/af/30/80210f08.jpg" width="30px"><span>MiffyLiye</span> 👍（1） 💬（1）<div>现有的工具越来越成熟，个人&#47;小团队能掌控的复杂度越来越高。
同时社会发展变快，提高研发效率，对市场需求快速反应越来越重要。
这些因素就让成为全栈工程师的投入产出比越来越高，变成了非常值得去发展的方向。</div>2019-09-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1c/f9/36/f44b633e.jpg" width="30px"><span>bidinggong</span> 👍（0） 💬（1）<div>DevOps 是打通开发和运维的文化和惯例，而 SRE 是 DevOps 的具体实践之一。说到相同点，它们都是为了打通 Dev 和 Ops，提高研发效能；说到区别，DevOps 是文化，而 SRE 是职位。如果要类比的话，DevOps 与 SRE 的关系，就像敏捷跟 Scrum 的关系。</div>2020-10-21</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/ajNVdqHZLLCkkXTINhMFfyQadnr8WdZ2hTW3ne86TE8cHayicqFsYtNPNBvnZdlAB0rSDPvic9jSOdCfPuuDY0GA/132" width="30px"><span>Geek_55b198</span> 👍（0） 💬（1）<div>开发和运维目标不一致，最近感触良多。
1.全栈开发，新型运维角色--类SRE，优化流程，提供工具，PE和SRE,50%为开发工作，工具和自动化开发
2.开发人员稳定的产品，承担一部分SRE工作。对一组代码负责，包括依赖的代码；让开发人员oncall

第1点实践上是否需要考虑统一的工具平台，小工具如何管理
第2点我们已经参考葛老师的建议，卷入了开发人员，24小时oncall
</div>2020-03-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/18/22/97/7a1c4031.jpg" width="30px"><span>Raymond吕</span> 👍（0） 💬（1）<div>想问下老师，DevOps适合什么规模的团队使用，有没有可参考的标准，比如10人以上？另外，老师也说了DevOps是方法论，需要从文化上切入，想问如果导入的效果不好，该怎么办？放弃还是继续试点推动。</div>2020-02-13</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTIPV2S8CfAd8P0OibnP8I0qWwvjKX7uiaibficPD2BDVNK6CCe09EFDuM9udVx1gVzcTK66VapQ9TMDuQ/132" width="30px"><span>Geek_d5da21</span> 👍（0） 💬（0）<div>我们的工程师不会去学习新技术，会java就不去学Android，更不用说全栈了。</div>2023-01-02</li><br/>
</ul>