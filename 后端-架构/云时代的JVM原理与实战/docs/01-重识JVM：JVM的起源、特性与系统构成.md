你好，我是康杨。欢迎你加入学习，和我一起开启JVM的探索之旅。

作为这门课程的第一讲，我希望通过我的介绍，能让你对JVM有一个整体的认知。我将从JVM的起源、它的基本特性、内部构成，以及它与我们常说的JDK、JRE的关系等多个维度展开，让你知其然并知其所以然。

## JVM的起源

区别于很多课程以“hello world” 开篇，我们今天从一个实际的需求开始。假设你是一家餐厅的老板，需要计算过去一周的营收总和，过去一周每天的营收分别是 102、230、320、431、130。假如你生活在公元前，这时候你可能就需要用结绳记事的方式来进行计算。

而如果你生活在20世纪50年代，那么恭喜你，你可以用计算机帮你计算了。幸亏有了计算机，不然，如果要算一年的营收，不知道要用掉多少根绳子，算多长时间呢。

当然，现在的你，显然会用更简单的方式得到结果，通过下面这段代码，JVM就会帮你完成运算，你甚至不用考虑是在Windows上运行，还是在苹果电脑上运行，因为JVM会帮你搞定。

```java
int[] arr = { 102，230，320，431，130};
int sum = 0;   
for(int i: arr){   
   sum += i;
}
System.out.println("Sum is: " + sum);
```
<div><strong>精选留言（13）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/0f/96/d9/a252585b.jpg" width="30px"><span>喆</span> 👍（10） 💬（4）<div>“相对于普通计算机基于寄存器的架构，JVM 是基于栈的虚拟机，正是因为基于栈的特性，使 JVM 具备了平台无关性”，基于栈的特性是什么意思，什么叫基于栈？可以展开说一下吗？为什么基于栈的特性就能平台无关了？</div>2023-08-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/d0/91/89123507.jpg" width="30px"><span>Johar</span> 👍（2） 💬（1）<div>请教一下加载的class文件什么时候会卸载？</div>2023-08-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/1e/f2/453d5f88.jpg" width="30px"><span>seker</span> 👍（1） 💬（1）<div>文稿中的代码，如果thread1先执行完，那么程序会正常输出1。如果是thread2先执行完，那么程序没有任何输出。由于引入多线程，导致线程执行先后顺序不确定出现上述问题。

从程序的意图看是想thread1先写，thread2再读，那么修改start()、join()顺序就可以避免问题。即修改为：
thread1.start(); 
thread1.join();
thread2.start();
thread2.join();

但如果是writer()和reader()都有多个线程进入，那就是另外的解决方案了。

所以还是想问老师那段代码的意图是什么？</div>2023-08-25</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/1e/f2/453d5f88.jpg" width="30px"><span>seker</span> 👍（0） 💬（1）<div>JVM 和普通计算机的关系是什么？

这里的普通计算机我理解就是物理机，是一种硬件。JVM终究是一个软件，不过可以进行内存管理、线程管理。在JVM之上可以运行Java应用程序，以及其它可以编译为字节码的编程语言。因此我觉得JVM更像是一个虚拟的操作系统，而Java应用程序则运行在这个虚拟的操作系统之上。

没有硬件作为支撑，那么软件将无法运行。因此软件对硬件是有依赖关系的。</div>2023-08-25</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/7a/56/29877cb9.jpg" width="30px"><span>临风</span> 👍（0） 💬（1）<div>问题1：对于这段代码，存在两个问题。
1.join的作用是等待线程执行结束，再继续往后执行，但thread2已经start了，所以我们没办法保证thread1和thread2谁先执行，flag显然是不能保证代码执行的先后顺序的，可以通过信号量或者CountDownLatch来解决（暂时只想到了这两个，不知道还有没用别的更好的方式）。
2.变量a缺乏volatile修饰，两个可能线程会读取各自线程中的值，导致reader执行的时候取的还是0。

问题2：
jvm就是对操作系统和硬件资源的抽象封装，让你无需考虑是x86还是arm的CPU，也不用管是window是还是Linux的操作系统，实现了一次编译到处运行。本质就是让你只关注自己的代码逻辑，而不用考虑底层硬件和操作系统的区别，但实际上这些事情还是得有人做的，只不过是jvm替你做了，这也就导致了一定程度上的性能损耗。但云原生时代的到了，docker的普及，因为已经对运行环境做了一层封装，大家都是执行镜像，导致Java的优势也就荡然无存了，反而因为其需要支持运行时的问题，启动服务缓慢，无法实现秒级的扩缩容而举步维艰。这些就是我的一些浅薄的认识，希望之后跟着老师能加深对云原生时代Java的理解。

附问题1的代码：
public class Demo {
    private volatile int a = 0;
    private final Semaphore semaphore = new Semaphore(1);

    public void writer() {
        a = 1;
        semaphore.release();
    }

    public void reader() {
        try {
            semaphore.acquire();
        } catch (InterruptedException e) {
            throw new RuntimeException(e);
        }
        int i = a * a;
        System.out.println(i);
    }

    public static void main(String[] args) throws InterruptedException {
        final Demo example = new Demo();
        Thread thread1 = new Thread(() -&gt; example.writer());
        Thread thread2 = new Thread(() -&gt; example.reader());
        thread1.start();
        thread2.start();
        thread1.join();
        thread2.join();
    }
}</div>2023-08-23</li><br/><li><img src="" width="30px"><span>edward</span> 👍（0） 💬（1）<div>最后这张图很赞👍</div>2023-08-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1f/5e/81/82709d6e.jpg" width="30px"><span>码小呆</span> 👍（0） 💬（1）<div>jvm 对于计算机来说,只能算是一个中间件工具,用于把字节码翻译成计算机能识别的机器码而已!</div>2023-08-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/18/75/bc/89d88775.jpg" width="30px"><span>Calvin</span> 👍（0） 💬（1）<div>给大佬点赞666，期待半桶水的自己学习这个课程后能查漏补缺底层知识更精进一些，PS：JVM 虚拟机类比真实的计算机之前我怎么没想到呢？😂

另外我看思考题有提到Thread线程，而 JDK 21 下个月就要 GA 了，到时“虚拟线程”（协程）就正式可用了，不知道利用其结构化编程能力能否实现优化它的目的？

以及大佬会否考虑在后面的章节中添加相关的知识点或者加餐介绍一下这个新特性呢？</div>2023-08-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/21/2f/b29e8af8.jpg" width="30px"><span>轻风悠扬</span> 👍（0） 💬（1）<div>flag应该用volatile来修饰以确保对其他线程可见。</div>2023-08-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/de/ca/73f15fe7.jpg" width="30px"><span>老衲</span> 👍（1） 💬（1）<div>public class Demo {
    private AtomicInteger a = new AtomicInteger(0);
    private volatile boolean flag = false;

    public void writer() {
        a = new AtomicInteger(1);
        flag = true;
    }

    public void reader() {
        if (flag) {
            int i = a.get() * a.get();
            System.out.println(i);
        }
    }

    public static void main(String[] args) throws InterruptedException {
        final Demo example = new Demo();
        Thread thread1 = new Thread(example::writer);
        Thread thread2 = new Thread(example::reader);
        thread1.start();
        thread2.start();
        thread1.join();
        thread2.join();
    }
}</div>2023-08-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/20/82/72/e6a56c30.jpg" width="30px"><span>ZYJ</span> 👍（0） 💬（0）<div>思考题:
1,如果想让程序输出1,只需要调整thread1.join()的顺序,让主线程等待thread1执行完再start t2线程
2,join的原理是,主线程调用thread1.join()时,join里会调用wait方法使主线程等待, 等thread1执行完后才会唤醒主线程(run方法里,最终会notifyAll唤醒主线程)
3,此时两个线程其实是串联执行,没有并发问题, 但是如果是多个线程的话, 需要给共享变量加上volatile保证可见性(原理:变量读取和写入前后加入内存屏障,保证刷新到主内存)
疑问:
老师在下面评论里提到的volatile和Raft协议的关系具体指的是什么?

final Demo example = new Demo();
 Thread thread1 = new Thread(() -&gt; example.writer()); 
Thread thread2 = new Thread(() -&gt; example.reader()); 
thread1.start(); 
thread1.join(); 
thread2.start(); 
thread2.join();</div>2023-09-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/2b/c7/5d/40bdba38.jpg" width="30px"><span>on</span> 👍（0） 💬（0）<div>文中指出的重排的例子不是很好吧。他实际和cpu线程调度关系更大点，指令重排体现不出来</div>2023-09-07</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/e3/41/bd0e3a04.jpg" width="30px"><span>雷小鸿</span> 👍（0） 💬（1）<div>其实 我看到这段代码，没想要怎么去改，我再想什么情况下，什么业务场景下，会这样写代码，我自己在什么场景下会这样写，对于我们这种业务小的公司很难再实际开发中这样去写。</div>2023-08-24</li><br/>
</ul>