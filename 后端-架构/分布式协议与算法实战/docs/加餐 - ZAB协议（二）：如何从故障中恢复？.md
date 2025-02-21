你好，我是韩健。

我们上一讲提到了ZAB的领导者选举，在我看来，它只是选举了一个适合当领导者的节点，然后把这个节点的状态设置成LEADING状态。此时，这个节点还不能作为主节点处理写请求，也不能使用领导职能（比如，它没办法阻止其他“领导者”广播提案）。也就是说，集群还没有从故障中恢复过来，而成员发现和数据同步会解决这个问题。

总的来说，成员发现和数据同步不仅让新领导者正式成为领导者，确立了它的领导关系，还解决了各副本的数据冲突，实现了数据副本的一致性。这样一来，集群就能正常处理写请求了。在这句话里：

- 确立领导关系，也就是在成员发现（DISCOVERY）阶段，领导者和大多数跟随者建立连接，并再次确认各节点对自己当选领导者没有异议，确立自己的领导关系；
- 处理冲突数据，也就是在数据同步（SYNCHRONIZATION）阶段，领导者以自己的数据为准，解决各节点数据副本的不一致。

对你来说，理解这两点，可以更好地理解ZooKeeper怎么恢复故障，以及当主节点崩溃了，哪些数据会丢失，哪些不会，以及背后的原因。也就是说，你能更加深刻地理解ZooKeeper的节点故障容错能力。

那么说了这么多，集群具体是怎么从故障中恢复过来的呢？带着这个问题，我们进入今天的学习。
<div><strong>精选留言（12）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/1d/92/9c/1312b3ca.jpg" width="30px"><span>小波菜</span> 👍（21） 💬（2）<div>“如果写请求对应的提案“SET X = 1”未被复制到大多数节点上，比如在领导者广播消息过程中，领导者崩溃了，那么，提案“SET X = 1”，可能被复制到大多数节点上，并提交和之后就不再改变，也可能会被删除。这个行为是未确定的，取决于新的领导者是否包含该提案。”
请教韩老师：
这边set x=1只复制到少数节点上，那么这些少数节点的zxid应该是最大，应该回成为新的leader，也就不会丢数据了啊？
然后这个问题又该如何避免呢？</div>2020-05-21</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/YicovLZyvibpkfJwuAib1FEyibVDN6Oia1Wsg7jibT0uTj0UDH75KAX6vfSvstjy1IHTW7WpNbMlZZO9SnGoPj3AE2DQ/132" width="30px"><span>要努力的兵长</span> 👍（8） 💬（1）<div>如果写请求对应的提案“SET X = 1”未被复制到大多数节点上，比如在领导者广播消息过程中，领导者崩溃了，那么，提案“SET X = 1”，可能被复制到大多数节点上，并提交和之后就不再改变，也可能会被删除。这个行为是未确定的，取决于新的领导者是否包含该提案  ----------像这种 提案的 事务ID明显是最大的吧。 那选举新leader 的时候， 也不可能选举出 没有接受的该提案的那种节点吧 (任期相同的情况下，选举  事务ID最大的   作为领导者)</div>2020-09-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/42/ab/75fb1cd6.jpg" width="30px"><span>Tim</span> 👍（8） 💬（5）<div>有个问题请教下韩老师，在做故障恢复数据同步时候，如果 minCommittedLog &lt; peerLastZxid &lt; maxCommittedLog, 比如leader 是 【5，6，7，8，9】，而follower是【5，7】，follower中间少了一个zxid 6的事务，这时候数据同步会恢复嘛？谢谢老师解答。</div>2020-05-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/19/d9/ff/b23018a6.jpg" width="30px"><span>Heaven</span> 👍（5） 💬（2）<div>少数节点为何我XID最大我不能成为领导者呢?</div>2020-08-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/03/1c/c9fe6738.jpg" width="30px"><span>Kvicii.Y</span> 👍（4） 💬（1）<div>感觉成员发现应该算是选举过后的一个选举补偿，而数据同步则是数据补偿</div>2020-07-01</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/d8/63/e4c28138.jpg" width="30px"><span>春风</span> 👍（2） 💬（1）<div>当接收到领导者的响应后，跟随者会判断领导者的任期编号是否最新，如果不是，就发起新的选举；

老师，什么情况下领导者的任期编号会不是最新呢？这个时候发起新的选举，其他节点的状态是不是应该是following状态，zab状态应该是discovery状态，这个时候是怎么响应选举的呢？</div>2020-07-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/4d/54/9c214885.jpg" width="30px"><span>kylexy_0817</span> 👍（1） 💬（1）<div>韩老师好，“只有当集群大多数节点处于广播状态的时候，集群才能提交提案”，是否意味着BROADCAST广播状态，是会与其它三个状态同时存在的呢？</div>2020-09-05</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/18/b3/15/30822e33.jpg" width="30px"><span>小麦</span> 👍（2） 💬（1）<div>【在 ZooKeeper 中，被复制到大多数节点上的提案，最终会被提交】

如果一个提案已经被复制到大多数节点上了，但是在 Leader 向节点发送 commit 之前崩溃了，那么 follower 是没有收到 commit 请求的，那这个提案最终也会被提交吗？为什么？</div>2022-01-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/26/be/e9/9d597e04.jpg" width="30px"><span>豆豆酱</span> 👍（0） 💬（0）<div>我一直以为zk的读是顺序一致性，然后今天读到这个commit的特性。
zk这个commit 的特性（退出跟随者时commit），会不会影响顺序一致性？如果这个时候commit的提案被读了，后面又被删了？那这样就是最终一致性了。所以到底是什么？</div>2023-05-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1c/96/dd/1620a744.jpg" width="30px"><span>simple_孙</span> 👍（0） 💬（1）<div>ZAB必须有数据同步的操作是不是因为Raft在提交数据的时候，跟随者会检查上一条数据是否提交成功，没成功的话就会重新同步；而ZAB的数据同步就是一个二阶段提交，没法检查上一个位置的同步结果。</div>2021-11-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/ba/ea/eb6ec134.jpg" width="30px"><span>我可能是个假开发</span> 👍（0） 💬（0）<div>应该怎么样理解大多数当选领导呢？
即是LOOKING状态的节点会在一段时间内（多久呢）收集选票？对于epoch相同的情况，按zxid从大到小遍历选票，如果看到某一个zxid的数量满足大多数条件（count(zxid)&gt;(n&#47;2)+1)，则投票该zxid中集群id最大的节点为领导者？</div>2021-06-30</li><br/><li><img src="" width="30px"><span>Geek_672f79</span> 👍（0） 💬（4）<div>韩老师， 你在ZAB协议（1） 有这么一句话：ZAB 的领导者选举，选举出的是大多数节点中数据最完整的节点。
 但在本章有这么一句话 ：如果写请求对应的提案“SET X = 1”未被复制到大多数节点上，比如在领导者广播消息过程中，领导者崩溃了，那么，提案“SET X = 1”，可能被复制到大多数节点上，并提交和之后就不再改变，也可能会被删除。这个行为是未确定的，取决于新的领导者是否包含该提案。

    我该如何去理解？</div>2021-03-21</li><br/>
</ul>