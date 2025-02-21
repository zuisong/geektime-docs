前不久我参加了一个国外程序员的讲座，讲座的副标题很有趣，叫做：“我如何学会停止恐惧，并且爱上Java虚拟机”。

这句话来自一部黑色幽默电影《奇爱博士》，电影描述了冷战时期剑拔弩张的氛围。

程序员之间的语言之争又未尝不是如此。写系统语言的鄙视托管语言低下的执行效率；写托管语言的则取笑系统语言需要手动管理内存；写动态语言的不屑于静态语言那冗余的类型系统；写静态语言的则嘲讽动态语言里面各种光怪陆离的运行时错误。

Java作为应用最广的语言，自然吸引了不少的攻击，而身为Java程序员的你，或许在口水战中落了下风，忿忿于没有足够的知识武装自己；又或许想要深入学习Java语言，却又无从下手。甚至是在实践中被Java的启动性能、内存耗费所震惊，因此对Java语言本身产生了种种的怀疑与顾虑。

别担心，我就是来解答你对Java的种种疑虑的。“知其然”也要“知其所以然”，学习Java虚拟机的本质，更多是了解Java程序是如何被执行且优化的。这样一来，你才可以从内部入手，达到高效编程的目的。与此同时，你也可以为学习更深层级、更为核心的Java技术打好基础。

我相信在不少程序员的观念里，Java虚拟机是透明的。在大家看来，我们仅需知道Java核心类库，以及第三方类库里API的用法，便可以专注于实现具体业务，并且依赖Java虚拟机自动执行乃至优化我们的应用程序。那么，我们还需要了解Java虚拟机吗？
<div><strong>精选留言（30）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/0f/67/f4/9a1feb59.jpg" width="30px"><span>钱</span> 👍（237） 💬（1）<div>JVM
1:现在我的理解
1-1:三个英文单词的缩写，中文意思是Java虚拟机，作用是帮助执行Java字节码的，不同的平台有不同的JVM，这样java源代码经过编译为字节码之后就能在各种平台上运行了
1-2:JVM还有内存管理，垃圾回收等底层功能，这样程序员就不用太操心这些事情了
1-3:内存管理主要是将JVM的内存容量划分成不同的模块，使用不同的管理方式，核心目的是为了更少的内存使用更快的内存性能以及恰当的内存回收策略
1-4:垃圾回收之所以存在是因为JVM是运行在内存之中的，它的内存空间是有限的，当加载进内存的对象越来越多的时候，会影响JVM的运行性能，所以，要回收一些内存空间，垃圾回收的关键是识别出垃圾以及使用不影响JVM运行的回收策略
1-5:JVM是Java代码执行的地方，Java程序性能上出现了问题的时候，我们要从代码层面进行分析、定位、优化，但是我们怎么知道那段代码性能差哪？此时要看JVM中代码的执行情况，看看谁慢？为什么慢？这些我还不清楚咋快速定位，所以，我订阅了这个专栏

2我希望我能学到如下内容
2-1:Java源代码怎么变成Java字节码的？
2-2:Java字节码怎么进入JVM的？
2-3:Java 字节码进入JVM后是怎么放置的？
2-4:JVM执行字节码的时候怎么定位的？他怎么知道该执行那句代码了？它怎么知道那句代码是什么意思？
2-5:性能优化，我的理解是让干活快的干活，不让干的慢的干，如果做不到，就让干活快的多干，干的慢的少干？JVM的性能优化可能也类似，哪JVM怎么知道谁干的慢谁干的快？JVM在执行Java字节码的时候都是需要做什么事情呢？它怎么安排自己的工作的呢？
2-6:实际开发工作中怎么监控JVM的工作情况哪？怎么定位那些懒蛋哪？定位到了怎么解决他们哪？
</div>2018-07-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/34/b6/0feb574b.jpg" width="30px"><span>我的黄金时代</span> 👍（2） 💬（0）<div>下面这个讲课的目录很给力</div>2018-07-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/b5/b0/7f350c5a.jpg" width="30px"><span>Desperado</span> 👍（2） 💬（0）<div>沙发期待中</div>2018-07-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/05/1c/d4854ba6.jpg" width="30px"><span>木甘</span> 👍（18） 💬（1）<div>是java10吗</div>2018-07-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/ff/f1/8e9d8e97.jpg" width="30px"><span>lynd</span> 👍（7） 💬（1）<div>能够对java虚拟机做分块的详细介绍不，最好能附上简短的代码介绍，谢谢！</div>2018-07-17</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTIJApYooQ8EHnStvnpnzUxusDjDib5icWcgHj73mqGicj6JwUbcnsS8HzV03LzoNAicQTtegNSgnUT2Gg/132" width="30px"><span>Geek_5sxyw2</span> 👍（41） 💬（0）<div>JVM很有用，目测会是个不错的专栏，期待！</div>2018-07-16</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/b1/cc/d7558b97.jpg" width="30px"><span>沙漏人生</span> 👍（10） 💬（0）<div>已购，看看作者大能如何把复杂的东西简单化。</div>2018-07-16</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/fa/6e/9ea01c1d.jpg" width="30px"><span>zhenTomcat</span> 👍（3） 💬（0）<div>期待</div>2018-07-16</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/7a/7f/1b389e44.jpg" width="30px"><span>闪亮的老刘</span> 👍（2） 💬（0）<div>希望不虚此行，希望有趣。</div>2018-07-16</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/42/c0/980a1cd4.jpg" width="30px"><span>浮生老莫</span> 👍（8） 💬（0）<div>期待老师后续的内容，刚想学JVM，就来了，再打磨打磨自己的技术</div>2018-07-16</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/51/b1/7d6879dc.jpg" width="30px"><span>未设置</span> 👍（16） 💬（0）<div>看了知识框架图 可以说十分期待了</div>2018-07-16</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/d4/f3/129d6dfe.jpg" width="30px"><span>李二木</span> 👍（2） 💬（0）<div>很期待</div>2018-07-16</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/9c/f9/2a2be193.jpg" width="30px"><span>GL€</span> 👍（2） 💬（1）<div>能否分享一下如何编译hotspot?</div>2020-01-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/7d/92/e5f22d7b.jpg" width="30px"><span>小当家</span> 👍（1） 💬（1）<div>希望老师能多推荐些自己研究方向最有用的书籍，补充原理</div>2018-08-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/ac/a1/43d83698.jpg" width="30px"><span>云学</span> 👍（18） 💬（1）<div>提一个建议:  让读者看懂是第一位的。只要读者会java语法，就应该能让他看懂，谢谢</div>2018-07-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/e9/69/779b48c2.jpg" width="30px"><span>苏忆</span> 👍（12） 💬（0）<div>看了下目录，介绍的比较笼统，希望讲解的时候比较深入并提供相关资料提供学习。谢谢，郑大，一起加油！</div>2018-07-16</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/97/25/eaa3132e.jpg" width="30px"><span>小宝儿</span> 👍（10） 💬（0）<div>Android用户也可以长按保存</div>2018-07-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/fe/7b/43d8bbbb.jpg" width="30px"><span>Daph</span> 👍（10） 💬（0）<div>我最嫉妒那些长的比我帅还比我用功的人，期待+1</div>2018-07-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/c9/75/62ce2d69.jpg" width="30px"><span>猿人谷</span> 👍（7） 💬（0）<div>单纯根据目录看，介绍的还是比较泛，希望在文章中对核心点能进行深入的分析，期待精彩干货。</div>2018-07-16</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/e4/76/a97242c0.jpg" width="30px"><span>黄朋飞</span> 👍（6） 💬（0）<div>已经拜读过jvm方面的书籍，但对于调优方面还是比较欠缺，希望能针对jvm线上问题能够学习到有效的解决方案，期待</div>2018-07-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/11/8d/769c8d2a.jpg" width="30px"><span>Daniel</span> 👍（5） 💬（0）<div>果断学习了，站在巨人的肩膀上看世界，然后许下要让世界更加精彩的诺言</div>2018-07-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/00/07/8e3ceda8.jpg" width="30px"><span>吴双</span> 👍（4） 💬（0）<div>已购买，期待后续文章啊</div>2018-07-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/63/14/06eff9a4.jpg" width="30px"><span>Jerry银银</span> 👍（3） 💬（0）<div>这几天，我一直在思考，老师的课程为什么这么编排？如果想深入并且系统地研究Java虚拟机，有没有一个很好的学习主线？

对于这个问题，我凭着我的认知，尝试来总结下：

	1. 首先，Java程序需要被编译成字节码；
	Java程序如何存储的？
	Java编译器相关知识
	字节码相关知识
	编译Java程序，编译器又做了哪些优化？
	AOT又是怎样的技术？

	2. 然后，字节码被加载之后才能被执行
	虚拟机是如何加载字节码的？
	字节码被加载到虚拟机哪个内存区域？
	虚拟机的内存布局又是怎么样的？
	从字节码被加载到执行，这中间虚拟机会做哪些事情？（加载、链接、初始化）
	
	3. 字节码可以被解释执行，还能被即时编译（JIT）成机器码后，然后被执行。
	解释执行的过程是怎么样的？
	JIT具体的原理是？
	虚拟机是如何检测热点代码的？这中间做了哪些优化？
	字节码被执行起来后，对一些无用对象如何处理？——垃圾回收算法
	
</div>2019-12-23</li><br/><li><img src="" width="30px"><span>Knuthie</span> 👍（3） 💬（0）<div>与openjdk  open jvm的对比可以讲讲么？</div>2018-07-19</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/kFu49bDxfrBicVUkSWViaYS74oy6a45ys6oMibZicR978ariaRbu7ib0WqrkpkW34vXSS2JAshotL1L9icuqbxsFACaVQ/132" width="30px"><span>小猫也是老虎</span> 👍（3） 💬（0）<div>希望大佬能在以后更新快点，毕竟秋招要来了😁</div>2018-07-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/48/1d/11d34d57.jpg" width="30px"><span>杨昌明</span> 👍（3） 💬（0）<div>居然亲自朗读</div>2018-07-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/68/1a/dac67baa.jpg" width="30px"><span>Adele</span> 👍（3） 💬（1）<div>我业务+测试+部署，非开发，希望能和开发人员对上话，更好地优化我们的系统😃。</div>2018-07-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/fe/85/9ab352a7.jpg" width="30px"><span>iMARS</span> 👍（3） 💬（0）<div>从.net clr平台转到JAVA平台，深知了解语言运行时处理的重要性，无论是对代码撰写还是效能分析都非常有帮助。</div>2018-07-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/19/78/54005251.jpg" width="30px"><span>鸡肉饭饭</span> 👍（3） 💬（0）<div>希望前期能尽快更新…期待不已</div>2018-07-16</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/12/93/3470fc43.jpg" width="30px"><span>Mr.钧👻</span> 👍（2） 💬（0）<div>我订阅这个专栏，是想学习到以下内容：
1.了解什么是JVM，组成部分
2.了解JVM为什么需要调优
3.了解JVM怎么调优</div>2018-10-03</li><br/>
</ul>