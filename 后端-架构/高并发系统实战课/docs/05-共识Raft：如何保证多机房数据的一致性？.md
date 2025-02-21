你好，我是徐长龙。

[上节课](https://time.geekbang.org/column/article/598570)我们讲了如何通过Otter实现同城双活机房的数据库同步，但是**这种方式并不能保证双机房数据双主的事务强一致性**。

如果机房A对某一条数据做了更改，B机房同时修改，Otter会用合并逻辑对冲突的数据行或字段做合并。为了避免类似问题，我们在上节课对客户端做了要求：用户客户端在一段时间内只能访问一个机房。

但如果业务对“事务+强一致”的要求极高，比如库存不允许超卖，那我们通常只有两种选择：一种是将服务做成本地服务，但这个方式并不适合所有业务；另一种是采用多机房，但需要用分布式强一致算法保证多个副本的一致性。

在行业里，最知名的分布式强一致算法要属Paxos，但它的原理过于抽象，在使用过程中经过多次修改会和原设计产生很大偏离，这让很多人不确定自己的修改是不是合理的。而且，很多人需要一到两年的实践经验才能彻底掌握这个算法。

随着我们对分布式多副本同步的需求增多，过于笼统的Paxos已经不能满足市场需要，于是，Raft算法诞生了。

相比Paxos，Raft不仅更容易理解，还能保证数据操作的顺序，因此在分布式数据服务中被广泛使用，像etcd、Kafka这些知名的基础组件都是用Raft算法实现的。
<div><strong>精选留言（21）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/13/71/05/db554eba.jpg" width="30px"><span>👽</span> 👍（4） 💬（4）<div>文中的这一段，如何保证数据一致性的解释：
“这里有个小技巧，就是 Follower 在收到查询请求时，会顺便问一下 Leader 当前最新 commit 的 log index 是什么。”

这里是不是意味着每次对从节点的查询，一定会伴随对主节点的查询？这么来看的话，性能岂不是会很差？不单单是要求修改量小，查询量多了主节点是否也容易承受不住？

另外一个问题是，我们有一个大佬说，现在的分布式一致性都是扯的，我们追求的只能是最终一致性。这样说有道理吗？我们是否还应该追求分布式数据的强一致性？
</div>2022-12-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/2c/6b/6c/3e80afaf.jpg" width="30px"><span>HappyHasson</span> 👍（3） 💬（1）<div>有两个问题，
一，这里没有主观下线和客观下线的区分吗，就是当一个follower检测到leader下线，但是不一定真的下线了，而且网络抖动引起的 

二，我看到的理论都是说投票过半数就选举成功了，这里说是三分之二，为什么</div>2022-11-04</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/80/82/3c21b30c.jpg" width="30px"><span>梅子黄时雨</span> 👍（2） 💬（1）<div>搜索了下，主要是存在脑裂的问题，就是在增减集群成员后，到底有哪些成员，新老节点看到的结果会不一样，从而到导致leader选举出错。</div>2023-01-04</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/94/fe/5fbf1bdc.jpg" width="30px"><span>Layne</span> 👍（2） 💬（3）<div>老师，主从之间通信不上的时候，怎么确定是主还是从出问题了呢？这种情况下主从分别会做些啥操作呀？</div>2022-11-30</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTLFTXb42lNxJQAZOmDicxP5iaOsUTkj1vtH9P53Mo0u7jlvUwrpJ54noOGPEEgLozZCbuIavB99bJtw/132" width="30px"><span>Geek_499240</span> 👍（2） 💬（3）<div>如果leader收到了一个请求，并把日志同步到了大部分的follower上，如果leader 还没来得及commit就奔溃了，那么新选举出来的leader会commit这条消息吗？</div>2022-11-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/2c/6b/6c/3e80afaf.jpg" width="30px"><span>HappyHasson</span> 👍（2） 💬（3）<div>收到投票申请的服务，并且申请服务（即“发送投票申请的服务”）的任期和同步进度都比它超前或相同，那么它就会投申请服务一票 

原文中这句话意思是，如果一个follower收到了自荐投票请求，任期比自己大但是同步进度没有自己大，这时候会拒绝投票？</div>2022-11-04</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1f/ae/7b/47200692.jpg" width="30px"><span>贺子</span> 👍（1） 💬（1）<div>这里有个小技巧，就是 Follower 在收到查询请求时，会顺便问一下 Leader 当前最新 commit 的 log index 是什么。如果这个 log index 大于当前 Follower 同步的进度，就说明 Follower 的本地数据不是最新的，这时候 Follower 就会从 Leader 获取最新的数据返回给客户端。可见，保证数据强一致性的代价很大。这里和后面的感觉矛盾呀！到底raft是什么机制呀，后面说wait index！tidb就是支持indx read，类似</div>2023-07-31</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/57/4f/6fb51ff1.jpg" width="30px"><span>奕</span> 👍（1） 💬（3）<div>如果集群中的 Follower 节点在指定时间内没有收到 Leader 的心跳
----------
这里是不是有数量的限制，比如说至少一半的 Follow 节点？</div>2022-11-15</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1a/9d/81/d748b7eb.jpg" width="30px"><span>千锤百炼领悟之极限</span> 👍（1） 💬（1）<div>可以说了解了 Raft，就相当于了解了分布式强一致性数据服务的半壁江山。另一半是ZAB吗？</div>2022-11-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/29/44/3c/8bb9e8b4.jpg" width="30px"><span>Mr.Tree</span> 👍（1） 💬（0）<div>对于Raft保证数据读取的强一致性，follower的读取都会向leader发送一个版本确认请求，如果是高并发的情况下，leader的压力岂不是会很大，会不会把它打崩，或者客户端出现延迟，对于这种主从结构系统；出现写冲突是如何处理呢？想到一个场景：张三人在国外，银行账户里存有1w，通过手机银行APP转帐给李四8k，于此同时，张三媳妇在国内通过ATM机查询账户1w，想要取5k，这种同时发生，对于这种强一致性要求系统会怎么处理？</div>2022-11-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/d6/e8/50b58ed8.jpg" width="30px"><span>OAuth</span> 👍（1） 💬（1）<div>单节点变更，一次变更一个节点</div>2022-11-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/0c/86/8e52afb8.jpg" width="30px"><span>花花大脸猫</span> 👍（1） 💬（1）<div>思考题中增加节点因为需要同步的数据量会比较大，所以 特殊去做，以防影响集群对外提供的服务稳定性。减少节点需要特殊处理是不是怕由于脑裂导致的选举异常，直接导致服务对外不可用，不知道这么理解对不对？</div>2022-11-06</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1e/d1/ab/6e925b26.jpg" width="30px"><span>boydenyol</span> 👍（1） 💬（1）<div>你好，老师！请问，文中提到 “在选举期间，若有服务收到上一任 Leader 的心跳，则会拒绝” ，这代表所有的Follower都会拒绝吗？ 如果上一任Leader仅仅是因为网络阻塞导致心跳异常，同时在选举Leader完成之前正常了，是否还能再做Leader，毕竟Leader的数据是最新的，还是必须得选举其它Leader？</div>2022-11-05</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/25/87/f3a69d1b.jpg" width="30px"><span>peter</span> 👍（1） 💬（1）<div>请问：cmd:a&lt;7，这里的 a &lt; -7是什么意思？</div>2022-11-02</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/YbUxEV3741vKZAiasOXggWucQbmicJwIjg3HDE58oyibYXbSop9QQFqZ7X6OhynDoo6rDHwzK8njSeJjN9hx3pJXg/132" width="30px"><span>黄堃健</span> 👍（0） 💬（1）<div>老师，你好！如果所有服务都没有获取到多数票（三分之二以上服务节点的投票）  ， 不是过半以上就可以了吗？   如果是9个副本服务，5个副本服务达成一致就可以了，不用6个服务达成一致
                         </div>2024-03-04</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/36/ae/95/4a0b0e97.jpg" width="30px"><span>微笑的胡圆圆</span> 👍（0） 💬（1）<div>可以推荐有时间或者有精力的可以完成6.824中的raft实现 https:&#47;&#47;pdos.csail.mit.edu&#47;6.824&#47;labs&#47;lab-raft.html</div>2024-01-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/31/7b/be/791d0f5e.jpg" width="30px"><span>Geek_595be5</span> 👍（0） 💬（1）<div>我之前看到的是kafka用的是zookeeper，zookeeper是基于zab协议的，而且zab协议早于raft</div>2023-12-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1f/ae/7b/47200692.jpg" width="30px"><span>贺子</span> 👍（0） 💬（1）<div>你可能会好奇：如何在业务使用时保证读取数据的强一致性呢？其实我们之前说的 Raft 同步等待 Leader commit log index 的机制，已经确保了这一点。我们只需要向 Leader 正常提交数据修改的操作，Follower 读取时拿到的就一定是最新的数据。
这里的描述和前面的描述不矛盾吗？</div>2023-07-31</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/DYAIOgq83eoWfXendN7czHpsyaWKLPK6Na9P5czquJ7Wdre4TibZQ5SQib88edyuib3LpCVFkp0gII2wyvvR8tEIA/132" width="30px"><span>OM</span> 👍（0） 💬（1）<div>老师，现在国产数据库如市面上的oceanbase数据库采用的是paxos实现分布式，说工业标准，不太明白paxos标准区分。</div>2023-07-11</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/DYAIOgq83epqMYnEEVK1D6Veh3VvPjHAb1sZg8AHtWkSUJIEEMFF2hVm9LN1fuqdXaiczyctaib6XicjhyvH8ymug/132" width="30px"><span>宋毅</span> 👍（0） 💬（1）<div>q:为什么 Raft 集群成员增减需要特殊去做？
a: 会触发选举，触发选举的逻辑是，当前集群存在leader了那么增加节点就没关系，但是减少的时候如果刚好干掉了ledaer，就会触发选举导致服务不可用，且如果是刚好仅存2个节点，还会触发选举等待（因为都不是大多数）。</div>2023-02-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/c6/20/124ae6d4.jpg" width="30px"><span>若水清菡</span> 👍（0） 💬（1）<div>为什么 Raft 集群成员增减需要特殊去做？
主要还是为了避免集群脑裂现象，如果是三节点的集群，剩余选举的节点必须超过半数，也就是只能宕机一台，这也是集群节点数量必须是奇数的原因。Raft 集群成员增减都需要考虑集群节点数量，避免出现存活节点数量不超过集群节点数量一半的情况。
</div>2023-01-11</li><br/>
</ul>