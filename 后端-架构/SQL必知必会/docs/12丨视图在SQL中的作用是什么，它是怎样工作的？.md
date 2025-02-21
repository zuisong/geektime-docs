我们之前对SQL中的数据表查询进行了讲解，今天我们来看下如何对视图进行查询。视图，也就是我们今天要讲的虚拟表，本身是不具有数据的，它是SQL中的一个重要概念。从下面这张图中，你能看到，虚拟表的创建连接了一个或多个数据表，不同的查询应用都可以建立在虚拟表之上。

![](https://static001.geekbang.org/resource/image/6c/e8/6c7cd968b0bd24ce5689a08c052eade8.jpg?wh=736%2A430)

视图一方面可以帮我们使用表的一部分而不是所有的表，另一方面也可以针对不同的用户制定不同的查询视图。比如，针对一个公司的销售人员，我们只想给他看部分数据，而某些特殊的数据，比如采购的价格，则不会提供给他。

刚才讲的只是视图的一个使用场景，实际上视图还有很多作用，今天我们就一起学习下。今天的文章里，你将重点掌握以下的内容：

1. 什么是视图？如何创建、更新和删除视图？
2. 如何使用视图来简化我们的SQL操作？
3. 视图和临时表的区别是什么，它们各自有什么优缺点？

## 如何创建，更新和删除视图

视图作为一张虚拟表，帮我们封装了底层与数据表的接口。它相当于是一张表或多张表的数据结果集。视图的这一特点，可以帮我们简化复杂的SQL查询，比如在编写视图后，我们就可以直接重用它，而不需要考虑视图中包含的基础查询的细节。同样，我们也可以根据需要更改数据格式，返回与底层数据表格式不同的数据。
<div><strong>精选留言（30）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/0f/ed/1a/269eb3d6.jpg" width="30px"><span>cfanbo</span> 👍（58） 💬（1）<div>视图的底层原理是什么？执行一个查询语句是会有哪些操作步骤？</div>2019-07-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/f1/84/7d21bd9e.jpg" width="30px"><span>Goal</span> 👍（44） 💬（1）<div>视图的作用：

1、视图隐藏了底层的表结构，简化了数据访问操作，客户端不再需要知道底层表的结构及其之间的关系。

2、视图提供了一个统一访问数据的接口。（即可以允许用户通过视图访问数据的安全机制，而不授予用户直接访问底层表的权限），从而加强了安全性，使用户只能看到视图所显示的数据。
3、视图还可以被嵌套，一个视图中可以嵌套另一个视图。
注意：视图总是显示最新的数据！每当用户查询视图时，数据库引擎通过使用视图的 SQL 语句重建数据。</div>2019-07-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/0d/45/b88a1794.jpg" width="30px"><span>一叶知秋</span> 👍（22） 💬（4）<div>优点：在总结中有写，安全、清晰 。
缺点：的话感觉就是如果需要额外的字段就需要更新视图吧...(感觉说的也不对

更新视图对基本表数据有影响。（比如update视图实际上就是对基本表的更新操作）
证明如下：
mysql&gt; select * from team_score;
+---------+-----------+-----------+--------------+--------------+------------+
| game_id | h_team_id | v_team_id | h_team_score | v_team_score | game_date  |
+---------+-----------+-----------+--------------+--------------+------------+
|   10001 |      1001 |      1002 |          102 |          111 | 2019-04-01 |
|   10002 |      1002 |      1003 |          135 |          134 | 2019-04-10 |
+---------+-----------+-----------+--------------+--------------+------------+
2 rows in set (0.00 sec)

mysql&gt; create view h_team_score as select game_id, h_team_score from team_score;
Query OK, 0 rows affected (0.01 sec)

mysql&gt; update h_team_score set h_team_score=103 where game_id=10001;
Query OK, 1 row affected (0.01 sec)
Rows matched: 1  Changed: 1  Warnings: 0

mysql&gt; select * from team_score;
+---------+-----------+-----------+--------------+--------------+------------+
| game_id | h_team_id | v_team_id | h_team_score | v_team_score | game_date  |
+---------+-----------+-----------+--------------+--------------+------------+
|   10001 |      1001 |      1002 |          103 |          111 | 2019-04-01 |
|   10002 |      1002 |      1003 |          135 |          134 | 2019-04-10 |
+---------+-----------+-----------+--------------+--------------+------------+
2 rows in set (0.00 sec)
</div>2019-07-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/e6/6e/062da5e4.jpg" width="30px"><span>肥而不腻</span> 👍（8） 💬（1）<div>我理解，视图是一个查询结果集，随实体数据表数据变化而变化。</div>2019-08-09</li><br/><li><img src="" width="30px"><span>Geek_weizhi</span> 👍（8） 💬（1）<div>本文章对我帮助很大！</div>2019-07-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/48/f3/65c7e3ef.jpg" width="30px"><span>cricket1981</span> 👍（8） 💬（1）<div>视图都是只读的吗？</div>2019-07-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/f3/6a/6d82e7a3.jpg" width="30px"><span>暮雨</span> 👍（5） 💬（1）<div>视图查询效率很低</div>2019-11-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/11/2b/4053b256.jpg" width="30px"><span>醉红颜</span> 👍（4） 💬（2）<div>陈老师，您好！我这儿有个问题，当视图创建成功后，之后对相应表有更新，该视图会自动更新吗？</div>2019-09-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/17/f8/58/f02a565f.jpg" width="30px"><span>不才~</span> 👍（4） 💬（1）<div>视图创建之后会保留在数据库吗？以后可以调用吗？
</div>2019-08-08</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/ic8KF0sfxicsx4F25HZrtZwP2fQEibicfibFeYIQBibxnVlHIiaqkfictJuvLCKia0p7liaQvbTzCYWLibjJK6B8kc8e194ng/132" width="30px"><span>爱思考的仙人球</span> 👍（2） 💬（1）<div>视图的优点是隔绝数据表操作，可以对不同的用户提供不同的结果集，让用户只看到自己该看到的内容；缺点是灵活性差，有时候可能缺少想看的数据。</div>2019-10-17</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTKT9Tk01eiaQ9aAhszthzGm6lwruRWPXia1YYFozctrdRvKg0Usp8NbwuKBApwD0D6Fty2tib3RdtFJg/132" width="30px"><span>欧阳洲</span> 👍（1） 💬（1）<div>老师，视图主要作用是重用吗，
那视图与自定义函数的区别是什么呢？</div>2020-08-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/d8/4f/65abc6f0.jpg" width="30px"><span>KaitoShy</span> 👍（1） 💬（1）<div>视图优点：简单清晰，安全。
缺点：不能索引，不能有关联的触发器或默认值，不包含数据可能会有性能问题。
综上：我们现在平时很少会用到视图，可能是因为小项目，意义并不大。但是大项目的时候是不是会有性能问题呢？</div>2019-07-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/17/7f/21/8ef07609.jpg" width="30px"><span>Dawson</span> 👍（0） 💬（1）<div>那 通过视图去修改 视图展示的数据 是否会直接影响到原数据表</div>2019-12-16</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/19/69/bf/58f70a2a.jpg" width="30px"><span>程序员花卷</span> 👍（0） 💬（4）<div>视图的作用
对SQL的语句进行封装，提高SQL的复用率
可以完成复杂的连接
可以对数据进行格式化操作
简洁高效

视图是一张虚拟表，所以更新数据的时候并不会对实际的表产生影响</div>2019-12-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/b5/98/ffaf2aca.jpg" width="30px"><span>Ronnyz</span> 👍（0） 💬（2）<div>多基表视图不允许操作，单基表数据可以增删改，但新增是视图须包含基表中所有不允许为空的字段</div>2019-07-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/5a/5e/a897cb0d.jpg" width="30px"><span>grey927</span> 👍（0） 💬（1）<div>MySQL里面似乎不支持视图里面包含子查询，这种情况要如何解决呢？</div>2019-07-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/c7/40/66a203cd.jpg" width="30px"><span>忙碌了一天的周师傅</span> 👍（0） 💬（1）<div>个人理解视图可以类比下编程里类的概念，根据需求固定了相应的字段（类属性），MTV里的model就像视图，view就像select不同视图的动作。</div>2019-07-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/17/61/47/0a6e9729.jpg" width="30px"><span>竹影</span> 👍（0） 💬（2）<div>通过视图怎么会把原始数据删掉？
</div>2019-07-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/18/ee/a1ed60d1.jpg" width="30px"><span>ABC</span> 👍（0） 💬（1）<div>视图简化了查询,在另外一方面确实提供了更好的安全保障。只是不确定在数据很多的情况下，查询效率会不会比直接查询低一些。

</div>2019-07-08</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/DYAIOgq83eoT9nVNcyrunC5RjsOZwLObffWPgKnsCVcjctqFPNSK6j1XHNibDPQpBVmO6jyIemnepILyTIJ7SQw/132" width="30px"><span>canownu</span> 👍（0） 💬（3）<div>老师 如果是数据更新了 视图返回的结果是更新的还是旧的呢</div>2019-07-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/4a/c7/ec18673b.jpg" width="30px"><span>大斌</span> 👍（0） 💬（1）<div>我的理解是：
视图优点：减少命令输入，可以简化思考过程，方便自己后续查询和他人使用，
视图缺点：视图只适合用来封装查询，不存储数据，想要修改数据比较麻烦，不利于后期维护
总结：合理使用，不能滥用
视图在更新的时候不会影响到数据表，因为视图本身只是个查询命令封装，本身不存储数据，想通过视图对数据修改也有很多限制。</div>2019-07-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/7e/f5/85b5931b.jpg" width="30px"><span>LittleWanng</span> 👍（0） 💬（2）<div>视图是一个虚拟表，其实也就是一个SQL查询语句，在更新这个视图时，就像我们执行一条…新的查询语句，并不能改变原始数据表。</div>2019-07-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/f9/9f/515d1686.jpg" width="30px"><span>Sam</span> 👍（12） 💬（0）<div>视图可以理解成给一个查询SQL起个别名，以后想执行同样的SQL，就不需要每次都输入同样的SQL文本，只需要查询视图就可以了；
当然视图也有特殊的功能，比如权限控制，通过视图只开发特定的列的查询权限给其他人，还有物化视图。</div>2019-07-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/9a/64/94737463.jpg" width="30px"><span>我</span> 👍（11） 💬（0）<div>可是工作中我们实际都是将权限控制放到了代码层面去控制的，希望老师也能讲解下物化视图和普通视图区别及底层原理。</div>2019-07-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/36/a9/2437b1d9.jpg" width="30px"><span>化作春泥</span> 👍（7） 💬（4）<div>用视图查询效率比直接sql连接查询，效率怎么样？</div>2019-07-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/6a/a1/6270eeb7.jpg" width="30px"><span>极客星星</span> 👍（5） 💬（1）<div>你好  想问下  当我接到一个需求时  我可以创建一个新表来实现   也可以创建一个视图来实现  这两种之间应该如何做选择呢</div>2019-07-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/73/38/7ef1bd5d.jpg" width="30px"><span>Victor.</span> 👍（3） 💬（0）<div>每次打开视图是的时候，是不是想当于运营一个sql，视图的数据是否占用存储空间？
如果占用空间，那么视图作为一个虚拟表它占用的是内存空间，还是磁盘空间？
如果是内存空间，那么我每次运行的时候都需要查找一遍，对于服务器的资源占用很大？
如果仅作为一个sql的封装，调用视图我是否可以理解为，它首先得执行本身视图的sql，然后在能输出，简洁在sql上，然而对于服务器计算压力并没有缓解？</div>2019-11-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/57/4f/6fb51ff1.jpg" width="30px"><span>奕</span> 👍（3） 💬（2）<div>视图我的理解是对 SQL 查询语句的提前封装，不保存数据。所以更新视图的时候，只是更新提前封装好的查询语句，不会影响到数据表</div>2019-07-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1d/64/78/78c84aa5.jpg" width="30px"><span>滇池</span> 👍（2） 💬（0）<div>类似于Excel透视表</div>2020-07-03</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/8f/82/374f43a1.jpg" width="30px"><span>假装自己不胖</span> 👍（2） 💬（1）<div>视图在什么时候创建?在初始化的时候?什么时候消失?只要在drop的时候才会失效吗?如果是这样,那和表的区别也就不大了,虚拟表和真表有什么区别?</div>2019-07-15</li><br/>
</ul>