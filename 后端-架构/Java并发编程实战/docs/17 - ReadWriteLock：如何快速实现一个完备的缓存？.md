前面我们介绍了管程和信号量这两个同步原语在Java语言中的实现，理论上用这两个同步原语中任何一个都可以解决所有的并发问题。那Java SDK并发包里为什么还有很多其他的工具类呢？原因很简单：**分场景优化性能，提升易用性**。

今天我们就介绍一种非常普遍的并发场景：读多写少场景。实际工作中，为了优化性能，我们经常会使用缓存，例如缓存元数据、缓存基础数据等，这就是一种典型的读多写少应用场景。缓存之所以能提升性能，一个重要的条件就是缓存的数据一定是读多写少的，例如元数据和基础数据基本上不会发生变化（写少），但是使用它们的地方却很多（读多）。

针对读多写少这种并发场景，Java SDK并发包提供了读写锁——ReadWriteLock，非常容易使用，并且性能很好。

**那什么是读写锁呢？**

读写锁，并不是Java语言特有的，而是一个广为使用的通用技术，所有的读写锁都遵守以下三条基本原则：

1. 允许多个线程同时读共享变量；
2. 只允许一个线程写共享变量；
3. 如果一个写线程正在执行写操作，此时禁止读线程读共享变量。

读写锁与互斥锁的一个重要区别就是**读写锁允许多个线程同时读共享变量**，而互斥锁是不允许的，这是读写锁在读多写少场景下性能优于互斥锁的关键。但**读写锁的写操作是互斥的**，当一个线程在写共享变量的时候，是不允许其他线程执行写操作和读操作。
<div><strong>精选留言（30）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/0f/48/ee/96a7d638.jpg" width="30px"><span>西西弗与卡夫卡</span> 👍（73） 💬（5）<div>考虑到是线上应用，可采用以下方法
1. 源代码分析。查找ReentrantReadWriteLock在项目中的引用，看下写锁是否在读锁释放前尝试获取
2. 如果线上是Web应用，应用服务器比如说是Tomcat，并且开启了JMX，则可以通过JConsole等工具远程查看下线上死锁的具体情况</div>2019-04-06</li><br/><li><img src="" width="30px"><span>ycfHH</span> 👍（55） 💬（5）<div>问题1：获取写锁的前提是读锁和写锁均未被占用？
问题2：获取读锁的前提是没有其他线程占用写锁？
基于以上两点所以只支持锁降级而不允许锁升级。
问题3
高并发下，申请写锁时是不是中断其他线程申请读锁，然后等待已有读锁全部释放再获取写锁？因为如果没有禁止读锁的申请的话在读多写少的情况下写锁可能一直获取不到。
这块不太懂，希望老师能指点一下。</div>2019-05-07</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/e7/56/c72997f3.jpg" width="30px"><span>缪文</span> 👍（55） 💬（7）<div>老师，感觉这里的读写锁，性能还有可以提升的地方，因为这里可能很多业务都会使用这个缓存懒加载，实际生产环境，写缓存操作可能会比较多，那么不同的缓存key，实际上是没有并发冲突的，所以这里的读写锁可以按key前缀拆分，即使是同一个key，也可以类似ConcurrentHash 一样分段来减少并发冲突</div>2019-04-07</li><br/><li><img src="" width="30px"><span>sibyl</span> 👍（36） 💬（7）<div>老师好，回答一下有些同学关于读锁有什么用的疑问，您看看对不对，如果对，给个置顶鼓励一下，谢谢老铁啦，啊哈哈

1、有些同学认为读锁没有用，他们的理由是：读操作又不会修改数据，想读就读呗，无论读的是就值还是新值，反正能读到。


2、也有同学认为读锁是为了防止多线程读到的数据不一致。

我认为不是这个原因，只需要问两个问题就知道了，首先问不一致的是什么？然后反问不一致会导致什么问题呢？

有些同学认为不一致就是有些线程读的是旧值，有些读的是新值，所以不一致。但是反问导致什么问题，就不是很好回答了，可能回答说为了保险吧，哈哈哈。

实际上即使加读锁，还是会存在有的线程读旧值，有的线程读新值，甚至非公平锁情况下，先开始的线程反而读到新值，而后开始的线程反而读到旧值，所以读锁并不是为了保证多线程读到的值是一样的。

3、那么读锁的作用是什么呢？

任何锁表面上是互斥，但本质是都是为了避免原子性问题（如果程序没有原子性问题，那只用volatile来避免可见性和有序性问题就可以了，效率更高），读锁自然也是为了避免原子性问题，比如一个long型参数的写操作并不是原子性的，如果允许同时读和写，那读到的数很可能是就是写操作的中间状态，比如刚写完前32位的中间状态。long型数都如此，而实际上一般读的都是复杂的对象，那中间状态的情况就更多了。

所以读锁是防止读到写操作的中间状态的值。</div>2020-07-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/ac/ef/494f56c3.jpg" width="30px"><span>crazypokerk</span> 👍（29） 💬（5）<div>老师，可不可以这样理解，ReadWirteLock不支持锁的升级，指的是：在不释放读锁的前提下，无法继续获取写锁，但是如果在释放了读锁之后，是可以升级为写锁的。锁的降级就是：在不释放写锁的前提下，获取读锁是可以的。请老师指正，感谢。</div>2019-04-06</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/0d/24/b07de4f2.jpg" width="30px"><span>WhoAmI</span> 👍（20） 💬（4）<div>一般都说线程池有界队列使用ArrayBlockingQueue，无界队列使用LinkedBlockingQueue，我很奇怪，有界无界不是取决于创建的时候传不传capacity参数么，我现在想创建线程池的时候，new LinkedBlockingQueue(2000)这样定义有界队列，请问可以吗？</div>2019-04-06</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/e9/0b/1171ac71.jpg" width="30px"><span>WL</span> 👍（17） 💬（1）<div>老师我们现在的项目全都是集群部署, 感觉在这种情况下是不是单机的Lock,和Synchronized都用不上, 只能采用分布式锁的方案? 那么这种情况下, 如何提高每个实例的并发效率?</div>2019-04-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/ee/d2/7024431c.jpg" width="30px"><span>探索无止境</span> 👍（11） 💬（5）<div>老师你好，我们在项目开发中，如果要实现缓存，会直接采用Redis，感觉更合适，所以不太清楚，实际中ReadWriteLock可以解决哪些问题？</div>2019-08-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/21/b3/db933462.jpg" width="30px"><span>文灏</span> 👍（10） 💬（5）<div>王老师你好，有个问题想请教一下。既然允许多个线程同时读，那么这个时候的读锁意义在哪里？</div>2019-05-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/15/01/927d96e5.jpg" width="30px"><span>随风而逝</span> 👍（9） 💬（2）<div>缓存一致性问题，我们都是双删缓存。老师，读写锁的降级和单独使用有什么区别？或者说有什么优势？</div>2019-04-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/ff/c6/8b5cbe97.jpg" width="30px"><span>刘志兵</span> 👍（9） 💬（2）<div>这里讲的读写锁和丁奇老师讲的mysql中的mdl锁和ddl锁原理好像是一样的，就是读写互斥，写写互斥，读读不互斥，老师讲的这个应该是读写锁的基本原理，mysql是这个锁的一种典型应用吧</div>2019-04-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/39/f9/acfb9a48.jpg" width="30px"><span>无言的约定</span> 👍（8） 💬（3）<div>王老师，&quot;&quot;如果一个写线程正在执行写操作，此时禁止读线程读共享变量&quot;&quot;  这句话反过来也成立，是不是意味着读操作和写操作是互斥的，不能同时进行？</div>2019-12-05</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/03/f7/3a493bec.jpg" width="30px"><span>老杨同志</span> 👍（7） 💬（4）<div>老师，如果读锁的持有时间较长，读操作又比较多，会不会一直拿不到写锁？</div>2019-04-06</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/30/c1/2dde6700.jpg" width="30px"><span>密码123456</span> 👍（6） 💬（1）<div>系统停止了响应，说明线程可能被占满了。cpu利用率低为什么会推断出，是读锁升级为写锁？是因为锁升级后，线程都是等待状态吗？是不是cpu高是锁竞争？还有怎么验证读锁升级为写锁？</div>2019-04-06</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTJic27dia65Z8OfsQBEmaIUdo53DgLCakbK9ulIrNgT86pe3RbbybuGCDh6StIzJ7XYFLrSYtibNe7Xg/132" width="30px"><span>guihaiyizhu</span> 👍（4） 💬（1）<div>看了下juc的源码，尝试着分析一波 为啥为啥ReentrantReadWriteLock不能锁的降低不能锁的降低，但是可以锁的升级。
ReentrantReadWriteLock 实现了 ReadWriteLock 的结构。所以会有读锁和写锁两个方法来获取对应的锁。

先说下 JUC 锁的一般讨论：
1. status 表示状态，比如：status 大于0 表示线程可以获得锁，线程等于0 表示需等待其他线程释放锁
2. 等待队列： 获取不到锁的线程会丢到等待队列。
3. LockSuppert.park &#47; unpark: 来作用线程的通信。

获取锁的大概逻辑可以认为是：1. status 不满足要求， 2. 线程丢到等到队列 3. 调用LockSuppert.park(thread.current)

可以分析出 判断线程是否可以进入的关键方法即是：status 是否符合要求，也就是 tryAcquire 的方法

基于此，我们来看ReentrantReadWriteLock 里面读锁写锁的设计了：

先给出状态定义的代码
static final int SHARED_SHIFT   = 16;
static final int SHARED_UNIT    = (1 &lt;&lt; SHARED_SHIFT);
static final int MAX_COUNT      = (1 &lt;&lt; SHARED_SHIFT) - 1;
static final int EXCLUSIVE_MASK = (1 &lt;&lt; SHARED_SHIFT) - 1;
static int sharedCount(int c)    { return c &gt;&gt;&gt; SHARED_SHIFT; }
static int exclusiveCount(int c) { return c &amp; EXCLUSIVE_MASK; }

给出结论：status 低16位用来做 排它锁的状态，高16位用来做共享锁的状态

WriteLock:
        protected final boolean tryAcquire(int acquires) {
            Thread current = Thread.currentThread();
            int c = getState();
            &#47;&#47; 获取写锁的status
            int w = exclusiveCount(c);
            if (c != 0) {
                &#47;&#47; 如果 c ！= 0 &amp;&amp; w == 0. 说明这个RWLock 被其他写锁占着，所有不会锁的升级
                if (w == 0 || current != getExclusiveOwnerThread())
                    return false;
            }
        }


ReadLock:
        protected final int tryAcquireShared(int unused) {
            Thread current = Thread.currentThread();
            int c = getState();
            &#47;&#47; 排它状态不等0 且 current 不是写锁的线程 才不能持有锁，
            if (exclusiveCount(c) != 0 &amp;&amp;
                getExclusiveOwnerThread() != current)
                return -1;
            &#47;&#47; ...
            return fullTryAcquireShared(current);
        }</div>2020-06-17</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/6LaITPQ4Lk5fZn8ib1tfsPW8vI9icTuSwAddiajVfibPDiaDvMU2br6ZT7K0LWCKibSQuicT7sIEVmY4K7ibXY0T7UQEiag/132" width="30px"><span>尔东橙</span> 👍（4） 💬（1）<div>老师您好，我想问下锁的升级&#47;降级有什么好处么？</div>2019-08-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/64/86/f5a9403a.jpg" width="30px"><span>yang</span> 👍（4） 💬（4）<div>老师，我想问一个“超纲”的问题:

我看分布式锁使用redis实现，主要就是在while循环里使用jedis的get(key); setnx(key,value);  

那这里分布式锁的实现，有没有必要采用今天讲的读写所+双检查来实现啊？

恳请老师回答，谢谢老师!</div>2019-04-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/a1/40/2c4ba425.jpg" width="30px"><span>IMSolar</span> 👍（3） 💬（1）<div>当有一个线程获取到写锁，其他线程都被阻塞了，假设这时候回源数据库时间比较长，会影响请求的响应时间，请问老师这里有什么办法可以在获取不到锁的情况直接返回null？</div>2019-04-06</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/3d/51/9723276c.jpg" width="30px"><span>邋遢的流浪剑客</span> 👍（3） 💬（1）<div>老师，在Spring的环境下，如果使用redis实现缓存（用RedisTemplate操作），需要像Cache中代码中一样再做一次检查吗？</div>2019-04-06</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/36/b3/c4a2f3fd.jpg" width="30px"><span>_light</span> 👍（2） 💬（2）<div>老师好，有一个问题想请教一下您，感谢😊
对于锁我一直有个疑问，我看了不少源码，发现每次加锁的时候，lock()都是在try语句上面，加锁这个动作放在异常捕获里面会有什么影响吗？
private void signalNotEmpty() {
    ReentrantLock takeLock = takeLock;
    takeLock.lock();
    try {
        notEmpty.signal();
    } finally {
        takeLock.unlock();
    }
}</div>2019-04-19</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/DYAIOgq83erWxMXolPylQk8Z6V6yt2LtibksrksC4bHtmxkuCC4Wzw7trl6CfwmsSFMyHFItFnvl21RvQ8fyOBQ/132" width="30px"><span>Geek_961eed</span> 👍（2） 💬（1）<div>为什么允许锁的降级而不允许锁的升级？</div>2019-04-07</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/e1/e5/815d4271.jpg" width="30px"><span>我是卖报小行家</span> 👍（2） 💬（2）<div>synchronized内部是支持升级却不支持降级，偏向锁可以升级成轻量级锁，反之则不行，是不是这样老师</div>2019-04-06</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/ee/c6/bebcbcf0.jpg" width="30px"><span>俯瞰风景.</span> 👍（1） 💬（1）<div>锁的降级：释放写锁前，降级为读锁
和
读写锁的原则3：如果一个写线程正在执行写操作，此时禁止读线程读共享变量。
老师，这样是否是矛盾了呢？怎么同时理解呢？

</div>2020-12-25</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTK6Nic6V6iawbbIF1RRbRlwNmC0Cmt3LlQRAiaiayCibpplSDPXticVyOp97CEypEuQm2Iib7ZYCjrrlIgWQ/132" width="30px"><span>奔跑的蜗牛</span> 👍（1） 💬（1）<div>请教下老师，如果读多写少情况下，是否会存在写锁饿死的情况？如果用公平锁，是否会导致写锁很久才能获取到的情况呢？</div>2019-12-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/5a/28/732d3f2f.jpg" width="30px"><span>GEEKBANG_6638780</span> 👍（1） 💬（1）<div>老杨同志
老师，如果读锁的持有时间较长，读操作又比较多，会不会一直拿不到写锁？
作者回复: 不会一直拿不到，只是等待的时间会很长
----------------------------------------------------
老师，你这个回答不对吧。我记得之前看源码是，读写锁，对于写锁是优先的。意思就是说，当有写线程时，哪怕有读线程在等待，都会优先分配给写线程的</div>2019-06-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/8c/4e/b81969fa.jpg" width="30px"><span>南北少卿</span> 👍（1） 💬（1）<div>王老师，读写锁中加读锁后如何避免写线程饿死？</div>2019-05-14</li><br/><li><img src="" width="30px"><span>有渔@蔡</span> 👍（1） 💬（1）<div>真的是用心写了，想必老师工作中也是很负责任的那种。每个要点，都从原理出发。而且纵横比较，这专栏太值了</div>2019-04-26</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/aNdZY7YBA3jx7354T4vLkrQmfzGYXMQ34eqlUSK3jbh8zccLx9rkysCeU0Qic1PkAlukFAibb3hoodpXcF0RjnibA/132" width="30px"><span>程序员就要进步</span> 👍（1） 💬（4）<div>老师，我有点不太理解这个读锁存在的意义是什么，既然支持多线程访问，直接不加锁不就行了。</div>2019-04-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/2b/c8/61eeae65.jpg" width="30px"><span>Sunny_Lu</span> 👍（1） 💬（1）<div>老师，读锁释放，获取写锁的时候，会存在并发，获取不到写锁阻塞的情况吧？</div>2019-04-11</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/BpprxVMjsB0Ok4wGunDLHOLEI9wJX5HIEVsqs2EaXpuODfM7tuiaNfjPcxKWc60TwTaJnTuSicGMicib4r4um02qicQ/132" width="30px"><span>Geek_c33c8e</span> 👍（1） 💬（1）<div>老师，看到你说写锁可以降级为读锁，是指在同一线程吗？如果是两个线程的话，读写就是互斥的了吧？</div>2019-04-10</li><br/>
</ul>