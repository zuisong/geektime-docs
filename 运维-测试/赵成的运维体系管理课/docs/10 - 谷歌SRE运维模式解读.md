前面我和你分享了一些关于运维组织架构和协作模式转型的内容，为了便于我们更加全面地了解先进的运维模式，今天我们再来谈一下谷歌的SRE（Site Reliability Engineer）。同时，也期望你能在我们介绍的这些运维模式中找到一些共通点，只有找到这些共通点，才能更深刻地理解，并借鉴到真正对我们有用的东西。

专栏的第一篇文章我们介绍了Netflix的NoOps模式。这个模式并不意味着不存在任何运维工作，只是Netflix将这些事情更紧密地融入到了日常的开发工作中，又做得非常极致，所以并没有很明显地体现出来。

但是，谷歌的SRE却是一个真实具体的岗位，也有明晰的岗位职责。从借鉴意义上来讲，SRE可以给我们提供更好的学习思路和样板。

SRE这个概念，我应该是2014年下半年的时候听到的。当时可接触的资料和信息有限，只知道是谷歌对运维岗位的定义，负责稳定性保障，就没有更多其他的认识了。

后来，有越来越多在谷歌工作或接触过这个岗位的专家开始在公开演讲中分享这个概念。同时，《SRE：Google 运维解密》，这本由多名谷歌SRE亲笔撰写的图书也开始在国内广泛流传，让我们对很多细节有了更加细致的了解。

## SRE岗位的定位

首先，SRE关注的目标不是Operation（运维），而是Engineering（工程），是一个“**通过软件工程的方式开发自动化系统来替代重复和手工操作**”的岗位。我们从SRE这本书的前面几个章节，可以看到谷歌不断强调SRE的工程能力。我简要摘取几段：

> Common to all SREs is the belief in and aptitude for developing  
> software systems to solve complex problems.  
> 所有的SRE团队成员都必须非常愿意，也非常相信用软件工程方法可以解决复杂的运维问题。
> 
> By design, it is crucial that SRE teams are focused on engineering.  
> SRE模型成功的关键在于对工程的关注。
> 
> SRE is what happens when you ask a software engineer to design an  
> operations team.  
> SRE就是让软件工程师来设计一个新型运维团队的结果。

与之相对应的，还有一个很有意思的地方，整本书中提到Operation的地方并不多，而且大多以这样的词汇出现：Operation load，Operation overload，Traditional/Manual/Toil/Repetitive Operation Works。你可以仔细体会一下，这些大多就是传统的纯人工操作模式下的一些典型词汇。

我们可以看到，从一开始，谷歌就没把SRE定义为纯操作类运维的岗位，也正是**谷歌换了一个思路，从另外一个维度来解决运维问题，才把运维做到了另一个境界**。

## SRE岗位的职责

书中对SRE的职责定义比较明确，**负责可用性、时延、性能、效率、变更管理、监控、应急响应和容量管理等相关的工作**。如果站在价值呈现的角度，我觉得可以用两个词来总结，就是“**效率**”和“**稳定**”。

接下来，详细说下我的理解和分析。
<div><strong>精选留言（11）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/0f/81/4b/32d4e113.jpg" width="30px"><span>luoweiro</span> 👍（20） 💬（1）<div>
赞博主精辟剖析！谈谈个人思考：

巨大流量对稳定性指标的冲击其实是量变引发了质变。不管是软件工程还是线上运维其实自然是一体，谷歌SRE其实更是无边界支撑线上业务的模式的实践。
另外，这和谷歌技术文化底蕴也有很大的关系，毕竟谷歌的工程师都是万里挑一的优秀人才，追求极致甚至是从他们进入公司都会耳濡目染，举个例子一个borg系统都做了十几年，不断优化完善。
而近几年一直火热的DevOps理念侧重点是为了提高研发应该具备的综合能力，在不依赖与运维的基础上，能在软件设计上多考虑可运维性，所以由此来看这也应运而生产生更多辅助产品来保障核心业务，而随着辅助产品逐渐逐渐完善也就逐渐催生业界更多优秀的解决方案。
稳定性很多时候是“望天收”的情况，也许幸苦一年建设的稳定性基础设施还不如蓝翔一铲子厉害。所以，建设过程中会逐渐考虑软件层面的高可用，这也是软件定义运维的意义。</div>2018-01-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/cd/e0/c85bb948.jpg" width="30px"><span>朱雯</span> 👍（5） 💬（1）<div>在一家创业公司做运维，现在做的事情是维护公司网络和报警。在您的专栏中提到的这些东西感觉和我差距太远了，是否因为道行太浅的缘故?</div>2018-01-14</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/AkO5s3tJhibth9nelCNdU5qD4J3aEn8OpBhOHluicWgEj1SbcGC6e9rccK8DrfJtRibJT5g6iamfIibt5xX7ketDF6w/132" width="30px"><span>Penn</span> 👍（2） 💬（1）<div>理念是道，实践是术，能落地的方案最有力，期待实践部分的讲解。</div>2018-01-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/a8/4b/702d497f.jpg" width="30px"><span>小朱不是猪</span> 👍（1） 💬（1）<div>看过sre后，对自己的定位更多的是一个计算机行业的从业者，而不仅仅是开发或者运维</div>2020-09-03</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/bf/03/9e5c2259.jpg" width="30px"><span>宵伯特</span> 👍（2） 💬（0）<div>国内的情况大概是因为大多数的公司组织对于运维的职能概念停留在软件后期维护的层面，对于敏捷开发和devops也是一知半解，认知层次和视角都需要进一步的提升。好在如今的技术交流和组织沟通都是自由的，即便是随着技术的发展和产品规模的扩大，也会有越来越多的组织团队意识到该职位的重要性。</div>2018-01-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/6d/ef/08132ab2.jpg" width="30px"><span>万里</span> 👍（1） 💬（0）<div>收获好大，重新定义了我对运维的理解，谢谢老师！</div>2019-03-31</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/ea/7a/f24c11a9.jpg" width="30px"><span>三宝</span> 👍（1） 💬（0）<div>Site Reliability Engineering</div>2018-02-07</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/52/a7/76c10ff6.jpg" width="30px"><span>永涛</span> 👍（0） 💬（1）<div>组织协作模式转型时，如何更好的借助供应商的力量？供应商如何更好的配合与支持来达成组织转型的目的。</div>2022-01-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/75/9b/611e74ab.jpg" width="30px"><span>技术修行者</span> 👍（0） 💬（0）<div>DevOps打破了Dev和Ops的界限，让整个应用从需求提出到上线运维形成了闭环。我理解SRE是DevOps的更进一步发展，通过技术和工程化的手段，提升Ops的效率和稳定。
SRE对人的技术要求更加全面，这对我们来说，是一个很好的机会，可以按照SRE的要求，对自己的技能进行查漏补缺，逐步建立线上产品运维的思维和方法论。</div>2020-05-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/bb/7d/c7f6b46e.jpg" width="30px"><span>魏红生</span> 👍（0） 💬（0）<div>要想做好运维，就得跳出运维的局限，要站在全局的角度，站在价值呈现的角度，站在如何能够发挥出整体技术架构运维能力的角度，来重新理解和定义运维才可以。</div>2019-11-15</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/74/ea/10661bdc.jpg" width="30px"><span>kevinsu</span> 👍（0） 💬（0）<div>运维需要不断挑战自己，不给自己设限制</div>2019-05-16</li><br/>
</ul>