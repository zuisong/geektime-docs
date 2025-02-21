今天我们主要学习如何使用SQL检索数据。如果你已经有了一定的SQL基础，这节课可以跳过，也可以把它当做是个快速的复习。

SELECT可以说是SQL中最常用的语句了。你可以把SQL语句看作是英语语句，SELECT就是SQL中的关键字之一，除了SELECT之外，还有INSERT、DELETE、UPDATE等关键字，这些关键字是SQL的保留字，这样可以很方便地帮助我们分析理解SQL语句。我们在定义数据库表名、字段名和变量名时，要尽量避免使用这些保留字。

SELECT的作用是从一个表或多个表中检索出想要的数据行。今天我主要讲解SELECT的基础查询，后面我会讲解如何通过多个表的连接操作进行复杂的查询。

在这篇文章中，你需要重点掌握以下几方面的内容：

1. SELECT查询的基础语法；
2. 如何排序检索数据；
3. 什么情况下用`SELECT*`，如何提升SELECT查询效率？

## SELECT查询的基础语法

SELECT可以帮助我们从一个表或多个表中进行数据查询。我们知道一个数据表是由列（字段名）和行（数据行）组成的，我们要返回满足条件的数据行，就需要在SELECT后面加上我们想要查询的列名，可以是一列，也可以是多个列。如果你不知道所有列名都有什么，也可以检索所有列。
<div><strong>精选留言（30）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/10/ce/60/7d17522d.jpg" width="30px"><span>君莫惜</span> 👍（171） 💬（4）<div>SELECT COUNT(*)  ＞ SELECT COUNT(1) ＞ SELECT COUNT(具体字段)

之前看到的，好像Mysql对count(*)做了单独的优化</div>2019-06-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/59/18/f9ee3c42.jpg" width="30px"><span>C先生丶陈</span> 👍（24） 💬（4）<div>做一个搬运工，下面是从老师GitHub上找到的建表语句：
SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
-- Table structure for heros
-- ----------------------------
DROP TABLE IF EXISTS `heros`;
CREATE TABLE `heros`  (
  `name` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `hp_max` float NULL DEFAULT NULL,
  `hp_growth` float NULL DEFAULT NULL,
  `hp_start` float NULL DEFAULT NULL,
  `mp_max` float NULL DEFAULT NULL,
  `mp_growth` float NULL DEFAULT NULL,
  `mp_start` float NULL DEFAULT NULL,
  `attack_max` float NULL DEFAULT NULL,
  `attack_growth` float NULL DEFAULT NULL,
  `attack_start` float NULL DEFAULT NULL,
  `defense_max` float NULL DEFAULT NULL,
  `defense_growth` float NULL DEFAULT NULL,
  `defense_start` float NULL DEFAULT NULL,
  `hp_5s_max` float NULL DEFAULT NULL,
  `hp_5s_growth` float NULL DEFAULT NULL,
  `hp_5s_start` float NULL DEFAULT NULL,
  `mp_5s_max` float NULL DEFAULT NULL,
  `mp_5s_growth` float NULL DEFAULT NULL,
  `mp_5s_start` float NULL DEFAULT NULL,
  `attack_speed_max` float NULL DEFAULT NULL,
  `attack_range` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
  `role_main` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
  `role_assist` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
  `birthdate` datetime(0) NULL DEFAULT NULL,
  PRIMARY KEY (`name`) USING BTREE
) ENGINE = InnoDB CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Dynamic;
</div>2019-06-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/32/b5/7f1e4280.jpg" width="30px"><span>Shame</span> 👍（108） 💬（9）<div>先交作业 select name,mp_max from heros order by hp_max desc limit 5;
 然后就是楼下一个同学问的问题，我也有些疑惑，就是这个
SELECT DISTINCT player_id, player_name, count(*) as num # 顺序 5
FROM player JOIN team ON player.team_id = team.team_id # 顺序 1
WHERE height &gt; 1.80 # 顺序 2
GROUP BY player.team_id # 顺序 3
HAVING num &gt; 2 # 顺序 4
ORDER BY num DESC # 顺序 6
LIMIT 2 # 顺序 7

对于这个语句，我还有一点疑问：既然HAVING的执行是在SELECT之前的，那么按理说在执行HAVING的时候SELECT中的count(*)应该还没有被计算出来才对啊，为什么在HAVING中就直接使用了num&gt;2这个条件呢？
希望老师百忙之中能抽空帮忙解释一下，谢谢老师</div>2019-06-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/18/00/23/17868694.jpg" width="30px"><span>Samson</span> 👍（23） 💬（1）<div>老师，可以说下SELECT语句执行原理那个视例中HAVING关键字的作用嘛？</div>2019-06-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/fc/90/c9df0459.jpg" width="30px"><span>ack</span> 👍（20） 💬（6）<div>老师好，请问能把建表的sql给出来吗？</div>2019-06-21</li><br/><li><img src="" width="30px"><span>lincan</span> 👍（18） 💬（4）<div>老师讲得很棒，但有一处困惑：limit是最后执行的话，执行limit时全表扫描和所有的虚拟表都已生成了，那使用limit为什么还能提高效率呢？</div>2019-09-01</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/0f/71/9273e8a4.jpg" width="30px"><span>时间是最真的答案</span> 👍（16） 💬（4）<div>MySQL
SELECT `name`,mp_max FROM heros ORDER BY hp_max DESC LIMIT 5 </div>2019-06-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/f1/15/8fcf8038.jpg" width="30px"><span>William</span> 👍（7） 💬（1）<div>前端开发第一次接触数据库。
1. 请问老师Mac上安装MySQL，安装8.0版本还是5.7版本更好？
2. 是否需要安装Navicat，PostgreSQL？
</div>2019-07-11</li><br/><li><img src="" width="30px"><span>hlz-123</span> 👍（7） 💬（1）<div>数据库，MySQL8.0
SELECT name as &#39;姓名&#39;,mp_max as &#39;最大法力&#39; FROM heros ORDER BY hp_max LIMIT 5;</div>2019-06-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/30/8a/b5ca7286.jpg" width="30px"><span>业余草</span> 👍（6） 💬（2）<div>create table 还没学吧，我是小白，教一下 create table 或者 create table like。就单拿 select 说，这章内容也不全啊，group，having 等都漏掉了</div>2019-06-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/4a/2c/f8451d77.jpg" width="30px"><span>石维康</span> 👍（6） 💬（3）<div>作业: SELECT name, mp_max FROM heros ORDER BY hp_max DESC  LIMIT 5;
MySQL数据库</div>2019-06-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/7f/0c/2ebdc487.jpg" width="30px"><span>魔兽rpg足球</span> 👍（4） 💬（3）<div>老师 我有一个疑问  场景是这样的，我有三张表，一张表存储文章posts，一张表存储文章标签tags，

一篇文章可以有多个标签，一个标签可以被多个文章拥有，文章和标签是多对多的关系，

此时我又增加了一个关系表post_tag,这个表只有两个字段，post_id和tag_id.

我现在有一个需求 查询出所有文章，查询出的文章数据中每篇文章都有一个tags属性，这个属性包含所有这篇文章的标签信息，这个查询应该怎么做呢？ 或者说sql只能做一部分，然后在通过其他脚本语言再处理呢？

我将问题发在了 segmentfaul 链接地址 https:&#47;&#47;segmentfault.com&#47;q&#47;1010000019472412</div>2019-06-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/10/61/7ba48062.jpg" width="30px"><span>菜鸡小王子</span> 👍（4） 💬（2）<div>希望老师在讲select的基础语法时  能稍微带一点底层原理啦 比如select的执行顺序  这样理解是不是可以更加透彻一点</div>2019-06-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/0c/0f/93d1c8eb.jpg" width="30px"><span>mickey</span> 👍（3） 💬（2）<div>建表语句没有给出。</div>2019-06-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/a0/3f/06b690ba.jpg" width="30px"><span>刘桢</span> 👍（3） 💬（1）<div>北邮倒计时186天</div>2019-06-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/d5/86/5b1ff7d9.jpg" width="30px"><span>Fan</span> 👍（2） 💬（1）<div>写 SQL 语句，对英雄名称和最大法力进行查询，按照最大生命从高到低排序，只返回 5 条记录即可.

SELECT name, max_mp FROM heros ORDER BY max_hp LIMIT 5;</div>2019-08-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/e6/68/1871d6ba.jpg" width="30px"><span>海洋</span> 👍（2） 💬（2）<div>作业：
SELECT name,mp_max FROM heros ORDER BY hp_max DESC LIMIT 5;</div>2019-08-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/48/f3/65c7e3ef.jpg" width="30px"><span>cricket1981</span> 👍（2） 💬（1）<div>mysql&gt; SELECT name, mp_max FROM heros ORDER BY hp_max DESC LIMIT 5;
+-----------+--------+
| name      | mp_max |
+-----------+--------+
| 廉颇      |   1708 |
| 白起      |   1666 |
| 程咬金    |      0 |
| 刘禅      |   1694 |
| 牛魔      |   1926 |
+-----------+--------+
5 rows in set (0.00 sec)
</div>2019-06-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/17/41/af/e5629318.jpg" width="30px"><span>꯭J꯭I꯭N꯭🙃</span> 👍（2） 💬（1）<div>SELECT name, mp_max FROM heros ORDER BY hp_max ASC LIMIT 5;</div>2019-06-25</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/87/f8/eb29ac28.jpg" width="30px"><span>New Youth</span> 👍（2） 💬（2）<div>同求建表语句 emmmm</div>2019-06-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/17/fd/ad/c0cfc767.jpg" width="30px"><span>Zero白</span> 👍（0） 💬（1）<div>这节也是收获的季节  (●ˇ∀ˇ●)</div>2020-03-29</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/AGicQgKibwja1SxkQ7oXQE8hYH7yCpiaicNHw3qZRuNB81aVDOQm9P1zd5F75Jbtv66G15D6ZjbbqfnoETR4321Zdw/132" width="30px"><span>高泽林</span> 👍（0） 💬（1）<div>select name,mp_max from heros order by hp_max desc limit 5;</div>2019-12-13</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/QD6bf8hkS5dHrabdW7M7Oo9An1Oo3QSxqoySJMDh7GTraxFRX77VZ2HZ13x3R4EVYddIGXicRRDAc7V9z5cLDlA/132" width="30px"><span>爬行的蜗牛</span> 👍（0） 💬（1）<div>SELECT name, mp_max
FROM heros
ORDER BY hp_max DESC
 LIMIT 5;</div>2019-12-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/3b/fc/04a75cd0.jpg" width="30px"><span>taoist</span> 👍（0） 💬（1）<div>MariaDB:
select name, mp_max from heros order by hp_max desc limit 5;
</div>2019-12-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/88/8d/0cf741d3.jpg" width="30px"><span>Simon</span> 👍（0） 💬（1）<div>MySQL数据库：
SELECT 
	`name` as &#39;姓名&#39;,
	`hp_max` as &#39;最大生命值&#39;,
	`mp_max` as &#39;法力最大值&#39;
FROM `heros`
ORDER BY `hp_max` asc 
LiMIT 5;</div>2019-12-07</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1a/9d/dd/c154d593.jpg" width="30px"><span>小凡</span> 👍（0） 💬（1）<div>我使用的是DBMS是SQL Server2008 
SELECT TOP 5 name,mp_max FROM hero ORDER BY hp_max   DESC </div>2019-11-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/61/66/ea3f7035.jpg" width="30px"><span>dusthui</span> 👍（0） 💬（1）<div>### 子查询
select  hero_name,max uo 
from(
	select  hero_name,max uo 
​			from heros
​			order by max_life desc
	)
limit 5;</div>2019-10-15</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTKELX1Rd1vmLRWibHib8P95NA87F4zcj8GrHKYQL2RcLDVnxNy1ia2geTWgW6L2pWn2kazrPNZMRVrIg/132" width="30px"><span>jxs1211</span> 👍（0） 💬（1）<div>SELECT name, hp_max FROM heroes ORDER BY mp_max DESC LIMIT 5</div>2019-10-05</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/4c/4e/91267714.jpg" width="30px"><span>Cola_</span> 👍（0） 💬（1）<div>select name,mp_max from heros order by hp_max desc limit 5;
mysql</div>2019-09-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/ea/46/9c9808a9.jpg" width="30px"><span>Serendipity</span> 👍（0） 💬（1）<div>SELECT name, mp_max FROM heros ORDER BY hp_max DESC LIMIT 5
</div>2019-08-27</li><br/>
</ul>