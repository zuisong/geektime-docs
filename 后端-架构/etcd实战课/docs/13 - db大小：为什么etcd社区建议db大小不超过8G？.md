你好，我是唐聪。

在[03](https://time.geekbang.org/column/article/336766)写流程中我和你分享了etcd Quota模块，那么etcd为什么需要对db增加Quota限制，以及不建议你的etcd集群db大小超过8G呢？ 过大的db文件对集群性能和稳定性有哪些影响？

今天我要和你分享的主题就是关于db大小。我将通过一个大数据量的etcd集群为案例，为你剖析etcd db大小配额限制背后的设计思考和过大的db潜在隐患。

希望通过这节课，帮助你理解大数据量对集群的各个模块的影响，配置合理的db Quota值。同时，帮助你在实际业务场景中，遵循最佳实践，尽量减少value大小和大key-value更新频率，避免db文件大小不断增长。

## 分析整体思路

为了帮助你直观地理解大数据量对集群稳定性的影响，我首先将为你写入大量数据，构造一个db大小为14G的大集群。然后通过此集群为你分析db大小的各个影响面，db大小影响面如下图所示。

![](https://static001.geekbang.org/resource/image/ab/11/ab657951310461c835963c38e43fdc11.png?wh=1920%2A685)

首先是**启动耗时**。etcd启动的时候，需打开boltdb db文件，读取db文件所有key-value数据，用于重建内存treeIndex模块。因此在大量key导致db文件过大的场景中，这会导致etcd启动较慢。

其次是**节点内存配置**。etcd在启动的时候会通过mmap将db文件映射内存中，若节点可用内存不足，小于db文件大小时，可能会出现缺页文件中断，导致服务稳定性、性能下降。
<div><strong>精选留言（13）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/14/e8/e5/fd4c7ea6.jpg" width="30px"><span>雾雾glu</span> 👍（10） 💬（2）<div>请教一下老师：
看到阿里贡献的 cncf 博客中提到了，优化了算法后可以将存储提升至 100G: https:&#47;&#47;www.cncf.io&#47;blog&#47;2019&#47;05&#47;09&#47;performance-optimization-of-etcd-in-web-scale-data-scenario&#47;#Conclusion

但是在官方文档中，还是写着的是 8G，不确定这个数据是否是最新的？
</div>2021-02-25</li><br/><li><img src="" width="30px"><span>fran712</span> 👍（10） 💬（2）<div>请问老师：
etcd的数据容量是直接查看数据目录的大小？还是通过prometheus等监控手段查看？还是通过API或命令查看?</div>2021-02-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/24/ee/ab/15cfcfc5.jpg" width="30px"><span>冬至未至</span> 👍（5） 💬（2）<div>求教大佬：
“将 limit 参数下推到了索引层，实现查询性能百倍提升” 这个下推到索引层，具体是怎么样的操作呢？</div>2021-02-25</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/41/38/4f89095b.jpg" width="30px"><span>写点啥呢</span> 👍（1） 💬（2）<div>请问下老师：
1. etcd启动时候构建treeindex为什么需要加锁？如果构建时候是单goroutine是否可以避免加锁操作？
2. .&#47;benchmark put --key-size 32 --val-size 10240 --total 1000000 --key-space-size 2000000 --clients 50 --conns 50 这个命令total参数是1个M，为啥会插入1.2M个key呢？</div>2021-02-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/13/45/16c60da2.jpg" width="30px"><span>蔫巴的小白菜</span> 👍（0） 💬（2）<div>请问老师：
在提到提交事务延迟过高，有freelist的原因，原因是申请n个page会增加耗时，我没理解的是：
freelist本就是空闲列表，直接取n个就可以了，为什么会增加耗时呢？难道是申请n个连续的内存？</div>2021-03-30</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/28/d9/84/9b03cd04.jpg" width="30px"><span>lidabai</span> 👍（1） 💬（1）<div>如何查看etcd中db的大小？</div>2022-06-25</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1e/f0/8b/a806789b.jpg" width="30px"><span>int8</span> 👍（1） 💬（0）<div>长事务导致db增大是因为长事务可能会阻塞压缩任务的执行么？</div>2021-06-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1a/2e/c5/231114ed.jpg" width="30px"><span>Hadesu</span> 👍（0） 💬（0）<div>不支持数据分片，制约了etcd的数据规模。在分布式环境做数分片分裂，分片合并，分片迁移和分片清理，需要克服一系列的问题。如分片变化过程中如何不停服，如何减少对服务影响，如何做到数据不丢失等等。业界应该有成熟的解决方案。但很多公开的资料都回避数据分片的内容或者三言两语地简单略过（导致读者不知道如何实现）。如果作者有数据分片详细且可落地的方案，希望分享一下。</div>2024-08-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/20/8b/c5/6e06e49c.jpg" width="30px"><span>愁脾气的愁妖精</span> 👍（0） 💬（0）<div>想问就是如果etcd有一次设置quato-backend-bytes为4G之后，是保持这个配额大小吗，还是停掉之后把这个配置删掉之后重启就又变成了2G，那如果之前内存已经是3G多呢</div>2021-12-15</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/07/d2/0d7ee298.jpg" width="30px"><span>惘 闻</span> 👍（0） 💬（1）<div>为什么长事务会导致db增大呢？</div>2021-08-06</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/28/82/02/0bf31808.jpg" width="30px"><span>天照</span> 👍（0） 💬（0）<div>请问唐老师是否遇到过这种情况：
当DBsize较大时，而且集群处理的写入请求较高时，要保证调用业务无损情况下，单节点重启、动态扩容操作失败</div>2021-07-07</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/96/bc/82a7becd.jpg" width="30px"><span>华仔</span> 👍（0） 💬（0）<div>请教老师，
当前说建议db大小不超过8G，怎么样去查询出当前的etcd的db存储能力是默认的2G或者是被调整过的大小呢？想查看下如果调整到了8G，怎么样可以查看到是否调整生效。</div>2021-05-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1b/96/47/93838ff7.jpg" width="30px"><span>青鸟飞鱼</span> 👍（0） 💬（0）<div>长常务导致db增大，是因为用了写时复制吗？</div>2021-05-11</li><br/>
</ul>