在上两节课中，我们学习了SOLID原则中的单一职责原则和开闭原则，这两个原则都比较重要，想要灵活应用也比较难，需要你在实践中多加练习、多加体会。今天，我们再来学习SOLID中的“L”对应的原则：里式替换原则。

整体上来讲，这个设计原则是比较简单、容易理解和掌握的。今天我主要通过几个反例，带你看看，哪些代码是违反里式替换原则的？我们该如何将它们改造成满足里式替换原则？除此之外，这条原则从定义上看起来，跟我们之前讲过的“多态”有点类似。所以，我今天也会讲一下，它跟多态的区别。

话不多说，让我们正式开始今天的学习吧！

## 如何理解“里式替换原则”？

里式替换原则的英文翻译是：Liskov Substitution Principle，缩写为LSP。这个原则最早是在1986年由Barbara Liskov提出，他是这么描述这条原则的：

> If S is a subtype of T, then objects of type T may be replaced with objects of type S, without breaking the program。

在1996年，Robert Martin在他的SOLID原则中，重新描述了这个原则，英文原话是这样的：
<div><strong>精选留言（30）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/1a/e7/07/0e9d85c3.jpg" width="30px"><span>年轻的我们</span> 👍（319） 💬（19）<div>个人理解里氏替换就是子类完美继承父类的设计初衷，并做了增强对吗</div>2019-12-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/11/e9/13f28df2.jpg" width="30px"><span>狼行天下</span> 👍（4） 💬（1）<div>LSP 规定子类替换父类，不能改变父类的输入、输出、异常等约定
常见的反例类型包括：1、子类违背父类声明要实现的功能。2、子类改变父类的输入、输出、异常等约定。3、子类违背父类注释中所罗列的特殊说明</div>2020-11-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/0c/8f/166aa472.jpg" width="30px"><span>Geek_j8uecm</span> 👍（2） 💬（1）<div>第一遍学完这节课，我的问题就是里式替换存在的意义是为啥哈哈哈哈</div>2019-12-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/ef/89/8c73a24d.jpg" width="30px"><span>Chen</span> 👍（216） 💬（12）<div>135看设计模式，246看数据结构与算法。争哥大法好</div>2019-12-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/50/d7/f82ed283.jpg" width="30px"><span>辣么大</span> 👍（177） 💬（13）<div>LSP的意义：
一、改进已有实现。例如程序最开始实现时采用了低效的排序算法，改进时使用LSP实现更高效的排序算法。
二、指导程序开发。告诉我们如何组织类和子类（subtype），子类的方法（非私有方法）要符合contract。
三、改进抽象设计。如果一个子类中的实现违反了LSP，那么是不是考虑抽象或者设计出了问题。

补充：
Liskov是美国历史上第一个女计算机博士，曾获得过图灵奖。
In 1968 she became one of the first women in the United States to be awarded a Ph.D from a computer science department when she was awarded her degree from Stanford University. At Stanford she worked with John McCarthy and was supported to work in artificial intelligence.

https:&#47;&#47;en.wikipedia.org&#47;wiki&#47;Barbara_Liskov</div>2019-12-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/d8/d6/47da34bf.jpg" width="30px"><span>任鹏斌</span> 👍（151） 💬（1）<div>里氏替换就是说父亲能干的事儿子也别挑，该怎么干就怎么干，儿子可以比父亲更有能力，但传统不能变</div>2019-12-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/f2/aa/32fc0d54.jpg" width="30px"><span>失火的夏天</span> 👍（110） 💬（7）<div>里氏替换最终一句话还是对扩展开放，对修改关闭，不能改变父类的入参，返回，但是子类可以自己扩展方法中的逻辑。父类方法名很明显限定了逻辑内容，比如按金额排序这种，子类就不要去重写金额排序，改成日期排序之类的，而应该抽出一个排序方法，然后再写一个获取排序的方法，父类获取排序调用金额排序，子类就重写调用排序方法，获取日期排序。

个人感觉也是为了避免“二意性”，这里是只父类的逻辑和子类逻辑差别太多，读代码的人会感觉模棱两可，父类一套，子类一套，到底应该读哪种。感觉会混乱。

总之就是，子类的重写最好是扩展父类，而不要修改父类。</div>2019-12-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/17/27/ec30d30a.jpg" width="30px"><span>Jxin</span> 👍（61） 💬（3）<div>里式替换是细力度的开闭原则。这个准则应用的场景，往往是在方法功能的调整上，要达到的效果是：该方法对已经调用的代码的效果不变，并能支撑新的功能或提供更好的性能。换句话说，就是在保证兼容的前提条件下做扩展和调整。

spring对里式替换贯彻得不错，从1.x到4.x能看到大部分代码都坚强的保留着兼容性。
但springboot就有点跳脱了，1.x小版本就会有违背里式替换的破坏性升级。1.x到2.x更是出现跳票重灾的情况。带来的损失相信做过springboot版本升级的人都很有感触，而这份损失也表达出坚守里式替换原则的重要性。不过，既然springboot会违背经营多年的原则（向下兼容），那么绝非空穴来风，相信在他们看来，违背里式替换做的升级，带来的价值能够盖过损失。所以我觉得里式替换依旧是个权衡项，在日常开发中我们要坚守，但当发现不合理，比如设计缺陷或则业务场景质变时，做破坏性改造也意味着即使止损，是一个可选项。</div>2019-12-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/f5/94/67fabf8e.jpg" width="30px"><span>Kevinlvlc</span> 👍（52） 💬（0）<div>我觉得可以从两个角度谈里式替换原则的意义。
首先，从接口或父类的角度出发，顶层的接口&#47;父类要设计的足够通用，并且可扩展，不要为子类或实现类指定实现逻辑，尽量只定义接口规范以及必要的通用性逻辑，这样实现类就可以根据具体场景选择具体实现逻辑而不必担心破坏顶层的接口规范。
从子类或实现类角度出发，底层实现不应该轻易破坏顶层规定的接口规范或通用逻辑，也不应该随意添加不属于这个类要实现的功能接口，这样接口的外部使用者可以不必关心具体实现，安全的替换任意实现类，同时内部各个不同子类既可以根据不同场景做各自的扩展，又不破坏顶层的设计，从维护性和扩展性来说都能得到保证</div>2019-12-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/a3/eb/d26459ae.jpg" width="30px"><span>时光勿念</span> 👍（38） 💬（4）<div>呃，我不知道这样理解对不对。
多态是一种特性、能力，里氏替换是一种原则、约定。
虽然多态和里氏替换不是一回事，但是里氏替换这个原则 需要 多态这种能力 才能实现。
里氏替换最重要的就是替换之后原本的功能一点不能少。</div>2019-12-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/23/a1/b08f3ee7.jpg" width="30px"><span>何妨</span> 👍（16） 💬（0）<div>多态是语法特性，是一种实现方法。里式替换是设计原则，是一种规范。其存在的意义是用来规范我们对方法的使用，即指导我们如何正确的使用多态。</div>2019-12-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/18/47/fd/895f0c27.jpg" width="30px"><span>Cy23</span> 👍（14） 💬（0）<div>听完感觉就是，子类可以无损替换父类，就是里氏替换原则。对否</div>2019-12-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1a/9d/9c/2d5eac97.jpg" width="30px"><span>destiny</span> 👍（12） 💬（10）<div>VIP提现可透支这种情况如何不违背里氏替换原则？</div>2019-12-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/19/69/bf/58f70a2a.jpg" width="30px"><span>程序员花卷</span> 👍（11） 💬（0）<div>在继承当中，尽量不要去重写父类的方法
里氏替换原则告诉我们，继承实际上是提高了两个类的耦合性，在适当的情况下，我们可以使用组合，依赖，聚合等来解决问题！</div>2019-12-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/17/37/4e/5c3153b2.jpg" width="30px"><span>知行合一</span> 👍（9） 💬（0）<div>多态是种能力，里氏是一种约定。能力是摆在那里的，约定却不一定强制遵守，有时候可能会打破约定。需要权衡</div>2019-12-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/93/da/0e47c76e.jpg" width="30px"><span>ladidili</span> 👍（8） 💬（0）<div>多态是工具，是实在的东西。里式替换是设计思路，是虚的东西。

多态做到外壳，做到结构一致。
里式替换在结构一致的前提下还要保持底层逻辑一致。

设计模式都是用来指导开发的。里式替换指导父类更加抽象复用，子类更加贴近最初的原则。
</div>2020-02-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/5c/c2/8ffd2ad0.jpg" width="30px"><span>qqq</span> 👍（6） 💬（0）<div>遵守协议，保证一致性</div>2019-12-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/49/a5/e4c1c2d4.jpg" width="30px"><span>小文同学</span> 👍（5） 💬（0）<div>父类假如在协议上约定得非常细，方法命名中说明了实现细节，就会导致子类扩展受限，也是对里氏替换的一种限制。</div>2020-02-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/30/ff/b3e54147.jpg" width="30px"><span>雨幕下的稻田</span> 👍（5） 💬（1）<div>LSP感觉是在多态的基础上强调了协议的重要性</div>2019-12-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/17/54/d0/4e1fc664.jpg" width="30px"><span>帆大肚子</span> 👍（5） 💬（0）<div>在可拔插的设计中，保证原有代码的正确性</div>2019-12-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/18/aa/3d/c14e338e.jpg" width="30px"><span>建锋</span> 👍（4） 💬（0）<div>带着镣铐舞蹈</div>2021-03-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/17/9c/1d/34c96367.jpg" width="30px"><span>G</span> 👍（4） 💬（0）<div>我感觉里式替换对心智的负担比较大，虽然没有改写父类，但实际父类不再使用了，等同于修改了父类。这种重构让我想起了js的痛苦，逻辑都要在运行时才能知道，而且静态编译时，编译器无法帮助推断，还不如多态直接告诉编译器。</div>2019-12-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/fa/ab/0d39e745.jpg" width="30px"><span>李小四</span> 👍（4） 💬（1）<div>设计模式_17:
里氏替换：
协议(一致性)带来效率！

从多态的角度，真的可以随便写，越是与父类不同，就显得越多态。
但如果没有限制&#47;协议地多态，抽象就困难起来，在任何时候都需要考虑所有子类的实现细节，多态也就没有意义。</div>2019-12-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/0e/38/cffa4734.jpg" width="30px"><span>董瑞</span> 👍（3） 💬（0）<div>里氏替换原则存在的意义：
1. 增强父类或接口进行约定，子类进行实现的设计原则，明确父类是抽象定义，子类是具体实现的面向对象编程思想
2. 为子类设计和实现提供了明确而有用的指导思想，子类的协议实现不能超越父类的抽象定义，否则，违背约定的子类实现会导致系统可读性、可运行性会出现不符合预期的逻辑行为
3. 增加了对多态编程方法的应用指导，多态是一种编码实现的思路，设计和实现可以很宽泛，应用里氏替换原则的指导，可以设计出高质量的多态编程，从而让面向对象编程实现的程序的可读性、健壮性更好</div>2020-01-06</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/a0/6b/0a21b2b8.jpg" width="30px"><span>迷羊</span> 👍（3） 💬（0）<div>一、如何理解里氏替换原则？
1.子类对象能够替换程序中父类对象出现的任何地方，并且保证原来程序的逻辑行为不变及正确性不被破坏。（示例可查看专栏文章）
2.里氏替换原则更有指导意义的描述是：按照协议来设计。子类在设计的时候，要遵守父类的行为约定&#47;协议。父类定义了函数的行为约定，那子类可以改变函数的内部实现逻辑，但不能改变函数原有的行为约定。行为约定包括：函数声明要实现的功能；对输入、输出、异常的约定；注释中所罗列的特殊说明。同理也可以对应到接口和实现类。

二、哪些代码明显违背了LSP?
1.子类违背父类声明要实现的功能
父类中提供的sortOrdersByAmount()订单排序函数，是按照金额从小到大来给订单排序的，而子类重写这个方法之后是按照创建日期来给订单排序的。那子类的设计就违背里氏替换原则。
2.子类违背父类对输入、输出、异常的约定
父类中某个函数约定：运行出错返回null；获取数据为空时返回空集合。子类重写函数之后，运行出错返回异常，获取不到数据返回null。那子类的设计就违背里氏替换原则。
父类中某个函数约定，输入数据可以是任意整数，子类实现只允许输入数据是正整数，负数就抛出，也就是说子类对输入的数据的校验比父类更加严格，那子类的设计就违背了里氏替换原则。
父类中某个函数约定，只会抛出ArgumentNullException异常，子类的设计实现抛出了其他的异常，那子类的设计就违背了里氏替换原则。
3.子类违背父类注释中所罗列的任何特殊说明
父类中定义的 withdraw() 提现函数的注释是这么写的：“用户的提现金额不得超过账户余额……”，而子类重写 withdraw() 函数之后，针对 VIP 账号实现了透支提现的功能，也就是提现金额可以大于账户余额，那这个子类的设计也是不符合里式替换原则的。
4.判断子类的设计实现是否违背里氏替换原则，我们可以拿父类的单元测试去验证子类的代码。如果某些单元测试运行事呗，就有可能说明子类的设计实现没有完全遵守父类的约定，子类就有可能违背了里氏替换原则。

三、多态和里氏替换原则的区别
多态是面向对象编程的一大特性，也是面向对象编程语言的一种语法。它是一种代码实现的思路。而里式替换是一种设计原则，用来指导继承关系中子类该如何设计，子类的设计要保证在替换父类的时候，不改变原有程序的逻辑及不破坏原有程序的正确性。</div>2020-01-04</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/6b/5b/16a93d9d.jpg" width="30px"><span>- -</span> 👍（3） 💬（0）<div>最直接的感受是增加可读性，也就是只要理解父类的方法是做什么的，阅读子类时大原则是不变的，只是逻辑实现会有点不一样</div>2020-01-02</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/68/fe/1353168d.jpg" width="30px"><span>岁月</span> 👍（3） 💬（1）<div>我觉得, 子类的设计更多的是为了增加&quot;某个需求的实现&quot;的方式, 比如后端, 一个读写类, 子类可以分别实现多种类型数据库的读写. 比如做前端, 一个界面的渲染, 子类可以提供多种多样的渲染结果. 所以一般子类是不会去重写父类的&quot;按照数量排序&quot;这种代码, 除非真的只是为了优化性能, 但是优化性能一般是直接修改父类代码而不是新增一个高性能子类, 除非是增加一个&quot;用空间换时间&quot;这样的高性能子类, 但是这样的子类又变成了我一开头说的:  为了增加&quot;某个需求的实现&quot;.</div>2019-12-20</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/PiajxSqBRaEIeTLkHYdJ3lTe21qGTH6j6KibTfFicc8IBj5gHbIZlBruoyT02HyBbVVMGSz93PMmN9xRVib40dKlyw/132" width="30px"><span>Geek_ad9237</span> 👍（2） 💬（0）<div>里氏替换原则约束了多态行为，以防出现不符合规约的多态在运行时出现意料之外的行为，如：参数校验、返回值、业务逻辑的规约</div>2021-03-05</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1a/7f/4b/b0afc0ae.jpg" width="30px"><span>青蛙军曹ψ</span> 👍（2） 💬（0）<div>多态是一种语法，lsp 是一种设计原则。lsp依赖多态的语法机制，但lsp从功能，输入，输出，异常等方面的约定，对子类提出了跟进一步的要求。</div>2021-01-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/37/3f/a9127a73.jpg" width="30px"><span>KK</span> 👍（2） 💬（1）<div>里式替换原则，可以形象的理解为：做一个上进的乖孩子！</div>2020-04-05</li><br/>
</ul>