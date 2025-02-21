你好，我是宫文学。

在前面的4讲当中，我们已经解析了OpenJDK中的Java编译器，它是把Java源代码编译成字节码，然后交给JVM运行。

用过Java的人都知道，在JVM中除了可以解释执行字节码以外，还可以通过即时编译（JIT）技术生成机器码来执行程序，这使得Java的性能很高，甚至跟C++差不多。反之，如果不能达到很高的性能，一定会大大影响一门语言的流行。

但是，对很多同学来说，对于编译器中后端的了解，还是比较模糊的。比如说，你已经了解了中间代码、优化算法、指令选择等理论概念，**那这些知识在实际的编译器中是如何落地的呢？**

所以从今天开始，我会花4讲的时间，来带你了解Java的JIT编译器的组成部分和工作流程、它的IR的设计、一些重要的优化算法，以及生成目标代码的过程等知识点。在这个过程中，你还可以印证关于编译器中后端的一些知识点。

今天这一讲呢，我首先会带你理解JIT编译的基本原理；然后，我会带你进入Graal编译器的代码内部，一起去修改它、运行它、调试它，让你获得第一手的实践经验，消除你对JIT编译器的神秘感。

## 认识Java的JIT编译器

我们先来探究一下JIT编译器的原理。

在[第5讲](https://time.geekbang.org/column/article/246281)中，我讲过程序运行的原理：把一个指令指针指向一个内存地址，CPU就可以读取其中的内容，并作为指令来执行。
<div><strong>精选留言（7）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/10/da/36/ac0ff6a7.jpg" width="30px"><span>wusiration</span> 👍（3） 💬（2）<div>这是目前在win 7环境下的编译报错，
Extracting LIBFFI_SOURCES...
Applying patches...
error: invalid path &#39;truffle\mxbuild\windows-amd64\src\libffi\libffi-3.2.1&#47;src&#47;x86&#47;ffi.c
可以分析出是编译代码在拼接路径的时候，用的是linux系统的分隔符...没找到能在哪里进行调整；

此外，最开始碰到的报错是windows自带的cmd是gbk编码，导致在python调用decode函数默认用utf8，无法正确解析路径。</div>2020-07-04</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/17/27/ec30d30a.jpg" width="30px"><span>Jxin</span> 👍（2） 💬（1）<div>本来我觉得jdk8的升级应该会很缓慢。但jdk9的aop编译如果不以补丁包加到jdk8，怕是能有效加快这个过程。毕竟原本不是很重要的启动时间，在servless下，变得至关重要。</div>2020-07-01</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/ef/04/f2942f14.jpg" width="30px"><span>Boomkeeper</span> 👍（1） 💬（1）<div>想问老师一个问题，就是启用graalvm去解析js代码是否执行第一次就进行了即时编译了，因为第二次去看执行时间从几百毫秒变为十几毫秒</div>2020-12-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/da/36/ac0ff6a7.jpg" width="30px"><span>wusiration</span> 👍（1） 💬（2）<div>老师，windows是不是很难编译graal，用mx工具build的时候，不停报错...</div>2020-07-01</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/23/c4/91/a017bf72.jpg" width="30px"><span>coconut</span> 👍（0） 💬（1）<div>github下载速度慢的话，可以在gitee上搜索相关的仓库

比如 https:&#47;&#47;gitee.com&#47;liyun_1981&#47;graal?_from=gitee_search</div>2021-01-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1e/f7/fb/16a90539.jpg" width="30px"><span>gkkrjj</span> 👍（0） 💬（1）<div>想知道老师的结构图一类的是什么工具画的</div>2020-07-07</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/26/eb/d7/90391376.jpg" width="30px"><span>ifelse</span> 👍（0） 💬（0）<div>牛逼plus</div>2022-01-12</li><br/>
</ul>