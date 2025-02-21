你好，我是倪朋飞。

到上一讲的高性能网络实战为止，我们就完成了“实战进阶篇”的学习。在这个模块中，我带你从实战出发，利用 BCC、libbpf、bpftrace 等常用的 eBPF 开发工具，开发了应用于内核跟踪、用户态跟踪、网络跟踪、容器安全、高性能网络等各个场景的 eBPF 程序。通过这个模块的学习，我想你已经掌握了 eBPF 在不同场景的应用方法，并能够举一反三，利用类似的步骤把 eBPF 应用到实际的工作当中去。

“实战进阶篇”结束后，我们课程的常规更新阶段的正文内容就基本更新完了。在之前的课程内容中，除了用实践帮你更好地理解原理，我也在案例中穿插介绍了很多开源项目和 eBPF 工具，帮你更好地利用 eBPF 去解决实际的问题。今天，我就基于现阶段的 eBPF 最新技术发展，为你汇总最实用的 eBPF 工具以及最新的开源项目状态。这样，在后续的学习和实践过程中，你就可以按图索骥，根据应用场景选择最合适的方案。今天的内容将分为开发工具集、实用工具集和最新开源项目三个部分。

## 开发工具集

首先来看第一个部分，开发工具集，也就是在开发 eBPF 程序时常用的开发库以及开发工具。

在这门课里，我已经在不同案例中为你反复介绍了 BCC、libbpf、bpftrace 等常用的开发库，以及把 eBPF 源代码编译为字节码的 LLVM 工具。除了这些方法，你还可以直接在内核源码库中，参考已有的示例（示例路径为 [samples/bpf](https://elixir.bootlin.com/linux/v5.13/source/samples/bpf) ）进行 eBPF 程序的开发。
<div><strong>精选留言（2）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/14/f0/1a/d5a1a648.jpg" width="30px"><span>张博</span> 👍（4） 💬（1）<div>有个排版错误，rust-bcc是bcc对rust的绑定吧</div>2022-02-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/cd/db/7467ad23.jpg" width="30px"><span>Bachue Zhou</span> 👍（2） 💬（0）<div>rust 现在能直接开发内核模块，不能用 rust 直接开发 ebpf 内核态程序吗？</div>2023-04-14</li><br/>
</ul>