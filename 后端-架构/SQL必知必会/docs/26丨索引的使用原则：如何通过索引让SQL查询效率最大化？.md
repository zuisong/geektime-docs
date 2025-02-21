我之前讲了索引的使用和它的底层原理，今天我来讲一讲索引的使用原则。既然我们的目标是提升SQL的查询效率，那么该如何通过索引让效率最大化呢？

今天的课程主要包括下面几个部分：

1. 什么情况下使用索引？当我们进行数据表查询的时候，都有哪些特征需要我们创建索引？
2. 索引不是万能的，索引设计的不合理可能会阻碍数据库和业务处理的性能。那么什么情况下不需要创建索引？
3. 创建了索引不一定代表一定用得上，甚至在有些情况下索引会失效。哪些情况下，索引会失效呢？又该如何避免这一情况？

## 创建索引有哪些规律？

创建索引有一定的规律。当这些规律出现的时候，我们就可以通过创建索引提升查询效率，下面我们来看看什么情况下可以创建索引：

**1.字段的数值有唯一性的限制，比如用户名**

索引本身可以起到约束的作用，比如唯一索引、主键索引都是可以起到唯一性约束的，因此在我们的数据表中，如果某个字段是唯一性的，就可以直接创建唯一性索引，或者主键索引。

**2.频繁作为WHERE查询条件的字段，尤其在数据表大的情况下**

在数据量大的情况下，某个字段在SQL查询的WHERE条件中经常被使用到，那么就需要给这个字段创建索引了。创建普通索引就可以大幅提升数据查询的效率。

我之前列举了product\_comment数据表，这张数据表中一共有100万条数据，假设我们想要查询user\_id=785110的用户对商品的评论。
<div><strong>精选留言（30）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/10/da/36/ac0ff6a7.jpg" width="30px"><span>wusiration</span> 👍（52） 💬（9）<div>索引失效，因为使用了date函数。改成SELECT comment_id, comment_text, comment_time FROM product_comment WHERE comment_time BETWEEN DATE(&#39;2018-10-01 10:00:00&#39;) AND DATE(&#39;2018-10-02 10:00:00&#39;)
</div>2019-08-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/f1/c6/6f39a982.jpg" width="30px"><span>Yuhui</span> 👍（37） 💬（1）<div>老师您好！请教一下如何查找“不经常使用的“索引呢？谢谢！</div>2019-09-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/06/85/f1b4d5c4.jpg" width="30px"><span>佚花</span> 👍（8） 💬（1）<div>关于like. 
%在左边，即使有索引，也会失效.
只有当%在右边时，才会生效</div>2019-08-21</li><br/><li><img src="" width="30px"><span>haer</span> 👍（7） 💬（1）<div>索引失效，因为使用了date函数</div>2019-08-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/63/84/f45c4af9.jpg" width="30px"><span>Vackine</span> 👍（5） 💬（1）<div>关于关系型数据库模型介绍的论文，老师有推荐的么✨</div>2019-08-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/db/a4/191be6ad.jpg" width="30px"><span>加载中……</span> 👍（4） 💬（1）<div>老师好，请教个问题，有没有经验数据，在索引区分度低于“某个值”(80%)的时候，就不适合在这个列上建立索引了？</div>2019-08-30</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/f1/84/7d21bd9e.jpg" width="30px"><span>Goal</span> 👍（4） 💬（1）<div>老师，今天文章中的“product_comment”表结构和数据，是从哪里导入的呢？

个人感觉，本课程用到的所有表都可以放到一个统一的地方，比如之前的 GitHub上面，方便我们统一下载。</div>2019-08-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/18/ee/a1ed60d1.jpg" width="30px"><span>ABC</span> 👍（4） 💬（1）<div>索引会失效，因为使用了date函数。

如果修改的话，可以用between和and，对查询条件进行转换。

例如:currtime between date(&#39;2018-01-10 10:00:00) and date(&#39;2018-02-10 12:00:00&#39;) 

手机回复，没有实际运行，如有错误请老师指正，谢谢</div>2019-08-09</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/E3XKbwTv6WTssolgqZjZCkiazHgl2IdBYfwVfAcB7Ff3krsIQeBIBFQLQE1Kw91LFbl3lic2EzgdfNiciaYDlJlELA/132" width="30px"><span>rike</span> 👍（3） 💬（3）<div>“按照 user_id 进行评论分组，同时按照评论时间降序的方式进行排序”，执行对应的sql后，报错。望大神验证一下，不要误导付费学习的读者。</div>2019-12-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/19/cc/b7/af6ef83d.jpg" width="30px"><span>抢小孩子糖吃</span> 👍（3） 💬（1）<div>老师 如果我们给女儿国的性别加上了索引   我们查看男性的话会快很多 
但如果我们有时需要查看男性 有时需要查看女性 还适合在性别上建索引吗  
查看女性的时候优化器会选择用这个索引找数据吗</div>2019-11-23</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/DYAIOgq83er4HlmmWfWicNmo3x3HKaOwz3ibcicDFlV5xILbILKGFCXbnaLf2fZRARfBdVBC5NhIPmXxaxA0T9Jhg/132" width="30px"><span>Geek_Wison</span> 👍（3） 💬（2）<div>老师您好，本节的内容我有个疑惑的地方：创建联合索引(comment_time, user_id)，但是查询语句是先GROUP BY，然后再ORDER BY，那这样子的话，这个联合索引不是应该不符合最左侧原则而失效了吗？</div>2019-08-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/c9/6e/1ac1c955.jpg" width="30px"><span>niemo</span> 👍（3） 💬（1）<div>老师 您好，sql条件执行顺序不是从右到左么？所有在使用联合索引的时候，把最左的索引写在where条件的最右边，这样理解对么？</div>2019-08-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/b5/98/ffaf2aca.jpg" width="30px"><span>Ronnyz</span> 👍（2） 💬（1）<div>作业：
对comment_time使用了函数，索引失效
SELECT comment_id, comment_text, comment_time FROM product_comment WHERE comment_time BETWEEN DATE(&#39;2018-10-01 10:00:00&#39;) AND DATE(&#39;2018-10-02 10:00:00&#39;);

2888 rows in set (1.60 sec)</div>2019-08-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/20/c0/6367536e.jpg" width="30px"><span>卡布</span> 👍（1） 💬（1）<div>KLOOK校招面试的时候就问了索引，那时候对索引一概不通，这回得在专栏补回来。</div>2019-12-04</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/40/d1/fb6f402a.jpg" width="30px"><span>melon</span> 👍（1） 💬（1）<div>老师 为什么group by   后的列要加索引呢？
</div>2019-08-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/18/14/5e/6d4f328f.jpg" width="30px"><span>LiuChen</span> 👍（1） 💬（1）<div>老师，对于已有的表结构去创建索引，创建后就直接可以用吗？需不需要其他操作？</div>2019-08-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/1b/4a/f9df2d06.jpg" width="30px"><span>蒙开强</span> 👍（1） 💬（3）<div>老师，你好，SQL执行where条件的时候是从左到右还是从右到左呢，过滤的时候可以优化先执行过滤数据多的条件。</div>2019-08-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/81/e6/6cafed37.jpg" width="30px"><span>旅途</span> 👍（0） 💬（1）<div>这节专栏我想背下来,干货太多了
</div>2019-12-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/19/69/bf/58f70a2a.jpg" width="30px"><span>程序员花卷</span> 👍（0） 💬（1）<div>索引会失效的！
原因——
在上述的那条查询语句中使用了Date()函数，所以索引会失效，

最终需要改为
SELECT comment_id, comment_text, comment_time FROM product_comment WHERE  comment_time BETWEEN DATE(&#39;2018-10-01 10:00:00&#39;) AND DATE(&#39;2018-10-02 10:00:00&#39;)</div>2019-12-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/19/f7/46/209ca424.jpg" width="30px"><span>Coool</span> 👍（0） 💬（1）<div>SELECT
	user_id,
	COUNT(*) AS num 
FROM
	product_comment 
GROUP BY
	user_id 
	LIMIT 100;

未创建索引查询时间：10.148s

创建user_id索引后查询时间：0.076s</div>2019-10-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/18/dc/49/43ae1627.jpg" width="30px"><span>Ansyear</span> 👍（0） 💬（1）<div>很多章节确实比mysql45讲的更清楚更容易理解，也更详细</div>2019-09-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/4d/fd/0aa0e39f.jpg" width="30px"><span>许童童</span> 👍（0） 💬（1）<div>会索引失效，用到了DATE函数，应该给字符串使用DATE函数
SELECT comment_id, comment_text, comment_time FROM product_comment WHERE comment_time &gt;= DATE(&#39;2018-10-01 10:00:00&#39;) AND comment_time &lt;= DATE(&#39;2018-10-02 10:00:00&#39;)


</div>2019-08-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/4d/5e/c5c62933.jpg" width="30px"><span>lmtoo</span> 👍（0） 💬（1）<div>应该把字符串转为date类型</div>2019-08-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/63/5b/062da5eb.jpg" width="30px"><span>黑山老妖</span> 👍（11） 💬（9）<div>老师 SELECT user_id, count(*) as num FROM product_comment group by user_id order by comment_time desc limit 100
这个例子中 对（comment_time,user_id）进行索引 ，老师不是说按照最左原则，索引会失效嘛 为什么还是会起作用，望老师解答 ：）</div>2019-08-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/dd/67/7d0d566a.jpg" width="30px"><span>梦想天空</span> 👍（6） 💬（5）<div>老师 您好。使用selet * from T where a&lt;4 or a=9;   a有索引，但还是全盘扫描，不知道什么原因</div>2019-08-10</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/mVtGLzdgB7pKFgaQdYUoAaNDic1xCqLqATcuVYPGCBuCy4tTwEBhicaZ70tvSbMaGAEEia7cJwcjfmdfTffFlAsSw/132" width="30px"><span>Andywu</span> 👍（4） 💬（0）<div>去掉date函数后，查看执行计划，索引生效了。
mysql&gt; explain SELECT comment_id, comment_text, comment_time FROM product_comment WHERE comment_time &gt;= &#39;2018-10-01 10:00:00&#39; AND comment_time &lt;= &#39;2018-10-02 10:00:00&#39;;
+----+-------------+-----------------+------------+-------+---------------+--------------+---------+------+------+----------+-----------------------+
| id | select_type | table           | partitions | type  | possible_keys | key          | key_len | ref  | rows | filtered | Extra                 |
+----+-------------+-----------------+------------+-------+---------------+--------------+---------+------+------+----------+-----------------------+
|  1 | SIMPLE      | product_comment | NULL       | range | comment_time  | comment_time | 6       | NULL | 2929 |   100.00 | Using index condition |
+----+-------------+-----------------+------------+-------+---------------+--------------+---------+------+------+----------+-----------------------+
1 row in set, 1 warning (0.00 sec)

查询时间缩短为0.01s。
mysql&gt; SELECT comment_id, comment_text, comment_time FROM product_comment WHERE comment_time &gt;= &#39;2018-10-01 10:00:00&#39; AND comment_time &lt;= &#39;2018-10-02 10:00:00&#39;;
2929 rows in set (0.01 sec)</div>2019-08-26</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/EcYNib1bnDf5dz6JcrE8AoyZYMdqic2VNmbBtCcVZTO9EoDZZxqlQDEqQKo6klCCmklOtN9m0dTd2AOXqSneJYLw/132" width="30px"><span>博弈</span> 👍（2） 💬（0）<div>
需要创建索引的情况：
1、	字段值唯一
2、	Where条件
3、	Group by 和order by
4、	Update、delete的where条件
5、	Distinct字段
6、	多表join操作时，表尽量不超过3个，对where条件创建索引，对连接的字段创建索引且类型一致
7、	多个单列索引在多条件查询时只会生效一个索引（MySQL 会选择其中一个限制最严格的作为索引），所以在多条件联合查询的时候最好创建联合索引。

不需要创建索引的情况：
1、	WHERE 条件（包括 GROUP BY、ORDER BY）里用不到的字段不需要创建索引
2、	如果表记录太少，比如少于 1000 个，那么是不需要创建索引的
3、	字段中如果有大量重复数据，也不用创建索引，比如性别字段
4、	频繁更新的字段不一定要创建索引

索引失效的情况：
1、	如果索引进行了表达式计算，则会失效
2、	如果对索引使用函数，也会造成失效
3、	在 WHERE 子句中，如果在 OR 前的条件列进行了索引，而在 OR 后的条件列没有进行索引，那么索引会失效
4、	当我们使用 LIKE 进行模糊查询的时候，后面不能是 %
5、	索引列尽量设置为 NOT NULL 约束
6、	我们在使用联合索引的时候要注意最左原则</div>2020-03-25</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/67/f4/9a1feb59.jpg" width="30px"><span>钱</span> 👍（0） 💬（0）<div>这节很有用，可以直接指导实践</div>2024-08-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/b4/94/2796de72.jpg" width="30px"><span>追风筝的人</span> 👍（0） 💬（0）<div>索引使用函数DATE()，也会造成失效</div>2022-09-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/2d/34/a7/52c4ea60.jpg" width="30px"><span>年少挽滑稽世无双</span> 👍（0） 💬（0）<div>索引失效，因为对索引使用了函数---&gt;DATE()。
修改：
SELECT comment_id, comment_text, comment_time FROM product_comment WHERE comment_time &gt;= &#39;2018-10-01 10:00:00&#39; AND comment_time &lt;= &#39;2018-10-02 10:00:00&#39;；</div>2022-09-15</li><br/>
</ul>