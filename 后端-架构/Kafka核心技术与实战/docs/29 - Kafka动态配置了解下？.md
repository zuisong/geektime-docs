你好，我是胡夕。今天我要和你讨论的主题是：Kafka的动态Broker参数配置。

## 什么是动态Broker参数配置？

在开始今天的分享之前，我们先来复习一下设置Kafka参数，特别是Broker端参数的方法。

在Kafka安装目录的config路径下，有个server.properties文件。通常情况下，我们会指定这个文件的路径来启动Broker。如果要设置Broker端的任何参数，我们必须在这个文件中显式地增加一行对应的配置，之后启动Broker进程，令参数生效。我们常见的做法是，一次性设置好所有参数之后，再启动Broker。当后面需要变更任何参数时，我们必须重启Broker。但生产环境中的服务器，怎么能随意重启呢？所以，目前修改Broker端参数是非常痛苦的过程。

基于这个痛点，社区于1.1.0版本中正式引入了动态Broker参数（Dynamic Broker Configs）。所谓动态，就是指修改参数值后，无需重启Broker就能立即生效，而之前在server.properties中配置的参数则称为静态参数（Static Configs）。显然，动态调整参数值而无需重启服务，是非常实用的功能。如果你想体验动态Broker参数的话，那就赶快升级到1.1版本吧。
<div><strong>精选留言（19）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/0f/67/f4/9a1feb59.jpg" width="30px"><span>钱</span> 👍（18） 💬（3）<div>请问老师，kafka动态调整配置的实现原理是啥？它怎么做到不需重启broker就能使配置生效的？</div>2019-08-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/48/f3/65c7e3ef.jpg" width="30px"><span>cricket1981</span> 👍（13） 💬（1）<div>follower为什么会拉取副本慢？它不负责读写只专心同步副本数据，增加线程就有用吗？会增加leader负担吗？</div>2019-08-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/19/ab/9b/b12c223d.jpg" width="30px"><span>第一片心意</span> 👍（12） 💬（1）<div>动态更改之后的参数，如果某个broker重启的话，那些动态修改过的参数会失效吧，毕竟broker启动时，会读取 config&#47;server.propertyes 文件的内容。</div>2019-12-16</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/48/f3/65c7e3ef.jpg" width="30px"><span>cricket1981</span> 👍（8） 💬（1）<div>怎样知道什么时候该调整这两组线程池大小？</div>2019-08-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/cd/2a/bdbed6ed.jpg" width="30px"><span>无菇朋友</span> 👍（6） 💬（1）<div>老师 请问下 怎么查看每个broker的请求积压情况？</div>2019-08-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/49/3d/4ac37cc2.jpg" width="30px"><span>外星人</span> 👍（1） 💬（2）<div>您好，我们生产上num.io.threads已经提高到了24，但是对应idle还是在0.3左右，是不是kafkaapi哪个接口处理慢了？这种情况一般如何定位啊？谢谢</div>2019-08-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/49/3d/4ac37cc2.jpg" width="30px"><span>外星人</span> 👍（1） 💬（1）<div>你好，我们用的版本是1.1，请问下，动态参数有没有bug啊？</div>2019-08-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/86/fa/4bcd7365.jpg" width="30px"><span>玉剑冰锋</span> 👍（1） 💬（2）<div>这么看的话，是不是不管是动态参数还是静态参数，集群中的broker配置是可以不一样的对吧？我用0.11（测试环境），环境中三台kafka磁盘容量不一样，导致的问题就是另外两台磁盘已经到了警戒值，剩下那一台磁盘始终用不上，如果可以的话我直接调整一台的保留时间就好了</div>2019-08-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/55/a9/5282a560.jpg" width="30px"><span>yic</span> 👍（0） 💬（2）<div>胡老师，有个问题想请教一下，我们项目想通过广播消息给下游服务。用到了kafka，消费消息的服务每个实例都设置自己的消费组groupId，如：server_prefix_IP_PORT。这样的话，每次服务部署，消费组的groupId都会发生变化。那之前的消费者组信息却还保留在系统中。这样就导致kafka监控时，还能看到老的消费者组相关指标。请问有什么好的方式处理这个问题吗？</div>2021-06-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/b3/53/25a4ae4b.jpg" width="30px"><span>DK</span> 👍（0） 💬（1）<div>胡老师好，我们通过canal将db的数据发送到kafka（kafka_2.11-1.1.1），设置的log.retention.hours=72，保留3天，但是偶尔出现某些topic的partion会删除当天的数据文件导致数据丢失。查看当时的kafka日志
[2021-03-15 11:06:51,824] INFO [Log partition=um.am_gongzhonghao_scene_user-0, dir=&#47;apps&#47;srv&#47;kafka&#47;data] Deleting segments LogSegment(baseOffset=73347921, size=470345801, lastModifiedTime=1615777551000, largestTime=1615518241494) (kafka.log.Log)
发现lastModifiedTime是更新了的，但largestTime没有更新，1615518241494对应的时间为“2021-03-12 11:04:01”，刚好是3天前。不知道这种情况胡老师是否遇到过。</div>2021-05-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/e8/c2/77a413a7.jpg" width="30px"><span>Action</span> 👍（0） 💬（3）<div>老师我进入到zookeepr安装目录，并没有找到您提到的路径，是我安装的版本不对吗？我的安装版本是 zookeeper-3.4.8]
以下是安装目录：
bin          conf     dist-maven       ivy.xml      NOTICE.txt            recipes              zookeeper-3.4.8.jar.asc
build.xml    contrib  docs             lib          README_packaging.txt  src                  zookeeper-3.4.8.jar.md5
CHANGES.txt  data     ivysettings.xml  LICENSE.txt  README.txt </div>2020-06-03</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/99/f0/d9343049.jpg" width="30px"><span>星亦辰</span> 👍（0） 💬（1）<div>请教下老师， confluent_kafka 的类库怎么样获取 consumer 指定group 的offset 值？ 或者有没有其他的办法监控到一个数据队列对于一个group 而言，堆积了多少未处理的数据？</div>2020-01-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/3a/70/a874d69c.jpg" width="30px"><span>Mick</span> 👍（0） 💬（2）<div>老师，请问下在文件系统中是不是看不到 znode路径结构的?我找了半天没找到图上的目录结构。我要怎么才能看到？</div>2019-09-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/3a/70/a874d69c.jpg" width="30px"><span>Mick</span> 👍（0） 💬（1）<div>INFO Got user-level KeeperException when processing sessionid:0x100000400f10000 type:create cxid:0x1 zxid:0x726 txntype:-1 reqpath:n&#47;a Error Path:&#47;consumers Error:KeeperErrorCode = NodeExists for &#47;consumers (org.apache.zookeeper.server.PrepRequestProcessor)
INFO Got user-level KeeperException when processing sessionid:0x100000400f10000 type:create cxid:0x2 zxid:0x727 txntype:-1 reqpath:n&#47;a Error Path:&#47;brokers&#47;ids Error:KeeperErrorCode = NodeExists for &#47;brokers&#47;ids (org.apache.zookeeper.server.PrepRequestProcessor)

INFO Got user-level KeeperException when processing sessionid:0x100000400f10000 type:create cxid:0x3 zxid:0x728 txntype:-1 reqpath:n&#47;a Error Path:&#47;brokers&#47;topics Error:KeeperErrorCode = NodeExists for &#47;brokers&#47;topics (org.apache.zookeeper.server.PrepRequestProcessor)

INFO Got user-level KeeperException when processing sessionid:0x100000400f10000 type:create cxid:0x4 zxid:0x729 txntype:-1 reqpath:n&#47;a Error Path:&#47;config&#47;changes Error:KeeperErrorCode = NodeExists for &#47;config&#47;changes (org.apache.zookeeper.server.PrepRequestProcessor)

INFO Got user-level KeeperException when processing sessionid:0x100000400f10000 type:create cxid:0xb zxid:0x730 txntype:-1 reqpath:n&#47;a Error Path:&#47;config&#47;clients Error:KeeperErrorCode = NodeExists for &#47;config&#47;clients (org.apache.zookeeper.server.PrepRequestProcessor)

INFO Got user-level KeeperException when processing sessionid:0x100000400f10000 type:create cxid:0xc zxid:0x731 txntype:-1 reqpath:n&#47;a Error Path:&#47;config&#47;users Error:KeeperErrorCode = NodeExists for &#47;config&#47;users (org.apache.zookeeper.server.PrepRequestProcessor)

INFO Got user-level KeeperException when processing sessionid:0x100000400f10000 type:create cxid:0xd zxid:0x732 txntype:-1 reqpath:n&#47;a Error Path:&#47;config&#47;brokers Error:KeeperErrorCode = NodeExists for &#47;config&#47;brokers (org.apache.zookeeper.server.PrepRequestProcessor)
老师，请问下启动zk 然后启动kafka后 zk报错 这是什么导致的?</div>2019-09-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/9b/27/f5e29b94.jpg" width="30px"><span>边城</span> 👍（0） 💬（5）<div>您好，动态参数会一直生效吗？是不是需要在 server.properties 里同步维护，防止下次重启时参数失效。
</div>2019-08-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/86/fa/4bcd7365.jpg" width="30px"><span>玉剑冰锋</span> 👍（0） 💬（3）<div>如果可以每台设置不同的日志保存时间，这样的话会导致分区留存时间不一致，消费者消费的问题怎么办？</div>2019-08-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/fd/fd/326be9bb.jpg" width="30px"><span>注定非凡</span> 👍（29） 💬（0）<div>1 诞生背景：
	普通做法是，一次性在server.properties文件中配置好所有参数后，启动Broker。但是在需要变更任何参数后，就必须要重启Broker，这很不方便
	在1.1.0版本中正是引入了动态Broker参数（Dynamic Broker Configs）。
2 概念：
	所谓动态，就是指修改参数值后，无需重启Broker就能立即生效，在server.properties中配置的参数称之为静态参数（Static Configs）。

3 分类：
	read-only:被标记为read-only的参数和原来的参数行为一样，只有重启Broker，才能令修改生效。
	per-broker:被标记为per-broker的参数属于动态参数，修改它之后，只会在对应的Broker上生效。
	cluster-wide:被标记为cluster-wide的参数也属于动态参数，修改它之后，会在整个集群范围内生效。

4 使用场景：
	A ：动态调整Broker端各种线程池大小，实时应对突发流量
	B ：动态调整Broker端连接信息或安全配置信息
	C ：动态更新SSL Keystore有效期
	D ：动态调整Broker端Compact操作性能
	E ：实时变更JMX指示收集器（JMX Metrics Reporter）
5 保存：
 
	A ：首先Kafka将动态Broker参数保存在Zookeeper中
		（1）changes是用来实时监控动态参数变更的，不会保存参数值；
		（2）topic是用来保存Kafka主题级别参数的。
		（3）user和clients是用于动态调整客户端配额（Quota）的znode节点。所谓配额是指Kafka运维人员限制连入集群的客户端的吞吐量或是限定他们的使用CPU资源。

	B ：&#47;config&#47;brokers znode才是真正保存动态Broker参数的地方。该znode下有两大类子节点。
		（1）第一类子节点只有一个，固定叫&lt;default&gt;，保存cluster-wide范围的动态参数
		（2）第二类以Broker.id为名，保存特定Broker的per-broker范围参数。

	C ：参数的优先级别：per-broker参数 &gt; cluster-wide参数 &gt; static参数 &gt; Kafka默认值。

6 如何配置：
	A ：使用Kafka自带的Kafka自带的Kafka-configs脚本。
	如果要设置cluster-wide范围的动态参数，需要显式指定entity-default。
	
	B ：较大几率被动态调整的参值
	（1）：log.retention.ms：修改日志留存时间
	（2）：num.io.threads 和 num.network.threads 
	（3）：与SS相关的参数
		ssl.keystore.type，ssl.keystore.location，ssl.kestore.password和ssl.key.password。允许动态实时调整他们，就能创建过期时间很短的SSL证书，使用新的Keystore，阶段性的调整这组参数，提升安全性。
	（4）：num.replica.fetchers：这个可以增加该参数值，确保有充足的线程可以执行Follower副本向Leader副本的拉取。
	
</div>2019-11-11</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTJkKNKezgVwHxn13elAia7xueLnHAguTrbXcnMmDWWpUsnVWj4iapXWSs4tJGZvL6VotbudUaGSLo6w/132" width="30px"><span>summer</span> 👍（0） 💬（0）<div>老师好，最近在做一个kafka限流功能，网上大部分都是通过命令或者直接修改zk节点的方式来管理配额，看jar包里有cilentQuotaCallback这个类，请问这个类的具体使用的方式是什么了</div>2021-12-02</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/0f/67/1cfb574e.jpg" width="30px"><span>Sunney</span> 👍（0） 💬（0）<div>老师你好，我想咨询一下NATS和Kafka的区别和各自的适用场景是什么？</div>2019-08-09</li><br/>
</ul>