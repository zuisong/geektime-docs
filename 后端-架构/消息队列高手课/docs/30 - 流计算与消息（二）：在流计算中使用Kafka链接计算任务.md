你好，我是李玥。

上节课我们一起实现了一个流计算的例子，并通过这个例子学习了流计算的实现原理。我们知道，流计算框架本身是个分布式系统，一般由多个节点组成一个集群。我们的计算任务在计算集群中运行的时候，会被拆分成多个子任务，这些子任务也是分布在集群的多个计算节点上的。

大部分流计算平台都会采用存储计算分离的设计，将计算任务的状态保存在HDFS等分布式存储系统中。每个子任务将状态分离出去之后，就变成了无状态的节点，如果某一个计算节点发生宕机，使用集群中任意一个节点都可以替代故障节点。

但是，对流计算来说，这里面还有一个问题没解决，就是在集群中流动的数据并没有被持久化，所以它们就有可能由于节点故障而丢失，怎么解决这个问题呢？办法也比较简单粗暴，就是直接重启整个计算任务，并且从数据源头向前回溯一些数据。计算任务重启之后，会重新分配计算节点，顺便就完成了故障迁移。

回溯数据源，可以保证数据不丢失，这和消息队列中，通过重发未成功的消息来保证数据不丢的方法是类似的。所以，它们面临同样的问题：可能会出现重复的消息。消息队列可以通过在消费端做幂等来克服这个问题，但是对于流计算任务来说，这个问题就很棘手了。

对于接收计算结果的下游系统，它可能会收到重复的计算结果，这还不是最糟糕的。像一些统计类的计算任务，就会有比较大的影响，比如上节课中统计访问次数的例子，本来这个IP地址在统计周期内被访问了5次，产生了5条访问日志，正确的结果应该是5次。如果日志被重复统计，那结果就会多于5次，重复的数据导致统计结果出现了错误。怎么解决这个问题呢？
<div><strong>精选留言（9）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/12/d1/29/1b1234ed.jpg" width="30px"><span>DFighting</span> 👍（14） 💬（1）<div>关于思考题，我在infoQ上找了一篇文章https:&#47;&#47;www.infoq.cn&#47;article&#47;58bzvIbT2fqyW*cXzGlG，不知道是不是这么实现的，请老师帮忙看下。</div>2019-10-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/8b/ec/dc03f5ad.jpg" width="30px"><span>张天屹</span> 👍（3） 💬（1）<div>老师你好，能介绍下Kafka 配合 Flink，与Kafka Stream 的核心区别吗</div>2019-10-05</li><br/><li><img src="" width="30px"><span>Geek_c24555</span> 👍（2） 💬（1）<div>老师好，请问下 rocketmq 可以配合 flink 实现exactly once 吗</div>2020-06-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/18/9b/46/ad3194bd.jpg" width="30px"><span>jack</span> 👍（2） 💬（1）<div>老师，使用spark streaming 和kafka时，
1、spark官方文档说，如果保存到checkpoint和把offset 提交到kafka，必须保证输出是幂等的，光使用事务是不行的；
2、那么如果无法保证输出是幂等的，是否只能把offset 保存在第三方的数据库(比如redis)中，但是这样做是否是不可以设置checkpoints ？否则spark依然会从checkpoint中读取，和从数据库中读取会造成冲突呢？
3、但不设置checkpoint，spark如何恢复现场呢？在提交命令时加入--supervise，好像yarn的模式不支持？即使使用supervise重启，没有checkpoint，也无法恢复现场吧？</div>2019-10-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/6b/27/8c964e52.jpg" width="30px"><span>不惑ing</span> 👍（0） 💬（2）<div>第25章讲kafka exactly once需要从kafka topicA读取计算再保存到kafka topocB，但从这章讲的流程看，最后不需要保存到kafka topicB，保存到其他hdfs里也可以，

所以最后一步保存位置有具体要求吗？</div>2019-10-06</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1b/65/b7/058276dc.jpg" width="30px"><span>i_chase</span> 👍（0） 💬（0）<div>kafka ==&gt; flink ==&gt; kafka虽然实现了exactly once,但是最终进入output kafka的数据不也需要消费出来的吗？
是不是因为这里从output topic消费只是打印一下消息，即使重复消费也没关系？</div>2022-03-28</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTK8qkY7FUvM17qTNadTAWzWgHtJTmnduMiaqNXJnJia0ffnpc5v6ToC139SI4FUb226eCQmBTBQzUMw/132" width="30px"><span>Geek_7825d4</span> 👍（0） 💬（0）<div>Flink 中有个 AsyncIO 算子，自身提供了 Exactly Once 语义，但是一致有个问题不太清楚，AsyncIO 为了提升性能，提供异步无序处理的方式，这种情况下，假设有一个 offset 为 1 的数据 阻塞在异步中，会不会有1一个 offset 为 2 的消息已经被处理完了，并继续向下游发送。 此时当 2 已经端到端完成时， Flink 是否会向 Kafka Source 提交 2 位置的偏移量呢，这样如何保证 Exactly Once 呢</div>2021-03-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/19/d9/ff/b23018a6.jpg" width="30px"><span>Heaven</span> 👍（0） 💬（0）<div>看了上面同学的留下的文章,发现Flink是维护两个位置offset和commitedOffset,内部在进行快照保存的时候,保存了offset作为快照内部位置,在快照完成之后,会变动维护的commitedOffset属性值,将变更后的commitedOffset提交到Kafka brokers或者ZK中</div>2021-02-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/0c/52/f25c3636.jpg" width="30px"><span>长脖子树</span> 👍（0） 💬（0）<div>正好最近在看 flink , 这部分端到端的 exactly once 实现讲得很清晰!</div>2020-08-26</li><br/>
</ul>