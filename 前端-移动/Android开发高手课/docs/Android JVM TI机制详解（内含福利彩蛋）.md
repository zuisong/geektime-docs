你好，我是孙鹏飞。

在专栏[卡顿优化](http://time.geekbang.org/column/article/73277)的分析中，绍文提到可以利用JVM TI机制获得更加非常丰富的顿现场信息，包括内存申请、线程创建、类加载、GC信息等。

JVM TI机制究竟是什么？它为什么如此的强大？怎么样将它应用到我们的工作中？今天我们一起来解开它神秘的面纱。

## JVM TI介绍

JVM TI全名是[Java Virtual Machine Tool Interface](https://docs.oracle.com/javase/7/docs/platform/jvmti/jvmti.html#SpecificationIntro)，是开发虚拟机监控工具使用的编程接口，它可以监控JVM内部事件的执行，也可以控制JVM的某些行为，可以实现调试、监控、线程分析、覆盖率分析工具等。

JVM TI属于[Java Platform Debugger Architecture](https://docs.oracle.com/javase/7/docs/technotes/guides/jpda/architecture.html)中的一员，在Debugger Architecture上JVM TI可以算作一个back-end，通过JDWP和front-end JDI去做交互。需要注意的是，Android内的JDWP并不是基于JVM TI开发的。

从Java SE 5开始，Java平台调试体系就使用JVM TI替代了之前的JVMPI和JVMDI。如果你对这部分背景还不熟悉，强烈推荐先阅读下面这几篇文章：

- [深入 Java 调试体系：第 1 部分，JPDA 体系概览](https://www.ibm.com/developerworks/cn/java/j-lo-jpda1/index.html)
- [深入 Java 调试体系：第 2 部分，JVMTI 和 Agent 实现](https://www.ibm.com/developerworks/cn/java/j-lo-jpda2/index.html)
- [深入 Java 调试体系：第 3 部分，JDWP 协议及实现](https://www.ibm.com/developerworks/cn/java/j-lo-jpda3/index.html)
- [深入 Java 调试体系：第 4 部分，Java 调试接口（JDI）](https://www.ibm.com/developerworks/cn/java/j-lo-jpda4/index.html)
<div><strong>精选留言（7）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/0f/a5/f1/76d4e6bb.jpg" width="30px"><span>功夫熊猫</span> 👍（2） 💬（1）<div>方法执行这段里的FileAccess 这个是不是写错了，应该是FieldAccess
https:&#47;&#47;docs.oracle.com&#47;javase&#47;7&#47;docs&#47;platform&#47;jvmti&#47;jvmti.html#FieldAccess</div>2018-12-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/7e/bb/947c329a.jpg" width="30px"><span>程序员小跃</span> 👍（0） 💬（2）<div>完了，第一次听说这个JVM TI 很认真的看了，还是有点不大明白，需要更好的消化下</div>2019-03-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/9a/bd/abb7bfe3.jpg" width="30px"><span>bonan</span> 👍（8） 💬（0）<div>今天看到Matrix 开源了，老师有计划介绍一下嘛？</div>2018-12-25</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTIK0hjb7AlzHYZGdoXibp8cWoWQFlr1KlwOjaFicJLfic62A2KpDsBGOrCsduYXzMcc38fGibTYcXyvmQ/132" width="30px"><span>hbl</span> 👍（1） 💬（0）<div>刚才看到Android 8.0 以后可以使用 apply change  这个功能通过 Android Studio 3.5 能够实现代码的动态加载，并且不需要重启，稍微了解了下原理，发现正是使用 JVM TI 的方式实现的</div>2019-08-15</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/b6/27/6ca3f497.jpg" width="30px"><span>Eric 老乌龟</span> 👍（1） 💬（0）<div>确实不太了解这块，先Mark下，用到了来学😂</div>2019-01-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/14/d8/2bacd9bb.jpg" width="30px"><span>GEEK_jahen</span> 👍（0） 💬（0）<div>运行Sample还是有闪退现象</div>2022-10-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/19/e6/e0/30b66693.jpg" width="30px"><span>珞小飞</span> 👍（0） 💬（0）<div>dexmaker貌似只能生成字节码，没办法修改已有字节码？</div>2020-06-01</li><br/>
</ul>