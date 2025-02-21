你好，我是吴磊。

在前面的几讲中，咱们不止一次提到，就数据源来说，Kafka是Structured Streaming最重要的Source之一。在工业级的生产系统中，Kafka与Spark这对组合最为常见。因此，掌握Kafka与Spark的集成，对于想从事流计算方向的同学来说，是至关重要的。

今天这一讲，咱们就来结合实例，说一说Spark与Kafka这对“万金油”组合如何使用。随着业务飞速发展，各家公司的集群规模都是有增无减。在集群规模暴涨的情况下，资源利用率逐渐成为大家越来越关注的焦点。毕竟，不管是自建的Data center，还是公有云，每台机器都是真金白银的投入。

## 实例：资源利用率实时计算

咱们今天的实例，就和资源利用率的实时计算有关。具体来说，我们首先需要搜集集群中每台机器的资源（CPU、内存）利用率，并将其写入Kafka。然后，我们使用Spark的Structured Streaming来消费Kafka数据流，并对资源利用率数据做初步的分析与聚合。最后，再通过Structured Streaming，将聚合结果打印到Console、并写回到Kafka，如下图所示。

![图片](https://static001.geekbang.org/resource/image/29/45/2968c988151de68798233229842c7e45.jpg?wh=1920x576 "资源利用率实时计算流程图")

一般来说，在工业级应用中，上图中的每一个圆角矩形，在部署上都是独立的。绿色矩形代表待监测的服务器集群，蓝色矩形表示独立部署的Kafka集群，而红色的Spark集群，也是独立部署的。所谓独立部署，它指的是，集群之间不共享机器资源，如下图所示。
<div><strong>精选留言（1）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/12/66/54/05b7341b.jpg" width="30px"><span>毕务刚</span> 👍（2） 💬（1）<div>老师， 有个需求是利用spark stream读kafka，分析后更新几个 mongodb表， 有几个疑问。

1. 如果利用foreach sink 更新mongodb表， foreach sink 是运行在driver侧， 还是 executor侧,如果是运行在driver侧， 那么并行处理能力是不是很差(没有利用executor的资源)
2. 如果利用 foreachBatch sink 更新mongodb表,  structured-streaming-programming-guide中foreachBatch sink的Fault-tolerant是Depends on the implementation，是不是说 foreachBatch sink 不能利用checkpoint来获得已经处理的offset?
   这种情况下， 如果管理 kafka的offset?</div>2021-12-13</li><br/>
</ul>