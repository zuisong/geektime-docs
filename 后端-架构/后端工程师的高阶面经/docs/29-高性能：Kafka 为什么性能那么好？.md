你好，我是大明。今天我们来讨论一个问题，Kafka 的性能为什么那么好？

Kafka 的高性能话题也算是热点了，如果你面试的公司在并发量或者数据量上已经到了一定地步，那么面试的时候大概率逃不过这个问题。

大部分人面不好这个部分的原因只有一个：Kafka 为了实现高性能采用的手段太多了，以至于根本记不住。那么这一节课我就先聚焦在 Kafka 本身为了高性能做了哪些事情，下一节课我再从实践出发，告诉你怎么优化 Kafka 的性能。

让我们先从 Kafka 的一些基本知识开始说起。

## Kafka 分段与索引

即便在同一个分区内部，Kafka 也进一步利用了分段日志和索引来加速消息查找。在 Kafka 内部，一个分区的日志是由很多个段（segment）组成的，每个段你可以理解成一个文件。同一个 topic 的文件就存放在以 topic 命名的目录下。

![图片](https://static001.geekbang.org/resource/image/5b/af/5b02d02b705bfd1b6afd1000b462bbaf.png?wh=1920x653)

为了快速找到对应的段文件，段日志文件使用了偏移量来命名。假如说一个文件的名字是 N.log，那么就表示这个段文件里第一条消息的偏移量是 N + 1。

这里你就能猜到，Kafka 完全可以根据文件名来进行二分查找，从而快速定位到段文件。

为了加快段文件内的查找，每一个段文件都有两个索引文件。

- 一个是偏移量索引文件，存储着部分消息偏移量到存储位置的映射，类似于 `<offset, position>` 这种二元组。这个 offset 不是全局 offset，是相对于这个文件第一条消息的偏移量。也就是说假如第一条消息的全局偏移量是 1000，那么偏移量为 1002 的消息的索引项是 `<2, pos1>`。
- 一个是时间索引文件，存储着时间戳到存储位置的映射，类似于 `<timestamp, position>` 二元组。
<div><strong>精选留言（12）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/14/dc/08/64f5ab52.jpg" width="30px"><span>陈斌</span> 👍（5） 💬（1）<div>老师这节课讲的很好，之前也看过其他人讲过Kafka为什么性能高，但是都讲的不全面，学习到了。

page cache 技术，MySQL、 Redis、Elasticsearch  也用到了。
顺序写  Hive、Spark、ClickHouse 都使用到了。
零拷贝 技术  Netty, RocketMQ肯定使用到了。

分区可以用来缩小并发粒度，减轻并发竞争:
JDK1.8 之前实现的 ConcurrentHashMap 版本。HashTable 是基于一个数组 + 链表实现的，所以在并发读写操作集合时，存在激烈的锁资源竞争，也因此性能会存在瓶颈。而 ConcurrentHashMap 就很很巧妙地使用了分段锁 Segment 来降低锁资源竞争</div>2023-08-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/37/3f/a9127a73.jpg" width="30px"><span>KK</span> 👍（1） 💬（3）<div>“可以确定 20000 这条消息应该放在 010031.log 这个文件里面。”，这里的20000是不是写错了，应该是2000？
根据描述：假如说一个文件的名字是 N.log，那么就表示这个段文件里第一条消息的偏移量是 N + 1。</div>2023-11-03</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/17/37/a0/032d0828.jpg" width="30px"><span>上杉夏香</span> 👍（0） 💬（1）<div>让我想到Go的GMP模型，P拿G的时候，先从本地G队列里面拿，没有的话，再去全局G队列拿。本地G队列竞争比较少（应该全无竞争，只不过得防一手其他P来自己这里偷拿），全局G队列就要面对所有P的“偷拿”。</div>2024-03-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/37/3f/a9127a73.jpg" width="30px"><span>KK</span> 👍（0） 💬（1）<div>请问老师一个问题：kafka 多分区，在写入的时候，是同时写入多个分区吗？还是只写主分区，然后同步到从分区？</div>2023-11-03</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/31/4e/78/ee4e12cc.jpg" width="30px"><span>Lum</span> 👍（0） 💬（1）<div>锁分离（Lock Separation）：在高并发环境下，锁竞争可能会成为瓶颈。锁分离是一种将锁拆分成多个细粒度锁的技术，以减少锁竞争和提高并发性能。例如，在数据库中，可以将表锁拆分为行锁或列锁。

数据分片（Data Sharding）：数据分片是一种将数据拆分成多个分片的技术，以提高并发性能和可扩展性。每个分片可以独立处理请求，从而减少竞争和提高吞吐量。例如，在分布式数据库中，可以将数据按照某种规则（如哈希或范围）划分到不同的节点上。

缓存（Caching）：缓存是一种将数据存储在内存中，以加速读写操作和减少对后端存储系统的访问的技术。例如，在 Web 应用中，可以使用缓存来缓存页面、结果集或对象，以减少数据库访问和提高响应速度。

异步处理（Asynchronous Processing）：异步处理是一种将请求和响应分离的技术，以提高并发性能和可扩展性。例如，在 Web 应用中，可以使用异步 Servlet 或异步消息处理器来处理请求，从而释放线程资源和提高吞吐量。

无锁编程（Lock-free Programming）：无锁编程是一种不使用锁的并发编程技术，以减少竞争和提高性能。例如，在并发数据结构中，可以使用无锁算法（如 CAS）来实现原子操作，从而避免锁竞争和死锁。</div>2023-10-27</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/o2pS2W4rp4ribiaoZpkeWRoCaibyNHqK5oqa71Rf23KPjBwCzsIdXiaalfT1o9BT8NbkViagSVAwD8sF6qOEC7bOibvg/132" width="30px"><span>Geek_icecream</span> 👍（0） 💬（2）<div>老师在讲解“零拷贝”时，提到的“四次内核态与用户态的切换”那张图里面，出现了两次“系统调用写操作”，是不是写错了？在进行第一次用户态与内核态切换时，不应该是“系统调用读操作”吗？先将内核态的数据“读”到用户态</div>2023-10-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/28/44/cf/791d0f5e.jpg" width="30px"><span>ZhiguoXue_IT</span> 👍（0） 💬（1）<div>请教一下老师，kafka高性能的原因是这些，阿里的rocketmq的高性能有相似的吗</div>2023-09-29</li><br/><li><img src="" width="30px"><span>Geek_43dc82</span> 👍（0） 💬（1）<div>发现了一些语言层面为了减少并发粒度的，减少锁并发竞争的优化，比如Golang GMP调度模型中的有global queue还有每个P本地的queue，实际P本地的queue的存在也是为了减少并发竞争</div>2023-09-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/37/c1/3a/880a0932.jpg" width="30px"><span>五号特派员</span> 👍（0） 💬（1）<div>请问老师kafka和pulsar对比如何呢</div>2023-09-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/25/87/f3a69d1b.jpg" width="30px"><span>peter</span> 👍（0） 💬（1）<div>请教老师几个问题：
Q1：应用进入内核态，以Java为例，是什么语句？
文中有这一句：“这一步应用就是发了一个指令，然后是 DMA 来完成的”，这里的“应用发指令”，从Java代码的角度，什么代码的效果是普通的两次拷贝？什么代码可以做到零拷贝（即该代码可以控制DMA来完成数据拷贝）？
(附：如果是C语言，又是哪一个语句？这个和专栏有点距离，可以不答)
Q2：kafa是用Java写的，kafka可以控制Page Cache，那么，什么Java代码可以控制Page Cache？
Q3：kafka的批量处理，是可以设置的吗？比如：是否采用批量处理，批量处理的数量等。应用可以设置吗？
Q4：电商的topic按什么分类？
比如京东，首页左边是商品分类，会按商品类型来设置topic吗？
Q5：生产者和消费者的压缩，并不是应用压缩，而是kafka客户端的压缩，对吗？ 即生产者和消费者的开发人员并不需要开发压缩、解压缩功能，而是调用kafka的客户端的库，由库来完成压缩和解压缩功能。
Q6：kafka功能强大，那其他三种MQ就没有必要用了，只选kafka就可以了。是这样吗？</div>2023-08-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/d0/91/89123507.jpg" width="30px"><span>Johar</span> 👍（0） 💬（1）<div>不过之前阿里云中间件团队测试过，在一个 topic 八个分区的情况下，超过 64 个 topic 之后，Kafka 性能就开始下降了。
老师，这个测试数据是部署了多少broker节点？换句话说，一个broker节点分配多少分区比较合适？</div>2023-08-23</li><br/><li><img src="" width="30px"><span>Geek_3d0fe8</span> 👍（3） 💬（0）<div>如果broken存储的是批量压缩后的消息，那么消费者读取的时候是会把整批读出来然后取满足条件的offset吗？</div>2024-03-16</li><br/>
</ul>