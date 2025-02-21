你好，我是徐文浩。

通过过去几篇论文的解读，相信现在你已经深入掌握好了大数据系统的基本知识。而在Google的这些论文发表之后，整个工业界也行动起来了。很快，我们就有了开源的GFS和MapReduce的实现Hadoop，以及Bigtable的实现HBase。

这些系统，的确帮助我们解决了很多海量数据处理的问题。并且这些系统设计得也还算易用，作为工程师，我们基本不太需要对分布式系统本身有深入地了解，就能够使用它们。

不过，这些系统都还很原始和粗糙，随便干点什么都很麻烦。所以自然而然地，工程师们就会通过封装和抽象，来提供更好用的系统。这次的系统，不再是来自于Google，而是Facebook了，它的名字叫做Hive。

Facebook在2009年发表了Hive的论文《Hive: a warehousing solution over a map-reduce framework》，并把整个系统开源。而在2010年，Facebook又把这篇论文丰富了一下，作为[《Hive-a petabyte scale data warehouse using hadoop》](http://infolab.stanford.edu/~ragho/hive-icde2010.pdf)发表出来。这两篇论文其实内容上基本是一致的，后一篇的内容会更完整、详细一些，你可以按照自己的需要有选择性地阅读。
<div><strong>精选留言（8）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/15/66/8f/02be926d.jpg" width="30px"><span>在路上</span> 👍（33） 💬（1）<div>徐老师好，从存储的角度上讲，分区和分桶都是在增加文件数量，合理使用分区和分桶，可以让文件不至于太大，减少查询时扫描的数据量，如果过度使用，会增加很多小文件，而HDFS并不适合存储小文件。从查询的角度讲，当我们按a、b、c、d四个字段分区时，会形成&#47;a=*&#47;b=*&#47;c=*&#47;d=*的四级目录，只有a、b、c、d同时作为查询条件时，才能利用这种存储方式的好处，否则需要检索很多文件，不如把它们放在同一个文件。只有经常使用的查询条件才会作为分区，比如时间，这样既能减少查询时扫描的数据量，又能避免形成很多小文件。</div>2021-10-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/1d/13/31ea1b0b.jpg" width="30px"><span>峰</span> 👍（5） 💬（0）<div>最明显的问题就是小文件过多，不按照分区查必然需要open巨量文件，而且对元数据也是个负担。虽然分区分桶都是为了快速定位定位到要操作的文件集合，但却物理分割了数据，而不像索引依然保证数据是连续的。</div>2021-10-25</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1a/e1/0c/73b89aa7.jpg" width="30px"><span>xunix</span> 👍（3） 💬（0）<div>在微软内部有一套大数据处理语言叫Scope 可以看做是兼容了SQL的Pig（对外的版本叫U-SQL 可以在Azure上体验）少数文件的话感觉用起来还是挺顺手的 
但随着数据量增加 我们使用的时候逐步加入了各种存储路径的管理 现在看起来也是和metastore差不多的形式</div>2021-10-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/1c/2e/93812642.jpg" width="30px"><span>Amark</span> 👍（1） 💬（1）<div>突然发现Hive就类型汽车驾驶舱油门，刹车，方向盘..设计一样，无论是油车（mapreduce + hdfs）还是电车 (spark)，都需要使用相同的使用方式。</div>2022-12-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/cd/db/7467ad23.jpg" width="30px"><span>Bachue Zhou</span> 👍（1） 💬（0）<div>Hive 居然是用分区充当索引来用的，还真是有新意。但是完全没有索引是不是也不方便？一句 SQL 哪怕再简单也有一个基础的扫描数据文件的时长。</div>2022-12-02</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/17/ef/c3/9b0211fb.jpg" width="30px"><span>我是金水🍎</span> 👍（1） 💬（0）<div>老师，阅读hive源码您有什么材料推荐吗，谢谢老师！</div>2022-03-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/22/f4/9fd6f8f0.jpg" width="30px"><span>核桃</span> 👍（1） 💬（0）<div>这里Hive有TEXTFILE，SEQUENCEFILE和RCFILE三种格式，其中RcFile格式则是后面提到的Dremel有点类似了</div>2022-02-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/83/c9/5d03981a.jpg" width="30px"><span>thomas</span> 👍（1） 💬（1）<div>Metastore，我们通常是使用中心化的关系数据库来进行存储的
--------------------------------------------------------------------------------------&gt;
若出现单点故障咋办？</div>2021-11-24</li><br/>
</ul>