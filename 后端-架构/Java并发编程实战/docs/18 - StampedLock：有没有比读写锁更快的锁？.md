在[上一篇文章](https://time.geekbang.org/column/article/88909)中，我们介绍了读写锁，学习完之后你应该已经知道“读写锁允许多个线程同时读共享变量，适用于读多写少的场景”。那在读多写少的场景中，还有没有更快的技术方案呢？还真有，Java在1.8这个版本里，提供了一种叫StampedLock的锁，它的性能就比读写锁还要好。

下面我们就来介绍一下StampedLock的使用方法、内部工作原理以及在使用过程中需要注意的事项。

## StampedLock支持的三种锁模式

我们先来看看在使用上StampedLock和上一篇文章讲的ReadWriteLock有哪些区别。

ReadWriteLock支持两种模式：一种是读锁，一种是写锁。而StampedLock支持三种模式，分别是：**写锁**、**悲观读锁**和**乐观读**。其中，写锁、悲观读锁的语义和ReadWriteLock的写锁、读锁的语义非常类似，允许多个线程同时获取悲观读锁，但是只允许一个线程获取写锁，写锁和悲观读锁是互斥的。不同的是：StampedLock里的写锁和悲观读锁加锁成功之后，都会返回一个stamp；然后解锁的时候，需要传入这个stamp。相关的示例代码如下。

```
final StampedLock sl = 
  new StampedLock();
  
// 获取/释放悲观读锁示意代码
long stamp = sl.readLock();
try {
  //省略业务相关代码
} finally {
  sl.unlockRead(stamp);
}

// 获取/释放写锁示意代码
long stamp = sl.writeLock();
try {
  //省略业务相关代码
} finally {
  sl.unlockWrite(stamp);
}
```

StampedLock的性能之所以比ReadWriteLock还要好，其关键是StampedLock支持乐观读的方式。ReadWriteLock支持多个线程同时读，但是当多个线程同时读的时候，所有的写操作会被阻塞；而StampedLock提供的乐观读，是允许一个线程获取写锁的，也就是说不是所有的写操作都被阻塞。
<div><strong>精选留言（30）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/11/4e/3a/86196508.jpg" width="30px"><span>linqw</span> 👍（107） 💬（5）<div>课后思考题：在锁升级成功的时候，最后没有释放最新的写锁，可以在if块的break上加个stamp=ws进行释放</div>2019-04-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/1c/82/74ab79df.jpg" width="30px"><span>等我先变个身</span> 👍（49） 💬（9）<div>乐观锁的想法是“没事，肯定没被改过”，于是就开心地获取到数据，不放心吗？那就再验证一下，看看真的没被改过吧？这下可以放心使用数据了。
我的问题是，验证完之后、使用数据之前，数据被其他线程改了怎么办？我看不出validate的意义。这个和数据库更新好像还不一样，数据库是在写的时候发现已经被其他人写了。这里validate之后也难免数据在进行业务计算之前已经被改掉了啊？</div>2019-04-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/08/d1/3c7747ef.jpg" width="30px"><span>Grubby🐑</span> 👍（42） 💬（1）<div>老师，调用interrupt引起cpu飙高的原因是什么</div>2019-04-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/8a/f3/7c89d00e.jpg" width="30px"><span>Presley</span> 👍（29） 💬（1）<div>老师，StampedLock 读模板，先通过乐观读或者悲观读锁获取变量，然后利用这些变量处理业务逻辑，会不会存在线程安全的情况呢? 比如，读出来的变量没问题，但是进行业务逻辑处理的时候，这时，读出的变量有可能发生变化了吧(比如被写锁改写了)？所以，当使用乐观读锁时，是不是等业务都处理完了（比如先利用变量把距离计算完），再判断变量是否被改写，如果没改写，直接return;如果已经改写，则使用悲观读锁做同样的事情。不过如果业务比较耗时，可能持有悲观锁的时间会比较长，不知道理解对不对</div>2019-04-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/08/d1/3c7747ef.jpg" width="30px"><span>Grubby🐑</span> 👍（21） 💬（2）<div>bug是tryConvertToWriteLock返回的write stamp没有重新赋值给stamp</div>2019-04-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/36/d2/c7357723.jpg" width="30px"><span>发条橙子 。</span> 👍（14） 💬（2）<div>老师 ， 我看事例里面成员变量都给了一个 final 关键字 。 请问这里给变量加 final的用意是什么 ，仅仅是为了防止下面方法中代码给他赋新的对象么 。 我在平常写代码中很少有给变量加 final 的习惯， 希望老师能指点一下 😄</div>2019-04-15</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/c7/dc/9408c8c2.jpg" width="30px"><span>ban</span> 👍（9） 💬（1）<div>老师，你好，
如果我在前面long stamp = sl.readLock();升级锁后long ws = sl.tryConvertToWriteLock(stamp);
这个 stamp和ws是什么关系来的，是sl.unlockRead(是关stamp还是ws)。两者有什么区别呢</div>2019-04-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/8c/4e/b81969fa.jpg" width="30px"><span>南北少卿</span> 👍（7） 💬（1）<div>jdk源码StampedLock中的示例，if (ws != 0L) 时使用了stamp=ws</div>2019-05-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/8d/a6/22c37c91.jpg" width="30px"><span>楊_宵夜</span> 👍（5） 💬（1）<div>王老师, 您好, 文章中的StampedLock模板, 只适用于单机应用吧? 如果是集群部署, 那还是得用数据库乐观锁, 是吗??</div>2019-06-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/8c/4e/b81969fa.jpg" width="30px"><span>南北少卿</span> 👍（4） 💬（1）<div>这个获取锁返回的stamp,可以理解成上锁后的钥匙吗?</div>2020-06-19</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/DYAIOgq83eoVRER40LhyAmwlCqszX6s02Ix04Yztia9UIFrcm3JV9gHmbswvffqCW0KentRGVrPJuibyzJlpcW5g/132" width="30px"><span>ttang</span> 👍（4） 💬（3）<div>老师，ReadWriteLock锁和StampedLock锁都是可以同时读的，区别是StampedLock乐观读不加锁。那StampedLock比ReadWriteLock性能高的原因就是节省了加读锁的性能损耗吗？另外StampedLock用乐观读的时候是允许一个线程获取写锁的，是不是可以理解为StampedLock对写的性能更高，会不会因为写锁获取概率增大大，导致不能获取读锁。导致StampedLock读性能反而没有ReadWriteLock高？</div>2019-04-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/0c/c2/bad34a50.jpg" width="30px"><span>张洋</span> 👍（3） 💬（1）<div>王老师还有一个问题，最近做一些关于秒杀的业务，是不是可以用到乐观读的性质。
将库存量放在redis里边，然后所有的节点操作的时候通过缓存读出来，在代码逻辑里边对库存加一个
乐观读的操作。然后库存量等于0 的时候再去和数据库进行交互。  这样做会存在并发安全问题吗。</div>2019-04-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/33/1f/35b68f47.jpg" width="30px"><span>on the way</span> 👍（3） 💬（1）<div>有点没看明白示例interrupt那个代码里的 Thread.sleep（100）…</div>2019-04-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/16/c8/980776fc.jpg" width="30px"><span>走马</span> 👍（2） 💬（1）<div>您好，老师，我一直有个疑惑， 类似ERP的系统，它的程序代码本身没做并发处理，但是卖的时候会和客户说不同并发价格不一样，它是怎么做到的 ？ 是由一个独立的软件来处理并发吗？</div>2019-12-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/4e/3a/86196508.jpg" width="30px"><span>linqw</span> 👍（1） 💬（1）<div>从头重新看一篇，也自己大致写了下对StampedLock的源码分析https:&#47;&#47;juejin.im&#47;editor&#47;posts&#47;5d00a6c8e51d45105d63a4ed，老师有空帮忙看下哦</div>2019-06-15</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTKZSibeTatZ2ImL5Xu3QqdTWQs5nyQAxDlsm3m0KicP3TN6icJqYricvhjOFfTB2B3oLInU45CC9LtqMA/132" width="30px"><span>狂风骤雨</span> 👍（1） 💬（1）<div>老师，你上章讲的ReadWriteLock，说的是当有一个线程在执行写操作时所有的读线程都被阻塞，本章你又提了一下ReadWriteLock，说的是当有多个线程进行读操作时，所有的写操作都被阻塞，这样是</div>2019-05-06</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/1c/82/74ab79df.jpg" width="30px"><span>等我先变个身</span> 👍（1） 💬（1）<div>validate也无法保证一致性是吗？如果是那么应该怎么用validate？</div>2019-04-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/4a/96/99466a06.jpg" width="30px"><span>Laughing</span> 👍（0） 💬（1）<div>课后题的代码就是官方的实例，这里在成功升锁之后没有把得到的写锁ws赋值给`stamp`变量，这样最后解锁时会报IllegalMonitorStateException的异常。</div>2021-03-29</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/DYAIOgq83eoEcoSRAWRtibKK8RHPc7XibzcyGEfDsUFOXRJWtfd2u549Qa4KpicFNpeq16IqK2KSp9rkF2hrMXDLg/132" width="30px"><span>小小米</span> 👍（0） 💬（1）<div>return Math.sqrt( curX * curX + curY * curY);
在执行这句的时候，因为已经释放了悲观读锁，变量又被其他线程改了怎么办？是不是应该把这句也放在try块里？请老师解答。</div>2020-06-03</li><br/><li><img src="" width="30px"><span>Geek_qomxrt</span> 👍（0） 💬（1）<div>老师好，对于数据库的乐观读锁的例子，虽然很巧妙，但有点疑问，除非应用场景是version不对就不允许update，如果应用场景只是互斥并发的update，我觉得应该利用数据库自身特性就足够，例如postgresql中update语句会锁表（http:&#47;&#47;www.postgres.cn&#47;docs&#47;10&#47;explicit-locking.html#LOCKING-TABLES），不太需要您说的这个方法就可以实现并发的update。</div>2019-10-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/30/8a/b5ca7286.jpg" width="30px"><span>业余草</span> 👍（0） 💬（1）<div>挺好的专栏，但是大多数人写业务逻辑用不到这些技术！</div>2019-09-25</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/6LaITPQ4Lk5fZn8ib1tfsPW8vI9icTuSwAddiajVfibPDiaDvMU2br6ZT7K0LWCKibSQuicT7sIEVmY4K7ibXY0T7UQEiag/132" width="30px"><span>尔东橙</span> 👍（0） 💬（1）<div>老师，乐观读升级为悲观读锁是，如果写操作还在进行怎么办？</div>2019-07-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/89/f4/b3dacf1a.jpg" width="30px"><span>VERITAS</span> 👍（0） 💬（1）<div>老师你好，请问官方示例URL是多少，没有找到</div>2019-07-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/9f/41/82306dfe.jpg" width="30px"><span>包子</span> 👍（0） 💬（1）<div>老师，一直有个问题想不明白，就是对一个变量的读和写是否会存在线程安全问题。
文章中举例是同时对x和y进行读写操作，那xy的读写不能保证原子性，所以需要用到锁。
如果是对一个变量x的读和写，我们对x加volatile，保证其多线程的可见性是不是就可以了？</div>2019-04-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/8b/ec/dc03f5ad.jpg" width="30px"><span>张天屹</span> 👍（0） 💬（1）<div>说到数据库乐观锁，有个问题想请教老师，比如spring使用事务的时候，底层就已经使用了读写相关的锁来保证并发了，在我们的程序中还需要显式的使用乐观锁机制来保证并发安全吗</div>2019-04-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/7d/da/780f149e.jpg" width="30px"><span>echo＿陈</span> 👍（8） 💬（0）<div>以前看过java并发编程实战，讲jdk并发类库……不过那个书籍是jdk1.7版本……所以是头一次接触StempLock……涨知识了</div>2019-04-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/0e/1f/d0472177.jpg" width="30px"><span>厉害了我的国</span> 👍（4） 💬（1）<div>分布式场景下，java的锁还有用武之地吗？感觉就是玩具啊。。</div>2020-03-16</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/f8/bb/8b2ba45d.jpg" width="30px"><span>冯传博</span> 👍（4） 💬（1）<div>解释一下 cpu 飙升的原因呗</div>2019-04-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/30/c1/2dde6700.jpg" width="30px"><span>密码123456</span> 👍（4） 💬（0）<div>悲观锁和乐观锁。悲观锁，就是普通的锁。乐观锁，就是无锁，仅增加一个版本号，在取完数据验证一下版本号。如果不一致那么就进行悲观锁获取锁。能够这么理解吗？</div>2019-04-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/97/4a/0da51831.jpg" width="30px"><span>夕阳武士</span> 👍（2） 💬（0）<div>int getAnd() {
        long stamp = stampedLock.tryOptimisticRead();
        System.out.println(Thread.currentThread().getName() + &quot;,乐观读：x: &quot; + x + &quot;,y: &quot; + y);
        if (!stampedLock.validate(stamp)) {
            stamp = stampedLock.readLock();
            try {
                System.out.println(Thread.currentThread().getName() + &quot;,悲观读锁：x: &quot; + x + &quot;,y: &quot; + y);
            } catch (Exception e) {
                e.printStackTrace();
            } finally {
                stampedLock.unlock(stamp);
            }
        }
        return x + y;
    }

    void set(int x, int y) {
        long stamp = stampedLock.writeLock();
        try {
            this.x = x;
            this.y = y;
            System.out.println(&quot;写锁开始赋值。。。。。&quot;);
        } catch (Exception e) {
            e.printStackTrace();
        } finally {
            stampedLock.unlock(stamp);
        }
    }

运行结果：
Thread-9927,乐观读：x: 0,y: 0
Thread-9920,乐观读：x: 0,y: 0
Thread-9923,乐观读：x: 0,y: 0
Thread-9902,乐观读：x: 0,y: 0
写锁开始赋值。。。。。
Thread-9996,乐观读：x: 22,y: 33
Thread-9993,乐观读：x: 22,y: 33
Thread-9994,乐观读：x: 22,y: 33
Thread-9990,乐观读：x: 22,y: 33
Thread-9997,乐观读：x: 0,y: 0
Thread-9899,乐观读：x: 0,y: 0
Thread-9987,乐观读：x: 22,y: 33
Thread-9997,悲观读锁：x: 22,y: 33
Thread-9986,乐观读：x: 22,y: 33
Thread-9992,乐观读：x: 22,y: 33
Thread-9891,乐观读：x: 22,y: 33
Thread-9899,悲观读锁：x: 22,y: 33
Thread-9983,乐观读：x: 22,y: 33

写个demo验证一下，从Thread-9997这个线程的改变，可以看出升级锁的过程。</div>2021-04-27</li><br/>
</ul>