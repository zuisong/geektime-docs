今天我们来深入聊聊线程，相信大家对于线程这个概念都不陌生，它是Java并发的基础元素，理解、操纵、诊断线程是Java工程师的必修课，但是你真的掌握线程了吗？

今天我要问你的问题是，一个线程两次调用start()方法会出现什么情况？谈谈线程的生命周期和状态转移。

## 典型回答

Java的线程是不允许启动两次的，第二次调用必然会抛出IllegalThreadStateException，这是一种运行时异常，多次调用start被认为是编程错误。

关于线程生命周期的不同状态，在Java 5以后，线程状态被明确定义在其公共内部枚举类型java.lang.Thread.State中，分别是：

- 新建（NEW），表示线程被创建出来还没真正启动的状态，可以认为它是个Java内部状态。
- 就绪（RUNNABLE），表示该线程已经在JVM中执行，当然由于执行需要计算资源，它可...
<div><strong>精选留言（30）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/10/fc/66/d7f7ad77.jpg" width="30px"><span>风动静泉</span> 👍（120） 💬（6）<div>一课一练:
使用了两种方式获取当前程序的线程数。
1、使用线程管理器MXBean
2、直接通过线程组的activeCount
第二种需要注意不断向上找父线程组，否则只能获取当前线程组，结果是1

结论:
使用以上两种方式获取的线程总数都是5个。
main
Attach Listener
Signal Dispatcher
Finalizer
Reference Handler

此外，如果使用的IDE是IDEA 直接运行会多一个Monitor Ctrl-break线程，这个是IDE的原因。debug模式下不会有这个线程。</div>2018-06-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/49/a5/e4c1c2d4.jpg" width="30px"><span>小文同学</span> 👍（86） 💬（5）<div>做了一个test分析老师的问题，观察到的情况如下：
JVM 启动 Hello World的线程分析
环境：
macOS + jdk8
检测获得
Thread[Reference Handler,10,system]
Thread[Finalizer,8,system]
Thread[main,5,main]
Thread[Signal Dispatcher,9,system]
Hello World!
其中：
Reference Handler：处理引用对象本身的垃圾回收
Finalizer：处理用户的Finalizer方法
Signal Dispatcher：外部jvm命令的转发器

在jdk6环境中
还有一个Attach Listener的线程
是负责接收外部命令的，如jmap、jstack

</div>2018-06-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/1c/80/2bc29ca9.jpg" width="30px"><span>爱折腾的老斑鸠</span> 👍（24） 💬（2）<div>theadlocal里面的值如果是线程池的线程里面设置的，当任务完成，线程归还线程池时，这个threadlocal里面的值是不是不会被回收？</div>2018-06-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/3b/36/2d61e080.jpg" width="30px"><span>行者</span> 👍（22） 💬（2）<div>“我们会发现一个特别的地方，通常幻象引用都会和引用队列配合清理机制使用，但是 ThreadLocal 是个例外，它并没有这么做。”
 老师，Entry继承的是WeakReference，这个是弱引用吧。
 main:
        System.out.println(&quot;hello world&quot;);
        ThreadGroup group = Thread.currentThread().getThreadGroup();
        ThreadGroup topGroup = group;
        while (group != null) {
            topGroup = group;
            group = group.getParent();
        }
        int nowThreads = topGroup.activeCount();
        Thread[] lstThreads = new Thread[nowThreads];
        topGroup.enumerate(lstThreads);
        for (int i = 0; i &lt; nowThreads; i++) {
            System.out.println(&quot;线程number：&quot; + i + &quot; = &quot; + lstThreads[i].getName());
        }
out:
线程number：0 = Reference Handler &#47;&#47; 计算对象是否可达？
线程number：1 = Finalizer &#47;&#47; 回收对象时触发的finalize方法？
线程number：2 = Signal Dispatcher &#47;&#47; 线程调度员
线程number：3 = main
线程number：4 = Monitor Ctrl-Break &#47;&#47; 监控器，锁相关</div>2018-06-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/f3/9f/3e4e8d46.jpg" width="30px"><span>tyson</span> 👍（12） 💬（1）<div>1、站在应用程序方面，只创建了一个线程。
2、站在jvm方面，肯定还有gc等其余线程。

总结：
1、线程是系统调度的最小单元，应该是进程吧。线程是操作系统的资源，在运行的时候会打开文件描述符等。
2、 resume、stop、suspend等已经被废弃了
3、线程的等待和唤醒，建议使用reentrantlock的condition wait&#47;notify方法
4、可以使用线程的join方法、countdownlatch、cyclicbarrier、future等进行线程的等待</div>2018-06-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/d4/f3/129d6dfe.jpg" width="30px"><span>李二木</span> 👍（9） 💬（1）<div>现在觉得踩坑是一种很好学习方法</div>2018-06-15</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/6f/63/abb7bfe3.jpg" width="30px"><span>扬～</span> 👍（6） 💬（3）<div>等待与阻塞有什么区别呢</div>2018-11-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/05/f3/4dd9e515.jpg" width="30px"><span>TonyEasy</span> 👍（6） 💬（1）<div>老师，我有一点疑问，在线程池里复用线程时是不是对同一个线程调用了多次.start()方法呢？</div>2018-06-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/fc/24/7d43d807.jpg" width="30px"><span>mongo</span> 👍（5） 💬（1）<div>杨老师请教你，关于高并发和线程池，我刚刚入门，工作中没有涉及过这一块。我阅读了oracle java tutorial high level concurrency 章节，阅读并粗略理解了《并发编程实践》这本书，想进一步清晰我的理解，我现在苦于在实践练习方面不知道怎么进行。老师有什么具体可行的思路指点一下吗？留言圈里有好多大神，在这里同时也请教其他的朋友。谢谢老师，谢谢大家。</div>2018-06-15</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/f3/83/e2612d81.jpg" width="30px"><span>锐</span> 👍（5） 💬（1）<div>通常弱引用都会和引用队列配合清理机制使用，但是 ThreadLocal 是个例外，它并没有这么做。

这意味着，废弃项目的回收依赖于显式地触发，否则就要等待线程结束，进而回收相应 ThreadLocalMap！这就是很多 OOM 的来源

这个平时还真没注意</div>2018-06-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/f4/d9/e572ae4d.jpg" width="30px"><span>食指可爱多</span> 👍（4） 💬（1）<div>我了解确定线程有:任务线程，Main线程，垃圾回收线程，还有些线程没细心关注名字和用途，惭愧了。可以在业务线程中等待，然后在命令行用jstack看看当前jvm的线程堆栈。</div>2018-06-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/25/c3/6569bd7d.jpg" width="30px"><span>高杰</span> 👍（2） 💬（1）<div>有几个弱引用，虚引用的地方，音频和文字对不上。把我搞晕了。
应该有2个线程，还有jvm的gc线程？还有第三个线程吗？</div>2018-06-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/32/3f/fa4ac035.jpg" width="30px"><span>sunlight001</span> 👍（2） 💬（1）<div>threadlocal在放入值之后，在get出来之后，需要做remove操作，我这么理解对么？以前写的程序都没remove😄</div>2018-06-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/8a/97/6c1e90f1.jpg" width="30px"><span>Eason</span> 👍（2） 💬（1）<div>“比如，线程试图通过 synchronized 去获取某个锁，但是其他线程已经独占了，那么当前线程就会处于阻塞状态”这个例子换一个理解，感觉也是在等待其他线程做某些操作。在“阻塞”中也是在“等待”中？？</div>2018-06-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/57/38/ba6a106f.jpg" width="30px"><span>Phoenix</span> 👍（0） 💬（1）<div>想要请教老师，对于tomcat服务器为每个用户请求新建一条线程，那么该线程的threadlocal也会随着请求结束，线程被回收，threadlocal也会相应的被回收，那么我理解的是，类似tomcat请求这种线程模型，threadlocal即使不调用remove，也不会出现OOM，这样理解对吗？</div>2018-11-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/29/9e/380a01ea.jpg" width="30px"><span>tracer</span> 👍（0） 💬（1）<div>有讲解那五个线程的资料吗？</div>2018-06-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/05/f3/4dd9e515.jpg" width="30px"><span>TonyEasy</span> 👍（0） 💬（1）<div>老师，我有一点疑问，在线程池复用线程时，对同一线程调用多次.start()方法，为何不报错呢？</div>2018-06-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/7e/dd/e4e6718a.jpg" width="30px"><span>扫地僧的功夫梦</span> 👍（0） 💬（1）<div>调用notify()&#47;notifyAll()方法线程是变为阻塞状态吧，因为线程还没获取到锁。</div>2018-06-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/fc/e5/605f423f.jpg" width="30px"><span>肖一林</span> 👍（0） 💬（1）<div>threadlocal和线程池结合的问题真的没考虑过</div>2018-06-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/fe/3c/13175251.jpg" width="30px"><span>Miaozhe</span> 👍（0） 💬（1）<div>问个问题，NIO 2的异步是不是利用协程的原理设计的？它实际运行的是多线程吗？</div>2018-06-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/f3/9f/3e4e8d46.jpg" width="30px"><span>tyson</span> 👍（0） 💬（1）<div>1、站在应用程序方面，只创建了一个线程。
2、站在jvm方面，肯定还有gc等其余线程。

总结：
1、线程是系统调度的最小单元，应该是进程吧。线程是操作系统的资源，在运行的时候会打开文件描述符等。
2、 resume、stop、suspend等已经被废弃了
3、线程的等待和唤醒，建议使用reentrantlock的condition wait&#47;notify方法
4、可以使用线程的join方法、countdownlatch、cyclicbarrier、future等进行线程的等待</div>2018-06-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/15/02/66f65388.jpg" width="30px"><span>雷霹雳的爸爸</span> 👍（0） 💬（1）<div>老师今天这课后题，又打脸了平时工作不仔细的地方，我首先想到的是好歹得sleep一下或打个断点用类似visualvm的工具看下，或者top之类数一下，赶着出门，回来试下</div>2018-06-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/1e/e5/bee05364.jpg" width="30px"><span>阿甘</span> 👍（0） 💬（1）<div>线程得内存分配是怎么样的呢？</div>2018-06-14</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/B5KGe7PEWv1m0ZdUSRBLaX65brD5Iice8ze7xpFDJIzOTQSN2JqCkCYwOnTMW5ApNCyicCAs8t48DUuX5t66VHBQ/132" width="30px"><span>hanmshashou</span> 👍（0） 💬（1）<div>weak 应该不是幻象引用吧</div>2018-06-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/33/92/99530cee.jpg" width="30px"><span>灰飞灰猪不会灰飞.烟灭</span> 👍（0） 💬（1）<div>老师 future模式是怎么异步返回结果的呢？是不是把每个线程的运行结果放到queue中，然后轮询queue返回结果？</div>2018-06-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/b9/45/c3d6fd51.jpg" width="30px"><span>黄启航</span> 👍（17） 💬（2）<div>杨老师您好，我有个疑问:

文章最后说&quot;弱引用都会和引用队列配合清理工作，但是Threadlocal是个例外，它并没有这么做。这意味着，废弃项目的回收依赖显示地触发，否则就要等待线程的结束&quot;  。

我的疑问：既然没有利用引用队列来实现自动清除，那TheadLocalMap内部的Entry继承WeakReference有何用意？能起到什么作用？
</div>2018-07-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/17/ba/ec/2b1c6afc.jpg" width="30px"><span>李飞</span> 👍（8） 💬（0）<div>&#47;&#47;线程数验证
        System.out.println(&quot;hello world&quot;);
        int activeCount = Thread.activeCount();
        System.out.println(&quot;线程活跃数：&quot; + activeCount);
        Set&lt;Thread&gt; threadSet = Thread.getAllStackTraces().keySet();
        for (Thread thread : threadSet) {
            System.out.println(&quot;线程&quot; + thread.getId() + &quot;:&quot; + thread.getName());
        }

输出结果：
hello world
线程活跃数：1
线程3:Finalizer
线程4:Signal Dispatcher
线程2:Reference Handler
线程5:Attach Listener
线程1:main</div>2020-05-01</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/1a/66/2d9db9ed.jpg" width="30px"><span>苦行僧</span> 👍（8） 💬（0）<div>边看老师的讲课 边反思工程代码 </div>2018-12-30</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/9f/06/287d77dd.jpg" width="30px"><span>承香墨影</span> 👍（2） 💬（0）<div>Java 线程状态切换的图有问题，Runnable 到 Blocked 不包括阻塞 IO，在 Java 层面是不关心是否调用了 阻塞API 的，此时不会切换线程状态，依然保持在 RUNNABLE 中。</div>2020-04-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/e9/29/629d9bb0.jpg" width="30px"><span>天王</span> 👍（2） 💬（0）<div>17 一次线程多次调用start方法会提示IllegnalThreadStateException，1 线程生命周期的几个状态，在Java.lang.thread.state中，new线程刚创建还没真正启动的状态，runnable 就绪 表示该线程已经在jvm中执行，执行需要计算资源，可能正在运行，也可能正在等待cpu分配cpu片段，在就绪队列排队，blocked，阻塞 表示当前线程处于Monitor lock，比如线程试图获取某个锁，发现被其他线程占了，就会处于阻塞状态，等待waiting，比如生产者消费者模式，消费者条件未满足，让当前消费者等待，生产者去准备数据，通过notify等动作，通知消费者线程可以继续工作，计时等待，和进入等待的条件一样，调用方法是等待超时的方法，终止 terminated 不管意外退出还是自动终止，线程终止运行，也叫死亡，第二次调用start的时候，线程已经死亡或者处于非new的状态，所以会抛出异常 2 线程是什么 线程是线程调度的基本单元，一个进城包含多个线程，作为任务真正的执行者，有自己的栈，寄存器和本地存储等，但是会和进城中其他线程共享文件描述符和虚拟地址空间，线程分为内核线程和用户线程，看Thread的源码，以JNI形式调用的本地代码，3 创建线程 new Thread().start() thread.join()，线程的方法，有start，join等待线程结束，yield告诉调度室，主动让出CPU，基类Object提供了一些基础方法，wait，notify，notifyAll等方法，如果一个线程持有Minitor锁，会让其他线程处于wait状态，直到其他线程notify或者notifyall，Daemon Thread 守护线程，长期存在的服务线程</div>2019-12-18</li><br/>
</ul>