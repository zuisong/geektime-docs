我们上节课讲到了SQL函数，包括算术函数、字符串函数、日期函数和转换函数。实际上SQL函数还有一种，叫做聚集函数，它是对一组数据进行汇总的函数，输入的是一组数据的集合，输出的是单个值。通常我们可以利用聚集函数汇总表的数据，如果稍微复杂一些，我们还需要先对数据做筛选，然后再进行聚集，比如先按照某个条件进行分组，对分组条件进行筛选，然后得到筛选后的分组的汇总信息。

有关今天的内容，你重点需要掌握以下几个方面：

1. 聚集函数都有哪些，能否在一条SELECT语句中使用多个聚集函数；
2. 如何对数据进行分组，并进行聚集统计；
3. 如何使用HAVING过滤分组，HAVING和WHERE的区别是什么。

## 聚集函数都有哪些

SQL中的聚集函数一共包括5个，可以帮我们求某列的最大值、最小值和平均值等，它们分别是：

![](https://static001.geekbang.org/resource/image/d1/15/d101026459ffa96504ba3ebb85054415.png?wh=776%2A326)

这些函数你可能已经接触过，我们再来简单复习一遍。我们继续使用heros数据表，对王者荣耀的英雄数据进行聚合。

如果我们想要查询最大生命值大于6000的英雄数量。

```
SQL：SELECT COUNT(*) FROM heros WHERE hp_max > 6000
```

运行结果为41。

如果想要查询最大生命值大于6000，且有次要定位的英雄数量，需要使用COUNT函数。

```
SQL：SELECT COUNT(role_assist) FROM heros WHERE hp_max > 6000
```

运行结果是 23。
<div><strong>精选留言（30）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/12/5a/5e/a897cb0d.jpg" width="30px"><span>grey927</span> 👍（78） 💬（2）<div>ORDER BY 是对分的组排序还是对分组中的记录排序呢？</div>2019-07-04</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/e5/33/ff5c52ad.jpg" width="30px"><span>不负</span> 👍（47） 💬（4）<div>一个发现：虽然 SELECT 的执行顺序在 GROUP BY 和 HAVING 后面，但对于SELECT中列的别名都可以使用。
MySQL中
1. &gt; SELECT COUNT(*) as num, role_main, AVG(hp_max) FROM heros
    -&gt; WHERE hp_max&gt;6000
    -&gt; GROUP BY role_main
    -&gt; HAVING COUNT(*)&gt;5
    -&gt; ORDER BY COUNT(*) DESC;
+-----+-----------+-------------+
| num | role_main | AVG(hp_max) |
+-----+-----------+-------------+
|  17 | 战士      |        7028 |
|  10 | 坦克      |      8312.4 |
|   6 | 法师      |        6417 |
+-----+-----------+-------------+
2. &gt; SELECT COUNT(*) num, ROUND(AVG(hp_max+mp_max), 2) avg, ROUND(MAX(hp_max+mp_max), 2) max, ROUND(MIN(hp_max+mp_max), 2) min FROM heros
    -&gt; WHERE (hp_max+mp_max)&gt;7000
    -&gt; GROUP BY attack_range
    -&gt; ORDER BY num DESC;
+-----+---------+----------+---------+
| num | avg     | max      | min     |
+-----+---------+----------+---------+
|  36 | 8654.42 | 11036.00 | 7117.00 |
|  26 | 7743.77 |  8737.00 | 7025.00 |
+-----+---------+----------+---------+
</div>2019-06-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/fc/90/c9df0459.jpg" width="30px"><span>ack</span> 👍（20） 💬（3）<div>练习题
1.SELECT COUNT(*) AS num,role_main,AVG(hp_max) FROM heros WHERE hp_max &gt; 6000 GROUP BY role_main HAVING num&gt;5 ORDER BY num DESC; 
2.SELECT COUNT(*) AS num,ROUND(MAX(hp_max+mp_max),2),ROUND(AVG(hp_max+mp_max),2),ROUND(MIN(hp_max+mp_max),2) FROM heros WHERE hp_max+mp_max &gt; 7000 GROUP BY attack_range ORDER BY num DESC;</div>2019-06-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/19/5b/08/b0b0db05.jpg" width="30px"><span>丁丁历险记</span> 👍（18） 💬（2）<div>讲个段子   having  常用来做过滤掉那些跑来冒充程序员的人。
他们深深的震惊了我的认知。</div>2019-11-07</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/ca/bd/a51ae4b2.jpg" width="30px"><span>吃饭饭</span> 👍（10） 💬（1）<div>讲的很详细了，入门必备</div>2019-06-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/41/bb/21ce60d2.jpg" width="30px"><span>安静的boy</span> 👍（8） 💬（1）<div>where先对数据进行排序，group by再进行分组。让我对数据筛选和分组恍然大悟！</div>2019-06-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/e1/1a/20977779.jpg" width="30px"><span>峻铭</span> 👍（7） 💬（1）<div>前面老师在评论中回复过，在group by分组和having筛选分组之间还有一步使用聚集函数进行计算，在目前看到的having都是对cout聚集函数结果的筛选，想试试对其他聚集函数的筛选，然后对训练1做了点小改动：
select count(*) as c,role_main,avg(hp_max) as v  from heros where hp_max &gt; 6000 GROUP BY role_main HAVING c &gt; 5 and v &gt; 7000 order by c DESC;</div>2019-09-01</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/d3/24/58c0a3dd.jpg" width="30px"><span>bear</span> 👍（5） 💬（1）<div>Having 部分精彩，赞👍</div>2019-08-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/0c/0f/93d1c8eb.jpg" width="30px"><span>mickey</span> 👍（5） 💬（1）<div>有个错误：
文中“比如，我们想要按照英雄的主要定位、次要定位进行分组，查看这些英雄的数量，并按照这些分组的英雄数量从高到低进行排序。”的SQL语句：SQL: SELECT COUNT(*), role_main, role_assist FROM heros GROUP BY role_main, role_assist ORDER BY num DESC

在MySQL里会报错：[Err] 1054 - Unknown column &#39;num&#39; in &#39;order clause&#39;

要改为：SELECT COUNT(*) as num, role_main, role_assist FROM heros GROUP BY role_main, role_assist ORDER BY num DESC;</div>2019-06-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/0c/0f/93d1c8eb.jpg" width="30px"><span>mickey</span> 👍（3） 💬（4）<div>&#47;*
1.筛选最大生命值大于6000的英雄，按照主要定位进行分组，选择分组英雄数量大于5的分组，
按照分组英雄数从高到低进行排序，并显示每个分组的英雄数量、主要定位和平均最大生命值。
*&#47;
SELECT count(*) as num, role_main, AVG(hp_max)
FROM heros 
WHERE hp_max &gt; 6000 
GROUP BY role_main 
HAVING num &gt; 5 
ORDER BY num DESC 

num role_main AVG(hp_max)
------------------------------------
17	战士	7028
10	坦克	8312.4
6	法师	6417

&#47;*
2.筛选最大生命值与最大法力值之和大于7000的英雄，按照攻击范围来进行分组，
显示分组的英雄数量，以及分组英雄的最大生命值与法力值之和的平均值、最大值和最小值，
并按照分组英雄数从高到低进行排序，其中聚集函数的结果包括小数点后两位。
*&#47;
SELECT count(*) as num, ROUND(AVG(hp_max + mp_max), 2), MAX(hp_max + mp_max), MIN(hp_max + mp_max)
FROM heros 
WHERE hp_max + mp_max &gt; 7000 
GROUP BY attack_range
HAVING num &gt; 5 
ORDER BY num DESC 

num, ROUND(AVG(hp_max + mp_max), 2), MAX(hp_max + mp_max), MIN(hp_max + mp_max)
------------------------------------------------------------------------
62	8272.53	11036	7025</div>2019-06-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/18/32/82/273a44cd.jpg" width="30px"><span>圆子蛋</span> 👍（3） 💬（1）<div>1.SELECT COUNT(*) as num,role_main,AVG(hp_max) FROM heros WHERE hp_max &gt; 6000 GROUP BY role_main HAVING num&gt;5 ORDER BY num DESC; 
2.SELECT COUNT(*) as num,ROUND(MAX(hp_max+mp_max),2),ROUND(AVG(hp_max+mp_max),2),ROUND(MIN(hp_max+mp_max),2) FROM heros WHERE (hp_max+mp_max) &gt; 7000 GROUP BY attack_range ORDER BY num DESC;
老师在“如何对数据进行分组，并进行聚集统计”的第三个例子里，COUNT(*) 后面没有加 as num，但是 ORDER BY 里直接出现了 num？</div>2019-06-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/2b/84/07f0c0d6.jpg" width="30px"><span>supermouse</span> 👍（2） 💬（1）<div>思考题 1：
SELECT 
    COUNT(*) AS num, role_main, AVG(hp_max)
FROM
    heros
WHERE
    hp_max &gt; 6000
GROUP BY role_main
HAVING num &gt; 5
ORDER BY num DESC;
思考题 2：
SELECT 
    COUNT(*) AS num,
    attack_range,
    ROUND(AVG(hp_max + mp_max), 2),
    ROUND(MAX(hp_max + mp_max), 2),
    ROUND(MIN(hp_max + mp_max), 2)
FROM
    heros
WHERE
    hp_max + mp_max &gt; 7000
GROUP BY attack_range
ORDER BY num DESC;</div>2019-06-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/aa/a3/0b7f0334.jpg" width="30px"><span>太精</span> 👍（2） 💬（1）<div>SELECT COUNT(*) AS num, role_main, AVG(hp_max)  AS avg_max FROM heros WHERE hp_max &gt; 6000 GROUP BY role_main HAVING num &gt; 5 ORDER BY num DESC;
SELECT ROUND((COUNT(*)),2) AS num, ROUND((AVG(hp_max+mp_max)),2) AS heros_avg, ROUND((MAX(hp_max+mp_max)),2) AS max_avg, ROUND((MIN(hp_max+mp_max)),2) AS min_avg FROM heros WHERE (hp_max+mp_max) &gt; 7000 GROUP BY attack_range ORDER BY num desc;
</div>2019-06-28</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTLIZpAiabrHDmPye39vFLPibWtlkcEVlOeufJ14uYACPamfZh0urvsumJvkalFUkDodqTescgj4j7tw/132" width="30px"><span>Geek_157522</span> 👍（1） 💬（1）<div>筛选最大生命值大于 6000 的英雄，按照主要定位进行分组，选择分组英雄数量大于 5 的分组，按照分组英雄数从高到低进行排序，并显示每个分组的英雄数量、主要定位和平均最大生命值。
SELECT COUNT(*) as num, role_main, AVG(hp_max)FROM heros WHERE hp_max&gt;6000 GROUP BY role_main HAVING num&gt;5  ORDER BY  num DESC
筛选最大生命值与最大法力值之和大于 7000 的英雄，按照攻击范围来进行分组，显示分组的英雄数量，以及分组英雄的最大生命值与法力值之和的平均值、最大值和最小值，并按照分组英雄数从高到低进行排序，其中聚集函数的结果包括小数点后两位。
SELECT COUNT(*) as num, ROUND(AVG(hp_max+mp_max),2)，ROUND(MAX(hp_max+mp_max),2),ROUND(MIN(hp_max+mp_max),2)FROM heros WHERE (hp_max+mp_max)&gt;7000 GROUP BY attack_max  ORDER BY  num DESC

</div>2021-02-26</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/QD6bf8hkS5dHrabdW7M7Oo9An1Oo3QSxqoySJMDh7GTraxFRX77VZ2HZ13x3R4EVYddIGXicRRDAc7V9z5cLDlA/132" width="30px"><span>爬行的蜗牛</span> 👍（0） 💬（1）<div>SELECT  COUNT(*) as num, role_main, avg(hp_max)
FROM heros
WHERE hp_max &gt; 6000 
GROUP BY role_main  HAVING num &gt; 5 ORDER BY num DESC; </div>2019-12-24</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/PiajxSqBRaEIzcqzRzz09q1XpPFZu752t0t03qDQZBI32FwiafYibfJbHqqATrRL5iaE591wyVl5Y3eHQMnBeyZxVQ/132" width="30px"><span>amor</span> 👍（0） 💬（1）<div>SELECT COUNT(*) AS num,role_main,AVG(hp_max) FROM heros WHERE hp_max &gt;6000 GROUP BY role_main HAVING num &gt;5 ORDER BY num DESC;
+-----+-----------+-------------+
| num | role_main | AVG(hp_max) |
+-----+-----------+-------------+
|  17 | 战士      |        7028 |
|  10 | 坦克      |      8312.4 |
|   6 | 法师      |        6417 |
+-----+-----------+-------------+
3 rows in set (0.02 sec)</div>2019-12-22</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/AGicQgKibwja1SxkQ7oXQE8hYH7yCpiaicNHw3qZRuNB81aVDOQm9P1zd5F75Jbtv66G15D6ZjbbqfnoETR4321Zdw/132" width="30px"><span>高泽林</span> 👍（0） 💬（1）<div>非常好！适合我！</div>2019-12-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/3b/fc/04a75cd0.jpg" width="30px"><span>taoist</span> 👍（0） 💬（1）<div># MariaDB:

1. SELECT role_main,AVG(hp_max) as avg_hp, COUNT(*) AS count FROM  heros WHERE hp_max &gt; 6000 GROUP BY  role_main HAVING count &gt; 5 ORDER BY count DESC;

2.  SELECT COUNT(*) as num, ROUND(AVG(hp_max+mp_max),2), ROUND( MAX(hp_max+mp_max), 2), ROUND(MIN(hp_max+mp_max) ,2) FROM heros WHERE (hp_max + mp_max) &gt; 7000 GROUP BY attack_range ORDER BY num DESC;</div>2019-12-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/d8/63/e4c28138.jpg" width="30px"><span>春风</span> 👍（0） 💬（1）<div>SELECT MIN(name), MAX(name) FROM heros;
result：不知火舞，黄忠
SELECT MIN(CONVERT(name USING gbk)), MAX(CONVERT(name USING gbk)) FROM heros
result：阿珂，庄周
这两条查出来的结果不一样？上面那个也不是a到z啊</div>2019-12-03</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/cKeYVTKJCJhrfTCBkEGla1WA7W0S9FPZrTR3ovYJFhcKo7kl72gR9VibCufhHsjOar2Z6mZlFKb8VEkkDv9lqVA/132" width="30px"><span>坤2021牛</span> 👍（0） 💬（1）<div>mysql:  SELECT COUNT(*) as num, role_main, role_assist FROM heros WHERE hp_max &gt; 6000 GROUP BY role_main, role_assist HAVING num &gt; 5 ORDER BY num DESC;
oracle: select count(*) as num,t.reson_code from E_STATE t where t.equi_code = &#39;R01&#39; group by t.reson_code HAVING num &gt; 5 order by num desc;

在oracle下报错，锁num无效。是不是oracle下不支持having，但是不应该啊。</div>2019-11-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/2e/74/88c613e0.jpg" width="30px"><span>扶幽</span> 👍（0） 💬（1）<div>作业：
1) SELECT COUNT(*) AS num, role_main, AVG(hp_max) FROM heros WHERE hp_max&gt;6000 GROUP BY role_main HAVING num&gt;5 ORDER BY num DESC;
2) SELECT COUNT(*) AS num, ROUND(AVG(hp_max+mp_max), 2) AS avg, ROUND(MAX(hp_max+mp_max),2) AS max, ROUND(MIN(hp_max+mp_max), 2) AS min FROM heros
WHERE hp_max+mp_max&gt;7000 GROUP BY attack_range ORDER BY num DESC;</div>2019-10-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/92/ba/9833f06f.jpg" width="30px"><span>半瓶醋</span> 👍（0） 💬（1）<div>1）
SELECT COUNT(*) nums,role_main,AVG(hp_max) avg_hp
from heros
WHERE hp_max &gt; 6000
GROUP BY role_main
HAVING nums &gt; 5
ORDER BY nums DESC

2）SELECT COUNT(*) as nums,attack_range,ROUND(AVG(hp_max + mp_max),2) as avg_hp_mp,
			 MAX(hp_max + mp_max) as max_hp_mp,
			 MIN(hp_max + mp_max) as min_hp_mp
FROM heros
WHERE (hp_max + mp_max) &gt; 7000
GROUP BY attack_range
ORDER BY nums DESC</div>2019-10-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/4c/4e/91267714.jpg" width="30px"><span>Cola_</span> 👍（0） 💬（1）<div>练习题
1.select count(*) as num,role_main,avg(hp_max) from heros where hp_max&gt;6000 group by role_main having num&gt;5 order by num desc;
2.select count(*) as num,round(avg(hp_max+mp_max),2),round(max(hp_max+mp_max),2),round(min(hp_max+mp_max),2) from heros where (hp_max+mp_max&gt;7000) group by attack_range order by num desc;</div>2019-09-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/19/00/bb/25a29311.jpg" width="30px"><span>森鱼</span> 👍（0） 💬（1）<div>课后题确实要写一下才会发现自己的错误在哪里，我竟然会忘了写FROM heros……</div>2019-09-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/ea/46/9c9808a9.jpg" width="30px"><span>Serendipity</span> 👍（0） 💬（1）<div>
SELECT COUNT(*) as num, role_main, AVG(hp_max) FROM heros WHERE hp_max&gt;6000 GROUP BY role_main HAVING num&gt;5 ORDER BY num DESC
SELECT COUNT(*) as num, attack_range, ROUND(AVG(hp_max+mp_max), 2), ROUND(MAX(hp_max+mp_max),2), ROUND(MIN(hp_max+mp_max),2) FROM heros WHERE (hp_max+mp_max)&gt;7000 GROUP BY attack_range ORDER BY num DESC
</div>2019-08-31</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/e6/68/1871d6ba.jpg" width="30px"><span>海洋</span> 👍（0） 💬（1）<div>作业：
mysql&gt; SELECT COUNT(*) as num, role_main, AVG(hp_max) FROM heros WHERE hp_max &gt; 6000 GROUP BY role_main HAVING COUNT(*) &gt; 5 ORDER  BY num DESC;
+-----+-----------+-------------+
| num | role_main | AVG(hp_max) |
+-----+-----------+-------------+
|  17 | 战士      |        7028 |
|  10 | 坦克      |      8312.4 |
|   6 | 法师      |        6417 |
+-----+-----------+-------------+
3 rows in set (0.06 sec)

mysql&gt; SELECT ROUND(COUNT(*),2) as num, ROUND(AVG(hp_max+mp_max),2), ROUND(MAX(hp_max+mp_max),2), ROUND(MIN(hp_max+mp_max),2) FROM heros  WHERE (hp_max+mp_max) &gt; 7000 GROUP BY attack_range ORDER BY num DESC;
+-----+-----------------------------+-----------------------------+-----------------------------+
| num | ROUND(AVG(hp_max+mp_max),2) | ROUND(MAX(hp_max+mp_max),2) | ROUND(MIN(hp_max+mp_max),2) |
+-----+-----------------------------+-----------------------------+-----------------------------+
|  36 |                     8654.42 |                    11036.00 |                     7117.00 |
|  26 |                     7743.77 |                     8737.00 |                     7025.00 |
+-----+-----------------------------+-----------------------------+-----------------------------+
2 rows in set (0.06 sec)</div>2019-08-12</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTIk46cor5XVFTPZbPOnb7pViabgy450pobo46hRHFQz5nR5ocYRKIzC8vShic36vwa553H4Vj50x5wA/132" width="30px"><span>冲</span> 👍（0） 💬（1）<div>1.SELECT COUNT(*) AS num,AVG(hp_max),role_main from heros WHERE hp_max&gt;6000 GROUP BY role_main HAVING num&gt;5 ORDER BY num desc
2.SELECT COUNT(*) AS num,ROUND(AVG(hp_max+mp_max),2),ROUND(MAX(hp_max+mp_max),2),ROUND(MIN(hp_max+mp_max),2) 
FROM heros
WHERE hp_max+mp_max &gt; 7000 GROUP BY attack_range ORDER BY num DESC  </div>2019-08-07</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/75/8d/c6a2a048.jpg" width="30px"><span>Reiser</span> 👍（0） 💬（1）<div>SQL：
SELECT COUNT(*) AS num ,role_main,AVG(hp_max) FROM heros WHERE hp_max&gt;6000 GROUP BY role_main HAVING num &gt;5 ORDER BY num DESC;

SELECT COUNT(*) AS num, ROUND(AVG(mp_max+hp_max),2),ROUND(MAX(mp_max+hp_max),2),ROUND(MIN(mp_max+hp_max),2) FROM heros WHERE (mp_max+hp_max)&gt;7000 GROUP BY attack_range ORDER BY num DESC ;</div>2019-08-05</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/89/3e/1976b66f.jpg" width="30px"><span>Fargo</span> 👍（0） 💬（1）<div>1. SELECT COUNT(*) as num , role_main, AVG(hp_max) FROM heros WHERE hp_max &gt; 6000 GROUP BY role_main HAVING num &gt; 5 ORDER BY num DESC;
+-----+-----------+-------------+
| num | role_main | AVG(hp_max) |
+-----+-----------+-------------+
|  17 | 战士      |        7028 |
|  10 | 坦克      |      8312.4 |
|   6 | 法师      |        6417 |
+-----+-----------+-------------+

2. SELECT COUNT(*) as num, ROUND(AVG(hp_max+mp_max), 2), MAX(hp_max+mp_max), MIN(hp_max+mp_max) FROM heros WHERE (hp_max+mp_max)&gt;7000 GROUP BY role_main ORDER BY num DESC;
+-----+------------------------------+--------------------+--------------------+
| num | ROUND(AVG(hp_max+mp_max), 2) | MAX(hp_max+mp_max) | MIN(hp_max+mp_max) |
+-----+------------------------------+--------------------+--------------------+
|  17 |                      7798.29 |               8898 |               7025 |
|  16 |                      8289.06 |               9290 |               7117 |
|  10 |                      9752.40 |              11036 |               8441 |
|   9 |                      7590.78 |               7770 |               7395 |
|   6 |                      8523.83 |               9843 |               7325 |
|   4 |                      7679.25 |               8054 |               7291 |
+-----+------------------------------+--------------------+--------------------+</div>2019-07-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/17/41/af/e5629318.jpg" width="30px"><span>꯭J꯭I꯭N꯭🙃</span> 👍（0） 💬（1）<div>#1筛选最大生命值大于6000的英雄，按照主要定位进行分组，选择分组英雄数量大于5的分组，按照分组英雄数从高到低进行排序，并显示每个分组的英雄数量、主要定位和平均最大生命值。
-- SELECT COUNT(*) as num, role_main, AVG(hp_max) 
-- FROM heros 
-- WHERE hp_max &gt; 6000
-- GROUP BY role_main
-- HAVING num &gt; 5
-- ORDER BY num DESC;

#2.筛选最大生命值与最大法力值之和大于7000的英雄，按照攻击范围来进行分组，显示分组的英雄数量，以及分组英雄的最大生命值与法力值之和的平均值、最大值和最小值，
#并按照分组英雄数从高到低进行排序，其中聚集函数的结果包括小数点后两位。
SELECT COUNT(*) as num, ROUND(AVG(DISTINCT (hp_max+mp_max)),2) ,ROUND(MAX(hp_max+mp_max), 2), ROUND(MIN(hp_max+mp_max), 2)
FROM heros
WHERE (hp_max+mp_max) &gt; 7000
GROUP BY attack_range
ORDER BY num desc;</div>2019-07-15</li><br/>
</ul>