你好！我是郑晔。

上一讲，我们学习了如何看接口，今天我们进入第三个部分——看实现。在一个系统中，模型和接口是相对稳定的部分。但是，同样的模型和接口，如果采用不同的实现，稳定性、可扩展性和性能等诸多方面相差极大。而且，只有了解实现，你才有改动代码的基础。

但是，不得不说，“看实现”是一个很大的挑战，因为有无数的细节在那里等着你。所以，在很多团队里，一个新人甚至会用长达几个月的时间去熟悉代码中的这些细节。

面对这种情况，我们该怎么办呢？

首先，你要记住一件事，你不太可能记住真实项目的所有细节，甚至到你离开项目的那一天，你依然会有很多细节不知道，可这并不妨碍你的工作。但是，如果你心中没有一份关于项目实现的地图，你就一定会迷失。

像我前面所说的新人，他们用几个月的时间熟悉代码，就是在通过代码一点点展开地图，但是，这不仅极其浪费时间，也很难形成一个整体认知。所以我建议，你应该直接把地图展开。怎么展开呢？**你需要找到两个关键点：软件的结构和关键的技术。**

可能你还不太理解我的意思，下面我就以开源软件Kafka为例，给你讲一下如何把地图展开，去看一个软件的实现。按照我们之前讲过的思路，了解一个软件设计的步骤是“先模型，再接口，最后看实现”。所以，我们要先了解Kafka的模型和接口。
<div><strong>精选留言（21）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/13/17/27/ec30d30a.jpg" width="30px"><span>Jxin</span> 👍（56） 💬（3）<div>旁外话: 我的能力只能做到描述自己的理解。我描述自己的理解是希望能从栏主和其他学员处获得反馈，从而调整个人认知。我的身边缺少在软件设计上有追求的队友，很感谢有这个平台可以让我试错，交流，调整。

1.我认为软件的结构和核心技术应该是分开的。kafka之所以是消息队列，看的是对消息队列这个模型的实现。kafka之所以是kafka看的是其消息存储这一核心技术的实现。所以，如果我是想通过看kafka了解消息队列，那么就没必要也不该去看存储实现，我该看的是，路由信息管理,消息生产,消息消费这3块核心业务的骨干，以及其旁支功能的选择(限制消息大小,故障节点延后,延迟消费)；如果我想知道kafka为什么在mq中间件中如此突出，那么我就得了解其核心技术的实现，也就这里所说的&#39;软硬结合的存储设计&#39;。

2.谈谈对模型的理解。模型是一个抽象的概念，被抽象的对象可以是某个聚合实体(订单中心中的订单),也可以是某个流程或功能(java内存模型中的主存与缓存同步的规则)。分层对模型来说是实现层面的东西，是一种水平方向的拆分，是一个实现上的规范；模型的细粒度拆分（父模型,子模型），应该是一种垂直维度的拆分，子模型的功能要高内聚，其复杂性不该发散到外部。

3.protected long p1, p2, p3, p4, p5, p6, p7; 这个玩意是Disruptor的缓存行填充中的填充字段。Disruptor中的一个元素是一个volatile的long类型,占用8字节。一但一个元素被修改，则与其出于同个缓存行的所有元素的缓存都会失效。这就导致变更索引位1的元素，会导致索引位0的元素缓存也失效(操作时需要重新从主内存加载)。故而Disruptor做了一个缓存行填充的优化,在目标元素的前后都加了7个类型字段,两边都占据掉56个字节。故而保证每个元素都独占缓存行。是一种用空间换时间的优化。

4.04讲说过要拿个开源项目来分析，刚好我拿的也是mq，就借当前这个篇幅补充下。我看的是RocketMq，目前看完了路由信息管理中心，消息生产端和消息存储的逻辑。拿路由信息管理中心NameServer来说。
被抽象的模型对象是路由信息管理中心,既包含路由信息也包含路由信息的管理。路由信息由QueueData，Broker，TopicRouteData三个实体承载，路由信息管理由BrokerLiveInfo和RouteInfoManager负责。
提供了路由注册，路由发现和路由删除三个接口。
路由注册的接口触发是以Nameserver处理Broker的心跳包的方式接入的，具体代码见RouteInfoManager#registerBroker。
路由发现的接口触发Nameserver不管,由客户端定时请求获取路由信息，具体看DefaultRequestProcessor#getRouteInfoByTopic。
路由删除接口的触发是由Nameserver定时10S扫一遍brokerLiveTable。将超时120s的broker信息全部剔除。或者broker正常关闭会来调用。具体见RouteInfoManager#scanNotActiveBroker和unregisterBroker。

评价，
作为路由信息中心，功能相对简单，所以技术设计上就没太多好说的。比较突出的就是NameServer节点间不做信息同步，每个NameServer都单独接收broker的心跳维护路由信息。这样的设计无疑极大降低了NameServer实现的复杂度，毕竟集群内消息同步一直是个头疼的事情。但是这样的方式，在NameServer节点过多和broker节点过多的场景下感觉都会有性能瓶颈(单位时间心跳的次数增多和需要心跳通知的节点增多)。可是这样的设计依旧抗住了大规模集群的场景，用实践案例打了我理论感观的脸。
但作为一个apache开源项目，其代码实现风格实在令人难受。违反单一职责原则，NamesrvController做了外放接口，存储数据，启动定时等等一系列事情。且因为涵盖数据容器的职责，所以还需要再其他类中传递。违反依赖倒置原则，接口都找不到，就不用提啥基于接口而非实现编程了。如果要说这个项目的风格或者说代码设计偏好，那么就是没有原则，甚至都看不到阿里巴巴编程规范的影子。而这个问题不仅是在NameServer一个子模块中，而是在整个rocketMq模块都普遍存在。于此带来的就是，这个项目的新老交接，持续迭代，成本都会比较高。
限于篇幅，其他部分就不表了。rocketMq是个很优秀很成功的产品，但也因为它的光辉，目前其背后的代码实现才越显得格格不入。</div>2020-06-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/88/c8/6af6d27e.jpg" width="30px"><span>Y024</span> 👍（13） 💬（1）<div>很多开源项目都会是基于某篇论文实现的，而这篇论文也就成为该项目的灵魂。

对于 Kafka 来说，它的灵魂是：
https:&#47;&#47;engineering.linkedin.com&#47;distributed-systems&#47;log-what-every-software-engineer-should-know-about-real-time-datas-unifying

中文版本：https:&#47;&#47;www.kancloud.cn&#47;kancloud&#47;log-real-time-datas-unifying&#47;58708</div>2020-11-07</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/92/6d/becd841a.jpg" width="30px"><span>escray</span> 👍（7） 💬（2）<div>看一个项目的实现，主要是去看软件结构和关键技术。

类似于 Kafka 这样的“网红”开源项目，可以找到的结构图和相关资料不少，特别是官方资料还是比较权威的，比平时工作中接触到的那些陈旧代码要好很多。

文中对于 Kafka 的生产者消费者模型的初步提问，并不难以想到，生产者、消费者、集群连接；而后续问出更多的问题——网络抖动、集群……这个就比较需要功力了。

Kafka 的关键技术在于利用了磁盘顺序读写的特性，这个和 Disruptor 利用缓存填充技术颇有异曲同工之妙。而我前两天刚好在“数据结构和算法之美”的打卡活动里面，看过 Disruptor，印象颇深。

顺路去看了“深入浅出计算机组成原理”中关于 Kafka 的章节，还试读了两篇“Kafka 核心技术与实战”，确实应该认真的学习一下 Kafka，这个号称薪资排名比较靠前的技能。

我也好奇，面对 SSD 硬盘，Kafka 怎么办？</div>2020-06-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/18/84/0d/4e289b94.jpg" width="30px"><span>三生</span> 👍（3） 💬（2）<div>先后看了php的源代码和laravel，CI，Tp等框架的源码。从从组件到接口，从组件到模型，最后从模型到实现，走完一整个生命周期，学习到了很多优雅的设计，以及扩展如何接入，不过并不真的为什么会这么设计，设计的时候会解决什么样的问题，以及应用场景，当时还是在大学，所以实战经验不是特别丰富，于是自己想动手实现一下框架，看看为什么框架可以引用于不同的架构，逐步扩展，发现思想虽然相同，但是实现的优雅程度还是不可比拟。</div>2020-06-10</li><br/><li><img src="" width="30px"><span>Geek_3b1096</span> 👍（3） 💬（1）<div>现在有工作就不错了，想办法画出一张图，不是最糟</div>2020-06-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/a0/a3/8da99bb0.jpg" width="30px"><span>业余爱好者</span> 👍（3） 💬（1）<div>相同的功能可能要不同的软件产品。他们的接口与模型都是差不多的，不同之处就在于实现。所以理解这些产品族以及他们的差异就该从实现入手。

就像LinkedList和ArrayList都可以提供List的功能，但是实现的不同决定了他们各自不同的特性。使用时的选型还是要根据业务场景的需求来的。</div>2020-06-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/c9/92/6361802a.jpg" width="30px"><span>滴流乱转小胖儿</span> 👍（2） 💬（1）<div>带着问题去学习，确实目的性更强。 问题是想不出那么多问题怎么破？ 真是见功力的啊</div>2020-06-15</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTJbh5FQajwKhNlMrkoSklPpOXBtEYXCLvuWibhfWIS9QxHWDqzhEHJzEdmtUiaiaqFjfpsr2LwgNGpbQ/132" width="30px"><span>Geek_q29f6t</span> 👍（1） 💬（1）<div>关于结构图，我觉得可以包含这些内容：
1. 技术上：
* 前后端是如何关联起来的
* 系统怎么与存储系统通信的 （DAO？框架）
* 大的架构是什么？（MVC）
* 有没有最基本的3层架构

2. 业务上
* 各个模块是如何关联的。即：各个模块的Input和Output是什么

</div>2020-06-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/43/e1/b7be5560.jpg" width="30px"><span>sam</span> 👍（0） 💬（1）<div>给老师化繁为简的神奇能力点赞，很多概念让我这前端开发都豁然贯通了</div>2020-06-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/f9/88/cdda9e6f.jpg" width="30px"><span>阳仔</span> 👍（6） 💬（0）<div>分析软件系统的实现是以模型和接口为基础的。
模型是分层的，每一层都有对外的接口，上层调用下层的接口。
对一层进行展开分析，需要抓住两个关键点软件结构和关键技术。
其实思路就是对软件系统先有一个整体的认识，建立一个大概思维概念，然后再层层深入，剖析具体实现。
同时理解软件实现还要对操作系统有深入的认识，好的软件设计都会考虑软硬件的性能对软件设计的影响，这些操作系统的思想在指导具体开发软件过程中也是非常有意义</div>2020-06-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/17/14/c2/46ebe3a0.jpg" width="30px"><span>侧耳倾听</span> 👍（1） 💬（0）<div>嗯，道理懂了这么多，你依然写不出一个被接受的开源框架，这就是现实！</div>2022-03-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/a4/be/39cc22f5.jpg" width="30px"><span>petit_kayak</span> 👍（1） 💬（0）<div>Kafka利用消息队列有序的特定，软硬结合优化性能，这让我自己曾经做过的各种优化，很多时候也都是通过仔细分析业务数据的特点和硬件实际执行的方式，利用它们的结合点进行。</div>2022-01-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/d0/4d/2116c1a4.jpg" width="30px"><span>Bravery168</span> 👍（1） 💬（0）<div>软硬结合，这个思路很好。
解决问题需要打开思路，不应自我设限。打开思维边界以后，可能又是一片新天地。</div>2021-09-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/4a/10/365ea684.jpg" width="30px"><span>聪明的傻孩子</span> 👍（0） 💬（0）<div>这里面一句话最打动我，就是“如果你来设计一个消息队列，你会怎么做呢？”。分析源码和软件的核心就是带着问题去了解，第一个问题就应该是“如果这件事是我来做，我会怎么做”。比如Okhttp，它是在Android上最常见的Http的网络请求框架，第一个问题就是“如果我需要用http来封装一个网络请求框架，我会怎么做？”</div>2024-02-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/19/fd/58/1af629c7.jpg" width="30px"><span>6点无痛早起学习的和尚</span> 👍（0） 💬（0）<div>尝试理解模型和接口，上一层的接口其实可能是下一层的模型构成，比如这样理解不知是否恰当，比如整体模型的 kafka 的生产和消费接口是下一层的模型：生产者、消费者、集群 3 个模型组成</div>2023-08-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/06/96/4273bb09.jpg" width="30px"><span>遥远的救世主</span> 👍（0） 💬（0）<div>作者总结了“先模型，再接口，最后看实现”，以及具体的指明性方向如一定要带着问题，按图索骥，否则就会深陷代码细节，只见树木不见森林，事倍功半，是了解软件和学习三方框架源码的“道”。</div>2023-04-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/13/cd/a1429abe.jpg" width="30px"><span>快手阿修</span> 👍（0） 💬（0）<div>【勘误】音频9分48秒，如果是随机写，读成了如果是顺序写</div>2023-03-30</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/4a/6f/e36b3908.jpg" width="30px"><span>xzy</span> 👍（0） 💬（0）<div>掌握模型与接口是前提，带着问题，按图索骥（结构图），了解项目的关键技术</div>2022-10-31</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/23/f8/d2/cf38b12e.jpg" width="30px"><span>愿凌飞</span> 👍（0） 💬（2）<div>有一个想法不知道对不对
分析模型、分析接口、分析实现，这个好像递归一样。
当我们分析实现的时候，把模型的结构打开呈现在眼前，我们看到了下一层次模型的交错组合，这就为我们下一层次的模型的分析提供了方向。 当提到关键技术的时候，又好像是下一层的某一个关键模型设计的来龙去脉（存储模型不同实现）。感觉浸染到了下一层模型分析，像一个递归一样。
这又让我想到了树的遍历：深度遍历和广度遍历。我们在了解一个项目，分析软件设计的时候也可以这样，不同时候采取不同的方式。整体架构了解采用广度遍历高层次模型，关键模型的时候想要了解其内核时采取深度遍历。</div>2022-05-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/26/eb/d7/90391376.jpg" width="30px"><span>ifelse</span> 👍（0） 💬（0）<div>理解实现，带着自己的问题，了解软件的结构和关键的技术。--记下来</div>2022-05-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/21/f8/2b/339660f1.jpg" width="30px"><span>Wangyf</span> 👍（0） 💬（0）<div>一口气看完了 3 篇文章，作为一个刚上路的菜鸟，真是打开了新世界的大门，读完酣畅淋漓</div>2022-03-14</li><br/>
</ul>