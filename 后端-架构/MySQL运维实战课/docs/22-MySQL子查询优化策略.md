你好，我是俊达。

这一讲，我们来讨论子查询的一些优化策略。子查询是SQL很重要的一个能力，平时也不少见。

## 子查询的一个例子

早期MySQL（5.5以及更早的版本）对子查询的支持比较弱，使用子查询时容易遇到性能问题。

在13讲的思考题中，就有一个执行了几天都没有完成的SQL。

```plain
Command: Query 
Time: 184551 
State: Sending data 
Info: select item_id, sum(sold) as sold 
      from stat_item_detail 
      where item_id in (
           select item_id 
           from stat_item_detail 
           where gmt_create >= '2019-10-05 08:59:00') 
      group by item_id
```

上面这个SQL语句并不复杂，我们来构建一个测试表，准备一些数据，并做一些测试。使用下面这段SQL创建表，并写入100万行数据。

```plain
create table stat_item_detail(
    id int not null auto_increment,
    item_id int not null,
    sold int not null,
    gmt_create datetime not null,
    padding varchar(4000),
    primary key(id),
    key idx_item_id(item_id),
    key idx_gmt_create(gmt_create)
) engine=innodb;


create view digit 
  as select 0 as a union all select 1 union all select 2 union all select 3 
     union all select 4  union all select 5 union all select 6 
     union all select 7  union all select 8 union all select 9 ;

create view numbers_1m AS 
select ((((a.a * 10 + b.a)*10 + c.a)*10 + d.a)*10+e.a)*10+f.a as n
from digit a, digit b, digit c, digit d, digit e, digit f;

insert into stat_item_detail(item_id, sold, gmt_create, padding)
select n + 1000000 - n % 2 as item_id, 
    n % 100 - n%100%2,  
    date_add('2024-06-01 00:00:00', interval n minute) as gmt_create,
    rpad('x', 1000, 'abcdefg ') as padding
from numbers_1m;
```
<div><strong>精选留言（3）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/15/8d/4d/992070e8.jpg" width="30px"><span>叶明</span> 👍（1） 💬（1）<div>思路1
+----+-------------+------------+------------+-------+----------------------------------------+
| id | select_type | table      | partitions | type  | Extra                                  |
+----+-------------+------------+------------+-------+----------------------------------------+
|  1 | PRIMARY     | &lt;derived2&gt; | NULL       | ALL   | Using temporary                        |
|  1 | PRIMARY     | t1         | NULL       | ref   | NULL                                   |
|  2 | DERIVED     | t2         | NULL       | range | Using index condition; Using temporary |
+----+-------------+------------+------------+-------+----------------------------------------+


第一种改写方式对应半连接转换中的 Materialize with deduplication 策略，
从 distinct item_id 的语义和执行计划中 Extra 列中的 Using temporary，再通过执行计划的执行顺序可知，先生成一个内存临时表，将 item_id 列设置为唯一键，
然后范围扫描索引 idx_gmt_create ，将满足查询条件的 item_id 插入到表中。插入完成后，用该临时表与表 stat_item_detail 进行 join 操作。
这个过程与 materialize with deduplication 策略的过程一样——先将子查询物化成一个临时表，然后对临时表中的记录进行去重操作，最后将去重后的临时表与原主查询中的表进行关联查询。


思路2
+----+-------------+------------+------------+-------+----------------------------------------+
| id | select_type | table      | partitions | type  | Extra                                  |
+----+-------------+------------+------------+-------+----------------------------------------+
|  1 | PRIMARY     | &lt;derived2&gt; | NULL       | ALL   | Using temporary                        |
|  2 | DERIVED     | t2         | NULL       | range | Using index condition; Using temporary |
|  2 | DERIVED     | t1         | NULL       | ref   | NULL                                   |
+----+-------------+------------+------------+-------+----------------------------------------+

第二种改写方式对应半连接转换中的 Duplicate Weedout 策略，使用到了内存临时表，并用主键来去重。</div>2024-10-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/22/42/11674804.jpg" width="30px"><span>陈星宇(2.11)</span> 👍（0） 💬（1）<div>这些策略分别是 pullout、duplicate weedout、first match、loose scan、materialization。 这些是8.0才有吗？在5.7里很少看到。</div>2024-10-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/22/42/11674804.jpg" width="30px"><span>陈星宇(2.11)</span> 👍（0） 💬（1）<div>mysql&gt; explain select item_id, sum(sold) as sold 
      from stat_item_detail 
      where item_id in (
           select item_id 
           from stat_item_detail 
           where Gmt_create &gt;= &#39;2026-04-26 10:30:00&#39;) 
      group by item_id;

+----+--------------------+------------------+----------------+----------------------------+-------------+---------+------+---------+-------------+
| id | select_type        | table            | type           | possible_keys              | key         | key_len | ref  | rows    | Extra       |
+----+--------------------+------------------+----------------+----------------------------+-------------+---------+------+---------+-------------+
|  1 | PRIMARY            | stat_item_detail | index          | NULL                       | idx_item_id | 4       | NULL | 1000029 | Using where |
|  2 | DEPENDENT SUBQUERY | stat_item_detail | index_subquery | idx_item_id,idx_gmt_create | idx_item_id | 4       | func |       1 | Using where |
+----+--------------------+------------------+----------------+----------------------------+-------------+---------+------+---------+-------------+
执行不是按id从大到小执行吗？感觉子查询应该走时间字段的索引，这里是不是有问题，有点没理解。
“从上面的这个执行计划可以看到，这个 SQL 在执行时，先全量扫描索引 idx_item_id，每得到一个 item_id 后，执行相关子查询（DEPENDENT SUBQUERY）select 1 from stat_item_detail where gmt_create &gt;= ‘2026-04-26 10:30:00’ and item_id = primary.item_id。当主查询中表中的数据量很大的时候，子查询执行的次数也会很多，因此 SQL 的性能非常差。”</div>2024-10-11</li><br/>
</ul>