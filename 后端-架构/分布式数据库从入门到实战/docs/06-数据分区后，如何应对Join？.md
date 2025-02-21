你好，我是彭旭。

上一讲，我们介绍了在分布式数据库中合理地分库分表或者分区的方法，还讲了如何裁剪查询时需要扫描的数据，优化查询性能。

但是，分区也会带来一个新的问题。数据表之间通常存在关联关系，一个完整的业务通常需要关联多个表，才能得到最终需要的业务数据。

这节课，我们就来看看数据分区后，分布式数据库是如何处理这种数据关联场景的。

相信这节课，你一定能了解分布式数据库连接的几种方式，以及它们各自的性能表现和适用场景。

## 分布式数据库的几种Join方式

为了更好地理解Join的各种方式，我给你准备了一个例子。

这是一个基于分布式数据库存储的用户行为管理系统。假设系统包含如下两个表，都以分区/分片形式存储。

用户表：以user\_id分区。

```plain
CREATE TABLE t_user
(
    `app_id`      UInt32 COMMENT '应用id',
    `user_id`     UInt32 COMMENT '用户ID',
    `name`        String COMMENT '姓名',
    `email`       String COMMENT '邮箱',
    `avatar`      String COMMENT '头像url',
    `phone`       String COMMENT '手机号',
    `address`     String COMMENT '地址',
    `create_date` DateTime COMMENT '创建时间'
) 
```
<div><strong>精选留言（2）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/31/1e/0a/159b2129.jpg" width="30px"><span>lufofire</span> 👍（5） 💬（1）<div>思考题：
Colocate Join 并不一定优于 Shuffle Join。 因为Colocate Join因为本身也具有局限性。比如上一讲说的关于片健选择，在多租户场景中，考虑到某些租户数据量很大，我们选择的片健一般是租户ID+时间的复合片健，更有利于负载均衡。而对于这种复合片健，相同的租户数据失不可能放在同一个Shard中，使得Colocate Join方式无法开展的， 而这个时候Shuffle Join就会是更好的选择。简单来说，Colocate Join会存在扩展性问题，负载均衡的问题， 它比较适合数据量适中，节点间的数据分布均匀，且查询模式稳定的场景。而对于需要高度扩展性和并行处理的大规模数据集，Shuffle Join 可能是更合适的选择， 当这种场景下使用join查询会消耗大量的I&#47;O， 延迟也会很高， 需要谨慎使用。
</div>2024-06-25</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/46/4d/161f3779.jpg" width="30px"><span>ls</span> 👍（1） 💬（0）<div>join问题还是能少就尽量少，不像关系型数据库 ，有时上来先来7个表关联</div>2024-08-09</li><br/>
</ul>