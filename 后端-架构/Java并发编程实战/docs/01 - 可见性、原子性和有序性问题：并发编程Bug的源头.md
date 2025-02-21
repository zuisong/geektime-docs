如果你细心观察的话，你会发现，不管是哪一门编程语言，并发类的知识都是在高级篇里。换句话说，这块知识点其实对于程序员来说，是比较进阶的知识。我自己这么多年学习过来，也确实觉得并发是比较难的，因为它会涉及到很多的底层知识，比如若你对操作系统相关的知识一无所知的话，那去理解一些原理就会费些力气。这是我们整个专栏的第一篇文章，我说这些话的意思是如果你在中间遇到自己没想通的问题，可以去查阅资料，也可以在评论区找我，以保证你能够跟上学习进度。

你我都知道，编写正确的并发程序是一件极困难的事情，并发程序的Bug往往会诡异地出现，然后又诡异地消失，很难重现，也很难追踪，很多时候都让人很抓狂。但要快速而又精准地解决“并发”类的疑难杂症，你就要理解这件事情的本质，追本溯源，深入分析这些Bug的源头在哪里。

那为什么并发编程容易出问题呢？它是怎么出问题的？今天我们就重点聊聊这些Bug的源头。

## 并发程序幕后的故事

这些年，我们的CPU、内存、I/O设备都在不断迭代，不断朝着更快的方向努力。但是，在这个快速发展的过程中，有一个**核心矛盾一直存在，就是这三者的速度差异**。CPU和内存的速度差异可以形象地描述为：CPU是天上一天，内存是地上一年（假设CPU执行一条普通指令需要一天，那么CPU读写内存得等待一年的时间）。内存和I/O设备的速度差异就更大了，内存是天上一天，I/O设备是地上十年。
<div><strong>精选留言（30）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/10/fb/7b/2d4b38fb.jpg" width="30px"><span>Jialin</span> 👍（624） 💬（33）<div>对于双重锁的问题，我觉得任大鹏分析的蛮有道理，线程A进入第二个判空条件，进行初始化时，发生了时间片切换，即使没有释放锁，线程B刚要进入第一个判空条件时，发现条件不成立，直接返回instance引用，不用去获取锁。如果对instance进行volatile语义声明，就可以禁止指令重排序，避免该情况发生。
对于有些同学对CPU缓存和内存的疑问，CPU缓存不存在于内存中的，它是一块比内存更小、读写速度更快的芯片，至于什么时候把数据从缓存写到内存，没有固定的时间，同样地，对于有volatile语义声明的变量，线程A执行完后会强制将值刷新到内存中，线程B进行相关操作时会强制重新把内存中的内容写入到自己的缓存，这就涉及到了volatile的写入屏障问题，当然也就是所谓happen-before问题。</div>2019-02-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/5b/79/d55044ac.jpg" width="30px"><span>coder</span> 👍（378） 💬（10）<div>long类型64位，所以在32位的机器上，对long类型的数据操作通常需要多条指令组合出来，无法保证原子性，所以并发的时候会出问题🌝🌝🌝</div>2019-02-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/f7/0a/067537fc.jpg" width="30px"><span>别皱眉</span> 👍（182） 💬（18）<div>周末了
对留言问题总结一下
 
------可见性问题------
对于可见性那个例子我们先看下定义:
可见性:一个线程对共享变量的修改，另外一个线程能够立刻看到
 
并发问题往往都是综合证，这里即使是单核CPU，只要出现线程切换就会有原子性问题。但老师的目的是为了让大家明白什么是可见性
或许我们可以把线程对变量的读可写都看作时原子操作，也就是cpu对变量的操作中间状态不可见，这样就能更加理解什么是可见性了。
 
------CPU缓存刷新到内存的时机------
cpu将缓存写入内存的时机是不确定的。除非你调用cpu相关指令强刷
 
------双重锁问题------
如果A线程与B线程如果同时进入第一个分支，那么这个程序就没有问题
 
如果A线程先获取锁并出现指令重排序时，B线程未进入第一个分支，那么就可能出现空指针问题，这里说可能出现问题是因为当把内存地址赋值给共享变量后，CPU将数据写回缓存的时机是随机的
 
------ synchronized------
线程在synchronized块中，发生线程切换，锁是不会释放的
 
------指令优化------
除了编译优化,有一部分可以通过看汇编代码来看，但是CPU和解释器在运行期也会做一部分优化，所以很多时候都是看不到的，也很难重现。
 
------JMM模型和物理内存、缓存等关系------
内存、cpu缓存是物理存在，jvm内存是软件存在的。
关于线程的工作内存和寄存器、cpu缓存的关系 大家可以参考这篇文章
https:&#47;&#47;blog.csdn.net&#47;u013851082&#47;article&#47;details&#47;70314778&#47;
 
------IO操作------
io操作不占用cpu，读文件，是设备驱动干的事，cpu只管发命令。发完命令，就可以干别的事情了。
 
 
------寄存器切换------ 
寄存器是共用的，A线程切换到B线程的时候，寄存器会把操作A的相关内容会保存到内存里，切换回来的时候，会从内存把内容加载到寄存器。可以理解为每个线程有自己的寄存器
 
请老师帮忙看看，有没问题。希望我的总结能帮到更多人😄😄</div>2019-03-16</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/4f/f9/1f0a9665.jpg" width="30px"><span>任大鹏</span> 👍（163） 💬（7）<div>对于阿根一世同学的那个疑问，我个人认为CPU时间片切换后，线程B刚好执行到第一次判断instance==null，此时不为空，不用进入synchronized里，就将还未初始化的instance返回了</div>2019-02-28</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTJGuKuqRI35yaUbfl0emNshRnHlIzMmspVI8WBv6mqZWRtianpncBBZJy6DFibQWfFfyKAmrwInm8hA/132" width="30px"><span>Geek_dcwrgy</span> 👍（111） 💬（50）<div>针对阿根一世的问题，问题其实出现在new Singleton()这里。
这一行分对于CPU来讲，有3个指令：
1.分配内存空间
2.初始化对象
3.instance引用指向内存空间
正常执行顺序1-2-3
但是CPU重排序后执行顺序可能为1-3-2，那么问题就来了
步骤如下：
1.A、B线程同时进入了第一个if判断
2.A首先进入synchronized块，由于instance为null，所以它执行instance = new Singleton();
3.然后线程A执行1-&gt; JVM先画出了一些分配给Singleton实例的空白内存，并赋值给instance
4.在还没有进行第三步（将instance引用指向内存空间）的时候，线程A离开了synchronized块
5.线程B进入synchronized块，读取到了A线程返回的instance，此时这个instance并未进行物理地址指向，是一个空对象。
有人说将对象设置成volatile，其实也不能完全解决问题。volatile只是保证可见性，并不保证原子性。

现行的比较通用的做法就是采用静态内部类的方式来实现。
public class MySingleton {
	
	&#47;&#47;内部类
	private static class MySingletonHandler{
		private static MySingleton instance = new MySingleton();
	} 
	
	private MySingleton(){}
	 
	public static MySingleton getInstance() { 
		return MySingletonHandler.instance;
	}
}</div>2019-02-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/03/10/15f82d62.jpg" width="30px"><span>阿根一世</span> 👍（108） 💬（10）<div>对于双重锁检查那个例子，我有一个疑问，A如果没有完成实例的初始化，锁应该不会释放的，B是拿不到锁的，怎么还会出问题呢？</div>2019-02-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/31/f4/467cf5d7.jpg" width="30px"><span>MARK</span> 👍（85） 💬（5）<div>刚看过《java并发实战》，又是看了个开始就看不下去了😂😂，希望订阅专栏可以跟老师和其他童鞋一起坚持学习并发编程😄😄

思考题：在32位的机器上对long型变量进行加减操作存在并发隐患的说法是正确的。
原因就是文章里的bug源头之二：线程切换带来的原子性问题。
非volatile类型的long和double型变量是8字节64位的，32位机器读或写这个变量时得把人家咔嚓分成两个32位操作，可能一个线程读了某个值的高32位，低32位已经被另一个线程改了。所以官方推荐最好把long\double 变量声明为volatile或是同步加锁synchronize以避免并发问题。

贴一段java文档的说明
https:&#47;&#47;docs.oracle.com&#47;javase&#47;specs&#47;jls&#47;se8&#47;html&#47;jls-17.html#jls-17.7

17.7. Non-Atomic Treatment of double and long

For the purposes of the Java programming language memory model, a single write to a non-volatile long or double value is treated as two separate writes: one to each 32-bit half. This can result in a situation where a thread sees the first 32 bits of a 64-bit value from one write, and the second 32 bits from another write.

Writes and reads of volatile long and double values are always atomic.

Writes to and reads of references are always atomic, regardless of whether they are implemented as 32-bit or 64-bit values.

Some implementations may find it convenient to divide a single write action on a 64-bit long or double value into two write actions on adjacent 32-bit values. For efficiency&#39;s sake, this behavior is implementation-specific; an implementation of the Java Virtual Machine is free to perform writes to long and double values atomically or in two parts.

Implementations of the Java Virtual Machine are encouraged to avoid splitting 64-bit values where possible. Programmers are encouraged to declare shared 64-bit values as volatile or synchronize their programs correctly to avoid possible complications.</div>2019-02-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/52/97/8f960ce9.jpg" width="30px"><span>xx鼠</span> 👍（47） 💬（6）<div>Singleton instance改为volatile或者final就完美了，这里面其实涉及Java的happen-before原则。</div>2019-02-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/0e/e8/5d2c3e08.jpg" width="30px"><span>何方妖孽</span> 👍（33） 💬（9）<div>synchronized修饰的代码块里，会出现线程切换么？我理解的synchronized作用就是同步执行，不会线程切换，请作者给我解答下。</div>2019-03-01</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/48/1b/7de6e72e.jpg" width="30px"><span>牧童纪年</span> 👍（33） 💬（7）<div>王老师，你文章中讲的 优化指令的执行次序 使得缓存能够更加合理的利用是什么意思？</div>2019-02-28</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/DYAIOgq83eo7ticAviaxUk04QAiadIo1O5G7ib03V0AEibWdVW6Zxwzy7xMaVgKjAVE4NXZuLqsbY8CFNiaoFwyRx3Aw/132" width="30px"><span>Geek_1dn4jq</span> 👍（25） 💬（7）<div>老师,运行文中的测试代码,有时会出现9000多的结果,不知道是什么原因?</div>2019-02-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/e2/f8/6e5da436.jpg" width="30px"><span>Gavin</span> 👍（24） 💬（3）<div>NIO和并发有什么关系呢？</div>2019-02-28</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/PiajxSqBRaELZPnUAiajaR5C25EDLWeJURggyiaOP5GGPe2qlwpQcm5e3ybib8OsP4tvddFDLVRSNNGL5I3SFPJHsA/132" width="30px"><span>null</span> 👍（19） 💬（4）<div>看完文章来刷评论，看到阿根一世的童鞋问题，确实是这样，锁🔒都还没有释放，线程B根本获取不到对象，所以线程A创建的对象是完整的，线程B后续获取的对象也是初始化完成的对象。
然后回去再看了一遍那一小段，当我看到线程B竞争锁资源失败后被阻塞，我就更肯定，应该是文章描述有误。
当再往下看文章，发现后面有说：“一切都很完美，无懈可击”。soga，这是描述我们自己觉得正常的场景。
接着文章下面分析异常的原因，但是没提到线程B在哪停下来，因此我们的思维还是停留在前面那一段，线程A和线程B都过了第一个判空语句，来了竞争锁 syncronized 这，所以有阿根一世同样的疑问。建议老师调整一下，在分析异常原因时，说明一下在哪个语句时发生了线程切换，这样童鞋们也更好理解。

😂这理解有偏差，属于可见性问题，是我们大脑缓存了之前的描述，导致了异常的理解😂</div>2019-03-31</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/36/d2/c7357723.jpg" width="30px"><span>发条橙子 。</span> 👍（18） 💬（2）<div>老师 ，我有几个问题希望老师指点 ，也是涉及到操作系统的：

1.  操作系统是以进程为单位共享资源 ，以线程单位进行调用 。 多个线程共享一个进程的资源 。 一个java应用占一个进程（jvm的内存模型的资源也在这个进程中） ，一个进程占一个cpu ， 所以老师所说的多核cpu缓存，每个cpu有自己的缓存 ，AB两个线程在不同的cpu上操作不太理解 ， 一个应用的AB两个线程是不是应该处在同个cpu上面 ？？？

2. 如果按照老师所说不同线程在不同cpu上运行 ， 是不是有个叫并行和并发的概念 。 单个cpu的时候多线程实际上是模拟并发的并行，实际上cpu只能一次执行一个线程，两个线程交替执行。 而到了多核中，可以真正的将两个线程AB同时分给cpu1 .cpu2同时执行，称之为并发？？

3. 我感觉老师第二点原子性中也有包含可见性问题，由于时间片到了， 当把资源读到自己的工作线程中时，由于不可见性，以为自己是最新的导致值不准确，这个也对应了第一个问题 ， 两个线程是否在同个进程内共享资源

问题有点多 ， 可能自己的理解有偏差 ，希望老师指正
</div>2019-02-28</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/DYAIOgq83eqHMAwG4atmGJ6H1cs1o3yUE2UhEian6cmbp9BWC1V2S7zAQdQHWYtaZbjahKHsMSkje5GrGjo9Iug/132" width="30px"><span>我会得到</span> 👍（17） 💬（1）<div>零点一过刚好看到更新，果断一口气读完，带劲！可见性，原子性，有序性，操作系统作为基础，内存模型，机器指令，编译原理，一个都不能少，开始有点意思了👍</div>2019-02-28</li><br/><li><img src="" width="30px"><span>suynan</span> 👍（14） 💬（5）<div>
并发编程的场景中的三个bug源头：可见性、原子性、有序性
1.可见性：多核系统每个cpu自带高速缓存，彼此间不交换信息（列子：两个线程对同一份实列变量count累加，结果可能不等于累加之和，因为线程将内存值载入各自的缓存中，之后的累加操作基于缓存值进行，并不是累加一次往内存回写一次）
2.原子性：cpu分时操作导致线程的切换，（列子：AB两个线程同时进行count+=1，由于+=操作是3步指令①从内存加载②+1操作③回写到主内，线程A对其进行了①②操作后，切换到B线程，B线程进行了①②③，这时内存值是1，然后再切到A执行③操作，这时的值也还是1，PS:这貌似也存在可见性的问题）
 3.有序性：指令的重排序（列子：单列模式的双重检测，new指令也是3步操作，①分内存②初始化③赋值给引用变量，可能会发生①③②的重排序，这时候如果又有操作系统的分时操作的加持，导致A操作①③后挂起，时间片被分配给了B线程，而B线程甚至都不需要进行锁的获取，因为此时instance已经不等于null了，但是此时的instance可能未初始化）</div>2019-03-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/e4/76/a97242c0.jpg" width="30px"><span>黄朋飞</span> 👍（11） 💬（1）<div>老师你好，请问文章中的缓存和内存什么区别，缓存不是在内存中存放着吗？</div>2019-02-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/a2/f3/aa504fa6.jpg" width="30px"><span>波波</span> 👍（10） 💬（1）<div>为老师点赞，讲了并发产生的前世今生，通俗易懂又不失深度。</div>2019-03-01</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/f2/86/d689f77e.jpg" width="30px"><span>Hank_Yan</span> 👍（9） 💬（2）<div>〔如果此时线程 B 也执行 getInstance() 方法，那么线程 B 会发现instance != null，所以直接返回 instance〕

这里加一句，线程B刚好执行到“第一个判断”，会发现  instance!=null ， 这样比较好，不然还是会有很多人误解是在执行第二个判断，然后问为什么锁没有释放，也能进行第二个判断。</div>2019-03-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/4c/12/f0c145d4.jpg" width="30px"><span>Rayjun</span> 👍（9） 💬（4）<div>第一个测试代码是不是有点问题，在静态方法中怎么能访问非静态变量呢？</div>2019-03-03</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/DYAIOgq83eo19qicyia7fD28fhVXB2dH2icFxIialY8ibmU30HicUJrLr8rOedVewgx1uhMKj0Gwl7FK44UKMNZOOicQQ/132" width="30px"><span>diexue798</span> 👍（9） 💬（3）<div>好好学习，不是很了解spring线程安全，springmvc线程安全这里,如果有成员变量，就算是数据共享了，就不安全了么，那么注入的servie怎么又是安全的，还有加不加锁的集合如果是局部变量是不是也都安全，那什么时候用线程安全的加了锁的集合呢？</div>2019-02-28</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTJZhuQk0ibMqdsASdJib2aUKNjTiaVm1ib3EfjyyiaKBJAyzYFls9KTEQ3w60cpy5CPLRNHsX8uooDoB8g/132" width="30px"><span>rock</span> 👍（6） 💬（1）<div>对于文中提到的双重检查的问题.我理解这本质上是指令重排序引起的“安全构造问题”。（参见java并发编程实战3.5 安全发布一章）。
如宝令老师文中所讲，一个new操作，实际上是多个CPU指令，不是原子操作而是复合操作。
这个复合操作会被线程切换中断，导致此构造状态处于“未完成”状态。
中断此刻，获得CPU执行权的其他线程会通过第一个判空条件，通过读取instance内存地址获取到此处于“未完成”状态的实例。

指令重排序在这里起到了关键的“作恶”。即如老师文中所讲，把‘将新开辟的内存地址赋值于instance’指令排序到了‘实例化新开辟内存的各个域’指令前面。这就导致了不正确构造状态的产生。

针对上述2点，1.构造过程中的，对构造对象的并发访问；2.不正确构造状态的产生；
解决方法，杜绝其中任意一个即可。

杜绝第1点，加锁在整个构造过程，即提高了加锁的范围，这会比文中的实现牺牲并发度，降低性能。
杜绝第2点，使用volatile变量禁用指令重拍序。有效且不像第1种方法那样牺牲并发度。</div>2019-05-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/54/9a/76c0af70.jpg" width="30px"><span>每天晒白牙</span> 👍（6） 💬（1）<div>老师，您的第一个例子，说单核cpu不会有线程安全问题。这个不对吧，多线程安全问题，与单核或多核没啥关系吧，希望老师能回复这个留言，谢谢老师</div>2019-05-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/06/62/898449d3.jpg" width="30px"><span>... ...</span> 👍（6） 💬（3）<div>老师，上面的两个线程的例子应该不是可见性导致而是原子性导致的吧！如果是可见性导致的话，我在变量count上加个volatile应该可以解决问题啊！还发现个小问题，非静态变量应该不能直接用于静态方法中吧！</div>2019-02-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/47/36/cb57ac83.jpg" width="30px"><span>magicHu</span> 👍（5） 💬（4）<div>老师，缓存导致的可见性问题不是因为多核的原因吧，单核上也会有缓存导致可见性问题，求老师翻牌</div>2019-05-27</li><br/><li><img src="" width="30px"><span>linus</span> 👍（5） 💬（5）<div>关于文章开始说的单cpu的情况，如果也是非原子行操作，也会出现并发问题？
</div>2019-03-06</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/46/c0/106d98e7.jpg" width="30px"><span>Sam_Deep_Thinking</span> 👍（5） 💬（1）<div>良心专栏呀。目前正准备组织小组成员学习该专栏，概念和背景都讲的非常清楚。老板让俺给一个技术规划，我列的其中一个，便是全组人员学习该专栏，并以小组分享的方式讲出来。</div>2019-03-03</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/dc/90/330d5620.jpg" width="30px"><span>pdai</span> 👍（5） 💬（2）<div>Count那个应该是1到20000之间吧，而不是10000到20000之间吧？</div>2019-02-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/ff/8d/8601f035.jpg" width="30px"><span>淞淞同学</span> 👍（4） 💬（3）<div>循环 10000 次 count+=1 操作如果改为循环 1 亿次，你会发现效果更明显，最终 count 的值接近 1 亿，而不是 2 亿。如果循环 10000 次，count 的值接近 20000，原因是两个线程不是同时启动的，有一个时差。  意思是指的  都有时差，但是基数越小，重复执行有并发问题的次数越少和时间越少，越接近应该的数字。</div>2019-12-16</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/08/1c/ef15e661.jpg" width="30px"><span> 臣馟飞扬</span> 👍（4） 💬（2）<div>JAVA内存模型中说的每个线程都有自己的工作内存，然后将共享变量从主存读到自己的工作内存中进行操作，操作完后再回写到主存中。假如线程A在将共享变量读到自己的工作内存后，发生CPU切换，线程B读共享变量并操作，操作完回写主存后，线程A继续操作并回写结果，导致可见性问题。那线程的工作内存到底指什么呢？如果是指CPU缓存的话，指的是多个线程共享同一块CPU缓存还是每个线程隔离一块呢？</div>2019-03-09</li><br/>
</ul>