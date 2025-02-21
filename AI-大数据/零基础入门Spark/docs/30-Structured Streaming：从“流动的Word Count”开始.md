你好，我是吴磊。

从今天这一讲开始，我们将进入流计算的学习模块。与以往任何时候都不同，今天的大数据处理，对于延迟性的要求越来越高，因此流处理的基本概念与工作原理，是每一个大数据从业者必备的“技能点”。

在这个模块中，按照惯例，我们还是从一个可以迅速上手的实例开始，带你初步认识Spark的流处理框架Structured Streaming。然后，我们再从框架所提供的能力、特性出发，深入介绍Structured Streaming工作原理、最佳实践以及开发注意事项，等等。

在专栏的第一个模块，我们一直围绕着Word Count在打转，也就是通过从文件读取内容，然后以批处理的形式，来学习各式各样的数据处理技巧。而今天这一讲我们换个花样，从一个“流动的Word Count”入手，去学习一下在流计算的框架下，Word Count是怎么做的。

## 环境准备

要上手今天的实例，你只需要拥有Spark本地环境即可，并不需要分布式的物理集群。

不过，咱们需要以“流”的形式，为Spark提供输入数据，因此，要完成今天的实验，我们需要开启两个命令行终端。一个用于启动spark-shell，另一个用于开启Socket端口并输入数据，如下图所示。
<div><strong>精选留言（3）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/20/ba/c6/10448065.jpg" width="30px"><span>东围居士</span> 👍（7） 💬（1）<div>老师，我一直都有个疑惑，Spark Streaming 和 Spark Structured Streaming 有什么区别呢，现在企业里面用哪个更多，如果我们现在要学习的话，是不是只学 Spark Structured Streaming 就可以了？</div>2021-11-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/07/8a/4bef6202.jpg" width="30px"><span>大叮当</span> 👍（6） 💬（2）<div>老师您好，一直有个问题想请请您解惑下。
就是kafka每个主题都有个分区的概念，理论上说，一个消费者组中消费者数目和分区数一致，是效率最高的。
引申到Spark Streaming&#47;Spark Structured Streaming,我的理解：
1、executor数目，和要消费的topic中的分区数目一致，效能最高，不知道这个点我理解对不对。

我的问题是：假设我的场景就是Spark Streaming&#47;Spark Structured Streaming消费kafka解析其中的json数据，然后写入诸如redis,hbase这样的nosql组件。

基于这样的场景，我是不是每个executor只分配1个CPU核就可以了，比如我一个topic有3个partition，那么我指定3个executor（先不考虑driver），每个executor1个cpu核就够了，如果每个executor多个核反而浪费了，用不到？？

恳请老师解惑，谢谢</div>2021-11-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/f9/18/14623fea.jpg" width="30px"><span>blank</span> 👍（1） 💬（0）<div>想问一下老师，_spark_metadata在本地时丢失 不会影响streaming job正常运行，但在azure上，会发生unable to find batch &#47;_spark_metadata&#47;0的情况 这个问题要怎么处理呢。什么情况下metadata文件会丢失呢</div>2022-09-06</li><br/>
</ul>