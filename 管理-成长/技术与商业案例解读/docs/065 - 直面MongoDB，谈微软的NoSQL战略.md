DocumentDB是微软于2014年推出的，基于Windows Azure的一个PaaS云产品。正如它的名字所示，这个产品是个文档数据库。它主要是冲着MongoDB的市场去的，它的数据模型和MongoDB很像。

2017年初，微软推出了和MongoDB兼容的DocumentDB的API。在2017年5月微软面向程序员的Build大会上，微软宣布DocumentDB升级为Cosmos DB。Cosmos DB包含多个数据模型，文档模型成为其子集。

**今天，我就带你回顾下这个MongoDB竞品的发展历程。**

让我们把时间线拉回2013年。那时候我还在微软，一个同事神神秘秘地宣布他要离开我们组，去投奔一个秘密项目了。和以往的各种离别不同，这个同事对于接下来转去做什么，一句话也不肯多说。事关公司机密，只是道听途说，这个秘密项目已经开发若干年，微软投入了若干人力物力。

因为我所在的组做的是经典的大数据基础架构的东西，而我同事十余年如一日地在数据库引擎上做开发，换来换去的组都是数据库引擎开发这方面的。所以我只能大概猜测，他要去的这个组做的应该也是和数据库相关的事情。我实在猜不出来，到底是一款什么样的神秘的数据库产品。

那时的数据库市场正如火如荼，大数据和NoSQL的风潮一浪高过一浪。MongoDB更是以简单易用、功能强大、服务周到，而成为很多创业者和初创企业的首选。像MongoDB这样的，基于文档而非传统关系模型的数据库，是如此受欢迎。

**那个时候的我一直有个困惑：为什么这么美好而巨大的市场，就没有人觊觎呢**？如果我是某家大公司的人，我一定会组个团队，开发一个和MongoDB一样容易卖钱的产品。

上面这两件事情一直盘旋在我脑海之中，但很长一段时间里都只是彼此孤立地存在。

然而，它们终究还是以很巧合的方式重合了。**2014年，微软正式公开了一个新的数据库——DocumentDB。**
<div><strong>精选留言（13）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/11/31/fe/30a17a9d.jpg" width="30px"><span>Leo</span> 👍（5） 💬（2）<div>飞总，咱们中小企业面对不断增长的数据，在基于MySQL的分库分表方案下，越走越坚难。请问飞总有没整体的解决方案推荐？现有的方案如使用中间件如mycat等总有这样那样的问题，有没类似greenplum这种在数据库端解决而且比较成熟的？</div>2018-07-30</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/76/ac/abb7bfe3.jpg" width="30px"><span>茉莉</span> 👍（0） 💬（1）<div>可以聊聊谷歌新发布的Cloud Firestore吗？</div>2017-10-25</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/10/82/6e7b9762.jpg" width="30px"><span>西唐王</span> 👍（2） 💬（0）<div>数据库的第一要义还是安全，如果cosmosDB能兼安全与易用于一身，那它无疑是更好的选择。</div>2018-06-19</li><br/><li><img src="" width="30px"><span>vivian</span> 👍（1） 💬（0）<div>您在微软工作过对公司有感情，但希望在这种公开课里尽量做到客观公正。前面两篇一直强调mongodb的安全性问题，这篇对CosmosDB的安全漏洞问题也希望补充一下。https:&#47;&#47;www.wiz.io&#47;blog&#47;chaosdb-how-we-hacked-thousands-of-azure-customers-databases</div>2021-09-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/0b/ab/0e2857e5.jpg" width="30px"><span>Coding小先</span> 👍（1） 💬（0）<div>如果想亚马逊，谷歌也开发了自己的文档数据库，兼容mogon，超低价甚至免费，可以更加容易的在云部署，mogon的机会有多大，毕竟云计算是一种更加基础的东西。</div>2019-11-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/2b/ec/af6d0b10.jpg" width="30px"><span>caohuan</span> 👍（1） 💬（0）<div>Azure 的Document DB听说的不多，用sql service 倒比较多</div>2018-11-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/a1/c9/501a1d02.jpg" width="30px"><span>self-discipline</span> 👍（0） 💬（0）<div>外部对手足够强大可以把自己杀死,除此之外都是自己把自己干掉了</div>2019-09-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/cc/de/e28c01e1.jpg" width="30px"><span>剑八</span> 👍（0） 💬（1）<div>主要是mongdb自身安全，事务等缺陷
这个是自己败了</div>2019-09-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/47/8c/9708a8c5.jpg" width="30px"><span>XIII</span> 👍（0） 💬（0）<div>自己软件杀自己软件 哈哈哈哈</div>2019-06-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/c3/1f/f1b88ff9.jpg" width="30px"><span>王超</span> 👍（0） 💬（0）<div>飞总怎么看cloud neutral的问题？cosmos db不能跑在aws上吧？会对他的推广有什么影响吗？感谢🙏</div>2018-11-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/57/4f/6fb51ff1.jpg" width="30px"><span>奕</span> 👍（0） 💬（0）<div>现在cosmosdb还是在azure里面吗？有没有单独发布成一个产品，可以单独下载使用的</div>2018-11-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/3f/bb/af9a920c.jpg" width="30px"><span>胡心鹏</span> 👍（0） 💬（0）<div>基础架构类 大战</div>2018-05-03</li><br/><li><img src="" width="30px"><span>hjhjjj</span> 👍（0） 💬（0）<div>不错</div>2017-10-22</li><br/>
</ul>