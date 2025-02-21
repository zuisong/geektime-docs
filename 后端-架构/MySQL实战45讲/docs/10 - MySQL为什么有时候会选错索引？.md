前面我们介绍过索引，你已经知道了在MySQL中一张表其实是可以支持多个索引的。但是，你写SQL语句的时候，并没有主动指定使用哪个索引。也就是说，使用哪个索引是由MySQL来确定的。

不知道你有没有碰到过这种情况，一条本来可以执行得很快的语句，却由于MySQL选错了索引，而导致执行速度变得很慢？

我们一起来看一个例子吧。

我们先建一个简单的表，表里有a、b两个字段，并分别建上索引：

```
CREATE TABLE `t` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `a` int(11) DEFAULT NULL,
  `b` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `a` (`a`),
  KEY `b` (`b`)
) ENGINE=InnoDB;
```

然后，我们往表t中插入10万行记录，取值按整数递增，即：(1,1,1)，(2,2,2)，(3,3,3) 直到(100000,100000,100000)。

我是用存储过程来插入数据的，这里我贴出来方便你复现：

```
delimiter ;;
create procedure idata()
begin
  declare i int;
  set i=1;
  while(i<=100000)do
    insert into t values(i, i, i);
    set i=i+1;
  end while;
end;;
delimiter ;
call idata();
```

接下来，我们分析一条SQL语句：

```
mysql> select * from t where a between 10000 and 20000;
```

你一定会说，这个语句还用分析吗，很简单呀，a上有索引，肯定是要使用索引a的。

你说得没错，图1显示的就是使用explain命令看到的这条语句的执行情况。

![](https://static001.geekbang.org/resource/image/2c/e3/2cfce769551c6eac9bfbee0563d48fe3.png?wh=1743%2A159)

图1 使用explain命令查看语句执行情况

从图1看上去，这条查询语句的执行也确实符合预期，key这个字段值是’a’，表示优化器选择了索引a。

不过别急，这个案例不会这么简单。在我们已经准备好的包含了10万行数据的表上，我们再做如下操作。
<div><strong>精选留言（30）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/14/16/31/ae8adf82.jpg" width="30px"><span>路过</span> 👍（37） 💬（7）<div>老师，关于本章中的“基数”（cardinality）问题。既然已经为列a创建了索引，即有专门的数据页存放索引。遍历索引是很快的，从而得到“基数”的值应该很快呀。为何要到原始的数据页中，找N页，统计上面不同的值呢？有点多此一举啊。如果这样操作，会导致信息不准确，比如本来一个页中有50条数据，后来其中20条数据被删除了，空间没有被释放，这导致统计的信息就发生偏差。基数信息就更不准确了。
从原始页中计算“基数”，是不是考虑到索引页中的数据具有滞后性，即更新了表中数据，要过一会才更新索引页？
请老师指正，谢谢！

</div>2018-12-05</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/f8/70/f3a33a14.jpg" width="30px"><span>某、人</span> 👍（74） 💬（3）<div>今天这个问题不是特别明白为什么。session A开启了一致性读,session B delete或者insert,之前记录都已经放进了undo了。二级索引的记录也写进了redo和change buffer,应该说删除了索引页也不影响session A的重复读。估计是开启了一致性读之后,在这个事务执行期间,不能释放空间,导致统计信息变大。还是需要老师解释下具体的细节

今天有两个问题,想请教下老师
1.我的理解是由于B是查找(50000,100000),由于B+树有序,通过二分查找找到b=50000的值,从50000往右扫描,一条一条回表查数据,在执行器上做where a(1,1000)的筛选,然后做判断是否够不够limit的数,够就结束循环。由于这里b(50000,100000)必然不存在a(1,1000),所以需要扫描5W行左右.但是如果把a改为(50001,51000),扫描行数没有变。那么是因为优化器给的扫描行数有问题还是执行器没有结束循环？为什么不结束循环?
(好像rows能直观展示limit起作用,必须在执行器上过滤数据,不能在索引上过滤数据,不知道为什么这样设计)

2.假设b上数据是会有很多重复的数据,b的最大值也存在多行重复
select * from t where (a between 1 and 1000) and (b between 50000 and 100000) order by b desc limit 1;
这里倒序去扫描b索引树,选取的是b值最大,id值为一个固定值(既不最大也不最小)
select * from t force index(a) where (a between 1 and 1000) and (b between 50000 and 100000) order by b desc limit 1;
由于这里选取的是a索引,排序不能用到索引,只能用优化排序.选取的是b值最大,id值最小那一行
这就是典型的两条相同的sql,但是索引选择的不同,出现的数据不一致。
所以如果是order by b,a就可以避免这种情况的引起的不一致,也可以避免堆排序造成的不一致
但是如果是asc没有出现这种情况。这里出现不一致,应该还不是由于堆排序造成的。这是什么原因造成的？</div>2018-12-05</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTI9q8ic0ISibeVvhBoTiaJmniamkg6MbVibTHN6lxCLLNJcibv7v04vABnWGwk3daWgh5DBzvbGlrpSqNMA/132" width="30px"><span>bowenz</span> 👍（15） 💬（7）<div>在5.7.21 percona 版本实验，未出现案例1的情况 。 
dev02&gt; select @@global.tx_isolation,@@tx_isolation,version(),&quot;session A&quot;;
+-----------------------+-----------------+---------------+-----------+
| @@global.tx_isolation | @@tx_isolation  | version()     | session A |
+-----------------------+-----------------+---------------+-----------+
| REPEATABLE-READ       | REPEATABLE-READ | 5.7.21-20-log | session A |
+-----------------------+-----------------+---------------+-----------+
dev02&gt; start transaction with consistent snapshot;
Query OK, 0 rows affected (0.00 sec)
dev02&gt; commit;
Query OK, 0 rows affected (0.00 sec)
dev02&gt; select now() ;
+---------------------+
| now()               |
+---------------------+
| 2018-12-04 22:03:48 |
+---------------------+
1 row in set (0.00 sec)
dev02&gt; select @@global.tx_isolation,@@tx_isolation,version(),&quot;session B&quot;;
+-----------------------+-----------------+---------------+-----------+
| @@global.tx_isolation | @@tx_isolation  | version()     | session B |
+-----------------------+-----------------+---------------+-----------+
| REPEATABLE-READ       | REPEATABLE-READ | 5.7.21-20-log | session B |
+-----------------------+-----------------+---------------+-----------+
1 row in set, 2 warnings (0.00 sec)

dev02&gt; delete from t;
Query OK, 100000 rows affected (0.51 sec)

dev02&gt; call idata();
Query OK, 1 row affected (2 min 38.34 sec)

dev02&gt; select now();
+---------------------+
| now()               |
+---------------------+
| 2018-12-04 22:03:58 |
+---------------------+
1 row in set (0.00 sec)

dev02&gt; explain select * from t where a between 10000 and 20000;
| id | select_type | table | partitions | type  | possible_keys | key  | key_len | ref  | rows  | filtered | Extra                 |
|  1 | SIMPLE      | t     | NULL       | range | a             | a    | 5       | NULL | 10001 |   100.00 | Using index condition |</div>2018-12-05</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/f8/70/f3a33a14.jpg" width="30px"><span>某、人</span> 👍（369） 💬（21）<div>趁着答案公布之前的最后时间,再来尝试性答一下这个题
1.为什么没有session A,session B扫描的行数是1W
由于mysql是使用标记删除来删除记录的,并不从索引和数据文件中真正的删除。
如果delete和insert中间的间隔相对较小,purge线程还没有来得及清理该记录。
如果主键相同的情况下,新插入的insert会沿用之前删除的delete的记录的空间。
由于相同的数据量以及表大小,所以导致了统计信息没有变化
2.为什么开启了session A,session B扫描行数变成3W
由于session A开启了一致性读,目的为了保证session A的可重复读,insert只能
另起炉灶,不能占用delete的空间。所以出现的情况就是delete虽然删除了,但是
未释放空间,insert又增加了空间。导致统计信息有误</div>2018-12-06</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/f3/4a/4874b350.jpg" width="30px"><span>Ying</span> 👍（71） 💬（13）<div>现学现用 今天有个500万的表 分页查询特别慢。
select * from table where create_time and create_time&gt;=时间戳 and  create_time&lt;=时间戳 
and subtype=&#39;xx&#39; and type=&#39;xx&#39; and company_id =x order by create_time limited 90,30 ;
已经建立了组合索引 union_index包括字段 create_time subtype  type company_id
但是 explain 发现竟然走了create_time 的索引
语句里加了一个use index(union_index) ，立马好了
真正的解决了客户的实际问题啊。 感谢老师</div>2018-12-05</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/5c/c5/1231d633.jpg" width="30px"><span>梁中华</span> 👍（52） 💬（17）<div>假如要查 A in () AND B in (), 怎么建索引?</div>2019-02-01</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/ea/9a/02d589f9.jpg" width="30px"><span>斜面镜子 Bill</span> 👍（51） 💬（4）<div>问题的思考：
我理解 session A 开启的事务对 session B的delete操作后的索引数据的统计时效产生了影响，因为需要保证事务A的重复读，在数据页没有实际删除，而索引的统计选择了N个数据页，这部分数据页不收到前台事务的影响，所以整体统计值会变大，直接影响了索引选择的准确性；</div>2018-12-05</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/9b/a8/6a391c66.jpg" width="30px"><span>geraltlaush</span> 👍（43） 💬（12）<div>公司测试机器IO性能太差，插十万条要27分钟，做这个文章的实验要1个小时以上</div>2018-12-05</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/fd/d5/0194ea41.jpg" width="30px"><span>沉浮</span> 👍（37） 💬（1）<div>图十下面第二段
现在 limit b,a 这种写法，要求按照 b,a 排序，就意味着使用这两个索引都需要排序。
应该是order by b,a吧
另外有个问题请教林老师，根据经验大表增加索引的时候比较慢，这个是理解的，但是删除索引的时候能做到秒删，这个什么原理呢？</div>2018-12-05</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/71/97/f1a3d398.jpg" width="30px"><span>张永志</span> 👍（33） 💬（10）<div>merge那段的解释明白了change buffer操作逻辑。即change buffer变化与数据块变化是分开的，最初redo中记录的只是change buffer的变更，因为还未应用到数据块上。而merge后redo记录的是数据块、change buffer的变更。
是这样吧？😄</div>2018-12-05</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/77/fd/c6619535.jpg" width="30px"><span>XD</span> 👍（32） 💬（1）<div>谢谢老师的解答，我之前一直以为这个操作也是在存储层进行的。
那执行器调用存储层的接口是不是只能获取到最原始的数据，后续的加工，比如order，join和group操作也都是在执行器里进行的吗？对应的buffer和内存临时表也都是server层的东西？</div>2019-02-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/80/45/24c30321.jpg" width="30px"><span>kevin</span> 👍（21） 💬（1）<div>老师你好。我用存储过程插入100000条数据特别慢，后来我set autocommit=0,每1000条才commit，这样就快了。我想不出来这是为什么，求解惑</div>2018-12-05</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/07/8c/0d886dcc.jpg" width="30px"><span>蚂蚁内推+v</span> 👍（19） 💬（4）<div>老师，原文中：在这个例子里，我们用 limit 100 让优化器意识到，使用b索引代价是很高的。
问题：为什么limit 100时候，使用b索引代价高呢？和limit 1相比，赶紧没有什么质的变化啊</div>2018-12-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/e3/bc/064401c7.jpg" width="30px"><span>EAGLE</span> 👍（19） 💬（3）<div>老师，看了一篇文章说innodb如果不加order by默认是按照主键排序的。也就是说如果不加order by，查询结果也是有一定次序的。那么如果没有业务需求，纯粹只是为了分页显示数据，不加order by也是可以的吗？</div>2018-12-06</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/78/31/c7f8d1db.jpg" width="30px"><span>Laputa</span> 👍（17） 💬（3）<div>老师，redo log 是实时写入磁盘的吗？是不是还有一层所谓的“redo log buffer”？</div>2018-12-05</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/51/93/ed274018.jpg" width="30px"><span>kuzicala</span> 👍（10） 💬（1）<div>请教一个疑问：
  存储引擎在找到一行合格的数据后 是先返回在继续查 还是一口气查完在一次性返回？ 
我的理解是查到一行就返回 不知对否？</div>2019-02-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/40/5e/b8fada94.jpg" width="30px"><span>Ryoma</span> 👍（10） 💬（2）<div>请问使用insert ... on duplicate key update对性能有什么影响呢</div>2018-12-05</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/02/33/b4bb0b9c.jpg" width="30px"><span>仲玄</span> 👍（9） 💬（2）<div>老师你好 , 我看你说数据写到redo log上,所以主机异常重启不会丢失, 但是redo log包括两部分：一是内存中的日志缓冲(redo log buffer)，该部分日志是易失性的；二是磁盘上的重做日志文件(redo log file)，该部分日志是持久的。 如果数据是在redo log buffer上的,是会丢失的吧?</div>2019-01-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/e1/09/9483f537.jpg" width="30px"><span>☞</span> 👍（7） 💬（1）<div>老师anlyze table或者optimize table都是会锁表的吧，线上可以直接执行吗？</div>2018-12-05</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/3a/46/9fd9bd26.jpg" width="30px"><span>kyq叶鑫</span> 👍（5） 💬（3）<div>老师您好：我反复读了几遍文章还是无法理解为什么这个语句：select * from  (select * from t where (a between 1 and 1000)  and (b between 50000 and 100000) order by b limit 100)alias limit 1可以诱导优化器选择正确的索引。。。求解惑。</div>2019-01-31</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/pc41FOKAiabVaaKiawibEm7zglvnsYBnYeRiaSAElf9ciczovXmXmI0hOeR6U9RULFtMoqX5kobNttvwXCLsUM9Hbcg/132" width="30px"><span>monkay</span> 👍（4） 💬（4）<div>merge的第三部写redo log，不是前面的更新语句已经写了redo log了吗？为什么merge时又写一次？</div>2018-12-05</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/80/d6/1f78bc57.jpg" width="30px"><span>萧若愚</span> 👍（4） 💬（1）<div>请教个问题，如果一个表的字段名中包含表情符号比如 a😇，查询表的结果中字段名变为a？，该表的字符集已设为 utf8_mb4。查看 information_schema 表中字段名也是a？，发现 information_schema 表的默认字符集是 utf8。查询时若条件语句中用到该字段名时，用`a?`，`a😇`，以及 a😇 都可正确查询到结果，这是为什么？还有，如何查询出正确的字段名，即查询结果中为 a😇 而不是 a?。谢谢！</div>2018-12-05</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/ba/ac/b44b256a.jpg" width="30px"><span>纸片人</span> 👍（3） 💬（1）<div>林老师，我就本章的第一示例，做了四组实验，发现您的说法存在问题。以下是我的实验过程，请指正！
第一组实验，mysql版本5.7.18，严格按照本章叙述步骤进行。复现失败，explain结果显示，mysql选择了索引a。
第二组实验，mysql版本5.6.24，同样的步骤，复现失败。同时我注意到，在第二次调用call idata()前，在会话A（即读事务所在会话）中explain目标select语句，返回的索引类型和长度都为NULL，预测扫描长度为1。此时，由于当前隔离级别为RR，读事务看到的数据都被会话B删除了，所以其视图来自undo日志。如果explain统计扫描行数会将undo log里的数据行统计在内的话，explain的rows不可能等于1。所以“因为undo log里的数据不能实际删除，导致explain... force index(a)...的扫描行数出现误差”的说法是错误的！！！
第三组实验，尝试将idb放入系统表空间。我想看看如果数据行和undo log放在一起，是否会改变现状。实验结果表明，mysql还是选择了索引a。
第四组实验，将id改成自增主键（灵感来自第11章您给@某、人的回复），成功复现示例结果！！explain... force index(a)...的rows为37136，和文章里的数值相差无几。

结论：
1、mysql的优化器评估select查询代价，读取的是表格和索引的元数据，所以explain结果不会因为事务不同被隔离。
2、explain不会将undo log上的数据计算在内，即undo上的数据不会影响explain的估算结果。
3、基数不是导致rows出现误差的根本原因——我其中有一组实验所有步骤完成后，三个索引的基数都为100141。
4、explain会把已经打上“删除”标记的行也考虑进去，这可能是rows出现误差的真正原因。</div>2019-04-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/93/8a/abb7bfe3.jpg" width="30px"><span>亮</span> 👍（3） 💬（1）<div>老师，您好，analyze table 语句会锁表吗</div>2019-01-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/2c/a9/cc/1183d71f.jpg" width="30px"><span>无</span> 👍（2） 💬（3）<div>force不是强制的？我用force指定index，explain后还是全表扫描</div>2024-01-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/20/3a/90db6a24.jpg" width="30px"><span>Long</span> 👍（2） 💬（1）<div>老师好，1. 能不能再说下关联的free data的统计，就是information_schema.tables里面的信息，优化器读取的行数信息应该是来自于这个表的吧？2. 还有修正统计信息可以用analyze table，optimize table，如果是innodb的还可以set engine = innodb来解决.这三者时候有什么大的算法上的区别？   3 有没有案例说自己的应用程序设计的时候应该注意什么，就好比说一个经常新增和删除的表应该注意什么，来减少free data的大小？希望老师能够解答一下，多谢</div>2018-12-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/33/af/dda311cf.jpg" width="30px"><span>TiTi</span> 👍（2） 💬（1）<div>看了老师对于上一期思考题的解答，“虽然是只更新内存，但是在事务提交的时候，我们把 change buffer的操作也记录到 redo log 里了，所以崩溃恢复的时候，change buffer也能够找回来 ”，难道记录redo log是在更新change buffer内存内容之前就做好的吗？照您的说法，事务提交也是在更新内存之前，从而保证写内存时断电，change buffer的内容依然保存在redo log里？有点颠覆我的三观啊</div>2018-12-06</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/NhbRicjvf8v3K6D3v1FtOicxOciaPZQsCjCmuGCqea4vJeRVaLicKLpAcFQlcTgLvczBWY7SYDkeOtibxXj1PGl7Nug/132" width="30px"><span>柚子</span> 👍（2） 💬（1）<div>我以前遇到过一次，字段a类型是int，where a=‘1’,条件值是字符串类型，最后发现没有用到索引，改成数值1就用到了，只在那一台机子复现了，请问这是mysql有这样设计么，是有配置控制的么</div>2018-12-05</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/e9/29/629d9bb0.jpg" width="30px"><span>天王</span> 👍（2） 💬（1）<div>请教几个问题  1 索引的基数＝页面不同值的平均值数量*索引的页面数，什么是索引的页面数，索引是在页面上连续保存的？2 一个表有多个索引的情况，where条件里面有多个索引列的条件，每次都只能走一个索引吗，能都优化让走多个索引吗，不能同时走多个索引的原因是什么？</div>2018-12-05</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/1hp9kzzuLUVHzmmddIPIO2OgUWr1ibJRr8cMoB7K0fwx8Vmn34L8yN2NoYUtgNicfPGaXKF02pQ2huXd59r2I0kw/132" width="30px"><span>三胖</span> 👍（1） 💬（1）<div>老师，我是windows上面实践的，用navicat开两个窗口进行复现，但是没有复现成功。是因为两个窗口其实都算一个ssesion吗</div>2019-02-25</li><br/>
</ul>