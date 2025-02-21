我们学院的一位教授之前去美国开会，入境的时候海关官员就问他：既然你会计算机，那你说说你用的都是什么语言吧？

教授随口就答了个Java。海关一看是懂行的，也就放行了，边敲章还边说他们上学那会学的是C+。我还特意去查了下，真有叫C+的语言，但是这里海关官员应该指的是C++。

事后教授告诉我们，他当时差点就问海关，是否知道Java和C++在运行方式上的区别。但是又担心海关官员拿他的问题来考别人，也就没问出口。那么，下次你去美国，不幸地被海关官员问这个问题，你懂得如何回答吗？

作为一名Java程序员，你应该知道，Java代码有很多种不同的运行方式。比如说可以在开发工具中运行，可以双击执行jar文件运行，也可以在命令行中运行，甚至可以在网页中运行。当然，这些执行方式都离不开JRE，也就是Java运行时环境。

实际上，JRE仅包含运行Java程序的必需组件，包括Java虚拟机以及Java核心类库等。我们Java程序员经常接触到的JDK（Java开发工具包）同样包含了JRE，并且还附带了一系列开发、诊断工具。

然而，运行C++代码则无需额外的运行时。我们往往把这些代码直接编译成CPU所能理解的代码格式，也就是机器码。
<div><strong>精选留言（30）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/11/12/da/a3ea305f.jpg" width="30px"><span>jiaobuchongจุ๊บ</span> 👍（97） 💬（1）<div>对老师写的那段 awk 不懂得可参考：
https:&#47;&#47;blog.csdn.net&#47;jiaobuchong&#47;article&#47;details&#47;83037467</div>2018-10-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/3b/65/203298ce.jpg" width="30px"><span>小名叫大明</span> 👍（49） 💬（5）<div>受益匪浅，多谢老师。 

请教老师一个问题，网上我没有搜到。 

服务器线程数爆满，使用jstack打印线程堆栈信息，想知道是哪类线程数太多，但是堆栈里全是一样的信息且没有任何关键信息，是哪个方法创建的，以及哪个线程池的都看不到。 

如何更改打印线程堆栈信息的代码（动态）让其打印线程池信息呢？</div>2018-07-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/f8/db/c4edf697.jpg" width="30px"><span>曲东方</span> 👍（430） 💬（10）<div>jvm把boolean当做int来处理

flag = iconst_1 = true

awk把stackframe中的flag改为iconst_2

if（flag）比较时ifeq指令做是否为零判断，常数2仍为true，打印输出

if（true == flag）比较时if_cmpne做整数比较，iconst_1是否等于flag，比较失败，不再打印输出


</div>2018-07-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/e9/a1/2fe5b97a.jpg" width="30px"><span>novembersky</span> 👍（150） 💬（7）<div>文中提到虚拟机会把部分热点代码编译成机器码，我有个疑问，为什么不把java代码全部编译成机器码？很多服务端应用发布频率不会太频繁，但是对运行时的性能和吞吐量要求较高。如果发布或启动时多花点时间编译，能够带来运行时的持久性能收益，不是很合适么？</div>2018-07-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/67/f4/9a1feb59.jpg" width="30px"><span>钱</span> 👍（53） 💬（1）<div>1:为什么使用JVM？
1-1:可以轻松实现Java代码的跨平台执行
1-2:JVM提供了一个托管平台，提供内存管理、垃圾回收、编译时动态校验等功能
1-3:使用JVM能够让我们的编程工作更轻松、高效节省公司成本，提示社会化的整体快发效率，我们只关注和业务相关的程序逻辑的编写，其他业务无关但对于编程同样重要的事情交给JVM来处理

2:听完此节的课程的疑惑（之前就没太明白，原期待听完后不再疑惑的）
2-1:Java源代码怎么就经过编译变成了Java字节码？
2-2:JVM怎么就把Java字节码加载进JVM内了？先加载那个类的字节码？它怎么定位的？拿到后怎么解析的？不会整个文件放到一个地方吧？使用的时候又是怎么找到的呢？这些感觉还是黑盒
2-3:JVM将内存区域分成堆和栈，然后又将栈分成pc寄存器、本地方法栈、Java方法栈，有些内存空间是线程可共享的，有些是线程私有的。现在也了解不同的内存区块有不同的用处，不过他们是怎么被划分的哪？为什么是他们，不能再多几种或少几种了吗？共享的内存区和私有的又是怎么控制的哪？</div>2018-07-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/5d/10/0acf7cbc.jpg" width="30px"><span>Ryan-Hou</span> 👍（43） 💬（3）<div>在为什么Java要在虚拟机里执行这一节您提到，java语法复杂，抽象度高，直接通过硬件来执行不现实，但是同样作为高级语言为什么C++就可以呢？这个理由作为引入虚拟机这个中间层的原因不是很充分吧</div>2018-07-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/04/4d/bd86bdc2.jpg" width="30px"><span>周仕林</span> 👍（38） 💬（2）<div>看到有人说热点代码的区别，在git里面涉及到的热点代码有两种算法，基于采样的热点探测和基于计数器的热点探测。一般采用的都是基于计数器的热点探测，两者的优缺点百度一下就知道了。基于计数器的热点探测又有两个计数器，方法调用计数器，回边计数器，他们在C1和C2又有不同的阈值。😂😂</div>2018-07-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/12/18/83293985.jpg" width="30px"><span>笨笨蛋</span> 👍（23） 💬（5）<div>什么时候使用C1，什么时候使用C2，他是怎么区分热点方法的呢？</div>2018-07-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/06/1b/ecd5fffe.jpg" width="30px"><span>那我懂你意思了</span> 👍（18） 💬（3）<div>老师，那个pc寄存器，本地方法栈，以及方法栈，java方法栈这三个组成的就是我们常统称的栈吧，然后也叫栈帧？</div>2018-07-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/33/58/1f1e33d5.jpg" width="30px"><span>踏雪无痕</span> 👍（16） 💬（1）<div>您好，我现在所在的项目经常堆外内存占用非常多，超过总内存的70%，请问一下有没有什么方法能观察一下堆外内存有什么内容？</div>2018-07-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/57/38/ba6a106f.jpg" width="30px"><span>Phoenix</span> 👍（14） 💬（1）<div>解释执行是将字节码翻译为机器码，JIT也是将字节码翻译为机器码，为什么JIT就比解释执行要快这么多？
如果说JIT检测到是热点代码并且进行优化，那么为什么解释执行不直接就用这种优化去解释字节码？
一些比较浅的问题，希望老师能指点一二</div>2018-09-16</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/be/d4/ff1c1319.jpg" width="30px"><span>金龟</span> 👍（12） 💬（2）<div>感觉看完后，解释执行和jit的区别还是有点没搞懂。解释执行的意思是:直接将整个字节码码文件转化成机器码，jit的意思是:用到哪段编译哪段?</div>2018-11-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/00/bd/c9b8252a.jpg" width="30px"><span>suzuiyue</span> 👍（11） 💬（3）<div>JIT程序重启之后还需要再来一遍吗？</div>2018-09-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/0d/29/3806fe23.jpg" width="30px"><span>临风</span> 👍（10） 💬（2）<div>我跟楼上的novembersky同学一样疑惑，对于性能要求高的web应用，为什么不直接使用即时编译器在启动时全部编译成机器码呢？虽然启动耗时，但是也是可以接受的</div>2018-07-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/fe/fb/ae860669.jpg" width="30px"><span>Kouichi</span> 👍（8） 💬（1）<div>为啥是&quot;理论&quot;上比cpp快...这样看起来 如果都编译成机器码了 应该就是挺快的呀... 那干啥不像Go一样 直接编译成目标平台的机器码... 咋感觉绕了一圈..</div>2018-07-20</li><br/><li><img src="" width="30px"><span>雾里听风</span> 👍（7） 💬（2）<div>理论上讲，即时编译后的 Java 程序的执行效率，是可能超过 C++ 程序的。
我们导师当时是这么解释的，c是所有CPU指令集的交集，而jit可以根据当前的CPU进行优化，调用交集之外的CPU指令集，往往这部分指令集效率很高。
作者如何看待这句话？</div>2018-07-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/ff/1e/2a40a5ca.jpg" width="30px"><span>大明</span> 👍（6） 💬（3）<div>对不起，听了29篇文章了，至今不太清楚hotspot和openjdk两者之间的关系。</div>2018-09-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/0f/66/b188ad18.jpg" width="30px"><span>Bert.zhu</span> 👍（6） 💬（1）<div>老师，对于jvm的即时编译，当方法里有很多if,elseif这样的判断，jvm也是整个方法进行编译，还是只部分编译？</div>2018-07-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/f8/f3/2f4f8eb7.jpg" width="30px"><span>Fyypumpkin</span> 👍（6） 💬（1）<div>老师，问一下这个asmtools是做什么用的</div>2018-07-20</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/SttQqfuIiazh8ZISZjWibV5fQk67T0fVBwmDKuHicWBEBiaBhHzXUs9IGBI3gyljEAM96X5aibTpVdTALNpIbxPUFCg/132" width="30px"><span>世界和平</span> 👍（5） 💬（1）<div>你好  我想问下  解释执行 Java 字节码后，再次执行到这里，还需要再次编译吗</div>2020-01-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/c3/df/a704066e.jpg" width="30px"><span>崔龙龙</span> 👍（5） 💬（2）<div>对于占据大部分的不常用的代码，我们无需耗费时间将其编译成机器码，而是采取解释执行的方式运行；

这是否意味着不常用的代码的多次调用就要多次进行解释执行</div>2018-11-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/2f/93/0d4a353b.jpg" width="30px"><span>YJ</span> 👍（4） 💬（2）<div>测试了一下，从iconst_1, ..., iconst_5都可以编译成功，但是iconst_6以上就会报错

```
➜  jvm-learn grep -n &quot;iconst_6&quot; Foo.jasm
18:		iconst_6;
➜  jvm-learn java -cp asmtools.jar org.openjdk.asmtools.jasm.Main Foo.jasm
jasm: null
null
fatal exception
Foo.jasm: [18, 253]
1 error
```
请问有人知道为什么吗？</div>2018-11-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/d0/00/9d05af66.jpg" width="30px"><span>加多</span> 👍（4） 💬（2）<div>方法区是不是属于堆的一部分？</div>2018-07-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/27/54/d38c34a0.jpg" width="30px"><span>小泷哥</span> 👍（2） 💬（1）<div>两点∶
1.无论是c1,c2,graal都只编译方法，不是整个类
2.编译后的机器码放在内存
疑惑：
1.为什么不保存下来？
2.如果说是因为虚函数导致每次都需要重新编译，那没有设计虚函数的方法是否能保存下来？</div>2018-12-04</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/0e/61/ae68f8eb.jpg" width="30px"><span>dream</span> 👍（2） 💬（1）<div>请问一下这段话是什么意思：$ awk &#39;NR==1,&#47;iconst_1&#47;{sub(&#47;iconst_1&#47;, &quot;iconst_2&quot;)} 1&#39; Foo.jasm.1 &gt; Foo.jasm，我知道awk是类似于vim的记事本工具，但是这段代码到底做了什么不理解</div>2018-10-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/12/18/83293985.jpg" width="30px"><span>笨笨蛋</span> 👍（2） 💬（1）<div>搞不懂，没有讲清楚堆栈到底如何共享？有些文章说栈数据共享，但又说每个线程都会有一个堆栈，那堆栈的数据还如何共享？还有堆有时候说数据不共享，但又说线程间数据共享？这老师能解答一下吗？</div>2018-07-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/81/d4/e92abeb4.jpg" width="30px"><span>Jecy-8</span> 👍（2） 💬（1）<div>我一直以为方法区是从推划出的一部分，用来存放类和静态信息等，方法区中又包含常量池😅</div>2018-07-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/7f/88/c4263c58.jpg" width="30px"><span>五年</span> 👍（1） 💬（1）<div>练习题的代码命令可以给注释解释就好了,百度也百度不到什么意思...</div>2018-11-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/0d/1a/2c364284.jpg" width="30px"><span>隔离样</span> 👍（1） 💬（1）<div>初中还是高中时真的学的是c+</div>2018-07-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/89/09/d660509d.jpg" width="30px"><span>intuition</span> 👍（0） 💬（1）<div>老师你好，我有个地方还是想不通，为什么java采用一次编译，到处运行的这种方式，而不是C++的不同平台都进行编译， java这样设计 加了中间层 反而执行效率降低，那这种设计的初衷是什么呢？  </div>2018-11-07</li><br/>
</ul>