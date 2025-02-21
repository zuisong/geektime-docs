你好，我是海纳。

在前面的课程里，我们讲解了进程内部的具体布局，以及每一个部分的功能和作用。你会发现，所有的例子都是用C/C++写的，我相信你在学习的过程中，心里可能会产生这样的疑问：**那Java和Python语言是怎么运行起来的呢？**

有这个疑问非常合理。我曾经讲过C/C++编译的结果，它在linux上是ELF文件，在windows上是exe文件，这两种文件都可以直接被操作系统加载运行的二进制文件。另外，C/C++源代码也可以被编译成动态链接库文件。

而在Java语言里，程序员都知道Java源代码被javac编译以后，生成的是字节码文件，也就是class文件，而且不管编译所使用的操作系统是什么，相同的Java源码必然得到相同的class文件。class文件显然与上面C/C++编译的二进制文件都不相同，因为它与编译的平台无关。

这节课，我们就围绕着Java是怎么运行起来的这个问题逐层展开，在这个过程中，我会教你如何阅读和分析字节码，以及猜测它的JIT结果。所以通过这节课的学习，你不仅能了解到Java字节码的核心知识、JVM中的解释器和JIT编译器的原理，而且，还能进一步理解JVM虚拟机。在这个基础上，你就能写出更高效、对编译器更友好的程序，而且碰到桥接方法这一类Java中非常抽象和难以理解的概念时，也能着手分析。
<div><strong>精选留言（8）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/1e/b3/32/0ee78a1a.jpg" width="30px"><span>陈狄</span> 👍（6） 💬（2）<div>a在栈中没有争议，怎么都说r在堆上呢？r是引用变量，也在栈中吧，ramdom对象才在堆中吧。</div>2021-12-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/ba/4d/7ba09ff0.jpg" width="30px"><span>郑童文</span> 👍（2） 💬（1）<div>您好老师，有两个问题我不太明白：
1）原文中说：“每一个 Java 方法的栈里面都有一个模拟栈”，栈中有栈？ 这个模拟栈和变量表是保存在Java方法的栈的某一个栈帧的吗？还是每个栈帧都要保存一个模拟栈和变量表？

2）请问“可执行权限”的内存区域怎么理解？ 就是代码段吗？</div>2021-12-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/18/39/d2/845c0e39.jpg" width="30px"><span>送过快递的码农</span> 👍（0） 💬（1）<div>终于到Java了 ，发现还是有许多看不懂。我猜应该还是在堆里面吧。虽然从Java的角度来说，临时变量是应该在栈里面。但是我猜想对于C进程来说，在解释之前，进程是不知道的啊，只有执行的时候，才知道你是在Java栈还是Java堆里面，而且老师也说过，Java是模拟的栈还有变量表，那模拟栈应该是对应C的结构体吧，应该是放堆存着先？</div>2021-11-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/9e/50/21e0beca.jpg" width="30px"><span>kylin</span> 👍（0） 💬（1）<div>a是局部变量，存放在虚拟机的模拟栈上，但JVM会将模拟栈创建在进程虚拟内存哪里呢？猜测是栈
r是Java对象，分配到Java堆中，JVM应该提前使用mmap创建一大块内存，应该是在内存映射区吧</div>2021-11-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/d4/f3/129d6dfe.jpg" width="30px"><span>李二木</span> 👍（0） 💬（2）<div>r是在堆上，a在虚拟机栈上？</div>2021-11-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/cf/c6/6a2d0a5e.jpg" width="30px"><span>鵼</span> 👍（2） 💬（0）<div>终于看到java了，思考题，a是本地变量，在栈上，具体点应该是在本地变量表中，r是对象，在堆上。目前java没有栈上分配对象技术，但是是可以将对象中的属性，比如通过逃逸分析，一些对象只在方法内用，并且用到的只是对象的一些属性，是可以将对象的属性直接放到栈上的，因此可以不用创建对象。但是r因为用的是方法，虽然只在本方法用，但是java没有栈上分配对象的技术，所以还是在堆上。其实更准确点应该是在tlab上。</div>2021-11-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/73/9b/67a38926.jpg" width="30px"><span>keepgoing</span> 👍（1） 💬（0）<div>虽然不太熟悉Java语言，但也学到了核心知识点，👍</div>2021-11-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/28/59/52/1d92a110.jpg" width="30px"><span>设置昵称</span> 👍（0） 💬（0）<div>遇到过单机code Cache满的问题，一直没有找到原因。能帮忙提供一下排查思路吗？</div>2022-06-11</li><br/>
</ul>