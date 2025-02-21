你好，我是康杨。今天我们来聊一聊JVM的编译器。

JVM的一个重要职责就是把字节码拿到实际运行的物理机上去执行，其中重要的一环，就是根据不同的底层操作系统和CPU架构，把字节码转化为实际物理机能够识别的机器码。

![图片](https://static001.geekbang.org/resource/image/yy/b2/yy3970yy80b5749a167747b6905216b2.png?wh=1920x607)

## 字节码转化为机器码的发展历程

在JVM的演进历程中，字节码到机器码的转化环节共经历了三个发展阶段，分别是解释执行阶段、解释执行+编译执行阶段、提前编译阶段。

![图片](https://static001.geekbang.org/resource/image/de/7d/de5aca6c5d034abaf30cb77412f5587d.png?wh=1920x1248)

### 解释执行（Interpreter Execution)

解释执行就是将编译好的字节码一行一行地翻译成机器码执行。这种模式在JVM的早期版本中就已经存在了，它舍弃了编译时间，只在程序运行时把字节码实时翻译为机器代码。

在解释执行过程中，由于每次都需要重新解释字节码，相同的字节码会存在被反复多次翻译执行的情况，所以采用这种模式的程序运行性能一般比较低。为此，JVM在解释执行的基础上引入了即时编译执行技术。

### 即时编译（Just in Time Compilation）

即时编译也就是我们常说的JIT，以方法为单位，即时编译将字节码一次性翻译为机器码后再执行。JIT编译器从JDK 1.1 版本开始引入。通过这种技术，JVM 就可以发现某段字节码被反复执行，从而启动JIT编译器，把这段字节码编译成机器代码，提高运行速度。
<div><strong>精选留言（14）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/10/da/d9/f051962f.jpg" width="30px"><span>浩仔是程序员</span> 👍（7） 💬（2）<div>AOT还可以使用反射和动态代理吗？</div>2023-08-30</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/7a/56/29877cb9.jpg" width="30px"><span>临风</span> 👍（6） 💬（1）<div>    java首先是通过javac编译成字节码，然后jvm才能通过执行字节码执行程序。jvm有两种执行方式，解释执行和编译执行，解释执行就是jvm直接翻译字节码为机器码运行，编译执行是jvm先将字节码编译成机器码并且缓存起来再执行。
    很明显解释执行在第一次绝对是比编译执行快的，但如果一段代码执行的次数多了，那么编译执行的效率反而是比解释执行高了。所以jvm会将热点代码进行编译执行，而大部分代码仍然保持解释执行。这也是为什么Java需要运行一段时间才能达到性能巅峰的原因。
    java使用c1（速度快、优化差、针对简单的逻辑）、c2（速度慢、优化好、针对复杂的逻辑）来进行编译，使用C++编写的，现在已经难以维护了。所以使用java推出了新的graal编译器代替c2编译器。这些编译器都属于JIT的范畴，都是在运行时去编译代码。
    为了适应云原生的背景，java推出了aot，支持直接将java文件编译为二进制执行文件，使用graal VM代替jvm执行，实现了毫秒级的启动时间。由于没有了运行时，对整个java生态也提出了挑战，不过spring boot3已经率先支持了这一特性。
    以上就是对本文的小结和自己一些简单的认识，如果有问题，还望老师指正。</div>2023-08-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/31/b6/2b/af79073f.jpg" width="30px"><span>追逐我的明天。</span> 👍（2） 💬（1）<div>关于逃逸分析 我想问个问题
作者原话：通过 JIT 我们能够确定哪些对象可以被限制在方法内部使用，不会逃逸到外部，然后可以对它们进行优化
但是下面的代码示例，引用肯定被传递到外面了，但是这段代码不还是被优化了嘛？我现在不太明白是传递到外面的 会被优化 还是不会被优化呢？</div>2023-08-31</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/24/5d/65e61dcb.jpg" width="30px"><span>学无涯</span> 👍（2） 💬（0）<div>看老师发的jit对比aot的图，好像aot除了启动时间，其他方面都不如jit，是我理解错了吗？</div>2023-08-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/0a/a4/828a431f.jpg" width="30px"><span>张申傲</span> 👍（1） 💬（1）<div>请教老师，使用 AOT 之后，一些基于字节码增强技术的框架是不是也无法支持了，比如 SkyWalking？</div>2023-09-16</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/ce/d7/074920d5.jpg" width="30px"><span>小飞同学</span> 👍（1） 💬（1）<div>那为啥不直接用aot直接将字节码转换为机器码？jit编译器感觉可以废弃了</div>2023-09-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/91/71/0b16655d.jpg" width="30px"><span>小麦</span> 👍（0） 💬（3）<div>为了从 JIT 过渡到 AOT，JVM 将字节码与 AOT 编译相结合。在 JIT 编译运行时，JVM 会监视代码的执行情况并收集相关的运行时信息，然后将这些信息传递给 AOT 编译器。AOT 编译器会利用这些信息对字节码进行优化，并生成可执行的本地机器代码。这样，当相同的代码再次执行时，就可以直接使用 AOT 编译得到的机器代码，而无需再次启动 JIT 编译。

从此描述中，没看出在 JIT 编译器识别出热点代码后，交给 AOT 编译器的好处是什么</div>2023-09-15</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/e5/4f/731ef2c1.jpg" width="30px"><span>geektime_zpf</span> 👍（0） 💬（1）<div>“为了从 JIT 过渡到 AOT，JVM 将字节码与 AOT 编译相结合。在 JIT 编译运行时，JVM 会监视代码的执行情况并收集相关的运行时信息，然后将这些信息传递给 AOT 编译器。AOT 编译器会利用这些信息对字节码进行优化，并生成可执行的本地机器代码。”，老师好，文中这几句不理解，jit收集的运行时信息，怎样传递给aot？</div>2023-09-06</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/21/e4/b4/889954ca.jpg" width="30px"><span>Levi</span> 👍（0） 💬（1）<div>使用 final 关键字来限制对象的可变性，这样 JIT 编译器更容易进行逃逸分析和优化。
老师这句话不太理解，能解释一下吗请问</div>2023-08-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/25/87/f3a69d1b.jpg" width="30px"><span>peter</span> 👍（0） 💬（1）<div>请教老师几个问题啊：
Q1：AOT难道没有运行时吗？
本课的第二张图，就是编译的那个图，AOT只有编译时，难道没有运行时吗？
Q2：AOT提前编译，编译的时候需要选择目标平台吗？比如，目标是Linux或Windows。
Q3：AOT必须与JIT结合吗？从文中看，好像AOT是基于JIT才能工作。
Q4：AOT与JIT的对比图中，吞吐量这一项，AOT的条比JIT的短，
这个正确吗?</div>2023-08-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1f/04/c0/42c70741.jpg" width="30px"><span>AmosLiu</span> 👍（0） 💬（0）<div>思考题个人总结
1、提升程序性能的编译器优化方式
1）前端优化（编译阶段）：
（1）方法内联：减少方法调用开销；
（2）常量折叠：编译时替换常量表达式；
（3）循环展开：减少循环控制的开销。

2）后端优化（运行时由JIT完成）：
（1）逃逸分析：栈上分配、同步省略；
（2）动态内联：将热点方法直接替换为调用点的具体代码；
（3）分支预测：优化条件判断，提高分支命中率。
3）JVM参数优化：
（1）-XX:+TieredCompilation：分层编译；
（2）-Xmx&#47;-Xms：调整堆大小；
（3）-XX:CompileThreshold=10000：设置热点方法触发阈值。

2、JIT 的原理
1）热点检测：通过计数器监控方法调用次数和循环执行频率；
2）动态优化：根据运行时数据优化代码；
3）分层编译：逐步将代码从解释执行优化到本地机器码。

3、JIT 的触发时机
1）计数器触发：方法调用或循环执行次数达到默认阈值（如 10,000 次），阈值可通过 -XX:CompileThreshold 调整；
2）代码热点识别：频繁调用的代码块会被标记为热点；
3）性能反馈优化：运行过程中根据实际执行情况动态调整。</div>2024-12-02</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/0b/34/f41d73a4.jpg" width="30px"><span>王盛武</span> 👍（0） 💬（0）<div>基于栈和基于寄存器的架构，性能上有多少差异？ Android上的Java是基于寄存器</div>2023-10-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/0b/34/f41d73a4.jpg" width="30px"><span>王盛武</span> 👍（0） 💬（0）<div>下面这段课文，是期望 还是已经实现了？

这种 JIT 和 AOT 结合的方式可以在保持性能优化和动态适应性的同时，拥有更快的启动时间和更高的执行速度。这样 Java 程序就能更好地适应云原生和容器化的环境了，性能和可扩展性也更好。</div>2023-10-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/57/60/65b006a6.jpg" width="30px"><span>Chief</span> 👍（0） 💬（0）<div>混合模式下 Java 代码执行流程的那张图，右上角的【编译执行】是不是有点歧义，缓存的机器码这个时候是可以直接执行的吧？ 
左边：编译执行 ---&gt; 是 ---&gt; 编译器编译 ---&gt; 执行
下边：缓存 ---&gt; 执行</div>2023-10-18</li><br/>
</ul>