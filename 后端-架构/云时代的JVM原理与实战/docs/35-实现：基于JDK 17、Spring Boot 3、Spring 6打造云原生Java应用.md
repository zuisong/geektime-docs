你好，我是康杨。

在当前云计算快速发展的背景下，云原生应用变得越来越受欢迎，这种应用程序需要具备高度可移植性、强大的可扩展性和高效的性能等特性。这也是Java语言在云原生应用开发中面临的挑战，例如需要更好地支持容器化、微服务架构和云原生技术等。

为了应对这些挑战，Java也作出了很多改变，比如利用JDK 17的稳定性、Spring Boot 3 和 Spring 6等现代化特性，来构建高效、可扩展的Java应用程序，来适应云原生环境的需求。这节课我就带你来看看Java的变化，为了让你体会更深刻，我还会手把手带你实现一个基于JDK 17、Spring Boot 3和Spring 6的云原生Java应用。

话不多说，我们马上开始吧！

## **原生时代Java生态面临的挑战**

云原生是现代软件开发的新趋势，它让我们的应用程序能够在多种云环境中运行，并且能够灵活地调整资源。在这样的环境下，我们的应用程序需要具备**快速启动、安静掉线**的特性，这对于Java生态来说是个挑战。我们都知道，Java应用程序的启动过程相对较长，这在一定程度上限制了它在云原生环境中的表现。

再者，Java应用常常会占用大量的内存。在云环境中，资源是有限的，特别是在微服务中，内存消耗可能会成为一个问题。我们需要寻找办法来**优化Java应用程序的内存使用**，以适应云原生环境的需求。
<div><strong>精选留言（3）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/0f/98/b7/eaae99f8.jpg" width="30px"><span>张立勋</span> 👍（6） 💬（1）<div>请问一下：
第5步：使用Dockerfile打包镜像，并且运行docker镜像，这个是单独运行，没有在K8S里面的相关配置和操作，和云原生还是差了一截，建议可以增加这部分的描述，以紧跟前面的主题 云原生。
第6步：生成 Native Image，并且用 .&#47;target&#47;my-spring-boot-app 直接启动，也没有打镜像，也没有在 K8S里面去 运行这个原生镜像文件，那我生成原生镜像，就是为了这样运行吗？这个还是差了一截吧。

建议作者这两个点，能否在更新完备一下，毕竟我们来这里看文章，这两个点，才是真正的关键点所在。</div>2023-11-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/60/a1/45ffdca3.jpg" width="30px"><span>静心</span> 👍（0） 💬（0）<div>这节课讲得好杂呀！不过有些点倒是挺新鲜，比如，Native Image</div>2024-02-05</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/25/87/f3a69d1b.jpg" width="30px"><span>peter</span> 👍（0） 💬（0）<div>请教老师两个问题：
Q1：例子是windows下的操作吗？
命令行好像是Linxu下的操作，但有的操作又好像是在windows下。
Q2：Native Image不需要Docker吗？
Step6中的Native Image，直接运行，不需要docker。Native Image和docker哪种方式更好？</div>2023-11-17</li><br/>
</ul>