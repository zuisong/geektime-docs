你好，我是黄金。欢迎来到第三期复习课，今天我们来回顾复习下Bigtable这篇论文的知识点。

## **Bigtable介绍**

在Bigtable论文中提到，当年Google的很多产品都使用Bigtable存储数据，包括Web索引、谷歌地球、谷歌金融。不管是完成批处理，还是实时数据服务，Bigtable表现得都很好。也就是说，**Bigtable不仅擅长顺序读写，也擅长随机读写**。

## **可运维性强**

徐老师在 [08讲](https://time.geekbang.org/column/article/423600)中，先是讲了为什么MySQL集群难以支撑百万级别的随机读写IOPS，主要的原因是**可运维性差**。第一，数据分区不灵活，导致随着数据规模的增长，有些分区数据多，有些分区数据少；第二，服务器扩容不灵活，扩容时要么需要移动大量数据，要么需要成倍增加服务器；第三，故障恢复时只能自动恢复主节点，不能自动恢复备份节点。

**那么，Bigtable是如何解决这些运维问题的呢？**

首先，为了应对数据规模的增长，我们需要把数据分配到不同的服务器，这个行为叫做**分区**。Bigtable的分区方式是为每个分区分配一段连续的**行键**（Row Key），每个分区管理固定大小的数据。当分区数据超过阈值时，比如128MB，分区就会自动分裂。之所以这样做，是因为数据分布可能是不均匀的，动态分区可以让数据在服务器上分布更均匀。
<div><strong>精选留言（3）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/13/d1/d1/ef8fd9ea.jpg" width="30px"><span>Dr.森</span> 👍（1） 💬（1）<div>优秀的课代表👏👏👏</div>2021-11-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1b/a9/12/e041e7b2.jpg" width="30px"><span>Ping</span> 👍（0） 💬（1）<div>请问Bigtable的主要用途是啥？</div>2021-12-31</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/76/e4/abb7bfe3.jpg" width="30px"><span>Geek_z</span> 👍（0） 💬（1）<div>老师后面有没有可能讲下Mesa: Near Real-Time, Scalable Data Warehousing，当下比较流行的Doris之类底层论文</div>2021-11-17</li><br/>
</ul>