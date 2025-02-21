你好，我是俊达。

上一讲的思考题中，我留了一个问题，就是删除表或索引时，表或索引已经缓存在Buffer Pool中的数据要怎么处理。实际上处理的方式跟表的类型（是普通表还是临时表，是否使用per-table）以及操作类型有关，还跟MySQL的版本有关，这一讲我会对这些情况做一些分析。

InnoDB还使用了自适应Hash索引（Adaptive Hash Index，AHI）、Change Buffer、Double Write Buffer，来提升性能或数据的可靠性，这一讲中我也会分别进行介绍。

## DDL和Buffer Pool

### 删除表（DROP Table/Truncate Table）

我们先来看一下DROP一个使用独立表空间（innodb\_file\_per\_table=ON）的普通表时，InnoDB内部需要做哪些处理。

首先要将AHI中，跟这个表相关的索引条目清理掉。上一讲中我们提到过，每一个页面的控制块中，有一个AHI结构。如果一个索引页面缓存在AHI中，那么控制块的ahi.index中会指向这个索引。索引在内存中还维护了一个search\_info结构，里面记录了索引中有多少个页面缓存到了AHI中。如果被删除的表，确实有页面缓存在AHI中，那么就要扫描每个Buffer实例的LRU链表，检查每个页面是不是存在和正在删除的这个表相关的AHI条目。如果有，先将页面添加到一个临时数组中，临时数组中的页面达到一定数量时，再批量清理这些页面相关的AHI条目。
<div><strong>精选留言（2）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/3c/4a/fe/7b6bd101.jpg" width="30px"><span>笙 鸢</span> 👍（0） 💬（1）<div>老师，change buffer和double write buffer的内存地址是都在buffer pool的内存里面，还是自己单独的内存空间啊</div>2024-12-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/8d/4d/992070e8.jpg" width="30px"><span>叶明</span> 👍（0） 💬（1）<div>相比于以前机械硬盘的几百 IOPS，现在的固态硬盘硬盘动不动上万的 IOPS，IO 能力提升了好几个数量级。
关闭的原因有几个
首先，如果你是固态硬盘，那么开启 change buffer 和 ahi 带来的性能提升很小，但维护 change buffer 代码的代价却不小，现在很多新的功能已经不兼容 change buffer 了，比如倒序索引，https:&#47;&#47;github.com&#47;mysql&#47;mysql-server&#47;blob&#47;trunk&#47;storage&#47;innobase&#47;rem&#47;rem0cmp.cc#L676-L682

其次，关闭掉 change buffer 和 ahi，buffer pool 能缓存的数据页更多，加上固态磁盘随机 IO 能力的增强，即使多几次 IO 影响也不大。</div>2024-10-25</li><br/>
</ul>