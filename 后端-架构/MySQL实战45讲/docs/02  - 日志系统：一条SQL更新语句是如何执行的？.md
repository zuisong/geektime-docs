前面我们系统了解了一个查询语句的执行流程，并介绍了执行过程中涉及的处理模块。相信你还记得，一条查询语句的执行过程一般是经过连接器、分析器、优化器、执行器等功能模块，最后到达存储引擎。

那么，一条更新语句的执行流程又是怎样的呢？

之前你可能经常听DBA同事说，MySQL可以恢复到半个月内任意一秒的状态，惊叹的同时，你是不是心中也会不免会好奇，这是怎样做到的呢？

我们还是从一个表的一条更新语句说起，下面是这个表的创建语句，这个表有一个主键ID和一个整型字段c：

```
mysql> create table T(ID int primary key, c int);
```

如果要将ID=2这一行的值加1，SQL语句就会这么写：

```
mysql> update T set c=c+1 where ID=2;
```

前面我有跟你介绍过SQL语句基本的执行链路，这里我再把那张图拿过来，你也可以先简单看看这个图回顾下。首先，可以确定的说，查询语句的那一套流程，更新语句也是同样会走一遍。

![](https://static001.geekbang.org/resource/image/0d/d9/0d2070e8f84c4801adbfa03bda1f98d9.png?wh=1920%2A1440)

MySQL的逻辑架构图

你执行语句前要先连接数据库，这是连接器的工作。

前面我们说过，在一个表上有更新的时候，跟这个表有关的查询缓存会失效，所以这条语句就会把表T上所有缓存结果都清空。这也就是我们一般不建议使用查询缓存的原因。

接下来，分析器会通过词法和语法解析知道这是一条更新语句。优化器决定要使用ID这个索引。然后，执行器负责具体执行，找到这一行，然后更新。
<div><strong>精选留言（30）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/12/43/38/72feb2e0.jpg" width="30px"><span>哇！怎么这么大个</span> 👍（176） 💬（17）<div>老师您好，我之前是做运维的，通过binlog恢复误操作的数据，但是实际上，我们会后知后觉，误删除一段时间了，才发现误删除，此时，我把之前误删除的binlog导入，再把误删除之后binlog导入，会出现问题，比如主键冲突，而且binlog导数据，不同模式下时间也有不同，但是一般都是row模式，时间还是很久，有没什么方式，时间短且数据一致性强的方式</div>2018-12-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/85/43/3dc8222d.jpg" width="30px"><span>小张</span> 👍（178） 💬（41）<div>老师您好，有一个问题，如果在非常极端的情况下，redo log被写满，而redo log涉及的事务均未提交，此时又有新的事务进来时，就要擦除redo log，这就意味着被修改的的脏页此时要被迫被flush到磁盘了，因为用来保证事务持久性的redo log就要消失了。但如若真的执行了这样的操作，数据就在被commit之前被持久化到磁盘中了。当真的遇到这样的恶劣情况时，mysql会如何处理呢，会直接报错吗？还是有什么应对的方法和策略呢？</div>2018-11-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/f5/de/c33e531e.jpg" width="30px"><span>Jason</span> 👍（809） 💬（36）<div>首先谈一下，学习后的收获
redo是物理的，binlog是逻辑的；现在由于redo是属于InnoDB引擎，所以必须要有binlog，因为你可以使用别的引擎
保证数据库的一致性，必须要保证2份日志一致，使用的2阶段式提交；其实感觉像事务，不是成功就是失败，不能让中间环节出现，也就是一个成功，一个失败
如果有一天mysql只有InnoDB引擎了，有redo来实现复制，那么感觉oracle的DG就诞生了，物理的速度也将远超逻辑的，毕竟只记录了改动向量
binlog几大模式，一般采用row，因为遇到时间，从库可能会出现不一致的情况，但是row更新前后都有，会导致日志变大
最后2个参数，保证事务成功，日志必须落盘，这样，数据库crash后，就不会丢失某个事务的数据了
其次说一下，对问题的理解
备份时间周期的长短，感觉有2个方便
首先，是恢复数据丢失的时间，既然需要恢复，肯定是数据丢失了。如果一天一备份的话，只要找到这天的全备，加入这天某段时间的binlog来恢复，如果一周一备份，假设是周一，而你要恢复的数据是周日某个时间点，那就，需要全备+周一到周日某个时间点的全部binlog用来恢复，时间相比前者需要增加很多；看业务能忍受的程度
其次，是数据库丢失，如果一周一备份的话，需要确保整个一周的binlog都完好无损，否则将无法恢复；而一天一备，只要保证这天的binlog都完好无损；当然这个可以通过校验，或者冗余等技术来实现，相比之下，上面那点更重要

不对的地方，望大神指点</div>2018-11-16</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/97/59/6f9c036e.jpg" width="30px"><span>Godruoyi</span> 👍（275） 💬（58）<div>Bin log 用于记录了完整的逻辑记录，所有的逻辑记录在 bin log 里都能找到，所以在备份恢复时，是以 bin log 为基础，通过其记录的完整逻辑操作，备份出一个和原库完整的数据。

在两阶段提交时，若 redo log 写入成功，bin log 写入失败，则后续通过 bin log 恢复时，恢复的数据将会缺失一部分。(如 redo log 执行了 update t set status = 1，此时原库的数据 status 已更新为 1，而 bin log 写入失败，没有记录这一操作，后续备份恢复时，其 status = 0，导致数据不一致）。

若先写入 bin log，当 bin log 写入成功，而 redo log 写入失败时，原库中的 status 仍然是 0 ，但是当通过 bin log 恢复时，其记录的操作是 set status = 1，也会导致数据不一致。

其核心就是， redo log 记录的，即使异常重启，都会刷新到磁盘，而 bin log 记录的， 则主要用于备份。

我可以这样理解吗？还有就是如何保证 redo log 和 bin log 操作的一致性啊？</div>2018-11-16</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/aa/21/6c3ba9af.jpg" width="30px"><span>lfn</span> 👍（537） 💬（76）<div>老师,今天MYSQL第二讲中提到binlog和redo log, 我感觉binlog很多余，按理是不是只要redo log就够了?[费解] 
您讲的时候说redo log是InnoDB的要求，因为以plugin的形式加入到MySQL中，此时binlog作为Server层的日志已然存在，所以便有了两者共存的现状。但我觉得这并不能解释我们在只用InonoDB引擎的时候还保留Binlog这种设计的原因.</div>2018-11-16</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/bb/10/f01eafe4.jpg" width="30px"><span>ricktian</span> 👍（84） 💬（29）<div>redo log的机制看起来和ring buffer一样的；
另外有个和高枕、思雨一样的疑问，如果在重启后，需要通过检查binlog来确认redo log中处于prepare的事务是否需要commit，那是否不需要二阶段提交，直接以binlog的为准，如果binlog中不存在的，就认为是需要回滚的。这个地方，是不是我漏了什么，拉不通。。。 麻烦老师解下疑，多谢～ </div>2018-11-16</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/f7/69/d8dba3de.jpg" width="30px"><span>DanielAnton</span> 👍（44） 💬（17）<div>有个问题请教老师，既然write pos和checkout都是往后推移并循环的，而且当write pos赶上checkout的时候要停下来，将checkout往后推进，那么是不是意味着write pos的位置始终在checkout后面，最多在一起，而这和老师画的图有些出入，不知道我的理解是不是有些错误，请老师指教。</div>2018-11-16</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/74/8b/840afbd8.jpg" width="30px"><span>super blue cat</span> 👍（1231） 💬（87）<div>我可以认为redo log 记录的是这个行在这个页更新之后的状态，binlog 记录的是sql吗？</div>2018-11-16</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/fe/68/e0bebd9a.jpg" width="30px"><span>高枕</span> 👍（1085） 💬（95）<div>我再来说下自己的理解 。
1 prepare阶段 2 写binlog 3 commit
当在2之前崩溃时
重启恢复：后发现没有commit，回滚。备份恢复：没有binlog 。
一致
当在3之前崩溃
重启恢复：虽没有commit，但满足prepare和binlog完整，所以重启后会自动commit。备份：有binlog. 一致</div>2018-11-16</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/f8/70/f3a33a14.jpg" width="30px"><span>某、人</span> 👍（678） 💬（102）<div>1.首先客户端通过tcp&#47;ip发送一条sql语句到server层的SQL interface
2.SQL interface接到该请求后，先对该条语句进行解析，验证权限是否匹配
3.验证通过以后，分析器会对该语句分析,是否语法有错误等
4.接下来是优化器器生成相应的执行计划，选择最优的执行计划
5.之后会是执行器根据执行计划执行这条语句。在这一步会去open table,如果该table上有MDL，则等待。
如果没有，则加在该表上加短暂的MDL(S)
(如果opend_table太大,表明open_table_cache太小。需要不停的去打开frm文件)
6.进入到引擎层，首先会去innodb_buffer_pool里的data dictionary(元数据信息)得到表信息
7.通过元数据信息,去lock info里查出是否会有相关的锁信息，并把这条update语句需要的
锁信息写入到lock info里(锁这里还有待补充)
8.然后涉及到的老数据通过快照的方式存储到innodb_buffer_pool里的undo page里,并且记录undo log修改的redo
(如果data page里有就直接载入到undo page里，如果没有，则需要去磁盘里取出相应page的数据，载入到undo page里)
9.在innodb_buffer_pool的data page做update操作。并把操作的物理数据页修改记录到redo log buffer里
由于update这个事务会涉及到多个页面的修改，所以redo log buffer里会记录多条页面的修改信息。
因为group commit的原因，这次事务所产生的redo log buffer可能会跟随其它事务一同flush并且sync到磁盘上
10.同时修改的信息，会按照event的格式,记录到binlog_cache中。(这里注意binlog_cache_size是transaction级别的,不是session级别的参数,
一旦commit之后，dump线程会从binlog_cache里把event主动发送给slave的I&#47;O线程)
11.之后把这条sql,需要在二级索引上做的修改，写入到change buffer page，等到下次有其他sql需要读取该二级索引时，再去与二级索引做merge
(随机I&#47;O变为顺序I&#47;O,但是由于现在的磁盘都是SSD,所以对于寻址来说,随机I&#47;O和顺序I&#47;O差距不大)
12.此时update语句已经完成，需要commit或者rollback。这里讨论commit的情况，并且双1
13.commit操作，由于存储引擎层与server层之间采用的是内部XA(保证两个事务的一致性,这里主要保证redo log和binlog的原子性),
所以提交分为prepare阶段与commit阶段
14.prepare阶段,将事务的xid写入，将binlog_cache里的进行flush以及sync操作(大事务的话这步非常耗时)
15.commit阶段，由于之前该事务产生的redo log已经sync到磁盘了。所以这步只是在redo log里标记commit
16.当binlog和redo log都已经落盘以后，如果触发了刷新脏页的操作，先把该脏页复制到doublewrite buffer里，把doublewrite buffer里的刷新到共享表空间，然后才是通过page cleaner线程把脏页写入到磁盘中
老师，你看我的步骤中有什么问题嘛？我感觉第6步那里有点问题,因为第5步已经去open table了，第6步还有没有必要去buffer里查找元数据呢?这元数据是表示的系统的元数据嘛,还是所有表的？谢谢老师指正</div>2018-11-16</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/7a/e0/3d5b28ef.jpg" width="30px"><span>清歌</span> 👍（176） 💬（10）<div>binlog为什么说是逻辑日志呢？它里面有内容也会存储成物理文件，怎么说是逻辑而不是物理</div>2018-11-16</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/d4/e0/513d185e.jpg" width="30px"><span>文@雨路</span> 👍（132） 💬（27）<div>老师，我想问下如果提交事务的时候正好重启那么redo log和binlog会怎么处理？此时redo log处于prepare阶段，如果不接受这条log，但是binlog已经接受，还是说binlog会去检查redo log的状态，状态为prepare的不会恢复？</div>2018-11-16</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/e2/9d/fbbd4611.jpg" width="30px"><span>cyberbit</span> 👍（95） 💬（7）<div>我理解备份就是救命药加后悔药，灾难发生的时候备份能救命，出现错误的时候备份能后悔。事情都有两面性，没有谁比谁好，只有谁比谁合适，完全看业务情况和需求而定。一天一备恢复时间更短，binlog更少，救命时候更快，但是后悔时间更短，而一周一备正好相反。我自己的备份策略是设置一个16小时延迟复制的从库，充当后悔药，恢复时间也较快。再两天一个全备库和binlog，作为救命药,最后时刻用。这样就比较兼顾了。</div>2018-11-16</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/07/8c/0d886dcc.jpg" width="30px"><span>蚂蚁内推+v</span> 👍（89） 💬（5）<div>老师，我这想请教两个问题：
1.写redo日志也是写io（我理解也是外部存储）。同样耗费性能。怎么能做到优化呢
2.数据库只有redo commit 之后才会真正提交到数据库吗</div>2018-11-16</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/fb/21/a89aca0a.jpg" width="30px"><span>未来小娃</span> 👍（84） 💬（22）<div>先说下阅读的收获：
1、更新的流程先写redo日志，写完后更新内存，到这里操作就直接返回了。后续的流程是生成此操作的binlog，然后写到磁盘
2、redo日志是存储引擎实现的，记录的在某个数据页做了什么修改，固定大小，默认为4GB，可以循环写，解决了每次更新操作写磁盘、查找记录、然后更新整个过程效率低下的问题，redo日志将磁盘的随机写变成了顺序写，这个机制是WAL，先写日志再刷磁盘。一句话，redo日志保证了事务ACID的特性
3、binglog日志Server层实现的，记录的是语句的原始逻辑，比如给ID=1的行的状态设置成1，追加写，上个文件写完回切换成下一个文件，类似滚动日志
4、两阶段提交，是为了解决redo log和binlog不一致问题的，这里的不一致是指redo log写成功binlog写失败了，由于恢复是根据binlog恢复的，这样恢复的时候就会少一条更新操作，导致和线上库的数据不一致。具体而言，两阶段是指prepare阶段和commit阶段，写完redo log进入prepare阶段，写完binlog进入commit阶段。
然后说下由redo log联想到之前遇到的一个问题：一个普通的select查询超过30ms，经过和DBA的联合排查，确认是由于MySQL“刷脏”导致的。
所谓刷脏就是由于内存页和磁盘数据不一致导致了该内存页是“脏页”，将内存页数据刷到磁盘的操作称为“刷脏”。刷脏是为了避免产生“脏页”，主要是因为MySQL更新先写redo log再定期批量刷到磁盘的，这就导致内存页的数据和磁盘数据不一致，为了搞清楚为什么“刷脏”会导致慢查，我们先分析下redo log再哪些场景会刷到磁盘。
场景1：redo log写满了，此时MySQL会停止所有更新操作，把脏页刷到磁盘
场景2：系统内存不足，需要将脏页淘汰，此时会把脏页刷到磁盘
场景3：系统空闲时，MySQL定期将脏页刷到磁盘

可以想到，在场景1和2都会导致慢查的产生，根据文章提到的，redo log是可以循环写的，那么即使写满了应该也不会停止所有更新操作吧，其实是会的，文中有句话“粉板写满了，掌柜只能停下手中的活，把粉板的一部分赊账记录更新到账本中，把这些记录从粉板删除，为粉板腾出新的空间”，这就意味着写满后是会阻塞一段时间的。

那么问题来了，innodb存储引擎的刷脏策略是怎么样的呢？通常而言会有两种策略：全量（sharp checkpoint）和部分（fuzzy checkpoint）。全量刷脏发生在关闭数据库时，部分刷脏发生在运行时。部分刷脏又分为定期刷脏、最近最少使用刷脏、异步&#47;同步刷脏、脏页过多刷脏。暂时先写到这，后面打算写文详细介绍。</div>2019-03-06</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/dc/b7/e59c22f0.jpg" width="30px"><span>黄金的太阳</span> 👍（75） 💬（8）<div>请教老师，redo log是为了快速响应SQL充当了粉板，这里有两个疑问
1. redo log本身也是文件，记录文件的过程其实也是写磁盘，那和文中提到的离线写磁盘操作有何区别？
2.响应一次SQL我理解是要同时操作两个日志文件？也就是写磁盘两次？</div>2018-11-16</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/df/e7/4ce5ed27.jpg" width="30px"><span>lunung</span> 👍（68） 💬（4）<div>昨天上午 恢复别人误操作配置表数据，幸好有xtarbackup凌晨的全量备份，只提取了改表的ibd文件，然后在本地 做了 一个一样的空表，释放该表空间，加载 提取后的ibd文件，提取昨天零晨到九点的binlog文件 筛选改表这个时段的操作记录 增量更新到本地导出csv 导入线上  。binlog太tm重要了</div>2018-11-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/f6/b0/837f5d36.jpg" width="30px"><span>Mackie .Weng</span> 👍（54） 💬（5）<div>老师，非常感谢你的优质文章，你的每篇文章，我都要研究一段时间，而且一直做笔记，而且真的使我对mysql一个全新的认识，因为之前总感觉一直止步于数据恢复等业务操作都无法前行了。
恕我冒昧我突然想到前不久刚遇到的一个mysql的问题，我总感觉和我们学习的有很大关系，不知道是不是通过binlog来修复的。
情形是这样的，我们因为磁盘IO异常导致数据库异常重启了，并发现某个表数据损坏了（无数据备份）且mysql无法开启，一开始的做法innodb_force_recovery设置到1-6直到数据库可以启动，然后进行mysqldump备份，然而并不能备份，报错是mysqldump: Error 2013: Lost connection to MySQL server during query when dumping table `XX表` at row: 31961089。于是就跳过这个表进行备份，并修复了其他数据库，但是这个表的数据丢失最终请了外援修复好了，但是具体没告诉我们，不知道和我们这个有没联系？有没提示让我学学习下这方面？是可以用ibd文件修复吗？</div>2018-11-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/e2/cb/6bc95e09.jpg" width="30px"><span>喔～</span> 👍（51） 💬（9）<div>redo 是引擎提供的，binlog 是server 自带的，文中提到前者用在crash的恢复，后者用于库的恢复
两者是否在某种程度上是重复的？如果在都是追加写的情况下，是否两种日志都能用于 crash 与 库 的恢复呢？</div>2018-11-16</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/70/51/f1825adb.jpg" width="30px"><span>Lugyedo</span> 👍（46） 💬（2）<div>redo log和bin log怎么对应</div>2018-11-16</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/f8/ba/d28174a9.jpg" width="30px"><span>Geek_zbvt62</span> 👍（33） 💬（12）<div>看到了文@雨路的留言，和我的疑问一模一样。另外有个没提到，如果认可这个事务可以从crash恢复，起码要求服务器告知客户端事务成功了吧，那您说redo log prepare + bin log ok，就可以恢复了，说明bin log写入成功就算事务成功了？那最后一步确实没什么用呀。</div>2018-11-16</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/16/a8/75476086.jpg" width="30px"><span>act</span> 👍（30） 💬（15）<div>执行一条Update 语句后，马上又执行一条 select * from table limit 10。

如果刚刚update的记录，还没持久化到磁盘中，而偏偏这个时候的查询条件，又包含了刚刚update的记录。

那么这个时候，是从日志中获取刚刚update的最新结果，还是说，先把日志中的记录先写磁盘，再返回最新结果？</div>2018-12-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/13/7d/1454db9c.jpg" width="30px"><span>KeepGoing</span> 👍（27） 💬（12）<div>我有点蒙，
1.如果把innodb_flush_log_at_trx_commit设置成1每次都写入到磁盘，那不就等于是掌柜的每次记账都记到账本上嘛，那还要小黑板干嘛呢？感觉我从文中没理解到各位大神已知的信息一样。
2.binlog是逻辑，redolog是物理，两者都能记录历史，如果发生异常情况binlog就可以恢复数据，为什么说只有redolog才能算是crash-safe了呢。
可能是我基础不够就看大神的文章，有些懵，还烦老师给解一下疑惑～谢谢。</div>2018-11-30</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/5b/72/4f8a4297.jpg" width="30px"><span>阿May的海绵宝宝</span> 👍（26） 💬（1）<div>1.单独依靠redologo无法做到指定某一点的恢复，是不是因为redologo是循环写的，如果要恢复的那一时刻被擦掉了，就无法知道这点的数据变动轨迹，而binlog是追加的方式，在文件完整的前提下，数据的变动轨迹都可以知晓？
2. 最后三步是 ①引擎写redolog，并处于prepare状态   ②执行器写binlog，成功后，发送commit
   ③引擎刚写入的redolog改变为commit状态
  如果crash发生后  redolog =prepare   binlog没有对应写入记录，则回滚
  如果crash发生后  redolog =prepare  binlog有对应写入记录，则提交
感觉有点像  1 &amp;&amp; 1= 1   1&amp;&amp;0=0   0&amp;&amp;1=0
3.binlog模式  ①记录sql语句    ②记录更新前后的行     一般是用哪种模式？</div>2018-11-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/4e/3a/86196508.jpg" width="30px"><span>linqw</span> 👍（24） 💬（3）<div>学习后的收获总结：
1、首先数据库更新操作都是基于内存页，更新的时候不会直接更新磁盘，如果内存有存在就直接更新内存，如果内存没有存在就从磁盘读取到内存，在更新内存，并且写redo log，目的是为了更新效率更快，等空闲时间在将其redo log所做的改变更新到磁盘中，innodb_flush_log_at_trx_commit设置为1时，也可以防止服务出现异常重启，数据不会丢失
2、redo log两阶段提交，是为了保证redo log和binlog的一致性，如果redo log写入成功处于prepare阶段，写binlog失败，事务回滚，redo log会回滚到操作之前的状态
3、redo log也是写磁盘，写redo log是顺序写，update直接更新磁盘，需要找到数据，再对此数据进行更新，如果没有使用索引，数据量大会导致更新效率慢，不对的地方，望老师指点哦</div>2018-11-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/7a/0a/0ce5c232.jpg" width="30px"><span>吕</span> 👍（21） 💬（4）<div>你好，关于提到的&#39;数据页&#39;这个词我没有太理解，是一种存储方式么？</div>2018-11-16</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/6c/03/75c65e8f.jpg" width="30px"><span>leon</span> 👍（18） 💬（4）<div>老师，有个问题一直很困惑

两阶段提交为了保证binlog和redolog的一致性，
1 prepare阶段  2 写binlog  3 commit阶段
假如在3之前崩溃，恢复时，虽没有commit，但prepare和binlog完整，所以重启后会自动commit，以此来保证有binlog一致性。

既然能这样做，那为什么不把commit阶段去掉，恢复时，只要redolog和binlog完整就认为redolog有效，否则回滚呢？ 是因为效率还是其他的原因？</div>2018-11-30</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/f8/34/2ce5e546.jpg" width="30px"><span>Elvis</span> 👍（18） 💬（4）<div>请教下redo log 和 binlog 也是需要写文件的，也会消耗IO，这个不会影响数据库的性能吗？ 从内容看redo log首先写道缓存中，如果这个时候断电了，缓存也清空了，尚未写道磁盘，这个时候不是redo log 不完整的如何保证恢复的完整性呢？麻烦老师指教下</div>2018-11-16</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/f9/03/439bdb70.jpg" width="30px"><span>魔都浪子</span> 👍（17） 💬（10）<div>在binlog写入磁盘后，commit提交前发生crash，由于commit没有成功，那返回给客户端的消息是事物失败，但是在系统恢复的时候却会重新提交事物，使之成功，这不是在欺骗客户端嘛？问题很大啊</div>2018-11-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/d2/c9/f262f947.jpg" width="30px"><span>haruki</span> 👍（17） 💬（4）<div>老师，有个疑问，怎么知道binlog是完整的？这个想不通</div>2018-11-16</li><br/>
</ul>