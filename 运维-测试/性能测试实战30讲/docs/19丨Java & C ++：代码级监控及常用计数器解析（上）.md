在性能测试分析中，有一部分人存在着一个思路上的误解，那就是一开始就一头扎进代码里，折腾代码性能。这是我非常反对的一种做法。

事实上，要想这么做，有一个前提，那就是架构中的其他组件都经过了千锤百炼，出现问题的可能性极低。

实际上，我凭着十几年的经验来看，大部分时候，代码出现严重性能瓶颈的情况还真是不多。再加上现在成熟的框架那么多，程序员们很多情况下只写业务实现。在这种情况下，代码出现性能瓶颈的可能性就更低了。

但我们今天终归要说代码级的监控及常用的计数器。如何去评估一个业务系统的代码性能呢？在我看来，分析的思路是下面这个样子的。

![](https://static001.geekbang.org/resource/image/ee/e3/eebce7bd7cab91685baf4a9a526be9e3.jpg?wh=1542%2A1112)

从上图可以看到，分析的时候有两个关键点：执行时间和执行空间。我相信很多人都清楚，我们要很快找到执行时间耗在哪一段和空间耗在哪里。

现在我们来实际操作一下，看如何判断。

## Java类应用查找方法执行时间

首先你得选择一个合适的监控工具。Java方法类的监控工具有很多，这里我选择JDK里自带的jvisualvm。

顺便说一下，我的Java版本号是这个：

```
(base) GaoLouMac:~ Zee$ java -version
java version "1.8.0_111"
Java(TM) SE Runtime Environment (build 1.8.0_111-b14)
Java HotSpot(TM) 64-Bit Server VM (build 25.111-b14, mixed mode)
```

打开应用服务器上的JMX之后，连上jvisualvm，你会看到这样的视图。

![](https://static001.geekbang.org/resource/image/76/36/76e17407985e427e832c0de988cc8f36.png?wh=1254%2A727)

这里再啰嗦一下我们的目标，这时我们要找到消耗CPU的方法，所以要先点`Sampler - CPU`，你可以看到如下视图。
<div><strong>精选留言（16）</strong></div><ul>
<li><img src="" width="30px"><span>嘟嘟爱学习</span> 👍（11） 💬（2）<div>我觉得某些生产环境还是可以直接上APM的：
1. 能接受10%性能损耗的，比如原来耗时1秒，上了变成1.1秒其实感觉不明显；原来高峰期CPU使用率30%，上了变成40%也还在可接受范围内；
2. APM的成功失败不影响业务的运行，就是即使APM挂了，业务也还能正常运行；
3. 在docker+k8且又有大量虚机大量服务的情况下，上APM也是一个方案，不然当出现问题时要在那么多服务里面把问题定位到，用jmx这类监控很容易措手不及和慌手慌脚。
4. 现在好些公司没有专职性能测试，好些系统没有经过性能测试就上线的，此时APM是开发和运维人员的一个救命稻草了，这种公司我相信很多。</div>2020-02-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/1d/de/62bfa83f.jpg" width="30px"><span>aoe</span> 👍（8） 💬（1）<div>在我知识范围内Java最强的监控工具是Oracle 开发的 JMC，没有之一。前Oracle首席工程师在 极客时间的《Java核心技术面试精讲》专栏 | 第26讲 | 如何监控和诊断JVM堆内和堆外内存使用？ 文中提到：“我这里特别推荐Java Mission Control（JMC），这是一个非常强大的工具，不仅仅能够使用JMX进行普通的管理、监控任务，还可以配合Java Flight Recorder（JFR）技术，以非常低的开销，收集和分析 JVM 底层的 Profiling 和事件等信息。目前， Oracle 已经将其开源，如果你有兴趣请可以查看 OpenJDK 的Mission Control项目。”</div>2020-10-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/fa/20/0f06b080.jpg" width="30px"><span>凌空飞起的剪刀腿</span> 👍（4） 💬（1）<div>使用strace 跟踪进程流程</div>2020-04-03</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/3b/01/7a0bfa9a.jpg" width="30px"><span>alley</span> 👍（2） 💬（1）<div>perftop 可以查看CPU热点函数</div>2021-02-16</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/2e/de/80/791d0f5e.jpg" width="30px"><span>娜娜</span> 👍（1） 💬（1）<div>请问老师C++、C的怎么监控</div>2022-07-28</li><br/><li><img src="" width="30px"><span>Geek_6a9aeb</span> 👍（1） 💬（1）<div>老师，为啥说代码造成瓶颈不多呢，高并发带来java线程死锁的情况 是很常见的代码问题吧</div>2021-01-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1b/3f/cc/d02e2c1e.jpg" width="30px"><span>老街头的猫🐱。</span> 👍（1） 💬（1）<div>高老师，这个第一个调用栈是用什么命令打出来的，根据什么关键字？在 jvisualvm中没看到进程ID呀？</div>2020-10-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/7e/3e/82202cc8.jpg" width="30px"><span>月亮和六便士</span> 👍（1） 💬（1）<div>高老师：1. 打调用栈的时候，怎么保证打印出来的正好是自己写的方法的调用栈，而不是一堆没用的调用栈，我连续打几次都不是自己写的方法的调用栈，这时候我觉得一定有什么技巧，而我不知道。2，interrunpts --&gt; softirqs 怎么对应，我知道interrunpts 逻辑终端号是 45，中断设备是网卡，在softirqs中没有找到45这个号，里面只有网卡设备模块。准备把老师的专栏，手抄一遍，然后练习一遍，然后再理解一遍</div>2020-04-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/18/b2/dc/67e0e985.jpg" width="30px"><span>顺利</span> 👍（1） 💬（1）<div>分段拆分时间如何做呢老师，没找到前面的相应内容。有什么工具吗？</div>2020-02-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/ae/f5/a17bbcc9.jpg" width="30px"><span>蜡笔小新爱看书</span> 👍（0） 💬（1）<div>打开应用服务器上的 JMX 之后，连上 jvisualvm，你会看到这样的视图。

这个具体是怎么操作？能说明一下吗？</div>2023-07-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/24/0f/a8/956452cd.jpg" width="30px"><span>蔚来懿</span> 👍（0） 💬（1）<div>老师，学到这一节了，为啥我还是不知道，响应时间长，怎么定位到代码这一层了，前面系统层的如何定位（操作系统、进程、线程耗时，这块在怎么得出时间呢？），么有看到在哪里可以分析出来的？</div>2021-01-16</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1a/9f/c2/3d1c2f88.jpg" width="30px"><span>蔡森冉</span> 👍（0） 💬（1）<div>降到agent我记得在华为云控制台要监控服务器就是安装了这个东西的</div>2020-03-23</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/PiajxSqBRaEKkXmlsKCY7hhNIjJFd0wxtd7CDySRrvdknyUoZd02vUWq4o1HS6r8y5nAAcCypvuxDdQK5BGV4Eg/132" width="30px"><span>目标就是这么明确</span> 👍（0） 💬（1）<div>清晰</div>2020-03-20</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/6Be8vjNk03LEXMl52vONOQvdKTL1MWPR6OsAGEDsHIZXw9FibW8c4YtNL6HAmB8wRkDNIEx15xawJ9PWLW4y1UA/132" width="30px"><span>董飞</span> 👍（0） 💬（1）<div>越来越看不懂了，老师，推荐下这方面的资料。</div>2020-03-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/10/dc/96476998.jpg" width="30px"><span>Hulk</span> 👍（2） 💬（0）<div>Arthas</div>2020-02-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/2f/f4/2dede51a.jpg" width="30px"><span>小老鼠</span> 👍（0） 💬（1）<div>打时间戳呀</div>2020-02-18</li><br/>
</ul>