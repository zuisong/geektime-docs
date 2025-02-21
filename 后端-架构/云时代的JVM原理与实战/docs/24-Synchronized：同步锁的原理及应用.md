你好，我是康杨。

Java 中的同步锁机制是 Java 并发编程的基础，它可以保证在多线程环境下对共享资源的互斥访问。在 Java 中，同步锁机制主要由 Synchronized 关键字实现。今天我将详细聊一聊同步锁的原理，以及在 JDK 源码中的应用，并给出最佳实践。

## 锁的状态与类型

Synchronized是Java中最具代表性的互斥同步手段之一，它在底层实现上并不依赖于Lock接口及其实现类。Synchronized 所依赖的是JVM内部的监视器锁（monitor）。在竞争程度较低的场景下，Synchronized 可以提供较高的性能。在JVM对Synchronized进行优化后，如使用偏向锁、轻量级锁等，能使其在无竞争和轻度竞争情况下避免重量级锁使用操作系统互斥量带来的性能消耗。

Synchronized 属于 JVM 的内置锁，Synchronized 方法或代码块在编译后，会在字节码层面有一对 **monitorenter 和 monitorexit 指令，分别表示获取锁和释放锁**。

当一个线程试图获取某个对象的监视器（也叫做监控锁或同步锁）时，它会执行 monitorenter 指令。这个指令会把对象引用加载到操作数栈中，然后尝试获取这个对象所指向的对象的锁。如果获取成功，那么这个线程将成为该对象的所有者，其他线程必须等待锁被释放才能获取。当线程退出同步代码块或调用 wait() 方法时，monitorexit 指令负责释放锁。
<div><strong>精选留言（4）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/10/25/87/f3a69d1b.jpg" width="30px"><span>peter</span> 👍（2） 💬（0）<div>请教老师几个问题：
Q1：锁的状态是怎么定义的？或者说怎么知道锁的状态？
Q2：偏向锁的对象是指谁？
“偏向锁会尝试获取该对象的锁” ，此处的“对象”是指谁？
Q3：偏向锁的单线程问题：
“向锁是一种针对单线程访问的优化手段”，怎么知道是单线程？谁判断的？既然是单线程，为啥还要加锁？（如果是单线程，不用加锁啊，当然也不用加偏向锁了啊）。
Q4：偏向锁，两个线程可以同时进入同步代码块吗？
“如果不是，则查看对象标记是否为可偏向，如果是，则尝试使用 CAS 将当前线程的 ID 记录在对象头中，如果成功，则执行同步代码。”，前面的句子，好像一个线程已经进入同步代码块了，这一句好像是另外一个线程也可以进入，这样的话，就有两个线程同时进入同步代码块了。
Q5：复制到新的栈帧是什么意思？
“当有其他线程尝试获取同一对象锁，此时 Mark Word 复制到新建的栈帧作为 Displaced Mark Word”，什么意思？
Q6：老师能否多画几个图？
画图来演示，更清楚。
Q7：ReentrantLock的例子不明白
A 代码和文字没有说明该锁的特点。 B “我们还看到 ReentrantLock 支持公平锁和非公平锁两种模式”，哪里看到了？
Q8：ReentrantReadWriteLock的例子，只有一个线程来读，能体现什么？</div>2023-10-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/60/a1/45ffdca3.jpg" width="30px"><span>静心</span> 👍（1） 💬（0）<div>从Java 6开始，JVM对Synchronized进行了大量优化，使得两者的性能差距大大缩小。在某些情况下，Synchronized的性能甚至优于ReentrantLock。</div>2024-02-04</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/b2/9c/b7b9896c.jpg" width="30px"><span>王云峰</span> 👍（1） 💬（0）<div>这个说的跟郑雨迪不一样，轻量级和重量级</div>2023-11-15</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/35/d5/17833946.jpg" width="30px"><span>八宝</span> 👍（0） 💬（0）<div>既然有了Synchronized，为何还会有ReentrantLock?   两者有啥区别？

在JDK21中， 虚拟线程等待Synchronized锁时会pinned平台线程，不能实现轻量级yield，所以不提倡使用Synchronized，21中标准库很多地方都用ReentrantLock替换了。
这个意义上讲，两者是等价可替换的。</div>2023-12-23</li><br/>
</ul>