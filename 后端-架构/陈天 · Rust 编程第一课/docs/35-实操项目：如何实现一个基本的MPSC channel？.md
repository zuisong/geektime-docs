你好，我是陈天。

通过上两讲的学习，相信你已经意识到，虽然并发原语看上去是很底层、很神秘的东西，但实现起来也并不像想象中的那么困难，尤其是在 Rust 下，在[第 33 讲](https://time.geekbang.org/column/article/442216)中，我们用了几十行代码就实现了一个简单的 SpinLock。

你也许会觉得不太过瘾，而且 SpinLock 也不是经常使用的并发原语，那么今天，我们试着实现一个使用非常广泛的 MPSC channel 如何？

之前我们谈论了如何在搜索引擎的 Index writer 上使用 MPSC channel：要更新 index 的上下文有很多（可以是线程也可以是异步任务），而 IndexWriter 只能是唯一的。为了避免在访问 IndexWriter 时加锁，我们可以使用 MPSC channel，在多个上下文中给 channel 发消息，然后在唯一拥有 IndexWriter 的线程中读取这些消息，非常高效。

好，来看看今天要实现的 MPSC channel 的基本功能。为了简便起见，我们只关心 unbounded MPSC channel。也就是说，当队列容量不够时，会自动扩容，所以，**任何时候生产者写入数据都不会被阻塞，但是当队列中没有数据时，消费者会被阻塞**：  
![](https://static001.geekbang.org/resource/image/cf/a2/cfb839fc9c21f9ec51930c063f0ffda2.jpg?wh=2364x1355)

## 测试驱动的设计

之前我们会从需求的角度来设计接口和数据结构，今天我们就换种方式，完全站在使用者的角度，用使用实例（测试）来驱动接口和数据结构的设计。
<div><strong>精选留言（18）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/29/ce/ed/3dbe915b.jpg" width="30px"><span>乌龙猹</span> 👍（11） 💬（1）<div>这清晰的逻辑，完美诠释TDD  提前预定老师未来推出的 elixir 课程 </div>2021-11-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/26/27/eba94899.jpg" width="30px"><span>罗杰</span> 👍（5） 💬（2）<div>老师在一遍遍的重复 TDD，然后我把 TDD 用在了现在的 Go 项目中，效果非常好，虽然开发的时间增长了，但是代码质量显著提高了。</div>2021-11-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/25/02/22/19585900.jpg" width="30px"><span>彭亚伦</span> 👍（1） 💬（1）<div>一边追这最新的课程更新, 一边反复温习前面的课程; 
之前追《westworld》都没这么过瘾过~</div>2021-11-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/0f/1f/e894ae27.jpg" width="30px"><span>Colt</span> 👍（0） 💬（1）<div>最喜欢老师的实践课,也许rust的知识学得还一知半解,但是跟着老师的思路敲代码感觉非常爽,很多时候一个顺便就完成了需求</div>2021-12-05</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/69/c8/d6f00a46.jpg" width="30px"><span>wowotuo</span> 👍（0） 💬（1）<div>也特别期待把异步tokio、元编程讲透</div>2021-11-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/69/c8/d6f00a46.jpg" width="30px"><span>wowotuo</span> 👍（0） 💬（1）<div>这个实操项目非常有意义，让我对这块有了一个体系性、深入的认知，值得多读多看。</div>2021-11-24</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/vHujib2CCrUYNBaia32eIwTyJoAcl27vASZ9KGjSdnH1dJhD7CrSUicBib19Tf8nDibWaHjzIsvIfdqcXX6vGrH8bicw/132" width="30px"><span>罗同学</span> 👍（0） 💬（2）<div>我想请问一下，实现这个主要是为了理解channel 原理，这个案例可以用于实际生产不？还是说标准库里的性能会更好一点</div>2021-11-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1e/96/38/4a73704d.jpg" width="30px"><span>Enoch Tang</span> 👍（1） 💬（0）<div>目前Sender 的Drop实现有bug，考虑以下场景：
Receiver thread:
1. 加锁
2. 判断 sender 是否为0；
3. 使用CondVar wait

假设在 Receiver thread 执行完2之后切换到 其他线程执行 drop s 的操作，其他线程notify_all，此时 Receiver thread还没有进入到wait的状态，那么后面Receiver thread进入到wait状态后再也不会被唤醒了</div>2023-11-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/f8/ba/d28174a9.jpg" width="30px"><span>Geek_zbvt62</span> 👍（1） 💬（2）<div>Drop for Sender&lt;T&gt;的实现中，notify_all没有在Mutex的保护下进行。这是否会导致一种可能性：
1. receiver发现sender不为0，准备进入wait
2. sender被drop，减一，为0，执行notify_all
3. receiver执行wait，释放锁，阻塞住
此时已经没有sender能唤醒receiver

？？？</div>2022-11-02</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/18/be/aa622bf8.jpg" width="30px"><span>爱学习的小迪</span> 👍（1） 💬（0）<div>看老师的课程真的是可以学习到很多东西啊，不止Rust。太爽了</div>2022-04-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/29/78/ce/c1f1ac55.jpg" width="30px"><span>吃藕吧割吾爱</span> 👍（1） 💬（1）<div>receiver_should_be_blocked_when_nothing_to_read()测试中主线程退出后，Sender全部被析构，thread1中的迭代器就返回None了，那不是就会运行到assert!(false)这句话了吗？</div>2022-04-02</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/82/54/b9cd3674.jpg" width="30px"><span>小可爱(`へ´*)ノ</span> 👍（0） 💬（0）<div>老师的课太强了，能学到很多深入的东西</div>2022-11-16</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/27/fb/f7/88ab6f83.jpg" width="30px"><span>进击的Lancelot</span> 👍（0） 💬（0）<div>思考题：对于 bounded_channel  的测试如下：
```rust
&#47;&#47; 需求6: 当 channel 满了的时候，sender 发送会被阻塞
    #[test]
    fn sender_should_block_when_channel_is_full() {
        let ( s, mut r) = bounded(3);
        let mut s1 = s.clone();
        let cnt = Arc::new(AtomicUsize::new(0));
        let cnt_1 = Arc::clone(&amp;cnt);
        thread::spawn(move || {
            for i in 0..10 {
                s1.send(i).unwrap();
                cnt_1.fetch_add(1, Ordering::AcqRel);
            }
            unreachable!();
        });

        &#47;&#47; 1ms 足以让 sender 发送完 3 个消息
        thread::sleep(Duration::from_millis(1));
        assert_eq!(3, cnt.load(Ordering::SeqCst));
        for i in 0..2 {
            assert_eq!(i, r.recv().unwrap());
        }
        &#47;&#47; 1ms 足以让 sender 再发送完 2 个消息
        thread::sleep(Duration::from_millis(1));
        assert_eq!(5, cnt.load(Ordering::SeqCst));
        assert_eq!(2, r.recv().unwrap());

        thread::sleep(Duration::from_millis(1));
        assert_eq!(s.total_queued_items(), 3);
    }
```
确定好了测试用例之后，就可以开始思考实现方式。主要就是给 shared 增加一个 capacity 的原子变量，在 send 时候减一，recv 的时候加一，并且在 send 时候，如果 capacity 为 0，则需要 block 住 send 所在的线程。由于 bounded_channel 底层容器有容量上限，使用 cache 会导致一些问题，比如：明明装满了 channel 读一次后，却又能继续往里面 send 数据，容易让用户感到困惑，因此取消了 cache 的优化。 
具体完整代码可以参考：https:&#47;&#47;play.rust-lang.org&#47;?version=stable&amp;mode=debug&amp;edition=2021&amp;gist=facca5a34f7bd1d103a482da3a6c8d5e</div>2022-09-30</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/a2/4b/b72f724f.jpg" width="30px"><span>zxk</span> 👍（0） 💬（1）<div>老师，receiver_shall_be_notified_when_all_senders_exit 应该只是大概率能测出问题吧？
```

#[test]
fn receiver_shall_be_notified_when_all_senders_exit() {
    let (s, mut r) = unbounded::&lt;usize&gt;();
    &#47;&#47; 用于两个线程同步
    let (mut sender, mut receiver) = unbounded::&lt;usize&gt;();
    let t1 = thread::spawn(move || {
        &#47;&#47; 保证 r.recv() 先于 t2 的 drop 执行
        sender.send(0).unwrap();
        assert!(r.recv().is_err());
    });

    thread::spawn(move || {
        receiver.recv().unwrap();
        drop(s);
    });

    t1.join().unwrap();
}
```
t1 的 sender.send(0).unwrap() 会唤醒 t2 中的 receiver.recv().unwrap()，这时候 t2 中的 drop(s) 是有可能在 t1 中的 assert!(r.recv().is_err()) 之前执行，导致无法测出问题，虽然概率非常小。</div>2022-07-07</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/VLB1WPGVDnicKaMGUcFZdtDQOXSib3LhFv6YqCZA16qfy2KHUAGL0ichSEE6rSu8HXSibGdg8vzIQ7qWlk9BZOeJjQ/132" width="30px"><span>Curricane</span> 👍（0） 💬（2）<div>实际项目中，会有网络请求，数据库，或者与其他组件交互，这个时候，怎么进行 TDD 呢</div>2022-06-15</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1a/ac/57/db7cc2a1.jpg" width="30px"><span>学不完不改名</span> 👍（0） 💬（0）<div>和jon的channel视频思路很像。。。</div>2022-03-14</li><br/><li><img src="" width="30px"><span>Geek_83f92d</span> 👍（0） 💬（1）<div>请问老师 这两句的顺序是不是反了？
sender.send(0).unwrap(); 
assert!(r.recv().is_err());</div>2022-02-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/45/31/53910b61.jpg" width="30px"><span>A 凡</span> 👍（0） 💬（0）<div>老师讲的确实非常好，还在跟着学习中，不过感觉需要不断复习一下前面的知识，能有更清晰的认识</div>2022-01-24</li><br/>
</ul>