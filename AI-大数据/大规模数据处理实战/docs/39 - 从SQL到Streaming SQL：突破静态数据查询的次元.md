你好，我是蔡元楠。

今天我要与你分享的主题是“从SQL到Streaming SQL：突破静态数据查询的次元”。

在前面的章节中，我们介绍了一些流数据处理相关的知识和技术，比如Apache Spark的流处理模块——Spark Streaming和Structured Streaming，以及Apache Beam中的窗口处理。相信你对流处理的重要性和一些基本手段都有所了解了。

流处理之所以重要，是因为现在是个数据爆炸的时代，大部分数据源是每时每刻都在更新的，数据处理系统对时效性的要求都很高。作为当代和未来的数据处理架构师，我们势必要深刻掌握流数据处理的技能。

“批”“流”两手抓，两手都要硬。

你还记得，我在[第15讲](https://time.geekbang.org/column/article/96256)中介绍过的Spark SQL吗？它最大的优点就是DataFrame/DataSet是高级API，提供类似于SQL的query接口，方便熟悉关系型数据库的开发人员使用。

当说到批处理的时候，我们第一个想到的工具就是SQL，因为基本上每个数据从业者都懂，而且它的语法简单易懂，方便使用。那么，你也能很自然地联想到，如果在流处理的世界中也可以用SQL，或者相似的语言，那真是太棒了。

这样的思想在[第17讲](https://time.geekbang.org/column/article/97121)中我们曾经提到过。
<div><strong>精选留言（7）</strong></div><ul>
<li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/DYAIOgq83eqTwSGXttkspRF37CTYQvVsibWicKJDtseiaE3DibfsSAHiaFM2Iwb04hg3O0Bq9JfG358A7Tlhia6vAhDw/132" width="30px"><span>Hobbin</span> 👍（5） 💬（0）<div>当前复杂的逻辑，Streaming SQL的支持还是比较有限的。请教一下，Streaming SQL有没有可能完全替代API开发方式呢？</div>2019-07-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/23/1c/a00aed90.jpg" width="30px"><span>小火柴</span> 👍（2） 💬（0）<div>现实开发中会遇到比如有的客户端网络条件不是很好，不能实时发送数据，会把数据存在本地等网络良好时候再发送给服务器。这样的情况实时处理如果用水印的话就会丢失很多数据</div>2019-10-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/19/70/3d/93aa82b6.jpg" width="30px"><span>Junjie.M</span> 👍（1） 💬（0）<div>请问beam有统一的streaming sql可以转换成其他runner运行吗</div>2020-04-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/29/44/3c/8bb9e8b4.jpg" width="30px"><span>Mr.Tree</span> 👍（0） 💬（0）<div>感觉sql是最好用的数据处理语言，在数据处理这块儿会不会sql实现统一化</div>2023-01-02</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/47/00/3202bdf0.jpg" width="30px"><span>piboye</span> 👍（0） 💬（0）<div>sql有没可能统一大数据的处理？</div>2021-12-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/45/20/24867e59.jpg" width="30px"><span>正向成长</span> 👍（0） 💬（0）<div>Streaming SQL从快速入手实操的角度来看有很大的意义，SQL语句的优化查询，尤其是随着数据规模日益庞大，性能应该是比较大的瓶颈吧，分布式系统存储，事务的实现？</div>2020-11-07</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/55/99/4bdadfd3.jpg" width="30px"><span>Chloe</span> 👍（0） 💬（0）<div>谢谢老师的讲解，深受启发。请问Siddihi Streaming SQL是目前比较推荐的Streaming SQL吗？老师您觉得这种streaming SQL的发展前景如何？</div>2020-02-18</li><br/>
</ul>