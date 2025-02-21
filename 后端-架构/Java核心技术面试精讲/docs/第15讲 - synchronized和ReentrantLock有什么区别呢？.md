从今天开始，我们将进入Java并发学习阶段。软件并发已经成为现代软件开发的基础能力，而Java精心设计的高效并发机制，正是构建大规模应用的基础之一，所以考察并发基本功也成为各个公司面试Java工程师的必选项。

今天我要问你的问题是， synchronized和ReentrantLock有什么区别？有人说synchronized最慢，这话靠谱吗？

## 典型回答

synchronized是Java内建的同步机制，所以也有人称其为Intrinsic Locking，它提供了互斥的语义和可见性，当一个线程已经获取当前锁时，其他试图获取的线程只能等待或者阻塞在那里。

在Java 5以前，synchronized是仅有的同步手段，在代码中， synchronized可以用来修饰方法，也可以使用在特定的代码块儿上，本质上synchronized方法等同于把方法全部语句用synchronized块包起来。

Reentran...
<div><strong>精选留言（30）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/10/4a/c8/7679cd2a.jpg" width="30px"><span>冬青树</span> 👍（138） 💬（9）<div>一直在研究JUC方面的。所有的Lock都是基于AQS来实现了。AQS和Condition各自维护了不同的队列，在使用lock和condition的时候，其实就是两个队列的互相移动。如果我们想自定义一个同步器，可以实现AQS。它提供了获取共享锁和互斥锁的方式，都是基于对state操作而言的。ReentranLock这个是可重入的。其实要弄明白它为啥可重入的呢，咋实现的呢。其实它内部自定义了同步器Sync，这个又实现了AQS，同时又实现了AOS，而后者就提供了一种互斥锁持有的方式。其实就是每次获取锁的时候，看下当前维护的那个线程和当前请求的线程是否一样，一样就可重入了。</div>2018-06-07</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/63/14/06eff9a4.jpg" width="30px"><span>Jerry银银</span> 👍（57） 💬（2）<div>先说说点学习感受：
并发领域的知识点很多也很散，并且知识点之间交错的。比如：synchronized，这个小小的关键字，能够彻底理解它，需要的知识储备有：基本使用场景、对锁的理解、对线程安全的理解、对同步语义的理解、对JMM的理解等等。有时候，一个知识点暂时做不到透彻理解，可能是正常的，需要再继续学习其它的知识点，等到一定时候，回过头来重新学习，会有一种柳暗花明又一村的感觉。我想，这也可能是老师提到的：并发领域相关知识的准备，需要点耐心。

再说说这篇专栏：
这篇专栏，在知识扩展部分，我觉得结构不是太清晰。我读了很多遍之后，还是有这种感觉：文章讲了很多东西，但是我却很难说出文章的主题。
为此，我自己总结了一下知识扩展部分的主线：
1. 进入并发领域，首先需要理解什么是线程安全，为什么会存在线程不安全，又为什么需要线程安全。这个知识点可参考《Java并发编程实践》，并且我也认为对于线程安全的讲解，这本书堪称权威；
2. 老师在讲解线程安全这个点的时候，顺其自然地使用了synchronized和ReentrantLock来保证线程安全（即：Java提供的锁机制）同时，老师也稍微讲解了一下synchronized和ReentrantLock的使用和区别；
3. 最后，老师举了一个ReentrantLock的典型使用场景：ArrayBlockingQueue。ArrayBlockingQueue使用ReentrantLock来实现加锁机制，保证队列的安全读取，并且使用Condition来实现队列阻塞的条件判断和读写端唤醒，特别提一句：具体的实现代码是相当的优雅！
</div>2019-02-01</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/16/53/03930a6b.jpg" width="30px"><span>BY</span> 👍（31） 💬（4）<div>要是早看到这篇文章，我上次面试就过了。。</div>2018-06-07</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/33/92/99530cee.jpg" width="30px"><span>灰飞灰猪不会灰飞.烟灭</span> 👍（20） 💬（1）<div>ReentrantLock 加锁的时候通过cas算法，将线程对象放到一个双向链表中，然后每次取出链表中的头节点，看这个节点是否和当前线程相等。是否相等比较的是线程的ID。
老师我理解的对不对啊？</div>2018-06-07</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/e0/9f/9259a6b9.jpg" width="30px"><span>Kyle</span> 👍（16） 💬（1）<div>最近刚看完《Java 并发编程实战》，所以今天看这篇文章觉得丝毫不费力气。开始觉得，极客时间上老师讲的内容毕竟篇幅有限，更多的还是需要我们课后去深入钻研。希望老师以后讲完课也能够适当提供些参考书目，谢谢。</div>2018-06-07</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/fe/3c/13175251.jpg" width="30px"><span>Miaozhe</span> 👍（15） 💬（2）<div>杨老师，问个问题，看网上有说Condition的await和signal方法，等同于Object的wait和notify，看了一下源码，没有直接的关系。
ReentractLock是基于双向链表的对接和CAS实现的，感觉比Object增加了很多逻辑，怎么会比Synchronized效率高？有疑惑。</div>2018-06-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/db/90/a0f2d021.jpg" width="30px"><span>木瓜芒果</span> 👍（14） 💬（3）<div>杨老师，您好，synchronized在低竞争场景下可能优于retrantlock，这里的什么程度算是低竞争场景呢？</div>2018-06-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/00/85/21e1a720.jpg" width="30px"><span>Daydayup</span> 👍（9） 💬（1）<div>我用过读写分离锁，读锁保证速度，写锁保证安全问题。再入锁还是挺好用的。老师写的很棒，学到不少知识。感谢</div>2018-06-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/6e/83/a912bfb4.jpg" width="30px"><span>xinfangke</span> 👍（6） 💬（3）<div>老师 问你个问题 在spring中 如果标注一个方法的事务隔离级别为序列化 而数据库的隔离级别是默认的隔离级别 此时此方法中的更新 插入语句是如何执行的？能保证并发不出错吗</div>2018-06-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/68/49/418a9486.jpg" width="30px"><span>Neil</span> 👍（4） 💬（2）<div>可以理解为synchronized是悲观锁 另一个是乐观锁</div>2019-01-07</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/32/3f/fa4ac035.jpg" width="30px"><span>sunlight001</span> 👍（4） 💬（1）<div>老师这里说的低并发和高并发的场景，大致什么数量级的算低并发？我们做管理系统中用到锁的情况基本都算低并发吧</div>2018-06-07</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/87/e5/67495b10.jpg" width="30px"><span>时间总漫不经心</span> 👍（3） 💬（1）<div>老师，jmm什么时候将工作内存的值写入到主内存中呢？</div>2018-08-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/6c/a3/11df679f.jpg" width="30px"><span>风吹过wu</span> 👍（1） 💬（1）<div>希望能够通过借此为契机，深入了解java并发。由于以前自学的java，不系统，借此风水宝地，好好的理理脉络，形成系统</div>2019-01-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/d2/81/db154f5f.jpg" width="30px"><span>飞鱼</span> 👍（1） 💬（1）<div>之前有被问到synchronize和ReetrantLock底层实现上的区别，笼统的答了下前者是基于JVM实现的，后者依赖于CPU底层指令的实现，关于这个，请问有更详细的解答吗？</div>2018-06-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/ac/a1/43d83698.jpg" width="30px"><span>云学</span> 👍（1） 💬（1）<div>看完还是觉得c++11的Lockguard比较优雅，难怪耗子哥说学习java是为了更好的用c++</div>2018-06-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/7c/8e/73581062.jpg" width="30px"><span>徐金铎</span> 👍（1） 💬（1）<div>补充一点，Syc的静态方法和syc(.class)确实是一样的，但是前者是在方法前加syc的flag，后者在反编译后的代码中看不到。所以我查阅了hotspot的文档和代码，确定这一个细节处理是有jvm做的。两者实际运行，确实是一样的处理。</div>2018-06-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/15/02/66f65388.jpg" width="30px"><span>雷霹雳的爸爸</span> 👍（1） 💬（1）<div>真不记得自己用过，诚如老师所讲，其有特殊语义能力，如超时，公平性等，但窃以为别给自己添乱最好，万一忘了unlock，话说他这玩意儿为啥不设计个类似try…with…resource的语法糖？估计就是为了把加锁解锁的语法能力分散在不同子例程里撰写使用的考虑？可问题是如果都写成那样了，是否有说明自己程序设计上内聚性不够呢？嗯，再看点源码来找答案吧…话说JCIP真是好书，学不学究的读读资本论之后就释然了，如果真能顺着它仔细读下来，发现它针对特定栗子还会随着内容深入给出不同解法，不禁感叹，也许在利用较低级别的通信原语时，很有可能是对并发包里面一些现成工具类缺乏了解或者是对真正的并发问题缺乏深入理解造成的…虽然自己看起来也就是个CRUD开发的老佃户命了，还是非常期待老师后面的主题，毕竟咱还是有颗通向地主阶层的心</div>2018-06-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/63/14/06eff9a4.jpg" width="30px"><span>Jerry银银</span> 👍（0） 💬（1）<div>@老师  ReentrantLock 和 synchronized的在JDK 6.0之前的在高度竞争场景下的性能差异，在Android虚拟机中也同样适用吗？ 或者说：在Android开发中，又该如何正确使用ReentrantLock呢？</div>2019-02-02</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/fb/9a/72f7b184.jpg" width="30px"><span>猿工匠</span> 👍（0） 💬（1）<div>刚好在熟悉ArrayBlockingQueue的源码。通过老师的例子，对 ReentrantLock 的概念和实践，有了点感觉。</div>2018-11-22</li><br/><li><img src="" width="30px"><span>john-jy</span> 👍（0） 💬（1）<div>ReentrantLock fairLock = new ReentrantLock(true);
try {
	&#47;&#47; do something
} finally {
 	fairLock.unlock();
}
请问ReentrantLock fairLock = new ReentrantLock(true);这一行可以写在try里面吗？我看别人有些代码写在try里面，会不会有问题呢，比如发生new异常</div>2018-10-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/d8/d6/47da34bf.jpg" width="30px"><span>任鹏斌</span> 👍（0） 💬（1）<div>老师sychronized应该也是再去锁吧？只是不能实现公平性</div>2018-08-16</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/9IUbqCCa3zXkSibzoPc8CgLELkMEbibUxrv8gdicySKeYttf2VG3lHNhU4ia61ibdQbGT556rI1sFgO9lxH9XPTjK2Q/132" width="30px"><span>java爱好者</span> 👍（0） 💬（1）<div>老师，怎么判断一个队列是有界或无界，arrayblockingqueue是有界</div>2018-06-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/33/92/99530cee.jpg" width="30px"><span>灰飞灰猪不会灰飞.烟灭</span> 👍（0） 💬（1）<div>老师，signal和await和notify wait有啥区别呢？
还有lock方式放入双向链表中的node，是不是按照线程对象（对象地址）进行比较的啊？
就是如何判断当前线程是否获得锁是不是按照线程对象地址啊。谢谢老师</div>2018-06-07</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/77/b3/991f3f9b.jpg" width="30px"><span>公号-技术夜未眠</span> 👍（268） 💬（4）<div>ReentrantLock是Lock的实现类，是一个互斥的同步器，在多线程高竞争条件下，ReentrantLock比synchronized有更加优异的性能表现。

1 用法比较
Lock使用起来比较灵活，但是必须有释放锁的配合动作
Lock必须手动获取与释放锁，而synchronized不需要手动释放和开启锁
Lock只适用于代码块锁，而synchronized可用于修饰方法、代码块等 

2 特性比较
	ReentrantLock的优势体现在：
	  具备尝试非阻塞地获取锁的特性：当前线程尝试获取锁，如果这一时刻锁没有被其他线程获取到，则成功获取并持有锁
	  能被中断地获取锁的特性：与synchronized不同，获取到锁的线程能够响应中断，当获取到锁的线程被中断时，中断异常将会被抛出，同时锁会被释放
	  超时获取锁的特性：在指定的时间范围内获取锁；如果截止时间到了仍然无法获取锁，则返回

3 注意事项
在使用ReentrantLock类的时，一定要注意三点：
	 在finally中释放锁，目的是保证在获取锁之后，最终能够被释放
	 不要将获取锁的过程写在try块内，因为如果在获取锁时发生了异常，异常抛出的同时，也会导致锁无故被释放。
	 ReentrantLock提供了一个newCondition的方法，以便用户在同一锁的情况下可以根据不同的情况执行等待或唤醒的动作。</div>2018-06-07</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/db/a4/191be6ad.jpg" width="30px"><span>加载中……</span> 👍（11） 💬（1）<div>看到留言区，有个同学问：new ReentrantLock()能不能写到里面，我看了回复，不是很认同，不知道到对不对。其实：new lock和lock api的调用得写到try外面，写到里面会有问题，如下：
lock() api 可能会抛出异常，如果放到try里面，在finally里面unlock会再抛出异常(因为当前状态不对)，这个时候 &quot;解锁异常&quot;会隐藏&quot;加锁异常&quot;，也就是异常堆栈只有“解锁异常”没有&quot;加锁异常&quot;，而这样会误导程序员吧？，模拟代码如下：
try {
            &#47;&#47;如果lock在try里，且lock抛出异常
            throw new RuntimeException(&quot;加锁异常&quot;);
        } finally {
            &#47;&#47;调用unlock如果lock没有获取到锁会抛出异常，这个在堆栈会隐藏“加锁异常”
            throw new RuntimeException(&quot;解锁异常&quot;);
        }</div>2019-02-25</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/1d/71/4d3d2a62.jpg" width="30px"><span>猪哥灰</span> 👍（8） 💬（0）<div>为了研究java的并发，我先把考研时候的操作系统教材拿出来再仔细研读一下，可见基础之重要性，而不管是什么语言，万变不离其宗</div>2018-06-29</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTLxDV4VqTISMDBPgnjDAicCnWbjE3FeFv4eNWdITw6aib82iasfb63vJCU6bxRB4zN6eaGztZPmlpWdg/132" width="30px"><span>豆子高</span> 👍（7） 💬（0）<div>看了杨老师的讲解，其实也不是很理解，这块儿平时也不怎么注意学习，每次都是要面试了临时抱佛脚，不过这次算是一次比较全面的学习，下面记录一下我的学习结果（比较简略，算是一个要点大纲，说错的的地方希望各位老师同学给个指点）：
Synchronize与ReentrantLock都是属于阻塞式同步，即当前线程正在执行时，其他线程都会阻塞在同步块外等待。（因为线程的唤起和阻塞代价都比较高，所以一般锁的优化都是往这方面考虑）

Synchronize（以下简称S）
S是一个关键字，用于修饰方法和代码块，加锁和释放锁都是通过JVM的编译器来自动实现的，所以属于JVM层面的锁机制；

S竞争锁的时候无法设置超时时间，所以是一直等待的，这样会导致死锁，不过这是S优化前会出现的问题，优化后，S引入了偏向锁、轻量级锁，就好用很多。S的优化借鉴了R的CAS技术（无锁算法），在用户态就试图进行加锁；

S控制等待和唤醒线程需要结合Object对象的wait()当前线程休眠且释放锁;和notify()获得锁;和notifyAll();方法；

S在代码块完成或出现异常的时候自动释放锁。

 

ReentrantLock（以下简称R）
R是一种再入锁，手动上锁，通过实现JDK的API接口lock方法和unlock来实现加锁和释放锁，所以是一种JDK层面的锁机制；

R竞争锁的时候可以设置超时时间，会尝试获得锁，若线程长时间得不到锁会选择放弃等待（通过lockInterruptibly来实现）（等待可中断）；

R可实现公平锁，针对等待的线程采取先到先得的措施；

R控制等待和唤醒线程需要结合Condition的await();和signal();和signalAll();方法；

R不会自动释放锁，需要使用finally{}手动释放unlock；

R提供了一些高级功能：

1、等待可中断；

2、公平锁；

R是基于AQS（AbstractQueueSynchronize）和LockSupport，AQS主要利用CAS实现轻量级的同步，AQS本质是一个同步器&#47;阻塞锁的基础框架，主要提供加锁和释放锁。在内部维护一个FIFO的等待队列，用于存储由于锁竞争而阻塞的线程，使用链表作为队列，volatile作为变量，state作为锁状态标识。

CAS是一种无锁算法，一种可以实现线程同步的原子操作。有三个参数，内存地址V，旧的预期值A，即将要更新的目标值B，当且仅当V=A的时候，才会将V修改成B。</div>2020-02-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/b1/20/8718252f.jpg" width="30px"><span>鲲鹏飞九万里</span> 👍（6） 💬（2）<div>老师，可以问您一个课外题吗。具备怎样的能力才算是java高级开发</div>2018-06-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/67/f4/9a1feb59.jpg" width="30px"><span>钱</span> 👍（3） 💬（0）<div>没有可修改，不用担心状态会改变，有没有多线程无所谓。
有可修改，只有一个线程，不用担心状态会被修改错。
有可修，有多线程，就存在修改错乱的情况，就需要加锁。锁，到底是啥东西呢？锁，本质是啥呢？经常说获取锁，到底是获取的啥呢？用完锁，要释放，释放啥？释放的动作是啥呢？

锁-本质上就是一种同步机制，能够保证多线程环境下，对共享数据的正确修改。
同步机制，是什么机制呢？怎么保证的呢？到这里是否就需要操作系统相关的知识才能理解了，能理解锁的作用和特点，但对锁本身认识还是模糊的，不太清楚他是怎么起作用的，他的特点是他内部的什么因素的外在表现？
恩，先继续，然后再回头看看，也许能领悟出的点什么🤔</div>2018-12-15</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/3b/86/170e58ae.jpg" width="30px"><span>一个帅哥</span> 👍（3） 💬（0）<div>从书写角度：reentrantlock 需要手动获取和释放锁，而syncgeonised不需要手动获取和释放
所以，此外，reentrantlock有trylock 和lockinterruptly ，所以对锁的操作更灵活。从功能的角度看，reentrantlock支持公平锁和非公平锁 而synchronized 仅支持非公平锁。</div>2018-06-08</li><br/>
</ul>