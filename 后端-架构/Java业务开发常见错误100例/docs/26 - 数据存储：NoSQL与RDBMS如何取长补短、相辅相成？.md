你好，我是朱晔。今天，我来和你聊聊数据存储的常见错误。

近几年，各种非关系型数据库，也就是NoSQL发展迅猛，在项目中也非常常见。其中不乏一些使用上的极端情况，比如直接把关系型数据库（RDBMS）全部替换为NoSQL，或是在不合适的场景下错误地使用NoSQL。

其实，每种NoSQL的特点不同，都有其要着重解决的某一方面的问题。因此，我们在使用NoSQL的时候，要尽量让它去处理擅长的场景，否则不但发挥不出它的功能和优势，还可能会导致性能问题。

NoSQL一般可以分为缓存数据库、时间序列数据库、全文搜索数据库、文档数据库、图数据库等。今天，我会以缓存数据库Redis、时间序列数据库InfluxDB、全文搜索数据库ElasticSearch为例，通过一些测试案例，和你聊聊这些常见NoSQL的特点，以及它们擅长和不擅长的地方。最后，我也还会和你说说NoSQL如何与RDBMS相辅相成，来构成一套可以应对高并发的复合数据库体系。

## 取长补短之 Redis vs MySQL

Redis是一款设计简洁的缓存数据库，数据都保存在内存中，所以读写单一Key的性能非常高。

我们来做一个简单测试，分别填充10万条数据到Redis和MySQL中。MySQL中的name字段做了索引，相当于Redis的Key，data字段为100字节的数据，相当于Redis的Value：
<div><strong>精选留言（19）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/13/71/05/db554eba.jpg" width="30px"><span>👽</span> 👍（30） 💬（1）<div>其实，具体使用何种数据库，如果了解其原理，那就很容易弄懂了。
我就说说ES，
ES，因为其本身全文索引，和复杂查询的高性能，最主要还是依赖于其分词之后简历的映射表。基本可以理解为类似数据库索引一样的存在。索引的弊端，也就是ES的弊端。
索引，基本目的是空间换时间，用一些冗余的节点数据来优化查询性能。但是带来的问题，一方面是空间的占用，以及维护索引所需要的成本。因为需要维护索引，所以删改数据时性能较差。
ES的索引又更加过分，几乎是针对单个文章的全部内容，建立了分词映射，修改一篇文章内容，可能会大幅度修改映射内容。所以不适合频繁修改的数据。
</div>2020-05-15</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/79/01/e71510dc.jpg" width="30px"><span>hellojd</span> 👍（22） 💬（1）<div>老师没说mongo数据库，我的理解是如果不是acid要求特别高的地方，都可以将mysql替换为mongo.不知道理解对不对。</div>2020-05-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1e/13/87/73a17c60.jpg" width="30px"><span>似曾相识</span> 👍（8） 💬（1）<div>老师 Infludb,和es 这些数据库做辅助数据库，需要保存全量数据吗？还是根据业务保存部分字段？</div>2020-05-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/74/8a/d5b0cf30.jpg" width="30px"><span>kyl</span> 👍（6） 💬（2）<div>说一下我对mongodb的理解，望老师指正。mongodb因为是文档型数据库以json格式存储，所以可以很方便的存储各种类型的数据，同时mongodb横向扩展只需增加分片比MySQL更加方便，数据量很大的场景下感觉性能优于MySQL。但是mongodb对事务支持比较差，虽然4.0引入了事务，但是可能有坑，另外mongodb不支持表的关联查询，所以还是要根据实际业务场景进行选择。</div>2020-05-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/9c/c6/05a6798f.jpg" width="30px"><span>苗</span> 👍（5） 💬（1）<div>MongoDB 4.2.x提供了相当于关系数据库RR的事务隔离级别；好像也能用于交易数据强acid的需求。感觉用数组字段处理简单的一对多关系很方便。</div>2020-09-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/1c/6e/6c5f5734.jpg" width="30px"><span>终结者999号</span> 👍（5） 💬（1）<div>老师，我想问一下对于一个高并发的系统，索引库您们保存多长时间呢？没有夜维清理吗？</div>2020-05-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/24/2a/33441e2b.jpg" width="30px"><span>汝林外史</span> 👍（5） 💬（1）<div>又是干货满满，很多新接触的东西，感谢老师。
对于Mysql擅长的地方的第二点不是很理解：
   1.不是不建议设置外键吗？ 
   2.专门弄个索引表放主键与外键的关联关系，那岂不是每张表都要配这么一个索引表，这不浪费内存吗？
   3.主键跟关联表是一对多的关系，那这个索引表相对数据表的数据量岂不是几倍的关系，性能能好了吗？
还请老师指教。</div>2020-05-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/96/b5/d09a53c7.jpg" width="30px"><span>永夜</span> 👍（2） 💬（1）<div>老师你好，我们这边主要做一些交互式数据可视化系统，目前用的主要是postgres数据库，但是一旦数据量比较大，几百万条的数据的一些过滤统计都会比较慢，需要20~30s，我们也需要用到数组，json这样的特殊类型，不知道有没有其它的数据库或者框架能提高这种场景下的效率问题。</div>2020-05-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/7a/b9/c3d3a92f.jpg" width="30px"><span>G小调</span> 👍（2） 💬（2）<div>老师 有个疑问❓ 你图里写的mysql索引库 是指表上建立了索引的库吗</div>2020-05-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/8f/cf/890f82d6.jpg" width="30px"><span>那时刻</span> 👍（1） 💬（1）<div>请问老师，文章提到的多数据库系统例子里，redis写入是怎么实现的呢？</div>2020-05-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/8f/cf/890f82d6.jpg" width="30px"><span>那时刻</span> 👍（9） 💬（3）<div>我说说个人对于MongoDB的理解，它的优势：
1.schema free，不需要额外定义列名，每个文档的key需要一致。
2.对于json结构存储和读取方便，比如取json某个key的value比较方便。相对于mysql存储json需要序列化和反序列化操作。
3.查询来看，3.0之后的mongo采用了B+树和LSM两种方式，来优化读多写少和写多读少情况。

劣势：
1. schema free，是双刃剑，如果某个字段并不是所有文档里存在，查询是个麻烦事。
2.不支持事务
3.为了向RDBMS靠拢，通过冗余字段来实现。实践起来不是很方便。</div>2020-05-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/87/a4/bd373a4a.jpg" width="30px"><span>fly12580</span> 👍（6） 💬（0）<div>redis还可以用来做分布式并发锁。</div>2020-05-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/10/bb/f1061601.jpg" width="30px"><span>Demon.Lee</span> 👍（6） 💬（6）<div>现在公司的业务对ACID没有那么高的要求，已经全部换成了NoSQL，主要就是MongoDB+Redis+ES，自从用了MongoDB，我感觉解脱了，再也不用去设计一堆关联的表了，字段的扩充或变化都没有什么影响，字段取值的检验全部在应用程序中解决，有点不爽是，写各种复杂查询和统计时没有写rdms的sql那么溜。另外就是，我们使用了Keys去redis查询所有相关的数据，一般数据量不大，但是我一直想优化下，今天老师又提了，必须优化了。</div>2020-05-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/19/1c/74/eb472cc3.jpg" width="30px"><span>海强</span> 👍（1） 💬（0）<div>做的一个政府项目，权限要求严格，数据权限采用行级白名单机制(名单是系统根据各种条件自动维护的)，白名单里面又涉及角色，个人和群组。用户和数据量都挺大的时候，白名单表特别大。列表查询(需要权限过滤)时候走数据库，各种索引和优化性能仍然达不到要求。
后面换成在es里面查，但是列表查询需要最新的数据，只好把数据更新推es做成同步的，数据的更新还比较频繁。
总结就是数据量大</div>2020-12-03</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/j5ld8j7BqIZe9fOVniaLJajbOwbnwKD7dn3RN5T79K00uy1utB7PTP7TiclxdhXyh4ER8hsu8mgnibUoIDaRwib4kg/132" width="30px"><span>刘飞</span> 👍（1） 💬（0）<div>mongdb 更好的应用场景呢》？</div>2020-09-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/dd/6e/1479ce4f.jpg" width="30px"><span>CoderWang</span> 👍（1） 💬（0）<div>我来说说个人对mongodb的理解，很多人之前对mongodb理解是不支持事物或者若事物，但是在4.0之后特别在最新版本4.2之后对事物支持很好了。而且mongodb是json格式存储，非常方便灵活对数据结构存储，比如数组类型。在加入aggregate之后对聚合管道查询非常方便，对数据统计分析特别大帮助。个人理解，谢谢</div>2020-06-09</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/DYAIOgq83ersGSic8ib7OguJv6CJiaXY0s4n9C7Z51sWxTTljklFpq3ZAIWXoFTPV5oLo0GMTkqW5sYJRRnibNqOJQ/132" width="30px"><span>walle斌</span> 👍（0） 💬（0）<div>1）我这边自研的统一消息推送引擎，底层所有的推送记录，会经过本地定时缓冲区，批量写入到mongo中。。主要是需要提供分页，可扩展字段【要允许业务定制自己的字段】，主要对内使用，所以写入量大，但是查询量不大。
2）然后再自研统一清库策略，批量小步删除一定时间之前的数据，删除是物理删除或者导入到公司内的phoenix中。
3）自研背后数据展示页面。中间会由于多项目资源隔离，所以还要把历史推送项目引入独立jar包开启固定接口，然后配置页面不同的jv 会默认路由到不同的数据展示。
4） 对测试人员提供同样逻辑接口。辅助其自动化脚本的完成
基本上从头到尾都有辅助。而做业务研发的同学，只需要引入推送引擎实现必须的几个业务内容，然后就OK了。</div>2021-07-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/dd/19/45afa234.jpg" width="30px"><span>🐛🐛</span> 👍（0） 💬（0）<div>hbase算是什么样类型的NoSQL呢</div>2021-05-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/19/1c/74/eb472cc3.jpg" width="30px"><span>海强</span> 👍（0） 💬（0）<div>数据量大，更新频繁，还需要查实时列表的场景有什么解决方案？有没有异步写es，但是查询时候对没来及进es的数据进行数据库查询补偿之类的方案</div>2020-12-03</li><br/>
</ul>