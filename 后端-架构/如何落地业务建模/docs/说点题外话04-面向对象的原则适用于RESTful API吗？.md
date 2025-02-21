你好，我是徐昊。今天我们再来专门说点题外话。

前面几期题外话都比较偏向于提供一种不同的角度，主要是因为你们也并没有针对课程的内容，提出什么特别的问题需要我来具体回答。那么作为我们在进入新约前的最后一篇题外话，我想聊一聊关于RESTful API的问题。

我记得有位同学在留言区问了这样一个问题：过长的URI是否破坏了迪米特法则（Law of Demeter）。这里我们就要搞清楚，什么是迪米特法则呢？

迪米特法则又叫最小可知法则，指的是**在面向对象设计中，实体应尽可能少地与其他实体发生交互**。为了说明什么是“少的交互”，我们还特别归纳了一组可以认为不违反迪米特法则，并且可以直接调用的对象：

- 当前对象自己（this，self）；
- 以参数形式传入的对象，比如函数的形参（parameter）；
- 当前对象内实例变量引用的对象（instance variable）；
- 如果实例变量是集合，那么集合中的对象也可以访问（collection，aggregration）；
- 由当前对象创建的对象（variable declaration in function）。

那么这些场景适用于RESTful API调用的场景吗？显然并不太适用。因为在RESTful API的场景中，实体只有客户端和API提供者，而API提供者的内在结构都被API层屏蔽了。所以无论怎么调用，都不会出现对于API提供者内部结构的依赖。
<div><strong>精选留言（6）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/13/ce/04/c324a7de.jpg" width="30px"><span>邹溪源</span> 👍（2） 💬（1）<div>接口无处不在，而良好的设计则更显得非常重要。基于restful的架构风格设计接口，相比传统的http风格设计的接口，更易于引入面向对象的程序设计。这种设计也成为实践单一职责原则的练兵场。
而有了接口，也使得依赖倒置成为一种基本操作。</div>2021-07-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/18/3f/fe/35d1afbd.jpg" width="30px"><span>阿鸡</span> 👍（1） 💬（1）<div>想请问下SOA能使用面向对象的原则吗？ 还是只能在服务内部面向对象，在服务边界还是传统的DO加XxService的形态</div>2021-08-01</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/5e/32/1ccb2b7c.jpg" width="30px"><span>海连天</span> 👍（2） 💬（0）<div>老师怎么看GraphQL</div>2022-03-03</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/9b/28/fec0aaf4.jpg" width="30px"><span>老敖</span> 👍（0） 💬（0）<div>“比如通过超媒体明确地表示资源之间的关联，而不是依靠客户端去拼凑 URI。如果客户端可以拼凑出 URI，则表明客户端对于 API 提供者的内在逻辑存在依赖。而通过 HATEOAS，把所有关联的链接直接提供，就避免了暴露内在的逻辑。”这段话多少有点耍流氓了，按这个逻辑，不穿衣服上街就没人能强奸我了？</div>2022-12-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/1d/de/62bfa83f.jpg" width="30px"><span>aoe</span> 👍（0） 💬（0）<div>原来 RESTful 还有一个 HATEOAS
</div>2022-04-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/18/7c/25/70134099.jpg" width="30px"><span>许凯</span> 👍（0） 💬（0）<div>功能和配置一致、单一、完整、正交</div>2021-11-01</li><br/>
</ul>