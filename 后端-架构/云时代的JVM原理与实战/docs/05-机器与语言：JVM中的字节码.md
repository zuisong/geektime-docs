你好，我是康杨。今天我们来聊聊JVM的语言——字节码。

在前面的介绍中，我们提到过Java语言的平台无关性，这也是Java能够快速崛起的原因之一。我们只需要用Java语言完成业务逻辑的开发，JVM就会帮助我们完成在物理服务器上的运行，而不用去关心底层硬件平台的差异性，能够达成这种效果的关键角色就是字节码。

借助字节码，JVM屏蔽了上层编程语言（Java、Scala ）和下层硬件平台的多样性。而JVM被认为是字节码的运行时。

![图片](https://static001.geekbang.org/resource/image/3b/c8/3b1c14f56ed0784ba781dc5894963dc8.png?wh=1920x595)

## 字节码是什么?

Java源代码经过编译器编译后，就会生成JVM字节码，它是Java程序在JVM上执行的中间表示形式。JVM字节码是一种基于栈的指令集架构（Stack-based Instruction Set Architecture）。每个字节码指令都会在JVM上执行一系列的操作，如加载、存储、运算、跳转等。

它使用基于操作数栈和局部变量表的执行模型。具有以下特点：

- 独立于具体的硬件和操作系统，不同平台上的JVM可以解释和执行相同的字节码文件。
- 相对于机器码和源代码，JVM字节码是一种更高级别的抽象，并且比机器码更容易阅读和编写（理解）。
- JVM字节码通过运行时的即时编译器或解释器执行。
<div><strong>精选留言（6）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/10/da/d9/f051962f.jpg" width="30px"><span>浩仔是程序员</span> 👍（6） 💬（2）<div>那个例子有点看不懂</div>2023-08-30</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/7a/56/29877cb9.jpg" width="30px"><span>临风</span> 👍（1） 💬（3）<div>老师，有个地方不太理解，为什么通过动态代理生成的List就比原来的性能更好，代理get方法后，不是也要执行判空逻辑吗？

对于字节码的应用，我想到的一个是性能监控，大概了解了一下，像skywalking就是通过注入字节码，将trace ID保存到threadLocal中去，并在调用其他接口时设置到header中去，由此完成了链路跟踪的功能。

</div>2023-08-30</li><br/><li><img src="" width="30px"><span>Geek_f46b9e</span> 👍（0） 💬（1）<div>为什么  采用乘以反数的方式替代除法计算可以提高运算效率呢</div>2023-09-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/28/47/6c/78184d19.jpg" width="30px"><span>非洲黑猴子</span> 👍（2） 💬（0）<div>最后这个例子不太明白, OptimizedStringProcessor怎么就快了? 谢谢</div>2023-09-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/16/d8/f15be64d.jpg" width="30px"><span>JavaBit</span> 👍（1） 💬（0）<div>OptimizedStringProcessor这个例子出错了吧，我测试了下没有调用get方法，使用的是iterator的方法，字符串并没有变成大写。

另外，这个例子哪里可以体现性能的优化呢，有没有大批量的数据验证呢</div>2024-03-06</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/25/87/f3a69d1b.jpg" width="30px"><span>peter</span> 👍（1） 💬（0）<div>请教老师几个问题：
Q1：“利用动态代理生成类的字节码”，这句话不太理解：文中是Java代码啊，什么时候生成字节码？类编译后就是字节码，还需要二次生成字节码？
Q2：#后面跟一个数字，比如#2表示什么意思？
Q3：在进行底层运算之前，JVM进行了自己的字节码运算，是吗？
如果是这样，相当于有两次运算，首先在JVM中进行了字节码级别的运算，然后交给系统CPU进行第二次运算，是吗？（我原来一直认为是把字节码翻译为机器码，然后运行）</div>2023-08-30</li><br/>
</ul>