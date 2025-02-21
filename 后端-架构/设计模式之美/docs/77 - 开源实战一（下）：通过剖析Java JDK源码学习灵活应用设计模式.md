上一节课，我们讲解了工厂模式、建造者模式、装饰器模式、适配器模式在Java JDK中的应用，其中，Calendar类用到了工厂模式和建造者模式，Collections类用到了装饰器模式、适配器模式。学习的重点是让你了解，在真实的项目中模式的实现和应用更加灵活、多变，会根据具体的场景做实现或者设计上的调整。

今天，我们继续延续这个话题，再重点讲一下模板模式、观察者模式这两个模式在JDK中的应用。除此之外，我还会对在理论部分已经讲过的一些模式在JDK中的应用做一个汇总，带你一块回忆复习一下。

话不多说，让我们正式开始今天的学习吧！

## 模板模式在Collections类中的应用

我们前面提到，策略、模板、职责链三个模式常用在框架的设计中，提供框架的扩展点，让框架使用者，在不修改框架源码的情况下，基于扩展点定制化框架的功能。Java中的Collections类的sort()函数就是利用了模板模式的这个扩展特性。

首先，我们看下Collections.sort()函数是如何使用的。我写了一个示例代码，如下所示。这个代码实现了按照不同的排序方式（按照年龄从小到大、按照名字字母序从小到大、按照成绩从大到小）对students数组进行排序。
<div><strong>精选留言（29）</strong></div><ul>
<li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTKELX1Rd1vmLRWibHib8P95NA87F4zcj8GrHKYQL2RcLDVnxNy1ia2geTWgW6L2pWn2kazrPNZMRVrIg/132" width="30px"><span>jxs1211</span> 👍（5） 💬（4）<div>文章中说Vector不是线程安全的，但是addElement和removeElement都是加了synchronized的呀，为什么不是线程安全的呢</div>2020-07-01</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/24/2a/33441e2b.jpg" width="30px"><span>汝林外史</span> 👍（5） 💬（8）<div>为什么说Vector不是线程安全的类呢？？ Vector的方法不都加了synchronize关键字实现串行化并发安全了吗，应该是线程安全的类啊。</div>2020-04-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/26/38/ef063dc2.jpg" width="30px"><span>Darren</span> 👍（68） 💬（1）<div>1、肯定会影响性能，但是因为保存观察者对象的必须是线程安全的，所以是不可避免，根据实际业务场景，如果很少被修改，可以使用CopyOnWriteArrayList来实现，但是如果修改频繁，CopyOnWriteArrayList 本质是写时复制，所以比较消耗内存，不建议使用，可以使用别的，比如ConcurrentSkipListSet等；
2、change是必须的，有些场景下（比如报警），状态发生变化其实是不报警，持续一定的时间菜报警，所以，把被观察者的对象是否发生变化独立出来，是可以做很多自己业务的事情；可以接单的理解为对变化抽象，提高可扩展性。</div>2020-04-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/47/31/f35367c8.jpg" width="30px"><span>小晏子</span> 👍（19） 💬（6）<div>思考题：
1. 每个函数加一把Synchronized锁，在并发激烈的时候是会影响性能的，优化的方式的话确实是可以使用CopyOnWriteList，copyOnWriteList是个并发安全的List，并且它不是基于锁实现的，而且又因为Oberser 中的List很少被修改经常被遍历的特点，所以使用CopyOnWriteList性能会提升。
2. changed成员变量还是必须的，这么做的好处是可以将“跟踪变化”和“通知观察者”两步分开，处理一些复杂的逻辑，</div>2020-04-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/a5/98/a65ff31a.jpg" width="30px"><span>djfhchdh</span> 👍（15） 💬（4）<div>1、方案一：使用性能更好的线程安全的容器，来替换vector；方案二：如果没有多线程添加、删除观察者的操作，而是在程序启动时就定义好了观察者，以后也不会变更的话，就不用给相关函数加锁了。              
2、changed成员不是多此一举，如果没有这个成员，notifyObservers()函数在多线程场景下，会出现重复通知观察者的情况。</div>2020-04-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/1e/71/54ff7b4e.jpg" width="30px"><span>3Spiders</span> 👍（10） 💬（1）<div>思考题

1，是否能用异步观察者模式，减少并发压力。

2，change必须，如果没有change，那在notifyObservers同步拷贝观察者对象进行通知时，如果这时候有新的变更，那被观察者又会被通知一次。</div>2020-04-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/50/d7/f82ed283.jpg" width="30px"><span>辣么大</span> 👍（8） 💬（1）<div>notifyObservers()这个方法写的巧妙呀！在高并发环境提高性能可以选择“折中“方案，控制锁的粒度。不禁感慨，人生面临的各种选择也是这样，也是各种妥协和折中。

使用cow遍历性能高，是因为不需要“复制”，它把复制的空间和时间开销，挪到了add之类的操作上，这也是一种折中。
</div>2020-05-04</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/17/27/ec30d30a.jpg" width="30px"><span>Jxin</span> 👍（5） 💬（1）<div>1.会，写多场景可以采用分治思想降低锁冲突，数据量不大且写少场景就采用cow拿空间换时间。

2.有这个change字段可能导致丢失通知的情况。并发多个线程发送通知，保障至少一个线程发送通知的场景可以用。</div>2020-04-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/be/e6/7808520d.jpg" width="30px"><span>Edward Lee</span> 👍（4） 💬（1）<div>课后思考
1. 使用 CopyOnWriteArrayList snapshot 方式提高性能
2. changed 变量是多此一举，在共享同一个 Observable 对象时，并发情况下甚至会出现通知丢失，这是因为 setChanged() 和 notifyObservers(args) 并不具备原子性，所以多个线程在 setChanged() 后都会被阻塞在 notifyObservers() 方法内，最终所有阻塞的线程都会全部通知失效。很多时候，像注册后通知就必须要能够通知到注册者，因此也不能容忍通知丢失的情况。</div>2020-05-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/19/d9/ff/b23018a6.jpg" width="30px"><span>Heaven</span> 👍（3） 💬（0）<div>
1.肯定降低了性能,而通常优化的手段,是更小粒度的锁或者使用乐观锁,在这个方法中已经将notifyObservers方法原本的大锁,利用一个复制技术缩小到一小点了,也是一种版本控制的方式,这里先给出一个尝试优化,使用原子类Boolean来替换setChanged这个大锁,并且使用copyonwriteArrayList来替换我们的数组
2.如果没有多并发的任何情况,changed的设计就是多此一举了,但是如果出现了高并发,那么直接去尝试直接执行更新操作可能会是一个非常漫长的等待,于是利用一个简单的标识位,并加上了锁来进行了修改,在高并发的情况下,无可厚非</div>2020-04-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/43/79/18073134.jpg" width="30px"><span>test</span> 👍（3） 💬（0）<div>1.会影响，如果要优化，可以使用CopyOnWriteArrayList；
2.有必要，如果没有change，则需要观察者知道被观测者什么时候会有状态改变。</div>2020-04-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1a/70/ac/83bc14c0.jpg" width="30px"><span>面向百度编程</span> 👍（2） 💬（0）<div>change是必须的，控制开关，并发控制。必须要锁啊，有并发，而且现在锁不是优化了么，偏向锁，自旋锁。真的影响很大么</div>2020-05-11</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTJETibDh9wrP19gj9VdlLRmppuG1FibI7nyUGldEXCnoqKibKIB18UMxyEHBkZNlf5vibLNeofiaN5U6Hw/132" width="30px"><span>steve</span> 👍（2） 💬（0）<div>2、changed 是在高并发的情况下减少重复通知的概率吧，不过也没法完全避免，是这样吗？</div>2020-05-06</li><br/><li><img src="" width="30px"><span>不能忍的地精</span> 👍（2） 💬（0）<div>1. 加同步关键字的方法操作内容简单,都是对容器进行操作和更改状态,所以影响有限,优化的方法可以是线程隔离.避免多线程操作共享变量的问题

2. changed变量不是多此一举,存在一种情况,就是被观察者行动了,但是条件不满足,但是不需要通知观察者的情况</div>2020-04-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/21/7e/fb725950.jpg" width="30px"><span>罗 乾 林</span> 👍（2） 💬（0）<div>1、会影响并发性能,synchronized主要保证Vector线程安全，高并发下会影响加入集合的速度，可以使用并发性好的无锁化容器
2、当多个线程同时发起notifyObservers时保证只通知Observer一次</div>2020-04-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/04/51/da465a93.jpg" width="30px"><span>超威丶</span> 👍（2） 💬（0）<div>先解决好并发问题，后续影响性能再做优化，没必要一上来就优化，优化也是对于锁的粒度优化</div>2020-04-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1d/5f/12/791d0f5e.jpg" width="30px"><span>mono176</span> 👍（1） 💬（0）<div>我认为这两个问题是有关联的。顺便杠下前几个热评...
原因是这里的synchronized并不是为了提升性能而作的，数组的copy是很快的,且观察者的添加删除相比并不频繁，没有必要引入相对重的CopyOnWriteArrayList，抛开场景谈优化没有任何意义。所以我觉得他的synchronized只是为了changed和这个vector能从主存读最新值，否则不加锁是一样的。

至于changed，读到最新值走到下面的clearChanged是能够避免一部分并发的重复通知但不能保证,比如0.5秒内的两个并发，第一个线程执行了1.set,2.通知,第二个线程又执行了1.set,2.通知那么如果也是重复请求,那么并不能避免。这个看自己怎么去定义重复。还有就是有人说参数不同,去重导致丢失通知，这个我认为确实是个坑，除非定义规范这个参数大家只是定义一个单例消息</div>2022-11-15</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1b/bb/41/2bcfff91.jpg" width="30px"><span>xxs</span> 👍（1） 💬（0）<div>看了下源码注释，感觉changed的设计直观来说是为了防止观察者可以触发通知的问题，从结果上看实现了延迟通知的功能。
1. notify()的时候将被观察者的对象传给了观察者，而notify是一个public方法，被观察者有权限调用，但若没有changed就会陷入死循环。
2. 相对应的setChange()是protected方法，被观察者没有权限调用。
3. notify()如果被设计成protected就不会有这个问题，但这样子灵活性就大幅降低，无法从外部主动发起notify()，例如定时通知。</div>2021-07-01</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/3a/f8/c1a939e7.jpg" width="30px"><span>君哥聊技术</span> 👍（1） 💬（0）<div>1.每个函数加synchronized，肯定会有性能影响的，尤其是高并发的情况下，会有大量现场阻塞在入口等待队列。对于非线程安全的操作，加锁不一定要在方法级别，可以在变量级别加锁，也可以用并发包下的一些安全类来取代synchronized
2.changed变量主要好处就是当通知的时候如果没有改变这个变量值，可以直接return。但是我觉得如果通知的时候，忘了set这个变量的值，那不是就相当于通知失败了吗？去掉changed我觉得也可以，保证被观察这在通知的时候，确实是有新消息到来或者有真实事件发生</div>2020-04-30</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/70/9e/9337ca8e.jpg" width="30px"><span>jaryoung</span> 👍（1） 💬（0）<div>课后习题：
1. 大量并发的时候会影响，但是在少量的并发的时候，其他影响会比较小，毕竟优化后的synchronized不是默认就是重量级锁。优化方案：更换为一些线程安全的集合类，changed 也可以更换为线程安全的AtomicBoolean，简单一句话，就是缩小锁的范围。
2. changed 算一个巧妙的设置吧，可能会存在需求暂时屏蔽某些主播（Observable）。
</div>2020-04-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/10/bb/f1061601.jpg" width="30px"><span>Demon.Lee</span> 👍（1） 💬（0）<div>1. 每个函数都加一把 synchronized 大锁，会不会影响并发性能？有没有优化的方法？
---查询资料，vector是jdk很早之前就有的，实现了线程安全，但性能很差，我觉得可以换成CopyOnWriteArrayList会好些，毕竟读多，写少一些。

2. changed 成员变量是否多此一举
---没想明白，不知道是不是防止滥用notifyObservers()方法，必须先设置标志位，然后再通知？看到有hasChanged()方法，难道是让Observer可以主动来检测数据是否变化了？</div>2020-04-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/25/5e/a4/d48b8298.jpg" width="30px"><span>Geek_sz</span> 👍（0） 💬（0）<div>一堆参差不齐的评论</div>2023-11-26</li><br/><li><img src="" width="30px"><span>Geek_f73a3e</span> 👍（0） 💬（0）<div>Collections的排序=====》List的排序========》数组的排序=======》数组元素的比较+交换=======》比较往往体现业务逻辑，是个变化点，被封装 为比较器 。排序时传入，。由于模板方法模式，需要抽象的模板类、内封装 模板方法和原生方法；客户继承模板类，实现原生方法；这里的应用场景中没有子类的产生；故不是模板方法模式，是回调机制 更好 </div>2023-08-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1b/bb/41/2bcfff91.jpg" width="30px"><span>xxs</span> 👍（0） 💬（0）<div>没看明白，changed有什么用，甚至感觉造成了消息丢失。
评论区有很多说有必要的，主要基于两个原因:
1. 有些变动不需要通知。这个逻辑就很奇怪，不需要通知就不要调用notice，为什么反而变成不调用change
2. 解决高并发下的重复通知。这个我对java不熟悉，可能理解不到位，没看出来哪里重复了。假设两个线程同时调用两个notice，那说明有两个事件需要通知，没有changed这个变量是正常的通知两个，有了changed变量反而因为原子性会有漏发一次的可能。
求大神解惑。</div>2021-07-01</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/26/e0/6f/7bd611db.jpg" width="30px"><span>橙粒</span> 👍（0） 💬（0）<div>Observable 类的33-34行能否移到synchronized 外面？  我理解只是对changed变量的读，并不存在线程安全问题。</div>2021-04-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1d/70/9f/741cd6a4.jpg" width="30px"><span>Henry</span> 👍（0） 💬（0）<div>1、可以将锁的范围缩小或者用快照的方式减小持有锁的时间；
2、多了一个change字段提供了状态变化而不通知的能力。当然也可以通过子类的控制实现，但是子类的代码就复杂了起来。所以，acceptable.</div>2020-11-11</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTK16hm4B3sbF0fbTTXrn0DhibaTOTLtygYFAcCmO8hdgz75jbSLjNk38AADIH6grmNzEaeGye0FiclA/132" width="30px"><span>Geek_bcac93</span> 👍（0） 💬（0）<div>既然对vector的add，remove等操作在外层都加了锁，为啥还要用vector这种重量容器，直接用array list这种轻量容器不就好了吗</div>2020-09-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/f9/aa/3e80212e.jpg" width="30px"><span>龙猫</span> 👍（0） 💬（0）<div>1、使用乐观锁替代如;cas算法，或者减小锁的粒度只有当使用或访问共享变量时加锁
2、changed成员变量是控制notifyObservers函数的开关，在并发条件下程序的执行的结果是可变的，加入开关变量可以控制并发问题。</div>2020-09-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/16/bd/e14ba493.jpg" width="30px"><span>翠羽香凝</span> 👍（0） 💬（1）<div>问题2：这里设置了一个change，实际上是为了多线程而设计的；

多线程模式下，最简单的方式是整个notifyObservers()函数加锁；
但是出于性能考虑，JDK采用了细粒度锁这种方式，仅仅对其中的一个代码块进行上锁；

当出现多个线程同时访问的时候，第一个线程在synchronized模块中，将change设置为false，然后后续的线程就不会再执行后面的update了。</div>2020-07-03</li><br/>
</ul>