你好，我是大明。今天我们来探讨一下Redis 高性能的原因。

这个问题在面试中还是很常见的，原因也很简单，除了 Redis 你基本上没有听过其他采用单线程模型的中间件，所以这就凸显了 Redis 的与众不同。

而且这个问题也很有现实意义。大部分时候对 Redis 的一些高级应用，比如前面提到的利用 Redis 实现一个分布式锁，其中有一个很重要的假设就是 Redis 是线程安全的，没有并发问题。而 Redis 是单线程的这一点就保证了线程安全的特性。

那么今天我就带你来看一下，Redis 的高性能究竟是怎样做到的。

## Redis 是单线程的含义

你在学习 Redis 的时候，肯定听过一句话，Redis 是单线程的。而实际上，Redis 并不是单线程的。业界说 Redis 是单线程的，是指它在处理命令的时候，是单线程的。在 Redis 6.0 之前，Redis 的 IO 也是单线程的，但是在 6.0 之后也改成了多线程。

但是其他部分，比如说持久化、数据同步之类的功能，都是由别的线程来完成的。因此严格来说，Redis 其实是多线程的。

## 面试准备

这一部分的面试内容基本上都是纯理论的，所以你需要做几件事情。

- 了解你使用的其他中间件，在 IO 上是否使用了 epoll，以及是否使用了 Reactor 模式。
- 了解你们公司有没有使用 Redis 的多线程，如果用了，那么弄清楚最开始的决策理由以及相比单线程性能究竟提升了多少。
- 了解清楚你使用的 Redis 的性能瓶颈。
<div><strong>精选留言（5）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/10/d0/91/89123507.jpg" width="30px"><span>Johar</span> 👍（6） 💬（1）<div>我在 Memcache 里面吐槽说为什么它用多线程而 Redis 用单线程，可能就是设计者的偏好问题，你是如何看待这个问题的？
redis虽然是单线程，但也只是网络io+内存操作是单线程，其他涉及文件io，数据同步等耗时操作都是多线程。当然涉及耗时读写操作，redis会造成阻塞。另外缓存本来就是读多写少的操作。从上述两点个人倾向于多线程模型。
你认为在 Redis 遇到性能瓶颈的时候，是应该优先考虑使用多线程模式还是应该考虑 Redis Cluster 增加新节点来解决？
大部分的情况新增节点提升高，除非是单个热key或crc相同的热key，在不改动代码的情况下，新增节点无用，需要开启多线程</div>2023-09-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/25/87/f3a69d1b.jpg" width="30px"><span>peter</span> 👍（1） 💬（2）<div>请教老师几个问题：
Q1：线程可以绑定到CPU的某个核上吗？
Q2：Redis在windows下的IO模型也是epoll+Reactor吗？
文中有“另外一方面，在 Linux 系统上 Redis 采用了 epoll 和 Reactor 结合的 IO 模型”，那么，Redis在windows下也是这样的IO模型吗？
Q3：普通的文件描述符也叫“套接字”吗？
我把“套接字”理解成socket了，用于网络通信的了。文中说的“套接字”好像范围很广，即包括socket，也包括其他类型的文件描述符了。
Q4：Redis用的epoll是借用Linux的epoll吗？
Epoll_create是一个系统调用，从这里看，应该是借用Linux本身的epoll特性。
Q5：Memcache是内存数据库吗？
Q6：Redis多线程模式下，主线程收到请求后，哪个IO线程来处理是怎么决定的？随机选一个吗？还是事先绑定好了？</div>2023-09-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1f/77/7b/338c4617.jpg" width="30px"><span>瀚海</span> 👍（0） 💬（1）<div>有个疑问      多线程模式下，redis还能保证命令按照到来的顺序执行吗？       本节中讲到，多线程时io线程负责解析命令交给主线程执行，那io线程解析命令后交给主线程的顺序就是不可预测的，是不是就不能保证命令按时序执行了？</div>2024-04-30</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/3c/fa/e2990931.jpg" width="30px"><span>文敦复</span> 👍（3） 💬（0）<div>牛逼。。。</div>2023-09-26</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/PiajxSqBRaEJKV0danxJVszB0s83BXaQfc8KhuUjzE9jUey7yzxq3csZNic549uZu2tZOLfORyTZBsc7pRVnzVTI2J7dd9HWofJBxkibgBLdVbMJBQ6wOo6uA/132" width="30px"><span>Geek_004fe2</span> 👍（1） 💬（0）<div>第一个的设计差异就是大明哥常言的编经性质的问题哈哈哈，我感觉就是多线程带来的使用收益和开发维护成本在 redis 作者看来不成正比，所以一开始就用单线程的开发模型来开发 redis 了，后期引入的多线程也没触及到核心的 redis 的命令执行模块，还是聚焦在外围的 IO 多线程，开发维护成本还是可控的。
第二个问题，可以看看机子的 cpu 使用情况，如果某个核心的使用率拉满了，可以先开多线程模式来测试一下性能问题有没有得到缓解，如果还是不行的话就只能上集群解决了</div>2024-07-22</li><br/>
</ul>