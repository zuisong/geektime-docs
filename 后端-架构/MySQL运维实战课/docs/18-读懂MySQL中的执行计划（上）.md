你好，我是俊达。

上一讲我介绍了数据库中最主要的几种访问路径，不同的访问路径，在执行性能上可能会存在巨大的差别。但是我们怎么知道某一个具体的SQL语句在执行时，采用了什么样的访问路径呢？这就涉及到SQL的执行计划了。执行计划描述了SQL语句的访问路径，通过执行计划，我们可以知道：

- 表上是否有可用的索引，SQL执行时是否使用了索引，使用了哪些索引？
- 表连接的顺序是怎样的？
- 使用了哪种表连接算法，是用了Nest Loop还是Hash Join？
- 查询是否用到了临时表，是否进行了文件排序？

在MySQL中，我们使用Explain命令查看语句的执行计划。这一讲中我会使用四十多个演示SQL，来解释EXPLAIN输出信息的具体含义。至于为什么一个SQL使用了这个执行计划，而不是别的执行计划，我会在接下来的几讲中慢慢展开。

为了便于演示各种不同的执行计划，我使用了下面这些测试表和测试数据，你也可以在自己的环境中进行测试。

```plain
CREATE TABLE `digit` (
  `a` tinyint NOT NULL,
  PRIMARY KEY (`a`)
) ENGINE=InnoDB;

insert into digit values (0),(1),(2),(3),(4),(5),(6),(7),(8),(9);

CREATE VIEW numbers AS 
select a.a*1000 + b.a*100 + c.a*10 + d.a as n 
from digit a, digit b, digit c, digit d;

-- 本章中大部分案例都使用tab表
CREATE TABLE `tab` (
  `id` int NOT NULL AUTO_INCREMENT,
  `a` int NOT NULL,
  `b` int NOT NULL,
  `c` int NOT NULL,
  `padding` varchar(7000) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `idx_abc` (`a`,`b`,`c`)
) ENGINE=InnoDB;

insert into tab (a,b,c,padding) 
select n%3, n, n%100, rpad('x', 100, 'x')  
from numbers where n < 10000;

-- t_merge主要用于演示index_merge的几种情况
create table t_merge(
    id int not null auto_increment, 
    a int not null,
    b int not null,
    c int not null,
    d int not null,
    padding varchar(4000),
    primary key(id),
    key idx_ad(a,d),
    key idx_bd(b,d),
    key idx_cd(c,d)
) ENGINE=InnoDB;

insert into t_merge(a,b,c,d,padding)
select n % 3 + 1, n % 17 + 1, n % 19 + 1, n % 10 + 1, rpad('y', 100, 'y')
from numbers
where n between 1 and 3*17*19*10;
```
<div><strong>精选留言（2）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/3c/4a/fe/7b6bd101.jpg" width="30px"><span>笙 鸢</span> 👍（0） 💬（1）<div>老师，派生表的讲解处，好多DRIVED的写法，是不是写错了？？</div>2024-11-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/19/83/6a/6f04edbd.jpg" width="30px"><span>mw</span> 👍（0） 💬（2）<div>老师好，请教个问题：在选择驱动表的时候 需要过滤where 之后的所有条件之后以数据量小的作为驱动表。
1、那要是where之后的条件没有索引或者无法使用索引的Cardinality进行估算过滤，那选择驱动表的时候就需要扫描全表过滤出符合where条件的数据，然后每个表比较符合的数据量大小，之后选出驱动表吗？ 还是说有其他的计算方法。
2、如果where后面同时存在一个表的索引字段条件和非索引字段条件，需要索引字段过滤之后 再过滤非索引字段的条件吗？</div>2024-10-17</li><br/>
</ul>