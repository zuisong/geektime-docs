前几天老板突然匆匆忙忙过来，说对账系统最近越来越慢了，能不能快速优化一下。我了解了对账系统的业务后，发现还是挺简单的，用户通过在线商城下单，会生成电子订单，保存在订单库；之后物流会生成派送单给用户发货，派送单保存在派送单库。为了防止漏派送或者重复派送，对账系统每天还会校验是否存在异常订单。

对账系统的处理逻辑很简单，你可以参考下面的对账系统流程图。目前对账系统的处理逻辑是首先查询订单，然后查询派送单，之后对比订单和派送单，将差异写入差异库。

![](https://static001.geekbang.org/resource/image/06/fe/068418bdc371b8a1b4b740428a3b3ffe.png?wh=1142%2A626)

对账系统流程图

对账系统的代码抽象之后，也很简单，核心代码如下，就是在一个单线程里面循环查询订单、派送单，然后执行对账，最后将写入差异库。

```
while(存在未对账订单){
  // 查询未对账订单
  pos = getPOrders();
  // 查询派送单
  dos = getDOrders();
  // 执行对账操作
  diff = check(pos, dos);
  // 差异写入差异库
  save(diff);
} 
```

## 利用并行优化对账系统

老板要我优化性能，那我就首先要找到这个对账系统的瓶颈所在。

目前的对账系统，由于订单量和派送单量巨大，所以查询未对账订单getPOrders()和查询派送单getDOrders()相对较慢，那有没有办法快速优化一下呢？目前对账系统是单线程执行的，图形化后是下图这个样子。对于串行化的系统，优化性能首先想到的是能否**利用多线程并行处理**。

![](https://static001.geekbang.org/resource/image/cd/a5/cd997c259e4165c046e79e766abfe2a5.png?wh=1142%2A507)

对账系统单线程执行示意图

所以，这里你应该能够看出来这个对账系统里的瓶颈：查询未对账订单getPOrders()和查询派送单getDOrders()是否可以并行处理呢？显然是可以的，因为这两个操作并没有先后顺序的依赖。这两个最耗时的操作并行之后，执行过程如下图所示。对比一下单线程的执行示意图，你会发现同等时间里，并行执行的吞吐量近乎单线程的2倍，优化效果还是相对明显的。
<div><strong>精选留言（30）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/12/0a/a4/828a431f.jpg" width="30px"><span>张申傲</span> 👍（257） 💬（13）<div>我觉得老师的问题其实是两个:
1.为啥要用线程池，而不是在回调函数中直接调用？
2.线程池为啥使用单线程的？

我的考虑:
1.使用线程池是为了异步操作，否则回掉函数是同步调用的，也就是本次对账操作执行完才能进行下一轮的检查。
2.线程数量固定为1，防止了多线程并发导致的数据不一致，因为订单和派送单是两个队列，只有单线程去两个队列中取消息才不会出现消息不匹配的问题。</div>2019-05-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/4f/a5/71358d7b.jpg" width="30px"><span>J.M.Liu</span> 👍（183） 💬（10）<div>老师，CyclicBarrier的回调函数在哪个线程执行啊？主线程吗？比如这里的最后一段代码中，循环会在回调的时候阻塞吗？
如果是这样的话，那check函数岂不是可以直接作为回调函数了呀，并不需要线程池了啊</div>2019-04-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/4f/78/c3d8ecb0.jpg" width="30px"><span>undifined</span> 👍（80） 💬（5）<div>线程池大小为1是必要的，如果设置为多个，有可能会两个线程 A 和 B 同时查询，A 的订单先返回，B 的派送单先返回，造成队列中的数据不匹配；所以1个线程实现生产数据串行执行，保证数据安全

如果用Future 的话可以更方便一些：

        CompletableFuture&lt;List&gt; pOrderFuture = CompletableFuture.supplyAsync(this::getPOrders);
        CompletableFuture&lt;List&gt; dOrderFuture = CompletableFuture.supplyAsync(this::getDOrders);
        pOrderFuture.thenCombine(dOrderFuture, this::check)
                    .thenAccept(this::save);

老师这样理解对吗，谢谢老师
</div>2019-04-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/76/23/31e5e984.jpg" width="30px"><span>空知</span> 👍（68） 💬（7）<div>老师,关于CyclicBarrier回调函数,请教下
自己写了个 CyclicBarrier的例子,回调函数总是在计数器归0时候执行,但是线程T1 T2要等回调函数执行结束之后才会再次执行...看了下CyclicBarrier 的源码,当内部计数器 index == 0时候, 

final Runnable command = barrierCommand;
                    
if (command != null)
                        
	command.run();
没有开启子线程吧.也就是说 对账还是同步执行的,结束之后才是下一次的查询</div>2019-04-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/25/7f/473d5a77.jpg" width="30px"><span>曾轼麟</span> 👍（65） 💬（4）<div>老师推荐您使用ThreadPoolExecutor去实现线程池，并且实现里面的RejectedExecutionHandler和ThreadFactory，这样可以方便当调用订单查询和派送单查询的时候出现full gc的时候 dump文件 可以快速定位出现问题的线程是哪个业务线程，如果是CountDownLatch，建议设置超时时间，避免由于业务死锁没有调用countDown()导致现线程睡死的情况</div>2019-04-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/a2/f3/aa504fa6.jpg" width="30px"><span>波波</span> 👍（28） 💬（8）<div>思考题中，如果生产者比较快，消费者比较慢，生产者通知的时候，消费者还在对账，这个时候会怎么处理？会不会导致消费者错失通知，导致队列满了，但是消费者却没有收到通知。</div>2019-04-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/9c/7c/408c2a0b.jpg" width="30px"><span>nanquanmama</span> 👍（19） 💬（1）<div>最后的那个例子，业务逻辑的部分已经变得很不直观，并发控制的逻辑掩盖住了业务逻辑。请问一下老师，实际项目开发中，并发控制逻辑如何做，才能和业务逻辑分离出来？</div>2019-04-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/06/62/898449d3.jpg" width="30px"><span>... ...</span> 👍（18） 💬（3）<div>追问：如果线程池是单线程的话。那假如生产者速度快运check函数执行时间。那是不是就会出现堵塞情况了。久而久之，是不是会出现队列内存溢出</div>2019-04-12</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTK36t2flfxhzKygfLfdIHbK99M9D9w3v3bwAHUibJSFAs1ibswf7hbhkqL321k5SUjfiaWkkHeRBlibNA/132" width="30px"><span>Adam</span> 👍（15） 💬（1）<div>如果生产者比较快，消费者check还没对账完 会不会照成 队列越来越多 最后内存溢出了 ，有没有什么好的方案解决呢？</div>2019-06-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/ae/00/791d0f5e.jpg" width="30px"><span>忍者无敌1995</span> 👍（14） 💬（2）<div>有，如果为线程池有多个线程，则由于check()函数里面的两个remove并不是原子操作，可能导致消费错乱。假设订单队列中有P1，P2；派送队列中有D1,D2；两个线程T1,T2同时执行check，可能出现T1消费到P1,D2，T2消费到P2，D1，就是T1先执行pos.remove(0), 而后T2执行pos.remove(0);dos.remov(0);然后T1才执行dos.remove(0)的场景</div>2019-05-01</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/b2/c5/6ae0be56.jpg" width="30px"><span>木偶人King</span> 👍（14） 💬（1）<div>老师，最后checkAll（） 这里为什么new 了两个Thread  而不是使用线程池


</div>2019-04-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/c8/6b/0f3876ef.jpg" width="30px"><span>iron_man</span> 👍（13） 💬（3）<div>王老师，cyclicbarrier，具体是在什么时候清零计数器呢？是在所有线程await返回后还是在回调函数调用后？await和回掉函数的调用顺序是怎样的</div>2019-04-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/0b/34/f41d73a4.jpg" width="30px"><span>王盛武</span> 👍（12） 💬（2）<div>undefind同学的意思差不多对。                         只有一个线程的线程池，是因为，订单队列和派单队列读取数据存在竞态条件。 如果要开多个线程，则需要一个lock进行同步那两个remove方法。    个人推荐的思路是，如果生产者速度比消费者快的情况下，放入一个双向的阻塞队列尾部，每次从双向队列头部取两个对象，根据对象属性来区别订单类型，也能开多个线程进行check操作。  但本文业务里check速度很快，所以这个场景只需要开1个线程的线程池是合理的。</div>2019-04-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/5e/d0/e676ac19.jpg" width="30px"><span>梦典</span> 👍（11） 💬（1）<div>1.回调处理交给新开辟的线程执行，让当前处理继续进行，无需等待
2.使用线程池解决新开辟线程创建和销毁的开销问题
3.单线程使得两个队列的出队无需同步</div>2019-09-25</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/e4/e9/0dd3829f.jpg" width="30px"><span>aguan(^･ｪ･^)</span> 👍（11） 💬（2）<div>老师，问一个业务逻辑的问题，在从两个队列中分别取订单和派送单的做比较的时候，怎么保证这订单和派送单是一一对应的关系呢？如果派送单有漏单，那如何对账比较取结果时的数据是一一对应关系？</div>2019-04-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/6a/e8/4bb87c34.jpg" width="30px"><span>月马穿关</span> 👍（10） 💬（1）<div>感谢老师，一直不太明白什么时候用CyclicBarrier，今天看到案例了，刚看到join那段我想到了CompletableFuture

</div>2019-04-11</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/PiajxSqBRaELZPnUAiajaR5C25EDLWeJURggyiaOP5GGPe2qlwpQcm5e3ybib8OsP4tvddFDLVRSNNGL5I3SFPJHsA/132" width="30px"><span>null</span> 👍（7） 💬（1）<div>老师，您好！我有几个疑问：

1. 文章里提到：获取订单 getPOrders() 和获取派送订 getDOrders() 是相互独立、互不依赖的。
我们的订单系统通过 MQ 与派送系统进行数据交互，并且一个订单有可能生成多个派送单（仓库不同，拆单），想了好久，也没想到比较好的方式实现订单和派送单的查询操作可以并行处理。
如果每次只筛选过去一个小时未对账的订单，和过去一小时的派送单，当存在漏生成派送单时，系统发现不了（不知道是漏生成派送单，还是 MQ 没消费）。

2. 文章第二种方案，线程池多生成一个线程，专门用来处理 ( check &amp; save )，也能够实现查询和对账并行处理。因此不太能理解“一个线程等待多个线程”和“一组线程之间的相互等待”的区别。感觉 CountDownLatch 和 CyclicBarrier 都是 (check &amp; save) 线程在等待 getPOrders 和 getDOrders 线程。

3.文章最后一种方案，每次只查询一条改成一次查多条，这样可以减少查询的次数。check 的时候，也批量处理，吞吐量是不是会好一点吖。

谢谢老师！！</div>2019-05-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/ac/ef/494f56c3.jpg" width="30px"><span>crazypokerk</span> 👍（7） 💬（1）<div>请教一下老师，上面说的将CyclicBarrier计数器初始值设为2，假如当T1先执行完，然后执行await时减1，此时计数器为1大于0，等待，然后T2执行await时再减1，此时计数器为0，则唤醒T3执行，与此同时，将计数器重置为2，T1、T2继续开始执行，以此循环往复，可以这样理解吗？</div>2019-04-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/26/38/ef063dc2.jpg" width="30px"><span>Darren</span> 👍（6） 💬（1）<div>而且其实可以直接single线程池的，但是最好不要Executors提供的线程池，都有弊端，最好自定义线程池</div>2019-04-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/8c/4e/b81969fa.jpg" width="30px"><span>南北少卿</span> 👍（5） 💬（2）<div>CountDownLatch可以理解成主线程等待其他线程吗</div>2019-05-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/01/05/6435d2ef.jpg" width="30px"><span>IT小白</span> 👍（5） 💬（1）<div>这个示例确实将这两个工具类的使用讲清楚了，但是对于这个具体业务这么改造是不合理的。因为整个对账过程里的所有操作必须是原子的，这么拆分到多个线程里执行，这个原子性的保证相对来说比较复杂，示例中也没有考虑。我觉得这里的性能优化可以很简单，比如：搞一组线程，将所有订单平均分摊到这一组线程上，所有线程并行对账，每个线程做的活都一样～ 注意每个线程维护独立的数据库连接～</div>2019-04-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/07/29/e5537b9e.jpg" width="30px"><span>冲鸭</span> 👍（3） 💬（1）<div>会出现计数器被同一个线程减到0的情况吗？</div>2019-04-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/3d/51/9723276c.jpg" width="30px"><span>邋遢的流浪剑客</span> 👍（3） 💬（1）<div>使用了固定大小为1的线程池，check方法是非线程安全的，让它串行执行</div>2019-04-11</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTKNDKOCoZvCqoYVM1t97Q77QPLmRBGvOLYzFsh8073RicycoIuwGrIsCXpAFEyVBOxcyE3Ih1mr6Vw/132" width="30px"><span>Geek_bbbda3</span> 👍（2） 💬（3）<div>老师，在回调中先执行remove，在丢给线程池执行对账，该线程池设置多个线程，是否可以？
    Executor executor = Executors.newFixedThreadPool(10); 
    final CyclicBarrier barrier =
            new CyclicBarrier(2, () -&gt; {
                P p = pos.remove(0);
                D d = dos.remove(0);
                executor.execute(() -&gt; check(p, d));
            });</div>2019-09-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/d5/18/7f3b1af2.jpg" width="30px"><span>头晕的小骚年</span> 👍（2） 💬（1）<div>查询订单库和查询运单库会使订单队列和派送单队列各多一个数据，也会把CyclicBarrier计数器的值变为0，然后触发线程池里的check方法，执行对账操作，check方法是消费者，会消费一个数据。是不是check方法执行完后，线程才能继续查询订单库和运单库，让生产者生产数据？如果是这样的话，订单队列和派送单队列不是最多只能各有一个数据吗？这样的话，能达到优化性能的目的吗？</div>2019-04-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/52/3c/d6fcb93a.jpg" width="30px"><span>张三</span> 👍（2） 💬（1）<div>CyclicBarrier那段代码只要调用一次checkAll（）方法就会一直执行了吧？里边的每次循环都会在计数器等于0的时候自动回调check（）方法对账，然后两个线程分别进行下一次循环。</div>2019-04-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/18/44/d2/a36c09bd.jpg" width="30px"><span>全村的希望</span> 👍（1） 💬（1）<div>如果线程t2在查询运单库的时候执行很慢，在没有调用t2方法的barrier.await()时，而t1的while循环查询了两次订单库调用了两次barrier.await()的情况时，是不是也会执行check方法</div>2019-08-30</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/52/37/13b4c8aa.jpg" width="30px"><span>Vincent</span> 👍（1） 💬（1）<div>你好，我想问下你怎么保证双队列元素之间的一一对应关系，你这个是两个不同的查询</div>2019-04-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/b5/d4/e58e39f0.jpg" width="30px"><span>Geek_0quh3e</span> 👍（1） 💬（1）<div>看了源码，再结合本篇文章，对CyclicBarrier的理解更加深刻了。
回调函数调用的时机为最终使计数器为0的线程，然后再唤醒所有阻塞的线程，（见nextGeneration()）
private int dowait(boolean timed, long nanos)
        throws InterruptedException, BrokenBarrierException,
               TimeoutException {
        final ReentrantLock lock = this.lock;
        lock.lock();
        try {
			.........省略
            int index = --count;
            if (index == 0) {  &#47;&#47; tripped
                boolean ranAction = false;
                try {
                    final Runnable command = barrierCommand;
                    if (command != null)
                        command.run();
                    ranAction = true;
                    nextGeneration();&#47;&#47; 唤醒所有阻塞的线程，并自动重置count
                    return 0;
                } finally {
                    if (!ranAction)
                        breakBarrier();
                }
            }

            &#47;&#47; loop until tripped, broken, interrupted, or timed out
            for (;;) {
                try {
                    if (!timed)
                        trip.await();&#47;&#47;阻塞线程
                    else if (nanos &gt; 0L)
                        nanos = trip.awaitNanos(nanos);
                } catch (InterruptedException ie) {
					.....省略
            }
        } finally {
            lock.unlock();
        }
    }</div>2019-04-24</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/DYAIOgq83eqOOrv7cDhjs53c333nZPYJnsWt83CsBIdgYSWVI2ajkwicqCuunfN8nyRGNdShOTer9hWQzNutzBA/132" width="30px"><span>Geek_sj3wqh</span> 👍（1） 💬（1）<div>如果最后的线程池有两个线程，会有什么问题？老师能举个例子吗？想了好久没想出来啊，有点折磨人</div>2019-04-17</li><br/>
</ul>