你好，我是程远。

今天这一讲，我们聊一聊eBPF。在我们专题加餐第一讲的分析案例时就说过，当我们碰到网络延时问题，在毫无头绪的情况下，就是依靠了我们自己写的一个eBPF工具，找到了问题的突破口。

由此可见，eBPF在内核问题追踪上的重要性是不言而喻的。那什么是eBPF，它的工作原理是怎么样，它的编程模型又是怎样的呢？

在这一讲里，我们就来一起看看这几个问题。

## eBPF的概念

eBPF，它的全称是“Extended Berkeley Packet Filter”。从名字看，你可能会觉奇怪，似乎它就是一个用来做网络数据包过滤的模块。

其实这么想也没有错，eBPF的概念最早源自于BSD操作系统中的BPF（Berkeley Packet Filter），1992伯克利实验室的一篇论文 [“The BSD Packet Filter: A New Architecture for User-level Packet Capture”](https://www.tcpdump.org/papers/bpf-usenix93.pdf)。这篇论文描述了，BPF是如何更加高效灵活地从操作系统内核中抓取网络数据包的。

我们很熟悉的tcpdump工具，它就是利用了BPF的技术来抓取Unix操作系统节点上的网络包。Linux系统中也沿用了BPF的技术。

那BPF是怎样从内核中抓取数据包的呢？我借用BPF论文中的图例来解释一下：
<div><strong>精选留言（5）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/12/1e/63/d5909105.jpg" width="30px"><span>小李同学</span> 👍（4） 💬（1）<div>老师，有没有能跑在arm64板子上的bpf用例，我用最简单的hello word测试用例，5.4的内核，报各种错误，都快怀疑是不是不能跑在atm64上</div>2021-03-04</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/7a/8b/2c81a375.jpg" width="30px"><span>好说</span> 👍（1） 💬（2）<div>老师，ebpf-kill-example编译后执行会有下面的报错，是内核少开启了什么吗？
libbpf: sec &#39;tracepoint&#47;syscalls&#47;sys_enter_kill&#39;: failed to find program symbol at offset 0
The kernel didn&#39;t load the BPF program</div>2021-02-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/26/82/0c/cc106ab1.jpg" width="30px"><span>Samaritan.</span> 👍（0） 💬（0）<div>加餐的内容很值，非常用心，谢谢老师！</div>2023-10-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/18/b7/24/17f6c240.jpg" width="30px"><span>janey</span> 👍（0） 💬（0）<div>请问下，Clang&#47;LLVM编译成 foo_kern.o文件再加载到内核中由BPF Verifier进行指令检查然后再由JIT编译成宿主机上的本地指令。这个过程中每次程序执行一次，这三个步骤都要走一遍吗？还是说会只需要做一次，当下次执行的时候直接用上次处理好的本地指令就行？</div>2022-11-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/c4/03/f753fda7.jpg" width="30px"><span>JianXu</span> 👍（0） 💬（0）<div>老师，ebpf 和 iptables 里面的hook 最本质的区别是什么呢？</div>2022-08-27</li><br/>
</ul>