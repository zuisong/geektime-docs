你好，我是陈天。

通过前几讲的学习，我们对并发处理，尤其是常用的并发原语，有了一个比较清晰的认识。并发原语是并发任务之间同步的手段，今天我们要学习的 Future 以及在更高层次上处理 Future 的 async/await，是**产生和运行并发任务**的手段。

不过产生和运行并发任务的手段有很多，async/await 只是其中之一。在一个分布式系统中，并发任务可以运行在系统的某个节点上；在某个节点上，并发任务又可以运行在多个进程中；而在某个进程中，并发任务可以运行在多个线程中；在某个（些）线程上，并发任务可以运行在多个 Promise / Future / Goroutine / Erlang process 这样的协程上。

它们的粒度从大到小如图所示：  
![](https://static001.geekbang.org/resource/image/75/66/7575380e2255ae078569bb7e185da666.jpg?wh=2139x979)

在之前的课程里，我们大量应用了线程这种并发工具，在 kv server 的构建过程中，也通过 async/await 用到了 Future 这样的无栈协程。

其实 Rust 的 Future 跟 JavaScript 的 Promise 非常类似。

如果你熟悉 JavaScript，应该熟悉 Promise 的概念，[02](https://time.geekbang.org/column/article/410038)也简单讲过，它代表了**在未来的某个时刻才能得到的结果的值**，Promise 一般存在三个状态；

1. 初始状态，Promise 还未运行；
2. 等待（pending）状态，Promise 已运行，但还未结束；
3. 结束状态，Promise 成功解析出一个值，或者执行失败。
<div><strong>精选留言（10）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/10/f7/1b/db7a0edc.jpg" width="30px"><span>Marvichov</span> 👍（6） 💬（1）<div>现在一节课需要很久才勉强消化...这课真心值!

```
    error: future cannot be sent between threads safely
    29 | tokio::spawn(async move {
    | ^^^^^^^^^^^^ future created by async block is not Send
```

tokio::spawn要求T是Send, 也就是可以cross thread boundary

```
pub fn spawn&lt;T&gt;(task: T) -&gt; JoinHandle&lt;T::Output&gt; 
where
    T: Future + Send + &#39;static,
    T::Output: Send + &#39;static, 

```
参见: https:&#47;&#47;docs.rs&#47;tokio&#47;0.2.18&#47;tokio&#47;fn.spawn.html

对executor了解很少...但从文中的提示 (task stealing, 从其他thread偷task), executor应该有个thread pool可以在不同的thread里面poll future...

至于await里面怎么就有多线程的executor, 还希望老师答疑解惑!</div>2021-12-08</li><br/><li><img src="" width="30px"><span>CyNevis</span> 👍（0） 💬（2）<div>标准库的 Mutex 不能跨越 await, 盲猜一手是不是标准库的Mutex实现是依赖线程绑定, 得去看代码是怎么实现的</div>2021-12-01</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/26/27/eba94899.jpg" width="30px"><span>罗杰</span> 👍（0） 💬（1）<div>代码中的 toml::from_str 编译不过，但在 play.rust-lang.org 中竟然可以编译通过，很神奇，我在本地添加了 toml 库，并且 use toml 之后，代码就可以正常运行了。</div>2021-11-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/a2/4b/b72f724f.jpg" width="30px"><span>zxk</span> 👍（4） 💬（0）<div>这是由于 MutexGuard 没有实现 Send trait。
对于 MutexGuard 为什么不实现 Send 的一点思考，不知道是否理解正确，望老师指点下。
标准库的 MutexGuard 主要是针对线程的，一个线程通过 lock 获取到锁后独占该临界区的资源。假设允许 MutexGuard 跨越 await，那么 MutexGuard 就有可能随着 Future 跑到其他线程上执行，那就破坏了之前的线程独占该临界区的语义了。</div>2022-07-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/e5/ab/56f348e5.jpg" width="30px"><span>ELSE</span> 👍（2） 💬（2）<div>有个疑问，像这样的语句，同步和异步有什么区别吗
let listener = TcpListener::bind(addr).await?;</div>2022-07-13</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/1Asuz2Fe5ibX18xyst9icmXv17j2wbB864bhHTpkAT4YrbJiczVGKxgt5ricrOTn7YSo1Tmug9NImheBjBtspQB5XbzQVonV0mRr6VFDCsEgatc/132" width="30px"><span>Geek_91aad0</span> 👍（1） 💬（0）<div>真的经典，反复做笔记反复理解，配合future的源码才完全看懂！真的是技术深度极高！</div>2024-03-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/26/27/eba94899.jpg" width="30px"><span>罗杰</span> 👍（1） 💬（0）<div>今天的内容要好好消化一下…</div>2021-11-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1b/3c/b8/9489387c.jpg" width="30px"><span>鱼丸粗面</span> 👍（0） 💬（0）<div>mutexGuard的drop方法里有释放锁的功能，它销毁时会释放锁，把它发出去会造成同步语义的破坏。比如guard已经被销毁而当前线程仍然在安全区域修改被保护的数据</div>2022-10-06</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/78/eb/c2fd27f6.jpg" width="30px"><span>RAY_CCW😝😝😝</span> 👍（0） 💬（0）<div>tyr老师，想问一下，其实Rust executor的Reactor 模式，本质是也是用了类似于事件驱动的异步方式来实现？因为近年都在写go，看到这个想起来以前写Python时候的gevent的感觉了。</div>2022-03-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/28/98/e5/a716040e.jpg" width="30px"><span>...zzZ</span> 👍（0） 💬（1）<div>rust future中的task和executor能不能类比于go MPG模型中的G和P？</div>2022-02-22</li><br/>
</ul>