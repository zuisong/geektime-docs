接上一讲

### POSSIBLE\_KEYS

possible\_keys列显示查询单元能使用range、ref等访问路径访问的索引。执行计划最终选择的索引在keys列显示。是否使用索引，以及使用哪个索引，取决于优化器对各种访问方式的成本评估，还跟表连接的顺序和连接算法也有关系。

下面这个例子中，t1表的possible\_keys有索引idx\_abc，但是当t1表作为驱动表时，就无法使用索引idx\_abc。

```plain
mysql> explain select * from tab t1, tab t2 where t1.a = t2.a and t1.b = t2.b;


+----+-------------+-------+------+---------------+---------+---------+-------------------+------+----------+-------+
| id | select_type | table | type | possible_keys | key     | key_len | ref               | rows | filtered | Extra |
+----+-------------+-------+------+---------------+---------+---------+-------------------+------+----------+-------+
|  1 | SIMPLE      | t1    | ALL  | idx_abc       | NULL    | NULL    | NULL              | 9913 |   100.00 | NULL  |
|  1 | SIMPLE      | t2    | ref  | idx_abc       | idx_abc | 8       | rep.t1.a,rep.t1.b |    1 |   100.00 | NULL  |
+----+-------------+-------+------+---------------+---------+---------+-------------------+------+----------+-------+
```
<div><strong>精选留言（3）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/24/f7/b9/f2eec64e.jpg" width="30px"><span>Shelly</span> 👍（1） 💬（1）<div>思考题： 
SELECT   
    t1.id, 
    t1.a, 
    t2.avg_b 
FROM 
    tab t1   
RIGHT JOIN 
    (SELECT 
        a, 
        AVG(b) AS avg_b 
     FROM 
        tab     
     GROUP BY 
        a) t2 
ON
    t1.a = t2.a 
ORDER BY 
    t1.id;
这么写会生成临时表，被驱动表t1被扫描三次</div>2024-09-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/28/a1/d8/42252c48.jpg" width="30px"><span>123</span> 👍（1） 💬（1）<div>老师，文中说到“const 表示查询最多返回 1 行记录。对主键或唯一索引的所有字段都使用常量等值匹配时，type 为 const。优化器会将 type 为 const 的查询单元直接替换为常量表。”这个常量表具体指什么，是如何产生的？该主键索引的查询到的值不也是需要通过B+树层级扫描链接获取到吗？</div>2024-09-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/8d/4d/992070e8.jpg" width="30px"><span>叶明</span> 👍（0） 💬（1）<div>思考题
将子查询改为联表查询，先聚合后 join,避免对表中每行记录都进行聚合计算
  
select
  t1.id,
  t1.a,
  t2.avg_b
from
  tab t1
  inner join (
    select
      a,
      avg(b) avg_b
    from
      tab
    group by
      a
  ) t2 on t1.a = t2.a
order by
  id;

10000 rows in set (0.04 sec)</div>2024-09-27</li><br/>
</ul>