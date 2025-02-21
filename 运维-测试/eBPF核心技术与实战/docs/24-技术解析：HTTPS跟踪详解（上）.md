你好，我是倪朋飞。

上一讲我带你回顾了 eBPF 在 2023 年的旅程。过去一年，Linux 内核不仅大幅增强了 eBPF 的功能特性，新增了通用迭代器、uprobe 多挂载、套接字销毁、自定义对象、红黑树数据结构等一系列的新特性，eBPF 的生态系统和实践也是遍地开花，很多开源项目都在去年达到了生产可用的稳定版本。特别是在云原生监控领域，由于无需对应用程序进行任何修改，eBPF 就成为无侵入监控方案的最佳选择。而在云原生这类典型的分布式系统中，HTTP/HTTPS 等网络请求的跟踪又尤为重要，它们是我们了解分布系统中多个系统组件如何通过网络进行交互的核心。

那么，如何对 HTTP 网络包进行跟踪，又如何跟踪加密的 HTTPS 网络包呢？今天，我就带你一起去看看这两个问题。 由于篇幅比较长，本次课程的内容将分为两篇，今天的内容是上篇。

## HTTP/HTTPS 协议回顾

要进行 HTTP/HTTPS 的跟踪，就需要首先了解它们的工作原理，特别是网络包的数据结构。你还记得 HTTP/HTTPS 协议是怎么工作的吗？你可以停下回忆一下再来继续下面的内容。

有没有想起来呢？没有想起来也没关系，接下来我带你一起回忆一下。

### HTTP 协议

HTTP 是超文本传输协议（HyperText Transfer Protocol）的简称，是用于分布式协作的应用层协议。HTTP 工作在 TCP/IP 模型之上，通常使用 80 端口，是万维网数据通信的基础。
<div><strong>精选留言（1）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/27/fb/f7/88ab6f83.jpg" width="30px"><span>进击的Lancelot</span> 👍（0） 💬（0）<div>按照上述文章中的代码编写，在加载 ebpf 程序时会产生错误信息：
139: (85) call bpf_skb_load_bytes#26
R4 invalid zero-sized read: u64=[0,99]
processed 159 insns (limit 1000000) max_states_per_insn 1 total_states 12 peak_states 12 mark_read 5
-- END PROG LOAD LOG --
libbpf: prog &#39;http_trace&#39;: failed to load: -13
libbpf: failed to load object &#39;http_trace_bpf&#39;
libbpf: failed to load BPF skeleton &#39;http_trace_bpf&#39;: -13
Failed to open and load BPF skeleton

产生这个错误信息的原因是因为 bpf_skb_load_bytes 的第四个参数必须是常量类型，而 read_length 是变量。这里分享一下找到这个原因的过程：
1. 在对应版本的内核当中找到这个错误信息 invalid zero-sized read，通过错误信息定位到 kfunc：check_mem_size_reg
2. 通过 bpftrace 追踪 check_mem_size_reg 返回值非零时的 kstack 。执行 sudo bpftrace -e &#39;kretprobe:check_mem_size_reg &#47;retval != 0&#47; { print(kstack());}&#39;, 得到以下调用栈：
        check_func_arg+1013
        check_helper_call.isra.0+514
        do_check+2778
        do_check_common+486
        bpf_check+1934
        bpf_prog_load+1733
        __sys_bpf+1381
        __x64_sys_bpf+26
        x64_sys_call+6552
        do_syscall_64+127
        entry_SYSCALL_64_after_hwframe+120
3. 通过阅读代码或者 faddr2line 找到 check_func_arg+1013 对应的位置, 即以下代码：
case ARG_CONST_SIZE:
		err = check_mem_size_reg(env, reg, regno, false, meta);
4. 通过 ARG_CONST_SIZE 可以找到 bpf_arg_type 定义，进而找到 bpf_func_proto。 通过注释，可以知道 bpf_func_proto 是用来帮助 verifier 对一个 ebpf helper func 进行验证的
5. 通过 bpf_func_proto 和对应的 helper bpf_skb_load_bytes 可以找到以下定义：
static const struct bpf_func_proto bpf_skb_load_bytes_proto = {
	.func		= bpf_skb_load_bytes,
	.gpl_only	= false,
	.ret_type	= RET_INTEGER,
	.arg1_type	= ARG_PTR_TO_CTX,
	.arg2_type	= ARG_ANYTHING,
	.arg3_type	= ARG_PTR_TO_UNINIT_MEM,
	.arg4_type	= ARG_CONST_SIZE,
};
至此可以确定 bpf_skb_load_bytes 要求第四个参数 len 的类型必须是常量类型</div>2024-12-31</li><br/>
</ul>