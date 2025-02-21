上一篇文章中，我们使用Redis模拟了多用户抢票的问题，这里再回顾一下原理。我们通过使用WATCH+MULTI的方式实现乐观锁机制，对ticket\_count这个键进行监视，当这个键发生变化的时候事务就会被打断，重新请求，这样做的好处就是可以保证事务对键进行操作的原子性，当然我们也可以使用Redis的incr和decr来实现键的原子性递增或递减。

今天我们用Redis搭建一个玩家的排行榜，假设一个服务器存储了10万名玩家的数据，我们想给这个区（这台服务器）上的玩家做个全区的排名，该如何用Redis实现呢？

不妨一起来思考下面几个问题：

1. MySQL是如何实现玩家排行榜的？有哪些难题需要解决？
2. 如何用Redis模拟10万名玩家数据？Redis里的Lua又是什么？
3. Redis如何搭建玩家排行榜？和MySQL相比有什么优势？

## 使用MySQL搭建玩家排行榜

我们如果用MySQL搭建玩家排行榜的话，首先需要生成10万名玩家的数据，这里我们使用之前学习过的存储过程来模拟。

为了简化，玩家排行榜主要包括3个字段：user\_id、score、和create\_time，它们分别代表玩家的用户ID、玩家的积分和玩家的创建时间。
<div><strong>精选留言（7）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/10/4a/2c/f8451d77.jpg" width="30px"><span>石维康</span> 👍（11） 💬（3）<div>在生成数据时,把&quot;temp = temp + create_time &#47; 10000000000&quot;换成 temp = temp +1 - create_time &#47; 10000000000 哈哈</div>2019-09-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/10/bb/f1061601.jpg" width="30px"><span>Demon.Lee</span> 👍（11） 💬（5）<div>感觉用redis，最终还是需要结合程序以及MySQL来处理，因为排行榜展示，前端还是需要用户名的，光给个用户id不知道是谁，除非redis有序集合的member包含了用户id和name，请指正。</div>2019-09-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/33/07/8f351609.jpg" width="30px"><span>JustDoDT</span> 👍（5） 💬（1）<div>注册时间排名靠后MySQL语法：create_time按照降序排列。
SELECT (@rownum := @rownum + 1) AS user_rank, user_id, score, create_time
FROM user_score, (SELECT @rownum := 0) b
ORDER BY score DESC, create_time DESC
</div>2019-09-11</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/EcYNib1bnDf5dz6JcrE8AoyZYMdqic2VNmbBtCcVZTO9EoDZZxqlQDEqQKo6klCCmklOtN9m0dTd2AOXqSneJYLw/132" width="30px"><span>博弈</span> 👍（3） 💬（1）<div>Redis在实现排行榜方面优势显著，有现成命令且在内存操作，速度快</div>2020-03-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/92/cd/d39e568c.jpg" width="30px"><span>felix</span> 👍（3） 💬（1）<div>咨询老师一个关于ip匹配的索引问题：
有一个IP的库表，每一条记录了一个开始ip和结束ip，然后想批量匹配ip，查询为何没有用上“联合索引KEY `ip_range_int` (`start_int`,`end_int`) USING BTREE”？要怎么设置索引才有效？
CREATE TABLE `t_dt_ip` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `start_ip` char(15) DEFAULT NULL,
  `end_ip` char(15) DEFAULT NULL,
  `location` varchar(100) DEFAULT NULL,
  `start_int` int(10) unsigned DEFAULT &#39;0&#39;,
  `end_int` int(10) unsigned DEFAULT &#39;0&#39;,
  PRIMARY KEY (`id`),
  KEY `ip_range` (`start_ip`,`end_ip`) USING BTREE,
  KEY `ip_range_int` (`start_int`,`end_int`) USING BTREE
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8;

explain  update t_tmp_ip t, t_dt_ip i  
set t.ip_id = i.id
where INET_ATON(t.ip_address) between i.start_int and i.end_int;
| id | select_type | table | partitions | type | possible_keys                       | key  | key_len | ref  | rows   | filtered | Extra                                          |
|  1 | UPDATE      | t     | NULL       | ALL  | NULL                                | NULL | NULL    | NULL |   1000 |   100.00 | NULL                                           |
|  1 | SIMPLE      | i     | NULL       | ALL  | ip_range_int      | NULL | NULL    | NULL | 541942 |    11.11 | Range checked for each record (index map: 0xC) |

甚至加上单个字段索引也没有用？？
alter table `t_dt_ip` add index indx_t_dt_ip_start_int (start_int);
mysql&gt; explain select * from t_dt_ip i join t_tmp_ip t on 1= 1 where t.ip_address &gt;= i.start_int limit 1;
| id | select_type | table | partitions | type | possible_keys                       | key  | key_len | ref  | rows   | filtered | Extra                                          |
|  1 | SIMPLE      | t     | NULL       | ALL  | NULL                                | NULL | NULL    | NULL |  73126 |   100.00 | NULL                                           |
|  1 | SIMPLE      | i     | NULL       | ALL  | ip_range_int,indx_t_dt_ip_start_int | NULL | NULL    | NULL | 541942 |    33.33 | Range checked for each record (index map: 0xC) |
</div>2019-09-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/17/30/d4/6eb8f5af.jpg" width="30px"><span>白菜炒五花肉</span> 👍（0） 💬（0）<div>ERR Error running script (call to f_84b63a152215a96efa70b8935ae3d2b0e5ab93d1): @user_script:3: user_script:3: bad argument #1 to &#39;randomseed&#39; (number expected, got nil) 老师，使用redis创建10w名玩家数据，执行lua脚本，报这个错误是啥问题</div>2022-08-25</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1d/4a/35/66caeed9.jpg" width="30px"><span>完美坚持</span> 👍（0） 💬（2）<div>为什么
查询某个玩家的排名
对玩家的分数和排名进行更新
查询指定玩家前后 M 名的玩家
增加或移除某个玩家，并对排名进行更新
的时间复杂度都是O(log(N))，这和有序集合的数据存储结构有关吗？老师能不能简单解释一下，或者给个链接
</div>2021-06-09</li><br/>
</ul>