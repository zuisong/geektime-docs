你好，我是大明。

从这节课开始，我们将进入数据库这一章。在实际工作中，数据库设计得好不好、SQL 写得好不好将极大程度影响系统性能。而且，即便是再小的公司，也不可能说没有数据库，所以如果你担忧自己因为没有微服务架构经验难以通过面试，那么数据库就可以成为你反败为胜的一个点。

所以今天我们来聊一聊数据库中的第一个话题——索引。

索引在数据库面试中占据了相当大的比重。但是大部分人面试索引的时候都非常机械，所以难以在面试官心中留下深刻印象。索引是一个理论和实践的结合，今天这节课我先带你分析索引的基本原理，下节课我再在 SQL 优化这一个大主题下进一步带你分析索引设计和优化的实战案例。

索引的内容还是非常多的，尤其是有很多非常细碎的、不成体系的点，记起来非常难。所以这一节课我就会尽量用非常简单的话，以及一些奇妙的比喻来帮助你记忆和索引有关的内容。

## 前置知识

索引是用来加速查找的数据结构。绝大多数跟存储、查找有关的中间件都有索引功能，但是它们的原理不尽相同。

我们先来了解一下B+树的定义与特征。

### B+ 树

B+ 树是一种多叉树，一棵m阶的B+树定义如下：

1. 每个节点最多有 m 个子女。
2. 除根节点外，每个节点至少有 `[m/2]` 个子女，根节点至少有两个子女。
3. 有 k 个子女的节点必有 k 个关键字。
<div><strong>精选留言（12）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/11/44/48/fae317c1.jpg" width="30px"><span>子休</span> 👍（17） 💬（1）<div>关于索引列区分度的问题，这里稍微补充一个例子。
其实也未必所有区分度不高的索引都不会生效，比如一个列里面只有0和1两种值，看上去似乎区分度不高，但是如果0和1的值比例完全失衡，比如是95:5的比例，那么这种索引也有可能是生效。
比如一般的任务表里面，状态字段绝大多数都是“success”，少部分是“failed”，如果你查询的是失败的记录，这个时候状态字段的索引就可以生效了。</div>2023-07-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/b4/a5/396268e5.jpg" width="30px"><span>死者苏生</span> 👍（8） 💬（3）<div>https:&#47;&#47;zhuanlan.zhihu.com&#47;p&#47;519658576  mongodb用的wiredTiger就是B+树，建议这篇修改下，不要误人子弟</div>2023-07-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/ce/6d/530df0dd.jpg" width="30px"><span>徐石头</span> 👍（5） 💬（1）<div>SELECT id, name FROM user_tab WHERE id = 123，这个SQL中需要强调id不是作为主键，因为id如果是主键，就会直接走主键索引，无法体现覆盖索引中只查询索引中的字段的过程，另外联合索引&lt;id，name&gt;中如果SQL改成SELECT id, name，age FROM user_tab WHERE id = 123就无法实现覆盖索引的效果</div>2023-07-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/0c/52/f25c3636.jpg" width="30px"><span>长脖子树</span> 👍（4） 💬（3）<div>Mongo用的就是B+树</div>2023-07-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/25/87/f3a69d1b.jpg" width="30px"><span>peter</span> 👍（2） 💬（1）<div>确认一下理解：根据文章内容，索引其实是表的一部分数据，如果表的数据是100M，那么，某个索引包含其中的10M数据，这样共有100M + 10M。这10M是表数据之外的数据，是表数据中某部分数据的一个拷贝。比如，表中有一个字段“name = zhangsan”,建立与该name的索引后，磁盘中有两份name。是这样吗？</div>2023-07-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/2a/44/e6/2c97171c.jpg" width="30px"><span>sheep</span> 👍（1） 💬（5）<div>你有没有遇到过索引设计不合理引发的线上故障？
线上ddl操作，需要删除一个索引，然后新建一个，删除之后，出现堆积大量的慢查询；这时候新建索引会被阻塞住（mdl读锁和写锁），后面的查询也一并阻塞住了。
解决办法是：临时关闭服务对外使用，kill掉创建索引后面的查询，待索引创建成功后，服务再恢复使用</div>2023-09-20</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/PiajxSqBRaEIw0wz2BO1OXKUD4h7RQ82mGQ8Zt6ibURuz4ciagvKgwGCJmXVVMqZggHZloEEvLgcuXd7x5YzpibibaUnqfZWROKeVIOnVApjR6FsrbqIHU3v32g/132" width="30px"><span>Geek_c1118e</span> 👍（0） 💬（0）<div>请教一下老师：InnoDB存储引擎的非主键（辅助索引等）和非聚簇索引是否是一个概念，另外，像MyISM中叶子节点存储地址的也是非聚簇索引，所以非聚簇索引是包含这两种格式吗？（：网上看一些相关概念有点混淆，想确认一下</div>2024-02-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/fd/49/2f38bb6d.jpg" width="30px"><span>Singin in the Rain</span> 👍（0） 💬（1）<div>关于哈希索引，文中提到『但是 MySQL 的 InnoDB 引擎并不支持这种索引。』这一段表述不是很精确。哈希索引确实用在MEMORY存储引擎中，但是这种索引存在一个变种，自适应哈希索引，InnoDB引擎通过innodb_adaptive_hash_index参数控制在其内部使用。</div>2023-08-25</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/2e/32/94/1596385e.jpg" width="30px"><span>小戴同学</span> 👍（0） 💬（4）<div>请教一下：
&quot;这个数据行存放在磁盘里，所以触发磁盘 IO 之后能够读取出来。磁盘 IO 是非常慢的，因此回表性能极差，你在实践中要尽可能避免回表&quot;这句话说回表的性能差的原因，但是前面&quot;一个默认的前提就是索引本身会全部装进内存中，只有真实的数据行会放在磁盘上&quot;，那使用主键索引也需要走磁盘，性能差别就是拿到主键之后再去拿数据的性能差吗？</div>2023-08-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/19/43/0b/7688f18c.jpg" width="30px"><span>江 Nina</span> 👍（0） 💬（5）<div>“如果查询条件是 WHERE A = a1 OR B = b1，那么这个查询并不会使用这个索引。” 这个是为什么呢 明白b不会走索引 但是感觉前一个A会走索引啊</div>2023-08-04</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/2a/39/93/f0247cf8.jpg" width="30px"><span>一本书</span> 👍（0） 💬（2）<div>如果你查询一张表，用到了索引，那么数据库就会先在索引里面找到主键，然后再根据主键去聚簇索引中查找，最终找出数据。
老师请教一下Q1：为啥是用到了索引，还要从索引里面找到主键，在通过主键回表查呢？不能通过主键直接查吗？是不是因为这个索引用的不是聚簇索引。存的是主键，只好通过主键去查了。
Q2：聚簇索引和非聚簇索引，可以人为的去干预吗？全部用聚簇，是不是就不会产生回表了。</div>2023-08-01</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/28/44/cf/791d0f5e.jpg" width="30px"><span>ZhiguoXue_IT</span> 👍（0） 💬（3）<div>我们之前遇到过一次线上问题，删了索引，导致数据插不进去了。
</div>2023-07-18</li><br/>
</ul>