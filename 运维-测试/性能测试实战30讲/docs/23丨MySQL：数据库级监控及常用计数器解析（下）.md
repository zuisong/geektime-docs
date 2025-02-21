上一篇文章中，我们讲了有关数据库的全局分析，那么在今天的文章中，我们继续看看在数据库中，如何做定向分析。

还记得我在上篇文章中提到的工具吗？mysqlreport、pt-query-digest和mysql\_exportor+Prometheus+Grafana。我们在上一篇中已经讲完了mysqlreport，今天我们来看看剩下的这几个。

## 定向抓取SQL：pt-query-digest

`pt-query-digest`是个挺好的工具，它可以分析`slow log`、`general log`、`binary log`，还能分析tcpdump抓取的MySQL协议数据，可见这个工具有多强大。`pt-query-digest`属于Percona-tool工具集，这个Percona公司还出了好几个特别好使的监控MySQL的工具。

`pt-query-digest`分析slow log时产生的报告逻辑非常清晰，并且数据也比较完整。执行命令后就会生成一个报告。

我来稍微解释一下这个报告。我们先看这个报告的第一个部分：

```
# 88.3s user time, 2.5s system time, 18.73M rss, 2.35G vsz
# Current date: Thu Jun 22 11:30:02 2017
# Hostname: localhost
# Files: /Users/Zee/Downloads/log/10.21.0.30/4001/TENCENT64-slow.log.last
# Overall: 210.18k total, 43 unique, 0.26 QPS, 0.14x concurrency _________
# Time range: 2017-06-12 21:20:51 to 2017-06-22 09:26:38
# Attribute          total     min     max     avg     95%  stddev  median
# ============     ======= ======= ======= ======= ======= ======= =======
# Exec time        118079s   100ms      9s   562ms      2s   612ms   293ms
# Lock time            15s       0     7ms    71us   119us    38us    69us
# Rows sent          1.91M       0  48.42k    9.53   23.65  140.48    2.90
# Rows examine      13.99G       0   3.76M  69.79k 101.89k  33.28k  68.96k
# Rows affecte       3.36M       0   1.98M   16.76    0.99   4.90k       0
# Query size       102.82M       6  10.96k  512.99  719.66  265.43  719.66
```

从上表中可以看得出来，在这个慢日志中，总执行时间达到了118079s，平均执行时间为562ms，最长执行时间为9s，标准方差为612ms。
<div><strong>精选留言（19）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/11/f6/55/b3ab84a2.jpg" width="30px"><span>张红占</span> 👍（13） 💬（1）<div>干货太多了，课程价格严重低估了！</div>2020-02-14</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTJGXndj5N66z9BL1ic9GibZzWWgoVeWaWTL2XUnCYic7iba2kAEvN9WfjmlXELD5lqt8IJ1P023N5ZWicg/132" width="30px"><span>Geek_f93234</span> 👍（10） 💬（1）<div>数据库分析的大体思路是什么吗？
全局分析--定向分析
1.全局分析：分析数据库硬件配置，数据库配置，SQL语句，采用全局监控工具如mysqlreport工具收集到的测试数据，分析可能存在的问题；
2.定向分析：如：针慢查询导致的性能问题，采用pt-query-digest工具分析慢查询日志抓取存在问题的sql，利用profiling分析sql语句的每一个层级，查看sql执行计划,对sql进行优化。

如何在数据库中迅速找到一个慢 SQL 的根本原因呢？
profiling分析sql语句的每一个层级，结合sql语句执行计划分析慢sql根本原因</div>2020-02-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/19/85/e2/540b91fa.jpg" width="30px"><span>凯耐</span> 👍（3） 💬（1）<div>数据库慢SQL分析基本思路：
1.配置慢sql条件，将满足条件的sql写入慢查询日志
2.通过explain工具解析sql，判断是否加了索引或索引是否失效
3.如果没有索引，在数据表添加合适的索引，再执行sql，看执行时间。
4.添加索引sql执行时间没有优化那就从sql编写逻辑过于复杂导致查询过慢
5.当然硬件配置，数据库配置都会影响数据库sql的执行时间</div>2021-03-12</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/DYAIOgq83erdesQy0moaicYTicoHRQXzbmJm15wohb77qD1OdbuSqPCSUerbcZHzxJJunfmEhTx4kBLxbGaxQ9iag/132" width="30px"><span>村夫</span> 👍（2） 💬（1）<div>老师，网上都建议Mysql要关闭query cache，我看您的示例是开启呢，所以执行同一个sql会读缓存。如果关闭了，偷懒的办法是没有用的吧</div>2020-03-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/17/96/3e/2295581a.jpg" width="30px"><span>程科长</span> 👍（1） 💬（1）<div>问题一：
先全局，在定向分析
问题二：
profiling，它可以把 SQL 执行的每一个步骤详细列出来，从一个 SQL 进入到数据库中，到执行完这整个生命周期。
MySQL 的profiling在session级生效，所以当你用了慢日志，知道哪个 SQL 有问题之后，再用这个功能是最见成效的。</div>2022-04-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/7e/3e/82202cc8.jpg" width="30px"><span>月亮和六便士</span> 👍（1） 💬（1）<div>看完昨天和今天的专栏，我有个想法，不管三七二十一，一上来先把慢日志拎出来，分析，然后执行计划，三板斧耍完了，然后在开始工作......</div>2020-03-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/b6/a2/c7ec1355.jpg" width="30px"><span>乐少</span> 👍（0） 💬（1）<div>老师哪里可以加微信群，也要学习下</div>2024-02-16</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/DYAIOgq83eoWfXendN7czHpsyaWKLPK6Na9P5czquJ7Wdre4TibZQ5SQib88edyuib3LpCVFkp0gII2wyvvR8tEIA/132" width="30px"><span>OM</span> 👍（0） 💬（1）<div>数据库方面的性能诊断涉及操作系统层,网络层,存储层,应用层，通常将关联数据库的其他层通过诊断分析确定是否与数据库有关系,缩小诊断范围和找到性能问题症结。</div>2023-08-02</li><br/><li><img src="" width="30px"><span>Geek_33192c</span> 👍（0） 💬（1）<div>初学者得从哪里学起</div>2023-03-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/01/b9/73435279.jpg" width="30px"><span>学习学个屁</span> 👍（0） 💬（1）<div>mac 如何安装 pt-query-digest  总是安装不成功</div>2021-09-25</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/01/b9/73435279.jpg" width="30px"><span>学习学个屁</span> 👍（0） 💬（1）<div>这些工具有搭建教程吗老师</div>2021-09-25</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/d9/36/92d8eb91.jpg" width="30px"><span>Promise</span> 👍（0） 💬（2）<div>老师mysql_exportor+Prometheus+Grafana这一套有搭建流程吗</div>2021-09-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/17/58/3b/22dbe7c3.jpg" width="30px"><span>LQQ</span> 👍（0） 💬（1）<div>老师，上文中提到 ID尾号为449F的sql 日志，标准差为823ms，95线为2s，平均值为957ms，如果是正态分布，根据标准差的定义，68%的请求应该在100ms~1780ms之间，您说的是大多数请求在100ms~1s内，可能是我太较真了，特意算了一下^_^</div>2020-07-01</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/7e/3e/82202cc8.jpg" width="30px"><span>月亮和六便士</span> 👍（0） 💬（1）<div>老师，哪可以看到MySQL- grafana 里面各个指标的详细解释，现在看到指标一脸懵逼，不知道哪个指标什么意思，值到了多少代表有问题，应该怎么办？怎么破解</div>2020-04-25</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/DYAIOgq83erdesQy0moaicYTicoHRQXzbmJm15wohb77qD1OdbuSqPCSUerbcZHzxJJunfmEhTx4kBLxbGaxQ9iag/132" width="30px"><span>村夫</span> 👍（0） 💬（1）<div>老师我看show profile在5.7以后就被废弃了，还有就是我同一个sql执行多次，通过show prorile查看每次queryId，步骤差不多呀。不知道为啥呢？</div>2020-03-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/2f/f4/2dede51a.jpg" width="30px"><span>小老鼠</span> 👍（0） 💬（1）<div>如何确定引起系统慢的原因是DB，是否可从OS分析入手？</div>2020-03-09</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/DYAIOgq83er3G5DWFp5PEklibQPYE1m8OxtYqTcryibkcUHpP4ibBicf8OUYHB6V1iaSRaNiaFV8cuNFb0xbOUF7mZhQ/132" width="30px"><span>Duke</span> 👍（0） 💬（1）<div>干活太多，我得看看吸收！</div>2020-02-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/2a/04/63/80aa615f.jpg" width="30px"><span>陈星</span> 👍（0） 💬（0）<div>percona monitor and manager</div>2025-01-01</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/57/6e/b6795c44.jpg" width="30px"><span>夜空中最亮的星</span> 👍（0） 💬（0）<div>好好在家呆着学习 那也不去</div>2020-02-13</li><br/>
</ul>