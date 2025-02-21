你好，我是胡夕。今天我要和你分享的主题是：Kafka的运维利器KafkaAdminClient。

## 引入原因

在上一讲中，我向你介绍了Kafka自带的各种命令行脚本，这些脚本使用起来虽然方便，却有一些弊端。

首先，不论是Windows平台，还是Linux平台，命令行的脚本都只能运行在控制台上。如果你想要在应用程序、运维框架或是监控平台中集成它们，会非常得困难。

其次，这些命令行脚本很多都是通过连接ZooKeeper来提供服务的。目前，社区已经越来越不推荐任何工具直连ZooKeeper了，因为这会带来一些潜在的问题，比如这可能会绕过Kafka的安全设置。在专栏前面，我说过kafka-topics脚本连接ZooKeeper时，不会考虑Kafka设置的用户认证机制。也就是说，任何使用该脚本的用户，不论是否具有创建主题的权限，都能成功“跳过”权限检查，强行创建主题。这显然和Kafka运维人员配置权限的初衷背道而驰。

最后，运行这些脚本需要使用Kafka内部的类实现，也就是Kafka**服务器端**的代码。实际上，社区还是希望用户只使用Kafka**客户端**代码，通过现有的请求机制来运维管理集群。这样的话，所有运维操作都能纳入到统一的处理机制下，方便后面的功能演进。
<div><strong>精选留言（25）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/10/26/f9/2a7d80a3.jpg" width="30px"><span>itzzy</span> 👍（15） 💬（5）<div>可视化kafka管理工具，老师能推荐下吗？能支持2.0+版本 感谢！</div>2019-08-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/7b/57/a9b04544.jpg" width="30px"><span>QQ怪</span> 👍（10） 💬（1）<div>想问下老师，在kafka某个topic下不小心创建了多个不用的消费组，怎么删除掉不用的消费组呢？</div>2019-08-15</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/1b/4a/f9df2d06.jpg" width="30px"><span>蒙开强</span> 👍（5） 💬（2）<div>老师，你好，这个只是提供了API是吧，那要是想可视化工具，还得基于它写代码是么</div>2019-08-15</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/47/1b/64262861.jpg" width="30px"><span>胡小禾</span> 👍（2） 💬（1）<div>是不是存在有 高版本的 AdminClient  不能兼容低版本的 broker的问题？

我记得调用 2.x 的 AdminClient API去触发低版本（0.8.x.x）broker的reassign，会报错提示 “这个操作不被支持”</div>2020-05-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/18/18/99/f47bcf7b.jpg" width="30px"><span>Unity</span> 👍（2） 💬（2）<div>老师 请问 org.apache.kafka 的kafka-clients 和 kafka_{scala版本号}这两个jar包的区别是啥 ? </div>2019-08-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/a0/cb/aab3b3e7.jpg" width="30px"><span>张三丰</span> 👍（1） 💬（1）<div>这句话没懂，就算引入了其它两个队列，也无法避免锁阻塞啊，放进新请求队列的时候是一定会存在锁争用的。我完全可以开启一个后台IO线程直接消费新请求的队列，因为新请求队列一定是有序且线程安全的。

为了确保前端主线程不会因为 monitor 锁被阻塞，后端 I&#47;O 线程会定期地将新请求队列中的所有 Call 实例全部搬移到待发送请求队列中进行处理。</div>2020-11-04</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/52/bb/225e70a6.jpg" width="30px"><span>hunterlodge</span> 👍（1） 💬（1）<div>老师，请问怎么采集consumer group的性能指标呢？比如消息堆积数，需要了解到消费应用程序的JMX端口才能采集吗？</div>2019-11-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/be/b9/f2481c2c.jpg" width="30px"><span>诗泽</span> 👍（1） 💬（3）<div>老师可以简单对比一下pulsar 与kafka吗？感觉pulsar 的好多设计都是借鉴kafka的，最大的一个区别是将broker 与数据存储分离，使得broker 可以更加容易扩展。另外，consumer 数量的扩展也不受partition 数量的限制。pulsar 大有取代kafka之势，老师怎么看？</div>2019-08-15</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/fe/b4/295338e7.jpg" width="30px"><span>Allan</span> 👍（0） 💬（2）<div>2.7 看了源码的 增加分区。但是没有看明白逻辑，对于kafka设计的原理不理解导致嘛？就是说为啥里面是这么分配。里面的集合的asList(1, 2),asList(2, 3), asList(3, 1) 表示的是什么意思？第一位是broker嘛？第二位是分区数量？看了半天没整明白？
Increase the partition count for a topic to the given totalCount assigning the new partitions according to the given newAssignments. The length of the given newAssignments should equal totalCount - oldCount, since the assignment of existing partitions are not changed. Each inner list of newAssignments should have a length equal to the topic&#39;s replication factor. The first broker id in each inner list is the &quot;preferred replica&quot;.
For example, suppose a topic currently has a replication factor of 2, and has 3 partitions. The number of partitions can be increased to 6 using a NewPartition constructed like this:
       NewPartitions.increaseTo(6, asList(asList(1, 2),
                                          asList(2, 3),
                                          asList(3, 1)))
       
In this example partition 3&#39;s preferred leader will be broker 1, partition 4&#39;s preferred leader will be broker 2 and partition 5&#39;s preferred leader will be broker 3.
Params:
totalCount – The total number of partitions after the operation succeeds.
newAssignments – The replica assignments for the new partitions.

public static NewPartitions increaseTo(int totalCount, List&lt;List&lt;Integer&gt;&gt; newAssignments) {
        return new NewPartitions(totalCount, newAssignments);
    }</div>2021-04-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/24/55/09/73f24874.jpg" width="30px"><span>建华</span> 👍（0） 💬（1）<div>老师好，用adminclient中的creatacl实现授权好像没有效果，用kafka-acl.sh查不到记录，老师在java代码中怎么动态授权呀</div>2021-01-05</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1a/32/ba/16a12b9e.jpg" width="30px"><span>王晓辉</span> 👍（0） 💬（1）<div>增加分区数
Map&lt;String, NewPartitions&gt; newPartitionsMap = new HashMap&lt;&gt;();
        newPartitionsMap.put(&quot;test-topic&quot;, NewPartitions.increaseTo(13));   &#47;&#47; 增加到x分区，x要比原有分区数大
        CreatePartitionsResult result = adminClient.createPartitions(newPartitionsMap);
        result.all().get();</div>2020-09-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/51/0d/fc1652fe.jpg" width="30px"><span>James</span> 👍（0） 💬（1）<div>之前代码统计分区数好像不太对(代码未测试),修改为以上代码
for (KafkaFuture&lt;TopicDescription&gt; kafkaFuture : kafkaFutures) {
                List&lt;TopicPartitionInfo&gt; topicPartitionInfos = kafkaFuture.get().partitions();
                count += topicPartitionInfos.size();
}</div>2020-07-04</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1c/af/7c/6d90b40a.jpg" width="30px"><span>毛怪</span> 👍（0） 💬（1）<div>老师10版本的kafka怎么可以通过JMX获取指定的监控对象值吗，所有api可以调用吗</div>2020-03-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/07/8a/4bef6202.jpg" width="30px"><span>大叮当</span> 👍（0） 💬（1）<div>请问下，想写个java程序，该程序的功能是传入一个topic，能列出该topic下当前各个parition最小的offset各是多少，请问用哪个类啊，谢谢您。</div>2020-03-06</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/76/f8/66e25be4.jpg" width="30px"><span>maslke</span> 👍（0） 💬（1）<div>手里的开发环境是这样：一台widnows 10的机器，在linux子系统中安装了kafka，在windows中进行AdminClient调用，刚开始连接不上kakfa。后来通过在windows下，调用bat脚本才发现是PCNAME.localdomain这个hostname识别不了。后来通过在hosts进行了一下配置才ok。</div>2019-09-07</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/DYAIOgq83eoPY23R9RRSfBeTJUlyc612VlodjAaWWBNiay9tPydkrd6b9NA8GNibdibnFibTsx94ItHE4jvQwprNzA/132" width="30px"><span>Geek_b809ff</span> 👍（0） 💬（2）<div>老师，请教一下：可视化Kafka管理工具，是Kafka Manager更好还是Kafka Eagle更好，为什么？</div>2019-08-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/76/23/31e5e984.jpg" width="30px"><span>空知</span> 👍（0） 💬（1）<div>老师问下 AdminClient通过Java Object的 wait notify 实现通知机制,这里是 前端主线程进行条件队列吗？是的话 主线程会阻塞吧</div>2019-08-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/62/59/a01a5ddd.jpg" width="30px"><span>ProgramGeek</span> 👍（0） 💬（1）<div>老师，有个问题，如果broker的端口号改变了，消费之前的 topic需要改动哪些参数</div>2019-08-15</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/fd/fd/326be9bb.jpg" width="30px"><span>注定非凡</span> 👍（10） 💬（0）<div>1 引入原因：
	A ：kafka自带的各种命令行脚本都只能运行在控制台上，不便于集成进应用程序或运维框架
	B ：这些命令行脚本很多都是通过连接Zookeeper来提供服务，这存在一些潜在问题，如这可能绕开Kafka的安全设置。
	C ：这些脚本需要使用Kafka内部的类实现，即Kafka服务端的代码。社区希望用户只使用Kafka客户端代码，通过现有的请求机制来运维管理集群。

2 如何使用：
	A ：要想使用，需要在工程中显示的地增加依赖。

3 功能：
	A ：有九大类功能：
	（1）主题管理：包括主题的创建，查询和删除
	（2）权限管理：包括具体权限的配置与删除
	（3）配置参数管理：包括Kafka各种资源的参数设置，详情查询。所谓的kafka资源主要有Broker，主题，用户，Client-id等
	（4）副本日志管理：包括副本底层日志路径的变更和详情查询
	（5）分区管理：即创建额外的主题分区
	（6）消息删除：删除指定位移之前的分区消息
	（7）Delegation Token管理：包括Delegation Token的创建，更新，过期和详情查询
	（8）消费者组管理：包括消费者组的查询，位移查询和删除
	（9）Preferred领导者选举：推选指定主题分区的Preferred Broker为领导者。
4 工作原理
	A ：从设计上来看，AdminClient是一个双线程的设计：前端主线程和后端I&#47;O线程。
	（1）前端线程负责将用户要执行的操作转换成对应的请求，然后将请求发送到后端I&#47;O线程的队列中；
	（2）后端I&#47;O线程从队列中读取相应的请求，然后发送到对应的Broker节点上，之后把执行结果保存起来，以便等待前端线程的获取。
	B ：AdminClient在内部大量使用生产者—消费者模型将请求生产和处理解耦
	C ：前端主线程会创建一个名为Call的请求对象实例。该实例的有两个主要任务
	（1）构建对应的请求对象：如要创建主题，就创建CreateTopicRequest；要查询消费者位移，就创建OffsetFetchRequest
	（2）指定响应的回调逻辑：如Broker端接收到CreateTopicResponse之后要执行的动作。
	（*）一旦创建好Call实例，前端主线程会将其放入到新请求队列（New Call Queue）中，此时，前端主线程的任务就算完成了。他只需要等待结果返回即可。剩下的所有事情都是后端I&#47;O线程的工作了。
	
	D ：后端I&#47;O线程，该线程使用了3个队列来承载不同时期的请求对象，他们分别是新请求队列，待发送请求队列和处理中请求队列。
	（1）使用3个队列的原因：新请求队列的线程安全是有Java的monitor锁来保证的。为了确保前端主线程不会因为monitor锁被阻塞，后端I&#47;O线程会定期地将新请求队列中的所有Call实例全部搬移到待发送请求队列中进行处理。
	（2）待发送请求队列和处理中请求队列只由后端I&#47;O线程处理，因此无需任何锁机制来保证线程安全。
	（3）当I&#47;O线程在处理某个请求时，他会显式的将该请求保存在处理中请求队列。一旦处理完成，I&#47;O线程会自动地调用Call 对象中的回调完成最后的处理。
	（4）最后，I&#47;O线程会通知前端主线程处理完毕，这样前端主线程就能够及时的获取到执行操作的结果。

5 构造和销毁AdminClient实例
	A ：切记它的的完整路径是org.apche.kafka.clients.admin.AdminClient。
	B ：创建AdminClient实例和创建KafkaProducer或KafkaConsumer实例的方法是类似的，你需要手动构造一个Properties对象或Map对象，然后传给对应的方法。

</div>2019-11-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/48/f3/65c7e3ef.jpg" width="30px"><span>cricket1981</span> 👍（1） 💬（0）<div>添加JMX指标以获取 Broker 磁盘占用这块感觉可以提个KIP</div>2019-08-15</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/30/65/18/791d0f5e.jpg" width="30px"><span>Lonely丶浅笑痕y</span> 👍（0） 💬（0）<div>老师，请问kafka-exporter有什么推荐吗？一个消费组如果换了一个topic，怎么删除他与原topic的关系，因为监控上看一只存在对原topic的消费积压</div>2023-12-06</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/51/0d/fc1652fe.jpg" width="30px"><span>James</span> 👍（0） 💬（0）<div> 使用 AdminClient 去增加某个主题的分区,暂时还没有测试
   private void test() throws InterruptedException, ExecutionException, TimeoutException {
        Properties props = new Properties();props.put(AdminClientConfig.BOOTSTRAP_SERVERS_CONFIG, &quot;kafka-host:port&quot;);props.put(&quot;request.timeout.ms&quot;, 600000);
        &#47;&#47;使用 AdminClient 去增加某个主题的分区
        String newTopicName = &quot;test-topic&quot;;
        try (AdminClient client = AdminClient.create(props)) {
            int count = 0;
            DescribeTopicsResult result = client.describeTopics(Arrays.asList(newTopicName));
            Map&lt;String, KafkaFuture&lt;TopicDescription&gt;&gt; kafkaFutureMap = result.values();
            Collection&lt;KafkaFuture&lt;TopicDescription&gt;&gt; kafkaFutures = kafkaFutureMap.values();
            for (KafkaFuture&lt;TopicDescription&gt; kafkaFuture : kafkaFutures) {
                List&lt;TopicPartitionInfo&gt; topicPartitionInfos = kafkaFuture.get().partitions();
                for (TopicPartitionInfo topicPartitionInfo : topicPartitionInfos) {
                    count += topicPartitionInfo.partition();
                }
            }
            &#47;&#47;新增一个分区
            ++count;
            Map&lt;String, NewPartitions&gt; newPartitionsMap = new HashMap&lt;&gt;();
            NewPartitions newPartition = NewPartitions.increaseTo(count);
            newPartitionsMap.put(newTopicName, newPartition);
            client.createPartitions(newPartitionsMap);
        }
    }</div>2020-07-04</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/0b/e6/99183c8d.jpg" width="30px"><span>Subfire</span> 👍（0） 💬（0）<div>👍</div>2019-10-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/76/f8/66e25be4.jpg" width="30px"><span>maslke</span> 👍（0） 💬（0）<div>        Map&lt;String, NewPartitions&gt; newPartitionsMap = new HashMap&lt;&gt;();
        newPartitionsMap.put(topicName, NewPartitions.increaseTo(partitions));
        CreatePartitionsResult createPartitionsResult = client.createPartitions(newPartitionsMap);
        KafkaFuture&lt;Void&gt; future1 = createPartitionsResult.values().get(topicName);
        future1.get();
        System.out.println(&quot;ok&quot;);</div>2019-09-07</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/67/f4/9a1feb59.jpg" width="30px"><span>钱</span> 👍（0） 💬（0）<div>打卡，此节介绍了kafka的运维利器——AdminClient
1：AdminClient 的工作原理？
从设计上来看，AdminClient 是一个双线程的设计：前端主线程和后端 I&#47;O 线程。前端线程负责将用户要执行的操作转换成对应的请求，然后再将请求发送到后端 I&#47;O 线程的队列中；而后端 I&#47;O 线程从队列中读取相应的请求，然后发送到对应的 Broker 节点上，之后把执行结果保存起来，以便等待前端线程的获取。
2：AdminClient的特点？
社区于 0.11 版本正式推出了 Java 客户端版的 AdminClient 工具，该工具提供了几十种运维操作，而且它还在不断地演进着——功能强悍，不断完善中。</div>2019-08-19</li><br/>
</ul>