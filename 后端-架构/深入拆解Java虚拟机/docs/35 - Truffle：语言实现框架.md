今天我们来聊聊GraalVM中的语言实现框架Truffle。

我们知道，实现一门新编程语言的传统做法是实现一个编译器，也就是把用该语言编写的程序转换成可直接在硬件上运行的机器码。

通常来说，编译器分为前端和后端：前端负责词法分析、语法分析、类型检查和中间代码生成，后端负责编译优化和目标代码生成。

不过，许多编译器教程只涉及了前端中的词法分析和语法分析，并没有真正生成可以运行的目标代码，更谈不上编译优化，因此在生产环境中并不实用。

另一种比较取巧的做法则是将新语言编译成某种已知语言，或者已知的中间形式，例如将Scala、Kotlin编译成Java字节码。

这样做的好处是可以直接享用Java虚拟机自带的各项优化，包括即时编译、自动内存管理等等。因此，这种做法对所生成的Java字节码的优化程度要求不高。

不过，不管是附带编译优化的编译器，还是生成中间形式并依赖于其他运行时的即时编译优化的编译器，它们所针对的都是[编译型语言](https://en.wikipedia.org/wiki/Compiled_language)，在运行之前都需要这一额外的编译步骤。

与编译型语言相对应的则是[解释型语言](https://en.wikipedia.org/wiki/Interpreted_language)，例如JavaScript、Ruby、Python等。对于这些语言来说，它们无须额外的编译步骤，而是依赖于解释执行器进行解析并执行。
<div><strong>精选留言（4）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/11/a9/84/c87b51ce.jpg" width="30px"><span>xiaobang</span> 👍（7） 💬（1）<div>感觉truffle的特化和pypy的做法有点像，老师能否评价一下这两者呢？另外，truffle的特化相当于对每份目标语言源码都要搞一个新目标语言解释器，这样似乎比较耗时间，而性能测试说明性能比其它解释器要高，能解释一下为什么吗</div>2018-10-15</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1c/96/dd/1620a744.jpg" width="30px"><span>simple_孙</span> 👍（0） 💬（0）<div>Polyglot是不是类似于mmap技术，在虚拟机的堆空间上只有一份，但是可以映射到不同语言的对象上</div>2021-09-25</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/01/1c/d638d46e.jpg" width="30px"><span>宋世通</span> 👍（0） 💬（0）<div>这招叫做釜底抽薪</div>2021-08-27</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTLqDHFficypYouwztiatvzQWAPHt2X8R0Qge0iaat9dhfTjb0AFeicS3kjWJEjjMCSbwcoCYBOjK9aia8A/132" width="30px"><span>zzj</span> 👍（0） 💬（0）<div>想问下对于没有垃圾回收的语言，如 C++，经过 Truffle 解释后，在 JVM 上运行的时候还有 GC 吗？是有 native 方法直接调用对象的析构吗？</div>2019-03-27</li><br/>
</ul>