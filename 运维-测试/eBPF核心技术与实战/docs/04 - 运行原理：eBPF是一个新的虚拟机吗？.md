你好，我是倪朋飞。

上一讲，我带你一起搭建了 eBPF 的开发环境，并从最简单的 Hello World 开始，带你借助 BCC 库从零开发了一个跟踪 [openat()](https://man7.org/linux/man-pages/man2/open.2.html) 系统调用的 eBPF 程序。

不过，虽然第一个 eBPF 程序已经成功运行起来了，你很可能还在想：这个 eBPF 程序到底是如何编译成内核可识别的格式的？又是如何在内核中运行起来的？还有，既然允许普通用户去修改内核的行为，它又是如何确保内核安全的呢？

今天，我就带你一起深入看看 eBPF 虚拟机的原理，以及 eBPF 程序是如何执行的。

## eBPF 虚拟机是如何工作的？

eBPF 是一个运行在内核中的虚拟机，很多人在初次接触它时，会把它跟系统虚拟化（比如kvm）中的虚拟机弄混。其实，虽然都被称为“虚拟机”，系统虚拟化和 eBPF 虚拟机还是有着本质不同的。

系统虚拟化基于 x86 或 arm64 等通用指令集，这些指令集足以完成完整计算机的所有功能。而为了确保在内核中安全地执行，eBPF 只提供了非常有限的指令集。这些指令集可用于完成一部分内核的功能，但却远不足以模拟完整的计算机。为了更高效地与内核进行交互，eBPF 指令还有意采用了 C 调用约定，其提供的辅助函数可以在 C 语言中直接调用，极大地方便了 eBPF 程序的开发。
<div><strong>精选留言（30）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/0f/5e/96/a03175bc.jpg" width="30px"><span>莫名</span> 👍（23） 💬（3）<div>追踪 bpf 系统调用，借助 BCC 宏定义 TRACEPOINT_PROBE(category, event) 比较方便，例如：

-------------- example.c ----------------

TRACEPOINT_PROBE(syscalls, sys_enter_bpf)
{
    bpf_trace_printk(&quot;%d\\n&quot;, args-&gt;cmd);
    return 0;
}

-------------- example.py -----------------

#!&#47;usr&#47;bin&#47;env python3

from bcc import BPF

# load BPF program
b = BPF(src_file=&quot;example.c&quot;)
b.trace_print()

</div>2022-01-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/58/eb/cf3608bd.jpg" width="30px"><span>18646333118</span> 👍（12） 💬（7）<div>解决方法:
{
    &quot;features&quot;: {
        &quot;libbfd&quot;: false
    }
}

uname -r
5.13.0-19-generic

apt-cache search linux-source
apt install linux-source-5.13.0

cd  &#47;usr&#47;src&#47;
tar -jxvf linux-source-5.13.0.tar.bz2

apt install libelf-dev
cd linux-source-5.13.0&#47;tools
make -C  bpf&#47;bpftool
.&#47;bpf&#47;bpftool&#47;bpftool version -p
{
    &quot;version&quot;: &quot;5.13.19&quot;,
    &quot;features&quot;: {
        &quot;libbfd&quot;: true,
        &quot;skeletons&quot;: true
    }
}
</div>2022-02-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/76/b0/14fec62f.jpg" width="30px"><span>不了峰</span> 👍（5） 💬（1）<div>你通常是如何快速理解一门新技术的运行原理的？
--- 看一下官方文档，了解体系架构，多看几遍。买书看感觉也是一个快速入门的方法。
但是对于没有编程经验，对于 字节码、cpu寄存器、jit ，编译器的理解还是很抽象，学到这里还是有点晕。感觉还是要把这课程从头再看一遍。</div>2022-01-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/19/1d/d2b6e006.jpg" width="30px"><span>火火寻</span> 👍（3） 💬（1）<div>1、你通常是如何快速理解一门新技术的运行原理的？
Get Essentials， ADEPT五步法：类比，画图，例子，文字说明，定义。

剩下的就是根据需要侧重地深入到细节。</div>2022-02-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/e8/ac/7324d5ca.jpg" width="30px"><span>七里</span> 👍（1） 💬（1）<div>请问，不能执行&#39;bpftool prog dump jited id 78&#39;是怎么回事？bpf相关的包都按照上一讲的提示按照上了

root@maqi-ubt:~# bpftool prog dump xlated id 78
int hello_world(void * ctx):
; int hello_world(void *ctx)
   0: (b7) r1 = 33
; ({ char _fmt[] = &quot;Hello, World!&quot;; bpf_trace_printk_(_fmt, sizeof(_fmt)); });
   1: (6b) *(u16 *)(r10 -4) = r1
   2: (b7) r1 = 1684828783
   3: (63) *(u32 *)(r10 -8) = r1
   4: (18) r1 = 0x57202c6f6c6c6548
   6: (7b) *(u64 *)(r10 -16) = r1
   7: (bf) r1 = r10
;
   8: (07) r1 += -16
; ({ char _fmt[] = &quot;Hello, World!&quot;; bpf_trace_printk_(_fmt, sizeof(_fmt)); });
   9: (b7) r2 = 14
  10: (85) call bpf_trace_printk#-63952
; return 0;
  11: (b7) r0 = 0
  12: (95) exit
root@maqi-ubt:~#
root@maqi-ubt:~# bpftool prog dump jited id 78
Error: No libbfd support</div>2022-02-02</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/41/38/4f89095b.jpg" width="30px"><span>写点啥呢</span> 👍（1） 💬（2）<div>请问老师，像上节课例子中 trace openat系统调用的这个函数int hello_world(struct pt_regs *ctx, int dfd, const char __user * filename, struct open_how *how)，bpf会自动把系统调用参数注入bpf函数执行中。本节课提到bpf虚拟机中对bpf函数的参数个数有限制，那如果碰到系统调用参数个数大于bpf限制了，该如何处理呢？

谢谢老师</div>2022-01-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/31/42/a1/716f3c50.jpg" width="30px"><span>22</span> 👍（0） 💬（5）<div>老师，sudo strace -v -f -ebpf .&#47;hello.py
strace: exec: 可执行文件格式错误
+++ exited with 1 +++
想请问一下这是什么原因啊？</div>2023-02-25</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/31/42/a1/716f3c50.jpg" width="30px"><span>22</span> 👍（0） 💬（2）<div>追踪系统调用，显示没有权限该怎么解决啊
sudo strace -v -f -ebpf .&#47;hello.py
strace: exec: 权限不够
+++ exited with 1 +++
</div>2023-02-25</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/99/f4/e0484cac.jpg" width="30px"><span>崔伟协</span> 👍（0） 💬（1）<div>ebpf是图灵完备的吗</div>2022-09-25</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/ibpASCYk5eF1lAEbJ3TSI0fuMtiaVDb7dNuBZDRPL6QjEict8Wrb8iax2OibbEBxSs4bicCYf3yMEkGmXB2b2UVypaIg/132" width="30px"><span>woo</span> 👍（0） 💬（1）<div>为啥我的strace输出的不像老师那种json格式很漂亮，是以行为单位的显示，是装了什么工具吗？</div>2022-03-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/76/b0/14fec62f.jpg" width="30px"><span>不了峰</span> 👍（0） 💬（1）<div>root@ubuntu-impish:~# bpftool prog dump jited id 331
Error: No libbfd support   
root@ubuntu-impish:~# 
----
root@ubuntu-impish:~# bpftool -V
&#47;usr&#47;lib&#47;linux-tools&#47;5.13.0-27-generic&#47;bpftool v5.13.19
features:
root@ubuntu-impish:~# 
-----
是不是因为新版的bpftool  Remove bpf_jit_enable=2 debugging mode。

-----
root@ubuntu-impish:~#  bpftool prog profile
Error: bpftool prog profile command is not supported. Please build bpftool with clang &gt;= 10.0.0
root@ubuntu-impish:~# clang -v
Ubuntu clang version 13.0.0-2
Target: x86_64-pc-linux-gnu</div>2022-01-27</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTKwGurTWOiaZ2O2oCdxK9kbF4PcwGg0ALqsWhNq87hWvwPy8ZU9cxRzmcGOgdIeJkTOoKfbxgEKqrg/132" width="30px"><span>ZR2021</span> 👍（0） 💬（3）<div>老师，我这边执行 bpftool prog dump jited id xxx，报&quot;Error: No libbfd support&quot; 错误，网上也没找到原因，系统是最新的ubuntu 21.10，vmvare的虚拟机，执行xlated是可以打印出指令的，不知道啥个情况</div>2022-01-27</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTKwGurTWOiaZ2O2oCdxK9kbF4PcwGg0ALqsWhNq87hWvwPy8ZU9cxRzmcGOgdIeJkTOoKfbxgEKqrg/132" width="30px"><span>ZR2021</span> 👍（0） 💬（2）<div>老师，sudo bpftool prog dump xlated id 89，这条命令输出的指令是存储模块存储的指令吗，这个指令是在验证器里进行转换的吗，验证器用转换后的指令去模拟执行是否安全，对bpf 接触的比较少，可能问的有点低级……</div>2022-01-26</li><br/><li><img src="" width="30px"><span>Geek_b84e15</span> 👍（4） 💬（1）<div>倪老师您好，我看hello_world的参数列表是(void * ctx)，而有的例子里参数是这样的：int hello_world(struct pt_regs *ctx, int dfd, const char __user * filename, struct open_how *how)，请问怎么确定参数的个数和参数的类型呢？</div>2022-04-25</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/d6/46/5eb5261b.jpg" width="30px"><span>Sudouble</span> 👍（2） 💬（0）<div>对于运行了sudo strace -v -f -ebpf .&#47;hello.py报了以下错误的小伙伴
strace: exec: Exec format error
+++ exited with 1 +++

替换成这个命令就可以出结果啦：sudo strace -v -f -ebpf python3 hello.py</div>2023-07-06</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTJGXndj5N66z9BL1ic9GibZzWWgoVeWaWTL2XUnCYic7iba2kAEvN9WfjmlXELD5lqt8IJ1P023N5ZWicg/132" width="30px"><span>Geek_f93234</span> 👍（1） 💬（1）<div># strace -v -f -ebpf .&#47;hello.py
strace: exec: Exec format error
+++ exited with 1 +++
</div>2023-03-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/20/9d/61efb39e.jpg" width="30px"><span>赵杨健</span> 👍（1） 💬（0）<div>有学习群吗？遇到一些环境问题</div>2023-03-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/c5/a1/f6a2d80d.jpg" width="30px"><span>穿靴子的outman</span> 👍（1） 💬（0）<div>1.你通常是如何快速理解一门新技术的运行原理的？

a.我通常首先搞清楚这门新技术想解决什么问题等背景知识.谁在什么场景下,会遇到什么问题.人永远是第一位的.
c.按照helloworld等例程实操一遍.
b.根据实际体验,重新思考这门技术,有哪些概念,组件,组件之间的关系是怎样.各个组件的输入输出怎么样的,怎么组合起来解决了这个问题.此时可以借助时序图,流程图等工具.加深理解.</div>2022-10-06</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/2b/56/ac/a047a944.jpg" width="30px"><span>李清泉🍻</span> 👍（0） 💬（0）<div>老师您好，bpf对性能要求这么是，怎么会用python写呢？</div>2024-03-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/d6/46/5eb5261b.jpg" width="30px"><span>Sudouble</span> 👍（0） 💬（0）<div>对于问题1：主要更多的从技术架构、技术特点、解决的业务难题等角度，先有一个总体的概览。之后再逐步深入，看更多的细节，避免一头扎进细节的海洋中。</div>2023-07-06</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/17/18/e4382a8e.jpg" width="30px"><span>有识之士</span> 👍（0） 💬（0）<div>root@instance-00qqerhq:~&#47;jike# sudo strace -v -f .&#47;hello.py
execve(&quot;.&#47;hello.py&quot;, [&quot;.&#47;hello.py&quot;], [&quot;LANGUAGE=en_US:&quot;, &quot;LANG=en_US.UTF-8&quot;, &quot;LS_COLORS=rs=0:di=01;34:ln=01;36&quot;..., &quot;TERM=xterm-256color&quot;, &quot;PATH=&#47;usr&#47;local&#47;sbin:&#47;usr&#47;local&#47;&quot;..., &quot;MAIL=&#47;var&#47;mail&#47;root&quot;, &quot;LOGNAME=root&quot;, &quot;USER=root&quot;, &quot;HOME=&#47;root&quot;, &quot;SHELL=&#47;bin&#47;bash&quot;, &quot;SUDO_COMMAND=&#47;usr&#47;bin&#47;strace -v &quot;..., &quot;SUDO_USER=root&quot;, &quot;SUDO_UID=0&quot;, &quot;SUDO_GID=0&quot;]) = -1 EACCES (Permission denied)
strace: exec: Permission denied
+++ exited with 1 +++

如果报上述错误，需要执行以下命令： chmod +x hello.py</div>2023-06-23</li><br/><li><img src="" width="30px"><span>Geek_5ada4a</span> 👍（0） 💬（3）<div>strace .&#47;hello.py
execve(&quot;.&#47;hello.py&quot;, [&quot;.&#47;hello.py&quot;], 0x7ffed513d760 &#47;* 30 vars *&#47;) = -1 EACCES (Permission denied)
strace: exec: Permission denied
+++ exited with 1 +++

哪位大佬帮忙看看，是 root 用户，ls -l hello.py 的结果是
-rw-r--r-- 1 root root 147 Nov  3 14:44 .&#47;hello.py</div>2022-11-03</li><br/><li><img src="" width="30px"><span>Geek_5ada4a</span> 👍（0） 💬（0）<div>openat(AT_FDCWD, &quot;&#47;sys&#47;bus&#47;event_source&#47;devices&#47;kprobe&#47;type&quot;, O_RDONLY) = 5
read(5, &quot;6\n&quot;, 4096) = 2
close(5) = 0

为什么下面的 type = 0x6 ，对不上诶
另外这个 read 作用是？

</div>2022-11-01</li><br/><li><img src="" width="30px"><span>Geek_ee7838</span> 👍（0） 💬（1）<div>root@iZbp18xpd2ia89yqcrhi48Z:~&#47;eBPF# ll
total 24
drwxr-xr-x 2 root root 4096 Sep 20 20:03 .&#47;
drwx------ 8 root root 4096 Sep 20 20:49 ..&#47;
-rw-r--r-- 1 root root   85 Sep 20 19:14 hello.c
-rwxr-xr-x 1 root root  274 Sep 20 19:18 hello.py*
-rw-r--r-- 1 root root  753 Sep 20 20:03 trace-open.c
-rw-r--r-- 1 root root  725 Sep 20 20:02 trace-open.py
root@iZbp18xpd2ia89yqcrhi48Z:~&#47;eBPF# sudo strace -v -f -ebpf .&#47;hello.py
strace: exec: Exec format error
+++ exited with 1 +++
为什么我的strace跟踪不了ebpf数据包，strace版本是5.16的，我查看命令帮助似乎并没有-ebpf的命令参数</div>2022-09-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1c/bb/50/c8ebd5e1.jpg" width="30px"><span>MoGeJiEr🐔</span> 👍（0） 💬（0）<div>“R1-R5寄存器用于函数调用的参数，因此这里的函数调用参数不能超过5个”是指bpf-helper函数的参数不能超过5个嘛？</div>2022-08-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/5f/43/3799a0f3.jpg" width="30px"><span>magina</span> 👍（0） 💬（0）<div>eBPF 运行时图中，不支持JIT是什么过程呢？文中也没有提什么情况下走JIT，什么情况不走JIT？</div>2022-07-25</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/17/18/e4382a8e.jpg" width="30px"><span>有识之士</span> 👍（0） 💬（0）<div>我的报错

root@3358d0bf1a7b:~# bpftool prog list
WARNING: bpftool not found for kernel 5.10.25

  You may need to install the following packages for this specific kernel:
    linux-tools-5.10.25-linuxkit
    linux-cloud-tools-5.10.25-linuxkit

  You may also want to install one of the following packages to keep up to date:
    linux-tools-linuxkit
    linux-cloud-tools-linuxkit

root@3358d0bf1a7b:~# bpftool
WARNING: bpftool not found for kernel 5.10.25

  You may need to install the following packages for this specific kernel:
    linux-tools-5.10.25-linuxkit
    linux-cloud-tools-5.10.25-linuxkit

  You may also want to install one of the following packages to keep up to date:
    linux-tools-linuxkit
    linux-cloud-tools-linuxkit</div>2022-07-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/17/18/e4382a8e.jpg" width="30px"><span>有识之士</span> 👍（0） 💬（1）<div>请教选，这个ebpf 虚拟机功能类似  java jvm 编译成class 字节码？还是有很大的不同点？</div>2022-07-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/28/04/7a/1306bf9c.jpg" width="30px"><span>cmz</span> 👍（0） 💬（1）<div>ebpf为什么要设计成虚拟机的形式</div>2022-05-07</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/28/04/7a/1306bf9c.jpg" width="30px"><span>cmz</span> 👍（0） 💬（0）<div>内核事件触发后，即时编译器才会把bpf指令编译成机器指令吗，还是说加载到内核时候就编译了？</div>2022-05-07</li><br/>
</ul>