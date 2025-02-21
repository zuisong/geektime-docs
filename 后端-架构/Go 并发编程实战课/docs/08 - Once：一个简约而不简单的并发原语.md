你好，我是鸟窝。

这一讲我来讲一个简单的并发原语：Once。为什么要学习Once呢？我先给你答案：**Once可以用来执行且仅仅执行一次动作，常常用于单例对象的初始化场景。**

那这节课，我们就从对单例对象进行初始化这件事儿说起。

初始化单例资源有很多方法，比如定义package级别的变量，这样程序在启动的时候就可以初始化：

```
package abc

import time

var startTime = time.Now()
```

或者在init函数中进行初始化：

```
package abc

var startTime time.Time

func init() {
  startTime = time.Now()
}

```

又或者在main函数开始执行的时候，执行一个初始化的函数：

```
package abc

var startTime time.Tim

func initApp() {
    startTime = time.Now()
}
func main() {
  initApp()
}
```

这三种方法都是线程安全的，并且后两种方法还可以根据传入的参数实现定制化的初始化操作。

但是很多时候我们是要延迟进行初始化的，所以有时候单例资源的初始化，我们会使用下面的方法：

```
package main

import (
    "net"
    "sync"
    "time"
)

// 使用互斥锁保证线程(goroutine)安全
var connMu sync.Mutex
var conn net.Conn

func getConn() net.Conn {
    connMu.Lock()
    defer connMu.Unlock()

    // 返回已创建好的连接
    if conn != nil {
        return conn
    }

    // 创建连接
    conn, _ = net.DialTimeout("tcp", "baidu.com:80", 10*time.Second)
    return conn
}

// 使用连接
func main() {
    conn := getConn()
    if conn == nil {
        panic("conn is nil")
    }
}
```

这种方式虽然实现起来简单，但是有性能问题。一旦连接创建好，每次请求的时候还是得竞争锁才能读取到这个连接，这是比较浪费资源的，因为连接如果创建好之后，其实就不需要锁的保护了。怎么办呢？

这个时候就可以使用这一讲要介绍的Once并发原语了。接下来我会详细介绍Once的使用、实现和易错场景。

# Once的使用场景

**sync.Once只暴露了一个方法Do，你可以多次调用Do方法，但是只有第一次调用Do方法时f参数才会执行，这里的f是一个无参数无返回值的函数。**
<div><strong>精选留言（28）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/11/1d/34/8201baab.jpg" width="30px"><span>端贺</span> 👍（19） 💬（4）<div>问题一：分离固定内容和非固定内容，使得固定的内容能被内联调用，从而优化执行过程。
问题二：Once被拷贝的过程中内部的已执行状态不会改变，所以Once不能通过拷贝多次执行。
不知道回答对不对，请老师指点。</div>2020-11-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/4e/bd/4076ebc4.jpg" width="30px"><span>Geek_klrat9</span> 👍（6） 💬（2）<div>请教这里所说的内联，提高执行效率是什么意思？</div>2020-11-16</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/62/dc/8876c73b.jpg" width="30px"><span>moooofly</span> 👍（6） 💬（13）<div>请教一个问题，在示例代码中有如下片段

```
func (o *Once) doSlow(f func()) {
    o.m.Lock()
    defer o.m.Unlock()
    &#47;&#47; 双检查
    if o.done == 0 {
        defer atomic.StoreUint32(&amp;o.done, 1)
        f()
    }
}
```

在双检查整改地方，读取 o.done 的值并没有使用使用 atomic.LoadUint32(&amp;o.done) 的方式，按照我的理解，是因为已经处于 o.m.Lock() 的保护下的缘故；那是否 atomic.StoreUint32(&amp;o.done, 1) 也可以直接 o.done = 1 呢？毕竟这个代码也在 o.m.Lock() 的保护下</div>2020-10-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/21/3d/c5/f43fa619.jpg" width="30px"><span>🍀柠檬鱼也是鱼</span> 👍（6） 💬（4）<div>once为什么不直接加锁，还需要加多一个 双重检测呢？这块不太懂，望老师解答，我的理解是，调用do()之后直接上锁，等执行完f()再解锁不就行了吗</div>2020-10-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/9b/ba/333b59e5.jpg" width="30px"><span>Linuxer</span> 👍（4） 💬（1）<div>第一个思考题：Linux内核也有很多这种fast code path和slow  code path，我想这样划分是不是内聚性更好，实现更清晰呢,从linux性能分析来看，貌似更多关注点是在slow code path
第二个思考题：应该不可以吧，Once的内部状态已经被改变了</div>2020-10-28</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/PXT6vnzzI62YFMeecE5Jic5jzrO2vAFlZicAOic3sTpTNFvs3YeDcBV2FyBfhHiaKjibplY2vIfBzeFDCkQSRQyOM1eDAvrGtvVJgS5MbCZJeiap4/132" width="30px"><span>Geek_fa7924</span> 👍（0） 💬（1）<div>老师您好。请问一下，这里slow单独提出来是为了让哪个函数可以内联，DO方法调用了 doslow，是不是也不会被内联到，求解惑</div>2024-06-24</li><br/><li><img src="" width="30px"><span>Geek_69bcfa</span> 👍（0） 💬（1）<div>&#47;&#47; 值是3.0或者0.0的一个数据结构
   var threeOnce struct {
    sync.Once
    v *Float
  }
  
    &#47;&#47; 返回此数据结构的值，如果还没有初始化为3.0，则初始化
  func three() *Float {
    threeOnce.Do(func() { &#47;&#47; 使用Once初始化
      threeOnce.v = NewFloat(3.0)
    })
    return threeOnce.v
  }

这个代码里 NewFloat(3.0)，那后面程序用完后怎么释放这个new出来的内存？是否建议在 程序退出前对这个做一下 delete 呢？</div>2023-03-22</li><br/><li><img src="" width="30px"><span>INFRA_1</span> 👍（0） 💬（1）<div>求分享第一题答案</div>2022-11-01</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1b/65/b7/058276dc.jpg" width="30px"><span>i_chase</span> 👍（0） 💬（1）<div>还可以只内联函数在doSlow的前的部分吗，一直以为内联是将整个函数内联上去了</div>2022-07-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1f/3a/8c/fc2c3e5c.jpg" width="30px"><span>xl666</span> 👍（0） 💬（1）<div>‘’这确实是一种实现方式，但是，这个实现有一个很大的问题，就是如果参数 f 执行很慢的话，后续调用 Do 方法的 goroutine 虽然看到 done 已经设置为执行过了，但是获取某些初始化资源的时候可能会得到空的资源，因为 f 还没有执行完。‘’老师我们运行Do初始化的时候 一般加锁保证线程安全 那就就是说 抢到锁的gofunc在初始化fn()没有运行结束时不会释放锁 其他gofunc进不来 所以不会导致上面说的那种情况

我是这样理解的

要是初始化不加锁倒是会 </div>2022-02-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/29/bb/e0/c7cd5170.jpg" width="30px"><span>Bynow</span> 👍（0） 💬（1）<div>请问：(*uint32)(unsafe.Pointer(&amp;o.Once))  这个表达式为什么会是1？
</div>2021-12-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/50/33/9dcd30c4.jpg" width="30px"><span>斯蒂芬.赵</span> 👍（0） 💬（1）<div>既然有未初始化错误的问题，为啥官方不去修复它呢</div>2021-08-30</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/24/98/33/04e9d1a4.jpg" width="30px"><span>Geek_c0a611</span> 👍（0） 💬（2）<div>func (a *AnimalStore) Init() {
        a.once.Do(func() { 
            longOperationSetupDbOpenFilesQueuesEtc() 
             atomic.StoreUint32(&amp;a.inited, 1) 
        })
}

老师，感觉这里的atomic.StoreUint32是不没必要呀，因为Do在执行f()的时候是已经加了锁的</div>2021-06-26</li><br/><li><img src="" width="30px"><span>K菌无惨</span> 👍（0） 💬（1）<div>鸟窝老师,我之前单例模式的时候说double-checking机制可能会由于cpu对代码语句执行顺序的优化导致双检查机制失败,我想知道sync.Once里面的双检查机制会出现同样的情况吗</div>2021-01-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/21/fa/e8/45211b5a.jpg" width="30px"><span>假期</span> 👍（0） 💬（3）<div>func (o *Once) doSlow(f func()) {
    o.m.Lock()
    defer o.m.Unlock()
    &#47;&#47; 双检查
    if o.done == 0 {
        defer atomic.StoreUint32(&amp;o.done, 1)
        f()
    }
}

老师你好，我看了一些内存模型资料之后想问，
defer atomic.StoreUint32(&amp;o.done, 1)这一行如果换成o.done = 1 的话是不是不能保证
o.done=1 和 f()的执行顺序 ？
</div>2020-11-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/c0/c4/3f7b5eed.jpg" width="30px"><span>悦悦</span> 👍（0） 💬（3）<div>package sync_once

import (
	&quot;sync&quot;
)

type Once struct {
	done uint32
	m    sync.Mutex
}

func (o *Once) Do(f func()) {
	&#47;&#47;if atomic.LoadUint32(&amp;o.done) == 0 {
	&#47;&#47;	o.doSlow(f)
	&#47;&#47;}

	if o.done == 0 {
		o.doSlow(f)
	}
}

func (o *Once) doSlow(f func()) {
	o.m.Lock()
	defer o.m.Unlock()
	&#47;&#47; 双检查
	if o.done == 0 {
		&#47;&#47;defer atomic.StoreUint32(&amp;o.done, 1)
		defer func() { o.done = 1 }()
		f()
	}
}


与不使用atomic有什么区别</div>2020-10-30</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/e1/4f/00476b4c.jpg" width="30px"><span>Remember九离</span> 👍（2） 💬（0）<div>一个once,看着就一点代码还能这么玩������，今日份整理：https:&#47;&#47;github.com&#47;wuqinqiang&#47;Go_Concurrency&#47;tree&#47;main&#47;class_8</div>2020-10-28</li><br/><li><img src="" width="30px"><span>Geek_3e807f</span> 👍（0） 💬（0）<div>Go是有多么拉跨 居然返回值都不实现一下 垃圾</div>2023-11-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/4f/94/05044c31.jpg" width="30px"><span>踢车牛</span> 👍（0） 💬（0）<div>写了一篇文章从介绍了单例模式，也介绍了 sync.once 的又来，感兴趣的可以读一下，保准你有收获

https:&#47;&#47;juejin.cn&#47;post&#47;7124720007447052302</div>2022-07-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/24/df/645f8087.jpg" width="30px"><span>Yayu</span> 👍（0） 💬（0）<div>“如果你真的担心这个 package 级别的变量被人修改，你可以不把它们暴露出来，而是提供一个只读的 GetXXX 的方法，这样别人就不会进行修改了。”

这个方法没法解决全局变量是指针类型或者结构内包含指针类型的变量呀，这种情况又该如何解决呢？</div>2021-07-16</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/b8/3c/1a294619.jpg" width="30px"><span>Panda</span> 👍（0） 💬（0）<div>一旦你遇到只需要初始化一次的场景，首先想到的就应该是 Once 并发原语。</div>2021-01-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/22/17/11/a63acc6a.jpg" width="30px"><span>( ･᷄ὢ･᷅ )</span> 👍（0） 💬（0）<div>1.slow 为了内联
2.不能复制 once里面有mutex 这玩意本身就不能复制</div>2020-12-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/80/de/c6191045.jpg" width="30px"><span>gitxuzan</span> 👍（0） 💬（0）<div>第二个坑前几天就采了，从数据库拉一份缓存，结果刚好数据库重启，导致初始化失败了，后面改成 == nil，最多是不是那一刻并发执行了，因为是缓存数据问题不大，是不是如果单实例没加锁就不能用 nil这么判断？</div>2020-10-30</li><br/><li><img src="" width="30px"><span>fsyyft</span> 👍（0） 💬（0）<div>这样扩展是否可以？

type (
	OnceDo interface {
		DoOnce(p ...interface{}) (interface{}, error)
	}

	OnceFunc func(p ...interface{}) (interface{}, error)
)

func (o OnceFunc) DoOnce(p ...interface{}) (interface{}, error) {
	return o(p)
}

type (
	Once struct {
		done uint32
		m    sync.Mutex
	}
)

func (o *Once) Do(i OnceDo, p ...interface{}) (interface{}, error) {
	return o.DoFunc(i.DoOnce, p)
}

func (o *Once) DoFunc(f OnceFunc, p ...interface{}) (interface{}, error) {
	var v interface{}
	var err error

	if atomic.LoadUint32(&amp;o.done) == 0 {
		v, err = o.doSlow(f, p)
	}

	return v, err
}

func (o *Once) Done() bool {
	return atomic.LoadUint32(&amp;o.done) == 1
}

func (o *Once) doSlow(f OnceFunc, p ...interface{}) (interface{}, error) {
	o.m.Lock()
	defer o.m.Unlock()

	var v interface{}
	var err error

	&#47;&#47; 已经加锁了，可以不需要使用 atomic.LoadUint32(&amp;o.done) == 0 判断。
	if o.done == 0 {
		defer func() {
			if r := recover(); nil != r {
				&#47;&#47; 如果出现 panic 了，recover 后，继续向外抛出。
				panic(r)
			} else if nil == err {
				&#47;&#47; 没有异常时，才设置完成。
				atomic.StoreUint32(&amp;o.done, 1)
			}
		}()
		v, err = f(p)
	}

	return v, err
}</div>2020-10-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/4b/69/c02eac91.jpg" width="30px"><span>大漠胡萝卜</span> 👍（0） 💬（1）<div>```go
atomic.LoadUint32((*uint32)(unsafe.Pointer(&amp;o.Once))) == 1
```
这个是怎么判断执行完的呢</div>2020-10-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/8f/cf/890f82d6.jpg" width="30px"><span>那时刻</span> 👍（0） 💬（0）<div>slowXXXX 的方法，从 XXXX 方法中单独抽取出来，是为了优化代码，方便内联</div>2020-10-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/21/3d/c5/f43fa619.jpg" width="30px"><span>🍀柠檬鱼也是鱼</span> 👍（0） 💬（1）<div>噢噢理解了，呜呜，双重检测是为了避免重复执行f()</div>2020-10-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/17/6e/76b4aa3d.jpg" width="30px"><span>橙子888</span> 👍（0） 💬（0）<div>打卡。</div>2020-10-28</li><br/>
</ul>