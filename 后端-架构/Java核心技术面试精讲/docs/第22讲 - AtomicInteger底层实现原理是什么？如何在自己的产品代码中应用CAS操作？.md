在今天这一讲中，我来分析一下并发包内部的组成，一起来看看各种同步结构、线程池等，是基于什么原理来设计和实现的。

今天我要问你的问题是，AtomicInteger底层实现原理是什么？如何在自己的产品代码中应用CAS操作？

## 典型回答

AtomicIntger是对int类型的一个封装，提供原子性的访问和更新操作，其原子性操作的实现是基于CAS（[compare-and-swap](https://en.wikipedia.org/wiki/Compare-and-swap)）技术。

所谓CAS，表征的是一系列操作的集合，获取当前数值，进行一些运算，利用CAS指令试图进行更新。如果当前数值未变，代表没有其他线程进行并发修改，则成功更新。否则，可能出现不同的选择，要么进行重试，要么就返回一个成功或者失败的结果。

从AtomicInteger的内部属性可以看出，它依赖于Unsafe提供的一些底层能力，进行底层操作；以volatile的value字段，记录数值，以保证可见性。

```
private static final jdk.internal.misc.Unsafe U = jdk.internal.misc.Unsafe.getUnsafe();
private static final long VALUE = U.objectFieldOffset(AtomicInteger.class, "value");
private volatile int value;
```

具体的原子操作细节，可以参考任意一个原子更新方法，比如下面的getAndIncrement。

Unsafe会利用value字段的内存地址偏移，直接完成操作。

```
public final int getAndIncrement() {
    return U.getAndAddInt(this, VALUE, 1);
}
```

因为getAndIncrement需要返归数值，所以需要添加失败重试逻辑。
<div><strong>精选留言（30）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/11/1f/2f/e35d6a1d.jpg" width="30px"><span>I.am DZX</span> 👍（34） 💬（1）<div>CANCELLED 1 因为超时或中断设置为此状态，标志节点不可用
SIGNAL -1 处于此状态的节点释放资源时会唤醒后面的节点
CONDITION -2 处于条件队列里，等待条件成立(signal signalall) 条件成立后会置入获取资源的队列里
PROPAGATE -3 共享模式下使用，头节点获取资源时将后面节点设置为此状态，如果头节点获取资源后还有足够的资源，则后面节点会尝试获取，这个状态主要是为了共享状态下队列里足够多的节点同时获取资源
0 初始状态</div>2018-06-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/e3/57/e5de0216.jpg" width="30px"><span>Cui</span> 👍（20） 💬（6）<div>老师，看了AQS的实现原理后，我再回顾了您之前关于synchronized的文章，心中有些疑问：
1、synchronized在JVM中是会进行锁升级和降级的，并且是基于CAS来掌握竞争的情况，在竞争不多的情况下利用CAS的轻量级操作来减少开销。
2、而AQS也是基于CAS操作队列的，位于队列头的节点优先获得锁，其他的节点会被LockSupport.park()起来（这个好像依赖的是操作系统的互斥锁，应该也是个重量级操作）。
我觉得这两种方式都是基于CAS操作的，只是操作的对象不同（一个是Mark Word，一个是队列节点），当竞争较多时，还是不可避免地会使用到操作系统的互斥锁。然而，我再测试这两者的性能时，在无竞争的情况下，两者性能相当，但是，当竞争起来后，AQS的性能明显比synchronized要好（测试案例是8个线程并发对一个int递增，每个线程递增1000万次，AQS的耗时大概要少30%），这是为什么呢？</div>2018-06-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/0c/49/d71e939d.jpg" width="30px"><span>三口先生</span> 👍（17） 💬（1）<div>大于0取消状态，小于0有效状态，表示等待状态四种cancelled，signal，condition，propagate</div>2018-06-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/6e/84/45a909a6.jpg" width="30px"><span>卡斯瓦德</span> 👍（5） 💬（3）<div>老师请教个问题，acquireQueued的源代码中，使用for（；；）做了个自旋锁吧，作者为什么不用while（true），这种方式呢，是因为开销不一样吗？</div>2018-07-05</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/05/f3/4dd9e515.jpg" width="30px"><span>TonyEasy</span> 👍（3） 💬（1）<div>老师，说实话这一期的对我来说有点难度了，钦佩老师对知识理解的深入，请问老师可以指点下java学习的路线图吗，或者您分享下您自己的学习路线。</div>2018-06-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/dd/b6/fcf322a7.jpg" width="30px"><span>antipas</span> 👍（2） 💬（2）<div>看AQS源码过程中产生了新问题，它对线程的挂起唤醒是通过locksupport实现的，那么它与wait&#47;notify又有何不同，使用场景有何不同。我的理解是使用 wait&#47;notify需要synchronized锁，而且wait需要条件触发</div>2018-06-26</li><br/><li><img src="" width="30px"><span>Geek_qomxrt</span> 👍（0） 💬（1）<div>LongAdder这里，说要考虑紧凑性的影响，不清楚指的是哪方面的考虑</div>2019-01-26</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTI2icbib62icXtibTkThtyRksbuJLoTLMts7zook2S30MiaBtbz0f5JskwYicwqXkhpYfvCpuYkcvPTibEaQ/132" width="30px"><span>xuanyuan</span> 👍（152） 💬（5）<div>建议；

1. 希望能有推外内存的主题，范型部分希望能与cpp比较讲解。
2. 一些主题如果已经有公开的比较好的资料，可以提供链接，对重点强调即可。希望能看到更多公开资料所没有的信息，这也是老鸟们付费的初衷。
同意的点赞</div>2018-06-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/8a/fc/d1dd57dd.jpg" width="30px"><span>ipofss</span> 👍（38） 💬（4）<div>这一讲对于我来说，挺有难度的，还是基础比较薄弱，整体上没太听懂。老师对于Java的理解真是太深入了，等我以后技术精进了，再回来看看老师的36讲，应该会有新的认识。继续往下听吧，已经懂点的加深理解，没听过的就当是听了名字以后用到了再仔细研究</div>2018-08-07</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/07/5a/abb7bfe3.jpg" width="30px"><span>OneThin</span> 👍（16） 💬（3）<div>能否出一节讲一下unsafe，感觉这个才是最基础的。另外unsafe为什么叫unsafe呢</div>2018-07-16</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/MdmRMTV2IwvQZF2IO0G0CFWbKxT9CIibmcdicS3J4SmrA4P1e36jCwyXZpia06ItwP4GibGnCrPJHicBbd5y9libTpiaA/132" width="30px"><span>^_^</span> 👍（8） 💬（1）<div>要讲AQS的话，这点篇幅远远不够。推荐b站寒食君AQS的讲解，很详细。</div>2021-02-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/20/39/3168c4ca.jpg" width="30px"><span>二木🐶</span> 👍（7） 💬（3）<div>一直很好奇，为何CAS指令在发现内容未变的时候就能判断没有其他线程修改呢？可能被修改后的值与比较的值一样呀</div>2018-06-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/04/b5/8bc4790b.jpg" width="30px"><span>Geek_987169</span> 👍（4） 💬（0）<div>老师，您说的&quot;更加紧凑&quot;，是什么意思？不太理解</div>2019-03-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/14/b1/7d974f0a.jpg" width="30px"><span>黄明恩</span> 👍（4） 💬（0）<div>老师可否分析下Object.wait和notify的原理</div>2018-06-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/e9/29/629d9bb0.jpg" width="30px"><span>天王</span> 👍（2） 💬（0）<div>22 AutomicInteger原理是什么，cas原理，cas操作怎么应用 1 Automic提供了对int类型的原子操作和更新，操作基于cas原理，cas全称Compare and Swap， cas的原理是操作前试图获取当前值，在操作时，看值是否改变，如果未改变，代表没有其他线程同步修改，操作成功，已经改变，返回操作失败或者重试。有2个属性 jdk.internal.misc.Unsafe u＝idk.internal.misc.Unsafe.getUnsafe(); volatile int value;Long VALUE＝U.objectFiledOffset(AutomicInter.Class,&quot;value&quot;); Unsafe会利用value字段的内存地址偏移完成操作 2 cas底层实现 依赖于CPU底层提供的指令，java提供了2个公共api支持cas操作，long tid＝Thread.currenThread().getId(); AutomicFiledUpdator.compareAndSet(this,0l,tid);Automic包提供了很多原子处理类，是很多原子操作的选择，java.9以后提供了 Variable Hand Api， private static final VarHandle handle 首先获取句柄，再调用cas方法，推荐使用Variable Handle Api，后续维护有保障，3 AQS AbstractQueueSynchronized 是实现各种同步结构的基础</div>2020-01-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/d4/f3/129d6dfe.jpg" width="30px"><span>李二木</span> 👍（2） 💬（0）<div>最近遇到配置tomcat连接池，导致cpu过高问题，最后发现配置连接池数过大导致上下文切换次数过多
，也就是线程池中任务数过少，空闲的线程过多，我想问为什么会导致上下文切换过多？</div>2018-06-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/43/14/8e2b48fb.jpg" width="30px"><span>Maxonor Love Muz 🎈</span> 👍（1） 💬（0）<div>老师把原理讲的差不多了，不过光看原理就以为自己会了，那是浅层次的理解。 有必要 把AQS源码走一遍</div>2020-05-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/76/48/5ab89daa.jpg" width="30px"><span>护爽使者</span> 👍（1） 💬（0）<div>cas  是乐观锁，while 循环</div>2020-03-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/17/61/c2/1da88a93.jpg" width="30px"><span>今天</span> 👍（1） 💬（0）<div>听起来还是很有难度的，我基础有点差</div>2020-03-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/88/93/26076028.jpg" width="30px"><span>七个猪</span> 👍（1） 💬（0）<div>CAS有部分实现是解决ABA问题，可以讲一下ABA问题是如何解决的，除了version外，还有没有其他的方式</div>2018-07-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/58/5d/8de7f8dc.jpg" width="30px"><span>爱新觉罗老流氓</span> 👍（1） 💬（1）<div>ReentrantLock的非公平锁，其实只有一次非公平的机会！那一次就是在lock方法中，非公平锁的实现有if else分支，在if时就进行一次cas state，成功的线程去执行任务代码去了。那么失败的线程就会进入else逻辑，就是AQS#acquired，从这里开始非公平锁和公平锁就完全一样了，只是公平锁被欺负了一次，它的lock方法是直接调acquired方法。

为什么只有这一次呢？先看AQS#acquired，第一个逻辑是tryAcquired，公平锁和非公平锁实现略有区别。但记住，在这个时刻下，即使你看到公平锁trtAcquired实现中多一个hasQueuedPredecessors判断，无关紧要，重要的是这个时刻，还没有执行后面的addWaiter逻辑，根本没有入队，那么公平锁进入这个hasXXX方法，当然也是马上出来，执行后面的cas state，跟非公平锁没有不同...

如果，AQS#acquired的第一个tryAcquired失败了，都会进入acquiredQueued，此方法中有个强制的逻辑，就是无限for循环中的 final Node p = node.predecessors(); 在这个逻辑下，非平锁锁也要乖乖排队......

以上只是分析了lock方法，带超时的tryLock方法还没有具体看代码。如果我的lock分析有误，欢迎指出批评！</div>2018-06-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/22/d9/05/0d772dbf.jpg" width="30px"><span>咦</span> 👍（0） 💬（0）<div>建议CAS系列可以讲到操作系统实现原理，这样整体更加连贯一些</div>2021-09-04</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/19/41/4d/f6d6d13a.jpg" width="30px"><span>啊良梓是我</span> 👍（0） 💬（0）<div>我看了一下源码  好像acquireQueued(final Node node, int arg) 方法里面的循环递归条件好像是在shouldParkAfterFailedAcquire(p, node) 方法里面？</div>2021-05-06</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/1c/6e/6c5f5734.jpg" width="30px"><span>终结者999号</span> 👍（0） 💬（0）<div>从CAS到AQS，可以说AQS是靠大量CAS操作来进行的，以便完成各种同步需求。但是在自己产品中如何使用CAS更多是靠各种同步包中的同步容器？</div>2020-02-29</li><br/><li><img src="" width="30px"><span>Paul Shan</span> 👍（0） 💬（0）<div>CAS适用的场景是多数修改都成功，少数不成功的修改靠增加CPU来轮询，也就是说只有CPU轮询付出的代价足够小才经济。</div>2019-11-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/3b/65/7a01c8c8.jpg" width="30px"><span>Nights</span> 👍（0） 💬（1）<div>行尾注释不建议吧</div>2019-11-20</li><br/><li><img src="" width="30px"><span>亮灯</span> 👍（0） 💬（0）<div>老师，您好， shouldParkAfterFailedAcquire表示是否挂起当前线程，为什么要有这个判断？这个判断有什么用？</div>2019-10-15</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/e3/f4/ecb33aef.jpg" width="30px"><span>流光</span> 👍（0） 💬（2）<div>老师,您的倒数第二个方法是非公平说的获取方法没问题,最后的acquireQueued()是公平锁的获取方法,前天面试就被面试官喷了</div>2019-07-03</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/46/90/a2b206e9.jpg" width="30px"><span>Pine</span> 👍（0） 💬（0）<div>请教老师一个问题，基本类型前面加volatile，大概能明白什么意思。 可加在引用类型前面就不是很明白了？</div>2019-04-30</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/64/86/f5a9403a.jpg" width="30px"><span>yang</span> 👍（0） 💬（0）<div>关于状态的其他童鞋已经说啦，  

AQS的Node中包含了 Thread和waitStatus，也就是链表中需要获取锁的线程吧～！</div>2019-04-28</li><br/>
</ul>