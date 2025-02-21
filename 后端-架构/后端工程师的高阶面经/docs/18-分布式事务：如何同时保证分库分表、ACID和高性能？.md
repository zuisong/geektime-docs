你好，我是大明。

我们在把单库拆分成为分库分表之后，一个巨大的挑战就是**本地事务变成了分布式事务**。事实上，即便没有分库分表，在微服务架构之下我们也还是会面临分布式事务的问题。所以，在学习了微服务架构又学习了分库分表之后，是时候深入讨论一下分布式事务了。

分布式事务在面试中是一把双刃剑，用得好，那么会是一个非常强的加分项。但是如果你基础不够扎实，见闻不够广博，面分布式事务很容易翻车，所以熟练掌握分布式事务很重要。

希望你学完这节课的内容之后可以自信地在简历里写上精通分布式事务这一条，提高简历通过筛选的几率，同时也在面试过程中刷出亮点，给面试官留下深刻印象。

## 前置知识

关于分布式事务，首先你需要弄清楚一个东西，就是分布式事务既可以是纯粹多个数据库实例之间的分布式事务，也可以是跨越不同中间件的业务层面上的分布式事务。前者一般是分库分表中间件提供支持，后者一般是独立的第三方中间件提供支持，比如 Seata。你在面试的时候，要根据上下文确定面试官问你的分布式事务是哪一类，然后有针对性地回答。

要学习分布式事务，我们要先学习分布式事务中几个比较常用的协议。

### 两阶段提交

两阶段提交协议（Two Phase Commit）是分布式事务中的一种常用协议，算法思路可以概括为参与者将操作成败通知协调者，再由协调者根据所有参与者的反馈情况决定各参与者要提交操作还是中止操作。
<div><strong>精选留言（12）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/28/44/cf/791d0f5e.jpg" width="30px"><span>ZhiguoXue_IT</span> 👍（4） 💬（2）<div>业界内落地实用基本都是mq保证最终一致性，但是据说银行系统是强一致性，作者认为呢</div>2023-07-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/45/b9/3db96ade.jpg" width="30px"><span>锅菌鱼</span> 👍（3） 💬（1）<div>saga的反向补偿和AT的undolog是差不多的吧？</div>2023-10-20</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/prPcXJuVeEQc8FJejyLqOH7hbXicozicbVcic3L3ia493ialSRB8bE0vhjjykbzhEbT6kU9Tj4zXstlJeJCuShJiaicCQ/132" width="30px"><span>程序猿佬鸟</span> 👍（0） 💬（1）<div>老师您好：
Q1: 延时事务在分库分表中间件中有实现吗？ 您能具体说一个方向吗？ 看完您这章我有点蒙圈了</div>2024-01-28</li><br/><li><img src="" width="30px"><span>Geek_3d0fe8</span> 👍（0） 💬（3）<div>那个TCC如果confirm失败了，为什么只能进行重试呢？ 调 cancel 不行吗</div>2023-12-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/2a/44/e6/2c97171c.jpg" width="30px"><span>sheep</span> 👍（0） 💬（1）<div>延迟事务有哪些中间件实现了呢？实际开发中要操作的话，我们该怎么操作</div>2023-11-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/2a/44/e6/2c97171c.jpg" width="30px"><span>sheep</span> 👍（0） 💬（1）<div>老师这里有几个问题[嘿嘿]
问题1: TCC 另外一个方案中，进行丢掉这个数据，这里图片好像没有看到丢掉这个流程耶
问题2: AT事务下会帮你生成反向操作。有哪些分布式事务中间件支持这种反向操作呀
问题3: 业务A调用业务B，业务A根据业务B的执行情况来确定是继续执行，还是回滚，这种也属于分布式事务么
问题4：并发高的业务，分布式事务频繁失败情况下，会不会导致不一致的情况越来越严重？虽然有自动修复进行缓解。

其他的：
“也就是把话题引导到延迟事务这个方案方案上”，是不是多了一个“方案”两个词
“只有db_2上开启的事务用上了”图片这里应该是db_1吧</div>2023-11-08</li><br/><li><img src="" width="30px"><span>Geek8004</span> 👍（0） 💬（1）<div>自动故障处理的机制不是很明白.针对这句话“修复数据本身分成两种，一种是用已经提交的数据库的数据来修复没有提交成功的数据库的数据；另外一种则是用没有提交成功的数据库的数据来还原已经提交的数据库的数据。 ”只有一份数据,假如我db1 rollback失败,此时db0之前已经提交了数据,我怎么用已提交的数据修复未提交的?他们数据没有冗余呀</div>2023-08-30</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/25/87/f3a69d1b.jpg" width="30px"><span>peter</span> 👍（0） 💬（1）<div>请教老师几个问题：
Q1：根据文章内容，不管哪种分布式事务解决方案，都做不到ACID，都无法保证不出问题。那么，在实际的应用中，分布式事务的成功率一般能达到多少？
Q2：AT是概念还是具体框架？
Q3：单库但有分表，是否存在分布式事务？
Q4：两个SQL可以共用一个事务，前提是这两个SQL是属于一个Session吗？不同Session的SQL不能共用一个事务吧。
Q5：对数据库进行修复会影响业务吗？如果会影响，会采取哪些措施？</div>2023-07-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/2d/90/3b/791d0f5e.jpg" width="30px"><span>进击的和和</span> 👍（0） 💬（1）<div>老师你好 协调者让参与者执行事务，但是并不提交，协调者返回执行情况 这里是不是参与者返回执行情况呢。  我在两阶段提交那里说到在提交阶段，协调者会不断重试直到把 Commit 请求发送给协调者；协调者如果在提交阶段中途崩溃，也要确定是否需要提交或者回滚。那么你就应该可以理解，在重试成功之前，或者在协调者恢复过来重新提交或者回滚之前，数据是不一致的。这句话好像有点小问题吧。  两阶段提交如果a参与者成功了,b参与者失败了,那么是不是只能人工处理或者有个修复数据的脚步进行修复呢?  关于容错,如果协调者挂了,那么参与者1是否可以询问其他参与者情况呢</div>2023-07-26</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/prPcXJuVeEQc8FJejyLqOH7hbXicozicbVcic3L3ia493ialSRB8bE0vhjjykbzhEbT6kU9Tj4zXstlJeJCuShJiaicCQ/132" width="30px"><span>程序猿佬鸟</span> 👍（1） 💬（0）<div>延迟事务？sharding JDBC也没有实现啊</div>2024-01-28</li><br/><li><img src="" width="30px"><span>aabb</span> 👍（0） 💬（0）<div>“准备阶段任何一个节点执行失败了，就都会回滚。全部执行成功就提交”，应该是提交阶段吧</div>2024-12-06</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/17/4a/c7/0cff4a59.jpg" width="30px"><span>木木夕</span> 👍（0） 💬（0）<div>延迟事务，听都没听过，有哪些中间件实现了？</div>2023-10-04</li><br/>
</ul>