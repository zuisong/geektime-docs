你好，我是秦晓辉。

上一讲我们了解了 Kafka 监控相关的知识，Kafka 是 Java 组件，主要使用 JMX 的方式采集指标。这一讲我们趁热打铁，介绍另一个Java组件：Elasticsearch（简称 ES ），Elasticsearch直接通过 HTTP 接口暴露指标，相比 Kafka 真是简单太多了。

Elasticsearch 的监控同样包含多个方面，操作系统、JVM 层面的关注点和 Kafka 是一样的，这里不再赘述。我们重点关注 Elasticsearch 本身的指标，它自身的指标有很多，哪些相对更关键呢？这就要从 Elasticsearch 的职能和架构说起了。

## Elasticsearch 的职能和架构

Elasticsearch 的核心职能就是对外提供搜索服务，所以**搜索请求的吞吐和延迟**是非常关键的，搜索是靠底层的索引实现的，所以**索引的性能指标**也非常关键，Elasticsearch 由一个或多个节点组成集群，**集群自身是否健康**也是需要我们监控的。

ElasticSearch 的架构非常简单，一个节点就可以对外提供服务，不过单点的集群显然有容灾问题，如果挂掉了就万事皆休了。一般生产环境，至少搭建一个三节点的集群。

![图片](https://static001.geekbang.org/resource/image/06/01/06dfyy8f73ae4cfe9b2f071ee2646d01.jpg?wh=1500x450 "Elasticsearch架构图")

三个节点分别部署三个 Elasticsearch 进程，这三个进程把 cluster.name 都设置成相同的值，就可以组成一个集群。Elasticsearch 会自动选出一个 master 节点，负责管理集群范围内所有的变更，整个选主过程是自动的，不用我们操心。
<div><strong>精选留言（4）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/10/25/87/f3a69d1b.jpg" width="30px"><span>peter</span> 👍（1） 💬（1）<div>请教老师几个问题：
Q1：文中的例子是生产环境的集群还是自己本机上的虚拟机？
Q2：number_of_nodes&quot; 和&quot;number_of_data_nodes&quot; 有什么区别？
Q3：categraf和ES都能采集OS指标，这两种采集方式会有冲突吗？也就是对同一个OS指标两种方式是不同的值。
Q4：&quot;indices&quot;列出的指标怎么看起来和索引没有什么关系啊。</div>2023-02-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1a/f3/8d/402e0e0f.jpg" width="30px"><span>林龍</span> 👍（0） 💬（1）<div>categraf实战中修改配置后是要重启categraf吗？能不能不通过重启的方式指定配置文件进行部分配置的变更</div>2023-02-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/29/a1/69/0af5e082.jpg" width="30px"><span>顶级心理学家</span> 👍（0） 💬（1）<div>jolokia是否能采集hbase的jmx数据，像kafka一样监控。</div>2023-02-15</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/08/8b/1b7d0463.jpg" width="30px"><span>晴空万里</span> 👍（1） 💬（0）<div>咋一个PromQL都没有?
</div>2023-04-10</li><br/>
</ul>