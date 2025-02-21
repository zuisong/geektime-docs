你好，我是蔡元楠。

从今天开始，我们进入专栏的第二模块。通过这一模块的学习，带你一起夯实大规模数据处理的基础。

首先，我将结合硅谷顶尖科技公司的**最佳实践** (Best Practice) ，和你一起分享在设计分布式系统架构时，我们有可能会碰到哪些雷区？又有哪些必备的基础知识？

在硅谷一线大厂所维护的系统服务中，我们经常可以看见SLA这样的承诺。

例如，在谷歌的云计算服务平台Google Cloud Platform中，他们会写着“99.9% Availability”这样的承诺。那什么是“99.9% Availability”呢？

要理解这个承诺是什么意思，首先，你需要了解到底什么是SLA？

SLA（Service-Level Agreement），也就是**服务等级协议**，指的是系统服务提供者（Provider）对客户（Customer）的一个服务承诺。这是衡量一个大型分布式系统是否“健康”的常见方法。

![](https://static001.geekbang.org/resource/image/77/be/77361f3533c4579bb0d9661af49616be.jpg?wh=1142%2A640)

在开发设计系统服务的时候，无论面对的客户是公司外部的个人、商业用户，还是公司内的不同业务部门，我们都应该对自己所设计的系统服务有一个定义好的SLA。

因为SLA是一种服务承诺，所以指标可以多种多样。根据我的实践经验，给你介绍最常见的四个SLA指标，可用性、准确性、系统容量和延迟。
<div><strong>精选留言（30）</strong></div><ul>
<li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/yYzf0yonEqKny7dHlvLibc7OrQJ6HszX3VP1fciaMD3hITFySbayL9vULch5hvicoqGA2EBzcPicss2ciaB7ibodgQ6w/132" width="30px"><span>sxpujs</span> 👍（21） 💬（1）<div>这几节干货有点少啊，也缺少一些实战和实例。</div>2019-04-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/0f/71/9273e8a4.jpg" width="30px"><span>时间是最真的答案</span> 👍（20） 💬（1）<div>作为一个学习大数据的新手，希望作者能用几篇文章讲解大数据处理中使用的技术如何搭建，运行，优化的，以及各个技术如何结合使用，这样新手也能玩起来</div>2019-04-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/8b/3c/0462eca7.jpg" width="30px"><span>Tomcat</span> 👍（4） 💬（1）<div>SLA，即服务等级协议，规定了我们的工程的质量和目标，这使得我们的工作具有可衡量的尺度。
以前我在中国移动做专线提供服务的时候，对这个颇为敏感，移动的专线产品，确实有许多不足之处，但是这让我构建了服务质量可以使用具体技术指标度量的理念。
对于现在我正在做的产品，同样也有一些苛刻的要求，所以通过本文，我构建了服务质量度量体系～</div>2019-04-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/80/b9/e2fbe96c.jpg" width="30px"><span>滨 风暴</span> 👍（1） 💬（1）<div>我的理解是为了提高SLA，系统就要达到一定的冗余度，对于大数据来说存储和计算使用的资源就更多，所以定义SLA的时候，是不是还是要考虑一下成本，或者有没有提供高SLA的轻量化系统架构？</div>2019-05-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/5c/d9/dc6bd5d4.jpg" width="30px"><span>Blakemmmm</span> 👍（1） 💬（1）<div>请问老师可用性的数据一般是如何测出或算出的呢？内部测试时不可能测试那么长时间，而短时间的测试又无法反应随着运行时间增长导致的系统更容易出问题的概率。</div>2019-05-16</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/93/33/94d7e3ab.jpg" width="30px"><span>王众</span> 👍（0） 💬（1）<div>回复里看到老师“纯狠操猛干”的用语，是在和这个斯文的头像不配哈，挺适合我的头像。感谢老师对很多留言的耐烦解答与鼓励。</div>2019-05-05</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/e7/87/9ad59b98.jpg" width="30px"><span>程序设计的艺术</span> 👍（0） 💬（1）<div>你好，老师，目前的大数据处理架构该是什么样子呢？我这边有每天40多万行数据形成数据仓库，离线匹配行记录，使用什么方法可以快速处理？谢谢</div>2019-04-25</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/9e/50/21e0beca.jpg" width="30px"><span>kylin</span> 👍（0） 💬（1）<div>我们公司这边的SLA优化主要是对Hive处理数据，特别是源表是全量表时，要求处理时长越短越好。有的要求从1小时优化到40分钟。这里的SLA优化好像和讲的服务等级协议的四个指标关系不大吧</div>2019-04-24</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/PiajxSqBRaEKCTAPGcRSicRNXwftZAe1MEwUwicXsPTltc3z2liak2VicdhWx7jAasZWr0SiciaoOEueX0zWEWpiaZVickEZvNx9DlfjriaAKOmaf5X6Q/132" width="30px"><span>Joseph</span> 👍（49） 💬（2）<div>在实际应用SLA的时候，有两点不解：
1. 在设计系统之初，大家拍脑袋来定义SLA。这个时期，SLA对应需要付出的成本还不明确，这样大家都会趋于订出很高标准。这种情况有好的解决办法吗？
2. 虽然定义了SLA，但在架构设计的时候，如何评估架构是否能满足SLA呢？等到软件实现了再来测试，似乎有点太晚了……请教老师一般是如何处理这两个问题的呢？</div>2019-04-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/ae/7c/251fc690.jpg" width="30px"><span>Dany</span> 👍（25） 💬（0）<div>我觉得这一节超赞。基础概念很重要，很重要，很重要。
实战这种事情，有的是时间去practice，而SLA这几个关键概念，会成为很多人理解的迷雾。
当我发现我的lead，拉着一大堆自己也还没理解清楚SLA指标去拉KPI，扛大旗的时候，我才进一步，深刻体会到这一节内容的重要性^ ^</div>2019-04-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/7c/16/4d1e5cc1.jpg" width="30px"><span>mgxian</span> 👍（13） 💬（0）<div>这个SLA和一般服务监控指标 RED 原则有点像
R rate 请求速率 qps
E errors 错误数错误率
D duration 延迟 
再加一个 服务可用性指标等级 就是今天讲的服务等级了</div>2019-04-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/6b/e4/afacba1c.jpg" width="30px"><span>孙稚昊</span> 👍（10） 💬（0）<div>我们公司为了高并发QPS, 以前的python server 全部换成 Golang 了，Golang 做高并发是真的有优势</div>2019-04-25</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/4d/49/28e73b9c.jpg" width="30px"><span>明翼</span> 👍（7） 💬（0）<div>我们系统一般可用性，系统容量有做定义也多在招投标的文件中，至于准确性和延迟更没有严格测试，准确性这个我觉得不好测试吧，如果知道出错了，干嘛不修改那，老师业界硅谷大厂如何测试准确性那？</div>2019-04-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/f5/80/baddf03b.jpg" width="30px"><span>zhihai.tu</span> 👍（5） 💬（0）<div>在银行做大数据平台的研发工作，也从可用性、准确性、系统容量、延迟四个指标来谈谈SLA，理解的不是很深，如有错误和不妥，请老师指导和更正：
1、可用性：不管是hadoop还是mppdb，数据库本身提供了本地高可用，另外，采用了双园区主备设计，提供了园区自动切换服务，保证了园区之间的高可用。
2、准确性：流数据处理平台，存在数据丢失的可能性。具体百分比应该是小于5%的。
3、系统容量：采用限流的方式，通过参数设置，从而控制最大的并发数量。
4、延迟：hadoop平台由于延迟较高，设计了异步处理请求及多线程技术，提高用户体验。</div>2019-04-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/23/a1/b08f3ee7.jpg" width="30px"><span>何妨</span> 👍（4） 💬（0）<div>记笔记:
定义SLA的四个维度
可用性:4个9，1日8秒
准确性:容错标准
系统容量:QPS,RPS
延迟:p95,p99
</div>2019-12-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/9b/9a/dcb2b713.jpg" width="30px"><span>hufox</span> 👍（3） 💬（0）<div>今天学到了什么SLA，请问老师，大数据平台中缓存的设计重要吗？一般如何设计？希望老师后面能讲讲新手如何搭建一个大数据平台，把整个流程运行起来，帮助更好的理解大数据处理流程！</div>2019-04-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/53/d4/2ed767ea.jpg" width="30px"><span>wmg</span> 👍（2） 💬（0）<div>老师我的理解SLA更适用于衡量oltp系统，和大数据处理系统有哪些联系呢？我的理解可能有误，老师指教</div>2019-04-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/9d/c0/cb5341ec.jpg" width="30px"><span>leesper</span> 👍（1） 💬（0）<div>“当 p95 或者 p99 过高时，总会有 5% 或者 1%的用户抱怨产品的用户体验太差”，这个不可小视，因为很可能这1%或者5%用户就是很资深的用户，比如他&#47;她在这个平台上买过很多东西所以响应慢，这个一定要做优化</div>2019-07-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/fa/be/0aef4c98.jpg" width="30px"><span>vic5210jp</span> 👍（1） 💬（0）<div>有4个问题不太明白，希望可以交流一下。
1.系统容量和延迟可以理解为吞吐量和响应速度么？
2.不同的业务访问的数据量不同，因而延迟也有所不同，用p95或者是p99这样描述整个系统的延迟是否不太准确。
3.除了介绍的SLA服务等级协议，系统的扩展性和复杂度等这些是否也应该被纳入一个系统的评价标准中。
4.在高可用中，99.99%这种在系统上线前是如何测试得出的？一般我们是根据运行一段时间的情况来预估的，其实并不准确。</div>2019-04-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/03/2f/0a5e0751.jpg" width="30px"><span>再见理想</span> 👍（0） 💬（0）<div>服务等级协议（SLA）指标： 
可用性 高可用系统需要达到3个9 甚至4个9的服务可用性
准确性 数据一致性
系统容量 系统能承受的最大负载 可以用限流、性能优化等方式提升
延迟 可以使用缓存技术缓解</div>2022-05-25</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/18/4b/d7/f46c6dfd.jpg" width="30px"><span>William Ning</span> 👍（0） 💬（0）<div>老师同学好，关于文中的可用性，这个是怎么统计出来的？

有个问题，比如，一个很简单的系统网站，单体架构，在对外提供访问的一年里都很稳定，说可用性100%，不合适吧，可用性如何衡量呢？</div>2022-04-04</li><br/><li><img src="" width="30px"><span>高景洋</span> 👍（0） 💬（0）<div>对我们的系统而言，我觉得 1、覆盖率、2、更新频率 尤为重要。

1、业务方侧数据量1100W+
2、我们会有同步程序，将业务方侧的新数据及状态变化的数据，同步到我们的全量库（hbase）中。因为只有业务侧的数据，在我们的全量库中，数据才会参与其他信息的补充。补充信息后的数据才会参与下游的数据流转。
3、因为有脏数据的问题，入库前会做过滤。当前千万级的数据每天会有3000-4000条，因为脏数据问题覆盖不到，未覆盖率 0.03% - 0.04%
4、这个未覆盖指标 对我们尤为重要，假如这个指标超过0.1%。 就意味着，脏数据比例变高，有环节出现问题，需要让业务侧排查处理

-------------
5、业务侧的数据进到我们的全量库后，我们会对数据的其他信息做补充。
6、例：千万级的数据，我们需要半小时内补充完数据，进入下游的数据流转。
7、这个半小时，也是我们的一个指标。 类似课程里说的 第四点：延时。只不过课程里说的是，单个请求的延时，而我们这个指标是 数据批量处理的频率时间</div>2021-09-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/66/c8/f598a816.jpg" width="30px"><span>Phantom01</span> 👍（0） 💬（0）<div>是只有服务才有sla吗？软件会有sla吗？ 比如 hadoop，我们可以有吞吐量(iops)，单机容量，资源利用率。但是像可用性和错误率就不好定义。</div>2020-12-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/75/9b/611e74ab.jpg" width="30px"><span>技术修行者</span> 👍（0） 💬（0）<div>有一个问题请教，目前在大规模集群架构下，应用使用的资源不是固定的，系统中的数据规模不是固定的，并发用户以及用户访问量不是固定的，在这种情况下，如何给出一个合理的SLA？尤其是在某些极端情况下，应用可能还没有真正在产品环境中跑起来。
我遇到的定义SLA的几种方式：
1. 和竞争对手比，与市场平均SLA看齐。
2. 基于内部性能测试结果。
3. 公司统一规定，所有应用的SLA是一样的。
4. 领导拍脑袋。

目前没有看到哪些项目是基于日志分析来定义SLA的。</div>2020-11-07</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1c/fa/96/4a7b7505.jpg" width="30px"><span>Eden2020</span> 👍（0） 💬（0）<div>这一讲SLA确实对架构改进很重要，谢谢作者分享</div>2020-03-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/44/f6/60f948e1.jpg" width="30px"><span>Aven</span> 👍（0） 💬（0）<div>老师，听了您的课，感觉自己对SLA中的可用性的理解还不是很透彻，目前我正在搭建维护一套etcd集群，通过这节所讲的知识，对照评估了下集群的正确性，容量和延迟等方面特性，但是唯独可用性不知道如何评估，可用性是不是说出现机房网络问题或者宕机的时候，恢复集群的可用性需要多久？还望老师深入解析下</div>2019-06-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/f7/e0/34290aa4.jpg" width="30px"><span>倪必荣</span> 👍（0） 💬（1）<div>文中主要谈及3种一致性模型，强一致必须同步后才能访问，弱一致按时间发生同步与访问操作，可以同步与访问穿插，而最终一致是特别的弱一致，可以理解为用弱一致的方式达到强一致的效果，应该就是提高自动访问的频次。主要区别有2:

0.同步与访问是否可同时进行
1.是否自动提高访问频次</div>2019-06-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/a1/e6/50da1b2d.jpg" width="30px"><span>旭东(Frank)</span> 👍（0） 💬（0）<div>发生内部错误的时候，准确率低了，这些也算不可用吧。那这个可用性和错误率是否有一点重叠</div>2019-04-25</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/8c/2b/3ab96998.jpg" width="30px"><span>青石</span> 👍（0） 💬（0）<div>性能测试可以比较直观的看到错误率、系统容量、延迟的结果。可用性是否可以理解成集群、系统监控（故障恢复）、弹性伸缩容等方式来提升系统可用性呢？</div>2019-04-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/34/c1/255161c9.jpg" width="30px"><span>xfly</span> 👍（0） 💬（0）<div>这就是服务的KPI</div>2019-04-24</li><br/>
</ul>