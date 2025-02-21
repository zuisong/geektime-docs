你好，我是倪朋飞。

上一讲，我带你一起梳理了应用进程的跟踪方法。根据编程语言的不同，从应用程序二进制文件的跟踪点中可以获取的信息也不同：编译型语言程序中的符号信息可以直接拿来跟踪应用的执行状态，而对于解释型语言和即时编译型语言程序，我们只能从解释器或即时编译器的跟踪点参数中去获取应用的执行状态。

除了前面三讲提到的内核和应用程序的跟踪之外，网络不仅是 eBPF 应用最早的领域，也是目前 eBPF 应用最为广泛的一个领域。随着分布式系统、云计算和云原生应用的普及，网络已经成为了大部分应用最核心的依赖，随之而来的网络问题也是最难排查的问题之一。

那么，eBPF 能不能协助我们更好地排查和定位网络问题呢？我们又该如何利用 eBPF 来排查网络相关的问题呢？今天，我就带你一起具体看看。

## eBPF 提供了哪些网络功能？

既然想要使用 eBPF 排查网络问题，我想进入你头脑的第一个问题就是：eBPF 到底提供了哪些网络相关的功能框架呢？

要回答这个问题，首先要理解 Linux 网络协议栈的基本原理。下面是一个简化版的内核协议栈示意图：

![图片](https://static001.geekbang.org/resource/image/ce/a5/ce9371b7e3b696feaf4233c1595e20a5.jpg?wh=1920x2960 "Linux内核协议栈")

如何理解这个网络栈示意图呢？从上往下看，就是应用程序发送网络包的过程；而反过来，从下往上看，则是网络包接收的过程。比如，从上到下来看这个网络栈，你可以发现：
<div><strong>精选留言（13）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/0f/5e/96/a03175bc.jpg" width="30px"><span>莫名</span> 👍（22） 💬（2）<div>1、比较赞同【最主要是因为不清楚内核中都有哪些函数和跟踪点可以拿来跟踪】这一观点。如果对内核不熟悉，借助 tracepoint 通配符可以很好的协助理解网络协议栈的关键路径。举两个简单例子。

&gt; 例 1：追踪 net 相关追踪点以及调用堆栈：

# bpftrace -e &#39;tracepoint:net:* { printf(&quot;%s(%d): %s %s\n&quot;, comm, pid, probe, kstack()); }&#39;

输出示例（sshd 发送数据包关键路径，涉及 tracepoint:net:net_dev_queue、tracepoint:net:net_dev_xmit 等追踪点，可以借助这些追踪点可进一步计算数据包排队时间等）：

sshd(219966): tracepoint:net:net_dev_queue
        __dev_queue_xmit+1524
        dev_queue_xmit+16
        ip_finish_output2+718
        __ip_finish_output+191
        ip_finish_output+54
        ip_output+112
        ip_local_out+53
        __ip_queue_xmit+354
        ip_queue_xmit+16
        __tcp_transmit_skb+1407
        tcp_write_xmit+982
        __tcp_push_pending_frames+57
        tcp_push+219
        tcp_sendmsg_locked+2415
        tcp_sendmsg+44
        inet_sendmsg+59
        sock_write_iter+156
        new_sync_write+287
        __vfs_write+38
        vfs_write+171
        ksys_write+97
        __x64_sys_write+26
        do_syscall_64+71
        entry_SYSCALL_64_after_hwframe+68

sshd(219966): tracepoint:net:net_dev_xmit
        dev_hard_start_xmit+368
        dev_hard_start_xmit+368
        sch_direct_xmit+278
        __dev_queue_xmit+1713
        dev_queue_xmit+16
        ip_finish_output2+718
        ...
        __x64_sys_write+26
        do_syscall_64+71
        entry_SYSCALL_64_after_hwframe+68

&gt; 例 2：使用 perf trace 也比较方便：

# perf trace --no-syscalls -e &#39;net:*&#39; curl -s time.geekbang.org &gt; &#47;dev&#47;null

输出示例（可以看到具体走了哪些网络设备、数据包长度、skb 内存地址等）：

0.439 curl&#47;2240 net:net_dev_queue:dev=eth1 skbaddr=... len=54
0.452 curl&#47;2240 net:net_dev_start_xmit:dev=eth1 skbaddr=... len=54
0.455 curl&#47;2240 net:net_dev_xmit:dev=eth1 skbaddr=... len=54
0.707 curl&#47;2240 net:netif_receive_skb:dev=eth1 skbaddr=... len=52

2、dropwatch.bt 头文件有些没使用到，可以做下简化：

#include &lt;linux&#47;skbuff.h&gt;
#include &lt;linux&#47;ip.h&gt;
#include &lt;linux&#47;socket.h&gt;
#include &lt;linux&#47;netdevice.h&gt;

=====================&gt;

#include &lt;linux&#47;skbuff.h&gt;
#include &lt;net&#47;ip.h&gt;

思考题直接用 bpftrace 内置变量 comm、pid 即可。</div>2022-02-07</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/18/b7/24/17f6c240.jpg" width="30px"><span>janey</span> 👍（1） 💬（1）<div>第二图里怎么没有tracepoint?应该是跟kprobe在同一个层面吧</div>2022-11-25</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/DYAIOgq83erFUhEiazDuzntpbECvyYdp6IdLwO1ic01sE02op3ZtGvqJEwxJhoUozjHwqF5vHprluUKeAIvmru8Q/132" width="30px"><span>Geek_9e1ece</span> 👍（0） 💬（1）<div>老师 ntop这个函数返回的是字符串么？为什么我用$sip或$dip去做if判断时候提示我两端的数据类不正确呢。

另外我翻了一下内核的源码，好像没有直接找到ntop（）这个名字的函数，请问还有pton（）这样的函数可以将字符串转成inet数据类型么，以便我在if判断中作为过滤条件。</div>2023-02-03</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/ec/0e/d64d4663.jpg" width="30px"><span>k8svip</span> 👍（0） 💬（1）<div>老师 如何跟踪下PHP-fpm线程，去处理MySQL 域名解析的过程呢？偶现连不通的情况，回出现udp receive error 包数量增加，tcpdump又捕获不到</div>2022-03-16</li><br/><li><img src="" width="30px"><span>从远方过来</span> 👍（0） 💬（1）<div>老师，看了你举的查找SKB的例子，我很好奇要怎么才能快速地从内核相关文档中找到相关的函数呢？  例如：找出关于内存分配的函数，  这个有什么好窍门么？</div>2022-02-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/28/1c/b7e3941c.jpg" width="30px"><span>阿斌斯基</span> 👍（0） 💬（1）<div>ubuntu 18.04 ,snap安装的bpftrace,kernel symbol解析失败
➜  ~ bpftrace -V
bpftrace v0.13.0
➜  ~ echo $BPFTRACE_VMLINUX
&#47;usr&#47;lib&#47;debug&#47;boot&#47;vmlinux-5.4.0-96-generic
➜  ~ uname -a              
Linux max-machine 5.4.0-96-generic #109~18.04.1-Ubuntu SMP Thu Jan 13 15:06:26 UTC 2022 x86_64 x86_64 x86_64 GNU&#47;Linux
➜  ~                       
sudo bpftrace -e &#39;kprobe:kfree_skb &#47;comm==&quot;curl&quot;&#47; {printf(&quot;kstack: %s\n&quot;, kstack);}&#39;
[sudo] password for max: 
Attaching 1 probe...
kstack: 
        0xffffffff9091b941
        0xffffffff90a5f5f7
        0xffffffff90914e41
        0xffffffff90a5eae9
        0xffffffff909f4009
        0xffffffff90a351c0
        0xffffffff9090b8e2
        0xffffffff9090b975
        0xffffffff902e0276
        0xffffffff902e047e
        0xffffffff900c493d
        0xffffffff90003ec9
        0xffffffff90004320
        0xffffffff90c0008c

kstack: 
        0xffffffff9091b941
        0xffffffff90a5f5f7
        0xffffffff90914e41
        0xffffffff90a5eae9
        0xffffffff909f4009
        0xffffffff90a351c0
        0xffffffff9090b8e2
        0xffffffff9090b975
        0xffffffff902e0276
        0xffffffff902e047e
        0xffffffff900c493d
        0xffffffff90003ec9
        0xffffffff90004320
        0xffffffff90c0008c

kstack: 
        0xffffffff9091b941
        0xffffffff9090fad3
        0xffffffff9090fb6a
        0xffffffff90004207
        0xffffffff90c0008c

kstack: 
        0xffffffff9091b941
        0xffffffff9090fad3
        0xffffffff9090fb6a
        0xffffffff90004207
        0xffffffff90c0008c

</div>2022-02-07</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/2d/27/c5/d4d00da2.jpg" width="30px"><span>为了维护世界和平</span> 👍（3） 💬（0）<div>github上的程序 执行 段错误
#bpftrace dropwatch.bt
Segmentation fault (core dumped)
</div>2022-07-19</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/e3LZWjQELTibuZAhfwhia16k7ehuQ4lg5oxrAbBdOGmNBYYAMpnrWlZGZmOOB7lc8nHeJnUBPvCAAdldvtcoVCTQ/132" width="30px"><span>InfoQ_1e92d5385cc8</span> 👍（0） 💬（0）<div>建议可以根据GPT 4.0来自动解析日志，如网络不通回复如下：
这是一个bpftrace日志，它使用了dropwatch.bt脚本来追踪丢失的网络数据包。从日志中，我们可以看到一个数据包从10.206.0.13发送到39.106.233.176时被丢弃了。以下是内核栈（kstack）的调用顺序：

    kfree_skb+1：释放数据包的内存。
    nf_hook_slow+167：调用Netfilter钩子，处理网络数据包。
    __ip_local_out+215：处理本地IP数据包的输出。
    ip_local_out+23：将数据包发送到本地IP层。
    __ip_queue_xmit+349：将数据包放入队列以进行传输。
    __tcp_transmit_skb+1362：传输TCP数据包。
    tcp_connect+2753：建立TCP连接。
    tcp_v4_connect+1112：建立IPv4 TCP连接。
    __inet_stream_connect+209：建立INET流连接。
    inet_stream_connect+54：建立流连接。
    __sys_connect+154：系统调用，发起连接。
    __x64_sys_connect+22：64位系统调用，发起连接。
    do_syscall_64+91：执行64位系统调用。
    entry_SYSCALL_64_after_hwframe+101：进入64位系统调用。

从这个调用栈中，我们可以看到数据包在网络层（Netfilter钩子）被丢弃。可能的原因包括防火墙规则、路由问题或其他网络配置问题。要解决这个问题，你需要检查你的网络设置，特别是防火墙规则和路由配置</div>2023-10-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/cd/db/7467ad23.jpg" width="30px"><span>Bachue Zhou</span> 👍（0） 💬（2）<div>$ sudo bpftrace -l &#39;kprobe:kfree_skb*&#39;
kprobe:kfree_skb_list_reason
kprobe:kfree_skb_partial
kprobe:kfree_skb_reason
kprobe:kfree_skbmem

$ uname -r
5.19.0-38-generic

尴尬 我这边 5.19 就没有 kfree_skb 这个函数了</div>2023-04-06</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1b/83/fb/621adceb.jpg" width="30px"><span>linker</span> 👍（0） 💬（0）<div>$ apt list --installed |grep &#39;\&lt;linux-&#39;

WARNING: apt does not have a stable CLI interface. Use with caution in scripts.

binutils-x86-64-linux-gnu&#47;jammy-updates,jammy-security,now 2.38-4ubuntu2.1 amd64 [installed,automatic]
linux-base&#47;jammy,now 4.5ubuntu9 all [installed,automatic]
linux-buildinfo-5.19.0-35-generic&#47;jammy-updates,jammy-security,now 5.19.0-35.36~22.04.1 amd64 [installed]
linux-firmware&#47;jammy-security,now 20220329.git681281e4-0ubuntu3.9 all [installed,upgradable to: 20220329.git681281e4-0ubuntu3.10]
linux-headers-5.19.0-35-generic&#47;jammy-updates,jammy-security,now 5.19.0-35.36~22.04.1 amd64 [installed]
linux-hwe-5.19-headers-5.19.0-35&#47;jammy-updates,jammy-security,now 5.19.0-35.36~22.04.1 all [installed,automatic]
linux-hwe-5.19-tools-5.19.0-35&#47;jammy-updates,jammy-security,now 5.19.0-35.36~22.04.1 amd64 [installed,automatic]
linux-image-5.19.0-35-generic&#47;jammy-updates,jammy-security,now 5.19.0-35.36~22.04.1 amd64 [installed]
linux-libc-dev&#47;jammy-updates,jammy-security,now 5.15.0-67.74 amd64 [installed,automatic]
linux-modules-5.19.0-35-generic&#47;jammy-updates,jammy-security,now 5.19.0-35.36~22.04.1 amd64 [installed,automatic]
linux-sound-base&#47;jammy,now 1.0.25+dfsg-0ubuntu7 all [installed,automatic]
linux-source-5.19.0&#47;jammy-updates,jammy-security,now 5.19.0-35.36~22.04.1 all [installed]
linux-tools-5.19.0-35-generic&#47;jammy-updates,jammy-security,now 5.19.0-35.36~22.04.1 amd64 [installed]
linux-tools-common&#47;jammy-updates,jammy-security,now 5.15.0-67.74 all [installed,automatic]</div>2023-03-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1b/83/fb/621adceb.jpg" width="30px"><span>linker</span> 👍（0） 💬（0）<div>$ cat &#47;etc&#47;os-release               
PRETTY_NAME=&quot;Ubuntu 22.04.1 LTS&quot;
NAME=&quot;Ubuntu&quot;
VERSION_ID=&quot;22.04&quot;
VERSION=&quot;22.04.1 LTS (Jammy Jellyfish)&quot;
VERSION_CODENAME=jammy
ID=ubuntu
ID_LIKE=debian
HOME_URL=&quot;https:&#47;&#47;www.ubuntu.com&#47;&quot;
SUPPORT_URL=&quot;https:&#47;&#47;help.ubuntu.com&#47;&quot;
BUG_REPORT_URL=&quot;https:&#47;&#47;bugs.launchpad.net&#47;ubuntu&#47;&quot;
PRIVACY_POLICY_URL=&quot;https:&#47;&#47;www.ubuntu.com&#47;legal&#47;terms-and-policies&#47;privacy-policy&quot;
UBUNTU_CODENAME=jammy

这个版本升级到 5.19 内核后，源码安装最新版bpftrace , 执行本节程序报错

definitions.h:2:10: fatal error: &#39;linux&#47;skbuff.h&#39; file not found
内核头文件已经安装了，内核开发包也安装了，请问老师这可能是什么问题？

下面是安装的包
</div>2023-03-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/fe/fc/e56c9c4a.jpg" width="30px"><span>A7kou</span> 👍（0） 💬（0）<div>老师想请问下，我看 cilium 的 ebpf 相关源码中，有个节叫 “from-container”，就在源码的 “cilium&#47;bpf&#47;bpf_lxc.c” 文件下，写作 “__section(&quot;from-container&quot;)”，但是关于这个 from-container 它长得很像一个 ebpf 的类型，但是我在 kernel 中又搜不到这个，用 &quot;bpftool feature probe&quot; 也没有和它相关的，所以想问下老师知不知道这个 from-container 是怎么变成 ebpf 程序被编译的？</div>2022-09-06</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/8a/b0/6ab66f1b.jpg" width="30px"><span>牛金霖</span> 👍（0） 💬（0）<div>老师，请问如何获取5.16的debuginfo</div>2022-07-24</li><br/>
</ul>