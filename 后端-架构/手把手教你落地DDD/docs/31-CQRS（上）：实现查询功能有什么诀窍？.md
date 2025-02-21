你好，我是钟敬。

前面几节课我们讲完了限界上下文。接下来的两节课，我们将学习一个和查询功能相关的模式——CQRS。虽然 《领域驱动设计》原书里没有这个模式，但近年来，CQRS 常常和 DDD 结合使用。

不过也有人对 CQRS有不同意见。这是因为，CQRS 实际上也有不同的变化，这就造成了不同的人对 CQRS 的理解也不太一样。学完这两节课，我想你就知道怎么分辨了。

CQRS 是 Command Query Responsibility Segregation 的简称，中文是 “命令查询职责分离”。这个名字乍听起来也不太好理解，咱们还是从业务需求开始，一步一步地理解。

## 查询功能遇到的问题

在第三个迭代中，在工时管理上下文，增加了更多的查询和统计需求。

我们先看一个简单的需求，给定一个工时项，要求查询出这个工时项下的所有工时记录，并显示在屏幕上。要求每条返回记录的字段包括“员工号”“员工姓名”“日期”“工时”和“备注”，并根据员工号和日期升序排序。为了简化问题，我们先不考虑“不在本级报工时”以及“父子工时项”的问题。

我们回忆一下工时项管理的领域模型。

![](https://static001.geekbang.org/resource/image/6a/66/6a7c2bd3bc372920b99f6e2a97cfbf66.jpg?wh=3118x2324)

根据之前学习的数据库设计以及上下文映射的方法，假定我们选择的是在本地建立员工表，并从“基础信息管理”上下文映射**员工**信息的策略。那么本地数据库会有**员工**（emp）表和**工时记录**（effort\_record）表。
<div><strong>精选留言（12）</strong></div><ul>
<li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTJIocn8OMjfSGqyeSJEV3ID2rquLR0S6xo0ibdNYQgzicib6L6VlqWjhgxOqD2iaicX1KhbWXWCsmBTskA/132" width="30px"><span>虚竹</span> 👍（6） 💬（4）<div>还有一种常用方式，是写到mysql里，异构到mongo里一份用来查询，</div>2023-02-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/28/cb/c5/c1d7ca5e.jpg" width="30px"><span>赵晏龙</span> 👍（4） 💬（3）<div>好多人都觉得CQRS就一定是EventSourcing，就一定是两个库。我也是去年的时候突然顿悟，其实CQRS的本质就是冗余。
1、我会考虑进一步抽象，甚至查询模型直接记录统计的最终数据。
2、分表能够分离变与不变的东西，但会增加额外的数据同步开发工作和认知负载，如果加上历史数据的迁移，工作量会越来越多。不分表会影响领域的相对不变性，但是认知负载可能会相对较低。这将会是一个权衡，没有银弹。</div>2023-03-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/15/69/187b9968.jpg" width="30px"><span>南山</span> 👍（3） 💬（1）<div>查询的代码中 repository放在了application层，依赖dto，这里的repository跟领域层的那个是什么关系？或者是两个吗？</div>2023-03-04</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/f3/06/8da1bf0c.jpg" width="30px"><span>Fredo</span> 👍（2） 💬（2）<div>1. 单独搞一张宽表，冗余存用来查询呢。如果是报表可能会这样做
2. 直接在原先的表上弄会有一定的风险，数据一致性要特别关注；维护两套的话，关注点分离，职责清晰，但维护成本上去了。</div>2023-03-02</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/1d/de/62bfa83f.jpg" width="30px"><span>aoe</span> 👍（1） 💬（1）<div>我们大部分让人头疼的统计数据，就是独立一张表存储的，单表查询出结果，遇到数据有问题时，重新计算一遍。
相比复杂的连表查询，这种方式轻松愉快，实现简单，额外支出的存储空间值了：空间换时间</div>2023-03-01</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/22/b0/050676f5.jpg" width="30px"><span>樱花</span> 👍（0） 💬（1）<div>emp和emp_effort_record算一个聚合里的对象吗？
或者说一个repo可以跨聚合查询吗</div>2024-08-06</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1a/89/3e/0dd8e96b.jpg" width="30px"><span>InfoQ_小汤</span> 👍（0） 💬（1）<div>如果执行cqrs拆封 这个时候某些增删改的逻辑是需要查询作为辅助的 这个时候做领域逻辑 是不是还会涉及到查询dto跟领域对象的转换处理场景</div>2024-06-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/05/81/22fdfc58.jpg" width="30px"><span>周昌武</span> 👍（0） 💬（1）<div>如果后续查询需求变化，需要新增显示字段，冗余的 emp_effort_record是不是就变得鸡肋了？这种情况有哪些解决方案？
1. 提前考虑emp_effort_record表多冗余些字段（存在未来变化不确定性，虽然是降低了）
2. 需求变化时emp_effort_record添加新字段，同时修改同步方案（可能需要补历史数据，根据对历史数据显示要求而定）

钟老师还有其他好的方案吗</div>2024-03-05</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/17/99/5a/32f3df3c.jpg" width="30px"><span>无问</span> 👍（0） 💬（1）<div>cqrs的模型转换要另外在弄一套builder了嘛</div>2023-10-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/3c/81/7ccdb399.jpg" width="30px"><span>+ 糠</span> 👍（0） 💬（3）<div>
cqrs没有领域层，会不会以后服务根据聚合拆分，改起来也比较麻烦？</div>2023-06-30</li><br/><li><img src="" width="30px"><span>雨</span> 👍（0） 💬（1）<div>问题1：先查询出符合条件的父子工时项id，再用多个工时项id进行查询
问题2：原来领域模型表反规范化的方式避免了2套数据源同步的复杂度，增加了写逻辑的复杂度，另外一套表的方式关注点清晰，能实现业务层的读写分离，但需要保证数据同步的稳定性及时效性
还请老师答疑，谢谢</div>2023-05-16</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1b/85/67/0d121bc4.jpg" width="30px"><span>神经蛙</span> 👍（0） 💬（1）<div>除了博主这篇文章的观点之外，我还有一种理解，修改会对一个对象产生影响，属于业务。而查询没有业务属性，它只是查询出某一时刻内某个领域实体对象的状态。所以把他们分离能更好的让开发关注到业务上去。但是我觉得cqrs这样拆好繁琐。ddd本身落地就够繁琐的了。。</div>2023-03-03</li><br/>
</ul>