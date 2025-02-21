你好，我是海纳。

我们前面几节课主要是以Java为例，介绍了JVM中垃圾回收算法的演进过程。实际上，除了JVM之外，用于运行JavaScript的V8虚拟机、Lua虚拟机、Python虚拟机和Go的虚拟机都采用了自动内存管理技术。这节课，我们就一起来分析一下它们的实现。

通过这节课，你将会看到垃圾回收算法的设计是十分灵活而且多种多样的，这会为你以后改进应用中自动或半自动的内存管理，提供很好的参考。你要注意的是，学习自动内存管理，一定要抓住核心原理，不要陷入到细节里去。另外，你可以通过查看虚拟机源代码来验证自己的猜想，但不要把源代码教条化。

接下来，我先解释一下为什么选择Python和GO这两种语言做为例子。

## 静态语言和动态语言

我先介绍两个基本概念：**动态语言和静态语言**。动态语言的特征是可以在运行时，为对象甚至是类添加新的属性和方法，而静态语言不能在运行期间做这样的修改。

动态语言的代表是Python和JavaScript，静态语言的代表是C++。Java本质上是一门静态语言，但它又提供了反射（reflection）的能力为动态性开了一个小口子。

从实现的层面讲，静态语言往往在编译时就能确定各个属性的偏移值，所以编译器能确定某一种类型的对象，它的大小是多少。这就方便了在分配和运行时快速定位对象属性。关于静态语言的对象内存布局，我们在[导学（三）](https://time.geekbang.org/column/article/431373)和[第19节课](https://time.geekbang.org/column/article/465516)都做了介绍，你可以去看看。
<div><strong>精选留言（6）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/10/cd/ed/825d84ee.jpg" width="30px"><span>费城的二鹏</span> 👍（4） 💬（1）<div>最后一集课程啦，感谢老师的细致讲解！
思考题，我猜一下值类型的优点吧，值类型都在栈上分配，随用随释放，有利于减少gc压力。</div>2021-12-22</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTI3lW3z0JqBDeM5S12SNsNAq6eEcHUYwFLuLsW96exY0kKicShGU6DIoqEibOMV8ialTae55icCvx1TFw/132" width="30px"><span>夏</span> 👍（0） 💬（1）<div>请问下老师，go垃圾回收过程中mutator assists的任务和目的是什么，谢谢</div>2022-01-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/8f/cf/890f82d6.jpg" width="30px"><span>那时刻</span> 👍（5） 💬（1）<div>请问老师，有了值类型的介入，编译器只需要关注函数内部的逃逸分析（intraprocedural escape analysis），而不用关注函数间的逃逸分析。 为什么有值类型介入后，就不需要关注函数间逃逸分析了呢？</div>2021-12-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/17/56/ff/cb2aa0a8.jpg" width="30px"><span>愣锤</span> 👍（1） 💬（0）<div>老师讲的真好，我为什么没有V8的垃圾回收详细教程呢？或者有没有推进？</div>2022-04-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/b8/d8/f81b5604.jpg" width="30px"><span>hcyycb</span> 👍（1） 💬（0）<div>正在学习Go语言，很开心在这节课明白了Go的内存管理机制。</div>2022-01-01</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/05/92/b609f7e3.jpg" width="30px"><span>骨汤鸡蛋面</span> 👍（0） 💬（0）<div>请问下go的虚拟内存布局和三级内存管理如何结合起来看呢</div>2022-07-12</li><br/>
</ul>