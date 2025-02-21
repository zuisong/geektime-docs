你好，我是唐聪。

我们继续来看如何优化及扩展etcd性能。上一节课里我为你重点讲述了如何提升读的性能，今天我将重点为你介绍如何提升写性能和稳定性，以及如何基于etcd gRPC Proxy扩展etcd性能。

当你使用etcd写入大量key-value数据的时候，是否遇到过etcd server返回"etcdserver: too many requests"错误？这个错误是怎么产生的呢？我们又该如何来优化写性能呢？

这节课我将通过写性能分析链路图，为你从上至下分析影响写性能、稳定性的若干因素，并为你总结出若干etcd写性能优化和扩展方法。

## 性能分析链路

为什么你写入大量key-value数据的时候，会遇到Too Many Request限速错误呢？ 是写流程中的哪些环节出现了瓶颈？

和读请求类似，我为你总结了一个开启鉴权场景的写性能瓶颈及稳定性分析链路图，并在每个核心步骤数字旁边标识了影响性能、稳定性的关键因素。

![](https://static001.geekbang.org/resource/image/14/0a/14ac1e7f1936f2def67b7fa24914070a.png?wh=1920%2A1167)

下面我将按照这个写请求链路分析图，和你深入分析影响etcd写性能的核心因素和最佳优化实践。

## db quota

首先是流程一。在etcd v3.4.9版本中，client会通过clientv3库的Round-robin负载均衡算法，从endpoint列表中轮询选择一个endpoint访问，发起gRPC调用。
<div><strong>精选留言（8）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/22/3b/46/3701e908.jpg" width="30px"><span>Coder</span> 👍（18） 💬（1）<div>老师，请问一下如果业务写多读少，有什么优化办法？难道不能用etcd</div>2021-02-27</li><br/><li><img src="" width="30px"><span>dbo</span> 👍（2） 💬（0）<div>文中下面两句话里的平均延时错了，看图中的结果，应该分别是18.9ms和27.9ms。

下面是 SSD 盘集群，执行如下 benchmark 命令的压测结果，写 QPS 51298，平均延时 189ms。
下面是非 SSD 盘集群，执行同样 benchmark 命令的压测结果，写 QPS 35255，平均延时 279ms。</div>2022-05-01</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/e9/91/4219d305.jpg" width="30px"><span>初学者</span> 👍（1） 💬（2）<div>有2个问题请教一下
1. leader和follower的心跳哪些操作需要落盘操作，为什么磁盘io会影响心跳，进而影响选举？
2. 写请求给client返回成功时，我的理解是leader已经apply了这次写操作的raftlog，为啥还会出现applied index远小于committed index的情况？</div>2021-11-30</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/38/71/65f84229.jpg" width="30px"><span>jiapeish</span> 👍（1） 💬（1）<div>唐老师，文中提到CPU较高时会出现发送心跳的goroutine出现饥饿，这是问什么呢？按说CPU是公平调度，问什么刚好发送心跳的协程会卡呢，这个情况能用nice值之类的解决吗</div>2021-04-02</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/15/4d/bbfda6b7.jpg" width="30px"><span>笃定</span> 👍（0） 💬（0）<div>文中说第八步的时候 Etcd 才会通过授权模块校验是否有权限执行对应的写操作，那如果这个时候权限校验失败，当前用户没有权限写入特定路径的 Key-vaule 数据，那这个时候已经写入的 WAL log 和已经发送给其他 follow 节点的变更 Raft Log 会怎么处理呢？为啥权限校验不在数据写入的时候直接进行校验呢（关于 Raft Log 在其他 follow 节点的处理，我理解为 follow 节点也会进行权限校验，如果权限校验没通过，那么 follow 节点的数据也不会成功写入）</div>2024-12-05</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/ec/21/b0fe1bfd.jpg" width="30px"><span>Adam</span> 👍（0） 💬（0）<div>老师，gRPC proxy跟我前端用一个LB负载均衡有什么区别不？</div>2022-03-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1b/43/c3/2c53acd7.jpg" width="30px"><span>雄鹰</span> 👍（0） 💬（0）<div>老师你好，刚才的问题还没描述完，一不小心点击了“发布”，就直接给发布成功了，不好意思，忽略前一条。我重新描述一下问题。
假设有1000把锁，每把锁有10个线程争抢申请加锁，即1万并发申请加1000锁，线上使用可能短期不会出现这么高的并发量，或者场景有不合理的，请老师指点（申请加锁时，申请加锁重试时间上限时间是8秒，锁持有时间上限是2分钟），5个节点的etcd集群（云服务器，单节点配置 CPU 4核，内存8GB 磁盘是SSD，部署配置采用默认，版本是3.5.2），每十分钟执行一次1万个并发申请加锁（单个key value都不大），持续压测2个多小时，发现etcd集群leader节点内存使用明显比其他4个节点多，再持续压测1个小时左右，leader节点的内存使用耗光，开始的leader节点直接宕机了。请教老师，针对这种情况如何来详细分析及优化？非常感谢。</div>2022-03-03</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/jA97yib7VetXc4iclOg2gGfZu1fO7efyib2mKeqvIxDdmgLqukusyFzPrbIQeZYR0WDJUicRakgVGroaYC7aWGFrEw/132" width="30px"><span>Turing</span> 👍（0） 💬（0）<div>写完之后是要触发watcher的. watcher过多, 查找, 发送event, 时间会稍微增加, 以及内存增大. </div>2021-08-22</li><br/>
</ul>