在日常开发中，尤其是业务开发，少不了利用Java对数据库进行基本的增删改查等数据操作，这也是Java工程师的必备技能之一。做好数据操作，不仅仅需要对Java语言相关框架的掌握，更需要对各种数据库自身体系结构的理解。今天这一讲，作为补充Java面试考察知识点的完整性，关于数据库的应用和细节还需要在实践中深入学习。

今天我要问你的问题是，谈谈MySQL支持的事务隔离级别，以及悲观锁和乐观锁的原理和应用场景？

## 典型回答

所谓隔离级别（[Isolation Level](https://en.wikipedia.org/wiki/Isolation_%28database_systems%29#Isolation_levels)），就是在数据库事务中，为保证并发数据读写的正确性而提出的定义，它并不是MySQL专有的概念，而是源于[ANSI](https://en.wikipedia.org/wiki/American_National_Standards_Institute)/[ISO](https://en.wikipedia.org/wiki/International_Organization_for_Standardization)制定的[SQL-92](https://en.wikipedia.org/wiki/SQL-92)标准。

每种关系型数据库都提供了各自特色的隔离级别实现，虽然在通常的[定义](https://en.wikipedia.org/wiki/Isolation_%28database_systems%29#Isolation_levels)中是以锁为实现单元，但实际的实现千差万别。以最常见的MySQL InnoDB引擎为例，它是基于 [MVCC](https://dev.mysql.com/doc/refman/8.0/en/innodb-multi-versioning.html)（Multi-Versioning Concurrency Control）和锁的复合实现，按照隔离程度从低到高，MySQL事务隔离级别分为四个不同层次：

- 读未提交（Read uncommitted），就是一个事务能够看到其他事务尚未提交的修改，这是最低的隔离水平，允许[脏读](https://en.wikipedia.org/wiki/Isolation_%28database_systems%29#Dirty_reads)出现。
- 读已提交（Read committed），事务能够看到的数据都是其他事务已经提交的修改，也就是保证不会看到任何中间性状态，当然脏读也不会出现。读已提交仍然是比较低级别的隔离，并不保证再次读取时能够获取同样的数据，也就是允许其他事务并发修改数据，允许不可重复读和幻象读（Phantom Read）出现。
- 可重复读（Repeatable reads），保证同一个事务中多次读取的数据是一致的，这是MySQL InnoDB引擎的默认隔离级别，但是和一些其他数据库实现不同的是，可以简单认为MySQL在可重复读级别不会出现幻象读。
- 串行化（Serializable），并发事务之间是串行化的，通常意味着读取需要获取共享读锁，更新需要获取排他写锁，如果SQL使用WHERE语句，还会获取区间锁（MySQL以GAP锁形式实现，可重复读级别中默认也会使用），这是最高的隔离级别。
<div><strong>精选留言（21）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/12/22/8f/00468236.jpg" width="30px"><span>lizishushu</span> 👍（113） 💬（2）<div>mybatis架构自下而上分为基础支撑层、数据处理层、API接口层这三层。

基础支撑层，主要是用来做连接管理、事务管理、配置加载、缓存管理等最基础组件，为上层提供最基础的支撑。
数据处理层，主要是用来做参数映射、sql解析、sql执行、结果映射等处理，可以理解为请求到达，完成一次数据库操作的流程。
API接口层，主要对外提供API，提供诸如数据的增删改查、获取配置等接口。</div>2018-07-31</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/d1/87/b8308152.jpg" width="30px"><span>一首歌一种心情一段路</span> 👍（53） 💬（9）<div>悲观锁和乐观锁在哪儿用的.......平时写sql没接触过啊</div>2018-11-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/97/77/dac7d3b3.jpg" width="30px"><span>文彦</span> 👍（14） 💬（1）<div>晓峰老师。最近感觉基础有点差，开始看jdk的源码，主要是结合api来看。但是感觉事倍功半，有什么好的建议吗？</div>2018-11-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/ff/a5/eccc7653.jpg" width="30px"><span>clz1341521</span> 👍（13） 💬（2）<div>mysql inndb默认可重复读级别，不会出现幻读。
mybatis架构自下而上分为基础支撑层、数据处理层、API接口层这三层。

基础支撑层，主要是用来做连接管理、事务管理、配置加载、缓存管理等最基础组件，为上层提供最基础的支撑。
数据处理层，主要是用来做参数映射、sql解析、sql执行、结果映射等处理，可以理解为请求到达，完成一次数据库操作的流程。
API接口层，主要对外提供API，提供诸如数据的增删改查、获取配置等接口。</div>2018-08-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/51/0d/14d9364a.jpg" width="30px"><span>L.B.Q.Y</span> 👍（12） 💬（2）<div>mysql（innodb）的可重复读隔离级别下，为什么可以认为不会出现幻像读呢?</div>2018-07-31</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/99/af/d29273e2.jpg" width="30px"><span>饭粒</span> 👍（8） 💬（5）<div>SQL标准的隔离级别可重复读还是有幻读问题的。 InnoDB 和 XtraDB存储引擎 通过多版本并发控制（ MVCC， Multiversion Concurrency Control） 解决了幻读的问题。</div>2019-02-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/d4/f3/129d6dfe.jpg" width="30px"><span>李二木</span> 👍（5） 💬（2）<div>说到mybatis,就想起了分页，现在绝大多分页都用到了pagehelper插件，我想问下老师为啥mybatis没有设计一个好用的分页了？</div>2018-07-31</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/ae/cd/3bffed26.jpg" width="30px"><span>kitten</span> 👍（1） 💬（1）<div>mysql，可重复读的隔离级别，也在有gap间隙锁吧？</div>2018-08-01</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/1b/6b/4a6b774c.jpg" width="30px"><span>互联网联络员</span> 👍（0） 💬（1）<div>老师是不是写错了，在可重复读隔离级别中，基于锁的并发控制 DBMS实现保持读取和写入锁定（在选定数据上获取），直到事务结束。但是，range-locks没有被管理 ，因此可能会发生幻像读取。

事物的隔离级别增强分别解决由脏读、不可重复读再到幻读，只有串行化能解决三者，但是损失了效率。</div>2018-10-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/d8/d6/47da34bf.jpg" width="30px"><span>任鹏斌</span> 👍（13） 💬（6）<div>对于mysql四个隔离级别中的不可重复读的最后一句不是很理解。不可重复读应该是不能避免幻读，为什么说是不产生幻读呢？</div>2018-08-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/19/a1/d25786fc.jpg" width="30px"><span>郝国梁</span> 👍（6） 💬（0）<div>乐观锁 悲观锁 脏读 幻读 不可重复读 CAS MVCC 隔离级别 锁队列 2PC TCC</div>2018-07-31</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/a1/5d/6f754b1f.jpg" width="30px"><span>anji</span> 👍（4） 💬（0）<div>0.sql工厂-主要设定数据库连接信息
1.接口层-主要有mapper接口用于对外提供具体的sql执行方法
2.xml文件-有具体的sql实现语句，以及数据库字段对应java类字段的映射关系，每个mapper对应每个数据库表
</div>2018-07-31</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/56/54/abb7bfe3.jpg" width="30px"><span>Geek_j5i7lb</span> 👍（3） 💬（1）<div>杨老师 您好，关于“可以简单认为MySQL在可重复读级别不会出现幻象读”没能理解，个人认为正是因为可重复读，即每个事务保存了快照，才导致了幻读的现象。想要解决幻读，只能加共享锁或者排它锁吧。 可能是因为知识浅导致无法理解，还望方便的话，您能点拨一下，感谢</div>2018-08-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/bc/43/11acdc02.jpg" width="30px"><span>Allen</span> 👍（3） 💬（0）<div>请问什么时候可以细说一哈ORM映射😋</div>2018-08-01</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/46/0b/c57f4f43.jpg" width="30px"><span>sunnyrqw</span> 👍（1） 💬（0）<div>评论有说悲观锁和乐观锁在哪里用，说下我的理解
悲观锁和乐观锁是概念，如专栏说的
悲观锁是完全排他性的，我在执行的时候，你不能动，具体实现 java的synchronized、ReentrantLock
乐观锁就是我在执行的时候不限制你的操作，通过对比前后的值看有没人操作，没人操作就更新，有人操作就重来一次，具体实现是java cas</div>2020-10-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/18/45/9b/b11a2421.jpg" width="30px"><span>尚有智</span> 👍（1） 💬（2）<div>亲测后，发现一个问题，没搞懂，希望老师指点一下（自动提交修改成了手动提交）：
start transaction；
select * from  user where status = 0 and id = 1;
update user set status = 1 where id =1;
select * from user where status = 0 and id =1;
并未commit，第一个select能查询到数据，第二个select 不能查询到数据，我的理解是事务没有提交的时候，第二个select也能查询到数据，不清楚这个是怎么回事，isolation level 设置为read committed 和 repeatable read 都有这个问题，望解答！
</div>2020-01-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/10/7b/eed9d6d6.jpg" width="30px"><span>小笨蛋</span> 👍（1） 💬（0）<div>sql方面我们从来没有使用过悲观锁，一直都是用的乐观锁，怎么办？</div>2019-01-02</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/fb/8d/6c3cccc7.jpg" width="30px"><span>Dream</span> 👍（1） 💬（0）<div>MVCC到底有没有加锁？如何应用的？</div>2018-08-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/17/ba/ec/2b1c6afc.jpg" width="30px"><span>李飞</span> 👍（0） 💬（0）<div>数据库管理系统（DBMS）中的并发控制的任务是确保在多个事务同时存取数据库中同一数据时不破坏事务的隔离性和统一性以及数据库的统一性。

乐观并发控制(乐观锁)和悲观并发控制（悲观锁）是并发控制主要采用的技术手段。

无论是悲观锁还是乐观锁，都是人们定义出来的概念，可以认为是一种思想。其实不仅仅是关系型数据库系统中有乐观锁和悲观锁的概念，像memcache、hibernate、tair等都有类似的概念。

针对于不同的业务场景，应该选用不同的并发控制方式。所以，不要把乐观并发控制和悲观并发控制狭义的理解为DBMS中的概念，更不要把他们和数据中提供的锁机制（行锁、表锁、排他锁、共享锁）混为一谈。其实，在DBMS中，悲观锁正是利用数据库本身提供的锁机制来实现的。

当我们要对一个数据库中的一条数据进行修改的时候，为了避免同时被其他人修改，最好的办法就是直接对该数据进行加锁以防止并发。

这种借助数据库锁机制在修改数据之前先锁定，再修改的方式被称之为悲观并发控制（又名“悲观锁”，Pessimistic Concurrency Control，缩写“PCC”）。

在关系数据库管理系统里，悲观并发控制（又名“悲观锁”，Pessimistic Concurrency Control，缩写“PCC”）是一种并发控制的方法。它可以阻止一个事务以影响其他用户的方式来修改数据。如果一个事务执行的操作都某行数据应用了锁，那只有当这个事务把锁释放，其他事务才能够执行与该锁冲突的操作。
悲观并发控制主要用于数据争用激烈的环境，以及发生并发冲突时使用锁保护数据的成本要低于回滚事务的成本的环境中。

悲观锁，正如其名，它指的是对数据被外界（包括本系统当前的其他事务，以及来自外部系统的事务处理）修改持保守态度(悲观)，因此，在整个数据处理过程中，将数据处于锁定状态。 悲观锁的实现，往往依靠数据库提供的锁机制 （也只有数据库层提供的锁机制才能真正保证数据访问的排他性，否则，即使在本系统中实现了加锁机制，也无法保证外部系统不会修改数据）

在数据库中，悲观锁的流程如下：
在对任意记录进行修改前，先尝试为该记录加上排他锁（exclusive locking）。
如果加锁失败，说明该记录正在被修改，那么当前查询可能要等待或者抛出异常。 具体响应方式由开发者根据实际需要决定。
如果成功加锁，那么就可以对记录做修改，事务完成后就会解锁了。
其间如果有其他对该记录做修改或加排他锁的操作，都会等待我们解锁或直接抛出异常。</div>2020-05-16</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/E3XKbwTv6WTssolgqZjZCkiazHgl2IdBYfwVfAcB7Ff3krsIQeBIBFQLQE1Kw91LFbl3lic2EzgdfNiciaYDlJlELA/132" width="30px"><span>rike</span> 👍（0） 💬（0）<div>这个数据库的隔离级别个人认为是停留在理论的层次上，我在学习专栏《SQL必知必会》中，做过实验，按照例子中执行的实际结果跟隔离级别的定义不一样，不清楚这是在什么场景下才会出现这些问题。</div>2020-02-02</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/42/4f/ff1ac464.jpg" width="30px"><span>又双叒叕是一年啊</span> 👍（0） 💬（0）<div>不同的事务隔离级别分别怎么实现事务机制一样吗</div>2018-08-01</li><br/>
</ul>