你好，我是庄振运。

我们来继续学习生产实践中的案例。在生产实践中，为了降低公司运营成本，更好地利用系统容量，并提高资源使用率，我们经常会让多个应用程序，同时运行在同一台服务器上。

但是，万事有利就有弊。这几个共存的应用程序，有可能会互相影响；有时还会导致严重的性能问题。我就遇到过，几个程序同时运行，最后导致吞吐量急剧下降的情况。

所以，今天我们就来探讨，当多个Java应用程序共存在一个Linux系统上的时候，会产生哪些性能问题？我们又该怎么解决这些问题？

## 怎样理解多程序互相干扰？

为了更好地理解后面的性能问题，你需要先了解一下应用程序内存管理机制的背景知识。我们运行的是Java程序，所以先快速复习一下**Java的JVM内存管理机制**。

Java程序在Java虚拟机JVM中运行，JVM使用的内存区域称为**堆**。JVM堆用于支持动态Java对象的分配，并且分为几个区域，称为“代”（例如新生代和老年代）。Java对象首先在新生代中分配；当这些对象不再被需要时，它们会被称为GC（Garbage Collection）的垃圾回收机制收集。发生GC时，JVM会从根对象开始，一个个地检查所有对象的引用计数。如果对象的引用计数降为零，那就删除这个对象，并回收使用这个对象相应的存储空间。
<div><strong>精选留言（7）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/14/20/1d/0c1a184c.jpg" width="30px"><span>罗辑思维</span> 👍（2） 💬（1）<div>老师的文笔也让想到两句诗：随风潜入夜，润物细无声。</div>2020-03-07</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/18/81/83b6ade2.jpg" width="30px"><span>好吃不贵</span> 👍（1） 💬（1）<div>老师讲的非常赞，又重温了Linux的page reclaim部分。学到了好多，比如何时控制THP的开关，以及THP的缺点。习题猜测是文件系统预先读取很多小文件时有影响，比如小于4kB的文件，而通常预读有128kB，可能会造成浪费，比如大量读写磁盘，导致D状态，影响性能？不过只是猜测，希望到时候看到老师的统一习题解答:)</div>2020-01-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/18/ce/80/f9f950f1.jpg" width="30px"><span>张翠山</span> 👍（0） 💬（1）<div>java应用程序运行时，发现一个现象cpu sys偏高，大约4到5，遇到这种问题。如何着手排查和优化？</div>2020-05-04</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/17/27/2a/a914cd3f.jpg" width="30px"><span>若镜</span> 👍（0） 💬（1）<div>老师   有经验说 非ibm系的jvm 堆内存 xms xmx最好设置成一样  以减少内存碎片  影响gc   不知是不是靠谱说？  内存碎片说  是不是和THP有关？</div>2020-02-04</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/0f/70/cdef7a3d.jpg" width="30px"><span>Joe Black</span> 👍（0） 💬（1）<div>请问文中说的程序吞吐量是什么意思？比如那个12K&#47;秒，具体指的什么？是分配内存的调用吗？另外THP可以随时打开或关闭吗？我以为只能在系统启动时设定呢</div>2020-01-31</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/75/dd/9ead6e69.jpg" width="30px"><span>黄海峰</span> 👍（4） 💬（0）<div>这篇干货了，以前看过好多关于jvm调优的文章或教程都没有提到这些知识点。。</div>2020-01-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/67/f4/9a1feb59.jpg" width="30px"><span>钱</span> 👍（0） 💬（0）<div>这篇厉害，多个应用程序在同一台机器上，由于一台机器的各种资源都是有限的，多个应用程序之间即使不会发生争抢的现象，但是也会是一种彼消此涨的使用模式，老师讲的很细致，开眼了！</div>2020-03-11</li><br/>
</ul>