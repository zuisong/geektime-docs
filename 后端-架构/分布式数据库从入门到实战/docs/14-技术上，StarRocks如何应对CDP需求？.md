你好，我是彭旭。

上一讲我们分析了CDP的业务场景，CDP从各个渠道收集用户业务数据、行为数据后，根据规则为用户生成标签画像。显然收集、清洗后的数据越多，就能产生更多的标签，对用户的画像也就越丰满。所以这节课，我们先来看一下StarRocks在技术架构上是怎样满足亿级数据的存储与快速分析的。

学完这一讲后，希望你能了解几个知识点。

1. StarRocks集群包含哪些组件，每个组件的作用，组件之间如何协作。
2. 为什么要存算分离，存算分离有什么优缺点。
3. StarRocks如何分布数据。

首先来看一下StarRocks的系统架构。

## StarRocks系统架构

提到StarRocks就不得不说Doris，Doris最初是百度为解决凤巢广告系统，报表统计的需求而开发的，后来贡献给Apache，成为开源社区的一员。2020年百度Doris团队的一部分成员离职创业，他们基于Apache Doris开发了一款商业化闭源产品，命名为DorisDB。这就是StarRocks的前身。

后来因为DorisDB和Apache Doris名字很像，为了避免版权纠纷，DorisDB改名为StarRocks。

StarRocks在设计和架构上参考了Impala、Presto这类MPP分析引擎的思想，甚至在组件功能上也非常相似。
<div><strong>精选留言（2）</strong></div><ul>
<li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/NZvVnbgUJjnvkPFmtqCqUmH1QB3xJv2A9iaMiacENwsQlFkn4hdMNrEGRShEGD9UdaxmX08zuvcslNGR2MH4robA/132" width="30px"><span>Geek_61c09d</span> 👍（0） 💬（1）<div>starrocks的分区、分桶与tablet的个数有什么关系？</div>2024-08-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/2d/36/1c/adfeb6c4.jpg" width="30px"><span>爱学习的王呱呱</span> 👍（0） 💬（0）<div>SR的具体优势，比如为什么CBO优化器更出色，老师可以详细介绍下。只看架构，分布式olap感觉都大同小异。</div>2024-08-26</li><br/>
</ul>