你好，我是石雪峰。

当一家企业好不容易接纳了DevOps的思想，并下定决心开始实施的时候，总会面临这样一个两难的选择：**工具和文化，到底应该哪个先行？**

的确，在DevOps的理论体系之中，工具和文化分别占据了半壁江山。在跟别人讨论这个话题的时候，我们往往会划分为两个不同的“阵营”，争论不休，每一方都有自己的道理，难以说服彼此。在DevOps的世界中，工具和文化哪个先行的问题，就好比豆浆应该是甜的还是咸的一样，一直没有一个定论。

可是，对于很多刚刚接触DevOps的人来说，如果不把这个问题弄清楚，后续的DevOps实践之路难免会跑偏。所以无论如何，这碗豆浆我先干为敬，今天我们就先来聊聊这个话题。

## DevOps工具

随着DevOps理念的深入人心，各种以DevOps命名的工具如雨后春笋般出现在我们身边，甚至有很多老牌工具，为了顺应DevOps时代的发展，主动将产品名称改为DevOps。最具代表性的，就是去年9月份微软研发协作平台VSTS（Visual Studio Team Services）正式更名为Azure DevOps，这也进一步地印证，DevOps已经成为了各类工具平台建设的核心理念。

在上一讲中，我提到高效率和高质量是DevOps的核心价值，而工具和自动化就是提升效率最直接的手段，让一切都自动化可以说是DevOps的行为准则。
<div><strong>精选留言（30）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/0f/b2/1c/48558abc.jpg" width="30px"><span>九脉一谷</span> 👍（19） 💬（1）<div>这两年来一直在推动内部研发体系的建设，平台从无到有，自主投入研发。但是在平台推广过程中遇到了很多问题，总结一下几点感受：
1、首先需要有一个认可的部门大领导支持，而且一定是要当成一项重点工作来推进；
2、平台开发团队的成员也需要形成统一的认识，是为整个公司研发体系服务，是先行者，改革者，同时我们也是平台用户，要坚信通过平台化、自动化、标准化是能够改善现状，提高效率，提升软件质量的；
3、要长期给项目业务线的核心骨干人员“洗脑”，宣传devops的理念，培训平台的功能点，指导依赖工具的使用，主动帮助梳理他们现有不合理的流程，尽量通过平台来帮助改造；
平台的建设推广，无论是领导，还是平台开发者，项项目业务线人员，更多的是人的认知的改变。</div>2019-10-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/4d/4d/abb7bfe3.jpg" width="30px"><span>铭熙</span> 👍（44） 💬（1）<div>雪峰帅哥，既然你说人加流程等于文化，展开下说如何从人和流程下手，有什么变化？</div>2019-10-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/c7/2d/05a18518.jpg" width="30px"><span>李金洋</span> 👍（30） 💬（1）<div>石老师好， 我们是运维团队，如果从运维团队去主导这种devop的推进，有什么好的思路？因为毕竟和开发是两个团队，所以我们之间的工作职能和理念其实不一样，如何能够统一两者，如何能在运维的角度，去让devops能够在所有团队推进起来？</div>2019-10-15</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/37/3b/495e2ce6.jpg" width="30px"><span>陈斯佳</span> 👍（8） 💬（3）<div>我们公司现在就在做DevOps的转型，我个人感觉到最大的阻碍，不是流程，而是人。一些老的员工不愿学习新的流程和工具，让转型变得很困难。我自己的实践方法就是，在各个部门中（开发&#47;测试&#47;运维&#47;DBA）找到那个最积极、最愿意改善的人，然后推进新流程和新工具的落地，等有了实际案例流程打通之后，再去和其他人推广。真心感觉人的积极主动才是一切变革的核心和内在驱动力</div>2019-10-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/03/8d/38a98dc6.jpg" width="30px"><span>牧野静风</span> 👍（5） 💬（2）<div>石老师好，我是一个运维，公司开发部门还是比较传统的方式，推动DevOps是否一定需要CTO级别的人来推动</div>2019-10-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/01/c2/0b88a29e.jpg" width="30px"><span>柯基道格</span> 👍（3） 💬（2）<div>文化VS工具。这个问题在很尖锐，个人认为文化和工具需要齐头并进，而且两者的推广并不冲突，但我认为工具可以先行。因为，文化是潜意识，工具是表意识，文化并不能马上让人接受，人对新文化的接受是慢慢才能接受，有时可能不达到触及某个痛点，可能永远都不接受，但工具不一样，工具是看得到摸得着的，接受起来比虚拟的文化更容易让人接受，就好比让父母用手机支付，如果只是空谈无币文化，而没有真实给他们买上一部手机和装上支付宝，是永远不会接受这个新鲜事务的。
说下我们公司一直存在的问题，我们是国企体制内的公司，想推广文化可比一般的互联网企业难太多了，国企的中上层，可能都不是技术出身（列如部门老大，没写过代码，没做过测试，没干过运维，只是在外包的协助下干过需求），对于技术文化的理解并没有技术人员那么透彻，对于国企管理者来说，只在乎结果完成，怎么过程并不重视。虽然随着DEVOPS的盛行，国企领导也听入其中，但是还是将其视为可以更快的出结果，而不是部门融合的文化。众所周知，国企类公司拥有难以打破的部门壁垒，部门与部门之间就如同次元壁一样难以打破。在这种情况，文件难以推广的情况下，我只能以工具效能的方式去推进，不知这算是无奈，还是这种模式只能如此。</div>2020-02-15</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/17/27/ec30d30a.jpg" width="30px"><span>Jxin</span> 👍（2） 💬（1）<div>看完老师文章，自己总结下。

1.人的主观意愿 + 制度 = 文化
2.流程的抽象 + 平台的落地 = 工具
3.人的诉求 + 平台的推广 = 培训

平台的定义：
1.可扩展，纵向扩展或横向扩展（不一定必须要很自由）
2.横向扩展，聚合多个工具或服务，助力某一大类工作的所有工作诉求，解决一个更大问题域的问题。
3.纵向扩展，从单体工具或服务，往多租户的工具或服务演变，提供配置化的定制能力。

</div>2019-10-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/cc/23/4d622bea.jpg" width="30px"><span>鲍建飞</span> 👍（2） 💬（1）<div>看了有段时间devops，但感觉一直在门外转来转去，文化工具都有了解，可能还是实践差了一些</div>2019-10-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/97/1a/389eab84.jpg" width="30px"><span>而立斋</span> 👍（2） 💬（1）<div>老板对这事儿还没有一个直观的考量，虽说有老板的加持，但他们总觉得现在这种传统手工作业的形式还挺好。所以我需要系统的知识进行引导，很荣幸遇到您。</div>2019-10-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/5b/b8/7b39de23.jpg" width="30px"><span>Geek_599062</span> 👍（1） 💬（1）<div>标准化都还没做好，路太长。对于如何推动公司技术栈的标准化，石总有何高见?</div>2019-10-14</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTIh6ofbI5fJbYN0kYmOw8hK6GLg2AOl2DX3Tnk1dC7OQFoQw11OLomtjnMBgjPVCy6eCjaDE5X6icg/132" width="30px"><span>caozhao</span> 👍（1） 💬（1）<div>石老师好，
devops 看起来虽好，可以提高开发效率，目前又有Aiops出现，如果需要转化到Aiops，devops文化会不会阻碍呢，devops是否有灵活性，可以转化或者可以添加其他技术 丰富devops平台。

回答问题：
我们公司 在很多最新的技术方面 比如devops 基本上一张白纸，所以有很大的上升空间，所以我们个人机会也很多，</div>2019-10-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/dc/19/c058bcbf.jpg" width="30px"><span>流浪地球</span> 👍（1） 💬（1）<div>老师您好，这句话不是很理解，平台的一些基础设施比如服务器，使用方增多了自然会增值，如何理解不线性增长呢？
规模效应：平台的成本不会随着使用方的扩展而线性增加，能够实现规模化


</div>2019-10-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/15/02/66f65388.jpg" width="30px"><span>雷霹雳的爸爸</span> 👍（0） 💬（1）<div>按照老师文章的定义，流程之下的人形成自身的行为准则，而准则的集合体构成文化；这么看起来，我们公司也没什么流程，我们的准则看起来就是别搞得太难看，谁都别太过分，那么我们形成的文化就是互相尊重，允许自由发挥，崇尚自我约束，就是自律啊...这么看起来我们的文化很高级啊，应该能让我们有了一个宽松的空间来实施devOps啊</div>2019-10-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/a8/e8/bc84c47d.jpg" width="30px"><span>熊斌</span> 👍（0） 💬（1）<div>喜欢那句 “真正的高手，比拼的不是武功，而是思想”，如果想法不对，手里攥一堆工具也是白搭。
总结起来就是 对的人+对的流程+对的平台</div>2019-10-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/7f/77/8c34e407.jpg" width="30px"><span>kalid</span> 👍（0） 💬（1）<div>DevOps 由人+流程+平台工具构成一个有机整体，其中最主要的还是人。推动需要一个说得上话的人，推进需要一群志同道合的人，实现则是服务一帮人。把人搞定了，什么都好搞了😄</div>2019-10-15</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/34/df/64e3d533.jpg" width="30px"><span>leslie</span> 👍（0） 💬（1）<div>       谈不上吸引吧：部门文化比较自由，不违法公司规定的事情基本不管-适合自己完成当下并做些技术钻研和探索；本地其它企业都会管理的偏严而忽视了效率。
        学习是为了自己的未来去探索和实践：明白怎么做了当机会来临时把握了就好。就像二叉树视频中鸟哥所说：“机会来临前你已做好了准备，机会来临时抓住就好”😀</div>2019-10-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/a8/b2/998448ca.jpg" width="30px"><span>悠游</span> 👍（7） 💬（0）<div>People、Process、Platform简称3P</div>2020-04-06</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTJe2v5tzdicP1tMPmEkjD7ltj4DGMqeN7C2eZoRJMOSTEN4r8YUnia7oPEib1IZPdagJadz0ibTWsocRg/132" width="30px"><span>Geek_c12cd9</span> 👍（2） 💬（0）<div>试读了4篇文章，感觉每一段、每一句话都是丰富的经验积累和完美的总结归纳出来的体现，受益匪浅。</div>2020-08-05</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/19/1b/ea/976c77a4.jpg" width="30px"><span>张哲宇</span> 👍（1） 💬（0）<div>太赞同了，企业搭建效能中台的主要目的还是固化标准动作，诚然企业中一定有不愿被束缚的“天才”，但更多的都是平庸程序员</div>2020-12-03</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1d/3f/0d/1e8dbb2c.jpg" width="30px"><span>怀揣梦想的学渣</span> 👍（0） 💬（0）<div>我认为工具是解决方案的组成部分，工具随时可以被替换，不能固定只有一个选择。
研发和运维的矛盾主体在于利益未捆绑一起，如果将研发和运维的绩效考核捆绑一起，共同进退，可以约束他们少一些帅锅，因为锅在内循环，甩不出去，集体绩效受影响。</div>2023-06-01</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/b4/17/0b5aad57.jpg" width="30px"><span>Marx</span> 👍（0） 💬（0）<div>任何问题的解决不外乎“人-事-物”三大要素。人即组织，事即流程，物即工具。</div>2023-04-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/e6/74/8b8097c1.jpg" width="30px"><span>牛2特工</span> 👍（0） 💬（0）<div>我们之前也做过DevOps工具开发，也是基于开源的二次开发，
做了有两年都不太成熟，各种问题层出不穷，当然我现在也不记得具体有哪些了，
落地应用的地方也是少之又少。
我想您的团队可能是比较强的，DevOps工具和流程本身也可以视作是一个产品，
团队开始做的时候自己可能就设计走偏了，或者压根也没什么规划，很快就成为了一个烂摊子。。
</div>2021-06-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/0b/ce/9920a59e.jpg" width="30px"><span>一醉</span> 👍（0） 💬（0）<div>老师好，我现在在一家小公司带产品研发团队，50人左右，基建相关能力（工具 平台 思想）刚起步，想咨询一下，这个阶段从哪个点落地DevOps比较好，按照怎么样的思路去走这条路呢？</div>2021-04-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/67/63/abb7bfe3.jpg" width="30px"><span>atom992</span> 👍（0） 💬（0）<div>关于DevOps的推广，我们计划的做法是CI是研发负责建立一个平台，CD是运维负责建立一个平台，先各自把各自关注的这一块打通，有了效果之后，再考虑串在一起，这样既能提高各自的效率，转型也不至于步子太大，阻力太大不好转。</div>2020-12-16</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/2a/ff/a9d72102.jpg" width="30px"><span>BertGeek</span> 👍（0） 💬（0）<div>新文化的推行，需要管理层给予技术、人力、财力支持。
工具的推行和迭代需要广和深，需要具备思想、文化，才能更好融入和组架！</div>2020-09-02</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/75/9b/611e74ab.jpg" width="30px"><span>技术修行者</span> 👍（0） 💬（0）<div>公司在前几年开始从上到下推广敏捷文化和敏捷实践，这对实施DevOps启动了很好的推动作用。
工具和文化都很重要，如果先选其一的话，我倾向于工具，用工具做一些大家能直接看到的事情，显示DevOps带来的好处，然后通过培训推广，进行文化建设。</div>2020-04-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/43/65/bf57c323.jpg" width="30px"><span>Pyel</span> 👍（0） 💬（0）<div>没有文化氛围的话，感觉还是难以落地……</div>2020-03-29</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTLAqN8yGhXKdUS9nLhEiapfesLdjEdBDJZhClibxOicYCpAeic92oIFYQnicywAF5lPROSIia6HWSrrF8pA/132" width="30px"><span>callmebaby</span> 👍（0） 💬（0）<div>学习了</div>2020-03-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/3a/46/82ce02f1.jpg" width="30px"><span>mayunyong</span> 👍（0） 💬（0）<div>老师这篇文章的高度蛮高的，不仅仅适用于DevOps，更像一篇理论指导，很多内容在工作中都是可以借以思考和学习的。</div>2020-02-04</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/37/3b/495e2ce6.jpg" width="30px"><span>陈斯佳</span> 👍（0） 💬（0）<div>对的，我十八岁之前都还不知道这世界上还有咸豆浆……</div>2019-12-30</li><br/>
</ul>