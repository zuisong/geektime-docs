你好，我是戴铭。今天，我来和你聊聊 iOS 是怎么管理内存的。

不同的系统版本对 App 运行时占用内存的限制不同，你可以利用我在第14篇文章中提到的方法，去查看不同版本系统对App占用内存的具体限制是多少。另外，系统版本的升级也会增加占用的内存，同时App功能的增多也会要求越来越多的内存。

然而，移动设备的内存资源是有限的，当App运行时占用的内存大小超过了限制后，就会被强杀掉，从而导致用户体验被降低。所以，为了提升App质量，开发者要非常重视应用的内存管理问题。

移动端的内存管理技术，主要有 GC（Garbage Collection，垃圾回收）的标记清除算法和苹果公司使用的引用计数方法。

相比较于 GC 标记清除算法，引用计数法可以及时地回收引用计数为0的对象，减少查找次数。但是，引用计数会带来循环引用的问题，比如当外部的变量强引用 Block时，Block 也会强引用外部的变量，就会出现循环引用。我们需要通过弱引用，来解除循环引用的问题。

另外，在 ARC（自动引用计数）之前，一直都是通过 MRC（手动引用计数）这种手写大量内存管理代码的方式来管理内存，因此苹果公司开发了 ARC 技术，由编译器来完成这部分代码管理工作。但是，ARC依然需要注意循环引用的问题。
<div><strong>精选留言（8）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/16/31/a9/28fa245b.jpg" width="30px"><span>ColdMountain</span> 👍（10） 💬（0）<div>内存就是 那边程序员自我修养 书里面说的 前两章节 看了两遍 收获很大</div>2019-06-01</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/57/c4/0fcdad37.jpg" width="30px"><span>刘儒勇</span> 👍（3） 💬（1）<div>“虚拟页大小是 16K，那么虚拟页最多能有 2^48 &#47; 2^14 = 16M 个，物理内存为 16G 对应物理页个数是 2^64 &#47; 2^14 = 524k 个。”

2^48&#47;2^14&#47;2^30 = 16 G个虚拟内存页
物理内存16G ，2^34&#47;2^14 = 2^20 = 1M 个</div>2020-09-27</li><br/><li><img src="" width="30px"><span>Geek_467f30</span> 👍（1） 💬（0）<div>&quot;程序生成的汇编代码会放在代码段。&quot;
是机器码吧</div>2021-09-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/35/5e/7a584fed.jpg" width="30px"><span>accessory</span> 👍（1） 💬（1）<div>您好，对于虚拟页和物理页的映射图，进程1的虚拟页vp5和进程2的虚拟页vp4映射到同一个物理页pp2不会有问题嘛？</div>2020-02-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/3f/9b/f626552c.jpg" width="30px"><span>阳光黑1</span> 👍（0） 💬（0）<div>MLeaksFinder在某个VC pop或dismiss后两秒会调用一个方法，如果能调用就说明该VC没有被释放掉</div>2020-11-30</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/ff/79/3b38c9e1.jpg" width="30px"><span>nil</span> 👍（0） 💬（0）<div>unix like的os，kernel设计真的是经过千锤百炼，设计精妙且高效，叹服前辈们。沉淀下来的基本就是最佳实践，或者说在满足已有限制下的比较合理的trade-off</div>2020-08-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/3e/19/873abe8a.jpg" width="30px"><span>董尚斌</span> 👍（0） 💬（6）<div>您好，请教个问题。望回复。
iOS采用的是引用计数，在开启ARC的情况下，我在一个花括号里面申请的变量出了花括号是不是意味着会被编译器自动加入release的释放代码，即保证在引用计数归0自动dealloc。
那为啥还需要@autoreleasepool{...} 这样的逻辑，我直接使用花括号{}不就可以了吗[c 里面对于出栈的会自动释放]，希望能明白我的意思。
{}出了这个花括号作用域之外，oc的对象不就自动销毁了吗？那为啥还要@autoreleasepool{}
</div>2020-04-01</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/6c/cb/8a41f8ce.jpg" width="30px"><span>Bill</span> 👍（0） 💬（0）<div>哈哈程序员自我修养里见过😬</div>2019-06-04</li><br/>
</ul>