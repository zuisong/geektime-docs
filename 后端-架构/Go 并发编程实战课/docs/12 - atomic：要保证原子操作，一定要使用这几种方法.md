你好，我是鸟窝。

前面我们在学习Mutex、RWMutex等并发原语的实现时，你可以看到，最底层是通过atomic包中的一些原子操作来实现的。当时，为了让你的注意力集中在这些原语的功能实现上，我并没有展开介绍这些原子操作是干什么用的。

你可能会说，这些并发原语已经可以应对大多数的并发场景了，为啥还要学习原子操作呢？其实，这是因为，在很多场景中，使用并发原语实现起来比较复杂，而原子操作可以帮助我们更轻松地实现底层的优化。

所以，现在，我会专门用一节课，带你仔细地了解一下什么是原子操作，atomic包都提供了哪些实现原子操作的方法。另外，我还会带你实现一个基于原子操作的数据结构。好了，接下来我们先来学习下什么是原子操作。

# 原子操作的基础知识

Package sync/atomic 实现了同步算法底层的原子的内存操作原语，我们把它叫做原子操作原语，它提供了一些实现原子操作的方法。

之所以叫原子操作，是因为一个原子在执行的时候，其它线程不会看到执行一半的操作结果。在其它线程看来，原子操作要么执行完了，要么还没有执行，就像一个最小的粒子-原子一样，不可分割。

CPU提供了基础的原子操作，不过，不同架构的系统的原子操作是不一样的。
<div><strong>精选留言（20）</strong></div><ul>
<li><img src="" width="30px"><span>myrfy</span> 👍（40） 💬（10）<div>恰好老婆大人是做芯片MMU相关工作的，咨询了一下她，她告诉我现代的CPU基本上都在硬件层面保证了多核之间数据视图的一致性，也就是说普通的LOAD&#47;STORE命令在硬件层面处理器就可以保证cache的一致性。如果是这样的话，那是不是可以理解为atomic包对指针的作用，主要是防止编译器做指令重排呢？因为编译器在这些现代架构上没必要使用特殊的指令了。
如果不止这样，麻烦老师指正，晚上回去和老婆大人再深入交流交流……</div>2020-11-06</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/1d/34/8201baab.jpg" width="30px"><span>端贺</span> 👍（6） 💬（2）<div>晁老师的内功真是深厚，整个系列读下来还是有点吃力的，尤其是文中推荐的外链，需要多花点时间好好消化，感谢晁老师。</div>2020-11-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/22/58/a2/24612c85.jpg" width="30px"><span>末班车</span> 👍（4） 💬（1）<div>老师您好，之前在用atomic的时候，疑惑为啥没有提供it  int16的相关方法，这是不是也跟内存对齐有关系啊？</div>2020-11-06</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTJMzj0MHiaXBdDFp4E16qhu6PZlu6xkJRWgaoJXOeqMDDLqM4vcvUbnVLiactTypZkYibOg7okwm2TAQ/132" width="30px"><span>Geek_921929</span> 👍（2） 💬（1）<div>晁老师，go包  cas针对ABA问题有啥封装吗，度学堂看到你的直播了哈哈，然后后来回放找不到了</div>2021-09-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/2a/a0/71/1725274f.jpg" width="30px"><span>赵敷</span> 👍（0） 💬（1）<div>晁老师你好，我有几个问题想向你请求一下。第一点，go的原子操作，是否有禁止指令重排的作用。即有一个func代码如下:
var s1 int32
var s2 int32
var s3 int
var s4 int
func f() {
1:	atomic.StoreInt32(&amp;s1,1)
2:      s3=1
3:	atomic.StoreInt32(&amp;s2,1)
4:      s4 = 1
}
我想问一下1指令一定在3指令之前执行吗，另外2指令一定在s4指令之前执行吗。另外在内存模型上，我知道原子操作底层会遵循MESI模型来保证数据在多核缓存的一致性，我想知道多线程访问上面f函数，当我们在一个协程里观测到3指令已经执行，是否可以认为2也已经执行（如果3不是原子操作，我知道这一点肯定无法保证），2对内存的访问结果，对观测线程是否可见。也就是说添加原子指令的位置，会添加内存屏障，但是对于写内存屏障，是该屏障之前所有写操作都会刷新到内存，还是只是针对那个store的原子变量会刷新到内存，其他普通写操作还是继续写到cache中，逐级淘汰到内存中
</div>2022-12-05</li><br/><li><img src="" width="30px"><span>强庚</span> 👍（0） 💬（1）<div>atomic.Load系列的原子操作具体作用是什么呢？比如if atomic.LoadInt32(&amp;a) == 1 如果直接写成if a== 1这样有什么问题吗</div>2022-10-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1b/a4/27/15e75982.jpg" width="30px"><span>小袁</span> 👍（0） 💬（2）<div>atomic.Value是怎样实现的呢？这里为啥可以支持任意的数据？用Pointer类型不香么？</div>2021-04-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/04/60/64d166b6.jpg" width="30px"><span>Fan</span> 👍（0） 💬（1）<div>老师，执行这条命令，报错是什么意思，怎样解决？
$ GOARCH=amd64 go tool objdump -gnu main.o


flag provided but not defined: -gnu
usage: go tool objdump [-S] [-s symregexp] binary [start end]

  -S    print go code alongside assembly
  -s string
        only dump symbols matching this regexp</div>2020-12-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/ac/66/a256008b.jpg" width="30px"><span>SuperDai</span> 👍（0） 💬（2）<div>老师，无锁队列对消费者数量和生产者数量是不是有要求？是不是要求消费者数量为1还是生产者数量为1？</div>2020-11-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/ac/66/a256008b.jpg" width="30px"><span>SuperDai</span> 👍（0） 💬（1）<div>老师，无锁队列对消费者数量和生产者数量是不是有要求？是不是要求消费者数量为1还是生产者数量为1？</div>2020-11-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/c1/0e/2b987d54.jpg" width="30px"><span>蜉蝣</span> 👍（3） 💬（1）<div>这个 lock-free queue 是能看懂，但要自己写出来就感觉有点难了。就譬如 tail == load(&amp;q.tail) 和 head == load(&amp;q.head) 的检查，我就想不到还要再做一次检查。前面章节看源码的时候也有这种感觉，能看懂，但自己写肯定想不到哪里要多检查一次。</div>2020-11-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/19/9d/7c/b3bfc1bf.jpg" width="30px"><span>JYZ1024</span> 👍（2） 💬（2）<div>删除了一部分逻辑，但是看起来没有问题  麻烦各位帮忙看下
type LockFreeList struct {
	head unsafe.Pointer &#47;&#47; 无意义非数据指针
	tail unsafe.Pointer &#47;&#47; 尾部元素
}

type elem struct {
	value interface{}
	next  unsafe.Pointer
}

var emptyNode = unsafe.Pointer(&amp;elem{})

func NewLockFreeList() *LockFreeList {
	return &amp;LockFreeList{
		head: emptyNode,
		tail: emptyNode,
	}
}

&#47;&#47; 入队
func (q *LockFreeList) Enqueue(v interface{}) {
	node := &amp;elem{value: v}
	&#47;&#47; load 队尾指针
	for {
		tail := q.loadElem(&amp;q.tail)
		next := q.loadElem(&amp;tail.next)   &#47;&#47; 这一步执行完以后，可能tail已经被改变
		if tail == q.loadElem(&amp;q.tail) { &#47;&#47; 确保load tail 和 next 是&quot;原子操作&quot;，不是就直接返回
			if next == nil {
				if atomic.CompareAndSwapPointer(&amp;tail.next, unsafe.Pointer(next), unsafe.Pointer(node)) {
					atomic.CompareAndSwapPointer(&amp;q.tail, unsafe.Pointer(tail), unsafe.Pointer(node))
					return
				}
			}
		}
	}
}

func (q *LockFreeList) Dequeue() interface{} {
	for {
		head := q.loadElem(&amp;q.head)
		tail := q.loadElem(&amp;q.tail)
		if head == tail {
			return nil
		}
		node := q.loadElem(&amp;head.next) &#47;&#47; 队头节点
		nodeNext := q.loadElem(&amp;node.next)
		if node == q.loadElem(&amp;head.next) {
			if atomic.CompareAndSwapPointer(&amp;head.next, unsafe.Pointer(node), unsafe.Pointer(nodeNext)) {
				return node.value
			}
		}
	}
}

func (q *LockFreeList) loadElem(p *unsafe.Pointer) *elem {
	return (*elem)(atomic.LoadPointer(p))
}</div>2020-11-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/5b/66/ad35bc68.jpg" width="30px"><span>党</span> 👍（0） 💬（0）<div>这个版本的有点低了 能不能与时俱进 更新一波</div>2023-04-10</li><br/><li><img src="" width="30px"><span>Geek8956</span> 👍（0） 💬（0）<div>对于修改内存中的值，swap和store是不是一样？或者说，swap和store的区别，就是swap可以额外获取原值？</div>2021-11-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/1a/f7/cb61b37f.jpg" width="30px"><span>Tatum 苏天斌</span> 👍（0） 💬（0）<div>无锁队列实现里面33行：cas(&amp;q.tail, tail, next)
这是为了当前routine入队更快（可能另一个入队操作刚走完28行）而优化的么？</div>2021-08-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/04/60/64d166b6.jpg" width="30px"><span>Fan</span> 👍（0） 💬（0）<div>
继续打卡，free-lock 能再详细解释下吗？</div>2020-12-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/45/2a/c4413de4.jpg" width="30px"><span>soooldier</span> 👍（0） 💬（2）<div>出队的时候为啥还需要判断head == load(&amp;q.head)呢？head只是在NewLKQueue的时候有赋值，别的任何地方没发现有更新的操作呢</div>2020-12-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/18/7e/75/3e6bdc4c.jpg" width="30px"><span>李金狗</span> 👍（0） 💬（2）<div>cas(&amp;q.tail, tail, n) &#47;&#47;入队成功，移动尾巴指针 :这一步有失败的风险吧。</div>2020-11-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/17/6e/76b4aa3d.jpg" width="30px"><span>橙子888</span> 👍（0） 💬（0）<div>打卡。</div>2020-11-06</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1b/96/47/93838ff7.jpg" width="30px"><span>青鸟飞鱼</span> 👍（0） 💬（0）<div>每周一三五早上，打卡，最后的总结涨知识了。</div>2020-11-06</li><br/>
</ul>