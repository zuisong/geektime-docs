你好，我是七牛云许式伟。

架构的本质是业务的正交分解。

在上一讲 “[61 | 全局性功能的架构设计](https://time.geekbang.org/column/article/173619)” 中我们提到，架构分解中有两大难题：其一，需求的交织。不同需求混杂在一起，也就是存在所谓的全局性功能。其二，需求的易变。不同客户，不同场景下需求看起来很不一样，场景呈发散趋势。

我们可能经常会听到各种架构思维的原则或模式。但，为什么我们开始谈到架构思维了，也不是从那些耳熟能详的原则或模式谈起？

因为，万变不离其宗。

就架构的本质而言，我们核心要掌握的架构设计的工具其实就只有两个：

- 组合。用小业务组装出大业务，组装出越来越复杂的系统。
- 如何应对变化（开闭原则）。

## 开闭原则（OCP）

今天我们就聊聊怎么应对需求的变化。

谈应对变化，就不能不提著名的 “开闭原则（Open Closed Principle，OCP）”。一般认为，最早提出开闭原则这一术语的是勃兰特·梅耶（Bertrand Meyer）。他在 1988 年在 《面向对象软件构造》 中首次提出了开闭原则。

什么是开闭原则（OCP）？

> 软件实体（模块，类，函数等）应该对于功能扩展是开放的，但对于修改是封闭的。

一个软件产品只要在其生命周期内，都会不断发生变化。变化是一个事实，所以我们需要让软件去适应变化。我们应该在设计时尽量适应这些变化，以提高项目的稳定性和灵活性，真正实现 “拥抱变化”。
<div><strong>精选留言（30）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/13/17/27/ec30d30a.jpg" width="30px"><span>Jxin</span> 👍（22） 💬（4）<div>笔记：

将开闭原则上移到业务系统。业务对外只读，意味着不可变，但不变的业务生命周期是很短暂的，所以要可扩。要扩展还要不变，就倒逼着要做兼容，而兼容可能会导致现有的功能职责不单一，这又倒逼着要对现有的功能做再抽象，以适应更广的“单一职责”。

所以不改是不可能的，只是改的结果应当是让项目往更稳定去发展。然而这里面其实好难，无论是新的抽象的定义还是职责范围的扩张，这都需要有强大的分析能力和精湛的设计思维、重构手法、调优能力以及站在核心目标上的权衡来支撑。然而难亦是乐趣所在。</div>2019-12-06</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/34/df/64e3d533.jpg" width="30px"><span>leslie</span> 👍（22） 💬（2）<div>  老师的课程中提及的两方面是我觉得自己理解的最不好的：一方面&quot;基础架构 + 业务架构，才是你设计的软件的全部&quot;，另一方面&quot;一方面从中学习怎么做需求分析，另一方面也从中体悟做架构的思维哲学&quot;。
      如同老师所说的&quot;架构课 的革命性，我自己从没怀疑过。它的内容是精心设计的，为此我准备了十几年&quot;,学习的过程中我其实同样在整体梳理自己作为DBA&amp;&amp;OPS十余年松散的知识体系。老师开课的这半年多不断的适度扩展梳理去破未知，完成了20余门功课的学习；除了画图部分的知识都是在不断的循环梳理。虽不断学习和梳理，但是依然觉得老师今天课程中提及的两方面其实是最难。如同前几天DevOps课程的石老师课程提出的Plan-Do-Check-Act时，我说这个顺序其实可以改变且石老师的回复中对此非常认可一样。这个认知其实是原来许老师课程的循环反复，梳理中悟出的东西。
      结合老师上堂课所提及&quot;任何功能都是可以正交分解的，即使我目前还没有找到方法，那也是因为我还没有透彻理解需求&quot;-可以理解为业务方面的。《全局性功能的架构设计》和《重新认识开闭原则》两章内容在强调今天课程结束老师的&quot;基础架构 + 业务架构，才是你设计的软件的全部&quot;。
      以上是个人结合这两节课的知识对于今天课程结束部分老师的理解：谢谢老师的分享和教诲。期待老师的下次分享。</div>2019-12-06</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/9b/a7/440aff07.jpg" width="30px"><span>风翱</span> 👍（9） 💬（1）<div>活字印刷术，也是开闭原则应用的一个例子。 字是稳定的，字的排序是变化的。</div>2021-05-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/62/a7/3e6fee86.jpg" width="30px"><span>K战神</span> 👍（8） 💬（1）<div>许大，希望出书。买来收藏。

时不时枕边翻阅体会大佬的思想。

多年以后，庆幸自己这段时间跟着许大的专栏，有了新的想法和思想。</div>2019-12-06</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/24/df/645f8087.jpg" width="30px"><span>Yayu</span> 👍（5） 💬（4）<div>如何理解“只读”模块？</div>2019-12-06</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/2d/fa/72/ffb60db2.jpg" width="30px"><span>swchen</span> 👍（3） 💬（2）<div>对于程序员而言，三种思维最为基础: 
1.DRY (Don’t Repeat Yourself) 。
   这是好程序员的根本追求，永久的驱动力。
2.分而治之。
   这是人类解决复杂问题的普遍方式。
3.开闭原则。
   这是应对变化(主动的变化如功能扩展，被动的变化如故障修复)的最佳手段。

其他各种原则&#47;方法&#47;模式&#47;最佳实践，全部都是以此三者为基础，结合具体领域&#47;场景&#47;时代的更具操作性的推论。</div>2022-05-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/29/24/60772229.jpg" width="30px"><span>另存为……</span> 👍（3） 💬（0）<div>老师，最近在了解区块链相关的知识，感悟到了一些开闭原则上的应用，跟您探讨下：
比特币旨在构建新一代的数字货币，而以太坊的目标则是要成为新一代点对点的分布式计算基础服务（终极目标是成为 web3.0 的标准），基于此发展除了智能合约，所谓“智能合约”，实际就是可编程的合约，跟我们普遍理解的“智能”没啥关系，那既然是程序，必定会涉及到升级或修复，业务数据存储结构变更，而区块链的特性决定了“变更”是一项成本极其高昂甚至几乎无法完成，我们称之为不可篡改特性，因此现在做dapp涉及一般设计为数据合约和程序逻辑合约组合，做到程序和数据分离（由此也可以看出对比中心化的程序还是相当原始和初级的），这样在程序更新的时候直接弃用旧的合约地址，改用新合约，数据也不用迁移，但是当我们的需求需要持续更新合约的时候，如果能懂得运用开闭原则，这件事情会优雅很多，因为无论是 以太坊的 ERC20 还是 ERC721 标准等等，都规定了相当有限且简单的接口标准，这就是架构的不可变部分，我们不能把所有的逻辑都堆在这个我们针对于接口的实现上，而应该采用组合的方式，通过合理的架构设计，多个合约组合出强大的功能，我看了几条最新的以太坊社区提案，一些针对于 NFTs 的提案，比如 ERC-998，旨在让多个 NFT 组合的新 NFT 具备不可拆解的特性，使新的NFT可以整体交易，这会极大的简化物品转移的处理，其实都是可以遵循开闭原则通过良好合理的设计组合合约来实现，没必要升级为最基础的接口标准，当然这也会带来 gas 成本的增加，因为运行在区块链上的程序是需要支付 gas 费用的，所以币安推出  bsc 币安智能链的原因之一，降低 gas 费用。</div>2021-12-25</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/fc/34/c733b116.jpg" width="30px"><span>何磊</span> 👍（2） 💬（1）<div>老师对于开闭原则，我也在思考这里的开、闭到底是针对什么的。
首先对于bug坑定是需要修复的；那么如文中提到的，对于需求的变化引起需要修改利用插件机制。但是实际的业务中，可能很多是需要在原有代码中增加一个if判断、或者类型转化、或者额外的数据处理。

针对这些问题，肯定不可避免要去对源代码产生修改。这里很难去控制什么时候可以改，什么时候该用插件</div>2020-07-16</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTJjXbIia8iavTicWJib3xteYYkx6yeeLVr5HV1ibiay0QoIuaf74NvCCL1Z7ZnLYTpTh29AdsNAJkZfgFwA/132" width="30px"><span>Geek_adf1c9</span> 👍（1） 💬（2）<div>开闭的核心还是明确“变与不变”，这很难，需要大量的需求分析</div>2022-05-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/d0/4d/2116c1a4.jpg" width="30px"><span>Bravery168</span> 👍（1） 💬（1）<div>需求稳定点与变化点，正交分解，开闭原则，我理解内在本质是一脉相承的。这种架构看看作一种生命体，在基础构造上是稳定的，但又具备足够的柔性和灵活性。在业务变化时能够灵活适应，同时又不会散发臭味。有了这种特质，这种架构才可以说是有生命力的。</div>2020-02-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/62/a7/3e6fee86.jpg" width="30px"><span>K战神</span> 👍（1） 💬（1）<div>许大，我们真的要考虑，将老的需求放入版本库。对于新的重新实现一个新的。

会不会最后系统会有很多名字类似业务有所区别的接口？</div>2019-12-11</li><br/><li><img src="" width="30px"><span>Geek_88604f</span> 👍（1） 💬（1）<div>        在业务正交分解的过程中必然会遇到以前分解好的模块需要调整的情况，比如说随着新模块的加入发现和老模块的部分实现有重复的情况。这种情况下是保持新老模块的重复部分呢还是抽取出共同的部分作为更基础的支撑模块呢？如果要抽取共同的模块必然会涉及老模块的修改，这种情况是否有违反了开闭原则呢？更进一步开闭原则和重构的关系应该如何处理？</div>2019-12-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/bc/25/1c92a90c.jpg" width="30px"><span>tt</span> 👍（1） 💬（1）<div>本课感受最深的一句话：

“第二，模块的业务变化点，简单一点的，通过回调函数或者接口开放出去，交给其他的业务模块。复杂一点的，通过引入插件机制把系统分解为 “最小化的核心系统 + 多个彼此正交的周边系统”。事实上回调函数或者接口本质上就是一种事件监听机制，所以它是插件机制的特例。”

由业务到数据，由核心到周边，再把这个过程映射到开闭选择，再把开放性具体到插件与接口，下节课讲接口。老师这三节课真是步步深入啊。:

偷懒得说，要是画图代码在通用一些就好了</div>2019-12-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/db/26/54f2c164.jpg" width="30px"><span>靠人品去赢</span> 👍（1） 💬（1）<div>这么一想，微服务其实也是单一职责原则的实现。像普通业务的话，不清晰以后的方向，可能现在是工具类，后来又搞商城类，侧重点变化可能无法一下子就确定那些是稳定点，做着做着又是一大坨，哪里不行搞哪里，这种怎么解？</div>2019-12-06</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/09/8f/ad6039b6.jpg" width="30px"><span>沫沫（美丽人生）</span> 👍（1） 💬（3）<div>许老师好，很感谢您上次关于PaSS问题的回复，读您的文章让我受益匪浅。还想请教一个问题，像Salesforce是基于元数据来构建系统的，元数据在信息架构里属于什么范畴呢，可以展开来讲一讲吗？盼复。</div>2019-12-06</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/2e/4e/f6/6fffd759.jpg" width="30px"><span>chenyong</span> 👍（0） 💬（1）<div>开闭原则，可以理解为接口定义固定，接口实现可以增加？</div>2023-08-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1b/26/79/815237cd.jpg" width="30px"><span>王根福</span> 👍（0） 💬（1）<div>cpu的架构距离不够清晰呀，论述不够充分，个人意见</div>2020-10-16</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/ec/81/2127e215.jpg" width="30px"><span>梦醒十分</span> 👍（10） 💬（0）<div>入木三分，好文章!</div>2019-12-06</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/d0/4a/7e3d158d.jpg" width="30px"><span>沉睡的木木夕</span> 👍（3） 💬（0）<div>开闭原则：设计良好的系统应该是易于拓展，同时是抗拒修改的。
系统设计的好坏，开闭原则有最直接的关系。如果一个新的需求的实现，要大肆改动以前的代码，说明这个系统极其 “不稳定”，也是不符开闭原则的。

我们在设计实现一个需求时，我们首先要做的是，理解需求。要对不同的需求进行业务分组（代码分组），每组负责一个独立的业务逻辑，也就是 SRP。然后在处理这些分组之间的依赖关系。

“具体到代码就是将不同的操作（业务）划分不同的类，再将这些类分割为不同的组件” —— 《架构整洁之道》

在此在这里推荐这本书，许老在专栏的核心思想其实与这本书讲到的都一样。想成为一位好架构师，这本书我觉得必看。</div>2020-03-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/7f/a8/d103904b.jpg" width="30px"><span>mark</span> 👍（2） 💬（0）<div>这个课程的特点就是，每次读都有新的体会，或许这就是传说中的经典。</div>2021-01-25</li><br/><li><img src="https://wx.qlogo.cn/mmopen/vi_32/DYAIOgq83eop9WylZJicLQ5wib49kcMPqCTRT1aThh6mMAVl6qseLwbVOLhicVLjZCxCoyQd5CrrHHibs2CVPaoK3g/132" width="30px"><span>ljf10000</span> 👍（1） 💬（0）<div>感觉开闭原则跟自底向上设计很相似，都是先构建稳定的底层模块&#47;机制，再一层层组合出来。</div>2019-12-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/26/eb/d7/90391376.jpg" width="30px"><span>ifelse</span> 👍（0） 💬（0）<div>学习打卡</div>2023-10-05</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/27/0e/e4/7444469a.jpg" width="30px"><span>阿白</span> 👍（0） 💬（0）<div>水平太高了，没有足够实践很难全部消化。可惜没有机会现场听课</div>2022-05-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/22/0a/7d/ac715471.jpg" width="30px"><span>独孤九剑</span> 👍（0） 💬（0）<div>台上一分钟，台下十年功。感谢许总的分享！</div>2021-05-12</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTLMDBq7lqg9ZasC4f21R0axKJRVCBImPKlQF8yOicLLXIsNgsZxsVyN1mbvFOL6eVPluTNgJofwZeA/132" width="30px"><span>Run</span> 👍（0） 💬（0）<div>开开眼界</div>2021-03-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/be/30/1154657e.jpg" width="30px"><span>风含叶</span> 👍（0） 💬（0）<div>牛逼，发现了新大陆，从一个非常高的维度去理解问题。</div>2020-12-02</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/ywV5EjGPovkbcj9zRmibTKBQjAvCFrKVYMmGfDwGfcz6dmq6Sia1AlHvSX8ydibu2xueLuSen1YVDZSKNib1UTJBsQ/132" width="30px"><span>路人</span> 👍（0） 💬（0）<div>文章见功底</div>2020-05-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/55/f2/ba68d931.jpg" width="30px"><span>有米</span> 👍（0） 💬（0）<div>设计原则是内功心法，无论练什么招式都要谨记于心</div>2020-04-03</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/7e/bb/947c329a.jpg" width="30px"><span>程序员小跃</span> 👍（0） 💬（0）<div>这几节课都把我从单纯的写代码思维里拉出来，拉到架构的层次来看问题，而且“正交分解”深入我心，我感觉我写的不是代码，是艺术。

要做好这个艺术品，需要的东西太多了</div>2020-02-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/20/e7/9f082f47.jpg" width="30px"><span>轶名</span> 👍（0） 💬（0）<div>功力深厚啊</div>2019-12-13</li><br/>
</ul>