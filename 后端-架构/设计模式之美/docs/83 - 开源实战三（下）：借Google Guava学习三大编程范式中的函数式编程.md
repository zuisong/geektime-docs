现在主流的编程范式主要有三种，面向过程、面向对象和函数式编程。在理论部分，我们已经详细讲过前两种了。今天，我们再借机会讲讲剩下的一种，函数式编程。

函数式编程并非一个很新的东西，早在50多年前就已经出现了。近几年，函数式编程越来越被人关注，出现了很多新的函数式编程语言，比如Clojure、Scala、Erlang等。一些非函数式编程语言也加入了很多特性、语法、类库来支持函数式编程，比如Java、Python、Ruby、JavaScript等。除此之外，Google Guava也有对函数式编程的增强功能。

函数式编程因其编程的特殊性，仅在科学计算、数据处理、统计分析等领域，才能更好地发挥它的优势，所以，我个人觉得，它并不能完全替代更加通用的面向对象编程范式。但是，作为一种补充，它也有很大存在、发展和学习的意义。所以，我觉得有必要在专栏里带你一块学习一下。

话不多说，让我们正式开始今天的学习吧！

## 到底什么是函数式编程?

函数式编程的英文翻译是Functional Programming。 那到底什么是函数式编程呢？

在前面的章节中，我们讲到，面向过程、面向对象编程并没有严格的官方定义。在当时的讲解中，我也只是给出了我自己总结的定义。而且，当时给出的定义也只是对两个范式主要特性的总结，并不是很严格。实际上，函数式编程也是如此，也没有一个严格的官方定义。所以，接下来，我就从特性上来告诉你，什么是函数式编程。
<div><strong>精选留言（30）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/10/36/2c/8bd4be3a.jpg" width="30px"><span>小喵喵</span> 👍（4） 💬（3）<div>函数式编程是无状态的，它和接口的幂等性设计有什么区别呢？是不是接口的幂等性设计可以用函数式编程来实现呢？</div>2020-05-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/a0/cb/aab3b3e7.jpg" width="30px"><span>张三丰</span> 👍（1） 💬（1）<div>
如果有两个未实现方法，参数返回值不一样呢，这种就可以了吧


实际上，函数接口就是接口。不过，它也有自己特别的地方，那就是要求只包含一个未实现的方法。因为只有这样，Lambda 表达式才能明确知道匹配的是哪个接口。如果有两个未实现的方法，并且接口入参、返回值都一样，那 Java 在翻译 Lambda 表达式的时候，就不知道表达式对应哪个方法了。</div>2020-07-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/44/47/3ddb94d0.jpg" width="30px"><span>javaadu</span> 👍（63） 💬（0）<div>我对函数式编程的看法有几点
1. 在集合操作方面非常强大，集合遍历、过滤、转换、分组等等，我现在在工作中经常用
2. 函数式编程的语法对于设计模式来说是一种具体的实现方式，可能代码行数会比较少，但是思路是一样的，所以最重要的还是前面一直强调的设计原则
3. 函数式编程最大的两个特点：函数是一等公民、函数没有副作用、强调对象的不变性，对于我们在面向对象编程时处理并发问题有指导意义</div>2020-05-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/50/d7/f82ed283.jpg" width="30px"><span>辣么大</span> 👍（32） 💬（1）<div>视角不同：
FP：数据围绕操作
OOP：操作围绕数据</div>2020-05-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/fc/3b/c6b5b64f.jpg" width="30px"><span>bboy孙晨杰</span> 👍（14） 💬（0）<div>复杂的业务逻辑我一般不会用函数式编程，可读性差，也不方便debug。。。发这条评论的主要目的是庆祝自己这几个月落下的进度终于补上了，哈哈</div>2020-05-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/47/31/f35367c8.jpg" width="30px"><span>小晏子</span> 👍（14） 💬（0）<div>我觉得函数式编程并不能代替面向对象语言，并不是适合除了数学计算分析等大部分的场景，从系统设计的角度来讲，使用面向对象设计还是更亦理解的方式。
函数式编程的优点：
1. 代码量少，比如文中的例子就是最直接的展示。
2. 因为都是“无状态函数”，固定输入产生固定输出，那么单元测试和调试都很简单
3. 同样是因为无状态，所以适合并发编程，不用担心兵法安全问题。
缺点：
1. 滥用函数式编程会导致代码难以理解，比如一大型项目有大量高阶函数混着变量，开发人员随意把函数当作参数和返回值，项目会变得很难维护。
2.函数式编程会导致大量递归，算法效率太低。
</div>2020-05-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/d4/f3/129d6dfe.jpg" width="30px"><span>李二木</span> 👍（9） 💬（0）<div>最爽莫过于集合遍历。简单集合遍历 一行就可以搞定。太多for看这难受。</div>2020-05-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/17/27/ec30d30a.jpg" width="30px"><span>Jxin</span> 👍（9） 💬（0）<div>a.优缺点：
优
1.代码量少（可读性相对就高，开发成本相对就低）
2.无状态，纯函数（幂等）。（可测试性就好，对并发编程友好，对迁移serverless友好）

1.每个函数返回的都是一个新对象。（额外的资源成本）

2.设计难度高。（设计一个恰到好处的领域对象难，设计一个符合“函数编程思想”的表达式也难）。难就意味着成本，意味着不好推广普及。

缺
3.相较于面向对象对业务流程的抽象。函数表达式更像是对业务流程做重定义。 相对更不易于理解。

b.能取代面向对象吗？

不能。与文中相驳的点是，我认为函数式编程可读性其实更好（代码量少），可维护性也更好（可测试性）。但是函数式编程的代码和具体的业务流程间的映射关系，更难理解。这会导致要设计出一个完美满足业务流程的代码会比较难，需要有更多的转换和考量。而面向对象在构建这种业务模型上，只是对原业务流程做抽象，相对更好理解。其传承能力，以及跨部门达成共识的能力都远优于函数式编程。

我看好函数式编程，在无状态的计算领域，和一些高并发场景，它能发挥出很优益的价值。只是取代面向对象这种就有点过了。目前来看各有其应用场景，按需选择是挺好的方式，不必执着于谁替换谁。毕竟从结果来看，就连流程式编程，也不是面向对象能完美替代的。各有应用场景，关键在权衡。</div>2020-05-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/a0/6b/0a21b2b8.jpg" width="30px"><span>迷羊</span> 👍（9） 💬（2）<div>Java8的函数式编程太香了，点点点很爽。</div>2020-05-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/aa/49/51790edb.jpg" width="30px"><span>落尘kira</span> 👍（6） 💬（0）<div>Java的函数式编程有一定的学习成本，而且由于强调不可变性，导致必须要求外部参数为final，这种情况下就老老实实的for循环；另外就是语法糖真香，相比原生的Stream，Flux更香</div>2020-05-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/56/09/4a9d4a35.jpg" width="30px"><span>zj坚果</span> 👍（3） 💬（0）<div>这么看来，一直使用C#的linq就是函数式编程了。感觉在一些集合业务处理中非常好用，能写出可读性和简洁度都很好的代码。</div>2020-08-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/19/d9/ff/b23018a6.jpg" width="30px"><span>Heaven</span> 👍（3） 💬（0）<div>优点:降低代码编写,提高编写效率,更加抽象.如果编写的好,复用性也很不错(因为无状态)
缺点:入门门槛不低,对于一些业务复杂的逻辑,有心而无力</div>2020-05-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1a/86/56/509535da.jpg" width="30px"><span>守拙</span> 👍（2） 💬（0）<div>函数编程在Android开发领域已经是家常便饭了. 
无论是RxJava还是LiveData都应用了函数式编程思想.

在MVVM架构中, 应用函数编程可以做到层之间的解耦彻底, 链式调用很好的体现编程优雅性.

函数式编程缺点是学习成本较高. 从面向对象思想向面向函数思想的转变需要付出一定的学习精力.
如果团队开发水平参差不齐还是慎用, 可能导致你的同事无法维护你写的代码.

函数式编程另一优点是纯函数思想与不可变(Immutable)思想隔绝了恼人的局部变量, 全局变量等对流程的影响.

另最近我在codewar上刷题的时候, 发现函数编程相比传统面向对象对数据的处理确实更加简洁优雅, 相信经常刷题的同学会有相同的感受.</div>2020-05-13</li><br/><li><img src="" width="30px"><span>Geek_7e0e83</span> 👍（1） 💬（0）<div>函数式编程的优点
1.代码简洁、易读、维护性较好。因为功能相对简单。同时是无状态函数，不需要关注多线程并发和竞争共享变量的问题

缺点
1.复杂的函数式编程，可能让人不好理解。简单的还好说，因为函数式编程可能对业务逻辑的解释不太够。
2.对于复杂的业务系统，不太好表达。和面向对象编程相比，不能很好的模块化，统一组织和管理一组相关的函数和数据。

我觉得它不能代替当前主流的面向对象。但是对于和业务相关度比较低的功能或者通用组件，我觉得是比较好的一种编程范式。比如做计数，做消息通知等独立的功能，可以很好的复用函数</div>2022-11-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/63/c6/0167415c.jpg" width="30px"><span>林肯</span> 👍（1） 💬（0）<div>这是迄今为止我看到过的对函数式编程解释的最好的文章，👍</div>2022-04-01</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/70/9e/9337ca8e.jpg" width="30px"><span>jaryoung</span> 👍（1） 💬（0）<div>所谓的面向过程，面向对象，函数式的编程范式，我们都是应该根据场景进行选择的。例如，如果是大量的异步编程个人觉得使用函数式编程范式相对比较合理。面向对象的话，对于一些业务非常复杂的系统来说更加合适，面向过程本人没有做过相应经验，就不胡扯了。</div>2020-05-13</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/1F8TyS4mNfhRib2nHvLZ1azGyYQj2fjr9G1RFkOINo2Mx1JYHLN7FEU9FGg5ibictp1QAQeNUFZlTVLdb8QgkJnow/132" width="30px"><span>mooneal</span> 👍（1） 💬（0）<div>函数式编程，相对于面向对象以及面向过程，最大的优点就是无状态了，就像数学表达式，给定输入一定有一个唯一的输出映射。所以，函数式编程又可以看作是对一类数据到另一类数据的映射。</div>2020-05-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/27/02/65/ddb6460e.jpg" width="30px"><span>柯里</span> 👍（0） 💬（0）<div>是的，debug这点是真的抓马，所以我觉得是无法完全取代的</div>2023-11-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/19/fd/58/1af629c7.jpg" width="30px"><span>6点无痛早起学习的和尚</span> 👍（0） 💬（0）<div>看完文章，我理解函数式编程可以简化代码， 但是会增加代码复杂度</div>2023-10-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/7d/c8/e4727683.jpg" width="30px"><span>恬毅</span> 👍（0） 💬（0）<div>优点：代码简洁，编写快速
缺点：相对java只是语法糖，最终还是会转成对应的代码。需要运用反射，性能相对较弱</div>2022-04-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/17/55/7a/d44df1d6.jpg" width="30px"><span>freesocean</span> 👍（0） 💬（0）<div>本人使用过scala进行过flink流式计算的开发，确实如争哥所言，很简洁。但底层还是调用大量java代码，本质都是JVM系列语言，所以也是一种语法糖。如果使用时间不长，有些语法晦涩难懂，容易出错，排查问题不容易。 正如硬币的两面，不管哪种语言，都很难兼顾各种优点，在未来很长时间，我觉得都会有多种类型的语言，只是随着社会需要，有些可能暂时称为主流，但是随着时间推移，其他的又会后来者居上，这也是一个动态变化的过程，正如争哥所言，重要的不是形式本身，而是掌握解决问题的办法，语言只是工具箱里的一个工具，不好用就换一个</div>2021-11-02</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/ac/96/46b13896.jpg" width="30px"><span>williamcai</span> 👍（0） 💬（0）<div>对数据集合操作支持比较好，但是可读性比较差</div>2021-08-15</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/DYAIOgq83eotIianb3beTzsGIte6BZxlIhEwc2ryrNBGxZy8ibKbfibVJyUS8d3ZxybAdfJwHPm13ydPC4VJP7Lbw/132" width="30px"><span>taku</span> 👍（0） 💬（0）<div>滥用stream将导致代码阅读困难，对新人极度不友好，慎用~</div>2021-07-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/79/ce/89d87a1c.jpg" width="30px"><span>隔壁老李</span> 👍（0） 💬（0）<div>还是要辩证的看待函数式编程。
比如在Java项目中使用Lambda表达式后，很多现存的略显臃肿的面向对象设计模式能够用更精简的方式实现了。不仅没有使代码可读性变差，反而更加清晰明了，可读性，扩展性更高。</div>2021-06-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/22/18/fc/4f92ee4e.jpg" width="30px"><span>江南一笑</span> 👍（0） 💬（1）<div>缺点就是方法不能复用，面向对象的好处它都没有，更像是面向过程。而且对于很复杂的方法，可能用函数式编程就不容易了。</div>2021-06-16</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1d/9c/52/dc770378.jpg" width="30px"><span>yang</span> 👍（0） 💬（0）<div>老师，flink是java函数式编程的吗？</div>2021-05-14</li><br/><li><img src="" width="30px"><span>Geek_86b838</span> 👍（0） 💬（0）<div>java 1.8 之后也提供了 stream处理，请问下大家这两者有什么联系吗</div>2021-04-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1f/4f/6a/0a6b437e.jpg" width="30px"><span>有风</span> 👍（0） 💬（0）<div>函数式编程的优点：
1. 使代码变得简单，使用一个行代码即可表达一个复杂得逻辑
2. 可以延后执行，把执行得动作进行存储，最后统一触发
缺点：
1. 理解起来相对困难
2. 如果出现bug， 不方便调试

对于是否能替代面向对象？ 这个使不可能的，每一种编程方式都有优缺点，没有好与坏，对与错，只是工具而已，使用的时候面对不同的业务场景，应该择优选择，相互配合，取长补短，方式代码编写之道。
</div>2021-04-01</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/97/81/c457def1.jpg" width="30px"><span>鹤涵</span> 👍（0） 💬（0）<div>优点：
1.函数式编程使代码更简洁 Stream操作集合很强大 Optional判空不用写很多行
缺点：
1.函数式编程传入的参数必须是final禁止改变的
2.团队中不熟悉的小伙伴看很多的函数式会懵逼</div>2021-03-15</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1e/40/f7/e62bbc62.jpg" width="30px"><span>zh</span> 👍（0） 💬（0）<div>函数式编程在集合对象的操作上确实能简化代码，且可读性也不会太差。但很多人因为这一个优点就大肆宣扬，我觉得主要还是因为懒，有些人觉得只要能（自己）省事的肯定支持，这本身就缺乏工匠精神。我觉得写代码就是是为他人、为日后阅读及维护的人服务，自己只是写一遍，显示地写个函数对象能累到哪里去，但后面读的人可能会有几十甚至上百次。</div>2021-02-08</li><br/>
</ul>