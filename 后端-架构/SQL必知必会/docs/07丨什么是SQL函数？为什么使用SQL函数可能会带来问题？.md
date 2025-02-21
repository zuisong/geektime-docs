函数在计算机语言的使用中贯穿始终，在SQL中我们也可以使用函数对检索出来的数据进行函数操作，比如求某列数据的平均值，或者求字符串的长度等。从函数定义的角度出发，我们可以将函数分成内置函数和自定义函数。在SQL语言中，同样也包括了内置函数和自定义函数。内置函数是系统内置的通用函数，而自定义函数是我们根据自己的需要编写的，下面讲解的是SQL的内置函数。

你需要从以下几个方面掌握SQL函数：

1. 什么是SQL函数？
2. 内置的SQL函数都包括哪些？
3. 如何使用SQL函数对一个数据表进行操作，比如针对一个王者荣耀的英雄数据库，我们可以使用这些函数完成哪些操作？
4. 什么情况下使用SQL函数？为什么使用SQL函数有时候会带来问题？

## 什么是SQL函数

当我们学习编程语言的时候，也会遇到函数。函数的作用是什么呢？它可以把我们经常使用的代码封装起来，需要的时候直接调用即可。这样既提高了代码效率，又提高了可维护性。

SQL中的函数一般是在数据上执行的，可以很方便地转换和处理数据。一般来说，当我们从数据表中检索出数据之后，就可以进一步对这些数据进行操作，得到更有意义的结果，比如返回指定条件的函数，或者求某个字段的平均值等。

## 常用的SQL函数有哪些
<div><strong>精选留言（30）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/12/f9/90/f90903e5.jpg" width="30px"><span>菜菜</span> 👍（34） 💬（4）<div>学得我想打王者荣耀了</div>2019-06-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/2b/84/07f0c0d6.jpg" width="30px"><span>supermouse</span> 👍（22） 💬（1）<div>计算英雄的最大生命平均值：
SELECT AVG(hp_max) FROM heros;

显示所有在2017年之前上线的英雄：
SELECT name FROM heros WHERE birthdate IS NOT NULL AND YEAR(birthdate) &lt; 2017;</div>2019-06-27</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTICAILuSqtnAfl1zcgRWIULia2nbjzlybTEQJUMT68KPj80BicwQyibAK3Icxp4qwC03LqrtvfX0fbZg/132" width="30px"><span>番茄</span> 👍（8） 💬（2）<div>能请教下，mysql不能用with table as 这个语句，要用什么来替代这个比较方便呢</div>2019-08-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/17/d9/a7/a794afb1.jpg" width="30px"><span>Andre</span> 👍（7） 💬（1）<div>答案：SELECT avg(hp_max) as avg_hp
FROM heros;

SELECT `name`
FROM heros
WHERE birthdate is NOT NULL AND DATE(birthdate)&lt;&#39;2017-01-01&#39;;
另外赞同时间是最真的答案的说法，应该来讲基础篇大家都还是学起来不费力的，希望基础篇能够快点更新，然后尽快的进入进阶篇</div>2019-06-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/64/29/da537902.jpg" width="30px"><span>Abyssknight</span> 👍（3） 💬（2）<div>select avg(hp_max) as avg_hp
from heros;

select name, birthdate
from heros
where birthdate &lt; date(&#39;2017-01-01&#39;);</div>2019-06-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/e6/68/1871d6ba.jpg" width="30px"><span>海洋</span> 👍（2） 💬（1）<div>作业：
SELECT AVG(hp_max) FROM heros;
+-------------------+
| AVG(hp_max)       |
+-------------------+
| 6580.478260869565 |
+-------------------+
1 row in set (0.07 sec)

-------------------------------------------
 SELECT name FROM heros WHERE Year(birthdate) &lt; 2017 AND birthdate is NOT NULL;
+----------+
| name     |
+----------+
| 夏侯惇   |
| 牛魔     |
| 吕布     |
| 芈月     |
| 太乙真人 |
| 刘邦     |
| 关羽     |
| 马可波罗 |
| 李元芳   |
| 虞姬     |
| 成吉思汗 |
| 不知火舞 |
| 貂蝉     |
| 周瑜     |
| 张良     |
| 钟馗     |
| 蔡文姬   |
| 花木兰   |
| 李白     |
| 杨戬     |
| 刘备     |
| 宫本武藏 |
| 娜可露露 |
+----------+
或者
SELECT name FROM heros WHERE DATE(birthdate) &lt;&#39;2017-01-01&#39; AND birthdate is NOT NULL;</div>2019-08-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/b7/b6/17103195.jpg" width="30px"><span>Elliot</span> 👍（2） 💬（1）<div>DBMS 之间的差异性很大，远大于同一个语言不同版本之间的差...

说明学数据库也难免会遇到各种看似毫无技术含量的坑喽。。。</div>2019-07-07</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/e5/33/ff5c52ad.jpg" width="30px"><span>不负</span> 👍（1） 💬（1）<div>&gt; SELECT ROUND(AVG(hp_max), 2) FROM heros;
+-----------------------+
| ROUND(AVG(hp_max), 2) |
+-----------------------+
|               6580.48 |
+-----------------------+
&gt; SELECT name FROM heros WHERE birthdate IS NOT NULL AND DATE(birthdate)&lt;&#39;2017-01-01&#39;;</div>2019-06-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/18/32/82/273a44cd.jpg" width="30px"><span>圆子蛋</span> 👍（1） 💬（1）<div>1. SELECT AVG(max_hp) FROM heros;
2. SELECT name,YEAR(birthdate) AS birthdate FROM heros WHERE birthdate is NOT NULL AND YEAR(birthdate)&lt;2017</div>2019-06-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/19/8f/4f/d42fdb9c.jpg" width="30px"><span>Amo,</span> 👍（0） 💬（1）<div>今日打卡sql函数</div>2020-03-22</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/QD6bf8hkS5dHrabdW7M7Oo9An1Oo3QSxqoySJMDh7GTraxFRX77VZ2HZ13x3R4EVYddIGXicRRDAc7V9z5cLDlA/132" width="30px"><span>爬行的蜗牛</span> 👍（0） 💬（1）<div>SELECT name,  hp_max
FROM heros
WHERE DATE (birthdate) &lt; &#39;2017-1-1&#39;  AND birthdate IS NOT NULL;</div>2019-12-22</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/QD6bf8hkS5dHrabdW7M7Oo9An1Oo3QSxqoySJMDh7GTraxFRX77VZ2HZ13x3R4EVYddIGXicRRDAc7V9z5cLDlA/132" width="30px"><span>爬行的蜗牛</span> 👍（0） 💬（1）<div>SELECT name,  hp_max
FROM heros
WHERE DATE (birthdate) &lt; &#39;2017-1-1&#39;  AND birthdate IS NOT NULL;</div>2019-12-22</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/AGicQgKibwja1SxkQ7oXQE8hYH7yCpiaicNHw3qZRuNB81aVDOQm9P1zd5F75Jbtv66G15D6ZjbbqfnoETR4321Zdw/132" width="30px"><span>高泽林</span> 👍（0） 💬（1）<div>计算英雄的最大生命平均值：
SELECT AVG(hp_max) FROM heros;

显示所有在2017年之前上线的英雄：
SELECT name FROM heros WHERE birthdate IS NOT NULL AND YEAR(birthdate) &lt; 2017;</div>2019-12-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/3b/fc/04a75cd0.jpg" width="30px"><span>taoist</span> 👍（0） 💬（1）<div>#MariaDB:

#英雄的最大生命平均值:
SELECT  ROUND(AVG(hp_max)) as avg_hp FROM heros;

#显示出所有在 2017 年之前上线的英雄:
SELECT name,birthdate FROM heros WHERE   EXTRACT(YEAR FROM birthdate) &lt; &#39;2017&#39;;</div>2019-12-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/19/69/bf/58f70a2a.jpg" width="30px"><span>程序员花卷</span> 👍（0） 💬（1）<div>第一题：计算最大生命值的平均值
mysql&gt; SELECT AVG(hp_max)
    -&gt; FROM heros；
第二题：计算在2017年之前上线的英雄，如果不存在，那么就不显示
mysql&gt; SELECT *
    -&gt; FROM heros
    -&gt; WHERE YEAR(birthdate) &lt; &#39;2017&#39; AND birthdate IS NOT NULL;
根据老师所讲的，所有的关键字和函数都尽量大写，其他的都小写，这是规范。
今天学习了几种比较常用的函数的类型：
日期函数
算数函数
字符串函数

在写查询语句的时候应该注意安全性的问题，有的语句虽然能执行出来，但是存在一些不安全的因素
在写SQL函数的时候，应该注意版本问题
最后就是大小写的规范！</div>2019-11-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/19/5b/08/b0b0db05.jpg" width="30px"><span>丁丁历险记</span> 👍（0） 💬（1）<div>坚决不用sql 日期函数的路过。</div>2019-11-07</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/2e/74/88c613e0.jpg" width="30px"><span>扶幽</span> 👍（0） 💬（1）<div>练习：
1) select AVG(hp_max) from heros;
2) select name, YEAR(birth_date) as birthdate from heros where birthdate is not null AND birthdate&lt;&#39;2017&#39;;</div>2019-10-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/19/f7/46/209ca424.jpg" width="30px"><span>Coool</span> 👍（0） 💬（1）<div>计算英雄的最大生命平均值：
SELECT AVG(hp_max) FROM heros;
显示出所有在 2017 年之前上线的英雄，如果英雄没有统上线时间则不显示：
SELECT * FROM heros WHERE birthdate is not null and DATE(birthdate)&lt;&#39;2017-01-01&#39;；</div>2019-10-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/92/ba/9833f06f.jpg" width="30px"><span>半瓶醋</span> 👍（0） 💬（1）<div>SELECT AVG(hp_max) as &#39;最大生命平均值&#39;
from heros;

SELECT name,hp_max,mp_max,YEAR(birthdate)
FROM heros
WHERE YEAR(birthdate) &lt; &#39;2017&#39;;
第二道题我没有加is not null 的判断，直接用YEAR（）函数进行判断的话可不可以呢？</div>2019-10-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/ea/46/9c9808a9.jpg" width="30px"><span>Serendipity</span> 👍（0） 💬（1）<div>SELECT AVG(hp_max) FROM heros
SELECT name, YEAR(birthdate) FROM heros WHERE YEAR(birthdate)&lt;2017 AND birthdate IS NOT NULL</div>2019-08-31</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/9b/a8/6a391c66.jpg" width="30px"><span>geraltlaush</span> 👍（0） 💬（1）<div>想起之前从mysql时间戳提取日期，都是用select from_unixtimestamp(%%%%)里面一堆参数，每次都要去记的笔记里找（参数太多记不住），我想扇自己一耳光</div>2019-08-18</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTIk46cor5XVFTPZbPOnb7pViabgy450pobo46hRHFQz5nR5ocYRKIzC8vShic36vwa553H4Vj50x5wA/132" width="30px"><span>冲</span> 👍（0） 💬（1）<div>SELECT name,AVG(hp_max) from heros WHERE DATE(birthdate)&lt;&#39;2017-01-01&#39; and birthdate is not null</div>2019-08-07</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/fd/90/ae39017f.jpg" width="30px"><span>爱吃锅巴的沐泡</span> 👍（0） 💬（1）<div>老师，有个问题？
在group by子句中可以直接使用列的别名嘛？
在group by子句中可以使用DATE()函数嘛？</div>2019-07-30</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/9b/a8/6a391c66.jpg" width="30px"><span>geraltlaush</span> 👍（0） 💬（1）<div>如果对索引做函数操作会导致索引无效，这个也是注意点吧</div>2019-07-30</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/b5/98/ffaf2aca.jpg" width="30px"><span>Ronnyz</span> 👍（0） 💬（1）<div>作业：
SELECT AVG(hp_max) FROM heros;
SELECT name, birthdate FROM heros WHERE YEAR(birthdate) &lt; 2017 AND birthdate IS NOT NULL;</div>2019-07-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/7a/d5/dbcaadf0.jpg" width="30px"><span>蓝影闪电</span> 👍（0） 💬（1）<div>SELECT AVG(hp_max) FROM heros;

SELECT name FROM heros
WHERE YEAR(birthdate)&lt;&#39;2017&#39; AND birthdate IS NOT NULL;
</div>2019-07-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/8f/82/374f43a1.jpg" width="30px"><span>假装自己不胖</span> 👍（0） 💬（1）<div>DATE()筛出来的是没有时分秒的.如果要时分秒,有其他函数可以使用吗</div>2019-07-15</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/e6/6e/062da5e4.jpg" width="30px"><span>肥而不腻</span> 👍（0） 💬（1）<div>学完打卡</div>2019-07-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/02/57/9b235866.jpg" width="30px"><span>2525</span> 👍（0） 💬（1）<div>作业: mysql

select AVG(hp_max) as 最大生命平均值 FROM heros;
select name,birthdate from heros where birthdate is not null and  EXTRACT(YEAR FROM DATE(birthdate))&lt;&quot;2017&quot;</div>2019-07-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/0d/45/b88a1794.jpg" width="30px"><span>一叶知秋</span> 👍（0） 💬（1）<div>交作业：
1)MySQL SELECT ROUND(AVG(hp_max), 2) as average_hp FROM heros;
执行结果： 
+------------+
| average_hp |
+------------+
|    6580.48 |
+------------+
1 row in set (0.00 sec)

2）MySQL：SELECT name, birthdate FROM heros WHERE birthdate IS NOT NULL and DATE(birthdate)&lt;&#39;2017-1-1&#39; ORDER BY birthdate ASC;
执行结果：
+--------------+------------+
| name         | birthdate  |
+--------------+------------+
| 张良         | 2015-10-26 |
| 宫本武藏     | 2015-10-30 |
| 周瑜         | 2015-11-10 |
| 牛魔         | 2015-11-24 |
| 芈月         | 2015-12-08 |
| 貂蝉         | 2015-12-15 |
| 吕布         | 2015-12-22 |
| 花木兰       | 2016-01-01 |
| 刘备         | 2016-02-02 |
| 娜可露露     | 2016-02-22 |
| 李白         | 2016-03-01 |
| 钟馗         | 2016-03-24 |
| 李元芳       | 2016-04-12 |
| 刘邦         | 2016-04-26 |
| 不知火舞     | 2016-05-12 |
| 虞姬         | 2016-05-24 |
| 关羽         | 2016-06-28 |
| 蔡文姬       | 2016-07-08 |
| 夏侯惇       | 2016-07-19 |
| 马可波罗     | 2016-08-23 |
| 成吉思汗     | 2016-09-27 |
| 杨戬         | 2016-10-11 |
| 太乙真人     | 2016-11-24 |
+--------------+------------+
23 rows in set (0.00 sec)

本章收获：规范大小写。</div>2019-07-05</li><br/>
</ul>