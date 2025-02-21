从你接触Java开发到现在，你对Java最直观的印象是什么呢？是它宣传的 “Write once, run anywhere”，还是目前看已经有些过于形式主义的语法呢？你对于Java平台到底了解到什么程度？请你先停下来总结思考一下。

今天我要问你的问题是，谈谈你对Java平台的理解？“Java是解释执行”，这句话正确吗？

## 典型回答

Java本身是一种面向对象的语言，最显著的特性有两个方面，一是所谓的“**书写一次，到处运行**”（Write once, run anywhere），能够非常容易地获得跨平台能力；另外就是**垃圾收集**（GC, Garbage Collection），Java通过垃圾收集器（Garbage Collector）回收分配内存，大部分情况下，程序员不需要自己操心内存的分配和回收。

我们日常会接触到JRE（Java Runtime Environment）或者JDK（Java Development Kit）。 JRE，也就是Java运行环境，包含了JVM和Java类库，以及一些模块等。而JDK可以看作是JRE的一个超集，提供了更多工具，比如编译器、各种诊断工具等。

对于“Java是解释执行”这句话，这个说法不太准确。我们开发的Java的源代码，首先通过Javac编译成为字节码（bytecode），然后，在运行时，通过 Java虚拟机（JVM）内嵌的解释器将字节码转换成为最终的机器码。但是常见的JVM，比如我们大多数情况使用的Oracle JDK提供的Hotspot JVM，都提供了JIT（Just-In-Time）编译器，也就是通常所说的动态编译器，JIT能够在运行时将热点代码编译成机器码，这种情况下部分热点代码就属于**编译执行**，而不是解释执行了。

## 考点分析

其实这个问题，问得有点笼统。题目本身是非常开放的，往往考察的是多个方面，比如，基础知识理解是否很清楚；是否掌握Java平台主要模块和运行原理等。很多面试者会在这种问题上吃亏，稍微紧张了一下，不知道从何说起，就给出个很简略的回答。

对于这类笼统的问题，你需要尽量**表现出自己的思维深入并系统化，Java知识理解得也比较全面**，一定要避免让面试官觉得你是个“知其然不知其所以然”的人。毕竟明白基本组成和机制，是日常工作中进行问题诊断或者性能调优等很多事情的基础，相信没有招聘方会不喜欢“热爱学习和思考”的面试者。
<div><strong>精选留言（30）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/10/2f/62/cd9958ee.jpg" width="30px"><span>Woj</span> 👍（1065） 💬（19）<div>        “一次编译、到处运行”说的是Java语言跨平台的特性，Java的跨平台特性与Java虚拟机的存在密不可分，可在不同的环境中运行。比如说Windows平台和Linux平台都有相应的JDK，安装好JDK后也就有了Java语言的运行环境。其实Java语言本身与其他的编程语言没有特别大的差异，并不是说Java语言可以跨平台，而是在不同的平台都有可以让Java语言运行的环境而已，所以才有了Java一次编译，到处运行这样的效果。
        严格的讲，跨平台的语言不止Java一种，但Java是较为成熟的一种。“一次编译，到处运行”这种效果跟编译器有关。编程语言的处理需要编译器和解释器。Java虚拟机和DOS类似，相当于一个供程序运行的平台。
        程序从源代码到运行的三个阶段：编码——编译——运行——调试。Java在编译阶段则体现了跨平台的特点。编译过程大概是这样的：首先是将Java源代码转化成.CLASS文件字节码，这是第一次编译。.class文件就是可以到处运行的文件。然后Java字节码会被转化为目标机器代码，这是是由JVM来执行的，即Java的第二次编译。
        “到处运行”的关键和前提就是JVM。因为在第二次编译中JVM起着关键作用。在可以运行Java虚拟机的地方都内含着一个JVM操作系统。从而使JAVA提供了各种不同平台上的虚拟机制，因此实现了“到处运行”的效果。需要强调的一点是，java并不是编译机制，而是解释机制。Java字节码的设计充分考虑了JIT这一即时编译方式，可以将字节码直接转化成高性能的本地机器码，这同样是虚拟机的一个构成部分。</div>2018-05-05</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/ed/4d/1d1a1a00.jpg" width="30px"><span>magict4</span> 👍（611） 💬（14）<div>我对『Compile once, run anywhere』这个宣传语提出的历史背景非常感兴趣。这个宣传语似乎在暗示 C 语言有一个缺点：对于每一个不同的平台，源代码都要被编译一次。我不解的地方是，为什么这会是一个问题？不同的平台，可执行的机器码必然是不一样的。源代码自然需要依据不同的平台分别被编译。 我觉得真正问题不在编译这一块，而是在 C 语言源文件这一块。我没有 C 语言的编程经验，但是似乎 C 语言程序经常需要调用操作系统层面的 API。不同的操作系统，API 一般不同。为了支持多平台，C 语言程序的源文件需要根据不同平台修改多次。这应该是一个非常大的痛点。我回头查了一下当时的宣传语，原文是『Write once, run anywhere』，焦点似乎并不在编译上，而是在对源文件的修改上。

以上是自己一点不成熟的想法，还请大家指正！</div>2018-05-05</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/06/29/bf619df8.jpg" width="30px"><span>三军</span> 👍（467） 💬（5）<div>Java特性:
面向对象（封装，继承，多态）
平台无关性（JVM运行.class文件）
语言（泛型，Lambda）
类库（集合，并发，网络，IO&#47;NIO）
JRE（Java运行环境，JVM，类库）
JDK（Java开发工具，包括JRE，javac，诊断工具）

Java是解析运行吗？
不正确！
1，Java源代码经过Javac编译成.class文件
2，.class文件经JVM解析或编译运行。
（1）解析:.class文件经过JVM内嵌的解析器解析执行。
（2）编译:存在JIT编译器（Just In Time Compile 即时编译器）把经常运行的代码作为&quot;热点代码&quot;编译与本地平台相关的机器码，并进行各种层次的优化。
（3）AOT编译器: Java 9提供的直接将所有代码编译成机器码执行。</div>2018-05-05</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/63/14/06eff9a4.jpg" width="30px"><span>Jerry银银</span> 👍（262） 💬（11）<div>关注了好久，终于期盼到了第一讲。

在看到这个题目时，我并没有立马点进来看原文，而是给了自己一些时间进行思考。

首先，个人觉得这个题目非常的抽象和笼统，这个问题没有标准答案，但是有『好』答案，而答案的好坏，完全取决于面试者自身的技术素养和对Java系统性的了解。我的理解如下：

宏观角度：
跟c&#47;c++最大的不同点在于，c&#47;c++编程是面向操作系统的，需要开发者极大地关心不同操作系统之间的差异性；而Java平台通过虚拟机屏蔽了操作系统的底层细节，使得开发者无需过多地关心不同操作系统之间的差异性。
通过增加一个间接的中间层来进行”解耦“是计算机领域非常常用的一种”艺术手法“，虚拟机是这样，操作系统是这样，HTTP也是这样。

Java平台已经形成了一个生态系统，在这个生态系统中，有着诸多的研究领域和应用领域：
1. 虚拟机、编译技术的研究(例如：GC优化、JIT、AOT等)：对效率的追求是人类的另一个天性之一
2. Java语言本身的优化
3. 大数据处理
4. Java并发编程
5. 客户端开发（例如：Android平台）
6. ......


微观角度：
Java平台中有两大核心：
1. Java语言本身、JDK中所提供的核心类库和相关工具
2. Java虚拟机以及其他包含的GC

1. Java语言本身、JDK中所提供的核心类库和相关工具
从事Java平台的开发，掌握Java语言、核心类库以及相关工具是必须的，我觉得这是基础中的基础。
&gt;&gt; 对语言本身的了解，需要开发者非常熟悉语言的语法结构；而Java又是一种面对对象的语言，这又需要开发者深入了解面对对象的设计理念；
&gt;&gt; Java核心类库包含集合类、线程相关类、IO、NIO、J.U.C并发包等；	
&gt;&gt; JDK提供的工具包含：基本的编译工具、虚拟机性能检测相关工具等。

2. Java虚拟机
Java语言具有跨平台的特性，也正是因为虚拟机的存在。Java源文件被编译成字节码，被虚拟机加载后执行。这里隐含的意思有两层：
1）大部分情况下，编程者只需要关心Java语言本身，而无需特意关心底层细节。包括对内存的分配和回收，也全权交给了GC。
2）对于虚拟机而言，只要是符合规范的字节码，它们都能被加载执行，当然，能正常运行的程序光满足这点是不行的，程序本身需要保证在运行时不出现异常。所以，Scala、Kotlin、Jython等语言也可以跑在虚拟机上。

围绕虚拟机的效率问题展开，将涉及到一些优化技术，例如：JIT、AOT。因为如果虚拟机加载字节码后，完全进行解释执行，这势必会影响执行效率。所以，对于这个运行环节，虚拟机会进行一些优化处理，例如JIT技术，会将某些运行特别频繁的代码编译成机器码。而AOT技术，是在运行前，通过工具直接将字节码转换为机器码。</div>2018-05-06</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/6a/27/9e8a8036.jpg" width="30px"><span>姜亮</span> 👍（186） 💬（5）<div>写个程序直接执行字节码就是解释执行。写个程序运行时把字节码动态翻译成机器码就是jit。写个程序把java源代码直接翻译为机器码就是aot。造个CPU直接执行字节码，字节码就是机器码。</div>2018-05-07</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/17/1b/4a088e67.jpg" width="30px"><span>欧阳田</span> 👍（158） 💬（6）<div>1，JVM的内存模型，堆、栈、方法区；字节码的跨平台性；对象在JVM中的强引用，弱引用，软引用，虚引用，是否可用finalise方法救救它？；双亲委派进行类加载，什么是双亲呢？双亲就是多亲，一份文档由我加载，然后你也加载，这份文档在JVM中是一样的吗？；多态思想是Java需要最核心的概念，也是面向对象的行为的一个最好诠释；理解方法重载与重写在内存中的执行流程，怎么定位到这个具体方法的。2，发展流程，JDK5(重写bug)，JDK6(商用最稳定版)，JDK7(switch的字符串支持)，JDK8(函数式编程)，一直在发展进化。3，理解祖先类Object，它的行为是怎样与现实生活连接起来的。4，理解23种设计模式，因为它是道与术的结合体。</div>2018-05-05</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/d7/f2/ca56e6ea.jpg" width="30px"><span>zaiweiwoaini</span> 👍（130） 💬（1）<div>看评论也能学习知识。 </div>2018-05-05</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/03/c2/e523d386.jpg" width="30px"><span>刻苦滴涛涛</span> 👍（101） 💬（5）<div>我理解的java程序执行步骤:
首先javac编译器将源代码编译成字节码。
然后jvm类加载器加载字节码文件，然后通过解释器逐行解释执行，这种方式的执行速度相对会比较慢。有些方法和代码块是高频率调用的，也就是所谓的热点代码，所以引进jit技术，提前将这类字节码直接编译成本地机器码。这样类似于缓存技术，运行时再遇到这类代码直接可以执行，而不是先解释后执行。</div>2018-05-05</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/be/20/8f4e0810.jpg" width="30px"><span>thinkers</span> 👍（99） 💬（4）<div>jre为java提供了必要的运行时环境，jdk为java提供了必要的开发环境！</div>2018-05-05</li><br/><li><img src="" width="30px"><span>scott</span> 👍（86） 💬（3）<div>解释执行和编译执行有何区别</div>2018-05-07</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/f8/ba/d28174a9.jpg" width="30px"><span>Geek_zbvt62</span> 👍（56） 💬（3）<div>这种基于运行分析，进行热点代码编译的设计，是因为绝大多数的程序都表现为“小部分的热点耗费了大多数的资源”吧。只有这样才能做到，在某些场景下，一个需要跑在运行时上的语言，可以比直接编译成机器码的语言更“快”</div>2018-05-05</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/05/2c/f6a29249.jpg" width="30px"><span>一叶追寻</span> 👍（41） 💬（1）<div>对Java平台的理解，首先想到的是Java的一些特性，比如平台无关性、面向对象、GC机制等，然后会在这几个方面去回答。平台无关性依赖于JVM，将.class文件解释为适用于操作系统的机器码。面向对象则会从封装、继承、多态这些特性去解释，具体内容就不在评论里赘述了。另外Java的内存回收机制，则涉及到Java的内存结构，堆、栈、方法区等，然后围绕什么样的对象可以回收以及回收的执行。以上是我对本道题的理解，不足之处还请杨老师指出，希望通过这次学习能把Java系统的总结一下~</div>2018-05-05</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/0f/4f/c75c4889.jpg" width="30px"><span>石头狮子</span> 👍（36） 💬（2）<div>1. 一次编译，到处运行。jvm 层面封装了系统API，提供不同系统一致的调用行为。减少了为适配不同操作系统，不同架构的带来的工作量。
2. 垃圾回收，降低了开发过程中需要注意内存回收的难度。降低内存泄露出现的概率。虽然也带来了一些额外开销，但是足以弥补带来的好处。合理的分代策略，提高了内存使用率。
3. jit 与其他编译语言相比，降低了编译时间，因为大部分代码是运行时编译，避免了冷代码在编译时也参与编译的问题。
    提高了代码的执行效率，之前项目中使用过 lua 进行相关开发。由于 lua 是解释性语言，并配合使用了 lua-jit。开发过程中遇到，如果编写的 lua 代码是 jit 所不支持的会导致代码性能与可编译的相比十分低下。
</div>2018-05-05</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/f9/8b/11c87d4e.jpg" width="30px"><span>櫻の空</span> 👍（32） 💬（3）<div>以下是我在本节课所得到的收获，结合TIJ的内容整理了一下我个人的理解，若有错误，还望老师指出。
Java采用的是解释和编译混合的模式。它首先通过javac将源码编译成字节码文件class.然后在运行的时候通过解释器或者JIT将字节码转换成最终的机器码。
只是用解释器的缺点：抛弃了JIT可能带来的性能优势。如果代码没有被JIT编译的话，再次运行时需要重复解析。
只用JIT的缺点：
需要将全部的代码编译成本地机器码。要花更多的时间，JVM启动会变慢非常多；
增加可执行代码的长度（字节码比JIT编译后的机器码小很多），这将导致页面调度，从而降低程序的速度。
有些JIT编译器的优化方式，比如分支预测，如果不进行profiling，往往并不能进行有效优化。
因此，HotSpot采用了惰性评估(Lazy Evaluation)的做法，根据二八定律，消耗大部分系统资源的只有那一小部分的代码（热点代码），而这也就是JIT所需要编译的部分。JVM会根据代码每次被执行的情况收集信息并相应地做出一些优化，因此执行的次数越多，它的速度就越快。
JDK 9引入了一种新的编译模式AOT(Ahead of Time Compilation)，它是直接将字节码编译成机器码，这样就避免了JIT预热等各方面的开销。JDK支持分层编译和AOT协作使用。
注：JIT为方法级，它会缓存编译过的字节码在CodeCache中，而不需要被重复解释</div>2018-05-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/ad/9a/e9d32750.jpg" width="30px"><span>Dee1024</span> 👍（24） 💬（1）<div>传统Java是解释型的语言，现在的JIT、AOT，让Java也支持了编译型语言的特性；
传统Java是面向对象的语言，JDK8引入Lambda，让Java也有了函数式编程的能力；
传统的Java是命令式编程范式，JDK9引入Flow，让Java更好的支持响应式编程范式；
... ...

Java是一个成熟稳定的语言和平台，更是历久弥新语言。
</div>2018-09-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/77/b3/991f3f9b.jpg" width="30px"><span>公号-技术夜未眠</span> 👍（21） 💬（2）<div>今日文章心得:个人理解的Java平台技术体系包括了以下几个重要组成部分：
Java程序设计语言
各种硬件平台上的Java虚拟机
Class文件格式
Java API类库及相关工具
来自商业机构和开源社区第三方Java类库

可以把Java程序设计语言、Java虚拟机、Java API类库及相关工具，这三部分统称为JDK，JDK是用于支持Java程序开发的最小环境；可以把Java API类库中的Java SE API子集和Java虚拟机这两部分统称为JRE，JRE是支持Java程序运行的标准环境。

提起Java，必然会想起TA跨平台的特性，但是跨平台重要吗？重要！因为可以write once，run anywhere，这是程序员的终极梦想之一。但是跨平台重要吗？不重要！作为程序语言，会更加关注TA的生态、兼容性、安全性、稳定性，以及语言自身的与时俱进。要要理解Java平台，JVM是必须要迈过去的坎，将会看到另外的风景。

为什么我们就不能把JVM作为透明的存在呢？

勿在浮沙筑高台，以JVM的GC为例。既然Java等诸多高级程序语言都已经实现了自动化内存管理，那我们为什么还要去理解内存管理了？因为当我们需要排查各种内存溢出、泄漏等底层问题时，当垃圾收集成为我们开发的软件系统达到更高并发量、更高性能的瓶颈时，我们就需要对这些“自动化”技术实施必要的监控与调节优化。</div>2018-05-05</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/80/66/c3000cdc.jpg" width="30px"><span>雪糕</span> 👍（17） 💬（1）<div>Hotspot 热点探测使用的方法是调用计数器和回边计数器，虚拟机为每个代码块，每个方法，建立计数器，统计执行次数，超过一定阀值，就视为热点代码，这种实现较为复杂，但是结果更为严谨</div>2018-10-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/e6/53/4b655144.jpg" width="30px"><span>吴有为</span> 👍（17） 💬（1）<div>老师，您好，看了文章和大家的评论有点疑问，程序执行的时候，类加载器先把class文件加载到内存中，一般情况下是解释执行，解释器把class里的内容一行行解释为机器语言然后运行。疑问1.每次执行class文件都需要解释整个class文件吗？疑问2.当new了一个对象的时候是怎么解释这个类的，是解释整个这个类对应的class？疑问3.JIT编译的热点代码是指class文件还是class文件的部分内容？</div>2018-05-06</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/1e/7b/2cf1a05a.jpg" width="30px"><span>jack</span> 👍（12） 💬（1）<div>Java平台包括java语言，class文件结构，jvm，api类库，第三方库，各种编译、监控和诊断工具等。
Java语言是一种面向对象的高级语言；通过平台中立的class文件格式和屏蔽底层硬件差异的jvm实现‘一次编写，到处运行’；
通过‘垃圾收集器’管理内存的分配和回收。
jvm通过使用class文件这种中间表示和具体语言解耦，使得任何在源码早期编译过程中以class文件为中间表示或者
能够转换成class文件的具体语言，都能运行jvm之上，也就可以使用jvm的各种特性。
api类库主要包含集合、IO&#47;NIO、网络、并发等。
第三方库包括各种商业机构和开源社区的java库，如spring、mybatis等。
各种工具如javac、jconsole、jmap、jstack等。</div>2018-05-06</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/7a/f2/6770d0a9.jpg" width="30px"><span>张驰</span> 👍（10） 💬（1）<div>所有的类运行时解析之后，再次运行时还会重复解析吗？</div>2018-05-06</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/a7/4a/7297bc4e.jpg" width="30px"><span>迎xiang李</span> 👍（10） 💬（1）<div>Java新手表示学习了，java的运行机制算是看明白了，但是发现还是有很多词汇不太了解。只有看高手们的文章才能发现自己的短板和不熟悉的领悟。期待后面更精彩，全面深入的讲解。感谢作者和各位大神的精彩评论！</div>2018-05-05</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/5b/49/90dbe5e5.jpg" width="30px"><span>MOSAIC</span> 👍（10） 💬（1）<div>关于JIT与AOT，我想KVM更有发言权，哈哈，好的东西终被学习与借鉴</div>2018-05-05</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/2d/d8/e06ec517.jpg" width="30px"><span>维#</span> 👍（8） 💬（1）<div>java的“一次编写，到处运行”，准确一点可以说是“一次编译，到处运行”，因为有了jvm的存在，编写的java代码编译为字节码，在任何平台的jvm虚拟机都可以上解释执行（简单点理解，抛开细节）。

jvm这种机制其实也是抽象和封装的体现，从01到汇编，从汇编到c，从c到java，不断地屏蔽底层的复杂性和繁琐的细节，供给上层的简单清晰的使用。我们“不用再去管硬件细节了”，“不用再去管内存了”，代码的看起来也更加人类语言了，jvm都让我们不用管操作系统平台了，至于过程中的性能啊，效率啊方面得失是值得的。

最后 write once, run anywhere的感受是mac写代码，linux运行。

</div>2018-10-28</li><br/><li><img src="" width="30px"><span>hailowell</span> 👍（7） 💬（1）<div>老师，看完后有个问题 jit是收集信息后编译热点代码 随着运行时间的增加 每个时间段的热点代码可能会变化吧？
比如测试系统 在登录模块的验证方法 每次登录循环调用10万次验证方法 这个验证方法是不是被认为热点代码？ 如果只有一个人登录过，之后验证方法再没有调用过 变成了事实上的冷代码 jvm面对不同时间段内相对热点的代码会有处理吗？</div>2018-08-03</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/3XbCueYYVWTiclv8T5tFpwiblOxLphvSZxL4ujMdqVMibZnOiaFK2C5nKRGv407iaAsrI0CDICYVQJtiaITzkjfjbvrQ/132" width="30px"><span>有铭</span> 👍（7） 💬（1）<div>我一直没想明白一个问题，既然jdk是jre的超集，为啥甲骨文提供的jdk安装包要同时安装他们两个。只装jdk不就行了吗，而且这一现象在所有平台均存在</div>2018-05-16</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/ce/b3/804aa247.jpg" width="30px"><span>大熊</span> 👍（6） 💬（1）<div>首先javac把源码编译成字节码(.class文件)，然后在程序运行时JVM把需要的.class文件加载内存，解释器逐行把该文件解释成机器码，在同样程序运行过程中部分热点代码可以通过JIT编译成机器码(不是逐行)并存在缓存里(运行时编译保证了可移植性)，下次运行可以直接从缓存里取机器码，效率更高。
AOT跟JIT的区别还是不太理解，原文的话是～AOT直接将字节码编译成机器代码，这样就避免了 JIT 预热等各方面的开销？
其他有不对的地方，麻烦指正</div>2018-05-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/fc/24/7d43d807.jpg" width="30px"><span>mongo</span> 👍（6） 💬（1）<div>首先什么是解释执行？什么是编译执行？我采纳了这位知乎大神的说法 https:&#47;&#47;www.zhihu.com&#47;question&#47;21486706&#47;answer&#47;18642540 。对于编译执行？是不是动态代理的实现原理字节码重组后的目标代理类的执行就是属于编译执行？包括反射的实现也是属于编译执行？这个猜想怎么验证？😂😂</div>2018-05-05</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/cf/e1/adacde45.jpg" width="30px"><span>无尘</span> 👍（4） 💬（1）<div>JDK 8 实际是解释和编译混合的一种模式，即所谓的混合模式（-Xmixed）。通常运行在 server 模式的 JVM，会进行上万次调用以收集足够的信息进行高效的编译，client 模式这个门限是 1500 次。

请教下，server模式下是不是所有调用上万次的代码都会被jit优化？</div>2018-11-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/58/1a/091b0e8b.jpg" width="30px"><span>Geek_0db725</span> 👍（4） 💬（1）<div>可否这么理解，&quot;java是解释执行&quot;这句话对而不全对。
正常流程，java编译为字节码class文件，而jvm通过解释器将字节码转化为机器码，此种情况应该就属于解释执行。
但是，文章中举例说明的，动态编译，JIT在运行时将热点代码编译成机器码，属于编译执行，就不属于解释执行了。
不知道这么理解是否正确。</div>2018-07-31</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/57/22/8944f1f5.jpg" width="30px"><span>石子儿</span> 👍（3） 💬（1）<div>我从事Java开发已经有9年了，本以为对Java开发已经有一定的了解。但看了第一篇文章就有看天书的感觉。jvm曾经由于好奇，也看书了解过，但工作中没有涉及到，没有实际应用过，就都忘记了。感觉自己在学习和工作中就是狗熊掰棒子，到最后没什么沉淀。怎样应对这种情况呢？</div>2019-01-27</li><br/>
</ul>