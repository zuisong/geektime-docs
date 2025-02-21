你好，我是康杨。今天这节课我们来聊聊JVM的运行时数据区。了解JVM的方法执行内存模型，掌握更多提升Java程序性能的技巧。

![图片](https://static001.geekbang.org/resource/image/2c/39/2c18969c0cbf8dd84f3be6fbfa421939.png?wh=1920x890)

运行时数据区（Runtime Data Area）用于提供JVM运行时的内存空间的数据。以线程的视角出发，这个区域又分成线程共享区域和线程独享区域。

线程的独享区域由**程序计数器、虚拟机栈（VM栈）和本地方法栈**构成，它们的使用寿命与线程的运行时间相同，因此可以有效避免垃圾回收的麻烦，并且可以根据线程的不断发展进行相应的调整。

![图片](https://static001.geekbang.org/resource/image/b5/83/b542607579b27a9d1424e80985dee383.png?wh=1920x944)

线程共享区域包括堆和方法区，方法区用于存储类的结构信息，堆用于存储对象实例等。这节课我们将聚焦在线程独享区域，方法区和堆的介绍我将在类加载器和GC的部分为你详细介绍。

## 程序计数器

程序计数器属于线程私有资源，每个线程都有一个唯一的属于自己的程序计数器，指定线程所执行的字节码指令的行号。执行Java方法时，这个地方记录的是线程正在执行的字节码的指令地址，如果执行本地方法，这个地方的值为空。

### 应用场景

程序计数器是字节码解释器的核心，它可以根据程序计数器的数值，为下一步的字节码操作提供准确的指引，从而使程序更加高效地完成任务。

在实际的流程控制中，循环、跳转、分支等基础功能的运作也依赖于程序计数器。在涉及多线程的环境下，程序计数器保存了当前线程运行的位置，这样在线程再次被调用时，可以了解到这个线程之前运行到了什么地方。
<div><strong>精选留言（9）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/21/e4/b4/889954ca.jpg" width="30px"><span>Levi</span> 👍（3） 💬（1）<div>老师请教一个问题，Slot只保存局部变量的值吗，比如a=2，slot中保存的是2这个数据值，那a这个变量被保存在哪里呢？</div>2023-08-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/38/c6/78/dc201b84.jpg" width="30px"><span>记得晚睡</span> 👍（2） 💬（2）<div>好难啊😭😭😭</div>2023-09-20</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/DYAIOgq83eoZqcVJzUjfu5noOW6OPAh6ibrBicibLmicibnVyVLHdf7GwAzf2th5s1oQ9pUbLpmq2mlVBauUZn8QUnw/132" width="30px"><span>funnyx</span> 👍（1） 💬（1）<div>请问老师，有没有什么方法在jvm运行时，向其中添加class文件让其加载。</div>2023-09-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/d0/91/89123507.jpg" width="30px"><span>Johar</span> 👍（1） 💬（1）<div>程序计数器是记录程序正在执行字节码的指令地址，但是执行本地方法，为空。
请问一下老师，执行本地方，程序计数器记录的指令地址为空，在cpu时间片切换时，怎么再次恢复本地方法的执行上下文？</div>2023-08-25</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/18/75/bc/89d88775.jpg" width="30px"><span>Calvin</span> 👍（0） 💬（1）<div>大佬好：
请问下“运行时常量池”包括哪些东西，在运行时数据区的哪个位呢置（本文好像没说？）？
与“字符串常量池”有什么区别，为什么还需要特意再分出来多一个常量池呢？</div>2023-08-25</li><br/><li><img src="" width="30px"><span>Geek1254</span> 👍（5） 💬（0）<div>看了两节，感觉讲的东西太浅，不适合工作多年的老鸟。要硬干货</div>2023-09-15</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/7a/56/29877cb9.jpg" width="30px"><span>临风</span> 👍（1） 💬（0）<div>1、JVM 中方法执行的内存模型对应的是运行时数据区的那个区域？
运行时数据区包括程序计数器、虚拟机栈、本地方法栈、方法区、堆区。一个执行方法对应虚拟机栈的一个栈帧，栈帧会保存局部变量表、操作数栈、动态链接、返回地址等。

2、这节课你学到了哪些提升程序性能的技巧？
一是不要定义多余的变量；二是方法不要过长。这两个都是编程规范要求的，之前以为仅仅只是为了可读性，还是为了避免局部变量表空间的浪费。</div>2023-08-27</li><br/><li><img src="" width="30px"><span>Geek_0e0559</span> 👍（0） 💬（0）<div>针对每个栈帧，我们还需要提供一个引用，以此在运行时常量池内可以识别出对应的方法，且在方法被调用的过程中能实现动态链接。-- 这句话没看明白</div>2024-02-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/25/87/f3a69d1b.jpg" width="30px"><span>peter</span> 👍（0） 💬（1）<div>请教老师几个问题：
Q1：动态链接部分的methodA方法的疑问：
--- 此函数没有参数，为什么args_size是1？
--- 此函数没有局部变量，为什么locals是1？
--- stack=2是什么意思？
Q2：sun hotpot将两个栈合并，虚拟机栈是执行Java代码的，那么本地方法还能执行C或C++代码吗？
Q3：本课所说的“动态链接”，主要是指“动态绑定”，即多态，不是指“动态链接库”一类的内容，对吗？ 
Q4：Java程序可以使用C或C++的DLL吗？</div>2023-08-26</li><br/>
</ul>