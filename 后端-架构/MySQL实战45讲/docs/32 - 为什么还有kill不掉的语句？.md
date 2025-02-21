在MySQL中有两个kill命令：一个是kill query +线程id，表示终止这个线程中正在执行的语句；一个是kill connection +线程id，这里connection可缺省，表示断开这个线程的连接，当然如果这个线程有语句正在执行，也是要先停止正在执行的语句的。

不知道你在使用MySQL的时候，有没有遇到过这样的现象：使用了kill命令，却没能断开这个连接。再执行show processlist命令，看到这条语句的Command列显示的是Killed。

你一定会奇怪，显示为Killed是什么意思，不是应该直接在show processlist的结果里看不到这个线程了吗？

今天，我们就来讨论一下这个问题。

其实大多数情况下，kill query/connection命令是有效的。比如，执行一个查询的过程中，发现执行时间太久，要放弃继续查询，这时我们就可以用kill query命令，终止这条查询语句。

还有一种情况是，语句处于锁等待的时候，直接使用kill命令也是有效的。我们一起来看下这个例子：

![](https://static001.geekbang.org/resource/image/17/d0/17f88dc70c3fbe06a7738a0ac01db4d0.png?wh=936%2A339)

图1 kill query 成功的例子

可以看到，session C 执行kill query以后，session B几乎同时就提示了语句被中断。这，就是我们预期的结果。
<div><strong>精选留言（30）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/12/9b/a8/6a391c66.jpg" width="30px"><span>geraltlaush</span> 👍（130） 💬（1）<div>kill connection本质上只是把客户端的sql连接断开，后面的执行流程还是要走kill query的，是这样理解吧</div>2019-01-30</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/38/fe/04f56d1e.jpg" width="30px"><span>learn more</span> 👍（102） 💬（1）<div>老师好，文中 set global innodb_thread_concurrency=2的那个例子，前面 Session A 和 Session B 已经占用了两个线程了，那为什么我们还可以在一个新的Session中执行 Kill 或 show full processlist 命令呢？</div>2019-12-26</li><br/><li><img src="" width="30px"><span>Mr.sylar</span> 👍（24） 💬（2）<div>老师，我想问下这些原理的&quot;渔&quot;的方法除了看源码，还有别的建议吗</div>2019-01-25</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/03/c7/563345e1.jpg" width="30px"><span>wjz1991</span> 👍（19） 💬（3）<div>老师，之前也是有遇到程序问题导致cpu爆满，临时先把innodb_thread_concurrency设置为16（降低cpu避免影响同机器实例），然后不断去kill，后面程序人员修复了这个问题后，一堆的killed的语句不释放，设置innodb_thread_concurrency=0，等了半个月都没释放，后面还是安排主从切换，强制重启解决，请问老师，这是为什么？</div>2019-02-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/b2/5a/574f5bb0.jpg" width="30px"><span>Lukia</span> 👍（17） 💬（4）<div>请教老师，删除中间列和修改末尾列这两种DDL的差别在什么地方呢？

作者回复: 对，其实只有 改索引、 加最后一列、删最后一列
其他的大多数不行，比如删除中间一列这种</div>2019-02-19</li><br/><li><img src="" width="30px"><span>700</span> 👍（14） 💬（7）<div>老师，请教。
1）文中开头说“当然如果这个线程有语句正在执行，也是要先停止正在执行的语句的”。我个人在平时使用中就是按默认的执行，不管这个线程有无正在执行语句。不知这样会有什么潜在问题？
2）文中说“实际上，执行 Ctrl+C 的时候，是 MySQL 客户端另外启动一个连接，然后发送一个 kill query 命令“。这个怎么解释呢？
我开启 general log 的时候执行 Ctrl+C 或 Ctrl+D 并没有看到有另外启动一个连接，也没有看到 kill query 命令。general log 中仅看到对应线程 id 和 Quit。
3）MySQL 为什么要同时存在 kill query 和 kill connection，既然 kill query 有无效的场景，干嘛不直接存在一个 kill connection 命令就好了？那它俩分别对应的适用场景是什么，什么时候考虑 kill query，什么时候考虑 kill connection？我个人觉得连接如果直接被 kill 掉大不了再重连一次好了。也没啥损失。
4）小小一个总结，不知对否？
kill query - 会出现无法 kill 掉的情况，只能再次执行 kill connection。
kill connection - 会出现 Command 列显示成 Killed 的情况。</div>2019-01-25</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/11/18/8cee35f9.jpg" width="30px"><span>HuaMax</span> 👍（13） 💬（1）<div>课后题。我认为需要看当时的业务场景。重启会导致其他的连接也断开，返回给其他业务连接丢失的错误。如果有很多事务在等待该事务的锁，则应该重启，让其他事务快速重试获取锁。另外如果是RR的事务隔离级别，长事务会因为数据可见性的问题，对于多版本的数据需要找到正确的版本，对读性能是不是也会有影响，这时候重启也更好。个人理解，请老师指正。</div>2019-01-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/69/de/42c4a3bc.jpg" width="30px"><span>gaohueric</span> 👍（11） 💬（1）<div>老师您好，一个表中 1个主键，2个唯一索引，1个普通索引 4个普通字段，当插入一条全部字段不为空的数据时，此时假设有4个索引文件，分别对应 主键 唯一性索引，普通索引，假设内存中没有这个数据页，那么server是直接调用innodb的接口，然后依次校验 （读取磁盘数据，验证唯一性）主键，唯一性索引，然后确认无误A时刻之后，吧主键和唯一性索引的写入内存，再把普通索引写入change buffer？那普通数据呢，是不是跟着主键一块写入内存了？</div>2019-01-26</li><br/><li><img src="" width="30px"><span>700</span> 👍（9） 💬（1）<div>老师，您好。客户端版本如下：
mysql  Ver 14.14 Distrib 5.7.24, for linux-glibc2.12 (x86_64) using  EditLine wrapper

老师，再请教另一个问题。并非所有的 DDL 操作都可以通过主从切换来实现吧？不适用的场景有哪些呢？</div>2019-01-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/d3/9f/36ea3be4.jpg" width="30px"><span>千年孤独</span> 👍（4） 💬（1）<div>可能不是本章讨论的问题，我想请问老师“MySQL使用自增ID和UUID作为主键的优劣”，基于什么样的业务场景用哪种好?</div>2019-01-27</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTJWjvLFWEzQkszn8nicSaaYFdmE4ribeIicSGu7rfquG3EeuqJYbpHrtThKKDVfDGIib7SE7FBbfuoYDQ/132" width="30px"><span>Geek_a67865</span> 👍（4） 💬（1）<div>也遇到@发条橙子一样的问题，例如队列两个消息同时查询库存，发现都不存在，然后就都执行插入语句，一条成功，一条报唯一索引异常，这样程序日志会一直显示一个唯一索引报错，然后重试执行更新，我暂时是强制查主库</div>2019-01-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/ef/3e/9c3a8abc.jpg" width="30px"><span>杜嘉嘉</span> 👍（4） 💬（1）<div>我想请问下老师，一个事务执行很长时间，我去kill。那么，执行这个事务过程中的数据会不会回滚？</div>2019-01-25</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/e7/7b/71da8283.jpg" width="30px"><span>似水流年</span> 👍（3） 💬（2）<div>老师，请问我直接在操作系统层面用kill命令掉会话的进程，这个会话的事物应该会回滚，除此外有不良影响吗？</div>2019-03-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/df/3e/5f60dfde.jpg" width="30px"><span>think_wtw</span> 👍（3） 💬（1）<div>老师如果正在执行ddl 比如删除一列或者创建一个索引，执行kill query也是事物进行回滚的是吗？内部会做什么操作？ 来得晚还没追上课程。谢谢解答！</div>2019-02-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/4f/78/c3d8ecb0.jpg" width="30px"><span>undifined</span> 👍（3） 💬（1）<div>如果此时仅有一个事务在执行,可以重启,此时 redo log 没有被fsync 到磁盘,重新启动恢复的时候也不会提交该事务
如果有其他事务在执行,就应该等待执行完成
老师这样理解对吗,谢谢老师</div>2019-01-25</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/ea/9a/02d589f9.jpg" width="30px"><span>斜面镜子 Bill</span> 👍（2） 💬（1）<div>“采用不缓存的方式时，如果本地处理得慢，就会导致服务端发送结果被阻塞，因此会让服务端变慢” 这个怎么理解？</div>2019-01-28</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTJWjvLFWEzQkszn8nicSaaYFdmE4ribeIicSGu7rfquG3EeuqJYbpHrtThKKDVfDGIib7SE7FBbfuoYDQ/132" width="30px"><span>Geek_a67865</span> 👍（1） 💬（1）<div>老师好，我猜发条橙子的问题 因为很多日志监控会统计error日志，这样并不很优雅，觉得他是想有什么办法规避这种并发引起的问题，</div>2019-01-26</li><br/><li><img src="" width="30px"><span>700</span> 👍（1） 💬（2）<div>老师，您好。我继续接着我上条留言。
关于2），因为是测试机，我是直接 tail -0f 观察 general log 输出的。确实没看到 KILL QUERY 等字眼。数据库版本是 MySQL 5.7.24。
关于4），文中您不是这样说的吗？
2.但是 session D 执行的 kill query C 命令却没什么效果， 
3.直到 session E 执行了 kill connection 命令，才断开了 session C 的连接，提示“Lost connection to MySQL server during query”， 

感谢您的解答。
</div>2019-01-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/ec/01/978d54af.jpg" width="30px"><span>Justin</span> 👍（1） 💬（1）<div>想咨询一个问题 如果走索引找寻比如age=11的人的时候是只会锁age=10到age=12吗 如果那个索引页包含了从5到13的数据 是只会锁离11最近的还是说二分查找时候每一个访问到的都会锁呢</div>2019-01-25</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/36/d2/c7357723.jpg" width="30px"><span>发条橙子 。</span> 👍（1） 💬（2）<div>老师我这里问一下唯一索引的问题 ，希望老师能给点思路

背景 ： 一张商品库存表 ， 如果表里没这个商品则插入 ，如果已经存在就更新库存 。同步这个库存表是异步的 ，每次添加商品库存成功后会发消息 ， 收到消息后会去表里新增&#47;更新库存

问题 ： 
商品库存表会有一个 商品的唯一索引。
当我们批量添加同一商品库存后会批量发消息 ，消息同时生效后去处理就有了并发的问题 。这时候两个消息都判断表里没有该商品记录， 但是插入的时候就会有一个消息插入成功，另一个消息执行失败报唯一索引的错误， 之后消息重试走更新的逻辑。

这个这样做对业务没有影响 ，但是现在批量添加的需求量上来了 ，线上一直报这种错误日志也不是个办法， 我能想到的除了 catch 掉这个异常就没什么其他思路了。 

老师能给一些其他的思路么</div>2019-01-25</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/46/56/5e83f44b.jpg" width="30px"><span>东青</span> 👍（1） 💬（1）<div>老师，请教一个 第八章 的问题。关于可见性判断，文中都是说事务id大于高水位都不可见。如果等于是不是也不可见。还有一个，readview中是否不包含当前事务id。谢谢老师</div>2019-01-25</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/d5/0c/8dd1791d.jpg" width="30px"><span>superFan</span> 👍（0） 💬（1）<div>老师,我这边无法kill掉, 尝试 &#47;etc&#47;init.d&#47;mysqld stop 报&quot;Timeout error occurred trying to stop MySQL Daemon&quot;, 尝试配置大sotp的timeout也不行,像这种情况有什么方法恢复吗</div>2019-12-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/16/31/ae8adf82.jpg" width="30px"><span>路过</span> 👍（0） 💬（1）<div>老师，kill语法是：
KILL [CONNECTION | QUERY] processlist_id
processlist_id是conn_id，不是thd_id.通过对比sys.processlist表中的信息就可以知道了。
通过查询官方文档也说明了：
thd_id：The thread ID.
conn_id：The connection ID.
所以，这篇文章开头的：
在 MySQL 中有两个 kill 命令：一个是 kill query + 线程 id
感觉有点不对。请老师指正。谢谢！</div>2019-01-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/93/8a/abb7bfe3.jpg" width="30px"><span>亮</span> 👍（0） 💬（1）<div>老师早，请问分库分表这块之后会讲到吗？谢谢老师</div>2019-01-25</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/67/f4/9a1feb59.jpg" width="30px"><span>钱</span> 👍（57） 💬（1）<div>kill不掉
1：kill命令被堵了，还没到位
2：kill命令到位了，但是没被立刻触发
3：kill命令被触发了，但执行完也需要时间
和猜测较近，估计所有的kill命令，kill不掉时都是这么个原因</div>2019-08-04</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTJCscgdVibmoPyRLRaicvk6rjTJxePZ6VFHvGjUQvtfhCS6kO4OZ1AVibbhNGKlWZmpEFf2yA6ptsqHw/132" width="30px"><span>夹心面包</span> 👍（22） 💬（0）<div>对于结尾的问题,我觉得肯定是等待,即便是mysql重启,也是需要对未提交的事务进行回滚操作的,保证数据库的一致性</div>2019-01-25</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/57/4f/6fb51ff1.jpg" width="30px"><span>奕</span> 👍（1） 💬（1）<div>对于 mysql 的各种程序库，是不是建立连接的时候 默认都要加 -A 参数呢？</div>2021-07-25</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/19/16/48/09493874.jpg" width="30px"><span>茶没喝完</span> 👍（1） 💬（0）<div>kill只是修改了线程状态+发出中断信号  
具体被中断的线程在收到中断信号怎么处理，由它自己决定。
直接杀死线程是不安全的，线程占用的资源没法释放，回滚操作没完成等等。</div>2021-02-25</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/40/5e/b8fada94.jpg" width="30px"><span>Ryoma</span> 👍（1） 💬（0）<div>想得简单点：既然事务处于回滚状态了，重启MySQL这部分事务还是需要回滚。私以为让它执行完成比较好。 </div>2019-01-25</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTKaibEtgC5S5OpWSIcogpvqBLm9LYlTdrcfKwicqGURJp3k6Phibnt2DO994p3xeNmX3lpXlerWV1ribw/132" width="30px"><span>努力学习</span> 👍（0） 💬（0）<div>但是 session D 执行的 kill query C 命令却没什么效果. &#47;&#47;测试发现是有效果的。
如下：
MySQL [d4531]&gt; show processlist;
+-------+-----------------+---------------------+-------+---------+---------+------------------------+---------------------------+----------------------+
| Id    | User            | Host                | db    | Command | Time    | State                  | Info                      | Proxy_host           |
+-------+-----------------+---------------------+-------+---------+---------+------------------------+---------------------------+----------------------+
|     5 | event_scheduler | localhost           | NULL  | Daemon  | 3125707 | Waiting on empty queue | NULL                      |                      |
|  9783 | test            | 192.168.26.92:55251 | d4531 | Query   |      16 | User sleep             | select sleep(1000) from t | 192.168.26.161:57637 |
| 26554 | test            | 192.168.26.92:52688 | d4531 | Query   |       5 | executing              | select * from t           | 192.168.26.161:39954 |
| 31355 | test            | 192.168.26.92:60246 | d4531 | Sleep   |     238 |                        | NULL                      | 192.168.26.161:35916 |
| 31370 | test            | 192.168.26.92:60274 | NULL  | Sleep   |     225 |                        | NULL                      | 192.168.26.161:36060 |
| 31382 | test            | 192.168.26.92:60284 | d4531 | Query   |      10 | User sleep             | select sleep(1000) from t | 192.168.26.161:36090 |
| 31430 | test            | 192.168.26.92:60454 | d4531 | Query   |       0 | init                   | show processlist          | 192.168.26.161:37380 |
+-------+-----------------+---------------------+-------+---------+---------+------------------------+---------------------------+----------------------+
7 rows in set (0.01 sec)

MySQL [d4531]&gt; kill query 26554;
Query OK, 0 rows affected (0.63 sec)
mysql参数： 
REPEATABLE-READ   innodb_thread_concurrency =2
</div>2024-07-22</li><br/>
</ul>