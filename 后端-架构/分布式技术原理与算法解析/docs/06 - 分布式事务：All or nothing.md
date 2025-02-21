你好，我是聂鹏程。今天，我来继续带你打卡分布式核心技术。

对于网上购物的每一笔订单来说，电商平台一般都会有两个核心步骤：一是订单业务采取下订单操作，二是库存业务采取减库存操作。

通常，这两个业务会运行在不同的机器上，甚至是运行在不同区域的机器上。针对同一笔订单，当且仅当订单操作和减库存操作一致时，才能保证交易的正确性。也就是说一笔订单，只有这两个操作都完成，才能算做处理成功，否则处理失败，充分体现了“All or nothing”的思想。

在分布式领域中，这个问题就是分布式事务问题。那么今天，我们就一起打卡分布式事务吧。

## 什么是分布式事务？

在介绍分布式事务之前，我们首先来看一下什么是事务。

事务（Transaction）提供一种机制，将包含一系列操作的工作序列纳入到一个不可分割的执行单元。只有所有操作均被正确执行才能提交事务；任意一个操作失败都会导致整个事务回滚（Rollback）到之前状态，即所有操作均被取消。简单来说，事务提供了一种机制，使得工作要么全部都不做，要么完全被执行，即all or nothing。

通常情况下，我们所说的事务指的都是本地事务，也就是在单机上的事务。而事务具备四大基本特征ACID，具体含义如下。
<div><strong>精选留言（30）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/0f/f8/ba/d28174a9.jpg" width="30px"><span>Geek_zbvt62</span> 👍（47） 💬（17）<div>
疑问不少
1. 2pc和3pc的第一步到底是不是“类似”？从本文中看，2pc corhort 收到CanCommit已经开始执行事务但不提交，3pc则写着在PreCommit阶段开始预提交。文中说二者第一步“类似”，但其实是非常不类似的吧？
2. 我看到的资料里，3pc出现的目的，并不是文中说的为了解决那两个问题，因为这两个问题的解决方案在2pc中也可以引入。同步阻塞问题和本地事务隔离性相关。数据不一致在两者也都会出现。3pc多了一步，这些就能避免了么？
3pc很多机制在这里没提到，这些才是真正对比2pc的改进。比如只要coordinator收到大多数ack，第三阶段即进入commit状态。本质上3pc并不能像共识算法那样保证一致性，而是比起2pc，增加了在一些未知状态下，“状态可能是成功”的判断依据。
3. 分布式消息中间件实现事务，重点是回查，这点没提啊。</div>2019-10-04</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/33/9f/8dbd9558.jpg" width="30px"><span>逆流的鱼</span> 👍（15） 💬（3）<div>三阶段为什么就不阻塞了？没明白</div>2019-10-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/6b/f8/b4da7936.jpg" width="30px"><span>大魔王汪汪</span> 👍（8） 💬（1）<div>可靠消息这种方式必须采用mq吗？使用db是不是也可以，看起来只是一个事务状态的存储和管理，是多个两阶段提交的组合啊！</div>2019-10-06</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/ed/89/86340059.jpg" width="30px"><span>licong</span> 👍（5） 💬（2）<div>三阶段也有一个协调者，为什么就不会有单点故障了？</div>2019-10-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1b/87/37/b071398c.jpg" width="30px"><span>等风来🎧</span> 👍（1） 💬（1）<div>你好，应该是3PC把2PC的投票阶段再次一分为二，不是把提交阶段一分为二了吧</div>2020-06-05</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/61/b2/f36c1d40.jpg" width="30px"><span>破发者</span> 👍（1） 💬（1）<div>老师好：
3pc在 DoCommit 阶段，当参与者向协调者发送 Ack 消息后，整个事务不就结束了吗？为什么文章里还说如果长时间没有得到协调者的响的话参与者会自动将超时的事务进行提交。</div>2020-05-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/c6/73/abb7bfe3.jpg" width="30px"><span>疯琴</span> 👍（1） 💬（2）<div>请问老师一个问题：两阶段提交中，第一阶段订单系统只是准备好增加一条关于用户 A 购买 100 件 T 恤的信息并锁库，但是没有实际的数据操作，那么在第二阶段不是直接解锁就好了么，何来的数据退回呢？</div>2019-10-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/f8/49/e292f240.jpg" width="30px"><span>boglond</span> 👍（0） 💬（1）<div>CAP理论老师没有讲一讲。</div>2019-10-06</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/bc/25/1c92a90c.jpg" width="30px"><span>tt</span> 👍（0） 💬（1）<div>老师，分布式事物，可以用于工作流系统么？

比如工作流上总体有3个节点，A,B,C，每个节点的操作均分为经办和复合操作，当作业顺序经历A→B→C后，一个事务才算完成。

中间任意一个环节都可能发生回退，如C认为条件不成立而将作业退回给B。

最后，每个环节经历的事件可能都很长，已天为度量单位。

我想请教一下老师，这样的系统还算是分布式系统么？如果不是，那该如何借鉴分布式事物的原理进行设计呢？</div>2019-10-05</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/62/1e/8054e6db.jpg" width="30px"><span>樂文💤</span> 👍（25） 💬（7）<div>
不太明白基于消息队列的方法如何解决数据不一致的问题 如果现在我有四个功能模块 前三个都成功了 按照文中所示协调者已经将前三个模块数据作出修改 但此时如果第四个模块数据更新失败的话 前三个模块如何做到回滚 因为前三个模块都没有锁定数据库资源</div>2019-10-16</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/b0/b0/30b29949.jpg" width="30px"><span>愚人</span> 👍（20） 💬（0）<div>基于消息的分布式事务，所给的例子中，如果支付失败或者出货，如何触发“订单系统”回滚？此外，这里的订单，支付和仓库三个节点更像是流水线，而不是事务的概念</div>2019-11-16</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/EwmZ8EEMC0thdWskIBImYW0iaQru0qiaZQeZ3vwnD8fviauO2utUnAT9S0JTkicHjW7t2GHWjXYGDTcMeDngOCpArg/132" width="30px"><span>Geek_a1d0be</span> 👍（12） 💬（0）<div>内容较浅适合框架学习，细节还需要找更多的资料。异常处理基本没有，这些才是一个协议的精华。</div>2021-01-03</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/30/2c/3feb407d.jpg" width="30px"><span>倾听</span> 👍（12） 💬（1）<div>2pc和3pc都会存在数据不一致问题，为什么属于强一致性方案？</div>2019-11-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/82/3d/356fc3d6.jpg" width="30px"><span>忆水寒</span> 👍（9） 💬（2）<div>分布式互斥是访问某一个共享资源防止产生不一致现象。分布式事务，是保证一组命令的完整执行或完全不执行。过程来看，都是保证数据一致性的手段。但是两者又不一样，互斥不可以回退（除非发起反向新操作），事务可以回退。</div>2019-10-04</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/20/02/df2bfda9.jpg" width="30px"><span>公共号</span> 👍（5） 💬（1）<div>分布式消息中间件咋解决分布式事务回滚呢，觉得只是搞了个中间件把同步调用改成异步了，记录了状态。</div>2019-10-12</li><br/><li><img src="" width="30px"><span>Geek3340</span> 👍（4） 💬（0）<div>三阶段提交，没有拿买衣服的例子去讲每一步做了什么，只讲过程。就理解不了了。没有讲明白。下面大家问的问题，答的又不彻底。建议这篇重新讲下。用一个例子，贯穿全文。</div>2020-09-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/67/f4/9a1feb59.jpg" width="30px"><span>钱</span> 👍（4） 💬（1）<div>留言区卧虎藏龙，老师互动量不足呀！
2PC&#47;3PC&#47;BASE理论之前也学习过也许是先入为主的缘故，这节我也觉得老师讲的不太好😁
正如其他同学的疑问一样3PC的协调者，如果是个集群，单点问题是能解决，否则应该还存在？不阻塞确实说不通？</div>2020-02-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/4b/4b/97926cba.jpg" width="30px"><span>Luciano李鑫</span> 👍（4） 💬（1）<div>总结了很久，总结出来我的问题是，文中提到的两阶段提交或者三阶段提交应该算是协议层的抽象，想知道具体实现这些协议的项目中协调者和参与者分别是哪些，和他们的关系。</div>2019-10-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/17/06/7e/735968e2.jpg" width="30px"><span>西门吹牛</span> 👍（3） 💬（0）<div>对于2PC：
只要第一阶段确定了的，第二阶段一定要按照第一阶段的确定结果执行提交或者回滚，也就是说，第一阶段，如果参与者都回复YES，那么第二阶段，所有参与者必须全部提交成功，并且只能成功不能失败，要保证只能成功，就必须要有重试机制，一次不行，俩次，这个重试时间越长就会导致资源占用越久，也就说同步阻塞问题。
至于老师说的数据不一致问题，个人感觉不太准确，2PC就是保证一致性的事物协议，如果第二阶段，发送断网，或者节点故障，那么在网络恢复后，或者节点恢复后，可以根据持久化的日志，继续执行第二阶段的提交，直到成功。典型的例子：mysql日志提交就是二阶段提交，binlog和redo log，就是靠2pc解决一致性的。</div>2020-08-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/39/fa/a7edbc72.jpg" width="30px"><span>安排</span> 👍（2） 💬（1）<div>上节说到分布式共识算法是保障系统满足不同程度一致性的核心算法，那这里的2pc,3pc可以认为是一种分布式共识算法吗？
还有paxos,2pc,3pc等等，这些一致性算法都用在哪些场景呢？最主要的是paxos的应用场景有哪些？</div>2019-12-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/c0/6c/29be1864.jpg" width="30px"><span>随心而至</span> 👍（2） 💬（0）<div>老师能不能放一些参考链接放出来，或者一些引申的链接</div>2019-10-05</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTKmyjUJe2FxeyL5VMuJlpCFeJKy4SYpicbpCgyPSqbiafPlhibQT2fLWJzqV1ANSDiaSMDVTJVGyAnIow/132" width="30px"><span>wangshanhe</span> 👍（1） 💬（0）<div>2PC方式，下面有一个疑问点：
在这一阶段，首先是，协调者（Coordinator，即事务管理器，一般为应用端）会向事务的参与者（Cohort，即本地资源管理器，一般为数据库端）发起执行操作的 CanCommit 请求，并等待参与者的响应。参与者接收到请求后，会执行请求中的事务操作，将操作信息记录到事务日志中但不提交（即不会修改数据库中的数据），待参与者执行成功，则向协调者发送“Yes”消息，表示同意操作；若不成功，则发送“No”消息，表示终止操作。
问题：事务管理器，一般为应用端，那多个应用服务应用，像订单服务和库存服务，他们是去中心的，怎么去平衡一个中心节点来统一处理所有节点的执行逻辑呢，这个是怎么实现的啊？</div>2022-08-07</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/38/8a/4dd15bd9.jpg" width="30px"><span>牛不才</span> 👍（1） 💬（0）<div>确实有点看不懂这篇写的，不考虑重新讲解下这个章节吗？核心读者问到的问题，作为授业者是否应该给予解答一下。不要老回答那些大家都懂的东西！</div>2021-11-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/fd/66/e6acce29.jpg" width="30px"><span>Geek_xqu85r</span> 👍（1） 💬（2）<div>基于分布式消息的最终一致性方案。介绍里的5.6.7完全没有理解。
如果下单成功，那么下单的消息也应该发出去。后续的支付仓储和下单没有半毛钱关系了。
假设 下单，支付，仓储履约 要放到一个事务，支付的结果是怎么通过同一个mq再告诉下单呢？如果不是同一个消息
我觉得事务型消息只是保证了消息发送与本地事务的原子性。下单的本地事务提交成功，通知mq把事务消息变为可发送，到此事务性消息的事务也就结束了。然后下游业务方消费消息就好了。</div>2021-01-25</li><br/><li><img src="" width="30px"><span>voyager</span> 👍（1） 💬（0）<div>感觉讲的2PC、3PC和MQ是两个维度的事情，2PC、3PC是为了解决分布式事务。MQ是一个同步转异步的问题。且不论MQ带来的延迟影响，光是MQ如何实现实务，如何回滚操作也没有说清楚，那么如何使用MQ做到分布式一致呢</div>2020-12-31</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/66/77/194ba21d.jpg" width="30px"><span>ileruza</span> 👍（1） 💬（1）<div>在纸上记录对比了一下文中的2PC和3PC，就我个人理解：

2PC，阶段一：执行事务（锁资源），返回结果YES或NO。阶段二：收到DoCommit，提交事务（释放资源）。若协调者挂了，参与者收不到DoCommit也没超时机制，则一直不释放资源了，即同步阻塞+单点故障的问题。

3PC，阶段一，询问是否可执行，参与者检查各种状态然后返回YES或NO（相当于对协调者做出一种承诺）。阶段二，PreCommit，执行事务操作（锁资源），返回ACK。阶段三，参与者收到DoCommit，则提交事务（释放资源），若收不到DoCommit，则timeout后自动提交（为什么能大胆的提交？因为之前已向协调者承诺过YES了，并且也收到PreCommit了---说明其他节点也是承诺YES的），这表示只要有PreCommit，则资源一定会被释放，即便协调者挂了，也不会像2PC那样所有节点的资源都被锁住。
所以3PC的阶段一还是有存在的意义的，至少能做出YES的承诺，后面timeout自动提交事务时也是有足够理由的。
但若3PC的某些参与者连PreCommit都没收到？那这些节点也不会执行事务，也不会锁住资源，这就出现了数据不一致的问题

个人拙见，只是看完文章觉得这么理解是最顺的</div>2020-09-16</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/8d/c5/898b13b4.jpg" width="30px"><span>亢（知行合一的路上）</span> 👍（1） 💬（0）<div>老师对比了分布式事务的三种实现方式，分布式消息牺牲掉强一致性，增大了并发度和性能，在妥协中取得更大的收益。
老师的这种学习方法值得借鉴，对比每种方式的优劣，才能真正理解👍</div>2020-03-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/3c/74/580d5bbb.jpg" width="30px"><span>renpeng</span> 👍（1） 💬（0）<div>最后的总结表格中  3pc和2pc都有单点问题和资源锁定问题吧  为什么表格中写的是无呢</div>2020-03-06</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/19/f2/f5/46c23dd0.jpg" width="30px"><span>leechanx</span> 👍（1） 💬（0）<div>3PC的第一步为什么感觉上没什么用。。。</div>2020-01-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/09/42/1f762b72.jpg" width="30px"><span>Hurt</span> 👍（1） 💬（0）<div>老师  基于 XA 协议的二阶段提交方法，三阶段方法以及基于分布式消息的最终一致性方法  都有哪些成熟的系统 能给举几个例子吗 想了解一下</div>2020-01-07</li><br/>
</ul>