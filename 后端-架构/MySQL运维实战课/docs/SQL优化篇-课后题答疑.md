你好，我是俊达。

这一讲我们来看一下SQL优化篇中的思考题的解答。

## 第17讲

问题：

```plain
create table t_n(a int not null, primary key(a));


insert into t_n values(1),(2),(3),(4),(5),(6),(7),(8),(9),(10),
  (11),(12),(13),(14),(15),(16),(17),(18),(19),(20);


create table t_abc(
    id int not null auto_increment,
    a int not null,
    b int not null,
    c int not null,
    d int not null,
    padding varchar(200),
    primary key(id),
    key idx_abc(a,b,c)
) engine=innodb;


insert into t_abc(a,b,c,d, padding)
select t1.a, t2.a, t3.a, t3.a, rpad('', 200, 'ABC DEF G XYZ')
from t_n t1, t_n t2, t_n t3;
```

根据测试表t\_abc的结构，分析下面这几个SQL语句的执行路径，有哪些区别？

```plain
-- SQL 1
select * from t_abc where a = 10 and b = 10;
-- SQL 2
select * from t_abc where a = 10 and c = 10;
-- SQL 3
select * from t_abc where a = 10 and d = 10;

-- SQL 4
select * from t_abc where a = 10 order by a,c;
-- SQL 5
select * from t_abc where a = 10 order by b,c;

-- SQL 6
select id, a, b, c from t_abc where a = 10;
-- SQL 7
select id, a, b, c from t_abc where b = 10;
-- SQL 8
select id, a, b, c, d from t_abc where b = 10;
```
<div><strong>精选留言（1）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/11/10/90/807689c3.jpg" width="30px"><span>Geek_9ius3m</span> 👍（0） 💬（1）<div>请问老师，是什么导致了数据库CPU居高不下呢？学了您的课程还是没有搞清楚。</div>2025-01-13</li><br/>
</ul>