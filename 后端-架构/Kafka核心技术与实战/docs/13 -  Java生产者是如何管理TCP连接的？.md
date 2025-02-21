你好，我是胡夕。今天我要和你分享的主题是：Kafka的Java生产者是如何管理TCP连接的。

## 为何采用TCP？

Apache Kafka的所有通信都是基于TCP的，而不是基于HTTP或其他协议。无论是生产者、消费者，还是Broker之间的通信都是如此。你可能会问，为什么Kafka不使用HTTP作为底层的通信协议呢？其实这里面的原因有很多，但最主要的原因在于TCP和HTTP之间的区别。

从社区的角度来看，在开发客户端时，人们能够利用TCP本身提供的一些高级功能，比如多路复用请求以及同时轮询多个连接的能力。

所谓的多路复用请求，即multiplexing request，是指将两个或多个数据流合并到底层单一物理连接中的过程。TCP的多路复用请求会在一条物理连接上创建若干个虚拟连接，每个虚拟连接负责流转各自对应的数据流。其实严格来说，TCP并不能多路复用，它只是提供可靠的消息交付语义保证，比如自动重传丢失的报文。

更严谨地说，作为一个基于报文的协议，TCP能够被用于多路复用连接场景的前提是，上层的应用协议（比如HTTP）允许发送多条消息。不过，我们今天并不是要详细讨论TCP原理，因此你只需要知道这是社区采用TCP的理由之一就行了。
<div><strong>精选留言（30）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/10/fd/fd/326be9bb.jpg" width="30px"><span>注定非凡</span> 👍（51） 💬（6）<div>Apache Kafka的所有通信都是基于TCP的，而不是于HTTP或其他协议的
1 为什采用TCP?
（1）TCP拥有一些高级功能，如多路复用请求和同时轮询多个连接的能力。
	（2）很多编程语言的HTTP库功能相对的比较简陋。
		名词解释：
			多路复用请求：multiplexing request，是将两个或多个数据合并到底层—物理连接中的过程。TCP的多路复用请求会在一条物理连接上创建若干个虚拟连接，每个虚拟连接负责流转各自对应的数据流。严格讲：TCP并不能多路复用，只是提供可靠的消息交付语义保证，如自动重传丢失的报文。

2 何时创建TCP连接？
	（1）在创建KafkaProducer实例时，
A：生产者应用会在后台创建并启动一个名为Sender的线程，该Sender线程开始运行时，首先会创建与Broker的连接。
B：此时不知道要连接哪个Broker，kafka会通过METADATA请求获取集群的元数据，连接所有的Broker。
	（2）还可能在更新元数据后，或在消息发送时
3 何时关闭TCP连接
	（1）Producer端关闭TCP连接的方式有两种：用户主动关闭，或kafka自动关闭。
		A：用户主动关闭，通过调用producer.close()方关闭，也包括kill -9暴力关闭。
		B：Kafka自动关闭，这与Producer端参数connection.max.idles.ms的值有关，默认为9分钟，9分钟内没有任何请求流过，就会被自动关闭。这个参数可以调整。
		C：第二种方式中，TCP连接是在Broker端被关闭的，但这个连接请求是客户端发起的，对TCP而言这是被动的关闭，被动关闭会产生大量的CLOSE_WAIT连接。
</div>2019-10-31</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/f3/f3/3fbb4c38.jpg" width="30px"><span>旭杰</span> 👍（28） 💬（4）<div>Producer 通过 metadata.max.age.ms定期更新元数据，在连接多个broker的情况下，producer是如何决定向哪个broker发起该请求？</div>2019-07-23</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/DYAIOgq83eoXW5rycAcrNTwgOvib8poPXO0zvIekIPzBZJfsnciaLPIw9Q1t3rsXeH6DR24QndpYQibvibhR1tKHPw/132" width="30px"><span>小马</span> 👍（23） 💬（2）<div>老师有个问题请教下：
Producer 通过 metadata.max.age.ms 参数定期地去更新元数据信息，默认5分钟更新元数据，如果没建立TCP连接则会创建，而connections.max.idle.ms默认9分钟不使用该连接就会关闭。那岂不是会循环往复地不断地在创建关闭TCP连接了吗？</div>2020-01-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/a8/0c/82ba8ef9.jpg" width="30px"><span>Frank</span> 👍（19） 💬（1）<div>最近在使用kafka Connector做数据同步服务，在kafka中创建了许多topic，目前对kafka了解还不够深入，不知道这个对性能有什么影响？topic的数量多大范围比较合适？</div>2019-07-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/9c/35/9dc79371.jpg" width="30px"><span>你好旅行者</span> 👍（16） 💬（4）<div>老师好，看了今天的文章我有几个问题：

1.Kafka的元数据信息是存储在zookeeper中的，而Producer是通过broker来获取元数据信息的，那么这个过程是否是这样的，Producer向Broker发送一个获取元数据的请求给Broker，之后Broker再向zookeeper请求这个信息返回给Producer?

2.如果Producer在获取完元数据信息之后要和所有的Broker建立连接，那么假设一个Kafka集群中有1000台Broker，对于一个只需要与5台Broker交互的Producer，它连接池中的链接数量是不是从1000-&gt;5-&gt;1000-&gt;5?这样不是显得非常得浪费连接池资源？</div>2019-07-02</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/9b/6e/edd2da0c.jpg" width="30px"><span>蓝魔丶</span> 👍（14） 💬（8）<div>老师，如果Broker端被动关闭，会导致client端产生close_wait状态，这个状态持续一段时间之后，client端不是应该发生FIN完成TCP断开的正常四次握手吗？怎么感觉老师讲的这个FIN就不会再发了，导致了僵尸连接的产生？</div>2019-08-04</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/80/bb/c0ed9d76.jpg" width="30px"><span>kursk.ye</span> 👍（12） 💬（12）<div>试想一下，在一个有着 1000 台 Broker 的集群中，你的 Producer 可能只会与其中的 3～5 台 Broker 长期通信，但是 Producer 启动后依次创建与这 1000 台 Broker 的 TCP 连接。一段时间之后，大约有 995 个 TCP 连接又被强制关闭。这难道不是一种资源浪费吗？很显然，这里是有改善和优化的空间的。

这段不敢苟同。作为消息服务器中国，连接应该是种必要资源，所以部署时就该充分给予，而且创建连接会消耗CPU,用到时再创建不合适，我甚至觉得Kafka应该有连接池的设计。

另外最后一部分关于TCP关闭第二种情况，客户端到服务端没有关闭，只是服务端到客户端关闭了，tcp是四次断开，可以单方向关闭，另一方向继续保持连接</div>2019-07-02</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/92/ba/9833f06f.jpg" width="30px"><span>半瓶醋</span> 👍（9） 💬（2）<div>胡夕老师，Kafka集群的元数据信息是保存在哪里的呢，以CDH集群为例，我比较菜：）</div>2020-05-13</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTKcGBqEZQKHjq3XaSZRLmxrCykMEotI0yKWX7RbbPZh6xTdmNRsum2YxtHv33zHGFdVqxic1pIEn8Q/132" width="30px"><span>yzh</span> 👍（8） 💬（1）<div>老是您好，咨询两个问题。
1. Producer实例创建和维护的tcp连接在底层是否是多个Producer实例共享的，还是Jvm内，多个Producer实例会各自独立创建和所有broker的tcp连接
2.Producer实例会和所有broker维持连接，这里的所有，是指和topic下各个分区leader副本所在的broker进行连接的，还是所有的broker，即使该broker下的所有topic分区都是flower
</div>2019-08-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/75/a8/dfe4cade.jpg" width="30px"><span>电光火石</span> 👍（5） 💬（1）<div>谢谢老师。有几个问题请教一下：
1. producer连接是每个broker一个连接，跟topic没有关系是吗？（consumer也是这样是吗？）
2. 我们运维在所有的broker之前放了一个F5做负载均衡，但其实应该也没用，他会自动去获取kafka所有的broker，绕过这个F5，不知道我的理解是否正确？
3. 在线上我们有个kafka集群，大概200个topic，数据不是很均衡，有的一天才十几m，有的一天500G，我们是想consumer读取所有的topic，然后后面做分发，但是consumer会卡死在哪，也没有报错，也没有日志输出，不知道老师有没有思路可能是什么原因？
谢谢了！</div>2019-07-07</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/25/7f/473d5a77.jpg" width="30px"><span>曾轼麟</span> 👍（4） 💬（1）<div>老师下面就有一个问题，KafkaProducer是建议创建实例后复用，像连接池那样使用，还是建议每次发送构造一个实例？听完这讲后感觉哪个都不合理，每次new会有很大的开销，但是一次new感觉又有僵尸连接，KafkaProducer适合池化吗？还是建议单例？</div>2019-07-02</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/f5/db/93d89a14.jpg" width="30px"><span>Wenthkim</span> 👍（3） 💬（1）<div>老师，请教一个问题，目前遇到一个文中所提的一个问题，就是broker端被直接kill -9,然后产生不量的close_wait,导致重启broker后，producer和consumer都连不上，刷了大量的日志，把机器磁盘给刷爆了，请问老师这个问题我应该怎么去处理？</div>2019-07-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/4f/60/049a20e9.jpg" width="30px"><span>吴宇晨</span> 👍（3） 💬（1）<div>老师你好，kafka更新元数据的方法只有每5分钟的轮训吗，如果有监控zk节点之类的，是不是可以把轮询元数据时间调大甚至取消</div>2019-07-02</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/b3/c5/7fc124e2.jpg" width="30px"><span>Liam</span> 👍（3） 💬（1）<div>producer是否会有类似于heart beat的机制去探测可能被broker关闭的连接然后建立重连呢？</div>2019-07-02</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/51/0d/fc1652fe.jpg" width="30px"><span>James</span> 👍（2） 💬（1）<div>请问老师，
第一次创建实例，获取metadata数据，比如有1000个Broker，则会创建1000个连接吗
然后跟不存在的主题发送消息，也会获取metadata数据，然后也是创建1000个连接吗
最后，定时更新metadada也是会创建1000个连接吗

然后最大保活时间又删除无用的连接，是吧。</div>2020-05-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/c8/99/22d2a6a7.jpg" width="30px"><span>张伯毅</span> 👍（2） 💬（1）<div>整个集群 topic 的数量有限制嘛, 最大是多少 ?
单台broker上分区数最好不要超过 2k . 这个是根据经验来的嘛,还是官方有推荐.??</div>2019-12-25</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/67/f4/9a1feb59.jpg" width="30px"><span>钱</span> 👍（2） 💬（3）<div>1：集群中的任意一台broker都拥有整个集群的所有broker的信息？
通过评论了解到，所有的元数据是存储在zookeeper集群节点中的，broker是缓存了这部分信息。元数据知都有主题的信息、都有broker的信息。

2：勇敢的质疑精神是，独立思考的前提

3：当Producer 尝试给一个不存在的主题发送消息时，Broker 会告诉 Producer 说这个主题不存在。此时 Producer 会发送 METADATA 请求给 Kafka 集群，去尝试获取最新的元数据信息。
这种情况是怎么发生的，一个主题如果不存在，producer怎么知道给那个broker建立连接，发送消息？</div>2019-08-15</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/a8/e2/f8e51df2.jpg" width="30px"><span>Li Shunduo</span> 👍（2） 💬（1）<div>请问Producer会和同一台broker建立多个TCP连接吗？</div>2019-07-03</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/64/9b/d1ab239e.jpg" width="30px"><span>J.Smile</span> 👍（1） 💬（1）<div>老师，深入思考🤔再追问下:
“如果某个 Socket 连接上连续 9 分钟都没有任何请求“过境”的话，那么消费者会强行“杀掉”这个 Socket 连接”，这个socket连接被杀掉后，还会重新跟leader副本所在的broker节点建立连接吗？如果会，这个应该是不会reblance因为跟心跳连接不是同一个。所以，会在啥场景重新建立？
</div>2020-07-06</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/b5/c4/9148b40d.jpg" width="30px"><span>SunshineBoy</span> 👍（1） 💬（1）<div>假如broker leader副本有100台机器，bootStrap.servers配置了10个broker地址，kafkaProducer创建实例时，是创建100个Tcp连接还是110个Tcp连接？</div>2020-03-24</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTLl9nj9b6RydKADq82ZwOad0fQcvXWyQKk5U5RFC2kzHGI4GjIQsIZvHsEm7mFELgMiaGx3lGq9vag/132" width="30px"><span>咸淡一首诗</span> 👍（1） 💬（2）<div>胡老师问一个问题，producer 异步发送数据时报这个错： The server disconnected before a response was received，想问一下这个可能导致的原因以及解决办法，kafka版本是0.10.1.1，谢谢老师。</div>2020-03-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/ee/d6/0142c3a3.jpg" width="30px"><span>HZ</span> 👍（1） 💬（2）<div>老师 有一点不明白，为什么更新元数据需要和所有的broker建立 tcp 连接呢？ 我感觉应该仅仅是controller或者某个broker吧。</div>2020-02-24</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTLHKka9hn8hYyd7SD12PEYiazRKg2a5iaFibP7z13t9ARicUvbwItESpIYONxV6gHMFYTmdp4eGZ4YDsA/132" width="30px"><span>cgddw</span> 👍（1） 💬（2）<div>broker有很多time_wait端口，甚至比established多，这是什么情况</div>2019-08-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/29/a5/9c6e7526.jpg" width="30px"><span>丽儿</span> 👍（1） 💬（1）<div>请问一下老师客户端是怎么选择broker的</div>2019-08-15</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/45/23/28311447.jpg" width="30px"><span>盘尼西林</span> 👍（1） 💬（1）<div>问一下元数据具体指的是什么？存放在broker端的维护topic的信息的元数据么？</div>2019-08-01</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/17/8b/4b/15ab499a.jpg" width="30px"><span>风轻扬</span> 👍（1） 💬（1）<div>老师，作为kafka的初学者来说。您建议使用kafka的原生API练习文中demo，还是使用被其他框架整合的kafka练习？</div>2019-08-01</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTJZCkGPSOcvucpfLqRP3aqp3qRpwJKyzjNms4jMwibIkxpjiaszqiazSItCeo3IxqQSFvMDh66XaJ2zw/132" width="30px"><span>JoeyLi666</span> 👍（1） 💬（2）<div>老师，最近使用kakfa，报了个异常：
Caused by: org.apache.kafka.common.KafkaException: Record batch for partition Notify-18 at offset 1803009 is invalid, cause: Record is corrupt (stored crc = 3092077514, computed crc = 2775748463)
kafka的数据还会损坏，不是有校验吗？</div>2019-07-04</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/88/26/b8c53cee.jpg" width="30px"><span>南辕北辙</span> 👍（1） 💬（2）<div>老师您好，我在本地分别用1.x版本和2.x版本的生产者去测试，为什么结果和老师的不一样呢。初始化KafkaProducer时，并没有与参数中设置的所有broker去建立连接，然后我sleep十秒，让sender线程有机会多运行会。但是还是没有看到去连接所有的broker。只有当运行到procuder.send时才会有Initialize connection日志输出，以及由于metadata的needUpdate被更新成true，sender线程会开始有机会去更新metadata去连接broker（产生Initialize connection to node...for sending metadata request）。之前学习源码的时候，也只注意到二个地方去连接broker（底层方法initiateConnect，更新metadata时建立连接以及发送数据时判断待发送的node是否建立了连接）。老师是我哪里疏忽了吗，还是理解有问题。翻阅老师的书上TCP管理这块貌似没有过多的讲解，求老师指导。。</div>2019-07-03</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/c7/dc/9408c8c2.jpg" width="30px"><span>ban</span> 👍（1） 💬（1）<div>如果多个线程都使用一个KafkaProducer实例，缓冲器被填满的速度会变快。
老师看评论这句话不太理解，多个线程共用一个实例，没有再new新的实例，为什么缓冲器很快填满，不是利用原有的实例的吗。</div>2019-07-03</li><br/><li><img src="" width="30px"><span>Geek_Sue</span> 👍（1） 💬（1）<div>胡老师，我想请教一下。
connections.max.idle.ms这个值如果设置为-1，按照您文章里所说，KafkaProducer会创建bootstrap.servers中全部tcp连接，如果是1000个，那么就是说这1000个连接永远不会关闭了？</div>2019-07-03</li><br/>
</ul>