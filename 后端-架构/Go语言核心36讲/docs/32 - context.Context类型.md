我们在上篇文章中讲到了`sync.WaitGroup`类型：一个可以帮我们实现一对多goroutine协作流程的同步工具。

**在使用`WaitGroup`值的时候，我们最好用“先统一`Add`，再并发`Done`，最后`Wait`”的标准模式来构建协作流程。**

如果在调用该值的`Wait`方法的同时，为了增大其计数器的值，而并发地调用该值的`Add`方法，那么就很可能会引发panic。

这就带来了一个问题，如果我们不能在一开始就确定执行子任务的goroutine的数量，那么使用`WaitGroup`值来协调它们和分发子任务的goroutine，就是有一定风险的。一个解决方案是：分批地启用执行子任务的goroutine。

## 前导内容：WaitGroup值补充知识

我们都知道，`WaitGroup`值是可以被复用的，但需要保证其计数周期的完整性。尤其是涉及对其`Wait`方法调用的时候，它的下一个计数周期必须要等到，与当前计数周期对应的那个`Wait`方法调用完成之后，才能够开始。

我在前面提到的可能会引发panic的情况，就是由于没有遵循这条规则而导致的。

只要我们在严格遵循上述规则的前提下，分批地启用执行子任务的goroutine，就肯定不会有问题。具体的实现方式有不少，其中最简单的方式就是使用`for`循环来作为辅助。这里的代码如下：
<div><strong>精选留言（30）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/12/7e/05/431d380f.jpg" width="30px"><span>拂尘</span> 👍（8） 💬（4）<div>@郝老师 有几点疑问烦劳回答下，谢谢！
1、在coordinateWithContext的例子中，总共有12个子goroutine被创建，第12个即最后一个子goroutine在运行结束时，会通过计算defer表达式从而触发cancelFunc的调用，从而通知主goroutine结束在ctx.Done上获取通道的接收等待。我的问题是，在第12个子goroutine计算defer表达式的时候，会不会存在if条件不满足，未执行到cancelFunc的情况？或者说，在此时，第1到第11的子goroutine中，会存在自旋cas未执行完的情况吗？如果这种情况有，是否会导致主goroutine永远阻塞的情况？
2、在撤销函数被调用的时候，在当前context上，通过contex.Done获取的通道会马上感知到吗？还是会同步等待，使撤销信号在当前context的所有subtree上的所有context传播完成后，再感知到？还是有其他情况？
3、WithDeadline和WithTimeout的区别是什么？具体说，deadline是针对某个具体时间，而timeout是针对当前时间的延时来定义自动撤销时间吗？
感谢回复！</div>2020-09-05</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/4a/d4/a3231668.jpg" width="30px"><span>Shawn</span> 👍（8） 💬（1）<div>看代码是深度优先，但是我自己写了demo，顺序是乱的，求老师讲解</div>2018-10-25</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/1a/3c/60b12211.jpg" width="30px"><span>mclee</span> 👍（4） 💬（4）<div>
实测了下，context.WithValue 得到的新的 ctx 当其 parent context cancle 时也能收到 done 信号啊，并不是文中说的那样会跳过！

package main

import (
	&quot;context&quot;
	&quot;fmt&quot;
	&quot;time&quot;
)

func main() {
	ctx1, cancelFun := context.WithCancel(context.Background())
	ctx2 := context.WithValue(ctx1, &quot;&quot;, &quot;&quot;)
	ctx3, _ := context.WithCancel(ctx1)

	go watch(ctx1, &quot;ctx1&quot;)
	go watch(ctx2, &quot;ctx2&quot;)
	go watch(ctx3, &quot;ctx3&quot;)

	time.Sleep(2 * time.Second)
	fmt.Println(&quot;可以了，通知监控停止&quot;)
	cancelFun()

	&#47;&#47;为了检测监控过是否停止，如果没有监控输出，就表示停止了
	time.Sleep(5 * time.Second)

}

func watch(ctx context.Context, name string) {
	for {
		select {
		case &lt;-ctx.Done():
			fmt.Println(name,&quot;监控退出，停止了...&quot;)
			return
		default:
			fmt.Println(name,&quot;goroutine监控中...&quot;)
			time.Sleep(2 * time.Second)
		}
	}
}
</div>2022-02-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/15/0f/954be2db.jpg" width="30px"><span>茴香根</span> 👍（4） 💬（1）<div>留言区很多人说Context 是深度优先，但是我在想每个goroutine 被调用的顺序都是不确定的，因此在编写goroutine 代码时，实际的撤销响应不能假定其父或子context 所在的goroutine一定先或者后结束。</div>2019-07-25</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/bd/68/3fd6428d.jpg" width="30px"><span>Cutler</span> 👍（4） 💬（3）<div>cotext.backround()和cotext.todo()有什么区别</div>2019-04-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/b1/20/8718252f.jpg" width="30px"><span>鲲鹏飞九万里</span> 👍（1） 💬（1）<div>老师，您还能看到我的留言吗，现在已经是2023年了。您看我下面的代码，比您的代码少了一句time.Sleep(time.Millisecond * 200)， 之后，打印的结果就是错的，只打印了12个数，您能给解释一下吗。（我运行环境是：go version go1.18.3 darwin&#47;amd64， 2.3 GHz 四核Intel Core i5）
func main() {
	&#47;&#47; coordinateWithWaitGroup()
	coordinateWithContext()
}

func coordinateWithContext() {
	total := 12
	var num int32
	fmt.Printf(&quot;The number: %d [with context.Context]\n&quot;, num)
	cxt, cancelFunc := context.WithCancel(context.Background())
	for i := 1; i &lt;= total; i++ {
		go addNum(&amp;num, i, func() {
			&#47;&#47; 如果所有的addNum函数都执行完毕，那么就立即分发子任务的goroutine
			&#47;&#47; 这里分发子任务的goroutine，就是执行 coordinateWithContext 函数的goroutine.
			if atomic.LoadInt32(&amp;num) == int32(total) {
				&#47;&#47; &lt;-cxt.Done() 针对该函数返回的通道进行接收操作。
				&#47;&#47; cancelFunc() 函数被调用，针对该通道的接收会马上结束。
				&#47;&#47; 所以，这样做就可以实现“等待所有的addNum函数都执行完毕”的功能
				cancelFunc()
			}
		})
	}
	&lt;-cxt.Done()
	fmt.Println(&quot;end.&quot;)
}

func addNum(numP *int32, id int, deferFunc func()) {
	defer func() {
		deferFunc()
	}()
	for i := 0; ; i++ {
		currNum := atomic.LoadInt32(numP)
		newNum := currNum + 1
		&#47;&#47; time.Sleep(time.Millisecond * 200)
		if atomic.CompareAndSwapInt32(numP, currNum, newNum) {
			fmt.Printf(&quot;The number: %d [%d-%d]\n&quot;, newNum, id, i)
			break
		} else {
			fmt.Printf(&quot;The CAS option failed. [%d-%d]\n&quot;, id, i)
		}
	}
}

运行的结果为：
$ go run demo01.go
The number: 0 [with context.Context]
The number: 1 [12-0]
The number: 2 [1-0]
The number: 3 [2-0]
The number: 4 [3-0]
The number: 5 [4-0]
The number: 6 [9-0]
The number: 7 [10-0]
The number: 8 [11-0]
The number: 10 [6-0]
The number: 11 [5-0]
The number: 9 [8-0]
end.


</div>2023-01-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/52/bb/225e70a6.jpg" width="30px"><span>hunterlodge</span> 👍（1） 💬（1）<div>“由于Context类型实际上是一个接口类型，而context包中实现该接口的所有私有类型，都是基于某个数据类型的指针类型，所以，如此传播并不会影响该类型值的功能和安全。”
请问老师，这句话中的「所以」二字怎么理解呢？指针不是会导致数据共享和竞争吗？为什么反而是安全的呢？谢谢！</div>2021-05-05</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/62/dc/8876c73b.jpg" width="30px"><span>moooofly</span> 👍（1） 💬（2）<div>“它会向它的所有子值（或者说子节点）传达撤销信号。这些子值会如法炮制，把撤销信号继续传播下去。最后，这个 Context 值会断开它与其父值之间的关联。”--这里有一个问题，我能理解，当在这个上下文树上的某个 node 上触发 cancel 信号时，以该 node 为根的子上下文树会从原来的树上断开；而文中又提到“撤销信号在被传播时，若遇到它们（调用 context.WithValue 函数得到的 Context 值）则会直接跨过” ，那么，这些被“跨过”的 node ，在上面说的子上下文树断开的过程里，是一起断开了？还是仍旧会和更上层的 node 节点有关联？</div>2019-09-30</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/ce/b2/1f914527.jpg" width="30px"><span>海盗船长</span> 👍（1） 💬（1）<div>实际使用中 http.ReverseProxy经常会报 proxy error：context canceled 请问老师有哪些原因可能导致这个问题</div>2019-09-02</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/75/aa/21275b9d.jpg" width="30px"><span>闫飞</span> 👍（1） 💬（1）<div>繁衍一词的翻译有些生硬，是否能换一个好理解一些的中文词汇</div>2019-07-16</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1f/75/d0/7c0f85bf.jpg" width="30px"><span>尚恩</span> 👍（0） 💬（1）<div>老师，你的图是用什么工具画的？
</div>2024-02-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/22/08/3b/6fbc7ea0.jpg" width="30px"><span>寻风</span> 👍（0） 💬（1）<div>Context可以看作是某个父goroutine的一个变量,并且这个变量是线程安全的, 当这个变量传入子的goroutine后, 就意味着父goroutine和子goroutine可以通过这个变量来进行信息交互?
或者Context是一个独立申请的的内存区域, 父goroutine和子goroutine都有一个指针指向它, 这样就可以通过这块共享的内存进行信息交互了?
</div>2022-05-11</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTKELX1Rd1vmLRWibHib8P95NA87F4zcj8GrHKYQL2RcLDVnxNy1ia2geTWgW6L2pWn2kazrPNZMRVrIg/132" width="30px"><span>jxs1211</span> 👍（0） 💬（1）<div>coordinateWithContext中，如果改成WithTimeout创建ctx的话，主goroutine只要&lt;-ctx.Done()接收到挂壁通道的信号后就会立马解除阻塞，而执行退出，这个时候即使for中的子goroutine还没有执行完成也会被强制退出了，这样情况下某个子goroutine执行到一半的时候，会被‘中断’，感觉上没有得到公平的对待，个人理解的cpu在goroutine中调度，如果足够公平的话，至少要在等到当前执行的goroutine阻塞而让出cpu，才切到其他goroutine执行，还是我理解错了，cpu就是不停的在各个goroutine间切来来去的执行，而不管某个goroutine有没有阻塞</div>2021-11-23</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTKELX1Rd1vmLRWibHib8P95NA87F4zcj8GrHKYQL2RcLDVnxNy1ia2geTWgW6L2pWn2kazrPNZMRVrIg/132" width="30px"><span>jxs1211</span> 👍（0） 💬（2）<div>waitgroup的改进版中，每批就是一个wg的技术周期，当前循环的计数周期没有完成，下一次不会开始，也就是说每stride这么多个个goroutine执行完成之前，是不会开起下一批goroutine的，这样的话，其实每一批之间是串行的，并不是并发total那么多goroutine，而是只并发了stride个goroutine，对吗？</div>2021-11-20</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTKELX1Rd1vmLRWibHib8P95NA87F4zcj8GrHKYQL2RcLDVnxNy1ia2geTWgW6L2pWn2kazrPNZMRVrIg/132" width="30px"><span>jxs1211</span> 👍（0） 💬（1）<div>func defaultCompareAndSwapInt32(addr *int32, old, new int32) (swapped bool) {
	if old != *addr {
		return false
	}
	*addr = new
	return true
}
这是我自己写的一个没有原子操作的defaultCompareAndSwapInt32，替换atomic.CompareAndSwapInt32，total := 120，测试的数据好像没有错乱，每个goroutine的交换都是都是递增的，是我理解错了吗
added from 0 to 1 --2 
added from 1 to 2 --4 
added from 2 to 3 --3 
added from 3 to 4 --5 
added from 4 to 5 --6 
added from 5 to 6 --7 
added from 6 to 7 --9 
added from 7 to 8 --8 
added from 8 to 9 --10 
added from 9 to 10 --11 
added from 10 to 11 --12 
added from 11 to 12 --13 
added from 12 to 13 --15 
added from 13 to 14 --14 
added from 14 to 15 --16 
added from 15 to 16 --18 
added from 16 to 17 --17 
added from 17 to 18 --19 
added from 18 to 19 --20 
added from 19 to 20 --22 
added from 20 to 21 --21 
added from 21 to 22 --23 
added from 22 to 23 --24 
added from 23 to 24 --25 
added from 24 to 25 --27 
added from 25 to 26 --28 
added from 26 to 27 --26 
。。。。
added from 83 to 84 --85 
added from 84 to 85 --87 
added from 85 to 86 --86 
added from 86 to 87 --88 
added from 87 to 88 --89 
added from 88 to 89 --91 
added from 89 to 90 --90 
added from 90 to 91 --93 
added from 91 to 92 --94 
added from 92 to 93 --92 
added from 93 to 94 --96 
added from 94 to 95 --97 
added from 95 to 96 --95 
added from 96 to 97 --98 
added from 97 to 98 --99 
added from 98 to 99 --100 
added from 99 to 100 --103 
added from 100 to 101 --101 
added from 101 to 102 --102 
added from 102 to 103 --104 
added from 103 to 104 --105 
added from 104 to 105 --106 
added from 105 to 106 --107 
added from 106 to 107 --108 
added from 107 to 108 --109 
added from 108 to 109 --112 
added from 109 to 110 --110 
added from 110 to 111 --111 
added from 111 to 112 --114 
added from 112 to 113 --113 
added from 113 to 114 --115 
added from 114 to 115 --117 
added from 115 to 116 --118 
added from 116 to 117 --116 
added from 117 to 118 --120 
added from 118 to 119 --119 
added from 119 to 120 --121 
</div>2021-10-26</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTKELX1Rd1vmLRWibHib8P95NA87F4zcj8GrHKYQL2RcLDVnxNy1ia2geTWgW6L2pWn2kazrPNZMRVrIg/132" width="30px"><span>jxs1211</span> 👍（0） 💬（1）<div>把old := atomic.LoadInt32(num)
改成old := *num这样在没有防中断的情况下取值，实际测试了一些数据，没有出现错乱的情况，都能顺序递增（如下),这样是否存在线程不安全的情况，运行时间足够长是否就会出现数据错乱的情况
added from 201 to 202 --5
add failed from 201 to 202 --4
add failed from 201 to 202 --6
added from 202 to 203 --6
add failed from 202 to 203 --4
added from 203 to 204 --4
added from 204 to 205 --6
add failed from 204 to 205 --5
add failed from 204 to 205 --4
added from 205 to 206 --4
add failed from 205 to 206 --5
added from 206 to 207 --5
added from 207 to 208 --4
add failed from 207 to 208 --5
add failed from 207 to 208 --6
added from 208 to 209 --6
add failed from 208 to 209 --5
added from 209 to 210 --5
added from 210 to 211 --4
add failed from 210 to 211 --5
add failed from 210 to 211 --6
added from 211 to 212 --6
add failed from 211 to 212 --5
added from 212 to 213 --5
added from 213 to 214 --5
add failed from 213 to 214 --6
add failed from 213 to 214 --4
</div>2021-10-26</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/DYAIOgq83er3buhru0LAs0WQZh9vdDk8P6duwdEIxvTwLTviasadOcP5nlKOjKlKJicNV2QHa9qSIxwUQoYhhYBg/132" width="30px"><span>Geek_74baaf</span> 👍（0） 💬（1）<div>老师，能请问一下backGround和TODO两种类型的具体又什么区别吗，如果方便的话，可不可以麻烦您举个小例子说明一下，看文档实在看的一愣一愣的</div>2021-09-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/17/4a/53/063f9d17.jpg" width="30px"><span>moonfox</span> 👍（0） 💬（1）<div>建议打开源码文件，一边阅读，一边看源码文件，利于理解</div>2021-05-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/2d/18/918eaecf.jpg" width="30px"><span>后端进阶</span> 👍（0） 💬（1）<div>context包其实相当于Java的同步工具类，比如cancelFunc其实就是一个countDownLatch</div>2019-07-04</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/80/b5/f59d92f1.jpg" width="30px"><span>Cloud</span> 👍（114） 💬（4）<div>还没用过context包的我看得一愣一愣的</div>2018-10-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/51/cb/c8b42257.jpg" width="30px"><span>Spike</span> 👍（62） 💬（0）<div>https:&#47;&#47;blog.golang.org&#47;pipelines
https:&#47;&#47;blog.golang.org&#47;context
要了解context的来源和用法，建议先阅读官网的这两篇blog
</div>2018-12-05</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/15/51/223b6e04.jpg" width="30px"><span>勉才</span> 👍（40） 💬（0）<div>context 树不难理解，context.Background 是根节点，但它是个空的根节点，然后通过它我们可以创建出自己的 context 节点，在这个节点之下又可以创建出新的 context 节点。看了 context 的实现，其实它就是通过一个 channel 来实现，cancel() 就是关闭该管道，context.Done() 在 channel 关闭后，会返回。替我们造的轮子主要实现两个功能：1. 加锁，实现线程安全；2. cancel() 会将本节点，及子节点的 channel 都关闭。</div>2019-01-01</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/3d/6e/60680aa4.jpg" width="30px"><span>Li Yao</span> 👍（37） 💬（1）<div>如果能举一个实际的应用场景就更好了，这篇看不太懂用途</div>2018-11-16</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/b4/30/d929bf57.jpg" width="30px"><span>丁香与茉莉</span> 👍（22） 💬（3）<div>http:&#47;&#47;www.flysnow.org&#47;2017&#47;05&#47;12&#47;go-in-action-go-context.html</div>2018-11-30</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/ac/95/9b3e3859.jpg" width="30px"><span>Timo</span> 👍（16） 💬（0）<div>Context 使用原则
不要把Context放在结构体中，要以参数的方式传递
以Context作为参数的函数方法，应该把Context作为第一个参数，放在第一位。
给一个函数方法传递Context的时候，不要传递nil，如果不知道传递什么，就使用context.TODO
Context的Value相关方法应该传递必须的数据，不要什么数据都使用这个传递
Context是线程安全的，可以放心的在多个goroutine中传递</div>2019-05-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/aa/53/62b5c104.jpg" width="30px"><span>郝林</span> 👍（7） 💬（5）<div>我看不少读者都说写一篇难理解。可能的确如此，因为我假设你们已对context包有基本的了解。

不过没关系，你们有此方面的任何问题都可以通过以下三个途径与我讨论：

1. 直接在专栏文章下留言；
2. 在 GoHackers 微信群或者 BearyChat 中的 GoHackers 团队空间里艾特我；
3. 在知识星球中的 GoHackers VIP 社群里向我提问。</div>2019-04-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/18/07/9f5f5dd3.jpg" width="30px"><span>憶海拾貝</span> 👍（7） 💬（0）<div>服务间调用通常要传递上下文数据，用带值Context在每个函数间传递是一种方式，但从Python过来的我觉得这对代码侵入性蛮大的。请问go中还有什么更好的办法传递上下文数据呢？</div>2018-11-15</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1a/6d/89/14031273.jpg" width="30px"><span>Direction</span> 👍（5） 💬（0）<div>在 Go 服务中，每个传入的请求都在它自己的 goroutine 中处理。请求处理程序通常启动额外的 goroutine 来访问后端，如数据库和 RPC 服务。
  处理请求的 goroutine 集通常需要访问特定于请求的值，例如最终用户的身份、授权令牌和请求的截止日期。当一个请求被取消或超时时（cancelFunc() or WithTimeout()），处理该请求的所
  有 goroutines 应该快速退出(ctx.Done（）)，以便系统可以回收（reclaim）它们正在使用的任何资源。

感觉这个举例挺好的（参考至：https:&#47;&#47;blog.golang.org&#47;context）</div>2020-10-22</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/Q3auHgzwzM6iagw7ct4ca3niaSEFNicu2wy2KuCibO6eiaRzoRGJb50WTrbkKQib9mTArnTr8jJUazO9O2ibLZNfjjl35cfCHkBPs7N/132" width="30px"><span>Geek_f39659</span> 👍（5） 💬（0）<div>根据这句话：“A great mental model of using Context is that it should flow through your program. Imagine a river or running water. This generally means that you don’t want to store it somewhere like in a struct. Nor do you want to keep it around any more than strictly needed. Context should be an interface that is passed from function to function down your call stack, augmented as needed.”

感觉上Context设计上更像是一个运行时的动态概念，它更像是代表传统call stack 层层镶套外加分叉关系的那颗树。代表着运行时态的调用树。所以它最好就是只存在于函数体的闭包之中，大家口口相传，“传男不传女”。“因为我调用你，所以我才把这个传给你，你可以传给你的子孙，但不要告诉别人！”。所以最好不要把它保存起来让旁人有机会看得到或用到。

楼上有人提到这种风格的入侵性，我能理解你的感觉。但以我以前玩Node.js中的cls (continuation local storage)踩过的那些坑来看，我宁愿两害相权取其轻。这种入侵性至少是可控的，显式的。同步编程的世界我们只需要TLS(Thread local storage)就好了，但对应的异步编程的世界里玩cls很难搞的。在我来看，Context显然是踩过那些坑的老鸟搞出来的。</div>2019-11-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/59/c0/6f02c096.jpg" width="30px"><span>属雨</span> 👍（3） 💬（0）<div>深度优先，看func (c *cancelCtx) cancel(removeFromParent bool, err error)方法的源代码。</div>2018-10-25</li><br/>
</ul>