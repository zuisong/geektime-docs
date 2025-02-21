你好，我是邵亚方。

上一讲，我们主要讲了“什么是Page Cache”（What），“为什么需要Page Cache”（Why），我们这堂课还需要继续了解一下“How”：**也就是Page Cache是如何产生和释放的。**

在我看来，对Page Cache的“What-Why-How”都有所了解之后，你才会对它引发的问题，比如说Page Cache引起的load飙高问题或者应用程序的RT抖动问题更加了然于胸，从而防范于未然。

其实，Page Cache是如何产生和释放的，通俗一点的说就是它的“生”（分配）与“死”（释放），即Page Cache的生命周期，那么接下来，我们就先来看一下它是如何“诞生”的。

## Page Cache是如何“诞生”的？

Page Cache的产生有两种不同的方式：

- Buffered I/O（标准I/O）；
- Memory-Mapped I/O（存储映射I/O）。

这两种方式分别都是如何产生Page Cache的呢？来看下面这张图：

![](https://static001.geekbang.org/resource/image/4e/52/4eb820e15a5560dee4b847227ee75752.jpg?wh=3957%2A2600 "Page Cache产生方式示意图")

从图中你可以看到，虽然二者都能产生Page Cache，但是二者的还是有些差异的：

标准I/O是写的(write(2))用户缓冲区(Userpace Page对应的内存)，然后再将用户缓冲区里的数据拷贝到内核缓冲区(Pagecache Page对应的内存)；如果是读的(read(2))话则是先从内核缓冲区拷贝到用户缓冲区，再从用户缓冲区读数据，也就是buffer和文件内容不存在任何映射关系。
<div><strong>精选留言（29）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/1e/3b/d7/9d942870.jpg" width="30px"><span>邵亚方</span> 👍（68） 💬（1）<div>课后作业答案：
- 为什么第一次读写某个文件，Page Cache 是 Inactive 的？
第一次读取文件后，文件内容都是inactive的，只有再次读取这些内容后，才会把它放在active链表上，处于inactive链表上的pagecache在内存紧张是会首先被回收掉，有很多情况下文件内容往往只被读一次，比如日志文件，对于这类典型的one-off文件，它们占用的pagecache需要首先被回收掉；对于业务数据，往往都会读取多次，那么他们就会被放在active链表上，以此来达到保护的目的。

- 如何让它变成 Active 的呢？
第二次读取后，这些内容就会从inactive链表里给promote到active链表里，这也是评论区里有人提到的二次机会法。

- 在什么情况下 Active 的又会变成 Inactive 的呢？
在内存紧张时，会进行内存回收，回收会把inactive list的部分page给回收掉，为了维持inactive&#47;active的平衡，就需要把active list的部分page给demote到inactive list上，demote的原则也是lru。

- 系统中有哪些控制项可以影响 Inactive 与 Active Page Cache 的大小或者二者的比例？
min_free_kbytes会影响整体的pagecache大小;vfs_cache_pressure会影响在回收时回收pagecache和slab的比例; 在开启了swap的情况下，swappiness也会影响pagecache的大小；zone_reclaim_mode会影响node的pagecache大小；extfrag_threshold会影响pagecache的碎片情况。

- 对于匿名页而言，当产生一个匿名页后它会首先放在 Active 链表上，请问为什么会这样子？这是合理的吗？
这是不合理的，内核社区目前在做这一块的改进。具体可以参考https:&#47;&#47;lwn.net&#47;Articles&#47;816771&#47;。


</div>2020-10-11</li><br/><li><img src="" width="30px"><span>zwb</span> 👍（21） 💬（3）<div>第二次机会法，避免大量只读一次的文件涌入 active，在需要回收时又从 active 移动到 inactive lru 链表。场景比如编译内核。</div>2020-08-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/65/cf/326c0eea.jpg" width="30px"><span>x-ray</span> 👍（11） 💬（3）<div>读这个确实需要对一些linux基础概念有一个了解。前几天刚读的时候，我连VFS都没有一个概念，读起来非常吃力，到第二章就看得云里雾里。这两天找了点视频把一些基础概念熟悉了下，今天再来看的时候，就感觉比较容易理解了。不过我有一个疑问，既然mmap映射的效率更高，为什么不都用这个呢？是因为标准IO无法像文件那样提前加载一块内存到PageCache吗？</div>2020-09-15</li><br/><li><img src="" width="30px"><span>Geek_162e2a</span> 👍（10） 💬（2）<div>应用开发者的视角
第一次读写文件，PageCache是inactive的，为什么要这样设计？可能内核底层是采用类似LRU链表的设计来管理PageCache, 如果单纯照搬LRU链表的设计的话，当读大文件的时候会将原本属于热点缓存的PageCache冲刷出去，导致性能波动，因此需要对PageCache进行分类，来避免这个问题，即新读入的文件先进入inactive区域</div>2020-08-27</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/DYAIOgq83epUBQibdMCca340MFZOe5I1GwZ0PosPIzA0TPCNzibgH00w45Zmv4jmL0mFRHMUM9FuKiclKOCBjSmsw/132" width="30px"><span>Geek_circle</span> 👍（9） 💬（1）<div>Memory-Mapped I&#47;O（存储映射 I&#47;O）
 是否就是零拷贝的概念呢？</div>2020-08-25</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/2b/09/2171f9a3.jpg" width="30px"><span>小白哥哥</span> 👍（7） 💬（6）<div>不认同邵老师对于pagecache产生原因的描述，应用程序调用了write，内核会根据fd当前的fpos计算出写文件操作的文件偏移，然后根据偏移去inode-&gt;mapping中找出对应的pagecache页，如果没有的话，分配一页，插入inode-&gt;mapping，然后把write调用中的buffer拷贝到pagecache中，这个过程并不会触发page fault。如果是mmap映射文件，然后直接对内存读写，才会触发page fault，进而驱动内核加载文件内容到对应的page cache中。</div>2021-05-13</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTJpJXWFP3dNle88WnTkRTsEQkPJmOhepibiaTfhEtMRrbdg5EAWm4EzurA61oKxvCK2ZjMmy1QvmChw/132" width="30px"><span>唐江</span> 👍（3） 💬（1）<div>什么地方讲了inactive 、active 是个数据结构链表啊！不是一个简单的数字吗</div>2021-05-20</li><br/><li><img src="" width="30px"><span>Geek_162e2a</span> 👍（3） 💬（1）<div>如何让它变成Active的呢？多读几次文件，达到系统设计的值后，此文件的PageCache会变成热点数据进入Active区域。
在什么情况Active会变成inactive的呢？热点文件太多，且此文件最近没有被读取过，自然就被挤出去了，静态资源服务器，可能会比较经常出现这种情况</div>2020-08-27</li><br/><li><img src="" width="30px"><span>地下城勇士</span> 👍（3） 💬（2）<div>老师的图是用什么工具画的？感觉以后可以尝试一下</div>2020-08-25</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/19/c4/35/2cc10d43.jpg" width="30px"><span>Wade_阿伟</span> 👍（1） 💬（1）<div>老师您好，看了上面老师的讲述，对存储映射I&#47;O和标准I&#47;O有了一定的理解。但是系统一般什么时候使用存储映射I&#47;O，什么时候使用标准I&#47;O呢？</div>2021-07-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/57/4f/6fb51ff1.jpg" width="30px"><span>奕</span> 👍（1） 💬（1）<div>当第一次写某个文件时，产生的 Page Cache 是 inactive 的，那么在什么事件触发的时候，才会转为 active 的？ </div>2020-08-30</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/e2/ff/ca3dec06.jpg" width="30px"><span>狗蛋</span> 👍（1） 💬（1）<div>这跟mysql策略一样啊，也许是mysql借鉴Linux的</div>2020-08-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/df/6c/5af32271.jpg" width="30px"><span>Dylan</span> 👍（0） 💬（2）<div>既然是Cache，那也会存在脏数据丢失的可能，那避免数据丢失的方法是不是和数据库的一些策略类似，比如WAL</div>2020-10-05</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/6e/05/d47cee18.jpg" width="30px"><span>wong ka seng</span> 👍（0） 💬（1）<div>老师好，本人对bash认识不多，有没有补充的资料呢？</div>2020-09-03</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/33/32/8f304f6c.jpg" width="30px"><span>--SNIPER</span> 👍（1） 💬（3）<div>测试了下都是0，能帮忙解释下为什么吗
10:39:31 AM  pgpgin&#47;s pgpgout&#47;s   fault&#47;s  majflt&#47;s  pgfree&#47;s pgscank&#47;s pgscand&#47;s pgsteal&#47;s    %vmeff
10:39:32 AM      0.00      8.00   1509.00      0.00   3651.00      0.00      0.00      0.00      0.00
10:39:33 AM      0.00      0.00   1566.00      0.00   3633.00      0.00      0.00      0.00      0.00
10:39:34 AM      0.00     12.00   1920.00      0.00   3815.00      0.00      0.00      0.00      0.00
10:39:35 AM      0.00      4.00   7944.00      0.00   6108.00      0.00      0.00      0.00      0.00
10:39:36 AM      0.00      0.00    993.00      0.00   3638.00      0.00      0.00      0.00      0.00
10:39:37 AM      0.00      0.00   1171.00      0.00   3616.00      0.00      0.00      0.00      0.00
10:39:38 AM      0.00      0.00    944.00      0.00   3756.00      0.00      0.00      0.00      0.00
10:39:39 AM      0.00     76.00  13438.00      0.00   6632.00      0.00      0.00      0.00      0.00
10:39:40 AM      0.00      0.00   7963.00      0.00   5471.00      0.00      0.00      0.00      0.00
^C

10:39:41 AM      0.00      4.76   1592.86      0.00   4565.48      0.00      0.00      0.00      0.00
Average:         0.00     10.57   3941.67      0.00   4487.30      0.00      0.00      0.00      0.00</div>2020-12-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1d/12/13/e103a6e3.jpg" width="30px"><span>扩散性百万咸面包</span> 👍（1） 💬（1）<div>不是很理解为什么要有alloc page，不是已经有了userspace page了吗？</div>2020-08-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/4a/15/106eaaa8.jpg" width="30px"><span>stackWarn</span> 👍（1） 💬（1）<div> &#47;proc&#47;sys&#47;vm&#47;pagecache_limit_mb 限制使用大小</div>2020-08-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/17/37/a0/032d0828.jpg" width="30px"><span>上杉夏香</span> 👍（0） 💬（0）<div>关于课后作业，不清楚 MySQL 的 Buffer Pool 和 操作系统的 Page Cache 谁先谁后。不过他们考虑的都是，作为缓存，想最大次数的被命中。第一次读文件为 Inactive，和 MySQL 查询时，将首次命中的记录 Page 放入 yound 区，都是为了避免新的、可能并不怎么被访问的缓存将之前频繁访问的缓存淘汰出去。</div>2023-04-04</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/0c/30/d4737cd5.jpg" width="30px"><span>lyonger</span> 👍（0） 💬（0）<div>这一节课把buffer算到了user space ，上一节课又算到了page cache ，而page cache属于kernel space。 有点不懂？</div>2022-12-23</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTJJ7Ft8jtL1CySd4jeZ32kSNvTcHV12s0zN47WmVr6N8GTtbt0rlfyRzFqlOIjjtdFrmoSNu49IiaQ/132" width="30px"><span>Geek_66675e</span> 👍（0） 💬（0）<div>生产环境很多没有开启swap。如果没有开启swap，那pagecache是由哪个内核线程回收呢？还是不会回收</div>2022-12-16</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/29/b1/10/061bc360.jpg" width="30px"><span>悦动音巧</span> 👍（0） 💬（0）<div>老师，咨询下我的内存都被buffer&#47;cache占用了，执行echo 3释放后，几分钟又被占满了，sar查看都是0
[root@test ~]# free   -g
              total        used        free      shared  buff&#47;cache   available
Mem:             63           1           0           2          61          57
Swap:             7           3           4

[root@test ~]# sar -B 1
Linux 3.10.0-514.el7.x86_64 (CRS-DB)    2022年11月11日  _x86_64_        (12 CPU)

17时42分01秒  pgpgin&#47;s pgpgout&#47;s   fault&#47;s  majflt&#47;s  pgfree&#47;s pgscank&#47;s pgscand&#47;s pgsteal&#47;s    %vmeff
17时42分02秒      0.00     32.00     57.00      0.00     79.00      0.00      0.00      0.00      0.00
17时42分03秒      0.00     12.00     42.00      0.00     67.00      0.00      0.00      0.00      0.00
17时42分04秒      0.00      0.00     32.00      0.00     51.00      0.00      0.00      0.00      0.00
17时42分05秒      0.00     32.00     23.00      0.00     40.00      0.00      0.00      0.00      0.00
17时42分06秒      0.00      0.00     38.00      0.00     62.00      0.00      0.00      0.00      0.00
17时42分07秒      0.00      0.00     23.00      0.00     40.00      0.00      0.00      0.00      0.00</div>2022-11-11</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/bibTL8t812ehcBB0cPYqsDycLq37iaXmbzdGwAibkSe4G9r0lDoYxibvnLEhkWNWicPbe70j926FbyibKGPIEMh7ib78Q/132" width="30px"><span>Geek_356c0d</span> 👍（0） 💬（1）<div>我对内存申请那张图有疑问，申请内存的时候如果内存不够，这时触发了kswapd内核线程去后台清理内存，这时不需要同步等待它清理完吗？按照图片得意思，是唤醒了kswapd之后就立刻走向下一步了</div>2022-03-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/19/bb/7e/4e86c5a5.jpg" width="30px"><span>Aizen</span> 👍（0） 💬（1）<div>Page Cache 我问个问题？容器内的Page Cache的回收策略是基于 真是物理机的内核分配不足才回收？还是容器本身的内存不足策略？</div>2022-01-17</li><br/><li><img src="" width="30px"><span>Geek_b8749d</span> 👍（0） 💬（0）<div>老师讲的太好了，以前觉的pagecache很神秘，经过老师讲解，有种豁然开朗的感觉</div>2021-01-24</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/foNlomhnJgM1e7DJZzjXhrrndVEubz273WVYfkcfZ3WMyGAA5jkJDmDD6WoWjvZxzic1BggdWXpaTia213q5LdSQ/132" width="30px"><span>LemonTree</span> 👍（0） 💬（1）<div>老师，本课中第一个脚本，我在x86平台和arm平台都运行了一次，如老师所说两个平台的page cache都会增加， 然而，在x86平台上主要增加的是和本文所说的一样是Inactive(anon)， 而在arm平台增加的却是Active(file): ，请问老师问这种差异可能是由什么导致的？ 是否是某些系统参数可以控制？感觉根据上一讲的内容他不应该跟平台相关啊。希望老师抽空解答，谢谢。 </div>2021-01-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/20/08/bc06bc69.jpg" width="30px"><span>Dovelol</span> 👍（0） 💬（2）<div>老师好，想问下对于标准io，那一份数据是不是在内存里面其实有2份？用户空间内存一份，pagecache一份。用户空间的那一份在开始写入的时候会有缺页中断吗？我看老师讲的是在copy到pagecache的时候会有缺页中断。还有就是用户空间的内存什么时候回收掉呢和pagecache有关系吗？</div>2020-12-02</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/a9/84/c87b51ce.jpg" width="30px"><span>xiaobang</span> 👍（0） 💬（0）<div>把脏页比作小朋友，也是够惊天动地了，还得拉孙悟空过来救下场。另外孙悟空那段音频里面漏掉了...</div>2020-09-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/f9/1a/d289c2ac.jpg" width="30px"><span>大飞哥</span> 👍（0） 💬（2）<div>Dirty数据在内存中驻留的时间超过一个特定的阈值时会回写，并且page cache中的页面有对应的文件和在文件中的位置信息，需要换入恢复的时候也更加容易，所以内核通常更倾向于换出page cache中的页面，只有当内存压力变得相对严重时，才会选择回收 anonymous pages，处理就是文件页会首先放在 Inactive 链表上，还有这也可以为了避免大量只访问一次的文件页涌入活跃LRU链表带来查找的复杂度。所以我觉得这是合理的。</div>2020-08-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1e/f5/95/a362f01b.jpg" width="30px"><span>Geek1560</span> 👍（0） 💬（3）<div>老师好，Linux的Page Cache，在IO负载较高的业务场景下，近似贪婪使用，除非后续内存不足时，才会内存回收来释放。其实有些文件在使用后，不会有后续的IO操作(比如日志文件)，但是Linux还是将其保留在cache中。虽然可以通过posix_fadvise来释放。但是感觉Linux这块管理的不够精细。而且，大量使用page cahe，如果开启swap，非常容易swap，没有就OOM。老师这块有经验或者一些其他思路吗？</div>2020-08-18</li><br/>
</ul>