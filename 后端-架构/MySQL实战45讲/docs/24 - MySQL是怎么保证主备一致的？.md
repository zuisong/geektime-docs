在前面的文章中，我不止一次地和你提到了binlog，大家知道binlog可以用来归档，也可以用来做主备同步，但它的内容是什么样的呢？为什么备库执行了binlog就可以跟主库保持一致了呢？今天我就正式地和你介绍一下它。

毫不夸张地说，MySQL能够成为现下最流行的开源数据库，binlog功不可没。

在最开始，MySQL是以容易学习和方便的高可用架构，被开发人员青睐的。而它的几乎所有的高可用架构，都直接依赖于binlog。虽然这些高可用架构已经呈现出越来越复杂的趋势，但都是从最基本的一主一备演化过来的。

今天这篇文章我主要为你介绍主备的基本原理。理解了背后的设计原理，你也可以从业务开发的角度，来借鉴这些设计思想。

# MySQL主备的基本原理

如图1所示就是基本的主备切换流程。

![](https://static001.geekbang.org/resource/image/fd/10/fd75a2b37ae6ca709b7f16fe060c2c10.png?wh=1142%2A856)

图 1 MySQL主备切换流程

在状态1中，客户端的读写都直接访问节点A，而节点B是A的备库，只是将A的更新都同步过来，到本地执行。这样可以保持节点B和A的数据是相同的。

当需要切换的时候，就切成状态2。这时候客户端读写访问的都是节点B，而节点A是B的备库。

在状态1中，虽然节点B没有被直接访问，但是我依然建议你把节点B（也就是备库）设置成只读（readonly）模式。这样做，有以下几个考虑：
<div><strong>精选留言（30）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/12/9b/a8/6a391c66.jpg" width="30px"><span>geraltlaush</span> 👍（133） 💬（12）<div>老师，我想问下双M架构下，主从复制，是不是一方判断自己的数据比对方少就从对方复制，判断依据是什么</div>2019-01-25</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTJAibnPX9jW8kqLcIfibjic8GbkQkEUYyFKJkc39hZhibVlNrqwTjdLozkqibI2IwACd5YzofYickNxFnZg/132" width="30px"><span>Sinyo</span> 👍（191） 💬（4）<div>主库 A 从本地读取 binlog，发给从库 B；
老师，请问这里的本地是指文件系统的 page cache还是disk呢？</div>2019-01-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/16/73/c3aa4992.jpg" width="30px"><span>Joker</span> 👍（128） 💬（3）<div>老师您好，读到您关于binlog的文章之后，我有个疑问。
我之前理解是，mysql 每执行一条事务所产生的binlog准备写到 binlog file时，都会先判断当前文件写入这条binlog之后是否会超过设置的max_binlog_size值。 如果超过，则rotate 自动生成下个binlog flie 来记录这条binlog信息。
那如果 事务所有产生的binlog 大于  max_binlog_size 值呢？ 那不是永久地rotate吗？ mysql是如何处理的？
谢谢。</div>2019-03-06</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/84/49/47d48fd0.jpg" width="30px"><span>观弈道人</span> 👍（81） 💬（2）<div>老师你好，问个备份问题，假如周日23点做了备份，周二20点需要恢复数据，那么在用binlog恢复时，如何恰好定位到周日23点的binlog,谢谢。</div>2019-01-07</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/69/bc/c22bf219.jpg" width="30px"><span>妥妥</span> 👍（65） 💬（10）<div>老师，我想问下，如果一张表并没有主键，插入的一条数据和这张表原有的一条数据所有字段都是一样的，然后对插入的这条数据做恢复，会不会把原有的那条数据删除？不知道在没有主键的情况下binlog会不会也记录数据库为其生成的主键id</div>2019-02-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/11/18/8cee35f9.jpg" width="30px"><span>HuaMax</span> 👍（60） 💬（8）<div>课后题。如果在同步的过程中修改了server id，那用原server id 生成的log被两个M认为都不是自己的而被循环执行，不知这种情况会不会发生</div>2019-01-07</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/00/f0/08409e78.jpg" width="30px"><span>一大只😴</span> 👍（51） 💬（3）<div>死循环第二种情况：
双主，log_slave_updates=on，binlog_format=statement
配置文件里写成statement格式，然后两个master都重启
(从row格式改成statement试了几次没有成功,因为binlog中记录格式还是row)
测试：
表t (id ,c,d) 主键id，有一条数据(1,2,1);
M1执行 
     stop slave;
     update t set c=c+1 ;或 update t set c=c+1 where id=1;
     set global server_id=new_server_id；
     start slave；
然后就能看到c的值在不断变大，想停止就把server_id改回原来的就可以了。


</div>2019-01-07</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/ed/d2/e3ae7ddd.jpg" width="30px"><span>三木禾</span> 👍（45） 💬（4）<div>老师，双M可能会造成数据不一致的情况么? 比如，A  B同时更新同一条数据？</div>2019-03-31</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/41/27/3ff1a1d6.jpg" width="30px"><span>hua168</span> 👍（45） 💬（8）<div>大神，我前些天去面试，面试官问了一题:
mysql做主从，一段时间后发现从库在高峰期会发生一两条条数据丢失（不记得是查询行空白还是查询不到了），主从正常，怎么判断？
1.我问他是不是所以从库都是一样，他说不一样
2.我说低峰期重做新的从库观察，查看日志有没有报错？他好像不满意这个答案。

 二、他还问主库挂了怎么办？
1.  mysql主从+keepalived&#47;heartbeat
     有脑裂，还是有前面丢数据问题
2. 用MMM或HMA之类
3.用ZK之类

三、写的压力大怎么办？
我回答，分库，分表

感觉整天他都不怎么满意，果然没让我复试了，我郁闷呀，我就面试运维的，问数据这么详细。😂
大神，能说下我哪里有问题吗？现在我都想不明白😂</div>2019-01-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/f3/0c/b46fb155.jpg" width="30px"><span>汪炜</span> 👍（42） 💬（7）<div>老师，问个问题，希望能被回答：
mmysql不是双一设置的时候，破坏了二阶段提交，事务已提交，redo没有及时刷盘，binlog刷盘了，这种情况，mysql是怎么恢复的，这个事务到底算不算提交？</div>2019-01-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/4e/3a/86196508.jpg" width="30px"><span>linqw</span> 👍（30） 💬（5）<div>写下学习完这篇的总结和理解，老师有空帮忙看下哦
1、简单主备，一主多备，主进行更新操作，将生成binlog文件发送给备，但是比较好奇一点的是所有备向主拿binlog文件的时候，主都是一个线程进行将binlog文件依次发送给备么？两个库互为主备可以将一个负责数据的写入，生成binlog文件，另一个作为数据的同步，将其改变的binlog同步到自身，然后其他备再从其同步binlog，多master可以做到一台宕机，快速切换到另一台作为主，防止主库宕机对业务造成的影响，但是这样可能导致一定程度的同步延迟。
2、主备复制关系搭建完成，主有数据写入的时候，发送给备的应该不是整个binlog log文件吧，是每次写入的binlog event么？
3、在图 2 主备流程图对bg-thread-&gt;undolog(disk)-&gt;data(disk)不太理解，回滚段也是先记录到内存，再记录在磁盘么？undolog(disk)再到data(disk),看了下undo log的控制参数没有看到控制类似行为的，没想通？老师帮忙解答下哦
4、binlog的三种格式，statement,记录数据库原句，有可能导致，主备所选择的索引不一致，导致主备数据不一致。row，binlog log记录的是操作的字段值，根据binlog_row_image 的默认配置是 FULL包括操作行为的所有字段值，binlog_row_image 设置为 MINIMAL，则会记录必须的字段,一般设置为row，可以根据binlog文件做其他操作，比如在误删除一行数据时，可以做insert，恢复数据。
5、如果执行的是 update 语句的话，binlog 里面会记录修改前整行的数据和修改后的整行数据，在二级索引的普通索引，有个change buffer优化，防止频繁的将数据页读入进来，可以减少buffer pool的消耗，可以在读取数据时，再将其marge，或者后台线程marge，但是在binlog log设置row格式的，update时，需要记录更新前后的数据，那这样的话，chage buffer不是用不上了么？还是说设置成row格式的时候，change buffer会没生效？老师麻烦帮忙解答下哦，没想明白</div>2019-02-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/1d/7f/aabc1b66.jpg" width="30px"><span>hetiu</span> 👍（23） 💬（2）<div>老师，请教下双M模式是如何解决数据冲突的？</div>2019-01-07</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/9a/64/eea9aa33.jpg" width="30px"><span>陈扬鸿</span> 👍（22） 💬（3）<div>老师，我现在生产上用的是MySQL5.6的主从同步，主库用的是ssd硬盘，备库用的是机械硬盘，现在从库落后主库好几个小时，主库上数据的写入更新比较大，这个问题是由于两端硬件问题造成的吗？线上只有一个数据库，有什么好的同步加速方案吗？麻烦老师给我解答一下，谢谢！</div>2019-02-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/17/6a/c979163e.jpg" width="30px"><span>古娜拉黑暗之神·巴啦啦能量·堕落达</span> 👍（15） 💬（10）<div>老师，您好，问一个关于change buffer的问题。
对于insert语句来说，change buffer的优化主要在非唯一的二级索引上，因为主键是唯一索引，插入必须要判断是否存在。
那么对于update语句呢？如下（假设c有非唯一索引，id是主键，d没有索引）：
update t set d=2 where c=10;
原先以为：从索引c取出id之后，不会回表，也不会把修改行的数据读入内存，而是直接在change buffer中记录一下。但看了今天得内容之后又迷糊了，因为如果不把修改行的数据读入内存，它又怎么把旧数据写入binlog中呢？
所以我想问的就是，上面的sql语句会不会把修改行的内容也读进内存？如果读进内存，那读进内存的这一步难道就为了写binlog吗？如果不读进内存，那binlog中的旧数据又是怎么来的呢？还有delete语句也同理。</div>2019-01-07</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/f6/b0/837f5d36.jpg" width="30px"><span>Mackie .Weng</span> 👍（12） 💬（4）<div>老师，你的课真好， 你讲的都是生产实际用到的，点赞~
不过近期有点苦恼，要请教一下近期遇到的事

场景：
SSD硬盘，我们数据一天一备份，想通过昨天凌晨备份+binlog恢复到最新数据，导出的binlog为2G，然后发现导入binlog花费了4，5小时，看了下binlog日志里面有很多这种信息
# at 2492
#190108 17:08:38 server id 2  end_log_pos 2601 CRC32 0x8b0598ec         Query   thread_id=12277795      exec_time=0     error_code=0
SET TIMESTAMP=1546938518&#47;*!*&#47;;
BEGIN
&#47;*!*&#47;;
# at 2601
# at 2633
# at 2919
#190108 17:08:38 server id 2  end_log_pos 2950 CRC32 0x13806369         Xid = 1924155105
COMMIT&#47;*!*&#47;;

问题：
1、在导出binlog为2G而且看了下里面很多这种事务，这是什么东西，有什么用吗
2、这种事务在导出binlog的时候可以不记录吗，然后来提高恢复数据的速度？
3、如果这是正常的情况，有无推荐更好的数据恢复方案或者工具

感谢老师</div>2019-01-14</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/NhbRicjvf8v3K6D3v1FtOicxOciaPZQsCjCmuGCqea4vJeRVaLicKLpAcFQlcTgLvczBWY7SYDkeOtibxXj1PGl7Nug/132" width="30px"><span>柚子</span> 👍（12） 💬（3）<div>大佬您好，文中说现在越来越多的使用row方式的binlog，那么只能选择接受写入慢和占用空间大的弊端么？</div>2019-01-07</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/42/e9/e27c659d.jpg" width="30px"><span>守护.</span> 👍（12） 💬（2）<div>老师早，问一个和本次课题之外的问题.mysql 数据库，我如果开启多线程对多张表同时进行insert 操作. 每张表自增的主键id会不连续.这个问题怎么处理呢？</div>2019-01-07</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/9a/0a/6c74e932.jpg" width="30px"><span>光</span> 👍（10） 💬（2）<div>林老师今天遇到个问题就是主从同步延迟，查到主从状态中出现：Slave_SQL_Running_State: Waiting for Slave Workers to free pending events。不知道这个是否会引起延迟。查了些资料说得都不是很明白。老师是否可以简短解答下。以及这种延迟如何避免。</div>2019-01-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/33/46/256e5728.jpg" width="30px"><span>静远投基</span> 👍（10） 💬（12）<div>请教一下，生产环境能不能使用正常使用表连接？要注意哪些地方？DBA总是说不建议用，还催促我将使用了表连接的地方改造，但也说不出个所以然。目前在两个百万级数据的表中有用到内连接，并没有觉得有什么问题</div>2019-01-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/45/64/2b09a36b.jpg" width="30px"><span>风二中</span> 👍（9） 💬（2）<div>在主库执行这条 SQL 语句的时候，用的是索引 a；而在备库执行这条 SQL 语句的时候，却使用了索引 t_modified
老师，您好，这里索引选择不一样，是因为前面提到的mysql 会选错索引吗？这种情况应该发生比较少吧，这里应该都会选择索引a吧，还是说这里只是一个事例，还有更复杂的情况</div>2019-01-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/41/27/3ff1a1d6.jpg" width="30px"><span>hua168</span> 👍（7） 💬（7）<div>面试官说的是mysql做一主多从，读写分离，运行一段时间后，发现从库在业务高峰期不规律性出现从库丢失数据，而所有从库丢失的数据情况都不一样，在一个从库查询某条记录是空的（不记得是空白还是直接查不到，真的没数据了，并不是延迟了，主从没停，就是没写进从库），在另一个从库却能查到，有的在这个从库查到了，另一个从库查不到，因为运行了几个月客户反馈才发现此问题，不确定所有从库中哪个从库数据是没有丢失的，和主库一致，怎么办？
我回答:
1.在业务低峰期，锁库，重新做主从，但是如果一天不能同步完的话，白天主库还要解锁。不会搞了……
又不像mongoDB那样不用记录pos值😂
2.减少主库io压力试下，比如分库分表
3.查看日志之类……

二、mysql主库高可用
mysql主从+keepalived&#47;heatbeat
HMA&#47;MMM
ZK
是我看配置视频，老师简单讲了一下，我在网上搜的

三、主库写压力过大
只能通过分库，分表
也是我看linux运维培训视频老师说的</div>2019-01-08</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/DYAIOgq83erFY9H3mxyTpZ9gxAmdeKic565hicicDZmv7cjswd8hdernmxib0chdQrlDNKUZQ8AticQCgDdgVEmJNuA/132" width="30px"><span>牧鱼</span> 👍（7） 💬（1）<div>老师好，mixed是row和statement的优点整合折中方案，这应该是好多系统设计理念吧？那么问题一：mixed既然能判断是什么时候使用row，什么时候使用statement，那么为什么好多推荐都是使用row而且不是使用mixed呢？是因为mixed这种模式下的自动选择转换不准确可能会出现主从问题吗？问题二：当使用mixed模式情况下，mysql内部是怎么判断的呢？比如有limit语句就会选择记录row格式，有now()函数还是同样会记录statement格式，mysql只是简单的某些特定场景下会使用记录row格式吗？谢谢。</div>2019-01-07</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/00/f0/08409e78.jpg" width="30px"><span>一大只😴</span> 👍（7） 💬（1）<div>思考题：
双主
M1 server_id 1363306 log_slave_updates=on
M2 server_id 1163306 log_slave_updates=on
双主复制正常
触发死循环场景：
test库中有一个t表(id int,c int,d int)，t表没有主键
M1执行：
stop slave;
insert into t values (3,3,3);
set global server_id=1373306 ;  ##变更M1的server_id
start slave;
然后就能看到M1和M2，一直在不停的插入(3,3,3)

我目前测试出来这一种情况，可能还有其它的触发方式，望补充
感觉这个机制不完善就是只依赖server_id作为判断是否是自身执行的语句，而且server_id还是动态变量，如果是只读也许会好的多




</div>2019-01-07</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/09/98/b11c372b.jpg" width="30px"><span>鸠翱</span> 👍（6） 💬（1）<div>也就是说 statement格式是不能用来恢复数据的是嘛……</div>2019-01-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/57/6e/b6795c44.jpg" width="30px"><span>夜空中最亮的星</span> 👍（5） 💬（1）<div>这节课完全学懂了，开心😃</div>2019-01-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/57/6e/b6795c44.jpg" width="30px"><span>夜空中最亮的星</span> 👍（5） 💬（2）<div>级联复制，3个数据库，首尾相连，应会出现死循环</div>2019-01-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/20/0d/93967314.jpg" width="30px"><span>远方夕阳</span> 👍（4） 💬（1）<div>1你至少应该把 binlog 的格式设置为 mixed  
2虽然 mixed 格式的 binlog 现在已经用得不多了 
老师你好，这2句话出现在一起如何理解？</div>2019-07-25</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/DYAIOgq83eop9WylZJicLQxlvXukXUgPp39zJHyyReK5s1C9VhA6rric7GiarbfQMuWhdCCDdxdfL610Hc4cNkn9Q/132" width="30px"><span>还一棵树</span> 👍（4） 💬（1）<div>第二遍到这里啦，看留言有个疑问：
关于没有主键的表 有同样的两行数据，在主库上 limit 1 删除其中的一条，备库也是随机删除其中的一条。
这里有个疑问：解析主库的binlog 看到的row记录完整的binlog如下：
# at 1245
#190523 16:58:32 server id 1  end_log_pos 1293 CRC32 0x598e440d         GTID    last_committed=0        sequence_number=0       rbr_only=no
SET @@SESSION.GTID_NEXT= &#39;f15197b2-f235-11e8-88f1-00163e02236b:6&#39;&#47;*!*&#47;;
# at 1293
#190523 16:58:32 server id 1  end_log_pos 1365 CRC32 0x61325084         Query   thread_id=2     exec_time=0     error_code=0
SET TIMESTAMP=1558601912&#47;*!*&#47;;
BEGIN
&#47;*!*&#47;;
# at 1365
#190523 16:58:32 server id 1  end_log_pos 1411 CRC32 0x2b9b4aea         Table_map: `test`.`bbb` mapped to number 78
# at 1411
#190523 16:58:32 server id 1  end_log_pos 1451 CRC32 0x31dec98e         Delete_rows: table id 78 flags: STMT_END_F

BINLOG &#39;
uGDmXBMBAAAALgAAAIMFAAAAAE4AAAAAAAEABHRlc3QAA2JiYgABAwAB6kqbKw==
uGDmXCABAAAAKAAAAKsFAAAAAE4AAAAAAAEAAgAB&#47;&#47;4BAAAAjsneMQ==
&#39;&#47;*!*&#47;;
### DELETE FROM `test`.`bbb`
### WHERE
###   @1=1 &#47;* INT meta=0 nullable=1 is_null=0 *&#47;
# at 1451
#190523 16:58:32 server id 1  end_log_pos 1482 CRC32 0xd6be57a8         Xid = 216
COMMIT&#47;*!*&#47;;

--从binlog看应该会删除2条的，但不知为什么只删除了一条，这个mysql是怎么控制的？</div>2019-05-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/4b/e4/0219e7c8.jpg" width="30px"><span>小超</span> 👍（4） 💬（2）<div>老师，我看好多人留言都说改set global server_id来造成死循环的，这个server_id为什么不设置成只读，这种修改一般用来做什么用？</div>2019-01-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/cb/0a/6a9e6602.jpg" width="30px"><span>React</span> 👍（3） 💬（1）<div>老师好，文章前面说主从最好从机设置readonly.那么在双主的情况(互为主备)下，设置不同的自增值是否就可以不用设置只读了？且此时复制是否可以跳过主键冲突，因为自增值不同？</div>2019-01-08</li><br/>
</ul>