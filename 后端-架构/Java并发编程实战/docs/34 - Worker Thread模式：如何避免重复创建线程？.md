在[上一篇文章](https://time.geekbang.org/column/article/95098)中，我们介绍了一种最简单的分工模式——Thread-Per-Message模式，对应到现实世界，其实就是委托代办。这种分工模式如果用Java Thread实现，频繁地创建、销毁线程非常影响性能，同时无限制地创建线程还可能导致OOM，所以在Java领域使用场景就受限了。

要想有效避免线程的频繁创建、销毁以及OOM问题，就不得不提今天我们要细聊的，也是Java领域使用最多的Worker Thread模式。

## Worker Thread模式及其实现

Worker Thread模式可以类比现实世界里车间的工作模式：车间里的工人，有活儿了，大家一起干，没活儿了就聊聊天等着。你可以参考下面的示意图来理解，Worker Thread模式中**Worker Thread对应到现实世界里，其实指的就是车间里的工人**。不过这里需要注意的是，车间里的工人数量往往是确定的。

![](https://static001.geekbang.org/resource/image/9d/c3/9d0082376427a97644ad7219af6922c3.png?wh=1142%2A511)

车间工作示意图

那在编程领域该如何模拟车间的这种工作模式呢？或者说如何去实现Worker Thread模式呢？通过上面的图，你很容易就能想到用阻塞队列做任务池，然后创建固定数量的线程消费阻塞队列中的任务。其实你仔细想会发现，这个方案就是Java语言提供的线程池。
<div><strong>精选留言（30）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/10/e5/42/fbe890c0.jpg" width="30px"><span>vector</span> 👍（103） 💬（1）<div>工厂里只有一个工人，他的工作就是同步的等待工厂里其他人给他提供东西，然而并没有其他人，他将等到天荒地老，海枯石烂~</div>2019-05-16</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/25/7f/473d5a77.jpg" width="30px"><span>曾轼麟</span> 👍（65） 💬（2）<div>EagerThreadPool 老师这个线程池可以避免死锁的情况，死锁的时候会自动撑大</div>2019-05-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/18/6b/55/2b0f219b.jpg" width="30px"><span>Geek_42f729</span> 👍（20） 💬（3）<div>看了一遍评论，有一部分同学回答了课后思考的结论，但是没有描述产生该结论的原因，我来描述一下吧，有不对的地方还请老师、同学们指出；

结论是：小灰写的代码会被一直阻塞；

原因是：

1. 通过Executors.newSingleThreadExecutor()创建的线程池默认是1个核心线程 + 无界工作队列；

2. 第一次submit时，会把池中唯一的一个核心线程给占用；

3. 第二次submit时，由于没有空闲的线程，并且工作队列也没满，所以线程池会把提交的任务添加到工作队列，然后等待空闲线程来执行该任务；

4. 在第二次submit时使用了.get()方法，这里会一直等到线程返回执行结果；

5. 由于两次submit是嵌套执行的，并且此时线程池中也没有空闲线程，所以第二次submit的任务永远不会被执行，.get()方法会就被永远阻塞，从而导致第一次submit的线程也被永远阻塞。</div>2022-03-18</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTKlwpFM3tkeG15YqyJTYWkfqkdmro9POq6SicYm57TaEFDOUZCXjoe0Z0Iz6UibGQqic3icJRsHdFzibtw/132" width="30px"><span>zero</span> 👍（15） 💬（1）<div>感觉这程序会调用栈内存溢出，这段代码相当于无限的递归调用啊。不知道理解的对不对，请老师指点。</div>2019-05-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/a9/36/972f7abf.jpg" width="30px"><span>木刻</span> 👍（9） 💬（1）<div>希望老师能开一栏专门讲一讲Linux下多线程并发情况下程序性能的排查和调优。谢谢老师</div>2019-05-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/fc/90/c9df0459.jpg" width="30px"><span>ack</span> 👍（6） 💬（1）<div>老师，请教个问题，线程死锁那个代码，是活锁吗，思考题我也认为是活锁</div>2019-05-16</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/61/c1/9ad88d67.jpg" width="30px"><span>Mr_杨</span> 👍（2） 💬（1）<div>老师请教个问题，如果不同业务用不同线程池，保证不了线程数量，会带来并发线程过大，如何控制频繁上下文切换的问题</div>2019-11-07</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/fe/b4/6902ac00.jpg" width="30px"><span>王成</span> 👍（1） 💬（1）<div>最近工作中遇到一个关于线程池的问题，莫名其妙的线程就不在执行
问题的原因是
每个线程都会去请求一次http，但是时间长了会出现阻塞现象（http工具类写的有点问题）
最终解决方案，除了优化工具类，还给每一个线程设置了超时时间</div>2021-07-07</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/0a/a4/828a431f.jpg" width="30px"><span>张申傲</span> 👍（1） 💬（1）<div>越来越发现，软件领域中的很多问题，都可以向现实世界寻求答案。</div>2021-03-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/16/5b/83a35681.jpg" width="30px"><span>Monday</span> 👍（0） 💬（3）<div>本篇就是一个主题，java创建线程池，并特别注意
1、生产中拒绝使用Executors提供的初始化线程池的方法（因为使用无解队列）
2、生产环境应根据业务自定义拒绝策略</div>2020-12-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/fe/58/2cddaca4.jpg" width="30px"><span>FH</span> 👍（0） 💬（1）<div>老师有个问题请教一下，线程池不应该是项目启动时加载或者懒加载模式吗，但是看示例代码都是调用业务代码时才去创建ExecutorService，这样合理吗？</div>2020-07-15</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/7b/57/a9b04544.jpg" width="30px"><span>QQ怪</span> 👍（0） 💬（1）<div>老师，有个疑问，想问下线程池该什么时候销毁?</div>2019-05-16</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/4e/3a/86196508.jpg" width="30px"><span>linqw</span> 👍（23） 💬（2）<div>newSingleThreadExecutor线程池只有单个线程，先将外部线程提交给线程池，外部线程等待内部线程执行完成，但由于线程池只有单线程，导致内部线程一直没有执行的机会，相当于内部线程需要线程池的资源，外部线程需要内部线程的结果，导致死锁。</div>2019-05-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/b5/d4/e58e39f0.jpg" width="30px"><span>Geek_0quh3e</span> 👍（6） 💬（1）<div>原始的workerThread模式包含三种角色：工人、传送带、产品，
传送带中维护一个productionsQueue以及最大的产品数量（为了防止产品无限积压）,
在传送带初始化时，创建了若干个worker（线程），worker不断从传送带取产品进行加工，
当传送带中无产品时，worker线程被挂起等待唤醒，当有新的产品加入到传送带中时，挂起的worker会被唤醒，取产品加工。
当上游线程Thread往传送带中加入产品时，如果productionsQueue到达最大产品数量时，Thread会被挂起。
当有worker线程取出产品后，会唤醒阻塞的线程Thread(当然这里也有可能唤醒worker)
线程池只是workerThread的一种实现，那么线程池中创建的Thread就是工人，线程池本身就是传送带，产品就是提交到线程池中的Runnable，
而在线程池中的阻塞队列就相当于productionsQueue，请问老师，我这样理解是否正确？

 </div>2019-05-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/6f/63/abb7bfe3.jpg" width="30px"><span>扬～</span> 👍（2） 💬（0）<div>可以出个线程池异常处理的方案吗</div>2019-05-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/62/d5/1f5c5ab6.jpg" width="30px"><span>大大大熊myeh</span> 👍（1） 💬（0）<div>首先它是一个单线程的线程池，第一次submit的任务是获取“给pool线程池设置的第二个submit任务的返回值”，然后输出。然而因为是单线程池，永远也等不到第二个线程任务返回QQ。第一个线程任务依赖于第二个任务，导致死锁。呼应本章主题：线程池分工。</div>2019-12-06</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/b5/d4/e58e39f0.jpg" width="30px"><span>Geek_0quh3e</span> 👍（1） 💬（0）<div>有问题，singlepool中只有一个线程池，future.get方法阻塞当前线程，导致打印qq的线程没有机会执行，会根据丢弃策略进行不同的操作。</div>2019-05-16</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/ff/0a/12faa44e.jpg" width="30px"><span>晓杰</span> 👍（1） 💬（0）<div>线程池里面的最大线程数只有一个，无法做到异步</div>2019-05-16</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/25/31/e9/d0e75bf4.jpg" width="30px"><span>霰雪纷飞</span> 👍（0） 💬（0）<div>这个countdown同一个线程池死锁我就遇到了！！然后分析好久才得出老师的结论。天可怜见，要是早点学这个，我就不会编写那样代码了，后面那个代码改成了单独写的forkjoin，进行join操作。但forkjoin本身不推荐支持IO密集型，需要用manager blocker。</div>2023-03-05</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/74/aa/178a6797.jpg" width="30px"><span>阿昕</span> 👍（0） 💬（0）<div>思考题：现在线程提交嵌套问题</div>2023-02-05</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1f/5e/81/82709d6e.jpg" width="30px"><span>码小呆</span> 👍（0） 💬（0）<div>这段代码,感觉是对应了书中的 : 如果提交到相同线程池的任务不是相互独立的，而是有依赖关系的，那么就有可能导致线程死锁 这一段话.</div>2022-07-03</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/4a/6f/e36b3908.jpg" width="30px"><span>xzy</span> 👍（0） 💬（0）<div>这跟上面讲的死锁例子一样呀</div>2021-04-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/aa/b6/46a5bbf3.jpg" width="30px"><span>俺能学个啥</span> 👍（0） 💬（0）<div>单线程池提交任务里面依然提交任务，这会导致里面的任务会放进阻塞队列，而只有一个线程会导致无法返回结果，外面的也会阻塞，里面的也会阻塞，就卡在那里。。</div>2021-03-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/17/e1/9d/3ec0adec.jpg" width="30px"><span>喃寻</span> 👍（0） 💬（0）<div>这里会死锁，原因是submit方法是需要等待返回值的，而这里是单线程，所以里面的submit没有可以执行的线程，导致一直等待</div>2021-01-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/a7/29/977c3280.jpg" width="30px"><span>Axe</span> 👍（0） 💬（0）<div>Executors .newSingleThreadExecutor() 创建的线程池只有一个线程，在实现上只有一个线程处理，跟异步的概念有差别，更恐怖是在线程池里有重复使用线程池执行任务，任务之间出现依赖，这样任务永远不会打印了。</div>2020-08-06</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/0f/9f/f4b06bd5.jpg" width="30px"><span>见南山</span> 👍（0） 💬（0）<div>单线程池线程池直接阻塞在get处，而再等待的任务永远在阻塞队列中放着。一个等结果，一个等线程。凉凉～</div>2020-04-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/24/5d/65e61dcb.jpg" width="30px"><span>学无涯</span> 👍（0） 💬（0）<div>老师，java的ThreadPoolExecutor里为什么把runState和WorkerCount两个字段包装到ctl一个变量里，分开两个它不香吗，还省得每次位运算才能获取到具体的runState和WorkerCount了</div>2020-04-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/b0/65/90387745.jpg" width="30px"><span>Mr.wang</span> 👍（0） 💬（0）<div>创建一个单线程线程池，再运行任务的时候，主任务先获取线程，进入到任务里面后，也使用线程中的线程，但这里是单线程线程池，子任务获取不到线程，解决方案是加大线程池的线程数量。</div>2020-03-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/75/a8/dfe4cade.jpg" width="30px"><span>电光火石</span> 👍（0） 💬（0）<div>有个问题是关于forkjoinpool的死锁问题，假设我现在创建了4个线程的forkjoinpool，当我做任务拆分的，可能需要拆分8次，我理解A拆成2个子任务的时候，A也是一直在等待的，那这样会不会造成没有线程可用而形成死锁？还是说forkjoinpool 有很好的机制，A线程等待的时候，可以把线程空出来进行调度？谢谢了！</div>2020-02-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/e8/fd/035f4c94.jpg" width="30px"><span>欢乐小熊</span> 👍（0） 💬（0）<div>这个 WorkerThread 任务分配模式与生产者消费者很像啊
</div>2019-09-30</li><br/>
</ul>