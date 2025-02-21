你好，我是王磊，你也可以叫我Ivan。

今天，我们会继续学习查询场景中的处理技术。这一讲的关键词是“多表关联”，也就是数据库中常见的Join操作。无论是单体数据库还是分布式数据库，关联操作的语义始终没有变，一些经典算法也保持了很好的延续性。

关联算法作为一个稍微细节点的设计，在不同数据库中是有差异的，我们还是秉承课程的整体思路，不陷入具体的设置参数、指令等内容。这样安排的依据是，只要你掌握关联算法的基本原理，就能快速掌握具体数据库的实现了。同时，有了这些原理作为基础，你也能更容易地掌握分布式数据库的优化思路。

那么，我们先来看看这些经典的关联算法吧。

## 三类关联算法

常见的关联算法有三大类，分别是嵌套循环（Nested Loop Join）、排序归并（Sort-Merge Join）和哈希（Hash Join）。

### 嵌套循环连接算法

所有的嵌套循环算法都由内外两个循环构成，分别从两张表中顺序取数据。其中，外层循环表称为外表（Outer表），内层循环表则称为内表（Inner表）。因为这个算法的过程是由遍历Outer表开始，所以Outer表也称为驱动表。在最终得到的结果集中，记录的排列顺序与Outer表的记录顺序是一致的。
<div><strong>精选留言（13）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/13/17/27/ec30d30a.jpg" width="30px"><span>Jxin</span> 👍（2） 💬（2）<div>重分布这个有疑惑: 如果我有多个关联查询呢?每次关联查询都重分布？这样重分布就可能是个死循环了。因为A关联查询和B关联查询的重分布,可能会相互影响。</div>2020-09-23</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/3XbCueYYVWTiclv8T5tFpwiblOxLphvSZxL4ujMdqVMibZnOiaFK2C5nKRGv407iaAsrI0CDICYVQJtiaITzkjfjbvrQ/132" width="30px"><span>有铭</span> 👍（0） 💬（1）<div>Grace这个最早使用GHJ算法数据库没有查到啊？

很久以前就困惑传统数据库在分表分库后如何解决joint的问题。今天看到这篇文章后豁然开朗</div>2020-09-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/00/f4/cc5f0896.jpg" width="30px"><span>Jowin</span> 👍（2） 💬（0）<div>分布式数据库的并行查询，底层依赖的是和大数据计算平台相同的并行计算技术。可以想见，在Spark上支持SQL查询，其实是一样的原理。这一讲非常棒，把分布式数据库和大数据技术串起来了！</div>2021-03-08</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/DYAIOgq83epWuRmpg9jWibtRH3mO9I0Sc9Y86fJpiaJDdLia39eib89R1raTkxMg9AOkjb0OTRkmXiaialJgHC5ve59g/132" width="30px"><span>Geek_64affe</span> 👍（0） 💬（0）<div>思考题最主要的问题我觉得应该是如何确定 大&#47;小 表</div>2022-05-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/3e/e9/116f1dee.jpg" width="30px"><span>wy</span> 👍（0） 💬（2）<div>老师有个问题不理解 假设两个表数据量一样大都是n,那么嵌套循环的复杂度是n*n ,而排序归并的复杂度应该是nlogn+nlogn+2*n约等于nlogn。这样看的话排序归并的效率更高一点，但是文中你说成本更高一些，体现在什么地方呢</div>2021-01-26</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/Q3auHgzwzM4z9WYWVvWDhMF0SicPE5ad56ME6DibyWGbRoQa0lH4U9icdsjNcv3ssRickcuRMDA01e6vMXnmOVSr9l5LVUefVxicn/132" width="30px"><span>black_mirror</span> 👍（0） 💬（0）<div>HI，Ivan老师好
1、GHJ算法，是不是每次只把inner表bucket加入内存，而outer表的bucket一直在磁盘中，进行2者的比较？
2、observer node4 节点第2个工作线程是不是应该叫4-2 ？</div>2020-12-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/e0/cf/43f201f2.jpg" width="30px"><span>幼儿编程教学</span> 👍（0） 💬（0）<div>大表join，查询过来的时候，再做重分布？在节点间移动数据？这样不会很慢？是不是我的理解哪里有问题？这种指的是olap吧？</div>2020-11-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/d5/b1/1007b5d2.jpg" width="30px"><span>星之柱</span> 👍（0） 💬（0）<div>h如果选择的inner表ash不均衡的时候，就退化成了嵌套循环</div>2020-11-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/71/3d/da8dc880.jpg" width="30px"><span>游弋云端</span> 👍（0） 💬（0）<div>“在计算逻辑允许的情况下，建立阶段选择数据量较小的表作为 Inner 表”，我的问题就是在什么情况下，系统无法根据数据量决定 Inner 表呢？
答复：如果连接属性本身内容重复较多，但是表格很大，这样反而选择较大的表格作为 Inner 表，可以根据内容相同，从而节省Hash的计算资源。想到这种场景。</div>2020-09-24</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTJqUkoCXOxRraVNVg1fTm4O892WFVCjeL9pS8kUX2nEeTEcaS6k0kP25h3rRKtUCwSoUrY6dvP43w/132" width="30px"><span>赵见跃</span> 👍（0） 💬（0）<div>哈希算法，“在计算逻辑允许的情况下，建立阶段选择数据量较小的表作为 Inner 表”，我的问题就是在什么情况下，系统无法根据数据量决定 Inner 表呢？这个问题，也很困惑，大家给指点一下呀，谢谢。</div>2020-09-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/47/00/3202bdf0.jpg" width="30px"><span>piboye</span> 👍（0） 💬（0）<div>复制表，写的时候也是异步复制到其他节点上？</div>2020-09-23</li><br/><li><img src="" width="30px"><span>licl1008</span> 👍（0） 💬（0）<div>数据量小的一侧不是构建侧，这种情况不能单单根据数据量来决定innner</div>2020-09-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1d/12/13/e103a6e3.jpg" width="30px"><span>扩散性百万咸面包</span> 👍（0） 💬（0）<div>我对重分布的理解：按照某个非分区键再做一遍重分区。

对于这个思考题，应该是两个关联表的大小都远远超过了单机的内存？所以必须要上分布式？</div>2020-09-23</li><br/>
</ul>