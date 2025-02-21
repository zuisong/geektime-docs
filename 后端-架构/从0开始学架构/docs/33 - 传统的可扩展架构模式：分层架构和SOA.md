相比于高性能、高可用架构模式在最近几十年的迅猛发展来说，可扩展架构模式的发展可以说是步履蹒跚，最近几年火热的微服务模式算是可扩展模式发展历史中为数不多的亮点，但这也导致了现在谈可扩展的时候必谈微服务，甚至微服务架构都成了架构设计的银弹，高性能也用微服务、高可用也用微服务，很多时候这样的架构设计看起来高大上，实际上是大炮打蚊子，违背了架构设计的“合适原则”和“简单原则”。

为了帮助你在实践中更好的进行可扩展架构设计，我将分别介绍几种可扩展架构模式，指出每种架构模式的关键点和优缺点。今天我来介绍传统的可扩展模式，包括分层架构和SOA，后面还会介绍微服务架构。

## 分层架构

分层架构是很常见的架构模式，它也叫N层架构，通常情况下，N至少是2层。例如，C/S架构、B/S架构。常见的是3层架构（例如，MVC、MVP架构）、4层架构，5层架构的比较少见，一般是比较复杂的系统才会达到或者超过5层，比如操作系统内核架构。

按照分层架构进行设计时，根据不同的划分维度和对象，可以得到多种不同的分层架构。

1. C/S架构、B/S架构

划分的对象是整个业务系统，划分的维度是用户交互，即将和用户交互的部分独立为一层，支撑用户交互的后台作为另外一层。例如，下面是C/S架构结构图。
<div><strong>精选留言（30）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/10/15/ca/bf3fb655.jpg" width="30px"><span>Lee</span> 👍（232） 💬（5）<div>SOA是把多个系统整合，而微服务是把单个系统拆开来，方向正好相反</div>2018-07-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/6a/21/fe356d0b.jpg" width="30px"><span>辉辉</span> 👍（89） 💬（1）<div>soa是集成的思想，是解决服务孤岛打通链条，是无奈之举。esb集中化的管理带来了性能不佳，厚重等问题。也无法快速扩展。不适合互联网的业务特点</div>2018-07-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/ac/ed/d868396d.jpg" width="30px"><span>铃兰Neko</span> 👍（53） 💬（2）<div>尝试说下个人浅见:
为什么互联网不用SOA?
1. 互联网企业, 通常比较年轻, 没有那么多异构系统, 技术是公司的关键;
如果有整合或者服务化的需求, 公司有人也有钱专门搞这个; 拆到重做&#47;重构 很平常;
相反的, 传统企业, 举个例子: 
某传统炼钢国企 : 有多个遗留.net系统,有几个实习生做的java系统, 有基于数据库procedure的系统;
有各种已经倒闭了的第三方企业的系统 等等;
企业领导不会有精力和想法全部推倒重来, 只会花钱请第三方 , 成本越低越好; 
这个时候就需要ESB这种总线
2. 传统企业IT追求的是&quot;需求灵活,变更快&quot;, 而互联网企业追求性能, 传统soa 性能不佳
传统的esb ,说实话, 使用webservice 以及soap这种基于xml的技术;
wsdl 这东西是真的难用, 难学难用难维护 ; 结构冗杂;
3. soa 这个东西很多时候只是一个概念, 而不是实践
个人觉得, 现在的微服务 , 更像是 soa 思想的一个落地 (相比esb)	</div>2018-07-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/bb/cc/fac12364.jpg" width="30px"><span>xxx</span> 👍（23） 💬（1）<div>一直不明白SOA和微服务的具体区别，知道作者讲到了ESB 的功能，原来就是适配各种协议，顿时明白了!SOA是为了适配老系统。</div>2019-10-25</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTIvMlvSXsYgJibIyDO78gPacZR1qukEOJrpfHAJmyGVtWPO3XMqVA9dImHhGJm2icp6lDuBw1GrNDbA/132" width="30px"><span>赤脚小子</span> 👍（18） 💬（1）<div>回答问题:文中也说了，soa是特定历史条件下的产物，为了适配各种异构的it系统，而有如此多系统的自然是变化减少且稳定的传统企业。互联网企业的特点就是小，新，快。没有历史包袱，变化快，大部分是从单体演进到分布式，技术栈一脉相承或者在分布式之前已经从php,ruby等改造到java等了。而到了分布式之后，面对不断的耦合，系统复杂度的陡增，这时一个soa的特例微服务出现了。
实际上soa的思想还在，只不过实现的方式不一样了。</div>2018-07-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/d3/3c/ab6425f7.jpg" width="30px"><span>hello</span> 👍（14） 💬（1）<div>soa解决的是资源的重复利用，它的拆分粒度比较大，比如财务系统跟oa系统的员工模块。1.互联网企业有几种情况，1.初创公司，这种公司一般会有试错的过程，需要技术快速实现业务落地，这种情况下使用SOA不适合快速敏捷迭代开发。2.对于成熟的互联网业务来说，需要解决的是是高并发，高性能和高存储等一系列问题，对于这类企业来说，使用SOA拆分不能解决太多问题，还得做更加细粒度的拆分。</div>2018-08-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/cf/bb/22af0e52.jpg" width="30px"><span>孙振超</span> 👍（12） 💬（1）<div>在传统企业从原先的手工作业转为采用IT系统作业的过程中，大多是采用向外采购的方式逐步实现的，在这个过程中不同部门采购系统的实现语言、通信协议并不完全相同，但为提升运行效率又要能够做到企业内部信息互通、相互协作，这是soa诞生的背景。
而互联网企业是新创的企业，没有这么多的历史包袱，同时出于快速迭代的要求，有时会自建所需的系统，即使是对外采购，也会选择和已有系统对接方便的系统，从根本上避免了相关问题，因而soa在互联网公司中使用不多。</div>2018-09-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/5f/1e/18ef8e84.jpg" width="30px"><span>7侠</span> 👍（8） 💬（1）<div>    SOA更像一种架构理念，不够具体。在传统企业的IT系统中落地为ESB，主要是为了集成异构系统。因为传统企业特别是大型企业的历史长，在其发展过程中自己开发或采购了不少异构系统。
    而互联网企业历史都短(腾讯98年，阿里99年，百度2000年)，很少有遗留异构系统(像阿里的系统绝大部分应该都是Java开发的吧？)。像阿里这种互联网大型企业的痛点是随着业务越来越多，整个系统成了个巨无霸(可能是数以千记的模块数)，模块之间的调用像蜘蛛网，极大降低了开发、测试、部署、运维的效率，所以把庞大的业务逻辑层又切分成了业务更独立的应用层和公共功能模块组成服务层。接下来一是要提供应用层与服务层之间、服务层内部服务之间的高效通信机制，二是要对大量的服务进行治理，于是分布式服务框架出现了(阿里就出了Dubbo和HSF两个服务框架？)。感觉在大型互联网企业，SOA实际是落地为分布式服务框架，它更像是微服务架构的一个雏形，服务框架提供的功能实际也是微服务架构里必不可少的功能。</div>2019-05-04</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/fc/34/c733b116.jpg" width="30px"><span>何磊</span> 👍（6） 💬（1）<div>soa主要是为了解决历史遗留问题，引入的esb。而互联网企业都年轻，没有历史包袱，另外互联网企业大部分都需要高性能，而esb可能成为瓶颈。
最后想咨询老师一个问题：在分层结构中。同层能不能互相调用？比如：下单时，需要用户信息，此时应该调用同层用户模块来完成，还是如何处理呢？</div>2018-08-10</li><br/><li><img src="" width="30px"><span>yason li</span> 👍（5） 💬（1）<div>其实，个人理解的传统SOA和ESB在互联网企业之所以不怎么使用主要原因就是中心化的ESB架构会逐渐成为性能、可用性、可扩展性的瓶颈。但是SOA的思想本身是没有什么问题的。互联网企业中用的微服务甚至最近很火的Service Mesh都可以看成是SOA、ESB的变形。比如Service Mesh也可以看成是一个去中心化的ESB。</div>2018-07-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/7a/4b/1a7b36ab.jpg" width="30px"><span>欧星星</span> 👍（4） 💬（1）<div>1.没有历史包袱
2.SOA架构太重，ESB容易成瓶颈
</div>2018-07-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/18/cb/edb5a0a0.jpg" width="30px"><span>小橙橙</span> 👍（4） 💬（1）<div>老师，有个疑问并不是很理解，互联网企业多数是采用微服务架构，那微服务不属于面向服务SOA架构的范畴吗？</div>2018-07-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/3b/85/df328870.jpg" width="30px"><span>tim</span> 👍（3） 💬（1）<div>soa是不是可以分成两部分：
1.服务化的思想，这个就是SOA 。
2.带有ESB 的实践，这个是针对当时问题的一种解决方案。

如果是这样其实微服务就是SOA的另一种实践。互联网公司其实是用了SOA的，不过esb和服务划分粒度已经不适合他们的场景了。

先接触了分布式和微服务，对SOA不是很了解，感觉都是分而治之的思想，粒度渐细，自动运维什么的附属产物</div>2019-06-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/30/ff/b3e54147.jpg" width="30px"><span>雨幕下的稻田</span> 👍（3） 💬（1）<div>第一章说MVC是开发规范，本章节说MVC是分层架构，不太明白，这两MVC说的不是一个东西吗，还是出发点不同</div>2019-02-15</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/wBibtTTkiaGtcJ3qBeG4BnB4MmaurYf8hZTrXiczmvLHlRrqxJicRaoQPAZ0vw9HHd7yxDH27TLCzBQqqOqyGukw1g/132" width="30px"><span>gen_jin</span> 👍（3） 💬（1）<div>我觉得有三点～互联网企业1.没有老系统包袱，2.钱多 3.需求变化快 2c性能及并发量要求高，三高(高性能 可用 扩展)，传统soa(esb)无法满足。</div>2018-07-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/d4/c2/910d231e.jpg" width="30px"><span>oddrock</span> 👍（3） 💬（1）<div>一、互联网企业的it系统大多数都是自己的it部门开发的，不存在太多异构问题，可以有较好的内部服务规范，因此不需要soa和esb去做异构系统的屏蔽和互通
二、esb的总线型架构会导致一定程度上的性能问题，因此互联网企业一般采用分布式服务架构
三、esb实质是用空间和时间换取it系统架构的有序性，esb本身有采购或研发费用，esb部署也要服务器，这些成本对互联网企业都是不必要的</div>2018-07-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/c5/68/7afb7304.jpg" width="30px"><span>narry</span> 👍（3） 💬（1）<div>互联网行业很少采用soa，感觉有两点原因:1）soa主要是解决异构系统之间的集成，传统企业有大量的异构系统，而互联网属于新兴行业，不存在大量的异构系统需要集成，2）esb存在性能的瓶颈和不易扩展的问题，无法应对互联网这种业务会快速增长场景</div>2018-07-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/c6/e5/7e86498f.jpg" width="30px"><span>cqc</span> 👍（2） 💬（1）<div>我觉得主要有以下几个原因：
1.互联网公司大多比较年轻，没有已有系统的历史包袱，所以不用考虑各种兼容的问题；
2.互联网公司大多业务量都比较大，对于性能要求比较高，所以不会优先考虑SOA</div>2018-07-12</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/DYAIOgq83eozpyAUaM6ra1hqeIsd4v0fulS4zVmxDM3LQyqGo0BFM141QpQnSib6oHdQricGrRxusp5rflGn54ew/132" width="30px"><span>甜宝仙女的专属饲养员</span> 👍（1） 💬（1）<div>旧的不合时宜的东西就要舍弃掉，斯科特·派克说过：懒惰是人的“原罪”，改变是人的“原恩”。</div>2022-11-04</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/c4/e0/eb9f6b80.jpg" width="30px"><span>Rainbow福才</span> 👍（1） 💬（1）<div>SOA架构用来整合传统企业已有子系统，微服务架构用来拆分负责业务系统。</div>2022-03-01</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/b0/cd/c1fa2a66.jpg" width="30px"><span>沐雪</span> 👍（1） 💬（1）<div>原因有3：
1、SOA出现的背景是 各种异构系统的不同协议之间的融合；而互联网行业根据就没有这个需求。
2、SOA服务的粒度不好控制，但是肯定是微服务粗。
3、SOA实现比较复杂，比较重。
</div>2022-02-07</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/ff/28/76d736e3.jpg" width="30px"><span>DDL007</span> 👍（1） 💬（1）<div>企业经营本质上是业务运营。在技术对业务的贡献度上，传统企业的认识远没有互联网企业认识深刻，即便有认识，投入上也远远不够。互联网企业则是既有认识，又愿意投入。所以，EBS对传统企业是在将就，互联网企业则是想办法彻底解决，后者显然是不将就的，也就不会引入EBS。</div>2021-12-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/88/18/9744d5ec.jpg" width="30px"><span>小超人</span> 👍（1） 💬（1）<div>互联网企业没有传统企业这么多的历史包袱， SOA 主要是解决现有的多个系统的协调问题
</div>2021-10-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1d/44/a0/16d0d300.jpg" width="30px"><span>ZHANGPING</span> 👍（1） 💬（1）<div>互联网本身就是技术和业务对半的性质，有技术问题，就解决即使问题。而传统行业：IT只是一个解决问题的工具，并不擅长技术。</div>2021-07-17</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/0lTiaKqiba7pqubScfQVtkuphwxD529icZMOgRjO5icxhF79mvs2JMp0XIOMGy24bkh79icCNPDDOeicKWuqMmMz0vfQ/132" width="30px"><span>Geek_626167</span> 👍（1） 💬（1）<div>首先各个服务之间可能会有很多共同的功能模块，如果按服务划分，可能存在重复开发的问题；其次，ESB层建设耗费大量资源但收益是很低的。
互联网服务往往单个服务是瓶颈，适合逐个优化扩展，如果建设ESB这种集中层，反而会拖垮整个系统，如果基于服务做拆分更适合用微服务架构。</div>2021-07-16</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/0e/a1/717e2768.jpg" width="30px"><span>磊吐槽</span> 👍（1） 💬（1）<div>可能是ESB 很贵，而且还不单独销售</div>2018-07-12</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/7P4wtgRQt1l0YQlVOtiaUKey2AFZqQCAcABzdCNTP0JR027tkhVkRYgj1iaYF8OlqsE8j6A6icsAvYHIAX8E31WNg/132" width="30px"><span>killer</span> 👍（0） 💬（1）<div>我们公司刚好用过ESB，用了之后发现弊大于利，最后全面重构下线了，说说我的看法（ps，现在评论不晚吧）。
1、只做了转发能力，a服务-&gt;esb-&gt;b服务，还需要配置规则，维护成本高，完全可以a服务-&gt;b服务就完事儿了；
2、企业大面积接入ESB，有些接口流量非常高，比如组织架构接口，整个系统都依赖了，很快遇到性能瓶颈；
3、稳定性差，核心业务都接了ESB，ESB挂掉核心业务全死掉。
总结就是：性能易瓶颈、扩展性差、稳定性差。但说复杂度吧，微服务也不低。</div>2024-11-25</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/b5/57/93df54ef.jpg" width="30px"><span>Xu Sheng</span> 👍（0） 💬（1）<div>因为互联网公司大部分是新公司，没有那么多的旧系统要整合。</div>2024-10-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1f/55/6c/cad715eb.jpg" width="30px"><span>Archer</span> 👍（0） 💬（1）<div>两方面考虑：1.存在重复开发，SOA虽然分出了服务的概念，但是是将系统视作一个大的服务，系统内部的功能仍然存在重复建设的情况。2.成本，互联网企业内部的系统大多是自建的，也好维护，所以更容易实现接口的统一，也更容易拆分出更细粒度的服务来减少重建成本</div>2024-03-18</li><br/><li><img src="" width="30px"><span>陈峰</span> 👍（0） 💬（1）<div>关于 逻辑分层架构 的疑问

现在的系统，一般都是采取这种架构进行编码的吧，但是，其中提到了，需要 严格的分层，否则容易对后续维护产生混乱。

但是，对于这一点，我有一些不同的看法，请教一下。

就比如，像我们项目组的规模比较小，如果采取强行强制分层，实际上对较少人维护的项目，是反复的冗余编码，虽然看似扩展性高了，实际场景下，大多数层是无需改变的。

那么，依据最初说的简单合适原则，我感觉分层架构其实也可以对于一个系统部分应用，部分跨层调用。

因为对于不会变的代码，其实无需考虑其扩展性，仅仅需要保证层间数据流向是自上而下就可以了。

在我自己设计过的几个模块，我感触比较深，最初都是严格按分层去写，但实际上维护人员很少，大部分代码在业务固定后基本不可能改动。所以，最新这个项目，我并没有保持严格的不允许跨层，而是对于可能变动的地方设计接口，保证可扩展性和不跨层调用，对于不会变动的地方直接进行夸层调用。

而且，如果发现有地方需要重新抽象接口进行分层，及时进行重构和分层还算是有一定的维护性。

我并不知道，我这样的做法在老师看来是什么样的，希望听一下老师的意见。</div>2023-10-26</li><br/>
</ul>