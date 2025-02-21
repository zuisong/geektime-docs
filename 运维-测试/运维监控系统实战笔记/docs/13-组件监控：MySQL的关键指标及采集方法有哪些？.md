你好，我是秦晓辉。

按照[第 9 讲](https://time.geekbang.org/column/article/624099)介绍的监控分类方法，从这一讲开始，我们进入数据库中间件监控实战环节。这些组件里最常用的非MySQL莫属，这一讲我们就来介绍一下如何监控MySQL。学完今天的内容之后，你就知道MySQL中哪些指标比较关键以及如何采集这些指标了。这些指标能够帮助我们提早发现问题，提升数据库的可用性。

![图片](https://static001.geekbang.org/resource/image/1c/61/1c26d8db1e861c007a1a362db13ace61.png?wh=1744x1128)

## 整体思路

在正式学习之前，我们要先理清两个问题：监控哪类指标？如何采集数据？这两个问题是不是还挺熟悉的，我们[第 10 讲](https://time.geekbang.org/column/article/624263)系统地介绍过监控方法论，这些方法论应该如何落地呢？这一讲，我们就可以在MySQL中应用起来。MySQL是个服务，所以我们可以借用Google四个黄金指标的思路来解决问题。下面我们一起梳理一下。

![](https://static001.geekbang.org/resource/image/fb/44/fb5a50e976687376703a0b44c3166344.jpg?wh=2134x878)

### 延迟

应用程序会向MySQL发起SELECT、UPDATE等操作，处理这些请求花费了多久，是非常关键的，甚至我们还想知道具体是哪个SQL最慢，这样就可以有针对性地调优。我们应该如何采集这些延迟数据呢？典型的方法有三种。

1. **在客户端埋点**。即上层业务程序在请求MySQL的时候，记录一下每个SQL的请求耗时，把这些数据统一推给监控系统，监控系统就可以计算出平均延迟、95分位、99分位的延迟数据了。不过因为要埋点，对业务代码有一定侵入性。
2. **Slow queries**。MySQL提供了慢查询数量的统计指标，通过下面这段命令就可以拿到。
<div><strong>精选留言（12）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/10/25/87/f3a69d1b.jpg" width="30px"><span>peter</span> 👍（3） 💬（1）<div>请教老师几个问题：
Q1：怎么用 increase 函数计算慢查询的数量
Q2：MySQL最大连接数在生产环境中一般设置为多大？
Q3：Innodb_buffer_pool_reads 是从缓存读吗？
“reads 这个指标除以 read_requests 就得到了穿透比例”，从这句话看，此指标不是从缓存中读，而是从库里直接读（即从硬盘读）。但从名字看，似乎Innodb_buffer_pool_reads 应该是从缓存读。
Q4：中心化探测，categraf是只探测本身机器上的MySQL吗？ 还是说既探测本机上的MySQL也探测其他机器上的MySQL？
Q5：生产环境中MySQL不用docker或k8s吗？
这一句“因为生产环境里 MySQL 一般很少放到容器里跑”，从这句看，似乎生产环境中MySQL是手动部署，不用docker 或k8s，是吗？
Q6：本专栏有学习微信群吗？</div>2023-02-06</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/32/46/13/48ca967c.jpg" width="30px"><span>Camera</span> 👍（2） 💬（1）<div>秦老您好！想请教您两个问题：
1、项目要求需要做一套运维监控，想基于Prometheus来二开，请问作为产品（对运维没有相关经验），需要从哪方面下手来做产品设计呢？
2、运维系统的指标很多是需要通过配置文件配置，是否可将它可视化呢？
感谢老师指导一二！</div>2023-02-06</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/f2/73/1c7bceae.jpg" width="30px"><span>乔纳森</span> 👍（1） 💬（2）<div>老师您好，怎么根据黄金指标计算组件的SLI呢？以MySQL为例</div>2023-02-06</li><br/><li><img src="" width="30px"><span>Geek_81d2ba</span> 👍（0） 💬（1）<div>现在很多都开始使用云数据库，不再自己本机部署mysql了，这种情况下是不是业务方主要还是要主动探测数据库状态，另外我理解云上的数据库很多应该也是用容器化方式去部署的吧，一般这种云上的数据库监控采集难道是采用sidecar的方式吗</div>2023-12-05</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/8hAib3LaXCPfDTTw0Vibj8ajLm79ZaFGiaFic7dJHZlypFuMft1Q1UukA2vklSUAg7OBCK1Xo2TDxYibLyMj5LMdgEQ/132" width="30px"><span>y</span> 👍（0） 💬（1）<div>和mysqld_exporter对比，Categraf有啥优势的地方呢？</div>2023-10-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/c4/92/338b5609.jpg" width="30px"><span>Roy Liang</span> 👍（0） 💬（1）<div>现在云时代了，最大连接数、innodb buffer pool大小等该调优的参数云产品都替我们做了，这种情况下我们需要重点关注哪些指标呢？</div>2023-02-15</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/28/a1/d8/42252c48.jpg" width="30px"><span>123</span> 👍（0） 💬（1）<div>请教老师一个问题，如果一个数据库服务里面有多个实例，在自定义业务指标时如何去制定对应的实例，并书写sql</div>2023-02-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/07/8a/4bef6202.jpg" width="30px"><span>大叮当</span> 👍（0） 💬（1）<div>老师您好，请教两个问题：
Q1：怎么用 increase 函数计算慢查询的数量？
Q2：MySQL最大连接数在生产环境中一般设置为多大？</div>2023-02-06</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/54/21/0bac2254.jpg" width="30px"><span>橙汁</span> 👍（0） 💬（2）<div>这段话 “表里的时间度量指标都是以皮秒为单位。”是毫秒吧，另外学到不少知识 相当于拿四个指标以mysql为案例讲了下监控思路，最后还给出实际解决方案夜莺监控 可直接用，思路清晰 牛逼。
以前：监控就那些玩意 基础层有云 都是云 不用做什么
现在：思考的更多 业务层也大有可为</div>2023-02-06</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/DYAIOgq83er67Ir89QuLrOwHU7ruZoiaLUqibvB0NibSD19UxiaPT79ZrMIC48t2a5Ohaib7Vt8qW9ez6uMicFMclAibg/132" width="30px"><span>Geek_be4f4d</span> 👍（0） 💬（0）<div>老师您好，脑图中的performance_schema 中的schema单词是否拼写错误了？</div>2023-06-07</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/36/83/9c/bb76204a.jpg" width="30px"><span>时过境迁᭄ꦿ</span> 👍（0） 💬（0）<div>大佬们，这个监控mysql只在Categraf 针对 MySQL 的采集插件配置，在 conf&#47;input.mysql&#47;mysql.toml这个文件加上就好了吗，不能用Grafana</div>2023-04-07</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/f1/84/7d21bd9e.jpg" width="30px"><span>Goal</span> 👍（0） 💬（0）<div>这个都是夜莺为例吗</div>2023-02-16</li><br/>
</ul>