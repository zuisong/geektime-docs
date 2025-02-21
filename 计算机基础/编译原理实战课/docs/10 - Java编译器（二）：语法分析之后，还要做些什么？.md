你好，我是宫文学。

上一讲，我带你了解了Java语言编译器的词法分析和语法分析功能，这两项工作是每个编译器都必须要完成的。那么，根据[第1讲](https://time.geekbang.org/column/article/242479)我对编译过程的介绍，接下来就应该是语义分析和生成IR了。对于javac编译器来说，生成IR，也就是字节码以后，编译器就完成任务了。也就是说，javac编译器基本上都是在实现一些前端的功能。

不过，由于Java的语法特性很丰富，所以即使只是前端，它的编译功能也不少。那么，除了引用消解和类型检查这两项基础工作之外，你是否知道注解是在什么时候处理的呢？泛型呢？还有各种语法糖呢？

所以，今天这一讲，我就带你把Java编译器的总体编译过程了解一遍。然后，我会把重点放在语义分析中的引用消解、符号表的建立和注解的处理上。当你学完以后，你就能真正理解以下这些问题了：

- **符号表是教科书上提到的一种数据结构，但它在Java编译器里是如何实现的？编译器如何建立符号表？**
- **引用消解会涉及到作用域，那么作用域在Java编译器里又是怎么实现的？**
- **在编译期是如何通过注解的方式生成新程序的？**

为了方便你理解Java编译器内部的一些对象结构，我画了一些类图（如果你不习惯看类图的话，可以参考下面的图表说明，比如我用方框表示一个类，用小圆圈表示一个接口，几种线条分别代表继承关系、引用关系和接口实现）。
<div><strong>精选留言（4）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/17/8c/d4/5972b7cc.jpg" width="30px"><span>宫文学Richard</span> 👍（6） 💬（0）<div>上一讲的参考：
对于a&gt;b*2+3，
step1: a                移进a
step2: a,b  &gt;  *      移进&gt;，再移进b。那现在能否对a&gt;b做规约呢？不能，因为后面跟的是*，优先级更高。
step3: a,b,2 &gt;,* +    所以继续移进*和2.那现在能不能对b*2做规约呢？可以的。因为后面跟的是+,优先级更低。
step4: a,b*2 &gt; +      规约掉b*2
step5: a,b*2,3 &gt;,+    继续移进+和3。现在后面已经是$了，所以不需要再移进了，接下来就连续做规约。
step6: a,b*2+3 &gt;      规约掉+操作，把操作数栈顶弹出两个值来，构建一棵加法子树。
step7 a&gt;b*2+3        再把&gt;操作规约掉。

注意，我可能一步会做两个移进，而你的步骤会比我多。但没关系，只要掌握算法规则就行了。</div>2020-06-30</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/da/36/ac0ff6a7.jpg" width="30px"><span>wusiration</span> 👍（2） 💬（1）<div>我的理解是有四个作用域，一个ScopeTest类的作用域，一个foo函数内部的作用域，if语句a&gt;0分支中的作用域以及if语句else分支中的作用域。</div>2020-06-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/2d/92/287f99db.jpg" width="30px"><span>lion_fly</span> 👍（1） 💬（2）<div>老师，您好，HelloWorldProcessor中是通过直接写文件的方式来生成相应的编译后的目标类，想问下老师，如何去通过修改语法树的方式来修改目标的类呢？我个人这边看到的资料，都是基于JDK8的来实现的，因为JDK8中是可以直接访问jdk.compiler中的定义的语法树的节点的，但是现在的JDK15这些数据结构已经无法直接在JDK的外部来直接访问了</div>2021-05-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/2d/92/287f99db.jpg" width="30px"><span>lion_fly</span> 👍（1） 💬（2）<div>老师可以提供一下这个类HelloWorldProcessor.java的源代码吗？</div>2021-03-03</li><br/>
</ul>