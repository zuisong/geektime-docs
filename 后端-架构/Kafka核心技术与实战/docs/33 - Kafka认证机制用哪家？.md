你好，我是胡夕。今天我要和你分享的主题是：Kafka的认证机制。

## 什么是认证机制？

所谓认证，又称“验证”“鉴权”，英文是authentication，是指通过一定的手段，完成对用户身份的确认。认证的主要目的是确认当前声称为某种身份的用户确实是所声称的用户。

在计算机领域，经常和认证搞混的一个术语就是授权，英文是authorization。授权一般是指对信息安全或计算机安全相关的资源定义与授予相应的访问权限。

举个简单的例子来区分下两者：认证要解决的是你要证明你是谁的问题，授权要解决的则是你能做什么的问题。

在Kafka中，认证和授权是两套独立的安全配置。我们今天主要讨论Kafka的认证机制，在专栏的下一讲内容中，我们将讨论授权机制。

## Kafka认证机制

自0.9.0.0版本开始，Kafka正式引入了认证机制，用于实现基础的安全用户认证，这是将Kafka上云或进行多租户管理的必要步骤。截止到当前最新的2.3版本，Kafka支持基于SSL和基于SASL的安全认证机制。

**基于SSL的认证主要是指Broker和客户端的双路认证**（2-way authentication）。通常来说，SSL加密（Encryption）已经启用了单向认证，即客户端认证Broker的证书（Certificate）。如果要做SSL认证，那么我们要启用双路认证，也就是说Broker也要认证客户端的证书。
<div><strong>精选留言（28）</strong></div><ul>
<li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/DYAIOgq83eqEacia8yO1dR5Tal9B7w8PzTRrViajlAvDph96OqcuBGe29icbXOibhibGmaBcO7BfpVia0Y8ksZwsuAYQ/132" width="30px"><span>杰洛特</span> 👍（11） 💬（1）<div>老师，请问再java代码里怎么使用认证？比如 producer，是配置好了 conf 文件，然后传入参数吗？
Properties props = new Properties();
props.put(&quot;producer.config&quot;, &quot;&lt;your_path&gt;&#47;producer.conf&quot;);
Producer&lt;String, String&gt; producer = new KafkaProducer&lt;&gt;(props)
类似这样可以吗？</div>2019-12-31</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/4d/49/28e73b9c.jpg" width="30px"><span>明翼</span> 👍（6） 💬（1）<div>老师说的这SCRAM认证用户名和密码直接保存在zookeeper上的，如果zookeeper不做安全控制，岂不是失去意义了？目前我们没有做认证的，研究过一段时间的ssl认证，很麻烦，还影响性能</div>2019-08-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/62/59/a01a5ddd.jpg" width="30px"><span>ProgramGeek</span> 👍（5） 💬（1）<div>老师，对于多个消费者，每个消费者分配的消息数量一样，每个消费者消费完的数据最快和最慢的大概有3s的差距，出现这个消费快慢差距会有哪些原因呢</div>2019-08-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/47/1b/64262861.jpg" width="30px"><span>胡小禾</span> 👍（2） 💬（1）<div>老师的测试中 SCRAM-SHA-256 以及 SCRAM-SHA-512   两个算法都用到了，其实使用其中之一是不是就足够了</div>2021-03-01</li><br/><li><img src="" width="30px"><span>Geek_a8727e</span> 👍（2） 💬（1）<div>kafka broker jaas  文件中admin 用户明文密码，如果别人能看到这个文件，相当于有了管理员的权限，安全性存在很大的风险，这块怎么考虑的</div>2020-11-02</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/0c/c2/bad34a50.jpg" width="30px"><span>张洋</span> 👍（2） 💬（1）<div>老师，我这边认证过后，就可以使用producer 使用 writer 去发送消息了，那是不是相当于也是给 writer授权了呀（发送消息的权限）</div>2020-07-06</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/60/22/92284df2.jpg" width="30px"><span>TeamCC</span> 👍（2） 💬（1）<div>老师你好，我们生产上kafka总是发生leader切换，频率大概和zk fsync的告警日志一致，请问有经验吗？zk隔一段时间会有个fsync慢的告警日志，然后差不多同一个时间点，收到partition leader切换的告警</div>2019-08-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/80/d8/17a5e3ec.jpg" width="30px"><span>花开漫夏</span> 👍（1） 💬（1）<div>请问下老师，认证后java代码如何访问？</div>2020-02-18</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/DYAIOgq83eoCl6Nxf9oW9sDOoibA7p8lKf0jqjPeDszqI4e7iavicQHtbtyibHIhLibyXYAaT02l7GRQvM9BJUxh6yQ/132" width="30px"><span>昀溪</span> 👍（1） 💬（1）<div>老师，您讲的上面的例子中，reader和writer用户只是做了认证，没有做授权，它们默认的权限是什么呢？如果不授权就能收发消息么？</div>2019-10-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/06/a2/350c4af0.jpg" width="30px"><span>知易</span> 👍（1） 💬（2）<div>老师求助，，win10环境
执行命令：
.\bin\windows\kafka-configs.bat --zookeeper localhost:2181 --alter --add-config &#39;SCRAM-SHA-256=[iterations=8192,password=admin],SCRAM-SHA-512=[password=admin]&#39; --ent
ity-type users --entity-name admin
报错如下：
requirement failed: Unknown Dynamic Configuration: Set(&#39;SCRAM-SHA-256).
网上搜了很久，没有找到解决方案，，请老师解惑。感谢</div>2019-08-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/20/de/58/d0c95706.jpg" width="30px"><span>渴望。</span> 👍（0） 💬（1）<div>老师，配置成功启动，出现Connection to node 1(kafka01&#47;192.168.100.101:9092) failed authentication due to : Authentication failed during authentication due to invalid credentials with SASL mechanism SCRAM-SHA-256 (org.apache.kafka.clients.NetworkClient)    这个报错。这是什么原因呢？</div>2021-03-03</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/47/1b/64262861.jpg" width="30px"><span>胡小禾</span> 👍（0） 💬（1）<div>基于 SSL 的认证主要是指 Broker 和客户端的双路认证（2-way authentication）。通常来说，SSL 加密（Encryption）已经启用了单向认证，即客户端认证 Broker 的证书（Certificate）。

---------
这里不是很理解。何谓： SSL 已经启用了单向认证？</div>2021-03-01</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/24/55/09/73f24874.jpg" width="30px"><span>建华</span> 👍（0） 💬（1）<div>是不是用户信息只能建到zookeeper节点上？</div>2020-12-25</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1e/cb/4f/c98fc7f5.jpg" width="30px"><span>李枭冰</span> 👍（0） 💬（2）<div>本低环境用apache kafka配置很简单，但是用cdh反而搞不定，一直说security.inter.broker.protocol can not be set to SASL_PLAINTEXT, as Kerberos is not enabled on this Kafka broker。求帮助。
</div>2020-06-18</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/W2O5VwL8wN6VIGPGCHIBIFuzhwG3Jic5Y90E049bLmxst9L67fhIDUNVlRpVqBfAG3Ykn2Rzl8EFiczWv0IVcLVw/132" width="30px"><span>七步</span> 👍（0） 💬（1）<div>动态增减用户，是否可以使用java api编码调用的方式？</div>2020-04-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/67/05/2e601469.jpg" width="30px"><span>HuAng</span> 👍（0） 💬（3）<div>做了认证后，使用 bin&#47;kafka-topics.sh --create --bootstrap-server localhost:9092 --replication-factor 3 --partitions 3 --topic test 创建主题失败
提示错误：
[2019-12-08 12:20:39,172] INFO [SocketServer brokerId=0] Failed authentication with &#47;127.0.0.1 (Unexpected Kafka request of type METADATA during SASL handshake.) (org.apache.kafka.common.network.Selector)
[2019-12-08 12:20:39,587] INFO [SocketServer brokerId=0] Failed authentication with &#47;127.0.0.1 (Unexpected Kafka request of type METADATA during SASL handshake.) (org.apache.kafka.common.network.Selector)
[2019-12-08 12:20:39,998] INFO [SocketServer brokerId=0] Failed authentication with &#47;127.0.0.1 (Unexpected Kafka request of type METADATA during SASL handshake.) (org.apache.kafka.common.network.Selector)

</div>2019-12-08</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/DYAIOgq83eoCl6Nxf9oW9sDOoibA7p8lKf0jqjPeDszqI4e7iavicQHtbtyibHIhLibyXYAaT02l7GRQvM9BJUxh6yQ/132" width="30px"><span>昀溪</span> 👍（0） 💬（3）<div>顺序是Broker是停止的，然后修改配置文件，创建用户，之后启动Broker。

我是单台环境 2.2.0
Broker server.properties 除了下面的其他都是默认配置

listeners=SASL_PLAINTEXT:&#47;&#47;172.16.247.100:9092
sasl.enabled.mechanisms=SCRAM-SHA-256
sasl.mechanism.inter.broker.protocol=SCRAM-SHA-256
security.inter.broker.protocol=SASL_PLAINTEXT

# 这里我使用的是sasl.jaas.config配置形式，而不是kafka_server_jaas.conf形式
# 官网中http:&#47;&#47;kafka.apache.org&#47;documentation&#47;#security_jaas_broker支持这种配置方式
listener.name.sasl_plaintext.scram-sha-256.sasl.jaas.config=org.apache.kafka.common.security.scram.ScramLoginModule required \
   username=&quot;admin&quot; \
   password=&quot;admin-secret&quot;;

创建admin账号
.&#47;kafka-configs.sh --zookeeper localhost:2181 --alter --add-config \
&#39;SCRAM-SHA-256=[password=admin-secret],SCRAM-SHA-512=[password=admin-secret]&#39; \
--entity-type users --entity-name admin

创建完我再ZK中的 config\users节点可以看到这个用户.

启动后的server.log，日志里kafka成功注册到zk节点
[2019-10-24 10:25:52,210] INFO Registered broker 0 at path &#47;brokers&#47;ids&#47;0 with addresses: ArrayBuffer(EndPoint(172.16.247.100,9092,ListenerName(SASL_PLAINTEXT),SASL_PLAINTEXT)), czxid (broker epoch): 148 (kafka.zk.KafkaZkClient)

[2019-10-24 10:25:52,462] INFO [KafkaServer id=0] started (kafka.server.KafkaServer)
[2019-10-24 10:25:52,582] INFO [SocketServer brokerId=0] Failed authentication with &#47;172.16.247.100 (Authentication failed during authentication due to invalid credentials with SASL mechanism SCRAM-SHA-256) (org.apache.kafka.common.network.Selector)
[2019-10-24 10:25:52,583] INFO [Controller id=0, targetBrokerId=0] Failed authentication with srv01.contoso.com&#47;172.16.247.100 (Authentication failed during authentication due to invalid credentials with SASL mechanism SCRAM-SHA-256) (org.apache.kafka.common.network.Selector)
[2019-10-24 10:25:52,584] ERROR [Controller id=0, targetBrokerId=0] Connection to node 0 (srv01.contoso.com&#47;172.16.247.100:9092) failed authentication due to: Authentication failed during authentication due to invalid credentials with SASL mechanism SCRAM-SHA-256 (org.apache.kafka.clients.NetworkClient)</div>2019-10-24</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/DYAIOgq83eoCl6Nxf9oW9sDOoibA7p8lKf0jqjPeDszqI4e7iavicQHtbtyibHIhLibyXYAaT02l7GRQvM9BJUxh6yQ/132" width="30px"><span>昀溪</span> 👍（0） 💬（2）<div>老师我按上面的方式配置，Kafka起来了，但是日志全是错误
[2019-10-23 14:46:39,465] ERROR [Controller id=0, targetBrokerId=0] Connection to node 0 (srv01.contoso.com&#47;172.16.247.100:9092) failed authentication due to: Authentication failed during authentication due to invalid credentials with SASL mechanism SCRAM-SHA-256 (org.apache.kafka.clients.NetworkClient)
[2019-10-23 14:46:39,578] INFO [SocketServer brokerId=0] Failed authentication with &#47;172.16.247.100 (Authentication failed during authentication due to invalid credentials with SASL mechanism SCRAM-SHA-256) (org.apache.kafka.common.network.Selector)
[2019-10-23 14:46:39,578] INFO [Controller id=0, targetBrokerId=0] Failed authentication with srv01.contoso.com&#47;172.16.247.100 (Authentication failed during authentication due to invalid credentials with SASL mechanism SCRAM-SHA-256) (org.apache.kafka.common.network.Selector)</div>2019-10-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/86/fa/4bcd7365.jpg" width="30px"><span>玉剑冰锋</span> 👍（0） 💬（1）<div>胡老师，kafka平滑升级后面会讲吗？</div>2019-08-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/4d/5e/c5c62933.jpg" width="30px"><span>lmtoo</span> 👍（4） 💬（1）<div>No JAAS configuration section named &#39;Client&#39; was found in specified JAAS configuration file: &#39;&#47;usr&#47;local&#47;kafka&#47;config&#47;kafka-broker.jaas&#39;. Will continue connection to Zookeeper server without SASL authentication, if Zookeeper server allows it.</div>2019-08-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/51/0d/fc1652fe.jpg" width="30px"><span>James</span> 👍（3） 💬（0）<div>还没做过，后续应该会做</div>2019-11-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/67/f4/9a1feb59.jpg" width="30px"><span>钱</span> 👍（3） 💬（0）<div>打卡，中间学习有断档，感觉模式了，学习还是得持续+专注。</div>2019-09-23</li><br/><li><img src="" width="30px"><span>Geek_9150ca</span> 👍（1） 💬（0）<div>老师，您好，我用的也是SASL&#47;SCRAM这种认证方式，可以正常赋权生产消费，但是查询消费者组信息时就会报错，另外配置了jmx-export后，那页面上的消费信息也是看不到，您能给指点下嘛？</div>2021-11-30</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/99/f0/d9343049.jpg" width="30px"><span>星亦辰</span> 👍（1） 💬（0）<div>有没有 哪个大佬  使用 SCRAM-SHA-512 的Python 消费客户端实践？ 
这边实现了好几个版本，总是失败。
</div>2019-12-20</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTJUJKviaecwxpAZCAnHWap86kXUichv5JwUoAtrUNy4ugC0kMMmssFDdyayKFgAoA9Z62sqMZaibbvUg/132" width="30px"><span>Geek_edc612</span> 👍（1） 💬（0）<div>（1）之前做kafak&#47; Sasl-Plain认证，几经转折才发现，这个认证用户跟linux用户名没关系，而且不能动态添加减少用户，最重要的是租户可以自己修改acl权限，目前也只是把客户端的kafka-topics.sh给禁用了，一叶障目吧，=。=；
（2）还有就是sasl-plain这个acl权限感觉肯定，明明给认证用户a赋予了所有topic的在所有host的读写权限，但重启时发现有部分topic突然无法消费写入了，提示没权限，再重启就好了；
（3）接（2）情况，还有就是用kafka-acls.sh去查看topic的所有acl权限时，有的acl完全为空，但是用户a还能写入消费数据，这块完全不懂
（4）目前kafa-acls.sh 只是用的基础的 Write和Read权限，像Cluster这个权限不知道干啥用的，其他的了解也不深入
（5）最后就是做kafka sasl plain 认证的时候给zk也加了认证，具体如下：
zkserver.sh加入这个
&quot;-Djava.security.auth.login.config=&#47;opt&#47;beh&#47;core&#47;zookeeper&#47;conf&#47;kafka_zoo_jaas.conf&quot; \
zoo.cfg加入这个：
authProvider.1=org.apache.zookeeper.server.auth.SASLAuthenticationProvider
requireClientAuthScheme=sasl
jaasLoginRenew=3600000
但是有点疑惑的就是不知道zk 这个认证是用在那块的？我发现加不加kafka sasl plain都能正常用</div>2019-08-19</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTI34ZlT6HSOtJBeTvTvfNLfYECDdJXnHCMj2BHdrRaqRLnZiafnxmKQ2aXoQkW1RLQOyt0tlyzEWIA/132" width="30px"><span>ahu0605</span> 👍（0） 💬（0）<div>https:&#47;&#47;issues.apache.org&#47;jira&#47;browse&#47;KAFKA-4090).
oom</div>2022-06-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/04/0d/3dc5683a.jpg" width="30px"><span>柯察金</span> 👍（0） 💬（0）<div>这个应该用的不多吧</div>2019-11-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/d0/09/7aaed1d8.jpg" width="30px"><span>🤡</span> 👍（0） 💬（0）<div>老胡，看到你的博客园了，什么时候把你的博客地址全分享出来，让大家学习下呗</div>2019-08-23</li><br/>
</ul>