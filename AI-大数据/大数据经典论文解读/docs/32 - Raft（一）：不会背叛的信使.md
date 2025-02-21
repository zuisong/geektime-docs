你好，我是徐文浩。

在前面课程中，我们了解过的这些大数据处理系统，其实都属于分布式系统。所以，它们也都需要解决分布式一致性，或者说分布式共识的问题。

我们之前已经介绍过Chubby，这个Google开发的分布式锁。正是通过Chubby这样的系统，使得我们可以确保系统里始终只有一个Master，以及所有的数据分区在一个时间点只有一个所有者。而Chubby的底层，就是**Paxos**这样的分布式共识（Distributed Consensus）算法。另外在后面的Spanner这样的分布式数据库里，我们也看到了Paxos也可以直接拿来作为分布式数据库的解决方案。

在之前的这些论文里，我们对Paxos的算法做了一些简单的介绍。不过，我们并没有对Paxos的算法做非常深入地剖析。一方面，Paxos算法其实并不容易理解，这也是为什么Paxos的论文第一次发表的时候，并没有得到足够的关注。另一方面，目前市场上实际的开源项目，大部分也并不是采用了Paxos或者Multi-Paxos算法，而是往往采取了简化和变形。Google的Chubby并没有开源，而开源的ZooKeeper实现的是自家的ZAB算法，对Paxos做了改造。
<div><strong>精选留言（5）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/10/47/00/3202bdf0.jpg" width="30px"><span>piboye</span> 👍（2） 💬（1）<div>老师，为什么follower不直接告诉leader我已提交的位置，而是要leader一个一个的去回朔，是基于什么考虑？</div>2022-01-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/04/30/7f2cb8e3.jpg" width="30px"><span>CRT</span> 👍（0） 💬（0）<div>再问老师一个问题哈，在选举的时候，能够选举有最新日志leader的前提是有过半数拥有最新日志的follower，那如果因为网络原因，没有过半数最新日志的follower呢？</div>2022-01-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/04/30/7f2cb8e3.jpg" width="30px"><span>CRT</span> 👍（0） 💬（0）<div>关于思考题目，可以利用时间的随机性，各自等待一个随机的时间再选举，时间戳最大为master，失败的话，继续等待随机时间再选举。</div>2022-01-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/66/8f/02be926d.jpg" width="30px"><span>在路上</span> 👍（0） 💬（0）<div>徐老师好，我认为启动时的选举涉及两个问题，第一、什么时候发起投票，第二、如何才能被选中。对于第一点，集群启动是需要一段时间的，每台机器启动完成的时间不同，本身符合随机性，所以可以在启动后立即发起投票，对于第二点，还是需要本地已提交的日志是最新的，并获得大多数的Follower同意。如果选举失败，则随机等待一段时间，进入下一个选举循环。</div>2021-12-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/25/7f/473d5a77.jpg" width="30px"><span>曾轼麟</span> 👍（0） 💬（0）<div>我理解刚启动的时候有点类似于抢占模式，每个刚启动的服务都会发起一次选举请求，最先获得半数的实例会宣布为master

我这边有一个疑问，redis的raft实现好像又是另一种变种，通过一群哨兵去基于raft选举redis master，而哨兵本身是不能成为master，不知道这种方式下能否满足raft的状态机复制的安全性呢？</div>2021-12-24</li><br/>
</ul>