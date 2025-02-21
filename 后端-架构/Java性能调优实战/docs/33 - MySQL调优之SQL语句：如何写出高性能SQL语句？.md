你好，我是刘超。

从今天开始，我将带你一起学习MySQL的性能调优。MySQL数据库是互联网公司使用最为频繁的数据库之一，不仅仅因为它开源免费，MySQL卓越的性能、稳定的服务以及活跃的社区都成就了它的核心竞争力。

我们知道，应用服务与数据库的交互主要是通过SQL语句来实现的。在开发初期，我们更加关注的是使用SQL实现业务功能，然而系统上线后，随着生产环境数据的快速增长，之前写的很多SQL语句就开始暴露出性能问题。

在这个阶段中，我们应该尽量避免一些慢SQL语句的实现。但话说回来，SQL语句慢的原因千千万，除了一些常规的慢SQL语句可以直接规避，其它的一味去规避也不是办法，我们还要学会如何去分析、定位到其根本原因，并总结一些常用的SQL调优方法，以备不时之需。

那么今天我们就重点看看慢SQL语句的几种常见诱因，从这点出发，找到最佳方法，开启高性能SQL语句的大门。

## 慢SQL语句的几种常见诱因

### 1. 无索引、索引失效导致慢查询

如果在一张几千万数据的表中以一个没有索引的列作为查询条件，大部分情况下查询会非常耗时，这种查询毫无疑问是一个慢SQL查询。所以对于大数据量的查询，我们需要建立适合的索引来优化查询。
<div><strong>精选留言（30）</strong></div><ul>
<li><img src="https://wx.qlogo.cn/mmopen/vi_32/DYAIOgq83eotSSnZic41tGkbflx0ogIg3ia6g2muFY1hCgosL2t3icZm7I8Ax1hcv1jNgr6vrZ53dpBuGhaoc6DKg/132" width="30px"><span>张学磊</span> 👍（98） 💬（13）<div>status和create_time单独建索引，在查询时只会遍历status索引对数据进行过滤，不会用到create_time列索引，将符合条件的数据返回到server层，在server对数据通过快排算法进行排序，Extra列会出现file sort；应该利用索引的有序性，在status和create_time列建立联合索引，这样根据status过滤后的数据就是按照create_time排好序的，避免在server层排序</div>2019-08-06</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/7b/57/a9b04544.jpg" width="30px"><span>QQ怪</span> 👍（17） 💬（2）<div>对staus和create_time建立联合索引</div>2019-08-06</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/9c/40/6323850e.jpg" width="30px"><span>Jian</span> 👍（16） 💬（4）<div>因为好久没有做SQL相关的开发了，所以开始没有特别明白【利用子查询优化分页查询】这里面的意思。我来说下自己的想法，请您检证。我看到您贴的截图中，优化后的sql语句，扫描的行数（rows列）分别是90409和10001，多余前一个较慢的查询，可见扫描行数，不是这个性能的主要原因。我推测这个是由于limit [m],n的实现方法导致的，即MySql会把m+n的数据都取出来，然后返回n个数据给用户。如果用第二种SQL语句，子查询只是获得一个id，虽然扫描了很多行，但都是在索引上进行的，切不需要回表获取内容。外查询是根据id获取数据20条内容，速度自然就会快了。我认为这里性能提高的原因还是居于索引的恰当使用。</div>2019-08-12</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/6LaITPQ4Lk5fZn8ib1tfsPW8vI9icTuSwAddiajVfibPDiaDvMU2br6ZT7K0LWCKibSQuicT7sIEVmY4K7ibXY0T7UQEiag/132" width="30px"><span>尔东橙</span> 👍（13） 💬（1）<div>老师，分页查询优化那一块，单从扫描函数看，采用子查询和不采用子查询扫描总行数是差不多的，而不采用子查询，第一个主查询就是返回10020条记录，采用子查询只返回20条记录？我理解是结果集有多少行就是返回多少记录。是因为子查询不返回记录么，它不也扫描了10000行么？</div>2020-02-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/67/f4/9a1feb59.jpg" width="30px"><span>钱</span> 👍（8） 💬（4）<div>课后思考及问题
1：按照效率排序的话，count(字段)&lt;count(主键 id)&lt;count(1)≈count(*)，所以我建议你，尽量使用 count(*)。——MySQL，丁奇老师的结论
如果对一张大表经常做 SELECT COUNT(*) 操作，这肯定是不明智的。——刘老师的结论
同样的问题，不同的老师给出了截然相反的结论，我希望有一天两位老师可以讨论一下为什么?
刘老师具体没讲COUNT(*)的原理，我倾向于认为丁奇老师的结论是正确的。</div>2019-09-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/17/11/6b/8034959a.jpg" width="30px"><span>迎风劲草</span> 👍（5） 💬（3）<div>创建 status create_time order_no 联合索引，避免回表</div>2019-08-06</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/eb/d7/712912a7.jpg" width="30px"><span>mumu</span> 👍（4） 💬（2）<div>
select * from `demo`.`order` where id&gt; (select id from `demo`.`order` order by order_no limit 10000, 1)  limit 20;，老师您好，我不懂这样写为什么是正确的，为什么id&gt;子查询结果的20条就是按order_no排序所需的20条？</div>2019-11-04</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/a0/cb/aab3b3e7.jpg" width="30px"><span>张三丰</span> 👍（4） 💬（2）<div>就算使用了联合索引，也避免不了排序吧，因为题目要求的是降序，联合索引是保证第一个索引有序的前提下再保证第二个索引有序，那么这个有序是升序，如果没记错的话。</div>2019-10-04</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTJ9WPJDCXbpOSCL7PxPic9TP2l2ahyGiakia6iaziaO0BicVUibyN4ymicckTzaKzhdZrU9W3GkpsmpBnfiaibg/132" width="30px"><span>Geek_002ff7</span> 👍（4） 💬（1）<div>真实情况一般不会在status上单独建索引，因为status大部分都是重复值，数据库一般走全表扫描了，感觉漏讲了索引失效的情况</div>2019-08-09</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/6LaITPQ4Lk5fZn8ib1tfsPW8vI9icTuSwAddiajVfibPDiaDvMU2br6ZT7K0LWCKibSQuicT7sIEVmY4K7ibXY0T7UQEiag/132" width="30px"><span>尔东橙</span> 👍（3） 💬（1）<div>为什么分页查询优化那块，主查询扫描这么多行？</div>2019-09-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/47/b4/e8b3f53f.jpg" width="30px"><span>IT橘子</span> 👍（2） 💬（1）<div>老师，常用的SQL优化-1.优化分页查询中利用子查询优化分页查询成立的条件是不是order_no建立了唯一索引，即order_no与id（主键）一一对应，并且在order_no的索引上，id是严格单调递增的？</div>2020-03-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/17/8b/4b/15ab499a.jpg" width="30px"><span>风轻扬</span> 👍（2） 💬（2）<div>select * from `demo`.`order` where id&gt; (select id from `demo`.`order` order by order_no limit 10000, 1)  limit 20;
老师，这个优化后的查询，您是先查询出来的第10001条数据的id，然后 id 大于此值。获取20条数据。这样获取的值不对啊，我试了。这样获取的是10002到10021的数据了，不是10001到10020的数据。子查询获取的值减一就对了</div>2019-09-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/d0/69/5dbdc245.jpg" width="30px"><span>张德</span> 👍（1） 💬（1）<div>没看别人评论  我来说一下  直接查状态为1的订单  索引的区分度太低</div>2019-08-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/5f/73/bb3dc468.jpg" width="30px"><span>拒绝</span> 👍（1） 💬（1）<div>感觉要建立联合索引，但不知具体原因</div>2019-08-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/38/f1/996a070d.jpg" width="30px"><span>LW</span> 👍（1） 💬（2）<div>order_no创建主键，status+create_time创建联合索引</div>2019-08-06</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/47/65/cce8eb34.jpg" width="30px"><span>nimil</span> 👍（1） 💬（2）<div>select * from table limit 1 这种sql语句会走主键索引么，我看explain里边没有任何索引记录</div>2019-08-06</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/30/c1/2dde6700.jpg" width="30px"><span>密码123456</span> 👍（1） 💬（1）<div>有Oracle吗？oracle感觉用的人不多了，是不是要被淘汰了？</div>2019-08-06</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/54/dc/cc1f6865.jpg" width="30px"><span>春暖花开</span> 👍（0） 💬（1）<div>我们平时最常用的就是 COUNT(*) 和 COUNT(1) 这两种方式了，其实两者没有明显的区别，在拥有主键的情况下，它们都是利用主键列实现了行数的统计
这个是不是一般使用占用内存最小的是索引统计？  一般二级索引比主键索引占用空间更小</div>2020-04-27</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTKhuGLVRYZibOTfMumk53Wn8Q0Rkg0o6DzTicbibCq42lWQoZ8lFeQvicaXuZa7dYsr9URMrtpXMVDDww/132" width="30px"><span>hello</span> 👍（0） 💬（1）<div>老师请教您一个问题，文中“优化SELECT COUNT(*)”，如果需要精确COUNT值时，可以额外新增一个汇总统计表来统计需要的COUNT值，如果COUTN时有条件过滤，这种如何操作的呀？多谢！</div>2020-03-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/62/49/6332c99b.jpg" width="30px"><span>man1s</span> 👍（0） 💬（1）<div>创建create_time + status 的组合索引
问：老湿，执行计划中的const&#47;system 你说B+树的第一层就可以返回，可是只有叶子节点才存储数据呀
</div>2019-09-16</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/17/8c/34/c0aef91d.jpg" width="30px"><span>陈影</span> 👍（0） 💬（1）<div>select * from `demo`.`order` where id&gt; (select id from `demo`.`order` order by order_no limit 10000, 1)  limit 20;
老师，这个子查询找到了按照order_no排序第10001行数据的id，这个id是按照这种排序递增的吗？主查询是怎么找到这种排序方式下第10001-10020行数据的？</div>2019-08-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/ac/62/37912d51.jpg" width="30px"><span>东方奇骥</span> 👍（0） 💬（4）<div>select * from `demo`.`order` order by order_no limit 10000, 20;
select * from `demo`.`order` where id&gt; (select id from `demo`.`order` order by order_no limit 10000, 1)  limit 20;  老师，感觉自己没完全弄明白，就是用子查询快那么多，但是子查询里，不是也要扫描10001行？还是说子查询里只查了id，不需要回行，所以速度快？
</div>2019-08-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/0a/c0/401c240e.jpg" width="30px"><span>撒旦的堕落</span> 👍（0） 💬（1）<div>订单状态字段的离散度很低  不适合做索引
因为离散度低   而又没有分页  所以当表数据量大的时候 查询出来的数量也有可能很大  
创建时间倒序 可以换成主键倒序 去除掉时间字段的索引  
根据状态查询 个人觉得可以从业务入手  将相同状态的数据保存到一张表  想听听老师的意见</div>2019-08-06</li><br/><li><img src="" width="30px"><span>Geek_xbye50</span> 👍（0） 💬（1）<div>创建status，创建时间及订单号联合索引，其中创建时间制定降序，这样避免产生filesort及回表！不知道是否正确？</div>2019-08-06</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/2b/fa/1cde88d4.jpg" width="30px"><span>大俊stan</span> 👍（22） 💬（5）<div>count(*) 的速度是最快的innodb自己有优化</div>2019-09-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/94/68/56794ea3.jpg" width="30px"><span>Kian.Lee</span> 👍（16） 💬（4）<div>我在实际项目中使用“select order_no from order where status =1 order by id desc
” 代替此功能，id为bigint ，也少维护一个索引（create_time）😁</div>2019-08-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/01/4b/196a7d8a.jpg" width="30px"><span>起点</span> 👍（5） 💬（0）<div>sql慢通常是两种情况
    1.sql没有使用到索引。
    2.因为sql语句使用了粗粒度的锁，导致大量的锁等待，所以也会让sql变慢。

怎样对慢sql进行分析
1.使用explain分析sql的索引使用情况。
2.使用show profile 指令分析sql的资源损耗情况

常用的sql优化
1.对于limit 的优化。
案例中优化的逻辑（子查询使用了覆盖索引，jion的sql需要把匹配的数据都拿到，再从数据中拿到10000到10010条的数据。子查询的案例中是先获取到符合条件的数据id条件，然后从主查询中查询过滤直接得到符合条件的20条数据）

2.对于count的优化。
可用explain获取近似值。
可冗余一个统计字段

思考题的sql问题在于
status和create_time分别是两个索引，而sql查询的时候只能用到一个索引，所以思考题的sql肯定会用create_time的索引（因为status列的离散性不高），而通过crete_time索引是无法获取到status的值的，所以又必须通过聚集索引获得status的值，然后再对status进行过滤，获得最终结果。
思考题可通过组合索引优化，把status和create_time建立为一个组合索引，这个时候就只需要通过这个组合索引就能过滤掉所有条件，而且索引中已经包含了需要查询显示的列，这里又会使用覆盖索引，索引无须查询聚集索引进行回表操作。

完全理解老师的优化案例还需要一定基础知识才行。参考下面这篇文章可帮大家补充一些sql优化的基础原则。
sql优化原则
https:&#47;&#47;mp.weixin.qq.com&#47;s&#47;u3FOsTroEo6eqKIrfoBBSQ</div>2020-08-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/c5/f2/fccf87bb.jpg" width="30px"><span>石妖</span> 👍（3） 💬（0）<div>思考题中，由于status区分度较低，无论是否有索引，以status为条件进行查询大概率是进行全表扫描，而且联合索引有一定的局限性（最左匹配），所以我觉得没有必要在status上添加索引。而create_time因为是排序字段，可以利用索引有序性优化查询速度。所以，我建议是只在create_time添加索引即可</div>2020-05-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/d0/d7/a09ef784.jpg" width="30px"><span>Tattoo</span> 👍（0） 💬（0）<div>mark：status和create_time单独建索引，在查询时只会遍历status索引对数据进行过滤，不会用到create_time列索引，将符合条件的数据返回到server层，在server对数据通过快排算法进行排序，Extra列会出现file sort；应该利用索引的有序性，在status和create_time列建立联合索引，这样根据status过滤后的数据就是按照create_time排好序的，避免在server层排序</div>2022-06-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/2a/f6/56/519489f4.jpg" width="30px"><span>002</span> 👍（0） 💬（0）<div>先排序 后条件查询</div>2022-05-06</li><br/>
</ul>