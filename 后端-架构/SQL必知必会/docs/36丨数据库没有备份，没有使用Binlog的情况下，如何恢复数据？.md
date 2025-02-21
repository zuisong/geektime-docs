我们上节课讲解了MySQL的复制技术，通过主从同步可以实现读写分离，热备份，让服务器更加高可用。MySQL的复制主要是通过Binlog来完成的，Binlog记录了数据库更新的事件，从库I/O线程会向主库发送Binlog更新的请求，同时主库二进制转储线程会发送Binlog给从库作为中继日志进行保存，然后从库会通过中继日志重放，完成数据库的同步更新。这种同步操作是近乎实时的同步，然而也有人为误操作情况的发生，比如DBA人员为了方便直接在生产环境中对数据进行操作，或者忘记了当前是在开发环境，还是在生产环境中，就直接对数据库进行操作，这样很有可能会造成数据的丢失，情况严重时，误操作还有可能同步给从库实时更新。不过我们依然有一些策略可以防止这种误操作，比如利用延迟备份的机制。延迟备份最大的作用就是避免这种“手抖”的情况，让我们在延迟从库进行误操作前停止下来，进行数据库的恢复。

当然如果我们对数据库做过时间点备份，也可以直接恢复到该时间点。不过我们今天要讨论的是一个特殊的情况，也就是在没做数据库备份，没有开启使用Binlog的情况下，尽可能地找回数据。

今天的内容主要包括以下几个部分：

1. InnoDB存储引擎中的表空间是怎样的？两种表空间存储方式各有哪些优缺点？
2. 如果.ibd文件损坏了，数据该如何找回？
3. 如何模拟InnoDB文件的损坏与数据恢复？
<div><strong>精选留言（17）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/13/16/5b/83a35681.jpg" width="30px"><span>Monday</span> 👍（7） 💬（2）<div>开启innodb_force_recovery只能进行有限制的select操作，那后续的四步中，怎么还能再删除旧表？
上网查的资料都是innodb_force_recovery&gt;0时，可以select，create，drop但是不可以insert，update，delete。。。恨windows系统下安装的mysql没找到在哪里设置innodb_force_recovery的值，所以没验证。。。</div>2019-09-16</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/4d/fd/0aa0e39f.jpg" width="30px"><span>许童童</span> 👍（7） 💬（1）<div>磁盘也是逻辑删除，只要文件还没有被覆盖写，也是可以通过物理的方式把数据找回来的。</div>2019-09-16</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/1b/4a/f9df2d06.jpg" width="30px"><span>蒙开强</span> 👍（4） 💬（2）<div>老师，你好，那个存储引擎是可以针对表级设定的么</div>2019-09-16</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/ic8KF0sfxicsx4F25HZrtZwP2fQEibicfibFeYIQBibxnVlHIiaqkfictJuvLCKia0p7liaQvbTzCYWLibjJK6B8kc8e194ng/132" width="30px"><span>爱思考的仙人球</span> 👍（3） 💬（1）<div>原来丢失数据连接这个错误是由于数据损坏造成的</div>2019-10-25</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/1c/f5/fd386689.jpg" width="30px"><span>Venom</span> 👍（1） 💬（1）<div>代码可不可以都放上来呀 少一句创建存储过程的语句也很麻烦的。。。</div>2019-10-17</li><br/><li><img src="" width="30px"><span>Cookie123456</span> 👍（6） 💬（2）<div>创建的存储过程的完整代码为：
DELIMITER $$
CREATE PROCEDURE `insert_t1`(IN i int, IN max_num int)
BEGIN 
-- 当前数据行
DECLARE i INT DEFAULT 0;
-- 最大数据行数
DECLARE max_num INT DEFAULT 100;
-- 关闭自动提交
SET autocommit=0;
REPEAT
SET i=i+1;
-- 向t1表中插入数据
INSERT INTO t1(id) VALUES(i);
UNTIL i = max_num
END REPEAT;
-- 提交事务
COMMIT;
END $$

CALL insert_t1(0,100);
SELECT @i as sum;
</div>2020-04-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/7b/c5/35f92dad.jpg" width="30px"><span>Jone_乔泓恺</span> 👍（4） 💬（0）<div>请问什么情况会导致.ibd文件损坏呢？</div>2020-04-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/b8/78/2828195b.jpg" width="30px"><span>隰有荷</span> 👍（3） 💬（0）<div>老师，我在使用ibd文件进行数据恢复时，进入了my.cnf文件，
然后设置了innodb_force_recovery = 1，再重新启动Mysql发现无法启动，然后在log里面看到下面这句话：
 [ERROR] &#47;usr&#47;sbin&#47;mysqld: unknown variable &#39;innodb_force_recovery = 1

我去网上搜索这个报错，但是目前没有发现好的解决办法，请问我该怎么样继续操作呢，即使无法获取数据，能获取原来的数据表结构也是好的，希望获取您的指导。</div>2019-11-15</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1d/4a/35/66caeed9.jpg" width="30px"><span>完美坚持</span> 👍（2） 💬（0）<div>想请教大家，文中提到的 “然后用编辑器打开 t1.ibd”，这里的编辑器是什么编辑器啊？</div>2021-06-05</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/59/1d/c89abcd8.jpg" width="30px"><span>四喜</span> 👍（2） 💬（0）<div>自己随便改了idb文件靠后面的2行，只能读取到第一条数据。</div>2020-03-02</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/E3XKbwTv6WTssolgqZjZCkiazHgl2IdBYfwVfAcB7Ff3krsIQeBIBFQLQE1Kw91LFbl3lic2EzgdfNiciaYDlJlELA/132" width="30px"><span>rike</span> 👍（2） 💬（0）<div>按照链接中的数据库文件，在数据库配置文件中添加配置参数后，无法启动。报错
[FATAL] Tablespace id is 1477 in the data dictionary but in file .&#47;wucai&#47;t1.ibd it is 83!</div>2020-01-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/7f/75/551c5d6c.jpg" width="30px"><span>CrazyCodes</span> 👍（1） 💬（0）<div>开启二进制会不会对性能造成影响
</div>2020-01-30</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/76/23/31e5e984.jpg" width="30px"><span>空知</span> 👍（1） 💬（1）<div>如果 ibd文件损坏的数据在开头，那会都select不出来吗？</div>2019-09-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/67/f4/9a1feb59.jpg" width="30px"><span>钱</span> 👍（0） 💬（0）<div>巧妇难为无米之炊，如果数据真没有了（物理删除，磁盘上也被复写了）那基本没什么好方法了，除非产生数据的源头还可以再次通过一定的逻辑生产这些数据。老师本节讲的是，非完全消失的数据，只是不清楚底层原理的话，不知道怎么找到这些可能还在的数据。点赞，很有趣。</div>2024-08-25</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/0c/8e/8a39ee55.jpg" width="30px"><span>文古</span> 👍（0） 💬（1）<div>老师，开始把数据库停止后，放上损坏的t1.ibd，再启动，就会报错Job for mysqld.service failed because the control process exited with error code. See &quot;systemctl status mysqld.service&quot; and &quot;journalctl -xe&quot; for details.
删除t1.ibd，数据库就启动正常，这是什么原因呢？
</div>2023-09-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1e/d7/b7/a78a3d45.jpg" width="30px"><span>中国杰</span> 👍（0） 💬（0）<div>误删表了怎么办，别担心，先把库整个删掉，然后跑路就可以了。。。。</div>2023-02-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/18/24/36/0829cbdc.jpg" width="30px"><span>TheOne</span> 👍（0） 💬（0）<div>磁盘里的数据也是逻辑删除，但是插入多了逻辑删除的数据也就彻底没了</div>2021-09-06</li><br/>
</ul>