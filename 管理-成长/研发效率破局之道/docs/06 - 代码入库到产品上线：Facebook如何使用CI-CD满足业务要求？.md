你好，我是葛俊。

在上一篇文章中，我和你分享了代码入库前的流程优化，即持续开发。今天，我会继续与你介绍流程优化中，代码入库和入库后的3种持续工程方法，即持续集成（Continuous Integration, CI)、持续交付（Continuous Delivery, CD）和持续部署（Continuous Deployment, CD)。

在接下来的分享中，首先我会与你介绍这3种方法的定义和作用，帮助你深入理解这3个“持续”背后的原理和原则；然后我会以Facebook为参考，给你介绍基于这些原则的具体工程实践。我希望，这些内容能够帮助你用好这三个“持续”方法，提高团队的研发效能。

首先，我先来介绍一下，持续集成、持续交付和持续部署是用来解决什么问题的，也就是它们的定义和作用。

## 3个“持续”的定义和作用

不知道你是否还记得，在开篇词中，我提到过一个低效能的情况，即产品发布上线时出现大量提交、合并，导致最后时刻出现很多问题。这个情况很常见，引起了很多用户的共鸣。产生这个问题最主要原因是，**代码合并太晚**。这里，我再与你详细解释一下原因。

当多个人同时开发一款产品的时候，很可能会出现代码冲突。而解决冲突，需要花费较多的时间；同时很可能出现冲突解决失败，导致产品问题。
<div><strong>精选留言（27）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/11/6e/8d/e07c8b7c.jpg" width="30px"><span>刘晓光</span> 👍（11） 💬（2）<div>最大的困难有三个都在人的工作习惯上：有效且同期建设的单元测试;每天至少一次的push代码；轻量级频繁的code review
</div>2019-09-05</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/75/9b/611e74ab.jpg" width="30px"><span>技术修行者</span> 👍（6） 💬（1）<div>1. 在几千名开发人员共同使用一个大代码仓的工作方式下，做好 CI 有很大的挑战性。你觉得挑战在哪里，容易出现什么样的问题，又应该怎么解决呢？
最大的挑战有两个：1. 代码冲突如何处理。2. 模块之间的依赖如何解决。
对于1，首先是要改善团队文化，鼓励大家频繁提交，而不是只在每天下班前提交一次，其次，出现冲突，需要开发人员自己解决，这部分在做plan，最好能预留一些buffer，不然大家都在赶进度，都不会愿意去做，容易拖到最后，更不容易解决。
对于2，模块之间尽量松耦合，要保证模块之间的接口是稳定的。


2. 今天我提到了持续开发在 CI 中的作用，请你结合上一篇文章，思考一下持续开发和 CI&#47;CD 是怎样互相促进的。
CI&#47;CD的快速反馈，对于持续开发来说，是一个正向激励的作用，让开发人员对于正在开发的功能更有信心。</div>2019-09-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/19/09/f2/6ed195f4.jpg" width="30px"><span>于小咸</span> 👍（6） 💬（3）<div>使用git rebase的话，具体操作流程应该是
add &#47;rm -&gt;commit -&gt;pull -&gt;rebase -&gt;push
这样子对吗</div>2019-09-05</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/19/2c/9c/6c64975a.jpg" width="30px"><span>詩鴻</span> 👍（2） 💬（2）<div>使用大仓和组件化多仓的权衡关键主要是什么呢？</div>2019-09-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/37/3b/495e2ce6.jpg" width="30px"><span>陈斯佳</span> 👍（1） 💬（1）<div>终于搞懂了持续交付和持续部署的区别，主要就是前者仅限于非生产环境，目的是随时随地提供可部署的软件；后者则是直接部署到生产环境中。看老师的观点，也就是提交量很大的情况才会考虑到持续部署。鉴于我们公司的提交量还处于excel checklist的可以摆平的状况，持续部署应该在很长的时间内不需要我去担心了……重点关注持续集成和持续交付上</div>2020-04-07</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/19/02/c5/301c1712.jpg" width="30px"><span>Lu</span> 👍（1） 💬（1）<div>老师您好～ 我所在的组织在尝试CICD流水线从而实现云上部署。CI流水线这一步每次都会有安全漏洞检查，单这个检查本身耗时很久，而且还需要等待排队，解决这个问题可以从哪些方面入手呢？谢谢。</div>2020-03-18</li><br/><li><img src="" width="30px"><span>GeekJ</span> 👍（1） 💬（1）<div>您好，我想请问在Facebook管理协作中，整个流水线的衔接、协作、融合、改进，是谁来推动的呢？或如何触发的呢？</div>2020-02-02</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/19/09/f2/6ed195f4.jpg" width="30px"><span>于小咸</span> 👍（1） 💬（2）<div>怎样提高自动测试的覆盖率和性能，会是很大的挑战，各模块开发者对其他模块不熟悉，发生bug的机率较高，测试覆盖到位比较难。

业务变化过程中，及时发现不必要的测试，提高测试性能也比较重要。</div>2019-09-04</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTJLPiafPkfZZg8xmrTkUiadHuBiaPticg6wUvOqkCicJTZE3LLL0TIiaWOX0tkRrSsJkOGsauYLHVauI2nQ/132" width="30px"><span>Geek_93f953</span> 👍（1） 💬（1）<div>持续集成、持续交付、持续部署的核心区别在我看来是自动化测试能力：
CI 每天多次将多人开发的代码合并到主干，并进行构建、代码检查、冒烟测试
CDelivery 自动将CI的结果打包、在测试环境和类生产环境进行自动化测试
CDeploy 自动将CDelivery的结果进行回归测试，并按照预设的灰度策略部署到生产环境</div>2019-09-04</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTLOMFSAg7ZEtwgdqTZMhjvdlOcRbHWTzDCBJMqdzpIqxQIRuE2aHianHHFibv1bGfAjnzmBpSJxx9MA/132" width="30px"><span>oliver</span> 👍（0） 💬（1）<div>增量测试有个问题，如果是较大范围的代码重构，如何确定增量测试的边界呢？</div>2020-04-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/82/a4/a92c6eca.jpg" width="30px"><span>墨灵</span> 👍（0） 💬（1）<div>我现在的公司还没有CI&#47;CD，看来要花时间搞起来，小公司很多东西都是不规范的。</div>2020-03-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/07/8c/0d886dcc.jpg" width="30px"><span>蚂蚁内推+v</span> 👍（0） 💬（1）<div>大仓库的缺点1.cu的执行效率可能有影响，代码获取，单元测试等全面检查等耗时长;2.代码的分支管理和合并复杂
Fb会做增量单元测试或自动化测试吗？她们包含部署和自动化测试的流水线的耗时大概是多少？我们面临的问题是部署时间5～10分钟，极大影响的反馈效率</div>2020-01-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/ca/8d/4ebf66a6.jpg" width="30px"><span>高倩</span> 👍（0） 💬（2）<div>比如，一个需求是基于用户不同状态来衍生出来的需求。测试过程中，需要考虑各种用户可能存在的状态扭转，以及对应的测试。但是上线以后，还是会存在没有考虑到的历史存量用户因为长期的业务累积，出现了预期之外的状态。导致代码上线以后，需要回滚。

再者，因为是多个端开发实现，上线时有一定的顺序上线，那比如等到中间上线的应用出现了问题。再想要回滚时，可能因为数据库数据被更改了的原因，导致无法回滚。后续就只能通过修复代码，或者修复数据库的办法才能解决</div>2019-09-17</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTLw3jpao45frZibQIAicWBfc7ofgrm5gJLiaFQSj5u2DDvkjy3ia5goicJLJlgVtZ0HryiaXb2VqpTSQT5Q/132" width="30px"><span>lisa</span> 👍（0） 💬（1）<div>请问facebook的性能测试平台和ci流程是怎么结合的？有专门的平台，还是这部分测试代码和单侧代码一样也是集成在工程里面随ci流程触发？</div>2019-09-16</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/ad/95/2d248ac2.jpg" width="30px"><span>师傅又被抓走了</span> 👍（0） 💬（1）<div>1 .在几千名开发人员共同使用一个大代码仓的工作方式下，做好 CI 有很大的挑战性。你觉得挑战在哪里，容易出现什么样的问题，又应该怎么解决呢？
容易出现代码合并冲突。出现冲突时的处理策略，回退or丢弃？冲突时，如何保证后续提交，可以正常合入？
功能依赖。功能模块大都不是独立的，如何保证双方一同合入？
代码功能冲突，大量冗余代码，一些功能可能会出现重复定义。

解决方案（我也不清楚，感觉需要一个好的架构师）</div>2019-09-05</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/ab/8b/fdb853c4.jpg" width="30px"><span>Weining Cao</span> 👍（0） 💬（1）<div>挑战在如何快速解决合并冲突。如何快速同步开发机器的代码保持最新。还有如果测试失败如何快速回滚。</div>2019-09-05</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/b1/4d/10c75b34.jpg" width="30px"><span>Johnson</span> 👍（0） 💬（1）<div>持续部署的描述那个链接打不开了</div>2019-09-04</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/4b/6f/ce96496d.jpg" width="30px"><span>飞奔的骆驼</span> 👍（0） 💬（1）<div>持续序列流水线中进去下一个节点的标准是什么，实操中难点是，大家对自动化的结果没有信心，如何做到呢？</div>2019-09-04</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/ca/8d/4ebf66a6.jpg" width="30px"><span>高倩</span> 👍（0） 💬（1）<div>大公司对接的业务复杂多变，很多线上故障都出现在一些没有预估到的流程。如何提高CI，如何全面自动化覆盖回归，这个是个很大的挑战。</div>2019-09-04</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/38/cf/f2c7d021.jpg" width="30px"><span>李双</span> 👍（0） 💬（5）<div>大公司的流程就是规范哈。如果一个小公司几十人的团队，是不是没必要搞这么多自动化，流程化，规范化。。。？</div>2019-09-04</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/c7/c6/35cc7c7c.jpg" width="30px"><span>Robert小七</span> 👍（0） 💬（1）<div>持续交付36讲专栏中说到持续交付包含持续集成和持续部署，老师你怎么看？</div>2019-09-04</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/f0/6d/3e570bb8.jpg" width="30px"><span>一打七</span> 👍（0） 💬（0）<div>看老师文中提到的主要是单元测试，想咨询下老师，在CD发布到线上环境时，这个流水线里有线上的自动化测试吗？比如说在上线的流水线里会先部署到预发布环境进行自动化接口测试，想知道Facebook这方便做的怎么样</div>2023-10-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/24/27/70/261d998b.jpg" width="30px"><span>cywen</span> 👍（0） 💬（0）<div>单元测试如何分级以使每次提交不用全量跑所有单元测试用例？在springboot项目中，单元测试一旦多起来，全量跑完耗时比较长，我们300多个用例就需要15分钟，每次提交都需要15分钟，开发使用的热情收到很大影响</div>2023-01-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1a/6b/5b/6d3ad7a3.jpg" width="30px"><span>我是xd</span> 👍（0） 💬（0）<div>目前经常说的CI CD主要是指持续集成、持续交付。持续部署一般公司都有固定的发布大版本的时间，不会频繁发布线上，除了紧急的hotfix。

持续集成是指开发频繁提交本地的开发代码到主干分支上进行代码集成，避免所有开发同一时间提交大量代码产生的代码冲突问题

持续交付是指对开发持续提交的代码发布到测试环境测试，测试通过后发布预发环境测试，确保每次提交后最新的主干分支验证通过保持可上线状态
</div>2022-05-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/ff/52/093bb1a1.jpg" width="30px"><span>小包</span> 👍（0） 💬（0）<div>Facebook 就有大量的单元测试和集成测试用例、安全扫描，以及性能专项测试用例
------
集成测试、安全测试、性能测试这些测试用例facebook是哪个角色完成的呢？
</div>2021-02-19</li><br/><li><img src="" width="30px"><span>Geek_0939f6</span> 👍（0） 💬（0）<div>问题1最大困难是代码提交都会卡在最后时刻，不管如何强调必须提前合并但是还是不被遵循，最后导致code reviews时间压缩，review不了了之流于形式</div>2021-01-05</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/DYAIOgq83eoOGZ6lbHiboIZMN9USbeutnmCWBahVLtSlKlIENKvrZQCUQzpzeZQOxTntIkBUeDk6qZUPdqmfKrQ/132" width="30px"><span>宝宝太喜欢极客时间了</span> 👍（0） 💬（4）<div>我再jenkins+gitlab+sonar做集成的时候，想通过Merge Requests触发代码检查，并且只检查请求合并的代码，这样能实现吗？有没有实现的教程可推荐呢？</div>2019-10-13</li><br/>
</ul>