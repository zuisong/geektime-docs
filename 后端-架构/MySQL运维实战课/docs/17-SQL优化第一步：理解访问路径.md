你好，我是俊达。

大家都知道，我们使用SQL来访问数据库，而优化 SQL 对于保证数据库系统的高效、稳定运行，以及满足业务需求和降低成本都具有至关重要的意义。从这一讲开始，我们来系统地学习SQL优化。一条SQL语句，在数据库内部是怎么执行的呢？SQL的性能，又会受哪些因素影响呢？

关系型数据库中，SQL语句的执行主要分为几个大的步骤。

1. 对SQL文本进行解析，生成SQL语法树。
2. 优化器根据SQL语法树、表和索引的结构和统计信息，生成执行计划。
3. SQL执行引擎根据执行计划，按一定的步骤，调用存储引擎接口获取数据，执行表连接、排序等操作，生成结果集。
4. 将结果集发送给客户端。

![图片](https://static001.geekbang.org/resource/image/74/78/748d265eb3b0e5b737eb9fa9aa473d78.jpg?wh=1602x766)

在这一讲和接下来的几讲中，我将围绕**优化器、执行计划、SQL执行引擎**，把SQL优化讲透。

我们先从访问路径（Access path）开始。访问路径是指根据表的物理存储结构，以及给定的查询条件，从表中获取数据的方法。访问路径包括表扫描和索引访问，还包括表连接的算法，如嵌套循环连接（Nested Loop Join）、哈希连接（Hash Join）、排序合并连接（Sort Merge Join）。

## 表的物理存储

### 数据页

数据页是数据表中数据存储的基本单位。一个数据页的大小通常可能为4K、8K、16K、32K。在InnoDB中，默认的页面大小为16K。记录以行的形式存储在数据页中，每行记录在数据页中占用一段连续的空间。通常1行记录可能占用几十字节到几百或几千字节。每个数据页能容纳的记录数一般在几行到几百行之间。
<div><strong>精选留言（4）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/28/a1/d8/42252c48.jpg" width="30px"><span>123</span> 👍（1） 💬（1）<div>思考题：
以下测验均在mysql8.0.29版本中：

#符合idx_abc索引的顺序条件，可以通过a,b进行条件筛选，但是需要回表
select * from t_abc where a = 10 and b = 10;

#符合idx_abc索引的最左匹配原则，c=10未能使用索引匹配，但可以使用索引条件下推，过滤一些索引行
select * from t_abc where a = 10 and c = 10;

#符合idx_abc索引最左匹配，但只能利用a字段过滤，需要回表，再判断d的值，若改成or则不走索引
select * from t_abc where a = 10 and d = 10;

上述三条语句全部走索引，区别在于能利用索引提升的速度不同；

#无法利用索引有序性消除排序，因为字段顺序不连续(Using filesort)
select * from t_abc where a = 10 order by a,c;

#无需额外排序
select * from t_abc where a = 10 order by b,c;

#完美匹配idx_abc，走覆盖索引
select id, a, b, c from t_abc where a = 10;

上述两条sql语句区别在于能否通过索引原有的顺序而消除排序；

#因为不符合最左匹配原则，应该不走二级索引，但是由于所需字段均在idx_abc中，mysql认为走索引的扫描成本会更低，所以走了索引，扫描行数和下面的全表扫描的行数是一致的，走了覆盖索引(Using index)
select id, a, b, c from t_abc where b = 10;

#和select * 无异，因为b上面建索引且不符合最左匹配原则，走全表扫描
select id, a, b, c, d from t_abc where b = 10;

上述三条sql区别在于是否可以利用覆盖索引，根据语句的内容选择扫描成本低的方案</div>2024-09-25</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/2b/fd/b6/5edc8c70.jpg" width="30px"><span>山河已无恙</span> 👍（0） 💬（1）<div>老师覆盖索引哪里 Where 条件不满足最左匹配原则么，也会走覆盖索引么
```sql
index(C1, C2, C3, C4, C5)


select C1,C2 
from tab
where C3=x
order by C5
```
</div>2025-01-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/2b/fd/b6/5edc8c70.jpg" width="30px"><span>山河已无恙</span> 👍（0） 💬（2）<div>测试用的表，用于模拟业务表
```sql
SET profiling=1;
SELECT COUNT(*)  FROM ams_accounts_order;
&#47;* 受影响记录行数: 0  已找到记录行: 1  警告: 0  持续时间 1 查询: 1.469 秒. *&#47;
SHOW PROFILE;
```
数据量

ams_accounts_order
---
| COUNT(*) | 
| ---: | 
| 6202700 | 

默认情况下只有主键，两个查询条件的查询时间

```sql
SET profiling=1;
SELECT * from ams_accounts_order where hotel_id = 10029 AND room_order_no = &#39;UDDH807015895560880128&#39; ORDER BY accounts_id DESC 

;
&#47;* 受影响记录行数: 0  已找到记录行: 18  警告: 0  持续时间 1 查询: 6.250 秒. *&#47;
SHOW PROFILE;
SET profiling=0;
```

对其中一个查询条件添加索引

```sql
ALTER TABLE `ams_accounts_order`
	DROP INDEX `hotel_id`,
	ADD INDEX `hotel_id` (`hotel_id`);
```

再次查询

```sql
SET profiling=1;
SELECT * from ams_accounts_order where hotel_id = 10029 AND room_order_no = &#39;UDDH807015895560880128&#39; ORDER BY accounts_id DESC ;
&#47;* 受影响记录行数: 0  已找到记录行: 18  警告: 0  持续时间 1 查询: 18.547 秒. *&#47;
SHOW PROFILE;
SET profiling=0;
```
发现加了不如不加，时间是原来的 3 倍多

查看 `EXPLAIN` 结果中的 `key` 和 `Extra` 字段,确认使用了创建的索引


EXPLAIN
| id | select_type | table | partitions | type | possible_keys | key | key_len | ref | rows | filtered | Extra | 
| ---: | --- | --- | --- | --- | --- | --- | --- | --- | ---: | ---: | --- | 
| 1 | SIMPLE | ams_accounts_order | \N | ref | hotel_id | hotel_id | 4 | const | 3069172 | 10.00 | Using where | 

老师这种情况为什么加了不如不加</div>2024-10-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/28/a1/d8/42252c48.jpg" width="30px"><span>123</span> 👍（0） 💬（1）<div>老师，请教两个问题：
1、“在分支页面中，Value 存了下一层索引页面的编号（Page No），页面编号就是页面在数据文件中的地址”，其中页面编号就是页面在数据文件中地址，这个数据文件应该就是.ibd文件吧，存储了数据信息，并且一二级索引的数据都在这个文件里面，所在在ibd文件中哪里可以看到页编号，老师后面会讲数据的物理存储结构吗？

2、表数据存储在页中，页中存储行数据，当行数据变大之后，例如可变长VARCHAR字段，则就会进行页的新增，老师文中提到，每个区块由连续的64个数据页组成，这里应该是物理连续吧？那么行内数据增加后务必会造成数据页的分裂，也就是说原来一页能存100条，现在只能存储50条了，同时为了保证连续，多出的页面会造成后续页面在空间上移动，进而造成在磁盘空间中数据的移动，不知道怎么理解对不对，那么为了防止大量的数据移动，区块或者段数据之间应该是逻辑连续而不是物理连续，也就是说使用链表的形式连接？</div>2024-09-25</li><br/>
</ul>