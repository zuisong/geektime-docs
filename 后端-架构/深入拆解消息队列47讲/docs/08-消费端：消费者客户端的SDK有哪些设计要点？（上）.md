你好，我是文强。上节课我们讲了生产端，这节课我们来讲讲消费端。

从技术上看，消费端SDK和生产端SDK一样，主要包括客户端基础功能和消费相关功能两部分。客户端基础功能在上一节讲过，我们就不再重复。

从实现来看，消费相关功能包括**消费模型**、**分区消费模式**、**消费分组（订阅）**、**消费确认**、**消费失败处理**五个部分。内容比较多，所以本节课我们将会聚焦消费模型的选择和分区消费模式设计这两个部分，下节课会继续完成剩下三个部分的讲解。

## 消费模型的选择

为了满足不同场景的业务需求，从实现机制上来看，主流消息队列一般支持 Pull、Push、Pop 三种消费模型。

### Pull 模型

Pull（拉）模型是指客户端通过不断轮询的方式向服务端拉取数据。它是消息队列中使用最广泛和最基本的模型，主流的消息队列都支持这个模型。

![](https://static001.geekbang.org/resource/image/f8/b9/f8cb7308f06113f96b53bbc1f986d2b9.jpg?wh=10666x3070)

它的好处是客户端根据自身的处理速度去拉取数据，不会对客户端和服务端造成额外的风险和负载压力。缺点是可能会出现大量无效返回的Pull调用，另外消费及时性不够，无法满足一些需要全链路低耗时的场景。

为了提高消费性能，Pull模型都会支持批量读，即**在客户端指定需要拉取多少条数据或者拉取多大的数据**，然后传递给服务端。客户端拉取到数据并处理完成后，再重复拉取数据处理。如前面讲的，这种拉取模式的缺点是可能会出现长时间轮询到空数据的情况，从而浪费通信资源，提高服务端的负载。
<div><strong>精选留言（15）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/12/3c/fa/e2990931.jpg" width="30px"><span>文敦复</span> 👍（3） 💬（1）<div>文中的“因为 Push 模型需要先分配分区和消费者的关系，客户端就需要感知分区分配、分区均衡等操作，从而在客户端就需要实现比较重的逻辑。” 这里的Push模型指的提到的第三种“伪Push模式”吧？</div>2023-07-07</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/3c/fa/e2990931.jpg" width="30px"><span>文敦复</span> 👍（2） 💬（2）<div>文中提到“实现广播消费一般有内核实现广播消费的模型、使用不同的消费分组消费和指定分区消费三种技术思路。”关于最后一种广播消息指定分区进行消费没搞清楚：为什么指定分区消费可以做到广播消费的效果？1个Topic会分成多个分区，所有分区合起来才的整体才是的所有消息？如果客户端指定分区消费不就只能消费其中一部分吗？</div>2023-07-07</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/0a/a4/828a431f.jpg" width="30px"><span>张申傲</span> 👍（1） 💬（1）<div>思考题：当 Topic 的消息写入存在倾斜，某些分区消息堆积很多，此时可以选择【共享消费】模式，给该 Partition 下挂多个 Consumer 来提升消费吞吐量，快速处理掉积压的消息。
小建议：这里【共享消费】这个说法个人感觉有点歧义，容易和【广播消费】产生混淆，是不是叫做【负载均衡消费】更直观一点？</div>2023-07-07</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/aa/0c/6a65f487.jpg" width="30px"><span>cykuo</span> 👍（1） 💬（1）<div>先回答问题：pop模型却可以根据积压情况动态调整消费分区，一定程度上可以解决写入倾斜问题。</div>2023-07-07</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTJIocn8OMjfSGqyeSJEV3ID2rquLR0S6xo0ibdNYQgzicib6L6VlqWjhgxOqD2iaicX1KhbWXWCsmBTskA/132" width="30px"><span>虚竹</span> 👍（0） 💬（2）<div>老师好，关于共享消费模型，或者叫消息粒度负载均衡，假设一个消费者组有 a b c 共3个具体消费者，假设b未返回消费状态，a c是不受影响可以继续往后消费吗？ 这样的话，该消费者组到底消费到队列的哪个位置了是不是就有点乱了？这个问题是怎么解决的呢？</div>2023-10-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1e/f5/97/9a7ee7b3.jpg" width="30px"><span>Geek4329</span> 👍（0） 💬（1）<div>“Pop 模型本质上是 Pull 模型的一种，只是在实现和功能层面上，与 Push 的实现思路和适用场景不一样。”这句话怎么理解呢？前半句讲pop跟pull的关系，后半句又讲pop跟push的关系</div>2023-10-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1f/86/17/0afc84df.jpg" width="30px"><span>jackfan</span> 👍（0） 💬（1）<div>独占是一个分区只能给一个消费者，共享是一个分区的消息给多个消费者，并且一条消息不会给多个消费者，广播是一个消费会被多个消费者消费，灾备也是独占消费。所以这里需要选择共享消费</div>2023-07-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/d0/91/89123507.jpg" width="30px"><span>Johar</span> 👍（0） 💬（1）<div>共享消费模型可以解决分区消息堆积问题</div>2023-07-07</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/DYAIOgq83eoyc6BbcH51u0wCyJWwj6cWrQOqm81nr47dhv0jB0e6vba4qZgK3dVDef108rbibKIPOcPs3RgU2zw/132" width="30px"><span>Geek_f6zh7v</span> 👍（1） 💬（0）<div>pulsar 的 Key_Shared模式。多个消费者，可以保证单个key发送给同一个消费者，保证局部有序。</div>2023-07-11</li><br/><li><img src="" width="30px"><span>Geek_4386bc</span> 👍（0） 💬（0）<div>独占消费那个图是不是画错了，怎么全是partition1</div>2024-08-25</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/28/43/5062a59b.jpg" width="30px"><span>shan</span> 👍（0） 💬（1）<div>1. Pull模型
客户端不断轮询的方式向服务端拉取消息。优点是客户端可以根据自身处理速度区拉取数据，缺点没有消息消费时，可能会出现大量无效的调用。

2. Push模型
指服务端有数据时会主动推送给客户端，一般有Broker内置Push功能、Broker独立实现Push组件、客户端实现伪Push功能。
（1）内置Push功能
在Broker中内置标准的Push功能，服务端想客户端主动推送数据。优点是自带推送功能，不需要重复开发和部署，缺点是消费者很多时，维护较多长链接，引起Broker性能和稳定性。

（2）独立实现Push组件
独立于Broker提供一个专门实现推送功能的组件。优点是独立部署，解决了Broker的性能问题，缺点是本质还是需要从服务端Pull数据再Push给客户端，并且独立部署开发运维成本高。

（3）客户端实现伪Push
客户端内部，底层通过Pull模型先从服务端拉取数据，在通过回调的方式触发回调函数推送消息进行消费，这种方案依旧是Pull模型，需要不断轮询向服务器请求数据。

RocketMQ在5.0之前有Pull和Push两种方式（客户端实现伪Push），对于Pull模式，消费者需要不断向Broker发送拉取消息的请求，拉取消息后会将消息放入一个阻塞队列中，主线程开启循环不断从这个阻塞队列中获取拉取到的消息进行消费。
对于Push模式，本质依旧就是通过Pull的方式拉取数据，只不过不需要开启循环不断从队列中读取数据，而且拉取到消息之后，会触发回调函数进行消息消费，从表面上看就像是Broker主动推送给消费者一样，所以是伪Push。
不管Push模式还是Pull模式，RocketMQ都需要在消费者端进行负载均衡，为消费者分配对应的消息队列，之后才可以向Broker发送请求从队列中拉取消息。

3. Pop模型
Push模型需要在消费者端做负载均衡分配分区&#47;消息队列，如果负载均衡时间过长会影响消费者消费，为了解决这个问题，推出了Pop模型，不再将分区&#47;消息队列与消费者绑定，消费者只需按Pop模型提供的接口去获取消息内容即可，不再感知数据的分布情况。

RocketMQ 5.0的Pop模型，消费者不需要再进行负载均衡，MessageQueue也不与消费者绑定，消费者只需调用服务端提供的接口获取消息进行消费并确认即可，并且Pop模型可以实现消息粒度的分配，在5.0之前只能基于消息队列进行分配。</div>2023-09-23</li><br/><li><img src="" width="30px"><span>TKF</span> 👍（0） 💬（0）<div>老师，文中的广播消费的实现思路部分，“在常见的消息队列产品中，Pulsar 支持的 Share 消费模型就是第一种实现思路。Kafka 和 RocketMQ 主要支持第二和第三种实现思路。”，RocketMQ是第一种思路，Pulsar和Kafka都是第二种思路吧？</div>2023-08-15</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/0c/c2/bad34a50.jpg" width="30px"><span>张洋</span> 👍（0） 💬（0）<div>共享消费、灾备消费都有可能解决：
消费者本身并无问题的情况，使用共享消费，针对于堆积比较严重的分区，增加多个消费者加速消费
如果仅仅是该分区对应的消费者本身出现问题，使用灾备消费，出现问题，及时切换备用消费者去处理。</div>2023-07-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/cb/92/cfc1cfd3.jpg" width="30px"><span>贝氏倭狐猴</span> 👍（0） 💬（0）<div>老师您好，关于pop模型能否深入讲解下，不太明白具体实现方法</div>2023-07-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/aa/0c/6a65f487.jpg" width="30px"><span>cykuo</span> 👍（0） 💬（0）<div>Pop 模型本质上是 Pull 模型的一种，只是在实现和功能层面上，与 Push 的实现思路和适用场景不一样。所以在模型的选择上来看，因为场景复杂，三种模型都是需要的。这句话不是特别的通顺…不知是不是自己理解的有问题</div>2023-07-07</li><br/>
</ul>