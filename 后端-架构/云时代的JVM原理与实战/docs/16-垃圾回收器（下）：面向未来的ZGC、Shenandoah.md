你好，我是康杨。

今天我们继续来聊GC的话题，上一节课我们介绍了当前生产环境中GC的王者G1，还记得它的特点吗？没错，就是垃圾优先、可预见性、并行、分区分代，我们也说过G1是一个承前启后的垃圾回收器，而它启的这个后就是ZGC和Shenandoah，也就是我们今天的主角，它们代表着未来GC的主流。

## ZGC的由来

随着云计算和大数据的迅猛发展，现代应用程序对于扩展性和低延迟的需求越来越高。传统的垃圾收集器在处理大内存应用程序时经常面临长时间停顿的问题，这导致了应用程序的性能下降。

为了解决这个问题，Oracle决定开发一种全新的垃圾收集器，旨在提供低停顿时间、高可伸缩性和适用于大内存应用程序的解决方案。于是在2017年，Oracle推出了名为ZGC的垃圾收集器，首先作为Oracle JDK的一个实验性功能引入。在随后的几个版本中，Oracle对ZGC进行了改进和优化，不断增加新功能，提升性能，并解决了一些问题。最终，ZGC在JDK 11中正式成为Oracle JDK的一部分，摇身一变，成为了一种稳定的垃圾收集器，并提供商业支持。

与此同时，ZGC也在OpenJDK中不断得到改进。Oracle把ZGC的源代码提交给了OpenJDK社区，供社区成员参与测试、优化。自JDK 11起，OpenJDK把ZGC作为它垃圾收集器的一部分，并在OpenJDK的发行版本中提供了稳定版本，供开源社区使用和改进。
<div><strong>精选留言（5）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/10/25/87/f3a69d1b.jpg" width="30px"><span>peter</span> 👍（1） 💬（1）<div>请教老师两个问题：
Q1：“ZGC 利用了 64 位机器的一些位来存储垃圾收集信息” ，这个具体是指什么？
Q2：每一个对象都有一个颜色指针吗？</div>2023-09-26</li><br/><li><img src="" width="30px"><span>Geek_fd6bd3</span> 👍（2） 💬（0）<div>ZGC 和 Shenandoah 的内容深度讲的太浅了。。。</div>2023-12-03</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/9dTx3AVia8Lbx2iaP3dibFvoic99ODDENbp5TAfQOuD4co82C1BzNjU3Uobcqc1CZ3e58qzd3bia0vibt6M0llxRWqicQ/132" width="30px"><span>Geek_f24e8e</span> 👍（1） 💬（0）<div>老师，有个疑惑，是不是三色标记和染色指针弄混了，染色指针是标记不同gc批次的，用来实现延迟更新引用指向的对象，分三个区域remapped和m0 m1</div>2024-03-06</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/0c/52/f25c3636.jpg" width="30px"><span>长脖子树</span> 👍（0） 💬（0）<div>Zgc和g1真的是两个级别的，生产环境上g1突刺可能接近100ms，而zgc大于0.2ms都很少</div>2023-10-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/da/d9/f051962f.jpg" width="30px"><span>浩仔是程序员</span> 👍（0） 💬（0）<div>老师你好，使用ZGC是不是意味着不能使用指针压缩了？</div>2023-10-07</li><br/>
</ul>