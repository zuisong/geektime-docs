在实际生产中，关于join语句使用的问题，一般会集中在以下两类：

1. 我们DBA不让使用join，使用join有什么问题呢？
2. 如果有两个大小不同的表做join，应该用哪个表做驱动表呢？

今天这篇文章，我就先跟你说说join语句到底是怎么执行的，然后再来回答这两个问题。

为了便于量化分析，我还是创建两个表t1和t2来和你说明。

```
CREATE TABLE `t2` (
  `id` int(11) NOT NULL,
  `a` int(11) DEFAULT NULL,
  `b` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `a` (`a`)
) ENGINE=InnoDB;

drop procedure idata;
delimiter ;;
create procedure idata()
begin
  declare i int;
  set i=1;
  while(i<=1000)do
    insert into t2 values(i, i, i);
    set i=i+1;
  end while;
end;;
delimiter ;
call idata();

create table t1 like t2;
insert into t1 (select * from t2 where id<=100)
```

可以看到，这两个表都有一个主键索引id和一个索引a，字段b上无索引。存储过程idata()往表t2里插入了1000行数据，在表t1里插入的是100行数据。

# Index Nested-Loop Join

我们来看一下这个语句：

```
select * from t1 straight_join t2 on (t1.a=t2.a);
```

如果直接使用join语句，MySQL优化器可能会选择表t1或t2作为驱动表，这样会影响我们分析SQL语句的执行过程。所以，为了便于分析执行过程中的性能问题，我改用straight\_join让MySQL使用固定的连接方式执行查询，这样优化器只会按照我们指定的方式去join。在这个语句里，t1 是驱动表，t2是被驱动表。

现在，我们来看一下这条语句的explain结果。

![](https://static001.geekbang.org/resource/image/4b/90/4b9cb0e0b83618e01c9bfde44a0ea990.png?wh=1394%2A163)

图1 使用索引字段join的 explain结果

可以看到，在这条语句里，被驱动表t2的字段a上有索引，join过程用上了这个索引，因此这个语句的执行流程是这样的：
<div><strong>精选留言（30）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/14/02/66/4ab9225e.jpg" width="30px"><span>没时间了ngu</span> 👍（117） 💬（9）<div>join这种用的多的，看完还是有很大收获的。像之前讲的锁之类，感觉好抽象，老是记不住，唉。</div>2019-01-30</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/e5/39/951f89c8.jpg" width="30px"><span>信信</span> 👍（376） 💬（19）<div>老师好，回答本期问题：如果驱动表分段，那么被驱动表就被多次读，而被驱动表又是大表，循环读取的间隔肯定得超1秒，这就会导致上篇文章提到的：“数据页在LRU_old的存在时间超过1秒，就会移到young区”。最终结果就是把大部分热点数据都淘汰了，导致“Buffer pool hit rate”命中率极低，其他请求需要读磁盘，因此系统响应变慢，大部分请求阻塞。</div>2019-01-30</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/ea/9a/02d589f9.jpg" width="30px"><span>斜面镜子 Bill</span> 👍（238） 💬（6）<div>因为 join_buffer 不够大，需要对被驱动表做多次全表扫描，也就造成了“长事务”。除了老师上节课提到的导致undo log 不能被回收，导致回滚段空间膨胀问题，还会出现：1. 长期占用DML锁，引发DDL拿不到锁堵慢连接池； 2. SQL执行socket_timeout超时后业务接口重复发起，导致实例IO负载上升出现雪崩；3. 实例异常后，DBA kill SQL因繁杂的回滚执行时间过长，不能快速恢复可用；4. 如果业务采用select *作为结果集返回，极大可能出现网络拥堵，整体拖慢服务端的处理；5. 冷数据污染buffer pool，block nested-loop多次扫描，其中间隔很有可能超过1s，从而污染到lru 头部，影响整体的查询体验。</div>2019-01-31</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/03/f7/3a493bec.jpg" width="30px"><span>老杨同志</span> 👍（67） 💬（1）<div>对被驱动表进行全表扫描，会把冷数据的page加入到buffer pool.,并且block nested-loop要扫描多次，两次扫描的时间可能会超过1秒，使lru的那个优化失效，把热点数据从buffer pool中淘汰掉，影响正常业务的查询效率</div>2019-01-30</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTIu1n1DhUGGKTjelrQaLYOSVK2rsFeia0G8ASTIftib5PTOx4pTqdnfwb0NiaEFGRgS661nINyZx9sUg/132" width="30px"><span>Zzz</span> 👍（46） 💬（7）<div>林老师，我没想清楚为什么会进入young区域。假设大表t大小是M页&gt;old区域N页，由于Block Nested-Loop Join需要对t进行k次全表扫描。第一次扫描时，1~N页依次被放入old区域，访问N+1页时淘汰1页，放入N+1页，以此类推，第一次扫描结束后old区域存放的是M-N+1~M页。第二次扫描开始，访问1页，淘汰M-N+1页，放入1页。可以把M页想象成一个环，N页想象成在这个环上滑动的窗口，由于M&gt;N，不管是哪次扫描，需要访问的页都不会在滑动窗口上，所以不会存在“被访问的时候数据页在 LRU 链表中存在的时间超过了 1 秒“而被放入young的情况。我能想到的会被放入young区域的情况是，在当次扫描中，由于一页上有多行数据，需要对该页访问多次，超过了1s，不管这种情况就和t大小没关系了，而是由于page size太大，而一行数据太少。</div>2019-01-30</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/df/87/0e05dadd.jpg" width="30px"><span>清风浊酒</span> 👍（45） 💬（2）<div>老师您好，left join 和 right join 会固定驱动表吗？</div>2019-01-30</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/f1/0e/e9b57b9b.jpg" width="30px"><span>泡泡爱dota</span> 👍（38） 💬（4）<div>explain select * from t1 straight_join t2 on (t1.a=t2.a) where t1.a &lt; 50; 
老师, 这条sql为什么t1.a的索引没有用上, t1还是走全表
</div>2019-01-31</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/69/d9/968df259.jpg" width="30px"><span>郝攀刚จุ๊บ</span> 👍（28） 💬（7）<div>业务逻辑关系，一个SQL中left join7，8个表。这我该怎么优化。每次看到这些脑壳就大！</div>2019-01-30</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/57/96/b65bdf43.jpg" width="30px"><span>萤火虫</span> 👍（25） 💬（14）<div>年底了有一种想跳槽的冲动 身在武汉的我想出去看看 可一想到自身的能力和学历 又不敢去了 苦恼... </div>2019-01-30</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/Nic2zzpAuiadVibETy3Um3IcjOa4O9gr8zVagG6tCbMlFF8O3tNmwMJicEEsA9pibcxgibtyKhl1ZicXYX8kLfXs6AMmg/132" width="30px"><span>呵呵</span> 👍（19） 💬（1）<div>老师，新年好！
优化器会自动选择小表作为驱动表，那么我们人为把小表写成驱动表还有意义吗？ </div>2019-02-11</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/NhbRicjvf8v3K6D3v1FtOicxOciaPZQsCjCmuGCqea4vJeRVaLicKLpAcFQlcTgLvczBWY7SYDkeOtibxXj1PGl7Nug/132" width="30px"><span>柚子</span> 👍（14） 💬（5）<div>join在热点表操作中，join查询是一次给两张表同时加锁吧，会不会增大锁冲突的几率？
业务中肯定要使用被驱动表的索引，通常我们是先在驱动表查出结果集，然后再通过in被驱动表索引字段，分两步查询，这样是否比直接join委托点？</div>2019-01-30</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/c6/ac/60d1fd42.jpg" width="30px"><span>抽离の❤️</span> 👍（14） 💬（1）<div>早上听老师一节课感觉获益匪浅</div>2019-01-30</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/49/8b/3596a3e2.jpg" width="30px"><span>403</span> 👍（13） 💬（1）<div>用那个作为驱动表，mysql会自己优化么？</div>2019-02-09</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/RNO4yZyBvic914hewmNNE8iblYDcfv5yGHZ9OnKuCuZXNmGR0F5qV3icKLT2xpMt66GyEpicZVvrmz8A6TIqt92MQg/132" width="30px"><span>啊啊啊哦哦</span> 👍（12） 💬（1）<div>NLJ join算法下。  驱动表假设全表先扫描。  这个全表扫描的数据存放在哪。 buffer bool中还是。全表扫描到单独的read buffer中？ 我的理解是。 驱动表全表扫描的数据。是从buffer bool中找驱动表的数据到 read buffer中。如果buffer bool 没有。那么从磁盘。到buffer bool 然后在到read buffer 中。 我的理解对吗。 </div>2019-03-31</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/dd/40/a185dfcb.jpg" width="30px"><span>思考特～</span> 👍（12） 💬（6）<div>老师，这边想请教一个困扰很久的问题，用mysql经常会制定这么一个规则，不允许多表join。从实际情况看，几乎不太可能遵守这个规则，有个交易的业务场景涉及 用户表 300W、订单表 900W、支付表 900W，每次需要查一个用户下面的订单信息可能就有点慢了，但是还能接受，如果是查询一个团体的订单信息，这个量就非常可观了,查询有时候根本返回不了结果。根本无法避免多表Join，所以想问问老师，在这种需要多表Join业务场景下，如何设计表，来提升性能？或者有这方面推荐的资料可以参考的</div>2019-03-03</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/40/5e/b8fada94.jpg" width="30px"><span>Ryoma</span> 👍（12） 💬（1）<div>上文中使用索引时扫描行数为200，但是根据字段a去做树搜索时，由于字段a是普通索引，在找到匹配值后还会继续匹配，实际上每个循环都做了至少两次的行扫描。
老师，这么理解对么？</div>2019-01-31</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/92/cd/d39e568c.jpg" width="30px"><span>felix</span> 👍（11） 💬（1）<div>不让用join，那用什么呢，用逗号分隔两表？
join有多个条件的话，写在on后面和where后面有什么区别吗？</div>2019-01-31</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/f3/69/7039d03f.jpg" width="30px"><span>渔村蓝</span> 👍（9） 💬（2）<div>但是，Block Nested-Loop Join 算法的这 10 万次判断是内存操作，速度上会快很多，性能也更好。
那Simple那种是直接在引擎里面计算吗？但是计算不都应该在内存吗？所以不理解为什么这里会更快，难得一次抢到这么早的留言，请老师指教，谢谢。</div>2019-01-30</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/93/c7/86352ccc.jpg" width="30px"><span>1024</span> 👍（8） 💬（4）<div>文中解释NLJ和BNL时间复杂度相同，都是M*N。但是对于BNL性能好于NLJ的原因只是提到:&quot;BNL的判断是在内存中操作，速度上会快很多，性能也更好&quot;。请问老师？这句话的言外之意是: NLJ的判断不是在内存中操作吗？不将数据加载到内存，CPU如何进行判断呢?</div>2019-02-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/0d/a9/8ddbfcd9.jpg" width="30px"><span>Franis</span> 👍（7） 💬（2）<div>老师，想问一下，如果是“一对多”的多个表进行join的话，应该选择“多”的表作为驱动表，还是选择“一”的表作为驱动表呢？</div>2019-03-03</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/3XbCueYYVWTiclv8T5tFpwiblOxLphvSZxL4ujMdqVMibZnOiaFK2C5nKRGv407iaAsrI0CDICYVQJtiaITzkjfjbvrQ/132" width="30px"><span>有铭</span> 👍（7） 💬（1）<div>今天这篇看了犹如醍醐灌顶一般，以前一直没搞明白当表数据比较大的时候join_buf是如何工作的，原来是分段载入的</div>2019-01-31</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/ed/1a/269eb3d6.jpg" width="30px"><span>cfanbo</span> 👍（7） 💬（1）<div>explain select * from t1 straight_join t2 on (t1.b=t2.b) where t2.id&lt;=50;
explain select * from t2 straight_join t1 on (t1.b=t2.b) where t2.id&lt;=50;
看两个sql的分析结果的 rows列数量，数量小的作为驱动表。而对于记录个数一样的，则采用存放 到 join buffer 里的字段数量来决定。
这样理解对么？</div>2019-01-30</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/14/98/0251b8fd.jpg" width="30px"><span>Cy190622</span> 👍（6） 💬（1）<div>专栏已经更新完毕，首先谢谢老师；有以下几个小问题，希望老师有时间能够看到。
1.普通的join查询是被执行器优化执行过的吧？但是优化执行是否做到最好呢？怎么验证一下优化过程用的是那种方式呢？是用两个表互换explain一下吗？
2.这种查询优化在Mysql哪个版本中做了较大的加强。
3.SELECT * FROM t1 STRAIGHT_JOIN t2 ON (t1.a=t2.b);  （t1是以a为索引的100行数据，t2中b非索引1000条数据）t1做了驱动表，属于BNL情形；如果用t2作为驱动表，t1的a索引就可以用，属于NLJ情形，选择哪个表作为驱动表更好呢？
</div>2019-03-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/0d/a9/8ddbfcd9.jpg" width="30px"><span>Franis</span> 👍（5） 💬（2）<div>如果我产品表有十条数据，订单表有一万条数据。
为什么我用订单表作为驱动表会比用产品表作为驱动表速度快呢？</div>2019-03-04</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTIu1n1DhUGGKTjelrQaLYOSVK2rsFeia0G8ASTIftib5PTOx4pTqdnfwb0NiaEFGRgS661nINyZx9sUg/132" width="30px"><span>Zzz</span> 👍（5） 💬（1）<div>林老师，关于课后问题，很多留言都提到大表数据会进入LRU young区域，这个是一定发生的吗？如果大表数据少于LRU old区域的大小，那所有大表数据都会进入young区域没问题。如果大表数据多于old区域的大小，下次扫描的时候早进入old区域的page都已经被淘汰出去，所以不会因为超过1s而进入young区域，导致的结果就是old区域hit很低，读取新一页都需要从磁盘读取到内存。</div>2019-01-30</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/05/d4/e06bf86d.jpg" width="30px"><span>长杰</span> 👍（5） 💬（2）<div>我们在上文说到，使用 Block Nested-Loop Join 算法，可能会因为 join_buffer 不够大，需要对被驱动表做多次全表扫描。
在这个情况下，由于被驱动表是冷表，被多次全表扫描，LRU算法虽然做了优化分为yong区和old区，但是join_buffer不够大，驱动表被分成多个block，被驱动表要查多次，会占用young区，导致bp命中率下降。</div>2019-01-30</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/00/f0/08409e78.jpg" width="30px"><span>一大只😴</span> 👍（4） 💬（1）<div>老师，我想问下，如果使用的是Index Nested-Loop Join，是不是就不会使用join_buffer了？直接将循环结果放到net_buffer_length中，边读边发哈？</div>2019-01-31</li><br/><li><img src="" width="30px"><span>700</span> 👍（4） 💬（1）<div>老师，您好。看完文章后有如下问题请教：
1）文章内容「可以看到，在这个查询过程，也是扫描了 200 行，但是总共执行了 101 条语句，比直接 join 多了 100 次交互。除此之外，客户端还要自己拼接 SQL 语句和结果。」
这个有没有啥方法来仅通过1次交互就将这101条语句发到服务端执行？

2）文章内容「每次搜索一棵树近似复杂度是以 2 为底的 M 的对数，记为 log2M，所以在被驱动表上查一行的时间复杂度是 2*log2M。」
这个复杂度的计算难理解，为什么是这么计算？
假设 M = 256，则搜索树的复杂度为8？

3）文章内容「因此整个执行过程，近似复杂度是 N + N*2*log2M。」
驱动表的复杂度直接记为 N？

4）文中提到索引扫描需扫1行数据，全表扫描需扫1000行数据。这是由统计信息决定的？

提前感谢老师！</div>2019-01-30</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/77/fd/c6619535.jpg" width="30px"><span>XD</span> 👍（4） 💬（3）<div>老师，三个表关联的执行流程也是一样的吗？记得阿里的mysql规范里有一条不允许3个及以上表进行join操作，这个原因是？</div>2019-01-30</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/b0/37/d654fbac.jpg" width="30px"><span>几近虚年</span> 👍（3） 💬（1）<div>    看了老师的课程，现在看到34讲，前面的锁、索引等基础常用的东西，因为我是Java开发嘛，有普通的SQL操作经验，所以看了以后很有收获。 但是到了分库分表、读写分离的课程，看着就很吃力了，之前没有做过类似的东西。
    但是总的来说，收获超级大，这是我进极客时间买的第一个课程，也是现在最有价值的课程，真的非常感谢老师的辛苦码字和把技术表达。
    看完这个课程，然后继续看老师推荐的书籍《高性能MySQL》。等跳槽后，把现在所学的基础类型的知识都应用一遍，然后分库那些再看有环境的话实践实践，最后再回过头，反复看老师中间段课程的知识点，到时候相信收获肯定也很大。
    感谢老师。</div>2019-02-21</li><br/>
</ul>