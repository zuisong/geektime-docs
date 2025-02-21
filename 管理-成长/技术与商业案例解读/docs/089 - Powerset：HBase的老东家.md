谷歌的“三驾马车”，即谷歌文件系统、MapReduce、BigTable，被誉为计算机科学进入大数据时代的标志。

作为开源大数据的标杆：Hadoop，它的开发者道格·卡丁（Doug Cutting），最初在实现自己的爬虫Nutch的时候，只实现了Hadoop文件系统和Hadoop MapReduce，并未实现BigTable。所以在很长一段时间里，BigTable在Hadoop的生态圈里是缺失的。

对于这种缺失，我们也可以理解为：无论是在爬虫还是当时Hadoop的几大生态圈里，大家对BigTable的需求并没有另外“两驾马车”那样强烈。

真正在Hadoop的生态圈里实现BigTable的开源版的，是一家叫做Powerset的公司推出的HBase项目。HBase代码量大，架构复杂，但是很多代码都写得非常优雅。与Hadoop文件系统和Hadoop MapReduce的快、糙、猛相比，HBase的出现无疑让人眼前一亮。

曾经的Powerset也是十分著名的创业公司，它创业的领域是下一代搜索引擎：自然语言搜索引擎。在今天，它却没有了当初的名气，为什么这么说呢，接下来我就会说到。

那么，这个曾经开发了HBase的创业公司，现在又是怎样的情况呢？今天我们就一起来了解一下。
<div><strong>精选留言（1）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/10/d6/bd/36e60787.jpg" width="30px"><span>白杨</span> 👍（0） 💬（0）<div>powerset hbase</div>2019-05-12</li><br/>
</ul>