你好，我是大明。今天我们来聊一聊数据库中的 SQL 优化。

一般而言，在面试过程中，我都是鼓励你尽可能为自己打造熟练掌握性能优化技巧的人设。高并发项目经验可遇不可求，但是高性能是可以勉强追求的，性能优化就是追求高性能的方法。和我在微服务里面讲到的高可用相结合，你在写简历、自我介绍和面试过程中，可以有意识地展示自己在高可用和高性能方面的知识和积累。

而 SQL 优化是性能优化中最平易近人、最好准备的点。所以今天我们就来学习一下 SQL 优化的多种方案。

## 前置知识

SQL 优化可以看作是一个更大的主题“数据库优化”下的一个子议题。数据库优化主要包含以下内容：

- 硬件资源优化：换更大更强的机器。
- 操作系统优化：调整操作系统的某些设置。
- 服务器/引擎优化：也就是针对数据库软件本体进行优化，比如说调整事务隔离级别。在 MySQL 里面还可以针对不同的引擎做优化，比如说调整 InnoDB 引擎的日志刷盘时机。
- SQL 优化：针对的就是 SQL 本身了。

![](https://static001.geekbang.org/resource/image/ea/f7/ea9337b3727f69fb1e494af845882ff7.png?wh=2440x1310)

如果站在数据库的角度，那么 SQL 优化就是为了达到两个目标。

1. **减少磁盘 IO**，这个又可以说是尽量避免全表扫描、尽量使用索引以及尽量使用覆盖索引。
2. **减少内存 CPU 消耗**，这一部分主要是尽可能减少排序、分组、去重之类的操作。
<div><strong>精选留言（13）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/11/44/48/fae317c1.jpg" width="30px"><span>子休</span> 👍（33） 💬（1）<div>这里列一下我个人之前总结的SQL优化的思路（稍微增加了一些本章节提到了，但是我也学习到了的内容）：
1. 索引的角度。
（1）根据执行计划优化索引，从type，keys，extra这几个主要字段去分析。
（2）避免返回不需要的列（覆盖索引，避免回表）
2. 架构层面。
（1）分库分表
（2）读写分离
（3）为了避免like这种，以及超级大数据量查询（没办法避免多表查询），可以借助数仓，建宽表，以及引入es等方法进行实现。
3. 分析问题角度
（1）执行sql之前，先执行“set profiling = 1;”，然后执行完查询sql之后，执行&quot;show profiles &quot;可以展示详细的具体执行时间。
（2）show profiles的方法已经开始被MySQL逐渐淘汰，后续会被 performance_schema代替，performance_schema是一个数据库，里面有87张表，可以通过查询这些表来查看执行情况。
4. 常见技巧
（1）深度分页问题：limit m,n分页越往后越慢的问题。
      a. select * from tableA where id &gt;=(select id from tableA limit m, 1) limit n；
这种做法有个弊端，要求主键必须自增。
      b. select * from tableA a
     inner join (select id from tableA limit m, n)b
     on a.id = b.id
(2)避免For循环里面查单条数据，改为一条sql查集合。
(3)建表的时候考虑增加冗余字段，尽可能保持单表查询，而非多表Join.
(4)在所有的排序场景中，都应该尽量利用索引来排序.
(5)算count行数的时候，如果业务场景要求不高，可以有一个偏门方法，就是执行explain select * from t where xxxx，在执行计划里面会预估出来大致的行数。
(6)where 替代 having</div>2023-07-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/ce/6d/530df0dd.jpg" width="30px"><span>徐石头</span> 👍（11） 💬（1）<div>1. 按前台业务和后台业务分表，前台业务表不包含各种审核状态，只包含纯粹的业务数据，所以表数据更少，字段更小，每次读到buffer pool 中能读更多的数据，性能更好
2. 避免like查询，搜索功能使用专业的搜索引擎，而且还能更加为业务提供更多发展空间，比如es的分词，权重打分等
3. 避免循环中查询单条数据的错误，写的时候要思考如果该接口高并发时会不会挂
4. 适当冗余少量字段，做一定的反范式设计，尽量使用单表查询
5. 索引是有代价的，在上千万的数据中，有时候索引占的空间比表数据更大，一定要避免滥用，不要为了sql建索引，而是从业务角度考虑索引</div>2023-07-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/19/43/0b/7688f18c.jpg" width="30px"><span>江 Nina</span> 👍（11） 💬（10）<div>[WHERE id &gt; max_id ] 具体实操过程中，max_id是如何获取的呢？假如直接点击第1000页的内容，是不是就没法实现了？</div>2023-07-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/50/2b/2344cdaa.jpg" width="30px"><span>第一装甲集群司令克莱斯特</span> 👍（7） 💬（1）<div>SQL查询分页偏移量大的问题，又名深度分页。</div>2023-07-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/2a/44/e6/2c97171c.jpg" width="30px"><span>sheep</span> 👍（6） 💬（1）<div>&quot;SHOW TABLE STATUS 也能看到一个 TABLE_ROWS 列，代表表的行数，那么能不能用这个来优化 COUNT(*)？&quot;
不太行，索引统计的值是通过采样来估算的。实际上，TABLE_ROWS 就是从这个采样估算得来的，因此它也很不准。有多不准呢，官方文档说误差可能达到 40% 到 50%。
《MySQL实战45讲》的第14章，也有介绍这一点</div>2023-09-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/da/d9/f051962f.jpg" width="30px"><span>浩仔是程序员</span> 👍（6） 💬（1）<div>老师你好，如果一个表单管理，有很多的筛选条件，超过10个，需要怎么设置索引比较合理，好像也避免不了回表的问题</div>2023-07-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/18/c9/fe/874b172b.jpg" width="30px"><span>benxiong</span> 👍（1） 💬（1）<div>请问下，优化 order by 这里，SELECT * FROM  xxx WHERE uid = 123 ORDER BY update_time，新建联合索引 &lt;uid,  update_time&gt;，uid 确定之后，update_time 自然是有序的。像我们线上都是最新订单数据放在上面，也就是倒序排序，这种情况，加联合索引是无法解决的吧，还有其他好的解决方案吗</div>2024-04-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/2a/44/e6/2c97171c.jpg" width="30px"><span>sheep</span> 👍（1） 💬（1）<div>&quot;优化 COUNT&quot;这里&quot;考虑使用 Redis 之类的 NoSQL 来直接记录总数&quot;，这里不太好记录吧，像MySQL有一致性视图就很难模拟吧，市场有啥成熟的案例咩</div>2023-09-25</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/08/ab/caec7bca.jpg" width="30px"><span>humor</span> 👍（1） 💬（2）<div>修改索引或者说表定义变更的核心问题是数据库会加表锁，直到修改完成。
好像mysql是支持online ddl的吧。那如果支持的话，是不是对大表也可以直接ddl了</div>2023-07-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/28/44/cf/791d0f5e.jpg" width="30px"><span>ZhiguoXue_IT</span> 👍（0） 💬（1）<div>在之前的团队中用过强制force指定索引，之所以这样做是为了在mysql表的数据量特别大的时候，mysql自己的内部优化器会给推荐别的索引，现实中发现强制有另一个索引，查询的性能会很大，也就是可以理解为mysql自己的查询优化器有时候会选择错误的索引</div>2023-07-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/28/44/cf/791d0f5e.jpg" width="30px"><span>ZhiguoXue_IT</span> 👍（0） 💬（1）<div>1）请教一下老师，select count(distinct(name)) from user 这条sql如何优化，能用group by优化吗？select name from user group by name;
</div>2023-07-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/99/6e/abb7bfe3.jpg" width="30px"><span>景</span> 👍（0） 💬（2）<div>「在所有的排序场景中，都应该尽量利用索引来排序，这样能够有效减轻数据库的负担，加快响应速度。进一步来说，像 ORDER BY，DISTINCT 等这样的操作也可以用类似的思路。」

在这个例子中，如果按 uid, uid &amp; update_time 的查询场景都有，那是建两个索引（一个单列索引，一个联合索引）还是一个联合索引呢？</div>2023-07-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/25/87/f3a69d1b.jpg" width="30px"><span>peter</span> 👍（0） 💬（1）<div>请教老师两个问题：
Q1：操作系统的设置可以优化数据库？
以前没有注意到这个方面。以MySQL为例，win10下，调整哪些参数可以改善MySQL性能？（也可以以Linux为例说明）。
Q2：为什么Limit后面是5000？
“当你要拿第101页的数据，需要写成 LIMIT 50000, 50。50000 就是偏移量”，为什么要写成“需要写成 LIMIT 50000, 50”？</div>2023-07-10</li><br/>
</ul>