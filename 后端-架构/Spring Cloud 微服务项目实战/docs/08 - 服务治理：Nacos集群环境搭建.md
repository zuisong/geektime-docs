你好，我是姚秋辰。

上节课我们对Nacos功能体系有了全面的认识。今天我们就来动手搭建Nacos服务注册中心。通过这节课，你可以知道如何搭建一个高可用的Nacos服务集群，以及如何使用MySQL作为Nacos的底层数据存储方案。这些内容可以帮助你理解什么是“高可用架构”。

我们在做系统架构的时候，首要目标就是保障系统的高可用性。不管你的系统架构多么精妙，用的技术多么先进，如果系统的可用性无法得到保障，那么你做什么都是白忙活。

这就像我们的人生一样，事业、家庭、地位都是0，健康才是一串0前面的那个1，没有1则一切皆无。所以，系统的高可用性，就是系统架构层面的那个1。

保障系统的高可用性有两个大道至简的方向。

- **避免单点故障**：在做系统架构的时候，你应该假设任何服务器都有可能挂掉。如果某项任务依赖单一服务资源，那么这就会成为一个“单点”，一旦这个服务资源挂掉就表示整个功能变为不可用。所以你要尽可能消灭一切“单点”；
- **故障机器状态恢复**：尽快将故障机器返回到故障前的状态。对于像Nacos这类中心化注册中心来说，因故障而下线的机器在重新上线后，应该有能力从某个地方获取故障发生前的服务注册列表。

那Nacos是如何解决上面这两个问题，来保证自己的高可用性的呢？很简单，就是构建服务集群。集群环境不仅可以有效规避单点故障引发的问题，同时对于故障恢复的场景来说，重新上线的机器也可以从集群中的其他节点同步数据信息，恢复到故障前的状态。
<div><strong>精选留言（30）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/1a/80/0b/7ae52ac0.jpg" width="30px"><span>Unknown</span> 👍（37） 💬（2）<div>这边windows本地 搭建的时候，端口不要连续，如果连续的话，在启动时候，会报端口占用 的错误
nacos 中的其他服务会占用相邻的端口grpc</div>2022-02-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/26/14/85/73e55be5.jpg" width="30px"><span>~</span> 👍（3） 💬（4）<div>Intel 的 mac，如果启动 nacos 时候，报错: 「找不到或无法加载主类，原因: java.lang.ClassNotFoundException」，八成是你的 jdk 版本不是 8，可以参照这个博客解决（我是按照方案 2 改动脚本，成功启动）。https:&#47;&#47;blog.csdn.net&#47;shentian885&#47;article&#47;details&#47;120718915
另：老师能否出个加餐讲一下使用 docker 启动的方式，或者指点我一下吗？我根据你之前评论的链接尝试安装却失败了。主要原因我认为有二：1 是我把 MySQL 也通过 docker 安装了，nacos 启动时候会报错找不到 DataSource；2 是我不知道 nacos1 和 nacos2 两个容器之间的 ip 地址改怎么设置，是使用 docker 的「内部 ip（我也不清楚是不是这么叫）」，还是 localhost 直接设置，还是用我本机分配的内网 ip？
还麻烦老师解答一下，谢谢老师！！</div>2022-01-07</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/17/5b/21/02a8d30f.jpg" width="30px"><span>前行</span> 👍（8） 💬（3）<div>windows 环境下单机模拟集群部署，需要注意的是在两个 Nacos Server 的 conf 文件夹下 都配置 cluster.conf 文件，其他配置按照文章来，启动时在两个 Nacos Server 的 bin 文件下执行 .\startup.cmd 即可。</div>2021-12-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/24/ad/2c/250e8aef.jpg" width="30px"><span>Sally Kang 蓝</span> 👍（7） 💬（2）<div>姚老师 我有个问题需要请教。Nacos 2.0.3 集群环境搭建后，假设3个Nacos节点，点击集群管理 -&gt; 节点列表 -&gt; 任意下线某个节点后，该节点没办法重新上线(重新加入集群)。问题: 是Nacos没有提供集群节点上线功能？还是这是一个Bug？还是需要通过参数配置进行设置。</div>2021-12-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/5f/d5/2fec2911.jpg" width="30px"><span>yu</span> 👍（4） 💬（3）<div>Mac M1 历经劫难，终于启动了单机nacos
docker pull zhusaidong&#47;nacos-server-m1:2.0.3

docker run -d -p 8848:8848 -p 9848:9848 -p 9555:9555 --name nacos-server \
-e PREFER_HOST_MODE=hostname \
-e MODE=standalone \
-e SPRING_DATASOURCE_PLATFORM= \
-e MYSQL_SERVICE_HOST=127.0.0.1 \
-e MYSQL_SERVICE_DB_NAME=nacos \
-e MYSQL_SERVICE_PORT=3306 \
-e MYSQL_SERVICE_USER=root \
-e MYSQL_SERVICE_PASSWORD= \
-e MYSQL_SERVICE_DB_PARAM=allowPublicKeyRetrieval=true \
--restart on-failure \
zhusaidong&#47;nacos-server-m1:2.0.3

</div>2022-04-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1f/5e/81/82709d6e.jpg" width="30px"><span>码小呆</span> 👍（3） 💬（1）<div>一次就搭建成功了哇</div>2022-02-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/20/9e/0b/e4d80306.jpg" width="30px"><span>Magic</span> 👍（3） 💬（4）<div>我的是m1芯片，采用老师在评论中回复的镜像搭建的。暂时还没翻车😀
# 拉取适合m1的镜像。
docker pull zhusaidong&#47;nacos-server-m1:2.0.3

# nacos-cluster1
docker run -d \
-e PREFER_HOST_MODE=hostname \
-e MODE=cluster \
-e NACOS_APPLICATION_PORT=8848 \
-e NACOS_SERVERS=&quot;192.168.96.126:8848 192.168.96.126:8948&quot; \
-e SPRING_DATASOURCE_PLATFORM=mysql \
-e MYSQL_SERVICE_HOST=192.168.96.126 \
-e MYSQL_SERVICE_PORT=3306 \
-e MYSQL_SERVICE_USER=root \
-e MYSQL_SERVICE_PASSWORD=123456 \
-e MYSQL_SERVICE_DB_NAME=nacos \
-e NACOS_SERVER_IP=192.168.96.126 \
-p 8848:8848 \
--name my-nacos1 \
zhusaidong&#47;nacos-server-m1:2.0.3

# nacos-cluster2
docker run -d \
-e PREFER_HOST_MODE=hostname \
-e MODE=cluster \
-e NACOS_APPLICATION_PORT=8948 \
-e NACOS_SERVERS=&quot;192.168.96.126:8848 192.168.96.126:8948&quot; \
-e SPRING_DATASOURCE_PLATFORM=mysql \
-e MYSQL_SERVICE_HOST=192.168.96.126 \
-e MYSQL_SERVICE_PORT=3306 \
-e MYSQL_SERVICE_USER=root \
-e MYSQL_SERVICE_PASSWORD=123456 \
-e MYSQL_SERVICE_DB_NAME=nacos \
-e NACOS_SERVER_IP=192.168.96.126 \
-p 8948:8948 \
--name my-nacos2 \
zhusaidong&#47;nacos-server-m1:2.0.3</div>2022-02-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/30/c1/2dde6700.jpg" width="30px"><span>密码123456</span> 👍（3） 💬（1）<div>遇到了一个问题，目录不能用中文，目录不能用中文，目录不能用中文。</div>2022-01-25</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/ed/8e/dc7e2ca6.jpg" width="30px"><span>kernel</span> 👍（3） 💬（2）<div>1、用腾讯云搭建nacos集群，在配置cluster.conf 后，启动，会在配置文件中多了一个
内网IP+端口？这是为什么？
10.0.16.14:8948  --- 这个是启动后自动加上的，对应的IP是腾讯云的内网ip
101.42.237.141:8848
101.42.237.141:8948
2、在idea中起服务，会报这个错误 
failed to req API:&#47;nacos&#47;v1&#47;ns&#47;instance after all servers([101.42.237.141:8848]) tried: ErrCode:400
网上查是说cluster.conf文件中配置了其他nacos时，若其他未启动，则会出现上述报错！是不是那个内网ip+端口导致的？</div>2022-01-18</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/DYAIOgq83er3FAKeM4ZRgicxkChAh7Z9H4zwjiavFw1vQFX50DYn8dYjgP8HVHbmsAA1iaTyJjUz2OvpVU8GekVbg/132" width="30px"><span>Geek_ebdb72</span> 👍（2） 💬（3）<div>我用的docker-compose搭建的但是启动总是报no datasource set 请问有交流群么</div>2022-02-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/40/7e/3f8684a4.jpg" width="30px"><span>wxyz2z</span> 👍（2） 💬（1）<div>m1的mac启动不了，看了日志have &#39;x86_64&#39;, need &#39;arm64e&#39;，请问老师怎么解决</div>2022-01-05</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/21/e2/2b/5eab1490.jpg" width="30px"><span>会飞的鱼</span> 👍（1） 💬（3）<div>不知道为啥，Nacos服务端总是启动失败，控制台、日志都看不出问题来，老师可以帮忙远程看下吗

添加集群机器列表时，用到的IP地址还用到application.properties中配置吗
## 注意，这里的IP不能是localhost或者127.0.0.1
192.168.1.100:8848
192.168.1.100:8948</div>2022-02-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/2a/62/d2/70e414c8.jpg" width="30px"><span>Earthkiid</span> 👍（1） 💬（1）<div>mysql版本太低了也不行，搞了半天一直都无法绑定数据源，后面查看日志才发现是有表没查到，然后才发现应该是导入sql时没注意，只成功建了五六个表，有的语句貌似执行不了？然后升级到5.7再重新来一次就行了。。</div>2022-01-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/17/06/7e/735968e2.jpg" width="30px"><span>西门吹牛</span> 👍（1） 💬（1）<div>Nacos 可以做服务注册中心，可以做配置中心
注册中心以高可用为主(AP)，采用最终一致性协议，和Gossip 不一样，每个节点只负责把自己管理的数据同步给集群中其他节点
做配置中心以一致性为主(CP)，采用强一致性协议，基于raft 实现</div>2022-01-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/24/70/4e7751f3.jpg" width="30px"><span>超级芒果冰</span> 👍（1） 💬（1）<div>nacos在使用集群部署的时候，是不是一定配置外置的mysql数据库，不能使用内置的Derby数据库</div>2022-01-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/0c/9b/0835caf1.jpg" width="30px"><span>大反派</span> 👍（1） 💬（1）<div>怎么用k8s起一个nacos</div>2022-01-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/cf/de/85555a93.jpg" width="30px"><span>_xcc</span> 👍（1） 💬（1）<div>安装个nacos集群也遇到很多错, 最终还是安装好了</div>2021-12-31</li><br/><li><img src="https://static001.geekbang.org/account/avatar/0.png" width="30px"><span>guopop</span> 👍（1） 💬（1）<div>可以docker 集群部署的方案么 和安装包比较呢</div>2021-12-30</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/dc/81/76aceead.jpg" width="30px"><span>塔矢亮的小螃蟹</span> 👍（1） 💬（3）<div>Hello 老师，遇到了一个问题，尝试启动两个nacos的start.sh文件
其中一个能够正常启动，访问nacos控制台
另外一个始终启动失败，查看start.out日志，发现提示Caused by: java.net.BindException: Address already in use
但是lsof-i:端口号没有发现端口被占用，Google了下没有找到有用的解决办法
完整日志没办法贴出来，这是部分error log
org.springframework.context.ApplicationContextException: Unable to start web server; nested exception is org.springframework.boot.web.server.WebServerException: Unable to start embedded Tomcat
Caused by: org.springframework.boot.web.server.WebServerException: Unable to start embedded Tomcat
Caused by: org.springframework.beans.BeanInstantiationException: Failed to instantiate [org.springframework.boot.web.servlet.FilterRegistrationBean]
</div>2021-12-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1d/20/88/41212eb9.jpg" width="30px"><span>Avalon</span> 👍（1） 💬（1）<div>nacos启动日志路径可以修改吗？</div>2021-12-29</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTI8mFt5wSkia3yumk409E65JIlGoreva1Q25icTks0XB0EDC7WJ5V0z6zuvgGkI2Zrh5cBXGS5Hea8A/132" width="30px"><span>OperaX</span> 👍（0） 💬（0）<div>new connection registered successfully, connectionId = 1708954819027_127.0.0.1_50623,connection=Connection{traced=false, abilities=null, metaInfo=ConnectionMeta{connectType=&#39;GRPC&#39;, clientIp=&#39;192.168.0.105&#39;, remoteIp=&#39;127.0.0.1&#39;, remotePort=50623, localPort=9848, version=&#39;Nacos-Java-Client:v2.2.0&#39;, connectionId=&#39;1708954819027_127.0.0.1_50623&#39;, createTime=Mon Feb 26 21:40:19 CST 2024, lastActiveTime=1708954819060, appName=&#39;-&#39;, tenant=&#39;null&#39;, labels={module=naming, source=sdk}}}

nacos.log 显示有注册了，但是控制台看不到服务。。。</div>2024-02-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1a/e7/d5/f4bb9ccf.jpg" width="30px"><span>い北风</span> 👍（0） 💬（2）<div>Caused by: com.alibaba.nacos.api.exception.NacosException: java.net.UnknownHostException: jmenv.tbsite.net
	at com.alibaba.nacos.core.cluster.lookup.AddressServerMemberLookup.run(AddressServerMemberLookup.java:152)
	at com.alibaba.nacos.core.cluster.lookup.AddressServerMemberLookup.doStart(AddressServerMemberLookup.java:100)
	at com.alibaba.nacos.core.cluster.AbstractMemberLookup.start(AbstractMemberLookup.java:55)
	at com.alibaba.nacos.core.cluster.ServerMemberManager.initAndStartLookup(ServerMemberManager.java:237)
	at com.alibaba.nacos.core.cluster.ServerMemberManager.init(ServerMemberManager.java:178)
	at com.alibaba.nacos.core.cluster.ServerMemberManager.&lt;init&gt;(ServerMemberManager.java:158)
	at sun.reflect.NativeConstructorAccessorImpl.newInstance0(Native Method)
	at sun.reflect.NativeConstructorAccessorImpl.newInstance(NativeConstructorAccessorImpl.java:62)
	at sun.reflect.DelegatingConstructorAccessorImpl.newInstance(DelegatingConstructorAccessorImpl.java:45)
	at java.lang.reflect.Constructor.newInstance(Constructor.java:423)
	at org.springframework.beans.BeanUtils.instantiateClass(BeanUtils.java:211)
	... 115 common frames omitted
Caused by: java.net.UnknownHostException: jmenv.tbsite.net
	at java.net.AbstractPlainSocketImpl.connect(AbstractPlainSocketImpl.java:196)
	at java.net.SocksSocketImpl.connect(SocksSocketImpl.java:394)
	at java.net.Socket.connect(Socket.java:606)
	at sun.net.NetworkClient.doConnect(NetworkClient.java:175)
	at sun.net.www.http.HttpClient.openServer(HttpClient.java:499)
	at sun.net.www.http.HttpClient.openServer(HttpClient.java:594)
	at sun.net.www.http.HttpClient.&lt;init&gt;(HttpClient.java:278)
	at sun.net.www.http.HttpClient.New(HttpClient.java:375)
	at sun.net.www.http.HttpClient.New(HttpClient.java:393)
	at sun.net.www.protocol.http.HttpURL</div>2024-01-04</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1a/e7/d5/f4bb9ccf.jpg" width="30px"><span>い北风</span> 👍（0） 💬（1）<div>Mac单机启动正常，集群启动报错 

org.springframework.context.ApplicationContextException: Unable to start web server; nested exception is org.springframework.boot.web.server.WebServerException: Unable to start embedded Tomcat
	at org.springframework.boot.web.servlet.context.ServletWebServerApplicationContext.onRefresh(ServletWebServerApplicationContext.java:165)
	at org.springframework.context.support.AbstractApplicationContext.refresh(AbstractApplicationContext.java:577)
	at org.springframework.boot.web.servlet.context.ServletWebServerApplicationContext.refresh(ServletWebServerApplicationContext.java:147)
	at org.springframework.boot.SpringApplication.refresh(SpringApplication.java:731)
	at org.springframework.boot.SpringApplication.refreshContext(SpringApplication.java:408)
	at org.springframework.boot.SpringApplication.run(SpringApplication.java:307)
	at org.springframework.boot.SpringApplication.run(SpringApplication.java:1303)
	at org.springframework.boot.SpringApplication.run(SpringApplication.java:1292)
	at com.alibaba.nacos.Nacos.main(Nacos.java:48)
	at sun.reflect.NativeMethodAccessorImpl.invoke0(Native Method)
	at sun.reflect.NativeMethodAccessorImpl.invoke(NativeMethodAccessorImpl.java:62)
	at sun.reflect.DelegatingMethodAccessorImpl.invoke(DelegatingMethodAccessorImpl.java:43)
	at java.lang.reflect.Method.invoke(Method.java:498)
	at org.springframework.boot.loader.MainMethodRunner.run(MainMethodRunner.java:49)
	at org.springframework.boot.loader.Launcher.launch(Launcher.java:108)
	at org.springframework.boot.loader.Launcher.launch(Launcher.java:58)
	at org.springframework.boot.loader.PropertiesLauncher.main(PropertiesLauncher.java:467)
Caused by: org.springframework.boot.web.server.WebServerException: Unable to start embedded Tomcat
	at </div>2024-01-04</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/15/bf/1e28e5db.jpg" width="30px"><span>彬彬有礼</span> 👍（0） 💬（1）<div>分别启动cluster1,cluster2,进入cluster1的nacos首页查看集群列表,cluster2的状态为DOWN</div>2023-04-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/28/d8/2b/21bbdcc4.jpg" width="30px"><span>狗蛋。</span> 👍（0） 💬（1）<div>windows安装太麻烦，我用win系统装个虚拟机然后桥接，用ssh连虚拟机当服务器，安装软件全docker,目前安装的很顺</div>2023-04-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/17/14/45/adf079ae.jpg" width="30px"><span>杨松</span> 👍（0） 💬（1）<div>老师请教下：
create schema nacos;和
create database nacos;是一样的吗？</div>2023-03-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/2b/c5/3f/b3a53275.jpg" width="30px"><span>有度</span> 👍（0） 💬（1）<div>win环境下，有兄弟姐妹启动nacos的时候调用的是vm1的ip而不是调用以太网的那个ip地址，搞不懂这东东</div>2023-02-16</li><br/><li><img src="" width="30px"><span>edward</span> 👍（0） 💬（1）<div>老师，请教下，集群模式网上（包括官网）都说至少要3个节点，2个节点会不会有什么问题？</div>2022-12-25</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/ed/3e/c1725237.jpg" width="30px"><span>楚翔style</span> 👍（0） 💬（2）<div>老师,mysql5.1建不了表,怎么升级到最新版呢</div>2022-11-04</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTJlN0AUA3CiaZ48S7icBeQr7t6ZbBeAQQSgCOrELcJWaP3Fg4BSOqiaxGhJSAV9IwlVvj3iaRCVpWf7gA/132" width="30px"><span>Geek_3b8e3f</span> 👍（0） 💬（1）<div>mac 本地启动 nacos 时，单机启动没问题，但是启动集群就会报错，有没有哪位大佬遇到过

Caused by: java.net.UnknownHostException: jmenv.tbsite.net</div>2022-10-16</li><br/>
</ul>