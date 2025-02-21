你好，我是Tony Bai。

通过上两节课的学习，我们知道了Go语言实现了基于CSP（Communicating Sequential Processes）理论的并发方案。

Go语言的CSP模型的实现包含两个主要组成部分：一个是Goroutine，它是Go应用并发设计的基本构建与执行单元；另一个就是channel，它在并发模型中扮演着重要的角色。channel既可以用来实现Goroutine间的通信，还可以实现Goroutine间的同步。它就好比Go并发设计这门“武功”的秘籍口诀，可以说，学会在Go并发设计时灵活运用channel，才能说真正掌握了Go并发设计的真谛。

所以，在这一讲中，我们就来系统学习channel这一并发原语的基础语法与常见使用方法。

## 作为一等公民的channel

Go对并发的原生支持可不是仅仅停留在口号上的，Go在语法层面将并发原语channel作为一等公民对待。在前面的[第21讲](https://time.geekbang.org/column/article/460666)中我们已经学过“一等公民”这个概念了，如果你记不太清了可以回去复习一下。

那channel作为一等公民意味着什么呢？

这意味着我们可以**像使用普通变量那样使用channel**，比如，定义channel类型变量、给channel变量赋值、将channel作为参数传递给函数/方法、将channel作为返回值从函数/方法中返回，甚至将channel发送到其他channel中。这就大大简化了channel原语的使用，提升了我们开发者在做并发设计和实现时的体验。
<div><strong>精选留言（30）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/11/70/6d/11ea66f0.jpg" width="30px"><span>peison</span> 👍（24） 💬（6）<div>请问计数信号量的例子中，因为jobs的容量是10，这里执行的循环不会导致阻塞，close(jobs) 应该会被执行到，那么下面的for range为什么不会终止，而可以继续运行？
go func() {
		for i := 0; i &lt; 8; i++ {
			jobs &lt;- (i + 1)
		}
		close(jobs) 
	}()</div>2022-04-15</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/0a/a4/828a431f.jpg" width="30px"><span>张申傲</span> 👍（13） 💬（1）<div>这节课信息量有点大，需要多看几遍好好消化。请问老师一个问题：如果程序中没有手动 close channel，那么 channel 会在什么时候关闭呢？是否需要借助 defer 去释放 channel 资源呢？</div>2022-02-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/29/32/40/d56f476c.jpg" width="30px"><span>ibin</span> 👍（10） 💬（4）<div>白老师，你好，下面这段可以模拟close(groupSignal)
for i := 0;i &lt; 5; i++ {
		groupSignal&lt;-signal(struct{}{})
}
为什么close(groupSignal) 可以给每个groupSignal都发送了{}</div>2022-01-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/29/44/b5/7eba5a0e.jpg" width="30px"><span>木木</span> 👍（8） 💬（1）<div>go的并发原语选择真的是非常精炼：简洁又强大，一个ch就负责了线程通信、同步的多种功能；一个select又实现了对阻塞、非阻塞的控制以及事件循环模式。</div>2022-03-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/d4/d9/c3296187.jpg" width="30px"><span>airmy丶</span> 👍（6） 💬（2）<div>请问下老师: 为什么 &quot;1 对 n 的信号通知机制&quot; 这个例子中，wg.Wait() 一定需要新起一个协程执行呢？而且在本地测试确实只能在新的协程中执行才不会报错，否则会报出: goroutine x [chan receive] 这样的错误。</div>2022-05-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/22/b1/54/6d663b95.jpg" width="30px"><span>瓜牛</span> 👍（5） 💬（2）<div>为啥有时需要手动调用close关闭channel，有时又不需要？</div>2022-04-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/2e/8c/f9/e1dab0ca.jpg" width="30px"><span>怎么睡才能做这种梦</span> 👍（4） 💬（1）<div>另外，select 语句中，如果有多个 case 同时都没有阻塞的话，会随机选择一个 case </div>2023-03-06</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1e/f2/f5/b82f410d.jpg" width="30px"><span>Unknown element</span> 👍（4） 💬（1）<div>老师我看makechan的源码发现分配内存的时候分了3种情况：
1. 缓冲区大小=0 
2. 元素类型不是指针 
3. 元素类型包含指针
我想问下为什么2和3要分成两种情况呢？我看区别好像是调用 mallocgc 时第二个参数不一样，但是mallocgc 的源码我就看不懂了。。。希望老师可以简单解释下 谢谢老师~</div>2022-11-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/54/9a/76c0af70.jpg" width="30px"><span>每天晒白牙</span> 👍（4） 💬（2）<div>感觉只发送channel和只接收channel类型定义符号，交换一下更好理解，也更形象吧

make(chan&lt;- int, 1) 这个代表只接收
make(&lt;-chan int, 1) 这个代表只发送</div>2022-07-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/26/27/eba94899.jpg" width="30px"><span>罗杰</span> 👍（4） 💬（1）<div>这节课比较绕，要静下心好好学习</div>2022-01-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/9d/a4/e481ae48.jpg" width="30px"><span>lesserror</span> 👍（2） 💬（1）<div>Tony bai 老师：

1. 文中：“直到 channel 中有数据可接收或 channel 被关闭循环”，这里的 channel 被关闭循环该怎么理解呢？

2. 文中的提到的“Goroutine 安全”，又该如何理解呢？

3. 还有能不能通俗的解释一下“竞态” 这个概念呀？</div>2023-06-30</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTKfxYdHJ3NNnOzBFu2N6oNPXhfMRibh3nMjneJLN6WCfVStQKLaJNVehUDmcpsj1mIfFegiauToaxbQ/132" width="30px"><span>Geek_640f2c</span> 👍（2） 💬（1）<div>白老师，请问您一个问题
无缓冲的 channel 替代锁那一节，我在 main 的代码中最后输出了 cter.i，但输出结果有时是10，有时却是11，这是什么原因呢？
main代码如下：
func main() {
	cter := NewCounter()
	var wg sync.WaitGroup
	for i := 0; i &lt; 10; i++ {
		wg.Add(1)
		go func(i int) {
			cter.Increase()
			fmt.Printf(&quot;goroutine-%d: current counter value is %d\n&quot;, i, v)
			wg.Done()
		}(i)
	}
	wg.Wait()
	println(cter.i)
}</div>2023-03-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/32/45/b2/24dee83c.jpg" width="30px"><span>Ppppppp</span> 👍（2） 💬（1）<div>for range对于channel会产生pop的效果吗？感觉好像跟对待slice和map不太一样。</div>2023-02-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/2e/8c/f9/e1dab0ca.jpg" width="30px"><span>怎么睡才能做这种梦</span> 👍（2） 💬（1）<div>满满的干货呀，感谢白老，希望老师能出进阶专栏，我一定买</div>2023-02-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/43/c6/0ba36190.jpg" width="30px"><span>knightjdq</span> 👍（2） 💬（1）<div>白老师好：请教下用于替代锁机制中的代码，十分感谢!
func NewCounter() *counter {
	cter := &amp;counter{
		c: make(chan int),
	}
	go func() {
		for {
			cter.i++
			cter.c &lt;- cter.i
		}
	}()
	return cter
}
这里的死循环，i++写入channel后阻塞，Increase函数来读取，for循环到9后，不再读取，channel阻塞，那死循环的groutine呢？在counter对象销毁后就停止执行了是么？</div>2022-11-25</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/3d/70/3d8aa6fc.jpg" width="30px"><span>小虎</span> 👍（2） 💬（1）<div>“无缓冲 channel 替代锁”这个示例说到“这种并发设计逻辑更符合 Go 语言所倡导的“不要通过共享内存来通信，而是通过通信来共享内存”的原则。”，没太想明白为什么符合这个原则，goroutine 中调用了cter.Increase()，这不是共享了cter这个变量吗？</div>2022-07-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/16/48/01567df1.jpg" width="30px"><span>郑泽洲</span> 👍（2） 💬（1）<div>这节课需要反复读，举的例子和示例代码都非常好，值得深入思考，只要思考到位，对channel认识就能加深一步👍🏻</div>2022-02-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/53/a8/abc96f70.jpg" width="30px"><span>return</span> 👍（2） 💬（1）<div>太干了，看了几天才看完， 面面俱到了， 各种坑也指点出来了。
收获非常大， 从瞎用channel，到现在 心里有底，知道该怎么用channel了。
非常感谢老师，老师讲的太赞了。
</div>2022-01-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/9d/a4/e481ae48.jpg" width="30px"><span>lesserror</span> 👍（2） 💬（1）<div>channel是Go并发设计的核心之一，要反复阅读理解。大白老师这里总结的很不错。有以下疑问，麻烦解答。

1. 无缓冲 channel 的惯用法 -&gt; 第一种用法：用作信号传递 。下面的示例代码： c &lt;- signal(struct{}{}) 改成 c &lt;- signal{}  会不会更好一些呢？

2. 无缓冲channel替代锁那里。计数器操作全部交给一个独立的 Goroutine 去处理。我的理解是这个Goroutine 其实最后还是处于阻塞的状态下。最后主 Goroutine 结束运行了。这个Goroutine 不得不退出了，这么理解对吗？</div>2022-01-16</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/18/75/bc/89d88775.jpg" width="30px"><span>Calvin</span> 👍（2） 💬（5）<div>请教下，文章中说到“select 这种判空或判满的方法适用于大多数场合，但是这种方法有一个“问题”，那就是它改变了 channel 的状态，会让 channel 接收了一个元素或发送一个元素到 channel。”，怎样理解这句话？为什么“会让 channel 接收了一个元素或发送一个元素到 channel”呢？</div>2022-01-13</li><br/><li><img src="" width="30px"><span>0mfg</span> 👍（2） 💬（5）<div>白老师好，请教个问题。对于无缓冲通道的结论，“对无缓冲 channel 类型的发送与接收操作，一定要放在两个不同的 Goroutine 中进行，否则会导致 deadlock。” 尝试了如下写法，发送在主goroutine，接收在新goroutine发现还是deadlock，请问具体原因是啥？谢谢

package main

import &quot;fmt&quot;

func main()  {
	ch := make(chan int)
	ch &lt;- 13
	go func() {
		n := &lt;- ch
		fmt.Println(n)
	}()
}</div>2022-01-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/18/7b/03/03583011.jpg" width="30px"><span>天天有吃的</span> 👍（1） 💬（1）<div>直接看，确实有点看不懂...</div>2023-05-09</li><br/><li><img src="" width="30px"><span>陈鹤</span> 👍（1） 💬（1）<div>这节课信息量巨大，被各种应用场景的奇思妙想震惊到了！个人觉得是本教程偏向应用最重要的一个章节，示例丰富，可以直接当模板应用，常看常新！</div>2023-04-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/21/95/f4/06442207.jpg" width="30px"><span>momo</span> 👍（1） 💬（1）<div>狂赞</div>2022-12-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/2e/35/c12029fd.jpg" width="30px"><span>fengruichao</span> 👍（1） 💬（1）<div>func test1() {
	ch1 := make(chan int)
	ch1 &lt;- 1
	go func() {
		fmt.Println(&lt;-ch1)
	}()
}

为什么把接收操作放在Goroutine会报fatal error: all goroutines are asleep - deadlock!,而把发送操作放到Goroutine中就不会报错</div>2022-09-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/56/4e/9291fac0.jpg" width="30px"><span>Jay</span> 👍（1） 💬（1）<div>
func worker() {
  heartbeat := time.NewTicker(30 * time.Second)
  defer heartbeat.Stop()
  for {
    select {
    case &lt;-c:
      &#47;&#47; ... do some stuff
    case &lt;- heartbeat.C:
      &#47;&#47;... do heartbeat stuff
    }
  }
}

老师，最后这段代码我没太明白，select如果没有default的话，不可发送和不可接受都会处于阻塞，状态，select本身不是会一直等待吗（select本身看起来像是个循环等待啊），外面的for循环有什么意义呢</div>2022-09-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/c0/24/01699070.jpg" width="30px"><span>Jack Xin</span> 👍（1） 💬（1）<div>白老师，想问您一个问题，关于无缓冲chan 的第二种用法：替换锁机制。我复制里面的例子在我的Mac上运行得到的是下面的结果，跟您的不一样，不是v=i+1的关系，想了半天也不知道为什么，我用的1.18版本的go，
goroutine-0: current counter value is 1
goroutine-1: current counter value is 9
goroutine-9: current counter value is 3
goroutine-5: current counter value is 4
goroutine-6: current counter value is 5
goroutine-7: current counter value is 6
goroutine-8: current counter value is 7
goroutine-2: current counter value is 8
goroutine-4: current counter value is 2
goroutine-3: current counter value is 10</div>2022-09-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/19/2e/ca/469f7266.jpg" width="30px"><span>菠萝吹雪—Code</span> 👍（1） 💬（1）<div>这节课解决了我很多疑惑，代码自己敲了一遍，一行一行分析，有感觉了。</div>2022-09-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1b/8c/60/58b6c39e.jpg" width="30px"><span>zzy</span> 👍（1） 💬（1）<div>在 1 对 n 的信号通知 的代码中，并没有看到向groupSingal中发送值，接收端不是应该一直阻塞吗？感觉没法走下去</div>2022-07-31</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/19/67/97/96e3f59b.jpg" width="30px"><span>fgr_SHU</span> 👍（1） 💬（1）<div>2s 后，ch2 被写入了一个数值 7。这样在某一轮 select 的过程中，分支case x := &lt;-ch2被选中得以执行，程序输出 7 之后满足退出条件，于是程序终止

具体是哪一轮呢？</div>2022-07-19</li><br/>
</ul>