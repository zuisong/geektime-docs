你好，我是卢誉声。

今天，我们继续上一讲的工作，实现基于协程调度的异步文件系统操作库。同时，在这一讲中，我们还要探讨一个重要话题，即实现所有调度线程全异步化的理想异步模型。

上一讲的最后，我们已经实现了任务调度模块，这意味着我们搭建好了基于协程的任务调度框架。但是，目前task模块是运行在主线程上的。因此，只有当主线程没有其他任务执行时，task模块才会从消息循环中获取任务执行，并唤醒协程。

这不是一个理想的异步框架模型，**我们更希望实现的是主线程和I/O调度全异步化。那么，这要如何实现呢？**

项目的完整代码，你可以[这里](https://github.com/samblg/cpp20-plus-indepth)获取。

## I/O调度模块

其实，task模块中预留的AsyncTaskSuspender函数，就是为了实现自定义任务的处理与唤醒机制。为此，我们继续讨论异步I/O的实现——基于task模块的任务调度框架，实现基于协程的异步I/O调度。

我们的基本思路是下图这样。

![](https://static001.geekbang.org/resource/image/13/11/13718c7eyy43faaaa2f6871f34623111.jpg?wh=3717x2458)

首先，我们要为I/O任务创建独立的任务队列。然后，AsyncTaskSuspender中的主线程，负责将任务与协程的唤醒函数分发到I/O任务队列中。

接下来还要创建一个有独立任务循环的新线程，读取I/O任务队列，用于处理I/O任务。最后，处理完I/O任务后，将任务的返回值和协程唤醒函数分发到主线程的任务队列中。根据主线程的任务循环机制，当主线程空闲时，唤醒协程。
<div><strong>精选留言（2）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/14/eb/4f/6a97b1cd.jpg" width="30px"><span>猪小擎</span> 👍（1） 💬（2）<div>老师的github代码有好多GBK文件，建议修改下。
携程的本质优点减少上下文切换，（中断），中断操作系统会把寄存器存在栈顶，然后内核栈和用户栈互换，这些大概会消耗1-10微秒。携程就要节约这无数的1-10微秒。可以操作系统的IO操作是默认会中断的，要把中断改成yield出让执行权需要做什么呢？底层调用的filesystem的操作本身就是中断操作吧？上层改成携程，对于进程来说，这中断的消耗并没有节省。</div>2023-03-30</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/25/87/f3a69d1b.jpg" width="30px"><span>peter</span> 👍（0） 💬（1）<div>请教老师两个问题：
Q1：asyncF与testVoid定义为什么不同？
asyncF与testVoid都是协程，但testVoid的定义是：asyncpp::task::Coroutine testVoid()；而testVoid的定义是Coroutine asyncF()。函数前面部分不同，为什么？
Q2：协程在C++语法层面的支持就是几个关键字吗？
这两篇读下来，有点模模糊糊，总体上感觉在C++语法层面，对于协程，似乎就是Coroutine、co_await这两个关键字，是吗？（Awaitable 和 Awaiter需要自己实现，不算关键字吧）</div>2023-02-07</li><br/>
</ul>