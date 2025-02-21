你好，我是宫文学。

基于Graal IR进行的优化处理有很多。但有些优化，针对Java语言的特点，会显得更为重要。

今天这一讲，我就带你来认识两个对Java来说很重要的优化算法。如果没有这两个优化算法，你的程序执行效率会大大下降。而如果你了解了这两个算法的机理，则有可能写出更方便编译器做优化的程序，从而让你在实际工作中受益。这两个算法，分别是**内联和逃逸分析**。

另外，我还会给你介绍一种JIT编译所特有的优化模式：**基于推理的优化**。这种优化模式会让某些程序比AOT编译的性能更高。这个知识点，可能会改变你对JIT和AOT的认知，因为通常来说，你可能会认为AOT生成的机器码速度更快，所以通过这一讲的学习，你也会对“全生命周期优化”的概念有所体会。

好，首先，我们来看看内联优化。

## 内联（Inlining）

内联优化是Java JIT编译器非常重要的一种优化策略。简单地说，内联就是把被调用的方法的方法体，在调用的地方展开。这样做最大的好处，就是省去了函数调用的开销。对于频繁调用的函数，内联优化能大大提高程序的性能。

**执行内联优化是有一定条件的。**第一，被内联的方法要是热点方法；第二，被内联的方法不能太大，否则编译后的目标代码量就会膨胀得比较厉害。
<div><strong>精选留言（5）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/12/c5/e5/fbacb7bf.jpg" width="30px"><span>😐饲养员小张😐</span> 👍（5） 💬（2）<div>老师，能讲讲不同语言混编的时候，编译器到底会怎么做么？ 最近在做swift和objc的混编的事情，有点没搞明白，如果主工程是objc引入swift文件，和主工程是swift引入objc文件有什么区别么？ 还有两种语言是怎么做到识别对方的呢？像编辑器的代码补全和报错都是怎么识别的呢？毕竟这时候还没有真正的编译啊！ 感谢老师</div>2020-07-07</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTKdzXiawss5gGiax48CJGAJpha4pJksPia7J7HsiatYwjBA9w1bkrDicXfQz1SthaG3w1KJ2ibOxpia5wfbQ/132" width="30px"><span>chris</span> 👍（2） 💬（1）<div>请教老师图1图2中的黑线和绿线是什么意思</div>2020-07-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/8c/58/abb7bfe3.jpg" width="30px"><span>易昊</span> 👍（0） 💬（1）<div>“它的具体做法是，在运行时，编译器会统计在调用多态方法的时候，到底用了哪几个实现。”这个是否有一定程度限制条件，比如我的程序运行在别人的虚拟机上，应该就统计不到了吧？</div>2020-07-07</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/2d/92/287f99db.jpg" width="30px"><span>lion_fly</span> 👍（1） 💬（0）<div>多态内联：Inlining of Virtual Methods。
老师这篇论文的连接失效了</div>2021-03-12</li><br/><li><img src="" width="30px"><span>jack123</span> 👍（0） 💬（2）<div>内联的第二个代码
“inlining方法” 打漏了，应该是“inlingingTest方法”

还有在内联优化的第1个部分--加载本地变量
一般我们使用getter和setter是因为想要封装外界直接对成员变量的访问，但是编译器这里直接加载私有字段，打破了private，在编译器层面是怎么做到的呢？或者说private关键词在Java编译器层面是怎么实现的呢，只是通过一个语法糖？还是底层就无法通过对象的offset偏移找到它的成员变量呢？</div>2021-10-09</li><br/>
</ul>