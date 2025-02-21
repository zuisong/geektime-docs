经过前面几期的讲解，你应该已经对微服务的架构有了初步的了解。简单回顾一下，微服务的架构主要包括服务描述、服务发现、服务调用、服务监控、服务追踪以及服务治理这几个基本组件。

那么每个基本组件从架构和代码设计上该如何实现？组件之间又是如何串联来实现一个完整的微服务架构呢？今天我就以开源微服务框架Dubbo为例来给你具体讲解这些组件。

## 服务发布与引用

专栏前面我讲过服务发布与引用的三种常用方式：RESTful API、XML配置以及IDL文件，其中Dubbo框架主要是使用XML配置方式，接下来我通过具体实例，来给你讲讲Dubbo框架服务发布与引用是如何实现的。

首先来看服务发布的过程，下面这段代码是服务提供者的XML配置。

```
<?xml version="1.0" encoding="UTF-8"?>
<beans xmlns="http://www.springframework.org/schema/beans"
    xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
    xmlns:dubbo="http://dubbo.apache.org/schema/dubbo"
    xsi:schemaLocation="http://www.springframework.org/schema/beans        http://www.springframework.org/schema/beans/spring-beans-4.3.xsd        http://dubbo.apache.org/schema/dubbo        http://dubbo.apache.org/schema/dubbo/dubbo.xsd">
 
    <!-- 提供方应用信息，用于计算依赖关系 -->
    <dubbo:application name="hello-world-app"  />
 
    <!-- 使用multicast广播注册中心暴露服务地址 -->
    <dubbo:registry address="multicast://224.5.6.7:1234" />
 
    <!-- 用dubbo协议在20880端口暴露服务 -->
    <dubbo:protocol name="dubbo" port="20880" />
 
    <!-- 声明需要暴露的服务接口 -->
    <dubbo:service interface="com.alibaba.dubbo.demo.DemoService" ref="demoService" />
 
    <!-- 和本地bean一样实现服务 -->
    <bean id="demoService" class="com.alibaba.dubbo.demo.provider.DemoServiceImpl" />
</beans>
```

其中“dubbo:service”开头的配置项声明了服务提供者要发布的接口，“dubbo:protocol”开头的配置项声明了服务提供者要发布的接口的协议以及端口号。

Dubbo会把以上配置项解析成下面的URL格式：

```
dubbo://host-ip:20880/com.alibaba.dubbo.demo.DemoService
```

然后基于[扩展点自适应机制](http://dubbo.incubator.apache.org/zh-cn/docs/dev/SPI.html)，通过URL的“dubbo://”协议头识别，就会调用DubboProtocol的export()方法，打开服务端口20880，就可以把服务demoService暴露到20880端口了。
<div><strong>精选留言（25）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/10/7d/da/780f149e.jpg" width="30px"><span>echo＿陈</span> 👍（17） 💬（1）<div>撸了半年的dubbo源码……
胡老师这篇很不错，已分享给同事</div>2018-09-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/67/0e/c77ad9b1.jpg" width="30px"><span>eason2017</span> 👍（7） 💬（1）<div>这篇文章好哇，学习dunno 必备</div>2018-09-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/67/1d/58425d0b.jpg" width="30px"><span>Home</span> 👍（5） 💬（1）<div>后期会有springcloud的介绍嘛？</div>2018-09-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/46/c0/106d98e7.jpg" width="30px"><span>Sam_Deep_Thinking</span> 👍（3） 💬（1）<div>没玩过，不过看起来doubo很强大哈。学习了。下篇是讲spring cloud吗？</div>2018-09-13</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/PUiby8MibibKcMd88OtDq1c0myEILZjap46fyiaOlML0UlNWzj9NTIEXOhXCCR1tcUibG0I6UoGp59Zj8H5EYwzkY9g/132" width="30px"><span>fldhmily63319</span> 👍（3） 💬（1）<div>老师能评价一下Dubbo, Spring Cloud甚至是ZooKeeper的区别，优劣势吗？</div>2018-09-13</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/DYAIOgq83eqOOrv7cDhjs48zvkq9Ngl90wxXCGKSIbiarmQjYlUZy2ukb0Jh7sANcLziaPWyXcCibueHxR5Mw61ibQ/132" width="30px"><span>小白</span> 👍（1） 💬（1）<div>在微服务架构中，同一个服务是不是有可能既充当服务提供者的角色又充当服务消费者的角色呢？</div>2018-11-03</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/9a/a9/dfea2c50.jpg" width="30px"><span>张龙大骗子</span> 👍（1） 💬（1）<div>neety是个好框架啊，thrift和protobuf也是</div>2018-09-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/57/4f/6fb51ff1.jpg" width="30px"><span>奕</span> 👍（1） 💬（3）<div>现在微服务框架，大部分都是java语言的，其他语言有推荐吗？比如nodejs或者go什么的</div>2018-09-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/55/fe/ab541300.jpg" width="30px"><span>小猪</span> 👍（0） 💬（1）<div>rancher可以用来做微服务框架吗？可以运行微服务系统吗？</div>2018-11-30</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/9e/6e/c4fa7cbc.jpg" width="30px"><span>二师哥</span> 👍（0） 💬（1）<div>就算有有了前面学习的基础, 我依旧无法做到立刻理解. 已经看了三、四遍。
打算看下文档，自己实现以下，然后边学习，边看文档和老胡的文章。</div>2018-09-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/4c/77/98a3f58a.jpg" width="30px"><span>庞小勇</span> 👍（37） 💬（4）<div>php开发者，听着一脸蒙逼</div>2018-09-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/4b/d4/b7719327.jpg" width="30px"><span>波波安</span> 👍（4） 💬（0）<div>老师对怎么去读源码，有什么好的建议和方式吗，每次都不知道从哪看起😬</div>2018-10-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/6c/ea/ce9854a5.jpg" width="30px"><span>坤</span> 👍（2） 💬（0）<div>Dubbo 服务治理相关的组件都是需要客户端自己在代码中选择使用吗？不像ServiceMesh可以独立于业务代码进行流量或服务的治理。</div>2021-03-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/00/45/a1fc2b46.jpg" width="30px"><span>Mr.Right</span> 👍（2） 💬（0）<div>python开发者，听着一脸蒙逼
</div>2019-10-25</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/67/f4/9a1feb59.jpg" width="30px"><span>钱</span> 👍（1） 💬（1）<div>牛逼的Dubbo
牛逼的阿里
牛逼的开源
感谢😊</div>2019-05-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/51/f0/d1142758.jpg" width="30px"><span>Billylin</span> 👍（1） 💬（0）<div>胡老师，您好，如果后端服务使用dubbo框架的话，有什么组件可以充当网关这个角色呢？</div>2018-09-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/7a/d2/4ba67c0c.jpg" width="30px"><span>Sch0ng</span> 👍（0） 💬（0）<div>Dubbo是阿里发布的基于Java语言的开源微服务框架。理解的最佳途径是自己做实验。</div>2021-09-01</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/8e/e0/847348b1.jpg" width="30px"><span>爱学习的大叔</span> 👍（0） 💬（0）<div>不错，对dubbo有两个一个整体上的认识。</div>2020-04-05</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/bd/91/29c2a7fd.jpg" width="30px"><span>lw</span> 👍（0） 💬（0）<div>学了这课，有信心去看dubbo源码了。</div>2019-09-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/8f/2b/c8922696.jpg" width="30px"><span>Geek_jra2hk</span> 👍（0） 💬（1）<div>rpc应该算是长连接吧？如果有多个服务端节点，每次都去通过负载均衡选择，那是在初始化的时候客户端需要跟所有服务端建立连接？求老师赐教</div>2019-09-05</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/e3/02/0c228d1c.jpg" width="30px"><span>Tony</span> 👍（0） 💬（0）<div>代码侵入高，相对于spring cloud
好处是可扩展性强，可定制化，性能优于http协议请求，虽然没玩过dubbo- ̗̀(๑ᵔ⌔ᵔ๑)</div>2019-02-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/7f/f6/32074937.jpg" width="30px"><span>Rainbow</span> 👍（0） 💬（0）<div>我们公司用的就是这一套，开发同学可以小团队做不同的模块，作为测试同学每天 xshell 都要开 n 多个窗口跟踪日志😅，还有就是某个功能出问题以后就要去检查环境，而且有好多个模块，好多个节点，好多个实例，也挺耗费时间的。课程很棒！感谢胡老师分享，看到跟微服务相关特地来学习的，谢谢分享！</div>2018-12-16</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/69/11/831cec7d.jpg" width="30px"><span>小寞子。(≥3≤)</span> 👍（0） 💬（0）<div>对于一个完全第一次听到dubbo这个词的人。我竟然听懂了。。。 理论上没毛病。。通过一系列的层集 来解决和自动化微服务的一系列问题和管理。。。只是看起来会很缓慢的样子。。。😂😂😂😂😂</div>2018-11-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/58/5a/15d1ffda.jpg" width="30px"><span>ctsPrsvrnc</span> 👍（0） 💬（1）<div>胡老师，一直有个疑问，spring cloud出了很久了，dubbo曾经断更过，为什么感觉国内依然还是选择dubbo多？仅仅是因为不依赖spring boot吗？</div>2018-09-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/a7/aa/2a8c15fa.jpg" width="30px"><span>AhianZhang</span> 👍（0） 💬（0）<div>使用 filter 会影响性能</div>2018-09-13</li><br/>
</ul>