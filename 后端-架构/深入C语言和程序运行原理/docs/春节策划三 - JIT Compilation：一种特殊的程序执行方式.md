你好，我是于航。

这是最后一篇春节加餐了，今天我想和你分享的是一篇我之前写过的文章。这篇文章主要介绍了什么是 JIT Compilation 技术，以及如何使用 C++ 语言来实现一个简单的 JIT 编译器。

之所以跟你分享这篇文章，是因为编译器一直是 C 和 C++ 等语言可以大显身手的重要基础软件领域。同时，因为 JIT 是一种特殊的程序执行流程，了解它还能够为我们后续深入理解程序运行原理打下一定基础。并且，通过这篇文章，你能够大致感受到 C 和 C++ 这两种语言在使用上的差异。后面我还会专门写一篇比较 C 和 C++ 的特别放送，用专门的一讲来向你介绍它们在多个方面的异同。

在之前的版本基础上，结合最近写专栏时的思考，我对这篇文章进行了部分迭代和更新。并且，为了方便你理解文章的主要内容，当遇到 C++ 的专有特性时，我也会为你简单介绍。希望这篇文章对你有帮助，如果你有任何问题或者疑惑，欢迎在评论区给我留言，我们一起交流讨论。

**以下是文章正文部分。**

通过这篇文章，我希望能够让你了解到以下这些内容：

- 什么是 JIT Compilation 技术？它有哪些特性？
- 如何使用 C++ 在不依赖任何框架的情况下实现一个简单的 JIT Compiler？

而限于篇幅和话题范围，本文不会涉及以下这些内容：
<div><strong>精选留言（3）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/13/14/66/70a6a206.jpg" width="30px"><span>后视镜</span> 👍（3） 💬（1）<div>这个JIT Compilation看起来和协程的原理有点像，不知道老师有空再详细讲讲协程的实现呢？</div>2022-02-04</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/23/a8/df/f3eaf89e.jpg" width="30px"><span>i Love 3🍀</span> 👍（1） 💬（2）<div>没太明白JIT Compilation为啥会有这么明显的性能优化？</div>2022-02-06</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/52/40/e57a736e.jpg" width="30px"><span>pedro</span> 👍（2） 💬（1）<div>好文，期待后续！</div>2022-02-06</li><br/>
</ul>