你好，我是鸟窝。

这节课，我来给你介绍两个非常重要的扩展并发原语：SingleFlight和CyclicBarrier。SingleFlight的作用是将并发请求合并成一个请求，以减少对下层服务的压力；而CyclicBarrier是一个可重用的栅栏并发原语，用来控制一组请求同时执行的数据结构。

其实，它们两个并没有直接的关系，只是内容相对来说比较少，所以我打算用最短的时间带你掌握它们。一节课就能掌握两个“武器”，是不是很高效？

# 请求合并SingleFlight

SingleFlight是Go开发组提供的一个扩展并发原语。它的作用是，在处理多个goroutine同时调用同一个函数的时候，只让一个goroutine去调用这个函数，等到这个goroutine返回结果的时候，再把结果返回给这几个同时调用的goroutine，这样可以减少并发调用的数量。

这里我想先回答一个问题：标准库中的sync.Once也可以保证并发的goroutine只会执行一次函数f，那么，SingleFlight和sync.Once有什么区别呢？

其实，sync.Once不是只在并发的时候保证只有一个goroutine执行函数f，而是会保证永远只执行一次，而SingleFlight是每次调用都重新执行，并且在多个请求同时调用的时候只有一个执行。它们两个面对的场景是不同的，**sync.Once主要是用在单次初始化场景中，而SingleFlight主要用在合并并发请求的场景中**，尤其是缓存场景。
<div><strong>精选留言（20）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/14/54/14/84d49453.jpg" width="30px"><span>木土</span> 👍（13） 💬（1）<div>谢谢老师的文章！第一次知道有这两种并发原语，不管之后工作能不能用到，这都是对个人眼界的开阔！
ps:老师的文章几乎都是一篇顶两篇，刚订阅的时候还担心课程内容太少，现在一看担心完全是多余的，这段时间读了老师的文章之后，个人对go并发知识了解更深刻了，谢谢老师！</div>2020-11-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/2a/b9/2bf8cc89.jpg" width="30px"><span>无名氏</span> 👍（1） 💬（2）<div>CyclicBarrier 那个测试例子没有看懂，2个H，一个O顺序怎么保证是HHO😅</div>2022-03-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/04/60/64d166b6.jpg" width="30px"><span>Fan</span> 👍（1） 💬（2）<div>老师，在你github地址 https:&#47;&#47;github.com&#47;smallnest&#47;dive-to-gosync-workshop&#47;tree&#47;master&#47;7.orchestration&#47;water中没有搜到WaitGroup版本的H2O的例子，但是按照你正文中WaitGroup版本实现H2O，有报错panic: sync: WaitGroup is reused before previous Wait has returned
。请问老师这应该怎么解决呢？很困惑，望老师指点。</div>2020-12-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/04/60/64d166b6.jpg" width="30px"><span>Fan</span> 👍（1） 💬（4）<div>老师，感觉你上面用waitGroup实现这个H2O的例子有问题的。我这边运行都panic的。</div>2020-12-25</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/30/49/f9e37ced.jpg" width="30px"><span>伟伟</span> 👍（1） 💬（1）<div>package main

import (
	&quot;context&quot;

	&quot;github.com&#47;marusama&#47;cyclicbarrier&quot;
	&quot;golang.org&#47;x&#47;sync&#47;semaphore&quot;
)

type H2O2 struct {
	semaH *semaphore.Weighted
	semaO *semaphore.Weighted
	b     cyclicbarrier.CyclicBarrier
}

func New() *H2O2 {
	return &amp;H2O2{
		semaH: semaphore.NewWeighted(2),
		semaO: semaphore.NewWeighted(2),
		b:     cyclicbarrier.New(4),
	}
}

func (h2o2 *H2O2) hydrogen(releaseHydrogen func()) {
	h2o2.semaH.Acquire(context.Background(), 1)
	releaseHydrogen()
	h2o2.b.Await(context.Background())
	h2o2.semaH.Release(1)
}

func (h2o2 *H2O2) oxygen(releaseOxygen func()) {
	h2o2.semaO.Acquire(context.Background(), 1)
	releaseOxygen()
	h2o2.b.Await(context.Background())
	h2o2.semaO.Release(1)
}</div>2020-11-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/28/d8/12/ff5037ef.jpg" width="30px"><span>白开d水</span> 👍（0） 💬（2）<div>为什么在 h2o.semaH.Acquire(context.Background(), 1) 1不能换成2呢，直接请求2个资源？</div>2023-03-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/c2/6c/677005ae.jpg" width="30px"><span>李晓清</span> 👍（0） 💬（1）<div>package main

import (
	&quot;context&quot;
	&quot;fmt&quot;
	&quot;time&quot;

	&quot;github.com&#47;marusama&#47;cyclicbarrier&quot;
)

var result chan string = make(chan string, 4)

var barrier = cyclicbarrier.NewWithAction(4, func() error {
	fmt.Println(&lt;-result, &lt;-result, &lt;-result, &lt;-result)
	return nil
})

var h = func() {
	for {
		time.Sleep(1 * time.Second)
		result &lt;- &quot;H&quot;
		barrier.Await(context.TODO())
	}
}

var o = func() {
	for {
		time.Sleep(1 * time.Second)
		result &lt;- &quot;O&quot;
		barrier.Await(context.TODO())
	}
}

func main() {

	go h()
	go h()
	go o()
	go o()

	select {}
}
</div>2023-03-17</li><br/><li><img src="" width="30px"><span>Geek8956</span> 👍（0） 💬（1）<div>老师，请问循环栏栅和cond并发原语有什么区别？他们都可以让多个协程等待某个条件满足，然后并发的开始执行。</div>2021-11-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/bb/d7/91da132b.jpg" width="30px"><span>老纪</span> 👍（0） 💬（1）<div>在CyclicBarrier中，是需要一组goroutine都执行到Await()方法后，才会都向下执行否则就会阻塞在Await()方法上吗</div>2020-12-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/9b/ba/333b59e5.jpg" width="30px"><span>Linuxer</span> 👍（0） 💬（1）<div>感觉自已Go刚刚入门，我确实也才学习一周左右，看着挺爽，写起来还是不顺手，还得多练习，老师能否给我们这些打算转Go的新手一些建议，谢谢</div>2020-11-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/8f/cf/890f82d6.jpg" width="30px"><span>那时刻</span> 👍（7） 💬（0）<div>SingleFlight 能不能合并并发的写操作呢？
我觉得得分情况讨论，如果多个写请求是对于同一个对象相同的写操作，比如把某条记录的一个字段设置为某一个值，这样的话可以合并。
如果写操作是对于对象增减操作，涉及幂等行操作不太合适合并。</div>2020-11-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/53/c4/dea5d7f3.jpg" width="30px"><span>chapin</span> 👍（4） 💬（2）<div>这一节在实际项目中都直接用到。</div>2020-11-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/80/de/c6191045.jpg" width="30px"><span>gitxuzan</span> 👍（1） 💬（0）<div>package main

import (
	&quot;golang.org&#47;x&#47;sync&#47;singleflight&quot;
	&quot;log&quot;
	&quot;time&quot;
)

func main() {
	var singleSetCache singleflight.Group

	getAndSetCache := func(requestID int, cacheKey string) (string, error) {
		value, _, _ := singleSetCache.Do(cacheKey, func() (ret interface{}, err error) { &#47;&#47;do的入参key，可以直接使用缓存的key，这样同一个缓存，只有一个协程会去读DB
			log.Printf(&quot;requestid执行一次 %v &quot;, requestID)
			return &quot;VALUE&quot;, nil
		})
		return value.(string), nil
	}

	cacheKey := &quot;cacheKey&quot;
	for i := 1; i &lt; 10; i++ { &#47;&#47;模拟多个协程同时请求
		go func(requestID int) {
			value, _ := getAndSetCache(requestID, cacheKey)
			&#47;&#47;_ = value
			log.Printf(&quot;requestID %v get 值: %v&quot;, requestID, value)
		}(i)
	}
	time.Sleep(20 * time.Second)
}</div>2021-10-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/b8/3c/1a294619.jpg" width="30px"><span>Panda</span> 👍（1） 💬（0）<div>学到了     SingleFight  合并      
</div>2021-06-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/b6/5b/4486e4f9.jpg" width="30px"><span>虫子樱桃</span> 👍（1） 💬（0）<div>写了singleFlight的例子辅助思考。
package main

import (
	&quot;log&quot;
	&quot;sync&quot;
	&quot;sync&#47;atomic&quot;
	&quot;time&quot;

	&quot;golang.org&#47;x&#47;sync&#47;singleflight&quot;
)

var (
	sf           = singleflight.Group{}
	requestCount = int64(0)
	resp         = make(chan int64, 0)
	wg           sync.WaitGroup
)

func main() {
	for i := 0; i &lt; 100; i++ {
		wg.Add(1)
		go func() {
			do, err, _ := sf.Do(&quot;number&quot;, Request)
			if err != nil {
				log.Println(err)
			}
			log.Println(&quot;resp&quot;, do)
			defer wg.Done()
		}()
	}
	time.Sleep(time.Second)
	resp &lt;- atomic.LoadInt64(&amp;requestCount)
	wg.Wait()

}

func Request() (interface{}, error) {
	atomic.AddInt64(&amp;requestCount, 1)
	return &lt;-resp, nil
}</div>2020-11-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/b2/5a/574f5bb0.jpg" width="30px"><span>Lukia</span> 👍（0） 💬（0）<div>“forgotten==false，所以第 8 行默认会被调用，也就是说，第一个请求完成后，后续的同一个 key 的请求又重新开始新一次的 fn 函数的调用。”这一段逻辑可以理解 ，但是forgotten的变量命名很奇怪（感觉是名字取反了？），false的时候去删除map里的key，这个和常识相悖？</div>2022-03-05</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/61/93/3191eafa.jpg" width="30px"><span>TT</span> 👍（0） 💬（0）<div>秒啊！赶紧自己写篇文章再总结一下，老师应该不介意我抄点作业吧哈哈哈，我会注明出处的</div>2021-04-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/20/27/a6932fbe.jpg" width="30px"><span>虢國技醬</span> 👍（0） 💬（1）<div>SingleFlight 这段话 “你要注意下第 7 行。在默认情况下，forgotten==false，所以第 8 行默认会被调用，也就是说，第一个请求完成后，后续的同一个 key 的请求又重新开始新一次的 fn 函数的调用”；感觉跟开头说的 SingleFlight 并发只执行一次相矛盾；
仔细理解源码原来是这样：比如 有100个并发k都是xxx；在SingleFlight内部doCall时，开始有20个并发了，那么会执行一次，完了会删除k（xxx）；后面又有60次并发了，会在执行一次然后删除；后面又有20次并发了就会又执行一次后删除。
</div>2021-01-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/04/60/64d166b6.jpg" width="30px"><span>Fan</span> 👍（0） 💬（0）<div>老师，在你github地址 https:&#47;&#47;github.com&#47;smallnest&#47;dive-to-gosync-workshop&#47;tree&#47;master&#47;7.orchestration&#47;water中没有搜到WaitGroup版本的H2O的例子，但是按照你正文中WaitGroup版本实现H2O，有报错panic: sync: WaitGroup is reused before previous Wait has returned
。请问老师这应该怎么解决呢？很困惑，望老师指点。</div>2020-12-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/17/6e/76b4aa3d.jpg" width="30px"><span>橙子888</span> 👍（0） 💬（0）<div>打卡。</div>2020-11-18</li><br/>
</ul>