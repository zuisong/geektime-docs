你好，我是蔡元楠。

今天我要与你分享的主题是“为什么MapReduce会被硅谷一线公司淘汰”。

我有幸几次与来Google参观的同行进行交流，当谈起数据处理技术时，他们总是试图打探MapReduce方面的经验。

这一点让我颇感惊讶，因为在硅谷，早已没有人去谈论MapReduce了。

今天这一讲，我们就来聊聊为什么MapReduce会被硅谷一线公司淘汰。

我们先来沿着时间线看一下超大规模数据处理的重要技术以及它们产生的年代。

![](https://static001.geekbang.org/resource/image/54/ca/54a0178e675d0054cda83b5dc89b1dca.png?wh=5000%2A3092)

我认为可以把超大规模数据处理的技术发展分为三个阶段：石器时代，青铜时代，蒸汽机时代。

### 石器时代

我用“石器时代”来比喻MapReduce诞生之前的时期。

数据的大规模处理问题早已存在。早在2003年的时候，Google就已经面对大于600亿的搜索量。

但是数据的大规模处理技术还处在彷徨阶段。当时每个公司或者个人可能都有自己的一套工具处理数据。却没有提炼抽象出一个系统的方法。

### 青铜时代

2003年，MapReduce的诞生标志了超大规模数据处理的第一次革命，而开创这段青铜时代的就是下面这篇论文《MapReduce: Simplified Data Processing on Large Clusters》。
<div><strong>精选留言（30）</strong></div><ul>
<li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/dV2JvjoAOHOibxVqExibsBv0ib9jJ9zD8icYaDtFbicUgP0GmRbzmgujvz6pOl6drUcgdvfQXTJpOOY9OL45WrkInbA/132" width="30px"><span>SpanningWings</span> 👍（16） 💬（1）<div>还想到一个问题有关consistent hashing的。map reduce下层的GFS也没有采用consistent hashing来控制分片，这又是为什么？老师有空回答下吗？
</div>2019-04-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/50/87/dde718fa.jpg" width="30px"><span>alexgreenbar</span> 👍（13） 💬（1）<div>赞一个，几乎每问必答，无论是否小白问题，很务实，具备高手风范！</div>2019-04-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/48/f3/65c7e3ef.jpg" width="30px"><span>cricket1981</span> 👍（10） 💬（1）<div>如果不需要按某些字段做聚合分析，只是普通数据处理的话，直接用Round Robin分片即可。我想了解什么是“动态分片”技术？即使不用MR，其他大数据处理框架也需要用到“分片”，毕竟大数据的处理是“分而治之”，如何分才能分得好是关键。日常工作中经常遇到数据倾斜问题，也是由于分片不合理导致的。如果对于待处理的数据你了解到好办，知道用哪些字段作分片最合适，但如果遇到不熟悉的数据你又该如何分片？而不是等到出现数据倾斜问题的时候才发现，进行分片修改再重跑呢？谢谢老师指教！</div>2019-04-17</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTLhMtBwGqqmyhxp5uaDTvvp18iaalQj8qHv6u8rv1FQXGozfl3alPvdPHpEsTWwFPFVOoP6EeKT4bw/132" width="30px"><span>Codelife</span> 👍（69） 💬（1）<div>我们最早采用的是哈希算法，后来发现增删节点泰麻烦，改为带虚拟节点的一致性哈希环开处理，稍微复杂点，但是性能还好</div>2019-04-17</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/dHawibgghoCDFTuT4uIF3yibBxhgSuGaiagGMO8QYSBL0L2IcJ2TvggBjZattqSeeoJY5S1CmcyfuE7gkpb4P6fibg/132" width="30px"><span>maye</span> 👍（14） 💬（1）<div>个人愚见：虽然MapReduce引擎存在性能和维护成本上的问题，但是由于Hive的封装使其适用性很广泛，学习成本很低，但是实际使用过程中和Spark等相比性能差太多了。不过对于计算引擎模型的理解方面，MapReduce还是一个很经典的入门模型，对于未来迁移到其他计算引擎也是有很大帮助的。
还有一个个人问题：不知道蔡老师对于流计算和批处理的关系是怎么看待的？流计算有可能完全取代批处理么？
关于思考题：问题的核心店在于Reducer Key是否倾斜，个人认为可以按照update_time之类的时间字段进行分片处理。</div>2019-04-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/7c/16/4d1e5cc1.jpg" width="30px"><span>mgxian</span> 👍（247） 💬（2）<div>把年龄倒过来比如 28 岁 变成 82 来分片</div>2019-04-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/4d/49/28e73b9c.jpg" width="30px"><span>明翼</span> 👍（7） 💬（1）<div>一般用户信息表都存在一个id，有的是递增的数字id，有的是类似uuid随机字符串，对于递增的直接对机器数量取余，如果是字符串通过比较均衡的hash函数操作后再对机器数量取余即可。</div>2019-04-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/0e/b9/7866f19d.jpg" width="30px"><span>王伟</span> 👍（35） 💬（1）<div>你好！我工作中遇到这样的场景：会员在我们平台注册，信息会保存在对应商家的商家库中，现在需要将商家库中的信息实时的同步到另一台服务的会员库中，商家库是按照商家编号分库，而且商家库和会员库没在同一台服务器部署。想请教一下，像这种我们如何做到实时同步？</div>2019-04-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/4d/87/57236a2d.jpg" width="30px"><span>木卫六</span> 👍（14） 💬（1）<div>年龄是值域在0-120（假定）之间的数值，难以分片的原因正是因为年龄的十位数权重过大，所以我觉得一切有效降低十位数权重的哈希算法应该都是可行的。
1.对于年龄ABC，比如倒置CBA，或(C*大质数1+B*较小质数+C)%numPartitions，这类方法应该可以明显改善分布不均，但是对某些单一热点无解，比如25岁用户特别多；
2.随机分区，可做到很好均衡，对combine，io等优化不友好
3. 先采样+动态合并和拆分，实现过于复杂，效果可能不稳定

这是我的想法，请老师指正。</div>2019-04-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/62/a5/43aa0c27.jpg" width="30px"><span>TKbook</span> 👍（10） 💬（1）<div>在评论在看到Consistent hashing，特地去搜索看了下，终于明白了。评论干货很多。。</div>2019-04-17</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/DYAIOgq83erQ5LXNgaZ3ReArPrY4YeT5mNVtBpiazFEQzNuUXxzdLOWtMliaGicNCpjaOezRISARHXPibkA4ACgib1g/132" width="30px"><span>JensonYao</span> 👍（8） 💬（1）<div>MapReduce是从纷繁复杂的业务逻辑中，为我们抽象出了 Map 和 Reduce这样足够通用的编程模型。
缺点：
1、复杂度高
	当你构造更为复杂的处理架构时，往往进行任务划分，而且每一步都可能出错。而且往往比认为的复杂的多。
2、时间性能达不到用户要求
	Google500 多页的 MapReduce 性能优化手册
	1PB的排序从12小时优化到0.5小时花了5年

思考题：如果你在 Facebook 负责处理例子中的用户数据，你会选择什么分片函数，来保证均匀分布的数据分片?
由于没有过相关的经验，从网上查了下资料，常见的数据分片有1、hash 2、consistent hash without virtual node 3、consistent hash with virtual node 4、range based
文章中使用的方法就是range based方法，缺点在于区间大小固定，但是数据量不确定，所以会导致不均匀。
其他三种方法都可以保证均匀分布的数据分片，但是节点增删导致的数据迁移成本不同。
1、hash函数节点增删时，可能需要调整散列函数函数，导致大量的数据迁移
　　consistent hash是将数据按照特征值映射到一个首尾相接的hash环上，同时也将节点映射到这个环上。对于数据，从数据在环上的位置开始，顺时针找到的第一个节点即为数据的存储节点
2、consistent hash without virtual node 增删的时候只会影响到hash环上响应的节点，不会发生大规模的数据迁移。但是，在增加节点的时候，只能分摊一个已存在节点的压力；同样，在其中一个节点挂掉的时候，该节点的压力也会被全部转移到下一个节点
3、consistent hash with virtual node 在实际工程中，一般会引入虚拟节点（virtual node）的概念。即不是将物理节点映射在hash换上，而是将虚拟节点映射到hash环上。虚拟节点的数目远大于物理节点，因此一个物理节点需要负责多个虚拟节点的真实存储。操作数据的时候，先通过hash环找到对应的虚拟节点，再通过虚拟节点与物理节点的映射关系找到对应的物理节点。引入虚拟节点后的一致性hash需要维护的元数据也会增加：第一，虚拟节点在hash环上的问题，且虚拟节点的数目又比较多；第二，虚拟节点与物理节点的映射关系。但带来的好处是明显的，当一个物理节点失效是，hash环上多个虚拟节点失效，对应的压力也就会发散到多个其余的虚拟节点，事实上也就是多个其余的物理节点。在增加物理节点的时候同样如此。
引用blog：http:&#47;&#47;www.cnblogs.com&#47;xybaby&#47;p&#47;7076731.html

所以这样看具体采用何种方式要结合其他的因素（显示场景，成本？），如何抉择我也不是很清楚。</div>2019-04-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/f8/a9/93e418f5.jpg" width="30px"><span>牛冠群</span> 👍（7） 💬（1）<div>您好，学习周期有点长，能不能加快些进度。感谢！</div>2019-04-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/40/bd/acb9d02a.jpg" width="30px"><span>monkeyking</span> 👍（6） 💬（2）<div>按照user_id哈希或者给user_id加一个随机数前缀</div>2019-04-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/6b/e4/afacba1c.jpg" width="30px"><span>孙稚昊</span> 👍（5） 💬（1）<div>我们公司现在还在使用hadoop streaming 的MapReduce，默认mapper 结果是按key sort 过得，在reducer 中借此实现join和group by的复杂操作，经常为了Join 一个table就要多写四个job</div>2019-04-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/37/d0/26975fba.jpg" width="30px"><span>西南偏北</span> 👍（5） 💬（1）<div>MR的劣势刚好对应了Spark的优势

1. 通过DAG RDD进行数据链式处理，最终只有一个job，大大降低了大数量MR的维护成本
2. 优先基于内存计算的Spark相对于基于磁盘计算的MR也大幅度提高了计算性能，缩短计算时间

个人觉得，这两点可以作为MR和Spark的主要区别。</div>2019-04-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/5b/71/140a10e8.jpg" width="30px"><span>王昊</span> 👍（4） 💬（1）<div>老师您好，我现在正在读研究生(专业计算机技术)，喜欢数据科学，编写过简单的MR，谢谢您高屋建瓴地述说其历史发展，想请教您比如很多学生应该怎么学习，如何成长为优秀的工程师，是应该从头从MR学起还是直接学高级的技术？</div>2019-04-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/6b/e4/afacba1c.jpg" width="30px"><span>孙稚昊</span> 👍（4） 💬（1）<div>现在写MapReduce job 开几百个worker经常有1，2个卡着不结束，基本都要在下班前赶着启动耗时长的任务。 我们分片用户是用的 country+username 的 hash，还是比较均匀的</div>2019-04-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/ef/a7/6e8f3636.jpg" width="30px"><span>mjl</span> 👍（4） 💬（1）<div>个人理解，对于已知数据分布情况的数据，我们大多数情况下能找到合适的一个分区策略对数据进行分片。但实际上这对于数据开发者来说，就需要知道整体数据的一个基本情况。而对于数据倾斜，基本分为分区策略不当导致的倾斜以及单热点key的倾斜，对于后者，无论用户设置什么分区策略，都无法对数据进行分割。
对于数据倾斜问题的话，spark 3.0版本计划合入的AE功能给出了一定的方案。对于倾斜的partition，在shuffleWrite阶段就可以统计每个map输出的各个分区信息，然后根据这些信息来调整下一个stage的并发度。进一步的话，对于两表join，一张表有存在热点key的话，可以广播另外一张表的该partition，最终与其他分区的join结果做union。基于这个思路的话，engine其实是能很灵活的处理数据倾斜类问题，而不用用户去花精力研究选择。</div>2019-04-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/a1/e6/50da1b2d.jpg" width="30px"><span>旭东(Frank)</span> 👍（4） 💬（1）<div>区分热点数据（占用）大的数据，以及关联性大的数据。应该有个数据抽样分析，再做具体分片策略</div>2019-04-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/6b/e4/afacba1c.jpg" width="30px"><span>孙稚昊</span> 👍（3） 💬（1）<div>如果我读Beam的文档没有理解错的话，Beam只是spark 和flink 的各种API的一个封装，本身并没有runner，该有的调优还得在spark 和flink上面做，所以除了google以外的公司用Beam的还是蛮少的</div>2019-04-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/93/b8/6510592e.jpg" width="30px"><span>渡码</span> 👍（3） 💬（1）<div>认同您说的MR的局限性，因此建立在MR之上的hive有用武之地。面对不断出现的新框架我们怎么快速掌握它的设计，尤其是即便看文档也会觉得模棱两可，这时候有必要深入到源码中吗，您在这后续课程中有没有相关的经验分享</div>2019-04-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/6b/e4/afacba1c.jpg" width="30px"><span>孙稚昊</span> 👍（3） 💬（1）<div>我们组还在用Hadoop Streaming而没有使用spark的原因是spark 内存使用不加节制，经常新起的job把周期性job的内存吃光，导致他们有时会挂掉，不知道这个问题是否有很好的解决方法。我们还是在保守地使用hadoop streaming，麻烦得很</div>2019-04-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/ed/3e/c1725237.jpg" width="30px"><span>楚翔style</span> 👍（3） 💬（1）<div>mapreduce更适合处理离线数据吧，而且数据量大了比spark要稳定。楠兄怎么看？</div>2019-04-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/c7/2a/02eea2ba.jpg" width="30px"><span>veio007</span> 👍（3） 💬（1）<div>如果是我，外面弄个自增的计数器，然后每次计数器的当前值对worker个数取模，但是就算每个人分配同等数量的数据，同样会出现有人快有人慢的情况，机器的性能处理能力不一样或者其他干扰项都可能会有影响</div>2019-04-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/41/27/3ff1a1d6.jpg" width="30px"><span>hua168</span> 👍（3） 💬（1）<div>那现在还在用MapReduce的大数据软件怎么搞了？也会被慢慢淘汰？还需要学习吗？</div>2019-04-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/24/0f/196fa05b.jpg" width="30px"><span>呆小木</span> 👍（3） 💬（1）<div>对用户id取哈希值，然后用哈希值对分区数取模。由于不同的id还是有可能计算得到相同的哈希值，也就是所谓的哈希碰撞，从而产生数据倾斜，可以在Map端给id拼上一个随机字符串，让它计算得到的哈希值分配更均匀，到Reduce端再去掉随机串。请老师指点😜ོ</div>2019-04-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/ef/c0/8adceaed.jpg" width="30px"><span>Li221</span> 👍（2） 💬（1）<div>给元楠老师100个赞，每问必答，是所有专栏里最敬业的老师了！</div>2019-04-18</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/3XbCueYYVWTiclv8T5tFpwiblOxLphvSZxL4ujMdqVMibZnOiaFK2C5nKRGv407iaAsrI0CDICYVQJtiaITzkjfjbvrQ/132" width="30px"><span>有铭</span> 👍（2） 💬（1）<div>今天这文章将MapReduce复杂度问题让我豁然开朗，以前我总觉得很多讲MapReduce的文章，讲的轻描淡写的，颇有点“把冰箱门打开，把大象装进去，把冰箱门关上”的味道。我当初就觉得可能MapReduce没那么简单。</div>2019-04-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/0d/c1/d36816df.jpg" width="30px"><span>M</span> 👍（2） 💬（1）<div>请问文中所说的分片是指InputFormat读取数据时还是指shuffle时的分发？</div>2019-04-17</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTLdWHFCr66TzHS2CpCkiaRaDIk3tU5sKPry16Q7ic0mZZdy8LOCYc38wOmyv5RZico7icBVeaPX8X2jcw/132" width="30px"><span>JohnT3e</span> 👍（2） 💬（1）<div>如果处理逻辑和用户年龄相关，那么可以在原始年龄上加随机值的方式，尽可能散列。如果需要的话，后期再对结果进行合并。如果处理逻辑和年龄无关，那么可以选择散列性好的字段，比如用户唯一标识。在sharding时hash生成方面可以选取一些散列性好的算法，比如murmurhash算法。</div>2019-04-17</li><br/>
</ul>