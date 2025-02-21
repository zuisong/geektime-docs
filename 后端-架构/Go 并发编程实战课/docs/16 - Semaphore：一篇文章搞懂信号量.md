你好，我是鸟窝。

在前面的课程里，我们学习了标准库的并发原语、原子操作和Channel，掌握了这些，你就可以解决80%的并发编程问题了。但是，如果你要想进一步提升你的并发编程能力，就需要学习一些第三方库。

所以，在接下来的几节课里，我会给你分享Go官方或者其他人提供的第三方库，这节课我们先来学习信号量，信号量（Semaphore）是用来控制多个goroutine同时访问多个资源的并发原语。

# 信号量是什么？都有什么操作？

信号量的概念是荷兰计算机科学家Edsger Dijkstra在1963年左右提出来的，广泛应用在不同的操作系统中。在系统中，会给每一个进程一个信号量，代表每个进程目前的状态。未得到控制权的进程，会在特定的地方被迫停下来，等待可以继续进行的信号到来。

最简单的信号量就是一个变量加一些并发控制的能力，这个变量是0到n之间的一个数值。当goroutine完成对此信号量的等待（wait）时，该计数值就减1，当goroutine完成对此信号量的释放（release）时，该计数值就加1。当计数值为0的时候，goroutine调用wait等待该信号量是不会成功的，除非计数器又大于0，等待的goroutine才有可能成功返回。
<div><strong>精选留言（18）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/15/a9/cb/a431bde5.jpg" width="30px"><span>木头发芽</span> 👍（5） 💬（1）<div>semaphore是用Mutex和Channel通知实现的,而Mutex又依赖于go内部的信号量实现,那这个内部的信号量又是用什么实现的?</div>2020-12-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/84/f8/c22d32b4.jpg" width="30px"><span>刚子</span> 👍（2） 💬（1）<div>不是很理解这句话 ：&quot;一次请求多个资源，这是通过 Channel 实现的信号量所不具备的。&quot;
Channel 也可以开启多个goroutine 去请求多个资源</div>2020-11-16</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/31/1e/0a/159b2129.jpg" width="30px"><span>lufofire</span> 👍（0） 💬（1）<div>
import (
	&quot;context&quot;
	&quot;errors&quot;
)

type ChannelSemaphore struct {
	ch chan struct{}
}

func NewChannelSemaphore(size int) *ChannelSemaphore {
	return &amp;ChannelSemaphore{
		ch: make(chan struct{}, size),
	}
}

func (s *ChannelSemaphore) Acquire(ctx context.Context, n int64) error {
	&#47;&#47; 判断申请数量大于容量
	if n &gt; int64(cap(s.ch)) {
		return errors.New(&quot;acquire too many&quot;)
	}

	for i := int64(0); i &lt; n; i++ {
		select {
		case s.ch &lt;- struct{}{}:
		case &lt;-ctx.Done():
			return ctx.Err()
		}
	}
	return nil
}

func (s *ChannelSemaphore) Release(ctx context.Context, n int64) error {
	&#47;&#47; 判断释放数量大于容量
	if n &gt; int64(cap(s.ch)) {
		return errors.New(&quot;release too many&quot;)
	}

	for i := int64(0); i &lt; n; i++ {
		select {
		case &lt;-s.ch:
		case &lt;-ctx.Done():
			return ctx.Err()
		}
	}
	return nil
}
</div>2024-12-25</li><br/><li><img src="" width="30px"><span>Geek_2c2c44</span> 👍（0） 💬（1）<div>基于channel的lock实现这里， Lock和UnLock的实现互换一下顺序是不是也是可以的呢？如果寻Accquire（P）是减去信号量的规范的话， 是不是lock那里把channel写在右边会更好（从channel中拿出一个信号量）？PS：前面一节的Lock顺序和这里就是不同的</div>2024-01-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/28/d8/12/ff5037ef.jpg" width="30px"><span>白开d水</span> 👍（0） 💬（1）<div>打卡</div>2023-03-23</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/GJXKh8OG00U5ial64plAIibbIuwkzhPc8uYic9Hibl8SbqvhnS2JImHgCD4JGvTktiaVnCjHQWbA5wicaxRUN5aTEWnQ/132" width="30px"><span>Geek_a6104e</span> 👍（0） 💬（1）<div>return &amp;semaphore{ch: make(chan struct{}, capacity)} 请问一下最后一个例子semaphore结构初始化为啥会多个capacity</div>2022-07-31</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/17/bf/86/c0cb35f0.jpg" width="30px"><span>8.13.3.27.30</span> 👍（0） 💬（1）<div>打卡完成</div>2022-01-06</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/30/49/f9e37ced.jpg" width="30px"><span>伟伟</span> 👍（0） 💬（6）<div>type Semaphore chan struct{}

func NewSemaphore(cap int) Semaphore {
	return make(chan struct{}, cap)
}

func (s Semaphore) Acquire(n int) {
	for i := 0; i &lt; n; i++ {
		s &lt;- struct{}{}
	}
}

func (s Semaphore) Release(n int) {
	for i := 0; i &lt; n; i++ {
		&lt;-s
	}
}

func NewSemaphore2(cap int) Semaphore {
	sem := make(chan struct{}, cap)
	for i := 0; i &lt; cap; i++ {
		sem &lt;- struct{}{}
	}
	return sem
}

func (s Semaphore) Acquire2(n int) {
	for i := 0; i &lt; n; i++ {
		&lt;-s
	}
}

func (s Semaphore) Release2(n int) {
	for i := 0; i &lt; n; i++ {
		s &lt;- struct{}{}
	}
}</div>2020-11-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/b6/5b/4486e4f9.jpg" width="30px"><span>虫子樱桃</span> 👍（0） 💬（1）<div>老师的例子里面，是通过 计算机的协程 runtime.GOMAXPROCS(0) 来模拟有限的资源（比喻例子里面的书），那么这个semaphore的场景是不是就是比较适用于请求有流量或者调用次数限制的场景呢？</div>2020-11-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/53/db/858337e3.jpg" width="30px"><span>Ethan Liu</span> 👍（0） 💬（3）<div>老师，Acquire函数为什么还会有第二个select语句？这部分逻辑是什么啊？</div>2020-11-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/83/c9/5d03981a.jpg" width="30px"><span>thomas</span> 👍（20） 💬（1）<div>补充说明下 信号量 p&#47;v的含义：
P—— passeren，中文译为&quot;通过&quot;，V—— vrijgeven，中文译为&quot;释放&quot; （因为作者是荷兰人，上面单词为荷兰语）</div>2021-01-01</li><br/><li><img src="" width="30px"><span>myrfy</span> 👍（7） 💬（1）<div>第一个问题:
至少两种，写入ch算获取，自己读取ch算获取

第二个问题应该是防止错误获取或者释放信号量时，出现负数溢出到无穷大的问题。如果溢出到无穷大，就会让信号量失效，从而导致1被保护资源更大规模的破坏</div>2020-11-16</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/4b/69/c02eac91.jpg" width="30px"><span>大漠胡萝卜</span> 👍（4） 💬（0）<div>在日常开发中，没怎么使用信号量semaphore，一般使用channel来解决这种问题。
另外，并发的时候使用池化技术感觉更加通用吧。</div>2020-11-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1d/1b/47/cf02e449.jpg" width="30px"><span>米琴香光</span> 👍（0） 💬（0）<div>type Semaphore struct {
	c        chan struct{}
	acq, rel chan []struct{}
}

func NewSemaphore(cap int) Semaphore {
	return Semaphore{
		c:   make(chan struct{}, cap),
		acq: make(chan []struct{}, 1),
		rel: make(chan []struct{}, 1),
	}
}

func (s Semaphore) Acquire(n int) {
	s.acq &lt;- make([]struct{}, n)
	for range &lt;-s.acq {
		s.c &lt;- struct{}{}
	}
}

func (s Semaphore) Release(n int) {
	s.rel &lt;- make([]struct{}, n)
	for range &lt;-s.rel {
		&lt;-s.c
	}
}</div>2024-01-15</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/26/b5/74/cd80b9f4.jpg" width="30px"><span>友</span> 👍（0） 💬（0）<div>https:&#47;&#47;github.com&#47;zzm996-zzm&#47;go-concurrent&#47;blob&#47;main&#47;semaphore&#47;semaphore.go
基于chan实现的信号量 其实和文章中的思路是一样的 不过全都是自己实现的</div>2021-08-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/26/b5/74/cd80b9f4.jpg" width="30px"><span>友</span> 👍（0） 💬（0）<div>总结一下，阻塞的操作就是依靠读取无缓冲chan来的，唤醒的操作就是把chan close掉。为了避免饥饿需要严格遵守队列条件，不会因为小就放行，必须先满足队列的第一个的需求 才会开始第二个。
两个select 就是为了双重检查，即使超时了也检查看看是否获取到了信号量。
对比纯chan的优势是 ，chan一次就只能读取一个,但是这个只需要给一个int就可以获取到对应数量是信号量 
</div>2021-08-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/d2/5e/f7f45406.jpg" width="30px"><span>容易</span> 👍（0） 💬（0）<div>老师的题还是有难度的</div>2020-11-16</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/17/6e/76b4aa3d.jpg" width="30px"><span>橙子888</span> 👍（0） 💬（0）<div>打卡。</div>2020-11-16</li><br/>
</ul>