你好，我是蔡元楠。

今天我要与你分享的主题是“弹性分布式数据集”。

上一讲中提到，Spark最基本的数据抽象是弹性分布式数据集（Resilient Distributed Dataset, 下文用RDD代指）。

Spark基于RDD定义了很多数据操作，从而使得数据处理的代码十分简洁、高效。所以，要想深入学习Spark，我们必须首先理解RDD的设计思想和特性。

## 为什么需要新的数据抽象模型？

传统的MapReduce框架之所以运行速度缓慢，很重要的原因就是有向无环图的中间计算结果需要写入硬盘这样的稳定存储介质中来防止运行结果丢失。

而每次调用中间计算结果都需要要进行一次硬盘的读取，反复对硬盘进行读写操作以及潜在的数据复制和序列化操作大大提高了计算的延迟。

因此，很多研究人员试图提出一个新的分布式存储方案，不仅保持之前系统的稳定性、错误恢复和可扩展性，还要尽可能地减少硬盘I/O操作。

一个可行的设想就是在分布式内存中，存储中间计算的结果，因为对内存的读写操作速度远快于硬盘。而RDD就是一个基于分布式内存的数据抽象，它不仅支持基于工作集的应用，同时具有数据流模型的特点。

## RDD的定义

弹性分布式数据集是英文直译的名字，乍一看这个名字相信你会不知所云。如果你去Google或者百度搜索它的定义，你会得到如下结果：
<div><strong>精选留言（30）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/0f/f3/cf/851dab01.jpg" width="30px"><span>Milittle</span> 👍（67） 💬（6）<div>对于思考题：需要重点理解原文中这句话：
窄依赖就是父 RDD 的分区可以一一对应到子 RDD 的分区，宽依赖就是父 RDD 的每个分区可以被多个子 RDD 的分区使用。
这句话说明了，窄依赖的父RDD必须有一个对应的子RDD，也就是说父RDD的一个分区只能被子RDD一个分区使用，但是反过来子RDD的一个分区可以使用父RDD的多个分区。那就回复今天的思考题，第一个疑问窄依赖子RDD的分区不一定只对应父RDD的一个分区，只要满足被子RDD分区利用的父RDD分区不被子RDD的其他分区利用就算窄依赖。第二个疑问其实上面已经做了回答，只有当子RDD分区依赖的父RDD分区不被其他子RDD分区依赖，这样的计算就是窄依赖，否则是宽依赖。
最后，总结以下，就是只有父RDD的分区被多个子RDD的分区利用的时候才是宽依赖，其他的情况就是窄依赖。如果有哪里理解不对的地方，请老师指正，谢谢~</div>2019-05-15</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/10/57/1adfd4f7.jpg" width="30px"><span>追梦</span> 👍（4） 💬（4）<div>老师，下面这句话对吗？
一个stage的所有task都执行完毕之后，会在各个节点本地的磁盘文件中写入计算中间结果，然后Driver就会调度运行下一个stage。下一个stage的task的输入数据就是上一个stage输出的中间结果。

说明：spark的中间计算结果会直接落到磁盘上的？？？
</div>2019-05-16</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/3b/7d/6376926b.jpg" width="30px"><span>吟游雪人</span> 👍（4） 💬（3）<div>新的RDD不就是上一步的RDD计算出的结果么？为什么说是不保存计算结果？</div>2019-05-16</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/a0/8e/6e4c7509.jpg" width="30px"><span>一</span> 👍（3） 💬（1）<div>老师好！能不能请老师讲讲Spark和Flink的对比呢？这二者谁在机器学习乃至深度学习中更有优势呢？</div>2019-05-15</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/04/64/b53c0cc2.jpg" width="30px"><span>Little Spirits</span> 👍（1） 💬（1）<div>多个父分区到一个子分区，对于任何一个父分区而言都是pipeline的所以是窄依赖，而一个父分区到多个子分区对父分区而言不是pipeline的所以是宽依赖</div>2019-05-16</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/4d/49/28e73b9c.jpg" width="30px"><span>明翼</span> 👍（1） 💬（1）<div>rdd的分区不保存数据什么意思？老师可以对rdd结构再深入讲解不？我认为子rdd在窄依赖中不会对应多个父rdd，才保障单向传递</div>2019-05-15</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/ee/16/742956ac.jpg" width="30px"><span>涵</span> 👍（1） 💬（2）<div>我想还可以算做是窄依赖，因为子RDD分区所依赖的对个父RDD分区是互斥的，所以每个子RDD分区所依赖的多个父RDD分区可以被看做一组分区。父RDD的组分区与子分区是一一对应关系，满足窄依赖可以并行计算，而无需所以父分区都计算完毕才可以开始计算的特性。</div>2019-05-15</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/57/bd/acf40fa0.jpg" width="30px"><span>lwenbin</span> 👍（0） 💬（1）<div>思考题答案应该算narrow partition. 
看了spark rdd论文，对老师说的这些概念有了新的认识。
narrow partition对应的转换例如：map, filter, join（子分区join key都在一个分区）, union. 其中join和union就对应了老师说的子分区来自于多个父分区。
区别在于wide partition有shuffle过程，存在对于同一个父分区中两个record, 经过转换操作后会对应到两个不同的子分区，所以这些操作例如：groupByKey, 通常的join。</div>2019-05-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/41/27/3ff1a1d6.jpg" width="30px"><span>hua168</span> 👍（0） 💬（1）<div>老师，hadoop计算框架Map&#47;Reduce 过时了，那另一个存储框架HDFS，也过时了吗？
现在我看很多云提供商都是对象存储实现海量需求，
现在开源的分布式存储，能在生产环境使用的，用什么了,ceph?</div>2019-05-16</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/4d/87/57236a2d.jpg" width="30px"><span>木卫六</span> 👍（0） 💬（1）<div>1.窄依赖是指父 RDD 的每一个分区都可以唯一对应子 RDD 中的分区，那么是否意味着子 RDD 中的一个分区只可以对应父 RDD 中的一个分区呢？

不是的，比如coalesce这种合并分区的操作中，子rdd需要依赖父rdd的若干个分区，但它不需要全部的分区，是窄依赖

2.如果子 RDD 的一个分区需要由父 RDD 中若干个分区计算得来，是否还算窄依赖？

算。只要纪录层级没发生重新分区，全局混洗，应该都属于窄依赖吧</div>2019-05-15</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/17/1a/ad/faf1bf19.jpg" width="30px"><span>windcaller</span> 👍（32） 💬（2）<div>窄：一子多父，一子一父
宽：一父多子</div>2019-07-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/67/8a/babd74dc.jpg" width="30px"><span>锦</span> 👍（2） 💬（0）<div>文中提到依赖关系的区分考虑基于两点：
1、性能考虑，窄依赖可以使得每个数据节点并行计算结果，也可以支持链式计算；宽依赖需要父分区的中每个分区中的数据节点计算，只能串行计算。
2、故障恢复考虑，窄依赖可以更快、更准的恢复数据，宽依赖则相对较慢。
那么基于以上考虑，父rdd与子rdd是多对多的关系，则划分到宽依赖；一对一、一对多或多对一的关系都可以划分到窄依赖。

分区方式：hash分区、rang分区，以及自定义分区
疑问：因为分区指向某个节点中的数据块，那么分区的key是分区在RDD中的index还是其引用的数据块中的某个数据字段？我认为是后者。
另外，hash分区和rang分区的应用场景分别是什么呢？

RDD具有不可变性，只能通过转换来创建新的RDD，但是不代表RDD中分区指向的节点数据块也不可变，那么如何保证数据块不可变性呢？我认为可能是使用CopyOnWrite技术实现的。

Spark优于MapReduce的地方之一在于：MapReduce的中间计算结果实时落盘，而Spark使用存储依赖关系和延迟存储中间数据来提高性能。</div>2019-05-15</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/17/2b/49/e94b2a35.jpg" width="30px"><span>CoderLean</span> 👍（2） 💬（0）<div>算啊，父子rdd可以通过函数进行转换，对于转换因子是基本不变的，那也应该支持逆转换。，而一个子rdd是无法推导出父rdd的，因为父rdd的数据是由函数转换后拆分给多个子rdd的。另外，之前没学过spark，对于flink内部算子也没有那么深入的理论，学完这个后要可以回去看看flink的算子是怎么实现的</div>2019-05-15</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/19/47/b27f1314.jpg" width="30px"><span>kissrain</span> 👍（1） 💬（1）<div>之前查阅了很多资料都没有一个对RDD完整解释或者说的很模糊。老师的这篇文章真是一针见血，越是厉害的人越是能把原理说的越通俗易懂。</div>2019-09-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/93/b8/6510592e.jpg" width="30px"><span>渡码</span> 👍（1） 💬（1）<div>思考题：
如果子RDD依赖多个父RDD的多个完整分区，也就是说不存在父RDD一个分区数据分到子RDD多个分区的情况，那就是窄依赖。因为此时父RDD不需要对key重新做分区计算，子RDD也不需要等父RDD所有分区计算完毕。</div>2019-05-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/3d/5d/ac666969.jpg" width="30px"><span>miwucc</span> 👍（1） 💬（1）<div>子rdd依赖多个父rdd来产出结果。明显是宽依赖。因为需要等待多个父rdd结果完毕才能开始计算。宽依赖还是窄依赖关键看是否要等待更多父rdd准备完毕。</div>2019-05-15</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/ac/a7/4d41966a.jpg" width="30px"><span>邱从贤※klion26</span> 👍（1） 💬（0）<div>思考题中窄依赖应该是不关心一个子 rdd 的 partition 对应多少个 父rdd 的 partition，只要partition可以独立计算就行，比如 map 操作，子 rdd 只有 3 个 partition，父 rdd 有6 个 partition，那么父 rdd 肯定有两个 partition 的数据会落到子 rdd 的一个 partition 中，但是落到子 rdd 同一个 partition 的两个 partition 不需要等待就可以进行计算，因此是窄依赖</div>2019-05-15</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/38/05/67aae6c8.jpg" width="30px"><span>Rainbow</span> 👍（1） 💬（0）<div>uion也是窄依赖</div>2019-05-15</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/25/53/70/f140cfb2.jpg" width="30px"><span>李飞</span> 👍（0） 💬（0）<div>最高赞的理解不对吧！</div>2021-04-11</li><br/><li><img src="" width="30px"><span>Geek_04168</span> 👍（0） 💬（0）<div>一子多父属于窄依赖，但我理解这种情况下，多个父依赖分布在不同的节点上，是不支持文中“窄依赖可以支持在同一个节点上链式执行多条命令”</div>2020-10-05</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/06/a0/3da0e315.jpg" width="30px"><span>茂杨</span> 👍（0） 💬（0）<div>讲的真是清楚啊。
RDD是抽象的数据结构，保存在内存当中，但是要记住这个内存可不是连续的，而是分布式的。
这就引出了分区的概念。它是隐藏在RDD下面的真正的存储空间。</div>2020-09-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/17/04/5d/259d1768.jpg" width="30px"><span>bwv825</span> 👍（0） 💬（0）<div>“而宽依赖则必须等父 RDD 的所有分区都被计算好之后才能开始处理”。此处应为“子 RDD 的所有分区”吧。宽依赖表示一个父分区可以被多个子分区使用，但不代表子分区有多个父分区。</div>2020-06-15</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/18/4b/b3/51bb33f2.jpg" width="30px"><span>北冥有鱼</span> 👍（0） 💬（0）<div>只要父RDD的分区数据能完整的交给子RDD就算窄依赖。也就是说，一个子RDD可以依赖多个父RDD。宽窄依赖是划分stage的依据，在同一个stage中，计算逻辑是可以合并的(如map，filter)，而不用每次计算逻辑都生成数据，再遍历数据。而不同的stage间需要shuffle，shuffle会生成中间数据，下一个stage需要等待上一个stage执行完再执行，逻辑也就不能和上一个stage进行合并了。同时spark要保证任务失败，能更好更快的重算，需要把依赖的父partition保留起来，以及shuffle后的结果数据保留起来… 理解不对的地方，请老师指正:)</div>2020-05-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1c/fa/96/4a7b7505.jpg" width="30px"><span>Eden2020</span> 👍（0） 💬（0）<div>主要区分一个计算是否要等待依赖计算完成了，有就是宽依赖，没有就是窄依赖，针对实际的计算需求是很容易区分的</div>2020-03-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/de/4c/a51ece16.jpg" width="30px"><span>刘润森</span> 👍（0） 💬（0）<div>spark集群读不了文件，spark本地读取得到，怎么办？</div>2020-03-02</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/be/bc/62d402da.jpg" width="30px"><span>Goku</span> 👍（0） 💬（1）<div>RDD的每个partition有没有replication？万一node挂了怎么办？</div>2019-10-04</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/be/93/247fb2c8.jpg" width="30px"><span>hel</span> 👍（0） 💬（1）<div>新RDD的分区数可以不和父RDD的分区数想等吗</div>2019-07-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/ce/8f/6daf02db.jpg" width="30px"><span>心灵捕手</span> 👍（0） 💬（0）<div>老师问下，
lines = sc.textFile(&quot;data.txt&quot;)
lineLengths = lines.map(lambda s: len(s))
totalLength = lineLengths.reduce(lambda a, b: a + b)
这个代码直接在spark上运行，报错&lt;console&gt;:1: error: &#39;)&#39; expected but &#39;(&#39; found.
val lineLengths = lines.map(lambda s: len(s))
</div>2019-06-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/8c/9c/d48473ab.jpg" width="30px"><span>dancer</span> 👍（0） 💬（2）<div>这里有个疑惑希望老师解答。spark每一个子rdd的都会记录他和父rdd分区的依赖关系，所以不需要持久化到磁盘。那么我理解所有这必须依赖于父rdd也要一直保存在内存中才可以。如果是这样的话，是不是spark需要保存所有步骤产生的rdd在内存中。 另外如果所有数据都保存在内存中，如果机器故障，该怎样恢复数据呢？感谢老师用来答疑的宝贵时间。</div>2019-06-16</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/4lUeUo6LHfsHLYfKaMQXQiaZVyEsqY1nfXU6dP0wN1KCch7LDIZTCO4rJ5mq1SdqY9FibCGMsjFdknULmEQ4Octg/132" width="30px"><span>Geek_f406a1</span> 👍（0） 💬（1）<div>窄依赖并不是完全的父子RDD一一对应，子RDD可以对应多个父RDD，父RDD只能对应一个RDD？是否可以这样理解</div>2019-05-30</li><br/>
</ul>