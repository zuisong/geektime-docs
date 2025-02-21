如今，Docker等容器早已不是新生事物，正在逐步成为日常开发、部署环境的一部分。Java能否无缝地运行在容器环境，是否符合微服务、Serverless等新的软件架构和场景，在一定程度上也会影响未来的技术栈选择。当然，Java对Docker等容器环境的支持也在不断增强，自然地，Java在容器场景的实践也逐渐在面试中被涉及。我希望通过专栏今天这一讲，能够帮你能做到胸有成竹。

今天我要问你的问题是，Java程序运行在Docker等容器环境有哪些新问题？

## 典型回答

对于Java来说，Docker毕竟是一个较新的环境，例如，其内存、CPU等资源限制是通过CGroup（Control Group）实现的，早期的JDK版本（8u131之前）并不能识别这些限制，进而会导致一些基础问题：

- 如果未配置合适的JVM堆和元数据区、直接内存等参数，Java就有可能试图使用超过容器限制的内存，最终被容器OOM kill，或者自身发生OOM。
- 错误判断了可获取的CPU资源，例如，Docker限制了CPU的核数，JVM就可能设置不合适的GC并行线程数等。

从应用打包、发布等角度出发，JDK自身就比较大，生成的镜像就更为臃肿，当我们的镜像非常多的时候，镜像的存储等开销就比较明显了。
<div><strong>精选留言（14）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/0f/fe/c5/3467cf94.jpg" width="30px"><span>正是那朵玫瑰</span> 👍（8） 💬（3）<div>老师好，再描述下我们的场景，我们在线上环境的参数是：xmx1g，永久带256m，docker限制2.2g，其他并没有设置，我们也怀疑是不是堆外内存有问题，于是在准生产环境修改了参数进行测试，设置了MaxRAM1g，堆外故意设小128m，然后进行测试，用jconsole进行监控，我们观察到docker容器的内存不断飙升，只升不降，而jconsole监控的却很正常，young gc很频繁，但是full gc一次没有，当docker内存接近设置的2.2g时，java进程就基本要被kill掉了，没有任何内存溢出的异常！</div>2018-08-07</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/6e/84/45a909a6.jpg" width="30px"><span>卡斯瓦德</span> 👍（6） 💬（1）<div>1.老师听说docker里面只能用open-jdk使用oracle-jdk是有法律风险的，现在还是这样么？            2.jdk8设置了-xmx值小于docker设定的值就好，我们使用了docker-compose貌似这个只有设定内存使用上限，但是不超过这个值一般没问题，3.至于swap没有遇见过，能能讲何时会出现么，好预警下。                                                                  4.说个docker遇到相关问题就是jdbc驱动，貌似mysql5.14以前的驱动对docker不友好，如果select count（*） from table 这个值超过5000就会拿不到结果，而实际mysql-server端已经执行完毕并且sleep了</div>2018-07-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/71/c3/09e22c1d.jpg" width="30px"><span>大卫李</span> 👍（5） 💬（1）<div>MAXRAM这个参数好像是openjdk的，oracle jdk文档里没有找到</div>2018-08-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/fe/c5/3467cf94.jpg" width="30px"><span>正是那朵玫瑰</span> 👍（4） 💬（2）<div>老师，有个问题想咨询下，我们现在迁移到docker环境，使用的还是java7，您说的那些参数我们都有设置，比如docker容器内存大小，最大堆内存，MaxRAM等，现在的问题是java应用在docker上跑一段时间就会被kill掉，我们监控内存情况是docker容器内存使用几乎被占满，但是jvm的内存使用却很正常，不知道为什么？老师能否指点下思路？</div>2018-08-06</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/1a/66/2d9db9ed.jpg" width="30px"><span>苦行僧</span> 👍（1） 💬（1）<div>目前在实际工作中还没有使用过docker</div>2019-02-05</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/f8/db/c4edf697.jpg" width="30px"><span>曲东方</span> 👍（47） 💬（0）<div>cpu问题

java 10之前： 手动设置jvm相关的选项，如：

    ParallelGCThreads
    ConcGCThreads
    G1ConcRefinementThreads
    CICompilerCount &#47; CICompilerCountPerCPU

java 10+: UseContainerSupport， 默认开启

------------------------------------------------------------------
mem问题

需关注这几个参数：

    Xmx: 1&#47;4 * 物理内存
    MaxDirectMemorySize
        Xmx 未设置，物理内存
        Xmx 设置了， Xmx - S0(1&#47;10 * Xmx) = 0.9 * Xmx # why? SurvivorRatio默认值8
    MaxPermSize: 默认64M
        [5.0+ 64 bit: 64M * 1.3 = 85M](http:&#47;&#47;www.oracle.com&#47;technetwork&#47;java&#47;javase&#47;tech&#47;vmoptions-jsp-140102.html)
    MaxMetaspaceSize: -1，无限制

--------------------------------
java5&#47;6&#47;7&#47;8u131-：务必设置上面提到的内存选项

  懒人可考虑，虽然也不准确
  java -Xmx`cat &#47;sys&#47;fs&#47;cgroup&#47;memory&#47;memory.limit_in_bytes`

java8u131+和java9+

	java 8u131+和java 9+-XX:+UnlockExperimentalVMOptions -XX:+UseCGroupMemoryLimitForHeap
	java 8u191+ UseContainerSupport默认开启，backported；java 9暂未backport这个feature

java 10+: UseContainerSupport， 默认开启
------------------------------------------------------------------</div>2018-07-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/95/04/dc153120.jpg" width="30px"><span>paopao</span> 👍（25） 💬（0）<div>年前就遇到了文中Gc线程数超过k8s设置核心数，jvm直接挂掉，看这文章印象深刻</div>2019-06-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/83/08/91caf5c1.jpg" width="30px"><span>Harry陈祥</span> 👍（12） 💬（4）<div>老师您好。对于java8+docker的场景，docker的cpu 内存配额是可能动态变化和伸缩的， docker启动之前，不知道会被分配多大内存多少cpu，这种情况，应该怎么处理参数问题？
还有一个问题是：docker hub里面有java各个版本的镜像，这些镜像是否已经对文中提到的问题都做了适配？我们在构建docker的时候，直接from java镜像，而不再设置java options 会不会有问题？</div>2019-02-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/c0/6c/29be1864.jpg" width="30px"><span>随心而至</span> 👍（6） 💬（0）<div>本科毕业两年了，打了两年多的计算机科学的基础，后端这些都是通用的，编程语言真的只是一个工具，容器相关的原理还是需要学习，要不然玩不转。</div>2021-01-06</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/1b/93/e3b44969.jpg" width="30px"><span>sgl</span> 👍（6） 💬（0）<div>没有一种技术是万能的，需要理解技术的优点和不足，才能使用好它</div>2018-09-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/fe/c5/3467cf94.jpg" width="30px"><span>正是那朵玫瑰</span> 👍（2） 💬（0）<div>目前容器只跑了java和consul的client进程，consul占的内存很小，java进程被kill掉后，consul进程还在，我们的java进程被kill掉都是在没有流量进来的时候，不过您说的使用swap区的我没有设置，不知道有没有什么影响？</div>2018-08-07</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/60/c5/69286d58.jpg" width="30px"><span>樱小路依然</span> 👍（1） 💬（0）<div>时隔三年多再次看这个专栏，又有不一样的感受，当初对docker根本没什么概念，现在公司内已经全部容器化了，但是对服务在容器上跑会出现这些问题竟然没什么印象。回过头看，可能是因为服务启动脚本早就配置好了具体参数而我也没有多注意，学习到了，谢谢老师</div>2022-02-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/d1/c8/bf71ac51.jpg" width="30px"><span>Shy</span> 👍（1） 💬（0）<div>老师，我在容器中部署Java应用时遇到一个问题，应用中存在一些jar冲突，但在物理机上能正常启动，放到容器中必定会启动失败，这是怎么回事？</div>2020-05-07</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/5e/48/4ad04a37.jpg" width="30px"><span>λ-Drive</span> 👍（0） 💬（0）<div>老师，docker会过度使用宿主机cpu的资源吗？</div>2021-03-24</li><br/>
</ul>