在上一篇文章中，我和你介绍了join语句的两种算法，分别是Index Nested-Loop Join(NLJ)和Block Nested-Loop Join(BNL)。

我们发现在使用NLJ算法的时候，其实效果还是不错的，比通过应用层拆分成多个语句然后再拼接查询结果更方便，而且性能也不会差。

但是，BNL算法在大表join的时候性能就差多了，比较次数等于两个表参与join的行数的乘积，很消耗CPU资源。

当然了，这两个算法都还有继续优化的空间，我们今天就来聊聊这个话题。

为了便于分析，我还是创建两个表t1、t2来和你展开今天的问题。

```
create table t1(id int primary key, a int, b int, index(a));
create table t2 like t1;
drop procedure idata;
delimiter ;;
create procedure idata()
begin
  declare i int;
  set i=1;
  while(i<=1000)do
    insert into t1 values(i, 1001-i, i);
    set i=i+1;
  end while;
  
  set i=1;
  while(i<=1000000)do
    insert into t2 values(i, i, i);
    set i=i+1;
  end while;

end;;
delimiter ;
call idata();
```

为了便于后面量化说明，我在表t1里，插入了1000行数据，每一行的a=1001-id的值。也就是说，表t1中字段a是逆序的。同时，我在表t2中插入了100万行数据。

# Multi-Range Read优化

在介绍join语句的优化方案之前，我需要先和你介绍一个知识点，即：Multi-Range Read优化(MRR)。这个优化的主要目的是尽量使用顺序读盘。

在[第4篇文章](https://time.geekbang.org/column/article/69236)中，我和你介绍InnoDB的索引结构时，提到了“回表”的概念。我们先来回顾一下这个概念。回表是指，InnoDB在普通索引a上查到主键id的值后，再根据一个个主键id的值到主键索引上去查整行数据的过程。
<div><strong>精选留言（30）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/13/03/f7/3a493bec.jpg" width="30px"><span>老杨同志</span> 👍（64） 💬（5）<div>我准备给
t1增加索引c
t2增加组合索引b,c
t3增加组合索引b,c
select * from t1 straight_join t2 on(t1.a=t2.a)  straight_join  t3 on (t2.b=t3.b) where t1.c&gt;=X and t2.c&gt;=Y and t3.c&gt;=Z;

另外我还有个问题，开篇提到的这句sql select * from t1 where a&gt;=1 and a&lt;=100;
a是索引列，如果这句索引有order by a，不使用MRR 优化，查询出来就是按a排序的，使用了mrr优化，是不是要额外排序

</div>2019-02-01</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/b8/36/542c96bf.jpg" width="30px"><span>Mr.Strive.Z.H.L</span> 👍（53） 💬（1）<div>老师您好，新年快乐~~

关于三表join有一个疑惑点需要确认：

老师您在评论中说到，三表join不会是前两个表join后得到结果集，再和第三张表join。
针对这句话，我的理解是：
假设我们不考虑BKA，就按照一行行数据来判断的话，流程应该如下（我会将server端和innodb端分的很清楚）：
表是t1 ,t2 ,t3。  t1 straight_join t2 straight_join t3，这样的join顺序。
1. 调用innodb接口，从t1中取一行数据，数据返回到server端。
2. 调用innodb接口，从t2中取满足条件的数据，数据返回到server端。
3. 调用innodb接口，从t3中取满足条件的数据，数据返回到server端。
上面三步之后，驱动表 t1的一条数据就处理完了，接下来重复上述过程。
（如果采用BKA进行优化，可以理解为不是一行行数据的提取，而是一个范围内数据的提取）。

按照我上面的描述，确实没有前两表先join得结果集，然后再join第三张表的过程。
不知道我上面的描述的流程对不对？（我个人觉得，将innodb的处理和server端的处理分隔清晰，对于sql语句的理解，会透彻很多）</div>2019-02-02</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/e9/29/629d9bb0.jpg" width="30px"><span>天王</span> 👍（34） 💬（4）<div>join语句的优化，NLJ算法的优化，MRR优化器会在join_buffer进行主键的排序，然后去主键索引树上一个个的查找，因为按照主键顺序去主键索引树上查找，性能会比较高，MRR优化接近顺序读，性能会比较高。BKA算法是对NLJ算法的优化，一次取出一批数据的字段到join_buffer中，然后批量join，性能会比较好。BKA算法依赖于MRR，因为批量join找到被驱动表的非聚集索引字段通过MRR去查找行数据</div>2019-02-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/d1/7c/4639f22c.jpg" width="30px"><span>郭健</span> 👍（33） 💬（3）<div>老师，有几个问题还需要请教一下:
1.上一章t1表100条数据，t21000条数据，mysql会每次都会准确的找出哪张表是合理的驱动表吗？还是需要人为的添加straight_join。
2.像left join这种，左边一定是驱动表吧？以左边为标准查看右边有符合的条件，拼成一条数据，看到你给其他同学的评论说可能不是，这有些疑惑。
3.在做join的时候，有些条件是可以放在on中也可以放在where中，比如(t1.yn=1 和t2.yn=1)这种简单判断是否删除的。最主要的是，需要根据两个条件才能join的(productCode和custCode),需要两个都在on里，还是一个在on中，一个在where中更好呢？</div>2019-02-07</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/ed/1a/269eb3d6.jpg" width="30px"><span>cfanbo</span> 👍（26） 💬（9）<div>最近遇到这个需求，in里面的值个数有5万左右，出现的情况很少但存在，这种情况怎么处理。？手动创建临时表再join？

另外in内的值用不用手动排序？</div>2019-02-01</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/11/18/8cee35f9.jpg" width="30px"><span>HuaMax</span> 👍（20） 💬（2）<div>前提假设：t1.c&gt;=X可以让t1成为小表。同时打开BKA和MRR。
1、t1表加（c,a)索引。理由：A、t1.c&gt;=X可以使用索引；B、加上a的联合索引，join buffer里放入的是索引（c,a）而不是去主键表取整行，用于与表t2的t1.a = t2.a的join查询，不过返回SELECT * 最终还是需要回表。
2、t2表加(a,b,c)索引。理由：A、加上a避免与t1表join查询的BNL；B、理由同【1-B】；C、加上c不用回表判断t2.c&gt;=Y的筛选条件
3、t3表加（b,c）索引。理由：A、避免与t2表join查询的BNL;C、理由同【2-C】

问题：
1、【1-B】和【2-B】由于select *要返回所有列数据，不敢肯定join buffer里是回表的整行数据还是索引（c,a)的数据，需要老师解答一下；不过值得警惕的是，返回的数据列对sql的执行策略有非常大的影响。
2、在有join查询时，被驱动表是先做join连接查询，还是先筛选数据再从筛选后的临时表做join连接？这将影响上述的理由【2-C】和【3-C】

使用straight_join强制指定驱动表，我会改写成这样:select * from t2 STRAIGHT_JOIN t1 on(t1.a=t2.a) STRAIGHT_JOIN t3 on (t2.b=t3.b)  where t1.c&gt;=X and t2.c&gt;=Y and t3.c&gt;=Z;
考虑因素包括：
1、驱动表使用过滤条件筛选后的数据量，使其成为小表，上面的改写也是基于t2是小表
2、因为t2是跟t1,t3都有关联查询的，这样的话我猜测对t1,t3的查询是不是可以并行执行，而如果使用t1,t3作为主表的话，是否会先跟t2生成中间表，是个串行的过程？
3、需要给t1加（a,c)索引，给t2加（c,a,b）索引。</div>2019-02-02</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/e9/0b/1171ac71.jpg" width="30px"><span>WL</span> 👍（18） 💬（2）<div>请教老师两个问题:
1. 通过主键索引找到的数据会会不会先在内存中查询, 如果没有再去磁盘查询?
2. 为什么在通过主键索引查询数据时, 符合条件的数据以单条数据的方式读到内存中而不是以一整个数据页的方式读到内存中? </div>2019-02-11</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/DYAIOgq83eqJobg767PUeqrqQQ4B6YvMatj2SRyOicKZZ4gWTf30dMketiaj58Gc3RFTmckGxAXlL9ERSxGovq9g/132" width="30px"><span>涛哥哥</span> 👍（15） 💬（1）<div>老师，对于现在的固态硬盘，这样类似顺序读写的数据库优化，不就不起作用了啊？</div>2019-03-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/62/a5/43aa0c27.jpg" width="30px"><span>TKbook</span> 👍（12） 💬（1）<div>BNL 算法效率低，建议你都尽量转成 BKA 算法。优化的方向就是给驱动表的关联字段加上索引；
老师最后总结的时候，这句话后面那句，应该是给被驱动表的关联字段加上索引吧。</div>2019-02-01</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/18/07/9f5f5dd3.jpg" width="30px"><span>憶海拾貝</span> 👍（11） 💬（8）<div>节后开工宜补课.

按照文中说明的MRR设计思路, 是否可以反推出: 被驱动表使用非递增主键(比如UUID作为主键),就没有必要开启MRR?</div>2019-02-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/dd/ac/f40bbd15.jpg" width="30px"><span>dzkk</span> 👍（11） 💬（1）<div>老师，记得我之前看mysql的join是和版本有关系的，另外NLJ是一个统称，被分为了SNLJ(Simple Nested-Loop Join，5.5版本之前采用的，当被驱动表上没有索引的时候使用，该方法比较粗暴，所以后来通过BNLJ进行了优化)、INLJ(Index Nested-Loop Join，被驱动表上有索引)、BNLJ(Block Nested-Loop Join，被驱动表上没有索引)，另外了解到mariadb是支持了hash join的Block Nested Loop Hash (BNLH) join，没有使用过，不知道效果怎么样。不知道我了解的信息对不对。</div>2019-02-01</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/0c/48/ba59d28d.jpg" width="30px"><span>poppy</span> 👍（9） 💬（2）<div>select * from t1 join t2 on(t1.a=t2.a) join t3 on (t2.b=t3.b) where t1.c&gt;=X and t2.c&gt;=Y and t3.c&gt;=Z;
老师，我的理解是真正做join的三张表的大小实际上是t1.c&gt;=X、t2.c&gt;=Y、t3.c&gt;=Z对应满足条件的行数，为了方便快速定位到满足条件的数据，t1、t2和t3的c字段最好都建索引。对于join操作，按道理mysql应该会优先选择join之后数量比较少的两张表先来进行join操作，例如满足t1.a=t2.a的行数小于满足t2.b=t3.b的行数，那么就会优先将t1和t2进行join，选择t1.c&gt;=X、t2.c&gt;=Y中行数少的表作为驱动表，另外一张作为被驱动表，在被驱动表的a的字段上建立索引，这样就完成了t1和t2的join操作并把结果放入join_buffer准备与t3进行join操作，则在作为被驱动表的t3的b字段上建立索引。不知道举的这个例子分析得是否正确，主要是这里不知道t1、t2、t3三张表的数据量，以及满足t1.c&gt;=X ，t2.c&gt;=Y ，t3.c&gt;=Z的数据量，还有各个字段的区分度如何，是否适合建立索引等。</div>2019-02-01</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/ee/23/b92b0811.jpg" width="30px"><span>读书看报</span> 👍（8） 💬（2）<div>order by cjsj desc limit 0,20 explain  Extra只是显示 Using where ，执行时间 7秒钟
order by cjsj desc limit 5000,20 explain  Extra只是显示 Using index condition; Using where; Using filesort,  执行时间 0.1 秒
有些许的凌乱了@^^@</div>2019-02-01</li><br/><li><img src="" width="30px"><span>bluefantasy3</span> 👍（7） 💬（4）<div>请教老师一个问题：innodb的Buffer Pool的内存是innodb自己管理还是使用OS的page cache? 我理解应该是innodb自己管理。我在另一个课程里看到如果频繁地把OS的&#47;proc&#47;sys&#47;vm&#47;drop_caches 改成 1会影响MySQL的性能，如果buffer pool是MySQL自己管理，应该不受这个参数影响呀？请解答。</div>2019-02-02</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/DYAIOgq83eqibSwKPg7hiapc49qoM4dibhM3fYANPjfltF2ibBZ3dHX2hibjg5EIIcziahrmjO5R2XrcRibvU39TQS7jg/132" width="30px"><span>库淘淘</span> 👍（6） 💬（1）<div>set optimizer_switch=&#39;mrr=on,mrr_cost_based=off,batched_key_access=on&#39;;
create index idx_c on t2(c);
create index idx_a_c on t1(a,c);
create index idx_b_c on t3(b,c);
mysql&gt; explain select * from t2 
    -&gt; straight_join t1 on(t1.a=t2.a)
    -&gt; straight_join t3 on(t2.b=t3.b)   
    -&gt; where t1.c&gt; 800 and t2.c&gt;=600 and t3.c&gt;=500;
+----+-------------+-------+------------+---------------------------------------
| id | select_type | table | partitions | type | possible_keys | key | key_len | ref | rows | filtered | Extra +----------------------------------------
| 1 | SIMPLE | t2 | NULL | range | idx_c | idx_c | 5 | NULL | 401 | 100.00 | Using index condition; Using where; Using MRR |
| 1 | SIMPLE | t1 | NULL | ref | idx_a_c | idx_a_c | 5 | test.t2.a | 1 | 33.33 | Using index condition; Using join buffer (Batched Key Access) |
| 1 | SIMPLE | t3 | NULL | ref | idx_b_c | idx_b_c | 5 | test.t2.b | 1 | 33.33 | Using index condition; Using join buffer (Batched Key Access) |
+----+-------------+-------+------------+-----+---------------------------------------
3 rows in set, 1 warning (0.00 sec)
以自己理解如下，有问题请老师能够指出
1.根据查询因是select * 肯定回表的，其中在表t2创建索引idx_c,为了能够使用ICP,MRR，如果c字段重复率高或取值行数多，可以考虑不建索引
2.已t2 作为驱动表，一方面考虑其他两表都有关联,t2表放入join buffer后关联t1后，再关联t2 得出结果 再各回t2,t3表取出 得到结果集（之前理解都是t1和t2join得结果集再与t3join，本次理解太确定）
3.t2、t3表建立联合查询目的能够使用ICP</div>2019-02-01</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/e0/d5/7485e51f.jpg" width="30px"><span>~玲玲玲~子~哥~</span> 👍（5） 💬（1）<div>老师好。
这节课评论我看好多人都问三表连接时的步骤，您指出和第三个表关联不是前两个表的结果集和第三张表关联。
那是第一张表和第二张表关联，然后第一张表在和第三张表关联，最后这两个结果集在关联？请纠正。</div>2019-03-31</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/b8/36/542c96bf.jpg" width="30px"><span>Mr.Strive.Z.H.L</span> 👍（5） 💬（2）<div>老师你好，今天在回顾这篇文章做总结的时候，突然有一个疑惑：

我们假设t2的b上面有索引，该语句是左连接

select * from t1  left join t2 on (t1.b=t2.b) where t2.b&gt;=1 and t2.b&lt;=2000;

和

select * from t1  left join t2 on (t1.b=t2.b) and t2.b&gt;=1 and t2.b&lt;=2000;

到底在内部执行流程上到底有什么区别？？
因为实际工作中左连接用得挺多的。
（这篇文章都是直连，所以使用on和where最后的结果都一样，但是左连接就不是了）
</div>2019-02-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/ee/23/b92b0811.jpg" width="30px"><span>读书看报</span> 👍（5） 💬（2）<div>刚刚凌乱了的那个问题，经explain验证，explain SELECT a.* FROM sys_xxtx a JOIN baq_ryxx r ON a.ryid = r.ID WHERE a.dwbh = &#39;7E0A13A14101D0A8E0430A0F23BCD0A8&#39; ORDER BY txsj DESC LIMIT 0,20;
使用的索引是txsj ；
explain SELECT a.* FROM sys_xxtx a JOIN baq_ryxx r ON a.ryid = r.ID WHERE a.dwbh = &#39;7E0A13A14101D0A8E0430A0F23BCD0A8&#39; ORDER BY txsj DESC LIMIT 5000,20;使用的索引是dwbh ；
然后回忆起了第10张：MySQL为什么有时候会选错索引？
但是从扫描行数、是否使用排序等来看在 LIMIT 5000,20时候也应该优选txsj ?可是这个时候选择的索引是dwbh, 查询时间也大大缩短</div>2019-02-01</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/0c/ca/6173350b.jpg" width="30px"><span>神奇小懒懒</span> 👍（5） 💬（2）<div>select * from t1 join t2 on(t1.a=t2.a) join t3 on (t2.b=t3.b) where t1.c&gt;=X and t2.c&gt;=Y and t3.c&gt;=Z;
这个语句建索引需要考虑三个表的数据量和相关字段的数据分布、选择率、每个条件返回行数占比等
我的测试场景是：
t1 1000行数据  t2 100w行数据  t3 100w行，关联字段没有重复值，条件查询返回行数占比很少，此时索引为： 
alter table t1 add key t1_c(c);
alter table t2 add key t2_ac(a,c);
alter table t3 add key t3_bc(b,c);
测试sql无索引是执行需要2分钟多，加了索引后需要0.01秒，加索引后执行计划为：
mysql&gt; explain select * from t1 join t2 on(t1.a=t2.a) join t3 on (t2.b=t3.b) where t1.c&gt;=100 and t2.c&gt;=10 and t3.c&gt;=90;
+----+-------------+-------+------------+------+---------------+-------+---------+---------------+------+----------+------------------------------------+
| id | select_type | table | partitions | type | possible_keys | key   | key_len | ref           | rows | filtered | Extra                              |
+----+-------------+-------+------------+------+---------------+-------+---------+---------------+------+----------+------------------------------------+
|  1 | SIMPLE      | t1    | NULL       | ALL  | t1_a          | NULL  | NULL    | NULL          | 1000 |    90.10 | Using where                        |
|  1 | SIMPLE      | t2    | NULL       | ref  | t2_ac         | t2_ac | 5       | sysbench.t1.a |    1 |    33.33 | Using index condition; Using where |
|  1 | SIMPLE      | t3    | NULL       | ref  | t3_bc         | t3_bc | 5       | sysbench.t2.b |    1 |    33.33 | Using index condition              |
+----+-------------+-------+------------+------+---------------+-------+---------+---------------+------+----------+------------------------------------+
另外，select * 如果改成具体字段的话考虑覆盖索引 可能需要建立不同的索引。
</div>2019-02-01</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/e9/29/629d9bb0.jpg" width="30px"><span>天王</span> 👍（3） 💬（1）<div>BNL算法优化，BNL算法，如果读取的是冷表，而且量比较大，循环读取，第一次数据会进入old区域，如果一秒之后没有访问，不会移到LRU头部，大表join对io影响查询完就结束了，但是buffer pool需要大量的查询把冷数据冲掉。BNL算法有3个问题，1 多次扫描被驱动表，占用磁盘io 2 判断join会耗费大量的cpu资源 3 会热数据淘汰，影响buffer pool的命中率</div>2019-02-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/40/5e/b8fada94.jpg" width="30px"><span>Ryoma</span> 👍（3） 💬（1）<div>read_rnd_buffer_length 参数应该是 read_rnd_buffer_size，见文档：https:&#47;&#47;dev.mysql.com&#47;doc&#47;refman&#47;8.0&#47;en&#47;server-system-variables.html#sysvar_read_rnd_buffer_size</div>2019-02-02</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/e5/39/951f89c8.jpg" width="30px"><span>信信</span> 👍（3） 💬（1）<div>老师好，有两点疑问请老师解惑：
1、图8上面提到的关于临时表的第三句是不是还是使用straight_join好一些？不然有可能temp_t被选为驱动表？
2、图8下面提到join过程中做了1000次带索引的查询，这里的1000也是在打开mrr的情况下的吗？是进行了1000次树搜索，还是找到第一个后，依次挨着读呢？
</div>2019-02-02</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/b2/5a/574f5bb0.jpg" width="30px"><span>Lukia</span> 👍（2） 💬（1）<div>老师好，针对BKA的描述：
“之后的 join 语句，扫描表 t1，这里的扫描行数是 1000；join 比较过程中，做了 1000 次带索引的查询。”
是不是可以理解为被扫描表的索引其实还是一个一个查的，只是在通过被扫描表的索引去访问主键索引的时候用了mrr？</div>2019-02-20</li><br/><li><img src="" width="30px"><span>Geek_02538c</span> 👍（2） 💬（1）<div>过年了，还有新文章，给个赞。 另，where  和 order  与索引的关系，都讲过了，group by 是否也搞个篇章说一下。</div>2019-02-02</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/48/8a/a20396e9.jpg" width="30px"><span>live fast</span> 👍（1） 💬（2）<div>老师，PHP 的 dict 这样的数据结构。应该是python,php只有数组</div>2019-02-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/d1/7c/4639f22c.jpg" width="30px"><span>郭健</span> 👍（1） 💬（1）<div>老师，新年快乐！！看到您给我提问的回答，特别期待您之后的答疑，因为dba怕我们查询数据库时连接时间过长，影响线上实际运行。所以就开发出一个网页，让我们进行查询，但是超过几秒(具体不知道，查询一个200w的数据，条件没有加索引有时候都会)就会返回time out，所以当查询大表并join的时候，就会很吃力！想法设法的缩小单位，一般我们都不会为createTime建一个索引，所以在根据时间缩小范围的时候有时候也并不是很好的选择。我们线上做统计sql的时候，因为数据量比较大，筛选条件也比较多，一个sql可能在0.4s多，这已经是属于慢sql了。感谢老师对我提问的回答！！</div>2019-02-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/56/8c/a8317e23.jpg" width="30px"><span>磊</span> 👍（1） 💬（1）<div>一直对多表的join有些迷惑，希望老师后面专门把这块给讲的透彻些</div>2019-02-03</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/20/08/bc06bc69.jpg" width="30px"><span>Dovelol</span> 👍（1） 💬（1）<div>老师，记得之前看目录之后要将一篇标题大概为“我的mysql为啥莫名其妙重启了”，最近看怎么没有了？我们确实遇到这种问题，在系统日志里也找不到OOM信息，现象是半个月左右就会自动重启一下，时间不固定，想请教下是什么问题呢？</div>2019-02-01</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/ab/18/b01e71d1.jpg" width="30px"><span>immortalCockroach</span> 👍（0） 💬（2）<div>在MRR优化那段，这个例子中a是递增，对应id列是递减，刚好和id递增相反，那这样难道不能“逆序”顺序磁盘读吗？谢谢老师</div>2019-03-01</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/ee/fd/a29a201f.jpg" width="30px"><span>ghostjia</span> 👍（0） 💬（1）<div>遇到一种情况 单表sum 很快，当时和一张大表join 时就很慢，求解决思路：
 SELECT rp.products_id AS ProductsId, sum( rp.products_quantity) AS saleCount FROM test_orders_products AS rp  WHERE  rp.products_id = 740818 ;
+------------+-----------+
| ProductsId | saleCount |
+------------+-----------+
|     740818 |     20772 |
+------------+-----------+
1 row in set (0.01 sec)



但是和一张大表做join,数据就出不来。
mysql&gt; desc SELECT rp.products_id AS ProductsId, sum( rp.products_quantity) AS saleCount FROM test_orders_products AS rp  JOIN test_orders as r ON rp.orders_id = r.orders_id WHERE  rp.products_id = 740818 ;
+----+-------------+-------+--------+------------------------------------------------------------+----------+---------+--------------------------------+-------+-------------+
| id | select_type | table | type   | possible_keys                                              | key      | key_len | ref                            | rows  | Extra       |
+----+-------------+-------+--------+------------------------------------------------------------+----------+---------+--------------------------------+-------+-------------+
|  1 | SIMPLE      | rp    | ref    | idx_orders_id_prod_id_zen,idx_orders_products_pid,idx_test | idx_test | 4       | const                          | 37278 |             |
|  1 | SIMPLE      | r     | eq_ref | PRIMARY                                                    | PRIMARY  | 4       | litb_inbox_master.rp.orders_id |     1 | Using index |
+----+-------------+-------+--------+------------------------------------------------------------+----------+---------+--------------------------------+-------+-------------+
2 rows in set (0.00 sec)
问题是也走了被驱动表的primary key了。 还是会慢。
求解决思路。</div>2019-02-28</li><br/>
</ul>