你好，我是程远。

上一讲里，我们一起学习了perf这个工具。在我们的案例里，使用perf找到了热点函数之后，我们又使用了ftrace这个工具，最终锁定了长延时的函数estimation\_timer()。

那么这一讲，我们就来学习一下ftrace这个工具，主要分为两个部分来学习。

第一部分讲解ftrace的最基本的使用方法，里面也会提到在我们的案例中是如何使用的。第二部分我们一起看看Linux ftrace是如何实现的，这样可以帮助你更好地理解Linux的ftrace工具。

## ftrace的基本使用方法

ftrace这个工具在2008年的时候就被合入了Linux内核，当时的版本还是Linux2.6.x。从ftrace的名字function tracer，其实我们就可以看出，它最初就是用来trace内核中的函数的。

当然了，现在ftrace的功能要更加丰富了。不过，function tracer作为ftrace最基本的功能，也是我们平常调试Linux内核问题时最常用到的功能。那我们就先来看看这个最基本，同时也是最重要的function tracer的功能。

ftrace的操作都可以在tracefs这个虚拟文件系统中完成，对于CentOS，这个tracefs的挂载点在/sys/kernel/debug/tracing下：
<div><strong>精选留言（4）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/0f/5e/96/a03175bc.jpg" width="30px"><span>莫名</span> 👍（15） 💬（2）<div>赞，非常适合入门 ftrace 的科普文。操控 tracefs 各种文件相对繁琐（但便于理解 ftrace），推荐使用 ftrace 的一个前端工具 trace-cmd，类似 perf 用法，简单易用。</div>2021-02-05</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/19/7c/bb/635a2710.jpg" width="30px"><span>徐少文</span> 👍（5） 💬（2）<div>inline函数在编译的时候实际上不是函数，而是直接在原函数处展开，主要是为了提高效率。所以实际上不能使用。static函数可以使用</div>2022-03-07</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/0c/30/d4737cd5.jpg" width="30px"><span>lyonger</span> 👍（2） 💬（1）<div>tracefs 这个虚拟文件系统，只能在宿主上操作？ 如果需要在容器里操作的话，有啥方法么？</div>2021-09-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/c4/03/f753fda7.jpg" width="30px"><span>JianXu</span> 👍（4） 💬（0）<div>今天才看完所有的文章，好多东西要学。周五晚上看到Sherlock&#47;SRE 群里Ralph 分享了一篇文章讲在Clickhouse 基础上支持类Spark 能力的文章，Huai 回复说这才是我们的工程师应该做的事情，顿时觉得自己那些小trick 不值一提。我们还是应该在这些技术上做深耕，Cloud 这条线也是一样的。</div>2022-09-11</li><br/>
</ul>