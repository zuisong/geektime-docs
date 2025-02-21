你好，我是海纳。

上一节课中，我们讲到GC算法大致可以分为两大类：引用计数法和基于可达性分析的算法。在基于可达性分析的GC算法中，最基础、最重要的一类算法是基于copy的GC算法（后面简称copy算法）。

Copy算法是最简单实用的一种模型，也是我们学习GC算法的基础。而且，它被广泛地使用在各类语言虚拟机中，例如JVM中的Scavenge算法就是以它为基础的改良版本。所以，掌握copy算法对我们后面的学习是至关重要的。

这一节课，我们就从copy算法的基本原理开始讲起，再逐步拓展到GC算法的具体实现。这些知识将帮助你对JVM中Scavenge的实现有深入的理解，并且让你正确地掌握Scavenge GC算法的参数调优。

## 最简单的copy算法

基于copy的GC算法最早是在1963年，由Marvin Minsky提出来的。这个算法的基本思想是把某个空间里的活跃对象复制到其他空间，把原来的空间全部清空，这就相当于是把活跃的对象从一个空间搬到新的空间。因为这种复制具有方向性，所以我们把原空间称为From空间，把新的目标空间称为To空间。

分配新的对象都是在From空间中，所以From空间也被称为**分配空间（Allocation Space）**，而To空间则相应地被称为**幸存者空间（Survivor Sapce）**。在JVM代码中，这两套命名方式都会出现，所以搞清楚这点比较有好处。我们这节课为了强调拷贝进行的方向，选择使用From空间和To空间来分别指代两个空间，而尽量不使用分配空间和幸存者空间的说法。
<div><strong>精选留言（8）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/10/cd/ed/825d84ee.jpg" width="30px"><span>费城的二鹏</span> 👍（2） 💬（1）<div>通过信号量通知，然后在编译生成的代码中插入检查点。用于检查信号量，判断是否需要停顿。</div>2021-12-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/18/39/d2/845c0e39.jpg" width="30px"><span>送过快递的码农</span> 👍（1） 💬（1）<div>老师，关于这个我有两个疑问
1，this是不是就是对象头部最顶端的内存地址
2，我们在复制算法执行完之后，对象地址发生改变。我们业务线程里面的栈里面的引用，啥时候变更的呢？比如Object obj = new Object(); 这个被多个线程栈里面都有这个地址，这个值更新的问题，是标志的时候，通过记一个列表，然后统一更新的么？这个感觉也挺复杂的</div>2021-12-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1d/85/d2/045c63fb.jpg" width="30px"><span>王建新</span> 👍（0） 💬（1）<div>请问，最后的问题，线程的停止时sleep吗</div>2021-12-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/d4/f3/129d6dfe.jpg" width="30px"><span>李二木</span> 👍（0） 💬（1）<div>safepoint?</div>2021-12-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/08/ab/caec7bca.jpg" width="30px"><span>humor</span> 👍（0） 💬（0）<div>。所以 JDK6 以前的 JVM 使用了广度优先的非递归遍历，而在 JDK8 以后，已经把广度优先算法改为深度优先了，尽管这样做需要额外引用一个独立的栈。

老师，这儿是不是写错了，jdk6到jdk8之间用的是什么算法啊🤣</div>2024-08-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/08/ab/caec7bca.jpg" width="30px"><span>humor</span> 👍（0） 💬（0）<div>所以 JDK6 以前的 JVM 使用了广度优先的非递归遍历，而在 JDK8 以后，已经把广度优先算法改为深度优先了，尽管这样做需要额外引用一个独立的栈。</div>2024-08-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/f8/ba/d28174a9.jpg" width="30px"><span>Geek_zbvt62</span> 👍（0） 💬（0）<div>看过中村成洋那本《垃圾回收的算法与实现》，这节课的伪代码还是挺熟悉的。
我比较好奇的是，在栈帧的那部分根，是怎么统计出来的，是要在生成机器码的时候加入一个操作，每在栈上或者是寄存器里保存一个值（就是对象的引用）时，同时还要操作某个数据结构来记录一下么？而且在栈帧销毁之前，还要从这个数据结构中将对应引用的数据删除</div>2023-09-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1d/85/d2/045c63fb.jpg" width="30px"><span>王建新</span> 👍（0） 💬（3）<div>“使用 scanned 指针将非递归的广度优先遍历所需的队列，巧妙地隐藏在了 To 空间中”
---这个不是特别理解，有人能帮忙解答下吗</div>2021-12-24</li><br/>
</ul>