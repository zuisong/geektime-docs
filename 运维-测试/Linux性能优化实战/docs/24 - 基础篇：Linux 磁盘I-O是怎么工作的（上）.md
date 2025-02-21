你好，我是倪朋飞。

上一节，我们学习了 Linux 文件系统的工作原理。简单回顾一下，文件系统是对存储设备上的文件，进行组织管理的一种机制。而Linux 在各种文件系统实现上，又抽象了一层虚拟文件系统VFS，它定义了一组，所有文件系统都支持的，数据结构和标准接口。

这样，对应用程序来说，只需要跟 VFS 提供的统一接口交互，而不需要关注文件系统的具体实现；对具体的文件系统来说，只需要按照 VFS 的标准，就可以无缝支持各种应用程序。

VFS 内部又通过目录项、索引节点、逻辑块以及超级块等数据结构，来管理文件。

- 目录项，记录了文件的名字，以及文件与其他目录项之间的目录关系。
- 索引节点，记录了文件的元数据。
- 逻辑块，是由连续磁盘扇区构成的最小读写单元，用来存储文件数据。
- 超级块，用来记录文件系统整体的状态，如索引节点和逻辑块的使用情况等。

其中，目录项是一个内存缓存；而超级块、索引节点和逻辑块，都是存储在磁盘中的持久化数据。

那么，进一步想，磁盘又是怎么工作的呢？又有哪些指标可以用来衡量它的性能呢？

接下来，我就带你一起看看， Linux 磁盘I/O的工作原理。

## 磁盘

磁盘是可以持久化存储的设备，根据存储介质的不同，常见磁盘可以分为两类：机械磁盘和固态磁盘。
<div><strong>精选留言（30）</strong></div><ul>
<li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTLdWHFCr66TzHS2CpCkiaRaDIk3tU5sKPry16Q7ic0mZZdy8LOCYc38wOmyv5RZico7icBVeaPX8X2jcw/132" width="30px"><span>JohnT3e</span> 👍（39） 💬（1）<div>工作中经常看到使用多线程读写单个磁盘中不同文件的实现，个人认为这种方法并不能有效地提高性能，因为每个线程读写磁盘的位置可能差异很大，且每个线程的数据的空间局部性和时间局部性存在差异，导致磁盘调度优化不足。不知道对不对</div>2019-01-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/14/2e/400913b1.jpg" width="30px"><span>金波</span> 👍（22） 💬（1）<div>有个问题一直没弄明白，想借此机会请老师解答下，
大家经常用select来多路复用读写管道，socket等类型的文件，
请问select可否用于普通磁盘文件的读写？ 不行的话为什么？
多谢</div>2019-01-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/2d/24/28acca15.jpg" width="30px"><span>DJH</span> 👍（14） 💬（2）<div>有一个纠正一下：ISCSI访问的是块设备，不是NAS。</div>2019-01-14</li><br/><li><img src="https://wx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTIU2IArYKPQ6l7DtsNERJW9NCiaHJ0uG89JRcV4M1QAiaSDPUVr6KVPbEvA24TPn1EwpRUGI7diarLFg/132" width="30px"><span>萨拉热窝的棒小伙儿</span> 👍（13） 💬（2）<div>老师，想问一下，如果申请的测试环境资源与生产环境资源是有差异的，那么在测试环境上做性能测试的话，是否可以按照资源差异同比例缩小，这个通过准则？
例如，生产环境10个cpu，5G 内存，期望能并发100用户，满足1秒响应。。。测试环境5个cpu，2.5G，，那么并发50用户，满足1秒响应就行了，，有这个说法嘛？</div>2019-01-14</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/Q3auHgzwzM4z9WYWVvWDhMF0SicPE5ad56ME6DibyWGbRoQa0lH4U9icdsjNcv3ssRickcuRMDA01e6vMXnmOVSr9l5LVUefVxicn/132" width="30px"><span>black_mirror</span> 👍（8） 💬（1）<div>倪老师，您好：
1.从内核版本2.6.32以后，磁盘io调度算法好像只有3种，文中提到的none算法系统层没看到：
  cat &#47;sys&#47;block&#47;sda&#47;queue&#47;scheduler 
  noop anticipatory deadline [cfq]
2.在运行db的环境中，如MySQL，mysql的程序运行在机械硬盘上，mysql的数据目录是挂载在dell存储上(2个控制器有缓存)，存储也是由机械硬盘组成，做的raid10&#47;raid6
通过sysbench压测，其它环境保持一致，仅修改磁盘调度算法为noop&#47;deadline：
进行只读、读写测试，分别测试3轮，每轮10分钟，求平均值比较，50个并发线程，50张表每张100w数据，oltp场景，每轮测试后，清空系统缓存和重启mysql程序
压测结果：只读场景noop比deadline好一点点，读写场景deadline比noop好一点点
请问老师这种场景下，应该选择noop 还是 deadline？因为看到下面一篇文章有些疑惑

Choosing a Disk Scheduling Algorithm
The disk controller receives requests from the operating system and processes them in an order determined by a scheduling algorithm. Sometimes changing this algorithm can improve disk performance. For other hardware and workloads, it may not make a difference. The best way to decide is to test them out yourself on your workload. Dead‐ line and completely fair queueing (CFQ) both tend to be good choices.
There are a couple of situations where the noop scheduler (a contraction of “no-op” is the best choice): if you’re in a virtualized environment, use the noop scheduler. The noop scheduler basically passes the operations through to the underlying disk controller as quickly as possible. It is fastest to do this and let the real disk controller handle any reordering that needs to happen.
Similarly, on SSDs, the noop scheduler is generally the best choice. SSDs don’t have the same locality issues that spinning disks do.
Finally, if you’re using a RAID controller with caching, use noop. The cache behaves like an SSD and will take care of propagating the writes to the disk efficiently.

选择磁盘调度算法
磁盘控制器接收来自操作系统的请求，并按调度算法确定的顺序处理它们。有时更改此算法可以提高磁盘性能。对于其他硬件和工作负载，它可能没有什么区别。决定的最佳方法是自己测试工作量。deadline和CFQ往往都是不错的选择。
有几种情况下，noop调度程序是最佳选择：如果您处于虚拟化环境中，请使用noop调度程序。 noop调度程序基本上将操作尽快传递到底层磁盘控制器。这样做最快，让真正的磁盘控制器处理需要发生的任何重新排序。同样，在SSD上，noop调度程序通常是最佳选择。 SSD没有与旋转磁盘相同的位置问题。
最后，如果您使用带有缓存的RAID控制器，请使用noop。缓存的行为类似于SSD，并且会有效地将写入传播到磁盘。
</div>2019-01-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/e6/ee/e3c4c9b3.jpg" width="30px"><span>Cranliu</span> 👍（6） 💬（1）<div>最最常用的是iostat了吧？还有pidstat，sar等</div>2019-01-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/2f/f4/2dede51a.jpg" width="30px"><span>小老鼠</span> 👍（5） 💬（1）<div>固态硬盘有扇区和磁道吗？</div>2019-01-14</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/ccpIPibkaTQfYbO5DGiaWpL86YSHAZfVO55WtJhjV0hb7AuyIMzLyRdLnQZ6tjB0Wars4ib7YX3fhmPh9R81MVKtA/132" width="30px"><span>肘子哥</span> 👍（4） 💬（2）<div>smartctl工具有缺陷，对于虚拟机和做了raid的机器是失效的</div>2019-02-23</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTL9hlAIKQ1sGDu16oWLOHyCSicr18XibygQSMLMjuDvKk73deDlH9aMphFsj41WYJh121aniaqBLiaMNg/132" width="30px"><span>腾达</span> 👍（3） 💬（1）<div>系统从上到下一级级都有缓存，如果另外一个进程更新了数据，如何做到缓存失效的？</div>2019-01-16</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/65/ae/9727318e.jpg" width="30px"><span>Boy-struggle</span> 👍（1） 💬（2）<div>通用块层是属于内核调度吗？raid 应该属于哪一层？</div>2019-04-02</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/93/43/0e84492d.jpg" width="30px"><span>Maxwell</span> 👍（1） 💬（1）<div>之前讲的buffer和cache就是缓存磁盘IO机制吧？</div>2019-01-15</li><br/><li><img src="https://wx.qlogo.cn/mmopen/vi_32/PiajxSqBRaEKQMM4m7NHuicr55aRiblTSEWIYe0QqbpyHweaoAbG7j2v7UUElqqeP3Ihrm3UfDPDRb1Hv8LvPwXqA/132" width="30px"><span>ninuxer</span> 👍（1） 💬（1）<div>day25打卡
所以这也就是如kafka这类队列用磁盘的顺序io实现高速队列的依据，磁盘顺序io的性能比内存的好～</div>2019-01-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/ba/a7/7de1ed78.jpg" width="30px"><span>Lance_zhong</span> 👍（0） 💬（1）<div>老师，您好。请教一下，什么是随机IO和连续IO。谢谢。</div>2019-03-04</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/86/fa/4bcd7365.jpg" width="30px"><span>玉剑冰锋</span> 👍（0） 💬（1）<div>老师您好，文中提到的I&#47;O调度机械盘和SSD都适用吗？另外在实际生产环境中有没有针对不同场景适用哪种调度方法？使用后每种方法如何调优？</div>2019-01-16</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTLx1Jz78aibuoJEWdLTsDhucnVDTvkkeRX2w6ZJWXp0h7Zfe7GM6vKAx3jNhFhJJaElDCicyHpf1e9Q/132" width="30px"><span>13001236383</span> 👍（0） 💬（3）<div>FC好像是传输scisi的协议，不是硬盘接口吧</div>2019-01-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/fc/fc/1e235814.jpg" width="30px"><span>耿长学</span> 👍（0） 💬（1）<div>打卡，有点不懂呀，希望老师多来点案例，结合案例将原理</div>2019-01-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/a3/25/5da16c25.jpg" width="30px"><span>coyang</span> 👍（46） 💬（0）<div>1.用iostat看磁盘的await，utils，iops，bandwidth
2.用smartctl看磁盘的health status
3.用iotop&#47;pidstat找出持续读写的进程做优化</div>2019-01-15</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/2f/1d/a68c2b56.jpg" width="30px"><span>Utopia</span> 👍（24） 💬（0）<div>作为一个非科班出身，学习一年的程序员来说，看到这里，犹如打穿了任督二脉，叹为观止，太过瘾了。</div>2019-10-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/64/05/6989dce6.jpg" width="30px"><span>我来也</span> 👍（4） 💬（2）<div>[D24打卡]
以前其实并没太注意到磁盘I&#47;O的性能.
平常就正常存储下程序的日志,程序的日志量也不大.
但是有一次在某云上,生产环境中的程序卡了持续3分多钟.
后来才发现是程序中有人打了一个超级大(其实也就2-3M)的日志,😁.
然后程序就在这里阻塞了几分钟.</div>2019-01-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/22/f5/30/761c875a.jpg" width="30px"><span>Adrian</span> 👍（2） 💬（1）<div>感觉读法是否有问题，RAID10，是RAID1和RAID0组合起来的，我觉得应该读作RAID一零 而不是读作RAID十</div>2021-09-03</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/2o1Izf2YyJSnnI0ErZ51pYRlnrmibqUTaia3tCU1PjMxuwyXSKOLUYiac2TQ5pd5gNGvS81fVqKWGvDsZLTM8zhWg/132" width="30px"><span>划时代</span> 👍（2） 💬（0）<div>打卡总结</div>2019-01-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/d6/46/5eb5261b.jpg" width="30px"><span>Sudouble</span> 👍（1） 💬（0）<div>工程师们为了速度够，还真是想了各种各样的办法。一点点造就了现在的操作系统，向以前的工程师们致敬！</div>2022-03-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1b/7b/2b/97e4d599.jpg" width="30px"><span>Podman</span> 👍（1） 💬（2）<div>请教：
所以进程的I&#47;O请求进入文件系统后，会先访问buffer，如果buffer中存在请求内容，则直接返回请求
如果没有，那么才会从通用块层陷入磁盘设备做I&#47;O，并返回结果给到buffer，进而返回给进程。

这样理解对么</div>2021-12-16</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTJutT9JkFAcOpZk9YPKHypdRsa8swgstS1LdrtLVyp8hBLIFxxbRAibNDD9iacmUdmFTJFyTpRYmdCw/132" width="30px"><span>流金岁月</span> 👍（0） 💬（0）<div>linux系统中，操作emmc设备时导致系统IO占用率较高，这种场景的工作原理是怎样的呢，和磁盘IO的一样吗</div>2024-01-25</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/dd/9e/a68a6339.jpg" width="30px"><span>糯米</span> 👍（0） 💬（1）<div>请教下，关于图&quot;Linux 存储系统的 I&#47;O 栈全景图&quot;的一些疑惑，没看明白，还请老师能够解答。
1.图中的Page cache是包含了Buffer和Cache吗？
2.图中Direct I&#47;O（O_DIRECT）模式从图中看是直接调用BIOS进行读写磁盘，那么是不是就不经过Buffer了，即O_DIRECT模式的读写不会导致buffer的变化？但从第16节课中&quot;场景1：磁盘和文件写案例&quot;中使用dd if=dev&#47;urandom of=&#47;dev&#47;sdb1 bs=1M count=2048的实验来看buffer是变化的（这里的写磁盘应就是O_DIRECT模式吧）？</div>2023-08-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1a/e3/cc/0947ff0b.jpg" width="30px"><span>nestle</span> 👍（0） 💬（0）<div>每种类型的存储设备都有各自的接口协议，需要一套特定的代码进行控制，这个代码就是设备驱动程序，是包含在内核代码中的。通用块层向下就是和驱动程序打交道，真正控制物理设备的是设备驱动程序。
请问这样的理解对吗？</div>2022-11-04</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/99/c3/e4f408d4.jpg" width="30px"><span>陌兮</span> 👍（0） 💬（0）<div>这一章看的是真的舒服，太过瘾了</div>2022-06-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/5b/6b/2ddbeab2.jpg" width="30px"><span>allen</span> 👍（0） 💬（1）<div>老师，我今天遇到个问题，有个oracle数据库服务器，用dd命令写磁盘时，分别用直接落盘 闲着缓存再落盘的方式，发现写缓存的方式时，前段应用服务器就出现延时，不经过缓存直接写硬盘事就一切正常，服务器配置全新，256G没错，请问是啥原因？</div>2021-11-05</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/f0/17/796a3d20.jpg" width="30px"><span>言十年</span> 👍（0） 💬（2）<div>其中，通用块层是 Linux 磁盘 I&#47;O 的核心。向上，它为文件系统和应用程序，提供访问了块设备的标准接口；向下，把各种异构的磁盘设备，抽象为统一的块设备，并会对文件系统和应用程序发来的 I&#47;O 请求进行重新排序、请求合并等，提高了磁盘访问的效率。

不是文件系统层提供向上的接口么？怎么是通用块层？块层在文件系统层下面呢呀......</div>2021-08-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/19/d9/ff/b23018a6.jpg" width="30px"><span>Heaven</span> 👍（0） 💬（1）<div>也就是说,实际的缓存和缓冲发生在VFS层,而非下层的通用块层是吗</div>2021-05-21</li><br/>
</ul>