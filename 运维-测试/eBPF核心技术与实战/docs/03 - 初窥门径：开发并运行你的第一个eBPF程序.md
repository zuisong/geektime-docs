你好，我是倪朋飞。

通过前面两讲，我已经带你为正式进入 eBPF 的学习做好了准备，接下来我们进入第二个模块“基础入门篇”的学习。在这个模块里，你会学习到 eBPF 的开发环境搭建方法、运行原理、编程接口，以及各种类型 eBPF 程序的事件触发机制和应用场景。

上一讲，我带你一起梳理了 eBPF 的学习路径和学习技巧，并特别强调了动手实践在学习 eBPF 过程中的重要性。那么，eBPF 程序到底是什么样子的？如何搭建 eBPF 的开发环境，又如何开发一个 eBPF 应用呢？

今天，我就带你一起上手开发第一个 eBPF 程序。

## 如何选择 eBPF 开发环境？

在前两讲中，我曾提到，虽然 Linux 内核很早就已经支持了 eBPF，但很多新特性都是[在 4.x 版本中逐步增加的](https://github.com/iovisor/bcc/blob/master/docs/kernel-versions.md#main-features)。所以，想要稳定运行 eBPF 程序，内核至少需要 **4.9** 或者更新的版本。而在开发和学习 eBPF 时，为了体验和掌握最新的 eBPF 特性，我推荐使用更新的 **5.x** 内核。

作为 eBPF 最重大的改进之一，一次编译到处执行（简称 CO-RE）解决了内核数据结构在不同版本差异导致的兼容性问题。不过，在使用 CO-RE 之前，内核需要开启 `CONFIG_DEBUG_INFO_BTF=y` 和 `CONFIG_DEBUG_INFO=y` 这两个编译选项。为了避免你在首次学习 eBPF 时就去重新编译内核，我推荐使用已经默认开启这些编译选项的发行版，作为你的开发环境，比如：
<div><strong>精选留言（30）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/0f/5e/96/a03175bc.jpg" width="30px"><span>莫名</span> 👍（9） 💬（3）<div>给倪老师的 Github 仓库里面的这个小程序挑个🐛：
1、b = BPF(src_file=&quot;trace-open.c&quot;)，trace-open.c -&gt; trace_open.c
2、依赖了 openat2.h 头文件，openat2 系统调用自 5.6 版本才出现，低于这个版本无法运行 trace_open.py，建议用 openat 系统调用，有比较好的版本兼容性。</div>2022-01-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/5e/96/a03175bc.jpg" width="30px"><span>莫名</span> 👍（68） 💬（3）<div>追踪文件打开事件，采用场景大致有：
1、查看某个程序启动时加载了哪些配置文件，便于确认是否加载了正确的配置文件。对于允许自定义配置文件路径的程序尤其有用，例如 MySQL、PostgreSQL。
2、查看是否存在频繁或周期性打开某些文件的情况，考虑是否存在优化可能。比如周期性打开某个极少变化的文件，可以一次性读取，且监听文件变动事件，避免多次打开读取。
3、分析依赖 &#47;proc、&#47;sys 等虚拟文件系统的 Linux 工具大致工作原理。比如执行 vmstat，，可以通过追踪文件打开事件看到至少打开了 &#47;proc&#47;meminfo、&#47;proc&#47;stat、&#47;proc&#47;vmstat 这几个文件，帮助你更好的理解工具的数据源与实现原理。
4、分析 K8s、Docker 等 cgroup 相关操作。比如 docker run xxx 时，可以看到 &#47;sys&#47;fs&#47;cgroup&#47;cpuset&#47;docker&#47;xxx&#47;cpuset.cpus、&#47;sys&#47;fs&#47;cgroup&#47;cpuset&#47;docker&#47;xxx&#47;cpuset.mems 等 cgroup 文件被打开，也可以查看 kube-proxy 在周期性刷新 cgroup 相关文件。
5、....</div>2022-01-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/50/05/90f1a14e.jpg" width="30px"><span>JUNLONG</span> 👍（10） 💬（2）<div>习惯用docker的同学可以试下 这个镜像，github地址：github.com&#47;Jun10ng&#47;ebpf-for-desktop 
用docker可以用vscode编辑会高效点。如果喜欢的话就来个start吧 谢谢</div>2022-01-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/5a/56/115c6433.jpg" width="30px"><span>jssfy</span> 👍（7） 💬（1）<div>请问这种对open系统调用的截获会影响用户文件打开的性能不? 影响到什么程度呢?</div>2022-02-08</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/rQOn22bNV0kHpoPWRLRicjQCOkiaYmcVABiaIJxIDWIibSdqWXYTxjcdjiadibIxFsGVp5UE4DBd6Nx2DxjhAdlMIZeQ/132" width="30px"><span>ThinkerWalker</span> 👍（6） 💬（3）<div>有个Python语法的疑问：trace_open.py中，print_event被调用的时候【28行，b[&quot;events&quot;].open_perf_buffer(print_event)】是如何传入三个参数（cpu, data, size）呢？</div>2022-01-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/76/b0/14fec62f.jpg" width="30px"><span>不了峰</span> 👍（5） 💬（1）<div>原来这个 trace_open.py  就是一个「简化」版的 opensnoop-bpfcc  工具呀。

我为了更清晰更简单的打印出 trace_open.py 的输出把一些服务都关了 ：）
systemctl stop multipathd
systemctl stop snapd
systemctl stop irqbalance </div>2022-01-25</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/pNKoOAa1QXibrykHNXibW4tyaIIhicocPGXtcVnEianCyOQY9bl0P2JQ3wSialUaolcLVEWycCEBz1Oe4Tj4yghH9yw/132" width="30px"><span>Geek_5aa343</span> 👍（5） 💬（3）<div>老师，您好，有几个问题请教下：
1. &quot;do_sys_openat2() 是系统调用 openat() 在内核中的实现&quot; 怎么去找到一个系统调用在内核中的实现呢？
2. 使用BPF map获取openat的打开文件名这里，&#47;&#47; 定义数据结构struct data_t { u32 pid; u64 ts; char comm[TASK_COMM_LEN]; char fname[NAME_MAX];}; 这个的格式为啥是这样呢，就是有具体每个探针的map说明文档嘛
多谢老师</div>2022-01-21</li><br/><li><img src="https://wx.qlogo.cn/mmopen/vi_32/DYAIOgq83eqtXSgThiaEiaEqqic5YIJ7v469nCM3VXiccOJ4SxbYjW91ciczuYYEzcTVtYWaWXaokZqShuLdKsXjnFA/132" width="30px"><span>Geek_b85295</span> 👍（4） 💬（5）<div>老师，我的环境是ubuntu20.04，内核5.4.0-92-generic，把环境依赖都正常安装好后，执行python3 hello.py 出现错误 Failed to attach BPF program b&#39;hello_world&#39; to kprobe b&#39;do_sys_openat2&#39;，网上没找到解决方法，可以帮忙看看嘛</div>2022-02-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/41/38/4f89095b.jpg" width="30px"><span>写点啥呢</span> 👍（3） 💬（2）<div>有几个问题想请教老师：
1. perf_buffer_poll方法是非阻塞的么
2. bpf_probe_read(&amp;data.fname, sizeof(data.fname), (void *)filename); 这里filename指针的内存大小是否也是NAME_MAX，不然读取应该会导致非法访问
3. hello_world方法的几个形参是什么含义，感觉ctx是bpf固定的，后面dfd, filename和open_how是openat2的参数，请问是否编写bpf函数都是可以在ctx后面加入对应系统调用接口的入参，然后bpf会在执行时候自动进行参数绑定？
4. perf_submit函数传入的c struct在bcc脚本中看上去可以通过event方法自动转化为python对象？

谢谢老师
</div>2022-01-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/97/95/aad51e9b.jpg" width="30px"><span>waterjiao</span> 👍（2） 💬（1）<div>还有几个问题咨询下老师
1. perf缓存区大小如何查看
2.如果缓存区满了，后续数据会覆盖之前的数据吗？open_perf_buffer是阻塞的么
3. libbpf是怎么做到co-re的</div>2022-02-17</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTKdVVxCVYJMmSmia51JzwSju1yNgDNNPD6lO9LOY2tygkxpGrVbIbAQZqHb04SDwuaibIEEGzudUD3g/132" width="30px"><span>HenryHui</span> 👍（2） 💬（3）<div>老师您好：
我在运行例子的时候出现了错误如下错误：

root@ubuntu-linux-20-04-desktop:~&#47;project&#47;ebpf&#47;study# sudo python3 hello.py
cannot attach kprobe, probe entry may not exist
Traceback (most recent call last):
  File &quot;hello.py&quot;, line 8, in &lt;module&gt;
    b.attach_kprobe(event=&quot;do_sys_openat2&quot;, fn_name=&quot;hello_world&quot;)
  File &quot;&#47;usr&#47;lib&#47;python3&#47;dist-packages&#47;bcc&#47;__init__.py&quot;, line 658, in attach_kprobe
    raise Exception(&quot;Failed to attach BPF program %s to kprobe %s&quot; %
Exception: Failed to attach BPF program b&#39;hello_world&#39; to kprobe b&#39;do_sys_openat2

我的系统内核是：
Linux ubuntu-linux-20-04-desktop 5.4.0-80-generic #90-Ubuntu SMP Fri Jul 9 17:43:26 UTC 2021 aarch64 aarch64 aarch64 GNU&#47;Linux

重点是这句报错：cannot attach kprobe, probe entry may not exist  是说我的kprobe不存在么
</div>2022-02-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/82/01/8ee18ad0.jpg" width="30px"><span>Y</span> 👍（2） 💬（3）<div>E: 无法定位软件包 libbpf-dev
提示这个报错怎么办？更新了源好像也不行</div>2022-02-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/bc/e2/e760c8e2.jpg" width="30px"><span>一位不愿透露姓名的王先生</span> 👍（2） 💬（1）<div>BPF_PERF_OUTPUT(events);
这个 events 是在哪定义的？ </div>2022-01-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/3c/c4/7c2bf312.jpg" width="30px"><span>草根</span> 👍（2） 💬（1）<div>请问老师，hello_world的入参是要和系统调用的入参设置一致吗？</div>2022-01-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1f/05/63/dd59ad18.jpg" width="30px"><span>加油加油</span> 👍（1） 💬（2）<div>老师问下，为什么我的ubuntu:20 里面只有设置 __x64_sys_openat  才有用  按照文章里的就不行呢 ？</div>2022-02-24</li><br/><li><img src="" width="30px"><span>Geek_7e93d7</span> 👍（1） 💬（4）<div>为什么我一启动就会提示这个，这算是报错吗？
include&#47;linux&#47;compiler-clang.h:41:9: warning: &#39;__HAVE_BUILTIN_BSWAP32__&#39; macro redefined [-Wmacro-redefined]
#define __HAVE_BUILTIN_BSWAP32__
        ^
&lt;command line&gt;:4:9: note: previous definition is here
#define __HAVE_BUILTIN_BSWAP32__ 1
        ^
In file included from &lt;built-in&gt;:2:
</div>2022-02-21</li><br/><li><img src="" width="30px"><span>Geek_9e8767</span> 👍（1） 💬（1）<div>希望老师能分享下 bpf 的开发环境搭建、路径配置这些基础。主要困难是如何在mac 上使用 ide 去开发bpf，ide 如何配置可以让头文件可以被索引到。 golang 开发者，接触这个有点陌生。</div>2022-02-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/5e/67/133d2da6.jpg" width="30px"><span>Geek_5244fa</span> 👍（1） 💬（1）<div>为什么要先判断 bpf_get_current_comm 成功之后再 bpf_probe_read ？</div>2022-01-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/53/b5/d914f2c2.jpg" width="30px"><span>晴天</span> 👍（1） 💬（2）<div>老师，请问下生产环境使用ebpf的话，哪个版本的内核合适啊？</div>2022-01-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/1e/63/d5909105.jpg" width="30px"><span>小李同学</span> 👍（1） 💬（1）<div>老师，你好，在arm嵌入式环境中，有没有办法添加这些依赖的库？</div>2022-01-21</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/DYAIOgq83eqKmVMIqxRO00L8J1iatIzeMHwzYb0s762j9B2dicy4P8tciat26cNDgoyMREjtluZEBXGvwz9nUSO2g/132" width="30px"><span>Geek_07f1e3</span> 👍（0） 💬（1）<div>请问下大家写bcc程序都用什么编辑器呀？</div>2023-02-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1b/5d/51/87fc7ef9.jpg" width="30px"><span>Issac慜</span> 👍（0） 💬（1）<div>我怎么感觉不用bcc更容易理解呢</div>2023-02-11</li><br/><li><img src="" width="30px"><span>Geek_b78911</span> 👍（0） 💬（1）<div>老师您好，我没执行完程序以后会有大量输出，有没有什么办法能过滤掉一部分输出呢</div>2023-01-25</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/b5/1d/f2f66e8d.jpg" width="30px"><span>团团-BB</span> 👍（0） 💬（1）<div>云上的Ubuntu最高一般就20.04，环境安装比较折腾，可以有个低点版本的环境说明么</div>2022-03-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/45/9c/5b06d143.jpg" width="30px"><span>芳菲菲兮满堂</span> 👍（0） 💬（2）<div>Traceback (most recent call last):
  File &quot;&#47;home&#47;vagrant&#47;hello.py&quot;, line 4, in &lt;module&gt;
    b.attach_kprobe(event=&quot;do_sys_openat2&quot;, fn_name=&quot;hello_world&quot;)
  File &quot;&#47;usr&#47;lib&#47;python3&#47;dist-packages&#47;bcc&#47;__init__.py&quot;, line 679, in attach_kprobe
    fn = self.load_func(fn_name, BPF.KPROBE)
  File &quot;&#47;usr&#47;lib&#47;python3&#47;dist-packages&#47;bcc&#47;__init__.py&quot;, line 411, in load_func
    raise Exception(&quot;Failed to load BPF program %s: %s&quot; %
Exception: Failed to load BPF program b&#39;hello_world&#39;: Invalid argument

运行hello world的时候提示这个 难道是python 3.9 不兼容？</div>2022-03-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/18/3e/87/ff97c31e.jpg" width="30px"><span>Li. Mr</span> 👍（0） 💬（1）<div>因为实际环境没到openat2的适用环境，倪老师能否也给出openat的开发流程呢？感谢。</div>2022-02-18</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/DYAIOgq83erbrXqgp8iaXnmAc5XtdmUG966ezcVml3TUngUslTlfqSuUib0BnBF640rPC6HibOSXzqKlU2QkftCSw/132" width="30px"><span>Geek_b0b350</span> 👍（0） 💬（2）<div>你们都能找到linux-tool-$(uname -r) linux-head-$(uname -r)这两个包？，我安装以后曝出找不到这两个包</div>2022-02-15</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1b/5d/51/87fc7ef9.jpg" width="30px"><span>Issac慜</span> 👍（0） 💬（1）<div>在搭建开发环境的时候，可能由于某些系统的安全性考虑，导致无法安装所需的内核头文件。后续使用Docker的方式而不行，最后只好选择了重新安装一个新版本的Linux发行版，程序最后也运行起来了</div>2022-02-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/b8/37/e723b8e6.jpg" width="30px"><span>liyi</span> 👍（0） 💬（1）<div>multipass 怎么安装Ubuntu20.10+。我看默认的版本是Ubuntu 20.04 LTS</div>2022-02-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/3a/39/72d81605.jpg" width="30px"><span>大尾巴老猫</span> 👍（0） 💬（1）<div>Debian 10环境搭建没有成功，demo程序无法运行，换到Debian 11一切正常。</div>2022-02-02</li><br/>
</ul>