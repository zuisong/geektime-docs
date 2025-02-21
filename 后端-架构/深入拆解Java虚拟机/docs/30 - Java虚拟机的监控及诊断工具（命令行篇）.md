今天，我们来一起了解一下JDK中用于监控及诊断工具。本篇中我将使用刚刚发布的Java 11版本的工具进行示范。

## jps

你可能用过`ps`命令，打印所有正在运行的进程的相关信息。JDK中的`jps`命令（[帮助文档](https://docs.oracle.com/en/java/javase/11/tools/jps.html)）沿用了同样的概念：它将打印所有正在运行的Java进程的相关信息。

在默认情况下，`jps`的输出信息包括Java进程的进程ID以及主类名。我们还可以通过追加参数，来打印额外的信息。例如，`-l`将打印模块名以及包名；`-v`将打印传递给Java虚拟机的参数（如`-XX:+UnlockExperimentalVMOptions -XX:+UseZGC`）；`-m`将打印传递给主类的参数。

具体的示例如下所示：

```
$ jps -mlv
18331 org.example.Foo Hello World
18332 jdk.jcmd/sun.tools.jps.Jps -mlv -Dapplication.home=/Library/Java/JavaVirtualMachines/jdk-11.jdk/Contents/Home -Xms8m -Djdk.module.main=jdk.jcmd
```
<div><strong>精选留言（21）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/0f/66/d0/6541f1d5.jpg" width="30px"><span>杨晓峰</span> 👍（20） 💬（1）<div>jmc早openjdk网站单独下载，目前需要7 ea版处理jdk11
http:&#47;&#47;jdk.java.net&#47;jmc&#47;</div>2018-09-30</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/04/b5/8bc4790b.jpg" width="30px"><span>Geek_987169</span> 👍（11） 💬（2）<div>老师为什么官方文档介绍工具开头都有&quot;This command is experimental and unsupported&quot;这句话？</div>2018-11-04</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/67/f4/9a1feb59.jpg" width="30px"><span>钱</span> 👍（5） 💬（1）<div>嘿嘿，就喜欢这样的简单拿来主义，随学随用。老师能否深入讲一下这些命令的底层实现，对应的信息都是怎么获取到的？都是从哪里获取到的？如果说都是从JVM中感觉范围有点大，往细了讲是从JVM的什么地方获取的呢？</div>2018-09-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/c3/56/0ad8772a.jpg" width="30px"><span>Axis</span> 👍（2） 💬（1）<div>Jdk11下开源了jfr但是没有jmc这个工具查看性能文件  是为什么？</div>2018-09-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/e2/58/8c8897c8.jpg" width="30px"><span>杨春鹏</span> 👍（1） 💬（1）<div>为什么我双击这些.exe，直接就闪退。</div>2018-10-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/5f/83/bb728e53.jpg" width="30px"><span>Douglas</span> 👍（0） 💬（2）<div>老师讲的好像和jdk11 没啥关系吧</div>2018-09-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/2d/75/e7c29de4.jpg" width="30px"><span>wkq2786130</span> 👍（6） 💬（0）<div>自己做的笔记，请大家斧正  http:&#47;&#47;weikeqin.com&#47;2020&#47;03&#47;28&#47;jvm-performance-tuning-monitoring-tool&#47; </div>2020-03-30</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/04/6f/55d943e6.jpg" width="30px"><span>美滋滋</span> 👍（6） 💬（0）<div>null那位朋友 oom killer了解一下</div>2018-10-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/46/69/78f18991.jpg" width="30px"><span>田斌</span> 👍（5） 💬（1）<div>Jstack -F会导致Java进程一直挂起吗，说是jdk的bug，什么情况下会一直挂起呢</div>2018-11-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/06/e0/fa7e80da.jpg" width="30px"><span>null</span> 👍（5） 💬（1）<div>老师， 你好
我想请教一个问题，
我们线上环境有一台tomcat偶尔会莫名的挂掉，
而且没有任何错误信息，日志都是正常的，
就像被kill -9一样。
请问这个怎么排查问题？
不会是人为的。
谢谢。</div>2018-09-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/e7/48/df149c8d.jpg" width="30px"><span>。。。。</span> 👍（0） 💬（0）<div>jmap导出是不是会很久很慢啊，有好的方法吗</div>2020-08-07</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/2d/75/e7c29de4.jpg" width="30px"><span>wkq2786130</span> 👍（0） 💬（0）<div>```
 S0C    S1C    S0U    S1U      EC       EU        OC         OU       MC     MU    CCSC   CCSU   YGC     YGCT    FGC    FGCT     GCT
28096.0 28096.0  0.0   28096.0 225024.0 225024.0  562560.0   562560.0  90916.0 88514.2 10304.0 9660.5     53   11.859  248   348.108  359.967
28096.0 28096.0  0.0   28095.9 225024.0 225024.0  562560.0   562560.0  90916.0 88514.2 10304.0 9660.5     53   11.859  249   349.650  361.510
28096.0 28096.0  0.0   28095.9 225024.0 225024.0  562560.0   562560.0  90916.0 88514.2 10304.0 9660.5     53   11.859  249   349.650  361.510
28096.0 28096.0  0.0   28096.0 225024.0 225024.0  562560.0   562560.0  90916.0 88514.2 10304.0 9660.5     53   11.859  250   351.329  363.189
28096.0 28096.0  0.0   28096.0 225024.0 225024.0  562560.0   562560.0  90916.0 88514.2 10304.0 9660.5     53   11.859  250   351.329  363.189
 S0C    S1C    S0U    S1U      EC       EU        OC         OU       MC     MU    CCSC   CCSU   YGC     YGCT    FGC    FGCT     GCT
28096.0 28096.0  0.0   28096.0 225024.0 225024.0  562560.0   562560.0  90916.0 88514.2 10304.0 9660.5     53   11.859  251   352.853  364.713
28096.0 28096.0  0.0   28096.0 225024.0 225024.0  562560.0   562560.0  90916.0 88514.2 10304.0 9660.5     53   11.859  253   354.598  366.457
28096.0 28096.0  0.0   28096.0 225024.0 225024.0  562560.0   562560.0  90916.0 88514.2 10304.0 9660.5     53   11.859  253   354.598  366.457
28096.0 28096.0  0.0   28096.0 225024.0 225024.0  562560.0   562560.0  90916.0 88514.2 10304.0 9660.5     53   11.859  253   354.598  366.457
28096.0 28096.0  0.0   28096.0 225024.0 225024.0  562560.0   562560.0  90916.0 88514.2 10304.0 9660.5     53   11.859  254   356.826  368.685
```

像这种 Old Space已经满了，但是还没有 OOM，大家知道是什么原因吗？</div>2020-03-30</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/c0/6c/29be1864.jpg" width="30px"><span>随心而至</span> 👍（0） 💬（0）<div>linux 下man 对应的command，结合老师给的文档，都会用了</div>2019-10-30</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/jAsPmqra89uLYer998tsdAmHIxy9iaVfLIkzkTB3ITfUZg21Yiadf73TqmcFZXTEv2wuQicDA2uvqXvicHJ9HckBWg/132" width="30px"><span>Geek_c991f2</span> 👍（0） 💬（1）<div>如果某个服务启动后,发现cpu使用率很高,这种问题怎么找出问题</div>2019-10-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/30/67/a1e9aaba.jpg" width="30px"><span>Roway</span> 👍（0） 💬（0）<div>老师， 您好！
我想请教一个问题，我们线上环境有一台tomcat偶尔会莫名的挂掉，
而且没有任何错误信息(tomcat bin目录下生成了文件hs_err_pid20894.log)，日志都是正常的，就像被kill -9一样。
请问这个怎么排查问题？
不会是人为的。
谢谢。</div>2019-06-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/ce/73/cded8343.jpg" width="30px"><span>believe me</span> 👍（0） 💬（0）<div>老师，为什么我用jstat命令查看：发现S0C和S1C的大小不一样，JDK版本是1.7</div>2019-06-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/23/72/70190bc1.jpg" width="30px"><span>子不语</span> 👍（0） 💬（0）<div>老师，咨询个问题，我通过jinfo -flag +PrintGC PID  jinfo -flag +PrintGCDetails PID，没办法指定路径，gc日志输出在哪里的，找不到。</div>2019-06-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/21/20/1299e137.jpg" width="30px"><span>秋天</span> 👍（0） 💬（0）<div>jps将打印所有正在运行的 Java 进程。 jstat允许...
</div>2019-06-05</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/e3/e5/7b2586cb.jpg" width="30px"><span>Warren</span> 👍（0） 💬（0）<div>我在使用jfr后发现method profiling为空，请问知道怎么解决吗</div>2019-05-15</li><br/><li><img src="" width="30px"><span>witluo</span> 👍（0） 💬（0）<div>为什么没有Gcplot，一般参数调整，有计算公式么？这个可以根据自己的业务流量和现有服务进行动态调整。
动态调整原则：调整理论合适值，再压测，将产生的gc.og,得出图形报表进行进一步分析，调整再压测，得出相对优参数值！
（个人意见）</div>2019-04-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/ed/b4/2f485987.jpg" width="30px"><span>啸风</span> 👍（0） 💬（1）<div>最近在分析was的JVM运行情况，好像没有jstack，和jmap，用的是javacore和heapdump分析，但用的不熟练，老师能否给适当的指导说明？</div>2019-03-19</li><br/>
</ul>