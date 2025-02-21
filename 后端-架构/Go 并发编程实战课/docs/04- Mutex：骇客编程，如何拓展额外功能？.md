你好，我是鸟窝。

前面三讲，我们学习了互斥锁Mutex的基本用法、实现原理以及易错场景，可以说是涵盖了互斥锁的方方面面。如果你能熟练掌握这些内容，那么，在大多数的开发场景中，你都可以得心应手。

但是，在一些特定的场景中，这些基础功能是不足以应对的。这个时候，我们就需要开发一些扩展功能了。我来举几个例子。

比如说，我们知道，如果互斥锁被某个goroutine获取了，而且还没有释放，那么，其他请求这把锁的goroutine，就会阻塞等待，直到有机会获得这把锁。有时候阻塞并不是一个很好的主意，比如你请求锁更新一个计数器，如果获取不到锁的话没必要等待，大不了这次不更新，我下次更新就好了，如果阻塞的话会导致业务处理能力的下降。

再比如，如果我们要监控锁的竞争情况，一个监控指标就是，等待这把锁的goroutine数量。我们可以把这个指标推送到时间序列数据库中，再通过一些监控系统（比如Grafana）展示出来。要知道，**锁是性能下降的“罪魁祸首”之一，所以，有效地降低锁的竞争，就能够很好地提高性能。因此，监控关键互斥锁上等待的goroutine的数量，是我们分析锁竞争的激烈程度的一个重要指标**。

实际上，不论是不希望锁的goroutine继续等待，还是想监控锁，我们都可以基于标准库中Mutex的实现，通过Hacker的方式，为Mutex增加一些额外的功能。这节课，我就来教你实现几个扩展功能，包括实现TryLock，获取等待者的数量等指标，以及实现一个线程安全的队列。
<div><strong>精选留言（30）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/13/d5/1f/9fbd95ac.jpg" width="30px"><span>+1day</span> 👍（24） 💬（7）<div>老师您好，在获取等待者数量的代码中
如果要加上锁持有者的数量的话，为什么不是 
v = v &gt;&gt; mutexWaiterShift + (v &amp; mutexLocked)
而是
v = v &gt;&gt; mutexWaiterShift &#47;&#47;得到等待者的数值
v = v + (v &amp; mutexLocked) &#47;&#47;再加上锁持有者的数量，0或者1
这样呢？第一步修改了 v 的值，v 的第一位已经不再是记录该锁是否被持有了，那 v&amp;mutexLocked 是不是不对呢？</div>2020-10-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/55/47/d217c45f.jpg" width="30px"><span>Panmax</span> 👍（10） 💬（4）<div>如果底层 Mutex 的 state 在某个版本中含义变了，上边写的 TryLock 和监控锁的一些方法就会失效，所以这样做是不是比较危险。</div>2020-10-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/ac/33/110437cc.jpg" width="30px"><span>不二</span> 👍（6） 💬（7）<div>请教一个基础问题，为啥 (*int32)(unsafe.Pointer(&amp;m.Mutex)) 可以获取sync.Mutex中state的值，Mutex结构中不是还有sema吗？</div>2020-10-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/24/89/c9/68457f80.jpg" width="30px"><span>天空之城</span> 👍（2） 💬（1）<div>关于 RWLock 的扩展，我这边给出一段代码（评论不好贴代码，贴个 share link）
https:&#47;&#47;go.dev&#47;play&#47;p&#47;X4YNwqZR4ta

```go
package sync

import (
	&quot;sync&quot;
	&quot;sync&#47;atomic&quot;
	&quot;unsafe&quot;
)

type RWMutex struct {
	rw sync.RWMutex
}

const (
	mutexLocked = 1 &lt;&lt; iota
	mutexWake
	mutexStarving
	mutexWaiterShift = iota
)

const (
	rwmutexMaxReaders = 1 &lt;&lt; 30
)

func (e *RWMutex) TryLock() bool {
	if e.GetReader() &lt; 0 {
		return false
	}
	e.rw.Lock()
	return true
}

&#47;&#47; readerCount &gt; 0 =&gt; Reader Hold without Writer, &lt;0 =&gt; Reader Hold and Writer waiting, ==0 =&gt; no reader
&#47;&#47; state.mutexLocked == 1 =&gt; Writer Hold (in the meanwhile, readerWaiter==0, all reader(readerCount) are waiting)
func (e *RWMutex) IsLocked() bool {
	return e.IsWriterLocked() || e.IsReaderLocked()
}

func (e *RWMutex) IsWriterLocked() bool {
	state := atomic.LoadInt32((*int32)(unsafe.Pointer(&amp;e.rw)))
	return state&amp;mutexLocked == mutexLocked
}

func (e *RWMutex) IsReaderLocked() bool {
	return atomic.LoadInt32(e.readerCountPtr()) != 0
}

func (e *RWMutex) HasWriter() bool {
	return atomic.LoadInt32(e.readerCountPtr()) &lt; 0
}

func (e *RWMutex) GetWriter() int32 {
	state := atomic.LoadInt32((*int32)(unsafe.Pointer(&amp;e.rw)))
	return int32((state &gt;&gt; mutexWaiterShift) + (state &amp; mutexLocked))
}

func (e *RWMutex) HasReader() bool {
	return atomic.LoadInt32(e.readerCountPtr()) != 0
}

func (e *RWMutex) GetReader() int32 {
	r := atomic.LoadInt32(e.readerCountPtr())
	if r &lt; 0 {
		r += rwmutexMaxReaders
	}
	return r
}

func (e *RWMutex) readerCountPtr() *int32 {
	return (*int32)(unsafe.Pointer(uintptr(unsafe.Pointer(&amp;e.rw)) + unsafe.Sizeof(sync.Mutex{}) + unsafe.Sizeof(uint32(0))*2))
}

func (e *RWMutex) readerWaitPtr() *int32 {
	return (*int32)(unsafe.Pointer(uintptr(unsafe.Pointer(&amp;e.rw)) + unsafe.Sizeof(sync.Mutex{}) + unsafe.Sizeof(uint32(0))*2 + unsafe.Sizeof((int32(0)))))
}
```

</div>2023-05-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/1c/cd/8d552516.jpg" width="30px"><span>Gojustforfun</span> 👍（2） 💬（1）<div>1）『获取等待者的数量等指标』小节，『第 15 行我们左移三位（这里的常量 mutexWaiterShift 的值为 3）』应该是右移三位。
2）在now～now+timout内，间隔重试调用TryLock</div>2020-10-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/7f/75/551c5d6c.jpg" width="30px"><span>CrazyCodes</span> 👍（1） 💬（1）<div>你可以为 Mutex 获取锁时加上 Timeout 机制吗？会有什么问题吗？

如果加上timeout机制，就不要用defer 去unlock，因为需要自行判断超时时间，然后直接unlock，如果defer再unlock就会触发panic</div>2023-11-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/50/33/9dcd30c4.jpg" width="30px"><span>斯蒂芬.赵</span> 👍（1） 💬（3）<div>fast path执行失败，直接返回false不就行了，为啥还要往下执行？正常不是多个携程并发只有一个执行成功，其他都是失败么？</div>2021-05-07</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/18/75/bc/89d88775.jpg" width="30px"><span>Calvin</span> 👍（0） 💬（1）<div>老师，TryLock 那里的以下这段代码，我对比了一下官方 1.18 以后的实现，貌似 mutexWoken 可以排除掉？
old := atomic.LoadInt32((*int32)(unsafe.Pointer(&amp;m.Mutex)))
if old&amp;(mutexLocked|mutexStarving|mutexWoken) != 0 {
	return false
}

官方的实现：
old := m.state
if old&amp;(mutexLocked|mutexStarving) != 0 {	&#47;&#47; 这里和本课程文章中的差别是少了 |mutexWoken
    return false
}

&#47;&#47; There may be a goroutine waiting for the mutex, but we are
&#47;&#47; running now and can try to grab the mutex before that
&#47;&#47; goroutine wakes up.
if !atomic.CompareAndSwapInt32(&amp;m.state, old, old|mutexLocked) {
	return false
}

if race.Enabled {
	race.Acquire(unsafe.Pointer(m))
}
return true</div>2024-05-20</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/DYAIOgq83erHzX39iazGeL5dIlBMibiaMTfXdzSfiamgCbAPZEx5QyQkIyBz1YqMWAgxGaWzT16UgowQgwY5uXGdeQ/132" width="30px"><span>路过</span> 👍（0） 💬（1）<div>想问一下，为什么最后实现线程安全的队列里面的 Dequeue() 方法释放锁不用defer，这样不用写两次unlock</div>2023-04-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/23/ac/55/80dc6b48.jpg" width="30px"><span>鲁迅原名周树人</span> 👍（0） 💬（2）<div>老师您好，

&#47;&#47; 如果能成功抢到锁 if atomic.CompareAndSwapInt32((*int32)(unsafe.Pointer(&amp;m.Mutex)), 0, mutexLocked) { return true }

在以上代码中，(*int32)(unsafe.Pointer(&amp;m.Mutex))是取的Mutex中state的首地址对嘛?
</div>2021-05-03</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/b0/c3/e1e2c097.jpg" width="30px"><span>黄毅</span> 👍（0） 💬（1）<div>func (m *Mutex) TryLock() bool {
	&#47;&#47; 如果能成功抢到锁
	if atomic.CompareAndSwapInt32((*int32)(unsafe.Pointer(&amp;m.Mutex)), 0, mutexLocked) {
		return true
	}

	&#47;&#47; 如果处于唤醒、加锁或者饥饿状态，这次请求就不参与竞争了，返回false
	old := atomic.LoadInt32((*int32)(unsafe.Pointer(&amp;m.Mutex)))
	fmt.Println(&quot;===old===:&quot;, old)
	if old&amp;(mutexLocked|mutexStarving|mutexWoken) != 0 {
		return false
	}

	&#47;&#47; 尝试在竞争的状态下请求锁
	new := old | mutexLocked
	fmt.Println(&quot;===new===:&quot;, new) &#47;&#47;请问在什么情况下会执行到这里
	return atomic.CompareAndSwapInt32((*int32)(unsafe.Pointer(&amp;m.Mutex)), old, new)
}

func main() {
	var mu Mutex
	go func() { &#47;&#47; 启动一个goroutine持有一段时间的锁
		mu.Lock()
		time.Sleep(time.Duration(rand.Intn(2)) * time.Second)
		mu.Unlock()
	}()

	time.Sleep(time.Second)

	n := int(10)
	var wg sync.WaitGroup
	wg.Add(n)

	for i := 0; i &lt; n; i++ {
		go func() {
			ok := mu.TryLock() &#47;&#47; 尝试获取到锁
			defer wg.Done()
			if ok { &#47;&#47; 获取成功
				fmt.Println(&quot;got the lock&quot;)
				&#47;&#47; do something
				mu.Unlock()
				return
			}
		}()
	}
	&#47;&#47; 没有获取到
	wg.Wait()
}

老师，你好。在main中尝试编写一段逻辑测试TryLock方法，请问在什么情况下会执行fmt.Println(&quot;===new===:&quot;, new) 请老师答疑解惑，谢谢。</div>2020-11-16</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/05/bf/cc9d43ae.jpg" width="30px"><span>樊少</span> 👍（0） 💬（1）<div>在安全Queue的实现中，锁的释放为什么不用defer?</div>2020-11-05</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/5a/11/1f0d54f8.jpg" width="30px"><span>Chen</span> 👍（0） 💬（1）<div>第 15 行我们右移三位（这里的常量 mutexWaiterShift 的值为 3），就得到了当前等待者的数量
=&gt;&gt; 这里看不懂，为什么右移三位=》得到等待者数量</div>2020-10-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/5c/88/222d946e.jpg" width="30px"><span>linxs</span> 👍（0） 💬（3）<div>TryLock方法内，对于这段代码有点不理解，为什么要把&amp;m.Mutex转换成*int32，这里的话我直接用&amp;m.Mutex.state是否是一样的

if atomic.CompareAndSwapInt32((*int32)(unsafe.Pointer(&amp;m.Mutex)), 0, mutexLocked) { 
     return true 
}</div>2020-10-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/ab/a9/590d6f02.jpg" width="30px"><span>Junes</span> 👍（34） 💬（2）<div>我来提供个思路~

最简单直接的是采用channel实现，用select监听锁和timeout两个channel，不在今天的讨论范围内。

1. 用for循环+TryLock实现：
先记录开始的时间，用for循环判断是否超时：没有超时则反复尝试tryLock，直到获取成功；如果超时直接返回失败。

问题：高频的CAS自旋操作，如果失败的太多，会消耗大量的CPU。

2. 优化1：TryLock的fast的拆分
TryLock的抢占实现分为两部分，一个是fast path，另一个是竞争状态下的，后者的cas操作很多。我会考虑减少slow方法的频率，比如调用n次fast path失败后，再调用一次整个Trylock。

3. 优化2：借鉴TCP重试机制
for循环中的重试增加休眠时间，每次失败将休眠时间乘以一个系数（如1.5），直到达到上限（如10ms），减少自旋带来的性能损耗</div>2020-10-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/22/03/fc/daa02847.jpg" width="30px"><span>18</span> 👍（17） 💬（1）<div>我变秃了，也变强了</div>2020-10-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/17/6e/76b4aa3d.jpg" width="30px"><span>橙子888</span> 👍（5） 💬（0）<div>认真消化完前三章后看今天的这章感觉容易多了。</div>2020-10-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/22/17/11/a63acc6a.jpg" width="30px"><span>( ･᷄ὢ･᷅ )</span> 👍（4） 💬（0）<div>可以通过Context.WithTimeout进行超时机制添加 也可以通过select time.After配合使用</div>2020-10-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/19/8e/f0/18720510.jpg" width="30px"><span>50%</span> 👍（3） 💬（2）<div>type Mutex struct {
	sync.Mutex
}
var m Mutex
	fmt.Printf(&quot;%+v\n&quot;, unsafe.Pointer(&amp;m))
	&#47;&#47;state 字段 先得到m中sync.Mutex字段的地址 再用int32类型的指针获取state字段
	fmt.Printf(&quot;%+v\n&quot;, (*int32)(unsafe.Pointer(&amp;m.Mutex)))
	&#47;&#47;sema 字段 先得到m中sync.Mutex字段的地址 + state（int32类型）所占的内存地址（偏移量）得到sema的字段的起始地址 在转换int32类型的指针获取sema字段
	&#47;&#47;fmt.Printf(&quot;%+v\n&quot;, unsafe.Sizeof(uint32(0)))
	fmt.Printf(&quot;%+v\n&quot;, (*uint32)(unsafe.Pointer(uintptr(unsafe.Pointer(&amp;m.Mutex))+unsafe.Sizeof(int32(0)))))</div>2020-11-02</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/17/2a/e6/c788257f.jpg" width="30px"><span>geek_arong2048</span> 👍（1） 💬（0）<div>timeout实现：
1、select+time.After
2、for自旋+时间戳判断</div>2021-06-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/51/ec/3d51d5e6.jpg" width="30px"><span>上校</span> 👍（1） 💬（0）<div>你可以为 Mutex 获取锁时加上 Timeout 机制吗？会有什么问题吗？

希望老师抽时间把相关的课后思考题解答下，从经验和工作中遇到的问题肯定不如老师理解的深刻，老师辛苦了</div>2021-05-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/c1/0e/2b987d54.jpg" width="30px"><span>蜉蝣</span> 👍（1） 💬（0）<div>老师好。在 trylock 中，我想不明白为什么在唤醒状态下也要直接 return 出去，是因为如果唤醒状态下取得锁会破坏原有的 Mutex 处理逻辑吗？我看如果 trylock 在唤醒取得锁，并且不清除 Mutex 的唤醒标记，对 Mutex 的处理不会有影响，但如果清除了，会造成一些走 Lock 方法的 goroutine 误以为是自己取得了锁（atomic.CompareAndSwapInt32(&amp;m.state, old, new) &amp;&amp; (old&amp;(mutexLocked|mutexStarving))）。不知道我的理解对不对。</div>2020-11-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/67/dd/55aa6e07.jpg" width="30px"><span>罗帮奎</span> 👍（1） 💬（0）<div>感觉可以把timeout分小段，每过一小段时间尝试拿锁，要不然一直卡在自旋拿锁会很耗cpu</div>2020-10-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/9b/ba/333b59e5.jpg" width="30px"><span>Linuxer</span> 👍（1） 💬（0）<div>通过tryLock-&gt;sleep-&gt;tryLock存在的问题是，可能sleep过程中就能获取到锁，但是不得不等设定的时长，如果间隔一段时间就尝试，有可能实际拿不到锁而浪费CPU</div>2020-10-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/1c/cd/8d552516.jpg" width="30px"><span>Gojustforfun</span> 👍（1） 💬（0）<div>TryLock方法中27行表示的是：
1）在锁的瞬时状态为正常模式+无唤醒的等待者+锁未被持有时，当前goroutine与等待队列中队头goroutine一起竞争（此时等待者队列不为空）。
2）与TryLock的fast path一样，锁的瞬时状态为正常模式+无唤醒的等待者+锁未被持有+等待队列为空。此时无竞争，直接获取到锁。

&#47;&#47; 尝试在竞争的状态下请求锁 
new := old | mutexLocked 
return atomic.CompareAndSwapInt32((*int32(unsafe.Pointer(&amp;m.Mutex)), old, new)</div>2020-10-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/0a/a4/828a431f.jpg" width="30px"><span>张申傲</span> 👍（0） 💬（0）<div>对于 Mutex 的理解更深入了一层</div>2022-04-06</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/2b/e0/61/53a17039.jpg" width="30px"><span>tourist</span> 👍（0） 💬（0）<div>不知道其他语言怎么搞，但看完Go写的，感觉Go确实挺简洁的</div>2022-02-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/d2/94/c7223eb8.jpg" width="30px"><span>白志稳</span> 👍（0） 💬（1）<div>每次思考题的答案在哪呀？有没有老师的标准答案？只看评论区也不知道谁的对啊？
v = v &gt;&gt; mutexWaiterShift &#47;&#47;得到等待者的数值 
v = v + (v &amp; mutexLocked) &#47;&#47;再加上锁持有者的数量，0或者1
这个地方能再解释一下吗？怎么拆出来的那几个字段？</div>2021-09-03</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/60/57/6a53393a.jpg" width="30px"><span>关东燕雀寇关来</span> 👍（0） 💬（0）<div>time.Sleep(time.Duration(rand.Intn(2)) * time.Second)前没有time.Seed() 导致随机数失效</div>2021-06-03</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/50/33/9dcd30c4.jpg" width="30px"><span>斯蒂芬.赵</span> 👍（0） 💬（0）<div>v = v + (v &amp; mutexLocked) &#47;&#47;再加上锁持有者的数量，0或者1 这块的逻辑是不是写的有问题，判断是否上锁不应该用state := atomic.LoadInt32((*int32)(unsafe.Pointer(&amp;m.Mutex))) return state&amp;mutexLocked == mutexLocked 来判断么，v &amp; mutexLocked) v 这时候代表的是锁等待着的数量，不是state当前的状态</div>2021-05-17</li><br/>
</ul>