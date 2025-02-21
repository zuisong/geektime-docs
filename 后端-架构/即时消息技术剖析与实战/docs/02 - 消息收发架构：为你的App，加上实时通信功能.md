你好，我是袁武林。

前一篇文章中，我们从使用者的直观角度和从业者的实现维度，了解一个IM系统都应该具备哪些要素。但实际上，从我的角度来看，我更倾向于把“IM”看作是一门可以融入到各种业务系统中，为业务系统提供“实时交互”能力的技术模块。

比如，极客时间想在它的App中增加一个互动模块，支持用户点对点的实时聊天功能。那么，我们就可以相应地通过一些IM SDK的方式，快速地把即时消息的技术引入到已有的业务系统中。

同样，一个传统的视频网站如果想让自己的视频支持弹幕功能，也可以通过引入即时消息的技术，来让视频弹幕的参与者能实时、高效地和其他观看者进行各种互动。

所以，从某种程度上看，随着移动网络的快速发展以及资费的快速下降，即时消息技术也越来越多地被广泛应用到各种业务系统中，用于提升用户实时互动的能力。

那么，接下来，我们就一起从即时消息更细化的实现角度来看一看，给一个已有系统增加即时消息功能，大致上都有哪些具体工作。

![](https://static001.geekbang.org/resource/image/1c/28/1c38c735ff95d2df0ca15040394f6f28.png?wh=1965%2A1637)

如果为原有的业务系统增加实时消息模块，在不需要重建账号体系的前提下，整体上大概包括几块内容：

**一般来说首先需要制定好消息内容和未读数的存储，另外需要建立比原业务系统更加高效实时的消息收发通道，当然也包括依托第三方辅助通道来提升消息到达率。**
<div><strong>精选留言（30）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/14/6a/58/f2c6d65b.jpg" width="30px"><span>王棕生</span> 👍（114） 💬（6）<div>1. 消息存储中，内容表和索引表如果需要分库处理，应该按什么字段来哈希？ 索引表可以和内容表合并成一个表吗？
答： 内容表应该按主键消息ID来哈希做分库分表处理，这样便于定位某一条具体的消息；索引表应该按索引的用户UID来哈希做分库分表处理，这样可以使得当前用户的所有联系人都落在一张表上，减少遍历所有表的麻烦。 
        索引表可以与内容表合成一张表，好处是显而易见的，能减少拉取历史消息时的数据库IO，不好的地方就是消息内容冗余存储，浪费了空间。

2. 能从索引表里获取到最近联系人所需要的信息，为什么还需要单独的联系人表呢？
答： 如果从索引表中获取一个用户的所有联系人信息（包括最后一条聊天内容和时间）的话，SQL语句中会有分组后取top 1的操作，性能不理想； 另外当前用户与单个联系人之间的未读数需要维护，用联系人表的一个字段来存储，比用索引表方便许多。

</div>2019-08-30</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/27/79/9cf3078f.jpg" width="30px"><span>hlai</span> 👍（22） 💬（1）<div>最后张图，客户端发消息到服务是通过API， 请问为什么不可以长连接么发过去呢？</div>2019-11-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/a1/00/68ffaa02.jpg" width="30px"><span>666</span> 👍（8） 💬（1）<div>想了解一下像微博这类消息系统如果解决大V用户的消息收发的？比如用户给大v点赞、评论或者是私信</div>2019-09-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/19/1b/7f/9698e2bd.jpg" width="30px"><span>关汉聪</span> 👍（6） 💬（2）<div>老师，您的一个回复中写到：“一般会先写缓存层，缓存层都成功的情况下，如果写有索引失败的情况可以先把失败的索引先写入到一个“失败队列”，由其他线程轮询尝试来写入。一般情况下，缓存层可以抗住db重试期间的数据可用性。”
想问下，缓存一般都是缓解读压力用的，这里是为了缓解写压力，那么：
1. 缓存服务器也是要主从或者集群吗，这样每次写入都保证主从缓存都写入后，在写入DB之前，返回消息发送方，成功的ACK，对吗？
2. 如果缓存成功，索引写入DB失败，在“失败队列”被轮询的过程中，消息发送方接下来的每一条消息，为了保证消息的顺序，是不是都要等待之前失败的消息写入DB后，接下来才能发送给消息接收方？
谢谢老师。</div>2019-12-18</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTKOiapmSZbkPzGQeUWicARkgT8h3axCgSHIMp0ushSibheCj1eGiaGuC45NVxqvt9xCz1uwLD9rTAtQQg/132" width="30px"><span>Dxn</span> 👍（5） 💬（3）<div>索引表为啥要插入两条记录？插入一条也是一样的啊</div>2019-11-03</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/QD9GIbqK8mx2zu6GbHQQEemJNhudlylOeQcbom2W909zCXHW33xBhEiaHrqoqJeDX4kVjvX32AmjlMpqyxJWpkg/132" width="30px"><span>Alber</span> 👍（5） 💬（1）<div>消息存储有什么推荐的数据库吗</div>2019-08-30</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/36/4c/46c43cce.jpg" width="30px"><span>小祺</span> 👍（4） 💬（6）<div>消息表和索引表合并后表结构：
发消息用户ID ，收消息用户ID,  消息状态,  消息内容，消息类型，消息产生时间
其中消息状态 0: 正常  1:发消息用户已删除   2: 收消息用户已删除  
如果两个用户都删除消息，那这条记录就被delete掉。
既可以满足合并消息，又可以满足单个用户删除消息，请问这样设计是否可行？</div>2019-09-03</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/5c/8f/551b5624.jpg" width="30px"><span>小可</span> 👍（4） 💬（3）<div>1.由于索性表与内容表有关联，分库时两张表都应该按内容表id哈希，如果按用户id哈希，如果记录与内容不在一个库，获取消息时还要夸库查询，增加了系统复杂度，也会影响性能；
不能合并，一般IM系统都有群发消息功能，如果内容表合并到索引表，那内容数据冗余就太多了，从而占用存储空间

2.索引表与联系人表两个的功能设计不同
索引表主要存储消息历史，联系人存储用户关系，如果两个表合并，那么获取联系人时要对所有索引表消息进行聚合才能获取到，性能大大降低；另外如果进行删除联系人操作，必须要将与该联系人的所有消息删除才可以，而联系人表独立的话只许将联系人删除，历史消息可根据需求是否就行删除，当然删除历史消息就可以异步执行了</div>2019-08-30</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/19/20/1e/23e6109f.jpg" width="30px"><span>小袁</span> 👍（3） 💬（1）<div>索引表按照聊天对像的id来哈希，这样和某个对象的聊天记录可以落在一个库中，没问题。

内容表我认为可以按时间分库，实际查询时一般都是从最近的聊天记录开始往前翻，或者看某一天的记录，这样按连续时间段来查询，不会只单独看一条记录吧。

如果按消息id分库那岂不是翻某天的聊天记录可能要查好几个库了吗？</div>2019-09-07</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/9b/a8/6a391c66.jpg" width="30px"><span>geraltlaush</span> 👍（3） 💬（1）<div>之间面试被问到怎么设计存储群聊的聊天记录，保证聊天记录的有序性，没答出来，老师帮忙解答下</div>2019-09-02</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTJZuwMDaoJviaf3lZ5BOgAvTzLzmbGrMrCZ22krLSRyxpKUrVicU9pSnWsyuSHjksyNldBpXrRzUqeA/132" width="30px"><span>挨踢菜鸟</span> 👍（3） 💬（10）<div>老师，请问websocket如何多实例部署，如何解决实例重启造成连接断开的问题</div>2019-08-30</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/02/d1/36285394.jpg" width="30px"><span>🐌🐌🐌</span> 👍（2） 💬（1）<div>QQ 或者微信app上面的消息总未读数 是如何实现的，这种情况下 APP与服务器端的长连接如何应用再后台运行的话 可能已经断了？ QQ应用图标上的这个总未读数是如何获取的呢？</div>2020-03-06</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/f8/59/58a575a4.jpg" width="30px"><span>大智</span> 👍（2） 💬（1）<div>感谢老师分享。如分享中所说一条点对点消息的存储包括消息内容记录插入，双方各一条索引记录的插入，和最近联系人表的更新。如果消息内容插入其成功，其中一方索引记录插入成功，但另外一方索引记录插入失败的异常是如何处理的？多谢</div>2019-10-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/dc/c3/e4ba51d5.jpg" width="30px"><span>Flash</span> 👍（2） 💬（2）<div>老师您好，请问联系人表，不需要存最近联系人的时间吗，
最近联系人列表应该是有多条，最新的排在前面吧。</div>2019-10-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/4e/1b/f4b786b9.jpg" width="30px"><span>飞翔</span> 👍（2） 💬（2）<div>老师 在开始聊天之前大家应该先成为好友吧。好友关系 怎么存呢</div>2019-09-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/19/30/61/50e24e09.jpg" width="30px"><span>煜</span> 👍（2） 💬（1）<div>老师，那个websocket网关无状态是什么意思呀，和http无状态一样吗？长连接一般不是有状态的吗？</div>2019-09-04</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/ed/1a/269eb3d6.jpg" width="30px"><span>cfanbo</span> 👍（2） 💬（1）<div>对于内容表根据主键字段分库分表的话，如果用户查看最近一段的消息的时候，不是从多个地方分别获取数据再聚合了么，这样也有弊端的吧？</div>2019-09-02</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/f5/98/45374bb9.jpg" width="30px"><span>小小小丶盘子</span> 👍（2） 💬（3）<div>老师，我之前用两个用户id，根据某种规则生成一个唯一会话id，然后外加一个发送人id，这样索引表和内容表用一个表就可以，这么做是否可行？有什么优缺点？</div>2019-08-30</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/jXbwicoDwia7ooDfwBTRyvNYQkefnVwF1CMicMS8FqKfuFAdvVZo2pqc4ic0R9kSdHTIxaE6YyqxwX8BdNGv5PqSIw/132" width="30px"><span>kamida</span> 👍（1） 💬（1）<div>老师 我觉得索引表应该按索引的uid和另一个对话用户的uid 共同shard 因为我们的查询需求是查一个对话的历史记录 而不会是这个用户的所有历史记录 您觉得对吗</div>2020-03-15</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/75/9b/611e74ab.jpg" width="30px"><span>技术修行者</span> 👍（1） 💬（1）<div>1. 消息存储中，内容表和索引表如果需要分库处理，应该按什么字段来哈希？ 索引表可以和内容表合并成一个表吗？
内容表可以按照消息ID进行哈希处理，索引表可以按照索引用户ID进行哈希处理。

2. 能从索引表里获取到最近联系人所需要的信息，为什么还需要单独的联系人表呢？
主要是从性能方面考虑，1. 如果从索引表找联系人信息，还需要做grouo by操作，2. 如果索引表数据比较大，某一个用户的所有消息索可能会存储到不同的分表中，这样获取联系人需要跨表查询，性能更差。

问题：对于索引表进行分表分库的依据怎么设计比较合理？
1. 用户维度（某个用户的所有聊天索引记录在一张表中）
2. 会话维度（某两个用户的聊天索引记录在一张表中）
3. 时间维度（某一时间段内用户的所有聊天索引记录在一张表中）</div>2020-02-16</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/4e/1b/f4b786b9.jpg" width="30px"><span>飞翔</span> 👍（1） 💬（1）<div>老师 组聊天 应该怎么存储呀</div>2019-12-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/e0/20/003190c1.jpg" width="30px"><span>康斯坦丁</span> 👍（1） 💬（1）<div>1. 消息存储中，内容表和索引表如果需要分库处理，应该按什么字段来哈希？ 索引表可以和内容表合并成一个表吗
	用户id。
	不可以， 接收方 和 发送方 是不同的人. 有各自的业务.

2. 能从索引表里获取到最近联系人所需要的信息，为什么还需要单独的联系人表呢？	
	为了性能，如果通过索引表获取，需要进行聚合排序</div>2019-11-05</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/PiajxSqBRaELZPnUAiajaR5C25EDLWeJURggyiaOP5GGPe2qlwpQcm5e3ybib8OsP4tvddFDLVRSNNGL5I3SFPJHsA/132" width="30px"><span>null</span> 👍（1） 💬（2）<div>课后习题2：
联系人列表中，只有小部分人是聊天的高频对象，需要频繁更新联系人表数据（更新最后的聊天记录时，只是锁行记录，不会影响其他用户的更新操作），而绝大部分用户都是读多写少的情况。
另外，索引表的记录随着时间越来越多，每次都从索引表获取联系人列表，耗时也会越来越长，同时获取联系人列表，会阻塞消息写入，降低并发量。</div>2019-09-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/13/e8/08b829a9.jpg" width="30px"><span>天天平安</span> 👍（1） 💬（1）<div>老师您好，如果不想自己实现一个IM，考虑市面上收费的产品，请问哪个比较好，因为我现在急需在我们的App 上面加上聊天功能</div>2019-09-25</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/ff/3f/bbb8a88c.jpg" width="30px"><span>徐凯</span> 👍（1） 💬（1）<div>你好  请问一下  聊天内容这个表  是所有用户共用的么  如果用户特别多的话  表不就会变的很大了么</div>2019-09-15</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/72/03/da1fcc81.jpg" width="30px"><span>overland</span> 👍（1） 💬（1）<div>老师，这个消息ID一般采取什么生成的策略</div>2019-09-06</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/75/33/a1e89b84.jpg" width="30px"><span>manymore13</span> 👍（1） 💬（1）<div>老师，我做前端的，问两个后台基础问题 
1. 图中网关怎么理解？做什么用的？
2.你提的第一个问题中 应该按什么字段来哈希? 
这个哈希是用来做什么的？是确定唯一值吗？内容表不是有消息ID吗？
</div>2019-09-02</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/fe/85/9ab352a7.jpg" width="30px"><span>iMARS</span> 👍（1） 💬（1）<div>按照消息ID取模进行负载分摊，如果按照用户ID会出现分布不均的问题。其次，不建议把消息内容和索引表合并。对于消息内容存储的需求和关系型数据库不一定相同，分离后，可考虑使用非关系型数据库管理，当然会有一些运维和数据关联查询上的需求。</div>2019-09-02</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/6b/1b/4b397b80.jpg" width="30px"><span>蛮野</span> 👍（1） 💬（1）<div>以往的实践中，我们采用uid进行分表，将单个用户的所有消息记录收敛到一个表中，在查询单个用户纬度上消息避免跨表。收发双方之所以都需要采用索引，是因为可能会放到不同的分表中去，消息内容表独立，也是避免冗余存储，特别是群聊时候。常用联系人表相比消息表，一个是只记录最新记录，一个是所有记录。前者更想一个会话纬度，在客户端查询是否消息是最新，避免了查询消息表用户所有记录分组并排序。是否理解有偏差？</div>2019-09-02</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/26/d0/a8fbf2de.jpg" width="30px"><span>飞羽惊鸿</span> 👍（1） 💬（1）<div>老师，websocket如果进行分布式部署？分布式部署后服务器之间的通信采用何种方式比较合理？如果统一管理分布式服务下的所有服务</div>2019-08-30</li><br/>
</ul>