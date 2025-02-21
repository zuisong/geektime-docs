你好，我是蔡元楠。

今天我要与你分享的话题是“站在Google的肩膀上学习Beam编程模型”。

在上一讲中，我带你一起领略了Apache Beam的完整诞生历史。通过上一讲，你应该对于Apache Beam在大规模数据处理中能够带来的便利有了一定的了解。

而在这一讲中，让我们一起来学习Apache Beam的编程模型，帮助你打下良好的基础以便应对接下来的Beam实战篇。希望你在以后遇到不同的数据处理问题时，可以有着Beam所提倡的思考模式。

现在让我们一起进入Beam的世界吧。

## 为什么要先学习Beam的编程模型？

可能你会有疑问，很多人学习一项新技术的时候，都是从学习SDK的使用入手，为什么我们不同样的从SDK入手，而是要先学习Beam的编程模型呢？

我的答案有两点。

第一，Apache Beam和其他开源项目不太一样，它并不是一个数据处理平台，本身也无法对数据进行处理。Beam所提供的是一个统一的编程模型思想，而我们可以通过这个统一出来的接口来编写符合自己需求的处理逻辑，这个处理逻辑将会被转化成为底层运行引擎相应的API去运行。

第二，学习Apache Beam的时候，如果只学习SDK的使用，可能你不一定能明白这些统一出来的SDK设计背后的含义，而这些设计的思想又恰恰是涵盖了解决数据处理世界中我们所能遇见的问题。我认为将所有的SDK都介绍一遍是不现实的。SDK会变，但它背后的原理却却不会改变，只有当我们深入了解了整个设计原理后，遇到各种应用场景时，才能处理得更加得心应手。
<div><strong>精选留言（13）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/10/4d/49/28e73b9c.jpg" width="30px"><span>明翼</span> 👍（18） 💬（1）<div>老师你好，看了介绍beam是集成流处理和批量处理模型形成一套统一的模型，而且可以跑在多个runner上，我在想如果有很好的兼容性那可能会牺牲些性能，beam的程序是否可以和原生的runner上写的代码一样的性能那？如果我下层绑定了runner，我何必再用beam？beam的适用场景是不是很窄了那？</div>2019-06-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/5f/e9/95ef44f3.jpg" width="30px"><span>常超</span> 👍（15） 💬（2）<div>终于进入beam了，讲得这些宏观概念以及举的例子都很清晰，很有收获。
从课表上看后面有关beam的还有13讲，感觉前面的铺垫太长，为了在这个专栏上维持数据处理的完整性，好多框架都拿出来泛泛谈一下，熟悉的人不需要，不熟悉的人也只能了解个大概皮毛，到不了能实战的程度。希望老师未来能出个针对某一个具体框架的深度学习课程。</div>2019-06-12</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTLdWHFCr66TzHS2CpCkiaRaDIk3tU5sKPry16Q7ic0mZZdy8LOCYc38wOmyv5RZico7icBVeaPX8X2jcw/132" width="30px"><span>JohnT3e</span> 👍（6） 💬（2）<div>是否可以把Beam应该可以称为大数据处理的高级语言。虽然直接使用高级语言编写会产生一定的性能损耗，但屏蔽了各个底层平台的差异，提供了统一的逻辑抽象，提高了开发效率。如果一个场景既需要离线处理，也需要实时处理，那么就需要两种不同的计算平台（比如采用lambda架构）。此时采用beam可以解决同样逻辑多个平台开发的问题吧</div>2019-06-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/98/3c/47d70fdc.jpg" width="30px"><span>ditiki</span> 👍（5） 💬（1）<div>这章在 Streaming 101&#47;102 中有更多讲解，可以作为reference 
https:&#47;&#47;www.oreilly.com&#47;ideas&#47;the-world-beyond-batch-streaming-102</div>2019-06-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/30/e9/13fb8d51.jpg" width="30px"><span>毛毛</span> 👍（3） 💬（1）<div>基于元素个数触发的窗口计算，统计交易数据，假如有很多个元素计数都为1，实际也没触发统计，这对当前时间窗口的统计就比实际差很多了，这种情况要怎么解决或者说适合什么场景呢，老师！</div>2019-07-07</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/17/1a/f9/180f347a.jpg" width="30px"><span>朱同学</span> 👍（3） 💬（1）<div>我们开始也是被底层开发困扰，每个指标都要写代码，然后发现了kylin  ,基本只关注模型和纬度了 </div>2019-06-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/37/d0/26975fba.jpg" width="30px"><span>西南偏北</span> 👍（1） 💬（1）<div>还是那个理念：让工程师更专注与业务逻辑，而不要把精力和时间放到底层的实现上去！
还是有利有弊吧！</div>2019-06-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/cf/76/9e413c61.jpg" width="30px"><span>Bin滨</span> 👍（0） 💬（1）<div>有针对kafka Stream 的支持吗? Kafka Stream 本身也提供对 WWWH的概念的支持。 </div>2019-06-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/2c/e7/3c0eba8b.jpg" width="30px"><span>wuhulala</span> 👍（1） 💬（0）<div>在做我们的统一etl工具开发的时候，就参考beam的思想做了设计。我们的etl工具也是只涉及到模型层，实际的runner由informatica、kettle、大数据平台等，一份etl代码 实现多处运行 。但后面也由于一些工作调动 这些东西也一直没有完成。遗憾</div>2020-04-02</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/78/eb/c2fd27f6.jpg" width="30px"><span>RAY_CCW😝😝😝</span> 👍（0） 💬（0）<div>想请教一个问题，如果我要用Beam去出一个报表的情况下，那么怎么去控制数据权限呢？
</div>2022-02-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/47/00/3202bdf0.jpg" width="30px"><span>piboye</span> 👍（0） 💬（0）<div>水位线没具体讲哦老师</div>2021-12-28</li><br/><li><img src="" width="30px"><span>Geek_7cc111</span> 👍（0） 💬（0）<div>老师，提个问题。
在wwwh的讲解中，When in processing time they are materialized? 我们可以通过使用水印和触发器配合触发计算。水印是用来表示与数据事件时间相关联的输入完整性的概念
但是你举的例子，我没有看到“水印”的影子。也就是说，从你的例子中，我怎么理解 “我们可以通过使用水印和触发器配合触发计算” 这句话
</div>2020-03-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/f3/44/e10d87c7.jpg" width="30px"><span>王治澎</span> 👍（0） 💬（0）<div>在业务系统中， 有非常复杂的业务逻辑计算， Beam 编程模型的引入会达到什么效果呢？</div>2019-11-09</li><br/>
</ul>