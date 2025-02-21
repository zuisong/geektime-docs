上一期，我讲了软件性能优化必须经过进行性能测试，并在了解软件架构和技术的基础上进行。今天，我们通过几个Spark性能优化的案例，看一看所讲的性能优化原则如何落地。如果你忘记了性能优化的原则，可以返回上一期复习一下。

基于软件性能优化原则和Spark的特点，Spark性能优化可以分解为下面几步。

1.性能测试，观察Spark性能特性和资源（CPU、Memory、Disk、Net）利用情况。

2.分析、寻找资源瓶颈。

3.分析系统架构、代码，发现资源利用关键所在，思考优化策略。

4.代码、架构、基础设施调优，优化、平衡资源利用。

5.性能测试，观察系统性能特性，是否达到优化目的，以及寻找下一个瓶颈点。

下面我们一起进入详细的案例分析，希望通过这几个案例，可以帮助你更好地理解Spark的原理，以及性能优化如何实践落地，希望能对你有所启发。

## 案例1：Spark任务文件初始化调优

首先进行性能测试，发现这个视频图谱N度级联关系应用分为5个job，最后一个job为保存结果到HDFS，其余job为同样计算过程的反复迭代。但是发现第一个job比其他job又多了个计算阶段stage，如图中红圈所示。

![](https://static001.geekbang.org/resource/image/6f/88/6fd436e3c6c11106cd7754792e78ee88.png?wh=670%2A206)

通过阅读程序代码，发现第一个job需要初始化一个空数组，从而产生了一个stage，但是这个stage在性能测试结果上显示，花费了14秒的时间，远远超出合理的预期范围。同时，发现这段时间网络通信也有一定开销，事实上只是内存数据初始化，代码上看不出需要进行网络通信的地方。下图是其中一台计算节点的通信开销，发现在第一个stage，写通信操作几乎没有，读通信操作大约每秒几十MB的传输速率。
<div><strong>精选留言（16）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/10/f9/e3/2529c7dd.jpg" width="30px"><span>吴科🍀</span> 👍（18） 💬（2）<div>我们公司集群作业最多的就是SQL作业约占80%，不管是hive SQL还是spark SQL，presto的SQL引擎都不是完美的，执行任务都有可能卡住99%就不动了。优化业务逻辑，SQL的写法是关键，减少重复计算，共用中间结果，还要有分区表的感念。</div>2018-12-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/78/a7/5b730eac.jpg" width="30px"><span>bill</span> 👍（13） 💬（3）<div>老师，文中的图是用什么软件得出的？</div>2018-12-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/38/19/c8d72c61.jpg" width="30px"><span>木白</span> 👍（3） 💬（1）<div>在第二个案例中说到，先注册的Executor可能会认领全部的任务，也就是说其所在的物理机会把那个stage的全部工作都做了吗？但是本着“移动计算比移动数据更划算的理论”，如果所有的任务都在一台机器上做岂不是会导致数据的移动？不知道我的理解有没有错哈</div>2019-01-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/37/d0/26975fba.jpg" width="30px"><span>西南偏北</span> 👍（0） 💬（1）<div>又看了一遍，觉得老师在代码方面功底很强！</div>2019-09-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/32/3f/fa4ac035.jpg" width="30px"><span>sunlight001</span> 👍（22） 💬（1）<div>在公司里没有接触大数据的机会，要想深入学习的话，需要怎么办呢，现在不管是看书，看demo，等总是感觉不深入，有什么好的办法吗</div>2018-12-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/cb/50/66d0bd7f.jpg" width="30px"><span>杰之7</span> 👍（8） 💬（0）<div>通过这节的阅读学习，通过第一个大数据实战产品，了解了性能调优的一般流程，通过性能测试，分析资源瓶颈，分析系统架构及代码，通过架构，代码及基础设施来进行调优，最后在进行测试。

老师通过5个方面进行的分析说明，1，Spark任务文件初始化调优，2，Spark任务调度优化，3，Spark应用配置优化，4，操作系统优化，5，硬件优化。通过这些维度的分析，我进一步的知道，做大数据开发，一样需要有好的计算机基本功，这是每一个技术人员的底层能力。

所以大数据开发中都会涉及到硬件，系统，大数据产品及其配置，应用程序开发和部署等实际经验，学习到这里，我需要真正做一判断，是真正决定走技术路，在接下来至少10年的时间去做技术呢？还是为了仅仅熟悉大数据方面的知识，适可而止呢？

我作为一名平凡而不想平庸的人，过程中再难我也会一路前行。</div>2018-12-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/88/e0/292508a4.jpg" width="30px"><span>Knuth</span> 👍（5） 💬（0）<div>操作系统究竟在忙什么，占用了这么多 CPU 时间？通过跟踪 Linux 内核执行指令。。。。。。。。。
具体是怎么发现的呢，可以列一下详细的步骤么？</div>2020-03-01</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTKugZjntLzMGvDicZaX7pAuwNw3aneI2zZlicKh0fqsmmlJ9VRrSjBBJc1m8K6CPuV6WQuHic4zNZT8Q/132" width="30px"><span>Geek_vqdpe4</span> 👍（3） 💬（1）<div>1.第一个案例的代码，关于文件锁的范围，我有强迫症，就是把锁的范围再缩小一点，仅仅锁住判断下载的那段代码就好啦。
2.关于案例5，我有点看不懂网络使用率的图，为什么是50多秒的延迟，能不能用红圈圈一下。</div>2018-12-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/da/ec/779c1a78.jpg" width="30px"><span>往事随风，顺其自然</span> 👍（3） 💬（0）<div>怎么实现操作的，讲解安利有什么具体指标？超过多少算不合理</div>2018-12-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/87/25/898dea4e.jpg" width="30px"><span>桃园悠然在</span> 👍（2） 💬（0）<div>第三步【分析系统架构、代码，发现资源利用关键所在，思考优化策略】思考过程中可以拿阿姆达尔法则做指引，选出优化收益最大的模块
</div>2018-12-13</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTLVxdKpjGwBPCyWkyoSib5YzHelnLPVhSEmDiaNEZy8OYOfBgRictaHXNqHJuOrMBff33orIHLINTc2Q/132" width="30px"><span>郭兰杰</span> 👍（1） 💬（0）<div>有啥比较推荐的开源性能监测工具吗？</div>2020-06-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/2f/b4/35a23718.jpg" width="30px"><span>zhaixc</span> 👍（0） 💬（0）<div>关于应用程序的优化：
hadoop三台服务器启动三个节点计算数据，发现只有一个节点在计算，排查发现，Map阶段的key全分配到同一台机器上了，后来从新设计key生成规则，平均分配到三台机器上，达到资源最优利用。</div>2024-01-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/67/f4/9a1feb59.jpg" width="30px"><span>钱</span> 👍（0） 💬（0）<div>😜还没实际用大数据的东西，先自己开阔视野学习学习。</div>2019-09-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/2f/f4/2dede51a.jpg" width="30px"><span>小老鼠</span> 👍（0） 💬（0）<div>1、你们用的是什么性能测试工具？
2、hadoop、spark是用java语言开发的吗？若是现在支持JDK9吗？</div>2019-01-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/cc/f3/5e4b0315.jpg" width="30px"><span>追梦小乐</span> 👍（0） 💬（0）<div>李老师，案例2中说的 Worker 提供的计算单元数   默认是有几十个的吗？同时是不是可以根据spark.default.parallelism这个来指定的吗？</div>2018-12-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/da/ec/779c1a78.jpg" width="30px"><span>往事随风，顺其自然</span> 👍（0） 💬（0）<div>代码直接提交到apache?为什么不能直接下找</div>2018-12-13</li><br/>
</ul>