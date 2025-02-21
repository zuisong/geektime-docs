你好，我是康杨。

今天我们来聊聊线程安全的另一种经典实现：ThreadLocal。在正式学习之前，我想先给你讲个故事，希望这个故事能帮你体会到ThreadLocal背后的设计思想。

![图片](https://static001.geekbang.org/resource/image/94/af/94ca3ebb79aaea2b9e2778dd244a83af.png?wh=1920x1102)

这个故事其实体现了ThreadLocal的设计原理。我们都知道，在多线程编程中，如果多个线程共享同一个变量，而没有应用类似乐观锁、悲观锁的同步机制时，很容易出现线程安全问题。

![图片](https://static001.geekbang.org/resource/image/26/64/2682695f1698d0aa58e05fb0f4565964.jpg?wh=1920x789)

就像图中 a 的值，最终到底是1还是2完全是不可预知的，在没有同步机制的情况下，它既可能是1也可能是2。而ThreadLocal绕过了线程间如何竞争一个变量的惯常思路，**通过为每个线程提供一个线程独享的变量副本的方式**，**以用空间换时间的思想从另一个角度解决了线程安全问题。**而这也是我们日常解决问题时可以借鉴的一种思想，当用通常的方式似乎无解的时候，也许换个视角，思路就完全打开了，借用古人的一句诗就是“行到水穷处，坐看云起时”。

在这个故事中，每个人独立的晾衣空间就相当于 ThreadLocal，晾衣空间中的衣服就相当于线程中的变量。每个人只能用自己的晾衣空间，也只能晾晒自己的衣服，从而避免了衣服被拿错的情况。当然，任何事情都是一体两面，为了解决线程安全的问题我们引入了ThreadLocal，但是对于 ThreadLocal 的误用又会带来其他风险，比如内存泄漏。
<div><strong>精选留言（2）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/14/35/d5/17833946.jpg" width="30px"><span>八宝</span> 👍（0） 💬（0）<div>遇到复杂问题时，通过多视角拆解，将复杂问题简单化的方式。点赞！
想到了数学中的3视图，一个角度看不到全貌，多个角度分析问题，层能更全面</div>2023-12-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/25/87/f3a69d1b.jpg" width="30px"><span>peter</span> 👍（0） 💬（0）<div>ThreadLocal虽然是多个线程之间各自有一个备份，但ThreadLocal的出现还是因为有共享变量，那多个线程之间最终还是需要同步这个共享变量吗？</div>2023-10-28</li><br/>
</ul>