和Web应用程序一样，Tomcat作为一个Java程序也跑在JVM中，因此如果我们要对Tomcat进行调优，需要先了解JVM调优的原理。而对于JVM调优来说，主要是JVM垃圾收集的优化，一般来说是因为有问题才需要优化，所以对于JVM GC来说，如果你观察到Tomcat进程的CPU使用率比较高，并且在GC日志中发现GC次数比较频繁、GC停顿时间长，这表明你需要对GC进行优化了。

在对GC调优的过程中，我们不仅需要知道GC的原理，更重要的是要熟练使用各种监控和分析工具，具备GC调优的实战能力。CMS和G1是时下使用率比较高的两款垃圾收集器，从Java 9开始，采用G1作为默认垃圾收集器，而G1的目标也是逐步取代CMS。所以今天我们先来简单回顾一下两种垃圾收集器CMS和G1的区别，接着通过一个例子帮你提高GC调优的实战能力。

## CMS vs G1

CMS收集器将Java堆分为**年轻代**（Young）或**年老代**（Old）。这主要是因为有研究表明，超过90％的对象在第一次GC时就被回收掉，但是少数对象往往会存活较长的时间。

CMS还将年轻代内存空间分为**幸存者空间**（Survivor）和**伊甸园空间**（Eden）。新的对象始终在Eden空间上创建。一旦一个对象在一次垃圾收集后还幸存，就会被移动到幸存者空间。当一个对象在多次垃圾收集之后还存活时，它会移动到年老代。这样做的目的是在年轻代和年老代采用不同的收集算法，以达到较高的收集效率，比如在年轻代采用复制-整理算法，在年老代采用标记-清理算法。因此CMS将Java堆分成如下区域：
<div><strong>精选留言（24）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/10/78/c7/083a3a0b.jpg" width="30px"><span>新世界</span> 👍（30） 💬（3）<div>设置过大，回收频率会降低，导致单次回收时间过长，因为需要回收的对象更多，导致GC stop the world时间过长，卡顿明显，导致请求无法及时处理</div>2019-07-30</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/79/4b/740f91ca.jpg" width="30px"><span>-W.LI-</span> 👍（14） 💬（5）<div>李老师好!感觉老师今天偷懒了，CMS负责老年代回收，年轻代一般配合parNew使用。
大概啥情况下使用G1比较好啊?之前看见网上说，大堆多核，jdk9以及以上可以使用G1，jdk8的话除非cms满足不了需求不然不建议使用G1。
G1不太了解老师能推荐下资料么?
我觉得工具，可以提高效率，初学者优先搞清楚原理扎实基础比较好。</div>2019-07-30</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/THkFNC52F0kYs2XI1fwxOvEPtZ8P6VFXzRSSBqCuw9ytdvkFOUahj6LjdiaJbgMRBibw5W1kibmtxibzEmhia52ZI8w/132" width="30px"><span>弃</span> 👍（2） 💬（1）<div>老师，我想问个问题:在docker中运行的springboot(使用默认的tomcat容器)，如何查看tomcat的gc日志?</div>2019-07-30</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/48/5c/3e46e189.jpg" width="30px"><span>Wyatt</span> 👍（1） 💬（2）<div>
执行命令：java -Xmx2048m -Xss256k -verbosegc -Xlog:gc*,gc+ref=debug,gc+heap=debug,gc+age=trace:file=gc-%p-%t.log:tags,uptime,time,level:filecount=2,filesize=100m -jar target&#47;demo-0.0.1-SNAPSHOT.jar
java -Xmx2048m -Xss256k -verbosegc -Xlog:gc*,gc+ref=debug,gc+heap=debug,gc+age=trace:file=gc-%p-%t.log:tags,uptime,time,level:filecount=2,filesize=100m -jar target&#47;demo-0.0.1-SNAPSHOT.jar
报错：
Unrecognized option: -Xlog:gc*,gc+ref=debug,gc+heap=debug,gc+age=trace:file=gc-%p-%t.log:tags,uptime,time,level:filecount=2,filesize=100m
</div>2019-08-01</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/67/8a/babd74dc.jpg" width="30px"><span>锦</span> 👍（0） 💬（3）<div>对于CMS来说，设置很大的堆内存，在导致单次STW时间长，会导致服务不可用，定时器出问题？对响应敏感的系统来说不太友好，但堆内存设置太小又会导致频道GC，所以需要综合评估。那么如何使用超大机器内存呢？可以使用集群方式部署，单个应用设置较小的堆内存。
对于G1来说，文中有提到可以设置较大内存，因为G1是局部收集，但极端情况下，区域之间的对象引用关系非常多，也会导致大面积回收，STW时间会较长。
目前Java8使用CMS的较多，那么G1普及可能还需要时间吗？</div>2019-07-30</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/79/4b/740f91ca.jpg" width="30px"><span>-W.LI-</span> 👍（45） 💬（0）<div>年轻代设置过大:
1.生命周期长的对象会长时间停留在年轻代，在S0和S1来回复制，增加复制开销。
2.年轻代太大会增加YGC每次停顿的时间，不过通过根节点遍历，OopMap，old scan等优化手段这一部分的开销其实比较少。
3.浪费内存。内存也是钱啊虽然现在租的很便宜
老年代设置过大:
1.降低FGC频率，有些堆外内存比如直接内存，需要靠FGC辅佐回收的，就会无法释放。万一剩余的堆外内存不够程序也会宕机的吧
2.单次FGC时间变长，如果在夜深人静的时候主动触发FGC内啥影响，如果白天业务繁忙的时候就凉凉
3.增加YGC的时间，old scan阶段会扫描老年代，而且这个阶段耗时在YGC总比重很大。

最好别让太多老年代对象引用年轻代对象，这个坑很痛。</div>2019-07-30</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/30/8a/b5ca7286.jpg" width="30px"><span>业余草</span> 👍（6） 💬（0）<div>需要实际操作一遍，光看是记不住的，过一段时间就忘记了。</div>2019-07-30</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/1e/3a/5b21c01c.jpg" width="30px"><span>nightmare</span> 👍（5） 💬（0）<div>分情况，如果是G1大年轻代和大老年代没什么问题    如果是cms parnew的话  也需要看情况  如果你的并发比较大并且很快占满eden区  或者 用jstat监控 supervisor区占比一直高于百分之70这个时候 这个时候加大新生代就没有什么问题   如果要很久才占满eden区 或者supervisor区占比比较小 这个时候就要把 新生代 设置小一点 减少新生代回收时间            老年代也要看年轻代晋升到老年代平均占多大  如果晋升很快并且对象占比较大 大一点没问题  否则就需要减少老年代</div>2019-07-30</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/7b/57/a9b04544.jpg" width="30px"><span>QQ怪</span> 👍（3） 💬（0）<div>设置过大回收频率降低，单次回收的对象量大，回收stw时间过长，设置大也不好，过小也不好，设置适合的才是最好的</div>2019-07-30</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/51/0d/fc1652fe.jpg" width="30px"><span>James</span> 👍（1） 💬（0）<div>一句话：纸上谈兵终觉浅 绝知此事要躬行</div>2021-03-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/83/c8/5ce842f6.jpg" width="30px"><span>maybe</span> 👍（1） 💬（0）<div>1、cms把堆分为老年代、年轻代。年轻代又细分为幸存区和伊甸园。对象创建在伊甸园，发生一次ygc后如果有幸存对象就移到幸存区。如果多次ygc后还存活的对象就移到老年代。老年代空间不足会发生fullgc。g1大部分回收工作都是可并行，这期间不会出现stop the world。g1不像cms分老年代和年轻代，而是分为一个个小区域，默认2m大小，这样就可以更小范围的进行垃圾回收。减少垃圾回收的时间。
2、cms调优需要根据需求划分好老年代和年轻代大小。
g1比较职能一般设置下堆大小就行。
3、课后思考：如果分配很大，一次垃圾回收需要的时间很会比较长，影响应用相应时间。还有浪费内存空间。</div>2020-08-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/8c/6a/ec181c50.jpg" width="30px"><span>小唐</span> 👍（1） 💬（0）<div>老师可以把code分享到github吗？我想自己执行一遍加深印象，这样我们就不用自己配置了，多谢老师！</div>2019-08-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/e2/4c/4e5e5721.jpg" width="30px"><span>月如钩</span> 👍（1） 💬（0）<div>实操很重要呀，朋友们，纸上谈兵很容易忘</div>2019-08-01</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/b2/bf/aea9e7c6.jpg" width="30px"><span>615</span> 👍（0） 💬（0）<div>JDK8 运行参数：

-Xmx2048m
-Xss256k
-Xloggc:.&#47;garbage-collection.log
-XX:+PrintGCDateStamps
-XX:+PrintGCDetails

Refer: https:&#47;&#47;docs.oracle.com&#47;javase&#47;8&#47;docs&#47;technotes&#47;tools&#47;windows&#47;java.html</div>2023-04-14</li><br/><li><img src="" width="30px"><span>Geek_88463d</span> 👍（0） 💬（0）<div>这个标题配图有意思，哈哈哈哈</div>2020-12-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/22/e3/510b69f9.jpg" width="30px"><span>benny</span> 👍（0） 💬（0）<div>JDK11使用ZGC，或者是Azul的zing，gc的性能都更好</div>2020-03-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/db/26/54f2c164.jpg" width="30px"><span>靠人品去赢</span> 👍（0） 💬（0）<div>之前觉得用到JDK8就够了，据说是XXX维护的最后一个版本。老师讲完G1收集器，突然有兴趣，怪不得人家IDEA新的直接自带JDK11，技术越新越有惊喜啊。</div>2019-11-28</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/DYAIOgq83eq3opKxGyQia0CQibZU8If7Qv6ia3j4XiaWIdCHxrK0T3uZ5RVUSgwf0IJVRVt0wVLibryycTqv4VnEzbw/132" width="30px"><span>Geek_8c4282</span> 👍（0） 💬（0）<div>老师，我不太明白，为什么你调大堆内存后堆的大小会频繁震荡，没有发生minorgc和fullgc为什么堆的大小会上下变化，请老师告知下，谢谢</div>2019-11-15</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/DYAIOgq83eoRiaKX0ulEibbbwM4xhjyMeza0Pyp7KO1mqvfJceiaM6ZNtGpXJibI6P2qHGwBP9GKwOt9LgHicHflBXw/132" width="30px"><span>Geek_ebda96</span> 👍（0） 💬（0）<div>老师您好，请问对于新生代的内存，supervisor和eden区域，大小比例怎样设置合理，这个比例是否对GC性能有影响呢？</div>2019-08-03</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/89/23/73569bd7.jpg" width="30px"><span>xj_zh</span> 👍（0） 💬（0）<div>老师，可以讲一讲undertow吗，为什么spring boot 2.0 选择undertow做为默认WEB容器。</div>2019-07-31</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/17/9a/44/26a5336b.jpg" width="30px"><span>双月鸟</span> 👍（0） 💬（1）<div>CMS默认开启-XX:+UseAdaptiveSizePolicy，所以G1收集器会根据算法动态决定年轻和年老代的大小不能成为G1的优势</div>2019-07-30</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/THkFNC52F0kYs2XI1fwxOvEPtZ8P6VFXzRSSBqCuw9ytdvkFOUahj6LjdiaJbgMRBibw5W1kibmtxibzEmhia52ZI8w/132" width="30px"><span>弃</span> 👍（0） 💬（0）<div>谢谢老师。</div>2019-07-30</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/4d/fd/0aa0e39f.jpg" width="30px"><span>许童童</span> 👍（0） 💬（0）<div>老师讲得好啊，虽然工作中没有用到Java，但读了这篇文章也基本懂了！</div>2019-07-30</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/PiajxSqBRaEIvUlicgrWtibbDzwhLw5cQrDSy2JuE1mVvmXq11KQIwpLicgDuWfpp9asE0VCN6HhibPDWn7wBc2lfmA/132" width="30px"><span>a、</span> 👍（0） 💬（1）<div>年老代如果设置过大，会导致full gc时间过长,full gc需要stop-the-world，程序会出现长时间停顿。如果年轻代设置过大，因为年轻代用的是标记-复制算法，所以会出现需要复制大量数据的情况，也需要stop-the-world，所以也会出现长时间停顿</div>2019-07-30</li><br/>
</ul>