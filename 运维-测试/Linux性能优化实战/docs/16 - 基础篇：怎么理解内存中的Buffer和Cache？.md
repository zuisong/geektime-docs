你好，我是倪朋飞。

上一节，我们梳理了 Linux 内存管理的基本原理，并学会了用 free 和 top 等工具，来查看系统和进程的内存使用情况。

内存和 CPU 的关系非常紧密，而内存管理本身也是很复杂的机制，所以感觉知识很硬核、很难啃，都是正常的。但还是那句话，初学时不用非得理解所有内容，继续往后学，多理解相关的概念并配合一定的实践之后，再回头复习往往会容易不少。当然，基本功不容放弃。

在今天的内容开始之前，我们先来回顾一下系统的内存使用情况，比如下面这个 free 输出界面：

```
# 注意不同版本的free输出可能会有所不同
$ free
              total        used        free      shared  buff/cache   available
Mem:        8169348      263524     6875352         668     1030472     7611064
Swap:             0           0           0
```

显然，这个界面包含了物理内存Mem和交换分区Swap的具体使用情况，比如总内存、已用内存、缓存、可用内存等。其中缓存是 Buffer和Cache两部分的总和 。

这里的大部分指标都比较容易理解，但 Buffer和 Cache可能不太好区分。从字面上来说，Buffer是缓冲区，而Cache是缓存，两者都是数据在内存中的临时存储。那么，你知道这两种“临时存储”有什么区别吗？

注：今天内容接下来的部分，Buffer和Cache我会都用英文来表示，避免跟文中的“缓存”一词混淆。而文中的“缓存”，则通指内存中的临时存储。

## free数据的来源
<div><strong>精选留言（30）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/0f/47/42/5b55bd1a.jpg" width="30px"><span>倪朋飞</span> 👍（449） 💬（19）<div>关于磁盘和文件的区别，本来以为大家都懂了，所以没有细讲。磁盘是一个块设备，可以划分为不同的分区；在分区之上再创建文件系统，挂载到某个目录，之后才可以在这个目录中读写文件。

其实 Linux 中“一切皆文件”，而文章中提到的“文件”是普通文件，磁盘是块设备文件，这些大家可以执行 &quot;ls -l &lt;路径&gt;&quot; 查看它们的区别（输出的含义如果不懂请 man ls 查询）。

在读写普通文件时，会经过文件系统，由文件系统负责与磁盘交互；而读写磁盘或者分区时，就会跳过文件系统，也就是所谓的“裸I&#47;O“。这两种读写方式所使用的缓存是不同的，也就是文中所讲的 Cache 和 Buffer 区别。

关于文件系统、磁盘以及 I&#47;O 的原理，大家不要着急，后面 I&#47;O 模块还会讲的。</div>2018-12-26</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTIbas4S4X5W15njMeoEPPSyBZRX37nrTXbMFFeHghXl4Slk6WXE7oq5yxoNnukYfcOQs00RAvUmEA/132" width="30px"><span>Geek_5258f8</span> 👍（241） 💬（11）<div>理论上，一个文件读首先到Block Buffer, 然后到Page Cache。有了文件系统才有了Page Cache.
在老的Linux上这两个Cache是分开的。那这样对于文件数据，会被Cache两次。这种方案虽然简单，
但低效。后期Linux把这两个Cache统一了。对于文件，Page Cache指向Block Buffer，对于非文件
则是Block Buffer。这样就如文件实验的结果，文件操作，只影响Page Cache，Raw操作，则只影响Buffer. 比如一此VM虚拟机，则会越过File System，只接操作 Disk, 常说的Direct IO.</div>2018-12-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/eb/1e/cbd63297.jpg" width="30px"><span>croco</span> 👍（59） 💬（2）<div>我好像明白了，就是&#47;proc&#47;&lt;pid&gt;&#47;smaps中的Pss相加，因为Pss是私有内存+共享内存按比例属于自己计算的那一部分
比如私有内存是200k， 共享内存500k和4个其它进程共享，那么是Pss就是200k+（500&#47;（1+4））=200k+100k=300k。 这样所有进程的Pss相加就不会有重复相加的顾虑，因为Pss中已经将共享内存部分帮我们算好了
参考命令：awk &#39;&#47;Pss:&#47;{ sum += $2 } END { print sum }&#39; &#47;proc&#47;$$&#47;smaps</div>2019-06-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/0d/a7/30e27d12.jpg" width="30px"><span>acm1204</span> 👍（30） 💬（1）<div>socket buffer属于哪一类？</div>2019-04-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/de/d4/b83c4185.jpg" width="30px"><span>David.cui</span> 👍（21） 💬（2）<div>数据库使用裸设备是明显的磁盘读写；如果数据库的数据文件在文件系统上就是文件读写。这样理解对么</div>2018-12-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/22/9a/989a3d8e.jpg" width="30px"><span>JJ</span> 👍（18） 💬（2）<div>还是有点困惑，感觉读写磁盘上的数据不就是读写磁盘上的文件里的数据嘛，难道读磁盘上的数据可以不经过文件系统吗，可以直接读裸磁盘？有点没理解buffer是磁盘上的数据缓存，cache是文件数据缓存，求大神解答下。。</div>2018-12-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/f8/70/f3a33a14.jpg" width="30px"><span>某、人</span> 👍（14） 💬（1）<div>老师,是否绕开文件系统,直接对磁盘进行读写会更快呢？</div>2018-12-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/b8/36/542c96bf.jpg" width="30px"><span>Mr.Strive.Z.H.L</span> 👍（13） 💬（3）<div>老师您好，有一个疑惑：
数据写入到page cache。后续应用程序强制刷盘或者系统自动刷盘的时候，page cache中的数据还会经过buffer，然后再到块设备吗？还是不会经过buffer，直接刷到块设备了？
（读取比较好理解，读取文件直接到page cache，读取块设备先到buffer，buffer不够再到page cache）</div>2019-01-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/a9/3b/f4ca20d8.jpg" width="30px"><span>吴林辉</span> 👍（10） 💬（3）<div>“因为 Linux 中块的大小是 1KB，所以这个单位也就等价于 KB&#47;s。”关于这一点，想请问下老师，linux block的大小不是4KB呢？</div>2019-02-18</li><br/><li><img src="" width="30px"><span>无名老卒</span> 👍（8） 💬（3）<div>看了这篇文章，终于理解 了buffers以及cache，之前在网上还专门查过这2者的区别，但就是像老师说的那样，文章看下来，啥也没有啥明白。

按照老师的总结，cache是针对文件系统的缓存 ，而buffers是对磁盘数据的缓存，是直接跟硬件那一层相关的，那一般来说，cache会比buffers的数量大了很多。生产环境下面看了多台机器，的确如此。

后面留的那个作业，如果要统计一个进程所占用的物理空间，我的做法是累加RSS的值。如下shell是我工作中所使用的命令，取内存占用top10的进程：

for i in $( ls &#47;proc&#47; |grep &quot;^[0-9]&quot;|awk &#39;$0 &gt;100&#39;) ;do cmd=&quot;&quot;;[ -f &#47;proc&#47;$i&#47;cmdline ] &amp;&amp; cmd=`cat &#47;proc&#47;$i&#47;cmdline`;[ &quot;$cmd&quot;X = &quot;&quot;X ] &amp;&amp; cmd=$i;awk -v i=&quot;$cmd&quot; &#39;&#47;Rss:&#47;{a=a+$2}END{printf(&quot;%s:%d\n&quot;,i,a)}&#39; &#47;proc&#47;$i&#47;smaps 2&gt;&#47;dev&#47;null; done | sort -t: -k2nr | head -10</div>2018-12-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/94/47/75875257.jpg" width="30px"><span>虎虎❤️</span> 👍（8） 💬（2）<div>
通过读csapp，又复习了下虚拟内存。其概念为 “虚拟内存组织为一个由存放在磁盘上的N个连续的字节大小的单元组成的数组。” 访问虚拟内存时，MMU通过访问页表，来索引到实际的存储地址。如果在物理内存中有缓存，直接从物理内存中读取数据。否则，从磁盘中读取，并选择牺牲一个物理页，并替换为新读取的页（当然，我觉得这种应该是在内存没有free的情况下）。如果被牺牲的页发生改变，则写回磁盘。最后更新页表。

我的问题是：
1. 上一节讲了虚拟内存的空间分布，那么物理内存有没有空间分布的概念？从vmstat的输出来看，物理内存是不是只包括buffer cache 和 free呢？
2. 这里的cache是不是等同于虚拟内存在物理内存中的缓存？
3. 上一节课所说的内存回收。使用LRU算法“回收缓存”，是否是我上面描述的概念？那么所谓的“回收不常访问的内存，把不常用的内存通过交换分区直接写到磁盘中”，指的是交换出哪种内存？cache？buffer？或者其他的种类？

希望得到老师回复，也欢迎各位大佬共同探讨。</div>2018-12-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/ef/3e/9c3a8abc.jpg" width="30px"><span>杜嘉嘉</span> 👍（6） 💬（1）<div>想请教一下老师，怎么看待一个系统buffer和cache使用率过高的问题。是好是坏，如果这些缓存没及时回收可能会导致，程序异常</div>2019-02-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/0b/78/22410c47.jpg" width="30px"><span>魏春河</span> 👍（6） 💬（1）<div>是不是普通文件系统最终还是要经过读写磁盘来完成保存？buffer在cache后面？</div>2018-12-26</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/GkMk4gBlfZcljsY3Vqu7w8ZkxBfe8WTz1ySnPTJARKXF0FpCr3HqlicIHQlItib9m7iaxLESkmBNpoiaY81EUUzQrA/132" width="30px"><span>小虎</span> 👍（4） 💬（4）<div>老是如果使用mmap进行写文件的话是先写入缓存，假如此时断电那么cache里面的数据会丢失吗？或者说系统怎么保证断电下cache的数据在恢复用电后还可以写入文件不丢失。</div>2019-01-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/64/05/6989dce6.jpg" width="30px"><span>我来也</span> 👍（4） 💬（1）<div>[D16打卡]
只有一块磁盘,就没轻易的试第二个案例.
---------------------------------------------------
以前应该只接触到了文件数据的缓存cache,没接触到磁盘数据的缓存buffer.
1.vim一个大文件,在第一次加载时较慢,之后再次打开时,会明显感觉到加载速度更快,应该就是cache的功劳.
2.在linux下写c程序时,打印日志printf后面习惯加fflush(stdout);
可以强制刷新缓冲区的内容到物理设备.在程序宕掉时可以定位到最后的输出日志.
如果不加fflush,可能会丢失掉部分缓冲区内的日志.
不知道这里的缓冲区跟系统的cache是不是一个概念.
---------------------------------------------------
ls -l 磁盘与普通文件的区别:
# ls -l &#47;dev&#47;sda1
brw-rw---- 1 root disk 8, 1 12月 12 10:17 &#47;dev&#47;sda1
# ls -ld &#47;root&#47;
drwx------ 12 root root 4096 12月 26 11:48 &#47;root&#47;
第一个字符b应该表示是磁盘类型 d就是目录类型了
有一列一个显示的第几块磁盘的第几个分区[8,1],一个是占用的空间大小[4096].
疑问:man ls 了也没看到各列具体的含义啊,这个去哪查呢?
---------------------------------------------------
老师最后的问题深入探索又是一篇长文了.哈哈!</div>2018-12-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/7c/59/26b1e65a.jpg" width="30px"><span>科学Jia</span> 👍（4） 💬（1）<div>老师，女同学我今天上班时间终于追到这里了。写的真真清楚，想知道您花了多少时间学这些?</div>2018-12-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/14/2e/400913b1.jpg" width="30px"><span>金波</span> 👍（4） 💬（1）<div>请问&#47;tmp&#47;file 是磁盘下的一个文件吗？ 没详细说明，可能是内存文件系统。磁盘下和tmpfs的读对Cache是否一样？</div>2018-12-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/83/69/77256c74.jpg" width="30px"><span>空白</span> 👍（3） 💬（1）<div>Buffer和Cache和其他的物理内存有什么区别呢？是位于内核空间嘛？ 应用使用时仍然需要进行映射嘛</div>2019-03-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/9b/a8/6a391c66.jpg" width="30px"><span>geraltlaush</span> 👍（2） 💬（1）<div>老师，无论是文件读写还是磁盘读写都是会涉及到bi bo的变化是吧。是因为文件读写到底层还是磁盘的块读写，是这样的吗
</div>2018-12-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/d4/79/e40f349d.jpg" width="30px"><span>long</span> 👍（1） 💬（2）<div>为什么我输入：man proc后输出如下：

proc(n)                                                        Tcl Built-In Commands                                                        proc(n)

___________________________________________________________________________________________________________________________________________________

NAME
       proc - Create a Tcl procedure

SYNOPSIS
       proc name args body
_________________________________________________________________

DESCRIPTION
       The  proc  command  creates  a  new  Tcl procedure named name, replacing any existing command or procedure there may have been by that name.
       Whenever the new command is invoked, the contents of body will be executed by the Tcl interpreter.  Normally, name is unqualified (does  not
       include  the names of any containing namespaces), and the new procedure is created in the current namespace.  If name includes any namespace
       qualifiers, the procedure is created in the specified namespace.  Args specifies the formal arguments to the procedure.  It  consists  of  a
       list,  possibly empty, each of whose elements specifies one argument.  Each argument specifier is also a list with either one or two fields.
       If there is only a single field in the specifier then it is the name of the argument; if there are two fields, then the first is  the  argu‐
       ment  name  and the second is its default value.  Arguments with default values that are followed by non-defaulted arguments become required
       arguments.  In 8.6 this will be considered an error.</div>2019-06-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/56/43/abb7bfe3.jpg" width="30px"><span>阿巍-豆夫</span> 👍（1） 💬（1）<div>老师请教下，Linux下buffer 和cache 的最大值是否有相关配置。 </div>2019-01-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/dc/dd/cf9e4ade.jpg" width="30px"><span>蒋良权</span> 👍（1） 💬（1）<div>老师，mysql等数据库使用文件系统跟使用磁盘裸IO哪个性能更好点？</div>2018-12-27</li><br/><li><img src="" width="30px"><span>Scott</span> 👍（1） 💬（1）<div>好像aerospike就是绕过文件系统直接写磁盘的，性能指标相当爆炸</div>2018-12-26</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTL9hlAIKQ1sGDu16oWLOHyCSicr18XibygQSMLMjuDvKk73deDlH9aMphFsj41WYJh121aniaqBLiaMNg/132" width="30px"><span>腾达</span> 👍（1） 💬（1）<div>$ dd if=&#47;tmp&#47;file of=&#47;dev&#47;null  为什么很快就结束了？导致vmstat值变化不大</div>2018-12-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/54/98/52ca7053.jpg" width="30px"><span>Vicky🐣🐣🐣</span> 👍（1） 💬（1）<div>困惑老师已经置顶回复了，还有一个小问题，
场景：读取文件&#47;tmp&#47;file，写入到&#47;dev&#47;null

前半部分是文件读，那后半部分的写入是什么呢？（文件读写、磁盘读写）</div>2018-12-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/da/ec/779c1a78.jpg" width="30px"><span>往事随风，顺其自然</span> 👍（1） 💬（2）<div># 首先清理缓存
$ echo 3 &gt; &#47;proc&#47;sys&#47;vm&#47;drop_caches
# 然后运行 dd 命令向磁盘分区 &#47;dev&#47;sdb1 写入 2G 数据
$ dd if=&#47;dev&#47;urandom of=&#47;dev&#47;sdb1 bs=1M count=2048
、
这个测试，在centos下是cache比buffer增长的快，和你说ub下正好相反，这是为什么？
procs -----------memory---------- ---swap-- -----io---- --system-- -----cpu-----
 r  b   swpd   free   buff  cache   si   so    bi    bo   in   cs us sy id wa st
 2  0  34840 213268    172 193516    0    0     0     0  952   94  0 23 77  0  0	
 1  0  34840 209176    172 197624    0    0     0     0 1044   92  0 24 76  0  0	
 1  0  34840 204092    172 202740    0    0     0     0 1042   97  0 24 76  0  0	
 1  0  34840 200000    180 206848    0    0     0    32 1056   97  0 25 75  0  0	
 1  0  34840 194792    180 211836    0    0     0     0 1060   87  0 25 75  0  0	
 1  0  34840 190700    180 216068    0    0     0     0 1006   96  0 24 76  0  0	
 1  0  34840 188716    180 218092    0    0     0     0  933   93  0 23 77  0  0	
 1  0  34840 184624    180 222212    0    0     0     0 1057   94  0 25 75  0  0	
 1  0  34840 179540    180 227196    0    0     0     0 1082  100  0 25 75  0  0	
 1  0  34840 175448    180 231428    0    0     0     0 1053   94  0 25 75  0  0	
 1  0  34840 170240    180 236412    0    0     0     0 1066   92  0 25 75  0  0	
 1  0  34840 166148    180 240644    0    0     0     0 1055   92  0 25 75  0  0	
 1  0  34840 164164    180 242668    0    0     0     0 1021  110  0 24 76  0  0	
 1  0  34840 158956    180 247812    0    0     0     0 1041   86  0 25 75  0  0	
 1  0  34840 154864    180 251908    0    0     0     0 1071   94  0 25 75  0  0</div>2018-12-26</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTLdWHFCr66TzHS2CpCkiaRaDIk3tU5sKPry16Q7ic0mZZdy8LOCYc38wOmyv5RZico7icBVeaPX8X2jcw/132" width="30px"><span>JohnT3e</span> 👍（1） 💬（1）<div>最后的思考题，关键点在于理解PSS项的含义。有兴趣的同学可以参考这个资料：
https:&#47;&#47;unix.stackexchange.com&#47;questions&#47;33381&#47;getting-information-about-a-process-memory-usage-from-proc-pid-smaps。</div>2018-12-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/42/f7/06cd1560.jpg" width="30px"><span>X</span> 👍（1） 💬（1）<div>另外，Linux里的块设备，可以直接访问(比如数据库应用程序)，也可以存储文件系统然后被访问吧。</div>2018-12-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/ca/e3/447aff89.jpg" width="30px"><span>记事本</span> 👍（0） 💬（1）<div>执行man free之后好像没看到有buffer cache的解释信息啊？</div>2019-10-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/18/97/e1/0f4d90ff.jpg" width="30px"><span>乖，摸摸头</span> 👍（0） 💬（1）<div>执行这个命令dd if=&#47;tmp&#47;file of=&#47;dev&#47;null ，得到的结果和你这个咋是相反的，我cache基本保持不变，buffer 组件变小
procs -----------memory---------- ---swap-- -----io---- -system-- ------cpu-----
 r  b   swpd   free   buff  cache   si   so    bi    bo   in   cs us sy id wa st
 1  0      0 117080 107504 3474324    0    0     0    20  238  377  1  1 99  0  0
 0  0      0 117068 107504 3474332    0    0     0     0  111  213  0  0 100  0  0
 0  0      0 117084 107504 3474332    0    0     0     0  135  226  0  0 100  0  0
 0  0      0 117084 107504 3474332    0    0     0     0  121  222  0  0 100  0  0
 0  0      0 117084 107504 3474332    0    0     0     0   92  194  0  0 100  0  0
 0  1      0 148380 107408 3442816    0    0 94032    88  691  469  3  8 63 26  0
 0  1      0 122760 107392 3468668    0    0 106496     0  613  288  4  9 49 38  0
 0  1      0 113608 107304 3477624    0    0 106476    52  794  526  4 11 48 38  0
 0  1      0 122352 106692 3469596    0    0 110572     0  685  364  3 11 49 37  0
 0  1      0 106076 104532 3488492    0    0 106496     0  805  343  3 10 50 38  0
 0  1      0 139176  95716 3464028    0    0 107112    36  845  441  3 11 43 44  0
 0  1      0 133140  90324 3475664    0    0 106496     4  718  419  4 10 50 38  0
 0  1      0 116984  85996 3494492    0    0 107840   112  765  403  4  9 47 41  0
 0  1      0 140996  79804 3476896    0    0 110592     0  784  374  3 10 49 38  0
 0  1      0 107904  74956 3514968    0    0 103936     0  837  486  4  9 50 38  0
 0  1      0 116384  67268 3513988    0    0 107332     0  958  475  4 11 48 36  0
 0  1      0 124256  60424 3513064    0    0 110592     0  806  440  4 11 49 38  0
 0  1      0 123492  54248 3519804    0    0 106496    16  908  436  4  9 49 38  0
 0  1      0 101788  52656 3544452    0    0 102192     0 1000  470  4 10 49 38  0
 1  0      0 110320  49340 3539408    0    0 66968     0 1020  402  7 20 49 23  0</div>2019-08-02</li><br/>
</ul>