在MySQL里面，grant语句是用来给用户赋权的。不知道你有没有见过一些操作文档里面提到，grant之后要马上跟着执行一个flush privileges命令，才能使赋权语句生效。我最开始使用MySQL的时候，就是照着一个操作文档的说明按照这个顺序操作的。

那么，grant之后真的需要执行flush privileges吗？如果没有执行这个flush命令的话，赋权语句真的不能生效吗？

接下来，我就先和你介绍一下grant语句和flush privileges语句分别做了什么事情，然后再一起来分析这个问题。

为了便于说明，我先创建一个用户：

```
create user 'ua'@'%' identified by 'pa';
```

这条语句的逻辑是创建一个用户’ua’@’%’，密码是pa。注意，在MySQL里面，用户名(user)+地址(host)才表示一个用户，因此 ua@ip1 和 ua@ip2代表的是两个不同的用户。

这条命令做了两个动作：

1. 磁盘上，往mysql.user表里插入一行，由于没有指定权限，所以这行数据上所有表示权限的字段的值都是N；
2. 内存里，往数组acl\_users里插入一个acl\_user对象，这个对象的access字段值为0。

图1就是这个时刻用户ua在user表中的状态。
<div><strong>精选留言（29）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/13/e0/b9/bca7ff9a.jpg" width="30px"><span>way</span> 👍（80） 💬（7）<div>写个比较小的点：在命令行查询数据需要行转列的时候习惯加个\G ; 比如slave slave stauts \G ; 后来发现 ; 是多余的。列几个常用的
\G 行转列并发送给 mysql server
\g 等同于 ;
\! 执行系统命令
\q exit
\c 清除当前SQL（不执行）
\s mysql status 信息
其他参考 \h</div>2019-02-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/4f/78/c3d8ecb0.jpg" width="30px"><span>undifined</span> 👍（45） 💬（8）<div>权限的作用范围和修改策略总结：
http:&#47;&#47;ww1.sinaimg.cn&#47;large&#47;d1885ed1ly1g0ab2twmjaj21gs0js78u.jpg</div>2019-02-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/9b/a8/6a391c66.jpg" width="30px"><span>geraltlaush</span> 👍（34） 💬（2）<div>老师我使用delte删除用户，再创建用户都是失败，但是使用drop就可以了
mysql&gt; create user &#39;ua&#39;@&#39;%&#39; identified by &#39;L1234567890c-&#39;;
ERROR 1396 (HY000): Operation CREATE USER failed for &#39;ua&#39;@&#39;%&#39;
mysql&gt; drop user &#39;ua&#39;@&#39;%&#39;;
Query OK, 0 rows affected (0.00 sec)

mysql&gt; create user &#39;ua&#39;@&#39;%&#39; identified by &#39;L1234567890c-&#39;;
Query OK, 0 rows affected (0.01 sec)
是不是drop才会同时从内存和磁盘删除用户信息，但是delete只是从磁盘删除</div>2019-02-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/1c/5c/f5f24221.jpg" width="30px"><span>发芽的紫菜</span> 👍（31） 💬（7）<div>老师，联合索引的数据结构是怎么样的？到底是怎么存的？看了前面索引两章，还是不太懂，留言里老师说会在后面章节会讲到，但我也没看到，所以来此问一下？老师能否画图讲解一下</div>2019-02-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/f9/32/8ced1824.jpg" width="30px"><span>冰点18</span> 👍（15） 💬（1）<div>两三个月的时间，终于在上班地铁上读完了整部专栏，老师辛苦了！接下来就是搭建环境，二刷和验证了！一直有个问题，想问下老师，您用的画图工具是哪个？风格我特别喜欢，但是没找到</div>2019-04-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/a1/e6/50da1b2d.jpg" width="30px"><span>旭东(Frank)</span> 👍（14） 💬（3）<div>老师请教一个问题：MySQL 表设计时列表顺序对MySQL性能的影响大吗？对表的列顺序有什么建议吗？</div>2019-02-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/77/fd/c6619535.jpg" width="30px"><span>XD</span> 👍（11） 💬（1）<div>老师，我刚说的是acl_db，是在db切换的时候，从acl_dbs拷贝到线程内部的？类似acl_user。

session a
drop user &#39;test&#39;@&#39;%&#39;;
create user &#39;test&#39;@&#39;%&#39; identified by &#39;123456&#39;;
grant SELECT,UPDATE on gt.* to &#39;test&#39;@&#39;%&#39;;

session b   使用test登录
use gt;

session a
revoke SELECT,UPDATE on gt.* from &#39;test&#39;@&#39;%&#39;;

session b
show databases;  &#47;&#47;只能看到information_schema库
use gt;   &#47;&#47; Access denied for user &#39;test&#39;@&#39;%&#39; to database &#39;gt&#39;
show tables;   &#47;&#47;可以看到gt库中所有的表
select&#47;update  &#47;&#47;操作都正常</div>2019-02-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/57/6e/b6795c44.jpg" width="30px"><span>夜空中最亮的星</span> 👍（11） 💬（2）<div>通过老师的讲解 flush privileges 这回彻底懂了，高兴😃</div>2019-02-18</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTJCscgdVibmoPyRLRaicvk6rjTJxePZ6VFHvGjUQvtfhCS6kO4OZ1AVibbhNGKlWZmpEFf2yA6ptsqHw/132" width="30px"><span>夹心面包</span> 👍（8） 💬（2）<div>我在此分享一个授权库的小技巧, 如果需要授权多个库,库名还有规律,比如 db_201701 db_201702
可以采用正则匹配写一条 grant  on db______,每一个_代表一个字符.这样避免了多次授权,简化了过程。我们线上已经采用</div>2019-02-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/67/f4/9a1feb59.jpg" width="30px"><span>钱</span> 👍（6） 💬（1）<div>这篇容易消化，老师辛苦，你不讲这个，我想我很难发现这个细节，业务开发增删改查用的多，其他命令平时不咋用。
多玩才能发现更多好玩的，如果能有几个老师这样的朋友一起玩，那该有多好玩。</div>2019-08-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/30/8a/b5ca7286.jpg" width="30px"><span>业余草</span> 👍（5） 💬（2）<div>从学习中来，到实战中去！做了一个总结，可能写的不对，希望老师指点。https:&#47;&#47;mp.weixin.qq.com&#47;s&#47;7KGQGpm0IGaVjco6UjLeAQ</div>2019-06-27</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTJAibnPX9jW8kqLcIfibjic8GbkQkEUYyFKJkc39hZhibVlNrqwTjdLozkqibI2IwACd5YzofYickNxFnZg/132" width="30px"><span>Sinyo</span> 👍（3） 💬（2）<div>查一张大表，order_key字段值对应的最小createtime；
以前一直用方法一查数，后来同事说可以优化成方法二，查询效率比方法一高了几倍；
mysql特有的group by功能，没有group by的字段默认取查到的第一条记录；

方法一：
select distinct order_key
      ,createtime
  from (select order_key
              ,min(createtime) createtime
          from aaa
         group by order_key) a
  join aaa b
    on a.order_key = b.order_key
   and a.createtime = b.createtime

方法二：
select order_key
      ,createtime
  from (select order_key
              ,createtime
          FROM aaa
         order by createtime
       ) a
 group by order_key</div>2019-02-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/57/96/b65bdf43.jpg" width="30px"><span>萤火虫</span> 👍（1） 💬（1）<div>坚持到最后 为老师打call</div>2019-02-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/a1/a5/2100367c.jpg" width="30px"><span>舜</span> 👍（1） 💬（1）<div>老师，介绍完了order by后能不能继续介绍下group by的原理？等了好久了，一直想继续在order by基础上理解下group by，在使用过程中两者在索引利用上很相近，性能考虑也类似</div>2019-02-19</li><br/><li><img src="" width="30px"><span>爸爸回来了</span> 👍（1） 💬（1）<div>众所周知，sql是不区分大小写的。然而，涉及插件的变量却不是这样；上次在配置一个插件的参数的时候，苦思良久……最后发现了这个问题。难受😭</div>2019-02-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/77/fd/c6619535.jpg" width="30px"><span>XD</span> 👍（0） 💬（1）<div>老师，实际测试了下。
两个会话ab，登陆账号都为user。a中给user授予db1的select、update权限，b切换到db1，可以正常增改。然后a中回收该用户的db权限，b会话中的用户还是可以进行增改操作的。
我发现用户的db权限好像是在切换数据库的时候刷新的，只要不切换，grant操作并不会产生作用，所以acl_db是否也是维护在线程内部的呢？

以及，权限检验应该是在优化器的语义分析里进行的吧？</div>2019-02-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/e9/8e/6dc15a91.jpg" width="30px"><span>晨思暮语</span> 👍（0） 💬（2）<div>丁老师,您好：
关于上一章我留言的疑问,我重新整理了下。就是第十五章中老师留的思考题。
我模拟了老师的实验,结果有点出入,请老师帮忙看看，谢谢！
基础环境:
mysql&gt; select version();
+------------+
| version()  |
+------------+
| 5.7.22-log |
+------------+
1 row in set (0.00 sec)

mysql&gt; show variables like &#39;%tx%&#39;;
+---------------+-----------------+
| Variable_name | Value           |
+---------------+-----------------+
| tx_isolation  | REPEATABLE-READ |
| tx_read_only  | OFF             |
+---------------+-----------------+
2 rows in set (0.00 sec)
模拟实验:
session A:	                                         
mysql&gt; begin;	
mysql&gt; select * from t;	
+----+------+	
| id | a    |	
+----+------+	
|  1 |    2 |	
+----+------+	
1 row in set (0.00 sec)	

session B:                                          
mysql&gt; update t set a=3 where id=1;      
Query OK, 1 row affected (0.00 sec)      
Rows matched: 1  Changed: 1  Warnings: 0 	                                                  

SESSION A:                                                 
mysql&gt;  update t set a=3 where id=1;	
Query OK, 0 rows affected (0.00 sec)	
Rows matched: 1  Changed: 0  Warnings: 0	
&#47;*老师的实验显示为：1 rows affected*&#47;	
mysql&gt; select * from t where id=1;	
+----+------+	
| id | a    |	
+----+------+	
|  1 |    2 |	
+----+------+	
1 row in set (0.00 sec)	
&#47;*老师实验的查询结果为：1,3	*&#47;</div>2019-02-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/20/27/a6932fbe.jpg" width="30px"><span>虢國技醬</span> 👍（20） 💬（0）<div>老师的文章信息量(密度)很大，一般情况下得读好几遍，甚至读到头大；本篇是少有的几篇一口气读完能理解的，不容易啊 😂</div>2019-07-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/57/4f/6fb51ff1.jpg" width="30px"><span>奕</span> 👍（4） 💬（4）<div>为什么执行 grant 赋权的命令时，后面还要加上 with grant option 呢？ 试了一下不加也是可以的</div>2020-04-05</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/ce/d7/5315f6ce.jpg" width="30px"><span>不负青春不负己🤘</span> 👍（4） 💬（0）<div>我以前一直以为新增加的授权，只针对新的连接生效，对于已存在的权限，不生效，现在是对于某个用户授予全局的权限，对于已存在的连接不生效，对于 db,table 相关的权限是对于已存在的连接和新的连接都是立即生效</div>2020-03-05</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/06/36/d288bcc7.jpg" width="30px"><span>3e21</span> 👍（2） 💬（0）<div>老师，我有一个问题。在我们的程序中，往往会用到数据库连接池。在修改mysql一些全局配置时，往往只会对后续新建立的连接才生效。但是数据库连接池中那种老的连接就会一直是原来的配置。
这种情况我们是必须重启应用才行吗？
还有能大概说一下修改配置，只对后续新增的连接生效的配置的例子吗？
类似修改全局的事务隔离级别，sql_mode的参数好像也是</div>2021-06-07</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/76/8a/74cf038a.jpg" width="30px"><span>老K</span> 👍（1） 💬（1）<div>实测了一把：
连接A：
CREATE USER &#39;tester&#39; @&#39;%&#39; IDENTIFIED BY &#39;pa&#39;;

连接B：
使用 tester 登录正常连接

随后在连接A里面执行：
REVOKE ALL PRIVILEGES ON *.* 
FROM
	&#39;tester&#39; @&#39;%&#39;;

flush PRIVILEGES;

无论怎么着都可以使用 tester连接上来，这是怎么了？让人凌乱
只有 service mysql restart 方可生效.
MySQL 版本：5.5.6
使用的 Navicat 客户端</div>2021-01-25</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/25/35/91/d523a803.jpg" width="30px"><span>PRETEXT</span> 👍（0） 💬（0）<div>貌似修改用户密码需要flushprivilege,新链接才可以用新密码链接</div>2022-01-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/56/ea/32608c44.jpg" width="30px"><span>giteebravo</span> 👍（0） 💬（0）<div>
面对一个数据库，怎么发现有这类不规范的权限操作存在呢？
</div>2021-04-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/17/83/96/73ff13a0.jpg" width="30px"><span>天亮前说晚安</span> 👍（0） 💬（0）<div>线程内的权限是不是没法刷新的啊？因为flush只是同步内存中全局权限数组的值。</div>2020-03-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/35/6a/8ab55564.jpg" width="30px"><span>AlphaLiu</span> 👍（0） 💬（0）<div>在生产库进行全量备份：
mysqldump -uroot -p654321 --all-databases &gt; alldatabases.sql
在本地库恢复：
mysql -uroot -p123456 &lt; alldatabases.sql
恢复后，还是能使用mysql -uroot -p123456登录，
而mysql -uroot -p654321，不能登录。
必须flush privileges或者systemctl restart mysqld.service后，
恢复后的root密码才能生效。
请教下老师，这是什么原因？</div>2019-11-06</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/8Zs7gEMVq90uejXZMvA409gcln7d9TJgvOW5GQPSfSN0eOTgibhmyKvWltOrtRxdODXGl9zg1eUbAAfliaTicUKqQ/132" width="30px"><span>朝伟</span> 👍（0） 💬（0）<div>全局权限、对于一个已经存在的连接，它的全局权限不受 grant 命令的影响。那如果我要更新已建立连接的权限、怎么办、难道必须重新建立连接才能生效吗？</div>2019-07-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/8a/a7/674c1864.jpg" width="30px"><span>William</span> 👍（0） 💬（0）<div>从文中了解到, flush privileges 实际上就是保证磁盘与内存的数据一致性.
如果一致,那么无需执行(执行了也没关系, 但是属于画蛇添足), 
但是不一致, 就需要执行..


全局的权限修改, 不影响当前已有线程, 新线程建立采用新的权限.
而对于db 表 列 的 权限 操作, 实时生效. </div>2019-07-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/ef/af/adce8c49.jpg" width="30px"><span>wljs</span> 👍（0） 💬（0）<div>老师我想问个问题 我们公司一个订单表有110个字段 想拆分成两个表 第一个表放经常查的字段 第二个表放不常查的 现在程序端不想改sql，数据库端来实现 当查询字段中 第一个表不存在 就去关联第二个表查出数据  db能实现不？</div>2019-02-19</li><br/>
</ul>