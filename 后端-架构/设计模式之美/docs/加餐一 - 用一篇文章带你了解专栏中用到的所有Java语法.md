尽管说设计模式跟编程语言没有直接关系，但是，我们也无法完全脱离代码来讲设计模式。我本人熟悉的是Java语言，所以专栏中的代码示例我都是用Java语言来写的。考虑到有些同学并不熟悉Java语言，我今天用一篇文章介绍一下专栏中用到的Java语法。

如果你有一定的编程基础，熟悉一门编程语言，结合我今天讲的Java语法知识，那看懂专栏中的代码基本不成问题。

如果你熟悉的是C/C++、C#、PHP，那几乎不用费多大力气，就能看懂Java代码。我当时从C++转到Java，也只看了一天的书，基本语法就全部掌握了。

如果你熟悉的是Python、Go、Ruby、JavaScript，这些语言的语法可能跟Java的区别稍微有些大，但是，通过这篇文章，做到能看懂也不是难事儿。

好了，现在，就让我们一块儿看下，专栏中用到的所有Java语言的语法。

## Hello World

我们先来看一下，Java语言的Hello World代码如何编写。

在Java中，所有的代码都必须写在类里面，所以，我们定义一个HelloWorld类。main()函数是程序执行的入口。main()函数中调用了Java开发包JDK提供的打印函数System.out.println()来打印hello world字符串。除此之外，Java中有两种代码注释方式，第一种是“//注释…”双斜杠，表示后面的字符串都是注释，第二种是“/\*注释…\*/”，表示中间的内容都是注释。
<div><strong>精选留言（30）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/0f/88/c8/6af6d27e.jpg" width="30px"><span>Y024</span> 👍（9） 💬（1）<div>Day013 加餐一
勘误：第二种是“&#47;注释…&#47;”
应为：第二种是“&#47;* 注释…*&#47;”</div>2019-11-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/0c/c6/934e3e4f.jpg" width="30px"><span>偶然~zZ</span> 👍（3） 💬（2）<div>啥时候出一篇  python所有语法啊</div>2019-11-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/18/03/ef0efcc4.jpg" width="30px"><span>EidLeung</span> 👍（3） 💬（1）<div>木有讲泛型🌚</div>2019-11-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/77/6f/454951d2.jpg" width="30px"><span>Lyre</span> 👍（2） 💬（2）<div>这篇有点混😂</div>2019-11-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/97/0b/a943bcb3.jpg" width="30px"><span>zhou</span> 👍（1） 💬（1）<div>C++转java麻烦问下作者看的那本书，推荐推荐</div>2019-11-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/50/d7/f82ed283.jpg" width="30px"><span>辣么大</span> 👍（106） 💬（13）<div>Java用的时间最长，大概4-5年，不敢说自己“熟练”掌握了。最近反而觉得不懂的更多了。我没有抓入Java8不放，而是跟着Java的发展，开始学习Java11和Java13的新特性，紧跟语言的变化，并学习虚拟机和并发编程的相关知识。

我觉得熟练使用某种编程语言，在技术能力评价中占比起码50%。因为“熟练”是衡量一名程序员对一门语言掌握程度的重要指标。说明他\她不但会使用该语言，而且知道语言的细节，优缺点、适用场合等等。从入门到掌握、精通一门语言或者技能，是要花大功夫的，能看出一个人是否能把一件事（可能很枯燥）做到极致，有是否钻研的精神。这种能力是很多人不具备的。

国内招人还是很实际的，来了就能干活。学习能力是很虚的一个东西，嘴上说说没啥用。熟练掌握一门语言，才能看出你有学习能力。</div>2019-11-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/0d/08/2f825f69.jpg" width="30px"><span>丁源(156*****518)</span> 👍（62） 💬（5）<div>常人嗑语言，高手玩算法，大师谈模式，神人给定律。计算机，数学，哲学，神学。对抽象的理解越发深刻，构建高层次，高维度的模型就越稳定，由此意识形态泛化出的物质形态也会跟着越接近现实。</div>2019-11-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/18/4f/c9/9f51fd27.jpg" width="30px"><span>编程界的小学生</span> 👍（29） 💬（2）<div>原谅我这篇文章三十秒就看完了，因为我是JAVA
1.用了多久我也不确定，但是学习方法是有的，首先看视频，资料，动手敲，晚上睡觉前在脑海里回顾一下学了什么，明天在动手敲一遍昨天学的内容，最后用自己的语言将其组织成一篇属于自己的文章。
2.熟练需要看成都，就比如很多人都说看源码感觉没用，看了就忘，也不知道能干嘛。我认为看源码首先能隐形锻炼你写代码的风格，学习里面的架构设计思想，且遇到奇葩问题你能知道怎么debug进去找问题，这些才是最主要的。我个人认为，如果没有看懂看清他里面的设计思想和核心源码，那我觉得你只是掌握了他的api，而不是熟悉。</div>2019-11-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/fa/ab/0d39e745.jpg" width="30px"><span>李小四</span> 👍（20） 💬（0）<div>从第一次接触Java，到得心应手，大概花了两年时间。这个周期让我理解了学习的非线性。
大一开始学习C语言，学的似懂非懂，做了课程设计就放下了，发大二开始学Java，同样似懂非懂。大三开始接触Android开发，用到了Java，才发现自己Java知识不足，于是花时间重学了Java，过程中发现有些东西不理解，又穿插着把C需要的指针内存啃了几遍，大三结束的时候，Java才算熟练了，距离刚开始学习过去将近两年，中途无数次被打击，也放弃了很多次，因为每个字都认识，但看一次两次根本不理解，直到某一天你发出了一声恍然大悟的“哦～～～”，这种非线性的特点应该是很多人最终放弃的原因吧，一次次被打击，多次尝试没有正反馈，出于自我保护心理，说服自己放弃了。</div>2019-11-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/ec/b1/d790b927.jpg" width="30px"><span>摸爬滚打三十年</span> 👍（18） 💬（0）<div>因为看老师的专栏太入迷，坐过了站</div>2019-11-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/a4/06/cf6b6d0f.jpg" width="30px"><span>Jason</span> 👍（12） 💬（0）<div>大学开始主要了两年Java，然后毕业找到深度学习的岗位，主要用python和c++。

有java基础，上手就很快，学习python就跟着GitHub上一个python 100 days那个项目学了一个礼拜，但没看web相关的，主要是看机器学习相关的一些库怎么用。反正现在能用tensorflow调调参。

然后两周前又转回Java，感受就是语言层面的没设计模式，数据结构与算法重要，更没分析问题，解决问题的能力重要。</div>2019-11-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/87/6b/0b6cd39a.jpg" width="30px"><span>朱月俊</span> 👍（8） 💬（1）<div>我使用过的语言包括c,c++,java,python,go。
我是按照使用的先后顺序列出的。
念书期间用c&#47;c++；后来第一份实习写了2个月的java,去重构一个项目，当时没人教，直接看别人的老代码，不会就网络查；再之后就是第一份正式工作，涉及到分布式存储，底层实现用了c++,客户端调用还是使用了python，python也是现学现卖；再后来，去搞区块链，当时那个区块链项目主要是go语言，我还没看go语言就给我派任务，我就直接用go写了，go的语法学习都是看看别人已经写好的代码，并且这完全不影响我开发的进度和质量，我的代码提交量还是number one。
最近，又用go去搞搜索引擎，还是比较得心应手吧。
总之，我同意争哥的说法，编程只是一个赚钱的手段，语言只是实现这个手段的一个工具，不重要。</div>2020-07-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/b8/dd/37726c34.jpg" width="30px"><span>小马哥</span> 👍（6） 💬（0）<div>大学课程中学习了C，工作中自学并使用JAVA，主要用于web和大数据开发，JAVA不仅仅是一门语言，还是一个技术体系，包括了后来的很多技术框架，学习JAVA语言如果有其他语言基础是很快的，精通后面的一些常用框架就需要一些设计模式的积累。所以还是学习能力最重要：学习，操练，总结，分享，这个路线是我认为很快捷的学习方法。最后学习的东西越多，越容易融会贯通，后来使用Python做推荐系统，我们几个JAVA开发人员，基本是用一个小时过了一遍Python语法，就开工了</div>2019-11-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/2f/7a/ab6c811c.jpg" width="30px"><span>相逢是缘</span> 👍（6） 💬（1）<div>非计算机专业，在学校就学习了C语言，在工作中也一直使用C。后来自己看了C++，JAVA。学习一门语言最开始就是一些基本语法和数据结构，了解了这两个就可以自己调试一些简单的demo。接下来就是你的程序不能只在控制台打印信息，要能对外输入和输出。这块一般是两部分:1、还是在自己的计算机内部，能从磁盘读取和保存数据。2、能够和别的计算机通信，也就是socket http等网络编程。再接下来就是一些每个编程语言自己特有的特性，需要好好琢磨和体会。深入一些就是编写的程序到计算机执行是个什么过程，对c来讲，程序如何被编译的，如何链接的，如何被系统装载运行的；对JAVA来讲，需要了解JVM。只有了解了这些，才能了解前辈大牛们的程序为什么那样去写，也才能解决后面遇到的一些深层次的问题。</div>2019-11-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/8a/a7/674c1864.jpg" width="30px"><span>William</span> 👍（4） 💬（0）<div>居然有加餐，666.
 
一篇文章涵盖java 语法，赞.

另外补充一下，关于权限限定符，
还有个default，支持的范围是 本包内可用， 

protected 也支持本包内可使用. 

编程语言确实不是最重要的，因为在企业中需要的是能够产生价值的软件，而非其他. 
</div>2019-11-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/18/fb/6c/12fdc372.jpg" width="30px"><span>被水淹没</span> 👍（3） 💬（1）<div>高中学了vb，以为大多编程语言都差不多，基本的变量、控制语句都差不多
然后去学C，看到后面... 我擦这指针啥玩意？看来得补一下指针，然后搜了下..  厚厚的一本指针教程... 然后就被打击到了
直到大学学了java，没指针，舒坦...     大学完就只会ssh，ssm，还好实习找得到工作，现在努力提升自己，先把争哥的这2套课程学了先 ^-^</div>2019-11-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/8d/67/2471da5b.jpg" width="30px"><span>阿辉</span> 👍（3） 💬（0）<div>Swift， Object-c，Java</div>2019-11-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/9a/12/06863960.jpg" width="30px"><span>稳</span> 👍（3） 💬（0）<div>1、拿个人Python的经历，入门3天，熟练的话需要至少写一个项目，工作写了2年也不敢吹精通。我觉得学习一门语言，入门时一定要打牢基础，把基础语法耐心看仔细了，以后才会少踩坑，书籍专栏视频都可以。熟练的话一定要多练，主要时熟悉常用库和生态，精通就需要研究源码和不断的思考了。
2、虽然语言是工具，我觉得必须要有一门足够熟练的编程语言，这样整个人思维深度都不一样。从国内招聘来说，也只愿意要来了就能赚钱的，而不是花钱培养还可能跑路的。</div>2019-11-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/0c/86/8e52afb8.jpg" width="30px"><span>花花大脸猫</span> 👍（2） 💬（0）<div>1.熟练大概是3-4年的时候，但是只是用的熟练，后续由于处理问题，对某些领域或者框架需要深挖，发现自己越来越渺小，关联的需要了解的知识也越来越多，越来越复杂，层次也越来越深。所以好的建议就是学以致用并以此为根基深挖，并针对学习的语言，时刻了解官方的版本更迭，以及其规划的发现路线。
2.我的理解来看，社招来看至少需要占到50％，校招的话可能更看重的是基础以及逻辑思维还有自身的发展潜力</div>2020-07-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/75/9b/611e74ab.jpg" width="30px"><span>技术修行者</span> 👍（2） 💬（0）<div>这篇看得毫无压力😁</div>2019-11-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/a0/6b/0a21b2b8.jpg" width="30px"><span>迷羊</span> 👍（2） 💬（0）<div>我大一上学期末最后一个月才开始学C，又学了一整个寒假，下学期回到学校就开始学Java了，到如今Java已经使用了近两年，我觉得0基础学编程语言，不要一上来就看书，看不进去的，个人推荐看视频，后面跟着视频做项目把学到的东西全部用上。在找bug的时候也会极大的增强你的编程能力。等到你什么时候觉得看视频学习很慢，而且也不深入，那个时候就是你开始看书和看博客开始的时候了。</div>2019-11-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/19/93/d7/93c8f92a.jpg" width="30px"><span>斜杠ing...</span> 👍（2） 💬（1）<div>语言虽然只是个工具，但对于大多数人来说，几乎就用一种语言，还是精通后才能说语言是相通的。</div>2019-11-17</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTKextUrbqPLdOUHdlngO8H8YWLIOhYc2L7FFtZmxS7yTwqwOgbe4ssSxXxkUibO5vFRwvzUG9Tb6gw/132" width="30px"><span>Geek_rtds5n</span> 👍（1） 💬（0）<div>学过N门语言，基本触类旁通，熟练的只有java和js吧，技巧就是多练，多看，多想，多练就不说了，多看就是多看源码，多看别人是怎么实现的，多想就是琢磨为什么要这么写不那么写。
熟练掌握算是基本，只要你认真学，勤于思考，肯定是很快可以熟练掌握的，掌握了一门语言，也只是开始而已。</div>2019-12-06</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/46/3f/7825378a.jpg" width="30px"><span>无名氏</span> 👍（1） 💬（0）<div>这篇毫无压力</div>2019-11-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/ec/a3/28763399.jpg" width="30px"><span>CHS</span> 👍（1） 💬（0）<div>学习一门新语言的时候，必须把基础过一遍，并且自己练一遍。是语言是一个工具，编程思想是互通的，但编程工具的使用却不一样，有的些工具相似，有些工具差异却很大。

所以一定要把这个工具的基础弄熟练，这样当你想要实现自己的某个思想的时候，才能得心应手。就比如开车，我们都会开车，之前开的是老式的车，在后来的新车有了很多新的功能，比如定速巡航，我们不知道，还是按照老式的车来开，虽然可以开，但是很多好用的功能都没用到，在到以后可以自动驾驶了，我们还是用老式车的方式去开，任然无法享受到新式车带来的便利</div>2019-11-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/a5/67/bf286335.jpg" width="30px"><span>AllenGFLiu</span> 👍（1） 💬（0）<div>跟大家一样，在学校里学的C，自然是没学懂，更谈不上精通了。

后来工作上用的是Delphi，只会CRUD，期间也想自学Java，但在学习过程中，对基本的数据结构都不了解，并且也没项目可以边学边做，所以很痛苦。

后来，转部门学了Python，并且学了争哥的上一门数据结构课，现在再过来看Java的基础知识课，真是眼前一亮的感觉，不过如此嘛，当时自学的时候死扣的容器，现在瞄一眼就知道干啥了，现在懊悔的是当时没早点学习基础知识。</div>2019-11-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/65/c5/b379fc6d.jpg" width="30px"><span>Chandler</span> 👍（1） 💬（0）<div>感觉学编程还是得注重语言特性的学习，编程语言有很多种，但语言特性就那么些东西。推荐一篇关于如何学习，选择编程语言的文章。
http:&#47;&#47;www.yinwang.org&#47;blog-cn&#47;2017&#47;07&#47;06&#47;master-pl</div>2019-11-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/cb/9f/ee68858c.jpg" width="30px"><span>阿玛铭</span> 👍（1） 💬（0）<div>掌握编程语言的含义：首先了解编程语言的优劣势和适用场景。然后是掌握语法，编程原则和范式，底层支撑原理（数据算法 数据结构  JVM 等），工具生态（熟悉第三方包、异常问题处理、整个软件开发过程的支撑工具框架等）。1. 语法上差别不大，所以对于一个已经掌握一门编程语言的程序员而言掌握另一门编程语言的语法是花费不了太多时间的，即便是刚开始接触计算机知识，也不会太难。2.编程范式和原则是本课程的重点内容，在跟着课程研究 3.偏理论部分，需要逻辑推理的知识。底层支撑是互联网大企业最看重的，重要性如何可以参考市场评价。4.偏实践工程部分的，需要时间来积淀的经验。
以上四个方面都做到深入研究的人才有资格说自己熟悉某某编程语言。都做到位之后才可以做到举一反三，触类旁通。但是学习的境界永无止境，业界语言大师之所以能推出编程语言，是因为他们有无意识地站在哲学高度上看变成语言的演进特点。能被留下来的语言或较广泛使用都是能解决某些领域的问题的语言。</div>2019-11-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/f4/0a/02ecee7a.jpg" width="30px"><span>女干部</span> 👍（1） 💬（0）<div>买了那么多java课没学，万万没想到，
从小争哥这里入门了java,
真的极具总结性</div>2019-11-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/f8/99/8e760987.jpg" width="30px"><span>許敲敲</span> 👍（1） 💬（0）<div>觉得真的是语言不是问题，最早大二开始学习C，C++后面Matlab。 读研写有限元、材料用户子程序用的Fortran。参数化建模，CAD里面会用到python，Lisp，VB。到了工作后才开始认真学习python，做深度学习需要这个。 
现在web开发，会用到JavaScript，TyperScript，还有写webGL也会了解一些Shader。
自己感觉，学一门语言，就是了解基本文法先，能写hello world。 后面再一点点精进，学advanced feature。</div>2019-11-17</li><br/>
</ul>