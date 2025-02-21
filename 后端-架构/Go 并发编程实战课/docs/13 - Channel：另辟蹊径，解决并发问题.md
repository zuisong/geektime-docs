你好，我是鸟窝。

Channel是Go语言内建的first-class类型，也是Go语言与众不同的特性之一。Go语言的Channel设计精巧简单，以至于也有人用其它语言编写了类似Go风格的Channel库，比如[docker/libchan](https://github.com/docker/libchan)、[tylertreat/chan](https://github.com/tylertreat/chan)，但是并不像Go语言一样把Channel内置到了语言规范中。从这一点，你也可以看出来，Channel的地位在编程语言中的地位之高，比较罕见。

所以，这节课，我们就来学习下Channel。

# Channel的发展

要想了解Channel这种Go编程语言中的特有的数据结构，我们要追溯到CSP模型，学习一下它的历史，以及它对Go创始人设计Channel类型的影响。

CSP是Communicating Sequential Process 的简称，中文直译为通信顺序进程，或者叫做交换信息的循序进程，是用来描述并发系统中进行交互的一种模式。

CSP最早出现于计算机科学家Tony Hoare 在1978年发表的[论文](https://www.cs.cmu.edu/~crary/819-f09/Hoare78.pdf)中（你可能不熟悉Tony Hoare这个名字，但是你一定很熟悉排序算法中的Quicksort算法，他就是Quicksort算法的作者，图灵奖的获得者）。最初，论文中提出的CSP版本在本质上不是一种进程演算，而是一种并发编程语言，但之后又经过了一系列的改进，最终发展并精炼出CSP的理论。**CSP允许使用进程组件来描述系统，它们独立运行，并且只通过消息传递的方式通信。**
<div><strong>精选留言（30）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/12/1c/a5/226ce8a7.jpg" width="30px"><span>Noir</span> 👍（13） 💬（5）<div>package main

import &quot;fmt&quot;
import &quot;time&quot;

func main() {
	chArr := [4]chan struct{} {
		make(chan struct{}),
		make(chan struct{}),
		make(chan struct{}),
		make(chan struct{}),
	}

	for i := 0; i &lt; 4; i++ {
		go func(i int) {
			for {
				&lt;- chArr[i % 4]
				fmt.Printf(&quot;i am %d\n&quot;, i)
	
				time.Sleep(1 * time.Second)
				chArr[(i + 1) % 4] &lt;- struct{}{}
			}
		}(i)
	}

	chArr[0] &lt;- struct{}{}
	select{}
}</div>2021-12-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/a9/be/f0b43691.jpg" width="30px"><span>星星之火</span> 👍（4） 💬（3）<div>channel 中包含的 mutex 是什么呢，和课程最开始的 sync.mutex 是同一个东西吗？
因为 sync.mutex 是依赖 channel 实现的，感觉应该不是同一个 mutex？</div>2020-12-05</li><br/><li><img src="" width="30px"><span>Geek_43dc82</span> 👍（2） 💬（3）<div>我实在是太蠢了，只能写出这样的代码了
package main

import &quot;fmt&quot;

func main() {
	signChan1 := make(chan struct{})
	signChan2 := make(chan struct{})
	signChan3 := make(chan struct{})
	signChan4 := make(chan struct{})
	mainSignChan := make(chan struct{})

	for i := 1; i &lt;= 4; i++ {
		go func(i int) {
			for {
				select {
				case &lt;-signChan1:
					fmt.Println(1)
					signChan2 &lt;- struct{}{}
				case &lt;-signChan2:
					fmt.Println(2)
					signChan3 &lt;- struct{}{}
				case &lt;-signChan3:
					fmt.Println(3)
					signChan4 &lt;- struct{}{}
				case &lt;-signChan4:
					fmt.Println(4)
					signChan1 &lt;- struct{}{}
				}
			}
		}(i)
	}
	signChan1 &lt;- struct{}{}
	&lt;-mainSignChan
}
</div>2022-04-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/96/a6/aac2a550.jpg" width="30px"><span>陌</span> 👍（2） 💬（1）<div>Goroutine 泄漏的那个例子，如果把 unbuffered chan 改成容量为 1 的 buffered chan，那么假如函数超时了，子 goroutine 也能够往 channel 中发送数据。那么 GC 会把这个 channel 回收吗?</div>2021-04-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/62/8e/985cbc25.jpg" width="30px"><span>老猫</span> 👍（1） 💬（1）<div>func chgoroutine(in,out,stop chan struct{},n int) {
	for{
		select{
			case  &lt;-in:
				fmt.Println(n)
				time.Sleep(time.Second)
				out &lt;-struct{}{}
			case &lt;-stop:
				return
		}
	}
}

func main() {
	ch1 := make(chan struct{}, 0)
	ch2 := make(chan struct{},0)
	ch3 := make(chan struct{},0)
	ch4 := make(chan struct{},0)
	stop := make(chan struct{},0)

	go chgoroutine(ch1,ch2,stop,1)
	go chgoroutine(ch2,ch3,stop,2)
	go chgoroutine(ch3,ch4,stop,3)
	go chgoroutine(ch4,ch1,stop,4) 

	ch1 &lt;-struct{}{}

	time.Sleep(time.Second * 20)

	stop &lt;-struct{}{}
}</div>2022-01-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/94/19/fa204fdf.jpg" width="30px"><span>滴水穿石</span> 👍（0） 💬（1）<div>package main

import (
	&quot;fmt&quot;
	&quot;strconv&quot;
	&quot;time&quot;
)

func main() {
	var ch = []chan struct{}{
		make(chan struct{}),
		make(chan struct{}),
		make(chan struct{}),
		make(chan struct{}),
	}

	for i := 0; i &lt; 4; i++ {
		go func(i int) {
			for {
				select {
				case &lt;-ch[i]:
					fmt.Println(&quot;Hello world &quot; + strconv.Itoa(i))
				}
			}
		}(i)
	}

	for i := 0; i &lt; 1000; i++ {
		time.Sleep(time.Second)
		chIndex := i % 4
		ch[chIndex] &lt;- struct{}{}
	}

}</div>2024-10-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/e4/ae/7b310c2d.jpg" width="30px"><span>呦呦鹿鸣</span> 👍（0） 💬（1）<div>老师，向一个nil的chan中send数据，我这边测试的结果是死锁，我看文章后面的表格里写的是block：
func main() {
	var c chan int
	c &lt;- 1
}

fatal error: all goroutines are asleep - deadlock!

goroutine 1 [chan send (nil chan)]:
main.main()
</div>2024-09-14</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/IM2JvRB8ibNWib6gc3Wr2QPNDuicfL3TLXU2MiajxSWmyIpRQEfMzUOj3jg54Xy0aAjYhWCefFj1nyQdDoxQkf7Jvg/132" width="30px"><span>Geek_24c089</span> 👍（0） 💬（1）<div>func LoopPrint() {
	n := 4
	cs := make([]chan struct{}, n)

	for i := 0; i &lt; n; i++ {
		c := make(chan struct{})
		cs[i] = c
		go func(i int) {
			for {
				select {
				case &lt;-c:
					fmt.Println(i + 1)
					time.Sleep(time.Second)
					cs[(i+1)%n] &lt;- struct{}{}
				}
			}
		}(i)
	}
	cs[0] &lt;- struct{}{}
	select {}
}</div>2024-07-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/3a/db/791d0f5e.jpg" width="30px"><span>huizhou92</span> 👍（0） 💬（1）<div>func main() {
	wg := sync.WaitGroup{}
	ctx, cancelFunc := context.WithCancel(context.Background())
	f := func(wg *sync.WaitGroup, index int, req, resp chan struct{}) {
		defer wg.Done()
		for {
			select {
			case _ = &lt;-req:
				fmt.Println(fmt.Sprintf(&quot;Hello, World!%d&quot;, index))
				time.Sleep(time.Second * 1)
				resp &lt;- struct{}{}
			case &lt;-ctx.Done():
				return
			}
		}
	}
	chain := make([]chan struct{}, 4)
	for i := 0; i &lt; 4; i++ {
		chain[i] = make(chan struct{}, 1)
	}
	wg.Add(4)
	for i := 0; i &lt; 4; i++ {
		go f(&amp;wg, i+1, chain[i], chain[(i+1)%4])
	}
	chain[0] &lt;- struct{}{}
	&lt;-time.After(time.Second * 20)
	cancelFunc()
	wg.Wait()
}</div>2024-03-01</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/DYAIOgq83erAwcfNMMg2rW4ROTF5icIic4h1OibuicZdxdibQLyXcrwALzmdKNaAGiapQWibXND8x5EIYngtRqHbfE5xQ/132" width="30px"><span>chimission</span> 👍（0） 💬（1）<div>package main

import (
	&quot;fmt&quot;
	&quot;time&quot;
)

func printChan(c chan int) {
	st := &lt;-c
	fmt.Println(st%4 + 1)
	time.Sleep(1 * time.Second)
	c &lt;- st + 1
	go printChan(c)
}

func main() {
	ch := make(chan int, 4)
	ch &lt;- 0
	printChan(ch)

	select {}

}</div>2023-01-07</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/30/d0/20/dc51f8e7.jpg" width="30px"><span>清风</span> 👍（0） 💬（1）<div>func main() {
	chArr := []chan struct{}{
		make(chan struct{}),
		make(chan struct{}),
		make(chan struct{}),
		make(chan struct{}),
		make(chan struct{}),
		make(chan struct{}),
	}
	for k, _ := range chArr {
		if k == len(chArr)-1 {
			go goon(chArr[k], chArr[0], k+1)
		} else {
			go goon(chArr[k], chArr[k+1], k+1)
		}
	}

	chArr[0] &lt;- struct{}{}
	select {}

}

func goon(ch chan struct{}, ch2 chan struct{}, index int) {
	time.Sleep(time.Duration(index*10) * time.Millisecond)
	for {
		&lt;-ch
		fmt.Printf(&quot;I am No %d Goroutine\n&quot;, index)
		time.Sleep(time.Second)
		ch2 &lt;- struct{}{}
	}
}
</div>2022-10-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/79/7d/b573c6d9.jpg" width="30px"><span>张觥</span> 👍（0） 💬（1）<div>func TestChannel1Practice(t *testing.T) {
	var ch = make(chan struct{})
	wg := sync.WaitGroup{}
	wg.Add(4)

	go func() {
		ch &lt;- struct{}{}
	}()

	for thread := 1; thread &lt;= 4; thread++ {
		go func(thead int) {
			_, ok := &lt;-ch
			if ok {
				for i := 1; i &lt;= 4; i++ {
					t.Logf(&quot;%d: %d&quot;, thead, i)
					time.Sleep(1 * time.Second)
				}
				wg.Done()
				ch &lt;- struct{}{}
			}
		}(thread)
	}

	wg.Wait()
	t.Log(&quot;finished&quot;)
}</div>2022-10-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/7b/d1/7eb3b4a4.jpg" width="30px"><span>草色青青</span> 👍（0） 💬（1）<div>func tt(ctx context.Context, c1, c2 *chan int) {
	for {
		select {
		case n := &lt;-*c1:
			fmt.Println(n)
			nn := n + 1
			if n == 4 {
				nn = 1
			}
			*c2 &lt;- nn
			&#47;&#47;fmt.Printf(&quot;c1:%p,c2:%p\n&quot;, c1, c2)
		case &lt;-ctx.Done():
			return

		}
	}
}
func PrintInfo() {
	ctx, cancel := context.WithCancel(context.Background())
	c1, c2, c3, c4 := make(chan int, 2), make(chan int, 2), make(chan int, 2), make(chan int, 2)
	fmt.Printf(&quot;c1:%p,c2:%p,c3:%p,c4:%p\n&quot;, &amp;c1, &amp;c2, &amp;c3, &amp;c4)
	go tt(ctx, &amp;c1, &amp;c2)
	go tt(ctx, &amp;c2, &amp;c3)
	go tt(ctx, &amp;c3, &amp;c4)
	go tt(ctx, &amp;c4, &amp;c1)
	c1 &lt;- 1

	fmt.Println(&quot;Hello, 世界&quot;)
	time.Sleep(time.Millisecond * 70)
	cancel()

	fmt.Println(&quot;Hello, 世界&quot;)
}</div>2022-09-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/e7/a7/9825371e.jpg" width="30px"><span>Penn</span> 👍（0） 💬（1）<div>&#47;&#47; 4个goroutine
	ch1 := make(chan struct{})
	ch2 := make(chan struct{})
	ch3 := make(chan struct{})
	ch4 := make(chan struct{})

	go func() {
		for {
			&lt;-ch1
			fmt.Println(&quot;1&quot;)
			time.Sleep(time.Second)
			ch2 &lt;- struct{}{}
			&#47;&#47; &lt;-ch1
		}
	}()

	go func() {
		for {
			&lt;-ch2
			fmt.Println(&quot;2&quot;)
			time.Sleep(time.Second)
			ch3 &lt;- struct{}{}
		}
	}()

	go func() {
		for {
			&lt;-ch3
			fmt.Println(&quot;3&quot;)
			time.Sleep(time.Second)
			ch4 &lt;- struct{}{}
		}
	}()

	go func() {
		for {
			&lt;-ch4
			fmt.Println(&quot;4&quot;)
			time.Sleep(time.Second)
			ch1 &lt;- struct{}{}
		}
	}()

	ch1 &lt;- struct{}{}
	select {}</div>2021-12-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/55/b6/15cf60cb.jpg" width="30px"><span>石头娃</span> 👍（0） 💬（2）<div>思考题：

func main() {
	var a = make(chan int, 1)
	var b = make(chan int, 1)
	var c = make(chan int, 1)
	var d = make(chan int, 1)
	var e = make(chan string)
	go func() {
		for {
			flag := &lt;-d
			log.Println(1)
			a &lt;- flag
		}
	}()
	go func() {
		for {
			flag := &lt;-a
			log.Println(2)
			b &lt;- flag
		}
	}()
	go func() {
		for {
			flag := &lt;-b
			log.Println(3)
			c &lt;- flag
		}
	}()
	go func() {
		for {
			flag := &lt;-c
			log.Println(4)
			time.Sleep(time.Second)
			d &lt;- flag
		}
	}()
	d &lt;- 1
	&lt;-e
}</div>2020-11-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/17/55/a1/e77b9612.jpg" width="30px"><span>峪五</span> 👍（0） 💬（1）<div>[close通过 close 函数，
可以把 chan 关闭，编译器会替换成 closechan 方法的调用。下面的代码是 close chan 的主要逻辑。如果 chan 为 nil，close 会 panic；如果 chan 已经 closed，再次 close 也会 panic。
否则的话，如果 chan 不为 nil，chan 也没有 closed，就把等待队列中的 sender（writer）和 receiver（reader）从队列中全部移除并唤醒。]
疑问：老师你好，全部移除能明白，为什么要唤醒的？</div>2020-11-15</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/55/47/d217c45f.jpg" width="30px"><span>Panmax</span> 👍（0） 💬（1）<div>recv 的第四部分的描述是不是不太对，这里并没有检查 buf，而是直接检查 sender队列，优先把sender队列中的数据给出去。

原文中写的是「第四部分是处理 sendq 队列中有等待者的情况。这个时候，如果 buf 中有数据，优先从 buf 中读取数据，否则直接从等待队列中弹出一个 sender，把它的数据复制给这个 receiver。」</div>2020-11-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/21/3d/c5/f43fa619.jpg" width="30px"><span>🍀柠檬鱼也是鱼</span> 👍（0） 💬（1）<div>channel底层也使用到了lock，在处理并发写的场景中，这和直接使用mutex.Lock有什么区别呢</div>2020-11-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/c7/67/0077314b.jpg" width="30px"><span>田佳伟</span> 👍（0） 💬（1）<div>func main() {
	ch := make(chan int, 4)
	wg := sync.WaitGroup{}
	for i := 1; i &lt;= 4; i++ {
		wg.Add(1)
		ch&lt;-i
	}
	for i := 1; i &lt;= 4; i++ {
		go func(wg *sync.WaitGroup) {
			a := &lt;-ch
			time.Sleep(time.Second*time.Duration(a))
			fmt.Println(a)
			wg.Done()
		}(&amp;wg)
	}
	wg.Wait()
	close(ch)
	fmt.Println(&quot;finish&quot;)
}</div>2020-11-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/8f/cf/890f82d6.jpg" width="30px"><span>那时刻</span> 👍（0） 💬（1）<div>老师，请问在hchan结构中lock是hchan所有字段中的大锁。是否可以把buf指向的循环队列采用lock free方式，这样lock不需要锁住循环队列相关的变量呢？</div>2020-11-10</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/ajZWFgjupJHhmSN3jJ5o9ibecnOQQmJBTxvjwm5ssJjmG1iaNic8XNR6DvZNwIJdjpjkBibicnJYyZUIAnOkw2wwv8w/132" width="30px"><span>坚白同异</span> 👍（32） 💬（1）<div>思考题
1.
func main() {
	ch1 := make(chan int)
	ch2 := make(chan int)
	ch3 := make(chan int)
	ch4 := make(chan int)
	go func() {
		for {
			fmt.Println(&quot;I&#39;m goroutine 1&quot;)
			time.Sleep(1 * time.Second)
			ch2 &lt;-1 &#47;&#47;I&#39;m done, you turn
			&lt;-ch1
		}
	}()

	go func() {
		for {
			&lt;-ch2
			fmt.Println(&quot;I&#39;m goroutine 2&quot;)
			time.Sleep(1 * time.Second)
			ch3 &lt;-1
		}

	}()

	go func() {
		for {
			&lt;-ch3
			fmt.Println(&quot;I&#39;m goroutine 3&quot;)
			time.Sleep(1 * time.Second)
			ch4 &lt;-1
		}

	}()

	go func() {
		for {
			&lt;-ch4
			fmt.Println(&quot;I&#39;m goroutine 4&quot;)
			time.Sleep(1 * time.Second)
			ch1 &lt;-1
		}

	}()



	select {}
}
2.双向通道可以赋值给单向,反过来不可以.</div>2020-11-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/ab/a9/590d6f02.jpg" width="30px"><span>Junes</span> 👍（16） 💬（5）<div>第一个问题实现的方法有很多，最常规的是用4个channel，我这边分享一个用单channel实现的思路：
因为channel的等待队列是先入先出的，所以我这边取巧地在goroutine前加一个等待时间，保证1~4的goroutine，他们在同个chan阻塞时是有序的

func main() {
	ch := make(chan struct{})
	for i := 1; i &lt;= 4; i++ {
		go func(index int) {
			time.Sleep(time.Duration(index*10) * time.Millisecond)
			for {
				&lt;-ch
				fmt.Printf(&quot;I am No %d Goroutine\n&quot;, index)
				time.Sleep(time.Second)
				ch &lt;- struct{}{}
			}
		}(i)
	}
	ch &lt;- struct{}{}
	time.Sleep(time.Minute)
}</div>2020-11-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/67/dd/55aa6e07.jpg" width="30px"><span>罗帮奎</span> 👍（11） 💬（0）<div>之前使用go-micro时候就遇到过，unbufferd chan导致的goroutine泄露的bug，当时情况是并发压力大导致rpc调用超时，超时退出当前函数导致了goroutine泄露，go-micro有一段类似的使用unbuffered chan的代码，后来改成了buffer=1</div>2020-11-15</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTJWFdKjyLOXtCzowmdCUFHezNlnux4NPWmYsqETjiaHNbnmb7xdzibDncZqP06nNbpN4AhmD76cpicfw/132" width="30px"><span>fhs</span> 👍（11） 💬（0）<div>func f(i int, input &lt;-chan int, output chan&lt;- int) {
	for {
		&lt;-input
		fmt.Println(i)
		time.Sleep(time.Second)
		output &lt;- 1
	}
}
func TestChannelPlan(t *testing.T) {
	c := [4]chan int{}
	for i := range []int{1, 2, 3, 4} {
		c[i] = make(chan int)
	}
	go f(1, c[3], c[0])
	go f(2, c[0], c[1])
	go f(3, c[1], c[2])
	go f(4, c[2], c[3])
	c[3] &lt;- 1
	select {}
}
</div>2020-11-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/31/9d/daad92d2.jpg" width="30px"><span>Stony.修行僧</span> 👍（3） 💬（0）<div>一个 goroutine 可以把数据的“所有权”交给另外一个 goroutine（虽然 Go 中没有“所有权”的概念，但是从逻辑上说，你可以把它理解为是所有权的转移）
这是要推广 Rust啊</div>2020-11-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/21/f9/7d/aafe382c.jpg" width="30px"><span>蜗牛🐌</span> 👍（2） 💬（0）<div>channl1 := make(chan int, 0)
	go func() {
		c := time.NewTicker(1 * time.Second)
		i := 0
		for {
			select {
			case &lt;-c.C:
				i++
				channl1 &lt;- i
				if i == 4 {
					i = 0
				}
			}
		}
	}()
	for {
		select {
		case i := &lt;-channl1:
			fmt.Println(i)
		}
	}</div>2021-01-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1c/d9/a6/c97ecf7d.jpg" width="30px"><span>ldeng 7</span> 👍（2） 💬（0）<div>对于 select 相关实现的源码个人认为还应该讲一下</div>2020-12-02</li><br/><li><img src="" width="30px"><span>taro</span> 👍（1） 💬（0）<div>func main() {
	var chans [N]chan struct{}
	for i := 0; i &lt; N; i++ {
		chans[i] = make(chan struct{})
	}

	for i := 0; i &lt; N; i++ {
		go func(i int) {
			for {
				&lt;- chans[i]
				fmt.Print(i + 1)
				time.Sleep(time.Second)
				chans[(i + 1) % N] &lt;- struct{}{}
			}
		}(i)
	}

	chans[0] &lt;- struct{}{}

	select{}
}</div>2022-12-16</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/19/8e/f0/18720510.jpg" width="30px"><span>50%</span> 👍（1） 💬（0）<div>func main() {
	const n int = 4
	const maxNum int = 100
	ch := make([]chan struct{}, n)
	for i := range ch {
		ch[i] = make(chan struct{})
	}
	wg := sync.WaitGroup{}
	wg.Add(n)
	i := 0
	go func() {
		ch[0] &lt;- struct{}{}&#47;&#47;一个开始的信号
	}()
	for j := 0; j &lt; n; j++ {
		chanNum := (j + 1) % n
		go func() {
			defer wg.Done()
			for {
				&lt;-ch[chanNum]
				fmt.Printf(&quot;i am goroutine %d\n&quot;, chanNum+1)
				fmt.Println(i) &#47;&#47;顺带练习n个goroutine交替打印 0 ~ n
				if i &gt;= math.MaxInt64-1 {
					return
				}
				i++
				time.Sleep(time.Second) &#47;&#47;控制打印速率
				ch[(chanNum+1)%n] &lt;- struct{}{}

			}
		}()
	}
	wg.Wait()
}
</div>2021-05-25</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/rRCSdTPyqWcW6U8DO9xL55ictNPlbQ38VAcaBNgibqaAhcH7mn1W9ddxIJLlMiaA5sngBicMX02w2HP5pAWpBAJsag/132" width="30px"><span>butterfly</span> 👍（1） 💬（2）<div>一直有一个疑问： channel底层也是通过一个mutex保护一个环形队列，这种方式和自己通过mutex方式实现的共享资源访问有什么不一样， 好处是什么，性能有多大差异？</div>2021-02-23</li><br/>
</ul>