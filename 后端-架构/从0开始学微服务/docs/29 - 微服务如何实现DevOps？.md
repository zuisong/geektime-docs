把一个大的单体应用拆分成多个微服务之后，每个服务都可以独立进行开发、测试和运维。但当拆分的微服务足够多时，却又仿佛陷入一个新的泥沼，无论是业务代码的开发还是测试和运维，工作量都比之前提升了很多。

采单体应用架构时，一个业务需求只需要修改单体应用的代码，然后针对这个单体应用进行测试，测试通过后再把单体应用的代码发布到线上即可。而拆分为微服务之后，一个大的系统被拆分为多个小的系统，一个业务需求可能要同时修改多个微服务的代码，这样的话多个微服务都需要进行测试，测试通过了都需要把代码发布到线上，显然工作量成倍增加。这时候就迫切需要一种新的开发、测试和运维模式来解决这个问题，这就是今天我要给你讲的微服务与DevOps。

## 什么是DevOps？

在介绍DevOps之前，我先来带你回顾一下传统的业务上线流程：开发人员开发完业务代码后，把自测通过的代码打包交给测试人员，然后测试人员把代码部署在测试环境中进行测试，如果测试不通过，就反馈bug给开发人员进行修复；如果通过，开发就把测试通过的代码交给运维人员打包，然后运维人员再发布到线上环境中去。可见在传统的开发模式下，开发人员、测试人员和运维人员的职责划分十分明确，他们往往分属于不同的职能部门，一次业务上线流程需要三者之间进行多次沟通，整个周期基本上是以天为单位。你肯定会想假如能够把开发、测试和发布流程串联起来，就像生产流水线上那样，每个步骤完成后，就自动执行下一个步骤，无须过多的人为干预，业务的迭代效率不就能提升很多吗。
<div><strong>精选留言（15）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/12/69/4d/81c44f45.jpg" width="30px"><span>拉欧</span> 👍（19） 💬（1）<div>单元测试是对每一个接口，每一个方法进行边界验证，集成测试是对整个调用流程进行测试，一般来说单元测试全通过集成测试也可能会暴露一些问题，但是单元测试不通过集成测试一定gg</div>2018-10-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/be/72/0df5092d.jpg" width="30px"><span>shawn</span> 👍（4） 💬（1）<div>Jekins 应该是 Jenkins。
顺便问一下，拆分成微服务之后，服务之间的兼容性是怎么处理的呢？</div>2018-10-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/2e/b5/5f1c7ae1.jpg" width="30px"><span>AmosWooo</span> 👍（4） 💬（1）<div>我的理解是UT是从函数粒度来保证业务逻辑的正确性合理性，可以帮助发现业务逻辑缺陷; IT则是从接口粒度来保证整个系统在子服务的协同下可以达到预期输出。IT作为软件系统交付的前一环节，主要是进一步验证系统核心业务逻辑的可用性，稳定性。</div>2018-10-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/46/c0/106d98e7.jpg" width="30px"><span>Sam_Deep_Thinking</span> 👍（2） 💬（1）<div>写的太好了，收货颇多。</div>2018-10-28</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/3XbCueYYVWTiclv8T5tFpwiblOxLphvSZxL4ujMdqVMibZnOiaFK2C5nKRGv407iaAsrI0CDICYVQJtiaITzkjfjbvrQ/132" width="30px"><span>有铭</span> 👍（1） 💬（1）<div>集成测试时跑测试用例你们是自动化的吗，用的什么工具实现自动化的测试用例？</div>2018-10-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/67/f4/9a1feb59.jpg" width="30px"><span>钱</span> 👍（3） 💬（0）<div>单元测试：确认方法级别的逻辑正确性
集成测试：确认接口级别的逻辑正确性

目前我们的测试不是这么玩的基本需要人员来触发，不是自动化的，感觉也不容易自动化。

我们的环境也都是隔离的分成开发、测试、预发布、线上等。
测试起来流程也比较多：
1：研发开发及自测
2：测试测试
3：视情况而定，可能需要预发布联调测试
4：合主干回归测试
5：视情况而定，可能需要业务线上验证测试
6：以上比较顺利，则可以线上跑起来啦
</div>2019-06-16</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/7icFGrBnjMnulAdrghQ72y5wGQKbztaMN7a3mzzwMBrzwz5pxdU7zib17d29niapsP0uGeYpsX2BJ5gMUjLuCnMUA/132" width="30px"><span>infancy</span> 👍（2） 💬（0）<div>1开发自测，打提测分支
2测试做冒烟测试，功能测试
3涉及多个系统的大功能做跨产品联调
4改动大的话做回归测试
5自动化测试脚本还没用到</div>2020-03-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/ee/c6/bebcbcf0.jpg" width="30px"><span>俯瞰风景.</span> 👍（1） 💬（0）<div>DevOps 通过将开发、测试和运维流程自动化，以减轻微服务拆分后带来的测试和运维复杂度的提升，同时还提高了业务研发的效率。

为了实现开发、测试、运维的一体化，需要在流程中实现自动化测试和自动化运维。单元测试依赖于更高的单元测试覆盖率，集成测试依赖于更高的测试用例覆盖率。
自动化运维可以采用Jenkins和GitLab进行自动部署。</div>2021-10-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/81/14/f5f71b6e.jpg" width="30px"><span>小呀嘛小二郎</span> 👍（1） 💬（0）<div>微服务的模块太多，如何本地实现多服务测试，是再搭建一个开发环境嘛，那注册上去的节点我们可以通过dubbo配置嘛，是我本地注册上去的节点</div>2018-12-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/19/fd/58/1af629c7.jpg" width="30px"><span>6点无痛早起学习的和尚</span> 👍（0） 💬（0）<div>我部门的 QA 就在折腾持续集成里的单测、代码扫描、集成测试强卡点，在上线流水线里</div>2024-05-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/e9/cd/b4a1ccf5.jpg" width="30px"><span>Tony</span> 👍（0） 💬（0）<div>举个例子，B调用A，如果A服务，有多个分支f1，f2，f3个分支在测试，调用方B也有多个b1，b2分支。b1分支对应的是f2，b2对应f1分支，这种测试环境怎么测呢？微博这么大，一个微服务应该开发的人很多吧，不同人有不同分支，同时在测试环境怎么测试呢？</div>2021-02-05</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/49/44/dc73845c.jpg" width="30px"><span>王德宝</span> 👍（0） 💬（0）<div>注意到，持续集成案例中描述，deploy阶段，开发分支代码不是测试环境，test阶段，开发分支代码部署到集成环境，这个划分不是很理解啊？</div>2020-09-21</li><br/><li><img src="https://wx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTKmPib4xRxiaIuo4VGMfpnfcfWbM19vWbbjXDxXf6VcmvIvZV1ricvm5lhgmib7H9Fib6VowIpoj3vTh6w/132" width="30px"><span>季艳玲</span> 👍（0） 💬（0）<div>收获颇丰</div>2020-03-24</li><br/><li><img src="" width="30px"><span>suke</span> 👍（0） 💬（1）<div>请问微服务应该如何做到自动化的灰度发布或者金丝雀发布</div>2019-02-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/51/f1/752eaf9e.jpg" width="30px"><span>勤之鹿</span> 👍（0） 💬（0）<div>web1.0时代即单体应用时代的产品有必要做单元测试吗？我们团队的成员都没有编写单元测试的习惯，请问该如何养成这些好的习惯呢？</div>2018-11-09</li><br/>
</ul>