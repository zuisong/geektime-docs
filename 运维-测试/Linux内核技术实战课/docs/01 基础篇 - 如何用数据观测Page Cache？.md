你好，我是邵亚方。今天我想和你聊一聊Page Cache的话题。

Page Cache你应该不陌生了，如果你是一名应用开发者或者Linux运维人员，那么在工作中，你可能遇见过与Page Cache有关的场景，比如：

- 服务器的load飙高；
- 服务器的I/O吞吐飙高；
- 业务响应时延出现大的毛刺；
- 业务平均访问时延明显增加。

这些问题，很可能是由于Page Cache管理不到位引起的，因为Page Cache管理不当除了会增加系统I/O吞吐外，还会引起业务性能抖动，我在生产环境上处理过很多这类问题。

据我观察，这类问题出现后，业务开发人员以及运维人员往往会束手无策，究其原因在于他们对Page Cache的理解仅仅停留在概念上，并不清楚Page Cache如何和应用、系统关联起来，对它引发的问题自然会束手无策了。所以，要想不再踩Page Cache的坑，你必须对它有个清晰的认识。

那么在我看来，认识Page Cache最简单的方式，就是用数据说话，通过具体的数据你会更加深入地理解Page Cache的本质。为了帮你消化和理解，我会用两节课的时间，用数据剖析什么是Page Cache，为什么需要Page Cache，Page Cache的产生和回收是什么样的。这样一来，你会从本质到表象，透彻理解它，深切感受它和你的应用程序之间的关系，从而能更好地理解上面提到的四个问题。
<div><strong>精选留言（30）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/14/34/df/64e3d533.jpg" width="30px"><span>leslie</span> 👍（31） 💬（2）<div>Coding能力有限：不过学过倪鹏飞老师的课，侧重点应当不同吧；PageCache大小的合理设置不知道为何老师不曾提及？单独的去谈代码似乎忘了底层硬件吧。我们说性能是基于硬件去提问，老师单独的去问而不提及硬件基础是否、、、这就像我们去说怎么样去设置软件更合理，不去提及我们硬件的主频和大小以及、、、</div>2020-08-31</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/20/08/bc06bc69.jpg" width="30px"><span>Dovelol</span> 👍（23） 💬（6）<div>老师好，能详细讲一下buffer cache和page cache的区别吗？这两个到底作用在哪的。</div>2020-08-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/9a/83/0802f4e7.jpg" width="30px"><span>Geek_lucky_brian</span> 👍（22） 💬（5）<div>感觉学习到了很多。请教老师一个问题，如果不做sync而是直接去drop cache，drop期间是不是也会把脏页刷盘呢？如果是的话，那么为什么还要单独做一次sync呢？直接drop cache不就好了吗</div>2020-08-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/0f/70/cdef7a3d.jpg" width="30px"><span>Joe Black</span> 👍（16） 💬（1）<div>我们的数据处理算法实际上对超大输入文件是从头到尾读一遍，而且整个程序仅读一遍，这样其实用direct io就行了吧？</div>2020-08-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/57/4f/6fb51ff1.jpg" width="30px"><span>奕</span> 👍（8） 💬（5）<div>所以 Page Cache 就是 磁盘的一个缓存区？</div>2020-08-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1b/96/47/93838ff7.jpg" width="30px"><span>青鸟飞鱼</span> 👍（7） 💬（1）<div>老师，你好，在有些地方看到经过PageCache的Io叫缓存IO，有些地方说是直接IO。不知道缓存IO，直接IO有什么区别吗</div>2020-09-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/18/ac/4d68ba46.jpg" width="30px"><span>金时</span> 👍（5） 💬（2）<div>mmap 产生的pageCache 也是内核态的吗</div>2021-06-21</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/4Lprf2mIWpJOPibgibbFCicMtp5bpIibyLFOnyOhnBGbusrLZC0frG0FGWqdcdCkcKunKxqiaOHvXbCFE7zKJ8TmvIA/132" width="30px"><span>Geek_c2089d</span> 👍（4） 💬（4）<div>Swap 过程产生的 I&#47;O 会很容易引起性能抖动不太明白是什么意思？</div>2020-10-15</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1a/e3/cc/0947ff0b.jpg" width="30px"><span>nestle</span> 👍（4） 💬（2）<div>老是，第一张图有个地方没太明白，Page Cache是由VFS模块来管理的吗？回写、预读这些操作都是由VFS控制的吗？还是说VFS只负责普通文件I&#47;O呢？</div>2020-08-30</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/aa/9a/92d2df36.jpg" width="30px"><span>tianfeiyu</span> 👍（3） 💬（1）<div>老师，想问一下，如果没有开启 Swap 分区，Inactive(anon)+Active(anon) 既然不会在 page cache，那就只会存在内存中吗</div>2021-07-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/09/fc/6f53d426.jpg" width="30px"><span>nuo-promise</span> 👍（3） 💬（1）<div>老师,  mac 上可以推荐 读linux  kernel 的 ide 和 推荐 kernel 源码的版本么？跟着你的教程,然后 课后 源码文件看起来 效果还是不错的
</div>2020-09-01</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1f/6e/78/e7045b49.jpg" width="30px"><span>BlingBling</span> 👍（2） 💬（2）<div>请教一下，sync &amp;&amp; echo 3 &gt; &#47;proc&#47;sys&#47;vm&#47;drop_caches命令是否并不能保证一定能将cache清除？
我在一台嵌入式设备上，
1. 多次执行cat命令读取dd创建的文件，耗时无差，并且&#47;proc&#47;memeinfo里面cached的大小也基本不变，
2. 执行sync &amp;&amp; echo 3 &gt; &#47;proc&#47;sys&#47;vm&#47;drop_caches命令后，立即查看&#47;proc&#47;memeinfo里面cached的大小，也和命令执行前基本一致？
请教下老是这是什么原因？</div>2020-10-12</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/K2DPibcnicQFUOxEGrnHysfvAqK8uyXCR3vqsas3xNwqvIMVuGoWRIV37Kiaia3vUlPkMRD5mDWh1OPaOBTEs86zbA/132" width="30px"><span>轩轩</span> 👍（1） 💬（1）<div>你好，“你可以发现 buff&#47;cache 包括下面这几项：
buff&#47;cache = Buffers + Cached + SReclaimable”
请问buffers统计里面的确是不包括SReclaimable这个的？</div>2021-05-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1f/6e/78/e7045b49.jpg" width="30px"><span>BlingBling</span> 👍（1） 💬（1）<div>老师你好，请教一下，我这边在项目的嵌入式设备上，发现
Buffers + Cached + SwapCached = Active(file) + Inactive(file) + Shmem + SwapCached
两者并不相等， Active(file) + Inactive(file) 的和远大于Buffers + Cached，请问下这是什么原因呢？或者什么原因可能导致这个现象？

另外，这个设备上执行free命令，看到的也只能看到buffers，看不到cached，这又是为什么呢？</div>2020-10-12</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/HFTNSboUOlebZEG3sFa4ewCWkyYyTFGhQhDYT4lQ1XgLBGG6JozjibygicofEG2fJBH5zru4ckA4ryOnrRKIKOvQ/132" width="30px"><span>下大雨没伞那就跑</span> 👍（1） 💬（2）<div>暂时闲置的进程所占用的内存会被移出内存以供其它内存需求量大的进程使用，在需要运行此进程时再加载进内存，此过程中文件相关的内存处理是由VFS管理的，而匿名内存是被交换进swap分区的（属于硬盘），本来就是为了清空内存供其它进程使用那为何还要浪费内存对这部分已经交换到swap分区的内容再次在内存中建立swapcache呢?! 说是为了减少io交互不是有点本末倒置了吗？不知道理解的对不对，求作者大师指点迷津，多谢！</div>2020-08-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/63/85/1dc41622.jpg" width="30px"><span>姑射仙人</span> 👍（0） 💬（1）<div>老师，我看文章说要为ES保留足够的filesystem cache，这个和Page Cache是一回事吗？</div>2021-03-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/09/fc/6f53d426.jpg" width="30px"><span>nuo-promise</span> 👍（0） 💬（2）<div>老师 可以推荐一下 你开发kernel mac 要部署的环境 教程吗？</div>2020-09-02</li><br/><li><img src="https://wx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTIt0nAFvqib3fpf9AIKUrEJMdbiaPjnKqCryevwjRdqrbzAIxdOn3P5wCz28MNb5Bgb2PwEdCezLEWg/132" width="30px"><span>KennyQ</span> 👍（0） 💬（1）<div>等式两边之和都是 112696 KB，这个值buffer+cache，没算上swapcache
Buffers:            1224 kB
Cached:           111472 kB
SwapCached:        36364 kB</div>2020-08-26</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/HFTNSboUOlebZEG3sFa4ewCWkyYyTFGhQhDYT4lQ1XgLBGG6JozjibygicofEG2fJBH5zru4ckA4ryOnrRKIKOvQ/132" width="30px"><span>下大雨没伞那就跑</span> 👍（0） 💬（1）<div>原来像cache一类的并不是缓存全部，只是缓存一部分使用到的而已，所以建立swapcache明白了</div>2020-08-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/64/9b/d1ab239e.jpg" width="30px"><span>J.Smile</span> 👍（0） 💬（1）<div>老师，我们是java工程师，不懂Linux编程，您应该指的是C语言编程吧</div>2020-08-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/fb/7f/746a6f5e.jpg" width="30px"><span>Q</span> 👍（9） 💬（1）<div>”从这个公式中，你能看到 free 命令中的 buff&#47;cache 是由 Buffers、Cached 和 SReclaimable 这三项组成的，它强调的是内存的可回收性，也就是说，可以被回收的内存会统计在这一项“ -- 读到这句话，感觉豁然开朗，我们知道Linux是尽可能把空闲内存作为IO的缓存来使用，提升文件读写的效率，但是这些内存是可以按实际需求会进行回收的。果然，跟大佬学习能减少自己理解的难度。</div>2020-08-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/f9/1a/d289c2ac.jpg" width="30px"><span>大飞哥</span> 👍（7） 💬（0）<div>很棒，让我们比较系统的了解了Page Cache，要观测PageCache就直接读写文件就能感受得到了，特别是大文件，可以与O_DIRECT一起对比。如果调试过程发现IO这一块确实容易出问题的话，可以使用 mount -o commit 降低文件系统同步时间可以更快复现及查找问题。</div>2020-08-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/64/9b/d1ab239e.jpg" width="30px"><span>J.Smile</span> 👍（5） 💬（0）<div>老师讲的不错，深入浅出！
总结：
PageCache的计算：
Buffers + Cached + SwapCached = Active(file) + Inactive(file) + Shmem + SwapCached
①SwapCached 是在打开了 Swap 分区后，把 Inactive(anon)+Active(anon) 这两项里的匿名页给交换到磁盘（swap out），然后再读入到内存（swap in）后分配的内存。由于读入到内存后原来的 Swap File 还在，所以 SwapCached 也可以认为是 File-backed page，即属于 Page Cache。
②SwapCached 只在 Swap 分区打开的情况下才会有，而我建议你在生产环境中关闭 Swap 分区，因为 Swap 过程产生的 I&#47;O 会很容易引起性能抖动，所以一般在禁止swap的情况下忽略SwapCached。那free命令中的buffer&#47;cache就是pageCache。</div>2020-08-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/20/08/bc06bc69.jpg" width="30px"><span>Dovelol</span> 👍（3） 💬（2）<div>老师好，想问下你知道rocketmq消息中间件，作者用了一个堆外内存，手动commit一页4k数据来优化写pagecache，为什么是优化呢，也就是少量的写pagecache和每次写一页pagecache有啥区别呢？</div>2020-12-02</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/9c/84/30906d5f.jpg" width="30px"><span>Rony</span> 👍（3） 💬（4）<div>请问下flush和fsync操作的区别，以及那个操作是针对page cache的呢？</div>2020-08-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/3a/82/1ff83a38.jpg" width="30px"><span>牛牛</span> 👍（1） 💬（0）<div>笔记、备忘 ~~~~

buffer&#47;cache = kb_main_buffers + kb_main_cached = kb_main_buffers + (kb_page_cache + kb_slab_reclaimable) = Buffers + (Cached + SReclaimable)

SReclaimable: 是指可以被回收的内核内存

Buffers + Cached + SwapCached = Active(file) + Inactive(file) + Shmem + SwapCached

buffer可以理解为是一类特殊文件的cache，这类特殊文件就是设备文件
cache 则是普通文件的缓存

swapCached只有在打开swap的情况下才有、而实际建议关闭swap、此时的 pageCache = Buffer + cache

</div>2020-09-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/1a/9c/082cf625.jpg" width="30px"><span>权</span> 👍（1） 💬（0）<div>第一张图很赞，一图胜千言</div>2020-08-18</li><br/><li><img src="" width="30px"><span>Geek_5816b7</span> 👍（0） 💬（0）<div>我想问一下咱们是根据linux内核哪一个版本讲的？</div>2024-08-18</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTJYiapdUmNoyStNORuFktoqiciaMOelBia7lJB5OOIl8vFdX6Kuj3MuoybFFPQfAvtkzTdrZCIT5UicibsA/132" width="30px"><span>Geek_06e79f</span> 👍（0） 💬（0）<div>讲的不够呀， 感觉没有做到释义解惑</div>2023-09-28</li><br/><li><img src="" width="30px"><span>Geek_292048</span> 👍（0） 💬（0）<div>老师，可以介绍哈里面谈到的概念吗，page cache 能swap划等号吗</div>2022-12-05</li><br/>
</ul>