你好，我是鸟窝。

前一讲，我介绍了Channel的基础知识，并且总结了几种应用场景。这一讲，我将通过实例的方式，带你逐个学习Channel解决这些问题的方法，帮你巩固和完全掌握它的用法。

在开始上课之前，我先补充一个知识点：通过反射的方式执行select语句，在处理很多的case clause，尤其是不定长的case clause的时候，非常有用。而且，在后面介绍任务编排的实现时，我也会采用这种方法，所以，我先带你具体学习下Channel的反射用法。

# 使用反射操作Channel

select语句可以处理chan的send和recv，send和recv都可以作为case clause。如果我们同时处理两个chan，就可以写成下面的样子：

```
    select {
    case v := <-ch1:
        fmt.Println(v)
    case v := <-ch2:
        fmt.Println(v)
    }
```

如果需要处理三个chan，你就可以再添加一个case clause，用它来处理第三个chan。可是，如果要处理100个chan呢？一万个chan呢？

或者是，chan的数量在编译的时候是不定的，在运行的时候需要处理一个slice of chan，这个时候，也没有办法在编译前写成字面意义的select。那该怎么办？

这个时候，就要“祭”出我们的反射大法了。

通过reflect.Select函数，你可以将一组运行时的case clause传入，当作参数执行。Go的select是伪随机的，它可以在执行的case中随机选择一个case，并把选择的这个case的索引（chosen）返回，如果没有可用的case返回，会返回一个bool类型的返回值，这个返回值用来表示是否有case成功被选择。如果是recv case，还会返回接收的元素。Select的方法签名如下：
<div><strong>精选留言（30）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/11/2b/02/7ef138a0.jpg" width="30px"><span>润豪</span> 👍（11） 💬（2）<div>channel 来实现互斥锁，优势是 trylock，timeout 吧，因为mutex 没有这些功能。否则的话，是不是用回 mutex 呢</div>2020-11-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/a1/9a/73c7b6c8.jpg" width="30px"><span>茶澜子</span> 👍（5） 💬（5）<div>老师好，我在测试扇出的例子的时候，在异步运行的时候出现了 panic: send on closed channel 的错误

&#47;&#47; 扇出模式 
func FunOut(ch &lt;-chan int, n int, async bool) []chan int {
	var outs []chan int
	for i := 0; i &lt; n; i++ {
		outs = append(outs, make(chan int))
	}

	go func() {
		defer func() {
			for i := 0; i &lt; len(outs); i++ {
				close(outs[i])
			}
		}()

		for v := range ch {
			v := v
			for i := 0; i &lt; n; i++ {
				i := i
				if async {
					go func() {
						outs[i] &lt;- v
					}()
				} else {
					outs[i] &lt;- v
				}
			}
		}
	}()

	return outs
}


&#47;&#47; TestFunOut 异步操作 扇入模式
func TestFunOutAsync(t *testing.T) {
	dataStreams := []int{13, 44, 56, 99, 9, 45, 67, 90, 78, 23}

	inputChan := gen(dataStreams...) &#47;&#47; 将数据写入一个channel

	ch := sq(inputChan) &#47;&#47; 将所有的数据平方，再重新放入channel

	outArray := FunOut(ch, 3,true)
	length := len(outArray)
	t.Log(&quot;length of out channel:&quot;, length)
	var wg sync.WaitGroup
	wg.Add(length)
	for i := 0; i &lt; length; i++ {
		c:=len(outArray[i])
		fmt.Println(&quot;输入chan len&quot;, i, c)
		go func(in &lt;-chan int, index int) {
			sum:=0
			for item:=range in{
				fmt.Println(&quot;item&quot;, index, item)
				sum+=item
			}
			fmt.Println(&quot;worker&quot;, index, sum)

			wg.Done()
		}(outArray[i], i)
	}
	wg.Wait()
}

老师，我没看明白是哪里出错了？</div>2020-11-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/50/33/9dcd30c4.jpg" width="30px"><span>斯蒂芬.赵</span> 👍（1） 💬（1）<div>老师想问一下上面所讲的击鼓传花的案例(流水线模式)的应用场景是？感觉就是按照顺序串行的话执行某些任务逻辑，不用goroutine的话也可以吧</div>2021-11-15</li><br/><li><img src="" width="30px"><span>myrfy</span> 👍（1） 💬（1）<div>老师好，我有两个问题
1、关于or done或者fan in模式，我之前在sof上看到过类似的问题，其中的高赞回答是说，启动与ch数量相等的goroutine，每个goroutine监听一个ch并把读到的结果放入一个收集ch的模式效率要比反射高，并且给出了测评数据，现在手机码字，不太好找到。但想和老师确认一下是不是后面go某个版本对反射做了优化呢？
2、fanout模式里提到可以同步或者异步启动任务。在老师给出的示例代码中，异步启动的优势是什么呢？我猜老师想表达的是不是启动任务前可能还有一些耗时的准备操作？如果是这样的话，建议增加一个注释，否则感觉启动一个goroutine只是为了写一个ch，好像异步效率会更低</div>2020-11-11</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/nzuJRhm0cUgOShDdpx5iafaDd1xTRT5TDl0lMoYBVGDOHapGY59zbhdKAjKz5gE7F8ScyDEMfzBjtOIFgNZSOlu0oPfIibNY8vvruxzb4bCmE/132" width="30px"><span>Geek_290bf5</span> 👍（0） 💬（1）<div>&#47;&#47; asStream 函数
func asStream(done &lt;-chan struct{}, values ...interface{}) &lt;-chan interface{} {
	s := make(chan interface{})

	go func() {
		defer close(s)
		for _, v := range values {
			select {
			case &lt;-done:
				return
			case s &lt;- v:
			}
		}
	}()

	return s
}

对于这个函数，其中使用 go func() 来执行values值的读取，因为是子 goroutine，会不会出现执行结束返回了，go func() 还未执行完毕的情况?为什么作者的很多函数中，都直接使用 go func()却没有等待其执行完毕的情况呢？</div>2024-10-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/98/b1/f89a84d0.jpg" width="30px"><span>wu526</span> 👍（0） 💬（1）<div>晁老师，这是我用多个goroutine 实现的 OrDone，但是有一个问题是在  执行close(orDone)是可能会引发panic，引发panic的原因是因为可能多次关闭一个chan, 请问我这个需要如何改才能不引发panic呢?

func or3(channels ...&lt;-chan interface{}) &lt;-chan interface{} {
	if len(channels) == 0 {
		return nil
	}

	orDone := make(chan interface{})
	for _, c := range channels {

		go func(ch &lt;-chan interface{}) {
			&lt;-ch
			close(orDone) &#47;&#47; 可能会引发panic
		}(c)

	}
	return orDone
}</div>2022-11-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/12/1b/f62722ca.jpg" width="30px"><span>A9</span> 👍（0） 💬（1）<div>一个基于 TCP 网络的分布式的 Channel ，请问这个有git仓库吗，想学习下</div>2022-09-13</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/GJXKh8OG00U5ial64plAIibbIuwkzhPc8uYic9Hibl8SbqvhnS2JImHgCD4JGvTktiaVnCjHQWbA5wicaxRUN5aTEWnQ/132" width="30px"><span>Geek_a6104e</span> 👍（0） 💬（1）<div>请问一下最后一段代码里面case &lt;-done: 有什么用呢？</div>2022-07-31</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/17/9e/42/ab4f65c8.jpg" width="30px"><span>པག་ཏོན་།</span> 👍（0） 💬（1）<div>老师您好，在看Marcio Castilho 在 使用 Go 每分钟处理百万请求的例子的时候我很困惑，我认为双层管道是没有意义的，生产者直接发送job给消费者，额定数量的消费者直接进行并发接收并处理就可以达到同样控制并发的效果。为什么非要消费者把一个管道交给生产者，生产者在把job通过管道传递给消费者。我想请问一下这个步骤的作用是什么？</div>2021-10-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/65/21/101a7075.jpg" width="30px"><span>davix</span> 👍（0） 💬（1）<div>請問老師，channel這些模式都適合哪些塲景使用，能哪些優缺點能講講嗎</div>2021-10-06</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/19/22/c8/f2892022.jpg" width="30px"><span>科科</span> 👍（0） 💬（1）<div>老师，请问下为什么在createCase函数里面，我们在创建一个SelectCase变量的时候，要使用reflect.ValueOf重新初始化一个的channel?</div>2021-05-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/74/82/552786e8.jpg" width="30px"><span>Le Incredible Sulk</span> 👍（0） 💬（1）<div>老师，请问一下channel适不适用于传输大文件？还有就是传输大文件的性能情况是怎样的？（刚遇到的面试题）</div>2021-05-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/d8/45/02047152.jpg" width="30px"><span>AFreeCoder</span> 👍（0） 💬（1）<div>orDone 模式的代码没看明白。如果channel数是一个，直接返回这个channel，如果大于等于2个，就会返回被close的orDone，两种情况下返回的channel含义不一样，这是为什么呢</div>2021-04-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/4b/71/591ae170.jpg" width="30px"><span>大恒</span> 👍（0） 💬（1）<div>实现观察者为何不使用类似java的接口回调、go的函数回调，而要用扇出模式呢</div>2020-12-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/59/6b/27238910.jpg" width="30px"><span>difoil</span> 👍（0） 💬（1）<div>```go
&#47;&#47; 加入一个超时的设置
func (m *Mutex) LockTimeout(timeout time.Duration) bool {
    timer := time.NewTimer(timeout)    
      select {    
         case &lt;-m.ch:        
             timer.Stop()      
             return true    
         case &lt;-timer.C:    
       }    
       return false
}
```
这里是不是返回值写反了？</div>2020-12-06</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/41/38/4f89095b.jpg" width="30px"><span>写点啥呢</span> 👍（0） 💬（1）<div>请问老师，扇入扇出中可不可以让所有goroutine公用一个channel呢？比如扇入中，所有调用者都向同一个channel发送，被调用的goroutine从这个公共channel接收数据后再通过另外一个out channel发出去. 这样实现有什么问题不？</div>2020-11-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/ac/66/a256008b.jpg" width="30px"><span>SuperDai</span> 👍（0） 💬（1）<div>func FanOut(in &lt;-chan interface{}, out []chan interface{}, async bool) {
	go func() {
		var finish atomic.Value

		defer func() { &#47;&#47; 退出时关闭所有的输出channel
			for async &amp;&amp; finish.Load().(int) &lt; len(out) {
			}

			for i := 0; i &lt; len(out); i++ {
				close(out[i])
			}
		}()

		for v := range in {
			if async {
				finish.Store(0)
			}

			v := v
			for i := 0; i &lt; len(out); i++ {
				i := i
				&#47;&#47; TODO: 异步模式下, 会出现向已关闭的channel写数据
				&#47;&#47; Done: 利用原子计数来修复
				if async {
					go func() {
						out[i] &lt;- v
						finish.Store(finish.Load().(int) + 1)
					}()
				} else {
					out[i] &lt;- v
				}
			}
		}
	}()
}


老师, 这样写应该能修复FanOut的问题吧</div>2020-11-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/4b/69/c02eac91.jpg" width="30px"><span>大漠胡萝卜</span> 👍（0） 💬（1）<div>fanOut模式示例代码会出现向已经close的chan发送数据么？</div>2020-11-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/77/67/b6ad1aeb.jpg" width="30px"><span>owl</span> 👍（22） 💬（0）<div>chan实现互斥锁，如果buffer大于1，可以实现令牌桶</div>2021-03-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/07/d2/0d7ee298.jpg" width="30px"><span>惘 闻</span> 👍（2） 💬（0）<div>令牌桶</div>2021-07-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/21/01/5d/be118cfe.jpg" width="30px"><span>Chris</span> 👍（2） 💬（0）<div>reflect性能是比较差的，贴一下压测结果：
BenchmarkFanIn-4                  382776              3255 ns&#47;op             131 B&#47;op          2 allocs&#47;op
BenchmarkFanInReflect-4          1000000             13168 ns&#47;op            6974 B&#47;op         90 allocs&#47;op
BenchmarkFanInRec-4               280599              5524 ns&#47;op            1009 B&#47;op         27 allocs&#47;op
</div>2020-11-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/43/e0/66b71c1f.jpg" width="30px"><span>哈哈</span> 👍（1） 💬（0）<div>&#47;&#47; 解决异步情况，通道关闭，send数据导致panic的情况
func fanOut(in &lt;-chan interface{}, outs []chan interface{}, async bool) {
	go func() {
		var wg sync.WaitGroup

		defer func() {
			wg.Wait()

			for i := 0; i &lt; len(outs); i++ {
				close(outs[i])
			}
		}()

		for v := range in {
			v := v
			for i := range outs {
				i := i

				if async {
					wg.Add(1)
					go func() {
						outs[i] &lt;- v
						wg.Done()
					}()
				} else {
					outs[i] &lt;- v
				}
			}
		}
	}()
}</div>2022-02-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/3a/f8/c1a939e7.jpg" width="30px"><span>君哥聊技术</span> 👍（1） 💬（2）<div>我们在利用 chan 实现互斥锁的时候，如果 buffer 设置的不是 1，而是一个更大的值，会出现什么状况吗？能解决什么问题吗？

这样就能走多个gorouting获取到锁了，这就是一个共享锁，对于读多写少的场景，很有用。但是就是对于写锁，还是要配合buffer是1的chann。这类似于Java中的RentrantReadWriteLock</div>2020-11-16</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1a/19/99/ba3719e1.jpg" width="30px"><span>The brain is a good thing</span> 👍（0） 💬（0）<div>基于老师的channel编排小小改动，毕竟如果worker 数量多，手动去make初始化工作量就有点大了。
type Token struct {}

func work(id int,ch chan Token,nextCh chan Token,data chan int,exit chan struct{}) {
	for {
		token := &lt;-ch
		if v,ok := &lt;-data; ok {
			fmt.Printf(&quot;groutine id:%v,val:%v \n&quot;,id+1,v)
		}else {
			exit &lt;- struct{}{}
			return
		}
		&#47;&#47;time.Sleep(time.Second)
		nextCh &lt;- token
	}
}

func main() {
	workerNum := 10
	chs := make([]chan Token,workerNum)
	nums := make(chan int)
	exit := make(chan struct{})
	&#47;&#47;worker
	for i := 0; i &lt; workerNum; i++ {
		if chs[i] == nil {
			chs[i] = make(chan Token)
		}
		if chs[(i+1)%workerNum] == nil {
			chs[(i+1)%workerNum] = make(chan Token)
		}
		go work(i,chs[i],chs[(i+1)%workerNum],nums,exit)
	}

	go func() {
		for i := 0; i &lt; 100; i++ {
			nums &lt;- i
		}
		close(nums)
	}()
	chs[0] &lt;- Token{}

	&lt;- exit

}</div>2022-08-17</li><br/><li><img src="" width="30px"><span>Geek_5a2059</span> 👍（0） 💬（0）<div>Go 的 select 是伪随机的，它可以在执行的 case 中随机选择一个 case，并把选择的这个 case 的索引（chosen）返回，如果没有可用的 case 返回，会返回一个 bool 类型的返回值，这个返回值用来表示是否有 case 成功被选择。如果是 recv case，还会返回接收的元素。
”如果没有可用的 case 返回，会返回一个 bool 类型的返回值“ 这句话不太对吧，看源码注释，如果没有可用的 case，会一直阻塞的
&#47;&#47; Select executes a select operation described by the list of cases.
&#47;&#47; Like the Go select statement, it blocks until at least one of the cases
&#47;&#47; can proceed












</div>2021-09-07</li><br/><li><img src="" width="30px"><span>Geek_a3c9f5</span> 👍（0） 💬（0）<div>每个源 Channel 的元素都会发送给目标 Channel，相当于目标 Channel 的 receiver 只需要监听目标 Channel，就可以接收所有发送给源 Channel 的数据。
上面这句是否为笔误，下面的句子应该比较接近原意？还是我理解有误？
每个源Channel 的元素都会发送给目标Channel，相当于目标Channel 的receiver 只需要监听目标Channel，就可以接收所有发送给目标Channel 的数据。</div>2021-07-15</li><br/><li><img src="" width="30px"><span>Geek_a3c9f5</span> 👍（0） 💬（0）<div>每個源Channel 的元素都會發送給目標Channel，相當於目標Channel 的receiver 只需要監聽目標Channel，就可以接收所有發送給源Channel 的數據。
上面这句是否为笔误，下面的句子应该比较接近原意？还是我理解有误？
每个源Channel 的元素都会发送给目标Channel，相当于目标Channel 的receiver 只需要监听目标Channel，就可以接收所有发送给目标Channel 的数据。</div>2021-07-15</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/19/22/c8/f2892022.jpg" width="30px"><span>科科</span> 👍（0） 💬（0）<div>这节课信息量爆炸了，没想到channel有这么多用法，学到了学到了。
如果buffer有多个，我觉得在业务场景当中处理发布订阅的场景很适合用，当服务端发出一个事件的时候，很多终端都会来订阅，需要限制一次同时允许访问的最大数，超过可以返回错误，告诉终端稍后重试。</div>2021-05-22</li><br/><li><img src="https://wx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTI9zRdkKuXMKh30ibeludlAsztmR4rD9iaiclPicOfIhbC4fWxGPz7iceb3o4hKx7qgX2dKwogYvT6VQ0g/132" width="30px"><span>Initiative Thinker</span> 👍（0） 💬（0）<div>如果cleanup处理超时，主goroutine结束了，docleanup也会终止，但是cleanup还没有处理完，是不是会造成泄漏呢？</div>2021-05-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1b/a4/27/15e75982.jpg" width="30px"><span>小袁</span> 👍（0） 💬（0）<div>拓展了我对channle应用场景的理解。</div>2021-04-25</li><br/>
</ul>