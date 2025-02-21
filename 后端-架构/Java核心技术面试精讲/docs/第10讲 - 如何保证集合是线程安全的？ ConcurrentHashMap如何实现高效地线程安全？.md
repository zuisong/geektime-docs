我在之前两讲介绍了Java集合框架的典型容器类，它们绝大部分都不是线程安全的，仅有的线程安全实现，比如Vector、Stack，在性能方面也远不尽如人意。幸好Java语言提供了并发包（java.util.concurrent），为高度并发需求提供了更加全面的工具支持。

今天我要问你的问题是，如何保证容器是线程安全的？ConcurrentHashMap如何实现高效地线程安全？

## 典型回答

Java提供了不同层面的线程安全支持。在传统集合框架内部，除了Hashtable等同步容器，还提供了所谓的同步包装器（Synchronized Wrapper），我们可以调用Collections工具类提供的包装方法，来获取一个同步的包装容器（如Collections.synchronizedMap），但是它们都是利用非常粗粒度的同步方式，在高并发情况下，性能比较低下。

另外，更加普遍的选择是利用并发包提供的线程安全容器类，它提供了：

- 各种并发容器，比如ConcurrentHashMap、CopyOnWriteArrayList。
- 各种线程安全队列（Queue/Deque），如ArrayBlockingQueue、SynchronousQueue。
- 各种有序容器的线程安全版本等。

具体保证线程安全的方式，包括有从简单的synchronize方式，到基于更加精细化的，比如基于分离锁实现的ConcurrentHashMap等并发实现等。具体选择要看开发的场景需求，总体来说，并发包内提供的容器通用场景，远优于早期的简单同步实现。

## 考点分析

谈到线程安全和并发，可以说是Java面试中必考的考点，我上面给出的回答是一个相对宽泛的总结，而且ConcurrentHashMap等并发容器实现也在不断演进，不能一概而论。

如果要深入思考并回答这个问题及其扩展方面，至少需要：
<div><strong>精选留言（30）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/10/7c/8e/73581062.jpg" width="30px"><span>徐金铎</span> 👍（121） 💬（6）<div>需要注意的一点是，1.8以后的锁的颗粒度，是加在链表头上的，这个是个思路上的突破。</div>2018-05-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/4e/6b/abb7bfe3.jpg" width="30px"><span>Sean</span> 👍（54） 💬（2）<div>最近用ConcurrentHashMap的场景是，由于系统是一个公共服务，全程异步处理。最后一环节需要http rest主动响应接入系统，于是为了定制化需求，利用netty写了一版异步http clinet。其在缓存tcp链接时用到了。
看到下面有一位朋友说起了自旋锁和偏向锁。
自旋锁个人理解的是cas的一种应用方式。并发包中的原子类是典型的应用。
偏向锁个人理解的是获取锁的优化。在ReentrantLock中用于实现已获取完锁的的线程重入问题。
不知道理解的是否有误差。欢迎指正探讨。谢谢</div>2018-05-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/11/93/8b41390b.jpg" width="30px"><span>虞飞</span> 👍（27） 💬（1）<div>老师在课程里讲到同步包装类比较低效，不太适合高并发的场景，那想请教一下老师，在list接口的实现类中。在高并发的场景下，选择哪种实现类比较好？因为ArrayList是线程不安全的，同步包装类又很低效，CopyonwriteArrayList又是以快照的形式来实现的，在频繁写入数据的时候，其实也很低效，那这个类型该怎么选择比较好？</div>2018-05-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/65/69/efb57b83.jpg" width="30px"><span>Leiy</span> 👍（13） 💬（1）<div>我感觉jdk8就相当于把segment分段锁更细粒度了，每个数组元素就是原来一个segment，那并发度就由原来segment数变为数组长度？而且用到了cas乐观锁，所以能支持更高的并发，不知道我这种理解对吗？如果对的话，我就在想，为什么并发大神之前没想到这种，哈哈😄，恳请指正。谢谢</div>2018-05-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/1e/c6/6f817e6e.jpg" width="30px"><span>coder王</span> 👍（12） 💬（3）<div>您说的synchronized被改进很多很多了，那么在我们平常使用中，就用这个synchronized完成一些同步操作是不是OK？😁</div>2018-05-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/f8/ba/d28174a9.jpg" width="30px"><span>Geek_zbvt62</span> 👍（10） 💬（1）<div>这期内容太难，分寸不好把握
看8的concurenthashmap源码感觉挺困难，网上的博文帮助也不大，尤其是扩容这部分（似乎文章中没提）
求问杨大有没有什么窍门，或者有什么启发性的paper或文章？
可以泛化成，长期对lock free实现多个状态修改的问题比较困惑，希望得到启发</div>2018-05-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/fc/24/7d43d807.jpg" width="30px"><span>mongo</span> 👍（5） 💬（1）<div>请教老师：putVal方法中，什么情况下会进入else if ((fh=f.hash) == MOVED)分支？是进行扩容的时候吗？nextTable是做什么用的？</div>2018-05-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/fc/24/7d43d807.jpg" width="30px"><span>mongo</span> 👍（5） 💬（2）<div>请教老师：putVal方法的第二个if分支，为什么要用tabAt？我的认识里直接数组下标寻址tab[i=(n-1) &amp; hash]也是一个原子操作，不是吗？tabAt里面的getObjectVolatle（）方法跟直接用数组下标tab[i=(n-1) &amp; hash]寻址有什么区别？</div>2018-05-26</li><br/><li><img src="" width="30px"><span>Xg huang</span> 👍（4） 💬（1）<div>这里有个地方想跟老师交流一下想法, 从文中&quot;所以，ConcurrentHashMap 的实现是通过重试机制（RETRIES_BEFORE_LOCK，指定重试次数 2），来试图获得可靠值。如果没有监控到发生变化（通过对比 Segment.modCount），就直接返回，否则获取锁进行操作。&quot; 可以看出, 在高并发的情况下, &quot;size()&quot; 方法只是返回&quot;近似值&quot;, 而我的问题是: 既然只是一个近似值, 为啥要用这种&quot;重试,分段锁&quot; 的复杂做法去计算这个值? 直接在不加锁的情况下返回segment 的size 岂不是更简单? 我能理解jdk开发者想尽一切努力在高性能地返回最精确的数值, 但这个&quot;精确&quot; 度无法量化啊, 对于调用方来说,这个值依然是不可靠的啊. 所以, 在我看来,这种做法收益很小(可能是我也比较懒吧), 或者有些设计上的要点我没有领悟出来, 希望老师指点一下.</div>2018-06-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/3b/36/2d61e080.jpg" width="30px"><span>行者</span> 👍（3） 💬（1）<div>老师麻烦讲讲自旋锁，偏向锁的特点和区别吧，一直不太清楚。</div>2018-05-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/f0/35/a5ded70c.jpg" width="30px"><span>陈坤</span> 👍（2） 💬（1）<div>老师，cas操作有没有什么弊端呢？因为cas也很长一段时间了，根据您的经验，有弊端吗？</div>2018-11-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/86/b1/4b5d3a3b.jpg" width="30px"><span>宁宁</span> 👍（2） 💬（1）<div>在构造的时候，Segment 的数量由所谓的 concurrentcyLevel 决定，默认是 16！并发数不是越多越好吗？</div>2018-06-04</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/76/9d/6dab9e0e.jpg" width="30px"><span>Levy</span> 👍（2） 💬（1）<div>老师你好，tabAt里面的getObjectVolatle（）方法跟直接用数组下标tab[i=(n-1) &amp; hash]寻址有什么区别，这个我也不懂，volitile不是已经保证内存可见性吗？</div>2018-05-30</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/ab/10/b812ff3e.jpg" width="30px"><span>Hesher</span> 👍（2） 💬（1）<div>并发包用的很少，这一节内容的前置知识比较多，对于使用经验少的人来说貌似是有点难了。问题很好，正好可以见识一下各种使用场景，不过留言大部分是针对内容的难点提问，而真正回答问题的还没有出现。</div>2018-05-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/33/92/99530cee.jpg" width="30px"><span>灰飞灰猪不会灰飞.烟灭</span> 👍（2） 💬（1）<div>jdk7和8的区别感觉就是加锁不一样了，其他的没看懂。
老师，synchronized和lock是不是都是在类字节码种携带自旋锁和偏向锁啊？
他两底层区别是啥呢？我知道lock里面维护了一个双向链表</div>2018-05-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/7b/5b/907744cf.jpg" width="30px"><span>bazindes</span> 👍（1） 💬（1）<div>老师的内容讲的丰富 深入浅出 希望提高一下朗读人的要求吧 每节课都感觉有读错的 英文读不准就不说了 互斥读成互拆听的实在是别扭</div>2018-06-26</li><br/><li><img src="" width="30px"><span>极客cq</span> 👍（1） 💬（1）<div>不从实现上只从图形结构上看，ConcurrentHashMap和HashMap一样，不过是将buckets换成了segment，然后加锁方式从整map，下沉到segment（buckets）上，这样简单理解正确么？</div>2018-05-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/fa/10/cefb0e21.jpg" width="30px"><span>cuzz.</span> 👍（1） 💬（1）<div>有点不懂。。</div>2018-05-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/b1/20/8718252f.jpg" width="30px"><span>鲲鹏飞九万里</span> 👍（0） 💬（1）<div>好几个词感觉第一次见，大哭😹</div>2018-06-02</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/5b/fc/5c24080b.jpg" width="30px"><span>牛在天上飞</span> 👍（0） 💬（1）<div>老师能解释下可重入锁吗？</div>2018-06-01</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/fe/3c/13175251.jpg" width="30px"><span>Miaozhe</span> 👍（0） 💬（1）<div>杨老师，看到ConcurrentHashMap中有定义N CPU,想问问跟CPU什么关系？</div>2018-05-31</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/d6/6c/874ca8ad.jpg" width="30px"><span>George</span> 👍（0） 💬（1）<div>文中说的UNSAFE是什么意思？</div>2018-05-30</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/DYAIOgq83epTXXDNFFe90dwTK2s5PxeuYn3MOLvfU6YLQ0uxuf9bXI8dWXgib5LRnOwk1uWiaDHqIGibOKyU4x3CQ/132" width="30px"><span>Ethan</span> 👍（0） 💬（1）<div>请问老师以后会不会有讲线程中断的不同处理呢？这一块一直对我来讲都比较抽象而且不好测试</div>2018-05-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/ee/64/2646f6ef.jpg" width="30px"><span>胖</span> 👍（0） 💬（1）<div>如果多线程中已经在上层代码使用了读写锁进行访问控制，底层集合是否就可以使用HashMap，而没有必要使用线程安全的容器了？</div>2018-05-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/f8/e9/f25cce9e.jpg" width="30px"><span>李军</span> 👍（0） 💬（1）<div>可不可以用AI让JVM更智能？</div>2018-05-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/ad/4d/e24fc9e4.jpg" width="30px"><span>蔡光明</span> 👍（209） 💬（9）<div>1.7
put加锁
通过分段加锁segment，一个hashmap里有若干个segment，每个segment里有若干个桶，桶里存放K-V形式的链表，put数据时通过key哈希得到该元素要添加到的segment，然后对segment进行加锁，然后在哈希，计算得到给元素要添加到的桶，然后遍历桶中的链表，替换或新增节点到桶中

size
分段计算两次，两次结果相同则返回，否则对所以段加锁重新计算


1.8
put CAS 加锁
1.8中不依赖与segment加锁，segment数量与桶数量一致；
首先判断容器是否为空，为空则进行初始化利用volatile的sizeCtl作为互斥手段，如果发现竞争性的初始化，就暂停在那里，等待条件恢复，否则利用CAS设置排他标志（U.compareAndSwapInt(this, SIZECTL, sc, -1)）;否则重试
对key hash计算得到该key存放的桶位置，判断该桶是否为空，为空则利用CAS设置新节点
否则使用synchronize加锁，遍历桶中数据，替换或新增加点到桶中
最后判断是否需要转为红黑树，转换之前判断是否需要扩容

size
利用LongAdd累加计算</div>2018-07-04</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/9b/29/c50118cf.jpg" width="30px"><span>t</span> 👍（44） 💬（2）<div>对于我这种菜鸟来说，应该来一期讲讲volatile😭</div>2018-07-03</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/55/a1/ed52e319.jpg" width="30px"><span>j.c.</span> 👍（34） 💬（0）<div>期待unsafe和cas的文章</div>2018-05-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/15/02/66f65388.jpg" width="30px"><span>雷霹雳的爸爸</span> 👍（30） 💬（0）<div>今天这个纯粹知识盲点，纯赞，源码也得不停看</div>2018-05-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/e0/9f/9259a6b9.jpg" width="30px"><span>Kyle</span> 👍（10） 💬（3）<div>之前用JavaFX做一个客户端IM工具的时候，我将拉来的未被读取的用户聊天信息用ConcurrentHashMap存储（同时异步存储到Sqlite），Key存放用户id，Value放未读取的聊天消息列表。因为我考虑到存消息和读消息是由两个线程并发处理的，这两个线程共同操作一个ConcurrentHashMap。可能是我没处理好，最后直到我离职了还有消息重复、乱序的问题。请问我这种应用场景有什么问题吗?</div>2018-05-28</li><br/>
</ul>