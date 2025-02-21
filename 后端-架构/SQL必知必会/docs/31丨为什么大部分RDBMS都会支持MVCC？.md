上一篇文章中，我们讲到了锁的划分，以及乐观锁和悲观锁的思想。今天我们就来看下MVCC，它就是采用乐观锁思想的一种方式。那么它到底有什么用呢？

我们知道事务有4个隔离级别，以及可能存在的三种异常问题，如下图所示：

![](https://static001.geekbang.org/resource/image/c2/9b/c2e9a4ce5793b031f3846890d0f6189b.png?wh=1331%2A694)  
在MySQL中，默认的隔离级别是可重复读，可以解决脏读和不可重复读的问题，但不能解决幻读问题。如果我们想要解决幻读问题，就需要采用串行化的方式，也就是将隔离级别提升到最高，但这样一来就会大幅降低数据库的事务并发能力。

有没有一种方式，可以不采用锁机制，而是通过乐观锁的方式来解决不可重复读和幻读问题呢？实际上MVCC机制的设计，就是用来解决这个问题的，它可以在大多数情况下替代行级锁，降低系统的开销。

![](https://static001.geekbang.org/resource/image/56/a0/568bb507e1edb431d8121a2cb5c7caa0.png?wh=1500%2A552)  
今天的课程主要包括以下几个方面的内容：

1. MVCC机制的思想是什么？为什么RDBMS会采用MVCC机制？
2. 在InnoDB中，MVCC机制是如何实现的 ？
3. Read View是如何工作的？

## MVCC是什么，解决了什么问题

MVCC的英文全称是Multiversion Concurrency Control，中文翻译过来就是多版本并发控制技术。从名字中也能看出来，MVCC是通过数据行的多个版本管理来实现数据库的并发控制，简单来说它的思想就是保存数据的历史版本。这样我们就可以通过比较版本号决定数据是否显示出来（具体的规则后面会介绍到），读取数据的时候不需要加锁也可以保证事务的隔离效果。
<div><strong>精选留言（30）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/0f/4d/fd/0aa0e39f.jpg" width="30px"><span>许童童</span> 👍（42） 💬（4）<div>我来回答一下思考题：
为什么隔离级别为读未提交时，不适用于 MVCC 机制呢？
因为隔离级别是读未提交，所以跟本就不需要版本控制，直接读取最新的数据就好了。

读已提交和可重复读这两个隔离级别的 Read View 策略有何不同？
读已提交每一次Select都会重新查询Read View，保证可以读到其它事务的提交。
可重复读会复用第一次查询到的Read View,不会读到其它事务的提交，加上Next-Key锁的配合，从而避免幻读。</div>2019-08-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/46/d0/6bafd7d4.jpg" width="30px"><span>DZ</span> 👍（22） 💬（1）<div>1. 为什么隔离级别为读未提交时，不适用于 MVCC 机制呢？

“读未提交”隔离级别不需要多版本数据。每个事务都读取最新数据，假设事务A把X从0改成1，无论事务A是否提交，事务B读到X为1，如果事务A回滚，事务B再次读X，自然就得到0，根本不需要MVCC帮衬。

2. 读已提交和可重复读这两个隔离级别的 Read View 策略有何不同？

“读已提交”时，每次SELECT操作都创建Read View，无论SELECT是否相同，所以可能出现前后两次读到的结果不等，即不可重复读。
“可重复读”时，首次SELECT操作才创建Read View并复用给后续的相同SELECT操作，前后两次读到的结果一定相等，避免了不可重复读。</div>2019-08-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/d7/45/d1621188.jpg" width="30px"><span>学渣汪在央企打怪升级</span> 👍（3） 💬（1）<div>内容量大，看了三遍，感觉有点懂了</div>2020-03-25</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/49/85/3f161d95.jpg" width="30px"><span>Alpha</span> 👍（2） 💬（5）<div>Step 4. 如果不符合Read View 规则，就需要从Undo Log中获取历史快照。不太明白这里的&quot;Read View规则&quot;指的是什么？</div>2019-08-21</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTJqWuvuicHD7RVlEDJamWNmwVdkjeH4pLxPXoicwqbnpOibI1MFFz9SIVJmQeKSZQRP9np1NUV3wpmnA/132" width="30px"><span>编码者</span> 👍（1） 💬（1）<div>这块有点难~</div>2019-12-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/cd/c1/19531313.jpg" width="30px"><span>innovationmech</span> 👍（1） 💬（1）<div>看了几遍文章和留言，有点懂了。。。</div>2019-09-16</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/16/5b/83a35681.jpg" width="30px"><span>Monday</span> 👍（13） 💬（0）<div>以为我看不懂，却原来只是恐惧学习mvcc，仔细看，3、5遍再结合《mysql45讲》的几节，慢慢琢磨品味，终于明白些了。继续学习，比昨天的自己更优秀</div>2020-05-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/ed/1a/269eb3d6.jpg" width="30px"><span>cfanbo</span> 👍（6） 💬（3）<div>如图所示，trx_ids 为 trx2、trx3、trx5 和 trx8 的集合，活跃的最大事务 ID（low_limit_id）为 trx10，活跃的最小事务 ID（up_limit_id）为 trx4。

没理解这个10和4怎么来的，不是说就2 3 5 8这个活跃事务吗？</div>2019-08-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/e0/2f/3aee5f24.jpg" width="30px"><span>宋雄斌</span> 👍（3） 💬（4）<div>RR  为什么还是会产生幻读呀，后面事务插入的数据它们的事务ID不应该比第一次获取的Read View 的事务ID大吗，那么后面插入的数据不应该看不到的吗？？</div>2020-07-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/a1/87/259ab5a3.jpg" width="30px"><span>桂冠远航</span> 👍（3） 💬（0）<div>老师应该少说了一个细节，就是要对height加索引，因为不加索引的update操作是表锁。</div>2020-04-15</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/DYAIOgq83erbY9UsqHZhhVoI69yXNibBBg0TRdUVsKLMg2UZ1R3NJxXdMicqceI5yhdKZ5Ad6CJYO0XpFHlJzIYQ/132" width="30px"><span>饭团</span> 👍（3） 💬（0）<div>重读第二遍  才理解了真谛  真是读书百遍  其义自见！</div>2020-01-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/76/23/31e5e984.jpg" width="30px"><span>空知</span> 👍（3） 💬（0）<div>老师 问下：
1、如果RV不符合 就需要去Undo Log里面去判断快照记录了，这里对于快照记录 会一直比较下去直到找到一个可见版本 或者查询全部历史版本为止？
2、间隙锁 锁住一个范围不包含 行记录本身，是指 对某条记录添加间隙锁之后 还可以针对这条记录本身做修改操作吗？</div>2019-08-31</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/41/bb/21ce60d2.jpg" width="30px"><span>安静的boy</span> 👍（3） 💬（2）<div>想说一下最后一个列子，innodb是如何解决幻读的。作者举的例子是innodb在当前读的情况下如何解决幻读（通过加next-key 锁）。如果在快照读下，利用readView就可以解决了。</div>2019-08-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/17/0f/5f/355f409e.jpg" width="30px"><span>岛の茶</span> 👍（2） 💬（2）<div>既然在InnoDB的事务隔离级别可重复读情况，同一个事务中的每一次快照查都会复用第一次快照查的ReadVIew，那么应该看不到其他事务已提交的内容呀，怎么还会出现幻读问题呢？</div>2020-07-04</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/f9/ec/9587eb26.jpg" width="30px"><span>陈逸新</span> 👍（2） 💬（6）<div>RC下MVVC的一个疑惑点。

假设两个事务先后开始，事务A（事务ID100）、事务B（事务ID101）。
事务B更新了一条记录，然后提交，此时该记录的trx_id=101。
接着事务A对该记录进行查询，生成视图，活跃的事务列表为 [100]，而101&gt;100，按照可见规则，理应不访问。
按照MVVC的规则，得出的结论和RC应有的结论矛盾。

这里的矛盾，数据库具体是如何处理的？</div>2020-05-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/f1/c6/6f39a982.jpg" width="30px"><span>Yuhui</span> 👍（2） 💬（2）<div>请教老师以下几个问题：
1. MVCC机制在各个数据库中默认是打开的还是关闭的？
2. 是否可以控制MVCC机制的打开和关闭？
3. 如何查看数据记录的隐藏列？
谢谢！</div>2019-09-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/e1/1a/20977779.jpg" width="30px"><span>峻铭</span> 👍（2） 💬（1）<div>测试结果发现比2.08矮的插入是也会阻塞</div>2019-09-26</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTJETibDh9wrP19gj9VdlLRmppuG1FibI7nyUGldEXCnoqKibKIB18UMxyEHBkZNlf5vibLNeofiaN5U6Hw/132" width="30px"><span>steve</span> 👍（1） 💬（1）<div>争哥求解答，我看这个源码：
http:&#47;&#47;www.iskm.org&#47;mysql56&#47;read0read_8cc_source.html
view-&gt;low_limit_no = trx_sys-&gt;max_trx_id;，
貌似low_limit_no应该是当前系统最大的trx_id才对啊，如果是活跃id列表的最大值貌似不太合理。</div>2020-04-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/a5/2b/e876e7d4.jpg" width="30px"><span>L荀</span> 👍（1） 💬（0）<div>不理解的请教下作者大神：1.可重复读级别下，新加入的行，版本号高于当前事物版本号，不用next-key锁，应该也不会出现幻读，这个怎么理解啊。2.例子中为什么加了for update 读锁呀，不是应该不用锁的么</div>2019-09-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/40/5e/b8fada94.jpg" width="30px"><span>Ryoma</span> 👍（1） 💬（0）<div>如果有的同学看了前面的，没有看到这一章 MVCC。是不是就会产生误解，比如 MySQL Innodb 在可重复读隔离级别下，会发生幻读现象？这类观点，在之前说的时候，是不是需要提前说一下？</div>2019-09-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/67/f4/9a1feb59.jpg" width="30px"><span>钱</span> 👍（0） 💬（0）<div>深水区了，每次学习都认为懂了，时间一长又有些模糊了，需要反复加深印象。</div>2024-08-25</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1d/d6/90/2b949521.jpg" width="30px"><span>tyro</span> 👍（0） 💬（0）<div>还得是我小林哥，清晰明了😏。https:&#47;&#47;zhuanlan.zhihu.com&#47;p&#47;564735312【MySQL 可重复读隔离级别，彻底解决幻读了吗？】</div>2023-03-12</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTLsLBibGjP4JZKxnGLibfkGqCMjSxgkkrugj9Cn5v3pm2icb6jbA2PibeZhSlSuFQwv5aVmpO6e7Pq1iag/132" width="30px"><span>平安喜乐</span> 👍（0） 💬（0）<div>在可重复读的隔离级别下，事务A读取某些数据，会使用间隙锁和Next-Key 锁吗？如果会的话，此时就可以防止幻读的情况出现吗？总觉得这里有点怪。
在之前的理解中，好像只有串行化可以防止幻读</div>2023-02-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1f/40/65/49b923aa.jpg" width="30px"><span>@mj 🍭</span> 👍（0） 💬（0）<div>为什么我height加了索引，insert的时候还是会阻塞的</div>2023-01-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/93/d4/dd2ee398.jpg" width="30px"><span>刘凯</span> 👍（0） 💬（0）<div>更像是CAS+自旋吧。判断版本是否为最新，如果不是就一直自旋等待符合条件返回值</div>2023-01-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1b/b8/21/f692bdb0.jpg" width="30px"><span>路在哪</span> 👍（0） 💬（0）<div>好难，看不明白</div>2022-05-04</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/96/e3/dd40ec58.jpg" width="30px"><span>火车日记</span> 👍（0） 💬（0）<div>最后rc级别的快照读其实可以解决幻读问题，当前读才不可以对吗？</div>2022-03-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/2a/f7/9c/69c5c5dc.jpg" width="30px"><span>越锋利</span> 👍（0） 💬（0）<div>所以 InnoDB 在可重复读这个级别既可以避免幻读了？</div>2021-11-04</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/27/b5/a5/1c62fe9c.jpg" width="30px"><span>爱吾尚</span> 👍（0） 💬（0）<div>你好，想问下MVCC实现过程的第四步和第五步我的理解对不对，就是遍历undo log列表将版本号进行比对，如果可见则返回结果，如果不可见则沿着回滚指针继续寻找判断</div>2021-08-13</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/Q1s3tUoYFJfNq06tg7Asib10yensClWluVxTYZ0KnfXA6WyVSCV4ibO8VAfziaWxojMHFcf1zKQ5iaDhHvtvDSddpQ/132" width="30px"><span>文野</span> 👍（0） 💬（0）<div>drop table if exists `test`;
CREATE TABLE `test` (
   `id` bigint NOT NULL AUTO_INCREMENT COMMENT &#39;编号&#39;,
   `aa` bigint unsigned NOT NULL COMMENT &#39;aa&#39;,
   PRIMARY KEY (`id`),
   KEY `idx_aa` (`aa`),
) ENGINE=InnoDB COMMENT=&#39;测试&#39;;

tx1：
update test set aa = 15 where id = 100;
select * from test where aa = 15 limit 10; 

tx1的第二条查询的时候是怎么用索引查的呢</div>2021-06-21</li><br/>
</ul>