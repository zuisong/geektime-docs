你好，我是大明。今天我们来学习 MongoDB 的另外一个热点面试主题——优化 MongoDB 的查询性能。

就像之前我多次提到的，任何中间件的面试说到底就是以高可用、高性能和高并发为主。高性能和高并发可以说是孪生兄弟，你做到了高性能，基本上就做到了高并发。

在面试中，性能优化一直被看作是一个高级面试点，因为只有对原理了解得很透彻的人，在实践中才能找准性能问题的关键点，从而通过各种优化手段解决性能问题。

在这之前，我们先来看看 MongoDB 的查询过程，这样方便你理解后面的优化手段。

## MongoDB 的查询过程

MongoDB 在分片之后肯定会有一些机制来保证查询能够准确找到数据。说到这里，你肯定想到了分库分表的查询过程。在分库分表中，查询的执行过程中最重要的一步，就是计算数据可能在哪个目标表上。如果实在计算不出来，那么只能考虑使用广播。

而MongoDB 也需要考虑类似的问题。在 MongoDB 里面，有一类实例叫做 mongos，这些实例就是负责路由查询到目标表上，还有合并结果集。

![图片](https://static001.geekbang.org/resource/image/71/62/717ef05ee34e5c413b5a27c479626062.png?wh=1920x1017)

而在分库分表中，计算目标表是分库分表中间件或者分库分表代理完成的。

## MongoDB 的 ESR 规则

在 MongoDB 里面设计索引的时候就要考虑所谓的 ESR 规则。ESR 代表的是 E（Equality）、S（Sort）和 R（Range），也就是相等、排序和范围。你在设计索引的时候，按照 ESR 规则来排列你的索引列。
<div><strong>精选留言（2）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/10/25/87/f3a69d1b.jpg" width="30px"><span>peter</span> 👍（0） 💬（1）<div>请问：MongoDB的索引，是包含真正的数据吗？还是只包含指向真正数据的指针？</div>2023-09-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/24/b8/be/bf2b6778.jpg" width="30px"><span>Stars゛</span> 👍（0） 💬（1）<div>拆分大文档是不是就跟mysql数据库分表一样了？</div>2024-03-12</li><br/>
</ul>