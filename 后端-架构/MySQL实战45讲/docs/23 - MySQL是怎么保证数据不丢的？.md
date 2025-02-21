今天这篇文章，我会继续和你介绍在业务高峰期临时提升性能的方法。从文章标题“MySQL是怎么保证数据不丢的？”，你就可以看出来，今天我和你介绍的方法，跟数据的可靠性有关。

在专栏前面文章和答疑篇中，我都着重介绍了WAL机制（你可以再回顾下[第2篇](https://time.geekbang.org/column/article/68633)、[第9篇](https://time.geekbang.org/column/article/70848)、[第12篇](https://time.geekbang.org/column/article/71806)和[第15篇](https://time.geekbang.org/column/article/73161)文章中的相关内容），得到的结论是：只要redo log和binlog保证持久化到磁盘，就能确保MySQL异常重启后，数据可以恢复。

评论区有同学又继续追问，redo log的写入流程是怎么样的，如何保证redo log真实地写入了磁盘。那么今天，我们就再一起看看MySQL写入binlog和redo log的流程。

# binlog的写入机制

其实，binlog的写入逻辑比较简单：事务执行过程中，先把日志写到binlog cache，事务提交的时候，再把binlog cache写到binlog文件中。

一个事务的binlog是不能被拆开的，因此不论这个事务多大，也要确保一次性写入。这就涉及到了binlog cache的保存问题。

系统给binlog cache分配了一片内存，每个线程一个，参数 binlog\_cache\_size用于控制单个线程内binlog cache所占内存的大小。如果超过了这个参数规定的大小，就要暂存到磁盘。
<div><strong>精选留言（30）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/14/30/28/6e019a7a.jpg" width="30px"><span>锅子</span> 👍（190） 💬（16）<div>老师好，有一个疑问：当设置sync_binlog=0时，每次commit都只时write到page cache，并不会fsync。但是做实验时binlog文件中还是会有记录，这是什么原因呢？是不是后台线程每秒一次的轮询也会将binlog cache持久化到磁盘？还是有其他的参数控制呢？</div>2019-01-04</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/c4/74/27cf551a.jpg" width="30px"><span>WilliamX</span> 👍（162） 💬（8）<div>为什么 binlog cache 是每个线程自己维护的，而 redo log buffer 是全局共用的？
这个问题，感觉还有一点，binlog存储是以statement或者row格式存储的，而redo log是以page页格式存储的。page格式，天生就是共有的，而row格式，只跟当前事务相关</div>2019-01-04</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/1d/b5/971261fd.jpg" width="30px"><span>alias cd=rm -rf</span> 👍（138） 💬（17）<div>事务A是当前事务，这时候事务B提交了。事务B的redolog持久化时候，会顺道把A产生的redolog也持久化，这时候A的redolog状态是prepare状态么？
</div>2019-01-28</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTIiatbibYU9p7aVpq1o47X83VbJtsnP9Dkribian9bArLleibUVMDfD9S0JF9uZzfjo6AX5eR6asTiaYkvA/132" width="30px"><span>倪大人</span> 👍（88） 💬（10）<div>老师求解sync_binlog和binlog_group_commit_sync_no_delay_count这两个参数区别

如果
       sync_binlog = N
       binlog_group_commit_sync_no_delay_count = M
       binlog_group_commit_sync_delay = 很大值
这种情况fsync什么时候发生呀，min(N,M)吗？
感觉sync_binlog搭配binlog_group_commit_sync_delay也可以实现组提交？

如果
        sync_binlog = 0
         binlog_group_commit_sync_no_delay_count = 10
这种情况下是累计10个事务fsync一次？</div>2019-01-04</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/e0/41/8ae7a30a.jpg" width="30px"><span>Komine</span> 👍（83） 💬（4）<div>为什么binlog 是不能“被打断的”的呢？主要出于什么考虑？</div>2019-01-22</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTLkhgYnYZBdhdwKnXQibey04cy9N9ria3DadH7iagoKukaWK1FJwjfCoh0He4p7b2icSYVzHH71l8ZXiaQ/132" width="30px"><span>猪哥哥</span> 👍（46） 💬（4）<div>老师 我想问下文件系统的page cache还是不是内存, 是不是文件系统向内核申请的一块的内存?</div>2019-01-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/f8/70/f3a33a14.jpg" width="30px"><span>某、人</span> 👍（42） 💬（19）<div>有调到非双1的时候,在大促时非核心库和从库延迟较多的情况。
设置的是sync_binlog=0和innodb_flush_log_at_trx_commit=2
针对0和2,在mysql crash时不会出现异常,在主机挂了时，会有几种风险:
1.如果事务的binlog和redo log都还未fsync,则该事务数据丢失
2.如果事务binlog fsync成功,redo log未fsync,则该事务数据丢失。
虽然binlog落盘成功,但是binlog没有恢复redo log的能力,所以redo log不能恢复.
不过后续可以解析binlog来恢复这部分数据
3.如果事务binlog fsync未成功,redo log成功。
由于redo log恢复数据是在引擎层,所以重新启动数据库,redo log能恢复数据,但是不能恢复server层的binlog,则binlog丢失。
如果该事务还未从FS page cache里发送给从库,那么主从就会出现不一致的情况
4.如果binlog和redo log都成功fsync,那么皆大欢喜。

老师我有几个问题:
1.因为binlog不能被打断,那么binlog做fsync是单线程吧?
如果是的话,那么binlog的write到fsync的时间,就应该是redo log fsync+上一个事务的binlog fsync时间。
但是测试到的现象,一个超大事务做fsync时,对其它事务的提交影响也不大。
如果是多线程做fsync,怎么保证的一个事务binlog在磁盘上的连续性？
2.  5.7的并行复制是基于binlog组成员并行的,为什么很多文章说是表级别的并行复制？</div>2019-01-06</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/e0/3c/ae0f6f57.jpg" width="30px"><span>xiaoyou</span> 👍（27） 💬（18）<div>老师，请教一个问题，文章说innodb的 redo log 在commit的时候不进行fsync，只会write 到page cache中。当sync_binlog&gt;1,如果redo log 完成了prepare持久化落盘，binlog只是write page cache，此时commit标识完成write 但没有落盘，而client收到commit成功，这个时候主机掉电，启动的时候做崩溃恢复，没有commit标识和binglog，事务会回滚。我看文章说sync_binlog设置为大于1的值，会丢binlog日志,此时数据也会丢失吧？</div>2019-01-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/b8/36/542c96bf.jpg" width="30px"><span>Mr.Strive.Z.H.L</span> 👍（25） 💬（12）<div>老师你好，看了@倪大人的问题，个人认为：
sync_binlog和binlog_group_commit_sync_no_delay_count的最大区别主要在于，数据的丢失与否吧？

sync_binlog = N：每个事务write后就响应客户端了。刷盘是N次事务后刷盘。N次事务之间宕机，数据丢失。

binlog_group_commit_sync_no_delay_count=N： 必须等到N个后才能提交。换言之，会增加响应客户端的时间。但是一旦响应了，那么数据就一定持久化了。宕机的话，数据是不会丢失的。

不知道我这么理解对不对？
</div>2019-01-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/00/f0/08409e78.jpg" width="30px"><span>一大只😴</span> 👍（25） 💬（1）<div>你是怎么验证的？等于0的时候虽然有走这个逻辑，但是最后调用fsync之前判断是0，就啥也没做就走了
回复老师:
       老师，我说的sync_binlog=0或=1效果一样，就是看语句实际执行的效果，参数binlog_group_commit_sync_delay我设置成了500000微秒，在=1或=0时，对表进行Insert，然后都会有0.5秒的等待，也就是执行时间都是0.51 sec，关闭binlog_group_commit_sync_delay，insert执行会飞快，所以我认为=1或=0都是受组提交参数的影响的。</div>2019-01-05</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/fe/75/46742f12.jpg" width="30px"><span>liao xueqiang</span> 👍（14） 💬（9）<div>每秒一次后台轮询刷盘，再加上崩溃恢复这个逻辑，InnoDB 就认为 redo log 在 commit 的时候就不需要 fsync 了，只会 write 到文件系统的 page cache 中就够了。老师好，这句话怎么理解呢？这不是服务器重启的情况下，会丢失1秒的数据吗</div>2019-03-01</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/1d/b5/971261fd.jpg" width="30px"><span>alias cd=rm -rf</span> 👍（12） 💬（3）<div>老师不好意思，我接着刚才的问题问哈
并发事务的redolog持久化，会把当前事务的redolog持久化，当前事务的redolog持久化后prepare状态么？redolog已经被持久化到磁盘了，那么当前事务提交时候，redolog变为prepare状态，这时候是从redologbuffer加载还是从磁盘加载？</div>2019-01-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/9f/1d/ec173090.jpg" width="30px"><span>melon</span> 👍（11） 💬（2）<div>老师帮忙看一下我binlog 组提交这块理解的对不对

binlog write 阶段
组里面第一个走到 binlog write 的事务记录一个时间戳，用于在 binlog fsync 阶段计算 sync delay了多少时间，姑且计为 start_time
组里已 sync write 次数+1，姑且记为 group_write
全局已 sync wirte 次数+1，姑且记为 global_write

binlog fsync 阶段
IF ( NOW - sart_time ) &gt;= binlog_group_commit_sync_delay || group_write &gt;= binlog_group_commit_sync_no_delay_count
    IF sync_binlog &gt;0 &amp;&amp; global_write &gt;= sync_binlog
        fsync

    设置 binlog 组提交信号，让其它等待的事务继续
ELSE
    等待 binlog 组提交信号

另外 binlog_group_commit_sync_no_delay_count 这个参数是不是不应该设置的比并发线程数大，因为一个组里的事务应该不会比并发线程数多吧，设置大了也就没什么意义了，可以这么理解吧老师。</div>2019-02-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/bd/be/53350286.jpg" width="30px"><span>Geek_527020</span> 👍（10） 💬（7）<div>事务还未结束，binlog和redo log就写到磁盘中了，如果出现了事务回滚，写到磁盘的数据要删除吗，如果不删除，MYSQL奔溃重启，岂不是多了操作，请老师解答下疑惑</div>2019-01-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/ec/01/978d54af.jpg" width="30px"><span>Justin</span> 👍（10） 💬（1）<div>您说的Lsn 确保不会二次执行 意思是持久化在磁盘中的页也有和redo log record相关的lsn吗 然后根据lsn的大小在recovery阶段确定redo log需不需要执行？</div>2019-01-05</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/d6/60/f21b2164.jpg" width="30px"><span>jacy</span> 👍（9） 💬（3）<div>1.先把 binlog 从 binlog cache 中写到磁盘上的 binlog 文件；
2.调用 fsync 持久化。

老师，这两步我不不太理解，写到磁盘binlog文件，不就是持久化了吗，为啥还要调用fsync再刷一次盘呢？能否帮忙解答一下，感谢🙏</div>2019-05-30</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/38/ed/72f73710.jpg" width="30px"><span>嘻嘻</span> 👍（9） 💬（1）<div>1. 如果客户端收到事务成功的消息，事务就一定持久化了；
commit是在什么阶段返回的？如果写完page cache就返回也没有持久化吧？</div>2019-01-25</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/b4/21/17a88779.jpg" width="30px"><span>莫名</span> 👍（8） 💬（1）<div>老师，sync_binlog=N，N之间客户端已明确收到事务提交，而如果期间机器崩溃或掉电，重启会导致数据库数据也丢失或回滚，那不是客户端处理的数据可能也会有问题？比如账户类数据、银行转账等？望解惑！</div>2019-05-11</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTLE4LYb3jrH63ZV98Zpc8DompwDgb1O3nffMoZCmiaibauRyEFv6NDNsST9RWxZExvMLMWb50zaanoQ/132" width="30px"><span>慧鑫coming</span> 👍（8） 💬（1）<div>这里提示和我一样的小白，注意老师最后的说的提升io性能方法3，是在主机掉电或os崩溃的时候，page cache 会丢失;而最后老师建议将redo log写到page cash，说的是能防止“MySQL异常重启时数据丢失”。也就是仅仅写数据的程序crash，那么已经写入page cash中的数据不会丢失，但如果系统crash或者重启的话，那就没办法啦😆</div>2019-01-04</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTLE4LYb3jrH63ZV98Zpc8DompwDgb1O3nffMoZCmiaibauRyEFv6NDNsST9RWxZExvMLMWb50zaanoQ/132" width="30px"><span>慧鑫coming</span> 👍（7） 💬（1）<div>老师，请问binlog_group_commit_sync_no_delay_count和sync_binlog参数有什么区别，前者设置为10后者设置为5，那是几次write page_cache才写盘一次？</div>2019-01-07</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/11/18/8cee35f9.jpg" width="30px"><span>HuaMax</span> 👍（6） 💬（1）<div>老师在解释组提交的原理那里的图中第二步应该是binlog cache写入到系统page cache的意思吧？</div>2019-01-04</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/da/ec/779c1a78.jpg" width="30px"><span>往事随风，顺其自然</span> 👍（6） 💬（1）<div>binlog cache 和page cache 有啥区别，一个在内存一个在磁盘，page cache 不是已经在磁盘？</div>2019-01-04</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/e9/ab/37903736.jpg" width="30px"><span>J!</span> 👍（5） 💬（4）<div>共同写一个binlog文件，这个过程应该需要锁来维持提交的时序吧，写文件的时候是不是可能会变成瓶颈点？</div>2019-01-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/b8/36/542c96bf.jpg" width="30px"><span>Mr.Strive.Z.H.L</span> 👍（5） 💬（1）<div>老师好，关于组提交还是有几个疑惑：
我理解的，组提交分为binlog和redolog。
binlog如果没有组提交的话，是不是涉及到 写binlog的顺序与写redolog的顺序不一致的问题？这个顺序问题需要加锁来解决，事务之间串行执行prepare到commit的过程。
而binlog有了组提交，内部实际上通过队列的机制，既保证了组提交减少IOPS消耗，同时队列的机制保证了binlog和redolog写入的顺序性。

上述这么理解正确吗？

还有一个问题就是图5两阶段提交细化的过程：
binlog的write 到 sync之间插入了 redolog的 sync。图上的顺序表示binlog的sync必须等到redolog的sync执行后才能执行？ redolog在引擎内部，binlog在server端，这个串行是如何保证的？？（因为我认为server与innodb只会交互两次呀，第一次是prepare请求，第二次是最后的commit请求，binlog怎么做到等待redolog sync完后再sync？）</div>2019-01-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/e0/b9/bca7ff9a.jpg" width="30px"><span>way</span> 👍（5） 💬（3）<div>老师新年好。之前遇到个有意思的现象。主从切换以后。从库延迟一直追不上。查下来是组提交的两个参数有设置。都调整为0以后，很快就追上了。</div>2019-01-05</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/e3/4f/4709b019.jpg" width="30px"><span>一只羊</span> 👍（4） 💬（2）<div>也不知道还会不会有问题解答，试试。

我的问题是：现在知道 redo log 和 binlog 的落盘时机。但是我不知道记录数据是在什么时候、什么方式落盘的。
不知道还有机会得到解答不。</div>2019-08-15</li><br/><li><img src="" width="30px"><span>miu</span> 👍（4） 💬（1）<div>老师，关于BINLOG_GROUP_COMMIT_SYNC_DELAY，
BINLOG_GROUP_COMMIT_SYNC_NO_DELAY_COUNT，
SYNC_BINLOG三个参数，我的理解是：
若SYNC_BINLOG&gt;1时，且设置了BINLOG_GROUP_COMMIT_SYNC_DELAY和BINLOG_GROUP_COMMIT_SYNC_NO_DELAY_COUNT两个参数。
例如 
sync_binlog=2，
BINLOG_GROUP_COMMIT_SYNC_DELAY=1000000，
BINLOG_GROUP_COMMIT_SYNC_NO_DELAY_COUNT=3，
那么在执行完第1个事务后，在第2个事务提交时，会根据后续的事务提交来判断fsync等待的时间，
若后续在1秒内没有累积3个事务的提交，则会等待1秒后再做fsync，从SQL语句来看，执行第一个语句很快，第二个语句需要等待1秒才成功。这时延时等待的时间是BINLOG_GROUP_COMMIT_SYNC_DELAY所设置的值。
若执行完第1个事务后，并行执行3个事务（1秒内完成），则后续3个事务会同时做fsync，这时延时等待的时间是BINLOG_GROUP_COMMIT_SYNC_NO_DELAY_COUNT设置的数量的事务提交的间隔时间。
也就是sync_binlog+BINLOG_GROUP_COMMIT_SYNC_NO_DELAY_COUNT-1 个事务做一次fsync。
我测试的版本是MySQL官方5.7.24，请老师点评。

</div>2019-02-01</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/bd/be/53350286.jpg" width="30px"><span>Geek_527020</span> 👍（3） 💬（1）<div>您好，老师，我有一个以后，组提交，把为提交事务的redo log写入磁盘，如果有查询，岂不是查到未提交事务的更新内容了?</div>2019-01-25</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/db/80/6b7629d7.jpg" width="30px"><span>roaming</span> 👍（3） 💬（1）<div>看了几遍，终于看明白了</div>2019-01-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/4e/3a/86196508.jpg" width="30px"><span>linqw</span> 👍（3） 💬（1）<div>老师打扰下，问几个问题哦
1、一次事务在提交前，redo log在prepare阶段就会刷盘，为什么在commit的时候，还需要write到文件系统的page cache中了？
2、有一次记得整个服务崩了，innodb_buffer_pool_size太小，修改了5.6 版的my.cnf文件那时多加了一句innodb_buffer_pool_chunk_size，这个好像在5.7之后新增的，导致mysqld.pid和mysqld.sock这两个文件没有生成，导致数据库服务报: Can&#39;t connect to local MySQL server through socket &#39;&#47;tmp&#47;mysql.sock&#39; (2)，那时将配置文件中的这行去掉，数据库才可以正常使用，其中的原理不是很清楚
3、rollback在commit之后立即执行，没有任何影响么？
4、varchar类型长度修改，varchar类型好像是没有存在聚簇索引中，若需要预留varchar类型字段，还无法确定实际需要的长度。而当需要启用到预留的字段时，表中可能已经有很多数据，此时要根据需要修改字段长度, 而不需要重做数据？</div>2019-01-05</li><br/>
</ul>