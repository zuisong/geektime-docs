在你开发应用的时候，一定会经常碰到需要根据指定的字段排序来显示结果的需求。还是以我们前面举例用过的市民表为例，假设你要查询城市是“杭州”的所有人名字，并且按照姓名排序返回前1000个人的姓名、年龄。

假设这个表的部分定义是这样的：

```
CREATE TABLE `t` (
  `id` int(11) NOT NULL,
  `city` varchar(16) NOT NULL,
  `name` varchar(16) NOT NULL,
  `age` int(11) NOT NULL,
  `addr` varchar(128) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `city` (`city`)
) ENGINE=InnoDB;
```

这时，你的SQL语句可以这么写：

```
select city,name,age from t where city='杭州' order by name limit 1000  ;
```

这个语句看上去逻辑很清晰，但是你了解它的执行流程吗？今天，我就和你聊聊这个语句是怎么执行的，以及有什么参数会影响执行的行为。

# 全字段排序

前面我们介绍过索引，所以你现在就很清楚了，为避免全表扫描，我们需要在city字段加上索引。

在city字段上创建索引之后，我们用explain命令来看看这个语句的执行情况。

![](https://static001.geekbang.org/resource/image/82/03/826579b63225def812330ef6c344a303.png?wh=1470%2A126)

图1 使用explain命令查看语句的执行情况

Extra这个字段中的“Using filesort”表示的就是需要排序，MySQL会给每个线程分配一块内存用于排序，称为sort\_buffer。

为了说明这个SQL查询语句的执行过程，我们先来看一下city这个索引的示意图。

![](https://static001.geekbang.org/resource/image/53/3e/5334cca9118be14bde95ec94b02f0a3e.png?wh=1142%2A856)

图2 city字段的索引示意图

从图中可以看到，满足city='杭州’条件的行，是从ID\_X到ID\_(X+N)的这些记录。

通常情况下，这个语句执行流程如下所示 ：
<div><strong>精选留言（30）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/10/77/fd/c6619535.jpg" width="30px"><span>XD</span> 👍（159） 💬（7）<div>老师，基于早上知道的sort_buffer是在server层，我重新理解了下rowid排序的过程，
1，执行器查看表定义，发现name、city、age字段的长度之和超过max_length_for_sort_data，所以初始化sort_buffer的时候只放入id和name字段。
2，执行器调用存储引擎的读数据接口，依次获取满足条件的数据的id和name，存入sort_buffer。
3，排序。
4，执行器根据limit条件筛选出id，再次调用引擎读数据的接口获取相应的数据，返回客户端。
整个过程实际上是被执行器拆成了两次查询，共调用两次存储层的读数据接口，所以总的扫描行数需要相加。（@b-@a=5000）

但是对于using index condition的场景，执行器只调用了一次查询接口，回表是由存储层来完成的，所以扫描行数只算一次，即只算走索引搜索的过程中扫描的行数。（@b-@a只会是4000）

不知道这么理解对不对？</div>2019-02-27</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/PiajxSqBRaELZPnUAiajaR5C25EDLWeJURggyiaOP5GGPe2qlwpQcm5e3ybib8OsP4tvddFDLVRSNNGL5I3SFPJHsA/132" width="30px"><span>null</span> 👍（56） 💬（11）<div>re: 问题3:回答得也很好，需要注意的是255这个边界。小于255都需要一个字节记录长度，超过255就需要两个字节

11 月过数据库设计方案，总监现场抛了一个问题，就是关于 varchar 255 的。现在回看，木有人回答到点上，都说是历史原因。
下回再问，就可以分享这一点了。ꉂ ೭(˵¯̴͒ꇴ¯̴͒˵)౨”哇哈哈～</div>2018-12-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/f8/70/f3a33a14.jpg" width="30px"><span>某、人</span> 👍（211） 💬（20）<div>回答下@发条橙子同学的问题:
问题一：
1)无条件查询如果只有order by create_time,即便create_time上有索引,也不会使用到。
因为优化器认为走二级索引再去回表成本比全表扫描排序更高。
所以选择走全表扫描,然后根据老师讲的两种方式选择一种来排序
2)无条件查询但是是order by create_time limit m.如果m值较小,是可以走索引的.
因为优化器认为根据索引有序性去回表查数据,然后得到m条数据,就可以终止循环,那么成本比全表扫描小,则选择走二级索引。
即便没有二级索引,mysql针对order by limit也做了优化,采用堆排序。这部分老师明天会讲

问题二:
如果是group by a,a上不能使用索引的情况,是走rowid排序。
如果是group by limit,不能使用索引的情况,是走堆排序
如果是只有group by a,a上有索引的情况,又根据选取值不同,索引的扫描方式又有不同
select * from t group by a  --走的是索引全扫描,至于这里为什么选择走索引全扫描,还需要老师解惑下
select a from t group by a  --走的是索引松散扫描,也就说只需要扫描每组的第一行数据即可,不用扫描每一行的值

问题三:
bigint和int加数字都不影响能存储的值。
bigint(1)和bigint(19)都能存储2^64-1范围内的值,int是2^32-1。只是有些前端会根据括号里来截取显示而已。建议不加varchar()就必须带,因为varchar()括号里的数字代表能存多少字符。假设varchar(2),就只能存两个字符,不管是中文还是英文。目前来看varchar()这个值可以设得稍稍大点,因为内存是按照实际的大小来分配内存空间的,不是按照值来预分配的。

老师我有几个问题:
1.我还是想在确认之前问的问题。一个长连接,一条sql申请了sort_buffer_size等一系列的会话级别的内存,sql成功执行完,该连接变为sleep状态。这些内存只是内容会被情况,但是占用的内存空间不会释放?
2.假设要给a值加1,执行器先找引擎取a=1的行,然后执行器给a+1,在调用接口写入a+1了数据。那么加锁不应该是在执行器第一次去取数据时，引擎层就加该加的锁？为什么要等到第二次调用写入数据时,才加锁。第一次和第二次之间,难道不会被其他事务修改吗？如果没有锁保证
3.始终没太明白堆排序是采用的什么算法使得只需要对limit的数据进行排序就可以,而不是排序所有的数据在取前m条。--不过这里期待明天的文章</div>2018-12-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/eb/20/a02c4f61.jpg" width="30px"><span>didiren</span> 👍（64） 💬（7）<div>刚才又测了一下，在binlog-row-image=full的情况下，第二次update是不写redolog的，说明update并没有发生
这样我就理解了，当full时，mysql需要读到在更新时读到a值，所以会判断a值不变，不需要更新，与你给出的update t set a=3 where id=1 and a=3原理相同，但binlog-row-image会影响查询结果还是会让人吃一惊</div>2018-12-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/03/f7/3a493bec.jpg" width="30px"><span>老杨同志</span> 👍（90） 💬（7）<div>1)
mysql&gt; select * from t where city in (&#39;杭州&#39;,&quot; 苏州 &quot;) order by name limit 100;
需要排序
原因是索引顺序城市、名称 与 单独按name排序的顺序不一致。

2）如果不想mysql排序
方案a
可以执行两条语句
select * from t where city = &#39;杭州&#39;  limit 100;
select * from t where city = &#39;苏州&#39;  limit 100;
然后把200条记录在java中排序。
方案b
分别取前100，然后在数据端对200条数据进行排序。可以sort buffer就可以完成排序了。
少了一次应用程序与数据库的网络交互
select * from (
	select * from t where city = &#39;杭州&#39;  limit 100
	union all
  select * from t where city = &#39;苏州&#39;  limit 100
) as tt order by name limit 100


3）对分页的优化。
  没有特别好的办法。如果业务允许不提供排序功能，不提供查询最后一页，只能一页一页的翻，基本上前几页的数据已经满足客户需求。
  为了意义不大的功能优化，可能会得不偿失。
  如果一定要优化可以 select id from t where city in (&#39;杭州&#39;,&quot; 苏州 &quot;) order by name limit 10000,100
  因为有city\name索引，上面的语句走覆盖索引就可以完成，不用回表。
  最后使用 select * from t where id in (); 取得结果
  对于这个优化方法，我不好确定的是临界点，前几页直接查询就可以，最后几页使用这个优化方法。
  但是中间的页码应该怎么选择不太清楚
  </div>2018-12-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/f7/95/3ebafd36.jpg" width="30px"><span>波波</span> 👍（78） 💬（1）<div>笔记:
1.MySQL会为每个线程分配一个内存（sort_buffer）用于排序该内存大小为sort_buffer_size
  1&gt;如果排序的数据量小于sort_buffer_size，排序将会在内存中完成
  2&gt;如果排序数据量很大，内存中无法存下这么多数据，则会使用磁盘临时文件来辅助排序，也称外部排序
  3&gt;在使用外部排序时，MySQL会分成好几份单独的临时文件用来存放排序后的数据，然后在将这些文件合并成一个大文件


2.mysql会通过遍历索引将满足条件的数据读取到sort_buffer，并且按照排序字段进行快速排序
	1&gt;如果查询的字段不包含在辅助索引中，需要按照辅助索引记录的主键返回聚集索引取出所需字段
  	2&gt;该方式会造成随机IO，在MySQL5.6提供了MRR的机制，会将辅助索引匹配记录的主键取出来在内存中进行排序，然后在回表
 	3&gt;按照情况建立联合索引来避免排序所带来的性能损耗，允许的情况下也可以建立覆盖索引来避免回表

全字段排序
1.通过索引将所需的字段全部读取到sort_buffer中
2.按照排序字段进行排序
3.将结果集返回给客户端


缺点：
1.造成sort_buffer中存放不下很多数据，因为除了排序字段还存放其他字段，对sort_buffer的利用效率不高
2.当所需排序数据量很大时，会有很多的临时文件，排序性能也会很差

优点：MySQL认为内存足够大时会优先选择全字段排序，因为这种方式比rowid 排序避免了一次回表操作


rowid排序
1.通过控制排序的行数据的长度来让sort_buffer中尽可能多的存放数据，max_length_for_sort_data
2.只将需要排序的字段和主键读取到sort_buffer中，并按照排序字段进行排序
3.按照排序后的顺序，取id进行回表取出想要获取的数据
4.将结果集返回给客户端

优点：更好的利用内存的sort_buffer进行排序操作，尽量减少对磁盘的访问

缺点：回表的操作是随机IO，会造成大量的随机读，不一定就比全字段排序减少对磁盘的访问


3.按照排序的结果返回客户所取行数</div>2018-12-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/bd/da/3d76ea74.jpg" width="30px"><span>看不到de颜色</span> 👍（38） 💬（9）<div>关于上期问题里的最后一个例子不太明白，还请老师指点一下。按说在更新操作的时候应该是当前读，那么应该能读到id=1 and a = 3的记录并修改。那么为什么再select还会查到a = 2。难道是即便update但是where条件也是快照读？但是如果这样那么幻读的问题不就不会存在了吗？（B insert了一条记录，此时A范围update后再select会把B insert的语句查出来）</div>2019-02-02</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/17/d4/d7a4e6f5.jpg" width="30px"><span>胡楚坚</span> 👍（33） 💬（9）<div>不好意思，上个留言没打完。
问题一，在跟max_length_for_sort_data坐比较时，mysql是怎么判断一行数据的大小的？是直接根据表定义字段的大小吗？

问题二，另外这‘一行’的含义是整行数据，还是单单最终引擎层需要返回的字段(即select字段+where字段+order by字段)？

麻烦老师有空解答下，谢谢哈</div>2019-02-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/36/d2/c7357723.jpg" width="30px"><span>发条橙子 。</span> 👍（27） 💬（3）<div>老师 ， 接前面 create_time的回答 。 语句确实是 select * from t order by create_time desc ;

老师是指 优化器会根据 order by create_time 来选择使用 create_time 索引么 

我之前误以为优化器是根据 where 后面的字段条件来选择索引 ，所以上面那条语句没有where 的时候我就想当然地以为不会走索引 。 看来是自己跳进了一个大坑里面 😅

另 ： 我之前在本地建了张表加了20w数据 ，用explain 查了一次 ，发现走的是全表没有走索引， 老师说会走索引。我想了一下， 可能是统计的数据有误的缘故，用 analyze table重新统计 ，再次查询果然走了索引  。😁</div>2018-12-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/eb/20/a02c4f61.jpg" width="30px"><span>didiren</span> 👍（24） 💬（1）<div>感谢！针对我之前提出的疑问，我又详细的做了实验，发现一个新的问题，我感觉是个bug，希望解答
# SessionA
mysql&gt; show variables like &#39;%binlog_row_image%&#39;;
| Variable_name    | Value |
| binlog_row_image | FULL  |
mysql&gt; create table t (id int not null primary key auto_increment,
    -&gt; a int default null)
    -&gt; engine=innodb;
mysql&gt; insert into t values(1,2);
mysql&gt; set tx_isolation = &#39;repeatable-read&#39;;
mysql&gt; begin;
mysql&gt; select * from t where id = 1;
| id | a    |
|  1 |    2 |
此时在另一个SessionB执行update t set a=3 where id = 1;成功更新一条记录。通过show engine innodb status看，Log sequence number 2573458
然后在SessionA继续。。
mysql&gt; update t set a=3 where id = 1;
Rows matched: 1  Changed: 0  Warnings: 0
Log sequence number 2573467
mysql&gt; select * from t where id = 1;
| id | a    |
|  1 |    2 |

这里与你给出的答案里的实验结果不同
可以看到redolog是记录了第二次的update的，但是select却没有看到更新后的值，于是我又换了一个平时测试用的实例，同样的步骤却得到了与你的答案相同的结果
然后我对比了2个实例的参数，发现当binlog-row-image=minimal时第二次查询结果a=3，当binlog-row-image=full时第二次查询结果a=2，而且不论哪个参数，redolog都会因为SessionA的update增长，说明redolog都做了记录，update是发生了的，但是binlog-row-image参数会影响查询结果，难以理解，我用的mysql版本是官方的5.7.13

下面是binlog-row-image = minimal的实验结果
mysql&gt; set  binlog_row_image=MINIMAL;
mysql&gt; drop table t;
mysql&gt; create table t (id int not null primary key auto_increment,
    -&gt; a int default null)
    -&gt; engine=innodb;
insert into t values(1,2);
mysql&gt; insert into t values(1,2);
mysql&gt; set tx_isolation = &#39;repeatable-read&#39;;
mysql&gt; begin;
mysql&gt; select * from t where id = 1;
| id | a    |
|  1 |    2 |
此时在另一个SessionB执行update t set a=3 where id = 1;成功更新一条记录。
mysql&gt; update t set a=3 where id = 1;
Rows matched: 1  Changed: 0  Warnings: 0
mysql&gt; select * from t where id = 1; 
| id | a    |
|  1 |    3 |</div>2018-12-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/36/d2/c7357723.jpg" width="30px"><span>发条橙子 。</span> 👍（12） 💬（2）<div>
正好有个 order by 使用场景 ， 有个页面，需要按数据插入时间倒序来查看一张记录表的信息 ，因为除了分页的参数 ， 没有其他 where 的条件 ，所以除了主键外没有其他索引 。 

这时候 DBA 让我给 create_time 创建索引， 说是按照顺序排列 ，查询会增快 。这篇文章看完后 ， 让我感觉实际上创建 create_time 索引是没用的 。 

因为查询本身并没有用到 create_time 索引 ，实际上查询的步骤是 ：

1. 初始化 sort_buffer 内存

2. 因为没索引 ， 所以扫出全表的数据到 sort_buffer 中

2. 如果内存够则直接内存按时间排序 

3. 如果内存不够则按数据量分成不同文件分别按时间排序后整合

4. 根据数量分页查询数量 回聚集索引中用 ID 查询数据

5. 返回

所以我分析create_time索引应该不需要创建。反而增加了维护成本


问题一 ：这种无条件查列表页除了全表扫还有其他建立索引的办法么

问题二 : 如果加入 group by ， 数据该如何走

问题三 ：老师之后的文章会有讲解 bigInt(20)  、 tinyint(2) 、varchar(32) 这种后面带数字与不带数字有何区别的文章么 。 每次建字段都会考虑长度 ，但实际却不知道他有何作用 


</div>2018-12-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/57/da/0adccef5.jpg" width="30px"><span>coderbee</span> 👍（11） 💬（1）<div>请教下林老师：
以文章中的 t 表，索引 city(city) 其实等价于 city(city, id) ，第2条语句加了 order by id，Extra 列多了 Using where ，为啥还要这个？？两个都是用到了覆盖索引。

mysql&gt; explain select id from t where city = &#39;city102&#39; limit 1, 10;
+----+-------------+-------+------------+------+---------------+------+---------+-------+------+----------+-------------+
| id | select_type | table | partitions | type | possible_keys | key  | key_len | ref   | rows | filtered | Extra       |
+----+-------------+-------+------------+------+---------------+------+---------+-------+------+----------+-------------+
|  1 | SIMPLE      | t     | NULL       | ref  | city          | city | 66      | const |    2 |   100.00 | Using index |
+----+-------------+-------+------------+------+---------------+------+---------+-------+------+----------+-------------+
1 row in set, 1 warning (0.00 sec)

mysql&gt; explain select id from t where city = &#39;city102&#39; order by id limit 1, 10;
+----+-------------+-------+------------+------+---------------+------+---------+-------+------+----------+--------------------------+
| id | select_type | table | partitions | type | possible_keys | key  | key_len | ref   | rows | filtered | Extra                    |
+----+-------------+-------+------------+------+---------------+------+---------+-------+------+----------+--------------------------+
|  1 | SIMPLE      | t     | NULL       | ref  | city          | city | 66      | const |    2 |   100.00 | Using where; Using index |
+----+-------------+-------+------------+------+---------------+------+---------+-------+------+----------+--------------------------+
1 row in set, 1 warning (0.00 sec)

</div>2019-01-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/bd/da/3d76ea74.jpg" width="30px"><span>看不到de颜色</span> 👍（9） 💬（2）<div>图14那个疑问明白了，是因为where条件中存在update的值InnoDB认为值一致所以没有修改，从而导致A的一致性视图中看不到B的修改。
这篇又看了一遍，还有个疑问，想请老师解答一下。
1.asc和desc会影响使用索引排序吗？
2.如果采用rowid也无法放入排序字段还是会转用磁盘排序吧。</div>2019-02-06</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/JKKWS6TzhncvAA0p0NDiaATPIvMicSM76vNAg9IG1ibibcJYPAiaicYjZfq4gAV8GRtcTpOibfRD8vzqHBtL0ibmhwQsbg/132" width="30px"><span>唐名之</span> 👍（6） 💬（3）<div>1：用@cyberbit 提供的方式，执行计划是不会使用到排序，但执行时间比使用排序消耗的多；
2：分页limit过大时会导致大量排序，可以记录上一页最后的ID，下一页查询条件带上 where  ID&gt;上一页最后ID limit 100</div>2019-01-09</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/RNO4yZyBvic914hewmNNE8iblYDcfv5yGHZ9OnKuCuZXNmGR0F5qV3icKLT2xpMt66GyEpicZVvrmz8A6TIqt92MQg/132" width="30px"><span>啊啊啊哦哦</span> 👍（5） 💬（2）<div>假设超过sort buffer  排序是一部分在内存中排序 超出的部分 用临时文件吗。</div>2019-03-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/1d/13/31ea1b0b.jpg" width="30px"><span>峰</span> 👍（4） 💬（1）<div>由于city有两个值，相当于匹配到了索引树的两段区域，虽然各自都是按name排序，但整体需要做一次归并，当然只是limit100，所以够数就行。再然后如果需要不做排序，业务端就按city不同的取值查询两次，每次都limit100，然后业务端做归并处理喽。再然后要做分页的话，好吧，我的思路是先整出一张临时的结果表，create table as select rownumber,* from t where city=x order by name(写的不对哈，只是表达意思，rownumber为行数,并为主键)然后直接从这张表中按rownumber进行分页查询就好。</div>2018-12-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/75/d9/24786b20.jpg" width="30px"><span>小岭哥</span> 👍（3） 💬（1）<div>为什么建立组合索引之后会天然的按照name递增排序呢</div>2018-12-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/4f/fb/3eb917f1.jpg" width="30px"><span>爱学习的好孩子</span> 👍（3） 💬（1）<div>老师你好，全字段排序那一节，我做了实验，我的排序缓存大小是1M， examined rows 是7715892，查询的三个字段都有数据，那么如果这些数据都放到缓存应该需要（4+8+11）*7715892等于160M，但是我看了都没有用到临时表，这是为什么？

CREATE TABLE `phone_call_logs` (
  `id` int(11) unsigned NOT NULL AUTO_INCREMENT COMMENT &#39;主键ID&#39;,
  `city_id` int(11) NOT NULL DEFAULT &#39;11&#39;,
  `call_sender` varchar(40) DEFAULT NULL COMMENT &#39;电话主叫号码&#39;,
  `phone_id` bigint(20) NOT NULL DEFAULT &#39;0&#39; COMMENT &#39;手机id&#39;,
  PRIMARY KEY (`id`),
  KEY `idx_city` (`city_id`)
) ENGINE=InnoDB AUTO_INCREMENT=64551193;
----------------sort_buffer_size=1M----------------------------
root:(none)&gt; show variables like &#39;sort_buffer_size&#39;;
+------------------+---------+
| Variable_name    | Value   |
+------------------+---------+
| sort_buffer_size | 1048576 |
+------------------+---------+
1 row in set (0.00 sec)
---------------查询sql---------------------
 select city_id,phone_id,call_sender from phone_call_logs where city_id=11 order by phone_id desc limit 1000;


-----------------------执行计划结果---------------------------------------------

  &quot;filesort_priority_queue_optimization&quot;: {
              &quot;limit&quot;: 1000,
              &quot;rows_estimate&quot;: 146364461,
              &quot;row_size&quot;: 146,
              &quot;memory_available&quot;: 1048576,
              &quot;chosen&quot;: true
            },
            &quot;filesort_execution&quot;: [
            ],
            &quot;filesort_summary&quot;: {
              &quot;rows&quot;: 1001,
              &quot;examined_rows&quot;: 7715892,
              &quot;number_of_tmp_files&quot;: 0,
              &quot;sort_buffer_size&quot;: 154160,
              &quot;sort_mode&quot;: &quot;&lt;sort_key, additional_fields&gt;&quot;
</div>2018-12-19</li><br/><li><img src="" width="30px"><span>yy</span> 👍（3） 💬（2）<div>老师我想问一下  mysql在做没有排序的查询语句的时候  每次扫描返回的结果集顺序一样吗？还是每次扫描的结果集顺序是变化的？</div>2018-12-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/d8/c6/2b2a58cf.jpg" width="30px"><span>搞怪者😘 😒 😏 👿</span> 👍（2） 💬（1）<div>老师，我发现刚刚问的问题是因为我将join写成了left join，但是为什么加了一个left就会有这么大变化呢？</div>2019-04-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/ec/1b/650e3dbe.jpg" width="30px"><span>zws</span> 👍（2） 💬（1）<div>看到redolog  和 binlog 的内容就相当头疼。。  这一章讲的排序写的非常好，看到结尾关于上一节的提问回答我又陷入的沉思。。。我不是dba这些内容有这么重要吗</div>2019-04-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/cb/50/66d0bd7f.jpg" width="30px"><span>杰之7</span> 👍（2） 💬（1）<div>通过这一节的阅读学习，知道了一个有Order by语言的排序逻辑和排序对内存的消耗。

老师介绍了4种情况，区分了全字段排序和Rowid排序的区别，如果有足够的内存，用全字段排序，否则用Rowid排序，这样排序的效率会更好。

在上述两种排序的基础之上，讲述了联合索引，联合索引解决了不需要按照姓名进行排序，这样只需要扫描1000次。进一步是覆盖索引，连回到主键取索引都不需要了。

通过这一节的学习，知道了一条有Order by 语句的执行流程和对系统资源的影响，谢谢老师哈。</div>2019-01-16</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/17/6a/c979163e.jpg" width="30px"><span>古娜拉黑暗之神·巴啦啦能量·堕落达</span> 👍（2） 💬（1）<div>堕落天使
老师，您好。
请问：建立了city、name、age的联合索引之后，执行 “select city,name,age from t where city=&#39;杭州&#39; order by name limit 1000 ;” 语句，显示的rows（影响行数）依旧是4000呢？不应该是1000吗？
2018-12-20
 作者回复
Explain 发来看看
我：
命令如下：
mysql&gt; select count(*) from p where city = &#39;杭州&#39;;
+----------+
| count(*) |
+----------+
|     4000 |
+----------+
1 row in set (0.00 sec)

mysql&gt; explain select city,name,age from p where city=&#39;杭州&#39; order by name limit 1000;
+----+-------------+-------+------------+------+---------------+---------------+---------+-------+------+----------+--------------------------+
| id | select_type | table | partitions | type | possible_keys | key           | key_len | ref   | rows | filtered | Extra                    |
+----+-------------+-------+------------+------+---------------+---------------+---------+-------+------+----------+--------------------------+
|  1 | SIMPLE      | p     | NULL       | ref  | city_name_age | city_name_age | 66      | const | 4000 |   100.00 | Using where; Using index |
+----+-------------+-------+------------+------+---------------+---------------+---------+-------+------+----------+--------------------------+
1 row in set, 1 warning (0.00 sec)
由explain的结果可见：使用的索引是city_name_age，扫描的行数（rows）是4000。而且您文章中的 图9 和 图11 中的rows值也是4000。这是为什么呢？
</div>2018-12-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/00/f0/08409e78.jpg" width="30px"><span>一大只😴</span> 👍（2） 💬（1）<div>课后思考题：还要使用排序。在虚拟机上测试了，没加order by name时候，city in 两个值时就没有走索引，所以还是要排序，city in 俩值相当于or了</div>2018-12-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/e1/e7/d1b2e914.jpg" width="30px"><span>明亮</span> 👍（2） 💬（1）<div>需要排序，可以将原来的索引中name字段放前面，city字段放后面，来建索引就可以了</div>2018-12-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/07/1e/bdbe93f4.jpg" width="30px"><span>尘封</span> 👍（2） 💬（1）<div>请问，第7步中遍历排序结果，取前 1000 行，并按照 id 的值回到原表中取出 city、name 和 age 三个字段返回给客户端：这里会把id再进行排序吗？转随机io为顺序io？</div>2018-12-19</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTJAibnPX9jW8kqLcIfibjic8GbkQkEUYyFKJkc39hZhibVlNrqwTjdLozkqibI2IwACd5YzofYickNxFnZg/132" width="30px"><span>Sinyo</span> 👍（1） 💬（1）<div>老师，如果row_id算法的大小也超出了sort_buffer_size，那么也会用到磁盘临时文件辅助么？</div>2019-02-13</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTLv9HJIW4OACkjlwOQJ9cU7HzvaDFYkACWCib2lzOMef9ZiaGDTVFqjPicpVK5KDRbBRVGGHrMHQO1Rw/132" width="30px"><span>fdconan</span> 👍（1） 💬（1）<div>老师，请教下，如果希望通过city找出记录后，按照name倒序(order by name desc)而又不想mysql进行排序(执行计划没有filesort关键字)，应该如何设计索引呢？有什么好的建议么？</div>2019-01-15</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/36/ec/ca162d6b.jpg" width="30px"><span>sam3125C</span> 👍（1） 💬（1）<div>类如图二的索引图，我一直有一个困惑。city的索引图上，有小一些的长方形和大一些的长方形。有时候箭头源自于小长方形，有些箭头又源自于大长方形。这究竟是什么含义？</div>2019-01-12</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTJAibnPX9jW8kqLcIfibjic8GbkQkEUYyFKJkc39hZhibVlNrqwTjdLozkqibI2IwACd5YzofYickNxFnZg/132" width="30px"><span>Sinyo</span> 👍（1） 💬（1）<div>老师，图 13 可见性验证方式，第二个select不应该是“当前读”么？更新数据不是先读后写么？</div>2018-12-21</li><br/>
</ul>