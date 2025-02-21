你好，我是胡夕。今天我要和你分享的主题是：如何监控Kafka。

监控Kafka，历来都是个老大难的问题。无论是在我维护的微信公众号，还是Kafka QQ群里面，大家问得最多的问题，一定是Kafka的监控。大家提问的内容看似五花八门，但真正想了解的，其实都是监控这点事，也就是我应该监控什么，怎么监控。那么今天，我们就来详细聊聊这件事。

我个人认为，和头疼医头、脚疼医脚的问题类似，在监控Kafka时，如果我们只监控Broker的话，就难免以偏概全。单个Broker启动的进程虽然属于Kafka应用，但它也是一个普通的Java进程，更是一个操作系统进程。因此，我觉得有必要从Kafka主机、JVM和Kafka集群本身这三个维度进行监控。

## 主机监控

主机级别的监控，往往是揭示线上问题的第一步。**所谓主机监控，指的是监控Kafka集群Broker所在的节点机器的性能**。通常来说，一台主机上运行着各种各样的应用进程，这些进程共同使用主机上的所有硬件资源，比如CPU、内存或磁盘等。

常见的主机监控指标包括但不限于以下几种：

- 机器负载（Load）
- CPU使用率
- 内存使用率，包括空闲内存（Free Memory）和已使用内存（Used Memory）
- 磁盘I/O使用率，包括读使用率和写使用率
- 网络I/O使用率
- TCP连接数
- 打开文件数
- inode使用情况
<div><strong>精选留言（25）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/14/d0/42/6fd01fb9.jpg" width="30px"><span>我已经设置了昵称</span> 👍（16） 💬（1）<div>要怎么看到JMX指标呢，能否讲下</div>2019-09-04</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/7c/b0/0ee17e1b.jpg" width="30px"><span>r</span> 👍（9） 💬（1）<div>老师总结的真好。我有个疑问，没找到相关资料做支撑。就是一套kafka集群，最多能容纳多少个topic-partition，这个是集群规模有关吗，</div>2019-08-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/4e/29/1be3dd40.jpg" width="30px"><span>ykkk88</span> 👍（6） 💬（2）<div>有什么好的开源的监控工具么 </div>2019-08-25</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/17/df/e5/65e37812.jpg" width="30px"><span>快跑</span> 👍（3） 💬（1）<div>请教老师一下
从监控上能看到读取kafka数据是从页缓存还是磁盘么，对应的指标有哪些？</div>2020-03-14</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/W1qXe7yEB8C9fsossNLH59OrNBrEhxnibaMNfKro6YtKyL3thNN3AMyGyme2el0IgzwGpiaycFwwSvKLINITjhzA/132" width="30px"><span>frenco</span> 👍（3） 💬（2）<div>老师好， 请教个问题：    按您之前有个推荐的配置kafka内存的说法，一般堆内存配置6G就好了。 那新生代和老年代默认2：1  分配。      如果只需要6G的内存，  我们生产的机器一般都是64G以上内存， 那机器是不是有很大浪费呢。</div>2019-11-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/c5/a7/cc8764d1.jpg" width="30px"><span>Geek_cd6rkj</span> 👍（3） 💬（2）<div>请教下老师，我们最近遇到一个监控问题，监控各个topic的消息堆积，发现如果业务方由于服务下线，不使用某个consume group了，结果这个group的消息堆积会一直增加，运维就会收到监控告警，但是运维并不好判断哪个group已经不使用了，这个能有什么自动化的手段吗</div>2019-08-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/99/1a/53ed3004.jpg" width="30px"><span>wxr</span> 👍（3） 💬（6）<div>怎样比较好的监控消费延时呢</div>2019-08-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/8f/35/f1839bb2.jpg" width="30px"><span>风中花</span> 👍（2） 💬（1）<div>老师你的公众号怎么找到呢</div>2019-11-30</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTIFrA5ztRGqQTFYIMoBVFgvlhH8GZOCj0K6QLhddcACsugr3BABZdWdSrNobhAWcuEb1W1vS2yicDg/132" width="30px"><span>Geek_72a3d3</span> 👍（2） 💬（4）<div>“同时，Load 值一直在增加，也说明这台主机上的负载越来越大。”
老师，您好，Load值好像是越来越小。？？</div>2019-09-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/49/3d/4ac37cc2.jpg" width="30px"><span>外星人</span> 👍（2） 💬（1）<div>你好，单个topic可以支撑的最多partition个数多少啊？我们生产上有个topic超级大，占了整个集群的一半以上的流量，这种情况是需要拆分吗？</div>2019-08-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/62/30/a8df1a4e.jpg" width="30px"><span>张亮</span> 👍（1） 💬（1）<div>Kafka监控是一个非常专业和体系化的事情，Elasticearch基本将系统指标、JVM指标作为Metric上报出来自闭环非常方便实用，在开源Logi-KafkaManager的时候，我一直计划将这些指标通过JMX直接暴露出来，你怎么看？</div>2021-02-15</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/f1/12/7dac30d6.jpg" width="30px"><span>你为啥那么牛</span> 👍（1） 💬（1）<div>这应该是最有水平的一篇文章了，经验值超高</div>2021-02-07</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/86/d7/33d628b1.jpg" width="30px"><span>夏日</span> 👍（1） 💬（1）<div>ttl一般多少以内比较正常，比如在考虑在双活中心搭建一套kafka集群的时候，怎么判断不会由于节点之间的传输延时导致kafka性能不高？</div>2020-11-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/47/1b/64262861.jpg" width="30px"><span>胡小禾</span> 👍（1） 💬（1）<div>“如果group不使用了，它的状态就是nonactive了”

这个nonactive 在ZK上是不是有节点？</div>2020-05-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/bf/69/dbfd10f7.jpg" width="30px"><span>追光者</span> 👍（1） 💬（3）<div>老师，您好，想请教一个关于  Metricbeat 采集 kafka 数据的问题：
配置好 modules.d&#47;kafka.yml 启动 metricbeat 采集不到数据，提示信息：
2019-08-29T16:13:33.827+0800    INFO    kafka&#47;log.go:53 kafka message: Successful SASL handshake
2019-08-29T16:13:33.828+0800    INFO    kafka&#47;log.go:53 SASL authentication successful with broker 10.162.7.2:9092:4 - [0 0 0 0]
2019-08-29T16:13:33.828+0800    INFO    kafka&#47;log.go:53 Connected to broker at 10.162.7.2:9092 (unregistered)
2019-08-29T16:13:33.832+0800    INFO    kafka&#47;log.go:53 Closed connection to broker 10.162.7.2:9092
system 的可以采集到，请问这是什么原因呀
配置文件：
- module: kafka
metricsets:
- partition
- consumergroup
period: 10s
hosts: [&quot;10.162.3.90:9092&quot;]
client_id: xl
retries: 3
backoff: 250ms
topics: []
username: &quot;admin&quot;
password: &quot;admin&quot;</div>2019-08-30</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/5b/aa/777d7f88.jpg" width="30px"><span>谁谁</span> 👍（0） 💬（1）<div>老师，tps不是应该包括ttl？从客户端发送请求到服务端处理完成返回，文中为什么说tps小而ttl大呢？</div>2021-01-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1a/d2/68/2149f518.jpg" width="30px"><span>Rosy</span> 👍（0） 💬（1）<div>kafka会频繁地删掉broker，导致频繁地切换leader，这是什么情况呢</div>2019-12-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/51/18/0b0c105b.jpg" width="30px"><span>皇甫</span> 👍（0） 💬（1）<div>老师，您好，最近遇到一个实践问题，通过调用kafka manage提供的api获取topic的流入消息数量，有时候有延时，在生产者流量激增的情况下，api不能及时返回消息流入数量，想问下这是什么原因，有啥解决办法吗？谢谢</div>2019-11-04</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/87/0b/6a4cf978.jpg" width="30px"><span>丰富</span> 👍（0） 💬（2）<div>请问老师，kafka支持snmp吗？</div>2019-08-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/67/f4/9a1feb59.jpg" width="30px"><span>钱</span> 👍（7） 💬（1）<div>感觉离开平台自己真的什么都不是，公司内部的监控挺全的，单机的CPU&#47;硬盘&#47;内存&#47;网络&#47;jvm等都有，也有针对方法级别的性能&#47;可用率&#47;调用次数，针对MQ有流入&#47;流出&#47;积压等，这里的每个监控工具都有专门的团队来负责，分工比较细，现在想一想业务开发，如果对业务不精通真是没有什么存在感和价值的。
感觉监控最大的痛点是怎么获取到对应的监控信息，只要能获取监控信息，剩下的就是怎么聚合和汇总展示的问题了。</div>2019-09-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/25/8b/26/d5c68a81.jpg" width="30px"><span>BLESSLH</span> 👍（0） 💬（0）<div>kakfa topic 经常发生leader 为-1的情况，请问应该怎么监控，防止这类问题发生</div>2023-05-15</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/8c/5c/3f164f66.jpg" width="30px"><span>亚林</span> 👍（0） 💬（0）<div>这些指标经验很有用</div>2023-03-14</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTI34ZlT6HSOtJBeTvTvfNLfYECDdJXnHCMj2BHdrRaqRLnZiafnxmKQ2aXoQkW1RLQOyt0tlyzEWIA/132" width="30px"><span>ahu0605</span> 👍（0） 💬（0）<div>胡老师，您对kafka部署k8s中有什么建议吗？</div>2021-11-21</li><br/><li><img src="" width="30px"><span>13761642169</span> 👍（0） 💬（0）<div>确实很经典</div>2019-08-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/4d/fd/0aa0e39f.jpg" width="30px"><span>许童童</span> 👍（0） 💬（0）<div>老师总结得很好，跟着老师一起精进。</div>2019-08-24</li><br/>
</ul>