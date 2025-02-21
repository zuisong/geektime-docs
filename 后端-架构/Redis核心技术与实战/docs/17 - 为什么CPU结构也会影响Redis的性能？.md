你好，我是蒋德钧。

很多人都认为Redis和CPU的关系很简单，就是Redis的线程在CPU上运行，CPU快，Redis处理请求的速度也很快。

这种认知其实是片面的。CPU的多核架构以及多CPU架构，也会影响到Redis的性能。如果不了解CPU对Redis的影响，在对Redis的性能进行调优时，就可能会遗漏一些调优方法，不能把Redis的性能发挥到极限。

今天，我们就来学习下目前主流服务器的CPU架构，以及基于CPU多核架构和多CPU架构优化Redis性能的方法。

## 主流的CPU架构

要了解CPU对Redis具体有什么影响，我们得先了解一下CPU架构。

一个CPU处理器中一般有多个运行核心，我们把一个运行核心称为一个物理核，每个物理核都可以运行应用程序。每个物理核都拥有私有的一级缓存（Level 1 cache，简称L1 cache），包括一级指令缓存和一级数据缓存，以及私有的二级缓存（Level 2 cache，简称L2 cache）。

这里提到了一个概念，就是物理核的私有缓存。它其实是指缓存空间只能被当前的这个物理核使用，其他的物理核无法对这个核的缓存空间进行数据存取。我们来看一下CPU物理核的架构。

![](https://static001.geekbang.org/resource/image/c2/3a/c2d620c012a82e825570df631a7fbc3a.jpg?wh=2114%2A1167)

因为L1和L2缓存是每个物理核私有的，所以，当数据或指令保存在L1、L2缓存时，物理核访问它们的延迟不超过10纳秒，速度非常快。那么，如果Redis把要运行的指令或存取的数据保存在L1和L2缓存的话，就能高速地访问这些指令和数据。
<div><strong>精选留言（30）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/23/31/d2/56bf47c8.jpg" width="30px"><span>薛定谔的猫</span> 👍（68） 💬（7）<div>小白请教一下，网络中断处理程序是指什么呢？</div>2020-11-25</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/23/cd/de/0334fd13.jpg" width="30px"><span>许峰</span> 👍（27） 💬（2）<div>阿里云ecs主机都是vcpus, 这玩意算物理核心吗?
比如一个4vcpu, lscpu可以看到
NUMA node0 CPU(s):     0-3
这么绑?</div>2020-11-30</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/19/91/c4/bcdcda65.jpg" width="30px"><span>T</span> 👍（17） 💬（1）<div>很多人都认为 Redis 和 CPU 的关系很简单，就是 Redis 的线程在 CPU 上运行，CPU 快，Redis 处理请求的速度也很快。
这种认知其实是片面的。CPU 的多核架构以及多 CPU 架构，也会影响到 Redis 的性能。如果不了解 CPU 对 Redis 的影响，在对 Redis 的性能进行调优时，就可能会遗漏一些调优方法，不能把 Redis 的性能发挥到极限。</div>2020-11-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/90/8a/288f9f94.jpg" width="30px"><span>Kaito</span> 👍（336） 💬（38）<div>这篇文章收获很大！对于CPU结构和如何绑核有了进一步了解。其实在NUMA架构下，不光对于CPU的绑核需要注意，对于内存的使用，也有很多注意点，下面回答课后问题，也会提到NUMA架构下内存方面的注意事项。

在一台有2个CPU Socket（每个Socket 8个物理核）的服务器上，我们部署了有8个实例的Redis切片集群（8个实例都为主节点，没有主备关系），采用哪种方案绑核最佳？

我更倾向于的方案是：在两个CPU Socket上各运行4个实例，并和相应Socket上的核绑定。这么做的原因主要从L3 Cache的命中率、内存利用率、避免使用到Swap这三个方面考虑：

1、由于CPU Socket1和2分别有自己的L3 Cache，如果把所有实例都绑定在同一个CPU Socket上，相当于这些实例共用这一个L3 Cache，另一个CPU Socket的L3 Cache浪费了。这些实例共用一个L3 Cache，会导致Cache中的数据频繁被替换，访问命中率下降，之后只能从内存中读取数据，这会增加访问的延迟。而8个实例分别绑定CPU Socket，可以充分使用2个L3 Cache，提高L3 Cache的命中率，减少从内存读取数据的开销，从而降低延迟。

2、如果这些实例都绑定在一个CPU Socket，由于采用NUMA架构的原因，所有实例会优先使用这一个节点的内存，当这个节点内存不足时，再经过总线去申请另一个CPU Socket下的内存，此时也会增加延迟。而8个实例分别使用2个CPU Socket，各自在访问内存时都是就近访问，延迟最低。

3、如果这些实例都绑定在一个CPU Socket，还有一个比较大的风险是：用到Swap的概率将会大大提高。如果这个CPU Socket对应的内存不够了，也可能不会去另一个节点申请内存（操作系统可以配置内存回收策略和Swap使用倾向：本节点回收内存&#47;其他节点申请内存&#47;内存数据换到Swap的倾向程度），而操作系统可能会把这个节点的一部分内存数据换到Swap上从而释放出内存给进程使用（如果没开启Swap可会导致直接OOM）。因为Redis要求性能非常高，如果从Swap中读取数据，此时Redis的性能就会急剧下降，延迟变大。所以8个实例分别绑定CPU Socket，既可以充分使用2个节点的内存，提高内存使用率，而且触发使用Swap的风险也会降低。

其实我们可以查一下，在NUMA架构下，也经常发生某一个节点内存不够，但其他节点内存充足的情况下，依旧使用到了Swap，进而导致软件性能急剧下降的例子。所以在运维层面，我们也需要关注NUMA架构下的内存使用情况（多个内存节点使用可能不均衡），并合理配置系统参数（内存回收策略&#47;Swap使用倾向），尽量去避免使用到Swap。</div>2020-09-16</li><br/><li><img src="" width="30px"><span>Geek_9b08a5</span> 👍（33） 💬（0）<div>1.作者讲了什么？
	在多核CPU架构和NUMA架构下，如何对redis进行优化配置
2.作者是怎么把这件事将明白的？
	1，讲解了主流的CPU架构，主要有多核CPU架构和NUMA架构两个架构
		多核CPU架构： 多个物理核，各物理核使用私有的1、2级缓存，共享3级缓存。物理核可包含2个超线程，称为逻辑核
		NUMA架构： 一个服务器上多个cpu，称为CPU Socket，每个cpu socker存在多个物理核。每个socket通过总线连接，并且有用私有的内存空间
3.为了讲明白，作者讲了哪些要点，哪些亮点？
	1、亮点：将主流的CPU架构进行剖析，使人更好理解cpu的原理，有助于后续redis性能的优化
	2、要点：cpu架构：一个cpu一般拥有多个物理核，每个物理核都拥有私有的一级缓存，二级缓存。三级缓存是各物理核共享的缓存空间。而物理核又可以分为多个超线程，称为逻辑核，同一个物理核的逻辑核会共享使用 L1、L2 缓存。
	3、要点：一级缓存和二级缓存访问延迟不超过10纳秒，但空间很小，只是KB单位。而应用程序访问内存延迟是百纳秒级别，基本上是一二级缓存的10倍
	4、要点：不同的物理核还会共享一个共同的三级缓存，三级缓存空间比较多，为几到几十MB，当 L1、L2 缓存中没有数据缓存时，可以访问 L3，尽可能避免访问内存。
	5、要点：多核CPU运行redis实例，会导致context switch，导致增加延迟，可以通过taskset 命令把redis进程绑定到某个cup物理核上。
	6、要点：NUMA架构运行redis实例，如果网络中断程序和redis实例运行在不同的socket上，就需要跨 CPU Socket 访问内存，这个过程会花费较多时间。
	7、要点：绑核的风险和解决方案：
			一个 Redis 实例对应绑一个物理核 ： 将redis服务绑定到一个物理核上，而不是一个逻辑核上，如 taskset -c 0,12 .&#47;redis-server
			优化 Redis 源码。
4.对于作者所讲的，我有哪些发散性思考？
给自己提了几个问题：
	1，在多核CPU架构和NUMA架构，那个对于redis来说性能比较好
	2，如何设置网络中断处理和redis绑定设置在同个socket上呢？

5.将来在哪些场景里，我能够使用它？

6.留言区收获
	如果redis实例中内存不足以使用时，会用到swap那会怎么样？（答案来自@kaito 大佬）
		因为Redis要求性能非常高，如果从Swap中读取数据，此时Redis的性能就会急剧下降，延迟变大。</div>2020-12-30</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/43/79/18073134.jpg" width="30px"><span>test</span> 👍（16） 💬（2）<div>课后问题：我会选择方案二。首先一个实例不止有一个线程需要运行，所以方案一肯定会有CPU竞争问题；其次切片集群的通信不是通过内存，而是通过网络IO。</div>2020-09-16</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/71/3d/da8dc880.jpg" width="30px"><span>游弋云端</span> 👍（12） 💬（0）<div>有两套房子，就不用挤着睡吧，优选方案二。老师实验用的X86的CPU吧，对于ARM架构来讲，存在着跨DIE和跨P的说法，跨P的访问时延会更高，且多个P之间的访问存在着NUMA distances的说法，不同的布局导致的跨P访问时延也不相同。</div>2020-09-16</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/5c/8f/551b5624.jpg" width="30px"><span>小可</span> 👍（11） 💬（3）<div>这篇文章真是太好了！对cpu有了更多的认识，公司服务lscpu挨个看了一遍，不懂的地方也去查了资料，自己也画了NUMA架构下多个cpu socket示意图，给每个逻辑cpu编号，对照图看怎么绑定网络中断和redis实例到同一个cpu socket，怎么绑定一个redis实例到同一个物理核，非常清晰！还有cpu的架构设计思路也可以应用到我们实际系统架构上，不得不赞叹这些神级设计，也感谢老师心细深入的讲解，真的发现宝藏了，O(∩_∩)O哈哈~</div>2021-02-04</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/20/e9/32/b89fcc77.jpg" width="30px"><span>元末</span> 👍（6） 💬（0）<div>这篇文章很顶</div>2021-07-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/41/5e/9d2953a3.jpg" width="30px"><span>zhou</span> 👍（5） 💬（0）<div>在 NUMA 架构下，比如有两个 CPU Socket：CPU Socket 1 和 CPU Socket 2，每个 CPU Socket 都有自己的内存，CPU Socket 1 有自己的内存 Mem1，CPU Socket 2 有自己的内存 Mem2。

Redis 实例在 CPU Socket 1 上执行，网络中断处理程序在 CPU Socket 2 上执行，所以 Redis 实例的数据在内存 Mem1 上，网络中断处理程序的数据在 Mem2上。

因此 Redis 实例读取网络中断处理程序的内存数据（Mem2）时，是需要远端访问的，比直接访问自己的内存数据（Mem1）要慢。
</div>2020-09-16</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/61/23/30d134cf.jpg" width="30px"><span>Young</span> 👍（3） 💬（0）<div>老师您好，有个疑问： 即使内核绑定，但是当cpu时间片用尽，context switch依然会发生对吧？ 之后，cache里的数据会被刷掉， 所谓绑定的优势如何保证呢？ 谢谢！</div>2021-05-06</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/ca/4b/c1ace3aa.jpg" width="30px"><span>蚝不鱿鱼</span> 👍（2） 💬（1）<div>结合隔壁我浩哥的计算机组成原理课程食用本节内容是真的香，感谢钧哥。</div>2021-01-13</li><br/><li><img src="" width="30px"><span>Geek_728b54</span> 👍（1） 💬（0）<div>这篇文章我是跪着看完的</div>2023-07-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/2e/3c/08/93bde3ee.jpg" width="30px"><span>⚽️</span> 👍（1） 💬（0）<div>网络中断和cpu怎么绑定啊</div>2022-08-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/43/f9/723ee153.jpg" width="30px"><span>wessonwang</span> 👍（1） 💬（0）<div>课后题，选第二种方案，相对于第一种方案来说，8个实例竞争一个L3 cache，比4个实例竞争要激烈的多，容易出现某些实例的L3缓存被刷出，搞得又得去内存加载数据。</div>2021-12-01</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/e2/d8/f0562ede.jpg" width="30px"><span>manatee</span> 👍（1） 💬（0）<div>请问网络中断程序如何绑核呢</div>2021-04-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/77/2a/4f72941e.jpg" width="30px"><span>cpzhao</span> 👍（1） 💬（0）<div>挺有收获，以前学习比较少关注系统cpu结构这块。这次顺带也了解cpu亲和度、NUMA结构相关的知识点，希望老师也可以在文章中推荐一些相关知识点的学习链接之类的。</div>2020-11-16</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/18/3e/3a/2267d2a3.jpg" width="30px"><span>hoppo</span> 👍（1） 💬（0）<div>这篇文章确实收获很大，从CPU核心说到NUMA架构、我原来其实就是抱着 ”Redis 的线程在 CPU 上运行，CPU 越快，Redis 处理请求的速度也越快”相法的。现在想来真是太肤浅了...orz（失意体前屈）

不过一步一步跟着老师的思路来，还是很容易理解的，读到远端内存访问影响性能的时候，就会想是不是可以分到一个核上；看完了绑核的优点介绍又联系到风险和解决方式，一气呵成，给老师点个赞~</div>2020-11-15</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/b6/75/32c19395.jpg" width="30px"><span>土豆白菜</span> 👍（1） 💬（0）<div>老师，我也想问下比如azure redis 能否做这些优化</div>2020-09-16</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/8f/cf/890f82d6.jpg" width="30px"><span>那时刻</span> 👍（1） 💬（2）<div>请问老师，您文中提到我们仔细检测了 Redis 实例运行时的服务器 CPU 的状态指标值，这才发现，CPU 的 context switch 次数比较多。再遇到这样的问题的时候，排查的点有哪些呢？</div>2020-09-16</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/e6/9a/d0725a24.jpg" width="30px"><span>Athena</span> 👍（0） 💬（0）<div>这章是真的牛逼，反复看了几次</div>2023-03-05</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/69/bc/c22bf219.jpg" width="30px"><span>妥妥</span> 👍（0） 💬（0）<div>老师请教一下，不修改redis源码的情况下，为什么不干脆绑定同一个cpu socket下的三个核心？这样就不会有cpu资源的竞争了</div>2022-10-16</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/23/4c/89/82a3ee04.jpg" width="30px"><span>going</span> 👍（0） 💬（0）<div>同一个socket运行八个实例。
</div>2022-08-05</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/17/2e/6d/00a1c1b1.jpg" width="30px"><span>Nerd</span> 👍（0） 💬（0）<div>才知道一台服务器可以有多个 CPU 的配置，学习了</div>2022-05-06</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1b/68/ec/eb0ebbb6.jpg" width="30px"><span>日月星辰</span> 👍（0） 💬（0）<div>taskset 是操作系统的命令还是 Redis 的命令，感觉应该是操作系统的命令，但是不知道对不对。</div>2022-02-16</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/15/f9/0b14785a.jpg" width="30px"><span>三三</span> 👍（0） 💬（0）<div>原来一根内存只会被一个cpu管理，本章学习到了不少东西</div>2022-02-07</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/18/41/13/bf8e85cc.jpg" width="30px"><span>树心</span> 👍（0） 💬（0）<div>收获很多，对底层cpu知识有了更多的了解！</div>2021-12-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/24/78/29/188c9bce.jpg" width="30px"><span>长路漫漫</span> 👍（0） 💬（0）<div>这节课很有收获</div>2021-12-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/b2/e0/d856f5a4.jpg" width="30px"><span>余松</span> 👍（0） 💬（0）<div>NUMA下的缓存模式和多IDC部署的系统中的Redis使用方式何其相似，在多IDC部署中，相关的系统尽量放在一个机房共用一个Redis集群而不是跨越公网（NUMA下的总线）去另外一个机房获取缓存数据。</div>2021-10-15</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/34/67/06a7f9be.jpg" width="30px"><span>while (1)等;</span> 👍（0） 💬（0）<div>之前以为CPU核越多性能越强，机器都用的48核，上面只部署一个实例，是不是很浪费？按老师说的是不是两核就够了</div>2021-09-28</li><br/>
</ul>