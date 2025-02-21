你好，我是鸟窝。

WaitGroup，我们以前都多多少少学习过，或者是使用过。其实，WaitGroup很简单，就是package sync用来做任务编排的一个并发原语。它要解决的就是并发-等待的问题：现在有一个goroutine A 在检查点（checkpoint）等待一组goroutine全部完成，如果在执行任务的这些goroutine还没全部完成，那么goroutine A就会阻塞在检查点，直到所有goroutine都完成后才能继续执行。

我们来看一个使用WaitGroup的场景。

比如，我们要完成一个大的任务，需要使用并行的goroutine执行三个小任务，只有这三个小任务都完成，我们才能去执行后面的任务。如果通过轮询的方式定时询问三个小任务是否完成，会存在两个问题：一是，性能比较低，因为三个小任务可能早就完成了，却要等很长时间才被轮询到；二是，会有很多无谓的轮询，空耗CPU资源。

那么，这个时候使用WaitGroup并发原语就比较有效了，它可以阻塞等待的goroutine。等到三个小任务都完成了，再即时唤醒它们。

其实，很多操作系统和编程语言都提供了类似的并发原语。比如，Linux中的barrier、Pthread（POSIX线程）中的barrier、C++中的std::barrier、Java中的CyclicBarrier和CountDownLatch等。由此可见，这个并发原语还是一个非常基础的并发类型。所以，我们要认真掌握今天的内容，这样就可以举一反三，轻松应对其他场景下的需求了。
<div><strong>精选留言（30）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/17/0c/dd/1b12d77d.jpg" width="30px"><span>Dragon Frog</span> 👍（20） 💬（10）<div>老师好！接 linxs 同学的提问，我觉得他是一开始没表述清楚问题，我之前也有类似的疑问，后来仔细想了想我是这么理解这个问题的，也想请教老师看理解的
--------------------------------------------------
为什么32bit系统的处理上，state1的元素排列和64bit的不同呢
64bit ： waiter,counter,sem
32bit ： sem,waiter,counter
------------------------------------------------------

首先要理解的是**内存对齐**，32 位机和 64 位机的差别在于每次读取的块大小不同，前者一次读取 4 字节的块，后者一次读取 8 字节的块。

 `WaitGroup` 的大小是 12 字节，接下来我声明了一个 `var wg sync.WaitGroup`，假设此处 wg 的内存地址是 0xc420016240，此时这个地址是 64bit 对齐的，因此这里的重点是**不论是 32 位机器还是 64 位机器，state1 的元素排列都是 `waiter,counter,sem`**。wg 的地址空间是 `0xc420016240~0xc42001624c`，因此如果此时是 64 位机的话还有4字节的空间可以分配给其他大小合适的变量。那此时 state1 的排列能不能是 `sem,waiter,counter` 呢？不能，因为 64 bit 值的原子操作必须 64 bit 对齐。

对于 32 位机器就会有一种**特殊情况**，那就是 wg 的内存地址起始被分配到了 0xc420016244，此时这个地址不是 64 bit 对齐的，因此这个时候排列变成了 `sem,waiter,counter`，这样的话，`waiter` 的起始地址变成了 0xc420016248，可以使用 64 bit 值的原子操作。


</div>2020-11-01</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/17/6e/76b4aa3d.jpg" width="30px"><span>橙子888</span> 👍（6） 💬（2）<div>issue 12813 按照 defer 后进先出的原则，Done 一定会在 Add 之前执行吧，为啥是“可能”呢？</div>2020-10-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/22/08/3b/6fbc7ea0.jpg" width="30px"><span>寻风</span> 👍（4） 💬（2）<div>老师你好，我想问一下，为啥64位的int要保证原子操作就一定要64位对齐呢，那么为啥要这样规定呢？之前看到atomic文档后面说了一句就是就是说有部分32位处理器需要使用者自行对齐来保证atomic包中方法的正确性，是不是就是因为waitgroup用了atomic包的东西，为了保证atomic使用的正确才有这样的规定。

atomic文档的内容是：On ARM, x86-32, and 32-bit MIPS, it is the caller’s responsibility to arrange for 64-bit alignment of 64-bit words accessed atomically. The first word in a variable or in an allocated struct, array, or slice can be relied upon to be 64-bit aligned.</div>2021-04-02</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/62/dc/8876c73b.jpg" width="30px"><span>moooofly</span> 👍（4） 💬（1）<div>没理解错的话，waiter 数量对应的应该是调用 Wait() 的 goroutine 的数量吧，文中的示例代码都只是在 main goroutine 中调用一次，所以 waiter 数量都只是 1 ，没错吧</div>2020-10-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/43/79/18073134.jpg" width="30px"><span>test</span> 👍（3） 💬（2）<div>32位&#47;64位对齐的思考：
如果内存地址不是64位对齐，则让seman填充第一个32位，这样子就可以使得后面的state以64位对齐（因为state存储的两个值要同步修改）。</div>2021-05-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/c9/4d/89a764b5.jpg" width="30px"><span>一笑淡然</span> 👍（2） 💬（4）<div>老师好，Add() 中，先将delta&lt;&lt;32位，加入counter，是不是counter应该在waiter位前，即
64bit ： counter,waiter,,sem
32bit ： sem,counter,waiter</div>2021-06-04</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/18/28/93/88a1ee95.jpg" width="30px"><span>蒋巧纯</span> 👍（2） 💬（2）<div>老师好，我想问一下，为什么不在waitgroup中使用32位的原子操作？state1代表的三个值，其实都各占32bit，分离他们并且使用32位的原子操作，不是应该更好理解吗？</div>2020-12-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/21/fd/47/499339d1.jpg" width="30px"><span>新味道</span> 👍（2） 💬（1）<div>  &#47;&#47; 阻塞休眠等待            
runtime_Semacquire(semap)
--------------

没理解『阻塞休眠等待』的意思，能否再详细讲一下。 </div>2020-10-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/17/2f/78/67512fcd.jpg" width="30px"><span>叶君度</span> 👍（1） 💬（2）<div>答案
type WaitGroup struct {
	sync.WaitGroup
}

func (wg *WaitGroup) GetCounter() int64 {

	type nocopy struct{}
	var no nocopy

	t := unsafe.Sizeof(no)
	pointer := unsafe.Pointer(&amp;wg.WaitGroup)
	state := (*atomic.Int64)(unsafe.Pointer(uintptr(pointer) + t))
	return state.Load() &gt;&gt; 32
}

func (wg *WaitGroup) GetWaiter() int64 {
	type nocopy struct{}
	var no nocopy

	t := unsafe.Sizeof(no)
	pointer := unsafe.Pointer(&amp;wg.WaitGroup)
	state := (*atomic.Int64)(unsafe.Pointer(uintptr(pointer) + t))
	return int64(uint32(state.Load()))
}

func Do() {
	var wg WaitGroup
	wg.Add(10)
	fmt.Printf(&quot;counter: %d, waiter: %d\n&quot;, wg.GetCounter(), wg.GetWaiter())
	for i := 0; i &lt; 10; i++ {
		go func() {
			time.Sleep(time.Second)
			wg.Done()
			fmt.Printf(&quot;counter: %d, waiter: %d\n&quot;, wg.GetCounter(), wg.GetWaiter())
		}()
	}
	for i := 0; i &lt; 10; i++ {
		go func() {
			wg.Wait()
		}()
	}
	wg.Wait()
	fmt.Printf(&quot;counter: %d, waiter: %d\n&quot;, wg.GetCounter(), wg.GetWaiter())

}</div>2024-04-16</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/4e/6c/71020c59.jpg" width="30px"><span>王麒</span> 👍（1） 💬（1）<div>如果你想要自己定义的数据结构不被复制使用，或者说，不能通过 vet 工具检查出复制使用的报警，就可以通过嵌入 noCopy 这个数据类型来实现。
这里不应该是能通过vet工具检查出复制吗。。看起来怪怪的。</div>2021-03-31</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/5c/88/222d946e.jpg" width="30px"><span>linxs</span> 👍（1） 💬（3）<div>为什么32bit系统的处理上，state1的元素排列和64bit的不同呢
64bit ： waiter,counter,sem
32bit ： sem,waiter,counter</div>2020-10-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/18/75/bc/89d88775.jpg" width="30px"><span>Calvin</span> 👍（0） 💬（1）<div>原文中“不能通过 vet 工具检查出复制使用的报警，就可以通过嵌入 noCopy 这个数据类型来实现。”我认为可以优化一下描述：“不能通过 vet 工具检查出复制使用的报警，就可以通过添加 noCopy 这个数据类型的非导出字段来实现。”，因为最新的（当前 go1.22）源码中 noCopy 结构体上中有明确的一个注意项描述：“Note that it must not be embedded, due to the Lock and Unlock methods.”！</div>2024-06-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/37/3f/7c/069c163f.jpg" width="30px"><span>hhhhhh</span> 👍（0） 💬（1）<div>老师您好，我看到对于64位环境来说，WaitGroup中的state1[0]表示witer数，state1[1]表示计数值，那么Add方法中，delta左移32位，修改的不是waiter数吗？

下面是我对Add方法的理解
func (wg *WaitGroup) Add(delta int) {
	statep, semap := wg.state()
	
    &#47;&#47; 将delta左移32位，然后将其作为无符号整数与state的高32位（waiter数）进行相加
	state := atomic.AddUint64(statep, uint64(delta)&lt;&lt;32)
	v := int32(state)          &#47;&#47; 计数值
	w := uint32(state &gt;&gt; 32)   &#47;&#47; waiter数（已经更新）
	
    if v == 0 || w &gt; 0 {
		return
	}
	
	*statep = 0
	for ; w != 0; w-- {
		runtime_Semrelease(semap, false, 0)
	}
}</div>2024-01-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1a/19/99/ba3719e1.jpg" width="30px"><span>The brain is a good thing</span> 👍（0） 💬（1）<div>有个疑问：
查阅到的资料：
为了充分利用CPU指令来达到最佳程序性能，为一个特定类型的值开辟的内存块的起始地址必须为某个整数N的倍数。 N被称为此类型的值地址对齐保证。  

type waitGroup struct {
		state1 [3]uint32
}
	var wg waitGroup
	fmt.Println(unsafe.Alignof(wg.state1))
	fmt.Println(uintptr(unsafe.Pointer(&amp;wg.state1))%8 == 0)

这里系统架构是64位，但输出的对齐保证是 4，并且%8 ！=0，

为什么原文中64位架构下，起始地址一定是64位（8字节，8N）对齐
uintptr(unsafe.Pointer(&amp;wg.state1))%8 == 0

求解答，是不是哪里理解错误了</div>2022-08-16</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTINObH6BicJCaorsWLcYs1QAvFt2wiaoRWHp5MQegAAJCrPH66Ucjgg5bpTOH78yvGwHzanhHPOc7VQ/132" width="30px"><span>GEEKBANG_5295513</span> 👍（0） 💬（1）<div>老师好，请教一个问题

func (wg *WaitGroup) Add(delta int) {
    statep, semap := wg.state()
    &#47;&#47; 高32bit是计数值v，所以把delta左移32，增加到计数上
    state := atomic.AddUint64(statep, uint64(delta)&lt;&lt;32)
    v := int32(state &gt;&gt; 32) &#47;&#47; 当前计数值
    w := uint32(state) &#47;&#47; waiter count

    if v &gt; 0 || w == 0 {
        return
    }

    &#47;&#47; 如果计数值v为0并且waiter的数量w不为0，那么state的值就是waiter的数量
    &#47;&#47; 将waiter的数量设置为0，因为计数值v也是0,所以它们俩的组合*statep直接设置为0即可。此时需要并唤醒所有的waiter
    *statep = 0
    for ; w != 0; w-- {
        runtime_Semrelease(semap, false, 0)
    }
}

在这段代码中，*statep = 0 这里没有用原子操作，不会有问题么？</div>2022-03-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/57/4f/6fb51ff1.jpg" width="30px"><span>奕</span> 👍（0） 💬（3）<div> 关于 WaitGroup state1 三部分含义是不是 counter,waiter,sema
看了代码和注释都是证明这一点
&#47;&#47; 64-bit value: high 32 bits are counter, low 32 bits are waiter count.
state := atomic.AddUint64(statep, uint64(delta)&lt;&lt;32)
v := int32(state &gt;&gt; 32)
w := uint32(state)

老师画的图是不是有问题？

</div>2022-03-03</li><br/><li><img src="" width="30px"><span>Geek6666</span> 👍（0） 💬（1）<div>不知道这个时候提出疑问，老师还会不会看的

对于func (wg *WaitGroup) state() (statep *uint64, semap *uint32) 函数，我的理解是由于要兼容64位的uint64原子操作，所以要判断内存对齐情况，这里只是判断wg.state1的地址是否是8个字节对齐的，如果是8字节对齐，就使用 waiter,counter,sem的顺序，结论就是不管是32位还是64位，只要wg.state1的地址是8字节对齐，就使用 waiter,counter,sem的顺序，，和大家的理解都不一致，不知道对错</div>2021-11-16</li><br/><li><img src="" width="30px"><span>地下城勇士</span> 👍（0） 💬（1）<div>「可以阻塞等待的 goroutine。等到三个小任务都完成了，再即时唤醒它们」
---
老师，没有理解这句话是什么意思？什么叫阻塞等待？还有完成了，为什么还要唤醒？</div>2020-10-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1b/95/dc/07195a63.jpg" width="30px"><span>锋</span> 👍（0） 💬（1）<div>老师好，有两个疑问，谢谢。

1.wg.Add(-1) 
这个方法是在Done中调用的。但是我没太理解 -1的时候，是怎么减去的。我在Add中的代码中看到
state := atomic.AddUint64(statep, uint64(delta)&lt;&lt;32)
我在想一个uint64是一个无符号的，是怎么做到减一呢

2.noCopy
像老师最后说的，想把我们自己写的一些struct组合以便通过vet可以进行复制检测。但是这个类型是私有的啊？该怎么使用,有没有样例，谢谢老师。</div>2020-10-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/8f/cf/890f82d6.jpg" width="30px"><span>那时刻</span> 👍（0） 💬（2）<div>请问老师，waitgroup里state1里提到对 64 位整数的原子操作要求整数的地址是 64 位对齐的，不是很理解，能否提供例子说明下呢？
另外在32位对齐的图例里，也有个64位对齐指示，是什么含义呢？</div>2020-10-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/8f/cf/890f82d6.jpg" width="30px"><span>那时刻</span> 👍（11） 💬（1）<div>关于64位对齐，这个帖子讲的也不错，分享一下。https:&#47;&#47;go101.org&#47;article&#47;memory-layout.html</div>2020-10-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/22/17/11/a63acc6a.jpg" width="30px"><span>( ･᷄ὢ･᷅ )</span> 👍（4） 💬（0）<div>刚才那个作业没完全 这回加上了 32位和64位的区分，因为没有32位测试环境 所以仅测试了64位
type WaitGroup struct {
	sync.WaitGroup
}

func (receiver *WaitGroup) GetCounter32()uint32   {
	pointer:=unsafe.Pointer(&amp;receiver.WaitGroup)
	return *(*uint32)(unsafe.Pointer(uintptr(pointer)+8))
}
func (receiver *WaitGroup) GetCounter64()uint32   {
	pointer:=unsafe.Pointer(&amp;receiver.WaitGroup)
	return *(*uint32)(unsafe.Pointer(uintptr(pointer)+4))
}

func main() {
 a:=WaitGroup{}
 a.Add(19999)
 fmt.Println(a.GetCounter64())
}</div>2020-12-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/ab/a9/590d6f02.jpg" width="30px"><span>Junes</span> 👍（2） 💬（0）<div>思路：主要难点在于32位和64位时的处理，具体逻辑就参考sync.WaiterGroup源码中的state()方法，跟老师的示例图互相映证。

实现：
func getStateAndWait(wgp *sync.WaitGroup) (uint32, uint32) {
	var statep *uint64
	if uintptr(unsafe.Pointer(wgp))%8 == 0 {
		statep = (*uint64)(unsafe.Pointer(wgp))
	} else {
		statep = (*uint64)(unsafe.Pointer(uintptr(unsafe.Pointer(wgp)) + unsafe.Sizeof(uint32(0))))
	}
	return uint32(*statep &gt;&gt; 32), uint32(*statep)
}

注意点：
1.  这里用了一个函数来实现，更常见的可以自己封一个类。用函数实现时注意用指针传递wg
2. 返回的两个值分别是state和wait，state是要完成的waiter计数值（即等待多少个goroutine完成）；wait是指有多少个sync.Wait在等待（和前面的waiter不是一个概念）。

最后谈一点：
nocopy这个字段之前一直没有注意，没想到还有这么巧妙的方法~</div>2020-10-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/18/75/bc/89d88775.jpg" width="30px"><span>Calvin</span> 👍（0） 💬（0）<div>原理图是反的，高32位应该是 counter 计数器，低32位是 waiter 计数。</div>2024-06-05</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/37/08/07/6fb347e5.jpg" width="30px"><span>KillSome</span> 👍（0） 💬（0）<div>这个代码有点老了吧，1.19的有两个state，state1和state2了</div>2023-08-02</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/37/92/961ba560.jpg" width="30px"><span>授人以🐟，不如授人以渔</span> 👍（0） 💬（0）<div>没人解答思考题，我贴下结果，请老师们看看是否正确：
func calcWaitGroupCount() {
	&#47;&#47; 获取 WaitGroup 的计数值
	var wg sync.WaitGroup

	wg.Add(20)
	&#47;&#47; state1 [3]uint32，当前是 64bit 的
	&#47;&#47; state1[0]：Waiter数目，也就是调用了 Wait() 的 goroutine 的数量
	&#47;&#47; state1[1]：计数值

	for i := 10; i &gt; 0; i-- {
		go func(i int) {
			wg.Wait()
		}(i)
	}

	time.Sleep(1 * time.Second)
	ptr := (*uint64)(unsafe.Pointer((uintptr(unsafe.Pointer(&amp;wg)))))
	counter := int32(*ptr &gt;&gt; 32)
	waiters := uint32(*ptr)
	log.Printf(&quot;waiters:%d, counter:%d&quot;, waiters, counter)

	wg.Add(-20)
	wg.Wait()
}</div>2021-11-03</li><br/><li><img src="" width="30px"><span>Geek8956</span> 👍（0） 💬（0）<div>结构体的state（）函数中，“if uintptr(unsafe.Pointer(&amp;wg.state1))%8 == 0 {”中的这个模8。这个就在判断state1的其实地址，是不是64位对齐的。</div>2021-10-25</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/c9/4d/89a764b5.jpg" width="30px"><span>一笑淡然</span> 👍（0） 💬（0）<div>老师好，Add() 中，先将delta&lt;&lt;32位，加入counter，是不是counter位应该在waiter位前，即
64bit：counter,waiter,,sem
32bit：sem,counter,waiter</div>2021-06-04</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/ab/a0/ea8b62f7.jpg" width="30px"><span>姜小凡</span> 👍（0） 💬（0）<div>我还是习惯用go的扩展 ErrorGroup</div>2021-05-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/f8/ba/d28174a9.jpg" width="30px"><span>Geek_zbvt62</span> 👍（0） 💬（0）<div>如果有一个goroutine先调用了runtime_Semrelease，之后另一个goroutine调用runtime_Semacquire，应该不会阻塞而是立即返回吧？考虑到如下场景：Wait方法假如执行完13行，此时Done方法整个执行完成，之后Wait方法执行15行。</div>2020-10-25</li><br/>
</ul>