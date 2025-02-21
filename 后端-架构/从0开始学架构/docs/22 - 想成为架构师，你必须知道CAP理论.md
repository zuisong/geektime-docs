CAP定理（CAP theorem）又被称作布鲁尔定理（Brewer's theorem），是加州大学伯克利分校的计算机科学家埃里克·布鲁尔（Eric Brewer）在2000年的ACM PODC上提出的一个猜想。2002年，麻省理工学院的赛斯·吉尔伯特（Seth Gilbert）和南希·林奇（Nancy Lynch）发表了布鲁尔猜想的证明，使之成为分布式计算领域公认的一个定理。对于设计分布式系统的架构师来说，CAP是必须掌握的理论。

布鲁尔在提出CAP猜想的时候，并没有详细定义Consistency、Availability、Partition Tolerance三个单词的明确定义，因此如果初学者去查询CAP定义的时候会感到比较困惑，因为不同的资料对CAP的详细定义有一些细微的差别，例如：

> **Consistency**: where all nodes see the same data at the same time.
> 
> **Availability**: which guarantees that every request receives a response about whether it succeeded or failed.
> 
> **Partition tolerance**: where the system continues to operate even if any one part of the system is lost or fails.
<div><strong>精选留言（30）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/0f/87/57/645159ee.jpg" width="30px"><span>鹅米豆发</span> 👍（71） 💬（3）<div>前面对于一致性的描述有些问题。修正一下。
1、Paxos算法本身是满足线性一致性的。线性一致性，也是实际系统能够达到的最强一致性。
2、Paxos及其各种变体，在实际工程领域的实现，大多是做了一定程度的取舍，并不完全是线性一致性的。
3、比如，Zookeeper和Etcd，都是对于写操作（比如选举），满足线性一致性，对于读操作未必满足线性一致性。即可以选择线性一致性读取，也可以选择非线性一致性读取。这里的非线性一致性，就是顺序一致性。
4、cap中的一致性，是指线性一致性，而不是顺序一致性。</div>2018-06-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/0f/80/7c3f35e4.jpg" width="30px"><span>luop</span> 👍（39） 💬（2）<div>第二版解释从 non-failing node 的角度去看待「可用性」，个人存疑。

如果一个集群有 2 个 node，某个时刻 2 个 node 都 fail 了，那么此时该集群的「可用性」该如何定义？

个人觉得：「一致性」和「可用性」都应该站在 client 侧去审视；而「分区容忍性」则是集群 node 侧在遇到网络分区的问题时，选择如何去影响 client 侧感知到的「一致性」和「可用性」。</div>2018-08-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/18/10/731b4319.jpg" width="30px"><span>轩辕十四</span> 👍（30） 💬（1）<div>网络分区类似于脑裂。

个人对CAP的类比，不知是否合适:
P要求数据有冗余，
C要求数据同步，会花时间，
A要求返回及时，不需要等。
不可能三角形说的是:
要备份要同步，就得等;
要备份不想等，就会不同步;
要同步还不想等，就别备份</div>2018-07-06</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/37/ef/66671161.jpg" width="30px"><span>Geek_7vgqz2</span> 👍（22） 💬（1）<div>应该再补充哪些系统上ca，哪些是cp，哪些是ap，他们为什么这么设计，都有什么好处。</div>2018-06-16</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/cf/82/a3ea8076.jpg" width="30px"><span>tim</span> 👍（21） 💬（2）<div>请问一下作者，在CP的选型中。 假如是查询一条并不存在的数据，文中还说得通。
但如果出现更新数据不及时，由于n1和n2 出现分区错误，那么n2如何知道自己不是最新的数据并返回error呢？？ 
假如就是简单的mysql主从， 从库并没有断连主库，只是数据在请求来是还没有更新到最新。 那么从库又从哪里得知这件事儿的呢？？</div>2018-07-22</li><br/><li><img src="" width="30px"><span>Geek_88604f</span> 👍（15） 💬（2）<div>        paxos的核心思想是少数服从多数，在节点数为2n+1的集群中，只要n+1节点上完成了写入就能保证接下来的读操作能够读到最新的值。从这一点来说它满足C（对某个指定的客户端来说，读操作保证能够返回最新的写操作结果);一个实现了paxos协议的集群最多可以容忍n个节点故障（n个节点同时故障的概率是比较小的），非故障节点组成的集群仍能正常提供服务，从这个角度来讲它满足A(非故障的节点在合理的时间内返回合理的响应，不是错误和超时的响应)；paxos集群发生分区肯能存在两种情况，第一种情况是发生分区后没有发生重新选举，这种情况下集群仍能正常工作，因此满足P(当出现网络分区后，系统能够继续“履行职责”)。另一种情况是发生分区后原来的集群达不到多数派，集群不在对外提供服务，因此不满足P，当发生这种情况的时候，一般会快速修复。总的来说在某种意义上来看paxos满足CAP。</div>2019-09-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/d8/a1/cd868183.jpg" width="30px"><span>aduan</span> 👍（15） 💬（2）<div>老师，你好，有个疑问，在cp架构中n1，n2通讯是中断的，n2根据设什么作为依据返回error？</div>2018-12-16</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/36/d2/c7357723.jpg" width="30px"><span>发条橙子 。</span> 👍（11） 💬（1）<div>你好老师 ，这里讲的分区容错是指什么 ，是指发生分区现象时系统正常运行 。 但是分区现象具体指的是什么 可以详细讲一下么</div>2019-01-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/ce/49/33b88f62.jpg" width="30px"><span>Gaozy</span> 👍（10） 💬（2）<div>有个疑问，很多工程实现都是选择AP并保证最终一致性，但是选择了A不就意味着返回数据不是最新的吗，最终一致性是如何实现的</div>2019-02-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/c9/20/e4f1b17c.jpg" width="30px"><span>zj</span> 👍（9） 💬（1）<div>ZK出现分区，不能再履行职责了吧，因此ZK不满足P。老师这样理解对吗</div>2018-06-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/61/bc/88a905a5.jpg" width="30px"><span>亮点</span> 👍（8） 💬（4）<div>CAP讨论的是分布式系统，文中又说分布式系统必然选择P，感觉有矛盾，有点像鸡和蛋的问题。分区是分布式系统的一种异常现象，分区容忍应该是当发生分区问题时系统对外的功能特性，P到底是区别于C和A的一种特性，还是需要C和A配合才能完成，不是很理解，还请老师帮忙解答。</div>2019-12-01</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1d/fe/83/df562574.jpg" width="30px"><span>慎独明强</span> 👍（6） 💬（2）<div>就拿分布式注册中心zookeeper和eruka来举例吧。当zk集群出现故障时，为了满足节点数据一致性，节点是不可被访问的，那么满足的是CP理论。而eruka每个节点都带全部数据，当节点出现故障，不能保障数据的一致性，但是可用的。满足了AP理论。</div>2020-08-03</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/0c/e1/e0ba4e87.jpg" width="30px"><span>卡莫拉内西</span> 👍（6） 💬（1）<div>paxos， zk的zab协议的理论基础，保证的是最终一致性，满足的是cp
</div>2018-06-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/61/f2/ca989d6f.jpg" width="30px"><span>Leon Wong</span> 👍（6） 💬（3）<div>老师你好，有个问题想请教：

最近正在研究 zookeeper，通读完本篇课程，心中存疑，还望解答。

zookeeper 并不保证所有的 client 都能读到最新的数据，相较于线性一致性而言，zookeeper 采用的是顺序一致性（我理解一致性程度更弱）。

那么对于这种情况，zookeeper 与最终一致性方案相比，结合本篇文章的解释，其本质上依然不能保证所有的  client 读到最新的数据，那是否可以理解为 zookeeper 就是 AP 系统？

抑或，根据本篇的解释，zookeeper 采用顺序一致性，能保证『指定』（而非所有）的 client 读到最新的数据，即可以称之为 CP 系统；而 AP 系统甚至可能不能保证任意一个 client 能读到最新数据。因此 zookeeper 属于 CP 系统的范畴？

请问老师，两个思路，哪个正确？</div>2018-06-16</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/ae/2d/26d7ed68.jpg" width="30px"><span>shenlinxiang</span> 👍（4） 💬（1）<div>重读18年买的极客时间，对比其它地方讲解的内容，简直佩服膜拜了</div>2021-03-31</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/f7/9d/be04b331.jpg" width="30px"><span>落叶飞逝的恋</span> 👍（4） 💬（1）<div>是不是在大多数场景下选择AP架构，而一致性是通过最终一致性来妥协实现的？</div>2020-10-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/cf/bb/22af0e52.jpg" width="30px"><span>孙振超</span> 👍（4） 💬（1）<div>知识获取来源分为几个层次：论文是第一手，书籍是第二层次，博客资料就是第三层的了，之前学习cap都是在网上找的博客，虽然也找了多篇博客相互佐证进行融合。但今天看了这篇文章才发现对cap的理解还是有些肤浅，真的是无声处惊雷，平凡处见真章，这种求学态度会贯穿在生活工作中的方方面面的，受教了。

paxos协议是为了解决数据一致性而设计的算法，主要是通过投票选举的方式决定出主节点，之后就以主节点的数据为准，因而属于pc模式。

另外，作者提到是以 Robert Greiner的文章进行cap的解读，网上介绍cap的文章很多，选择他的原因能否透漏一下？</div>2018-07-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/61/f2/ca989d6f.jpg" width="30px"><span>Leon Wong</span> 👍（4） 💬（2）<div>老师你好，有个问题想请教：

最近正在研究 zookeeper，通读完本篇课程，心中存疑，还望解答。

zookeeper 并不保证所有的 client 都能读到最新的数据，相较于线性一致性而言，zookeeper 采用的是顺序一致性（我理解一致性程度更弱）。

那么对于这种情况，zookeeper 与最终一致性方案相比，结合本篇文章的解释，其本质上依然不能保证所有的  client 读到最新的数据，那是否可以理解为 zookeeper 就是 AP 系统？

抑或，根据本篇的解释，zookeeper 采用顺序一致性，能保证『指定』（而非所有）的 client 读到最新的数据，即可以称之为 CP 系统；而 AP 系统甚至可能不能保证任意一个 client 能读到最新数据。因此 zookeeper 属于 CP 系统的范畴？

请问老师，两个思路，哪个正确？</div>2018-06-16</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/cd/7b/31a6bf42.jpg" width="30px"><span>强</span> 👍（3） 💬（1）<div>面试时曾被问到过，Redis是基于CAP中的哪个？至今还没明白到底是CP还是AP</div>2020-11-03</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/45/c9/a4f7054f.jpg" width="30px"><span>佳</span> 👍（3） 💬（1）<div>区块链属于cp,因为区块链对要求数据一致性很高，就是所有人看到的数据都要一致</div>2018-11-01</li><br/><li><img src="" width="30px"><span>laurencezl</span> 👍（3） 💬（2）<div>先谢过老师分享！
关于p我还是有点疑问❓p要的是当网络脑裂分区时依然提供合理的response，他跟a要的合理有啥区别？
cp架构中，当网络发生故障导致分区两边数据不一致时，为了保证c而牺牲a，这个时候，系统不已经牺牲高可用而返回了错误吗，那不是已经违背了p下的合理响应吗？</div>2018-09-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/90/c6/0ba1789a.jpg" width="30px"><span>半夏</span> 👍（2） 💬（2）<div>CAP 应用
1.CP
有个疑惑，N1节点因为网络分区问题，没有把数据复制给N2
客户端访问N2，N2 需要返回 Error
这块要怎么实现返回Error？</div>2021-03-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/dd/bd/9b93ea26.jpg" width="30px"><span>blacknccccc</span> 👍（2） 💬（1）<div>cap定理中的p既然是必然要满足的一个而且很容易满足，c和a选择一个就可以满足p了，那为啥不直接说是ca定理呢，另外zk没有数据共享，套用这个定理不太合适呢</div>2018-08-07</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/cf/82/a3ea8076.jpg" width="30px"><span>tim</span> 👍（2） 💬（1）<div>有个问题，既然无法保证p，那么我们选择它又有什么用呢。
况且有些p是无法通过服务器来处理的，比如连接到服务器时，网络超时，服务器未接到任何信息。总不能指望浏览器来重试保证吧。

对于p的理解，我觉得还是难以理解。有没有更加深入的文章</div>2018-07-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/84/f8/c22d32b4.jpg" width="30px"><span>刚子</span> 👍（2） 💬（2）<div>你好，大神，原文中&#39;&#39;第二版定义了什么才是 CAP 理论探讨的分布式系统，强调了两点：interconnected 和 share data，为何要强调这两点呢？分布式系统并不一定会互联和共享数据&#39;&#39;

其中&#39;&#39;分布式系统并不一定会互联和共享数据&#39;&#39;结合上下文理解起来是一定的意思</div>2018-06-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/05/e5/aa579968.jpg" width="30px"><span>王磊</span> 👍（2） 💬（1）<div>关于提到的问题，我首先需要考虑的是，Paxos构建的集群是不是互联和有数据共享的，从而确定它是不是CAP所讨论的?
关于本文，我也建议把主流的集群环境，如spark,集群，kafka集群按照CAP理论，是满足了哪两个要素，和为什么这么取舍做下分析。</div>2018-06-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/99/23/3c3272bd.jpg" width="30px"><span>林</span> 👍（2） 💬（1）<div>ZK应该是CP，因为如果节点挂了则节点会自动down下线，而不会把错误或超时的信息给到客户端。且ZK必须保证3台及以上的节点才会提供服务，本质是不是保证C而不是A?</div>2018-06-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1b/87/37/b071398c.jpg" width="30px"><span>等风来🎧</span> 👍（1） 💬（1）<div>老师，你说mysql这种互联和共享信息的集群是CAP讨论的范围，那如果不是集群，是两个不同业务的系统，但两个系统有各自的数据库，且会冗余同一个字段，且要保证该冗余字段，在一次业务处理中保持一致性。那么这种情况属于CAP的讨论范畴吗？</div>2023-09-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1e/f5/90/2caa07d0.jpg" width="30px"><span>Geek8815</span> 👍（1） 💬（1）<div>辛苦老师解答：
1.P表示 当出现网络分区后，系统能够继续“履行职责”，这点和可用性是一脉相承的。也就是说，只有返回 reasonable response 才是 function。
当采用CP架构，当发生P时，为了保证C，A肯定就不支持了，也就无法返回easonable response，因此它就不是function，那从什么角度任务它是已经履行职责呢了（很明显CP，P和A并不一脉相承？？？），
2. CP架构肯定不满足A，那怎么理解这个一脉相承呢？</div>2021-12-31</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/8a/09/ca696484.jpg" width="30px"><span>肖克</span> 👍（1） 💬（1）<div>怎么理解CAP定理？CAP中，C代表一致性，A代表可用性，P代表分区容忍，分区容忍翻译的不好，你就直接理解为数据分片就OK了。闭上眼睛，你想想，永远的A不可能实现，A就像永动机一样，理论存在，所以A追求的是HA（高可用）。而我们是可以追求100%的C和P的。CAP定理的发明人Eric Brewe曾经承认CAP是一个容易误导人的而且过于简化的模型。在2000年，CAP的意义在于让大家开始讨论关于分布式系统的取舍。但CAP并不是一个精确的理论，他仅仅用于指方向。

这个是tidb创始人黄东旭最近一次（2021.5)接受极客时间访谈的观点，我觉得是有道理的。分区容忍是可以做到的吧，所以只能cp和ap，用觉得不对劲，到底怎么理解才正确呢？</div>2021-05-22</li><br/>
</ul>