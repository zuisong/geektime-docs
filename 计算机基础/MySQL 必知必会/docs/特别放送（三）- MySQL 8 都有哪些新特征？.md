你好，我是朱晓峰。今天，我来和你聊一聊MySQL 8的新特征。

作为应用最广泛的三大关系型数据库之一，MySQL的背后有一个强大的开发团队，使MySQL能够持续迭代和创新，满足不断变化的用户需求。在MySQL 8中，就有很多新特征。

今天，我就给你介绍两个重要的新特征：窗口函数和公用表表达式（Common Table Expressions，简称CTE）。它们可以帮助我们用相对简单的查询语句，实现更加强大的查询功能。

## 什么是窗口函数？

窗口函数的作用类似于在查询中对数据进行分组，不同的是，分组操作会把分组的结果聚合成一条记录，而窗口函数是将结果置于每一条数据记录中。一会儿我会借助一个例子来对比下，在此之前，你要先掌握窗口函数的语法结构。

窗口函数的语法结构是：

```
函数 OVER（[PARTITION BY 字段]）
```

或者是：

```
函数 OVER 窗口名 … WINDOW 窗口名 AS （[PARTITION BY 字段名]）
```

现在，我借助一个小例子来解释一下窗口函数的用法。

假设我现在有这样一个数据表，它显示了某购物网站在每个城市每个区的销售额：

```
mysql> SELECT * FROM demo.test1;
+----+------+--------+------------+
| id | city | county | salesvalue |
+----+------+--------+------------+
|  1 | 北京 | 海淀   |      10.00 |
|  2 | 北京 | 朝阳   |      20.00 |
|  3 | 上海 | 黄埔   |      30.00 |
|  4 | 上海 | 长宁   |      10.00 |
+----+------+--------+------------+
4 rows in set (0.00 sec)
```

现在我想计算一下，这个网站在每个城市的销售总额、在全国的销售总额、每个区的销售额占所在城市销售额中的比率，以及占总销售额中的比率。

如果用分组和聚合函数，就需要分好几步来计算。
<div><strong>精选留言（3）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/27/da/ee/63090718.jpg" width="30px"><span>流云追风</span> 👍（1） 💬（1）<div>这和oracle的分析函数,with as一样</div>2021-09-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/21/b7/88/0c3e1a80.jpg" width="30px"><span>freshswq</span> 👍（1） 💬（1）<div>1.建表语句：
DROP TABLE
IF
	EXISTS memtrans;
	
CREATE TABLE
IF
	NOT EXISTS memtrans (
		id INT PRIMARY KEY auto_increment,
		membername VARCHAR ( 20 ) NOT NULL,
		goodname VARCHAR ( 20 ) NOT NULL,
		actualvalue DECIMAL ( 10, 2 ) NOT NULL 
	)ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

2.插入数据：
insert into memtrans values(1,&#39;张三&#39;,&#39;书&#39;,890);
insert into memtrans values(2,&#39;李四&#39;,&#39;笔&#39;,30);
insert into memtrans values(3,&#39;王五&#39;,&#39;书&#39;,89);

3.数据查询：
SELECT
	membername AS 会员名称,
	goodname AS 商品名称,
	actualvalue AS 销售金额,
	sum( actualvalue ) over ( PARTITION BY goodname ) AS 总计金额,
	actualvalue &#47; sum( actualvalue ) over ( PARTITION BY goodname ) AS 销售占比 
FROM
	memtrans;</div>2021-05-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/28/e6/eb/7b7c0101.jpg" width="30px"><span>彭彬</span> 👍（0） 💬（0）<div>SQL  SERVER有这两个概念</div>2021-10-07</li><br/>
</ul>