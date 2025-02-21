我们在前几次讲的互斥锁、条件变量和原子操作都是最基本重要的同步工具。在Go语言中，除了通道之外，它们也算是最为常用的并发安全工具了。

说到通道，不知道你想过没有，之前在一些场合下里，我们使用通道的方式看起来都似乎有些蹩脚。

比如：**声明一个通道，使它的容量与我们手动启用的goroutine的数量相同，之后再利用这个通道，让主goroutine等待其他goroutine的运行结束。**

这一步更具体地说就是：让其他的goroutine在运行结束之前，都向这个通道发送一个元素值，并且，让主goroutine在最后从这个通道中接收元素值，接收的次数需要与其他的goroutine的数量相同。

这就是下面的`coordinateWithChan`函数展示的多goroutine协作流程。

```
func coordinateWithChan() {
 sign := make(chan struct{}, 2)
 num := int32(0)
 fmt.Printf("The number: %d [with chan struct{}]\n", num)
 max := int32(10)
 go addNum(&num, 1, max, func() {
  sign <- struct{}{}
 })
 go addNum(&num, 2, max, func() {
  sign <- struct{}{}
 })
 <-sign
 <-sign
}
```

其中的`addNum`函数的声明在demo65.go文件中。`addNum`函数会把它接受的最后一个参数值作为其中的`defer`函数。

我手动启用的两个goroutine都会调用`addNum`函数，而它们传给该函数的最后一个参数值（也就是那个既无参数声明，也无结果声明的函数）都只会做一件事情，那就是向通道`sign`发送一个元素值。
<div><strong>精选留言（30）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/10/27/fc/b8d83d56.jpg" width="30px"><span>Geek_e68th4</span> 👍（20） 💬（2）<div>“双重检查” 貌似也并不是完全安全的吧，像c++11那样加入内存屏障才是真正线性安全的。go有这类接口吗</div>2019-02-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/05/3c/6f2a4724.jpg" width="30px"><span>唐大少在路上。。。</span> 👍（17） 💬（3）<div>个人感觉Once里面的逻辑设计得不够简洁，既然目的就是只要能够拿到once的锁的gorountine就会消费掉这个once，那其实直接在Do方法的最开始用if atomic.CompareAndSwapUint32(&amp;o.done, 0,1)不就行了，连锁都不用。
还请老师指正，哈哈</div>2019-10-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/17/4a/53/063f9d17.jpg" width="30px"><span>moonfox</span> 👍（10） 💬（1）<div>请问一下，在 sync.Once的源码里， doSlow()方法中，已经用了o.m.Lock()，什么写入o.done=1的时候，还要用原子写入呢？</div>2021-05-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/02/3b/b4a47f63.jpg" width="30px"><span>only</span> 👍（10） 💬（0）<div>可不可以把 sync.once 理解为单例模式，比如连接数据库只需要连接一次，把连接数据库的代码实在once.do()里面</div>2019-12-10</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTIGMzsqGicBHicmA0xosKibBSmFjrwG8LuRwky3QlZibJt1treDMLPuaKviaC9JrJdQpdJE199ztVMJOGQ/132" width="30px"><span>超大叮当当</span> 👍（7） 💬（1）<div>sync.Once 不用 Mutex ，直接用 atomic.CompareAndSwapUint32 函数也可以安全吧？</div>2019-03-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1d/c3/22/8520be75.jpg" width="30px"><span>1287</span> 👍（3） 💬（2）<div>没理解使用once和自己只调用一次有什么区别，类似初始化的操作，我在程序执行前写个init也是只执行一次吧，求教</div>2020-05-25</li><br/><li><img src="" width="30px"><span>窗外</span> 👍（3） 💬（2）<div>go func ()  {
		 wg.Done()
		fmt.Println(&quot;send complete&quot;)
	 }()
老师，为什么在Done()后的代码就不会被执行呢？</div>2019-11-03</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/0M3kK7d2sLapYh9VgqzQargLNkiaJbJZTDNjzLhm9s9FYbFUVDSKa74yvcvH5IHWgknuibmh9fObbrHXvfAib28IQ/132" width="30px"><span>手指饼干</span> 👍（3） 💬（2）<div>请问老师，如下deferFunc为什么要用func包装起来，直接使用defer deferFunc()不可以吗？
func addNum(numP *int32, id, max int32, deferFunc func()) {
	defer func() {
		deferFunc()
	}()
	&#47;&#47;...
}</div>2019-10-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/4a/96/99466a06.jpg" width="30px"><span>Laughing</span> 👍（3） 💬（1）<div>子任务的结果应该用通道来传递吧。另外once的应用场景还是没有理解。郝大能简单说一下么？</div>2018-10-30</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/97/c5/84491beb.jpg" width="30px"><span>罗峰</span> 👍（2） 💬（1）<div>老师，你好，waitgroup的计数周期这个概念是自创的吗？使用上感觉 只要 add操作在wait语句之前执行就可以，使用个例子：
 for {
      select {
      case &lt;- cancel:
         break;
      case &lt;- taskqueue:
        go func {
             wg.add(1)
              ....
             defer wg.done()
            }
     }
}
wg.wait()</div>2021-01-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/3b/ba/3b30dcde.jpg" width="30px"><span>窝窝头</span> 👍（1） 💬（1）<div>执行结果可以通过共享内存、channel之类的，如果只是想让其他协程等待所有协程都完成后统一退出的话是不是每个协程里面wg.Done,然后wg.Wait就行了</div>2022-01-06</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/97/86/fb564a19.jpg" width="30px"><span>bluuus</span> 👍（1） 💬（3）<div>func coordinateWithWaitGroup() {
	var wg sync.WaitGroup
	wg.Add(2)
	num := int32(0)
	fmt.Printf(&quot;The number: %d [with sync.WaitGroup]\n&quot;, num)
	max := int32(10)
	go addNum(&amp;num, 3, max, wg.Done)
	&#47;&#47;go addNum(&amp;num, 4, max, wg.Done)
	wg.Wait()
}

run result:
The number: 0 [with sync.WaitGroup]
The number: 2 [3-0]
The number: 4 [3-1]
The number: 6 [3-2]
The number: 8 [3-3]
The number: 10 [3-4]
fatal error: all goroutines are asleep - deadlock!

执行这段代码会死锁，我以为最多在wai()方法那儿阻塞，谁能解释一下？
</div>2019-09-06</li><br/><li><img src="" width="30px"><span>NeoMa</span> 👍（0） 💬（1）<div>您好，关于once.go中 doSlow方法有两个疑问：
1. 在拿到m.Lock()锁之后的o.done == 0 的判断能否省略？或者说这个判断针对的是某些可能的未知场景吗？我的理解是，理论上此时这个值一定是0，但为了确保预防未知场景又做了一次判断。
2. defer atomic.StoreUint32(&amp;o.done, 1) 这个操作是否可以不用原子操作，只是使用例如 o.done = 1类似的赋值操作？
希望您多多指正。</div>2022-01-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/74/d5/56b3a879.jpg" width="30px"><span>poettian</span> 👍（0） 💬（1）<div>老师，once 里的实现为什么要用原子操作呢？不是已经有锁了。这点不是很明白。</div>2021-01-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/97/59/6f9c036e.jpg" width="30px"><span>Godruoyi</span> 👍（0） 💬（1）<div>type myOnce struct {
	done uint32
	m    sync.Mutex

	a bool
}

func (m *myOnce) Do(f func()) {
	if atomic.CompareAndSwapUint32(&amp;m.done, 0, 1) {
		f()
		m.a = true
	}

	for {
		if m.a {
			break
		}
	}

	return
}


for 循环阻塞和加锁阻塞有什么区别呢</div>2020-11-10</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTKdiaUiaCYQe9tibemaNU5ya7RrU3MYcSGEIG7zF27u0ZDnZs5lYxPb7KPrAsj3bibM79QIOnPXAatfIw/132" width="30px"><span>Geek_a8be59</span> 👍（0） 💬（6）<div>个人感觉Once里面的逻辑设计得不够简洁，既然目的就是只要能够拿到once的锁的gorountine就会消费掉这个once，那其实直接在Do方法的最开始用if atomic.CompareAndSwapUint32(&amp;o.done, 0,1)不就行了，连锁都不用。
还请老师指正，哈哈

作者回复: 这样不行啊，它还得执行你给它的函数啊。怎么能在没执行函数之前就把 done 变成 1 呢，对吧。但如果是在执行之后 swap，那又太晚了，有可能出现重复执行函数的情况。

所以 Once 中才有两个执行路径，一个是仅包含原子操作的快路径，另一个是真正准备执行函数的慢路径。这样才可以兼顾多种情况，让总体性能更优。

您好，根据这位描述，我也觉得可以直接这么使用呀，类似改成下面这块
func (o *once) Do(fn func())  {
	if atomic.CompareAndSwapInt32(&amp;o.done, 0, 1) {
		fn()
	}
	return
}
只有在交换成功的时候执行这个操作，不知道我这个理解上有什么问题，请指教</div>2020-07-15</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/53/db/858337e3.jpg" width="30px"><span>Ethan Liu</span> 👍（0） 💬（3）<div>为什么在慢路径中第二次进行条件判断（if o.done == 0）不对done用原子操作呢？</div>2020-06-25</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/df/1e/cea897e8.jpg" width="30px"><span>传说中的成大大</span> 👍（0） 💬（1）<div>关于思考题 采用共享内存 或者通道的方式去获取结果</div>2020-04-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/5f/43/3799a0f3.jpg" width="30px"><span>magina</span> 👍（0） 💬（1）<div>WaitGroup能不能设置超时</div>2019-08-05</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/20/27/a6932fbe.jpg" width="30px"><span>虢國技醬</span> 👍（6） 💬（0）<div>二刷走起</div>2019-11-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/6c/b2/362353ba.jpg" width="30px"><span>蔺晨</span> 👍（4） 💬（0）<div>思考题 :
func getAllGoroutineResult(){
		wg := sync.WaitGroup{}
		wg.Add(3)

		once := sync.Once{}
		var aAndb int
		var aStrAndb string
		var gflag int32

		addNum := func(a,b int, ret *int) {
			defer wg.Done()
			time.Sleep(time.Millisecond * 2000)
			*ret = a+b
			atomic.AddInt32(&amp;gflag,1)
		}

		addStr := func(a,b string, ret *string) {
			defer wg.Done()
			time.Sleep(time.Millisecond * 1000)
			*ret = a+b
			atomic.AddInt32(&amp;gflag,1)
		}

		&#47;&#47; waitRet需要等待 addNum和addStr执行完成后的结果
		waitRet := func(ret *int, strRet *string) {
			defer wg.Done()
			once.Do(func() {
				for atomic.LoadInt32(&amp;gflag) != 2 {
					fmt.Println(&quot;Wait: addNum &amp; addStr&quot;)
					time.Sleep(time.Millisecond * 200)
				}
			})
			fmt.Println(fmt.Sprintf(&quot;AddNum&#39;s Ret is: %d\n&quot;, *ret))
			fmt.Println(fmt.Sprintf(&quot;AddStr&#39;s Ret is: %s\n&quot;, *strRet))
		}

		&#47;&#47; waitRet goroutine等待AddNum和AddStr结束
		go waitRet(&amp;aAndb, &amp;aStrAndb)
		go addNum(10, 20, &amp;aAndb)
		go addStr(&quot;测试结果&quot;, &quot;满意不?&quot;, &amp;aStrAndb)

		wg.Wait()
}</div>2018-11-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/bb/10/f01eafe4.jpg" width="30px"><span>ricktian</span> 👍（3） 💬（2）<div>执行结果如果不用channel实现，还有什么方法？请老师指点～</div>2018-11-30</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/4f/78/c3d8ecb0.jpg" width="30px"><span>undifined</span> 👍（3） 💬（0）<div>执行结果用 Callback，放在通道中，在主 goroutine 中接收返回结果</div>2018-10-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/df/1e/cea897e8.jpg" width="30px"><span>传说中的成大大</span> 👍（1） 💬（0）<div>今日总结
这里主要讲了sync&#47;waitgroup和sync&#47;once这两种同步的方式
waitgroup一般用于一对多的同步 例如 主goroutine等待其他goroutine的执行完成
唯一要注意的是 add方法和wait方法不要并行执行 也即 wait方法调用过后 不要立即再调用add方法
once值 主要还是保证函数只被执行一次 且只有第一次调用Do方法的参数函数会被执行一次 once值底层依赖的是互斥锁 所以操作和互斥锁很类似
并且 如果某个Do的参数函数一直不结束 那么其他调用Do方法的goroutine都会被阻塞在获取互斥锁这一步，只有当首次Do方法的参数函数执行结束过后 这些goroutine才会被逐一唤醒
所以要注意 Once 在使用死的死锁 </div>2020-04-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/7f/75/551c5d6c.jpg" width="30px"><span>CrazyCodes</span> 👍（0） 💬（0）<div>在使用WaitGroup值实现一对多的 goroutine 协作流程时，怎样才能让分发子任务的 goroutine 获得各个子任务的具体执行结果？

可以通过channel的方式，或者context来通知子任务的执行情况</div>2023-11-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/e8/55/63189817.jpg" width="30px"><span>MClink</span> 👍（0） 💬（0）<div>easy case
func TestWaitGroup() {
	var wg sync.WaitGroup
	wg.Add(3)
	for i := 0; i &lt; 3; i++ {
		go func() {
			defer wg.Done()
			time.Sleep(time.Second * 3)
			fmt.Println(&quot;done!&quot;)
		}()
	}

	wg.Wait()
	fmt.Println(&quot;over&quot;)
}

func TestOnce() {
	var o sync.Once
	var wg sync.WaitGroup
	wg.Add(10)
	for i := 0; i &lt; 10; i++ {
		go func() {
			defer wg.Done()
			time.Sleep(time.Second * 1)
			o.Do(func() {
				fmt.Println(&quot;mclink&quot;)
			})
		}()
	}
	wg.Wait()
	fmt.Println(&quot;over&quot;)
}</div>2022-07-10</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/DYAIOgq83erpYZalYvFGcBs7zZvYwaQAZwTLiaw0mycJ4PdYpP3VxAYkAtyIRHhjSOrOK0yESaPpgEbVQUwf6LA/132" width="30px"><span>Harlan</span> 👍（0） 💬（0）<div>go 里面使用waitGroup后，对多个goroutine 的结果还是得用 ch来处理,比较难受</div>2021-09-15</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/e8/ed/f9347e5e.jpg" width="30px"><span>松小鼠</span> 👍（0） 💬（0）<div>感觉 sync.WaitGroup 和java的CountDownLatch（）很像。</div>2020-12-03</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1c/f7/62/947004d0.jpg" width="30px"><span>www</span> 👍（0） 💬（0）<div>“Once类型使用互斥锁和原子操作实现了功能，而WaitGroup类型中只用到了原子操作。	所以可以说，它们都是更高层次的同步工具。它们都基于基本的通用工具，实现了某一种特定的功能。sync包中的其他高级同步工具，其实也都是这样的。“，点出sync包搭积木的基础，类别数据结构中的数组和链表是其他数据结构的基础，精彩</div>2020-06-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1c/f7/62/947004d0.jpg" width="30px"><span>www</span> 👍（0） 💬（0）<div>LoadInt32()原子性得到原变量的值，执行操作后，再通过CompareAndSwapInt32()原子性的比较*addr和old，如果相同则将new赋值给*addr并返回真，通过比较来判断原变量在函数运行过程中没有被其他Go程修改，进而保证得到结果是符合预期的。如果被修改则得到失败结果。感觉原子操作比上锁解锁操心的多，老师代码例子写得真好。</div>2020-06-28</li><br/>
</ul>