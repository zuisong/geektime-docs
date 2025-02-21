你好，我是郑雨迪。

在 JVM 中，每个 Java 对象都包含一个对象头，用于存储多种元数据，例如锁信息、哈希码、垃圾回收状态及指向其类的指针等。

这些数据主要是为了维护 JVM 的正常运行，并不包含任何应用程序相关的数据，因此，通常被视作运行 JVM 所需的额外内存开销。

目前，64 位 JVM 的默认对象头大小为 12 字节，其中包括 8 字节的标记字段（mark word）以及 4 字节的压缩类指针。据调研[\[1\]](https://wiki.openjdk.org/display/lilliput/Lilliput+Experiment+Results)，Java 对象在大多数场景下的平均大小约为 32 至 64 字节，其中对象头所占的比例大致在 37.5% 至 18.75% 之间。

这一显著的内存开销使得 JVM 饱受诟病，也因此催生了名为 Project Lilliput 的项目。

**Project Lilliput 的理念相对简单，核心在于压缩对象头的大小。**

为了说明这一点，我们可以假设Java对象的平均大小为 32 字节。根据这个假设，原本 12 字节的对象头若被压缩为 8 字节，便可实现 12.5% 的内存节省；若能够进一步将对象头压缩至 4 字节，内存节省则可达到 25%。

在 Lilliput 的相关介绍中[\[2\]](https://openjdk.org/jeps/450)提到，实际生产环境中，通过压缩对象头大小所节省的内存通常在 10% 到 20% 之间。这项技术的应用，不仅能够降低内存占用，还可以提高 JVM 的效率，进而优化 Java 应用程序的性能。
<div><strong>精选留言（2）</strong></div><ul>
<li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/9dTx3AVia8Lbx2iaP3dibFvoic99ODDENbp5TAfQOuD4co82C1BzNjU3Uobcqc1CZ3e58qzd3bia0vibt6M0llxRWqicQ/132" width="30px"><span>Geek_f24e8e</span> 👍（0） 💬（0）<div>这个项目似乎有点得不偿失</div>2025-02-21</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTLUDoNibohMic2oxC3UvaubWmuY5gcaS2Ht1GHcm3q99e5x0Xg0kSEwrR4XVO64zicwLFZEo1gZiaTJoQ/132" width="30px"><span>陈时锐</span> 👍（0） 💬（0）<div>昨天刚翻lilliput的相关文档，今天就看到这篇文章</div>2025-02-14</li><br/>
</ul>