你好，我是程远。

前面两讲，我们分别学习了perf和ftrace这两个最重要 Linux tracing工具。在学习过程中，我们把重点放在了这两个工具最基本的功能点上。

不过你学习完这些之后，我们内核调试版图的知识点还没有全部点亮。

如果你再去查看一些perf、ftrace或者其他Linux tracing相关资料，你可能会常常看到两个单词，“tracepoint”和“kprobe”。你有没有好奇过，这两个名词到底是什么意思，它们和perf、ftrace这些工具又是什么关系呢？

这一讲，我们就来学习这两个在Linux tracing系统中非常重要的概念，它们就是**tracepoint**和**kprobe**。

## tracepoint和kprobe的应用举例

如果你深入地去看一些perf或者ftrace的功能，这时候你会发现它们都有跟tracepoint、kprobe相关的命令。我们先来看几个例子，通过这几个例子，你可以大概先了解一下tracepoint和kprobe的应用，这样我们后面做详细的原理介绍时，你也会更容易理解。

首先看看tracepoint，tracepoint其实就是在Linux内核的一些关键函数中埋下的hook点，这样在tracing的时候，我们就可以在这些固定的点上挂载调试的函数，然后查看内核的信息。
<div><strong>精选留言（5）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/0f/5e/96/a03175bc.jpg" width="30px"><span>莫名</span> 👍（12） 💬（3）<div>关于思考题，想到一个比较笨拙的方法：gdb + qemu 调试内核。先进入虚拟机在某个内核函数上注册一个 kprobe，然后 gdb 远程调试内核，查看该内核函数的汇编指令（disass）是否被替换。

应该有更简单的方法，这方面了解不深。</div>2021-02-05</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1f/68/12/031a05c3.jpg" width="30px"><span>A免帅叫哥</span> 👍（0） 💬（1）<div>看到内核还有一个kretprobe_example</div>2021-08-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/47/00/3202bdf0.jpg" width="30px"><span>piboye</span> 👍（0） 💬（0）<div>kprobe 用int3的方式性能会差吧，为神马不替换callq的指令呢？</div>2023-03-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/18/b7/24/17f6c240.jpg" width="30px"><span>janey</span> 👍（0） 💬（0）<div>一下子讲清楚了tracepoint核kprobe函数的区别，谢谢老师！另外eBPF还涉及了uprobe和USDT这两种类型又是啥意思呢？</div>2022-11-18</li><br/><li><img src="" width="30px"><span>Geek_e4cf2e</span> 👍（0） 💬（0）<div>crash来查看很方便</div>2021-09-19</li><br/>
</ul>