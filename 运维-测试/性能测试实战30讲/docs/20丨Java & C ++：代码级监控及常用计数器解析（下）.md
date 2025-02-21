在上一篇文章中，我们描述了在Java开发语言中如何抓取方法的执行时间，其中描述的操作也是我们在分析时经常使用的。

今天我们将接着描述如下几点内容：

1. Java语言中如何查找有问题的内存对象。
2. 简单介绍一下在C/C++语言中如何查找方法执行时间和对象的内存消耗。

之所以要描述C/C++语言的相关内容，就是为了告诉你，几乎在任何一语言中都有相应的工具，都有办法捕获到相应的内容。

下面我们来看看如何抓取Java应用中对象占用多大内存，以及如何分辨占用是合理的和不合理的。

## Java类应用查找对象内存消耗

对Java的内存分析通常都落在对JVM的使用上（不要认为我这句话说得片面），再具体一点，说的就是内存泄露和内存溢出。由于现在对象都是可变长的，内存溢出就不常见了；而由于底层框架的慢慢成熟，内存泄露现在也不常见了。

有人说了，那你还啰嗦个什么劲呢？别捉急呀，不常见不等于没有。只是说它不再是No.1级的问题，但是排在No.2级还是没问题的。

如果你的应用有了问题，看到了像这样的图：

![](https://static001.geekbang.org/resource/image/c1/19/c12c874e2048b88e71510ad5fb3af319.png?wh=376%2A96)  
这是我在一个项目中遇到的问题，图片不够清晰，我们只要关注黄线的趋势就好。

之所以把它拿出来说事，是因为这个问题太极端了。上图是近20天的JVM使用率，从曲线的趋势上就可以看出来，它存在明显的内存泄露，但是又泄露得非常非常慢。这个系统要求24x365运行。
<div><strong>精选留言（10）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/24/24/73/91ef894b.jpg" width="30px"><span>kaixin</span> 👍（10） 💬（1）<div>时间和空间。
时间是指执行的够不够快，快才能在同样的时间内处理更多的请求
空间就是内存，每个形成的对象小，或者使用后释放快，才能在固定内存下有更多对象可以使用内存</div>2021-01-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/77/72/8f77ddb0.jpg" width="30px"><span>johnny</span> 👍（4） 💬（1）<div>对代码的性能分析过程中，主要是哪两点？
1.运行速度
2.占用内存
针对代码分析的这两点，有什么样的分析链路？
链路的分析思路还是先分析系统架构、然后分段，分层，先全局后定向。
运行速度分析链路
响应时间长-&gt;分段拆分时间-&gt;操作系统-&gt;进程-&gt;线程-&gt;方法或函数CPU执行时间
占用内存分析链路
响应时间长-&gt;分段拆分时间-&gt;操作系统-&gt;进程-&gt;线程-&gt;对象或变量内存使用情况</div>2021-05-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/2f/f4/2dede51a.jpg" width="30px"><span>小老鼠</span> 👍（2） 💬（2）<div>代码级的性能分析应该由开发人员作还是测试人员作？我个人观点是测试人员测试是否存在性能问题，比如内存泄漏，再由开发人员去定位，当然有全栈工程师更好。</div>2020-02-25</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1f/88/1b/deca1dba.jpg" width="30px"><span>王顺</span> 👍（0） 💬（1）<div>时间和空间</div>2021-11-22</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTJJ6G2xZvNRmhyXBjmGbI5G8icGCCMPupr6yxZ1IcURwp7GTRHcpWGWpg9A0fLlyicmVdDwzqZqwiaOQ/132" width="30px"><span>jy</span> 👍（0） 💬（1）<div>原文内容：“实际上，这张图说明以下四点：年轻代（第三列）、年老代（第四列）全满了，持久代在不断增加，并且也没有释放过。两个保留区（第一列、第二列）都是空的。Yonug GC（第六列）已经不做了。Full GC（第八列）一直都在尝试做回收的动作，但是一直也没成功，因为年轻代、年老代都没回收下来，持久代也在不停涨。如果出现了 1 和 2 的话，不用看什么具体对象内存的消耗，只要像网上那些只玩 JVM 参数的人一样，调调参数就行了。“

问题：具体是如何调参数呢？</div>2021-06-25</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/3b/01/7a0bfa9a.jpg" width="30px"><span>alley</span> 👍（0） 💬（1）<div>老师，我在平时测试性能基线中发现有缓慢的性能泄露问题，开发说不用管，触发FullGC来回收内存；那FullGC的时候，是不是系统业务不可用？</div>2021-01-04</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1f/87/6f/a1c56129.jpg" width="30px"><span>chailyn</span> 👍（0） 💬（1）<div>卡在分析了，windows系统如何监控分析c&#47;c++语言程序的CPU，感觉还是很懵呀</div>2020-10-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/7e/3e/82202cc8.jpg" width="30px"><span>月亮和六便士</span> 👍（0） 💬（3）<div>高老师，1. gc， FGC 多久一次算正常？我经常看到书籍上说什么频繁的Fgc ，不知道怎么样算频繁，2.  jvm设置多大 与总内存有比例关系么，比如我有120G内存，我设置3G xmx  这个要怎么确定？</div>2020-04-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/39/fa/a7edbc72.jpg" width="30px"><span>安排</span> 👍（0） 💬（1）<div>valgrind分析大型程序比较慢，有没有其他好用的快的工具呢？</div>2020-04-01</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/40/8c/bc76ecd3.jpg" width="30px"><span>吴小喵</span> 👍（0） 💬（1）<div>老师，为什么我的jvisualvm没有Deltas </div>2020-02-28</li><br/>
</ul>