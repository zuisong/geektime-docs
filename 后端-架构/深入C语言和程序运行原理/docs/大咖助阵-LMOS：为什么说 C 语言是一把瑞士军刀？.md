你好，我是LMOS。

很高兴受邀来到这个专栏做一期分享。也许这门课的一些同学对我很熟悉，我是极客时间上[《操作系统实战45讲》](https://time.geekbang.org/column/intro/100078401?tab=catalog)这门课的作者，同时也是LMOS、LMOSEM这两套操作系统的独立开发者。十几年来，我一直专注于操作系统内核研发，在C语言的使用方面有比较深刻的理解，所以想在这里把我的经验、见解分享给你。

操作系统和C语言的起源有着千丝万缕的联系，那么今天，我就先从C语言的起源和发展历史讲起。然后，我会从C语言自身的语法特性出发，向你展示这门古老的语言简单在哪里，又难在哪里。

## **C语言、UNIX的起源和发展**

从英国的剑桥大学到美国的贝尔实验室，C语言走过了一段不平凡的旅程。从最开始的CPL语言到BCPL语言，再到B语言，到最终的C语言，一共经历了四次改进。从20世纪中叶到21世纪初，C语言以它的灵活、高效、通用、抽象、可移植的特性，在计算机界占据了不可撼动的地位。但是，C语言是如何产生的？诞生几十年来，它的地位为何一直不可动摇？请往下看。

### C语言是两位牛人“玩”出来的

1969年夏天，美国贝尔实验室的肯·汤普森的妻子回了娘家，这位理工男终于有了自己的时间。于是，他以BCPL语言为基础，设计出了简单且接近于机器语言的B语言（取BCPL的首字母）。然后，他又用B语言写出了UNICS操作系统，这就是后来风靡全世界的UNIX操作系统的初级版本。
<div><strong>精选留言（5）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/27/2c/b5/10141329.jpg" width="30px"><span>杰良</span> 👍（3） 💬（0）<div>C 语言与 UNIX 操作系统相互成就，可以说是比 UNIX 走得更远，尤其是在广阔的嵌入式领域。C 语言简洁有力的语法特点，能在小到单片机程序达到 Linux 操作系统上玩出花来。
当然，强大灵活的代价就是容易用错，误伤自己。包括遭受非法攻击的风险也是特别需要注意的。</div>2021-12-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/fd/79/edf06cd5.jpg" width="30px"><span>胡子拉差的我</span> 👍（0） 💬（1）<div>用的什么编译器？</div>2021-12-25</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/27/ac/bf/f549183e.jpg" width="30px"><span>=</span> 👍（2） 💬（0）<div>通篇读完，“有趣而有益”。
“有趣”是指在阅读中了解了与C语言相关的历史背景知识;“有益”是指开卷有益——指针的不良使用对于栈的破坏是我获得的新知识。
读完后开始期待(下)篇的内容。</div>2021-12-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/6b/10/22f93764.jpg" width="30px"><span>sky</span> 👍（1） 💬（4）<div>请教一下大家，陷阱三 代码中的*l— =(long)test;这里的test是在哪里定义的？</div>2021-12-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1d/0c/a5/0bbfd5e7.jpg" width="30px"><span>Tiger</span> 👍（0） 💬（0）<div>想问下LMOS老师，在“通过汇编代码看C语言的本质”一小节，那三段汇编代码是怎么得出来的？</div>2024-06-10</li><br/>
</ul>