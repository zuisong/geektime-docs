你好，我是宫文学。

在前面两讲中，我们已经分析了Python从开始编译到生成字节码的机制。但是，我们对Python只是了解了一半，还有很多问题需要解答。比如：**Python字节码是如何运行的呢？它是如何管理程序所用到的数据的？它的类型体系是如何设计的，有什么特点？**等等。

所以今天这一讲，我们就来讨论一下Python的运行时机制。其中的**核心，是Python对象机制的设计**。

我们先来研究一下字节码的运行机制。你会发现，它跟Python的对象机制密切相关。

## 理解字节码的执行过程

我们用GDB跟踪执行一个简单的示例程序，它只有一行：“`a=1`”。

这行代码对应的字节码如下。其中，前两行指令实现了“`a=1`”的功能（后两行是根据Python的规定，在执行完一个模块之后，缺省返回一个None值）。

![](https://static001.geekbang.org/resource/image/8a/50/8ae69517e1bfec78fddea57e4da89e50.jpg?wh=532%2A116)

你需要在**\_PyEval\_EvalFrameDefault()函数**这里设置一个断点，在这里实际解释指令并执行。

**首先是执行第一行指令，LOAD\_CONST。**

![](https://static001.geekbang.org/resource/image/de/48/def47ca68f979af8cf684e47c0889848.jpg?wh=1052%2A332)

你会看到，解释器做了三件事情：

1. 从常数表里取出0号常数。你知道，编译完毕以后会形成PyCodeObject，而在这个对象里会记录所有的常量、符号名称、本地变量等信息。常量1就是从它的常量表中取出来的。
2. 把对象引用值加1。对象引用跟垃圾收集机制相关。
3. 把这个常数对象入栈。
<div><strong>精选留言（4）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/11/a9/84/c87b51ce.jpg" width="30px"><span>xiaobang</span> 👍（4） 💬（1）<div>请问pypy内部也有类似的pytype结构吗</div>2020-09-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1d/11/80/730acb11.jpg" width="30px"><span>维李设论</span> 👍（1） 💬（1）<div>python也是万物皆对象？堆那里跟js有点儿像啊，比js的能力更多了，是不是解释性脚本语言都是这个特点？</div>2020-08-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/23/c4/91/a017bf72.jpg" width="30px"><span>coconut</span> 👍（0） 💬（1）<div>你可以注意到，我在图 1 中标出了每个字段所占内存的大小，总共是 28 个字节

这里没看懂，图上标的不是32个字节么？</div>2021-01-14</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/J3dqALgicfVklewMjVkpyLbTk9YiamnBf5QQZ3NPHGlMeVSdLDB5yHLicEZHKBbUets76KOFwbl9ju0xJw1VeGa1A/132" width="30px"><span>飞翔</span> 👍（0） 💬（1）<div> python编译过程中会调到python的代码，pgen用来生成c语言的代码，那这个原始的Python编译器是用什么实现的？也就是第一个的Python编译器是怎么出来的？</div>2020-07-17</li><br/>
</ul>