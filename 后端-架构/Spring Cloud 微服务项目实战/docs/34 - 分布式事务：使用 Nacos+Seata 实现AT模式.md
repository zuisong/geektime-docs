你好，我是姚秋辰。

在上一节中我们已经搭建了Seata Server，这节课我们就来动手落地一套Seata AT方案。Seata AT不仅是官方最推荐的一套分布式事务解决方案，也是大多数Seata使用者选用的方案。AT方案备受推崇，一个最主要的原因就在于省心。

Seata AT可以给你带来一种“无侵入”式的编程体验，你不需要改动任何业务代码，只需要一个注解和少量的配置信息，就可以实现分布式事务。这似乎听上去有那么点玄幻，如果一个分布式方案既不依赖XA协议的长事务方案，又不依赖代码补偿逻辑，那碰到Rollback的时候它怎么知道该回滚哪些内容呢？

下面我就通过一个实际的业务模型，带你了解一下AT方案的底层原理。

## Seata AT底层原理

我们以“删除券模板”作为落地案例，它需要Customer和Template两个服务的共同参与。其中Customer服务是整个业务的起点，它先是调用了Template服务注销券模板，然后再调用本地方法注销了由该模板生成的优惠券。说白了，我们就是在两个不同的微服务中，分别使用Update SQL语句修改了底层数据。

我们接下来就基于“删除券模板”场景，看一下Seata AT背后的业务流程。在开始之前，我需要先花点时间带你认识下Seata框架的三个重要角色，TC、TM和RM。
<div><strong>精选留言（14）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/15/bc/e1/cb5ffddf.jpg" width="30px"><span>药味</span> 👍（12） 💬（5）<div>怎么理解&quot;传统的事务型消息 + 日志补偿 + 跑批补偿的方式&quot;</div>2022-03-02</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/24/4d/f5/2e80aca6.jpg" width="30px"><span>奔跑的蚂蚁</span> 👍（5） 💬（4）<div>大佬，能加个餐 详情说下 传统的方式嘛，最好再说点rocketMq</div>2022-03-02</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/24/4d/f5/2e80aca6.jpg" width="30px"><span>奔跑的蚂蚁</span> 👍（4） 💬（1）<div>今天用seata 遇到一个问题，没有配置代理数据源 好像也能使用，请问下老师 这个和配置数据源在使用上有什么区别嘛</div>2022-03-15</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/25/87/f3a69d1b.jpg" width="30px"><span>peter</span> 👍（3） 💬（2）<div>请教老师几个问题啊：
Q1：undo_log问题：
A undo_log是文件还是数据库的表？从文中看，似乎是数据库的表。B 如果是表的话，该表由seata框架自己创建并维护，不需要开发人员维护，对吗？
Q2：RM是怎么监测到业务代码的DB操作的？
既然seata AT方案是无感知的，那seata框架又是怎么知道业务代码做了哪些DB操作？
Q3：阶段二回滚的时候，RM 无法获取本地锁，它会原地打转不停重试。一直处于这个状态吗？这样岂不是相当于死机了？
Q4：阶段一，每个本地事务会提交或回滚吗？
每个本地事务不都是在阶段二执行提交或回滚吗？
Q5：能否单独讲一讲&quot;“传统的事务型消息 + 日志补偿 + 跑批补偿的方式”？ 比如以加餐形式写一章？</div>2022-03-02</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTLz44WGtTHNfNiaficzyiasJAQgLcSh6cVLsTpczlXxIlbBXNhAT1qKbM4OZRpcWP56KAp2fHiaJVsKGw/132" width="30px"><span>Geek_eabafe</span> 👍（0） 💬（1）<div>姚老师，阶段二是全局事务的 Commit 和 Rollback 是异步执行。
1. 这里的异步执行是指哪里异步呢？
2. 如果异步执行失败了 TC 仍认为整个事务已经结束了吗？ 如果是这样 肯定有脏数据的
</div>2024-01-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/18/7b/03/03583011.jpg" width="30px"><span>天天有吃的</span> 👍（0） 💬（1）<div>请问下，阶段二是全局事务的 Commit 和 Rollback 是异步执行。这里的异步执行是指哪里异步呢？</div>2023-11-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/18/7b/03/03583011.jpg" width="30px"><span>天天有吃的</span> 👍（0） 💬（1）<div>请问下这里支持的 db 回滚有哪些db呀？hbase mongo这些也都支持吗</div>2023-11-08</li><br/><li><img src="" width="30px"><span>Geek_bf202a</span> 👍（0） 💬（1）<div>timestamp&quot;: &quot;2023-10-18T14:34:46.564+00:00&quot;,
    &quot;status&quot;: 500,
    &quot;error&quot;: &quot;Internal Server Error&quot;,
    &quot;message&quot;: &quot;Executing an update&#47;delete query; nested exception is javax.persistence.TransactionRequiredException: Executing an update&#47;delete query&quot;,
    &quot;path&quot;: &quot;&#47;coupon-customer&#47;template&quot;
}
请求总是报这个啊，老师</div>2023-10-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/19/b8/09/62f74df5.jpg" width="30px"><span>Amy</span> 👍（0） 💬（1）<div>老师，请教下几个问题
1.RM执行第一阶段完成，是不是可以理解为对于mysql来说已经执行了commit，只是在undo_log表中记录了回滚的数据，第二阶段依赖这个数据对数据进行还原
2.基于问题1，如果RM1执行了一个update操作，比如把id=1的姓名从张三更新了李四，那RM2，第一阶段还没执行完，此时有其他的业务B去查id=1的数据，取出的名字是李四，然后RM2执行失败，触发了RM1的回滚操作，这个时候业务B查的不就是错误数据了吗</div>2023-05-16</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/26/71/0d/4dc04ac8.jpg" width="30px"><span>Q</span> 👍（0） 💬（1）<div>老师customer调template卡流程了，脑壳痛
template服务启动一直报 ERROR [coupon-template-serv,,] 21120 --- [  main] i.s.c.r.netty.NettyClientChannelManager  : no available service &#39;null&#39; found, 这个错
customer调template的时候报这个错Request processing failed; nested exception is org.springframework.orm.jpa.JpaSystemException: Unable to commit against JDBC Connection; nested exception is org.hibernate.TransactionException: Unable to commit against JDBC Connection] with root cause，我查了下是jpa和seata在强数据库资源，</div>2022-06-25</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/17/06/7e/735968e2.jpg" width="30px"><span>西门吹牛</span> 👍（0） 💬（1）<div>本地锁该如何理解呢？</div>2022-06-02</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/18/7b/03/03583011.jpg" width="30px"><span>天天有吃的</span> 👍（0） 💬（0）<div>这个图中，tm也是rm吗
</div>2023-11-09</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/DYAIOgq83erwIgbTd3oy4ESHr6bX9iblONuwgU0MWHcgxndWwNNRQGXlhicduummSiamfTcxHsicicxR4nElxzj280Q/132" width="30px"><span>Geek_5c44aa</span> 👍（0） 💬（0）<div>可不可以不使用Nacos，直接Kubernetes、Redis和Seata一起的？</div>2023-10-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1f/05/63/dd59ad18.jpg" width="30px"><span>加油加油</span> 👍（0） 💬（0）<div>您好，请教下，使用了@GlobalTransactional 之后，有没有对应的全局事务钩子方法，比如说传统的本地事务@Transaction 对应的钩子是 TransactionSynchronizationManager.registerSynchronization  那么全局事务有类似的机制吗 ？</div>2023-08-16</li><br/>
</ul>