你好，我是Mike。

这门课目前已接近尾声，剩下的两节课我准备讲讲Rust中看起来有点黑魔法的部分——Unsafe Rust。这一节课我们先来聊聊相关的概念。

在前面课程的学习中，你有没有感觉到，Rust编译器就像是一个严厉的大师傅，或者一个贴心的小助手，在你身边陪你结对编程，你写代码的时候，他盯着屏幕，时不时提醒你。如果某个时刻，这个大师傅或小助手突然离开了，你会不会慌？就像刚提车，第一次独自上路的那种感觉。

## 三个王国

Unsafe Rust 就是这样一个领域，进入这个领域，你突然拥有了几种必杀技能，但是身边已经没有大师傅同行了，只能靠你自己完全控制这几种技能的使用。使用得好，威力无穷。使用不好，对自己也会造成巨大伤害。Unsafe Rust就是这样一个相对独立的领域。前面我们讲到过，Async Rust也是相对独立的一个附属王国，现在又多了一个Unsafe Rust这样的附属王国。

![图片](https://static001.geekbang.org/resource/image/f7/88/f71d96faf019a6e0dc3f4291cf251f88.jpg?wh=1003x683)

Rust语言可以看作是这三块疆域的合体，它们共同组成了一个联盟Rust王国。你甚至可以把Rust语言看成包含上面三种编程语言的一种混合语言。所以很多人抱怨Rust难学，也是可以理解的。

现在让我们把注意力集中在Unsafe Rust这个王国里面。它到底是什么样的？简单地说，你可以把它理解成这个王国里面住着一个C语言族的国王。也就是说，C语言能做的事情，Unsafe Rust都能做。C语言能做哪些事情呢？理论上来说，它能做计算机中的任何事情。因此，在Unsafe Rust中，你也能做计算机中的任何事情。C的强大威力来源于它锋利的指针，而在Unsafe Rust中也提供了这种能力。
<div><strong>精选留言（4）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/1e/36/33/3411df0d.jpg" width="30px"><span>seven9t</span> 👍（5） 💬（1）<div>unsafe改名叫trustMe多好</div>2024-01-21</li><br/><li><img src="" width="30px"><span>Geek_03197d</span> 👍（2） 💬（1）<div>raw pointer 翻译成 裸指针 是不是更通用？</div>2024-02-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/38/a0/06/f0ca94ca.jpg" width="30px"><span>Apa琦</span> 👍（2） 💬（2）<div>tokio库也是用unsafe实现的么，rust自己没有实现Async，也就只能使用unsafe调用c语言库实现了</div>2024-01-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/ac/5f/894761f8.jpg" width="30px"><span>十八哥</span> 👍（2） 💬（0）<div>Unsafe Rust 比 C 语言更安全吗？是的。虽然是Unsafe，可以用指针。但是，Unsafe依然属于所有权这样的语法范畴。</div>2023-12-29</li><br/>
</ul>