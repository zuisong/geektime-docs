你好，我是韩健。

相信很多同学都知道MySQL支持单机事务，那么在分布式系统中，涉及多个节点，MySQL又是怎么实现分布式事务的呢？

这个和我最近遇到的问题很类似，我现在负责的一个业务系统，需要接收来自外部的指令，然后访问多个内部其他系统来执行指令，但执行完指令后，我需要同时更新多个内部MySQL数据库中的值（比如MySQL数据库A、B、C）。

但又因为业务敏感，系统必须处于一个一致性状态（也就是说，MySQL数据库A、B、C中的值要么同时更新成功，要么全部不更新）。不然的话，会出现有的系统显示指令执行成功了，有的系统显示指令尚未被执行，导致多部门对指令执行结果理解混乱。

那么我当时是如何实现多个MySQL数据库更新的一致性呢？答案就是采用MySQL XA。

在我看来，MySQL通过支持XA规范的二阶段提交协议，不仅实现了多个MySQL数据库操作的事务，还能实现MySQL、Oracle、SQL Server等支持XA规范的数据库操作的事务。

对你来说，理解MySQL XA，不仅能理解数据层分布式事务的原理，还能在实际系统中更加深刻的理解二阶段提交协议，这样一来，当你在实际工作中，遇到多个MySQL数据库的事务需求时，就知道如何通过MySQL XA来处理了。
<div><strong>精选留言（15）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/17/14/c2/46ebe3a0.jpg" width="30px"><span>侧耳倾听</span> 👍（36） 💬（1）<div>既然是多数据库场景，首先，需要搞清楚的是为什么引入多数据库？如果是基于性能的考虑，并发量大，需要考虑的是读多写少，还是写多读少？如果是读多写少，那么可以采用一主多从，主库负责写，以及引入缓存机制来提高数据的实时性。如果是写多读少，问题有些复杂，如果读的实时要求不高，可以考虑采用队列的形式，后台线程负责写入数据库。如果是基于业务的拆分，要搞明白是不是需要拆分？是在现有硬件基础上解决不了并发的写入，还是仅仅是因为模仿。如果是后者，不妨先考虑将业务表的表空间分不到不同的磁盘，避免单磁盘的写入，可以提高一定的数据写入效率。在这个过程中还需要考虑数据库各种缓存的大小设定，比如chang buffer，redolog文件。争取做到单点优化做到无突破，再考虑横向或者纵向的扩展。一旦牵扯进分布式架构，就不再是一个数量级的问题展现。</div>2020-06-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/9d/ec/235b74c0.jpg" width="30px"><span>ppyh</span> 👍（22） 💬（3）<div>这个和我最近遇到的问题很类似，我现在负责的一个业务系统，需要接收来自外部的指令，然后访问多个内部其他系统来执行指令，但执行完指令后，我需要同时更新多个内部 MySQL 数据库中的值（比如 MySQL 数据库 A、B、C）。
不过，虽然 MySQL XA 能实现数据层的分布式事务，但在我现在负责的这套业务系统中，还面临这样的问题：那就是在接收到外部的指令后，我需要访问多个内部系统，执行指令约定的操作，而且，我必须保证指令执行的原子性，也就是说，要么全部成功，要么全部失败，那么我应该怎么做呢？答案是 TCC，这也是我在下一讲想和你聊一聊的。



这两句话有区别吗，怎么第一句话就可以用mysql xa，第二句话就得用tcc啊</div>2020-06-26</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTKhuGLVRYZibOTfMumk53Wn8Q0Rkg0o6DzTicbibCq42lWQoZ8lFeQvicaXuZa7dYsr9URMrtpXMVDDww/132" width="30px"><span>hello</span> 👍（10） 💬（1）<div>课程都完结好长一段时间了，老师还在时不时加餐，给老师点赞。</div>2020-06-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/0f/70/f59db672.jpg" width="30px"><span>槑·先生</span> 👍（4） 💬（2）<div>老师，有个问题不太理解。事务不就包含原子性吗？分布式事务不是也应该包含指令的原子性吗，为什么会存在最后那个指令原子性的问题。</div>2020-06-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/18/f9/31/b75cc6d5.jpg" width="30px"><span>ξ！</span> 👍（2） 💬（4）<div>老师，raft是不是在保证有状态节点间的内存中数据一致性，而XA在保证数据持久化后的一致性</div>2020-06-23</li><br/><li><img src="" width="30px"><span>Geek_9d0e04</span> 👍（1） 💬（1）<div>请假老师，操作两个数据库，我自己在代码中也能实现两阶段提交呀，两个数据库连接先各自执行自己的SQL，作为第一阶段；都没问题再提交事务，否则回滚，作为第二阶段。我觉得事务管理器的作用，也就是上面内容吧，那为何有需要独立一个事务管理器，增加单点呢？</div>2020-07-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/19/d9/ff/b23018a6.jpg" width="30px"><span>Heaven</span> 👍（0） 💬（1）<div>我的思路是,首先只在主节点上执行事务,然后降低和跟随者的延迟,来保证,在主节点上执行成功了,必然会可以在从节点上执行成功,这是否是一种解决方案呢?
可以利用GTID来辅助查询工作</div>2020-08-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1d/12/13/e103a6e3.jpg" width="30px"><span>扩散性百万咸面包</span> 👍（0） 💬（1）<div>按照文章中的表述，如果要实现分布式事务的话，需要对应的数据库实现XA规范接口。而且客户端会聚集一定的复杂性：因为我看图中客户端需要把一个事务里的不同语句发给不同的MySQL，那要怎么样才能知道自己的语句应该放在哪个SQL上执行呢？</div>2020-08-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/b9/3b/7224f3b8.jpg" width="30px"><span>janey</span> 👍（3） 💬（0）<div>请问老师，mysql xa在xa prepare后资源锁定，锁定的主要是什么资源呢？这个资源锁定的影响面主要是哪些？</div>2022-03-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/18/7b/03/03583011.jpg" width="30px"><span>天天有吃的</span> 👍（0） 💬（0）<div>xa的实现就是2pc、3pc吧</div>2023-08-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/df/70/52f2ab90.jpg" width="30px"><span>Andy Huang</span> 👍（0） 💬（0）<div>有谁知道postgresql的分布式版本有哪些? 各是用了什么协议? 我正在做选型</div>2022-04-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/ae/8b/43ce01ca.jpg" width="30px"><span>ezekiel</span> 👍（0） 💬（1）<div>既然我提到了我通过 MySQL XA 解决了数据库操作的一致性问题，而 MySQL XA 性能不高，适用于对并发性能要求不高的场景中。那么你不妨想想，在 MySQL XA 不能满足并发需求时，如何重新设计底层数据系统，来避免采用分布式事务呢？为什么呢？
==============================================================
思考题的答案是什么呢？</div>2021-10-10</li><br/><li><img src="" width="30px"><span>Geek_a21638</span> 👍（0） 💬（0）<div>&quot;事务管理器只是标记事务，并不执行事务，最终是由（应用程序）通知资源管理器来执行事务操作的&quot;, 我的理解应该是 “最终是由（事务管理器TM）通知资源管理器来执行事务操作的”？？</div>2021-10-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/3e/e7/261711a5.jpg" width="30px"><span>blentle</span> 👍（0） 💬（0）<div>韩老师, 如果有一个事物分支在 commit阶段由于外部影响，commit了一个不存在的 Xid. 抛出了异常.这时其他的分支已经commit成功了. 最终能否保证所有的事物分支回滚呢？</div>2021-02-05</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/8b/83/d2afc837.jpg" width="30px"><span>路人</span> 👍（0） 💬（2）<div>commit阶段如果只有部分成功，需要程序考虑补偿机制</div>2020-09-03</li><br/>
</ul>