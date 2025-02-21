你好，我是鸟窝。

在前面的四节课中，我们学习了第一个同步原语，即Mutex，我们使用它来保证读写共享资源的安全性。不管是读还是写，我们都通过Mutex来保证只有一个goroutine访问共享资源，这在某些情况下有点“浪费”。比如说，在写少读多的情况下，即使一段时间内没有写操作，大量并发的读访问也不得不在Mutex的保护下变成了串行访问，这个时候，使用Mutex，对性能的影响就比较大。

怎么办呢？你是不是已经有思路了，对，就是区分读写操作。

我来具体解释一下。如果某个读操作的goroutine持有了锁，在这种情况下，其它读操作的goroutine就不必一直傻傻地等待了，而是可以并发地访问共享变量，这样我们就可以**将串行的读变成并行读**，提高读操作的性能。当写操作的goroutine持有锁的时候，它就是一个排外锁，其它的写操作和读操作的goroutine，需要阻塞等待持有这个锁的goroutine释放锁。

这一类并发读写问题叫作[readers-writers问题](https://en.wikipedia.org/wiki/Readers%E2%80%93writers_problem)，意思就是，同时可能有多个读或者多个写，但是只要有一个线程在执行写操作，其它的线程都不能执行读写操作。

**Go标准库中的RWMutex（读写锁）就是用来解决这类readers-writers问题的**。所以，这节课，我们就一起来学习RWMutex。我会给你介绍读写锁的使用场景、实现原理以及容易掉入的坑，你一定要记住这些陷阱，避免在实际的开发中犯相同的错误。
<div><strong>精选留言（28）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/12/e7/e0/33521e13.jpg" width="30px"><span>DigDeeply</span> 👍（31） 💬（1）<div>这门课的质量真高啊，看的酣畅淋漓👍</div>2020-12-04</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/8f/cf/890f82d6.jpg" width="30px"><span>那时刻</span> 👍（9） 💬（1）<div>请问老师一个关于select{}问题，

func foo() {
	fmt.Println(&quot;in foo&quot;)
}

func goo() {
	var i int
	fmt.Println(&quot;in goo&quot;, i)
}

func main() {
	go goo()
	go foo()
	select {}
}

这个代码会报all goroutines are asleep - deadlock，是不是select{}这种写法不推荐么？

</div>2020-10-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/19/8e/f0/18720510.jpg" width="30px"><span>50%</span> 👍（3） 💬（1）<div>r := atomic.AddInt32(&amp;rw.readerCount, -rwmutexMaxReaders) + rwmutexMaxReaders
这句老师看我理解的对么。首先前一步反转操作是用原子操作实现的，此时其他的reader可能会改变readerCount字段的状态。虽然看起来加减同一个rwmutexMaxReaders看似结果相等，但在并发的场景下，其他reader读到的readerCount的状态为负值，表示有写锁的情况存在。</div>2020-11-07</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTImmLJCKerl9CI4sTpPDNCUgswp04ybsJ4J6mpJmMlHh43Iibp1RPOLam5PpOv2ZDGcjvGrY94lNRw/132" width="30px"><span>Varphp</span> 👍（2） 💬（1）<div>原谅我的小白 请教个问题

RWMutex是读写锁，Mutex就是锁吗？区别在于一个精确到读写 一个只能精确到协程对吗</div>2021-01-16</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/56/6c/042a2e41.jpg" width="30px"><span>David</span> 👍（1） 💬（6）<div>func (rw *RWMutex) RLock() {
    if atomic.AddInt32(&amp;rw.readerCount, 1) &lt; 0 {
            &#47;&#47; rw.readerCount是负值的时候，意味着此时有writer等待请求锁，因为writer优先级高，所以把后来的reader阻塞休眠
        runtime_SemacquireMutex(&amp;rw.readerSem, false, 0)
    }
}
这个代码， rw.readerCount 为负数，表示有writer，正在等待，则reader要进行休眠。


func (rw *RWMutex) Lock() {
    &#47;&#47; 首先解决其他writer竞争问题
    rw.w.Lock()
    &#47;&#47; 反转readerCount，告诉reader有writer竞争锁
    r := atomic.AddInt32(&amp;rw.readerCount, -rwmutexMaxReaders) + rwmutexMaxReaders
    &#47;&#47; 如果当前有reader持有锁，那么需要等待
    if r != 0 &amp;&amp; atomic.AddInt32(&amp;rw.readerWait, r) != 0 {
        runtime_SemacquireMutex(&amp;rw.writerSem, false, 0)
    }
}
这里是先获取到了锁，才去修改 rw.readerCount 的值，也就是说 每个writer 只有在获取到锁的情况下，才去把 rw.readerCount改成负数，而读锁是否休眠，也是根据这个值来判断。


func (rw *RWMutex) Unlock() {
    &#47;&#47; 告诉reader没有活跃的writer了
    r := atomic.AddInt32(&amp;rw.readerCount, rwmutexMaxReaders)
    
    &#47;&#47; 唤醒阻塞的reader们
    for i := 0; i &lt; int(r); i++ {
        runtime_Semrelease(&amp;rw.readerSem, false, 0)
    }
    &#47;&#47; 释放内部的互斥锁
    rw.w.Unlock()
}

而这个地方 先去释放了 reader，再去释放阻塞的writer

假设一种情况，在lock的时候，先后有a,b两个writer 进来，发现还有其他的reader正在使用，那么a，b进行阻塞，当reader 使用完了后，唤醒了a，a获取到了锁，在a使用期间，也有多个reader 进来，进行的休眠。当a使用完成后，调用unlock方法，先是修改了rw.readerCount（根据rlock的方法，rw.readerCount是唯一判断，是否阻塞的条件，那么，当这个时候，有新的reader进来，就可以无条件使用了）；再去唤醒被阻塞的reader（这个情况下，唤醒的reader 也可以进行无条件使用了），最后去释放锁，唤醒了b，b去获取锁的时候，发现有reader在使用，修改rw.readerCount的值（标示有等待的writer），然后进行休眠，当最后一个reader使用完成后，唤醒b，这个时候b才正在获取到了锁。

按照以上逻辑，多个writer的情况下，并没有造成reader出现饥饿状态，反而在释放写锁的那一刹那，新的reader 占了先机，这种情况怎么叫 Write-preferring 方案。我理解的Write-preferring 方案：是只有在没有writer的情况下，才轮到reader执行，多个writer的情况，是一个writer一个writer执行完，才会执行reader。我从代码中看出了不明白的地方，希望老师 帮忙解答一下</div>2021-01-04</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/3c/6b/99/b58d6d47.jpg" width="30px"><span>香芋地瓜粽</span> 👍（0） 💬（1）<div>读尝试锁RTryLock的实现:
思路:直接找到RWMutex中Mutex字段,调用TryLock方法尝试获取内部互斥锁,如果失败直接返回false,成功则只会阻塞写锁,不影响读锁(因为事实上获取读锁并不进行内部互斥锁的判断而是判断readCount是否为负)进而调用RLock直接获取读锁就好.记得获取之后务必调用Mutex字段的Unlock方法释放内部互斥锁
func (m *RWMutex) RTryLock() bool {
	if (*sync.RWMutex)(unsafe.Pointer(&amp;m.RWMutex)).TryLock() {
		defer (*sync.RWMutex)(unsafe.Pointer(&amp;m.RWMutex)).Unlock()
		m.RLock()
		return true
	} else {
		return false
	}
}</div>2024-09-09</li><br/><li><img src="" width="30px"><span>john-jy</span> 👍（0） 💬（1）<div>没人发现factorial退出条件是错误的吗？</div>2023-06-07</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1b/3d/2e/d098ea99.jpg" width="30px"><span>Traveller</span> 👍（0） 💬（1）<div>第二种死锁的场景有点隐蔽。我们知道，有活跃 reader 的时候，writer 会等待，如果我们在 reader 的读操作时调用 writer 的写操作（它会调用 Lock 方法），那么，这个 reader 和 writer 就会形成互相依赖的死锁状态。Reader 想等待 writer 完成后再释放锁，而 writer 需要这个 reader 释放锁之后，才能不阻塞地继续执行。这是一个读写锁常见的死锁场景。 
这是什么意思？完全看不懂</div>2023-04-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/2c/c7/89/16437396.jpg" width="30px"><span>极客酱酱</span> 👍（0） 💬（1）<div>鸟窝老师，麻烦问一下您这边使用的脑图工具是哪个，我正在学习这种用脑图梳理知识点的方法，手头的工具不太友好，手动狗头。</div>2022-04-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/17/bf/86/c0cb35f0.jpg" width="30px"><span>8.13.3.27.30</span> 👍（0） 💬（1）<div>有一个问题、写错unlock逻辑中、解锁之前会唤醒所有等待读的锁、但是再锁的过程当中并可能会继续来读和写的操作、这些操作这里貌似并不能保证写锁的优先，因为写锁解锁的过程会把后来的读锁也唤醒、而这个时候后来的写锁（但是它先于后来的读锁操作锁）没有办法优先后来的读锁获取到锁，不知道理解是否正确，另外读写锁的实现看上去在极限情况下会导致写饥饿、当然也可能是读饥饿（理论上这种情况不应该使用读写锁）、请教老师我的理解是否正确，如果正确怎么解决写饥饿的问题</div>2021-11-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/24/62/c4/be92518b.jpg" width="30px"><span>🐭</span> 👍（0） 💬（1）<div>第一个例子中，写操作在主携程里，为什么还要加锁</div>2021-08-06</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/PiajxSqBRaEIk8csm2UvibqAOdiaZ9fZ4tBI727gpdnwVSmH9dfkY9dSBpPQbibTBc2mm4ONdQj1lYWyZxKTZyFxpQ/132" width="30px"><span>GoGoGo</span> 👍（0） 💬（1）<div>
func main() {
    var counter Counter
    for i := 0; i &lt; 10; i++ { &#47;&#47; 10个reader
        go func() {
            for {
                counter.Count() &#47;&#47; 计数器读操作
                time.Sleep(time.Millisecond)
            }
        }()
    }

    for { &#47;&#47; 一个writer
        counter.Incr() &#47;&#47; 计数器写操作
        time.Sleep(time.Second)
    }
}
&#47;&#47; 一个线程安全的计数器
type Counter struct {
    mu    sync.RWMutex
    count uint64
}

&#47;&#47; 使用写锁保护
func (c *Counter) Incr() {
    c.mu.Lock()
    c.count++
    c.mu.Unlock()
}

&#47;&#47; 使用读锁保护
func (c *Counter) Count() uint64 {
    c.mu.RLock()
    defer c.mu.RUnlock()
    return c.count
}

当能明确的区分 读写操作时  为什么读还要加锁 这段代码里 加读锁和不加读锁有什么区别吗？</div>2021-07-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/57/d8/425e1b0a.jpg" width="30px"><span>小虾米</span> 👍（0） 💬（1）<div>rwmutexMaxReaders 为何不能用满32位呢</div>2021-05-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/aa/2a/ce7c487d.jpg" width="30px"><span>Terence孫</span> 👍（0） 💬（1）<div>读写锁中读写锁Lock的总结：
当前锁和新锁类型不同，新锁阻塞等待
当前锁和新锁类型相同，读锁不阻塞，写锁阻塞</div>2021-03-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/f6/a0/8ea0bfba.jpg" width="30px"><span>Yimmy</span> 👍（0） 💬（1）<div>老师好，“同时，它还会调用 GetCPUSet 或 GetDefaultCPUSet 方法。当这两个方法都请求写锁时，是获取不到的，因为 GetCPUSetOrDefault 方法还没有执行完，不会释放读锁，这就形成了死锁。”

看了这个issue, GetCPUSet 或 GetDefaultCPUSet 这2个方法中调用的是读锁，不是写锁，这个issuse的问题，我理解是重入锁，而不是reader和writer相互等待的死锁

补充源码（https:&#47;&#47;github.com&#47;kubernetes&#47;kubernetes&#47;pull&#47;62464&#47;files ）
func (s *stateMemory) GetCPUSet(containerID string) (cpuset.CPUSet, bool) {
	s.RLock()
	defer s.RUnlock()
	res, ok := s.assignments[containerID]
	return res.Clone(), ok
}
func (s *stateMemory) GetDefaultCPUSet() cpuset.CPUSet {
	s.RLock()
	defer s.RUnlock()
	return s.defaultCPUSet.Clone()
}</div>2020-11-06</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/24/df/645f8087.jpg" width="30px"><span>Yayu</span> 👍（0） 💬（1）<div>老师好，请问“原语”的意思是什么？原子性语句吗？</div>2020-10-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/1d/34/8201baab.jpg" width="30px"><span>端贺</span> 👍（33） 💬（3）<div>简单梳理面试题:
    1. 读写锁用过吗，读写锁用在什么样的场景？（或读写锁主要用来解决什么问题，说说对读写锁的理解？）
    2.说说RWMutex的实现原理？说说RWMutex与Mutex的区别？
    3.RWMutex源码看过吗？如果使用Mutex来设计一个RWMutex你有什么思路？
    4.在执行Lock，Unlock，Rlock，RUnlock时需要考虑什么问题？
    5.使用读写锁时如何规避死锁问题？
    6.如何监控读写锁的等待情况？你有什么思路？</div>2020-11-06</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/ab/a9/590d6f02.jpg" width="30px"><span>Junes</span> 👍（32） 💬（4）<div>交一下作业，我就不贴完整代码了，分享一下核心思路：

获取两个关键变量，大致思路是根据 起始地址+偏移量，
&#47;&#47; readerCount 这个成员变量前有1个mutex+2个uint32
readerCount := atomic.LoadInt32((*int32)(unsafe.Pointer(uintptr(unsafe.Pointer(&amp;m)) + unsafe.Sizeof(sync.Mutex{}) + 2*unsafe.Sizeof(uint32(0)))))

&#47;&#47; readerWait 这个成员变量前有1个mutex+2个uint32+1个int32
readerWait := atomic.LoadInt32((*int32)(unsafe.Pointer(uintptr(unsafe.Pointer(&amp;m)) + unsafe.Sizeof(sync.Mutex{}) + 2*unsafe.Sizeof(uint32(0)) + unsafe.Sizeof(int32(0)))))

剩下的，大量借鉴Mutex那块TryLock的实现了，大量地使用atomic原子操作：

TryLock: 读取readerCount，小于0则返回false，否则尝试Lock
是否有writer：读取readerCount，小于0则有writer，否则没有。
reader的数量：读取readerCount，小于0则加上rwmutexMaxReaders，结果即为reader数量。

另外还可以通过readerWait，查询当前Lock被多少个RLock阻塞着。

再谈一个感受，RWMutex的实现依赖于Mutex，这最大的好处是简化了代码，但同时，在读少写多的情况下，由于额外维护了4个变量，性能不如直接调用Mutex。这个读写比例的临界值，找个时间自己测试测试。 :)</div>2020-10-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/67/d5/1b26b725.jpg" width="30px"><span>Gopher</span> 👍（1） 💬（0）<div>作业思路
和mutex的扩展思路一样，通过unsafe获取指针，在进行偏移获取到reader数量，不等于0直接返回，否则尝试lock</div>2020-10-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/b8/3c/1a294619.jpg" width="30px"><span>Panda</span> 👍（1） 💬（0）<div>RWMutex 是 Mutex 的增强版本  也是分而治之的思想体现</div>2020-10-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/53/db/858337e3.jpg" width="30px"><span>Ethan Liu</span> 👍（1） 💬（0）<div>区分reader和writer的场景，可不可以用channel来实现？如果可以的话，与使用RWMutex有什么区别？</div>2020-10-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/19/8e/f0/18720510.jpg" width="30px"><span>50%</span> 👍（0） 💬（0）<div>r := atomic.AddInt32(&amp;rw.readerCount, -rwmutexMaxReaders) + rwmutexMaxReaders

再看一遍又有新的理解呀。这句话实际上仅有前半部分保证了对readerCounter的原子性操作。那么在并发的情况下，持有读锁的goroutine就被阻塞。</div>2022-03-16</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/18/da/40/bda5ad2b.jpg" width="30px"><span>ChuanBing จุ๊บ</span> 👍（0） 💬（0）<div>func (rw *RWMutex) Unlock() {
	if race.Enabled {
		_ = rw.w.state
		race.Release(unsafe.Pointer(&amp;rw.readerSem))
		race.Disable()
	}
&#47;&#47; ..........
}

请问 其中的  _ = rw.w.state  作用是什么?</div>2021-07-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1b/96/47/93838ff7.jpg" width="30px"><span>青鸟飞鱼</span> 👍（0） 💬（0）<div>涨知识了</div>2020-11-05</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/8d/87/47d95f4a.jpg" width="30px"><span>syuan</span> 👍（0） 💬（0）<div>干货满满</div>2020-11-04</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/9b/ba/333b59e5.jpg" width="30px"><span>Linuxer</span> 👍（0） 💬（1）<div>试着回答一下课后题，初学GO，请各位大佬指点
const {
   READ = 0 
   WRITE = 1
}

func (rw **RWMutex) TryLock(mode int32)  bool {
   n := atomic.LoadInt32(&amp;rw.readerCount)
   if n &lt; 0 {
      return false 
   }   
   if mod == 0 &amp;&amp; atomic.CompareAndSwapInt32(n, n+1) == n{
      return true ;
   }else if mod == 1 &amp;&amp; atomic.CompareAndSwapInt32(0, -rwmutexMaxReaders) == 0 {
      rw.w.Lock()
      return true
   }else{
      return false
   }
}
func (rw *RWMutex) ExistWriter() bool {
     return atomic.LoadInt32(&amp;rw.readerCount) &lt; 0
}

func (rw *RWMutex) GetReaderNum() int32 {
   n := atomic.LoadInt32(&amp;rw.readerCount) ;
   if n &lt; 0 {
       return atomic.LoadInt32(&amp;rw.readerWait)
   }else{
      return n 
   }
}</div>2020-10-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/19/2b/fe/7925eb7e.jpg" width="30px"><span>pdf</span> 👍（0） 💬（6）<div>Go 1.15
main函数结尾 select {} 直接报死锁</div>2020-10-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/17/6e/76b4aa3d.jpg" width="30px"><span>橙子888</span> 👍（0） 💬（0）<div>又是一个需要花时间消化的章节，理解读写锁的原理之后，再参考之前 Mutex 章节扩展的实现，写一个扩展的读写锁应该不难，惊讶地发现已经有大佬给出答案了……</div>2020-10-21</li><br/>
</ul>