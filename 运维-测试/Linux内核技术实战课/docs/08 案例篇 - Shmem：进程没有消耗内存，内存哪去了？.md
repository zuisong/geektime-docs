你好，我是邵亚方。

在前一节课，我们讲述了进程堆内存的泄漏以及因为内存泄漏而导致的OOM的危害。这节课我们继续讲其他类型的内存泄漏，这样你在发现系统内存越来越少时，就能够想到会是什么在消耗内存。

有的内存泄漏会体现在进程内存里面，这种相对好观察些；而有的内存泄漏就很难观察了，因为它们无法通过观察进程消耗的内存来进行判断，从而容易被忽视，比如Shmem内存泄漏就属于这种容易被忽视的，这节课我们重点来讲讲它。

## 进程没有消耗内存，内存哪去了？

我生产环境上就遇到过一个真实的案例。我们的运维人员发现某几台机器used（已使用的）内存越来越多，但是通过top以及其他一些命令，却检查不出来到底是谁在占用内存。随着可用内存变得越来越少，业务进程也被OOM killer给杀掉，这给业务带来了比较严重的影响。于是他们向我寻求帮助，看看产生问题的原因是什么。

我在之前的课程中也提到过，在遇到系统内存不足时，我们首先要做的是查看/proc/meminfo中哪些内存类型消耗较多，然后再去做针对性分析。但是如果你不清楚/proc/meminfo里面每一项的含义，即使知道了哪几项内存出现了异常，也不清楚该如何继续去分析。所以你最好是记住/proc/meminfo里每一项的含义。
<div><strong>精选留言（13）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/0f/97/2e/100345a3.jpg" width="30px"><span>springchan</span> 👍（12） 💬（1）<div>老师您好，
有一个疑问：tmpfs是一种基于内存的虚拟文件系统，存储空间是在虚拟内存里，重启机器后会丢失，但是我用mmap 在tmpfs下面映射文件以后，通过使用stat 查看tmpfs下面的文件，为什么会占用block 块呢？block 块不是硬盘的空间么？</div>2020-09-17</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTKT9Tk01eiaQ9aAhszthzGm6lwruRWPXia1YYFozctrdRvKg0Usp8NbwuKBApwD0D6Fty2tib3RdtFJg/132" width="30px"><span>欧阳洲</span> 👍（7） 💬（1）<div>老师好，看完这一讲有两个疑问想请教：
（1）tmpfs的特点是快，那么与内存有什么不同呢？
假设一个app只有白天可访问，晚上不提供服务。
白天用tmpfs，晚上再来做耗时的部分：写磁盘，清理tmpfs。
那这样的话，为什么白天不直接存储在内存就好，不必写入tmpfs吧？
（2）tmpfs与mmap有什么区别和联系吗，除了mmap属于进程，tmpfs不属于进程之外。</div>2020-09-10</li><br/><li><img src="https://wx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTIt0nAFvqib3fpf9AIKUrEJMdbiaPjnKqCryevwjRdqrbzAIxdOn3P5wCz28MNb5Bgb2PwEdCezLEWg/132" width="30px"><span>KennyQ</span> 👍（6） 💬（1）<div>有几个问题：
1. 哪些进程会去使用tmpfs? 
2. 如何使用tmpfs，是在启动进程的时候把代码嵌入进去？还是说有接口可以调用？
3. tmpfs是怎么被挂载起来的？重启后是否会自动挂载？
4. tmpfs如果被100个进程调用了，会挂载100次么？
5. 启动tmpfs后是否会修改&#47;etc&#47;mtab?
6. tmpfs使用是否有最佳实践？
7. tmpfs是否可以在线扩缩容？</div>2020-09-06</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/64/9b/d1ab239e.jpg" width="30px"><span>J.Smile</span> 👍（2） 💬（1）<div>要点总结：
①tmpfs ,可以通过 df -h来看是不是 tmpfs 占用的内存较多
②tmpfs 作为一种特殊的 Shmem，它消耗的内存是不会体现在进程内存中的，这往往会给问题排查带来一些难度。
③可以通过 &#47;proc&#47;meminfo 找到哪种类型的内存开销比较大，来作为一种辅助手段，比如找到就是tempfs类型的内存，紧接着就可以分析tmpfs的内存占用情况。</div>2020-10-11</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/J3dqALgicfVklewMjVkpyLbTk9YiamnBf5QQZ3NPHGlMeVSdLDB5yHLicEZHKBbUets76KOFwbl9ju0xJw1VeGa1A/132" width="30px"><span>飞翔</span> 👍（1） 💬（3）<div>我这里有一个这样的问题，服务器集群每隔一段时间就有机器进入死机状态，可以ping通，但是ssh连不上， 这时候就得联系现场人员去重启机器，很麻烦。怀疑是内存耗尽的原因，但是重启机器后，从message日子又看不到证据，oom是不是不一定会释放内存？ 这种问题应该怎么定位呢？有什么解决方案呢？</div>2020-09-05</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/19/70/67/0c1359c2.jpg" width="30px"><span>qinsi</span> 👍（0） 💬（1）<div>看了下那个patch，为啥原始代码里要把负分给截断阿，是有什么特别的考虑吗</div>2020-09-09</li><br/><li><img src="" width="30px"><span>ray</span> 👍（0） 💬（1）<div>老师您好，
请问我们该怎么判断一个process会不会使用到tmpfs呢？

谢谢老师的解答^^</div>2020-09-06</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/5a/56/115c6433.jpg" width="30px"><span>jssfy</span> 👍（0） 💬（1）<div>这个patch很赞！请问老师这个mm oom的bug在centos 7下是否也有?</div>2020-09-05</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/47/b0/a9b77a1e.jpg" width="30px"><span>冬风向左吹</span> 👍（9） 💬（0）<div>&#47;PROC&#47;MEMINFO之谜：http:&#47;&#47;linuxperf.com&#47;?p=142</div>2020-09-05</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/9b/ba/333b59e5.jpg" width="30px"><span>Linuxer</span> 👍（2） 💬（0）<div>赞！意犹未尽，爽！</div>2020-09-05</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/28/84/76cfc35e.jpg" width="30px"><span>Sky</span> 👍（0） 💬（0）<div>请问一下，发现tmpfs过大后，是怎么再一步定位到是systemd 占用了tmpfs呢？</div>2024-09-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/97/a5/ba371e7f.jpg" width="30px"><span>nobody</span> 👍（0） 💬（0）<div>tmpfs 内存是不是也会被 swap out?</div>2024-07-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1a/83/09/42c48319.jpg" width="30px"><span>老酒馆</span> 👍（0） 💬（0）<div>精彩</div>2020-09-06</li><br/>
</ul>