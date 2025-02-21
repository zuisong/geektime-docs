你好，我是朱涛。今天，我们来聊聊Android的Jetpack。

在我看来，Kotlin和Jetpack，它们两个简直就是天生一对。作为Android开发者，如果只用Kotlin不用Jetpack，我们其实很难在Android平台充分发挥Kotlin的语言优势。而如果我们只用Jetpack而不用Kotlin，那么，我们将只能用到Jetpack的小部分功能。毕竟，Jetpack当中有很多API和库，是专门为Kotlin提供的。

经过前面课程内容的学习，相信现在你已经对Kotlin十分熟悉了，那么，接下来就让我们来看看Jetpack吧！这节课里，我会为你介绍Jetpack核心库的基本概念、简单用法，以及它跟Kotlin之间的关系，从而也为我们下节课的实战项目打下基础。

## Jetpack简介

Jetpack，它有“喷气式背包”的意思。对于我们开发者来说，它其实就是Google官方为我们提供的一套开发套件，专门用来帮助Android开发者提升开发效率、提升应用稳定性的。

[![](https://static001.geekbang.org/resource/image/ba/c2/ba1e45560e1e6510591d75ee6ee862c2.jpg?wh=600x600)](https://android-developers.googleblog.com/2019/05/whats-new-with-android-jetpack.html)

Android Jetpack，最初的宣传图标，就是“穿着喷气式背包的Android机器人”。大概意思就是：有了Jetpack，Android就能“起飞了”。这当然只是一种夸张的比喻，不过，从我实际的开发体验来说，Jetpack确实可以给Android开发者带来极大的好处，尤其是当Jetpack与Kotlin结合到一起的情况下。
<div><strong>精选留言（2）</strong></div><ul>
<li><img src="" width="30px"><span>Paul Shan</span> 👍（6） 💬（3）<div>思考题:viewModelScope是一个CloseableCoroutineScope，这个对象是懒加载的，第一次使用的时候才会创建，一旦创建以后，这个对象有一个close函数，会在ViewModel clear的时候调用，确保了viewModelScope的Coroutine scope和viewModel生命周期一致。了viewModelScope总体上和lifecycle的scope实现类似。区别是创建的时候，lifecycle用的是无锁+不断循环+compareAndSet方式，而viewModelScope实现的是synchronized带锁的方式，请问老师Android为什么会在两种类似的情况下采用不同的线程同步策略?</div>2022-04-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/06/96/4273bb09.jpg" width="30px"><span>遥远的救世主</span> 👍（0） 💬（3）<div>Android KTX 已经归档，不推荐使用了</div>2022-09-15</li><br/>
</ul>