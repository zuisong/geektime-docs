垃圾收集机制是Java的招牌能力，极大地提高了开发效率。如今，垃圾收集几乎成为现代语言的标配，即使经过如此长时间的发展， Java的垃圾收集机制仍然在不断的演进中，不同大小的设备、不同特征的应用场景，对垃圾收集提出了新的挑战，这当然也是面试的热点。

今天我要问你的问题是，Java常见的垃圾收集器有哪些？

## 典型回答

实际上，垃圾收集器（GC，Garbage Collector）是和具体JVM实现紧密相关的，不同厂商（IBM、Oracle），不同版本的JVM，提供的选择也不同。接下来，我来谈谈最主流的Oracle JDK。

- Serial GC，它是最古老的垃圾收集器，“Serial”体现在其收集工作是单线程的，并且在进行垃圾收集过程中，会进入臭名昭著的“Stop-The-World”状态。当然，其单线程设计也意味着精简的GC实现，无需维护复杂的数据结构，初始化也简单，所以一直是Client模式下JVM的默认选项。  
  从年代的角度，通常将其老年代实现单独称作Serial Old，它采用了标记-整理（Mark-Compact）算法，区别于新生代的复制算法。  
  Serial GC的对应JVM参数是：

```
-XX:+UseSerialGC
```
<div><strong>精选留言（30）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/10/cb/83/bf876c13.jpg" width="30px"><span>张南南</span> 👍（24） 💬（2）<div>JDK8的话，互联网B&#47;S项目，追求高响应和底停顿，请问是用CMS好还是G1好呢，或者有其他更好的选择</div>2018-07-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/14/d6/e79204be.jpg" width="30px"><span>家庆</span> 👍（16） 💬（1）<div>老师，能整理一份每个jdk 版本对应默认的GC是什么吗？为什么会变更，优势在哪里，谢谢！</div>2018-08-18</li><br/><li><img src="" width="30px"><span>achenbj</span> 👍（10） 💬（1）<div>g1不是8的默认回收器？</div>2018-11-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/63/14/06eff9a4.jpg" width="30px"><span>Jerry银银</span> 👍（9） 💬（1）<div>老师：做Android应用层开发的同学该如何学习虚拟机？Android系统中的虚拟机，估计也只有系统厂商能修改和优化。有时候感觉学了很多虚拟机的理论，但是用在工作中的场景不多，也只有在“内存优化”和开发中编写代码时会用到一些jvm内存区域相关知识</div>2019-01-25</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/a2/80/abb7bfe3.jpg" width="30px"><span>Chris</span> 👍（7） 💬（1）<div>老师，python支持那里好像有笔误，应该是同时支持引用计数和可达性等垃圾收集机制。其二，标记清楚算法不适合大堆，请问这里的大堆有什么可以量化的标准吗？比如多大的堆才是大堆😂，希望老师能解答下，谢谢~</div>2018-07-07</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/03/b7/5afe5b1d.jpg" width="30px"><span>Evan</span> 👍（4） 💬（1）<div>直接分配到老年代的对象在年轻代有空间了会移动回来吗？</div>2018-07-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/ac/83/2f143a22.jpg" width="30px"><span>雪粮</span> 👍（4） 💬（1）<div>ZGC如此强大，非常期待！

咨询大师，Java未来有没有计划让手动内存回收辅助自动内存回收以提高回收效率？既默认情况下自动内存回收完全没问题，但在极致情况下允极客开发者介入甚至完全接管内存回收过程（类似与C和C++）以提高程序执行效率？</div>2018-07-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/d4/f3/129d6dfe.jpg" width="30px"><span>李二木</span> 👍（3） 💬（1）<div>用过-XX:+PrintGCDetails，打印比较详细</div>2018-07-07</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/2e/4b/de04a33b.jpg" width="30px"><span>null</span> 👍（2） 💬（2）<div>老师，请问一下，当Survivor满了而且Survivor中的对象还没有达到进去老年代的年龄后怎么处理，是会增加Survivor的大小吗还是直接将Survivor中的对象放到老年代呢</div>2018-07-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/15/69/187b9968.jpg" width="30px"><span>南山</span> 👍（1） 💬（2）<div>老师，Oracle的jvm的CMSGC，本身能够解决内存碎片化的问题吗？</div>2018-07-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/77/b3/991f3f9b.jpg" width="30px"><span>公号-技术夜未眠</span> 👍（142） 💬（4）<div>JVM提供的收集器较多，特征不一，适用于不同的业务场景：

Serial收集器：串行运行；作用于新生代；复制算法；响应速度优先；适用于单CPU环境下的client模式。
ParNew收集器：并行运行；作用于新生代；复制算法；响应速度优先；多CPU环境Server模式下与CMS配合使用。
Parallel Scavenge收集器：并行运行；作用于新生代；复制算法；吞吐量优先；适用于后台运算而不需要太多交互的场景。

Serial Old收集器：串行运行；作用于老年代；标记-整理算法；响应速度优先；单CPU环境下的Client模式。
Parallel Old收集器：并行运行；作用于老年代；标记-整理算法；吞吐量优先；适用于后台运算而不需要太多交互的场景。
CMS收集器：并发运行；作用于老年代；标记-清除算法；响应速度优先；适用于互联网或B&#47;S业务。

G1收集器：并发运行；可作用于新生代或老年代；标记-整理算法+复制算法；响应速度优先；面向服务端应用。</div>2018-07-08</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/DYAIOgq83eqxPHQ0mFEJ8lhIANMFa2YMb6lPYzmfNl1rUbarrG45ROM9MAk0wHJRk5vo4bnzvTWmWGWDgaVaxg/132" width="30px"><span>一孑</span> 👍（23） 💬（5）<div>老师有个问题不太明白，full gc、major gc、minor gc都会stop_the_word吗？还是说是跟具体的垃圾收集算法有关系？
</div>2018-07-19</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTLzSRrK59sydiaCJ5PrDv2jeuNTwXuXlN6JnYvCMkUHVmPEQ9fTG46mQV1ptkPMBdBL4gV56zickeqQ/132" width="30px"><span>黄黄的叶子</span> 👍（17） 💬（1）<div>jdk 9 用 -Xlog:gc* 
以前用 -XX:+PringGCStamps  -XX:+PringGCDetails</div>2019-03-01</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/97/1a/389eab84.jpg" width="30px"><span>而立斋</span> 👍（2） 💬（1）<div>老师，这里的服务端和client端，具体指的是啥？是不是可以理解为，client端就需要依赖jdk的一些C&#47;S客户端的软件。而服务端就比如是咱们现在的一些web应用服务器。</div>2020-08-05</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/fc/c8/15c85ee4.jpg" width="30px"><span>潭州太守</span> 👍（1） 💬（1）<div>老师，Serial GC和serverless Runtime有什么关联，愿听深度讲解</div>2020-05-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/8e/a8/c9819e37.jpg" width="30px"><span>时光</span> 👍（1） 💬（3）<div>老师，我一直很关心一个问题，方法区的垃圾回收是哪个收集器？</div>2020-03-16</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/E3XKbwTv6WTssolgqZjZCkiazHgl2IdBYfwVfAcB7Ff3krsIQeBIBFQLQE1Kw91LFbl3lic2EzgdfNiciaYDlJlELA/132" width="30px"><span>rike</span> 👍（1） 💬（1）<div>jdk 9以前gc是Parallel GC，之后是G1 GC，看着很多文章，CMS GC作用于老年代，ParNew GC作用于新生代，那Parallel GC是包含CMS GC和ParNew GC，还是什么关系？同理，Serial GC，G1 GC？</div>2020-02-25</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/18/59/daeb0b6c.jpg" width="30px"><span>日光倾城</span> 👍（1） 💬（0）<div>垃圾收集过程中，新生代的From区和To区应该是只有存活的对象才会被移动吧</div>2019-10-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/d4/67/0eaa81a4.jpg" width="30px"><span>Lh</span> 👍（1） 💬（1）<div>JVM提供的收集器较多，特征不一，适用于不同的业务场景：

Serial收集器：串行运行；作用于新生代；复制算法；响应速度优先；适用于单CPU环境下的client模式。
ParNew收集器：并行运行；作用于新生代；复制算法；响应速度优先；多CPU环境Server模式下与CMS配合使用。
Parallel Scavenge收集器：并行运行；作用于新生代；复制算法；吞吐量优先；适用于后台运算而不需要太多交互的场景。

Serial Old收集器：串行运行；作用于老年代；标记-整理算法；响应速度优先；单CPU环境下的Client模式。
Parallel Old收集器：并行运行；作用于老年代；标记-整理算法；吞吐量优先；适用于后台运算而不需要太多交互的场景。
CMS收集器：并发运行；作用于老年代；标记-清除算法；响应速度优先；适用于互联网或B&#47;S业务。

G1收集器：并发运行；可作用于新生代或老年代；标记-整理算法+复制算法；响应速度优先；面向服务端应用。</div>2019-07-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/2a/db/86437192.jpg" width="30px"><span>张旭</span> 👍（1） 💬（1）<div>老师，根据你画的minor gc图，minor gc发生时不会回收from区中的垃圾吗？</div>2019-04-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/04/7f/39707f39.jpg" width="30px"><span>HaoBin-Leo</span> 👍（1） 💬（0）<div>为什么有些文章会在serial old后面加上msc备注，serial old 不是采用的mark-compact么</div>2018-11-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/24/21/90b748a2.jpg" width="30px"><span>不归橙</span> 👍（0） 💬（1）<div>Python使用引用计数法，循环依赖的问题是怎么解决的？网上看了一圈也没看到说怎么解决的</div>2021-07-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/d8/97/51693617.jpg" width="30px"><span>fancy</span> 👍（0） 💬（0）<div>标记-清除算法，标记的应该是不可回收的对象吧。</div>2020-12-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/61/c7/b64ac05e.jpg" width="30px"><span>sky</span> 👍（0） 💬（2）<div>老师有2个问题请教一下
1:Parallel GC 与CMS  都是多线程版本, 区别就是Parallel GC带整理,CMS不带整理所以有内存碎片触发Full GC 的时候STW时间长么?
2:G1之后   S0    S1  两个区域发生YGC 的时候空间不会发生变化,是不再使用Survivor 了么</div>2020-05-03</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/zxkns28cIAUZIt3WjDb8G26qiccT84d9GMr9ZpbYR60TU1ibqSj9NoYVHlJvGF1kOltkqNDmEfJCqPuYVkue3WHg/132" width="30px"><span>Geek_55e386</span> 👍（0） 💬（0）<div>强大</div>2020-03-26</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/E3XKbwTv6WTssolgqZjZCkiazHgl2IdBYfwVfAcB7Ff3krsIQeBIBFQLQE1Kw91LFbl3lic2EzgdfNiciaYDlJlELA/132" width="30px"><span>rike</span> 👍（0） 💬（0）<div>第二次垃圾收集流程示意图中s1区域有1吗？</div>2020-02-01</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTIXjLm1ZXhj5RE2eQXribnkVURaianGEbdKDWGLug8L4TjEktl8aP4LyeiaeyeibD6j3lG85Vdib4HGoOA/132" width="30px"><span>codolio</span> 👍（0） 💬（0）<div>老师，您好！我在学习G1，查看了一下Oracle JDK 8和9关于GC的文档，有一些疑惑，想请教您一下。在JDK 8的文档（https:&#47;&#47;docs.oracle.com&#47;javase&#47;8&#47;docs&#47;technotes&#47;guides&#47;vm&#47;gctuning&#47;g1_gc_tuning.html）中讲到标记循环的几个阶段（Phases of the Marking Cycle）与JDK 9文档（https:&#47;&#47;docs.oracle.com&#47;javase&#47;9&#47;gctuning&#47;garbage-first-garbage-collector.htm#JSGCT-GUID-1CDEB6B6-9463-4998-815D-05E095BFBD0F）Garbage Collection Cycle中讲到阶段有些不同，JDK 8中说到有5个阶段，JDK 9中说到有2个阶段（Young-only phase和Space-reclamation phase），麻烦问一下，JDK 9中是有一些调整吗？还是在JDK 9的Young-only phase Initial Mark中包含了JDK 8中说到的多个阶段？</div>2019-12-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/8a/a7/674c1864.jpg" width="30px"><span>William</span> 👍（0） 💬（1）<div>老师,有个疑问.

请问“第二， 经过一次 Minor GC，Eden 就会空闲下来，直到再次达到 Minor GC 触发条件，这时候，另外一个 Survivor 区域则会成为 to 区域，Eden 区域的存活对象和 From 区域对象，都会被复制到 to 区域，并且存活的年龄计数会被加 1。”

如果此时:  Eden 区域的存活对象和 From 区域对象 的需要内存大小 &gt; to 区域的内存, 怎么处理的? 只是直接存储到永久代了么?</div>2019-11-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/18/59/daeb0b6c.jpg" width="30px"><span>日光倾城</span> 👍（0） 💬（3）<div>对于对象实例收集，主要是两种基本算法
，这个算法和常用的垃圾收集算法里面的算法是什么关系？</div>2019-10-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/37/b8/c887a5ea.jpg" width="30px"><span>Xs.Ten</span> 👍（0） 💬（0）<div>老师好，minor GC 发生第三次及以上的时候，from和to区域的角色会发生互换吗？不然的话，to中不是会存在标记为1的引用吗？还是存在会讲to的内容复制到from？</div>2019-09-02</li><br/>
</ul>