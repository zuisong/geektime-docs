你好，我是倪朋飞。

在第 6 讲 [各类 eBPF 程序的触发机制及其应用场景](https://time.geekbang.org/column/article/483364) 中，我曾讲过 eBPF 程序的分类以及每种不同类型程序的使用场景。而在后续的实战进阶篇中，也通过多讲课程详细为你讲述了各种类型 eBPF 程序的开发方法。但是，无论在课程留言区还是微信讨论群中，依然有很多同学不清楚如何从零开发一个 eBPF 程序，特别是开发的第一步———到底该如何为要开发的 eBPF 程序设置参数。

今天，我就带你一起来深入探讨这个问题，看看不同类型 eBPF 程序的参数到底是如何设置的，它们的返回值又代表着什么含义。

## 再谈 eBPF 程序

我相信你一定已经开发了很多不同的 eBPF 程序了，也已经跟随我们课程学习了很多常用 eBPF 程序的使用方法。简单来说，eBPF 程序就是通过 C 语言开发并可被编译为 eBPF 字节码的程序，而这个程序中最核心的就是挂载到内核态或用户态事件的 eBPF 函数。

在开发 eBPF 程序过程中，我想你一定已经体会到 eBPF 中的函数远没有普通程序中的函数那么灵活，其编程模型与普通程序有着明显的不同。与普通程序相比，eBPF 程序不仅无法随意调用各种库函数，而且其函数功能相对受限。这些限制主要源于 eBPF 的设计理念和安全考虑。

eBPF 指令集定义了严格的函数调用约定，所有 eBPF 程序都必须遵循，以确保在内核环境中的安全和高效运行。这些约定包括：
<div><strong>精选留言（1）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/27/fb/f7/88ab6f83.jpg" width="30px"><span>进击的Lancelot</span> 👍（1） 💬（0）<div>XDP 程序类型老师已经讲过，这里不再赘述。
TC 类型的返回值有 TC_ACT_OK（放行） 和 TC_ACT_SHOT（丢弃），可以参考 
定义：https:&#47;&#47;elixir.bootlin.com&#47;linux&#47;v6.8&#47;source&#47;samples&#47;bpf&#47;net_shared.h#L17
示例：&#47;samples&#47;bpf&#47;tc_l2_redirect_kern.c

至于 kprobe，大部分情况下返回值都是和 map 访问相关的错误处理，以 &#47;samples&#47;bpf&#47;tracex6.bpf.c 为例，具体可以参考 get_map_perf_counter 实现（https:&#47;&#47;elixir.bootlin.com&#47;linux&#47;v6.8&#47;source&#47;kernel&#47;trace&#47;bpf_trace.c#L549）  
</div>2024-12-27</li><br/>
</ul>