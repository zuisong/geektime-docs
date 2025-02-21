今天我和你聊聊 Java 语言，这也是我使用最久最熟悉的编程语言之一。

读博士的时候我做过两个领域。刚刚进入莱斯大学的时候进的是程序语言设计组。组里当时有两个教授，分别做两个领域。

一个是瓦利德·塔哈（ Walid Taha ），主要研究领域是类型系统和嵌入式系统的程序语言设计。另一个是罗伯特·卡特赖特（ Robert Cartwright），他喜欢大家叫他 Corky，主要研究的是 Java 的理论和实现。

Corky 教授的研究项目中，有一个叫做 DrJava 的项目。DrJava 是一个轻量级的 Java 开发环境。主要是给在校学生用的，它提供了一个简单直观的交互界面，可以实现类似 Shell 的交互式 Java 代码执行方式。DrJava 在美国大学里有很多人使用，目前已经超过两百万的下载量。

Corky 是个典型的美国教授，与生俱来的花白卷发，清癯的脸庞上一双眼睛炯炯有神，高挺的鼻梁。他常年都是和学生一样的打扮：T恤牛仔裤加运动鞋。出入的时候，背上总是背着一个蓝灰色的电脑包。

当他不谈学术的时候，你会觉得他有着与年龄不相称的单纯和童真。他会和一群学生一起吃系里免费的披萨和点心，也会和其他教授一起站在系里走廊上聊天和哈哈大笑；然而一旦你和他讨论起 Java，他就变得滔滔不绝，整个人散发出特别的魅力。他对 Java 的理解十分深入，我每次和他对话都颇有收益。

虽然我的导师是瓦利德（Walid），但同在一个语言组，平时的研讨班都在一起，我也就有了很多的机会和 Corky 一起讨论各种程序语言的特性和实现。也就是在那个时候，我对 Java 语言有了比较多深层次的了解。

## 我和 Java 语言的开发者

我的硕士论文是独立实现的一个程序设计语言，包括它的解释编译和用户界面。这个语言主要用于机器人系统的嵌入式编程和仿真，曾经在一家石油公司的井下控制系统开发中被使用。不过因为我导师的离开和种种其他原因，我博士生涯的后三年转了另一个导师做生物信息学的数据分析和建模。

因为有程序设计语言的研究经验，博士毕业找工作的时候，也投了份简历在 Oracle 的 Java 语言开发组。也因为有这样相应的背景，我很顺利地拿到了Java核心类库 （Java Core Library） 开发小组的 Onsite 面试机会。

我去面试的时候应该是 2012 年底，当时面试的那个小组一共好像只有七八个人的样子。Oracle 的面试大部分是白板和聊天，和现在比较主流的面试，上机做题并无 Bug 运行的体验很不相同。我介绍了自己的硕士毕业设计，然后就谈起 Java 新的库或版本可能会增加哪些支持。

2012 年底的时候，Scala 和 Clojure 刚刚火起来不太久，Java 还没有对Lambda 的支持。而当时整个Java团队也正在考虑这件事。话题牵扯到了 Lambda 的实现，正好是我非常熟悉的话题，因为我的导师瓦利德（ Walid ）主要的研究领域就是函数式语言，而对 Lambda 的实现，也是函数式编程语言的核心。

具体的讨论细节我已经不记得了，不过有两点感触颇深：一是他们对于选择哪些函数进核心库（ Core Libarary ）非常谨慎。Java 早期是很轻量级的，后来的版本功能越来越强大，但是语言本身也越来越沉重，这也是很多人喜欢 Scala 的原因。

二是实现函数库的语言开发者对每个函数的精度和运行时间的要求到了令人发指的程度，听说他们有时候读无数的论文，看无数的实现，作大量的比较，就只是为了敲定到底应该在最终的函数中使用哪一种实现方式。

比如浮点数是有舍入误差（ Rounding Error ）的，那么一个数值计算中先算哪一步、后算哪一步带来结果都可能是不同的；而实现中的考虑，往往为了小数点后面十几位以后的一个 1，组里也要反复斟酌很久。
<div><strong>精选留言（15）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/0f/55/e6/87197b10.jpg" width="30px"><span>GeekAmI</span> 👍（18） 💬（1）<div>Java看了两周，找了一份工作，以战养兵。期待安姐开设Java系列的技术高阶课程！</div>2018-01-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/43/bf/9a982bc1.jpg" width="30px"><span>子悠</span> 👍（9） 💬（0）<div>每过段时间看自己以前写的代码都有一种，“我去，这代码哪个傻瓜写的，肯定不是我”的感觉</div>2018-01-12</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTJvJDBrTrESPwZhQkoibT0NYdasIia7ZOCbU0oKgY2icrE9flAbzMsI7CZoiblTpqukMEzTfzrQU0ibPBg/132" width="30px"><span>白白白小白</span> 👍（5） 💬（0）<div>虽然我是php开发，但是我还是认真的读完就！</div>2018-05-07</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/f3/81/42e29d40.jpg" width="30px"><span>有福</span> 👍（5） 💬（0）<div>为了这个文章直接订阅了专栏</div>2018-01-15</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/5a/75/4e0d7419.jpg" width="30px"><span>飓风</span> 👍（4） 💬（0）<div>工具文件夹可能叫util比较合适，个人偏见。</div>2018-01-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/75/aa/21275b9d.jpg" width="30px"><span>闫飞</span> 👍（3） 💬（0）<div>第一个例子好像有点不对啊，f返回的是一个匿名函数，所以f(10)得到的是个函数对象，必需要再加一层括号才能求值，得到调用值。

Java用接口的概念和多态来封装函数对象，和C++某些方面有异曲同工之处，但是其stream api和optional类型提供了极好的monad实现。

c++的类型系统对函数式支持更加严格一些，尤其是fp和自动类型推断以及泛型元编程的支持水乳交融，非常巧妙，不像Java尝试用OO来搞定一切。</div>2018-01-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/80/04/e6989d2a.jpg" width="30px"><span>极客时间攻城狮。</span> 👍（1） 💬（1）<div>吉利</div>2018-01-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/67/bb/abb7bfe3.jpg" width="30px"><span>王建Tyrion</span> 👍（1） 💬（0）<div>上个月刚刚把代码重构一番，按照标准的文件夹规范，上个版本真是自己能把自己看晕(=_=)</div>2018-01-12</li><br/><li><img src="" width="30px"><span>何慧成</span> 👍（0） 💬（0）<div>组织级的规范很重要</div>2020-08-30</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/8e/e0/847348b1.jpg" width="30px"><span>爱学习的大叔</span> 👍（0） 💬（0）<div>我们在开发时基本只停留在语言表面上，只是手到擒来的拿来用，原来在背后有这么多的故事。学习了.</div>2019-12-05</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/4d/7a/106c3745.jpg" width="30px"><span>mikejiang</span> 👍（0） 💬（0）<div>java语言用得不多，没想到居然也支持Lamda了</div>2019-11-25</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/44/28/948cab86.jpg" width="30px"><span>JasonYe</span> 👍（0） 💬（0）<div>Scala语言怎样</div>2019-09-04</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/a4/49/1c8598d1.jpg" width="30px"><span>军舰</span> 👍（0） 💬（0）<div>实现闭包大体有两种方式。能不能用源代码展示一下？</div>2018-10-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/59/0b/fb876077.jpg" width="30px"><span>michael</span> 👍（0） 💬（0）<div>参与设计一门语言再学习应用语言，真是得心应手</div>2018-09-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/1a/f3/41d5ba7d.jpg" width="30px"><span>iLeGeND</span> 👍（0） 💬（0）<div>为什么留言不显示呢</div>2018-05-21</li><br/>
</ul>