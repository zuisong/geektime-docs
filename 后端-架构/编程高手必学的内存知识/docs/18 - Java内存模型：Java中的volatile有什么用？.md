你好，我是海纳。

随着这节课的开始，我们将进入到专栏的最后一个模块：**自动内存管理篇**。在这个模块，你将会了解到，以Java为代表的托管型语言是如何自动进行内存管理和回收整理的，这将提高你使用Java、Python、 Go等托管型语言的能力。

为什么我要把自动内存管理篇放到最后才讲呢？因为要理解这一篇的内容，需要软件篇和硬件篇的知识做铺垫。比如说，在面试时，有一个问题面试官问到的频率非常高，但几乎没有人能回答正确，因为它需要的前置知识太多。这个问题是：Java中的volatile有什么用？如何正确地使用它？

这个问题之所以会频繁出现在面试中，是因为Java并发库中大量使用了volatile变量，在JVM的研发历史上，它在各种不同的体系结构下产生了很多典型的问题。那么，在开发并发程序的时候，深刻地理解它的作用是非常有必要的。

幸运的是，前面硬件篇的知识已经帮我们打好了足够的基础，今天我们就可以深入讨论这个问题了。由于在这个问题中，volatile的语义是由Java内存模型定义的，我们就先从Java内存模型这个话题聊起。

## Java内存模型

我们知道在不同的架构上，缓存一致性问题是不同的，例如x86采用了TSO模型，它的**写后写（StoreStore）和读后读（LoadLoad）**完全不需要软件程序员操心，但是Arm的弱内存模型就要求我们自己在合适的位置添加StoreStore barrier和LoadLoad barrier。例如下面这个例子：
<div><strong>精选留言（13）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/14/99/f2/c74d24d7.jpg" width="30px"><span>大豆</span> 👍（9） 💬（6）<div>1、volatile不能代替锁，它的作用是绕过高速缓存，直接与内存进行交互并读写数据。
2、当多线程时，会存在线程A将新值写入内存前，线程B又从内存读取了旧值，这样就会导致sum的值不会是80000。
3、要想sum的值为80000，还得给Main.sum += 1;这句代码加锁。
4、volatile还有一个作用是防止指令重排，对吗？老师。</div>2021-12-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1b/b7/f0/380183ff.jpg" width="30px"><span>AriseFX</span> 👍（3） 💬（5）<div>请教一个问题，思考题如果使用CAS来更新sum的话，这里使用volatile关键字还有意义么，CAS不是已经包含了volatile读&#47;写的语义么？</div>2022-02-16</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1d/85/d2/045c63fb.jpg" width="30px"><span>王建新</span> 👍（2） 💬（1）<div>菜鸡求请教：acquire 语意，和release 语意 都代表什么，求解答。。</div>2021-12-15</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/62/28/0356880b.jpg" width="30px"><span>.</span> 👍（1） 💬（1）<div>volatile作用的自我总结：
1.给编译器看在编译层面禁止重拍
2.给虚拟机看让其在对应的指令加入屏障。防止cpu级别的重排序与缓存一致性问题

思考题:
这个问题就像++i问题类似，由于加一是由多个字节码才能完成（java虚拟机基于栈的设计尤其明显比安卓虚拟机完成一件事需要更多指令）。假设cpu1取出数据放入操作栈，还没进行计算操作，而此时时间片正好用完另线程cpu2完成一次加一，在切回cpu1时数据已经错误。

解决方案：

1.加锁保证多线程的串行
2.操作变成原子操作，如使用并发包下的原子类



老师能不能以后讲讲cpu之上的内存模型呢？比如arm</div>2021-12-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/18/39/d2/845c0e39.jpg" width="30px"><span>送过快递的码农</span> 👍（0） 💬（2）<div>我尝试对之前的知识和今天的文章我来梳理一下。volatile 关键字修饰的变量要遵循happen-bofore模型。由于cpu缓存的情况，我们会出现读滞后数据的情况。前面的知识，cpu通过缓存一致性协议，对缓存状态进行管理，一旦失效，会通过总线同步给其他核心。但是由于，这样性能成本太高，所以出现写缓存区+失效队列+内存屏障来进行补充？又由于我理解这个是jmm内存模型提出的规范，由于不同平台，不同cpu缓存架构不一样，cpu所提供的内存屏障实现也不一样。volatile关键字，虽说是可见性，但是也是集cpu，操作系统，jvm这些在不同层级上做自己的事情，方能实现。感觉也是现代计算机知识体系的一个精华（由于，前面很多看了不懂不懂，所以麻烦老师看看我的理解对不对，感觉这个也是要多刷的，不然越学越废）</div>2021-12-09</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTKtlEYuHnR8VdRkNPcmkIqTM9DKahpcpicDdBvcmBWMIAAhBrd0QNWvl09slqrzB5TibryVcIfPmb7Q/132" width="30px"><span>raisecomer</span> 👍（0） 💬（2）<div>“happen-before模型”的表格中“对volatile的写操作在对该变量的读操作之前执行”，太令人费解了</div>2021-12-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/d4/f3/129d6dfe.jpg" width="30px"><span>李二木</span> 👍（0） 💬（1）<div>volatile 只能保证可见性和有序性。不能保证原子性。</div>2021-12-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/59/0a/9b2126ac.jpg" width="30px"><span>anqi</span> 👍（2） 💬（0）<div>volatile 可以保证可见性，但无法保证原子性
因为数据可能在 寄存器或者 （store buffer + cpu cache + memory）组成的内存子系统中，
当在寄存器中时，如果发生中断，另一个线程仍然可以在上面的内存子系统中读到同样的值， 造成两次操作都是基于一个值做了自增操作，虽然刷新回内存的操作可以保证可见性，但已经于事无补了。</div>2022-05-30</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1b/b7/f0/380183ff.jpg" width="30px"><span>AriseFX</span> 👍（1） 💬（0）<div>思考题
 
public void run() {
        long sumOffset = UNSAFE.staticFieldOffset(Main.class.getDeclaredField(&quot;sum&quot;));
        for (int i = 0; i &lt; 40000; i++) {
            UNSAFE.getAndAddInt(Main.class, sumOffset, 1);
        }
    }</div>2022-02-16</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/cb/d5/fab32cf7.jpg" width="30px"><span>卖藥郎</span> 👍（0） 💬（0）<div>volatile 能替代锁（或者 CAS 操作）的能力吗？
答：不能。比如 i++，实际会包含读改写三个操作，T1从主存中读取值之后，由于没有原子性限制，主存中的值可能会在此刻发生变化。
不知道这样理解的对不对，望老师指正</div>2022-03-31</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/4f/7f/5dc11380.jpg" width="30px"><span>苏志辉</span> 👍（0） 💬（1）<div>怎么理解程序顺序规则和控制流依赖、数据流依赖，程序顺序规则不会让有数据依赖的禁止重排吗？</div>2022-02-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/11/fa/e0dcc1bf.jpg" width="30px"><span>榕</span> 👍（0） 💬（1）<div>而 Arm 上，由于存在单向的 barrier，所以 LoadLoad 和 LoadStore barrier 就可以使用 acquire load 代替，LoadStore 和 StoreStore barrier 也可以使用 release store 代替，而 StoreLoad barrier 就只能使用 dmb 代替了。

老师，本文以上描述跟第16课内存模型中以下描述有点不一致:

与 stlr 相对称的是，它同时具备 LoadLoad barrier 的能力和 StoreLoad barrier 的能力。在实际场景中，我们使用最多的还是 LoadLoad barrier，此时我们会使用 ldar 来代替。

16课中讲acquire load是具有LoadLoad barrier和StoreLoad barrier能力，但本文说LoadLoad 和 LoadStore barrier 就可以使用 acquire load 代替，而 StoreLoad barrier 就只能使用 dmb 代替了。这里有点搞不清了，麻烦老师解惑</div>2022-01-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/d4/f3/129d6dfe.jpg" width="30px"><span>李二木</span> 👍（0） 💬（0）<div>“JMM 是一种理论上的内存模型，并不是真实存在的”，那JMM是不是跟OSI七层模型一样了</div>2021-12-15</li><br/>
</ul>