在开发系统的时候，你可能经常需要计算一个表的行数，比如一个交易系统的所有变更记录总数。这时候你可能会想，一条select count(\*) from t 语句不就解决了吗？

但是，你会发现随着系统中记录数越来越多，这条语句执行得也会越来越慢。然后你可能就想了，MySQL怎么这么笨啊，记个总数，每次要查的时候直接读出来，不就好了吗。

那么今天，我们就来聊聊count(\*)语句到底是怎样实现的，以及MySQL为什么会这么实现。然后，我会再和你说说，如果应用中有这种频繁变更并需要统计表行数的需求，业务设计上可以怎么做。

# count(\*)的实现方式

你首先要明确的是，在不同的MySQL引擎中，count(\*)有不同的实现方式。

- MyISAM引擎把一个表的总行数存在了磁盘上，因此执行count(\*)的时候会直接返回这个数，效率很高；
- 而InnoDB引擎就麻烦了，它执行count(\*)的时候，需要把数据一行一行地从引擎里面读出来，然后累积计数。

这里需要注意的是，我们在这篇文章里讨论的是没有过滤条件的count(\*)，如果加了where 条件的话，MyISAM表也是不能返回得这么快的。

在前面的文章中，我们一起分析了为什么要使用InnoDB，因为不论是在事务支持、并发能力还是在数据安全方面，InnoDB都优于MyISAM。我猜你的表也一定是用了InnoDB引擎。这就是当你的记录数越来越多的时候，计算一个表的总行数会越来越慢的原因。
<div><strong>精选留言（30）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/13/36/d2/c7357723.jpg" width="30px"><span>发条橙子 。</span> 👍（26） 💬（15）<div>老师 ，我这边有几个问题  ：

1. 看到老师回复评论说 count(id) 也是走普通索引 ，那是不是也算是优化了 ， 我以为 count(字段) 是走的聚集索引 。老师的意思是 count(字段) 是走二级索引，但是不一定是数据最少的索引树的意思是么 

2. count(*) 的话， innodb 还会有取数判空这样的判断逻辑么 ，还是直接取行数 +1 了 ， 还是按所取索引类型分情况。 允许为 null 的索引是不是行数比较少， 取的总数会不会有问题呢

3.  我这边试了一下 ， 库里总共 30w 数据 。 第一次用 count(*) 是 120多ms , 第二次就是 60多 ms 。 第三次用了 count(1) ，也是60多ms 。 请问 count(*) 这两次的前后时间差是什么原因，也会走缓存 ？

4. 另一个问题是一个题外话 ，我看老师的例子事务级别应该都是 rr 。 我偶然看到我们公司事务隔离级别是  rc 。 我比较惊讶，就去问 DBA 为什么是 rc 而不是默认的 rr 。 她说一般都是用的 rc  ，我想问现在公司一般都是 rc 么， 请问老师现在用的隔离级别是什么 ？？ 在我的印象里 ，rr 保证事务的隔离性会更好一些吧 。 我google 了一下， rc 会不会在某些场景下出现一些问题，但是没有查出来相关结果。老师能不能讲解一下，rc 的话会在哪些场景下会踩坑么 。 （我之前码代码都是按照 rr 级别下的思维码的代码）</div>2018-12-15</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTIiatbibYU9p7aVpq1o47X83VbJtsnP9Dkribian9bArLleibUVMDfD9S0JF9uZzfjo6AX5eR6asTiaYkvA/132" width="30px"><span>倪大人</span> 👍（74） 💬（16）<div>看到有同学说会话A是幻读，其实图一的会话B才是幻读吧？</div>2018-12-15</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/76/93/c78a132a.jpg" width="30px"><span>果然如此</span> 👍（28） 💬（15）<div>一、请问计数用这个MySQL+redis方案如何：
1.开启事务（程序中的事务）
2.MySQL插入数据
3.原子更新redis计数
4.如果redis更新成功提交事务，如果redis更新失败回滚事务。

二、.net和java程序代码的事务和MySQL事务是什么关系，有什么相关性？</div>2018-12-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/61/57/6f3c81dd.jpg" width="30px"><span>包包up</span> 👍（695） 💬（18）<div>从并发系统性能的角度考虑，应该先插入操作记录，再更新计数表。

知识点在《行锁功过：怎么减少行锁对性能的影响？》
因为更新计数表涉及到行锁的竞争，先插入再更新能最大程度地减少了事务之间的锁等待，提升了并发度。</div>2018-12-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/d4/f3/129d6dfe.jpg" width="30px"><span>李二木</span> 👍（116） 💬（17）<div>一直以为带*查询效率是最差的，平时查询特意加了 count(ID) 查询。罪过啊。</div>2018-12-15</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/62/c4/98a9e594.jpg" width="30px"><span>菜鸡一只</span> 👍（93） 💬（11）<div>count（id）和count（这段）都是要把每一行的该字段值取出来，然后判断是否为空，那为什么count（id）的效率要高？</div>2019-02-01</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/f8/70/f3a33a14.jpg" width="30px"><span>某、人</span> 👍（28） 💬（9）<div>老师我先问个本章之外的问题:
1.rr模式下,一张表上没有主键和唯一键,有二级索引c.如果是一张大表,删除一条数据delete t where c=1.
在主库上利用二级索引,在根据虚拟的主键列回表删除还挺快.但是在备库上回放特别慢,而且状态是system lock,是因为binlog event里没有包含虚拟主键列.导致在备库回放的时候,必须全表扫描,耗时特别久?还是其他原因

2.回放过程中,在备库delete一条语句是被阻塞的,insert又是可以的,说明只在记录上的X锁没有gap锁。
但是如果在主库session A begin,delete where c=1.在开启一个session B,在主库上操作也是delete阻塞,insert正常.不过等session A执行完成,不提交.insert都阻塞了,说明最后上了gap锁。有点没明白这儿的上锁逻辑是什么？

3.还有就是备库回放binlog,相对于主库的一条update语句流程来说,从库回放哪些流程是省略了的啊,
server层的应该都省略了,应该主要是引擎层的回放,这里有点模糊从库是怎么回放的binlog event?
因为第一个问题从库回放的时候,从库上的二级索引貌似没起作用,直接就在聚簇索引上做的更新。

感谢老师</div>2018-12-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/4d/70/7d736d5f.jpg" width="30px"><span>小动物很困</span> 👍（24） 💬（4）<div>我记得有一个并发插入的方法,就是说计数表对同一个表开很多行,然后计数增加对这些数据随机做加法,当做count操作的时候取sum,这样对行锁竞争会削弱.</div>2019-01-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/de/bc/1245cd12.jpg" width="30px"><span>不忘初心</span> 👍（18） 💬（1）<div>对于 count(主键 id) ，server层拿到ID，判断ID是不可能为空的按行累加。这个地方，是不是又点问题，既然是主键ID，是一定不会为空的，这个server层还需要判断不为空吗</div>2018-12-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/cb/f8/f4adadcb.jpg" width="30px"><span>陈天境</span> 👍（11） 💬（6）<div>碰到大部分情形都是带条件查询的count,，这个怎么解？</div>2018-12-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/ef/af/adce8c49.jpg" width="30px"><span>wljs</span> 👍（9） 💬（1）<div>为何没说在information_schema.tables也可以查看表记录数。</div>2018-12-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/77/fd/c6619535.jpg" width="30px"><span>XD</span> 👍（6） 💬（3）<div>对于 count(1) 来说，InnoDB 引擎遍历整张表，但不取值。

老师，有点好奇innodb不取值的话，返回给执行器的数据是啥？我猜是一个类似endOfLine的标识？
那如果返回数据带值的话，这个数据格式怎么样的呢？类似json的kv对，还是类似excel的先有一行表头，后面跟着数据呢？

我本来觉得更像后者，这样在做count(1)和count(id)的时候只开头多一次表头判断就好了。但是看文章中的描述好像是每一行都要判断一次？那似乎更像是kv了。</div>2019-03-03</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/e8/45/c58cb283.jpg" width="30px"><span>帆帆帆帆帆帆帆帆</span> 👍（6） 💬（1）<div>如果字段上有索引，且字段非空，count(字段)的效率就不是最差的了吧。</div>2018-12-14</li><br/><li><img src="" width="30px"><span>Ivy</span> 👍（5） 💬（2）<div>老师，你好，
如果这个“字段”是定义为 not null 的话，一行行地从记录里面读出这个字段，判断不能为 null，按行累加；
这段话没读懂，既然已经知道not null为何还要再次判断不能为 null？直接读出来累加不就可以了吗？另外是否我对引擎层面的数据读取有误解，是否说无论使用哪种 count 方式，引擎都一定要逐行去读只是在是否使用索引和是否返回给server层具体数据的区别？</div>2019-01-04</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTLE4LYb3jrH63ZV98Zpc8DompwDgb1O3nffMoZCmiaibauRyEFv6NDNsST9RWxZExvMLMWb50zaanoQ/132" width="30px"><span>慧鑫coming</span> 👍（5） 💬（1）<div>晓斌老师，图4中会话B会等待会话A提交后再执行吧？A中拿了count的写锁，我分析的对吧？</div>2018-12-14</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTIyn6s0CNx9F9Uu4nia6z7ZldUo8XdXEF4ia4ojfTRCvMT8IZgjRcpFulYqZjq4IvtrE5yYfzpgzMWA/132" width="30px"><span>Ruian</span> 👍（4） 💬（2）<div>老师，我有一个问题请教下您。我的mysql数据库 有一张表project_des (850万数据) count(1) 只要0.05s   和从表project（6500条数据）关联后需要15s       查看执行计划发现都走索引了。不知道为啥这么慢？
查询语句 select count(1) from project_des a,project b where a.project_id=b.id 我换exists 和in 也这么慢</div>2018-12-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/d6/c3/09a4b5eb.jpg" width="30px"><span>po</span> 👍（3） 💬（1）<div>老师你说Myisam引擎的总行数是写在磁盘上的，但是如果更新了数据，这个总行数的值是会时事改变，还是他有什么其他的策略。</div>2019-01-24</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTIu1n1DhUGGKTjelrQaLYOSVK2rsFeia0G8ASTIftib5PTOx4pTqdnfwb0NiaEFGRgS661nINyZx9sUg/132" width="30px"><span>Zzz</span> 👍（3） 💬（3）<div>老师，对于自增主键，批量插入是否会存在阻塞的情况？</div>2019-01-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/32/0b/981b4e93.jpg" width="30px"><span>念你如昔</span> 👍（2） 💬（3）<div>老师，我这边explain 看 select count(primary_id) count(1) count(*) 都是遍历的最小索引树，没有遍历全表的情况。是不是count(1) 和count(*) 虽遍历最小索引树，但是并没有扫描树里的数据，而count（id）扫描了树里的数据，所以比他俩慢？关于这个谁快谁慢的问题，真的是众说纷纭，，，</div>2019-03-05</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/1a/66/2d9db9ed.jpg" width="30px"><span>苦行僧</span> 👍（2） 💬（1）<div>二话不说 先把代码中count改成count(* ）</div>2019-01-30</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/ad/27/5556ae50.jpg" width="30px"><span>Demter</span> 👍（1） 💬（3）<div>count(1)虽然不取值，到时要返回整行数据，，这样返回的数据量大啊，对性能没影响吗??</div>2019-03-04</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/f5/7f/81b3f5ec.jpg" width="30px"><span>胡小珊</span> 👍（1） 💬（1）<div>如果是多表关联并有很多where条件查询，此时count虽然走了索引，但还是特别慢，具体业务是页面查询条件与显示需要关联这些表，并做条件查询</div>2019-02-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/08/75/512b9f26.jpg" width="30px"><span>张汉桂-东莞</span> 👍（1） 💬（1）<div>我觉得应该先插入再更新计数表。因为先有记录，再有统计数。这样做逻辑上更合理</div>2019-01-26</li><br/><li><img src="" width="30px"><span>Ivy</span> 👍（1） 💬（1）<div>老师，文章中反复强调不取值，这是什么概念呢？引擎不取值server怎么拿到数据又怎么计数呢？能不能大概解释一下引擎读取数据返回给server的过程呀？</div>2019-01-04</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/9c/9c/e02a0daf.jpg" width="30px"><span>运斤成风</span> 👍（1） 💬（3）<div>老师好，Count（字段），若字段是二级索引，又添加了非空约束。这样的话应该是遍历小树（仅遍历二级索引就能取得正确记数），遍历的叶子结点要比主键的全遍少很多。应该效率比主键快吧？谢谢</div>2018-12-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/c7/a1/273bff58.jpg" width="30px"><span>可凡不凡</span> 👍（1） 💬（1）<div>老师 count() 不管有没有索引 一定会走全表扫描吗</div>2018-12-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/f7/7a/55618020.jpg" width="30px"><span>马若飞</span> 👍（1） 💬（1）<div>对于infobright这种列式存储的引擎，是不是就不能用*了</div>2018-12-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/8d/46/fd0bd694.jpg" width="30px"><span>风中奇缘</span> 👍（1） 💬（1）<div>放到数据库里单独的一张计数表 C也不是一个好的方案，我这边当时有个需求是需要按照各种条件搜索来统计总个数的，计数表C估计罗列不完各种条件搜索。</div>2018-12-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/17/6a/c979163e.jpg" width="30px"><span>古娜拉黑暗之神·巴啦啦能量·堕落达</span> 👍（1） 💬（1）<div>老师，看了这节课之后，有两个疑问，望能解答一下：
第一：您在《08-事务到底是隔离的还是不隔离的？》中讲过，begin&#47;start transaction;并不是一个事务的起点，所以本节 图1 中的“begin;”是不是应该是“start transaction with consistent snapshot”这个命令？
第二：MySQL专门针对 count(*) 做了优化，那么这个优化是在哪个版本加入的呢？如果公司使用的是优化之前的版本，是不是还是 count(1) 效率最高？</div>2018-12-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/8a/fc/d1dd57dd.jpg" width="30px"><span>ipofss</span> 👍（0） 💬（1）<div>老师，我问一个题外话：对于一个MySQL的表结构的修改，需要重建主键索引吗？
我平时用Navicat，导出的sql语句，会自动带上drop主键索引，然后又add主键索引，然后结合你前面讲的，我认为对于新加的列，如果不重建索引，那么对于旧数据，主键索引树上的叶子节点，就不会有新加的列的数据，所以我认为应该是需要重建主键索引的。
我的理解对吗？</div>2020-02-26</li><br/>
</ul>