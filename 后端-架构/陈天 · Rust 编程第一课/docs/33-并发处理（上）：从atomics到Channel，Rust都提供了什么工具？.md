你好，我是陈天。

不知不觉我们已经并肩作战三十多讲了，希望你通过这段时间的学习，有一种“我成为更好的程序员啦！”这样的感觉。这是我想通过介绍 Rust 的思想、处理问题的思路、设计接口的理念等等传递给你的。如今，我们终于来到了备受期待的并发和异步的篇章。

很多人分不清并发和并行的概念，Rob Pike，Golang 的创始人之一，对此有很精辟很直观的解释：

> Concurrency is about **dealing with** lots of things at once. Parallelism is about **doing** lots of things at once.

并发是一种同时处理很多事情的能力，并行是一种同时执行很多事情的手段。

我们把要做的事情放在多个线程中，或者多个异步任务中处理，这是并发的能力。在多核多 CPU 的机器上同时运行这些线程或者异步任务，是并行的手段。可以说，并发是为并行赋能。当我们具备了并发的能力，并行就是水到渠成的事情。

其实之前已经涉及了很多和并发相关的内容。比如用 std::thread 来创建线程、用 std::sync 下的并发原语（Mutex）来处理并发过程中的同步问题、用 Send/Sync trait 来保证并发的安全等等。
<div><strong>精选留言（17）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/10/53/db/858337e3.jpg" width="30px"><span>Ethan Liu</span> 👍（8） 💬（1）<div>rust相比go在并发处理上 有什么优点和缺点？</div>2021-11-16</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/21/5e/f0/62d8cf9e.jpg" width="30px"><span>D. D</span> 👍（3） 💬（1）<div>既然 Semaphore 是 Mutex 的推广，那么实现的思路应该有点类似。
参考老师文章中所说的 Mutex 的实现方法，实现 Semaphore 的一个思路是：
我们可以用一个 AtomicUsize 记录可用的 permits 的数量。在获取 permits 的时候，如果无法获取到足够的 permits，就把当前线程挂起，放入 Semaphore 的一个等待队列里。获取到 permits 的线程完成工作后退出临界区时，Semaphore 给等待队列发送信号，把队头的线程唤醒。

至于像图书馆那样的人数控制系统，tokio 的 Semaphore 文档中使用 Semaphore::acquire_owned 的例子可以说就是这种场景的模拟。</div>2021-11-14</li><br/><li><img src="" width="30px"><span>Geek_b52974</span> 👍（1） 💬（1）<div>作業:
use std::sync::Arc;

use tokio::{sync::Semaphore, task::JoinHandle};

#[tokio::main]
async fn main() {
    let library = Box::new(Library::new(3));
    let mut tasks: Vec&lt;JoinHandle&lt;()&gt;&gt; = vec![];
    for i in 0..10 {
        tasks.push(library.enter(move || println!(&quot;no: {}, borrow book&quot;, i)));
    }
    for task in tasks {
        task.await.unwrap();
    }
    println!(&quot;{:?}&quot;, library.semaphore.available_permits());
}

struct Library {
    semaphore: Arc&lt;Semaphore&gt;,
}

impl Library {
    fn new(capacity: usize) -&gt; Self {
        Self {
            semaphore: Arc::new(Semaphore::new(capacity)),
        }
    }

    fn enter(&amp;self, chore: impl Fn() + Send + &#39;static) -&gt; JoinHandle&lt;()&gt; {
        let semaphore = self.semaphore.clone();
        tokio::spawn(async move {
            &#47;&#47; remove this you will get panic
            &#47;&#47; semaphore.close();
            println!(&quot;{} quota left&quot;, semaphore.available_permits());
            let s = semaphore.acquire_owned().await.unwrap();
            chore();
            drop(s);
        })
    }
}</div>2021-12-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/29/ce/f1/d2fc86bb.jpg" width="30px"><span>终生恻隐</span> 👍（1） 💬（1）<div>&#47;&#47; [dependencies]
&#47;&#47; tokio = { version = &quot;1&quot;, features = [&quot;full&quot;] }
&#47;&#47; chrono = &quot;*&quot;


use tokio::sync::{Semaphore, TryAcquireError};
use std::sync::Arc;
use std::thread;
use std::time::Duration;
use chrono::prelude::*;

#[tokio::main]
async fn main() {
    let semaphore = Arc::new(Semaphore::new(3));
    let mut join_handles = Vec::new();

    for c in 0..5 {
        let permit = semaphore.clone().acquire_owned().await.unwrap();
        join_handles.push(tokio::spawn(async move {
            let local: DateTime&lt;Local&gt; = Local::now();
            println!(&quot;count{} start time: {}&quot;, c+1, local);
            thread::sleep(Duration::new(10, 0));
            drop(permit);
        }));
    }

    for handle in join_handles {
        handle.await.unwrap();
    }
}</div>2021-11-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/f3/cf/851dab01.jpg" width="30px"><span>Milittle</span> 👍（0） 💬（1）<div>cas是指令集指令提供的能力 一般语言封装的并发原语都是在这个基础上的</div>2022-01-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/18/be/aa622bf8.jpg" width="30px"><span>爱学习的小迪</span> 👍（0） 💬（1）<div>感觉和java对应的功能，原理一致</div>2022-01-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/22/f4/9fd6f8f0.jpg" width="30px"><span>核桃</span> 👍（0） 💬（1）<div>另外关于Ordering那几个的区别，个人写代码的时候，绝大部分时候，要么最简单的Relaxed，要么最严格的SeqCst，剩下的，不一定考虑那么多，除非特殊需要才去查一下区别，平时记不住的。。。</div>2021-12-05</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/22/f4/9fd6f8f0.jpg" width="30px"><span>核桃</span> 👍（0） 💬（1）<div>理解一下，对于所谓的指令原子操作，在计算机底层里面，没记错就是中断总线关闭吧。

然后那段优化的代码，就是拿不到锁先while空转一下，这里就有点像java的自旋锁的概念那样。
当然这里为什么空转性能会比spin好，从系统的角度理解，空转没有调用系统调用，那么就没有太多的进程或者线程切换，而切换这个是涉及上下文变更的。不管进程还是线程，上下文切换的时候，其实五大结构都是要考虑的，例如信号量那些是否要保存起来等等，那样代码自然会大很多了。

不知道这样理解是否对哈。</div>2021-12-05</li><br/><li><img src="" width="30px"><span>Geek_b52974</span> 👍（0） 💬（1）<div>compare_exchange(false, true, Ordering::Acquire, Ordering::Relaxed)
想问一下第三个参数 为何不是 acqRel，这样其他线程会知道吗？</div>2021-11-16</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/26/27/eba94899.jpg" width="30px"><span>罗杰</span> 👍（0） 💬（1）<div>CAS 的原理挺绕的，需要好好的消化，最近也在看“Go 并发实战课”，有一些互通的地方。</div>2021-11-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/e5/ab/56f348e5.jpg" width="30px"><span>ELSE</span> 👍（1） 💬（0）<div>golang不是也支持atomic, mutex这些原语吗，为什么说遇到channel不好解决的时候就比较尴尬呢，不好理解</div>2022-07-13</li><br/><li><img src="" width="30px"><span>Geek_9f3c8c</span> 👍（1） 💬（1）<div>该文章关于CAS的代码示例似乎并未实现线程间同步，只是实现了对临界区访问的互斥。该示例运行结果可能是100或者10。</div>2022-04-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/28/91/61/7ff2f4d5.jpg" width="30px"><span>无邪</span> 👍（0） 💬（0）<div>&#47;&#47; semaphore 作业
use std::sync::Mutex;
&#47;&#47;atomic
use std::sync::atomic::{AtomicUsize, Ordering};
use std::error::Error;

&#47;&#47; item id
struct Item {
    id: usize,
}

struct Semaphore {
    count: AtomicUsize,
    max: usize,
    queue: Mutex&lt;Vec&lt;usize&gt;&gt;,
}

impl Semaphore {
    fn new(max: usize) -&gt; Self {
        Self {
            count: AtomicUsize::new(0),
            max,
            queue: Mutex::new(Vec::new()),
        }
    }

    fn add(&amp;self, item_id: usize) -&gt; Option&lt;usize&gt;{
        let mut count = self.count.fetch_add(1, Ordering::Acquire);
        if *count &gt; self.max {
            return Some(item_id);
        }

        self.queue.lock().unwrap().push(item_id);
        None
    }
    fn remove(&amp;self, item_id: usize) -&gt; Option&lt;usize&gt; {
        let mut count = self.count.fetch_sub(1, Ordering::Release);
        &#47;&#47; 遍历vec， 找到item
        let mut queue = self.queue.lock().unwrap();
        for (i, &amp;id) in queue.iter().enumerate() {
            if id == item_id {
                queue.remove(i);
                return None;
            }
        }
        Some(item_id)
    }
}

</div>2025-02-17</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/BtgsMc6CpC0O1djDcNicib2eTDliaLicZjibH4dDVKZPuF9gaIG3VGEanFNnx8wqt3iaPwKD8uZcNNaOlicT2PwuToVxQ/132" width="30px"><span>Rex Wang</span> 👍（0） 💬（0）<div>按老师的推荐找到一个博客，用c++把ordering讲得很清楚。

https:&#47;&#47;luyuhuang.tech&#47;2022&#47;06&#47;25&#47;cpp-memory-order.html#%E5%86%85%E5%AD%98%E9%A1%BA%E5%BA%8F</div>2023-09-06</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/27/fb/f7/88ab6f83.jpg" width="30px"><span>进击的Lancelot</span> 👍（0） 💬（0）<div>作业：https:&#47;&#47;play.rust-lang.org&#47;?version=stable&amp;mode=debug&amp;edition=2021&amp;gist=453c39051a8257931b0cb167bf8fc60f</div>2022-09-30</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/7e/38/ae659af9.jpg" width="30px"><span>BeCool</span> 👍（0） 💬（1）<div>老师，我是刚学习的萌新，想问下，这段代码有时候是100有时候是10，正常吗</div>2022-06-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/bd/a9/688b9bc6.jpg" width="30px"><span>菅田</span> 👍（0） 💬（0）<div>看了一遍老师的文章之后结合crust的youtube视频，有一点还是没弄明白：什么情况下可以不使用SeqCst？
还有我对Ordering的理解是否正确：
1. Ordering 是对同一个Atomic的值的使用的限制，如果涉及多个atomic的值时应该使用SeqCst来保证顺序；
2. 在对同一个值读写时，load时使用Acquire，在store时使用Release，用这Acquire 、Release代码包裹起来中间的读写操作是安全的？比方说：
```
while !x.load(Ordering::Acquire) {
}
x.store(&#47;** );**&#47;
x.store(&#47;** );**&#47;
x.store(&#47;** );**&#47; &#47;&#47; 这三句store都是安全的，在被别的线程load的时候都是在x.store(1)之后的结果？其他线程在此期间不会插入进来；
x.store(1, Ordering::Release);

```</div>2022-05-29</li><br/>
</ul>