我们前面说了，容器实现封闭的环境主要靠两种技术，一种是“看起来是隔离”的技术Namespace，另一种是用起来是隔离的技术cgroup。

上一节我们讲了“看起来隔离“的技术Namespace，这一节我们就来看一下“用起来隔离“的技术cgroup。

cgroup全称是control group，顾名思义，它是用来做“控制”的。控制什么东西呢？当然是资源的使用了。那它都能控制哪些资源的使用呢？我们一起来看一看。

首先，cgroup定义了下面的一系列子系统，每个子系统用于控制某一类资源。

- CPU子系统，主要限制进程的CPU使用率。
- cpuacct 子系统，可以统计 cgroup 中的进程的 CPU 使用报告。
- cpuset 子系统，可以为 cgroup 中的进程分配单独的 CPU 节点或者内存节点。
- memory 子系统，可以限制进程的 Memory 使用量。
- blkio 子系统，可以限制进程的块设备 IO。
- devices 子系统，可以控制进程能够访问某些设备。
- net\_cls 子系统，可以标记 cgroups 中进程的网络数据包，然后可以使用 tc 模块（traffic control）对数据包进行控制。
- freezer 子系统，可以挂起或者恢复 cgroup 中的进程。
<div><strong>精选留言（13）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/13/39/fa/a7edbc72.jpg" width="30px"><span>安排</span> 👍（5） 💬（1）<div>Cgroup文件系统是只存在内存中吗？每一次设置之后在掉电后是不是就消失了？</div>2019-08-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/a0/3f/06b690ba.jpg" width="30px"><span>刘桢</span> 👍（4） 💬（6）<div>二十天闭关冲北邮</div>2019-08-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/3b/36/2d61e080.jpg" width="30px"><span>行者</span> 👍（8） 💬（1）<div>老师，麻烦讲下华为鸿蒙系统，它和linux区别与联系是什么？</div>2019-08-10</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/4kF5cFK9MN5PuSvNzkgpH4bk0Fcmt2SVIXsQ2tLsRZnv9YI2KZqiafhNejhIjWiaNYnmma5G2s6d8I5T9ovOJxyA/132" width="30px"><span>张亚琛</span> 👍（4） 💬（0）<div>补充一些背景：

Cgroup是Linux系统内核提供的一种机制，它是在Linux 内核版本 2.6.24中引入的，来解决资源管理和隔离的问题。在它出现之前，Linux只能对单个进程进行资源限制，例如通过sched_setaffinity设置进程CPU亲和性，使用ulimit限制进程打开文件上限、栈大小等。

在这个时代，有一些早期的容器技术，如Chroot和Linux VServer。
Chroot 可以将进程及其子进程与操作系统的其余部分隔离开来，但是，对于 root process，却可以任意退出 chroot。
Linux VServer 是一种基于 Security Contexts 的软分区技术，可以做到虚拟服务器隔离，共享相同的硬件资源。主要问题是 VServer 应用程序针对 &quot;chroot-again&quot; 类型的攻击没有很好的进行安全保护，攻击者可以利用这个漏洞脱离限制环境，访问限制目录之外的任意文件。

虽然在没有 Cgroup 技术的情况下，还有其他的方法可以实现一定程度的资源隔离和管理，但是这些方法在处理多进程或者进程组的资源管理时显得力不从心，而且在安全性和功能性方面也存在一些问题。

随着容器技术的发展，Docker的开发者在了解并掌握了 Cgroup 技术之后，应用这项技术去实现Docker 的资源管理和隔离功能。因此，Cgroup 不仅解决了 Linux 系统的资源管理问题，也为容器技术的发展提供了基础。


</div>2024-02-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/21/85/609a2e51.jpg" width="30px"><span>fhchina</span> 👍（3） 💬（0）<div>cpu.cfs_period_us的单位是us, 微秒不是毫秒</div>2019-11-23</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTLTFKH3aA1FVyz7VvAIlISibAPbmiaAyQ5fAK3ElyEcXuRmsmicAefXxkhbC11icjBgfbXPXkHHt5O0xw/132" width="30px"><span>羊仔爸比</span> 👍（1） 💬（1）<div>老师：
      请教一下docker 里面我设置了 内存的limit是2g，cgroup 文件中memory.usage_in_bytes这个文件是是包含memory.stat中的total_rss 和total_cache 相加的大小，oom kill的时候会根据memory.usage_in_bytes的值kill吗，如果不是根据这个文件的值kill是根据哪个值进行kill的？</div>2020-05-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/d0/4d/2116c1a4.jpg" width="30px"><span>Bravery168</span> 👍（0） 💬（0）<div>容器从概念上就是通过各种数据结构的定义建构了一个模型，从执行层面，本质上是对进程资源和行为的定义和控制。牛</div>2022-12-15</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/e0/cf/43f201f2.jpg" width="30px"><span>幼儿编程教学</span> 👍（0） 💬（0）<div>&gt;第五步，对于 CPU 来讲，会修改 scheduled entity，放入相应的队列里面去，从而下次调度的时候就起作用了。对于内存的 cgroup 设定，只有在申请内存的时候才起作用。

请教老师，2个我比较非常的问题。
* 设置 cgroup cpu后，极端情况下，是否会突发cpu超过限制？
文章中说”对于 CPU 来讲，会修改 scheduled entity，放入相应的队列里面去，从而下次调度的时候就起作用了“。如果1个进程，占用时间太长，或者短时间内，耗费了很多cpu，是否会引发cpu超量使用，导致系统卡死？k8s中，如果cpu设置的不好（配置大于宿主机实际量），是会引发宿主机卡死的情况。这时候，只能重启宿主机
* 设置 cgroup memory后，极端情况下，是否会突发memory超过限制？
内存好像会？因为上面说，”只有在申请内存的时候才起作用“。那之前申请的内存呢？申请内存的时候，申请的都是虚拟内存。假设宿主机只有1g内存。2个进程a,b，都申请内存1g。内存应该是在实际使用时，才会去分配。所以，进程a,b运行起来，可以超过宿主机实际1g内存。这时，操作系统会oom。应该是这样吧？</div>2022-11-02</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/d6/46/5eb5261b.jpg" width="30px"><span>Sudouble</span> 👍（0） 💬（0）<div>这么多篇深度文章，很好的诠释了十几年前的一个疑问，为什么不让电脑突然断电！内存、缓存里存的大量数据，操作系统还没有触发写，这时突然断电，这部分数据全都丢了。</div>2022-06-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/2a/27/65/0790efd2.jpg" width="30px"><span>EST4What</span> 👍（0） 💬（0）<div>为什么我mount -t cgroup会显示，而切换到&#47;sys&#47;fs&#47;cgroup时，文件却不见了呢

[root@jenkins cgroup]# mount -t cgroup 
cgroup on &#47;sys&#47;fs&#47;cgroup&#47;systemd type cgroup (rw,nosuid,nodev,noexec,relatime,seclabel,xattr,release_agent=&#47;usr&#47;lib&#47;systemd&#47;systemd-cgroups-agent,name=systemd)
cgroup on &#47;sys&#47;fs&#47;cgroup&#47;memory type cgroup (rw,nosuid,nodev,noexec,relatime,seclabel,memory)
cgroup on &#47;sys&#47;fs&#47;cgroup&#47;devices type cgroup (rw,nosuid,nodev,noexec,relatime,seclabel,devices)
cgroup on &#47;sys&#47;fs&#47;cgroup&#47;cpu,cpuacct type cgroup (rw,nosuid,nodev,noexec,relatime,seclabel,cpuacct,cpu)
cgroup on &#47;sys&#47;fs&#47;cgroup&#47;hugetlb type cgroup (rw,nosuid,nodev,noexec,relatime,seclabel,hugetlb)
cgroup on &#47;sys&#47;fs&#47;cgroup&#47;cpuset type cgroup (rw,nosuid,nodev,noexec,relatime,seclabel,cpuset)
cgroup on &#47;sys&#47;fs&#47;cgroup&#47;freezer type cgroup (rw,nosuid,nodev,noexec,relatime,seclabel,freezer)
cgroup on &#47;sys&#47;fs&#47;cgroup&#47;perf_event type cgroup (rw,nosuid,nodev,noexec,relatime,seclabel,perf_event)
cgroup on &#47;sys&#47;fs&#47;cgroup&#47;blkio type cgroup (rw,nosuid,nodev,noexec,relatime,seclabel,blkio)
cgroup on &#47;sys&#47;fs&#47;cgroup&#47;net_cls,net_prio type cgroup (rw,nosuid,nodev,noexec,relatime,seclabel,net_prio,net_cls)
cgroup on &#47;sys&#47;fs&#47;cgroup&#47;pids type cgroup (rw,nosuid,nodev,noexec,relatime,seclabel,pids)
[root@jenkins cgroup]# ls
[root@jenkins cgroup]# ll
total 0

</div>2022-03-02</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/5e/61/985f3eb7.jpg" width="30px"><span>songyy</span> 👍（0） 💬（0）<div>testnginx 不在docker的repo里面吧。示例里面

 docker run -d --cpu-shares 513 --cpus 2 --cpuset-cpus 1,3 --memory 1024M --memory-swap 1234M --memory-swappiness 7 -p 8081:80 testnginx:1

这个代码就跑不起来了</div>2021-07-04</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTKOnpl8fRB9r2vED2s8j7Arwbn2K6M6HUBWNjgoqV4uqe94fTGK4WGpOJLeRxXcBXk3dp23eQR0AQ/132" width="30px"><span>吴钩</span> 👍（0） 💬（0）<div>对namespace和cgroup了解增加了很多，赞！</div>2021-04-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/4d/fd/0aa0e39f.jpg" width="30px"><span>许童童</span> 👍（0） 💬（0）<div>跟着老师一起精进。</div>2019-08-09</li><br/>
</ul>