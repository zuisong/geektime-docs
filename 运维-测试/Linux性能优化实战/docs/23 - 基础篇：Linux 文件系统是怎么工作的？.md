你好，我是倪朋飞。

通过前面CPU和内存模块的学习，我相信，你已经掌握了CPU和内存的性能分析以及优化思路。从这一节开始，我们将进入下一个重要模块——文件系统和磁盘的I/O性能。

同CPU、内存一样，磁盘和文件系统的管理，也是操作系统最核心的功能。

- 磁盘为系统提供了最基本的持久化存储。
- 文件系统则在磁盘的基础上，提供了一个用来管理文件的树状结构。

那么，磁盘和文件系统是怎么工作的呢？又有哪些指标可以衡量它们的性能呢？

今天，我就带你先来看看，Linux文件系统的工作原理。磁盘的工作原理，我们下一节再来学习。

## 索引节点和目录项

文件系统，本身是对存储设备上的文件，进行组织管理的机制。组织方式不同，就会形成不同的文件系统。

你要记住最重要的一点，在Linux中一切皆文件。不仅普通的文件和目录，就连块设备、套接字、管道等，也都要通过统一的文件系统来管理。

为了方便管理，Linux文件系统为每个文件都分配两个数据结构，索引节点（index node）和目录项（directory entry）。它们主要用来记录文件的元信息和目录结构。

- 索引节点，简称为inode，用来记录文件的元数据，比如inode编号、文件大小、访问权限、修改日期、数据的位置等。索引节点和文件一一对应，它跟文件内容一样，都会被持久化存储到磁盘中。所以记住，索引节点同样占用磁盘空间。
- 目录项，简称为dentry，用来记录文件的名字、索引节点指针以及与其他目录项的关联关系。多个关联的目录项，就构成了文件系统的目录结构。不过，不同于索引节点，目录项是由内核维护的一个内存数据结构，所以通常也被叫做目录项缓存。
<div><strong>精选留言（30）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/0f/a3/25/5da16c25.jpg" width="30px"><span>coyang</span> 👍（174） 💬（1）<div>课后题：
这个命令，会不会导致系统的缓存升高呢？
--&gt; 会的
如果有影响，又会导致哪种类型的缓存升高呢？
--&gt; &#47;xfs_inode&#47; proc_inode_cache&#47;dentry&#47;inode_cache

实验步骤：
1. 清空缓存：echo 3 &gt; &#47;proc&#47;sys&#47;vm&#47;drop_caches ; sync
2. 执行find ： find &#47; -name test
3. 发现更新top 4 项是：
  OBJS ACTIVE  USE OBJ SIZE  SLABS OBJ&#47;SLAB CACHE SIZE NAME
 37400  37400 100%    0.94K   2200       17     35200K xfs_inode
 36588  36113  98%    0.64K   3049       12     24392K proc_inode_cache
104979 104979 100%    0.19K   4999       21     19996K dentry
 18057  18057 100%    0.58K   1389       13     11112K inode_cache

find &#47; -name 这个命令是全盘扫描（既包括内存文件系统又包含本地的xfs【我的环境没有mount 网络文件系统】），所以 inode cache &amp; dentry &amp; proc inode cache 会升高。

另外，执行过了一次后再次执行find 就机会没有变化了，执行速度也快了很多，也就是下次的find大部分是依赖cache的结果。</div>2019-01-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/99/ff/046495bb.jpg" width="30px"><span>小成</span> 👍（17） 💬（2）<div>请问老师，除了目录项以外还有哪些地方保存有文件名，下一节讲到目录项是一个内存缓存，那么不会保存文件名到磁盘上面？</div>2019-02-01</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/f8/19/05a2695f.jpg" width="30px"><span>伟忠</span> 👍（16） 💬（7）<div>机器上 df 查看占用了 200G，但 du 查看发现只有 90G，看网上的办法用 lsof | grep delete 查看，但没有找到，请问老师，这个可能是什么原因呢？</div>2019-01-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/4a/2c/f8451d77.jpg" width="30px"><span>石维康</span> 👍（16） 💬（4）<div>阻塞 I&#47;O 和非阻塞 I&#47;O的概念和同步和异步 I&#47;O的区别是什么?</div>2019-01-11</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/ccpIPibkaTQfYbO5DGiaWpL86YSHAZfVO55WtJhjV0hb7AuyIMzLyRdLnQZ6tjB0Wars4ib7YX3fhmPh9R81MVKtA/132" width="30px"><span>肘子哥</span> 👍（12） 💬（4）<div>有个疑惑，如果目录项存在内存中是不是意味着内存故障后，目录就无法访问了呢？</div>2019-02-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/f7/9b/1b1e288a.jpg" width="30px"><span>董文荣</span> 👍（8） 💬（2）<div>课后题：
Q:$ find &#47; -name file-name
这个命令，会不会导致系统的缓存升高呢？如果有影响，又会导致哪种类型的缓存升高呢？
A:分析
1)、&quot;&#47;&quot;代表文件系统的根目录，目录项已经缓存在cached。(通过下面的测试，怀疑应该只是部分目录项的内容缓存在cache中，待验证)
2)、因为会匹配值“file-name“，会将索引节点读入缓存进行匹配。
因此会导致cached增长。以下是三组测试对比，给出了执行find命令前后，cached变化的对比。
命令之前前后，slabtop的执行前后对比:
Active &#47; Total Objects (% used)    : 184412 &#47; 240169 (76.8%)
 Active &#47; Total Size (% used)       : 42926.19K &#47; 59199.82K (72.5%)

  OBJS ACTIVE  USE OBJ SIZE  SLABS OBJ&#47;SLAB CACHE SIZE NAME                   
 11088   2313  20%    0.57K    198	 56	 6336K radix_tree_node
 10450   9515  91%    0.58K    190	 55	 6080K inode_cache
 27510  12695  46%    0.19K    655	 42	 5240K dentry
  4710   1003  21%    1.06K    157	 30	 5024K xfs_inode


 Active &#47; Total Objects (% used)    : 1795399 &#47; 1809652 (99.2%)
 Active &#47; Total Size (% used)       : 1004316.02K &#47; 1007573.47K (99.7%)

  OBJS ACTIVE  USE OBJ SIZE  SLABS OBJ&#47;SLAB CACHE SIZE NAME                   
708420 708420 100%    1.06K  23614	 30    755648K xfs_inode
787878 787878 100%    0.19K  18759	 42    150072K dentry

free命令在find命令执行前后结果对比:
[root@localhost ~]# free -m
              total        used        free      shared  buff&#47;cache   available
Mem:           1824         200        1534          15          89        1500
Swap:          2047         196        1851
[root@localhost ~]# free -m
              total        used        free      shared  buff&#47;cache   available
Mem:           1824         480         105          15        1238        1161
Swap:          2047         196        1851

vmstat在find命令执行前后对比：
[root@localhost &#47;]# vmstat  2 
procs -----------memory---------- ---swap-- -----io---- -system-- ------cpu----
 r  b   swpd   free   buff  cache   si   so    bi    bo   in   cs us sy id wa st
 2  0 201208 1570636    136  92168    0    0     5     5   16   19 27  3 70  0  0
 0  0 201208 1511788    136 149564    0    0  1702     0  491  599  2  6 90  1  0
 0  0 201208 1509428    136 149716    0    0  1106     0  478  801  0  2 98  0  0
注:发表长度限制，省略部分测试显示


</div>2019-01-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/b8/36/542c96bf.jpg" width="30px"><span>Mr.Strive.Z.H.L</span> 👍（6） 💬（1）<div>老师您好：
关于目录项有一个疑惑：

通过目录项找到inode节点，从而访问具体的文件内容。其中inode和文件数据块都会被持久化，而目录项竟然不会被持久化，只是放在内存中进行缓存。

那么是否在每次开机时，内核都会自动构建文件系统完整的目录项，然后进行缓存？？</div>2019-01-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/13/51/99c88021.jpg" width="30px"><span>成为祝福</span> 👍（6） 💬（1）<div>老师好，请问在slabtop中的inode_cache和ext4_inode_cache有什么区别呢？如果每个文件系统都有inode_cache，整个vfs的有效命名空间都映射到了对应的文件系统，vfs为什么还需要inode_cache呢？</div>2019-01-16</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/2d/24/28acca15.jpg" width="30px"><span>DJH</span> 👍（6） 💬（1）<div>请教三个问题。

1. 目录项是维护在内核中的一个内存数据结构，包括文件名。
我的问题是：文件名不是也应该存储在磁盘上么？不可能仅仅存在于内存吧？

2. 缓冲 I&#47;O，是指利用标准库缓存来减速文件的访问...
我的问题时：减速文件访问的原因是什么？

3. 阻塞&#47;非阻塞与同步&#47;非同步的区别是什么？</div>2019-01-11</li><br/><li><img src="" width="30px"><span>Geek_9815f1</span> 👍（2） 💬（3）<div>你要记住最重要的一点，在 Linux 中一切皆文件。不仅普通的文件和目录，就连块设备、套接字、管道等，也都要通过统一的文件系统来管理。    老师，上次听你 讲块设备和 文件系统的区别： 说块设备读写是绕过文件系统的。 现在是 块设备也通过统一的文件系统来管理。 这有矛盾吗？</div>2020-07-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/ce/c6/958212b5.jpg" width="30px"><span>sugar</span> 👍（2） 💬（1）<div>老师您好，想问 inode信息是存在文件内 还是单独存在另外的磁盘区域呢？换句话说，如果我把一个文件scp到另一台机器上，它的inode信息会跟过去吗？ 因为我发现 有时刚刚从linux上下载到mac本地的文件，stat命令查看创建时间（ext好像不记录这个 但mac的fs会有这个字段） 竟然早于当天。</div>2019-03-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/47/ab/3311945c.jpg" width="30px"><span>shonm</span> 👍（2） 💬（4）<div>老师 您好 您说目录项是个缓存，那么关机后会存放在磁盘吗，否则下次开机的时候去哪里读取目录呢</div>2019-03-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/4e/0f/c43745e7.jpg" width="30px"><span>hola</span> 👍（2） 💬（1）<div>“索引节点和文件一一对应，它跟文件内容一样，都会被持久化存储到磁盘”
是一对一关系吗，那么看我的服务器
$ df -i &#47;
文件系统                                 Inode 已用(I) 可用(I) 已用(I)% 挂载点
&#47;dev&#47;mapper&#47;VolGroup-lv_root 655360   98862  556498      16% &#47;
意思是这个下面理论最多存放655360个文件  对吗



</div>2019-02-23</li><br/><li><img src="" width="30px"><span>Geek_9815f1</span> 👍（1） 💬（1）<div>你要记住最重要的一点，在 Linux 中一切皆文件。不仅普通的文件和目录，就连块设备、套接字、管道等，也都要通过统一的文件系统来管理。   上一章不是说过 块设备绕过文件系统， 现在又说统一由文件系统管理 </div>2020-07-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/02/59/989f65c8.jpg" width="30px"><span>jacky</span> 👍（1） 💬（2）<div>请问老师，我的Linux的Use%显示100%，我该如何排查呢？</div>2019-05-10</li><br/><li><img src="" width="30px"><span>frank_</span> 👍（1） 💬（1）<div>请教老师， 对文件系统挂载不是很理解，VFS虚拟文件系统也有目录树，它不是只定义了API吗，它的目录树默认是什么的？任何一个路径都可以作为挂载点吗？</div>2019-04-01</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/ce/c6/958212b5.jpg" width="30px"><span>sugar</span> 👍（1） 💬（1）<div>老师您好，接我的上一条提问，有关inode的存储位置，其实我是想问，如果我直接读一个文件的内容二进制格式，并把它传输到另一台机器，那么原机器的inode及dentry信息都是不会保留的，因为文件本身的内容里不包含这些，这么说对吗？</div>2019-04-01</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/0f/51/ec3a5d28.jpg" width="30px"><span>Something</span> 👍（1） 💬（1）<div>为什么能把内存也能搞成文件系统？它又不是IO设备？</div>2019-01-15</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/11/4b/fa64f061.jpg" width="30px"><span>xfan</span> 👍（1） 💬（2）<div>我觉得目录项应该也是要交换到磁盘里，在内存里的话怎么持久化呢</div>2019-01-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/41/f2/34fb0a9d.jpg" width="30px"><span>橘子</span> 👍（1） 💬（1）<div>操作系统中只能用一种文件系统还是可以多个文件系统在同一个操作系统中共存？共存的话如何查看操作系统用了哪些文件系统，这些文件系统由哪些设备使用，比如磁盘用的什么文件系统，网络用的什么文件系统，内存用的什么文件系统</div>2019-01-13</li><br/><li><img src="" width="30px"><span>bluefantasy1</span> 👍（1） 💬（2）<div>请教老师一个问题：dentry目录缓存项属于内核的缓存，但是它肯定是要持久化在的呀，持久化在哪里？操作系统启动的时候加载到缓存对吧？是把整个系统的所有dentry全部加载到缓存吗？</div>2019-01-12</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/3XbCueYYVWTiclv8T5tFpwiblOxLphvSZxL4ujMdqVMibZnOiaFK2C5nKRGv407iaAsrI0CDICYVQJtiaITzkjfjbvrQ/132" width="30px"><span>有铭</span> 👍（1） 💬（1）<div>老师我想请教两个问题：
1.目录项是维护在内核中的一个内存数据结构，这是不是说每次系统启动的时候，都得检索硬盘，然后生成这个结构？这样说来，如果磁盘上文件挺多的时候，启动会不会很慢？
2.我这有一台别人设置的ubuntu，之前的人做了一件事情，它把一块vfs管理的设备&#47;dev&#47;vda1 （大小50G）挂载到了&#47;目录下，然后把另外一块存储设备&#47;dev&#47;vdb1 （大小99G）挂载到了&#47;home&#47;ubuntu&#47;data2目录下。结果现在df -h报告&#47;dev&#47;vda1使用接近97%。我查了好久，du -h --max-depth=1  挨个扫目录，也查不出到底哪里被使用了。而且du看到&#47;目录的使用大小是68G。就是不知道这到底是怎么回事</div>2019-01-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/17/1b/ab/a5f88914.jpg" width="30px"><span>kubxy</span> 👍（0） 💬（1）<div>老师，您好。我有一个疑问，内存中的目录项是如何生成的呢？
我们都知道内存中的数据在关机后会丢失。目录项是由内核维护的，存储在内存中，那么关机时内存中的目录项如何处理：
1）持久化到磁盘？下次开机直接从磁盘读入内存
2）丢就丢呗（就这么任性），下次开机时由内核重新生成，如果是这种机制，那么问题又来了，如何生成呢，根据超级块和索引节点区计算吗？
3）其他...</div>2019-05-25</li><br/><li><img src="" width="30px"><span>anwj</span> 👍（0） 💬（2）<div>老师，遇到这样一个实际问题，目录下有200万+个文件，用什么方式可以比较快的统计出来，最好用1s时间能统计出结果</div>2019-04-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/75/ba/ac35ac17.jpg" width="30px"><span>chich chung kai</span> 👍（0） 💬（1）<div>老师，请问怎么释放源文件已经删除的文件句柄，不用杀掉进程的那种：
[root@VM_2_2_centos fd]# ll
total 0
lr-x------. 1 root root 64 Mar  6 19:46 0 -&gt; &#47;dev&#47;null
l-wx------. 1 root root 64 Mar  6 19:46 1 -&gt; &#47;dev&#47;null
lr-x------. 1 root root 64 Mar  6 19:46 10 -&gt; pipe:[12921]
lr-x------. 1 root root 64 Mar  6 19:46 11 -&gt; pipe:[12923]
l-wx------. 1 root root 64 Mar  6 19:46 12 -&gt; &#47;tmp&#47;gunicorn_command-stdout---supervisor-cFRLNf.log (deleted)
l-wx------. 1 root root 64 Mar  6 19:46 13 -&gt; &#47;tmp&#47;gunicorn_command-stderr---supervisor-siKNox.log (deleted)
l-wx------. 1 root root 64 Mar  6 19:46 14 -&gt; pipe:[12925]
lr-x------. 1 root root 64 Mar  6 19:46 15 -&gt; pipe:[12924]
lr-x------. 1 root root 64 Mar  6 19:46 16 -&gt; pipe:[12926]
l-wx------. 1 root root 64 Mar  6 19:46 17 -&gt; &#47;tmp&#47;todb_command-stdout---supervisor-MUh7Ph.log (deleted)
l-wx------. 1 root root 64 Mar  6 19:46 18 -&gt; &#47;tmp&#47;todb_command-stderr---supervisor-jPHkOa.log (deleted)
l-wx------. 1 root root 64 Mar  6 19:46 2 -&gt; &#47;dev&#47;null
lr-x------. 1 root root 64 Mar  6 19:46 20 -&gt; pipe:[12927]
l-wx------. 1 root root 64 Mar  6 19:46 22 -&gt; &#47;tmp&#47;nginx_command-stdout---supervisor-ZRr66X.log (deleted)
l-wx------. 1 root root 64 Mar  6 19:46 23 -&gt; &#47;tmp&#47;nginx_command-stderr---supervisor-073_FI.log (deleted)
l-wx------. 1 root root 64 Mar  6 19:46 3 -&gt; &#47;tmp&#47;supervisord.log (deleted)
lrwx------. 1 root root 64 Mar  6 19:46 4 -&gt; socket:[12616]
lrwx------. 1 root root 64 Mar  6 19:46 5 -&gt; socket:[12693]
l-wx------. 1 root root 64 Mar  6 19:46 7 -&gt; pipe:[12919]
lr-x------. 1 root root 64 Mar  6 19:46 8 -&gt; pipe:[12920]
l-wx------. 1 root root 64 Mar  6 19:46 9 -&gt; pipe:[12922]

</div>2019-04-03</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/fb/1d/12c7c021.jpg" width="30px"><span>挺直腰板</span> 👍（0） 💬（1）<div>老师，你说free 输出的 Cache，是页缓存和可回收 Slab 缓存的和，但在centos7中得出数据还有些差异是为什么?
[root@localhost ~]# cat &#47;proc&#47;meminfo |grep -E &quot;SReclaimable|Cached&quot;
Cached:         13924792 kB
SwapCached:           20 kB
SReclaimable:     659860 kB
[root@localhost ~]# free -m
             total       used       free     shared    buffers     cached
Mem:         31883      23390       8492        353          0      13242
-&#47;+ buffers&#47;cache:      10148      21734
Swap:        31999          3      31996</div>2019-03-16</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/5a/9e/8f2ccc1d.jpg" width="30px"><span>有点意思</span> 👍（0） 💬（2）<div>奇怪了 想讲内容打印出来看 可是使用网页的浏览功能却只能打印一页 这是什么鬼</div>2019-03-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/fb/1d/12c7c021.jpg" width="30px"><span>挺直腰板</span> 👍（0） 💬（1）<div>老师能知道内核态用了多少内存？</div>2019-03-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/33/46/7b2dac61.jpg" width="30px"><span>苏宁</span> 👍（0） 💬（1）<div>老师，能否推荐关于linux文件系统的书</div>2019-01-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/ec/02/083566d7.jpg" width="30px"><span>在路上</span> 👍（0） 💬（1）<div>请问老师，后期有关于网络方面性能分析吗？多谢
</div>2019-01-13</li><br/>
</ul>