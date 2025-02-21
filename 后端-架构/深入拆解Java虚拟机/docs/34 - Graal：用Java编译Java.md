最后这三篇文章，我将介绍Oracle Labs的GraalVM项目。

GraalVM是一个高性能的、支持多种编程语言的执行环境。它既可以在传统的OpenJDK上运行，也可以通过AOT（Ahead-Of-Time）编译成可执行文件单独运行，甚至可以集成至数据库中运行。

除此之外，它还移除了编程语言之间的边界，并且支持通过即时编译技术，将混杂了不同的编程语言的代码编译到同一段二进制码之中，从而实现不同语言之间的无缝切换。

今天这一篇，我们就来讲讲GraalVM的基石Graal编译器。

在之前的篇章中，特别是介绍即时编译技术的第二部分，我们反反复复提到了Graal编译器。这是一个用Java写就的即时编译器，它从Java 9u开始便被集成自JDK中，作为实验性质的即时编译器。

Graal编译器可以通过Java虚拟机参数`-XX:+UnlockExperimentalVMOptions -XX:+UseJVMCICompiler`启用。当启用时，它将替换掉HotSpot中的C2编译器，并响应原本由C2负责的编译请求。

在今天的文章中，我将详细跟你介绍一下Graal与Java虚拟机的交互、Graal和C2的区别以及Graal的实现细节。
<div><strong>精选留言（9）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/0f/9b/2f/b7a3625e.jpg" width="30px"><span>Len</span> 👍（26） 💬（1）<div>我们可不可以把 profile 和编译的机器码保存到磁盘，在代码和运行平台不变的情况下，下次启动（或部署多实例）的时候直接装载这部分数据？这算作是一种系统预热的可行性方案吗？</div>2018-10-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/1e/a5/85b05303.jpg" width="30px"><span>金龙</span> 👍（10） 💬（2）<div>GraalVM和JVM是什么关系？它在OpenJDK上是怎么运行的？求解惑</div>2018-10-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/a9/84/c87b51ce.jpg" width="30px"><span>xiaobang</span> 👍（7） 💬（1）<div>openjdk里Graal自身的及时编译是调用Graal自身吗？如果这么做会不会出现无穷递归？</div>2018-10-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/be/c6/8a92bd2e.jpg" width="30px"><span>ZY</span> 👍（3） 💬（1）<div>GraalVM大概什么时候会发布release版本？</div>2018-10-16</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/67/f4/9a1feb59.jpg" width="30px"><span>钱</span> 👍（7） 💬（0）<div>阅过留痕
最后几篇了，这个专栏马上结束了，回头想想自己都学到了那些内容了呢？
JVM的各个部分从外到内，由浅入深老师都讲到了，大部分内容是都挺明白了，有些还有待消化，不过下面还要继续的学习，专栏的目标是带我们入门！

本节讲解的Graal先混个脸熟，以后继续深入

1：Graal是一个编译器，是使用java语言编写的编译器，既然是编译器就拥有编译器的各种特点（主要负责接收JAVA字节码，并且声称可以直接运行的二进制码），当然，后来者通常比先来的会多一些特点，否则也没有必要来啦！Graal性能相对来说更好一点、更具模块化、更易维护（相对C2而言）Graal编译器是一个即时编译器，从JDK9就被集成到JDK中了，当然，可能还不成熟时作为一个实验性质的编译器集成到JDK中的，可以有选择的行的启动或者关闭。

2：Graal编译器是GraalVm的基石，编译器是VM的一部分，相对来说比较独立，它和JVM的交互主要有如下三部分，
2-1）响应变异请求
2-2）获取编译所需的元数据（如：类、方法、字段）和反应程序执行状态的profile
2-3）将生成的二进制码不熟至代码缓存里

3：Graal和JVM通过JVMCI来实现解耦，本质是通过java语言层面的接口来实现解耦的

嗯，感觉有些懵懂，专栏快结束了，老师辛苦了，希望老师来点随学随用的分析jvm性能瓶颈和解决方式的例子，当然，这个部分内容网上也比较多，只是希望更系统一点，举几个高频的示例！

</div>2018-10-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/47/80/5c6289b6.jpg" width="30px"><span>xiangguang</span> 👍（2） 💬（0）<div>求证: 同样的代码，使用jdk1.6编译的和使用jdk1.8编译，在同样的jdk1.8的jvm环境运行，性能是否有差异？
是不是需要看1.6的javap和1.8的javap 出来的字节码是否有差别？</div>2019-04-17</li><br/><li><img src="" width="30px"><span>Geek_2ab487</span> 👍（1） 💬（2）<div>你好，我在使用graalVM native-image进行部署spring项目时有几个问题，1.打包成可执行文件后，jvm一些参数包括gc、堆栈大小这些要怎么设置 2.使用native-image提前编译后，实际运行时还会进行即时编译吗？</div>2020-07-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/b7/ae/a25fcb73.jpg" width="30px"><span>colin</span> 👍（1） 💬（2）<div>其实我好奇openJdk是不是可以代替Oracle 的Jdk呢</div>2019-05-31</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1f/67/4f/aafc8614.jpg" width="30px"><span>MasterOogway</span> 👍（0） 💬（0）<div>JMH跑了一段时间，graal比默认的性能提升约5%。应该不是误差</div>2021-04-20</li><br/>
</ul>