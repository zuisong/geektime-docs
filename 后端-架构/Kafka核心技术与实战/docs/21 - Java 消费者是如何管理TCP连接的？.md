你好，我是胡夕。今天我要和你分享的主题是：Kafka的Java消费者是如何管理TCP连接的。

在专栏[第13讲](https://time.geekbang.org/column/article/103844)中，我们专门聊过“Java**生产者**是如何管理TCP连接资源的”这个话题，你应该还有印象吧？今天算是它的姊妹篇，我们一起来研究下Kafka的Java**消费者**管理TCP或Socket资源的机制。只有完成了今天的讨论，我们才算是对Kafka客户端的TCP连接管理机制有了全面的了解。

和之前一样，我今天会无差别地混用TCP和Socket两个术语。毕竟，在Kafka的世界中，无论是ServerSocket，还是SocketChannel，它们实现的都是TCP协议。或者这么说，Kafka的网络传输是基于TCP协议的，而不是基于UDP协议，因此，当我今天说到TCP连接或Socket资源时，我指的是同一个东西。

## 何时创建TCP连接？

我们先从消费者创建TCP连接开始讨论。消费者端主要的程序入口是KafkaConsumer类。**和生产者不同的是，构建KafkaConsumer实例时是不会创建任何TCP连接的**，也就是说，当你执行完new KafkaConsumer(properties)语句后，你会发现，没有Socket连接被创建出来。这一点和Java生产者是有区别的，主要原因就是生产者入口类KafkaProducer在构建实例的时候，会在后台默默地启动一个Sender线程，这个Sender线程负责Socket连接的创建。
<div><strong>精选留言（30）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/14/3b/aa/e8dfcd7e.jpg" width="30px"><span>AAA_叶子</span> 👍（23） 💬（3）<div>消费者tcp连接一旦断开，就会导致rebalance，实际开发过程中，是不是需要尽量保证长连接的模式？</div>2019-12-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/b8/5b/dbe74486.jpg" width="30px"><span>taj3991</span> 👍（21） 💬（1）<div>老师同一个消费组的客户端都只会连接到一个协调者吗？</div>2019-07-22</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/DYAIOgq83eol8MiawYVfCtkaFL9DFGoWpuajsKicwyt7IWm07JfrLMDuksEZJqia4Rbicw0biayokhgvSK0rUXIAngQ/132" width="30px"><span>Geek_ab3d9a</span> 👍（8） 💬（1）<div>老师您好，请问k8s这样的容器平台，适合部署kafka的消费者吗？如果容器平台起了二个一模一样的消费者，对kafka来说会不会不知道自己通信的哪一个消费者?  kafka通过什么来判断不同的客户端?</div>2020-03-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/bb/c9/37924ad4.jpg" width="30px"><span>天天向上</span> 👍（8） 💬（1）<div>元数据不包含协调者信息吗？为啥还要再请求一次协调者信息 什么设计思路？</div>2019-09-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/1b/7a/390a8530.jpg" width="30px"><span>小木匠</span> 👍（6） 💬（1）<div>“负载是如何评估的呢？其实很简单，就是看消费者连接的所有 Broker 中，谁的待发送请求最少。”  
老师这个没太明白，这时候消费者不是还没连接么？那这部分信息是从哪获取到的呢？消费者本地吗？</div>2019-07-22</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/DYAIOgq83eqxnw92EOgZbyHDGMZ1d1OFDjjJKnBdmpiac8J7kBEN5h3AvvzU85mo5Chj8pkIHQc390dL1mu0neQ/132" width="30px"><span>真锅</span> 👍（4） 💬（1）<div>意思是即便知道了协调者在node 2上，还是会依然用2147483645这个id的TCP连接去跟协调者通信吗。</div>2020-04-25</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/x86UN2kFbJGGwiaw7yeVtyaf05y5eZmdOciaAF09WEBRVicbPGsej1b62UAH3icjeJqvibVc6aqB0EuFwDicicKKcF47w/132" width="30px"><span>Eco</span> 👍（4） 💬（2）<div>应该是3个tcp连接，第一个id=-1的没什么争议，然后是连接协调者的，但是broker，5个分区的leader肯定会分布到这两台broker上，那么第三类tcp就是2个tcp连接，但是这2个中完全可以有一个是直接使用连接协调者的那个tcp连接吧，但老师好像说过连接协调者的连接会和传输数据的分开，id的计算都不相同，好吧，那就4个tcp连接吧。可这里真的不能复用吗？我觉得可以。</div>2020-01-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/26/d9/f7e96590.jpg" width="30px"><span>yes</span> 👍（3） 💬（2）<div>老师我有个疑问，consumer在FindCoordinator的时候会选择负载最小的broker进行连接，文章说看消费者连接的所有 Broker 中，谁的待发送请求最少。请问consumer如何得知这个消息？如果它想知道这个消息，不就得先和“某个东西”建立连接了？</div>2020-06-20</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/DYAIOgq83eqKurYDna034zK0ibDIWicybibQhiaM6afgla2zVFqBrAemLgCh3WoibjACnic5ibiaYMd29tMB26cjaGaPoA/132" width="30px"><span>Treagzhao</span> 👍（2） 💬（1）<div>老师，“消费者程序会向集群中当前负载最小的那台 Broker 发送请求”，消费者怎么单方面知道服务器待发送的消息数量呢？而且应该只有leader才会实际发送消息吧，follower待发送的都是0,消费者怎么在建立连接之前就知道服务器的角色呢？</div>2020-05-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/64/34/03335c4a.jpg" width="30px"><span>臧萌</span> 👍（2） 💬（2）<div>我们要设计一个消息系统。有两个选择，更好的一种是每种不同schema的消息发一个topic。但是有一种担心是consumer会为每个topic建立一个连接，造成连接数太多。请问胡老师，kafka client的consumer是每个集群固定数目的tcp连接，还是和topic数目相关？</div>2019-08-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/b5/3c/967d7291.jpg" width="30px"><span>艺超(鲁鸣)</span> 👍（1） 💬（2）<div>老师好，请教一个问题，现在对于producer和consumer都介绍了维持tcp连接的情况，那么对于kafka集群 broker来说，这么多的tcp连接，是如何管理的呢？</div>2020-07-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/d3/43/f22b39c3.jpg" width="30px"><span>举个荔枝</span> 👍（1） 💬（1）<div>老师，想问下这里是不是笔误。
还记得消费者端有个组件叫Coordinator吗？协调者应该是位于Broker端的吧？</div>2019-10-02</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/93/61/3e4607c7.jpg" width="30px"><span>hpfish</span> 👍（0） 💬（2）<div>老师，我的kafka部在k8s上，版本是2.1.1，消费者通过serviceName+port的方式去访问，但是kafka重启后Pod的IP变了，消费者连得还是原来的IP有什么办法吗</div>2020-12-16</li><br/><li><img src="" width="30px"><span>crud~boy</span> 👍（0） 💬（2）<div>老师我们有这样一个场景，我们需要监测kafka是否存活，然后有一个程序没隔1s就通过tcp连接kafka，然后断开！这样会不会把kakfa连接资源耗尽了啊</div>2020-11-16</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/d5/7b/c512da6a.jpg" width="30px"><span>石栖</span> 👍（0） 💬（2）<div>胡老师，您好。我这边用的kafka 2.3 。Consumer一直出现这个错误信息在日志里面：2020-05-05 07:31:06.428  INFO 6 --- [ntainer#1-0-C-1] o.a.kafka.clients.FetchSessionHandler    : [Consumer clientId=consumer-4, groupId=test-collections] Node 1 was unable to process the fetch request with (sessionId=2065156504, epoch=1204): FETCH_SESSION_ID_NOT_FOUND. 但是我看log是INFO级别的，请问是不是可以忽略掉？网上说需要修改broker的max.incremental.fetch.session.cache.slots，有其他办法吗？</div>2020-05-05</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/eb/de/087611a3.jpg" width="30px"><span>大鸡腿</span> 👍（0） 💬（1）<div>胡大佬，问下 &quot;它连接的 Broker 节点的 ID 是 -1，表示消费者根本不知道要连接的 Kafka Broker 的任何信息。&quot; 这边会有真实的broker机器与之对应嘛？ </div>2019-12-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/bd/18/2af6bf4b.jpg" width="30px"><span>兔2🐰🍃</span> 👍（0） 💬（1）<div>有2个 Broker，5个分区的领导者副本，由zookeeper分配Leader，所以默认是均匀的，第三类会创建2个TCP连接，故共有4个TCP连接。
请问胡老师 Leader副本 分配策略是什么？</div>2019-09-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/5f/e9/95ef44f3.jpg" width="30px"><span>常超</span> 👍（45） 💬（3）<div>整个生命周期里会建立4个连接，进入稳定的消费过程后，同时保持3个连接，以下是详细。
第一类连接：确定协调者和获取集群元数据。 
 一个，初期的时候建立，当第三类连接建立起来之后，这个连接会被关闭。

第二类连接：连接协调者，令其执行组成员管理操作。
 一个

第三类连接：执行实际的消息获取。
两个分别会跟两台broker机器建立一个连接，总共两个TCP连接，同一个broker机器的不同分区可以复用一个socket。</div>2019-07-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/fd/fd/326be9bb.jpg" width="30px"><span>注定非凡</span> 👍（25） 💬（0）<div>1，何时创建
	A ：消费者和生产者不同，在创建KafkaConsumer实例时不会创建任何TCP连接。
		原因：是因为生产者入口类KafkaProducer在构建实例时，会在后台启动一个Sender线程，这个线程是负责Socket连接创建的。

	B ：TCP连接是在调用KafkaConsumer.poll方法时被创建。在poll方法内部有3个时机创建TCP连接
	（1）发起findCoordinator请求时创建
		Coordinator（协调者）消费者端主键，驻留在Broker端的内存中，负责消费者组的组成员管理和各个消费者的位移提交管理。
		当消费者程序首次启动调用poll方法时，它需要向Kafka集群发送一个名为FindCoordinator的请求，确认哪个Broker是管理它的协调者。

	（2）连接协调者时
		Broker处理了消费者发来的FindCoordinator请求后，返回响应显式的告诉消费者哪个Broker是真正的协调者。
		当消费者知晓真正的协调者后，会创建连向该Broker的socket连接。
		只有成功连入协调者，协调者才能开启正常的组协调操作。

	（3）消费数据时
		消费者会为每个要消费的分区创建与该分区领导者副本所在的Broker连接的TCP.

2 创建多少
	消费者程序会创建3类TCP连接：
	（1） ：确定协调者和获取集群元数据
	（2）：连接协调者，令其执行组成员管理操作
	（3） ：执行实际的消息获取

3 何时关闭TCP连接
	A ：和生产者相似，消费者关闭Socket也分为主动关闭和Kafka自动关闭。
	B ：主动关闭指通过KafkaConsumer.close()方法，或者执行kill命令，显示地调用消费者API的方法去关闭消费者。
	C ：自动关闭指消费者端参数connection.max.idle.ms控制的，默认为9分钟，即如果某个socket连接上连续9分钟都没有任何请求通过，那么消费者会强行杀死这个连接。
	D ：若消费者程序中使用了循环的方式来调用poll方法消息消息，以上的请求都会被定期的发送到Broker，所以这些socket连接上总是能保证有请求在发送，从而实现“长连接”的效果。
	E ：当第三类TCP连接成功创建后，消费者程序就会废弃第一类TCP连接，之后在定期请求元数据时，会改为使用第三类TCP连接。对于一个运行了一段时间的消费者程序来讲，只会有后面两种的TCP连接。
</div>2019-11-06</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/87/57/e28ba87b.jpg" width="30px"><span>Williamzhang</span> 👍（13） 💬（2）<div>我觉得作者可以跟学员的留言互动，然后每期课后思考可以在下期中贴出答案及分析，其实留言讨论也是一个非常让人有收获的地方</div>2019-07-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/e5/39/951f89c8.jpg" width="30px"><span>信信</span> 👍（6） 💬（0）<div>一共建过四次连接。若connection.max.idle.ms 不为-1，最终会断开第一次连的ID为-1的连接。</div>2019-07-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/5c/d7/e4673fde.jpg" width="30px"><span>October</span> 👍（6） 💬（0）<div>总共创建4个连接，最终保持3个连接：
        确定消费者所属的消费组对应的GroupCoordinator和获取集群的metadata时创建一个TCP连接，由于此时的node id = -1，所以该连接无法重用。
        连接GroupCoordinator时，创建第二个TCP连接，node id值为Integer.MAX_VALUE-id
        消费者会与每个分区的leader创建一个TCP连接来消费数据，node id为broker.id，由于kafka只是用id这一维度来表征Socket连接信息，因此如果多个分区的leader在同一个broker上时，会共用一个TCP连接，由于分区数大于broker的数量，所以会创建两个TCP连接消费数据。</div>2019-07-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/57/3c/081b89ec.jpg" width="30px"><span>rm -rf 😊ི</span> 👍（2） 💬（0）<div>我认为也是3个连接，第一个是查找Coordinator的，这个会在后面断开。然后5个partition会分布在2个broker上，那么客户端最多也就连接2次就能消费所有partition了，因此是连接3个，最后保持2个。</div>2019-07-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/4f/60/049a20e9.jpg" width="30px"><span>吴宇晨</span> 👍（1） 💬（0）<div>一个获取元数据的连接（之后会断开）+两个连接分区leader的连接+一个连接协调者的连接</div>2019-07-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/4d/49/28e73b9c.jpg" width="30px"><span>明翼</span> 👍（1） 💬（0）<div>连接有三个阶段：首先获取协调者连接同时也获取元数据信息，这个连接后面会关闭；连接协调者执行，等待分配分区，组协调等，这需要一个连接；后面真正消费五个分区两个broker最多就两个连接，分区大于broker所以一定是两个，因为第一类连接没有id，所以无法重用，会在第三类开启连接后关闭，所以开始四个连接最终保持三个连接</div>2019-07-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/1e/3a/5b21c01c.jpg" width="30px"><span>nightmare</span> 👍（1） 💬（0）<div>3个tcp连接  一个查询协调着和获取元数据的tcp连接    一个连接协调写 管理组成员的tcp连接    主题5个分区只有连接leader副本的broker需要创建连接</div>2019-07-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/30/65/18/791d0f5e.jpg" width="30px"><span>Lonely丶浅笑痕y</span> 👍（0） 💬（2）<div>老师，有个问题，如果消费者的实例重新启动，那是不是原本的tcp连接会很快断掉？
当前生产环境中，我看是正常1000多，重启有3000；从这节课的学习中发现，重新链接过程中的链接会比原本的多了两个阶段的链接，但应该不会多这么多</div>2024-02-04</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/kGxYrILChD8xJPX4CXxAJeia7tmvQbbMZsyV7CmnqWflUEYF4rWn1ywtNv0ZXWx04kdqcjpebpHwBz4LEOWJRmA/132" width="30px"><span>Tong</span> 👍（0） 💬（0）<div>老师，请问消费者客户端有限制端口占用的方法吗，类似白名单的方式</div>2024-01-27</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTKotsBr2icbYNYlRSlicGUD1H7lulSTQUAiclsEz9gnG5kCW9qeDwdYtlRMXic3V6sj9UrfKLPJnQojag/132" width="30px"><span>ppd0705</span> 👍（0） 💬（0）<div>请问一下如果消费多个主题，那么同一个Broker不同主题的分区消息是共用连接还是单独的？简而言之，第三类连接是broker级别还是主题级别的？</div>2022-07-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1e/37/29/b3af57a7.jpg" width="30px"><span>凯文小猪</span> 👍（0） 💬（0）<div>consumer的poll其实就是个long polling这样理解我感觉就清楚了</div>2021-09-28</li><br/>
</ul>