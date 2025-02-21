你好，我是程远。这一讲，我们来看看容器中是否可以使用Swap空间。

用过Linux的同学应该都很熟悉Swap空间了，简单来说它就是就是一块磁盘空间。

当内存写满的时候，就可以把内存中不常用的数据暂时写到这个Swap空间上。这样一来，内存空间就可以释放出来，用来满足新的内存申请的需求。

它的好处是可以**应对一些瞬时突发的内存增大需求**，不至于因为内存一时不够而触发OOM Killer，导致进程被杀死。

那么对于一个容器，特别是容器被设置了Memory Cgroup之后，它还可以使用Swap空间吗？会不会出现什么问题呢？

## 问题再现

接下来，我们就结合一个小例子，一起来看看吧。

首先，我们在一个有Swap空间的节点上启动一个容器，设置好它的Memory Cgroup的限制，一起来看看接下来会发生什么。

如果你的节点上没有Swap分区，也没有关系，你可以用下面的[这组命令](https://github.com/chengyli/training/blob/main/memory/swap/create_swap.sh)来新建一个。

这个例子里，Swap空间的大小是20G，你可以根据自己磁盘空闲空间来决定这个Swap的大小。执行完这组命令之后，我们来运行free命令，就可以看到Swap空间有20G。

输出的结果你可以参考下面的截图。

![](https://static001.geekbang.org/resource/image/33/5b/337a5efa84fc64f5a7ab2b12295e8b5b.png?wh=1622%2A496)

然后我们再启动一个容器，和OOM那一讲里的[例子](https://github.com/chengyli/training/blob/main/memory/oom/start_container.sh)差不多，容器的Memory Cgroup限制为512MB，容器中的mem\_alloc程序去申请2GB内存。
<div><strong>精选留言（15）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/15/ff/46/7e4039ea.jpg" width="30px"><span>伟平</span> 👍（20） 💬（2）<div>k8s下容器貌似不能用swap</div>2020-12-07</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/5e/96/a03175bc.jpg" width="30px"><span>莫名</span> 👍（10） 💬（1）<div>Memory Cgroup 参数 memory.swappiness 起到局部控制的作用，前提是节点开启了 swap 功能，不然无论如何设置都无济于事。</div>2020-12-07</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/7e/99/c4302030.jpg" width="30px"><span>Khirye</span> 👍（8） 💬（2）<div> 想问下老师，对于最近k8s宣布放弃docker有什么看法？</div>2020-12-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1c/f4/c7/037235c9.jpg" width="30px"><span>kimoti</span> 👍（8） 💬（2）<div>既然memory.swappiness设置为0了,Swap分区是不会有数据写入的。</div>2020-12-07</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/9f/a1/d75219ee.jpg" width="30px"><span>po</span> 👍（2） 💬（5）<div>老师，文章中你说的这两句话好像是矛盾的，swappiness设置为0的时候，到底会不会回收匿名内存呢？
1. 不过，这里有一点不同，需要你留意：当 memory.swappiness = 0 的时候，对匿名页的回收是始终禁止的，也就是始终都不会使用 Swap 空间。这时 Linux 系统不会再去比较 free 内存和 zone 里的 high water mark 的值，再决定一个 Memory Cgroup 中的匿名内存要不要回收了。请你注意，当我们设置了&quot;memory.swappiness=0 时，在 Memory Cgroup 中的进程，就不会再使用 Swap 空间，知道这一点很重要.

2. 值为 0 的时候，当系统中空闲内存低于一个临界值的时候，仍然会释放匿名内存并把页面写入 Swap 空间。</div>2020-12-15</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/e4/8b/8a0a6c86.jpg" width="30px"><span>haha</span> 👍（2） 💬（1）<div>所以对于开启了swap，且swap空间够大的前提下，goup的mem limit没用咯?</div>2020-12-15</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1e/f5/97/9a7ee7b3.jpg" width="30px"><span>Geek4329</span> 👍（2） 💬（1）<div>感谢老师的分享，学习的越多，越感到自己的自信😼

学完这个课程，并完全吸收的话，是不是可以说自己接近精通容器技术了😁</div>2020-12-07</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/b0/c8/cae61286.jpg" width="30px"><span>chong chong</span> 👍（1） 💬（1）<div>老师，k8s pod默认的memory.swappiness 值是60，如何设置才能使得默认是0呢？</div>2021-05-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/23/81/60/71ed6ac7.jpg" width="30px"><span>谢哈哈</span> 👍（1） 💬（1）<div>已经设置memory.swappiness参数，全局参数swappiness参数失效，那么容器里就不能使用swap了</div>2020-12-07</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/27/8e/3e/bdfb6dc3.jpg" width="30px"><span>刘宏</span> 👍（1） 💬（1）<div>请问一下在容器里如何加快page cache的释放速度，原因是发现scp的时候，page cache会很快将内存占满，速度会骤然下降，drop cache以后，速度能显著提升；配置了vm.vfs_cache_pressure为1w，依旧在容器里没改善</div>2021-10-03</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/2a/ff/a9d72102.jpg" width="30px"><span>BertGeek</span> 👍（1） 💬（0）<div>1、swappiness（&#47;proc&#47;sys&#47;vm&#47;swappiness） 的取值范围在 0 到 100 之间，我们可以记住下面三个值：
1.1 值为 100 的时候，释放 Page Cache 和匿名内存是同等优先级的。
1.2 值为 60，这是大多数 Linux 系统的缺省值，这时候 Page Cache 的释放优先级高于匿名内存的释放。
1.3 值为0，也不能完全禁止 Swap 分区的使用，就是当系统中空闲内存低于一个临界值的时候，仍然会通过swap回收匿名内存（释放匿名内存并把页面写入 Swap 空间）。

2、Memroy Cgroup 控制组中的memory.swappiness参数
    如果设置memory.swappiness参数，此容器中的全局swappiness参数失效，那么此容器里就不能使用swap了</div>2021-07-05</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1f/56/a4/9d4089e8.jpg" width="30px"><span>Yann彦</span> 👍（0） 💬（0）<div>k8s集群中是否建议打开swap呢？打开过关闭有什么优缺点呢？</div>2022-08-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/8d/6d/8c0a487b.jpg" width="30px"><span>册书一幕</span> 👍（0） 💬（2）<div>“不过，这里有一点不同，需要你留意：当 memory.swappiness = 0 的时候，对匿名页的回收是始终禁止的，也就是始终都不会使用 Swap 空间。”
这句话是指的仅在cgroup情况下吗？在主机下，memory.swappiness = 0是不会分配swap但是会回收</div>2022-04-04</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/8d/6d/8c0a487b.jpg" width="30px"><span>册书一幕</span> 👍（0） 💬（0）<div>不过，这里有一点不同，需要你留意：当 memory.swappiness = 0 的时候，对匿名页的回收是始终禁止的，也就是始终都不会使用 Swap 空间。</div>2022-04-04</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/a6/69/cf2eb6be.jpg" width="30px"><span>景b</span> 👍（0） 💬（0）<div>如果有分布式存储的能力且能做到按卷级别做限速，每个容器都是单独挂一个卷进去，是不是开swap就利大于弊。可以这么理解不</div>2021-11-07</li><br/>
</ul>