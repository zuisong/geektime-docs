你好，我是黄勇。今天我的目标是，让你快速掌握 OKR 的概念以及用法，相信你在看完这篇文章后，会对 OKR 有一个清晰的理解。

在 2015 年的某一天，我开始在公司小范围内实践 OKR，开启了一段神奇的 OKR 探秘之旅，一路踩坑不断。经过几年的学习和实践，我终于摸索出来一套能够在企业中有效落地 OKR 的实践方法。

为此，我想通过极客时间专栏，竭尽所能地分享我实践 OKR 时的一些心得，希望可以给你带来一点启发。

现在 OKR 在国内逐渐流行起来，越来越火的 OKR 究竟是什么呢？我就从这个问题开始聊聊 OKR 吧。

## 越来越火的 OKR 究竟是什么？

OKR 是一款目标管理工具，它由 Objectives（目标）和 Key Results（关键结果）两部分构成。同时，OKR 也被称为“目标与关键结果工作法”，简称为“OKR 工作法”。OKR 是融合了一系列框架、方法和哲学后的产物，它起源于 Intel，发展于 Google。

![](https://static001.geekbang.org/resource/image/ad/0e/ad16da5cc73c1517e7870933c0b7570e.png?wh=680%2A230)

其实，我们可以把 OKR 中的 O 想象成一个你想要去的最终目的地，它时刻为你指明前进的方向，此外，可以把 KR 想象成一个带有距离标记的路标，它时刻告诉你距离目的地还有多远。

以下描述都是 O：

- 成为市场的领导者
- 推出最受欢迎的 iPhone 应用程序
- 比去年创造更多的收入
<div><strong>精选留言（30）</strong></div><ul>
<li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/454EibFlHB6VucdjFQiatiau0VtMp5XBWv6Wva1Lf89F4QB3icxPuCG0LwzzB3EQ8dCOoFrC1NTMT3ickkC7r6azVOA/132" width="30px"><span>hedylh</span> 👍（3） 💬（2）<div>黄老师您好，作为技术部门HRBP，近段时间阅读了大量关于OKR的书籍，对OKR内涵，实操算是有了一些浅薄的见解。这里主要有两个实际问题想请教，望黄老师能够指点12，鄙人当不胜感激！
问题1.部门OKR与个人OKR的关系。下级员工到底支撑的是上级的OKR还是本部门&#47;团队的OKR？因为OKR实施有两条业务线，一是组织，二是个人。我看了市面上有关OKR的著作，都是强调下级员工要支撑部门&#47;团队OKR。
情况1：假如下级支撑了部门的OKR，那上级的OKR谁来承载？
情况2：假如下级支撑了上级的OKR，那部门的OKR谁来承载？
情况3：假如下级同时支撑了部门和上级的OKR，那过多的OKR不是和OKR的理念背道而驰吗？而且当上级OKR和部门OKR有出入时，下级员工有限的资源以及精力应该如何取舍？
情况4：假如将部门主管与部门OKR合并，然后部门主管在不影响下属的情况下，以个人资源以及能力去完成一些部门OKR没规定但自己认为有价值且能支撑企业级OKR的O是否可行？
问题2：开发的一些KPI是否能应用到OKR中，例如交付期限，BUG数，稳定运行数等？
再次感谢黄老师的耐心解答！</div>2019-07-06</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/18/45/42/d2cb8435.jpg" width="30px"><span>jerry</span> 👍（3） 💬（1）<div>OKR的基本概念和理念已经清楚了。

从去年到现在我在公司也推行了OKR工作法，以季度为单位制定，效果不是特别好，我知道问题肯定出在我们自己身上，碰到两个问题向老师请教下：

1, 业务部门写的OKR把具体的业务指标kpi当成KR，从定义上好像没有毛病，所以他们认为kpi和OKR区别不大，至少在形式上是一样的。

2,技术部门在OKR基础上同时在实施scrum敏捷开发，发现敏捷开发中的计划会议，总结会和OKR中的制定，周期回顾复盘是重叠的，导致很多会议，不知道如何是好。

期待老师的指点，谢谢。</div>2019-06-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/17/10/0e/e44fe6c0.jpg" width="30px"><span>undefined</span> 👍（14） 💬（1）<div>文章中提到这个OKR适合组建学习型团队，提升团队成员的个人能力。技术团队确实需要不断的学习和成长，然而我们公司属于996型的公司，经常连续性加班，个人的时间很少，这样的团队能否使用OKR</div>2019-06-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/3b/36/2d61e080.jpg" width="30px"><span>行者</span> 👍（3） 💬（1）<div>OKR - Objectives &amp; Key Results
KPI - Key Performance Indicator
OKR目标在前，行动在后；KPI更多的体现在行动上。
从人性上讲，OKR让员工充分了解目标，有更好的主观能动性。
在适用场景上，KPI用在生产型公司比较多，因为更多的产品=更好的效益；对于广大互联网公司这个等式是不成立的，需要让员工自己去找到KR，所以互联网公司大多使用OKR。
昨天重新看了我之前定的OKR，发现部分KR定的是有问题的，不具体，更像O。-_-</div>2019-06-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/59/0c/f0952a99.jpg" width="30px"><span>ming_hgm</span> 👍（6） 💬（1）<div> KPI强调的是结果，只强调KPI的坏处是会不择手段达到KPI，也就是说呈现出来的未必是真的数据，OkR能帮助到您的是如何把事做好，配合使用很好。</div>2019-06-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/1e/84/03053efe.jpg" width="30px"><span>w*waiting</span> 👍（4） 💬（1）<div>okr和kpi的最大区别在参与感。
okr会让大家理解目标，每个人都要根据最终目标、阶段目标制定切实可行的计划，在保证目标准确性的情况下，又放大了人性的作用。
kpi是顶层设计思想，负责人制定考核指标（任务）后，参与者进行打怪升级，通过任务理解目标，不一定能100%实现最后的目标。</div>2019-06-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/48/ee/96a7d638.jpg" width="30px"><span>西西弗与卡夫卡</span> 👍（73） 💬（2）<div>OKR和KPI的差别主要不在形式，而在于底层理念和实施方法。

两者都可以用于目标管理。OKR偏重于目标制订，配合信息化工具可进一步延展，从战略拆解到目标初始制订，然后上下左右对齐，再到目标完成度和问题追踪，接着依据情况（包括执行状况、团队资源和市场情形等）进行调整，再开始新的循环。按照其理念，KR虽然有量化，但并不用于考核，而是给团队衡量目标的达成情况。

KPI的量化指标其实就是目标，但因为直接是数字，实践中容易让人忽略其背后企业和团队真正要达成的使命，而变成主要用来考核。在不强调使命愿景的时代，这是简单易用的绩效管理方法。

OKR强调目标制订和绩效考核分开，运用得好团队就可能制订出有挑战性的目标。KPI直接用来考核，团队可能就会保守。

OKR和KPI都可以达到信息透明、沟通顺畅的目的。它们更主要的差别是，前者强调上级的辅导职能（时髦词叫赋能），帮助团队达成目标，而不是完成不了受惩罚。后者则强调监控，胡萝卜和大棒齐飞。</div>2019-06-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/ea/1b/32954f5e.jpg" width="30px"><span>祥</span> 👍（8） 💬（2）<div>老师请教下，怎么理解子目标与KR，kr是否也可以变成o再拆解出KR？</div>2019-06-30</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/57/6e/b6795c44.jpg" width="30px"><span>夜空中最亮的星</span> 👍（6） 💬（2）<div>一切不以物质激励为前提的激励都是扯犊子。okr kpi 都是换个方式管理人。谷歌是全球福利最高的公司，这个是大前提。就算不搞okr 搞okx 也能成功。最根本的问题是，老板雇你来实现老板的目标和理想的，还是你和老板的目标一致利益一致</div>2019-06-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/30/cb/95ea2150.jpg" width="30px"><span>KK_TTN</span> 👍（3） 💬（1）<div>大家都在讨论OKR和KPI的区别，个人经历来看其实只是赋予一系列行为以一个名词，KPI如果也是上下同欲制定出来，专注于几个核心目标，也伴随着成长和激励，那这是KPI还是OKR呢？</div>2019-06-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/f2/70/8159901c.jpg" width="30px"><span>David Mao</span> 👍（3） 💬（1）<div>年初的时候，百度刮起了OKR的风暴。国内其他公司也竞相效仿，传统企业过去大多采用KPI来做绩效考核，但现在出现了很多的不确定性，任何公司都在积极思考未来的变革和方向，OKR相比KPI更能应对这种变革和未来的不确定性。</div>2019-06-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/f9/07/e4cc74a7.jpg" width="30px"><span>王昶</span> 👍（2） 💬（1）<div>KPI把人异化为机器，只要有动作就能产生可预期的结果，注重的是动作；OKR发挥人的主动性，规定的是一系列目标。OKR是可调整的，KPI不好调整。</div>2019-09-06</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/59/1e/5f77ce78.jpg" width="30px"><span>吃草🐴~</span> 👍（2） 💬（1）<div>个人认为，OKR 比 KPI 在布置和分析任务时更为“负责”。打个程序猿角度的比方（个人理解），KPI 就仿佛是老大布置了任务和完成时间，稍微负责一点的最多也就是 Review 一下你写完的 Code。而 OKR 就好像老大布置完任务时会把接口写好，把框架搭好（比如 Dao 层写好），甚至会一同商量，把业务逻辑的思路也定了。这是我目前的理解~
我想请问老师一个问题：为何所有的 KR 都需要有挑战性？假使我列出了三个 KR，其中有一个是重复工作多但不太费脑子的那种可以么？</div>2019-07-15</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/18/66/77/0f661752.jpg" width="30px"><span>Rain Song</span> 👍（2） 💬（3）<div>完了，我还是很模糊。作为销售部主管，天职是完成业绩目标，使命必达，但按照OKR的理解，完成业绩目标只是关键结果的体现，我怎么制定O呢？</div>2019-07-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/57/6e/b6795c44.jpg" width="30px"><span>夜空中最亮的星</span> 👍（2） 💬（1）<div>我上次的留言有点片面，今天又重新反思了下OKR。1关于物质激励：目前自己是职业生存期，所以自己看中物质，这是我的阶段给我的局限。2今天对OKR的理解：OKR可以用来实现自己的计划，如果自己的目标和公司的一致最好，不一致就修改自己的，让自己的和公司的一致，当牛逼了在让公司适应自己。3跟老师好好学OKR，不要自我封闭。4自己要慎言</div>2019-07-01</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/ajNVdqHZLLAZUMxZDXiaVdiaEq6wK8XMBBXiaA6icoQykatgybzeqicLUv3420cCPqONmTwTZBydJG5V1TiamIyeiaTxw/132" width="30px"><span>unanao</span> 👍（2） 💬（1）<div>黄老师，您好，有没有推荐的okr管理工具啊？</div>2019-06-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/d0/46/1a9229b3.jpg" width="30px"><span>NEVER SETTLE</span> 👍（2） 💬（2）<div>老师，如果我制定一个KR对对应多个O，这样设定合不合理？</div>2019-06-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/18/4c/38/f7b6aa70.jpg" width="30px"><span>wyj</span> 👍（2） 💬（1）<div>个人认为，OKR. 应该更适合用到创新性质的管理活动中，如工程部  研发部等，旨在5激励员工；而KPI适合用到常规的   重复性的管理活动中，比如按图加工 的生产部门等，旨在完成绩效
</div>2019-06-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/e9/0b/1171ac71.jpg" width="30px"><span>WL</span> 👍（2） 💬（0）<div>老师讲的很好很清晰，有两点我不太理解，第一是“对齐”的概念是具体指什么，是指就目标而言下级目标是上级目标的一个分解项，还是行动上下级去跟上级确认自己的目标；第二是文章中说KR不是任务，但好像没说KR是什么，究竟啥才算关键结果我没有理解</div>2019-06-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/97/1a/389eab84.jpg" width="30px"><span>而立斋</span> 👍（1） 💬（1）<div>这段“我认为，OKR 是一种融入了人性的科学管理框架。在人性角度上讲，承诺的事情就要去努力做到。深层次来看，OKR 便恰恰体现了这样一种“承诺”精神，这也是社会心理学中提到的“承诺和一致原理”，即人们通常会将自己的承诺与行动保持一致。此外，当我们看到许多人在同时做某件事情时，自己也会跟着去效仿，这就是社会心理学中所提到的“从众心理”。可见，OKR 绝不是一款简单的目标管理工具，它充满了人性和智慧”，
“承诺”跟“从众心理”有什么交集呢？</div>2019-07-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/f7/9d/be04b331.jpg" width="30px"><span>落叶飞逝的恋</span> 👍（1） 💬（1）<div>其实不管是OKR还是KPI这些都是管理工具，工具没有单纯的好与坏，只有看实施的人。</div>2019-07-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/17/27/ec30d30a.jpg" width="30px"><span>Jxin</span> 👍（1） 💬（4）<div>文化这块补充下。因为写代码这件事有太多不好度量的点，代码规范，业务逻辑优雅实现，注释文档健全，测试代码覆盖率全面，开发进度等等等。所以对写代码这件事制订kpi的话很可能会带来更多问题。比方说，抓质速降，抓速质降，而且质和速本身也不好定论，比方说受限于员工技术水平，公司开放环境稳定健全，部门沟通机制，开发架构基建。所以，程序员这个职业采用kpi水土不服，因为工作结果不好指标度量。所以okr就比较适合，更具活力和灵活性。不过具体的kr还是可以挂一些明确的kpi项的。而且如果项目抓速其实kpi会更适合，抓质和综合指标okr更合适。</div>2019-07-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/f6/6d/143deae5.jpg" width="30px"><span>冬天的树</span> 👍（1） 💬（1）<div>老师。请教个问题，像我们这种项目型的公司是都适合Okr。每次都是好多项目并行，都是以项目的进度为衡量目标，，那怎么样制定O呢？</div>2019-07-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/26/a8/3ec2d0fd.jpg" width="30px"><span>weilei</span> 👍（1） 💬（1）<div>OKR与KPI的区别，浅见如下：
    ①目标高度不同，OKR站在更高、更远的角度设定目标，而KPI更在意眼前的目标(OKR好比挣年薪，KPI好比挣月薪)；
    ②沟通角度不同，OKR的沟通的范围比较宽广，而KPI比较局限(OKR好比沟通整个技术框架，KPI好比沟通技术框架中的某一个技能点)；
    ③成就感不同，OKR带来的成就感不仅有物质奖励还有精神奖励，而KPI更多的是达到标准后的物质奖励(OKR好比成绩优异并且帮助其他同学一同获得奖学金，KPI好比成绩优异获得奖学金)。</div>2019-07-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/76/93/c78a132a.jpg" width="30px"><span>果然如此</span> 👍（1） 💬（1）<div>我以为是单选</div>2019-07-01</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/40/10/b6bf3c3c.jpg" width="30px"><span>纯洁的憎恶</span> 👍（1） 💬（1）<div>初学者的粗浅理解：KPI是以指标为核心，冷冰冰的数字意味更浓，不太容易把其背后的思想准确传递给员工，时间长了也容易变味，上有政策下有对策嘛。OKR是站在价值观、使命感与自驱力的高度，更重视上下同欲与步调一致，自发与赋能的意味更重。</div>2019-06-30</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/17/37/4e/5c3153b2.jpg" width="30px"><span>知行合一</span> 👍（0） 💬（1）<div>OKR和API有什么不同？都是目标管理，但OKR更强调主动和过程，API更强调被动和结果。OKR制定需要向上对齐和部门间或者员工间的平级对齐。关键结果可量化可调整。制定之后有阶段性成果可以检验。流程更加完善，需要公开透明，不断更新进度，并在周期结束时评估和复盘，再开始下一轮OKR周期。</div>2019-12-29</li><br/><li><img src="" width="30px"><span>andox</span> 👍（0） 💬（1）<div>O和KR 这两个我没搞太清楚界限，比如 KR1：专栏“累计订阅数”达到 10000 人 ，是不是也可以当成一个O，如何去界定和划分？</div>2019-11-07</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/70/c2/aeda3aab.jpg" width="30px"><span>馍馍</span> 👍（0） 💬（1）<div>您说到“子 O 支撑上级 O”，同时也说到“KR 支撑 O”
结合两者我就顺理成章的理解成了：上级的 KR 就是下级的 O
但是您又说不能这样做；
我看您的示例都是单独的 OKR，能举个下级怎么拆解上级的 OKR 例子吗？万分感谢。</div>2019-09-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/12/e5/592d9324.jpg" width="30px"><span>TH</span> 👍（0） 💬（1）<div>黄老师，文末的例子“在极客时间上发布精品OKR专栏”，我感觉重点在于“发布”，但是看下面的两条KR，似乎针对的是“精品”，请问是这样吗？我觉得如果目标只是发布专栏，难道KR不应该是多长时间内完成多少篇文章吗？</div>2019-08-27</li><br/>
</ul>