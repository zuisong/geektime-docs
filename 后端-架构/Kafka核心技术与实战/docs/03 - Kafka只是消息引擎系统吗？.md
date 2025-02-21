你好，我是胡夕。今天我们来聊一个老生常谈的话题：Kafka只是消息引擎系统吗？

要搞清楚这个问题，我们不可避免地要了解一下Apache Kafka的发展历程。有的时候我们会觉得说了解一个系统或框架的前世今生似乎没什么必要，直接开始学具体的技术不是更快更好吗？其实，不论是学习哪种技术，直接扎到具体的细节中，亦或是从一个很小的点开始学习，你很快就会感到厌烦。为什么呢？因为你虽然快速地搞定了某个技术细节，但无法建立全局的认知观，这会导致你只是在单个的点上有所进展，却没法将其串联成一条线进而扩展成一个面，从而实现系统地学习。

我这么说是有依据的，因为这就是我当初学习Kafka的方式。你可能不会相信，我阅读Kafka源码就是从utils包开始的。显然，我们不用看源码也知道这玩意是干什么用的，对吧？就是个工具类包嘛，而且这种阅读源码的方式是极其低效的。就像我说的，我是在一个点一个点地学习，但全部学完之后压根没有任何感觉，依然不了解Kafka，因为不知道这些包中的代码组合在一起能达成什么效果。所以我说它是很低效的学习方法。

后来我修改了学习的方法，转而从自上而下的角度去理解Kafka，竟然发现了很多之前学习过程中忽略掉的东西。更特别的是，我发现这种学习方法能够帮助我维持较长时间的学习兴趣，不会阶段性地产生厌烦情绪。特别是在了解Apache Kafka整个发展历史的过程中我愉快地学到了很多运营大型开源软件社区的知识和经验，可谓是技术之外的一大收获。
<div><strong>精选留言（30）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/12/19/43/226ca347.jpg" width="30px"><span>Michael 🛡YZY</span> 👍（76） 💬（3）<div>学到了。刚接触， 对一次性处理语义的概念和背后的含义不太明确， 能否结合实例讲解比较一下…</div>2019-06-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/5c/d7/e4673fde.jpg" width="30px"><span>October</span> 👍（66） 💬（11）<div>对于kafka streams相对于其他大数据流式计算框架的优势的第一点不是特别理解。spark或者flink读取消息之后再写回kafka，可能会导致多次写入kafka，老师能不能解释一下什么情况下会多次写入kafka？</div>2019-06-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/fb/58/6c422e70.jpg" width="30px"><span>清晨吼于林</span> 👍（26） 💬（2）<div>老师您好~~~
我了解的：一个partition在一个group内，只能被一个消息者进程消费（一个jvm，启动了一个java进程）。  
问题前提：经过分区算法的匹配，A partition 被 B 消费者 消费。
我的问题：在这个B的消费者里面，假如我用多线程消费（多个线程，每个线程维护了一个KafkaConsumer实例。 而不是一个KafkaConsumer然后多个worker线程消费的模式），那这多个线程都能从这个A partition里面取到消息嘛？</div>2019-06-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/e8/c5/8bdb0bba.jpg" width="30px"><span>DarKnight</span> 👍（19） 💬（2）<div>胡老师您好！我对于第一点优势那个例子不是很懂，但又很感兴趣。我能否用一个这样的情形去理解呢：

我在spark内部consume了一条数据并要进行有状态的计算，我可以通过roll back确保做到exactly once，当状态计算过程中可以通过捕捉exception从而roll back到初始状态，但状态计算过程中我可能已经将某些结果发送到kafka了（这些结果我并不想重复发送），虽然我可以roll back所有处于spark内部的数据状态，但发送到kafka的所有数据就已经收不回了。

不知道这个例子算不算一种解读呢？谢谢！</div>2019-06-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/67/f4/9a1feb59.jpg" width="30px"><span>钱</span> 👍（17） 💬（1）<div>课前思考
kafka除了可以作为一个消息引擎系统，还能用来干什么？这个还真不太清楚，它的核心功能不就是，将消息倒一道手嘛？
课后思考
1：kafka可以作为什么来使用？
1-1：一个分布式消息引擎系统——广泛使用
1-2：一个分布式流处理平台，可以和Storm&#47;Spark&#47;Flink相媲美——越来越多这么玩，根据老师的评论回复，感觉kafka更是一个分布式流处理库。
1-3：一个分布式存储系统——很少使用，关键增删改查的效率好不？如果挺好，也可以这么玩吧！

如果我是kafka的掌舵人，我会逐渐丰富kafka的生态圈，把kafka弄得和Spring全家桶类似，以后的ABC把kafka家族的程员作为标配。

2：啥是流处理？
是指实时处理无限数据集的数据的一种处理方式嘛？
3：啥是批处理？
是指一次处理一批数据，且此数据的集合是有限的？
4：流处理和批处理，没理解，kafka作为分布式流处理平台的优势也没理解？看评论，流处理的数据集是无限数据集，那岂不是永远处理不完，直到天荒地老？
5：数据正确性不足是什么意思？会丢数据？没明白和数据收集的方式的逻辑是什么？

计算机我的理解，就是处理数据的，处理数据无非是针对数据的存储转发增删改查存分析统计，然后就是挖空心思加快速度。
感觉不该如此难以理解😊，一图胜千言，希望后面看到老师有图有真相。</div>2019-08-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/8d/6f/c21eff20.jpg" width="30px"><span>平叔叔</span> 👍（7） 💬（1）<div>在这样的需求之下，搭建重量级的完整性平台实在是“杀鸡焉用牛刀，的意思中小企业使用Kafka 不用配套提供集群调度、弹性部署？

</div>2019-09-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/b4/50/c5dad2dc.jpg" width="30px"><span>Shane</span> 👍（7） 💬（2）<div>老师，能举个例子说明下流出来和批处理的区别吗？
目前我的理解就是批处理是一次请求中包含多条消息？然后消费者取出这一整个请求内容进行处理消费。流处理就是每个请求每次只发送一条消息，所以消费者也只能每次消费一条？

感觉自己理解的应该不怎么正确呢？网络上的解释也是非常虚，想看看老师有啥指导的吗？</div>2019-06-15</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/9c/35/9dc79371.jpg" width="30px"><span>你好旅行者</span> 👍（7） 💬（1）<div>关于【但是计算结果有可能多次写入到 Kafka，因为它们不能控制 Kafka的语义处理】。我想问老师，Kafka不是在0.11版本实现了exactly once，保证一条消息只会被消费一次吗，为什么说计算结果还有可能会被多次写入到Kafka呢？</div>2019-06-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/6d/1c/d9746372.jpg" width="30px"><span>EricJones</span> 👍（5） 💬（1）<div>我又仔细意会了一下，流处理大概已经懂了，但是批处理的正确性到底体现在哪里。还是不知道。</div>2019-06-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/ac/62/37912d51.jpg" width="30px"><span>东方奇骥</span> 👍（5） 💬（3）<div>老师，请问一下，kafka相比于rabbitmq和activemq作为消息引擎系统的优势是什么呢。就是文中所说的消息正确性吗？</div>2019-06-16</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/d3/6e/281b85aa.jpg" width="30px"><span>永光</span> 👍（5） 💬（1）<div>老师好，
对于流处理不是很了解，然后你说的Kafka流处理的两个优点都没有get到，呜呜呜。
1、第一点是更容易实现端到端的正确性。
目前主流的大数据流处理框架都宣称实现了精确一次处理语义，但这是有限定条件的，即它们只能实现框架内的精确一次处理语义，无法实现端到端的。

主流的大数据流处理框架为什么不能实现端到端的精确一次处理语义，什么是端到端的精确一次处理语义呀？

2、它自己对于流式计算的定位。这是在说Kafka流处理相比于其他的更轻量级？
</div>2019-06-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/47/31/f35367c8.jpg" width="30px"><span>小晏子</span> 👍（4） 💬（2）<div>课后思考：我不是特别清楚kafka未来发展方向，不过在老师的提示下我感觉可以让kafka提供扩展接口，用户可以自定义plugin去扩展kafka的功能，kafka只提供核心的消息服务和流处理服务。</div>2020-04-15</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/5c/d7/e4673fde.jpg" width="30px"><span>October</span> 👍（4） 💬（2）<div>看到老师评论区的回复有个问题，kafka目前到底能否实现exactly once的处理语义？</div>2019-06-17</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTJZCkGPSOcvucpfLqRP3aqp3qRpwJKyzjNms4jMwibIkxpjiaszqiazSItCeo3IxqQSFvMDh66XaJ2zw/132" width="30px"><span>JoeyLi666</span> 👍（3） 💬（1）<div>flink支持kafka的端到端 exactly once,不过有一定局限性</div>2019-06-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/cd/39/abe23300.jpg" width="30px"><span>TrumanDu</span> 👍（2） 💬（3）<div>推荐一个kafka监控及管理的平台开源产品 https:&#47;&#47;github.com&#47;xaecbd&#47;KafkaCenter

国人开源，国货之光</div>2020-09-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/6d/1c/d9746372.jpg" width="30px"><span>EricJones</span> 👍（2） 💬（1）<div>学到了，消息引擎系统、分布式流处理平台。
kafka 流处理平台具有的优势：正确性，精确一次处理语义。对流式计算的定位。
理解了精确一次处理语义，但是没get到这其中的点。为什么说正确性是批处理的强项。一批消息传给服务器A，A进行处理然后B服务器从A获取这批消息。这个过程不也是有可能出现消息获取失败，需要第二次去获取吗？该怎么理解框架内流处理与端与端？有大佬可以解释下吗？ 谢谢</div>2019-06-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/d5/3f/80bf4841.jpg" width="30px"><span>文竹</span> 👍（2） 💬（1）<div>目前kafka相关组件太分散以及通过命令行运维，希望有一个平台产品集成所有组件（基础运维，ksql，AI等）</div>2019-06-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/9c/aa/6f780187.jpg" width="30px"><span>言希</span> 👍（2） 💬（1）<div>胡大神，最近生产环境上遇到问题，数据在kafka中积压了一段时间，重新启动消费者后显示加入消费组成功但是一直不消费数据，current-offset一直没变。能帮忙提供排查思路嘛|</div>2019-06-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/64/34/03335c4a.jpg" width="30px"><span>臧萌</span> 👍（2） 💬（1）<div>虽然Kafka的优势是吞吐量，但是我想请教一下latency的问题。对于生产级的硬件（ssd，Linux系统优化，最新cpu，0.1以下的ping），一个Kafka的消息从发出到被收到，合理的latency应该是多少范围内？</div>2019-06-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/37/d0/26975fba.jpg" width="30px"><span>西南偏北</span> 👍（2） 💬（1）<div>作为对比，Spark生态比较完善，flink也在完善批处理，而且两者都对机器学习支持的也比较好，在以后人工智能技术和应用场景越来越成熟的情况下，如果kafka要想持续获得竞争力，是不是也要发力机器学习？</div>2019-06-08</li><br/><li><img src="" width="30px"><span>Geek_fanfan</span> 👍（1） 💬（1）<div>胡老，kafka流处理是像spark一样window机制？</div>2020-05-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/77/88/965e9951.jpg" width="30px"><span>shi.yunlai</span> 👍（1） 💬（2）<div>请教一个问题：基于kafka如何实现同步的请求&#47;响应？（我的第一反应是需要请求和处理双方预先约定好一来一回两个topic）请教夕哥、同时也请各位大牛指点。</div>2020-04-23</li><br/><li><img src="" width="30px"><span>武塘</span> 👍（1） 💬（1）<div>请教下kafka和camel在流处理上的实际区别。理论上来说，kafka是一个有着一定流处理能力的消息引擎，camel是一个ETL的framework，但实际应用在结合一个消息引擎比如ActiveMQ也可以实现流处理，当然这里也可以采用Kafka做消息引擎。我的迷惑是有了kafka，在工程应用中是否可以完全取代camel，还是它们还是有自己适用的不同场景呢？</div>2019-06-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/17/e1/95/29a5cb97.jpg" width="30px"><span>Bitson</span> 👍（1） 💬（1）<div>请问confluence kafka要收费的吗，有没有免费版的？</div>2019-06-16</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/Dj5vm74aAUm94vSrpRlCx2YOHhcufubUA6yJHzcdNw3X7TYwKjpl0kAxfTs9Xcmt0YuIHZu7fHI4mt1mzKs4sw/132" width="30px"><span>demmm</span> 👍（1） 💬（1）<div>消息引擎系统，也是一个分布式流处理平台

想问下这两个概念到底有什么区别呢</div>2019-06-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/4d/10/5c9bc771.jpg" width="30px"><span>懒懒想睡觉</span> 👍（0） 💬（1）<div>我面对的客户往往都不是互联网企业，一台服务器是标配，两台服务器基本没有，多数只有局域网，少部分移动信号都没有，不知道Kafka有何用武之地。</div>2020-12-25</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/17/9d/93/4159edaa.jpg" width="30px"><span>朴素柠檬c</span> 👍（0） 💬（1）<div>作为应用开发，真心吧kafka作为存储系统，异步定时从Kafka中获取数据</div>2020-11-19</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTKT7Exm9wh9wgRBRBhXlLN3l8F2lWPgRVuYHgCgmUPicZGzB7Viackcib1rs2Bj2VS7K6P4ibcDHZDzgA/132" width="30px"><span>Geek_ilryj8</span> 👍（54） 💬（3）<div>推荐大家去搜索一个Confluence的演讲，题目是ETL is dead，其中讲到了Kafka在流处理平台的来龙去脉</div>2019-06-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/3a/96/9fddfb4a.jpg" width="30px"><span>赵鹏举</span> 👍（6） 💬（0）<div>夕哥的英文非常标准，听着语音很舒服</div>2019-07-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/d3/db/5ce5bb26.jpg" width="30px"><span>燕子上</span> 👍（3） 💬（0）<div>还是那句话：Apache Kafka 是消息引擎系统，也是一个分布式流处理平台！主：消息引擎，辅：流处理</div>2019-06-09</li><br/>
</ul>