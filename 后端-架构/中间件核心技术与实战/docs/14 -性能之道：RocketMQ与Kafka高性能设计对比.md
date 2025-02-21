你好，我是丁威。

RocketMQ和Kafka是当下最主流的两款消息中间件，我们这节课就从文件布局、数据写入方式、消息发送客户端这三个维度对比一下实现kafka和RocketMQ的差异，通过这种方式学习高性能编程设计的相关知识。

## 文件布局

我们首先来看一下Kafka与RocketMQ的文件布局。

Kafka 的文件存储设计在宏观上的布局如下图所示：

![图片](https://static001.geekbang.org/resource/image/77/7e/77bd5812f5b3e056d407b38af75d197e.jpg?wh=1920x1026)

我们解析一下它的主要特征。

- 文件的组织方式是“ topic + 分区”，每一个 topic 可以创建多个分区，每一个分区包含单独的文件夹。
- 分区支持副本机制，即一个分区可以在多台机器上复制数据。topic 中每一个分区会有 Leader 与 Follow。**Kafka的内部机制可以保证 topic 某一个分区的 Leader 与Follow 不在同一台机器上，并且每一台Broker 会尽量均衡地承担各个分区的 Leade。**当然，在运行过程中如果Leader不均衡，也可以执行命令进行手动平衡。
- Leader 节点承担一个分区的读写，Follow 节点只负责数据备份。

Kafka 的负载均衡主要取决于分区 Leader 节点的分布情况。分区的 Leader 节点负责读写，而从节点负责数据同步，如果Leader分区所在的Broker节点宕机，会触发主从节点的切换，在剩下的 Follow 节点中选举一个新的 Leader 节点。这时数据的流入流程如下图所示：
<div><strong>精选留言（6）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/20/22/a0/d8631910.jpg" width="30px"><span>Y a n g</span> 👍（2） 💬（1）<div>文件布局：更改commitlog副本为分区维度,充分利用磁盘性能。
数据写入方式：FileChannel调用transferTo而不是wirte，发挥块设备优势
客户端消息发送：加入缓存队列，存储格式的数据组装放在客户端，引入批处理思想
</div>2022-07-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/9f/f6/7431e82e.jpg" width="30px"><span>xueerfei007</span> 👍（0） 💬（1）<div>又来催更了</div>2022-12-15</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/65/d0/b5b00bc2.jpg" width="30px"><span>在路上</span> 👍（0） 💬（1）<div>事务消息方面，老师可以补充下吗</div>2022-11-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/ec/b0/4e22819f.jpg" width="30px"><span>syz</span> 👍（0） 💬（1）<div>老师求助个问题， 在window server 2012下使用RocketMQ，日志清理时会宕机吗，谢谢
问题：历史项目在win下运行，运行一段时间kafka后日志清理时宕机
方案：win中装centos、使用网上kafka补丁版本、换RocketMQ
</div>2022-08-04</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1a/6d/2d/de41f9cf.jpg" width="30px"><span>麻婆豆腐</span> 👍（0） 💬（3）<div>首先文件组织方式可以考虑更多的利用磁盘的IO。
数据写入采用零拷贝。
数据发送可以客户端组织数据来提高吞吐。</div>2022-07-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/ba/e4/6df89add.jpg" width="30px"><span>芋头</span> 👍（0） 💬（0）<div>rocketmq如何通过commitlog构建队列文件的？本文漏了对比消费端的情况</div>2023-05-29</li><br/>
</ul>