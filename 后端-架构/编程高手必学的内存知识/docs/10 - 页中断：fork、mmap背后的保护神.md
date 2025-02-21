你好，我是海纳。

这节课是对前面所有课程的一次总结和回顾。前面我们介绍了很多内存管理的相关机制，其实都是为了把这节课的故事讲完整。在前面的课程里，我们了解了进程内部的分布，但也留下了三个关键的问题没有讲清楚：

1. fork的工作方式非常奇怪，一方面父进程和子进程还可以访问共有的变量，另一方面，它们又可以各自修改这个变量，且这个修改对方都看不见，这是怎么做到的呢？
2. 我们在[第1节课](https://time.geekbang.org/column/article/430073)讲内存映射时，就讲过页表中未映射状态的页表项，并不存在一块具体的物理内存与之对应。但是当我们访问到这一页的时候，页表项可以自动变成已映射的正常状态。谁在背后做了什么事情呢？
3. mmap的功能十分强大，这些强大的能力是怎么完成的呢？

这三个问题，虽然看上去相互之间关系不大，但实际上它们背后都依赖**页中断机制**。

页中断和普通的中断一样，它的中断服务程序入口也在IDT中（[第2节课](https://time.geekbang.org/column/article/431400)的内容），但它是由MMU产生的硬件中断。**页中断有两类重要的类型：写保护中断和缺页中断。正是这两类中断在整个系统的后台默默地工作着，就像守护神一样支撑着内存系统正常工作**。

大多数时候，我们即使不知道它们的存在，程序也能正常地运行。但是有时候，程序写得不好就有可能造成中断频繁发生，从而带来巨大的性能下降。面对这种情况，我们第一时间就应该想到统计页中断。因为除了页中断本身会带来性能下降之外，统计页中断也可以反推程序的运行特点，从而为进一步分析程序瓶颈点，提供数据和思路。
<div><strong>精选留言（11）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/20/3b/2a/f05e546a.jpg" width="30px"><span>🐮</span> 👍（5） 💬（1）<div>老师，建议对思考题进行分析下，验证我们分析过程；

父进程使用mmap申请私有匿名内存后，再使用fork创建子进程，这块内存会被子进程共享，同时系统会将这块内存设置为只读，当子进程使用sprintf去写数据时，会触发写时复制机制，拷贝一份内存区域，也就是说创建子进程后父子进程写的数据都不可见，他们都是操作自己特有内存空间；除非是在创建子进程前写入的数据，父子进程才可见；</div>2021-11-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/08/99/6ab45a2f.jpg" width="30px"><span>小时候可鲜啦</span> 👍（3） 💬（1）<div>1、吊打面试官中，对于全局变量，映射方式应该是可读可写（而不是只读）吧。
2、对于共享库的映射，在第三课中将其归类到了私有文件映射。我觉得对于只读部分是不是应该归属于共享文件映射，而可读可写的部分才归属于私有文件映射。</div>2021-12-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/19/70/67/0c1359c2.jpg" width="30px"><span>qinsi</span> 👍（2） 💬（1）<div>参考资料里的《Linux 内核设计与实现》似乎还是旧版的，新版（第三版）里已经提到了page cache从hash改为radix tree的理由，比如hash的冲突解决使用了链表，对于不存在的key需要遍历完整个链表才能知道不存在；又比如radix tree（又名压缩前缀树）可以压缩存储相同前缀的key，比hash更节省空间。</div>2021-11-16</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/flibDYwNrpSVceVKvryUnfqicDILpxLx1FLzyDfoRuA0NU5PUzzCzjzJbU2GeiaP7BjKEBAhHtib3xK5NhIC8Vv73A/132" width="30px"><span>Geek_347b1f</span> 👍（1） 💬（1）<div>作者能不能讲一下java零拷贝和直接内存用mmap怎么实现的</div>2021-12-03</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/26/82/0c/cc106ab1.jpg" width="30px"><span>Samaritan.</span> 👍（0） 💬（2）<div>老师，请问一下，由于fork复制了父进程的task_struct，那么子进程就可以读取到父进程所有的信息了吧？这样是安全的吗？</div>2021-11-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1b/83/fb/621adceb.jpg" width="30px"><span>linker</span> 👍（0） 💬（1）<div>思考题:后执行的进程应该会发生crash</div>2021-11-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/cd/ed/825d84ee.jpg" width="30px"><span>费城的二鹏</span> 👍（0） 💬（1）<div>老师，私有文件映射，多个进程加载同一个文件，其中一个进程进行写入时会发生写时复制。那么，其它进程能否感知到这个文件的变化？</div>2021-11-16</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/cd/ed/825d84ee.jpg" width="30px"><span>费城的二鹏</span> 👍（0） 💬（2）<div>吊打面试官中，共享库加载时设置为只读，代码段与全局变量都是只读的，在写入是会进行复制。系统如何保护代码段不会被写入的？这两种内容的只读标记是是相同的吗？</div>2021-11-16</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/20/75/b5/858275ac.jpg" width="30px"><span>大鑫仔Yeah</span> 👍（0） 💬（1）<div>作者能不能后续讲解下非自动管理内存的语言，比如 Swift </div>2021-11-15</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/ba/4d/7ba09ff0.jpg" width="30px"><span>郑童文</span> 👍（3） 💬（1）<div>你好老师， 从这一课中所学的内容来看，似乎mmap在分配内存时只是分配了虚拟内存，要等到进程访问这块虚拟内存时 才会被映射到物理内存页， 那既然内存分配都只是分配虚拟内存，虚拟内存非常大，我们为什么还需要考虑虚拟内存的内部碎片和外部碎片的问题呢？虚拟内存那么大浪费一些无所谓啊？

还请教老师一个关于伙伴系统的问题：

操作系统的教材上说伙伴系统被用于分配连续的物理页。我有些不明白我们为什么需要策略来管理物理内存的分配呢？ 在我的理解中，物理内存应该是已经被划分成一页一页的了，当虚拟内存被分配以后，将虚拟内存直接映射到空闲的物理页就可以了，进程使用的是虚拟内存地址，它只需要连续的虚拟内存，而连续的虚拟内存完全可以映射到不连续的物理页啊？我们只需要记录哪些物理页已经被映射， 哪些物理页是未被映射的，这些物理页连不连续无所谓啊？ 在需要物理页的时候找一个空闲的页来映射就可以了啊？

谢谢！</div>2021-12-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1a/1e/de/cdee1780.jpg" width="30px"><span>我是内存</span> 👍（1） 💬（0）<div>mmap的这4种方式中，都用到了vma，只要是进程间有共享需求的情况都需要关联到一个文件，不管是实际文件还是虚拟的文件。vma唯一不需要关联文件的情况是进程申请空间自己用。</div>2021-11-22</li><br/>
</ul>