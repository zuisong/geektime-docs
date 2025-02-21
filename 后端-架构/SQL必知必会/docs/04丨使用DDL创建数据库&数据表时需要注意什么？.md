DDL是DBMS的核心组件，也是SQL的重要组成部分，DDL的正确性和稳定性是整个SQL运行的重要基础。面对同一个需求，不同的开发人员创建出来的数据库和数据表可能千差万别，那么在设计数据库的时候，究竟什么是好的原则？我们在创建数据表的时候需要注意什么？

今天的内容，你可以从以下几个角度来学习：

1. 了解DDL的基础语法，它如何定义数据库和数据表；
2. 使用DDL定义数据表时，都有哪些约束性；
3. 使用DDL设计数据库时，都有哪些重要原则。

## DDL的基础语法及设计工具

DDL的英文全称是Data Definition Language，中文是数据定义语言。它定义了数据库的结构和数据表的结构。

在DDL中，我们常用的功能是增删改，分别对应的命令是CREATE、DROP和ALTER。需要注意的是，在执行DDL的时候，不需要COMMIT，就可以完成执行任务。

1.**对数据库进行定义**

```
CREATE DATABASE nba; // 创建一个名为nba的数据库
DROP DATABASE nba; // 删除一个名为nba的数据库
```

2.**对数据表进行定义**

创建表结构的语法是这样的：

```
CREATE TABLE [table_name](字段名 数据类型，......)
```

### 创建表结构

比如我们想创建一个球员表，表名为player，里面有两个字段，一个是player\_id，它是int类型，另一个player\_name字段是`varchar(255)`类型。这两个字段都不为空，且player\_id是递增的。
<div><strong>精选留言（30）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/11/5f/27/a6873bc9.jpg" width="30px"><span>我知道了嗯</span> 👍（289） 💬（14）<div>外键多了会有很多维护问题吧？</div>2019-06-19</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/3hZfficKPGCq2kjFBu9SgaMjibJTEl7iaW1ta6pZNyiaWP8XEsNpunlnsiaOtBpWTXfT5BvRP3qNByml6p9rtBvqewg/132" width="30px"><span>夜路破晓</span> 👍（39） 💬（3）<div>类比自己，
主键就好比是我的身份证；
外键就好比我在各种团队组织中的身份，如在单位是员工和管理者、在家是儿子和丈夫、在协会是会员和委员等；
索引就好比是我的某些特征或者独树一帜的风格，玉树临风、风流倜傥之类的。</div>2019-06-19</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/3hZfficKPGCq2kjFBu9SgaMjibJTEl7iaW1ta6pZNyiaWP8XEsNpunlnsiaOtBpWTXfT5BvRP3qNByml6p9rtBvqewg/132" width="30px"><span>夜路破晓</span> 👍（20） 💬（3）<div>修改字段数据类型,报错,改写成:
ALTER TABLE player MODIFY column player_age float(3,1)
</div>2019-06-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/54/b2/5ea0b709.jpg" width="30px"><span>Danpier</span> 👍（11） 💬（3）<div>数据库管理工具墙裂推荐开源免费的 HeidiSQL（支持 MariaDB，MySQL，Microsoft SQL Server，PostgreSQL），运存占用低，很流畅，功能还全，Navicat 年费实在太贵了。</div>2019-07-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/0b/4e/fd946cb2.jpg" width="30px"><span>allean</span> 👍（11） 💬（1）<div>实际生产环境，更多的是用一个冗余字段取代外键吧？</div>2019-06-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/59/f6/ed66d1c1.jpg" width="30px"><span>chengzise</span> 👍（11） 💬（1）<div>我的理解：
主键：确保本表每行数据的唯一性
外键：与外表建立连接
索引：加快本表数据的查找</div>2019-06-19</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTICAILuSqtnAfl1zcgRWIULia2nbjzlybTEQJUMT68KPj80BicwQyibAK3Icxp4qwC03LqrtvfX0fbZg/132" width="30px"><span>番茄</span> 👍（6） 💬（2）<div> 直接写这段，会报错哦
create table player (
player_id int(11) NOT NULL AUTO_INCREMENT,
player_name varchar(255) NOT NULL
);
报错信息如下，所以是要设置主键吗：
Incorrect table definition; there can be only one auto column and it must be defined as a key</div>2019-08-07</li><br/><li><img src="" width="30px"><span>学习爱好者</span> 👍（4） 💬（1）<div>老师能给推荐几本关于SQL以及MySQL的书吗？市面上的书感觉讲的太零散，不系统，也不全面，看完之后总觉得缺少了很多知识点。希望老师能回复。</div>2019-10-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/1e/19/17245c59.jpg" width="30px"><span>Eglinux</span> 👍（4） 💬（1）<div>ALTER TABLE student DROP COLUMN player_age;
这里是 player 吧？</div>2019-06-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/a1/69/0ddda908.jpg" width="30px"><span>满怀</span> 👍（3） 💬（1）<div>主键：主键是一张表中唯一表示每一个行记录的属性
外键：外键是当子表中存在父表中的主键字段时，将子表中的字段设置为父表的外键，用于实现参照完整性
索引：类似书中的书签，索引就是表中的&quot;书签&quot;，根据索引字段存储记录信息，从而利用索引的快速查找功能，提高我们的SQL语句执行效率</div>2019-06-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/1a/66/2d9db9ed.jpg" width="30px"><span>苦行僧</span> 👍（3） 💬（1）<div>修改大表字段需要谨慎 容易引发表结构写锁</div>2019-06-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/18/2b/80/1f2bc7a8.jpg" width="30px"><span>‭</span> 👍（3） 💬（1）<div>创建表结构那里 是不是没把player_id设为主键</div>2019-06-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/f7/2f/da7f1a62.jpg" width="30px"><span>奋斗中的小神仙</span> 👍（2） 💬（1）<div>老师您好，这里写的是六个约束吧</div>2019-12-25</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/19/d6/e6/87234c32.jpg" width="30px"><span>木心云影</span> 👍（2） 💬（1）<div>首先，这门课程真心不错，非常感谢作者的用心。打个比方：语句最后以分号（;）作为结束符，最后一个字段的定义结束后没有逗号，这样一段，虽然很细微但是新手很容易犯错的问题，作者注意到且不厌其烦地指出来，足以证明作者的用心。另外，前端页面的划线功能，只有一种颜色，如果能够更加完善一下，比如可以改变线条颜色、改变粗细就够了。当然这有点吹毛求疵，不过既然是产品嘛，肯定是越完美越好。
作者留下的问题：
主键：保证每条记录的唯一性；
外键：建立表与表之间的关联性；
索引：提高查询效率。不过据说一个表索引也不是越多越好，要有一个度。</div>2019-11-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/72/65/68bd8177.jpg" width="30px"><span>雪飞鸿</span> 👍（2） 💬（1）<div>文中说有7种约束，只看到了主键、外键、惟一、Not Null、Default、Check六种约束。</div>2019-07-30</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/03/3f/09308258.jpg" width="30px"><span>雨先生的晴天</span> 👍（2） 💬（1）<div>主键：UNIQUE+NOT NUL
外键：确保表与表之间引用完整性，可以重复，可以为空。一个表中的外键对应另一张表的主键
检索：只是为了提高查询速度，对于字段没有唯一性的约束
</div>2019-06-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/5f/f0/a73607b3.jpg" width="30px"><span>victor666</span> 👍（2） 💬（1）<div>工程上不是少使用外键 应该是避免使用数据库层面的物理外键 使用逻辑外键来保存表的关系</div>2019-06-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/c7/40/66a203cd.jpg" width="30px"><span>忙碌了一天的周师傅</span> 👍（2） 💬（1）<div>老师。文章里create table的sql语句字段的单引号是普通的单引号吗？我看您写的像是反引号` `</div>2019-06-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/e9/0b/1171ac71.jpg" width="30px"><span>WL</span> 👍（2） 💬（1）<div>平时好像比较少用外键, 如果外键比较多会不会增加表之间的耦合度, 提高理解和维护的成本?</div>2019-06-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/18/f1/7e/8925aba5.jpg" width="30px"><span>小熊</span> 👍（1） 💬（1）<div>学习了</div>2020-04-03</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/AGicQgKibwja1SxkQ7oXQE8hYH7yCpiaicNHw3qZRuNB81aVDOQm9P1zd5F75Jbtv66G15D6ZjbbqfnoETR4321Zdw/132" width="30px"><span>高泽林</span> 👍（1） 💬（1）<div>三少一多！！！</div>2019-12-13</li><br/><li><img src="" width="30px"><span>Geek_d3a509</span> 👍（1） 💬（1）<div>主键：唯一标识一条记录，不能为空，不能重复。
外键：是用于建立和加强两个表数据之间的一列或多列，允许为空，可以重复。
索引：为了能够快速找到具有特定值的记录。
区别——主键只能有一个，一个表可以有多个外键，一个表可以有多个唯一索引</div>2019-12-04</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/oPPib2eqibMhUlnmFY7fLWuxSJibrBDrQUNZDTr7kSDNpFAeeNm8QibjO149R6Ddo6Lp8qtticGgstph5SKA2hcG8EQ/132" width="30px"><span>橙子冰</span> 👍（1） 💬（1）<div>老师，数据库在哪里下载</div>2019-10-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/34/d6/cc060875.jpg" width="30px"><span>嗯丶屌丝</span> 👍（1） 💬（1）<div>您好 sql 文件在那？</div>2019-08-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/ea/46/9c9808a9.jpg" width="30px"><span>Serendipity</span> 👍（1） 💬（1）<div>MySQL 版本：8.0.16

运行 ALTER TABLE player MODIFY (player_age FLOAT(3,1)) 报错：1064 - You have an error in your SQL syntax; check the manual that corresponds to your MySQL server version for the right syntax to use near &#39;(player_age FLOAT(3,1))&#39; at line 1, Time: 0.000000s

原因是什么呢？？
</div>2019-08-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/3a/a4/9d78ac16.jpg" width="30px"><span>邢雪</span> 👍（1） 💬（3）<div>老师你好，我这个一直报错，百度了我也不知道什么原因
alter table player modify(age float(3,1));
报错：
1064 - You have an error in your SQL syntax; check the manual that corresponds to your MySQL server version for the right syntax to use near &#39;(age float(3,1))&#39; at line 6</div>2019-07-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/eb/b8/22065888.jpg" width="30px"><span>小年</span> 👍（1） 💬（1）<div>刚来，还不晚，问一下老师，这个专栏大概更新到几月份会结束呢？9月份前可以更新完吗</div>2019-07-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/2d/56/5a1dce22.jpg" width="30px"><span>傅hc</span> 👍（1） 💬（1）<div>小白一枚，是用Navicat Premium还是Navicat for MySQL？我看课程有说MySQL和Oracle···</div>2019-07-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/b7/ba/ae4cabd8.jpg" width="30px"><span>仙道</span> 👍（1） 💬（2）<div>阿里java开发规范里面讲不要用外键</div>2019-06-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/44/a7/171c1e86.jpg" width="30px"><span>啦啦啦</span> 👍（1） 💬（1）<div>打卡</div>2019-06-20</li><br/>
</ul>