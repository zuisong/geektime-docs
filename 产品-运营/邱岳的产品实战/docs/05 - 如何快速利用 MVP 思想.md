你好，我是邱岳，今天我分享的主题是：如何快速利用MVP思想。

在上一篇 “用最少的资源给你的产品试试水”中，我们谈到了最小可用产品MVP，并分享了几个关于它的经典案例。现在，让我们从例子里面跳出来，去看看怎么能快速地在自己的工作中利用 MVP 思想，这里有几个原则可以参考。

## 1.提前推演逻辑，不要盲目验证

在设计最小可用产品之前，一定要想清楚自己想验证的问题，要收集哪些数据项，还有这些数据项可能出现的结果，以及不同结果代表的结论。

这个事情有点像软件工程中的 TDD（测试驱动开发），先把想要得到的结果列出来，再反推设计，以免设计逻辑不清楚，或者漏掉数据打点，反倒浪费了资源。

比如我前面举的那个数据分析功能，我也是在推演的时候才发现需要多做一些数据功能，否则如果功能本身太简陋导致使用率高留存低的情况，就会难以辨别哪里出了问题。

另外，推演的时候还会提前去准备一些数据，比如使用率高，那么多高算高呢？这就需要去查一下在同区域其他类似功能的使用率。

这个过程本身也很有意思，你在心里默默估一个可能出现的数字，然后把功能做上去，再看看实际跑出来的数字，这个过程就好像谜底揭晓一样。

我觉得这个过程本身也是一种训练，就是你有判断，然后再看结果。时间久了，你可能会逐渐形成自己对于用户习惯，以及一些具体数字项的感觉。
<div><strong>精选留言（28）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/12/24/53/ee876b63.jpg" width="30px"><span>刘奥纳多</span> 👍（12） 💬（2）<div>请问打点是什么意思呢？</div>2018-08-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/89/4c/c268cc92.jpg" width="30px"><span>laulend™</span> 👍（7） 💬（1）<div>最近一直跟产品在争论一个功能，由于我们的用户特性，喜欢抽奖、抽券或者实物奖品，也做过小范围的测试，哪怕是插件，后来二爷家的抽奖助手支持嵌入功能，一直想接入二爷家的抽奖助手到自家的小程序做个MVP测试，如果效果反馈和好的话，那么就自己在页面上开发一个抽奖功能，支持自家优惠券抽奖等等，但是，产品一直不给做，非要自己搞一个抽奖功能，运营的延期和用户活动只能拖到一个月以后，对于这件事一直在撕逼，看完二爷的文章，我打算再去撕逼一次，不管成功与否，还是得去尝试一下。实在不行，推荐他们来看二爷的课程。</div>2018-08-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1c/1e/e4/ce9cac62.jpg" width="30px"><span>Cindy</span> 👍（0） 💬（1）<div>内部想孵化一个项目，市面上有完备的竞品，业务需求很大很多，怎么确保是mvp？</div>2020-02-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/8c/95/4544d905.jpg" width="30px"><span>sylan215</span> 👍（24） 💬（1）<div>1. 其实推演基本所有产品经理都会做，问题是，有些人的推演就是自己在意yin而已，所以推演的结果就不尽如人意了。

2. 长板理论逆袭木桶理论，赞。

3. 创造低成本方案这个我尝试补充一个，现在很多的业务和系统全都是云端化，但是 MVP 阶段其实可以不去搭建复杂的云端配合系统，虽然那个很灵活，但是处于验证的目的，完全可以使用硬编码，或者规则文件来做前期的配置，等量级足够大的时候，再去搞云端化。

4. 根据「增长黑客」的理念，MVP 主要是为了找到产品的 PMF 状态，所以二爷说的 MVP 思想，我理解为就是验证或者探寻产品真实的 PMF 状态，所有精力优先聚焦在这个上面即可。

以上，欢迎沟通交流，公众号「sylan215」</div>2018-08-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/3a/25/f5ef389a.jpg" width="30px"><span>木头人</span> 👍（13） 💬（1）<div>上面某位朋友，打点也称为埋点，解决数据采集的问题。</div>2018-08-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/26/4b/bc3daee8.jpg" width="30px"><span>牛小妞</span> 👍（7） 💬（1）<div>印象最深的利用MVP快速验证产品的是多抓鱼，最早他们就是建立微信群人工发书单，人工下单转账来使业务跑起来的。</div>2018-08-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/94/56/4b8395f6.jpg" width="30px"><span>CC</span> 👍（6） 💬（0）<div>之前我在制作MVP产品有两个误区。

一是认为动手比推演重要，觉得推演很久不如动手制作，认为动手才是获得结果的捷径。实际上产生这个误区的原因是战略上的懒惰，没有深入思考制作MVP产品的目的，结果绕了一个大弯路。

之前读过一篇文章，依稀记得，某个大牛在短短一个周末就鼓捣出了一个MVP产品，验证了想法。我只记住了结论，却没有记住逻辑推演过程，以及项目之前的准备。他之所以能做成，一是之前做过推演，二是有自己想要验证的明确目标。

第二个误区是要求完美，过度担心用户的负面口碑，这就导致不仅把资源浪费在产品的短板上，还下意识的拒绝采用灵活的低成本方案，比如人工方案。

会使用工具的人，比如会写代码，某种程度上也是受到知识诅咒，很容易一大步跨入产品细节，考虑实现方式，考虑如何做出一个完美的产品，而不是投入时间在推演上。

明确目的，然后行动。</div>2018-08-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/26/7e/54e086f0.jpg" width="30px"><span>胡氏</span> 👍（4） 💬（0）<div>有个小优化提下：播放可操作的进度条，比如返回重复听那一段话，倍速听；可跳选时间进度；</div>2019-02-25</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/8e/8b/38b93ca0.jpg" width="30px"><span>听天由己</span> 👍（4） 💬（0）<div>关于人工替代系统，这对创业公司来说，更是常见。很多时候，我们想要验证一个功能的适用性，我们想得特别完美，可是资源有限，也只能先实现最核心的特性。例如，在赛事系统中，组织者很希望在报名结束后导出名单，这一需求并不着急，我们完全可以通过人工导出 Excel 表格的方式进行沟通。

还有一点，产品不够，运营来凑，这话一点都不假。哪有上来就完美的产品？我们更重要的是展现自己的理念和态度，建立产品与用户之间的信任，然后快速响应和迭代，这样才有重视感和成就感。运营工作的确不必可少。</div>2018-08-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/3e/5b/3e547777.jpg" width="30px"><span>Symon</span> 👍（3） 💬（1）<div>这一节超实用，我们在做B端产品时，很多时候一些功能都是低频的操作，这时候人工反而比系统更优化些（从成本和灵活性角度来看，毕竟新产品的体量还没有那么大）！</div>2018-08-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/91/32/9386e7ed.jpg" width="30px"><span>时间之树</span> 👍（3） 💬（0）<div>特别关注了二爷讲到的关于MVP的局限性。任何理论和方法，都有他的使用条件和适用边界。只有充分了解它的局限性，才能更加有针对性的去使用。</div>2018-08-08</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/ktzqVgXgRT94bm0H3bhvk7ODs0KlOCtdYhISuUzOYIz6LYjicYxcHLEoVfWdMCovLmoGU7oHMoOdgg2BDqB0W0A/132" width="30px"><span>J不湿</span> 👍（2） 💬（0）<div>MVP是种思维，可以根据不同情况进行调整优化方法</div>2019-04-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/25/31/c6/2dbc10e5.jpg" width="30px"><span>铛丹丹</span> 👍（1） 💬（0）<div>那么mvp是由产品还是运营来确定呢？毕竟产品觉得合适的mvp可能运营觉得不合适。</div>2021-04-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/19/5b/08/b0b0db05.jpg" width="30px"><span>丁丁历险记</span> 👍（1） 💬（0）<div>每一个MVP其实是需要洞见的，
不然真的是瞎hb乱扯。
舍弃是一种能力</div>2021-03-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/7d/78/0181656d.jpg" width="30px"><span>孙伟贤</span> 👍（1） 💬（0）<div>局部最优和全局最优的思考也很重要，产品其实都在努力控制系统和产品的熵，也就是局部系统有序和全局系统有序，也是走向产品架构的必由之路，回去想某个局部最优解可能会导致全局系统紊乱，到这个阶段的产品思考能力就是上等了，比如竞价排名，负面反馈，举报，敏感词等功能的意义，以及如何控制他们的负面效应</div>2018-08-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/1a/d0/72820980.jpg" width="30px"><span>张叔夏</span> 👍（1） 💬（0）<div>订阅数码博主的内容推送不会是不鸟万如一的会员吧</div>2018-08-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/8e/8b/38b93ca0.jpg" width="30px"><span>听天由己</span> 👍（1） 💬（1）<div>与其更好，不如不同。这话放在今天这个时代，更是如此。中国这样的人口特征与需求分层让我们有机会尝试各种各样的产品设计与理念，可是同类产品的核心功能特性在哪里，一定要在第一版产品上线初就想好并且完善。

产品本身是服务的一部分，二爷提到的 12306 就是典型的例子，这样的资源型产品，有足够多的资源可供用户来选择，才是最为关键的一点，因而产品体验要更靠后了。若是连票都没有，这样的产品有作用？

梁宁老师说，产品要有系统能力，无论是技术支持、核心资源、市场营销、后勤客服等方面，每一项都是用户体验的一环，光靠产品本身出彩，是不足以支撑后续发展的，这样的例子就像几年前大火的足迹、脸萌等。</div>2018-08-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/66/43/c48c0c0e.jpg" width="30px"><span>冯广</span> 👍（0） 💬（0）<div>MVP最大的优势就是节省资源，让关键目标关键服务快速实现，但是不是所有的事情都可以借用MVP，或者说MVP的程度需要好好把握，因为当前处于流量红利消失殆尽的阶段，我们左右有大量的同质化竞争，很多时候是能不能成拼的是系统能力，拼的是细节的体验。</div>2021-09-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/c4/03/f753fda7.jpg" width="30px"><span>JianXu</span> 👍（0） 💬（0）<div>我们最近在做Kubernetes 的前端体验，我其实也在想我们的长板到底是什么？目前Kubenetes 各个对象之间互相navigation 非常不方便，所以我们用graph DB 做了一个索引，但是问题是为什么用户需要在不同对象之间navigate 呢？我觉得一个是看到自己应用的相关资源，一个是排查问题。 相关资源的展示方式我觉得还是应该从用户角度来看，比如我们内部的TFAP , TFD 这些概念不是最优展示方式；而排查问题应该是我们在做上层的抽象上直接给出来。</div>2020-12-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/23/d6/3b/3e8ed6a3.jpg" width="30px"><span>你是谁呀</span> 👍（0） 💬（0）<div>长短板理论很赞，不过短板差到不及格应该也不太行？结合负面口碑效应，短板太短也会损害产品</div>2020-12-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/56/ee/3d00ac06.jpg" width="30px"><span>Ivan.YAO</span> 👍（0） 💬（0）<div>二爷对于MVP的讲解非常透彻</div>2020-12-16</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/04/37/aa04f997.jpg" width="30px"><span>和小胖</span> 👍（0） 💬（0）<div>mvp可能对于小功能的验证以及尝试更为有效。也是一种决定是否要大量推某个功能的依据。</div>2018-12-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/79/7e/c38ac02f.jpg" width="30px"><span>北冥Master</span> 👍（0） 💬（0）<div>能讲讲抽奖助手和readhub两个工具的mvp 1.0做了些什么功能，留了什么未完成功能？</div>2018-11-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/b2/cb/5f963fbb.jpg" width="30px"><span>🤖</span> 👍（0） 💬（0）<div>笔记：
MVP裁剪-留住长板
解决方案-减少开发成本，人力验证服务是否靠可以落地；第三方平台验证产品idae
根据自身产品形态和自身资源，选择最合适的产品验证方式，MVP并不适合所有产品不是唯一原则</div>2018-08-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/4b/3b/a02ab724.jpg" width="30px"><span>四毛</span> 👍（0） 💬（0）<div>在小程序这类开发成本较低的平台上，是否也有MVP的必要呢？</div>2018-08-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/20/3b/c94a4b62.jpg" width="30px"><span>我叫什么来着</span> 👍（0） 💬（0）<div>期待后面的分享中多一些工作中的具体案例</div>2018-08-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/1a/04/8c327014.jpg" width="30px"><span>Novelty</span> 👍（0） 💬（0）<div>对二爷所述两点印象尤深，第一是验证长板，第二是对于领域相对成熟的产品而言，产品体验细节的叠加才能构建出核心竞争力，而mvp可能很难将它构建出来。

自己在利用MVP过程中踩过挺多坑，个人体会对于MVP方法而言，可能更适用于一些开创性的设计或是不为市场中大多数人所熟知，我理解就是二爷所述的长板，这样可以避免用户对产品新功能不完善的不满，反而能增强其体验完整版的期望。

我们此前设计过的一款功能，在进行测试时，用户点击量很高，但留存却很差，后来得知是用户因我们产品部分基础功能体验不好，而影响到他对新功能的整体体验。
</div>2018-08-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/4c/62/e5dd183f.jpg" width="30px"><span>子洋</span> 👍（0） 💬（0）<div>MVP只是工具，无法代替产品经理的核心思考。但是能用好工具的人其实也不多。</div>2018-08-08</li><br/>
</ul>