在前面的篇章中，有不少同学反馈对Java字节码并不是特别熟悉。那么今天我便来系统性地介绍一遍Java字节码。

## 操作数栈

我们知道，Java字节码是Java虚拟机所使用的指令集。因此，它与Java虚拟机基于栈的计算模型是密不可分的。

在解释执行过程中，每当为Java方法分配栈桢时，Java虚拟机往往需要开辟一块额外的空间作为操作数栈，来存放计算的操作数以及返回结果。

具体来说便是：执行每一条指令之前，Java虚拟机要求该指令的操作数已被压入操作数栈中。在执行指令时，Java虚拟机会将该指令所需的操作数弹出，并且将指令的结果重新压入栈中。

![](https://static001.geekbang.org/resource/image/13/21/13720f6eb83d096ec600309648330821.png?wh=1158%2A290)

以加法指令iadd为例。假设在执行该指令前，栈顶的两个元素分别为int值1和int值2，那么iadd指令将弹出这两个int，并将求得的和int值3压入栈中。

![](https://static001.geekbang.org/resource/image/13/db/138c20e60c081c8698770ff8d5d93fdb.png?wh=1134%2A176)

由于iadd指令只消耗栈顶的两个元素，因此，对于离栈顶距离为2的元素，即图中的问号，iadd指令并不关心它是否存在，更加不会对其进行修改。

Java字节码中有好几条指令是直接作用在操作数栈上的。最为常见的便是dup： 复制栈顶元素，以及pop：舍弃栈顶元素。

dup指令常用于复制new指令所生成的未经初始化的引用。例如在下面这段代码的foo方法中，当执行new指令时，Java虚拟机将指向一块已分配的、未初始化的内存的引用压入操作数栈中。
<div><strong>精选留言（22）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/0f/67/f4/9a1feb59.jpg" width="30px"><span>钱</span> 👍（23） 💬（2）<div>1:.Java代码由Java的语言语法组成，有开发人员来编写

2:.class 代码有Java编译器来编译，Java编译器也是有对应的开发人员来编写的，.class代码有字节码指令来组成，如果人理解Java字节码指令集比较简单也可以直接编写.class代码

3:Java对应的机器码有JVM来编译出来，原料是.class代码，如果人类理解机器码比较容易，那么可能变成就直接在机器硬件上直接编写机器码了

4:高级语言的出现是为提高人编写代码的效率，我们学习.class字节码指令集、JVM、机器码等的知识，是为了使我们编写高级语言代码能更好的在机器硬件上的执行效率更高，从高级语言的代码到能在机器上运行的机器码，中间经过了好几层的转换，所以，了解每一层是怎么转换就能更快的定位出高级语言代码的性能瓶颈了，感觉是为了在人的编码效率和机器的执行效率之间找平衡点

有个疑问❓
没太理解，JVM基于栈的计算模型的原因，推测可能是为了更简单的实现和更高的性能但是是怎么做到的呢？请老师解释一下</div>2018-09-07</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/d4/f3/129d6dfe.jpg" width="30px"><span>李二木</span> 👍（12） 💬（3）<div>为什么局部变量要初始化？想请老师专业解答下！</div>2018-09-03</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/f8/0e/de697f9b.jpg" width="30px"><span>熊猫酒仙</span> 👍（9） 💬（1）<div>C&#47;C++的汇编指令，会有大量寄存器的操作
请问java的指令会用到寄存器吗？</div>2018-09-07</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/9a/68/92caeed6.jpg" width="30px"><span>Shine</span> 👍（7） 💬（3）<div>“因此，我们需要利用 dup 指令复制一份 new 指令的结果，并用来调用构造器。当调用返回之后，操作数栈上仍有原本由 new 指令生成的引用去...”

第一步栈顶压入new对象的引用r0，执行dup后复制r0得到r1，压入栈顶。r1用于调用构造器,完成后会pop, 留下栈顶元素r0。不知我这样理解对不？
我的问题是为什么要dup呢？直接用r0不做pop不好吗？</div>2018-09-06</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/30/2b/bc5873c6.jpg" width="30px"><span>对方正在输入</span> 👍（5） 💬（1）<div>在JVM中,每个方法中,代码语句执行完毕,是不是都会默认有个return</div>2018-11-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/57/0f/1f229bf5.jpg" width="30px"><span>Void_seT</span> 👍（1） 💬（1）<div>数组访问指令表，int文稿中写的iaload，iastore；表格中列的iastore和istore</div>2018-09-03</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/f8/db/c4edf697.jpg" width="30px"><span>曲东方</span> 👍（37） 💬（0）<div>详尽，赞👍

随便找几断代码，javap反编译，查jvm手册一会儿就明白了</div>2018-09-03</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/63/14/06eff9a4.jpg" width="30px"><span>Jerry银银</span> 👍（3） 💬（0）<div>老师，请教下，在专栏中（关于虚拟机的书籍中）有提到：Java虚拟机大部分都是基于栈，有些虚拟机是基于寄存器的，比如Android的Dalvik和ART。

这听起来挺抽象的，老师能具体讲讲它们的区别？

是字节码执行的时候有区别的吗？  还是说字节码本身就有区别？</div>2019-12-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/99/af/d29273e2.jpg" width="30px"><span>饭粒</span> 👍（3） 💬（0）<div>图文并茂，总结详尽！感觉这篇放在前面可能更好。</div>2019-12-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/d9/61/4999fbc3.jpg" width="30px"><span>啸疯</span> 👍（2） 💬（0）<div>看的真爽，了解了很多字节码层面的细节，例如常量相加后赋值给变量，那么在字节码层面其实直接就是相加后的值，再比如两个string的相加，字节码层面其实也是调用stringbuiler不断append后tostring来实现的</div>2021-12-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/a4/ee/cffd8ee6.jpg" width="30px"><span>魏全运</span> 👍（2） 💬（0）<div>
  public void foo() {
    Object o = new Object();
  }
  &#47;&#47; 对应的字节码如下：
  public void foo();
    0  new java.lang.Object [3]
    3  dup
    4  invokespecial java.lang.Object() [8]
    7  astore_1 [o]
    8  return

通过对象创建的字节码就能明白对象的创建不是原子操作，所以需要双重检查锁保证单例安全</div>2020-03-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/d9/9f/7b2f2a97.jpg" width="30px"><span>师爷</span> 👍（2） 💬（0）<div>某些方法阻塞会不会导致弹栈阻塞呢</div>2019-09-25</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/cf/2f/4f89f22a.jpg" width="30px"><span>李鑫磊</span> 👍（2） 💬（0）<div>笔记：https:&#47;&#47;www.jianshu.com&#47;p&#47;b395ed905e0d</div>2018-11-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/51/6f/f33beea5.jpg" width="30px"><span>YIFENG</span> 👍（2） 💬（3）<div>64位虚拟机中long和double也都是占用两个栈单元吗？</div>2018-09-03</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/80/bf/3041138b.jpg" width="30px"><span>　素丶　　</span> 👍（1） 💬（0）<div>可以配合美团的这篇文章一起观看
https:&#47;&#47;tech.meituan.com&#47;2019&#47;09&#47;05&#47;java-bytecode-enhancement.html</div>2022-02-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/11/e9/b6aa6364.jpg" width="30px"><span>shenfl</span> 👍（1） 💬（1）<div>想请教下 编译后匿名内部类会生成一个class文件，但是函数式接口实现的代码却不会生成一个class文件，这是什么原理？</div>2019-04-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/27/1d/1cb36854.jpg" width="30px"><span>小辉辉</span> 👍（0） 💬（2）<div>有个疑问，如果在本地变量表中用 lload 或者 fload 时，怎么保证两个单元的数值同时被 load 到栈中。比如说方法有一个局部变量 long a = 5，然后在本地变量表中占用两个单元格，JVM是怎么保证这两个单元格中的数值都被 load 过去。</div>2021-03-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/9a/28/03613c22.jpg" width="30px"><span>track6688</span> 👍（0） 💬（0）<div>写得很详细，比较好理解， 相当于总结了一下。</div>2020-10-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/cc/de/e28c01e1.jpg" width="30px"><span>剑八</span> 👍（0） 💬（0）<div>讲的比较清晰了
java方法的栈帧包括了：
局部变量表，操作数栈
局部变量表是在编绎时刻就确定的，用于存储局部变量
操作数栈则用于存储在方法字节码执行的时候涉及到的变量值，以及运算完的结果

java虚拟机制定了一系列的java执行指令，有：
dup（用于将new指令生成的的引用复制到操作数栈）
iload：用于加载局部变量表中的变量到操作数栈
iadd&#47;imup等用于执行运算
</div>2020-06-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/4e/60/0d5aa340.jpg" width="30px"><span>gogo</span> 👍（0） 💬（0）<div>老师您好，从第一篇看到现在，对某个方法的执行流程还不是很理解，有哪一篇文章是说整个流程的吗，从主类加载初始化到某个方法执行结束的</div>2019-09-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/07/8c/0d886dcc.jpg" width="30px"><span>蚂蚁内推+v</span> 👍（0） 💬（0）<div>就是说如果是解释执行就在栈桢内完成了，不用寄存器。如果是即时编译执行，就用寄存器来存放操作数，对么</div>2019-07-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/25/80/fdd5a88f.jpg" width="30px"><span>ゞ﹏雨天____゛</span> 👍（0） 💬（0）<div>讲解内容中，这几张总结表，写的真的给力。赞</div>2019-03-27</li><br/>
</ul>