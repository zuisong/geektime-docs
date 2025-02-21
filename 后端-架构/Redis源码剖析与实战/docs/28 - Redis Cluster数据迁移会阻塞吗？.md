你好，我是蒋德钧。

上节课，我给你介绍了Redis Cluster节点处理命令的过程。现在你知道，在这个过程中，节点会调用**getNodeByQuery函数**检查访问的key所属的节点，如果收到命令的节点并不是key所属的节点，那么当前节点就会生成CLUSTER\_REDIR\_MOVED或者CLUSTER\_REDIR\_ASK的报错信息，并给客户端返回MOVED或ASK命令。

其实，这两个报错信息就对应了Redis Cluster的数据迁移。数据迁移是分布式存储集群经常会遇到的一个问题，当集群节点承担的负载压力不均衡时，或者有新节点加入或是已有节点下线时，那么，数据就需要在不同的节点间进行迁移。所以，**如何设计和实现数据迁移也是在集群开发过程中，我们需要考虑的地方。**

那么今天这节课，我就来介绍下Redis Cluster是如何实现数据迁移的。从源码层面掌握这部分内容，可以帮助你了解数据迁移对集群节点正常处理命令的影响，这样你就可以选择合适时机进行迁移。而且，掌握Redis的数据迁移实现，也能为你自己开发集群提供一个不错的参考示例。

好了，接下来，我们就先来看下和数据迁移相关的主要数据结构。这些数据结构比较重要，它们记录了数据迁移的状态信息。
<div><strong>精选留言（5）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/0f/90/8a/288f9f94.jpg" width="30px"><span>Kaito</span> 👍（4） 💬（0）<div>1、Redis Cluster 因为是多个实例共同组成的集群，所以当集群中有节点下线、新节点加入、数据不均衡时，需要做数据迁移，把某些实例中的数据，迁移到其它实例上

2、数据迁移分为 5 个阶段

- 标记迁入、迁出节点
- 获取待迁出的 keys
- 源节点实际迁移数据
- 目的节点处理迁移数据
- 标记迁移结果

3、获取待迁出的 keys 会用 CLUSTER GETKEYSINSLOT 命令，可返回指定 slot 下的 keys

4、从源节点迁出数据，会调用 MIGRATE 命令，该命令可指定一批 key，迁移到目标 Redis 实例。迁移时，源节点会把 key-value 序列化，然后传输给目标节点

5、目标节点收到源节点发来的数据后，会执行 RESTORE 命令逻辑，校验序列化的数据格式是否正确，正确则解析数据，把数据添加到实例中

6、标记迁移结果会向源节点和目标节点执行 CLUSTER SETSLOT 命令，目的是设置迁移 key 的最终归属 slot

课后题：在维护 Redis Cluster 集群状态的数据结构 clusterState 中，有一个字典树 slots_to_keys。当在数据库中插入 key 时它会被更新，db.c 更新 slots_to_keys 字典树的相关函数调用有哪些？

全局搜索 slots_to_keys 关键词，可以看到 db.c 中的相关函数有：

- slotToKeyUpdateKey，分别被 slotToKeyAdd 和 slotToKeyDel 调用，看名字是向 slots_to_keys 添加 &#47; 删除 key
- slotToKeyFlush，清空 slots_to_keys 中的数据
- getKeysInSlot：获取指定 slot 下的 keys
- delKeysInSlot：删除指定 slot 下的 keys</div>2021-10-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/25/7f/473d5a77.jpg" width="30px"><span>曾轼麟</span> 👍（4） 💬（0）<div>回答老师的问题：
clusterState 中的 slots_to_keys 在查阅git历史提交记录中发现，之前是使用跳跃表（zskiplist）在后来才替换成了-字典树，其最主要的目的是为了方便通过 slot 快速查找到solt下的keys，getKeysInSlot 函数正是使用这种方式来获取待迁出的 keys。

        【获取key调用路径】:clusterCommand -&gt; getKeysInSlot -&gt; raxStart(迭代器)
        【插入key调用路径】:dbAdd -&gt; slotToKeyAdd -&gt; slotToKeyUpdateKey -&gt; raxInsert
        【删除key调用路径】:dbAsyncDelete&#47;dbSyncDelete -&gt; slotToKeyDel -&gt; slotToKeyUpdateKey -&gt; raxRemove

总结：
本篇文章老师介绍了Redis Cluster 数据迁移过程的实现思路，其中数据迁移整体可以归纳为5个步骤：

        1、标记迁入、迁出节点；
        2、获取待迁出的 keys；
        3、源节点实际迁移数据；
        4、目的节点处理迁移数据；
        5、标记迁移结果；

其中迁移涉及的函数有clusterCommand，migrateCommand，restoreCommand，其中老师有个点提醒的很好，syncWrite 和 syncReadLine是进行同步调用的，需要对key数量进行控制。

此外Redis为了保证传输效率和传输的安全性，分别使用了自定义的序列化方案（这里复用了DUMP命令，文件序列化的方案） 和 CRC64验证其中结构大致如下所示：
----------------+---------------------+---------------+
... RDB payload | 2 bytes RDB version | 8 bytes CRC64 |
----------------+---------------------+---------------+

理论上来说RESP协议也能实现类似的效果，但是在传输效率上来说自定义的序列化方案效率更高。</div>2021-10-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/25/44/aa/2439eff2.jpg" width="30px"><span>秦静</span> 👍（1） 💬（0）<div>还是没回答问题呀，，，阻塞还是不阻塞</div>2022-12-02</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/28/43/5062a59b.jpg" width="30px"><span>shan</span> 👍（1） 💬（0）<div>Redis Cluster数据迁移总结
1.在源节点和目标节点分别标记slot迁出和迁入信息
（1）在需要迁入的目标节点使用IMORITING命令标记要将SLOT从哪个节点迁入
（2）在源节点也就是slot所在节点使用MIGRATING命令标记数据迁出到哪个节点
2.在源节点使用CLUSTER GETKEYSINSLOT命令获取待迁出的KEY
3.在源节点执行MIGRATE命令进行数据迁移
4.在源节点和目标节点使用CLUSTER SETSLOT标记slot最终迁移的节点

总结了一篇集群故障迁移的源码分析
https:&#47;&#47;www.cnblogs.com&#47;shanml&#47;p&#47;16290642.html</div>2022-06-15</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/22/bd/9b/366bb87b.jpg" width="30px"><span>飞龙</span> 👍（0） 💬（0）<div>cluster这个章节还是很吃力的</div>2022-10-26</li><br/>
</ul>