你好，我是陈天。

对于并发状态下这三种常见的工作模式：自由竞争模式、map/reduce 模式、DAG 模式，我们的难点是如何在这些并发的任务中进行同步。atomic / Mutex 解决了自由竞争模式下并发任务的同步问题，也能够很好地解决 map/reduce 模式下的同步问题，因为此时同步只发生在 map 和 reduce 两个阶段。  
![](https://static001.geekbang.org/resource/image/00/58/003294c9ba4b291e47585fa1a599a358.jpg?wh=2364x1142)

然而，它们没有解决一个更高层次的问题，也就是 DAG 模式：如果这种访问需要按照一定顺序进行或者前后有依赖关系，该怎么做？

这个问题的典型场景是**生产者-消费者模式：生产者生产出来内容后，需要有机制通知消费者可以消费**。比如 socket 上有数据了，通知处理线程来处理数据，处理完成之后，再通知 socket 收发的线程发送数据。

## Condvar

所以，操作系统还提供了 Condvar。Condvar 有两种状态：

- 等待（wait）：线程在队列中等待，直到满足某个条件。
- 通知（notify）：当 condvar 的条件满足时，当前线程通知其他等待的线程可以被唤醒。通知可以是单个通知，也可以是多个通知，甚至广播（通知所有人）。

在实践中，Condvar 往往和 Mutex 一起使用：**Mutex 用于保证条件在读写时互斥，Condvar 用于控制线程的等待和唤醒**。我们来看一个例子：
<div><strong>精选留言（14）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/24/cf/9e/e695885e.jpg" width="30px"><span>×22</span> 👍（3） 💬（1）<div>请问一下，目前rust的标准库中并没有类似concurrent hash map等并发安全的集合，虽然第三方库有一些实现，但是不容易从中做出选择，请问老师有什么推荐吗</div>2021-12-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/22/f4/9fd6f8f0.jpg" width="30px"><span>核桃</span> 👍（2） 💬（1）<div>Channel 把锁封装在了队列写入和读取的小块区域内，然后把读者和写者完全分离，使得读者读取数据和写者写入数据，对开发者而言，除了潜在的上下文切换外，完全和锁无关，就像访问一个本地队列一样

这段文字，我还是没有很明白，所谓对于channel和mutex锁的区别，是不是可以这样理解？channel可以看成是一个队列(vec那样的)，然后channel这里就是一头写入一头消费，那么如果有并发的时候，就是对头尾进行加锁，并且会做多一些其他的辅助操作，例如队列满了或者空的时候各种安全检查判断等等，实际上channel就是对mutex+queue的抽象封装？ 多谢了</div>2021-12-05</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/d2/1f/2ef2514b.jpg" width="30px"><span>newzai</span> 👍（1） 💬（1）<div>go经常会使用 chan struct 来作为actor对象的退出信号，rust有什么建议不？不想和数据channel混合在一起。</div>2021-11-16</li><br/><li><img src="" width="30px"><span>千回百转无劫山</span> 👍（0） 💬（1）<div>读完本节有一个感悟，actor model是异步任务级别的“微服务”：发送信息给一个actor，然后从actor再接收信息，就类似于后端中发送一个请求给一个微服务，再接收响应。也就是说，一个actor对应一个“”微服务“”，不知道这种理解是否正确？还有就是，一个actor对应的是类似于tokio的一个task吗？</div>2021-11-16</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/26/27/eba94899.jpg" width="30px"><span>罗杰</span> 👍（0） 💬（1）<div>对，合理的使用 Channel，不应该死搬硬套。</div>2021-11-15</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/af/af/8b03ce2c.jpg" width="30px"><span>GengTeng</span> 👍（0） 💬（2）<div>笨拙地用 Channel 叠加 Channel 来应对所有的场景?Go: 你直接说我名儿得了。</div>2021-11-15</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/2b/07/66/b703a6e5.jpg" width="30px"><span>朱叶子</span> 👍（5） 💬（0）<div>工作线程中，缺了drop(started)，导致主线程无法获取mutex</div>2022-06-24</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/UmdVZ3v0axr9ymauQGQRyexSK58icbICh9h2hIycfDB7pJFPeYvYVRFW4ql6icXbE7s1RqScra0TP5HL2XWVN5Nw/132" width="30px"><span>Geek_e188ed</span> 👍（2） 💬（1）<div>老师，代码示例有点少啊，比如Channel这块，你的文字描述我都看懂了，但是没有使用Channel的代码示例，可能怎么调用我都不知道</div>2022-07-10</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/BtgsMc6CpC0O1djDcNicib2eTDliaLicZjibH4dDVKZPuF9gaIG3VGEanFNnx8wqt3iaPwKD8uZcNNaOlicT2PwuToVxQ/132" width="30px"><span>Rex Wang</span> 👍（1） 💬（0）<div>Mutex使用lock方法生成Guard锁住数据，而Guard通过drop方法才能把数据解锁。老师的例子化用了doc中的例子，但因为没有对变量 started 显式使用drop方法，而使用loop阻塞了 started 自动调用drop，所以和预设的结果表现不同。</div>2023-09-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/29/ce/f1/d2fc86bb.jpg" width="30px"><span>终生恻隐</span> 👍（1） 💬（0）<div>#[test]
fn test_mpsc() {
    let (a2btx, a2brx) = mpsc::channel();
    let (b2atx, b2arx) = mpsc::channel();

    let threada = thread::spawn(move || {
        a2btx.send(&quot;hello world!&quot;.to_string()).unwrap();
        for re in b2arx {
            println!(&quot;{}\n&quot;, re);
            thread::sleep(Duration::from_secs(1));
            a2btx.send(&quot;hello world!&quot;.to_string()).unwrap();
        }
    });

    let threadb = thread::spawn(move || {
        for re in a2brx {
            println!(&quot;{}\n&quot;, re);
            thread::sleep(Duration::from_secs(1));
            b2atx.send(&quot;goodbye!&quot;.to_string()).unwrap();
        }
    });

    thread::sleep(Duration::from_secs(10));
    return
}</div>2021-11-15</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/f8/ba/d28174a9.jpg" width="30px"><span>Geek_zbvt62</span> 👍（0） 💬（0）<div>golang也是有atomic，mutex，rwlock，cond的，而且各种三方库也是把这些原语用得飞起。只是官方一直在强烈建议使用channel来用在大多数场景，这可能就是文中说的“但不该营造一种气氛”?</div>2022-10-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/27/fb/f7/88ab6f83.jpg" width="30px"><span>进击的Lancelot</span> 👍（0） 💬（0）<div>思考题：https:&#47;&#47;play.rust-lang.org&#47;?version=stable&amp;mode=debug&amp;edition=2021&amp;gist=3604e3e575fd7dbc98c1e926c62583eb</div>2022-09-30</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1c/f8/4e/3026516d.jpg" width="30px"><span>一雄</span> 👍（0） 💬（0）<div>老师，前面发的代码，和小伙伴讨论了一下以后，知道问题在哪里了。在子线程上，lock需要在通知完了condvar之后，需要释放，那个lock。我想到的打补丁的方法是，加个大括号，和老师信息更新一下</div>2022-03-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1c/f8/4e/3026516d.jpg" width="30px"><span>一雄</span> 👍（0） 💬（2）<div>
use std::sync::{Arc, Condvar, Mutex};
use std::thread;
use std::time::Duration;

fn main() {
    let pair = Arc::new((Mutex::new(false), Condvar::new()));
    let pair2 = Arc::clone(&amp;pair);

    thread::spawn(move || {
        let (lock, cvar) = &amp;*pair2;
        let mut started = lock.lock().unwrap();
        *started = true;
        eprintln!(&quot;I&#39;m a happy worker!&quot;);
        &#47;&#47; 通知主线程
        cvar.notify_one();
        loop {
            thread::sleep(Duration::from_secs(1));
            println!(&quot;working...&quot;);
        }
    });

    &#47;&#47; 等待工作线程的通知
    let (lock, cvar) = &amp;*pair;
    let mut started = lock.lock().unwrap();
    while !*started {
        started = cvar.wait(started).unwrap();
    }
    eprintln!(&quot;Worker started!&quot;);
}

老师麻烦看一下，这个demo跑不起来，我尝试把loop拿掉发现是有效的，但没理解为什么加了loop就无效了</div>2022-03-21</li><br/>
</ul>