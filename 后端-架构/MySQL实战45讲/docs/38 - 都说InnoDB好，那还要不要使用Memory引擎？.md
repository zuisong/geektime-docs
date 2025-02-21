我在上一篇文章末尾留给你的问题是：两个group by 语句都用了order by null，为什么使用内存临时表得到的语句结果里，0这个值在最后一行；而使用磁盘临时表得到的结果里，0这个值在第一行？

今天我们就来看看，出现这个问题的原因吧。

# 内存表的数据组织结构

为了便于分析，我来把这个问题简化一下，假设有以下的两张表t1 和 t2，其中表t1使用Memory 引擎， 表t2使用InnoDB引擎。

```
create table t1(id int primary key, c int) engine=Memory;
create table t2(id int primary key, c int) engine=innodb;
insert into t1 values(1,1),(2,2),(3,3),(4,4),(5,5),(6,6),(7,7),(8,8),(9,9),(0,0);
insert into t2 values(1,1),(2,2),(3,3),(4,4),(5,5),(6,6),(7,7),(8,8),(9,9),(0,0);
```

然后，我分别执行select * from t1和select * from t2。

![](https://static001.geekbang.org/resource/image/3f/e6/3fb1100b6e3390357d4efff0ba4765e6.png?wh=599%2A330)

图1 两个查询结果-0的位置

可以看到，内存表t1的返回结果里面0在最后一行，而InnoDB表t2的返回结果里0在第一行。

出现这个区别的原因，要从这两个引擎的主键索引的组织方式说起。

表t2用的是InnoDB引擎，它的主键索引id的组织方式，你已经很熟悉了：InnoDB表的数据就放在主键索引树上，主键索引是B+树。所以表t2的数据组织方式如下图所示：

![](https://static001.geekbang.org/resource/image/4e/8d/4e29e4f9db55ace6ab09161c68ad8c8d.jpg?wh=1142%2A880)

图2 表t2的数据组织

主键索引上的值是有序存储的。在执行select \*的时候，就会按照叶子节点从左到右扫描，所以得到的结果里，0就出现在第一行。

与InnoDB引擎不同，Memory引擎的数据和索引是分开的。我们来看一下表t1中的数据内容。
<div><strong>精选留言（30）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/11/fa/44/aa19d1f6.jpg" width="30px"><span>放</span> 👍（26） 💬（1）<div>老师新年快乐！过年都不忘给我们传授知识！</div>2019-02-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/20/3a/90db6a24.jpg" width="30px"><span>Long</span> 👍（23） 💬（1）<div>老师新年好 :-)
刚好遇到一个问题。 

本来准备更新到，一个查询是怎么运行的里面的，看到这篇更新文章，就写在这吧，希望老师帮忙解答。

关于这个系统memory引擎表：information_schema.tables
相关信息如下
（1）Verison: MySQL 5.6.26
（2）数据量table_schema = abc的有接近4W的表，整个实例有接近10W的表。（默认innodb引擎）
（3）mysql.user和mysql.db的数据量都是100-200的行数，MyISAM引擎。
（4）默认事务隔离级别RC


在运行查询语句1的时候：select * from information_schema.tables where table_schema = &#39;abc&#39;;
状态一直是check permission，opening tables，其他线程需要打开的表在opend tables里面被刷掉的，会显示在opening tables，可能需要小几秒后基本恢复正常。

但是如果在运行查询语句2：select count(1) from information_schema.tables where table_schema = &#39;abc&#39;; 这个时候语句2本身在profiling看长期处于check permission状态，其他线程就会出现阻塞现象，大部分卡在了opening tables，小部分closing tables。我测试下了，当个表查询的时候check permission大概也就是0.0005s左右的时间，4W个表理论良好状态应该是几十秒的事情。
但是语句1可能需要5-10分钟，语句2需要5分钟。

3个问题，请老师抽空看下：
（1）information_schema.tables的组成方式，是我每次查询的时候从数据字典以及data目录下的文件中实时去读的吗？
（2）语句1和语句2在运行的时候的过程分别是怎样的，特别是语句2。
（3）语句2为什么会出现大量阻塞其他事务，其他事务都卡在opening tables的状态。


PS: 最后根据audit log分析来看，语句实际上是MySQL的一个客户端Toad发起的，当使用Toad的object explorer的界面来查询表，或者设置connection的时候指定的的default schema是大域的时候就会run这个语句：（table_schema改成了abc，其他都是原样）
SELECT COUNT(1) FROM information_schema.tables WHERE table_schema = &#39;abc&#39; AND table_type != &#39;VIEW&#39;;


再次感谢！</div>2019-02-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/1e/4c/d6416f57.jpg" width="30px"><span>salt</span> 👍（22） 💬（3）<div>新年好！
课后作业：在备库配置跳过该内存表的主从同步。

有一个问题一直困扰着我：SSD以及云主机的广泛运用，像Innodb这种使用WAL技术似乎并不能发挥最大性能（我的理解：基于SSD的WAL更多的只是起到队列一样削峰填谷的作用）。对于一些数据量不是特别大，但读写频繁的应用（比如点赞、积分），有没有更好的引擎推荐。</div>2019-02-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/da/ec/779c1a78.jpg" width="30px"><span>往事随风，顺其自然</span> 👍（18） 💬（3）<div>为什么memory 引擎中数据按照数组单独存储，0索引对应的数据怎么放到数组的最后</div>2019-02-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/df/e7/4ce5ed27.jpg" width="30px"><span>lunung</span> 👍（16） 💬（1）<div>重启前 my.cnf 添加 skip-slave-errors 忽略 内存表引起的主从异常导致复制失败

</div>2019-02-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/97/f4/6709b8cf.jpg" width="30px"><span>llx</span> 👍（12） 💬（1）<div>1、如果临时表读数据的次数很少（比如只读一次），是不是建临时表时不创建索引效果很更好？
2、engine=memory 如果遇到范围查找，在使用哈希索引时应该不会使用索引吧</div>2019-02-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/ef/3e/9c3a8abc.jpg" width="30px"><span>杜嘉嘉</span> 👍（11） 💬（1）<div>我的认识里，有一点不是很清楚。memory这个存储引擎，最大的特性应该是把数据存到内存。但是innodb也可以把数据存到内存，不但可以存到内存(innodb buffer size)，还可以进行持久化。这样一对比，我感觉memory的优势更没有了。不知道我讲的对不对</div>2019-02-10</li><br/><li><img src="" width="30px"><span>晚风·和煦</span> 👍（9） 💬（1）<div>老师，内存表就是使用memory引擎创建的表吗？😂</div>2020-01-16</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/9a/64/eea9aa33.jpg" width="30px"><span>陈扬鸿</span> 👍（6） 💬（2）<div>老师你好，今天生产上出碰到一个解决不了的问题,php的yii框架，使用show full processlist 查看 全是如下语句有100多条
SELECT
    kcu.constraint_name,
    kcu.column_name,
    kcu.referenced_table_name,
    kcu.referenced_column_name
FROM information_schema.referential_constraints AS rc
JOIN information_schema.key_column_usage AS kcu ON
    (
        kcu.constraint_catalog = rc.constraint_catalog OR
        (kcu.constraint_catalog IS NULL AND rc.constraint_catalog IS NULL)
    ) AND
    kcu.constraint_schema = rc.constraint_schema AND
    kcu.constraint_name = rc.constraint_name
WHERE rc.constraint_schema = database() AND kcu.table_schema = database()
AND rc.table_name = &#39;t1&#39; AND kcu.table_name = &#39;t1&#39; 
这个可以优化吗 这个库是数据字典的 现在数据库无法对外提供服务  请老师指教！</div>2019-03-06</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTJCscgdVibmoPyRLRaicvk6rjTJxePZ6VFHvGjUQvtfhCS6kO4OZ1AVibbhNGKlWZmpEFf2yA6ptsqHw/132" width="30px"><span>夹心面包</span> 👍（5） 💬（1）<div>我们线上就有一个因为内存表导致的主从同步异常的例子,我的做法是先跳过这个表的同步,然后开发进行改造,取消这张表的作用</div>2019-02-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/05/d4/e06bf86d.jpg" width="30px"><span>长杰</span> 👍（2） 💬（1）<div>内存表一般数据量不大，并且更新不频繁，可以写一个定时任务，定期检测内存表的数据，如果数据不空，就将它持久化到一个innodb同结构的表中，如果为空，就反向将数据写到内存表中，这些操作可设置为不写入binlog。</div>2019-02-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/20/3a/90db6a24.jpg" width="30px"><span>Long</span> 👍（1） 💬（1）<div>追问更新1: 谢谢老师的答复，我看了下innodb_stats_on_metadata就是OFF，今天在5.7环境验证，发现竟然不是几百秒，而且几秒，不知道这个是代码的优化，还是参数不一致的原因，有几十个参数差异需要排查。   所以在不知道是因为参数变化导致，还是内部查询逻辑变化。如果是参数，担心有一天被人设置错，又回滚到不好的情况. 老师，我想入坑源码了… </div>2019-03-01</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/20/3a/90db6a24.jpg" width="30px"><span>Long</span> 👍（1） 💬（1）<div>追问：多谢老师回复，在上面回复中，为什么语句2会阻塞其他的线程把其他线程都卡在opening tables 和closing tables，而语句1不会.

猜测是不是语句2用了lock_open的方法？
老师有什么好的建议，我怎么能通过日志或者调试来看？
已经看了innodb status, processlist, profiling都看了，没发现异常

语句1: SELECT table_name, table_schema, data_length, index_length FROM information_schema.TABLES WHERE ENGINE in (&#39;MyISAM&#39;,&#39;InnoDB&#39;) and table_schema &lt;&gt; &#39;information_schema&#39;;

语句2:select count(1) from information_schema.tables where table_schema = &#39;abc&#39;;</div>2019-03-01</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/11/18/8cee35f9.jpg" width="30px"><span>HuaMax</span> 👍（0） 💬（1）<div>课后题。是不是可以加上创建表的操作，并且是innodb 类型的？</div>2019-02-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/03/f7/3a493bec.jpg" width="30px"><span>老杨同志</span> 👍（0） 💬（1）<div>安装之前学的知识，把主库delete语句的gtid，设置到从库中，就可以跳过这条语句了吧。
但是主备不一致是不是要也处理一下，将主库的内存表数据备份一下。然后delete数据，重新插入。
等备件执行者两个语句后，主备应该都有数据了</div>2019-02-08</li><br/><li><img src="" width="30px"><span>Geek_da015d</span> 👍（17） 💬（4）<div>很重要的一点没说啊，内存表不支持事务。怪不得写demo的时候总锁不住</div>2020-11-25</li><br/><li><img src="" width="30px"><span>Geek_6krw94</span> 👍（2） 💬（0）<div>问句：在真实业务场景中真的有像文中动态创建临时表这么用的吗？怎么感觉这么反人类啊</div>2021-06-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/3b/55/ad/791d0f5e.jpg" width="30px"><span>joyboy</span> 👍（0） 💬（0）<div>学习本篇文章的收获：
1.正常所有场景都建议使用innodb引擎来建表，因为memory引擎容易丢数据，并且只支持表级锁并发度不高
2.当需要使用内存临时表的时候，memory引擎会比innodb引擎更合适，因为memory引擎默认是使用hash索引来组织数据的，这时候会更快。</div>2024-07-15</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/32/4b/9c/3a33f731.jpg" width="30px"><span>someone: )</span> 👍（0） 💬（0）<div>最后一个例子中，是对字段b进行范围查询，不应该是b树索引优于hash索引吗？</div>2023-08-31</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/27/02/65/ddb6460e.jpg" width="30px"><span>柯里</span> 👍（0） 💬（0）<div>没有表后，全量同步？？</div>2023-05-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1d/1e/2b/138e26e5.jpg" width="30px"><span>G95</span> 👍（0） 💬（0）<div>老师，MySQL8.0.30中，Memory引擎的数据表应该也实现行级锁，图6的示例我没发重现，没有出现SessionB被SessionA阻塞的情况。</div>2023-04-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1f/5e/81/82709d6e.jpg" width="30px"><span>码小呆</span> 👍（0） 💬（1）<div>有一个问题就是,备库,为什么还需要去同步主库呢,不应该都是主库去更新备库吗</div>2023-01-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/27/13/a8/38255467.jpg" width="30px"><span>yangman</span> 👍（0） 💬（0）<div>老师你好，有个问题：为什么相同的数据，t1和t2的data_length会相差这么大？ 
Name |Engine|Rows |Data_length|
-----+------+-----+-----------+
t1   |MEMORY|   10|     126992|
t2   |InnoDB|   10|      16384|
</div>2021-08-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/24/2b/ef/7d650974.jpg" width="30px"><span>bulingbuling</span> 👍（0） 💬（0）<div>老师:
memory和innodb引擎的区别第3点:数据位置发生变化的时候，InnoDB 表只需要修改主键索引，而内存表需要修改所有索引。这句话没理解，数据位置发生变化的时候，memory修改所有索引的原理是什么</div>2021-06-02</li><br/><li><img src="" width="30px"><span>Geek_66dfcd</span> 👍（0） 💬（1）<div>临时表是临时表，临时表存在磁盘上，内存表是内存表，内存表存在内存中，为什么这里说用户临时表是普通内存表的一个例外呢？</div>2020-11-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/19/15/03/682bd618.jpg" width="30px"><span>DavidJiang</span> 👍（0） 💬（1）<div>按照全表扫描原理，扫描的行数应该是总行数。但是如下实验发现并不相同。—todo list
               另外，增加了list，原则上应该扫描前十行就可以了，为啥也是全表扫描
mysql&gt; select count(*) from employees;
+----------+
| count(*) |
+----------+
|   300024 |
+----------+
1 row in set (0.09 sec)


mysql&gt; explain select * from employees ;
+----+-------------+-----------+------------+------+---------------+------+---------+------+--------+----------+-------+
| id | select_type | table     | partitions | type | possible_keys | key  | key_len | ref  | rows   | filtered | Extra |
+----+-------------+-----------+------------+------+---------------+------+---------+------+--------+----------+-------+
|  1 | SIMPLE      | employees | NULL       | ALL  | NULL          | NULL | NULL    | NULL | 299202 |   100.00 | NULL  |
+----+-------------+-----------+------------+------+---------------+------+---------+------+--------+----------+-------+
1 row in set, 1 warning (0.02 sec)


mysql&gt; explain select * from employees limit 10;
+----+-------------+-----------+------------+------+---------------+------+---------+------+--------+----------+-------+
| id | select_type | table     | partitions | type | possible_keys | key  | key_len | ref  | rows   | filtered | Extra |
+----+-------------+-----------+------------+------+---------------+------+---------+------+--------+----------+-------+
|  1 | SIMPLE      | employees | NULL       | ALL  | NULL          | NULL | NULL    | NULL | 299202 |   100.00 | NULL  |
+----+-------------+-----------+------------+------+---------------+------+---------+------+--------+----------+-------+
1 row in set, 1 warning (0.01 sec)
</div>2020-11-06</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/19/15/03/682bd618.jpg" width="30px"><span>DavidJiang</span> 👍（0） 💬（2）<div>     博主好，大家好，请教两个问题。
1、问题一：不指定顺序是否就是按照主键索引顺序输出结果。下面是验证部分
mysql&gt; select * from employees limit 10;
mysql&gt; select emp_no from employees limit 10;
+--------+
| emp_no |
+--------+
|  10001 |
|  10002 |
|  10003 |
|  10004 |
|  10005 |
|  10006 |
|  10007 |
|  10008 |
|  10009 |
|  10010 |

mysql&gt; select first_name from employees limit 10;
+------------+
| first_name |
+------------+
| Georgi     |
| Bezalel    |
| Parto      |
| Chirstian  |
| Kyoichi    |
| Anneke     |
| Tzvetan    |
| Saniya     |
| Sumant     |
| Duangkaew  |

问题二、select如果全表扫描，按照文章分析应该扫描行数就是总的rows数，但是验证结果确不是，为啥？另外，加limit为啥还是全表扫描？
mysql&gt; select count(*) from employees;
+----------+
| count(*) |
+----------+
|   300024 |
+----------+

mysql&gt; explain select * from employees ;
+----+-------------+-----------+------------+------+---------------+------+---------+------+--------+----------+-------+
| id | select_type | table     | partitions | type | possible_keys | key  | key_len | ref  | rows   | filtered | Extra |
+----+-------------+-----------+------------+------+---------------+------+---------+------+--------+----------+-------+
|  1 | SIMPLE      | employees | NULL       | ALL  | NULL          | NULL | NULL    | NULL | 299202 |   100.00 | NULL  |


mysql&gt; explain select * from employees limit 10;
+----+-------------+-----------+------------+------+---------------+------+---------+------+--------+----------+-------+
| id | select_type | table     | partitions | type | possible_keys | key  | key_len | ref  | rows   | filtered | Extra |
+----+-------------+-----------+------------+------+---------------+------+---------+------+--------+----------+-------+
|  1 | SIMPLE      | employees | NULL       | ALL  | NULL          | NULL | NULL    | NULL | 299202 |   100.00 | NULL  |
+----+-------------+-----------+------------+------+---------------+------+---------+------+--------+----------+-------+</div>2020-11-06</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/e1/5c/86606d9c.jpg" width="30px"><span>湮汐</span> 👍（0） 💬（0）<div>利用临时表去进行关联查询，特别是在写报表的时候去用临时表，那么速度会更快！</div>2020-05-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/d3/86/b5d72c87.jpg" width="30px"><span>Zhaoyang</span> 👍（0） 💬（0）<div>内存表：锁粒度比较粗，还有就是放到内存里面重启会丢数据。</div>2020-01-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/67/f4/9a1feb59.jpg" width="30px"><span>钱</span> 👍（0） 💬（0）<div>老师 memory 引擎，只有表锁，这个表锁是锁在哪里？
“在内存表 t1 中，当我执行 select * 的时候，走的是全表扫描，也就是顺序扫描这个数组。因此，0 就是最后一个被读到，并放入结果集的数据。”
这个数组是指存放数据的数组，这次(0,0)是在数据数组的最后，难道每次都会放在最后，没明白为什么会这样？
另外，看图3存放数据的数组是有序的，难道是先依次存好数据，然后对主键哈希定位主键应该存放的位置？</div>2019-08-06</li><br/>
</ul>