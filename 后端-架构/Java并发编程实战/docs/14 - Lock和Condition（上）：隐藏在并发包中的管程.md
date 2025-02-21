Java SDK并发包内容很丰富，包罗万象，但是我觉得最核心的还是其对管程的实现。因为理论上利用管程，你几乎可以实现并发包里所有的工具类。在前面[《08 | 管程：并发编程的万能钥匙》](https://time.geekbang.org/column/article/86089)中我们提到过在并发编程领域，有两大核心问题：一个是**互斥**，即同一时刻只允许一个线程访问共享资源；另一个是**同步**，即线程之间如何通信、协作。这两大问题，管程都是能够解决的。**Java SDK并发包通过Lock和Condition两个接口来实现管程，其中Lock用于解决互斥问题，Condition用于解决同步问题**。

今天我们重点介绍Lock的使用，在介绍Lock的使用之前，有个问题需要你首先思考一下：Java语言本身提供的synchronized也是管程的一种实现，既然Java从语言层面已经实现了管程了，那为什么还要在SDK里提供另外一种实现呢？难道Java标准委员会还能同意“重复造轮子”的方案？很显然它们之间是有巨大区别的。那区别在哪里呢？如果能深入理解这个问题，对你用好Lock帮助很大。下面我们就一起来剖析一下这个问题。

## 再造管程的理由

你也许曾经听到过很多这方面的传说，例如在Java的1.5版本中，synchronized性能不如SDK里面的Lock，但1.6版本之后，synchronized做了很多优化，将性能追了上来，所以1.6之后的版本又有人推荐使用synchronized了。那性能是否可以成为“重复造轮子”的理由呢？显然不能。因为性能问题优化一下就可以了，完全没必要“重复造轮子”。
<div><strong>精选留言（30）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/13/55/a3/88cbb981.jpg" width="30px"><span>　</span> 👍（122） 💬（8）<div>我觉得:不会出现死锁，但会出现活锁</div>2019-03-30</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/67/ab/facff632.jpg" width="30px"><span>小华</span> 👍（97） 💬（5）<div>有可能活锁，A，B两账户相互转账，各自持有自己lock的锁，都一直在尝试获取对方的锁，形成了活锁</div>2019-03-30</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTIBarfQrgZjEW8uUgvQckubEIFwNCJL93OygIgx3fCkObgRzSdo2baVWRd1C8mV6VDGKuoBFic4ZZA/132" width="30px"><span>xiyi</span> 👍（77） 💬（1）<div>存在活锁。这个例子可以稍微改下，成功转账后应该跳出循环。加个随机重试时间避免活锁</div>2019-03-30</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/4a/45/04a13bf9.jpg" width="30px"><span>bing</span> 👍（69） 💬（5）<div>文中说的公平锁和非公平锁，是不按照排队的顺序被唤醒，我记得非公平锁的场景应该是线程释放锁之后，如果来了一个线程获取锁，他不必去排队直接获取到，应该不会入队吧。获取不到才进吧</div>2019-03-30</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/4f/a5/71358d7b.jpg" width="30px"><span>J.M.Liu</span> 👍（35） 💬（1）<div>1.这个是个死循环啊，有锁没群，都出不来。
2.如果抛开死循环，也会造成活锁，状态不稳定。当然这个也看场景，假如冲突窗口很小，又在单机多核的话，活锁的可能性还是很小的，可以接受</div>2019-03-30</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/e8/99/0ea71e63.jpg" width="30px"><span>森呢</span> 👍（25） 💬（5）<div>老师，你好，这是我第二遍研读你的课程了，每一遍都收获很大。第一次写留言有点紧张。
你上面写的jdk利用内存模型的三条规则来保证可见性，是正确的。但我觉得好像描述的理由好像不充分，我不知道我理解的对不对，请老师解答一下
我的理解应该是 ：1）释放锁成功后，写state的值 （unlock&gt;state-=1） 顺序性
2）获取锁前，读state值（state&gt;lock）顺序性
3）传递性  unlock&gt;lock

下面是jdk的源码
final boolean nonfairTryAcquire(int acquires) {
    final Thread current = Thread.currentThread();&#47;&#47;获取当前线程实例
    int c = getState();&#47;&#47;获取state变量的值,即当前锁被重入的次数
    if (c == 0) {   &#47;&#47;state为0,说明当前锁未被任何线程持有
        if (compareAndSetState(0, acquires)) { &#47;&#47;以cas方式获取锁
            setExclusiveOwnerThread(current);  &#47;&#47;将当前线程标记为持有锁的线程
            return true;&#47;&#47;获取锁成功,非重入
        }
    }
    else if (current == getExclusiveOwnerThread()) { &#47;&#47;当前线程就是持有锁的线程,说明该锁被重入了
        int nextc = c + acquires;&#47;&#47;计算state变量要更新的值
        if (nextc &lt; 0) &#47;&#47; overflow
            throw new Error(&quot;Maximum lock count exceeded&quot;);
        setState(nextc);&#47;&#47;非同步方式更新state值
        return true;  &#47;&#47;获取锁成功,重入
    }
    return false;     &#47;&#47;走到这里说明尝试获取锁失败
}

</div>2019-07-04</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/4e/3a/86196508.jpg" width="30px"><span>linqw</span> 👍（25） 💬（15）<div>class Account {
  private int balance;
  private final Lock lock
          = new ReentrantLock();
  &#47;&#47; 转账
  void transfer(Account tar, int amt){
	boolean flag = true;
    while (flag) {
      if(this.lock.tryLock(随机数，NANOSECONDS)) {
        try {
          if (tar.lock.tryLock(随机数，NANOSECONDS)) {
            try {
              this.balance -= amt;
              tar.balance += amt;
	      flag = false;
            } finally {
              tar.lock.unlock();
            }
          }&#47;&#47;if
        } finally {
          this.lock.unlock();
        }
      }&#47;&#47;if
    }&#47;&#47;while
  }&#47;&#47;transfer
}
感觉可以这样操作</div>2019-04-07</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/d9/93/098e5ef5.jpg" width="30px"><span>海鸿</span> 👍（21） 💬（4）<div>突然有个问题：
cpu层面的原子性是单条cpu指令。
java层面的互斥（管程）保证了原子性。
这两个原子性意义应该不一样吧？
我的理解是cpu的原子性是不受线程调度影响，指令要不执行了，要么没执行。而java层面的原子性是在锁的机制下保证只有一个线程执行，其余等待，此时cpu还是可以进行线程调度，使运行中的那个线程让出cpu时间，当然了该线程还是掌握锁。
我这样理解对吧？</div>2019-03-30</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/28/9c/73e76b19.jpg" width="30px"><span>姜戈</span> 👍（14） 💬（1）<div>我也觉得是存在活锁，而非死锁。存在这种可能性：互相持有各自的锁，发现需要的对方的锁都被对方持有，就会释放当前持有的锁，导致大家都在不停持锁，释放锁，但事情还没做。当然还是会存在转账成功的情景，不过效率低下。我觉得此时需要引入Condition，协调两者同步处理转账！</div>2019-03-30</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/9a/43/d6291e76.jpg" width="30px"><span>Q宝的宝</span> 👍（14） 💬（3）<div>老师，本文在讲述如何保证可见性时，分析示例--“线程 T1 对 value 进行了 +=1 操作后，后续的线程 T2 能否看到 value 的正确结果？“时，提到三条Happen-Before规则，这里在解释第2条和第3条规则时，似乎说反了，正确的应该是，根据volatile变量规则，线程T1的unlock()操作Happen-Before于线程T2的lock()操作，所以，根据传递性规则，线程 T1 的 value+=1操作Happen-Before于线程T2的lock()操作。请老师指正。</div>2019-03-30</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/d5/75/75dab2b3.jpg" width="30px"><span>羊三</span> 👍（10） 💬（1）<div>用非阻塞的方式去获取锁，破坏了第五章所说的产生死锁的四个条件之一的“不可抢占”。所以不会产生死锁。

用锁的最佳实践，第三个“永远不在调用其他对象的方法时加锁”，我理解其实是在工程规范上避免可能出现的锁相关问题。</div>2019-03-30</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/cd/67/23fab87a.jpg" width="30px"><span>张鑫</span> 👍（9） 💬（1）<div>公平锁和非公平锁，公平锁唤醒策略就是谁等待时间长，就唤醒谁。非公平锁，有可能等待时间短。
对于公平锁和非公平锁我有不同的理解。

个人理解：公平锁是直接先进入AQS同步队列，抢占锁。非公平锁，是先抢占锁，若没有抢到则进入AQS同步队列，等待唤醒。

非公平锁代码：
	final void lock() {
            if (compareAndSetState(0, 1))
                setExclusiveOwnerThread(Thread.currentThread());
            else
                acquire(1);
        }
公平锁：
	 final void lock() {
            acquire(1);
        }

acquire(1)是当前线程抢占锁，若没有抢到则加入到同步队列中。公平锁和非公平锁逻辑一致。</div>2019-09-25</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/b3/c5/7fc124e2.jpg" width="30px"><span>Liam</span> 👍（9） 💬（1）<div>1 不会出现死锁，因为不存在阻塞的情况
2 线程较多的情况会导致部分线程始终无法获取到锁，导致活锁</div>2019-03-30</li><br/><li><img src="" width="30px"><span>zyz</span> 👍（7） 💬（1）<div>老师，lock是用aqs实现的，aqs是用了volatile＋cas操作系统原子操作保证线程安全的，这个也是管程吗？</div>2019-08-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/02/02/1080b30c.jpg" width="30px"><span>朱小豪</span> 👍（7） 💬（1）<div>应该是少了个break跳出循环，然后这个例子是会产生死锁的，因为满足了死锁产生的条件。</div>2019-03-30</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/06/1e/51ad425f.jpg" width="30px"><span>tdytaylor</span> 👍（5） 💬（3）<div>老师，关于这个问题，我思考之后觉得不会出现死锁，但是没看出为什么会出现活锁</div>2019-05-15</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/a3/1f/c94facb8.jpg" width="30px"><span>nodlee</span> 👍（3） 💬（1）<div>T1                    T2
lock(1)               lock(1)
  	getState              getState
value += 1;           value += 1;
unlock(1);            unlock(1); 
	getState              getState
	setState              setState
T1 和 T2 的操作序列可以简化为上面的内容，我的理解：T1 unlock 最后会写 state, 而 T2 的 lock 首先读 state, 根据 volatile 写优先于读的原则，所以 T1 的 unlock() 操作 Happens-Before T2 的 lock() 操作； 不知道这样理解有没有问题？</div>2020-04-24</li><br/><li><img src="https://wx.qlogo.cn/mmopen/vi_32/DYAIOgq83eqLcWH3mSPmhjrs1aGL4b3TqI7xDqWWibM4nYFrRlp0z7FNSWaJz0mqovrgIA7ibmrPt8zRScSfRaqQ/132" width="30px"><span>易儿易</span> 👍（3） 💬（1）<div>老师，notifyAll()在面对公平锁和非公平锁的时候，是不是效果就一样了？所有等待队列中的线程全部被唤醒，统统到入口等待队列中排队？这些被唤醒的线程不用根据等待时间排队再放入入口等待队列中了吧？</div>2019-04-04</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/98/3b/5af90c80.jpg" width="30px"><span>右耳听海</span> 👍（3） 💬（1）<div>请问state=1先读取是怎么得出来的，还有lock和unlock的方法对state都是写操作，怎么用到valiate规则的，valiate规则不是读取操作先与写操作吗，这个地方两个都是写操作</div>2019-03-31</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/7d/8e/bc1a990d.jpg" width="30px"><span>link</span> 👍（2） 💬（1）<div>请问老师一个问题。AQS实现的锁，阻塞唤醒线程使用的是park&#47;unpark方法。synchronized关键字实现的锁，在底层也是park&#47;unpark。这两种锁底层实现可以认为是一致的吗。如果是一致的。那么lock接口也是重量级锁了。</div>2019-09-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/f3/7f/2dd9409b.jpg" width="30px"><span>xinglichea</span> 👍（2） 💬（1）<div>2.永远只在访问可变的成员变量时加锁

老师，请问下，访问可变的成员变量时加锁方案，能否用volatile变量替代？如果可以，在并发能力上有什么区别？</div>2019-08-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/71/4c/2cefec07.jpg" width="30px"><span>静水流深</span> 👍（2） 💬（3）<div>以前学并发编程时候很吃力，就是坚持学完了本章后，我有种豁然开朗的感觉！谢谢老师！这个专栏，强烈建议涨价！！</div>2019-08-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/67/8a/babd74dc.jpg" width="30px"><span>锦</span> 👍（2） 💬（1）<div>文中提到JAVA SDK 里面Lock也是JAVA对管程的另一种实现，那么想必也是符合管程的工作原理，即内部封装共享变量和条件变量等待队列和操作方法。那么其可见性为什么不能通过管程中锁的happens-before规则来保证呢？</div>2019-04-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/5f/73/bb3dc468.jpg" width="30px"><span>拒绝</span> 👍（2） 💬（1）<div>老师您好：
   那在解决这个活锁问题时，是在获取其他对象锁前面（tar.lock.tryLock()）加个随机线程睡眠时间？还是《java编程：设计原则与模式》中的第三条，永远不在调用其他对象时加锁；去掉（tar.lock.tryLock()） 这个锁来解决活锁呢？</div>2019-03-31</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/DYAIOgq83er78PmxPDq4a3vNuvvX10fiaBC4FZ7XXuOX1nMjhCIqiaHWfpjfd5CDoVVB0GRGveChNmkSmuy7smxQ/132" width="30px"><span>Geek_7a9e2c</span> 👍（1） 💬（1）<div>关于非公平锁的解释与其他的资料有点出入，其他资料讲非公平锁的场景是当锁释放后，如果刚好有个线程在尝试获取锁，则直接给这个线程，而不用在队列里唤醒一个线程，因为唤醒一个线程需要的时间比较多，而你举例的场景是唤醒的可能不是从队列头部唤醒，而是随机从队列里拿出来一个线程</div>2021-11-01</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/24/ad/26/767527f6.jpg" width="30px"><span>Owen</span> 👍（1） 💬（1）<div>“解锁 Happens-Before 于后续对这个锁的加锁”，这个原则是只针对synchronized，与Lock无关吗？</div>2021-02-04</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTK0NwSicic81RbxQPraALLtK44KOSahvRlvic8B5yD0RX43xKaMDGMibJZnhBe0BY0IibWFpErzXPuyZNg/132" width="30px"><span>Geek_8a997f</span> 👍（1） 💬（1）<div>老师，有个疑惑请教一下，您的文章中提到，synchronized不能响应中断，是指线程被中断，需要自己读取中断标志并自行处理终止，这种的不算响应中断么？</div>2019-09-01</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/e5/a5/fae40ac3.jpg" width="30px"><span>倚梦流</span> 👍（1） 💬（4）<div>会出现活锁和死循环，老师你好，这是我的优化后的代码，运用了之前学过的知识，优先获取id值比较小的资源，请老师指点是否有不足之处，谢谢！
    void transfer6(Account tar,int amt){
        boolean isOver=false;
        Account left=this;
        Account right=tar;
        if(left.id&gt;right.id){
            left=tar;
            right=this;
        }
        Thread th=Thread.currentThread();
        while (!th.isInterrupted() &amp;&amp; !isOver){
            if(left.lock.tryLock()){
                try{
                    if(right.lock.tryLock()){
                        try{
                            System.out.println(&quot;账号：&quot;+this.id+&quot;开始转账啦！,转出金额：&quot;+amt);
                            if(this.balance&gt;=amt){
                                this.balance-=amt;
                                tar.balance+=amt;
                                System.out.println(&quot;转账成功！&quot;);
                            }else{
                                System.out.println(&quot;转账失败，余额不足！&quot;);
                            }
                            isOver=true;
                            System.out.println(&quot;转入账号:&quot;+this.id+&quot; 余额：&quot;+this.balance);
                            System.out.println(&quot;转出账号:&quot;+tar.id+&quot; 余额：&quot;+tar.balance);
                            System.out.println(&quot;转账结束！&quot;);
                        }finally {
                            right.lock.unlock();
                        }
                    }
                }finally {
                    left.lock.unlock();
                }
            }
        }
    }</div>2019-07-06</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/c1/1b/e08d42f8.jpg" width="30px"><span>尹圣</span> 👍（1） 💬（1）<div>public class Main {

    static volatile int state = 0;

    public static long account = 0;

    public static void main(String[] args) throws InterruptedException {

        for (int i = 0; i &lt; 100000; i++) {
            new Thread(() -&gt; {
                new Main().addAccount();
            }).start();
        }

        Thread.sleep(6000);
        System.out.println(account);
    }

    private void addAccount() {
        &#47;&#47;  线程不安全
        state = 1;   &#47;&#47;----1
        account++;   &#47;&#47;----2
        state = 0;   &#47;&#47;----3
    }
}

老师，有个疑问，如果按照volatile的Happens-Before这里的程序也应该是线程安全的，但实际上不是线程安全的，问题出在哪呢？</div>2019-04-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/52/3c/d6fcb93a.jpg" width="30px"><span>张三</span> 👍（1） 💬（1）<div>可重入函数的线程安全是不是由函数内部的可重入锁保证的呢？</div>2019-04-01</li><br/>
</ul>