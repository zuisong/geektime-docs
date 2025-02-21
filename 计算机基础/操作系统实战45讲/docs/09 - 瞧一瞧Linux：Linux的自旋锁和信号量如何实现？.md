你好，我是LMOS。

上节课，我们学习了解决数据同步问题的思路与方法。Linux作为成熟的操作系统内核，当然也有很多数据同步的机制，它也有原子变量、开启和关闭中断、自旋锁、信号量。

那今天我们就来探讨一下这些机制在Linux中的实现。看看Linux的实现和前面我们自己的实现有什么区别，以及Linux为什么要这么实现，这么实现背后的机理是什么。

## Linux的原子变量

首先，我们一起来看看Linux下的原子变量的实现，在Linux中，有许多共享的资源可能只是一个简单的整型数值。

例如在文件描述符中，需要包含一个简单的计数器。这个计数器表示有多少个应用程序打开了文件。在文件系统的open函数中，将这个计数器变量加1；在close函数中，将这个计数器变量减1。

如果单个进程执行打开和关闭操作，那么这个计数器变量不会出现问题，但是Linux是支持多进程的系统，如果有多个进程同时打开或者关闭文件，那么就可能导致这个计数器变量多加或者少加，出现错误。

为了避免这个问题，Linux提供了**一个原子类型变量atomic\_t**。该变量的定义如下。

```
typedef struct {
    int counter;
} atomic_t;//常用的32位的原子变量类型
#ifdef CONFIG_64BIT
typedef struct {
    s64 counter;
} atomic64_t;//64位的原子变量类型
#endif
```

上述代码自然不能用普通的代码去读写加减，而是要用Linux专门提供的接口函数去操作，否则就不能保证原子性了，代码如下。
<div><strong>精选留言（30）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/16/5f/09/2ec44412.jpg" width="30px"><span>Qfeng</span> 👍（10） 💬（2）<div>回答思考题：Linux 的读写锁，因为每次读锁加锁计数-1，所以最多支持0x01000000个进程并发读取共享数据。
这样的读写锁的不足：读或者写锁拿不到时忙等，可以优化成trylock，拿不到可以先干其他的，等一段时间再尝试拿锁。（不知道回答的对不对）

感悟：不论是单值信号量还是多值信号量，亦或是原始自旋锁、trylock版本自旋锁还是读写锁，各种机制的设计和优化都是为了资源（CPU等）的更合理更高效的使用而优化。互斥机制有很多，理解每种锁机制重要，但是理解我们的业务更重要，这样才能因地制宜选择合适的锁。

老师简明扼要，点到即止的文风太赞了，谢谢。</div>2022-03-29</li><br/><li><img src="" width="30px"><span>springXu</span> 👍（20） 💬（4）<div>同步与锁
操作系统是让应用程序认为当前有超大的内存空间和强大的cpu来工作的硬件环境，但其实硬件没有这么强大。那如何解决呢？比如在单核cpu上可以用分时技术，让进程交替执行。对于一个进程来说，我们可以把一个进程变成了多个线程来执行。但这样就产生了同一个资源可以是内存的某一具体地址，可以是鼠标可以是磁盘上的某一文件被多个线程访问和修改的问题。这两节课提供了解决思路，一个是cosmos操作系统的方案，一个是linux的方案。
1.原子性。就是硬件执行指令时不被打断。对于x86是复杂指令集。一条指令可以做读修改内存值的操作，指令集中直接支持锁定操作。对于精简指令集，就相对麻烦些，硬件会提供bitband的操作。
2.中断控制是在执行时，防止中断信号突然来了把当前执行的过程打断了。 解决方法就是关闭中断。让中断信号等到可以通知时，才发起通知。
3.自旋锁。在多核的cpu环境下，当前核心的cpu要访问的资源是有可能被其他核的cpu来访问的。如果产生这种情况，那就让其他核的cpu自己执行空转。一直到当前核心的cpu把访问资源让出后，其他核的cpu通过检测到了可以访问资源，不在空转执行相关操作恢复正常运行。而这个过程就是自旋锁。这里会有一点浪费cpu的运行效率。毕竟有个cpu在空转。当空转时间过长时，浪费的效能更大。我们需要更好的利用cpu核的方式来解决这个问题。那就是互斥。
4.信号量
对于单一资源的信号量也可以说是互斥锁。  互斥锁和自旋锁的区别就是原来那个空转的核不再空转，而是把当前运行的线程或者进程睡眠去执行其他的线程或者进程了。  当资源被适当后，去通知睡眠线程或者进程。这就是信号量。linux下新版本的信号量在被移除。</div>2021-05-30</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/4f/b2/1e8b5616.jpg" width="30px"><span>老男孩</span> 👍（34） 💬（4）<div>这个排队自旋锁的实现方式感觉很风骚啊。关于读锁最大支持进程数是0x01000000（学友们都已经解答了）关于写饥饿的问题，既然写锁和读锁在同时获取锁状态时候写锁优先，那么就应该对读锁做一个限制，不能让读锁朝着最大数奔去。比如，系统检测到有写锁在等待，那么就限制新的读锁加入，等已经存在的读锁都释放了，写锁马上加锁更新资源。然后等待的读锁再开始加锁读取。这个等待的队列要分为读锁队列和写锁队列。优先处理写锁队列，在没有写锁的时候才能继续加读锁，如果有写锁等待，那么新的读锁不管超没超出那个最大数，都要进入读锁队列等待写锁完成后再开始自己的表演。</div>2021-05-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/52/40/e57a736e.jpg" width="30px"><span>pedro</span> 👍（29） 💬（2）<div>以后我就是第一东吹了😁！
像这样的清晰明了，言简意赅的Linux内核源码解读实在是太少了，这样的文章读起来实在是太爽了，强烈小编安排一下东哥的下一个专栏叫做 《纵览Linux源码，小白也能学透》。

对于思考题答案，读并发进程的最大个数就是0x01000000，只要lock大于0都是可以共享数据的。
至于读写锁的不足，我个人觉得最不友好的点在于读写互斥上，由于读锁对写锁是互斥的，如果一直有人读，那么计数器一直小于0x01000000，加写锁时也一直小于0，写锁一直也不会成功，会陷入长时间的写饥饿状态，并且一直自旋，浪费CPU资源。
所以改进点就在于，给写进程配上一个休眠队列，待加锁失败进入队列休眠等待，待解读锁时判断计数器，决定是否唤醒队列中的写进程。
当然还有很多其它的优化点，欢迎大家集思广益~</div>2021-05-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/3e/e7/261711a5.jpg" width="30px"><span>blentle</span> 👍（15） 💬（1）<div>回答一下思考题
1.理论上可以支持x01000000这么多进程，但实际上受限于文件句炳也就是文件描述符的限制，还有考虑多个线程的问题等等，注定最终远远小于这个值
2.读写锁造成写饥饿的情况是不是可以参考jdk的读写锁的实现，在条件等待队列中判断队列第一个元素是不是一个写进程，如果是写进程，让其直接优先获取锁.</div>2021-05-28</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/sOuSC65kXWdWBAIIs6uXAD41Ed8Wo8tib81LLVOQJ2oK23TgPDy6x0PGmp7rXwLR3BHOicaKx1zib1DyfpCITK3dw/132" width="30px"><span>GeekYanger</span> 👍（6） 💬（3）<div>文中：
“&#47;&#47;Linux没有这样的结构，这只是为了描述方便
typedef struct raw_spinlock
{ 
        union 
                { 
                        unsigned int slock;&#47;&#47;真正的锁值变量 
                        u16 owner; 
                        u16 next; 
                }
}raw_spinlock_t;”
这里老师为了帮助我们理解汇编代码构造了一个这样的结构体，我觉得，这个owner和next要被包在一个struct中才是老师想要表述的意思，不然owner和next的取值是一样的，都是低16位。</div>2021-12-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/4f/9d/72461b25.jpg" width="30px"><span>子青</span> 👍（4） 💬（2）<div>老师，我有两个问题想请教
1 。Linux自旋锁，如果一个进程在获取锁之后挂了怎么办，没人给owner +1了，后面排队的进程岂不是永远等不到锁释放？
2。信号量那里，down是在链表的头部插入，up是唤醒链表的头部，这样不会有饥饿问题吗，链表后面的可能永远拿不到资源？</div>2021-09-23</li><br/><li><img src="" width="30px"><span>3k</span> 👍（4） 💬（1）<div>为什么这节里实现自旋锁的时候都没有关中断了呢？</div>2021-06-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/50/d5/73334a95.jpg" width="30px"><span>doos</span> 👍（3） 💬（1）<div>感觉不学习汇编和c很多都看不懂</div>2022-04-21</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/vQiadbkZYR239J80hjekw7jzY9vy6otLKPNDSuz2lruDiaXlKGkcsX5wwiaFevicgqV8odlRG4UITiadDF3fgicrHPcw/132" width="30px"><span>疯码</span> 👍（3） 💬（1）<div>请问下为什么保存和恢复eflags那段代码用push pop而不是mov呢</div>2022-01-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/27/ef/18/6a620733.jpg" width="30px"><span>kocgockohgoh王裒</span> 👍（3） 💬（1）<div>关于小弟问的那个关于排队自旋锁的问题，好像是因为gcc汇编的源 目的和intel手册上的顺序是反的。关于 xaddl，intel手册上说源是寄存器，目的是寄存器或内存。而slock是内存，不可能是源。所以小弟觉得源是%0  inc，目的是%1 slock, 所以xaddl相当于 temp = inc + slock,  inc = slock,  slock = slock + inc。 否则的话，每次调用slock都会被设成inc的初值0001000，不合理。不知道彭东大神觉得如何</div>2021-11-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1a/46/27/eb318d12.jpg" width="30px"><span>Geek_4b6813</span> 👍（3） 💬（1）<div>最多支持同时有2^24个进程共享读锁(计算机常驻的进程基本上是不可能达到这个数的)
存在的问题，写饥饿，只要有读进程存在，写进程就永远没机会获得锁。</div>2021-07-06</li><br/><li><img src="" width="30px"><span>K菌无惨</span> 👍（3） 💬（1）<div>请问“_cond_lock 只用代码静态检查工作”这句话时什么意思？</div>2021-06-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/28/60/81/38b00111.jpg" width="30px"><span>Feen</span> 👍（2） 💬（1）<div>到第9课的时候，发现留言的数量少了很多，感觉操作系统（或者计算机原理）的淘汰率真的很高，能出师的太少了。关于最后的问题，应该说读锁最大支持的进程数是0x01000000，写锁最大的进程数人为的设置为1。写锁也可以设置为0x01000000，因为对于计算机来说，到底有多少进程写对它来说无关，数据对计算机没有意义，数据只对于人能不能正确使用有关。所以才有上写锁的时候直接减去0x01000000这个初始值，目的是控制只有一个进程可以写，而不是为了1而设置1。不管是中断，信号量，各种锁，最后都要靠CPU硬件的集成指令支持才能完成，就是原子操作，计算机上的各种软件，应用，服务都是靠原子操作完成自己的事务，手段就是在操作的时候不受打断，目的是完成一件事。怎么样能玩好原子操作，就能出师了。哈哈</div>2021-06-17</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTJWFdKjyLOXtCzowmdCUFHezNlnux4NPWmYsqETjiaHNbnmb7xdzibDncZqP06nNbpN4AhmD76cpicfw/132" width="30px"><span>fhs</span> 👍（2） 💬（2）<div>读写锁部分中。假设t1时候1号写线程获取到了锁且不释放：lock=0，t2时刻2号写线程尝试获取：lock=-(0x0100 0000)，t3时刻1号读尝试获取：lock=-(0x0100 0001)。
之后1号写即便释放了锁，此时lock = -1。但是2号写的比较成功的条件是：&quot;lock+0x01000000，直到结果的值等于 0x01000000&quot;。1号读的比较条件是&quot;循环测试 lock+1 的值，直到结果的值大于等于 1&quot;。
即在1号写释放之后，2号写和1号读因为lock是-1永远达不到各自退出循环的条件，一直在自旋？</div>2021-05-30</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTIBV8Deuz0Ys4omVlErUvTeRLt7xYRPd8nxhSZ1C2Q9Nice7icHnndsHmyT3KBenxLGw7xghlDzfIuA/132" width="30px"><span>LT</span> 👍（1） 💬（2）<div>static inline int __raw_spin_trylock(raw_spinlock_t*lock){    int tmp;    int new;    asm volatile(    &quot;movl %2,%0\n\t&quot;&#47;&#47;tmp=slock    &quot;movl %0,%1\n\t&quot;&#47;&#47;new=tmp    &quot;roll $16, %0\n\t&quot;&#47;&#47;tmp循环左移16位，即next和owner交换了    &quot;cmpl %0,%1\n\t&quot;&#47;&#47;比较tmp和new即（owner、next）？=（next、owner）    &quot;jne 1f\n\t&quot; &#47;&#47;不等则跳转到标号1处     &quot;addl $0x00010000, %1\n\t&quot;&#47;&#47;相当于next+1    &quot;lock ; cmpxchgl %1,%2\n\t&quot;&#47;&#47;new和slock交换比较        &quot;1:&quot;    &quot;sete %b1\n\t&quot; &#47;&#47;new = eflags.ZF位，ZF取决于前面的判断是否相等    &quot;movzbl %b1,%0\n\t&quot; &#47;&#47;tmp = new    :&quot;=&amp;a&quot;(tmp),&quot;=Q&quot;(new),&quot;+m&quot;(lock-&gt;slock)    ::&quot;memory&quot;,&quot;cc&quot;);    return tmp;}

这段代码我看懂了，但是在linux代码树中我没有找到，甚至是用grep.
我看linux代码经常会有这种情况，找不到相关的ASM代码的实现。LMOS，这段代码在那个文件中？

建议以后相关代码，标注下linux下的文件路径。</div>2021-06-06</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1a/11/7c/bf5049b3.jpg" width="30px"><span>Freddy</span> 👍（1） 💬（1）<div>Linux的读写锁支持0x01000000 = 16777216个进程并发读取共享数据；
Linux的读写锁本质上是自旋锁，进程没有成功获取到读锁或者写锁时，会进行自旋，浪费了CPU资源；</div>2021-06-01</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/27/ea/dc/aa699264.jpg" width="30px"><span>宏典</span> 👍（1） 💬（1）<div>重新定义一个代码段，避免后面的代码填充cache。因为大部分加锁都是成功的。
这个可以理解。
但是为何重新重新定义一个代码段，就可以保证后面的代码不填充cache?</div>2021-05-31</li><br/><li><img src="" width="30px"><span>Paul Shan</span> 👍（1） 💬（1）<div>请问老师，四种解决并发的方法中里是不是只有关中断是只和CPU的状态有关，也就是关闭了CPU接受中断调用的服务，其他的原子操作，自旋锁，信号量都需要内存和CPU各自的原子操作来配合？</div>2021-05-30</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTJWFdKjyLOXtCzowmdCUFHezNlnux4NPWmYsqETjiaHNbnmb7xdzibDncZqP06nNbpN4AhmD76cpicfw/132" width="30px"><span>fhs</span> 👍（1） 💬（7）<div>请问下，Linux的读写锁实现中，写锁每次获取的时候都减0x0100 0000，那么如果有超过128个线程同时写，不是就可能会溢出么？即这个实现中最多只能支持128个写线程？</div>2021-05-29</li><br/><li><img src="" width="30px"><span>Paul Shan</span> 👍（1） 💬（1）<div>请问老师，原子变量的本质是不是只是对寄存器和内存操作，跳过了其他所有中间缓存，是一种用速度换一致性的方法？</div>2021-05-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/27/d5/be/183c222b.jpg" width="30px"><span>陈超</span> 👍（1） 💬（1）<div>我认为，支持并发读的数量是0x01000000,支持并行读的数量是cpu核心的数量；而不足之处就在于忙等浪费cpu时间了。读的时候可以让写的进程让出cpu休眠吗？期望老师高见！</div>2021-05-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/18/39/d2/845c0e39.jpg" width="30px"><span>送过快递的码农</span> 👍（1） 💬（2）<div>说下自己对锁底层的理机，锁是依赖硬件提供的原子指令来执行的。普通互斥锁是lock值1 获取锁则对该值进行原子减，如果这个值本身就小于1，那说明被锁住了。。。独写锁的区别是他是0x01000000的值，读锁减1，写锁减0x01000000，读锁可以被0x01000000共享，写锁是互斥的只能被减一次。。。 突然感觉原子操作是计算机最底层的功能，以前在Java碰到这个问题就范懵，就是自己对底层理解太少导致的，无论是应用层的并发包，还是操作系统内核层，对原子操作都是非常依赖。。。</div>2021-05-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/21/7e/fb725950.jpg" width="30px"><span>罗 乾 林</span> 👍（1） 💬（6）<div> Linux的读写锁，我的看法正好相反，写会造成读饥饿，一直有写入时读进程将会饥饿</div>2021-05-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/3e/e7/261711a5.jpg" width="30px"><span>blentle</span> 👍（1） 💬（4）<div>还请教老师和各位童鞋一个问题，看着内核里各种锁实现函数里的汇编代码头大，这个是看到什么指令去查一遍还是先系统的学习遍，本人学习过一遍王爽的x86汇编，这里看着陌生的指令还是头大</div>2021-05-28</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/XeGpHsAib2ZBic8PsR7z18plF2AccJ6Op5WmRDnv4Y9Vkmdiba9ibbcQSPGLJ1yuACAhkLQVQZHSz9WUcNj7UKSw6Q/132" width="30px"><span>Geek_ba3598</span> 👍（0） 💬（2）<div>自旋锁在哪个头文件中啊？linux&#47;spin_lock.h里吗？但是include根本找不到这个头文件。</div>2022-08-16</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/17/06/7e/735968e2.jpg" width="30px"><span>西门吹牛</span> 👍（0） 💬（1）<div>Java 中的 aqs 和 linux 的排队自旋锁，异曲同工。aqs 用队列的数据结构维护了公平性，而 linux 只用 next 和 owner 维护了抢占的顺序性。</div>2022-07-06</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/17/87/db/c132ef37.jpg" width="30px"><span>花树</span> 👍（0） 💬（3）<div>读写锁那里提到写会优先得到锁，代码里没看到，是怎么实现的呀</div>2022-05-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/17/87/db/c132ef37.jpg" width="30px"><span>花树</span> 👍（0） 💬（1）<div>开始锁值变量为 1 时，执行 decb 指令就变成了 0，0 就表示加锁成功。如果小于 0，则表示有其它进程已经加锁了，就会导致循环比较。

这里加锁成功值就为0了，其他进程获取值不应该是0吗？为什么是小于零</div>2022-05-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/25/56/86/db4c0d1c.jpg" width="30px"><span>ljx</span> 👍（0） 💬（1）<div>老师，读写锁的代码没看出来为什么竞争时写锁会优先获得。能解释一下吗？</div>2022-04-23</li><br/>
</ul>