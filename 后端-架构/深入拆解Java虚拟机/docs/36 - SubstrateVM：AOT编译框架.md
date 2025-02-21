今天我们来聊聊GraalVM中的Ahead-Of-Time（AOT）编译框架SubstrateVM。

先来介绍一下AOT编译，所谓AOT编译，是与即时编译相对立的一个概念。我们知道，即时编译指的是在程序的运行过程中，将字节码转换为可在硬件上直接运行的机器码，并部署至托管环境中的过程。

而AOT编译指的则是，在**程序运行之前**，便将字节码转换为机器码的过程。它的成果可以是需要链接至托管环境中的动态共享库，也可以是独立运行的可执行文件。

狭义的AOT编译针对的目标代码需要与即时编译的一致，也就是针对那些原本可以被即时编译的代码。不过，我们也可以简单地将AOT编译理解为类似于GCC的静态编译器。

AOT编译的优点显而易见：我们无须在运行过程中耗费CPU资源来进行即时编译，而程序也能够在启动伊始就达到理想的性能。

然而，与即时编译相比，AOT编译无法得知程序运行时的信息，因此也无法进行基于类层次分析的完全虚方法内联，或者基于程序profile的投机性优化（并非硬性限制，我们可以通过限制运行范围，或者利用上一次运行的程序profile来绕开这两个限制）。这两者都会影响程序的峰值性能。

Java 9引入了实验性AOT编译工具[jaotc](http://openjdk.java.net/jeps/295)。它借助了Graal编译器，将所输入的Java类文件转换为机器码，并存放至生成的动态共享库之中。
<div><strong>精选留言（7）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/11/f9/98/95b13446.jpg" width="30px"><span>Jimbol</span> 👍（13） 💬（3）<div>老师好，写了这么多期，老师辛苦了！老师能否多写一些关于jvm性能优化调优，或者开发中常见的坑呢？太深奥的内容对一线开发来说好遥远</div>2018-10-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/09/7e/11cf22de.jpg" width="30px"><span>横云断岭</span> 👍（1） 💬（1）<div>请问SubstrateVM怎样调试？因为传统的java排查工具都失效了。使用方更加关注的是易用性。</div>2018-10-16</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/17/00/b3/2536a41b.jpg" width="30px"><span>Jolyne</span> 👍（0） 💬（1）<div>编辑的多彩图片从开始用到了结束。相当统一⌓‿⌓</div>2023-01-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/0b/0a/fa152399.jpg" width="30px"><span>wahaha</span> 👍（0） 💬（1）<div>老师，SubstrateVM以后会支持32位的X86和ARM处理器吗？</div>2018-10-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/29/b6/37ad78e0.jpg" width="30px"><span>dyangx</span> 👍（4） 💬（2）<div>今后有可能java 11会收费吗</div>2018-10-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/bf/10/b7974690.jpg" width="30px"><span>BD</span> 👍（2） 💬（1）<div>在Java开源框架源码里经常看到一种写法，object a=new object; object b=a; 接下来直接操作b。我想问这里为什么不直接操作a非要“多此一举”的赋值给b再操作b呢</div>2019-01-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/fe/30/c9b568c3.jpg" width="30px"><span>NullPointer</span> 👍（1） 💬（0）<div>谢谢老师辛勤付出，对于JVM有了通盘的理解，也有jvm未来发展。svm无意之间也为java-on-java做出不少努力，😁</div>2019-10-08</li><br/>
</ul>