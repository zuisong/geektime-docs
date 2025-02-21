你好，我是倪朋飞。

上一讲，我带你一起梳理了 eBPF 在内核中的实现原理，以及 BPF 指令的具体格式。

用高级语言开发的 eBPF 程序，需要首先编译为 BPF 字节码，然后借助 bpf 系统调用加载到内核中，最后再通过性能监控等接口与具体的内核事件进行绑定。这样，内核的性能监控模块才会在内核事件发生时，自动执行我们开发的 eBPF 程序。

那么，eBPF 程序到底是如何跟内核事件进行绑定的？又该如何跟内核中的其他模块进行交互呢？今天，我就带你一起看看 eBPF 程序的编程接口。

## BPF 系统调用

如下图（图片来自[brendangregg.com](https://www.brendangregg.com/ebpf.html)）所示，一个完整的 eBPF 程序通常包含用户态和内核态两部分。其中，用户态负责 eBPF 程序的加载、事件绑定以及 eBPF 程序运行结果的汇总输出；内核态运行在 eBPF 虚拟机中，负责定制和控制系统的运行状态。

![图片](https://static001.geekbang.org/resource/image/a7/6a/a7165eea1fd9fc24090a3a1e8987986a.png?wh=1500x550)

对于用户态程序来说，我想你已经了解，**它们与内核进行交互时必须要通过系统调用来完成**。而对应到 eBPF 程序中，我们最常用到的就是 [bpf 系统调用](https://man7.org/linux/man-pages/man2/bpf.2.html)。

在命令行中输入 `man bpf` ，就可以查询到 BPF 系统调用的调用格式：

```plain
#include <linux/bpf.h>

int bpf(int cmd, union bpf_attr *attr, unsigned int size);
```
<div><strong>精选留言（16）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/0f/5e/96/a03175bc.jpg" width="30px"><span>莫名</span> 👍（34） 💬（2）<div>倪老师留的思考题比较基础，尝试从另一个角度做下觉得有趣的对比：

1、bpf 系统调用一定程度上参考了 perf_event_open 设计，bpf_attr、perf_event_attr 均包含了大量 union，用于适配不同的 cmd 或者性能监控事件类型。因此，bpf、perf_event_open 接口看似简单，其实是大杂烩。

bpf(int cmd, union bpf_attr *attr, ...) 
perf_event_open(struct perf_event_attr *attr, ...)

2、bpftool 命令设计风格重度参考了 iproute2 软件包中的 ip 命令，用法基本上一致。

Usage: bpftool [OPTIONS] OBJECT { COMMAND | help }
Usage: ip [ OPTIONS ] OBJECT { COMMAND | help }

无论内核开发还是工具开发，都可以看到设计思路借鉴的影子。工作之余不妨多些学习与思考，也许就可以把大师们比较好的设计思路随手用于手头的任务之中。</div>2022-01-26</li><br/><li><img src="" width="30px"><span>Geek_e8988c</span> 👍（9） 💬（1）<div>飞哥，你好，看完前两章感觉比较迷糊。没能做到学以致用，或者说举一反三。
例如第一个ebpf程序，通过trace open系统调用来监控应用的open动作。
那我实际中，有没有什么快速的方案&#47;套路来完成一些其他的trace，例如我想知道监控那些程序使用了socket&#47;bind(尤其适用于有些短暂进程使用udp发送了一些报文就立马退出了）。
当我想新增一个trace事件，我的.c需要去包含那些头文件，我的.py需要跟踪那个系统调用。
这些头文件与系统调用在哪可以找到，如果去找？

希望飞哥大佬能给个大体的框架，思路，谢谢</div>2022-01-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/41/38/4f89095b.jpg" width="30px"><span>写点啥呢</span> 👍（4） 💬（1）<div>想请教下老师关于bpf内核态程序的成名周期，比如前几节课的例子，如果我通过ctrl-c终端用户态程序的时候在bpf虚拟机会发生什么呢？我理解应该会结束已经加载的bpf指令，清理map之类的资源等等，具体会有哪些，这些操作是如何在我们程序中自动插入和实现，请老师指点下。</div>2022-01-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/76/b0/14fec62f.jpg" width="30px"><span>不了峰</span> 👍（2） 💬（1）<div>BPF 系统调用  --&gt; 发生在 用户态
BPF 辅助函数  --&gt; 内核态
---
root@ubuntu-impish:&#47;proc# bpftool perf
pid 38110  fd 6: prog_id 572  kprobe  func do_sys_openat2  offset 0

root@ubuntu-impish:&#47;proc# ps -ef|grep 38110
root       38110   38109  0 03:41 pts&#47;2    00:00:02 python3 .&#47;trace_open.py</div>2022-01-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/47/00/3202bdf0.jpg" width="30px"><span>piboye</span> 👍（1） 💬（3）<div>老师， bpf 的 map 怎么移除啊？ 没看到 bpftools 的命令</div>2022-03-15</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTJlaNica7xRH6LlMNJtrbK0toc1od8YdqLZOD2AbnOZ2QyKC13gvrrL9cOx5dyYNcsHnJkR6K4ibxZQ/132" width="30px"><span>Geek_59a6f9</span> 👍（1） 💬（1）<div>在高版本内核编译运行的ebpf程序，移植到低版本也能直接运行吗？低版本的libbpf 如何感知到高版本内核的修改，从而预定义不同内核版本的数据结构吗？</div>2022-02-04</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/25/6f/a7/565214bc.jpg" width="30px"><span>│．Sk</span> 👍（0） 💬（1）<div>倪老师好，

想请教一下，在支持 BTF 的内核中，利用 CO-RE 编译出的 ebpf 程序可执行文件，直接 copy 到低版本不支持 BTF 的内核版本的系统上能正常运行吗？ 谢谢！</div>2022-12-31</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1c/bb/50/c8ebd5e1.jpg" width="30px"><span>MoGeJiEr🐔</span> 👍（1） 💬（0）<div>BTF那块是不是没说完阿？不是只介绍了可以使用bpftool生成vmlinux.h头文件嘛？ 怎么后面CO-RE就可以借助BTF的调试信息？这个调试信息哪里来？一头雾水。</div>2022-08-15</li><br/><li><img src="" width="30px"><span>woJA1wCgAAbjKldokPvO1h9ZEJTUP8ug</span> 👍（1） 💬（0）<div>老师，结构化的数据需要怎么看，bpftool map dump id mapid和bpftool map dump name mapname结果都是一样的16进制数</div>2022-04-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/52/17/e3015ba5.jpg" width="30px"><span>helloworld</span> 👍（0） 💬（0）<div>老师，请问下ebpf对系统内核的要求，可以通过容器的操作系统来屏蔽掉对吗？ 不要求物理机节点的内核版本吧？ </div>2024-03-26</li><br/><li><img src="" width="30px"><span>Geek_94444c</span> 👍（0） 💬（0）<div>&quot;eBPF 程序最多可以访问 64 个不同的 BPF 映射&quot; 
1. 这句话的意思是单个用户态的ebpf程序能创建64个map，还是主机上所有ebpf程序加起来可以创建64个内核态的ebpf程序？
2. 用户态的ebpf程序怎么绑定这些map的，有实例吗？</div>2023-12-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/33/ae/5e05b9dc.jpg" width="30px"><span>朝东</span> 👍（0） 💬（1）<div>你好，偶尔遇到个问题，在bpf加载成功后，没看到prink 到pipe 调试打印，重启系统就恢复，不知什么原因？</div>2023-04-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/23/3b/1d/cbfbd93e.jpg" width="30px"><span>小印_zoe</span> 👍（0） 💬（0）<div>有没有详细的付费学习群？</div>2023-03-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/25/3c/92/81fa306d.jpg" width="30px"><span>张Dave</span> 👍（0） 💬（0）<div>老师，请问下，一次编译到处执行，哪里还有更详细的解释呢？
没太明白文中总结的两点具体是怎么做的？</div>2022-09-24</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTJOBwR7MCVqwZbPA5RQ2mjUjd571jUXUcBCE7lY5vSMibWn8D5S4PzDZMaAhRPdnRBqYbVOBTJibhJg/132" width="30px"><span>ヾ(◍°∇°◍)ﾉﾞ</span> 👍（0） 💬（0）<div>老师，请教个问题，就是在比如在jdbc连接的时候，有时候一些防火墙或者VPN什么瞬间的原因会导致这个连接要卡住很长时间（通常是2小时15分），有什么办法可以快速探测并结束这种TCP反馈给客户端，ebpf这个手段可以嘛？</div>2022-05-07</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/b5/02/3bf0509e.jpg" width="30px"><span>reonard</span> 👍（0） 💬（1）<div>倪老师好，我试了4.18的内核，也可以用bpftool btf dump file &#47;sys&#47;kernel&#47;btf&#47;vmlinux format c 获得vmlinux.h，是不是就不需要5.2的内核了？</div>2022-04-25</li><br/>
</ul>