你好，我是李玥。

回顾我们之前讲MySQL相关的几节课程，你会发现主从同步有多重要。解决数据可靠性的问题需要用到主从同步；解决MySQL服务高可用要用到主从同步；应对高并发的时候，还是要用到主从同步。

我们在运维MySQL集群时，遇到的很多常见的问题，比如说，为什么从节点故障会影响到主节点？为什么主从切换之后丢数据了？为什么明明没有更新数据，客户端读到的数据还是变来变去的？这些都和主从同步的配置有密切的关系。

你不但要理解MySQL主从同步的原理，还要掌握一些相关配置的含义，才能正确地配置你的集群，知道集群在什么情况下会有什么样的行为，可能会出现什么样的问题，并且知道该如何解决。

今天这节课我们就来详细讲一下，MySQL的主从同步是怎么实现的，以及如何来正确地配置主从同步。

## 如何配置MySQL的主从同步？

当客户端提交一个事务到MySQL的集群，直到客户端收到集群返回成功响应，在这个过程中，MySQL集群需要执行很多操作：主库需要提交事务、更新存储引擎中的数据、把Binlog写到磁盘上、给客户端返回响应、把Binlog复制到所有从库上、每个从库需要把复制过来的Binlog写到暂存日志中、回放这个Binlog、更新存储引擎中的数据、给主库返回复制成功的响应。
<div><strong>精选留言（29）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/16/e7/76/79c1f23a.jpg" width="30px"><span>李玥</span> 👍（34） 💬（1）<div>Hi，我是李玥。

这里回顾一下上节课的思考题：

课后请你对照你现在负责开发或者维护的系统来分享一下，你的系统实施读写分离的具体方案是什么样的？比如，如何分离读写数据库请求？如何解决主从延迟带来的数据一致性问题？欢迎你在留言区与我讨论。

课后很多小伙伴在留言区对这个问题做了回复，分离读写请求大多数采用的是代理或者Sharding-JDBC这两种方案。那解决主从延迟，没有完全避免延迟的方法，但至少要做到能够监控主从延迟，当延迟太大的时候，采用一些降级方案。比如说，把重要业务的读请求切回主库，暂停一些不重要的业务，甚至限流等等。</div>2020-03-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/21/60/b21da12a.jpg" width="30px"><span>渐渐迷失</span> 👍（7） 💬（1）<div>老师你好
之前学mq的时候您课讲完了，我才进入学习的，有好些问题还不会，追过来问问可以吗</div>2020-03-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/81/4e/d71092f4.jpg" width="30px"><span>夏目</span> 👍（24） 💬（0）<div>redis在重启时现在也可以采用这种策略，RDB快照加上aof日志恢复数据</div>2020-04-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/34/df/64e3d533.jpg" width="30px"><span>leslie</span> 👍（17） 💬（0）<div>最典型的应当是VMware:其实复制技术不仅仅在linux系统的中间件存储 mysql、redis、ES上使用，Windows的sql server同样适用了此技术。</div>2020-03-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/57/4f/6fb51ff1.jpg" width="30px"><span>奕</span> 👍（10） 💬（0）<div>MySQL 启用半同步复制，需要登录MySQL安装插件(或者修改配置文件)
Linux： install plugin rpl_semi_sync_master soname &#39;semisync_master_so&#39; (window 是 dll)
从库使用的是 semisync_slave.so 文件

这时候MySQL 会自动去 安装目录的 lib&#47;plugin 文件夹下去找</div>2020-03-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/73/ce/23bd3997.jpg" width="30px"><span>Wiggins</span> 👍（9） 💬（2）<div>读完mysql实战45讲再读老师的文章感觉又复习了一遍 老师的文章很清晰 更加偏向实战中的配置了</div>2020-03-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/8d/99/f886543d.jpg" width="30px"><span>渔夫</span> 👍（8） 💬（0）<div>目前主流前端技术的状态管理也是这个状态机机制：state + action = next state</div>2020-03-31</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/da/dd/1e5e7b0c.jpg" width="30px"><span>image</span> 👍（4） 💬（0）<div>fork and write，典型有docker镜像，linux fork都和复制状态机有关系，这也是一种基本的构建模式</div>2020-03-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/9c/c6/05a6798f.jpg" width="30px"><span>苗</span> 👍（3） 💬（0）<div>基于事件朔源的应用程序，就是用snapshot + 事件来快速恢复对象的状态。</div>2020-05-03</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/31/00/b5fd38df.jpg" width="30px"><span>Ling</span> 👍（2） 💬（0）<div>- rpl_semi_sync_master_timeout
  为了防止半同步复制在没有收到确认的情况下发生堵塞，如果主库在`rpl_semi_sync_master_timeout`毫秒超时之前没有收到确认，将恢复到异步复制
  以毫秒为单位，默认值是10000(10秒)。

- rpl_semi_sync_master_wait_for_slave_count
  在继续处理事务之前，必须接收的副本确认的数量；
  越小，需要等待确认的从节点越少，性能越好；
  MySQL默认值是`1`；阿里云的一主一备高可用版RDS，配置该值为`1`

- rpl_semi_sync_master_wait_no_slave
  当前存活从节点数小于`rpl_semi_sync_master_wait_for_slave_count`中配置的值时，是否还需要等待`rpl_semi_sync_master_timeout`中配置的超时时间；
  环境：如果配置的`rpl_semi_sync_master_wait_for_slave_count`是2，但是当前只有一个从节点
  如果配置为`ON`：主库还是会等待`rpl_semi_sync_master_timeout`秒后超时，然后切换为`异步复制`
  如果配置为`OFF`：立刻变为`异步复制`
  MySQL默认该值为`ON`，阿里云的一主一备高可用版RDS，配置该值为`OFF`</div>2021-05-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/fa/64/457325e6.jpg" width="30px"><span>Sam Fu</span> 👍（1） 💬（0）<div>指出老师文章中的一个错误:文章中说半同步复制和同步复制的区别是同步复制在 commit 之前需要等待所有的从节点全部返回 ack，而半同步只需要等待部分从节点（ack 数量可配置）返回 ack。这里是有问题的。按照老师的说法，对于一主一从的架构，半同步和全同步岂不是没有区别了。
半同步和全同步的区别在于：

- 设置为半同步，从节点将 binlog 写入 relay log 返回 ack 给主节点
- 设置为全同步，从节点将 relay log 执行完返回 ack 给主节点。

补充一个半同步设置的参数 rpl_semi_sync_master_timeout:为了防止半同步复制在没有收到确认的情况下发生堵塞，如果主库在`rpl_semi_sync_master_timeout`毫秒超时之前没有收到确认，将恢复到异步复制,以毫秒为单位，默认值是 10000(10 秒)。
这里如果业务上不能接受数据丢失，比如金融场景用户转账了但是钱没收到引起社会舆论，应该将其设置为永远不降级。
</div>2023-08-25</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/51/86/b5fd8dd8.jpg" width="30px"><span>建强</span> 👍（1） 💬（0）<div>思考题：
复制状态机的思想也用于数据同步，当把一批频繁变化的数据从一个地方同步到另一个地方时，先对数据做一个初始化的全量同步，相当于给数据拍一个快照，然后给数据加一个时间戳字段，记录下拍快照时的时间戳，每当数据发生增、删、改时，时间戳也发生改变，根据时间戳的变化，只需要把时间戳大于快照时间戳的数据进行增量同步即可，这种思想算不是复制状态机，请老师指正。</div>2021-12-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1c/c8/7b/153181d7.jpg" width="30px"><span>夜辉</span> 👍（1） 💬（0）<div>redis持久化存储方式：rdb 和 aof
后面还出了一种二者混合的方式
</div>2021-04-10</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/vQiadbkZYR239J80hjekw7jzY9vy6otLKPNDSuz2lruDiaXlKGkcsX5wwiaFevicgqV8odlRG4UITiadDF3fgicrHPcw/132" width="30px"><span>疯码</span> 👍（1） 💬（0）<div>游戏同步。从同一基础状态开始，各客户端施加同样的操作 得到同样的结果。</div>2020-12-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/26/eb/d7/90391376.jpg" width="30px"><span>ifelse</span> 👍（0） 💬（0）<div>任何一个存储系统，无论它存储的是什么数据，用什么样的数据结构，都可以抽象成一个状态机。--记下来</div>2022-12-09</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/DYAIOgq83er4rbCWDxib3FHibYBouTwZqZBH6h5IgvjibEiaBv4Ceekib9SYg0peBBlFGu8hDuGvwjKp6LNznvEAibYw/132" width="30px"><span>DonaldTrumpppppppppp</span> 👍（0） 💬（0）<div>老师好，现在有个问题急需您指点。一主一备时，半同步模式下，主节点退化为异步同步模式后，从节点恢复后但未和主同步一致的情况下，主挂了，备升级为主。这时出现不一致的情况该如何处理？ </div>2022-03-04</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/65/cf/f4305170.jpg" width="30px"><span>ALEX</span> 👍（0） 💬（0）<div>git commit log 加上本地副本</div>2021-12-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1e/37/29/b3af57a7.jpg" width="30px"><span>凯文小猪</span> 👍（0） 💬（0）<div>感谢老师深入浅出的分享 看过这篇后 对于redis mongodb kafka mysql这些存储介质豁然开朗。原来一天学完存储介质真的不是梦</div>2021-04-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/66/d1/8664c464.jpg" width="30px"><span>flyCoder</span> 👍（0） 💬（1）<div>半同步复制，主节点挂了，怎么样保证数据的完整性呢？ 从节点之间会相互复制吗？</div>2021-02-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/45/8f/a56b2214.jpg" width="30px"><span>innocent</span> 👍（0） 💬（0）<div>Raft协议也用到了复制状态机</div>2021-02-02</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/8c/5c/3f164f66.jpg" width="30px"><span>亚林</span> 👍（0） 💬（0）<div>学好数学建模课程的重要性</div>2020-10-22</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTIxEuD0ytJhQYiceS3EZbyE8M3nQ7fWyTFnAm6Vjo5F8P8utfTw4fkWlqJeNEGJfQyXAgnap18gk1w/132" width="30px"><span>肖雄</span> 👍（0） 💬（0）<div>kafka的leader节点和follow节点同步</div>2020-08-16</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/ee/bb/7afd6824.jpg" width="30px"><span>闫冬</span> 👍（0） 💬（0）<div>这篇收获满满</div>2020-04-16</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/19/2e/ca/469f7266.jpg" width="30px"><span>菠萝吹雪—Code</span> 👍（0） 💬（0）<div>打卡</div>2020-04-01</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/1d/de/62bfa83f.jpg" width="30px"><span>aoe</span> 👍（0） 💬（0）<div>复制状态机！原来这个理论这么强大！第一次听说，非常激动！感谢老师！</div>2020-03-30</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/21/60/b21da12a.jpg" width="30px"><span>渐渐迷失</span> 👍（0） 💬（1）<div>我之前关于mq的发言上墙了 我就直接问了 之前mq的课程 讲生产者和消费者源码尤其namedservice部分讲透了  我还想了解下 mq在集群模式下 队列怎么分布，rocketmq 是否有镜像队列，脑裂后怎么处理，mq 集群对比es和redis这种读远大于写的集群有什么特点 求解答或者知识链接</div>2020-03-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/2a/a5/625c0a2e.jpg" width="30px"><span>hhhh</span> 👍（0） 💬（0）<div>老师您讲过的消息队列应该也是这种模式</div>2020-03-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/57/6e/b6795c44.jpg" width="30px"><span>夜空中最亮的星</span> 👍（0） 💬（0）<div>老师带我们一起飞</div>2020-03-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/1a/05/f154d134.jpg" width="30px"><span>刘楠</span> 👍（0） 💬（0）<div>mongodb写大多数节点，和这个半同步有点一样，</div>2020-03-26</li><br/>
</ul>