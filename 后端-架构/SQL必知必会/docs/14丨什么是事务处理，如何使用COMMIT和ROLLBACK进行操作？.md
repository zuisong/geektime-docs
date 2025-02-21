我们知道在MySQL 5.5版本之前，默认的存储引擎是MyISAM，在5.5版本之后默认存储引擎是InnoDB。InnoDB和MyISAM区别之一就是InnoDB支持事务，也可以说这是InnoDB取代MyISAM的重要原因。那么什么是事务呢？事务的英文是transaction，从英文中你也能看出来它是进行一次处理的基本单元，要么完全执行，要么都不执行。

这么讲，你可能觉得有些抽象，我换一种方式讲。

不知道你是否遇到过这样的情况，你去家门口的小卖铺买东西，已经交了钱，但是老板比较忙接了个电话，忘记你是否交过钱，然后让你重新付款，这时你还要找之前的付款记录证明你已经完成了付款。

实际上如果我们线下的交易也能支持事务（满足事务的特性），就不会出现交了钱却拿不到商品的烦恼了，同样，对于小卖铺的老板来说，也不存在给出了商品但没有收到款的风险。总之，事务保证了一次处理的完整性，也保证了数据库中的数据一致性。它是一种高级的数据处理方式，如果我们在增加、删除、修改的时候某一个环节出了错，它允许我们回滚还原。正是因为这个特点，事务非常适合应用在安全性高的场景里，比如金融行业等。

我们今天就来学习下SQL中的事务。今天的课程你将重点掌握以下的内容：
<div><strong>精选留言（30）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/18/03/dd/e9f4c243.jpg" width="30px"><span>柔软的胖</span> 👍（63） 💬（1）<div>set autocommit=0;
BEGIN;
INSERT INTO test1 VALUES (&#39;a&#39;) ;
BEGIN;
INSERT INTO test1 VALUES (&#39;b&#39;);
INSERT INTO test1 VALUES (&#39;b&#39;);

在上面代码中，第一个BEGIN没有显示提交。在执行第二个BEGIN时，自动把第一个事务提交了。请问这是MYSQL中默认的行为吗？</div>2019-07-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/83/af/1cb42cd3.jpg" width="30px"><span>马以</span> 👍（18） 💬（1）<div>老师能不能穿插着一些工作环境中的实例来介绍呢？比如说事务的自动提交，生产当中我们要设置成自动提交还是不自动提交，是基于什么样的情况下才这样设计，这样就更容易理解了～，一个小建议</div>2019-07-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/92/ba/9833f06f.jpg" width="30px"><span>半瓶醋</span> 👍（11） 💬（1）<div>MySQL中InnoDB是支持事务的，MyISAM不支持事务的，可以通过SHOW ENGINES命令查看~
事务，简单来说就是：要么成功，要么失败。具体：四个特性（ACID）
A：原子性，不可分割；
C：一致性，无论事务是否提交成功，数据库的完整性约束不会改变，即会由原来的一致性状态变为另一种一致性状态；
I：隔离性，各个事务是独立的，不会互相影响；
D：持久性，一旦事务提交，对数据的修改是持久的，即使系统故障，修改依然有效。

----分割线---
记一下，加深印象~</div>2019-10-26</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/3hZfficKPGCq2kjFBu9SgaMjibJTEl7iaW1ta6pZNyiaWP8XEsNpunlnsiaOtBpWTXfT5BvRP3qNByml6p9rtBvqewg/132" width="30px"><span>夜路破晓</span> 👍（11） 💬（2）<div>事务是个有理想、有个性、讲爱憎的耿直BOY。跟这样的人打交道会很放心。</div>2019-07-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/01/00/326f3d4d.jpg" width="30px"><span>庞鑫华</span> 👍（9） 💬（1）<div>老师，什么时候能讲一下redo,undo log</div>2019-07-25</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/18/04/c8/c75f4f2d.jpg" width="30px"><span>张小倔</span> 👍（7） 💬（1）<div>文章中提到的保存点 savepoint，实用场景有哪些呢 </div>2019-09-04</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/17/9b/b1/74b04ee6.jpg" width="30px"><span>毛豆</span> 👍（6） 💬（4）<div>为什么一直重点在讲Mysql呢，oracle只是随口一提，而且oracle是有自动提交的，例如像create语句，oracle是自动提交</div>2019-07-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/33/07/8f351609.jpg" width="30px"><span>JustDoDT</span> 👍（4） 💬（2）<div>看着文章听一遍，然后在读文章实践一下。然后消化消化，然后1个小时学完一篇。
我是不是很菜。</div>2019-07-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/18/03/dd/e9f4c243.jpg" width="30px"><span>柔软的胖</span> 👍（3） 💬（1）<div>如果“INSERT INTO test SELECT &#39;关羽&#39;;”之后没有执行COMMIT，结果应该是空。
但是我执行出来的结果是&#39;关羽&#39;，为什么ROLLBACK没有全部回退。

代码如下
CREATE TABLE test(name varchar(255), PRIMARY KEY (name)) ENGINE=InnoDB;
BEGIN;
INSERT INTO test SELECT &#39;关羽&#39;;
BEGIN;
INSERT INTO test SELECT &#39;张飞&#39;;
INSERT INTO test SELECT &#39;张飞&#39;;
ROLLBACK;
SELECT * FROM test;
</div>2019-07-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/0f/71/9273e8a4.jpg" width="30px"><span>时间是最真的答案</span> 👍（3） 💬（4）<div>不知道作者在什么样的环境下操作的，我实验结果和你的不一样；
我的 MySQL8.0，使用 Navicat 12 操作的，实验结果都不一样
第一个实验，数据库中插入两条数据：关羽，张飞
第二个实验，数据库中插入两条数据：关羽，张飞
第三个实验，数据库中插入一条数据：关羽
麻烦老师回复一下</div>2019-07-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/10/bb/f1061601.jpg" width="30px"><span>Demon.Lee</span> 👍（3） 💬（1）<div>ACID 可以说是事务的四大特性，在这四个特性中，原子性是基础，隔离性是手段，一致性是约束条件，而持久性是我们的目的。
------以后面试就说这一句，如果问ACID</div>2019-07-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/ce/25/b9970aa8.jpg" width="30px"><span>我不是矿长</span> 👍（2） 💬（1）<div>学习了</div>2019-07-12</li><br/><li><img src="" width="30px"><span>hlz-123</span> 👍（2） 💬（1）<div>1.在MySQL中，只有InnoDB引擎支持事务，可以通过命令SHOW ENGINES查看
2.事务的特性，可以理解为完整性，在一个事务中的所有指令要么全部有效，要么全部失效，
                       如果有一部分语句成功，有一部分语句失败，数据库也会撤销成功的语句效果，
                       回滚到该事务执行前的状态。</div>2019-07-12</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/60IQmdia47hpG35UJwqXuL52DdibibQJ5vkOxbjP6hjdoLpZsfDPOLYZiar9M0QAiaCZckVl8ZENjMnKmFlvpv9Ur2w/132" width="30px"><span>tttttttttttt_SL</span> 👍（1） 💬（1）<div>看了四五遍懂了</div>2019-12-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/b5/98/ffaf2aca.jpg" width="30px"><span>Ronnyz</span> 👍（1） 💬（1）<div>作业：
SHOW ENGINES; 显示的引擎有：MEMORY、MRG_MYISAM、CSV 、FEDERATED 、PERFORMANCE_SCHEMA、 MyISAM  、InnoDB 、BLACKHOLE 、ARCHIVE ，其中只有InnoDB Supports transactions
事务的保存点就相当于存档吧</div>2019-07-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/4a/c7/ec18673b.jpg" width="30px"><span>大斌</span> 👍（1） 💬（1）<div>在mysql中用的最多的存储引擎有：innodb，bdb，myisam ,memory 等。其中innodb和bdb支持事务而myisam等不支持事务。

查看命令：show engines

对事务特性的理解：原子性是基础，隔离性是手段，一致性是约束条件，持久性是目的</div>2019-07-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/c7/40/66a203cd.jpg" width="30px"><span>忙碌了一天的周师傅</span> 👍（0） 💬（1）<div>老师，前面两个例子您应该也是在autocommit=1的环境下运行的吧，我这边不管这个参数是1还是0，事务里连续提交两个一样的name字段会报错然后也会添加上一条，除非rollback，所以您前面两个例子是不是举反了？</div>2019-07-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/08/ab/caec7bca.jpg" width="30px"><span>humor</span> 👍（0） 💬（2）<div>第一例子插入两条‘张飞’，应该是用rollback而不是commit吧，我测试的使用commit的话，会有一条&#39;张飞&#39;的记录持久化到了数据库中</div>2019-07-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/48/f3/65c7e3ef.jpg" width="30px"><span>cricket1981</span> 👍（0） 💬（4）<div>第二个例子结果也不同

mysql&gt; DROP TABLE test;
Query OK, 0 rows affected (0.02 sec)

mysql&gt; CREATE TABLE test(name varchar(255), PRIMARY KEY (name)) ENGINE=InnoDB;
Query OK, 0 rows affected (0.04 sec)

mysql&gt; BEGIN;
Query OK, 0 rows affected (0.00 sec)

mysql&gt; INSERT INTO test SELECT &#39;aaa&#39;;
Query OK, 1 row affected (0.00 sec)
Records: 1  Duplicates: 0  Warnings: 0

mysql&gt; COMMIT;
Query OK, 0 rows affected (0.02 sec)

mysql&gt; INSERT INTO test SELECT &#39;bbb&#39;;
Query OK, 1 row affected (0.00 sec)
Records: 1  Duplicates: 0  Warnings: 0

mysql&gt; INSERT INTO test SELECT &#39;bbb&#39;;
ERROR 1062 (23000): Duplicate entry &#39;bbb&#39; for key &#39;PRIMARY&#39;
mysql&gt; ROLLBACK;
Query OK, 0 rows affected (0.00 sec)

mysql&gt; SELECT * FROM test;
+------+
| name |
+------+
| aaa  |
+------+
1 row in set (0.00 sec)
</div>2019-07-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/48/f3/65c7e3ef.jpg" width="30px"><span>cricket1981</span> 👍（0） 💬（3）<div>为什么我试下来的结果跟老师说的不一样呢？

mysql&gt; set autocommit=0;
Query OK, 0 rows affected (0.00 sec)

mysql&gt; 
mysql&gt; DROP TABLE test;
Query OK, 0 rows affected (0.02 sec)

mysql&gt; CREATE TABLE test(name varchar(255), PRIMARY KEY (name)) ENGINE=InnoDB;
Query OK, 0 rows affected (0.05 sec)

mysql&gt; BEGIN;
Query OK, 0 rows affected (0.00 sec)

mysql&gt; INSERT INTO test SELECT &#39;aaa&#39;;
Query OK, 1 row affected (0.00 sec)
Records: 1  Duplicates: 0  Warnings: 0

mysql&gt; COMMIT;
Query OK, 0 rows affected (0.02 sec)

mysql&gt; BEGIN;
Query OK, 0 rows affected (0.00 sec)

mysql&gt; INSERT INTO test SELECT &#39;bbb&#39;;
Query OK, 1 row affected (0.00 sec)
Records: 1  Duplicates: 0  Warnings: 0

mysql&gt; INSERT INTO test SELECT &#39;bbb&#39;;
ERROR 1062 (23000): Duplicate entry &#39;bbb&#39; for key &#39;PRIMARY&#39;
mysql&gt; COMMIT;
Query OK, 0 rows affected (0.01 sec)

mysql&gt; SELECT * FROM test;
+------+
| name |
+------+
| aaa  |
| bbb  |
+------+
2 rows in set (0.00 sec)</div>2019-07-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/8e/0a/31ec5392.jpg" width="30px"><span>挠头侠</span> 👍（11） 💬（2）<div>老师，在第一个例子中，在第二个begin中插入了两个 ‘张飞’ ，但是执行时发生错误，不是说错误会回滚吗？为什么我们还需要指定 ROLLBACK？

如果将第一个例子中的ROLLBACK 改成COMMIT 为什么会有一条 ‘张飞’ 插入成功呢？这两个insert不应该是一个事务内吗？不应该都进行回滚吗？</div>2019-08-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/19/00/bb/25a29311.jpg" width="30px"><span>森鱼</span> 👍（9） 💬（0）<div>你好，在总结部分之前，音频中有一段“DELIMITER”操作方式，我看文本中并没有相应的段落，可否有空让工作人员补上？谢谢！</div>2019-09-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/8e/9e/7b4aa967.jpg" width="30px"><span>Tyrant</span> 👍（4） 💬（1）<div>我发现在navicat里，rollback完全没用，不知道为啥</div>2019-09-10</li><br/><li><img src="" width="30px"><span>知行合一</span> 👍（3） 💬（3）<div>为什么在navicat中，我和老师的代码一致。但是，实验结果，总是不同。 张飞，每次都被存进去了。很不理解！能说说吗？ 谢谢</div>2019-10-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/67/80/4e52c16f.jpg" width="30px"><span>演</span> 👍（3） 💬（5）<div>CREATE TABLE test(name varchar(255), PRIMARY KEY (name)) ENGINE=InnoDB;
BEGIN;
INSERT INTO test SELECT &#39;关羽&#39;;
COMMIT;
INSERT INTO test SELECT &#39;张飞&#39;;
INSERT INTO test SELECT &#39;张飞&#39;;
ROLLBACK;
SELECT * FROM test;

老师 后面两次插入张飞不在一个事务里是什么意思？这两次插入前面也没有begin</div>2019-07-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/05/88/0a1f1b1d.jpg" width="30px"><span>linus</span> 👍（3） 💬（3）<div>DROP TABLE test;
CREATE TABLE test(name varchar(255), PRIMARY KEY (name)) ENGINE=InnoDB;
set autocommit=0;
BEGIN;
INSERT INTO test SELECT &#39;aaa&#39;;
COMMIT;
BEGIN;
INSERT INTO test SELECT &#39;bbb&#39;;
INSERT INTO test SELECT &#39;bbb&#39;;
ROLLBACK;
SELECT * FROM test;

为什么我的结果还是
 aaa
 bbb</div>2019-07-15</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/41/87/46d7e1c2.jpg" width="30px"><span>Better me</span> 👍（1） 💬（1）<div>老师您好，数据库事务的隐式提交和显式提交分别有什么使用场景，能否具体举例说明下。</div>2019-07-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/14/c4/e354d8ba.jpg" width="30px"><span>魏颖琪</span> 👍（1） 💬（0）<div>在我的实验中，事务出现错误是不会自动回滚，必须显式有 ROLLBACK 命令。如果使用sql client工具，那很可能是工具进行了判断，并做了自动处理。如果在mysql client的命令行中，不会遇错自动回滚。</div>2019-07-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/0b/18/b82d4617.jpg" width="30px"><span>mocobk</span> 👍（1） 💬（1）<div>
Mysql中什么情况下会用到显示事务？</div>2019-07-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/67/f4/9a1feb59.jpg" width="30px"><span>钱</span> 👍（0） 💬（0）<div>事务，数据库核心内容之一，四大特性很容易理解，理解如何实现更为重要。</div>2024-08-20</li><br/>
</ul>