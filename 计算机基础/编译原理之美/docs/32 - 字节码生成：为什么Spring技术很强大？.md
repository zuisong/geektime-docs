**Java程序员几乎都了解Spring。**它的IoC（依赖反转）和AOP（面向切面编程）功能非常强大、易用。而它背后的字节码生成技术（在运行时，根据需要修改和生成Java字节码的技术）就是一项重要的支撑技术。

Java字节码能够在JVM（Java虚拟机）上解释执行，或即时编译执行。其实，除了Java，JVM上的Groovy、Kotlin、Closure、Scala等很多语言，也都需要生成字节码。另外，playscript也可以生成字节码，从而在JVM上高效地运行！

**而且，字节码生成技术很有用。**你可以用它将高级语言编译成字节码，还可以向原来的代码中注入新代码，来实现对性能的监测等功能。

目前，我就有一个实际项目的需求。我们的一个产品，需要一个规则引擎，解析自定义的DSL，进行规则的计算。这个规则引擎处理的数据量比较大，所以它的性能越高越好。因此，如果把DSL编译成字节码就最理想了。

既然字节码生成技术有很强的实用价值，那么本节课，我就带你掌握它。

我会先带你了解Java的虚拟机和字节码的指令，然后借助ASM这个工具，生成字节码，最后，再实现从AST编译成字节码。通过这样一个过程，你会加深对Java虚拟机的了解，掌握字节码生成技术，从而更加了解Spring的运行机制，甚至有能力编写这样的工具！
<div><strong>精选留言（8）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/16/0a/83/f916f903.jpg" width="30px"><span>风</span> 👍（14） 💬（3）<div>老师能不能为我们展望一下量子计算机的面世和普及，会给编译器、操作系统、网络等传统计算机技术带来什么样的冲击？会不会完全是另外一套技术栈？</div>2019-11-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/22/a0/0e8d56df.jpg" width="30px"><span>孤星可</span> 👍（11） 💬（1）<div>我正在写一个简单的 解释型 jvm  有兴趣欢迎共建  github mini-jvm</div>2019-11-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/23/96/e1f20e9f.jpg" width="30px"><span>树袋熊</span> 👍（2） 💬（1）<div>老师，为什么把dsl编译成字节码会提高性能呢？和用java程序来解析dsl，然后用jvm运行两者有什么不同呢？dsl编译成字节码比较快是相对什么情况比较快？</div>2020-06-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/ce/c6/958212b5.jpg" width="30px"><span>sugar</span> 👍（4） 💬（0）<div>补充一点：基于寄存器的虚拟机，google的js虚拟机v8目前也是了（以前是栈机）。</div>2020-05-03</li><br/><li><img src="" width="30px"><span>Geek_08d95a</span> 👍（1） 💬（0）<div>老师 你好 你说的你们正在使用dsl这块做规则引擎 可以分享一下吗</div>2022-11-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/e8/ca/2a7cc193.jpg" width="30px"><span>阿鼎</span> 👍（1） 💬（0）<div>像c++这种编译型语言，如何做到AOP、IOC？</div>2021-08-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/4b/11/d7e08b5b.jpg" width="30px"><span>dll</span> 👍（0） 💬（0）<div>栈机并不是不用寄存器，实际上，操作数栈是可以基于寄存器实现的，寄存器放不下的再溢出到内存里。只不过栈机的每条指令，只能操作栈顶部的几个操作数，所以也就没有办法访问其它寄存器，实现更多的优化
-——————————————————————————————————
不太理解，jvm的指令只能操作栈顶的数据，栈一定不在寄存器上，cpu是通过把这部分字节码的栈放到高速缓存里被快速读取到吗？要是次次都从内存读不得慢死了吗？
但是好像栈用到对象引用地址，对象都得从堆上取真正的对象数据，那不是次次都得访问内存？jvm是自己内部的机制产生的指令才会用到寄存器？专门操作字节码的指令就不用寄存器？是这样吗</div>2022-07-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/26/eb/d7/90391376.jpg" width="30px"><span>ifelse</span> 👍（0） 💬（0）<div>学习了，字节码生成</div>2021-10-25</li><br/>
</ul>