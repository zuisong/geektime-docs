你好，我是卢誉声。

在上一讲中，我们掌握了C++20标准下需要实现的协程接口约定。就目前来说，在没有标准库支持的情况下，这些约定我们都需要自己实现。

但是，仅通过阅读标准文档或参考代码，编写满足C++协程约定的程序比较困难。因此，我安排了两讲内容带你实战演练一下，以一个异步文件系统操作库为例，学习如何编写满足C++协程约定的程序。

这一讲我们先明确模块架构，完成基础类型模块和任务调度模块，为后面实现基于协程的异步I/O调度打好基础，今天的重点内容是任务调度模块。

好，话不多说，就让我们从模块架构开始，一步步实现任务调度模块（（课程配套代码，点击[这里](https://github.com/samblg/cpp20-plus-indepth)即可获取））。

## 模块组织方式

由于这是一个用C++实现的异步文件操作库，我们就将它命名为asyncpp，取async（即异步asynchronous这一单词的缩写）和cpp的组合。这个基于C++协程的库支持通用异步任务、I/O异步任务以及异步文件系统操作，主要用于I/O等任务而非计算任务。

整个项目的模块架构图如下。

![](https://static001.geekbang.org/resource/image/5f/c6/5fd10bd7916781554c4a61bd2yy2f8c6.jpg?wh=2900x2384)

我们用C++ Modules组装整个库，我先带你了解一下里面的模块有哪些。

- asyncpp.core：核心的基础类型模块，主要用来定义基础的类型与concepts。
- asyncpp.task：通用异步任务模块，实现了主线程内的异步任务框架，包括queue、loop、coroutine和asyncify几个分区。
- asyncpp.io：异步I/O模块，实现了独立的异步I/O线程和任务处理框架，用于独立异步处理I/O，包括task、loop和asyncify几个分区。
- asyncpp.fs：异步文件系统模块，基于asyncpp.io模块实现了异步的文件系统处理函数。
<div><strong>精选留言（4）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/30/db/86/51ec4c41.jpg" width="30px"><span>李云龙</span> 👍（1） 💬（1）<div>关于课后思考题：我认为老师课件中的当前代码无法做到等待另一个协程执行结束，因为传递给await_suspend函数的协程句柄是当前协程的，所以无法获知另外一个协程的信息。如果要等待另一个协程执行结束，需要在Awaitable类中存储另外一个协程的句柄，然后defaultAysncAwaitableSuspend函数的第三个实参应该是被存储的另外一个协程的句柄。在defaultAysncAwaitableSuspend函数内部使用循环检查的方式，检查 h.done（） 是否为true，只有条件成立后，再调用 AsyncTaskResumer 。
烦请老师批评指正</div>2023-12-25</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/18/c1/39/11904266.jpg" width="30px"><span>Steiner</span> 👍（0） 💬（1）<div>我想问一下，课程中的代码是在哪个平台上运行，用哪种编译器</div>2024-08-19</li><br/><li><img src="" width="30px"><span>常振华</span> 👍（0） 💬（1）<div>.handler = [resumer, awaitable] {
    awaitable-&gt;_taskResult = awaitable-&gt;_taskHandler(); 
    resumer(); 
}
这个写法是lamda表达式吗？然后赋值给struct AsyncTask的handler成员？</div>2023-09-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/25/87/f3a69d1b.jpg" width="30px"><span>peter</span> 👍（0） 💬（1）<div>请问：“主线程内”是什么意思？
文中有一句“asyncpp.task：通用异步任务模块，实现了主线程内的异步任务框架”。是说通用异步任务模块运行在主线程中吗？异步 I&#47;O 模块、异步文件系统模块是运行在其他线程吗？
另外，“主线程”是“库”的主线程，不是调用者的主线程，对吗？</div>2023-02-04</li><br/>
</ul>