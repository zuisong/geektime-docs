你好，我是徐文浩。上一讲里我们一起分析了如何对一个MySQL集群进行扩容，来支撑更高的随机读写请求。而在扩容过程中遇到的种种不便，也让我们深入理解了Bigtable的设计中需要重点解决的问题。

第一个问题，自然还是如何支撑好每秒十万、乃至百万级别的随机读写请求。

第二个问题，则是如何解决好“可伸缩性”和“可运维性”的问题。在一个上千台服务器的集群上，Bigtable怎么能够做到自动分片和灾难恢复。

今天我们就先来看看第二个问题，其实也是Bigtable的整体架构。而第一个问题，一半要依赖第二个问题，也就是可以不断将集群扩容到成百上千个节点。另一半，则取决于在每一个节点上，Bigtable的读写操作是怎么进行的，这一部分我们会放到下一讲，也就是Bigtable的底层存储SSTable究竟是怎么一回事儿。

那么接下来，我们就一起来看看Bigtable的整体架构。在学完这一讲后，希望你可以掌握Bigtable三个重要的知识点：

- 第一个，Bigtable是如何进行数据分区，使得整个集群灵活可扩展的；
- 第二个，Bigtable是如何设计，使得Master不会成为单点故障，乃至单点性能的瓶颈；
- 最后，自然是整个Bigtable的整体架构和组件由哪些东西组成。
<div><strong>精选留言（26）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/15/66/8f/02be926d.jpg" width="30px"><span>在路上</span> 👍（10） 💬（4）<div>徐老师好，在Bigtable论文的第 7 部分“性能评估”里写道：
Each random read involves the transfer of a 64 KB SSTable block over the network from GFS to a tablet server, out of which only a single 1000-byte value is used……
Random and sequential writes perform better than random reads since each tablet server appends all incoming writes to a single commit log and uses group commit to stream these writes efficiently to GFS.

随机写和顺序写的性能旗鼓相当，不仅在单台tablet server上表现类似，在tablet server集群上表现也几乎一样。原因是它们都会先写commit log，同步修改内存中的数据，异步修改SSTable中的数据。随机写和顺序写的差异在于SSTable的变更，由于这个操作被异步执行，所以它们的性能没有差异。
如果SSTable的不缓存在tablet server上，随机读的性能非常差，比写入操作几乎慢一个数量级。原因是不管要实际需要多小的数据，都需要从GFS上加载64k的SSTable块数据。它的瓶颈不在于tablet server的多少，而在于从GFS上读取数据。

我在学习今天的课程和阅读Bigtable论文的时候，有三个疑问：
1.课程中提到通过外部服务去监控Master的存活，可能会导致系统中出现两个Master，那么GFS没有这个问题吗？如果有的话不会造成严重的后果吗？
2.当我向bigtable写入数据时，metadata的三层结构会如何变更？变更的过程如何避免加锁？如果需要全局锁的话，我想读写性能肯定上不去。
3.随机读比写入操作慢一个数量级我还是很惊讶，因为写入操作的commit log需要写入GFS，同样有GFS操作，怎么能差出一个数量级？</div>2021-10-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/83/c9/5d03981a.jpg" width="30px"><span>thomas</span> 👍（3） 💬（4）<div>METADATA 的一条记录，大约是 1KB，而 METADATA 的 Tablet 如果限制在 128MB，三层记录可以存下大约 (128*1000)2=234 个 Tablet 的位置，也就是大约 160 亿个 Tablet
=============================================》
这个是如何算出来的？</div>2021-10-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/8f/60/be0a8805.jpg" width="30px"><span>陈迪</span> 👍（2） 💬（2）<div>问老师：
10多年前的Bigable架构是否是一种符合当下潮流的“存储和计算分离”的架构？存储GFS做得够了，就用GFS单独存，前面哪个tablet压力大可以调度出来多一点。
当下则是objcet storage又便宜又可靠，不要share nothing本机再做一遍存储了，都交给object storage</div>2021-10-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/8f/cf/890f82d6.jpg" width="30px"><span>那时刻</span> 👍（2） 💬（0）<div>Bigtable数据随机读写慢，我想到的原因是：其一是个三层 Tablet 信息存储的架构，读写有多次网络请求。其二是tablet的分裂和合并，使数据产生迁移。</div>2021-10-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/17/23/cf/7429d6e8.jpg" width="30px"><span>爱码士</span> 👍（1） 💬（0）<div>感觉这一片的三层结构的插图有点抽象，希望老师能够再解释一下</div>2023-02-01</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/1e/b7/b20ab184.jpg" width="30px"><span>麋鹿在泛舟</span> 👍（1） 💬（0）<div>3层b+tree结构的metadata存储tablet个数的计算: 
1. 第1层为根节点，第2层每个元素指向的是一个tablet，因此总存储tablet个数实际上是2层b+tree存储元素的总个数。
2. 一个tablet元素个数 = (128 * 1024KB) &#47; 1KB = 2 ^ 17，即根节点可以存储这么多元素
3. 根节点的每个元素又指向了一个tablet，因此2层b+tree存储个数= 2^17 * 2^17 = 2 ^ 34</div>2022-11-07</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/8f/60/be0a8805.jpg" width="30px"><span>陈迪</span> 👍（1） 💬（0）<div>随机读，最差情况下，要网络走查元数据+从gfs读出来，gfs一读一block就是64mb，一个key value大小往往远小于这个数字。写的话就没这个问题，读内存也会快，顺序读的话key排序+ gfs支持得本来也好。相比之下，随机读显得很糟糕了</div>2021-10-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/1d/13/31ea1b0b.jpg" width="30px"><span>峰</span> 👍（1） 💬（0）<div>随机读最后只落在一台sever上，不能并行，再加上一次读取转换成了串行的三次读，自然相较而言是慢的。</div>2021-10-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/2d/00/9f/656eee94.jpg" width="30px"><span>lilyanchi</span> 👍（0） 💬（0）<div>似懂非懂 需要再读几遍</div>2024-05-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/bb/cc/fac12364.jpg" width="30px"><span>xxx</span> 👍（0） 💬（0）<div>描述方式太过抑扬顿挫了，结构感不够。</div>2023-11-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/47/00/3202bdf0.jpg" width="30px"><span>piboye</span> 👍（0） 💬（0）<div>tablet迁移是怎么搞的？ 迁移会带来短时间不可以用吧？</div>2022-01-15</li><br/><li><img src="" width="30px"><span>Geek_80bb15</span> 👍（0） 💬（0）<div>徐老师好，HBase把Root表干掉了，是怎么解决Meta表的热点访问问题的呢？多谢</div>2022-01-06</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/43/24/3f9f7c70.jpg" width="30px"><span>zixuan</span> 👍（0） 💬（0）<div>请问老师，5.1 Tablet Location 这里的 Location指的是tablet的gfs文件路径，还是其所述的tablet server的地址？</div>2022-01-03</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTKJrOl63enWXCRxN0SoucliclBme0qrRb19ATrWIOIvibKIz8UAuVgicBMibIVUznerHnjotI4dm6ibODA/132" width="30px"><span>Helios</span> 👍（0） 💬（0）<div>因为sstable这种格式是用lsm tree实现的更加适合顺序读，b tree更适合随机读</div>2021-12-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/22/f4/9fd6f8f0.jpg" width="30px"><span>核桃</span> 👍（0） 💬（1）<div>这里有几个问题不太理解。

1.首先读可以不经过master能理解，写也不经过就有点困惑了，既然master就是负责平衡tablet server的，那么写入的时候，到底指定哪个server写入?这个该由谁来负责呢？如果不是master，那么必然就可能会有数据倾斜问题吧。
2.文件查询过程那里，三次请求获取到具体数据所在的tablet server的tablets上面，这里有个疑惑。三级架构下和文件系统的文件目录树类似嘛，但是访问root tablet的时候，怎么会知道你所在的表在哪个节点呢？这里又不像域名访问那样，一个root tablet不可能具体知道你这个表可以从哪里读取的呀，应该是只有下面一层数据所对应的上级才真正知道的。</div>2021-11-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/21/e3/9b/b045124d.jpg" width="30px"><span>林军人</span> 👍（0） 💬（1）<div>老师看完这节,我有两个问题:
1.虽然BT在进行读写的时候, 不需要经过Master, 但是Root Tablet 本身会不会成为系统的瓶颈呢, 如果同时有大量第一次请求的客户端, 都去访问Root Tablet, 而Root Tablet又不会分片, BT会怎么处理呢?
2.MetaData表中的行键是怎么设计的呢？ 是 &quot;表名+对应Tablet起始行键&quot; 吗？</div>2021-11-14</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTKJrOl63enWXCRxN0SoucliclBme0qrRb19ATrWIOIvibKIz8UAuVgicBMibIVUznerHnjotI4dm6ibODA/132" width="30px"><span>Helios</span> 👍（0） 💬（0）<div>原来Bigtable集群Chubby才是核心
</div>2021-10-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/2b/10/c6/5e7f3148.jpg" width="30px"><span>Somnus💫</span> 👍（0） 💬（0）<div>感觉看完一遍之后还有一些些乱。还要多学几次，反过来再看。
</div>2021-10-23</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTL33HdAfZA9cQseTJ5HIWZ2XNVes8X29E5VabpU1q0UicxClNppEwUcMOXEZnTxPUEibv8uic5Oiaia8lQ/132" width="30px"><span>Geek_fe2f4c</span> 👍（0） 💬（0）<div>客户端如果需要做特殊缓存，那就还是需要客户端做特殊设计，对吧</div>2021-10-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/04/30/7f2cb8e3.jpg" width="30px"><span>CRT</span> 👍（0） 💬（0）<div>检测的方法也不复杂，其实就是通过心跳。Master 会定期问 Tablets，你是不是还占着独占锁呀？
这个应该是定期问Tablets Server？</div>2021-10-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/83/c9/5d03981a.jpg" width="30px"><span>thomas</span> 👍（0） 💬（0）<div>老师，Bigtable 的基本数据模型 希望举个实际的数据应用场景</div>2021-10-15</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/20/5d/69170b96.jpg" width="30px"><span>灰灰</span> 👍（0） 💬（0）<div>打卡，不是很仔细，还需要重新读。</div>2021-10-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/f9/e6/47742988.jpg" width="30px"><span>webmin</span> 👍（0） 💬（0）<div>思考题：
1. 随机读无法真正做到随着节点数的增加线性增长，这是为什么呢？
读取1000字节的值，需要从GFS读取一个64KB的Block，随着机器的增加1Gbps 网络带宽达到饱和，每个节点的吞吐量都有显示下降，瓶颈在网络总带宽。
2. 这个和我们今天讲的 Bigtable 的设计中的哪一个设计点相关？
Bigtable的tablet的三层结构设计有关</div>2021-10-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/00/4e/be2b206b.jpg" width="30px"><span>吴小智</span> 👍（0） 💬（0）<div>想请教老师，metadata 里面具体存了什么呢？与 gfs 中文件的位置的关联的信息是怎么存的？</div>2021-10-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/00/4e/be2b206b.jpg" width="30px"><span>吴小智</span> 👍（0） 💬（0）<div>想请教老师，tablet 的 split 具体会做些什么？会涉及到 gfs 中数据的迁移吗？还是仅涉及到 metadata 的修改？</div>2021-10-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/00/4e/be2b206b.jpg" width="30px"><span>吴小智</span> 👍（0） 💬（2）<div>METADATA 的一条记录，大约是 1KB，而 METADATA 的 Tablet 如果限制在 128MB，三层记录可以存下大约 (128*1000)2=234 个 Tablet 的位置，也就是大约 160 亿个 Tablet，肯定是够用了。  中  (128*1000)2=234  这个怎么理解？</div>2021-10-08</li><br/>
</ul>