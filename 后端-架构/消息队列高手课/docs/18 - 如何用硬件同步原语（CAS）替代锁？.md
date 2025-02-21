你好，我是李玥。上节课，我们一起学习了如何使用锁来保护共享资源，你也了解到，使用锁是有一定性能损失的，并且，如果发生了过多的锁等待，将会非常影响程序的性能。

在一些特定的情况下，我们可以使用硬件同步原语来替代锁，可以保证和锁一样的数据安全性，同时具有更好的性能。

在今年的NSDI（NSDI是USENIX组织开办的关于网络系统设计的著名学术会议）上，伯克利大学发表了一篇论文《[Confluo: Distributed Monitoring and Diagnosis Stack for High-speed Networks](http://www.usenix.org/conference/nsdi19/presentation/khandelwal)》，这个论文中提到的Confluo，也是一个类似于消息队列的流数据存储，它的吞吐量号称是Kafka的4～10倍。对于这个实验结论我个人不是很认同，因为它设计的实验条件对Kafka来说不太公平。但不可否认的是，Confluo它的这个设计思路是一个创新，并且实际上它的性能也非常好。

Confluo是如何做到这么高的吞吐量的呢？这里面非常重要的一个创新的设计就是，它使用硬件同步原语来代替锁，在一个日志上（你可以理解为消息队列中的一个队列或者分区），保证严格顺序的前提下，实现了多线程并发写入。

今天，我们就来学习一下，如何用硬件同步原语（CAS）替代锁？
<div><strong>精选留言（30）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/10/99/7b/0a056674.jpg" width="30px"><span>ponymm</span> 👍（54） 💬（2）<div>“CAS 和 FAA 在各种编程语言中，都有相应的实现，可以来直接使用，无论你是使用哪种编程语言，它底层使用的系统调用是一样的，效果也是一样的。” 李老师这句话有点小问题：car,faa并不是通过系统调用实现的，系统调用的开销不小，cas本来就是为了提升性能，不会走系统调用。事实上是在用户态直接使用汇编指令就可以实现</div>2019-09-03</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/14/17/8763dced.jpg" width="30px"><span>微微一笑</span> 👍（32） 💬（3）<div>老师好，实现了下CAS,代码连接：https:&#47;&#47;github.com&#47;shenyachen&#47;JKSJ&#47;blob&#47;master&#47;study&#47;src&#47;main&#47;java&#47;com&#47;jksj&#47;study&#47;casAndFaa&#47;CASThread.java。
对于FAA，通过查找资料，jdk1.8在调用sun.misc.Unsafe#getAndAddInt方法时，会根据系统底层是否支持FAA，来决定是使用FAA还是CAS。</div>2019-09-03</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/57/4f/6fb51ff1.jpg" width="30px"><span>奕</span> 👍（11） 💬（2）<div>NodeJS中，没有发现有关操作CpU原语CAS或者FAA的实现的</div>2019-09-03</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/7b/57/a9b04544.jpg" width="30px"><span>QQ怪</span> 👍（6） 💬（1）<div>MutxLock：https:&#47;&#47;github.com&#47;xqq1994&#47;algorithm&#47;blob&#47;master&#47;src&#47;main&#47;java&#47;com&#47;test&#47;concurrency&#47;MutxLock.java
CAS、FFA:
https:&#47;&#47;github.com&#47;xqq1994&#47;algorithm&#47;blob&#47;master&#47;src&#47;main&#47;java&#47;com&#47;test&#47;concurrency&#47;CAS.java
完成了老师的作业，好高兴</div>2019-09-03</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/52/3c/d6fcb93a.jpg" width="30px"><span>张三</span> 👍（3） 💬（3）<div>Java里边有支持FAA这种CPU指令的实现吗？以前没听说</div>2019-09-03</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/51/8d/09f28606.jpg" width="30px"><span>明日</span> 👍（2） 💬（1）<div>Java实现: https:&#47;&#47;gist.github.com&#47;imgaoxin&#47;a2b09715af99b993e30b44963cebc530</div>2019-09-03</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/b0/eb/43be030a.jpg" width="30px"><span>Sicily9</span> 👍（1） 💬（3）<div>有一个小疑问，关于原子性的话，有一个极端情况，多核并行情况下 两个线程 同时在执行一个cas原语 会有安全问题吗</div>2019-11-19</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/iaZdMmzM0Vfass2ukHOqGgSBbtJMwb4NxDvLdN3R67iczzPVdtF0F0WS0abvls3edQpOVxaUJBmlr2YxHzUpveIQ/132" width="30px"><span>衹是一支歌</span> 👍（0） 💬（1）<div>CAS FAA是不是只能用于单机情况下的资源控制访问呢？</div>2020-06-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/8d/c4/6f97daea.jpg" width="30px"><span>长期规划</span> 👍（0） 💬（1）<div>Python没找到CAS和FAA的实现</div>2019-10-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/33/1c/59a4e803.jpg" width="30px"><span>青舟</span> 👍（0） 💬（2）<div>https:&#47;&#47;github.com&#47;qingzhou413&#47;geektime-mq.git
做了1000万次加法，
Lock: 380ms
CAS: 200ms
FAA: 280ms</div>2019-09-04</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/19/d9/ff/b23018a6.jpg" width="30px"><span>Heaven</span> 👍（0） 💬（0）<div>https:&#47;&#47;github.com&#47;HeavenXin&#47;geektime_message_queue&#47;tree&#47;master&#47;src18</div>2021-02-07</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1f/27/be/b666abb4.jpg" width="30px"><span>tongZi</span> 👍（0） 💬（0）<div>“如果线程之间的碰撞非常频繁，经常性的反复重试，这个重试的线程会占用大量的 CPU 时间，随之系统的整体性能就会下降。”
老师你好，请问这个重试的线程为什么会占用“大量”的cpu时间？？
会比其它正常请求的线程，占用时间更多吗？？</div>2020-07-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1f/27/be/b666abb4.jpg" width="30px"><span>tongZi</span> 👍（0） 💬（1）<div>==对于 “CAS 和 FAA 在各种编程语言中，都有相应的实现”
我想起之前在操作数据的时候，为了并发的修改用户数据(Money)，当时的做法是
先Select出用户的Money
再对Money做操作
最后在Update的时候多附加一个条件（Money=OldMoney）==
老师您好，这个问题，如果cpu多核并行，假如极端情况，多线程同时去更新money字段，是否会有线程安全问题？？？</div>2020-07-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/43/79/18073134.jpg" width="30px"><span>test</span> 👍（0） 💬（0）<div>public class CASTest implements Runnable{
    private AtomicInteger account;
    private CountDownLatch latch;

    public CASTest(CountDownLatch latch, AtomicInteger account){
        this.account = account;
        this.latch = latch;
    }

    @Override
    public void run() {
        while (!account.compareAndSet(account.get(), account.get() + 1)){}
        latch.countDown();
    }

    public static void main(String[] args) throws InterruptedException {
        StopWatch stopWatch = new StopWatch();
        stopWatch.start();
        int THREAD_NUM = 10000;
        int cpuCore = Runtime.getRuntime().availableProcessors();
        AtomicInteger account = new AtomicInteger(0);
        CountDownLatch latch = new CountDownLatch(THREAD_NUM);
        ThreadPoolExecutor executor = new ThreadPoolExecutor(cpuCore + 1, THREAD_NUM, 0,
                TimeUnit.SECONDS, new LinkedBlockingQueue&lt;&gt;(65536));
        for(int i = 0;i &lt; THREAD_NUM;++i) {
            executor.execute(new CASTest(latch, account));
        }
        latch.await();
        System.out.println(account.get());
        System.out.println(stopWatch.getTime());
        executor.shutdown();
    }
}</div>2020-07-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/7e/99/c4302030.jpg" width="30px"><span>Khirye</span> 👍（0） 💬（0）<div>老师您好，想请教下如何检测线程碰撞是否频繁呢？</div>2020-06-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/6d/46/e16291f8.jpg" width="30px"><span>丁小明</span> 👍（0） 💬（0）<div>翻看了一下java中的unsafe类，虽然提供了faa的方法，但是实现还是通过cas，为什么java没有直接提供faa呢</div>2020-05-03</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTKDfO7wKibzpw4YsoqLRCHUKxX4rYRUh7m7RCdOwzWVaN9QLlhcU5ho3w2Qcpib1O69YPj65ib07xQBQ/132" width="30px"><span>努力呼吸</span> 👍（0） 💬（0）<div>public class Cas {
    private static AtomicInteger balance = new AtomicInteger(0);

    private static CountDownLatch countDownLatch = new CountDownLatch(10000);

    private static void transforFaa() {
        balance.addAndGet(1);
        countDownLatch.countDown();
    }

    private static void transforCas() {
        int oldVal = balance.get();
        int newVal = oldVal + 1;
        balance.compareAndSet(oldVal, newVal);
        countDownLatch.countDown();
    }

    public static void main(String[] args) throws InterruptedException {
        for (int j = 0; j &lt; 10000; j++) {
            CompletableFuture.runAsync(() -&gt; Cas.transforCas());
        }
        countDownLatch.await();
        System.out.println(balance.get());
    }
}</div>2020-03-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/07/36/d677e741.jpg" width="30px"><span>黑山老妖</span> 👍（0） 💬（0）<div>清晰</div>2020-02-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/18/57/f6/2c7ac1ad.jpg" width="30px"><span>Peter</span> 👍（0） 💬（0）<div>交作业：https:&#47;&#47;github.com&#47;PeterLu798&#47;MQ&#47;tree&#47;master&#47;src&#47;com&#47;lbj&#47;mq&#47;lock
LockBalance.java使用Java独占锁实现，平均耗时 300毫秒左右
CASBalance.java使用AtomicInteger实现，平均耗时250毫秒左右</div>2019-10-30</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/67/f4/9a1feb59.jpg" width="30px"><span>钱</span> 👍（0） 💬（0）<div>之前只知CAS，还有FAA，想必应该有一坨类似的原语。打卡，感谢，又增长了一点见识。</div>2019-09-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/5e/d0/e676ac19.jpg" width="30px"><span>梦典</span> 👍（0） 💬（0）<div>代码工程
https:&#47;&#47;github.com&#47;dlutsniper&#47;wy-ja-lock&#47;tree&#47;master&#47;src&#47;main&#47;java&#47;wy&#47;ja&#47;lock&#47;demo
试验耗时的环节，深刻体会JIT的强大，执行次数越多，耗时均值越低
JIT吗？执行越多速度越快？
关闭JIT -Xint &#47; -Djava.compiler=NONE
AccountDemoSynchronized 100次关闭前后
  开启 16.66ms 13.77ms 11.26ms
  关闭 93.14ms 102.12ms 81.13ms
AccountDemoCas 100次关闭前后
  开启 12.74ms 10.5ms 12.42ms
  关闭 82.48ms 74.7ms 77.09ms</div>2019-09-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/88/a7/fb383ef7.jpg" width="30px"><span>MaLu</span> 👍（0） 💬（0）<div>用户硬件同步原语来代替锁的效果，确实是一个好思路</div>2019-09-04</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/4d/fd/0aa0e39f.jpg" width="30px"><span>许童童</span> 👍（0） 💬（0）<div>老师讲得很好，对于我这种基础薄弱的，长见识了，感谢老师。</div>2019-09-03</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/4e/3a/86196508.jpg" width="30px"><span>linqw</span> 👍（0） 💬（0）<div>最近出差都落下了好些，找个空闲时间把这些实现下</div>2019-09-03</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTJOBwR7MCVqwZbPA5RQ2mjUjd571jUXUcBCE7lY5vSMibWn8D5S4PzDZMaAhRPdnRBqYbVOBTJibhJg/132" width="30px"><span>ヾ(◍°∇°◍)ﾉﾞ</span> 👍（0） 💬（0）<div>yiald感觉还是不是等一定周期使用是不是更好，如果系统线程多，线程的频繁切换带来的开销也不小，go的协程会好些</div>2019-09-03</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/5e/60/1c13626b.jpg" width="30px"><span>白小白</span> 👍（0） 💬（0）<div>打卡打卡！晚上回家做作业！</div>2019-09-03</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/f3/69/7039d03f.jpg" width="30px"><span>渔村蓝</span> 👍（0） 💬（0）<div>看完，先抢个沙发，晚点上链接。</div>2019-09-03</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/25/66/4835d92e.jpg" width="30px"><span>潘政宇</span> 👍（0） 💬（2）<div>go的语法太奇特了，代码中的done作用是什么啊</div>2019-09-03</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/18/e7/0f/fa840c1b.jpg" width="30px"><span>刘天鹏</span> 👍（0） 💬（3）<div>对于 “CAS 和 FAA 在各种编程语言中，都有相应的实现”
我想起之前在操作数据的时候，为了并发的修改用户数据(Money)，当时的做法是
先Select出用户的Money
再对Money做操作
最后在Update的时候多附加一个条件（Money=OldMoney）</div>2019-09-03</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/18/e7/0f/fa840c1b.jpg" width="30px"><span>刘天鹏</span> 👍（0） 💬（1）<div>https:&#47;&#47;gist.github.com&#47;liutianpeng&#47;6f72bca647be41705d68736a79246c2f
用Golang实现的版本,其实老师都已经实现了，Test和Benchmark都做了，果然操作时间 FAA &lt; CAS &lt; Mutex

另外还有一个问题 atomic.LoadXXX 这组函数是什么作用（或者说为了解决什么问题的?）
</div>2019-09-03</li><br/>
</ul>