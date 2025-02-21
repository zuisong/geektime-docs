你好，我是蔡元楠。

今天我要与你分享的主题是CAP定理。

在分布式系统的两讲中，我们一起学习到了两个重要的概念：可用性和一致性。

而今天，我想和你讲解一个与这两个概念相关，并且在设计分布式系统架构时都会讨论到的一个定理——**CAP定理**（CAP Theorem）。

## CAP定理

CAP这个概念最初是由埃里克·布鲁尔博士（Dr. Eric Brewer）在2000年的ACM年度学术研讨会上提出的。

如果你对这次演讲感兴趣的话，可以翻阅他那次名为“[Towards Robust Distributed Systems](https://people.eecs.berkeley.edu/~brewer/cs262b-2004/PODC-keynote.pdf)”的演讲deck。

在两年之后，塞思·吉尔伯特（Seth Gilbert）和麻省理工学院的南希·林奇教授（Nancy Ann Lynch）在他们的论文“Brewer’s conjecture and the Feasibility of Consistent, Available, Partition-Tolerant Web Services”中证明了这一概念。

![](https://static001.geekbang.org/resource/image/2b/8f/2bfd96a97ce8d38834105964d0cb0e8f.png?wh=1278%2A1346)

他们在这篇论文中证明了：在任意的分布式系统中，一致性（Consistency），可用性（Availability）和分区容错性（Partition-tolerance）这三种属性最多只能同时存在两个属性。
<div><strong>精选留言（30）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/11/56/cf/53f64618.jpg" width="30px"><span>王燊 شن ون</span> 👍（14） 💬（3）<div>我的理解：A是机器挂掉仍可用，P是网络挂掉仍可用。如果我的理解正确，那老师您说Kafka不支持P的解释，即当Kafka leader挂掉整个系统不可用，其实是不是表明Kafka是不支持A，而不是不支持P的？</div>2019-05-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/5f/e9/95ef44f3.jpg" width="30px"><span>常超</span> 👍（27） 💬（1）<div>关于大家出现很多疑问的Kafka是否有P属性的问题，上网搜了一下，找到一个可以说明Kafka不具备P属性的例子，不知道理解对不对，请老师和大家批评指正。

比如：在以下的场景序列下，会出现数据写入丢失的情况，所以不能说kafka是有P属性

前提：leader和两个slave 1、2
序列：
1.机器leader跟两个slave之间发生partion
这是leader成为唯一服务节点，继续接受写入请求w1,但是w1只保存在了leader机器上，无法复制到slave1和2
2.leader和zookeeper之间发生partition，导致kafka选取slave 1为新leader，新leader接受新写入w1
这时候，上面1的w1写入丢失了。即使之后旧leader复活，w1的写入数据也不会被恢复出来。
参考：https:&#47;&#47;bit.ly&#47;2VGKtu1
</div>2019-05-06</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/67/8a/babd74dc.jpg" width="30px"><span>锦</span> 👍（2） 💬（2）<div>AP，发微博保证最终一致性就可以。
疑问一，mongodb采用CP，那么它在可用性方面有做什么事情吗？
疑问二，kafka这种通过选举leader的方式不就是分区容错性吗？为什么说放弃了P呢？</div>2019-05-06</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/5f/e9/95ef44f3.jpg" width="30px"><span>常超</span> 👍（14） 💬（3）<div>老师您好，文中说kafka放弃了P属性。
但是从后面的解释来看，即使出现分区（领导者节点和副本1无法通讯），整个系统也能正常工作，这种行为难道不是保持了P属性吗。您能否举一个P属性被放弃的例子？</div>2019-05-06</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTLhMtBwGqqmyhxp5uaDTvvp18iaalQj8qHv6u8rv1FQXGozfl3alPvdPHpEsTWwFPFVOoP6EeKT4bw/132" width="30px"><span>Codelife</span> 👍（19） 💬（2）<div>严格来说,CAP理论是针对分区副本来定义的，之所以说kafka放弃P，只支持CA，是因为，kafka原理中当出现单个broke宕机，将要出现分区的时候，直接将该broke从集群中剔除，确保整个集群不会出现P现象</div>2019-05-06</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/26/1b/4caf36bd.jpg" width="30px"><span>coldpark</span> 👍（8） 💬（1）<div>有一个形象的比喻不知道恰当不恰当，一个系统相当于一个团队，有C属性说明这个团队每次都能保质保量完成任务，A属性说明这个团队每次都能及时完成任务，P属性相当于这个团队内部偶尔会犯一些小错误。犯错是很常见的，所以一般都具有P属性。
CP类型的团队对外的形象相当于：我的团队不是完美的，但我的产品绝对不会出问题，只要你给我足够的时间让我们把问题排查清楚。
AP类型的团队给人的感觉就是：人非圣贤，孰能无过，我的队员会犯错，我的团队也有估计不足的时候，但是客户的需求我们总会最快响应。
CA类型的团队有个强人领袖（leader节点）：任何事务无论大小都过问一遍，一旦发现手下有人犯错，立马剔除出团队，如果自己犯错，让出领袖地位，整个团队一定要保证最快最好完成任务。</div>2019-08-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/87/25/898dea4e.jpg" width="30px"><span>桃园悠然在</span> 👍（3） 💬（1）<div>另外，增加一个评论：蔡老师的文章头图每张都跟内容强相关（不知是否自己P图或者照相的），而且右上角有文章序号很用心，点赞！</div>2019-05-06</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/a3/06/9fa93074.jpg" width="30px"><span>王聪 Claire</span> 👍（3） 💬（1）<div>kafka 的replication机制，即使出现分区这样的错误，系统也能够通过领导者节点返回消息。怎么算放弃了P呢？谢谢。</div>2019-05-06</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/4f/a5/71358d7b.jpg" width="30px"><span>J.M.Liu</span> 👍（2） 💬（1）<div>老师，我好像懂了。kafka replication不保证p，指的是当网络出现分区后，和主有一台副本比如replicatin1和leader失联了，那replication1就会被踢出去，相当它于宕机了。在这里，分区导致replication1不可用了，所以说不保证p。
是这样理解吗？</div>2019-05-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/ef/67/bb9d9358.jpg" width="30px"><span>LaimanYeung</span> 👍（2） 💬（2）<div>A：集群某个或某几节点挂掉时，客户端仍然可以访问服务端.
C：客户访问集群中任一服务端，返回的状态都是一致的.
P：集群内部机器通讯出现问题导致服务A的数据无法同步到其他节点时，客户端访问服务A，服务A扔能返回未同步到其他节点的数据.</div>2019-05-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/4f/a5/71358d7b.jpg" width="30px"><span>J.M.Liu</span> 👍（2） 💬（1）<div>不太理解ca系统，允许有机子挂掉，却不允许网络分区。机子都挂掉了，到这台机子的网络可不就是连不通了吗？ 允许机子化掉却不允许机子和集群失联，这是个悖论呀。怎么理解这个呢老师</div>2019-05-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/87/25/898dea4e.jpg" width="30px"><span>桃园悠然在</span> 👍（2） 💬（1）<div>我理解kafka作为一个消息系统平台，是不允许消息丢失的，所以通过replication机制冗余数据保证。但是P属性更像是一个缺点（容忍了消息丢失），它的好处该怎么理解呢？谢谢老师！</div>2019-05-06</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/53/d4/2ed767ea.jpg" width="30px"><span>wmg</span> 👍（2） 💬（1）<div>老师，如果kafka支持必须同步节点写成功，那是不是就是一个cp系统，如果支持非健康节点选举为leader，是不是就是ap系统？</div>2019-05-06</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/dc/c3/e4ba51d5.jpg" width="30px"><span>Flash</span> 👍（1） 💬（1）<div>谢谢老师，是不了解微博的机制，请问老师，发微博应该要用什么CAP属性？
看到留言有人说，发微博保证最终一致性就好，不知道这个跟CAP的线性一致性是不是一个意思？
</div>2019-05-15</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/41/27/3ff1a1d6.jpg" width="30px"><span>hua168</span> 👍（1） 💬（1）<div>Availability和Partition Tolerance并不是由是否允许数据丢失来判断的。

我来举个例子说明吧。假设现在有一个由两个节点组成的集群，这两个节点都可以独立运作也可以与对方通讯，而客户端是与这个集群通讯的。作为一个集群来说，Availability指的是不管这两个节点哪一个节点坏掉不能运作了，对于客户端来说还是可以继续与这个集群进行通讯的。Partition Tolerance指得是，本来这两个节点可能是需要互相通讯来同步数据的，而因为Network Partition使得它们之间不能通讯了，但是对于客户端来说还是可以继续与这个集群进行通讯的。

按照您这样说，我疑惑的是：
1. 节点是所有节点，包括主节点吧？
2. 两个节点之间，如果有数据分别写入的话，那不就是数据不一致吗？
  如果node1写入A数据，node2被写入B数据，怎同步？那数据不是乱套了？读也出现不一的情况
比如是金钱类的，不能是负数，我请求node1花完了，我刷新一下又访问到node2发现还是原来，我又花完了，那我不是可以花双倍？一同步那不是出错？同步不了，因为扣双倍，已小于0

3. 如果是CA的话，P出问题，不是出现不一致吗，那么我怎么保证C？</div>2019-05-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/ee/16/742956ac.jpg" width="30px"><span>涵</span> 👍（1） 💬（1）<div>老师好，通过您对kafka replication的讲解，以及同学们分析的其他系统，感觉一个分布式平台在设计时需要选择保障CP或AP，被拿掉的A或C也不是完全不考虑，会通过一些其他的辅助系统来支持保障，所以对于平台来说绝大多数时间是可以做到CAP的。不知道这样理解是否正确?</div>2019-05-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/f4/32/c4550f66.jpg" width="30px"><span>刘万里</span> 👍（1） 💬（1）<div>老师，您有apache beam相关的书推荐吗？谢谢</div>2019-05-07</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/9chAb6SjxFiapSeicsAsGqzziaNlhX9d5aEt8Z0gUNsZJ9dICaDHqAypGvjv4Bx3PryHnj7OFnOXFOp7Ik21CVXEA/132" width="30px"><span>挖矿的小戈</span> 👍（1） 💬（1）<div>1. kafka作为CA系统的理解：
      kafka的设计是只需要保证单个数据中心的broker之间能够数据复制就好，出现网络分区的情况比较少，因此他主攻高可用和强一致性
2.  文中，老师提到kafka的Leader选举是由Zookeeper选举的，这儿有点不严谨
     原因：kafka会由Zookeeper选举一台broker作为controller，之后由controller来维护partition的leader、flower，而leader宕机之后进行新leader的选举也是由controller负责的
3. 微博发微博的功能，满足AP就行，C的话只需要是最终一致性就好，就跟微信朋友圈一样</div>2019-05-06</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/9chAb6SjxFiapSeicsAsGqzziaNlhX9d5aEt8Z0gUNsZJ9dICaDHqAypGvjv4Bx3PryHnj7OFnOXFOp7Ik21CVXEA/132" width="30px"><span>挖矿的小戈</span> 👍（1） 💬（1）<div>1. kafka作为CA系统的理解：
      kafka的设计是只需要保证单个数据中心的broker之间能够数据复制就好，出现网络分区的情况比较少，因此他主攻高可用和强一致性
2.  文中，老师提到kafka的Leader选举是由Zookeeper选举的，这儿有点不严谨
     原因：kafka会由Zookeeper选举一台broker作为controller，之后由controller来维护partition的leader、flower，而leader宕机之后进行新leader的选举也是由controller负责的
3. 微博发微博的功能，满足AP就行，C的话只需要是最终一致性就好，就跟微信朋友圈一样</div>2019-05-06</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/80/1e/784e50c9.jpg" width="30px"><span>coder</span> 👍（1） 💬（1）<div>Kafka集群leader维护了一个in-sync replica (ISR) set，表示一个和leader保持同步的follower集合，如果follower长时间未向leader同步数据，时间超过一个设置的参数，则该follower就会被踢出ISR，而后该follower回重启自己并向leader同步数据，通过这种方法避免长时间不能同步数据的问题</div>2019-05-06</li><br/><li><img src="" width="30px"><span>kris37</span> 👍（1） 💬（1）<div>kafka之所以说是ca系统，是因为他跟本就不保证p，因为发生了p kafka 的被独立的分区部分无法保证c 也无法保证a</div>2019-05-06</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/60/95/0b2a67fa.jpg" width="30px"><span>Geek_f80wzm</span> 👍（1） 💬（1）<div>redis是ap 吧，redis集群挂一台，key会rehash，保证可用。redis做分不式锁，主节点挂了，假如主还没来得及同步数据，数据丢了，锁会被申请多次。保证你能申请，这是可用性，不限制你申请多次，这是没有一致性。</div>2019-05-06</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/lUOVNGBvDTqss5XExibXsOrx1mAM7raMhQbdEHdkAeIEGLoK2wJXjy1QiaDKZlQ9vLjTyZcia39KVmrpzJB8zRhqA/132" width="30px"><span>Geek_1987v5</span> 👍（1） 💬（1）<div>CP</div>2019-05-06</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/c2/1f/343f2dec.jpg" width="30px"><span>9527</span> 👍（1） 💬（1）<div>老师好，我有几个问题不明白
1.文中提到的一致性是线性一致的，这个是相当于强一致性吗

2.Cassandra是AP的，HBase是CP的，很多项目都将HBase替代了Cassandra，是因为运维水平上来了，可以用运维来弥补HBase中高可用的不足吗，而Cassandra被很多项目弃用是因为它不是最终一致性的，导致在一段时间窗口内会出现数据不一致，这样理解对吗？

3.HBase的Master可以起多个作为备份避免单点问题，那不是应该是CA吗，为什么是CP呢？

4.MySql集群应该是属于CA还是CP呢？</div>2019-05-06</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/4e/29/1be3dd40.jpg" width="30px"><span>ykkk88</span> 👍（1） 💬（1）<div>kafka replication和放弃p有什么关系么</div>2019-05-06</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/dc/c3/e4ba51d5.jpg" width="30px"><span>Flash</span> 👍（0） 💬（1）<div>看完本篇文章，我也不知道微博是用什么CAP中的哪两个属性啊，更别说去思考重新设计怎么做呢？？</div>2019-05-15</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/2b/fa/1cde88d4.jpg" width="30px"><span>大俊stan</span> 👍（0） 💬（1）<div>老师您好 能否把kaffka的ca类比为zookeeper作为注册中心时也缺少p，还有就是zookeeper在进行大量节点重新选取时是缺少a的</div>2019-05-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/1b/4a/f9df2d06.jpg" width="30px"><span>蒙开强</span> 👍（0） 💬（1）<div>老师，你好，我看到在留言区里你回答提问者时，说了kafka选择了ca，这个是在官网的那个地方可以查看这个说明呢</div>2019-05-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/41/27/3ff1a1d6.jpg" width="30px"><span>hua168</span> 👍（0） 💬（1）<div>老师，我想问一下A与P是怎区别的，是不是从是否允许数据丢失上判断？
A所有节点间发数据是没有丢失的
P节点间数据是允许丢失的，
如果这样的话，那么主节点和节点间数据不是产生不一致的情况吗，又怎么保证C，一致性？</div>2019-05-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/f5/80/baddf03b.jpg" width="30px"><span>zhihai.tu</span> 👍（0） 💬（1）<div>AP吧，C只要保持最终一致性就可以了。用户发送微博，写和读之间可以容忍一定的延迟。</div>2019-05-09</li><br/>
</ul>