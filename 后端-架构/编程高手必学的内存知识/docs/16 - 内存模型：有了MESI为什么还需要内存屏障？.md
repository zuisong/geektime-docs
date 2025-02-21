你好，我是海纳。

上一节课，我们学习了MESI协议，我们了解到，MESI协议能够解决多核 CPU体系中，多个CPU之间缓存数据不一致的问题。但是，如果CPU严格按照MESI协议进行核间通讯和同步，核间同步就会给CPU带来性能问题。既要遵守协议，又要提升性能，这就对CPU的设计人员提出了巨大的挑战。

那严格遵守MESI协议的CPU会有什么样的性能问题呢？我们又可以怎么来解决这些问题呢？今天我们就来仔细分析一下。搞清楚了这些问题，你会对C++内存模型和Java内存模型有更加深入的理解，在分析并发问题时能够做到有的放矢。

## 严守MESI协议的CPU会有啥问题？

我们上节课说过，MESI代表的是Modified、Exclusive、Shared、Invalid这四种缓存状态，遵守MESI协议的CPU缓存会在这四种状态之间相互切换。这种CPU缓存之间的关系是这样的：

![](https://static001.geekbang.org/resource/image/1d/57/1dabf3dccd6113d76b29c05dd3ea3c57.jpg?wh=2284x1407)

从上面这张图你可以看到，Cache和主内存(Memory)是直接相连的。一个CPU的所有写操作都会按照真实的执行顺序同步到主存和其他CPU的cache中。

严格遵守MESI协议的CPU设计，在它的某一个核在写一块缓存时，它需要通知所有的同伴：我要写这块缓存了，如果你们谁有这块缓存的副本，请把它置成Invalid状态。Invalid状态意味着该缓存失效，如果其他CPU再访问这一缓存区时，就会从主存中加载正确的值。
<div><strong>精选留言（24）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/0f/a6/b6/27412d76.jpg" width="30px"><span>sc</span> 👍（25） 💬（2）<div>CPU 从单核发展为多核，增加缓存，导致出现了多个核间的缓存一致性问题 --&gt; 为了解决缓存一致性问题，提出了 MESI 协议 --&gt; 完全遵守 MESI 又会给 CPU 带来性能问题 --&gt; CPU 设计者又增加 store buffer 和 invalid queue --&gt; 又导致了缓存的顺序一致性变为了弱缓存一致性 --&gt; 需要缓存的顺序一致性的，就需要软件工程师自己在合适的地方添加内存屏障</div>2021-12-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/62/28/0356880b.jpg" width="30px"><span>.</span> 👍（8） 💬（5）<div>我看了一些文献关于X86（total store ordering ）加上自己的理解：

1）由于不存在invalidate queue且读和读之间不会重排序切读线程会先读取store buffer，因此LoadLoad屏障在x86是无用的
2）由于store buffers是采用队列且不同地址的写是不会重排序因此StoreStore 可不存在
3）读可以与之前同位置排序，但不能与非同位置重排序（我在wiki搜不到这个屏障多线程问题，关于这个多线程实际应用场景不明确） LoadStore也没有了意义
4）但是写可能与之前的读重排序因此需要特别考虑这种重排序，StoreLoad存在意义 且存在可行性问题（但是老师说TSO不存在缓存一致性我不大理解这个在StoreLoad是否也是成立）</div>2021-12-06</li><br/><li><img src="" width="30px"><span>shenglin</span> 👍（6） 💬（1）<div>思考题实例代码使用fullFence()正确性是可以保证的，只是性能下降？

&#47;&#47; CPU0
void foo() {
    a = 1;
    unsafe.storeFence();
    b = 1;
}

&#47;&#47; CPU1
void bar() {
    while (b == 0) continue;
    unsafe.loadFence();
    assert(a == 1);
}
可以改成这样？因为由于store buffer的存在，foo()函数要a的新值写入缓存之后，b的新值才能写入，所以要使用storeFence屏障； bar()函数要读取b和a的新值，且由于invalid_queue的存在，要加入loadFence保证读取到a的新值前invalid_queue的消息已经被处理完成，即将CPU1的缓存中的a值更新。这样即保证了正确性，又兼顾了性能，不知道这样理解对不对？</div>2021-12-03</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/e2/86/90041355.jpg" width="30px"><span>一塌糊涂</span> 👍（5） 💬（1）<div>必须赞，看过很多资料，唯一能讲明白的！大神推荐点资料吧。</div>2021-12-03</li><br/><li><img src="" width="30px"><span>Vvin</span> 👍（3） 💬（1）<div>你好！请问:如果在有store buffer的情况！cup0 and cpu1都写同一个状态为shared的a变量，怎么处理？</div>2021-12-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/d8/71/d6f79534.jpg" width="30px"><span>一个工匠</span> 👍（1） 💬（2）<div>在正常的程序中，多个 CPU 一起操作同一个变量的情况是比较少的，所以 store buffer 可以大大提升程序的运行性能。

这一块不是很理解，单个cpu操作同一个变量不就不需要mesi了么？所以mesi就是处理多核数据读写不一致问题而存在的，并且可以解决。但是优化之后，又不可以解决了，并且要让开发人员添加屏障进一步解决。那是不是可以理解mesi最后还是没完成“多核缓存一致性”工作？</div>2022-02-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1e/b3/32/0ee78a1a.jpg" width="30px"><span>陈狄</span> 👍（1） 💬（1）<div>请问老师，「内存屏障的作用是屏障前面的读写未完成，不会进行屏障后面的读写」，怎么判断store buffer，尤其是invalid queue里的数据是屏障前面未完成的读写？</div>2022-01-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/a0/57/c78b489b.jpg" width="30px"><span>BlockQuant</span> 👍（0） 💬（1）<div>“CPU0 在得到这个确认消息以后，就可以独占该缓存了，直接将这块缓存变为 Modified 状态，然后把 a 写入。在 a 写入以后，foo 函数中的内存屏障就可以顺利通过了，接下来就可以写入变量 b 的新值。由于 b 是 Exclusive 的”  这个 b 为啥是 E 状态，CPU1也在用，不应该是 S 吗？</div>2021-12-07</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/8f/cf/890f82d6.jpg" width="30px"><span>那时刻</span> 👍（0） 💬（1）<div>请问老师，内存屏障对于其它语言，比如go，是否是一致的呢？ 对于其它语言，读写屏障可以保证代码的执行顺序是一致的</div>2021-12-07</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/DYAIOgq83er6OV33jHia3U9LYlZEx2HrpsELeh3KMlqFiaKpSAaaZeBttXRAVvDXUgcufpqJ60bJWGYGNpT7752w/132" width="30px"><span>dog_brother</span> 👍（0） 💬（1）<div>老师，这里说的内存屏障跟c++11的memory order是一回事么？</div>2021-12-06</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/d7/bb/dd4442ba.jpg" width="30px"><span>Stormouble</span> 👍（0） 💬（1）<div>有个问题想请问一下，在乱序执行下，不是会保证按原有顺序提交吗（ROB）？那么为什么还会导致赋值顺序被打乱呢？</div>2021-12-06</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/62/28/0356880b.jpg" width="30px"><span>.</span> 👍（0） 💬（1）<div>思考题：
给b加上volatile修饰，从而触发java的happen before 原则，这个原则我记得没错也有靠内存屏障实现</div>2021-12-06</li><br/><li><img src="" width="30px"><span>shenglin</span> 👍（0） 💬（1）<div>请问一下， StoreStore barrier, LoadStore barrier, LoadLoad barrier, StoreLoad barrier具体含义是什么</div>2021-12-03</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/cd/ed/825d84ee.jpg" width="30px"><span>费城的二鹏</span> 👍（0） 💬（1）<div>思考题第一瞬间想到的就是 volatile 结果它不是答案。</div>2021-12-03</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/28/04/8c/d8b757e0.jpg" width="30px"><span>蝉沐风</span> 👍（2） 💬（1）<div>作者写得太棒了！推荐一下https:&#47;&#47;www.chanmufeng.com&#47;posts&#47;concurrency&#47;%E7%BC%93%E5%AD%98%E4%B8%80%E8%87%B4%E6%80%A7%E4%B8%8E%E5%86%85%E5%AD%98%E5%B1%8F%E9%9A%9C.html，希望能帮到大家</div>2022-09-01</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/f8/ba/d28174a9.jpg" width="30px"><span>Geek_zbvt62</span> 👍（0） 💬（0）<div>感觉看得更糊涂了，比如介绍stlr具有 StoreStore 和 LoadStore 的功能，stlr是单向屏障，是否意味着StoreStore也是单向？(因为如果StoreStore是双向，那不可能“具有”）。但从文章中意思，大概能推导出StoreStore有双向的效果，就是在屏障&quot;前&#47;后&quot;的写操作不会移动到&quot;后&#47;前&quot;去
</div>2023-09-08</li><br/><li><img src="" width="30px"><span>Geek_369ed5</span> 👍（0） 💬（0）<div>老师,&#47;&#47; CPU0void foo() { a = 1; b = 1;}&#47;&#47; CPU1void bar() { while (b == 0) continue; assert(a == 1);}这个程序会出现缓存一致性问题的前提是不是在多线程下执行才会有问题,如果在单线程在main方法里跑是不是不会有多个CPU执行这个程序,也就不会有问题,只有在多线程下跑才会有多个CPU参与进来执行这个程序,也就有了缓存一致性问题?望老师解答一下,万分感谢</div>2023-02-03</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1d/e7/8e/318cfde0.jpg" width="30px"><span>Spoon</span> 👍（0） 💬（0）<div>1.问题一：关于stlr与ldar指令，ARM文档中并没有说指出LoadStore&#47;StoreStore&#47;LoadLoad&#47;StoreLoad这种语义-&gt;
https:&#47;&#47;developer.arm.com&#47;documentation&#47;den0024&#47;a&#47;Memory-Ordering&#47;Barriers&#47;One-way-barriers
2.问题二：在ARM中有个Share Domain的概念，对于STLR与LDAR在文档中也没有具体指明，作者有了解吗？</div>2023-01-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/19/7e/08/a50945c3.jpg" width="30px"><span>muzigef</span> 👍（0） 💬（0）<div>对这节课的感触有两点：内存模型设计的核心思想是lazy，拖到最后才去处理；从内存模型的角度，更深刻的理解内存屏障</div>2022-11-08</li><br/><li><img src="" width="30px"><span>Geek_dd538f</span> 👍（0） 💬（0）<div>引用：
“但是在 Share 状态下，如果一个核想独占缓存进行修改，就需要先给所有 Share 状态的同伴发出 Invalid 消息，等所有同伴确认并回复它“Invalid acknowledgement”以后，它才能把这块缓存的状态更改为 Modified，这是保持多核信息同步的必然要求。”

如果是两个核同时要独占缓存呢？互相等待同伴确认并回复，这样就造成死锁了吗？</div>2022-11-02</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/24/f6/e4/7ad3bba6.jpg" width="30px"><span>FRANK-MA</span> 👍（0） 💬（2）<div>通过mesi协议本身 是不是可以解决线程锁之间的问题了？比如多个线程同时操作A变量 cpu0 写完A以后 直接把cpu1的A 设置成invaild了. 哪为什么像java这些语言还需要加锁呢？加锁难道也是内存屏障的一种 用来解决store buffer 和invalid queue的 读写问题？</div>2022-05-01</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/3a/27/5d218272.jpg" width="30px"><span>八台上</span> 👍（0） 💬（1）<div>想问一下在程序中使用各种锁锁，和本节讲的内存屏障有什么关系吗</div>2021-12-05</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/62/28/0356880b.jpg" width="30px"><span>.</span> 👍（0） 💬（0）<div>我总算等到这节课。。。。。。。。老师打算就java方面出类似的教程吗？在这块网上的比较零散。</div>2021-12-03</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/4d/bb/abb7bfe3.jpg" width="30px"><span>csyangchsh</span> 👍（0） 💬（0）<div>这篇文章很棒，如果执行过程加上图示九更好了。</div>2021-12-03</li><br/>
</ul>