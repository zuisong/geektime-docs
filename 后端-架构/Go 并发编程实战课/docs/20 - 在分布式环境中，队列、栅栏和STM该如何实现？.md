你好，我是鸟窝。

上一讲，我已经带你认识了基于etcd实现的Leader选举、互斥锁和读写锁，今天，我们来学习下基于etcd的分布式队列、栅栏和STM。

只要你学过计算机算法和数据结构相关的知识， 队列这种数据结构你一定不陌生，它是一种先进先出的类型，有出队（dequeue）和入队（enqueue）两种操作。在[第12讲](https://time.geekbang.org/column/article/304127)中，我专门讲到了一种叫做lock-free的队列。队列在单机的应用程序中常常使用，但是在分布式环境中，多节点如何并发地执行入队和出队的操作呢？这一讲，我会带你认识一下基于etcd实现的分布式队列。

除此之外，我还会讲用分布式栅栏编排一组分布式节点同时执行的方法，以及简化多个key的操作并且提供事务功能的STM（Software Transactional Memory，软件事务内存）。

# 分布式队列和优先级队列

前一讲我也讲到，我们并不是从零开始实现一个分布式队列，而是站在etcd的肩膀上，利用etcd提供的功能实现分布式队列。

etcd集群的可用性由etcd集群的维护者来保证，我们不用担心网络分区、节点宕机等问题。我们可以把这些通通交给etcd的运维人员，把我们自己的关注点放在使用上。

下面，我们就来了解下etcd提供的分布式队列。etcd通过github.com/coreos/etcd/contrib/recipes包提供了分布式队列这种数据结构。
<div><strong>精选留言（11）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/10/ff/a4/55520286.jpg" width="30px"><span>answer宫</span> 👍（6） 💬（1）<div>打卡,坚持看完了,慢慢吸收!</div>2021-03-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/2a/b9/2bf8cc89.jpg" width="30px"><span>无名氏</span> 👍（1） 💬（1）<div>想请教下老师这个STM事务能达到什么隔离级别？</div>2022-03-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1b/2c/3d/0bd58aa4.jpg" width="30px"><span>Em</span> 👍（0） 💬（1）<div>etcd 这么猛吗，一个 k-v 有这么多并发原语，不是一个单纯的 kv 啊</div>2023-12-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/7f/75/551c5d6c.jpg" width="30px"><span>CrazyCodes</span> 👍（0） 💬（1）<div>打卡第一遍</div>2023-11-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/18/93/38/71615300.jpg" width="30px"><span>DayDayUp</span> 👍（0） 💬（1）<div>在地铁上打卡，感动一下自己😂</div>2022-06-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/80/de/c6191045.jpg" width="30px"><span>gitxuzan</span> 👍（0） 💬（1）<div>刷了第三遍了，每次都有不一样的收获</div>2021-10-26</li><br/><li><img src="" width="30px"><span>myrfy</span> 👍（4） 💬（0）<div>感觉是包装了一层最基础的乐观锁，离分布式事务应该还差不少吧</div>2020-11-25</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/a4/16/6463e374.jpg" width="30px"><span>jack</span> 👍（1） 💬（0）<div>终于看完了，感觉还得再看几遍 消化消化。</div>2021-04-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/87/5f/6bf8b74a.jpg" width="30px"><span>Kepler</span> 👍（1） 💬（0）<div>算分布式事务吧，毕竟操作的数据可能来自不同etcd 节点</div>2020-12-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/23/c5/b5/25179772.jpg" width="30px"><span>Jamey</span> 👍（0） 💬（0）<div>报了这节课真是收获满满，虽然只有20几节，但是节节干货，感觉自己对并发的认知又提高了。</div>2021-10-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/17/6e/76b4aa3d.jpg" width="30px"><span>橙子888</span> 👍（0） 💬（0）<div>打卡。</div>2020-11-26</li><br/>
</ul>