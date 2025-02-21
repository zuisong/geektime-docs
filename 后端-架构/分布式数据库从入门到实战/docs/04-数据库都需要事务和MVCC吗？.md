你好，我是彭旭。

想要保证数据操作的一致性、隔离性和持久性，提高数据库系统的并发性和可靠性，事务与MVCC（Multi-Version Concurrency Control，多版本并发控制）是一个绕不开的话题。

MVCC是一种数据库事务并发控制的方法，能够在数据库系统中高效地处理并发事务。在保证事务的隔离性和一致性的同时，也能提升数据库性能。

不同类型的数据库对事务与MVCC的需求不尽相同。在深入了解不同的需求之前，我们要先来看看不同事务隔离级别下可能发生的一些数据问题。

## 不同事务隔离级别带来的问题

现在有一个银行账户表u\_account，这个表有id、account\_id、balance等多个字段。基于这个表在不同的事务隔离级别与并发的情况下，我们看看会出现一些什么样的问题。

第1个问题是**脏读。**

t1时刻：小明的账户有余额200。事务B开启，向小明的账户转入1000，事务还未提交。

t2时刻：小明基于事务A查询账户，发现现在有1200余额。

t3时刻：事务B发现转错账户了，事务回滚。小明账户余额仍然是200。

t4时刻：小明以为余额有1200，消费300，结果要么导致最后余额账户-100，要么交易失败。

![图片](https://static001.geekbang.org/resource/image/8e/83/8eb218d4cdbcce078279df87db207183.png?wh=3712x2040)

也就是说，脏读导致业务使用的可能是一个中间态的数据，以至于业务的数据出现问题。显然，如果我们的业务系统需要保障数据的准确与一致性，那就应该避免脏读。
<div><strong>精选留言（4）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/1a/2e/c5/231114ed.jpg" width="30px"><span>Hadesu</span> 👍（3） 💬（1）<div>如果老旧的undolog被删除了，会影响mvcc的正确性吗？</div>2024-06-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/6e/2c/e2f3cfc0.jpg" width="30px"><span>注意力$</span> 👍（0） 💬（0）<div>请问MySQL的undo保留周期由那个参数决定呢</div>2025-02-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/45/18/3d05adb4.jpg" width="30px"><span>蓝山</span> 👍（0） 💬（0）<div>Oracle中ora15333应该属于这种情况</div>2024-09-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/46/4d/161f3779.jpg" width="30px"><span>ls</span> 👍（0） 💬（0）<div>感觉各种数据库 oracle ，mysql ，ch  事务一致性实现方式大的方向都差不多。</div>2024-08-09</li><br/>
</ul>