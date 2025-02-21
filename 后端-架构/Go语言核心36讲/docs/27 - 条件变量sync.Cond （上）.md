在上篇文章中，我们主要说的是互斥锁，今天我和你来聊一聊条件变量（conditional variable）。

## 前导内容：条件变量与互斥锁

我们常常会把条件变量这个同步工具拿来与互斥锁一起讨论。实际上，条件变量是基于互斥锁的，它必须有互斥锁的支撑才能发挥作用。

条件变量并不是被用来保护临界区和共享资源的，它是用于协调想要访问共享资源的那些线程的。当共享资源的状态发生变化时，它可以被用来通知被互斥锁阻塞的线程。

比如说，我们两个人在共同执行一项秘密任务，这需要在不直接联系和见面的前提下进行。我需要向一个信箱里放置情报，你需要从这个信箱中获取情报。这个信箱就相当于一个共享资源，而我们就分别是进行写操作的线程和进行读操作的线程。

如果我在放置的时候发现信箱里还有未被取走的情报，那就不再放置，而先返回。另一方面，如果你在获取的时候发现信箱里没有情报，那也只能先回去了。这就相当于写的线程或读的线程阻塞的情况。

虽然我们俩都有信箱的钥匙，但是同一时刻只能有一个人插入钥匙并打开信箱，这就是锁的作用了。更何况咱们俩是不能直接见面的，所以这个信箱本身就可以被视为一个临界区。

尽管没有协调好，咱们俩仍然要想方设法的完成任务啊。所以，如果信箱里有情报，而你却迟迟未取走，那我就需要每过一段时间带着新情报去检查一次，若发现信箱空了，我就需要及时地把新情报放到里面。
<div><strong>精选留言（30）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/12/54/ba/8721e403.jpg" width="30px"><span>hello peter</span> 👍（39） 💬（2）<div>老师, 感觉这个送信的例子似乎用chanel实现更简单.在网上也查了一些例子, 发现都可以用chanel替代. 那使用sync.Cond 的优势是什么呢, 或者有哪些独特的使用场景?</div>2018-10-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/59/c0/6f02c096.jpg" width="30px"><span>属雨</span> 👍（34） 💬（1）<div>个人理解，不确定对不对，请老师评判一下：
因为Go语言传递对象时，使用的是浅拷贝的值传递，所以，当传递一个Cond对象时复制了这个Cond对象，但是低层保存的L(Locker类型)，noCopy(noCopy类型)，notify(notifyList类型)，checker(copyChecker)对象的指针没变，因此，*sync.Cond和sync.Cond都可以传递。</div>2018-10-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/df/1e/cea897e8.jpg" width="30px"><span>传说中的成大大</span> 👍（19） 💬（1）<div>这几天一直对条件变量的理解比较模糊，但是我想既然要学就学好 于是又去翻了Unix环境高级编程 总算把它跟互斥锁区分开了
互斥锁 是对一个共享区域进行加锁 所有线程都是一种竞争的状态去访问
而条件变量 主要是通过条件状态来判断，实际上他还是会阻塞 只不过不会像互斥锁一样去参与竞争，而是在哪里等待条件变量的状态发生改变过后的通知 再被唤醒</div>2020-04-09</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTKdiaUiaCYQe9tibemaNU5ya7RrU3MYcSGEIG7zF27u0ZDnZs5lYxPb7KPrAsj3bibM79QIOnPXAatfIw/132" width="30px"><span>Geek_a8be59</span> 👍（15） 💬（3）<div>var mailbox uint8
var lock sync.RWMutex
sendCond := sync.NewCond(&amp;lock)
recvCond := sync.NewCond(&amp;lock)
为什么不能向上面那样都用同一个互斥量，非要两个不同呢？老师，能讲一下区别么
</div>2019-08-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/0a/0b/985d3800.jpg" width="30px"><span>郭星</span> 👍（5） 💬（1）<div>在for 循环中使用 wait,在我的测试中,当条件变量处于wait状态时,如果没有唤醒,当前协程会一直阻塞等待在wait这行代码,因此使用for 和 使用if 实际最终结果是相同的,为什么要使用for呢?

package lesson27

import (
	&quot;sync&quot;
	&quot;testing&quot;
	&quot;time&quot;
)

&#47;&#47; 利用条件变量实现协调多协程发取信件操作
func TestCond(t *testing.T) {
	var wg sync.WaitGroup
	var mu sync.RWMutex
	&#47;&#47; 信箱
	mail := false
	&#47;&#47; 两个条件变量
	&#47;&#47; 发送信条件变量
	sendCond := sync.NewCond(&amp;mu)
	&#47;&#47; 接收信条件变量, 对于接收实际是只读操作,因此只需要使用读锁就可以
	receiveCond := sync.NewCond(mu.RLocker())
	&#47;&#47; 最大发送接收次数
	max := 5
	wg.Add(2)
	&#47;&#47; 发送人协程
	go func(i int) {
		for ; i &gt; 0; i-- {
			time.Sleep(time.Second * 3)
			mu.Lock()
			&#47;&#47; 如果信箱不为空,则需要等待
			&#47;&#47;for mail {
			if mail {
				&#47;&#47; 发送者等待
				t.Log(&quot;sendCond准备进入等待队列&quot;)
				sendCond.Wait()
				t.Log(&quot;sendCond进入等待队列&quot;)
			}
			mail = true
			t.Log(&quot;发送信件成功&quot;)
			mu.Unlock()
			&#47;&#47; 通知发送者
			receiveCond.Signal()
			t.Log(&quot;唤醒receiveCond&quot;)
		}
		wg.Done()
	}(max)

	go func(i int) {
		for ; i &gt; 0; i-- {
			mu.RLock()
			&#47;&#47;for !mail {
			if !mail {
				&#47;&#47;接收者等待
				t.Log(&quot;receiveCond准备进入等待队列&quot;)
				receiveCond.Wait() &#47;&#47; 如果没有被唤醒会一直阻塞在此
				t.Log(&quot;receiveCond进入等待队列&quot;)
			}
			mail = false
			t.Log(&quot;获取信件成功&quot;)
			mu.RUnlock()
			&#47;&#47; 通知接收者
			sendCond.Signal()
			t.Log(&quot;唤醒sendCond&quot;)
		}
		wg.Done()
	}(max)
	wg.Wait()
}
</div>2020-09-02</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/2e/16/ed/acd6df5e.jpg" width="30px"><span>啦啦啦</span> 👍（3） 💬（1）<div>想请问下老师，两个goroutine都使用了同一把锁，26讲（Mutex）里不是说明，尽量使用：是让每一个互斥锁都只保护一个临界区或一组相关临界区。有点搞不明白，望老师指点



go func(max int) { &#47;&#47; 用于发信。
		defer func() {
			sign &lt;- struct{}{}
		}()
		for i := 1; i &lt;= max; i++ {
			time.Sleep(time.Millisecond * 500)
			lock.Lock()
			for mailbox == 1 {
				sendCond.Wait()
			}
			log.Printf(&quot;sender [%d]: the mailbox is empty.&quot;, i)
			mailbox = 1
			log.Printf(&quot;sender [%d]: the letter has been sent.&quot;, i)
			lock.Unlock()
			recvCond.Signal()
		}
	}(max)
	go func(max int) { &#47;&#47; 用于收信。
		defer func() {
			sign &lt;- struct{}{}
		}()
		for j := 1; j &lt;= max; j++ {
			time.Sleep(time.Millisecond * 500)
			lock.RLock()
			for mailbox == 0 {
				recvCond.Wait()
			}
			log.Printf(&quot;receiver [%d]: the mailbox is full.&quot;, j)
			mailbox = 0
			log.Printf(&quot;receiver [%d]: the letter has been received.&quot;, j)
			lock.RUnlock()
			sendCond.Signal()
		}
	}(max)</div>2022-06-07</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/9d/a4/e481ae48.jpg" width="30px"><span>lesserror</span> 👍（3） 💬（1）<div>郝林老师，demo61.go 中的  两个go function（收信 和 发信），是怎么保证先 发信 后收信的呢？

不是说 go function 函数 的执行 是 随机的么？ 我打印了很多遍，发现 都是执行的 发信 操作，然后是 收信 操作。</div>2021-08-15</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/38/e2/28aa8e6c.jpg" width="30px"><span>会玩code</span> 👍（2） 💬（2）<div>老师，不懂这里的recvCond为什么可以用读锁呢？这里也是有对资源做操作的呀（将mailbox置为0），用读锁不会有问题吗？</div>2020-05-15</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/2e/39/7682b49e.jpg" width="30px"><span>lofaith</span> 👍（1） 💬（1）<div>老师，读写锁之间不是互斥的吗，我理解应该在加上读锁的时候，写锁就会阻塞在lock这里，不会走到 sendCond.Wait() 这里啊。虽然能明白条件变量的作用了，但还是不清楚它的使用场景，老师能说一下使用场景吗</div>2021-11-15</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/6d/52/404912c3.jpg" width="30px"><span>...</span> 👍（1） 💬（3）<div>老师 wait会释放锁吗</div>2019-02-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/7f/75/551c5d6c.jpg" width="30px"><span>CrazyCodes</span> 👍（0） 💬（1）<div>*sync.Cond类型的值可以被传递吗？那sync.Cond类型的值呢？

代码测试*sync.Cond 可以被传递，但sync.Cond不能，是因为必须是指针类型吗？</div>2023-11-24</li><br/><li><img src="" width="30px"><span>川川</span> 👍（0） 💬（1）<div>老师，我没太理解为啥 广播 是要在解锁之后再 触发吗？  client-go 中广播都是在锁内发生的啊

func (f *FIFO) Add(obj interface{}) error {
	id, err := f.keyFunc(obj)
	if err != nil {
		return KeyError{obj, err}
	}
	f.lock.Lock()
	defer f.lock.Unlock()
	f.populated = true
	if _, exists := f.items[id]; !exists {
		f.queue = append(f.queue, id)
	}
	f.items[id] = obj
	f.cond.Broadcast()
	return nil
}</div>2022-05-22</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTKELX1Rd1vmLRWibHib8P95NA87F4zcj8GrHKYQL2RcLDVnxNy1ia2geTWgW6L2pWn2kazrPNZMRVrIg/132" width="30px"><span>jxs1211</span> 👍（0） 💬（1）<div>在运行读取mailbox的goroutine中，当mailbox=1时，可以取信，在这段由读锁锁定的临界区中，mailbox=0实际是一个写入操作，怎么理解这个读锁锁定的临界区中实则为一个写操作呢
log.Printf(&quot;receiver [%d]: the mailbox is full.&quot;, j)
mailbox = 0
log.Printf(&quot;receiver [%d]: the letter has been received.&quot;, j)
lock.RUnlock()</div>2021-10-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/9d/a4/e481ae48.jpg" width="30px"><span>lesserror</span> 👍（0） 💬（1）<div>郝林老师，如果能对照代码的打印输出流程讲就好了，有好多讲我看代码的输出挺懵的。</div>2021-08-15</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/66/77/194ba21d.jpg" width="30px"><span>ileruza</span> 👍（0） 💬（1）<div>a := &amp;lock
b := lock.RLocker()

fmt.Printf(&quot;%p\n&quot;, a)
fmt.Printf(&quot;%p\n&quot;, b)

它们地址都是一样的呀，为什么说是不同的lock呢？</div>2021-03-31</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/3f/8d/a89be8f9.jpg" width="30px"><span>寻路人</span> 👍（0） 💬（2）<div>var lock sync.RWMutex明明是读写锁，
一个goroutine使用了lock.Lock()，另一个goroutine再调用lock.RLock()会互斥。
这里作者应该忽略了告诉读者Wait()会释放独占锁的一个概念。</div>2021-01-23</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/PiajxSqBRaEIBJYQ73yYqmiaU7Zg0BHPh9gpSglI79Dzcbob7I2tZOhTjbTTCw13KzVusYhLbKkukV9Ru5UfJMxQ/132" width="30px"><span>Geek_2d276a</span> 👍（0） 💬（2）<div>有个疑问：互斥锁的解锁操作可以唤醒之前因为加锁导致的阻塞的协程，为什么还要用条件变量来实现唤醒阻塞的协程呢？</div>2020-06-04</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/fe/2d/2c9177ca.jpg" width="30px"><span>给力</span> 👍（0） 💬（1）<div>指针类型可以被传递，因为底层数据是同一份。
传值的话
type Cond struct {
	noCopy noCopy

	&#47;&#47; L is held while observing or changing the condition
	L Locker

	notify  notifyList
	checker copyChecker
}
Locker 是接口，传递时是引用类型
notifyList 是结构体，会被浅拷贝
checker 是数值类型，也会被拷贝

如果sync.Cond在传递过程中，结构体和数值类型各层都有一份备份数据，容易造成不一致情况，所以极容易出问题。
</div>2020-03-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/2a/94/8c128d36.jpg" width="30px"><span>Howard</span> 👍（0） 💬（2）<div>我能把mailbox = 0放到lock.RUnlock()外面吗？总觉得读锁里面改动mailbox有点不好。</div>2019-12-16</li><br/><li><img src="" width="30px"><span>qiushye</span> 👍（0） 💬（2）<div>文章的例子是“我发信，你收信”，示例图表达的是“你发信，我收信”，稍有不足.</div>2019-08-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/97/86/fb564a19.jpg" width="30px"><span>bluuus</span> 👍（0） 💬（2）<div>我试了一下demo61.go, 发现永远只有一个协程可以进到wait方法，当mailbox初始值是0，只有可能收协程进到wait方法；当mailbox初始值为1，只有可能发协程进到wait方法。为什么会这样</div>2019-08-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/c6/73/abb7bfe3.jpg" width="30px"><span>疯琴</span> 👍（7） 💬（0）<div>秘密接头的类比形象生动，学习过程轻松有趣又不失深度。</div>2019-12-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/ea/80/8759e4c1.jpg" width="30px"><span>🐻</span> 👍（6） 💬（0）<div>需传递 *sync.Cond

因为 Cond 结构体中的 notify 变量和 checker 变量都是值类型，传递sync.Cond 会复制值，这样两个锁保留的被阻塞的 Goroutine 就不同了。</div>2019-04-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/d4/e0/513d185e.jpg" width="30px"><span>文@雨路</span> 👍（6） 💬（0）<div>指针可以传递，值不可以，传递值会拷贝一份，导致出现两份条件变量，彼此之间没有联系</div>2018-10-12</li><br/><li><img src="https://wx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTLmBgic9UlGySyG377pCVzNnbgsGttrKTCFztunJlBTDS32oTyHsJjAFJJsYJyhk9cNE5OZeGKWJ6Q/132" width="30px"><span>beiliu</span> 👍（5） 💬（0）<div>您好，老师，官方文档是建议，singal在锁住的情况下使用的“Signal唤醒等待c的一个线程（如果存在）。调用者在调用本方法时，建议（但并非必须）保持c.L的锁定“</div>2018-12-31</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/e8/58/ecb493dc.jpg" width="30px"><span>ming</span> 👍（5） 💬（3）<div>多routine从信箱中获取情报, 都在等mailbox变量的值不为0的时候再把它的值变为0，
这个 RLock 限制不了写操作，可能会有多个routine同时将 mailbox 变为0的，跟文中的场景有些不合。 
不知道我理解的有没有问题
</div>2018-12-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/d9/d2/4ae9b17f.jpg" width="30px"><span>q</span> 👍（4） 💬（0）<div>个人感觉，从底层原理解释条件变量可能更容易理解</div>2020-11-03</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1c/f7/62/947004d0.jpg" width="30px"><span>www</span> 👍（1） 💬（0）<div>这篇讲解太棒了，看了lock.RLocker()的源码，又返回去看了前面第14篇讲解接口的文章。多看多写，逐步提升</div>2020-06-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/2b/39/19041d78.jpg" width="30px"><span>😳</span> 👍（1） 💬（0）<div>这个类比生动形象，很有趣，简单易懂</div>2020-04-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/12/70/10faf04b.jpg" width="30px"><span>Lywane</span> 👍（1） 💬（0）<div>recvCond.Signal()表示接收方可以接受了，发送这个信号的是发送方。
sendCond.Signal()表示发送方可以再次发送了，发送这个信号的是接收方。</div>2020-03-27</li><br/>
</ul>