你好，我是吴咏炜。

上一讲我们讨论了一些并发编程的基本概念，今天我们来讨论一个略有点绕的问题，C++ 里的内存模型和原子量。

## C++98 的执行顺序问题

C++98 的年代里，开发者们已经了解了线程的概念，但 C++ 的标准里则完全没有提到线程。从实践上，估计大家觉得不提线程，C++ 也一样能实现多线程的应用程序吧。不过，很多聪明人都忽略了，下面的事实可能会产生不符合直觉预期的结果：

- 为了优化的必要，编译器是可以调整代码的执行顺序的。唯一的要求是，程序的“可观测”外部行为是一致的。
- 处理器也会对代码的执行顺序进行调整（所谓的 CPU 乱序执行）。在单处理器的情况下，这种乱序无法被程序观察到；但在多处理器的情况下，在另外一个处理器上运行的另一个线程就可能会察觉到这种不同顺序的后果了。

对于上面的后一点，大部分开发者并没有意识到。原因有好几个方面：

- 多处理器的系统在那时还不常见
- 主流的 x86 体系架构仍保持着较严格的内存访问顺序
- 只有在数据竞争（data race）激烈的情况下才能看到“意外”的后果

举一个例子，假设我们有两个全局变量：

```c++
int x = 0;
int y = 0;
```

然后我们在一个线程里执行：

```c++
x = 1;
y = 2;
```

在另一个线程里执行：

```c++
if (y == 2) {
  x = 3;
  y = 4;
}
```
<div><strong>精选留言（27）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/16/bc/25/1c92a90c.jpg" width="30px"><span>tt</span> 👍（25） 💬（1）<div>感觉这里的无锁操作就像分布式系统里面谈到的乐观锁，普通的互斥量就像悲观锁。只是CPU级的乐观锁由CPU提供指令集级别的支持。

内存重排会引起内存数据的不一致性，尤其是在多CPU的系统里。这又让我想起分布式系统里讲的CAP理论。

多线程就像分布式系统里的多个节点，每个CPU对自己缓存的写操作在CPU同步之前就造成了主内存中数据的值在每个CPU缓存中的不一致，相当于分布式系统中的分区。

我大概看了参考文献一眼，因为一级缓存相对主内存速度有数量级上的优势，所以各个缓存选择的策略相当于分布式系统中的可用性，即保留了AP（分区容错性与可用性，放弃数据的一致性），然后在涉及到缓存数据一致性问题上，相当于采取了最终一致性。

其实我觉得不论是什么系统，时间颗足够小的话，都会存在数据的不一致，只是CPU的速度太快了，所以看起来都是最终一致性。在保证可用性的时候，整个程序的某个变量或内存中的值看起来就是进行了重排。

分布式系统中将多个节点解耦的方式是用异步、用对列。生产者把变化事件写到对列里就返回，然后由消费者取出来异步的实施这些操作，达到数据的最终一致性。

看资料里，多CPU同步时，也有在CPU之间引入对列。当需要“释放前对内存的修改都在另一个线程的获取操作后可见”时，我的理解就是用了所谓的“内存屏障”强制让消费者消费完对列里的&quot;CPU级的事物&quot;。所以才会在达到严格内存序的过程中降低了程序的性能。

也许，这个和操作系统在调度线程时，过多的上下文切换会导致系统性能降低有关系。</div>2020-01-10</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/aFAYPyw7ywC1xE9h1qibnTBwtWn2ClJqlicy5cMomhZVaruMyqSq76wMkS279mUaGhrLGwWo9ZnW0WCWfmMovlXw/132" width="30px"><span>木瓜777</span> 👍（8） 💬（1）<div>您好，看了这篇后，对互斥量和原子量的使用 有些不明白，什么时候应该用互斥量，什么时候用原子量，什么时候一起使用？</div>2020-01-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/af/a6/3f15ba2f.jpg" width="30px"><span>czh</span> 👍（4） 💬（2）<div>专栏里面的评论都满地是宝，这就是比啃书本强太多的地方，大家可以讨论请教。文章需要复习，评论也同样需要复习，看看是否有了新的想法💡。

在阅读的时候，我心里也有前面几个读者的关于锁、互斥量、原子操作的区别与联系的疑问🤔️。

我尝试说一下我的理解：站在需求的角度
1.对单独没有逻辑联系的变量，直接使用原子量的relaxed就够了，没必要加上内存序
2.对于有联系的多个多线程中的变量，这时就需要考虑使用原子量的内存序
3.对于代码段的保护，由于原子量没有阻塞，所以必须使用互斥量和锁来解决
ps：互斥量+锁的操作   可取代  原子量。反之不可。

另外，还产生新的疑问：
1.互斥量的定义中，一个互斥量只允许在多线程中加一把锁，那么是否可以说互斥量只有和锁配合达到保护代码段的作用，互斥量还有其他单独的用法吗？
2.更近一步，原子量+锁，是否可以完成对代码段的保护？而吴老师也在评论区里提到：锁是由原子量构成的。

望老师解答，纠正。</div>2020-02-05</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/8c/df/77acb793.jpg" width="30px"><span>禾桃</span> 👍（4） 💬（4）<div>和大家分享一个链接


操作系统中锁的实现原理


https:&#47;&#47;mp.weixin.qq.com&#47;s&#47;6MRi_UEcMybKn4YXi6qWng</div>2020-01-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/44/54/7e40e592.jpg" width="30px"><span>prowu</span> 👍（4） 💬（1）<div>吴老师，您好！有两个问题请帮忙解答下：
1、在解释相关memory_order_acquire, memory_order_release等时，都有提到“当前线程可见”，这个“可见”该怎么理解？
2、可以帮忙总结下，在什么场景下需要保证内存序，比如：满足了以下条件，就需要考虑是否保证内存序了：
（1）多线程环境下
（2）存在多个变量是可多个线程共享的，比如：类成员变量、全局变量
（3）这多个共享变量在实现逻辑上存在相互依赖的关系
（4）...

谢谢！</div>2020-01-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/f7/67/4997eebf.jpg" width="30px"><span>Counting stars</span> 👍（2） 💬（2）<div>链接[2]的代码在msvc编译器release模式下用atomic int测试了一下，X Y通过 store的指定memory_order_release并没有达到期望的内存屏障效果，仍然出现了写读序列变成读写序列的问题，仔细分析了一下：
memory_order_release在x86&#47;64上看源码有一个提示，
case memory_order_release:
            _Compiler_or_memory_barrier();
            _ISO_VOLATILE_STORE32(_Storage, _As_bytes);
            return;
查看了一下具体定义
#elif defined(_M_IX86) || defined(_M_X64)
&#47;&#47; x86&#47;x64 hardware only emits memory barriers inside _Interlocked intrinsics
#define _Compiler_or_memory_barrier() _Compiler_barrier()
看起来msvc的做法，并没有针对memory_order_release实现标准的内存屏障支持
参考老师提供示例连接中的例子MemoryBarrier()是可以手动效果实现这一个效果
最终结论如下：
msvc2019下，memory_order_release并不能保证内存屏障效果，只能通过默认的memory_order_seq_cst来保证
老师可以和您交流一下我的观点吗</div>2021-05-16</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/35/4e/d4f70f29.jpg" width="30px"><span>fengbeihong</span> 👍（1） 💬（1）<div>老师请教下单例的实现：
一种是利用static变量的初始化：
Foo&amp; getInst()
{
    static Foo inst(...);
    return inst;
}

一种是利用pthread_once来保证线程安全

这两种方式是否可行呢，应该可以简化单例模式的代码实现吧</div>2023-11-06</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/30/db/86/51ec4c41.jpg" width="30px"><span>李云龙</span> 👍（1） 💬（1）<div>老师，单例类的加锁过程如果用读取-修改-写入的方式，比如compare_exchange_strong，也是可以的吗？我觉得这种方式写起来会更简单。</div>2023-10-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/0e/b6/37b19725.jpg" width="30px"><span>王大为</span> 👍（1） 💬（1）<div>y.store(4, memory_order_relaxed);
应该是released吧？某段代码第4行</div>2020-09-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/8c/df/77acb793.jpg" width="30px"><span>禾桃</span> 👍（1） 💬（3）<div>is_lock_free，判断对原子对象的操作是否无锁（是否可以用处理器的指令直接完成原子操作）

#1
这里的处理器的指令指的是，
“lock cmpxchg”?

#2
“是否可以用处理器的指令直接完成原子操作”, 这里的直接指的是仅使用“处理器的指令吗？

#3
能麻烦给个is_not_lock_free的对原子对象的操作的大概什么样子吗？

谢谢！</div>2020-01-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/c4/eb/2285a345.jpg" width="30px"><span>花晨少年</span> 👍（1） 💬（3）<div>这一节讲的实在是太好了，我对前几节的编译器模版相关的不是很感冒，要是能把这期更深入的细节探讨一下，多做几节，就更好了。

singleton* singleton::instance()
{
  @a
  if (inst_ptr_ == nullptr) {&#47;&#47;@1
    @b
    lock_guard lock;  &#47;&#47;  加锁
    if (inst_ptr_ == nullptr) {
	@c
      inst_ptr_ = new singleton();&#47;&#47;@2
        @d
    }
  }
  return inst_ptr_;
}

有个问题，就是对double check那个例子的疑惑，会出现什么问题？
inst_ptr_应该就两种状态，null和非null。
如果线程1在@b处，等待锁，这个时候线程2不管在@c或者@d处，线程a获得锁的时候，都不会进入@c，因为inst_ptr已经非空。
如果线程1在@a处，线程2在@2处，执行new操作，难道@2这个语句有什么问题吗，难道@2不是一个原子操作，会导致线程1已经得到线程2分配的对象地址，而内存还没有准备好吗？如果是这种情况的话，
那么下面加入了原子操作后，也没有解决new问题啊，

singleton* singleton::instance()
{
  singleton* ptr = inst_ptr_.load(
    memory_order_acquire);
  if (ptr == nullptr) {
    lock_guard&lt;mutex&gt; guard{lock_};
    ptr = inst_ptr_.load(
      memory_order_relaxed);
    if (ptr == nullptr) {
      ptr = new singleton();
      inst_ptr_.store(
        ptr, memory_order_release);
    }
  }
  return inst_ptr_;
}</div>2020-01-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/8c/df/77acb793.jpg" width="30px"><span>禾桃</span> 👍（1） 💬（1）<div>Preshing 

“In particular, each processor is allowed to delay the effect of a store past any load from a different location. “

这里的”delay”指的是1已经被写到X_cpu_cache, 但是还没有没到推送到X_memeory?

#1
X = 1;
asm volatile(&quot;&quot; ::: &quot;memory&quot;);  &#47;&#47; Prevent memory reordering
r1 = Y;

上面的代码,能确保cpu会先执行store,（至少先写到X_cpu_cache,无法保证1被推送到X_memory)，然后再read?


#2
X = 1;
asm volatile(&quot;mfence&quot; ::: &quot;memory&quot;); 
r1 = Y;

上面的代码,能确保cpu会先执行store（包括把1写到X_cpu_cache，再推送至X_memoery), 然后再read?

上面的代码，cpu 执行到mfence时，会确保1从X_cpu_cache推送到X_memory, 然后再去读Y?

谢谢！</div>2020-01-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/29/6a/0d/38607302.jpg" width="30px"><span>少年</span> 👍（0） 💬（1）<div>由于 volatile 不能在多处理器的环境下确保多个线程能看到同样顺序的数据变化，在今天的通用应用程序中，不应该再看到 volatile 的出现。
这句话并不是太理解，想问下:如果只有一个线程修改某一变量，其他线程对此变量只读，那么是否应该用volatile?或者不用volatile也可?</div>2024-12-16</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/22/9c/73/b4e064d4.jpg" width="30px"><span>nxt</span> 👍（0） 💬（1）<div>老师您好，有两个线程T1和T2，分别执行如下代码的话，有可能会print出“bug”么。
主要是想问“T1读到x的旧值，memory_order_seq_cst语义” 是否happen before于“T2修改x为新值，memory_order_seq_cst语义”
int x=0;
int y=0;
int z=0;

T1:
y=1;
if( load(x, memory_order_seq_cst) == 0 ) z=1;
else y=0;

T2: 
if( CAS(x, 0, 1, memory_order_seq_cst, memory_order_seq_cst) )
{
   if( z==1&amp;&amp;y==0 )
   {
      printf(&quot;bug&quot;);
   }
}</div>2023-11-02</li><br/><li><img src="" width="30px"><span>Geek_26c53e</span> 👍（0） 💬（2）<div>请教一下，如果在获取锁之前，别的线程对inst_ptr_进行了store，那加锁之后走到load时，由于是松散的load，会不会读取到旧的inst_ptr_（null）啊？

&#47;&#47; 头文件
class singleton {
public:
  static singleton* instance();
  …
private:
  static singleton* inst_ptr_;
};

&#47;&#47; 实现文件
singleton* singleton::inst_ptr_ =
  nullptr;

singleton* singleton::instance()
{
  if (inst_ptr_ == nullptr) {
    lock_guard lock;  &#47;&#47; 加锁
    if (inst_ptr_ == nullptr) {
      inst_ptr_ = new singleton();
    }
  }
  return inst_ptr_;
}</div>2023-09-05</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/43/61/eeefa369.jpg" width="30px"><span>tony</span> 👍（0） 💬（1）<div>老师，被mutex保护的全局变量是否有使用原子变量的必要？
举例如下：
int global_var1_;
mutex.lock();
global_var1_ = 2;
mutex.unlock();
假设有两个核cpu1, cpu2, 变量global_var1_在cpu2 cache中，线程A 在cpu1上访问该代码块赋值变量为2，该代码赋值时只是写入到cpu1的store buffer中，还没有更新到cpu2的缓存就返回；此时线程B在cpu2上被调度，执行同样代码块，读取到的变量值是否可能不等于2？
个人认为应该等于2，理由如下：
a. 线程B在cpu2上被调度执行需要等待的时间要远大于从cpu1 cache中同步到cpu2 cache的时间；
b. unlock中可能有内存屏障指令，确保数据同步以后才返回（还需再确认一下）；
请斧正，谢谢。</div>2023-03-04</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTKtlEYuHnR8VdRkNPcmkIqTM9DKahpcpicDdBvcmBWMIAAhBrd0QNWvl09slqrzB5TibryVcIfPmb7Q/132" width="30px"><span>raisecomer</span> 👍（0） 💬（1）<div>关于单例的双检查锁定的例子，个人认为inst_ptr_.store还是应该使用release语义，虽然它确实在互斥量的保护范围内，互斥量只能保证它以及它前面的构造函数调用时对内存的写操作，都在互斥量释放锁之前完成。但是在第19行读取inst_ptr_时并没有互斥量的保护，既然不受保护，别的线程在此处是可以（不经过互斥量）直接读取它的，也就没有互斥量加锁时的acquire和在29行互斥量解锁时的release形成的release-acquire语义，而26、27行虽然都在互斥量的保护范围内，如果在27行使用relaxed语义，可能会造成26、27行乱序（不过，26、27不管谁先谁后，它们整体都在互斥量释放锁之前完成），造成原子量inst_ptr_虽然已经store了，但是构造函数没有完成（当然，不是表面上看到的c++语句，而是指汇编指令级上的写内存，可能优化后乱序），这样另一个线程在19行可能得到的是inst_ptr_已经不为nullptr了，但单例还未完全初始化的对象实例。
恰恰相反，可以在19行把内存序改为memory_order_relaxed，因为inst_ptr_原子量在此处并没有要保证其它内存读取数据的顺序要求，只要它不是nullptr，就能保证单例对象构造时的写内存操作已经完成，这是由28行的release内存序保证的。</div>2022-04-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/92/7c/12c571b6.jpg" width="30px"><span>Slience-0°C</span> 👍（0） 💬（1）<div>最开始的问题，对x,y加锁，不就能实现想要的结果了么？当然加锁肯定有损耗，内存模型，一直没有理解为了解决什么问题</div>2021-10-28</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/DYAIOgq83epWuRmpg9jWibtRH3mO9I0Sc9Y86fJpiaJDdLia39eib89R1raTkxMg9AOkjb0OTRkmXiaialJgHC5ve59g/132" width="30px"><span>Geek_64affe</span> 👍（0） 💬（1）<div>老师，有个疑问

1. if (y.load(memory_order_acquire) ==
    2) {
2.   x = 3;
3.   y.store(4, memory_order_relaxed);
4. }

如果其他线程在 第2行 或者 第3行期间 修改了 y 的值，逻辑不就出错了吗</div>2021-07-02</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/7a/83/b62508b4.jpg" width="30px"><span>Dooms</span> 👍（0） 💬（1）<div>#include &lt;thread&gt;
#include &lt;iostream&gt;
#include &lt;atomic&gt;

int x = 0;
std::atomic&lt;int&gt; y;

void a()
{
    x = 1;
    y.store(2, std::memory_order_release);
    &#47;&#47; 保证x = 1的写操作, 不会因为指令重排, 导致出现在y赋值的后执行. 
    x = 2;
    y.store(3, std::memory_order_release);
}

void b()
{
    &#47;&#47; 保证y读操作, 后续的读写操作都不会重排到这个指令之前.
    &#47;&#47; 并且线程a中y的释放(写入), 对内存的修改, 在b线程的获取(读取)操作是必定可见的, 
    &#47;&#47; 就是说a只要在执行y写入后, b线程执行到y读取的时候, 一定会读取到a线程写入的值.  当读取到 y = 2 的时候, x 的是 1 还是 2 呢? 
    if (y.load(std::memory_order_acquire) == 2)
    {
        printf(&quot;%d %d\n&quot;, x, y.load(std::memory_order_acquire)); &#47;&#47; 这里读取到的是 x = 2, y = 3 有没可能x = 2, y = 2 或者 x = 1, y = 2 ?? 还是说这个具体的值是不确定的 ??
        x = 3;
        y.store(4, std::memory_order_relaxed);
    }
}

int main()
{
    y = 0;
    std::thread t1(a);
    std::thread t2(b);
    t1.detach();
    t2.detach();
    std::this_thread::sleep_for(std::chrono::microseconds(1500));
    printf(&quot;%d %d\n&quot;, x, y.load(std::memory_order_acquire));
    return 0;
}

std::atomic 的实现原理是什么? 内存屏障指令吗?</div>2021-01-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/76/53/21d62a23.jpg" width="30px"><span>鲁·本</span> 👍（0） 💬（1）<div>#include &lt;thread&gt;
#include &lt;atomic&gt;
#include &lt;cassert&gt;
#include &lt;string&gt;
#include &lt;iostream&gt;
#include &lt;unistd.h&gt;

struct ServerT
{
    int id;
    int port;
};
typedef struct ServerT serverT;

std::atomic&lt;ServerT*&gt; ptr;

void set()
{
    ServerT* pS  = new serverT;

    ptr.store(pS, std::memory_order_release);
    std::cout &lt;&lt; std::this_thread::get_id() &lt;&lt; &quot; &quot; &lt;&lt;  __FUNCTION__ &lt;&lt; &quot; 1 port:&quot; &lt;&lt; pS-&gt;port &lt;&lt; std::endl;
    pS-&gt;port = 2345;
    std::cout &lt;&lt; std::this_thread::get_id() &lt;&lt; &quot; &quot; &lt;&lt;  __FUNCTION__ &lt;&lt; &quot; 2 port:&quot; &lt;&lt; pS-&gt;port &lt;&lt; std::endl;
}

void get()
{
    ServerT* pS = nullptr;
    while (!(pS = ptr.load(std::memory_order_acquire)));
    std::cout &lt;&lt; std::this_thread::get_id() &lt;&lt; &quot; &quot; &lt;&lt;  __FUNCTION__ &lt;&lt; &quot; 1 port:&quot; &lt;&lt; pS-&gt;port &lt;&lt; std::endl;
    pS-&gt;port = 4567;
    std::cout &lt;&lt; std::this_thread::get_id() &lt;&lt; &quot; &quot; &lt;&lt;  __FUNCTION__ &lt;&lt; &quot; 2 port:&quot; &lt;&lt; pS-&gt;port &lt;&lt; std::endl;
}

int main()
{
    std::thread t1(set);
    sleep(1);
    std::thread t2(get);
    sleep(2);
    std::thread t3(get);
    t1.join();
    t2.join();
    t3.join();
}

运行结果:

140388121650944 set 1 port:0
140388121650944 set 2 port:2345
140388111161088 get 1 port:2345
140388111161088 get 2 port:4567
140388100671232 get 1 port:4567
140388100671232 get 2 port:4567

老师,您看这个例子,load 取出的指针,直接修改指针指向的对象的内容,不调用store,其他线程也能看到修改的, 那么这种情况, 要怎么对原子对象进行原子修改呢? 难道要在修改的地方加上互斥锁?</div>2020-09-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/76/53/21d62a23.jpg" width="30px"><span>鲁·本</span> 👍（0） 💬（1）<div>老师load返回的指针是原始内存地址，还是副本地址？</div>2020-09-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/c4/eb/2285a345.jpg" width="30px"><span>花晨少年</span> 👍（0） 💬（3）<div>https:&#47;&#47;en.cppreference.com&#47;w&#47;cpp&#47;atomic&#47;memory_order最后一段讲解
memory_order_seq_cst提到，如果要保证最后的断言&quot;assert(z.load() != 0);&quot;不会发生，必须使用
memory_order_seq_cst，这里很不理解。
下面是代码

#include &lt;thread&gt;
#include &lt;atomic&gt;
#include &lt;cassert&gt;
 
std::atomic&lt;bool&gt; x = {false};
std::atomic&lt;bool&gt; y = {false};
std::atomic&lt;int&gt; z = {0};
 
void write_x()
{
    x.store(true, std::memory_order_seq_cst);
}
 
void write_y()
{
    y.store(true, std::memory_order_seq_cst);
}
 
void read_x_then_y()
{
    while (!x.load(std::memory_order_seq_cst))&#47;&#47;@1
        ;
    if (y.load(std::memory_order_seq_cst)) {&#47;&#47;@2
        ++z;
    }
}
 
void read_y_then_x()
{
    while (!y.load(std::memory_order_seq_cst))
        ;&#47;&#47;@3
    if (x.load(std::memory_order_seq_cst)) {&#47;&#47;@4
        ++z;
    }
}
 
int main()
{
    std::thread a(write_x);
    std::thread b(write_y);
    std::thread c(read_x_then_y);
    std::thread d(read_y_then_x);
    a.join(); b.join(); c.join(); d.join();
    assert(z.load() != 0);  &#47;&#47; will never happen
}

把代码全部改成memory_order_acq_rel操作为什么不可以?
按照memory_order_acq_rel的描述，在其他线程中,@2的所有操作应该都不会被重排到@1之前，
@4的操作也不会被重排到@3之前，
那如果是这样的话，也能确保断言永远不会发生。
</div>2020-01-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/8c/df/77acb793.jpg" width="30px"><span>禾桃</span> 👍（0） 💬（2）<div>
  void add_count() noexcept
  {
    count_.fetch_add(
      1, std::memory_order_relaxed);
  }

  void add_count() noexcept
  {
    count_.fetch_add(
      1, std::memory_order_seq_cst);
  }


std::memory_order_seq_cst 比std::memory_order_relaxed，
性能方面的浪费，具体指的是什么？

谢谢！</div>2020-01-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/c4/eb/2285a345.jpg" width="30px"><span>花晨少年</span> 👍（0） 💬（4）<div>介绍memory_order_seq_cst时，说这是所有原子操作的默认内存序，但是在文章前面又说 

y = 2 相当于 y.store(2, memory_order_release)
y == 2 相当于 y.load(memory_order_acquire) == 2
？
有点凌乱，这里。</div>2020-01-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/c4/eb/2285a345.jpg" width="30px"><span>花晨少年</span> 👍（0） 💬（1）<div>memory_order_acq_rel只能作用到读取-修改-写操作吗，貌似单纯的读或者写操作也可以用这个order.
那这个order和seq_cst貌似并没有很大的区别，
不明白这两个order的不止区别是什</div>2020-01-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/09/5c/b5d79d20.jpg" width="30px"><span>李亮亮</span> 👍（0） 💬（1）<div>C++真是博大精深</div>2020-01-11</li><br/>
</ul>