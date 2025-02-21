你好，我是倪朋飞。

在上一讲中，我带你学习了 eBPF for Windows 的主要原理以及如何在 Windows 系统上开发 eBPF 程序。eBPF for Windows 把开源社区的 eBPF 工具链带到了 Linux，让 Windows 开发者也可以利用 eBPF 技术来解决网络、观测、性能优化等各类问题。由于复用了相同的工具链，Windows eBPF 程序的开发流程同 Linux 非常相似，主要也是利用 libbpf 开发 eBPF 内核程序、利用 LLVM 编译 eBPF 程序为字节码、最后再到用户态程序中加载和挂载 eBPF 字节码，并通过 BPF 映射同内核态 eBPF 程序进行交互。

今天这一讲我将带你换一种编程语言，也就是通过在容器和云原生应用中最流行的 Go 语言来开发 eBPF 程序。

## eBPF Go 语言开发库

在[阶段总结｜实用eBPF工具及最新开源项目总结](https://time.geekbang.org/column/article/487227)中我曾经讲到，BCC、libbpf 以及内核源码，都主要使用 C 语言开发 eBPF 程序，而实际的应用程序可能会以多种多样的编程语言进行开发。所以，开源社区开发和维护了很多不同语言的接口，方便这些高级语言跟 eBPF 系统进行交互。比如，我们课程多次使用的 BCC 就提供了 Python、C++ 等多种语言的接口，而使用 BCC 的 Python 接口去加载 eBPF 程序，要比 libbpf 和内核源码的方法简单得多。
<div><strong>精选留言（2）</strong></div><ul>
<li><img src="" width="30px"><span>0mfg</span> 👍（0） 💬（0）<div>老师，今年的更新可以来个rust开发ebpf程序吗</div>2024-11-06</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/b5/ca/c3949f49.jpg" width="30px"><span>疯狂的小企鹅</span> 👍（0） 💬（1）<div>&gt; 也可以通过 BTF 来解决不同内核版本中数据结构不同的问题，从而实现一次编译到处执行。

请教一下哦，要想通过BTF来解决不同内核版本数据结构不同的问题，应该还需要用户态程序能够通过类似libbpf的方式来完成eBPF程序的重定位工作吧？请问cilium&#47;ebpf库是怎么解决这个问题的？我看官方文档写着也比较浅https:&#47;&#47;ebpf-go.dev&#47;guides&#47;portable-ebpf&#47;#compile-once-run-everywhere 。目前我们采用的办法是根据不同kernel版本生成多份.o文件，然后用户态程序再判断下kernel版本来决定加载哪一份.o。但我感觉这不是最佳实践，求老师赐教。</div>2024-03-21</li><br/>
</ul>