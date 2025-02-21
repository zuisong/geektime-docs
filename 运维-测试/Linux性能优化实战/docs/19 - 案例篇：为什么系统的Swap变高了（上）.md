你好，我是倪朋飞。

上一节，我通过一个斐波那契数列的案例，带你学习了内存泄漏的分析。如果在程序中直接或间接地分配了动态内存，你一定要记得释放掉它们，否则就会导致内存泄漏，严重时甚至会耗尽系统内存。

不过，反过来讲，当发生了内存泄漏时，或者运行了大内存的应用程序，导致系统的内存资源紧张时，系统又会如何应对呢？

在内存基础篇我们已经学过，这其实会导致两种可能结果，内存回收和 OOM 杀死进程。

我们先来看后一个可能结果，内存资源紧张导致的 OOM（Out Of Memory），相对容易理解，指的是系统杀死占用大量内存的进程，释放这些内存，再分配给其他更需要的进程。

这一点我们前面详细讲过，这里就不再重复了。

接下来再看第一个可能的结果，内存回收，也就是系统释放掉可以回收的内存，比如我前面讲过的缓存和缓冲区，就属于可回收内存。它们在内存管理中，通常被叫做**文件页（**File-backed Page）。

大部分文件页，都可以直接回收，以后有需要时，再从磁盘重新读取就可以了。而那些被应用程序修改过，并且暂时还没写入磁盘的数据（也就是脏页），就得先写入磁盘，然后才能进行内存释放。

这些脏页，一般可以通过两种方式写入磁盘。

- 可以在应用程序中，通过系统调用 fsync ，把脏页同步到磁盘中；
- 也可以交给系统，由内核线程 pdflush 负责这些脏页的刷新。
<div><strong>精选留言（30）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/10/38/d7/d549bf3e.jpg" width="30px"><span>Ray</span> 👍（90） 💬（6）<div>关于上面有同学表示 hadoop 集群建议关 swap 提升性能。事实上不仅 hadoop，包括 ES 在内绝大部分 Java 的应用都建议关 swap，这个和 JVM 的 gc 有关，它在 gc 的时候会遍历所有用到的堆的内存，如果这部分内存是被 swap 出去了，遍历的时候就会有磁盘IO

可以参考这两篇文章：
https:&#47;&#47;www.elastic.co&#47;guide&#47;en&#47;elasticsearch&#47;reference&#47;current&#47;setup-configuration-memory.html

https:&#47;&#47;dzone.com&#47;articles&#47;just-say-no-swapping</div>2019-01-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/91/b4/d5d9e4fb.jpg" width="30px"><span>爱学习的小学生</span> 👍（69） 💬（2）<div>请问老师、为什么kubernetes要关闭swap呢？</div>2019-02-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/f8/70/f3a33a14.jpg" width="30px"><span>某、人</span> 👍（33） 💬（1）<div>swap应该是针对以前内存小的一种优化吧,不过现在内存没那么昂贵之后,所以就没那么大的必要开启了
numa感觉是对系统资源做的隔离分区,不过目前虚拟化和docker这么流行。而且node与node之间访问更耗时,针对大程序不一定启到了优化作用,针对小程序,也没有太大必要。所以numa也没必要开启。
不知道我的理解对否,老师</div>2019-01-02</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/d4RrUl4AJ3tdhsK76Kdcc9jQ2cvCzLsBfLYIiaRop7Ufj3byHrnvPS0O7sO935GG0fH8kicB67PklFdQJENZXNDQ/132" width="30px"><span>bob</span> 👍（18） 💬（4）<div>swappiness=0
Kernel version 3.5 and newer: disables swapiness.
Kernel version older than 3.5: avoids swapping processes out of physical memory for as long as possible.
如果linux内核是3.5及以后的，最好是设置swappiness=10，不要设置swappiness=0

以前整理的说明，供大家参考。</div>2019-01-03</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/1b/ca/9afb89a2.jpg" width="30px"><span>Days</span> 👍（13） 💬（1）<div>我们公司处理嵌入式系统都是关闭swap分区，具体不知道什么原因？</div>2019-01-02</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/J2FTWGBAoMDpKicgiaJ4b5AourOIQvlicJRu0iaDAJhlJkyRaialzuW9UUahN0CUQRuYLYciaN8Lu6u6ibYZrgj0XoXuQ/132" width="30px"><span>日行一善520</span> 👍（12） 💬（1）<div>看到评论有人问
hadoop集群服务器一般是建议关闭swap交换空间，这样可提高性能。在什么情况下开swap、什么情况下关swap？

为了性能关闭swap，这样就不会交换也不会慢了。内核里有个vm.xx的值可以调节swap和内存的比例，在使用内存90%时才交换到swap，可以设置这个来保持性能。在内存比较少的时候，还可以交换，就好了。

</div>2019-01-16</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/f2/e4/825ab8d9.jpg" width="30px"><span>刘政伟</span> 👍（11） 💬（1）<div>老师，在工作中经常会遇到这种情况，系统中的剩余内存较小、缓存内存较大的，也就是整体可用内存较高的情况下，就开始使用swap了，而查看swappiness的配置为10，理论上不应该使用swap的；具体看下面的free命令，麻烦老师看下是什么原因？
[root@shvsolman ~]# free -m
             total       used       free     shared    buffers     cached
Mem:         32107      31356        750          0         15      12514
-&#47;+ buffers&#47;cache:      18825      13281
Swap:         3071       1581       1490
[root@shvsolman ~]# sysctl -a | grep swappiness
vm.swappiness = 10</div>2019-03-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/64/05/6989dce6.jpg" width="30px"><span>我来也</span> 👍（7） 💬（1）<div>[D19打卡]
很遗憾,还未遇到过swap导致的性能问题.
刚买电脑时,512M内存要四百多,可是当时也不玩linux.
等工作了,用linux了,内存相对来说已经比较便宜了.
现在就更不用说了,基本小钱能解决的问题都不是问题了.
--------------------
以前的程序喜欢在启动时预分配很多内存,可是现在的几乎都是动态分配了.
以前一个程序动辄实际使用内存2-3G.
现在即使重构后,只需要100M内存,老板都不愿意换了.[稳定第一]</div>2019-01-02</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/16/31/ae8adf82.jpg" width="30px"><span>路过</span> 👍（6） 💬（3）<div>老师，前面你写只有当剩余内存落在页最小阈值和页低阈值中间，才开始回收内存。后面讲即使把 swappiness 设置为0，当剩余内存 + 文件页小于页高阈值时，还是会发生 Swap。我理解，这里是不是应该是：当剩余内存 + 文件页小于页低阈值时，还是会发生 Swap。谢谢！</div>2019-01-03</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/2d/24/28acca15.jpg" width="30px"><span>DJH</span> 👍（3） 💬（1）<div>倪老师，请教一下，Linux下怎么关闭SWAP功能？直接不分配SWAP卷（或者分区、文件），还是通过某个关闭SWAP功能的系统选项？</div>2019-01-02</li><br/><li><img src="https://wx.qlogo.cn/mmopen/vi_32/PiajxSqBRaEKQMM4m7NHuicr55aRiblTSEWIYe0QqbpyHweaoAbG7j2v7UUElqqeP3Ihrm3UfDPDRb1Hv8LvPwXqA/132" width="30px"><span>ninuxer</span> 👍（3） 💬（1）<div>打卡day20
我们机器上，都不启用swap😂</div>2019-01-02</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/ec/21/b0fe1bfd.jpg" width="30px"><span>Adam</span> 👍（2） 💬（1）<div>数据库应用一般都需要调整下numa。不然跨node访问内存性能就变差了。</div>2019-01-04</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/24/ca/932741cb.jpg" width="30px"><span>爆爱渣科_无良🌾 🐖</span> 👍（2） 💬（3）<div>感觉后面越写越变成讲述linux工具的文章。。。</div>2019-01-02</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/cb/0a/6a9e6602.jpg" width="30px"><span>React</span> 👍（2） 💬（1）<div>老师好，文中说电脑的休眠是基于swap.如果系统没有分配swap分区，还会将内存数据写入磁盘吗</div>2019-01-02</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/fd/63/c482d271.jpg" width="30px"><span>徳柏</span> 👍（1） 💬（1）<div>嵌入式系统一般都启用了zram技术，小内存swap还是要开启的，很有好处，跟swap到磁盘不是一个事</div>2019-07-17</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTJZicRP0FZ78kT68wEGeWzPnxrF4s3Ea36XdMA2pj2TAbU3eibVt7KqzS5B7LbWMhRfSc3XEUL3Hrjw/132" width="30px"><span>liubiqianmoney</span> 👍（1） 💬（1）<div>匿名页换出到磁盘之后，如果进程再次使用到，会被换入到内存中，这时候磁盘中的这个匿名页会从磁盘中释放掉吗？如果换出的匿名页一直没有被使用，从磁盘中释放的策略又怎样的呢？
</div>2019-01-29</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/2o1Izf2YyJSnnI0ErZ51pYRlnrmibqUTaia3tCU1PjMxuwyXSKOLUYiac2TQ5pd5gNGvS81fVqKWGvDsZLTM8zhWg/132" width="30px"><span>划时代</span> 👍（1） 💬（2）<div>最近碰到内存打满，瞬间导致系统负载和CPU使用率打满的情况。</div>2019-01-03</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/57/6e/b6795c44.jpg" width="30px"><span>夜空中最亮的星</span> 👍（1） 💬（1）<div>老师好，现在买的 云主机都不分配swap 空间，这样是有好处呢，还是想多卖内存？</div>2019-01-02</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/49/3d/4ac37cc2.jpg" width="30px"><span>外星人</span> 👍（0） 💬（1）<div>https:&#47;&#47;community.hortonworks.com&#47;questions&#47;71095&#47;why-not-set-swappiness-to-zero.html

这里哈，不过不确定是不是真的完全不会swap</div>2019-07-07</li><br/><li><img src="" width="30px"><span>Geek_6d9216</span> 👍（0） 💬（1）<div>为什么 
cat &#47;proc&#47;sys&#47;vm&#47;min_free_kbytes 
67584

而  cat &#47;proc&#47;zoneinfo
  pages free     33069
        min      8004
        low      10005
        high     12006
安照 文章说的 page_low = min_free_kbytes * 5&#47;4 , page_high = min_free_kbytes * 3&#47;2, 这个low和high 也不是正确的数据啊, 怎么理解这个 min_free_kbytes ?</div>2019-05-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/49/3d/4ac37cc2.jpg" width="30px"><span>外星人</span> 👍（0） 💬（1）<div>好像是新内核这个逻辑变了，设置成0就不会swap</div>2019-04-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/4e/0f/c43745e7.jpg" width="30px"><span>hola</span> 👍（0） 💬（1）<div>swap不是说在物理内存紧张不够的时候才会发生吗？
那么当物理内存不够的时候，使用swap会降低应用性能，但是这时候本身是内存很紧张的时候，不开岂不是有可能会导致oom呢
所以我还是不太明白为什么建议关掉swap</div>2019-03-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/0c/d2/381c75f5.jpg" width="30px"><span>道无涯</span> 👍（0） 💬（1）<div>老师你好，请问一下如果匿名页被swap到内存后。free查看到的used内存会减少么？还是也会算到已经使用的内存里，谢谢！</div>2019-03-16</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/ba/f9/351e4fc0.jpg" width="30px"><span>生活在别处</span> 👍（0） 💬（1）<div>请问分配给所有node的内存之外的内存,cpu是怎么访问的？</div>2019-01-09</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/xzHDjCSFicNY3MUMECtNz6sM8yDJhBoyGk5IRoOtUat6ZIkGzxjqEqwqKYWMD3GjehScKvMjicGOGDog5FF18oyg/132" width="30px"><span>李逍遥</span> 👍（0） 💬（2）<div>cat &#47;proc&#47;sys&#47;vm&#47;min_free_kbytes 
67584
Node 0, zone    DMA32
  pages free     656605
        min      12775
这两个值对不上啊</div>2019-01-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/31/d8/18a2de6d.jpg" width="30px"><span>朱林浩</span> 👍（0） 💬（1）<div>zone_reclaim_mode默认值不应该是1吗？</div>2019-01-07</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/b8/66/5fd18e55.jpg" width="30px"><span>李炀</span> 👍（0） 💬（1）<div>文章里的两张图片，上午看的时候还有，下午就看不到了，不管是手机上连接移动网络看，还是电脑上连接WIFI，都看不到。请老师确认一下。</div>2019-01-04</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/DYAIOgq83ernR4NKI5tejJAV3HMTF3gszBBUAjkjLO2QYic2gx5dMGelFv4LWibib7CUGexmMcMp5HiaaibmOH3dyHg/132" width="30px"><span>渡渡鸟_linux</span> 👍（0） 💬（1）<div># cat &#47;proc&#47;zoneinfo 中的值和free -m ，vm.min_free_kbytes 值怎么算都对不上，这是为啥？</div>2019-01-03</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/93/43/0e84492d.jpg" width="30px"><span>Maxwell</span> 👍（0） 💬（1）<div>当物理内存不足时，swap的值会升高吧，此时系统性能会受到很大影响吧，如响应时间，系统变慢？</div>2019-01-03</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/7a/e1/326f83b9.jpg" width="30px"><span>石头</span> 👍（13） 💬（0）<div>hadoop集群服务器一般是建议关闭swap交换空间，这样可提高性能。在什么情况下开swap、什么情况下关swap？</div>2019-01-02</li><br/>
</ul>