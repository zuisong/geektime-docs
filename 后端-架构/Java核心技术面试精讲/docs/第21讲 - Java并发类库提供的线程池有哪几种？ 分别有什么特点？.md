我在[专栏第17讲](http://time.geekbang.org/column/article/9103)中介绍过线程是不能够重复启动的，创建或销毁线程存在一定的开销，所以利用线程池技术来提高系统资源利用效率，并简化线程管理，已经是非常成熟的选择。

今天我要问你的问题是，Java并发类库提供的线程池有哪几种？ 分别有什么特点？

## 典型回答

通常开发者都是利用Executors提供的通用线程池创建方法，去创建不同配置的线程池，主要区别在于不同的ExecutorService类型或者不同的初始参数。

Executors目前提供了5种不同的线程池创建配置：

- newCachedThreadPool()，它是一种用来处理大量短时间工作任务的线程池，具有几个鲜明特点：它会试图缓存线程并重用，当无缓存线程可用时，就会创建新的工作线程；如果线程闲置的时间超过60秒，则被终止并移出缓存；长时间闲置时，这种线程池，不会消耗什么资源。其内部使用SynchronousQueue作为工作队列。
- newFixedThreadPool(int nThreads)，重用指定数目（nThreads）的线程，其背后使用的是无界的工作队列，任何时候最多有nThreads个工作线程是活动的。这意味着，如果任务数量超过了活动队列数目，将在工作队列中等待空闲线程出现；如果有工作线程退出，将会有新的工作线程被创建，以补足指定的数目nThreads。
- newSingleThreadExecutor()，它的特点在于工作线程数目被限制为1，操作一个无界的工作队列，所以它保证了所有任务的都是被顺序执行，最多会有一个任务处于活动状态，并且不允许使用者改动线程池实例，因此可以避免其改变线程数目。
- newSingleThreadScheduledExecutor()和newScheduledThreadPool(int corePoolSize)，创建的是个ScheduledExecutorService，可以进行定时或周期性的工作调度，区别在于单一工作线程还是多个工作线程。
- newWorkStealingPool(int parallelism)，这是一个经常被人忽略的线程池，Java 8才加入这个创建方法，其内部会构建[ForkJoinPool](https://docs.oracle.com/javase/9/docs/api/java/util/concurrent/ForkJoinPool.html)，利用[Work-Stealing](https://en.wikipedia.org/wiki/Work_stealing)算法，并行地处理任务，不保证处理顺序。
<div><strong>精选留言（30）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/10/d6/8d/7db04ad3.jpg" width="30px"><span>I am a psycho</span> 👍（64） 💬（3）<div>通过看源码可以得知，core和max都是1，而且通过FinalizableDelegatedExecutorService进行了包装，保证线程池无法修改。同时shutdown方法通过调用interruptIdleWorkers方法，去停掉没有工作的线程，而shutdownNow方法是直接粗暴的停掉所有线程。无论是shutdown还是shutdownNow都不会进行等待，都会直接将线程池状态设置成shutdown或者stop，如果需要等待，需要调用awaitTernination方法。查找了一下threadFactory的使用，只找到了在worker创建的时候，用来初始化了线程。</div>2018-06-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/d4/f3/129d6dfe.jpg" width="30px"><span>李二木</span> 👍（52） 💬（5）<div>我觉得还有一点很重要，就是放在线程池中的线程要捕获异常，如果直接抛出异常，每次都会创建线程，也就等于线程池没有发挥作用，如果大并发下一直创建线程可能会导致JVM挂掉。最近遇到的一个坑</div>2018-06-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/f8/ba/d28174a9.jpg" width="30px"><span>Geek_zbvt62</span> 👍（27） 💬（11）<div>疑问，为什么当初sun的线程池模式要设计成队列满了才能创建非核心线程？类比其他类似池的功能实现，很多都是设置最小数最大数，达到最大数才向等待队列里加入，比如有的连接池实现。</div>2018-06-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/b3/9e/c88ac921.jpg" width="30px"><span>沈琦斌</span> 👍（15） 💬（1）<div>老师，我想问的是cache的线程池大小是1，每次还要新创建，那和我自己创建而不用线程池有什么区别？</div>2018-06-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/99/af/d29273e2.jpg" width="30px"><span>饭粒</span> 👍（11） 💬（2）<div>写了个简单demo玩了下。
创建线程池会初始化线程工厂，工作线程是在提交任务的创建的。工作线程在执行任务中抛出异常，再次提交任务会又新建工作线程。newFixedThreadPool 正常执行任务时会优先创建线程已达到核心线程数，不会优先复用空闲工作线程。
```
&#47;**
 * 线程池工作线程执行任务抛出异常
 *&#47;
@Test
public void test03() throws InterruptedException {
    &#47;&#47; java.util.concurrent.Executors.DefaultThreadFactory.DefaultThreadFactory 构造线程工厂
    ExecutorService executorService = Executors.newCachedThreadPool();
    Runnable task = new Runnable() {
        @Override
        public void run() {
            System.out.println(&quot;hello world&quot;);
            &#47;&#47; 抛出异常
            throw new RuntimeException();
        }
    };
    executorService.execute(task);
    &#47;&#47; 提交任务通过 DefaultThreadFactory.newThread() 创建线程
    TimeUnit.SECONDS.sleep(2);
    &#47;&#47; 前一个工作线程在执行任务中抛出异常，再提交任务又会新建工作线程
    executorService.execute(task);

    TimeUnit.SECONDS.sleep(3);
}
```</div>2019-01-15</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/05/e5/aa579968.jpg" width="30px"><span>王磊</span> 👍（6） 💬（1）<div>core和max应该都是1。验证的方法是自己写一个Threadlocal, 里面有相应创建线程的日志，然后把它传入创建线程池。</div>2018-06-25</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/05/aa/3c7c00a4.jpg" width="30px"><span>GK java</span> 👍（5） 💬（1）<div>线程池到底需不需要关闭</div>2019-01-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/cb/64/4afad7da.jpg" width="30px"><span>欣</span> 👍（5） 💬（2）<div>杨老师，我照着文章翻看源码，下面那块是不是不太对？
----------------
Executors 目前提供了 5 种不同的线程池创建配置：

newSingleThreadExecutor，它创建的是个 FinalizableDelegatedExecutorService

newSingleThreadScheduledExecutor 创建的是 ScheduledThreadPoolExecutor</div>2018-07-04</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/6e/64/456c280d.jpg" width="30px"><span>镰仓</span> 👍（3） 💬（1）<div>听了一段时间课程，质量很高。我的需求是android JavaVM</div>2018-06-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/33/92/99530cee.jpg" width="30px"><span>灰飞灰猪不会灰飞.烟灭</span> 👍（2） 💬（1）<div>老师 放入队列中的线程是直接调用start方法还是把队列中的线程放入线程工厂，让线程工厂执行？
另外，怎么判断一个线程是否执行完成呢？（只有执行完成才返回结果）谢谢老师</div>2018-06-25</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/67/ae/f7e8ce72.jpg" width="30px"><span>JasonLai</span> 👍（1） 💬（1）<div>老师你好，我在学些线程池时候遇到一个说法，创建线程池不推荐使用executors
而是使用threadpoolexecutor去创建。首先executor都是继承于threadpoolexecutor 其次是编写的线程池更为明确运行规则，有助于规避资源耗尽的风险。请老师分析下这种说法，其次是您的观点</div>2019-02-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/99/af/d29273e2.jpg" width="30px"><span>饭粒</span> 👍（1） 💬（1）<div>Geotz那本java并发实战线程池大小计算还有个CPU利用率？
线程数 = CPU 核数 × CPU利用率 ×（1 + 平均等待时间 &#47; 平均工作时间）</div>2019-01-15</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/06/9b/ade9c3bd.jpg" width="30px"><span>洗头用酱油</span> 👍（0） 💬（1）<div>老师，我看NewSingleExecutor 所有的队列是LinkedBlockingQueue，它好像是有界的队列不是无界的吧？</div>2018-08-03</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/83/08/91caf5c1.jpg" width="30px"><span>Harry陈祥</span> 👍（36） 💬（11）<div>老师您好。有次面试，面试官问：为什么java的线程池当核心线程满了以后，先往blockingQueue中存任务，queue满了以后才会创建非核心线程？ 是在问，为什么要这么设计？
请问这个问题应该怎么回答？</div>2019-02-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/5a/13/3160996d.jpg" width="30px"><span>nb Ack</span> 👍（17） 💬（1）<div>阻塞性：
BlockQueue存入任务队列时是没有阻塞，使用的是offer，无阻塞添加方法。
BlockQueue取出任务队列时是有阻塞，有超时使用poll取值，无超时使用take阻塞方法取值

添加任务逻辑：
1.当任务数小于核心线程数，新建核心线程来执行任务
2.任务数大于核心线程数，队列不满，放入任务队列
3.任务数大于核心线程数，队列已满，新建线程执行
4.任务数大于核心线程数，队列已满，工作线程已达最大线程数，拒绝任务，抛出异常（而不是阻塞任务，等待进入队列）
</div>2019-05-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/68/5f/2b4abbb6.jpg" width="30px"><span>不告诉你</span> 👍（4） 💬（0）<div>无论是创建核心线程还是非核心线程，都需要获取全局锁。只有在工作队列满了以后才去创建非核心线程，应该就是为了在时间上尽量延后非核心线程的创建，为了线程池的性能做考虑吧。</div>2019-02-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/81/f0/695ca05f.jpg" width="30px"><span>Ifdevil</span> 👍（3） 💬（1）<div>老师您好，我看了线程池源码，里面是用HashSet存放worker的，为什么这里用hashset呢？去重？线程池需要去重吗？</div>2019-03-04</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/06/08/855abb02.jpg" width="30px"><span>Seven.Lin澤耿</span> 👍（2） 💬（1）<div>corePoolSize=maxPoolSize=1

 ThreadFactory threadFactory = new ThreadFactory(){
    @Override
    public Thread newThread(Runnable r) {
        System.out.println(&quot;new thread ...&quot;);
        return new Thread(r,&quot;Thread-&quot;+System.currentTimeMillis());
    }
};

ExecutorService executorService = Executors.newSingleThreadExecutor(threadFactory);

executorService.execute(()-&gt;{
    System.out.println(&quot;A Run&quot;);
});

executorService.execute(()-&gt;{
    System.out.println(&quot;B Run Exception&quot;);
    throw new RuntimeException();
});

executorService.execute(() -&gt; {
    System.out.println(&quot;C Run&quot;);
});

结果，发生两次创建线程，也就是发生异常之后，原先线程会被替换掉，具体看ThreadPoolExecutor的processWorkerExit()方法</div>2020-03-07</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/53/e1/dd7b3206.jpg" width="30px"><span>何義</span> 👍（2） 💬（1）<div>请教一下，多线程下面是否可以再嵌套多线程</div>2019-12-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/ae/8a/e67def95.jpg" width="30px"><span>念头通达</span> 👍（1） 💬（0）<div>原来SingleThreadPoolExecutor是使用LingkBlockQueue维护工作队列 ，第一个节点 创建Worker 线程 ，之后的线程使用 enqueue(node)方法构建链 </div>2020-04-16</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/e7/7e/34fa766f.jpg" width="30px"><span>康</span> 👍（1） 💬（0）<div>我的理解，设置非核心线程的目的是防止任务数的段时间激增，导致任务数过多，从而核心线程处理时间太长。正常情况下要保证线程数小于核心线程数，非核心线程会过一段时间就被移出，保证了资源的利用，而核心一般不会变少</div>2019-03-03</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/81/e6/6cafed37.jpg" width="30px"><span>旅途</span> 👍（0） 💬（0）<div>这篇非常好，关键点都讲到了</div>2023-05-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/18/d1/fe/2ca6f40a.jpg" width="30px"><span>影山飞雄</span> 👍（0） 💬（0）<div>想问下这个单线程池情况下，内部的包装类的作用是什么？
A wrapper class that exposes only the ExecutorService methods  * of an ExecutorService implementation.
这是源代码的注释，是为了只暴露ExecutorService的方法，而不暴露父类AbstractExecutorService的方法吗？</div>2020-10-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1b/36/47/8e80082c.jpg" width="30px"><span>大成尊者</span> 👍（0） 💬（0）<div>如果利用 newSingleThreadExecutor() 创建一个线程池，corePoolSize、maxPoolSize 等都是什么数值？ThreadFactory 可能在线程池生命周期中被使用多少次？怎么验证自己的判断？
答：corePoolSize、maxPoolSize 都是1，ThreadFactory只会被调用1次。验证倒没想到怎么验证，不过new Thread()的时候，指定了线程名称中带了AtomicInteger，可以看这个值是多少，如果是1，就说明值执行了一次。</div>2020-06-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/ae/8a/e67def95.jpg" width="30px"><span>念头通达</span> 👍（0） 💬（0）<div>ThreadPoolExecutor.java 616行创建Worder的时候使用ThreadFactory构建线程</div>2020-04-16</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/ce/db/72b7c594.jpg" width="30px"><span>飘香剑雨</span> 👍（0） 💬（0）<div>size都是1吧</div>2020-03-22</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/E3XKbwTv6WTssolgqZjZCkiazHgl2IdBYfwVfAcB7Ff3krsIQeBIBFQLQE1Kw91LFbl3lic2EzgdfNiciaYDlJlELA/132" width="30px"><span>rike</span> 👍（0） 💬（3）<div>文章中“建议按照 CPU 核的数目 N 或者 N+1。”，这里的n是指多少？</div>2020-02-21</li><br/><li><img src="" width="30px"><span>Paul Shan</span> 👍（0） 💬（1）<div>我个人更倾向于用rxjava解决多线程的问题而不是直接操作线程池。</div>2019-11-26</li><br/><li><img src="" width="30px"><span>Paul Shan</span> 👍（0） 💬（0）<div>newCachedThreadPool() 60s时间窗口缓存线程，适合的场景是系统需要的线程数在每分钟是差不多的。
newFixedThreadPool(int nThreads)，设定了活动线程的最大值，如果超过这个数目，线程进入等待状态。适合场景例如总共只有n个CPU，为了提高效率，最多的并行也就是n。
newSingleThreadExecutor()，单线程执行，可以保证多个线程的执行顺序。
newSingleThreadScheduledExecutor() 和 newScheduledThreadPool(int corePoolSize) 周期性调度
newWorkStealingPool(int parallelism) 并行处理线程</div>2019-11-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/e2/cf/eb6cea42.jpg" width="30px"><span>rain</span> 👍（0） 💬（0）<div>学习了一下，自己总结一下：https:&#47;&#47;www.jhonrain.org&#47;2018&#47;09&#47;14&#47;%E9%AB%98%E5%B9%B6%E5%8F%91-%E7%BA%BF%E7%A8%8B%E6%B1%A0%E5%89%96%E6%9E%90&#47;</div>2019-08-18</li><br/>
</ul>