你好，我是Mike。今天我们来了解并发编程的另一种范式——使用channel在不同的任务间进行通信。

channel翻译成中文就是通道或管道，用来在task之间传递消息。这个概念本身并不难。我们回忆一下上节课的目标：要在多个任务中同时对一个内存数据库进行更新。其实我们也可以用channel的思路来解决这个问题。

我们先来分解一下任务。

1. 创建三个子任务，task\_a、task\_b 和另一个起代理作用的 task\_c。
2. 在 task\_a 和 task\_b 中，不直接操作db本身，而是向 task\_c 发一个消息。
3. task\_c 里面会拿到 db 的所有权，收到从 task\_a 和 task\_b 来的消息后，对db进行操作。

基于这个思路，我们来重写上一节课的示例。

## MPSC Channel

我们使用tokio中的MPSC Channel来实现。MPSC Channel是多生产者，单消费者通道（Multi-Producers Single Consumer）。

MPSC的基本用法如下：

```plain
let (tx, mut rx) = mpsc::channel(100);
```

使用MPSC模块的 `channel()` 函数创建一个通道对，tx表示发送端，rx表示接收端，rx前面要加mut修饰符，因为rx在接收数据的时候使用了可变借用。channel使用的时候要给一个整数参数，表示这个通道容量多大。tokio的这个 `mpsc::channel` 是带背压功能的，也就是说，如果发送端发得太快，接收端来不及消耗导致通道堵塞了的话，这个channel会让发送端阻塞等待，直到通道里面的数据包被消耗到留出空位为止。
<div><strong>精选留言（12）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/10/82/42/8b04d489.jpg" width="30px"><span>刘丹</span> 👍（4） 💬（2）<div>请问老师： r = task_a =&gt; r.unwrap() 这是闭包，还是匿名函数？

</div>2023-11-24</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/7Q403U68Oy4lXG5sFBPVKLrfwaRzBqpBZibpEBXcPf9UOO3qrnh7RELoByTLzBZLkN9Nukfsj7DibynbZjKAKgag/132" width="30px"><span>superggn</span> 👍（1） 💬（1）<div>背压 - back pressure

带背压的 channel
tokio::mpsc::channel(n)
std::mpsc::sync_channel(n)

不带背压的 channel
tokio::mpsc::unbounded_channel();
std::mpsc::channel();</div>2024-01-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/61/c1/93031a2a.jpg" width="30px"><span>Aaaaaaaaaaayou</span> 👍（1） 💬（1）<div>join 和 select 类似于 JavaScript 中的 Promise.all 和 Promise.race</div>2024-01-26</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/7Q403U68Oy4lXG5sFBPVKLrfwaRzBqpBZibpEBXcPf9UOO3qrnh7RELoByTLzBZLkN9Nukfsj7DibynbZjKAKgag/132" width="30px"><span>superggn</span> 👍（0） 💬（1）<div>思考题
- Arc::new(Mutex::new(target_var));
- res = join_handler.await.unwrap();
- channel
</div>2023-12-25</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/7Q403U68Oy4lXG5sFBPVKLrfwaRzBqpBZibpEBXcPf9UOO3qrnh7RELoByTLzBZLkN9Nukfsj7DibynbZjKAKgag/132" width="30px"><span>superggn</span> 👍（0） 💬（1）<div>捉虫： `等待所有任务一起返回`  main 前面少个 fn</div>2023-12-25</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1f/05/ca/eefef69b.jpg" width="30px"><span>刘永臣</span> 👍（0） 💬（1）<div>.await()类似于等待组吧？ channel的四种模式也是go channel常用的四种场景。</div>2023-11-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/27/06/f8/09ad484b.jpg" width="30px"><span>学水</span> 👍（0） 💬（1）<div>如果通道都没有任何生产者消息，select语句中的消费者是堵塞在那里还是会之间进入下一个语句呢</div>2023-11-25</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/ee/85/c0cf6544.jpg" width="30px"><span>老大</span> 👍（0） 💬（1）<div>为啥我按照你写的，运行不起来呢？</div>2023-11-24</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTLO6XvxfFPMGcVSSX8uIZY2yib29qlyat178pU4QM3gIic5GXZ8PC0tzRiazP3FiajXbTj19SE4ZhV0gQ/132" width="30px"><span>PEtFiSh</span> 👍（0） 💬（1）<div>从任务收集返回结果的方式有：
1、任务直接返回值，然后通过handler取回，比如：a = task_a.await.unwrap();
2、通过锁的方式直接写在目标位置
3、通过channel的形式传递结果
4、似乎也可以unsafe来写全局变量。</div>2023-11-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/18/5c/d7/3b92bb0d.jpg" width="30px"><span>伯阳</span> 👍（0） 💬（1）<div>这种无锁并发，快是快了点，但是如果给通道打满了，怎么处理呢</div>2023-11-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/ff/88/36fb189f.jpg" width="30px"><span>BBJB</span> 👍（0） 💬（0）<div>MPSC Channel模式，如果在send的异步线程中，套一层循环 for i in 0..100{tx1.send(50).await}
为什么接受线程需要等循环完才开始执行recv。而不是send一个，recv一个。</div>2024-04-25</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/7Q403U68Oy4lXG5sFBPVKLrfwaRzBqpBZibpEBXcPf9UOO3qrnh7RELoByTLzBZLkN9Nukfsj7DibynbZjKAKgag/132" width="30px"><span>superggn</span> 👍（0） 💬（0）<div>背压 - back pressure

带背压的 channel
tokio::mpsc::channel(n)
std::mpsc::sync_channel(n)

不带背压的 channel
tokio::mpsc::unbounded_channel();
std::mpsc::channel();</div>2024-01-26</li><br/>
</ul>