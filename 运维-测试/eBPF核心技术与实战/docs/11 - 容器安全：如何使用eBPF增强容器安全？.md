你好，我是倪朋飞。

上一讲，我以最常见的网络丢包为例，带你一起梳理了 eBPF 所提供的网络功能特性，并教你使用 bpftrace 开发了一个跟踪内核网络协议栈的 eBPF 程序。虽然 eBPF 起源于网络过滤，并且网络过滤也是 eBPF 应用最为广泛的一个领域，但其实 eBPF 的应用已经远远超出了这一范畴。故障诊断、网络优化、安全控制、性能监控等，都已是 eBPF 的主战场。

随着容器和云原生技术的普及，由于容器天生共享内核的特性，容器的安全和隔离就是所有容器平台头上的“紧箍咒”。因此，如何快速定位容器安全问题，如何确保容器的隔离，以及如何预防容器安全漏洞等，是每个容器平台都需要解决的头号问题。

既然容器是共享内核的，这些安全问题的解决自然就可以从内核的角度进行考虑。除了容器自身所强依赖的命名空间、cgroups、Linux 权限控制 Capabilities 之外，可以动态跟踪和扩展内核的 eBPF 就成为了安全监控和安全控制的主要手段之一。 Sysdig、Aqua Security、Datadog 等业内知名的容器安全解决方案，都基于 eBPF 构建了丰富的安全特性。

那么，到底如何使用 eBPF 来监控容器的安全问题，又如何使用 eBPF 阻止容器中的恶意行为呢？今天，我就带你一起来看看如何借助 eBPF 来增强容器安全。
<div><strong>精选留言（6）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/0f/5e/96/a03175bc.jpg" width="30px"><span>莫名</span> 👍（14） 💬（1）<div>另外分享一个经验，结构体 nsproxy 的 net 字段（代表进程所在的网络命名空间）在追踪网络包在宿主机 -&gt; 容器传递过程时尤其有用，可以比较清楚的看到网络包从宿主机的网络命名空间传递到容器独立的网络命名空间之中，协助更好的理解容器网络模型。（把网络设备名字也打印出来会更好。）

倪老师文中的示例程序 execsnoop-container.bt 使用了结构体 nsproxy 的 pid_ns_for_children 获取 PID 命名空间，稍微改动了一下，换成 NET 命名空间，把具体的 id 打出来。

输出示例（shell1 执行 docker run ... bash, shell2 追踪 execve 事件，可以看到 bash 进程在一个新的网络命名空间下执行。）：

shell 1 # docker exec -ti vibrant_jepsen bash
root@c340ba5cb9de:&#47;#

shell2 # # .&#47;execve.bt
Attaching 3 probes...
NETNS          CONTAINER              PPID     PID     COMM         ARGS
4026531993   VM-56-211-centos   799603 181059 bash            docker exec -ti vibrant_jepsen bash
...
4026532351   c340ba5cb9de         181078   181083 runc:[2:INIT]   bash

具体源码：
======================================

#!&#47;usr&#47;bin&#47;env bpftrace

#include &lt;linux&#47;sched.h&gt;
#include &lt;linux&#47;nsproxy.h&gt;
#include &lt;linux&#47;utsname.h&gt;
&#47;&#47;#include &lt;linux&#47;pid_namespace.h&gt;
#include &lt;net&#47;net_namespace.h&gt;

BEGIN 
{
  printf(&quot;%-12s %-18s %-6s %-6s %-16s %s\n&quot;, &quot;NETNS&quot;, &quot;CONTAINER&quot;, &quot;PPID&quot;, &quot;PID&quot;, &quot;COMM&quot;, &quot;ARGS&quot;);
}

tracepoint:syscalls:sys_enter_execve,
tracepoint:syscalls:sys_enter_execveat
{
  $task = (struct task_struct *)curtask;
  $netns = $task-&gt;nsproxy-&gt;net_ns-&gt;ns.inum;
  &#47;&#47;$pidns = $task-&gt;nsproxy-&gt;pid_ns_for_children-&gt;ns.inum;
  $cname = $task-&gt;nsproxy-&gt;uts_ns-&gt;name.nodename;
  printf(&quot;%-12ld %-18s %-6d %-6d %-16s&quot;, (uint64)$netns, $cname, curtask-&gt;parent-&gt;pid, pid, comm);
  join(args-&gt;argv);
}</div>2022-02-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/41/38/4f89095b.jpg" width="30px"><span>写点啥呢</span> 👍（5） 💬（1）<div>本节课是关于eBPF在安全方面的使用，微博上看到有人发的这个rookit：https:&#47;&#47;weibo.com&#47;tv&#47;show&#47;1034:4718242451882158?from=old_pc_videoshow，因此我对eBPF如何保证自身安全性很好奇，想请教下老师对于系统来说eBPF是一个两面利器，它自身设计与实现，还有在使用中该如何注意避免引入安全问题呢？

另外像bpf_send_signal辅助函数能够通过信号杀死进程，这是不是一种类似变成语言的unsafe方法，应该在实际中谨慎使用呢？

谢谢老师。</div>2022-02-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/5e/96/a03175bc.jpg" width="30px"><span>莫名</span> 👍（3） 💬（1）<div>1、曾使用过 sysdig，老版本通过插入内核模块的方式进行安全审计。后来 sysdig 支持了 eBPF driver，主要通过追踪系统调用分析可能的安全隐患。sysdig eBPF driver 实现比较简单，一共十几个 program，统一放在 probe.c 源文件，里面的思路借鉴下还是不错的。
2、觉得需要在 bash 自身上做手脚，比如把 bash 软链接到一个脚本文件，记录下 bash 执行记录，然后 直接 exit。或者修改 bash 配置文件 .bashrc，文件末尾直接 exit。两种方法都有局限性，如果被识破可以很容易绕过去。</div>2022-02-10</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTIsEia7TcYPiaO53QIydh4tPonwnpktgrhLeJqg4sNa8s11XNVTVajrI9jKibHs0FYn0EW8d8t3EM8ibQ/132" width="30px"><span>Geek_89541f</span> 👍（0） 💬（2）<div>请问我在阿里云的虚拟机（centos系统，内核版本4.18)中使用ip link加载xdp程序，若指定xdpdrv模式会报错，xdpgeneric可以。这是为啥？虚拟网卡只能使用generic模式吗？这样性能不能满足生产需求。</div>2022-02-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/cd/db/7467ad23.jpg" width="30px"><span>Bachue Zhou</span> 👍（0） 💬（0）<div>如果运行 bpftrace 找不到 BEGIN symbol，例如出现：
ERROR: Could not resolve symbol: &#47;proc&#47;self&#47;exe:BEGIN_trigger
就运行 
sudo apt install bpftrace-dbgsym
就行了哈</div>2023-04-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/32/a8/d5bf5445.jpg" width="30px"><span>郑海成</span> 👍（0） 💬（0）<div>https:&#47;&#47;elixir.bootlin.com&#47;linux&#47;v5.13&#47;source&#47;include&#47;linux&#47;sched.h#L657 老师，bootlin这个网站是有什么要求吗？为什么我所有的代码link都显示 &quot;This file does not exist.&quot;呢？</div>2022-04-13</li><br/>
</ul>