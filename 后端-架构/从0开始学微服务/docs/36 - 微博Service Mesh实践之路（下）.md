专栏上一期我们聊到了微博的服务化是如何一步步走向Service Mesh之路的，可以说正是由于微博自身业务对跨语言服务调用的需求日趋强烈，才促使了Weibo Mesh的诞生，也因此乘上了Service Mesh的东风。我在前面讲过，Service Mesh主要由两部分组成，一部分是SideCar，负责服务之间请求的转发；一部分是Control Plane，负责具体的服务治理。从Weibo Mesh的实现方案来看，对应的SideCar采用的是自研的Motan-go Agent，服务治理则是通过统一服务治理中心来实现，这里面的一些思路还是和Control Plane有很大区别的。

今天我们就来聊聊Weibo Mesh实现的技术细节，看看它给业务带来了哪些收益，最后再谈谈Weibo Mesh下一步的发展方向。

## Motan-go Agent

通过上一期的学习，我们知道Weibo Mesh中使用的SideCar就是Motan-go Agent，考虑到Motan-go Agent要与PHP进程部署在一起，为了减少对本机资源的占用，这里Motan-go Agent采用了Go语言来实现，它包含的功能模块请看下图。

![](https://static001.geekbang.org/resource/image/79/2b/79b6ebf400d8d6eb4b390ffc3de6bf2b.png?wh=1830%2A917)

我们拆解一下图中Motan-go Agent主要的模块，看看它们的作用是什么。
<div><strong>精选留言（11）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/12/2c/e7/3c0eba8b.jpg" width="30px"><span>wuhulala</span> 👍（5） 💬（1）<div>service mesh 可不可以理解为把之前的一些封装在服务框架里面的内容 比如复杂均衡 注册 远程通讯 等这些功能 糅合成一个新的agent 以后业务服务只与这个agent交互 ？</div>2018-12-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/a3/ce/12f9d2ae.jpg" width="30px"><span>朱升平</span> 👍（2） 💬（1）<div>weibo mesh这两期还是非常赞的！</div>2018-11-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/fb/3c/fa047695.jpg" width="30px"><span>Geek_70qnwa</span> 👍（1） 💬（1）<div>服务与服务之间的事务怎么控制</div>2018-11-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/6d/45/7e95bd13.jpg" width="30px"><span>小菜鸡</span> 👍（0） 💬（2）<div>想问下老师用Golang写Agent，GC对调用延时带来的的影响大吗</div>2018-11-26</li><br/><li><img src="" width="30px"><span>suke</span> 👍（0） 💬（1）<div>微博不就是各种拉取信息流么，事务应该不多吧</div>2018-11-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/75/9b/611e74ab.jpg" width="30px"><span>技术修行者</span> 👍（9） 💬（0）<div>Service Mesh带来的最大好处是解耦服务和服务框架，服务只需要关注业务逻辑，其他的事情由服务框架通过非侵入的方式实现，将来如果升级或者替换服务框架，成本会非常低。
服务和服务框架解耦的设计，可以
1. 更容易在环境中针对同一个服务维护多个版本，用来做AB测试。
2. 更高效的运维产品环境，对于限流、机房切换等，只需要调整agent的配置，无需修改服务。</div>2019-09-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/f3/00/01137172.jpg" width="30px"><span>Bobo</span> 👍（1） 💬（0）<div>除了分开部署，service mesh和dubbo这种框架的本质区别在哪呢，dubbo客户端不也是代理所有远程调用以及一些服务治理动作的吗</div>2019-01-02</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/20/20/4338bf54.jpg" width="30px"><span>Ilmen</span> 👍（1） 💬（1）<div>请问限流和熔断是怎么做的呢</div>2018-12-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/19/29/67/fc61a741.jpg" width="30px"><span>田小麦</span> 👍（0） 💬（0）<div>没太明白，业务（client）多语言，是怎么和agent交互的？</div>2022-10-14</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTLicryBoLjDicckia0c5bkOoAlYoR2I9NMK8BiaD7HCGxhS1eM9YSfDuUJuZC90uwv9FvHIVSsBoxFgZw/132" width="30px"><span>MwumLi</span> 👍（0） 💬（0）<div>1. Service Mesh 每一个微服务部署的时候是怎么部署的? 是在部署的时候, ops 平台内部把这个微服务和一个 agent 组成一个 pod 运行起来的吗?
2. 微服务每次请求其他服务的时候应该是不关心 agent 的, 那么它是如何做到编码不关心 agent, 而实际运行的时候请求会先到 agent

1. 是通过一个</div>2022-09-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/1f/e7/4007ba43.jpg" width="30px"><span>　　　　　　　　　　　　　</span> 👍（0） 💬（0）<div>老师，您好，有些地方还是不太明白，如果在kubernetes里面，用的istio，这个时候的服务注册和发现是具体怎么实现的呢？如果用kubernetes自身的dns服务发现方式，具体是如何去做服务注册呢？</div>2018-11-18</li><br/>
</ul>