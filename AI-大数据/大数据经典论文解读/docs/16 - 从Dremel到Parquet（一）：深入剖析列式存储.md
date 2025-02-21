你好，我是徐文浩。

在解读Hive论文的过程中，我们看到Hive已经通过分区（Partition）和分桶（Bucket）的方式，减少了MapReduce程序需要扫描的数据，但是这还远远不够。

的确，MapReduce有着非常强的伸缩性，架起一个1000个节点的服务器毫无压力。可MapReduce的缺陷也很明显，那就是**它处理数据的方式太简单粗暴，直接就是把所有数据都扫描一遍。**

要知道，通常来说，我们的Hive表也好，或者以Thrift序列化后存放到HDFS上的日志也好，采用的都是“宽表”，也就是我们会把上百个字段都直接存放在一张表里。但是实际我们在分析这些日志的时候，往往又只需要用到其中的几个字段。

比如，我们之前的日志，有超过100个字段，但是如果我们想要通过IP段和IP地址，查看是否有人刻意刷单刷流量的话，我们可能只需要IP地址等有限的4~5个字段。而如果这些字段在Hive里并不是一个分区或者分桶的话，MapReduce程序就需要扫描所有的数据。这个比起我们实际需要访问的数据，多了数十倍。

但是，我们又不可能对太多字段进行分区和分桶，因为那样会导致文件数量呈几何级数地上升。就以上节课的例子来说，如果我们要在国家之后再加上“州”这个维度，并进行分区，那么目录的数量会增长50倍（以美国为例有50个州）。而如果我们再在时间维度上加上一个“小时”的数据维度，那么目录的数量还要再增长24倍。
<div><strong>精选留言（6）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/11/f9/d2/dc2ac260.jpg" width="30px"><span>wd</span> 👍（16） 💬（0）<div>试着回答一下这个思考题：&quot;为什么采用列存储之后，数据的压缩率也能提升呢？&quot;
一些取值比较连续分布的数据，在使用列存储以后，可以利用 runlength encoding 类似的压缩方法大大提高压缩率。因为这些数据的值会在一个比较小的区间范围内变动，存储的时候只要存delta就行了；一个通常64-bit的数值的delta可能只需要4个bit来存。</div>2021-10-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/66/8f/02be926d.jpg" width="30px"><span>在路上</span> 👍（6） 💬（1）<div>徐老师好，在《数据密集型计算系统》第3章介绍了列式存储，当数据按列存储时，可以采用位图编码来对数据压缩。用一个数组 A 保存所有出现的值，列存储中的值用位图表示，比如某行某列的值为00001000，表示这个值对应数值 A 中下标为4的值（起始下标为0）。所有的列的值都是都是差不多的数字，放在一起可以进一步压缩。这样一来，数据的压缩率就提升了。</div>2021-11-02</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/b9/9c/28339742.jpg" width="30px"><span>Steven</span> 👍（2） 💬（0）<div>列存储压缩率上升应该是相同数据类型的每一列都可以提高压缩率</div>2021-10-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/db/bc/286e72d2.jpg" width="30px"><span>阿橦木</span> 👍（1） 💬（4）<div>code: en-us country：us在数据结构中的位置都一样，为何d值一个是2一个是3呢？ </div>2021-10-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/20/b7/bdb3bcf0.jpg" width="30px"><span>Eternal</span> 👍（0） 💬（0）<div>一列的值相似度很高，比如姓名，长度，和名字重复率很高，二次编码可以降低很多空间</div>2023-03-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/77/2a/4f72941e.jpg" width="30px"><span>cpzhao</span> 👍（0） 💬（0）<div>我们用来分析的列存储数据，可以直接通过一个 MapReduce 程序，进行数据格式转换来生成。
这句有人能解释下吗，没明白写入的时候怎么弄，是存两份数据，用一个mapreduce异步转成列式存储？</div>2022-12-09</li><br/>
</ul>