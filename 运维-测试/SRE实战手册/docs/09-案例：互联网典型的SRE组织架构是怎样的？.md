你好，我是赵成，欢迎回来。

前面三讲，我们从故障这个关键事件入手，讲解了“优先恢复业务是最高优先级”这个原则，基于这个原则，在故障发生后，我们要做好快速响应和应急，并从故障中学习和改进。在这个学习过程中，你应该也能体会到，高效的故障应对和管理工作，其实是需要整个技术团队共同参与和投入的。这就引出了大家落地SRE都会遇到的一个难点：组织架构调整。

那落地SRE必须调整组织架构吗？典型的SRE组织架构是怎样的？接下来，我会用两讲内容和你探讨这些问题，分享我在蘑菇街实践的一些经验。

## 落地SRE必须调整组织架构吗？

好，那我们就开始吧，先给你看一张技术架构图。  
![](https://static001.geekbang.org/resource/image/69/ac/69a12388ac0795a84bcdc8489bb196ac.jpg?wh=3107%2A1874)  
这是蘑菇街基于微服务和分布式技术的High-Level的架构图，也是非常典型的互联网技术架构图，自下而上共四层，分别是基础设施层、业务&amp;技术中台层、业务前台层以及接入层，在右侧还有一个技术保障体系。如果你平时经常看一些架构方面的图书和文章，或者听过一些技术大会演讲的话，对这样的图应该不陌生。

你也许会问，咦，我们不是讲组织架构吗？咋一上来就说到技术架构上了？别急，我这么讲是有原因的，在讲SRE的组织架构之前，我们需要先明确两点内容。

**第一，组织架构要与技术架构相匹配**。
<div><strong>精选留言（15）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/0f/c3/d1/bdf895bf.jpg" width="30px"><span>penng</span> 👍（7） 💬（2）<div>我觉得PE这个角色很重要，需要整理业务需求和反馈，沉淀到平台工具开发团队和稳定性开发团队。又需要和业务团队沟通交流，来适配技术中台。虽然他不是一手需求设计者，也不是具体技术中台功能开发者。但是确是关键的核心枢纽。</div>2020-04-07</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/0c/30/d4737cd5.jpg" width="30px"><span>lyonger</span> 👍（6） 💬（1）<div>从一个公司的组织架构，往往能看出公司的技术架构。另外很期待老师分享一些云原生领域在SRE下的实践。😄</div>2020-04-07</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/17/27/ec30d30a.jpg" width="30px"><span>Jxin</span> 👍（6） 💬（1）<div>1.我认为是效能和稳定性工具平台的开发。
2.在所有角色中没有重要的轻重，因为我们要的是保证系统稳定运行这一最终目标，所以，哪怕是一根稻草的重量，那也是同等的重要.
3.但是，搭建整套完善的sre是一个长期的工程，安排好优先级可以让团队和公司在在搭建的过程中获得更高的效益，毕竟效益这个东西不是快照，而是一个时间上的积累。
4.所以，我认为优先做效能和稳定性平台的开发会比较好，因为他能比较快的拿出东西，也没有那么多因地制宜的限制，在sre推进的前期，既可以降低公司的顾虑，也可以提高团队的士气。是个开刀的好口子。至于iaas和paas这两块，能用云先用云。而业务这块，这是一件任重道远的事，不适合做先头。</div>2020-04-07</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/9e/d3/abb7bfe3.jpg" width="30px"><span>wholly</span> 👍（4） 💬（1）<div>SRE角色不仅仅是定位某个问题，还应该具备更全的技术栈及系统思维，当业务发展到一定规模的时候，我觉得这个角色还是很有必要的。</div>2020-04-07</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/7a/e1/326f83b9.jpg" width="30px"><span>石头</span> 👍（3） 💬（2）<div>国内传统行业的sre组织架构是什么样了的，有必要设置sre岗位吗？
</div>2020-04-06</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/bf/aa/32a6449c.jpg" width="30px"><span>蒋悦</span> 👍（1） 💬（2）<div>请问，什么规模的公司可以选择上云，什么规模的公司可以考虑自建云呢？
我们现在的公司其实规模不小，是自建的云，是否有可能上云呢？是否有可能分批上云呢？比如先让前台上云，成功了，在把中台上云？</div>2020-04-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1b/a2/4f/0d983a3e.jpg" width="30px"><span>Quinn</span> 👍（0） 💬（1）<div>云原生架构的图中，从左到右是什么轴？为什么敏捷要和虚拟机一起？我的理解是敏捷和devops是相辅相成。devops只是在工具上支持敏捷而已。希望细致讲解一下这张图的用意。</div>2020-05-05</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/DYAIOgq83epy83Wich4cvDO6dvYbC9DVONqluiaTKn5ATuTmY3HQuXWlAcx2k52FE8TUcjq7Q08f6NwYwdlNnj0A/132" width="30px"><span>Geek_80674c</span> 👍（0） 💬（3）<div>老师你好，
请问对于在大厂私有云里做基础架构层的运维，也就是你文中指的传统运维，有什么职业发展的建议吗？文中对这个职位介绍比较少，大厂里基础架构部人数也不小，所以希望可以指导职业发展。
是向PE转型比较好？
</div>2020-04-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/bf/aa/32a6449c.jpg" width="30px"><span>蒋悦</span> 👍（0） 💬（1）<div>看了这个组织架构，我都不好意思说我是哪家公司的，传统行业，差距太大</div>2020-04-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/34/df/64e3d533.jpg" width="30px"><span>leslie</span> 👍（4） 💬（0）<div>个人觉得技术运营或者说去年GOPS大会提及的运维运营：这个其实是个中间层，熟悉产品、懂得且能处理技术相关的问题、能针对现状提出问题；个人可能对此还有更深层次的整体设计的事情。
站在中间且能看到两头大致梳理好两头其实这是任何事情发展到中期必然要面对的问题：中台的概念个人觉得其实同样基于此。就像我们说起系统运维，这个其实同样有两头硬件设备和网络，系统只是中间而已，如果硬件方面和网络方面没有处理好系统、、、
谢谢老师的分享尤其是云原生架构图引发的反思，期待后续的课程。</div>2020-04-06</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/1c/a5/21303c71.jpg" width="30px"><span>Reggie</span> 👍（0） 💬（0）<div>SRE = PE + 工具平台开发 + 稳定性平台开发，这个结构应该算是SRE本土化了，按照google的SRE定义，上面的三个角色应该是同一波人轮流不同的角色。按照google的SRE标准应该很难凑出一支队伍，运维能力和工程能力都在线的人才在国内还是太少了。</div>2023-07-05</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1b/7b/2b/97e4d599.jpg" width="30px"><span>Podman</span> 👍（0） 💬（0）<div>“运维能力一定是整个技术架构能力的体现，而不是单纯的运维的运维能力体现。微服务和分布式架构下的运维能力，一定是跟整个架构体系不分家的。”
也是运维崛起的契机
</div>2022-04-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/3d/f5/5c7d550f.jpg" width="30px"><span>小蓝罐</span> 👍（0） 💬（0）<div>老师，反之我更多的认为SRE其实合适任何大小项目架构的。只要你需要可靠性这样的高要求那就能行。大的架构有大的做法，小的也同理。SRE一样适配</div>2022-03-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/0f/d5/73ebd489.jpg" width="30px"><span>于加硕</span> 👍（0） 💬（0）<div>工具平台团队，可以理解成DevOps吗？或部分能力</div>2020-10-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/0f/d5/73ebd489.jpg" width="30px"><span>于加硕</span> 👍（0） 💬（0）<div>个人认为业务运维较重要吧，在我们的环境中，业务运维承载了业务方需求，与应用的维护，运维产品的推广，这种持续性的工作是可以为SRE产出MVP提供输入的。</div>2020-04-21</li><br/>
</ul>