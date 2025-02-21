在MySQL中，有很多看上去逻辑相同，但性能却差异巨大的SQL语句。对这些语句使用不当的话，就会不经意间导致整个数据库的压力变大。

我今天挑选了三个这样的案例和你分享。希望再遇到相似的问题时，你可以做到举一反三、快速解决问题。

# 案例一：条件字段函数操作

假设你现在维护了一个交易系统，其中交易记录表tradelog包含交易流水号（tradeid）、交易员id（operator）、交易时间（t\_modified）等字段。为了便于描述，我们先忽略其他字段。这个表的建表语句如下：

```
mysql> CREATE TABLE `tradelog` (
  `id` int(11) NOT NULL,
  `tradeid` varchar(32) DEFAULT NULL,
  `operator` int(11) DEFAULT NULL,
  `t_modified` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `tradeid` (`tradeid`),
  KEY `t_modified` (`t_modified`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
```

假设，现在已经记录了从2016年初到2018年底的所有数据，运营部门有一个需求是，要统计发生在所有年份中7月份的交易记录总数。这个逻辑看上去并不复杂，你的SQL语句可能会这么写：

```
mysql> select count(*) from tradelog where month(t_modified)=7;
```

由于t\_modified字段上有索引，于是你就很放心地在生产库中执行了这条语句，但却发现执行了特别久，才返回了结果。

如果你问DBA同事为什么会出现这样的情况，他大概会告诉你：如果对字段做了函数计算，就用不上索引了，这是MySQL的规定。

现在你已经学过了InnoDB的索引结构了，可以再追问一句为什么？为什么条件是where t\_modified='2018-7-1’的时候可以用上索引，而改成where month(t\_modified)=7的时候就不行了？
<div><strong>精选留言（30）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/0f/bc/8a/9420cf2a.jpg" width="30px"><span>冠超</span> 👍（34） 💬（2）<div>非常感谢老师分享的内容，实打实地学到了。这里提个建议，希望老师能介绍一下设计表的时候要怎么考虑这方面的知识哈😊</div>2019-01-28</li><br/><li><img src="" width="30px"><span>700</span> 👍（8） 💬（6）<div>老师您好，有个问题恳请指教。背景如下，我长话短说：

mysql&gt;select @@version;
5.6.30-log

 CREATE TABLE `t1` ( `id` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL,  `plan_id` int(11) NOT NULL DEFAULT &#39;0&#39; ,  PRIMARY KEY (`id`),
  KEY `userid` (`user_id`) USING BTREE,  KEY `idx_planid` (`plan_id`)
) ENGINE=InnoDB DEFAULT CHARSET=gb2312;

 CREATE TABLE `t3` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `status` int(4) NOT NULL DEFAULT &#39;0&#39;,
  `ootime` varchar(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `idx_xxoo` (`status`,`ootime`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

t1 和 t3 表的字符集不一样

sql 执行计划如下：
explain
SELECT t1.id, t1.user_id
  FROM t1, t3
 WHERE t1.plan_id = t3.id
   AND t3.ootime &lt; UNIX_TIMESTAMP(&#39;2022-01-18&#39;)
+----+-------------+-------+-------+---------------+--------------+---------+--------------+-------+----------------------------------------+
| id | select_type | table | type  | possible_keys | key          | key_len | ref          | rows  | Extra                                  |
+----+-------------+-------+-------+---------------+--------------+---------+--------------+-------+----------------------------------------+
|  1 | SIMPLE      | t3    | index | PRIMARY       | idx_xxoo     | 51      | NULL         | 39106 | Using where; Using index               |
|  1 | SIMPLE      | t1    | ref   | idx_planid    | idx_planid   | 4       |        t3.id |   401 | Using join buffer (Batched Key Access) |
+----+-------------+-------+-------+---------------+--------------+---------+--------------+-------+----------------------------------------+

我的疑惑是
1)t3 的 status 没出现在 where 条件中，但执行计划为什么用到了 idex_xxoo 索引？
2)为什么 t3.ootime 也用到索引了，从 key_len 看出。t3.ootime 是 varchar 类型的，而 UNIX_TIMESTAMP(&#39;2022-01-18&#39;) 是数值，不是发生了隐式转换吗？

请老师指点。
</div>2019-01-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/c7/a1/273bff58.jpg" width="30px"><span>可凡不凡</span> 👍（23） 💬（21）<div>1.老师好
2.如果在用一个 MySQL 关键字做字段,并且字段上索引,当我用这个索引作为唯一查询条件的时候 ,会 造  成隐式的转换吗? 
例如:SELECT * FROM b_side_order WHERE CODE = 332924 ; (code 上有索引)
3. mysql5.6  code 上有索引  intime 上没有索引
语句一:
SELECT * FROM b_side_order WHERE CODE = 332924 ;
语句二;
  UPDATE b_side_order SET in_time = &#39;2018-08-04 08:34:44&#39; WHERE 1=2 or CODE = 332924;

这两个语句 执行计划走 select 走了索引,update 没有走索引 是执行计划的bug 吗??

 


</div>2018-12-25</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTICBNZjA9hW65x6g9b2iaicKUJW5gxFxtgPXH9Cqp6eyFfY1sD2hVY4dZrY5pmoK2r1KZEiaaIKocdZQ/132" width="30px"><span>赖阿甘</span> 👍（42） 💬（12）<div>“mysql&gt;select l.operator from tradelog l , trade_detail d where d.tradeid=l.tradeid and d.id=4;”
图6上面那句sql是不是写错了。d.tradeid=l.tradeid是不是该写成l.tradeid = d.tradeid？不然函数会作用在索引字段上，就只能全表扫描了</div>2018-12-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/03/f7/3a493bec.jpg" width="30px"><span>老杨同志</span> 👍（179） 💬（30）<div>感谢老师鼓励，我本人工作时间比较长，有一定的基础，听老师的课还是收获很大。每次公司内部有技术分享，我都去听课，但是多数情况，一两个小时的分享，就只有一两句话受益。老师的每篇文章都能命中我的知识盲点，感觉太别爽。

对应今天的隐式类型转换问题也踩过坑。
我们有个任务表记录待执行任务，表结构简化后如下：
CREATE TABLE `task` (
  `task_id` int(11) NOT NULL AUTO_INCREMENT COMMENT &#39;自增主键&#39;,
  `task_type` int(11) DEFAULT NULL COMMENT &#39;任务类型id&#39;,
  `task_rfid` varchar(50) COLLATE utf8_unicode_ci DEFAULT NULL COMMENT &#39;关联外键1&#39;,
  PRIMARY KEY (`task_id`)
) ENGINE=InnoDB AUTO_INCREMENT CHARSET=utf8 COLLATE=utf8_unicode_ci COMMENT=&#39;任务表&#39;;

task_rfid 是业务主键，当然都是数字，查询时使用sql：
select * from task where task_rfid =123;
其实这个语句也有隐式转换问题，但是待执行任务只有几千条记录，并没有什么感觉。
这个表还有个对应的历史表，数据有几千万
忽然有一天，想查一下历史记录，执行语句
select * from task_history where task_rfid =99;
直接就等待很长时间后超时报错了。
如果仔细看，其实我的表没有task_rfid 索引，写成task_rfid =‘99’也一样是全表扫描。
运维时的套路是，猜测主键task_id的范围，怎么猜，我原表有creat_time字段，我会先查
select max(task_id) from task_history   然后再看看 select * from task_history  where task_id = maxId - 10000的时间，估计出大概的id范围。然后语句变成
select * from task_history where task_rfid =99 and id between ？ and ？;
</div>2018-12-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/ee/d2/7024431c.jpg" width="30px"><span>探索无止境</span> 👍（230） 💬（14）<div>老师，有道面试题困扰了很久，求指教！题目是这样的，a表有100条记录，b表有10000条记录，两张表做关联查询时，是将a表放前面效率高，还是b表放前面效率高？网上各种答案，但感觉都没有十分的说服力，期待老师的指点！</div>2019-01-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/9b/a8/6a391c66.jpg" width="30px"><span>geraltlaush</span> 👍（113） 💬（9）<div>索引字段不能进行函数操作，但是索引字段的参数可以玩函数，一言以蔽之</div>2018-12-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/18/34/c082419c.jpg" width="30px"><span>风轨</span> 👍（63） 💬（4）<div>刚试了文中穿插得思考题:当主键是整数类型条件是字符串时，会走索引。
文中提到了当字符串和数字比较时会把字符串转化为数字，所以隐式转换不会应用到字段上，所以可以走索引。
另外，select &#39;a&#39; = 0 ; 的结果是1，说明无法转换成数字的字符串都被转换成0来处理了。</div>2018-12-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/03/a2/ceb37046.jpg" width="30px"><span>crazyone</span> 👍（57） 💬（5）<div>老师你好，我在执行explain的时候，发现extra 里面 有using where，using index ，using index condition 能具体讲下这几个的区别吗？</div>2018-12-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/99/af/d29273e2.jpg" width="30px"><span>饭粒</span> 👍（30） 💬（1）<div>感觉要使用索引就不能“破坏”索引原有的顺序，这节的函数操作，隐式转换都“破坏”了原有的顺序。前一节的select * from t where city in in (“杭州”,&quot; 苏州 &quot;) order by name limit 100; 同样是破坏了 (city,name) 联合索引的递增顺序，类似的还有使用联合索引，一个字段DESC，一个ASC。</div>2019-02-25</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/16/77/73bd9d18.jpg" width="30px"><span>匿名的朋友</span> 👍（26） 💬（2）<div>丁奇老师，我有个疑问，就是sql语句执行时那些order by group by  limit 以及where条件，有执行的先后顺序吗？</div>2019-01-05</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/DYAIOgq83eqJobg767PUeqrqQQ4B6YvMatj2SRyOicKZZ4gWTf30dMketiaj58Gc3RFTmckGxAXlL9ERSxGovq9g/132" width="30px"><span>涛哥哥</span> 👍（22） 💬（11）<div>老师，您好！我是做后端开发的。想问一下 mysql in关键字 的内部原理，能抽一点点篇幅讲一下吗？比如：select * from T where id in (a,b,d,c,,e,f); id是主键。1、为什么查询出来的结果集会按照id排一次序呢（是跟去重有关系么）？2、如果 in 里面的值较多的时候，就会比较慢啊（是还不如全表扫描么）？问我们公司很多后端的，都不太清楚，问我们DBA，他说默认就是这样（这不跟没说一样吗）。希望老师可以帮忙解惑。祝老师身体健康！微笑~</div>2019-01-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/67/29/b0ec5430.jpg" width="30px"><span>greatcl</span> 👍（16） 💬（1）<div>刚刚帮一个同事看SQL慢的问题，帮他找出来问题，并拿出这篇文章让他看，哈哈</div>2019-05-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/c7/a1/273bff58.jpg" width="30px"><span>可凡不凡</span> 👍（14） 💬（2）<div>1.老师对于多表联合查询中,MySQL 对索引的选择 以后会详细介绍吗?
</div>2018-12-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/ed/a5/ca3b4cc4.jpg" width="30px"><span>Wrelon</span> 👍（10） 💬（1）<div>在第10章的时候提问过一次，当时表述的不够清楚，现在知道了，应该是因为隐式类型转换导致了全索引扫描。这个课程真实太棒了，我踩过的坑都说了。</div>2018-12-25</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/8a/9a/7270d764.jpg" width="30px"><span>Enterprize</span> 👍（8） 💬（1）<div>再选字符集和排序集上有什么最佳实践么</div>2018-12-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/9c/9c/e02a0daf.jpg" width="30px"><span>运斤成风</span> 👍（6） 💬（1）<div>说下我的理解：驱动表的索引字段不能添加函数运算或算术运算，若是则无法用到快速索引。而被驱动表则没有这个限制。</div>2019-01-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/62/a5/43aa0c27.jpg" width="30px"><span>TKbook</span> 👍（6） 💬（3）<div>老师，对于最后回答上一课的问题：mysql&gt; select * from t limit N, M-N+1;
这个语句也不是取3条记录。 没理解。</div>2018-12-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/f3/69/7039d03f.jpg" width="30px"><span>渔村蓝</span> 👍（6） 💬（1）<div>上期问题答案是取三个数，但是这里貌似不是三个数，不理解。</div>2018-12-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/ed/1a/269eb3d6.jpg" width="30px"><span>cfanbo</span> 👍（6） 💬（3）<div>在这个例子里，放弃了树搜索功能，优化器可以选择遍历主键索引，也可以选择遍历索引 t_modified，优化器对比索引大小后发现，索引 t_modified 更小，遍历这个索引比遍历主键索引来得更快。

优化器如何对比的，根据参与字段字段类型占用空间大小吗？</div>2018-12-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/f8/ba/d28174a9.jpg" width="30px"><span>Geek_zbvt62</span> 👍（6） 💬（2）<div>谁是驱动表谁是被驱动表，是否大多数情况看where条件就可以了？这是否本质上涉及到mysql底层决定用什么算法进行级联查询的问题？后面会有课程详细说明嘛？
</div>2018-12-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/fa/4b/c385f755.jpg" width="30px"><span>向前走</span> 👍（5） 💬（2）<div>老师您好,问个可能低级的问题,个人不太明白,望解惑下,就是我看您写的那些多个表的关联查询里面没有使用join关键字来关联两个表的查询,想问下是mysql默认作了join操作,还是join的写法对性能有什么影响而不使用join么,谢谢</div>2018-12-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/9b/a8/6a391c66.jpg" width="30px"><span>geraltlaush</span> 👍（5） 💬（3）<div>老师，经常面试被问到工作中做了什么优化，有没有好的业务表的设计，请问老师课程结束后能不能给我们一个提纲挈领的大纲套路，让我们有个脉络和思路来应付这种面试套路</div>2018-12-25</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/93/85/f5d9474c.jpg" width="30px"><span>乔丹</span> 👍（4） 💬（2）<div>老师，做全表扫描，怎么不是用primary key做索引扫描呢？</div>2020-03-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/9c/9c/e02a0daf.jpg" width="30px"><span>运斤成风</span> 👍（4） 💬（1）<div>老师好，用explain工具能看到索引是否被用，而无法看到索引为什么没有被用，比如优化内部做了隐藏转换导致索引无法使用。我的问题是有没有工具能看到这一步的具体转换？谢谢</div>2019-01-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/61/c7/b64ac05e.jpg" width="30px"><span>sky</span> 👍（4） 💬（1）<div>字符集 utf8mb4 是 utf8 的超集，所以当这两个类型的字符相互转换的时候，小的转大的精度不会丢失，大的转小的再比较不会有问题么， 就像long 转int 的时候会截断</div>2018-12-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/06/f2/1f511b7f.jpg" width="30px"><span>大坤</span> 👍（4） 💬（1）<div>之前遇到过按时间范围查询大表不走索引的情况，如果缩小时间范围，又会走索引，记得在一些文章中看到过结果数据超过全表的30%就会走全表扫描，但是前面说的时间范围查询大表，这个时间范围绝对是小于30%的情况，想请教下老师，这个优化器都是在什么情况下会放弃索引呢？</div>2018-12-25</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/05/d4/e06bf86d.jpg" width="30px"><span>长杰</span> 👍（4） 💬（1）<div>这里我给出一种方法，取 Y1、Y2 和 Y3 里面最大的一个数，记为 M，最小的一个数记为 N，然后执行下面这条 SQL 语句：

mysql&gt; select * from t limit N, M-N+1;
再加上取整个表总行数的 C 行，这个方案的扫描行数总共只需要 C+M 行。
优化后的方案应该是C+M+1行吧？</div>2018-12-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/ed/4e/ef406442.jpg" width="30px"><span>唯她命</span> 👍（3） 💬（1）<div>优化方案 CONVERT(l.tradeid USING utf8)   会丢精度吧？</div>2019-03-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/76/93/c78a132a.jpg" width="30px"><span>果然如此</span> 👍（3） 💬（4）<div>我想问一个上期的问题，随机算法2虽然效率高，但是还是有个瑕疵，比如我们的随机出题算法无法直接应用，因为每次随机一个试题id，多次随机没有关联，会产生重复id，有没有更好的解决方法？</div>2018-12-25</li><br/>
</ul>