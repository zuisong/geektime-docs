你好，我是唐聪。

在前面的etcd读写流程学习中，我和你多次提到了etcd是基于Raft协议实现高可用、数据强一致性的。

那么etcd是如何基于Raft来实现高可用、数据强一致性的呢？

这节课我们就以上一节中的hello写请求为案例，深入分析etcd在遇到Leader节点crash等异常后，Follower节点如何快速感知到异常，并高效选举出新的Leader，对外提供高可用服务的。

同时，我将通过一个日志复制整体流程图，为你介绍etcd如何保障各节点数据一致性，并介绍Raft算法为了确保数据一致性、完整性，对Leader选举和日志复制所增加的一系列安全规则。希望通过这节课，让你了解etcd在节点故障、网络分区等异常场景下是如何基于Raft算法实现高可用、数据强一致的。

## 如何避免单点故障

在介绍Raft算法之前，我们首先了解下它的诞生背景，Raft解决了分布式系统什么痛点呢？

首先我们回想下，早期我们使用的数据存储服务，它们往往是部署在单节点上的。但是单节点存在单点故障，一宕机就整个服务不可用，对业务影响非常大。

随后，为了解决单点问题，软件系统工程师引入了数据复制技术，实现多副本。通过数据复制方案，一方面我们可以提高服务可用性，避免单点故障。另一方面，多副本可以提升读吞吐量、甚至就近部署在业务所在的地理位置，降低访问延迟。
<div><strong>精选留言（30）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/10/3e/e7/261711a5.jpg" width="30px"><span>blentle</span> 👍（35） 💬（1）<div>老师，如果一个日志完整度相对较高的节点因为自己随机时间比其他节点的长，没能最先发起竞选，其他节点当上leader后同步自己的日志岂不是冲突了？</div>2021-01-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/46/0f/f6cfc659.jpg" width="30px"><span>mckee</span> 👍（29） 💬（1）<div>思考题：
1.哪些场景会出现 Follower 日志与 Leader 冲突？
leader崩溃的情况下可能(如老的leader可能还没有完全复制所有的日志条目)，如果leader和follower出现持续崩溃会加剧这个现象。follower可能会丢失一些在新的leader中有的日志条目，他也可能拥有一些leader没有的日志条目，或者两者都发生。
2.follower如何删除无效日志？
leader处理不一致是通过强制follower直接复制自己的日志来解决了。因此在follower中的冲突的日志条目会被leader的日志覆盖。leader会记录follower的日志复制进度nextIndex，如果follower在追加日志时一致性检查失败，就会拒绝请求，此时leader就会减小 nextIndex 值并进行重试，最终在某个位置让follower跟leader一致。
</div>2021-01-31</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/9d/84/171b2221.jpg" width="30px"><span>jeffery</span> 👍（12） 💬（2）<div>讲的太好了、图文并貌、形象生动、raft这章就够本了！老师问下.es 也用raft！为啥会出现数据不一致性？部署etcd高可用有运维有最佳实践建议吗？谢谢老师</div>2021-01-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/41/38/4f89095b.jpg" width="30px"><span>写点啥呢</span> 👍（11） 💬（6）<div>谢谢老师的回答，关于第三个问题，“3. 如果在写数据过程中leader崩溃了。比如在leader完成自身WAL并发送MsgApp后崩溃了，本次写提案没有完成，重新选leader之后新leader有这次写记录的log，它会怎么恢复数据？” 我详细描述下，请老师帮忙解答下：
1. Leader收到用户put请求后，完成自己的WAL日志及raft日志持久化后发送MsgApp到其它follower节点。
2. 其它follower节点接收到MsgApp后也完成自己的WAL及raft日志操作。
3. 此时Leader节点崩溃了，follower节点无法发送自己日志MsgAppResp给已经崩溃的Leader。此时集群开始新一轮选举并选出一个Leader
4. 新的Leader接收过之前的put提案并在日志中找到它，新的Leader如何恢复这条提案到提交状态？新的leader是不是在日志中看到这条没有完成提案后重新在做一轮提案？

谢谢老师
</div>2021-01-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/41/38/4f89095b.jpg" width="30px"><span>写点啥呢</span> 👍（9） 💬（1）<div>关于选举过程和节点崩溃后恢复有几个问题请教老师：
1. 如果多数follower崩溃后重启恢复（比如极端情况只剩下Leader其它follower同时重启），根据选举规则是不是会出现重启follower占多数投票给了一个数据不是最新的节点而导致数据丢失。我理解这种情况不满足法定票算法前提，所以是无法保障数据一致的。
2. 对于少数节点崩溃恢复后，它是如何追上leader的最新数据的呢？比如对于日志复制过程，leader完成自身的WAL及raft日志然后发送MsgApp，但是其它follower没有来得及发送MsgResp就崩溃了，那么这条raft日志其实没有得到法定票数的提交信息，raft模块应该通过什么方式来让follower恢复这份数据，让它能够最终在恢复的节点得到法定票数提交，然后应用到上层状态机？
3.  如果在写数据过程中leader崩溃了。比如在leader完成自身WAL并发送MsgApp后崩溃了，本次写提案没有完成，重新选leader之后新leader有这次写记录的log，它会怎么恢复数据？

谢谢老师</div>2021-01-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/76/7d/04c95885.jpg" width="30px"><span>Index</span> 👍（4） 💬（2）<div>关于etcd的raft实现源码有个问题
func ExampleNode() {
	c := &amp;Config{}
	n := StartNode(c, nil)
	defer n.Stop()

	&#47;&#47; stuff to n happens in other goroutines

	&#47;&#47; the last known state
	var prev pb.HardState
	for {
		&#47;&#47; Ready blocks until there is new state ready.
		rd := &lt;-n.Ready()
		if !isHardStateEqual(prev, rd.HardState) {
			saveStateToDisk(rd.HardState)
			prev = rd.HardState
		}

		saveToDisk(rd.Entries)
		go applyToStore(rd.CommittedEntries)
		sendMessages(rd.Messages)
	}
}

网络，存储都是用户自己实现的，如果这里在处理存储和发送消息很慢，这样不会影响到心跳吗？比如心跳默认是1s，那如果处理存储和网络的时间经常超过1s，岂不是心跳就时常超时，集群经常处于选举的状态吗？求解答</div>2021-01-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1b/96/47/93838ff7.jpg" width="30px"><span>青鸟飞鱼</span> 👍（4） 💬（5）<div>主从复制缺点是因为主节点崩溃后，没有选主机制（是否可以考虑redis的哨兵选主）呢？还是因为数据一致性呢（raft保持强一致性的话，也是通过某些机制保证强一致性（主节点读或者ReadIndex））</div>2021-01-27</li><br/><li><img src="" width="30px"><span>Geek_aaa517</span> 👍（3） 💬（2）<div>raft日志跟wal日志没太搞明白，分别是什么作用呢</div>2021-03-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/d8/63/e4c28138.jpg" width="30px"><span>春风</span> 👍（3） 💬（1）<div>假如老的 Leader A 因为网络问题无法连通 B、C 节点，这时候根据状态图，我们知道它将不停自增任期号，发起选举。等 A 节点网络异常恢复后，那么现有 Leader 收到了新的任期号，就会触发新一轮 Leader 选举，影响服务的可用性。

老师，这里没太懂，A不是本身是leader吗，为什么还要发起选举？</div>2021-01-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/11/3e/925aa996.jpg" width="30px"><span>HelloBug</span> 👍（2） 💬（2）<div>老师在讲解流程的时候，会说raft模块，kvserver模块，这些都好理解。但又会说etcd发送什么消息，或者etcdserver怎么怎么样，具体是什么模块呢？我之前以为这两者不指哪个模块，就是etcd的框架代码，但是这篇文章里又看到etcdserver模块，着实不知道怎么理解了</div>2021-12-02</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/41/38/4f89095b.jpg" width="30px"><span>写点啥呢</span> 👍（1） 💬（2）<div>请问唐老师，我理解follower上的WAL和稳定raft日志是通过接收leader的MsgApp消息来更新的。那如果leader是在发送MsgApp之后接收MsgResp之前崩溃，选举完成的新集群如何知道一个日志条目已经被多数follower持久化了呢？是不是选举后集群中的新leader和follower是不是根据自己raft模块中的提案日志来确定的？谢谢</div>2021-01-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/19/e9/90/0ad18371.jpg" width="30px"><span>java</span> 👍（0） 💬（1）<div>额 老师 上节课的思考题答案呢.,是xpensive read会导致频繁升级读写锁.导致写请求往后推迟,然后就超时了.吗</div>2021-01-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/4c/83/7788fc66.jpg" width="30px"><span>Simon</span> 👍（0） 💬（2）<div>在日志图 2 中，Follower B 返回给 client 成功后若突然 crash 了，此时可能还并未将 6 号日志条目已提交的消息通知到 Follower A 和 C

老师, 这里的Follower B是不是Leader B啊?</div>2021-01-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1b/97/d3/239aa4d5.jpg" width="30px"><span>科精</span> 👍（79） 💬（1）<div>Raft分布式算法，打开连接玩1分钟就能学会
http:&#47;&#47;kailing.pub&#47;raft&#47;index.html</div>2021-02-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/22/3a/de/e5c30589.jpg" width="30px"><span>云原生工程师</span> 👍（3） 💬（0）<div>日志复制流程图很赞，清晰易懂</div>2021-01-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1b/96/47/93838ff7.jpg" width="30px"><span>青鸟飞鱼</span> 👍（2） 💬（0）<div>老师，为什么最开始会追加到不稳定raft日志中呢？</div>2021-12-15</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/IIkdC2gohpcibib0AJvSdnJQefAuQYGlLySQOticThpF7Ck9WuDUQLJlgZ7ic13LIFnGBXXbMsSP3nZsbibBN98ZjGA/132" width="30px"><span>batman</span> 👍（2） 💬（0）<div>raft log 和 WAL是同一东西吗</div>2021-06-09</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTLDUJyeq54fiaXAgF62tNeocO3lHsKT4mygEcNoZLnibg6ONKicMgCgUHSfgW8hrMUXlwpNSzR8MHZwg/132" width="30px"><span>types</span> 👍（2） 💬（1）<div>选举规则当节点收到选举投票的时候，需检查候选者的最后一条日志中的任期号，若小于自己则拒绝投票。如果任期号相同，日志却比自己短，也拒绝为其投票。

请问“日志比自己短” 是指什么状态下的日志 ，是commited还是？
如果不是commited， B（leader）AppMsg 给A和C后crash， A收到了， C没收到。 这个时候C会不会成为leader，导致数据丢失</div>2021-03-01</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/28/c6/6e/49aff2bd.jpg" width="30px"><span>erge</span> 👍（1） 💬（0）<div>老师好，peer节点是什么呢</div>2022-01-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/e1/da/d7f591a7.jpg" width="30px"><span>励研冰</span> 👍（1） 💬（2）<div>等 A 节点网络异常恢复后，那么现有 Leader 收到了新的任期号，就会触发新一轮 Leader 选举，影响服务的可用性。
上文说到leader选举收到选举票之后会跟自己的现在的任期号对比，且要比自己的数据新，那发起选票之后B跟C收到投票请求任期号可能比自己的要大，但是数据应该没有比B跟C的大吧，所以这时候B告诉A现在自己是leader让A直接成为follower 就行了，为什么会重新选举呢？</div>2021-11-04</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/98/b1/f89a84d0.jpg" width="30px"><span>wu526</span> 👍（1） 💬（0）<div>老师，您好请教一写问题：
1. 如果一个集群有3个节点, 则Leader会维护3组 (NextIndex, MatchIndex)吗?
2. 由于每个节点都可以变为Leader, 是否也意味着Follower也会同步更新这两个变量的值呢?
3. 假设当前任期号是1，此时Leader crash了，进行选举理论上这次任期号是2，但此次选举失败了，再下一次选举成功时会使用任期号3还是任期号2？

</div>2021-02-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/66/34/0508d9e4.jpg" width="30px"><span>u</span> 👍（1） 💬（0）<div>厉害了，不过之前没接触过相关知识，看的有点吃力，找了一篇通俗易懂的补了下基础，为后面的课程做准备，分享一下：https:&#47;&#47;blog.csdn.net&#47;wangxuelei036&#47;article&#47;details&#47;108894053</div>2021-02-16</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/cb/38/4c9cfdf4.jpg" width="30px"><span>谢小路</span> 👍（1） 💬（0）<div>行吧。raft 动画版。http:&#47;&#47;thesecretlivesofdata.com&#47;raft&#47;</div>2021-02-04</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1a/2e/c5/231114ed.jpg" width="30px"><span>Hadesu</span> 👍（0） 💬（0）<div>pipeline 和 stream 模式有什么不同？</div>2025-02-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/0e/ed/1c662e93.jpg" width="30px"><span>莫珣</span> 👍（0） 💬（0）<div>旧的Leader crash的瞬间，Fllower也没收到同步日志的请求，且Leader节点之后也没重新上线，Follower怎么才能将这个新增日志同步过来？而且旧Leader都宕机了，数据也没法传了呀
</div>2024-01-04</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/27/e4/04/18933a58.jpg" width="30px"><span>心如水滴</span> 👍（0） 💬（0）<div>思考题
1. leader节点收到了client的请求写到WAL，但是还没同步给Follower就crash了。
新Leader当选后就会发现旧leader节点存在多余的无法提交的log entry。

2. Follower节点可以同步Leader节点的WAL快照来替换含有无效日志条目的WAL
</div>2023-12-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/31/4f/45/507464b6.jpg" width="30px"><span>warm</span> 👍（0） 💬（0）<div>老师，集群一致性是不是只能保证客户端的查询无论落到哪个节点得到的值都是一样的，但是不能保证有一些较新的数据因为多次频繁换主而导致丢失更新。</div>2023-08-18</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/KjXNw3FNfsJhktyGDNEpQdicnaR0MZCiaQwGg3icQXUGVzqsRHL1FfxO87FX0VNzcl858AUjWPaABmogsWNFa8OGw/132" width="30px"><span>阿基米德</span> 👍（0） 💬（0）<div>如果etcd集群有5个节点，分别是a,b,c,d,e节点，a是leader，a将一条新数据x=5刷盘到wal之后，只给b节点发去了追加日志的消息，然后a宕机了。重新选举，b有可能成为新一任的leader吗？b成为leader之后，它日志文件中的x=5这条数据会被删除还是会同步到其他follower节点，因为这条x=5的数据在上一个leader的任期内是还没有写入到大多数节点的？如果不删除x=5，算不算是脏数据，因为写入这条数据的客户端肯定超时报错了</div>2022-08-05</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/21/5f/f8/1d16434b.jpg" width="30px"><span>陈麒文</span> 👍（0） 💬（0）<div>那个图1和图2各个节点的符号标识是什么意思，比如x&lt;-1,y&lt;-2,money&lt;-10 a&lt;-1</div>2022-08-04</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/26/83/69/fda7d5f5.jpg" width="30px"><span>清茗</span> 👍（0） 💬（0）<div>小白看了四章了，感觉看着很吃力</div>2022-07-20</li><br/>
</ul>