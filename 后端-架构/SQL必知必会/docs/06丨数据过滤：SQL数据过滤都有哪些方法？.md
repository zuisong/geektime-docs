我在上篇文章中讲到过，提升查询效率的一个很重要的方式，就是约束返回结果的数量，还有一个很有效的方式，就是指定筛选条件，进行过滤。过滤可以筛选符合条件的结果，并进行返回，减少不必要的数据行。

那么在今天的内容里，我们来学习如何对SQL数据进行过滤，这里主要使用的就是WHERE子句。

你可能已经使用过WHERE子句，说起来SQL其实很简单，只要能把满足条件的内容筛选出来即可，但在实际使用过程中，不同人写出来的WHERE子句存在很大差别，比如执行效率的高低，有没有遇到莫名的报错等。

在今天的学习中，你重点需要掌握以下几方面的内容：

1. 学会使用WHERE子句，如何使用比较运算符对字段的数值进行比较筛选；
2. 如何使用逻辑运算符，进行多条件的过滤；
3. 学会使用通配符对数据条件进行复杂过滤。

## 比较运算符

在SQL中，我们可以使用WHERE子句对条件进行筛选，在此之前，你需要了解WHERE子句中的比较运算符。这些比较运算符的含义你可以参见下面这张表格：

![](https://static001.geekbang.org/resource/image/3a/e0/3a2667784b4887ef15becc7056f3d3e0.png?wh=799%2A545)

实际上你能看到，同样的含义可能会有多种表达方式，比如小于等于，可以是（&lt;=），也可以是不大于（!&gt;）。同样不等于，可以用（&lt;&gt;），也可以用（!=），它们的含义都是相同的，但这些符号的顺序都不能颠倒，比如你不能写（=&lt;）。需要注意的是，你需要查看使用的DBMS是否支持，不同的DBMS支持的运算符可能是不同的，比如Access不支持（!=），不等于应该使用（&lt;&gt;）。在MySQL中，不支持（!&gt;）（!&lt;）等。
<div><strong>精选留言（30）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/0f/57/4f/6fb51ff1.jpg" width="30px"><span>奕</span> 👍（106） 💬（5）<div>就是要避免全表扫描，所以我们会考虑在 WHERE 及 ORDER BY 涉及到的列上增加索引
-----------------------------------------------
where 条件字段上加索引是可以明白的，但是为什么 order by 字段上还要加索引呢？这个时候已经通过 where条件过滤得到了数据，已经不需要在筛选过滤数据了，只需要在排序的时候根据字段排序就好了。不是很明白</div>2019-06-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/6a/a1/6270eeb7.jpg" width="30px"><span>极客星星</span> 👍（57） 💬（1）<div>你好  老师 不是很明白您说的对where语句建索引是什么意思 通过sql语句怎么实现
谢谢</div>2019-06-25</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/64/29/da537902.jpg" width="30px"><span>Abyssknight</span> 👍（35） 💬（6）<div>关于通配符匹配里的 % 相当于正则表达式里的 .* 表示匹配大于等于0个任意字符，
所以  % 太 % 匹配的是 [大于等于0个任意字符]太[大于等于0个任意字符]，[东皇]太[一] 和 []太[乙真人]都符合；
而 _% 相当于正则表达式里的 .+ 表示匹配至少一个，即大于等于1个，
所以  &#39;_% 太 % 匹配的是 [大于等于1个字符]太[大于等于0个字符]，只有 [东皇]太[一] 符合。</div>2019-06-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/9a/64/eea9aa33.jpg" width="30px"><span>陈扬鸿</span> 👍（33） 💬（1）<div>老师，你好，现在mysql8已经没有frm文件，一旦数据字典丢失，没有表结构就无法恢复单个ibd文件的数据，如何通过mysql8的 sdi文件生成创建表的ddl语句。</div>2019-06-25</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/78/9c/5780b1de.jpg" width="30px"><span>怪兽宇</span> 👍（32） 💬（7）<div>老师好, 平日因业务考核需要，一条查询语句查询条件需要写 30 多个 like &quot;%A%&quot;  ，语句跑起来特别慢，请问有什么优化方法吗？</div>2019-06-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/f1/84/7d21bd9e.jpg" width="30px"><span>Goal</span> 👍（26） 💬（3）<div>老师关于通配符给的解释，不够清晰！
说明如下：
SQL：SELECT name FROM heros WHERE name LIKE &#39;_% 太 %&#39;

因为太乙真人的太是第一个字符，而_%太%中的太不是在第一个字符，所以匹配不到“太乙真人”，只可以匹配上“东皇太一”。

说明：
&quot;_&quot;：匹配任意一个字符，包括可以匹配到“太乙真人”的太字。 
但是，整体的通配符  &#39;_% 太 %&#39;，需要后面继续匹配到一个&quot;太&quot;字符，显然，&quot;太乙真人&quot;不符合了，如果是，&quot;太乙真人太太&quot;，就可以匹配到。</div>2019-06-24</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/DYAIOgq83epGMibYc0m7cDGC8CyCIwXynpzicpeAo6pJ8mLWxI3LxTLyaj2QLMg9Ea1M7KMWw4B9wbMfRJIs3vbg/132" width="30px"><span>stormsc</span> 👍（23） 💬（2）<div>有个问题想问老师：
SELECT name,role_main,role_assist from heros where role_assist is not null LIMIT 5 
这样限定的查询结果为5条数据，是随机选择的5条数据吗？</div>2019-06-25</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/5c/3f/34e5c750.jpg" width="30px"><span>看，有只猪</span> 👍（20） 💬（3）<div>解答一下对使用DATE函数的疑问：
birthdate字段可能会有时间包含在里面，如2019-01-01 00:00:00，如果直接和2019-01-01比较是会失败的，用DATE函数可以提取出原始数据的日期部分</div>2019-06-25</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/DYAIOgq83epGMibYc0m7cDGC8CyCIwXynpzicpeAo6pJ8mLWxI3LxTLyaj2QLMg9Ea1M7KMWw4B9wbMfRJIs3vbg/132" width="30px"><span>stormsc</span> 👍（11） 💬（4）<div>作业 mysql: select name 英雄名称, role_main 主要定位, role_assist 次要定位,hp_max 最大生命值,mp_max 最大法力值 from heros where (role_main in (&#39;坦克&#39;,&#39;战士&#39;) 
AND role_assist is not null) AND (hp_max &gt; 8000 or mp_max &lt;1500) ORDER BY (hp_max+mp_max) DESC</div>2019-06-25</li><br/><li><img src="" width="30px"><span>hlz-123</span> 👍（9） 💬（1）<div>where子句WHERE 子句中比较运算符、逻辑运算符和通配符这三者各自作用？
1、比较运算符，比较数值的大小，数值类型可以是整数，浮点数，字符串，布尔类型等等。
2、逻辑运算符，定义where子句中多个条件之间的关系。
3、通配符，对文本类型字段进行模糊查询。
Mysql查询语句：
SELECT name,role_main,role_assist,hp_max,mp_max FROM heros 
WHERE (role_main in (&#39;坦克&#39;,&#39;战士&#39;) AND role_assist is not null) 
AND (hp_max&gt;8000 OR mp_max&lt;1500) order by (hp_max+mp_max) DESC;</div>2019-06-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/1e/02/2864e0f2.jpg" width="30px"><span>华夏</span> 👍（5） 💬（3）<div>SELECT name, role_main, role_assist, hp_max, mp_max 
FROM heros 
WHERE (role_main IN (&#39;坦克&#39;, &#39;战士&#39;) AND role_assist IS NOT NULL) 
AND (hp_max &gt; 8000 OR mp_max &lt; 1500) 
ORDER BY (hp_max+mp_max) DESC;
+-----------+-----------+-------------+--------+--------+
| name      | role_main | role_assist | hp_max | mp_max |
+-----------+-----------+-------------+--------+--------+
| 牛魔      | 坦克      | 辅助        |   8476 |   1926 |
| 刘邦      | 坦克      | 辅助        |   8073 |   1940 |
| 程咬金    | 坦克      | 战士        |   8611 |      0 |
| 张飞      | 坦克      | 辅助        |   8341 |    100 |
| 亚瑟      | 战士      | 坦克        |   8050 |      0 |
| 吕布      | 战士      | 坦克        |   7344 |      0 |
| 关羽      | 战士      | 坦克        |   7107 |     10 |
| 花木兰    | 战士      | 刺客        |   5397 |    100 |
+-----------+-----------+-------------+--------+--------+
8 rows in set (0.00 sec)
</div>2019-06-30</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/17/42/7f/db8fa45f.jpg" width="30px"><span>晓涛</span> 👍（4） 💬（2）<div>sql建立索引是什么意思，老师能详细解释下不？
</div>2019-08-16</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/e5/33/ff5c52ad.jpg" width="30px"><span>不负</span> 👍（4） 💬（1）<div>过滤上线时间 DATE(birthdate) NOT BETWEEN &#39;2016-01-01&#39; AND &#39;2017-01-01&#39;，是MySQL里date类型可以直接与字符串进行比较运算？那这里birthdate可以不用 DATE 函数转换了；Oracle中日期的比较就比较严格，TO_DATE、TO_CHAR 效率也不同</div>2019-06-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/17/41/af/e5629318.jpg" width="30px"><span>꯭J꯭I꯭N꯭🙃</span> 👍（3） 💬（1）<div>SELECT name, role_main, role_assist,hp_max,mp_max
FROM heros
WHERE (role_main IN (&#39;坦克&#39;,&#39;战士&#39;) AND role_assist IS NOT NULL) 
AND (hp_max &gt; 8000 or mp_max &lt; 1500)
ORDER BY (hp_max+mp_max) DESC;</div>2019-06-25</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTIR9QrAn9TZOrJMSYMyN96PAuAjETVrN5SPp3hMbfUAGIWtHceWPEoQtPdXeuBn7VB7dagtxynAIA/132" width="30px"><span>ballgod</span> 👍（2） 💬（1）<div>关于通配符的问题想问一下老师，有看过python的正则表达式，评论第三位的解释中，+是一个或无穷个，*是零个或无穷个。按照老师说的%和_的含义，_%太%应该是匹配 </div>2019-07-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/99/ee/5204b281.jpg" width="30px"><span>Krison</span> 👍（2） 💬（1）<div>打卡，坚持学习</div>2019-06-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/e0/99/5d603697.jpg" width="30px"><span>MJ</span> 👍（2） 💬（1）<div>select name,role_main,role_assist,hp_max,mp_max from heros where (role_main in (&#39;坦克&#39;,&#39;战士&#39;) and role_assist  is not NULL) and (hp_max &gt; 8000 or mp_max &lt; 1500) order by (mp_max+hp_max) desc;

+-----------+-----------+-------------+--------+--------+
| name      | role_main | role_assist | hp_max | mp_max |
+-----------+-----------+-------------+--------+--------+
| 牛魔      | 坦克      | 辅助        |   8476 |   1926 |
| 刘邦      | 坦克      | 辅助        |   8073 |   1940 |
| 程咬金    | 坦克      | 战士        |   8611 |      0 |
| 张飞      | 坦克      | 辅助        |   8341 |    100 |
| 亚瑟      | 战士      | 坦克        |   8050 |      0 |
| 吕布      | 战士      | 坦克        |   7344 |      0 |
| 关羽      | 战士      | 坦克        |   7107 |     10 |
| 花木兰    | 战士      | 刺客        |   5397 |    100 |
+-----------+-----------+-------------+--------+--------+
</div>2019-06-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/aa/a3/0b7f0334.jpg" width="30px"><span>太精</span> 👍（2） 💬（1）<div>select name,role_main,role_assist,mp_max,hp_max from heros where role_main in(&#39;战士&#39;,&#39;坦克&#39;) and role_assist is not null and (hp_max &gt; 8000 or mp_max&lt;1500) order by (hp_max+mp_max) desc;
</div>2019-06-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/44/a7/171c1e86.jpg" width="30px"><span>啦啦啦</span> 👍（2） 💬（1）<div>打卡打卡</div>2019-06-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/19/8f/4f/d42fdb9c.jpg" width="30px"><span>Amo,</span> 👍（0） 💬（1）<div>今日打卡条件搜索</div>2020-03-20</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/QD6bf8hkS5dHrabdW7M7Oo9An1Oo3QSxqoySJMDh7GTraxFRX77VZ2HZ13x3R4EVYddIGXicRRDAc7V9z5cLDlA/132" width="30px"><span>爬行的蜗牛</span> 👍（0） 💬（1）<div>SELECT name, role_main, role_assist, hp_max, mp_max 
FROM heros
WHERE (role_main IN (&#39;坦克&#39;,&#39;战士&#39;) )  AND ( role_assist IS NOT NULL) AND (hp_max &gt; 8000 OR mp_max &lt; 1500) 
ORDER BY (hp_max + mp_max) DESC;   # 注意这个排序需要加括号， 不然不会生效。 </div>2019-12-22</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/AGicQgKibwja1SxkQ7oXQE8hYH7yCpiaicNHw3qZRuNB81aVDOQm9P1zd5F75Jbtv66G15D6ZjbbqfnoETR4321Zdw/132" width="30px"><span>高泽林</span> 👍（0） 💬（1）<div>减少全表的搜索，加强效率！</div>2019-12-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/3b/fc/04a75cd0.jpg" width="30px"><span>taoist</span> 👍（0） 💬（1）<div>MariaDB:
select name,role_main,role_assist,hp_max, mp_max from heros where role_main in(&#39;坦克&#39;,&#39;战士&#39;) and (role_assist is not null ) and (hp_max &gt; 8000 or mp_max &lt;1500) order by (hp_max + mp_max) desc;
</div>2019-12-11</li><br/><li><img src="" width="30px"><span>Geek_d3a509</span> 👍（0） 💬（1）<div>作业：（第一次提交的留言中的SQL发现我误解题目意思了，后续更改如下）select name ,hp_max ,mp_max, role_main, role_assist from heros where (role_main in(&#39;战士&#39;, &#39;坦克&#39;) and role_assist is not null) and (hp_max&gt;8000 or mp_max&lt;1500)  order by (hp_max + mp_max) desc;</div>2019-12-09</li><br/><li><img src="" width="30px"><span>Geek_d3a509</span> 👍（0） 💬（1）<div>比较运算符：有‘大于’、‘小于’、‘不等于’、‘等于’等等，主要的作用为比较两个数的关系或者实现某些特定的条件。
逻辑运算符：有‘or’、‘and’、‘in’、‘not’，实现多个字句之间的关系连接，in在某些特定的范围或条件中而not则是不在或’非’。
通配符：‘_’、‘%’、‘？’等，不同DBMS中略有不同，‘%’作用是查询所有包含某个字符的记录，‘_’和‘？’表示放在字符中的任何位置表示任意一个字符。
SQL语句：select name ,hp_max ,mp_max, role_main, role_assist from heros where hp_max&gt;8000 and mp_max&lt;1500 and (role_main in(&#39;战士&#39;, &#39;坦克&#39;) and role_assist is not null) order by (hp_max + mp_max) desc;</div>2019-12-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/88/8d/0cf741d3.jpg" width="30px"><span>Simon</span> 👍（0） 💬（1）<div>MySQL：
SELECT 
	`name` AS &#39;英雄姓名&#39;,
	`role_main` AS &#39;主要定位&#39;,
	`role_ASsist` AS &#39;次要定位&#39;,
	`hp_max` AS &#39;最大生命值&#39;,
	`mp_max` AS &#39;最大法力值&#39;
FROM `heros`
WHERE
	`role_main` IN (&#39;坦克&#39;,&#39;战士&#39;)
	AND `role_assist` IS NOT NULL
	AND (
	`hp_max` &gt;8000
	OR `mp_max` &lt;1500
	)
ORDER BY 
	(`hp_max`+`mp_max`) DESC;</div>2019-12-07</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/2e/74/88c613e0.jpg" width="30px"><span>扶幽</span> 👍（0） 💬（1）<div>作业：
select name, main_role, role_asisst, hp_max, mp_max from hero 
where main_role in (&#39;坦克&#39;, &#39;战士&#39;) and role_asisst is not null 
and (hp_max&gt;8000 or mp_max&lt;1500)
order by (hp_max+mp_max) DESC;</div>2019-10-25</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/19/f7/46/209ca424.jpg" width="30px"><span>Coool</span> 👍（0） 💬（1）<div>name	role_main	role_assist	hp_max	mp_max
牛魔	坦克	辅助	8476	1926
刘邦	坦克	辅助	8073	1940
程咬金	坦克	战士	8611	0
张飞	坦克	辅助	8341	100
亚瑟	战士	坦克	8050	0
吕布	战士	坦克	7344	0
关羽	战士	坦克	7107	10
花木兰	战士	刺客	5397	100</div>2019-10-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/19/f7/46/209ca424.jpg" width="30px"><span>Coool</span> 👍（0） 💬（1）<div>SELECT name,role_main,role_assist,hp_max,mp_max FROM heros WHERE (role_main IN(&#39;坦克&#39;,&#39;战士&#39;) AND role_assist IS NOT NULL) AND (hp_max&gt;8000 OR mp_max&lt;1500) ORDER BY (hp_max+mp_max) DESC  交作业啦~</div>2019-10-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/92/ba/9833f06f.jpg" width="30px"><span>半瓶醋</span> 👍（0） 💬（1）<div>1）比较运算符：比较字段的数值；
2）逻辑运算符：多条件筛选
3）通配符：进行一些条件复杂的过滤，但效率较低，一般会全表扫描。

#MySQL5.5 
SELECT name,role_main,role_assist,hp_max,mp_max
FROM heros
WHERE (role_main in(&#39;坦克&#39;,&#39;战士&#39;) AND role_assist IS NOT NULL)
AND (hp_max&gt;8000 OR mp_max&lt;1500)
ORDER BY (hp_max + mp_max) DESC</div>2019-10-17</li><br/>
</ul>