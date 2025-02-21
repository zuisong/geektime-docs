我在前面用20多篇文章，为你详细地剖析了Go语言本身的一些东西，这包括了基础概念、重要语法、高级数据类型、特色语句、测试方案等等。

这些都是Go语言为我们提供的最核心的技术。我想，这已经足够让你对Go语言有一个比较深刻的理解了。

从本篇文章开始，我们将一起探讨Go语言自带标准库中一些比较核心的代码包。这会涉及这些代码包的标准用法、使用禁忌、背后原理以及周边的知识。

* * *

既然Go语言是以独特的并发编程模型傲视群雄的语言，那么我们就先来学习与并发编程关系最紧密的代码包。

## 前导内容： 竞态条件、临界区与同步工具

我们首先要看的就是`sync`包。这里的“sync”的中文意思是“同步”。我们下面就从同步讲起。

相比于Go语言宣扬的“用通讯的方式共享数据”，通过共享数据的方式来传递信息和协调线程运行的做法其实更加主流，毕竟大多数的现代编程语言，都是用后一种方式作为并发编程的解决方案的（这种方案的历史非常悠久，恐怕可以追溯到上个世纪多进程编程时代伊始了）。

一旦数据被多个线程共享，那么就很可能会产生争用和冲突的情况。这种情况也被称为**竞态条件（race condition）**，这往往会破坏共享数据的一致性。

共享数据的一致性代表着某种约定，即：多个线程对共享数据的操作总是可以达到它们各自预期的效果。
<div><strong>精选留言（30）</strong></div><ul>
<li><img src="" width="30px"><span>Geek_cd5dcf</span> 👍（21） 💬（6）<div>讲的通俗易懂，还是挺好理解的，想问下mutex如果加锁后
mutex.lock（）
defer mutex.unlock（）
在所有场景下都不会出错吗？</div>2018-10-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/ea/80/8759e4c1.jpg" width="30px"><span>🐻</span> 👍（17） 💬（1）<div>1. Locker 接口
2. func (rw *RWMutex) RLocker() Locker</div>2019-03-16</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/82/fb/9d232a7a.jpg" width="30px"><span>Pana</span> 👍（13） 💬（3）<div>如果cpu只有一个核心，是不是就不会产生并发的情况？</div>2020-03-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/37/92/961ba560.jpg" width="30px"><span>授人以🐟，不如授人以渔</span> 👍（8） 💬（4）<div>老师，麻烦分析一下这样的场景：main goroutine 拿到读锁，此时 goroutine 1 试图拿到写锁但被阻塞，紧接着 goroutine 2 试图拿到读锁。我想知道 goroutine 2 为什么也会被阻塞，另外 main goroutine 读锁被释放后，哪个 goroutine 会继续运行？</div>2021-05-07</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/39/fa/a7edbc72.jpg" width="30px"><span>安排</span> 👍（6） 💬（3）<div>goroutine和协程有什么本质区别啊，搜了网上也没看出来啥本质区别，有这方面的资料吗？</div>2019-09-22</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTKOM6tVLSiciaQeQst0g3iboWO74ibicicVAia9qno0X6cf65pEKLgdKkUdcpCWpjAB5e6semrFrruiaGQWhg/132" width="30px"><span>NoTryNoSuccess</span> 👍（5） 💬（3）<div>请问老师，多核心条件下如果两个goroutine底层同时运行在两个线程上，那么此时这两个goroutine实际上是完全并行的。此时它们如果同时进行互斥锁的锁定操作（随后可能同时对同一资源进行写操作）岂不是不能达到对临界区的保护目的了吗？</div>2020-04-04</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/8e/b0/ef201991.jpg" width="30px"><span>CcczzZ</span> 👍（4） 💬（3）<div>老师，有个疑问，文中说的这句：「对读锁进行解锁，只会在没有其他读锁锁定的前提下，唤醒“因试图锁定写锁，而被阻塞的 goroutine”」。
我的理解是，对读锁进行解锁时，此刻若存在其他读锁等待的话，是会优先唤醒读锁的，如果不存在其他等待的读锁，才会唤醒写锁。不知道这样理解是否正确？

而基于上面的理解，我写了段代码测试了一下，发现结果并不是这样，实际情况是：「当读锁进行解锁时，若此刻存在其他的读锁和写锁，会根据他们实际阻塞等待的时间长短，优先唤醒并执行」
就像下面，写锁在前面执行，等待的时间也比读锁场，所以当读锁解锁时，优先唤醒的是等待时间较长的写锁。

func main() {

    var rwMu sync.RWMutex

    &#47;&#47; 模拟多个写&#47;读锁进行阻塞，当释放读锁的时候看谁先获取到锁（会在没有其他读锁的时候，唤醒写锁）

    rwMu.RLock()
    fmt.Println(&quot;start RLock&quot;)

    &#47;&#47; 写
    go func() {
        defer func() {
            rwMu.Unlock()
            fmt.Println(&quot;get UnLock&quot;)
        }()
        rwMu.Lock()
        fmt.Println(&quot;get Lock&quot;)
    }()
    time.Sleep(time.Millisecond * 200)

    &#47;&#47; 读
    go func() {
        defer func() {
            rwMu.RUnlock()
            fmt.Println(&quot;get RUnLock&quot;)
        }()
        rwMu.RLock()
        fmt.Println(&quot;get RLock&quot;)
    }()
    time.Sleep(time.Millisecond * 200)

    rwMu.RUnlock()
    fmt.Println(&quot;start RUnLock&quot;)
    time.Sleep(time.Second * 1)
}

运行结果（等待时间较长的写操作先执行了）：
start RLock
start RUnLock
get Lock
get UnLock
get RLock
get RUnLock</div>2020-01-16</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/c6/f9/caf27bd3.jpg" width="30px"><span>大王叫我来巡山</span> 👍（3） 💬（2）<div>需要请教老师的是，主协程收到信号就被唤醒了，认为可以读了，但是被阻塞的写协程收到锁释放的消息会不会比主协程要早，然后继续获得写的机会，主协程会不会被阻塞？我认为是不会的，此处的锁只是保证了不同写协程互斥的写入，也就是写操作是原子的，但是并不保证读操作一定在写完后就读吧</div>2019-09-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/58/d4/c52f9f6d.jpg" width="30px"><span>芝士老爹</span> 👍（3） 💬（3）<div>如果一直有新的读锁请求，会不会导致写锁锁不了？
还是说如果有了一个wlock锁请求了，现在因为有rlock未释放锁，wlock的协程被阻塞，后面再有新的rlock锁请求也会先被阻塞，等待wlock锁协程先恢复？</div>2019-08-04</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/45/2a/c4413de4.jpg" width="30px"><span>soooldier</span> 👍（2） 💬（1）<div>配套代码里puzzlers&#47;article26下并没有demo58.go，也没有demo59.go，懵圈中。。。</div>2019-05-31</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/43/2d/af86d73f.jpg" width="30px"><span>enjoylearning</span> 👍（1） 💬（1）<div>go本身是不是提供了对死锁的检查？</div>2023-05-05</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/fe/2d/2c9177ca.jpg" width="30px"><span>给力</span> 👍（1） 💬（1）<div>对于使用锁有个疑问：
type Mutex struct {
	state int32
	sema  uint32
}
state表示锁的一个状态

sema这个变量没太理清是做什么的？什么场景下使用</div>2020-03-26</li><br/><li><img src="" width="30px"><span>Geek_da1447</span> 👍（0） 💬（2）<div>老师，请问下sync pool发生inconsistent mutex state问题怎么定位原因？</div>2022-11-07</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/18/50/b1/f9b6b317.jpg" width="30px"><span>黄仲辉</span> 👍（0） 💬（1）<div>同一个goroutine也不能多次执行一个mutex的lock，这是不可重入锁，go为何没有原生实现可重入锁？</div>2022-09-04</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTKELX1Rd1vmLRWibHib8P95NA87F4zcj8GrHKYQL2RcLDVnxNy1ia2geTWgW6L2pWn2kazrPNZMRVrIg/132" width="30px"><span>jxs1211</span> 👍（0） 💬（1）<div>根据执行go run demo58.go -protecting=0的结果来看，go程序运行时调度时机并不是某个goroutine阻塞（即使不阻塞也会可能被P从M上分离），而是有它自己判断机制，对吗，那么他的调度机制是怎么样的呢，是否类似原理的参考资料</div>2021-12-20</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTKELX1Rd1vmLRWibHib8P95NA87F4zcj8GrHKYQL2RcLDVnxNy1ia2geTWgW6L2pWn2kazrPNZMRVrIg/132" width="30px"><span>jxs1211</span> 👍（0） 💬（1）<div>&#47;&#47; 2 只有读的情况下就是用读锁,同时又读写的情况下,就是用读写锁并分别用读锁保护读操作,写锁保护写操作,是这样吗?
	&#47;&#47; 衍生的问题:
		&#47;&#47; 如果只用读锁，保护写操作，是否有什么问题
		&#47;&#47; 读写锁引入了更多的复杂度，是否要结合实际情况确定读写情况下，是否一定要引入读写锁
		&#47;&#47; 是否有一定需要使用读写锁而不适用读锁的场景，可否举例</div>2021-12-20</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTKELX1Rd1vmLRWibHib8P95NA87F4zcj8GrHKYQL2RcLDVnxNy1ia2geTWgW6L2pWn2kazrPNZMRVrIg/132" width="30px"><span>jxs1211</span> 👍（0） 💬（1）<div>1 一个是避免多个线程在同一时刻操作同一个数据块，另一个是协调多个线程，以避免它们在同一时刻执行同一个代码块。这2个描述的区别在哪？</div>2021-12-20</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTKELX1Rd1vmLRWibHib8P95NA87F4zcj8GrHKYQL2RcLDVnxNy1ia2geTWgW6L2pWn2kazrPNZMRVrIg/132" width="30px"><span>jxs1211</span> 👍（0） 💬（1）<div>如果所有写入数据都被读完了，reader是否可能因为读取不到数据返回EOF,而一直无法退出for循环呢
for {
	data, n, err = readConfig.handler()
	if err == nil || err != io.EOF {
	    break
	}
        ....
}</div>2021-10-19</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTKELX1Rd1vmLRWibHib8P95NA87F4zcj8GrHKYQL2RcLDVnxNy1ia2geTWgW6L2pWn2kazrPNZMRVrIg/132" width="30px"><span>jxs1211</span> 👍（0） 💬（1）<div>发现不同goroutine写入操作时可能会写入相同的时间数据：
2021&#47;10&#47;19 22:34:29 writer [2-4]: Oct 19 22:34:29.119490600      (total: 494)
2021&#47;10&#47;19 22:34:29 writer [5-4]: Oct 19 22:34:29.119490600      (total: 520)
以为是因为genWriter中mu.Lock()并没有把产生data的代码包括在临界区中，于是将这行代码加入到mu.Lock()中，但是测试出来的数据还是会写入相同的数据，难道不应该是当一个goroutine获取令牌进入临界区写入数据，其它goroutine等待吗，这个的话怎么会出现不同goroutine写入的时间一样的情况呢，求解</div>2021-10-19</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTKELX1Rd1vmLRWibHib8P95NA87F4zcj8GrHKYQL2RcLDVnxNy1ia2geTWgW6L2pWn2kazrPNZMRVrIg/132" width="30px"><span>jxs1211</span> 👍（0） 💬（1）<div>&#47;&#47; Package sync provides basic synchronization primitives such as mutual
&#47;&#47; exclusion locks. Other than the Once and WaitGroup types, most are intended
&#47;&#47; for use by low-level library routines. Higher-level synchronization is
&#47;&#47; better done via channels and communication.
这段注释中描述的low-level和high-level的区别是指底层和上层吗，这个意思是go底层对并发控制的实现是用的是mutual exclusion locks. 而用户要使用的话推荐还是用channel或者通信的机制吗</div>2021-10-04</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/4f/73/b1db99da.jpg" width="30px"><span>星渊王</span> 👍（0） 💬（1）<div>var sy sync.Mutex

func main() {
	router := gin.Default()

	router.GET(&quot;&#47;&quot;, func(c *gin.Context) {
		num := c.Query(&quot;num&quot;)

		num2,err := strconv.Atoi(num)
		if err != nil {
			c.JSON(200,gin.H{
				&quot;name&quot;:&quot;maogou&quot; + err.Error(),
			})
		}
		demo(num2)
		c.JSON(200,gin.H{
			&quot;name&quot;:&quot;maogou&quot;,
		})
	})

	router.GET(&quot;&#47;demo1&quot;, func(c *gin.Context) {
		sy2 := sy

		fmt.Printf(&quot;%p\n&quot;,&amp;sy)
		fmt.Printf(&quot;%p\n&quot;,&amp;sy2)
		fmt.Println(sy == sy2)
}

最终输出结果
0xa87858
0xc0003060a0
true   不太理解这两个为什么会相等 ? </div>2021-09-30</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/e0/cf/43f201f2.jpg" width="30px"><span>幼儿编程教学</span> 👍（0） 💬（1）<div>郝老师，请教下。
看文章，推荐用defer的方式去解锁。
但，这样的话，锁的范围会大一点。但，好像这是最保险的方法，好像也没办法，是吧？</div>2021-04-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/19/8c/e2/48f4e4fa.jpg" width="30px"><span>mkii</span> 👍（0） 💬（2）<div>老师，如果当前写锁被锁定，解锁时这2者有没有唤醒的优先级。等待读锁的goroutine和等待写锁的goroutine</div>2021-02-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/e8/ed/f9347e5e.jpg" width="30px"><span>松小鼠</span> 👍（0） 💬（3）<div>我用同一把互斥锁，在两个协程里面用，都有对应的加锁解锁操作，另一个协程莫名就阻塞了？咋回事</div>2021-01-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1f/52/3e/f74da7bd.jpg" width="30px"><span>初学者</span> 👍（0） 💬（1）<div>老师，想问下读写锁的读锁和写锁具体操作的内容是什么，比如加读锁的代码块，这段代码块里面的关于读的内容都会被读锁区分出来吗，代码块中的读和写具体指什么呢</div>2020-12-10</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTJSmAhbvPia1msvk91m5rQLTpicY85f2moFMCcAibictL3OeiaaVREadpHN2O3FwicmylwiclTUJJa1peS1Q/132" width="30px"><span>张sir</span> 👍（0） 💬（1）<div>一组临界区是什么场景下会，能举个例子吗？</div>2019-05-05</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/6d/52/404912c3.jpg" width="30px"><span>...</span> 👍（0） 💬（6）<div>老师 go有没有可重入锁的概念</div>2019-02-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/ed/4c/8674b6ad.jpg" width="30px"><span>timmy21</span> 👍（0） 💬（1）<div>郝老师，我使用race进行竞争检测，发现有些变量只有一个写者，一个读者。程序运行没有问题，上锁我担心性能下降，这种情况下需要去上锁吗？</div>2018-10-11</li><br/><li><img src="" width="30px"><span>CBBIOT</span> 👍（0） 💬（1）<div>郝老师你的这个学习群怎么加?有买你的书还没有看，目前还在学基础。</div>2018-10-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/59/c0/6f02c096.jpg" width="30px"><span>属雨</span> 👍（33） 💬（2）<div>第一个问题：
Lock接口。
第二个问题：
变量.Rlock()</div>2018-10-10</li><br/>
</ul>