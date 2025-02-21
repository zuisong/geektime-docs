你好，我是李玥。

对于任何一个企业来说，数据安全的重要性是不言而喻的。我在开篇词中也曾经强调过，凡是涉及到数据的问题，都是损失惨重的大问题。

能够影响数据安全的事件，都是极小概率的事件，比如说：数据库宕机、磁盘损坏甚至机房着火，还有最近频繁出现在段子中“程序员不满老板删库跑路”的梗儿，但这些事儿一旦发生了，我们的业务就会损失惨重。

一般来说，存储系统导致的比较严重的损失主要有两种情况，一是数据丢失造成的直接财产损失，比如大量的坏账；二是由于存储系统损坏，造成整个业务系统停止服务而带来的损失。

所谓防患于未然，你从设计一个系统的第一天起，就需要考虑在出现各种问题的时候，如何来保证这个系统的数据安全性。今天我们来聊一聊，如何提前预防，将“删库跑路”等这类问题导致的损失尽量降到最低。

## 如何更安全地做数据备份和恢复？

保证数据安全，最简单而且有效的手段就是定期备份数据，这样出现任何问题导致的数据损失，都可以通过备份来恢复数据。但是，如何备份，才能最大程度地保证数据安全，并不是一个简单的事儿。

2018年还出现过某个著名的云服务商因为硬盘损坏，导致多个客户数据全部丢失的重大故障。这么大的云服务商，数据是不可能没有备份的，按说硬盘损坏，不会导致数据丢失的，但是因为各种各样的原因，最终的结果是数据的三个副本都被删除，数据丢失无法找回。
<div><strong>精选留言（30）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/16/e7/76/79c1f23a.jpg" width="30px"><span>李玥</span> 👍（64） 💬（1）<div>Hi，我是李玥。

照例说一下上节课思考题：

我们在电商的搜索框中搜索商品时，它都有一个搜索提示的功能，比如我输入“苹果”还没有点击搜索按钮的时候，搜索框下面会提示“苹果手机”、“苹果11、苹果电脑”这些建议的搜索关键字，请你课后看一下ES的文档，想一下，如何用ES快速地实现这个搜索提示功能？

在课后留言中，Geek_c76e2d同学给出的答案非常赞，我在这里就直接“盗用”了，以下是Geek_c76e2d同学的答案：

因为用户每输入一个字都可能会发请求查询搜索框中的搜索推荐。所以搜索推荐的请求量远高于搜索框中的搜索。es针对这种情况提供了suggestion api，并提供的专门的数据结构应对搜索推荐，性能高于match，但它应用起来也有局限性，就是只能做前缀匹配。再结合pinyin分词器可以做到输入拼音字母就提示中文。如果想做非前缀匹配，可以考虑Ngram。不过Ngram有些复杂，需要开发者自定义分析器。比如有个网址www.geekbang.com，用户可能记不清具体网址了，只记得网址中有2个e，此时用户输入ee两个字母也是可以在搜索框提示出这个网址的。以上是我在工作中针对前缀搜索推荐和非前缀搜索推荐的实现方案。</div>2020-03-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/0c/0f/93d1c8eb.jpg" width="30px"><span>mickey</span> 👍（24） 💬（1）<div>请问，回放binlog是幂等性的，那为什么我连续执行两条相同的mysqlbinlog语句后，系统报错了呢（第一次执行正常，数据恢复）？
语句：mysqlbinlog --start-datetime &quot;2020-04-17 10:00:00&quot; --stop-datetime &quot;2020-04-17 10:48:00&quot; E:\data\test\mysql-bin.010163 | mysql -uroot -p

报错：ERROR 1062 (23000) at line 33: Duplicate entry &#39;4&#39; for key &#39;PRIMARY&#39;</div>2020-04-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/23/72/70190bc1.jpg" width="30px"><span>子不语</span> 👍（19） 💬（5）<div>老师，您这里提到的高可用方案，把binlog日志同步到从库，然后从库立即回放。那如果是删库的动作，从库也回放，不是把从库也干掉了。</div>2020-04-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/20/08/bc06bc69.jpg" width="30px"><span>Dovelol</span> 👍（16） 💬（1）<div>老师好，想问下有没有什么比较好的监控mysql性能还有主从延迟之类的工具，还有就是读写分离在遇到主从延迟突然增大的情况下该怎么办呢？</div>2020-03-15</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/86/06/72b01bb7.jpg" width="30px"><span>美美</span> 👍（14） 💬（3）<div>一主多从同步复制有点类似于KafKa的ISR。
有一个疑惑，还请老师解惑。感觉这种模式还是会有丢数据的可能。比如，第一次请求同步到从A成功，从B延迟。第二次同步给从B，从A延迟。然后主挂掉，此时感觉切从A或者从B都会有问题。</div>2020-03-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1b/a4/27/15e75982.jpg" width="30px"><span>小袁</span> 👍（11） 💬（1）<div>老师，你说同步复制性能差，哪到底差到一个什么样的程度呢？有定量的测试数据么？</div>2020-03-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/81/e6/6cafed37.jpg" width="30px"><span>旅途</span> 👍（10） 💬（1）<div>老师 问一下 使用全量备份和binlog增量 这个binlog 删除以前的吗？还是保留全量所有的？</div>2020-03-15</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/1a/05/f154d134.jpg" width="30px"><span>刘楠</span> 👍（5） 💬（4）<div> binlog 日志中也是有删除库的SQL的，难道，备库或者从库不会执行吗？感觉会执行，所以数据在几个库都删除了。怎么保证备库或者从的数据？</div>2020-03-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/64/9b/d1ab239e.jpg" width="30px"><span>J.Smile</span> 👍（2） 💬（1）<div>老师，如果系统只有一个binlog，而且delete操作就在这个binlog.那应该就不能回放了，因为回放的最后还是delete这个误操作！</div>2020-04-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/64/9b/d1ab239e.jpg" width="30px"><span>J.Smile</span> 👍（2） 💬（1）<div>一主二从架构下，如果其中一个从宕机，重启后应该可以自动回放binlog吧，不然这个架构也就失去意义了！</div>2020-04-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/9a/a6/3bddb98c.jpg" width="30px"><span>大叶枫</span> 👍（2） 💬（2）<div>李大师，想了解mysql大买家大卖家单库数据倾斜的慢sql问题～</div>2020-03-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/0c/0f/93d1c8eb.jpg" width="30px"><span>mickey</span> 👍（1） 💬（1）<div>
$mysql -uroot test &lt; test.sql  少了个 -p</div>2020-04-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/12/70/10faf04b.jpg" width="30px"><span>Lywane</span> 👍（0） 💬（3）<div>如果跑路的人比较&quot;变态&quot;，执行脚本来删除，删除语句和正常的业务语句都混合在一起了。。。是不是就没办法恢复了</div>2020-05-15</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/2QR4YBpeXgVXGXIfnibt80oLbjibIdp1c5ty5wbBTHvgheZRcLWDZAVklOpG2yjlDS2N3rZH66pDOvsvvqI2ic7icw/132" width="30px"><span>ljr_bird</span> 👍（0） 💬（1）<div>想问下老师，其实我们是使用阿里云的mysql主从方式，按介绍是属于第二种的自动切换，那么就是可能出现数据丢失的情况是吗</div>2020-04-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/85/bf/36b01d36.jpg" width="30px"><span>德斯儿</span> 👍（0） 💬（1）<div>Galera Gluster这种方案和课程中介绍的这三种方案有什么区别呢</div>2020-03-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/ec/18/bf7254d3.jpg" width="30px"><span>肥low</span> 👍（0） 💬（1）<div>很不幸 主从延迟的问题就发生在身边，主要也是主库压力大，延迟时间几个小时都有可能，主库倒是没有当机，但是延迟这么久也是醉了，目前有些对实时性要求高的业务都是通过维护一个Cache来解决延迟问题的，大佬有没有什么更好的办法呢</div>2020-03-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/45/4f/f94caf47.jpg" width="30px"><span>qbit</span> 👍（38） 💬（0）<div>腾讯云是一家著名的云服务商:-D</div>2020-03-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/4d/ba/83e6dcbf.jpg" width="30px"><span>skyline</span> 👍（28） 💬（2）<div>除了技术方面，我觉得删库跑路也是一个管理机制上的问题，要当成不可抗因素去对待。

为防止地震我们需要异地备份，距离越远越好，为防止跑路我们需要完善的权限管理。

不能让一个人有能接触到所有备份的权限，否则就跟单机故障一样出现&quot;单人故障&quot;🤔</div>2020-03-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/c9/92/6361802a.jpg" width="30px"><span>滴流乱转小胖儿</span> 👍（4） 💬（0）<div>老师好，开篇的某云场景叙述，好皮啊！优秀！</div>2020-03-12</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTIlRVTQ1mpTLY34BAje4xRY0PFSJk6J1su2jicrtEQASP3DakQ7lQkWZNADoh8mLibwATLJB9EMrIVQ/132" width="30px"><span>Z</span> 👍（1） 💬（1）<div>老师你好，看了些MySQL相关书和文章，总结的主从更新数据时序好像不太一样
MySQL主从两个数据库更新数据时序：
1、记录undo log，然后修改引擎中的数据页
2、二阶段提交redo log+bin log
3、二阶段提交后数据持久化完成，事务可认为成功，此时可以同步bin log到从库
4、释放锁、mvcc等等东西，然后给客户端返回成功相应
相关文章：https:&#47;&#47;blog.51cto.com&#47;wangwei007&#47;2323844</div>2020-12-30</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/20/dd/82d8eff2.jpg" width="30px"><span>Mine</span> 👍（1） 💬（1）<div>老师，感觉binlog已经记录了所有的数据呀，为啥还需要定期的全量备份呢，直接拿binlog进行数据恢复就可以了啊，还是我对binlog理解错了🤔</div>2020-12-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/45/4f/f94caf47.jpg" width="30px"><span>qbit</span> 👍（1） 💬（1）<div>SHOW VARIABLES LIKE &#39;%log_bin%&#39;;
---
&quot;log_bin&quot;  &quot;OFF&quot;
&quot;log_bin_basename&quot;  &quot;&quot;
&quot;log_bin_index&quot;  &quot;&quot;
&quot;log_bin_trust_function_creators&quot;  &quot;OFF&quot;
&quot;sql_log_bin&quot;  &quot;ON&quot;
---
请问 sql_log_bin 和 log_bin 有什么区别和联系？</div>2020-03-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/26/eb/d7/90391376.jpg" width="30px"><span>ifelse</span> 👍（0） 💬（0）<div>特别要注意的是，让备份数据尽量地远离数据库。--记下来</div>2022-12-06</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/26/eb/d7/90391376.jpg" width="30px"><span>ifelse</span> 👍（0） 💬（0）<div>学习打卡</div>2022-12-06</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/ca/07/22dd76bf.jpg" width="30px"><span>kobe</span> 👍（0） 💬（0）<div>有个问题想咨询下，主备和主从是不同的概念吧？备机应该是只做备份，在主机正常时并不提供服务，而主从的从机会分担读请求的流量。是这样吧？</div>2022-07-14</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/sFkJYPdIIjHfxgCxAh1D4Pyk1jAueicu7egY1PUvR8egs12gAXxmO51YT6Bk7NianYRyMRPTpd3kKWXvZ8TEkRyw/132" width="30px"><span>Geek_7794e2</span> 👍（0） 💬（0）<div>这个专栏，竟然这么少人看，我觉得很不错</div>2022-07-03</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/DYAIOgq83er4rbCWDxib3FHibYBouTwZqZBH6h5IgvjibEiaBv4Ceekib9SYg0peBBlFGu8hDuGvwjKp6LNznvEAibYw/132" width="30px"><span>DonaldTrumpppppppppp</span> 👍（0） 💬（0）<div>Ha半同步模式可以保证一致性，这种模式能否介绍下？</div>2022-03-06</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/4b/6c/f09b085d.jpg" width="30px"><span>青峰</span> 👍（0） 💬（0）<div>老师, 那主库的binlog不也可以恢复吗, 如果能删除主库的人员, 意味着从库也有权限的吧, 除非人员备份, 权限分割咯</div>2021-07-05</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/8c/5c/3f164f66.jpg" width="30px"><span>亚林</span> 👍（0） 💬（0）<div>老师这节后面的内容就是CAP原则</div>2020-10-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/f1/96/9571fa3d.jpg" width="30px"><span>青青子衿</span> 👍（0） 💬（0）<div>老师，这篇讲的特别好</div>2020-06-03</li><br/>
</ul>