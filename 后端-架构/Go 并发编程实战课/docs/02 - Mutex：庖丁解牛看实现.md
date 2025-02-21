你好，我是鸟窝。

上一讲我们一起体验了Mutex的使用，竟是那么简单，只有简简单单两个方法，Lock和Unlock，进入临界区之前调用Lock方法，退出临界区的时候调用Unlock方法。这个时候，你一定会有一丝好奇：“它的实现是不是也很简单呢？”

其实不是的。如果你阅读Go标准库里Mutex的源代码，并且追溯Mutex的演进历史，你会发现，从一个简单易于理解的互斥锁的实现，到一个非常复杂的数据结构，这是一个逐步完善的过程。Go开发者们做了种种努力，精心设计。我自己每次看，都会被这种匠心和精益求精的精神打动。

所以，今天我就想带着你一起去探索Mutex的实现及演进之路，希望你能和我一样体验到这种技术追求的美妙。我们从Mutex的一个简单实现开始，看看它是怎样逐步提升性能和公平性的。在这个过程中，我们可以学习如何逐步设计一个完善的同步原语，并能对复杂度、性能、结构设计的权衡考量有新的认识。经过这样一个学习，我们不仅能通透掌握Mutex，更好地使用这个工具，同时，对我们自己设计并发数据接口也非常有帮助。

那具体怎么来讲呢？我把Mutex的架构演进分成了四个阶段，下面给你画了一张图来说明。

“**初版**”的Mutex使用一个flag来表示锁是否被持有，实现比较简单；后来照顾到新来的goroutine，所以会让新的goroutine也尽可能地先获取到锁，这是第二个阶段，我把它叫作“**给新人机会**”；那么，接下来就是第三阶段“**多给些机会**”，照顾新来的和被唤醒的goroutine；但是这样会带来饥饿问题，所以目前又加入了饥饿的解决方案，也就是第四阶段“**解决饥饿**”。
<div><strong>精选留言（30）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/14/ab/a9/590d6f02.jpg" width="30px"><span>Junes</span> 👍（109） 💬（7）<div>老师讲得太棒了，我自己看Mutex源码时，没有前因后果，知识不成体系。交个作业：

1. 目前 Mutex 的 state 字段有几个意义，这几个意义分别是由哪些字段表示的？
和第四个阶段的讲解基本一致：前三个bit分别为mutexLocked、mutexWoken、mutexStarving，剩余bit表示mutexWaiter

2. 等待一个 Mutex 的 goroutine 数最大是多少？是否能满足现实的需求？
单从程序来看，可以支持 1&lt;&lt;(32-3) -1 ，约 0.5 Billion个
    其中32为state的类型int32，3位waiter字段的shift
考虑到实际goroutine初始化的空间为2K，0.5Billin*2K达到了1TB，单从内存空间来说已经要求极高了，当前的设计肯定可以满足了。</div>2020-10-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/5e/d3/e4d2ae68.jpg" width="30px"><span>buckwheat</span> 👍（41） 💬（1）<div>这源码看的感觉好难啊，尤其是这种并发的源码，老师有什么好的建议吗？</div>2020-10-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/17/0c/dd/1b12d77d.jpg" width="30px"><span>Dragon Frog</span> 👍（15） 💬（2）<div>老师，你好我有个疑问。在第二版中的 mutexWoken 这个含义到底该怎么理解。没办法很好的理解这个字段的作用</div>2020-10-25</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1b/95/dc/07195a63.jpg" width="30px"><span>锋</span> 👍（8） 💬（2）<div>老师您好，有个疑问。
runtime_Semrelease 信号唤起的总队queue中的第一个吗？
争抢锁在非饥饿模式下，是不是只有队首的waiter和新的goroutine之间发生？
谢谢</div>2020-10-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/37/92/961ba560.jpg" width="30px"><span>授人以🐟，不如授人以渔</span> 👍（4） 💬（1）<div>老师，有一个关于编程的疑惑，很难解决：我以后可能也会写一些复杂的逻辑，特别是并发的逻辑，但如何用逻辑思维去证明代码是没有问题的？比如第二版本的 Mutex 代码，就写的很好。</div>2021-11-03</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/24/a5/05/8254e9e1.jpg" width="30px"><span>Leo</span> 👍（4） 💬（1）<div>看第一遍的时候真的一脸懵，所以想起了老师开篇讲的很重要的一句“先建立体系”，所以我第二遍没有去关注源码，而是去理解老师文档中对锁实现过程的描述找到大体脉络。也就是先理解思路，再去逐个追究源码的细节。所以第三遍就能很顺利理解Mutex第一个版本的实现，第二个版本因为涉及到位运算，所以需要先把go的位运算基础搞清楚再继续分析。虽然还没有完全弄懂整个Mutex的实现，但现在也收获良多，因为从源码以及老师的文档描述中包含了程序的策略，而这些策略也可以用于我们开发中解决其他问题。</div>2021-06-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/60/54/b3eb605b.jpg" width="30px"><span>阿牛</span> 👍（4） 💬（1）<div>交作业
1、目前 Mutex 的 state 字段有几个意义，这几个意义分别是由哪些字段表示的？
state有四个字段：
• mutexLocked 占1bit，持有锁标记
• mutexWoken  占1bit，唤醒标记
• mutexStarving 占1bit，饥饿标记
• mutexWaiters  阻塞等待的waiter数量
2、等待一个 Mutex 的 goroutine 数最大是多少？是否能满足现实的需求？
32-3=29位=2^29=536 870 912</div>2021-02-19</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/vRoYUplibtKY2YFg7icP8A7SBSicAuhxz2mxgY6kibzaKRO8c1PXpNskGJB2Z3WfFoRaX5nh8oztib0NOr5qNdibCyaw/132" width="30px"><span>消逝文字</span> 👍（4） 💬（1）<div>底层实现的代码和业务代码果然有很大不同，理解起来也更加困难，光是上面那一堆位运算就已经够让人头疼的了，全程懵逼的看完了这一篇，还需要好好消化一下</div>2020-10-14</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTJAWUhO0xSjD6wbGScY5WOujAE94vNYWlWmsVdibb0IWbXzSSNXJHp0lqfWVq8ZicKBsEY1EuAWArew/132" width="30px"><span>Felix</span> 👍（2） 💬（1）<div>我有一件事想不明白，如果大家用的是同一个s
ync.Mutex,那么在每个goroutine中的sema数值不都是一样的，如果其中一个goroutine中的mutexLocked变为1,所有goroutine中mutexLocked不都是变为1吗，我的理解是mutex没有用值传递，应该指向同一块内存区域啊。</div>2021-06-28</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTJQyP4WVaRJVX6j5k8ZblWHo2BicmehWWSz571L8Lou2QWOSxPOg6ib0fuibfic6q6dS3ficLGNibIEo4uw/132" width="30px"><span>果酱</span> 👍（2） 💬（2）<div>new = old + 1&lt;&lt;mutexWaiterShift.    1&lt;&lt;mutexWaiterShift这个结果是4 为啥大佬注释说的是加1啊 求解</div>2020-11-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/99/f0/d9343049.jpg" width="30px"><span>星亦辰</span> 👍（2） 💬（1）<div>这一讲有点儿烧脑了 , 需要仔细看看</div>2020-10-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/82/62/f65cfadd.jpg" width="30px"><span>大飞</span> 👍（1） 💬（1）<div>交个作业加深印象：
1、state有以下信息worken、starvin、locked。 这个是最后三位存储的。 前32-3=29位用来存储等待的goroutine的数量。
2、最大数量为2的29次方= 536870912。大约5亿多。 每个goroutine占用2kb。5亿*2kb=1024G。从内存角度考虑，这个数量级已经足够了。
</div>2023-06-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/28/02/e6/a6932fd8.jpg" width="30px"><span>神经蛙</span> 👍（1） 💬（3）<div>队列中的groutine中，在没唤醒之前，有个新的goroutine来申请锁，此时通过自旋把woken标记挂起，同时获得到锁的那个goroutine开始解锁，因为woken标志导致没释放信号量，新的goroutine直接获取到了锁，如果一直发生这种情况，是否就无法进入饥饿模式。 作者大大请帮忙解答下。 </div>2021-09-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/26/fc/47/5fb0d905.jpg" width="30px"><span>张健华</span> 👍（1） 💬（3）<div>有个疑问，在最终版本中，如果一直有新goroutine到来且自旋的执行去执行Lock()操作，此时一个goroutine执行UnLcok()时，由于有自旋的goroutine将Woken位置为1，它是否就不会执行唤醒操作了？而不唤醒goroutine，也就无法计算它等待的时间差，怎么能进入饥饿模式呢？</div>2021-09-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/8f/cf/890f82d6.jpg" width="30px"><span>那时刻</span> 👍（1） 💬（1）<div>老师对于mutex讲的很仔细，之前看过mutex源码，有些地方看的不是明白，看了老师的讲解后，清晰了很多。

请问老师一个问题，从 1.14 版本起，Go 对 defer 做了优化，采用更有效的内联方式，这种内联方式和lock里slowlock内联方式一样么？

另外，go里的内联和C++内联有什么区别吗？</div>2020-10-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/17/6e/76b4aa3d.jpg" width="30px"><span>橙子888</span> 👍（1） 💬（1）<div>熬夜学习01课时后发现02课时也出来了，先来抢个沙发。</div>2020-10-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/e3/9e/b26da70d.jpg" width="30px"><span>closer</span> 👍（0） 💬（1）<div>分享几个学习这个章节的代码 帮助同学理解吧。
第一个是初级阶段的代码demo
package main

import (
	&quot;fmt&quot;
	&quot;sync&quot;
	&quot;sync&#47;atomic&quot;
)

&#47;&#47; 定义Mutex结构体
type Mutex struct {
	key  int32 &#47;&#47; 锁是否被持有的标识
	sema int32 &#47;&#47; 信号量专用，用以阻塞&#47;唤醒goroutine
}

&#47;&#47; cas操作，原子地比较并交换
func cas(val *int32, old, new int32) bool {
	return atomic.CompareAndSwapInt32(val, old, new)
}

&#47;&#47; 信号量获取
func semacquire(sema *int32) {
	&#47;&#47; 模拟获取信号量的操作
}

&#47;&#47; 信号量释放
func semrelease(sema *int32) {
	&#47;&#47; 模拟释放信号量的操作
}

&#47;&#47; 保证成功在val上增加delta的值
func xadd(val *int32, delta int32) (new int32) {
	for {
		v := *val
		if cas(val, v, v+delta) {
			return v + delta
		}
	}
	&#47;&#47; 这个panic语句实际上是不会被执行的，只是为了保证编译通过
	panic(&quot;unreached&quot;)
}

&#47;&#47; 请求锁
func (m *Mutex) Lock() {
	&#47;&#47; 尝试原子地将key加1
	fmt.Println(&quot;m.key&quot;, m.key)
	if xadd(&amp;m.key, 1) == 1 {
		&#47;&#47; 如果加1后的值为1，表示成功获取到锁
		fmt.Println(&quot;执行加锁。加锁后m.key&quot;, m.key)
		return
	}
	&#47;&#47; 否则，阻塞等待
	semacquire(&amp;m.sema)
}

&#47;&#47; 释放锁
func (m *Mutex) Unlock() {
	&#47;&#47; 尝试原子地将key减1
	if xadd(&amp;m.key, -1) == 0 {
		&#47;&#47; 如果减1后的值为0，表示没有其他等待者，直接返回
		fmt.Println(&quot;执行解锁&quot;)
		return
	}
	&#47;&#47; 否则，唤醒其他等待的goroutine
	semrelease(&amp;m.sema)
}

func main() {
	var wg sync.WaitGroup
	var mu Mutex
	wg.Add(10)
	&#47;&#47; 模拟10个goroutine
	for i := 0; i &lt; 10; i++ {
		go func(id int) {
			defer wg.Done()

			&#47;&#47; 请求锁
			mu.Lock()
			fmt.Printf(&quot;Goroutine %d acquired the lock\n&quot;, id)

			&#47;&#47; 模拟一些临界区操作
			fmt.Printf(&quot;Goroutine %d in the critical section\n&quot;, id)
			fmt.Println(&quot;main.key&quot;, mu.key)
			fmt.Println(&quot;main.sema&quot;, mu.sema)
			fmt.Println(&quot;**********************************************&quot;)
			&#47;&#47; 释放锁
			mu.Unlock()
			fmt.Printf(&quot;Goroutine %d released the lock\n&quot;, id)
			fmt.Println(&quot;---------------------------------------------&quot;)
		}(i)
	}

	&#47;&#47; 等待所有goroutine执行完毕
	wg.Wait()
}
</div>2023-12-06</li><br/><li><img src="" width="30px"><span>Geek_4d5dab</span> 👍（0） 💬（1）<div>老师讲的真的是太好了！
但是在“给新人机会” Unlock() line10 “old&amp;(mutexLocked|mutexWoken) != 0”，什么时候old&amp;mutexWoken会出现不为0的情况不太理解。
我理解的是如果old的mutexWoken位为1，说明存在其他的goroutine已经经过unlock line13、14的过程将m.state的mutexWoken置为1。如果存在这样的goroutine，那么当前goroutine在尝试line3时应该发现m.state未持有锁，直接panic</div>2023-09-15</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/25/34/81/f44f2f11.jpg" width="30px"><span>MG.Fre</span> 👍（0） 💬（1）<div>难，前端学go</div>2023-06-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/82/62/f65cfadd.jpg" width="30px"><span>大飞</span> 👍（0） 💬（1）<div>一只没明白woken标的作用。今天算是理解了一些。
可以从第二版的实现入手，第二班主要解决的问题是“给新人一些机会”。
那么如何实现呢？
首先unlock操作，换醒一个被lock阻塞的goroutine。此时这个被唤醒的goroutine不会直接获得锁。
而是要和新的请求lock的goroutine竞争。

那么这个竞争如何体现呢？
当前有两个goroutine再抢占锁，一个是之前被lock阻塞住，现在被唤醒的，一个是之前没有阻塞，当前正在执行lock逻辑的。
这两个goroutine并发执行cas操作。也就是第二版的19行。
那么这个时候，谁的cas成功，谁就可以获得锁，然后继续执行。
cas失败的，会执行到 23行 runtime.Semacquire(&amp;m.sema) 被阻塞。</div>2023-06-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/90/9c/53d0f906.jpg" width="30px"><span>黄豆豆</span> 👍（0） 💬（1）<div>老师，通过循序渐进的方式，将Mutex的源码以及背后的设计逻辑讲的非常透彻。虽然源码里对state的不同状态计算略显复杂难懂，但是不影响对整个核心设计原理的理解。

state是32位int类型，其中三位表示持有锁标志locked、唤醒标志woken和饥饿标志starving，还有29位可表示等待的goroutine的数量waiter，大概为5亿3千万。足够现实开发中使用了。</div>2022-12-02</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1e/f2/f5/b82f410d.jpg" width="30px"><span>Unknown element</span> 👍（0） 💬（1）<div>老师我想问下runtime_Semrelease这个函数第三个参数skipframes是什么含义？sdk的注释里说skipframes是跟踪过程中要省略的帧数，没看懂这里的帧数是什么意思；网上也没搜到能说清楚的文章
谢谢老师</div>2022-10-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/23/50/1f5154fe.jpg" width="30px"><span>无笔秀才</span> 👍（0） 💬（2）<div>老师，semacquire1 这个函数的逻辑 能具体讲讲吗？</div>2022-09-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/23/ac/55/80dc6b48.jpg" width="30px"><span>鲁迅原名周树人</span> 👍（0） 💬（1）<div>有个疑问：mutexWoken做什么用的，为什么要设置它？</div>2022-05-30</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/18/84/0d/4e289b94.jpg" width="30px"><span>三生</span> 👍（0） 💬（1）<div>为什么mutex从int换成了uint</div>2022-05-07</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/27/1b/11/1b4e53e5.jpg" width="30px"><span>ttty</span> 👍（0） 💬（1）<div>请问为什么不直接使用对信号量的PV操作实现mutex呢？为什么还要维护这个key呢？</div>2022-02-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/6c/fa/56e9f147.jpg" width="30px"><span>我就是那一把火</span> 👍（0） 💬（1）<div>老师您好，我有个疑问，第一个版本和第二个版本，在我看来，都是使用信号量唤醒在Lock方法中成功CAS但被阻塞住的goroutine，至于第二个版本能唤醒有CPU时间片的goroutine体现在哪里呢</div>2022-02-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1f/3a/8c/fc2c3e5c.jpg" width="30px"><span>xl666</span> 👍（0） 💬（2）<div>func (m *Mutex) Lock() { if xadd(&amp;m.key, 1) == 1 { &#47;&#47;标识加1，如果等于1，成功获取到锁 return } semacquire(&amp;m.sema) &#47;&#47; 否则阻塞等待 }
这个xadd不是死循环吗 不应该是卡在xadd(&amp;m.key, 1) == 1这块吗。  semacquire(&amp;m.sema)是不是不会走到</div>2022-02-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1f/44/27/71bed926.jpg" width="30px"><span>三太子AI</span> 👍（0） 💬（1）<div>第一遍听懂很懵，第二次切底明白啦，第二个问题：取决于 state 的类型，因为 int32，由于3个字节代表了状态，还有： 2^(32 – 3) – 1 等于 536870911，一个 goroutine 初始化的为 2kb，约等于 1024 GB 即 1TB，目前内存体量那么大的服务还是少有的，可以满足现在的使用。</div>2022-01-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/25/78/dc/bcdb3287.jpg" width="30px"><span>丶</span> 👍（0） 💬（1）<div>干活满满，看的特别爽，谢谢老师</div>2021-12-26</li><br/>
</ul>