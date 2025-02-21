你好，我是陈现麟。

在前面的“概述篇”里，我们介绍了分布式技术的来龙去脉，以及在构建一个分布式系统的时候，我们会面临的相关挑战。从这节课开始，我们将一起进入到“分布式技术篇”的学习当中。

在这个专栏里，我们会聚焦日常工作中接触最频繁的分布式在线业务技术。学完这部分内容，相信你会对分布式计算技术心中有数，同时不会迷失于实现的细节中。

当然，分布式计算是个非常大的技术体系，包括 MapReduce 之类的分布式批处理技术，Flink 之类的分布式流计算技术和 Istio 之类的分布式在线业务技术。但是万变不离其宗，我们掌握了分布式计算技术中稳定不变的知识、原理和解决问题的思路，再研究这些技术的时候也会一通百通。

如果直接讨论技术知识和原理，可能会让你觉得非常枯燥和抽象。通过具体的场景案例来讨论技术是非常好的方式，所以我给你虚构了后面这个场景。

假设你是极客时间的一个研发工程师，负责极客时间 App 的后端开发工作。目前极客时间采用的是单体架构，服务端所有的功能、模块都耦合在一个服务里。由于现在用户数据和流量都在快速增长，经常会因为一次小的发布，导致全站都不可用，所以在白天的时候，你都不敢发布服务。

等到时间一长，凌晨流量低峰时的运维慢慢变成常态，你经常收到机器 CPU、内存的报警，但是每一次都很难知道是什么业务功能导致的，只能直接升级机器配置。慢慢的，你发现工作中的问题和挑战越来越多，但是不知道怎么处理。
<div><strong>精选留言（12）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/1b/96/47/93838ff7.jpg" width="30px"><span>青鸟飞鱼</span> 👍（13） 💬（3）<div>老师，redis做服务注册发现，从高可用角度来看其实挺合适的，主从架构足够存储ip、port等信息。</div>2022-01-30</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/0c/f7/d6547adb.jpg" width="30px"><span>努力努力再努力</span> 👍（11） 💬（1）<div>思考题：
互联网中 一个服务的调用流程
1. 客户端 访问域名 -》 DNS （获取对应的ip）-〉 局域网内部路由器 （再获取下一个局域网的ip） -》 一直到服务端 -〉 返回

当然了中间还少了 消息怎么组成 域名的解析过程 等等 但是不是重点
这个流程中 其实DNS 就属于域名-ip的注册中心
猜想：
1. DNS 域名到ip 映射修改是CP （必须成功）
2  各地DNS 自身刷新是 定时更新 （异步）

需要之后实践：
1. 一个信息在多实例上同时生效 ，要通过配置信息来实现，配置信息为什么能实现这个功能 和 区别点是什么？</div>2022-01-28</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTKu71e4qLenzmVZPQe2ZJzt30rKFuBSdfib0UzhAKTicpj74cCRZL4nFGdeMBlfdibiciciby2v9bz6HNkg/132" width="30px"><span>Ricky Gu</span> 👍（9） 💬（1）<div>互联网系统通过DNS 实现服务注册和发现。所以中介存储是DNS。DNS 存在缓存，修改DNS 之后会有生效时间，所以DNS 是最终一致性而不是强一致性系统。同时DNS的可用性几乎是100%的。所以我觉得DNS是AP 系统。</div>2022-02-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/3e/e7/261711a5.jpg" width="30px"><span>blentle</span> 👍（6） 💬（2）<div>老师，有个疑问.如果选择ap作为服务发现中心，网络发生分区时.读到过时的数据，如果刚好那个服务更新后因为网络分区没有来得及更新，比如广告竞价出价服务的价格变更，岂不是比cp服务发现产生更大的灾难.这时候可以容忍调用失败不会损失广告主的利益.</div>2022-01-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/23/bb/a1a61f7c.jpg" width="30px"><span>GAC·DU</span> 👍（4） 💬（1）<div>老师，如何优雅的摘掉一个发生故障的服务，让注册中心处理还是让上游服务调用时发现故障通报注册中心？如果这个服务有十个接口，只有其中的一个接口出了故障，能做到接口级别的隔离吗？

之前在传统的物理机部署服务时利用Etcd来做服务的注册与发现，后来所有的服务都迁移到云原生下部署利用Service来进行服务发现和负载均衡很方便，老师我这个跟进的方向正确吗？

服务注册与发现本质是实现服务的负载均衡，最终的目的还是让整个分布式系统实现高可靠，是AP系统还是CP系统，要看最终的服务用户的忍受度。比如一个量化交易系统CP应该比AP更合适。</div>2022-01-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/b9/3b/7224f3b8.jpg" width="30px"><span>janey</span> 👍（2） 💬（1）<div>老师你好，解释贴合场景非常方便理解，感觉非常赞。业务经验不是很多，在学习本章的时候，单体服务局限在异构负载上的解释不是特别理解，希望能得到答疑：如果说服务里有模块A是IO密集型，模块B是CPU密集型，那么单体部署的时候肯定要同时兼顾IO和CPU；假设我们把这2个模块拆开了，模块A可以部署到一台IO好的机器上，模块B部署到一台CPU好的机器上；现在需要2台机器资源，并且2台机器CPU和IO资源加和不能降，从资源上看的话，收益在哪里呢？</div>2022-07-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/50/fa/48e2acbd.jpg" width="30px"><span>Pikachu</span> 👍（1） 💬（1）<div>一直有个问题想请老师帮忙解惑，使用kubernetes的部署的应用，服务间的访问可以通过k8s的service name进行访问，原理就类似于老师上面提到的，在K8s集群的DNS实现解析，并且集群还可以根据服务的可用状态进行节点加入和摘除。那么这种情况，我理解除了需要访问指定的节点情况以外，其他就已经满足服务注册和发现的机制了，是不是就不需要单独的服务发现中间件了？不知道理解的对不对</div>2022-03-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/f8/ba/d28174a9.jpg" width="30px"><span>Geek_zbvt62</span> 👍（0） 💬（2）<div>个人感觉mysql和redis不适合做注册发现中心的最重要原因不是高可用，而是一致性。Eureka能满足最终一致性。mysql和redis满足不了。</div>2022-04-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/59/91/fa2d8bb2.jpg" width="30px"><span>不吃辣👾</span> 👍（0） 💬（1）<div>老师 假如我一个底层服务部署节点万年不变，迭代周期非常长。这还适合做服务注册发现吗？是否为核心服务，是否需要平滑升级的场景才需要注册发现？注册发现与版本变更有啥区别和联系？</div>2022-03-31</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/59/91/fa2d8bb2.jpg" width="30px"><span>不吃辣👾</span> 👍（0） 💬（1）<div>老师你怎么知道eureka zookeeper etcd redis的高可用存在的问题，哪里可以学习这部分知识？</div>2022-03-31</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/59/91/fa2d8bb2.jpg" width="30px"><span>不吃辣👾</span> 👍（0） 💬（1）<div>当出现网络分区时，Eureka读到过期的数据(服务都搬迁了)，不还是用不了？</div>2022-03-31</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/59/91/fa2d8bb2.jpg" width="30px"><span>不吃辣👾</span> 👍（0） 💬（0）<div>老师我觉得 
1、底层服务部署节点万年不变，迭代周期非常长。
2、网络结构并不不复杂。
的场景是否也应该纳入服务注册作为思考题。</div>2022-03-31</li><br/>
</ul>