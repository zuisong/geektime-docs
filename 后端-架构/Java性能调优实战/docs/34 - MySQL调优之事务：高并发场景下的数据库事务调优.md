你好，我是刘超。

数据库事务是数据库系统执行过程中的一个逻辑处理单元，保证一个数据库操作要么成功，要么失败。谈到他，就不得不提ACID属性了。数据库事务具有以下四个基本属性：原子性（Atomicity）、一致性（Consistent）、隔离性（Isolation）以及持久性（Durable）。正是这些特性，才保证了数据库事务的安全性。而在MySQL中，鉴于MyISAM存储引擎不支持事务，所以接下来的内容都是在InnoDB存储引擎的基础上进行讲解的。

我们知道，在Java并发编程中，可以多线程并发执行程序，然而并发虽然提高了程序的执行效率，却给程序带来了线程安全问题。事务跟多线程一样，为了提高数据库处理事务的吞吐量，数据库同样支持并发事务，而在并发运行中，同样也存在着安全性问题，例如，修改数据丢失，读取数据不一致等。

在数据库事务中，事务的隔离是解决并发事务问题的关键， 今天我们就重点了解下事务隔离的实现原理，以及如何优化事务隔离带来的性能问题。

## 并发事务带来的问题

我们可以通过以下几个例子来了解下并发事务带来的几个问题：

1.数据丢失

![](https://static001.geekbang.org/resource/image/db/7d/db7d28a1f27d46cf534064ab4e74f47d.jpg?wh=2530%2A384)

2.脏读

![](https://static001.geekbang.org/resource/image/d7/4c/d717c7e782620d2e46beb070dbc8154c.jpg?wh=2506%2A384)

3.不可重复读

![](https://static001.geekbang.org/resource/image/61/9a/6173739ee9a5d7e26c8b00f2ed8d9e9a.jpg?wh=2560%2A372)

4.幻读

![](https://static001.geekbang.org/resource/image/28/b6/280826363e1d5a3e64529dfd3443e5b6.jpg?wh=2598%2A374)

## 事务隔离解决并发问题

以上 4 个并发事务带来的问题，其中，数据丢失可以基于数据库中的悲观锁来避免发生，即在查询时通过在事务中使用 select xx for update 语句来实现一个排他锁，保证在该事务结束之前其他事务无法更新该数据。
<div><strong>精选留言（30）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/0f/4d/fd/0aa0e39f.jpg" width="30px"><span>许童童</span> 👍（78） 💬（3）<div>binlog + redo log 两阶段提交保证持久性
事务的回滚机制 保证原子性 要么全部提交成功 要么回滚
undo log + MVCC 保证一致性 事务开始和结束的过程不会其它事务看到 为了并发可以适当破坏一致性</div>2019-08-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/7b/57/a9b04544.jpg" width="30px"><span>QQ怪</span> 👍（25） 💬（1）<div>默认transaction用的是数据库默认的隔离级别不是一定是RR，只是用MySQL默认是RR</div>2019-08-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/07/cf/b0d6fe74.jpg" width="30px"><span>L.</span> 👍（14） 💬（7）<div>老师，对于可重复读(Repeatable Read)的事务级别可以避免不可重复读的现象有个疑问：
对于事务A来说，它在获得共享锁期间修改了数据，比如把A改为B，修改完成后释放共享锁。在A获得共享锁期间，事务B看到的数据是A，释放共享锁后，事务B才获得排他锁，然后看到的数据是B。两次的数据不一样啊，还是没有避免不可重复读。。。。不知道我理解的哪里不对，望老师指点。。。🙏</div>2019-08-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/63/cb/7c004188.jpg" width="30px"><span>和你一起搬砖的胡大爷</span> 👍（7） 💬（3）<div>老师能否重点讲一下record lock、gap lock 以及 next-key lock？</div>2019-08-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/49/ef/02401473.jpg" width="30px"><span>月迷津渡</span> 👍（6） 💬（4）<div>一个问题困扰我挺久希望解答，spring的事务隔离和db的事务隔离机制有什么关系，这么问吧比如db里默认是RR的隔离级别（默认也肯定会有一个隔离级别），我spring的事务里就不用配置隔离级别了？如果spring的事务里的代码并没有db操作我也能设置spring的事务隔离级别？
其次就是设置db级别的事务隔离的话，那如果业务不一样的话是不是理论上可以把库拆开来？因为肯定有一些库用到了不需要的更高隔离级别影响性能。</div>2019-10-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/3a/5d/c5dc789a.jpg" width="30px"><span>珠穆写码</span> 👍（5） 💬（2）<div>老师，您这些数据库的相关知识是从官网还是某些书籍中获取的？我的数据库进阶的知识比较浅，看官网觉得有点费劲，不知道从哪入手去看去学</div>2019-08-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/88/6e/3bd860d3.jpg" width="30px"><span>.</span> 👍（4） 💬（1）<div>1. 结合业务场景，使用低级别事务隔离
2. 避免行锁升级表锁
3. 控制事务的大小，减少锁定的资源量和锁定时间长度</div>2020-03-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/f5/57/ce10fb1b.jpg" width="30px"><span>天天向上</span> 👍（3） 💬（3）<div>老是有个问题，希望得到解答：InnoDB引擎下，select语句是不加锁的啊，那在文章中 避免行锁升级表锁一节中，讲到 如果不通过索引条件检索数据，行锁将会升级到表锁，应该不成立啊？</div>2020-01-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/07/5a/abb7bfe3.jpg" width="30px"><span>OneThin</span> 👍（1） 💬（1）<div>最后一个例子，有个疑问，因为要判断库存，这里是不是应该用可重复读的隔离级别，所以读取库存的时候已经加锁了，直到事务结束，那么锁对啊时间应该差不多才对啊</div>2020-03-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/e7/70/2a382ccf.jpg" width="30px"><span>飞天小猪</span> 👍（1） 💬（1）<div>最后减库存例子中，如果要避免长时间持有锁，不应该先减库存，选择执行顺序2吗？</div>2019-12-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/a0/cb/aab3b3e7.jpg" width="30px"><span>张三丰</span> 👍（1） 💬（2）<div>未提交读（Read Uncommitted）：在事务 A 读取数据时，事务 B 读取和修改数据加了共享锁。这种隔离级别，会导致脏读、不可重复读以及幻读。

这句话怎么理解呢？事务B读取和修改数据加了共享锁？修改数据不是只能加排它锁么？</div>2019-10-04</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/17/8b/4b/15ab499a.jpg" width="30px"><span>风轻扬</span> 👍（1） 💬（2）<div>老师，对数据库锁不是很熟悉。以下结构是正确的吗？
数据库锁=乐观锁 + 悲观锁[共享锁、排它锁[行锁、表锁]]
这些是数据库所有的锁吗?
</div>2019-09-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/db/a4/191be6ad.jpg" width="30px"><span>加载中……</span> 👍（1） 💬（7）<div>老师好，有个问题请教下。文章中说：“可重复读（Repeatable Read）可以避免脏读、不可重复读，但依然存在幻读的问题。”
我之前了解的是，SQL标准不要求RR解决幻读，但InnoDB的 RR下 是不会产生幻读的。
而且自己实验也是InnoDB在RR下没有幻读的现象。操作如下：
sessionA: begin;
sessionA: select * from t where id&gt;1;(2条记录)
sessionB: insert into t(id,a) values(5,5);
sessionA: select * from t where id&gt;1;(还是2条看不到5,5。没有产生幻读)</div>2019-08-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/1e/9e/abb7bfe3.jpg" width="30px"><span>小布丁</span> 👍（1） 💬（2）<div>老师数据库的事务和Spring的事务是一回事吗？写业务代码的时候，两种不同的事务分别起什么作用呢？或者说控制范围有何不同呢？</div>2019-08-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/79/4b/740f91ca.jpg" width="30px"><span>-W.LI-</span> 👍（1） 💬（1）<div>老师好!之前听说不少互联网公司，把mysql数据库默认隔离级别设置为读已提交(不手动设默认是RR)，来提高吞吐量。这样就需要开发人员根据业务选择合适的隔离级别是么?
接着老师减库存的例子:
新建订单,减库存操作可以在，读已提交隔离级别下执行么?
我觉得新建订单和减库存只要保证原子行就好了。减库存是读当前操作，还是需要在RR下。</div>2019-08-08</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/aobibE2ABHn3njdaHBY23hcZcIs71aRahryuUDcLghQqTjmwghEIgKYelBERlNK881MP0oRpWGnrQdscD85dZ9g/132" width="30px"><span>云封</span> 👍（0） 💬（1）<div>老师，上面不是说普通的select不加锁嘛，为啥后面又说，在select下，除了基于唯一索引外，其他的索引查询都会获取gap lock以及next-key lock</div>2020-03-28</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/6LaITPQ4Lk5fZn8ib1tfsPW8vI9icTuSwAddiajVfibPDiaDvMU2br6ZT7K0LWCKibSQuicT7sIEVmY4K7ibXY0T7UQEiag/132" width="30px"><span>尔东橙</span> 👍（0） 💬（1）<div>老师，共享锁排他锁和行锁的三种实现算法是什么关系？</div>2020-02-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/f5/57/ce10fb1b.jpg" width="30px"><span>天天向上</span> 👍（0） 💬（1）<div>在结合业务场景，使用低级别事务隔离中，所举的用户、积分的例子中，使用不同的隔离级别，但是隔离级别不能单独给表设置吧。</div>2020-01-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/12/4e/ff0702fc.jpg" width="30px"><span>火锅小王子</span> 👍（0） 💬（2）<div>您好 对于可重复读的描述：事务 A 在读取数据时，事务 B 只能读取数据，不能修改。当事务 A 读取到数据后，事务 B 才能修改。 经试验  事务A在读取但是事务并未结束的时候  事务B是可以修改数据并提交的  不知道是我哪里理解有问题？</div>2019-12-20</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/icHicAP9M4M4DIjAvlj5FDdFxIeA0pR3J15QdvVjXQXbznwunDN8OvrYqnsFchtBTNrZCCfGTE2RpPzIxjkvFAKg/132" width="30px"><span>奋斗的小白鼠</span> 👍（0） 💬（3）<div>老师，您说MVCC 对普通的 Select 不加锁，那RC和RR级别不一样了吗？这两个不就是select加锁不一样吗？还有既然RC select也是快照读，那是不是也解决了不可重复读问题？
望解答，研究了一晚上Mvcc搞晕了</div>2019-12-04</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/19/78/99/6060eb2d.jpg" width="30px"><span>平凡之路</span> 👍（0） 💬（3）<div>老师，您好，我在可重复读里面，事务A没有结束，不做修改操作，但是事务B也可以修改数据</div>2019-12-03</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/49/ef/02401473.jpg" width="30px"><span>月迷津渡</span> 👍（0） 💬（3）<div>有个问题请教下，我看到说 redolog 为了提升持久化的IO效率而产生，把每次事务写数据文件改成写redoLog然后再批量写redoLog到数据文件。我就有个问题了，redoLog和数据文件不都是磁盘读么？并且写redolog也需要在事务中同步写，因为异步写不能保证redolog必定写成功。。。求教</div>2019-10-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/66/df/501ba989.jpg" width="30px"><span>面试官问</span> 👍（0） 💬（1）<div>Serializable 翻译为 可串行化 会更合理一些。</div>2019-10-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/67/f4/9a1feb59.jpg" width="30px"><span>钱</span> 👍（0） 💬（1）<div>请问老师数据库的事务本质是不是都是利用单库的事务机制实现的?分布式数据库事务，只是将控制事务提交或回滚的动作往上层提升啦?</div>2019-09-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/4e/2a/e606529b.jpg" width="30px"><span>小学生🍭</span> 👍（0） 💬（1）<div>老师update语句是行锁，那insert语句是什么锁呢</div>2019-09-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/b3/c5/7fc124e2.jpg" width="30px"><span>Liam</span> 👍（0） 💬（1）<div>老师好，查询未加索引时行锁升级为表锁这里有个疑问，mvvc机制下select不是不加锁吗？除非是in share mode或for update</div>2019-08-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/5e/86/40877404.jpg" width="30px"><span>星星滴蓝天</span> 👍（0） 💬（1）<div>老师能否多讲点innodb锁。最近我们老是出现锁等待的情况，老师可否给一些优化的思路</div>2019-08-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/4f/7f/5dc11380.jpg" width="30px"><span>苏志辉</span> 👍（0） 💬（1）<div>RR是基于MVVC的，而后者对于select不加锁，那么如果事务a有两次查询，事务b在a的两次查询之间做了修改，要保证可重复读，a两次读取的都是b改之前的快照吗？</div>2019-08-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/38/f1/996a070d.jpg" width="30px"><span>LW</span> 👍（0） 💬（1）<div>思考题：通过redo log和undo log实现</div>2019-08-08</li><br/><li><img src="https://wx.qlogo.cn/mmopen/vi_32/DYAIOgq83eotSSnZic41tGkbflx0ogIg3ia6g2muFY1hCgosL2t3icZm7I8Ax1hcv1jNgr6vrZ53dpBuGhaoc6DKg/132" width="30px"><span>张学磊</span> 👍（0） 💬（1）<div>MySQL通过事务实战原子性，一个事务内的DML语句要么全部成功要么全部失败。通过redo log和undo log实现持久性和一致性，当执行DML语句时会将操作记录到redo log中并记录与之相反的操作到undo log中，事务一旦提交，就将该redolog中的操作，持久化到磁盘上，事务回滚，则执行undo log中记录的操作，恢复到执行前的状态。</div>2019-08-08</li><br/>
</ul>