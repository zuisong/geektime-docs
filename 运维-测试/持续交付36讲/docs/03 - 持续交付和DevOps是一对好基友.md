现在很多人都在困惑持续交付和DevOps到底是什么关系，有什么区别，或许你也感觉傻傻分不清楚。那么今天，我就来和你聊聊持续交付和DevOps，以及它们到底是什么关系。

## 持续交付是什么？

我在专栏的第一篇文章中，已经跟你很详细地分享了持续交付是什么，为了加深你的印象，并与DevOps形成对比，我在这里再从另外一个角度给你总结一下：

> 持续交付是，提升软件交付速率的一套工程方法和一系列最佳实践的集合。

它的关注点可以概括为：持续集成构建、测试自动化和部署流水线。

那么，DevOps又是什么呢？其实一直以来，学术界、工业界都对DevOps没有明确的定义，所以造成了大家对它的看法也是众说纷纭，也难免片面。

在我给出我个人的认识之前，我先给你讲讲DevOps是怎么被发明的吧。

## DevOps的诞生

DevOps的故事，要从一个叫帕特里克 · 德博伊斯（Patrick Debois）的IT咨询师讲起。2007年，帕特里克参与了一个政府下属部门的大型数据中心迁移的项目。

在这个项目中，帕特里克发现开发团队（Dev）和运维团队（Ops）的工作方式和思维方式有巨大的差异：

- Dev的工作是，为软件增加新功能和修复缺陷，这要通过频繁的变更来达到；
- Ops的工作是，保证系统的高稳定性和高性能，这代表着变更越少越不容易出错。
<div><strong>精选留言（13）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/0f/4d/4d/abb7bfe3.jpg" width="30px"><span>铭熙</span> 👍（23） 💬（1）<div>学习DevOps必读书籍，改变世界的机器，精益思想，目标，凤凰项目，持续交付，DevOps实践指南，DevOps实施手册。</div>2018-07-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/c6/20/124ae6d4.jpg" width="30px"><span>若水清菡</span> 👍（5） 💬（1）<div>我是做运维和SA的，之前对CI&#47;CD不是很了解，看了很多网上的文章和微信技术公众号的文章还是一头雾水，看了作者的文章后有点&quot;恍然大悟&quot;的感觉。最近部门和开发一起在推动CI&#47;CD，文章对我很有用，多谢作者。</div>2018-07-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/54/41/3d352f74.jpg" width="30px"><span>酷飞不会飞</span> 👍（2） 💬（1）<div>首先，敬畏每一种职业。现在DevOps的发展也越来越快，越来越好，个人觉得，DevOps的时代会衍生一个新的职业，而Ops也会被重新定义，或者成为DevOps的一个分支，而DevOps则不仅仅体现在技术层面，流程化，标准化，规范化甚至管理也会逐渐加深，最后可能会发展一个新的学科。而Ops肯定会在其中扮演一个重要的角色，不仅不会被代替，甚至是进入DevOps的一个敲门砖！纯属个人见解。</div>2018-07-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/db/ed/106a8ec9.jpg" width="30px"><span>王浩槟</span> 👍（2） 💬（1）<div>我算是小白了，ops指的是运维吧。可以说ops是专指后台运维吗？</div>2018-07-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/ac/65/dc6261b0.jpg" width="30px"><span>夜幽魂</span> 👍（1） 💬（1）<div>关于学习持续集成，有什么推荐的书籍</div>2018-07-10</li><br/><li><img src="" width="30px"><span>有道测试组</span> 👍（7） 💬（0）<div>ops的岗位肯定是需要的， 但是对这个岗位本身的能力要求也会不断提升。如果devops把平台、工具建设的足够强大，手动ops的需求量应该会减少，ops应该要不断提升自身dev能力，除了把每次遇到的重复问题解决掉， 还应该有思考通用的解决方案，不断提升自身以及团队的工作效率， 目前大公司对ops的要求应该是这样的。</div>2018-12-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/64/9b/d1ab239e.jpg" width="30px"><span>J.Smile</span> 👍（1） 💬（0）<div>总结一下：
①”DevOps 是一种组织架构，将 Dev 和 Ops 置于一个团队内，一同工作，同化目标，以达到 DevOps 文化地彻底贯彻。“
②
* DevOps 的本质其实是一种鼓励协作的研发文化；
* 持续交付与 DevOps 所追求的最终目标是一致的，即快速向用户交付高质量的软件产品；
* DevOps 的概念比持续交付更宽泛，是持续交付的继续延伸；
* 持续交付更专注于技术与实践，是 DevOps 的工具及技术实现。
----------------------------
一句话：Dev 与 Ops 本质上是不同的，一个开发，一个运维。它们目标一致------快速交付，但达成目标的手段不同。</div>2020-08-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/73/08/dd9a4a38.jpg" width="30px"><span>小狼</span> 👍（1） 💬（1）<div>不过现在招聘运维都会写一条熟悉devops</div>2018-08-31</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/14/99/5b1ed92b.jpg" width="30px"><span>戴斌</span> 👍（0） 💬（0）<div>我理解的持续交付是devops的子集</div>2020-03-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1b/ae/e1/04973e79.jpg" width="30px"><span>Vickie-liang</span> 👍（0） 💬（0）<div>我认为不是的</div>2020-01-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/42/f7/06cd1560.jpg" width="30px"><span>X</span> 👍（0） 💬（0）<div>好</div>2019-05-15</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/cf/60/f4e0b87a.jpg" width="30px"><span>蒋大培</span> 👍（0） 💬（1）<div>期待讲讲如何做到代码上线业务不上线😁😁</div>2018-07-16</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/0c/94/56ea80f7.jpg" width="30px"><span>沐风</span> 👍（0） 💬（0）<div>有没有相关书籍推荐</div>2018-07-10</li><br/>
</ul>