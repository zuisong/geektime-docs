你好，我是韩健。

学习了前面15讲的内容后，我们了解了很多常用的理论和算法（比如CAP定理、Raft算法等）。是不是理解了这些内容，就能够游刃有余地处理实际系统的问题了呢？

在我看来，还远远不够，因为理论和实践的中间是存在鸿沟的，比如，你可能有这样的感受，提到编程语言的语法或者分布式算法的论文，你说起来头头是道，但遇到实际系统时，还是无法写程序，开发分布式系统。

而我常说，实战是学习的最终目的。为了帮你更好地掌握前面的理论和算法，接下来，我用5讲的时间，分别以InfluxDB企业版一致性实现、Hashicorp Raft、KV系统开发实战为例，带你了解如何在实战中使用技术，掌握分布式的实战能力。

今天这一讲，我就以InfluxDB企业版为例，带你看一看系统是如何实现一致性的。有的同学可能会问了：为什么是InfluxDB企业版呢？因为它是排名第一的时序数据库，相比其他分布式系统（比如KV存储），时序数据库更加复杂，因为我们要分别设计2个完全不一样的一致性模型。当你理解了这样一个复杂的系统实现后，就能更加得心应手地处理简单系统的问题了。

那么为了帮你达到这个目的。我会先介绍一下时序数据库的背景知识，因为技术是用来解决实际场景的问题的，正如我之前常说的“要根据场景特点，权衡折中来设计系统”。所以当你了解了这些背景知识后，就能更好的理解为什么要这么设计了。
<div><strong>精选留言（27）</strong></div><ul>
<li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTKrzZT06vXeP6IfR9iasoiaaDeYiaUmmN6pgwvNUpLhrauiasU9acvNcdSuicrhicMmBhvEufcjPTS7ZXRA/132" width="30px"><span>Geek_3894f9</span> 👍（21） 💬（2）<div>课后思考题，答案是QNWR，Wn，R1。wn是因为对写入的时间要求不高，r1是因为可以读取任意一节点，读性能好。</div>2020-03-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/c3/5d/ced9b5c2.jpg" width="30px"><span>Michael Tesla</span> 👍（15） 💬（3）<div>我觉得思考题的场景特点是：读多写少，读的性能要求高，数据要保证强一致性。

如果使用 Raft 算法 保证强一致性，那么读写操作都应该在领导者节点上进行。这样的话，读的性能相当于单机，不是很理想。

应该采用 Quorum NWR 技术，设置 W = N，R = 1。每次都要写入全部节点，写操作的性能会比较差。但是，因为写操作比较少，所以这个缺点可以忍受。而读操作只需要读任意一个节点就能返回最新的数据，性能非常高。</div>2020-04-06</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/99/27/47aa9dea.jpg" width="30px"><span>阿卡牛</span> 👍（9） 💬（5）<div>这个实战太企业了，新手完全无从下门，有没有些入门的课程</div>2020-03-25</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/03/1c/c9fe6738.jpg" width="30px"><span>Kvicii.Y</span> 👍（5） 💬（1）<div>1.META节点是Raft算法实现，那是不是存在这如果节点过多消息同步慢的问题呢？存在的话如何解决呢？(只能减少Raft节点？)
2.思考题使用quorum nwr可以达到最终一致性，这里说的强一致是最终一致的意思吗？</div>2020-03-30</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1f/7d/31/b630e3a1.jpg" width="30px"><span>Following U</span> 👍（3） 💬（1）<div>hello，讲师好，influxdb 企业版你这边的分布式版本的github 地址吗？</div>2020-07-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/54/9a/76c0af70.jpg" width="30px"><span>每天晒白牙</span> 👍（3） 💬（2）<div>感觉自己对这些知识理解的还是不够，更不能进行实战应用，还得好好学学。

对于思考题，首先要求强一致性，读多写少，那是不是可以像  META 节点一样，采用 Raft 算法实现强一致性。但这样对性能可能就有影响了，不过这个 KV 系统是读多写少，应该也可以

然后就是从性能考虑，可以在 AP 系统中实现强一致性。根据文中提示，可以采用 Quorun NWR 实现
</div>2020-03-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/43/56/62c38c36.jpg" width="30px"><span>欧阳</span> 👍（2） 💬（2）<div>除了quorum NWR。kfk的分区是不是也是一种思路</div>2020-03-30</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/19/b3/57/2d92cf9a.jpg" width="30px"><span>姜川</span> 👍（2） 💬（1）<div>老师，raft要实现强一致是不是就需要收到所有节点的ACK才可以，半数以上那种只能是最终一致性吧，因为会有短暂的不一致发生</div>2020-03-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/57/6e/b6795c44.jpg" width="30px"><span>夜空中最亮的星</span> 👍（2） 💬（1）<div>喜欢案例，让案例来的更猛烈些吧</div>2020-03-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/19/d9/ff/b23018a6.jpg" width="30px"><span>Heaven</span> 👍（1） 💬（1）<div>读多写少啊,只需要保证在每次都必须要写入到每一个节点上就可以了,然后读的时候直接去读,自然是最新的
</div>2020-08-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/19/89/20488013.jpg" width="30px"><span>hanazawakana</span> 👍（1） 💬（1）<div>hinted-handoff是直接邮寄的一种实现方式吗</div>2020-06-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/df/6c/5af32271.jpg" width="30px"><span>Dylan</span> 👍（1） 💬（1）<div>可以在AP模型中，引入QNWR</div>2020-04-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/25/00/3afbab43.jpg" width="30px"><span>88591</span> 👍（1） 💬（1）<div>1、存储系统，数据肯定要冗余
2、可以使用WNR 模型
          1、写不多 ，全写
          2、读多，一个读</div>2020-04-02</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/52/40/e57a736e.jpg" width="30px"><span>pedro</span> 👍（1） 💬（1）<div>前面的十几讲都在为这一讲做铺垫，快更新，看看后面的实战部分😃</div>2020-03-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/ea/8b/613c162e.jpg" width="30px"><span>nomoshen</span> 👍（0） 💬（1）<div>关于最后的堆砌开源软件这个观点我其实有点不能认同；的确在influxdb场景上的存储不断的优化是值得鼓励，并且觉得这就是它的门槛和优势；但是在一些时序场景上加入内存数据库、消息队列、流式引擎来解决时序场景上的一些难点我觉得也是可以的；</div>2020-10-19</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/YicovLZyvibpkfJwuAib1FEyibVDN6Oia1Wsg7jibT0uTj0UDH75KAX6vfSvstjy1IHTW7WpNbMlZZO9SnGoPj3AE2DQ/132" width="30px"><span>要努力的兵长</span> 👍（0） 💬（1）<div>它使用 Raft 算法实现 META 节点的一致性（一般推荐 3 节点的集群配置）   ------------ Raft算法  来实现强一致性？？？  Raft算法不是只可 最终一致性吗？</div>2020-09-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/19/89/20488013.jpg" width="30px"><span>hanazawakana</span> 👍（0） 💬（1）<div>请问这个Quorum NWR是influxdb enterprise才有的吗？influxdb 1.0版本和2.0版本没有吗？</div>2020-06-01</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/83/39/f9623363.jpg" width="30px"><span>竹马彦四郎的好朋友影法師</span> 👍（0） 💬（1）<div>&quot;因为查询时就会出现访问节点数过多而延迟大的问题。&quot; 这句话感觉是不是想表达的是如果AP系统包含节点过多，因为要达到最终一致性，会导致同步时间比较长，所以读到最新数据延迟长~</div>2020-05-06</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/83/39/f9623363.jpg" width="30px"><span>竹马彦四郎的好朋友影法師</span> 👍（0） 💬（1）<div>我觉得这是老师对前面的知识的一个串讲~ 感觉很好~ 赞！</div>2020-05-06</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/15/d7/96e77edd.jpg" width="30px"><span>问心</span> 👍（0） 💬（1）<div>存储使用Raft，可能的话对数据进行分区分片，或者使用Quorun NWR进行查询，尽可能的将热数据加载到缓存</div>2020-03-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/87/30/4626c8c0.jpg" width="30px"><span>Fs</span> 👍（0） 💬（1）<div>AP型的实现大框架是类似的，influxDB的介绍和Cassandra的实现非常相似。那么支持时序这一特点，influxDB有什么不一样的设计呢</div>2020-03-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/17/fe/f1/4f1632f8.jpg" width="30px"><span>Scream!</span> 👍（0） 💬（1）<div>多来点实战案例</div>2020-03-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/00/4e/be2b206b.jpg" width="30px"><span>吴小智</span> 👍（0） 💬（1）<div>懵懵懂懂，似懂非懂，还是要多学习。</div>2020-03-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/3e/d2/5f9d3fa7.jpg" width="30px"><span>羽翼1982</span> 👍（0） 💬（1）<div>在AP的系统中，使用Quorum NWR理论
如果写少读多，假设有3个副本，可以将策略调整为3个副本写成功才返回，读则可以只读取一个副本的内容；如果网络不稳定，3副本写成功到时失败率高，99线的延迟大，可以退一步使用2写2读的策略；不过很少在实际系统上看到类似3副本，允许1副本写不成功时缓存本地等待Hinted-handoff后续同步这样的策略，InfluxDB中不太清楚，至少Cassandra里面没有

PS: 我们公司今年刚刚把时序数据库从InfluxDB转到VictoriaMetrics上，据说性能更高，与Promeheus的适配也更好，不知道老师对VM是否有研究可以简单分享下
</div>2020-03-18</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTKhuGLVRYZibOTfMumk53Wn8Q0Rkg0o6DzTicbibCq42lWQoZ8lFeQvicaXuZa7dYsr9URMrtpXMVDDww/132" width="30px"><span>hello</span> 👍（0） 💬（1）<div>给老师大大的赞，对实战部分很是期待，我现在就希望快点更新！</div>2020-03-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/47/31/f35367c8.jpg" width="30px"><span>小晏子</span> 👍（0） 💬（1）<div>课后思考：这个里面有几个点是设计这个系统的关键，读请求（百万级）远大于写请求（千级），要求读的强一致性。
因为写请求很低，可以仿照influxDB的设计，分成meta节点和data节点，meta节点使用cp模型，使用raft算法，data节点使用ap模型，使用quorum NWR和反墒算法保证强一致性，因为写少，所以只要少量meta节点即可满足要求，比如三个，对于大量读请求，data节点可以保障一致性和百万级请求。</div>2020-03-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/22/f4/9fd6f8f0.jpg" width="30px"><span>核桃</span> 👍（0） 💬（0）<div>这里关于InfluxDB的副本机制,因为这里的数据是监控数据的话,其实没必要实现主副本那种,但是在其他场景中,例如分布式文件系统里面,就需要了,因为修复数据的难度更大了.
当然这里关于副本数据传输,有一个优化点的,使用两个缓存队列来实现.
第一队列就是正常接受到数据的时候正常串行发送.
如果节点发送Data数据到其他节点上失败了,那么在简单重试后还是失败,就应该放到第二缓存队列中.
在第二队列的任务都是那些有问题的需要不断重试的,这时候可以上报到Meta集群里面了.进行其他的处理.

总的来说,因为本人是做分布式文件系统的,这里真的有很多很多相似的地方,但是文件系统需要考虑修复和数据重平衡等很多很多问题.</div>2022-01-09</li><br/>
</ul>