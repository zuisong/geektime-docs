你好，我是康杨。

在这个时代，云计算正如早晨的太阳一般，照耀着每个现代企业。而今天，我们要探讨的GraalVM，则是伴随云原生概念而生的新星。它不仅仅是能高效执行Java程序的JVM，更是一种多语言平台，能帮助我们在构建云原生应用时，实现更快启动、更小的内存占用，甚至是跨语言的即时编译能力。今天就让我们基于GraalVM来搭建一个JVM云原生环境搭建，从头开始探索这一技术的奥秘。

## 云原生与GraalVM

GraalVM是一个非常酷的技术，也是Java界的一个明星产品。每一个使用Java编写代码的人都希望它跑得跟闪电一样快。而这就是GraalVM正在做的事情，让Java代码运行得更快、更高效。而且，不只是Java，其他语言也可以享受这种高速体验。下面，我们先来认识下GraalVM的三个核心组件。

### GraalVM核心组件

#### 超级编译器：Graal编译器

首先来说说Graal编译器。你写的Java代码在运行前需要被编译成字节码，JVM再把字节码转换成机器能懂的语言，也就是本地代码。这个过程有点像翻译，你的代码是英文书，而机器需要的是中文版。想象一下如果你问个问题，Graal编译器可以边听边给出答案，而不是等你说完所有话才开始翻译。而这就是Graal编译器动态编译的能力。
<div><strong>精选留言（2）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/22/83/bd/35960ffb.jpg" width="30px"><span>18667027789</span> 👍（0） 💬（0）<div>请教老师一个问题， demo中 image: graalvm&#47;graalvm-ce:latest   这个拉取不到，需要做什么特殊配置么？ </div>2023-11-16</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/25/87/f3a69d1b.jpg" width="30px"><span>peter</span> 👍（0） 💬（0）<div>请教老师几个问题：
Q1：k8s的windows安装部分，ste7的命令好像是Linux下的命令，不像是windows下的命令。
Q2：本地搭建的环境，怎么就是“云原生”？“云原生”的特征是什么？
Q3：truffle被称作“框架”，其功能是什么？不是很明白。</div>2023-11-13</li><br/>
</ul>