不知道你在实际运维过程中有没有碰到这样的情景：业务高峰期，生产环境的MySQL压力太大，没法正常响应，需要短期内、临时性地提升一些性能。

我以前做业务护航的时候，就偶尔会碰上这种场景。用户的开发负责人说，不管你用什么方案，让业务先跑起来再说。

但，如果是无损方案的话，肯定不需要等到这个时候才上场。今天我们就来聊聊这些临时方案，并着重说一说它们可能存在的风险。

# 短连接风暴

正常的短连接模式就是连接到数据库后，执行很少的SQL语句就断开，下次需要的时候再重连。如果使用的是短连接，在业务高峰期的时候，就可能出现连接数突然暴涨的情况。

我在第1篇文章[《基础架构：一条SQL查询语句是如何执行的？》](https://time.geekbang.org/column/article/68319)中说过，MySQL建立连接的过程，成本是很高的。除了正常的网络连接三次握手外，还需要做登录权限判断和获得这个连接的数据读写权限。

在数据库压力比较小的时候，这些额外的成本并不明显。

但是，短连接模型存在一个风险，就是一旦数据库处理得慢一些，连接数就会暴涨。max\_connections参数，用来控制一个MySQL实例同时存在的连接数的上限，超过这个值，系统就会拒绝接下来的连接请求，并报错提示“Too many connections”。对于被拒绝连接的请求来说，从业务角度看就是数据库不可用。
<div><strong>精选留言（30）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/13/f8/70/f3a33a14.jpg" width="30px"><span>某、人</span> 👍（72） 💬（11）<div>最近才发生了个案列:
由于一个delete大事务导致磁盘空间满了,数据库hang住,连接不上,所以无法kill掉该大事务
当时的观察到的现象是:
binlog有一个文件已经达到50多G
lsof | grep delete 该tmp文件100多G
redo log还是只有4个组,每个文件1G
undo log大概有100来G
由于数据库连不上,只有把连接切到从库,kill掉主库的进程。过了几分钟,binlog文件才缩小为原来的大小。把主库启起来,但是recovery非常慢。后面kill掉,又以innodb_force_recovery=3恢复,recovery也是半天没反应。由于这个库也不是重要的库,就把新的主库的备份文件重做了之前的主库,以从库启起来

通过最近的学习+测试分析了下,为什么binlog达到了50多G。tmp文件100多G.
由于binlog_cache不够用,把binlog写进了tmp文件中,binlog文件50多G,说明事务已经执行完成,是binlog在fsync阶段,把空间占满了。fsync并不是一个move而是相当于copy。要等binlog完全落盘以后,才会删除之前的tmp文件。redo log由于是循环写,而且在事务执行过程中,就会把redo log分为mtx落地到磁盘上。所以没有一次性暴增,还是以1G的大小持续写.
我也是后续做测试,观察在事务进行中,redo log文件一直都有变化。binlog没有变化
binlog是在事务执行完以后,才一次性fsync到磁盘
但是为什么recovery=3的情况下,还比较耗时。我估计是之前脏页较多,而redo log又全部被覆盖掉,
需要先通过binlog来恢复redo log,然后再通过redo log来恢复数据页。

请问老师有没有更好的办法来处理这种hang住的情况?
如果在操作系统层面kill掉执行的线程,就好了。
昨天提到的问题3,我也没有测试出来Sending to client这个状态.是之前别人问到的,我也挺懵</div>2019-01-03</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/20/3a/90db6a24.jpg" width="30px"><span>Long</span> 👍（87） 💬（4）<div>不是专业DBA，遇到过几次数据库问题，有的能解决，有的好像除了重启或者干等着没啥好办法。
MySQL5.6版本遇到的部分问题：

1. 几个线程处于killed状态一直kill不掉（1天），然后备份的时候MySQL backup flush all tables with read lock的时候被阻塞，后面的线程只能等待flush table, kill backup以后也没有办法kill那几个killed状态的语句（processlist显示的killed状态的语句的就是show columns, show create table这样的），后面没办法，重启了server。（看到老师后面第25讲有关于kill的解释，非常期待新知识）

2. 一个非常大（大几百万行）的表truncate，结果后面所有的线程都阻塞了，类似于下面这个MySQL bug的场景，结果就是等这个truncate结束。没有继续干预。
https:&#47;&#47;bugs.mysql.com&#47;bug.php?id=80060

3.  某个新功能上线以后，一个记录操作人员操作页面操作时间KPI的功能，由于sql性能不好，在业务上线跑了3天后数据量增多到临界值，突然影响了整个系统性能。数据库发现是大量的sql执行状态是converting heap to MyISAM，sql写法类似 select (select * from table) where id(有索引)= xxxx order by yyyy
DBA以及他们团队要求重启。但是分析了几分钟后提供了几个意见给&quot;DBA&quot;，并解释重启解决不了问题：首先这个问题重启是解决不了，因为每次这个sql查询全表，查询分配的临时表空间不足了，需要把结果集转到磁盘上，重启了sql动作没变，参数没变所以重启解决不了问题。
页面查询也没法屏蔽，页面查询也无法过滤条件，
（1）和研发确认后，表数据删除不影响功能，只影响客户的KPI报表，先备份表，然后删除，后面等功能修复了再补回去。
（2）调整max_heap_table_size，tmp_table_size，扩大几倍
（3）给这个sql的唯一的一个order by字段加个索引。
同时催促研发提供hotfix。最终选择了最简单有效的（1）问题解决，研发迅速后面也发了hotfix解决了。

4. 某个消费高峰时间段，高频查询被触发，一天几十万次执行，由于存量数据越来越多，查询性能越来越慢，主要是索引没有很好规划，导致CPU资源使用飙升，后面的sql执行越来越慢。 最后尝试了给2个字段添加单独的索引，解决了50%的问题，看到执行计划，extra里面，索引合并使用了intersect，性能还是慢，然后立马drop原先的2个单独索引，创建两个字段的联合索引，问题解决了。

5. 死锁回滚，导致的MySQL hang住了，当时刚入门，只能简单复现死锁，没有保留所有的日志，现在想查也查不了了。。。
感觉大部分都是慢sql和高频事务导致的。

（当然后面的慢sql监控分析，项目上就很重视了。。）


今天看了这期专栏，发现5.7的这个功能，query_rewrite，受教了。等我们升到5.7以后，可以实际操练下。上面的问题3，也可以用这个功能了（因为是新业务，新表，特殊sql，完全可以起到hotfix的作用）。


请老师帮忙看下上面几次故障是否有更好，更专业的解决方案。多谢</div>2019-01-02</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/40/5e/b8fada94.jpg" width="30px"><span>Ryoma</span> 👍（73） 💬（13）<div>我之前的描述有点问题，其实想问的是：为什么加了 order by c desc，第一个定位c=20 的行，会加上间隙锁 (20,25) 和 next-key lock (15,20]？

如果没有order by c desc，第一次命中c=15时，只会加上next-key lock(10.15]；
而有了order by c desc，我的理解是第一次命中c=20只需要加上next-key lock (15,20]

当然最后(20,25)还是加上了锁，老师的结论是对的，我也测试过了，但是我不知道如何解释。
唯一能想到的解释是order by c desc 并不会改变优化2这个原则：即等值查询时，会向右遍历且最后一个值不满足等值条件；同时order by c desc 带来一个类似于优化2的向左遍历原则。
进而导致最后的锁范围是(5,25)；而没有order by c desc的范围是(10,25]。
</div>2019-01-03</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/48/bd/6c7d4230.jpg" width="30px"><span>Tony Du</span> 👍（43） 💬（27）<div>对于上期问题的解答，有一点不是特别理解，
因为order by desc，在索引c上向左遍历，对于（15， 25）这段区间没有问题，
然后，扫描到c=10才停下来，理论上把（10，15]这个区间锁上就应该是完备的了呀。（5，10]这段区间是否锁上对结果应该没有影响呀，为什么会需要（5，10] 这段的next-key lock ?
</div>2019-01-02</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/20/3a/90db6a24.jpg" width="30px"><span>Long</span> 👍（27） 💬（3）<div>老师好，看到有的同学在讨论锁的释放问题。

之前分析过一个锁表异常，很多用workbench或者类似客户端的同学可能会遇到，
复现方式：
Step 1：显示的打开一个事务，或者把autocommit=0，或者mysql workbench中把自动提交的置灰按钮打开以后
Step 2: 执行一个sql（比如，update或者delete之类的），然后sql还没有返回执行结果的中途点击workbench 自带的那个stop的红色的按钮。
这个时候很多人可能就不再做其他操作，大多会认为执行已经结束了。但是实际上，锁还在继续锁着的并不会释放。

系统日志记录：
（1）processlist的状态是sleep，info为null
（2）innodb_trx的状态是running，trx_query为null
（3）performance_schema.events_statements_current表中的，
sql_text，digest_text：是有正确的sql的。---这个5.6以后就有了，如果ps打开的话，应该是可以看到的。
message_text ：Query execution was interrupted
（4）inoodb_locks，lock_waits，以及show engine innodb status，只有出现锁等待的时候才会记录，如果只有一个事务的记录行锁，或者表锁，是不会记录的。（不知道是否有参考控制，还是默认的）
（5）关于行锁记录数的问题，从测试的结果看，inoodb_trx的locked rows，当我点停止的时候，锁定行数保持不变了，当我继续点击执行的时候，锁定记录行数会在之前的记录上向上累加，并不是从0开始。

然后查了audit log以后发现，客户端（mysqlworkbench）送给server端的是KILL QUERY thread_id，而不是Kill thread_id，
所以MySQL只是终止了事务中的statement执行，但是并不会释放锁，因为目前的琐的获取和释放都是基于事务结束的（提交或者回滚）。
这里面关于kill query&#47; thread_id的区别解释
https:&#47;&#47;dev.mysql.com&#47;doc&#47;refman&#47;5.6&#47;en&#47;kill.html

解决方法：
自己解决：kill 对应的thread_id，或者关闭执行窗口（这个时候会送个quit给server端）。
别人解决：有super权限的人kill thread_id。

关于kill的那个文章，其实对所有DDL，DML的操作释放过程，还没有全部搞清楚，期待老师的第25讲。</div>2019-01-02</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/71/97/f1a3d398.jpg" width="30px"><span>张永志</span> 👍（26） 💬（1）<div>分享一个主从切换时遇到的问题，主从切换前主库要改为只读，设置只读后，show master status发现binlog一直在变化，当时应用没断开。
主库并不是其他库的从库，怎么搞的呢？
检查业务用户权限发现拥有super权限，查看授权语句原来是grant all on *.* to user，这里要说的是*.* 权限就太大了，而且这个也很容易被误解，需要特别注意。</div>2019-01-04</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/48/bd/6c7d4230.jpg" width="30px"><span>Tony Du</span> 👍（17） 💬（8）<div>对于上期问题的解答，有一点不是特别理解，
因为order by desc，在索引c上向左遍历，对于（15， 25）这段区间没有问题，
然后，扫描到c=10才停下来，理论上把（10，15]这个区间锁上就应该是完备的了呀。（5，10]这段区间是否锁上对结果应该没有影响呀，为什么会需要（5，10] 这段的next-key lock ?
2019-01-02
 作者回复
就是这么实现的😓

C=10还是要锁的，如果不锁可能被删除

我的回复：
所以，如果把sql改成
select * from t where c&gt;=15 and c&lt;=20 order by c asc lock in share mode;
那锁的范围就应该是索引c上（10，25）了吧。
同样查询条件，不同的order顺序，锁的范围不一样，稍微感觉有一点奇怪...
</div>2019-01-03</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/73/4f/abb7bfe3.jpg" width="30px"><span>沙漠里的骆驼</span> 👍（15） 💬（1）<div>qps(查询语句)突然增大的情况，我们的实践是:
1. 账号、接口级别的限流。
2.引导到备库执行</div>2019-02-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/21/ae/416a7d6d.jpg" width="30px"><span>Moby</span> 👍（12） 💬（6）<div>丁奇老师好，不好意思，学渣看得比较慢。关于前两期的问题，我有一点没搞懂。就是你说的：&quot;session A 在 select 语句锁的范围是 1.... ; 2.在主键索引上id=10、15、20三个行锁”，经我测试(MySQL版本：5.7.17-log; 隔离级别：可重复读)：“session 
A: begin; select * from t where c&gt;=15 and c&lt;=20 order by c desc lock in share mode;&quot;、&quot;session B:  update t set c=1010 where id=10; Query ok&quot;、”session C:  update t set c=1515 where id=15;block...“。即：为什么id=10这一行可以更新数据？而id=15、20这两行更新数据就被阻塞？</div>2019-01-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/fc/24/7d43d807.jpg" width="30px"><span>mongo</span> 👍（11） 💬（1）<div>看完了《算法导论》那本书的前20章，看到了动态规划。再来看老师的专栏，发现我终于可以无障碍get到本专栏的知识了。</div>2019-07-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/f8/70/f3a33a14.jpg" width="30px"><span>某、人</span> 👍（10） 💬（3）<div>老师,我有几个问题:
1.如果把order by去掉或者order by c asc,往右扫描,为什么没有加[25,30)next-key lock?
2.执行session A,为什么slow log里的Rows_examined为2?按照答案来讲不应该是为3嘛
3.thread states里sending data包括sending data to the client,
另外还有一种state是Sending to client(5.7.8之前叫Writing to net)是writing a packet to the client.
请问针对发送数据给客户端,这两种状态有什么区别？</div>2019-01-02</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/68/d7/714c3d89.jpg" width="30px"><span>不二</span> 👍（9） 💬（1）<div>老师，曾剑同学的问题
关于上期遗留问题的解答，我有一点疑惑：
解答中的1中，第一个要定位的是索引 c 上“最右边的”c=20 的行，为啥只会加上间隙锁（20,25）和next-key lock(15,20]呢，为啥不是两个next-key lock(15,20]和(20,25]呢？25上的行锁难道是退化的？老师上一篇文章中说到加锁的基本原则中第一点是加锁的基本单位是next-key lock，而退化都是基于索引上的等值查询才会发生呀？盼老师指点迷津。
您给回答是定位到c=20的时候，是等值查询，所以加的是(20,25)的间隙锁，25的行锁退化了，那么在上一期中的案例五：唯一索引范围锁 bug，那id&lt;=15,不也是先定位到id=15，然后向右扫描，那应该也是等值查询，那么应该加的是（15，20）间隙锁，那为啥你说的加的是（15，20],为啥这个id=20的行锁也加上了呢，为啥同样是范围查询，一个行锁退化了，一个没有退化呢，求老师指点迷津

</div>2019-01-04</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/71/97/f1a3d398.jpg" width="30px"><span>张永志</span> 👍（9） 💬（1）<div>我是从Oracle转到MySQL来的，先接触的Oracle再看MySQL就经常喜欢拿两者对比，包括表数据存储结构，二级索引的异同，redo，binlog，锁机制，以及默认隔离级别。
研究锁后，根据自己的理解得出一个结论，MySQL默认隔离级别选为RR也是无奈之举！
因为当时binlog还是语句格式，为了保证binlog事务顺序正确就得有gap和next key锁。
而对开发人员来说，他们未必清楚事务隔离级别，且大多数开发都是从Oracle转向MySQL的，故果断将隔离级别全部调整为RC。

</div>2019-01-04</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/ec/1b/650e3dbe.jpg" width="30px"><span>zws</span> 👍（8） 💬（1）<div>老师，如果不是专业的dba看着专栏是不是有点太深了。 老师可不可以把文章分下类，哪部分可以适合业务开发人员看。</div>2019-04-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/47/44/66a6ab1a.jpg" width="30px"><span>刘昆</span> 👍（8） 💬（6）<div>老师你好，上期问题里面我遇到一下问题：
insert into t values(6,5,6) =&gt; block
insert into t values(4,5,6) =&gt; no block
insert into t values(6,4,6) =&gt; no block
insert into t values(7,5,6) =&gt; block
insert into t values(7,4,6) =&gt; no block
根据你的解答，c 上面的 next-key lock 在 (5, 10]，那么上面的情况应该都不会阻塞还对呀？
Server version: 5.7.24-log MySQL Community Server (GPL)
</div>2019-02-02</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/00/f0/08409e78.jpg" width="30px"><span>一大只😴</span> 👍（7） 💬（1）<div>老师，我找到我上次说RR隔离级别下，session 1:begin;select * from t where d=5 for update;  session 2:update t set d=5 where id=0;可以执行的原因了，我配置文件中禁用了间隙锁，innodb_locks_unsafe_for_binlog=on,改成off默认值就正常了。</div>2019-01-03</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/40/5e/b8fada94.jpg" width="30px"><span>Ryoma</span> 👍（7） 💬（4）<div>select * from t where c&gt;=15 and c&lt;=20 order by c desc lock in share mode; 这条语句在索引C上锁的范围是(5,25)；
如果把order by c desc去掉，锁的范围即(10,25]；、
请问老师为什么加上order by c desc后差异这么大，第一次定位到c=20的时候，为什么还要继续往后再查一次呢；而没有order by c desc后，第一次定位到10，就不会往前再查一次，这个差异是什么导致的？</div>2019-01-03</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/71/97/f1a3d398.jpg" width="30px"><span>张永志</span> 👍（5） 💬（1）<div>小系统，昨天一直报CPU使用率高，报警阈值设定为CPU平均使用率0.8。
登录看进程都在执行同一条SQL，活动会话有40个，主机逻辑CPU只有4个，这负载能不高吗？
检查SQL，表很小不到两万行，创建一个复合索引后，负载立刻就消失不见啦😄</div>2019-01-04</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/56/16/f8b22bf5.jpg" width="30px"><span>黄继立</span> 👍（4） 💬（5）<div>老师您好：
     首先要感谢您的分享，您以上的例子在我的线上环境都出现过。 一般情况都是慢sql 语句没有使用索引，我们所有线上的数据库，全部部署了实时kill 脚本，针对查询语句全部进行一个阀值的制定，例如是5秒，超过以后自动kill，这样会保证线上的稳定。 二就是在测试环境严格把控没有使用索引的语句。 </div>2019-03-02</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/21/ae/416a7d6d.jpg" width="30px"><span>Moby</span> 👍（4） 💬（3）<div>谢谢谢谢谢谢老师的回答！“作者回复
这没问题呀
begin; select * from t where c&gt;=15 and c&lt;=20 order by c desc lock in share mode;
锁的范围是这样的：
索引c上，next-key lock: (5，10],(10,15],(15,20];
索引id上，行锁: id=15和id=20”

不过在文末（二十二：MySQL有哪些”饮鸩止渴“提高性能的方法）上写的是“
因此，session A 的 select 语句锁的范围就是：1.索引c上(5,25); 2. 主键索引上id=10、15、20三个行锁”（写错了吧？）</div>2019-01-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/e9/5a/a6f2ec4b.jpg" width="30px"><span>曾剑</span> 👍（4） 💬（1）<div>老师，关于上期遗留问题的解答，我有一点疑惑：
解答中的1中，第一个要定位的是索引 c 上“最右边的”c=20 的行，为啥只会加上间隙锁（20,25）和next-key lock(15,20]呢，为啥不是两个next-key lock(15,20]和(20,25]呢？25上的行锁难道是退化的？老师上一篇文章中说到加锁的基本原则中第一点是加锁的基本单位是next-key lock，而退化都是基于索引上的等值查询才会发生呀？盼老师指点迷津。
</div>2019-01-02</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/cf/2f/4f89f22a.jpg" width="30px"><span>李鑫磊</span> 👍（3） 💬（1）<div>用数据库连接池应该不存在短连接的情况的吧？</div>2019-09-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/63/c6/0167415c.jpg" width="30px"><span>林肯</span> 👍（3） 💬（1）<div>老师，请教个问题。我们线上有台数据库服务器内存长期高达80%，由2核4g升级到4核8g，占用cpu略降(10%），内存仍然是80%多。我观察到我们的连接数长期在600多，是不是连接数导致的？挥或者还可能有哪些原因？谢谢</div>2019-02-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/ea/9a/02d589f9.jpg" width="30px"><span>斜面镜子 Bill</span> 👍（3） 💬（3）<div>业务侧查询特地表A的SQL均通过显式地开启事务控制，存在部分的慢SQL，高并发的查询影响了表A查询的commit效率，没有及时释放DML锁，此时业务发起DDL操作，获取MDL写锁被阻塞，导致后续需要获取MDL读锁的SQL被阻塞，快速导致这个库的连接池被用完，阻塞了整个实例的查询！
</div>2019-01-03</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/05/d4/e06bf86d.jpg" width="30px"><span>长杰</span> 👍（3） 💬（2）<div>在平时的工作中有时候会遇到业务新上一个功能，sql没及时给dba进行审核，导致有些高频sql没有加索引，引起数据库的并发高。通过慢sql分析找到缺索引的表，及时执行alter语句加索引，问题便可得到解决。但有时候由慢sql导致的并发高会导致一些正常高效的sql变慢，通过慢sql排名分析，排名靠前的sql并不是真正需要优化的，如何快速定位慢sql，老师有没有好的方法？</div>2019-01-02</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/1c/15/68680348.jpg" width="30px"><span>Vincent</span> 👍（3） 💬（1）<div>如果使用古老的DDL添加方法，那不是主备的binlog里面都没有Ddl的日志，如果用之前备份加上binlog 恢复的话，那不表结构不一致啦</div>2019-01-02</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/df/94/84296110.jpg" width="30px"><span>Max</span> 👍（3） 💬（2）<div>我们的系统是用php开发的 php没有连接池 所以我就把thread_cache_size 调整一下 把创建过的连接cache起来 用的是thinkphp的框架 这个框架有个功能 每次打开表要show columhs from 表 qps只要到达4000-5000 每个语句状态opening Tom table 然后removing tmp table 造成cpu(system)会爆涨 后来调教了innodb_thread_concurrency=56 另外show colums from 表名 每次会在磁盘上创建一个几k的临时表 然后在删除掉 一到高并发对性能影响很大</div>2019-01-02</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/df/80/f5d91c66.jpg" width="30px"><span>Invictus_CD </span> 👍（2） 💬（1）<div>老师好，这个课后题c≥15加锁和上一课的例子4的c≥10解释的不太一样啊。例子4的直接在10上面加的间隙锁啊，这个为啥要在5上面加呢？</div>2019-02-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/17/6a/c979163e.jpg" width="30px"><span>古娜拉黑暗之神·巴啦啦能量·堕落达</span> 👍（2） 💬（2）<div>老师，您好：
我引用一下 Ryoma 的留言，如下：
Ryoma
我之前的描述有点问题，其实想问的是：为什么加了 order by c desc，第一个定位c=20 的行，会加上间隙锁 (20,25) 和 next-key lock (15,20]？
如果没有order by c desc，第一次命中c=15时，只会加上next-key lock(10.15]；
而有了order by c desc，我的理解是第一次命中c=20只需要加上next-key lock (15,20]
当然最后(20,25)还是加上了锁，老师的结论是对的，我也测试过了，但是我不知道如何解释。
唯一能想到的解释是order by c desc 并不会改变优化2这个原则：即等值查询时，会向右遍历且最后一个值不满足等值条件；同时order by c desc 带来一个类似于优化2的向左遍历原则。
进而导致最后的锁范围是(5,25)；而没有order by c desc的范围是(10,25]。
2019-01-03
 作者回复
因为执行c=20的时候，由于要order by c desc, 就要先找到“最右边第一个c=20的行”，
这个怎么找呢，只能向右找到25，才能知道它左边那个20是“最右的20”

我的问题是：
1. 按照老师您说的，先找c=20，由于是order by c desc，所以要找最右边的20，即找到25。那如果c是唯一索引呢？是不是就不会找到25了（是否会加 (20,25) 的gap lock）？我把语句改造了一下，“select * from t_20 where id &gt;= 15 and id&lt;=20 ORDER BY id desc lock in share mode;”。发现当 session A 执行完这行语句不提交的时候，session B 执行 “insert into t_20 values(24,24,24);” 是阻塞的。也就是说也加了(20,25)的间隙锁。这又是为什么呢？
2. 间隙锁本身不冲突，但和插入语句冲突。那么delete语句呢?
我做了个如下实验（以下语句按时间顺序排序）：
session A
begin;
select * from t_20 where c=10 lock in share mode;

session B
delete from t_20 where c=15;
insert into t_20 values(16,16,16); 
(blocked)

session B 中第一条delete语句执行正常，第二条insert语句被阻塞。
我的分析是：session A在索引c上的锁是：(5,10]  (10,15)；当session B把(15,15,15)这条记录删了之后，(10,15)的间隙就不存在了，所以此时session A在索引c上的锁变为：(5,10]  (10,20)。这时再在session B中插入(16,16,16)就被阻塞了。这个分析正确吗？</div>2019-01-04</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/71/97/f1a3d398.jpg" width="30px"><span>张永志</span> 👍（2） 💬（2）<div>说一个锁全库(schema)的案例，数据库晚间定时任务执行CTAS操作，由于需要执行十几分钟，导致严重会话阻塞，全库所有表上的增删改查全被阻塞。
后改为先建表再插数解决。</div>2019-01-04</li><br/>
</ul>