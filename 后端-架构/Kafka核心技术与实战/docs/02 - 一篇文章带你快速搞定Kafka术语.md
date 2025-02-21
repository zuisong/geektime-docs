你好，我是胡夕。今天我们正式开启Apache Kafka学习之旅。

在Kafka的世界中有很多概念和术语是需要你提前理解并熟练掌握的，这对于后面你深入学习Kafka各种功能和特性将大有裨益。下面我来盘点一下Kafka的各种术语。

在专栏的第一期我说过Kafka属于分布式的消息引擎系统，它的主要功能是提供一套完备的消息发布与订阅解决方案。在Kafka中，发布订阅的对象是主题（Topic），你可以为每个业务、每个应用甚至是每类数据都创建专属的主题。

向主题发布消息的客户端应用程序称为生产者（Producer），生产者程序通常持续不断地向一个或多个主题发送消息，而订阅这些主题消息的客户端应用程序就被称为消费者（Consumer）。和生产者类似，消费者也能够同时订阅多个主题的消息。我们把生产者和消费者统称为客户端（Clients）。你可以同时运行多个生产者和消费者实例，这些实例会不断地向Kafka集群中的多个主题生产和消费消息。

有客户端自然也就有服务器端。Kafka的服务器端由被称为Broker的服务进程构成，即一个Kafka集群由多个Broker组成，Broker负责接收和处理客户端发送过来的请求，以及对消息进行持久化。虽然多个Broker进程能够运行在同一台机器上，但更常见的做法是将不同的Broker分散运行在不同的机器上，这样如果集群中某一台机器宕机，即使在它上面运行的所有Broker进程都挂掉了，其他机器上的Broker也依然能够对外提供服务。这其实就是Kafka提供高可用的手段之一。
<div><strong>精选留言（30）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/13/a7/9a/495cb99a.jpg" width="30px"><span>胡夕</span> 👍（157） 💬（6）<div>结尾处增加了一张图，提炼了02中讲到的Kafka概念和术语，希望能够帮助到你：）</div>2019-06-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/ae/27/3dfcc699.jpg" width="30px"><span>时光剪影</span> 👍（177） 💬（13）<div>整理一遍个人的理解：

Kafka体系架构=M个producer +N个broker +K个consumer+ZK集群

producer:生产者

Broker：服务代理节点，Kafka服务实例。
n个组成一个Kafka集群，通常一台机器部署一个Kafka实例，一个实例挂了其他实例仍可以使用，体现了高可用

consumer：消费者
消费topic 的消息， 一个topic 可以让若干个consumer消费，若干个consumer组成一个 consumer group ，一条消息只能被consumer group 中一个consumer消费，若干个partition 被若干个consumer 同时消费，达到消费者高吞吐量

topic ：主题

partition： 一个topic 可以拥有若干个partition（从 0 开始标识partition ），分布在不同的broker 上， 实现发布与订阅时负载均衡。producer 通过自定义的规则将消息发送到对应topic 下某个partition，以offset标识一条消息在一个partition的唯一性。
一个partition拥有多个replica，提高容灾能力。 
replica 包含两种类型：leader 副本、follower副本，
leader副本负责读写请求，follower 副本负责同步leader副本消息，通过副本选举实现故障转移。
partition在机器磁盘上以log 体现，采用顺序追加日志的方式添加新消息、实现高吞吐量</div>2019-06-16</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/3d/51/9723276c.jpg" width="30px"><span>邋遢的流浪剑客</span> 👍（100） 💬（13）<div>如果允许follower副本对外提供读服务（主写从读），首先会存在数据一致性的问题，消息从主节点同步到从节点需要时间，可能造成主从节点的数据不一致。主写从读无非就是为了减轻leader节点的压力，将读请求的负载均衡到follower节点，如果Kafka的分区相对均匀地分散到各个broker上，同样可以达到负载均衡的效果，没必要刻意实现主写从读增加代码实现的复杂程度</div>2019-06-06</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/2e/8b/32a8c5a0.jpg" width="30px"><span>卡特</span> 👍（62） 💬（4）<div>加入a主题有4个分区，消费者组有2个实例，发布应用的时候，会先新启动一个服务节点，加入消费组，通过重平衡分配到到至少1个最多2个分区，消费者的偏移量是
1，重新从0开始
2，拿到分配分区的上一个消费者偏移量？

如果按照文章说的，即偏移量为0，消息应该会重复消费；

如果拿到上一个消费者的偏移量则不会消息重复消费，具体过程又是怎样的？

求解惑，</div>2020-04-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/d3/6e/281b85aa.jpg" width="30px"><span>永光</span> 👍（49） 💬（6）<div>为什么 Kafka 不像 MySQL 那样允许追随者副本对外提供读服务？

答：因为mysql一般部署在不同的机器上一台机器读写会遇到瓶颈，Kafka中的领导者副本一般均匀分布在不同的broker中，已经起到了负载的作用。即：同一个topic的已经通过分区的形式负载到不同的broker上了，读写的时候针对的领导者副本，但是量相比mysql一个还实例少太多，个人觉得没有必要在提供度读服务了。（如果量大还可以使用更多的副本，让每一个副本本身都不太大）不知道这样理解对不对?</div>2019-06-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/b7/f9/a8f26b10.jpg" width="30px"><span>jacke</span> 👍（39） 💬（7）<div>胡老师：
       还想问个分区的问题，比如一个topic分为0，1，2 个分区
       写入0到9条消息，按照轮训分布:
              0分区：0，1，2，9
              1分区：3，4，5，
              2分区：6，7，8
        那对于消费端来说，不管是p2p点对点模式，还是push&#47;sub模式来说，
        如何保证消费端的读取顺序也是从0到9？因为0到9条消息是分布在3个
        分区上的，同时消费者是主动轮训模式去读分区数据的，
        有没有可能读到后面写的数据呢？比如先读到5在读到4？
        ps:刚开始学习，问题比较多，谅解
    </div>2019-06-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/b3/bb/7789fc32.jpg" width="30px"><span>杨枝雨</span> 👍（28） 💬（2）<div>老师，我想问下
1、 kafka是按照什么规则将消息划分到各个分区的？
2、既然同一个topic下的消息分布在不同的分区，那是什么机制将topic、partition、record关联或者说管理起来的？</div>2019-06-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/8d/c7/d66952bc.jpg" width="30px"><span>Happy</span> 👍（23） 💬（3）<div>主写从读无非就是为了减轻leader节点的压力，而kafka中数据分布相对比较均匀，所说的Follower从节点,实际上也是其他topic partition的Leader节点，所以在Follower可以读数据，那么会影响Follower节点上的做为Leader的partition的读性能，所以整体性能并没有提升，但是带来了主从数据同步延迟导致的数据不一致的问题</div>2019-06-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/78/dc/0c9c9b0f.jpg" width="30px"><span>(´田ω田`)</span> 👍（23） 💬（3）<div>1、主题中的每个分区都只会被组内的一个消费者实例消费，其他消费者实例不能消费它。
2、假设组内某个实例挂掉了，Kafka 能够自动检测到，然后把这个 Failed 实例之前负责的分区转移给其他活着的消费者。

意思是1个分区只能同时被1个消费者消费，但是1个消费者能同时消费多个分区是吗？那1个消费者里面就会有多个消费者位移变量？
如果1个主题有2个分区，消费者组有3个消费者，那至少有1个消费者闲置？</div>2019-06-06</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/17/df/e5/65e37812.jpg" width="30px"><span>快跑</span> 👍（15） 💬（2）<div>老师，你好
假如只有一个Producer进程，Kafka只有一分区。Producer按照1，2，3，4，5的顺序发送消息，Kafka这个唯一分区收到消息一定是1，2，3，4，5么？ Producer端，网络，数据格式等因素，会不会导致Kafka只有一个分区接收到数据顺序跟Producer发送数据顺序不一致</div>2019-07-02</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1b/55/2a/1ef26397.jpg" width="30px"><span>FunnyCoder</span> 👍（13） 💬（1）<div>小白一枚 Kafka可以关闭重平衡吗？可不可在逻辑上新建一个消费者或者将failed消费者重启 而不是分配给其他消费者</div>2019-12-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/b3/bb/7789fc32.jpg" width="30px"><span>杨枝雨</span> 👍（11） 💬（6）<div>老师 ，一个分区的N个副本是在同个Broker中的吗，还是在不同的Broker中，还是说是随机的？</div>2019-07-02</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/9c/35/9dc79371.jpg" width="30px"><span>你好旅行者</span> 👍（10） 💬（2）<div>我之前在学习Kafka的时候也有过这个问题，为什么Kafka不支持读写分离，让从节点对外提供读服务？
其实读写分离的本质是为了对读请求进行负载均衡，但是在Kafka中，一个topic的多个Prtition天然就被分散到了不同的broker服务器上，这种架构本身就解决了负载均衡地问题。也就是说，Kafka的设计从一刻开始就考虑到了分布式的问题，我觉得这是Linkedln开发团队了不起的地方。
尽管如此，我觉得还有一个问题我没有想明白，如果Producer就是对某些broker中的leader副本进行大量的写入，或者Consumer就是对某些broker中的leader副本进行大量的拉取操作，那单台broker服务器的性能不还是成为了整个集群的瓶颈？请问老师，这种情况Kafka是怎么解决的呢？</div>2019-06-07</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/17/8b/4b/15ab499a.jpg" width="30px"><span>风轻扬</span> 👍（8） 💬（2）<div>专栏过去这么久了。不知道还回不回被老师回答。老师，如果consumer一直不提交位移，会有什么影响？目前想到的是：当前consumer 实例宕机，后续消费该分区的消费者实例就只能遵从auto.reset.offset的指定了。除此之外还有其他问题吗？</div>2020-04-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/6b/1b/4b397b80.jpg" width="30px"><span>蛮野</span> 👍（8） 💬（1）<div>分区数量一开始定义后，后面可以增加分区后，原来分区的数据应该不会迁移吧？分区数量可以减少吗？</div>2019-09-11</li><br/><li><img src="" width="30px"><span>dbo</span> 👍（7） 💬（3）<div>Myaql中从追随者读取数据对server和client都没有影响，而Kafka中从追随者读取消息意味着消费了数据，需要标记该数据被消费了，涉及到做一些进度维护的操作，多个消费实例做这些操作复杂性比较高，如果可以从追随者读也可能会牺牲性能，这是我的理解，请老师指正。</div>2019-06-06</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/36/08/e3ed94b8.jpg" width="30px"><span>周小桥</span> 👍（7） 💬（2）<div>这里的术语介绍，在阿里一面的时候有被问到。

为什么副本不提供对外读？

我认为这个副本只是提供一个数据跟leader的同步，和当leader故障后能进行切换。还有消费者读取数据是根据offset去读取的，一份文件够了。</div>2019-06-06</li><br/><li><img src="" width="30px"><span>wrzgeek</span> 👍（6） 💬（3）<div>小白提问:
1. leader 副本分布在哪个broker上随机的吗？还是有什么机制
2. 如文中最后一个图所示，假如broker1挂掉，broker2上的follower副本会变为leader副本吗？假如不止一个follower副本，是不是有某种选举方式来决定哪个follower副本会升级为leader副本？</div>2019-06-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/7b/57/a9b04544.jpg" width="30px"><span>QQ怪</span> 👍（6） 💬（3）<div>kafka能否做到多个消费者消费一个生产者生产的数据，并能保证每个消费者消费的消息不会重复，做到并行消费?</div>2019-06-06</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/7a/93/c9302518.jpg" width="30px"><span>高志强</span> 👍（5） 💬（3）<div>老师我有个问题，消费者位移可以手动往回调么，当位移向前后，分区里之前的数据还会存在么，如果存在啥时会被删除呢</div>2019-12-05</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/ae/57/7504f5ca.jpg" width="30px"><span>蚊子</span> 👍（5） 💬（2）<div>请教一下老师：high water mark怎么理解？</div>2019-09-03</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/DYAIOgq83eoZqcVJzUjfu5noOW6OPAh6ibrBicibLmicibnVyVLHdf7GwAzf2th5s1oQ9pUbLpmq2mlVBauUZn8QUnw/132" width="30px"><span>funnyx</span> 👍（5） 💬（2）<div>胡老师，您好，最近正在学习Kafka，看了您的文章，感觉获益匪浅，但是有个地方还请指教一下，在Kafka官网看的，”Each partition has one server which acts as the &quot;leader&quot; and zero or more servers which act as &quot;followers&quot;. 请问这里的server该作何理解？</div>2019-07-02</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/d3/6e/281b85aa.jpg" width="30px"><span>永光</span> 👍（5） 💬（1）<div>谢谢老师之前的回答：
对于之前的回答还有点小疑惑：
1、客户端会首先请求topic分区的leader副本在哪个broker上，内部自动执行的，你无需操心； 
     哈哈，确实不用操心，只是特别好奇他是怎么选的？ 因为每个topic的每个分区leader还不一样。

2、重平衡时每个消费者都会尽力去做一次位移提交（如果它会提交位移的话），这样当rebalance完成后Kafka会告诉它们订阅分区当前消费到了那里。
我理解你说的应该是在检测到有节点挂了，kafka会进行重平衡，此时未挂的节点会尽力提交自己的位移，对吧？但是针对挂了的节点我理解是没法位移提交的，针对没有没有位移提交怎么处理呀？

真的感谢老师的回答。</div>2019-06-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/c7/e6/11f21cb4.jpg" width="30px"><span>川杰</span> 👍（5） 💬（1）<div>老师请教一个问题，对于发布&#47;订阅者模式来说，消息往往是存储在某种形式的队列中的，那如何把这个队列中的消息推送给消费者呢？我们公司的做法就是利用一个线程去轮询将消息分发到各自的消费者中；可是，从实际业务场景来看，往往消息生产者只在某个特定的时间段去生产消息，而且消息是少量的，几十到几百个；服务器一直开一个线程去轮询我总觉得有些浪费资源；请问除了轮询以外有没有其他办法？</div>2019-06-06</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/ac/46/7e24bad6.jpg" width="30px"><span>杨俊</span> 👍（5） 💬（1）<div>领导者将数据同步到追随者副本既不是同步复制又不是异步复制，有一个isr列表维护，追随者副本自己去拉数据，有时候可能网络问题导致追随者副本之间存在数据不一致问题，高低水位不一样，isr列表的副本数也会不一样</div>2019-06-06</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/97/1a/389eab84.jpg" width="30px"><span>而立斋</span> 👍（4） 💬（1）<div>本来以为理解了，看了评论区之后更加糊涂了。还是能弄清楚 broker的部署，和topic partition有什么关系？</div>2020-04-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/75/9b/611e74ab.jpg" width="30px"><span>技术修行者</span> 👍（4） 💬（1）<div>文章讲的很清楚，让我对Kafka的结构有了初步的认识，有几个问题想请教一下：
1. 一个Broker就是一个Kafka实例吗？在Kafka集群中，一个Kafka实例可以有多个Broker吗？
2. 一个Topic可以由多个Broker处理吗？topic下面不同的分区的数据可以由不同的Broker来处理吗？
3. 消费者组去消费消息的时候，不同的消费者可以同时消费同一个分区里面的消息吗？

上面的问题都比较基础，请见谅。
</div>2020-03-07</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/c7/eb/50a4842a.jpg" width="30px"><span>翟岳辉</span> 👍（4） 💬（1）<div>老师，我想问两个问题
1.kafka支持接入多少生产者，生产者连接数有没有限制？
2.kafka生产侧是否支持f5负载均衡，或者是说如果kafka的服务ip发生变化，有没有什么设计，可以避免让生产者修改broker的列表，dns?</div>2020-02-15</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/67/f4/9a1feb59.jpg" width="30px"><span>钱</span> 👍（4） 💬（1）<div>Kafka 的服务器端由被称为 Broker 的服务进程构成，即一个 Kafka 集群由多个 Broker 组成，Broker 负责接收和处理客户端发送过来的请求，以及对消息进行持久化。虽然多个 Broker 进程能够运行在同一台机器上，但更常见的做法是将不同的 Broker 分散运行在不同的机器上，这样如果集群中某一台机器宕机，即使在它上面运行的所有 Broker 进程都挂掉了，其他机器上的 Broker 也依然能够对外提供服务。这其实就是 Kafka 提供高可用的手段之一。
再次请教几个小问题：
1：启动一个kafka程序，就是启动一个broker进程服务嘛？
2：假设有三台服务器A&#47;B&#47;C，三个broker进程服务1&#47;2&#47;3，老师的建议是将1&#47;2&#47;3三个broker进程同时分别放在A&#47;B&#47;C三台机器上吗？还有不同的broker是什么概念？他们应该都是同样的kafka程序，启动后进程号会不一样，这里的不同的broker是以什么角度讲的？
初学，感觉这个broker的意思没弄明白，望老师或其它同学帮忙解答一下。</div>2019-08-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/9b/6e/edd2da0c.jpg" width="30px"><span>蓝魔丶</span> 👍（4） 💬（2）<div>老师，kafka采用多个多个分区支持负载均衡，这样无法保证全局顺序唯一吧，现在业内常采用单分区来解决这个问题，但是这样又丢失了负载均衡能力，后面kafka会针对这个问题会进一步加强吗？</div>2019-08-03</li><br/>
</ul>