你好，我是Tony Bai。

上一讲，我们探讨了**“Go从哪里来，并可能要往哪里去”**的问题。根据“绝大多数主流编程语言将在其15至20年间大步前进”这个依据，我们给出了一个结论：**Go语言即将进入自己的黄金5~10年**。

那么此时此刻，想必你已经跃跃欲试，想要尽快开启Go编程之旅。但在正式学习Go语法之前，我还是要再来给你**泼泼冷水**，因为这将决定你后续的学习结果，是“从入门到继续”还是“从入门到放弃”。

很多编程语言的初学者在学习初期，可能都会遇到这样的问题：最初兴致勃勃地开始学习一门编程语言，学着学着就发现了很多“别扭”的地方，比如想要的语言特性缺失、语法风格冷僻与主流语言差异较大、语言的不同版本间无法兼容、语言的语法特性过多导致学习曲线陡峭、语言的工具链支持较差，等等。

其实以上的这些问题，本质上都与语言设计者的设计哲学有关。所谓编程语言的设计哲学，就是指决定这门语言演化进程的高级原则和依据。

**设计哲学之于编程语言，就好比一个人的价值观之于这个人的行为。**

因为如果你不认同一个人的价值观，那你其实很难与之持续交往下去，即所谓道不同不相为谋。类似的，如果你不认同一门编程语言的设计哲学，那么大概率你在后续的语言学习中，就会遇到上面提到的这些问题，而且可能会让你失去继续学习的精神动力。
<div><strong>精选留言（30）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/27/52/40/db9b0eb2.jpg" width="30px"><span>自由</span> 👍（40） 💬（6）<div>Tony Bai 老师，你好，例举两个我认为复合 Go 语言设计哲学的例子，我的技术能力捉襟见肘，说的不对地方还希望老师斧正。

一、异常处理

Go 语言核心开发者 Dave 曾说过 “You only need to check the error value if you care about the result”，在我们不处理错误的时候，我们不应该对它的返回值抱有任何幻想。

Go 的异常处理逻辑，没有引入 exception，而是使用了多参数返回，在返回中带上错误，由调用者来判定这个错误。

- 简单
- 没有隐藏的控制流
- 完全交给你控制 error
- 考虑失败，而不是成功

二、类型别名

在特定情况下，帮助代码逐步修复。

类型别名的存在，是 渐进式代码修复(Gradual code repair) 的关键，什么是渐进式代码修复？举一个🌰 重构。重构代码，我们当然希望重构后的好处，能够适用于所有代码，但是，重构的好处与代价是成正比的，往往一次重构会伴随着大量的修改，随着代码量越来越大，一次完成所有修改变得不可行。修复需要逐步完成。在代码量少时，我们可以一次性完成所有的修复，这样的修复被称为原子代码修复(atomic code repair)，它的概念很简单，就是在一次提交中，更新所有的因为重构带来的问题修复，但是概念的简单会被实际的复杂性抵消，一次提交可能非常大，大的提交很难去一次性修复，出现问题也很难去溯源，最重要的是，可能会与其他同学的工作产生冲突，例如某个同学，在工作时，使用了旧的 API，合并代码时，并不会产生冲突，而我的提交错过了它的引用。

因此，我们需要一个过渡期，这个过渡期就是为了逐步替换，也就是渐进式代码修复，将旧的引用，逐步替换，同时将旧的换为新的，这就是渐进式代码修复，它的缺点是比原子代码修复的工作量更大，但是它更容易提交、审查，并且保证了，没有人引用后再删除旧的类型别名。
</div>2021-10-15</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/79/69/5960a2af.jpg" width="30px"><span>王智</span> 👍（33） 💬（6）<div>表示身为一名Java工程师，在看到组合的时候有一点疑惑，我的想法是这里的组合就是将另一个类里面的东西平移过来，类似于java中的继承，我想问的是如果存在两个类包含相同名字的方法或者属性，这个go怎么处理？还是直接就不允许呢？go语言从来没接触过，不懂就问</div>2021-10-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/26/27/eba94899.jpg" width="30px"><span>罗杰</span> 👍（22） 💬（7）<div>21 世纪的 C 语言，的确实至名归。依然有几个小问题：1. Go 有 GC，我们使用 Go 来开发后端的所有服务，有个 PVP 的服务，需要逐帧计算客户端上报的结果是否正确，此时对于内存的分配就要特别小心，开发起来很不顺畅。是否这种服务的性质不太合适使用 Go 来开发；2. 有人吐槽 Go 核心人员不想做的东西，就是 Less is more，自己想做就是各种哲学，这个问题，老师怎么看？</div>2021-10-15</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/20/1e/18/9d1f1439.jpg" width="30px"><span>liaomars</span> 👍（16） 💬（9）<div>go的异常处理，使用起来简单，但是不方便，请问老师这是在践行go的简单设计哲学吗？</div>2021-10-15</li><br/><li><img src="" width="30px"><span>Geek_399042</span> 👍（12） 💬（2）<div>自动加入分号是不是也是简单的设计哲学呢，能让编译器做的事不需要交给开发者。</div>2021-10-15</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/0a/a4/828a431f.jpg" width="30px"><span>张申傲</span> 👍（10） 💬（3）<div>尤其认同 Go 语言的“面向工程”这一设计哲学。作为 Java 的资深用户，每天都深受编译速度慢、依赖树失控、代码风格不统一等问题的困扰。Go 语言的设计哲学恰恰迎合了现代大规模业务系统的开发和维护。</div>2021-12-01</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/38/65/edf48816.jpg" width="30px"><span>悟二空</span> 👍（8） 💬（1）<div>只有 TonyBai 老师的这门专栏课，我会把每条留言评论都认真看完，因为老师都有很认真的在回复，一点儿也不含糊。能学到非常多的知识，非常感谢老师，我一定能学好Go语言并进入自己想去的公司的。</div>2022-04-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/16/5c/d0476f9f.jpg" width="30px"><span>运维夜谈</span> 👍（7） 💬（5）<div>老师，请教两个问题：
1、文中提到的正交独立是什么意思？不是很理解。
2、Go不支持面向对象，那意味着复用性不好，这种后面老师会讲工程实践吗？</div>2021-12-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/a2/5e/3871ff79.jpg" width="30px"><span>迷途书童</span> 👍（5） 💬（3）<div>Go语言的设计哲学有什么权威出处吗？还是老师自己总结的？</div>2022-06-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/9d/a4/e481ae48.jpg" width="30px"><span>lesserror</span> 👍（4） 💬（1）<div>Tony Bai老师，关于文中的“去除包的循环依赖，循环依赖会在大规模的代码中引发问题，因为它们要求编译器同时处理更大的源文件集，这会减慢增量构建”，这里一直没太理解，能详细解释一下么？</div>2023-05-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/30/77/1c/791d0f5e.jpg" width="30px"><span>ucat</span> 👍（3） 💬（1）<div>站在巨人的肩膀上的语言，对自己有着清晰的定位，并能解决痛点。
喜欢这样的设计哲学。
Go 语言的设计哲学：**简单**、**显式**、**组合**、**并发**和**面向工程**。

* 简单：是指Go语言特性始终保持在少且足够的水平
* 显示：是指任何代码行为都需开发者明确知晓，不存在暗箱操作
* 组合：是构建Go程序骨架的主要方式，分为 **垂直组合** 与 **水平组合** 可以大幅降低程序元素间的耦合，提高程序的可拓展性和灵活性
* 并发：采用了用户层轻量级线程goroutine 占用的资源非常小，Go 运行时默认为每个 goroutine 分配的栈空间仅 2KB。goroutine 调度的切换也不用陷入（trap）操作系统内核层完成，代价很低
* 面向工程：Go 语言最初设计阶段就将解决工程问题作为 Go 的设计原则之一去考虑 Go 语法、工具链与标准库的设计，如 快速构建，包名称不必是唯一的，去除循环依赖，不支持默认函数参数，增加类型别名，引入必使用，</div>2022-12-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/23/e6/12b3d2bf.jpg" width="30px"><span>Holy</span> 👍（3） 💬（1）<div>go底层代码深入发现了很多巧妙的地方， 
defer+panic简单使用，里面的实现不一般
内存管理多级缓存快速减少锁，为GC埋下众多伏笔，
Mutex兼顾公平
GMP模式实现等等，
每个版本迭代，持续进化（GOPHER坐享其成）</div>2022-04-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/fb/6a/03aabb63.jpg" width="30px"><span>Alexhuihui</span> 👍（3） 💬（1）<div>“水平组合是一种能力委托（Delegate），我们通常使用接口类型来实现水平组合。“，原文这段话没理解，老师能再解释一下水平组合吗</div>2021-10-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/48/11/420b6a25.jpg" width="30px"><span>Hua.R</span> 👍（3） 💬（1）<div>搭车问一下，去年我曾在大佬博客咨询过慕课网的专栏出版纸质书的问题，大佬回答当年底出版。大半年过去后没有动静我又问了一次你说已经提交出版社。那大概多久可以看到实物呢？</div>2021-10-16</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/9d/a4/e481ae48.jpg" width="30px"><span>lesserror</span> 👍（3） 💬（2）<div>感谢 Tony Bai 这一篇的分享，很精彩。有以下几点困惑，麻烦有时间回答一下：

1. go1.16.4 版本中的 poolLocal 结构体的实现和本文中的不太一样呢？

2. 水平组合“模式”还有点缀器、中间件等方式后面的文章中会有例子吗？

3. 很多课程中，都有“并发原语”一词，百度查了一下，有一些理解。老师这里会有比较通俗易懂的理解吗？</div>2021-10-15</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1c/96/dd/1620a744.jpg" width="30px"><span>simple_孙</span> 👍（2） 💬（1）<div>通读一遍课程之后，回头看这篇文章更通透了</div>2022-03-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/a3/ea/bd83bd4f.jpg" width="30px"><span>麦芽糖</span> 👍（2） 💬（1）<div>设计哲学很重要，就比如一个人的价值观，或者背景。 
在不了解别人价值观的时候去评价是不合理的，具备同样价值观的人才能走的更好。
比如国家之前的相互不理解，是因为国家的文化不同。

同样，需要理解 Go 的设计哲学显得非常重要。

设计哲学有
● 简单
● 显示
● 组合
● 并发
● 面向工程

简单。
比如关键字就很少。入门快。

显示。
如不同类型不能做运算，避免意料之外的事情发生。

组合。
暂时还不是很理解。

并发。
天生就为多核 CPU 开发，同时有自己的 goroutine 用户层轻量级线程，性能更好。

面向工程。
格式化、调试、工具链、默认参数等。</div>2022-01-15</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/ce/d7/5315f6ce.jpg" width="30px"><span>不负青春不负己🤘</span> 👍（2） 💬（2）<div>最新版本Go 支持泛型，也就是不完全显式，算是平衡？</div>2021-10-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1d/74/e1/284e7c38.jpg" width="30px"><span>许诺</span> 👍（1） 💬（1）<div>问下老师，什么时候更新完啊？</div>2021-10-16</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/7d/04/d606b6a8.jpg" width="30px"><span>phylony-lu</span> 👍（0） 💬（1）<div>Tony老师好，组合中的垂直组合是通过什么样方式实现的呢？水平组合不是特别清楚为什么这样可以降低耦合。</div>2023-07-14</li><br/><li><img src="" width="30px"><span>Geek_46a7a4</span> 👍（0） 💬（1）<div>没有视频？只有语音？</div>2023-07-03</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/18/7b/03/03583011.jpg" width="30px"><span>天天有吃的</span> 👍（0） 💬（1）<div>老师请问下，这门课程有没有goruntime go并发相关的内容？</div>2023-04-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/17/00/b3/2536a41b.jpg" width="30px"><span>Jolyne</span> 👍（0） 💬（1）<div>如果 Go 是男孩子，那我现在、立刻、马上 就表白。</div>2023-02-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1d/1a/e1/1acde886.jpg" width="30px"><span>demajiao</span> 👍（0） 💬（1）<div>看了2章，作者是懂go语言的。</div>2023-01-06</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/c1/46/a81f7402.jpg" width="30px"><span>王大华</span> 👍（0） 💬（1）<div>刚开始接触 Go 看了这篇有点懵，对于一些名字理解不太好，看完后面再来重新刷一下。</div>2022-07-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/57/1e/8ed4a7cf.jpg" width="30px"><span>Paradise</span> 👍（0） 💬（1）<div>感谢 Tony Bai 的分享，这一讲值得反复体会</div>2022-04-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/20/95/99/959f14de.jpg" width="30px"><span>s t o a</span> 👍（0） 💬（1）<div>看了一下语法感觉很简单。</div>2021-11-07</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/53/a8/abc96f70.jpg" width="30px"><span>return</span> 👍（0） 💬（3）<div>老师，请教一下  “Hello and Bye” 是表达了什么， 没有google到。。。。</div>2021-11-04</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/2a/e9/dc/cc05ebc7.jpg" width="30px"><span>小明</span> 👍（0） 💬（1）<div>老师后续是视频还是一直都是这种录音呀</div>2021-10-16</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/2a/e1/09/efa69f7a.jpg" width="30px"><span>学昊</span> 👍（13） 💬（1）<div>本人老java码农了。进阶的代码设计是设计模式，让代码能更优雅的实现。终极的代码设计是哲学，是代码中表达出的价值观。</div>2021-10-15</li><br/>
</ul>