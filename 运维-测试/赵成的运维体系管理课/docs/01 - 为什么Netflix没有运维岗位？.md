众所周知，Netflix是业界微服务架构的最佳实践者，其基于公有云上的微服务架构设计、持续交付、监控、稳定性保障，都为业界提供了大量可遵从的原则和实践经验。

Netflix超前提出某些理念并付诸实践，以至于在国内众多互联网公司的技术架构上也可以看到似曾相识的影子。当然殊途同归也好，经验借鉴也罢，这都不影响Netflix业界最佳实践者的地位。

同样，在运维这个细分领域，Netflix仍然是最佳实践的典范。所以专栏的开始，就让我们一起看看世界顶级的互联网公司是如何定义运维以及如何开展运维工作的。

## Netflix运维现状

准确一点说，Netflix是没有运维岗位的，和运维对应的岗位其实是我们熟知的SRE（Site Reliability Engineer）。但我们知道SRE≠运维，**SRE理念的核心是：用软件工程的方法重新设计和定义运维工作**。

也就是要改变之前靠人去做运维的方式，转而通过工具体系、团队协作、组织机制和文化氛围等方式去改变，同时将之前处于研发体系最末端的运维，拉回到与开发肩并肩的同一起跑线上。

但是Netflix的神奇和强大之处在于，连Google都非常重视和大力发展的SRE岗位，在Netflix却没有几个。按照Netflix一位技术主管（Katharina Probst）在今年9月份更新的博客中所描述，在1亿用户，每天1.2亿播放时长、万级微服务实例的业务体量下，SRE人数竟然不超过10个，他们称这样的角色为Core SRE。描述具体如下：

> 100+ Million members. 125+ Million hours watched per day. Hundreds of  
> microservices. Hundreds of thousands of instances. Less than 10 Core  
> SREs.

不可否认，Netflix拥有强大的技术实力和全球最优秀的工程师团队。按照SRE的理念，完全可以打造出这一系列的工具产品来取代运维和SRE的工作。但是能够做到如此极致，就不得不让人惊叹和好奇，Netflix到底是怎么做到的？
<div><strong>精选留言（23）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/0f/bf/03/9e5c2259.jpg" width="30px"><span>宵伯特</span> 👍（17） 💬（1）<div>就像自动化取代传统手工业，技术的发展使得生产率提升的同时，也使得行业内的职能配置不断发生变化。现在大部分的软件行业由于敏捷开发的流行也逐渐的淘汰或替换了传统的QA部门，运维的职能也逐渐的从传统的手工业向自动化不断的改进，软件的生命周期也早已不是传统瀑布开发所规定的那样简单。从软件开发的历史来看，代码层级的一些规范也逐渐的向架构层次延展，像微服务的出现不就是kiss原则和dry原则在架构设计上的应用嘛。所以，从大的方向上来看软件行业的发展其实并没有那么快，绝大多数的改变和革新都只不过是过去的理论在现在合适的时刻得到了应用而已。</div>2017-12-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/c6/83/59641b08.jpg" width="30px"><span>白开水</span> 👍（14） 💬（1）<div>有具体的Netflix原则和最佳实践参考吗？</div>2017-12-21</li><br/><li><img src="" width="30px"><span>阿隆索</span> 👍（4） 💬（1）<div>作为运维人员如何权衡自己的发展呢？如果将来的运维人员的发展方向更偏于容器，k8s，自动化。那企业内应用，比如说windows的AD运维，exchange运维。企业如何在没有开发团队的基础上实现运维？开发团队如何在远离生产环境的模式中实现owner&amp;build？</div>2017-12-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/c3/92/9df49838.jpg" width="30px"><span>岑崟</span> 👍（3） 💬（1）<div>在组织架构设计方面有没有什么方法论层面的内容和方向</div>2017-12-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/69/2d/ff2fa54e.jpg" width="30px"><span>诺克大叔</span> 👍（2） 💬（1）<div>owner 直接体现了自带责任属性 可以避免好多推锅和定位故障难问题 </div>2018-03-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/c5/f7/0d7c1488.jpg" width="30px"><span>希望</span> 👍（2） 💬（1）<div>从专精的角度上考虑，开发和运维技术栈，看待问题的角度还是有所区别的，我比较好奇Netflix的开发人员如何做到既能关注自身开发的功能，又能关注到产品上线后的运维和部署架构？他们到达今天这个程度是开发的能力推动，还是因为运维基础平台的完善推动？</div>2018-01-23</li><br/><li><img src="" width="30px"><span>阿隆索</span> 👍（1） 💬（1）<div>传统应用的运维模式会逐渐转变到这种模式下吗？那运维外包业务岂不是会慢慢萎缩，运维人员的成长也被局限了</div>2017-12-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/fb/8b/a1feb0bf.jpg" width="30px"><span>华仔</span> 👍（0） 💬（1）<div>奈飞的贡献真大 到处都是它的影子</div>2020-03-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/bf/22/26530e66.jpg" width="30px"><span>趁早</span> 👍（0） 💬（1）<div>那具体的话，作为一个owner如何保障自己“随意”每次提交的代码没有问题？ </div>2019-01-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/cd/e0/c85bb948.jpg" width="30px"><span>朱雯</span> 👍（8） 💬（0）<div>运维价值
1:定义范围:除了业务需求实现层面，其他都是运维
价值所在：运维能力就是架构能力,运维层面爆发问题或者故障，一定是技术架构中的问题，单纯看待没有意义
矛盾:割裂运维和开发，按照软件生命周期开始划分运维和开发，所以应该先转换运维思路，后提升运维技术，让运维和研发团队保持一致，聚焦效率，稳定和成本

netflix 运维现状
sre运维: 用软件工程的方法重新设计和定义运维工作
方式：微服务化
代价和成本:架构复杂度大大增加,无法人力掌控，后续的交付和线上运维难度提高，必须通过软件工程思路打造工具体系支持。
例子：比如服务上下线、路由策略调整、并发数动态调整、功能开关、访问...
为什么微服务会产生sre: 微服务架构复杂到了一定的程度，已经远远超过单纯开发和运维的职责范围，也超过了单纯人力的认知掌控范畴，所以必须的有效的统一的解决方案必须出现
自由与责任并存的企业文化:ower意识，谁构建谁负责

netflix启示一：微服务架构模式下，我们必须换一个思路来重新定义和思考运，运维一定要与微服务架构本身紧密结合起来
Netflix 带给我们的启示二：合理的组织架构是保障技术架构是落地的必要条件，用技术手段来解决运维过程中遇到的效率和稳定问题才是根本解决方案

应用:从整体服务拆出来的独立模块，每个模块只执行一个功能，可以独立运行和部署。每一个应用都有单一的业务职能，如果要完成整体的业务流程和目标，那么需要和其他应用交互，同时执行过程中会和其他的基础设施和组件进行交互，比如机器，域名，db,缓存，消息队列等
</div>2019-04-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/86/fa/4bcd7365.jpg" width="30px"><span>玉剑冰锋</span> 👍（7） 💬（0）<div>老师您好，听了两小节了课程了，有几个想法想听听您的见解:1.案例中提到的毕竟是整个行业的风向标或者说是趋势，但是这毕竟是大公司或者具备很强团队才能达到预期效果，如果一个公司才几十个人或者上百人，这种情况该如何处理？2.我相信大部分中小型公司运维岗位还是必须要设立的，而且更多的是人肉运维，是否能给这些人一些建议或者发现方向，谢谢！</div>2018-09-03</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/b8/24/039f84a2.jpg" width="30px"><span>咱是吓大的</span> 👍（2） 💬（0）<div>这就要求集开发、测试、运维于一身，或于一个团队，而不是根据分工硬生生把人员分到不同部门</div>2020-11-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/75/9b/611e74ab.jpg" width="30px"><span>技术修行者</span> 👍（2） 💬（1）<div>Netflix带给我的最大启示就是Ownership，要在平时的工作中更具备主人翁意识，You build it, you own it.
最近几年微服务改造如火如荼，很多系统都被改造成微服务架构，很多新项目一开始做设计时，就拆分成很多服务。但是在服务监控运维方面，做的不到位，大部分时候都是想着服务设计出来了，功能实现了，交付上线了，剩下的事情，就是运维团队的责任了，和我没有关系了。
不要给自己设定边界，适当跨出舒适区，站在更高的角度，看待自己的工作，完整交付自己工作的价值，这样才会更有意义。</div>2020-05-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/92/6d/becd841a.jpg" width="30px"><span>escray</span> 👍（1） 💬（0）<div>我觉的说 Netflix 没有运维岗位，和之前一段时间说某某大公司没有测试岗位一样，其实职能还在，只不过合并到了开发人员那一端。

另外我觉的 Netflix 的“You Build it, You Run ti”，和之前常说的“Eating your own dog food”还不完全一样。dog food 更多的时强调要自己去使用自己的产品，而 “Run” 似乎就包括了运营和运维。自己的产品如果不好用，那么自己明显能感受到种种不便；自己的产品如果故障太多，或者没法运维，那么也会让  Owner 焦头烂额。

但是有一个想法，是否是因为 Netflix 的产品线相对比较单一，我知道的只有视频网站这一块，所以它才能把微服务包括其运维体系做成这个样子，当然其开发人员的功力应该也比较高。如果业务比较复杂，是否就没有办法按照 Netflix 的风格去做运维。

在体制内单位，对市场上的软件行业不是特别的了解，但是我觉的应该还没有到“用敏捷开发代替传统 QA”的程度，甚至很多开发商连测试和配置管理可能都不是很正规。那么对于现阶段的情况，一般的软件公司瞄准 Google 的 SRE 体系，是否更加合适一点？

无论是 Google 还是 Netflix 其实都把运维提高到了相对全局，并且权重比较大的位置；而且对于个人能力的要求也比较高，我觉的这应该也是运维人员的机会。

（不好意思，因为遇到了敏感词，所以留言分了好几部分，最后发现是 dog food 的中文，不知道为什么这个比较敏感）</div>2020-01-04</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/4c/fc/0e887697.jpg" width="30px"><span>kkgo</span> 👍（1） 💬（0）<div>这种技术储备要掌握那些技能</div>2018-09-05</li><br/><li><img src="" width="30px"><span>阿隆索</span> 👍（1） 💬（0）<div>我能明白市场选择所带来的阵痛，不管是对企业对个人。其实运维主要面临两个问题：一个是企业方面，如果市场趋势如此，那企业在选择业务服务的话，是否应该把运维独立出来以服务的形式提供，并且押宝在上面。另一个就是运维人员，因为如果按照这种趋势下去，运维最终会由工具的使用者转变为工具的制造者。这个转变是巨大的，也有会一部分开发者进入这一领域，对传统运维冲击很大。另外就是对第三方独立应用来说，如何提供产品，以及后续的交付都是值得深思的地方。</div>2017-12-25</li><br/><li><img src="" width="30px"><span>leo</span> 👍（1） 💬（1）<div>期待后续更新</div>2017-12-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/22/e2/31/d8a6e429.jpg" width="30px"><span>皇甫冉</span> 👍（0） 💬（0）<div>是的，核心还是公司文化使然，这才是根因。</div>2024-03-12</li><br/><li><img src="" width="30px"><span>幻灭一只狼</span> 👍（0） 💬（0）<div>日常发布变更管控，从sre 角度，怎么做呀</div>2022-04-16</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/eb/c9/b1b233cf.jpg" width="30px"><span>小伟</span> 👍（0） 💬（0）<div>理想状态是：业务只需写业务代码，其他的（数据一致性、稳定性、发布、安全、问题定位等等）都不需要关注或仅需很少成本；这样业务进展会很快，商业上回报也会很大；
相应的，会给非业务的投入会增多，形成一个良性循环。</div>2020-07-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/1a/66/2d9db9ed.jpg" width="30px"><span>苦行僧</span> 👍（0） 💬（0）<div>you build it ，you run it</div>2019-03-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/07/66/1328e652.jpg" width="30px"><span>cc</span> 👍（0） 💬（0）<div>很有感触，我觉得这种模式正是需要的，运维不能只做背锅侠</div>2018-11-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/47/0f/eeb52659.jpg" width="30px"><span>大爷静悄悄</span> 👍（0） 💬（0）<div>Netflix 带给我们的启示二：合理的组织架构是保障技术架构落地的必要条件，用技术手段来解决运维过程中遇到的效率和稳定问题才是根本解决方案。</div>2018-05-20</li><br/>
</ul>