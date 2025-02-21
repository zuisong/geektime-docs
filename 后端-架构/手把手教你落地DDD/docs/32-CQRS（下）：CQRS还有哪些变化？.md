你好，我是钟敬。

上节课，我们从业务需求出发，一步步推演，学习了CQRS的基本原理。另外，我们还学习了“代码结构分离”和“数据库结构分离”两种策略。

在这两种策略中，程序仍然在同一个微服务，数据库也只有一个实例。但是，当我们遇到更高的并发性能需求时，就要考虑分布式程序和数据库了。这就是今天的两种策略要解决的问题。之后，我们还会讨论如何权衡这些策略，做出恰当的技术决策。

## 应用服务分离

我们先回顾一下[上节课](https://time.geekbang.org/column/article/633063)里，“数据库结构分离”部分的架构图。

![](https://static001.geekbang.org/resource/image/b3/5f/b3fb11bdd53747684020c488dc01265f.jpg?wh=3600x3956)

如果我们发现，使用命令的并发请求相对比较少，而使用查询的并发请求却很多，需要横向扩展才能满足性能和可用性要求，那么就可以考虑拆成两个微服务了。我们把这种策略称为“应用服务分离”。

拆分后的架构图是后面这样。  
![](https://static001.geekbang.org/resource/image/65/72/656061a78fa5cfdb3cd55a602683fe72.jpg?wh=3600x3956)

对照这张图我们可以看到，命令处理器和查询处理器原来是在同一个微服务中的，现在拆成了两个。这样，两个服务的可伸缩性就可以不一样了。例如负责处理命令的微服务可以部署在 5 个容器里，而负责处理查询的微服务部署在 10 个容器里。

另外还有一个小细节，你可以结合后面这张图看一下。

![](https://static001.geekbang.org/resource/image/61/yy/611f0feb8662f020c1ae1db97240beyy.jpg?wh=3600x3956)

在之前的组件图里，供给接口和需求接口是直接相连的。而这里使用了表示依赖的线。这两种方法都可以。如果供给和需求接口离得比较远，或者像这张图一样，两个需求接口共用一个供给接口，就可以采用依赖的形式来描述。
<div><strong>精选留言（12）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/11/1d/de/62bfa83f.jpg" width="30px"><span>aoe</span> 👍（8） 💬（5）<div>“为了实现命令而进行的查询”其实不算 CQRS 里的 Q，而是应该在命令处理器中处理，这点提醒的太及时了，不然不知道什么时候才能从迷惑中走出来</div>2023-03-03</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/f3/06/8da1bf0c.jpg" width="30px"><span>Fredo</span> 👍（4） 💬（2）<div>1. 如果查询比较简单，是不是可以直接走领域模型，而不用 Q
2. 搜索场景，canal 增量同步 ES；flink CDC 同步到数仓</div>2023-03-02</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/2a/1f/0a/3dd0cabc.jpg" width="30px"><span>黑夜看星星</span> 👍（1） 💬（2）<div>老师，请教数据库结构分离和数据库实例分离的区别</div>2023-08-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/2b/53/df/77fa7fbd.jpg" width="30px"><span>你来吧</span> 👍（1） 💬（3）<div>手把手教你落地DDD的源代码在哪里呢</div>2023-03-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/32/c2/dc/78e809b7.jpg" width="30px"><span>NoSuchMethodError</span> 👍（0） 💬（2）<div>比如领域服务中需要查询list，list中的item是聚合根，且只需要item中的部分属性，那么还需要挨个重新生成聚合根嘛</div>2023-04-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/6f/e0/ddfc33a5.jpg" width="30px"><span>胡昌龙</span> 👍（0） 💬（1）<div>钟老师，如果一个聚合如营销补贴计算。需要用到同一限界上下文里的另一个聚合 如营销补贴规则。考虑到性能，此时希望从数据库只查询出补贴规则的局部属性，是建一个新的值对象类来接收并参与运算，还是使用原来的补贴规则聚合对象类，只是对局部属性赋值呢（感觉模型重建就不完整啦）？假设新建值对象类，那如果有多种计算场景，需要用到不同的补贴规则局部属性，这样会导致建出很多的类来，这些个类放在哪里又比较合适？</div>2023-04-15</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/6f/e0/ddfc33a5.jpg" width="30px"><span>胡昌龙</span> 👍（0） 💬（1）<div>钟老师，如果一个聚合如营销补贴计算。需要用到同一限界上下文里的另一个聚合 如营销补贴规则。考虑到性能，此时希望从数据库只查询出补贴规则的局部属性，是建一个新的值对象类来接收并参与运算，还是使用原来的补贴规则聚合对象类，只是对局部属性赋值呢（感觉模型重建就不完整啦）？假设新建值对象类，那如果有多种计算场景，需要用到不同的补贴规则局部属性，这样会导致建出很多的类来，这些个类放在哪里又比较合适？</div>2023-04-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/6f/e0/ddfc33a5.jpg" width="30px"><span>胡昌龙</span> 👍（0） 💬（1）<div>钟老师，如果一个聚合如营销补贴计算。需要用到同一限界上下文里的另一个聚合 如营销补贴规则。考虑到性能，此时希望从数据库只查询出补贴规则的局部属性，是建一个新的值对象类来接收并参与运算，还是使用原来的补贴规则聚合对象类，只是对局部属性赋值呢（感觉模型重建就不完整啦）？假设新建值对象类，那如果有多种计算场景，需要用到不同的补贴规则局部属性，这样会导致建出很多的类来，这些个类放在哪里又比较合适？</div>2023-04-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/ee/3a/c0ad9c43.jpg" width="30px"><span>杰</span> 👍（0） 💬（2）<div>老师，如果是应用和数据库都不分离的情况，用cqrs是不是可以理解为我直接跟以前一样，使用表关联查询就行？</div>2023-04-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/19/fd/58/1af629c7.jpg" width="30px"><span>6点无痛早起学习的和尚</span> 👍（0） 💬（2）<div>思考题：
1. 需求一：没有说清楚累计工时信息是不是 累计工时时间？
直接 select effort_item_id,xxx effort_record where emp_id = xxx and 时间区间 group by effort_item_id

需求二：把项目表、工时项、工时记录表 join

越到后面，留言越少</div>2023-02-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/6f/e0/ddfc33a5.jpg" width="30px"><span>胡昌龙</span> 👍（0） 💬（0）<div>钟老师，如果是一个聚合（如营销补贴计算）的命令，用到同一个限界上下文另一个聚合（营销补贴规则）的查询，此时考虑到性能，希望只从数据库查询出部分补贴规则的属性，此时是创建新的补贴规则值对象，还是直接重建出带有部分属性的补贴规则聚合呢（感觉模型重建不完整）？假设创建新的值对象，那如果有多种补贴计算场景需要用到不同的补贴规则局部属性，就可能建出很多新entity出来，这些个类又放在哪里合适？感谢

备注：</div>2023-04-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/6f/e0/ddfc33a5.jpg" width="30px"><span>胡昌龙</span> 👍（0） 💬（0）<div>钟老师，如果一个聚合（如营销补贴计算）的命令逻辑，需要用到另一个聚合（如营销补贴规则）里面的少部分字段，因为并发量较高，考虑到性能希望只从数据库查询出部分字段，而不是重建整个补贴规则聚合出来，这时怎么处理合适？如果有多种补贴计算场景分别需要不同的补贴规则局部属性，是分别创建多个补贴规则的值对象，还是都用补贴规则这个领域模型实体（也就是同一个实体类），只是每次只赋需要的那几个字段的属性（感觉只重建了部分，会带来模型不完整的问题）？

备注：是命令计算里的q哈，只是q了另一个关联紧密的聚合而已</div>2023-04-14</li><br/>
</ul>