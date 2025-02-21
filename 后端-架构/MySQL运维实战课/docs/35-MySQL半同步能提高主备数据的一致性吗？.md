你好，我是俊达。

上一讲中，我留了一个问题，就是在默认的情况下，MySQL的数据复制是异步的，当主库意外崩溃后，备库是否有可能比主库多执行一些事务？

回答这个问题，需要对主库事务提交的过程，以及数据复制的细节有更深入的了解。这一讲我们就来看一看事务的提交过程，分析Binlog是什么时候发送给备库的，还有Semi-Sync插件在中间起到的作用。这里我假定只使用了InnoDB存储引擎，开启了GTID，并且使用了ROW格式Binlog，这也是推荐的使用方式。

## MySQL数据复制回顾

下面这张数据复制的架构图，你应该在上一讲中就看到过了。

![图片](https://static001.geekbang.org/resource/image/66/6c/66909ff3d10813e114aff69913085d6c.jpg?wh=1790x812)

我们回顾一下。

1. 用户线程在执行事务的过程中不断产生Binlog事件。Binlog事件的内容和事务中执行的语句相关，同时也受参数binlog\_format影响。产生的Binlog事件会先缓存到Binlog Cache中。每一个用户线程都有各自独立的Binlog Cache。
2. 提交事务时，用户线程将Binlog Cache中的数据写入到Binlog文件。一个事务会产生多个Binlog事件，这些事件在Binlog文件中是连续存放的。一个线程在往Binlog文件中写入数据时，其他线程要等待之前的线程写完数据，才能写入Binlog文件。
3. 用户线程将Binlog事件写入到文件或将Binlog文件同步到磁盘后，通知Dump线程有新的binlog事件产生，通知的具体时机跟参数sync\_binlog的设置有关系。
4. 对每一个备库上的IO线程，主库上都会创建一个Dump线程。Dump线程负责将已提交事务的Binlog事件发送给IO线程。
5. IO线程接收到Binlog事件后，将事件写入RelayLog文件。
6. SQL线程从RelayLog文件中解析出Binlog事件，并进行应用。启用了多线程复制时，SQL线程也称为协调线程。备库上参数replica\_parallel\_workers设置为大于1的值，就能开启多线程复制。参数replica\_parallel\_type用来控制并行复制的方式，建议设置为LOGICAL\_CLOCK。
7. 如果启用了多线程复制，SQL线程会将Binlog事件分发给各个Worker线程。
8. SQL线程或Worker线程执行Binlog事件。
<div><strong>精选留言（2）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/15/8d/4d/992070e8.jpg" width="30px"><span>叶明</span> 👍（3） 💬（1）<div>可以用 pt-table-checksum 工具来校验主备数据的一致性。主要原理是让主备处于理论上数据一致的视图里，利用事务的可重复读以及函数 WAIT_FOR_EXECUTED_GTID_SET(gtid_set[, timeout]) &#47; MASTER_POS_WAIT(log_name,log_pos[,timeout][,channel]) 来拿到主备理论上的一致性视图，
然后分别计算主备上表分批的 checksum，不同就代表这段范围的数据不一致，再到行级别比对数据。</div>2024-11-12</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/Q3auHgzwzM59PTNiaDASVicbVaeWBU1WKmOgyHcqVtl85nDwAqDicib1EUKE2RRoU0x0vZctZO4kbPDUTTke8qKfAw/132" width="30px"><span>binzhang</span> 👍（2） 💬（1）<div>Question: in chapter &quot;事务怎么回滚（上）&quot;, you mention in undo segment header save TrxID, XA XID, GTID.  what&#39;s difference between TrxID and XA XID and this chapter&#39;s XID?  looks like innodb also write GTID to undo header during two-phase commit?</div>2024-11-21</li><br/>
</ul>