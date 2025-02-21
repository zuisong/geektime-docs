在上一篇文章中，我提到MySQL对自增主键锁做了优化，尽量在申请到自增id以后，就释放自增锁。

因此，insert语句是一个很轻量的操作。不过，这个结论对于“普通的insert语句”才有效。也就是说，还有些insert语句是属于“特殊情况”的，在执行过程中需要给其他资源加锁，或者无法在申请到自增id以后就立马释放自增锁。

那么，今天这篇文章，我们就一起来聊聊这个话题。

# insert … select 语句

我们先从昨天的问题说起吧。表t和t2的表结构、初始化数据语句如下，今天的例子我们还是针对这两个表展开。

```
CREATE TABLE `t` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `c` int(11) DEFAULT NULL,
  `d` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `c` (`c`)
) ENGINE=InnoDB;

insert into t values(null, 1,1);
insert into t values(null, 2,2);
insert into t values(null, 3,3);
insert into t values(null, 4,4);

create table t2 like t
```

现在，我们一起来看看为什么在可重复读隔离级别下，binlog\_format=statement时执行：

```
insert into t2(c,d) select c,d from t;
```

这个语句时，需要对表t的所有行和间隙加锁呢？

其实，这个问题我们需要考虑的还是日志和数据的一致性。我们看下这个执行序列：

![](https://static001.geekbang.org/resource/image/33/86/33e513ee55d5700dc67f32bcdafb9386.png?wh=931%2A104)

图1 并发insert场景

实际的执行效果是，如果session B先执行，由于这个语句对表t主键索引加了(-∞,1]这个next-key lock，会在语句执行完成后，才允许session A的insert语句执行。

但如果没有锁的话，就可能出现session B的insert语句先执行，但是后写入binlog的情况。于是，在binlog\_format=statement的情况下，binlog里面就记录了这样的语句序列：
<div><strong>精选留言（30）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/14/8c/94/5282994c.jpg" width="30px"><span>huolang</span> 👍（112） 💬（28）<div>老师，死锁的例子，关于sessionA拿到的c=5的记录锁，sessionB和sessionC发现唯一键冲突会加上读锁我有几个疑惑：
1. sessionA拿到的c=5的记录锁是写锁吗？
2. 为什么sessionB和sessionC发现唯一键冲突会加上读锁？
3. 如果sessionA拿到c=5的记录所是写锁，那为什么sessionB和sessionC还能加c=5的读锁，写锁和读锁不应该是互斥的吗？
4.  sessionA还没有提交，为什么sessionB和sessionC能发现唯一键冲突？</div>2019-02-13</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTIEl3fX9nvzUF26ekUIicp4sgA5jZ1mGvGMhIHkwJabbjt9h5uTLw5zzU1U6JZbCSpRXBNQwuejLJg/132" width="30px"><span>轻松的鱼</span> 👍（72） 💬（12）<div>老师好，想请教一下死锁的例子中：
1. 在 session A rollback 前，session B&#47;C 都因为唯一性冲突申请了 S Next-key lock，但是被 session A 的 X but not gap lock 阻塞；
2. 在 session A rollbak 后，session B&#47;C 顺利获得 S Next-key lock，并且都要继续进行插入，这时候我认为是因为插入意向锁（LOCK_INSERT_INTENTION）导致的死锁，因为插入意向锁会被 gap lock 阻塞，造成了相互等待。还没有进入到记录 X lock。
不知道我分析的对不对？</div>2019-03-06</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/f9/48/bf570bab.jpg" width="30px"><span>sonic</span> 👍（51） 💬（4）<div>你好，
我想问下文章中关于为什么需要创建临时表有这一句话：
如果读出来的数据直接写回原表，就可能在遍历过程中，读到刚刚插入的记录，新插入的记录如果参与计算逻辑，就跟语义不符。

我的疑问是：既然隔离级别是可重复读，照理来说新插入的的记录应该不会参与计算逻辑呀。</div>2019-02-14</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTJCscgdVibmoPyRLRaicvk6rjTJxePZ6VFHvGjUQvtfhCS6kO4OZ1AVibbhNGKlWZmpEFf2yA6ptsqHw/132" width="30px"><span>夹心面包</span> 👍（51） 💬（2）<div>
1 关于insert造成死锁的情况,我之前做过测试,事务1并非只有insert,delete和update都可能造成死锁问题,核心还是插入唯一值冲突导致的.我们线上的处理办法是 1 去掉唯一值检测 2减少重复值的插入 3降低并发线程数量
2 关于数据拷贝大表我建议采用pt-archiver,这个工具能自动控制频率和速度,效果很不错,提议在低峰期进行数据操作</div>2019-02-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/b8/36/542c96bf.jpg" width="30px"><span>Mr.Strive.Z.H.L</span> 👍（36） 💬（2）<div>老师您好：
关于文中的锁描述有所疑惑。

文中出现过 共享的next-key锁 和 排他的next-key锁。

我们知道next-key是由 gap lock 和 行锁组成的。

我一直以来的认知是 gap lock都是s锁，没有x锁。
而行锁有s锁和x锁。
比如 select………lock in share mode，行锁是s
锁。
比如select………for update，行锁就是x锁。
但是gap lock 始终是s锁。

文中直接描述next-key lock是排他的，总让我认为gap lock和行锁都是x锁。

不知道我理解得对不对？</div>2019-02-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/03/f7/3a493bec.jpg" width="30px"><span>老杨同志</span> 👍（32） 💬（1）<div>课后问题：
      我用的最多还是insert into select 。如果数量比较大，会加上limit 100,000这种。并且看看后面的select条件是否走索引。缺点是会锁select的表。方法二：导出成excel，然后拼sql 成 insert into values(),(),()的形式。方法3，写类似淘宝调动的定时任务，任务的逻辑是查询100条记录，然后多个线程分到几个任务执行，比如是个线程，每个线程10条记录，插入后，在查询新的100条记录处理。
      </div>2019-02-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/ec/01/978d54af.jpg" width="30px"><span>Justin</span> 👍（25） 💬（7）<div>插入意向锁的gal lock和next key lock中的 gaplock互斥吗？</div>2019-02-15</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/00/f0/08409e78.jpg" width="30px"><span>一大只😴</span> 👍（19） 💬（6）<div>老师，我想问下：insert 语句出现唯一键冲突，会加next-key lock，而产生死锁的例子中，同样也是唯一键冲突却只加了记录锁，然后我按照唯一键冲突中的两个例子试了试
1、比如t表中有两条记录(19,19,19)，(22,22,22)，这时候我再insert (22,22,22)造成了主键冲突，这时候加的就是(19,22]的next-key lock，这个insert为啥不是等值查询？
2、根据死锁的例子，我又在t表中准备插入一行
      session A :begin; insert into t values (25,25,25)
      session B :insert into t values (25,25,25)  这时候sessionB锁等待
      session C：insert into t values (24,24,24)  锁等待，等B锁等待超时，session C插入成功
      那这里的session B应该是加了个(22,25]的next-key lock，并没有因为是唯一键退化成记录锁
我想死锁的例子中t表已经有了(1,1,1),(2,2,2),(3,3,3),(4,4,4)4条记录，这时候insert (null,5,5)，是不是加的(4,5]这个next-key lock，由于是整型并且间隙非常小，所以将他当成记录锁？</div>2019-02-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/03/e2/5768d26e.jpg" width="30px"><span>inrtyx</span> 👍（17） 💬（2）<div>现在一般都用utf8mb4?</div>2019-04-07</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/db/80/6b7629d7.jpg" width="30px"><span>roaming</span> 👍（15） 💬（1）<div>MySQL8.0.12环境下，
执行insert into t(c,d)  (select c+1, d from t force index(c) order by c desc limit 1);
slow log Rows_examined: 2
Innodb_rows_read 的值增加1

是不是MySQL8进行了优化，先把子查询的结果读出来，再写入临时表？</div>2019-02-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/e5/39/951f89c8.jpg" width="30px"><span>信信</span> 👍（13） 💬（1）<div>老师好，文中提到：insert into t2(c,d) (select c+1, d from t force index(c) order by c desc limit 1)的加锁范围是表 t 索引 c 上的 (4,supremum] 这个 next-key lock 和主键索引上 id=4 这一行。
可是如果我把表t的id为3这行先删除，再执行这个insert...select，那么别的会话执行insert into t values(3,3,3)会被阻塞，这说明4之前也是有间隙锁的？
另外，select c+1, d from t force index(c) order by c desc limit 1 for update 是不是不能用作等值查询那样分析？因为如果算等值查询，根据优化1是没有间隙锁的。</div>2019-02-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/ec/01/978d54af.jpg" width="30px"><span>Justin</span> 👍（11） 💬（2）<div>为什么insert 还会使用到next key lock 呢 ，我记得我原来看的资料写的是插入使用的是插入意向锁啊</div>2019-02-15</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/e5/39/951f89c8.jpg" width="30px"><span>信信</span> 👍（10） 💬（3）<div>老师好，
图6下方“发生主键冲突的时候”是不是应该改为“发生唯一键冲突的时候”？因为c不是主键。
还有，图7下方：T2时刻session b 发现“唯一键冲突”，这里为啥不是锁冲突？因为如果没有锁冲突，仅有唯一键冲突，就对应图6的情况，这时加的是next-key lock，而不仅仅是记录锁了。</div>2019-02-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/ea/aa/cdd13ad2.jpg" width="30px"><span>王伯轩</span> 👍（9） 💬（4）<div>老师你好,去年双11碰到了dbcrash掉的情况.至今没有找到答案,心里渗得慌.老师帮忙分析下.  
我是一个开发,关于db的知识更多是在应用和基本原理上面,实在是找不到原因. 我也搜了一些资料 感觉像是mysql的bug,不过在其buglist中没有找到完全一致的，当然也可能是我们业务也许导致库的压力大的原因.   
应用端看到的现象是db没有响应，应用需要访问db的线程全部僵死.db表现是hang住 , 当时的诊断日志如下，表面表现为一直获取不到latch锁（被一个insert线程持有不释放） https:&#47;&#47;note.youdao.com&#47;ynoteshare1&#47;index.html?id=1771445db3ff1e08cbdd8328ea6765a7&amp;type=note#&#47;  隔离级别是rr

同样的crash双11当天后面又出现了一次（哭死）,
都是重启数据库解决的,

后面应用层面做了一样优化,没有再crash过，优化主要如下：
1.减小读压力，去除一些不必要的查询，
2.优化前，有并发事务写和查询同一条数据记录，即事务a执行insert 尚未提交，事务b就来查询（快照读），优化后保证查询时insert事务已经提交</div>2019-02-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/1d/30/3e280597.jpg" width="30px"><span>phpzheng</span> 👍（8） 💬（1）<div>循环插入数据，然后拿着刚刚插入的主键id，更新数据。请问怎么提高这个情况的效率</div>2019-02-15</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTJCscgdVibmoPyRLRaicvk6rjTJxePZ6VFHvGjUQvtfhCS6kO4OZ1AVibbhNGKlWZmpEFf2yA6ptsqHw/132" width="30px"><span>夹心面包</span> 👍（7） 💬（2）<div>我来补充应用表空间迁移的场景
1  冷数据表的复制和迁移
2 大表数据的恢复,线上DDL操作失误,需要恢复时,利用备份+binlog进行恢复后,表空间迁移进行导入
对于热表数据的复制建议还是采用pt-archiver慢慢搞</div>2019-02-15</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/36/d2/c7357723.jpg" width="30px"><span>发条橙子 。</span> 👍（5） 💬（2）<div>老师，年后过来狂补课程了哈哈 ， 看到老师的bug留言已经被fix掉准备在最新版本发布了呢。 

这里我有一个疑问， 我之前以为只有更新的时候才会加锁， 参考前面的文章，innodb要先扫描表中数据，被扫描到的行要加锁 。

或者我们执行 select 的时候手动加上 排他锁 或者 共享锁，也会锁住。

这里老师讲到如果索引唯一键冲突， innodb为了做处理加了 next_key lock（S） 这个可以理解。

insert .. select 也是因为有 select 索引会加锁 也可以理解

问题 ：

图7那个死锁的案例， session A 的时候 只是执行了 insert 语句，执行 insert的时候也没有select之类的，为什么也会在索引c上加个锁， 是什么时候加的呢 ？？？ 是 insert 语句有索引的话都会给索引加锁么？？

</div>2019-02-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/e3/2e/77ad18f4.jpg" width="30px"><span>滔滔</span> 👍（5） 💬（1）<div>老师，有个问题insert into … on duplicate key update语句在发生冲突的时候是先加next key读锁，然后在执行后面的update语句时再给冲突记录加上写锁，从而把之前加的next key读锁变成了写锁，是这样的吗？</div>2019-02-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/ea/aa/cdd13ad2.jpg" width="30px"><span>王伯轩</span> 👍（5） 💬（1）<div>内存锁 大大计划讲下么,实际中碰到内存锁被持有后一直不释放导致db直接crash掉</div>2019-02-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/e3/2e/77ad18f4.jpg" width="30px"><span>滔滔</span> 👍（5） 💬（1）<div>老师您好，想问一下next key lock是gap锁和行锁的组合，但究竟是gap锁和共享锁还是排它锁的组合是不是要看具体的sql语句？具体哪些sql语句中的next key lock是由共享锁组成，哪些是由排它锁组成呢？🤔</div>2019-02-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/71/97/f1a3d398.jpg" width="30px"><span>张永志</span> 👍（4） 💬（1）<div>对主键插入加读锁的个人理解，两个会话insert同样记录，在没有提交情况下，insert主键加读锁是为了避免第一个会话回滚后，第二个会话可以正常执行；第一个会话提交后，第二个会话再报错。</div>2019-02-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/f5/ff/523fb378.jpg" width="30px"><span>颜海航</span> 👍（4） 💬（1）<div>[Note] Multi-threaded slave: Coordinator has waited 8551 times hitting slave_pending_jobs_
size_max; current event size = 8198. 老师 我们数据库一直报这个错，然后数据库就进行crash recovery，是是什么状况。。</div>2019-02-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/ec/01/978d54af.jpg" width="30px"><span>Justin</span> 👍（3） 💬（1）<div>那如果是冲突时 会加next key lock的话 间隙锁和插入意向锁不会冲突吗？</div>2019-02-15</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/e3/2e/77ad18f4.jpg" width="30px"><span>滔滔</span> 👍（3） 💬（1）<div>老师，之前提到的一个有趣的问题&quot;A、B两个用户，如果互相喜欢，则成为好友。设计上是有两张表，一个是like表，一个是friend表，like表有user_id、liker_id两个字段，我设置为复合唯一索引即uk_user_id_liker_id。语句执行顺序是这样的：
以A喜欢B为例：
1、先查询对方有没有喜欢自己（B有没有喜欢A）
select * from like where user_id = B and liker_id = A
2、如果有，则成为好友
insert into friend
3、没有，则只是喜欢关系
insert into like&quot;，这个问题中如果把select语句改成&quot;当前读&quot;，则当出现A,B两个人同时喜欢对方的情况下，是不是会出现由于&quot;当前读&quot;加的gap锁导致后面insert语句阻塞，从而发生死锁？</div>2019-02-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/31/4d/ea8ac77c.jpg" width="30px"><span>伟仔_Hoo</span> 👍（2） 💬（1）<div>老师，看到您的回复，当select c+1, d from t force index(c) order by c desc limit 1;这条语句单独执行是会在c索引上加(4,sup] 这个next key lock, 于是我进行了尝试
sessionA: 
begin;
select c+1, d from t3 force index(c) order by c desc limit 1;
sessionB:
insert into t3 values(5, 5, 5);
结果是，sessionB插入成功，是不是我哪里理解错了？我的版本是5.7.23</div>2019-03-15</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/34/ce/289dadb6.jpg" width="30px"><span>Lilian</span> 👍（2） 💬（2）<div>老师，重复主键插入冲突是否推荐insert ignore方法？</div>2019-03-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/df/e7/4ce5ed27.jpg" width="30px"><span>lunung</span> 👍（1） 💬（1）<div>mysql&gt; insert into t select null,5,5; 已经又4条记录
mysql&gt; select * from t;
| 1 | 1 | 1 |
| 2 | 2 | 100 |
| 3 | 3 | 3 |
| 4 | 4 | 4 |
| 5 | 5 | 5 |
+----+------+------+
5 rows in set (0.00 sec)

mysql&gt; select last_insert_id();
+------------------+
| last_insert_id() |
+------------------+
| 5 |
+------------------+
1 row in set (0.00 sec)

mysql&gt; select * from t2; 已经有三条记录
+----+------+------+
| id | c | d |
+----+------+------+
| 5 | 1 | NULL |
| 6 | 6 | 6 |
| 7 | 7 | 7 |
+----+------+------+
3 rows in set (0.01 sec)
mysql&gt; select last_insert_id(); 此处的自增ID 是否理解为 最近一次的 insert 操作的 获取的ID
+------------------+
| last_insert_id() |
+------------------+
| 5 |
+------------------+
1 row in set (0.00 sec)

mysql&gt; insert into t2 select null,8,8;
Query OK, 1 row affected (0.01 sec)
Records: 1 Duplicates: 0 Warnings: 0

mysql&gt; select last_insert_id();
+------------------+
| last_insert_id() |
+------------------+
| 8 |
+------------------+
1 row in set (0.00 sec)

mysql&gt; select * from t2;
+----+------+------+
| id | c | d |
+----+------+------+
| 5 | 1 | NULL |
| 6 | 6 | 6 |
| 7 | 7 | 7 |
| 8 | 8 | 8 |
+----+------+------+
4 rows in set (0.00 sec)
mysql&gt; select last_insert_id(); 此处的自增ID 是否理解为 最近一次的 insert 操作的 获取的ID
+------------------+
| last_insert_id() |
+------------------+
| 8 |
+------------------+
1 row in set (0.00 sec)
上面的 ID 与那个表没有关系, 至于当前session insert 最新一次记录为准 
mysql&gt; select last_insert_id();
|                8 |
+------------------+
1 row in set (0.00 sec)
mysql&gt; insert into t2 select 19,19,19;
mysql&gt; select last_insert_id();
+------------------+
| last_insert_id() |
+------------------+
|                8 |
+------------------+
1 row in set (0.00 sec)
mysql&gt; insert into t2 select null,20,20;
Query OK, 1 row affected (0.01 sec)
Records: 1  Duplicates: 0  Warnings: 0

mysql&gt; select last_insert_id();
+------------------+
| last_insert_id() |
+------------------+
|               20 |
+------------------+
ID 除非为空的时候 才能获取到新的last_insert_id</div>2019-02-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/df/90/68408c1b.jpg" width="30px"><span>郭烊千玺</span> 👍（1） 💬（1）<div>有个问题想请教下大神  information_schema.tables  表里的这三个字段data_length  data_free  index_length的值准确吗，mysql内部是怎么计算每个表的这个三个值的？在没有碎片的情况下，实践上用du 命令统计的ibd的大小和这几个字段的值感觉差别很大，所以很想知道这几个字段的值得准确度如何，还是仅供参考，因为实践中可能需要知道是否有碎片，如果date_free值不准确，而盲目的alter table一下，表大的话代价很高啊 求回答啊 感觉这也是很多dba关心的一个问题</div>2019-02-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/e3/2e/77ad18f4.jpg" width="30px"><span>滔滔</span> 👍（0） 💬（1）<div>老师，select c+1, d from t force index(c) order by c desc limit 1;这条语句如果单独执行，是会对表t进行全表加锁，还是只加(3,4],(4,sup]这两个next key锁。还有一个问题，这里为什么要加force index(c)，不加会是怎样的效果呢？🤔</div>2019-02-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/7c/56/dd5e7e0a.jpg" width="30px"><span>Geek_ct4ha3</span> 👍（0） 💬（2）<div>表结构
CREATE TABLE `PushTask` (
  `Id` int(11) NOT NULL AUTO_INCREMENT COMMENT &#39;主键ID，自增长&#39;,
  `DpId` varchar(100) NOT NULL DEFAULT &#39;&#39;,
  `DetailId` int(11) NOT NULL,
  `SceneType` tinyint(1) DEFAULT NULL,
  `DataId` int(11) DEFAULT NULL,
  `SendTime` datetime NOT NULL,
  `AddTime` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `UpdateTime` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `Status` tinyint(1) DEFAULT &#39;0&#39;,
  `SendDate` date DEFAULT NULL,
  PRIMARY KEY (`Id`),
  UNIQUE KEY `IX_DpId_SendDate_DetailId` (`DpId`,`SendDate`,`DetailId`),
  KEY `IX_UpdateTime` (`UpdateTime`),
  KEY `IX_SendTime` (`SendTime`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

请问老师，为啥insert ... ON DUPLICATE KEY UPDATE
        UpdateTime = now()的时候会出现死锁？</div>2019-02-13</li><br/>
</ul>