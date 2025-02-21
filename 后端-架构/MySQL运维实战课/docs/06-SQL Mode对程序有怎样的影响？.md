你好，我是俊达。

SQL Mode是MySQL中比较特殊的一个概念，可以通过参数sql\_mode进行设置。设置SQL Mode会影响数据库对SQL的语法支持，也会影响数据写入时的校验规则。早期的MySQL使用非严格模式，这样有一些不符合SQL标准的语句在MySQL中也能执行，一些按SQL标准来说不合法的数据，也能写到表里面。

不过从MySQL 5.7开始，默认就开启了严格模式。这一讲中，我们一起来看看SQL Mode是怎么影响到SQL语句的，以及应该怎么设置SQL Mode。

## 非严格模式

非严格模式下，MySQL会允许你执行一些不符合SQL标准的语句。我们通过一些例子来说明这种情况。先创建一个测试表，写入一些数据。

```go
mysql> create table tab2(
    b int, 
    c varchar(10), 
    d varchar(30)
) engine=innodb;

Query OK, 0 rows affected (10.16 sec)

mysql> insert into tab2 values
    (10, 'AAA1', 'BBB1'),
    (20, 'AAA4', 'BBB4'), 
    (10, 'AAA3', 'BBB3'), 
    (20, 'AAA2', 'BBB2')

Query OK, 4 rows affected (0.56 sec)
Records: 4  Duplicates: 0  Warnings: 0

mysql> select * from tab2;
+------+------+------+
| b    | c    | d    |
+------+------+------+
|   10 | AAA1 | BBB1 |
|   20 | AAA4 | BBB4 |
|   10 | AAA3 | BBB3 |
|   20 | AAA2 | BBB2 |
+------+------+------+
4 rows in set (0.00 sec)
```
<div><strong>精选留言（3）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/2a/39/93/f0247cf8.jpg" width="30px"><span>一本书</span> 👍（0） 💬（1）<div>如果同时设置STRICT_TRANS_TABLES、STRICT_ALL_TABLES，那在非事务表中 INSERT 超出范围的值，处理方式是什么呢？</div>2024-09-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/17/e9/26/472e16e4.jpg" width="30px"><span>Amosヾ</span> 👍（0） 💬（1）<div>为什么建议设置严格模式？非严格模式会有哪些危害呢？</div>2024-08-31</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/28/a1/d8/42252c48.jpg" width="30px"><span>123</span> 👍（0） 💬（1）<div>思考题：

首先查看数据库的版本是否一致，mysql在5.7默认开启严格模式，通过show variables like &#39;innodb_strict_mode&#39;查看，当前情况下，主库是在非严格模式下，而备库在严格模式下

解决方案：
1、设置备库为非严格模式，除非是业务需求，尽量不要使用非严格模式
2、修改主库表的DDL，开启严格模式（在业务改动不大的情况下），让备库忽略该GTID，不执行该语句，后由主库重新创建后会自动同步

另外，请教下老师，非严格模式使用会多吗，我们生产要求必须要使用严格模式</div>2024-08-30</li><br/>
</ul>