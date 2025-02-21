你好，我是文强。

上节课我们分析了RocketMQ在通信协议、网络模块、存储模块、生产者、消费者这五个模块的设计思路。这节课同样还是分析 Kafka 在这五个模块的设计实现。

在学习的过程中，你会发现Kafka和RocketMQ的架构是非常像的，那为什么今天我们还要单独拿出一节课来分析 Kafka 呢？因为它们俩面对的场景是不一样的，一个是消息场景、一个是流场景，所以它们在底层的协议设计、存储模型、消费方式的实现上也是不一样的。而实现的不同，又导致了它们在功能和性能上的表现不一样。

接下来我们就从底层原理的角度来看一下，它们都有哪些异同点。

## Kafka 系统架构

首先来看一下Kafka的架构图。

![](https://static001.geekbang.org/resource/image/39/5a/39d54678ca944b19d2470521dfbec15a.jpg?wh=10666x5048)

如上图所示，Kafka 由 Producer、Broker、ZooKeeper、Consumer 四个模块组成。其中，ZooKeeper 用来存储元数据信息，集群中所有元数据都持久化存储在ZooKeeper 当中。

Kafka有Topic和分区的概念，分区就相当于RocketMQ的MessageQueue。一个Topic可以包含一个或多个分区。消费方面通过Group来组织消费者和分区的关系。

到这你是不是发现了？**Kafka架构和RocketMQ非常像。**从社区信息来看，RocketMQ最初的设计应该参考过Kafka，所以它们的架构和概念非常像，只是在具体实现方式上不太一样。比如概念上分区和MessageQueue的作用是一样的，元数据存储ZooKeeper和NameServer 的作用也是一样的。
<div><strong>精选留言（6）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/12/0c/c2/bad34a50.jpg" width="30px"><span>张洋</span> 👍（3） 💬（2）<div>关于存储模块有一个问题，Kafka为什么每个分区一个文件（逻辑上的会分段），rocketMQ为什么一个Broker所有的queue都在一个commitlog中？
自己想的是Kafka的方式如果分区太多会创建大量的资源，如果FD资源耗尽就会出现问题，所以Rocketmq会支持的分区更多。
还有其他原因吗？</div>2023-07-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/14/5c/f076c170.jpg" width="30px"><span>fc1997</span> 👍（1） 💬（2）<div>想问下，如果kafka一个topic有五个partition然后有三台broker，这种情况下会存在一台broker有三个partition的情况嘛，因为没用过kafka</div>2023-07-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1f/86/17/0afc84df.jpg" width="30px"><span>jackfan</span> 👍（0） 💬（1）<div>有一个疑问 就是客户端寻址，寻的是哪个的地址？是broker的还是topic、分区这些的</div>2023-07-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1a/f3/8d/402e0e0f.jpg" width="30px"><span>林龍</span> 👍（1） 💬（1）<div>看完前面的篇章，我以为kafka是poll的，认为poll = pull + ack ；能够更加详细讲一下poll这个模式吗？</div>2023-07-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/f0/85/6dfb8ac5.jpg" width="30px"><span>开发很忙</span> 👍（0） 💬（1）<div>文中提到，“消费分组模式下，一个分区只能给一个消费者消费，消费是顺序的。”意思是说Kafka不能实现共享消息吗？即消息粒度的负载均衡？</div>2023-09-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/18/04/78/37b46ba6.jpg" width="30px"><span>鲁米</span> 👍（0） 💬（1）<div>消费端的消费分组是出于高可用目的设计么？客户端寻址是怎样动态保持与生产端元数据的一致的呢？</div>2023-08-10</li><br/>
</ul>