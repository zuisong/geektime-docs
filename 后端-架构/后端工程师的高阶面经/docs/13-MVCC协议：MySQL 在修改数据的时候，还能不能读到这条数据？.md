你好，我是大明。今天我们来学习 MySQL 面试中非常重要的一个内容—— MVCC 协议。

MVCC（Multi-Version Concurrency Control）中文叫做多版本并发控制协议，是 MySQL InnoDB 引擎用于控制数据并发访问的协议。它在面试中属于必面题，而且从 MVCC 出发能够将话题引申到事务、隔离级别两个重头戏上，所以掌握 MVCC 能让你进可攻退可守。

那么今天我就带你从 MVCC 的基本原理开始讲起，教你怎么在 MVCC 的面试中进退自如，秀出实力。在开始之前，我们先思考一个问题，为什么 InnoDB 会需要 MVCC？

## 为什么需要 MVCC？

你在前面已经学过了锁，知道锁本身就是用于并发控制的，那么为什么 InnoDB 还需要引入 MVCC，读写都加锁不就可以控制住并发吗？

锁确实可以，但是性能太差。如果是纯粹的锁，那么写和写、读和写、读和读之间都是互斥的。如果是读写锁，那么写和写、读和写之间依旧是互斥的。

数据库和一般的应用有一个很大的区别，就是**数据库即便是读，也不能被写阻塞住。**试想一下，如果一个线程准备执行 UPDATE 一行数据，如果这时候阻塞住了所有的 SELECT 语句，那么这个性能你能接受吗？

![图片](https://static001.geekbang.org/resource/image/a0/02/a031e076bb10c09dff987230ac68df02.png?wh=1920x787)

显然接受不了，所以数据库要有一种机制，避免读写阻塞。在理解了为什么 MVCC 必不可少之后，现在你需要进一步了解一个和 MVCC 紧密关联的概念：**隔离级别**。
<div><strong>精选留言（24）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/2a/44/e6/2c97171c.jpg" width="30px"><span>sheep</span> 👍（5） 💬（1）<div>有一个加锁的问题？
可重复读由于加了next-key lock防止了幻读，这里加了锁叫next-key lock。
那读提交情况下，就不会加锁了么，都是靠read view来获取数据？update和delete下，读提交也不会加锁了么</div>2023-10-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/44/e0/a6a51198.jpg" width="30px"><span>nirvana</span> 👍（2） 💬（1）<div>请问下老师，有推进数据库改成rc真实案例的结果么，比如改成rc后，死锁减少了百分之多少，数据库压力减少了百分之多少</div>2023-08-23</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/bvj76PmeUvW8kokyu91IZWuRATKmabibDWbzAj2TajeEic7WvKCJOLaOh6jibEmdQ36EO3sBUZ0HibAiapsrZo64U8w/132" width="30px"><span>梦倚栏杆</span> 👍（1） 💬（1）<div>是引入mvcc之后，对于读写来说，原来读加的读锁不再加了？还是说写锁加的逻辑时机变了？</div>2023-12-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/a3/f2/ab8c5183.jpg" width="30px"><span>Sampson</span> 👍（1） 💬（3）<div>你好，为什么使用了临健锁之后，可重复读的幻读问题解决了呢</div>2023-08-15</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/39/24/963178c4.jpg" width="30px"><span>rrbbt</span> 👍（1） 💬（8）<div>老师讲的确实很精彩，但有个问题没明白：可重复读的情况下，看不到别的事物的修改结果，当前事物还是基于老数据去修改，这时候最后的结果不会出问题吗？这个怎么解决呢？（我感觉mysql应该用读已提交才对啊，因为别人已经把数据改了，我再改的话，肯定得基于最新的数据去改啊，为什么mysql要默认设置成可重复读呢？）</div>2023-07-14</li><br/><li><img src="" width="30px"><span>Geek_2493f9</span> 👍（0） 💬（1）<div>关于rc和rr的执行过程中上锁的过程， 独占锁，行级锁，间隙锁相关的问题老师咋不讲讲</div>2024-04-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/33/7a/ac307bfc.jpg" width="30px"><span>到不了的塔</span> 👍（0） 💬（1）<div>邓明老师，请问下，为什么mysql在读已提交隔离级别下会比可重复读隔离级别下性能更好？
比如不带锁的select语句查询，性能应该差不多吧，甚至可重复读的性能更好（因为可能不需要生成读快照）。</div>2024-02-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/f2/2e/cb647708.jpg" width="30px"><span>起风了</span> 👍（0） 💬（1）<div>m_up_limit_id 在左边，而 m_low_limit_id 在右边 这块能再详细讲吗 </div>2024-01-04</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/bvj76PmeUvW8kokyu91IZWuRATKmabibDWbzAj2TajeEic7WvKCJOLaOh6jibEmdQ36EO3sBUZ0HibAiapsrZo64U8w/132" width="30px"><span>梦倚栏杆</span> 👍（0） 💬（2）<div>感觉幻读和不可重复读是一回事，他俩的区别是啥呀？</div>2023-12-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1d/e0/cc/a8c26fb2.jpg" width="30px"><span>okkkkk</span> 👍（0） 💬（1）<div>readview的几张图太棒了，很有收获，感谢</div>2023-11-29</li><br/><li><img src="" width="30px"><span>Geek_035c60</span> 👍（0） 💬（1）<div>已提交读，读已提交，是否可以统一一下称呼。</div>2023-11-16</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/08/b8/ac8a778e.jpg" width="30px"><span>我得儿意的笑</span> 👍（0） 💬（1）<div>你好老师，在已提交读的情况下，直接读最后一次提交的数据就可以了，为什么还需要readview?</div>2023-10-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/da/d9/f051962f.jpg" width="30px"><span>浩仔是程序员</span> 👍（0） 💬（1）<div>老师你好，为什么可以同时多个事务修改同一条数据呢，第一个事务要修改时候不会对这条记录加锁吗？其他事务不是等待拿到锁？</div>2023-09-03</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/da/d9/f051962f.jpg" width="30px"><span>浩仔是程序员</span> 👍（0） 💬（1）<div>老师你好，这个版本链是一直维护的吗？还是执行完事务之后会断开这条链</div>2023-09-03</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/dc/08/64f5ab52.jpg" width="30px"><span>陈斌</span> 👍（0） 💬（1）<div>这里尤其要注意一点，就是理论上来说可重复读是没有解决幻读的。但是 MySQL 因为使用了临键锁，因此它的可重复读隔离级别已经解决了幻读问题。你在面试的过程中不要忘了强调这一点。

有人知道为啥吗，解释一下，是不是如下原因：

如果是范围查询SQL语句的话，如果没有临建锁，查询出来的数据会变多，导致不一致。例如 where id &lt; 3 for update, 如果没有临建锁把[4, 正无穷）的记录锁住，那么会导致查出的数据会不一致吗？

</div>2023-07-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/08/ab/caec7bca.jpg" width="30px"><span>humor</span> 👍（0） 💬（1）<div>MySQL 在可重复读这个隔离级别下，查询的执行效果和快照读非常接近。
在rr隔离级别下，查询不就是快照读吗，为什么说和快照读非常接近呢？</div>2023-07-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/08/ab/caec7bca.jpg" width="30px"><span>humor</span> 👍（0） 💬（1）<div>rc为什么比rr性能更好呢，ru级别下是否还有锁呢</div>2023-07-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/1e/cf/97cd8be1.jpg" width="30px"><span>so long</span> 👍（0） 💬（2）<div>老师你好，请教一个问题。多个事物并发更新同一条数据，应该会加记录锁，同一时间这条数据最多就一个活跃的事物。老师上文所讲的Read View m_ids会存在多条活跃的事物，什么情况下会出现多条活跃事物呢？</div>2023-07-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/25/87/f3a69d1b.jpg" width="30px"><span>peter</span> 👍（0） 💬（4）<div>请教老师两个问题：
Q1：快照读，当前读，是怎么指定的？SQL语句中指定吗？
Q2：用版本链的话，一行记录会生成多个备份。数据库会有很多读、写，就会有很多行的版本链，这样会占用很多内存吗？</div>2023-07-15</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/d0/91/89123507.jpg" width="30px"><span>Johar</span> 👍（0） 💬（1）<div>1.读未提交，每次都查询最新的数据即可；串行化，由于代码是串行，所以每次直接读取即可。
2.计算客户的账单，需要保证整个事务读取的数据是一致的</div>2023-07-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/54/9a/76c0af70.jpg" width="30px"><span>每天晒白牙</span> 👍（0） 💬（0）<div>READ UNCOMMITTED：直接读取最新的数据行，不使用 MVCC，也不加锁。允许脏读，性能较高，但数据一致性较差。
SERIALIZABLE：通过加锁机制（共享锁、排他锁和间隙锁）来实现完全隔离，防止脏读、不可重复读和幻读。数据一致性最高，但并发性能较低。</div>2024-07-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/f8/c4/c7f665df.jpg" width="30px"><span>一块跑跑</span> 👍（0） 💬（0）<div>课程中面试准备部分“如果这时候你回答读取到事务 101 的数据，那么面试官就进一步追问。如果这时候事务 103 提交了，但是 102 还没提交，那么会读到谁的呢？”

针对同一行的数据，102未提交的情况下103是不可能提交的，会一直阻塞等待102提交后才执行吧</div>2024-04-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/09/b1/0750daba.jpg" width="30px"><span>哈哈哈</span> 👍（0） 💬（1）<div>老师，有个问题我和您理解的不一样。
RR下，如果A和B两个事务，A事务先进行快照读，然后B事务执行Insert且提交，然后A继续在原有的事务里执行Update所有记录，然后A事务再进行一次快照读，这时候在A这里，出现了幻读。所以可重复读级别下，即使使用临键锁，也没有完全解决幻读问题。</div>2024-03-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/17/94/8e/c611687c.jpg" width="30px"><span>学无涯</span> 👍（0） 💬（0）<div>--- 可重复读：事务开始的时候，创建出 Read View。</div>2024-01-03</li><br/>
</ul>