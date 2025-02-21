你好，我是刘超。今天我们来聊聊死锁，开始之前，先分享个小故事，相信你可能遇到过，或能从中获得一点启发。

之前我参与过一个项目，在项目初期，我们是没有将读写表分离的，而是基于一个主库完成读写操作。在业务量逐渐增大的时候，我们偶尔会收到系统的异常报警信息，DBA通知我们数据库出现了死锁异常。

按理说业务开始是比较简单的，就是新增订单、修改订单、查询订单等操作，那为什么会出现死锁呢？经过日志分析，我们发现是作为幂等性校验的一张表经常出现死锁异常。我们和DBA讨论之后，初步怀疑是索引导致的死锁问题。后来我们在开发环境中模拟了相关操作，果然重现了该死锁异常。

接下来我们就通过实战来重现下该业务死锁异常。首先，创建一张订单记录表，该表主要用于校验订单重复创建：

```
CREATE TABLE `order_record`  (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `order_no` int(11) DEFAULT NULL,
  `status` int(4) DEFAULT NULL,
  `create_date` datetime(0) DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `idx_order_status`(`order_no`,`status`) USING BTREE
) ENGINE = InnoDB
```

为了能重现该问题，我们先将事务设置为手动提交。这里要注意一下，MySQL数据库和Oracle提交事务不太一样，MySQL数据库默认情况下是自动提交事务，我们可以通过以下命令行查看自动提交事务是否开启：

```
mysql> show variables like 'autocommit';
+---------------+-------+
| Variable_name | Value |
+---------------+-------+
| autocommit    | ON    |
+---------------+-------+
1 row in set (0.01 sec)
```

下面就操作吧，先将MySQL数据库的事务提交设置为手动提交，通过以下命令行可以关闭自动提交事务：

```
mysql> set autocommit = 0;
Query OK, 0 rows affected (0.00 sec)
```
<div><strong>精选留言（30）</strong></div><ul>
<li><img src="https://wx.qlogo.cn/mmopen/vi_32/DYAIOgq83eotSSnZic41tGkbflx0ogIg3ia6g2muFY1hCgosL2t3icZm7I8Ax1hcv1jNgr6vrZ53dpBuGhaoc6DKg/132" width="30px"><span>张学磊</span> 👍（68） 💬（1）<div>MySQL默认开启了死锁检测机制，当检测到死锁后会选择一个最小(锁定资源最少得事务)的事务进行回滚</div>2019-08-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/9c/32/77e30b6e.jpg" width="30px"><span>ok</span> 👍（13） 💬（6）<div>老师，请问事例中insert order_record的事务AB中，请解答下疑惑，我描述如下
1、事务A执行select 4 for update获取（4,+∞）间隙锁
2、图中B事务再执行select 5 for update获取（5,+∞）的间隙锁 
3、事务A执行insert 4 发现事务A自己持有（4,+∞）间隙锁，所以不用等待呀！
4、事务B执行insert 5 发现事务A没有commit，持有（4,+∞）间隙锁，所以等待事务A释放锁
5、事务A提交，事务B insert 5获取到锁，commit

请指出问题…</div>2019-08-16</li><br/><li><img src="" width="30px"><span>ty_young</span> 👍（11） 💬（4）<div>老师您好，请问插入意向锁是一种表锁么</div>2020-04-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/d0/42/6fd01fb9.jpg" width="30px"><span>我已经设置了昵称</span> 👍（7） 💬（3）<div>老师。我们一般不会在查询的时候加上for update，我们的组长让我们事务中不要放查询语句，只能放插入或者更新，就是提前查好，组装好，然后开始执行事务。我觉得这其实会出现重复插入（并发量一高就会出现）。请问老师事务中真的不能做查询操作吗，还有查询的时候怎么防止同时两个事务查不到相对应的数据而造成重复插入</div>2019-08-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/46/d1/a1ddf49f.jpg" width="30px"><span>阿杜</span> 👍（4） 💬（3）<div>老师，有两个人闻到这个问题，感觉回答的我也不是很明白：
1:老师你最后放的那张图，为啥主健索引还需要获取非主键索引的锁啊，主键索引不是已经持有这一整行数据了么？
2.老师，您最后的那个例子，更新status时要获取index_order_status非聚簇索引，这句话能稍微解释一下吗？谢谢了
麻烦老师详细解答下。</div>2020-01-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/17/48/3ab39c86.jpg" width="30px"><span>insist</span> 👍（3） 💬（3）<div>事务 A 和事务 B 都持有间隙 (4,+∞）的 gap 锁，而接下来的插入操作为了获取到插入意向锁，都在等待对方事务的 gap 锁释放，于是就造成了循环等待，导致死锁
------------------
老师，请问一下，1、为什么A、B可以同时持有gap锁呢？2、为什么获取意向锁之前需要等待对方的gap锁呢？ 比较迷茫</div>2019-12-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/0d/9d/58d09086.jpg" width="30px"><span>达达队长</span> 👍（1） 💬（1）<div>老师这一句不懂：事务 A 和事务 B 都持有间隙 (4,+∞）的 gap 锁？
应该是：A是(4,+∞）B是(5,+∞）吧</div>2020-04-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/49/ef/02401473.jpg" width="30px"><span>月迷津渡</span> 👍（1） 💬（1）<div>一个表它的主键是UUID生成的，如果说为了避免幻读而加了一个Next-key lock，那它会怎么锁的，感觉后插入的位置待定。。。还是全表锁？</div>2019-10-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/89/a1/00d7330d.jpg" width="30px"><span>郭奉孝</span> 👍（0） 💬（1）<div>老师，为什么订单表校验重复订单不在主表而要用这么一张冗余表</div>2020-03-30</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/51/2f/7b04140c.jpg" width="30px"><span>孫やさん</span> 👍（0） 💬（4）<div>老师，您最后的那个例子，更新status时要获取index_order_status非聚簇索引，这句话能稍微解释一下吗？谢谢了</div>2019-12-25</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/cc/fe/702cf7bf.jpg" width="30px"><span>～</span> 👍（0） 💬（1）<div>老师， 我实践了一下， 发现select col from t where t.col = &#39;xx&#39; for update会导致覆盖索引失效,而使用使用共享锁就不会失效， 这是什么原理呢</div>2019-10-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/18/f8/3a/e0c14cb3.jpg" width="30px"><span>lizhibo</span> 👍（0） 💬（4）<div>老师 ，最后那个 根据主键ID 和 订单编号更新状态的例子 我这边怎么都是 锁等待 而没有出现死锁的情况， 事物级别RR </div>2019-10-04</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/10/bb/f1061601.jpg" width="30px"><span>Demon.Lee</span> 👍（0） 💬（1）<div>感悟：
1、默认将mysql隔离级别调成RC
2、使用主键更新

疑问：RR级别下，如果使用唯一索引更新，是record lock么？ </div>2019-09-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/67/f4/9a1feb59.jpg" width="30px"><span>钱</span> 👍（0） 💬（1）<div>课后思考及问题
1：有个疑问，文中说“插入意向锁其实也是一种 gap 锁，它与 gap lock 是冲突的，所以当其它事务持有该间隙的 gap lock 时，需要等待其它事务释放 gap lock 之后，才能获取到插入意向锁。”
在锁的兼容矩阵图中，先获取到Next-key lock再请求获取Insert Intention lock时是冲突的，反过来就是兼容的?</div>2019-09-15</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/23/f8/24fcccea.jpg" width="30px"><span>💢 星星💢</span> 👍（0） 💬（3）<div>老师你最后放的那张图，为啥主健索引还需要获取非主键索引的锁啊，主键索引不是已经持有这一整行数据了么？</div>2019-09-10</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/a5U0nqaicLy5ZJkESxBd5lMicNQcTTDK8vURyyWiabHxic7vS1VVk7HWTZg6ltyWJ3n9jb3Gq554ibfjsf7bv1v1Sdw/132" width="30px"><span>Geek_hp60mz</span> 👍（0） 💬（1）<div>老师，RC隔离级别下的select、update、delete基于聚簇索引和辅助索引分别获取什么lock？</div>2019-08-31</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/10/a6/4d2c933e.jpg" width="30px"><span>K</span> 👍（0） 💬（1）<div>老师您好，麻烦问一下：“如果使用辅助索引来更新数据库，就需要使用聚簇索引来更新数据库...”这句话是什么意思啊？</div>2019-08-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/5e/86/40877404.jpg" width="30px"><span>星星滴蓝天</span> 👍（0） 💬（1）<div>我们有一个很悲催的经历，更新的时候没有使用主键更新，之前还好好的，后来（服务迁移、降低配置......处理流程变长）很悲剧的死锁了。</div>2019-08-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/44/d7/915da418.jpg" width="30px"><span>阿琨</span> 👍（0） 💬（1）<div>老师，使用ON DUPLICATE KEY UPDATE这个是不是也可以解决这种呢</div>2019-08-16</li><br/><li><img src="" width="30px"><span>奇奇</span> 👍（0） 💬（1）<div>mysql本身自带死锁检测
超时时间在业务上是很难接受的</div>2019-08-15</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/49/7d/7b9fd831.jpg" width="30px"><span>Fever</span> 👍（0） 💬（1）<div>兼容矩阵图里的Gap锁和横向的Insert Intention不兼容吧。。</div>2019-08-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/15/69/187b9968.jpg" width="30px"><span>南山</span> 👍（0） 💬（1）<div>for update基本不被允许使用，除非经过review以及测试不会有死锁风险
对于锁机制，要很好的了解索引数据结构才能明白锁导致的奇怪现象是怎么出现的
</div>2019-08-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/e5/67/16322a5d.jpg" width="30px"><span>cky.宇</span> 👍（4） 💬（0）<div>感觉还可以把隔离级别改成RC。RR下锁比较严格，举两个例子：一个就是间隙锁的原因，就像老师的例子一样，如果一个事务在表t1 insert后没有commit，其他事务就不能对表t1进行insert，这样就可能会出现用户A的insert锁住了用户B的insert的情况，其实用户A和B是业务不相关的。而RC下没有间隙锁，不会有这种情况。 第二个就是RR加锁的范围更大，RR下会锁住所有扫描过的行，只有commit后才会全部释放，例如：select no from orders where status = 1 and create_at &gt; xx for update; 其中只有status有索引，那么mysql就要先扫描status索引再回表找满足create_at的行。如果是RR下，会锁住所有status=1的行，直到commit后释放。如果是RC下，当找到满足条件(status, craeted_at)的行后，会释放掉不满住条件但是status=1的行，不需要等到commit。这些细节都会造成RC和RR的性能差距很大。而一些需要重复读的需求可以通过代码来保证。  </div>2019-11-17</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/PiajxSqBRaEIvUlicgrWtibbDzwhLw5cQrDSy2JuE1mVvmXq11KQIwpLicgDuWfpp9asE0VCN6HhibPDWn7wBc2lfmA/132" width="30px"><span>a、</span> 👍（4） 💬（0）<div>1.设置Transaction的超时时间
2.设置Transaction的级别为串行化级别</div>2019-08-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1a/6c/70/934857f4.jpg" width="30px"><span>李飞</span> 👍（0） 💬（0）<div>对于文中的:

只在可重复读或以上隔离级别下的特定操作才会取得 gap lock 或 next-key lock，在 Select、Update 和 Delete 时，除了基于唯一索引的查询之外，其它索引查询时都会获取 gap lock 或 next-key lock，即锁住其扫描的范围。主键索引也属于唯一索引，所以主键索引是不会使用 gap lock 或 next-key lock。

不是很理解, 希望老师解答, 在 RR 隔离级别下, 如果有 SQL:  select * from table where num = 100 for update; , num 为唯一索引, 并且 num=100 查询不到数据, 按照我的想法是应该存在间隙锁的. </div>2023-08-04</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/d0/91/89123507.jpg" width="30px"><span>Johar</span> 👍（0） 💬（0）<div>老师，这个问题是不是也可以把orderNo设置为唯一索引？</div>2023-03-07</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/57/4f/6fb51ff1.jpg" width="30px"><span>奕</span> 👍（0） 💬（0）<div>gap lock 的范围不是根据数据库中已有的记录来确定的吗？</div>2021-10-16</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/ce/5e/b103d538.jpg" width="30px"><span>大明猩</span> 👍（0） 💬（0）<div>这种事务A,事务B同时执行时利用的多线程吗，还是单纯用的SQL语句</div>2021-09-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/ce/5e/b103d538.jpg" width="30px"><span>大明猩</span> 👍（0） 💬（1）<div>这种事务A，事务B的先后顺序是怎么模拟的不会搞啊</div>2021-09-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/26/3a/5c1f4d91.jpg" width="30px"><span>胖佳</span> 👍（0） 💬（0）<div>老师，能介绍一下mysql集群使用的ndbcluster引擎与innoDB在加锁方面的区别吗？</div>2021-09-07</li><br/>
</ul>