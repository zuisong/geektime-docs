你好，我是姚秋辰。

今天我们来学习大型微服务系统中高可用性的重要一环：服务容错。通过这节课的内容，你可以了解什么是降级熔断和流量整形，以及它们和服务高可用之间的联系。最后我再带你从架构层面去了解Sentinel服务容错的工作流程，为后面的实战课程做一些理论知识的铺垫。

说到高可用，你也许会不由自主地想到“集群化”。没错，通过搭建服务集群来避免单点故障确实是高可用性保障的常规操作。但是，仅仅搭建集群就能高枕无忧了吗？当面对真正的高可用杀手“服务雪崩”时，即便是集群也会显得脆弱无力。

那么服务雪崩在微服务系统中能引起多大的故障呢？在学习什么是服务容错之前，我们先来了解一下服务容错所要解决的实际问题。

## 什么是服务雪崩？

我来用一个模拟场景带你感受一下服务雪崩的厉害之处。

假设我有一个微服务系统，这个系统内包含了ABCD四个微服务，这四个服务都是以集群模式构建的。我画了一张图用来表示各个服务之间的调用关系。

![](https://static001.geekbang.org/resource/image/be/6b/becfd73ed87c8d1747300b1b79f5d06b.jpg?wh=2000x940)

从上面的图中我们可以看出，服务A会向服务B和服务C发起调用，而服务B和服务C都会去调用服务D。也就是说，服务ABC都直接或间接地依赖服务D完成自己的业务逻辑。

由于服务D底层有数据读写的需求，所以它会对数据库执行CRUD操作。如果开发服务D的程序员学艺不精，写了一段性能比较差的SQL语句，那么一次DB操作的执行时间就会比较长。这在小并发访问量的情况下没有什么问题，不过，一旦并发量堆积了起来，这种性能问题就会被放大。
<div><strong>精选留言（7）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/11/a1/6d/a4ff33bb.jpg" width="30px"><span>Lee</span> 👍（7） 💬（1）<div>限流单机guava的ratelimit 或者分布式下用redis的rratelimit</div>2022-05-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/25/87/f3a69d1b.jpg" width="30px"><span>peter</span> 👍（4） 💬（3）<div>A “降级”和“熔断”都会执行降级逻辑。但对于“降级”，下一次A服务还会调用B服务，只不过失败后再执行降级逻辑，对吗？
B 我对“降级”的理解是“下线某些不重要的服务”，和本篇所讲的“降级”不一样。是不同层次的“降级”吗？
Q2：预热模型两个问题？
A 预热模型是在线上使用的吗？还是上线之前测试用的？
B 对于窗口内的某一个阈值，请求失败后怎么处理？

Q3：Sentinel创建的entry对象是对请求的封装吗？ 还是对要访问的资源的封装？
Q4：为什么叫Slot吗？slot本意是“时隙”，感觉用这个名字不合适？</div>2022-01-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/29/cc/d0/28aa9dbe.jpg" width="30px"><span>子夜</span> 👍（0） 💬（2）<div>有个疑问 限流和熔断降级都是入口处拦截的，假如有两台服务器a，b。a调用b 在b处做限流或熔断降级，无论b的资源是否被占用，a的计算资源都被占用了不是嘛</div>2022-06-30</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1b/a3/4d/59390ba9.jpg" width="30px"><span>排骨</span> 👍（3） 💬（0）<div>Sentinel里面有个DefaultSlotChainBuilderTest单元测试类，可以大概看清楚全流程</div>2023-02-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/2b/ca/97/87f1f07c.jpg" width="30px"><span>罗逸</span> 👍（0） 💬（0）<div>改了git配置，拉下来了，sorry</div>2022-02-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/2b/ca/97/87f1f07c.jpg" width="30px"><span>罗逸</span> 👍（0） 💬（0）<div>服务容错拉不下来 warning: Clone succeeded, but checkout failed. 
sentinel-annotation-quarkus-adapter-deployment 说这个名称过长</div>2022-02-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/c0/ff/9355810e.jpg" width="30px"><span>海布里王力宏</span> 👍（0） 💬（0）<div>能简单介绍一下slot的底层原理实现吗？如何做到即保护了资源又不影响可用性。</div>2022-01-30</li><br/>
</ul>