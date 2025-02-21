在开发中我们经常会碰到“池”的概念，比如数据库连接池、内存池、线程池、常量池等。为什么需要“池”呢？程序运行的本质，就是通过使用系统资源（CPU、内存、网络、磁盘等）来完成信息的处理，比如在JVM中创建一个对象实例需要消耗CPU和内存资源，如果你的程序需要频繁创建大量的对象，并且这些对象的存活时间短，就意味着需要进行频繁销毁，那么很有可能这部分代码会成为性能的瓶颈。

而“池”就是用来解决这个问题的，简单来说，对象池就是把用过的对象保存起来，等下一次需要这种对象的时候，直接从对象池中拿出来重复使用，避免频繁地创建和销毁。在Java中万物皆对象，线程也是一个对象，Java线程是对操作系统线程的封装，创建Java线程也需要消耗系统资源，因此就有了线程池。JDK中提供了线程池的默认实现，我们也可以通过扩展Java原生线程池来实现自己的线程池。

同样，为了提高处理能力和并发度，Web容器一般会把处理请求的工作放到线程池里来执行，Tomcat扩展了原生的Java线程池，来满足Web容器高并发的需求，下面我们就来学习一下Java线程池的原理，以及Tomcat是如何扩展Java线程池的。

## Java线程池

简单的说，Java线程池里内部维护一个线程数组和一个任务队列，当任务处理不过来的时，就把任务放到队列里慢慢处理。
<div><strong>精选留言（30）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/10/d3/6e/281b85aa.jpg" width="30px"><span>永光</span> 👍（31） 💬（8）<div>观察 Tomcat 线程池和 Java 原生线程池的区别，其实就是在第 3 步，Tomcat 在线程总数达到最大数时，不是立即执行拒绝策略，而是再尝试向任务队列添加任务，添加失败后再执行拒绝策略。  
问题： 
感觉这两种方式都一样呀，前corePoolSize都是直接创建线程来处理。后续都是先放在队列里面，满了在创建临时线程来处理。  Tomcat线程池，在达到max时 再次检测，并尝试插入队列有什么意义呢？我理解再次检测队列也是满的呀？
2、
</div>2019-06-18</li><br/><li><img src="" width="30px"><span>世纪猛男</span> 👍（9） 💬（7）<div>关于今日的思考题 getPoolSize.  用Volatile去修饰一个变量不可行，因为变更过程，会基于之前的pool size，无法做到原子操作。 用atomic 也不合适  并发量高的时候 会导致 大量的更新失败， 持续消耗CPU。  所以还不如加锁来的痛快。 请教老师的想法</div>2019-06-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/ca/bd/a51ae4b2.jpg" width="30px"><span>吃饭饭</span> 👍（7） 💬（5）<div>老师，TaskQueue 重写了 offer 方法的关键是什么？是 TaskQueue(int capacity) ，只是把无界变有界了吗？每台看明白 offer 具体的改变是什么</div>2019-07-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/17/11/6b/8034959a.jpg" width="30px"><span>迎风劲草</span> 👍（7） 💬（1）<div>老师，核心线程如果超过keeplive时间，是否也会回收？还有如果我的队列中还有等待执行的runable,这时候kill 进程，时候需要等到所有runable被执行要，进程才结束吗？</div>2019-06-18</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTKl06gDibQ7aO1g1jgH9Koy2jcxpLCiavoia14REXotyVUsUvT0wkv9Oqk6wbyjK03SVt8MgFfsibe51g/132" width="30px"><span>13963865700</span> 👍（4） 💬（2）<div>老师，您好，请问：
1.Tomcat在默认队列长度无限制的情况下，是不是不会触发拒绝策略，即使线程数达到maxQueueSize也一直把任务放队列中？
2.这种情况会不会拖垮Tomcat，发生内存溢出？

</div>2019-06-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/79/4b/740f91ca.jpg" width="30px"><span>-W.LI-</span> 👍（4） 💬（1）<div>李老师好。我有个问题，原生队列是在队列满时新建线程处理。然后当线程达到最大线程数的时候，不就是队列已满，线程也开满了么。Tomcat补获异常后再往队列里放一次，只是为了做后的努力争取不丢任务么?</div>2019-06-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/05/7f/a7df049a.jpg" width="30px"><span>Standly</span> 👍（4） 💬（3）<div>感觉直接读workers.size()就可以了么，因为创建线程和销毁线程的方法都加锁了，而且是同一把锁，不懂为啥getPoolSize()方法还要额外加锁？</div>2019-06-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/17/71/6fc00748.jpg" width="30px"><span>HARDMAN</span> 👍（3） 💬（1）<div>请教老师，如果线程池已满，任务队列也满了，那么tomcat会拒绝后面的请求，这时如何进一步增强tomcat的处理能力，让它能同时处理更多请求呢？</div>2019-07-06</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/0f/9f/3f87896c.jpg" width="30px"><span>Geek_8eedf1</span> 👍（1） 💬（1）<div>看明白了😂，老师，学习 Java 线程池有哪些需要注意的点呢？</div>2019-06-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/64/86/f5a9403a.jpg" width="30px"><span>yang</span> 👍（0） 💬（1）<div>结合老师的讲解去看，印象会更深刻，脉络和细节点也会变得清晰，给老师点赞!</div>2019-08-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/a4/9c/b32ed9e9.jpg" width="30px"><span>陆离</span> 👍（0） 💬（1）<div>corePoolSize的有什么设置的策略吗？
需要和CPU个数联系起来吗？</div>2019-06-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/53/3d/1189e48a.jpg" width="30px"><span>微思</span> 👍（19） 💬（0）<div>给李老师点赞👍解析得非常到位！</div>2019-06-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1e/f0/aa/6ba4a1ab.jpg" width="30px"><span>℡ㄨ和尚ふ</span> 👍（10） 💬（5）<div>我的理解是：比如核心线程数为4，总线程数为10个。通过execute方法提交个4个任务，消耗了4个核心线程，所以此时的getPoolSise得到的就是4个线程数。
当第5个任务调教到线程池中时，因为已经创建了4个核心的线程，此时会尝试放入队列taskQueue中
条件1：parent.getPoolSize() == parent.getMaximumPoolSize() -》 4 == 10不成立
条件2：parent.getSubmittedCount()&lt;=(parent.getPoolSize()) -》 5 &lt;= 4 不成立
条件3：parent.getPoolSize()&lt;parent.getMaximumPoolSize() -》 4 &lt; 10 成立
可以理解为此时线程池中只有4个线程，但是任务有5个，如果四个线程统统阻塞在自己的任务上的话，第5个任务是迟迟得不到执行的，也就是说5个任务超出了4个线程的处理能力，而且此时没有超出最大线程数限制，所以这里可以理解为任务队列的容量为0，创建一个新的线程进行处理。
此时当前线程数有了5个。
当第6个任务进来的时候，如果前5个线程都阻塞在自己的任务上的话，之后的分析过程和前面类似。
但是假设5个线程中有一个任务已经执行完毕了，那么此时线程池中的未完成任务数为5，线程数也为5，就表示有一个线程是空闲的，那么 5 &lt;= 5 满足条件2，就将当前第5个任务加入到任务队列当中，由空闲线程从任务队列中取出进行执行。
我的理解是taskQueue队列的容量是动态变化的，取决于当前线程池中的空闲的线程数。但是当已创建线程数已经等于最大限制线程数的时候，任务队列就退化成了无界队列，这样来讲的话，默认情况下感觉拒绝策略是没有机会执行的（可以通过设置 maxQueueSize 参数来限制任务队列的长度，这样就可以执行拒绝策略了），不知道理解的对不对</div>2021-10-16</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/13/b9/69b92608.jpg" width="30px"><span>吴大山</span> 👍（8） 💬（4）<div>Tomcat 线程池扩展了原生的 ThreadPoolExecutor，通过重写 execute 方法实现了自己的任务处理逻辑：
1. xxx
2. 再来任务的话，就把任务添加到任务队列里让所有的线程去抢，如果队列满了就创建临时线程。
3. xxx
4. xxx

我细看了一下第二步代码：
方法定位：org.apache.tomcat.util.threads.TaskQueue#offer
逻辑定位：if (parent.getPoolSize()&lt;parent.getMaximumPoolSize()) return false;

这么看逻辑好像是：再来任务的话，如果线程数少于maximumPoolSize时，都会优先使用线程，而不会入队</div>2019-10-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/3d/c9/a1e6a307.jpg" width="30px"><span>沐</span> 👍（4） 💬（3）<div>平时开发的Web系统通常都有大量的 IO 操作，比方说查询数据库、查询缓存等等。任务在执行 IO 操作的时候 CPU就空闲了下来，这时如果增加执行任务的线程数而不是把任务暂存在队列中，就可以在单位时间内执行更多的任务，大大提高了任务执行的吞吐量。
Tomcat 使用的线程池就不是 JDK 原生的线程池，而是做了一些改造，当线程数超过 coreThreadCount 之后会优先创建线程，直到线程数到达 maxThreadCount，这样就比较适合于 Web 系统大量 IO 操作的场景了
                                                                                                                               --摘自《高并发系统40问》</div>2021-11-01</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/83/c8/5ce842f6.jpg" width="30px"><span>maybe</span> 👍（2） 💬（0）<div>1、java线程池内部维护一个数组和队列，当任务处理不过来的时候把任务放队列里慢慢处理
2、ThreadPoolExecutor核心类，有这些参数corePoolSize（核心线程数）、maximumPoolSize（最大线程数）、keepAliveTime（线程空闲时间）、unit（空闲时间单位）、workQueue（任务队列）、threadFactory（线程创建工厂）、handler（拒绝策略）
3、ThreadPoolExecutor这些参数的作用是这样的：当提交任务的时候，如果线程数还未到达核心线程数，那么就直接创建新线程。继续提交任务，如果线程数到达核心线程数，那么就把任务放入队列中。如果队列满了还有任务提交过来，那么就需要创建临时线程，如果还有任务来，线程数到达了最大线程数，那么就会执行拒绝策略。threadFactory用来扩展原生的线程工厂，比如可以设置一个有意义的线程名称。keepAliveTime, unit这两个参数的意义是如果高峰期过了，线程都比较闲了，这些线程去任务队列使用poll方法拉活（poll方法设置了超时时间），如果拉不到活，那么就把这些线程销毁。
4、FixedThreadPool、CachedThreadPool都是ThreadPoolExecutor的定制版，设置了不同的参数而已。
FixedThreadPool设置了（nThreads, nThreads, 0L, TimeUnit.MILLISECONDS, new LinkedBlockingQueue()）这几个参数，固定线程数组长度，LinkedBlockingQueue默认是个无界队列，当任务处理不来，都丢到队列里等待。
CachedThreadPool设置了（0, Integer.MAX_VALUE, 60L, TimeUnit.SECONDS, new SynchronousQueue()），最大线程数设置为 Integer.MAX_VALUE，相当于无限制，忙不过来的时候就不断创建临时线程。它的任务队列是 SynchronousQueue，表明队列长度为 0。
5、tomcat的线程池也是ThreadPoolExecutor的定制版，不同的是如果线程数已大于核心线程数，当继续创建临时线程达到最大线程数的时候，并没有直接执行拒绝策略，而是重写了excute逻辑，当发生RejectedExecutionException时候进行了捕获，再尝试把任务往队列里放，如果还是满的，那么再执行拒绝策略。目的就是再次检查，如果任务被消耗了，那么就继续保留任务了，尽可能的保留任务。


</div>2020-08-06</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/fb/59/e4fa1482.jpg" width="30px"><span>chen</span> 👍（1） 💬（1）<div>我感觉老师在这一课上讲得不够完善，tomcat的线程池和原生线程还有一个不同点，就是当核心线程数满了，但是还未达到最大线程数量的时候，这时候直接触发非核心线程的创建，而不是加入队列。</div>2023-08-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/17/a3/95/b04d2746.jpg" width="30px"><span>FOCUS</span> 👍（1） 💬（0）<div>tomcat相当于综合了FixedThreadPool，CachedThreadPool各自的特点了， 优先使用线程处理，超过最大线程数就放在队列中等待处理</div>2022-05-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/cf/10/9fa2e5ba.jpg" width="30px"><span>进击的巨人</span> 👍（1） 💬（0）<div>既然要限制队列长度，为何不直接用arrayblockingquene啊</div>2020-11-20</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/2UXuSevhia94o9Eky4OfMuSictaldxcqpjGuvRCOcvjIIoVBAENLEZbv2lgwmwC8icK1ZrUcneNtiaeFBV8MT3uzNg/132" width="30px"><span>Gavin</span> 👍（1） 💬（3）<div>如果高峰过去了，线程池比较闲了怎么办？临时线程使用 poll（keepAliveTime, unit）方法从工作队列中拉活干，请注意 poll 方法设置了超时时间，如果超时了仍然两手空空没拉到活，表明它太闲了，这个线程会被销毁回收。

这个只回收maximunPoolSize吧</div>2020-09-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/70/9e/9337ca8e.jpg" width="30px"><span>jaryoung</span> 👍（1） 💬（0）<div>课后题，获取一次设置成一个局部变量，局部变量属于线程安全，无惧</div>2019-08-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/e8/4b/57fa0e34.jpg" width="30px"><span>brianway</span> 👍（1） 💬（4）<div>所以通过重写TaskQueue的offer方法，达到的效果就是将无界队列变成了有界队列，且队列长度限制=当前线程数，不知道我理解的对不对。举个例子，corePoolSize=4，maximumPoolSize=10，那来一个任务起一个线程，直到线程数为4，然后再来的任务就入队列，如果队列里任务积累到4个，随着任务继续增多，会新起线程处理，队列长度限制也会依次变成5，6，7，8，一直到10。</div>2019-08-07</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/f7/ee/6eeb58a3.jpg" width="30px"><span>calljson</span> 👍（1） 💬（1）<div>空闲线程到队列取任务，能否讲解下原理，最好附上源码，谢谢</div>2019-07-02</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/b3/c5/7fc124e2.jpg" width="30px"><span>Liam</span> 👍（1） 💬（1）<div>可以用atomic原子变量替换锁吧</div>2019-06-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1b/b7/d4/263e04e6.jpg" width="30px"><span>秋名山小司机</span> 👍（0） 💬（0）<div>这里明显有问题，请老师再看一下
- tomcat线程池：核心线程数-&gt;最大线程数-&gt;队列-&gt;抛弃
- 常规线程池：核心线程数-&gt;队列-&gt;最大线程数-&gt;抛弃</div>2024-08-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/f3/06/8da1bf0c.jpg" width="30px"><span>Fredo</span> 👍（0） 💬（0）<div>看最新版本的tomcat已经是无锁了：
```java
    @Override
    public boolean offer(Runnable o) {
      &#47;&#47;we can&#39;t do any checks
        if (parent==null) {
            return super.offer(o);
        }
        &#47;&#47;we are maxed out on threads, simply queue the object
        if (parent.getPoolSizeNoLock() == parent.getMaximumPoolSize()) {
            return super.offer(o);
        }
        &#47;&#47;we have idle threads, just add it to the queue
        if (parent.getSubmittedCount() &lt;= parent.getPoolSizeNoLock()) {
            return super.offer(o);
        }
        &#47;&#47;if we have less threads than maximum force creation of a new thread
        if (parent.getPoolSizeNoLock() &lt; parent.getMaximumPoolSize()) {
            return false;
        }
        &#47;&#47;if we reached here, we need to add it to the queue
        return super.offer(o);
    }
```</div>2023-07-25</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/22/28/e8/7734b8d3.jpg" width="30px"><span>P</span> 👍（0） 💬（0）<div>感觉不准确，定制线程池+定制队列，合起来达到的效果就是：优先创建线程，再使用工作队列。</div>2023-02-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/80/46/9ccbf0d5.jpg" width="30px"><span>蔚蓝</span> 👍（0） 💬（0）<div>submittedCount，如果设置了队列长度，那么这个值维护就没意义了吧
</div>2022-11-21</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/6LaITPQ4Lk5fZn8ib1tfsPW8vI9icTuSwAddiajVfibPDiaDvMU2br6ZT7K0LWCKibSQuicT7sIEVmY4K7ibXY0T7UQEiag/132" width="30px"><span>尔东橙</span> 👍（0） 💬（0）<div>tomcat为什么线程都要定义成守护线程</div>2022-10-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/1d/d1/f427b83e.jpg" width="30px"><span>javaworker</span> 👍（0） 💬（0）<div>老师，有了tomcat的线程池，为什么还要设置java的线程池，或者数据库的线程池呐？比如tomcat核心线程10，最大线程数20，也就是最多也就20个并发，起到了防止并发的作用。Java程序中用为什么还要用线程池呐？Java中的线程和tomcat中的线程，是同一个线程吗？</div>2022-08-16</li><br/>
</ul>