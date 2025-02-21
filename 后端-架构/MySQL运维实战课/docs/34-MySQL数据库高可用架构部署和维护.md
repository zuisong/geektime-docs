你好，我是俊达。

从这一讲开始，我们来聊一聊怎么构建和运维MySQL高可用环境。高可用的重要性和必要性，这里就不多说了。实现高可用，需要在IT系统的整个链路上消除单点。MySQL要实现高可用，最基本的就是数据复制技术。

## MySQL数据复制技术简介

数据复制是MySQL一直以来最受欢迎的功能之一。应用程序访问主库，对主库的修改操作都记录到Binlog中。备库从主库同步Binlog、执行Binlog，这样，备库和主库始终保持一致。

![图片](https://static001.geekbang.org/resource/image/35/0b/35201d05c58c91f74a2b704f35a1b80b.jpg?wh=1195x765)

基于数据复制，可以实现多种高可用架构。

- 高可用

应用程序只访问主库，备库作为主库的热备。当主库发生故障，或者主库需要停机维护时，将业务流量切到备库上，减少停机时间。在备库上进行数据库备份等运维操作。

![图片](https://static001.geekbang.org/resource/image/cc/4b/cc4fdaed31d6129394d901e5da68b54b.png?wh=818x254)

- 读写分离

将应用的一部分读流量分发（select）到备库上执行。MySQL支持一主多备的数据复制架构，在读多写少的场景下，可以增加多个备库，来提高数据库集群的业务支撑能力。

![图片](https://static001.geekbang.org/resource/image/53/0a/536d21d821b25ed860e790b7b5e8300a.jpg?wh=1228x558)

还可以使用备库来支持一些分析类的大查询、数据抽取等资源消耗较高的操作，避免影响主库业务。

- 报表库

![图片](https://static001.geekbang.org/resource/image/9a/71/9a298065bfea34a5605ayy845fdbd871.jpg?wh=1140x564)

### MySQL数据复制的基本原理

我们把整个数据库看作是一个状态。每个事务将数据库转换到一个新的状态。虽然主库上事务可以并发执行，但是事务具备原子性和隔离性，因此可以设想主库的事务按顺序执行。如果备库和主库拥有相同的初始状态，并且按相同的顺序执行主库上执行过的事件，那么备库和主库就应该是完全一致的。
<div><strong>精选留言（2）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/2a/39/93/f0247cf8.jpg" width="30px"><span>一本书</span> 👍（1） 💬（1）<div>“如果主库使用了 GTID，生产的备份文件中已经记录了备份时，主库的 GTID_executed 变量。这可以从文件中直接看到。”，老师，我看下方的代码中是SET @@GLOBAL.GTID_PURGED=...，难道 GTID_executed 与GTID_PURGED变量之间是有什么关联吗？</div>2024-11-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/8d/4d/992070e8.jpg" width="30px"><span>叶明</span> 👍（0） 💬（1）<div>当 sync_binlog != 1 时，source 上的 sync binlog 操作可能并没有使 binlog 落盘，如果没有落盘，那么在 engine commit 前，source 掉电，然后恢复，那么这个事务会被回滚（处于 prepare 状态，但没完整的 binlog），但是 replica 可能已经收到该事务并执行，这个时候就会出现 Slave 比 Master 多的情况。
可参考 http:&#47;&#47;mysql.taobao.org&#47;monthly&#47;2017&#47;04&#47;01&#47;</div>2024-11-08</li><br/>
</ul>