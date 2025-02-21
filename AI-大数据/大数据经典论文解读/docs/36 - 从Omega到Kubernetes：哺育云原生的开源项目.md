你好，我是徐文浩。

在前面两节课里，我们一起看过在2015年发表的Borg的论文。不过，Borg这个系统的开发与使用，其实要远远早于2015年。事实上，在2004年Google发表的MapReduce的论文里，我们就已经隐隐约约可以看到Borg的存在了。

而在2015年，Borg也早就已经进行了很多次的进化。在2013年，Google就发表了一篇叫做《Omega: Flexiable, Scalable Schedulers for large compute clusters》的论文，向整个工业界介绍了 **Omega** 这个调度系统。而在不久之后的2014年7月，Google更是首次发布了开源的 **Kubernetes** 系统。

在2016年，Google更是发表了一篇叫做《Borg, Omega, and Kubernetes: Lessons Learned From Three Container-Management Systems Over A Decade》的文章。这篇文章总结了十多年来，Google从开发Borg，到优化调度系统变成Omega，以及最后重起炉灶开源Kubernetes中的经验与教训。

那么，今天我们就一起来了解下，在2013和2016年发表的这两篇论文到底讲了什么。虽然Google并没有开源Borg和Omega，但是从开源的Kubernetes和发表的论文中，我们也多少能够一窥这些系统是如何一路走来的。我在这个课程的一开始就说过，我们学习这些论文和知识，重要的并不只是“是什么”“怎么做”的，更重要的是**“为什么”**。了解系统是如何逐渐演变过来的，你才能真的体会到如何在不断地迭代优化中设计系统。
<div><strong>精选留言（2）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/15/22/f4/9fd6f8f0.jpg" width="30px"><span>核桃</span> 👍（1） 💬（0）<div>把大数据系统部署在k8s上面，我们以前曾经尝试过，但是这里有一个问题，到底什么类型的大数据项目适合放在k8s上面呐？其实应该是计算型的工具，如spark,flink和storm这些，而存储型的工具，像hdfs,hbase则不适合，原因是spark这些运行的job任务，其实可以不断重试和调度的，目前spark也已经不断适配k8s系统了。
而存储型的工具，目前云原生有一个叫openEBS的项目出现，这个项目的核心是资源隔离，向spanner架构那样，一个服务对应一个存储管理单元一个存储池，互不干扰，当然对资源肯定会消耗多一些，但是这恰恰就和云原生的思想匹配的。</div>2022-03-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/66/8f/02be926d.jpg" width="30px"><span>在路上</span> 👍（0） 💬（0）<div>徐老师好，批处理能够高吞吐地处理历史数据，但是对即席查询而言有点慢。流式处理能够低延迟地处理实时数据，但是需要先写逻辑再消费数据。Dremel查询性能好，但是它的数据文件采用列式存储，不可修改，数据难以以分钟级别的延迟落到数据库中。我认为实时数据湖是一个方向，数据以低成本、低延迟的方式落入湖中，支持快速查询、快速分析。</div>2022-01-17</li><br/>
</ul>