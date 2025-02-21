关系数据库经过几十年的发展后已经非常成熟，强大的SQL功能和ACID的属性，使得关系数据库广泛应用于各式各样的系统中，但这并不意味着关系数据库是完美的，关系数据库存在如下缺点。

- 关系数据库存储的是行记录，无法存储数据结构

以微博的关注关系为例，“我关注的人”是一个用户ID列表，使用关系数据库存储只能将列表拆成多行，然后再查询出来组装，无法直接存储一个列表。

- 关系数据库的schema扩展很不方便

关系数据库的表结构schema是强约束，操作不存在的列会报错，业务变化时扩充列也比较麻烦，需要执行DDL（data definition language，如CREATE、ALTER、DROP等）语句修改，而且修改时可能会长时间锁表（例如，MySQL可能将表锁住1个小时）。

- 关系数据库在大数据场景下I/O较高

如果对一些大量数据的表进行统计之类的运算，关系数据库的I/O会很高，因为即使只针对其中某一列进行运算，关系数据库也会将整行数据从存储设备读入内存。

- 关系数据库的全文搜索功能比较弱

关系数据库的全文搜索只能使用like进行整表扫描匹配，性能非常低，在互联网这种搜索复杂的场景下无法满足业务要求。

针对上述问题，分别诞生了不同的NoSQL解决方案，这些方案与关系数据库相比，在某些应用场景下表现更好。但世上没有免费的午餐，NoSQL方案带来的优势，本质上是牺牲ACID中的某个或者某几个特性，**因此我们不能盲目地迷信NoSQL是银弹，而应该将NoSQL作为SQL的一个有力补充**，NoSQL != No SQL，而是NoSQL = Not Only SQL。

常见的NoSQL方案分为4类。

- K-V存储：解决关系数据库无法存储数据结构的问题，以Redis为代表。
- 文档数据库：解决关系数据库强schema约束的问题，以MongoDB为代表。
- 列式数据库：解决关系数据库大数据场景下的I/O问题，以HBase为代表。
- 全文搜索引擎：解决关系数据库的全文搜索性能问题，以Elasticsearch为代表。

今天，我来介绍一下各种高性能NoSQL方案的典型特征和应用场景。
<div><strong>精选留言（30）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/0f/87/57/645159ee.jpg" width="30px"><span>鹅米豆发</span> 👍（340） 💬（31）<div>       关于NoSQL，看过一张图，挺形象：“1970，We have no SQL”-&gt;“1980，Know SQL”-&gt;“2000，NoSQL”-&gt;“2005，Not only SQL”-&gt;“2015，No，SQL”。目前，一些新型数据库，同时具备了NoSQL的扩展性和关系型数据库的很多特性。
       关系型和NoSQL数据库的选型。考虑几个指标，数据量、并发量、实时性、一致性要求、读写分布和类型、安全性、运维性等。根据这些指标，软件系统可分成几类。
       1.管理型系统，如运营类系统，首选关系型。
       2.大流量系统，如电商单品页的某个服务，后台选关系型，前台选内存型。
       3.日志型系统，原始数据选列式，日志搜索选倒排索引。
       4.搜索型系统，指站内搜索，非通用搜索，如商品搜索，后台选关系型，前台选倒排索引。
       5.事务型系统，如库存、交易、记账，选关系型+缓存+一致性协议，或新型关系数据库。
       6.离线计算，如大量数据分析，首选列式，关系型也可以。
       7.实时计算，如实时监控，可以选时序数据库，或列式数据库。</div>2018-06-04</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/f8/ba/d28174a9.jpg" width="30px"><span>Geek_zbvt62</span> 👍（39） 💬（1）<div>看过一些资料，RDB当年（比我还大好多）也是在数据库大战的血雨腥风中一条血路杀出来的。现在回魂的document db当前也是RDB对手之一。如果真有这么多问题，怎么还能脱颖而出，主宰软件开发领域这么久。只能说现互联网和物联网的兴起使得应用场景向海量数据，线下上分析，读多写也多这些情况偏移了，这些场景对ACID的要求很低。
但现在大多数应用的也许还是直接面对用户，要求数据有一定可靠性，数据总量和并发量并没那么高。RDB技术成熟，人才易得，声明式SQL语法让开发者忽略底层实现，关系型的模型也符合人的思考模式。而且现在大多数一流的RDB都集成了基本的文档存储和索引，空间存储，全文检索，数据分析等功能。在没达到一定规模和深度前，完全可以用个RDB来做MVP，甚至搞定中小型也许场景。
从码农的角度看，我还是更崇拜关系型数据库，因为其底层实现里包罗了算法，系统，网络，分布式，数学统计学各种绝世武功。
前几年在NoSQL炒起来没多久，NewSQL的概念又被提出了。现在各路牛人都投入到D RDB的研发中，成型的也有不少。虽然不太可能完全取代现在的各种NoSQL，但也许能收复不少失地。
历史就是个循环，天下大势分久必合合久必分...
</div>2018-06-02</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/cf/bb/22af0e52.jpg" width="30px"><span>孙振超</span> 👍（29） 💬（3）<div>本章最大的收获是了解了nosql数据库的四种类型以及特点、使用场景和关系型数据库的区别，比如redis中的list结构的强大之处、列式存储为什么压缩比会高很多，这也是作者比较强的地方。作为存储数据的系统，肯定有共同的地方，但既然能单独拎出来又说明有不同之处，掌握了相同之处可以快速理解系统能力，了解了不同之处可以明白其使用范围，并且对自己以后的架构设计方案选择提供基础。
自己之前总觉得要掌握一个系统要从看源代码开始，但后来发现这种方式太过耗时，效率过低，就开始转变为了解这个系统主要的能力是什么，然后根据能力去进行拆解，看那些是自己已经掌握了解的，那些是陌生的，对于陌生的部分了解其实现思路是怎么样的，对于实现思路的主要细节看下代码了解，这样有针对性的看效率得到了比较大的提升。

对于本篇的问题，在文章中其实已经说明白了，关系型数据库是不可替代的，比如事务能力、强管控、经常性读取多列的场景都需要关系型数据库。</div>2018-06-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/15/a6/723854ee.jpg" width="30px"><span>姜戈</span> 👍（29） 💬（4）<div>华仔，我们公司刚起步的时候有2个应用，数据库用的mysql,  日志也存储在mysql,   用户增长很快，没有专职架构师，现在准备重构以适应业务增长，考虑jhipster on kubernetes ,  昨天同事之间交流了一下方案: gateway + registry + k8s traefik ingress, 通过k8s 实现hipster技术栈的高可用，所有微服务容器化， 第一阶段准备拆成5个service,  在gateway做路由规则和鉴权，日志部分用mongodb,  mysql暂时不分库，订单rocketMQ队列化,  这样合理吗？有什么更好的建议?</div>2018-06-02</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/85/e8/1e3e5657.jpg" width="30px"><span>彬哥</span> 👍（26） 💬（8）<div>我认为，行式数据库读取的时候，用sql可以指定关心的列，无需读取所有。

所以，这一段是不是笔者笔误？求赐教

</div>2018-06-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/c2/1f/343f2dec.jpg" width="30px"><span>9527</span> 👍（17） 💬（5）<div>老师您好，问个题外话😂
如今各种新技术层出不穷，像那种底层的大块头之类的书籍，比如深入理解计算机系统，编译原理这样的，还有必要深入学习吗？
像深入理解计算机系里面的反汇编分析在实际工作中确是是用不到，更别提开发个编译器了
面对这些看似不错的书籍，但又觉得里面的内容无法运用到实际中，有些迷茫，望老师指点</div>2018-06-05</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/ac/ed/d868396d.jpg" width="30px"><span>铃兰Neko</span> 👍（16） 💬（1）<div>认真的看到现在，有两点疑问。
1.es和lucene这种，一般当做搜索引擎，也划在nosql里面合适吗?
2.能否给一些常见nosql性能和数据量的数据，
网上搜不大到，唯一知道的都是从ppt里面扣的

另外，nosql那个图原图应该在reddit上，地址是
 http:&#47;&#47;i.imgur.com&#47;lkG9Vm8.jpg</div>2018-06-04</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/36/2c/8bd4be3a.jpg" width="30px"><span>小喵喵</span> 👍（14） 💬（3）<div>跨库操作如何做事物呢？看到这期了还是没有答案吗？</div>2018-06-03</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/4d/49/28e73b9c.jpg" width="30px"><span>明翼</span> 👍（11） 💬（1）<div>文档数据库和es有何区别，es我看也是对scheme不敏感的啊</div>2018-06-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/24/86/6069f169.jpg" width="30px"><span>func</span> 👍（9） 💬（1）<div>关系数据库就是行式存储，从硬盘读到内存的时候，是整行读取，实际上还是整页读取的。不明白这个整页指的是？这个整页指的是  包括很多行数据吗？这个整页的数据都是我需要的吗？</div>2018-09-29</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/pc41FOKAiabVaaKiawibEm7zglvnsYBnYeRiaSAElf9ciczovXmXmI0hOeR6U9RULFtMoqX5kobNttvwXCLsUM9Hbcg/132" width="30px"><span>monkay</span> 👍（8） 💬（2）<div>有个商品搜索的需求，怎么评估elasticsearch和solr哪个更合适？</div>2018-06-02</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/18/10/731b4319.jpg" width="30px"><span>轩辕十四</span> 👍（7） 💬（1）<div>mongo4 开始支持事务了吧</div>2018-06-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/c9/20/e4f1b17c.jpg" width="30px"><span>zj</span> 👍（6） 💬（1）<div>提一个问题，数据本来是存在mysql的，然后将数据同步到es中，中年如何保证一致性</div>2018-06-06</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/36/2c/8bd4be3a.jpg" width="30px"><span>小喵喵</span> 👍（6） 💬（1）<div>跨库如何用最终一致性呢？老师能加微信吗</div>2018-06-04</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/ca/e4/f15a1cf0.jpg" width="30px"><span>三月沙@wecatch</span> 👍（6） 💬（1）<div>Nosql 数据库好用，但是用好不容易，接触过一些团队在 MongoDb 中存储一些结构变动频繁的数据，结果导致每次结构发生变化时，之前的数据都不做结构变更，由于业务复杂，代表量大，很多地方没有做好兼容性，而且还用的动态语言，导致线上莫名就会就会出 null和 keyError 错误。从个人使用角度来讲，虽然数据库本身 schema 没有强约束，不代表开发者可以滥用这一能力，最佳实践是应该是终保持新老数据结构的一致性，保证数据在代码中的稳定性。</div>2018-06-04</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/c5/3e/41339003.jpg" width="30px"><span>幻影霸者</span> 👍（6） 💬（1）<div>mongodb4.0不是支持acid事务吗？</div>2018-06-03</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/fb/ba/68bb346c.jpg" width="30px"><span>shihpeng</span> 👍（5） 💬（2）<div>曾经面试过一个在新加坡金融创业公司的小老弟，让他介绍一下之前做的系统：主要数据存储是MongoDB，因为他们数据量比较大 (2亿条)，要用大数据存储；架构图中MongoDB旁边一个PostgreSQL，因为MongoDB没法join，所以用了PostgreSQL；下面有一个ES，因为MongoDB&#47;PSQL搜索不方便；远一点的地方有一个ArangoDB，说是因为他们需要事务处理....

我问他，你知道你的这些需求一台MySQL可以全搞定吗？他回：MySQL不是很慢吗...</div>2021-01-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/64/9b/d1ab239e.jpg" width="30px"><span>J.Smile</span> 👍（5） 💬（2）<div>要点总结：
● 文档数据库的缺点
	○ 不支持事务
	○ 不支持join
● 倒排索引与正排索引
	○ “正排索引”的基本原理是建立文档到单词的索引
	○ ”倒排索引“适用于根据关键词来查询文档内容。

✓ 心得
● 记得一次面试中被问到了关于条件组合搜索的问题，当时回答的一塌糊涂，现在才明白可以使用全文搜索引擎比如es这种方案来代替。而当时自己的思维局限在了关系型数据库。
● 通过学习了解到作为一个技术人，不一定动不动就去看源码，那样很耗时耗力，结果未必就是好的。但一定要知道哪些技术解决那些问题。这样当做架构的概要设计与技术选型的时候有利于纵览全局，快速确定目标方案。而具体的细节问题可以在详细设计阶段掌握。
</div>2020-12-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/16/2d/2753369a.jpg" width="30px"><span>Geek_58ezrw</span> 👍（5） 💬（3）<div>华哥，我想问下，我之前在做电商时，将商品全部存到redis中以hash结构存储，同时商品下面有个库存也存在其下面，库存在做减操作时，我用hincrby来进行，并发小的时候问题不大，库存不会超。
并发大了以后会不会数据库一样超了？</div>2018-12-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/32/4a/2dc9cfde.jpg" width="30px"><span>ncicheng</span> 👍（5） 💬（1）<div>对于需要存储大量非文本格式的文档（如doc），项目中一般采取blob，但是搜索文档内容不容易，如果换成NoSQL来存储是不是比现在好？谢谢~</div>2018-06-05</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/17/6c/c62ae8ef.jpg" width="30px"><span>caison</span> 👍（4） 💬（1）<div>redis的操作应该是原子性的吧，因为redis的单线程的</div>2018-07-25</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/ef/37/4b12b4cc.jpg" width="30px"><span>ZYCHD(子玉)</span> 👍（4） 💬（2）<div>保险行业用的关系型数据库多些，No SQL少些。保险行业一个重要的要求是数据不能丢失！</div>2018-06-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/15/73/e5e4b245.jpg" width="30px"><span>Andy</span> 👍（3） 💬（1）<div>对于这个观点，个人觉得，对方并没有完全吃透关系型数据库与非关系型数据之间的区别和联系，为什么会产生非关系型数据，那是为了弥补关系型数据库的缺点而诞生的，基于大数据时代背景而出现的，一个用于解决缺点的东西，并不能说明把优点就覆盖了，这个世界没有觉得最优的解决方案。关系型数据的存在，就像作者说的，基于其自身ACID特性和强大的SQL，这是非关系型数据库无法替代的，故NoSql != No Sql而是Not Only Sql</div>2020-09-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/0c/e1/e54540b9.jpg" width="30px"><span>冯宇</span> 👍（3） 💬（1）<div>所以postgresql功能性和性能就平衡的非常好，原生支持全文检索，不必因为简单的关键字查询就必须引入es增加架构复杂性</div>2018-11-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/2d/0d/50658bcf.jpg" width="30px"><span>joinboo</span> 👍（2） 💬（1）<div>华哥，hbase作为列式数据库的代表，在实时写和读的性能都不错，对于一些数据一致性要求不那么高的在线场景我们就是直接用hbase, 目前用着也挺香。所以我想问下，在你之前的项目中使用hbase提供在线服务的场景多吗，比如有哪些场景？</div>2021-04-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/92/6d/becd841a.jpg" width="30px"><span>escray</span> 👍（2） 💬（1）<div>如果遇到关系型数据就用 MySQL；需要 K-V 存储的时候，就采用 Redis；需要文档数据库的时候，就用 MongoDB；需要列式数据库的话，就采用 HBase；需要全文搜索的时候，用 Elasticsearch 或者 Solr。

谈笑风生……但是我的问题是，除了 MySQL，对其他几个都不熟，学习之路漫漫。

K-V 存储的 Redis 和文档数据库都不支持事务，如果需要的话，只能使用代码实现。列式存储虽然没有明说，但是我觉的在事务支持上应该也没什么优势，与全文搜索数据库类似，都是更重视读的效率。

NoSQL = Not Only SQL

可想而知，其实有很多领域还是无法离开关系型数据库的，比如涉及到账目流转的金融系统，还有电商平台的订单系统，大部分的用户管理系统……

NoSQL 可能会成为关系型数据库的好的补充方案，在我的感觉里面，现实社会映射到技术领域，应该还是关系型数据为主，也相对简单一些。总不可能，未来所有的系统都变成人工智能、深度学习……的黑盒子。</div>2020-09-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/2c/45/e8bcf142.jpg" width="30px"><span>(╯‵□′)╯︵┻━┻</span> 👍（2） 💬（1）<div>思考：这个说法是自相矛盾的。假如NoSQL的强大是因为一系列适配专有的业务场景的NoSQL种类，那么就会产生一种适应传统SQL业务场景的NoSQL，也就是SQL本身。</div>2019-08-03</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/0b/a6/b234aa79.jpg" width="30px"><span>孙晓明</span> 👍（2） 💬（1）<div>前两天看消息说MySql发布新版本，支持NoSql，这是不是也是数据库发现的趋势，李老师对这个怎么看？</div>2018-06-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/36/2c/8bd4be3a.jpg" width="30px"><span>小喵喵</span> 👍（2） 💬（1）<div>而用文档数据库是无法进行 join 查询的，需要查两次：一次查询订单表中购买了苹果笔记本的用户，然后再查询这些用户哪些是女性用户。
具体如何查呢？
把一串的
ID拼接起来，然后用户ID in () and sex ＝女吗，如果这样的话，数据多性能很差的。期待老师其他更好的方案。</div>2018-06-02</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/d5/68/2201b6b9.jpg" width="30px"><span>归零</span> 👍（1） 💬（1）<div>这篇文章非常赞，高屋建瓴的介绍关系型数据的问题和对应的NoSQL解决方案，对于技术选型很有帮助</div>2022-08-24</li><br/>
</ul>