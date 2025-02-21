你好，我是宫文学。

通过前面8节课的学习，我们实现了对浮点数、字符串、数组、自定义对象类型和函数类型的支持，涵盖了TypeScript的一些关键数据类型，也了解了实现这些语言特性所需要的一些关键技术。

在这些数据类型中，字符串、数组、class实例，还有闭包，都需要从堆中申请内存，但我们目前还没有实现内存回收机制。所以，如果用我们现在的版本，长时间运行某些需要在堆中申请内存的程序，可能很快会就把内存耗光。

所以，接下来的两节课，我们就来补上这个缺陷，实现一个简单的内存管理模块，支持内存的申请、内存垃圾的识别和回收功能。在这个过程中，你会对内存管理的原理产生更加清晰的认识，并且能够自己动手实现基本的内存管理功能。

那么，首先我们要分析一下内存管理涉及的技术点，以此来确定我们自己的技术方案。

## 内存管理中的技术点

计算机语言中的内存管理模块，能够对内存从申请到回收进行全生命周期的管理。

内存的申请方面，一般不会为每个对象从操作系统申请内存资源，而是要提供自己的内存分配机制。

而垃圾回收技术则是内存管理中的难点。垃圾回收有很多个技术方案，包括标记-清除、标记-整理、停止-拷贝和自动引用计数这些基础的算法。在产品级的实现里，这些算法又被进一步复杂化。比如，你可以针对老的内存对象和新内存对象，使用不同的回收算法，从而形成分代管理的方案。又比如，为了充分减少由于垃圾收集所导致的程序停顿，发展出来了增量式回收和并行回收的技术。
<div><strong>精选留言（5）</strong></div><ul>
<li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTIicr82CnrdEjibibAvyeKRQHszSzIAqoCWxN0kqC442XcjEae6S9j6NDtKLpg4Da4CUQQeUFUicWqiaDw/132" width="30px"><span>有学识的兔子</span> 👍（2） 💬（0）<div>.asciz 代表以&quot;\0&quot;作为结束符的字符串； .p2align代表数据边界需要满足对齐的字节倍数；.quad:代表大数，8字节的整数； 
要数据区写4个字节整数，是不是类似如下，声明数据段然后填入数据？
 .section __DATA,__const
 .globl _foo.meta    ## can be accessed globally
 .p2align 2     ## 4 byte alignment
_foo.meta:
 .word _val  ##4字节整数</div>2021-11-07</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/23/7f/24/ceab0e7b.jpg" width="30px"><span>奋斗的蜗牛</span> 👍（1） 💬（0）<div>.asciz用来声明字符串，.p2align用来声明下一条指令所在位置的对齐要求，.quad声明8字节的数</div>2021-11-02</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/92/0b/2ccf7908.jpg" width="30px"><span>...</span> 👍（1） 💬（0）<div>是否选择使用C语言编写才需要考虑内存管理 使用JS编译的话内存管理会由JS完成</div>2021-11-02</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/23/7f/24/ceab0e7b.jpg" width="30px"><span>奋斗的蜗牛</span> 👍（1） 💬（0）<div>这节课知识量很大，看来汇编语言还是很重要</div>2021-11-01</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/26/eb/d7/90391376.jpg" width="30px"><span>ifelse</span> 👍（0） 💬（0）<div>学习打卡</div>2022-09-29</li><br/>
</ul>