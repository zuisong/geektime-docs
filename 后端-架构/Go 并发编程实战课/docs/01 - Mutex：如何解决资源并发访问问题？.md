你好，我是鸟窝。

今天是我们Go并发编程实战课的第一讲，我们就直接从解决并发访问这个棘手问题入手。

说起并发访问问题，真是太常见了，比如多个goroutine并发更新同一个资源，像计数器；同时更新用户的账户信息；秒杀系统；往同一个buffer中并发写入数据等等。如果没有互斥控制，就会出现一些异常情况，比如计数器的计数不准确、用户的账户可能出现透支、秒杀系统出现超卖、buffer中的数据混乱，等等，后果都很严重。

这些问题怎么解决呢？对，用互斥锁，那在Go语言里，就是**Mutex。**

这节课，我会带你详细了解互斥锁的实现机制，以及Go标准库的互斥锁Mutex的基本使用方法。在后面的3节课里，我还会讲解Mutex的具体实现原理、易错场景和一些拓展用法。

好了，我们先来看看互斥锁的实现机制。

## 互斥锁的实现机制

互斥锁是并发控制的一个基本手段，是为了避免竞争而建立的一种并发控制机制。在学习它的具体实现原理前，我们要先搞懂一个概念，就是**临界区**。

在并发编程中，如果程序中的一部分会被并发访问或修改，那么，为了避免并发访问导致的意想不到的结果，这部分程序需要被保护起来，这部分被保护起来的程序，就叫做临界区。

可以说，临界区就是一个被共享的资源，或者说是一个整体的一组共享资源，比如对数据库的访问、对某一个共享数据结构的操作、对一个 I/O 设备的使用、对一个连接池中的连接的调用，等等。
<div><strong>精选留言（30）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/0f/55/47/d217c45f.jpg" width="30px"><span>Panmax</span> 👍（27） 💬（4）<div>原文中关于 race detector 的介绍有两句话前后矛盾，老师可否解释一下：

前边说：在编译（compile）、测试（test）或者运行（run）Go 代码的时候，加上 race 参数，就有可能发现并发问题。

后边却又说：因为它的实现方式，只能通过真正对实际地址进行读写访问的时候才能探测，所以它并不能在编译的时候发现 data race 的问题。

所以结论是 race detector 并不能在编译阶段发现并发问题？那么前边那句是不是就没必要提了，不然容易让大家误会。</div>2020-10-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/52/40/e57a736e.jpg" width="30px"><span>pedro</span> 👍（21） 💬（4）<div>大家都已经解答了，就不重复了。这里给一些不熟悉 go 需要的同学补充一下，go 语言查看汇编代码命令:
go tool compile -S file.go
对于文中 counter 的例子可以过度优化一下，那就是获取计数的 Count 函数其实可以通过读写锁，也就是 RWMutex 来优化一下。</div>2020-10-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/6b/5f/8d10c47a.jpg" width="30px"><span>骁勇善战</span> 👍（14） 💬（2）<div>老师，为什么读也要加锁呢？</div>2021-06-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/99/54/55554fa1.jpg" width="30px"><span>ZY</span> 👍（7） 💬（1）<div>有两种情况
1. 如果当前有协程进入自旋模式，当前协程会成功获取到锁
2. 如果没有协程进入自选模式，释放锁的协程会释放的信号量会成功唤醒等待队列中的协程，该卸程会成功获取到锁，并且把等待计数器减1.

老师：在饥饿模式下，信号量唤醒的协程成功获取到锁之后，该Mutex的模式会改变吗？</div>2020-10-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/f9/43/654d107e.jpg" width="30px"><span>一代咩神</span> 👍（6） 💬（1）<div>能否解答一下，为什么获取计数器的值也需要加锁？</div>2021-01-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/53/c4/dea5d7f3.jpg" width="30px"><span>chapin</span> 👍（4） 💬（1）<div>个人希望🐤 窝大佬可以多分析一些源码。</div>2020-10-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/27/ff/e4/927547a9.jpg" width="30px"><span>无名无姓</span> 👍（3） 💬（1）<div>请问老师goroutine里面自旋怎么理解</div>2021-10-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1f/52/3e/f74da7bd.jpg" width="30px"><span>初学者</span> 👍（3） 💬（1）<div>老师好，“多个goroutine并发更新同一个资源”，这里的同一个资源的条件是不是应该是堆栈分析后分配到堆上的变量，因为堆上是线程共享的，如果是栈上的变量的话，因为是线程独有的就不会出现并发更新的问题，望老师解答下</div>2021-05-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/fd/49/2f38bb6d.jpg" width="30px"><span>Singin in the Rain</span> 👍（2） 💬（1）<div>在Go 1.20之后的版本，执行命令『go tool compile -race -S counter.go』会报如下的错误：
could not import fmt (file not found)
could not import sync (file not found)
导致错误的原因是：在Go 1.20之前，标准库被安装到$GOROOT&#47;pkg&#47;$GOOS_$GOARCH。从Go 1.20开始，标准库被构建和缓存但没有安装。可以通过设置GODEBUG=installgoroot=all，然后编译重新安装Go运行环境，恢复$GOROOT&#47;pkg&#47;$GOOS_$GOARCH的使用，但是改动太大。可以通过如下命令解决这个问题：
不带race参数：go build -gcflags=-S counter.go 1&gt; normal.txt 2&gt;&amp;1
带race参数：go build -race -gcflags=-S counter.go 1&gt; race.txt 2&gt;&amp;1
参考链接：
https:&#47;&#47;github.com&#47;golang&#47;go&#47;issues&#47;58629
https:&#47;&#47;pkg.go.dev&#47;cmd&#47;go
https:&#47;&#47;go.dev&#47;doc&#47;asm</div>2023-04-04</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/5b/66/ad35bc68.jpg" width="30px"><span>党</span> 👍（1） 💬（1）<div>再用boltDb数据库时候 加上-race就会报错 fatal error: checkptr: converted pointer straddles multiple allocations 去掉就不报错了，代码里只有一句创建表，报的这个错也不是 data race错 是指针转换问题 咋弄啊</div>2021-11-01</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/5b/66/ad35bc68.jpg" width="30px"><span>党</span> 👍（1） 💬（1）<div>用了一个内存库 github.com&#47;boltdb&#47;bolt，在用-race 运行的时候，里边一个函数的时候报错 panic类型的，fatal error: checkptr: converted pointer straddles multiple allocations 关键的两行报错  
D:&#47;GO&#47;src&#47;runtime&#47;checkptr.go:20 +0xc9 fp=0xc00029f9e8 sp=0xc00029f9b8 p
c=0x554b89
github.com&#47;boltdb&#47;bolt.(*freelist).write(0xc0004e5290, 0xc000508000, 0xc00050800
0, 0x0)
百度不出来所以然 老师这东西为啥报错啊 不带race运行好好的</div>2021-09-02</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/21/fc/ae/0bfbb04a.jpg" width="30px"><span>Albert</span> 👍（1） 💬（1）<div>老师，，获取计数器的值 也加锁，解释为可能不能得到刚增加的值。&#47;&#47; 使用WaitGroup等待10个goroutine完成 既然已经完了计数的协程。为啥最后打印计数器 还可能不是最终的值啊？</div>2021-01-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/21/fd/47/499339d1.jpg" width="30px"><span>新味道</span> 👍（1） 💬（4）<div>func (c *Counter) Incr() { c.mu.Lock() c.count++ c.mu.Unlock()}&#47;&#47; 得到计数器的值，也需要锁保护func (c *Counter) Count() uint64 { c.mu.Lock() defer c.mu.Unlock() return c.count}

问题：Incr()里为什么不用defer c.mu.Unlock() ?</div>2020-10-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/1c/cd/8d552516.jpg" width="30px"><span>Gojustforfun</span> 👍（1） 💬（2）<div>如果可以，希望老师将完整代码发一下。

另外，有个长久的疑问（很多Java背景的同事都这样）——明明Counter类型本身已经具有语义&#47;上下文，其中的字段只要用Type&#47;Name命名就好，调用:counter.Type&#47;counter.Name。

但常常看到的是counter.CounterType&#47;counter.CounterName？</div>2020-10-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1b/93/b2/27620044.jpg" width="30px"><span>寻回光明</span> 👍（0） 💬（2）<div>老师go tool compile -race -S Counter.go
Counter.go:4:2: could not import fmt (file not found)
Counter.go:5:2: could not import sync (file not found)这个什么原因呀</div>2022-12-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/19/bb/e0/72d9448e.jpg" width="30px"><span>方寸</span> 👍（0） 💬（1）<div>题外话， 后面两个例子不创建实例， 是可以定义的时候， 会默认实例吗？</div>2022-07-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/22/c9/cc/6df7887e.jpg" width="30px"><span>吴同学</span> 👍（0） 💬（2）<div>老师，不是说“若有新goroutine竞争大概率新goroutine获得”，为什么下边的代码，每次都是50个旧的go程抢到锁之后，新的go程才会抢到。而不是在50个旧的go程执行的过程中，被每隔五秒创建的100个新的go程给抢断了。希望老师帮忙解释一下，万分感谢。

func main() {

	var mux sync.Mutex
	for i := 1; i &lt;= 50; i++ {
		go func(i int) {
			mux.Lock()
			fmt.Printf(&quot;第%d个go程获取到锁！\n&quot;, i)
			time.Sleep(time.Second)
			mux.Unlock()
		}(i)
		time.Sleep(time.Millisecond)
		fmt.Printf(&quot;第%d个go程准备就位\n&quot;, i)
	}

	&#47;&#47; 睡两秒确保上述50个go程均处于阻塞状态
	time.Sleep(time.Second * 2)

	&#47;&#47; 监听go程数量
	go func() {
		for i := 0; i &lt; 1000; i++ {
			fmt.Println(&quot;此时go程的数量是:&quot;, runtime.NumGoroutine())
			time.Sleep(time.Second)
		}
	}()

	&#47;&#47; 每隔五秒创建100个新的go程，同样无法模拟新的go程会比之前50个go程优先抢到锁
	for {
		for i := 0; i &lt; 100; i++ {
			go func() {
				mux.Lock()
				fmt.Println(&quot;新go程获取到锁！&quot;)
				mux.Unlock()
			}()
		}
		time.Sleep(time.Second * 5)
	}
}
</div>2022-02-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/9c/5e/80bbb02c.jpg" width="30px"><span>BROOKS</span> 👍（0） 💬（2）<div>&gt; 得到计数器的值，也需要锁保护

个人认为 Count() 方法不需要加锁，请问 Count() 方法加锁的作用是什么？</div>2021-09-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/83/c9/5d03981a.jpg" width="30px"><span>thomas</span> 👍（0） 💬（1）<div>
 &#47;&#47; count++操作的汇编代码
    MOVQ    &quot;&quot;.count(SB), AX
    LEAQ    1(AX), CX
    MOVQ    CX, &quot;&quot;.count(SB)
============================
count++的汇编码为什么和我go tool compile查看的不同呀？

MOVQ    &quot;&quot;.&amp;count+8(SP), AX
INCQ    (AX)</div>2021-08-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/31/9d/daad92d2.jpg" width="30px"><span>Stony.修行僧</span> 👍（0） 💬（1）<div>二涮 走去，突然发现对go越发着迷</div>2021-07-15</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/59/49/3299e908.jpg" width="30px"><span>Only Once</span> 👍（0） 💬（1）<div>type Counter struct 当中的“CounterType int 和Name string”貌似并没有被引用啊，去掉也能运行；小白一个，请老师赐教</div>2021-03-05</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/cf/93/d31d1938.jpg" width="30px"><span>DukeAnn</span> 👍（0） 💬（2）<div>退出锁是不是用 defer 更好些</div>2020-12-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/5b/66/ad35bc68.jpg" width="30px"><span>党</span> 👍（0） 💬（1）<div>我想做一个数据仓库，用map结构，每个key值是唯一键，每个value是一个结构体，保存具体数据，结构体里加上锁保证数据并发安全，那这个整体的map结构可以不加锁吧，就算并发的增删查，对于同一个key对应的结构体都可以保证完全执行吧。</div>2020-12-04</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1f/bc/9d/eaba20ca.jpg" width="30px"><span>未定义丶</span> 👍（0） 💬（1）<div>作者大大会解答最后的题目吗?</div>2020-11-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/c0/c4/3f7b5eed.jpg" width="30px"><span>悦悦</span> 👍（0） 💬（2）<div>在运行的时候，只有在触发了 data race 之后，才能检测到，如果碰巧没有触发（比如一个 data race 问题只能在 2 月 14 号零点或者 11 月 11 号零点才出现），是检测不出来的。我运行时，开启data race     不太理解，2月14号是检查不出来！</div>2020-10-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/21/fd/47/499339d1.jpg" width="30px"><span>新味道</span> 👍（0） 💬（1）<div>没提到后面文章要用到的信号量？  能否简要的说下go里的信号量作用。 </div>2020-10-16</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1e/e9/34/2eb0c21a.jpg" width="30px"><span>飞沉血</span> 👍（0） 💬（1）<div>打卡，希望自己坚持学完22讲，加油！！！</div>2020-10-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1d/79/3b/93e6fc6d.jpg" width="30px"><span>A😇芳</span> 👍（0） 💬（2）<div>更新快点，课程非常实用</div>2020-10-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/53/db/858337e3.jpg" width="30px"><span>Ethan Liu</span> 👍（0） 💬（2）<div>可以在编译期探测data race吗</div>2020-10-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/1c/cd/8d552516.jpg" width="30px"><span>Gojustforfun</span> 👍（173） 💬（5）<div>等待的goroutine们是以FIFO排队的
1）当Mutex处于正常模式时，若此时没有新goroutine与队头goroutine竞争，则队头goroutine获得。若有新goroutine竞争大概率新goroutine获得。
2）当队头goroutine竞争锁失败1ms后，它会将Mutex调整为饥饿模式。进入饥饿模式后，锁的所有权会直接从解锁goroutine移交给队头goroutine，此时新来的goroutine直接放入队尾。

3）当一个goroutine获取锁后，如果发现自己满足下列条件中的任何一个#1它是队列中最后一个#2它等待锁的时间少于1ms，则将锁切换回正常模式

以上简略翻译自https:&#47;&#47;golang.org&#47;src&#47;sync&#47;mutex.go 中注释Mutex fairness.</div>2020-10-12</li><br/>
</ul>