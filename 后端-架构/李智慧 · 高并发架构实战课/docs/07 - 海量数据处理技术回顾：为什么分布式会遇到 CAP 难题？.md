你好，我是李智慧。

在这个模块的几个案例中，我们都需要处理海量的数据，需要用到海量的存储介质，其实海量数据本质上就是一种磁盘资源敏感的高并发场景。

我们说过，为了应对资源不足的问题，我们常采用水平伸缩，即分布式的方案。数据存储的分布式问题是所有分布式技术中最具挑战性的，因为相对于“无状态”（stateless）的计算逻辑（可执行程序），数据存储是“**有状态**”（stateful）的。无状态的计算逻辑可以在任何一台服务器执行而结果不会改变，但有状态的数据却意味着数据存储和计算资源的绑定：每一个数据都需要存储在特定的服务器上，如果再增加一台空的服务器，它没有数据，也就无法提供数据访问，无法实现伸缩。

数据存储的“有状态”特性还会带来其他问题：为了保证数据存储的可靠性，数据必须多备份存储，也就是说，同一个数据需要存储在多台服务器上。那么又如何保证多个备份的数据是一致的？

因此，海量数据存储的核心问题包括：如何利用分布式服务器集群实现海量数据的统一存储？如何正确选择服务器写入并读取数据？为了保证数据的高可用性，如何实现数据的多备份存储？数据多备份存储的时候，又如何保证数据的一致性？

为了解决这些问题，在这个模块的案例设计中，我们使用了多个典型的分布式存储技术方案：分布式文件系统HDFS、分布式NoSQL数据库HBase、分布式关系数据库。下面我们就来回顾这几个典型技术方案。你可以再重新审视一下，我们案例中的技术选型是否恰当，是否有改进的空间。
<div><strong>精选留言（12）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/28/de/68/27ea710e.jpg" width="30px"><span>阿卷</span> 👍（28） 💬（1）<div>普通的hash算法是通过数据与机器数取模运算来将数据映射到具体的节点，如果有机器加入和退出，则所有的数据都需要重新映射，这将会导致大量的数据迁移。
一致性hash就是用来解决这个问题的，一致性hash算法可以在加减节点时尽可能的保证现有的映射关系不变，从而减少数据迁移量。
大致的实现思路就是预先设置一个环形节点空间，比如环上预设1万个节点，将机器id通过hash算法对应到这个环上的具体节点，数据通过hash算法对应到环上的一个节点，然后沿着这个节点顺时针寻找离他最近的机器。这样当机器上下线时只会影响环上的部分数据。
但还有一个问题，就是一个机器下线后它负责的数据将全部由环中的下一个机器接管，而且当机器数比较少的时候必然造成大量数据集中到一个节点上面，为了解决这种数据倾斜问题，一致性哈希算法引入了虚拟节点机制，即对每一个服务节点计算多个哈希，每个计算结果位置都放置一个此服务节点，这样可以使数据分布更均匀</div>2022-03-02</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/3f/2b/6ec0c1ae.jpg" width="30px"><span>curry</span> 👍（9） 💬（1）<div>老师，布隆过滤器应该只能保证数据肯定不存在，并不能保证数据一定存在，就算八个比特位都匹配了，但是仍然有几率是其他数据占用的</div>2022-03-03</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/16/65/c22b4415.jpg" width="30px"><span>风华神使</span> 👍（7） 💬（1）<div>一致性哈希的目的是让存储节点数增减时数据少挪一些，比如ceph的crush</div>2022-03-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/25/87/f3a69d1b.jpg" width="30px"><span>peter</span> 👍（2） 💬（1）<div>请教老师一个问题：
Q1：HBase图例中，Zookeeper是独立于HMaster的集群吗？
如果是独立的集群，zookeeper不了解HMaster的情况，根据什么来选主？
或者，另外一种情况是：Zookeeper和HMaster运行在同样的机器上，一台HMaster所在的机器上就有一个Zookeeper，这样zookeeper才能根据HMaster的情况选主；这种情况下，图例中的zookeeper只是逻辑上的独立集群。</div>2022-03-02</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/18/7a/5f/c05cd5dc.jpg" width="30px"><span>Ronnie</span> 👍（0） 💬（1）<div>一致性哈希解决了哈希算法在增加服务节点时，需要更改数据路由算法逻辑的问题</div>2022-03-03</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/71/05/db554eba.jpg" width="30px"><span>👽</span> 👍（0） 💬（1）<div>一致性hash：
首先先说hash，就是为了把数据均匀分布到每一个节点上。根据数据的hash值，hash值再跟节点数了取余，就得出了节点编号。但是节点如果扩容，所有节点就需要重新将数据初始化。这是我们不愿意看到的。

于是乎，有了一种解决方案。这个节点数我们假设它很长，大部分文档都是在说2点32-1次方，但我觉得其实这个长度是多少其实不重要，但主要是说他很长。与这个长度取余，这个余数就是节点在这个环的位置。

现在，我们的数据进来了。我们把数据也跟这个长度取余，也得到了一个环的下标。但是因为环很长，实际节点数量肯定远远小于这个数量。那就等数据打进来了之后，按照顺时针找一个最近的节点。这时候，如果新增节点，则不需要重新hash取余，重新分布数据。新的数据寻找就近节点的时候会自动打到这个新节点上。
一致性hash的主要原理其实就说完了。

但还有问题，如果节点数量不够多，或者节点hash值分布不均匀，就会造成数据的分布不均匀。可以尝试引入虚拟节点，让虚拟节点分布的更均匀，然后虚拟节点再指向真实节点地址即可。</div>2022-03-03</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/23/c2/5c/791d0f5e.jpg" width="30px"><span>易企秀-郭彦超</span> 👍（0） 💬（1）<div>什么是cap讲了 为什么会有cap好像没讲</div>2022-03-02</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/26/9c/3f/18624ac5.jpg" width="30px"><span>超大超</span> 👍（2） 💬（0）<div>zookeeper数据以二阶段提交协议进行写入，实现的是最终一致性或顺序一致性。
1. 客户端访问zk进行数据写入时，不论访问到哪台机器都会转发到leader服务器。
2. leader服务器生成提案发送给follower服务器，如果follower可以写入则返回ACK响应，leader收到半数以上的ack响应，则发送commit给follower服务进行写入。
3. 在写入完成后leader向客户端响应写入成功后，可能有部分follower服务器写入失败的情况。
也就是有可能读取到的数据不是最新的， 可能是旧的数据。</div>2022-04-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/b9/32/84346d4a.jpg" width="30px"><span>雪碧心拔凉</span> 👍（0） 💬（0）<div>普通hash算法有一个痛点，即没增加&#47;删除一个节点时，所有实例上的数据都会进行迁移，在数据迁移过程中，所有实例可能都暂时不可用。
一致性hash算法能保证只有附近一个节点需要迁移数据</div>2022-05-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/b9/32/84346d4a.jpg" width="30px"><span>雪碧心拔凉</span> 👍（0） 💬（0）<div>Zab协议能保证读取到的数据一定是正确的吗，如果正好读取的follow节点与其他节点网络分区，那是不是就访问到旧数据了？</div>2022-05-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/18/ee/a1ed60d1.jpg" width="30px"><span>ABC</span> 👍（0） 💬（0）<div>老师，OceanBase和MySQL比较一下，此处的分布式关系数据库是否可以替换成OceanBase？</div>2022-03-23</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTKWYicxW2TxmZbD80jCQbfs7icgV7fGdOTRWLzN7YSfLicVxU3lorJ3NSlNuzBvABrSiaHIjgibECjAVDg/132" width="30px"><span>qchang</span> 👍（0） 💬（1）<div>一致性hash，对于节点的下线，那么这个节点上的数据不就丢了吗；新节点上线，那原来的存储在下一个节点的数据，也访问不到了，这是怎么处理的，请老师解答一下</div>2022-03-10</li><br/>
</ul>