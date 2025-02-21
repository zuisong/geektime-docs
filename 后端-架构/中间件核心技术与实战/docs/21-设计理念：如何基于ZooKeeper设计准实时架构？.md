你好，我是丁威。

先跟你分享一段我的经历吧。记得我在尝试学习分布式调度框架时，因为我们公司采用的分布式调度框架是ElasticJob，所以我决定以ElasticJob为突破口，通过研读ElasticJob的源码，深入探究定时调度框架的实现原理。

在阅读ElasticJob源码的过程中，它灵活使用ZooKeeper来实现多进程协作的机制让我印象深刻，这里蕴藏着互联网一种通用的架构设计理念，那就是：基于ZooKeeper实现元信息配置管理与实时感知。

上节课中我们也重点提到过，ElasticJob可以实现分布式部署、并且支持数据分片，它同时还支持故障转移机制，其实这一切都是依托ZooKeeper来实现的。

## 基于ZooKeeper的事件通知机制

ElasticJob的架构采取的是去中心化设计，也就是说，ElasticJob在集群部署时，各个节点之间没有主从之分，它们的地位都是平等的。并且，ElasticJob的调度侧重对数据进行分布式处理（也就是数据分片机制），在调度每一个任务之前需要先计算分片信息，然后才能下发给集群内的其他节点来执行。实际部署效果图如下：

![图片](https://static001.geekbang.org/resource/image/7c/25/7cdb21b91a10d1501f49ed7fdee2d925.jpg?wh=1920x646)

在这张图中，order-service-job应用中创建了两个定时任务job-1和job-2，而且order-service-job这个应用部署在两台机器上，也就是说，我们拥有两个调度执行器。那么问题来了，job-1和job-2的分片信息由哪个节点来计算呢？
<div><strong>精选留言（2）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/18/bd/f6/558bb119.jpg" width="30px"><span>ᯤ⁵ᴳ</span> 👍（0） 💬（1）<div>快结课了，希望老师也讲讲分库分表的中间件</div>2022-08-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/55/bf/d442b55e.jpg" width="30px"><span>mikewt</span> 👍（0） 💬（2）<div>老师 watch机制其实可以用客户端主动轮询来解决，那么这两者有啥区别吗，使用场景是什么</div>2022-08-10</li><br/>
</ul>