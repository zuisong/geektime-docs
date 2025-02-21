你好，我是倪朋飞。

上一讲，我带你一起梳理了 eBPF 程序跟内核交互的基本方法。一个完整的 eBPF 程序通常包含用户态和内核态两部分：用户态程序通过 BPF 系统调用，完成 eBPF 程序的加载、事件挂载以及映射创建和更新，而内核态中的 eBPF 程序则需要通过 BPF 辅助函数完成所需的任务。

在上一讲中我也提到，并不是所有的辅助函数都可以在 eBPF 程序中随意使用，不同类型的 eBPF 程序所支持的辅助函数是不同的。那么，eBPF 程序都有哪些类型，而不同类型的 eBPF 程序又有哪些独特的应用场景呢？今天，我就带你一起来看看。

## eBPF 程序可以分成几类？

eBPF 程序类型决定了一个 eBPF 程序可以挂载的事件类型和事件参数，这也就意味着，内核中不同事件会触发不同类型的 eBPF 程序。

根据内核头文件 [include/uapi/linux/bpf.h](https://elixir.bootlin.com/linux/v5.13/source/include/uapi/linux/bpf.h#L908) 中 `bpf_prog_type` 的定义，Linux 内核 v5.13 已经支持 30 种不同类型的 eBPF 程序（注意， `BPF_PROG_TYPE_UNSPEC`表示未定义）：

```c++
enum bpf_prog_type {
	BPF_PROG_TYPE_UNSPEC, /* Reserve 0 as invalid program type */
	BPF_PROG_TYPE_SOCKET_FILTER,
	BPF_PROG_TYPE_KPROBE,
	BPF_PROG_TYPE_SCHED_CLS,
	BPF_PROG_TYPE_SCHED_ACT,
	BPF_PROG_TYPE_TRACEPOINT,
	BPF_PROG_TYPE_XDP,
	BPF_PROG_TYPE_PERF_EVENT,
	BPF_PROG_TYPE_CGROUP_SKB,
	BPF_PROG_TYPE_CGROUP_SOCK,
	BPF_PROG_TYPE_LWT_IN,
	BPF_PROG_TYPE_LWT_OUT,
	BPF_PROG_TYPE_LWT_XMIT,
	BPF_PROG_TYPE_SOCK_OPS,
	BPF_PROG_TYPE_SK_SKB,
	BPF_PROG_TYPE_CGROUP_DEVICE,
	BPF_PROG_TYPE_SK_MSG,
	BPF_PROG_TYPE_RAW_TRACEPOINT,
	BPF_PROG_TYPE_CGROUP_SOCK_ADDR,
	BPF_PROG_TYPE_LWT_SEG6LOCAL,
	BPF_PROG_TYPE_LIRC_MODE2,
	BPF_PROG_TYPE_SK_REUSEPORT,
	BPF_PROG_TYPE_FLOW_DISSECTOR,
	BPF_PROG_TYPE_CGROUP_SYSCTL,
	BPF_PROG_TYPE_RAW_TRACEPOINT_WRITABLE,
	BPF_PROG_TYPE_CGROUP_SOCKOPT,
	BPF_PROG_TYPE_TRACING,
	BPF_PROG_TYPE_STRUCT_OPS,
	BPF_PROG_TYPE_EXT,
	BPF_PROG_TYPE_LSM,
	BPF_PROG_TYPE_SK_LOOKUP,
};
```
<div><strong>精选留言（16）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/2a/d4/99/594e35c2.jpg" width="30px"><span>YF</span> 👍（15） 💬（1）<div>你是怎么理解 eBPF 程序类型的呢？

eBPF 对应与内核的事件类型，犹如订阅同类消息事件，内核发现对应的事件，则通知订阅者处理。</div>2022-01-30</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/87/06/bedf7932.jpg" width="30px"><span>阿立</span> 👍（6） 💬（3）<div>作者大佬，xdp是一个内核网络处理模块，还是网络包进入协议栈之前的事件钩子点呢？ tc呢？</div>2022-02-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/9c/f3/e01dfe3a.jpg" width="30px"><span>于競</span> 👍（4） 💬（1）<div>看了上面介绍的网络类型的eBPF程序，好奇可不可以用来开发流量复制工具呢</div>2022-02-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/31/5a/e3/cfc48236.jpg" width="30px"><span>白璐</span> 👍（1） 💬（1）<div>老师，ebpf 可以阻断进程的行为吗，例如某个进程调用了write 系统调用 然后 我应用ebpf阻断调用 不让这个进程调用write系统调用 。 这个可以用ebpf实现吗</div>2023-02-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1f/0b/6e/e0409a35.jpg" width="30px"><span>XYS</span> 👍（1） 💬（1）<div>原理：钩子就是系统在各个数据处理路径上放置的一个埋点（例如：map[int]func）,我们需要确定int值（枚举类型）和处理函数，处理路径上会查看map[特定值]下是否有函数，有就执行。
应用：熟悉各个枚举值的位置（既作用）就能在实际工作中利用该技术解决实际问题。</div>2023-02-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/18/b7/24/17f6c240.jpg" width="30px"><span>janey</span> 👍（1） 💬（1）<div>我理解ebpf分类，可以分为tracepoint,kprobe,uprobe,USDT等</div>2022-11-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/91/21/d38d8391.jpg" width="30px"><span>任智杰byte</span> 👍（1） 💬（1）<div>如何扩展程序类型呢？</div>2022-03-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/76/b0/14fec62f.jpg" width="30px"><span>不了峰</span> 👍（1） 💬（1）<div>打卡</div>2022-01-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/19/1d/d2b6e006.jpg" width="30px"><span>火火寻</span> 👍（0） 💬（1）<div>老师，问下，如果想要做业务层的流量控制，比如dubbo请求部分黑名单不让进来，使用哪种合适？
</div>2022-03-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/70/ab/7a7399a7.jpg" width="30px"><span>tj.•</span> 👍（1） 💬（0）<div>老师，使用cilium代替iptables之后，pod访问一个service ip，是在哪个hook做DNAT成endpoint pod ip的？</div>2022-10-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/2d/b1/60/23c03681.jpg" width="30px"><span>一</span> 👍（1） 💬（1）<div>老师，我想问一下，比如我想在系统弹窗时插装，怎么找到系统弹窗这个hook点呢，比如SEC（“uprobe&#47;这个地方应该填什么呢，或者说在哪里有这个uprobe下面hook点的列表呢”）</div>2022-05-02</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/23/73/de/2d9bc244.jpg" width="30px"><span>彬</span> 👍（1） 💬（0）<div>老师后续会有更全的环境搭建吗？比如升级内核，如果不能直接apt安装bcc等需要采取源码编译等情况，如何在本地环境中编译然后发布到生产环境等情况讲解或者资料</div>2022-04-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/ed/1a/269eb3d6.jpg" width="30px"><span>cfanbo</span> 👍（1） 💬（2）<div>怎么知道网卡是否支持XDP？</div>2022-03-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/22/f4/9fd6f8f0.jpg" width="30px"><span>核桃</span> 👍（0） 💬（0）<div>请教一下如果是内核文件系统方面，我想给zfs或者ext4的write或者read函数进行监控，知道文件系统的版本，也知道一些对应的函数名称，有没有类似的相关工具可以实现？还是要自己根据版本写代码？</div>2023-10-02</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/17/24/b1/9462135f.jpg" width="30px"><span>重庆杜员外</span> 👍（0） 💬（0）<div>想要用ebpf实现一个http流量分析和统计的旁路系统，线上内核版本5.4，请问老师有什么好的建议吗</div>2023-04-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/2c/7b/7a/70c904e9.jpg" width="30px"><span>Lime</span> 👍（0） 💬（0）<div>ePBF有没有办法修改内核传进来的参数</div>2022-07-13</li><br/>
</ul>