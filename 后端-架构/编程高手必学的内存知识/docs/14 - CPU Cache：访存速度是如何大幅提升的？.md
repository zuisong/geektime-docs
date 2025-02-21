你好，我是海纳。

经过上一节课的学习，我们了解到不同的物理器件，它们的访问速度是不一样的：速度快的往往代价高、容量小；代价低且容量大的，速度通常比较慢。为了充分发挥各种器件的优点，计算机存储数据的物理器件不会只选择一种，而是以CPU为核心，由内而外地组建了一整套的存储体系结构。它将各种不同的器件组合成一个体系，让各种器件扬长避短，从而形成一种快速、大容量、低成本的内存系统。

而我们要想写出高性能的程序，就必须理解这个存储体系结构，并运用好它。因此，今天这节课我们就来看看常见的存储结构是如何搭建的，并借此把握好影响程序性能的主要因素，从而对程序性能进行优化。

## 存储体系结构的核心

作为程序员，我们肯定是希望有无限资源的快速存储器，来存放程序的数据。而现实是，快速存储器的制造成本很高，速度慢的存储器相对便宜。所以从成本角度来说，计算机的存储结构被设计成分层的，一般包括寄存器、缓存、内存、磁盘等。

其中，缓存又是整个存储体系结构的灵魂，它让内存访问的速度接近于寄存器的访问速度。所以，要想深入理解存储体系结构，我们就要围绕“缓存”这个核心来学习。

在过去的几十年，处理器速度的增长远远超过了内存速度的增长。尤其是在2001～2005年间，处理器的时钟频率在以55%的速度增长，而同期内存速度的增长仅为7%。为了缩小处理器和内存之间的速度差距，缓存被设计出来。
<div><strong>精选留言（16）</strong></div><ul>
<li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTKwGurTWOiaZ2O2oCdxK9kbF4PcwGg0ALqsWhNq87hWvwPy8ZU9cxRzmcGOgdIeJkTOoKfbxgEKqrg/132" width="30px"><span>ZR2021</span> 👍（5） 💬（4）<div>老师太棒了，这是我见过将缓存讲的最详细的文章，课买的真值！！！
不过有几个问题想请教下老师：
1. 文章中提到的根据32位地址确定缓存的组和路，这个地址是虚拟地址还是物理地址？ 后面的案例里的数组的地址是虚拟的连续地址，映射到物理地址的话不一定连续，所以当第二层4096循环的时候不一定会落到同一组；如果是物理地址的话，那就是说也得经过页表转换，这个转换是不是先经过TLB的转换，如果TLB miss里再到内存里加载新的页表？
2. 缓存伪共享看样子只会出现在多线程的场景下，单进程的话每个进程内存映射后的物理地址的间隔远远大于一个cache line，所以不会出现多进程访问了同一个cache line的情况
3. 进程切换比线程切换的代价小是不是有一部分就是这个cache line 缺失导致的，因为切换到新的进程后，里面的数据要从内存重新加载到cache line中，频繁的进程切换导致的cache 缺失也挺严重的

希望得到老师的解答，万分感谢！！！</div>2021-12-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/2f/7a/ab6c811c.jpg" width="30px"><span>相逢是缘</span> 👍（3） 💬（1）<div>老师，我可能陷入思维误区了，有几个问题请教一下
1、CPU如何把数据读取到cache的呢？
某个时刻一个CPU指令访问数据地址0，一个cache line 64个字节，CPU会把0~63这64个字节全部读取到cache line，假如数据线是64位，一次能读取8个字节，也需要读取8次，如果读取一次需要100个CPU时钟周期，那读取一个cache line需要800个时钟周期。但是下条指令访问的数据地址可能是0x100000，这时CPU是插入NOP操作，等待800个时钟周期等着cache line填充完吗？还是怎么操作的呢？
2、缓存做成多级，每一级电路上有什么不同吗（都是SRAM？），主要是因为硬件集成电路价格的原因去分为这么多级缓存吗？
3、了解到L1级缓存一般都分为指令Icache和数据Dcache，而到L2、L3就不分了Icache和Dcache了呢？</div>2021-11-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/23/57/5ba842bc.jpg" width="30px"><span>aikeke</span> 👍（1） 💬（2）<div>老师，一个cache line里，V（valid）、M（modified）以及tag这几个字段是保存在哪里呢？&quot;假设要寻址一个 32 位的地址，缓存块的大小是 64 字节，缓存组织方式是 4 路组相连，缓存大小是 8K。经过计算我们得到缓存一共有 32 个组（8×1024÷64÷4=32）&quot;</div>2021-12-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/20/3b/2a/f05e546a.jpg" width="30px"><span>🐮</span> 👍（0） 💬（1）<div>老师，你好，平台我们为提升读取数据性能，会把所需要的数据尽量放在同一个cache line中，但如果存在多个进程会对相临数据写时又要尽量不要把数据放在同一个cache line中，这块是否是从读和写来理解比较好啊，如果是读，就放一起，多进程写就不要放一起；</div>2021-11-30</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/8f/cf/890f82d6.jpg" width="30px"><span>那时刻</span> 👍（0） 💬（1）<div>从文件角度理解，buffer可以理解为是一类特殊文件的cache，这类特殊文件就是设备文件，比如&#47;dev&#47;sda1, 这类设备文件的内容被读到内存后就是buffer。而cache则是普通文件的内容被读到了内存。</div>2021-11-30</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1b/83/fb/621adceb.jpg" width="30px"><span>linker</span> 👍（0） 💬（1）<div>LEVEL1_ICACHE_SIZE                 32768
LEVEL1_ICACHE_ASSOC                8
LEVEL1_ICACHE_LINESIZE             64
LEVEL1_DCACHE_SIZE                 32768
LEVEL1_DCACHE_ASSOC                8
LEVEL1_DCACHE_LINESIZE             64

一个cacheline == 64bytes, 总共有8路，64组，64*64*8=32768bytes是这样吗？
如果是这样的话，每个路就相当于一个cacheline</div>2021-11-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1b/83/fb/621adceb.jpg" width="30px"><span>linker</span> 👍（0） 💬（1）<div>大佬，L1 cache，一路等于64个cacheline， 这个是怎么计算出来的，有点懵？</div>2021-11-29</li><br/><li><img src="" width="30px"><span>shenglin</span> 👍（0） 💬（1）<div>cache的物理介质是SRAM，存储的是主存里某些地址上的数据，buffer是主存的一部分，物理介质是DRAM，存储的是业务的缓冲数据。</div>2021-11-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/2a/16/cd/226cd9f1.jpg" width="30px"><span>满分💯</span> 👍（3） 💬（0）<div>看完收获很多，最近看了一票文章 ，结合这看，效果更加 https:&#47;&#47;coolshell.cn&#47;articles&#47;20793.html
 </div>2021-12-16</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/25/3c/92/81fa306d.jpg" width="30px"><span>张Dave</span> 👍（2） 💬（1）<div>第二层循环是以 512 为间隔访问元素，即每次访问都会落在同一个组内的不同 cache line ，因为一组有 8 路。
有点疑问：
一个组内有8路，8条cacheline，可容纳64元素。为什么不是按照64元素间隔遍历，这样就可以把一个组内的cacheline都替换完啊，为什么要按照512元素遍历？</div>2022-02-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/23/c1/37/f1579f8a.jpg" width="30px"><span>奥陌陌</span> 👍（1） 💬（0）<div>组是横着看,一行叫一个组吗,路是竖着看,一列是一个路吗 ???</div>2023-02-01</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/2b/52/40/1fe5be2b.jpg" width="30px"><span>联通</span> 👍（1） 💬（0）<div>cache一般是缓存，在读场景中用的比较懂，比如加载的文件缓存内存中，当下次读取就不用去磁盘加载；buffer一般缓冲区，在写场景中用的比较多，比如写一个文件，可以将多次写的数据先缓存下来，然后一次性写入磁盘，减少IO等待的时间</div>2022-03-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1e/b2/83/7cf8e650.jpg" width="30px"><span>Chunel</span> 👍（0） 💬（0）<div>老师，请问：
我new了两个类对象，分别在两个线程里做 i++
我怎么确定，这两个类中的 i 变量，在不在一个cacheline，从而避免伪共享呢？</div>2022-09-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/26/82/0c/cc106ab1.jpg" width="30px"><span>Samaritan.</span> 👍（0） 💬（0）<div>老师你好，我想请教一个问题:
对组数 32 取模，组号同时也等于 Addr 的第 6~10 位（ (Addr &gt;&gt; 6) &amp; 0x1F ）

是根据什么信息得出，组号等于addr第二的第6~10位呢？主号不可以使用地址的高5位，而使用地址中间的21位作为tag吗？</div>2022-07-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/99/f2/c74d24d7.jpg" width="30px"><span>大豆</span> 👍（0） 💬（0）<div>1，我认为cache是真实存在的硬件，buffer是人为抽象出来的。buffer所对应的区域可以在cache中，也可以在内存中。它们共同的目的都是为了提高运行效率。
2，我认为buffer实际上是一种预热操作，通过cache及局部性来实现了高效，在需要及时响应场景用的多;而cache则是一个通用的操作，可以用于任何场景。</div>2021-11-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/cd/ed/825d84ee.jpg" width="30px"><span>费城的二鹏</span> 👍（0） 💬（0）<div>cache是缓存的数据，一般是完整的数据。buffer是缓冲数据，类似于看视频时，加载当前到几分钟以后的内容。

不知道这样解释对不对。</div>2021-11-29</li><br/>
</ul>