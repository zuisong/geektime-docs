今天，我会介绍一些日常开发中类似线程死锁等问题的排查经验，并选择一两个我自己修复过或者诊断过的核心类库死锁问题作为例子，希望不仅能在面试时，包括在日常工作中也能对你有所帮助。

今天我要问你的问题是，什么情况下Java程序会产生死锁？如何定位、修复？

## 典型回答

死锁是一种特定的程序状态，在实体之间，由于循环依赖导致彼此一直处于等待之中，没有任何个体可以继续前进。死锁不仅仅是在线程之间会发生，存在资源独占的进程之间同样也可能出现死锁。通常来说，我们大多是聚焦在多线程场景中的死锁，指两个或多个线程之间，由于互相持有对方需要的锁，而永久处于阻塞的状态。

你可以利用下面的示例图理解基本的死锁问题：

![](https://static001.geekbang.org/resource/image/ea/6c/ea88719ec112dead21334034c9ef8a6c.png?wh=551%2A356)

定位死锁最常见的方式就是利用jstack等工具获取线程栈，然后定位互相之间的依赖关系，进而找到死锁。如果是比较明显的死锁，往往jstack等就能直接定位，类似JConsole甚至可以在图形界面进行有限的死锁检测。

如果程序运行时发生了死锁，绝大多数情况下都是无法在线解决的，只能重启、修正程序本身问题。所以，代码开发阶段互相审查，或者利用工具进行预防性排查，往往也是很重要的。

## 考点分析

今天的问题偏向于实用场景，大部分死锁本身并不难定位，掌握基本思路和工具使用，理解线程相关的基本概念，比如各种线程状态和同步、锁、Latch等并发工具，就已经足够解决大多数问题了。
<div><strong>精选留言（30）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/11/0f/4f/c75c4889.jpg" width="30px"><span>石头狮子</span> 👍（181） 💬（1）<div>1. 死锁的另一个好朋友就是饥饿。死锁和饥饿都是线程活跃性问题。
实践中死锁可以使用 jvm 自带的工具进行排查。
2. 课后题提出的死循环死锁可以认为是自旋锁死锁的一种，其他线程因为等待不到具体的信号提示。导致线程一直饥饿。
这种情况下可以查看线程 cpu 使用情况，排查出使用 cpu 时间片最高的线程，再打出该线程的堆栈信息，排查代码。
3. 基于互斥量的锁如果发生死锁往往 cpu 使用率较低，实践中也可以从这一方面进行排查。</div>2018-06-16</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/d6/8d/7db04ad3.jpg" width="30px"><span>I am a psycho</span> 👍（66） 💬（2）<div>当是死循环引起的其他线程阻塞，会导致cpu飙升，可以先看下cpu的使用率。</div>2018-06-16</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/e9/11/e435e996.jpg" width="30px"><span>curlev3</span> 👍（56） 💬（3）<div>回答老师的问题
可以通过linux下top命令查看cpu使用率较高的java进程，进而用top -Hp ➕pid查看该java进程下cpu使用率较高的线程。再用jstack命令查看线程具体调用情况，排查问题。</div>2018-06-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/13/d3/8f880956.jpg" width="30px"><span>西鄉十六夜</span> 👍（32） 💬（1）<div>老师，面试遇到过一个很刁钻的问题。如何在jvm不重启的情况下杀死一个线程，在stop被移除后，如果线程存在死锁那是否意味着必须要修复代码再重启虚拟机呢？</div>2018-07-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/f7/e2/0c13b4fc.jpg" width="30px"><span>残阳</span> 👍（12） 💬（1）<div>以前做排查的时候看thread dump, 一般都会直接按一些关键字搜索。比如wait，lock之类，然后再找重复的内存地址。看完这遍文章之后感觉对死锁的理解更深刻。</div>2018-06-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/96/5e/8bba3a8a.jpg" width="30px"><span>陈一嘉</span> 👍（11） 💬（1）<div>任务线程规范命名，详细记录逻辑运行日志。jstack查看线程状态。</div>2018-06-16</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/fc/e5/605f423f.jpg" width="30px"><span>肖一林</span> 👍（8） 💬（1）<div>初学nio的时候确实动不动就发生死锁。现在好像也没有特别好的教程，都是一些java.io的教程。很多教程跟不上技术的迭代。也可能是因为直接io编程在项目实践中偏少。

另外，这个小程序的图片不能放大看，不知道是微信的原因还是小程序的原因。老师看到了帮忙反馈一下。</div>2018-06-16</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/d6/60/f21b2164.jpg" width="30px"><span>jacy</span> 👍（5） 💬（1）<div>尽然可以用ThreadMXBean来抓线程死锁信息，受教了。
循环死锁，会导致cpu某线程的cpu时间片占用率相当高，可以结合操作系统工具分析出线程号，然后用jstack分析线程</div>2018-06-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/fc/e5/605f423f.jpg" width="30px"><span>肖一林</span> 👍（5） 💬（1）<div>一课一练：
最典型的场景是nio的Selector类，这个类内部有三个集合，并且对这些集合做了同步。如果多个线程同时操作一个Selector，就很容易发生死锁。它的select方法会一直拿着锁，并且循环等待事件发生。如果有其他线程在修改它内部的集合数据，就死锁了。

同样用jstack可以发现问题，找出被阻塞的线程，看它等待哪个锁，再找到持有这把锁的线程，这个线程一搬处于运行状态</div>2018-06-16</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/06/9b/ade9c3bd.jpg" width="30px"><span>洗头用酱油</span> 👍（1） 💬（1）<div>杨老师，有点迷糊，所以说一个对象偏向一个线程后，这个线程就有工作了优先权吗？ 问题我记得不特殊设置的话，JVM是随机执行线程的呀？</div>2018-07-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/b5/6f/7c964414.jpg" width="30px"><span>coolboy</span> 👍（0） 💬（1）<div>杨老师，问个小白问题，java的线程状态有BLOCK、WAITING状态，使用java的内置关键字sychronized时，会出现BLOCK状态。但如果用java的reentrantLock时，也会出现BLOCK状态的吗，不应该只有WAITING状态的？</div>2018-06-25</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/fe/3c/13175251.jpg" width="30px"><span>Miaozhe</span> 👍（0） 💬（1）<div>杨老师，我Win7系统，Java 8上运行Dead Lock Simple例子，通过Jstack获取的Thread 1和Thread 2的线程状态，都是Runnable,但是Waiting on Condition[0x 000000000]。
但是，我通过Thread Group打印出来，两个线程状态都是Block。
晕乎了。。。。</div>2018-06-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/29/9e/380a01ea.jpg" width="30px"><span>tracer</span> 👍（30） 💬（0）<div>看了下jconsole检测死锁功能的源码，果然也是用ThreadMXBean获取死锁线程并分组，然后打印相关线程信息的。</div>2018-06-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/54/19/95ff4cbd.jpg" width="30px"><span>格非</span> 👍（6） 💬（0）<div>操作系统中学过进程死锁发成的四个必要条件：1、互斥条件，2、占有和等待条件，3、不可抢占条件，4、循环等待条件；破环这四个必要条件中的一个就可以避免发生死锁</div>2019-10-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/c0/6c/29be1864.jpg" width="30px"><span>随心而至</span> 👍（4） 💬（0）<div>一：死锁的主要原因：
不同线程获取锁的顺序不一致导致。
二：解决方法：
1.确保按照一定顺序获取锁，比如两个类似lockA, lockB的hash值比较，如果相等（概率很低），再添加一把另外的锁tieLock ，具体示例 参加 JCIP 10-3
2.开放调用 不要同时获取多把锁 具体示例 参见JCIP 10-6
3.使用定时的锁 ，tryLock() 或者tryLock(timeout) 

三：死锁检测：
3.1 jstack pid &gt; app.dump 然后在文件中查找线程状态（比如搜索Blocking) -&gt; 查看等待目标 -&gt; 对比 Monitor...
3.2 ThreadMXBean   



</div>2019-09-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1d/43/dc/95d4f2c5.jpg" width="30px"><span>林毅鑫</span> 👍（2） 💬（0）<div>一、死锁发生的原因
两个进场之间发生互斥，你不让我，我不让你。
二、处理死锁的方法
1、避免使用多个锁，不要赋予一段程序太多功能；
2、用图形化方式设计好锁的获取方式，参考银行家算法；
3、使用带超时（timed_wait）的方法，指定超时时间，并为无法得到锁时准备退出逻辑；
4、通过静态代码分析（如 FindBugs）去查找固定的模式，进而定位可能的死锁或者竞争情况；
三、解决办法
1、使用jps或ps命令定位死锁进程
2、开发自己的管理工具，需要用更加程序化的方式扫描服务进程、定位死锁，可以考虑使用 Java 提供的标准管理 API，ThreadMXBean，其直接就提供了 findDeadlockedThreads​() 方法用于定位。
</div>2021-03-30</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/e5/7c/2a5a418b.jpg" width="30px"><span>looper</span> 👍（2） 💬（0）<div>死锁一般的表现是CPU占用很高，内存占用不高。当检测到这种情况的时候，就需要考虑是否发生了死锁，然后找到对应的进程，使用jstack、jconsole和visualVm等工具查看栈调用栈信息，根绝业务定位问题</div>2020-07-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/e9/29/629d9bb0.jpg" width="30px"><span>天王</span> 👍（2） 💬（0）<div>18 死锁产生的原因，死锁检测工具的使用，以及在实际编码的时候如何注意 1 死锁是一种程序的状态，在实体之间由于循环依赖导致彼此都处于等待之中，没有任何个体可以继续进行，死锁存在于线程与线程之间，也存在与资源独占的进程之间，比较常见的场景是多线程并发环境中的死锁，两个或者多个线程互相持有对方需要的锁，而永久处于阻塞状态。2 检测死锁可以用jstack等工具获取线程栈，然后定位相互之间的关系，找到死锁。2.1 死锁产生的demo，定义两个对象，两个线程，线程一synchronized先锁对象a再锁对象b，线程二先锁对象b，再锁a，两个线程启动，就会产生死锁 2.2 用jstack找死锁步骤 首先确定进程ID，然后用jstack pid，可以打印出具体的死锁信息 2.3 可以用java提供的标准管理api ThreadMxBean 提供了findDeadLockedThreads方法用于定位 3 如何在预防死锁 死锁产生有几个条件 互斥条件，且互斥条件是长期持有，使用结束之前，只能自己持有，别的线程用不了，循环依赖关系，两个或者多个个体之间出现了锁的链条环，实际使用注意步骤 尽量避免使用多个锁，并且只有在需要时才持有锁，如果必须使用多个锁，设计好锁的使用顺序，再者使用带超时的方法，无法获取到锁，超时执行退出逻辑，再者，通过通过静态代码分析，去查找固定的模式，进而定位可能的死锁或者竞争情况 </div>2019-12-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/7b/57/a9b04544.jpg" width="30px"><span>QQ怪</span> 👍（2） 💬（0）<div>还有一种锁叫做活锁，可能两个线程一直在释放锁，抢占锁，互不相让，这种也是一种并发问题</div>2019-04-01</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/fe/3c/13175251.jpg" width="30px"><span>Miaozhe</span> 👍（2） 💬（0）<div>杨老师，Sorry。接着上了问题，是我的进程PID搞错了，应该用Javax，我用成eclipse的PID了。</div>2018-06-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/03/f8/f98df0a7.jpg" width="30px"><span>vaccywen</span> 👍（1） 💬（1）<div>多执行几次jstack，如果同一个线程id多次结果都是running，而其他线程一直都是BLOCKED状态，是不是就可以判断某个持锁线程进入死循环？</div>2019-11-04</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/0b/2d/4a6d7d41.jpg" width="30px"><span>道法自然</span> 👍（1） 💬（0）<div>请教老师，线程饥饿的情况，有没有什么好的诊断办法？</div>2019-08-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/38/85/105667e6.jpg" width="30px"><span>JSON</span> 👍（1） 💬（0）<div>如果是生产环境出现了死锁状态，该怎么排查问题</div>2019-07-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/1a/66/2d9db9ed.jpg" width="30px"><span>苦行僧</span> 👍（1） 💬（0）<div>平常工作发生的死锁都发生在数据库层面，多线程并发修改同一条记录</div>2019-02-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1c/bd/7a/37df606b.jpg" width="30px"><span>乔帆 Kayla</span> 👍（0） 💬（0）<div>对比 Monitor 等持有状态？什么是有状态？</div>2023-06-06</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/0c/76/0c07376d.jpg" width="30px"><span>蒙奇君杰</span> 👍（0） 💬（0）<div>循环死锁，会导致cpu某线程的cpu时间片占用率相当高，可以结合操作系统工具分析出线程号，然后用jstack分析线程。
from jacy
</div>2020-09-16</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1b/36/47/8e80082c.jpg" width="30px"><span>大成尊者</span> 👍（0） 💬（0）<div>有时候并不是阻塞导致的死锁，只是某个线程进入了死循环，导致其他线程一直等待，这种问题如何诊断呢？
答：这种依然可以通过jstack来看线程的状态，如果是阻塞，那么可以去看这个线程的实现，如果是死循环，那么很容易debug出来</div>2020-06-24</li><br/><li><img src="" width="30px"><span>Paul Shan</span> 👍（0） 💬（0）<div>死锁是两个线程相互试图获取对方独占的资源的情况。如果随机使用锁，这种情况不可避免。</div>2019-11-12</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/gCN0rqmg3cDYQYfddTuWCXMIaPfbeR3kDVdCtzlmvp3r4l132Hju86TzRn3382ic52icylZuryUgGvA8fib1icIib7A/132" width="30px"><span>Geek_7eb30c</span> 👍（0） 💬（0）<div>老师有个问题咨询下，我在跑一个大批量数据导入数据库的程序，用线程池一批1000导入数据库，头尾用了分布式redis锁防止并发，但在倒入中还是出现锁表的情况，不知道是不是我的分布式锁放错位置，是否应该放在异步线程开启前加锁</div>2019-06-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/db/26/3c8d68fb.jpg" width="30px"><span>天使梦泪</span> 👍（0） 💬（0）<div>java8环境，连着多运行几次那个死锁实例代码才会出现blocked状态，前几次都是RUNNABLE状态，而且用线程组打印的才是blocked，直接用线程的getState方法打印的都是RUNNABLE。</div>2019-02-28</li><br/>
</ul>