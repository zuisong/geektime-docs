你好，我是陶辉。

上一讲我们谈到，调低一致性可以提升有状态服务的性能。这一讲我们扩大范围，结合无状态服务，看看怎样提高分布式系统的整体性能。

当你接收到运维系统的短信告警，得知系统性能即将达到瓶颈，或者会议上收到老板兴奋的通知，接下来市场开缰拓土，业务访问量将要上一个大台阶时，一定会马上拿起计算器，算算要加多少台机器，系统才能扛得住新增的流量。

然而，有些服务虽然可以通过加机器提升性能，但可能你加了一倍的服务器，却发现系统的吞吐量没有翻一倍。甚至有些服务无论你如何扩容，性能都没有半点提升。这缘于我们扩展分布式系统的方向发生了错误。

当我们需要分布式系统提供更强的性能时，该怎样扩展系统呢？什么时候该加机器？什么时候该重构代码？扩容时，究竟该选择哈希算法还是最小连接数算法，才能有效提升性能？

在面对Scalability可伸缩性问题时，我们必须有一个系统的方法论，才能应对日益复杂的分布式系统。这一讲我将介绍AKF立方体理论，它定义了扩展系统的3个维度，我们可以综合使用它们来优化性能。

## 如何基于AKF X轴扩展系统？

AKF立方体也叫做[scale cube](https://en.wikipedia.org/wiki/Scale_cube)，它在《The Art of Scalability》一书中被首次提出，旨在提供一个系统化的扩展思路。AKF把系统扩展分为以下三个维度：
<div><strong>精选留言（6）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/11/82/3d/356fc3d6.jpg" width="30px"><span>忆水寒</span> 👍（3） 💬（1）<div>X轴扩展，将单个应用多起几套服务器进行扩展。Y轴扩展，类似于数据库读写分离，均分流量。Z轴扩展，根据地域进行负载均衡。</div>2020-09-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/7f/91/962eba1a.jpg" width="30px"><span>唐朝首都</span> 👍（10） 💬（0）<div>（1）以质数为基数；（2）充分利用key的个性信息</div>2020-06-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/4d/d3/67bdcca9.jpg" width="30px"><span>林铭铭</span> 👍（5） 💬（0）<div>总结下：扩实例，拆功能，拆数据</div>2021-06-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/fe/30/c9b568c3.jpg" width="30px"><span>NullPointer</span> 👍（4） 💬（0）<div>传统单体应用演变Y轴可以理解为逐渐拆解微服务化，Z轴可以理解为为特定服务进行分库分表进一步拆解，代价也逐渐扩大，收益理论上也是对等。</div>2020-06-30</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/64/9b/d1ab239e.jpg" width="30px"><span>J.Smile</span> 👍（1） 💬（0）<div>又来读了一遍。挺有感触的，技术是不断演进的，能用最简单方式解决的问题，就不要用复杂方式，AKF立方体随x,y,z依次增加了复杂度。其中x,y倾向于提升并发性能，而z倾向于克服容量窘境。分布式系统的两大难题也就体现了，高并发与分布式存储，进而引出CAP理论中分布式架构数据存储一致性和可用性的权衡。y轴功能拆分如读写分离需要解决一致性读的问题，x轴水平复制只能是无状态，避免了一致性问题，则重在提升可用性问题。z轴分库分表，既面临拆分之后数据的可用性问题，又面临可用性冗余数据复制带来的一致性问题，更加复杂了。</div>2021-04-05</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/19/c4/35/2cc10d43.jpg" width="30px"><span>Wade_阿伟</span> 👍（0） 💬（0）<div>讲的真好，很有收货</div>2024-06-22</li><br/>
</ul>