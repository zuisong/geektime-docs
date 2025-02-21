你好，我是徐文浩。

在上节课里，我们已经了解了Kafka的基本架构。不过，对于基于Kafka的流式数据处理，我们还有两个重要的问题没有回答：

- 第一个，Kafka的分布式是如何实现的呢？我们已经看到了Kafka会对数据进行分区，以进行水平扩展。那么，如果我们可以动态添加Broker来增加Kafka集群的吞吐量，这个集群的上下游是怎么知道的呢？
- 第二个，在我们有了Kafka和Storm这样的系统之后，我们的流式处理系统应该怎么搭建呢？我们如何解决可能遇到的各种故障带来的数据不准确的问题呢？

那么，今天这节课，就是要帮助我们回答这两个问题。**一方面**，今天我们会深入来看一下，Kafka是如何随着Broker的增加和减少，协调上下游的Producer和Consumer去收发消息的。**另一方面**，我们会从整个大数据系统的全局视角，来看一下在有了Kafka和Storm这样的利器之后，我们的大数据系统的整体架构应该如何搭建。

## Kafka的分布式系统的实现

首先，Kafka系统并没有一个Master节点。不过，这一点倒是不让人意外，主要是Kafka的整体架构实在太简单了。我们在上一讲就看到了，单个的Broker节点，底层就是一堆顺序读写的文件。而要能够分布式地分摊压力，**只需要用好ZooKeeper** 就好了。
<div><strong>精选留言（8）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/15/66/8f/02be926d.jpg" width="30px"><span>在路上</span> 👍（6） 💬（0）<div>徐老师好，在分布式系统中恰好一次的语义需要两阶段提交的支持，通过协调者记录正在处理哪一条数据，等各个节点确认数据可以被处理之后，在应用处理方案。这个方式最大的问题就是延迟高。如果还需要保持数据处理顺序的话，后面的数据还要排队，吞吐量也受到严重影响。</div>2021-12-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/27/fd/57/b45cc8cd.jpg" width="30px"><span>雨~雨~雨</span> 👍（4） 💬（0）<div>kafka的exactly once的实现，依赖于生产和消费两方面的幂等实现。具体方法有很多，可以依赖kafka自己的消息唯一id，可以自己对consumer的消费逻辑做幂等改造。</div>2022-04-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/8f/60/be0a8805.jpg" width="30px"><span>陈迪</span> 👍（4） 💬（1）<div>至少一次+消费幂等=正好一次。最最基本的分布式系统模型下，一方请求一方响应，请求方没有收到响应，无法分辨请求是否被处理，只能再发，即至少一次</div>2022-01-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/04/30/7f2cb8e3.jpg" width="30px"><span>CRT</span> 👍（2） 💬（0）<div>我自己实现的正好一次，就是在客户端保证的，只能说性能不好保证，而且要用到redis保存已经消费的消息。</div>2022-01-06</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/60/6d/3c2a5143.jpg" width="30px"><span>二进制傻瓜</span> 👍（2） 💬（1）<div>说的是老版本的kafka吧，新版本kafka消费者不依赖zk</div>2021-12-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/20/b7/bdb3bcf0.jpg" width="30px"><span>Eternal</span> 👍（0） 💬（0）<div>首先：消费端，偏移量提交通过自己控制
然后：业务逻辑加上幂等处理
表现为恰好处理了一次</div>2023-04-07</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTKJrOl63enWXCRxN0SoucliclBme0qrRb19ATrWIOIvibKIz8UAuVgicBMibIVUznerHnjotI4dm6ibODA/132" width="30px"><span>Helios</span> 👍（0） 💬（0）<div>kappa架构如果新的storm重放的时候能够保证是正好一次么</div>2022-01-06</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/fb/7b/2d4b38fb.jpg" width="30px"><span>Jialin</span> 👍（0） 💬（0）<div>Kafka 的 Exactly Once 机制可以依赖消费者实现：消费者处理程序保证消息的幂等性（比如说依赖数据库的唯一键或者消息本身的唯一性标示）</div>2021-12-11</li><br/>
</ul>