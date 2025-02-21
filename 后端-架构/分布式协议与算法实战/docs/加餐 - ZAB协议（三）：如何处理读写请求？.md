你好，我是韩健！

你应该有这样的体会，如果你想了解一个网络服务，执行的第一个功能肯定是写操作，然后才执行读操作。比如，你要了解ZooKeeper，那么肯定会在zkCli.sh命令行中执行写操作（比如“create /geekbang 123”）写入数据，然后再是读操作（比如“get /geekbang”）查询数据。这样一来，你才会直观地理解ZooKeeper是如何使用的了。

在我看来，任何网络服务最重要的功能就是处理读写请求，因为我们访问网络服务本质上都是在执行读写操作，ZooKeeper也不例外。**而且对ZooKeeper而言，这些功能更为重要，因为在ZooKeeper中，如何处理写请求，关乎着操作的顺序性，而操作的顺序性会影响节点的创建；如何处理读请求，关乎着一致性，它们又影响着客户端是否会读到旧数据。**

接下来，我会从ZooKeeper系统的角度，全面地分析整个读写请求的流程，帮助你更加全面、透彻地理解读写请求背后的原理。

你肯定知道，在ZooKeeper中，写请求是必须在领导者上处理，如果跟随者接收到了写请求，它需要将写请求转发给领导者，当写请求对应的提案被复制到大多数节点上时，领导者会提交提案，并通知跟随者提交提案。而读请求可以在任何节点上处理，也就是说，ZooKeeper实现的是最终一致性。
<div><strong>精选留言（17）</strong></div><ul>
<li><img src="" width="30px"><span>zyz</span> 👍（11） 💬（5）<div>Zookeeper通过Leader来主导写操作，保证了顺序一致性。当一半以上的节点返回已写入，就返回客户端已写入，但是这时候只是部分节点写入，有的节点可能还没有同步上数据，所以读取备份节点可能不是最新的。同时Zookeeper的单一视图特征，保证客户端看到的数据不会比在之前服务器上所看到的更老。</div>2020-05-21</li><br/><li><img src="" width="30px"><span>zyz</span> 👍（6） 💬（1）<div>老师！Zookeeper版本3.5.0开始支持dynamic configuration，成员变更的时候，不需要重启了吧</div>2020-05-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/83/14/099742ae.jpg" width="30px"><span>xzy</span> 👍（2） 💬（2）<div>你好，既然 zk 只能保证最终一致性，那么在分布式系统中，如 kafka、hbase 等，用 zk 做元数据管理岂不是有问题</div>2020-05-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/20/08/bc06bc69.jpg" width="30px"><span>Dovelol</span> 👍（1） 💬（1）<div>老师好，想问下zab协议处理写请求要这么多步骤，那还能保证性能吗？如果其中某一小步骤延迟或阻塞都会影响写的性能把。</div>2020-06-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/de/8a/8b4d7dbd.jpg" width="30px"><span>DY-杨</span> 👍（1） 💬（1）<div>老师，咨询下。paxos算法从您讲解下来好像仅是对某个提案达成共识。没有看到故障恢复或日志恢复的过程啊。反倒zab和raft有。那您知道用这种共识算法的软件是自研的日志恢复吗?另外联合共识算法是什么呢。</div>2020-05-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1c/48/c6/3c8d9a0c.jpg" width="30px"><span>爱德华</span> 👍（0） 💬（2）<div>老师，在说处理写请求的时候好像有点问题。本文中所说的是leader要在第二阶段（commit）后才会返回给客户端成功。但是在前几讲中，好像是说zab在第一阶段，收到大多数响应后就返回给客户端成功。那么这两个说法哪个正确呢？</div>2020-07-07</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/03/1c/c9fe6738.jpg" width="30px"><span>Kvicii.Y</span> 👍（0） 💬（1）<div>领导者CommitProcessor.tryToCommit() 提交提案的方法似乎在3.6.0在Leader类中</div>2020-07-02</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/8e/b8/31671fba.jpg" width="30px"><span>王伟建</span> 👍（4） 💬（3）<div>老师有几个问题不太理解：
1.zk的写请求是领导者节点的两阶段提交，说写请求是强一致性，是说这个两阶段过程未完成之前不允许其他操作，所以说他是强一致性吗？
2.zk的读只能提供顺序一致性，也就是说他可能读到旧的版本的数据，那为什么还要把zk归为CP类型的系统呢？CAP里的C 不应该是强一致性吗，说到底感觉还是对这个一致性没理解透，就之前的理解来说，我认为C是指每次读取的数据都是最近一次写入的数据，而不是过期的数据。希望老师能讲解一下这块儿。
3.利用zk来实现分布式锁，多个服务同时去拿锁时，如果zk提供的读不是强一致性，那么会不会读到旧的锁信息？这块儿是怎么保证每个服务拿到的都是最新的数据，实现上来说是靠sync读吗？</div>2020-12-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/8b/83/d2afc837.jpg" width="30px"><span>路人</span> 👍（2） 💬（1）<div>写我看用的是2pc，2pc中有些如果只有部分commit成功，zookeeper会怎么处理呢？是有什么补偿机制么？</div>2020-09-03</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/63/85/1dc41622.jpg" width="30px"><span>姑射仙人</span> 👍（1） 💬（3）<div>老师，那么Zookeeper是CP呢，还是AP呢？读是最终一致，那么我理解是AP。但之前读的一篇文章，说Zookeeper不适合作为注册中心，说Zookeeper是CP，AP更适合作为注册中心，因为是读多写少，不要求马上能看到新的实例更新。 至于同步机制，Zookeeper也是支持增量更新，这样看来完全没有问题。麻烦老师指点下。</div>2021-03-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/e5/fe/51d688a3.jpg" width="30px"><span>何柱国</span> 👍（0） 💬（0）<div>在我看来，ZAB 的成员发现，可以和领导者选举合到一起，类似 Raft，在领导者选举结束后，直接建立领导者关系，而不是再引入一个新的阶段；数据同步阶段，是一个冗余的设计，可以去除的，因为 ZAB 不是必须要先实现数据副本的一致性，才可以处理写请求，而且这个设计是没有额外的意义和价值的。

-- 我觉得还是有意义的，因为ZK的Follower节点是可以用于查询的，经过数据同步尽可能保持于Leader数据一致，减少了不一致的可能，当然了也可以强制先sync先</div>2023-12-05</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/23/5b/983408b9.jpg" width="30px"><span>悟空聊架构</span> 👍（0） 💬（0）<div>课后题：我提到 ZooKeeper 提供的是最终一致性，读操作可以在任何节点上执行。那么如果读操作访问的是备份节点，为什么无法保证每次都能读到最新的数据呢？

回答：因为主节点发送 commit 消息给所有备份节点时，备份节点执行 commit 的时机不一定都是同步完成的，只有当 commit 之后，客户端读取的数据才是最新的，比如备份节点 B 先commit，客户端 1 连接的是 备份节点 B，那么客户端 1 肯定读到的是最新的，但是如果客户端连接的是备份节点 C，但是节点 C     还没有收到 commit 消息或者收到了，还没来得及 commit，客户端就发起请求了，这个时候读到的就是旧数据。但是过了短暂时间后，所有备份节点都 commit 了，这个时候任何客户端都可以读到最新的一致性数据了，这个就是最终一致性。
补充：这里 commit 操作就是将数据 放到 znode 内存数据结构上，这样客户端就可以读到最新的数据了。</div>2022-03-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/83/22/c3dae274.jpg" width="30px"><span>阿kai(aeo</span> 👍（0） 💬（0）<div>为什么觉得代码顺序是反的呢？比如下面这段FinalRequestProcessor怎么是首先创建的呢?

RequestProcessor finalProcessor = new FinalRequestProcessor(this);            &#47;&#47; 创建finalProcessor，最终提交提案和响应查询
  &#47;&#47; 创建toBeAppliedProcessor，存储可提交的提案，并在提交提案后，从toBeApplied队列移除已提交的
  RequestProcessor toBeAppliedProcessor = new Leader.ToBeAppliedRequestProcessor(finalProcessor, getLeader());
  &#47;&#47; 创建commitProcessor，处理提案提交或读请求      
  commitProcessor = new CommitProcessor(toBeAppliedProcessor, Long.toString(getServerId()), false, getZooKeeperServerListener());
  commitProcessor.start();
  &#47;&#47; 创建proposalProcessor，按照顺序广播提案给跟随者
  ProposalRequestProcessor proposalProcessor = new ProposalRequestProcessor(this, commitProcessor);
  proposalProcessor.initialize();
  &#47;&#47; 创建prepRequestProcessor，根据请求创建提案      
  prepRequestProcessor = new PrepRequestProcessor(this, proposalProcessor);
  prepRequestProcessor.start();
  &#47;&#47; 创建firstProcessor，接收发给领导者的请求
  firstProcessor = new LeaderRequestProcessor(this, prepRequestProcessor);
</div>2022-01-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/03/cd/264f6a1c.jpg" width="30px"><span>渔夫</span> 👍（0） 💬（0）<div>韩老师，想问下分布式集群模式下，FollowerZooKeeperServer.setupRequestProcessors方法是如何被调用的呢，找了好久找不到。不像standolone模式那么好找</div>2021-02-16</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTKUcSLVV6ia3dibe7qvTu8Vic1PVs2EibxoUdx930MC7j2Q9A6s4eibMDZlcicMFY0D0icd3RrDorMChu0zw/132" width="30px"><span>Tesla</span> 👍（0） 💬（1）<div>老师，请问zk的最终一致性是以提升读的效率为目标的嘛，写的速率和强一致性的算法差不多吧？</div>2021-01-04</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/19/d9/ff/b23018a6.jpg" width="30px"><span>Heaven</span> 👍（0） 💬（0）<div>虽然领导者向着大部分的跟随者节点发送了commit请求,但是并不会等待跟随者响应完成写入再返回客户端,而是直接发送了一个完成消息给接收到客户端请求的节点,这就导致,客户端去读取的时候,可能读取到的节点是没有数据生效的节点,所以没法保证每次都读到最新的数据</div>2020-08-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/03/1c/c9fe6738.jpg" width="30px"><span>Kvicii.Y</span> 👍（0） 💬（0）<div>Raft的强一致性是体现在读写都由领导者完成；ZAB的最终一致性是读写可以由领导者也可由Follower或Observer转发完成，如果ZAB想要实现强一致性，似乎也是可以通过sync API完成的吧</div>2020-08-15</li><br/>
</ul>