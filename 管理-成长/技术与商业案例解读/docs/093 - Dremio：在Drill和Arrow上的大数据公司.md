今天这篇文章，我们来讲讲一个非常年轻的公司Dremio的故事。这个故事涉及了两个Apache开源项目Drill和Arrow，和一家Hadoop发行商MapR。

我们先从MapR公司开始讲起，MapR在2009年成立，发展一直不错，在CTO的带领下，公司出品了一个自己的文件系统，取代了HDFS，同时，它的Hadoop发行版也取得了不俗的成绩。

托马尔 · 希兰（Tomer Shiran）和雅克 · 纳杜（Jacques Nadeau），这两位都是MapR公司的核心员工。让我们记住这两个人的名字，因为他们与我们接下来的故事息息相关。托马尔是MapR的第一位产品经理，负责整个产品线的开发。雅克则是Apache Drill项目和Apache Arrow项目的主要负责人。

## 第一个项目：Apache Drill

让我们把时间倒回到2013年。当时Hive已经存在，但是很慢很不好用。谷歌的Dremel刚出来没多久，就掀起了交互式查询的风潮，随之而来的是Cloudera开始了它的Impala引擎的计划；而MapR也决定做一款查询引擎，自己主导开源项目，这就是后来的Apache Drill。

当时筹建这个项目的人，是托马尔，而具体负责干事情的人，是雅克。我之所以知道这件事情的详细情况，是因为2013年的时候，这两位打电话给我，希望我加盟这个尚未展开的项目。
<div><strong>精选留言（1）</strong></div><ul>
<li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/PiajxSqBRaELbYFAXthMl6KBS3dKjYX2lAicRL7ZhahfCkabo12dQjhkvxGCc0BaC0IxibOjZdO5RWibD8CIcELb1Q/132" width="30px"><span>Mao</span> 👍（0） 💬（0）<div>Dremio的低版本开源了，高级的一些功能是付费的。现在支持的数据源也多了，可能因为比较新，连接器识别元数据还是会有各种各样的问题。
我觉得Dremio最大的优势在于基于明细数据直接进行分析，这个对数据使用方非常友好。</div>2022-01-17</li><br/>
</ul>