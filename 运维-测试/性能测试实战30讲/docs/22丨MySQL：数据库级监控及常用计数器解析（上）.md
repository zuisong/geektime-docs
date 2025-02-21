数据库是一个非常大的话题，我们在很多地方，都会看到对数据库的性能分析会包括以下部分。

![](https://static001.geekbang.org/resource/image/17/40/178e637e4723e37abb7eb9d477d20f40.png?wh=1667%2A856)

但其实呢，以上这些内容都是我们应该具备的基础知识，所以我今天要讲的就是，具备了这些基础知识之后我们应该干什么事情。

也就是说，从性能瓶颈判断分析的角度入手，才是性能从业人员该有的逻辑。每次我分析一个性能问题时，逻辑总是这样的：

![](https://static001.geekbang.org/resource/image/62/ab/625d1ec2717f84cb2dc9119d8c7e43ab.jpg?wh=1947%2A1431)

1. 先画出整个系统的架构图。
2. 列出整个系统中用到了哪些组件。这一步要确定用哪些监控工具来收集数据，具体的内容你可以看下之前讲到的监控设计相关的内容。
3. 掌握每个组件的架构图。在这一步中需要列出它们的关键性能配置参数。
4. 在压力场景执行的过程中收集状态计数器。
5. 通过分析思路画出性能瓶颈的分析决策树。
6. 找到问题的根本原因。
7. 提出解决方案并评估每个方案的优缺点和成本。

这是我一直强调的分析决策树的创建逻辑。有了这些步骤之后，即使不熟悉一个系统，你也可以进行性能分析。

对于MySQL数据库来说，我们想对它进行分析，同样也需要看它的架构图。如下图所示（这是MySQL5版本的架构示意图）：

![](https://static001.geekbang.org/resource/image/34/42/34c20915477740cac9cfa18aa7114542.png?wh=799%2A673)

这里就有一个问题了：看架构图是看什么？这个图够细吗？

首先，看架构图，一开始肯定是看大而全的架构。比如说上图，我们知道了，MySQL中有Connection Pool、SQL Interface、Parser等这些大的模块。
<div><strong>精选留言（13）</strong></div><ul>
<li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTJGXndj5N66z9BL1ic9GibZzWWgoVeWaWTL2XUnCYic7iba2kAEvN9WfjmlXELD5lqt8IJ1P023N5ZWicg/132" width="30px"><span>Geek_f93234</span> 👍（12） 💬（1）<div>MySQL 中全局监控工具可以给我们提供哪些信息？
索引报表、操作报表、查询和排序报表、查询缓存报表、表锁报表、表信息报表、连接报表和临时报表、线程报表、innodb缓存池报表、innodb锁报表、
如何判断 MySQL 状态值和配置值之间的关系呢？
SHOW GLOBAL VARIABLES;用来查看配置的参数值，和SHOW GLOBAL status;用来查询状态值
测试结束后通过mysql监控工具查看和分析状态值，从而判断数据库配置值是否合理</div>2020-02-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1a/9f/c2/3d1c2f88.jpg" width="30px"><span>蔡森冉</span> 👍（11） 💬（1）<div>看到这里真是测试方向从一个坑到另一个坑的过程，没有开发基础真的不行，前两天刚搞jmeter+influxdb++grafana，接着是找了系统监控相关的代码和中间件基本上不了解，然后到数据库。这个过程中数据库中数据拿到如何看看完这篇了解了一些。但是回想一下前面几个怎么分析又完全被不知道了。分析每一个方面的需要关注的数据如何分析，这成为了最难的学习内容，就像老师常说工具不重要，关键得到我们想要的，但是对我来说就是图形数据出来了，但是对我就是一堆数据，分析过程关注点，还有场景不同会有什么结果，数据什么场景，正常数据应该是什么样，脑中十万个为什么。。。</div>2020-03-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/77/72/8f77ddb0.jpg" width="30px"><span>johnny</span> 👍（4） 💬（1）<div>老师，我是这样理解的，理解不对的地方老师帮我纠正一下。
如何判断 MySQL 状态值和配置值之间的关系呢？
状态值和配置值：
状态值也称为状态计数器，可以通过show global status命令来查看有哪些状态计数器。
配置值也称为配置参数，可以通过show global variables命令来查看有哪些配置参数。
两者关系：
状态值一定程度上反映了配置值的合理性。
比如Max_used_connections是一个状态值，它反映了配置值max_connections的合理性；
在比如Open_tables是一个状态值，它反映了配置值table_open_cache的合理性，但是不能看到Open_tables过高就去调整table_open_cache，因为有可能是其它原因导致的。
所以说分析状态值超过既定指标的原因，我们除了要分析配置值外，还要分析sql语句或者其它组件。</div>2021-06-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/17/58/3b/22dbe7c3.jpg" width="30px"><span>LQQ</span> 👍（4） 💬（1）<div>老师 请教一个问题，文中提到的状态计数器、打开表、查询缓存等数据给刷新一下，具体怎么刷新？</div>2020-06-30</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1b/42/9f/428dbb20.jpg" width="30px"><span>新思维</span> 👍（4） 💬（1）<div>看完文章觉得对一个性能测试工程师的要求太高了，需要把报表中的每个参数的意思都得搞懂，达到了对DBA的要求</div>2020-03-15</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTJJ6G2xZvNRmhyXBjmGbI5G8icGCCMPupr6yxZ1IcURwp7GTRHcpWGWpg9A0fLlyicmVdDwzqZqwiaOQ/132" width="30px"><span>jy</span> 👍（1） 💬（1）<div>老师，请教下：文中“在这个性能场景中，慢日志太多了，需要定向监控看慢 SQL，找到慢 SQL 的执行计划”，是不是需要先把慢查询日志开启？设置慢查询的阈值？ 这样才可以在全局监控中看到有慢日志</div>2021-05-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/38/2d/9c971119.jpg" width="30px"><span>若丶相依</span> 👍（1） 💬（1）<div>运维看的津津有味。</div>2020-10-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/7e/3e/82202cc8.jpg" width="30px"><span>月亮和六便士</span> 👍（1） 💬（1）<div>老师，一条SQL语句（插入语句）单执行特别快，高并发很慢，这种情况是不是锁等待造成的？还是老规矩看执行计划？</div>2020-04-25</li><br/><li><img src="" width="30px"><span>廖志勇</span> 👍（0） 💬（1）<div>你好，老师 ，有两个问题请教下：
1、mysqlreport 是否需要管理员权限（网上没有找到相关资料）。我们数据库管的严，管理源权限不开放，查询出来的结果始终不变的，比如开启慢查询了，但是慢查询比例一直为0。但是查apm工具，明显有慢sql
2、我们的数据库服务器有个多个项目数据库，mysqreport 只能是查询整个数据库服务器的数据指标？是否可以统计特点的项目库指标？</div>2022-10-23</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/DYAIOgq83eovjNRNjPcwyoVfLELrqEdLiazqeZyDgvsFGQ7sEXhbmSuFSiarWvy3an1FHbcPhlWBQEXguh3msJdg/132" width="30px"><span>问号和感叹号</span> 👍（0） 💬（1）<div>mysqlreport怎么安装呢 windows和linux下都尝试过 各种不成功。。。</div>2022-07-04</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTIUw2n2cOLticrdgJWu5ibM1Hib58XNRt5jQwRibT27ZLvqKvsPoZDicrFmUic2GF9vtI2EjgMWVpiatwgFw/132" width="30px"><span>Geek_f9e0e5</span> 👍（0） 💬（2）<div>oracle就看AWR么</div>2021-03-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1a/06/ab/ba20f342.jpg" width="30px"><span>餘生</span> 👍（0） 💬（1）<div>我在公司测试用elk就可以监控到慢查询的语句，还有其他监控工具能看到主从库延迟那些是不是就够了</div>2020-03-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/2f/f4/2dede51a.jpg" width="30px"><span>小老鼠</span> 👍（0） 💬（2）<div>1，模糊查询的SQL为select * from paper where title like ‘%var%’，这个是全表扫描的，性能肯定不好，有没有更好的解决方案？2,对于数据库读写分离的架构，有什么办法提高性能？</div>2020-03-04</li><br/>
</ul>