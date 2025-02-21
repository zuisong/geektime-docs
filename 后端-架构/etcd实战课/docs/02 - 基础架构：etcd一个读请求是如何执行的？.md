你好，我是唐聪。

在上一讲中，我和你分享了etcd的前世今生，同时也为你重点介绍了etcd v2的不足之处，以及我们现在广泛使用etcd v3的原因。

今天，我想跟你介绍一下etcd v3的基础架构，让你从整体上对etcd有一个初步的了解，心中能构筑起一幅etcd模块全景图。这样，在你遇到诸如“Kubernetes在执行kubectl get pod时，etcd如何获取到最新的数据返回给APIServer？”等流程架构问题时，就能知道各个模块由上至下是如何紧密协作的。

即便是遇到请求报错，你也能通过顶层的模块全景图，推测出请求流程究竟在什么模块出现了问题。

## 基础架构

下面是一张etcd的简要基础架构图，我们先从宏观上了解一下etcd都有哪些功能模块。

![](https://static001.geekbang.org/resource/image/34/84/34486534722d2748d8cd1172bfe63084.png?wh=1920%2A1240)

你可以看到，按照分层模型，etcd可分为Client层、API网络层、Raft算法层、逻辑层和存储层。这些层的功能如下：

- **Client层**：Client层包括client v2和v3两个大版本API客户端库，提供了简洁易用的API，同时支持负载均衡、节点间故障自动转移，可极大降低业务使用etcd复杂度，提升开发效率、服务可用性。
- **API网络层**：API网络层主要包括client访问server和server节点之间的通信协议。一方面，client访问etcd server的API分为v2和v3两个大版本。v2 API使用HTTP/1.x协议，v3 API使用gRPC协议。同时v3通过etcd grpc-gateway组件也支持HTTP/1.x协议，便于各种语言的服务调用。另一方面，server之间通信协议，是指节点间通过Raft算法实现数据复制和Leader选举等功能时使用的HTTP协议。
- **Raft算法层**：Raft算法层实现了Leader选举、日志复制、ReadIndex等核心算法特性，用于保障etcd多个节点间的数据一致性、提升服务可用性等，是etcd的基石和亮点。
- **功能逻辑层**：etcd核心特性实现层，如典型的KVServer模块、MVCC模块、Auth鉴权模块、Lease租约模块、Compactor压缩模块等，其中MVCC模块主要由treeIndex模块和boltdb模块组成。
- **存储层**：存储层包含预写日志(WAL)模块、快照(Snapshot)模块、boltdb模块。其中WAL可保障etcd crash后数据不丢失，boltdb则保存了集群元数据和用户写入的数据。
<div><strong>精选留言（30）</strong></div><ul>
<li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/4S6xTsiauPNbQrEHiayUVNvNXgl1WR4BFwvuJbPbGicSzpbYeKNGicPJ8RiaibAGZEDLcicJRibGQNUqfjs2t90EBPK9Pg/132" width="30px"><span>hiroshi</span> 👍（71） 💬（10）<div>老师，readIndex 需要请求 leader，那为啥不直接让 leader 返回读请求的结果，而要等待自己的进度赶上 leader？</div>2021-02-16</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/18/4c/e12f3b41.jpg" width="30px"><span>姜姜</span> 👍（29） 💬（6）<div>老师，文中有些地方不太明白:
1, KVServer中的拦截器
我认为它只是作为一个辅助的功能吧，用于实现一些观测功能。但对于一个普通的读请求，是否必须通过拦截器才能完成读取数据的操作？

2, 文中“handler 首先会将上面描述的一系列拦截器串联成一个执行”
这段话中，拦截器是一系列的，一系列是指会有多个拦截器吗？难道不是一个请求只注册一个拦截器吗，还能注册多个？为什么要注册多个？
“串联成一个执行”，如何串联成一个？将多个拦截器串联成一个拦截器？

3, 串行读与线性读
这里我理解串行读是“非强一致性读”，线性读是“强一致性读”，对吗？
而且这里的“串行”总让我想到“并行&#47;串行”的概念，不知有关系吗？

4, ReadIndex，committed index，applied index
这几种索引底层实现是一样的吗，它们的数据结构是怎样的？是对同一份数据，分别建立不同的索引？又为什么建立这么多种索引？

5，版本号
您说是一个递增的全局ID， revision{2, 0}，ID指的是2还是0？ 版本号的格式是怎样的，另一个数字代表什么？

6,  bucket
请问一个 bucket 相当于一整个 B+ tree 索引树吗？还是相当于 B+ tree 中一个节点？</div>2021-01-26</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/yb5R8iaxicD8sfspaUaqMDpOopzqGjcnqxI83kxJcDlOUcdHTPP8wx6PzEiaNvl5Sf3CuMtU6r1Jzf3M0AQuef96w/132" width="30px"><span>小军</span> 👍（24） 💬（1）<div>请问老师，当Readindex结束并等待本节点的状态机apply的时候，key又被最新的更新请求给更新了怎么办，这个时候读取到的value是不是又是旧值了</div>2021-01-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/53/c4/dea5d7f3.jpg" width="30px"><span>chapin</span> 👍（11） 💬（1）<div>没有基础，学习这个，可能会比较吃力。</div>2021-01-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/22/28/0f/e0abc71b.jpg" width="30px"><span>站在树上的松鼠</span> 👍（7） 💬（5）<div>老师，下面这句话没有理解到，麻烦解答下呢，谢谢！
在client 3.4之前的版本中，负载均衡算法有一个严重的Bug：如果第一个节点异常了，可能会导致你的client访问etcd server异常。
	（1）这里第一个节点怎么理解呢？ 是指的负载均衡刚好选中的那个etcd server节点异常吗？
	（2）如果访问的节点异常了，是client库中会做重试机制，还是业务代码需要做重试呢？
</div>2021-01-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/9d/84/171b2221.jpg" width="30px"><span>jeffery</span> 👍（7） 💬（1）<div>干货太多需要慢慢消化！老师能把课程代码放到github上吗……谢谢老师</div>2021-01-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/0f/e9/564eaf5b.jpg" width="30px"><span>Want less</span> 👍（5） 💬（4）<div>当收到一个线性读请求时，它首先会从 Leader 获取集群最新的已提交的日志索引 (committed index)。
所有的client请求不是应该都通过leader下发至follower吗？</div>2021-01-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/a5/cd/3aff5d57.jpg" width="30px"><span>Alery</span> 👍（5） 💬（1）<div>请教一个问题，在treeIndex中查询key对应的版本号，这里是会返回当前key的所有版本号吗？</div>2021-01-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/18/a5/34/6e3e962f.jpg" width="30px"><span>yayiyaya</span> 👍（4） 💬（2）<div>问答： etcd 在执行读请求过程中涉及磁盘 IO 吗？
答： 涉及到磁盘， 当读请求从treeIndex获取到用户的 key 和相关版本号信息后，去查询value值时， 没有命中 buffer， 会从boltdb获取数据， 这个时候就涉及到了磁盘。</div>2021-02-04</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/19/78/df/424bdc4a.jpg" width="30px"><span>于途</span> 👍（4） 💬（1）<div>如果你的 client 版本 &lt;= 3.3，那么当你配置多个 endpoint 时，负载均衡算法仅会从中选择一个 IP 并创建一个连接（Pinned endpoint）

请问，此句提到的负载均衡算法是否等同：随机选中某个IP？</div>2021-01-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/5f/e5/54325854.jpg" width="30px"><span>范闲</span> 👍（4） 💬（2）<div>wal log里面会涉及到磁盘读写。lsm树，双memtable，都满了刷到磁盘，继续写memtable.</div>2021-01-22</li><br/><li><img src="" width="30px"><span>Geek_ddfeca</span> 👍（3） 💬（1）<div>有一点没明白，文中提到：C 节点则会等待，直到状态机已应用索引 (applied index) 大于等于 Leader 的已提交索引时 (committed Index)(上图中的流程四)，然后去通知读请求，数据已赶上 Leader，你可以去状态机中访问数据了 (上图中的流程五)。
但12中提到，“etcd 无论 Apply 流程是成功还是失败，都会更新 raftAppliedIndex 值&quot;。那岂不是即使apply失败了，也会更新raftAppliedIndex ，但其实follower并没真正赶上leader，读到的还是旧数据?</div>2021-10-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/e8/ac/7324d5ca.jpg" width="30px"><span>七里</span> 👍（2） 💬（1）<div>boltdb怎么保证全局的revision呢</div>2021-01-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/d4/9b/00f6c7f8.jpg" width="30px"><span>no-one</span> 👍（2） 💬（1）<div>如果读之前follower节点的索引已经是最新的了，还会先去leader节点读readindex吗</div>2021-01-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/41/38/4f89095b.jpg" width="30px"><span>写点啥呢</span> 👍（2） 💬（1）<div>另外还想问下唐老师，是否会有章节介绍下etcd集群管理和请求路由的原理，比如节点如何探活及增减，及像在线性读场景里，请求是否一定要通过已提交的quorum内节点处理还是任何节点都可以处理呢？</div>2021-01-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1b/96/47/93838ff7.jpg" width="30px"><span>青鸟飞鱼</span> 👍（2） 💬（2）<div>老师，如果ReadIndex读过程中，流程4状态机迟迟不应用索引？或者流程5中，未能通知到读请求？这些情况会换节点读还是幂等重试呢？</div>2021-01-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/17/46/ac/9c324436.jpg" width="30px"><span>抖腿冠军</span> 👍（1） 💬（3）<div>这个goreman  怎么搞不下来？ 只有我一个人搞不下来？</div>2022-03-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/11/3e/925aa996.jpg" width="30px"><span>HelloBug</span> 👍（1） 💬（1）<div>从状态机里读数据是什么意思呢？</div>2021-11-02</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/e1/4f/00476b4c.jpg" width="30px"><span>Remember九离</span> 👍（1） 💬（2）<div>有一个问题，当我发起一个线性读的时候，此时Leader 发生脑裂，这时候etcd是咋么处理的，响应异常？</div>2021-04-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/26/ae/9e/9ef2bf83.jpg" width="30px"><span>%v</span> 👍（1） 💬（2）<div>请问下，老师，如果没从treeIndex 中获取到key对应的revision是不是就直接返回key not found了？</div>2021-03-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1f/66/1b/1e76e031.jpg" width="30px"><span>Nights Watch</span> 👍（1） 💬（1）<div>老师，请问下etcd是不是对IO读写延迟要求很高，最近发现磁盘IO性能下降时apiserver连不上etcd</div>2021-01-25</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1f/59/d3/696b1702.jpg" width="30px"><span>校歌</span> 👍（1） 💬（1）<div>通过goreman，快速安装etcd集群，提示“transport: http2Server.HandleStreams failed to read frame: read tcp 127.0.0.1:2379-&gt;127.0.0.1:47320: read: connection reset by peer”，是什么那里设置不对吗？</div>2021-01-24</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTJcvQzf86HsxOkPcRpibBdCxDW0IK9wel9TmkEhicHPUHPRhzKna8wecDcJcVbNHNSrUMt4GHLxY3iaA/132" width="30px"><span>Coder4</span> 👍（1） 💬（1）<div>ReadIndex其实没读懂，又查了下其他资料
其实应该是写成read index，维持和commited index一致，就能明白了</div>2021-01-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/57/4f/6fb51ff1.jpg" width="30px"><span>奕</span> 👍（1） 💬（1）<div>ETCD 集群中，每个节点都有 WAL 和状态机功能吗？ WAL 不是 leader 节点才起作用的？</div>2021-01-22</li><br/><li><img src="" width="30px"><span>叶峥瑶</span> 👍（0） 💬（1）<div>你好，想问下etcd 默认应该实现的是你描述的线性读吧。。我们可以调整他的一致性级别吗？调整为串行读。</div>2021-10-13</li><br/><li><img src="" width="30px"><span>Geek_369a15</span> 👍（0） 💬（1）<div>etcd在 client 3.4 之前的版本中，负载均衡算法有一个严重的 Bug：如果第一个节点异常了，可能会导致你的 client 访问 etcd server 异常，特别是在 Kubernetes 场景中会导致 APIServer 不可用。不过，该 Bug 已在 Kubernetes 1.16 版本后被修复。--------公司的kubernetes版本是1.14，etcd版本是3.3.10, k8s集群起不来，原因是断电引起etcd数据不一致，一主二从，有一个从节点可以正常，其它都挂了，请问老师，这种情况可以修复吗，试了一些网上提的方法都不行，刚好在这篇文章看到了原因。</div>2021-09-30</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/20/c3/94/e89ebc50.jpg" width="30px"><span>神毓逍遥</span> 👍（0） 💬（1）<div>本章节的作用，尤其针对新手，比如说我，了解了全景图，掌握了读请求的整个请求的路径这是重点，具体到链路中的每个模块是如何实现的，初次看时，不懂没关系，老师会在后续详细讲解，学习好比建大厦，先跟老师学习如何设计，画出架构图，然后针对每块知识点突击</div>2021-09-15</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/e8/c2/77a413a7.jpg" width="30px"><span>Action</span> 👍（0） 💬（2）<div>17:16:33 etcd1 | Starting etcd1 on port 5000
17:16:33 etcd2 | Starting etcd2 on port 5100
17:16:33 etcd3 | Starting etcd3 on port 5200
17:16:33 etcd1 | &#47;bin&#47;sh: bin&#47;etcd: No such file or directory
17:16:33 etcd1 | Terminating etcd1
17:16:33 etcd2 | &#47;bin&#47;sh: bin&#47;etcd: No such file or directory
17:16:33 etcd2 | Terminating etcd2
17:16:33 etcd3 | &#47;bin&#47;sh: bin&#47;etcd: No such file or directory
17:16:33 etcd3 | Terminating etcd3
老师 我这问题应该怎么修复呀？</div>2021-09-15</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/18/26/dd/d58156b1.jpg" width="30px"><span>一粒</span> 👍（0） 💬（1）<div>“比如 etcd Learner 节点只允许指定接口和参数的访问”，老师，learner节点是什么角色</div>2021-09-07</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/51/c6/5929b321.jpg" width="30px"><span>1</span> 👍（0） 💬（1）<div>buffer的缓存同步机制是哪种？旁路缓存机制吗？</div>2021-09-04</li><br/>
</ul>