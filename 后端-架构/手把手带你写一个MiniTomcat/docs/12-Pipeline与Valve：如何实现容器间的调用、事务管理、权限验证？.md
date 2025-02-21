你好，我是郭屹。今天我们继续手写MiniTomcat。

上一节课我们把项目结构进一步抽象成两层Container，分别是Context和Wrapper，从而实现一个服务器管理多个容器，而容器又可以管理多个Servlet，层层嵌套，提升了容器的扩展性。然后我们在这个基础上，参考Tomcat的项目结构，进行对应的调整，让它更贴近Tomcat源码本身。

接下来我们再转向通用部分的组件，首先考虑的就是日志。日志可以有效帮助我们调试程序运行过程中的问题，在合理的地方打印日志也可以帮助我们了解服务器的运行情况，所以我们接下来会**定义通用的日志组件**。

在日志组件定义完毕后，我们紧接着会学习**职责链模式**在Tomcat中的应用，当服务器要调用某个具体的Servlet时，是经过这些Contaienr一层一层调用的，所以Tomcat中每个Container的invoke()都是通过职责链模式调用的。

![图片](https://static001.geekbang.org/resource/image/4e/de/4e90331a1b5ef8ba077c7cbd5d3670de.png?wh=1920x1147)

我们一起来动手实现。

## 项目结构

这节课我们新增Logger、Pipeline、Valve、ValveContext接口，以及处理日志Logger与Valve的实现类等众多Java文件，具体内容后面我们会详细说明。你可以看一下现在这个项目的目录结构。
<div><strong>精选留言（2）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/10/25/87/f3a69d1b.jpg" width="30px"><span>peter</span> 👍（1） 💬（1）<div>请教老师几个问题：
Q1：Logger接口定义中FATAL 为什么用 Integer.MIN_VALUE？
用0不就可以了吗？
Q2：“后端”是指什么？
“存在 Exception 异常时，后端会调用 printStackTrace 抛出异常”这句话中用到的“后端”是指什么？有“后端”就有“前端”，“前端”和“后端”分别指什么？
Q3：为什么先调用next再调用自身业务?
AccessLogValve的invoke方法中，先调用context中的invokeNext，实现职责链调用，再调用自己的业务。那就是先处理下一个，再处理自己，如此迭代下去，变成倒序了，类似于堆栈了。假设有3个业务，先到业务1，业务1调用业务2，业务2调用业务3,；业务3处理完以后再处理业务2，最后处理业务1。为什么这样设计？
Q4：Tomcat中的日志处理有什么特别之处？</div>2024-01-04</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/4c/6e/5435e214.jpg" width="30px"><span>HH🐷🐠</span> 👍（1） 💬（2）<div>个人理解是 Valve 先添加先执行，可以当做为 Filter，在 Servlet 前面拦截先执行； Basic 属于自身业务最后执行， 可以当做 Servlet。</div>2024-01-03</li><br/>
</ul>