你好，我是徐文浩。

过去的两讲里，我们都在尝试做一件事情，就是在Master和Backup Master之间保持数据的同步复制。无论是通过分布式事务的两阶段提交算法，还是通过分布式共识的Paxos算法，都是为了做到这一点。

而我们要去保障Master和Backup Master之间的同步复制，也是为了一个小小的目标，那就是**整个系统的高可用性**。因为系统中只有一个Master节点，我们希望能够在Master节点挂掉的时候，快速切换到另外一个节点，所以我们需要这两个节点的数据是完全同步的。不然的话，我们就可能会丢失一部分数据。

不过，无论是GFS也好，Bigtable也好，我们能看到它们都是一个单Master系统，而不是有多个Master，能够同时接受外部的请求来保持高可用性。所以，尽管在论文里面，Google没有说GFS在Master和Backup Master之间数据的同步复制是怎么进行的，但是根据我的推测，采用一个两阶段提交的方式会更简单直接一点。

那么，现在你可能就会觉得有问题了：如果还是使用两阶段提交这样的方式，我们不还是会面临单点故障吗？而且，我们上一讲所说的Paxos算法也用不上啊？

要回答这个问题，就请你一起来和我学习今天这一讲，也就是Chubby这个系统到底是怎么一回事儿。通过这一讲，我会让你知道：
<div><strong>精选留言（10）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/1e/a7/1b/ef507d9d.jpg" width="30px"><span>Cc</span> 👍（6） 💬（0）<div>选主的时候没有办法提供服务 应该是牺牲了可用性吧</div>2021-10-22</li><br/><li><img src="" width="30px"><span>Geek_26755e</span> 👍（2） 💬（0）<div>介绍 lock-sequencer 这种方案时作者似乎漏了一种子方案？即在应用侧收到请求时拿着 sequencer 去 consistent cache 中校验一把锁是否还有效，这个子方案相比应用侧只校验 lock generation number 单增适用范围更广（比方说支持多对象的资源锁），缺点是要维护 session（其中含有 cache）。不知道这种子方案在业界是否有实践应用呢？

对应原文：
The recipient server is expected to test whether the sequencer is still valid and has the appropriate mode; if not, it should reject the request. The validity of a sequencer can be checked against the server’s Chubby cache or, if the server does not wish to maintain a session with Chubby, against the most recent sequencer that the server has observed.</div>2023-01-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/4b/cd/185e5378.jpg" width="30px"><span>泊浮目</span> 👍（2） 💬（0）<div>&quot;CAP 之间难以满足是一个伪问题&quot;感觉要引出BASE了啊</div>2021-10-27</li><br/><li><img src="" width="30px"><span>Geek_26755e</span> 👍（1） 💬（0）<div>关于思考题：使用 Chubby 提高了应用层 Master 的可用性并不是解决了可用性问题，实际是 Chubby 向外屏蔽了可用性问题（基于 Paxos 的服务如果挂了多余半数的服务也就不能向外服务了，如果向外提供服务就是牺牲了一致性）。</div>2023-01-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/a2/55/1092ebb8.jpg" width="30px"><span>边城路远</span> 👍（1） 💬（0）<div>master挂掉后，临时文件被释放，这个时候backup master观察到这一事件去创建文件（拿到锁）将自己的ip和port写入，从而实现master模块的高可用</div>2022-04-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/4c/6d/c20f2d5a.jpg" width="30px"><span>LJK</span> 👍（1） 💬（1）<div>老师好，所以通过chubby选master的话只是在master选举上达到共识，解决了谁是master的问题，这个跟big table里面存储的数据本身的一致性有什么关系吗？
我理解对数据的写入和同步机制好像没什么影响，一些replica如果和master之间有同步延迟的话还是会产生数据不一致，不知道这个理解对吗？</div>2022-01-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/22/f4/9fd6f8f0.jpg" width="30px"><span>核桃</span> 👍（0） 💬（0）<div>关于CAP的选择，目前很多系统是追求最终一致性比较多的，牺牲了可用性，例如leader切换的时候，事务的执行是非常容易出现问题的。但是实际上，学术界也有论文讲述了这个问题，在master切换的时候，并不需要停止原来的业务，可以通过repair这些算法来修复，但是难度会很大，这些目前我们也在逐渐实现。</div>2022-02-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/95/52/66c86cf8.jpg" width="30px"><span>clpsz</span> 👍（0） 💬（0）<div>重剑无锋</div>2022-02-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/20/a6/9f/3c60fffd.jpg" width="30px"><span>青阳</span> 👍（0） 💬（1）<div>怎么感觉和redis的哨兵集群有点相似</div>2021-11-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/27/b1/4f/5b67f467.jpg" width="30px"><span>hunt5</span> 👍（0） 💬（1）<div>非常感谢作者的分享 受益匪浅哈
有个问题:
1.Chubby发现master断掉需要选出新的master
2.master失效的广播由于网络分区没有到达客户端A
3.客户端A依旧发数据到挂掉的master进行二阶段提交
4.客户端B发数据到新的master进行二阶段提交
所以是否每次写入都要和Chubby交互来保持一致性呢?</div>2021-11-04</li><br/>
</ul>