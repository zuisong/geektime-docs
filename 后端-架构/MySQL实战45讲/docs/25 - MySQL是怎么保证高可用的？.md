在上一篇文章中，我和你介绍了binlog的基本内容，在一个主备关系中，每个备库接收主库的binlog并执行。

正常情况下，只要主库执行更新生成的所有binlog，都可以传到备库并被正确地执行，备库就能达到跟主库一致的状态，这就是最终一致性。

但是，MySQL要提供高可用能力，只有最终一致性是不够的。为什么这么说呢？今天我就着重和你分析一下。

这里，我再放一次上一篇文章中讲到的双M结构的主备切换流程图。

![](https://static001.geekbang.org/resource/image/89/cc/89290bbcf454ff9a3dc5de42a85a69cc.png?wh=1142%2A880)

图 1 MySQL主备切换流程--双M结构

# 主备延迟

主备切换可能是一个主动运维动作，比如软件升级、主库所在机器按计划下线等，也可能是被动操作，比如主库所在机器掉电。

接下来，我们先一起看看主动切换的场景。

在介绍主动切换流程的详细步骤之前，我要先跟你说明一个概念，即“同步延迟”。与数据同步有关的时间点主要包括以下三个：

1. 主库A执行完成一个事务，写入binlog，我们把这个时刻记为T1;
2. 之后传给备库B，我们把备库B接收完这个binlog的时刻记为T2;
3. 备库B执行完成这个事务，我们把这个时刻记为T3。

所谓主备延迟，就是同一个事务，在备库执行完成的时间和主库执行完成的时间之间的差值，也就是T3-T1。

你可以在备库上执行show slave status命令，它的返回结果里面会显示seconds\_behind\_master，用于表示当前备库延迟了多少秒。
<div><strong>精选留言（30）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/13/f8/70/f3a33a14.jpg" width="30px"><span>某、人</span> 👍（202） 💬（15）<div>遇到过下面几种造成主从延迟的情况:
1.主库DML语句并发大,从库qps高
2.从库服务器配置差或者一台服务器上几台从库(资源竞争激烈,特别是io)
3.主库和从库的参数配置不一样
4.大事务(DDL,我觉得DDL也相当于一个大事务)
5.从库上在进行备份操作
6.表上无主键的情况(主库利用索引更改数据,备库回放只能用全表扫描,这种情况可以调整slave_rows_search_algorithms参数适当优化下)
7.设置的是延迟备库
8.备库空间不足的情况下

这期的问题：
看这曲线,应该是从库正在应用一个大事务,或者一个大表上无主键的情况(有该表的更新)
应该是T3随着时间的增长在增长,而T1这个时间点是没变的,造成的现象就是
随着时间的增长,second_behind_master也是有规律的增长</div>2019-01-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/f8/cb/506edc3c.jpg" width="30px"><span>可可</span> 👍（100） 💬（16）<div>老师，我先来讲个笑话
昨天去面试另一家公司，问mysql的问题，问罢之后。
面试官:我看你对mysql了解的还蛮深得，是不是也看了极客时间的。。。～
我: 没有没有(连忙否认，有一种提前看了考试答案的罪恶感😂😂😂)


所以最后我有个问题，如果后面还有这样的问题，老师您觉得我应该怎么回答？</div>2019-03-27</li><br/><li><img src="" width="30px"><span>aubrey</span> 👍（50） 💬（5）<div>semi-sync在网络故障超时的情况下会退化成async，这个时候如果刚好主库掉电了，有些binlog还没有传给从库，从库无法判断数据跟主库是否一致，如果强行切换可能会导致丢数据，在金融业务场景下只能＂人工智能＂来做切换，服务中断时间长。AliSQL采用双通道复制更容易判断主备数据是否一致，如果一致可以自动切换，如果不一致才需要人工恢复数据。</div>2019-02-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/4e/3a/86196508.jpg" width="30px"><span>linqw</span> 👍（38） 💬（7）<div>总结下学习完高可用，老师有空帮忙看下
1、主备延迟，就是在同一个事务在备库执行完成的时间和主库执行完成的时间之间的差值，包括主库事务执行完成时间和将binlog发送给备库，备库事务的执行完成时间的差值。每个事务的seconds_behind_master延迟时间，每个事务的 binlog 里面都有一个时间字段，用于记录主库上的写入时间，备库取出当前正在执行的事务的时间字段的值，计算它与当前系统时的差值。
2、主备延迟的来源①首先，有些部署条件下，备库所在机器的性能要比主库所在的机器性能差，原因多个备库部署在同一台机器上，大量的查询会导致io资源的竞争，解决办法是配置”双1“，redo log和binlog都只write fs page cache②备库的压力大，产生的原因大量的查询操作在备库操作，耗费了大量的cpu，导致同步延迟，解决办法，使用一主多从，多个从减少备的查询压力③大事务，因为如果一个大的事务的dml操作导致执行时间过长，将其事务binlog发送给备库，备库也需执行那么长时间，导致主备延迟，解决办法尽量减少大事务，比如delete操作，使用limit分批删除，可以防止大事务也可以减少锁的范围。
④大表的ddl，会导致主库将其ddl binlog发送给备库，备库解析中转日志，同步，后续的dml binlog发送过来，需等待ddl的mdl写锁释放，导致主备延迟。
3、可靠性优先策略，①判断备库 B 现在的 seconds_behind_master如果小于某个值（比如 5 秒）继续下一步，否则持续重试这一步，②把主库 A 改成只读状态，即把 readonly 设置为 true，③判断备库 B 的 seconds_behind_master的值，直到这个值变成 0 为止； 把备库 B 改成可读写也就是把 readonly 设置为 false； 把业务请求切换到备库，个人理解如果发送过来的binlog在中转日志中有多个事务，业务不可用的时间，就是多个事务被运用的总时间。如果非正常情况下，主库掉电，会导致出现的问题，如果备库和主库的延迟时间短，在中转日志运用完成，业务才能正常使用，如果在中转日志还未运用完成，切换为备库会导致之前完成的事务，”数据丢失“，但是在一些业务场景下不可接受。
4、可用性策略，出现的问题：在双m，且binlog_format=mixed，会导致主备数据不一致，使用使用 row 格式的 binlog 时，数据不一致的问题更容易发现，因为binlog row会记录字段的所有值。
5、老师有个问题不太理解，就是主备延迟时，会导致备库在没有运用中转日志时，业务查询时导致”数据丢失“，那如何解决了？</div>2019-02-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/8a/a8/cf86fe53.jpg" width="30px"><span>cyberty</span> 👍（27） 💬（9）<div>请问老师，如果备库连接主库之后，主库的系统时间修改了，备库同步的时候是否会自动修正？</div>2019-01-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/f9/a4/f0b92135.jpg" width="30px"><span>万勇</span> 👍（25） 💬（3）<div>主备同步延迟，工作中常遇到几种情况：
1.主库做大量的dml操作，引起延迟
2.主库有个大事务在处理，引起延迟
3.对myisam存储引擎的表做dml操作，从库会有延迟。
4.利用pt工具对主库的大表做字段新增、修改和添加索引等操作，从库会有延迟。
</div>2019-01-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/df/ea/7ad267ea.jpg" width="30px"><span>John</span> 👍（22） 💬（1）<div>循环复制根本原因是binlog中引入了非当前主机的server id，可以通过ignore server ids过滤，但是一般情况如果出现循环复制，数据的可靠性就值得怀疑了，不管是过滤还是重新找点都很难保证循环的部分完整执行过，最后都要验证数据的状态，属于特别严重故障😂</div>2019-01-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/df/94/84296110.jpg" width="30px"><span>Max</span> 👍（22） 💬（3）<div>老师，图中产生的这个现象的原因应该是，执行一个大事务，导致second_behind_master一直在增加。
其实second_behind_master的计算机方法应该当前系统的时间戳减去sql_thread线程正在执行的binglog event上的时间戳，得到的差值就是seconds_behind_master.
但根据seconds_behind_master来判断主从同步有一个严重的问题，如果主库和从库网络如果不通，从库不会马上知道和主库连接不能，从库有一个
salve_net_timeout=多少秒，从库会通过这个参数定时的检测是否与主库保持通讯，所以这个参数应该设为小一点。slave_net_timeout=10(单位是秒).
或者用pt-hearbeat来检测主从延迟。

老师，请教一个题外问题，mysql的主从复制，到底是主库把binlog事件推送给从库，还是从库请求主库把binlog事件推送给从库。
除了start slave;这个动作表示从库请求把某一个binlog事件推送给它。因为一般情况下主库的binlog推送给从库是异步模式，不需要从库告诉主库我接收这个事件.
如果主从之间网络不通，主库会多次发送已经执行过的binlog事件吗？网络不好可能多次提交 实在抱歉</div>2019-01-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/23/98/bd96932f.jpg" width="30px"><span>xm</span> 👍（19） 💬（1）<div>一般主从延时多少算是合理的？是秒级别吗？</div>2019-01-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/5c/c5/1231d633.jpg" width="30px"><span>梁中华</span> 👍（19） 💬（6）<div>我有一个比较极端一点的HA问题，假设主库的binlog刚写成功还未来得及把binlog同步到从库，主库就掉电了，这时候从库的数据会不完整吗？
第二个问题，原主库重启加入集群后，那条没有传出去的binlog会如何处理？</div>2019-01-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/99/f4/e0484cac.jpg" width="30px"><span>崔伟协</span> 👍（12） 💬（3）<div>发生主从切换的时候，主有的最新数据没同步到从，会出现这种情况吗，出现了会怎么样</div>2019-01-11</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/iatN3FI9buSibNumGuaAZYHTI2hHlSrJIhqKZADYKg6bxqzLbNsOD7rDYFialIqSick0qntB3dXQYXkPG3d2XSYSeA/132" width="30px"><span>Geek_mvw5du</span> 👍（12） 💬（4）<div>老师，生产环境有一张表需要清理，该表大小140G。要保留最近一个月的数据，又不能按时间直接用detele删（全表扫描），本来想通过清空分区表删，但是分区表又是哈希的。。有没好的办法呢？</div>2019-01-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/20/3a/90db6a24.jpg" width="30px"><span>Long</span> 👍（11） 💬（1）<div>老师，您好：

一直追这个课程，解决了我自己的很多知识盲点，或者更加深入的了解一些知识点，已经在试读留言下推荐了这个课程。

但是有的时候在分析问题的时候，看很多日志，比如error log中的死锁日志，报错日志中每个字段是什么意思，以及show innodb engine status中每个日志段的意思，比如在将redo log的时候innodb status就会记录，这样就可以结合课程中的log write，page cahce和fsync逻辑到数据库中实际感受到学到的原因，在应用中怎么一一对应。
比如，show innodb engine status中：
 --------
 FILE I&#47;O
 --------
***
***
 Pending normal aio reads: 0 [0, 0, 0, 0, 0, 0, 0, 0] , aio writes: 0 [0, 0, 0, 0, 0, 0, 0, 0] ,
  ibuf aio reads: 0, log i&#47;o&#39;s: 0, sync i&#47;o&#39;s: 0
 Pending flushes (fsync) log: 1; buffer pool: 0
 14321192292 OS file reads, 120057595 OS file writes, 60413577 OS fsyncs
 10 pending preads, 1 pending pwrites
 4648.01 reads&#47;s, 16383 avg bytes&#47;read, 48.09 writes&#47;s, 34.98 fsyncs&#47;s


 ---
 LOG
 ---
 Log sequence number 3893849611607
 Log flushed up to   3893849603096
 Pages flushed up to 3893705803837
 Last checkpoint at  3893705803837
 1 pending log writes, 0 pending chkp writes
 28053287 log i&#47;o&#39;s done, 10.15 log i&#47;o&#39;s&#47;second

之前看过网上的一些分析，由于和原理脱离，所以理解的都不深。
非常期待老师能结合error log一些常见问题分析比如dead lock，常见crash啊之类的，
以及show innodb engine status中的重点内容！

多谢

</div>2019-01-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/e3/bc/064401c7.jpg" width="30px"><span>EAGLE</span> 👍（11） 💬（1）<div>文中提到“如果一个主库上的语句执行 10 分钟，那这个事务很可能就会导致从库延迟 10 分钟”。这个延迟是针对当前delete事务，还是所有的事务都延迟。

</div>2019-01-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/8a/3e/30c05bce.jpg" width="30px"><span>aliang</span> 👍（9） 💬（3）<div>老师，我有一个问题：（1）seconds_behind_master的计算方法是通过从库的系统时间戳减去sql_thead线程正在执行的binlog_event上的时间戳的差值。当从库系统时间不准时也不会影响seconds的值，因为从库连接到主库时会通过select unix_timestamp（）查询主库的系统时间，若发现和从库不一致会在计算seconds这个值时作调整（2）我的疑惑是在主从网络正常时，select unix_timestamp执行的频率和触发条件是怎样的（换句话说（1）中描述的从库连接到主库这个行为是一直存在的还是有其他触发条件？）。如果这个频率不高，那在两次select unix_timestamp期间从库系统时间发生变化，seconds的值岂不是不准了？</div>2019-02-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/e7/dd/e68f9cf5.jpg" width="30px"><span>易翔</span> 👍（9） 💬（2）<div>常见的都讲了，补充几点我遇到过的。

1,备库做逻辑备份时，有产生MDL锁。然后复制线程刚好被堵塞。。kill掉备份线程，一切都畅快了。。我遇到过，但是感觉那备份期间产生的非共享锁不是短时间就释放的吗？为什么堵的时间那么长，感觉像是遇到死锁。大神讲讲其中原因。

2，数据库用了共享存储，其它业务的不期待(我们当时是归档程序)占用会导致同样连接该存储上的数据库遇到写入瓶颈，写入不仅仅是应用中继日志产生的数据。还有写中继日志。写中继日志慢，应用日志线程工作却有条不紊。这时候也会产生备库延迟。由于体现没有中继日志滞留，没有想到io问题，当时第一反应是网络带宽被打满了，确认了，没有问题过后。然后找到存储，看存储IOPS。最后定位到归档程序正在批量写入数据。</div>2019-01-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/87/60/fe8a31ea.jpg" width="30px"><span>via</span> 👍（7） 💬（4）<div>通过 binlog 输出到外部系统，比如 Hadoop 这类...

文中这个具体是可采用什么工具呢？
 </div>2019-01-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/7a/ed/f52b84b9.jpg" width="30px"><span>Sr7vy</span> 👍（6） 💬（2）<div>问题1：T3的解释是：备库执行完这个事物。则：Seconds_Behind_Master=T3-T1。如T1=30min，主执行完成，备没有执行。猜测1：那么Seconds_Behind_Master=30min吗？猜测2：备执需要先把这个30min的事务执行完后，Seconds_Behind_Master=30min？
问题2：很多时候是否能把Seconds_Behind_Master当作真正的延迟时间（面试常被问）？如果能，pt-heartbeat存在还有啥意义啊？</div>2019-01-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/16/97/9e342700.jpg" width="30px"><span> JJ</span> 👍（6） 💬（2）<div>请问老师，主库断电了，怎么把binlog传给从库同步数据，怎么使的SBM为0主从切换呢？</div>2019-01-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/4f/78/c3d8ecb0.jpg" width="30px"><span>undifined</span> 👍（5） 💬（1）<div>问题答案：
1. 备库在执行复杂查询，导致资源被占用
2. 备库正在执行一个大事务
3. DML 语句执行

老师我的理解对吗</div>2019-01-09</li><br/><li><img src="" width="30px"><span>700</span> 👍（4） 💬（1）<div>老师请教下，MySQL 主从跨 IDC 的痛点是什么？同城 IDC 和异地 IDC 的痛点一样吗？怎么来解决这些痛点？</div>2019-01-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/2b/d3/7c42e06c.jpg" width="30px"><span>康磊</span> 👍（4） 💬（2）<div>老师你好，现在一般采用读写分离，读的是从库，那么主从如果出现延迟的话，读库就读的不是最新数据，对这种问题有什么好建议吗？</div>2019-01-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/c4/74/27cf551a.jpg" width="30px"><span>WilliamX</span> 👍（4） 💬（1）<div>大事务导致主从延时的问题，我修改下。
主库上即使有大事务，但只要影响行数不多，传送到从库时间为t1，完成时间为T3，那这个时间gap和是否大事务没关系吧？</div>2019-01-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/07/1e/bdbe93f4.jpg" width="30px"><span>尘封</span> 👍（4） 💬（1）<div>表没有主键，sysbench压力测试也会导致主从延时</div>2019-01-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/69/c6/513df085.jpg" width="30px"><span>强哥</span> 👍（3） 💬（3）<div>今天跟公司的dba咨询了下，目前公司用的主备切换策略都是可用性优先，说是可靠性优先的话，可能会引起雪崩，主要还是业务的并发高，这种场景您是怎么看呢？麻烦给下思路谢谢。</div>2019-01-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/5c/c5/1231d633.jpg" width="30px"><span>梁中华</span> 👍（3） 💬（1）<div>关于semi–sync，大神什么时候开一讲，感觉比较鸡肋，和网络绑死了，可用性肯能会降低。不过阿里的Oceanbase也是用类似强一致同步的方式，大神怎么看？</div>2019-01-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/03/f7/3a493bec.jpg" width="30px"><span>老杨同志</span> 👍（3） 💬（1）<div>思考题情况我感觉有两种情况
1）大事务。如老师文章里说的时间段t1、t2、t3, t1 10分钟，t2很快完成，t3也要在从库上执行10分钟。那么在t3时间段内，应该就是延时不断增加吧。

2）我的猜测，主库多线程执行事务。从库单线程执行relayLog，相当于串行化事务，在主库比较繁忙的情况下，是不是从库也会出现延时逐步增加的情况</div>2019-01-09</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTJAibnPX9jW8kqLcIfibjic8GbkQkEUYyFKJkc39hZhibVlNrqwTjdLozkqibI2IwACd5YzofYickNxFnZg/132" width="30px"><span>Sinyo</span> 👍（3） 💬（2）<div>老师，在 binlog row模式下，insert 到表中一条记录，这条记录中某个字段不填，该字段在表中有设置默认值，利用canal解析binlog出来，这个不填的字段会不存在；难道 binlog 只记录有插入的字段数据，表字段的默认数据就不会记录么？mysql版本5.7.22 canal版本1.0.3</div>2019-01-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/8a/3e/30c05bce.jpg" width="30px"><span>aliang</span> 👍（2） 💬（1）<div>老师，我之前在看贺春旸写的《MySQL管理之道：性能调优、高可用与监控》 第2版时，书上提到：当（1）从库的系统时间不准（没有提到老师讲的从库访问主库时会执行select unix_timestamp（）获取主库系统时间） （2）主从之间网络中断（此时主库binlog无法推送到从库，导致从库没有正在执行的binlog；slave_net_timeout设置太大导致slave很久才尝试重连主库）这两种情况时，靠seconds_behind_master的值来判断主从延迟是不准的。这与老师讲的有点出入，是不是书上描述错了呢？</div>2019-02-16</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/b7/00/12149f4e.jpg" width="30px"><span>郭刚</span> 👍（2） 💬（1）<div>如果不使用自增序列作为主键，用UUID，是不是就不会出现不一致的问题？</div>2019-01-09</li><br/>
</ul>