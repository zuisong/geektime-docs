你好，我是郝林，今天我继续分享条件变量sync.Cond的内容。我们紧接着上一篇的内容进行知识扩展。

## 问题 1：条件变量的`Wait`方法做了什么？

在了解了条件变量的使用方式之后，你可能会有这么几个疑问。

1. 为什么先要锁定条件变量基于的互斥锁，才能调用它的`Wait`方法？
2. 为什么要用`for`语句来包裹调用其`Wait`方法的表达式，用`if`语句不行吗？

这些问题我在面试的时候也经常问。你需要对这个`Wait`方法的内部机制有所了解才能回答上来。

条件变量的`Wait`方法主要做了四件事。

1. 把调用它的goroutine（也就是当前的goroutine）加入到当前条件变量的通知队列中。
2. 解锁当前的条件变量基于的那个互斥锁。
3. 让当前的goroutine处于等待状态，等到通知到来时再决定是否唤醒它。此时，这个goroutine就会阻塞在调用这个`Wait`方法的那行代码上。
4. 如果通知到来并且决定唤醒这个goroutine，那么就在唤醒它之后重新锁定当前条件变量基于的互斥锁。自此之后，当前的goroutine就会继续执行后面的代码了。

你现在知道我刚刚说的第一个疑问的答案了吗？

因为条件变量的`Wait`方法在阻塞当前的goroutine之前，会解锁它基于的互斥锁，所以在调用该`Wait`方法之前，我们必须先锁定那个互斥锁，否则在调用这个`Wait`方法时，就会引发一个不可恢复的panic。
<div><strong>精选留言（30）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/0f/f5/b9/888fe350.jpg" width="30px"><span>不记年</span> 👍（20） 💬（1）<div>老师，我有一个疑问，对于cond来说，每次只唤醒一个goruntine，如果这么goruntine发现消息不是自己想要的就会从新阻塞在wait函数中，那么真正需要这个消息的goruntine还会被唤醒吗？</div>2019-07-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/4a/96/99466a06.jpg" width="30px"><span>Laughing</span> 👍（15） 💬（1）<div>L公开变量代表cond初始化时传递进来的锁，这个锁的状态是可以改变的，但会影响cond对互斥锁的控制。</div>2018-10-15</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/12/70/10faf04b.jpg" width="30px"><span>Lywane</span> 👍（6） 💬（1）<div>```
	lock.Lock()
	for mailbox == 1 {
		sendCond.Wait()
	}
	mailbox = 1
	lock.Unlock()
	recvCond.Signal()
```
只要共享资源的状态不变，即使当前的 goroutine 因收到通知而被唤醒，也依然会再次执行这个Wait方法，并再次被阻塞。

老师我对这句话有个疑问，假设Wait不解锁，直接阻塞了当前goroutine，那么当收到通知时，mailbox的值应该已经被改成0了，此时唤醒，应该不满足for循环条件了呀，为什么会再次执行Wait方法呢？

我思考的结论是：Wait解锁是为了让其他goroutine去修改mailbox的值，不知道这么理解对吗。</div>2020-03-27</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTKdiaUiaCYQe9tibemaNU5ya7RrU3MYcSGEIG7zF27u0ZDnZs5lYxPb7KPrAsj3bibM79QIOnPXAatfIw/132" width="30px"><span>Geek_a8be59</span> 👍（2） 💬（1）<div>老实您好，不太明白为什么一定要用条件变量呢。我看了 go并发编程第2版和你这边的做了对应，书上是已生成者消费者为例，我想的是用两个互斥量不行么？生成一个锁，消费一个锁，只是说可能会浪费在循环判断是否可生成，是否可消费中，还有可能因为某些不成功导致一直不能解锁的状况。  难不成条件变量主要就是优化上述问题的么？</div>2019-08-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/62/1e/8054e6db.jpg" width="30px"><span>樂文💤</span> 👍（2） 💬（3）<div>所以如果用的signal方法只通知一个go routine的话 条件变量的判断方法改成if应该是没问题的 但如果是多个go routine 同时被唤醒就可能导致多个go routine 在不满足唤醒状态的时候被唤醒而导致处理错误，这时候就必须用for来不断地进行检测可以这么理解么</div>2019-08-03</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/0M3kK7d2sLapYh9VgqzQargLNkiaJbJZTDNjzLhm9s9FYbFUVDSKa74yvcvH5IHWgknuibmh9fObbrHXvfAib28IQ/132" width="30px"><span>手指饼干</span> 👍（1） 💬（1）<div>老师您好，关于发送通知是否需要在锁的保护下调用，还是有些疑问，以下想法请老师帮忙看看是否理解正确：
一个在等待通知的 goroutine 收到通知信号被唤醒，接下来执行的是条件变量 c.L.Lock() 操作，无论信号的发送方是否是在锁的保护下发送信号，该 goroutine 已经不是在等待通知的状态了，而是在尝试获取锁的状态，即使被阻塞，也是因为获取不到锁。区别只是，如果信号发送方在 Unlock() 之后发送信号，那么该 goroutine 被唤醒后获得锁可能会衔接得更好一点。
对于某些场景，比如说函数的开头两行代码就是
mutex.Lock() 
defer mutex.Unlock()
这种情况是否可以允许通知在 Unlock() 之前调用</div>2020-08-01</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/18/50/b1/f9b6b317.jpg" width="30px"><span>黄仲辉</span> 👍（0） 💬（1）<div>sync.crod 类比 java的 监视器锁</div>2022-09-04</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/KhQRc8hIxHHyPV3Og2Fc5qhN3zkWUnw31wkc7mcmGyxicD9Yrvhh7N5B3icqpgWZXfuWbysn7Lv6QMPIEmYPeC4w/132" width="30px"><span>Geek_108cb5</span> 👍（0） 💬（1）<div>试了一下把互斥锁改成读写锁， 中途会发生一个发送消息被两个接受者同时收到的场景， 导致最后发送者阻塞， 此时主线程的信道也阻塞了， 接受者协程执行完毕， 整体是死锁的情况。 那假如发送者和接收者都是无限循环， 而且多个接收者接收者接到同一份消息不会对业务有影响的情况下， 使用读写锁应该也是没有问题的？</div>2022-03-01</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1e/96/3a/e06f8367.jpg" width="30px"><span>HiNeNi</span> 👍（0） 💬（1）<div>func testCond() {
	mu := sync.Mutex{}
	cond := sync.NewCond(&amp;mu)
	s := &quot;&quot;

	go func () {
		fmt.Println(&quot;This is consumer&quot;)
		for {
			mu.Lock()

			for len(s) == 0 {
				cond.Wait()
			}
			&#47;&#47;time.Sleep(time.Second * 1)
			fmt.Println(&quot;consumer, s:&quot;, s)
			s = &quot;&quot;
			mu.Unlock()
			cond.Signal()
		}
	}()

	go func () {
		fmt.Println(&quot;This is producer&quot;)
		for {
			mu.Lock()
			for len(s) &gt; 0 {
				cond.Wait()
			}
			fmt.Println(&quot;produce a string&quot;)
			s = &quot;generate s resource&quot;
			mu.Unlock()
			cond.Signal()
		}

	}()

	time.Sleep(time.Second * 10)
}
==========================================
自己测的时候发现用一个Cond就可以满足生产者消费者的简单模型，谁能告诉我为什么例子一定要使用两个Cond？</div>2021-11-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/df/1e/cea897e8.jpg" width="30px"><span>传说中的成大大</span> 👍（0） 💬（1）<div>看了你下面的留言 感觉条件变量主要是为了避免互斥锁或者读写锁 锁竞争条件</div>2020-04-07</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/df/1e/cea897e8.jpg" width="30px"><span>传说中的成大大</span> 👍（0） 💬（1）<div>今天主要讲的go的同步 条件变量
总的来说我又去看了一下unix环境高级编程的条件变量感觉二者一样
这两个方法并不需要受到互斥锁的保护，我们也最好不要在解锁互斥锁之前调用它们
关于这个结论的我猜测是如果没有解锁 某个goroutine 还没解锁又被唤醒了 但是又不是它想要的共享状态 然后又加锁 又进入wait导致死锁？</div>2020-04-07</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/12/70/10faf04b.jpg" width="30px"><span>Lywane</span> 👍（0） 💬（1）<div>它们都在等mailbox变量的值不为0的时候再把它的值变为0，这就相当于有多个人在等着我向信箱里放置情报。

老师这里不对吧，上一讲说的是`mailbox 代表信箱。0代表信箱是空的，1代表信箱是满的`。大家等着把mailbox设置为0，应该是都在等着拿信</div>2020-03-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/c6/73/abb7bfe3.jpg" width="30px"><span>疯琴</span> 👍（0） 💬（1）<div>wait的原理讲解很清晰。

请问老师两个问题：
1. 收信人也修改了mailbox，为什么不用写锁？我试了一下，如果把收信人分成两个goroutine，一个循环2次另一个循环3次，有可能两个收信人先后连续收了信，这样最后一步是发信人发信。recvCond.Signal()只唤醒一个收信人，为什么会有两个收信人先后连续收信呢？我把recvCond改成用写锁就恢复正常了。用写锁是为了演示一下获取写锁的方法么？
package main

import (
	&quot;log&quot;
	&quot;sync&quot;
	&quot;time&quot;
)

func main() {
	var mailbox uint8
	var lock sync.RWMutex
	sendCond := sync.NewCond(&amp;lock)
	recvCond := sync.NewCond(lock.RLocker())

	sign := make(chan struct{}, 3)
	max := 5

	&#47;&#47; 发信
	go func(max int) {
		defer func() {
			sign &lt;- struct{}{}
		}()

		for i := 1; i &lt;= max; i++ {
			time.Sleep(time.Millisecond * 500)
			lock.Lock()
			for mailbox == 1 {
				sendCond.Wait()
			}
			log.Printf(&quot;sender [%d]: the mail box is empty.&quot;, i)
			mailbox = 1
			log.Printf(&quot;sender [%d]: the letter has been send.&quot;, i)
			lock.Unlock()
			recvCond.Signal()
		}
	}(max)

	&#47;&#47; 收信
	go func(max int) {
		defer func() {
			sign &lt;- struct{}{}
		}()
		for j := 1; j &lt;= max; j++ {
			time.Sleep(time.Millisecond * 500)
			lock.RLock()
			for mailbox == 0 {
				recvCond.Wait()
			}
			log.Printf(&quot;receiver [%d]: the mail box is full.&quot;, j)
			mailbox = 0
			log.Printf(&quot;receiver [%d]: the letter has been received.&quot;, j)
			lock.RUnlock()
			sendCond.Signal()
		}
	}(2)

	&#47;&#47; 收信
	go func(max int) {
		defer func() {
			sign &lt;- struct{}{}
		}()
		for j := 1; j &lt;= max; j++ {
			time.Sleep(time.Millisecond * 500)
			lock.RLock()
			for mailbox == 0 {
				recvCond.Wait()
			}
			log.Printf(&quot;receiver [%d]: the mail box is full.&quot;, j)
			mailbox = 0
			log.Printf(&quot;receiver [%d]: the letter has been received.&quot;, j)
			lock.RUnlock()
			sendCond.Signal()
		}
	}(3)

	&lt;-sign
	&lt;-sign
	&lt;-sign

	log.Println(mailbox)
}
2. “当通知被发送的时候，如果没有任何 goroutine 需要被唤醒，那么该通知就会立即失效。”这一点我没有理解。我让收信人启动更晚一点，也就是发信人执行Signal()的时候收信人还没有Wait()，但是依然正常执行了。</div>2019-12-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/79/37/3316de0c.jpg" width="30px"><span>K_night</span> 👍（0） 💬（1）<div>send := func(id int, index int) {
		&#47;&#47; defer func() {
		&#47;&#47; 	sign &lt;- struct{}{}
		&#47;&#47; }()
		lock.Lock()
		wakeupNum := 0
		log.Printf(&quot;wait before wakeupNum: [%d]&quot;, wakeupNum)
		for msgbox == 1 {
			fmt.Printf(&quot;wait before in for wakeupNum: [%d]&quot;, wakeupNum)
			&#47;&#47; log.Printf(&quot;wait before in for wakeupNum: [%d]&quot;, wakeupNum)
			sendCond.Wait()
			&#47;&#47; log.Printf(&quot;other Broadcast&quot;)
			wakeupNum = 1
			log.Printf(&quot;wait after wakeupNum: [%d]&quot;, wakeupNum)
		}
		log.Printf(&quot;sender: id:[%d] index:[%d] msgbox is empty&quot;, id, index)
		log.Printf(&quot;wakeupNum: [%d]&quot;, wakeupNum)
		sendNum = wakeupNum
		msgbox = 1
		log.Printf(&quot;sender: id:[%d] index:[%d] mail has been send&quot;, id, index)
		lock.Unlock()
		recvCond.Broadcast()
	}
for循环里面的代码被优化了吗。怎么没有执行呢。望老师解惑感谢</div>2019-11-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/42/7c/8ef14715.jpg" width="30px"><span>NIXUS</span> 👍（0） 💬（4）<div>请教老师一个问题: 
demo62.go中, 收信只是读数据, 可是为什么使用RLock()和RUnlock()就报错, 而必须要使用Lock()和Ulock()呢?</div>2019-04-15</li><br/><li><img src="" width="30px"><span>Geek_7b1949</span> 👍（0） 💬（1）<div>关于第一个问题，有个疑问，文中说，如果不先加锁，wait方法中解锁，很容易造成wait方法对加锁的锁重复加锁从而造成goroutine阻塞，但是在wait方法调用之前，不是同样也会造成这个问题吗，也有可能在还没有走到wait的时候造成goroutine的阻塞呀，求解答</div>2019-04-03</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/2f/ff/e9ebafec.jpg" width="30px"><span>RegExp</span> 👍（0） 💬（1）<div>条件变量的Wait方法在阻塞当前的 goroutine之前，会解锁它基于的互斥锁，那是不是显示调用lock.Lock()的锁也被解锁了呢？

</div>2019-03-30</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/d4/78/53d93c43.jpg" width="30px"><span>奋斗</span> 👍（0） 💬（1）<div>Java的notify和notifyall?</div>2019-01-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/18/c4/e55fdc1c.jpg" width="30px"><span>cygnus</span> 👍（0） 💬（1）<div>思考题：sync.Cond类型中的公开字段L是用来保存NewCond方法传递进来的互斥锁的，这个锁是条件变量自己控制的，所以我们不能在使用过程中改变这个字段的值，否则可能会导致panic或死锁
</div>2018-10-15</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/fb/a7/12c90699.jpg" width="30px"><span>Askerlve</span> 👍（0） 💬（1）<div>老师总结中句子:&quot;sync.Mutex类型的值以及*sync.RWMutex类型的值&quot;sync.Mutex是不是少个&quot;*&quot;哇?</div>2018-10-15</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/aa/53/62b5c104.jpg" width="30px"><span>郝林</span> 👍（44） 💬（3）<div>对条件变量这个工具本身还有疑问的读者可以去看我写的《Go 并发编程实战》第二版。这本书从并发程序的基本概念讲起，用一定篇幅的图文内容详细地讲解了条件变量的用法，同时还有一个贯穿了互斥锁和条件变量的示例。由于这本书的版权在出版社那里，所以我不能把其中的内容搬到这里。

我在这里只对大家共同的疑问进行简要说明：

1. 条件变量适合保护那些可执行两个对立操作的共享资源。比如，一个既可读又可写的共享文件。又比如，既有生产者又有消费者的产品池。

2. 对于有着对立操作的共享资源（比如一个共享文件），我们通常需要基于同一个锁的两个条件变量（比如 rcond 和 wcond）分别保护读操作和写操作（比如 rcond 保护读，wcond 保护写）。而且，读操作和写操作都需要同时持有这两个条件变量。因为，读操作在操作完成后还要向 wcond 发通知；写操作在操作完成后还要向 rcond 发通知。如此一来，读写操作才能在较少的锁争用的情况下交替进行。

3. 对于同一个条件变量，我们在调用它的 Signal 方法和 Broadcast 方法的时候不应该处在其包含的那个锁的保护下。也就是说，我们应该先撤掉保护屏障，再向 Wait 方法的调用方发出通知。否则，Wait 方法的调用方就有可能会错过通知。这也是我更推荐使用 Broadcast 方法的原因。所有等待方都错过通知的概率要小很多。

4. 相对应的，我们在调用条件变量的 Wait 方法的时候，应该处在其中的锁的保护之下。因为有同一个锁保护，所以不可能有多个 goroutine 同时执行到这个 Wait 方法调用，也就不可能存在针对其中锁的重复解锁。

5. 再强调一下。对于同一个锁，多个 goroutine 对它重复锁定时只会有一个成功，其余的会阻塞；多个 goroutine 对它重复解锁时也只会有一个成功，但其余的会抛 panic。</div>2019-06-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/80/8e/1b14c6bc.jpg" width="30px"><span>Geek_14c558</span> 👍（22） 💬（1）<div>我理解是这样的。流程： 外部函数加锁 -&gt; 判断条件变量-&gt;wait内部解锁-&gt;阻塞等待信号-&gt;wait内部加锁-&gt; 修改条件变量-&gt; 外部解锁-&gt; 触发信号。 第一次加解锁是为了保证读条件变量时它不会被修改， wait解锁是为了条件变量能够被其他线程改变。wait内部再次加锁，是对条件变量的保护，因为外部要修改。 </div>2019-05-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/ac/a1/43d83698.jpg" width="30px"><span>云学</span> 👍（8） 💬（2）<div>有个疑问，broadcast唤醒所有wait的goroutine，那他们被唤醒时需要去加锁(wait返回)，都能成功吗？</div>2018-10-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/0e/9c/cb9da823.jpg" width="30px"><span>猫王者</span> 👍（5） 💬（2）<div>“我们最好在解锁条件变量基于的那个互斥锁之后，再去调用它的这两个方法（signal和Broadcast）。这更有利于程序的运行效率”    这个应该如何理解？

我的理解是如果先调用signal方法，然后在unlock解锁，如果在这两个操作中间该线程失去cpu，或者我人为的在siganl和unlock之间调用time.Sleep();在另一个等待线程中即使该等待线程被前者所发出的signal唤醒，但是唤醒的时候同时会去进行lock操作，但是前者的线程中由于失去了cpu，并没有调用unlock，那么这次唤醒不是应该失败了吗，即使前者有得到了cpu去执行了unlcok，但是signal操作具有及时性，等待线程不是应该继续等待下一个signal吗，感觉最后会变成死锁啊

</div>2018-10-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/67/ff/d4f31b87.jpg" width="30px"><span>打你</span> 👍（4） 💬（0）<div>在看了一遍，清楚了</div>2018-11-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/93/ce/d4ac6fae.jpg" width="30px"><span>甦</span> 👍（2） 💬（2）<div>源码问题问一下郝老师，cond wait方法里，多个协程走到c.L.Unlock()那一步不会出问题吗？ 只有一个协程可以unlock成功，其他协程重复unlock不就panic了吗？</div>2018-12-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/67/ff/d4f31b87.jpg" width="30px"><span>打你</span> 👍（2） 💬（3）<div>lock.Lock()
for mailbox == 1 {
 sendCond.Wait()
}
mailbox = 1
lock.Unlock()
recvCond.Signal()
如果wait已经解锁lock.Lock()锁住的锁，后面lock.Unlock解锁是什么意思？不会panic。
条件变量这2篇看起来前后理解不到</div>2018-11-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/a0/c5/9259d5ca.jpg" width="30px"><span>daydaygo</span> 👍（1） 💬（0）<div>看完虽然了解了 syncCond 的用法, 但是使用场景还是不了解, 特别是从来没遇到过, 更感觉这个东西「无用」</div>2022-11-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/2e/f1/f3/6a2e6977.jpg" width="30px"><span>严光</span> 👍（0） 💬（0）<div>这节看了很多遍还是没看明白，先收藏着。</div>2024-07-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1b/be/af/93e14e9d.jpg" width="30px"><span>扁舟</span> 👍（0） 💬（0）<div>go里面不支持可重入锁，是因为go想让开发者主动思考，将少锁的粒度，哪些是不可变的吗</div>2024-04-04</li><br/>
</ul>