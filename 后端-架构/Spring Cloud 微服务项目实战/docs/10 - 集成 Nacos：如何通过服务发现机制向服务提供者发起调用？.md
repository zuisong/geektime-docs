你好，我是姚秋辰。

在上一课里，我们对coupon-template-serv和coupon-calculation-serv这两个服务做了微服务化改造，通过服务注册流程将它们注册到了Nacos Server。这两个服务是以服务提供者的身份注册的，它们之间不会发生相互调用。为了发起一次完整的服务调用请求，我们还需要构建一个服务消费者去访问Nacos上的已注册服务。

coupon-customer-serv就扮演了服务消费者的角色，它需要调用coupon-template-serv和coupon-calculation-serv完成自己的业务流程。今天我们就来动手改造coupon-customer-serv服务，借助Nacos的服务发现功能从注册中心获取可供调用的服务列表，并发起一个远程服务调用。

通过今天的内容，你可以了解如何使用Webflux发起远程调用，并熟练掌握如何搭建一套基于Nacos的服务治理方案。

## 添加Nacos依赖项和配置信息

在开始写代码之前，你需要将以下依赖项添加到customer-customer-impl子模块的pom.xml文件中。

```
<!-- Nacos服务发现组件 -->
<dependency>
    <groupId>com.alibaba.cloud</groupId>
    <artifactId>spring-cloud-starter-alibaba-nacos-discovery</artifactId>
</dependency>

<!-- 负载均衡组件 -->
<dependency>
    <groupId>org.springframework.cloud</groupId>
    <artifactId>spring-cloud-starter-loadbalancer</artifactId>
</dependency>

<!-- webflux服务调用 -->
<dependency>
    <groupId>org.springframework.boot</groupId>
    <artifactId>spring-boot-starter-webflux</artifactId>
</dependency>    
```

第一个依赖项你一定很熟悉了，它是Nacos服务治理的组件，我们在上一节课程中也添加了同款依赖项到coupon-template-impl和coupon-calculation-impl两个模块。
<div><strong>精选留言（20）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/26/14/85/73e55be5.jpg" width="30px"><span>~</span> 👍（29） 💬（2）<div>回答一下调用链路的问题：
首先在 spring.factory 文件中配置了 NacosDiscoveryClientConfiguration 类，用于 springboot 的初始化时的自动装配。在 NacosDiscoveryClientConfiguration 类中会向 spring 容器中添加  NacosWatch 这个 bean。顺着 NacosWatch 的 start 方法一路往下，就能看到：NacosWatch#start -&gt;NacosNamingService#subscribe -&gt; HostReactor#subscribe -&gt; HostReactor#addTask；UpdateTask 就是作为 task 添加到定时执行队列里的。
</div>2022-01-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/70/0c/53f1d461.jpg" width="30px"><span>Lee KouKuKing</span> 👍（6） 💬（1）<div>【分享】nacos的“订阅者列表”中的多块网卡地址问题，以及应用名为unknown的问题：
customer服务向nacos注册后，在nacos web的“订阅者列表”菜单中，发现订阅者的地址是我的第二块网卡的地址（我在笔记本上装过virtualbox，有一个虚拟网卡。说明：我是在win10上运行了3个nacos进程组成的集群。），并且应用名是：unknown。这样看着很别扭，我就想修改一下，于是在application.yml添加了spring.cloud.nacos.discovery.ip，但是发现不生效。最后通过源码发现在UpdateTask中请求所有服务器列表时：&#47;instance&#47;list，请求的clientIP是这样获取的：
String ip = System.getProperty(&quot;com.alibaba.nacos.client.naming.local.ip&quot;,InetAddress.getLocalHost().getHostAddress()); 
使用System.getProperty获取系统变量，而不是从application.yml中获取，如过获取不到就查找本机的网卡，由于本机有两块网卡，所有就选中了那块虚拟网卡的ip了。
同时&#47;instance&#47;list请求的app参数也是System.getProperty(&quot;project.name&quot;);这样获取的，由于没有获取到&quot;project.name&quot;，所以就默认应用名是：unknown，然后我就在java启动服务加了这俩参数进行解决的。
不只为什么这俩参数不在application.yml中配置呢？这俩参数在application.yml中配置这样多方便呀。
				

java -D&quot;com.alibaba.nacos.client.naming.local.ip&quot;=&quot;192.168.18.8&quot; -D&quot;project.name&quot;=&quot;customer&quot; -jar coupon-customer-impl-1.0-SNAPSHOT.jar</div>2022-02-03</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1d/20/88/41212eb9.jpg" width="30px"><span>Avalon</span> 👍（4） 💬（1）<div>老师，我有两个疑问：
1、为什么依赖注入的是 WebClient.Builder，而不直接注入 WebClient？
2、bodyToMono 的返回值类型 Mono，“Mono”是什么意思？</div>2022-01-04</li><br/><li><img src="" width="30px"><span>Geek_e93c48</span> 👍（4） 💬（1）<div>老师，我发现UpdateTask通过当前类addTask()方法进行任务调度，顺着藤蔓一直摸上去：addTask()-&gt;scheduleUpdateIfAbsent()-&gt;NamingClientProxyDelegate.subscribe()-&gt;NacosNamingService.getAllInstances()-&gt;NamingFactory-&gt;App启动类加载时调用。</div>2022-01-04</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/2c/7e/f1efd18b.jpg" width="30px"><span>摊牌</span> 👍（2） 💬（1）<div>咨询老师个阅读源码的思路与技巧，比如nacos的服务发现，如何从应用的角度追溯到UpdateTask这个类呢，想了解nacos的服务发现底层逻辑，最繁琐的办法是得从头来，搭建nacos的调试环境，下载源码跟踪分析，有没有办法在应用的时候作为切入点去分析局部的底层逻辑呢</div>2023-08-17</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/m7fLWyJrnwEPoIefiaxusQRh6D1Nq7PCXA8RiaxkmzdNEmFARr5q8L4qouKNaziceXia92an8hzYa5MLic6N6cNMEoQ/132" width="30px"><span>alex_lai</span> 👍（2） 💬（3）<div>根据目前项目里的service discovery setup 所有在一个group里的service都可以互相调用? customer service 也可以被另外两个子项目调用？所以nacos有可以设置service topo的相关设置么？
大厂里PP也是有这个专门的architect和team 去review和维护吧</div>2022-01-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/1e/cf/97cd8be1.jpg" width="30px"><span>so long</span> 👍（2） 💬（1）<div>nacos服务发现正向顺藤摸瓜：主要靠NacosWatch实现SmartLifecycle，在spring容器初始化后开始进行服务发现
NacosDiscoveryClientConfiguration-&gt;NacosWatch.start()-&gt;NamingService. subscribe(String serviceName, String groupName, List&lt;String&gt; clusters, EventListener listener)-&gt;HostReactor. subscribe(String serviceName, String clusters, EventListener eventListener)</div>2022-01-05</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/19/fd/58/1af629c7.jpg" width="30px"><span>6点无痛早起学习的和尚</span> 👍（2） 💬（1）<div>2 个问题：
1. 项目 customer 上的注解：@LoadBalancerClient(value = &quot;coupon-template-serv&quot;, configuration = CanaryRuleConfiguration.class)，没有说明是啥作用
2. 运行 customer 这个项目的时候会报错，Access to DialectResolutionInfo cannot be null when &#39;hibernate.dialect&#39; not set，
Google 解决方式：加入spring:jpa:database-platform: org.hibernate.dialect.MySQLDialect</div>2022-01-03</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1f/e0/54/c2a1abbc.jpg" width="30px"><span>王鸿轩</span> 👍（1） 💬（2）<div>老师，以下这段代码似乎有问题（CouponCustomerServiceImpl -&gt; findCoupon）：
Map&lt;Long, CouponTemplateInfo&gt; templateMap = webClientBuilder.build().get()
                .uri(&quot;http:&#47;&#47;coupon-template-serv&#47;template&#47;getBatch?ids=&quot; + templateIds)
                .retrieve()
                .bodyToMono(new ParameterizedTypeReference&lt;Map&lt;Long, CouponTemplateInfo&gt;&gt;() {})
                .block();
好像不能在查询参数上直接拼接一个数组，要转化成xx=1,2,3...这样的形式</div>2022-02-15</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/2c/89/24/4ab4f8c3.jpg" width="30px"><span>Geek_482132</span> 👍（0） 💬（1）<div>想问一下老师，客户端进行服务调用的时候使用的是本地缓存的服务端信息吗，还是再向nacos发送一次请求呢</div>2024-06-03</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/65/d0/b5b00bc2.jpg" width="30px"><span>在路上</span> 👍（0） 💬（1）<div>老师可以聊聊这个吗：通过WebClient非阻塞方式优化性能</div>2023-01-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/28/d9/31/22fc55ea.jpg" width="30px"><span>Believe</span> 👍（0） 💬（1）<div> http:&#47;&#47;coupon-template-serv&#47;template&#47;getBatch?ids=%5B3,%201,%202,%204,%207%5D [DefaultWebClient]
直接拼接参数ids=templateIds 是会出现问题的</div>2022-11-16</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/60/5e/b9624166.jpg" width="30px"><span>被圣光照黑了</span> 👍（0） 💬（2）<div>启动报错了：Spring Cloud LoadBalancer is currently working with the default cache. You can switch to using Caffeine cache, by adding it and org.springframework.cache.caffeine.CaffeineCacheManager to the classpath.的警告。coupon-customer-serv没有注册到nacos里。百度了说引入Caffeine依赖就好，但还是不行</div>2022-01-04</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/19/fd/58/1af629c7.jpg" width="30px"><span>6点无痛早起学习的和尚</span> 👍（0） 💬（1）<div>再加一个问题，类UpdateTask是在HostReactor中，文中应该写错了不是在HostReactive中</div>2022-01-03</li><br/><li><img src="https://wx.qlogo.cn/mmopen/vi_32/DYAIOgq83epUm0LibVnFOia7CN1fj91UyicicIOxib8POPG2dkVIN5IuJJlOQqwJAH4koEEUMoujZKBqzfZIrVmA5wA/132" width="30px"><span>安静的美男子</span> 👍（2） 💬（1）<div>UpdateTask里有一个serviceName，看起来是本机服务名，每个方法也都有这个，那应该只能获取到本机的注册信息才对，不能拿到同分组的其他服务注册信息呀，看了很久没没看懂怎么获取其他服务的？</div>2023-06-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/a7/25/e4535b98.jpg" width="30px"><span>TigerWu</span> 👍（0） 💬（0）<div>我觉得nacos还不够优秀，它背后用的是一个线程去定时维护服务列表的，定时维护延迟相对比较大。如果是订阅模式，当服务器端已更新，客户端立即得到最新服务列表，这个模式会更好一点（就像kafka,客户端一样，topic有消息了，客户端毫秒级响应）。特别是对于交易系统，服务列表更新的延迟要控制在毫秒级内才好。</div>2024-06-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/66/0c/370626c4.jpg" width="30px"><span>IT_matters</span> 👍（0） 💬（0）<div>除了应用启动时会注册一个自己的UpdateTask， 调用其他service时，也会启动一个新的updateTask。

debug可以发现，customer通过webClient调用template服务时，会调用到NacosServiceDiscovery进行服务发现。
</div>2024-01-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/4b/da/c93eaab5.jpg" width="30px"><span>18610296143</span> 👍（0） 💬（0）<div>https:&#47;&#47;space.bilibili.com&#47;1562778141
学完老师Nacos课程之后，录制了几个视频，喜欢的可以看看</div>2023-03-16</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1c/f4/c7/037235c9.jpg" width="30px"><span>kimoti</span> 👍（0） 💬（0）<div>心跳检测机制</div>2022-01-04</li><br/><li><img src="" width="30px"><span>Geek_e93c48</span> 👍（0） 💬（0）<div>UpdateTask通过当前类addTask()方法进行任务调度，顺着藤蔓一直摸上去：addTask()-&gt;scheduleUpdateIfAbsent()-&gt;NamingClientProxyDelegate.subscribe()-&gt;NacosNamingService.getAllInstances()-&gt;NamingFactory-&gt;App启动类加载时调用。</div>2022-01-04</li><br/>
</ul>