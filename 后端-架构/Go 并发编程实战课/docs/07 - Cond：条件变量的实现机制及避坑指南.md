你好，我是鸟窝。

在写Go程序之前，我曾经写了10多年的Java程序，也面试过不少Java程序员。在Java面试中，经常被问到的一个知识点就是等待/通知（wait/notify）机制。面试官经常会这样考察候选人：请实现一个限定容量的队列（queue），当队列满或者空的时候，利用等待/通知机制实现阻塞或者唤醒。

在Go中，也可以实现一个类似的限定容量的队列，而且实现起来也比较简单，只要用条件变量（Cond）并发原语就可以。Cond并发原语相对来说不是那么常用，但是在特定的场景使用会事半功倍，比如你需要在唤醒一个或者所有的等待者做一些检查操作的时候。

那么今天这一讲，我们就学习下Cond这个并发原语。

## Go标准库的Cond

Go标准库提供Cond原语的目的是，为等待/通知场景下的并发问题提供支持。Cond通常应用于等待某个条件的一组goroutine，等条件变为true的时候，其中一个goroutine或者所有的goroutine都会被唤醒执行。

顾名思义，Cond是和某个条件相关，这个条件需要一组goroutine协作共同完成，在条件还没有满足的时候，所有等待这个条件的goroutine都会被阻塞住，只有这一组goroutine通过协作达到了这个条件，等待的goroutine才可能继续进行下去。
<div><strong>精选留言（30）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/11/8f/cf/890f82d6.jpg" width="30px"><span>那时刻</span> 👍（13） 💬（1）<div>老师，上节课你提到noCopy，是一个辅助的、用来帮助 vet 检查用的类型，而Cond还有个copyChecker 是一个辅助结构，可以在运行时检查 Cond 是否被复制使用。

nocpoy是静态检查，copyChecker是运行时检查，不是理解是否正确？

另外不是是否有其他区别呢？</div>2020-10-26</li><br/><li><img src="" width="30px"><span>myrfy</span> 👍（4） 💬（1）<div>还是没有想明白k8s为什么不能用channel通知
close可以实现broadcast的功效，在pop的时候，也是只有一个goroutine可以拿到数据，感觉除了关闭队列之外，不存在需要broadcast的情况。也就是感觉不需要多次broadcast，这样channel应该是满足要求的……请老师明示</div>2020-10-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/e2/c0/e7a59706.jpg" width="30px"><span>chongsheng</span> 👍（2） 💬（1）<div>关于Cond还有一种会不小心误用的场景，因为一些原因导致Wait执行的时候，Signal&#47;Broadcast就已经执行完了，导致Wait一直等待无法唤醒。比如这里的例子
https:&#47;&#47;stackoverflow.com&#47;questions&#47;36857167&#47;how-to-correctly-use-sync-cond</div>2022-01-06</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/62/dc/8876c73b.jpg" width="30px"><span>moooofly</span> 👍（1） 💬（2）<div>请教一个问题，nocpoy 是用于 vet 静态检查，copyChecker 是为了运行时检查，都是为了检查 copy 问题，为啥 Cond 要在两处检查，而 Mutex 只需要一处？</div>2020-10-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/3d/c5/c6/9592c42c.jpg" width="30px"><span>hhhccp</span> 👍（0） 💬（1）<div>不知道现在发还会不会被看到😂，浇给作业
package main

import (
	&quot;fmt&quot;
	&quot;sync&quot;
	&quot;sync&#47;atomic&quot;
)

type TaskQueue struct {
	q        []interface{}
	capacity int
	size     int32
	front    int
	rear     int
	popLock  sync.Mutex
	pushLock sync.Mutex
	pushCon  *sync.Cond
	popCon   *sync.Cond
}

func NewTaskQueue(capacity int) *TaskQueue {
	tq := &amp;TaskQueue{
		q: make([]interface{}, capacity),
		capacity: capacity,
		front: 0,
		rear: 0,
		size: 0,
	}
	tq.pushCon = sync.NewCond(&amp;tq.pushLock)
	tq.popCon = sync.NewCond(&amp;tq.popLock)
	return tq
} 

func (tq *TaskQueue) Size() int {
	return int(atomic.LoadInt32(&amp;tq.size))
}

func (tq *TaskQueue) PushTask(v interface{}) {
	tq.pushLock.Lock()
	defer tq.pushLock.Unlock()
	for tq.Size() == tq.capacity {
		tq.pushCon.Wait()
	}

	tq.q[tq.rear] = v
	tq.rear = (tq.rear + 1) % tq.capacity
	atomic.AddInt32(&amp;tq.size, 1)
	tq.popCon.Signal()
}

func (tq *TaskQueue) PopTask() interface{} {
	tq.popLock.Lock()
	defer tq.popLock.Unlock()
	for tq.Size() == 0 {
		tq.popCon.Wait()
	}

	v := tq.q[tq.front]
	tq.front = (tq.front + 1) % tq.capacity
	atomic.AddInt32(&amp;tq.size, -1)
	tq.pushCon.Signal()
	return v
}</div>2024-12-01</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/17/2f/78/67512fcd.jpg" width="30px"><span>叶君度</span> 👍（0） 💬（1）<div>对比waitGroup。cond 实质是将waitGroup 的 计数能力 暴露给开发者，让开发自定义”计数”，waitGroup的计数state是atomic的原子操作，cond 通过 mutex来保证原子操作。所以在 更新 和 判断时，需要加锁检查。</div>2024-04-16</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/3a/08/fb/791d0f5e.jpg" width="30px"><span>Krean</span> 👍（0） 💬（1）<div>不知道现在发还会不会被看到😂，浇给作业
type queue struct {
	vals []int
	cap int
	cond *sync.Cond
}

func (q *queue) enQueue(v int) {
	if q.cap == len(q.vals) {
		q.cond.L.Lock()
		q.cond.Wait()
		q.cond.L.Unlock()
	}
	q.vals = append(q.vals, v)
	q.cond.Signal()
}

func (q *queue) deQueue() int {
	if len(q.vals) == 0 {
		q.cond.L.Lock()
		q.cond.Wait()
		q.cond.L.Unlock()
	}
	ret := q.vals[0]
	q.vals = q.vals[1:]
	q.cond.Signal()
	return ret
}</div>2024-03-22</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/DYAIOgq83eoo6hOiaqGVOPOpicY4tKZZCSlNawfxSJ6jgYtLnYj0ByD3s5kUDwwV7wUSMsiar0Z3HRzl7rMiaAbr5w/132" width="30px"><span>kyo</span> 👍（0） 💬（2）<div>
func main() {
    c := sync.NewCond(&amp;sync.Mutex{})
    var ready int

    for i := 0; i &lt; 10; i++ {
        go func(i int) {
            time.Sleep(time.Duration(rand.Int63n(10)) * time.Second)

            &#47;&#47; 加锁更改等待条件
            c.L.Lock()
            ready++
            c.L.Unlock()

            log.Printf(&quot;运动员#%d 已准备就绪\n&quot;, i)
            &#47;&#47; 广播唤醒所有的等待者
            c.Broadcast()
        }(i)
    }

    c.L.Lock()
    for ready != 10 {
        c.Wait()
        log.Println(&quot;裁判员被唤醒一次&quot;)
    }
    c.L.Unlock()

    &#47;&#47;所有的运动员是否就绪
    log.Println(&quot;所有运动员都准备就绪。比赛开始，3，2，1, ......&quot;)
}

这个例子有问题吧.  这里的 ready 变量共享了变量 c 的锁.  会导致在 c.Wait() 语句执行前 for 中的   goroutine 全部堵塞. 在 c.Wait() 前加句 time.Sleep(time.Second * 10) 试试就知道了. 是不是应该给 ready 变量单独定义一个 Mutex?</div>2022-12-04</li><br/><li><img src="" width="30px"><span>Geek_b45293</span> 👍（0） 💬（1）<div>有个问题，为什么 Mutex 不使用 copyChecker 来检测是否被复制呢？</div>2022-09-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/37/92/961ba560.jpg" width="30px"><span>授人以🐟，不如授人以渔</span> 👍（0） 💬（1）<div>文章中在描述 Cond 的复杂性时，说明了 3 点，第三点：「条件变量的更改」 是否可需改为：「等待条件的更改」？</div>2021-11-03</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/ba/ce/fd45714f.jpg" width="30px"><span>bearlu</span> 👍（0） 💬（1）<div>老师请教一个问题，如果Wait前加锁，然后执行完Wait又Unlock有什么作用，我把Wait后面的Unlock去掉，好似程序也能正常运行。是我漏了什么？</div>2021-07-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/f5/14/92b373dd.jpg" width="30px"><span>网管</span> 👍（0） 💬（1）<div>老师，Kubernetes  PriorityQueue的那个Pop方法里没有使用p.cond.L.Lock()方法，他们是怎么防止不出现释放未加锁的panic啊。</div>2020-11-01</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/34/3e/0b1c2b7f.jpg" width="30px"><span>S.S Mr Lin</span> 👍（0） 💬（2）<div>每次调用wait前都要加锁，为啥加锁语句放在了fo的外面？第二次wait是不是就没有加锁了？</div>2020-10-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/8d/87/47d95f4a.jpg" width="30px"><span>syuan</span> 👍（0） 💬（1）<div>Wait 方法，会把调用者 Caller 放入 Cond 的等待队列中并阻塞，直到被 Signal 或者 Broadcast 的方法从等待队列中移除并唤醒。
百米跑代码第22行:    c.Wait(),把调用者加入队列阻塞，不理解? for循环一直检查，是把c一直加入阻塞队列吗？还是waiter方法自已生成t对象加入阻塞队列？如果是，同一个c对应t( t := runtime_notifyListAdd(&amp;c.notify)对象唯一吗？</div>2020-10-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/4c/f1/8dc266ee.jpg" width="30px"><span>儿戏</span> 👍（0） 💬（1）<div>老师，请教个课程外的问题，使用httputil.ReverseProxy 做方向代理，压测的时候大量报出 http: proxy error: context canceled 这个错误。linux 打开文件数调整了，time_waite也都优化过了，一直没有找到问题，您的博客也看了还是不能定位，求赐教</div>2020-10-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/7c/cf/d5382404.jpg" width="30px"><span>RRR</span> 👍（0） 💬（1）<div>感觉 Cond 是不是和 Java 中的 notify &#47; wait 机制对应而存在的呢？Golang 和 Java 的异步模式最大的区别是不是就在这里呢？</div>2020-10-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/1c/cd/8d552516.jpg" width="30px"><span>Gojustforfun</span> 👍（32） 💬（3）<div>思考题：
1. 唤醒的方式有broadcast，第N个waiter被唤醒后需要检查等待条件，因为不知道前N-1个被唤醒的waiter所作的修改是否使等待条件再次成立。
2. 以下是我实现的一个，有限容量Queue，欢迎讨论！
https:&#47;&#47;play.studygolang.com&#47;p&#47;11K2iPVYErn

package main

import (
	&quot;fmt&quot;
	&quot;math&#47;rand&quot;
	&quot;strings&quot;
	&quot;sync&quot;
)

type Queue struct {
	cond *sync.Cond
	data []interface{}
	capc int
	logs []string
}

func NewQueue(capacity int) *Queue {
	return &amp;Queue{cond: &amp;sync.Cond{L: &amp;sync.Mutex{}}, data: make([]interface{}, 0), capc: capacity, logs: make([]string, 0)}
}

func (q *Queue) Enqueue(d interface{}) {
	q.cond.L.Lock()
	defer q.cond.L.Unlock()

	for len(q.data) == q.capc {
		q.cond.Wait()
	}
	&#47;&#47; FIFO入队
	q.data = append(q.data, d)
	&#47;&#47; 记录操作日志
	q.logs = append(q.logs, fmt.Sprintf(&quot;En %v\n&quot;, d))
	&#47;&#47; 通知其他waiter进行Dequeue或Enqueue操作
	q.cond.Broadcast()

}

func (q *Queue) Dequeue() (d interface{}) {
	q.cond.L.Lock()
	defer q.cond.L.Unlock()

	for len(q.data) == 0 {
		q.cond.Wait()
	}
	&#47;&#47; FIFO出队
	d = q.data[0]
	q.data = q.data[1:]
	&#47;&#47; 记录操作日志
	q.logs = append(q.logs, fmt.Sprintf(&quot;De %v\n&quot;, d))
	&#47;&#47; 通知其他waiter进行Dequeue或Enqueue操作
	q.cond.Broadcast()
	return
}

func (q *Queue) Len() int {
	q.cond.L.Lock()
	defer q.cond.L.Unlock()
	return len(q.data)
}

func (q *Queue) String() string {
	var b strings.Builder
	for _, log := range q.logs {
		&#47;&#47;fmt.Fprint(&amp;b, log)
		b.WriteString(log)
	}
	return b.String()
}</div>2020-10-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/ac/66/a256008b.jpg" width="30px"><span>SuperDai</span> 👍（4） 💬（0）<div>上一个自己的实现

package caplimitqueue

import (
	&quot;sync&quot;

	&quot;github.com&#47;gammazero&#47;deque&quot;
)

&#47;&#47; CapLimitQueue 限容队列
type CapLimitQueue struct {
	cond *sync.Cond
	q    deque.Deque
	cap  int
}

&#47;&#47; NewCapLimitQueue 返回CapLimitQueue实例.
func NewCapLimitQueue(cap int) *CapLimitQueue {
	if cap == 0 {
		cap = 64
	}
	q := &amp;CapLimitQueue{
		cap: cap,
	}
	q.cond = sync.NewCond(&amp;sync.Mutex{})
	return q
}

&#47;&#47; Push 往限容队列添加数据对象.
func (q *CapLimitQueue) Push(elem interface{}) {
	q.cond.L.Lock()
	for q.q.Len() &gt;= q.cap {
		&#47;&#47; (1) 队列已满, 等待消费goroutine取出数据对象.
		q.cond.Wait()
	}
	defer q.cond.L.Unlock()

	q.q.PushBack(elem)
	&#47;&#47; (2) 通知消费goroutine已有数据对象进队列 -&gt; (3)
	q.cond.Broadcast()
}

&#47;&#47; Pop 从限容队列取出数据对象.
func (q *CapLimitQueue) Pop(want int) []interface{} {
	q.cond.L.Lock()
	for q.q.Len() == 0 {
		&#47;&#47; (3) 队列为空, 等待生产goroutine添加数据对象.
		q.cond.Wait()
	}
	defer q.cond.L.Unlock()

	if want &gt; q.q.Len() {
		want = q.q.Len()
	}
	output := make([]interface{}, want)
	for i := 0; i &lt; want; i++ {
		output[i] = q.q.PopFront()
	}
	&#47;&#47; (4) 通知生产goroutine已有数据对象出队列 -&gt; (1)
	q.cond.Broadcast()

	return output
}

&#47;&#47; Len 返回限容队列当前长度.
func (q *CapLimitQueue) Len() int {
	q.cond.L.Lock()
	defer q.cond.L.Unlock()
	return q.q.Len()
}
</div>2020-11-03</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/ab/a9/590d6f02.jpg" width="30px"><span>Junes</span> 👍（3） 💬（1）<div>1. 是否需要等待，是看业务实现的需求吧：
每个caller会唤醒一个或者所有的waiter
caller和waiter的数量对应是不确定的，如N:M
waiter唤醒后的处理逻辑是自己决定的，比如示例中的ready和队列长度

2. 有长度限制的队列，代码可以参考示例中的PriorityQueue
Push入队Broadcast，Pop出队Wait
队列长度有限制的话，在Dueue中维护一个变量size，当前队列长度大于等于size时，Push操作直接返回错误
改造：如果希望Dueue满时Push操作阻塞，可以在Push用个Wait来阻塞，收到Broadcast后，检测到当前队列小于size就Push
附上一块伪代码

&#47;&#47; 从队列中取出一个元素
func (p *Dueue) Pop() (interface{}, error) {
	p.lock.Lock()
	defer p.lock.Unlock()

	&#47;&#47; 如果队列为空,等待，直到被唤醒
	for p.queue.Len() == 0 {
		p.cond.Wait()
	}
	return p.queue.Pop()
}

&#47;&#47; 增加元素到队列中(非阻塞方式)
func (p *Dueue) Push(e interface{}) error {
	p.lock.Lock()
	defer p.lock.Unlock()

	&#47;&#47; 如果队列满了，直接返回error(阻塞改造：在Pop中添加个Broadcast方法，这里改造成for循环进行wait)
	if p.queue.Len() &gt;= p.maxSize {
		return fmt.Errorf(&quot;over size&quot;)
	}

	&#47;&#47; 把元素加入到队列后，通知所有的waiter
	p.queue.Push(e)
	p.cond.Broadcast()
	return nil
}
</div>2020-10-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/09/42/1f762b72.jpg" width="30px"><span>Hurt</span> 👍（1） 💬（0）<div>打卡</div>2020-11-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/20/27/a6932fbe.jpg" width="30px"><span>虢國技醬</span> 👍（1） 💬（2）<div>第一个思考题其实不难，其他goroutine只是ready++后唤醒，如果等待的主goroutine不检查条件变量，主goroutine在第一次唤醒时就继续执行了！也就体现不出条件变量的“条件”了</div>2020-11-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/26/27/eba94899.jpg" width="30px"><span>罗杰</span> 👍（1） 💬（1）<div>文章虽然看明白了，但是要完成思考题还是有一定的难度的。
</div>2020-10-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/f8/ba/d28174a9.jpg" width="30px"><span>Geek_zbvt62</span> 👍（1） 💬（0）<div>第一题的答案应该应该还包括spurious wakeup的因素</div>2020-10-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/c9/11/3b678d53.jpg" width="30px"><span>淡漠</span> 👍（0） 💬（0）<div>type queueWithCond struct {
	cond  sync.Cond
	limit int32
	index int32 &#47;&#47; 索引,记录下一个数据插入的位置
	data  []interface{}
}

func newQueueWithCond(limit int32) *queueWithCond {
	return &amp;queueWithCond{
		cond:  sync.Cond{L: new(sync.Mutex)},
		limit: limit,
		data:  make([]interface{}, limit, limit),
	}
}

func (q *queueWithCond) push(v interface{}) {
	&#47;&#47; wait前加锁
	q.cond.L.Lock()
	defer q.cond.L.Unlock()
	&#47;&#47; 超过数量，阻塞等待
	for atomic.LoadInt32(&amp;q.index) == q.limit {
		q.cond.Wait()
	}
	index := atomic.LoadInt32(&amp;q.index)
	&#47;&#47; 插入数据
	q.data[index] = v
	&#47;&#47; 索引+1
	atomic.AddInt32(&amp;q.index, 1)
	&#47;&#47;q.index = index + 1
	&#47;&#47; 唤醒一个等待的协程
	q.cond.Broadcast()
}

func (q *queueWithCond) pop() interface{} {
	q.cond.L.Lock()
	defer q.cond.L.Unlock()
	&#47;&#47; 空，阻塞等待
	for atomic.LoadInt32(&amp;q.index) == 0 {
		q.cond.Wait()
	}
	v := q.data[0]
	index := atomic.LoadInt32(&amp;q.index)
	&#47;&#47; 数据移动
	for i := 0; i &lt; int(index)-1; i++ {
		q.data[i] = q.data[i+1]
	}
	atomic.AddInt32(&amp;q.index, -1)
	&#47;&#47;q.index = index - 1
	q.cond.Broadcast()
	return v
}</div>2024-04-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/e2/c0/e7a59706.jpg" width="30px"><span>chongsheng</span> 👍（0） 💬（0）<div>关于Cond还有一种不小心误用的场景，就是在Wait()调用之前，Signal&#47;Broadcast就执行完了，导致一直Wait()。比如这里的例子</div>2022-01-06</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/cf/cc/8de5007b.jpg" width="30px"><span>徐改</span> 👍（0） 💬（0）<div>关于思考题2：
我使用了环形队列，用来避免线性队列队满情况下因数据搬移而带来的时间开销:
&#47; 环形队列，实现阻塞、通知机制
func (queue *PriorityQueue) Add(v interface{}) {
	queue.cond.L.Lock()
	defer queue.cond.L.Unlock()
	&#47;&#47; 判断队满
	if (queue.tail + 1) % cap(queue.item) == queue.head {
		fmt.Println(&quot;生产者被阻塞&quot;)
		queue.cond.Wait()
		fmt.Println(&quot;生产者被唤醒&quot;)
	}
	fmt.Println(&quot;生产者生产数据&quot;)
	queue.item[queue.tail] = v
	queue.tail = (queue.tail + 1) % cap(queue.item)
	queue.cond.Broadcast()
}

func (queue *PriorityQueue) Pop() interface{} {
	queue.cond.L.Lock()
	defer queue.cond.L.Unlock()
	&#47;&#47; 判断队空
	if queue.tail == queue.head {
		fmt.Println(&quot;消费者被阻塞&quot;)
		queue.cond.Wait()
		fmt.Println(&quot;消费者被唤醒&quot;)
	}
	fmt.Println(&quot;消费者消费数据&quot;)
	v := queue.item[queue.head]
	queue.head = (queue.head + 1) % cap(queue.item)
	queue.cond.Broadcast()
	return v
}</div>2021-10-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/f2/15/c5be3083.jpg" width="30px"><span>Allen</span> 👍（0） 💬（0）<div>package main

import (
	&quot;fmt&quot;
	&quot;sync&quot;
	&quot;time&quot;

	&quot;go.uber.org&#47;atomic&quot;
)

type CondQue struct {
	c    *sync.Cond
	size int
	list []int
}

func NewCondQue(size int) *CondQue {
	return &amp;CondQue{size: size, c: sync.NewCond(&amp;sync.Mutex{})}
}

func (q *CondQue) Add(item int) {
	q.c.L.Lock()
	defer q.c.L.Unlock()
	for len(q.list) &gt;= q.size { &#47;&#47; 当前队列长度已满
		q.c.Wait() &#47;&#47; 等待
		fmt.Printf(&quot;wait for add:%v\n&quot;, item)
	}
	q.list = append(q.list, item)
	q.c.Broadcast()
	fmt.Printf(&quot;add:%v cur len:%v\n&quot;, item, len(q.list))
}

func (q *CondQue) Pop() int {
	q.c.L.Lock()
	defer q.c.L.Unlock()
	for len(q.list) &lt;= 0 { &#47;&#47; 当前队列长度已空
		q.c.Wait() &#47;&#47; 等待
		fmt.Printf(&quot;wait for pop\n&quot;)
	}

	item := q.list[0]
	q.list = q.list[1:]
	fmt.Printf(&quot;pop:%v cur len:%v\n&quot;, item, len(q.list))
	return item
}

func main() {
	cond := NewCondQue(2)
	var g atomic.Int32
	for i := 0; i &lt; 3; i++ {
		go func() {
			for {
				g.Add(1)
				cond.Add(int(g.Load()))
				time.Sleep(time.Second * 1)
			}
		}()
	}
	for i := 0; i &lt; 2; i++ {
		go func() {
			for {
				_ = cond.Pop()
				time.Sleep(time.Millisecond * 500)
			}
		}()
	}
	time.Sleep(time.Second * 10)
}
</div>2021-09-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/00/4e/be2b206b.jpg" width="30px"><span>吴小智</span> 👍（0） 💬（0）<div>想问老师，为什么 ready 在 Wait 之后处理，会有死锁的时候发生？
c.L.Lock()
for ready != 10 {
	c.Wait()
	ready ++
	fmt.Println(&quot;裁判员被唤醒&quot;,ready)
}
c.L.Unlock()
</div>2021-07-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/57/d8/425e1b0a.jpg" width="30px"><span>小虾米</span> 👍（0） 💬（0）<div>如果在执行    runtime_notifyListWait(&amp;c.notify, t)之前有其他协程broadcast了，会不会永远不会醒来了？</div>2021-05-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/09/9d/8af6cb1e.jpg" width="30px"><span>臭猫</span> 👍（0） 💬（0）<div>k8s里，p.lock.Lock() 这个在wait之前的锁，并不是p.cock.L.Lock()，这样不会有问题？</div>2020-12-11</li><br/>
</ul>