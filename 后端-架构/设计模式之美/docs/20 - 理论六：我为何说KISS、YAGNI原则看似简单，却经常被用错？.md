上几节课中，我们学习了经典的SOLID原则。今天，我们讲两个设计原则：KISS原则和YAGNI原则。其中，KISS原则比较经典，耳熟能详，但YAGNI你可能没怎么听过，不过它理解起来也不难。

理解这两个原则时候，经常会有一个共同的问题，那就是，看一眼就感觉懂了，但深究的话，又有很多细节问题不是很清楚。比如，怎么理解KISS原则中“简单”两个字？什么样的代码才算“简单”？怎样的代码才算“复杂”？如何才能写出“简单”的代码？YAGNI原则跟KISS原则说的是一回事吗？

如果你还不能非常清晰地回答出上面这几个问题，那恭喜你，又得到了一次进步提高的机会。等你听完这节课，我相信你很自然就能回答上来了。话不多说，让我们带着这些问题，正式开始今天的学习吧！

## 如何理解“KISS原则”？

KISS原则的英文描述有好几个版本，比如下面这几个。

- Keep It Simple and Stupid.
- Keep It Short and Simple.
- Keep It Simple and Straightforward.

不过，仔细看你就会发现，它们要表达的意思其实差不多，翻译成中文就是：尽量保持简单。

KISS原则算是一个万金油类型的设计原则，可以应用在很多场景中。它不仅经常用来指导软件开发，还经常用来指导更加广泛的系统设计、产品设计等，比如，冰箱、建筑、iPhone手机的设计等等。不过，咱们的专栏是讲代码设计的，所以，接下来，我还是重点讲解如何在编码开发中应用这条原则。
<div><strong>精选留言（30）</strong></div><ul>
<li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/hg9Tsg2iaBeG6Q5mxiczjw1ph0OvhKziblEIiaOxg4gwQ0Dgia7Fw7pDQ0mM8AL5SJAm2Yavk1RmBJrFd9jKPBQRkOw/132" width="30px"><span>小毅</span> 👍（30） 💬（4）<div>“不要使用同事可能不懂的技术来实现代码”这一条我觉得是可以值得商榷的~ 比如在项目中引入新技术就可能会违反这一条，我觉得关键点在于这个新技术是否值得引入？新技术是否可以在团队中得到推广？ 

有时候，在code review看到不理解的新技术时，其实刚好也是可以触发讨论和学习，如果只是单纯的不去使用，很容易造成整个技术团队停滞不前。</div>2019-12-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/4e/d0/d8a5f720.jpg" width="30px"><span>Ken张云忠</span> 👍（19） 💬（1）<div>提个疑问:
文中&quot;所以，评判代码是否简单，还有一个很有效的间接方法，那就是 code review。&quot;,这里的code review有个前提该是团队成员的技术要有一定的水平,如果全是些初级人员,不按照面条式写代码就看起来费劲,这种代码评审就没意义了,所以前提是评审必须要有一定的内功修为.</div>2019-12-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/6c/c2/5a8b7468.jpg" width="30px"><span>拖鞋党副长</span> 👍（10） 💬（6）<div>老师，以java为例，什么样的写法可以被称为不建议使用的过于高级的语法呢</div>2019-12-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/24/1b/7aa4d93d.jpg" width="30px"><span>盒子</span> 👍（6） 💬（10）<div>争哥好，想请问一个问题，文中说到不要写同事可能不懂的技术实现，这该如何权衡呢；
对于 Java 8 的 lambda 表达式，我认为这样的代码会更为直观；可是由于同事都习惯使用存储过程，Java 7 的语法糖；

是否因为团队大部分人都不使用 lambda，就应该在项目中放弃使用呢？</div>2019-12-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/5a/8c/1fec5fa2.jpg" width="30px"><span>一名小学生</span> 👍（5） 💬（2）<div>打卡～
我觉得做项目中是不需要去重复造轮子的，但如果一个轮子特别大，但我只需要这个轮子很小的一部分内容，那是不是考虑借鉴它的思想去造个轮子呢？</div>2019-12-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/19/ee/e395a35e.jpg" width="30px"><span>小先生</span> 👍（5） 💬（1）<div>那请问像正则表达式这样的东西是不是就没有用武之地？</div>2019-12-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/17/85/b0/496ae224.jpg" width="30px"><span>Boogie 捷</span> 👍（3） 💬（1）<div>想请问一下老师对于使用正则匹配的看法，因为在平时的工作中还是会时不时看见，而且感觉确实可以省掉一些代码。</div>2019-12-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/1f/66/59e0647a.jpg" width="30px"><span>万历十五年</span> 👍（1） 💬（2）<div>KISS就是杀鸡别用牛刀，
YAGNI就是要少而美。</div>2020-11-12</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/DYAIOgq83erpYZalYvFGcBs7zZvYwaQAZwTLiaw0mycJ4PdYpP3VxAYkAtyIRHhjSOrOK0yESaPpgEbVQUwf6LA/132" width="30px"><span>Harlan</span> 👍（0） 💬（1）<div>KISS ：简单做   YAGNI：需要才做  
但大多数设计模式都是超前设计，也许项目初期根本用不到，那是否违背这两个原则，等需要用到的时候再重构？</div>2020-09-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/c5/5e/24cc5a72.jpg" width="30px"><span>阿狸爱JAVA</span> 👍（0） 💬（1）<div>@Test
    public void getNextsTest(){
        String s = &quot;helloWorld&quot;;
        char[] chars = s.toCharArray();
        int[] nexts = getNexts(chars, 10);
        System.out.println(nexts);
    }


    &#47;&#47; b表示模式串，m表示模式串的长度
    private static int[] getNexts(char[] b, int m) {
        int[] next = new int[m];
        next[0] = -1;
        int k = -1;
        for (int i = 1; i &lt; m; ++i) {
            while (k != -1 &amp;&amp; b[k + 1] != b[i]) {
                k = next[k];
            }
            if (b[k + 1] == b[i]) {
                ++k;
            }
            next[i] = k;
        }
        return next;
    }
这个函数的意义是啥，为啥最后输出的结果是{-1,-1,-1,-1,-1,-1,-1,-1,-1,-1}</div>2020-07-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/71/05/db554eba.jpg" width="30px"><span>👽</span> 👍（0） 💬（1）<div>奇技淫巧，问一下  Lambda，和Stream  以及  int ... a; 这些  哪个算是尽量别用的奇技淫巧呢？ 为什么团队里，有的人把Stream+Lambda 一行写完的代码，分了五六行去写。谁是对的？</div>2019-12-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/50/d7/f82ed283.jpg" width="30px"><span>辣么大</span> 👍（320） 💬（17）<div>很好奇这三个方法运行效率的高低。测了一下争哥给的代码的执行效率，结果正如争哥文章说，第三个是最快的。
方法一（正则）&lt; 方法二 &lt; 方法三

正则就真的这么不堪么？效率如此之低？其实不然。

Java中正则的最佳实践是：
用于校验和匹配的正则表达式使用时需要预先compile，在类中写做静态变量（经常会重用），这样可以提高效率。Pattern.compile(IP_REGEXP)

优化正则后的效率如何呢？
方法一（正则）&lt; 方法二 &lt; 方法一（正则改进后）&lt; 方法三

测试参数设置：每个方法执行100万次。
实验结果：
方法一：2.057s
方法一优化：0.296s 提前编译正则
方法二：0.622s
方法三：0.019s
有兴趣的小伙伴看看代码，欢迎一起讨论！https:&#47;&#47;github.com&#47;gdhucoder&#47;Algorithms4&#47;blob&#47;master&#47;designpattern&#47;u20&#47;TestPerformance.java

参考：
https:&#47;&#47;stackoverflow.com&#47;questions&#47;1720191&#47;java-util-regex-importance-of-pattern-compile</div>2019-12-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/f2/aa/32fc0d54.jpg" width="30px"><span>失火的夏天</span> 👍（233） 💬（10）<div>开发中的重复造轮子，这东西怎么说呢。我认为这句话是对公司来说的，但是对自己来说，重复造轮子是有必要的。就好比之前的数据结构和算法，那也是所有轮子都有啊，为什么还要自己写响应代码。这个问题在另一个专栏都说烂了，这里也不再赘述了。

光说不练假把式，轮子用不用的好，自己了解的深入才知道。我们读书的时候，用数学定理去解题，也是在一些已知条件下才能用这个定理。不能上来就套定理，而是要分析是否满足使用情况。只有吃透定义和原理，才能更好的使用轮子。

开发中也一样，我们要排查各种各样的问题，如果轮子内部出了问题，对轮子原理实现都不了解的，怎么排查问题。怎么知道用那种轮子是最好的呢。而且还会存在改造轮子的情况，轮子不满足我们特定的需求，那也是吃透了才能改的动。

总之，轮子这东西，对公司来说，不要重复，对自己来说，要多去理解，多动手。总不希望自己就是个调包侠吧</div>2019-12-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/fa/ab/0d39e745.jpg" width="30px"><span>李小四</span> 👍（55） 💬（4）<div>设计模式_19
今天的内容有一些哲学味道，让我联想到奥卡姆剃刀原理：
如无必要，勿增实体。

用同事不懂的技术，增加了整个团队的理解成本；重复造轮子和过度优化，大多数情况下带来的便利小于增加的成本；
不要写炫技的代码，就像杜峰(CBA广东队教练)说的：“如果没有目的，就不要运球。(因为运球就可能丢球)”，降低出错的概率是一个数学问题，它能够真实得提高软件质量。

回到作业，同上：
只有必须造轮子时，才要造轮子。
那什么又是必须呢？
- Vim如果不用KMP，恐怕就没有人用了。
- MySql的性能(即将)已经不能满足阿里的业务量
- 微信作为国民应用，需要解决各种弱网络下尽可能收发消息。
...</div>2019-12-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/4e/d0/d8a5f720.jpg" width="30px"><span>Ken张云忠</span> 👍（29） 💬（0）<div>你怎么看待在开发中重复造轮子这件事情？
轮子:供上层业务应用使用的基础组件.
造轮子:设计并实现基础组件.
重复造轮子:重新设计实现一套新的组件.
开发中重复造轮子:
对于个人可以有深度度地提升对业务与技术认知的理解,还可以提升设计与动手能力,由于掌握了更多细节的知识,以后对于这类问题的排查定位及处理是有益处的.
对于技术团队,重复造出的轮子多了日后就需要有更多的人手和精力维护各个轮子,使轮子的维护成本变高;在使用方面,团队的每个成员为了能够正确的使用轮子就需要花费精力去熟悉各个轮子的特征.
什么时候要重复造轮子？
新的业务场景中原来的轮子不再合用,并且改造的成本高于重新建造的成本.比如原有业务量不大对于性能要求一般时,旧轮子足够满足;但随着业务的迅猛增长,对于性能提出明确苛刻的要求,就可以考虑重新建造新轮子了.
什么时候应该使用现成的工具类库、开源框架？
业务发展的初中期阶段时应该使用.这个阶段业务需求一般比较通用且对性能要求也不高,这时的业务与技术的特点就是要快,快速响应业务占领市场.
但发展到一定规模,性能成为了制约业务发展的瓶颈,拿来主义已经不能满足业务的更高要求了,就必须要动手建造适合自身业务需求的特定轮子.</div>2019-12-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/85/5d/ec94b66d.jpg" width="30px"><span>程序袁帅</span> 👍（21） 💬（4）<div>可能大家会说KISS、YAGNI这些原则听起来容易，做起来难。其实我认为不是做起来难，而是难在为什么要做和为什么不做。回到写代码这份职业来说，我觉出三个不同的问题：
1. 你为什么要写可用代码代码？ -- 赢得公司的信任，让自己能够活下来
2. 你为什么要写简洁可用的代码？   --  解放自己的生产力，创造更多价值，升职加薪
3. 你为什么要写简洁可用，并影响其他人？ -- 赢得别人尊重，获得职业成就感

我觉得程序员首先要思考上面三个事情为什么要做，而且要回答上这些问题，需要自己持续精进，比如提升编码Sense、设计思维、提升系统思考能力。


在探索上面三个问题的道路上，很多开发人员可能有如下内心小九九：

1. “我要用炫酷的方式Show技能。看，正则，你看得懂吗，哈哈。小样”
2. “我要用最少的代码写出这个而功能。看，我的代码就是比你少”
3. “我要用极致的性能来写这个功能。来，测一测，谁的用时最短，我开始用了快速排序法的”
4. “我要用上5个设计模式。你瞧瞧，这里有5个设计模式的精髓，健壮无比的代码”
5. ....


以上这些内心小九九是我们要去尽量克制的，尽量少做、甚至不做，而为什么不做这些事情，去思考这个问题的答案更重要。


道理可能都懂，缺的是刻意练习，推荐一些实操落的方法论和实践：
1. 简单设计（4原则和优先级）
2. 测试驱动开发（Tasking + TDD）
3. 重构（作者后面会提到）</div>2020-02-05</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/62/bb/323a3133.jpg" width="30px"><span>下雨天</span> 👍（15） 💬（0）<div>一.什么时候要重复造轮子？
1. 想学习轮子原理(有轮子但是不意味着你不要了解其原理)
2. 现有轮子不满足性能需求(轮子一般会考虑大而全的容错处理和前置判断，这些对性能都有损耗)
3. 小而简的场景(比如设计一个sdk,最好不宜过大，里面轮子太多不易三方集成)
4.定制化需求

二.什么时候应该使用现成的工具类库、开源框架？
1.第一条中提到的反面情况
2. 敏捷开发，快速迭代，需求急的场景
3. 轮子比自己写的好，BUG少，设计好
4. KISS原则</div>2019-12-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/17/65/a8/6431f8b0.jpg" width="30px"><span>Kang</span> 👍（10） 💬（1）<div>曾经有个外包同学，为了体现自己的技术能力，所有的数学计算都是写的位运算，气的我把血吐了他一脸，让他改！！！</div>2020-09-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/97/81/c457def1.jpg" width="30px"><span>鹤涵</span> 👍（6） 💬（0）<div>重复造轮子是加深理解的最好方式</div>2020-08-16</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/26/eb/d7/90391376.jpg" width="30px"><span>ifelse</span> 👍（5） 💬（0）<div>我可以不造，但是不能不会。</div>2021-06-04</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/fc/3b/c6b5b64f.jpg" width="30px"><span>bboy孙晨杰</span> 👍（4） 💬（1）<div>哈哈，联想到英雄联盟这个游戏，kiss就像盖伦的大宝剑，专制一切花里胡哨，用最简单的操作解决问题，而与之相反就是就是花里胡哨，一顿乱秀猛如虎，一看战绩0-5</div>2019-12-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/a5/ee/6bbac848.jpg" width="30px"><span>再见孙悟空</span> 👍（4） 💬（1）<div>很早就知道 kiss 原则了，以前的理解是代码行数少，逻辑简单，不要过度设计这样就符合 kiss 原则。虽然知道这个原则，但是却没有好好在实践中注意到，导致写的代码有时候晦涩难懂，有时候层层调用，跟踪起来很繁琐。看完今天的文章，理解更深了，代码不仅是给自己看的，也是给同事看的，并且尽量不自己造轮子，使用大家普遍知道的技术或方法会比炫技好很多。
至于另一个原则，你不需要它这个实际上做的还是不错的。</div>2019-12-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/82/3d/356fc3d6.jpg" width="30px"><span>忆水寒</span> 👍（3） 💬（0）<div>1、你怎么看待在开发中重复造轮子这件事情？
答：公司其实不会重复造轮子的，但是某些组件还是会自己定制的，主要考虑的是维护性。但是开源的框架还是可以看看和学习一下优秀的设计。如果什么都引入开源框架，万一有人不懂这个框架，维护起来就很困难了。通过自己定制一些框架，企业还可以培养一批优秀的人才。
2、什么时候要重复造轮子？
有特殊的应用场景的时候，应该考虑重复造轮子。这个轮子可大可小。也可以说是自己某个模块抽出来的工具类之类的。有时候造一些小轮子是为了避免引入更多的依赖框架。
3、什么时候应该使用现成的工具类库、开源框架？
通用的场景就应该使用成熟的框架和工具类。比如，做web开发，spring或spring boot肯定会用的，自己造这个轮子就太浪费时间和人力了。还有就是看企业规模，小公司没能力还是用成熟的框架更快的开发吧。毕竟生存下去才是第一位的。</div>2020-03-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/3b/ac/40807e85.jpg" width="30px"><span>无所从来</span> 👍（3） 💬（0）<div>KISS用于设计之初的理念，是规划；YAGNI用于设计之后的优化，是减法。</div>2020-01-02</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/79/f4/d85e7e58.jpg" width="30px"><span>看山</span> 👍（3） 💬（3）<div>“不要使用同事可能不懂的技术来实现代码。比如前面例子中的正则表达式，还有一些编程语言中过于高级的语法等。”
针对这条建议，不是很赞同。正则表达式是每个开发应该掌握的，对于初级来说比较有难度，但这种好用的就该主动去学；在jdk8刚出来的时候，lambda表达式是高级用法，到这个语法在很多其他语言中已经成熟，那就该在编码过程中实践，否则就会被甩在车轮后面。
我认为我们要保持代码的简洁高效、通俗易懂，但也要充分利用语言特性。</div>2019-12-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/49/d8/71860550.jpg" width="30px"><span>ca01ei</span> 👍（3） 💬（0）<div>要不这样吧，如果编程语言里有个地方你弄不明白，而正好又有个人用了这个功能，那就开枪把他打死。这比学习新特性要容易些，然后过不了多久，那些活下来的程序员就会开始用0.9.6版的Python，而且他们只需要使用这个版本中易于理解的那一小部分就好了（眨眼）。￼
——Tim Peters 传奇的核心开发者，“Python之禅”作者</div>2019-12-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/18/4f/c9/9f51fd27.jpg" width="30px"><span>编程界的小学生</span> 👍（3） 💬（3）<div>我觉得如果开源类库完全能满足需求的话，那完全没必要造轮子，如果对性能有要求，比如类库太复杂，想要简单高效的，那可以造个轮子，比如我认为shiro也是spring security的轮子，他简化了很多东西，小巧灵活。还有就是觉得类库能满足需求但是相对于当前需求来讲不够可扩展，那也可以采取类库思想造一个全新的轮子来用。</div>2019-12-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/ca/c7/00e544c2.jpg" width="30px"><span>黄林晴</span> 👍（2） 💬（0）<div>对工作上重复造轮子，没有必要，因为讲究效率问题，别人不会管你实现的功能是复制粘贴的，还是自己实现的，能正常使用就ok，对于自己来说也没必要盲目造轮子，不要造大轮子，除非你觉得你造的轮子可以碾压现有的，造一些小轮子，使用别的轮子的思想和设计还是有些用处的。</div>2019-12-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/18/bb/9299fab1.jpg" width="30px"><span>Null</span> 👍（1） 💬（0）<div>不要使用同事可能不懂的技术来实现代码，大有从使用正则这件事儿片面引导了。比如swift是现行或者将来要使用的iOS开发语言，为了更好的跟进官网进度，使用swift写新业务，但是同事不会，我就不写了吗？显然不是。所以我觉得这句话应该修改下，不要不常见、非大众，有更好解决方案的技术。而不是管同事的事儿，技术好，好比设计模式，很多人就不懂啊，就不会用啊，我一样要用。“三观正确”的事儿坚持还是要做的。</div>2022-11-02</li><br/><li><img src="" width="30px"><span>Geek_dc3cf1</span> 👍（1） 💬（0）<div>“不要使用同事可能不懂的技术 ”：同事不懂不是因为她们菜吗</div>2022-10-10</li><br/>
</ul>