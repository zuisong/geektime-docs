你好，我是黄鸿波。

这是推理部署篇的第二节课，学习完在Linux上部署推荐服务后，今天我们沿着推荐服务这条线，继续来讲Kafka相关的内容。

我把本节课分为了下面三大部分。

1. 什么是Kafka。
2. Kafka在推荐系统中的作用和用法。
3. 如何在我们的Service项目中加入Kafka。

## Kafka概述

首先，我们来大概了解一下什么是Kafka。

Kafka是一种基于发布/订阅模式的消息队列系统，它具有高性能、高可靠性和可扩展性等特点。Kafka最初由LinkedIn公司开发，用于解决其大规模数据流的处理和传输问题。今天，Kafka被广泛应用于流处理、实时处理、数据管道、日志聚合等场景中。

Kafka的核心设计思想在于，将消息发送者称为生产者（Producer），将消息接收者称为消费者（Consumer），将消息数据的缓存区称为主题（Topic），并通过多个分区（Partition）来平衡负载和扩展性。

![图片](https://static001.geekbang.org/resource/image/87/7d/87242885040112acca36c819e155757d.png?wh=1678x746)

Kafka的核心组件包括下面五个部分。

**1. Producer**

Producer是消息的生产者，负责向Kafka中发送消息。Producer将消息发布到指定的Topic中，同时负责将消息插入到Topic中指定的Partition中，实现了数据的分区存储。在Kafka中，可以拥有多个Producer向同一个Topic发送消息。
<div><strong>精选留言（2）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/10/25/87/f3a69d1b.jpg" width="30px"><span>peter</span> 👍（0） 💬（1）<div>请教老师几个问题：
Q1：有一个ZMQ，老师知道吗？kafka是独立运行，是个单独的进程。但ZMQ好像不是这样，是一个库，好像只是对socket的一个封装。
Q2：producer和consumer能感受到partition吗？感觉只能用topic这个层次。
Q3：kafka这个软件，需要提供一个库给producer和consumer 
Q4：kafka集群有中心节点吗？如果没有中心节点，是否有数据同步问题？</div>2023-06-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/21/67/fe/5d17661a.jpg" width="30px"><span>悟尘</span> 👍（0） 💬（0）<div>RocketMQ比Kafka更优，且数据丢失率更低，使用起来也更安全，为什么不用RocketMQ呢？像这种涉及到选型方面的内容，能否给我们列举表格进行对比，然后再根据一些平衡最终选定Kafk呢？</div>2023-12-19</li><br/>
</ul>