到目前为止，我们已经一起学习了Go语言标准库中最重要的那几个同步工具，这包括非常经典的互斥锁、读写锁、条件变量和原子操作，以及Go语言特有的几个同步工具：

1. `sync/atomic.Value`；
2. `sync.Once`；
3. `sync.WaitGroup`
4. `context.Context`。

今天，我们来讲Go语言标准库中的另一个同步工具：`sync.Pool`。

`sync.Pool`类型可以被称为临时对象池，它的值可以被用来存储临时的对象。与Go语言的很多同步工具一样，`sync.Pool`类型也属于结构体类型，它的值在被真正使用之后，就不应该再被复制了。

这里的“临时对象”的意思是：不需要持久使用的某一类值。这类值对于程序来说可有可无，但如果有的话会明显更好。它们的创建和销毁可以在任何时候发生，并且完全不会影响到程序的功能。

同时，它们也应该是无需被区分的，其中的任何一个值都可以代替另一个。如果你的某类值完全满足上述条件，那么你就可以把它们存储到临时对象池中。

你可能已经想到了，我们可以把临时对象池当作针对某种数据的缓存来用。实际上，在我看来，临时对象池最主要的用途就在于此。

`sync.Pool`类型只有两个方法——`Put`和`Get`。Put用于在当前的池中存放临时对象，它接受一个`interface{}`类型的参数；而Get则被用于从当前的池中获取临时对象，它会返回一个`interface{}`类型的值。
<div><strong>精选留言（30）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/11/c4/c1/1118e24e.jpg" width="30px"><span>Stone</span> 👍（10） 💬（1）<div>看了一下 1.14 的源码，那个锁现在是全局的了，即一个临时对象池中本地池列表中的所有本地池都共享一个锁，而不是每个本地池都有自己的锁。</div>2020-07-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/04/fb/40f298bb.jpg" width="30px"><span>小罗希冀</span> 👍（7） 💬（2）<div>请问一下老师, 如果syn.Pool广泛的应用场景是缓存, 那为什么不直接使用map缓存呢?这样岂不是更方便, 更快捷?</div>2020-10-26</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTJSmAhbvPia1msvk91m5rQLTpicY85f2moFMCcAibictL3OeiaaVREadpHN2O3FwicmylwiclTUJJa1peS1Q/132" width="30px"><span>张sir</span> 👍（7） 💬（1）<div>还有一个问题，如果多goruntine同时申请临时对象池内资源，所有goruntine都可以同时获取到吗，还是只能有一个goruntine获取到，其它的goruntine都阻塞，直到这个goruntine释放完后才能使用</div>2019-05-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/0a/0b/985d3800.jpg" width="30px"><span>郭星</span> 👍（3） 💬（1）<div>&quot;在每个本地池中，都包含一个私有的临时对象和一个共享的临时对象列表。前者只能被其对应的 P 所关联的那个 goroutine 中的代码访问到，而后者却没有这个约束&quot;
对于private只能被当前协程才能访问,其他协程不能访问到private,这个应该怎么测试呢?
import (
	&quot;runtime&quot;
	&quot;sync&quot;
	&quot;testing&quot;
)

type cache struct {
	value int
}
func TestShareAndPrivate(t *testing.T) {
	p := sync.Pool{}
	&#47;&#47; 在主协程写入10
	p.Put(cache{value: 10})
	var wg sync.WaitGroup
	wg.Add(1)
	go func() {
		for i := 0; i &lt; 10; i++ {
			p.Put(cache{value: i})
		}
		wg.Done()
	}()
	wg.Wait()
	wg.Add(1)
	go func() {
		for true {
			v := p.Get()
			if v == nil {
				break
			}
			t.Log(v)
		}
		wg.Done()
	}()
	wg.Wait()
}
这段代码没有体现出来私有和共享的区别</div>2020-09-03</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/e0/4b/bbb48b22.jpg" width="30px"><span>越努力丨越幸运</span> 👍（3） 💬（1）<div>老师，当一个goroutine在访问某个临时对象池中一个本地池的shared字段时被锁住，此时另外一个goroutine访问临时对象池时，是会跳过这个本地池，去访问其他的本地池，还是说会被阻塞住？
</div>2020-04-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/b1/20/8718252f.jpg" width="30px"><span>鲲鹏飞九万里</span> 👍（2） 💬（1）<div>郝老师您好，你在article70.go 的示例中使用sync.Pool 的作用是啥呢，看不出来。你看：
func main() {
	&#47;&#47; buf := GetBuffer()
	&#47;&#47; defer buf.Free()
	buf := &amp;myBuffer{delimiter: delimiter}

在main函数中，我用`buf := &amp;myBuffer{delimiter: delimiter}`这行代码代替上面两行代码后，执行的效果是一样的。 article70.go 的示例，为啥要使用 sync.Pool 呢，麻烦老师进一步讲解下</div>2023-02-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1b/a4/27/15e75982.jpg" width="30px"><span>小袁</span> 👍（2） 💬（1）<div>为啥本地池列表长度不是跟M一致，而是跟P一致？</div>2021-02-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/75/aa/21275b9d.jpg" width="30px"><span>闫飞</span> 👍（2） 💬（1）<div>这里存放的临时对象是否是无状态，无唯一标识符的纯值对象? 对象的类型是否都是一样，还是说必须要用户自己做好具体类型的判定?</div>2019-07-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/44/84/25a17f05.jpg" width="30px"><span>苏安</span> 👍（2） 💬（1）<div>老师，不知道还有几讲，最初的课程大纲有相关的拾遗章节，不知道后续的安排还有没？</div>2018-10-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/df/1e/cea897e8.jpg" width="30px"><span>传说中的成大大</span> 👍（1） 💬（1）<div>之前学习 go routine的时候 初次了解到这个p以为就是用来调度goroutine的  但是今天又讨论到这个p 这个P还关联到了临时对象池，这个临时对象池也涉及到被运行时系统所清理 所以我产生了以为 这个p时候就是运行时系统呢？</div>2020-04-16</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/c6/73/abb7bfe3.jpg" width="30px"><span>疯琴</span> 👍（1） 💬（1）<div>请问老师，demo70 的 37 行 return 后面没跟东西，是相当于 return nil 么？</div>2020-01-02</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/24/27/7c/97b0c1dd.jpg" width="30px"><span>林嘉裕</span> 👍（0） 💬（1）<div>数组可以通过put(arr[:0])清空，如果是map呢？只能通过遍历？</div>2021-12-21</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTKELX1Rd1vmLRWibHib8P95NA87F4zcj8GrHKYQL2RcLDVnxNy1ia2geTWgW6L2pWn2kazrPNZMRVrIg/132" width="30px"><span>jxs1211</span> 👍（0） 💬（1）<div>由于fmt包中的代码在真正使用这些临时对象之前，总是会先对其进行重置，
func newPrinter() *pp {
	p := ppFree.Get().(*pp)
	p.panicking = false
	p.erroring = false
	p.wrapErrs = false
	p.fmt.init(&amp;p.buf)
	return p
}
思考：这段重置的代码为什么不能放到使用完成后，一并p.free
func (p *pp) free() {
	&#47;&#47; Proper usage of a sync.Pool requires each entry to have approximately
	&#47;&#47; the same memory cost. To obtain this property when the stored type
	&#47;&#47; contains a variably-sized buffer, we add a hard limit on the maximum buffer
	&#47;&#47; to place back in the pool.
	&#47;&#47;
	&#47;&#47; See https:&#47;&#47;golang.org&#47;issue&#47;23199
	if cap(p.buf) &gt; 64&lt;&lt;10 {
		return
	}

	p.buf = p.buf[:0]
	p.arg = nil
	p.value = reflect.Value{}
	p.wrappedErr = nil
	ppFree.Put(p)
}</div>2021-10-30</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/DYAIOgq83erpYZalYvFGcBs7zZvYwaQAZwTLiaw0mycJ4PdYpP3VxAYkAtyIRHhjSOrOK0yESaPpgEbVQUwf6LA/132" width="30px"><span>Harlan</span> 👍（0） 💬（1）<div>我理解pool使用场景是 做一个结构体原型池，一般用在结构体创建成本较高的场景，如db 连接 ，http连接等</div>2021-09-16</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/9d/a4/e481ae48.jpg" width="30px"><span>lesserror</span> 👍（0） 💬（1）<div>以下问题，盼老师看到了，帮忙解答一下：

1：  文中说：“sync.Pool类型只有两个方法——Put和Get”。 我的golang版本是：go1.16.4，不止这两个方法了，还有：getSlow、pin、pinSlow，不过他们都是包级私有的方法。

2： 像： allPools 这个 变量的 上面的 注释最后 写的 “STW.” 代表什么意思呀？

3：课程到目前 sync.pool 这一讲为止，前面的文章基本都懂了。就是这一讲读了几遍，看的还是一知半解。我以为这一讲牵扯的源码比较多 而且 感觉 难度 有点大。不知道 郝林老师 三年后重新看这个有没有什么新的想法 能否帮我重新梳理一下或者给一些 关于学习 sync.pool的建议？

多谢老师的解答。</div>2021-08-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/19/8c/e2/48f4e4fa.jpg" width="30px"><span>mkii</span> 👍（0） 💬（1）<div>老师你好，预期是使用pool 和不使用pool相比，平均操作时间长但分配内存少。目前看起来不是这样的，是我的代码有问题吗？麻烦老师解答一下。
func BenchmarkBufferPool(b *testing.B) {
	var pool = sync.Pool{New: func() interface{} {
		return make([]byte, 1024)
	}}

	b.ResetTimer()
	for i := 0; i &lt; b.N; i++ {
		bytesObj := pool.Get().([]byte)
		_ = bytesObj
		pool.Put(bytesObj)
	}
	b.StopTimer()
}
func BenchmarkBuffer(b *testing.B) {
	b.ResetTimer()
	for i := 0; i &lt; b.N; i++ {
		bytesObj := make([]byte, 1024)
		_ = bytesObj
	}
	b.StopTimer()
}
========
go test -bench=. -benchmem
========
goos: windows
goarch: amd64
pkg: go_demo&#47;src&#47;go-core-36&#47;syncpool
BenchmarkBufferPool-6           26087295                50.1 ns&#47;op            32 B&#47;op          1 allocs&#47;op
BenchmarkBuffer-6               1000000000               0.268 ns&#47;op           0 B&#47;op          0 allocs&#47;op
PASS
ok      go_demo&#47;src&#47;go-core-36&#47;syncpool 1.972s</div>2021-04-14</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/tmVLphkQHLxRsAOZOzJNhJKXvAhkvvT8koMjMUpIQbJN1e8Uico1habQvNibvibI14yM7DWVicJIgNriaib9tRv735mg/132" width="30px"><span>Geek_9b9769</span> 👍（0） 💬（1）<div>老师，我有个问题，我用sync.Pool写了一个benchmark, sync.Pool比不用的时候性能变差了，为什么
pb.UserInfo是protoBuf的一个数据结构

使用pool代码:
func BenchmarkPool(b *testing.B) {

	var pool = sync.Pool{
		New: func() interface{} {
			return new(pb.UserInfo)
		},
	}

	for i := 0; i &lt; b.N; i++ {
		pb := pool.Get().(*pb.UserInfo)
		pb.IsOK = true
		pb.Maps = make(map[string]int32)
		pool.Put(pb)
	}

}
benchmark结果：
goos: windows
goarch: amd64
pkg: learn
cpu: AMD Ryzen 7 4800H with Radeon Graphics
BenchmarkPool
BenchmarkPool-16
24863664	        58.62 ns&#47;op	      48 B&#47;op	       1 allocs&#47;op
PASS

不使用pool的代码：
func BenchmarkNoPool(b *testing.B) {
	for i := 0; i &lt; b.N; i++ {
		pb := new(pb.UserInfo)
		pb.IsOK = true
		pb.Maps = make(map[string]int32)
	}
}

benchmark结果：
goos: windows
goarch: amd64
pkg: learn
cpu: AMD Ryzen 7 4800H with Radeon Graphics
BenchmarkNoPool
BenchmarkNoPool-16
28364434	        41.48 ns&#47;op	      48 B&#47;op	       1 allocs&#47;op</div>2021-04-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/cc/25/8c6eab2c.jpg" width="30px"><span>ArtistLu</span> 👍（0） 💬（1）<div>老师， 能简单讲下 “使用完临时对象之后，都会先抹掉其中已缓冲的内容”，其中抹掉缓冲如何实现的吗？</div>2020-08-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/df/1e/cea897e8.jpg" width="30px"><span>传说中的成大大</span> 👍（0） 💬（1）<div>关于思考题 我觉得要及时回收 外加提供new字段 不然肯定会出现 不够用的情况</div>2020-04-16</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/df/1e/cea897e8.jpg" width="30px"><span>传说中的成大大</span> 👍（0） 💬（1）<div>还有就是 到底go语言中有多少个p?</div>2020-04-16</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/df/1e/cea897e8.jpg" width="30px"><span>传说中的成大大</span> 👍（0） 💬（1）<div>然后临时对象池底层依赖的是数组 我想问的是 初始化的时候这个数组是多大？后面是否还涉及到扩容呢？ 我本来以为底层是链表 因为增删方便，后来才发现是为了查询方便</div>2020-04-16</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/bd/f3/a59e8c99.jpg" width="30px"><span>湛</span> 👍（0） 💬（1）<div>请问 sync.Pool可以作为切片的一部分吗</div>2020-03-04</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTJSmAhbvPia1msvk91m5rQLTpicY85f2moFMCcAibictL3OeiaaVREadpHN2O3FwicmylwiclTUJJa1peS1Q/132" width="30px"><span>张sir</span> 👍（0） 💬（2）<div>你好，请问put一个不存在的临时对象池会引发别的问题吗</div>2019-05-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/42/7c/8ef14715.jpg" width="30px"><span>NIXUS</span> 👍（0） 💬（1）<div>请教老师一个问题: Get方法从临时对象池中取走一个私有临时对象时, 会不会把自己的共享临时对象列表中的临时对象转移一个为私有临时对象, 以方便下一个Get方法调用? 从文中的内容看, 应该是不会的</div>2019-04-16</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/20/27/a6932fbe.jpg" width="30px"><span>虢國技醬</span> 👍（29） 💬（2）<div>go1.13对本地池的shared共享列表做了存储结构变更,改为双向链表（在shared的头部存，尾部取），取消锁以提高性能</div>2020-01-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/bc/15/23ce17f9.jpg" width="30px"><span>数字记忆</span> 👍（16） 💬（1）<div>这个代码很形象：

package main

import (
	&quot;fmt&quot;
	&quot;sync&quot;
	&quot;time&quot;
)

&#47;&#47; 一个[]byte的对象池，每个对象为一个[]byte
var bytePool = sync.Pool{
	New: func() interface{} {
		b := make([]byte, 1024)
		return &amp;b
	},
}

func main() {
	a := time.Now().Unix()
	fmt.Println(a)
	&#47;&#47; 不使用对象池
	for i := 0; i &lt; 1000000000; i++{
		obj := make([]byte,1024)
		_ = obj
	}
	b := time.Now().Unix()
	fmt.Println(b)
	&#47;&#47; 使用对象池
	for i := 0; i &lt; 1000000000; i++{
		obj := bytePool.Get().(*[]byte)
		_ = obj
		bytePool.Put(obj)
	}
	c := time.Now().Unix()
	fmt.Println(c)
	fmt.Println(&quot;without pool &quot;, b - a, &quot;s&quot;)
	fmt.Println(&quot;with    pool &quot;, c - b, &quot;s&quot;)
}

&#47;&#47;  run时禁用掉编译器优化，才会体现出有pool的优势
&#47;&#47;  go run -gcflags=&quot;-l -N&quot; testSyncPool1.go</div>2019-11-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/33/7a/ac307bfc.jpg" width="30px"><span>到不了的塔</span> 👍（12） 💬（0）<div>临时对象池初始化时指定new字段对应的函数返回一个新建临时对象；
临时对象使用完毕时调用临时对象池的put方法，把该临时对象put回临时对象池中。
这样就能保证一个临时对象池中总有比较充足的临时对象。</div>2018-11-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/20/27/a6932fbe.jpg" width="30px"><span>虢國技醬</span> 👍（5） 💬（2）<div>二刷</div>2019-11-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/12/70/10faf04b.jpg" width="30px"><span>Lywane</span> 👍（2） 💬（0）<div>直到看到最近两三章，我才体会到，老师就是在讲源码啊！对着源码学习课程，对着课程学习源码。事半功倍！！</div>2020-03-31</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/a9/b1/0d550474.jpg" width="30px"><span>Haij!</span> 👍（1） 💬（0）<div>fmt包为了识别、格式化和暂存需要打印的内容，定义了一个名为pp的结构体。调用不同的打印方法时，都需要一个pp的结构体介入逻辑进行处理；如果未使用sync.Pool，则每次均会通过new函数初始化pp类型的变量，这时会频繁申请内存。所以为避免每次需要时都调用pp的new方法申请内存，故基于sync.Pool创建一个临时对象池。当打印操作很活跃时，可以直接从池中获取pp结构体并使用；使用后抹取过程中的信息再存入。一方面可以利用“缓存”特性进行性能提升，避免频繁内存申请分配；另一方面可以借由sync.Pool初始时在运行时系统注册的cleanPool方法，及时清理空间，释放内存。</div>2022-08-25</li><br/>
</ul>