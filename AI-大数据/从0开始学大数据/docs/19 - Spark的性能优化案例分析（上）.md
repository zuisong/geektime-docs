我们知道，现在最主流的大数据技术几乎都是开源的产品，不管是Hadoop这样的大数据存储与计算产品，还是Hive、Spark SQL这样的大数据仓库，又或者Storm、Flink这样的大数据流计算产品，还有Mahout、MLlib这样的大数据机器学习算法库，它们都来自开源社区。所以，我们在使用大数据、学习大数据的过程中肯定少不了要和开源社区打交道。

我在Intel工作期间主要工作就是参与Apache开源社区的大数据项目开发，其实上一期我讲的Panthera最初也是准备为Hive项目增强标准SQL处理能力而开发，但是因为和Apache Hive项目管理方在开发理念上的冲突，最终选择独立开源。后来我又参与了Apache Spark的开发，为Spark源代码提交了一些性能优化的Patch。我想通过专栏两期的内容，具体介绍一下如何参与Apache这样开源社区的软件开发，如何进行软件性能优化，以及我在Apache Spark源码上做的一些优化实践。

一方面我希望你能借此更深入、系统地了解软件性能优化；另一方面也可以更深入了解Spark的一些运行机制，同时也可以了解Apache开源社区的运作模式。因为我们在使用各类大数据产品的时候，一定会遇到各种问题，想要解决这些问题，你可以直接到官方的开源社区去求助并寻找答案。在使用过程中，如果这些大数据产品不能满足你的需求，你可以阅读源代码并直接对源代码进行修改和优化。因为你在实践过程中产生的需求可能其他人也会有，你可以将你修改的源代码提交到开源社区，请求合并到发布版本上，供全世界开发者使用。这也是开源最大的魅力。
<div><strong>精选留言（22）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/13/52/3e/a0614b62.jpg" width="30px"><span>Jack Zhu</span> 👍（28） 💬（1）<div>确定问题细节原因，针对主要问题进行解决
1.如是网卡接入能力不够，则需要更换网卡或增加网卡
2.如是网卡--应用之间的io瓶颈，则需要考虑零拷贝减少copy释放性能，使用大页内存减少页表miss，使用专门核心做收包缓存到软队列等

</div>2018-12-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/32/3f/fa4ac035.jpg" width="30px"><span>sunlight001</span> 👍（7） 💬（1）<div>考虑传输压缩，牺牲cpu的办法了</div>2018-12-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/64/86/f5a9403a.jpg" width="30px"><span>yang</span> 👍（5） 💬（1）<div>1.批量发送数据
2.压缩传输数据
3.增加带宽

还有咩？</div>2018-12-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/4b/b4/4768f34b.jpg" width="30px"><span>旭</span> 👍（3） 💬（1）<div>请问文中的几个性能测试的图怎么快速生成呢？</div>2018-12-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/4f/b2/1e8b5616.jpg" width="30px"><span>老男孩</span> 👍（2） 💬（2）<div>因为我对 hadoop,spark也是跟随专栏在学习。不知道计算过程中节点之间通信是一种什么方式？是否可以采用netty这样的网络框架，因为netty的数据读写都是在bytebuf中进行的。而且我们可以自定义channelHandler在数据出站入站的时候编解码，压缩解压。</div>2018-12-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/df/73/4a4ce2b5.jpg" width="30px"><span>足迹</span> 👍（2） 💬（1）<div>硬件上可以升级网卡，比如百兆升级到千兆；
软件上看看是否可以新的版本可以解决；
逻辑上最关键，尽量做到数据本地性，能本地算好的一定不传输到其他节点。</div>2018-12-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/db/7d/1fbad49b.jpg" width="30px"><span>John</span> 👍（0） 💬（1）<div>李老师，我想请教下，Impala 和 Hive 的应用场景区别，换句话，就是什么时候用 Impala 比 Hive 有优势？谢谢</div>2018-12-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/96/6d/86a3f9c3.jpg" width="30px"><span>linazi</span> 👍（0） 💬（1）<div>老师 spark图谱如何生成那几个性能测试图</div>2018-12-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/67/f4/9a1feb59.jpg" width="30px"><span>钱</span> 👍（34） 💬（0）<div>1：换更强劲的网卡，千兆换万兆试试
2：减少数据量，压缩数据，用CPU计算能力减空间
3：减少IO次数，批量发送数据
4：从业务逻辑下手，看看是否可以优化逻辑减少IO，或者减少数据量
5：看看网络是否共享，不是自己的流量打满的网卡，如果是，采用独占的资源使用方式
6：换一种方式，只发送必要的信息，将计算迁移到接收消息的机器上，或者部分迁移计算逻辑</div>2019-09-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/cb/50/66d0bd7f.jpg" width="30px"><span>杰之7</span> 👍（12） 💬（0）<div>		学习完基础篇，来学实战篇的Spark性能优化课程。通过这篇文章的阅读，无论是开源的软件，还是收费的软件，基本上都是被美国人开发出来的，至少这点上我们的路还很远，对于我自身，通过我的学习和实践，我希望至少能通过我的努力做到我想做的数据开发的工作。
		通过对这节内容的阅读，熟悉了开源软件的管理平台Apache,我们可以通过提交自己的代码到开源平台上，一旦经过Commiter通过，我们就是这个开源平台的Contributor。
		在软件性能优化上，不经过性能测试的软件不要优化，不懂其架构设计的软件不要进行性优化。因为性能测试包括多维度的指标，没有对比，何来优化，不懂架构设计，也不可能真正知道性能瓶颈在哪里。基于此，老师讲述了讲述了大数据软件优化的方向，SQL语句的优化，数据倾斜处理，也就是对不需要的数据剔除，Mapreduce、Spark代码优化，因为这些软件是开源，厉害的人就能针对公司具体的产品业务做源码的修改。通过配置参数的优化，也是运维工程师正做的事。
		总之，我们可以通过自己的一点点的努力让自己有那么一点点价值，能做对这个世界上一点有用的东西吧，这就够了。
</div>2018-12-11</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/6uQj0EmXTGstVxNicLWqJhGvY0tavWvxK5RwgxjaMK1rNB9Rf7kAdnzBnG7YOicHjTibOf6G6HEFwonRFXDN3Pp8A/132" width="30px"><span>葛聂</span> 👍（4） 💬（0）<div>1. in网络打满：增加locality,尽量访问本地数据
2. out网络打满：优化代码或数据，看能否提前合并减少发送的数据量
3. 优化container摆放策略或并发数，避免热点</div>2018-12-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/82/f3/01bf3b3e.jpg" width="30px"><span>王亚南</span> 👍（2） 💬（0）<div>经常等待IO，可以考虑使用异步非阻塞IO模型，集体就是建立IO池，从多个链接读入数据，供系统处理。</div>2018-12-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/f5/c5/c9a67483.jpg" width="30px"><span>Oliver</span> 👍（1） 💬（0）<div>看到问题后先思考了一下，发现和大家的思路比较一致，分两点看
1、网卡打满
    1）能否拆分业务执行时间点，因为是性能测试，pass
    2）优化业务逻辑
    3）能否批量发送
    4）升级网络硬件
2、系统等待
    1）同步IO改为IO多路复用或异步IO</div>2018-12-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/d6/46/5eb5261b.jpg" width="30px"><span>Sudouble</span> 👍（0） 💬（0）<div>1. 如果是网卡性能不够，升级网卡
2. 改进系统架构，改为分布式结构，将不同机器的负载进行均衡
3. 如果是应用软件产生的瓶颈，优化数据的通信协议或通讯机制，精简数据量
4. 结合其他留言，牺牲一部分CPU资源和内存资源，进行数据压缩</div>2022-09-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/19/e3/d7/d7b3505f.jpg" width="30px"><span>官</span> 👍（0） 💬（0）<div>升级网卡，使用更强劲性能的网卡。优化I&#47;O操作，减少不必要I&#47;O次数。优化数据结构，从源头上减少冗余数据的传输。</div>2020-07-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/19/a6/7ae63d7e.jpg" width="30px"><span>Jun</span> 👍（0） 💬（0）<div>关于网卡问题，从硬件角度可以升级带宽和增加网卡。从操作系统角度可以调节网络相关参数。从数据角度可以考虑数据本地性，即让计算节点尽量计算本地或者最近节点上的数据。还有就是reduce可以在做map的节点上先做，传输中间结果到reduce节点上汇总。这样可以减少网络传输</div>2020-01-04</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/03/1e/f605f4a9.jpg" width="30px"><span>吕宗霖</span> 👍（0） 💬（0）<div>Doris不是百度的Palo么？</div>2019-09-02</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/fe/c6/0e382962.jpg" width="30px"><span>iK_Leehom</span> 👍（0） 💬（0）<div>网卡可以比作一条水管，可以从两个角度出发，要么减少水量，要么增加水管</div>2019-05-07</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/21/19/50085e26.jpg" width="30px"><span>张云翔</span> 👍（0） 💬（0）<div>针对业务进行分析 尽量不使用shuffle算子 减少网络开销</div>2019-02-07</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/93/ba/45d127b8.jpg" width="30px"><span>Lev</span> 👍（0） 💬（0）<div>明早是用尽了网卡的能力了，也就是网络瓶颈。
两个方面，
第一，提高网卡的能力，换个方式就是更换更强劲的网卡。
第二，减少程序对网络的请求的压力，具体为频率和数据量。频率可以通过类似程序限流，数据量可以通过调整传输数据格式，协议，达到更小传输，这包括压缩数据，使用简化编码等方式传输更少的数据</div>2019-02-03</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/2f/f4/2dede51a.jpg" width="30px"><span>小老鼠</span> 👍（0） 💬（0）<div>压缩传输或者更换高质量网卡</div>2019-01-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/1a/e2/9e59dd38.jpg" width="30px"><span>修行者</span> 👍（0） 💬（0）<div>我第一想法，首先是带宽是否不够</div>2018-12-13</li><br/>
</ul>