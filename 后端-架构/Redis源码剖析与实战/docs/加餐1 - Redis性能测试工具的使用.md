你好，我是蒋德钧。

咱们的课程已经更新过半了，在前面几个模块里，我带你从源码层面，分别了解和学习了Redis的数据结构、事件驱动框架和缓存算法的具体实现过程，相信你现在对Redis的数据类型和运行框架有了更加深入的认识。不过，阅读源码确实是一个比较烧脑的任务，需要你多花些时间钻研。所以，今天这节课，我们就通过加餐，来聊聊相对比较轻松的话题：Redis的性能测试工具。

我们在使用Redis的时候，经常会遇到需要评估Redis性能的场景。比如，当我们需要为部署Redis实例规划服务器配置规格时，或者当需要根据工作负载大小，决定Redis实例个数的时候，我们都需要了解Redis实例的运行性能。

那么这节课，我就来和你聊聊Redis的性能测试工具redis-benchmark，并带你了解下redis-benchmark的使用方法和基本实现。掌握了今天学习的内容之后，你既可以把redis-benchmark用在需要评估Redis性能的场景中，而且你还可以对redis-benchmark进行二次开发，添加新的功能特性，来满足实际业务场景中的需求。

好，下面，我们就先来看看redis-benchmark的使用。
<div><strong>精选留言（5）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/0f/90/8a/288f9f94.jpg" width="30px"><span>Kaito</span> 👍（9） 💬（2）<div>1、redis-benchmark 是 Redis 官方提供的性能测试工具，一般都用这个工具测试其性能

2、测试性能结果，与客户端并发数、value 大小、是否用 pipeline 都有关系

3、除此之外，性能结果还受系统环境的影响，例如 CPU 负载、网络带宽、客户端和服务端是否在同一机器、实例是否部署在虚拟机、Redis 绑核情况都会影响性能结果

4、提升 Redis 性能的几点优化：

- 控制客户端并发数
- value 小于 10KB
- 推荐使用 pipeline
- 隔离部署
- 保证 CPU、网络带宽负载正常
- 不部署在虚拟机
- 进程绑核
- CPU 绑定网卡队列
- Redis 内存碎片
- 不使用 Swap</div>2021-09-04</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/c5/4d/3e75e5f1.jpg" width="30px"><span>命运女神在微笑</span> 👍（2） 💬（1）<div>redislab 提供了一款开源的压测工具，同原生的压测工具相比，加入了线程数的超参数，可以有效的提高redis的负载，在单机的时候就能压的很高。 地址如下 https:&#47;&#47;github.com&#47;RedisLabs&#47;memtier_benchmark</div>2021-09-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/18/c5/71/f7c43b49.jpg" width="30px"><span>风向北吹</span> 👍（0） 💬（0）<div>压测完成后，那些测试数据多久会清理掉呢？</div>2022-10-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/b4/94/2796de72.jpg" width="30px"><span>追风筝的人</span> 👍（0） 💬（0）<div>老师测了下 Redis 集群 主要瓶颈在CPU</div>2022-06-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/b4/94/2796de72.jpg" width="30px"><span>追风筝的人</span> 👍（0） 💬（0）<div>老师  redis-benchmark工具有性能瓶颈， 没有测出系统的系统瓶颈时候，redis-benchmark已经达到cpu瓶颈了，需要开启多个redis-benchmark客户端，测redis集群性能的时候至少开启2个redis-benchmark客户端窗口， 例如  3主3从开启3个redis-benchmark 客户端</div>2022-06-27</li><br/>
</ul>