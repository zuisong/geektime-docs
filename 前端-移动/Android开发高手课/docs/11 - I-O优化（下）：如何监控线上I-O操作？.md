通过前面的学习，相信你对I/O相关的基础知识有了一些认识，也了解了测量I/O性能的方法。

但是在实际应用中，你知道有哪些I/O操作是不合理的吗？我们应该如何发现代码中不合理的I/O操作呢？或者更进一步，我们能否在线上持续监控应用程序中I/O的使用呢？今天我们就一起来看看这些问题如何解决。

## I/O跟踪

在监控I/O操作之前，你需要先知道应用程序中究竟有哪些I/O操作。

我在专栏前面讲卡顿优化的中提到过，Facebook的Profilo为了拿到ftrace的信息，使用了PLT Hook技术监听了“atrace\_marker\_fd”文件的写入。那么还有哪些方法可以实现I/O跟踪，而我们又应该跟踪哪些信息呢？

**1. Java Hook**

出于兼容性的考虑，你可能第一时间想到的方法就是插桩。但是插桩无法监控到所有的I/O操作，因为有大量的系统代码也同样存在I/O操作。

出于稳定性的考虑，我们退而求其次还可以尝试使用Java Hook方案。以Android 6.0的源码为例，FileInputStream的整个调用流程如下。

```
java : FileInputStream -> IoBridge.open -> Libcore.os.open 
-> BlockGuardOs.open -> Posix.open
```

在[Libcore.java](http://androidxref.com/6.0.1_r10/xref/libcore/luni/src/main/java/libcore/io/Libcore.java)中可以找到一个挺不错的Hook点，那就是[BlockGuardOs](http://androidxref.com/6.0.1_r10/xref/libcore/luni/src/main/java/libcore/io/BlockGuardOs.java)这一个静态变量。如何可以快速找到合适的Hook点呢？一方面需要靠经验，但是耐心查看和分析源码是必不可少的工作。
<div><strong>精选留言（9）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/17/2e/13/598bd22b.jpg" width="30px"><span>gmm</span> 👍（5） 💬（1）<div>想问下 libjavacore.so、libopenjdkjvm.so、libopenjdkjvm.so 是系统的共享库，为什么 hook 修改了这些库，不会影响到其他的 APP 呢</div>2019-11-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/e8/fd/035f4c94.jpg" width="30px"><span>欢乐小熊</span> 👍（5） 💬（2）<div>看了 Matrix IO 监控的源码, 被其骚操作震惊了, 通过 .so 库名找到了 mmap 区的库地址, 然后 hook 函数的实现, 有趣极了</div>2019-06-21</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTKE7KHyLv1Zian5yzyby3ricSClVp0wwia8evbicGPH9icSAVYHhREVO39CtcHc77x05XONNK61JXoNXfg/132" width="30px"><span>iniesta2014</span> 👍（3） 💬（1）<div>对大文件使用 mmap 或者 NIO 方式? 这样的话，大文件 mmap不是需要很大虚拟内存吗？</div>2019-04-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/55/28/66bf4bc4.jpg" width="30px"><span>荷兰小猪8813</span> 👍（2） 💬（1）<div>2013 年我在做 Multidex 优化的时候，发现代码中...

老师，可以讲一下这个是如何优化的吗？</div>2019-08-31</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/57/2e/0c85eecd.jpg" width="30px"><span>小洁</span> 👍（1） 💬（1）<div>请问下，上面说到&quot;采用 Native Hook 的监控方法性能损耗基本可以忽略&quot;，请问下在监控前和加入Native Hook 之后是通过什么方式去对比性能损耗的而且保证这个统计的准确性，这个统计本身也会是一个损耗吗</div>2019-03-15</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/e7/89/207cc841.jpg" width="30px"><span>HI</span> 👍（1） 💬（1）<div>你好，Canary_Io源码中，检测 重复读，有这样代码
    bool RepeatReadInfo::operator==(const RepeatReadInfo &amp;target) const {
        return target.path_ == path_
            &amp;&amp; target.java_thread_id_ == java_thread_id_
            &amp;&amp; target.java_stack_ == java_stack_
            &amp;&amp; target.file_size_ == file_size_
            &amp;&amp; target.op_size_ == op_size_;
    }
为什么这里要检测 op_size，这个貌似代表的是当前总的buff的大小，这个值就可以代表内容是一样的吗</div>2019-03-06</li><br/><li><img src="" width="30px"><span>林</span> 👍（1） 💬（1）<div>绍文大佬，文章中这句话没理解：“对启动过程需要的文件，我们可以指定在安装包中不压缩”。默认打的apk包中resource、resource.arsc文件不是就是没压缩过的吗？如何指定不压缩类</div>2019-02-19</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/DYAIOgq83erWIeibZYTNuoOACcQsERyhVD0MstTOwvviaSDB3mfJrnm4OTlNEhNvuEiciaHtXyiaASIJvFicBN0kDyrA/132" width="30px"><span>木木哈</span> 👍（4） 💬（0）<div>给大佬献上膝盖</div>2019-03-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/4a/10/365ea684.jpg" width="30px"><span>聪明的傻孩子</span> 👍（3） 💬（0）<div>过去五年，再看依然能学到东西</div>2024-02-21</li><br/>
</ul>