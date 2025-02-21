你好，我是Mike。今天我们一起来学习如何在tokio的多个任务之间共享同一片数据。

并发任务之间如何共享数据是一个非常重要的课题，在所有语言中都会碰到。不同的语言提供的方案支持不尽相同，比如 Erlang 语言默认只提供消息模型，Golang 也推荐使用 channel 来在并发任务之间进行同步。

Rust语言考虑到其应用领域的广泛性和多样性，提供了多种机制来达到这一目的，需要我们根据不同的场景自行选择最合适的机制。所以相对来说，Rust在这方面要学的知识点要多一些，好处是它在几乎所有场景中都能做到最好。

## 任务目标

定义一个内存数据库db，在不同的子任务中，并发地向这个内存数据库更新数据。

## 潜在问题

为了简化问题，我们把 `Vec<u32>` 当作db。比如这个db中现在有10个数据。

```plain
let mut db: Vec<u32> = vec![1,2,3,4,5,6,7,8,9,10];
```

现在有两个任务 task\_a 和 task\_b，它们都想更新db里的第5个元素的数据 db\[4]。

task\_a 想把它更新成 50，task\_b 想把它更新成 100。这两个任务之间是没有协同机制的，也就是互相不知道对方的存在，更不知道对方要干嘛。于是就可能出现这样的情况，两个任务几乎同时发起更新请求，假如 task\_a 领先一点点时间，先把 db\[4] 更新成 50 了，但是它得校验一下更新正确了没有，所以它得发起一个索引请求，把 db\[4] 的数据取出来看看是不是 50。
<div><strong>精选留言（19）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/1e/bc/a3/7f753d36.jpg" width="30px"><span>lilp</span> 👍（6） 💬（2）<div>1. 应该是防止这两个任务还没走完，主线程就结束了？
2. 不会阻塞。我理解的是这两个任务 同时启动，顺序完成。不管他俩怎么去抢这个锁 最后的完成顺序应该还是和main中写的.await() 顺序一样。</div>2023-11-23</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTLO6XvxfFPMGcVSSX8uIZY2yib29qlyat178pU4QM3gIic5GXZ8PC0tzRiazP3FiajXbTj19SE4ZhV0gQ/132" width="30px"><span>PEtFiSh</span> 👍（4） 💬（1）<div>await代码会持续等待直到任务结束，因此在main thread里第一行会阻塞第二行。但这不会让task_a阻塞task_b。加入await可以使最后的println!打印两个任务执行完以后被修改的db值，如果不加入await。有一定几率最后println!打印的还是原始的db</div>2023-11-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/17/99/09/29c46a7b.jpg" width="30px"><span>-</span> 👍（4） 💬（3）<div>有个疑问，Arc::new(Mutex::new(db))后可以将一个不可变的变量变成可变变量？这个是什么原因</div>2023-11-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1e/36/33/3411df0d.jpg" width="30px"><span>seven9t</span> 👍（2） 💬（1）<div>可以说下如果用rust自带的Mutex而不是tokio的会有什么问题 （是否必须配套</div>2024-01-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/62/bb/323a3133.jpg" width="30px"><span>下雨天</span> 👍（2） 💬（4）<div>看实现，就当前例子而言task_a不会阻塞task_b。 如果task_a中loop{}下就可以阻塞了。

有个疑问，为啥task::spawn后面会自动执行呢？ 我理解只有.await了才会加到调度器里面执行。</div>2023-11-23</li><br/><li><img src="" width="30px"><span>Geek_72807e</span> 👍（2） 💬（2）<div>请问老师，方案四中，会不会出现两次修改操作顺序不确定的问题，最终结构可以是40，也会是100？</div>2023-11-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/61/38/d586a684.jpg" width="30px"><span>yunyi</span> 👍（1） 💬（1）<div>1、为了等待任务完成
2、不会阻塞，两个任务是并行运行的，结果也有可能是被改成50，taskb先完成，再执行taska。</div>2024-01-12</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/qUHuge7oea6mA4bUTyJ4rpTP7Havj5m2WEqKvrARDbe8HYnu52vQ8DfAWNkLEfQbic83ibDhnUZYRTwut5Dl8icDA/132" width="30px"><span>雍和</span> 👍（1） 💬（1）<div>会，因为要获取mutex</div>2023-11-22</li><br/><li><img src="" width="30px"><span>Geek_3b58b9</span> 👍（0） 💬（1）<div>对原子变量的读写访问可以用指针？还是说应该用专门的API？我记得原子类型有特定的CPU指令的</div>2024-01-15</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/61/38/d586a684.jpg" width="30px"><span>yunyi</span> 👍（0） 💬（1）<div>哇 ，居然看到了Erlang的字眼，我一直是用erlang做为主力语言的后端开发，最近在学rust，找了很多资料，最后买了老师的教程，如获至宝</div>2024-01-12</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/7Q403U68Oy4lXG5sFBPVKLrfwaRzBqpBZibpEBXcPf9UOO3qrnh7RELoByTLzBZLkN9Nukfsj7DibynbZjKAKgag/132" width="30px"><span>superggn</span> 👍（0） 💬（3）<div>问个事儿， Arc::clone(arc_db) 和 arc_db.clone() 一样吗？

为啥 不用 `std::sync::{Arc, Mutex}` 而是 `tokio::sync::{Arc, Mutex}`

如果是因为在 tokio runtime 里头要用 tokio 的东西的话， 那么在啥情况下会用 std 的几板斧呢？

同步场景都用 std::sync 底下的东西吗？</div>2023-12-21</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/7Q403U68Oy4lXG5sFBPVKLrfwaRzBqpBZibpEBXcPf9UOO3qrnh7RELoByTLzBZLkN9Nukfsj7DibynbZjKAKgag/132" width="30px"><span>superggn</span> 👍（0） 💬（1）<div>思考题
意义： 等执行完了再打印， 对齐一下子， 别任务没跑完主进程就完事儿了
到 await 这块儿就是同步了， 这俩 await 是顺序执行， 
如果 task_a 没执行完， task_b 已经执行完了， 就会卡在 task_a 这里， task_a 这行完事儿了在执行 task_b 的 await, 这会儿 task_b 因为已经完事儿了， 所以第2个 await 不会卡
</div>2023-12-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/30/77/2a/0cd4c373.jpg" width="30px"><span>-Hedon🍭</span> 👍（0） 💬（1）<div>task_a.await.unwrap() 是阻塞等待任务结果，所以 task_a.await.unwrap() 会阻塞 task_b.await.unwrap() ，但是 task_a 不会阻塞 task_b，spwan 并发执行的。</div>2023-12-20</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/axiaxUndY1I8iaOu5qZOwFiaKgicR1AlWsSUyyYIMdEnibuhhzuQnicvXibaOxSakMNAQIPmgicsTfPvUnWJ5WCFzmdHDw/132" width="30px"><span>Geek_e5eb33</span> 👍（0） 💬（1）<div>请问老师，rust 中不建议使用全局变量。那如果我想进行模块化开发，在 A 模块中定义的变量(比如缓存了用户信息)，怎么供其他模块使用呢，目前能想到的是都定义到 main 里。</div>2023-12-15</li><br/><li><img src="" width="30px"><span>Taozi</span> 👍（0） 💬（1）<div>关于arc里面为何需要套lock才能修改值，当然是为了在运行时保证内存安全。为什么说在运行时，因为还有对应的在静态时。还记得最开始我们说rust中每个值都有一个owner，这是为了保证ower在其作用域结束时释放值，这是可以通过代码静态分析出来的。对于所有权不能静态确定的情况，就需要arc来这个第三方来持有所有权，然后动态的决定何时释放值。原理也很简单，就是引用计数。同样最开始我们也说一个值只能同时存在一个可变借用或者多个不可变借用，这也是可以通过静态分析保证的，但是在arc这里只能通过加锁在运行时保证这点。</div>2023-11-22</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/DYAIOgq83eqrbHib1v0wPRVHxrFK2CPQQX8Wg3rRMPiaZ5teMKu5klT48yns6yo4krZsIqHskwdEsibVvQ3QB7CUQ/132" width="30px"><span>Geek_6fjt20</span> 👍（0） 💬（1）<div>太方便了，不像java，即使有各种同步锁也要考虑多种情况下的不一致</div>2023-11-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/39/ab/ca/32d6c05d.jpg" width="30px"><span>哄哄</span> 👍（0） 💬（1）<div>看命名是否规范，有些人会将future命名为task。如果task_a和task_b都是task，那么他们都会在各自执行，task_b不需要等待task_a完成才开始执行，而是在spawn之后就开始执行。如果如果task_a和task_b都是future，那么就是按照顺序执行，task_b必须等待task_a完成才能执行。</div>2023-11-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/39/ab/ca/32d6c05d.jpg" width="30px"><span>哄哄</span> 👍（0） 💬（2）<div>Rwlock：请问怎么理解：Each read and write should be run in its own task.Otherwise ,they can cause a deadlock.</div>2023-11-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/18/5c/d7/3b92bb0d.jpg" width="30px"><span>伯阳</span> 👍（0） 💬（1）<div>确实比其他语言方便多一些</div>2023-11-22</li><br/>
</ul>