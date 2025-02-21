你好，我是LMOS。

前面我们了解了网络的宏观架构，建立了网络模块知识的大局观，也进行了实际的组网实践。现在我们来瞧一瞧Linux的网络程序，不过想要入门Linux的网络编程，套接字也是一个绕不开的重要知识点，正是有了套接字，Linux系统才拥有了网络通信的能力。而且网络协议的最底层也是套接字，有了这个基础，你再去看相关的网络协议的时候也会更加轻松。

我会通过两节课的内容带你了解套接字的原理和具体实现。这节课，我们先来了解套接字的作用、工作原理和关键数据结构。下一节课，我们再一起研究它在Linux内核中的设计与实现。

好，让我们开始今天的学习吧。

## 如何理解套接字

根据底层网络机制的差异，计算机网络世界中定义了不同协议族的套接字（socket），比如DARPA Internet地址（Internet套接字）、本地节点的路径名（Unix套接字）、CCITT X.25地址（X.25 套接字）等。

我们会重点讲解跟网络子系统和TCP/IP协议栈息息相关的一种套接字——Internet 套接字。如果你对其他类型的套接字有兴趣，可以自行阅读这里的[资料](https://elixir.bootlin.com/linux/v5.10.23/source/include/linux/socket.h)。

Internet套接字是TCP/IP协议栈中传输层协议的接口，也是传输层以上所有协议的实现。
<div><strong>精选留言（7）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/28/58/ef/e7c7f2b4.jpg" width="30px"><span>不及胜于过之</span> 👍（0） 💬（2）<div>昨天一天撸完，体会很深，专门写了一个学习总结与linux的爬坡之路，https:&#47;&#47;mp.weixin.qq.com&#47;s&#47;XqXIvEfhNPXQ1RSs0XeFUQ
麻烦多指正，过去一直持续在学linux，这个时候看到您的文章对我是一个很好的沉淀与认知突破，巨感谢大佬</div>2021-08-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/28/58/ef/e7c7f2b4.jpg" width="30px"><span>不及胜于过之</span> 👍（8） 💬（2）<div>今天一天看完了您的所有课程，收获非常非常大。尤其是：要实现一个功能模块，首先要设计出相应的数据结构(以及这些数据结构的管理数据结构，比如链表等)，基于数据结构设计初始化函数以及该功能模块对应的业务函数。为学习操作系统模块或所有技术项目代码提供了思路，感谢东哥。</div>2021-08-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/52/40/e57a736e.jpg" width="30px"><span>pedro</span> 👍（8） 💬（1）<div>进程间的通信方式有很多，比如说管道，共享内存，信号等，但这些通信方式都有一个很大的局限性，那就是无法跨物理机通信，只能与同一个机器上的其它进程通信，而套接字恰好打破了这个桎梏，只要你在线上(网络上)，我就可以通过ip地址打你电话，和你说话！</div>2021-08-06</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/2d/06/30/c26ea06a.jpg" width="30px"><span>艾恩凝</span> 👍（0） 💬（2）<div>哎，说实话从本科开始就讨厌网络，现在依然如此</div>2022-05-16</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1a/85/87/727142bc.jpg" width="30px"><span>MacBao</span> 👍（0） 💬（1）<div>套接字可以跨主机，其他的不可以</div>2021-08-06</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/29/bf/e1/deab777f.jpg" width="30px"><span>摘桃慢</span> 👍（1） 💬（0）<div>好多新的名字出现，有些抽象，希望能够形象一些。不知道能不能举个例子？</div>2023-07-16</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/27/ee/52/cda34b19.jpg" width="30px"><span>Mike_Han</span> 👍（0） 💬（0）<div>老师，有个疑问，文中说到：“结合上面代码我们发现，内核使用 struct inet_protosw 数据结构实现的协议交换表，将应用程序通过 socketcall 系统调用指定的套接字操作，转换成对某个协议实例实现的套接字操作函数的调用。”为什么不直接调用 socket 中的 ops（ops 直接指向具体协议的操作）呢</div>2021-10-21</li><br/>
</ul>