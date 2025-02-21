高性能是每个程序员的追求，无论我们是做一个系统还是写一行代码，都希望能够达到高性能的效果，而高性能又是最复杂的一环，磁盘、操作系统、CPU、内存、缓存、网络、编程语言、架构等，每个都有可能影响系统达到高性能，一行不恰当的debug日志，就可能将服务器的性能从TPS 30000降低到8000；一个tcp\_nodelay参数，就可能将响应时间从2毫秒延长到40毫秒。因此，要做到高性能计算是一件很复杂很有挑战的事情，软件系统开发过程中的不同阶段都关系着高性能最终是否能够实现。

站在架构师的角度，当然需要特别关注高性能架构的设计。高性能架构设计主要集中在两方面：

- 尽量提升单服务器的性能，将单服务器的性能发挥到极致。
- 如果单服务器无法支撑性能，设计服务器集群方案。

除了以上两点，最终系统能否实现高性能，还和具体的实现及编码相关。但架构设计是高性能的基础，如果架构设计没有做到高性能，则后面的具体实现和编码能提升的空间是有限的。形象地说，架构设计决定了系统性能的上限，实现细节决定了系统性能的下限。
<div><strong>精选留言（30）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/0f/87/57/645159ee.jpg" width="30px"><span>鹅米豆发</span> 👍（202） 💬（4）<div>       不同并发模式的选择，还要考察三个指标，分别是响应时间（RT），并发数（Concurrency），吞吐量（TPS）。三者关系，吞吐量=并发数&#47;平均响应时间。不同类型的系统，对这三个指标的要求不一样。
       三高系统，比如秒杀、即时通信，不能使用。
       三低系统，比如ToB系统，运营类、管理类系统，一般可以使用。
       高吞吐系统，如果是内存计算为主的，一般可以使用，如果是网络IO为主的，一般不能使用。</div>2018-06-07</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/a7/ce/7ee0d672.jpg" width="30px"><span>Regular</span> 👍（116） 💬（6）<div>我怎么觉得，凡是高并发请求的系统都适合本节讲的高性能模式？！</div>2018-06-07</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/ee/67/c146c144.jpg" width="30px"><span>W_T</span> 👍（96） 💬（2）<div>老师在文章和留言里已经透露答案了。
首先，PPC和TPC能够支持的最大连接数差不多，都是几百个，所以我觉得他们适用的场景也是差不多的。
接着再从连接数和请求数来划分，这两种方式明显不支持高连接数的场景，所以答案就是：
1. 常量连接海量请求。比如数据库，redis，kafka等等
2. 常量连接常量请求。比如企业内部网址</div>2018-06-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/c8/d5/e88c1805.jpg" width="30px"><span>JackLei</span> 👍（39） 💬（2）<div>看到这篇文章，这个专栏的价值远远远远远远远远远远远远远远远远大于专栏购买的价格。</div>2018-06-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/fe/c5/3467cf94.jpg" width="30px"><span>正是那朵玫瑰</span> 👍（39） 💬（3）<div>根据华仔回复留言的提示，分析下
1. 海量连接（成千上万）海量请求：例如抢购，双十一等
这样的系统，我觉得这讲所说的模式都不适应，面对海量的连接至少要使用IO复用模型或者异步IO模型，针对海量的请求，无论使用多进程处理还是多线程，单机都是无法支撑的，应该集群了吧。
2. 常量连接（几十上百）海量请求：例如中间件
常量连接，我觉得这讲的模式应该可以适用，如使用TPC的preyhtead模型，启动几十上百的线程去处理连接，应该问题不大吧，但是老师举的列子是中间件是这类系统，我就有点疑问了，是不是中间件系统都可以是阻塞IO模型来实现，比如activemq既支持BIO也支持NIO，但是NIO只是解决了能处理更多的连接，而真正每个请求的处理快慢还得看后面的业务的处理；而阿里的rocketmq也是使用netty这样的NIO框架实现的。但在面对常量连接的场景下，NIO并没有优势啊。
3. 海量连接常量请求：例如门户网站
这种系统我觉得非常适合使用netty这样的NIO框架来实现，IO复用模型可以处理海量的连接，而每个连接的请求数据量会很小，处理会很长快，如华仔说的门户网站，只要简单返回页面即可。
4. 常量连接常量请求：例如内部运营系统，管理系统
这种系统，本讲的模式就很适合了。

水平有限，望华仔指点下。</div>2018-06-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/70/6d/11ea66f0.jpg" width="30px"><span>peison</span> 👍（31） 💬（5）<div>请教一个比较小白的问题…为什么说门户网站是海量连接常量请求的情况？海量连接下为什么会常量请求，一直想不通</div>2018-07-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/0b/a6/b234aa79.jpg" width="30px"><span>孙晓明</span> 👍（21） 💬（4）<div>李老师，看完文章后查了一下bio和nio，还有一种aio，看的不是太明白，能麻烦您解答一下，并且它与nio的差别在哪里？</div>2018-06-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/ac/a1/43d83698.jpg" width="30px"><span>云学</span> 👍（20） 💬（1）<div>希望再多写几篇讲解单机性能优化，比如线程模型，数据库，网络等，猜测下一篇讲IO复用了吧</div>2018-06-07</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/38/57/a9f9705a.jpg" width="30px"><span>无聊夫斯基</span> 👍（18） 💬（5）<div>我无法想到ppc比tpc更适合的场景</div>2018-08-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/f1/97/e3bbbb14.jpg" width="30px"><span>胖胖的程序猿</span> 👍（17） 💬（4）<div>1. 海量连接（成千上万）海量请求：例如抢购，双十一等
2. 常量连接（几十上百）海量请求：例如中间件
3. 海量连接常量请求：例如门户网站
4. 常量连接常量请求：例如内部运营系统，管理系统

这个不理解，连接和请求有什么区别</div>2019-04-01</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/d8/ca/b0a0e033.jpg" width="30px"><span>LakNeumann</span> 👍（15） 💬（1）<div>大神， ……纯新手感觉这里读起来已经有点吃力了 ～  好难啊</div>2018-06-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/49/a5/e4c1c2d4.jpg" width="30px"><span>小文同学</span> 👍（15） 💬（1）<div>PPC和TPC对那些吞吐量比较大，长连接且连接数不多的系统应该比较适用。两种模式的特点都比较重，每个连接都能占有较多计算资源，一些内部系统，如日志系统用于实时监控的估计可以采用。这类型的系统一般连接数不多，吞吐量比较大，不求服务数量，求服务质量。不知道这样的假设符不符合？</div>2018-06-07</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/cf/bb/22af0e52.jpg" width="30px"><span>孙振超</span> 👍（11） 💬（1）<div>本章中提到的几个概念，比如阻塞、非阻塞、同步、异步以及主要的两种方式ppc和tpc，以前都是记住了，今天通过这篇文章是理解了而不再是记住了。
ppc和tpc都是有一个进程来处理链接，收到一个请求就新创建一个进程或线程来处理，在处理完成之前调用方是处于阻塞状态，这种机制决定了单机容量不会太大。
但在文章中提到数据库一般是ppc模式，但数据库通常是链接数少请求量大的场景，为什么会采用这种模式呢？reactor模式为什么不适合数据库？还望老师解惑，多谢！</div>2018-07-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/d9/a2/afbc447c.jpg" width="30px"><span>海军上校</span> 👍（10） 💬（2）<div>如何系统的学习liunx～ 包括网络～文件系统～内存管理～进程管理～然后串起来形成面呢😂</div>2018-08-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/e4/59/02c37587.jpg" width="30px"><span>james</span> 👍（9） 💬（1）<div>互联网高并发的系统全部适应啊，现在C10K已经不是问题了，有些可优化度较高的系统（例如读多写少的系统）C100k的性能都很常见了</div>2018-06-07</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTJQWibq0rrOy5zyj0wkCU8sZL2YT1hPbCClbE3MKtLlR9VycaScdgFJiclKqibavyK9TYqhU8C7dE0zw/132" width="30px"><span>Hanson</span> 👍（7） 💬（1）<div>如果针对自内部系统，是否使用长链接性能损耗较低，毕竟频繁建链拆链性能损耗还是不小的，尤其是TLS的情况下</div>2018-11-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/45/23/28311447.jpg" width="30px"><span>盘尼西林</span> 👍（6） 💬（1）<div>怎么理解常量连接 海量请求。
如果请求多的话，连接还会是常量么？
</div>2020-03-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/ce/3d/385b8263.jpg" width="30px"><span>星火燎原</span> 👍（6） 💬（1）<div>像您说的这种多进程多线程模式好似更加稳定，但是tomcat为什么采用单进程多线程模型呢？</div>2018-06-07</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/67/f4/9a1feb59.jpg" width="30px"><span>钱</span> 👍（5） 💬（1）<div>课前思考及问题
1：啥是PPC？它怎么提高性能的？
2：啥是TPC？它怎么提高性能的？
3：还存在XPC吗？

课后思考及问题
1：今天讲的知识，感觉是自己的知识盲点，不是很了解。
2：文中核心观点
2-1：高性能架构设计主要集中在两方面：
一是，尽量提升单服务器的性能，将单服务器的性能发挥到极致。
二是，如果单服务器无法支撑性能，设计服务器集群方案。
2-2：架构设计决定了系统性能的上限，实现细节决定了系统性能的下限。
2-3：服务器高性能的关键之一就是服务器采取的并发模型，并发模型有如下两个关键设计点：
服务器如何管理连接，和I&#47;O模型相关，I&#47;O 模型：阻塞、非阻塞、同步、异步。
服务器如何处理请求，和进程模型相关，进程模型：单进程、多进程、多线程。
详情需参考《UNIX网络编程》《NUIX环境高级编程》《LINUX系统编程》
3：PPC 是 Process Per Connection 的缩写，其含义是指每次有新的连接就新建一个进程去专门处理这个连接的请求，这是传统的 UNIX 网络服务器所采用的模型。
这里没太明白老师讲的是网络通信的通用I&#47;O模型，还是指UNIX特有的，感觉没讲全，也没讲出它怎么实现单服务器的高性能的？
4：TPC 是 Thread Per Connection 的缩写，其含义是指每次有新的连接就新建一个线程去专门处理这个连接的请求。与进程相比，线程更轻量级，创建线程的消耗比进程要少得多；同时多线程是共享进程内存空间的，线程通信相比进程通信更简单。
5：这块知识差的太多了，感觉听完老师的讲解，发现自己对于进程、线程、子进程、子线程、怎么阻塞的、怎么唤醒的、怎么分配内存空间的、怎么被CPU执行的、网络链接怎么建立的、进程怎么切换的、线程怎么切换的、一个请求怎么发送怎么处理的怎么返回的、长链接怎么保持的这些东西的具体细节都不太清楚。惭愧啊！知耻而后勇，我一定把这些补上来！
</div>2019-08-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/d5/3f/80bf4841.jpg" width="30px"><span>文竹</span> 👍（5） 💬（1）<div>PPC适合对稳定性要求高，但并发量不大的场景，对于互联网的场景不适合。

TPC支持的并发量大，适合互联网产品场景。对于支持稳定性，需要创建冗余进程。
</div>2018-08-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/d1/29/1b1234ed.jpg" width="30px"><span>DFighting</span> 👍（4） 💬（2）<div>看大家的评论，对aio、bio和nio讨论的比较多，我也来凑个数：
请求到达服务器到最终处理完毕可以分为3个过程，接受请求+系统处理+结果返回，其中需要切换线程写作的是请求接受后，在系统处理这段时间，连接线程如何做：
bio:阻塞调用等待系统处理完毕
nio:不阻塞调用，不断查询结果，其实从结果上来看依然是阻塞等待的一种，只不过是主动点
io复用：一个连接同时处理多个io请求，本质上还是阻塞，不过由多个线程同时阻塞等待转为一个线程阻塞，等待多个io调用结果
aio:连接请求和处理请求完全异步，连接交给系统处理以后，我就可以去处理下一个连接，等待系统处理结果完毕以后，发送消息或者信号异步发送结果返回
其实从本质以上来看，阻塞和非阻塞这两种性能差异感觉不大，多路复用虽然也是阻塞但是它复用了阻塞线程，提高了性能。异步io才是真正实现了连接线程和系统处理线程的并发执行。
以上是我自己的了解，如有不正确的地方，欢迎指正和探讨</div>2021-03-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/e1/11/8eac267f.jpg" width="30px"><span>咬尾巴的蛇</span> 👍（4） 💬（3）<div>很感谢分享，我想问下 就是我开一个tomcat，支持tcp请求，然后什么都不做处理，同时有几百个请求是后面连接就进不来了吗，我是新手才开始架构这块，希望能帮忙解释下，非常感谢</div>2018-08-15</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/DYAIOgq83eo3DrWeV7ZwRLXrRZg4V3ic1LQYdZ3u1oicDhqPic47vMguvf5QS69roTiaJrwDr5Re3Sy2UyHDWwmsTA/132" width="30px"><span>大光头</span> 👍（4） 💬（1）<div>高吞吐和高稳定是互斥的，如果要高吞吐就要采用prethread模式，如果要高稳定就需要高preprocess，如果要综合，线程进程同时</div>2018-06-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/70/5a/01637b6e.jpg" width="30px"><span>琴扬枫</span> 👍（4） 💬（1）<div>老师好，请教个问题，文中提到的几百连接是在什么样的软硬件环境参数下面呢？谢谢</div>2018-06-07</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/5d/c4/abb7bfe3.jpg" width="30px"><span>Liang</span> 👍（3） 💬（2）<div>进程和线程就像公司和部门。
PPC需要进程之间通信，效率会比较低。
TPC进程调用线程就像公司指挥自己的部门，资源是共享的，效率比进程之间的通信要高。但是有死锁风险，就像公司不同部门之间争夺资源有时会导致某些项目无法推进。</div>2021-03-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/0c/94/56ea80f7.jpg" width="30px"><span>沐风</span> 👍（3） 💬（2）<div>单台数据库服务器可以支撑多少并发？单台nginx 可以支撑多少呢</div>2018-06-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/f8/0e/de697f9b.jpg" width="30px"><span>熊猫酒仙</span> 👍（3） 💬（2）<div>单方close和双方close应该是全双工与半双工的区别，连接仍然还存在的。
ppc&#47;tpc比较适合系统中担当路由器或容器角色的部分，像nginx，甚至像mongodb集群也有router。
感觉一些部署容器的线程池，应该属于tpc范畴！</div>2018-06-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/de/17/75e2b624.jpg" width="30px"><span>feifei</span> 👍（3） 💬（1）<div>PPC和TPC,这2种模式，无论进程还是线程都受cpu的限制，进程和线程的切换都是有代价的，所以像小型的系统合适，所以很多传统行业选择的是这2种</div>2018-06-07</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/18/60/f9/85738be3.jpg" width="30px"><span>katejc</span> 👍（2） 💬（1）<div>老师，我看了一些留言，有疑问：一个请求不就会 进行一次连接吗，那么海量的请求不就是 会带来海量的连接吗；</div>2022-05-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/24/b2/17/3161b49c.jpg" width="30px"><span>达叔灬</span> 👍（2） 💬（1）<div>prethread  感觉有点像线程池。</div>2021-11-26</li><br/>
</ul>