我在[上一讲](http://time.geekbang.org/column/article/8799)对比和分析了synchronized和ReentrantLock，算是专栏进入并发编程阶段的热身，相信你已经对线程安全，以及如何使用基本的同步机制有了基础，今天我们将深入了解synchronize底层机制，分析其他锁实现和应用场景。

今天我要问你的问题是 ，synchronized底层如何实现？什么是锁的升级、降级？

## 典型回答

在回答这个问题前，先简单复习一下上一讲的知识点。synchronized代码块是由一对儿monitorenter/monitorexit指令实现的，Monitor对象是同步的基本实现[单元](https://docs.oracle.com/javase/specs/jls/se10/html/jls-8.html#d5e13622)。

在Java...
<div><strong>精选留言（30）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/0f/77/b3/991f3f9b.jpg" width="30px"><span>公号-技术夜未眠</span> 👍（193） 💬（2）<div>自旋锁:竞争锁的失败的线程，并不会真实的在操作系统层面挂起等待，而是JVM会让线程做几个空循环(基于预测在不久的将来就能获得)，在经过若干次循环后，如果可以获得锁，那么进入临界区，如果还不能获得锁，才会真实的将线程在操作系统层面进行挂起。

适用场景:自旋锁可以减少线程的阻塞，这对于锁竞争不激烈，且占用锁时间非常短的代码块来说，有较大的性能提升，因为自旋的消耗会小于线程阻塞挂起操作的消耗。
如果锁的竞争激烈，或者持有锁的线程需要长时间占用锁执行同步块，就不适合使用自旋锁了，因为自旋锁在获取锁前一直都是占用cpu做无用功，线程自旋的消耗大于线程阻塞挂起操作的消耗，造成cpu的浪费。</div>2018-06-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/6e/ff/bcbfae67.jpg" width="30px"><span>yearning</span> 👍（82） 💬（5）<div>这次原理真的看了很久，一直鼓劲自己，看不懂就是说明自己有突破。

下面看了并发编程对于自旋锁的了解，同时更深刻理解同步锁的性能。

自旋锁采用让当前线程不停循环体内执行实现，当循环条件被其他线程改变时，才能进入临界区。

由于自旋锁只是将当前线程不停执行循环体，不进行线程状态的改变，所以响应会更快。但当线程不停增加时，性能下降明显。
线程竞争不激烈，并且保持锁的时间段。适合使用自旋锁。

为什么会提出自旋锁，因为互斥锁，在线程的睡眠和唤醒都是复杂而昂贵的操作，需要大量的CPU指令。如果互斥仅仅被锁住是一小段时间，
用来进行线程休眠和唤醒的操作时间比睡眠时间还长，更有可能比不上不断自旋锁上轮询的时间长。

当然自旋锁被持有的时间更长，其他尝试获取自旋锁的线程会一直轮询自旋锁的状态。这将十分浪费CPU。

在单核CPU上，自旋锁是无用，因为当自旋锁尝试获取锁不成功会一直尝试，这会一直占用CPU，其他线程不可能运行，
同时由于其他线程无法运行，所以当前线程无法释放锁。

混合型互斥锁， 在多核系统上起初表现的像自旋锁一样， 如果一个线程不能获取互斥锁， 它不会马上被切换为休眠状态，在一段时间依然无法获取锁，进行睡眠状态。

混合型自旋锁，起初表现的和正常自旋锁一样，如果无法获取互斥锁，它也许会放弃该线程的执行，并允许其他线程执行。

切记，自旋锁只有在多核CPU上有效果，单核毫无效果，只是浪费时间。


以上基本参考来源于：
http:&#47;&#47;ifeve.com&#47;java_lock_see1&#47;
http:&#47;&#47;ifeve.com&#47;practice-of-using-spinlock-instead-of-mutex&#47;</div>2018-06-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/d6/60/f21b2164.jpg" width="30px"><span>jacy</span> 👍（38） 💬（4）<div>看了大家对自旋锁的评论，我的收获如下:
1.基于乐观情况下推荐使用，即锁竞争不强，锁等待时间不长的情况下推荐使用
2.单cpu无效，因为基于cas的轮询会占用cpu,导致无法做线程切换
3.轮询不产生上下文切换，如果可估计到睡眠的时间很长，用互斥锁更好
</div>2018-06-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/32/3f/fa4ac035.jpg" width="30px"><span>sunlight001</span> 👍（32） 💬（1）<div>自旋锁是尝试获取锁的线程不会立即阻塞，采用循环的方式去获取锁，好处是减少了上下文切换，缺点是消耗cpu</div>2018-06-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/fe/3c/13175251.jpg" width="30px"><span>Miaozhe</span> 👍（25） 💬（3）<div>杨老师，偏斜锁有什么作用？还是没有看明白，如果只是被一个线程获取，那么锁还有什么意义？
另外，如果我有两个线程明确定义调用同一个对象的Synchronized块，JVM默认肯定先使用偏斜锁，之后在升级到轻量级所，必须经过撤销Revoke吗？编译的时候不会自动优化？</div>2018-06-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/96/5e/8bba3a8a.jpg" width="30px"><span>陈一嘉</span> 👍（13） 💬（1）<div>自旋锁 for(;;)结合cas确保线程获取取锁</div>2018-06-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/33/92/99530cee.jpg" width="30px"><span>灰飞灰猪不会灰飞.烟灭</span> 👍（9） 💬（1）<div>老师 AQS就不涉及用户态和内核态的切换了 对吧？</div>2018-06-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/ff/70/9329316e.jpg" width="30px"><span>stephen chow</span> 👍（7） 💬（1）<div>StampLock是先试着读吧？你写的先试着修改。。</div>2018-10-01</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/fe/3c/13175251.jpg" width="30px"><span>Miaozhe</span> 👍（6） 💬（1）<div>关于自旋转锁不适合单核CPU的问题，下来查找了一下资料:
1.JVM在操作系统中是作为一个进程存在，但是OS一般都将将线程作为最小调度单位，进程是资源分配的最小单位。这就是说进程是不活动的，只是作为线程的容器，那么Java的线程是在JVM进程中，也被CPU调度。
2.单核CPU使用多线程时，一个线程被CPU执行，其它处于等待轮巡状态。
3.为什么多线程跑在单核CPU上也比较快呢？是由于这种线程还有其它IO操作(File,Socket)，可以跟CPU运算并行。
4.结论，根据前面3点的分析，与自旋转锁的优点冲突：线程竞争不激烈，占用锁时间短。</div>2018-06-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/fe/3c/13175251.jpg" width="30px"><span>Miaozhe</span> 👍（5） 💬（1）<div>杨老师，看到有回复说自旋锁在单核CPU上是无用，感觉这个理论不准确，因为Java多线程在很早时候单核CPC的PC上就能运行，计算机原理中也介绍，控制器会轮巡各个进程或线程。而且多线程是运行在JVM上，跟物理机没有很直接的关系吧？</div>2018-06-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/ce/b3/804aa247.jpg" width="30px"><span>大熊</span> 👍（4） 💬（3）<div>老师，请问下为什么要有读锁？读不会改变数据为什么还要加锁呢</div>2018-10-16</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/e3/57/e5de0216.jpg" width="30px"><span>Cui</span> 👍（4） 💬（1）<div>老师你好 心中一直有个疑问：synchronize和AQS的LockSupport同样起到阻塞线程的作用，这两者的区别是什么？能不能从实现原理和使用效果的角度说说？</div>2018-06-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/63/14/06eff9a4.jpg" width="30px"><span>Jerry银银</span> 👍（3） 💬（1）<div>『其逻辑是先试着修改，然后通过 validate 方法确认是否...』    
这里面先试着修改写错了，小编帮忙改下吧，应该是：『其逻辑是先试着读，然后....』 我看到留言中，有其它同学早就提出了，但是一直没有被修正。。。。</div>2019-02-02</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/fc/e5/605f423f.jpg" width="30px"><span>肖一林</span> 👍（3） 💬（1）<div>重量级锁还是互斥锁吗？自旋锁应该是线程拿不到锁的时候，采取重试的办法，适合重试次数不多的场景，如果重试次数过多还是会被系统挂起，这种情况下还不如没有自旋锁。</div>2018-06-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/15/02/66f65388.jpg" width="30px"><span>雷霹雳的爸爸</span> 👍（2） 💬（1）<div>今天老师讲这个真够我喝一壶的，而且老师总结的角度启发性很大，最近也再读JCIP，对比起来很有意思，对于自旋锁这个理解，我一直还是蛮肤浅的，顾名思义比较多，就是在那里兜几个圈子——写个循环——试几次，好处是减少线程切换导致的开销，一般也需要有底层有CAS能力的构件支持一下，比如用Atomic开头那些类，当然也未必，比如说nio读不出来东西的时候，也先尝试几次，总之就是暂时不把cpu让度出去，先在占着坑来几次，大概可能这么个意思吧</div>2018-06-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/1f/2f/e35d6a1d.jpg" width="30px"><span>I.am DZX</span> 👍（1） 💬（1）<div>请问自旋锁和非公平获取锁是不是有点冲突了</div>2018-06-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/f8/4d/4b748ff1.jpg" width="30px"><span>THROW</span> 👍（1） 💬（1）<div>StampedLock那里乐观读锁好像是说写操作不需要等待读操作完成，而不是&quot;读操作并不需要等待写完成&quot;吧</div>2018-06-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/f4/d9/e572ae4d.jpg" width="30px"><span>食指可爱多</span> 👍（1） 💬（1）<div>以前写过自旋锁的实现，当某个线程调用自旋锁实例的lock方法时，使用cas进行设置，cas（lockThread, null, currentThread）,也就是当前无锁定时当前线程会成功,失败则循环尝试直到成功。利用cas保证操作的原子性，成员变量lockThread设置为volatile保证并发时线程间可见性。所以从机制上可以看到，若是在高并发场景，成功拿到锁之外的所有线程会继续努力尝试持有锁，造成CPU资源的浪费。如评论中其它同学所说适合在低并发场景使用。</div>2018-06-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/6e/a3/bec136c0.jpg" width="30px"><span>cxzm</span> 👍（1） 💬（1）<div>杨老师，操作系统的互斥锁要怎么理解</div>2018-06-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/59/c9/f44cb7f3.jpg" width="30px"><span>爪哇夜未眠</span> 👍（1） 💬（1）<div>老师后面会详细讲 AQS 吗</div>2018-06-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/c0/71/c83d8b15.jpg" width="30px"><span>一个坏人</span> 👍（0） 💬（3）<div>老师好，请教一下：“自动内存管理系统为什么要求对象的大小必须是8字节的整数倍？”，即内存对齐的根本原因在于？</div>2018-08-25</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/fe/3c/13175251.jpg" width="30px"><span>Miaozhe</span> 👍（0） 💬（1）<div>杨老师，StampedSample这个例子，access方法是不是写错了？
long stamp = sl.tryOptimisticRead();
Data data = read();
应该是先判断tryOptimisticRead的结果，如果获取了所，才进入Read()吧？因为没有获取锁的读，可能是脏读。
自己代码调试，发现即使try Optimistic的结果为0, 也会向下执行read().

</div>2018-06-15</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/DYAIOgq83eqqQYBLvb0h2SjjZpRFicPb6LHWflobgRs8gicBn5N3QIEUnpJDmaRxUMvTJ1nZfmNwZ7L6Cq71R2YA/132" width="30px"><span>Geek_e61ae8</span> 👍（0） 💬（1）<div>老师讲到读写锁，这里涉及到读并发高，当我更改要加载的数据，这时需要写，读到内存后准备切换，但是一直获取不了写锁。这种采用自己boolean值来控制，让读sleep等待，或者直接返回不进锁（已经获取读锁的线程等处理结束）。写获取锁后更新，替换boolean值。另一种采用公平锁。老师觉得建议那种？</div>2018-06-13</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/DYAIOgq83eqqQYBLvb0h2SjjZpRFicPb6LHWflobgRs8gicBn5N3QIEUnpJDmaRxUMvTJ1nZfmNwZ7L6Cq71R2YA/132" width="30px"><span>Geek_e61ae8</span> 👍（0） 💬（1）<div>这块老师讲了读写锁，如果读并发高，当配置更改，触发了写，但是又获取不了锁，这种情况可以采用boolean值自己控制当写完，替换内存时，让读的线程等待。（已经获取锁的等处理完）没处理的等待。 这种是建议加上公平锁好，还是说自己控制好</div>2018-06-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/f5/2f/56117bab.jpg" width="30px"><span>张玮(大圣)</span> 👍（0） 💬（1）<div>自旋锁类似和忙等待一个套路</div>2018-06-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/f3/9f/3e4e8d46.jpg" width="30px"><span>tyson</span> 👍（0） 💬（1）<div>简单来说就是while，一直cas直到成功吧。</div>2018-06-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/fb/81/f41482ff.jpg" width="30px"><span>浩</span> 👍（0） 💬（1）<div>自旋就是空转，什么都不干，就在循环等待锁，相当于缓冲一段时间，看能否获得锁，如果此次自旋获得锁，那么下次，会比此次更长时间自旋，增大获得锁的概率，否则，减少自旋次数。</div>2018-06-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/02/6f/301b1381.jpg" width="30px"><span>Roysatm</span> 👍（26） 💬（3）<div>
1.synchronized锁，可分为偏向锁、轻量级锁、重量级锁。在jvm没有显示关闭偏向锁的情况下，初始状态时默认是偏向锁时，
线程请求先通过CAS替换mark word中threadId,如果替换成功则该线程持有当前锁。如果替换失败，锁会升级为轻量级锁，
线程请求会尝试CAS替换mark word中指向栈中锁记录的指针，如果替换成功则该线程持有当前锁。
如果替换失败，当前线程会自旋一定次数，继续尝试获取CAS替换，如果超过一定自旋次数，锁升级为重量级锁。

synchronized锁是调用系统内核互斥锁实现的，线程在获取synchronized锁失败后，也会进入一个等待获取锁队列中（系统内核实现的），
线程会由运行态切换到阻塞态，让出CPU，待其他线程释放锁后唤醒它。

synchronize锁重（1.6之后jvm有优化）就是重在两点，一是调用内核互斥锁实现，二是线程获取锁失败会变成阻塞态，让出CPU，等待唤醒（有一定的上下文切换）</div>2019-02-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/1a/66/2d9db9ed.jpg" width="30px"><span>苦行僧</span> 👍（7） 💬（2）<div>轻量级锁和重量级锁没有详细说明和区别，仅从名字不好区别</div>2019-02-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/e2/47/e910afec.jpg" width="30px"><span>刘杰</span> 👍（5） 💬（0）<div>偏斜锁和轻量级锁的区别不是很清晰</div>2018-07-12</li><br/>
</ul>