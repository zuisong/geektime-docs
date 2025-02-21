上一讲我介绍了JVM内存区域的划分，总结了相关的一些概念，今天我将结合JVM参数、工具等方面，进一步分析JVM内存结构，包括外部资料相对较少的堆外部分。

今天我要问你的问题是，如何监控和诊断JVM堆内和堆外内存使用？

## 典型回答

了解JVM内存的方法有很多，具体能力范围也有区别，简单总结如下：

- 可以使用综合性的图形化工具，如JConsole、VisualVM（注意，从Oracle JDK 9开始，VisualVM已经不再包含在JDK安装包中）等。这些工具具体使用起来相对比较直观，直接连接到Java进程，然后就可以在图形化界面里掌握内存使用情况。

以JConsole为例，其内存页面可以显示常见的**堆内存**和**各种堆外部分**使用状态。

- 也可以使用命令行工具进行运行时查询，如jstat和jmap等工具都提供了一些选项，可以查看堆、方法区等使用数据。
- 或者，也可以使用jmap等提供的命令，生成堆转储（Heap Dump）文件，然后利用jhat或Eclipse MAT等堆转储分析工具进行详细分析。
- 如果你使用的是Tomcat、Weblogic等Java EE服务器，这些服务器同样提供了内存管理相关的功能。
- 另外，从某种程度上来说，GC日志等输出，同样包含着丰富的信息。
<div><strong>精选留言（25）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/11/d9/d5/3834f474.jpg" width="30px"><span>Loading...</span> 👍（58） 💬（12）<div>今天阿里面试官问了我一个问题，我想了很久没想通，希望得到解答。为什么在标记垃圾的时候，需要stop the world</div>2018-07-05</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/49/a5/e4c1c2d4.jpg" width="30px"><span>小文同学</span> 👍（56） 💬（3）<div>班门弄斧，为老师补充一些关于Eden、两个Survivor的细节。
1、大部分对象创建都是在Eden的，除了个别大对象外。
2、Minor GC开始前，to-survivor是空的，from-survivor是由对象的。
3、Minor GC后，Eden的存活对象都copy到to-survivor中，from-survivor的存活对象也复制to-survivor中。其中所有对象的年龄+1
4、from-survivor清空，成为新的to-survivor，带有对象的to-survivor变成新的from-survivor。重复回到步骤2

这是我看这边文章也有的疑问，通过查阅资料理解的，希望可以帮到其他同学</div>2018-07-07</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/b5/26/d635d8d3.jpg" width="30px"><span>铁拳阿牛</span> 👍（21） 💬（2）<div>-XX:NewRatio=value
默认是2
这里说是3面试官还说我记错了😣
</div>2018-07-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/fa/fa/28832dd5.jpg" width="30px"><span>北溟鱼汤</span> 👍（19） 💬（1）<div>java.lang.Runtime类有freeMemory()、totalMemory()等方法可以获取到jvm内存情况，看了一下是本地方法。</div>2018-07-05</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/af/2d/3dd65e6b.jpg" width="30px"><span>xhkk</span> 👍（14） 💬（1）<div>老师，请问如何判断是否有内存泄露</div>2018-07-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/ff/a5/eccc7653.jpg" width="30px"><span>clz1341521</span> 👍（13） 💬（1）<div>java.lang.Runtime类有freeMemory()、totalMemory()等方法可以获取到jvm内存情况，看了一下是本地方法。
另外看到有同学说jmc，jconsole在linux上用不了的问题，其实1可以远程连接，2可以使用xshell</div>2018-08-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/51/0d/14d9364a.jpg" width="30px"><span>L.B.Q.Y</span> 👍（10） 💬（1）<div>jmx可以做到通过代码而不是工具去监控，其实jdk安装包的工具也是对jmx的一个薄层的封装。</div>2018-07-05</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/24/9d/ba45ff4a.jpg" width="30px"><span>陈道恒</span> 👍（9） 💬（1）<div>当然，也有特殊情况，我们知道普通的对象会被分配在 TLAB 上；如果对象较大，JVM 会试图直接分配在 Eden 其他位置上；如果对象太大，完全无法在新生代找到足够长的连续空闲空间，JVM 就会直接分配到老年代。
        杨老师你好，大对象直接分配到老年代，这里是指多大？有没什么衡量标准？</div>2018-08-15</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTK44Hvr0AreUic5s1gdxGBibTOZy3RiaeA5iccSNW9ibmAIcsNcz3Mb67ZGxRL1rZ3iboLTMndsXr5uX2hA/132" width="30px"><span>ethan</span> 👍（6） 💬（1）<div>jar包发生冲突，如何定位是哪些jar包发生问题</div>2018-07-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/d4/f3/129d6dfe.jpg" width="30px"><span>李二木</span> 👍（4） 💬（1）<div>还有一个就是jstat，可以实时查看gc信息,这个也还是没有工具直观，</div>2018-07-05</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/b7/d4/abb7bfe3.jpg" width="30px"><span>代码狂徒</span> 👍（3） 💬（1）<div>老师，麻烦咨询下，像jconsole和jmc这些图形化的工具不适用于linux 服务器环境下使用吧，我试了下貌似并没有反应，所以对服务器环境内存监控或者问题跟踪，有什么好的工具呢？</div>2018-07-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/01/5e/95f7d928.jpg" width="30px"><span>Hidden</span> 👍（3） 💬（1）<div>新对象都会创建在eden 和from 区域，当发生minor gc时 把这两个区域的存活对象复制到 to区域，然后清理eden 和from 区域，是这样理解吧</div>2018-07-05</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/d4/f3/129d6dfe.jpg" width="30px"><span>李二木</span> 👍（3） 💬（1）<div>除了工具就是命令方式了，用过命令有vmstat，这属于linux的，主要监控cpu和内存使用情况，这里是服务器总体内存，所以这个命令不是非常直观。</div>2018-07-05</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/f5/2f/56117bab.jpg" width="30px"><span>张玮(大圣)</span> 👍（2） 💬（1）<div>当然，也有特殊情况，我们知道普通的对象会被分配在 TLAB 上；如果对象较大，JVM 会试图直接分配在 Eden 其他位置上；如果对象太大，完全无法在新生代找到足够长的连续空闲空间，JVM 就会直接分配到老年代。

这里的较大具体会分配到eden的哪个位置呢，请杨兄指教下</div>2018-07-07</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/cb/de/4d857c5d.jpg" width="30px"><span>Bruce</span> 👍（34） 💬（1）<div>回答一下留言的问题，为什么标记的时候要stop the world，是为了避免在标记的时候又有对象在堆内生成，如果这个对象对其他未标记对象有引用，而这个时候由于gc而清理掉了未标记的对象，会有问题</div>2019-03-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/a5/fb/e78299a6.jpg" width="30px"><span>szh</span> 👍（6） 💬（0）<div>Direct Buffer 的直接内存可以用MXBean查看，相关接口是java.lang.management.BufferPoolMXBean。在JConsole中的MBean java.nio.BufferPool可以看到。</div>2019-07-31</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/45/d8/5f9cb4e4.jpg" width="30px"><span>Liu Xian</span> 👍（2） 💬（0）<div>分析过一次Android上的堆外内存OOM，是通过&#47;proc&#47;pid&#47;maps文件里找到的线索。在Linux和Android上堆外内存基本都是通过操作系统的mmap接口从内存映射区分配的，所以maps文件也可以提供一些分析线索。</div>2019-05-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/2a/32/6354a589.jpg" width="30px"><span>小卡向前冲</span> 👍（2） 💬（0）<div>使用javaagent可以获得对象的大小，但是引入时有点麻烦，查到的资料都说需要将代码放到jar包中，然后在启动时加上 -javaagent:jar包名。
放不知道这个算不算。</div>2018-07-11</li><br/><li><img src="https://wx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTKj4w4lW7ibGEVxPv8wS1CrXKDeBz3RAaAdISxQSD23uUpV3wicsIMepaYZE8GzRcWmSpjet5NDN4MA/132" width="30px"><span>Zm</span> 👍（1） 💬（0）<div>tlab不一定是start到end就会开辟新的空间，可以对其设置参数，允许浪费的空间为800kb，假设剩余1m，新来一个对象为1.2m，则在正常的堆上分配，然后再来一个500kb的对象还会在该线程分配好的空间上分配，这时还剩500kb小于允许浪费的空间800kb，就会对该线程重新分配。</div>2020-12-20</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/E3XKbwTv6WTssolgqZjZCkiazHgl2IdBYfwVfAcB7Ff3krsIQeBIBFQLQE1Kw91LFbl3lic2EzgdfNiciaYDlJlELA/132" width="30px"><span>rike</span> 👍（1） 💬（1）<div>Eden 和 Survivor 的大小是按照比例设置的，如果 SurvivorRatio 是 8，那么 Survivor 区域就是 Eden 的 1&#47;8 大小，也就是新生代的 1&#47;10，因为 YoungGen=Eden + 2*Survivor
“Survivor 区域就是 Eden 的 1&#47;8 大小”，这里的Survivor是指其中的s0或s1，还是两个加起来？</div>2020-01-31</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/ed/4c/4db1d58b.jpg" width="30px"><span>Jeffrey</span> 👍（1） 💬（1）<div>-Xms和-Xmx为什么很多文章都建议设置成一样大？有的解释是增长过程中会引发Full Gc，请问老师是这样么？</div>2019-04-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/b7/d4/abb7bfe3.jpg" width="30px"><span>代码狂徒</span> 👍（1） 💬（1）<div>老师，麻烦咨询下，像jconsole和jmc这些图形化的工具不适用于linux 服务器环境下使用吧，我试了下貌似并没有反应，所以对服务器环境内存监控或者问题跟踪，有什么好的工具呢？</div>2018-07-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1f/62/81/69b09ed8.jpg" width="30px"><span>木槿花</span> 👍（0） 💬（0）<div>如何合理设置java进程的堆内存大小呢？在多进程机器上，设置太大会降费资源，设置太小又怕运行时不够用</div>2022-08-01</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/E3XKbwTv6WTssolgqZjZCkiazHgl2IdBYfwVfAcB7Ff3krsIQeBIBFQLQE1Kw91LFbl3lic2EzgdfNiciaYDlJlELA/132" width="30px"><span>rike</span> 👍（0） 💬（0）<div>Compiler 部分，就是 JIT 的开销，显然关闭 TieredCompilation 会降低内存使用。
按照上面讲的，加上参数-XX:-TieredCompilation后反而变大，jdk11，执行下面两个命令对比的结果
java -XX:NativeMemoryTracking=summary -XX:+UnlockDiagnosticVMOptions -XX:+PrintNMTStatistics HelloWorld
Compiler (reserved=133KB, committed=133KB)
                            (malloc=2KB #42)
                            (arena=131KB #5)

java -XX:NativeMemoryTracking=summary -XX:+UnlockDiagnosticVMOptions -XX:+PrintNMTStatistics -XX:-TieredCompilation -XX:+UseParallelGC HelloWorld
Compiler (reserved=2180KB, committed=2180KB)
                            (malloc=1KB #30)
                            (arena=2179KB #11)</div>2020-01-31</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/E3XKbwTv6WTssolgqZjZCkiazHgl2IdBYfwVfAcB7Ff3krsIQeBIBFQLQE1Kw91LFbl3lic2EzgdfNiciaYDlJlELA/132" width="30px"><span>rike</span> 👍（0） 💬（0）<div>在 JVM 内部，如果 Xms 小于 Xmx，堆的大小并不会直接扩展到其上限，也就是说保留的空间（reserved）大于实际能够使用的空间（committed）。当内存需求不断增长的时候，JVM 会逐渐扩展新生代等区域的大小，所以 Virtual 区域代表的就是暂时不可用（uncommitted）的空间。
这里的Virtual 区域没看懂</div>2020-01-31</li><br/>
</ul>