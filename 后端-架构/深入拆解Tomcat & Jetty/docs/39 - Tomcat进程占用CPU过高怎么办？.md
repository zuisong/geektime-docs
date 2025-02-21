在性能优化这个主题里，前面我们聊过了Tomcat的内存问题和网络相关的问题，接下来我们看一下CPU的问题。CPU资源经常会成为系统性能的一个瓶颈，这其中的原因是多方面的，可能是内存泄露导致频繁GC，进而引起CPU使用率过高；又可能是代码中的Bug创建了大量的线程，导致CPU上下文切换开销。

今天我们就来聊聊Tomcat进程的CPU使用率过高怎么办，以及怎样一步一步找到问题的根因。

## “Java进程CPU使用率高”的解决思路是什么？

通常我们所说的CPU使用率过高，这里面其实隐含着一个用来比较高与低的基准值，比如JVM在峰值负载下的平均CPU利用率为40％，如果CPU使用率飙到80%就可以被认为是不正常的。

典型的JVM进程包含多个Java线程，其中一些在等待工作，另一些则正在执行任务。在单个Java程序的情况下，线程数可以非常低，而对于处理大量并发事务的互联网后台来说，线程数可能会比较高。

对于CPU的问题，最重要的是要找到是**哪些线程在消耗CPU**，通过线程栈定位到问题代码；如果没有找到个别线程的CPU使用率特别高，我们要怀疑到是不是线程上下文切换导致了CPU使用率过高。下面我们通过一个实例来学习CPU问题定位的过程。
<div><strong>精选留言（18）</strong></div><ul>
<li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/PiajxSqBRaEIvUlicgrWtibbDzwhLw5cQrDSy2JuE1mVvmXq11KQIwpLicgDuWfpp9asE0VCN6HhibPDWn7wBc2lfmA/132" width="30px"><span>a、</span> 👍（19） 💬（3）<div>1.使用了Java的newCachedThreadPool，因为最大线程数是int最大值
2.自定义线程池最大线程数设置不合理
3.线程池的拒绝策略，选择了如果队列满了并且线程达到最大线程数后，提交的任务交给提交任务线程处理</div>2019-08-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/6d/8f/81e282e2.jpg" width="30px"><span>802.11</span> 👍（9） 💬（2）<div>老师这些都是一些实时的操作，但是大部分情况CPU高的时候并没有及时的在服务器上观察，一旦错过了这个发生的时间点，事后该怎样去判断和定位呢</div>2019-08-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/6d/8f/81e282e2.jpg" width="30px"><span>802.11</span> 👍（4） 💬（3）<div> TIMED_WAITING 是什么意思呢？有什么寓意呢</div>2019-08-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/a4/9c/b32ed9e9.jpg" width="30px"><span>陆离</span> 👍（0） 💬（1）<div>容器在启动起来之后就被kill掉的原因有哪些？和CPU过高有关系吗</div>2019-08-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/78/c7/083a3a0b.jpg" width="30px"><span>新世界</span> 👍（5） 💬（0）<div>线程池和等待队列设置不合理以及拒绝策略设置不合理会导致线程数失控，比如线程池设置小，等到队列也不大，拒绝策略选择用主线程继续执行，瞬间大量请求，会导致等到队列占满，进而用主线程执行任务，导致tomcat线程被打满，线程数失控</div>2019-08-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/be/e6/7808520d.jpg" width="30px"><span>Edward Lee</span> 👍（3） 💬（0）<div>课后思考

之前做了一个与第三方系统的集成，在未设置读超时时间的前提下发生读超时（卡着接近2分钟），导致Tomcat线程耗尽，并同时出现假死情况</div>2020-12-06</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/0c/86/8e52afb8.jpg" width="30px"><span>花花大脸猫</span> 👍（1） 💬（0）<div>大量处理时间很长的请求，外加未规划的tomcat连接配置，会导致线程数随着请求量的增大无限递增。</div>2022-06-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/10/9f/40a9a568.jpg" width="30px"><span>JamesZhou</span> 👍（1） 💬（0）<div>排查CPU过高，发现一个小工具可以试试：https:&#47;&#47;github.com&#47;oldratlee&#47;useful-scripts&#47;blob&#47;dev-2.x&#47;docs&#47;java.md#-show-busy-java-threads</div>2020-05-31</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTL3xax4aG4h59x50C7LQ5K7BicvIEicakyfE0lV4Pyib6OsYc1jC7Qa37g2v8qhib5BQiaB2DfB4DMG5Cw/132" width="30px"><span>花花世界小人物</span> 👍（0） 💬（0）<div>Blocking 指的是一个线程因为等待临界区的锁（Lock 或者 synchronized 关键字）而被阻塞的状态，请你注意的是处于这个状态的线程还没有拿到锁

老师 Blocking状态只有synchronized阻塞的时候才会有这个状态。我试了一下ReentrantLock锁是WAITING
&quot;222&quot; #14 prio=5 os_prio=31 tid=0x00007f852d20a800 nid=0x9503 waiting on condition [0x0000000306dc1000]
   java.lang.Thread.State: WAITING (parking)
	at sun.misc.Unsafe.park(Native Method)
	- parking to wait for  &lt;0x000000076cb6eb48&gt; (a java.util.concurrent.locks.ReentrantLock$NonfairSync)
	at java.util.concurrent.locks.LockSupport.park(LockSupport.java:175)
	at java.util.concurrent.locks.AbstractQueuedSynchronizer.parkAndCheckInterrupt(AbstractQueuedSynchronizer.java:836)
	at java.util.concurrent.locks.AbstractQueuedSynchronizer.acquireQueued(AbstractQueuedSynchronizer.java:870)
	at java.util.concurrent.locks.AbstractQueuedSynchronizer.acquire(AbstractQueuedSynchronizer.java:1199)
	at java.util.concurrent.locks.ReentrantLock$NonfairSync.lock(ReentrantLock.java:209)
	at java.util.concurrent.locks.ReentrantLock.lock(ReentrantLock.java:285)
	at cn.labnetwork.service.order.requisition.RequisitionController$1.run(RequisitionController.java:123)
	at java.lang.Thread.run(Thread.java:750)</div>2023-03-03</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/43/3e/960d12cb.jpg" width="30px"><span>DY</span> 👍（0） 💬（0）<div>老师真牛</div>2021-05-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/51/0d/fc1652fe.jpg" width="30px"><span>James</span> 👍（0） 💬（0）<div>top -H -p 4361 最后一个指标全部显示java。。。而不是具体的线程名字。。</div>2021-03-31</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/07/d2/0d7ee298.jpg" width="30px"><span>惘 闻</span> 👍（0） 💬（0）<div>waiting是线程拿到过锁进入过临界区后因为等待条件而释放锁,blocking是从未拿到过锁从未进入过临界区.两个状态都是不占有锁的状态.老师我理解的对吗?</div>2021-01-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/83/c8/5ce842f6.jpg" width="30px"><span>maybe</span> 👍（0） 💬（0）<div>1、cpu使用过高定位思路：先看看有没有占用高得线程，如果没有择可以考虑线程数太多导致上下文切换带来的开销大
2、思考题：使用newcachedthreadpool，因为最大线程数为int最大值相当于无限制，会无限制创建线程。使用自定义线程池，设置和newcachedthreadpool差不多。</div>2020-08-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/19/c7/02/8346ebf6.jpg" width="30px"><span>Chris</span> 👍（0） 💬（1）<div>老师，线程栈那么多信息，怎么直接定位到了submit的问题呢</div>2020-07-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/4d/fd/0aa0e39f.jpg" width="30px"><span>许童童</span> 👍（0） 💬（0）<div>哪些情况可能导致程序中的线程数失控，产生大量线程呢？
创建线程池时参数是计算出来的，而计算的过程是有bug的，导致结果有问题，从而创建了大量线程。
这种需要对程序进行测试，线上持续进行性能监控，发现并解决问题。</div>2019-08-10</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/PiajxSqBRaEIvUlicgrWtibbDzwhLw5cQrDSy2JuE1mVvmXq11KQIwpLicgDuWfpp9asE0VCN6HhibPDWn7wBc2lfmA/132" width="30px"><span>a、</span> 👍（0） 💬（0）<div>1.使用了Java的newCachedThreadPool，因为最大线程数是int最大值
2.</div>2019-08-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/79/4b/740f91ca.jpg" width="30px"><span>-W.LI-</span> 👍（0） 💬（0）<div>用线程池创建线程，设置合理的最大线程数。
之前遇见过压测十几个接口200并发下cpu使用率90%可是看了大多都是4%消耗。当时确实发现全部加起来没到90%，最后也没找到原因，就不了了之了。。线上多加了太服务器</div>2019-08-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/47/65/cce8eb34.jpg" width="30px"><span>nimil</span> 👍（0） 💬（0）<div>👍赞</div>2019-08-10</li><br/>
</ul>