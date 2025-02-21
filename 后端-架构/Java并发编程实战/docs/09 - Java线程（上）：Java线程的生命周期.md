在Java领域，实现并发程序的主要手段就是多线程。线程是操作系统里的一个概念，虽然各种不同的开发语言如Java、C#等都对其进行了封装，但是万变不离操作系统。Java语言里的线程本质上就是操作系统的线程，它们是一一对应的。

在操作系统层面，线程也有“生老病死”，专业的说法叫有生命周期。对于有生命周期的事物，要学好它，思路非常简单，只要能搞懂**生命周期中各个节点的状态转换机制**就可以了。

虽然不同的开发语言对于操作系统线程进行了不同的封装，但是对于线程的生命周期这部分，基本上是雷同的。所以，我们可以先来了解一下通用的线程生命周期模型，这部分内容也适用于很多其他编程语言；然后再详细有针对性地学习一下Java中线程的生命周期。

## 通用的线程生命周期

通用的线程生命周期基本上可以用下图这个“五态模型”来描述。这五态分别是：**初始状态、可运行状态、运行状态、休眠状态**和**终止状态**。

![](https://static001.geekbang.org/resource/image/9b/e5/9bbc6fa7fb4d631484aa953626cf6ae5.png?wh=1142%2A714)

通用线程状态转换图——五态模型

这“五态模型”的详细情况如下所示。

1. **初始状态**，指的是线程已经被创建，但是还不允许分配CPU执行。这个状态属于编程语言特有的，不过这里所谓的被创建，仅仅是在编程语言层面被创建，而在操作系统层面，真正的线程还没有创建。
2. **可运行状态**，指的是线程可以分配CPU执行。在这种状态下，真正的操作系统线程已经被成功创建了，所以可以分配CPU执行。
3. 当有空闲的CPU时，操作系统会将其分配给一个处于可运行状态的线程，被分配到CPU的线程的状态就转换成了**运行状态**。
4. 运行状态的线程如果调用一个阻塞的API（例如以阻塞方式读文件）或者等待某个事件（例如条件变量），那么线程的状态就会转换到**休眠状态**，同时释放CPU使用权，休眠状态的线程永远没有机会获得CPU使用权。当等待的事件出现了，线程就会从休眠状态转换到可运行状态。
5. 线程执行完或者出现异常就会进入**终止状态**，终止状态的线程不会切换到其他任何状态，进入终止状态也就意味着线程的生命周期结束了。
<div><strong>精选留言（30）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/10/28/9c/73e76b19.jpg" width="30px"><span>姜戈</span> 👍（407） 💬（12）<div>可能出现无限循环，线程在sleep期间被打断了，抛出一个InterruptedException异常，try catch捕捉此异常，应该重置一下中断标示，因为抛出异常后，中断标示会自动清除掉！
Thread th = Thread.currentThread();
while(true) {
  if(th.isInterrupted()) {
    break;
  }
  &#47;&#47; 省略业务代码无数
  try {
    Thread.sleep(100);
  }catch (InterruptedException e)｛
    Thread.currentThread().interrupt();
    e.printStackTrace();
  }
}</div>2019-03-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/94/47/75875257.jpg" width="30px"><span>虎虎❤️</span> 👍（124） 💬（6）<div>我的一位长辈曾告诉我，没有真正学不会的知识或者技术，只是缺乏好的老师。

有的人可以把复杂的知识讲明白，但是讲解的过程却也是晦涩难懂，不免落了下成。

而学习王老师的课，我一直都觉得很轻松。云淡风轻地就把并发知识抽丝剥茧，确是更显功力。另一方面，我觉得人的大脑更喜欢接受这些平易近人的文字。看似浅近的文字，却更能带领我深入的思考，留下更深刻的印象。反观一些看起来高端大气上档次的论述，让人觉得云山雾罩，好不容易看懂了，但看过后却什么也想不起来了。大概是读文章的时候脑细胞都用来和晦涩的文字做斗争了，已经没有空间去思考和记忆了。

再次感谢王老师给大家带来优秀的课程。</div>2019-03-19</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/15WXictKcv02AGs8PPBGvykHg3tYc7Xb33xs0iayGLMIYdFhlPoHe0ABw5F93yyInM9D5nDSAU7TWwROz4rTk0YA/132" width="30px"><span>Tristan</span> 👍（98） 💬（16）<div>为什么实战高并发程序设计医术中写道“Tread.stop()方法在结束线程时，会直接终止线程，并且会释放这个线程所持有的锁”，而您文中所写的“果线程持有 synchronized 隐式锁，也不会释放”？？</div>2019-04-14</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTKb5BzdGZbSYFlk3fx1QIeNuwo9TmRQyb29b7KJd8ibdWt4L6KYGpXJWGPJJh29s09I2ZJtZ59ktJQ/132" width="30px"><span>thas</span> 👍（49） 💬（3）<div>interrupt是中断的意思，在单片机开发领域，用于接收特定的事件，从而执行后续的操作。Java线程中，（通常）使用interrupt作为线程退出的通知事件，告知线程可以结束了。
interrupt不会结束线程的运行，在抛出InterruptedException后会清除中断标志（代表可以接收下一个中断信号了），所以我想，interrupt应该也是可以类似单片机一样作为一种通知信号的，只是实现通知的话，Java有其他更好的选择。
因InterruptedException退出同步代码块会释放当前线程持有的锁，所以相比外部强制stop是安全的（已手动测试）。sleep、join等会抛出InterruptedException的操作会立即抛出异常，wait在被唤醒之后才会抛出异常（就像阻塞一样，不被打扰）。
另外，感谢老师提醒，I&#47;O阻塞在Java中是可运行状态，并发包中的lock是等待状态。</div>2019-03-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/54/44/4e541a86.jpg" width="30px"><span>Junzi</span> 👍（38） 💬（2）<div>当发起中断之后，Thread.sleep(100);会抛出InterruptedException异常，而这个抛出这个异常会清除当前线程的中断标识，导致th.isInterrupted()一直都是返回false的。

InterruptedException - if any thread has interrupted the current thread. The interrupted status of the current thread is cleared when this exception is thrown.</div>2019-03-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/d9/93/098e5ef5.jpg" width="30px"><span>海鸿</span> 👍（21） 💬（5）<div>如果线程处于阻塞状态（BLOCKED）,此时调用线程的中断方法，线程会又如何反应?
是否会像等待状态一样抛异常?
还是会像运行状态一样被标记为已中断状态?
还是不受到任何影响?
麻烦老师解答一下😁</div>2019-03-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/0d/24/b07de4f2.jpg" width="30px"><span>WhoAmI</span> 👍（17） 💬（1）<div>老师，Java调用阻塞API时，Java层面是runnable，那仍然占用CPU吗，此时此线程在操作系统中是什么状态呢？这个问题好几个人都在问，能详细解释下吗？</div>2019-03-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/e5/67/16322a5d.jpg" width="30px"><span>cky.宇</span> 👍（15） 💬（2）<div>根据接口文档描述，stop()虽然也会中止线程并释放锁，但是没有提供一种补偿的机会，可能某个线程对共享对象进行了不完整的修改，此时如果stop后，该共享对象会继续被其他线程使用，造成线程安全问题。interrupt()则是提供给使用者一种被中断后补偿的机会，例如回滚之前的修改。个人理解是这样的，请老师指点一下。</div>2019-11-04</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/1d/b5/971261fd.jpg" width="30px"><span>alias cd=rm -rf</span> 👍（13） 💬（5）<div>思考题，不能中断循环，异常捕获要放在while循环外面
</div>2019-03-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/44/f6/60f948e1.jpg" width="30px"><span>Aven</span> 👍（10） 💬（1）<div>老师，您好，想问下，在讲到“java调用阻塞api的情况下，java程序仍然是Runnable状态”这里的时候，我不太理解，哪些api是属于阻塞api呢</div>2019-07-02</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/4f/a5/71358d7b.jpg" width="30px"><span>J.M.Liu</span> 👍（10） 💬（2）<div>感谢老师提醒，原来jvm层面的线程状态和os层面上的线程状态是不一样的，i&#47;o挂起在jvm也是runable状态。另外并发包的lock其实是处于waitting状态。
但是有个疑问，jvm中blocked状态的线程和waitting状态的线程，除了处在不同的队列之外，还有没有什么区别呀？我这里问的区别包括jvm和os两个层面，谢谢老师</div>2019-03-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/64/86/f5a9403a.jpg" width="30px"><span>yang</span> 👍（8） 💬（1）<div>
public class TestThread {

	public static void main(String[] args) throws InterruptedException {

		Worker t = new Worker();
		t.start();

		Thread.sleep(2000);
		
		System.out.println(&quot;-1-1-1-&quot;);
		t.interrupt();
		System.out.println(&quot;000000&quot;);
		Thread.sleep(2000);
		t.stop();
		System.out.println(&quot;000111&quot;);
		Thread.sleep(2000);
		t.join();
		System.out.println(&quot;111111&quot;);
	}

}

class Worker extends Thread {

	@Override
	public void run() {
		int i = 0;
		while (i&lt;20) {
			if (Thread.currentThread().isInterrupted()) {
				break;
			}
			++i;
			System.out.println(Thread.currentThread().getName() + &quot;i: &quot; + i);
			try {
				Thread.sleep(1000);
			} catch (InterruptedException e) {
				&#47;&#47; TODO Auto-generated catch block
				e.printStackTrace();
			}
		}
	}
}

----------------------------------------------------------------------------
忽然发现极客时间网页版的留言窗口好小啊，都看不到自己上面写的东西...
----------------------------------------------------------------------------

1. 如果worker中没有sleep方法，则调用th.interrupt()方法会真正的中断th线程，并且不会抛出InterruptException 但是该演示代码不能体现锁的释放；
2. 如果worer中有sleep方法，则调用th.interrupt()方法会抛 java.lang.InterruptException(), 是针对sleep方法抛出的
	同样的Object的wait() wait(带参) 也会抛出java.lang.InterruptException()而从当前的wait&#47;blocked状态被中断（唤醒）
	那也就是说，throws InterruptedException 的方法 在线程被调用interrupt()方法后，会被从当前状态中断
	至于调用interrupy()方法后线程的状态属于哪种，取决于interrupt方法前的执行的方法使得当前线程处于哪种状态，
	老师的总结很到位，需要好好理解，感受~！
3. 无论worder的run中有没有slee()方法，stop都会直接中断线程，当前演示代码也无法演示锁没有被释放
4. join()总是在等待被调用的线程执行完毕
5. while循环放在try里面, 在调用th.interrupt之后，可以有效捕获InterruptException 从而使th线程中断

说的有点多了， 大家多多讨论~！~！~！

</div>2019-03-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/04/13/aac9b508.jpg" width="30px"><span>悟</span> 👍（8） 💬（3）<div>老师 stop方法直接杀掉线程了，什么不会释放锁呢</div>2019-03-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/b4/3b/a1f7e3a4.jpg" width="30px"><span>ZOU志伟</span> 👍（6） 💬（1）<div>老师，我有个疑问，文章中讲到线程调用阻塞式 API 时，不会转换到 BLOCKED 状态，而是保持RUNNABLE状态，想知道这些阻塞式API是什么？</div>2019-03-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/52/32/bb570f48.jpg" width="30px"><span>向往的生活</span> 👍（6） 💬（3）<div>当线程 A 处于 WAITING、TIMED_WAITING 状态时，如果其他线程调用线程 A 的 interrupt() 方法，会使线程 A 返回到 RUNNABLE 状态，同时线程 A 的代码会触发 InterruptedException 异常。此时如果线程A获取不到锁，岂不是会立马又变成BLOCKED 状态？</div>2019-03-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/6e/8e/5d309a85.jpg" width="30px"><span>拯救地球好累</span> 👍（5） 💬（2）<div>---总结---
1. JAVA的线程生命周期模型在操作系统的基础上稍作了修改，一是Runnable表示可运行与运行状态（等待资源依然是Runnable），二是将休眠状态扩展成了Blocked&amp;Waiting&amp;Time_waiting三种状态

---启发---
1. 作为工程师能搞懂理论模型并能在其基础上按需求变化是个必备的能力
2. 对使用的任何类，懂得其原理和设计理念能保证更好地使用
3. 对使用的任何方法，懂得其操作方式和可能出现的异常也非常重要
4. 养成看doc的习惯

---课后思考---
sleep方法的java doc中写道“if any thread has interrupted the current thread. The interrupted status of the current thread is cleared when this exception is thrown.”
因此在try-catch中出现的中断异常被捕获后不做处理将会导致interruped status被清理。</div>2019-07-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/17/ce/43/317ddb97.jpg" width="30px"><span>粉色记忆</span> 👍（4） 💬（1）<div> Thread.join() 这个方法有些不解，举个例子：在主线程起个周期性任务，在周期性任务启动前调用join，join什么时候算执行完？是周期性任务一次执行完？还是周期执行完？如果是周期执行完，那么主线程不是永远备阻塞了，主线程永久阻塞不现实，那就是一次执行完？


老师，虾米在线等？
</div>2019-06-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/4e/29/4b0d7a05.jpg" width="30px"><span>ren</span> 👍（3） 💬（2）<div>老师。那么jvm在进行gc的时候的停顿所有线程(stw) 这个期间 jvm中的线程应该属于生命周期的哪一个状态呢？ 我看到有资料讲的是 jvm中的线程 会因为jvm设置的安全点和安全区域 执行test指令产生一个自陷异常信号 这个指令应该是汇编中的触发线程中断的 那么之后的恢复成运行状态也都是交给操作系统层面来实现的吗？</div>2019-03-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/4e/3a/86196508.jpg" width="30px"><span>linqw</span> 👍（3） 💬（2）<div>老师，不知道能否在理论讲解清楚的同时也能补上对源码的分析，比如线程a的interrupt方法被其他线程调用，有两种形式检测，异常和使用isInterrupted检测，但是内部原理还是感觉不清楚不明白，根据异常它是如何中断的？还有java有阻塞和等待状态，但是没能理解java为什么要将其区分开来，比如阻塞是在获取不到锁阻塞，会在锁对象中的队列排队，wait等待状态，不是也会在调用的对象队列中排队么？不太清楚为什么要怎么做？</div>2019-03-24</li><br/><li><img src="" width="30px"><span>刘同青</span> 👍（2） 💬（3）<div>老师好，经过测试stop一个持锁线程，无论是synchronized的隐士锁，还是JUC中的Lock，都是自动释放的，测试如下：
测试1：测试synchronized
public class TestStopSynchronized {
    public static void main(String[] args) throws Exception {
        Thread thread1 = new MyThread();
        thread1.setName(&quot;thread1&quot;);
        thread1.start();
        sleep(3);
        Thread thread2 = new MyThread();
        thread2.setName(&quot;thread2&quot;);
        thread2.start();
        sleep(3);
        System.out.println(nowTime() + &quot; stop thread1&quot;);
        thread1.stop();
        thread1.join();
        thread2.join();
    }
    private static class MyThread extends Thread{
        public void run() {
            fun1();
        }
    }
    private static synchronized void fun1(){
        System.out.println(nowTime() + Thread.currentThread().getName() + &quot; start&quot;);
        sleep(30);
        System.out.println(nowTime() + Thread.currentThread().getName() + &quot; end&quot;);
    }
    private static void sleep(long second){
        try {
            TimeUnit.SECONDS.sleep(second);
        } catch (InterruptedException e) {
            Thread.currentThread().interrupt();
        }
    }

    private static String nowTime(){
        return new SimpleDateFormat(&quot;yyyy&#47;MM&#47;dd HH:mm:ss&quot;).format(new Date()) + &quot; &quot;;
    }
}
测试1结果：
2020&#47;07&#47;07 13:28:28 thread1 start
2020&#47;07&#47;07 13:28:34  stop thread1
2020&#47;07&#47;07 13:28:34 thread2 start
2020&#47;07&#47;07 13:29:04 thread2 end

测试2：测试lock
public class TestStopLock {
    &#47;&#47;main方法和其他方法省略，和TestStopSynchronized中代码一样
    private static Lock lock = new ReentrantLock();
    private static void fun1(){
        lock.lock();
        try {
            System.out.println(nowTime() + Thread.currentThread().getName() + &quot; start&quot;);
            sleep(30);
            System.out.println(nowTime() + Thread.currentThread().getName() + &quot; end&quot;);
        }finally {
            lock.unlock();
        }
    }
}

测试结果：

2020&#47;07&#47;07 13:27:20 thread1 start
2020&#47;07&#47;07 13:27:26  stop thread1
2020&#47;07&#47;07 13:27:26 thread2 start
2020&#47;07&#47;07 13:27:56 thread2 end</div>2020-07-07</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTJUhJakYu4BI7eFnheKDdibDjZqz32ia2rhN0Jz5YoR1ZRlDrLcFNr4MJnPg3WiaxaocWotOANeqsBibw/132" width="30px"><span>小白</span> 👍（2） 💬（1）<div>stop之后可以释放锁吧。。。</div>2019-09-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/66/75/54bb858e.jpg" width="30px"><span>life is short, enjoy more.</span> 👍（2） 💬（1）<div>老师，请问思考题中，为什么抛异常就会重置标识呢？</div>2019-03-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/ef/5e/381d043b.jpg" width="30px"><span>Lorne.Z</span> 👍（2） 💬（1）<div>老师，这样是不是也可以，在异常里加一个break
Thread thread = Thread.currentThread();
        while (true) {
            if (thread.isInterrupted()) {
                break;
            }
            try {
                Thread.sleep(100);
            } catch (InterruptedException e) {
                e.printStackTrace();
                break;
            }
        }</div>2019-03-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/e2/58/2468a5e9.jpg" width="30px"><span>JGOS</span> 👍（2） 💬（2）<div>老师，问下Java调用阻塞API时，Javav层面是runnable，那仍然占用CPU？</div>2019-03-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/19/29/a1/41607383.jpg" width="30px"><span>hello</span> 👍（1） 💬（1）<div>文中说“RUNNABLE 与 BLOCKED 的状态转换只有一种场景会触发这种转换，就是线程等待 synchronized 的隐式锁。”
lock 也可以达到synchronized 相同的目的呀，虽然lock 是并发包里面的，但也是java 的呀。但为什么文中说只有synchronized 这一种情况呢？</div>2021-10-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/02/7f/ddf56ac5.jpg" width="30px"><span>runzhliu</span> 👍（1） 💬（1）<div>这篇是真的非常经典，而且就在app上，随便一翻就能查阅！</div>2019-09-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/e2/58/2468a5e9.jpg" width="30px"><span>JGOS</span> 👍（1） 💬（1）<div>老师，调用阻塞API时Java层面是runnable状态，那他是ready状态还是running状态，占用CPU吗？</div>2019-03-21</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTJ5ricEp2SDpA2d2iaw6TOVaPfmeicDicP34bamibX1JbHEkJl8wDQOK3ia4vic9WacKjFia9wibeG3nwOIiafA/132" width="30px"><span>hunter</span> 👍（0） 💬（1）<div>请问休眠状态可以直接到终止状态吗？</div>2021-12-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/79/69/5960a2af.jpg" width="30px"><span>王智</span> 👍（0） 💬（1）<div>获得 synchronized 隐式锁的线程，调用带超时参数的 Object.wait(long timeout) 方法； 中如何获取隐式锁的线程呢？使用Thread.currentThread()获取吗？这个隐式锁也是没有办法指定唤醒的，是吗？</div>2021-05-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/a6/56/abb7bfe3.jpg" width="30px"><span>云韵</span> 👍（0） 💬（1）<div>“而 JVM 层面不关心这两个状态，因为 JVM 把线程调度交给操作系统处理了” 操作系统是怎么判断JVM的这两个状态呢？麻烦王老师解答一下</div>2020-04-08</li><br/>
</ul>