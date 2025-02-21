你好，我是倪朋飞。

前面两讲，我带你梳理了查询 eBPF 跟踪点的常用方法，并以短时进程的跟踪为例，通过 bpftrace、BCC 和 libbpf 等三种方法实现了短时进程的跟踪程序。学完这些内容，我想你已经可以根据自己的实际需求，查询到内核跟踪点或内核函数，并自己开发一个 eBPF 内核跟踪程序。

也许你想问：我们能不能利用与跟踪内核状态类似的方法，去跟踪用户空间的进程呢？答案是肯定的。只要把内核态跟踪使用的 `kprobe` 和 `tracepoint` 替换成 `uprobe` ，或者用户空间定义的静态跟踪点（User Statically Defined Tracing，简称 USDT），并找出用户进程需要跟踪的函数，作为 eBPF 程序的挂载点，你就可以去跟踪用户进程的内部状态。

那具体该怎么做呢？今天，我就带你一起来看看，如何使用 eBPF 去跟踪用户进程的执行状态。

## 如何查询用户进程跟踪点？

在 [07讲](https://time.geekbang.org/column/article/484207) 中我曾提到，在跟踪内核的状态之前，你需要利用内核提供的调试信息查询内核函数、内核跟踪点以及性能事件等。类似地，在跟踪应用进程之前，你也需要知道**这个进程所对应的二进制文件中提供了哪些可用的跟踪点**。那么，从哪里可以找到这些信息呢？如果你使用 GDB 之类的应用调试过程序，这时应该已经想到了，那就是**应用程序二进制文件中的调试信息**。
<div><strong>精选留言（15）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/0f/5e/96/a03175bc.jpg" width="30px"><span>莫名</span> 👍（10） 💬（1）<div>1. 跟踪编译型语言应用程序以 Bash Shell 作为例子，觉得有些容易与解释型语言混淆。解释型语言的特征是解释程序自身为编译型程序，利用自身内置的函数进行语法分析和执行，Bash readline 函数的功能即是如此。以编译型语言 Golang helloworld 程序使用 uprobes 或者开源的 Nginx 使用 USDT 可能更恰当一些。 

2. 思考题完整的 BCC 追踪程序：

----------- python_functions.c -------------

#include &lt;uapi&#47;linux&#47;ptrace.h&gt;

struct data_t {
	char filename[128];
	char funcname[64];
	int lineno;
};
BPF_PERF_OUTPUT(events);

int print_functions(struct pt_regs *ctx)
{
	uint64_t argptr;
	struct data_t data = { };

	bpf_usdt_readarg(1, ctx, &amp;argptr);
	bpf_probe_read_user(&amp;data.filename, sizeof(data.filename), (void *)argptr);
	bpf_usdt_readarg(2, ctx, &amp;argptr);
	bpf_probe_read_user(&amp;data.funcname, sizeof(data.funcname), (void *)argptr);
	bpf_usdt_readarg(3, ctx, &amp;data.lineno);

	events.perf_submit(ctx, &amp;data, sizeof(data));

	return 0;
};

----------- python_functions.py -------------

#!&#47;usr&#47;bin&#47;python3

import sys
from bcc import BPF, USDT

if len(sys.argv) &lt; 2:
    print(&quot;Usage: %s &lt;tracee_pid&gt;&quot; % sys.argv[0])
    sys.exit(1)

u = USDT(pid=int(sys.argv[1]))
u.enable_probe(probe=&quot;function__entry&quot;, fn_name=&quot;print_functions&quot;)
b = BPF(src_file=&quot;python_functions.c&quot;, usdt_contexts=[u])


def print_event(cpu, data, size):
    event = b[&quot;events&quot;].event(data)
    printb(&quot;%-9s %-6d %s&quot; % (event.filename, event.lineno, event.funcname))


print(&quot;%-9s %-6s %s&quot; % (&quot;FILENAME&quot;, &quot;LINENO&quot;, &quot;FUNCTION&quot;))

b[&quot;events&quot;].open_perf_buffer(print_event)
while True:
    try:
        b.perf_buffer_poll()
    except KeyboardInterrupt:
        exit()</div>2022-02-04</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTKwGurTWOiaZ2O2oCdxK9kbF4PcwGg0ALqsWhNq87hWvwPy8ZU9cxRzmcGOgdIeJkTOoKfbxgEKqrg/132" width="30px"><span>ZR2021</span> 👍（4） 💬（2）<div>老师，跟踪用户态程序的时候还有512字节的限制吗</div>2022-02-04</li><br/><li><img src="" width="30px"><span>Geek3340</span> 👍（2） 💬（1）<div>sudo apt install bash-dbgsym 命令，执行后找不到dbgsym包的，可以参考这篇文章
https:&#47;&#47;cloud.tencent.com&#47;developer&#47;article&#47;1637887</div>2022-03-20</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTJlaNica7xRH6LlMNJtrbK0toc1od8YdqLZOD2AbnOZ2QyKC13gvrrL9cOx5dyYNcsHnJkR6K4ibxZQ/132" width="30px"><span>Geek_59a6f9</span> 👍（1） 💬（1）<div>用户态进程跟踪是不是使用frida效果更好？</div>2022-02-04</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1a/f4/f2/9a28aaff.jpg" width="30px"><span>郑小凯</span> 👍（0） 💬（1）<div>老师，咨询下ibm jdk，使用bcc的话有办法么？</div>2022-12-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/25/6f/a7/565214bc.jpg" width="30px"><span>│．Sk</span> 👍（0） 💬（1）<div>老师您好，请教一下

1. 执行了 strip 命令删除了  .symtab  的二进制文件，是否就“不能”用 .symtab 里的符号执行 bpftrace -e &#39;uretprobe:&#47;usr&#47;bin&#47;bash:符号  {...}&#39; ？

2. 如果 1. 中的理解是对的，那么上面的 &#47;usr&#47;bin&#47;bash 的 .symtab 实际已经被 strip 了，但是还能执行上面的 trace 是否是因为 BCC 会用 &#47;usr&#47;bin&#47;bash 的 build id 去 &#47;usr&#47;lib&#47;debug&#47;.build-id&#47; 关联相应的符号表，然后再用符号找到函数地址？

谢谢老师！</div>2022-03-05</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1f/85/e3/7df90bff.jpg" width="30px"><span>王恒</span> 👍（0） 💬（3）<div>某线程CPU占用率过高，通过perf工具生成了该线程的火焰图。发现该线程的系统函数占比较高，但是又无法查到这些系统函数的调用堆栈。（火焰图中，ia32_sysenter_target函数占比约6%，sysexit_from_sys_call函数占比约9%。）

特别想搞懂这些内核函数是什么时候被调用的，调用堆栈是怎么样的，为什么耗时这么久。所以特地来学习ebpf，希望边学边解决工作中的实际问题。</div>2022-03-05</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/WgRsoJMxcTMcDkRlR59jCDLux2JDdtz1G8Ophe3a7EnhP8lqOdFw8F7sURXkRTYXibzVicozrQ8HFYj578myJ0CA/132" width="30px"><span>行所当行</span> 👍（0） 💬（0）<div>老师您好，bash历史执行命令可以用history来快捷查看，那么在审计操作系统用户行为和操作系统安全方面，ebpf还有什么典型的应用场景？</div>2024-10-09</li><br/><li><img src="" width="30px"><span>Geek_722e86</span> 👍（0） 💬（0）<div>老师， 

除了符号表之外，理论上你可以把 uprobe 插桩到二进制文件的任意地址。不过这要求你对应用程序 ELF 格式的地址空间非常熟悉，并且具体的地址会随着应用的迭代更新而发生变化。所以，在需要跟踪地址的场景中，一定要记得去 ELF 二进制文件动态获取地址信息。

-----------
请问， 这个应该怎么操作呢？ 加入我OS上的bash就是没有符号信息。 我还是想挂载readline函数，怎么办呢？

# 挂载uretprobeb.attach_uretprobe(name=&quot;&#47;usr&#47;bin&#47;bash&quot;, sym=&quot;readline&quot;, fn_name=&quot;bash_readline&quot;)
这个参数具体是怎么写？


sudo bpftrace -e &#39;uretprobe:&#47;usr&#47;bin&#47;bash:readline { printf(&quot;User %d executed \&quot;%s\&quot; command\n&quot;, uid, str(retval)); }&#39;
这个参数怎么写？
</div>2023-06-01</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/cd/db/7467ad23.jpg" width="30px"><span>Bachue Zhou</span> 👍（0） 💬（0）<div>好奇这种 uprobe 是怎么做到的？只是调用应用程序里另一个函数为什么会被内核介入？如果 epbf 程序执行时间较长，是不是应用程序会等待 ebpf 执行完再继续执行？</div>2023-04-04</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/cd/db/7467ad23.jpg" width="30px"><span>Bachue Zhou</span> 👍（0） 💬（0）<div>其实现在的解释型脚本语言，比如 Python，Ruby 之类的语言，各自都有自己的字节码，虚拟机和 JIT，本质上和 Java 没有太大差异，只是不把字节码保存下来而已。</div>2023-04-04</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/eb/4f/6a97b1cd.jpg" width="30px"><span>猪小擎</span> 👍（0） 💬（0）<div>plan 9对应的不是elf吗？怎么和abi有关系？</div>2023-03-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/25/3c/92/81fa306d.jpg" width="30px"><span>张Dave</span> 👍（0） 💬（0）<div>老师，能详细讲解一下USDT吗？怎么定义？怎么使用？怎么生效？</div>2022-10-03</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/23/c4/91/a017bf72.jpg" width="30px"><span>coconut</span> 👍（0） 💬（1）<div>&#47;usr&#47;bin&#47;bash 即使没有用 debuginfo-install 安装调试符号，也能执行 bpftrace -e &#39;uretprobe:&#47;usr&#47;bin&#47;bash:readline { printf(&quot;User %d executed \&quot;%s\&quot; command\n&quot;, uid, str(retval)); }&#39;</div>2022-07-25</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/32/a8/d5bf5445.jpg" width="30px"><span>郑海成</span> 👍（0） 💬（3）<div>sudo bpftrace -l &#39;*:&#47;usr&#47;bin&#47;python3:*&#39; 执行后没有任何跟踪点信息</div>2022-04-12</li><br/>
</ul>