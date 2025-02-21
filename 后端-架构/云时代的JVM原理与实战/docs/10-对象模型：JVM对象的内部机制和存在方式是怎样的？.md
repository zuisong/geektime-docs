你好，我是康杨。

这节课，我们一起来分析下微观环境下的JVM“分子”——对象。我们会先从 Everything  is  object 中的 object讲起，通过协议、模型、应用三部曲带你重新认识JVM中的对象。

对象是我们使用Java的基础，是所有方法和数据的载体，也是我们和Java世界交互的媒介，区别于以往的C、C++语言，即使我们实现一个最简单的“Hello World” 程序，也需要先创建一个Java对象。那这个我们再熟悉不过的对象，在JVM中是以怎样的形态存在的？又是如何影响到我们的日常编码和调优的？带着这些问题，我们一起来开启JVM对象的探索之旅。

## JVM 对象基础协议

### Java 对象的大小

首先请你思考一个问题：一个Java对象有多大？你可能下意识地会觉得一个Java对象的大小没法评估，这取决于它管理了多少属性，而JVM并没有限制一个对象所管理的属性的数量和大小。但其实一个Java对象的大小在JVM中是有一个要求的，那就是 Java对象的大小必须是8字节的整数倍。

**JVM为什么这么要求？又是如何做到的呢？**这就涉及到了Java对象的基础协议。Java对象协议是JVM对Java对象在JVM中如何存储的规定，协议中规定，在JVM中对象由三个部分构成，分别是对象头、实例数据、对齐区。
<div><strong>精选留言（8）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/17/dd/00/4a7b9a9f.jpg" width="30px"><span>Nico</span> 👍（5） 💬（1）<div>public class Main {
    public static void main(String[] args) {
        Book book =  new Book();
        Book colorBook = new ColorBook();
        book.print();
        colorBook.print();
    }
}
针对这段代码的主要字节码如下：
Code:
  stack=2, locals=3, args_size=1
    0: new           #2                  &#47;&#47; class com&#47;minis&#47;jvm&#47;Book
    3: dup
    4: invokespecial #3                  &#47;&#47; Method com&#47;minis&#47;jvm&#47;Book.&quot;&lt;init&gt;&quot;:()V
    7: astore_1
    8: new           #4                  &#47;&#47; class com&#47;minis&#47;jvm&#47;ColorBook
   11: dup
   12: invokespecial #5                  &#47;&#47; Method com&#47;minis&#47;jvm&#47;ColorBook.&quot;&lt;init&gt;&quot;:()V
   15: astore_2
   16: aload_1
   17: invokevirtual #6                  &#47;&#47; Method com&#47;minis&#47;jvm&#47;Book.print:()V
   20: aload_2
   21: invokevirtual #6                  &#47;&#47; Method com&#47;minis&#47;jvm&#47;Book.print:()V
   24: return
之前看JVM类加载阶段时说 “解析” 在某些情况下可以在初始化阶段之后开始，这是为了支持 Java 语言的运行时绑定，从这个字节码上看 ColorBook.print 执行的是 Book.print，那这个初始化阶段之后，是如何把 Book.print 换成了 ColorBook.print，这一段一直有点模糊，辛苦老师空了帮忙解答下，感谢！</div>2023-09-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/da/d9/f051962f.jpg" width="30px"><span>浩仔是程序员</span> 👍（3） 💬（1）<div>老师，你好！对象头的mark world有些不理解，在图中展示的意思一个对象在不同的状态存储不同的状态吗？比如在重量级锁的时候就没有储存hashcode？</div>2023-09-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/25/87/f3a69d1b.jpg" width="30px"><span>peter</span> 👍（1） 💬（1）<div>请教老师两个问题：
Q1：CPU读的“字”是四个字节吗？
Q2：klass是方法的内存地址吗？</div>2023-09-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/19/aa/5c/d2c1c7ce.jpg" width="30px"><span>^_^</span> 👍（1） 💬（1）<div>方法表是在准备阶段还是解析阶段创建的呢？</div>2023-09-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/30/d2/40/02139069.jpg" width="30px"><span>哪有什么胜利可言</span> 👍（0） 💬（0）<div>JVM 采用的是 OOP-Klass 对象模型，这个地方存储的就是指向 Klass 的指针，正是通过这个指针，JVM 知道当前这个对象是哪一个类的实例。
这个地方指的是哪个地方呢？没有讲清楚啊！！！</div>2024-09-07</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/60/a1/45ffdca3.jpg" width="30px"><span>静心</span> 👍（0） 💬（0）<div>也不知道是我的基本不够，还是理解有点差。总感觉没太完全理解。比如，Markword中几种锁的数据，是每个对象都会预留各种锁的数据？还是会根据情况切换不同的锁数据存储结构？</div>2024-02-04</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1b/87/37/b071398c.jpg" width="30px"><span>等风来🎧</span> 👍（0） 💬（0）<div>最后一张图，对象实例数据和类指针的位置是不是画反了？类指针不该再对象头里面吗？老师都用英文表示吧比如Book 的 Klass 指针，而不是 Book 的类指针。因为 java 的 Class 和 Klass&#39;很容易让人混淆。</div>2024-01-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/0b/5a/453ad411.jpg" width="30px"><span>C.</span> 👍（0） 💬（0）<div>JVM 的对象模型：对象、类、类加载器和类型信息。
JVM 层的数据类型：基本数据类型、引用类型、数组类型、接口类型、枚举类型。
特殊的数据类型和机制：泛型、注解、反射。</div>2023-09-11</li><br/>
</ul>