你好，我是Mike。从今天开始，我们会用几节课的时间系统学习Rust异步并发编程。

和其他语言不大一样的是，异步 Rust（async Rust）相当于Rust世界里的一块儿新的王国，这个王国有一定的独立性，有它突出的特点。当然，独立并不代表封闭，我们前面所有的知识和经验仍然能顺利地在这个王国里发挥作用。

## async rust

从Rust v1.39版本以后，Rust引入了async关键字，用于支持异步编程的工程学体验，使程序员可以用已经习惯了的同步代码书写方式来编写异步代码。

如果你了解过早期的JavaScript语言，你可能会对回调模式以及“回调地狱”有所了解。感兴趣的话，你可以搜索“回调地狱”这个关键词，看看它是如何产生的，以及可以用什么方式去解决。

JavaScript在ECMAScript 2017版本中引入了 `async/await` 关键字组合，用于改进JavaScript中异步编程体验，从此以后程序员可以用顺序的逻辑书写方式来写出异步执行的代码，而不是那种用回调方式把一段连续的逻辑切割成一小块一小块的。

Rust其实也差不多，它用类似的方式引入了 `async/.await` 关键字对。如果你对Mozilla公司有所了解的话，就不会感觉奇怪了，Mozilla是互联网标准组织的重要成员，JavaScript之父就在Mozilla公司，参与了JavaScript标准制定的全过程。同时，Mozilla还推出了Rust语言以及WebAssembly字节码规范。
<div><strong>精选留言（16）</strong></div><ul>
<li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/VF71Gcf2C2bjYPFCRv0TPfwhkJmT5WhtusltuaXQM0KMDibdallNFypqWV6v2FJ4bqNwzujiaF5LEDeia7JMZTTtw/132" width="30px"><span>Geek_e72251</span> 👍（6） 💬（5）<div>异步函数必须要.await得到返回结果才能够接着往下执行吗？那和同步函数有什么区别</div>2023-11-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/35/fa/25/e40eeb9c.jpg" width="30px"><span>三过rust门而不入</span> 👍（2） 💬（1）<div>https:&#47;&#47;zhuanlan.zhihu.com&#47;p&#47;667313965#:~:text=Rust%20%E5%88%9D%E6%AD%A5%E4%BA%86%E8%A7%A3Rust%E5%BC%82%E6%AD%A5%E5%B9%B6%E5%8F%91%E7%BC%96%E7%A8%8B%201%20async%20rust%20%E4%BB%8E%20Rust%20v1.39,%E5%87%BD%E6%95%B0%E5%89%8D%E5%B0%B1%E5%8F%AF%E4%BB%A5%E5%8A%A0%20async%20%E4%BF%AE%E9%A5%B0%E4%BA%86%E3%80%82%20...%207%20%E4%BB%A3%E7%A0%81%E7%A4%BA%E4%BE%8B%20...%20%E6%9B%B4%E5%A4%9A%E9%A1%B9%E7%9B%AE
被转载了唐老师，很多文章都转了</div>2024-01-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/0f/70/cdef7a3d.jpg" width="30px"><span>Joe Black</span> 👍（2） 💬（1）<div>如果启动了多个异步任务，不想挨着顺序await（因为有可能后面启动的提前结束），有没有办法实现等待一批任务并且其中一个任务完成就返回处理呢？处理后再去等待其它未完成的任务。</div>2023-12-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/ed/1a/269eb3d6.jpg" width="30px"><span>cfanbo</span> 👍（2） 💬（1）<div>也就是说，在一个 task 没有遇到 .await 之前，它是不会主动交出这个 CPU 核的，其他 task 也不能主动来抢占这个 CPU 核。所以 tokio 实现的这个模型叫做合作式的。和它相对的，Go 语言自带的 Runtime 实现的 Goroutine 是一种抢占式的轻量级线程。
---
这样如果一个task长期被执行，同一个cpu 上的其它 task将长期得不到执行，有失公平性的吗？go的抢占印象中就是解决这个不公平的问题</div>2023-11-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1b/96/47/93838ff7.jpg" width="30px"><span>青鸟飞鱼</span> 👍（1） 💬（1）<div>如果我写一个死循环，会不会有问题</div>2024-04-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/39/ab/ca/32d6c05d.jpg" width="30px"><span>哄哄</span> 👍（1） 💬（2）<div>rust的命名其他都挺好，就是有时候难以一眼分清引入的是struct还是trait。他们都是首字母大写驼峰命名，而且，程序用到什么trait就需要引用什么trait，不像python里引用类就行了。</div>2023-11-17</li><br/><li><img src="" width="30px"><span>Geek_3b58b9</span> 👍（0） 💬（1）<div>嵌入式系统中好像是用Embassy这个运行时的，既然运行时是依赖底层操作系统的，那嵌入式上用的这个运行时是基于什么的啊？</div>2024-01-12</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/7Q403U68Oy4lXG5sFBPVKLrfwaRzBqpBZibpEBXcPf9UOO3qrnh7RELoByTLzBZLkN9Nukfsj7DibynbZjKAKgag/132" width="30px"><span>superggn</span> 👍（0） 💬（1）<div>笔记：

async runtime &#47; 异步运行时

- async fn &#47; async block 必须用 await 才能跑
- await 必须写在 async block &#47; async fn 里
- main 不能是 async 的 =&gt; main 里头不能有 await =&gt; 那 main 里写啥来驱动 async fn &#47; async block?
- 这时就需要一个 async runtime &#47; 异步运行时
- 简单来说就是一个可以写在 main 里的 await
</div>2023-12-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/39/ab/ca/32d6c05d.jpg" width="30px"><span>哄哄</span> 👍（0） 💬（1）<div>请问，tokio::task::spawn和tokio::spawn的区别</div>2023-12-02</li><br/><li><img src="" width="30px"><span>Geek_72807e</span> 👍（0） 💬（2）<div>请问老师，如果crateA为crateB1.1版本实现了一个trait，而我的项目中依赖了crateB1.0版本，那么这个trait会失效吗？还有，我奇怪的是如果一个struct的trait分散在各个crate中，怎么能让这些trait都生效呢……</div>2023-11-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/38/a0/06/f0ca94ca.jpg" width="30px"><span>Apa琦</span> 👍（0） 💬（1）<div>tokio是完全使用操作系统的api实现的异步，那rust底层就没有提供异步的方法么。</div>2023-11-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/82/42/8b04d489.jpg" width="30px"><span>刘丹</span> 👍（0） 💬（1）<div>请问老师，如果异步函数返回的是 Result，那么就必须在 .await 后面继续调用 .unwrap() ？在实际项目里，有没有不使用 unwrap() 的写法吗？</div>2023-11-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/18/75/bc/89d88775.jpg" width="30px"><span>Calvin</span> 👍（1） 💬（0）<div>老师，是 JoinHandle 而不是 JoinHandler!</div>2024-04-12</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/DYAIOgq83ep66fdwo3ebSicKjf0iacAx4C2tZOthDDD4bSJqib1iauFBK6EoMSWUBp4UbbN2BQlib7mFR3hQD6MUwew/132" width="30px"><span>chai</span> 👍（0） 💬（0）<div>&quot;独立王国“是相对于rust同步机制来说的，在异步机制中，对其对应的同步机制，都重新实现了一遍，例如文件io、网络io等</div>2024-12-02</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/5b/69/7ace1ddb.jpg" width="30px"><span>独钓寒江</span> 👍（0） 💬（0）<div>比如示例里，我们就把这个新的任务命名为 task_a，它的类型是 JoinHandler。在用 spawn() 创建 task_a 后，这个新任务就立即执行。--&gt; 不是应该碰到await才执行吗？</div>2024-06-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/b8/bf/39151455.jpg" width="30px"><span>Aioria</span> 👍（0） 💬（0）<div>老师，这门课程中没有介绍线程方面的内容，是不是在实际开发中用异步编程就行了，除非特殊场景否则根本不需要用到线程相关操作呢？类似go语言中，只要使用协程就可以了。</div>2024-05-10</li><br/>
</ul>