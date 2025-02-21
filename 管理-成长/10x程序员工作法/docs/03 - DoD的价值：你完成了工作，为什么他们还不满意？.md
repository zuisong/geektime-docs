你好，我是郑晔。

在开始今天的讨论之前，我们先来看一个小故事。小李是一个程序员，有一天，项目经理老张来到他身边，和他商量一个功能特性的进度：

> 老张：这有一个任务需要完成，你看一下。  
> 小李：这个不难，两天就能做完，两天以后就能上线。

两天以后，老张又来到小李的身边验收工作：

> 老张：怎么样，做完了吗？今天能上线吗？  
> 小李：我的代码写完了。  
> 老张：测试人员测过了吗？  
> 小李：还没有。  
> 老张：那今天能测完吗？  
> 小李：那我就不知道了。  
> 老张：什么？我可是答应了业务的人，今天一定要上线的！

很明显，老张有些愤怒，而小李也有些委屈。于是，老张、小李和测试人员一起度过了一个不眠之夜。

听完这个故事，你有什么感想呢？先不急，我们继续看后面的故事。

又过了几天，老张又来找小李，给小李安排一个很简单的功能。在小李看来，一天就能搞定，而按照老张给出的时间表，小李有两天时间处理这个功能。小李心中暗喜：看来我可以“偷得浮生一日闲”了。

两天以后，老张又来检查工作。

> 老张：这个功能开发完了吗？  
> 小李：写完了，你看我给你演示一下。

小李熟练地演示了这个新写好的功能，这次老张很满意：

> 老张：做得不错。单元测试都写了吧？  
> 小李：啊？还要写单元测试吗？  
> 老张：要不为啥给你两天的时间？
<div><strong>精选留言（30）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/0f/75/9b/611e74ab.jpg" width="30px"><span>技术修行者</span> 👍（66） 💬（6）<div>看这篇文章的时候，我一直在想着小兔子和大灰狼的故事。

小白兔在森林里散步，遇到大灰狼迎面走过来，上来&quot;啪啪&quot;给了小白兔两个大耳贴 子，说&quot;我让你不戴帽子&quot;。小白兔很委屈的撤了。
第二天，她戴着帽子蹦蹦跳跳的走出家门，又遇到大灰狼，他走上来&quot;啪啪&quot;又给了小白兔两个大嘴巴，说&quot;我让你戴帽子。&quot; 
兔兔郁闷了，思量了许久，最终决定去找森林之王老虎投诉。说明了情况后，老虎说&quot;好了，我 知道了，这件事我会处理的，要相信组织哦&quot;。
当天，老虎就找来自己的哥们儿大灰狼。&quot;你这样做不妥啊，让老子我很难办嘛。&quot; 说罢抹了抹桌上飘落的烟灰：&quot;你看这样行不行哈？&quot; 你可以说，兔兔过来，给我找块儿肉去！她找来肥的，你说你要瘦的。她找来瘦的，你说你要肥的。这样不就可以揍她了嘛。&quot; &quot;当然，你也可以这样说。兔兔过来，给我找个女人去。她找来丰满的，你说你喜 欢苗条的。她找来苗条的，你说你喜欢丰满的。可以揍她揍的有理有力有节&quot;。大灰狼频频点头，拍手称快，对老虎的崇敬再次冲向新的颠峰。 
不料以上指导工作，被正在窗外给老虎家除草的小白兔听到了，心里这个恨啊。
 次日，小白兔又出门了，怎么那么巧，迎面走来的还是大灰狼。大灰狼说：&quot;兔兔，过来，给我找块儿肉去。&quot; 兔兔说：&quot;那，你是要肥的，还是要瘦的呢？&quot; 大灰狼听罢，心里一沉，又一喜，心说，幸好还有B方案。 他又说：&quot;兔兔，麻利儿给我找个女人来。&quot; 兔兔问：&quot;那，你是喜欢丰满的，还是喜欢苗条的呢？&quot; 大灰狼沉默了2秒钟，抬手更狠的给了兔兔两个大耳帖子。 &quot;靠，我让你不戴帽子。&quot;</div>2020-03-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/44/47/3ddb94d0.jpg" width="30px"><span>javaadu</span> 👍（29） 💬（2）<div>之前就接过产品的类似这种需求：在某个全量表里加个字段。我接过来之后问了一个问题：业务方在什么场景下怎么用这个数据，产品经理语塞，最后这个需求转换成了一个数据分析产品的雏形，而我也用另一种临时的解决方案帮业务解决了问题。感受就是：产品当了传话筒，自己就必须搞清楚业务方要的到底是什么，也就是文中老师说的DoD</div>2020-03-01</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/fc/0a/ac47aaa2.jpg" width="30px"><span>雍</span> 👍（15） 💬（9）<div>公司有各种checklist，类似于DoD，举例开发过程自检就有41项，开发人员真要check完，至少要花半天时间，大多时候开发都是复制以前的，然后“偷得浮生半日闲”了，项目组成员一多，全部复核一遍基本不可能，如何确定真正落实checklist就成个问题了，老师有没有什么好的建议?</div>2018-12-31</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1d/08/e0/97260137.jpg" width="30px"><span>尚逸文</span> 👍（11） 💬（2）<div>老大让我这两天去熟悉一个框架，今天聊起来问我这个框架是什么，我笼统说了一遍在这个框架里数据的走向，老大表示要明白这个框架从底层究竟干了什么。惭愧，没学明白。看来我们对熟悉（这件事的DoD）的定义不同。
然后下班他把这个课程推给了我（捂脸</div>2020-03-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/92/6d/becd841a.jpg" width="30px"><span>escray</span> 👍（9） 💬（2）<div>DoD 是思维模式，其实也是一种沟通的方式吧。

感觉有时候不光是定义完成的标准，而且需要明确重要概念的定义，比如说完成标准中的那些检查项。

在 Scrum 中也强调 DoD，而且是要在团队中达成共识。一般情况下，和直接领导达成 DoD 的共识应该并不困难。

一方面可以要求领导能够提供或者一起讨论，得出准确的 DoD，另一方面可能也需要适度的揣摩，站在对方的立场上考虑一下可能存在的要求。工作中，难免会遇见领导或者客户无法给出准确定义和描述的时候，而且很可能并没有那么多沟通的机会。

文中列举的老张和小李的段子，其实双方都有责任。老张应该讲清楚 DoD，而小李也应该向上管理（沟通）问明白。

留言中的例子，老板说弄一下考勤，那么单纯的导出考勤记录明显不能满足老板的要求，简单的做一下统计，是应有之意。而如果做的太多，花费过多的时间和精力，似乎也没有什么必要。喜欢揣摩上意的非技术人员也不少。

还有那个总是被大灰狼扇耳光的小兔子，该跳槽了。</div>2020-05-31</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/37/3b/495e2ce6.jpg" width="30px"><span>陈斯佳</span> 👍（9） 💬（1）<div>定义DoD清单，可以参考使用SMART原则，也就是Specific（具体），Measurable（可衡量），Attainable（可达到），相关性（Relevant），有明确截止日期（Time-based）</div>2019-07-09</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/ibZVAmmdAibBeVpUjzwId8ibgRzNk7fkuR5pgVicB5mFSjjmt2eNadlykVLKCyGA0GxGffbhqLsHnhDRgyzxcKUhjg/132" width="30px"><span>pyhhou</span> 👍（5） 💬（1）<div>老师想请教一下，现在我在一家小公司里工作，人很少，没有项目经理，直接听老板讲需求，老板不怎么懂技术，没有什么技术基础，对一个项目需要的时间以及技术流程不太清晰，加上我也是刚从学校里出来可以说没啥经验，他问我多久能完成我也是迷迷糊糊的给不出一个大概的时间，老板需求也会时常变化即便是经常开会说想法讨论方案，没有严格的DoD，可能就像您说的完成功能代码就算完成，因此我们的产品老是出问题，想请问下在这种环境下如何更好的使用DoD呢，或者说是更好的提升工作效率，和上级沟通呢？是不是只要是时间足够就尽量把自己的DoD定严一些，或者是根据时间来定DoD？谢谢老师</div>2018-12-31</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTJ7mAt63VrbLZPHpeZxSc4IlBYswQSnaAB5wGePaGFDehgiaNfIxI1SJ5yIHIlmVk8hsw0RaoaSCPA/132" width="30px"><span>Stephen</span> 👍（4） 💬（1）<div>之前给自己估工作量的时候，往往直线思维。去想每个功能大概花多长时间，没有去考虑联调和最终测试的时间，到最后慌的不得了。这也是自己没有和自己做好DOD的情况</div>2021-05-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/21/30/8ecce1e1.jpg" width="30px"><span>北天魔狼</span> 👍（4） 💬（1）<div>偶像，醒醐灌顶啊。一开始就要确定完成的定义。</div>2018-12-31</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/dd/42/4a82631e.jpg" width="30px"><span>小小杨</span> 👍（3） 💬（1）<div>领导经常交代一些事 只是说要做好 没有说做到什么程度.开始按自己想象做 结果非常不好.反复返工.后来自己站在领导角度思考最终要什么结果，做到什么程度.有了结果做前先做确认，效果有显著提高，效率也高了，由于经常沟通默契也高了，达成一致很关键</div>2021-03-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/a1/a0/7687413f.jpg" width="30px"><span>Zopen</span> 👍（3） 💬（1）<div>新人刚入职场，编写完功能代码之后，被leader质问：单测为什么没写？功能为什么没测？因为职场新人不知道需要做这些，新人和leader的DoD未达成一致。解决方法：多跟leader沟通，弄清楚leader的DoD到底是什么。</div>2021-03-07</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/f5/cd/3890be04.jpg" width="30px"><span>小川</span> 👍（3） 💬（1）<div>老师，那应该按照什么标准来定义 DOD 呢。</div>2020-07-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/82/a4/a92c6eca.jpg" width="30px"><span>墨灵</span> 👍（3） 💬（1）<div>这段时间尝试实践以终为始的工作方式，效率确实比以前都有所提升了，产出的质量也有所提升。</div>2020-03-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/e6/b7/6065c5ce.jpg" width="30px"><span>xiaoqcn</span> 👍（3） 💬（2）<div>完全是教程序员怎么处理各种异常
不合格的项目经理
不合格的产品经理
。。。
当然，我们也有可能是不合格的程序员

何况，即使都合格还有意外</div>2020-01-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/2b/2b/7166cc98.jpg" width="30px"><span>木子輕颺</span> 👍（3） 💬（1）<div>最近两周在开发一个功能模块，当时刚好错过 DoD 这篇文章，那时草率的觉得完成任务的周期，当然了我是按照开发人员的角度来自我定义完成的，就是开发完成，自测完成。

现在功能模块正式上线，超过当时预期的两倍。其实这里面的问题让我思考很多，如何正确评估一个任务的工作量？对一个完全陌生的功能，需要陌生的组件呢？

现在重新回头看 DoD 觉得提前定义好概念，明确边界真的很重要。避免造成不必要的误解，最主要的可以缓解压力，免得高估自己。

当我开始下一项任务时，一定要对它拆开了看，明确每一个想当然的概念，把东西打散了拆开了看。然后再制定计划表。</div>2019-01-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/de/cf/ef2e0501.jpg" width="30px"><span>奇小易</span> 👍（2） 💬（1）<div># Why

工作中常见的例子，特性开发和功能开发，领导所理解的完成和员工所理解的完成不一致。这就是导致了自己明明完成了工作，领导却还是不满意的原因。

# What

人与人之间进行协作一起完成某件事时，必定存在理解上的差异，导致最终完成的结果无法让大家都满意。要让大家的理解达成一致，解决的方式可以使用业界的一种最佳实践。

DoD，完成的定义。就是一起协作完成某件事之前，先定义好这件事情完成的标准。

例如：功能开发的完成定义，完成功能代码、单元测试、集成测试，测试可以通过，代码通过了代码风格检查、测试覆盖率检查。



想要更好的发挥DoD的作用，需要三个

- DoD是一个清单，清单是由一个个检查项组成的，用来检查我们的工作完成情况。

- DoD的检查项，是实际可检查的。可以通过某种手段检查是否完成。例如：功能做完了，通过演示功能来检查；

- DoD是团队成员间彼此汇报的一种机制。有了DoD之后，做事的状态就只有完成和未完成。（有什么价值吗？）

# How

在团队层面也可以定义DoD，例如：某个功能的DoD，这个功能特性已经开发完成，经过产品负责人的验收，处于一个可部署的状态。



跨团队层面的DoD，例如：接口完成的定义。



工作生活层面的DoD，例如：帮忙买手机的定义。仅帮忙确定手机款式。



DoD是一种思考方式，让协作的双方尽可能达到共识的一种方式。</div>2021-07-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/21/c0/38816c31.jpg" width="30px"><span>春之绿野</span> 👍（2） 💬（1）<div>之前做过一个任务是测试artifactory 的性能，并发上载下载100个时的表现，然后我测了，等到周末review 的时候我们组架构师说你怎么只测了100个，0到100间其他的数字呢？我说plan 的时候也没有要求啊，架构师说你自己不会举一反三吗？其实那次不光没有dod ，需求澄清也有没弄清楚“终”是什么。现在回过头来看发现我们的工作做的都好不专业啊。不过后来我们有了ac，就是accept criterion ，也是检查项，不然真是扯不清楚。</div>2019-05-02</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/6a/5b/b973bf40.jpg" width="30px"><span>大廖</span> 👍（1） 💬（1）<div>感觉和另一个说法，有个叫“目标对齐”有点像</div>2020-11-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/34/01/30ca98e6.jpg" width="30px"><span>arronK</span> 👍（1） 💬（1）<div>之前完全不知道DoD。
不过可以说个我的例子，在我们团队里面，之前对一个开发版本是否开发完成的定义是功能完成和UI也完成。
后来我发现功能完成后给到测试进行测试的期间，我们的时间是空余的，于是我就在团队里强调，提测仅限于功能提测，功能完成即可给到测试。然后在测试期间我们再去细调UI，这样异步进行，整体效率提升不少</div>2020-10-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/43/e1/b7be5560.jpg" width="30px"><span>sam</span> 👍（1） 💬（1）<div>定义DoD的过程中，也梳理了工作，甚至工作的拆解也大概明确了，间接推动完善的事项还挺多的</div>2020-06-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/3b/86/170e58ae.jpg" width="30px"><span>一个帅哥</span> 👍（1） 💬（1）<div>做事情之前，要确保双方对完成的定义的理解是相同的</div>2020-05-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/18/89/a5/f89a1946.jpg" width="30px"><span>快乐一家</span> 👍（1） 💬（1）<div>开发前确认验收标准，然后按照验收标准进行开发</div>2020-03-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/17/74/ff/a60f335b.jpg" width="30px"><span>利</span> 👍（1） 💬（1）<div>老师有时间可以回答一下我的问题么？ 比如技术性调研如何进行DoD设置或者说分解，还有一些辅助性的工作如何设置DoD？ 另外DoD是要监督执行，还是强调个人的自发性？</div>2020-03-05</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/c5/5e/24cc5a72.jpg" width="30px"><span>阿狸爱JAVA</span> 👍（1） 💬（1）<div>一开始钢筋公司的那会，组长让我梳理一个下单的流程，我以为他说的是创建订单这个功能，而到最后才发现他说的是经过各个审批之后的下单。由此增加了我和他之间的埋怨。类似这样的事情发生过多次，在工作中，总是因为各种原因没有做DoD，又或者比如接口，明明做了参数和返回值的定义，但对方依旧会在开发过程中对其进行改动，导致我方针对该接口的调用又要重头再来。</div>2018-12-31</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/83/ad/d3cb8dc5.jpg" width="30px"><span>Toly</span> 👍（0） 💬（1）<div>需求文档应该也算是Dod的一部分， 如果我没理解错。</div>2021-05-03</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTJbh5FQajwKhNlMrkoSklPpOXBtEYXCLvuWibhfWIS9QxHWDqzhEHJzEdmtUiaiaqFjfpsr2LwgNGpbQ/132" width="30px"><span>Geek_q29f6t</span> 👍（0） 💬（2）<div>漫无边际，无限延展的“终”是没有意义的。DoD 就是用来定义“以终为始”的“终”，何时才是“终”，如何才是“终”。</div>2020-07-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/18/a0/5f/cf72d453.jpg" width="30px"><span>小豹哥</span> 👍（0） 💬（1）<div>统一团队对事情完成的结果，结果的完成可以由一项项检查项构成，这些检查项都完成了，事情也就完成了。</div>2020-06-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1b/a9/ea/5bfce6c5.jpg" width="30px"><span>mgs2002</span> 👍（0） 💬（1）<div>遇到过很多次因为两方对于某个东西理解不一样导致的问题，确实没有做好DoD的有效沟通，没有就完成的标准达成共识</div>2020-06-15</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/5fibB9p7PfndN4kU0lhHv4TyKRsibISvaxGdI4yviao0WcDS7rmEP9vqiaMiclxrs2GQJlRcCyZxTkRibK5r4uWQQBhg/132" width="30px"><span>wengyifa</span> 👍（0） 💬（1）<div>其实一直都有确定目标完成标准的想法，但是当任务来临的时候，通常都是仅仅只有一句话或者一句口头的嘱咐，目标相当的模糊，在这么模糊的目标下，想要具体问一些细节，就感觉无从下手，不知道从哪里问题，只先答应做了先，一些细节问题才会做的过程中慢慢浮现出来，这样效率就完全下降下来了。对此老师是否能给出点指导意见呢？</div>2020-06-01</li><br/><li><img src="" width="30px"><span>高飞龙</span> 👍（0） 💬（1）<div>收获颇深，站在完整的角度看待问题</div>2020-03-21</li><br/>
</ul>