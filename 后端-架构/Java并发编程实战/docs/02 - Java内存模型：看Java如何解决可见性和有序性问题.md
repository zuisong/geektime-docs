上一期我们讲到在并发场景中，因可见性、原子性、有序性导致的问题常常会违背我们的直觉，从而成为并发编程的Bug之源。这三者在编程领域属于共性问题，所有的编程语言都会遇到，Java在诞生之初就支持多线程，自然也有针对这三者的技术方案，而且在编程语言领域处于领先地位。理解Java解决并发问题的解决方案，对于理解其他语言的解决方案有触类旁通的效果。

那我们就先来聊聊如何解决其中的可见性和有序性导致的问题，这也就引出来了今天的主角——**Java内存模型**。

Java内存模型这个概念，在职场的很多面试中都会考核到，是一个热门的考点，也是一个人并发水平的具体体现。原因是当并发程序出问题时，需要一行一行地检查代码，这个时候，只有掌握Java内存模型，才能慧眼如炬地发现问题。

## 什么是Java内存模型？

你已经知道，导致可见性的原因是缓存，导致有序性的原因是编译优化，那解决可见性、有序性最直接的办法就是**禁用缓存和编译优化**，但是这样问题虽然解决了，我们程序的性能可就堪忧了。

合理的方案应该是**按需禁用缓存以及编译优化**。那么，如何做到“按需禁用”呢？对于并发程序，何时禁用缓存以及编译优化只有程序员知道，那所谓“按需禁用”其实就是指按照程序员的要求来禁用。所以，为了解决可见性和有序性问题，只需要提供给程序员按需禁用缓存和编译优化的方法即可。
<div><strong>精选留言（30）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/12/69/df/2dca1305.jpg" width="30px"><span>Healtheon</span> 👍（1035） 💬（36）<div>老师，还差两个规则，分别是：
线程中断规则：对线程interrupt()方法的调用先行发生于被中断线程的代码检测到中断事件的发生，可以通过Thread.interrupted()方法检测到是否有中断发生。
对象终结规则：一个对象的初始化完成(构造函数执行结束)先行发生于它的finalize()方法的开始。

所以，个人对于Java内存模型总结起来就是：
1. 为什么定义Java内存模型？现代计算机体系大部是采用的对称多处理器的体系架构。每个处理器均有独立的寄存器组和缓存，多个处理器可同时执行同一进程中的不同线程，这里称为处理器的乱序执行。在Java中，不同的线程可能访问同一个共享或共享变量。如果任由编译器或处理器对这些访问进行优化的话，很有可能出现无法想象的问题，这里称为编译器的重排序。除了处理器的乱序执行、编译器的重排序，还有内存系统的重排序。因此Java语言规范引入了Java内存模型，通过定义多项规则对编译器和处理器进行限制，主要是针对可见性和有序性。
2. 三个基本原则：原子性、可见性、有序性。
3. Java内存模型涉及的几个关键词：锁、volatile字段、final修饰符与对象的安全发布。其中：第一是锁，锁操作是具备happens-before关系的，解锁操作happens-before之后对同一把锁的加锁操作。实际上，在解锁的时候，JVM需要强制刷新缓存，使得当前线程所修改的内存对其他线程可见。第二是volatile字段，volatile字段可以看成是一种不保证原子性的同步但保证可见性的特性，其性能往往是优于锁操作的。但是，频繁地访问 volatile字段也会出现因为不断地强制刷新缓存而影响程序的性能的问题。第三是final修饰符，final修饰的实例字段则是涉及到新建对象的发布问题。当一个对象包含final修饰的实例字段时，其他线程能够看到已经初始化的final实例字段，这是安全的。
4. Happens-Before的7个规则：
	(1).程序次序规则：在一个线程内，按照程序代码顺序，书写在前面的操作先行发生于书写在后面的操作。准确地说，应该是控制流顺序而不是程序代码顺序，因为要考虑分支、循环等结构。
	(2).管程锁定规则：一个unlock操作先行发生于后面对同一个锁的lock操作。这里必须强调的是同一个锁，而&quot;后面&quot;是指时间上的先后顺序。
	(3).volatile变量规则：对一个volatile变量的写操作先行发生于后面对这个变量的读操作，这里的&quot;后面&quot;同样是指时间上的先后顺序。
	(4).线程启动规则：Thread对象的start()方法先行发生于此线程的每一个动作。
	(5).线程终止规则：线程中的所有操作都先行发生于对此线程的终止检测，我们可以通过Thread.join（）方法结束、Thread.isAlive（）的返回值等手段检测到线程已经终止执行。
	(6).线程中断规则：对线程interrupt()方法的调用先行发生于被中断线程的代码检测到中断事件的发生，可以通过Thread.interrupted()方法检测到是否有中断发生。
	(7).对象终结规则：一个对象的初始化完成(构造函数执行结束)先行发生于它的finalize()方法的开始。
5. Happens-Before的1个特性：传递性。
6. Java内存模型底层怎么实现的？主要是通过内存屏障(memory barrier)禁止重排序的，即时编译器根据具体的底层体系架构，将这些内存屏障替换成具体的 CPU 指令。对于编译器而言，内存屏障将限制它所能做的重排序优化。而对于处理器而言，内存屏障将会导致缓存的刷新操作。比如，对于volatile，编译器将在volatile字段的读写操作前后各插入一些内存屏障。</div>2019-03-02</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/DYAIOgq83erTlRJ6skf7iawAeqNfIT1PPgjD7swUdRIRkX1iczjj97GNrxnsnn3QuOhkVbCLgFYAm7sMZficNTSbA/132" width="30px"><span>senekis</span> 👍（237） 💬（14）<div>
我思考下认为有三种方式可以实现:
1.声明共享变量abc，并使用volatile关键字修饰abc
2.声明共享变量abc，在synchronized关键字对abc的赋值代码块加锁，由于Happen-before管程锁的规则，可以使得后续的线程可以看到abc的值。
3.A线程启动后，使用A.JOIN()方法来完成运行，后续线程再启动，则一定可以看到abc==3

如有错误，请给指出错误所在！谢谢大家！谢谢老师！

听课后感觉对我帮助好大，以前零碎的知识被重新系统的整理。错误的理解也得到修正，感谢老师！</div>2019-03-02</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/61/94/713b38ef.jpg" width="30px"><span>小和尚笨南北</span> 👍（130） 💬（13）<div>补充一个： 在abc赋值后对一个volatile变量A进行赋值操作，然后在其他线程读取abc之前读取A的值，通过volatile的可见性和happen-before的传递性实现abc修改后对其他线程立即可见</div>2019-03-02</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTJUzv6S9wroydkGP6m3OsQ8QuI4jAibv21tNkm7KVGPffJibj8Y29yIdKl4qkDGd3iaGJCSGVarfxoibQ/132" width="30px"><span>狂战俄洛伊</span> 👍（77） 💬（7）<div>回复tracer的问题@tracer，你说的这个问题其实就是一个happens-before原则。例如有以下代码：
     int a = 1;&#47;&#47;代码1
     int b = 2;&#47;&#47;代码2
     volatile int c = 3;&#47;&#47;代码3
     int d = 4;&#47;&#47;代码4
     int e = 5;&#47;&#47;代码5
编译器解释这5行代码的时候，会保证代码1和代码2会在代码3之前执行，而代码1和代码2的执行顺序则不一定（这就是重排序，在不影响执行结果的情况下，虚拟机可能会对命令重排。当然所谓的不影响执行结果，java只保证在单线程中不影响执行结果）。代码4和代码5也一定会在代码3之后执行，同理代码4和代码5的执行顺序也是不一定的。
    所以这篇文章中你说的那段代码，由于v是volatile修饰的，对v的赋值永远在对x的赋值之后。所以在reader中输出的x一定是42</div>2019-03-02</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/63/14/06eff9a4.jpg" width="30px"><span>Jerry银银</span> 👍（62） 💬（17）<div>思考题的通用性表述为：如何保证一个共享变量的可见性？
有以下方法：
1. 保证共享变量的可见性，使用volatile关键字修饰即可
2. 保证共享变量是private，访问变量使用set&#47;get方法，使用synchronized对方法加锁，此种方法不仅保证了可见性，也保证了线程安全
3. 使用原子变量，例如：AtomicInteger等
4. 最后一种不是办法的办法：保证多个线程是「串行执行」^_^</div>2019-03-02</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/36/d2/c7357723.jpg" width="30px"><span>发条橙子 。</span> 👍（47） 💬（11）<div>感悟 ： 
老师用第一篇介绍了造成并发问题的由来引出了此文如果解决其中的 可见性、排序性问题 。 有了第一篇做铺垫让此篇看起来更加的流畅 。 

尤其以前看书中讲解 happens-before原则只是单单把六个规则点列了出来，很难吃透。此篇文章给出详细的事例逐点分析，使得更好的去理解每个点。 

例如 我之前看到的文章都说 在单线程中不会出现有序性问题 ，在多线程中会出现有序性问题。 之前很难理解单线程中没有有序性的问题是什么原因， 原来是happens-before第一条规则限制住了编译器的优化

问题： 
第一个例子中添加了 volatile 关键字， 如果例子中 ， v变量没有使用volatile ，那么x会是什么呢 ？？
答案： 42

我的思考是， 没有了volatile那么规则二就不满足 ， 但是规则一和规则三还是满足 ，虽然 writer()方法修改 v不能让其他立即可见，但是如果是循环调用reader()方法 ，等到可见到 v == true，根据第一条原则 ， x happens-before v ，所以能读到 x=42 

老师请问我的判断正确么？


思考题 ：

一个共享变量在一个线程中修改让另其他线程可见， 那就是解决可见性（缓存）的问题 , happens-before的规则就是用于对可见性进行约束的

按照老师课中所讲 ：
思考如下：

  1. 第一条规则同线程中编译会保证顺序性 ， 和问题不符合 

 2. 第二条规则 ， 使用volatile关键字 ， 这个关键字可以让其他线程写之前先读最新的值，所以保证读到的是最新的值 ，可行

3. 第三条规则 ，传递性， 和问题不符

4. 第四条规则， 使用管程，由于是访问共享变量，如果是在syn中修改值只能保证当前线程下一次进入syn可以看见最新的值，其他线程直接访问还可能不是最新值 ， 不行

5. 第五条规则 ， 如果前提是其他线程都在 主线程修改abc变量后 start()，则可见

6. 第六条规则 ，如果前提是其他线程等 修改abc变量线程 join()执行，则可见

  7.   Final关键字， 由于final关键字表示已经定义了常量，任意线程都不可以修改， 不可用 

综上总结 ： 

使用2 添加volatile可行 。在符合某些场景下时，56可让其他线程可见


</div>2019-03-02</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/14/50/c23cf47d.jpg" width="30px"><span>李</span> 👍（44） 💬（6）<div>老师，第一章里提到程序中x=5；x=6可能被重排。可是今天第一个规则里提到，同一个线程里，是顺序的。这两个不就矛盾了吗？</div>2019-03-03</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/29/9e/380a01ea.jpg" width="30px"><span>tracer</span> 👍（37） 💬（3）<div>我明白了，写先于读指的是不会因为cpu缓存，导致a线程已经写了，但是b线程没读到的情况。我错误理解成了b要读，一定要等a写完才行</div>2019-03-02</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/ed/4d/1d1a1a00.jpg" width="30px"><span>magict4</span> 👍（26） 💬（5）<div>老师你好，

我对『3. 传递性』中您的解释，还是有点疑惑。感觉许多留言的小伙伴们也都有类似的疑惑，还请老师再耐心回答一次。

您提到：
&gt; “x=42” Happens-Before 写变量 “v=true” ，这是规则 1 的内容；
我的疑惑：变量 x 和 v 没有任何依赖关系，为什么对 x 的赋值 Happens-Before 对 v 的赋值呢？

这个 Happens-Before 关系，根据我的理解，不是由规则 1 决定的，而是有 volatile 决定的。如果 v 没有被 volatile 修饰，编译器是可以对 x、v 的赋值语句进行重排的。 不知道我的理解是否有问题？</div>2019-03-04</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/e9/0b/1171ac71.jpg" width="30px"><span>WL</span> 👍（26） 💬（3）<div>想问一下老师最后关于逸出的例子，是因为有可能通过global.obj 可能访问到还没有初始化的this对象吗，但是将this赋值给global.obj不也是初始化时才赋值的吗，这部分不太理解，请老师指点一下</div>2019-03-02</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/bc/eb/c22ef3a5.jpg" width="30px"><span>Nevermore</span> 👍（22） 💬（5）<div>&#47;&#47; 以下代码来源于【参考 1】
class VolatileExample {
  int x = 0;
  volatile boolean v = false;
  public void writer() {
    x = 42;
    v = true;
  }
  public void reader() {
    if (v == true) {
      &#47;&#47; 这里 x 会是多少呢？
    }
  }
}


感觉老师对这个volatile变量规则这块讲的有点草率，volatile变量的写对于读是可见的，对于程序来说，也就是线程A执行write中的v=true对于reader中的v==true是可见的 ，但是这对于x有什么关系？x并没有被volatile修饰。
根据我的理解，volatile强制所修饰的变量及它前边的变量刷新至内存，并且volatile禁止了指令的重排序。
 
望指正
</div>2019-03-02</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/69/c6/513df085.jpg" width="30px"><span>强哥</span> 👍（15） 💬（3）<div>关于java内存模型、jvm内存结构及java对象模型分别深入讲解一下，这样效果更好一些。</div>2019-03-02</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/09/98/b11c372b.jpg" width="30px"><span>鸠翱</span> 👍（13） 💬（3）<div>对于@Junzi的问题：
x=45; &#47;&#47; 1
v=true; &#47;&#47; 2
这两行会不会导致指令重排？ 答：不会
如果这两行重排序了，那么线程B读取到read()的时候也有可能出现x=0，也就是说线程B看到了v=true却没又看到x=45，这不符合第一条规则（请问老师 这么理解对不对）
我课外查询了一下，从实现方法上，volatile的读写前后会插入内存屏障，保证一些操作是无法没重排序的，其中就有对于volatile的写操作之前的动作不会被重排序到之后</div>2019-03-04</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/1d/13/31ea1b0b.jpg" width="30px"><span>峰</span> 👍（11） 💬（1）<div>我觉得课后题其实就是利用happenbefore规则去构建abc的写入happenfore于另外一个线程的读取。而6条规则中传递性规则是纽带，然后采用比如规则4，就是把abc的赋值加入一同步块，并先执行，同时另外一个线程申请同一把锁即可。其他的也类似。

java内存模型对程序员来说提供了按需禁止缓存禁止指令重排的方法。这是我第一次看到这么简单又深刻的解释，老师棒棒哒！！！</div>2019-03-02</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/72/b1/a8b272ef.jpg" width="30px"><span>飞翔的花狸猫</span> 👍（10） 💬（2）<div>Happen-before 这个知识点终于理解了，追并发专栏比以前看小说还勤快，盼老师速更啊</div>2019-03-02</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/b7/f0/a570f68a.jpg" width="30px"><span>wang</span> 👍（9） 💬（1）<div>老师。对呀 发条橙子 提到如果不加 volatile，当读到v的时候，x就一定能读到42，使用的是使用的是规则1。
我认为不对呀，规则一不是只适用于单线程吗？而读取v是在另一个线程，所以不能使用规则一判断吧。
希望老师可以解释一下，谢谢</div>2019-03-02</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/f3/b1/0429aa3b.jpg" width="30px"><span>青冰白夜</span> 👍（8） 💬（1）<div>那老师，就我的那个问题，
int i=0 ;
int j=1;
您也说了，可能重排序成
int j=1;
int i=0;
那int i=0明明是在前面，这重排序在后面，不就不符合happens-befor的程序顺序性规则了吗？</div>2019-03-03</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/29/9e/380a01ea.jpg" width="30px"><span>tracer</span> 👍（7） 💬（1）<div>测试重排序可以使用OpenJDK CodeTools 项目的jcstress 工具, 详细见极客时间深入拆解虚拟机13讲和https:&#47;&#47;wiki.openjdk.java.net&#47;display&#47;CodeTools&#47;jcstress</div>2019-03-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/6a/e9/d76511d8.jpg" width="30px"><span>Yesterday</span> 👍（7） 💬（2）<div>我有一个问题一直弄不明白，volatile 禁用指令重排的边界如何确定？synchornzied 包裹的代码块有明确的边界，不管是否在临界区内的代码是否调用其他方法。

而对 volatile 类型变量前后的变量的操作并没有明确的语义上的边界？查了很多资料，仍然没有找到答案，希望老师解答一下。
</div>2019-03-04</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/06/96/6ae77c39.jpg" width="30px"><span>柳絮飞</span> 👍（7） 💬（1）<div>王老师，请教一下，为什么这些编译优化规则叫内存模型？jvm的堆和栈应该叫什么？多谢！这样叫是不是容易让人误解</div>2019-03-04</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/66/75/54bb858e.jpg" width="30px"><span>life is short, enjoy more.</span> 👍（5） 💬（1）<div>新学生对本门课程的第一次留言~
&#47;&#47; 以下代码来源于【参考 1】
final int x;
&#47;&#47; 错误的构造函数
public FinalFieldExample() { 
  x = 3;
  y = 4;
  &#47;&#47; 此处就是讲 this 逸出，
  global.obj = this;
}

老师你好，这个例子我不是很理解，看到你给其他同学的答复是，this可能没有初始化完。但是这不就是一个构造函数吗，this位于构造函数的最后一行，而且x已经赋值了，为什么可能存在其他线程读到x==0的情况呢？</div>2019-03-18</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTI9kA8IicSJFKtglFv10EHGmLgCRGET22HylnXB7pT0xibjOYtDia0cib4uuSnvOJSINeoF71LAKU1F4A/132" width="30px"><span>Geek_faf1c5</span> 👍（5） 💬（1）<div>老师您好：
cpu缓存导致的可见性  cpu运行的单位是线程 而每个线程有本地内存 因为有线程本地内存的存在 也会导致可见性问题  那么线程的本地内存和cpu缓存是一会事吗  有什么关联？？？？</div>2019-03-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/d0/03/2e632d36.jpg" width="30px"><span>Geek_c42505</span> 👍（5） 💬（1）<div>1. 使用volatile修饰abc -禁止cpu缓存直接从内存获取和volatile写 happens before volatile读。
2. synchronized 代码块中操作abc 解锁happens before 加锁。
3. 线程A操作共享变量abc然后start方法启动B线程 B线程中可见abc操作。
4. 线程A操作共享变量abc，B join A 对于B线程可见。
不知道叙述的是否准确，忘老师指正</div>2019-03-05</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/DYAIOgq83eoRiaKX0ulEibbbwM4xhjyMeza0Pyp7KO1mqvfJceiaM6ZNtGpXJibI6P2qHGwBP9GKwOt9LgHicHflBXw/132" width="30px"><span>Geek_ebda96</span> 👍（5） 💬（2）<div>我理解的volatile 在操作系统层面，在修改变量的值时候，cpu缓存锁还是要加锁，修改完成后从缓存写入内存，锁才释放，锁的过程中，其他线程读是要等待写入完成，只不过这个锁的时间很短，所以一般感受不出来吧，不然线程a写入还没完成，线程b读取变量值不是最新的，这才能保证写对读可见性，望指正</div>2019-03-04</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/17/06/7e/735968e2.jpg" width="30px"><span>西门吹牛</span> 👍（4） 💬（1）<div>逸出：
在构造方法中将this 复制给别的变量，意味着，构造方法还没结束，对象this 就给别人使用了。对象还没初始化完成，别人就使用，类似双层校验创建单例的例子。
逸出要避免，要避免这种写法。
同时，如果在构造方法中对成员变量赋初始值，比如this.x = x，这样的代码在编译的时候，也会被重排序，将赋值操作重排序到构造方法之外，那么也就是，构造方法结束了，初始化完成了，这时候，别的线程先后可能会读取到俩个不同的值，一个没初始化的，一个初始化后的值。要避免这种情况的发送，就要用fianl，final修饰的变量，可以保证，不会被抽排序到构造方法之外，那么就保证了，只要别的线程拿到该对象的引用，那么改对象的fianl修饰的变量，别的线程一定是能读到在构造方法中初始化的值的，避免了上面同一变量，读取值俩次不一样的问题。</div>2020-09-02</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/cb/6f/c78ef1cf.jpg" width="30px"><span>王二北</span> 👍（4） 💬（2）<div>&quot;分析一下，为什么 1.5 以前的版本会出现 x = 0 的情况呢？我相信你一定想到了，变量 x 可能被 CPU 缓存而导致可见性问题。”， 这句话是不是有问题，线程B读取到变量x为0，不是因为cpu缓存导致的可见性问题，而应该是 指令重排导致的。</div>2019-04-27</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/PiajxSqBRaELZPnUAiajaR5C25EDLWeJURggyiaOP5GGPe2qlwpQcm5e3ybib8OsP4tvddFDLVRSNNGL5I3SFPJHsA/132" width="30px"><span>null</span> 👍（4） 💬（2）<div>@发条橙子… 的思考题分析，有些不太准确吧，例如评论里指出的程序顺序性。还有 synchronized 的分析也不太准确吧，synchronized(abc) 可能保证后续操作可见。

老师是否应该在回复评论时指正，否则童鞋们看到“分析得比我好”的回复，很大可能就照着分析来理解了。</div>2019-04-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/16/31/929f811e.jpg" width="30px"><span>Hello,Hello,Hello Kitty</span> 👍（4） 💬（1）<div>x = 42;
v = true;
老师 我想请假一下 x并没有加volatile修饰 JVM是如何保证x的结果也是被可见呢 是因为x跟v都在同一个寄存器中 voatile修饰的v被刷新回内存的时候 整个寄存器中的值都被刷新到内存中了吗？
</div>2019-03-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/f8/a1/8780f900.jpg" width="30px"><span>封万里</span> 👍（4） 💬（1）<div>happens-before的第一个规则实际上禁止了指令重排序，可以这么理解吗？希望老师解答一下呢</div>2019-03-03</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/e5/a5/fae40ac3.jpg" width="30px"><span>倚梦流</span> 👍（4） 💬（1）<div>这里实例里的共享变量为什么没有用static修饰？是因为这里的线程操作的都是同一个实例，所以共享变量不需要用static修饰吗？如果用了static，结果应该也是一样的吧</div>2019-03-02</li><br/>
</ul>