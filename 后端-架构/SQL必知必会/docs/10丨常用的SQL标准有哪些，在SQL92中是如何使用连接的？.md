今天我主要讲解连接表的操作。在讲解之前，我想先给你介绍下连接（JOIN）在SQL中的重要性。

我们知道SQL的英文全称叫做Structured Query Language，它有一个很强大的功能，就是能在各个数据表之间进行连接查询（Query）。这是因为SQL是建立在关系型数据库基础上的一种语言。关系型数据库的典型数据结构就是数据表，这些数据表的组成都是结构化的（Structured）。你可以把关系模型理解成一个二维表格模型，这个二维表格是由行（row）和列（column）组成的。每一个行（row）就是一条数据，每一列（column）就是数据在某一维度的属性。

正是因为在数据库中，表的组成是基于关系模型的，所以一个表就是一个关系。一个数据库中可以包括多个表，也就是存在多种数据之间的关系。而我们之所以能使用SQL语言对各个数据表进行复杂查询，核心就在于连接，它可以用一条SELECT语句在多张表之间进行查询。你也可以理解为，关系型数据库的核心之一就是连接。

既然连接在SQL中这么重要，那么针对今天的内容，需要你从以下几个方面进行掌握：

1. SQL实际上存在不同的标准，不同标准下的连接定义也有不同。你首先需要了解常用的SQL标准有哪些；
2. 了解了SQL的标准之后，我们从SQL92标准入门，来看下连接表的种类有哪些；
3. 针对一个实际的数据库表，如果你想要做数据统计，需要学会使用跨表的连接进行操作。
<div><strong>精选留言（30）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/10/0c/0f/93d1c8eb.jpg" width="30px"><span>mickey</span> 👍（102） 💬（12）<div>&#47;*
team 表做一道动手题，表格中一共有 3 支球队，现在这 3 支球队需要进行比赛，请用一条 SQL 语句显示出所有可能的比赛组合。
*&#47;
#分主客队
SELECT CONCAT(kedui.team_name, &#39; VS &#39;, zhudui.team_name) as &#39;客队 VS 主队&#39; FROM team as zhudui LEFT JOIN team as kedui on zhudui.team_id&lt;&gt;kedui.team_id;

客队 VS 主队
------------------------------------
底特律活塞 VS 印第安纳步行者
底特律活塞 VS 亚特兰大老鹰
印第安纳步行者 VS 底特律活塞
印第安纳步行者 VS 亚特兰大老鹰
亚特兰大老鹰 VS 底特律活塞
亚特兰大老鹰 VS 印第安纳步行者

#不分主客队
SELECT a.team_name as &#39;队伍1&#39; ,&#39;VS&#39; , b.team_name as &#39;队伍2&#39; FROM team as a ,team as b where a.team_id&lt;b.team_id;

队伍1    VS    队伍2
------------------------------------
底特律活塞	VS	印第安纳步行者
底特律活塞	VS	亚特兰大老鹰
印第安纳步行者	VS	亚特兰大老鹰</div>2019-07-03</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/57/4f/6fb51ff1.jpg" width="30px"><span>奕</span> 👍（26） 💬（2）<div>有两个问题：
1: 在进行连接查询的时候，查询的顺序是什么呢？ 是先进行笛卡尔积在进行条件条件筛选吗？
2: 在进行连接查询的时候 on 中的条件和 where 中的条件有什么区别呢？ 这两个的筛选顺序一样吗？</div>2019-07-05</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/1b/4d/bf34b774.jpg" width="30px"><span>长安落雪</span> 👍（22） 💬（1）<div>SELECT t1.team_name,t2.team_name FROM team as t1 LEFT  JOIN team as t2 ON t1.team_id  != t2.team_id

SELECT t1.team_name , t2.team_name  FROM team as t1 ,team as t2 where t1.team_id&lt;t2.team_id;</div>2019-07-04</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/18/32/82/273a44cd.jpg" width="30px"><span>圆子蛋</span> 👍（5） 💬（3）<div>三队对阵的可能组合：
SELECT * FROM team AS a,team AS b WHERE a.team_id &lt; b.team_id
主客场对阵的可能（只列出名字的话是不是可以这样？）
SELECT a.team_name as 主场,b.team_name as 客场 FROM team AS a,team AS b WHERE a.team_id != b.team_id</div>2019-07-03</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/18/00/23/17868694.jpg" width="30px"><span>Samson</span> 👍（4） 💬（3）<div>SQL：SELECT p.player_name, p.height, h.height_level
FROM player AS p, height_grades AS h
WHERE p.height BETWEEN h.height_lowest AND h.height_highest
 

老师，我还是不能够理解这条语句中WHERE之后的部分，可以麻烦详加解释一番吗？

另外，对于外连接的两个例子，可以把已经结果也贴一下吗？感觉这样子下效果会更好</div>2019-07-05</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/40/d8/69722032.jpg" width="30px"><span>野马</span> 👍（4） 💬（1）<div>那一个RDBMS支持多个SQL标准吗？</div>2019-07-04</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/75/9b/611e74ab.jpg" width="30px"><span>技术修行者</span> 👍（3） 💬（1）<div>目前主流的DNMS应该都是按照SQL99的规定来设计连接操作的，在实际工作中，极少看到SAL语句中带+的情况。我的建议是在介绍了基本概念后，可以直接使用SAL99，这样更有利于实战。</div>2019-10-02</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/aa/a3/0b7f0334.jpg" width="30px"><span>太精</span> 👍（3） 💬（1）<div>select * from team as a, team as b where a.team_id != b.team_id;
+---------+-----------------------+---------+-----------------------+
| team_id | team_name             | team_id | team_name             |
+---------+-----------------------+---------+-----------------------+
|    1002 | 印第安纳步行者        |    1001 | 底特律活塞            |
|    1003 | 亚特兰大老鹰          |    1001 | 底特律活塞            |
|    1001 | 底特律活塞            |    1002 | 印第安纳步行者        |
|    1003 | 亚特兰大老鹰          |    1002 | 印第安纳步行者        |
|    1001 | 底特律活塞            |    1003 | 亚特兰大老鹰          |
|    1002 | 印第安纳步行者        |    1003 | 亚特兰大老鹰          |
+---------+-----------------------+---------+-----------------------+
</div>2019-07-04</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/OrfXQWvE0jIuibibw0dnicPM0iaRPXyyGTPicFfmvykUNiaVT7E8PQeqhzct4HhtdnSZvZdPzHmknIv56icPtYOD6Fibsw/132" width="30px"><span>xy</span> 👍（2） 💬（2）<div>表怎么下载下来的？</div>2019-07-15</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/f1/84/7d21bd9e.jpg" width="30px"><span>Goal</span> 👍（2） 💬（1）<div>老师好，
1. 文中“等值连接” 的结果图配错了，此处应该是只有：底特律活塞、印第安纳步行者的37名成员的表；
2. 思考题，主客场共计6场比赛
SELECT a.team_name,b.team_name  from team a,team b WHERE a.team_id != b.team_id
SELECT a.team_name,b.team_name FROM team a JOIN team b WHERE a.team_name &lt;&gt; b.team_name</div>2019-07-03</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/90/4e/efaea936.jpg" width="30px"><span>墨禾</span> 👍（1） 💬（1）<div>&#47;*等值连接:两张表存在相同的列属性*&#47;
SELECT player_id, player.team_id, player_name, height, team_name FROM player, team WHERE player.team_id = team.team_id;

&#47;*非等值连接*&#47;
SELECT p.player_name, p.height...

极客时间版权所有: https:&#47;&#47;time.geekbang.org&#47;column&#47;article&#47;104637


&#47;*外连接：包括左连接、右连接、全连接*&#47;
-- 左外连接：左边的表为主表
 select count(*) from team t left outer join player p  on t.team_id = p.team_id;
 &#47;*
1001	底特律活塞	10001	1001	韦恩-艾灵顿	1.93
1001	底特律活塞	10002	1001	雷吉-杰克逊	1.91
1002	印第安纳步行者	10037	1002	Ike Anigbogu	2.08
1003	亚特兰大老鹰				
*&#47;
-- 右外连接：右边的表为主表
select count(*) from team t RIGHT outer join player p  on t.team_id = p.team_id;
&#47;*
1001	底特律活塞	10001	1001	韦恩-艾灵顿	1.93
1001	底特律活塞	10002	1001	雷吉-杰克逊	1.91
1002	印第安纳步行者	10037	1002	Ike Anigbogu	2.08
1003	亚特兰大老鹰				
*&#47;

-- 全连接：两张表做笛卡尔积
select count(*) from team t  outer join player p  on t.team_id = p.team_id;
&#47;*
1001	底特律活塞	10001	1001	韦恩-艾灵顿	1.93
1001	底特律活塞	10002	1001	雷吉-杰克逊	1.91
1002	印第安纳步行者	10037	1002	Ike Anigbogu	2.08
1003	亚特兰大老鹰				
*&#47;


select count(*) from team t  inner join player p  on t.team_id = p.team_id;


-- 自连接：可对单表或多表进行操作
SELECT b.player_name, b.height FROM player as a , player as b WHERE a.player_name = &#39;布雷克 - 格里芬&#39; and a.height &lt; b.height

&#47;*请用一条 SQL 语句显示出所有可能的比赛组合*&#47;
SELECT * FROM team t1 , team t2 WHERE t1.team_id&lt;&gt; t2.team_id
-- 或
SELECT * FROM team t1 , team t2 WHERE t1.team_id !=t2.team_id</div>2019-07-03</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/AGicQgKibwja1SxkQ7oXQE8hYH7yCpiaicNHw3qZRuNB81aVDOQm9P1zd5F75Jbtv66G15D6ZjbbqfnoETR4321Zdw/132" width="30px"><span>高泽林</span> 👍（0） 💬（1）<div>要实际验证一下！</div>2019-12-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/3b/fc/04a75cd0.jpg" width="30px"><span>taoist</span> 👍（0） 💬（1）<div>-- MariaDB

-- 主客
SELECT CONCAT( t1.team_name ,&#39;(主)－－－－（客）&#39;, t2.team_name) FROM team t1, team t2
WHERE t1.team_id != t2.team_id;


-- 不分主客
SELECT CONCAT( t1.team_name ,&#39;－－－－&#39;, t2.team_name) FROM team t1, team t2
WHERE t1.team_id &lt; t2.team_id;</div>2019-12-16</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/19/69/bf/58f70a2a.jpg" width="30px"><span>程序员花卷</span> 👍（0） 💬（1）<div>外连接不仅可以返回符合条件的行，还可以返回一些不符合条件的行
内连接只能返回符合条件的行，不能返回不符合条件的行
自连接自己连接自己，查询的时候用到了自己的字段，也可以多表进行连接

学习这一节我觉得重点在于理解连接是如何进行的，区分清楚各个连接查询的主表和从表
想要很深刻的理解，还是需要多做题目

练习题
SQL语句
SELECT a.`team_name` AS 主队,b.team_name AS 客队
FROM team AS a,team AS b
WHERE a.`team_id` &lt; b.`team_id`;

</div>2019-12-06</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/QD6bf8hkS5dHrabdW7M7Oo9An1Oo3QSxqoySJMDh7GTraxFRX77VZ2HZ13x3R4EVYddIGXicRRDAc7V9z5cLDlA/132" width="30px"><span>爬行的蜗牛</span> 👍（0） 💬（1）<div>SELECT * FROM team as a, team as b WHERE a.team_name != b.team_name;</div>2019-11-23</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTIF4hVQibicU336icg4zJ1ia5iaT5almR5EE99EjgiazFu37CnJLLL2KibvOiaC6jEWroaJJqTKfW6B3TXKRQ/132" width="30px"><span>凌晨四点半</span> 👍（0） 💬（1）<div>为什么代码不能显示多行？每次我都需要把代码复制到记事本上看，直接在网页上还需要拖着才能看全局。</div>2019-11-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/2e/74/88c613e0.jpg" width="30px"><span>扶幽</span> 👍（0） 💬（1）<div>作业：
SELECT a.team_name, b.team_name 
FROM team AS a, team AS b 
WHERE a.team_name&lt;&gt;b.team_name;</div>2019-10-27</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/NFpgmsqvyPs8ibTrrrJ24OqoISOVW2aaYESotwl5r5PqhyLuECj6gvJN9SibECg142eyW5S9mebZGdyGzMWS1VtQ/132" width="30px"><span>chenysh38</span> 👍（0） 💬（1）<div>mysql&gt; select a.team_name as team1, b.team_name as team2
    -&gt; from team as a, team as b
    -&gt; where (
    -&gt; select distinct a.team_id - b.team_id
    -&gt; ) &gt; 0;
+----------------+----------------+
| team1          | team2          |
+----------------+----------------+
| 印第安纳步行者 | 底特律活塞     |
| 亚特兰大老鹰   | 底特律活塞     |
| 亚特兰大老鹰   | 印第安纳步行者 |
+----------------+----------------+
3 rows in set (0.02 sec)</div>2019-09-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/e1/1a/20977779.jpg" width="30px"><span>峻铭</span> 👍（0） 💬（1）<div>select * from team as a inner join team as b where a.team_id!=b.team_id and a.team_id &gt; b.team_id;</div>2019-09-04</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/e6/68/1871d6ba.jpg" width="30px"><span>海洋</span> 👍（0） 💬（1）<div>mysql&gt; SELECT * FROM team host LEFT JOIN team guest ON host.team_id &lt;&gt; guest.team_id;
+---------+----------------+---------+----------------+
| team_id | team_name      | team_id | team_name      |
+---------+----------------+---------+----------------+
|    1002 | 印第安纳步行者 |    1001 | 底特律活塞     |
|    1003 | 亚特兰大老鹰   |    1001 | 底特律活塞     |
|    1001 | 底特律活塞     |    1002 | 印第安纳步行者 |
|    1003 | 亚特兰大老鹰   |    1002 | 印第安纳步行者 |
|    1001 | 底特律活塞     |    1003 | 亚特兰大老鹰   |
|    1002 | 印第安纳步行者 |    1003 | 亚特兰大老鹰   |
+---------+----------------+---------+----------------+
6 rows in set (0.14 sec)

mysql&gt; SELECT a.team_name as &#39;队伍1&#39;,&#39;VS&#39;, b.team_name as &#39;队伍2&#39; FROM team a, team b WHERE a.team_id &lt; b.team_id;
+----------------+----+----------------+
| 队伍1          | VS | 队伍2          |
+----------------+----+----------------+
| 底特律活塞     | VS | 印第安纳步行者 |
| 底特律活塞     | VS | 亚特兰大老鹰   |
| 印第安纳步行者 | VS | 亚特兰大老鹰   |
+----------------+----+----------------+
3 rows in set (0.07 sec)

mysql&gt; SELECT CONCAT(a.team_name, &#39;VS&#39;, b.team_name) as &#39;主队 VS 客队&#39; FROM team a LEFT JOIN team b ON a.team_id &lt;&gt; b.team_id;
+------------------------------+
| 主队 VS 客队                 |
+------------------------------+
| 印第安纳步行者VS底特律活塞   |
| 亚特兰大老鹰VS底特律活塞     |
| 底特律活塞VS印第安纳步行者   |
| 亚特兰大老鹰VS印第安纳步行者 |
| 底特律活塞VS亚特兰大老鹰     |
| 印第安纳步行者VS亚特兰大老鹰 |
+------------------------------+
6 rows in set (0.07 sec)</div>2019-08-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/1c/c2/adba355c.jpg" width="30px"><span>王之刚</span> 👍（0） 💬（1）<div>请问老师，关于sql中使用str-to-date函数的问题，比如有个表里有个date类型的字段x，我查询条件需要比较时间，where条件是x&gt;str-to-date（&#39;20190808080802&#39;,时间格式），但我发现不用str-to-date函数，查询条件为x&gt;&#39;20190808080802&#39; 一样是同样的效果，请问where条件里str-to-date函数是否一定需要呢？带和不带这个函数有什么区别呢，谢谢了</div>2019-08-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/d6/fa/1f5bf642.jpg" width="30px"><span>未来的胡先森</span> 👍（0） 💬（1）<div>SELECT t1.`team_name` AS &#39;主队&#39;,t2.`team_name` AS &#39;客队&#39;
FROM team t1,team t2
WHERE t1.`team_id`!=t2.`team_id`;
做 team*team 的笛卡尔积，即列出所有的排列组合，取出比赛的两只队尾是同一只的情况</div>2019-08-06</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/b5/98/ffaf2aca.jpg" width="30px"><span>Ronnyz</span> 👍（0） 💬（1）<div>作业：
SELECT a.team_name AS &#39;主队&#39;, b.team_name AS &#39;客队&#39; FROM team AS a LEFT JOIN team AS b ON a.team_name!=b.team_name;
我觉得自连接查询有点像子查询啊，比如查看比布雷克-格里芬高的球员：
SELECT player_name, height FROM player WHERE height &gt; (SELECT height FROM player WHERE player_name=&#39;布雷克-格里芬&#39;);</div>2019-07-22</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTIR9QrAn9TZOrJMSYMyN96PAuAjETVrN5SPp3hMbfUAGIWtHceWPEoQtPdXeuBn7VB7dagtxynAIA/132" width="30px"><span>ballgod</span> 👍（0） 💬（1）<div>符号明白了，请问评论第一个中left  join是否可以换成where。 另外，能不能添加评论管理的功能，上一个评论的问题理解了，想要删掉。</div>2019-07-20</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTIR9QrAn9TZOrJMSYMyN96PAuAjETVrN5SPp3hMbfUAGIWtHceWPEoQtPdXeuBn7VB7dagtxynAIA/132" width="30px"><span>ballgod</span> 👍（0） 💬（2）<div>有点没明白为什么，为什么分主客队用0不等于，不分主客队用小于，希望解释一下，谢谢</div>2019-07-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/49/f6/ef3e5c81.jpg" width="30px"><span>shengsheng</span> 👍（0） 💬（1）<div>解释得很到位，理解得比较好</div>2019-07-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/ba/fc/8391cf28.jpg" width="30px"><span>mick</span> 👍（0） 💬（1）<div>老师，关于一个数据库管理系统，支持什么什么标准的sql，有没有可考究的资料，还是必须得去尝试</div>2019-07-18</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/fUDCLLob6DFS8kZcMUfxOc4qQHeQfW4rIMK5Ty2u2AqLemcdhVRw7byx85HrVicSvy5AiabE0YGMj5gVt8ibgrusA/132" width="30px"><span>NO.9</span> 👍（0） 💬（1）<div>select t1.team_name,&#39; VS &#39; VS, t2.team_name 
	from HERO2019.team as t1 , HERO2019.team as t2 
	where t1.team_id != t2.team_id ORDER By t1.team_name;
-----------------------------------------------
&#39;亚特兰大老鹰&#39;, &#39; VS &#39;, &#39;底特律活塞&#39;
&#39;亚特兰大老鹰&#39;, &#39; VS &#39;, &#39;印第安纳步行者&#39;
&#39;印第安纳步行者&#39;, &#39; VS &#39;, &#39;底特律活塞&#39;
&#39;印第安纳步行者&#39;, &#39; VS &#39;, &#39;亚特兰大老鹰&#39;
&#39;底特律活塞&#39;, &#39; VS &#39;, &#39;印第安纳步行者&#39;
&#39;底特律活塞&#39;, &#39; VS &#39;, &#39;亚特兰大老鹰&#39;</div>2019-07-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/02/57/9b235866.jpg" width="30px"><span>2525</span> 👍（0） 💬（1）<div>作业：mysql
SELECT
	a.team_name,
	&#39;vs&#39;,
	b.team_name
FROM
	team AS a,
	team AS b
WHERE
	a.team_id &lt; b.team_id;

SELECT
	*
FROM
	team AS t1
RIGHT JOIN team AS t2 ON t1.team_id != t2.team_id</div>2019-07-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/e2/bd/b65420ae.jpg" width="30px"><span>leol</span> 👍（0） 💬（1）<div>select * from team t1,team t2 where t1.team_id&lt;&gt;t2.team_id;</div>2019-07-10</li><br/>
</ul>